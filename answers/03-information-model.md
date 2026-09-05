# Information model (Part 1.3)

Status: not started. See `OUTLINE.md`, "Step: information model." Needs the tax + SAP domain briefings first, plus `case-facts.md` §5 (evidence document → entity mapping table, ready to use directly) and §4 (per-hub jurisdiction research).

## Key design decision: jurisdiction, not hub, is the rules boundary
The 3 regional hubs (Chicago/Rotterdam/Singapore) are a staffing and org construct — the brief never says they're a rules boundary, and they aren't one: EMEA alone spans France (~2yr reclaim window) and Netherlands (~5yr), and APAC likely spans similarly divergent regimes (see `case-facts.md` §4 for the per-hub minimum research). **Jurisdiction must be its own first-class entity, parameterized per country** (reclaim window, invoice-field requirements, filing frequency), looked up per transaction by that transaction's actual jurisdiction — not by which hub happens to staff the work. Hub stays a real, separate entity for routing/staffing, but must not be conflated with the rules boundary.

**Concrete "what breaks if you get this wrong":** if reclaim window were modeled per-hub instead of per-jurisdiction, the system would treat a Netherlands transaction (5yr window) as expired at whatever the coarser EMEA minimum turned out to be — actively abandoning money that was still legally recoverable. Flattening 30 countries to 3 hub-buckets repeats the exact mistake the brief warns against, just one level coarser than flattening to a single global constant.

## Summary (for the deck)
Legal entity, jurisdiction, supplier, transaction, invoice, recoverability determination, filing period, reclaim — what each means in Northgate's world, and how they relate. What's deliberately left out of v1, and what breaks if the model is wrong.

## Full entity detail (appendix material)
Attribute-level detail per entity, backed by the SAP/tax domain research where available; anything not settled by research gets resolved as an assumed customer clarification, tagged in `claims.md`.
