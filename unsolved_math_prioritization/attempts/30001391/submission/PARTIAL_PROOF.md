# Restricted bounds for degenerate Herman curves

Status: author candidate for independent audit. These statements do not settle the unrestricted periodic-curve question in Oberwolfach Problem 2(2).

## A. A pole-count bound for individually invariant curves

Let f be a rational map of degree d >= 2. Let C_1,...,C_N be distinct Jordan curves such that:
1. f(C_i)=C_i and f restricted to C_i is topologically conjugate to an irrational rotation;
2. C_i is contained in the Julia set J(f);
3. C_i is not a boundary component of a Siegel disk or Herman ring.

Then N <= d-1. No smoothness, analyticity, or exclusion of spherical circles is required for this restricted assertion.

Proof.
(a) The curves are pairwise disjoint. If x lies in C_i intersect C_j, its forward orbit is dense in both curves. The orbit closure is unique, so C_i=C_j.

(b) A rational map of degree at least two has a fixed point q on the sphere. No C_i contains q, because irrational rotation has no periodic points. Conjugate by a Möbius map taking q to infinity. Thus infinity is a fixed point and hence a pole of f on the sphere. The total pole multiplicity is d; at most d-1 remains at finite points.

(c) A union of N disjoint Jordan curves on the sphere has N+1 complementary regions. In the coordinate of (b), exactly N of them are bounded. Every boundary component of each such region U is one of the C_i, and is mapped onto itself with its orientation preserved. (Orientation preservation of a circle homeomorphism does not depend on which of its two orientations is chosen.)

(d) Suppose one bounded region U contains no pole. There is no pole on its boundary either, since every boundary curve is invariant and avoids infinity. For w outside the boundary, the argument principle gives

  number of zeros of f(z)-w in U, counted with multiplicity
       = winding(f(boundary U),w)
       = winding(boundary U,w)
       = 1 if w is in U, and 0 if w is outside its closure.

The boundary is oriented positively with respect to U, including negative orientation on its hole boundaries. The argument principle here is the topological winding-number version for finitely connected Jordan regions, so rectifiability is not assumed. One can equivalently replace boundary components by close curves in a pole-free neighborhood and use invariance of winding numbers.

No interior point maps onto the boundary: the open mapping theorem would then yield images outside the closure of U, contradicting the zero count. Consequently f:U -> U is a bijective holomorphic map, and its local multiplicities are one. It is therefore a conformal automorphism.

(e) Since U is bounded and all iterates map U into U, the iterates are a normal family there. Thus U is contained in a Fatou component V. Every boundary component of U is in J(f), so a path in V cannot leave U; therefore V=U.

Use the standard classification of invariant Fatou components of a rational map of degree at least two: attracting or parabolic basins, Siegel disks, or Herman rings. Because f:U->U is a conformal automorphism, U cannot be an attracting basin (an automorphism of a hyperbolic domain with an interior fixed point cannot have multiplier of modulus less than one). If U is a parabolic basin, its parabolic fixed point belongs to the boundary, which is a union of C_i, contradicting the lack of periodic points there. Hence U is a Siegel disk or a Herman ring. This contradicts assumption (3) for its boundary curves.

(f) Every bounded region therefore contains at least one finite pole. Distinct regions are disjoint. There are at most d-1 finite poles counted with multiplicity, giving N <= d-1. This bound on arbitrary finite families also proves that an infinite family of individually invariant curves satisfying (1)-(3) cannot exist. QED.

Scope cautions. The result counts individually f-invariant curves, not all f-periodic curves and not cycles without a period restriction. For curves whose periods all divide L, apply it to f^L to obtain at most d^L-1 such curves. Since L can grow, this does not yield a degree-only bound for all periodic curves. The bound is not claimed sharp or novel. The 2025 invariant formulation and the 2009 periodic formulation must not be silently identified.

## B. At most one periodic spherical circle

Let f have degree d>=2. There is at most one spherical circle C such that some iterate maps C homeomorphically onto itself with irrational rotation number.

Proof. Suppose C and D are distinct such circles. Choose a common iterate g=f^L preserving both. The restrictions still have irrational rotation number, and have no periodic points. If C and D intersect, their intersection has one or two points and is forward invariant under g. It would contain a periodic point, a contradiction. Thus C and D are disjoint.

Let sigma_C and sigma_D be the anti-Möbius reflections in the circles. On C, g sigma_C = sigma_C g; the identity principle extends this identity to the sphere. The same holds for D. Hence g commutes with the Möbius transformation T=sigma_D sigma_C.

The composition of reflections in disjoint circles is loxodromic with a positive real multiplier different from one. For completeness, map C to the unit circle and arrange D inside it, then rotate so D has real center a>=0 and radius r>0 with a+r<1. The transformation sigma_D sigma_C is

  T(z) = (a+(r^2-a^2)z)/(1-a z).

Its matrix has determinant r^2>0 and trace 1+r^2-a^2. The discriminant is

  ((1-r)^2-a^2)((1+r)^2-a^2)>0.

Thus its two eigenvalues are distinct and positive. In a Möbius coordinate T becomes z -> lambda z with lambda>0 and lambda !=1.

Write G for g in that coordinate. It satisfies G(lambda z)=lambda G(z). The Laurent expansion at zero has coefficients a_k with (lambda^k-lambda)a_k=0. Only k=1 is possible. Hence G(z)=a_1 z locally, and therefore globally by rational identity. Its degree is one, contrary to deg(g)=d^L>=2. QED.

Scope cautions. This bounds only the spherical-circle subcase permitted in the 2009 wording. The modern Yang/Eremenko definition excludes circles altogether. It says nothing about noncircular analytic or smooth curves.

## C. Critical-point charging for a restricted class

For distinct periodic Jordan curves on which return maps are conjugate to irrational rotations, any finite family becomes individually invariant under a common iterate; the density-of-orbits argument in A(a) shows these curves are disjoint. Therefore the number of those curves that contain a critical point of f is at most 2d-2, by Riemann-Hurwitz. Likewise, there are at most 2d-2 cycles that contain a critical point of f somewhere on their component curves.

This is not a bound on all component curves in such cycles, since their periods could be arbitrarily large, and it is not a bound on critical-point-free curves. Yang's smooth cubic examples in his Theorem A are critical-point-free, as explicitly checked in the construction. Thus a universal charge to an on-curve critical point is unavailable.

## D. Analytic conjugacy creates a Fatou collar

Suppose an analytic embedding h of the unit circle extends univalently to an open annulus around it and satisfies F(h(z))=h(lambda z) on the circle, where F is an iterate of f and lambda is an irrational unit multiplier. The identity principle extends the relation to a smaller circular annulus, invariant under z->lambda z. Every iterate F^n is conjugate there to z->lambda^n z, so the iterates are normal on its image. Thus the image circle is contained in the Fatou set, and cannot be a Julia-set degenerate curve.

The missing step in using this to bound analytic degenerate curves is substantial: an analytic invariant curve with a merely topological irrational conjugacy need not be supplied with an analytic linearizing conjugacy. The argument does not manufacture one, nor give any bound for the cases where it fails.

## E. A support obstruction to parameter counting

A finite union of C^1 Jordan curves has planar area zero: each curve is the image of a compact interval under a piecewise Lipschitz parametrization, and covering the interval by O(1/epsilon) subintervals covers the image by O(1/epsilon) disks of radius O(epsilon), of total area O(epsilon). Consequently a Beltrami coefficient supported only on such a union is zero almost everywhere. The measurable Riemann mapping theorem then gives only a Möbius map (the identity after the usual three-point normalization).

Therefore the standard deformation-parameter count for genuine Herman annuli cannot be copied by placing one independently variable Beltrami coefficient on each smooth degenerate curve. Open annuli have area and conformal modulus; the curves alone do not. A proposed replacement would need a simultaneous thickening/welding theorem for every finite collection, preserving rational degree, irrational dynamics, and distinct cycles. No such theorem is established here. Existing constructions of particular curves do not provide it.

## Dependencies

- The rational Fatou-component classification used in A(e) is Theorem 2.1 of C. McMullen and D. Sullivan, *Quasiconformal homeomorphisms and dynamics III: The Teichmüller space of a holomorphic dynamical system*, author PDF, https://people.math.harvard.edu/~ctm/papers/home/text/papers/qciii/qciii.pdf.
- The total critical multiplicity 2d-2 used in C is the Riemann-Hurwitz formula for a degree-d map of the sphere.
- The normal-family, identity-principle, argument-principle, and Schwarz-Pick facts invoked here are standard complex-analysis results. This packet includes no machine proof of them.
