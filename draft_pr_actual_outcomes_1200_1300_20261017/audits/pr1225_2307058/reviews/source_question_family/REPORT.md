# Frozen source-question-only report

**Strongest result:** the original implication in Hayman–Lingham Problem 7.58 has an affirmative analytic proof under the standard planar arclength 2-modulus conventions, including both globally rectifiable and locally rectifiable curves with endpoint limits. The proof is in DERIVATION.md. This is an independent mathematical reconstruction, not a claim of novelty or present-day openness/closedness.

## Exact authenticated source

W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*, arXiv:1809.07200v2, Problem 7.58. The original HTML at https://arxiv.org/html/1809.07200v2, lines 5002–5004, and original PDF page 179 (printed 178) agree. The question assumes compact E⊂[0,1] on the real axis with positive modulus to the radius-2 circle and asks whether the modulus from E to R\E is infinite. Attribution is A. A. Gonchar, communicated by M. Vuorinen. The source's historical update is recorded only as source text; no present-status inference is made.

## Mechanism

Assume a finite-energy density admissible for every E-to-(R\E) curve. Preserve all its pointwise values by a lower-semicontinuous L² majorant. A pointwise weighted-path potential has boundary values 1_E on the line. Its finite Dirichlet energy gives an H^{1/2} trace, and a compactly supported characteristic function in H^{1/2}(R) must be zero almost everywhere. Therefore E has zero line length.

Positive original modulus then forces a point x∈E with finite local Riesz potential of that density. Otherwise cutoff and smoothing of Riesz potentials would give smooth functions ≥1 near E with arbitrarily small energy; their gradients are directly admissible for E-to-circle curves. No touching-condenser or logarithmic-capacity identification is used.

Finally average short polygonal curves x→z→y with z in a small upper rectangle and y in its real-line base outside E. Their mean density length is bounded by a vanishing local Riesz integral plus ten times a vanishing local L² norm. A curve of length <1 contradicts admissibility.

## Edge checks

- Zero line length and positive original modulus are covered by the Riesz-potential and polygon argument; line length was never substituted for capacity.
- Infinite-valued Borel densities on area-null sets are preserved pointwise by the majorant. All curve integrals use arclength, so endpoint values carry no atoms.
- Every contradicting curve is globally rectifiable and has interior strictly in the upper half-plane.
- Smooth test densities are admissible also for locally rectifiable curves with the prescribed endpoint limits. The theorem therefore works for both requested curve conventions without assuming their moduli equal.
- Weak admissibility outside modulus-zero exceptional families reduces to strong admissibility by adding an arbitrarily small multiple of an L² density whose integral is infinite on each exceptional curve.
- Empty and polar E do not meet the positive-modulus assumption. The argument does not infer positive modulus from uncountability, line length zero, or positive Hausdorff dimension.

## Status and exact remaining gap

**Discovery goal estimate: 90%.** The independent derivation is complete and checkable. The remaining 10% is independent adversarial verification and comparison after the freeze, particularly of the weighted-path-potential measurability and the Fourier cutoff argument. Neither is left as an unsupported condenser-equivalence claim; both have explicit arguments in DERIVATION.md. No counterexample or unresolved central transfer is being promoted.

No candidate PR, submitted/current proof, outcome, audit body, prior agent analysis, or other project-program body was inspected before this freeze. Read-only source/background inputs and the one incidental repository-status filename exposure are recorded in RESEARCH_LOG.md. No Git branch, index, commit, or remote mutation was performed.
