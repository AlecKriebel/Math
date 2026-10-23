# Barycentric hyperplanes verified prior negative result

**The universal question for every dimension n ≥ 3 is false.** Sergii Myroshnychenko, Kateryna Tatarko, and Vladyslav Yaskin (MTY) already supplied the sufficient counterexample in their published paper [*Answers to questions of Grünbaum and Loewner*, Advances in Mathematics 461 (2025), 110081](https://doi.org/10.1016/j.aim.2024.110081). This reader verifies and explains that prior result; it claims no new counterexample.

The [full dimension-five reconstruction](mty/MTY_DIMENSION5_VERIFICATION.md) constructs a compact convex body with nonempty interior, ordinary volume centroid zero, and exactly **one distinct unoriented hyperplane** whose section has centroid zero under induced four-dimensional Euclidean measure. The exceptional section is exactly an **origin-centered four-ball**. Every other direction has strictly positive fifth section moment. Since the proposed bound in dimension five is six, this already negates the universal assertion.

The target is the centroid specialization in Zuzana Patáková's contribution with Martin Tancer and Uli Wagner, *Oberwolfach Reports* 17 (2020), Q2 on printed p. 1502; the range n ≥ 3 is inherited from Q1. Public tracking identifiers: 1779 / 30004514 / OWR-1703876-007. This is not the separate arbitrary-interior-point or maximal-Tukey-depth question.

## Read the sufficient proof first

1. [MTY dimension-five reconstruction](mty/MTY_DIMENSION5_VERIFICATION.md): complete authored analytic argument, including convexity, centering, every direction, and exact counting.
2. [Independent geometry and measure audit](geometry/MTY_GEOMETRY_AUDIT.md): a separate check of the construction and its target hypotheses; it also explains the original n ≥ 5 range.
3. [Proof and dependency map](PROOF_AND_DEPENDENCY_MAP.md): where each obligation is discharged and what background is used.
4. [Source and version map](SOURCE_AND_VERSION_MAP.md): precise inspected versions, public citations, hashes, and access limits.
5. [Checker guide](CHECKER_GUIDE.md): reproduce the finite algebraic and numerical diagnostics without confusing them with the proof.

## Two repaired statements in inspected author v2

The inspected [arXiv:2404.15188v2](https://arxiv.org/abs/2404.15188v2), dated 7 November 2024, needs two local statement repairs. Both are explicit in the reconstruction §9 and geometry audit §§3–4:

- The complementary-homogeneity hypotheses attached to equation (5) do not support its displayed equality. The actual construction needs same-degree −1 self-adjointness, proved in the reconstruction using the spherical Radon transform.
- The inverse-radius comparison on p. 5 is non-strict on the equator. The proved positive lower bound for the seed radius is sufficient.

These repairs leave the construction valid. **The published journal PDF bytes were not recovered or inspected.** Publication identity is verified separately; no author/publisher byte equivalence or allegation about the uninspected journal text is made.

## Optional all-dimensional supplement

Shouda Wang, Ge Xiong, and Kaiwen Yang (WXY), [*A complete solution to the Grünbaum–Loewner centroid problems*, arXiv:2606.19865v2](https://arxiv.org/abs/2606.19865v2), dated 31 July 2026, remains publicly labeled a **submitted preprint**, as checked on 14 October 2026. Its [full authored reconstruction](wxy/WXY_RECONSTRUCTION_AUDIT.md) and [independent geometric audit](geometry/WXY_SUPPLEMENTARY_GEOMETRY_AUDIT.md) verify the main all-dimensional construction, including n = 3 and n = 4, subject to the stated standard analytic prerequisites. Its conclusion is credited entirely to WXY. **The universal negative result does not depend on this supplement.**

## What verified means here

This is an AI-assisted authored reconstruction and independent computational/analytic audit, not a claim of human review, journal acceptance of this reader, or formal proof-assistant certification. The original authors retain credit for the mathematical results. The analytic proofs establish existence; finite checker runs are diagnostic corroboration. No explicit numerical value of the existential perturbation or centering parameter is certified.

[ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md) summarizes the accepted evidence and its limits. The source report and provenance manifest are preserved source-only snapshots: their statements that they do not certify proofs describe those files' scope, not a missing proof in this reader. The separate reconstructions and cross-review receipt provide the proof-verification record.

## Integrity and contents

All four original mathematical proof/audit documents and both original checker scripts are byte-for-byte preserved. One inspection receipt has only two workflow-only fields removed. A separate WXY checker copy replaces its five optimization-sensitive assertions with explicit conditional raises; the original remains available. [Original/output mapping](integrity/ORIGINAL_ARTIFACT_MAP.json) and [exact checker derivation](integrity/CHECKER_DERIVATION.json) record every such change.

Run `python checks/verify_integrity.py` to check every listed file, cross-review pins, and the exact checker derivation. The payload is restricted to authored analysis, diagnostic code/results, and public verification metadata. Source PDFs, copied source text, page images, dataset contents, personal information, and private coordination material are excluded. The public archive contains only this reader directory.
