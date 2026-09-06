# Requirements

Everything the proposal has to satisfy, consolidated from the brief's constraints plus everything derived since. Updated as the plan develops — see `claims.md` for sourcing/status on any derived item.

## 1. Non-negotiable constraints (verbatim from the brief)
- 2 engineers + the PM, 8 weeks to something usable.
- Vendor security review, ~11 weeks, starts at signing.
- No data leaves Northgate's tenant.
- Read access to SAP. No writes, any version.
- 3 SAP instances, not being consolidated.
- Year-end close is a fixed date.
- Head of Tax Risk has a veto.

## 2. Architecture & security
- System design is "extract, determine, recommend" — never in-transaction write-back into SAP. See `answers/02-workflow-proposal.md`.
- The read-only, no-data-leaves-tenant posture applies to all four data sources named in the brief (3 SAP instances, tax engine, shared mailbox, regional spreadsheets) — not just SAP. Stated explicitly, not silently extended. See `case-facts.md` §6.
- The model/agent must run entirely within Northgate's own tenant boundary — no calls to a public multi-tenant model API. Resolved as a menu, not one answer: Azure OpenAI (if Azure), AWS Bedrock via PrivateLink (if AWS), or Vertex AI with VPC Service Controls (if Google Cloud, lower-confidence single-pass research) — all provisioned in Northgate's own subscription, private-endpoint-only, no-training-use terms. Self-hosting an open-weight model considered and declined (too much ops burden for 2 engineers/8 weeks); a public multi-tenant API declined (directly disqualified). See `answers/02-workflow-proposal.md`, point 8.
- "Determine externally" (workflow language) reconciled with "nothing leaves our tenant": the two describe different boundaries (SAP's application layer vs. Northgate's cloud tenant) and are fully compatible once stated explicitly on the assumptions slide.
- Which hyperscaler Northgate actually runs (Azure/AWS/GCP) is unverified — an open discovery question, not something to state as fact.
- Northgate's own cloud provider bills Northgate directly for the AI/compute consumption, since the resource is provisioned in Northgate's own subscription — this is separate from, and not included in, Ampliwork's engagement fee. Standard bring-your-own-cloud structure.
- "Nothing leaves our tenant" needs a precise, checkable definition for the pitch: data stays within the customer-owned resource and region, never used for training, never visible to the model provider, never transits the public internet — not a literal "zero third-party infrastructure" claim, which no hosted (or even most self-hosted) option actually achieves.
- Security review readiness: SIG and CAIQ are the standard questionnaires; CAIQ specifically probes tenancy/residency/encryption — the tenant-boundary architecture answer needs to hold up to that scrutiny, not just read well on a slide.
- Plain-language version of the tenant explanation (for the pitch itself, not just internal understanding) is in `case-facts.md` §10.
- Reclaim-window urgency ranking (11 researched jurisdictions, tightest first) is in `case-facts.md` §4 — Italy is the single most urgent, not France; India beats Singapore by ~8x.

## Explicit scope exclusions
- Automated supplier outreach (drafting/sending/tracking correction requests to suppliers) — out of scope.
- Full support for China's fapiao-based invoicing model — out of scope until scheduled as its own phase; not assumed to extend for free.
- Consolidation of the 3 SAP instances — out of scope; the solution operates across all 3 as-is.

## 3. Data model
- Jurisdiction, not hub, is the rules boundary — parameterized per country (reclaim window, invoice-field requirements, filing frequency, compliance-mechanism type). Hub stays a separate entity for staffing/routing only. See `answers/03-information-model.md`.
- Reclaim window needs a *rule-type* attribute (rolling N-years vs. return-deadline-bound), not just a number — Italy and India bind to an annual filing date, not a rolling count from the invoice.
- Time-to-expiration is computed per transaction (not per jurisdiction), using that transaction's own invoice date.
- Supplier (real-world entity) and vendor master record (per-instance SAP object) are distinct entities, connected by an entity-resolution layer — not 1:1.
- Invoice compliance status is jurisdiction-parameterized, with a compliance-mechanism-type attribute (field-checklist vs. government-clearance) — not a single global field list.
- The individual transaction/determination is the unit of record. Batch exists only in the review UI, never in the underlying data.

## 4. Workflow & model behavior
- A human reviews and approves every claim before filing — the system never files anything itself.
- Exception queue is urgency-weighted (time-to-expiration), not confidence-only.
- Model optimization target: precision for auto-processed determinations, recall for the routing decision. Accuracy is not the headline metric.
- Confidence threshold tightens over time as accuracy is demonstrated — not fixed from day one.
- One pipeline serves both the backlog (Phase 1) and the ongoing monthly stream (Phase 2+) — same engine, different input and dominant queue axis, not two builds.
- Invoice format-compliance checking is in scope, confirmed for Phase 1/EMEA. Automated supplier outreach (drafting/tracking correction requests) is explicitly out of scope.
- Current error-rate baseline (precision/recall of the human-only process today) must be measured empirically in Phase 1 — no external rate is computable from the brief's numbers.

## 5. Roadmap & business
- Pilot scope: EMEA (Rotterdam hub) first.
- Phase 2 sequencing is by jurisdiction (India next), not by hub — resolves the build-tractability vs. Cost-of-Delay conflict.
- Value sequencing: Phase 1 delivers cash (urgent recoverables captured, defensive), headcount redeployment is a trailing effect of Phase 2+ scope expansion.
- Working-capital number (the VP's "defend by year-end close" ask) is reported as a burndown — baseline plus recurring updates — not a single static estimate.
- Supplier-master-data-quality scale (EMEA manager's "a third" claim) is measured and reported back to her specifically, alongside the dollar burndown.
- Pricing: fixed-fee/retainer for the core engagement; contingency fee narrowly on the Phase 1 urgent-recoverables-captured bucket only.
- India's compliance-check extension (IRP/IRN clearance) and China's fapiao model are named as explicit later-phase risks, not assumed to generalize for free.

## 6. Prototype
- Must handle one awkward/messy input, not the clean case (recommended: duplicate-vendor-tax-profile, tied to EMEA's complaint).
- Must show the exception path — matters more than the happy path given who holds the veto.
- Low fidelity is fine, ugly is fine, working is not optional.
- Includes a batch view for review convenience, but the underlying record stays at the unit level.
- Synthetic invoice data anchored to real EU VAT rates (vatnode/eu-vat-rates-data, MIT licensed) — no open dataset fits as-is.

## 7. Deliverables (the case study submission itself)
- Deck: ≤8 slides (Part 1) + ≤4 slides (Part 2) = 12 max. Appendix optional, uncapped.
- Live prototype demo, ≤3 minutes, inside the 10-minute pitch.
- One-page pre-read email to the VP, written as an actual sendable note.
- Survive: one unscripted interruption during the pitch, plus a scripted fact-change curveball at the start of Q&A.
- "How we built this" appendix — tools/frameworks used, where AI helped, where it led astray.
- Talking points ready: one thing chosen not to build (automated supplier outreach, answered) and one thing that surprised us while building (pending the actual prototype build).
