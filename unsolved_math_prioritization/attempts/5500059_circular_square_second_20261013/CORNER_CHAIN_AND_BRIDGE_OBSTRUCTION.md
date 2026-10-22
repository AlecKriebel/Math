# Corner attachment, graded boundary chains, and a failed direct bridge

Problem: row 1757 / 5500059 / AMR0540059. Second newly documented pass, 2026-10-13. No novelty claim.

## Outcome

The first-pass non-tangent two-cell construction can be attached exactly to a square-corner cell and repeated for any finite number of cells. Four copies give mutually nonoverlapping corner-and-side patches in one square. Their circularity can be made at most G+epsilon with finite convex polygons, for any epsilon>0. These patches leave four mid-side gaps and a large interior region. They are not a partition of the square.

A specific tempting completion fails: reflecting the constant-angle chains and filling a mid-side gap with a single cell forces that cell's ratio to be at least

    1+1/(4t0^2) = 1.36957...,

which exceeds G. This obstruction concerns the two prescribed boundary-separator directions. It does not exclude inserting a sequence of angle-changing boundary cells, nor prove any new unrestricted lower bound.

## 1. Parameters and exact corner attachment

Let t=t0 be the first-pass balancing root, 0.82<t<0.83, and put

    b=1+t, G=b/sqrt(2)=(t^4+3t^2+1)/(4t^2),
    A=(1+t^2)/(2t), k=G-1/2,
    c=(1-t^2)/(1+t^2), s=2t/(1+t^2), e=(c,s),
    I=(1/t,1), O=(A,k),
    r=t^2(1+2t^2)/(2+t^2),
    U=t(1+2t^2)/(1+t^2),
    L=(2+t^2)/(t(1+t^2)).

Here U=rL. The canonical strip cell has baseline endpoints 0,(2A,0), indisk B(I,1), enclosing disk B(O,G), and additional points

    q_left=L e, q_right=(2A,0)+U e.

The two additional points lie on that enclosing circle. Its indisk lies between the parallel supports through its baseline endpoints in direction e. Their width is exactly 2. Thus

    K=conv(B(I,1), 0, (2A,0), q_left, q_right)

has exact inradius 1 and circumradius G. The latter follows already from the disk and the baseline endpoints, using the valid three-contact branch. Its intersections with the left and right supports are exactly the segments [0,q_left] and [(2A,0),q_right]. Indeed the disk contacts occur lower on those supports, at parameters 1/t and t respectively, because L-1/t=1/(t(1+t^2))>0 and U-t=t^3/(1+t^2)>0. Every other generator lies strictly on the correct side.

For the corner cell take indisk B(J,1), J=(1,1), enclosing center O_c=(b/2,b/2), radius G, and boundary vertices

    o=(0,0), p=(b,0), p'=(0,b).

The disk lies in the enclosing circle because

    |J-O_c|+1=(1-t)/sqrt(2)+1 <= (1+t)/sqrt(2)=G,

using t>1/sqrt(2). The two square-axis supports and the supports through p and p' in directions (c,s) and (s,c), respectively, all contain the disk on their inward side.

The second intersection of the ray p+lambda e with the corner enclosing circle has parameter

    V=b(s-c).

Let q=p+Ve and q' be its reflection in x=y. Both belong to the enclosing circle. They are on the correct side of the other exit support as well: for q, the signed supporting expression for that other line is

    b(c+s)+V(c^2-s^2)=2bsc(c+s)>0.

Define

    K_c=conv(B(J,1), o,p,p',q,q').

Its inradius is exactly 1. To prove maximality without assuming an incenter, any contained disk of radius z and center (x,y) obeys x,y>=z and

    -s x+c y+sb>=z,   c x-s y+sb>=z.

As c-s<0, adding and using x+y>=2z gives z<=sb/(1+s-c)=1. Its circumradius is exactly G because p and p' are separated by 2G. The disk contact on the exit ray has parameter t, while

    V-t=(3t^2-1)/(1+t^2)>0.

The first strip cell can therefore meet the corner along exactly [p,q] by scaling it by

    rho=V/L = b*t*(t^2+2t-1)/(2+t^2)

and translating its left endpoint to p. Numerically rho=0.74005167223658... . The two cells lie on opposite sides of their shared support. No mutual indisk tangency is required.

## 2. Repeating the side chain

For j=0,...,M-1 set

    sigma_j=rho*r^j,
    x_j=b+2A*rho*(1-r^j)/(1-r),
    K_j=(x_j,0)+sigma_j K.

Consecutive cells share the exact segment from (x_{j+1},0) to

    (x_{j+1},0)+sigma_j U e
      =(x_{j+1},0)+sigma_{j+1} L e.

They lie in consecutive disjoint parallel strips, so their interiors are disjoint. The corner lies on the opposite side of the first strip's left support and hence is disjoint from every strip cell except the intended common boundary with the first. All these compact convex sets have exact ratio G.

These are curved convex sets because they contain circular arcs on their boundaries. For any fixed finite M and epsilon>0, replace them by sufficiently close finite outer polygonal approximations, keeping the square-axis supports, strip supports, corner exit supports, and sufficient supporting lines through each prescribed shared-edge endpoint. Each indisk remains contained. The retained strip width, or the four corner supports proved above, keeps the inradius exactly its stated value. An arbitrarily close approximation lies in the enclosing circle enlarged by epsilon times that inradius. The fixed shared endpoints and separators preserve the exact shared segments and disjoint interiors. Nonincident members of a finite patch have positive separation, so choosing the approximations sufficiently close introduces no other intersections. This gives actual finite convex polygonal patches of ratio at most G+epsilon.

## 3. Four corner patches in one square

Choose the square side length

    S=2(b+2A*rho/(1-r)) = 11.0884966808933... .

Place K_c at all four corners by the corresponding square symmetries, and place M strip cells on each of the eight oriented half-sides. These patches have pairwise disjoint interiors.

Here are explicit bounds verifying the separation instead of relying on a drawing. The balancing-root bracket gives G<1.29 (already t0<0.823 suffices). Direct rational bounds on 0.82<t<0.83 give the other estimates below:

    A<1.02, 0<c<0.2, G<1.29,
    0.58<r<0.62, 0.7<rho<0.8, L<2, U<1.2.

Every bottom strip cell has 0<=y<=sigma_j(2G-1/2), hence lies below

    H=rho(2G-1/2)<0.8*2.08=1.664<b.

It has x>=x_j. Each generator's x-coordinate relative to its left baseline endpoint is less than 2.3 sigma_j: the disk gives 1+1/t<2.22, the left upper point gives Lc<0.4, and the right gives 2A+Uc<2.28. But the distance from that endpoint to the limiting midpoint is

    S/2-x_j=2A*sigma_j/(1-r)> (2/0.42)sigma_j>4.7sigma_j.

Thus each cell from one corner stays strictly in its own half-side, separated from the reflected chain by the perpendicular midpoint line. Chains on adjacent sides lie in strips of width H<b, while their sidewise coordinates start at b, so they cannot meet. Each corner cell lies in its corner's box of side b/2+G<2.21, and S>10; opposite corner regions and the far-side strips are disjoint. The corner exit supports already separate a corner from its two adjacent side chains. These observations check every class of pair.

For finite M, the uncovered middle interval on each square side has length

    g_M=4A*rho*r^M/(1-r)>0.

There are 4+8M displayed cells. The polygonal approximation argument preserves the baseline intervals, so the same middle gaps remain. Much of the square interior also remains uncovered. No infinite partition or completion is asserted by this limiting notation.

## 4. Exact obstruction to a single constant-angle bridge

Suppose a candidate bridge cell meets a straight square side in one interval and is bounded at its left and right endpoints by separators at angles theta=2 atan(t) and pi-theta, measured from the positive baseline direction into the square. This is precisely the missing middle-cell geometry if the two reflected constant-angle chains are connected directly, without inserting angle-changing boundary cells.

Normalize any actual indisk to radius 1 centered at 0 and put the baseline at y=-h, h>=1. The same support-distance inequalities as in the first-pass crossing argument force the baseline interval to contain

    (-u,-h), (u,-h),  where u=csc(theta)+h cot(theta)=A+h C,
    C=cot(theta)=(1-t^2)/(2t).

Since the indisk contains T=(0,1), every enclosing circle contains the isosceles triangle with these three vertices. For h>=1 and the stated t range, u<h+1. (It holds at h=1 because A+C=1/t<2, and C<1.) The triangle is acute, and its circumradius is

    R_triangle(h)=((h+1)^2+u^2)/(2(h+1)).

This function is strictly increasing in h. Indeed, setting v=u/(h+1)<1 gives

    R_triangle'(h)=(1-v^2)/2+C v>0.

Therefore every such bridge cell has ratio at least

    R_triangle(1)=1+1/(4t^2)>1.36>G.

This lower bound is sharp for the relaxed local data: the disk and those two feet at h=1 are enclosed by the circle centered at (0,-1/(4t^2)) of radius 1+1/(4t^2). This circle contains the unit disk with equality and the feet with equality. It does not certify a polygon at exact equality or a full-square partition.

Thus the geometric radius decay that makes a favorable two-cell opening does not by itself allow opposite side chains to close. Boundary-separator directions must change, or more cells must be inserted into the remaining gap. Controlling such transitions and the interior fill is still the unresolved completion step.
