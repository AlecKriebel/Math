# Acceptance report for the prior negative result

**Disposition: VERIFIED PRIOR NEGATIVE.** The published Myroshnychenko–Tatarko–Yaskin counterexample, reconstructed explicitly in dimension five, falsifies the universal n ≥ 3 centroid-section lower bound. The mathematical result belongs to Sergii Myroshnychenko, Kateryna Tatarko, and Vladyslav Yaskin. This report makes no novelty claim.

## Accepted sufficient claim

There exists a compact convex body K in R⁵ with nonempty interior and ordinary volume centroid zero for which exactly one distinct unoriented affine hyperplane has a section with centroid zero under ordinary induced four-dimensional Euclidean measure.

The reconstruction verifies global convexity, positive radius, smoothness of the equatorial division, exact centering without translation, a strictly positive fifth section moment in every nonexceptional direction, and the entire centroid vector of the remaining section. That exceptional section is an origin-centered four-ball. The opposite normals ±e₅ count as one hyperplane. One is fewer than the proposed six.

The full proof is [MTY_DIMENSION5_VERIFICATION.md](mty/MTY_DIMENSION5_VERIFICATION.md); the independent check is [MTY_GEOMETRY_AUDIT.md](geometry/MTY_GEOMETRY_AUDIT.md). The geometry cross-review receipt pins the exact full-proof bytes and reports no mathematical correction requested. The public reader preserves those bytes unchanged.

## Explicit repairs and their limit

The inspected author manuscript arXiv:2404.15188v2 has two local statement inaccuracies:

1. Equation (5)'s complementary-homogeneity formulation does not imply its displayed equality. The actual applications need same-degree −1 self-adjointness. The reconstruction proves that replacement through a symmetric spherical-Radon identity and its smooth inverse.
2. The inverse-radius comparison on the equator is non-strict. The seed's proved positive lower bound suffices for the construction.

Neither issue invalidates the counterexample. The reconstruction additionally makes the smooth quotient and exact parameter-continuity steps explicit. These are authored verification and repair arguments, credited to the prior construction.

The published journal's identity is verified, but its PDF bytes were not recovered or inspected. These observations do not allege that the uninspected journal text contains either statement. No author/publisher byte identity is asserted.

## Supplementary acceptance

The [WXY reconstruction](wxy/WXY_RECONSTRUCTION_AUDIT.md) and [independent supplementary audit](geometry/WXY_SUPPLEMENTARY_GEOMETRY_AUDIT.md) accept the main construction in the 31 July 2026 three-author version arXiv:2606.19865v2. It supplies examples in every n ≥ 3, including n = 3 and n = 4. This result belongs to Shouda Wang, Ge Xiong, and Kaiwen Yang and remains a submitted-preprint result under the checked public status.

Its explicit analytic prerequisites include standard spherical harmonic decomposition, Funk–Hecke, compact-sphere Sobolev theory, and elementary differential calculus. The pivotal transform normalization, exact phase cancellation and first moment, global convexity, and critical-count stability are reconstructed. The full original proofs of every cited background work were not audited. This supplementary acceptance is not needed for the sufficient universal negative disposition.

## Evidence and reproducibility

- Four mathematical proof/audit documents are preserved byte-for-byte.
- Both original diagnostic scripts and both original result JSON files are preserved byte-for-byte.
- The source report and public provenance manifest are preserved byte-for-byte. Their non-certification fields describe their source-only remit.
- The inspection receipt removes only two workflow-only members. Its mathematical, source-inspection, version, and status fields are unchanged.
- The derived WXY checker replaces exactly five assertions with explicit conditional raises so that all diagnostic rejection conditions remain active under optimization. Its original source is retained and its complete edit map is public.
- The packaged replay runs both accepted diagnostic paths in normal, -O, and -OO modes and requires deliberate wrong-residual rejection in all three WXY modes. Recorded output and dependency details are in [REPLAY_RESULTS.json](checks/REPLAY_RESULTS.json).
- The strict integrity checker verifies all packaged files and the links between original bytes, review pins, and derived checker bytes.

## What is not certified

This is AI-assisted authored reconstruction and independent audit. It does not claim human review, formal proof-assistant verification, acceptance of this reader by a journal, new original theorems, numerical certification of an explicit perturbation parameter, or inspection of the unavailable MTY version-of-record PDF. Finite diagnostics support the analytic arguments and are not substituted for them. The arbitrary-interior-point question and maximal-Tukey-depth results retain their distinct scopes.
