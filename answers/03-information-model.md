# Information model (Part 1.3)

Status: drafted. See `OUTLINE.md`, "Step: information model." Draws on `case-facts.md` §5 (evidence document → entity mapping table) and §4 (per-hub jurisdiction research).

## The eight entities, defined directly against the brief's own list, and how they relate

**Legal entity** — the Northgate operating company that books a given transaction and files the return in its own name (e.g., "Northgate Industries GmbH" in Germany). Distinct from both jurisdiction (the rules boundary a legal entity operates within) and hub (a staffing construct with no rules meaning at all).

**Jurisdiction** — the actual rules boundary. Its own reclaim-window rule (type and value), invoice-content requirements, filing frequency, and standard VAT/GST rate. First-class entity, parameterized per country, looked up per transaction by that transaction's actual jurisdiction — see the design decision immediately below for why this can't be hub-level.

**Supplier** — the real-world business Northgate buys from. Distinct from **vendor master record**, the per-SAP-instance object representing that supplier — because of the 3 acquisitions, one real supplier can exist as multiple, disconnected vendor master records with different tax profiles (the Vantpoint case, FR2a/DR2). Entity resolution is what reconciles "supplier" back to one identity across records that don't know about each other.

**Transaction** — the atomic unit of record: one supplier (resolved identity), one invoice, one legal entity, one point in time. This is the level at which the three decisions and time-to-expiration are computed. Batch is a UI/UX convenience for review, never an aggregation at the data layer (DR3) — see "Batch is a UI/UX layer" below for why that has to hold.

**Invoice** — the supplier-issued document describing a transaction. Carries the surface facts (amount, VAT rate/amount charged, line description) but is not always sufficient alone to answer 2 of the 3 required questions (recoverability and correct reporting jurisdiction often depend on the contract, customs paperwork, or goods receipt — case-facts.md §7), and isn't automatically compliant with its jurisdiction's mandatory-field rules (FR6) just because it exists.

**Recoverability determination** — the actual output object: the three-part judgment (charged correctly / recoverable / where reported) plus a confidence score and reasoning, computed per transaction (FR1/FR2). This is what the whole system produces.

**Filing period** — the recurring cadence (monthly or quarterly, jurisdiction-dependent) a legal entity's return is filed within. A transaction's finalized determination gets swept into whichever filing period is current when it's filed.

**Reclaim** — the actual right to recover previously-paid input tax on a transaction, bounded by its jurisdiction's reclaim window (rolling-years, e.g. Netherlands ~5yr, or return-deadline-bound, e.g. Italy/India). Once the window closes, an unclaimed reclaim is permanently lost — time-to-expiration (below) tracks how close a *specific transaction's* reclaim right is to that point, not a jurisdiction-wide clock.

**How they relate, as one flow:** a legal entity buys from a supplier (resolved past duplicate vendor records) → a transaction, documented by an invoice → evaluated against its jurisdiction's rules → a recoverability determination → filed in the legal entity's next applicable filing period → if recoverable and unclaimed, an active reclaim, ticking down to that jurisdiction's window.

**What's left out of v1, specific to this data model (beyond the already-named EX1-EX3 scope exclusions):**
- Legal entity isn't yet modeled as fully independent from jurisdiction — v1 assumes something close to 1:1 (one legal entity per jurisdiction Northgate operates a transaction in), which won't hold if Northgate runs multiple legal entities within the same country.
- Credit notes are a named evidence type (per the brief's own list) but aren't yet modeled as linked adjustments to a specific prior transaction — they exist as a category, not a relationship.
- Filing period isn't tracked as its own record with its own state (open/filed/closed) — it's currently just a frequency attribute on jurisdiction, not something a transaction is explicitly assigned to.

## Key design decision: jurisdiction, not hub, is the rules boundary
The 3 regional hubs (Chicago/Rotterdam/Singapore) are a staffing and org construct — the brief never says they're a rules boundary, and they aren't one: EMEA alone spans France (~2yr reclaim window) and Netherlands (~5yr), and APAC likely spans similarly divergent regimes (see `case-facts.md` §4 for the per-hub minimum research). **Jurisdiction must be its own first-class entity, parameterized per country** (reclaim window, invoice-field requirements, filing frequency), looked up per transaction by that transaction's actual jurisdiction — not by which hub happens to staff the work. Hub stays a real, separate entity for routing/staffing, but must not be conflated with the rules boundary.

**Concrete "what breaks if you get this wrong":** if reclaim window were modeled per-hub instead of per-jurisdiction, the system would treat a Netherlands transaction (5yr window) as expired at whatever the coarser EMEA minimum turned out to be — actively abandoning money that was still legally recoverable. Flattening 30 countries to 3 hub-buckets repeats the exact mistake the brief warns against, just one level coarser than flattening to a single global constant.

**A second, sharper failure mode research surfaced:** reclaim window isn't even a flat N-years-from-invoice-date everywhere. Italy and India both bind the deadline to an *annual return filing date*, not a rolling count from the invoice — so the actual runway depends on when in the fiscal year the invoice lands (Italy: ~4-5 months for a December invoice vs. ~15-16 months for a January one; India similarly ~8 to ~20 months depending on FY timing). A model that stores "reclaim window = N years" per jurisdiction, even correctly per-jurisdiction, still gets Italy and India wrong — it needs the jurisdiction's *rule type* (rolling N-years vs. return-deadline-bound) as an attribute, not just a number. See `case-facts.md` §4.

**A derived attribute this all points to: time-to-expiration.** Every recoverability determination that's identified-but-not-yet-claimed should carry a computed "time remaining before this specific transaction's window closes" — not just the jurisdiction's rule, but that rule applied to this transaction's actual invoice date. This is the same idea as an AR-aging schedule (0-30/31-60/61-90 days), applied to unclaimed recoverable tax instead of unpaid invoices. Without it, a small amount three weeks from expiring and a large amount with years of runway look identical on a list — and the urgent one is the one that actually gets lost. This attribute is also what makes the workflow's exception queue urgency-aware, not just confidence-aware (see `answers/02-workflow-proposal.md`).

## Invoice compliance status is jurisdiction-parameterized too, and not always a flat checklist
Same jurisdiction-not-hub principle, applied to the compliance-check capability (`answers/02-workflow-proposal.md`, point 7): mandatory invoice fields vary by jurisdiction (EU: up to 15 fields under Art. 226; Singapore: 10 fields; India: ~19 particulars), so this has to be a per-jurisdiction rule set, not one global field list. Two sharper wrinkles:
- **Some jurisdictions require an EU-Art.-226-style baseline; two assumed EMEA countries need their own regime entirely.** Switzerland and Turkey aren't EU members and aren't covered by Art. 226 at all. A compliance check built only against the EU baseline would silently treat their invoices as failing checks that don't actually apply to them, or miss checks that do.
- **Compliance isn't always a static field checklist — some jurisdictions require government clearance.** Italy, Poland (from 2026), and Spain (from 2027) require the tax authority's own platform to validate and stamp an invoice before it's legally valid — a correctly-fielded invoice can still fail on pure clearance/schema grounds. India's IRP/IRN model works the same way. The information model needs a jurisdiction attribute for *compliance mechanism type* (field-checklist vs. government-clearance), not just a field list — otherwise it silently assumes every jurisdiction works like the simplest case.

## Batch is a UI/UX layer, never the unit of record
Same principle as jurisdiction-not-hub, applied one level deeper: the atomic unit of the data model is the **individual transaction/determination**, never a batch. Batching exists only in the review UI — grouping similar transactions so a reviewer can bulk-approve efficiently — never in the underlying record. Reasons this has to hold, not just a style preference:
- **Audit trail:** an auditor needs to see one transaction's own evidence and determination, not "processed as part of a $2M batch." Aggregating away transaction identity would recreate the exact audit-exposure risk the Head of Tax Risk owns.
- **Time-to-expiration is inherently per-unit** (above) — each transaction has its own invoice date and therefore its own expiration date. Batching would average away the one thing the urgency-weighted queue depends on.
- **Exception routing is per-unit** — two transactions a reviewer sees grouped in one UI batch can have different confidence scores; one may auto-process while its neighbor needs review. The batch is a convenience for the human, not a shared fate for the data.

## Summary (for the deck)
Legal entity, jurisdiction, supplier, transaction, invoice, recoverability determination, filing period, reclaim — what each means in Northgate's world, and how they relate. What's deliberately left out of v1, and what breaks if the model is wrong.

## Full entity detail (appendix material)
Attribute-level detail per entity, backed by the SAP/tax domain research where available; anything not settled by research gets resolved as an assumed customer clarification, tagged in `claims.md`.

## The source-data map — every field, traced through `prototype/src/determine.py`

Traced from the actual code, not described from memory. Four sources, and a precise line for each field: does it stay deterministic (plain Python, no model involved), or does it reach the LLM prompt. This distinction is the same one already established for entity resolution and compliance checking (`answers/02-workflow-proposal.md`'s architecture section) — most of what looks like "the AI's job" is actually structured-data logic; the LLM is reserved for the genuine judgment call.

### 1. The 3 SAP exports (`input/sap_eu_*_export.csv`) — real-world source: SAP, pulled by the analyst today

| Field | Used for | Reaches the LLM prompt? |
|---|---|---|
| `sap_instance` | Provenance display, entity-resolution clustering context | No |
| `vendor_record_id` | Entity-resolution clustering key | No |
| `supplier_name_as_recorded` | Entity-resolution name-similarity matching | **Yes** — "Supplier: ..." |
| `vat_id` | Entity-resolution VAT-similarity matching (catches the Vantpoint stale-digit case) | No — resolved before the call; the LLM only ever sees a supplier with no conflict |
| `tax_classification` | Entity-conflict check (do resolved records disagree); the treatment itself | **Yes** — "Tax classification on file: ..." |
| `invoice_id`, `invoice_number`, `invoice_date` | Row identity, time-to-expiration input | `invoice_number`/`invoice_date`: **Yes**. `invoice_id`: No |
| `jurisdiction` | Looks up the jurisdiction rule | **Yes** (as the jurisdiction name/code) |
| `net_amount` | — | **Yes** |
| `vat_rate_charged` | — | **Yes** |
| `vat_amount_charged` | — | **Yes** — "VAT amount actually charged: ..." with an explicit instruction to cross-check it against `net_amount × vat_rate_charged`. *(Found missing during this trace, fixed and confirmed on a live re-run, same session.)* |
| `fields_present` | Deterministic compliance check (`check_compliance`) | No |
| `purchase_order`, `goods_receipt`, `contract` | — | **Yes, but only as an ID/reference string** — "PO-DE-88213," not the document's actual content. See the evidence-ingestion gap below. |
| `notes` | — | **Yes** — free-text context |

### 2. The knowledge base (`input/emea_vat_exceptions.csv`) — real-world source: the analyst's own shadow spreadsheet, formalized (FR12)

| Field | Used for | Reaches the LLM prompt? |
|---|---|---|
| `id`, `rule` | The actual exception content | **Yes — but only for entries that are both `status == approved` AND jurisdiction-matched** (`retrieve_kb_context`). This is FR12a's enforcement point, not a policy statement. |
| `status`, `added_by`, `date`, `reviewed_by`, `review_date`, `origin_transaction` | Governance/provenance, `apply_feedback.py`'s override/approve workflow | No — the model never sees who added a rule or when, only the rule itself, and only once approved |

### 3. Jurisdiction reference config (`input/jurisdictions.json`) — real-world source: tax-engine config or the tax team's own research; not something an individual analyst maintains

| Field | Used for | Reaches the LLM prompt? |
|---|---|---|
| `vat_standard_rate` | — | **Yes** |
| `reclaim_window` (rule type, value) | Time-to-expiration calculation (`time_to_expiration_days`) | **No — fully deterministic.** The LLM never reasons about reclaim windows at all; urgency-sorting (FR4/FR5) happens entirely outside the model. |
| `invoice_compliance.mandatory_fields` | Compliance check (`check_compliance`) | **No — fully deterministic.** |

### 4. Document content — the gap, then actually closed (revision history kept, since it's honest build history)

**Status: resolved.** An earlier pass through this section (kept below for the actual build history, not deleted) found and then over-narrowed a real gap: no document content was ingested anywhere, including the invoice's own — everything was hand-authored structured data standing in for extraction that hadn't been built. That's now fixed for the unstructured-document half of the problem (not the invoice-field-presence half — see the honest remaining limit below).

**The hard line the pipeline now draws, per the explicit design direction it was built to:**

| | Structured system records (SAP + tax engine) | Unstructured document context (PDFs, mailbox, spreadsheets) |
|---|---|---|
| **What lives here** | AP voucher line (vendor, invoice number, amounts, native tax code e.g. `I0`/`I1`), PO details (price, quantity, GL/cost-center code), goods receipt (received y/n), vendor master data | Invoice PDF text (multilingual — e.g. INV-1006's German line item), contracts, customs paperwork, supplier dispute emails, the knowledge-base spreadsheet |
| **Why it's not enough alone** | Flat and rigid — a vendor, an amount, a cost-center number, a default tax code. Cannot tell you *why* a purchase was made or whether a vague code was applied correctly | Invisible to SAP and the tax engine entirely — this is where the actual judgment evidence lives |
| **How the pipeline uses it** | Loaded directly from the 3 SAP export CSVs (`sap_eu_*_export.csv`) — no ingestion step needed, already structured | `load_document_text()` in `determine.py` reads the actual file content from `input/documents/` when a PO/contract/customs reference resolves to one — real ingestion, not a reference string, for the first time this session |

**What this actually demonstrates, concretely:** INV-1006 (new flagship case, added this pass) — SAP shows only a vague line description and a default `I0` (non-recoverable) tax code against cost center `CC-4520-RND`. The model reads the actual German invoice text (`Spezialwerkzeuge für Reinraum` — cleanroom tooling), the contract confirming that cost center is the R&D facility fit-out, and the knowledge-base rule (`KB-DE-004`) specifically covering 4520-series cost centers — and overrides the SAP default to recoverable, citing the specific facts that justify it. This is the exact "LLM connects the dots across fragmented sources" chain, built and running, not just described.

**Confirmed live, same session:** INV-1005 (Ostrava) now resolves cleanly once its contract is actually attached and read (`CTR-OSTRAVA-2025_contract.txt`, confirming no intra-group relationship) — previously stuck at "indeterminate without contract." INV-1001 correctly retrieved *two* approved knowledge-base entries and rejected both, citing the specific cost-center mismatch — real evidence the relevance-justification fix (from the earlier RAG finding) holds up with more retrieved context in play, not just the original single-entry case.

**The honest remaining limit, precisely scoped now, not overstated:** the invoice's *own* field-presence determination (feeding `check_compliance`/FR6 — is Germany's *Leistungsdatum* actually on this invoice) is still hand-authored (`fields_present` in the CSV), not extracted from the invoice text the pipeline now reads for other purposes. That's a smaller, well-defined remaining gap — extending `load_document_text()`'s already-built pattern to also drive the compliance check, not a new capability to design from scratch. State it exactly this way if asked, not as if nothing was fixed.

**Real constraint surfaced building this, worth having ready:** the Gemini free tier caps at 20 requests/day per model. A live run partway through this build hit that cap mid-batch — `determine.py` previously crashed with no output at all when that happened; it now writes every row it successfully computed and marks the rest `RETRY_NEEDED` with the real error preserved, rather than losing everything. Get a billing-enabled key before presenting live, or budget rehearsal runs deliberately (`prototype/src/README.md`).

## Claims for claims.md

| Claim | Status | Source | Notes |
|---|---|---|---|
| `vat_amount_charged` is never passed to the LLM prompt, so the model cannot cross-check it against `net_amount × vat_rate_charged` for internal consistency | VERIFIED (traced directly from `prototype/src/determine.py`'s `build_prompt`) | Code inspection | A real, fixable gap — not a design choice. Should be added to the prompt before presenting the pipeline as finished |
| Reclaim-window rules and compliance mandatory-field lists are never passed to the LLM — both are fully deterministic, computed in plain Python before/instead of any model call | VERIFIED (traced directly from `determine.py`) | Code inspection | Reinforces the "most of this isn't actually the AI's job" architecture point already established |
| The prototype does not ingest evidence-document content (PO/goods receipt/contract/customs paperwork/credit note) — only ID/reference strings reach the prompt | VERIFIED (traced directly from `determine.py` and the input CSVs) | Code inspection | Real scoping gap for FR1a, not yet designed in detail — state plainly if asked, don't imply this is solved |
