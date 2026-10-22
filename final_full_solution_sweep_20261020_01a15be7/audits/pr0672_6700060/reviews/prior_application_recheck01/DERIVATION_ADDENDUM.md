# Local extension and adversarial checks

2026-10-21 UTC. This addendum follows the preserved source-first checkpoint and immutable candidate inspection; it does not replace or alter that checkpoint.

## Local ambient extensions suffice

The candidate uses locally extending smooth charts. A single preassigned global ambient extension of the map is unnecessary. View the map's components in the actual Euclidean source and target ambient coordinates. Cover the compact source P by finitely many open sets with local smooth extensions F_i. On P the extensions agree with f. On the full-dimensional interior, every derivative of F_i−F_j is zero; continuity gives equality of all these derivatives at points of P in overlaps, including closed corners. A smooth partition of unity on a neighborhood of P therefore glues the vector-valued extensions into one smooth F agreeing with f and with the prescribed derivatives along P. The same observation applies to a local ambient extension of the inverse. The chain-rule and nonzero-determinant argument in the preserved derivation then supplies a neighborhood with nonsingular DF. Thus its direct flat neighborhood construction applies under the candidate's local ambient convention as well.

Alternatively glue the local positive definite metric extensions directly. All jets agree on P, for the same interior-density reason. Their partition-of-unity sum agrees there in all derivatives relevant to scalar and face mean curvature. Positivity survives convex combination after shrinking neighborhoods. Its curvature outside P need not be zero, because the prior theorem only constrains curvature on P. The candidate's version of this metric-gluing argument is sufficient.

## Independent exact controls

`exact_application_controls.py` is newly authored here and was not copied from or run through a candidate verifier. It uses only exact standard-library rational arithmetic and explicitly implemented one-variable polynomial operations. All 358 diagnostics pass in both normal and optimized Python, with identical output. The tests establish only the finite identities they name.

The nonlinear map F(x,y,z)=(x,y+x²,z) has smooth inverse (X,Y,Z)↦(X,Y−X²,Z). Its metric is

    g = [[1+4x²,2x,0],[2x,1,0],[0,0,1]], det(g)=1.

The script derives the Christoffel symbols from the metric; the only nonzero one is Γ^y_xx=2. It computes all 81 Riemann components as exact zero polynomials. For the facet y=0, the outward metric-normal numerator (2x,−(1+4x²),0) pushes to (2x,−1,0), pointing out of the epigraph Y≥X². Its normalized divergence is 2/(1+4x²)^(3/2)>0, matching the sphere-positive target mean curvature. Reflection in the first output coordinate reverses ambient orientation and preserves the pullback metric and outward-side test. These are concrete checks against a silent normal or mean-curvature sign reversal.

At e_1 of the n-dimensional cross-polytope, 2^(n−1) facets meet. The script treats n=3,4,7, so the vertices are nonsimple. Exact normal-push, norm, and adjacent-facet Gram formulas agree under an invertible triangular linear map, and product inverse-metric pairings preserve old angles while making cap-side pairings zero. This checks examples of the coordinate algebra; the absence of a dimension bound or simplicity restriction comes from the theorem statement, not these finitely many examples.

The affine shear (x,y)↦(x+3y/4,y) gives a flat constant metric with straight facets but changes the right angle at one corner to a smaller angle: its outward-normal cosine is −3/5. At an opposite corner the cosine changes sign, producing a larger interior angle. Thus flatness and totally geodesic facets by themselves do not establish the needed equality with the reference. The stated prior theorem's all-angle hypothesis and equality conclusion supply the essential global restriction.

The polynomial pullback for x↦x³ is 9x⁴, vanishing at x=0. This falsifies the attempted extension argument when smooth inverse/nonsingularity is dropped; it is not a counterexample to the properly qualified application. Exact planar turning-budget controls also show that any strict decrease produces positive excess turning, repairable only by a negative integrated boundary curvature.

## Historical smoothness context

Only after the source-first derivation and candidate inspection, Gromov's *Dirac and Plateau Billiards in Domains with Corners*, author manuscript dated September 20, 2013, §1 printed pp.2–3, was retrieved and read for its definition of a cornered structure by extension into an ambient smooth manifold and of its restricted ambient tangent bundle. It supports the naturalness of the candidate's category. It does not supply a theorem making every facewise/interior smooth homeomorphism into an ambient diffeomorphism, or a reduction from arbitrary singular corner maps. The 2017 question itself does not spell out a nonsimple-corner differentiability convention, so the explicit qualification remains necessary.
