# Independent source-first derivation checkpoint

Prepared 2026-10-21 UTC before opening any candidate mathematical body, earlier candidate acceptance, or old target verdict. The exact head supplied for the later comparison is `13d9b2d944ce8ec121381a4bc21e48d2bb19846e`. Only its 24-path input inventory has been inspected at this checkpoint.

## Exact question and conditional prior input

Gromov's October 1, 2017 compilation, §22, printed page 60, starts with a compact convex polyhedron with nonempty interior. Question 64 asks whether extremality against convex competitors implies mean-convex extremality against corresponding smooth-faced Euclidean competitors. The forbidden competitor has all corresponding interior dihedral angles at most the original angles and at least one strict inequality. Printed page 61 supplies cube context, rather than a change of question.

The relevant prior input is Yuchen Bi, *Dihedral Rigidity for Convex Polytopes by Smooth Approximation*, arXiv:2608.06320v1, submitted August 6, 2026, 17:35:23 UTC. On the retrieval date, the abstract page lists only v1 and no journal reference. It is a recent preprint. This checkpoint establishes an implication from its stated Theorem 1.1; it does not independently certify the 18-page analytic argument or conventional peer review.

For a compact full-dimensional convex polytope represented by its irredundant affine facet inequalities, Bi assumes a smooth positive definite metric on an open neighborhood, nonnegative scalar curvature, sphere-positive outward mean curvature of every facet, and exterior dihedral angles at least Euclidean ones. Besides flatness and totally geodesic facets, its conclusion equates the pairwise metric and Euclidean outward-normal inner products on every nonempty facet intersection. Its statement imposes neither an upper dimension bound nor simplicity, acuteness, or a separate spin hypothesis. Dimension is at least three.

## Competitor category and the neighborhood metric

Fix a compact full-dimensional convex polytope P in R^n. In the category considered here, the competitor D is a Euclidean domain and f:P→D is a bijection of the closed domains taking each labeled closed facet to its corresponding facet, with interiors to interiors. Require smooth ambient extensions F on a neighborhood of P and G on a neighborhood of D of f and f^{-1}. This means nonsingularity through every corner, not just on the open stratum. These assumptions are explicit: the phrase "diffeomorphic" in a historical question is not itself a proof that every other proposed corner category has these properties.

On P's interior, G∘F is the identity. Thus DG(F(p)) DF(p)=I there. Both derivatives are continuous through the compact boundary, so the same identity holds at every p in P. Consequently DF(p) is invertible at every closed-corner point. The determinant is continuous and nonzero on the compact set P, hence there exists an open neighborhood U of P on which it remains nonzero. Shrink F's original domain to U and set

    g_p(v,w) = <DF(p)v, DF(p)w>_Euclidean.
    [g] = DF^T DF,  det(g) = det(DF)^2 > 0.

This is a smooth positive definite metric on U, exactly the type of neighborhood extension required in the theorem. Global injectivity of F on all U is unnecessary: by the inverse function theorem it is a local Euclidean isometry near every point of U. Thus its full Riemann curvature tensor, and in particular R_g, is identically zero. Local neighborhoods may map outside D; the ambient Euclidean metric is defined there too.

This construction does not use an orthant chart at a vertex. Arbitrarily many facets can meet there. Compactness, the actual ambient extension, and the derivative identity are sufficient at nonsimple corners in every finite dimension.

## Boundary sign and angle transport

At the relative interior of a facet, DF maps its tangent hyperplane to that of the corresponding competitor facet. Since f sends the domain interior to the domain interior, the g-unit *outward* normal maps to the Euclidean *outward* unit normal. The sign is fixed by which side contains the interior, so orientation-reversing ambient diffeomorphisms cause no sign change. Euclidean isometries in this metric transport the second fundamental form and its outward, sphere-positive trace. Therefore the metric facet mean curvature equals the competitor's Euclidean mean curvature (with an immaterial positive dimension normalization if normalized mean curvature is used consistently). Nonnegativity is preserved. Smooth facet extensions and continuity carry this to their boundaries.

Write N_a,N_b for the original outward Euclidean normals and ν_a,ν_b for the outward g-unit normals. Let α=arccos<N_a,N_b> and α_g=arccos<ν_a,ν_b>_g be the exterior angles. The competitor interior angle is θ_D=π−α_g; the reference interior angle is θ_P=π−α. Thus

    θ_D ≤ θ_P  iff  α_g ≥ α,

with strictness reversed in precisely the same way. This is Bi's hypothesis, not its opposite. No angle claim is deduced just from R_g=0.

Apply the stated theorem. Its additional normal-inner-product equality yields α_g=α, and therefore θ_D=θ_P, on every codimension-two face. This excludes the required strict inequality. If the historical definition allows the strict point on the closed boundary of such a face, the same conclusion applies there directly; alternatively continuity from the face's relative interior suffices. The conclusion also covers pairs intersecting only in higher codimension, although those extra equalities are not needed for Question 64.

In this ambient-smooth category, every compact full-dimensional convex P is mean-convexly extremal as a direct consequence of the prior theorem, whether or not P is convexly extremal. The implication asked in Question 64 follows immediately. The original extremality hypothesis is unused.

## Low dimensions

For n=2, the theorem as stated cannot be applied directly. There are two checkable bridges.

First, for a curvilinear polygon D diffeomorphic to a disk, orient its boundary positively. Under the outward sphere-positive convention the boundary turning/geodesic curvature k agrees in sign with the facet mean curvature. Gauss–Bonnet in the Euclidean plane gives

    integral_boundary k ds + sum_i (π−θ_D,i) = 2π.

The convex reference polygon has sum_i(π−θ_P,i)=2π. Nonnegative k and θ_D,i≤θ_P,i imply equality in every summand, so no strict improvement is possible. A nonsingular ambient map sends a convex pointed corner cone to another convex pointed cone, so its interior angles are in (0,π); no reflex-corner convention is silently being substituted.

Second, form P×[0,1] and D×[0,1], and use f×id and g⊕dt². These have smooth nonsingular neighborhood extensions. Product scalar curvature is zero; vertical-face mean curvatures retain their signs; horizontal caps are totally geodesic. Side-cap angles are π/2 in both metrics and side-side angles are inherited. Bi in dimension three forces equality on each vertical edge. This supplies an alternative reduction without claiming n=2 is in the original theorem statement.

For n=1 there are no codimension-two dihedral strata and no point at which the defining strict angle improvement can occur. The strict-angle assertion is vacuous.

## Completeness boundary and falsification conditions

This implication requires the *closed-domain ambient-smooth, smoothly invertible* competitor convention. A homeomorphism smooth only on the interior or each open face can have a derivative that degenerates or blows up at an edge or vertex. Its pullback need not extend to a smooth positive definite neighborhood metric. For example x↦x³ is smooth and bijective near a half-line endpoint, but its inverse is not smooth there and its pullback coefficient 9x⁴ vanishes at the endpoint. Such maps are excluded by the assumptions above. No singular smoothing theorem, approximation preserving the weak inequalities, or equivalence of broader corner categories has been established here.

Flatness alone is not the contradiction: an affine shear gives a flat pullback metric and straight facets with changed angles, some smaller and some larger. All-angle comparison plus the prior theorem's equality clause is essential. The source-first finding is thus positive dated overlap of an exact prior theorem with the regular-category claim, not an inference from absent search hits. An originality or full-resolution assessment still requires reading the immutable candidate and checking whether it supplies a new analytic mechanism or a bridge outside this category.

## Reading receipts and checkpoint

Fresh GWS read completed before substantive source comparison: 178 returned rows, no exact target entry. Broad matches at rows 4 and 61 concern AMR-066-0025 and Fuchs's labeled polygon-length problem, respectively. Source bodies are private. Original Gromov PDF printed pages 60–61 and adjacent page 59 were read through extracted text; Bi PDF pages 1–2 and HTML introduction/conventions/Theorem 1.1 were read, with abstract submission metadata checked live. No complete reading or verification of Bi §§2–3 is claimed.

Completion estimate for this limited source-implication review: 65%. The regular-category implication is established conditionally on the stated prior theorem; immutable candidate inspection, adversarial exact controls, and final sealing remain.
