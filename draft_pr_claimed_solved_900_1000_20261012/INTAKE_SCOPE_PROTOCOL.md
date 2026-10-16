# Controller scope and transition protocol

The frozen per-result finalization helpers propose a next PR through metadata
and immutable-head QUEUE status only. A proposal is not mathematical intake.
The root controller must perform the following checks before reading the next
problem's statement, proof, prior report or artifacts.

1. Finish the current result's actual DOI/files, Google CLI exact row, native
   ledger and final PR metadata readbacks. Preserve that result's complete
   publication record under its dedicated audit folder and in completed_results.
2. Remove any remaining previous-target-only convenience fields from the global
   CURRENT_STATE before attributing details to a newly selected target. In
   particular, later-added merge/draft/operator/reconciliation/readiness/clean
   review fields may not be carried into another target. Their authoritative
   receipts remain in the previous target's own folder; do not erase history.
3. Obtain current PR metadata again. Require an OPEN draft in900..1000. At its
   exact immutable head, use current_identity from
   resweep_draft_statuses_900_1000.py. Initial inventory identity may be reused
   only if the head is exactly unchanged. A changed head needs current PR
   filename metadata identifying exactly one numeric attempt ID. Ambiguous or
   missing identity prevents intake; do not infer an ID from an unrelated row.
4. Read only that exact head's QUEUE status and require literal claimed_solved.
   Every other status is a status-only skip: no statement, math, audit, repair,
   paper, merge, close or comment. Save the metadata/status/identity receipt.
   If the proposal was stale, correct only the controller's own metadata state
   and continue ascending. A later actual-head change requires a new gate.
5. Only after this successful scope gate create/fill the dedicated new audit
   folder and authenticate the immutable PR files and complete selected source.
   Continue independent math, priority and adversarial publication workflows.

After the ascending range, run the separate whole101-PR metadata/status sweep,
with its before/after metadata stability check and changed-head identity
reconciliation. Process any newly eligible drafts rather than treating the
initial inventory as permanently authoritative. Unstable/unknown identities
prevent claiming scope completion. Independently verify all own completed
outcomes before marking the persistent goal complete. Neither an unchanged
initial skip nor a stale next-target proposal overrides a current exact
claimed_solved gate.

This protocol adds controller scope checks and honest state transitions; it
does not alter any frozen scientific package, source, old review, approval or
external record. It also does not authorize processing any nonclaimed status.
