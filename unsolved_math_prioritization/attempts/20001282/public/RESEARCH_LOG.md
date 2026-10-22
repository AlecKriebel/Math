# Five approaches to AIM Question 18

Problem 20001282 / AIM-CONVEX_GEOMETRY-0014. Date: 2026-10-03.

The stopping criterion is the original compound question, not the product-prism wording in the queue title. The five approaches below are distinct mathematical routes. The end result is partial: the absence-of-local-minima assertion follows from current literature, and the stronger critical-point assertion is proved here for two full dual face types; the universal critical-point assertion is still unresolved. No novelty or priority claim is made.

## Approach 1: Try to upgrade the global Mahler inequality

**Target.** Deduce the fixed-type local assertion from the established three-dimensional symmetric Mahler inequality and its equality classification.

**Work.** The theorem says that P(K)≥32/3, with equality only at affine cubes or octahedra. Hence every body in one of the nonexcluded types has strictly larger product. This identifies the absolute lower boundary value, but a strict positive gap at each individual point does not supply an admissible descending path. The realization stratum is not closed: a minimizing sequence may change incidences at its limit. One therefore cannot use attainment of a minimum in the larger compact normalized convex-body space to infer attainment, or absence of local extrema, in this open stratum.

The logical gap has a simple exact model. The coercive polynomial

\[
f(x)=x^4/4-x^3/3-x^2+8/3
\]

has derivative x(x+1)(x−2). Its global minimum is f(2)=0; nevertheless x=−1 is a local minimum, with f(−1)=9/4 and f''(−1)=3>0. A sharp global bound and unique equality location coexist with a higher local minimum. Likewise, known local minimality of cubes says nothing about a different stratum, and an unrestricted ellipsoid-maximizer theorem does not exclude maxima constrained to a polytopal face type.

**Outcome.** This route alone fails. It is retained as a quantifier check: a new local deformation mechanism is necessary. The actual modern no-minimum argument found later is an admissible-shadow argument, not an automatic corollary of the global inequality.

## Approach 2: Reconstruct the planar-product subfamily

**Target.** Obtain an explicit same-type deformation for geometric product hexagonal prisms and see whether it covers the full question.

**Work.** A centrally symmetric planar strict hexagon has a marked affine chart

\[
H_{p,q}=\operatorname{conv}\{\pm e_1,\pm e_2,\pm(p,q)\},\quad
p,q>0,\ p+q>1,\ |p-q|<1.
\]

Its area is p+q+1. Its polar is a square cut by a symmetric strip, of area
\(4-(p+q-1)^2/(pq)\). Therefore

\[
P(H_{p,q})=(p+q+1)\left(4-\frac{(p+q-1)^2}{pq}\right).
\]

For K=H×[−a,a], the primal volume is 2a|H| and the polar consists of two pyramids of total volume 2|H°|/(3a). Thus P(K)=4P(H)/3. At fixed p+q, increasing |p−q| lowers the planar product. Direct differentiation gives its sole critical point p=q=1, of value 9, and hence product-prism value 12. This indeed produces decreasing paths inside the ambient prism stratum at every product point.

The coverage failure is geometric. A combinatorial prism need not be an affine Cartesian product. Dually, a combinatorial bipyramid can have an equatorial six-cycle that is not planar. A submanifold stationary point is not automatically stationary in the ambient realization space, nor does uniqueness of stationary points in a submanifold prove uniqueness in the entire stratum.

**Outcome.** The route verifies the familiar restricted family but does not close the original question. It is not counted as a new result. Its exact missing parameter motivates the next approach.

## Approach 3: Add the nonplanar-equator parameter

**Target.** Cover every centrally symmetric realization of the hexagonal-bipyramid face lattice, rather than just a product-dual subclass.

**Work.** Normalize two equatorial vertices and one pole to e₁,e₂,e₃. The remaining equatorial pair is ±(p,q,r). Checking all twelve triangular supporting planes gives the complete chamber

\[
|r|<p+q-1,\quad |p-q|+|r|<1,\quad p,q>0.
\]

The new coordinate r measures whether the equatorial set spans a plane or all of three-space. Its nonzero values cannot be removed by an affine coordinate change. A triangular-facet determinant calculation makes primal volume independent of r. Horizontal square sections of the polar provide its r dependence exactly. The resulting product is

\[
\frac43(p+q+1)\left(4-\frac{(p+q-1)^2+r^2/3}{pq}\right).
\]

The r derivative vanishes only at r=0. Then the d=p−q derivative vanishes only at d=0, and the s=p+q derivative only at s=2. The full normalized Hessian is diag(−2/3,−2,−8/3). This proves one critical affine orbit and strict maximality in the full realization space, not merely on the planar-equator slice. Increasing |r| also gives a decreasing curve at every point, including the maximum. Polarity transfers everything to the full hexagonal-prism class.

**Outcome.** Complete affirmative critical-point classification for these two dual face types, with exact product range (32/3,12]. The checker independently reconstructs primal/polar rational hulls at 81 interior realizations and verifies every facet size, both volumes, polarity, and the Taylor Hessian. Prior work already announced the global maximum 12, so this is presented as an explicit verification without a priority claim.

## Approach 4: Single antipodal-vertex shadow motions

**Target.** Move from a special eight-vertex chart to arbitrary centrally symmetric simplicial types.

**Work.** If all facets are triangles, moving one pair ±v with opposite velocities in a fixed direction automatically preserves all facet planarity constraints for sufficiently small time. Every determinant contributing to volume is affine in that time. The reciprocal polar volume is convex by the Meyer–Reisner shadow theorem.

If an interior point minimizes the product along such a path, the ratio argument in PROOF.md forces primal volume and reciprocal polar volume to be affine in the equality regime. Meyer–Reisner rigidity then makes the movement a global linear shear. Choose a vertex pair whose deletion leaves three linearly independent vertices fixed. Any such shear fixing those three vectors is the identity, whereas the selected pair actually moves. Contradiction.

Such a removable pair exists whenever the number of opposite vertex pairs exceeds three: select a basis from three pairs and remove another pair. Hence every centrally symmetric simplicial three-polytope with more than six vertices is not a local minimum in its fixed type. The exceptional six-vertex body is precisely an affine octahedron. Polarity gives the corresponding result for simple types other than the cube.

This is a direct application of established shadow-system machinery, not a new theorem claim. The obstacle to applying the same isolated-pair movement to an arbitrary mixed-face polytope is real: a vertex belonging to several nontriangular facets must satisfy their planarity equations. An arbitrary one-vertex motion can split facets and leave the prescribed stratum. The issue is preservation of incidence, not a lack of a global lower bound.

**Outcome.** A rigorous broad special case and a sharply identified obstruction. Coordinated speeds, rather than unconstrained single-vertex perturbations, are required for the remaining face types.

## Approach 5: Coordinated admissible speeds and the remaining stationary question

**Target.** Remove the mixed-face obstruction and then test whether the same method also proves uniqueness of critical points.

**Work.** Chen–Li–Xi–Xu's 2026 preprint provides exactly the coordinated construction. Odd scalar speeds are required to be affine along every facet not parallel to the shadow direction. Parallel facets need no additional constraint. The affine-volume property follows from the determinant expansion. A local minimum permits only a three-dimensional space of globally linear speeds, both for the polytope and its polar.

The elementary bound

\[
\dim A_\theta\geq(F-V)/2+2+C_\theta
\]

then reduces possible shadow-rigid pairs to |F−V|≤2. In the ±2 cases, applying the bound to a suitable nonsimplicial dual facet forces the six-facet/eight-vertex cube or its polar. In the equality case F=V, the same count limits facets to triangles and quadrilaterals with no shared quadrilateral edge. Euler's relation forces four triangles, and edge counting forces at most two quadrilaterals; the resulting V=F=6 is incompatible with a symmetric three-polytope. PROOF.md supplies the details and the local-to-dual-stratum step. No global-minimum hypothesis is used.

The method therefore yields the entire no-minimum assertion, as a source-backed consequence of this preprint. It does not give the additional assertion about all critical points. A negative direction is compatible with a critical saddle. Even a collection of one-dimensional restrictions cannot be used to assert a negative-definite full Hessian without controlling cross terms and proving the directions cover the relevant tangent geometry. The explicit chart in Approach 3 avoids these issues only for the two indicated types.

**Outcome and stopping point.** Main no-local-minimum assertion recovered from modern literature; full critical classification verified for the hexagonal-bipyramid/prism strata; universal unique-critical-orbit claim still unproved and not disproved. Five substantive approaches have been completed. Publication should preserve this partial status and require a fresh independent mathematical audit.
