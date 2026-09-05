# Ampliwork Case Study — Northgate Industries

**Due: EOD Thu Sep 10, 2026** · Today: Sep 5 · 5 days out
**Ask, one line:** pitch an AI system for indirect-tax invoice recovery to a fictional client, live-demo a working prototype, argue whether to productize it, send a one-page follow-up. Evaluated on thinking, not slides.

## Deliverables
- [ ] Deck: ≤8 slides (pitch) + ≤4 slides (product) = 12 max. Appendix optional, uncapped.
- [ ] Agent/workflow proposal, with a stated human-in-the-loop point (Part 1 proposal)
- [ ] Information model — a concise version plus full entity-by-entity detail as reference material (Part 1 info model)
- [ ] Customer roadmap (phasing, timeline, **and pricing logic**, mapped to stakeholder needs) (Part 1 phasing)
- [ ] Live prototype demo (not screenshots) — ≤3 min, must handle one messy input + show the exception path. Brief explicitly says low fidelity/ugly is fine — the "wow" has to come from nailing the hard case, not from polish. Don't spend build budget on cosmetics.
- [ ] Eval harness for the prototype — doubles as a client-facing roadmap item
- [ ] Productization recommendation (Part 2) — yes/no, niche, market sizing, packaging/pricing logic
- [ ] One-page pre-read email to the VP
- [ ] "How we built this" appendix — PIL claims ledger + tools/frameworks used (answers the brief's "tell us what you used, where it helped, where it led you astray")
- [ ] Talking points ready, not slides: one thing chosen **not** to build and why; one thing that surprised you while building it
- [ ] Survive: 1 live interruption during the pitch (unscripted — "handle it however you would in the room") + the fact-change curveball at the start of Q&A + general pushback through the 15 min of questions

## Stakeholder map — a method, not a guess
No external fact to look up here (fictional client), but there's a real technique: stakeholder mapping (champion / approver / gatekeeper), not vibes. Six voices, two roles that matter most:

- **Champion — VP, Global Indirect Tax.** Holds budget, sponsor, already sold it to the CFO. Her quotes ("free 24 people from data entry, that's the whole business case" / "I need a number I can defend by year-end close") are a throughput-and-ROI story. She needs us to be right — her credibility is already staked on it upward.
- **Approver we actually have to convince — Head of Tax Risk.** No budget, no enthusiasm, but "nothing ships without her." Her quote ("$4M in penalties last year on returns filed on time and wrong — I care far more about wrong than slow") reframes the whole deal around correctness, not speed. Win the VP and lose her, and the deal is dead. **Budget-holder ≠ approver is itself the central risk in this deal.**

**Everyone else — not deciders, but each can quietly break the plan:**
- *EMEA regional manager (9 yrs)*, practitioner reality-check — says the VP's own diagnosis is wrong: coding isn't the bottleneck, dirty supplier master data is (same supplier, 3 tax profiles). If true, it changes what the prototype needs to prove.
- *APAC analyst*, practitioner reality-check — a third root cause: much of the loss is non-compliant supplier invoices, not misclassification. Caps how much of the $8–30M an AI classifier can ever recover — a scope boundary to state, not hide.
- *Head of Tax Technology*, technical gatekeeper — can't approve the deal but can make it unbuildable: 3 SAP instances, no consolidation before 2029.
- *Enterprise security*, compliance gatekeeper — owns the ~11-week review that collides with the 8-week build window. Not a vote on the idea, but can stall or kill the timeline regardless of who's sold.

**Decide after Breakpoint A research (not before):** which root-cause story (VP's / EMEA's / APAC's) is primary. This needs the domain briefings first — you can't credibly weigh "is dirty supplier master data really the bigger loss driver than format non-compliance" without knowing how indirect tax recovery actually works.

**Worth noting on stage:** Northgate itself can't agree on the $8–30M figure, and the width of that range is part of the problem, not incidental to it — likely evidence for whichever diagnosis points at a data-quality root cause.

## Frameworks in play
- **PIL** — claims stay ASSUMED until sourced or you sign off. Governs the domain research below, the customer-profile numbers, and shows up in the deck itself as the "how we built this" appendix.
- **Build Engine** (`pil/build-engine/`) — PRD → architecture decision → parallel background-agent build. Runs the prototype build at Breakpoint B. Also the pattern we'd propose to Northgate for the real build, so it doubles as roadmap credibility.
- **Consulting frameworks** (`career/Consulting management books/`) — fast-pass extraction, not full reads, mapped to specific steps:
  - *Bulletproof Problem Solving* (Conn & McLean) → structuring the diagnosis and the productization case
  - *Playing to Win* (Lafley & Martin) → the "where to play / how to win" niche choice (Part 2)
  - *The McKinsey Way* (Rasiel) → yours to draw on for pitch structure and storyline when you design the deck
  - *The Flawless Consulting Fieldbook* (Block) → stakeholder handling — VP vs. Head of Tax Risk, the "she's wrong about X" moment, pre-read tone, composure under pushback

## Step: get you to expert level — fast pass, runs first (Breakpoint A)
Three domain tracks, each a short list of real sources plus a brief you can skim fast, not study. Goal: enough to hold your own against the Head of Tax Risk, not exhaustive mastery. This has to land *before* the diagnosis decision, the workflow/info-model design, and the prototype design — all three depend on it.
1. **Indirect tax domain** — VAT/GST/sales-and-use mechanics, recoverability, reclaim windows, invoice compliance rules by jurisdiction.
2. **SAP technical domain** — multi-instance SAP + tax engine (Vertex/ONESOURCE/Avalara-type) integration patterns, what read-only access actually constrains.
3. **Vendor security review norms** — what an ~11-week enterprise security review checks and how vendors typically phase delivery around it.
4. **Commercial models already in this space** — what tax-recovery specialists and tax-tech vendors actually charge today (contingency fee as % of recovered amount is common in VAT reclaim specifically, vs. per-transaction fees, seat/subscription pricing, fixed implementation + retainer). Real reference points, not a guessed number — feeds both the Part 1 engagement pricing and the Part 2 productization pricing.

## Step: agent & workflow design (Part 1, point 2)
"What you propose" — the core of the pitch, not a bullet inside the diagnosis. Shaped by two hard constraints, not just preference:
1. **Read-only SAP, no writes, any version** — the agent can never file or post anything itself. Something else — a human, or a downstream system — has to own write-back. Name it.
2. **The Head of Tax Risk's veto** — she needs to see where a human sits in the loop and why *there specifically*, not just "a human reviews it somewhere."
3. Define: the agent(s), the workflow stages end to end, the exact point(s) a human is in the loop and the reason for each. Feeds directly into the prototype's exception path and the roadmap's shadow-mode milestone.

## Step: information model (Part 1, point 3)
The brief names the entities explicitly — don't improvise a different set. Define, and diagram if useful:
1. **Legal entity, jurisdiction, supplier, transaction, invoice, recoverability determination, filing period, reclaim** — what each means in Northgate's world and how they relate.
2. What's deliberately left out of v1 (e.g., is "supplier" one entity or does it need a dedupe/identity layer given EMEA's 3-vendors-1-supplier problem?) and what breaks if the model is wrong.
3. Needs the tax + SAP domain briefings first — these entities have real-world SAP/tax-engine analogs, don't invent them from scratch. If the research doesn't pin down entity-level detail (attributes, exact relationships) that a real SAP/tax-engine data model would have, treat that as a gap to research one layer deeper before guessing — and only if it's still unresolved, assume it was clarified with the customer during discovery, tagged ASSUMED in `claims.md` like the customer profile below.
4. Write it up as two clean pieces — a concise version and the full entity-by-entity detail — and leave what becomes slide vs. appendix to the deck-design step, not here.

## Step: business case — assumed customer profile
The brief omits the numbers a real deal needs, and we can't email the fictional client. So: construct the missing customer facts ourselves, grounded in the domain research, not invented from nothing.
1. AP volume per hub, invoice mix, avg invoice value, current team cost, today's recovery rate.
2. **A contract-signing date** — needed to put the 8-week build and the 11-week security review on an actual calendar against the year-end close. Assume the engagement signs shortly after this pitch; this is the number the whole roadmap timeline hangs on.
3. Tag every figure ASSUMED with its reasoning, in `claims.md`. Used to make the ROI/market-sizing arithmetic defensible under a skeptic's pushback — where Part 2 gets pushed hardest.

## Step: customer roadmap — needs mapped to milestones, phasing + pricing logic (Part 1, point 5)
Not "build the final thing and hope it fits" — sequence around what Northgate actually needs at each stage, and around one hard fact: **the 11-week security review outlasts the 8-week build by ~3 weeks.** Early milestones can't depend on full production access, because it isn't cleared yet. So: de-risk the most contested question first, on bounded/sandboxed data, and only expand access as trust and the review both clear.
1. List each stakeholder's need from the map above (VP: freed headcount + defensible year-end number; Head of Tax Risk: proof of correctness before scale; EMEA: master-data problem not ignored; APAC: compliance-chasing burden; Tech: works across 3 unconsolidated instances; Security: review satisfied, nothing leaves tenant).
2. Sequence milestones so the riskiest/most contested thing (does the exception path actually satisfy the Head of Tax Risk) gets proven early and cheaply, before asking for full production trust.
3. For each milestone: what Northgate gets, what it asks of them, **and the pricing logic for that phase** (e.g., fixed-fee pilot vs. time-and-materials vs. converting to recurring) — logic, not exact numbers. Lands on the signed timeline from the business-case step above.

## Step: prototype data
1. Search for open-source invoice/tax datasets first — check license and realism.
2. If nothing usable: hand-build synthetic data using the domain briefings above — one clean invoice, one non-compliant-format invoice, one duplicate-supplier-three-tax-profiles case, one missing-field case. (Invoices in the brief span 14 languages — worth deciding if the messy case should reflect that.)
3. Log which path we took and why in `claims.md`.

## Step: evals — first-class, not an afterthought
1. Before building, define what "correct" looks like for the prototype's flow: treatment call, confidence, exception routing.
2. Build a small eval set from the synthetic data above.
3. In the deck, present evals as a roadmap deliverable to Northgate — not internal QA. It's the trust mechanism the Head of Tax Risk actually wants, and the first milestone's proof point above.

## Step: is this a product? (Part 2)
1. Recommendation, one sentence — yes or no, defended.
2. First niche — *Playing to Win*'s where-to-play/how-to-win: segment by size, geography, ERP landscape, buying trigger; name who we'd refuse to sell to.
3. Market-sizing arithmetic, defensible — built from the comparables research and the assumed customer profile extrapolated across the niche (how many companies look like Northgate).
4. Packaging/pricing logic — how a pilot converts into something recurring.
5. What has to be true for this to be a product, not a series of custom builds — *Bulletproof Problem Solving*'s hypothesis test. This is what gets pushed hardest.

## Step: Q&A and composure prep
Distinct from the deck — this is rehearsal, not content. Evaluation criteria explicitly reward defending a position, updating it when the argument is good, and saying "I don't know" when true — bluffing is penalized.
1. Rehearse reacting to the fact-change curveball fast — assume the tightest plausible window.
2. Mock pushback round on the diagnosis, the architecture, and the productization case — not just the scripted curveball.
3. Land on the one thing not built (and why) and the one build surprise, ready to say out loud.

## Plan

| Phase | Time | Mode | Output |
|---|---|---|---|
| 0. Kick off research | 15 min | Together | Confirm research questions, launch Breakpoint A |
| **Breakpoint A** | agent time, background | Agents | Fast-pass domain briefings (tax / SAP / security review / commercial models), consulting-framework extraction, comparables research, open-data search |
| 1. Diagnose, propose & model | 60 min | Together | Read briefings → diagnosis locked, agent/workflow design, info model v1, prototype flow chosen, "VP is wrong about ___" |
| 2. Business case, roadmap & product case | 60 min | Together | Assumed customer profile + signing date, customer roadmap (needs → milestones → pricing logic), product niche & market-sizing approach, data plan, eval plan |
| **Breakpoint B** | agent time, background | Agents (Build Engine) | PRD → prototype build + eval harness, on the data plan above |
| 3. Consolidate findings | 60 min | Together | Clean, concise write-up of every locked decision — diagnosis, workflow, info model, roadmap, business case, product case — content only, no deck yet. Pre-read draft. |
| 4. Test + integrate | 45 min | Together | Prototype passes its evals |
| 5. Design the deck & story | — | You, solo | Slide flow and narrative, whichever pitch framework fits — your call. We're on hand if you want a sounding board, not to design it for you. |
| 6. Polish + curveball prep | 30 min | Together | Final deck, final pre-read, PIL appendix, Q&A/composure rehearsal |

**Together time ≈ 4.5 hrs** — close to the original 4-hour hope; deck design is your own time and isn't counted here. Splits cleanly across the 5 days to Thursday — no need to do it in one sitting.

## PIL rule
No market-size number, competitor claim, domain fact, or customer-profile figure (including the signing date) goes in the deck as fact until it's in `claims.md` — sourced, or explicitly signed off by you as a stated assumption. Default status: ASSUMED.

## Next action
Kick off Phase 0: confirm the research questions above and launch Breakpoint A.
