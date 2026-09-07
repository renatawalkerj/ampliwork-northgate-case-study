# Prototype v1 — sheet, not UI

Deliberately "ugly but works": data ingestion + LLM + a CSV she opens in Excel/Sheets. No web UI. She still makes the actual SAP entry herself — this tool recommends, it never writes (FR7). Build the UI in `../` (see the wireframe artifact) only if time remains after this works end to end.

## Setup

```
pip install -r requirements.txt
export GEMINI_API_KEY=your-key-here
```

## The 3-minute demo sequence

This is the actual live-demo script — it tells the trust-building story, not just the determination.

**1. Run the baseline.**
```
python3 determine.py
```
Open `../output/determination_sheet.csv`. Point at three rows specifically:
- **INV-1004** (Italy) sorts first — most urgent, not most uncertain. Proves urgency-weighting (FR4/FR5).
- **INV-1002** (Vantpoint) shows `ENTITY_CONFLICT`, flagged without ever calling the LLM — the entity-conflict check is deterministic (FR2a).
- **INV-1005** (Ostrava) comes back `confidence: low`, reasoning names the missing contract — the LLM recognizing insufficient evidence rather than guessing (FR1b).

**2. Show the override.**
```
python3 apply_feedback.py override --invoice INV-1005 --jurisdiction FR \
  --rule "Cross-border services from EU suppliers to Northgate's French entity: absent an explicit intra-group designation in the contract, resolve as a fully recoverable taxable third-party supply."
python3 apply_feedback.py list
```
Point out: `KB-FR-003` exists now, status `pending_review` — it does **not** influence anything yet (FR12a). This is the audit trail the Head of Tax Risk would want: her judgment call is captured, not lost, but not auto-trusted either.

**3. Show the approval and the payoff.**
```
python3 apply_feedback.py approve --id KB-FR-003 --reviewer "hub tax manager"
python3 determine.py
```
Open the sheet again. This is the moment: a *future* transaction shaped like INV-1005 would now retrieve `KB-FR-003` via RAG and resolve at higher confidence automatically — "gets smarter over time," demonstrated, not asserted.

## Why a sheet, not a UI, for v1

She already lives in spreadsheets — the shadow tracker, the multi-system consolidation, all of it (see the day-in-the-life artifact). A CSV she opens directly isn't a compromise; it's the format that costs zero learning curve. The wireframe in `../` shows what a real review queue would look like eventually — build it only after this pipeline is solid, since the LLM + feedback loop is the actual thing being pitched, not the UI chrome around it.
