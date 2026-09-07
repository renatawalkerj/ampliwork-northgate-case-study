# Case Facts & Assumptions — Northgate Industries

Feeds Phase 1 (diagnose, propose, model) directly. Three layers throughout: **What the brief says** (cited), **What we're assuming** (tagged, reasoning shown, mirrored in `claims.md`), **What research filled in** (linked to `research/*.md`).

## 1. Who does the tax function actually manage, and what does "right" mean

**What the brief says:** the team is responsible for VAT, GST, and sales & use tax "across every jurisdiction Northgate operates in" — all 30 countries, not just the 3 hub cities. Chicago, Rotterdam, and Singapore are where the 24 people are organized, not a scope limit. Confirmable from the brief's own quote attributions: "Regional tax manager, **EMEA**" and "Analyst, **APAC**" tell us Rotterdam = EMEA hub, Singapore = APAC hub, Chicago = Americas hub by elimination.

**Per transaction, three separate decisions**, straight from the brief: (1) was tax charged correctly, (2) is it recoverable, (3) where should it be reported. These aren't one lookup — see §7, this is the crux of the diagnosis.

**Volume, straight from the brief, previously not logged here:** "every month they work through hundreds of thousands of accounts payable transactions" — a real, verbatim number (not an estimate), and the anchor for any transaction-volume or per-invoice-value arithmetic (`research/assumed-customer-profile.md`).

**Wrong in one direction vs. the other, precisely:**
- Fail to identify/claim recoverable tax → **leaves cash on the table** (the $8–30M problem, §3)
- Incorrectly claim or misreport → **audit exposure and penalties** (the $4M problem, §3)

**Key insight, not stated directly in the brief but follows from combining §1 and §2:** the reclaim window (§2) is a safety net for the *first* kind of mistake — an under-claim can still be caught and fixed until the window closes. There is **no equivalent safety net for the second kind** — an over-claim or misreport is caught by auditors, on their timeline, at the company's expense, with no self-correction runway. This asymmetry is a sharper, more concrete justification for the Head of Tax Risk's "wrong matters more than slow" position than just calling her risk-averse — her risk genuinely has no safety net; the VP's does.

## 2. The two clocks (plus a third we found)

**What the brief says:** filing deadlines are monthly or quarterly depending on jurisdiction; separately, each jurisdiction has a reclaim window, "typically three to four years," after which the money is gone.

**What research confirmed (VERIFIED, see `claims.md`):** the "3–4 years" is a reasonable average but not one clock — UK ~4yr, Germany ~4yr, **Netherlands ~5yr**, **France ~2yr** (a real outlier), US states ~3–4yr, **Singapore 5yr** (confirmed directly from IRAS, closing a gap — Singapore was the one hub jurisdiction not yet checked). Singapore also has a genuine third clock the brief doesn't mention: if input tax is claimed before the supplier is paid, payment is due within 12 months or the claim must be repaid.

**What we're assuming:** per-jurisdiction filing frequency (monthly vs. quarterly, specifically) isn't given for any of the 30 countries, and we haven't researched it country by country — that level of enumeration isn't feasible or necessary for the pitch. ASSUMED: Northgate's high-volume hub jurisdictions are more likely on monthly filing given transaction volume, stated as a general pattern, not a per-country confirmed fact. This is thin enough that it shouldn't be quoted as specific in the room.

**What this means operationally:** monthly transaction volume creates a rolling decision cadence; the reclaim window is the outer deadline for catching missed recoverable amounts within that cadence — it's a grace period after a miss, not the moment of failure. A miss in month T can still be caught and corrected in month T+1, T+2, etc., right up until the window closes; only running out that grace period turns a miss into a permanent loss. There's no equivalent grace period on the over-claim side — which is exactly why phasing the rollout around proving correctness first (see the roadmap) matters more than proving speed first.

**The pairing this implies — reclaimable size needs to be paired with time-to-expiration, not tracked alone.** A recoverable-but-unclaimed amount three weeks from its jurisdiction's window closing and one with four years of runway look identical as dollar figures on a list; only the first one is actually at risk of being lost this cycle. This is the same concept as an AR-aging schedule, applied to unclaimed recoverable tax instead of unpaid invoices. It's now a first-class part of the design: `answers/03-information-model.md`'s time-to-expiration attribute, and `answers/02-workflow-proposal.md`'s urgency-weighted (not just confidence-weighted) exception queue.

**This also reframes rollout sequencing, not just the workflow.** If a hub's reclaim window is tight, unclaimed money there decays into permanent loss faster while the rollout is busy elsewhere — a Cost of Delay argument (Reinertsen; ASSUMED, general knowledge) for sequencing by *urgency*, not just build tractability. See `answers/05-roadmap-pricing.md` for where this conflicts with the tractability-based sequencing and how it's resolved (targeting India specifically as the phase-2 priority, not "all of APAC").

## 3. The money — $4M penalties, $8–30M unrecovered

**$4M in penalties/interest, last year, across two jurisdictions — the brief does not name them.** Recommendation: don't invent specific countries for the pitch. If the deck needs concreteness, name two illustrative jurisdictions (e.g. one EU country + the US) and flag it explicitly as illustrative, not a stated fact — inventing unstated specifics that could get challenged is a worse risk than leaving it as "two jurisdictions," which is what the brief actually says.

**$8–30M/year unrecovered is Northgate's own disputed internal estimate.** The brief is explicit that the width of the range is itself part of the problem — this is a diagnostic signal, not a data gap to apologize for.

**Can we tighten it externally? No — and we shouldn't pretend to.** Research found no benchmark for indirect-tax leakage as a % of AP spend at Northgate's specific scale (`research/tax-domain.md`). One rough cross-check, offered as a sanity check only, not a confirmation: AP-recovery-audit firms report recovering roughly $1M per $1B of supplier spend (ASSUMED, vendor-sourced ratio, `claims.md`). If Northgate's AP spend is ~40–60% of its $14B revenue (a common but unconfirmed ratio for an industrial manufacturer), that ratio implies **~$5.6–8.4M** — landing near the *low* end of Northgate's own $8–30M estimate. That's suggestive (the $30M end may be optimistic, or Northgate's multi-jurisdiction VAT complexity exceeds what a domestic-audit ratio captures) but built on two stacked assumptions — not something to state as fact in the room.

**Should narrowing this number be part of the plan? Yes — explicitly.** This is the strongest argument for the roadmap's diagnostic-first phase: the only credible way to turn $8–30M into a number the VP can defend by year-end close is to measure it from Northgate's own exception data, not from outside benchmarks. This should be stated plainly as Milestone 1's actual deliverable in `answers/05-roadmap-pricing.md`, not left implicit.

## 4. Jurisdictions

**Named directly:** only the 3 hub countries (US, Netherlands, Singapore) out of "30 countries." The other ~27 aren't enumerated anywhere in the brief.

**ASSUMED — a plausible 30-country footprint, split by hub.** The brief gives no country list. This is a constructed assumption for a $14B industrial manufacturer with real physical operations (factories/distribution, not a digital-only footprint), built to be representative, not a claim about the actual Northgate. Do not present this list as fact in the room — it exists so the jurisdiction analysis below has something concrete to sit on.

| Hub | Assumed countries (count) |
|---|---|
| **Americas — Chicago** | US, Canada, Mexico, Brazil, Argentina, Chile, Colombia (7) |
| **EMEA — Rotterdam** | Netherlands, UK, Germany, France, Italy, Spain, Belgium, Poland, Sweden, Switzerland, Austria, Czech Republic, Turkey, South Africa (14) |
| **APAC — Singapore** | Singapore, China, Japan, India, South Korea, Australia, Thailand, Vietnam, Indonesia (9) |
| **Total** | **30** |

**Reclaim windows confirmed for the 6 previously-researched countries (VERIFIED, §2):** UK ~4yr, Germany ~4yr, Netherlands ~5yr, France ~2yr, US states ~3–4yr, Singapore 5yr.

**The gap this fills: is there a tighter window per hub, beyond those 6?** The brief's own framing — "a window in which a reclaim can still be made... after which the money is simply gone" — implies the number that actually matters operationally for a hub is its *tightest* window, because that's the fastest point at which money becomes permanently unrecoverable. A hub-wide "5 years" story (Singapore) or "3–4 years" story (US) is misleading if one country in that hub's footprint has a materially shorter clock. Fast-pass research (not exhaustive — India, China, Canada, and Italy were checked as the most-likely-to-be-tight candidates per hub; not all 30 countries) found real, non-obvious minimums in two of the three hubs:

### Americas hub — real floor: Canada, ~2 years for large businesses, not the US's ~3–4yr

**Finding:** Canada's general GST/HST input tax credit (ITC) time limit is 4 years — but it drops to **2 years** for "large businesses" (annual taxable supplies over CAD $6 million) and listed financial institutions. A $14B multinational's Canadian entity would almost certainly exceed that $6M threshold.
**Source:** VERIFIED — Canada Revenue Agency (CRA) directly, "Input tax credits" (canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/calculate-prepare-report/input-tax-credit.html) — primary regulator source, same tier as the Singapore/IRAS citation in §2.
**What it means operationally:** the Americas hub's real floor is likely Canada's ~2yr, not the US's ~3–4yr the brief's average implies — a large-business Canadian claim has half the runway to self-correct that the US-anchored story suggests.

### EMEA hub — real floor: Italy, a return-deadline-bound window as short as ~4–5 months, not France's flat ~2yr

**Finding:** Italy's *current* rule (in effect until a scheduled 1 Jan 2027 reform) does not give a fixed number of years — it lets a business deduct input VAT only up to the filing deadline of the *annual VAT return for the year the deduction right arose* (that return is due ~30 April of the following year). Because the window's length depends on *when in the year* the invoice lands, an invoice from January gives ~15–16 months of runway, but an invoice from December gives only **~4–5 months**. From 2027 this extends to a flat 2 years, matching the France pattern — but that reform isn't in effect yet.
**Source:** VERIFIED (converging multiple tax-advisory sources, not one primary regulator citation — same sourcing tier used for UK/Germany/France in §2): vatcalc.com ("Italy VAT changes to deductions and penalties"), globalvatcompliance.com Italy VAT Guide 2025, eurofiscalis.com. Could not pull the exact DPR 633/72 Article 19 statutory text directly in this pass — flag if pushed on the legal citation itself.
**What it means operationally:** EMEA's real floor for a late-year invoice is tighter than France's already-tight ~2yr, and tighter in the worst case than APAC's India finding below — the France outlier isn't EMEA's actual floor, Italy's year-end timing risk is.

### APAC hub — real floor: India, ~8–20 months (Nov 30 cutoff), decisively beating Singapore's 5yr

**Finding:** India's GST input tax credit (ITC) cannot be claimed after **30 November following the end of the financial year** (India's FY runs April–March) the invoice belongs to, or the filing of that year's annual return, whichever is earlier. Because the clock runs to a fixed calendar date regardless of invoice date, an invoice from early in the FY (April) gets ~19–20 months of runway; an invoice from late in the FY (March) gets only **~8 months**.
**Source:** VERIFIED — primary regulator source. CBIC (India's Central Board of Indirect Taxes and Customs) Circular No. 237/31/2024-GST (15 Oct 2024), which reproduces the exact bare-act text of CGST Act Section 16(4) directly. Same tier of sourcing as the Singapore/IRAS citation in §2.
**Secondary check — China:** China's general rule allows indefinite carryforward of excess input VAT (confirmed structurally under the new VAT Law effective 1 Jan 2026) — but multiple secondary/practitioner sources (not a primary State Taxation Administration citation — **could not verify this one from a primary source in this pass**) describe a longstanding **360-day** window to certify/confirm a special VAT invoice (fapiao) on the government's invoice platform, after which the right to deduct that invoice's input VAT is lost. If accurate, that's a ~12-month procedural clock — tighter than Singapore's 5yr, in the same range as India's floor, but structurally different (a certification deadline, not a claim-filing deadline) and its status under the new 2026 VAT Law regime is unconfirmed. Flag as ASSUMED, not stated as fact.
**What it means operationally:** APAC's real floor may be India's ~8–20 months (or China's ~360 days, if that rule still holds), not Singapore's 5yr — the Singapore-hub story significantly undersells APAC's actual urgency. Of all three hubs, APAC's spread between its best-documented country (Singapore, 5yr) and its real floor (India, as low as ~8 months) is the widest — roughly an 8x difference within one hub.

**Urgency ranking, grouped for a fast read.** Ranks by *urgency* (how fast the window closes), not dollar size — no per-jurisdiction $ breakdown of the $8–30M exists. Covers only the 11 jurisdictions researched, not the full assumed 30-country footprint.

| Urgency | Jurisdiction(s) | Window | Source |
|---|---|---|---|
| Most urgent | Italy (EMEA) | ~4–5mo (Dec invoice) to ~15–16mo (Jan); flat 2yr from 2027 | Secondary |
| 2nd | India (APAC) | ~8mo to ~20mo, depending on invoice date | Primary (CBIC) |
| 3rd | China, if the fapiao rule holds (APAC) | ~12 months | ASSUMED, unverified |
| Moderate | France (EMEA), Canada large-business (Americas) | 2 years, flat | Secondary / Primary (CRA) |
| Lower | UK, Germany (EMEA), Canada general (Americas), US states | ~3–4 years, flat or varies | Secondary / Primary |
| Least urgent | Netherlands (EMEA), Singapore (APAC) | 5 years, flat | Secondary / Primary (IRAS) |

**Full per-jurisdiction detail, for sourcing and defensibility:**

| Rank | Jurisdiction | Hub | Worst-case floor | Typical / flat case | Source |
|---|---|---|---|---|---|
| 1 — most urgent | Italy | EMEA | ~4–5 months (Dec invoice) | ~15–16mo (Jan invoice); flat 2yr from 2027 | Secondary (converging) |
| 2 | India | APAC | ~8 months (March invoice) | ~20mo (April invoice) | Primary (CBIC) |
| 3 | China — *if* the fapiao-certification rule holds | APAC | ~12 months (360 days) | — | ASSUMED, secondary only, unverified |
| 4 (tie) | France | EMEA | 2 years, flat | — | Secondary |
| 4 (tie) | Canada, large business | Americas | 2 years, flat | — | Primary (CRA) |
| 6 (tie) | UK | EMEA | ~4 years, flat | — | Secondary |
| 6 (tie) | Germany | EMEA | ~4 years, flat | — | Secondary |
| 6 (tie) | Canada, general | Americas | 4 years, flat | — | Primary (CRA) |
| 9 | US states | Americas | ~3–4 years, varies by state | — | Secondary |
| 10 (tie) — least urgent | Netherlands | EMEA | 5 years, flat | — | Secondary |
| 10 (tie) | Singapore | APAC | 5 years, flat | — | Primary (IRAS) |

**Why this is worth showing, not just knowing:** it turns eleven scattered facts into one clear priority order — exactly the kind of synthesis a strong partner produces. It also directly explains two decisions already in the plan: Italy's #1 ranking is the sharpest reason for piloting in EMEA first (`answers/05-roadmap-pricing.md`), and India's #2 ranking is why it's the named phase-2 target ahead of the rest of APAC, not a hub-level choice.

**Recommendation:** don't attempt to research all 30 jurisdictions — not feasible at fast-pass depth and not needed. Use the hub-level minimums above (not the 3 hub headquarters' own numbers) as the representative "how fast can money actually be lost" figures for the info model, the prototype, and the diagnosis narrative. Keep the three hubs' numbers separate — do not flatten into one global "reclaim window" constant; that's exactly the mistake the brief's own "typically three to four years" framing risks, and the India/Italy/Canada findings show the risk is real, not theoretical. Also note: Italy and India's windows aren't flat N-years-from-invoice-date at all — they're bound to an annual return-filing deadline, so the actual runway depends on *when in the year* the invoice lands (see `answers/03-information-model.md` for why this is a modeling risk, not just a bigger number). All claims merged into `claims.md`.

## 5. Evidence document types — what they are, and what they map to

| Document | What it is | What it's actually used for | Info-model entity it feeds |
|---|---|---|---|
| Supplier invoices (14 languages) | The primary transaction record — price, tax charged, parties | Ground truth for "was tax charged correctly" | Invoice |
| Purchase orders | The pre-agreed terms and price | 3-way-match validation; confirms goods vs. services classification, which affects tax rules | Transaction; informs Recoverability Determination |
| Goods receipts | Confirms delivery or completion occurred | Timing — which filing period the transaction belongs to; completeness (partial deliveries) | Filing Period linkage |
| Contracts | The underlying agreement terms | Special tax treatment rules — reverse charge, intercompany arrangements, capital vs. opex | Recoverability Determination; Legal Entity relationships |
| Customs paperwork | Import/export documentation | Required evidence for cross-border import VAT/GST recoverability | Recoverability Determination (cross-border flag); Reclaim |
| Credit notes | Corrections to previously issued invoices | Retroactively adjusts a previously claimed or reported amount — can reopen a filing question | Transaction (correction subtype); Reclaim |

**Why this matters for the agent, concretely:** a clean case may only need invoice + PO + goods receipt. A cross-border case additionally needs customs paperwork. A correction needs the credit note plus the original invoice. A non-standard treatment needs the contract. This is direct input to what the exception path checks for, and to what "confidence" means at each step — not every determination needs every document, but the agent needs to know which documents a given case actually requires before it can be confident.

## 6. The systems evidence lives in — four sources, not three

**What the brief says, read precisely:** "It lives across **three SAP instances** inherited from acquisitions, **a tax engine**, **a shared mailbox** where suppliers send queries, and **a set of regional spreadsheets** nobody will admit to relying on." That's a list of four distinct source types — the three SAP instances are one item on the list, not the whole list:

1. **Three SAP instances** (from 3 acquisitions) — the core ERP records: invoices, POs, vendor master data
2. **A tax engine** — a separate system (Vertex/ONESOURCE/Avalara-type) that determines/records tax treatment
3. **A shared mailbox** — unstructured email correspondence with suppliers about invoice queries and disputes
4. **Regional spreadsheets** — informal, locally-maintained workarounds; "nobody will admit to relying on" is itself a tell that these are load-bearing shadow processes, not a minor footnote

**Gap worth flagging explicitly:** the brief's stated constraints ("no data leaves Northgate's tenant," "read access to SAP, no writes") are stated specifically about SAP. They say nothing about the tax engine, the mailbox, or the spreadsheets. **ASSUMED:** apply the same conservative posture (read-only, tenant-bound) to all four sources by default — this should be stated as an explicit assumption in `answers/02-workflow-proposal.md`, not silently extended.

**Diagnostic value of the spreadsheets specifically:** their existence is corroborating evidence for a data-quality/process-fragility root cause (supports EMEA's complaint) independent of anything EMEA said directly — worth naming as a second, independent signal pointing the same direction.

## 7. The stated ask vs. the actual job — "what the VP is wrong about," resolved

**Resolved candidate (the headline for Part 1.6):** the VP's own business-case quote — *"If AI codes the invoices, I free 24 people to do analysis instead of data entry. That is the whole business case"* — treats "coding" as mechanical data entry, separable from the tax-treatment judgment. It isn't. In AP/tax operations, "coding" an invoice means assigning it a tax code, and that code **is** the encoded answer to two of the brief's own three questions (charged correctly, recoverable) — not a task sitting next to treatment-classification, but largely the same action seen from a process lens instead of a substance lens. The EMEA manager's own words confirm this read: *"Coding is not the hard part."* She isn't calling coding trivial — she's saying that once supplier data is clean, getting the code right isn't where effort or errors concentrate. The real bottlenecks sit upstream of coding: dirty supplier master data (her complaint) and non-compliant invoices (the APAC analyst's complaint) — both corrupt the inputs to a coding/treatment decision regardless of how good the determination logic itself is.

**What this means for the pitch's reframe:** the VP isn't wrong that AI should absorb the coding work — he's wrong about what "coding" is (he thinks it's separable, low-value data entry) and wrong about what "analysis" will turn out to mean once people are freed from it. The freed capacity shouldn't go to a vague "analysis" bucket — it should go to the two concrete problems his own team already named: supplier-master-data remediation and invoice-compliance triage, plus the exception queue for genuinely ambiguous cases. That's a more specific, more defensible correction than "you asked for the wrong tool," because it's built entirely from stakeholders' own words, not an outside critique.

**Supporting point, not the headline:** the VP's literal ask — *"reads our invoices and tells us the right tax treatment"* — is also invoice-only in scope, and the team's actual job draws on evidence beyond the invoice (recoverability rules often live in the contract, cross-border treatment needs customs paperwork, timing needs the goods receipt, §5). This is real and worth having as Q&A ammunition, but it's a scope-of-input correction, smaller than the coding/judgment conflation above — useful supporting material, not the lead.

**How it reframes the other stakeholders' quotes:** EMEA's and APAC's complaints stop looking like two unrelated gripes and start looking like corroborating evidence for the same underlying point — both are naming exactly the upstream problems that survive no matter how good the coding/treatment logic is. This gives the diagnosis a throughline: the VP's own words, not just the practitioners' complaints, are evidence that "just automate the coding" undersells the job.

## 8. The EMEA manager's claim — "a third of our supplier master data is wrong"

**What the brief says:** "Coding is not the hard part. A third of our supplier master data is wrong. The same supplier exists as three vendors with three different tax profiles, and no model fixes that."

**What research confirmed (`research/sap-domain.md`):** SAP splits vendor data into general (client-wide) and company-code-specific data, including tax classification. Because Northgate's 3 SAP instances came from 3 separate acquisitions, each instance's AP team independently onboarded suppliers with no cross-instance identity concept — SAP's native duplicate-detection only fuzzy-matches within one instance. The same real-world supplier ends up as 3 separate vendor records, each with its own independently-set tax profile. This is why "no model fixes that": a better invoice-reader still looks up whichever tax profile is attached to the record the invoice happens to be coded against — if that record's profile is wrong, the answer is confidently wrong regardless of how good the reading is.

**Why this carries more weight than a stakeholder opinion:** independently corroborated by a real, documented SAP mechanism, not just her account — same evidentiary status as the APAC claim below, different from the VP's or Head of Tax Technology's quotes, which aren't independently confirmed by an outside mechanism.

**Two things we're assuming, because the brief doesn't specify them:** (a) what "a third" is measured against — vendor records, unique suppliers, or AP dollar volume. This doesn't change the severity call (large under any reading), but it does affect how big the entity-resolution build actually is; (b) which specific field differs across a supplier's duplicate profiles — most likely tax classification (VAT registration status, exemption, rate category), since that's the most consequential field, but not confirmed.

**Stakeholder-confidence risk, stated plainly:** treating this as a footnote risks losing her confidence — she gave the single most concrete, falsifiable claim in the whole discovery call. Phase 1 measures and reports the actual scale back to her, alongside the dollar burndown (`answers/05-roadmap-pricing.md`), rather than leaving her estimate unresolved.

## 9. The APAC analyst's claim — "the invoice does not meet the local format rules"

**What the brief says:** "Most of my month is chasing suppliers for compliant invoices. A lot of what we cannot recover is because the invoice does not meet the local format rules, not because anyone coded it wrong."

**What research confirmed:** real and documented, not an excuse. EU Directive 2006/112/EC Art. 226 sets an exhaustive 15-field mandatory invoice list; CJEU case law holds the deduction right shouldn't in principle be denied for purely formal defects, but tax authorities routinely deny administratively first, forcing the taxpayer to fight it back with secondary evidence. A VAT-reclaim firm (VAT IT) working live EMEA cases names incomplete invoices and missing VAT numbers as a recurring real rejection cause; Germany has a specific named trap (a missing *Leistungsdatum*, the date of supply, distinct from the invoice date).

**Is this only an APAC problem? No — confirmed as an EMEA problem too, and an expanding one.** Italy (since 2019), Poland (mandatory from 2026), and Spain (from 2027) are layering national e-invoicing *clearance* mandates on top of the EU content minimum — a correctly-fielded invoice can still be rejected on pure schema/clearance grounds. This is what confirms the format-compliance check belongs in Phase 1/EMEA scope now, not deferred to an APAC-only phase.

**APAC specifics, researched to the same depth as the EU:** Singapore (IRAS — 10 mandatory fields, a S$1,000 simplified-invoice threshold, single-field omission voids the claim) is the same shape as the EU and should generalize cheaply. India (Rule 46, ~19 particulars, plus government IRP/IRN clearance above ₹5 crore turnover) is structurally closer to Italy/Poland's clearance model — real extension work, not a config change. China (special VAT fapiao, state-issued and STA-verified) is a fundamentally different model — secondary-sourced only, flagged as a "known won't work as-is" if China is ever discussed as a later phase.

**A gap this surfaced in our own assumed footprint:** Switzerland and Turkey, both in the assumed EMEA country list, aren't EU members and aren't covered by Art. 226 at all — a compliance check built only against the EU baseline would silently miss them.

**Scoping decision:** the compliance *check* is in scope — it feeds the recoverability determination directly (a non-compliant invoice can't be reliably scored regardless of what it says). Automated supplier *outreach* (drafting/tracking correction requests) is explicitly out of scope — a supplier-communication system, not a tax-determination system, outside the brief's ask and the 2-engineer/8-week budget. This is the answer to the prototype's required "one thing chosen not to build" talking point (`answers/04-prototype-notes.md`).

## 10. Enterprise security — "nothing leaves our tenant," and the ~11-week review

**What the brief says:** "Nothing leaves our tenant. And you go through the vendor security review like everyone else. It runs about eleven weeks."

**In plain terms:** "tenant" means Northgate's own private cloud environment — like a locked room only Northgate holds the key to. The obvious approach (calling a public AI API directly) sends data out of that room into the AI vendor's own room. That's exactly what's ruled out. The answer isn't "don't use AI" — it's "run the AI inside Northgate's own room." Microsoft's Azure OpenAI offering lets a customer provision their own private instance of the model inside their own Azure account, so the question and answer never leave Northgate's environment. A "private endpoint" adds a private hallway between Northgate's system and that AI instance so the connection never touches the public internet either. Microsoft also contractually commits not to read the data or use it to train its own models. The one honest limit: the underlying hardware is still Microsoft's — no hosted option (and realistically no self-hosted one either) achieves a literal "zero third party ever involved." The checkable, defensible definition to propose: data stays in the customer-owned resource and chosen region, is never used for training, is never visible to the model provider, and never transits the public internet.

**What research confirmed on the review itself (`research/security-review-norms.md`):** 8–12+ week reviews are standard for high-risk-tier vendors — Northgate's 11 weeks sits inside that range. SIG and CAIQ are the standard questionnaires; CAIQ specifically probes cloud tenancy, residency, and encryption — meaning the review will directly test whatever tenant-boundary answer is given, not just accept it as a slide claim. The review starts at signing and outlasts the 8-week build by ~3 weeks — the entire justification for the sandbox → shadow-mode → staged-access sequencing already in the roadmap.

**Hyperscaler: confirmed as Microsoft/Azure for planning purposes.** Two independent, stacking signals supported this before it was settled: large SAP-centric multinationals commonly pair with Azure (the "RISE with SAP" ecosystem), and "tenant" is specifically Microsoft/Entra ID's core term for this concept — AWS calls the equivalent an "Account/Organization," GCP a "Project/Organization." Still ASSUMED in the PIL sense (nothing external verified this — it's Renata's call to settle the fictional detail for planning), but no longer hedged as an open three-way question.
- **Azure (confirmed)** → Azure OpenAI, provisioned in Northgate's own subscription, private-endpoint-only. The primary, presented answer.
- **AWS (noted alternative)** → AWS Bedrock, via PrivateLink — kept as a one-line fallback in case the brief's curveball ever touches this, not a hedged parallel option.
- **Self-hosted open-weight model** — the most literal answer to "nothing leaves our tenant," considered and declined: unrealistic for 2 engineers in 8 weeks given the GPU/MLOps burden.
- **A public multi-tenant API** — considered and declined: directly disqualified by the security stakeholder's line.

**Who pays for this, and why it matters for pricing.** Because the AI resource lives inside Northgate's own cloud subscription, Northgate's cloud provider bills Northgate directly for the compute/API consumption — not Ampliwork. Ampliwork's fee (`answers/05-roadmap-pricing.md`) covers the service layer: designing, building, and operating the determination logic and exception workflow. It does not include Northgate's own cloud consumption cost. This is standard for a "bring your own cloud" deployment, and it strengthens the fixed-fee argument rather than complicating it: usage-based AI cost scales with Northgate's own transaction volume on Northgate's own bill, so Ampliwork's fee doesn't need to absorb that variability to stay fixed and predictable.

**Reconciling the language:** "determine externally" (the workflow's architecture — outside SAP) and "nothing leaves our tenant" (outside Northgate's cloud boundary) describe two different boundaries, not a contradiction. State this explicitly on the assumptions slide rather than leaving it for the panel to question.

## Decisions made

- **$4M penalty jurisdictions:** left as stated in the brief — "two jurisdictions," not named, not "all of them." The brief is precise here: exactly two, a bounded and comparatively mild picture, not systemic exposure across the footprint.
- **Hyperscaler:** confirmed as Microsoft/Azure for planning purposes. Simplifies the architecture story to Azure OpenAI directly (`answers/02-workflow-proposal.md`), with AWS/Bedrock kept as a one-line noted alternative rather than a hedged three-way menu.
- **Contingency pricing:** revised — phased expansion from the narrow Phase 1 bucket to the full ongoing recovered-$, conditional on proven human-in-the-loop control, tracked metrics, and a demonstrated below-baseline error cost. See `answers/05-roadmap-pricing.md`.
- **"What the VP is wrong about" (Part 1.6 headline):** resolved as the coding/judgment conflation in her own business-case quote (§7) — not the invoice-only-scope point, which is now supporting material. See `answers/01-diagnosis.md` for the full candidate comparison.
- **Regional spreadsheets become a supported knowledge base, curated not imported, with a review gate.** The 4th named data source (the shadow spreadsheets analysts already keep) gets formalized into a structured, versioned exceptions store — but seeded by *curating* existing content, not ingesting it wholesale, since the spreadsheets are informal precisely because nobody fully trusts them either. New entries come from a feedback loop: an analyst's override of a system determination becomes a *candidate* entry, reviewed and approved (by the hub tax manager) before it can influence future auto-processed determinations. This is the concrete mechanism behind NFR5's "confidence threshold tightens as accuracy improves" claim — previously an unexplained promise — and it's the trust-building answer for the Head of Tax Risk specifically: every accepted override is now an auditable, reviewed record instead of a one-off judgment call. Included in the prototype, not deferred. See FR12/FR12a/FR13/FR13a/DR4 above.

## Deferred as follow-ups (not blocking)

- [ ] Switzerland/Turkey (§9): whether they get their own compliance rule set or are explicitly excluded from v1 coverage — not needed to lock the current plan, revisit later.

## Still open

- [ ] Decide whether the AP-spend cross-check calculation (§3) — Accounts Payable, money Northgate owes suppliers; the calc landed at ~$5.6-8.4M, near the low end of the $8-30M range — is worth including as a defensible sanity-check in the deck, clearly labeled as such

## Product requirements (for the PRD)

Testable, ready to seed a PRD. Grouped by feature, not by requirement type — IDs (FR/NFR/DR/EX) are kept as-is so existing cross-references (in Decisions above, `requirements.md`, the digest) still resolve; only the grouping and order changed. Tags: **[brief]** = stated directly in the case study, not derived; **[prototype]** = actually built/demonstrated in the prototype. Mirrors the digest's blue/green color-coding — see `prototype/README.md`'s build breakdown for what "actually built" means concretely.

**1. Tax-treatment determination engine** — the core capability: read the evidence, cross-reference beyond the invoice where needed, determine the three-part treatment, score confidence, and use the correct (deduplicated) supplier identity.
- FR1. The system shall determine, per transaction, whether tax was charged correctly, whether it is recoverable, and where it should be reported. **[brief] [prototype]**
- FR1a. The system shall extract and structure the evidence needed for a given determination from whichever of the six named document types apply — invoice, purchase order, goods receipt, contract, customs paperwork, credit note — not only the invoice. **[prototype]**
- FR1b. Where a determination depends on evidence beyond the invoice (e.g., recoverability terms in a contract, cross-border treatment in customs paperwork, timing from the goods receipt), the system shall retrieve and incorporate that evidence rather than determining from invoice content alone (case-facts.md §7). **[prototype]**
- FR2. The system shall compute a confidence score for each determination. **[prototype]**
- FR2a. The system's determination shall use the entity-resolved supplier tax profile (DR2), flagging cases where a supplier has conflicting duplicate profiles, rather than silently using whichever vendor record the transaction happens to be coded against (case-facts.md §8 — the EMEA manager's failure mode). **[prototype]**
- DR2. Supplier (real-world entity) and vendor master record (per-instance SAP object) shall be distinct entities, connected via an entity-resolution mapping. **[prototype]**

**2. Confidence-based routing & analyst workflow** — how a human stays in the loop at every confidence level, since the system can never execute anything itself.
- FR3. The system shall route determinations below a configurable confidence threshold to human review, with supporting evidence and reasons attached. **[prototype]**
- FR3a. Determinations at or above the confidence threshold shall still require an explicit analyst confirm-and-file action before any filing occurs — presented as a streamlined batch-confirm step, not autonomous execution. No determination, at any confidence level, is filed without an analyst action (consequence of FR7 — the system cannot write to SAP or any filing system regardless of confidence). **[prototype]**
- NFR5. The confidence threshold shall be configurable and shall tighten over time as measured accuracy improves. **[prototype]**
- NFR6. Auto-processed determinations shall be optimized for precision; the routing decision shall be optimized for recall. **[prototype]**
- FR9. The review interface shall present transactions grouped for reviewer efficiency, while each transaction remains its own individually addressable record. **[prototype]**
- DR3. The individual transaction shall be the atomic unit of record; no aggregation into a batch record at the data layer. **[prototype]**

**3. Reclaim-window urgency tracking** — jurisdiction-aware timing, so the queue reflects what's about to expire, not just what's uncertain.
- FR4. The system shall compute a time-to-expiration value per transaction, from that transaction's own invoice date and its jurisdiction's reclaim-window rule (rolling-N-years or return-deadline-bound). **[prototype]**
- FR5. The exception queue shall be ordered by urgency (time-to-expiration) in addition to confidence. **[prototype]**
- DR1. Jurisdiction shall be a first-class entity with its own parameters (reclaim-window rule type/value, invoice-content rules, filing frequency), independent of which hub processes the transaction. **[prototype]**

**4. Invoice format-compliance checking** — a second, separate capability from tax-treatment determination: is the document itself valid before its content is even scored.
- FR6. The system shall check each invoice against its jurisdiction's mandatory-content requirements (field-checklist or government-clearance mechanism) as a distinct step feeding the recoverability determination. **[prototype]**
- EX1. Automated supplier outreach (drafting/sending/tracking correction requests) is out of scope for this engagement.
- EX2. Full support for China's fapiao-based invoicing model is out of scope until scheduled as its own phase; the compliance check shall not be assumed to extend there without dedicated rework.

**5. Backlog + ongoing processing pipeline** — one engine, two input modes.
- FR8. The system shall process both an accumulated historical backlog (batch mode) and an ongoing incoming stream (continuous mode) via the same determination pipeline.

**6. Recovery & diagnostic reporting** — what gets reported back to the VP and the EMEA manager specifically.
- FR10. The system shall report, on a recurring cycle, dollar amount recovered to date against the updated remaining-estimate (a burndown). **[prototype]**
- FR11. The system shall report the measured scale of the supplier-master-data-quality problem as part of Phase 1 diagnostics. **[prototype]**
- FR11a. The system shall report the measured error rate (false-positive rate on auto-processed determinations) on a recurring cycle, trended against the Phase 1 human-only baseline and against a modeled annualized cost-of-error line derived from Northgate's own $4M/year penalty figure. This is the reporting mechanism that produces the evidence for Phase 2+ pricing condition 3 ("demonstrated below-baseline error cost," `answers/05-roadmap-pricing.md`) — not a separate nice-to-have metric. **[prototype — wireframe mockup, not live-calculated; see methodology below]**

**FR11a's calculation, stated honestly — one more stacked assumption, flagged as such, not hidden in a clean chart.** Modeled annualized error cost = (measured false-positive rate) × (auto-processed transaction volume/year) × (average $ exposure per false positive). The first two terms are measurable in Phase 1 (real eval data) or already-estimated (`research/assumed-customer-profile.md`'s volume/invoice-mix work). The third — average $ exposure per false positive — has no source in the brief; the illustrative placeholder is the average invoice value (~$1,700, itself a stacked estimate), used as an order-of-magnitude proxy for "amount at risk if this specific determination is wrong," not a real penalty formula (actual penalty/interest exposure per error isn't 1:1 with invoice value, and isn't disclosed). **The $4M/year figure itself is real and VERIFIED (the brief's own number) — only the "modeled cost" line being compared against it is illustrative.** State this distinction plainly if asked how the crossover is actually computed: one real anchor, one modeled trend.

**8. Knowledge base & trust-building feedback loop** — the fourth named data source (regional spreadsheets) formalized, plus the mechanism that makes NFR5's "accuracy improves over time" concrete rather than a promise. Load-bearing for trust with the Head of Tax Risk specifically: every accepted override becomes an auditable, reviewed record, not a one-off judgment call lost after the fact.
- FR12. The system shall maintain a structured, versioned knowledge base of jurisdiction- and entity-specific exceptions beyond the base rule set, seeded by curating existing regional-spreadsheet content — not by importing it wholesale (§ new decision below). **[prototype]**
- FR12a. Each knowledge-base entry shall carry provenance (source, author, date, review status: proposed / reviewed / approved). An entry shall not influence auto-processed (high-confidence) determinations until approved. **[prototype]**
- FR13. When an analyst overrides a system determination, the override and its stated reason shall be captured as a candidate knowledge-base entry, not discarded. **[prototype]**
- FR13a. Candidate knowledge-base entries shall be surfaced for review (by the hub tax manager persona, `answers/02-workflow-proposal.md`) before being promoted to an approved, active rule. **[prototype]**
- DR4. Knowledge-base entries shall be a first-class entity, distinct from jurisdiction rules (DR1) and entity-resolution mappings (DR2), linked to the specific transaction(s) that originated or were affected by them, for auditability. **[prototype]**

**7. Platform & security constraints** — the tenant/SAP boundary the whole system is built inside of.
- NFR1. All data processed shall remain within Northgate's own cloud tenant/subscription; no data shall be sent to a public multi-tenant model API. **[brief]**
- NFR2. All communication with any model/AI resource shall occur over a private network path, not the public internet.
- NFR3. Any third-party model provider shall be contractually prohibited from using Northgate's data for training or accessing it outside the agreed service boundary.
- NFR4. SAP access shall be read-only; no write access to any SAP instance, in any version. **[brief]**
- FR7. The system shall not write or post any determination into SAP or any filing system; write-back is performed only by an authorized human or downstream system. **[brief] [prototype]**
- EX3. Consolidation of the 3 SAP instances is out of scope; the solution operates across all 3 as-is. **[brief] [prototype]**
