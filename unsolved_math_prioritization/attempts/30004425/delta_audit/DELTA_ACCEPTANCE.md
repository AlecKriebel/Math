# Delta acceptance: 30004425

Audit date: 5 October 2026.

## Verdict: PASS for the corrected publication package

Both required corrections from the initial independent audit are fixed. The corrected package is accepted as a qualified prior-results/source-curation finding, with publication disposition **unsolved, 1/5**. This acceptance does not certify a new theorem, new counterexample, unrestricted semigroup classification, or universal resolution.

The original author freeze and original independent audit remain unchanged. Their historical REVISE_REQUIRED/pending language records their respective snapshots; this separately bound acceptance closes the two specified corrections for the exact corrected bytes below. No remote write was made.

## Exact accepted inputs

- Corrected author archive: `TROPICAL_WALL_30004425_CORRECTED_SAFE_FREEZE.zip`; 25,136 bytes; SHA-256 `a53534d916ae974461131d47fab6589d80bfc1799ecffad4c6b3f56691d303c8`.
- Corrected MANIFEST.json: 1,500 bytes; SHA-256 `bd3994c0ff3a51c3695135291206af0e50455c461a482f1738b0939fe3eb5a82`.
- CORRECTIONS.diff: 9,236 bytes; SHA-256 `ae6cd7dd45c4192d050fb123d7de6c81f881504557bfaf854fe5c88f9cdd2407`.
- PUBLICATION_SCOPE.md: 3,288 bytes; SHA-256 `43e8e239cda32ecd0a01bd97419ddae3226b2dc31774db5303f02e206efd2f0d`.
- Original author archive: 17,849 bytes; SHA-256 `8297f9480c92cf9a736468cfeefc008b62a04b7e4674c8851b9e72fb6c99a446`.
- Original independent-audit MANIFEST.json: SHA-256 `a52431e654bd7354f89867de09c823a3b0010768cb9ad1c3a4a35f253097e413`.

Every ZIP member agrees byte-for-byte with its corresponding frozen file. The corrected ZIP contains exactly eleven files, and its manifest verifies all ten non-manifest files.

## Required corrections and bounded change set

1. REPORT.md differs only by replacing the incorrect finiteness terminology with “finitely generated semigroups.” No theorem statement, example proof, or formula was otherwise changed.
2. SOURCE_VERIFICATION.json now records complete queue-byte verification: 389,371 bytes, Git blob `483de6795be8c12bacc3d18e1ef04900eddedf04`, and SHA-256 `6b37d1112c4223ae1c39156a98a745389112a7b129080dcd3a6439c334ebf2c2`. Both the queue entry and the corresponding retrieval-history entry correctly identify the old header as stale literal file content. Neither calls for a queue repair.

The other source-metadata changes are limited to the check timestamp, historical audit-state description, and qualified unsolved/1-of-5 publication disposition. A structural JSON comparison verifies that all remaining fields are unchanged.

The only changed original files are REPORT.md, SOURCE_VERIFICATION.json, and the regenerated MANIFEST.json. The only additions are PUBLICATION_SCOPE.md, CORRECTIONS.diff, and CORRECTION_RESULTS.json. The diff is an exact independently regenerated unified diff for the declared prose/metadata changes and added scope statement. The manifest and correction-results receipt separately describe their bookkeeping roles; they are not represented as part of that prose diff.

EXACT_CONTROLS.md, verify.py, VERIFICATION_RESULTS.json, verify_manifest.py, and README.md are byte-identical to the original author freeze. Thus every retained example-specific proof and all executable mathematical code remain exactly as previously audited.

## Source clarifications checked

The added scope statement was read in full and compared with the already independently retrieved and hash-verified [Escobar–Harada v2](https://arxiv.org/abs/1912.04809v2): equation (2.4), the choices immediately before Theorem 2.7, and Lemmas 3.7–3.8.

- The common rows belong to the shared face, are independent and integral, and include the degree row. Complementary rows are taken in their respective cones under the cited integral-row setup; their sums with the common rows lie in the relative interiors. The matrix orientation is correct. This does not authorize arbitrary vectors chosen merely on opposite sides of a wall.
- Reversed comparison of the degree coordinate followed by ordinary lexicographic comparison of the remaining coordinates agrees with equation (2.4). Initial forms use the minimum convention. Homogeneity makes the degree reversal harmless for comparisons among terms of the defining homogeneous polynomial.
- For the vertical rank-one subgroup of the generated value lattice, division by its positive generator gives the appropriate normalized length. Those normalized fiber lengths agree, while ordinary coordinate lengths satisfy L2 = kappa L1. Last-row rescaling changes ordinary lengths. In the original example both column groups are Z^3 and the scale is one. These statements agree with the source normalization argument and previously verified example.

These are accurate source clarifications, not additional universal existence assertions. The unchanged normality, saturation, common-Gröbner-cone, and nonadditivity boundaries remain in force.

## Replayed checks

- Original author manifest: PASS, seven covered files.
- Corrected author manifest: PASS, ten covered files.
- Original independent-audit manifest and independent arithmetic replay: PASS.
- Corrected author arithmetic: PASS; output byte-identical to both the corrected and original saved result.
- Four isolated code mutations: all rejected at mathematical assertions, covering the second-matrix sign, standard reduction, standard cutoff, and flip orientation.
- Exact diff regeneration, metadata change allowlist, additions/removals, archive membership, and correction receipt: PASS.

Run `python3 verify_delta.py ORIGINAL_FREEZE CORRECTED_FREEZE ORIGINAL_INDEPENDENT_AUDIT` to reproduce the exact delta checks. DELTA_RESULTS.json records the complete check results and pins. The source-reading judgments above remain mathematical review rather than formal proof-assistant certification.

This acceptance is limited to the pinned corrected package. It does not authorize broader edits or remote publication actions and does not alter the original audit's mathematical scope. The delta package contains only authored audit material, code/results, and public verification metadata.
