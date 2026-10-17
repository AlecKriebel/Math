# Third-pass cofactor normal form and compact-quadratic controls

Third mathematical edition. This is the corrected mathematical text accepted by the [independent cofactor audit](INDEPENDENT_COFACTOR_ACCEPTANCE.md). Agreement of the piecewise spline with the local polynomial is restricted to incident edge segments.

## Scope and outcome

This is one branch of the same shared third substantive pass for row 1761 / problem 30002861 / OWR-13678-002. It does not add a separate pass. The accepted second-pass reduction, balance criterion, exterior-attachment theorem and compact-quadratic construction are the baseline, linked in [DEPENDENCIES.md](DEPENDENCIES.md).

This branch gives an exact characterization of the special local proportionality, an exact counterexample to a naive directional-derivative maximum principle, and a fully explicit compact quadratic on a Morgan–Scott-type disk that demonstrates why compact support and nonzero jumps alone are insufficient. It also excludes the direct construction obtained by independently scaling and gluing these zero-boundary patches at a macro vertex with three distinct incident macro-edge lines.

These results do not construct a balanced admissible support, do not prove universal quartic interpolation, and do not replace the required exterior geometry or full Ceva magnitudes.

## 1. Exact local normal form

Let v be an original even-valence interior vertex, with its full counterclockwise fan of outgoing vectors d_i and triangles T_i=(v,v+d_i,v+d_(i+1)). Put

    a_i=det(d_i,d_(i+1))>0,
    L_i(X)=det(d_i,X-v),
    s_i in {+1,-1}, s_(i+1)=-s_i,
    rho_i=s_i det(d_(i-1),d_(i+1))/(a_(i-1)a_i).

Indices are cyclic. This is the accepted face-color normalization of the quartic row. The following is a local equivalence, allowing zero row entries.

**Normal-form lemma.** A C1 piecewise quadratic q on this full fan has jumps

    q_(T_i)-q_(T_(i-1))=x_v rho_i L_i^2

for one scalar x_v if and only if there is one polynomial p_v of degree at most two such that

    q_(T_i)(X)=p_v(X)+x_v s_i L_i(X)L_(i+1)(X)/a_i.       (1)

The p_v has the same value and gradient as q at v. If the row is nonzero, x_v and p_v are unique.

**Proof.** The elementary linear-form identity

    L_(i+1)/a_i + L_(i-1)/a_(i-1)
      = det(d_(i-1),d_(i+1)) L_i/(a_(i-1)a_i)

holds because both sides vanish on d_i and have the same value on d_(i+1). Therefore the adjacent differences of

    F_i=s_i L_i L_(i+1)/a_i

are rho_i L_i^2. Subtracting x_v F_i from q_(T_i) makes every adjacent polynomial difference zero; connectivity gives a single polynomial p_v. Conversely, (1) gives the required differences. Each F_i is homogeneous of degree two around v, so its value and gradient there vanish. If two values of x_v work, their difference times every nonzero rho_i vanishes. Thus x_v, and then p_v, are unique. ∎

The same statement applies at a boundary vertex of a closed support by including its actual original exterior triangles, where the compact extension q is identically zero. One must not invent a circular fan using only the supported rays: its missing angular sector need not be a legal triangle.

### Hessian and edge-gradient form

Let J=[[0,-1],[1,0]], n_i=Jd_i, and define

    S_i=(n_i n_(i+1)^T+n_(i+1)n_i^T)/a_i.

Then

    det(S_i)=-1,
    S_i d_i=-Jd_i,
    S_i d_(i+1)=Jd_(i+1),
    S_i+S_(i-1)
      =2 det(d_(i-1),d_(i+1)) n_i n_i^T/(a_(i-1)a_i).

Writing B_v=D²p_v gives

    D²q_(T_i)=B_v+x_v s_i S_i,                            (2)
    g_(v+d_i)-g_v=(B_v-x_v s_i J)d_i,                    (3)

where g is the continuous piecewise-linear gradient of q. These identities follow by differentiating (1). The determinant identity follows from det(n_i,n_(i+1))=a_i and det(uv^T+vu^T)=-det(u,v)^2.

In particular q agrees with the single polynomial p_v on every incident edge segment. The two polynomial pieces adjacent to that segment also agree with p_v on its entire supporting line. This does not assert agreement of the piecewise function q with p_v on the opposite ray when that ray lies inside a different fan sector. This is a stronger condition than merely possessing some moment-compatible quadratic cofactors at v; for higher valence it is the exact extra restriction relevant to the quartic problem.

## 2. A strict local maximum of a directional derivative is possible

The normal form does not give a local maximum principle for derivatives. Here is a rational negative control in a nonsingular four-star, with every cofactor nonzero.

Take v=(0,0) and, counterclockwise,

    d_0=(1,0), d_1=(1,5), d_2=(-3,-1), d_3=(0,-1).

The consecutive doubled areas are (5,14,3,1), all positive. Use s_i=(-1)^i, x_v=1, and

    B=[[-1/4,33/32],[33/32,0]],
    p_v(X)=(1/2) X^T B X,
    q_i=p_v+s_i L_i L_(i+1)/a_i.

The nonzero cofactor row is

    rho=(1/5,1/70,-1/42,-1/3).

The scalar function h=partial_x q is continuous and piecewise linear, with h(v)=0 and

    (h(d_0),h(d_1),h(d_2),h(d_3))
       =(-1/4,-3/32,-41/32,-1/32).

All four values are strictly negative. On each star triangle h is affine, so h(X)<0 at every point other than v. Thus h has a strict local maximum at v, even under precisely the special cofactor condition and with all fan jumps nonzero. Any purported proof that locally forbids such maxima needs an additional hypothesis. This example is local and is not asserted to extend compactly or to satisfy the global support conditions.

## 3. Exact compact quadratic with all jumps nonzero

Consider the triangle with vertices

    A=(0,0), B=(5,0), C=(0,5)

and interior vertices

    a=(2,2), b=(1,2), c=(2,1).

In the following order, the seven triangles and their quadratic pieces are

    T_0=(A,B,c):       3 y²,
    T_1=(B,a,c):      -x²-6xy+10x-6y²+30y-25,
    T_2=(B,C,a):       3(x+y-5)²,
    T_3=(C,b,a):      -6x²-6xy+30x-y²+10y-25,
    T_4=(C,A,b):       3x²,
    T_5=(A,c,b):      -x²+4xy-y²,
    T_6=(a,b,c):      -6x²-6xy+30x-6y²+30y-45.

Set q=0 outside ABC. All triangles have positive orientation, and their pairwise intersections are precisely the prescribed common simplices. They form a conforming triangulation of ABC. Exact triangle-intersection, boundary-cycle, and vertex-link checks are specified in [REPRODUCTION.md](REPRODUCTION.md) and independently accepted in the [cofactor audit](INDEPENDENT_COFACTOR_ACCEPTANCE.md).

Number A,B,C,a,b,c by 0,...,5. For each edge oriented from the smaller to the larger index, the scalar a_e in

    q_left-q_right=a_e det(v_j-v_i,X-v_i)^2

is, in the following edge order,

    edges: (0,1),(0,2),(0,4),(0,5),(1,2),(1,3),
           (1,5),(2,3),(2,4),(3,4),(3,5),(4,5),

    a_e:   3/25,-3/25,1,-1,3/25,-1,1,1,-1,-5,5,-5.

Every scalar is nonzero. These exact polynomial identities prove C1 continuity across every edge, including the boundary against the zero exterior. The spline is nonzero: it has value 3 at each of a,b,c and value 5 at (5/3,5/3).

Each of a,b,c has degree four and four distinct incident line directions, so each is a nonsingular degree-four interior vertex. At such a star the three-dimensional squared-line moment system has one-dimensional kernel, hence its nonzero cofactor vector is automatically proportional to the quartic row. Thus even compactness, nonzero cofactors on every edge, three nonsingular interior four-stars, and the requisite proportionality at all interior vertices of this disk do not suffice for a contradiction.

The piecewise Hessian determinants in the displayed triangle order are

    (0,-12,0,-12,0,-12,108).

The three negative-determinant faces each have area 3/2, and the central positive-determinant face has area 1/2. Thus the integral of det(D²q) is exactly zero, with genuine cancellation. The determinant-minus-one normal-form matrices do not force the actual Hessians to have nonpositive determinants. This explicit control also blocks an argument that would replace the compact Hessian determinant integral by a strictly signed energy without additional justification.

This is not a quartic counterexample. Its support has only three strict boundary corners. The accepted exterior-attachment theorem rules out embedding this disk as a closed quartic active support: the required exterior vertex across AB would have to lie simultaneously on the positive outward continuations of CA at A and CB at B. Those lines meet at C, which lies on neither outward ray. The boundary vertices do not possess admissible full exterior fans satisfying the required zero coefficients.

### Relation to the inspected primary source

Feng, Kozak and Zhang, *On the Dimension of the C1 Spline Space for the Morgan–Scott Triangulation from the Blossoming Approach* (1996), explicitly treats the seven-triangle inner/outer-triangle configuration. Its abstract and introduction state that the C1 quadratic dimension is seven rather than six exactly when the three corresponding inner-to-outer lines are concurrent. The present example has Aa, Bb and Cc concurrent at (5/3,5/3). The formulas and compactness above are independently verified here; the source's dimension statement alone is not used to assert compactness or the quartic cofactor condition.

Primary author-hosted PDF, inspected 2026-10-13, pages 1–2:
https://users.fmf.uni-lj.si/kozak/RaziskovalnoDelo/NekateriClanki/DIMS1N/fengetal.pdf

## 4. Why direct zero-boundary patch gluing fails

A limited obstruction explains why simply tiling a larger convex polygon with scaled copies of the preceding compact patch does not automatically repair its boundary.

**Three-ray zero lemma.** Suppose q satisfies the local normal form at v, q(v)=0 and gradient q(v)=0. If q vanishes identically on three incident edge segments with distinct supporting lines, then q vanishes identically on every incident edge segment.

**Proof.** Formula (1) says q=p_v on each incident edge segment. Since p_v has zero value and first derivatives at v, it is homogeneous quadratic in X-v. Vanishing on each of the three nondegenerate segments forces p_v to vanish on its entire supporting line. A nonzero homogeneous binary quadratic cannot vanish on three distinct lines through the origin. Therefore p_v=0, and (1) gives the claim on every incident edge segment. ∎

Now triangulate a macro domain and put an independently scaled affine image of the explicit compact patch inside each macro triangle. This produces a C1 quadratic globally, because every patch has zero value and gradient on its macro boundary. At an old macro vertex v, q and its gradient vanish. Suppose v has an actual full even fan, including exterior triangles where needed, and the quartic proportionality is imposed there. If at least three distinct macro-edge lines are incident to v, their incident macro-edge segments satisfy the three-ray lemma, which forces zero values at every neighboring micro vertex. But the two interior micro vertices adjacent to v inside each incident macro triangle have the patch amplitude times the nonzero value 3 (under our normalization). Hence every patch amplitude in a macro triangle incident to v must be zero if the quartic proportionality is to hold there.

This is a rigorous obstruction to that particular direct assembly. It is not an obstruction to all Morgan–Scott-based constructions: overlapping constructions, different boundary data, or macro stars with only two distinct line directions are not covered. Neither are general box-spline constructions covered by this argument.

## 5. Remaining obstruction

The unresolved task remains an admissible convex closed support with at least five strict corners, actual feasible exterior attachments, even nonsingular supported original vertices, and full magnitude balance on every cycle. The local normal form is equivalent to the required local cofactor span but supplies no global positivity. The strict-maximum control shows why local maximum-principle reasoning cannot be substituted for such positivity. The compact triangular control shows why general compact-spline existence cannot be substituted for the missing exterior geometry.

## 6. Exact reproduction

The [mathematical certificate](THIRD_PASS_CERTIFICATES.json) specifies the exact authored coordinates, polynomial coefficients, fan data, jumps, and Hessian values. [REPRODUCTION.md](REPRODUCTION.md) explains how to reconstruct every local and compact polynomial identity, all 21 triangle intersections, the boundary and links, the interior cofactor proportionalities, and the Hessian integral. The three-ray zero lemma and the general assembly implication are proved above rather than inferred from finite tests.
