# An explicit finite-complexity obstruction for circular square partitions

Problem: row 1757 / 5500059 / AMR0540059. Date: 2026-10-13.
This is the second newly documented mathematical pass in this continuation; lifetime earlier pass counts are unknown. No novelty claim is made.

## Result and scope

Let G=1.288684461870457901325875... be the balancing constant from the independently reviewed first-pass report. If a square is partitioned into at most N positive-area compact convex cells, and gamma is the maximum circumradius/inradius ratio, then

    gamma > G + 1/(192 * 25^(N+2)).                         (1)

This is a global necessary complexity constraint. It makes the earlier, nonquantitative fixed-N strict gap explicit. It is extremely weak numerically. It does not improve the unrestricted finite-partition infimum lower bound G, construct a complete partition attaining or approaching G, or settle any infinite-partition interpretation.

All circles in this argument are free to have different centers; neighboring indisks need not touch. The number of sides is counted after removing redundant collinear vertices.

## 1. A finite-sided eccentric-annulus lemma

**Lemma.** Suppose a convex polygon P has m sides, contains a unit disk, and is contained in a disk of radius R <= 13/10. Let d be the distance between the two disk centers and put delta=R-d-1. Then

    delta > 1/(36 * 25^(m-1)).                            (2)

In particular, the circles cannot be internally tangent.

**Proof.** Translate and rotate so the unit disk is centered at 0 and the enclosing disk is centered at (-d,0). Necessarily 0 <= d <= R-1 <= 3/10 and delta >= 0.

Move every supporting line of P inward parallel to itself until it is tangent to the unit disk. The intersection Q of the resulting halfplanes is a bounded convex polygon containing the unit disk and contained in P. Its number k of sides is at most m. Delete redundant inequalities. Write its distinct outward unit normals in cyclic angular order. Every consecutive angular gap is less than pi: a gap at least pi would leave the intersection unbounded.

For consecutive normals with angles theta-h and theta+h, where 0<h<pi/2, the intervening vertex is

    v = sec(h) (cos(theta), sin(theta)).

Choosing consistent real angle representatives, containment of this vertex in the outer disk implies, with s=sec(h),

    d^2+s^2+2ds cos(theta) <= R^2.

Subtract (d+1)^2. Using s+1+2d cos(theta) >= 2(1-d), s-1 >= h^2/2, and 2(cos(theta)-1) >= -theta^2 gives

    (1-d)h^2 - d theta^2 <= 2R delta - delta^2 <= 2R delta.

Consequently

    h^2 <= (3/7)theta^2+(26/7)delta
         <= (4/9)theta^2+4delta.                         (3)

Select the consecutive normals bracketing angle 0; if 0 itself is a normal, select either adjacent gap containing it as an endpoint. In this gap |theta|<=h, so (3) gives

    h <= (6/sqrt(5))sqrt(delta) < 3sqrt(delta)

when delta>0. If delta=0, it forces h=0, impossible, proving delta>0. Each bracketing normal therefore has absolute angle less than 6sqrt(delta).

Because Q is bounded, its normals cannot all lie in the open right semicircle. Thus at least one normal, represented in [-pi,pi], has absolute angle at least pi/2. Starting with the appropriate one of the bracketing normals, follow the positive or negative angular direction to the first such normal, reflecting angles if necessary. Let a,b be two successive nonnegative angles on this walk. Equation (3), with theta=(a+b)/2 and h=(b-a)/2, implies

    h <= (2/3)theta+2sqrt(delta),
    b <= 5a+12sqrt(delta),
    b+3sqrt(delta) <= 5(a+3sqrt(delta)).                 (4)

There are at most k-1 steps from the initial bracketing normal. Iterating (4), and using its initial angle less than 6sqrt(delta), yields

    pi/2 <= b < 9*5^(k-1)*sqrt(delta).

Since pi/2>3/2, delta>1/(36*25^(k-1)) >= 1/(36*25^(m-1)). This proves (2). The argument permits a normal exactly opposite angle 0, and treats a normal exactly at angle 0 by the stated endpoint convention. ∎

## 2. The crossing-cell envelope, with explicit sensitivity

The first-pass lower-bound proof and its independent acceptance establish the following boundary facts for any finite partition of ratio at most 13/10:

- The four square corners belong to four distinct corner cells.
- Exactly two cells meet at a genuine interior subdivision point of a square side, with supplementary angles. All genuine cell angles exceed 75 degrees.
- Both exit angles into neighboring cells at each corner are less than 90 degrees.
- If alpha,beta are those two exit angles at one corner, its circularity is at least

      (1/2)*sqrt((1+tan(alpha/2))^2+(1+tan(beta/2))^2).

For completeness, these do not assume face-to-face combinatorics. The angle estimate follows by enclosing a unit indisk and a corner vertex; it gives (1+csc(omega/2))/2. Its value at 75 degrees exceeds 13/10. Finitely many incident sectors then exclude three cells on a square-side subdivision and two at a square corner. The corner chord estimate follows from support-line distance inequalities and a positive-weight Cauchy-Schwarz argument, as fully proved in the accepted first report. Its version with one exit at least 90 degrees exceeds 13/10. The same support argument handles a cell spanning adjacent square corners, and a cell spanning opposite corners has ratio at least sqrt(2).

By the first-pass strict lower bound, gamma>G. For now suppose gamma<=13/10, and set

    t=sqrt(2)*gamma-1, theta=2 atan(t),
    a=csc(theta), c=cot(theta),
    F(t)=(t^4+3t^2+1)/(4t^2).

Here t0<t<1, where t0 is the unique root in (0.82,0.83) of C(t)=F(t), C(t)=(1+t)/sqrt(2), and G=C(t0). The corner chord bound ensures that some corner exit is at most theta. Walking along its side to the opposite corner ends with an angle above 90 degrees, hence above theta. There are consecutive boundary separators with angles alpha<=theta<=beta, bounding one crossing cell P.

Normalize P's actual indisk to be the unit disk centered at 0, and write its baseline y=-h, h>=1. Support distances show that its bottom edge contains both

    p_-(h)=(-a-hc,-h),    p_+(h)=(a-hc,-h).

Indeed its actual left endpoint (-u,-h) obeys u>=csc(alpha)+h cot(alpha), a decreasing function of alpha; its right endpoint (v,-h) obeys v>=csc(beta)-h cot(beta), an increasing function of beta. The derivatives have signs because h>=1. No support contact or indisk tangency between cells is asserted.

Define

    f(h,z)=min_o max(|o|+z, |o-p_-(h)|, |o-p_+(h)|).

For fixed z, this is even and convex in h. Convexity follows by projecting the jointly convex epigraph over o. Evenness follows by central inversion, which swaps the two feet at h and -h. Therefore f(h,z)>=f(1,z) when h>=1.

We need a quantitative bound as the centered disk radius z grows. At z=1, h=1, the correct three-contact branch gives f(1,1)=F(t). It is valid because t>=t0>0.82>sqrt((sqrt(5)-1)/2). The optimal circle center is

    o_*=(-c,F(t)-3/2),

with distance |o_*|=F(t)-1 from the unit-disk center. Positive convex weights on the two endpoint distance constraints and the disk distance constraint have zero total gradient. The weight of the disk constraint is

    w(t)=2(F(t)-1/2)(F(t)-1)
        =(t^4+1+t^(-4))/8 >= 3/8.                      (5)

The weights of p_+(1) and p_-(1), respectively, are

    (t^4+t^2-1)(t^4+3t^2+1)/(8t^4(1+t^2)),
    (1+t^2-t^4)(t^4+3t^2+1)/(8t^2(1+t^2)).

They and w sum to one and their weighted distance gradients vanish. Both endpoint weights are positive on the stated interval; the displayed factors verify this directly. These are also the barycentric weights of the two feet and the inner/outer-circle contact point. Convexity of the three distance functions consequently gives, for every eta>=0,

    f(1,1+eta) >= F(t)+w(t)eta.                         (6)

To spell out the dual argument, the weighted sum of the three functions at any o is at least its value F(t) at o_*, because its zero gradient makes o_* a global minimizer. Replacing |o|+1 by |o|+1+eta adds exactly w(t)eta to that weighted sum. The maximum dominates the weighted sum, and minimizing the maximum proves (6).

Let the actual enclosing circle of P have radius R<=gamma, center at distance d from its incenter, and slack delta=R-d-1. The same outer circle contains the concentric disk of radius 1+delta and the two canonical feet. Thus

    gamma >= R >= f(h,1+delta) >= f(1,1+delta)
          >= F(t)+(3/8)delta.                          (7)

This controls the internal-tangency slack without a circumcenter-stability assumption.

Finally define D(gamma)=gamma-F(sqrt(2)gamma-1). For G<=gamma<=13/10,

    D'(gamma)=1+(sqrt(2)/2)(t^(-3)-t) < 2.

For example t>4/5 and t<1 imply t^(-3)-t<369/320, and sqrt(2)/2<3/4. Since D(G)=0, we have

    D(gamma)<2(gamma-G) for gamma>G.                   (8)

## 3. Global side count and conclusion

A cell in a partition with at most N positive-area convex cells has at most N+3 sides. To see this without assuming polygonality in advance, separate it weakly from each other cell by a line and intersect the containing halfplanes with the four square halfplanes. This intersection contains the cell. If the inclusion were strict, there would be an open disk in the intersection outside the chosen cell; the finite union of the other cells' boundaries cannot cover that disk, but their interiors are excluded by the separating halfplanes. This contradicts coverage. The intersection therefore equals the chosen cell, and uses at most N-1+4 inequalities.

Apply the annulus lemma to the crossing cell with m<=N+3. Equations (2), (7), and (8) give

    2(gamma-G) > D(gamma) >= (3/8)delta
               > 1/(96*25^(m-1))
               >= 1/(96*25^(N+2)),

which proves (1) for gamma<=13/10. If gamma>13/10, then G<1.29 gives gamma-G>0.01, whereas the right-side correction in (1) is below 1/192<0.01. Thus (1) holds in that case as well.

A useful contrapositive is that any partition with gamma<=G+epsilon must obey

    192*epsilon*25^(N+2)>1,
    N > log_25(1/(192*epsilon))-2.

This necessary condition is quantitatively very weak. It does not explain the presently certified whole-square upper bound gap, does not rule out gamma approaching G as N grows, and does not fill a square. The remaining geometric problem is to complete a compatible boundary arrangement by finite convex interior cells under the same circularity ceiling.

## Dependencies and source context

- First-pass complete proof: [the complete first-pass theory proof](../5500059_circular_square_first_20261013/THEORY_REPORT.md).
- Independent first-pass acceptance: [the independent first-pass theory acceptance](../5500059_circular_square_first_20261013/INDEPENDENT_THEORY_REVIEW.md).
- Source/admissibility audit: [the source and admissibility audit](../5500059_circular_square_first_20261013/SOURCE_BOUND_AUDIT.md).
- Mirela Damian and Joseph O'Rourke, *Partitioning Regular Polygons into Circular Pieces I: Convex Partitions*, arXiv cs/0304023v2, https://arxiv.org/abs/cs/0304023v2.
- TOPP Problem 59: https://topp.openproblem.net/p59.

No copied source document or dataset content is included here. The source's open tradeoff question about number of pieces versus circularity motivates this bounded result; no exhaustive priority search or claim of a new literature result is made.
