# Attempt 2: an exact finite antipodal-completion test

2026-10-03 08:12 UTC. Substantive author turn 2/5. Outcome: exact reformulation; no counterexample or universal lower bound. Estimated progress: 25% (subjective).

## Finite realization theorem

Let x_1,...,x_m be a closed polygon in Euclidean space, with nonzero consecutive edges and nonzero reflection differences u_(i-1)-u_i. Put

    u_i = (x_(i+1)-x_i)/|x_(i+1)-x_i|,
    n_i = (u_(i-1)-u_i)/|u_(i-1)-u_i|,
    y_i = x_i-n_i,
    S = {x_1,...,x_m,y_1,...,y_m}.

Then this ordered polygon is a generalized billiard trajectory in **some** Euclidean constant-width-1 body if and only if diam(S)<=1.

Necessity follows from Attempt 1: n_i is a supporting normal, so its antipode y_i belongs to the same body, whose diameter is 1.

For sufficiency, use the classical Euclidean completion theorem: every bounded set of diameter 1 is contained in a body of constant width 1. The hypothesis gives diameter exactly 1 because |x_i-y_i|=1. Choose such a completion K. For every z in K, |z-y_i|<=1. Since x_i-y_i=n_i, expansion gives

    2 (z-x_i).n_i + |z-x_i|^2 <= 0.

Thus (z-x_i).n_i<=0: n_i supports K at x_i and the displayed polygon has precisely the required reflection law. The completion has nonempty interior by the classical theorem. No smoothness or uniqueness of completion is needed.

### Credited completion input

This is the Euclidean Meissner theorem together with existence of diametric completions, not an original theorem here. See Ethan Akin, *Maximal r-Diameter Sets and Solids of Constant Width*, https://arxiv.org/abs/1003.5824 ; and J. P. Moreno and R. Schneider, *Lipschitz selections of the diametric completion mapping in Minkowski spaces*, Advances in Mathematics, https://doi.org/10.1016/j.aim.2012.10.005 . The latter introduction explicitly states both Euclidean equivalence and existence of completions of any bounded set. These facts are special to Euclidean geometry for the present use; no analogous assertion for arbitrary norms is assumed.

## Scale separation

For a fixed polygonal shape q_i, set x_i=t q_i with t>0. Its edge directions and n_i do not change with scale. Put d_ij=q_i-q_j and D_ij=|d_ij|^2. Every diameter constraint becomes one of

    t^2 D_ij <= 1,                                      (XX)
    t^2 D_ij + 2t d_ij.n_j <= 0,                        (XY)
    t^2 D_ij - 2t d_ij.(n_i-n_j) + |n_i-n_j|^2 <= 1.   (YY)

All ordered XY pairs are needed; XX and YY can be indexed by i<j. The i=j XY constraints are exact equalities. For a shape with perimeter 1, the objective length is t. Thus feasibility for a fixed shape is an intersection of explicit quadratic intervals, rather than a search over arbitrary bodies or support functions.

## Exact consequences and equality warning

A feasible polygon of length <2 would refute the source conjecture: its completion has shortest length <= that length, while every two-bounce orbit has length 2. A feasible non-two-bounce polygon of length exactly 2 also refutes the source conjecture, although by a case split: if the completion's minimum is <2, no minimizing orbit is two-bounce; if the minimum is 2, the supplied polygon is a higher-period minimizer. Existence of a shortest orbit is the credited Bezdek–Bezdek theorem. Therefore the original conjecture is equivalent to the assertion that every feasible primitive polygon other than a two-bounce segment has length strictly >2. This equivalence does not establish the inequality.

The test gives a complete finite witness format for a counterexample. It does not make the unbounded-dimensional problem finite: m and the ambient dimension remain unbounded. Even after restricting to m<=n+1 for shortest orbits, an all-dimensional inequality is still needed. Numerical optimization cannot substitute for that inequality or certify an exact equality case.
