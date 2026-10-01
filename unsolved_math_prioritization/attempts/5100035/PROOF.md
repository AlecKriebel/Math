# The focal-antipedal area identity and its quotient domain

**5100035 / AMR-050-0035, arXiv k607. Author turn 1. Full candidate awaiting independent review.** No novelty or priority claim.

## 1. Exact target, edition and conventions

The imported target is Table 7, p.9 of Reznik–Garcia–Koiller,
*Eighty New Invariants in the Elliptic Billiard*, arXiv:2004.12497v11,
29 October 2020. Its k607 is the ratio of the two focal **antipedal areas
of the original orbit**, with asserted value 1 for N divisible by 4.
The published *Fifty New Invariants*, Arnold Math. J. 7 (2021), Table 7,
p.349, does not contain this row. Its k607 is instead a relation between
original and outer **pedal** area ratios. Those are different targets.

Let E be x²/a²+y²/b²=1, a>b>0, with foci F+=(c,0), F−=(−c,0),
c²=a²−b². Fix a strictly nested, nondegenerate confocal elliptical
caustic. Let P_0,...,P_(N−1) be a primitive periodic billiard orbit,
in traversal order. Primitive means least period N; allowed star winding
classes are included. This proof does not infer least-period symmetry
from an artificially repeated odd orbit whose indexing length is even.

For a focus F define the antipedal side line

    L_i(F)={X:(P_i−F)·(X−P_i)=0},
    Q_i(F)=L_i(F) intersection L_(i+1)(F).          (1)

Thus the lines pass through the original vertices and are perpendicular
to their focal rays. This is the antipedal construction in source §3.5;
it is not orthogonal projection onto a billiard chord or a tangent side.
Indices are cyclic. As specified by source equation (1), area means
signed traversal area, even when the derived polygon self-intersects:

    B_F=(1/2) sum_i det(Q_i(F),Q_(i+1)(F)).        (2)

### Theorem

For every even primitive period N in this ensemble, all vertices in (1)
are finite and

    B_(F+)=B_(F−).                                (3)

Consequently the arXiv k607 ratio is identically 1 on its defined locus
for N divisible by 4. The cross-multiplied identity (3) holds on the
whole family, including zero-area orbits. The ratio has the constant
extension 1 across common zeros, but its literal expression is 0/0
there. Such zeros genuinely occur at admissible primitive convex
8-periodic orbits, as certified in §4. Therefore no universal
nonvanishing assertion is appended to the invariant.

This resolves the usual rational-invariant assertion, with its domain
made explicit. The zero example is a domain qualification, not a
counterexample to constancy wherever the quotient is defined.

## 2. Finite intersections and the credited symmetry input

The two normal vectors in (1) are linearly dependent exactly when
F,P_i,P_(i+1) are collinear. But their chord line is tangent to the
strict elliptical caustic, while both foci are strictly inside that
caustic. A tangent line cannot contain an interior point. Thus the
normal determinant is nonzero, and every consecutive antipedal
intersection exists uniquely in the real affine plane. This argument
does not assume the antipedal polygon is simple or convex.

We use the established central-symmetry theorem, not a new integrability
claim: Stachel, *The geometry of billiards in ellipses and their
Poncelet grids*, J. Geom. 112, article 40 (2021), Corollary 4.2(i),
pp.22–23, DOI 10.1007/s00022-021-00606-2. For an even period and odd
turning number it gives, with the source's corresponding indices,

    P_(i+N/2)=−P_i.                               (4)

For a primitive orbit, the period and turning number are coprime, so
even N forces odd turning number. The same source explains the
nonprimitive splitting immediately before the corollary. Thus (4)
includes every primitive even star winding class under the stated
elliptical-caustic hypotheses. It need not apply to hyperbolic caustics,
which are outside this source target.

The source authors already use central inversion for the neighboring
focal-pedal equality rows. We credit that elementary symmetry mechanism;
the present check is its application to the exact antipedal construction
and the quotient's domain. No separate major-discovery claim is made.

## 3. Equivariance proves equality of signed areas

Let J(X)=−X, which exchanges the foci. Substitution in the line equation
shows

    J(L_i(F+))=L_(i+N/2)(F−).

Indeed both factors of the scalar product change sign. Since the
intersections are unique, it follows that

    Q_(i+N/2)(F−)=−Q_i(F+).                       (5)

The index change is a cyclic shift, not traversal reversal. Moreover
det(−X,−Y)=det(X,Y): central inversion in two dimensions preserves
oriented area. Apply (5) in (2) and relabel the cyclic sum to obtain
(3). This proves the theorem's equality and defined-locus ratio claims.

Any repetition of an even primitive orbit multiplies both signed areas
by the same repetition number and retains equality. Merely saying an
indexing length is divisible by four, without checking its underlying
primitive orbit, is not used in this argument.

## 4. An exact zero-area orbit in the claimed parity

This section checks the denominator instead of assuming it is positive
because the original billiard orbit is convex.

Let t be the unique root in (3/10,1/3) of

    f(t)=t⁴−6t³−2t²−2t+1.                        (6)

Existence follows from f(3/10)=661/10000>0 and f(1/3)=−8/81<0.
Uniqueness on (0,1/3) follows from
f'(t)=4t³−18t²−4t−2<0. Put

    C=(1−t²)/(1+t²),  S=2t/(1+t²),
    b=1,  a²=R=C(1−S)/(S(1−C))
             =(1−t)³(1+t)/(4t³),
    c=sqrt(a²−1).                                (7)

We have 0<S<C<1, C²+S²=1 and R>1. In particular a>1 and c is a
positive real number. Consider the ordered eight vertices

    (a,0), (aC,S), (0,1), (−aC,S),
    (−a,0), (−aC,−S), (0,−1), (aC,−S).           (8)

They are distinct and appear in counterclockwise order on E. The
polygon is convex and has least period eight.

### 4.1 Reflection law and strict elliptic caustic

Write d_1=|(aC,S)−(a,0)| and d_2=|(0,1)−(aC,S)|.
Equation (7) implies

    d_1/d_2=(1−C)/(1−S).                          (9)

This follows by squaring, using the explicit positive lengths, and
substituting R. Let v_in=((aC,S)−(a,0))/d_1 and
v_out=((0,1)−(aC,S))/d_2. Then (9) gives

 v_in−v_out=(C+S−1)/d_1 · (a(1−C)/(1−S),1).

The vector on the right is parallel to the outward ellipse normal
(C/a,S), because R=C(1−S)/(S(1−C)). Its multiplier is positive.
As v_in and v_out are unit vectors, this is exactly the specular
reflection law. Axis vertices obey the law by reflection symmetry;
the remaining off-axis vertices follow by the same symmetries.

For completeness the chord from (a,0) to (aC,S) is tangent to the
confocal conic

    x²/(a²−lambda)+y²/(1−lambda)=1,
    lambda=a²(1−C)²/[S²+a²(1−C)²].              (10)

The adjacent chord has the identical lambda by (7). Reflecting the
two chord types gives all eight sides. Formula (10) follows directly
from the dual-conic tangency criterion. It has 0<lambda<1, so the
caustic is a strictly nested nondegenerate ellipse and its foci are
the required ±c. This independently verifies the source admissibility.

### 4.2 Signed antipedal area

For F+=(c,0), write P_i=(x_i,y_i), set

    n_i=x_i−c,  h_i=n_i x_i+y_i²,
    Delta_i=n_i y_(i+1)−y_i n_(i+1).

Solving the two line equations in (1) gives the fully explicit formula

 Q_i=( (h_i y_(i+1)−y_i h_(i+1))/Delta_i,
       (n_i h_(i+1)−h_i n_(i+1))/Delta_i ).        (11)

Every Delta_i is nonzero by the already verified strict caustic.
Substitute the eight vertices (8) into (11) and then into (2).
Using c²=a²−1, C²+S²=1 and (7), ordinary rational simplification gives

    B_(F+)/a =
      (t²−2t−1)(t⁴−6t³−2t²−2t+1)/(4t³).        (12)

Equation (11) and the specified substitutions provide a reproducible
finite algebraic identity; `check_exact.py` independently forms all
eight intersections and certifies the reduced rational identity (12).
It also verifies the chord/caustic and reflection relations without
using floating-point roots. There are no divisions by f(t).

At the algebraic t in (6), (12) is exactly zero. The opposite focal
area is also zero by (3). All vertices and antipedal intersections
remain finite. Thus the source parity N=8 itself admits a literal 0/0
quotient. This example changes the ellipse and caustic as t varies;
it is not an argument that the quotient varies within any one family.

## 5. Result and exclusions

The strongest uniform statement is equality of the two signed areas,
with quotient 1 wherever it is defined and a constant removable
extension at common zeros. It includes the arXiv k607 parity and all
primitive stars with strict elliptical caustics. No claim is made that
the raw quotient is a real number at every orbit, that the ratio of
unsigned region areas is the source invariant, or that published k607
is the same assertion. The neighboring outer-focal-pedal product in
campaign PR210 is neither assumed nor needed.

The proof uses credited classical central symmetry and elementary
Euclidean equivariance. Finite exact checks support the algebraic
certificate; they do not replace the published symmetry theorem or
the universal argument.
