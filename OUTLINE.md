# Ampliwork Case Study — Northgate Industries

**Due: EOD Thu Sep 10, 2026** · Today: Sep 5 · 5 days out
**Ask, one line:** pitch an AI system for indirect-tax invoice recovery to a fictional client, live-demo a working prototype, argue whether to productize it, send a one-page follow-up. Evaluated on thinking, not slides.

## Deliverables
- [ ] Deck: ≤8 slides (pitch) + ≤4 slides (product) = 12 max. Appendix optional, uncapped.
- [ ] Live prototype demo (not screenshots) — ≤3 min, must handle one messy input + show the exception path. Goal: it should feel like proof they've found the right partner, not a tech demo.
- [ ] Eval harness for the prototype — doubles as a client-facing roadmap item (see below)
- [ ] One-page pre-read email to the VP
- [ ] "How we built this" appendix — PIL claims ledger + tools/frameworks used (answers the brief's "tell us what you used, where it helped, where it led you astray")
- [ ] Survive: 1 live interruption during the pitch + a "we're changing one fact, 3 min to react" curveball in Q&A

## Stakeholder map — a method, not a guess
No external fact to look up here (fictional client), but there's a real technique: stakeholder mapping (champion / approver / gatekeeper), not vibes. Six voices, two roles that matter most:

- **Champion — VP, Global Indirect Tax.** Holds budget, sponsor, already sold it to the CFO. Her quotes ("free 24 people from data entry, that's the whole business case" / "I need a number I can defend by year-end close") are a throughput-and-ROI story. She needs us to be right — her credibility is already staked on it upward.
- **Approver we actually have to convince — Head of Tax Risk.** No budget, no enthusiasm, but "nothing ships without her." Her quote ("$4M in penalties last year on returns filed on time and wrong — I care far more about wrong than slow") reframes the whole deal around correctness, not speed. Win the VP and lose her, and the deal is dead. **Budget-holder ≠ approver is itself the central risk in this deal.**

**Everyone else — not deciders, but each can quietly break the plan:**
- *EMEA regional manager (9 yrs)*, practitioner reality-check — says the VP's own diagnosis is wrong: coding isn't the bottleneck, dirty supplier master data is (same supplier, 3 tax profiles). If true, it changes what the prototype needs to prove.
- *APAC analyst*, practitioner reality-check — a third root cause: much of the loss is non-compliant supplier invoices, not misclassification. Caps how much of the $8–30M an AI classifier can ever recover — a scope boundary to state, not hide.
- *Head of Tax Technology*, technical gatekeeper — can't approve the deal but can make it unbuildable: 3 SAP instances, no consolidation before 2029.
- *Enterprise security*, compliance gatekeeper — owns the ~11-week review that collides with the 8-week build window. Not a vote on the idea, but can stall or kill the timeline regardless of who's sold.

**Decide in Phase 1:** which root-cause story (VP's / EMEA's / APAC's) is primary, state it as an assumption on one slide, and pick the one flow the prototype proves.

## Frameworks in play
- **PIL** — claims stay ASSUMED until sourced or you sign off. Governs the domain research below, the customer-profile numbers, and shows up in the deck itself as the "how we built this" appendix.
- **Build Engine** (`pil/build-engine/`) — PRD → architecture decision → parallel background-agent build. Runs the prototype build at Breakpoint B. Also the pattern we'd propose to Northgate for the real build, so it doubles as roadmap credibility.
- **Consulting frameworks** (`career/Consulting management books/`) — fast-pass extraction, not full reads, mapped to specific steps:
  - *Bulletproof Problem Solving* (Conn & McLean) → structuring the diagnosis (Phase 1) and the productization case (Part 2)
  - *Playing to Win* (Lafley & Martin) → the "where to play / how to win" niche choice (Part 2)
  - *The McKinsey Way* (Rasiel) → pitch structure, hypothesis-driven storyline (Phase 3)
  - *The Flawless Consulting Fieldbook* (Block) → stakeholder handling — VP vs. Head of Tax Risk, the "she's wrong about X" moment, pre-read tone

## Step: get you to expert level — fast pass, before the prototype is designed
Three domain tracks, each a short list of real sources plus a brief you can skim fast, not study. Goal: enough to hold your own against the Head of Tax Risk, not exhaustive mastery.
1. **Indirect tax domain** — VAT/GST/sales-and-use mechanics, recoverability, reclaim windows, invoice compliance rules by jurisdiction.
2. **SAP technical domain** — multi-instance SAP + tax engine (Vertex/ONESOURCE/Avalara-type) integration patterns, what read-only access actually constrains.
3. **Vendor security review norms** — what an ~11-week enterprise security review checks and how vendors typically phase delivery around it.

## Step: prototype data
1. Search for open-source invoice/tax datasets first — check license and realism.
2. If nothing usable: hand-build synthetic data using the domain briefings above — one clean invoice, one non-compliant-format invoice, one duplicate-supplier-three-tax-profiles case, one missing-field case.
3. Log which path we took and why in `claims.md`.

## Step: business case — assumed customer profile
The brief omits the numbers a real deal needs, and we can't email the fictional client. So: construct the missing customer facts ourselves (AP volume per hub, invoice mix, avg invoice value, current team cost, today's recovery rate), grounded in the domain research, not invented from nothing.
1. Draft the assumed profile, each figure tagged ASSUMED with its reasoning, in `claims.md`.
2. Use it to make the ROI/market-sizing arithmetic defensible under a skeptic's pushback — this is where Part 2 gets pushed hardest.

## Step: evals — first-class, not an afterthought
1. Before building, define what "correct" looks like for the prototype's flow: treatment call, confidence, exception routing.
2. Build a small eval set from the synthetic data above.
3. In the deck, present evals as a roadmap deliverable to Northgate — not internal QA. It's the trust mechanism the Head of Tax Risk actually wants.

## Plan

| Phase | Time | Mode | Output |
|---|---|---|---|
| 1. Diagnosis & scope | 45 min | Together | Diagnosis locked, info model v1, prototype flow chosen, "VP is wrong about ___" |
| **Breakpoint A** | agent time, background | Agents | Fast-pass domain briefings (tax / SAP / security review), consulting-framework extraction, comparables research, open-data search |
| 2. Study + lock plan | 60 min | Together | Fast-pass on all 3 domains + relevant frameworks; architecture, niche, customer-profile assumptions, data plan, eval plan all locked |
| **Breakpoint B** | agent time, background | Agents (Build Engine) | PRD → prototype build + eval harness, on the data plan above |
| 3. Deck + pre-read draft | 90 min | Together | Slide narrative (both parts), pre-read draft, evals framed as a roadmap item |
| 4. Test + integrate | 45 min | Together | Prototype passes its evals, demo rehearsed inside the deck flow |
| 5. Polish + curveball prep | 30 min | Together | Final deck, final pre-read, PIL appendix, curveball rehearsal list |

**Together time ≈ 4.5 hrs** — a bit past the original 4-hour hope; the up-skilling and evals steps you just added are the reason. Splits cleanly across the 5 days to Thursday — no need to do it in one sitting.

## PIL rule
No market-size number, competitor claim, domain fact, or customer-profile figure goes in the deck as fact until it's in `claims.md` — sourced, or explicitly signed off by you as a stated assumption. Default status: ASSUMED.

## Next action
Start Phase 1 together: read the contradictions above, pick a diagnosis.
