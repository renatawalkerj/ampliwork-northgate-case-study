# Prototype v1 — sheet, not UI

Deliberately "ugly but works": data ingestion + LLM + a CSV she opens in Excel/Sheets. No web UI. She still makes the actual SAP entry herself — this tool recommends, it never writes (FR7). Build the UI in `../` (see the wireframe artifact) only if time remains after this works end to end.

## Real constraint, found by hitting it: Gemini free-tier daily quota

The free tier caps at **20 requests/day per model**. It blocked full verification twice in one build session. Rather than burn more of it testing, the two new scenarios (INV-1006, INV-1007) were verified by extracting the exact generated prompt and running it blind through a separate, zero-context agent — confirms the prompt/reasoning design is sound, but **does not replace a real Gemini run**. `determine.py` no longer crashes on quota failure (it did, before this was found and fixed) — it writes every row it successfully computed and marks the rest `RETRY_NEEDED`.

**Before presenting: get a billing-enabled key (or wait for the daily reset) and run `determine.py` once, for real, end to end.** The blind test is strong evidence, not a substitute for that.

## Setup

```
pip3 install -r requirements.txt
export GEMINI_API_KEY=your-key-here
```

## How it works

`determine.py` runs one pass over `../input/`, end to end:

1. **Consolidate.** `load_and_consolidate_sap_exports()` reads the 3 separate SAP-instance CSVs (`sap_eu_1_export.csv`, `sap_eu_2_export.csv`, `sap_eu_3_export.csv`) as if they came from 3 systems that have never talked to each other — because in the real Northgate setup, they haven't.
2. **Resolve entities.** `resolve_entities()` clusters vendor records across those exports by name similarity and VAT-ID closeness, not exact match — this is what catches the same supplier registered slightly differently in two SAP instances (the Vantpoint/INV-1002 case). This step is plain Python, never an LLM call.
3. **Deterministic gates, before any model call.** For each transaction: `check_entity_conflict()` flags a supplier whose resolved cluster has conflicting tax profiles; `check_compliance()` flags an invoice missing a jurisdiction-mandatory field. Either failure short-circuits straight to a row — no LLM call happens, because there's nothing sound for it to reason about yet (a conflict needs a human to pick the correct vendor record; a compliance gap needs a corrected invoice). Both can fire on the same transaction, and the row reports both, not just the first one hit.
4. **Retrieve.** For everything that clears the gates, `retrieve_kb_context()` pulls only `approved` knowledge-base entries for that transaction's jurisdiction (`../input/emea_vat_exceptions.csv`) — a `pending_review` entry, like one just created by an analyst override, is retrievable but has no effect until someone with review authority approves it.
5. **Assemble the prompt.** `build_prompt()` combines the structured record, the jurisdiction's VAT rules, the retrieved KB entries, and — where a matching file exists in `../input/documents/` — the actual unstructured text of the invoice, contract, or email `load_document_text()` finds for that reference. The prompt asks the model to return `kb_entries_applied` (what it actually relied on, with justification) separately from `kb_entries_retrieved` (everything it was shown) — the model has to earn a citation, not just have an entry within reach.
6. **Determine.** `call_llm()` sends that prompt to Gemini and gets back charged-correctly / recoverable / reporting-jurisdiction / confidence / reasoning. Wrapped in try/except: a quota or API failure writes that row as `RETRY_NEEDED` with the real error message, instead of crashing the whole run and losing every row already computed.
7. **Sort and write.** All rows — gated and modeled — are sorted by `time_to_expiration_days` first, confidence second, and written to `../output/determination_sheet.csv`. Most urgent surfaces first regardless of how confident the model was, on purpose (FR4/FR5): urgency and certainty are different axes, and burying an urgent-but-uncertain case under confident ones is exactly the kind of thing this tool exists to prevent.

**Can't run it right now (quota, no key yet)?** `../output/example_determination_sheet.csv` is a worked example showing exactly this output shape for all 8 scenarios — 2 rows (INV-1001, INV-1004) are real, confirmed Gemini output from a live run this build session, per `claims.md`; 3 (INV-1005, INV-1006, INV-1007) are blind-test-verified per the quota note above, not yet reconfirmed on a live call; 3 (INV-1002, INV-1003, INV-1008) are fully deterministic (entity conflict / compliance check, no LLM call involved) so they needed neither.

## The 3-minute demo sequence

This is the actual live-demo script — it tells the trust-building story, not just the determination.

**1. Run the baseline.**
```
python3 determine.py
```
Open `../output/determination_sheet.csv`. Point at these rows specifically:
- **INV-1004** (Italy) sorts first — most urgent, not most uncertain. Proves urgency-weighting (FR4/FR5).
- **INV-1002** (Vantpoint) shows `ENTITY_CONFLICT`, flagged without ever calling the LLM — the entity-conflict check is deterministic (FR2a).
- **INV-1008** (a second Vantpoint invoice, also missing `gross_total`) shows `ENTITY_CONFLICT + COMPLIANCE_FAIL` together — proves both deterministic checks report independently when a transaction trips both, instead of one silently hiding the other.
- **INV-1006** (Reinraum Technik, the cleanroom case) — the flagship "connects the dots across structured + unstructured evidence" story: SAP defaults to non-recoverable on a vague description, the model overrides using the invoice text, contract, and `KB-DE-004`. Blind-tested, not yet confirmed on a live Gemini call — verify before presenting.
- **INV-1005** (Ostrava) resolves confidently now that its contract is attached and read, confirming no intra-group relationship — shows the value of document ingestion on its own, separate from the feedback loop below.
- **INV-1007** (Nordkant Client Events) is the case that now carries "the agent is not sure" — client-appreciation-event costs, genuinely ambiguous (blocked entertainment spend vs. legitimate marketing), contract deliberately left unattached. Blind-tested, not yet confirmed live.

**2. Show the override — on INV-1007, not INV-1005.** (INV-1005 no longer needs one; its own contract already resolved it. The still-ambiguous case is INV-1007.)
```
python3 apply_feedback.py override --invoice INV-1007 --jurisdiction NL \
  --rule "Client-appreciation and relationship-building event costs booked to marketing cost centers (6100-series) are recoverable as ordinary marketing spend, not blocked entertainment, provided the event's business purpose is documented in the underlying contract."
python3 apply_feedback.py list
```
Point out: the new entry exists now, status `pending_review` — it does **not** influence anything yet (FR12a). This is the audit trail the Head of Tax Risk would want: her judgment call is captured, not lost, but not auto-trusted either.

**3. Show the approval and the payoff.**
```
python3 apply_feedback.py approve --id KB-NL-002 --reviewer "hub tax manager"
python3 determine.py
```
Open the sheet again. This is the moment: INV-1007 itself now retrieves the newly-approved entry via RAG and resolves at higher confidence — "gets smarter over time," demonstrated, not asserted. (The entry's exact auto-generated id may differ — `apply_feedback.py list` shows the real id before you approve it.)

## Why a sheet, not a UI, for v1

She already lives in spreadsheets — the shadow tracker, the multi-system consolidation, all of it (see the day-in-the-life artifact). A CSV she opens directly isn't a compromise; it's the format that costs zero learning curve. The wireframe in `../` shows what a real review queue would look like eventually — build it only after this pipeline is solid, since the LLM + feedback loop is the actual thing being pitched, not the UI chrome around it.
