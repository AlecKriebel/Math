# Independent geometric derivation for PR 672

Target 6700060. The accepted input is immutable head `13d9b2d944ce8ec121381a4bc21e48d2bb19846e`, with controlling attempt README. This report checks the geometric implication from Bi's stated Theorem 1.1. It does not independently establish the theorem's PDE and index-theoretic foundations, decide priority, or prescribe a PR disposition.

## 1. Exact claim and falsification criteria

Let P be a compact, full-dimensional convex polytope in R^n, n >= 2. Let D be a compact Euclidean domain with corresponding smooth facet pieces. Assume a face-preserving bijection F:P -> D and its inverse are locally restrictions of smooth maps on ambient open sets. Assume every competitor facet has nonnegative outward mean curvature, with a sphere positive, and every interior dihedral angle is at most the corresponding constant reference angle. The claim is that every such angle is equal; therefore strict inequality at even one point is impossible.

The claim excludes a merely combinatorial correspondence or one that is smooth only on open strata. To falsify the reduction one could exhibit loss of positive definiteness at a corner despite the specified smooth inverse, a reversed normal/angle convention, a missed assumption of Bi's theorem, a one-point strictness escape at a lower corner, or a dimension outside the imported result and planar argument. No such example was found under the stated assumptions. Section 5 gives exact adverse examples showing why weaker assumptions cannot silently replace them.

## 2. Nonsingular differential and neighborhood metric

Write G=F^{-1}. At an interior point x, the usual chain rule gives dG(F(x)) dF(x)=I. Every boundary point of a full-dimensional convex P is a limit of interior points. Choose local smooth ambient extensions of F and G near the point and its image. Passing the chain-rule identity to the limit gives the same identity at the boundary. Thus dF is invertible at every point of P, including nonsimple vertices. Consequently g=F^*e is a smooth positive-definite tensor there.

The differentiation is unambiguous: two smooth extensions agreeing on P agree on its interior, so all their jets agree at boundary points by continuity from the interior. A finite cover of P by local extensions of g may be shrunk until every extension is positive definite. On an open neighborhood of P take a smooth partition of unity subordinate to this cover and sum the extended tensors. Positive definiteness is preserved by a convex combination. The sum agrees with g on P. Its derivatives on P are those of g, for the same interior-density reason. This proves the precise neighborhood-metric hypothesis in Bi; no curvature requirement outside P is needed.

An alternative check is to patch coordinate extensions of F itself, obtaining a smooth ambient map with invertible derivative on a neighborhood of P. The resulting pullback tensor is flat there. This stronger extension observation is unnecessary for the submitted argument; the tensor-extension proof already suffices.

On P's interior, F:(P,g) -> (D,e) is an isometry, hence R_g=0. Continuity of the smooth extension gives R_g=0 also on the boundary. Flatness alone cannot give the desired angle equality, because the competitor was Euclidean from the start. The angle clause in the imported theorem is indispensable.

## 3. Outward side, curvature, and angle signs

At a facet-interior point, the domain is locally one side of a smooth hypersurface. F maps its interior to D's interior and its facet to the corresponding facet. A short inward path maps to an inward path. Thus the isometry carries the outward g-unit normal to the outward Euclidean unit normal of D, independently of the ambient orientation of F. It carries the Levi-Civita connection and the second fundamental form II(X,Y)=<nabla_X nu,Y> to the corresponding objects in D. Its trace therefore preserves mean curvature with the sphere-positive convention. By continuity the same facet tensor data extend to closed facets.

For two adjacent facets let theta be the interior angle and alpha the angle between their outward unit normals. Then theta=pi-alpha and <nu_a,nu_b>=-cos(theta). This is valid also when theta exceeds pi/2; replacing theta by the acute angle between unoriented tangent hyperplanes is invalid. Therefore

    theta_D <= theta_P  iff  alpha_g >= alpha_0,

and strictness is preserved with the reversed alpha inequality. Equivalently the normal inner product for g is no larger than its reference value. These are exactly the sign conventions in Bi's theorem, not an additional metric comparison. No inequality g >= e, prescribed boundary metric, fixed area, fixed volume, or edge-length condition is needed.

The comparison applies pointwise on each ridge. Bi's stated conclusion gives normal inner-product equality on every closed intersection of two facets, including intersections of dimension less than n-2. Hence it prohibits strictness anywhere in the original closed ridge. If one initially imposes the weak comparison only on a relative ridge interior, its extension to the closed ridge follows from continuity. A strict decrease at a closed endpoint also extends to nearby ridge-interior points, so isolated-corner strictness is no escape in this smooth category.

## 4. Dimensions and higher corners

For n >= 3, Bi's Theorem 1.1 states exactly the hypotheses just established for a smooth neighborhood metric on an arbitrary compact full-dimensional convex polytope. It requires neither simple combinatorics nor acute reference angles. Its final normal-pairing conclusion gives the desired equality directly. The theorem's stronger flatness and totally geodesic conclusions are unnecessary here. Applying it to arbitrary P gives a stronger statement than the implication asked for an extremal P, within the specified smooth category.

The source proof passes from odd n to even n through P x [-1,1] with g+dt^2. The product is again a compact full-dimensional convex polytope with a smooth neighborhood metric. R is unchanged. Side-facet mean curvatures are unchanged because the extra principal curvature is zero. The two end facets are totally geodesic. Every old/end adjacent normal pair is orthogonal for both metrics; hence all new interior angles are pi/2. Old angle comparisons persist. Thus the statement has no hidden upper dimension bound or missing even dimension. Since a neighborhood of a convex set may be chosen contractible, the pulled-back tangent bundle has a spin structure; no additional topology condition on D is being imposed.

Nonsimplicity does not make a ridge incident with more than two irredundant facets. A transverse section at a relative ridge-interior point is a pointed two-dimensional convex cone, which has two boundary rays. Each is one facet, and another supporting inequality through the same ridge would be redundant. Therefore intersections of three distinct irredundant facets have codimension at least three, including polytopes with many facets at a vertex. This validates the geometric higher-corner stratification used in the cited source; it does not itself verify the source's analytic estimate.

For n=2, F maps P to an embedded disk whose oriented boundary is a piecewise-smooth Jordan curve. Choose counterclockwise orientation. With outward normal and sphere-positive II convention, smooth-boundary signed turning curvature k equals the mean curvature; for the unit circle both are +1. The turning theorem gives

    sum_i(pi-theta'_i) + integral k ds = 2 pi.

The reference convex polygon has sum_i(pi-theta_i)=2pi. Each theta'_i<=theta_i and k>=0 makes the left side at least 2pi, with a strict excess if even one angle is smaller. Thus every angle is equal. The original comparison excludes reflex corners; continuity and compact smooth arcs give a finite curvature integral. If n=1 is admitted, there is no codimension-two face on which the required strict angle inequality could occur. This is vacuous, not a new rigidity theorem.

## 5. Exact adverse models and what they prove

### A. A smooth weak map can have degenerate pullback

On the square, F(x,y)=(x^3,y) is a face-preserving homeomorphism, smooth on the ambient plane, with inverse smooth on every relative open stratum. Its derivative has rank one at x=0 and its pullback metric is diag(9x^4,1), degenerate on the left edge. Its inverse fails ambient smoothness there. This refutes the inference from weak stratum/interior smoothness to Bi's metric hypotheses. It does not refute the scoped result: the square also has other, genuinely smooth correspondences.

### B. The smooth category genuinely restricts nonsimple polytope pairs

Take two pentagonal pyramids with apex 0 and base plane z=1, with cyclic base vertices

    V=((0,0),(2,0),(3,1),(2,3),(0,2)),
    W=((0,0),(2,0),(3,1),(2,3),(-1,2)).

Both bases are strictly convex: for every oriented edge all other base vertices lie strictly on its left. Thus the pyramids are combinatorially equivalent. Their unique five-valent vertex is the apex. Any smooth corner diffeomorphism would differentiate there to an invertible linear map between the apex tangent cones. Such a map must permute the five extreme rays by a cyclic or reversed-cyclic permutation, because it preserves the facet incidence cycle.

Write r_i=(V_i,1), r'_i=(W_i,1). For each of the ten allowed permutations sigma, solve the exact homogeneous linear system

    A r_i = lambda_i r'_{sigma(i)}  (i=0,...,4)

in the nine entries of A and five lambda_i. Every 15-by-14 coefficient matrix has rank 14 over the rationals. Its only solution is zero, so no invertible A exists. These two combinatorially equivalent convex polytopes therefore have no ambient smooth corner diffeomorphism at their apex, even allowing any combinatorial face correspondence. The exact independent control reproduces all ten ranks.

This example does not satisfy or test simultaneous angle decrease and is not a counterexample to mean-convex extremality. It proves that one cannot broaden the submitted theorem from ambient diffeomorphism to combinatorial equivalence by terminology alone.

### C. Flat Euclidean geometry does not make a competitor mean convex

Let F(x,y)=(x,y+c x^2) on a rectangle. The pullback tensor is

    g=[[1+4c^2 x^2,2cx],[2cx,1]],  det g=1.

Its sole nonzero Christoffel coefficient is Gamma^2_11=2c and all Riemann tensor components vanish. Nevertheless the bottom facet has outward mean curvature 2c/(1+4c^2x^2)^(3/2) and the top facet has its negative. For c>0 the top facet violates mean convexity. Independent symbolic calculations recover both signs from g and from the pushed Euclidean normals. Thus no hidden inference from flatness to the face-curvature hypothesis is being used.

## 6. Source interpretation and exact remaining boundary

The 2017 Question 64 is posed for a diffeomorphic Euclidean domain with corresponding faces and a strict angle inequality somewhere; it does not add metric-size conditions. It does not define a separate convention for 'diffeomorphic' at a nonsimple corner in that paragraph. Gromov's 2013 Section 1 defines a cornered structure using an ambient smooth extension, with tangent bundle restricted from that ambient manifold. This supports the selected interpretation. It is not a proof that every weaker interpretation of the 2017 wording is equivalent.

The strongest verified geometric statement is the theorem application in Sections 1–4, conditional on the imported analytic theorem. The controlling README already states its ambient-smooth restriction and credits Bi. No required geometric repair was identified. The broader corner-singular category remains an exact unsupported gap; neither the model in A nor the pair in B fills it. The independent analytic review and priority assessment are separate gates.
