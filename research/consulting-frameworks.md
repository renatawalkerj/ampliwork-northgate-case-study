# Consulting frameworks — fast-pass extraction

Source: `career/Consulting management books/` in renata-projects. Fast-pass extraction (targeted chapters/keyword search, not full reads) done via epub unzip + tag-stripping for the three .epub files, and `pdftotext` for the Playing to Win PDF. Each section below is marked with what was actually read from the book vs. general knowledge — see the claims table at the bottom for the per-claim breakdown.

---

## Bulletproof Problem Solving (Conn & McLean) — VERIFIED (read Ch. 2 "Define the Problem" and Ch. 3 "Problem Disaggregation and Prioritization")

**Logic trees, MECE, and cleaving frames.** The book's core disaggregation move: state a problem, then break it into a *logic tree* — trunks, branches, twigs, leaves — that is MECE (mutually exclusive, collectively exhaustive). It names four tree types and when to use each: **component/factor trees** (early, when you only know the rough shape of a problem — inductive, built from brainstorming), **hypothesis trees** (once you have enough to state testable claims at each branch — "vague labels do not drive analysis or action"), **deductive logic trees** (when the structure is arithmetic/logically complete, e.g. a return-on-capital tree), and **decision trees**. It also names a technique it calls **"what you have to believe" analysis** — using a deductive/return-on-capital tree to make a team debate how realistic the assumptions are that would have to hold for a number to work out.

**Problem statement discipline.** Before disaggregating, the book insists a problem statement be outcomes-focused, specific/measurable, time-bound, and — critically — **solved at the highest level possible**, not optimized for one team's slice of it (the steel-company case: the client asked to evaluate a capital plan; the real problem was cash generation from an uncompetitive cost position one level up).

**Application to Northgate:**
- *Resolving the contradictory quotes:* Northgate's stakeholder quotes are not yet a MECE list — several describe the same underlying issue from different vantage points (VP: throughput; Head of Tax Risk: accuracy; EMEA manager: master-data quality; APAC analyst: invoice format compliance; Tax Tech: system fragmentation). Start with a **component tree** (what actually drives the $8–30M unrecovered figure: coding errors vs. bad master data vs. non-compliant invoices vs. missed reclaim windows vs. system fragmentation), then convert the highest-leverage branches into a **hypothesis tree** — each branch a testable claim about where the money is actually leaking — and use that structure, not stakeholder seniority, to decide which quotes to weight.
- *Structuring "is this a product":* the productization question is a **deductive/return-on-capital-style tree** — market size × penetration × price, with the "what you have to believe" framing forcing an explicit, defensible statement of the assumptions behind the opportunity-sizing arithmetic the brief asks for.
- *"Solve at the highest level":* the brief's own framing — pitch first, then step back and ask if this should be a product — mirrors the book's steel-company lesson: don't just solve Northgate's instance, ask whether the real problem (and real value) sits one level up, at the market level.

---

## Playing to Win (Lafley & Martin) — VERIFIED (read Chapter One, "Strategy Is Choice," via pdftotext)

**The strategic choice cascade.** Strategy is defined as five interlocking, iterative choices, each setting context for the ones below and getting refined by the ones above:
1. **Winning aspiration** — the purpose, "what does winning look like."
2. **Where to play** — which markets, customers, channels, geographies, product categories, vertical stage(s) — the set of choices that *narrows* the field. "No company can be all things to all people and still win."
3. **How to win** — the way you create and deliver unique value on that specific chosen field (not "how to win generally" — how-to-win only makes sense paired with a specific where-to-play; the book's Olive Garden vs. Mario Batali contrast makes this concrete).
4. **Core capabilities** — the map of activities/competencies that must be in place to win the chosen way.
5. **Management systems** — the systems and measures that support and sustain the capabilities and choices.

The book stresses this is **not a linear checklist** — it's an iterative cascade, and it nests: a company has a cascade at the corporate level, another within each business unit, another within each frontline role, each constrained by the ones above it.

**Application to Northgate:** Part 2 of the case ("is this a product?") maps directly onto the cascade:
- *Winning aspiration:* not just "sell software" — something like "become the system indirect-tax teams trust to find recoverable cash without adding audit risk."
- *Where to play:* the brief already asks for the first niche — size, geography, systems run, buying trigger, who to refuse — this is a where-to-play answer, and it should be narrow, not "all multinationals with indirect tax."
- *How to win:* differentiated not on "AI reads invoices" (commodity claim) but on the exception-handling/human-in-the-loop workflow and the information model that survives messy multi-SAP, multi-format reality — the same design choices the pitch itself has to defend.
- *Core capabilities / management systems:* what would have to be built (beyond the prototype) — connectors to fragmented SAP instances, a security/compliance posture that survives an 11-week vendor review repeatedly, and systems to keep the recoverability determinations auditable — is exactly the "what has to be true for this to be a product, not a series of custom builds" question the brief asks and says it will "push hardest" on.

---

## The McKinsey Way (Rasiel) — VERIFIED (read via full-text extraction of both epub sections; Part One "Thinking About Business Problems" and Part Three "Making Presentations")

**MECE.** Same "mutually exclusive, collectively exhaustive" discipline as Bulletproof Problem Solving — the book calls it "a sine qua non of the problem-solving process at McKinsey," applied to every issue list, every slide, every memo.

**The initial hypothesis (IH).** "Figure out the solution to the problem before you start." Build a top-line answer from the key drivers, structure it as an **issue tree** (branch out from the IH at each issue), then spend the engagement proving or disproving it with facts — "if your IH is correct, it will be the first slide in your presentation." The book is explicit that an IH is not always possible (when the client barely knows the problem, or the scope is too vague) — in that case, don't force one, just get the facts and let the structure emerge.

**The elevator test.** "Know your solution so thoroughly you can explain it clearly and precisely... in 30 seconds." The practical version: lead with the recommendation and its payoff (the top 2–3 issues with the biggest impact), not the supporting data — "we think you can boost X by Y% if you do Z. We can talk about the details later."

**Prewiring.** Before any big presentation, McKinsey teams walk every relevant player through the findings privately, one-on-one, so there are no surprises (and no ambushes) in the room on presentation day — "a McKinsey team will take all the relevant players in the client organization through their findings in private... otherwise it was just too risky."

**Application to Northgate:** structure the 10-minute pitch as an **issue tree built from an explicit initial hypothesis** ("we believe the $8–30M gap is driven primarily by X, secondarily by Y, and NOT primarily by Z — here's why we weighted the quotes that way"), lead each section with the elevator-test version of the answer before the supporting detail, and treat the pre-read to the VP as **prewiring** — surfacing the one uncomfortable point (that she's wrong about something) privately before the room, exactly the discipline the book describes, rather than springing it live.

---

## The Flawless Consulting Fieldbook & Companion (Block, 2nd ed.) — mixed: VERIFIED for resistance-handling; ASSUMED for the sponsor/contact/resistance taxonomy itself

Important caveat found during extraction: the physical book on the shelf is the **Fieldbook & Companion** (2nd ed., 2024) — a collection of contributed essays and case stories written as a companion volume, not the original *Flawless Consulting* (1981) that defines the client-system roles (sponsor / contact / resistance as a stakeholder taxonomy with specific tactics per role). The Fieldbook's own front matter says explicitly: "we have also framed this book as a fieldbook to go along with *Flawless Consulting*... the core skill in consulting is how to contract with your clients, and this is the heart of *Flawless Consulting*" — i.e., it assumes you already have the original book's model. So:

- **The sponsor/contact/resistance role definitions themselves (sponsor = holds authority/budget and can say yes; contact = day-to-day working relationship; resistance = a stakeholder expressing indirect pushback) — ASSUMED**, from general knowledge of the original *Flawless Consulting*, not confirmed against this specific text.
- **The technique for handling resistance and delivering an uncomfortable truth — VERIFIED**, read in full in Chapter 8, "Dealing with Resistance" (essay by Phil Grosnick): resistance is **"the indirect expression of real concerns"** — not something to overcome, something to surface. The method: (1) give a **"good faith response"** — answer the objection straightforwardly, with a real business reason, legitimizing the concern, but **cap it at two good-faith attempts**; (2) if resistance persists, **name the resistant behavior directly** ("You're yelling at me," "You're choosing a solution without data to back it up") — naming isn't the end, it's what starts the real conversation; (3) manage all **three levels of every meeting** — the content, the client's emotional reaction, and your own — using four guidelines: recognize the difficult conversation is the right one to be having, let go of the need to defend yourself, stay there to engage rather than win, and actually want to hear what the client has to say.

**Application to Northgate:** the Head of Tax Risk's flat "not enthusiastic" stance and her veto is textbook resistance-as-indirect-concern — her real objection ("wrong costs us more than slow") is already stated directly in the brief, so the job is to design the exception path *around* that stated concern rather than argue her out of it. For the VP — telling her "one thing she's wrong about" — the good-faith/name-the-behavior sequence gives a concrete script: state the business reason for the correction plainly and once or twice, then, if she pushes, name what's happening ("you've sold the CFO on headcount savings, and I don't think that's where the value actually is") rather than softening it into ambiguity. The sponsor/contact distinction (ASSUMED, not verified in this text) is still useful shorthand: the VP is the sponsor (budget, already sold it upward) but not the approver; the Head of Tax Risk holds the actual veto — so the pitch has to satisfy the person who can kill it, not just the person who invited you in.

---

## Claims for claims.md

| Claim | Status | Source | Notes |
|---|---|---|---|
| Bulletproof Problem Solving: logic tree types (component/factor, hypothesis, deductive, decision) and MECE discipline, used for disaggregating a problem before analyzing it | VERIFIED — confirmed against actual book text | Bulletproof Problem Solving, Ch. 3 "Problem Disaggregation and Prioritization" (epub, OPS/c03.xhtml) | Includes "what you have to believe" analysis via return-on-capital-style deductive trees |
| Bulletproof Problem Solving: problem statements should be outcomes-focused, specific/measurable, time-bound, and solved at the highest organizational level possible | VERIFIED — confirmed against actual book text | Bulletproof Problem Solving, Ch. 2 "Define the Problem" (epub, OPS/c02.xhtml) | Steel-company capital-plan case is the book's own illustration of "solve one level up" |
| Playing to Win: the five-part strategic choice cascade (winning aspiration, where to play, how to win, core capabilities, management systems), applied iteratively and nested at multiple org levels | VERIFIED — confirmed against actual book text | Playing to Win, Chapter One "Strategy Is Choice" (PDF, extracted via pdftotext) | Both copies of the PDF are identical; only one was opened |
| McKinsey Way: MECE, the initial hypothesis (IH) / issue tree method, the elevator test, and "prewiring" before big presentations | VERIFIED — confirmed against actual book text | The McKinsey Way (epub, index_split_000.html and index_split_001.html) | Book has no numbered chapter headers in the extracted HTML; content located by keyword search rather than table of contents |
| Flawless Consulting Fieldbook: resistance is "the indirect expression of real concerns"; handle it via capped good-faith responses, then directly naming the resistant behavior, while managing content + client emotion + own emotion | VERIFIED — confirmed against actual book text | The Flawless Consulting Fieldbook & Companion, Ch. 8 "Dealing with Resistance" (essay by Phil Grosnick) (epub, OPS/c08.xhtml) | |
| Flawless Consulting: the sponsor (authority/budget, can approve) vs. contact (day-to-day relationship) vs. resistance stakeholder taxonomy | ASSUMED — from general knowledge, not confirmed against this specific text | General knowledge of the original *Flawless Consulting* (1981/2011) by Peter Block | The book physically on hand is the 2nd-ed. Fieldbook & Companion (2024), a collection of contributed essays that explicitly assumes familiarity with the original book's model rather than restating it; the taxonomy itself was not found defined in this text during extraction |
