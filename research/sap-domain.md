# SAP technical domain briefing — fast pass

Status: not yet researched (Breakpoint A).

Covers: multi-instance SAP + tax engine (Vertex/ONESOURCE/Avalara-type) integration patterns, what read-only access actually constrains. Feeds the workflow proposal and the information model directly — these entities have real SAP/tax-engine analogs, don't invent them from scratch.

Also needed:
- SAP vendor/supplier master data structure — how the same real-world supplier ends up as multiple vendor records (e.g. one per company code/hub) with different tax profiles. This is exactly EMEA's "3 vendors, 1 supplier" complaint — directly informs the info model's supplier entity and its dedupe/identity question (`answers/03-information-model.md`).
- How existing tax-tech/AP-automation tools (Vertex, ONESOURCE, AppZen, Vic.ai, similar) implement confidence-based human-review queues / exception routing — feeds the workflow proposal's human-in-the-loop design (`answers/02-workflow-proposal.md`), so it's grounded in how this is actually done, not invented.

Output shape: a short list of real sources + a condensed brief.
