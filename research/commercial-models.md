# Commercial models already in this space — fast pass

Covers: what tax-recovery specialists and tax-tech vendors actually charge today. Feeds the Part 1 phasing/pricing logic and the Part 2 productization pricing.

---

## 1. Contingency-fee models (VAT/GST reclaim specialists)

This is the dominant model in the specific niche of cross-border VAT/GST reclaim. Firms recover money the client wasn't otherwise going to get, and take a cut of what lands.

**Named firms confirmed to use contingency pricing:**
- **VAT IT (vatit.com)** — global VAT reclaim specialist, claims €240M+ recovered for clients in the past year across 49+ countries. Publicly confirms "no upfront cost, no fee unless money is recovered," fee is "a percentage of what lands back in your account." **Exact percentage not published** — quoted per-client.
- **Taxback International (now trading as Fintua)** — same contingency structure, publicly confirmed via SAP Concur co-branded materials, no published rate.
- **Ryan, LLC** — large tax recovery/consulting firm (also acquired Avalara's sales-and-use-tax recovery business line in 2023, consolidating the space). States it offers **hourly, fixed, or contingency fee** options depending on engagement — contingency isn't the only model even at this tier. No published rate.

**Reference range from the adjacent, better-documented AP recovery-audit industry** (PRGX, apexanalytix, Strategic Audit Solutions — same "find money that was going to be lost" economics, well-documented because these firms publish buyer-education content):
- Typical contingency range: **10–40% of recovered amount**, most commonly cited as **20–30%** for standard AP recovery audits.
- PRGX specifically offers **10–40%** contingency, "no win no fee," or a fixed-fee-plus-lower-commission hybrid that shifts some risk back to the buyer for a better rate.
- Industry rule of thumb cited by apexanalytix: recovery audits typically find **~$1M per $1B of supplier spend** — useful as a sanity-check ratio, not a fee rate.
- Adjacent analog: **R&D tax credit studies** (a different tax specialty but same "we only get paid if we find you money" logic) are commonly priced at **15–25% of the credit recovered**, or a flat $10K–$50K+ fee for mid-market engagements — this is the clearest publicly-stated percentage band found across the research and a reasonable proxy for what a sophisticated buyer would consider "market" for contingency tax recovery work generally.

**Why exact VAT-specific percentages are hard to find:** none of the three major reclaim specialists (VAT IT, Taxback/Fintua, Ryan) publish a rate card — it's negotiated per client based on recovery complexity, jurisdiction mix, and volume, consistent with how enterprise B2B services in general withhold pricing until a sales conversation. This is a **pattern**, not a gap in the research — treat "quote-based, undisclosed %" as itself a finding.

## 2. Tax-tech vendor pricing (engines / platforms)

None of Vertex, Thomson Reuters ONESOURCE, Avalara, or Sovos publish pricing. All require a sales call; all price off a similar set of variables: transaction volume, number of jurisdictions/entities, modules selected, and support tier. Rough bands assembled from third-party pricing-intelligence sites (Vendr, Zamp, Galvix, TaxCloud — buyer-side firms that aggregate what customers report paying):

| Vendor | Model | Rough annual range |
|---|---|---|
| **Vertex** | Base platform subscription + transaction-volume tiers (Vertex Cloud/O Series); heavy professional-services layer for ERP integration | Mid-market (10K–50K txns/mo): $40K–$100K platform; enterprise (100K+ txns/mo): $150K–$400K. First-year TCO incl. implementation: $50K–$200K mid-market, $500K+ large enterprise |
| **Thomson Reuters ONESOURCE** | Modular subscription — pay only for modules used (Indirect Tax, Provision, etc.); scales with users/entities | Not disclosed in ranges; consistently reported as custom-quoted |
| **Avalara (AvaTax)** | Tiered subscription by monthly transaction volume (0–500 / 501–2,500 / 2,501–10,000 / custom above that); overage billed at 2–3x contracted per-transaction rate | Publishes zero pricing; entry tiers exist but scale to custom quotes fast |
| **Sovos** | Quote-based, scoped by transaction volume, jurisdiction count, modules, deployment complexity; multi-year contracts common | $15K–$250K+/year typical; $500K+ for multi-workstream enterprise deployments |

**Pattern across all four:** none is a pure per-transaction meter at the price point that matters — all converge on **platform subscription + implementation services**, with transaction volume as a tier-setting input rather than a line-item charge. This is the closer analog to Northgate's shape (an enterprise deployment against SAP, not a pay-per-invoice utility).

## 3. Enterprise AI / consulting engagement pricing (closest shape-match to the Northgate proposal)

This is the best analog for **how to structure**, not what to charge — the case study needs *logic*, not a number.

- **Fixed-fee scoped build phase**, sized to weeks not months: reported ranges for a 4–8 week single-use-case AI proof-of-concept/MVP run **$20K–$50K** at the small end up to **$50K–$250K** for a fuller pilot with real users in a controlled environment. An 8-week two-engineers-plus-PM build (Northgate's actual constraint) sits toward the lower-to-mid part of that band by effort, but enterprise/Big-Four-adjacent positioning and the security-review overhead here would push it up.
- **Retainer/managed-service phase after the pilot**: commonly $2K–$30K/month depending on depth — light advisory retainers ($2K–$5K/mo) vs. embedded weekly engagement with project oversight ($5K–$15K/mo) vs. full-service ($15K+/mo).
- **Tax-specific advisory retainers** (closer peer group): **$1,500–$7,500/quarter** for lighter tax advisory access, up to **$1,500–$15,000/month** for ongoing advisory engagement — useful as the retainer-band analog once Northgate's engagement moves from build to steady-state.
- **General pattern**: fixed-fee for the defined, time-boxed build (cost certainty, incentive-aligned for the vendor to deliver fast); then a recurring retainer or subscription once the thing is running, priced by depth of ongoing involvement rather than a meter on usage.

## 4. What this means for the two Northgate pricing questions (logic only, no invented number)

**(a) Pricing the 8-week-build-then-phased engagement:**
The tax-tech vendor pattern (platform/subscription + implementation) and the AI-consulting pattern (fixed-fee build + retainer) converge on the same shape: **fixed fee for the 8-week build** (bounded scope, bounded team, client bears delivery risk on nothing because it's capped), **converting to a retainer or phased SOW once the security review clears and the system starts touching real filings**. A contingency/gain-share component (a cut of *recovered* VAT/GST once the system is live and producing recoverable determinations, in the 10–25% range the recovery-audit and R&D-credit comps support) is a legitimate stretch option for the value case the VP wants "by year-end close" — but it only make sense layered on top of a fixed build fee, not replacing it, since the 8-week build produces no recoveries by itself (nothing is live and audited yet within 8 weeks — the veto-holder hasn't signed off).

**(b) Pricing if productized and sold repeatedly:**
The vendor comps (Vertex/Sovos/ONESOURCE) show the market ceiling for "AI reads invoices, decides tax treatment" as a **platform subscription tiered by transaction/entity volume, plus an implementation fee** — this is what a repeatable SaaS-shaped version of Northgate's tool would converge toward once sold to multiple multinationals. The contingency model (VAT IT et al.) is the alternative path if the product is positioned as a recovery service rather than software.

**Superseded — revised recommendation (see `claims.md`, "Pricing, revised," and `answers/05-roadmap-pricing.md`):** an earlier pass here argued contingency conflicts with "Head of Tax Risk holds the veto," on the reasoning that a contingency vendor has an incentive to overclaim recoverability, and recommended platform/subscription pricing as the safer default with contingency named only as an alternative to argue against. That reasoning assumed the AI's output goes unchecked into a filing. **It doesn't** — Northgate's own risk-owning team (the Head of Tax Risk's function) is the human-in-the-loop reviewer with zero contingency stake, which neutralizes the incentive conflict once paired with continuously tracked precision/recall metrics and a demonstrated below-baseline error cost. The current, correct recommendation is a **phased contingency-expansion model**: Phase 1 runs fixed-fee/retainer plus a narrow contingency slice on the urgent-recoverables bucket only; Phase 2+ expands contingency to the full ongoing recovered-$, conditional on those three conditions being proven in Phase 1. This is closer to the VAT-reclaim norm above (contingency as primary model, not a hedge) than the platform-subscription framing this section originally favored. Do not cite the "platform/subscription is more defensible" line above as current guidance — it was reversed after direct challenge.

---

## Claims for claims.md

| Claim | Status | Source | Notes |
|---|---|---|---|
| VAT IT, Taxback International/Fintua, and Ryan all use or offer contingency-fee ("no recovery, no fee") pricing for VAT/GST/tax recovery | ASSUMED | vatit.com, Fintua/Taxback marketing PDF via SAP Concur, ryan.com/services/recovery | Publicly stated on vendor sites; not independently verified beyond vendor's own marketing claims |
| None of VAT IT, Taxback/Fintua, or Ryan publish an exact contingency percentage | ASSUMED | Same as above — absence checked across multiple search passes | Absence of evidence, not confirmation no rate card exists anywhere non-public |
| VAT IT recovered €240M+ in foreign VAT for clients in the past year, operating in 49+ countries | ASSUMED | vatit.com company materials (via search summary) | Vendor's own claim, not third-party verified |
| Ryan acquired Avalara's sales-and-use-tax recovery business line in 2023 | ASSUMED | Businesswire press release, Sept 2023 | Standard press-release sourcing, not cross-checked against a second outlet |
| AP recovery-audit industry (PRGX, apexanalytix, Strategic Audit Solutions) typically charges 10–40% contingency, most commonly cited as 20–30% | ASSUMED | apexanalytix "How Much Does an Accounts Payable Recovery Audit Cost?" blog; PRGX AP Recovery Audit Services Guide | Vendor/industry-participant content, directionally consistent across two independent firms' public materials |
| R&D tax credit studies commonly priced at 15–25% of credit recovered, or $10K–$50K+ flat fee for mid-market | ASSUMED | Search-aggregated tax-advisory pricing content (consultfees.com and related) | Best publicly-stated specific percentage band found in the entire research pass; used here as the closest proxy for a VAT-reclaim-style contingency rate |
| Recovery audits typically find ~$1M per $1B of supplier spend | ASSUMED | apexanalytix blog content | Vendor-stated ratio, used as sanity-check only, not a fee |
| Vertex Cloud pricing: mid-market ~$40K–$100K/year platform fee (10K–50K txns/mo), enterprise $150K–$400K/year (100K+ txns/mo), first-year TCO $50K–$200K mid-market / $500K+ enterprise | ASSUMED | Aggregated from Vendr, Zamp, Galvix, TaxCloud third-party pricing-intelligence sites | These are buyer-reported/estimated figures, not Vertex's own published price list (Vertex does not publish pricing) |
| Thomson Reuters ONESOURCE uses modular, subscription-based pricing scaled by business size, users, and modules selected, with no public per-transaction rate | ASSUMED | Vendr, saasworthy.com, pricingnow.com aggregator content | No official Thomson Reuters price list found |
| Avalara AvaTax uses tiered subscription pricing by monthly transaction volume (0–500 / 501–2,500 / 2,501–10,000 / custom), with overage at 2–3x contracted rate, and publishes no pricing publicly | ASSUMED | Vendr, checkthat.ai, costbench.com aggregator content | Third-party aggregator estimates; Avalara itself confirmed (via same sources) to publish zero pricing |
| Sovos pricing typically $15K–$250K+/year, with multi-workstream enterprise deployments exceeding $500K/year, quote-based | ASSUMED | Vendr, taxcloud.com, erpresearch.com aggregator content | Same caveat — third-party estimates, not vendor-published figures |
| AI proof-of-concept/MVP builds typically run $20K–$50K (single use case, 4–8 weeks) up to $50K–$250K for a fuller pilot; retainers commonly $2K–$30K/month scaled by engagement depth | ASSUMED | Multiple 2026 AI-consulting pricing-guide blog posts (groovyweb.co, codewave.com, winder.ai, layer3labs.io, and others aggregated in search) | Broad, SEO-content-driven pricing-guide genre; treat as an order-of-magnitude reference band, not a benchmark study |
| Tax advisory retainers commonly run $1,500–$7,500/quarter (light) up to $1,500–$15,000/month (ongoing advisory access) | ASSUMED | Search-aggregated tax-advisory pricing content | Same genre caveat as above |
