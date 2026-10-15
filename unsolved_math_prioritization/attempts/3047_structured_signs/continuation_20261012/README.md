# Partition signs: full ternary obstruction, zero restrictions and exact prefix tests

12 October 2026. This appendix continues the authored partial investigation of David Newman's independently signed unrestricted-partition problem (3047 / OPG-37222). Every original factor remains present:

\[
P(q)=\prod_{m\ge1}\left(1+\sum_{j\ge1}\epsilon_{m,j}q^{mj}\right),
\qquad \epsilon_{m,j}\in\{-1,1\}.
\]

The question asks whether all coefficients of \(P\) can belong to \(\{-1,0,1\}\). This appendix does not resolve it. It makes no novelty, priority or unrestricted finite-search record claim.

## Results and full proofs

1. [Interior-zero bound](INTERIOR_ZERO_BOUND.md). If the unrestricted product has coefficient bound \(M\), Jensen's formula gives the exact necessary zero-mass inequality, with all analytic multiplicities. For fixed \(0<\rho<1\), the total number \(Z_\rho(N)\) of zeros in \(|z|\le\rho\) among the first \(N\) original local factors satisfies
   \[
   \limsup_{N\to\infty}\frac{Z_\rho(N)}{\log N}
   \le\frac1{2\log(1/\rho)}.
   \]
   The proof covers convergence, nonvanishing tails, lifted zeros, boundary radii and the order of limits. It is a necessary condition, not an impossibility result.
2. [Common-factor obstruction](COMMON_FACTOR_OBSTRUCTION.md). When the same arbitrary sign sequence is used in every original factor, degree 81 is the sharp first unavoidable coefficient failure. The unique good prefix through degree 80 is displayed. This is a computer-assisted exhaustive result for that restricted class.
3. [Ternary defect obstructions](TERNARY_DEFECT_OBSTRUCTIONS.md). Ternary-digit products with at most 0, 1 or 2 noncyclotomic blocks in total have sharp unavoidable failure degrees 31, 42 and 55. Explicit witnesses and the exact recurrence are given. A hypothetical successful ternary product must satisfy \(B(15)\ge1\), \(B(21)\ge2\), \(B(27)\ge3\), while the zero bound forces \(B(N)=O(\log N)\). These conditions are compatible. These earlier finite-cap results remain valid; the separate later theorem below excludes the entire ternary family using additional global Jensen constraints.
4. [One-exception binary hybrid](ONE_EXCEPTION_HYBRID_OBSTRUCTION.md). If every factor is binary-digit multiplicative except possibly one arbitrary factor with index \(a\ge3\), degree 94 is the sharp universal obstruction. The sharp fixed-index degrees are 94 for \(a=3\), 78 for \(a=4\), and 76 for \(a\ge5\). Indices 1 and 2 and multiple arbitrary exceptions are not excluded.
5. [Exact unrestricted prefix geometry](UNRESTRICTED_PREFIX_REDUCTION.md). Exact one-step existence/counting, half-prefix sign-constrained linearization through \(2M+1\), finite-horizon column grouping, an at-most-four-pair two-step test, and the compactness equivalence are proved. A degree-6 feasible prefix can first fail when attempting degree 7; this rules out universal extension of every feasible prefix, not nonemptiness of the full tree.

6. [Full ternary-digit obstruction](FULL_TERNARY_OBSTRUCTION.md). A subsequently accepted computer-assisted proof excludes the entire ternary-digit-multiplicative family, including infinitely many noncyclotomic blocks. It combines exact coefficient transitions with finitely many exact algebraic Jensen tests, under the hypothesized global coefficient bound one. The combined search has 831,371 states including the root and first becomes empty at degree 59. Degree 59 is not asserted to be a sharp coefficient-only failure degree for finite prefixes, and the result does not claim every ternary product has unbounded coefficients.

## Independent reviews and acceptance

- [Zero and restricted-class review](REVIEW_ZERO_AND_RESTRICTED_CLASSES.md) retains the complete analytic audit, independent common-factor and ternary enumeration reasoning, state-set comparison results, negative controls, and the corrected relationship between binary and ternary families.
- [Hybrid and prefix review](REVIEW_HYBRIDS_AND_PREFIXES.md) retains all substantive algebraic checks, exact original-factor diagnostics, independent hybrid enumeration, labelled-fibre tests, arithmetic bounds, complete-state comparisons, and limitations.
- [Full ternary review](REVIEW_FULL_TERNARY.md) retains the complete later audit: deferred-choice completeness, exact integer Jensen comparisons, independent logarithmic coefficient arithmetic, every-state comparison, negative controls, overflow bounds and sanitized replay.
- [Acceptance](ACCEPTANCE.md), [correction history](CORRECTION_HISTORY.md), and [dated source scope](SOURCE_SCOPE.md) describe precisely what is accepted and which public references were inspected.

These are AI-assisted, unrefereed mathematical research and independent AI-assisted verification. They are not external human peer review or proof-assistant certification.

## Computational evidence and public reproducibility

The finite obstructions are computer-assisted exhaustive enumerations. The complete mathematical transition rules, state domains, abstract witness encodings, frontier counts or complete per-case totals, explicit sharpness witnesses and substantive reviews are retained. The historical audits report exact complete-frontier comparisons using separately implemented arithmetic, rather than just equal aggregate counts or hashes.

The executable programs, raw state certificates, exploratory outputs and private verification records are not distributed in this appendix. This is a prose proof-and-review edition, not a publicly executable replay package. A reader can independently implement the stated recurrences and check the displayed witnesses, but reproducing the exhaustive claims requires that additional implementation and enumeration. The manifest authenticates distributed bytes; it is not mathematical evidence of exhaustive search on its own.

The analytic zero bound and exact prefix criteria are proved in prose. Their validity does not depend on the computer-assisted finite obstruction computations. The supplementary small-prefix numerical counts are identified as diagnostics.

## Dependencies and scope boundaries

The hybrid index reduction uses the preceding [all-binary obstruction](../BINARY_CLASS_OBSTRUCTION.md), independently rechecked during the hybrid audit. The [general radial caveat](../GENERAL_RADIAL_CAVEAT.md) remains controlling: finitely many arbitrary sign factors can suppress partition-scale growth on the positive real radius, which does not control all Taylor coefficients. The new angular zero restriction does not reverse that correction.

The binary and ternary digit-multiplicative families are incomparable. The entire ternary family is now excluded by the separate later theorem; neither that theorem nor the other restricted obstructions applies to every unrestricted sign array. No finite witness is asserted to extend to an infinite bounded-coefficient solution. No assertion is made that the number of ternary defects must be finite.

[MANIFEST.json](MANIFEST.json) inventories only the files actually distributed in this appendix, including itself without a recursive self-hash. Public scholarly references appear in the source scope. No source PDF, copied third-party source text, dataset, unpublished program or raw frontier is distributed.
