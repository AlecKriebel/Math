# Attempt 1: project the reflection law to its affine span

2026-10-03 08:08 UTC. Substantive author turn 1/5. Outcome: rigorous reduction, full target unresolved. Estimated progress toward a full resolution: 15% (subjective).

## Lemma: antipodes and strict convexity

If K has constant width 1, its diameter is 1. Indeed, for x,y in K, choose u=(x-y)/|x-y|. Then |x-y| <= h_K(u)+h_K(-u)=1; conversely each pair of support planes is distance 1 apart. Given a supporting point x with unit outward normal u, choose y in the opposite support plane. We have (x-y).u=1 and |x-y|<=1, so equality in Cauchy–Schwarz forces y=x-u. The same argument with this y and any other point in the original support plane shows that x is unique. Thus K is strictly convex (its boundary can nevertheless be nonsmooth), and every supporting normal at x has antipodal point x-u in K.

Every such diametral segment [x,x-u] is a two-bounce trajectory of total length 2. In particular the shortest length is at most 2. A two-bounce trajectory must be perpendicular to its two support planes, so its chord length is 1 and its total length is exactly 2.

## Proposition: every planar orbit is harmless

Let P=(x_1,...,x_m) be a generalized billiard trajectory of K whose affine span A has dimension two. Orthogonally project K to A, obtaining C. For each direction u parallel to A, the supporting values of C equal those of K after the harmless choice of origin in A; hence C has constant width 1. At x_i the reflection normal n_i is a linear combination of the adjacent unit edge directions, so n_i lies parallel to A. Since n_i supports K at x_i, it supports C there as well. All edges, lengths and reflection vectors of P are unchanged under the projection. Consequently P is a generalized billiard trajectory of the planar constant-width body C.

By the credited planar theorem, C's minimum billiard length is 2 and all its minimizing trajectories have period 2. Therefore length(P) >= 2, with equality only for a two-bounce trajectory. No assumption of smooth boundary was used in the projection step. The affine-dimension-one case is the interval of width 1 and gives the same conclusion directly.

It follows that **every genuinely higher-period planar orbit in a constant-width body, regardless of the ambient dimension, has length strictly greater than 2**. Such an orbit cannot be a shortest one in K.

## Consequences and limit of this route

Combining this with Bezdek–Bezdek Theorem 1.1, any counterexample in R^3 must have a minimizing four-bounce orbit whose vertices are affinely independent. In R^n any non-two-bounce minimizer must have at least four vertices, span dimension at least three, and have at most n+1 vertices. The statement does not show that all shortest orbits are planar. Projections to an arbitrary plane generally lose the reflection law because the normals need not lie in that plane; that missing step cannot be assumed.

This reduces the first unresolved dimension to nonplanar tetrahedral four-orbits but does not exclude them. The next attempt will encode exactly when finitely many reflection contacts can lie in a constant-width completion.
