# Attempt 4: balanced-normal moment inequality

2026-10-03 08:19 UTC. Substantive author turn 4/5. Outcome: quantitative necessary condition on a counterexample, not a resolution. Estimated progress: 30% (subjective).

## A weighted finite bound

For an orbit passing the finite test, define

    a_i=|u_(i-1)-u_i|, A=sum_i a_i, lambda_i=a_i/A,
    sigma=sum_i lambda_i^2, n_i=(u_(i-1)-u_i)/a_i,
    y_i=x_i-n_i, c=sum_i lambda_i y_i.

Then sum_i lambda_i n_i=0 by telescoping, and

    L = sum_i x_i.(u_(i-1)-u_i)
      = A sum_i lambda_i x_i.n_i.

The first identity is obtained by grouping the terms involving each edge u_i: (x_(i+1)-x_i).u_i is its length. Since x_i=y_i+n_i,

    L/A = 1 + sum_i lambda_i (y_i-c).n_i
         >= 1 - sqrt(sum_i lambda_i |y_i-c|^2).

Here weighted Cauchy–Schwarz uses sum_i lambda_i |n_i|^2=1. The variance identity and diam({y_i})<=1 give

    sum_i lambda_i |y_i-c|^2
      = (1/2) sum_(i,j) lambda_i lambda_j |y_i-y_j|^2
      <= (1-sigma)/2.

Consequently every feasible orbit satisfies the exact inequality

    L >= A [1 - sqrt((1-sigma)/2)]
      = A - sqrt((A^2-sum_i a_i^2)/2).                 (M)

No differentiability of K or uniqueness of reflection normals is used. These are the selected normals determined by the orbit.

## Why A is at least 4

The original edge lengths l_i are positive and sum_i l_i u_i=0. Hence the unit vectors u_i have origin in their convex hull. Any ball containing all of them has radius at least 1: for weights mu_i=l_i/L and any center z,

    sum_i mu_i |u_i-z|^2=1+|z|^2 >= 1.

On the other hand, every closed polygonal curve of perimeter A lies in some ball of radius A/4. Choose two points p,q dividing its arclength into equal halves. Each point v lies on a half of length A/2, so |v-p|+|v-q|<=A/2. Triangle inequality about the midpoint gives |v-(p+q)/2|<=A/4. Apply this to the closed polygon through the u_i in cyclic order, whose perimeter is A. Therefore A>=4.

Together with sigma>=1/m, (M) yields

    L >= 4 [1-sqrt((m-1)/(2m))].                      (B)

For m=4 this is 4-sqrt(6), approximately 1.550510257, still below 2. In ambient dimension n, using m<=n+1 gives 4[1-sqrt(n/(2(n+1)))]. This is consistent with the classical inradius/Jung bound and is not asserted as a new global estimate. The orbit-specific version (M) retains angular information lost in that dimension-only specialization.

## A concrete exclusion region and the remaining gap

If

    A > 2 / [1-sqrt((1-sigma)/2)],

then L>2, excluding the orbit from the shortest class. In particular, for four bounces, A>2/[1-sqrt(3/8)] (approximately 5.15959) suffices regardless of the individual weights. Equality at this threshold gives only L>=2 and requires separate equality analysis; it is not silently promoted to strictness.

Thus a four-bounce counterexample must have relatively small total chordal turn A. There is no proof here that the full XX/XY/YY constraints force A above the threshold. A near-retracing sequence of arbitrary polygons can have A near 4; ruling out its constant-width realization is the missing geometric step. The inequality is a quantitative filter, not an argument that that missing step holds.
