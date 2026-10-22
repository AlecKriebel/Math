# Square circularity: rigorous boundary reduction and a non-tangent local junction

Date: 2026-10-13. Problem: row 1757 / 5500059 / AMR0540059.
Status: substantive partial result; the full optimal value and attainment remain open in this work. This is the first newly documented theory pass in the present continuation, not a claim of zero lifetime prior attempts. No novelty claim is made.

## Scope and sources

For a finite partition of the unit square into positive-area compact convex polygonal cells, let the objective be the maximum of each cell's smallest enclosing radius divided by its largest inscribed radius. Steiner points are unrestricted, the two circles need not be concentric, and different indisks need not be tangent. Write the infimum over these finite partitions as Gamma_fin. The literal problem and the source also discuss infinite limiting partitions; no equivalence between that larger admissible class and the finite-partition infimum is assumed here.

The principal source is Mirela Damian and Joseph O'Rourke, *Partitioning Regular Polygons into Circular Pieces I: Convex Partitions*, arXiv:cs/0304023v2, https://arxiv.org/abs/cs/0304023v2 (version posted 2026-02-08); problem statement: https://topp.openproblem.net/p59. Section 5.3 reports the general lower bound about 1.28868; Section 5.2 reports a 92-piece upper construction about 1.29950. Section 5.4's 1.28939 is explicitly conjectural and restricted to tangent neighboring boundary indisks. The present report does not independently certify the published upper construction.

The source's printed local Lemmas 13-14 use `min` where the balancing argument requires `max`; the displayed reciprocal for the unit-indisk ratio in Lemma 14 is also inconsistent with its definition. There are additional angle-selection and tangency-reduction presentation gaps. These observations must be separated from validity of the intended lower bound. Below is a complete replacement proof of that lower bound in the finite case. The source's Lemma 16 formula has an active-constraint branch restriction, stated precisely below.

## 1. Exact constant and the disk-plus-feet problem

Let t0 be the unique t in (0.82,0.83) such that

    C(t) = (1+t)/sqrt(2) = F(t) = (t^4+3t^2+1)/(4t^2).

Set theta0 = 2 atan(t0), G = C(t0) = F(t0). The first function increases and the second decreases on (0,1), proving uniqueness. Equivalently t0 is the root in this interval of

    t^8 - 2t^6 - 16t^5 + 3t^4 + 6t^2 + 1 = 0.

Numerically,

    t0 = 0.82247504359667524339664689...
    theta0 = 78.87288765518407078676545... degrees
    G = 1.288684461870457901325875...

For a unit disk tangent to a baseline and to two parallel lines making angle theta with that baseline, the minimum radius enclosing the disk and the two baseline feet is NOT always 1/4+csc(theta)^2. For 0 < theta <= pi/2 it equals

    (1+csc(theta/2))/2,  if tan(theta/2)^2 <= (sqrt(5)-1)/2;
    1/4+csc(theta)^2,   if tan(theta/2)^2 >= (sqrt(5)-1)/2.

The transition angle is 2 atan(sqrt((sqrt(5)-1)/2)), approximately 76.345 degrees. At theta=60 degrees the true radius is 3/2, whereas the second expression is 19/12. Thus only the second branch is used near theta0.

Proof of branches. Put a=csc(theta), z=cot(theta), disk center I=(z,1), and the feet at (-a,0),(a,0). An enclosing circle determined by the disk and the left foot alone has radius (1+csc(theta/2))/2. It contains the other foot exactly in the first stated range, by comparing its center's horizontal coordinate with zero. Otherwise both feet are active. The candidate center is O=(0,a^2-1/4) and radius R=a^2+1/4; it contains the disk because |I-O|=R-1. In the second range O is in the convex hull of the two feet and the point where the disk touches this circle; therefore the circle is minimal. Equivalently, the three active distance gradients have a nonnegative convex combination equal to zero. For an explicit optimality certificate in terms of t=tan(theta/2), the barycentric weights of the right foot, left foot, and disk-contact point, respectively, are

    lambda_right = (t^4+t^2-1)(t^4+3t^2+1)/(8t^4(1+t^2)),
    lambda_left  = (1+t^2-t^4)(t^4+3t^2+1)/(8t^2(1+t^2)),
    lambda_disk  = (t^2-t+1)(t^2+t+1)(t^4-t^2+1)/(8t^4).

They sum to 1 and reconstruct O. All are nonnegative in the stated two-foot range; all are strictly positive at t0. The branch transition follows from u^4-u^2-1=0 for u=cot(theta/2). This also checks that theta0 is strictly inside the two-foot branch.

## 2. A complete finite-partition lower bound

**Theorem. Every finite convex polygonal partition of a square has maximum ratio strictly larger than G. Consequently Gamma_fin >= G.**

This does not determine whether Gamma_fin is G or larger. In particular it does not resolve attainment at Gamma_fin if that infimum is larger than G.

It is enough to consider partitions with maximum ratio at most 1.3. The elementary one-angle bound says that a cell having an angle omega must have ratio at least (1+csc(omega/2))/2. Therefore every cell angle is greater than 75 degrees, since the latter expression at 75 degrees exceeds 1.3. Collinear redundant vertices are ignored throughout. This implies:

- a square corner is occupied by exactly one cell;
- at each subdivision point in the relative interior of a square side, exactly two cells meet with supplementary angles (three angles greater than 75 degrees cannot fit into 180 degrees);
- all separating angles along a square side lie between 75 and 105 degrees.

### 2.1 Corner chord bound without assumed tangencies

At a square corner take coordinates with the square in x,y>=0 and normalize a corner-cell indisk to radius 1. Its center (x,y) has x,y>=1. Let the two boundary endpoints of that cell be (B,0),(0,C), and let alpha,beta be the angles in the neighboring cells. Support-line distance inequalities give

    B >= x+csc(alpha)-y cot(alpha),
    C >= y+csc(beta)-x cot(beta).

No contact of the indisk with these four supporting lines has been assumed.

For alpha,beta in [75,105] degrees define b0=1+tan(alpha/2), c0=1+tan(beta/2). Both b0-c0 cot(beta) and c0-b0 cot(alpha) are positive. For example b0,c0 lie between 1.767 and 2.304, while the positive cotangents are at most 0.268. Multiply the preceding inequalities by b0,c0 respectively. Their sum is minimized over x,y>=1 at x=y=1, so

    b0 B+c0 C >= b0^2+c0^2.

Cauchy-Schwarz gives sqrt(B^2+C^2)>=sqrt(b0^2+c0^2). Any enclosing circle contains the chord between the endpoints; consequently

    R/r >= (1/2) sqrt((1+tan(alpha/2))^2+(1+tan(beta/2))^2.       (Corner)

In particular if either alpha or beta is at least 90 degrees, the right side exceeds sqrt((1+tan(37.5 degrees))^2+4)/2 > 1.3. Thus both exits from every competitive corner cell have neighbor angles less than 90 degrees.

A cell cannot contain two square corners in a competitive partition. For opposite corners, or three corners, the diagonal diameter bound and r<=side/2 give ratio at least sqrt(2). If exactly two adjacent corners are present, use either corner and treat the next square corner as an artificial exit of 90 degrees. There is an actual exit on the other incident side (otherwise there are at least three corners). The same supporting-line and positive-weight argument applies and again gives a ratio above 1.3. Hence the four corner cells are distinct.

### 2.2 A crossing cell contains canonical strip feet

Suppose, for contradiction, that a finite partition has ratio at most G. For a corner cell let theta be its smaller exit angle. (Corner) implies

    G >= (1+tan(theta/2))/sqrt(2),

so theta<=theta0. Start walking along the associated square side from this corner toward the other corner. Write the successive separating angles as alpha_1,...,alpha_m, all measured from the positive baseline direction into the square. The first is at most theta0. The last is greater than 90 degrees, because the other corner's exit is less than 90 degrees. Finiteness gives adjacent angles alpha<=theta0<=delta, bounding one side cell.

Normalize that cell's indisk to the unit disk centered at the origin and write the baseline as y=-h, h>=1. Its left and right endpoints are b=(-u,-h), c=(v,-h). The support distances give

    u >= csc(alpha)+h cot(alpha),
    v >= csc(delta)-h cot(delta).

For h>=1, the first function is decreasing in its angle, since its derivative is -(cos(angle)+h)/sin(angle)^2. The second is increasing, since its derivative is (h-cos(angle))/sin(angle)^2. Therefore [b,c] contains the two points

    b0=(-csc(theta0)-h cot(theta0),-h),
    c0=( csc(theta0)-h cot(theta0),-h).

The cell also contains the unit disk.

Let f(h) be the minimum radius enclosing the unit disk and b0,c0. This is a convex function of h: its epigraph is the projection, over a freely varying circumcenter, of the jointly convex inequalities bounding the three relevant distances (the unit disk contributes distance-to-origin plus 1). Also f(-h)=f(h), by central inversion swapping the two points while preserving the disk. An even convex function is nondecreasing on [0,infinity), so f(h)>=f(1)=G.

### 2.3 Strictness for polygonal cells

In fact equality in the last bound requires h=1. At h=0 the radius-csc(theta0) circle centered at the origin encloses the unit disk and both canonical feet, so f(0)<=csc(theta0)<G=f(1). For h>1 convexity gives

    f(h) >= f(1)+(h-1)(f(1)-f(0)) > f(1).

At h=1, the canonical smallest enclosing circle is unique and is internally tangent to the indisk. A polygon containing the indisk and contained in this circle cannot exist: at their common tangency point, any supporting polygon edge through that point follows the common tangent and immediately lies outside the outer circle. Equivalently, a polygon locally containing the disk must either cut the disk or leave the outer circle. Therefore the side cell has ratio strictly greater than G, a contradiction. This proves the theorem.


## 3. Non-tangent local junction: a constructive result

This is a local result, not a partition of the square. It shows that the particular next-level angle obstruction described under mutually tangent indisks disappears for an explicit allowed non-tangent pair.

Let t>0 and set

    sin(theta)=2t/(1+t^2), cos(theta)=(1-t^2)/(1+t^2),
    a=(1+t^2)/(2t), R=a^2+1/4, k=R-1/2,
    I=(1/t,1), O=(a,k), p=(2a,0), e=(cos(theta),sin(theta)),
    r=t^2(1+2t^2)/(2+t^2),
    s=t(1+2t^2)/(1+t^2), q=p+s e.

Use the two indisks D1=B(I,1), D2=B(p+rI,r), and outer disks C1=B(O,R), C2=B(p+rO,rR). Each indisk is tangent to the baseline and to the two parallel supports through its two baseline feet. The shared support line is T={p+lambda e : lambda is real}. The two indisks lie in opposite closed halfplanes bounded by T. Their squared center separation minus the squared sum of radii is

    |(p+rI)-I|^2-(1+r)^2 = t^2(t-1)^2(t+1)^2/(t^2+2)^2.

Thus they are strictly non-tangent unless t=1. Direct substitution shows:

- C1 contains D1 and the feet 0,p;
- C2 contains D2 and the feet p,p+(2ar,0);
- q lies on both outer circles;
- q lies on the upper part of T, above both indisk support contacts.

Thus the compact convex sets

    K1=conv(D1,{0,p,q}),
    K2=conv(D2,{p,p+(2ar,0),q})

have disjoint interiors, share exactly segment [p,q], and fit in their indicated outer circles. In the two-foot branch their inradii are 1,r and circumradii R,rR exactly.

The distances along T from the two indisk contact points to q, divided by their respective inradii, are

    x=t^3/(1+t^2), y=1/(t(1+t^2)).

The two nonshared upper supporting tangents at q leave an interior-region opening

    phi(t)=2 atan(x)+2 atan(y).

For every t>0,

    phi(t) >= 4 atan(1/2) = 106.260204708... degrees > 90 degrees.

Proof: xy=t^2/(1+t^2)^2<=1/4, so atan(x)+atan(y)<pi/2 and the tangent addition formula applies. The claimed inequality is equivalent to

    3(t^4+1)(1+t^2)-4t(1+t^2+t^4)
      =(t-1)^2(3t^4+2t^3+4t^2+2t+3) >= 0.

At t=t0 the numerical values are

    r = 0.59469315175267761886325...
    phi = 108.62173123339741046128... degrees.

Mutual tangency would instead force r=t0^2=0.67646519733935284229541... . Using that radius ratio with the same limiting R and theta gives an opening approximately 88.984565 degrees. The latter comparison is descriptive; it is not used in any proof.

### 3.1 Actual finite polygonal cells

For every epsilon>0 the preceding pair can be replaced by two finite convex polygons with circularity at most R+epsilon, the same baseline feet and common segment [p,q], and the same upper tangent opening phi(t). Approximate each K_i from outside by finitely many of its support lines, including its two strip supports, baseline, and upper nonshared support through q. Compactness and continuity of the support function give an arbitrarily close outer approximation. It remains inside the outer circle expanded by epsilon times its inradius. The retained parallel strip supports bound the inradius above by its stated value, while the original indisk remains contained, so the inradius is exactly that value. Retaining the two supports through q preserves the vertex and opening. The common separator keeps interiors disjoint.

The companion exact-rational construction makes this approximation explicit for t=822475043597/10^12. It produces cells with 208 and 162 vertices and certifies ratio at most 1.28878 for both (the tested circle's maximum vertex-distance ratio is approximately 1.28870508). A separate verifier checks indisk containment from every polygon edge, global convexity, the retained strip width and therefore exact inradius, common-edge separation, and the outer-circle bound at every vertex using rational arithmetic. It also rejects five deliberate corruptions and is run normally and with Python -O/-OO. These checks certify a local two-cell patch only.

## 4. Admissibility, fixed complexity, and what remains

For every positive integer N the minimum circularity among partitions into at most N positive-area convex cells exists. One proof uses Hausdorff compactness of the cells in the square, after labeling and allowing empty slots. If a sequence has bounded ratios, any cell whose inradius tends to zero has its circumradius and diameter tend to zero. Such limiting points cannot account for an uncovered open subset, so the positive-area limit cells still cover the square. Their interiors remain disjoint. The radius functionals are continuous on nondegenerate compact convex sets. Finally a finite convex partition is polygonal: separate every two positive-area cells by a line and intersect the corresponding halfplanes with the square; the cover property identifies each cell with that intersection. Thus the limit is admissible and uses at most N cells.

Combined with the theorem above, the at-most-N minimum is strictly larger than G. This does not show that those minima tend to G, and does not prove nonattainment at their eventual infimum if it is larger than G.

For arbitrary infinite partitions, the finite boundary-crossing argument may fail at an accumulation point; compactness and the distinction between a maximum and a supremum also require separate treatment. No infinite-partition lower-bound or equivalence is claimed here.

The remaining obstruction is global completion: arrange an entire boundary layer and then partition the whole residual interior, with all cells obeying the same target ratio. A favorable local opening, including the one certified here, does not establish this. The new patch permits non-tangent neighboring indisks and therefore cannot be dismissed using the restricted tangent-indisk conjecture. It also does not disprove that conjecture.
