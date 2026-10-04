# Five substantive attempts

Date: 3 October 2026. Mathematical attempts are distinguished from retrieval, packaging, and later independent review. All five concern the same unrestricted printed target. No full solution was obtained, so there is no early-stop classification.

## Attempt 1: exact Kähler geometry and the known kernel construction

Approach: seek a global Stein criterion from the Hessian lift and compare with Shimizu's construction.

Work: derived the global primitive λ=−g_x(y,dπ), verified dλ=ω, proved completeness of the lifted metric from finite-length paths, and checked Shimizu's original full argument. The exact symplectic form excludes compact positive-dimensional complex submanifolds. The older kernel construction is strict only off its possible divisor in general.

Outcome: neither an exact Kähler form nor the cited divisor-complement result supplies the global exhaustion required by the target. PROOF.md §§1,6 retain the precise positive facts and gap.

## Attempt 2: fiber-norm exhaustions and scalar repairs

Approach: test whether the natural squared fiber norm ρ=g_x(y,y), perhaps after an increasing reparametrization, is plurisubharmonic.

Work: constructed the periodic positive Hessian matrix of φ=|x|²/2−(1/4)cos x₁cos x₂ on the affine two-torus. Its eigenvalues stay between 3/4 and 5/4. At x=0,y=(4,0), the z₂-gradient of ρ vanishes while its Levi value is −3/8. The scalar-chain-rule term involving H'' therefore vanishes in exactly the bad direction. Every reparametrization with positive derivative fails there. A fixed added base function also fails at large fibers.

Outcome: a rigorous obstruction to this proof method, not to Steinness. The tangent complex manifold remains (C*)². PROOF.md §2.

## Attempt 3: finite-facet equivariance

Approach: replace metric potentials by affine supporting forms whose holomorphic logarithms have explicit transformation rules.

Work: proved the full line-free polyhedral quotient theorem, even for noncompact base. A finite-index subgroup fixes facets; their positive scale characters yield a discrete real lattice. Componentwise logarithms embed the tube as a closed complex submanifold of a product strip modulo that lattice. An explicit projection-plus-log-cosine exhaustion is strictly plurisubharmonic and proper. Finite averaging handles the facet-permutation quotient. Also proved the shorter sum-of-facet-ratios exhaustion when the base is compact.

Outcome: complete affirmative special case. The finite list of facets is essential to this argument; it does not cover arbitrary nonpolyhedral Ω. PROOF.md §3.

## Attempt 4: lineality and translation reduction

Approach: extend the special-case result through groups preserving complete affine directions, and close the lowest-dimensional cases.

Work: proved that convexity upgrades invariance under a discrete translation lattice Λ to invariance under its real span V. The quotient splits holomorphically as (C*)^rank(Λ) times a convex tube. The one-dimensional tangent manifold is an open Riemann surface. Both give Steinness, with exact quotient maps and hypotheses stated.

Outcome: complete affirmative translation and dimension-one cases. Nontrivial affine linear holonomy in a general complete Hessian manifold is not eliminated. PROOF.md §4.

## Attempt 5: all supporting halfspaces

Approach: remove the finite-facet assumption by taking a supremum over all positive affine supporting forms.

Work: constructed the affine-invariant support norm N_Ω and U_Ω=(1/2)log(1+N_Ω²). Proved compactness of the normalized support-gradient set, continuity, nondegeneracy, locally uniform norm bounds, plurisubharmonicity by the disk submean inequality, and properness on compact-base quotients. On the positive quadrant, the formula becomes a maximum of coordinate ratios; an explicit open region has a transverse Levi null direction.

Outcome: continuous weak plurisubharmonic exhaustion for all compact hyperbolic quotients. Strictness and general noncompact-base control remain unproved. No inference from this weak exhaustion to Steinness is made. PROOF.md §5.

## Final accounting

Original target unresolved; five substantive attempts completed. Retained results have full written proofs and exact local controls. Symbolic verification does not decide the unresolved universal assertion. No novelty or human-peer-review claim is made.
