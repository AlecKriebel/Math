# Conditional literal noisy consistency established

Corrected release v2 for problem 30003790 / OWR-16161-003.

The independently accepted safeguard establishes expected integrated squared-error
consistency and sample-conditional integrated-risk convergence in probability for
arbitrary Borel designs in fixed finite dimension, under bounded continuity of the
regression function and conditionally centered noise with a common finite conditional
second-moment bound. The full construction and explicit independence/selection
requirements are in `public/RESULT.md`, Section 5A.

Coverage of the underspecified original model has not been established. Conservative
queue disposition remains `unsolved`, 5/5. Dimension-efficient geometric rates are
separately unproved, not an extra condition in the literal source question. No novelty
is claimed; Stone (1977) is credited for longstanding generic regression consistency.

## Start here

- `FINDINGS.md`: the affirmative result and exact remaining scope gap
- `public/RESULT.md`: corrected original results and complete current model statement
- `public/AUXILIARY_THEOREM.md`: exact accepted proof, unchanged
- `CHANGE_LEDGER.md`: explicit correction and stale-status supersession record
- `AUTHOR_V1_TO_CORRECTED_V2.diff`: exact changes to the author packet
- `history/`: unchanged author freeze and both unchanged independent audit packets
- `VERIFY_RELEASE.py`: manifest, historical preservation, exact-diff and replay checks

The historical candidate's not-yet-audited banner is preserved to avoid rewriting
history. It is superseded by the fresh acceptance bound to its exact SHA256 in
`history/auxiliary-independent-audit/AUDIT.md`. The corrected assembly itself awaits
release-binding review. This is a prepared release, not a published result; no remote
write has been made. Third-party PDFs, full texts and private inventories are excluded.

Run `python3 VERIFY_RELEASE.py` from this directory to check the complete assembly.
