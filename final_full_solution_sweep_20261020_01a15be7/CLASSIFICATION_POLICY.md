# Sequential classification rules

1. The final cursor advances only after a per-PR disposition is recorded. Metadata
   collection ahead of that cursor is not final classification or mathematical
   acceptance. Unknown fields, absent patches and ambiguous row correspondence
   remain unresolved rather than becoming exclusions.
2. A corresponding changed QUEUE row supplies the PR's historical explicit status.
   Preserve that status even when a later accepted audit changed it. Match the
   problem identifier and provenance; an unrelated added table row is not the
   PR's own status.
3. A later explicit canonical `already_solved`/`unsolved` classification that
   identifies this PR, together with its current description withdrawing the
   novel full-solution claim, supersedes a historical `claimed_solved` patch.
   Record both states and the published-coverage check. This follows the user's
   instruction to skip explicitly non-claimed-solved problems. An untouched
   generic `queued` main row alone cannot exclude a missing-status PR.
4. When there is no usable corresponding status, inspect the current PR's actual
   claim, changed proof/report files and limitations. Do not infer a complete
   solution merely from words such as "prove", "counterexample", or "solution".
   Conversely, an absent QUEUE edit, merged state or draft label cannot exclude
   a complete solution. These cases require an explicit reasoned classification.
5. Check the live GWS ledger before substantive candidate work. Compare the
   original problem/aliases, exact mathematical result and hypotheses, title,
   PR references, and DOI/publication evidence. Title or identifier matching
   alone is only a lead. A matching already-published, correctly recorded result
   is skipped entirely; a defective record is reconciled rather than republished.
6. No new mathematical correctness, priority or novelty conclusion follows from
   an old audit label. Any remaining eligible, unpublished full-solution claim
   receives the full independent audit and fresh package-review workflow.
7. Recheck live heads/base/main, publication state and ledger immediately before
   an irreversible action. No package is cleared while a material objection or
   unexplained duplicate remains.
