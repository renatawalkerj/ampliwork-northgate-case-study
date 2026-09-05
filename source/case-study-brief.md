Ampliwork Senior Product Manager Case Study
Northgate Industries
Session
15 minute presentation, then 15 minutes of questions
Deliverables
A deck of 12 slides or fewer, a working prototype demoed live, and a one page email. Appendix optional and uncapped.
Send by
End of day Thursday, September 10
Before you start
	•	Use AI tools freely. We do, at every hour of the day. Build the prototype however you like. Tell us what you used, where it helped, and where it led you astray. We are more interested in that than in a clean story.
	•	The brief is deliberately incomplete and partly contradictory. So is a first call. Decide what to believe, state your assumptions on one slide, and move.
	•	Fifteen minutes is a hard cap. Ten minutes on the pitch, five on the product question. Everything will not fit. Choosing what to present, and what to leave in the appendix for us to ask about, is part of what we are assessing.
	•	We will interrupt, and we will change something. Clients do. At the start of the questions we will alter one fact about the situation and give you 30 sec to say what changes in your plan. You cannot prepare for it. That is the point.
	•	We are evaluating how you think, not how you decorate slides. A recommendation beats a survey of options. Clarity beats polish.
The situation
Northgate Industries is a multinational industrial manufacturer. Around 14 billion dollars in revenue, operations in 30 countries, 38,000 employees. The global tax function is about 120 people, of whom 24 sit in indirect tax across three regional hubs in Chicago, Rotterdam and Singapore.
That team is responsible for value added tax, goods and services tax, and sales and use tax across every jurisdiction Northgate operates in. Every month they work through hundreds of thousands of accounts payable transactions, deciding three things for each one: whether tax was charged correctly, whether it is recoverable, and where it should be reported. Wrong in one direction leaves cash on the table. Wrong in the other creates audit exposure and penalties.
The evidence is supplier invoices in fourteen languages, purchase orders, goods receipts, contracts, customs paperwork and credit notes. It lives across three SAP instances inherited from acquisitions, a tax engine, a shared mailbox where suppliers send queries, and a set of regional spreadsheets nobody will admit to relying on.
Two clocks run. Filing deadlines are monthly or quarterly depending on the jurisdiction. Separately, each jurisdiction has a window in which a reclaim can still be made, typically three to four years, after which the money is simply gone.
Northgate believes it leaves somewhere between 8 and 30 million dollars a year unrecovered. Nobody inside the company agrees on the number, and the width of that range is itself part of the problem. Last year it also paid roughly 4 million in penalties and interest across two jurisdictions for incorrect filings.
Two people matter in the room. The VP of Global Indirect Tax is your sponsor, holds the budget, is enthusiastic, and has already presented this to the CFO. The Head of Tax Risk, who signs the returns, is not enthusiastic. She carries the exposure on every filing that goes out.
Their stated ask, from the first call: "can you build us an AI that reads our invoices and tells us the right tax treatment?"
What we heard on the discovery call
Verbatim, in the order it came up. Nobody has reconciled these with each other.
Who | What they said
VP, Global Indirect Tax (your sponsor) | "If AI codes the invoices, I free 24 people to do analysis instead of data entry. That is the whole business case."
Head of Tax Risk, signs the returns | "We paid four million in penalties and interest last year on returns that were filed on time and wrong. I care far more about wrong than about slow."
Regional tax manager, EMEA, 9 years | "Coding is not the hard part. A third of our supplier master data is wrong. The same supplier exists as three vendors with three different tax profiles, and no model fixes that."
Analyst, APAC | "Most of my month is chasing suppliers for compliant invoices. A lot of what we cannot recover is because the invoice does not meet the local format rules, not because anyone coded it wrong."
Head of Tax Technology | "Three SAP instances from acquisitions. They will not be consolidated before 2029. Whatever you build has to live with that."
Enterprise security | "Nothing leaves our tenant. And you go through the vendor security review like everyone else. It runs about eleven weeks."
VP, Global Indirect Tax, later in the call | "The board is asking about working capital. I need a number I can defend by the year-end close."
Constraints
These are not negotiable. A proposal that ignores one of them is not a proposal.
	•	Two engineers plus you. Eight weeks to something the team can use.
	•	The vendor security review takes about eleven weeks, and it starts when you sign. Work out what that means for the eight.
	•	No data leaves Northgate's tenant.
	•	Read access to SAP. No writes, in any version.
	•	Three SAP instances. They are not being consolidated.
	•	The year-end close is a fixed date.
	•	The Head of Tax Risk has a veto. Nothing ships without her.
What we are asking you to do
One story with a turn in it. You pitch Northgate, then you step out of that room and tell us what you really think.
Part | What you produce | Time
1. The pitch | The proposal you would take into the second meeting with Northgate, with the prototype demoed live inside it | 10 minutes, max 8 slides
2. Is this a product? | Step back out of the client conversation and tell us whether we should take this to market | 5 minutes, max 4 slides
Pre-read | The follow-up note you would send the VP of Global Indirect Tax after the meeting. Sent with the deck, read by the panel beforehand | One page

Part 1. The pitch, 10 minutes
Present this as you would to Northgate, with the prototype demoed live inside it, where a client would see it. Cover:
1. What you believe is actually happening at Northgate, and how you got there. The quotes above do not agree with each other. Say which you weighted and why.
2. What you propose. The agent or agents, the workflow, and where a human stays in the loop and why there.
3. The information model. What a legal entity, a jurisdiction, a supplier, a transaction, an invoice, a recoverability determination, a filing period and a reclaim are in Northgate's world, and how they relate. Name what you leave out of version one, and what breaks if you get this wrong.
4. The prototype, live. A working version one of the most important flow. Not screenshots. Up to three minutes, inside the ten.
5. Phasing, timeline and pricing logic against the eight weeks, the eleven week security review and the year-end close. What Northgate gets at the end of each phase, and what each phase asks of them. Logic, not exact numbers.
6. One thing the VP of Global Indirect Tax is wrong about, and how you would tell her. She has already presented this to the CFO.
The prototype, in more detail
	•	It must handle one awkward input, not the clean case. An invoice that does not meet the local format rules, a supplier that exists three times under different tax profiles, a field that is missing entirely.
	•	It must show the exception path. What happens when the agent is not sure. That path matters more here than the happy path, because of who holds the veto.
	•	Low fidelity is fine. Ugly is fine. Working is not optional. Build it however you like, including with AI tools.
	•	Be ready to say one thing you chose not to build and why, and one thing that surprised you while building it.

Part 2. Is this a product? 5 minutes
Stop pitching. Every large multinational with an in-house indirect tax function has a version of this problem. Tell us whether we should productize what you just proposed, and back it.
1. Your recommendation, in one sentence, on the first slide.
2. The first niche if you say yes. Size, geography, systems they run, buying trigger, and who you would refuse to sell to.
3. Rough size of the opportunity, with arithmetic you would defend in front of a sceptic.
4. Packaging and pricing logic, and how a pilot converts into something recurring.
5. What has to be true for this to be a product and not a series of custom builds. We will push hardest here.
The pre-read
One page. The follow-up note you would send the VP of Global Indirect Tax the evening after the meeting, before anything is signed. Send it with the deck. The panel reads it beforehand, and we are reading it as a writing sample, so write it the way you would actually send it.
How the session runs
	•	Ten minutes on the pitch, five on the product question. We will hold both marks.
	•	We will interrupt during the pitch. Clients do. Handle it however you would handle it in the room.
	•	Then fifteen minutes of questions, opening with a change to the situation. You will get three minutes to tell us what changes in your plan. You cannot prepare for it, which is the point.
How we will evaluate this
	•	Thinking. Do you work out what is really going on, or do you take the order? Can you hold a position, and change it out loud when the argument is good?
	•	Business acumen. Where the money is, what they are really buying, and what has to be true for the case to hold.
	•	Prototyping. Something real, built fast, that survives contact with a messy input.
	•	Communication. Fifteen minutes, decisions rather than description, in a room that talks back. Plus the written note.
	•	Composure. We will push. Defend what you believe, update when you should, and say you do not know when you do not. All three are good answers. Bluffing is not.
Practical notes
	•	Northgate Industries is fictional. The shape of the problem is not.
	•	Do not email us for clarifications on the content. Deciding what to do with an incomplete brief is part of the exercise. Logistics questions go to Roxane.
