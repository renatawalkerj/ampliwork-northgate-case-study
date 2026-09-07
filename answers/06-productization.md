# Is this a product? (Part 2)

Status: drafted. See `OUTLINE.md`, "Step: is this a product?" Draws on `research/comparables-market.md`, `research/commercial-models.md`, `research/assumed-customer-profile.md`, and the decisions already established in `case-facts.md`/the digest.

## 1. Recommendation, one sentence

**Yes, conditionally** — the core capability (jurisdiction-aware, confidence-scored tax-treatment determination sitting downstream of an existing tax engine, with an entity-resolution layer that reconciles fragmented multi-instance ERP data) is a real, differentiated wedge that nobody found is doing exactly this way (`research/comparables-market.md`) — but it's only a product if it's scoped to the specific niche below, not generalized to "any company with tax problems," and only if the vendor-security-review overhead (the single biggest cost this business carries) is treated as something to systematically shrink, not absorb per customer.

## 2. First niche — where to play, how to win

**Segment by size:** $10–20B+ revenue multinationals — large enough to run a dedicated in-house indirect-tax function of meaningful size (Northgate's 24 people is the reference point), small enough that they haven't already built proprietary tooling the way the largest tech/retail companies typically have.

**Segment by ERP landscape — this is the sharper, more defensible filter than size alone:** target companies with **fragmented, multi-instance ERP estates from M&A history** (Northgate's 3 SAP instances from acquisitions is the pattern, not an edge case for this segment). This is counterintuitive but load-bearing: a company with one clean ERP instance and tidy vendor master data has much less need for the entity-resolution capability that's the actual differentiator here — a generic AP-coding tool (Vic.ai, AppZen) serves them fine. The fragmentation *is* the addressable problem.

**Segment by tax exposure shape:** genuine multi-jurisdiction VAT/GST exposure (EU + APAC mix, ideally), not primarily US domestic sales/use tax — that's Avalara/Anrok's territory, a different rule shape (single-jurisdiction-per-transaction, no reclaim-window/invoice-clearance complexity) that doesn't need this product's core capability.

**Buying trigger, matching Northgate's own shape:** recent M&A activity creating ERP fragmentation, an internally disputed unrecovered-tax estimate (the width-of-the-range-itself-is-a-signal pattern), and/or a recent penalty event creating a risk-owner with real leverage to insist on the human-in-the-loop model.

**Who to refuse to sell to:**
- Companies without an existing in-house indirect-tax function of meaningful size — there's no risk-owner to pair with the confidence-based routing model, and the human-in-the-loop design this whole pitch depends on has nothing to attach to.
- Single-ERP, clean-master-data companies — no differentiated need; a generic AP tool is cheaper and sufficient.
- Companies whose tax exposure is primarily single-jurisdiction domestic sales tax — wrong rule shape, existing incumbents (Avalara, Anrok) already fit.

## 3. Market-sizing arithmetic (defensible under pushback, not precise)

**Starting point (real data):** ~350–550 public multinationals sit in Northgate's revenue tier with genuine cross-border exposure (`research/comparables-market.md`, built from a real CompaniesMarketCap.com revenue-rank pull × an explicitly-flagged 40–55% multinational-shape filter).

**Applying the niche filter (a further, unsourced judgment call, flagged as such):** of those, an estimated **30–50%** plausibly carry the specific M&A-driven ERP fragmentation this product targets — large industrials, consumer goods, and pharma companies with decades of acquisition history skew toward "yes"; younger, organically-grown multinationals skew toward "no." This is a judgment call, not a researched figure — **applying it gives a rough SAM of ~100–275 companies.**

**Per-account revenue potential (illustrative, heavily stacked):** using Northgate's own profile as the reference case — $8–30M/year in disputed unrecovered tax, a mature-state contingency take-rate in the 15–25% range (the low-to-middle of the 10–40% AP-recovery-audit-industry band in `research/commercial-models.md`, since a technology-enabled model should command a lower rate than a pure manual-audit consultancy) — implies a **mature-state per-account revenue range of roughly $1.2M–$7.5M/year**, once Phase 2+ contingency expansion is fully realized (`answers/05-roadmap-pricing.md`). Multiplying by the SAM above gives a **theoretical ceiling in the low hundreds of millions to low billions of dollars in annual recurring revenue** — not a realistic near-term number, and not meant as one.

**The honest caveat, stated plainly because it matters for section 5:** this is a ceiling at full penetration, and full penetration is not realistic on this business's actual sales motion — each account carries an ~11-week vendor security review (`research/security-review-norms.md`) and a genuinely consultative, trust-building sales cycle. **The real constraint on revenue isn't market size, it's sales/onboarding velocity** — worth stating in the room before a skeptic gets there first.

## 4. Packaging/pricing logic — how a pilot converts into recurring revenue

**The mechanism is already built into the pricing decision, not a separate upsell motion.** Phase 1 (fixed-fee/retainer + narrow contingency on the urgent-recoverables bucket) → Phase 2+ (contingency expands to the full ongoing recovered-$) is conditioned on three *proven* conditions — human-in-the-loop control, tracked metrics, demonstrated below-baseline error cost (`answers/05-roadmap-pricing.md`). That structure **converts a pilot into a recurring, expanding relationship automatically as trust is earned**, rather than requiring a renegotiation event — a cleaner product narrative than "we'll ask for more once you like us."

**For productization beyond Northgate specifically:** the natural expansion unit mirrors how the tax-engine incumbents already price (`research/commercial-models.md`) — **jurisdictions covered.** Each new jurisdiction is real, non-trivial engineering (a new reclaim-window rule type, a new invoice-compliance rule set, per `answers/03-information-model.md`), so a **per-jurisdiction platform fee, layered on top of the contingency structure once it matures**, is coherent with both research threads (the VAT-reclaim-specialist contingency norm and the tax-engine-incumbent platform-subscription norm) rather than forcing a choice between them.

## 5. What has to be true for this to be a product, not a series of custom builds

Testable hypotheses (*Bulletproof Problem Solving* framing) — this is the section a skeptic pushes hardest, so each one names what would falsify it:

- **H1 — the core determination logic must be reusable with configuration, not rebuilt per customer.** Jurisdiction rule packs (reclaim-window rule type, invoice-compliance requirements) are genuinely shared assets — the same France/Germany/Italy rules apply to *any* multinational operating there, not just Northgate. **Falsified if:** each new customer requires materially new core-logic work rather than new jurisdiction-pack configuration and a new ERP connector.
- **H2 — the "extract, determine, recommend, never write-back" architecture must generalize across ERPs, not just SAP.** The initial niche can reasonably scope to SAP-centric customers (where the pattern is proven here), but the architecture itself — not the SAP-specific integration — is what has to hold. **Falsified if:** the read-only/no-write-back pattern turns out to require fundamentally different handling per ERP vendor rather than a swappable connector layer.
- **H3 — the ~11-week vendor security review must become a compounding asset, not a flat per-customer tax.** A repeatable trust package (pre-built architecture documentation, SOC 2, reference architecture diagrams reusable across reviews) should make each subsequent review faster, not identically slow. **Falsified if:** review time doesn't meaningfully compress after the first several customers — in which case this stays a high-touch service business, not a scalable product, regardless of how good the technology is.
- **H4 — the SAM estimate in section 3 must hold up under real prospecting**, not just the illustrative arithmetic above. **Falsified if:** the real count of companies with both meaningful M&A-driven ERP fragmentation *and* a real risk-owner willing to adopt the human-in-the-loop model is a small fraction of the 100–275 estimate — in which case this is a strong service offering for a narrow set of accounts, not a venture-shaped product.
- **H5 — jurisdiction rule packs must actually amortize.** This is the strongest argument *for* productization: tax rules are jurisdiction-specific, not customer-specific, so build cost per jurisdiction is paid once and reused indefinitely. **Falsified if:** in practice, each customer's specific evidence/document format and ERP quirks dominate the engineering effort relative to the shared jurisdiction logic — in which case the product surface is thinner than it looks and most of the value is still bespoke integration work.

**Bottom line for the pitch:** H5 is the strongest yes, H3 is the biggest controllable risk, and H4 is the one no amount of internal reasoning can resolve — it needs real pipeline data, which is exactly why this section's numbers are framed as illustrative ceilings, not commitments.

## 6. Open consideration for further discussion — compute cost doesn't pool across customers, and that cuts both ways

Not one of the 5 questions above, but a real economic characteristic of this product shape, worth having a position on before it gets asked live.

**The single-tenant-per-customer deployment model (`answers/02-workflow-proposal.md`, point 9) means compute cost never gets centrally optimized by Ampliwork the way a normal SaaS vendor's would.** In a typical multi-tenant SaaS business, the vendor runs one shared service, controls the model/infrastructure choice centrally, and captures the benefit of any cost optimization (a cheaper model tier, better caching, batching) across the entire customer base at once. Here, each customer's deployment lives inside *their own* cloud subscription, billed directly to *them* (row 30a) — so:

- **Model-tier choice is effectively a per-customer configuration, not a platform-wide lever Ampliwork pulls once.** One customer might run a cheaper model tier if their volume/cost-sensitivity calls for it; another might run a more capable tier. That's a genuine flexibility selling point (no forced one-size-fits-all cost structure), but it also means Ampliwork can't unilaterally capture economies of scale on compute the way a pooled multi-tenant architecture would let it.
- **The Phase 2+ triage-classifier idea (`answers/02-workflow-proposal.md`) has the same shape.** A small model trained on accumulated, reviewed determination history would need to be trained *per customer*, since each tenant's knowledge base and eval history is isolated by design (no cross-customer pooling, per the tenant-isolation discussion) — it's a real cost optimization, but it doesn't compound across the customer base for free the way a shared-infrastructure SaaS vendor's model improvements would.
- **Net effect on the H3 "compounding trust package" argument:** the security-review overhead compounds in Ampliwork's favor (a reusable trust package, documented once, gets faster with each customer). Compute-cost optimization does not compound the same way — it has to be re-earned per customer. Worth being precise about which parts of this business actually get cheaper at scale and which don't, rather than assuming single-tenant SaaS behaves like multi-tenant SaaS on cost.
