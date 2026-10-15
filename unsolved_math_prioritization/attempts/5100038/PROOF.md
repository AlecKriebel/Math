# Inner focal-antipedal areas and their exact domain

**5100038 / AMR-050-0038, arXiv k610. Author turn 1; full domain-qualified candidate awaiting independent review.** No novelty or priority claim.

## 1. Exact source assertion

The target is k610 in Reznik–Garcia–Koiller, *Eighty New Invariants in
the Elliptic Billiard*, arXiv:2004.12497v11, 29 October 2020,
Table 7 p.9. It concerns the two focal **antipedal areas of the inner
caustic-contact polygon**, whose ratio is asserted to be 1 for even N.
It is absent from the final *Fifty New Invariants*, Arnold Math. J. 7
(2021), Table 7 p.349. The latter is not used as a replacement target.

Let E be x²/a²+y²/b²=1, a>b>0, with foci F±=(±c,0),
c²=a²−b². Fix a strict nondegenerate confocal elliptical caustic.
Let P_i be a primitive billiard orbit of even least period N, in
traversal order, and R_i its side-contact points on the caustic.
Primitive star winding classes are included. Repetition of an even
primitive orbit preserves the result, but a repeated odd orbit is not
declared centrally symmetric merely because its indexing length is even.

For a focus F, the inner-antipedal side lines and putative vertices are

    L_i(F)={X:(R_i−F)·(X−R_i)=0},
    Q_i(F)=L_i(F) intersection L_(i+1)(F).         (1)

These are perpendicular lines through the **contact points**, not
projections onto the inner sides and not perpendiculars through the
original billiard vertices. Their area, when all vertices exist, is the
source's signed shoelace area

    B_F=(1/2) sum_i det(Q_i(F),Q_(i+1)(F)).       (2)

Define Delta_i(F)=det(R_i−F,R_(i+1)−F). Let U be the orbit locus
where every Delta_i(F+) is nonzero. Let D be the sublocus of U where
B_(F−) is nonzero. These domain conditions cannot be discarded.

### Theorem

The same U is obtained using F−. On U all focal-antipedal vertices
are uniquely finite, and

    B_(F+)=B_(F−).                               (3)

Consequently the arXiv k610 quotient equals 1 on D. Equality of the
rational area expressions holds identically after their intersection
denominators are cleared. The constant 1 supplies their algebraic
quotient continuation, but it does not manufacture finite polygon
vertices or assign a numerical value to a raw 0/0 expression.

Both exclusions occur for admissible **convex primitive four-periodic**
billiards: at a²/b²=2, both finite focal antipedals collapse to points,
and at a²/b²=(1+sqrt(5))/2 a required pair of lines is parallel and
an antipedal vertex does not exist. Exact certificates appear in §4.
Thus even convexity of the original orbit does not make this raw
quotient globally defined. These are domain qualifications, not
counterexamples to rational invariance on its defined locus.

## 2. Credited central symmetry and the finite locus

The published input is Stachel, *The geometry of billiards in ellipses
and their Poncelet grids*, J. Geom. 112, article 40 (2021),
Corollary 4.2(i), pp.22–23, DOI 10.1007/s00022-021-00606-2.
For a primitive even orbit its turning number is odd, so

    P_(i+N/2)=−P_i,  R_(i+N/2)=−R_i.            (4)

The second identity follows from uniqueness of tangency after applying
central inversion to the caustic and the corresponding side line.
The theorem covers the stated primitive stars as well as convex
orbits. Hyperbolic caustics obey different symmetry cases and are not
included here.

Consecutive contacts are distinct. If their billiard side lines
coincided, reflection would be either grazing or normal backtracking.
The outer tangent misses the strict inner caustic. At an outer point
(a cos(theta),b sin(theta)), the normal chord's confocal parameter is
a² sin²(theta)+b² cos²(theta)>=b², so it also cannot be tangent to
the strict elliptical caustic, whose parameter is between 0 and b².
This parameter follows directly from the dual-conic line tangency
criterion. This is the same elementary contact-uniqueness observation
used for the related inner-pedal target.

Each vector R_i−F is nonzero because the focus is strictly inside the
caustic and R_i is on its boundary. Two consecutive lines in (1)
intersect uniquely exactly when Delta_i(F) is nonzero. If it is zero,
the two contacts and F are collinear. Writing them as F+r u and
F+s u with r≠s, their perpendicular lines are respectively
u·(X−F)=r and u·(X−F)=s. Thus they are distinct parallel lines,
not coincident lines with a hidden choice of intersection.

From (4),

    Delta_(i+N/2)(F−)=Delta_i(F+).                (5)

This proves equality of the two finite loci without assuming that
the foci lie inside the contact polygon. They need not.

## 3. Equivariance and signed area

Central inversion exchanges the two focal constructions:

    −L_i(F+)=L_(i+N/2)(F−).

On U, uniqueness of intersection implies

    Q_(i+N/2)(F−)=−Q_i(F+).                      (6)

This preserves traversal up to a cyclic shift. Since det(−X,−Y)
equals det(X,Y), equation (6) in the signed sum (2) proves (3).
No unsigned-region-area argument is being substituted.

The coordinates of Q_i are rational functions obtained from a two-by-two
linear system with denominator Delta_i. Therefore this is also an
identity of rational area expressions on their common domain. The
ratio simplifies to 1 wherever its denominator is nonzero. At a
common zero or a missing intersection, the algebraic constant extension
is a statement about the simplified expression, not an assertion that
the original quotient or polygon exists there.

The source already credits central inversion for neighboring focal
pedal equalities. Related campaign k607 and k609 work checks the same
mechanism on other constructions. We explicitly reuse this established
symmetry idea; it is not a separate discovery for each table row.

## 4. Exact convex four-periodic domain certificates

Scale b=1 and write R=a²>1, c=sqrt(R−1). The axis diamond

    (a,0), (0,1), (−a,0), (0,−1)                (7)

is a primitive convex four-periodic billiard: at each axis vertex the
two incident unit directions are symmetric about the ellipse normal.
All four sides are tangent to the strict confocal ellipse

    x²/alpha²+y²/beta²=1,
    alpha²=R²/(R+1), beta²=1/(R+1),
    lambda=R/(R+1),                             (8)

where 0<lambda<1, alpha²=R−lambda and beta²=1−lambda.
In particular alpha²−beta²=R−1=c². The side x/a+y=1 has contact

    (x,y)=(a³/(R+1),1/(R+1)),                   (9)

by the dual-conic tangency formula. The inner contact polygon is the
rectangle (x,y),(−x,y),(−x,−y),(x,−y), in that order.

### 4.1 Explicit antipedal of a rectangle

For any x,y>0 and F=(c,0), provided c≠x and c≠−x, solving (1)
for this rectangle gives, in order,

    Q_0=(−c,H),       Q_1=(L,0),
    Q_2=(−c,−H),      Q_3=(T,0),

    H=(x²+y²−c²)/y,
    L=−x−y²/(x+c),   T=x+y²/(x−c).             (10)

The signed area is consequently

    B_F=H(T−L)=2x(x²+y²−c²)²/[y(x²−c²)].        (11)

These formulas follow from the four explicit line equations and are
also verified symbolically by `check_exact.py`.

For the genuine billiard contacts (9), the relevant factors simplify to

    x²−c²=(−R²+R+1)/(R+1)²,
    x²+y²−c²=(2−R)/(R+1).                       (12)

### 4.2 Finite collapse at R=2

At R=2, the billiard ellipse has a=sqrt(2), b=1 and c=1.
Its caustic has alpha²=4/3, beta²=1/3. The contacts have
x=2sqrt(2)/3, y=1/3 and x²+y²=1=c², but x≠c.
All four consecutive line determinants are nonzero. In (10), H=0
and L=T=−c, so every F+ antipedal vertex is the single point F−.
The opposite construction similarly collapses to F+.

Both signed areas are exactly zero although all required intersections
are unique and finite. This lies in U but not in D. It is a literal
0/0 case in the source's even-period range, without any singularity in
the original billiard or its caustic.

### 4.3 A missing vertex at the golden-ratio aspect square

Let R=phi=(1+sqrt(5))/2, so R²−R−1=0. Equation (12) gives x=c>0.
The two contacts on the right side of the inner rectangle are
(c,y) and (c,−y). Relative to F+=(c,0), their normal vectors are
(0,y) and (0,−y). Their antipedal lines are y_coordinate=y and
y_coordinate=−y. Since y>0 these lines are distinct and parallel.
Their proposed consecutive vertex is undefined. At F− the opposite
side gives the same failure by central inversion.

The outer four-orbit and the strict caustic (8) are still perfectly
nondegenerate. This example is outside U, so no finite signed
antipedal area is asserted. In particular, it is not interchangeable
with the finite collapsed-polygon example in §4.2.

Both examples vary the ellipse/caustic within the explicit construction.
Neither is presented as variation of a defined ratio along one fixed
Poncelet family.

## 5. Exact conclusion and credit

For the precise inner-antipedal source target, signed areas agree on
the common finite locus, and their quotient equals 1 on its defined
locus. The exact examples show why an unqualified everywhere-finite,
everywhere-nonzero formulation would be false even for convex orbits.
They do not disprove the intended rational invariant.

The proof credits classical central symmetry and the source's
neighboring symmetry arguments, with the shared campaign mechanism
disclosed. The finite checker corroborates exact formulas and domain
certificates; the universal proof is geometric. No novelty guarantee,
hyperbolic-caustic claim, or claim about a different published table row
is made.
