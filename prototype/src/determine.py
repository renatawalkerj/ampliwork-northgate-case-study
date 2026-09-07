#!/usr/bin/env python3
"""
Northgate prototype — determination engine.

Ugly-but-works, deliberately: reads the synthetic data, runs each transaction
through the pipeline, and writes a flat CSV (a "sheet") the analyst opens
directly. No UI. She still makes the actual SAP entry herself — this tool
recommends, it never writes (FR7, FR3a).

Pipeline per transaction, in order:
  1. Entity resolution (deterministic, no LLM) — does this supplier's resolved
     vendor records disagree on tax classification / VAT ID? (FR2a, DR2)
  2. Compliance check (deterministic, no LLM) — are this jurisdiction's
     mandatory fields all present? (FR6)
  3. If either check fails: skip the LLM, the case is already low-confidence
     and the reasoning is templated directly from the structured facts.
  4. If both checks pass: retrieve the approved knowledge-base entries for
     this transaction's jurisdiction (RAG — FR12), and call the LLM with the
     invoice, the resolved vendor profile, the jurisdiction rule, and that
     retrieved context to get the three-part determination + confidence.
  5. Time-to-expiration (deterministic, no LLM) — jurisdiction rule type
     applied to this transaction's own invoice date (FR4).

Requires: GEMINI_API_KEY env var. Model name is configurable (GEMINI_MODEL)
since it will drift — set it to whatever's current when you run this.

Usage:
    export GEMINI_API_KEY=...
    python3 determine.py
    # writes ../output/determination_sheet.csv
"""

import csv
import json
import os
import sys
from datetime import date, timedelta

try:
    import google.generativeai as genai
except ImportError:
    print("Missing dependency. Run: pip install google-generativeai", file=sys.stderr)
    sys.exit(1)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")


def load_data():
    with open(os.path.join(DATA_DIR, "jurisdictions.json")) as f:
        jurisdictions = {j["code"]: j for j in json.load(f)["jurisdictions"]}
    with open(os.path.join(DATA_DIR, "vendor_master_records.json")) as f:
        vmr = json.load(f)
        vendor_records = {v["vendor_record_id"]: v for v in vmr["vendor_master_records"]}
        entity_resolution_map = vmr["entity_resolution_map"]
    with open(os.path.join(DATA_DIR, "invoices.json")) as f:
        invoices_doc = json.load(f)
        invoices = invoices_doc["invoices"]
        as_of_date = date.fromisoformat(invoices_doc["as_of_date"])
    with open(os.path.join(DATA_DIR, "knowledge_base.json")) as f:
        kb_entries = json.load(f)["knowledge_base_entries"]
    return jurisdictions, vendor_records, entity_resolution_map, invoices, as_of_date, kb_entries


def check_entity_conflict(invoice, vendor_records, entity_resolution_map):
    """Deterministic — FR2a/DR2. No LLM needed: this is a structured comparison."""
    vendor_id = invoice["vendor_record_id"]
    vendor = vendor_records[vendor_id]
    supplier_id = vendor["real_world_supplier_id"]
    related_ids = entity_resolution_map.get(supplier_id, [vendor_id])
    related = [vendor_records[rid] for rid in related_ids]

    if len(related) <= 1:
        return False, None, related

    tax_classes = {r["tax_classification"] for r in related}
    vat_ids = {r["vat_id"] for r in related}
    conflict = len(tax_classes) > 1 or len(vat_ids) > 1
    return conflict, supplier_id, related


def check_compliance(invoice, jurisdiction):
    """Deterministic — FR6. Set difference, no LLM needed."""
    required = set(jurisdiction["invoice_compliance"]["mandatory_fields"])
    present = set(invoice["fields_present"])
    missing = required - present
    return (len(missing) == 0), sorted(missing)


def time_to_expiration_days(invoice, jurisdiction, as_of_date):
    """Deterministic — FR4. Two rule shapes: rolling-years and return-deadline-bound."""
    invoice_date = date.fromisoformat(invoice["invoice_date"])
    rule = jurisdiction["reclaim_window"]

    if rule["rule_type"] == "rolling_years":
        expiry = invoice_date.replace(year=invoice_date.year + rule["value_years"])
    elif rule["rule_type"] == "return_deadline_bound":
        # Deadline is <deadline_month>/<deadline_day> of the year AFTER the
        # right arose (invoice_date's year) — matches Italy's DPR 633/72
        # mechanic already documented in claims.md.
        deadline_year = invoice_date.year + 1
        expiry = date(deadline_year, rule["annual_return_deadline_month"], rule["annual_return_deadline_day"])
    else:
        raise ValueError(f"Unknown reclaim-window rule_type: {rule['rule_type']}")

    return (expiry - as_of_date).days


def retrieve_kb_context(jurisdiction_code, kb_entries):
    """RAG retrieval — FR12. Only APPROVED entries for this jurisdiction ever
    reach the prompt. A pending_review entry must never influence a live
    determination (FR12a) — this filter is the enforcement point."""
    return [
        e for e in kb_entries
        if e["jurisdiction"] == jurisdiction_code and e["status"] == "approved"
    ]


def build_prompt(invoice, vendor, jurisdiction, kb_context):
    kb_text = "\n".join(f"- {e['rule']} (source: {e['id']})" for e in kb_context) or "(none for this jurisdiction yet)"
    return f"""You are a tax-determination assistant for an indirect-tax team. You do not
file anything — you only recommend. Answer strictly as JSON.

TRANSACTION
Invoice: {invoice['invoice_number']}, dated {invoice['invoice_date']}
Jurisdiction: {jurisdiction['name']} ({jurisdiction['code']})
Net amount: {invoice.get('net_amount')}
VAT rate charged: {invoice.get('vat_rate_charged')}
Notes: {invoice.get('vat_rate_charged_note', invoice.get('jurisdiction_note', ''))}

RESOLVED SUPPLIER (single, no conflict — already checked)
{vendor['supplier_name_as_recorded']} — tax classification: {vendor['tax_classification']}

JURISDICTION RULE
Standard VAT rate: {jurisdiction['vat_standard_rate']}

KNOWN EXCEPTIONS FOR THIS JURISDICTION (approved knowledge-base entries — apply these
if relevant to this specific transaction; do not invent exceptions not listed here)
{kb_text}

LINKED EVIDENCE
{json.dumps(invoice.get('linked_evidence', {}), indent=2)}

Determine, per the invoice: (1) was tax charged correctly, (2) is it recoverable,
(3) which jurisdiction should it be reported in. If the linked evidence is
insufficient to answer confidently (e.g. a referenced contract isn't attached),
say so — do not guess. Respond as JSON only:
{{
  "charged_correctly": true | false | "indeterminate_without_<what's missing>",
  "recoverable": true | false | "indeterminate_without_<what's missing>",
  "reporting_jurisdiction": "<jurisdiction code>",
  "confidence": "high" | "low",
  "reasoning": "<2-3 sentences, plain language, cite the knowledge-base entry id if one applied>"
}}"""


def call_llm(model, prompt):
    response = model.generate_content(prompt)
    text = response.text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{"):]
    return json.loads(text)


def main():
    jurisdictions, vendor_records, entity_resolution_map, invoices, as_of_date, kb_entries = load_data()

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(MODEL_NAME)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    rows = []

    for invoice in invoices:
        jurisdiction = jurisdictions[invoice["jurisdiction"]]
        vendor = vendor_records[invoice["vendor_record_id"]]

        conflict, supplier_id, related_records = check_entity_conflict(
            invoice, vendor_records, entity_resolution_map
        )
        compliant, missing_fields = check_compliance(invoice, jurisdiction)
        ttx_days = time_to_expiration_days(invoice, jurisdiction, as_of_date)

        if conflict:
            record_lines = "; ".join(
                f"{r['vendor_record_id']} ({r['sap_instance']}): {r['tax_classification']}, {r['vat_id']}"
                for r in related_records
            )
            row = {
                "invoice_id": invoice["invoice_id"],
                "supplier": vendor["supplier_name_as_recorded"],
                "jurisdiction": invoice["jurisdiction"],
                "charged_correctly": "INDETERMINATE",
                "recoverable": "INDETERMINATE - entity conflict",
                "reporting_jurisdiction": invoice["jurisdiction"],
                "confidence": "low",
                "time_to_expiration_days": ttx_days,
                "flag": "ENTITY_CONFLICT",
                "reasoning": (
                    f"Supplier {supplier_id} has {len(related_records)} vendor records with "
                    f"conflicting tax profiles, not resolved from a single source of truth: {record_lines}. "
                    f"Route to analyst — do not auto-process (FR2a)."
                ),
                "kb_entries_used": "",
                "recommended_action": "Escalate for review — resolve which vendor record is correct.",
            }
        elif not compliant:
            row = {
                "invoice_id": invoice["invoice_id"],
                "supplier": vendor["supplier_name_as_recorded"],
                "jurisdiction": invoice["jurisdiction"],
                "charged_correctly": "CANNOT_DETERMINE",
                "recoverable": "BLOCKED - compliance failure",
                "reporting_jurisdiction": invoice["jurisdiction"],
                "confidence": "low",
                "time_to_expiration_days": ttx_days,
                "flag": "COMPLIANCE_FAIL",
                "reasoning": (
                    f"Missing mandatory field(s) for {jurisdiction['name']}: {', '.join(missing_fields)}. "
                    f"Recoverability cannot be scored until the invoice is corrected (FR6)."
                ),
                "kb_entries_used": "",
                "recommended_action": f"Request corrected invoice from supplier (missing: {', '.join(missing_fields)}).",
            }
        else:
            kb_context = retrieve_kb_context(invoice["jurisdiction"], kb_entries)
            prompt = build_prompt(invoice, vendor, jurisdiction, kb_context)
            result = call_llm(model, prompt)
            row = {
                "invoice_id": invoice["invoice_id"],
                "supplier": vendor["supplier_name_as_recorded"],
                "jurisdiction": invoice["jurisdiction"],
                "charged_correctly": result.get("charged_correctly"),
                "recoverable": result.get("recoverable"),
                "reporting_jurisdiction": result.get("reporting_jurisdiction"),
                "confidence": result.get("confidence"),
                "time_to_expiration_days": ttx_days,
                "flag": "" if result.get("confidence") == "high" else "NEEDS_REVIEW",
                "reasoning": result.get("reasoning", ""),
                "kb_entries_used": ", ".join(e["id"] for e in kb_context) or "(none)",
                "recommended_action": (
                    "Batch-confirm, then file in SAP yourself (FR7)."
                    if result.get("confidence") == "high"
                    else "Review evidence, then decide and file in SAP yourself (FR7)."
                ),
            }

        rows.append(row)
        print(f"{invoice['invoice_id']}: {row['flag'] or 'ok'} (confidence={row['confidence']})")

    # Sort by urgency (time-to-expiration) then confidence — FR5, not confidence alone.
    rows.sort(key=lambda r: (r["time_to_expiration_days"], 0 if r["confidence"] == "low" else 1))

    out_path = os.path.join(OUTPUT_DIR, "determination_sheet.csv")
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} rows to {out_path}")
    print("Open this in Excel/Sheets — this is the demo. No UI required for v1.")


if __name__ == "__main__":
    main()
