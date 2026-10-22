# Inner focal-pedal areas: equality, positivity and quotient domain

**5100037 / AMR-050-0037, arXiv k609. Author turn 1; unreviewed full domain-qualified candidate.** No novelty or priority claim.

## 1. Source target and statement

The target is k609 in Table 7, p.9 of Reznik–Garcia–Koiller,
*Eighty New Invariants in the Elliptic Billiard*, arXiv:2004.12497v11,
29 October 2020. It states equality of the ratio of the two focal
**pedal areas of the inner polygon** to 1 for even N. This row has no
counterpart in the final *Fifty New Invariants*, Arnold Math. J. 7
(2021), Table 7, p.349. The inner vertices are the caustic tangency
points in billiard traversal order, not the original vertices or the
outer tangent intersections. Pedal vertices are orthogonal projections
onto the supporting lines of consecutive inner-polygon sides.
The source's equation (1) uses signed shoelace area, including stars.

Let the outer ellipse be x²/a²+y²/b²=1, a>b>0, with foci
F±=(±c,0), c²=a²−b², and fix a strictly nested nondegenerate
confocal elliptical caustic. Let P_i, indexed cyclically modulo N,
be a primitive billiard orbit of even least period N. Let R_i be the
contact point of side P_i P_(i+1) with the caustic. Define

    d_i=R_(i+1)−R_i,
    Q_i(M)=R_i+d_i [(M−R_i)·d_i]/|d_i|²,
    B_M=(1/2) sum_i det(Q_i(M),Q_(i+1)(M)).       (1)

### Theorem

For every such primitive even orbit, all d_i are nonzero and

    B_(F+)=B_(F−).                               (2)

Thus k609 is the constant 1 on its defined quotient locus, and the
cross-multiplied identity is valid at every orbit. For convex orbits,
the common signed area is strictly positive in counterclockwise
orientation, so the quotient is defined everywhere. Primitive stars
can have common zero area: §4 gives an exact winding-3, period-8
example with finite pedal vertices. There the literal quotient is
0/0; its constant removable extension is still 1.

This is not a refutation of rational invariance. No claim of phase
variation of a defined quotient is made. Repetitions of even primitive
orbits retain equality; an artificially even indexing length of a
repeated odd orbit is not used to infer central symmetry.

## 2. Central symmetry and finite projection lines

We credit the established input: Stachel, *The geometry of billiards
in ellipses and their Poncelet grids*, J. Geom. 112, article 40 (2021),
Corollary 4.2(i), pp.22–23, DOI 10.1007/s00022-021-00606-2.
Primitive even period forces odd turning number, and the theorem gives

    P_(i+N/2)=−P_i.                              (3)

Central inversion sends each chord tangent to the centrally symmetric
caustic to its opposite chord. The tangency point is unique, hence

    R_(i+N/2)=−R_i.                              (4)

Consecutive R_i are distinct. Otherwise the adjacent sides would be
the same caustic tangent line. Specular reflection on a single line
would require either grazing incidence or normal backtracking.
Grazing uses the outer tangent, which misses the inner caustic.
At P=(a cos(theta),b sin(theta)), the normal chord has confocal
parameter lambda=a² sin²(theta)+b² cos²(theta)>=b², as follows from
the dual-conic line tangency formula. It cannot be tangent to the
strict elliptical caustic, whose parameter satisfies 0<lambda<b².
Thus neither case occurs. Every inner side and projection in (1)
is well defined.

Orthogonal projection is equivariant under the isometry X↦−X.
Applying (4) to the line R_i R_(i+1) therefore yields

    Q_(i+N/2)(F−)=−Q_i(F+).                     (5)

This is a cyclic shift with orientation preserved, not reversal.
Since det(−X,−Y)=det(X,Y), summing (5) in (1) proves (2), including
all primitive star turning numbers under the same caustic hypotheses.

The source already invokes this mechanism for neighboring original
and outer focal-pedal equalities. The campaign's arXiv k607 work also
uses the same credited central inversion. The present contribution
checks the distinct inner-polygon construction and its domain; these
are not counted as independent discoveries of the symmetry theorem.

## 3. A denominator theorem for the convex case

We prove a general Euclidean lemma: a centrally symmetric strictly
convex polygon with at least four vertices has positive signed pedal
area from every point, in counterclockwise traversal.

Write N=2m. Let its outward side normals be
n_i=(cos theta_i,sin theta_i), support numbers h_i>0, and
t_i=(-sin theta_i,cos theta_i). The origin is its symmetry center.
Let delta_i=theta_(i+1)−theta_i be the positive turning increments,
chosen so 0<delta_i<pi. Central symmetry gives
n_(i+m)=−n_i, h_(i+m)=h_i, and
sum_(i=0)^(m−1) delta_i=pi. The projection is

    Q_i(M)=h_i n_i+t_i(t_i·M).                   (6)

In the signed area, the linear terms in M cancel between opposite
index pairs. For the quadratic terms, the trigonometric identities

 2 sin(delta_i) cos(2phi−theta_i−theta_(i+1))
   =sin(2phi−2theta_i)−sin(2phi−2theta_(i+1))

telescope around the cycle. Expanding the products in (6) consequently
gives the exact radial formula

    B_M=B_0+C |M|²,
    B_0=(1/2) sum_i h_i h_(i+1) sin(delta_i)>0,
    C=(1/8) sum_i sin(2delta_i).                 (7)

To determine the sign of C, consider the m unit-circle points with
angles 2theta_0,...,2theta_(m−1). They are distinct and occur in
counterclockwise cyclic order. If m≥3, they form a strictly convex
inscribed polygon of positive area D. Its shoelace formula and the
opposite-pair repetition give C=D/2>0. For m=2 its two-edge shoelace
sum is zero, so C=0. In all cases B_M>0.

For a convex primitive even billiard, the contacts R_i occur in cyclic
order on the strictly convex caustic. Their inner polygon is strictly
convex and centrally symmetric, so this lemma applies at both foci.
Reversing traversal negates both areas and still leaves a nonzero
denominator. The positivity assertion is not extended to star polygons.

## 4. An exact zero for a primitive star

This example verifies that the signed-area qualification matters even
though all pedal projections are finite.

Let t be any root in (3/8,2/5) of

    f(t)=t⁷−4t⁶+3t⁵+6t⁴−t³+5t−2.              (8)

Such a root exists because
f(3/8)=−98389/2097152<0 and f(2/5)=8248/78125>0.
Set

    C=(1−t²)/(1+t²), S=2t/(1+t²), b=1,
    a²=R=C(1+S)/(S(1+C))=(1−t)(1+t)³/(4t),
    c=sqrt(R−1).                                (9)

The interval lies below sqrt(2)−1, so 0<S<C<1, C²+S²=1 and R>1.
The following is the billiard traversal order:

    (a,0), (−aC,S), (0,−1), (aC,S),
    (−a,0), (aC,−S), (0,1), (−aC,−S).           (10)

These are the eight distinct ellipse vertices in cyclic-position
step 3 order, hence winding number 3 and least period 8 once the
reflection law is checked.

### 4.1 Reflection and caustic certificate

At P=(−aC,S), let d_1=|P−(a,0)| and
d_2=|(0,−1)−P|. Equation (9) gives the positive ratio

    d_1/d_2=(1+C)/(1+S).

For the incoming and outgoing unit velocities,

 v_in−v_out=(1+C+S)/d_1 · (−a(1+C)/(1+S),1),

which is parallel to the outward normal (−C/a,S) by (9).
This proves specular reflection at P. The remaining vertices follow
from the two axial symmetries. All eight sides are tangent to

    x²/(a²−lambda)+y²/(1−lambda)=1,
    lambda=R(1+C)²/[S²+R(1+C)²],                (11)

since the adjacent chord's expression
R(1+S)²/[(1+S)²+R C²] is identical. The dual-conic tangency test
verifies both expressions directly. We have 0<lambda<1, establishing
a strict nondegenerate confocal elliptical caustic.

### 4.2 The inner contacts and exact pedal area

Define positive numbers

 X=(R−lambda)/a,       Y=(1−lambda)(1+C)/S,
 U=(R−lambda)(1+S)/(aC), V=1−lambda.

The contact points of the sides in (10), in the same cyclic order, are

 (X,Y), (−U,−V), (U,−V), (−X,Y),
 (−X,−Y), (U,V), (−U,V), (X,−Y).               (12)

For example the first side has line equation
S x+a(1+C)y=aS, and its contact is obtained by applying
diag(R−lambda,1−lambda) to its normal and dividing by aS.
This gives (X,Y). The adjacent side and reflections give all of (12).
Since U>X>0 and Y>V>0, these eight points are distinct.

Apply the explicit projection formula (1) with M=(c,0) to (12).
Put

    G(t)=t⁶−2t⁵−3t⁴−8t³+3t²+2t−1.

Exact rational simplification, using c²=R−1 and (9), gives

 B_(F+)/a = −8t³(1−t)²(1+t)² f(t)
             /[(1+t²)²(t²−2t−1)² G(t)].          (13)

There is no hidden zero denominator in (13). Indeed direct substitution
also gives

 (X+U)²+(Y+V)²
   =−(1+t)² G(t)/[t(1+t²)(t²−2t−1)²]>0.        (14)

Thus G(t)<0 on the stated interval. All other displayed factors in the
denominator are nonzero. Equations (13)–(14) are finite rational
identities verified by the authored exact checker, which constructs
the contacts and pedal feet directly rather than assuming the result.
At the root (8), the signed area is exactly zero. Equation (2) gives
zero at the opposite focus too.

This is a genuine admissible star, not a repeated smaller orbit,
spurious scalar root, tangent-line singularity or unsigned-area claim.
The construction varies the ellipse/caustic with t; it does not assert
that a defined quotient changes within one Poncelet family.

## 5. Disposition

The source invariant is established on its defined locus, with the
global polynomial identity of equal signed areas. For convex primitive
even orbits the quotient is globally defined. Stars require the stated
zero-area qualification and admit the exact exception above. At common
zeros one can use the constant removable extension, but the raw 0/0
expression itself is not assigned a real value.

The substantial central-symmetry input is credited to Stachel and the
neighboring source symmetry arguments. Finite exact checks are algebraic
controls, not substitutes for this universal geometric proof. No claim
is made for hyperbolic caustics, repeated odd primitive periods, or the
different published table labels.
