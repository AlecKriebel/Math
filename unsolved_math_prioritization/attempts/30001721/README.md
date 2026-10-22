# Problem 30001721: tree modules for roots of acyclic quivers

**Status: unsolved. Five substantive approaches.** This investigation supplies valid auxiliary proofs and exact finite controls, not a proof or counterexample to the universal existence question.

Start with the [corrected report](release-v2/author/REPORT.md) and [source audit](release-v2/author/SOURCES.md). The [complete original independent audit](release-v2/original-audit/AUDIT_REPORT.md) accepted the mathematics and requested one metadata correction. The [supplemental acceptance](supplemental-audit-v2/SUPPLEMENTAL_ACCEPTANCE.md) verifies that correction and accepts the exact corrected release.

The C1 fix names cache counts `algebra_cases_evaluated` and reports whether the basis-permutation quotient was used. Mathematical findings and counts are unchanged. The corrected release, original author packet, original audit, and supplemental audit are preserved in full. Historical statements such as “pending review” remain in frozen files and are superseded by the separate supplemental acceptance for its exact bound hashes.

The positive controls include a real non-Schur affine-D4 tree module with dual-number endomorphism algebra. Exact enumeration finds 96 indecomposable supports among 8,748 labelled affine-D4 trees. Labelled supports, basis-permutation orbits, and isomorphism classes are different counts.

## Portable final-layout checks

Requires Python 3 and SymPy 1.14.0 for the mathematics scripts. The strict manifest checker uses only the standard library:

    python verify_manifests.py
    python release-v2/author/verify_tree_controls.py --extended-control --output /tmp/corrected-tree-replay.json
    cmp /tmp/corrected-tree-replay.json release-v2/author/control_results.json
    python release-v2/original-author/verify_tree_controls.py --extended-control --output /tmp/original-tree-replay.json
    cmp /tmp/original-tree-replay.json release-v2/original-author/control_results.json
    python release-v2/original-audit/independent_controls.py --output /tmp/independent-tree-replay.json
    cmp /tmp/independent-tree-replay.json release-v2/original-audit/independent_results.json

Final-layout replay outputs are in `publication-validation/`. The independent implementation enumerates all 8,748 affine supports without an orbit cache. The manifest checker requires exact inventory and hashes, rejects unsafe paths and symlinks, and exercises nine isolated negative controls. Archived verification scripts are preserved verbatim; the commands above and the new manifest checker are the portable entry points.

The publication changes only this attempt directory and this problem's queue Status/Turns cells to `unsolved` and `5/5`. No Findings value or mathematical solution claim is added.
