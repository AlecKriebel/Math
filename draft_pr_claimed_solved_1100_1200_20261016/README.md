> Superseded on 17 October 2026: the user directed inspection of actual PR outcomes because QUEUE.md may be stale. The queue-only skip decision does not determine the current processing scope. See ../draft_pr_actual_claims_1100_1200_20261017/ for the corrected active program.

# Draft PR claimed-solved publication program, #1100–#1200

Process PRs in ascending order from #1100 through #1200 inclusive. Only open
draft PRs whose current problem status in `unsolved_math_prioritization/QUEUE.md`
is exactly `claimed_solved` are eligible. Every other status is skipped without
mathematical review, priority audit, repair, comment, closure, merge, or paper
preparation. Compare the workspace queue, a pinned remote-main queue, and
each draft's own queue row. A disagreement must be resolved before any
mathematical processing or final skip decision.

For eligible PRs, require rigorous mathematical reproduction, extensive
independent adversarial review, priority audit of the original full problem,
and a submission-ready preprint and verification package. Review and fix the
package with fresh subagents until no actionable issues remain. Disclose
extensive AI use and the actual peer-review status. Publish with the repository
Zenodo kit, add the verified DOI and paper details to the specified tracker
through the Google Workspace CLI, and merge accepted PRs. Reasonably attempt
repair before closing any irreparable in-scope claim with an explanation.

All program artifacts live here. Stay on `main`, checkpoint with timestamps
and completion estimates, preserve other agents' work, and contact no
individuals or other shard agents. Percentages measure completion of this
bounded processing pass, not confidence in mathematical claims.

Reproduce the saved status gate with `python3 verify_status_gate.py` from this
folder. Its inputs are PR metadata and the two saved queue snapshots. It does
not open PR mathematical reports or change external systems.

The pass is complete: all 101 drafts have status exactly `queued` in the workspace, pinned remote main, and pinned PR-head queue rows. All were skipped. Independent adversarial verification found no actionable issues. See `DISPOSITION.md`, `DISPOSITIONS.json`, and `reviews/status_gate_01/REVIEW.md`. No mathematical result is accepted by this status-only pass.
