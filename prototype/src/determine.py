#!/usr/bin/env python3
"""
Northgate prototype — determination engine, v2 (realistic inputs).

Starts from what the analyst would actually have, not a pre-merged answer key:
- 3 separate SAP exports (`input/sap_eu_1_export.csv`, `_2_`, `_3_`) — one per
  instance, exactly like the "pull three separate AP voucher registers"
  09:00 task in the day-in-the-life. This tool automates that consolidation
  step, it doesn't skip past it.
- Her own shadow spreadsheet (`input/emea_vat_exceptions.csv`) — the regional-
  spreadsheets data source, formalized (FR12), read as an actual CSV she'd
  recognize, not a clean database table.
- `input/jurisdictions.json` — reference config the tool ships with (not
  something she personally exports; the tax rules aren't hers to maintain).

Entity resolution (FR2a/DR2) is COMPUTED here, not looked up from a
precomputed map — normalized-name similarity + VAT-ID closeness across all
3 exports. This is the real capability: given three exports that don't know
about each other, find the supplier that's the same real-world entity under
three different names and three different tax profiles.

Pipeline per transaction:
  1. Consolidate the 3 SAP exports (deterministic).
  2. Resolve entities across the consolidated vendor rows (deterministic).
  3. Compliance check against jurisdiction rules (deterministic).
  4. If entity conflict or compliance failure: skip the LLM, template the
     reasoning directly from the structured facts.
  5. Otherwise: retrieve approved knowledge-base entries for the transaction's
     jurisdiction (RAG, FR12) and call the LLM for the three-part
     determination + confidence.
  6. Time-to-expiration (deterministic) drives the final sort (FR4/FR5).

Requires: GEMINI_API_KEY env var. Model name is configurable (GEMINI_MODEL)
since it will drift.

Usage:
    python3 determine.py
    # writes ../output/determination_sheet.csv
"""

import csv
import json
import os
import re
import sys
from datetime import date
from difflib import SequenceMatcher

try:
    import google.generativeai as genai
except ImportError:
    print("Missing dependency. Run: pip3 install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

INPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "input")
DOCUMENTS_DIR = os.path.join(INPUT_DIR, "documents")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
AS_OF_DATE = date(2026, 9, 6)

SAP_EXPORTS = ["sap_eu_1_export.csv", "sap_eu_2_export.csv", "sap_eu_3_export.csv"]
LEGAL_SUFFIX_RE = re.compile(r"\b(b\.?v\.?|gmbh|ltd\.?|sarl|s\.r\.o\.?|inc\.?|llc|corp\.?)\b")
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


# ---------- Step 1: consolidate the 3 SAP exports (her old 09:00 task) ----------

def load_and_consolidate_sap_exports():
    """Reads the 3 separate exports and merges them into one list — this is
    the manual multi-system reconciliation from the day-in-the-life,
    automated. Each row is one vendor-appearance-in-an-instance, with invoice
    fields populated only if that vendor had a transaction this period."""
    all_rows = []
    per_file_counts = {}
    for filename in SAP_EXPORTS:
        path = os.path.join(INPUT_DIR, filename)
        with open(path, newline="") as f:
            rows = list(csv.DictReader(f))
        per_file_counts[filename] = len(rows)
        all_rows.extend(rows)

    print("Consolidating 3 SAP exports (the old 09:00 manual task, automated):")
    for filename, count in per_file_counts.items():
        print(f"  {filename}: {count} rows")
    print(f"  -> {len(all_rows)} total vendor appearances across 3 instances")
    return all_rows


def load_kb_csv():
    path = os.path.join(INPUT_DIR, "emea_vat_exceptions.csv")
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def load_jurisdictions():
    with open(os.path.join(INPUT_DIR, "jurisdictions.json")) as f:
        return {j["code"]: j for j in json.load(f)["jurisdictions"]}


# ---------- Step 2: entity resolution, computed, not looked up ----------

def normalize_name(name):
    n = name.lower()
    n = LEGAL_SUFFIX_RE.sub(" ", n)
    n = NON_ALNUM_RE.sub(" ", n).strip()
    return n


def names_similar(a, b, threshold=0.6):
    return SequenceMatcher(None, normalize_name(a), normalize_name(b)).ratio() > threshold


def vat_ids_similar(a, b):
    """Same country prefix, same length, at most 1 digit different —
    catches a plausible stale/mistyped VAT ID (e.g. the Vantpoint case)."""
    if not a or not b:
        return False
    if a == b:
        return True
    if len(a) != len(b) or a[:2] != b[:2]:
        return False
    diffs = sum(1 for x, y in zip(a, b) if x != y)
    return diffs <= 1


def resolve_entities(vendor_rows):
    """Naive O(n^2) clustering — fine at prototype scale. Groups rows that
    are plausibly the same real-world supplier by name similarity OR VAT-ID
    closeness. Returns vendor_record_id -> list of all rows in its cluster."""
    clusters = []
    for row in vendor_rows:
        placed = False
        for cluster in clusters:
            rep = cluster[0]
            if names_similar(row["supplier_name_as_recorded"], rep["supplier_name_as_recorded"]) or \
               vat_ids_similar(row["vat_id"], rep["vat_id"]):
                cluster.append(row)
                placed = True
                break
        if not placed:
            clusters.append([row])

    vendor_to_cluster = {}
    for cluster in clusters:
        for row in cluster:
            vendor_to_cluster[row["vendor_record_id"]] = cluster
    return vendor_to_cluster


def check_entity_conflict(vendor_row, vendor_to_cluster):
    """Deterministic — FR2a/DR2. The cluster was computed above; this just
    checks whether its members disagree on tax profile."""
    cluster = vendor_to_cluster[vendor_row["vendor_record_id"]]
    if len(cluster) <= 1:
        return False, cluster
    tax_classes = {r["tax_classification"] for r in cluster}
    vat_ids = {r["vat_id"] for r in cluster}
    conflict = len(tax_classes) > 1 or len(vat_ids) > 1
    return conflict, cluster


# ---------- Step 3: compliance check ----------

def check_compliance(invoice_row, jurisdiction):
    """Deterministic — FR6."""
    required = set(jurisdiction["invoice_compliance"]["mandatory_fields"])
    present = set(invoice_row["fields_present"].split("|")) if invoice_row["fields_present"] else set()
    missing = required - present
    return (len(missing) == 0), sorted(missing)


# ---------- Step 4: time-to-expiration ----------

def time_to_expiration_days(invoice_row, jurisdiction, as_of_date):
    """Deterministic — FR4. Two rule shapes: rolling-years and return-deadline-bound."""
    invoice_date = date.fromisoformat(invoice_row["invoice_date"])
    rule = jurisdiction["reclaim_window"]
    if rule["rule_type"] == "rolling_years":
        return (invoice_date.replace(year=invoice_date.year + rule["value_years"]) - as_of_date).days
    elif rule["rule_type"] == "return_deadline_bound":
        deadline = date(invoice_date.year + 1, rule["annual_return_deadline_month"], rule["annual_return_deadline_day"])
        return (deadline - as_of_date).days
    raise ValueError(f"Unknown reclaim-window rule_type: {rule['rule_type']}")


# ---------- Step 5: RAG retrieval + LLM determination ----------

def retrieve_kb_context(jurisdiction_code, kb_rows):
    """RAG retrieval — FR12. Only APPROVED entries for this jurisdiction ever
    reach the prompt (FR12a's enforcement point)."""
    return [r for r in kb_rows if r["jurisdiction"] == jurisdiction_code and r["status"] == "approved"]


def load_document_text(reference):
    """Structured vs. unstructured, drawn as a hard line (per the source-data map in
    `answers/03-information-model.md`): SAP/the tax engine hold structured system
    records only — this function is the ONLY place the pipeline reaches into the
    unstructured document pool (PDFs/mailbox/contracts, extracted to text here).
    Returns None if no document exists for this reference — that absence is itself
    meaningful (see INV-1005's original 'referenced, not attached' state) and must
    reach the LLM as an explicit absence, not be silently skipped."""
    if not reference:
        return None
    ref_id = reference.split(" ")[0].strip()  # strip trailing notes like "(referenced, not attached)"
    if not os.path.isdir(DOCUMENTS_DIR):
        return None
    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.startswith(ref_id):
            with open(os.path.join(DOCUMENTS_DIR, filename)) as f:
                return f.read().strip()
    return None


def build_prompt(invoice_row, jurisdiction, kb_context):
    kb_text = "\n".join(f"- {e['rule']} (source: {e['id']})" for e in kb_context) or "(none for this jurisdiction yet)"

    po_ref = invoice_row.get("purchase_order")
    contract_ref = invoice_row.get("contract")
    customs_ref = invoice_row.get("customs_ref")

    invoice_doc_text = load_document_text(invoice_row["invoice_id"])  # unstructured: the actual invoice PDF text
    contract_text = load_document_text(contract_ref)                  # unstructured
    customs_text = load_document_text(customs_ref)                    # unstructured

    return f"""You are a tax-determination assistant for an indirect-tax team. You do not
file anything — you only recommend. Answer strictly as JSON.

=== STRUCTURED SYSTEM RECORDS (SAP + tax engine — what the system already "knows") ===
Invoice: {invoice_row['invoice_number']}, dated {invoice_row['invoice_date']}
Supplier: {invoice_row['supplier_name_as_recorded']} (single resolved profile, no conflict — already checked)
Tax classification on file: {invoice_row['tax_classification']}
Native SAP tax code applied: {invoice_row.get('native_tax_code') or '(not recorded)'}
Jurisdiction: {jurisdiction['name']} ({jurisdiction['code']})
Net amount: {invoice_row['net_amount']}
VAT rate charged: {invoice_row['vat_rate_charged']}
VAT amount actually charged: {invoice_row['vat_amount_charged']} (cross-check this against net_amount x vat_rate_charged yourself — a mismatch is itself a signal)
Purchase order: {po_ref or '(none)'} — PO amount {invoice_row.get('po_amount') or 'n/a'}, quantity {invoice_row.get('po_quantity') or 'n/a'}, GL/cost center {invoice_row.get('gl_cost_center') or 'n/a'}
Goods receipt: {invoice_row.get('goods_receipt') or '(none — not yet confirmed received)'}
Notes on file: {invoice_row.get('notes', '')}

This is what SAP's flat line description would show you: a vendor, an amount, a rigid
tax code, and a cost-center number. It does NOT tell you what was actually purchased or
why — that requires the unstructured evidence below, when it exists.

=== JURISDICTION RULE ===
Standard VAT rate: {jurisdiction['vat_standard_rate']}

=== KNOWN EXCEPTIONS FOR THIS JURISDICTION (approved knowledge-base entries — retrieved
because they're approved for this jurisdiction; being retrieved does NOT mean one applies) ===
{kb_text}

=== UNSTRUCTURED DOCUMENT CONTEXT (PDFs/mailbox/contracts — invisible to SAP and the tax
engine; this is the only part of this prompt where that content is actually read, not just
referenced) ===
Invoice document text: {invoice_doc_text or '(not available — no extracted text for this invoice; determine only from the structured records above)'}

Contract ({contract_ref or 'none referenced'}): {contract_text if contract_ref else '(none referenced)'}{' — REFERENCED BUT NOT ATTACHED, no text available' if (contract_ref and not contract_text) else ''}

Customs paperwork ({customs_ref or 'none referenced'}): {customs_text if customs_ref else '(none referenced — not a cross-border goods movement, or not applicable)'}

Determine, per the invoice: (1) was tax charged correctly, (2) is it recoverable,
(3) which jurisdiction should it be reported in. Use the unstructured document context
above to resolve what the structured records alone cannot — a vague SAP line description
or a default tax code is not the final answer if the actual invoice text, contract, or
customs paperwork tells a different story. If a document is referenced but its text isn't
available, say so explicitly — do not guess at what it might contain.

On the knowledge-base entries above: list an entry in "kb_entries_applied" ONLY if
you can state, specifically, which fact of THIS transaction makes it apply — not
because it was merely available. If none of the listed entries actually apply,
"kb_entries_applied" must be an empty list. Being topically related to the
jurisdiction is not sufficient justification.

Respond as JSON only:
{{
  "charged_correctly": true | false | "indeterminate_without_<what's missing>",
  "recoverable": true | false | "indeterminate_without_<what's missing>",
  "reporting_jurisdiction": "<jurisdiction code>",
  "confidence": "high" | "low",
  "kb_entries_applied": ["<entry id>", ...] | [],
  "reasoning": "<2-3 sentences, plain language. If kb_entries_applied is non-empty, state which specific fact of this transaction triggered that entry.>"
}}"""


def call_llm(model, prompt):
    response = model.generate_content(prompt)
    text = response.text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{"):]
    return json.loads(text)


def main():
    all_vendor_rows = load_and_consolidate_sap_exports()
    kb_rows = load_kb_csv()
    jurisdictions = load_jurisdictions()

    vendor_to_cluster = resolve_entities(all_vendor_rows)
    distinct_clusters = {tuple(sorted(r["vendor_record_id"] for r in c)) for c in vendor_to_cluster.values()}
    print(f"Entity resolution: {len(all_vendor_rows)} vendor appearances -> "
          f"{len(distinct_clusters)} distinct real-world suppliers computed (not looked up)")
    for cluster_ids in distinct_clusters:
        if len(cluster_ids) > 1:
            print(f"  cluster: {', '.join(cluster_ids)}")

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(MODEL_NAME)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    rows = []

    # Only rows that actually carry an invoice this period are transactions
    # to determine — the vendor-master-only rows exist purely so entity
    # resolution has something to cross-reference against.
    invoice_rows = [r for r in all_vendor_rows if r.get("invoice_id")]

    for invoice_row in invoice_rows:
        jurisdiction = jurisdictions[invoice_row["jurisdiction"]]
        conflict, cluster = check_entity_conflict(invoice_row, vendor_to_cluster)
        compliant, missing_fields = check_compliance(invoice_row, jurisdiction)
        ttx_days = time_to_expiration_days(invoice_row, jurisdiction, AS_OF_DATE)

        if conflict or not compliant:
            # Both checks are independent and both must be reported if both fire —
            # a transaction can be simultaneously a duplicate-vendor conflict AND
            # missing a mandatory field. An if/elif here would silently drop
            # whichever check ran second; that's exactly the kind of thing that
            # doesn't show up as a wrong answer, only as an incomplete one.
            flags, reasoning_parts, actions = [], [], []

            if conflict:
                # De-dupe by vendor_record_id: `cluster` holds one row per invoice
                # appearance, so a vendor with more than one invoice this period
                # would otherwise get listed (and counted) more than once here,
                # even though it's still a single distinct vendor record.
                distinct_records = list({r["vendor_record_id"]: r for r in cluster}.values())
                record_lines = "; ".join(
                    f"{r['vendor_record_id']} ({r['sap_instance']}): {r['tax_classification']}, {r['vat_id']}"
                    for r in distinct_records
                )
                flags.append("ENTITY_CONFLICT")
                reasoning_parts.append(
                    f"This supplier resolves to {len(distinct_records)} vendor records across SAP instances with "
                    f"conflicting tax profiles, computed from 3 separate exports that didn't know about "
                    f"each other: {record_lines}. Route to analyst — do not auto-process (FR2a)."
                )
                actions.append("Escalate for review — resolve which vendor record is correct.")

            if not compliant:
                flags.append("COMPLIANCE_FAIL")
                reasoning_parts.append(
                    f"Missing mandatory field(s) for {jurisdiction['name']}: {', '.join(missing_fields)}. "
                    f"Recoverability cannot be scored until the invoice is corrected (FR6)."
                )
                actions.append(f"Request corrected invoice from supplier (missing: {', '.join(missing_fields)}).")

            row = {
                "invoice_id": invoice_row["invoice_id"],
                "supplier": invoice_row["supplier_name_as_recorded"],
                "jurisdiction": invoice_row["jurisdiction"],
                "charged_correctly": "INDETERMINATE" if conflict else "CANNOT_DETERMINE",
                "recoverable": "INDETERMINATE - entity conflict" if conflict else "BLOCKED - compliance failure",
                "reporting_jurisdiction": invoice_row["jurisdiction"],
                "confidence": "low",
                "time_to_expiration_days": ttx_days,
                "flag": " + ".join(flags),
                "reasoning": " ".join(reasoning_parts),
                "kb_entries_used": "",
                "kb_entries_retrieved": "",
                "recommended_action": " ".join(actions),
            }
        else:
            kb_context = retrieve_kb_context(invoice_row["jurisdiction"], kb_rows)
            prompt = build_prompt(invoice_row, jurisdiction, kb_context)
            try:
                result = call_llm(model, prompt)
            except Exception as e:
                # A single failed call (rate limit, quota, transient API error) must
                # not lose every other row's already-computed result — write what we
                # have and flag this one for a re-run, rather than crashing silently.
                rows.append({
                    "invoice_id": invoice_row["invoice_id"],
                    "supplier": invoice_row["supplier_name_as_recorded"],
                    "jurisdiction": invoice_row["jurisdiction"],
                    "charged_correctly": "LLM_CALL_FAILED", "recoverable": "LLM_CALL_FAILED",
                    "reporting_jurisdiction": invoice_row["jurisdiction"], "confidence": "low",
                    "time_to_expiration_days": ttx_days, "flag": "RETRY_NEEDED",
                    "reasoning": f"Model call failed: {type(e).__name__}: {e}. Re-run determine.py to retry just this determination once the underlying issue (e.g. rate/quota limit) clears.",
                    "kb_entries_used": "", "kb_entries_retrieved": "", "recommended_action": "Re-run and review — not yet determined.",
                })
                print(f"{invoice_row['invoice_id']}: LLM call failed ({type(e).__name__}) — recorded as RETRY_NEEDED, continuing")
                continue
            retrieved_ids = {e["id"] for e in kb_context}
            applied = [a for a in result.get("kb_entries_applied", []) if a in retrieved_ids]
            row = {
                "invoice_id": invoice_row["invoice_id"],
                "supplier": invoice_row["supplier_name_as_recorded"],
                "jurisdiction": invoice_row["jurisdiction"],
                "charged_correctly": result.get("charged_correctly"),
                "recoverable": result.get("recoverable"),
                "reporting_jurisdiction": result.get("reporting_jurisdiction"),
                "confidence": result.get("confidence"),
                "time_to_expiration_days": ttx_days,
                "flag": "" if result.get("confidence") == "high" else "NEEDS_REVIEW",
                "reasoning": result.get("reasoning", ""),
                "kb_entries_used": ", ".join(applied) or "(none applied)",
                "kb_entries_retrieved": ", ".join(retrieved_ids) or "(none)",
                "recommended_action": (
                    "Batch-confirm, then file in SAP yourself (FR7)."
                    if result.get("confidence") == "high"
                    else "Review evidence, then decide and file in SAP yourself (FR7)."
                ),
            }

        rows.append(row)
        print(f"{invoice_row['invoice_id']}: {row['flag'] or 'ok'} (confidence={row['confidence']})")

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
