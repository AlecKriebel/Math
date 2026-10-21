# Integer progression permutations: EP195 / 1986

**Partial research only. The all-integer four-term question remains unresolved in this edition; the universally forced threshold is 3 or 4.**

The target is a bijection N0 -> Z. A forbidden arithmetic progression is a subsequence at increasing, not necessarily consecutive indices, with any nonzero integer difference. Both signs count. A finite avoiding order, arbitrary total order, and doubly infinite permutation do not settle this omega-enumeration target.

This is an AI-assisted, unrefereed research edition. The independent check described here is an internal AI audit, not external human peer review or formal proof-assistant certification. Source results retain their named attribution. No novelty claim is made. This prose-and-metadata edition is not a computational reproduction package: code, raw result files, copied source documents, source text, and images are not distributed. Historical execution and inspection statements describe the authenticated research and audit records; no mathematical code or formalization was rerun during publication preparation. Hashes authenticate bytes, not mathematical truth. The complete written mathematics is retained below, with the single safe-prefix orientation correction disclosed in ACCEPTANCE.md and nonmathematical publication edits.

## What is included

- PROOF.md is the complete authored research report, with the audit's single orientation correction and disclosed publication edits. It retains every mathematical argument, finite example, construction, obstruction and limitation.
- AUDIT.md is the complete independent mathematical audit. It includes the full reconstruction of Ho's N0 proof, the all-Z three/five bounds, signed obstructions, demand-cycle certificates, shell argument and compactness criterion.
- ACCEPTANCE.md and ACCEPTANCE.json state the accepted scope, exact correction, original/corrected identities and unresolved boundary.
- SOURCES.json preserves public titles, URLs, versions, manuscript status, snapshot hashes/sizes and bounded historical inspection records.
- VERIFICATION.json distinguishes historical finite computations, independent audit checks, and publication-only integrity checks.
- MANIFEST.json lists exactly these eight files and hashes the other seven; its own digest is pinned separately in the publication record.

## Mathematical result and boundary

Ho's September 2026 written proof gives a four-term-free omega-permutation of N0 and N, for both signs of the difference. Its parity-buffer argument uses nonnegativity essentially. The all-Z fixed-tail attempt fails, and the exact signed-splice residual and symmetric-buffer obstruction explain a concrete obstacle. They exclude specified strategies, not all possible integer permutations.

The dead-prefix examples, residue-grouped shell obstruction and uniform-predecessor compactness equivalence are partial deductions. The missing uniform bounds are not supplied. Adenwalla's known five-term-free construction is reconstructed with exposition repairs, and its infinitely many negative-difference four-term progressions are explicit. The threshold remains 3 or 4.

The safe finite prefix must use the reverse of Ho's fixed tail order. Prefix (1,2) in the same orientation creates (1,2,3,4); this is the sole required mathematical wording correction. The frozen research original is preserved unchanged, while PROOF.md uses the corrected working copy.

## Source and verification boundaries

Sources are credited where used. The Ho and Geneson 2026 items were inspected as arXiv preprints; the independent audit read Ho's complete five-page written proof but did not execute source Python, Lean or builds. Adenwalla's Theorem 1 was inspected and reconstructed; the full 16-page article was not audited. Geneson's density supremum is not treated as exact full support. The later repository's formalization claims are attributed without independent certification. Direct tracker access failed and bounded searches do not prove literature completeness.

The historical independent checker used separately authored code, with identical reports in normal, -O, and -OO modes. Candidate scripts and source-author scripts were not executed by that audit. The finite results corroborate written proofs and cannot establish an infinite conclusion by themselves. Publication preparation performs integrity and editorial-replay checks only; it is not a new mathematical audit or fresh source review.

## Public sources

- Sarosh Adenwalla, Avoiding Monotone Arithmetic Progressions in Permutations of Integers: https://arxiv.org/abs/2211.04451v7 ; published article https://doi.org/10.1016/j.disc.2024.114183
- Jesse Geneson, Density bounds for permutations avoiding monotone arithmetic progressions: https://arxiv.org/abs/2608.12604v1
- Boon Suan Ho, A 4AP-free permutation of the positive integers: https://arxiv.org/abs/2609.12780v1
- Later repository human proof, acknowledging Ho: https://github.com/coleski/erdos196/blob/main/FINAL-HUMAN-PROOF.md

No copied third-party source document, extracted source text, image, dataset, raw result file or executable code is part of this edition. Explicit finite sequences and formulas are retained as necessary authored written mathematics. This edition changes no pre-existing repository file or research queue entry.
