# How we built this

Status: not started. Draws on `claims.md` and `extras-rationale.md`.

Answers the brief's own ask directly: "Use AI tools freely... tell us what you used, where it helped, and where it led you astray." Include:
1. Tools and process used (PIL for claims discipline, Build Engine for the prototype build) — the claims ledger itself as evidence, not just a description of it.
2. Where AI assistance helped.
3. Where it led us astray, and what we did about it.
4. **The prototype's model choice, stated as a deliberate build decision, not a production recommendation.** The demo runs on Gemini's free tier (public API) — fast and free to build against, and appropriate here because the demo uses synthetic data we built ourselves, not real Northgate data, so the tenant-isolation constraint doesn't apply to it. This is separate from and doesn't imply the production recommendation (`answers/02-workflow-proposal.md`): in production, this same logic runs on Azure OpenAI Service, confirmed, provisioned privately inside Northgate's own Azure subscription — never the public API used here. Ready if asked why: the public API would fail the "nothing leaves our tenant" test on real data; it's fine for a synthetic demo built in a few hours.
5. **Evals as a first-class deliverable, not an afterthought.** The prototype's synthetic data carries ground-truth expected values, scored against 7 named metrics, with an eval-and-refine iteration loop documented before any code exists (`prototype/evals/eval-plan.md`) — precise about what it is (prompt/threshold iteration against measured results) and isn't (weight-level fine-tuning, which the free-tier build has no budget for, consistent with the same constraint already named for production).
