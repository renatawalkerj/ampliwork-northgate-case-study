# Customer roadmap: phasing, timeline, pricing logic (Part 1.5)

Status: not started. See `OUTLINE.md`, "Step: customer roadmap." Needs `research/assumed-customer-profile.md` (signing date) and `research/commercial-models.md` first.

## Pilot scope: EMEA (Rotterdam hub) first, then expand
**ASSUMED, tag in `claims.md`.** EMEA is the first hub, not a random or arbitrary choice, for four independent reasons:
1. **The EU VAT Directive is harmonized** (Article 226's 15-field invoice standard applies across all member states) — the most tractable regulatory environment to build a robust rules engine against first, unlike the fragmented US (50 states, no harmonizing directive) or APAC (no common regime at all).
2. **It's where the one falsifiable, specific complaint lives** — the EMEA regional manager's "a third of our supplier master data is wrong." Piloting there tests her hypothesis directly, where she can see it — turns the sharpest skeptic into either an ally (if validated) or forces an early, cheap correction to the diagnosis (if not).
3. **It's consistent with "prove the hard case first,"** already the roadmap's own logic — EMEA being the hardest data-quality case is a reason to start there, not to avoid it.
4. **It has the single tightest reclaim window found across all research** — Italy's current rule caps input VAT deduction at the annual return filing deadline, giving a December invoice as little as ~4-5 months of runway. That beats every other finding, including APAC's India (~8mo floor) and Americas' Canada (~2yr for large businesses). See `case-facts.md` §4. This is the sharpest urgency argument of the four, not just an additional data point.

**Two separate assumptions stacked in reasons 1-3, tag both distinctly:** (a) EMEA has the most countries in Northgate's footprint — consistent with the assumed 30-country-by-hub distribution in `case-facts.md` §4; (b) more countries implies more AP volume/payables — a second, unverified assumption layered on top, since the brief gives no data on relative volume by hub. Reason 4 (Italy's window) doesn't depend on either of these — it holds regardless of the volume assumption.

**Sequencing after EMEA:** expand to Americas next (Canada's 2yr large-business threshold is the real floor there, per `case-facts.md` §4 — more tractable than APAC's fully fragmented regimes), APAC last. Note APAC's own floor (India, ~8-20mo) is tighter than its Singapore-anchored 5yr headline suggested — worth naming when justifying why APAC still isn't first despite that, since the reason is regulatory fragmentation and tractability, not urgency.

## To answer
1. Milestones sequenced against the 8-week build / 11-week security review / year-end close, with the riskiest question (does the exception path satisfy the Head of Tax Risk) proven early on bounded data, scoped to EMEA first per above.
1a. State plainly that Milestone 1's deliverable includes narrowing the $8-30M range using Northgate's own exception data — see `case-facts.md` §3. No external benchmark can do this; that's the actual justification for a diagnostic-first phase, not just a hedge.
2. What Northgate gets at the end of each milestone, and what it asks of them.
3. Pricing logic per phase (e.g. fixed-fee pilot vs. time-and-materials vs. converting to recurring), backed by real commercial-model research — not a guessed number.
