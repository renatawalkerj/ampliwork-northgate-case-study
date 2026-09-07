# Eval framework (Part 1.4 support — "evals first-class, not an afterthought")

Status: methodology + scorecard defined; not yet run against a built system (no build exists yet — this is the plan the build will be tested against). See `OUTLINE.md`, "Step: evals," and the Decision "Phase 1 runs as iterative eval-and-refine cycles" (digest §5).

## Precision point, stated up front

**This is not fine-tuning in the ML-weights sense.** The prototype runs on Gemini's free-tier public API — no fine-tuning budget exists for the prototype or (per `claims.md`) for the production recommendation either (it's one of the named reasons self-hosting was declined). What actually improves, iteration to iteration, is **the prompt/instructions and the confidence threshold, scored against a growing labeled eval set** — not the model's weights. Say it this way if asked "are you fine-tuning the model": no — we're doing prompt and threshold iteration against measured results, which is what NFR5 ("confidence threshold tightens over time as accuracy improves") and the eval-and-refine Decision actually describe. Calling this "fine-tuning" in the pitch would overclaim a capability this build doesn't have.

**Two distinct "gets better over time" mechanisms — don't conflate them if asked.** (1) **Engineering-side:** the prompt/threshold iteration described above, done by the build team against the eval set. (2) **Domain-content-side:** the knowledge-base feedback loop (FR12/FR13, `data/knowledge_base.json`) — an analyst's override becomes a candidate, reviewed exception rule, growing the system's actual tax-domain knowledge over time, independent of any prompt change. The first makes the *engine* better at reasoning; the second makes the *knowledge it reasons over* more complete. Both are real, and they're not the same claim.

## 1. What "correct" means, per output type

Defined *before* building, per `OUTLINE.md`'s instruction — each of the 5 synthetic invoices in `prototype/data/invoices.json` carries an `expected` block with ground truth for:

| Output | Ground truth field | What it tests |
|---|---|---|
| Charged correctly | `expected.charged_correctly` | Core tax-judgment accuracy |
| Recoverable | `expected.recoverable` | Core tax-judgment accuracy |
| Reporting jurisdiction | `expected.reporting_jurisdiction` | Correct jurisdiction routing |
| Confidence tier | `expected.confidence_tier` (high/low) | Whether the system's own confidence score would route the case correctly |
| Entity conflict flagged | `expected.entity_conflict_flagged` | FR2a — does it catch a duplicate-vendor tax-profile conflict, or silently trust whichever record it's coded against |
| Compliance pass | `expected.compliance_pass` | FR6 — does the format-compliance check fire independently of the tax-judgment call |
| Time-to-expiration | `expected.time_to_expiration_days_approx` | FR4 — is the jurisdiction-specific rule (rolling vs. return-deadline-bound) applied correctly |

Three of the five cases (INV-1002, INV-1003, INV-1005) have deliberately unresolvable "charged_correctly"/"recoverable" values (`indeterminate_pending_correction`, `cannot_determine_pending_compliance_fix`, `indeterminate_without_contract`) — **correct behavior for these is recognizing indeterminacy and routing, not guessing a confident wrong answer.** A scoring approach that only checks "did it match a definite answer" would miss the actual point of these three cases; the scorer must treat "correctly routed as indeterminate, at low confidence" as a pass.

## 2. Metrics computed from the 5-case eval set

Small by design — 5 cases is enough to test each named capability once, not a statistical sample. It scales up in real Phase 1 work against a sampled slice of Northgate's actual backlog (see `answers/02-workflow-proposal.md`'s point on establishing the human-only baseline empirically), which is where precision/recall become statistically meaningful (row 33 / FR11).

- **Determination accuracy** — per-question match rate (charged correctly / recoverable / reporting jurisdiction) against `expected`, with indeterminate-recognition counted as a match where `expected` says indeterminate.
- **Confidence-tier accuracy** — did the system's own confidence score land the case in the tier `expected.confidence_tier` says it should (i.e., would it actually get routed the right way).
- **Precision on the auto-processed subset** — of cases the system would auto-process (high confidence), what fraction are actually correct. On this 5-case set, only INV-1001 and INV-1004 should land here — a single false auto-process anywhere is a hard fail worth stopping to fix before adding more cases.
- **Recall on routing** — of cases that should route (INV-1002, INV-1003, INV-1005), what fraction actually got routed rather than silently auto-processed. This is the number the Head of Tax Risk's stated fear ("wrong matters more than slow") is actually about — recall failures here are confidently-wrong auto-filings, the exact $4M-penalty failure mode.
- **Entity-conflict detection rate** — binary, INV-1002 specific, but treated as its own tracked metric because it's the flagship case tied to the EMEA manager's complaint.
- **Compliance-check accuracy** — binary, INV-1003 specific, and must fire independently of the tax-judgment call (a system that only ever fails compliance and recoverability together isn't actually running two distinct checks per FR6).
- **Time-to-expiration correctness** — exact numeric check against `expected.time_to_expiration_days_approx` (small tolerance for date-math rounding), split by rule type (rolling vs. return-deadline-bound) since that's the one most likely to silently break if a future jurisdiction is added carelessly.
- **Knowledge-base governance correctness (FR12a)** — binary check that no `pending_review` entry (e.g., `KB-FR-003`) ever influences an auto-processed (high-confidence) determination. This is a harder failure to notice than a wrong tax call, since it wouldn't show up as an obviously wrong answer — it would show up as *unearned* confidence on a case that should still require review. Treat any violation as a hard fail, not a score deduction.

## 3. The eval-and-refine loop

1. Run the full 5-case set through the current prompt/threshold configuration.
2. Score against the metrics above; log every miss with the specific case and specific field that failed.
3. Diagnose *why* — a wrong answer and a wrong routing decision have different fixes (the first needs better reasoning/evidence use, the second needs threshold or confidence-calibration adjustment, not necessarily better reasoning).
4. Change exactly one thing (a prompt instruction, or the confidence threshold) per iteration — not both at once, so it's clear which change caused which effect.
5. Re-run the full set (not just the case that failed) — a fix for one case regressing another is exactly the kind of thing a partial re-run would hide.
6. Log the iteration (see example below) — this log is itself a deliverable: presented to Northgate as the trust mechanism the Head of Tax Risk wants, not internal QA (`OUTLINE.md`).

### Worked example (from the actual first live run against `determine.py`, Sept 6 2026)

**Superseded design note:** an earlier draft of this section speculated that catching INV-1002's duplicate-vendor conflict would require an explicit prompt instruction telling the LLM to check for contradicting vendor records. That question never actually arose, because the build (correctly, on reflection) made entity-conflict detection a deterministic code check against the structured data (`determine.py`'s `check_entity_conflict`), not an LLM judgment call — the LLM is never even invoked for INV-1002. That's the more defensible design (cheap, fast, 100% reliable for a comparison a computer does perfectly), but it means the speculative "surprise" below never happened. Replaced with what actually did.

| Iteration | Change | Result | Miss? |
|---|---|---|---|
| 1 (baseline run) | Retrieve all `approved` knowledge-base entries for the transaction's jurisdiction, inject as context, ask the LLM to determine treatment | INV-1001 (a plain, non-intra-group Meridian purchase) came back citing `KB-DE-002` (an intra-group cost-sharing exception) in `kb_entries_used`, with no explanation in the reasoning text for why an intra-group rule applied to a transaction that isn't intra-group | **Fail** — the model treats "available in context" as license to cite, not as something it must justify |
| 2 (actually run) | Added an explicit instruction: only list a knowledge-base entry in a new `kb_entries_applied` field if the reasoning states which specific fact of *this* transaction triggers it; separately track `kb_entries_retrieved` (what was available) vs. `kb_entries_used` (what the model actually claimed applies), so the two are never conflated again | INV-1001 now returns `kb_entries_used: (none applied)`, `kb_entries_retrieved: KB-DE-002` — and the reasoning explicitly states *why* it doesn't apply: "KB-DE-002 was not applied because this transaction shows no evidence of being an intra-group cost-sharing invoice." | **Pass** |

**This is the real "one thing that surprised us" (`answers/04-prototype-notes.md`, point 2):** retrieval-augmented context doesn't get filtered for relevance by default — the model will cite whatever's available in the prompt unless explicitly required to justify the citation. That's a real, generalizable finding about building RAG-augmented determination systems, observed on an actual run and then actually fixed on the next one, not a hypothesis about how the model might behave. The fix generalizes beyond this one case: `determine.py` now separately reports what was *retrieved* vs. what was *applied* for every transaction, not just this one — so the same silent-over-citation failure mode would be visible in the sheet itself if it recurred elsewhere.

**A second thing the same run surfaced, worth being honest about:** the first version of INV-1004's synthetic invoice had the French supplier charging Italy's 22% VAT rate directly — a real live run correctly flagged this as wrong (cross-border EU B2B services are reverse-charged, not charged at the buyer-country's rate). That's a bug in the test fixture I built, not a finding about the model — fixed in `data/invoices.json` (see its `vat_rate_charged_note`), not used as a talking point, since presenting "the model caught my own data-construction error" as a product insight invites exactly the pushback that it's actually a data-quality issue, not a model-behavior one.

## 4. What this is for in the pitch

Presented in the deck as the answer to "how do we know this will actually work, and how do we know it'll keep getting better" — not as an appendix. The eval set and the iteration log are the concrete, checkable version of "confidence threshold tightens over time as accuracy improves" (NFR5) and "Phase 1 runs as iterative eval-and-refine cycles" (digest §5 Decision) — this is what that decision looks like as an artifact, not just a sentence in a slide.
