# Unequal-angle envelopes and complete boundary closure near the square lower bound

Problem: row 1757 / 5500059 / AMR0540059. Third newly documented substantive pass, 2026-10-13; lifetime earlier count unknown. No novelty claim.

## Result and limitations

For every epsilon>0 there is a square and a finite family of positive-area convex polygons, with pairwise disjoint interiors, such that:

- every point of the square boundary belongs to this family;
- every polygon has circumradius/inradius ratio at most G+epsilon;
- a nonempty open neighborhood of the square center remains uncovered.

Here G=1.288684461870457901325875... is the previously accepted balancing constant. Thus angle changes remove the four side gaps in the second-pass corner/constant-angle construction. This is NOT a partition of the square and gives NO new whole-square upper bound or unrestricted lower bound. Interior completion remains unresolved. All statements concern finite families; no infinite-partition equivalence is used.

An additional exact rational certificate gives 56 actual convex polygons covering the entire boundary, with maximum ratio strictly below 64439/50000 = 1.28878. It explicitly certifies an uncovered square center. The certificate is a boundary-patch witness, not a complete-square witness.

## 1. A sharp unequal-angle support envelope

Put a=1/t, b=u, A=(a+b)/2, m=(b-a)/2, and assume

    41/50 <= t <= u <= 1.

Consider a unit disk centered at the origin and baseline feet p-=(-a,-1), p+=(b,-1). Define

    R(t,u) = 1/2 + ((1+t^2)u+1/u)/(4t),
    y = m^2/(ab)-ab/4, O=(m,y), d=R-1.

Direct expansion gives

    R=1+y+ab/2,
    |O|=R-1, |O-p-|=|O-p+|=R.

The signs needed when taking square roots hold: R>1 by the arithmetic-geometric mean inequality, and 1+y>0 because

    1+y=((tu+1)^2-u^2)/(4tu)>0.

Hence B(O,R) contains the unit disk and both feet. Its three active contacts certify minimality. Explicit nonnegative weights on the right-foot, left-foot, and disk-distance constraints are

    w+ = (t^2u^2+u^2-1)(t^2u^2+2tu+u^2+1)
           /(8tu^3(tu+1)),
    w- = (1+u^2-t^2u^2)(t^2u^2+2tu+u^2+1)
           /(8u^2(tu+1)),
    wd = (tu-u+1)(tu+u+1)(t^2u^2-2tu+u^2+1)
           /(8tu^3).

They sum to one and satisfy

    w+ (O-p+)/R + w- (O-p-)/R + wd O/(R-1) = 0.

All three are strictly positive on the stated parameter domain. For w+, u^2(1+t^2)>= (41/50)^2(1+(41/50)^2)>1. For w-, 1+u^2-t^2u^2>=1. Both factors tu-u+1 and tu+u+1 are positive; the remaining disk factor is (tu-1)^2+u^2>0. Thus the weighted sum of the three convex distance functions is minimized at O, so their maximum is at least R at every proposed center. This proves the formula on its stated branch, rather than extending a two-foot formula across an unverified branch switch.

### No baseline tangency assumption in the lower bound

Suppose a convex cell has the baseline as a support and its left/right separators make angles alpha=2 atan(t), beta=2 atan(u), respectively, from the positive baseline direction into the cell's half-plane. Normalize its actual indisk to radius one and center zero, so the baseline is y=-h with h>=1. The support-distance inequalities force its baseline interval to contain

    p-(h)=(-csc(alpha)-h cot(alpha),-h),
    p+(h)=( csc(beta)-h cot(beta),-h).

At h=1 these are the preceding p-,p+. Every enclosing circle must contain the unit disk and these two points. Use the preceding weights in the jointly convex functions of center and h. Their center gradients cancel at (O,1); their weighted h derivative is exactly

    Dh=(t^2u^2+u^2+1)/(8tu)>0.

The supporting-hyperplane inequality therefore yields, for every h>=1,

    R_cell/r_cell >= R(t,u)+Dh(h-1).                 (1)

No neighboring-indisk tangency, common incenter/circumcenter, or prescribed actual incenter location beyond the normalization is assumed. Equality for a finite polygon is impossible: at h=1 the minimum enclosing circle of the relaxed data is unique and internally tangent to its unit indisk; no finite polygon can contain that disk while remaining in its internally tangent outer circle. At h>1, (1) is already strict relative to R(t,u).

In particular any such finite polygon of ratio at most gamma must satisfy the precise transition obstruction

    (1+t^2)u^2-(4gamma-2)tu+1 < 0.                  (2)

This is a local necessary condition, not a new unrestricted square bound. Its reflected version holds after replacing (t,u) by (1/u,1/t).

## 2. A cell with explicit complete separator segments

Translate the baseline feet to 0 and (w,0), where w=1/t+u. Put

    I=(1/t,1), O=(w/2,Y), Y=R-u/(2t),
    e(v)=((1-v^2)/(1+v^2), 2v/(1+v^2)),
    L(t,u)=1/t+1/(u(1+t^2)),
    U(t,u)=u+tu^2/(1+u^2),
    qL=L(t,u)e(t), qR=(w,0)+U(t,u)e(u).

The circle B(O,R) contains B(I,1), both feet, qL, and qR. Specifically qL and qR are the second intersections of the two upward separator rays with that circle. Their parameters exceed the two disk-contact parameters because

    L-1/t=1/(u(1+t^2))>0,
    U-u=tu^2/(1+u^2)>0.

Every generator is in both separator half-planes. Besides disk tangency and the baseline feet, the only nontrivial checks are the other upper point's signed support expressions. They are

    sin(beta)(w-qL_x)+cos(beta)qL_y
      =2t(tu+1)(t^2u^2+tu+u^2+1)
         /(u(1+t^2)^2(1+u^2)) >0,

    sin(alpha)qR_x-cos(alpha)qR_y
      =2(tu+1)(t^2u^2+tu+u^2+1)
         /((1+t^2)(1+u^2)^2) >0.

Consequently

    K(t,u)=conv(B(I,1),0,(w,0),qL,qR)

is a compact convex cell of ratio at most R(t,u). Its left and right separator intersections are exactly [0,qL] and [(w,0),qR]. Its actual inradius need not be asserted equal to one: the exhibited disk gives the needed lower bound and (1) bounds the true ratio from below when applicable.

If K(t,u) at scale sigma is followed by K(u,v) at scale

    sigma'=sigma U(t,u)/L(u,v),                    (3)

and its left foot is translated to the preceding right foot, the two entire separator segments agree. The cells occupy opposite half-planes of that common separator. Equation (3) is a shared-edge matching relation; it does not impose mutual disk tangency.

## 3. A finite transition from the corner angle to vertical separators

Let t0 be the accepted root C(t0)=F(t0), with

    C(t)=(1+t)/sqrt(2), F(t)=R(t,t), G=C(t0),
    0.82<t0<0.83.

It suffices to treat 0<epsilon<1/100, because a smaller positive epsilon gives the assertion for larger targets. Choose any integer n such that

    Delta=(1-t0)/n <= epsilon/4,
    t_j=t0+j Delta, 0<=j<=n.

The constant-angle cell K(t0,t0) comes first, followed by the n cells K(t_{j-1},t_j), j=1,...,n. Finally insert the central cell K(1,1).

For t0<=t<=u<=1,

    partial R/partial u=((1+t^2)-1/u^2)/(4t) <1.

Also F(t)<=F(t0)=G on [t0,1], since F'(t)=(t-t^(-3))/2<=0. Therefore every transition has

    R(t_{j-1},t_j) <= G+Delta < G+epsilon/2,

while R(1,1)=5/4. This is a finite explicit parameter sequence for every epsilon>0; no limiting infinite chain is being counted as a finite family.

Attach the first constant-angle cell to the accepted corner cell as follows. Write b=1+t0, e=e(t0), V=b(e_y-e_x), rho=V/L(t0,t0). The corner is

    Kc=conv(B((1,1),1),(0,0),(b,0),(0,b),q,q'),
    q=(b,0)+V e, q'=(q_y,q_x).

The accepted corner proof gives ratio G and exact exit segments of parameter V. The first strip scale rho therefore matches it exactly. Its previously verified bounds give 0.7<rho<0.8. Apply (3) successively to the whole left chain and then to the central cell.

Every scale is at most rho. Indeed if t<=u<=v<=1,

    U(t,u) <= U(u,u),
    L(u,v) >= 1/u+1/(1+u^2),
    L(u,1)-U(u,u)
      =(1-u)(2u^3+2u^2+2u+1)/(u(1+u^2)) >=0.

The inequality is strict before all three parameters equal one. The last transition ends at u=1, and its ratio into K(1,1) is U(t,1)/(3/2)=(2+t)/3<=1.

Let x be the last left-chain right foot and let sigma_c be the central scale. Choose

    S=2(x+sigma_c).

The central cell occupies the baseline [x,x+2sigma_c] and is invariant under reflection in x=S/2. Reflect the left chain and the corner across this perpendicular bisector. The entire interval [0,S] is now covered by exactly the consecutive prescribed baseline intervals. Repeat this side arrangement by square rotations at all four corners; corner cells are counted once.

## 4. Global disjointness of the boundary family

The matching separators handle incident side cells. The following uniform estimates prove all other pairs are disjoint and justify subsequent polygonal approximation.

For a left-chain cell, t0<=t<=u<=1 implies cos(alpha),cos(beta)<1/5 and L<2. All its generators have nonnegative x relative to its left foot. Its left upper point has x<2/5<w. The disk has rightmost x=w+(1-u), and the right upper point has x=w+U cos(beta). Since U>=u>=41/50,

    (1-u)/U <=9/41<1/4, cos(beta)<1/4.

Thus every point of this cell has x strictly less than its right foot plus sigma U/4. For the following cell, L(u,v)<2/u and w(u,v)>=1/u, so w(u,v)/L(u,v)>1/2. By (3), its baseline width exceeds sigma U/2. Therefore the earlier cell ends strictly before the next-but-one baseline foot. Every nonadjacent left-chain pair is separated by a vertical line. The same argument separates a nonlast left cell from the central cell.

The last left cell has u=1, so all its generators have x at most its right foot x: the disk ends at that foot and its right separator is vertical. The central cell lies between x and x+2sigma_c. The reflected right chain starts beyond that interval. Adjacent last/central cells are still separated by their exact vertical support. These statements give disjointness of the whole side patch, including the reflected half.

All left-chain cells have height at most

    sigma(R+Y)=sigma(2R-u/(2t)) <=rho(2R-1/2)<0.8*2.1=1.68<b.

The central cell has height 2sigma_c<=1.6<b, and reflection preserves height. Thus chains on adjacent square sides are disjoint: their heights perpendicular to their own sides are below b, while their baseline coordinates measured from a corner start at b.

The corner cell lies in a box of side b/2+G<2.21. The first constant-angle cell is separated from it by its exact exit support. Every later bottom-side cell starts at x>=b+rho(t0+1/t0)>1.82+0.7*2>3.22, so is horizontally separated from the corner box. The analogous claim holds on the other adjacent side. The square side satisfies S>2(b+rho(t0+1/t0))>6.44, which separates corner boxes from each other and from nonincident side patches. Opposite side patches have respective heights below 1.68 and above S-1.68 and are disjoint. These bounds cover all pair classes.

Moreover all cells miss an open neighborhood of (S/2,S/2). Side cells have perpendicular height below 1.68<S/2, and corner boxes end below 2.21<S/2 in both coordinates. Hence the construction demonstrably leaves interior area uncovered.

## 5. Finite polygonal approximation preserving coverage and incidence

For the fixed finite construction, approximate each compact convex hull from outside by finitely many supporting half-planes. Retain its baseline and two separator supports. At each upper separator endpoint retain the tangent to its known outer circle; together with the separator this fixes that exact endpoint. These two lines are distinct because the separator ray has two different circle intersections. At each baseline endpoint the separator and baseline fix the point. The corner's two axis supports and two exit supports are retained in the same way.

Compactness of the set of normal directions gives arbitrarily close outer polygonal approximations; equivalently, a sufficiently fine finite net of support directions bounds the support-function error. The original disk remains contained, so the actual inradius is at least its displayed radius. An approximation within distance eta times that radius lies within the enclosing circle with radius increased by eta times that radius. Choose eta small enough that every resulting polygon has ratio at most G+epsilon.

Incident cells remain in opposite separator half-planes and keep exactly their prescribed common segments. All nonincident pairs have the strict separation established above; finitely many such margins can be preserved simultaneously. Baseline intervals are unchanged, so every square-boundary point remains covered. The height and square-center gaps can likewise be kept positive. The retained square-side supports keep all polygons inside the square. This proves the finite boundary-cover theorem with its explicitly uncovered interior.

## 6. Exact 56-polygon example

The machine-readable certificate uses these rational half-angle parameters:

    0.82248, 0.8235, 0.831, 0.87, 0.96, 1.

There is one initial constant-angle cell, followed by the five successive transitions, on each half-side, and one middle cell per side. With four corner cells the total is 4+4(2*6+1)=56. The corner construction uses the rational t=0.82248 directly; it does not falsely substitute C(t)=F(t) away from t0. Its indicated enclosing circle has squared radius (1+t)^2/2, while the transition circles have their separate exact radii R(t,u).

The maximal relaxed transition radius is approximately 1.288744068924455. The finite polygon vertices are supplied as exact rational numbers in eight canonical types, with exact rational similarities and square symmetries for all 56 placements. Each type contains its explicit unit indisk, and every vertex is strictly within distance 64439/50000 of its indicated circumcenter. The corresponding transformed cells inherit those bounds. A separate verifier checks strict convexity, exact disk containment edge by edge, all enclosing-circle inequalities, all 1540 pair separations, exact consecutive shared segments, all four complete boundary intervals, and an uncovered central point. It checks finite polygons directly rather than accepting the curved hull formulas in place of a witness.

The stated inequality is strict for this certificate. Its cells cover the boundary of a square, not its interior; the certificate and checker both encode that distinction.

## Dependencies and source context

The complete [prior theory](../5500059_circular_square_first_20261013/THEORY_REPORT.md), [quantitative obstruction](../5500059_circular_square_second_20261013/QUANTITATIVE_COMPLETION_OBSTRUCTION.md), [corner-chain proof](../5500059_circular_square_second_20261013/CORNER_CHAIN_AND_BRIDGE_OBSTRUCTION.md), and their [theory](../5500059_circular_square_first_20261013/INDEPENDENT_THEORY_REVIEW.md), [quantitative](../5500059_circular_square_second_20261013/INDEPENDENT_QUANTITATIVE_REVIEW.md) and [corner-chain](../5500059_circular_square_second_20261013/INDEPENDENT_CORNER_CHAIN_REVIEW.md) independent reviews are unchanged sibling dependencies. They supply the accepted t0 and G facts and corner construction used here. The new envelope algebra, chain gluing, boundary closure, and exact witness are proved or checked in this pass.

Public source context was rechecked on 2026-10-13: Mirela Damian and Joseph O'Rourke, *Partitioning Regular Polygons into Circular Pieces I: Convex Partitions*, arXiv cs/0304023v2, revised 2026-02-08, https://arxiv.org/abs/cs/0304023v2; TOPP Problem 59, https://topp.openproblem.net/p59. The source's Section 5.4 is expressly conjectural. No copied source text, source PDF, dataset, private source, or literature-priority claim is part of this deliverable.
