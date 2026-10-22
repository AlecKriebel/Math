# Hilbert-space quasiconformality: radial reduction and ball roundness

Status: unresolved original problem; two substantive approaches. Independent review pending. This package does not establish the general implication from metric quasiconformality to quasisymmetry. No novelty claim.

## 1. Exact source and conventions

Kapovich, *Problems on boundaries of groups and Kleinian groups*, October 24, 2007, Problem 49 (Juha Heinonen), printed p.14, asks whether the Euclidean chain “quasiconformal implies quasisymmetric implies balls map to quasiballs” remains true in Hilbert spaces. The preceding sentence explicitly assumes Euclidean dimension at least two. Despite the collection's title, this is not a group-boundary realization question. Primary source: https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf .

We use real Hilbert spaces of dimension at least two, global self-homeomorphisms, and metric linear dilatation

H_f(x) = limsup_{r down to 0} (sup_{||y-x||=r} ||f(y)-f(x)||)/(inf_{||y-x||=r} ||f(y)-f(x)||).

This is the everywhere-bounded definition in Väisälä, *The Free Quasiworld*, Section 1.1, equations (1.2), printed p.56, https://matwbn.icm.edu.pl/ksiazki/bcp/bcp48/bcp4814.pdf . We do not replace this hypothesis by freely quasiconformal (FQC) maps. The latter theory has additional hypotheses and its theorems do not automatically settle this question. The source passage does not define “quasiball”; Section 2 proves an explicit concentric-ball estimate rather than assuming a stronger unstated meaning.

A global map is eta-quasisymmetric if eta is an increasing homeomorphism of [0,infinity) onto itself and, for distinct x,a,b,

||f(a)-f(x)|| / ||f(b)-f(x)|| <= eta(||a-x||/||b-x||).

## 2. Quasisymmetry gives uniform ball roundness without compact spheres

**Proposition.** If f:H->H is a global eta-quasisymmetric homeomorphism, then for every x and r>0 there are 0<l<=L<infinity such that

B(f(x),l) subset f(B(x,r)) subset B(f(x),L), and L/l <= eta(1).

**Proof.** Define L as the supremum of ||f(y)-f(x)|| over ||y-x||<r and l as the infimum of ||f(z)-f(x)|| over ||z-x||>=r. Select z0 on the sphere and set b=||f(z0)-f(x)||>0. Quasisymmetry shows L<=eta(1)b. Applying it to z0 and each exterior z gives b<=eta(1)||f(z)-f(x)||, so l>=b/eta(1)>0. For every interior y and exterior z, the same inequality gives ||f(y)-f(x)||<=eta(1)||f(z)-f(x)||. Taking the supremum and infimum proves L<=eta(1)l. Moreover l<=b, while radial interior points tending to z0 show L>=b by continuity; hence l<=L.

Surjectivity and the definition of l show the inner inclusion: a preimage of a point at distance less than l cannot be exterior. Every interior image point has distance at most L. Equality cannot occur, since f(B(x,r)) is open; a small outward displacement from a noncentral equality point would have distance greater than L and still belong to this open image. Since L>0 the central point is not an equality case. This proves the strict outer-ball inclusion. No sphere compactness or attainment of a supremum was used. QED.

This establishes bounded eccentricity with center f(x). It is not a claim that every bounded-eccentricity domain is a quasiball in a stronger extension, uniform-domain, or boundary-parametrization sense.

## 3. A restricted radial class reduces to three dimensions

**Theorem.** Let rho:[0,infinity)->[0,infinity) be an increasing homeomorphism with rho(0)=0. Set f(0)=0 and f(x)=rho(||x||)x/||x|| for x nonzero. If H_f(x)<=K everywhere on H, then f is globally quasisymmetric with distortion depending only on K and on whether dim H=2 or dim H>=3, not on any larger ambient dimension.

**Proof.** Every linear subspace E is preserved, and f|E is a global self-homeomorphism of E. For a center x in E and radius r, the sphere in E is a subset of the sphere in H. Consequently the numerator for E is at most the numerator for H and the denominator for E is at least the denominator for H. Whenever the ambient quotient is finite this gives its restricted counterpart no larger; the extended-value interpretation gives the same conclusion otherwise. Taking limsups yields H_{f|E}(x)<=K.

If dim H>=3, any triple x,a,b is contained in a three-dimensional linear subspace E (extend their span if necessary). Identify E isometrically with R^3. The Euclidean global metric-QC-to-QS theorem provides one distortion function eta_{K,3} for every such restriction. This theorem is stated in Väisälä Section 6.9, printed p.76; its parameter K uses the metric definition of Section 1.1. Applying it to the given triple proves the global assertion. If dim H=2, apply the same theorem in R^2. QED.

This is an application of a published theorem, not an independent reconstruction of Euclidean quasiconformal theory. The invariant three-dimensional-subspace mechanism is already explicit for radial power maps in Väisälä Section 6.8(2)(a), printed p.75. We credit that mechanism and make no priority claim for the stated extension to general radial homeomorphisms.

For a C1 rho with positive derivative at r>0, the derivative has radial eigenvalue rho'(r) and tangential eigenvalue rho(r)/r. Thus at nonzero points the infinitesimal distortion bound is equivalent to 1/K <= r rho'(r)/rho(r) <= K. If these inequalities hold for all r>0, integration gives (R/r)^(1/K) <= rho(R)/rho(r) <= (R/r)^K for R>=r>0. At the origin the radial map has equal image radii, so H_f(0)=1. These are useful restricted diagnostics, not a criterion for arbitrary maps.

## 4. Dimension-one caution and exact remaining gap

The exclusion of dimension one matters. The homeomorphism f(t)=sinh(t) of R is differentiable with positive derivative and hence H_f(x)=1 at every x. But the equal-distance triple (x,a,b)=(t,2t,0) gives the image-distance ratio 2 cosh(t)-1, unbounded as t tends to infinity. Thus it is not quasisymmetric. This is not a counterexample to the intended dimension-at-least-two or infinite-dimensional problem.

For a general Hilbert-space homeomorphism, the image of the span of a triple need not remain in that subspace or in any fixed-dimensional Euclidean space. Projection cannot repair this without losing injectivity and the relevant metric estimates. The reduction in Section 3 therefore does not establish metric-QC-to-QS in general. The exact meaning of “quasiball” in the brief original passage is also not supplied. The original target remains unsolved by this package.

## 5. Verification boundary

The checker performs exact rational tests of radial cubic maps, orthogonal changes of coordinates, and radial/tangential derivative formulas. These test algebraic identities, not all Hilbert-space homeomorphisms, sphere compactness, or the imported Euclidean theorem. The proofs and source scope above carry those logical obligations.
