# Prototype

Status: not started (Breakpoint B, via Build Engine — PRD → architecture → parallel-agent build).

Must handle one awkward input, not the clean case (non-compliant format / duplicate supplier / missing field), and show the exception path — that matters more than the happy path given who holds the veto. Low fidelity is fine, ugly is fine, working is not optional. See `OUTLINE.md`, "Step: prototype data" and "Step: evals."

**Include a batch view, but keep the record at the unit level.** The demo should show a batch/list UI (multiple transactions reviewable together, e.g. bulk-approve the high-confidence ones) — it's a real, expected part of the workflow. But every record underneath stays per-transaction: its own evidence, confidence, and time-to-expiration. Don't aggregate the underlying data to make the UI simpler; if the demo needs to prove one thing structurally, it's that batch is presentation, not data model. See `answers/03-information-model.md`, "Batch is a UI/UX layer, never the unit of record."
