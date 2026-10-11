# Acceptance of the repaired dimension three target proof

Problem 1900017, Karpenkov Problem 17. Acceptance date: 11 October 2026.

## Decision and exact object

The accepted object is the authored reconstructed proof of finiteness of the sum of origin-sensitive geometric relative face frequencies in ambient dimension three. It comprises the full [geometric reduction](REDUCTION_AUDIT.md) and [planar finite-measure proof](MEASURE_AUDIT.md), as summarized in [AUDIT.md](AUDIT.md). The original and public-report bytes are bound in [ACCEPTANCE_SCOPE.json](ACCEPTANCE_SCOPE.json), with all editorial changes accounted for in [EDITORIAL_PROVENANCE.json](EDITORIAL_PROVENANCE.json).

An AI-assisted mathematical acceptance review read the complete target, reduction and measure reports. It checked the explicit group/Haar identification, the local first-contact flow-box argument, the reduced-minima basis and witness-selection proofs, the three support cuts and radial integral, and the precise hypotheses of the original White theorem. This is not an independent human referee report or a proof-assistant certificate.

## Accepted dependency chain

1. The face-frequency convention retains the origin and uses integer-linear face types. The primary Karpenkov source resolves the affine-versus-linear ambiguity. The GL₃/SL₃ indexing and arrangement/chamber comparisons are finite changes that preserve finiteness.
2. The face-adapted positive-height chart and direct finite-candidate first-contact flow boxes replace the source's defective global coverage and closed-orbit steps. Null-boundary exclusions, the positive component of the plane-preserving group and the level denominator are handled explicitly.
3. The explicit group isomorphism and slice calculation identify the needed cross-section with the affine-lattice first-contact set. The right-Haar translation fiber is ordinary area. This formerly separate measure-report dependency is established by the accompanying AI-assisted reduction audit, Sections 3–5, and is not left as an unresolved hypothesis.
4. The stabilizer bound is at most six, and distinct origin-sensitive integer-linear face types give disjoint measurable cross-section images. The measure comparison uses one face-independent normalization constant B.
5. The planar estimate proves the reduced-minima basis property and witness selection, uses a valid first-contact-restricted configuration cover, and verifies the required White theorem substitution. Corrected Farey support bounds and an independently recomputed radial integral yield the summable harmonic bound.
6. The level-one determinant bound and Tonelli summation yield finite total measure. The Haar-almost-everywhere planar scope suffices; an all-lattice pointwise theorem is unnecessary.

## Established external mathematics retained

The specialized imported theorem is G. K. White, *Lattice Tetrahedra*, Canadian Journal of Mathematics 16 (1964), 389–396, Theorem 2 on printed page 390, [DOI 10.4153/CJM-1964-040-2](https://doi.org/10.4153/CJM-1964-040-2). Its original publisher statement was visually inspected and the substitution (a,b,c,d)=(1,c1,c2,k) was checked. Its full proof was not independently re-proved. Reliance on this established theorem is explicit ordinary mathematical dependence, not an identified unresolved proof gap.

The ordinary imports are Haar measure and its local factorization on the stated Lie groups, finite invariant volume of SL₂(R)/SL₂(Z), countable additivity and Tonelli for nonnegative functions. The proof does not require the Kannan–Lovász covering-radius lemma, Minkowski's convex-body theorem, a generic ergodic frequency theorem or periodic-sail equidistribution.

## What this decision does not certify

- The original printed argument verbatim, every assertion of its 50-page manuscript, or all claims of its Theorem 3.3.
- Any lower estimate in Proposition 5.1, Proposition 6.3 or Theorem 3.3.
- Proposition 6.2's all-lattices pointwise formulation or the exceptional-boundary portion of Lemma 9.2.
- Generic ergodic or periodic-sail conclusions.
- A canonical absolute numeric normalization of the original Möbius measure.
- A new result, any dimension at least four, journal acceptance, human referee review or formal verification.

## Source status and precise criticism

Aggarwal and Andritsch's [arXiv:2608.05853v1](https://arxiv.org/abs/2608.05853v1), submitted 6 August 2026, already claims the dimension-three finite sum in Theorem 1.9. No journal reference was visible in the inspected version-pinned record. The accompanying reports identify and repair literal intermediate errors; they neither produce a counterexample to the final finite-sum claim nor allege that the final theorem is false. The proper disposition is a prior preprint theorem claim supported by a completed repaired target-proof reconstruction with the explicit established imports above.

## Verification boundary

All 38 accepted-audit files, all 80 files in the closed reference inventory, and the five explicit input pins were rechecked against exact sizes and SHA-256 hashes. The original independently authored algebraic and finite sanity checks were rerun in normal, -O and -OO modes with identical results matching the accepted records. The full mathematical proof sections were preserved byte-for-byte. These integrity and finite checks are supplementary evidence, not substitutes for universal arguments or formal proof verification. Third-party source copies, raw datasets, scripts and private coordination material are excluded.
