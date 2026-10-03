# 2100406: a classical obstruction to the literal interior-accumulation question

## Disposition and scope

**Credited negative answer to the literal statement, conditional only on the cited classical Lazutkin theorem.** This is a source-derived correction, not a new-discovery claim or a solution of a strengthened rational/resonant problem. It was identified during the readiness/literature gate; substantive research budget consumed: **0/5**. Independent review is pending.

The catalogue target asks whether a planar billiard must be an ellipse if it has convex caustics with rotation numbers approaching some value strictly between 0 and 1/2. We use a sequence with pairwise distinct rotation numbers, so the conclusion does not depend on allowing a constant sequence.

The exact source is Bolsinov–Matveev–Miranda–Tabachnikov, *Open Problems, Questions, and Challenges in Finite-Dimensional Integrable Systems*: arXiv v1 Question 3.10, printed p.22; arXiv v2 Question 4.10, printed p.17; published 2018 Question 4.10. See [v1](https://arxiv.org/pdf/1804.03737v1), [v2](https://arxiv.org/pdf/1804.03737v2), and the [published text](https://pmc.ncbi.nlm.nih.gov/articles/PMC6158379/). The catalogue's reference to Question 4.6 does not identify this sentence in either inspected arXiv edition.

The original words include “sequence of convex caustics” and “converging to some number” with the displayed condition omega in (0,1/2). No rationality or periodicity qualification appears in that question. The preceding discussion does concern rational caustics. We do not infer or silently supply an intended extra hypothesis.

## The classical input

We use the following consequence of **V. F. Lazutkin's existence theorem**, *The existence of caustics for a billiard problem in a convex domain*, Math. USSR-Izv. 7 (1973), 185–214, [DOI](https://doi.org/10.1070/IM1973v007n01ABEH001932), [official record](https://www.mathnet.ru/eng/im2221).

**Lazutkin input.** For a smooth closed planar table with everywhere positive curvature, there is a set R contained in (0,1/2), of positive one-dimensional Lebesgue measure, such that each rho in R is the rotation number of a smooth closed convex caustic inside the table. The rotation numbers can be taken irrational.

The original paper's pp.185–187 impose finite differentiability and positive upper/lower bounds on curvature radius. Page 186 defines a Diophantine set E(a), states its Lebesgue-measure bound in (0.3), and identifies its elements as rotation-number parameters: “their rotation numbers will run through the set E(a)”; Theorem 1, p.187, supplies the caustics. Thus the measure is genuinely in the rotation-number parameter, not merely planar area or phase-space area. Convexity is part of the paper's definition and construction, not an inference that every invariant circle has a convex envelope. Its p.191 explains the convexity condition (1.10).

For an explicit modern check of the precise parameter formulation, Koudjinan–Ramírez-Ros, *High-order persistence of resonant caustics in perturbed circular billiards*, ETDS 46 (2026), 514–542, **p.515**, states the positive-measure Diophantine rotation-number conclusion and credits Lazutkin; [DOI](https://doi.org/10.1017/etds.2025.10248), [publisher text](https://www.cambridge.org/core/journals/ergodic-theory-and-dynamical-systems/article/highorder-persistence-of-resonant-caustics-in-perturbed-circular-billiards/B4470663ABCF007954C499D182C62173). We use the classical theorem as published, without claiming to reprove KAM theory here.

## An explicit admissible nonellipse

Let theta be the outward normal angle, and put

    h(theta) = 1 + (1/16) cos(3 theta),
    n(theta) = (cos(theta), sin(theta)),
    t(theta) = (-sin(theta), cos(theta)),
    X(theta) = h(theta)n(theta) + h'(theta)t(theta).

This is the support-function parametrization of the boundary of a real-analytic strictly convex body. For completeness, its relevant geometric properties follow directly:

    r(theta) = h(theta) + h''(theta)
             = 1 - (1/2) cos(3 theta),
    1/2 <= r(theta) <= 3/2,
    X'(theta) = r(theta)t(theta).

For fixed theta, the derivative of X(u) dot n(theta), with respect to u, is r(u) sin(theta-u). It is negative on (theta,theta+pi) and positive on (theta+pi,theta+2pi). Consequently X(theta) uniquely maximizes that projection over one full period. The closed regular curve therefore has one supporting point for every normal direction, is embedded, and bounds a strictly convex body with support function h. Equivalently, the body is the intersection of the half-planes x dot n(theta) <= h(theta). The positive bound h >= 15/16 also places the origin in its interior.

Since ds/dtheta = r(theta) > 0, the curvature is 1/r(theta), and the curvature radius is real analytic as a function of arclength as well. All differentiability and nonvanishing-curvature requirements of Lazutkin's theorem are satisfied.

This body is not centrally symmetric about any point. Indeed, central symmetry about c=(c_x,c_y) would make the support function after translation by -c pi-periodic. It would imply

    h(theta)-h(theta+pi) = 2 c_x cos(theta) + 2 c_y sin(theta).

The left side is (1/8) cos(3 theta). Multiplication by cos(3 theta) and integration over [0,2pi] gives pi/8 on the left and zero on the right, a contradiction. Every ellipse is centrally symmetric about its centre; therefore this table is not an ellipse, including after arbitrary translation or rotation.

## Selecting the required interior accumulation

Apply the Lazutkin input to this single fixed table. Obtain the positive-measure rotation set R contained in (0,1/2), with a convex caustic C_rho for every rho in R.

Here is an elementary way to ensure that accumulation does not occur only at zero. Write

    (0,1/2) = union over integers m >= 5 of [1/m, 1/2-1/m].

If every intersection of R with these compact intervals had measure zero, their countable union would have measure zero. Hence some such intersection has positive measure and, in particular, is infinite. By compactness it contains a sequence of distinct numbers rho_n tending to a limit omega in that same compact interval. Thus 0 < omega < 1/2. Distinct rotation numbers entail distinct caustics, because the rotation number is fixed by the dynamics on a caustic. The caustics C_rho_n meet the literal hypothesis, while the table is not an ellipse.

One can even arrange omega in R, hence irrational: the isolated points of any subset of the real line form a countable set (assign a rational-endpoint interval isolating each point). Since R is uncountable, it has a nonisolated point in itself, to which a sequence of distinct members converges. The compactness argument already suffices for the target and does not need this refinement.

This proves the claimed literal negative answer.

## What this does not prove

- It does not produce rational or resonant caustics. The selected rotation numbers are irrational.
- It does not settle any conjecture in which the sequence is required to be rational/resonant, or its limit is prescribed in advance.
- It does not imply a foliation by caustics on an open region. A positive-measure Cantor family is enough here.
- It does not contradict the endpoint rigidity theorem for convex caustics whose rotation numbers approach 1/2. The limit here lies strictly inside the interval.
- It does not resolve the Birkhoff integrability conjecture, reflection symmetry of caustics, higher-dimensional invariant-hypersurface questions, or commuting billiard-map questions.

The mathematical mechanism and existence theorem are classical and credited to Lazutkin. We have not located a source explicitly announcing this exact question as corrected; this certificate records the direct consequence of the published theorem for the wording that is actually printed. No claim about what the proposers intended is made.
