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
- The model/agent must run entirely within Northgate's own tenant boundary — no calls to a public multi-tenant model API. **Resolved and confirmed: Microsoft/Azure.** Azure OpenAI Service, provisioned in Northgate's own subscription, private-endpoint-only, no-training-use terms. AWS Bedrock kept as a one-line noted alternative, not a hedged parallel option. Self-hosting an open-weight model considered and declined (too much ops burden for 2 engineers/8 weeks); a public multi-tenant API declined (directly disqualified). See `answers/02-workflow-proposal.md`, point 8.
- "Determine externally" (workflow language) reconciled with "nothing leaves our tenant": the two describe different boundaries (SAP's application layer vs. Northgate's cloud tenant) and are fully compatible once stated explicitly on the assumptions slide.
- Hyperscaler confirmed as Azure for planning purposes (still ASSUMED in the PIL sense — nothing external verified it, it's a settled premise for this exercise, supported by two stacking signals: SAP/BTP-Azure pairing convention + "tenant" being Microsoft/Entra ID's specific term vs. AWS "Account" or GCP "Project").
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
- **Regional spreadsheets (4th data source) become a supported, versioned knowledge base — curated from existing content, not imported wholesale.** New entries come from a feedback loop: an analyst's override of a determination becomes a candidate entry, reviewed/approved by the hub tax manager before it can influence future auto-processed determinations. This is the concrete mechanism behind "confidence threshold tightens as accuracy improves" and the trust-building answer for the Head of Tax Risk — every accepted override becomes an auditable, reviewed record. Included in the prototype build, not deferred to a later phase. See `case-facts.md`, feature group 8.

## 5. Roadmap & business
- Pilot scope: EMEA (Rotterdam hub) first.
- Phase 2 sequencing is by jurisdiction (India next), not by hub — resolves the build-tractability vs. Cost-of-Delay conflict.
- Value sequencing: Phase 1 delivers cash (urgent recoverables captured, defensive), headcount redeployment is a trailing effect of Phase 2+ scope expansion.
- Working-capital number (the VP's "defend by year-end close" ask) is reported as a burndown — baseline plus recurring updates — not a single static estimate.
- Supplier-master-data-quality scale (EMEA manager's "a third" claim) is measured and reported back to her specifically, alongside the dollar burndown.
- **Measured error rate (false-positive rate on auto-processed determinations) reported on a recurring cycle, trended against the Phase 1 human-only baseline and against a modeled annualized cost-of-error line derived from the real $4M/year penalty figure.** This is the evidence for Phase 2+ pricing condition 3 ("demonstrated below-baseline error cost"), not a separate metric — the reporting mechanism that actually proves the trigger, not just asserts it. The $4M anchor is real; the modeled cost curve stacks one more illustrative assumption (average $ exposure per false positive, proxied by average invoice value) — state that distinction if asked how it's calculated. See `case-facts.md`, feature group 6 (FR11a).
- **Pricing, revised: phased contingency expansion.** Phase 1: fixed-fee/retainer for the build, contingency narrowly on the urgent-recoverables bucket. Phase 2+: contingency expands to the full ongoing recovered-$, pre-agreed at signing, conditional on Phase 1 proving (1) human-in-the-loop review sits with Northgate's own Head-of-Tax-Risk function, (2) precision/recall metrics tracked and reported continuously, (3) measured error-driven cost stays below the pre-engagement baseline. See `answers/05-roadmap-pricing.md`.
- India's compliance-check extension (IRP/IRN clearance) and China's fapiao model are named as explicit later-phase risks, not assumed to generalize for free.
- $4M penalty jurisdictions: left as stated in the brief — exactly "two jurisdictions," not named, not all 30. A bounded, comparatively mild exposure picture, not systemic.
- Switzerland/Turkey compliance-rule-set question: deferred as a follow-up, not blocking the current plan.

## 6. Prototype
- Must handle one awkward/messy input, not the clean case — flagship: duplicate-vendor-tax-profile (INV-1002), tied to EMEA's complaint. Built alongside 4 more: happy path, format-compliance failure, urgency-queue jump, and a genuine tax-judgment ambiguity. See `prototype/data/invoices.json`.
- Must show the exception path — matters more than the happy path given who holds the veto.
- Low fidelity is fine, ugly is fine, working is not optional.
- Includes a batch view for review convenience, but the underlying record stays at the unit level.
- Synthetic invoice data anchored to real EU VAT rates (vatnode/eu-vat-rates-data, MIT licensed) — no open dataset fits as-is.
- Eval framework defined before the build: ground-truth expected values baked into each synthetic invoice, scored against determination accuracy, confidence-tier accuracy, precision-on-auto-processed, recall-on-routing, entity-conflict detection, compliance-check accuracy, and time-to-expiration correctness. See `prototype/evals/eval-plan.md`.
- What improves iteration-to-iteration is prompt/instruction and confidence-threshold refinement against the eval set — not weight-level fine-tuning (no fine-tuning budget on Gemini's free tier, consistent with the same constraint already named for the production recommendation).
- **v1 build priority, revised: a CSV/sheet pipeline first, UI only if time remains.** Data ingestion → deterministic entity-conflict/compliance checks → RAG retrieval of approved knowledge-base entries → LLM determination → a flat sheet she opens directly. Matches how the analyst already works (spreadsheets) and demos the actual pitch (the LLM + the feedback loop), not UI chrome. See `prototype/src/`.

## 7. Deliverables (the case study submission itself)
- Deck: ≤8 slides (Part 1) + ≤4 slides (Part 2) = 12 max. Appendix optional, uncapped.
- Live prototype demo, ≤3 minutes, inside the 10-minute pitch.
- One-page pre-read email to the VP, written as an actual sendable note.
- Survive: one unscripted interruption during the pitch, plus a scripted fact-change curveball at the start of Q&A.
- "How we built this" appendix — tools/frameworks used, where AI helped, where it led astray.
- Talking points ready: one thing chosen not to build (automated supplier outreach, answered) and one thing that surprised us while building (pending the actual prototype build).
