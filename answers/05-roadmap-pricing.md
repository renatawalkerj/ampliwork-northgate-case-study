# Customer roadmap: phasing, timeline, pricing logic (Part 1.5)

Status: not started. See `OUTLINE.md`, "Step: customer roadmap." Needs `research/assumed-customer-profile.md` (signing date) and `research/commercial-models.md` first.

## Pilot scope: EMEA (Rotterdam hub) first, then expand
**ASSUMED, tag in `claims.md`.** EMEA is the first hub, not a random or arbitrary choice, for four independent reasons:
1. **The EU VAT Directive is harmonized** (Article 226's 15-field invoice standard applies across all member states) — the most tractable regulatory environment to build a robust rules engine against first, unlike the fragmented US (50 states, no harmonizing directive) or APAC (no common regime at all).
2. **It's where the one falsifiable, specific complaint lives** — the EMEA regional manager's "a third of our supplier master data is wrong." Piloting there tests her hypothesis directly, where she can see it — turns the sharpest skeptic into either an ally (if validated) or forces an early, cheap correction to the diagnosis (if not).
3. **It's consistent with "prove the hard case first,"** already the roadmap's own logic — EMEA being the hardest data-quality case is a reason to start there, not to avoid it.
4. **It has the single tightest reclaim window found across all research** — Italy's current rule caps input VAT deduction at the annual return filing deadline, giving a December invoice as little as ~4-5 months of runway. That beats every other finding, including APAC's India (~8mo floor) and Americas' Canada (~2yr for large businesses). See `case-facts.md` §4. This is the sharpest urgency argument of the four, not just an additional data point.

**Two separate assumptions stacked in reasons 1-3, tag both distinctly:** (a) EMEA has the most countries in Northgate's footprint — consistent with the assumed 30-country-by-hub distribution in `case-facts.md` §4; (b) more countries implies more AP volume/payables — a second, unverified assumption layered on top, since the brief gives no data on relative volume by hub. Reason 4 (Italy's window) doesn't depend on either of these — it holds regardless of the volume assumption.

## Sequencing after EMEA: two lenses that disagree, and how we resolve it
**Build-tractability lens** (how hard is it to build for): EMEA → Americas → APAC — APAC's regulatory fragmentation makes it the hardest to build for as a whole hub.

**Cost of Delay lens** (Reinertsen's framework — ASSUMED/general knowledge, ranking by what delay actually destroys, not what's easiest to build): rank hubs by their real tightest floor, since a tighter window means unclaimed money there is decaying into permanent loss faster while we're busy elsewhere. That ranking is EMEA (Italy, ~4-5mo) → **APAC (India, ~8-20mo)** → Americas (Canada, ~2yr large-business threshold) — the *opposite* middle slot from the tractability lens.

**These conflict on APAC vs. Americas, and we shouldn't paper over it.** The resolution: don't sequence phase 2 by hub at all — sequence by *jurisdiction*, the same unit of analysis already locked into the info model (§ jurisdiction-not-hub design decision). After the EMEA pilot, target the highest-cost-of-delay **jurisdiction** next — India specifically, not "all of APAC" — as a bounded, single-jurisdiction add-on proving the system handles a return-deadline-bound window correctly, before committing to APAC's full regulatory fragmentation. Americas (lower urgency, more tractable) follows. This keeps the rollout logic consistent with the data-model logic instead of switching frameworks between the two.

## To answer
1. Milestones sequenced against the 8-week build / 11-week security review / year-end close, with the riskiest question (does the exception path satisfy the Head of Tax Risk) proven early on bounded data, scoped to EMEA first per above.
1a. State plainly that Milestone 1's deliverable includes narrowing the $8-30M range using Northgate's own exception data — see `case-facts.md` §3. No external benchmark can do this; that's the actual justification for a diagnostic-first phase, not just a hedge.
2. What Northgate gets at the end of each milestone, and what it asks of them.
3. Pricing logic per phase (e.g. fixed-fee pilot vs. time-and-materials vs. converting to recurring), backed by real commercial-model research — not a guessed number.
