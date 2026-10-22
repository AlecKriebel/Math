# Conditional literal noisy consistency established

Problem 30003790 / OWR-16161-003. Audited corrected research checkpoint.

The accepted safeguard establishes expected integrated squared-error consistency
and sample-conditional integrated-risk convergence in probability in each fixed
finite dimension, for arbitrary Borel designs with bounded continuous regression
function and conditionally centered noise with one common finite conditional
second-moment bound. All-candidate ranking, independent label use, deterministic
ties and joint test independence are explicit. No novelty is claimed; generic
regression consistency is credited to Stone (1977).

- [Findings and limitations](release-v2/FINDINGS.md)
- [Corrected results and explicit model](release-v2/public/RESULT.md)
- [Exact accepted auxiliary theorem](release-v2/public/AUXILIARY_THEOREM.md)
- [Supplemental acceptance of this corrected assembly](release-v2-binding-audit/ACCEPTANCE.md)
- [Correction and historical-status ledger](release-v2/CHANGE_LEDGER.md)

Conservative queue disposition is `unsolved`, 5/5, because full coverage of the
underspecified original model has not been established. This does not negate
the affirmative bounded-model consistency result. Dimension-efficient geometric
rates are a separate unproved objective, not an added condition in the source.

## Publication packaging and status supersession

The 44-file corrected release and six-file supplemental acceptance packet are
copied byte-for-byte into the two sibling directories above. No mathematical
or portable-reference edits were made. The release's frozen binding-pending
and not-yet-published statements describe its preparation stage. Supplemental
PASS supersedes the binding-pending state for that exact manifest. Publication
of this package as a draft pull request does not alter those historical records
or imply a merge, formal peer review, unrestricted source resolution or novelty.

`PUBLICATION_MANIFEST.json` binds this wrapper, the portable verifier and all
50 accepted files. Downloaded source PDFs, extracted full texts and private
inventories are excluded. Run `python3 VERIFY_PUBLICATION.py` from any directory
to verify the inventory, exact accepted manifests, supplemental binding and
recorded control replays.
