# Central-section perimeters: uniform C² local rigidity and the global gap

**20001284 / AIM-CONVEX_GEOMETRY-0016. Original problem unresolved after five substantive author attempts.**

AIM's 2010 Problem 20, attributed to R. J. Gardner, asks whether two origin-symmetric star bodies in R³ must coincide when their intersections with every plane through the origin have equal boundary lengths. The imported catalogue title refers to a finite-dimensional partial result, not the full problem. This packet does not claim a global resolution.

## Strongest positive result

There exist absolute ε,C>0 such that, for every R>0 and any positive even C² radial functions ρ₀,ρ₁ satisfying

||ρ_i/R−1||_{C²(S²)}<ε,

one has

||ρ₁−ρ₀||_{L²(S²)} ≤ C ||P(ρ₁)−P(ρ₀)||_{H^(1/2)(S²)}.

Here P is the central planar-section perimeter map and Sobolev norms use the spherical-Laplacian spectral convention. Thus equality of all central-section perimeters implies equality of the two bodies in a full C² neighborhood of a ball, without a fixed harmonic cutoff or analytic-path assumption. Convexity is not needed. The constant is uniform across all even harmonic frequencies. This is an author-proved local theorem, pending a fresh final audit; historical novelty has not been established.

The proof integrates the derivative by parts to remove derivatives from the unknown difference. The resulting geometric weight is only C⁰ in the body-direction variable but smoothly controlled in the plane-normal variable by the C² radial norm. Expanding only in the normal variable yields a summable L²→H½ operator series. Mere pointwise smallness of a general weight would not suffice.

## Five written attempts

1. [Uniform C² local theorem and proof](attempts/ATTEMPT_1.md), with [independent contributing calculation](contributing_calculation/WEIGHTED_FUNK_C2_ESTIMATE.md). The latter is author support, not the final review.
2. [Global midpoint-defect identity](attempts/ATTEMPT_2.md). The average defect controls the Dirichlet energy of the radial log-ratio; strict convexity does not establish injectivity of the complete data map.
3. [Six explicit planes](attempts/ATTEMPT_3.md). For ρ_A=R+uᵀAu and ||A||F≤R/100, these planes give a stable injective chart. Explicit inverse formulas and radius are provided.
4. [Finite-data invisibility](attempts/ATTEMPT_4.md). For any finite list of planes there are distinct arbitrarily close even analytic strictly convex bodies with exactly the same sections in those planes. This does not match all planes.
5. [Antipodal switching and its symmetry barrier](attempts/ATTEMPT_5.md). A fully checked nonsymmetric construction illustrates the known Ryabogin–Yaskin mechanism. Enforcing evenness collapses this pair to the same body.

## Source and validation status

Gardner's official update, version 3.0 of 14 September 2026, printed p. 12, still lists the general problem as open. See [SOURCE_AUDIT.md](SOURCE_AUDIT.md) for theorem scope, dates, sources and the exact live catalogue-page access limitation. Rusu's analytic-path theorem, Yaskin's polytope theorem and the nonsymmetric counterexample literature are credited, not treated as new results.

Run `python3 verify_exact.py` from this folder. Python 3 and SymPy are required. [EXACT_CHECKS.json](EXACT_CHECKS.json) records exact algebraic controls. These finite checks do not establish the functional-analytic convergence arguments by computation, replace the written proofs, or provide formal/human peer review.

The remaining target is global uniqueness or a genuine equal-data pair of origin-symmetric star bodies outside the established local neighborhood. No C¹-local theorem, nonsmooth/infinite-perimeter resolution, global theorem or historical-priority claim is made.
