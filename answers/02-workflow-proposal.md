# Agent & workflow proposal (Part 1.2)

Status: not started. See `OUTLINE.md`, "Step: agent & workflow design," and `case-facts.md` §5 (which evidence documents the agent needs, and when) and §6 (four data sources, not three — the read-only assumption needs to be stated for all four, not just SAP).

To answer:
1. The agent(s) and the workflow stages, end to end.
2. Where exactly a human stays in the loop, and why there specifically — not "a human reviews it somewhere."
3. Who/what owns write-back to SAP or filing, since the agent never can (read-only, no writes, any version).
4. **The exception queue is urgency-weighted, not confidence-only.** A low-confidence case with years of reclaim-window runway can wait for review; a high-confidence case with weeks of runway left (per the time-to-expiration attribute in `answers/03-information-model.md`) needs to jump the queue regardless of confidence — otherwise it expires while sitting in a review pile that was prioritized the wrong way. See `case-facts.md` §4 for why this isn't hypothetical: Italy and India's windows can be single-digit months for a late-in-year invoice.
