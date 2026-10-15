# Working through the research queue

This supplements the repository's Independent Research Policy and Research Workflow.

- Read `README.md`, `QUEUE.md`, and the selected record's complete source statement and prior report before an attempt. Scores and desk notes are hypotheses, not proof certificates or novelty guarantees.
- Use the numeric upstream ID. Keep each attempt in `attempts/<id>/`, including a timestamped research log, exact claim, source checks, proof artifacts, independent challenges, and completion estimates.
- Check the exact full target, current literature, related records, and `review_v2/related_target_groups.json`. Resolve readiness holds with evidence. Do not replace a bundled target with an easier special case without defining a separate problem.
- Each distinct target gets at most five substantive proof-attempt responses. Record every such response with `queue.py turn`, including unsuccessful attempts. Tool calls are not separate turns. Source triage is not a way to hide fresh proof work outside the budget.
- Use `turn --outcome candidate` only when a complete candidate artifact has been saved within those five turns. Independent verification may check it afterward, but must not become extra search turns for an unfinished proof.
- If the fifth turn is unfinished, keep the automatic `exhausted` status and move to the next target. Do not reset counters or bypass status gates.
- Update related targets after a shared lemma, counterexample, or obstruction. Distinct formulations are not automatically independent discoveries.
- Preserve every review and correction. Use `assess` for later assessments; do not edit historical `review_v2/reviews_*.json` or replay a historical merge over newer work. New source content requires a fresh individual review.
- Regenerate the queue after status or assessment changes; the commands do this automatically. Commit and push meaningful checkpoints on `main` in accordance with the repository policy. Do not contact outside individuals or create a GitHub release for routine progress.
