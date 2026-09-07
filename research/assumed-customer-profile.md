# Assumed customer profile

Status: fully drafted against the original 6-item list (AP volume per hub, invoice mix, avg invoice value, team cost, recovery rate, signing date). Grounded in the brief's own numbers and the named country footprint (`case-facts.md` §4) where they exist; stacked assumptions clearly labeled where they don't. Every figure here is mirrored in `claims.md`. Used to make the ROI/market-sizing arithmetic in `answers/06-productization.md` defensible under pushback — not to be quoted as Northgate fact in the room.

## 1. AP transaction volume — total and per hub

**Anchor (real, verbatim brief quote, not an estimate):** "Every month they work through hundreds of thousands of accounts payable transactions" (`case-facts.md` §1).

**ASSUMED — the range "hundreds of thousands" implies:** reading it as low-to-mid hundreds (not approaching a million), a working range of **200,000–500,000/month**, midpoint **~350,000/month → ~4.2M/year.**

**Per-hub split, done properly this time — weighted by economic/industrial size, not by raw country count.** Flat country-count (7/14/9) was rejected earlier because volume and country-count aren't necessarily correlated — a few large-economy countries can outweigh many small ones. Using the named 30-country footprint (`case-facts.md` §4) and a simple, transparent 3-tier economic-size proxy (Tier 1 = major industrial economy, weight 3; Tier 2 = mid-size, weight 2; Tier 3 = smaller, weight 1) — chosen because AP transaction volume for a physical-goods manufacturer scales with production/logistics activity, which scales with economic size, not headcount:

| Hub | Countries by tier | Weight | Share |
|---|---|---|---|
| **Americas** | T1: US · T2: Canada, Mexico, Brazil · T3: Argentina, Chile, Colombia | 3+2+2+2+1+1+1 = **12** | ~23.5% |
| **EMEA** | T1: UK, Germany, France · T2: Netherlands, Italy, Spain · T3: Belgium, Poland, Sweden, Switzerland, Austria, Czech Republic, Turkey, South Africa | 3+3+3+2+2+2+1×8 = **23** | ~45.1% |
| **APAC** | T1: China, Japan · T2: India, South Korea, Australia · T3: Singapore, Thailand, Vietnam, Indonesia | 3+3+2+2+2+1×4 = **16** | ~31.4% |
| **Total** | 30 countries | **51** | 100% |

Applied to the ~4.2M/year midpoint:

| Hub | Annual transactions (approx.) | Monthly (approx.) |
|---|---|---|
| Americas | ~990,000 | ~82,000 |
| EMEA | ~1,895,000 | ~158,000 |
| APAC | ~1,315,000 | ~110,000 |

**Worth stating in the room if pushed on methodology:** this weighted split lands within ~2 percentage points of the naive country-count split (23%/47%/30%) — the correction doesn't overturn the country-count picture, it *reinforces* it. That's a useful sentence to have ready: EMEA's volume lead isn't an artifact of counting more countries, it holds up under a materially different (size-weighted) methodology too — which strengthens, not weakens, the EMEA-first pilot argument (`case-facts.md` §4), even though that decision itself is driven by reclaim-window urgency and rule harmonization, not volume.

## 2. Invoice / transaction mix

**Not previously addressed — filling the gap.** Constructed from the brief's own evidence-document list (`case-facts.md` §5: invoices, purchase orders, goods receipts, contracts, customs paperwork, credit notes) and general knowledge of an industrial manufacturer's AP composition. All percentages ASSUMED, illustrative only:

| Category | Share of transaction volume | Reasoning |
|---|---|---|
| Raw materials / components | ~60% | Highest-volume, lowest-complexity category for a manufacturer — recurring supplier relationships, largely domestic or intra-region |
| Capital goods / equipment | ~20% | Lower volume, higher dollar value per transaction; more likely to involve customs paperwork on cross-border purchases |
| Services (logistics, consulting, cross-border intercompany) | ~15% | Most likely to require reverse-charge treatment and a contract to resolve recoverability — this is the category INV-1005 in the prototype represents |
| Credit notes / corrections / other | ~5% | Residual |

**Cross-border share:** ASSUMED **~30–35%** of transactions are cross-border within Northgate's own operations (a global manufacturer sourcing across its 30-country footprint), the remainder domestic-to-hub-country supplier relationships. Cross-border transactions are disproportionately represented in the "requires customs paperwork" and "requires contract" evidence categories.

**Evidence-dependency implication (ties directly to FR1a/FR1b):** combining the two splits above, an estimated **~75–80% of transactions** (raw materials + credit notes/other) are plausibly resolvable from invoice + purchase order + goods receipt alone; the remaining **~20–25%** (capital goods + services) more often need a contract or customs document to fully resolve recoverability or cross-border treatment. **This is the rough scale of the "evidence beyond the invoice" engineering surface** — useful context for scoping FR1a/FR1b, though it should be presented as a plausibility estimate, not a measured figure; the actual mix is exactly the kind of thing Phase 1's own diagnostic measurement would establish for real.

## 3. Average invoice value (cross-check, not a new anchor)

**ASSUMED, derived from two independent stacked estimates already in `claims.md`:** AP spend ≈ 40–60% of Northgate's ~$14B revenue → **~$5.6B–$8.4B annual AP spend.** Dividing by the transaction-volume estimate above (~2.4M–6M/year) gives an implied average invoice value of roughly **$1,000–$3,500**, midpoint **~$1,700.**

**Cross-checked against the invoice-mix split above, for an extra plausibility pass:** if capital goods (~20% of volume) carry a materially higher average value than raw materials (~60% of volume) — a reasonable expectation for an industrial manufacturer — a blended average in the low thousands is exactly what a mix skewed toward high-volume/lower-value raw-materials transactions, with a smaller high-value capital-goods tail, would produce. Two independently-derived numbers (a headcount/volume-based path and a revenue-based path) landing in the same believable range is mild corroboration, not confirmation — it's built on the 40–60% AP-spend ratio (itself unsourced to Northgate) stacked on the transaction-volume range above.

## 4. Current indirect-tax team cost

**ASSUMED:** 24 indirect-tax FTEs (brief fact) × an assumed blended fully-loaded cost of **~$150,000/person/year** (a reasonable blended estimate for a mixed-seniority team spanning US/EU/APAC, not sourced to a specific benchmark) → **~$3.6M/year total team cost.**

**What this is for, and what it isn't:** useful only as a capacity-value reference point if the deck needs to translate "frees 24 people for analysis" into a dollar figure — it is explicitly **not** a labor-cost-reduction pitch (nobody is being let go; `answers/05-roadmap-pricing.md` already establishes cash, not headcount reduction, as the lead value metric). Flag this distinction if the number comes up: it quantifies redeployed capacity, not savings.

## 5. Today's recovery rate — deliberately not constructed

**Not estimated, and this is a decision, not an oversight.** `claims.md`/row 33 already establishes that no current error rate is computable from the brief's numbers — the brief gives costs ($4M, $8–30M), not a transaction-volume-weighted error rate, and stacking enough assumptions to force a number here would produce something less defensible than just saying so. **The correct answer, stated the same way it already is elsewhere:** this gets measured empirically in Phase 1 by sampling and re-reviewing past determinations (`answers/02-workflow-proposal.md`) — it is not something this profile fabricates in advance. Do not let a productization or market-sizing slide imply a recovery-rate baseline exists yet; it doesn't.

## 6. Contract-signing date

**ASSUMED, constructed to anchor the calendar:** signing occurs within **~2 weeks of this pitch**, consistent with the VP's own urgency (already presented to the CFO, wants a working-capital number by year-end close). Against a **December 31 fiscal year-end** and the brief's own ~11-week security review starting at signing, that puts full production access at roughly **mid-to-late week 13 post-pitch** — after year-end close, not before it.

**This is exactly why the sandbox → shadow-mode → staged-access sequencing already in the plan matters, not just as an architecture detail but as the thing that makes the VP's own deadline achievable at all:** the 8-week build runs against sandboxed/synthetic data in parallel with the security review (`research/security-review-norms.md`), so a working, evaluated system exists well before full production access clears — meaning the backlog-clearing run (Phase 1's actual value delivery) can start on staged/expanding real access as soon as it's granted, not only after the full 11 weeks complete. **Without this sequencing, the year-end-close ask is not achievable on this calendar at all** — worth stating plainly if asked how the timeline actually works, since "11 weeks starting at signing" alone would blow past most reasonable year-end-close deadlines if build and review ran strictly sequentially.

## Claims for claims.md

| Claim | Status | Source | Notes |
|---|---|---|---|
| Northgate processes ~200,000–500,000 AP transactions/month (~2.4M–6M/year), reading "hundreds of thousands" as low-to-mid hundreds | ASSUMED (range constructed from a real brief quote) | Brief: "every month they work through hundreds of thousands of accounts payable transactions" | The brief's number is real; the specific range within "hundreds of thousands" is our construction |
| Per-hub transaction-volume split, weighted by a 3-tier economic-size proxy against the named 30-country footprint: Americas ~23.5%, EMEA ~45.1%, APAC ~31.4% | ASSUMED (methodology constructed, not sourced) | Derived from `case-facts.md` §4's named country list + an original economic-size-tier weighting | Lands within ~2pp of the naive country-count split — reinforces rather than overturns the EMEA-volume-lead picture; still not a number to present as measured fact |
| Invoice/transaction mix: ~60% raw materials, ~20% capital goods, ~15% services, ~5% other; ~30-35% cross-border; ~20-25% of volume plausibly needs evidence beyond invoice+PO+goods receipt | ASSUMED (illustrative construction) | Derived from the brief's own evidence-document list (`case-facts.md` §5) + general manufacturing AP-composition knowledge | Gives FR1a/FR1b a rough engineering-scale estimate; the real mix is a Phase 1 measurement question, not something this file can determine |
| Implied average invoice value ≈ $1,000–$3,500 (midpoint ~$1,700), derived from stacking the AP-spend-% estimate against the transaction-volume estimate, cross-checked against the invoice-mix value skew | ASSUMED (cross-check only, stacked assumptions) | Derived from claims already in claims.md (AP-spend %) and the volume/mix estimates above | Mild corroboration only — not a number to state as fact |
| Indirect-tax team cost ≈ $3.6M/year (24 FTEs × ~$150K/person blended fully-loaded cost) | ASSUMED | N/A — general industry blended-cost estimate, not sourced to a specific benchmark | For capacity-value framing only, not a labor-cost-reduction claim |
| No current recovery-rate/error-rate baseline is estimated for Northgate — deliberately left unconstructed, to be measured empirically in Phase 1 | ASSUMED (as a decision not to estimate) | Consistent with claims.md row on no-current-error-rate-computable | Do not let a slide imply this baseline already exists |
| Contract signing assumed within ~2 weeks of the pitch, against a Dec 31 fiscal year-end; sandbox/shadow-mode build proceeds in parallel with the 11-week security review so a working system predates full production access | ASSUMED (calendar construction) | N/A — reasoning built from the brief's own stated timelines | This is the mechanism that makes the VP's year-end-close ask achievable at all on this calendar — worth stating explicitly if the timeline is challenged |
