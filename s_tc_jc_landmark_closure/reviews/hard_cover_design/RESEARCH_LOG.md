# Hard Cover Design Research Log

Scope: `reviews/hard_cover_design/` only.  No primary files were edited.  No
external contact was made or prepared.

## 2026-08-09 23:31 PDT

Checkpoint: 35% complete.

Recorded byte hashes for the audited sources, especially
`primary/hard_cover_compiler.py`.  The repository is not on `main`; per the
user's explicit instruction this review will not commit or push and will leave
the branch/worktree state untouched.

## 2026-08-09 23:44 PDT

Checkpoint: 65% complete.

Reconstructed the restoration recursion.  The implementation restores dummy
roles in sorted order, assigns the next fresh label, and inserts that label in
every source segment position while carrying the extended source words forward
recursively.  This is enough to enumerate prefixes of one fixed full labelled
relation, provided that the restored target dummy roles are actual boundaries
of that same full relation.

Found the main adversarial distinction: restoration is not a valid
unconditional lift of a selected marginal containment.  Added the exact
two-polynomial counterexample in
`counterexamples/unconditional_lift_failure.json`.

## 2026-08-09 23:58 PDT

Checkpoint: 90% complete.

Status-labelled every requested design claim in `claims.json`.  The strongest
verified result is conditional fixed-full relation exhaustiveness.  The
stronger selected-marginal lift claim is false.  Finite-union promotion and
cross-probe/full-relation artifact binding remain unresolved in the compiler
artifact design.

## 2026-08-10 00:08 PDT

Checkpoint: 100% complete.

Added `structural_audit.py`, `make_manifest.py`, and `verify_all.sh`.  The
verifier imports no primary module and does not inspect hard-cover census
output.  It checks audited source hashes, static design hooks, claim labels,
and the exact counterexample.
