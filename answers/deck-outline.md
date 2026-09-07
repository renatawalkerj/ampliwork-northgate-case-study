# Deck outline — content first, visuals later

Status: drafted. 12 slides total (8 + 4), matching the brief's cap exactly — no slack, so anything added later has to displace something here, not stack on top. Content pulled directly from existing answers/case-facts, not written fresh, so it stays consistent with everything already decided. Per the brief's own evaluation note: "we are evaluating how you think, not how you decorate slides... clarity beats polish" — this pass is about getting the argument right; visual design is a separate, later pass.

---

## PART 1 — THE PITCH (10 minutes, 8 slides max)

### Slide 1 — Six quotes disagree; only three are competing theories (merges title + brief's point 1, answered directly)
- No separate title slide. Opens by naming the actual structure of the disagreement, not just picking a side.
- **Only 3 of 6 discovery-call quotes are competing root-cause theories** — the VP's (coding is the bottleneck), EMEA's (dirty supplier master data), APAC's (non-compliant invoices). The other 3 (Head of Tax Risk, Head of Tax Technology, Enterprise Security) are stakeholder constraints, not diagnoses — weighting them against the three theories would be a category error. Full reasoning: `answers/01-diagnosis.md`.
- **Weighted most — EMEA and APAC:** both independently corroborated by real research (SAP architecture; EU Art. 226 case law), not just stated opinion. EMEA's is grounded further by what her own analyst runs into daily: manually pulling 3 separate SAP exports just to see what tax code was applied (the day-in-the-life journey, full version in the published journey/wireframe artifact).
- **Weighted least — the VP:** her own opinion, no independent corroboration. Resolved directly on the final Part 1 slide.
- One line: "$8-30M/year disputed internally — the width of that range is itself the diagnostic signal."

### Slide 2 — Assumptions (the brief's explicit "one slide")
Compact, load-bearing only — full ledger lives in `claims.md`:
- Hyperscaler: Azure, confirmed as a settled premise for planning, not externally verified.
- 30-country footprint (~7 Americas/14 EMEA/9 APAC) constructed, not stated in the brief.
- Contingency pricing is viable broadly (revised after direct challenge — human-in-the-loop neutralizes the incentive-conflict concern), not narrowly carved out.
- No current error-rate baseline exists — Phase 1 measures it, doesn't assume it.
- Sample data: Northgate shared sample records during discovery — the prototype's synthetic dataset is built from that, not invented from nothing.
- Follow-up access: clarifying questions beyond the discovery-call quotes let us build the analyst's actual day-in-the-life, not just infer it from six lines of transcript.

### Slide 3 — What we propose: one agent, a deterministic pipeline around it, a human at the end (brief's point 2)
- **The agent or agents, answered precisely:** one reasoning model does the actual determination — not several agents stitched together. Everything around it (entity resolution, compliance checking, urgency calculation, knowledge-base retrieval) is deterministic code, not additional AI — cheaper, faster, and no model risk on the parts a computer can already do perfectly. See `answers/02-workflow-proposal.md`'s full pipeline/model trace for the honest stage-by-stage breakdown.
- **The workflow:** ingest & deterministic checks → the one agent determines treatment + confidence + evidence → route (never write-back, FR7 — hard constraint, not a design choice) → the analyst files it herself, always.
- **Where the human stays, and why there specifically:** every determination requires an analyst action before filing, at every confidence level — because the system literally cannot write to SAP. Precision on auto-processed, recall on routing (the Head of Tax Risk's "wrong matters more than slow," made into an actual metric target).
- The knowledge-base feedback loop: an analyst's override becomes a reviewed, auditable rule — not a one-off judgment lost after the fact. This is the concrete answer to "how does this get more accurate over time."

### Slide 4 — The information model: eight entities, one flow (brief's point 3 — answered directly against all 8 named terms)
- **Legal entity** — the Northgate operating company that books the transaction and files the return.
- **Jurisdiction** — the actual rules boundary, not hub — its own reclaim window, invoice rules, filing frequency. EMEA alone spans a 2-year (France) to 5-year (Netherlands) window.
- **Supplier** — the real-world business Northgate buys from, resolved across possibly-duplicate vendor master records (entity resolution, FR2a/DR2 — not an afterthought).
- **Transaction** — the atomic unit of record: one supplier, one invoice, one legal entity, one point in time. Batch is a UI convenience only (DR3).
- **Invoice** — the supplier's own document; not always sufficient alone for 2 of the 3 required determinations (case-facts.md §7).
- **Recoverability determination** — the output: charged correctly / recoverable / where reported, plus confidence.
- **Filing period** — the monthly or quarterly cadence a determination gets swept into.
- **Reclaim** — the actual right to recover input tax, alive until its jurisdiction's window closes; time-to-expiration tracks this per transaction, not per jurisdiction (Italy/India bind to a return-filing date, not a rolling count).
- **How they relate:** legal entity buys from supplier (resolved) → transaction, documented by invoice → evaluated against jurisdiction rules → recoverability determination → filed in the next filing period → if recoverable, an active reclaim ticking down to the window.
- **Left out of v1:** legal entity isn't yet independent from jurisdiction (assumed near 1:1); credit notes are named but not yet linked to a specific prior transaction; filing period is a jurisdiction attribute, not its own tracked record; also automated supplier outreach, full China fapiao support, SAP consolidation.
- **What breaks if this is wrong:** a hub-level (not jurisdiction-level) rules model would treat a 5-year Netherlands claim as expired at whatever the coarser EMEA minimum is — actively abandoning recoverable money.

### Slide 5 — The prototype, live (brief's point 4 — up to 3 minutes, inside the 10)
- One slide of setup, then hand off to the actual live run — do not screenshot it
- What to show, in order: the sorted sheet (urgency beats confidence — INV-1004 first) → the duplicate-vendor flag (all 3 conflicting vendor records, EMEA manager's exact complaint) → the override → approve → re-run sequence proving the feedback loop actually works
- One thing chosen not to build: automated supplier outreach (EX1) — a different kind of system
- One thing that surprised us: RAG retrieval doesn't filter for relevance by default — the model cited an available knowledge-base entry that didn't actually apply, until explicitly required to justify the citation. Real finding, from an actual run, then actually fixed on the next one.

### Slide 6 — The risk, and how we bound it (shown right after the live demo, on purpose)
- The confusion matrix, defined for our determination (recoverable: yes/no): true positive (flagged recoverable, genuinely is — captured correctly), false positive (flagged recoverable, actually isn't — if auto-filed, this *is* the $4M penalty problem), false negative (not flagged, but was recoverable — contributes to the $8-30M left on the table), true negative (not flagged, genuinely not recoverable — correctly ignored)
- Design response: precision on auto-processed determinations (minimize false positives, "wrong matters more than slow"); recall on routing (minimize false negatives, never silently decide "not recoverable" with unearned confidence)
- **The baseline we hold ourselves to:** Phase 1 measures the current human-only process's actual precision/recall empirically — the number the system has to beat, specifically on the auto-processed bucket, since that's exactly where a wrong answer slips through fastest if the analyst blindly accepts a high-confidence batch. See `answers/02-workflow-proposal.md`'s expanded reasoning on why this baseline matters for that specific moment, not as a general QA metric.
- Closing line: we don't ask her to double-check what she's told is safe — we build the system to earn not needing that.

### Slide 7 — Phasing, timeline, pricing logic (brief's point 5 — logic, not exact numbers)
- Calendar: signing → 11-week security review runs in parallel with an 8-week sandboxed build (not sequentially) — this is the only way the VP's year-end-close ask is achievable at all on this timeline
- Phase 1 (EMEA/Rotterdam): clears the urgent-recoverables backlog — cash first, not headcount reduction, because cash doesn't depend on the coding-bottleneck diagnosis being right and matches the Head of Tax Risk's actual risk tolerance
- Phase 2+ (India, targeted — not "all of APAC"): Cost-of-Delay-ranked, not just build-tractability-ranked
- Pricing: fixed-fee + narrow contingency in Phase 1, expanding to contingency on the full ongoing recovered-$ in Phase 2+ once three conditions are proven (human-in-the-loop control, tracked metrics, demonstrated below-baseline error cost) — phased, not permanently narrow

### Slide 8 — What the VP is wrong about (brief's point 6)
- Her own words: *"If AI codes the invoices, I free 24 people to do analysis instead of data entry. That is the whole business case."*
- She's treating "coding" as mechanical data entry, separable from tax judgment. It isn't — the tax code assigned during coding **is** the "charged correctly / recoverable" determination, just recorded as a code instead of a sentence.
- The EMEA manager's own words confirm it: *"Coding is not the hard part."* The real bottlenecks sit upstream — dirty supplier data, non-compliant invoices.
- **How to tell her:** the freed capacity shouldn't go to a vague "analysis" bucket — it should go to the two concrete problems her own team already named, which is a more specific, more defensible reframe than "you asked for the wrong tool," because it's built entirely from her team's own words.

---

## PART 2 — IS THIS A PRODUCT? (5 minutes, 4 slides max)

### Slide 9 — Recommendation, one sentence (brief's point 1 — mandatory, first slide of this part)
- **"Yes, conditionally"** — the core capability (jurisdiction-aware determination + entity resolution across fragmented ERP data) is a real, differentiated wedge nobody found doing exactly this — but only if scoped to the right niche, and only if the vendor-security-review overhead is treated as something to systematically shrink, not absorb per customer.

### Slide 10 — The first niche (brief's point 2)
- Segment by **ERP fragmentation from M&A history** (not just size) — this is the sharper filter than revenue alone; a clean single-ERP company has no need for the differentiated capability here
- $10-20B+ revenue, genuine multi-jurisdiction VAT/GST exposure (not primarily US domestic sales tax), fragmented multi-instance ERP
- **Refuse:** no in-house indirect-tax function of meaningful size (no risk-owner to pair with the human-in-the-loop model); single-ERP/clean-data companies; primarily-domestic-sales-tax exposure

### Slide 11 — Opportunity size + packaging/pricing (brief's points 3 and 4, combined)
- ~350-550 public multinationals in Northgate's tier (real revenue-rank data) × ~30-50% niche filter (judgment call, flagged as such) ≈ **100-275 company SAM**
- Illustrative per-account ceiling at full Phase 2+ contingency maturity: **$1.2-7.5M/year** — theoretical ceiling, not a near-term number; the real constraint is sales/review velocity, not market size
- Packaging: the phased-contingency structure **is** the expansion mechanism — a pilot converts to recurring automatically as trust conditions are proven, not via a separate renegotiation

### Slide 12 — What has to be true (brief's point 5 — "we will push hardest here")
- **H5 (strongest yes):** jurisdiction rule packs are genuinely shared assets — the same France/Germany/Italy rules apply to any multinational, built once, reused indefinitely
- **H3 (biggest controllable risk):** the ~11-week security review must become a compounding asset (a reusable trust package) — otherwise this stays a service business, not a product, no matter how good the technology is
- **H4 (the one nothing here can resolve):** the 100-275 SAM estimate needs real pipeline data, not just this arithmetic
- One line on the open consideration, if asked: compute cost doesn't pool across customers the single-tenant model requires (each customer's deployment is billed to them directly) — the security-review trust package compounds in Ampliwork's favor; compute-cost optimization has to be re-earned per customer

---

## What's NOT in the deck (lives in the appendix/pre-read/Q&A prep instead)
- Full claims ledger, full research sourcing — `claims.md`, `research/*.md`
- The full analyst day-in-the-life and wireframe — reference material for design discussion, not pitch content (the live demo replaces it)
- Deep SAP transaction-code mechanics, security-review questionnaire details (SIG/CAIQ) — Q&A ammunition, not slide content
