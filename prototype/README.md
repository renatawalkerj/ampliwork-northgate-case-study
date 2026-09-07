# Prototype

Status: data + eval plan built (this pass); code build not started (Breakpoint B, via Build Engine — PRD → architecture → parallel-agent build).

Must handle one awkward input, not the clean case (non-compliant format / duplicate supplier / missing field), and show the exception path — that matters more than the happy path given who holds the veto. Low fidelity is fine, ugly is fine, working is not optional. See `OUTLINE.md`, "Step: prototype data" and "Step: evals."

**Include a batch view, but keep the record at the unit level.** The demo should show a batch/list UI (multiple transactions reviewable together, e.g. bulk-approve the high-confidence ones) — it's a real, expected part of the workflow. But every record underneath stays per-transaction: its own evidence, confidence, and time-to-expiration. Don't aggregate the underlying data to make the UI simpler; if the demo needs to prove one thing structurally, it's that batch is presentation, not data model. See `answers/03-information-model.md`, "Batch is a UI/UX layer, never the unit of record."

**Model: Gemini free tier (public API), for build practicality — not a production recommendation.** Free, fast to build against, capable enough for the demo's synthetic invoices. Legitimate here specifically because the demo uses synthetic data we built ourselves, not real Northgate data — the "nothing leaves our tenant" constraint governs the production recommendation (`answers/02-workflow-proposal.md`: Azure OpenAI Service, confirmed, provisioned in Northgate's own subscription), not this exercise. Keep these two answers explicitly separate if asked — see `answers/08-how-we-built-this.md`.

## Build breakdown — sheet first, UI only if time remains

**Revised priority, per explicit direction: demo the LLM + the feedback loop first, ugly is fine, UI last.** The v1 build is a script, not a web app — data ingestion, deterministic checks, an LLM call for the actual tax-judgment reasoning, and a flat CSV she opens in Excel. She still keys the result into SAP herself either way (FR7) — a sheet and a polished review queue hand her the same information, so build the cheap one first. See `src/README.md` for the actual runnable code and the 3-minute demo script.

**Must build — v1, the sheet:**
1. **Data ingestion + deterministic pre-checks (FR2a, FR6, DR2)** — entity-conflict detection and compliance-field checking are structured comparisons against the JSON data, not LLM calls. `src/determine.py`.
2. **LLM determination + RAG retrieval of the knowledge base (FR1, FR1b, FR2, FR12)** — for transactions that pass the deterministic checks, retrieve the jurisdiction's *approved* knowledge-base entries and inject them as context before asking the model for the three-part determination and confidence. `pending_review` entries are filtered out before they ever reach a prompt (FR12a) — this is the enforcement point for that requirement, not just a policy statement.
3. **Time-to-expiration + urgency sort (FR4, FR5)** — deterministic date math, sorts the output sheet so INV-1004 (Italy) surfaces first despite INV-1001 having equal-or-higher confidence.
4. **The feedback loop, demoed as two CLI commands (FR13, FR13a)** — `src/apply_feedback.py override` captures an analyst's override as a `pending_review` candidate entry; `approve` flips it live; re-running `determine.py` shows the next similar transaction resolving at higher confidence. This is the actual trust-building mechanism, demonstrated end to end, not asserted.
5. **Structured-vs-unstructured document ingestion (FR1a) — INV-1006, the flagship "connects the dots" case (Reinraum Technik GmbH, cleanroom R&D tooling).** SAP alone shows a vague line description and a default non-recoverable tax code. The model reads the actual invoice text (German), the contract (confirming the R&D cost center), and a knowledge-base rule (KB-DE-004) to override to recoverable — the real version of "the LLM bridges what SAP and the tax engine can't see." Not yet confirmed on a full live run (built the same pass the Gemini free-tier quota was exhausted) — confirm before presenting.

**Should build if time allows:**
5. **The review-queue UI** (the wireframe artifact) — once the sheet pipeline works end to end. The sheet already carries every column the UI would show (confidence, urgency, flags, reasoning, KB entries used); the UI is a presentation layer on the same data, not a different capability.
6. **Minimal burndown/diagnostic reporting (FR10, FR11)** — answers the VP's and EMEA manager's asks directly; secondary to the exception-handling story either way.

**Cut, mocked only:** no OCR/scanned documents (data is structured JSON from the start, per `research/open-data-search.md`); "3 SAP instances" is a label on 3 JSON records, not 3 real databases; no real cloud call for anything beyond the LLM determination step itself.

## Architecture: LLM layer vs. UI/app layer — a real code boundary, not just a concept

Even though the prototype runs on synthetic data via Gemini's public API (the tenant constraint doesn't apply to it), the code should still be structured with a clean separation between these two pieces, so the demo's architecture story matches what production would actually look like:

- **Determination service** — the module that calls the LLM. Decomposed per capability (extraction, entity-resolution check, compliance check, tax determination), not one monolithic prompt — matches how `evals/eval-plan.md` already scores these as independent metrics, and is the pattern that would carry over to a real RAG-style retrieval of knowledge-base entries in production (fetch the relevant KB entries for a transaction's jurisdiction/entity, inject as context, rather than baking everything into a static system prompt).
- **Review UI** — everything else: the queue, evidence display, confirm/override actions, knowledge-base review screens, reporting. No LLM in the loop for most of this — it's conventional CRUD against the data files, with the determination service invoked only at specific trigger points (a transaction needs a determination). Keep this as a separate module even though both run in the same demo process — don't let LLM calls leak into UI-rendering code.

In production, this separation stops being a code-organization nicety and becomes a deployment boundary: the determination service must be a private-endpoint-only resource inside Northgate's own Azure subscription (the piece all the tenant-isolation discussion is about), while the review UI — which also touches real transaction data, not just the LLM piece — must *also* run inside that subscription (NFR1 says "all data processed," not "the model call specifically"). Both pieces live in-tenant; only the *reasoning* piece needs the private-endpoint-to-a-model-resource pattern specifically.

## Input (`input/`)

- `sap_eu_*_export.csv` — the 3 structured SAP exports (vendor + invoice + PO/GR/GL-cost-center detail + native tax codes).
- `emea_vat_exceptions.csv` — the knowledge base, including `KB-DE-004` (the cleanroom-R&D rule for INV-1006).
- `documents/` — the unstructured half: actual invoice PDF text (multilingual), contract excerpts, and customs paperwork, actually read by `determine.py`'s `load_document_text`, not just referenced. Includes the full documentation for the new flagship case (INV-1006, Reinraum Technik GmbH) and the contract that resolves INV-1005 (Ostrava). See `answers/03-information-model.md` §4 for the structured-vs-unstructured map and what's still not built (invoice field-presence extraction for FR6).

## Source (`src/`)

`determine.py` (the pipeline: deterministic checks → RAG retrieval → LLM → CSV) and `apply_feedback.py` (the two-command feedback-loop demo: `override`, `approve`, `list`). See `src/README.md` for setup and the exact 3-minute demo sequence.

## Data files (`data/`)

- `jurisdictions.json` — 4 EMEA jurisdictions (NL, DE, FR, IT), reclaim-window rule type/value, invoice-compliance mechanism and mandatory fields. VAT rates anchored to real, current values (vatnode/eu-vat-rates-data, MIT licensed).
- `vendor_master_records.json` — mock 3-SAP-instance vendor extract, including the Vantpoint duplicate-vendor conflict and an `entity_resolution_map` (what FR2a requires the system to compute, precomputed here as the demo's input).
- `invoices.json` — the 5 synthetic transactions, each with an `expected` ground-truth block used by the eval harness (see `evals/`).
- `knowledge_base.json` — the regional-spreadsheets data source, formalized: 2 approved seed entries + 1 `pending_review` candidate entry generated from INV-1005's resolution, each with full provenance (source, author, date, review status).

## Eval framework (`evals/`)

See `evals/eval-plan.md` for the full methodology (what "correct" means per output type, the metrics tracked, and the eval-and-refine iteration loop) and `evals/scorecard-template.json` for the run-scoring structure. **Precision point:** this is prompt/threshold iteration against a labeled eval set, not weight-level fine-tuning — the prototype has no fine-tuning budget (Gemini free tier), consistent with the same constraint already named for the production recommendation.
