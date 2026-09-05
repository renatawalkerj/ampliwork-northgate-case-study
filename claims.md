# Claims — Northgate Case Study

PIL rule: every claim starts ASSUMED. Moves to VERIFIED only with a source or Renata's sign-off. Nothing in the deck as fact until VERIFIED. Merged from `research/*.md` after Breakpoint A — see each file for full context.

## Tax domain

| Claim | Status | Source | Notes |
|---|---|---|---|
| EU input VAT invoice content rules are set by Directive 2006/112/EC Article 226, an exhaustive list of up to 15 fields; member states can't require fields beyond Art. 226/227/230 | VERIFIED | EU VAT Directive 2006/112/EC Art. 226; VATupdate.com explainer | Directly usable for the information-model slide |
| CJEU case law generally holds the right to deduct VAT shouldn't be denied purely for formal invoice defects if substantive conditions are provable — but tax authorities routinely deny administratively first | VERIFIED | VATupdate ECJ Art. 226 case-law roundup; VAT IT | Supports APAC analyst's quote as a real, documented mechanism |
| Reclaim/deduction windows vary materially by jurisdiction: UK ~4yr, Germany ~4yr, Netherlands ~5yr, France ~2yr; US state sales/use tax refunds typically 3-4yr | VERIFIED | Marosa VAT country manuals; VATupdate NL guide; Cyplom (France); TaxValet/Commenda/CDTFA (US) | Brief's "3-4 years" is a reasonable average, not literal everywhere — France is tighter, NL looser |
| **No published benchmark quantifies indirect-tax leakage as a % split across misclassification vs. dirty supplier master data vs. non-compliant invoices** — all three are independently documented as real by KPMG, Deloitte, and vendor sources, none ranked against the others | VERIFIED (as an absence) | KPMG 2026 Indirect Tax Benchmarking Survey; Deloitte digital-indirect-tax commentary; Oversight.com/Vertex on master-data duplication | **Key finding for `answers/01-diagnosis.md`** — can't be weighed externally, has to be diagnosed from Northgate's own data |
| Duplicate/fragmented supplier master records is a named, recognized driver of VAT leakage and audit risk | VERIFIED | Oversight.com "Five Ways Duplicates..."; Vertex "Master Data..." | Corroborates EMEA manager's quote |
| KPMG Global Tax Function Benchmarking: tax departments average ~17 FTEs at HQ + ~19 at other locations | VERIFIED (source exists), not indirect-tax-specific | KPMG "Inside global tax functions" | Total tax function, not indirect-tax-only or revenue-scaled — don't overstate as a Northgate comparator |
| "54% of eligible VAT is left unclaimed by businesses" | ASSUMED | Vanson Bourne research commissioned by SAP Concur | Vendor-commissioned, widely recirculated, no visible primary methodology — directional only |
| "4-10% of total eligible spend" is typically VAT-recoverable | ASSUMED | VAT-recovery vendor marketing (mobilexpense.com) | Vendor-sourced, unverified |
| >€5B foreign VAT unrecovered annually across original 25 EU states; 86.1% of large companies report difficulty; 53.5% don't file a claim | ASSUMED | Cited via Avalara, tracing to an unverified EU Commission-era study | Needs a primary-source check before saying this aloud |
| No external benchmark exists for indirect-tax leakage as % of AP spend, or indirect-tax FTE count, at Northgate's specific scale | VERIFIED (as an absence) | Searched KPMG/Deloitte/EY/PwC/Vertex/Sovos/Ryan public material | Northgate's own $8-30M range (~0.06-0.21% of revenue) has no outside anchor |

## SAP technical domain

| Claim | Status | Source | Notes |
|---|---|---|---|
| Tax engines (Vertex, ONESOURCE) integrate with SAP by intercepting the pricing/tax-determination step and writing the tax code back onto the document in real time | ASSUMED | Vertex SAP partner page; sapinsider | Standard documented pattern, high confidence, not verified against SAP's own architecture docs |
| One tax engine instance can serve multiple SAP company codes/instances without consolidation (per-company-code vendor class/entity config) | ASSUMED | Vertex SAP partner page; ONESOURCE Determination for Oracle Cloud page | Vendor-facing language, directionally correct |
| A strictly read-only SAP constraint rules out live in-transaction write-back, forcing a side-by-side "extract, determine externally, recommend" architecture | ASSUMED | Reasoned from SAP BTP side-by-side extensibility / communication-scenario model | No source documents this exact constraint combination — architectural inference |
| SAP vendor master data splits into general (client-wide) vs. company-code-specific data; independently onboarded company codes commonly recreate the same real-world supplier as separate vendor records with separate tax classifications | ASSUMED | SAP Community threads; Codasol vendor master data cleansing article | Consistent across independent sources; matches EMEA quote closely |
| SAP's native duplicate-vendor prevention relies on address/match-code fuzzy matching within one instance, no cross-instance identity concept | ASSUMED | SAP Community thread | Reasonable inference, not a formal SAP architecture statement |
| Vic.ai routes invoices below a confidence threshold to human review; exception queue shrinks over time as accuracy is proven | ASSUMED | Vic.ai FAQ/blog | Vendor's own claims, not independently benchmarked |
| AppZen assigns a per-transaction risk score, routes high-risk items to manual review with reasons/evidence attached | ASSUMED | AppZen blog posts | Vendor's own claims; 70-80% auto-approval / ~90% time-savings are AppZen marketing figures |
| ONESOURCE's public docs describe exception/variance/reconciliation workflows at the compliance-filing layer, but no public source documents a per-transaction ML confidence-routing mechanism inside ONESOURCE Determination itself | ASSUMED | Thomson Reuters ONESOURCE Determination features page | Absence of evidence, not evidence of absence |

## Vendor security review norms

| Claim | Status | Source | Notes |
|---|---|---|---|
| Enterprise vendor security reviews commonly take 8-12+ weeks for high-risk-tier vendors | ASSUMED | UpGuard, Trackforce, NHI Mgmt Group (triangulated) | Directionally well-supported, no single citable KPI. Northgate's 11 weeks sits inside this range |
| SIG and CAIQ are the two dominant vendor security questionnaires; SIG broader, CAIQ deeper on cloud tenancy/residency/encryption | VERIFIED | Bitsight, SecurityScorecard, Agency Insights comparisons | Multiple independent sources agree |
| A current SOC 2 report + recent (≤12mo) pen test are the two artifacts that most shorten a review | ASSUMED | License Logic and similar | Consistent across sources, no hard time-saved data |
| Sequential, siloed handoffs (security/legal/procurement) rather than parallel workstreams are a primary named cause of long review timelines | ASSUMED | Trackforce, UpGuard, NHI Mgmt Group | Repeated pattern, not precisely measured |
| Sandbox demos on synthetic/anonymized data are standard for letting prospects evaluate before security review clears production access | ASSUMED | PayProGlobal, License Logic | Well-established SaaS pattern, not tax/ERP-specific |
| Crawl-walk-run staged data-access expansion is current standard guidance for agentic AI rollouts | ASSUMED | Microsoft Security Blog, Zscaler, Writer | Multiple current (2026) sources converge |
| Shadow-mode operation (agent runs in parallel with humans, doesn't act, before being trusted with production decisions) is a named pattern for building trust in AI systems | ASSUMED | VentureBeat, Brightlume AI, ITSM Autopilot | Duration estimates (2-8 weeks) loosely sourced, approximate |
| Mapping sandbox → shadow-mode → staged-SAP-access onto Northgate's 8-week/11-week gap is original synthesis, not a reported real-world case | VERIFIED (as a statement about this doc's own reasoning) | N/A — original synthesis | Say so honestly if asked "is this a known playbook" |

## Commercial models

| Claim | Status | Source | Notes |
|---|---|---|---|
| VAT IT, Taxback International/Fintua, and Ryan all use or offer contingency-fee ("no recovery, no fee") pricing | ASSUMED | vatit.com, Fintua/Taxback marketing, ryan.com | Vendor's own marketing |
| None of VAT IT, Taxback/Fintua, or Ryan publish an exact contingency percentage | ASSUMED | Absence checked across multiple search passes | Absence of evidence, not confirmation no rate card exists anywhere |
| VAT IT recovered €240M+ for clients in the past year, operating in 49+ countries | ASSUMED | vatit.com company materials | Vendor's own claim |
| Ryan acquired Avalara's sales-and-use-tax recovery business line in 2023 | ASSUMED | Businesswire press release, Sept 2023 | Not cross-checked against a second outlet |
| AP recovery-audit industry (PRGX, apexanalytix) typically charges 10-40% contingency, most commonly 20-30% | ASSUMED | apexanalytix and PRGX public material | Directionally consistent across two independent firms |
| R&D tax credit studies commonly priced at 15-25% of credit recovered, or $10K-$50K+ flat fee mid-market | ASSUMED | Aggregated tax-advisory pricing content | Best publicly-stated specific % band found — closest proxy for a VAT-reclaim contingency rate |
| Recovery audits typically find ~$1M per $1B of supplier spend | ASSUMED | apexanalytix blog | Sanity-check ratio only, not a fee |
| Vertex Cloud: ~$40K-$100K/yr mid-market, $150K-$400K/yr enterprise; first-year TCO $50K-$200K mid-market / $500K+ enterprise | ASSUMED | Vendr, Zamp, Galvix, TaxCloud aggregators | Buyer-reported/estimated, not Vertex's own published price list |
| ONESOURCE: modular subscription pricing scaled by size/users/modules, no public per-transaction rate | ASSUMED | Vendr, saasworthy.com, pricingnow.com | No official price list found |
| Avalara AvaTax: tiered subscription by monthly volume, overage at 2-3x contracted rate, publishes no pricing | ASSUMED | Vendr, checkthat.ai, costbench.com | Third-party aggregator estimates |
| Sovos: typically $15K-$250K+/yr, multi-workstream enterprise >$500K/yr, quote-based | ASSUMED | Vendr, taxcloud.com, erpresearch.com | Third-party estimates |
| AI PoC/MVP builds typically $20K-$50K (single use case, 4-8 wks) up to $50K-$250K fuller pilot; retainers $2K-$30K/month | ASSUMED | Multiple 2026 AI-consulting pricing-guide blogs | Order-of-magnitude reference band, not a benchmark study |
| Tax advisory retainers commonly $1,500-$7,500/quarter (light) up to $1,500-$15,000/month (ongoing) | ASSUMED | Aggregated tax-advisory pricing content | Same genre caveat |

## Comparables / market

| Claim | Status | Source | Notes |
|---|---|---|---|
| Taxback International (rebranded Fintua, June 2025): 25+ yr VAT compliance/reclaim/tech firm, founded 1996 Kilkenny, Ireland | ASSUMED | taxbackinternational.com, LinkedIn | Self-description, not cross-checked against a filing |
| VAT IT: founded 2000, 32 locations, 8,000+ clients, 100 countries, 1,000-5,000 employees | ASSUMED | vatit.com, ZoomInfo | Employee range is ZoomInfo's estimate, not company-disclosed |
| Ryan, LLC: 9,000+ clients in 40 countries, claims $4B in client tax savings "last year" | ASSUMED | ryan.com | Ryan's own marketing claim, not audited |
| Yonda Tax: founded 2022, London, 350+ clients, raised €12M first round | ASSUMED | yondatax.com, Crunchbase | Wrong buyer segment (eCommerce/SaaS) — not a functional comparable to Northgate |
| Vertex Inc.: founded 1978, 195+ countries/19,000+ jurisdictions, $15M minority investment in Kintsugi | ASSUMED | vertexinc.com, SeekingAlpha PR | Investment amount from press-release language, not opened as primary source |
| Thomson Reuters ONESOURCE: 205+ countries, 460,000+ product/service codes, 60,000+ jurisdictions; has an "Indirect Compliance AI" product | ASSUMED | tax.thomsonreuters.com | Vendor-published figures |
| Avalara launched "Agentic Tax & Compliance" (ALFA framework) Sept 2025 across SAP/Oracle/NetSuite/SYSPRO | ASSUMED | Search summary; avalara.com | Not opened directly, secondary summary |
| **Way2VAT + RBCVAT pairs patented AI VAT-recoverability tech with VAT advisory consultancy** | ASSUMED | cbinsights.com and related search summary | **Closest direct comparable found to Northgate's "AI + human judgment" ask — verify directly at way2vat.com before the actual pitch** |
| Fonoa raised $110M Series C (May 2026), acquired PwC's Indirect Tax Edge platform same round; clients incl. Uber, Netflix, Canva, Booking.com | ASSUMED | Search summary of funding/press coverage | Not opened directly, verify before quoting |
| Anrok raised $55M Series C (Oct 2025); clients incl. Anthropic, Notion, Cursor | ASSUMED | Search summary | Places Anrok in SaaS, not Northgate's industrial segment |
| AppZen: "automated compliance for FCPA, Sunshine Act, VAT recovery, and global regulations," claims $2.1B in identified customer savings | ASSUMED | appzen.com | Most directly relevant "AI reads invoice → tax/compliance" product found |
| Vic.ai claims 97-99% invoice extraction/coding accuracy, trained on 1B+ invoices | ASSUMED | vic.ai | Vendor-published |
| MindBridge AI analyzes 100% of financial transactions (not sampling) for anomaly/risk detection | ASSUMED | mindbridge.ai | Vendor-published |
| CompaniesMarketCap.com: 11,258 public companies tracked, $65.02T combined TTM revenue; ~$14B TTM revenue ranks roughly #850-950 | VERIFIED | companiesmarketcap.com (pulled directly) | Live, continuously-updating ranking — re-pull before Sept 10. Public companies only, excludes private multinationals |
| Forbes Global 2000 (2026) minimum cutoff: $6.2B sales, $470M profit, $15.4B assets, $10.1B market value | ASSUMED | forbes.com methodology article | Surfaced via search summary, open directly before quoting exact numbers |
| KPMG Indirect Tax Benchmarking Survey: 65%+ of respondents have $5B+ annual revenue | ASSUMED | kpmg.com | Corroborates that $14B-revenue companies routinely run in-house indirect-tax functions; not a headcount source |
| **Estimate: ~350-550 public multinationals worldwide sit in Northgate's tier** (public, $14B+, cross-border, likely in-house indirect tax) | ASSUMED (explicit estimate) | Derived: CompaniesMarketCap rank data × ~40-55% multinational-shape filter (judgment, not sourced) | **Weakest link in the chain, most likely thing a skeptic pushes on** — be ready to defend or narrow the filter live |

## Prototype data

| Claim | Status | Source | Notes |
|---|---|---|---|
| SROIE/ICDAR2019 dataset is CC-BY-4.0 licensed | ASSUMED | github.com/zzzDavid/ICDAR-2019-SROIE | Needs check against official rrc.cvc.uab.es terms |
| CORD dataset is CC-BY-4.0 licensed | ASSUMED | github.com/clovaai/cord | Verify against repo's LICENSE file directly |
| FUNSD dataset is restricted to non-commercial/research use only | ASSUMED | guillaumejaume.github.io/FUNSD | High-confidence exclusion regardless |
| None of the surveyed open invoice/receipt datasets contain multinational VAT/GST-structured B2B invoices in multiple languages | ASSUMED | Fast-pass web search only | Search-based judgment, not exhaustive — say so if challenged |
| vatnode/eu-vat-rates-data is MIT licensed, covers 45 European jurisdictions, updated daily from the EC's TEDB | ASSUMED | github.com/vatnode/eu-vat-rates-data | Verify LICENSE file + spot-check a rate value before a live demo |
| No comparably-licensed open structured GST rate dataset exists for non-EU jurisdictions (e.g. Singapore) | ASSUMED | Web search only | Absence-of-evidence — worth a targeted follow-up if a non-EU jurisdiction ends up in the demo |
| "High-Quality Invoice Images for OCR" dataset is ODbL licensed | ASSUMED | huggingface.co/datasets/Voxel51/high-quality-invoice-images-for-ocr | Not planned for use |

## Consulting frameworks

| Claim | Status | Source | Notes |
|---|---|---|---|
| Bulletproof Problem Solving: logic tree types (component/factor, hypothesis, deductive, decision) and MECE discipline | VERIFIED — confirmed against book text | Ch. 3 "Problem Disaggregation and Prioritization" | Includes "what you have to believe" analysis via deductive trees |
| Bulletproof Problem Solving: problem statements should be outcomes-focused, specific/measurable, time-bound, solved at the highest organizational level possible | VERIFIED — confirmed against book text | Ch. 2 "Define the Problem" | Steel-company capital-plan case illustrates "solve one level up" |
| Playing to Win: five-part strategic choice cascade (winning aspiration, where to play, how to win, core capabilities, management systems), iterative and nested | VERIFIED — confirmed against book text | Chapter One "Strategy Is Choice" | Both copies of the PDF are identical, only one opened |
| McKinsey Way: MECE, initial hypothesis/issue tree method, the elevator test, "prewiring" before presentations | VERIFIED — confirmed against book text | epub full-text keyword search | No chapter headers in the extracted HTML — located by keyword, not TOC |
| Flawless Consulting Fieldbook: resistance is "the indirect expression of real concerns"; handle via capped good-faith responses then directly naming the behavior, managing content + emotions | VERIFIED — confirmed against book text | Ch. 8 "Dealing with Resistance" | |
| Flawless Consulting: sponsor vs. contact vs. resistance stakeholder taxonomy | ASSUMED — from general knowledge, not confirmed against this text | General knowledge of the original 1981/2011 *Flawless Consulting* | The physical book on hand (2024 Fieldbook & Companion) assumes familiarity with this taxonomy rather than defining it |
| Cialdini's Influence: six principles (reciprocation, commitment/consistency, social proof, liking, authority, scarcity) incl. rejection-then-retreat, foot-in-the-door, low-ball, pluralistic ignorance, psychological reactance | VERIFIED — confirmed against book text | Influence: The Psychology of Persuasion, Ch. 1-7 + Epilogue, read in full | This edition is the classic six-principle text (rev. 2006/2009) |
| Cialdini's Influence does not cover a seventh "Unity" principle | VERIFIED (fact about this specific text) | Full table of contents reviewed | Unity was added in the 2021 New and Expanded edition, not this copy — flag if asked to apply it |
| Switch: Rider/Elephant/Path model and its three levers (direct the Rider, motivate the Elephant, shape the Path), plus reinforcement mechanics | VERIFIED — confirmed against book text | Switch, extracted_text + career/org_knowledge_base/frameworks/20-24 | Read via an existing career-pipeline extraction, not re-parsed from the epub this session |
| Mapping Switch's sandbox/shadow-mode/staged-access roadmap onto "shaping the Path," and identity-based buy-in onto winning the Head of Tax Risk | VERIFIED (as this doc's own reasoning) | N/A — original synthesis on verified Switch content | The Switch mechanisms are from the book; the Northgate application is original reasoning |
| Never Split the Difference: tactical empathy, mirroring, labeling, the accusation audit, calibrated "how/what" questions, "That's right" vs. "you're right," "no" as the start of the real negotiation | ASSUMED — general knowledge, not book text | Cross-checked against multiple independent summaries via web search | Book not owned/purchased for the deadline — reconstruction, not extraction |
| The Challenger Sale: five rep profiles (Challenger = top performer in complex B2B; Relationship Builder disproportionately underperforms), Teach-Tailor-Take Control, commercial teaching/insight | ASSUMED — general knowledge, not book text | Cross-checked against multiple independent summaries via web search | Book not owned/purchased for the deadline — same reconstruction caveat |
