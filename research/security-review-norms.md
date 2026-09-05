# Vendor security review norms — fast pass

Status: researched (fast pass, web search only — see caveats below).

Covers: what an ~11-week enterprise security review typically checks, and how vendors/consultancies phase delivery when the review outlasts the build window. Feeds the Northgate roadmap directly — the review (11 weeks) outlasts the build (8 weeks) by ~3 weeks, which is what forces phase sequencing in the pitch.

---

## 1. What a vendor security review actually checks, and why large-enterprise reviews run 8-12+ weeks

**The standard toolkit:**
- **Questionnaires** — the two dominant standardized forms are **SIG (Standardized Information Gathering)**, from Shared Assessments, and **CAIQ (Consensus Assessments Initiative Questionnaire)**, from the Cloud Security Alliance. They overlap but differ in scope: CAIQ is narrower and cloud-specific — deep on shared responsibility, multi-tenancy/tenant isolation, data residency, encryption and key management. SIG is broader — it covers those same cloud topics at lower resolution but also pulls in HR security, physical security, operational resilience, and third-party governance. A large enterprise like Northgate's security team plausibly runs a SIG-style questionnaire (or an internal equivalent) precisely because they care about more than "is your cloud config sane" — they also want vendor governance, subprocessor lists, incident history, insurance.
- **SOC 2 report** (Type II ideally) — the artifact that answers most of the questionnaire before it's even filled out. Its absence is itself a major reason reviews stretch: without it, every control question has to be answered manually and then independently verified.
- **Penetration test evidence** — enterprise buyers commonly require a third-party pen test report from within the last 12 months before finalizing. If the vendor doesn't have one, or the AI-specific attack surface isn't covered by an existing one, that alone can add weeks (commissioning + running + remediating a fresh test).
- **Data residency / tenancy questions** — where data physically lives, how tenants are logically isolated, whether the vendor commingles customer data for model training, subprocessor chains (does the vendor's own AI vendor see the data too).
- **Third-party / supply-chain risk assessment** — the vendor's own vendors get assessed transitively, which is exactly Northgate's "nothing leaves our tenant" posture pointed at a build that itself likely touches an LLM provider.

**Why 8-12+ weeks is normal for a large enterprise, not an outlier:**
- Timelines compound across departments that don't move in parallel by default: security review, legal (data ownership, liability, SLAs, termination), procurement (contract structure, compliance exposure), and often a separate privacy/DPIA step for anything touching personal data. Each has its own queue.
- A commonly cited breakdown for enterprise security software deals: internal consensus-building (6-8 weeks), legal review (2-4 weeks), procurement negotiation (8-12 weeks) — these can overlap somewhat but frequently run sequentially because of a "handoff gap": security doesn't start the clock until someone has explicitly routed the vendor into their queue, and the queue often doesn't open until commercial/executive sign-off exists.
- Sequential requirement discovery is a recurring, named failure mode — the reviewer surfaces a new requirement only after the vendor clears the current one, so each round-trip adds a week or more that a fully-scoped review wouldn't need. This is consistent with Northgate's "starts when you sign" framing: the review clock plausibly can't even start (or can't finish scoping) before contract signature, which is the exact structural constraint the brief calls out.
- General industry vendor-onboarding averages (all risk tiers blended) run 45-60 days engineering-org-wide, with best-in-class or low-risk-tier vendors clearing in under two weeks — but that average includes lightweight SaaS tools. An 11-week estimate for Northgate (an AI system with read access into three SAP instances holding financial/tax data, at a $14B multinational) sits at the high end of normal for a **high-risk-tier, data-adjacent** vendor, not an anomaly.

**Caveat:** I could not find a single authoritative source that states "enterprise vendor security reviews average exactly 8-12 weeks" as a clean statistic — the figures above are triangulated from several vendor-risk-management blogs (UpGuard, Shared Assessments/CAIQ comparison pieces, TPRM industry blogs) rather than one canonical benchmark study. Treat the 8-12+ week range as well-supported directionally, not as a precise, citable industry KPI.

---

## 2. How delivery gets phased when the security review outlasts the build

Three real, named patterns recur across vendor/consulting and AI-rollout playbooks:

**a) Sandbox / synthetic-data pilot that doesn't require full review clearance.**
Standard enterprise SaaS sales pattern: stand up a sandbox that "looks and feels like the real product" but runs on synthetic or anonymized data, independent of production infrastructure. This lets a vendor demo and even let users work in a live-feeling environment before the full security review clears, because the risk surface (real customer/production data) isn't present yet. Directly applicable to Northgate: a version of the invoice-coding agent could run against synthetic/sample invoices and non-production SAP extracts during the review window, with the switch to live SAP read access gated on review sign-off.

**b) Crawl-walk-run staged data-access expansion, scoped by least privilege.**
This is the dominant pattern in current agentic-AI enterprise rollout guidance (Microsoft, Zscaler, Writer, and others all converge on the same shape): start with **scoped, short-lived credentials against staging/non-production data**, not production-grade access; expand access only as evidence accumulates (accuracy on historical/back-tested data, simulated decisions, bounded pilot with a kill switch); avoid granting broad access up front "to unblock a pilot" because that access rarely gets walked back later. For Northgate this maps cleanly onto "read access to SAP, no writes" — the review could gate the read scope itself (e.g., one SAP instance / one region first, expand to three instances after full clearance).

**c) Shadow-mode operation before production trust.**
Run the agent in parallel with the human process — it produces a recommendation/determination but doesn't act on it or replace the human's output — while its outputs are logged and compared against what the human analysts actually did. This is explicitly used to build organizational trust (does the team believe it) as distinct from technical validation (does it work), which matters directly for Northgate given the Head of Tax Risk holds veto power and "wrong" worries her more than "slow." Typical minimum duration cited is a couple of weeks, realistically 4-8 weeks, sometimes followed by a canary-style expansion (e.g., 5% of live decisions, then 10%, 25%, 100%) once error rates are acceptable — though the canary-percentage pattern is more common in general ML/software rollout writing than in tax/finance-specific vendor material.

**Net structural implication for the pitch:** the 8-week build and 11-week review don't have to be sequential. The standard playbook is to build/demo in weeks 1-8 against a sandbox or synthetic-data / non-production SAP extract (pattern a), run in shadow mode against real (or real-shaped) data as the review continues (pattern c), and flip to live SAP read access only after the review clears in week 11 — with the "flip" itself potentially staged one SAP instance at a time rather than all three at once (pattern b). This gives Northgate something to see and evaluate by week 8 without violating "nothing ships without [security's] clearance."

**Caveat:** these three patterns are well-documented as general enterprise SaaS / agentic-AI rollout practice (sandbox demos, least-privilege staged access, shadow-mode validation are all named, current — 2026 — practitioner content from vendors like Microsoft, Zscaler, Writer, and enterprise sandbox/sales-process writeups). I did not find a source describing this exact three-pattern sequencing specifically for a security-review-outlasts-build scenario in tax/ERP software — that synthesis (mapping pattern a/b/c onto Northgate's specific 8-week/11-week gap) is original reasoning for this case study, not a reported industry case.

---

## Sources

- [CAIQ vs SIG: Which Security Questionnaire Should You Use?](https://blog.getagency.com/articles/caiq-vs-sig) — Agency Insights
- [What Is the CAIQ Questionnaire? A Clear Guide](https://securityscorecard.com/blog/what-is-the-caiq-questionnaire-a-clear-guide/) — SecurityScorecard
- [CAIQ vs. SIG Questionnaires: What's the Difference?](https://www.bitsight.com/blog/caiq-vs-sig-top-questionnaires-vendor-risk-assessment) — Bitsight
- [Security Bottleneck? Here's How to Accelerate Vendor Approvals](https://www.upguard.com/blog/accelerate-vendor-approvals) — UpGuard
- [Why Security Software Deals Stall at Procurement](https://www.trackforce.com/resources/blog-articles/why-security-software-deals-stall-at-procurement-and-how-to-prevent-it/) — Trackforce
- [Why do periodic vendor assessments so often become a bottleneck?](https://nhimg.org/faq/why-do-periodic-vendor-assessments-so-often-become-a-bottleneck/) — NHI Mgmt Group
- [The Vendor Onboarding Process: 5 Stages, Best Practices](https://technologymatch.com/blog/vendor-onboarding-process-5-stages-best-practices-for-it) — TechnologyMatch
- [Vendor Onboarding: The Risk-Led Process](https://visualping.io/blog/vendor-onboarding) — Visualping
- [What Is a SaaS Sandbox? Safe Testing & Development](https://payproglobal.com/answers/what-is-saas-sandbox/) — PayProGlobal
- [SaaS Vendor Security Review: What IT Teams Ask & How to Prep](https://licenselogic.co/blog/saas-vendor-security-review-checklist) — License Logic
- [Shadow mode, drift alerts and audit logs: Inside the modern audit loop](https://venturebeat.com/orchestration/shadow-mode-drift-alerts-and-audit-logs-inside-the-modern-audit-loop) — VentureBeat
- [Shadow Mode Rollouts for AI Agents: A Safer Path from Pilot to Production](https://brightlume.ai/blog/shadow-mode-rollouts-ai-agents-pilot-production) — Brightlume AI
- [Shadow mode: how to roll out AI agents safely in your service desk](https://www.itsmautopilot.com/en/blog/shadow-mode-ai-rollout) — ITSM Autopilot
- [Least privilege for AI agents: Identity, access, and tool binding](https://www.microsoft.com/en-us/security/blog/2026/07/16/least-privilege-for-ai-agents-identity-access-and-tool-binding/) — Microsoft Security Blog
- [How to Establish Least-Privilege for AI Agents and Assistants](https://www.zscaler.com/blogs/product-insights/least-privilege-access-ai-agents-assistants) — Zscaler
- [Agentic AI adoption: A leader's roadmap to enterprise governance](https://writer.com/blog/responsible-ai-adoption-and-training/) — Writer
- [How to Roll Out AI Agents Safely](https://praesidia.ai/blog/how-to-roll-out-ai-agents-safely) — Praesidia

---

## Claims for claims.md

| Claim | Status | Source | Notes |
|---|---|---|---|
| Enterprise vendor security reviews commonly take 8-12+ weeks for high-risk-tier vendors (data-adjacent, financial systems access) | ASSUMED | UpGuard, Trackforce, NHI Mgmt Group blogs (triangulated, no single benchmark study found) | Directionally well-supported; not a single citable industry KPI. Northgate's stated 11 weeks sits inside this range for a high-risk vendor. |
| SIG and CAIQ are the two dominant standardized vendor security questionnaires; SIG is broader (HR, physical, ops, governance), CAIQ is deeper on cloud-specific tenancy/residency/encryption | VERIFIED | Bitsight, SecurityScorecard, Agency Insights CAIQ/SIG comparisons | Multiple independent sources agree on this scope distinction. |
| A current SOC 2 report and a recent (≤12 month) third-party pen test are the two artifacts that most shorten a review by pre-answering the questionnaire | ASSUMED | License Logic, general SOC 2/vendor-review blogs | Consistent across sources but no hard data on time saved. |
| Sequential, siloed handoffs between security/legal/procurement (rather than parallel workstreams) are a primary named cause of long review timelines | ASSUMED | Trackforce, UpGuard, NHI Mgmt Group | Repeated pattern across sources; framed as "bottleneck," not measured precisely. |
| Sandbox demos on synthetic/anonymized data are a standard way vendors let enterprise prospects evaluate a product before security review clears production access | ASSUMED | PayProGlobal, License Logic | Well-established SaaS sales pattern; not tax/ERP-specific. |
| Crawl-walk-run staged data-access expansion (scoped, short-lived credentials on non-production data first, production access only after evidence accumulates) is current standard guidance for agentic AI rollouts | ASSUMED | Microsoft Security Blog, Zscaler, Writer | Multiple current (2026) vendor practitioner sources converge on this shape. |
| Shadow-mode operation (agent produces output in parallel with humans, without acting, before being trusted with production decisions) is a named, current pattern for building organizational trust in AI systems, distinct from technical validation | ASSUMED | VentureBeat, Brightlume AI, ITSM Autopilot | Duration estimates (2 weeks minimum, 4-8 weeks realistic) are loosely sourced, treat as approximate. |
| Mapping sandbox-pilot -> shadow-mode -> staged-SAP-access specifically onto Northgate's 8-week-build / 11-week-review gap is original synthesis for this case study, not a reported real-world case | VERIFIED (as a statement about this document's own reasoning) | N/A — original synthesis | Flag this honestly if asked "is this a known playbook" — the individual patterns are real; this specific sequencing applied to Northgate is not a documented case. |
