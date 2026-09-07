# Ampliwork — Northgate Industries Case Study

Senior PM take-home for Ampliwork. Due EOD Thu Sep 10, 2026.

## Start here
- `source/case-study-brief.md` — original brief, never edited
- `case-facts.md` — what the brief says vs. what we're assuming vs. what research filled in — read before anything else
- `requirements.md` — consolidated, testable requirements (FR/NFR/DR/EX), traced to decisions
- `claims.md` — the PIL ledger: every claim tagged VERIFIED or ASSUMED, with sourcing

## Working artifacts
Each lives in this repo (`artifacts/`) as a self-contained HTML file — open directly in a browser — and is also published for sharing/commenting. The local file is a point-in-time snapshot; the published link may run ahead of it if edited directly.
- **The Northgate Ledger** — case facts, research findings, the full requirements list, decisions, and risks in one reference: `artifacts/northgate-ledger.html` / https://claude.ai/code/artifact/65a0635e-777f-4e65-8dba-8ce378322ebd
- **Analyst journey & wireframe** — the current-state vs. AI-enabled day-in-the-life, plus a low-fi wireframe mapped step by step to it: `artifacts/analyst-journey-wireframe.html` / https://claude.ai/code/artifact/015caaee-fe54-4b5f-9217-8ac8cde14e3d
- **Northgate Proposal (the deck)** — the 12-slide pitch: `artifacts/northgate-proposal-deck.html` / https://claude.ai/code/artifact/8505f7ae-f44c-4695-9344-dceb84c14456

## Repo structure
- `OUTLINE.md` — working project plan
- `research/` — domain briefings and market research (Breakpoint A)
- `answers/` — content answering each part of the brief, one file per sub-question
- `artifacts/` — local copies of the 3 published artifacts above
- `prototype/` — the actual build:
  - `src/` — the runnable pipeline (`determine.py`, `apply_feedback.py`) — see `prototype/src/README.md` for setup and the live-demo sequence
  - `input/` — the 3 SAP exports, knowledge base, jurisdiction config, and supporting documents the pipeline reads
  - `output/` — `example_determination_sheet.csv`, a worked example of the pipeline's output
  - `evals/` — what "correct" means, the metrics tracked, and the eval-and-refine methodology
- `extras-rationale.md` — what we added beyond the literal brief, and why
- `checklist.md` — final gate before sending: constraints, evaluation criteria, content integrity

## Running the prototype
```
cd prototype/src
pip install -r requirements.txt
export GEMINI_API_KEY=your-key-here
python3 determine.py
```
See `prototype/src/README.md` for the full demo script (baseline → override → approve → re-run).
