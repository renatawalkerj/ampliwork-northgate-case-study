# Appendix — assumptions, research anchors, requirements, verification

Optional backing material, not part of the timed 15 minutes. Full detail and sourcing lives in `case-facts.md`, `claims.md`, and `requirements.md` — this condenses those into what's worth having on hand for Q&A.

## Assumptions
1. Hyperscaler: Azure — a settled premise for planning, not externally verified.
2. Country footprint: ~7 Americas / 14 EMEA / 9 APAC — constructed, not stated in the brief.
3. Contingency pricing is viable broadly, not narrowly carved out — revised after direct challenge.
4. Error-rate baseline doesn't exist yet — Phase 1 measures it, we don't assume it.
5. $4M penalty jurisdictions: left as stated (two, unnamed) — not invented for concreteness.
6. "A third of supplier master data is wrong": denominator unspecified (records / suppliers / $ volume) — doesn't change the severity call, does affect entity-resolution build size.

## Research anchors (verified unless noted)

**Reclaim-window urgency**, of 11 jurisdictions researched, tightest first:

| Rank | Jurisdiction | Window | Source |
|---|---|---|---|
| 1 | Italy | ~4–5mo (Dec invoice) to ~15–16mo (Jan); flat 2yr from 2027 | Secondary, converging |
| 2 | India | ~8–20mo, return-deadline-bound | Primary (CBIC) |
| 3 | China, if the fapiao-certification rule holds | ~12mo | ASSUMED, unverified |
| 4 | France / Canada (large business) | 2yr flat | Secondary / Primary (CRA) |
| 5 | UK / Germany / Canada (general) / US states | ~3–4yr | Secondary / Primary |
| 6 | Netherlands / Singapore | 5yr flat | Secondary / Primary (IRAS) |

Why it matters: a hub-level "5-year" story (Singapore) hides an ~8x-tighter real floor (India) in the same hub. Drives EMEA-first sequencing (Italy's floor) and India, specifically, as the Phase 2 target — not "all of APAC."

**EU invoice compliance is real, not an excuse.** Directive 2006/112/EC Art. 226 sets 15 mandatory fields. Germany's *Leistungsdatum* (date of supply) is a commonly-missed one. Italy/Poland/Spain are layering e-invoicing clearance mandates on top — a correctly-fielded invoice can still be rejected on schema grounds.

**SAP's duplicate-vendor mechanism independently corroborates the EMEA manager's claim.** 3 acquisitions → 3 SAP instances, each onboarding suppliers separately, no cross-instance identity. Native duplicate-detection is intra-instance only. The same real-world supplier ends up as 3 vendor records with 3 independently-set tax profiles — "no model fixes that" because a better invoice-reader still looks up whichever record the invoice happens to be coded against.

**"Nothing leaves our tenant," defined precisely:** data stays in the customer-owned resource/region, never used for training, never visible to the model provider, never transits the public internet. Azure OpenAI, private-endpoint-only, in Northgate's own subscription — checkable, not just a slide claim (CAIQ specifically probes this).

**Contingency pricing is a standard model in VAT reclaim**, not a novelty (VAT IT, Ryan, Taxback International all run it as their primary model) — why it's viable more broadly than a narrow carve-out.

## Requirements, condensed (full list: `requirements.md`)

**Non-negotiable, verbatim from the brief:** 2 engineers + PM, 8 weeks · 11-week security review starts at signing · no data leaves tenant · SAP read-only, no writes, any version · 3 SAP instances, not consolidating · year-end close is fixed · Head of Tax Risk has veto.

**Architecture:** extract → determine → recommend, never write-back. All 4 data sources (SAP, tax engine, mailbox, spreadsheets) held to the same tenant-bound posture, not just SAP. Azure OpenAI, private-endpoint, in Northgate's own subscription — billed to Northgate directly, not part of Ampliwork's fee.

**Data model:** jurisdiction, not hub, is the rules boundary. Supplier ≠ vendor master record — an entity-resolution layer connects them. Reclaim-window rule needs a *type* (rolling-years vs. return-deadline-bound), not just a number. Transaction is the atomic unit of record; batch is a UI layer only.

**Workflow:** a human reviews and approves every claim; the system never files. Queue ordered by urgency, not confidence alone. Precision on auto-processed determinations, recall on routing. Confidence threshold tightens as accuracy is demonstrated. One pipeline serves both the backlog and the ongoing stream.

**Explicitly out of scope:** automated supplier outreach, full China fapiao support, consolidating the 3 SAP instances.

**Roadmap:** EMEA (Rotterdam) first, then India specifically. Cash first (Phase 1); headcount redeployment trails as a Phase 2+ effect. Working-capital number reported as a burndown, not a static estimate. Pricing: fixed-fee + narrow contingency in Phase 1, expanding once 3 conditions are proven — human-in-the-loop control, tracked metrics, below-baseline error cost.

## Prototype verification status

8 scenarios in `prototype/output/example_determination_sheet.csv`:
- **Real, live Gemini output:** INV-1001, INV-1004
- **Blind-test verified** (fresh Claude agent, zero project context, exact generated prompt — confirms the prompt/reasoning design, not Gemini specifically): INV-1005, INV-1006, INV-1007
- **Fully deterministic, no LLM call:** INV-1002, INV-1003, INV-1008 (entity-conflict / compliance checks are plain code, by design)

If quota allows, get a real Gemini run on the blind-tested rows before presenting — the blind test is strong evidence, not a substitute.

## Key decisions and why
- **Azure, not a 3-way hyperscaler menu:** the SAP/BTP-Azure pairing convention, plus "tenant" being Microsoft's specific term for this concept.
- **Contingency pricing widened, not narrowed:** the incentive-conflict concern assumed unchecked AI output — it doesn't apply once the reviewer is Northgate's own risk-owning team, with zero contingency stake.
- **What the VP is wrong about:** she treats "coding" as separable data entry — it isn't; the tax code assigned during coding *is* the recoverability determination. The EMEA manager's own words confirm it ("coding is not the hard part").
- **Regional spreadsheets become a governed knowledge base**, curated rather than imported wholesale. An analyst's override becomes a candidate entry, approved by the hub tax manager before it affects auto-processed determinations — the concrete mechanism behind "confidence tightens over time."
