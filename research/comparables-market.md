# Comparable / competitor products — fast pass

Status: researched (fast pass, not exhaustive). All figures dated to search date; company sites/press cited directly. Estimates are flagged inline.

---

## 1. VAT/GST reclaim specialist consultancies (contingency-fee model)

These firms recover indirect tax for clients on a success-fee basis — they don't sell software, they sell "we find the money." Closest thing to what Northgate's VP wants if you strip out the AI framing.

| Company | Founded | Scale | Model | Notes |
|---|---|---|---|---|
| **Taxback International** (rebranded **Fintua**, June 2025) | 1996, Kilkenny, Ireland | Not disclosed | VAT compliance + reclaim ("Recover" product) + payments (TBI Pay) | 25+ years in the space; moved from pure contingency-fee reclaim into a broader compliance/tech suite — same trajectory Northgate's VP is implicitly asking Ampliwork to shortcut. |
| **VAT IT** | 2000, South Africa/UK | 32 locations, 8,000+ clients, 100 countries, 1,000–5,000 employees | Reclaim (T&E, foreign VAT, AP), compliance, e-invoicing | Largest pure-play reclaim shop by headcount/footprint found. Core business is travel & expense VAT reclaim, not AP/indirect-tax-on-purchases at Northgate's scale — adjacent, not identical. |
| **Ryan, LLC** | Dallas, TX | 9,000+ clients, 40 countries | Full tax practice: recovery, consulting, advocacy, compliance, tech | Largest indirect + property tax practice in North America; claims **$4B in tax savings for clients "last year"** (their figure, not independently verified) using proprietary review software processing 1M+ transactions at a time. Ryan is the one name here already selling to Northgate's exact tier (Global 5000). |
| **Yonda Tax** | 2022, London | 350+ clients, €12M raised | Automated compliance (registration→filing→remittance) for VAT/GST/sales tax | Wrong segment for Northgate — built for eCommerce/SaaS/marketplace sellers managing *outbound* sales tax obligations, not a $14B industrial manufacturer's *inbound* AP recoverability problem. Included for completeness per brief but not a real comparable. |

**Read:** this category proves the "AI reads invoices, decides tax treatment" pitch isn't new — Ryan already runs proprietary software at Northgate's scale, and reclaim shops are already drifting into tech/compliance products. The contingency-fee shops compete on "we get paid only if we find money," which is a genuinely different buyer conversation than a software/services proposal.

---

## 2. Tax engines / ERP tax add-ons

These are the incumbent tax-determination layer sitting on top of ERPs like Northgate's three SAP instances — the systems Northgate's proposal has to *coexist with*, not replace.

| Company | Scale/coverage | Notes |
|---|---|---|
| **Vertex, Inc.** | Founded 1978, NASDAQ: VERX. 300M+ tax rules, 19,000+ jurisdictions, 195+ countries. Deep SAP/Oracle/NetSuite integration. | Launched Vertex O Series Tax Engine + Indirect Tax Accelerator on Oracle Marketplace (Mar 2026). Made a **$15M minority strategic investment in Kintsugi** (AI-native SMB sales-tax startup) — signals the incumbent is buying its way into AI rather than building it fast. |
| **Thomson Reuters ONESOURCE** (Indirect Tax Determination) | 205+ countries/territories, 460,000+ product/service tax codes, 60,000+ jurisdictions | Pre-built SAP integration; also ships "ONESOURCE Indirect Compliance AI" — TR is already layering AI onto the compliance side. |
| **Avalara** | 190+ countries | Launched **"Agentic Tax & Compliance"** (Sept 2025) with an "ALFA" framework — autonomous agents acting across SAP, Oracle, NetSuite, SYSPRO; shipped MCP servers for tool-level integration. This is the incumbent closest to "agent that acts on tax data inside your ERP," but positioned at determination/compliance/filing, not recoverability triage on messy AP invoices. |
| **Sovos** | Enterprise, multi-jurisdiction | Launched "Sovi," an AI layer on its Compliance Cloud — reported as narrower/less agentic than Avalara's push. |

**Read:** the tax-engine incumbents calculate tax correctly at the point of transaction (determination) — they are not built to retroactively audit a backlog of messy AP invoices for recoverability, and they don't touch reclaim filing. Northgate already has "a tax engine" per the brief; this proposal sits downstream of it, on exception/recovery, which is real white space relative to this category.

---

## 3. AI-native entrants — closest comparables to "AI reads invoices, determines tax treatment/recoverability"

This is the most load-bearing category for Part 2 of the brief. Fast-moving; funding rounds below are current as of the search date (Sept 2026) and should be treated as a snapshot.

| Company | Stage | What they do | Relevance to Northgate's ask |
|---|---|---|---|
| **Way2VAT** (merged with **RBCVAT**) | AI-native, patented tech + advisory arm | Combines AI-driven invoice/VAT-recoverability processing with hands-on VAT advisory consultancy | **Closest direct comparable found.** Explicitly pairs "patented AI technology" with deep VAT advisory — same pairing Northgate needs (AI triage + human judgment for the Head of Tax Risk). |
| **Fonoa** | $110M Series C, May 2026; acquired PwC's **Indirect Tax Edge** platform same round | Global indirect tax platform; clients include Uber, Netflix, Canva, Booking.com | Well-funded, credible enterprise traction, but publicly-known client base skews digital/platform companies, not industrial manufacturers with legacy multi-SAP estates. The PwC acquisition (buying an established Big 4 tax product) is the same "buy trust, build speed" pattern Ampliwork should expect competitors to use. |
| **Anrok** | $55M Series C, Oct 2025 | VAT/GST/sales tax across 100+ countries | Clients named (Anthropic, Notion, Cursor) are SaaS companies with simple, largely-digital transaction flows — not a fit for Northgate's problem shape (physical goods, customs paperwork, 14 languages, 3 SAP instances). Notable mainly as evidence of investor appetite in this space generally. |
| **Kintsugi** | Backed by $15M strategic investment from Vertex | AI-native sales-tax compliance for SMBs | Wrong tier (SMB) but worth naming because an incumbent (Vertex) chose to invest rather than build — a signal about how hard the AI-native rebuild is even for players with the domain data. |
| **AppZen** | Established AI-for-AP vendor | AI invoice audit/capture (100% of invoices, any format/language) + AP automation; explicitly markets **"automated compliance for FCPA, Sunshine Act, VAT recovery, and global regulations"**; claims $2.1B in identified customer savings | **Most relevant adjacent player.** Already does "AI reads invoice, flags tax/compliance issue" at enterprise AP scale — this is the nearest existing product to what Northgate's VP is describing, just framed as expense/AP audit rather than indirect-tax recoverability specifically. |
| **Vic.ai** | Established | Autonomous AP automation, invoice ingestion→classification→posting, 97–99% claimed extraction/coding accuracy, trained on 1B+ invoices | AP-automation-with-tax-angle per the brief's framing — does the "read and code the invoice" half, not the recoverability/reclaim-filing half. |
| **MindBridge AI** | Established | AI anomaly detection over 100% of financial transactions (not sampling) for internal audit/controls | Adjacent tooling — good for the "Head of Tax Risk" audit-exposure side of the problem (finding what's wrong), not the recovery side (finding what's owed back). Worth a namecheck if the pitch needs a credible AI-anomaly-detection analogue for the exception path. |

**Read for Part 2 ("is this a product?"):** nobody found is doing exactly "AI determines VAT/GST/sales-tax recoverability on messy multi-language AP invoices, sitting downstream of an existing tax engine, across acquired/fragmented ERP estates" as a named, funded product. The closest is Way2VAT (AI + advisory pairing) and AppZen (AI invoice reading with a VAT-recovery compliance angle, but framed as expense audit). This is real white space, but it's a crowded, well-capitalized adjacent space (Fonoa $110M, Anrok $55M, Avalara's agentic push, Vertex buying into Kintsugi) — any productization pitch has to explain why Ampliwork's version beats a well-funded incumbent or startup bolting recoverability onto what they already have, not just "no one does this."

---

## 4. TAM-proxy: how many multinationals sit in Northgate's tier

**Method:** Northgate is ~$14B revenue, 30 countries, 38,000 employees, ~120-person tax function (24 in indirect tax). The cleanest available real anchor is a public-company revenue ranking, since no published source directly counts "multinationals with an in-house indirect-tax function of dozens of people."

**Step 1 — revenue-band count (real data, not estimated):**
Source: [CompaniesMarketCap.com — Companies ranked by revenue](https://companiesmarketcap.com/largest-companies-by-revenue/), TTM revenue, pulled Sept 2026. The site tracks **11,258 public companies globally** with $65.02T in combined TTM revenue.

Pulling specific rank pages to bracket $14B revenue:
- Rank 801–900: revenue $16.47B (Ambev) down to $14.78B (Xcel Energy)
- Rank 901–1000: revenue $14.76B (CNA Financial) down to $13.17B (Jacobs Engineering)

So **companies with revenue right around $14B sit at roughly rank #850–950** among public companies worldwide — i.e., **there are roughly 850–950 publicly listed companies globally with revenue at or above Northgate's ~$14B level.**

**Step 2 — apply Northgate-shape filters (this part is estimate, reasoning shown):**
Not every ~$14B+ company looks like Northgate. Filter down:
- **Multinational footprint (operations in ~20-30+ countries, not a domestic giant):** a meaningful share of $10-20B-revenue companies are regionally concentrated (US regional utilities, US regional insurers/banks — both Xcel Energy and CNA Financial above are exactly this type). **Estimate: roughly 40-55% of this revenue band are true multinationals with cross-border AP/VAT exposure at Northgate's complexity** (industrial manufacturers, consumer goods, pharma, tech hardware, logistics — sectors that actually move physical goods/services across many VAT/GST jurisdictions). This is a judgment call, not sourced — flagged as the weakest link in the arithmetic.
- **Private companies excluded from this count:** CompaniesMarketCap tracks public companies only. Large private multinationals (some family-owned industrials, PE-owned platforms) exist in this tier too but are invisible to this method — meaning the true count is **an undercount**, not an overcount.
- **In-house indirect-tax function of meaningful size:** per KPMG's "Benchmarking Indirect Tax in a data-driven era" survey, **over 65% of respondent organizations carry $5B+ in annual revenue or turnover** — i.e., the survey population KPMG itself benchmarks against is already concentrated in Northgate's tier and above, corroborating that companies at this revenue level routinely run dedicated in-house indirect-tax functions (not outsourced entirely). This doesn't give a headcount-by-revenue table (not found in the fast pass), but supports the assumption that "$14B-revenue multinational → has an in-house indirect tax team worth selling to" is a safe default, not a stretch.

**Resulting estimate:** roughly **350-550 public multinationals worldwide** sit in Northgate's tier (public, $14B+ revenue, genuinely cross-border/physical-goods-and-services operations, likely in-house indirect tax function) — the midpoint of ~850-950 total companies in the revenue band times the ~40-55% multinational-shape filter. Add an unknown-but-nonzero number of large private multinationals on top (undercounted by this method). **This is the number to defend in the room: "a few hundred public companies, plus an unquantified handful of large private ones, not thousands."**

This is deliberately a narrower, more defensible number than "every Fortune Global 500 company" — Forbes Global 2000's cutoff is $6.2B in sales for 2026 (per Forbes' own published methodology), which is far too low a bar and would sweep in companies much smaller and simpler than Northgate.

---

## Claims for claims.md

| Claim | Status | Source | Notes |
|---|---|---|---|
| Taxback International (rebranded Fintua, June 2025) is a 25+ year VAT compliance/reclaim/tech firm founded 1996 in Kilkenny, Ireland | ASSUMED | https://taxbackinternational.com/vatconnect/ , https://uk.linkedin.com/company/taxbackinternational | Company self-description via web search; not cross-checked against a filing. |
| VAT IT: founded 2000, 32 locations, 8,000+ clients, 100 countries, 1,000-5,000 employees | ASSUMED | https://vatit.com/our-company/ , ZoomInfo | Employee count range is ZoomInfo's estimate band, not company-disclosed. |
| Ryan, LLC serves 9,000+ clients in 40 countries and claims $4B in client tax savings "last year" | ASSUMED | https://ryan.com/services/recovery/ , https://ryan.com/services/ | "$4B in tax savings" is Ryan's own marketing claim, not independently audited. |
| Yonda Tax: founded 2022, London, 350+ clients, raised €12M first institutional round | ASSUMED | https://www.yondatax.com/about , Crunchbase | Wrong buyer segment for Northgate (eCommerce/SaaS sellers) — included per brief's named list, not a functional comparable. |
| Vertex, Inc. founded 1978, covers 195+ countries/19,000+ jurisdictions, made $15M minority investment in Kintsugi | ASSUMED | https://www.vertexinc.com/ , https://seekingalpha.com/pr/20084569-vertex-announces-strategic-investment-in-ai-tax-compliance-startup-kintsugi | Investment amount from press release language surfaced via search; not opened as primary source. |
| Thomson Reuters ONESOURCE covers 205+ countries, 460,000+ product/service codes, 60,000+ jurisdictions; has an "Indirect Compliance AI" product | ASSUMED | https://tax.thomsonreuters.com/en/products/onesource-determination , https://tax.thomsonreuters.com/en/products/onesource-indirect-compliance-ai | Vendor-published figures. |
| Avalara launched "Agentic Tax & Compliance" (ALFA framework, MCP servers) in Sept 2025 across SAP/Oracle/NetSuite/SYSPRO | ASSUMED | Surfaced via search (dmihaylov.com AI TaxTech Map), https://www.avalara.com/us/en/products/ai-compliance.html | Not opened directly; secondary summary of Avalara's own announcement. |
| Way2VAT combined with RBCVAT to pair patented AI VAT-recoverability tech with VAT advisory consultancy | ASSUMED | https://www.cbinsights.com/company/way2vat and related search summary | This is the closest direct comparable found to Northgate's "AI + human judgment" ask — worth verifying directly (visit way2vat.com) before citing in the actual pitch deck. |
| Fonoa raised $110M Series C (May 2026) and acquired PwC's Indirect Tax Edge platform in the same round; clients include Uber, Netflix, Canva, Booking.com | ASSUMED | Surfaced via search summary of funding/press coverage | Not opened directly; verify amount and date before quoting in the deck. |
| Anrok raised $55M Series C (Oct 2025); clients include Anthropic, Notion, Cursor | ASSUMED | Surfaced via search summary | Same caveat — verify before quoting; client list places Anrok in SaaS, not Northgate's industrial-manufacturer segment. |
| AppZen offers "automated compliance for FCPA, Sunshine Act, VAT recovery, and global regulations" and claims $2.1B in identified customer savings | ASSUMED | https://www.appzen.com/ , https://www.appzen.com/ai-for-expense-audit | Vendor's own claim; this is the single most directly relevant "AI reads invoice → tax/compliance angle" product found in the fast pass. |
| Vic.ai claims 97-99% invoice extraction/coding accuracy, trained on 1B+ invoices | ASSUMED | https://www.vic.ai/how-it-works | Vendor-published figure. |
| MindBridge AI analyzes 100% of financial transactions (not sampling) for anomaly/risk detection | ASSUMED | https://www.mindbridge.ai/technology/ | Vendor-published figure. |
| CompaniesMarketCap.com tracks 11,258 public companies globally, $65.02T combined TTM revenue; companies with ~$14B TTM revenue rank roughly #850-950 (rank 801-900 spans $16.47B-$14.78B; rank 901-1000 spans $14.76B-$13.17B) | VERIFIED | https://companiesmarketcap.com/largest-companies-by-revenue/ (pulled directly, page 9 and page 10) | This is a live, continuously-updating public ranking — re-pull before the actual presentation date (Sept 10) since ranks shift with TTM updates. Public companies only; excludes private multinationals. |
| Forbes Global 2000 2026 minimum cutoff to make the list: $6.2B sales, $470M profit, $15.4B assets, $10.1B market value | ASSUMED | https://www.forbes.com/sites/andreamurphy/2026/06/04/how-we-crunch-the-numbers-the-2026-global-2000-methodology/ | Surfaced via search summary of Forbes' own methodology article; recommend opening directly before quoting the exact cutoff numbers in the deck. |
| KPMG's Indirect Tax Benchmarking Survey: over 65% of respondent organizations have $5B+ in annual revenue/turnover | ASSUMED | https://kpmg.com/xx/en/our-insights/operations/indirect-tax-benchmark-survey.html | Used as corroboration that $14B-revenue companies routinely run in-house indirect tax functions worth selling to; not a direct headcount-by-revenue source. |
| Estimate: ~350-550 public multinationals worldwide sit in Northgate's tier (public, $14B+ revenue, genuinely cross-border, likely in-house indirect tax function), understated because it excludes large private multinationals | ASSUMED (explicit estimate) | Derived: CompaniesMarketCap rank data (~850-950 companies at $14B+ revenue) × ~40-55% multinational-shape filter (author's judgment, not sourced) | This is the weakest link in the chain and the most likely thing a skeptic pushes on — the 40-55% filter is reasoned, not measured. Be ready to defend or narrow it live. |
