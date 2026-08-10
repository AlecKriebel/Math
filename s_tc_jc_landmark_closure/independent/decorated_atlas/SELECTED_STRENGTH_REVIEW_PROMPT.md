> Historical prompt preserved for reproducibility. Its use of “selected
> strength” was too broad; the active certified predicate is only
> `selected_retains_strong_core`, not intrinsic selected `S_TC` after arbitrary
> reduction.

Act as an adversarial independent reviewer of the selected-strength correction
in this directory. Work read-only. First read
`../../docs/DEFINITIONS_LOCK.md`, `PRECORRECTION_FAILURE.md`,
`SELECTED_STRENGTH_CORRECTION.md`, `selected_restrictions.py`,
`build_atlas.py`, and `verify_contract.py`.

Do not import or execute `selected_restrictions.py` for your independent
count. Using only Python's standard library in a scratch command, independently
derive or audit:

1. whether the five contracted cycle/theta directed cores are exhaustive;
2. whether their minimum repair sizes are `1,1,2,2,2`;
3. whether selected strength is exactly all sink ports selected plus selected
   ordinary occupancy containing a minimum repair;
4. whether a dummy in one chosen completion can coexist with a selected-strong
   restriction;
5. the completion counts and old/new strength buckets for selected counts
   3,4,5,6;
6. whether existing fully selected primitive T-relation counts should change;
7. whether the pre-correction failure is honestly described and preserved.

Seek a counterexample, especially a false-strong or a mismatch between the
repair predicate and direct graph `S_TC`. Distinguish completion target rows
from complete decorated source-target relations. Return ranked findings and
one verdict: ACCEPT_CORRECTION, ACCEPT_WITH_LIMITATION, or REJECT_CORRECTION.
Do not assess the global identifiability theorem.
