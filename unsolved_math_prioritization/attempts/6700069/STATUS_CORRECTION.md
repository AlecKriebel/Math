# Later-literature resolution of Gromov's Question [?73][c]

Problem 6700069 / AMR-066-0069. Source assessment on 2026-10-01. Proposed status: **already_solved, 0/5 author research turns**, pending independent source/application review. The answer is negative in the original geometric sense, by a direct application of the published ball-map theorem of Berdnikov–Guth–Manin. No new proof of that theorem or historical novelty is claimed.

## 1. Exact question and category

Gromov's *101 Questions, Problems and Conjectures around Scalar Curvature*, October 1, 2017, printed page 72, Question [?73][c], asks about a fixed Riemannian manifold S homeomorphic to the connected sum of twenty copies of S^2 times S^2. It asks for 1-Lipschitz maps f_R from the Euclidean four-ball of radius R to S, for unbounded R, with evaluation of a fixed fundamental cohomology cocycle at least c(S) R^4 for some positive constant. A closed four-form is an explicitly offered representative.

The complete context on pages 71–72 specifies Euclidean balls, fixed target metrics, and quantitative evaluation of geometric cocycles. It imposes no scalar-curvature inequality on this question, despite the title of the containing list. It also imposes no constant boundary condition, no requirement that all f_R extend one fixed map on R^4, no quasiregular distortion bound and no prescribed smooth structure beyond S being a Riemannian manifold of the stated homeomorphism type.

For a smooth closed fundamental four-form h, the evaluation is the signed integral integral_(B^4(R)) f_R^*h. We prove that its absolute value is o(R^4), uniformly over all 1-Lipschitz maps at each R. Thus even an arbitrary sequence of different ball maps cannot have the requested positive lower bound.

The statement is about fixed controlled geometric representatives, as in the source discussion. An arbitrary unbounded algebraic singular cochain can have pathological values on noncycles and is not a metric evaluation covered by that discussion. We do not replace the source's geometric evaluation by that unrelated convention. The smooth-form case is proved for every representative, with the exact boundary correction; cocycle representatives differing by a bounded geometric coboundary have the same asymptotic conclusion.

## 2. Published theorem with the required ball quantifier

Aleksandr Berdnikov, Larry Guth and Fedor Manin, *Degrees of maps and multiscale geometry*, Forum of Mathematics, Pi 12 (2024), e2, 1–48, DOI 10.1017/fmp.2023.33, **Theorem 2.3**, printed page 5, states the following. If M is a closed connected oriented n-manifold whose real cohomology algebra does not embed into the exterior algebra of R^n, then there exists alpha(M)>0 such that, for a fixed Riemannian metric g and every L-Lipschitz map F:B^n(1)->M,

    integral_(B^n(1)) F^*dvol_M <= C(M,g) L^n (log L)^(-alpha(M))   (2.1)

for large L. The estimate is uniform in F. The full proof is in Section 2.3, especially its ball adaptation in Section 2.3.1, printed page 24.

This is a theorem for arbitrary maps of a ball, not merely self-map degrees or the restriction of one global map. No formality or simple-connectivity hypothesis is imposed in Theorem 2.3. Such extra conditions occur in different introduction theorems but are unnecessary here.

The bound also holds with the absolute value of the integral: apply (2.1) to F and to F composed with an orientation-reversing Euclidean reflection of the ball. Both have the same Lipschitz constant. It is the signed pullback integral that is bounded; no assertion that the unsigned multiplicity integral is subvolume is made.

## 3. Topological obstruction for the requested target

A manifold homeomorphic to #20(S^2 times S^2) is closed, connected and orientable. Its real Betti numbers are

    (b_0,b_1,b_2,b_3,b_4)=(1,0,40,0,1).

Indeed each S^2 times S^2 contributes two degree-two generators, and connected sum adds the middle cohomology; equivalently its intersection form is the orthogonal sum of twenty hyperbolic planes. These facts depend only on the homeomorphism type, not on a choice of smooth structure.

A graded algebra injection into the exterior algebra of R^4 would inject the 40-dimensional degree-two space into a six-dimensional space, which is impossible. Even disregarding grading, the total real dimensions are 42 and 16, respectively, so an injective real-algebra map is impossible. Therefore Theorem 2.3 applies to every Riemannian metric and every smooth structure allowed in the question. No claim about existence of a special curvature metric is needed.

## 4. Scaling the published estimate correctly

Given any 1-Lipschitz f_R:B^4(R)->S, define F_R(u)=f_R(Ru) on B^4(1). Then Lip(F_R)<=R. Change of variables for pullbacks gives

    integral_(B^4(1)) F_R^*dvol_S
       = integral_(B^4(R)) f_R^*dvol_S.                         (4.1)

There is no additional R^4 factor outside this identity: it is already present in the pullback under the dilation u->Ru. Applying (2.1) with L=R and using reflection for the negative sign yields

    |integral_(B^4(R)) f_R^*dvol_S|
       <= C(S,g) R^4 (log R)^(-alpha(S)).                       (4.2)

Since alpha(S)>0, this is o(R^4), uniformly over the whole family of maps. The maps need not be compatible as R varies. A claim only about a single map R^4->S would not have been enough; the published ball theorem supplies exactly the needed stronger quantifier.

## 5. An arbitrary fixed smooth fundamental representative

Choose the orientation and normalize a fundamental representative h by integral_S h=1; any other fixed nonzero normalization changes only constants. Put V=volume_g(S). De Rham theory gives a smooth three-form eta on compact S such that

    h = V^(-1) dvol_S + d eta.                                 (5.1)

The primitive eta is bounded in comass because S is compact. Stokes's theorem for Lipschitz pullbacks gives

    integral_(B^4(R)) f_R^*d eta
       = integral_(partial B^4(R)) f_R^*eta.

The boundary restriction remains 1-Lipschitz. Consequently

    |integral_(partial B^4(R)) f_R^*eta|
       <= ||eta||_infinity area(S^3(R))
       = 2 pi^2 ||eta||_infinity R^3.                          (5.2)

If the source ball is regarded as open, the map extends to its closure by completeness of the compact target; the same statement follows by exhaustion or the Lipschitz Stokes formula. One can also obtain the formula by smooth approximation in local charts, or a tubular embedding and projection, with uniform Lipschitz bounds. No vanishing boundary data is assumed.

Combining (4.2)–(5.2), for all sufficiently large R,

    |h(f_R)| <= (C(S,g)/V) R^4 (log R)^(-alpha(S))
                 + 2 pi^2 ||eta||_infinity R^3 = o(R^4).        (5.3)

Here h and the metric are fixed. The constants need not be uniform over R-dependent choices of representatives or metrics, which the original question does not request. For a controlled geometric cocycle differing from h by a coboundary whose boundary evaluation is O(R^3), precisely the same conclusion follows. The source's quantitative evaluation convention is the one used in this correspondence.

Equation (5.3) excludes the requested c(S)>0 along every unbounded sequence of radii. This is the negative answer obtained from the already published theorem.

## 6. Reading the theorem's proof and avoiding inappropriate substitutes

The source proof was read, including its Fourier-localized primitive estimates, the cohomology-relation argument and the ball extension. Here is a short verification map, not a newly claimed replacement proof.

In Section 2.3, normalized pullbacks of representative forms are uniformly bounded, while normalized primitives of the algebra relations are O(L^(-1)). Failure of a cohomology-algebra embedding forces the top-degree value to be quantitatively small when the relations are nearly satisfied, by the real Nullstellensatz (Lemma 2.19). Littlewood–Paley localization and averaging across logarithmically many scales yield a strictly positive logarithmic-loss exponent. The exponent is allowed to depend on the cohomology algebra; no explicit value is needed here.

The ball argument in Section 2.3.1 extends F from B(1) to B(2) by F(u/|u|) in the outer annulus. This is uniformly O(L)-Lipschitz and has derivative rank at most n-1 in that annulus. Hence its pulled-back top form vanishes there almost everywhere. A cutoff equal to one on B(1) recovers the unweighted ball integral from the localized estimate. This is why no boundary condition is required. It also confirms that one need not glue the family f_R into a global map.

The final published edition, not only the earlier author/NSF copy, was checked. Its theorem numbering and full assumptions agree. This is a source-status correction and standard application, with zero fresh author research turns. A separate independent review of exact source coverage and all normalization steps is required before publication.
