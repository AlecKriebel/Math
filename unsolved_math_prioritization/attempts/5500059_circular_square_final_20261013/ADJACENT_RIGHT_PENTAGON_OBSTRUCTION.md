# An exact pentagon obstruction for nearly perpendicular collars

Problem: row 1757 / 5500059 / AMR0540059. A local result within the fifth and final newly documented pass of this continuation, 2026-10-13. No novelty claim.

## Results and scope

**Theorem 1 (sharp adjacent-right bound).** Every convex pentagon with two adjacent interior angles exactly 90 degrees satisfies

    R/r >= rho = 1.290772978969... > 129077/100000,

where r is its largest contained-disk radius and R its smallest enclosing-disk radius. The two disk centers are independent. Let m be the unique number in (0,1) satisfying

    (1+m)^2 (1-m^2) = 4m^2.

Then

    rho = sqrt(1+(1+m)^2/4) = (1+m)/(2m).

Equality is attained by the tangential and cyclic pentagon explicitly given below.

**Theorem 2 (quantified stability).** No convex pentagon of circularity at most 64439/50000 = 1.28878 has two adjacent interior angles both within 1/1100 radians of a right angle. In particular, the interval [89.95 degrees, 90.05 degrees] is forbidden for both members of an adjacent pair.

These are local necessary conditions for a pentagonal collar cell along a fixed boundary facet. In a completion at the stated ceiling, a pentagon cannot have both incident collar seams perpendicular to that facet, or both within the quantified tolerance. They do not forbid hexagonal caps, differently oriented pentagons, or general finite completions. No conclusion for arbitrary adjacent angles merely bounded above by 90 degrees is asserted here. No convergence or nonconvergence of an optimizer is used as evidence of nonexistence.

## 1. Tangential reduction without a common-center assumption

Normalize a largest contained disk to the unit disk centered at the origin. Express the given pentagon as the intersection of its five inward-containing side half-planes

    n_i dot x <= h_i,     |n_i|=1,     h_i>=1.

Replace each h_i by 1, retaining the normal directions. The intersection P0 contains the unit disk and is a subset of the original pentagon. Its circumradius therefore does not exceed that of the normalized original. The ordered normal directions are distinct, with all consecutive angular gaps in (0,pi). Every tangent point n_i satisfies n_j dot n_i<1 for j!=i, so a neighborhood of that point on its support is feasible for all other half-planes. Thus all five tangent supports remain genuine sides, and all interior angles are preserved.

Thus it suffices to prove a lower bound on the circumradius of this tangential pentagon. It is unnecessary to assume that an original side touched the original indisk, or that either original extremizing center was the origin.

## 2. Complete proof of the sharp bound

Orient the common side of the adjacent right-angle corners horizontally, below the unit disk. The three associated tangent support lines are y=-1 and x=+/-1. List the vertices cyclically as

    A=(-1,-1), B=(1,-1), C=(1,a), D=(x,y), E=(-1,b).

The other two supports are upper tangents to the unit circle. Hence a,b>0, ab<1, and solving the two tangent-line equations gives

    x=(b-a)/(a+b),       y=(1+ab)/(a+b).

Put t=max(a,b). If t>=1, one of AC and BE has length at least 2 sqrt(2), so the enclosing radius is at least sqrt(2)>rho. Suppose 0<t<1. Two independent enclosing-radius bounds apply:

    R >= G(t) := sqrt(1+(1+t)^2/4),                      (1)

from the longer of AC and BE, and

    R >= F(Y(t)),
    Y(t) := (1+t^2)/(2t),
    F(y) := ((1+y)^2+1)/(2(1+y)).                        (2)

For (2), write the smaller of a,b as s<=t. Then

    y=(1+ts)/(t+s)
      = t + (1-t^2)/(t+s)
      >= t + (1-t^2)/(2t) = Y(t).

The smallest enclosing radius of the three points (-1,-1), (1,-1), (x,y) is at least that for x=0 with the same y. Indeed the enclosing-radius functional is convex in the point coordinates: averaging two enclosing disks gives an enclosing disk for the pointwise averages with the averaged radius, by the triangle inequality. Reflect the triangle across the vertical axis and interchange the two fixed base labels; averaging sets the apex x-coordinate to zero without increasing the optimal radius.

For the centered apex at height y>=1, the enclosing triangle is acute, its circumcircle is its smallest enclosing circle, and its radius is F(y). This can also be obtained directly by minimizing

    max(sqrt(1+(c+1)^2), y-c)

over a center (0,c). The function F is increasing for y>=1, proving (2).

Now G(t) increases strictly on (0,1), while F(Y(t)) decreases strictly from infinity to 5/4. They have exactly one crossover. The unique m in (0,1) satisfying

    (1+m)^2 (1-m^2)=4m^2                               (3)

is that crossover: substitution gives

    G(m)=F(Y(m))=(1+m)/(2m).

Uniqueness in (3) follows by writing it as

    1/(1-m^2) = (1+m)^2/(4m^2),

whose left side increases strictly from 1 to infinity and whose right side decreases strictly from infinity to 1. Equations (1)-(2) therefore give R>=rho globally, including all asymmetric choices of a,b.

For equality, take

    (-1,-1), (1,-1), (1,m), (0,(1+m^2)/(2m)), (-1,m).

Every side is tangent to the unit disk. The width between x=-1 and x=1 forces the inradius to be exactly 1. All five vertices lie on the circle with center (0,(m-1)/2) and radius rho, by (3). The diagonal from (-1,-1) to (1,m) is a diameter of that circle, so its enclosing radius is exactly rho. This proves sharpness.

## 3. An entirely rational lower bound

No numerical root approximation is needed for the strict comparison with the target. Set

    t0=63229/100000,        L=129077/100000.

For t>=t0 use (1); for t<=t0 use (2). The exact checks are

    G(t0)^2-L^2 = 8749/1600000000 > 0,

    F(Y(t0))-L
      = 2540928578701869/673861965823195600000 > 0.

Thus every adjacent-right pentagon has R/r>L=1.29077>1.28878. The included standard-library checker verifies these fractions and the stability margin below using Fraction arithmetic and explicit exceptions, not Python assertions.

## 4. Stability under normal perturbations

First record an elementary support lemma. Suppose

    P0 = intersection_i {x: n_i dot x<=1}

is contained in the radius-M disk centered at the origin. Replace its unit normals by unit normals n_i' satisfying |n_i'-n_i|<=delta and suppose M delta<1. Put

    Q = intersection_i {x: n_i' dot x<=1}.

For every unit direction u, boundedness and the radial extent of P0 imply

    max_i n_i dot u >= 1/M.

Consequently max_i n_i' dot u>=1/M-delta, so Q is bounded and |x|<=M/(1-M delta) for x in Q. Also

    n_i dot x <= n_i' dot x + delta |x|
              <= 1/(1-M delta).

Therefore

    (1-M delta) Q subset P0,
    R(Q) <= R(P0)/(1-M delta).                         (4)

This lemma allows independent enclosing centers; enclosing radius is monotone under inclusion and homogeneous under scaling.

Now suppose the original normalized pentagon has circularity R<=gamma=64439/50000 and the specified adjacent angles differ from pi/2 by at most delta=1/1100. Its enclosing disk contains the unit disk, so its center C satisfies |C|<=R-1. Thus P0 is contained in the origin-centered disk of radius

    M=2gamma-1=39439/25000.

Take the common tangent support normal at angle -pi/2. The right neighboring normal is at angle phi in [-delta,delta]; the left neighboring normal is at angle pi+eta with eta in [-delta,delta]. The remaining two normals have ordered angles between phi and pi+eta. Replace the neighboring normal angles by 0 and pi, and clamp each of the other two angles to [0,pi]. Every angular change is at most delta, hence every Euclidean normal displacement is at most delta.

The resulting Q is bounded by (4), contains the unit disk, and has the three supports y=-1, x=+/-1 plus at most two distinct upper supports. None of the upper supports cuts off (+/-1,-1), because for theta in [0,pi],

    +/-cos(theta)-sin(theta) <=1.

If both upper supports remain distinct genuine sides, Q is an adjacent-right pentagon, so R(Q)>L. If a support merges and Q is a quadrilateral, its single upper tangent has side heights a and 1/a on x=+/-1; one is at least 1, giving a diagonal of length at least 2sqrt(2). Thus R(Q)>=sqrt(2)>L. Boundedness rules out the case with no upper support.

Combining (4) with R(P0)<=R<=gamma now gives the contradiction

    gamma >= R(P0) >= (1-M delta)R(Q) > (1-M delta)L,

because the exact positive margin is

    (1-M delta)L-gamma
      = 381832197/2750000000000 > 0.

Finally, 0.05 degrees=pi/3600<1/1100 (for example pi<22/7 suffices). This proves the displayed degree version.

## 5. Conditional application to the coarsened boundary patch

The coarsened fixed patch has 416 exposed inner facets and requires at least 310 added pentagons in any completion at the target ceiling, as established separately. These counts alone do not force the adjacent-near-right pattern proved impossible here.

If a proposed completion assigns a pentagon to an entire exposed facet and both of that cell's other incident sides meet the facet within 0.05 degrees of perpendicular, that cell is impossible at circularity <=1.28878. At least one endpoint angle must leave this interval, or the cell must have at least six genuine sides. This tests a concrete candidate collar design; it does not turn the boundary-only witness into a complete partition or prove that no completion exists.

## 6. A stronger rational collar window around 90.30 degrees

The coarse perturbation from exactly 90 degrees is not the most useful test for the coarsened patch. The following separate, exactly checked window is stronger in the relevant direction.

Put

    u=131/50000,
    eta=2 arctan(u),
    alpha0=pi/2+eta,
    delta0=1/30000.

**Theorem 3.** A convex pentagon of circularity at most 1.28878 cannot have two adjacent angles both in [alpha0-delta0, alpha0+delta0]. In degrees the window endpoints are approximately 90.298319338 and 90.302139057. The approximate endpoints are explanatory only; the theorem uses the exact arctangent and radian interval above.

### 6.1 Exact equal-angle lower bound

Consider first a tangential pentagon with both specified angles exactly alpha0. Put

    s=sin(eta)=13100000/2500017161,
    c=cos(eta)=2499982839/2500017161,
    k=(1-s)/c=49869/50131.

After orientation the bottom vertices are A=(-k,-1), B=(k,-1), and the two incident side supports are

    c x-s y=1,       -c x-s y=1.

Their upper vertices can be written

    C=((1+s a)/c,a),       E=(-(1+s b)/c,b),

where a,b>-s. Write m=max(a,b). The longer cross-diagonal gives

    R >= G_eta(m)
      := (1/2)sqrt(((2+s(m-1))/c)^2+(1+m)^2).          (5)

This is increasing for m>-s. To obtain a second bound when m is small, parameterize the right upper support normal by theta1 and the left upper support normal by theta2, with theta1<theta2. The right incident normal has angle -eta. Its intersection with the right upper support satisfies

    a=-s+c tan((theta1+eta)/2).

The analogous left formula gives

    theta1<=theta_m := 2 arctan((m+s)/c)-eta,
    theta2>=pi-theta_m.

Because the intervening normal gap is less than pi, theta_m>0. If m<1, theta_m<pi/2. Put v1=pi/2-theta1 and v2=theta2-pi/2. Then v1,v2>=pi/2-theta_m>0 and v1+v2<pi. The upper apex height is

    y = cos((v1-v2)/2)/cos((v1+v2)/2)
      = (1+tan(v1/2)tan(v2/2))/(1-tan(v1/2)tan(v2/2)).

It increases with each v_i, so

    y >= 1/sin(theta_m)
      = Y_eta(m)
      := (1+m^2+2ms)/(2m+s(1+m^2)).                  (6)

On the relevant range -s<m<1 with positive denominator, Y_eta decreases: its derivative is

    -2c^2(1-m^2)/(2m+s(1+m^2))^2 < 0.

The same reflection-and-averaging argument as in Section 2 gives, whenever y+1>=k,

    R >= F_k(y) := ((1+y)^2+k^2)/(2(1+y)).            (7)

The function F_k increases for y+1>=k.

Now choose the rational split

    m0=62869/100000,       L0=32222/25000=1.28888.

If m>=m0, use (5). If m<=m0, (6) gives y>=Y_eta(m0)>1, so use (7). The exact positive checks, reproduced by the accompanying checker, are

    G_eta(m0)^2-L0^2
      =1441207690329957386549237/
       49999313562355999368000000000 >0,

    F_k(Y_eta(m0))-L0
      =122769539567160253054980613287270197037275897/
       10593995089531398850250290835758532989309685800000 >0.

Thus every such equal-angle tangential pentagon has R>L0. This argument proves a sufficient lower bound; it does not claim that (5) and (7) give the sharp minimum for eta>0.

### 6.2 Allowing the stated angle interval

Apply the support-perturbation lemma with M=39439/25000 and delta0=1/30000. Move the two incident normals to angles -eta and pi+eta and clamp the other two angles into [-eta,pi+eta]. Each normal changes by at most delta0. The resulting polygon Q keeps the two base corners (-k,-1), (k,-1): an upper tangent with normal angle in this interval cannot cut them off. For example k cos(theta)-sin(theta)<=1 throughout the interval; its interior critical point there is a minimum and its endpoint values are 1 and -1+2s. The reflected inequality applies at the other base corner.

If both upper supports are genuine, Q is a pentagon of the equal-angle type just bounded. If Q has only one genuine upper support, it is a quadrilateral; its upper edge crosses x=0 at height at least 1 because Q contains the unit disk. At least one of its upper endpoint heights is therefore >=1. Its cross-diagonal then gives

    R(Q)>=G_eta(1)=sqrt(1+1/c^2)>sqrt(2)>L0.

The boundedness estimate rules out a polygon with no upper support. Consequently R(Q)>L0 in every case, while (4) and the target ceiling would imply

    gamma >= (1-M delta0)R(Q) > (1-M delta0)L0.

The exact contradiction is

    (1-M delta0)L0-gamma
      =302098271/9375000000000 >0.

This proves Theorem 3.

### 6.3 Exact membership for two facets of the pinned coarsened patch

The checker reads the coarsened rational certificate and requires SHA-256

    6e7136b295451a6bd8c49c04440f319dce534c94f91484eac21530e53492393e.

It selects the canonical type named left_1 and its zero-based vertex indices 5, 6, and 7. These are one-cell vertices of the exposed inner boundary, rather than prescribed shared endpoints, as in the separately verified patch topology. At each vertex form the incoming and outgoing directed edge vectors e,f and set

    D=e dot f,       K=det(e,f).

The checker verifies D>0 and K>0. Thus the polygon's positive exterior turn tau lies in (0,pi/2), with tan(tau)=K/D. Put the exact rationals

    q0=tan(eta)=13100000/2499982839,
    q_minus=q0-1/30000,
    q_plus=q0+1/30000.

For each of the three vertices it verifies strictly

    K(1-q_minus^2)-2q_minus D > 0,
    2q_plus D-K(1-q_plus^2) > 0.

Because 0<q_minus<q_plus<1 and tan(2 arctan q)=2q/(1-q^2), these inequalities prove

    q_minus < tan(tau/2) < q_plus.

The derivative of arctan is at most 1, so

    |tau/2-eta| < 1/30000.

The equal division of the unfilled sector produces a collar-cell angle

    (2pi-(pi-tau))/2 = pi/2+tau/2,

which therefore lies strictly inside Theorem 3's excluded interval. All comparisons use the exact rational vertices; no rounded angle is used. The exact positive margins are retained in [EXACT_PENTAGON_OBSTRUCTION_CHECK.json](EXACT_PENTAGON_OBSTRUCTION_CHECK.json).

Consequently, under the prescription that the separating collar seams at these vertices are the exact bisectors of the unfilled sectors, neither full facet 5->6 nor full facet 6->7 can be the base side of a pentagonal added cell of circularity <=1.28878. The same local obstruction holds for every similarity or reflected/rotated occurrence of these facets. It does not constrain a collar that changes these separators, subdivides the facets, or uses cells of at least six sides.

The displayed endpoint angles, computed only for orientation, are approximately 90.301256663, 90.299877037, and 90.298490551 degrees. They are not inputs to the proof.

### 6.4 Replay

The standard-library checker uses the exact [coarsened boundary certificate](../5500059_circular_square_fourth_20261013/coarsened_boundary_certificate.json). Its [mathematical output](EXACT_PENTAGON_OBSTRUCTION_CHECK.json) and [mode replay record](MODE_REPLAY_CHECK.json) are published here. The normal, -O, and -OO runs produce identical JSON. Every failed check raises an explicit exception, so optimized interpreter modes retain all acceptance checks. The complete independent [proof audit](INDEPENDENT_PENTAGON_REVIEW.md) and [arithmetic check](INDEPENDENT_PENTAGON_CHECK.json) are separate evidence.
