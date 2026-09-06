# Information model (Part 1.3)

Status: not started. See `OUTLINE.md`, "Step: information model." Needs the tax + SAP domain briefings first, plus `case-facts.md` §5 (evidence document → entity mapping table, ready to use directly) and §4 (per-hub jurisdiction research).

## Key design decision: jurisdiction, not hub, is the rules boundary
The 3 regional hubs (Chicago/Rotterdam/Singapore) are a staffing and org construct — the brief never says they're a rules boundary, and they aren't one: EMEA alone spans France (~2yr reclaim window) and Netherlands (~5yr), and APAC likely spans similarly divergent regimes (see `case-facts.md` §4 for the per-hub minimum research). **Jurisdiction must be its own first-class entity, parameterized per country** (reclaim window, invoice-field requirements, filing frequency), looked up per transaction by that transaction's actual jurisdiction — not by which hub happens to staff the work. Hub stays a real, separate entity for routing/staffing, but must not be conflated with the rules boundary.

**Concrete "what breaks if you get this wrong":** if reclaim window were modeled per-hub instead of per-jurisdiction, the system would treat a Netherlands transaction (5yr window) as expired at whatever the coarser EMEA minimum turned out to be — actively abandoning money that was still legally recoverable. Flattening 30 countries to 3 hub-buckets repeats the exact mistake the brief warns against, just one level coarser than flattening to a single global constant.

**A second, sharper failure mode research surfaced:** reclaim window isn't even a flat N-years-from-invoice-date everywhere. Italy and India both bind the deadline to an *annual return filing date*, not a rolling count from the invoice — so the actual runway depends on when in the fiscal year the invoice lands (Italy: ~4-5 months for a December invoice vs. ~15-16 months for a January one; India similarly ~8 to ~20 months depending on FY timing). A model that stores "reclaim window = N years" per jurisdiction, even correctly per-jurisdiction, still gets Italy and India wrong — it needs the jurisdiction's *rule type* (rolling N-years vs. return-deadline-bound) as an attribute, not just a number. See `case-facts.md` §4.

**A derived attribute this all points to: time-to-expiration.** Every recoverability determination that's identified-but-not-yet-claimed should carry a computed "time remaining before this specific transaction's window closes" — not just the jurisdiction's rule, but that rule applied to this transaction's actual invoice date. This is the same idea as an AR-aging schedule (0-30/31-60/61-90 days), applied to unclaimed recoverable tax instead of unpaid invoices. Without it, a small amount three weeks from expiring and a large amount with years of runway look identical on a list — and the urgent one is the one that actually gets lost. This attribute is also what makes the workflow's exception queue urgency-aware, not just confidence-aware (see `answers/02-workflow-proposal.md`).

## Batch is a UI/UX layer, never the unit of record
Same principle as jurisdiction-not-hub, applied one level deeper: the atomic unit of the data model is the **individual transaction/determination**, never a batch. Batching exists only in the review UI — grouping similar transactions so a reviewer can bulk-approve efficiently — never in the underlying record. Reasons this has to hold, not just a style preference:
- **Audit trail:** an auditor needs to see one transaction's own evidence and determination, not "processed as part of a $2M batch." Aggregating away transaction identity would recreate the exact audit-exposure risk the Head of Tax Risk owns.
- **Time-to-expiration is inherently per-unit** (above) — each transaction has its own invoice date and therefore its own expiration date. Batching would average away the one thing the urgency-weighted queue depends on.
- **Exception routing is per-unit** — two transactions a reviewer sees grouped in one UI batch can have different confidence scores; one may auto-process while its neighbor needs review. The batch is a convenience for the human, not a shared fate for the data.

## Summary (for the deck)
Legal entity, jurisdiction, supplier, transaction, invoice, recoverability determination, filing period, reclaim — what each means in Northgate's world, and how they relate. What's deliberately left out of v1, and what breaks if the model is wrong.

## Full entity detail (appendix material)
Attribute-level detail per entity, backed by the SAP/tax domain research where available; anything not settled by research gets resolved as an assumed customer clarification, tagged in `claims.md`.
