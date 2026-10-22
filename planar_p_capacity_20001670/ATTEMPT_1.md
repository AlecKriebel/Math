# Attempt 1: an area--diameter improvement

Status: a proved partial comparison, conditional only on the cited classical
triangle-reduction and isocapacitary theorems. The original conjecture remains
open. This is a substantive proof attempt; source retrieval is not counted.

Write `q=2-p`, `b_p=C_p(B_1)=2*pi*((2-p)/(p-1))^(p-1)`, and
`c_p=C_p([0,1])`. Normalize the perimeter to 2, so the target segment has length
1 and capacity `c_p`.

## 1. Combine two genuinely different lower bounds

For a triangle of area `A` and longest side `a`, monotonicity and the sharp
isocapacitary inequality give

\[
 C_p(T)\geq\max\{c_pa^q,\ b_p(A/\pi)^{q/2}\}.                 \tag{1}
\]

The second bound follows by Schwarz rearrangement of admissible functions: their
radially decreasing rearrangements have no larger p-energy and contain a disk
of area `A` in their superlevel set of level one. Approximation, followed by the
infimum, yields the capacity of that disk. No perimeter rearrangement is being
asserted.

For the unit segment, the perimeter of its distance-r parallel set is
`2+2*pi*r`. Testing with functions of distance to the segment and minimizing the
one-dimensional weighted energy gives

\[
 c_p\leq\left[\int_0^\infty(2+2\pi r)^{-1/(p-1)}\,dr\right]^{1-p}
       =b_p\pi^{-q}.                                         \tag{2}
\]

One can first use a positive inner distance cutoff and finite outer cutoff and
then pass to the limits. This produces smooth admissible approximants. This
parallel-set method is classical; see van den Berg--Gavitone, Theorem 1.
Dividing (1) by `c_p` and using (2) therefore gives

\[
 \frac{C_p(T)}{c_p}\geq\max\{a,\sqrt{\pi A}\}^{q}.             \tag{3}
\]

Unlike the longest-side argument alone, area can help at nearly equilateral
triangles, exactly where the previous factor `2/3` is weakest.

## 2. Optimize the geometric bound exactly

Order the sides as `a >= b >= c`, with `a+b+c=2`. Then `2/3 <= a < 1` and
`(2-a)/2 <= b <= a`. Heron's formula reads

\[
 A^2=(1-a)(1-b)(a+b-1).
\]

For fixed `a`, the product `(1-b)(a+b-1)` is a concave quadratic in `b`,
symmetric about `(2-a)/2`, hence decreasing on the admissible interval.
Consequently

\[
 A\geq(1-a)\sqrt{2a-1},                                    \tag{4}
\]

with equality at the isosceles triangle whose two longer sides both equal `a`.
The right side of (4) decreases on `[2/3,1]`: its derivative is
`(2-3a)/sqrt(2a-1)`.

Let `rho` be the unique solution in `(2/3,1)` of

\[
 \rho^2=\pi(1-\rho)\sqrt{2\rho-1}.                           \tag{5}
\]

Uniqueness follows because the left side is strictly increasing and the right
side strictly decreasing, with opposite ordering at the two endpoints. If
`a >= rho`, the first term of (3) is at least `rho`. If `a <= rho`, (4) makes
the second term at least `rho`. Thus

\[
 C_p(T)\geq \rho^{2-p}c_p.                                  \tag{6}
\]

The numerical value `rho = 0.7472461733...` is illustrative; equation (5), not
floating-point computation, defines the constant.

## 3. Pass to all convex sets

Capacity is Hausdorff-continuous on compact convex planar sets. An elementary
proof splits into an interior limit, a segment limit (using the converging
endpoint chord), and a point limit; upper semicontinuity follows directly by
neighborhood admissibility. After translation, fixed-perimeter sets are
uniformly bounded because `2*diameter <= perimeter`. Blaschke selection then
gives attainment. The classical strict Brunn--Minkowski reduction supplies a
minimizing triangle or segment. Applying (6) to this minimizer and undoing the
normalization proves

\[
 \boxed{C_p(K)\geq \rho^{2-p}C_p(I_{P(K)})\quad(1<p<2).}       \tag{7}
\]

Since `rho > 2/3`, (7) improves the supplied longest-side comparison for every
allowed `p`. All inequalities and the direction of using the segment UPPER
bound have been checked: `c_p <= U_p` implies `b_p/c_p >= b_p/U_p`.

## Remaining gap

The bound is still strictly weaker than the desired factor one. Neither the
triangle reduction nor (3) identifies the true minimizer. Equality in the
geometric minimax (5) does not imply equality in the capacitary bounds. Novelty
of this elementary combined estimate has not been established.
