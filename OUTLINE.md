# Ampliwork Case Study — Northgate Industries

**Due: EOD Thu Sep 10, 2026** · Today: Sep 5 · 5 days out
**Ask, one line:** pitch an AI system for indirect-tax invoice recovery to a fictional client, live-demo a working prototype, argue whether to productize it, send a one-page follow-up. Evaluated on thinking, not slides.

## Deliverables
- [ ] Deck: ≤8 slides (pitch) + ≤4 slides (product) = 12 max. Appendix optional, uncapped.
- [ ] Live prototype demo (not screenshots) — ≤3 min, must handle one messy input + show the exception path
- [ ] One-page pre-read email to the VP
- [ ] Survive: 1 live interruption during the pitch + a "we're changing one fact, 3 min to react" curveball in Q&A

## Contradictions to resolve first — judgment, not research
- VP: auto-coding frees 24 people → the business case. Head of Tax Risk (has veto): cares about *wrong*, not *slow* — paid $4M in penalties last year on returns filed on time and wrong.
- EMEA manager: coding isn't the hard part, supplier master data is (same supplier = 3 vendors, 3 tax profiles).
- APAC analyst: recovery loss is often invoice-format non-compliance, not misclassification.
- **Decide:** which failure mode is primary, state it as an assumption on one slide, and pick the one flow the prototype proves.

## Research needed — delegate to agents (Breakpoint A)
1. Indirect tax domain: VAT/GST recoverability rules, reclaim windows, invoice compliance requirements by jurisdiction.
2. SAP tax stack: multi-instance SAP + tax engine (Vertex/ONESOURCE/Avalara-type) integration patterns, read-only; realistic "no data leaves tenant" architecture (customer-tenant-hosted or on-prem model).
3. Enterprise vendor security review norms (~11 weeks) — how vendors phase delivery around them.
4. Comparable/competitor products in AI-for-tax-recovery — for Part 2 market sizing. Real players, real methodology, estimates labeled as estimates.

## Plan — target ~4 hours of your time

| Phase | Time | Mode | Output |
|---|---|---|---|
| 1. Diagnosis & scope | 45 min | Together | Locked diagnosis, info model v1, prototype flow chosen, "VP is wrong about ___" |
| **Breakpoint A** | — | Agents, background | Research: tax domain, SAP/no-data-leaves-tenant architecture, security-review phasing, comparables |
| 2. Lock the plan | 30 min | Together | Architecture + phasing decided, product niche & market-size approach decided |
| **Breakpoint B** | — | Agents, background | Build prototype (messy-input flow + exception path) |
| 3. Deck + pre-read draft | 90 min | Together | Slide narrative (both parts), pre-read draft |
| 4. Test + integrate | 45 min | Together | Demo rehearsed inside the deck flow, breaks fixed |
| 5. Polish + curveball prep | 30 min | Together | Final deck, final pre-read, list of "what fact might they change" to rehearse reacting to |

## PIL rule
No market-size number, competitor claim, or domain fact goes in the deck as fact until it's VERIFIED in `claims.md` — either sourced or signed off by you. Default status: ASSUMED.

## Next action
Start Phase 1 together: read the contradictions above, pick a diagnosis.
