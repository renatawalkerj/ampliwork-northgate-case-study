# Case Facts & Assumptions — Northgate Industries

Feeds Phase 1 (diagnose, propose, model) directly. Three layers throughout: **What the brief says** (cited), **What we're assuming** (tagged, reasoning shown, mirrored in `claims.md`), **What research filled in** (linked to `research/*.md`).

## 1. Who does the tax function actually manage, and what does "right" mean

**What the brief says:** the team is responsible for VAT, GST, and sales & use tax "across every jurisdiction Northgate operates in" — all 30 countries, not just the 3 hub cities. Chicago, Rotterdam, and Singapore are where the 24 people are organized, not a scope limit. Confirmable from the brief's own quote attributions: "Regional tax manager, **EMEA**" and "Analyst, **APAC**" tell us Rotterdam = EMEA hub, Singapore = APAC hub, Chicago = Americas hub by elimination.

**Per transaction, three separate decisions**, straight from the brief: (1) was tax charged correctly, (2) is it recoverable, (3) where should it be reported. These aren't one lookup — see §7, this is the crux of the diagnosis.

**Wrong in one direction vs. the other, precisely:**
- Fail to identify/claim recoverable tax → **leaves cash on the table** (the $8–30M problem, §3)
- Incorrectly claim or misreport → **audit exposure and penalties** (the $4M problem, §3)

**Key insight, not stated directly in the brief but follows from combining §1 and §2:** the reclaim window (§2) is a safety net for the *first* kind of mistake — an under-claim can still be caught and fixed until the window closes. There is **no equivalent safety net for the second kind** — an over-claim or misreport is caught by auditors, on their timeline, at the company's expense, with no self-correction runway. This asymmetry is a sharper, more concrete justification for the Head of Tax Risk's "wrong matters more than slow" position than just calling her risk-averse — her risk genuinely has no safety net; the VP's does.

## 2. The two clocks (plus a third we found)

**What the brief says:** filing deadlines are monthly or quarterly depending on jurisdiction; separately, each jurisdiction has a reclaim window, "typically three to four years," after which the money is gone.

**What research confirmed (VERIFIED, see `claims.md`):** the "3–4 years" is a reasonable average but not one clock — UK ~4yr, Germany ~4yr, **Netherlands ~5yr**, **France ~2yr** (a real outlier), US states ~3–4yr, **Singapore 5yr** (confirmed directly from IRAS, closing a gap — Singapore was the one hub jurisdiction not yet checked). Singapore also has a genuine third clock the brief doesn't mention: if input tax is claimed before the supplier is paid, payment is due within 12 months or the claim must be repaid.

**What we're assuming:** per-jurisdiction filing frequency (monthly vs. quarterly, specifically) isn't given for any of the 30 countries, and we haven't researched it country by country — that level of enumeration isn't feasible or necessary for the pitch. ASSUMED: Northgate's high-volume hub jurisdictions are more likely on monthly filing given transaction volume, stated as a general pattern, not a per-country confirmed fact. This is thin enough that it shouldn't be quoted as specific in the room.

**What this means operationally:** monthly transaction volume creates a rolling decision cadence; the reclaim window is the outer deadline for catching missed recoverable amounts within that cadence. There's no equivalent grace period on the over-claim side — which is exactly why phasing the rollout around proving correctness first (see the roadmap) matters more than proving speed first.

## 3. The money — $4M penalties, $8–30M unrecovered

**$4M in penalties/interest, last year, across two jurisdictions — the brief does not name them.** Recommendation: don't invent specific countries for the pitch. If the deck needs concreteness, name two illustrative jurisdictions (e.g. one EU country + the US) and flag it explicitly as illustrative, not a stated fact — inventing unstated specifics that could get challenged is a worse risk than leaving it as "two jurisdictions," which is what the brief actually says.

**$8–30M/year unrecovered is Northgate's own disputed internal estimate.** The brief is explicit that the width of the range is itself part of the problem — this is a diagnostic signal, not a data gap to apologize for.

**Can we tighten it externally? No — and we shouldn't pretend to.** Research found no benchmark for indirect-tax leakage as a % of AP spend at Northgate's specific scale (`research/tax-domain.md`). One rough cross-check, offered as a sanity check only, not a confirmation: AP-recovery-audit firms report recovering roughly $1M per $1B of supplier spend (ASSUMED, vendor-sourced ratio, `claims.md`). If Northgate's AP spend is ~40–60% of its $14B revenue (a common but unconfirmed ratio for an industrial manufacturer), that ratio implies **~$5.6–8.4M** — landing near the *low* end of Northgate's own $8–30M estimate. That's suggestive (the $30M end may be optimistic, or Northgate's multi-jurisdiction VAT complexity exceeds what a domestic-audit ratio captures) but built on two stacked assumptions — not something to state as fact in the room.

**Should narrowing this number be part of the plan? Yes — explicitly.** This is the strongest argument for the roadmap's diagnostic-first phase: the only credible way to turn $8–30M into a number the VP can defend by year-end close is to measure it from Northgate's own exception data, not from outside benchmarks. This should be stated plainly as Milestone 1's actual deliverable in `answers/05-roadmap-pricing.md`, not left implicit.

## 4. Jurisdictions

**Named directly:** only the 3 hub countries (US, Netherlands, Singapore) out of "30 countries." The other ~27 aren't enumerated anywhere in the brief.

**Reclaim windows confirmed (VERIFIED):** UK, Germany, Netherlands, France, generic US states, and now Singapore (§2).

**Recommendation:** don't attempt to research all 30 jurisdictions — not feasible at fast-pass depth and not needed. Use the 3 hub jurisdictions as the representative set for the info model, the prototype, and the diagnosis narrative; treat the general "2–5 year, jurisdiction-dependent" pattern as sufficiently well-evidenced for everything outside those 3.

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

## 7. The stated ask vs. the actual job — the sharpest candidate for "what the VP is wrong about"

**The VP's literal words:** *"can you build us an AI that reads our invoices and tells us the right tax treatment?"* — one input (invoices), one output (a single "treatment").

**The team's actual job, per the brief's own description (§1):** three separate determinations per transaction, each drawing on **different evidence beyond the invoice** — recoverability rules often live in the contract, cross-border treatment needs customs paperwork, timing needs the goods receipt (§5).

**This is a strong, evidence-based answer to Part 1.6.** The VP's own framing of the solution undersells what's actually required: an invoice-only reader cannot reliably answer 2 of the 3 questions the team actually has to answer (recoverability, correct reporting jurisdiction), because those depend on evidence the invoice alone doesn't contain.

**How it reframes the other stakeholders' quotes:** EMEA's and APAC's complaints stop looking like two unrelated gripes and start looking like corroborating evidence for the same underlying point — both are describing exactly the kind of non-invoice context (supplier identity, document validity/compliance) that an invoice-only tool would miss. This gives the diagnosis a throughline: the VP's own framing of the ask, not just the three practitioners' complaints, is evidence for a broader-than-invoices information model — which is also the direct justification for why the workflow proposal (§Part 1.2) needs multi-document input, not invoice-only.

## Open items before Phase 1 locks

- [ ] Decide whether to name illustrative jurisdictions for the $4M penalty story, or leave it as "two jurisdictions" per the brief (recommend the latter)
- [ ] Decide whether the AP-spend cross-check calculation (§3) is worth including as a defensible sanity-check in the deck, clearly labeled as such
- [ ] Confirm the "VP is wrong about invoice-only framing" angle (§7) as the Part 1.6 answer, or weigh it against alternatives
