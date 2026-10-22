# Independent audit of the restricted pentagon obstruction

Problem row 1757 / 5500059 / AMR0540059. Audit date: 2026-10-13. No novelty claim.

## Verdict and exact scope

Accepted: the bound for every convex pentagon with two adjacent right angles is sharp, attained, and permits independent incenter and circumcenter. Its value is rho=1.290772978969... . The two perturbation results also follow: an excluded adjacent-angle interval near 90 degrees and a separate narrower interval centered near 90.30 degrees. The second interval excludes pentagonal full-facet caps on specified edges of the pinned boundary patch **only under the exact equal-free-sector-bisector seam prescription**.

There is no unrestricted lower bound above G, no obstruction to every completion of the fixed patch, and no whole-square upper-bound improvement. Variable seams, subdivided facets, and cells with six or more sides are outside that restricted conclusion.

The full [proof](ADJACENT_RIGHT_PENTAGON_OBSTRUCTION.md), with references normalized for this edition, is 16,432 bytes, SHA-256 `62e58b11308988277bb535dadaf6175384bea49bb269743c65fd2f51048be76d`. Its complete rational [boundary dependency](../5500059_circular_square_fourth_20261013/coarsened_boundary_certificate.json) is included as an exact sibling dependency, SHA-256 `6e7136b295451a6bd8c49c04440f319dce534c94f91484eac21530e53492393e`.

One purely documentary reference in the original proof section 6.3 read `EXACT_CHECK.json`; this edition corrects that link to [EXACT_PENTAGON_OBSTRUCTION_CHECK.json](EXACT_PENTAGON_OBSTRUCTION_CHECK.json). The independent margins are in [INDEPENDENT_PENTAGON_CHECK.json](INDEPENDENT_PENTAGON_CHECK.json). This filename clarification changes no formula, claim, or acceptance result; the complete original proof remains separately preserved.

## Tangential reduction

Normalize a largest contained disk to radius one at the origin. Move each of the five distinct supporting lines inward until tangent to that disk, retaining its normal. The new intersection is contained in the original pentagon, so its circumradius is no larger. All consecutive normal gaps remain in (0,pi), and the polygon is bounded.

Every support is genuine: its tangent point satisfies every other distinct unit-normal constraint strictly, so a neighborhood along that tangent line is feasible. Thus this reduction really preserves five sides and every interior angle; it does not silently replace the pentagon by a different angle class. The new unit disk is a valid contained disk, and the lower bound sought is on its circumradius. No assertion about concentric extremizing circles is needed.

## Adjacent-right family and asymmetric cases

Orient the common base as y=-1. The neighboring tangent supports are x=1 and x=-1. The vertices have the form

    A=(-1,-1), B=(1,-1), C=(1,a),
    D=((b-a)/(a+b),(1+ab)/(a+b)), E=(-1,b),

where a,b>0 and ab<1. These ranges follow from the ordered two upper support normals between the vertical support normals. Their intersection formula follows by solving their tangent equations.

Set t=max(a,b). For t>=1, a cross-diagonal has length at least 2sqrt(2), already giving a stronger lower bound. For 0<t<1, the longer of AC and BE yields

    R >= G(t)=sqrt(1+(1+t)^2/4).

Writing the smaller height as s<=t, the apex height satisfies

    y=(1+ts)/(t+s)=t+(1-t^2)/(t+s)
     >=(1+t^2)/(2t)=Y(t).

The smallest enclosing radius of the three points A,B,(x,y) is at least that of A,B,(0,y). To justify this carefully, reflect the apex and the enclosing disk, interchange the fixed base labels, and average corresponding point coordinates and disk centers. The triangle inequality puts each averaged point in the averaged-radius disk. This is the required convexity of the minimum-enclosing-radius functional; it does not assume the original optimizer's center lies on the axis.

For the centered apex and y>=1, the triangle is acute, and its circumcircle is its minimum enclosing circle. The radius is

    F(y)=((1+y)^2+1)/(2(1+y)).

The same expression follows by minimizing the larger of the base-vertex distance and apex distance over an axis center. It increases on y>=1, so R>=F(Y(t)). G increases on (0,1), while F composed with Y decreases from infinity to 5/4. Their crossover is unique and controls every asymmetric pentagon through the maximum of these two bounds.

Let m be the unique root in (0,1) of

    (1+m)^2(1-m^2)=4m^2.

Uniqueness follows from the increasing left function 1/(1-m^2) and decreasing right function (1+m)^2/(4m^2). Direct substitution gives

    G(m)=F(Y(m))=(1+m)/(2m)=rho.

The independent checker verifies both equality numerators reduce to precisely

    q(m)=m^4+2m^3+4m^2-2m-1.

It independently bisects a rational bracket of this unique root and encloses rho between rational endpoints within (1.290772978968,1.290772978971). This decimal enclosure is ancillary to the analytic argument.

## Equality is attained

The symmetric pentagon

    (-1,-1), (1,-1), (1,m),
    (0,(1+m^2)/(2m)), (-1,m)

has all five supports tangent to the unit disk. The distance between its two vertical supports is two, so no larger disk fits; its true inradius is exactly one. Its five vertices lie on the circle centered at (0,(m-1)/2) with radius rho. The same quartic verifies the apex equality. The segment from (-1,-1) to (1,m) is a diameter of that circle, forcing the true circumradius to be at least rho. Therefore the bound is an attained sharp minimum in this restricted angle class, not merely an infimum or numerical candidate.

## Rational lower bound and support perturbation

At t0=63229/100000 and L=129077/100000, the checker independently obtains

    G(t0)^2-L^2=8749/1600000000>0,
    F(Y(t0))-L=2540928578701869/673861965823195600000>0.

Monotonicity on the two sides of the split gives the strict global comparison R>L without numerically approximating m.

The support perturbation lemma is valid with free enclosing centers. If a unit-tangent polygon P is contained in the origin-centered disk of radius M, then for every unit direction u its support-normal maximum is at least 1/M. Perturb every unit normal by Euclidean distance at most delta with Mdelta<1. The new normal maximum is at least 1/M-delta, so the perturbed intersection Q is bounded by M/(1-Mdelta). Its points satisfy each original support inequality with right side at most 1/(1-Mdelta). Hence

    (1-Mdelta)Q subset P,
    R(Q)<=R(P)/(1-Mdelta).

For an original normalized cell of circumradius at most gamma, the enclosing disk contains the unit disk, so its center is within gamma-1 of the origin and P lies within M=2gamma-1. This justifies the origin-based M even though the enclosing center is independent.

When the two adjacent angles lie within delta=1/1100 of pi/2, straighten the neighboring normals and clamp the remaining normals between them. Every angular movement, and therefore every Euclidean normal movement, is at most delta. Boundedness follows from the lemma. The two base corners remain, and Q is either an adjacent-right pentagon or a quadrilateral with one upper tangent. In the latter case one upper height is at least one, forcing a cross-diagonal lower bound sqrt(2). Fewer sides are incompatible with boundedness.

Thus R(Q)>L in every case, while

    (1-Mdelta)L-gamma=381832197/2750000000000>0

contradicts the hypothesized original ceiling. The degree interval +/-0.05 degrees is contained in this radian interval by pi<22/7. The claim does not extend merely because both angles are at most 90 degrees.

## The independent near-90.30-degree window

Put u=131/50000, eta=2arctan(u), and alpha0=pi/2+eta. Rational half-angle identities give

    sin(eta)=13100000/2500017161,
    cos(eta)=2499982839/2500017161,
    k=(1-sin(eta))/cos(eta)=49869/50131.

The base corners are (+/-k,-1), and the adjacent support lines are +/-cos(eta)x-sin(eta)y=1. Their upper endpoint heights a,b are greater than -sin(eta). With t=max(a,b), the longer cross-diagonal gives the displayed G_eta(t) bound in the proof.

The two upper normal angles satisfy theta1<=theta_t and theta2>=pi-theta_t, where theta_t=2arctan((t+sin(eta))/cos(eta))-eta. The intervening normal gap is less than pi, so theta_t>0. On t<1, theta_t<pi/2. Defining v1=pi/2-theta1 and v2=theta2-pi/2 gives positive v1,v2 with sum below pi. The apex height

    (1+tan(v1/2)tan(v2/2))/(1-tan(v1/2)tan(v2/2))

increases with each variable, proving the rational lower bound

    Y_eta(t)=(1+t^2+2t sin(eta))/(2t+sin(eta)(1+t^2)).

Its derivative is negative on the relevant range. The reflection-and-averaging argument with base half-width k gives F_k(y)=((1+y)^2+k^2)/(2(1+y)), increasing in the used acute-triangle range.

At the rational split t0=62869/100000 and lower bound L0=32222/25000, the independent checker reproduces both exact positive diagonal and triangle margins. It verifies their geometric range hypotheses, rather than accepting a positive fraction detached from its domain. This proves R>L0 for exactly equal adjacent angles alpha0. It does not establish sharpness for these tilted angles.

Perturbing angles by at most delta0=1/30000 straightens the two neighboring normals to -eta and pi+eta and clamps the remaining normals between them. Their upper tangents cannot cut off the base corners, as the endpoint and critical-point check of kcos(theta)-sin(theta)<=1 shows. A bounded quadrilateral degeneration has an upper edge crossing x=0 at height at least one, so at least one upper endpoint has height at least one. Its diagonal bound exceeds sqrt(2). Therefore both pentagonal and degenerate-quadrilateral cases have R(Q)>L0.

Finally,

    (1-Mdelta0)L0-gamma=302098271/9375000000000>0.

This gives the exact excluded interval [alpha0-delta0,alpha0+delta0]. Approximate degree endpoints are explanatory, not acceptance inputs.

## Exact application and semantic controls

For canonical left_1 vertices 5,6,7 of the pinned boundary certificate, the independent checker computes the incoming/outgoing dot product D and positive determinant K. With q0=tan(eta) and q_-=q0-delta0, q_+=q0+delta0, all three satisfy

    K(1-q_-^2)>2q_-D,
    K(1-q_+^2)<2q_+D.

Since all relevant tangents are in their increasing branch, this puts tan(tau/2) between q_- and q_+. The derivative bound |arctan'|<=1 gives |tau/2-eta|<delta0. The equal split of the exterior sector therefore has angle pi/2+tau/2 inside the forbidden interval. Both whole facets 5->6 and 6->7 have forbidden angles at both ends under the prescribed bisectors. Similarities and reflections preserve that conclusion at all eight occurrences.

The fresh standard-library checker imports no producer code. Six semantic negative controls reject an overstrong false lower bound, excessive perturbation tolerance, the wrong selected vertex, an incorrect central angle, a bad diagonal/triangle split, and a collapsed boundary edge. Exact outputs and all controls are compared in normal, -O, and -OO modes. The checker verifies arithmetic and the proof's concrete premises; the analytic reductions and monotonicity arguments above are supplied by this independent authored review, not claimed to follow from computation alone.
