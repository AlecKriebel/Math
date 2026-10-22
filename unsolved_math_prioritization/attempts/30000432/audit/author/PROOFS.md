# Equal-area plane triangulations: exact partial results

## Disposition and conventions

UnsolvedMath 30000432 / OWR-1194-001 concerns Ziegler's Problem 2, printed
page 692 of Oberwolfach Report 12/2006. For a 4-connected plane triangulation
with selected exterior triangle, seek a crossing-free straight-edge drawing
whose bounded faces have a common positive area. There are 2n−5 such faces.
The complete general problem remains unresolved here after five substantive
approaches. No novelty or historical-priority claim is made.

“Drawing” permits collinear nonfacial triples, but requires distinct vertices,
nonzero-area faces, and edges meeting only at their shared endpoints. This is
important: the exact family below necessarily has collinear nonfacial triples.
A prescribed nondegenerate shape of the exterior triangle causes no additional
obstruction: the unique affine map between labeled triangles preserves all area
ratios, incidence, and crossing-freeness. Exterior area is not required to equal
one bounded-face area.

Write [XYZ]=det(Y−X,Z−X), twice oriented area. We normalize exterior vertices
C=(0,0), E=(1,0), A=(0,1), counterclockwise as C,E,A.

## 1. Paired-face geometry: complete cycle-bipyramid classification

Let G_m, m≥4, have cycle V_0,...,V_{m−1} and two nonadjacent apices A,B,
each joined to every cycle vertex. Select A,V_0,V_1 as the exterior face;
put V_0=C,V_1=E. The bounded faces, with positive orientation, are

* (V_i,V_{i+1},B), i=0,...,m−1, cyclic indices;
* (A,V_{i+1},V_i), i=1,...,m−1, with V_m=V_0.

This graph is 4-connected. After deleting at most three vertices, if an apex
survives, all surviving cycle vertices connect through it; a second surviving
apex connects through a surviving cycle vertex. If both apices were deleted,
at most one cycle vertex was deleted, leaving a connected cycle or path.
There is always a surviving cycle vertex because m≥4. Its sphere embedding
has triangular faces as displayed, so it is a 4-connected triangulation.

### Theorem

For this fixed labeled plane graph and fixed exterior coordinates there are
exactly m−2 equal-area drawings. They are rational and parametrized by
positive integers r,s with r+s=m−1.

Put t=2m−1 and set

    B=(2s/t,1/t),     M=(s/t,m/t).

The cycle path E=V_1,V_2,...,V_{m−1},V_m=C follows E to M in r equal
segments, then M to C in s equal segments. Thus, explicitly,

    V_{1+j}=E+(j/r)(M−E),                 0≤j≤r,
    V_{1+r+j}=(1−j/s)M,                  0≤j≤s,

where the final vertex V_m means V_0. Every bounded triangle has doubled
area 1/t. All selected exterior faces are covered by relabeling: the graph's
cycle symmetries and apex exchange act transitively on faces.

### Construction proof

M is strictly inside ACE, because s/t>0, m/t>0, and (s+m)/t=1−r/t<1.
The three coarse triangles CEM, AEM and AMC partition ACE. In CEM, B has
barycentric coordinates (r/m,s/m,1/m) relative to C,E,M: they are positive
and their weighted sum is (2s/t,1/t). Hence B is strictly inside CEM.
Draw its fan to all subdivided boundary vertices. In the other two coarse
triangles draw A's fan to their subdivided bases. These are compatible
triangulations of the three coarse triangles, so no edge crossings, overlaps,
unintended vertex-edge incidences, or zero-area faces occur.

Directly, [CEB]=1/t, [AEM]=−r/t and [AMC]=−s/t when written in those
orders. The positively ordered outer fan faces each have doubled area 1/t
by equal subdivision. The point M=(A+B)/2 lies on each nonbase cycle edge's
supporting line. A and B lie on opposite sides of that line and have equal
perpendicular distances to it; thus each paired B-face also has doubled
area 1/t. The base B-face was already checked. This proves existence for
every m, not merely for enumerated examples.

### Exhaustiveness proof

Suppose an equal-area drawing exists. Its 2m−1 bounded faces partition the
exterior triangle, so their common doubled area is 1/t. The face CEB forces
B_y=1/t. For every nonbase cycle edge UV, the A-face and B-face are on
opposite sides of UV and have equal area. Therefore M=(A+B)/2 lies on its
supporting line. Consecutive noncollinear edges of the path E,...,C must
meet at M. Distinct vertices allow at most one such change of line. There
must be a change: otherwise the whole path, including E and C, lies on their
base line, whereas M_y=(1+1/t)/2=m/t>0. Hence precisely one path vertex
is M, and the path consists of two straight chains E to M to C.

The embedding condition forces both chains to progress monotonically along
the corresponding segments. A reversal would overlap adjacent edges. Let
their edge counts be r,s>0. Equal A-face areas force equal segment lengths
on each chain. Adding the s face areas on AMC gives M_x=s/t; hence
B_x=2s/t. All coordinates are now forced as in the construction. Different
r yield a different labeled midpoint vertex, and different coordinates.
There are m−2 choices. This proves completeness.

The family is the cycle-bipyramid/accordion family. Kleist's established
area-universality theorem already implies equal-area existence for odd m;
the octahedron example is attributed to Ringel in Kleist's related-work
discussion. The present elementary family calculation and classification
are supplied without a claim that they are historically new. No external
area-universality theorem is needed in this proof.

## 2. Continuation and degree: an interior critical point already occurs

For m=4 write D=V_2,F=V_3 and coordinates z=(b,h,d,e,f,g) for B,D,F.
In face order CEB,EDB,DFB,FCB,ADE,AFD,ACF, the doubled-area map is

    h;
    −be+dh+e−h;
    be−bg+dg−dh−ef+fh;
    bg−fh;
    1−d−e;
    −dg+d+ef−f;
    f.

The sum is identically 1. Use the first six coordinates as a square map H.
The two equal-area solutions are

    z_+=(2,1,4,2,1,4)/7,     z_−=(4,1,2,4,1,2)/7.

At their midpoint z_0=(3,1,3,3,1,3)/7 the seven doubled areas are

    (7,8,4,8,7,8,7)/49,

all positive. This is an actual drawing: C,E,D,F bound a convex quadrilateral,
B is strictly inside it, and the remaining A-fan lies outside the ring and
inside ACE. These facts can alternatively be checked by the exact edge
intersection tests in the verifier.

For u=(z_+−z_−)/2, u≠0, one has DH(z_0)u=0. Indeed every area coordinate
is quadratic, so its directional derivative at the midpoint is half the
difference of its values at the endpoints. Those differences vanish.
Exact differentiation gives rank DH(z_0)=5, whereas

    det DH(z_+)=8/49,     det DH(z_−)=−8/49.

Thus the area map is not everywhere locally invertible even within valid
positive-area drawings. The two preimages of the equal vector have opposite
local signs; an attempted globally positive degree based on this orientation
fails already for the octahedron. This does not exclude a more subtle degree
or continuation argument. The missing step is global access to the equal
vector despite interior critical values; generic local rigidity alone does
not give it. The midpoint quadratic identity also appears in Whiteley's
discussion on the original source page and is credited, not newly asserted.

## 3. Harmonic placement: fixed barycentric weights do not balance areas

For the same octahedron, requiring every interior vertex to be the arithmetic
mean of its four neighbors gives

    B=(2/5,1/5), D=(2/5,2/5), F=(1/5,2/5).

Direct substitution verifies each neighbor-mean equation. Uniqueness follows
from the finite maximum principle: the difference of two solutions is
harmonic with zero boundary; a positive maximum propagates along a path to
the boundary, a contradiction, and the same applies to a negative minimum.
Its seven doubled areas are (5,3,1,3,5,3,5)/25, not equal.

Consequently the unmodified equal-neighbor barycentric construction fails.
Variable positive weights might still work, but no rule producing weights
that satisfy all equal-area equations for every triangulation is established.
This example does not refute general weighted barycentric methods.

## 4. Weighted induction: the stronger inductive statement is false

Deleting vertices or amalgamating faces naturally introduces unequal target
areas. A universal prescribed-positive-area induction cannot work: already
the octahedron has a positive unrealizable assignment. The following is an
independent normalized reconstruction of Firsching, Proposition 45, itself
within the earlier Ringel non-area-universality line of work.

Prescribe doubled areas (1,3,1,3,1,1,1)/11 in the face order above. The three
exterior-adjacent faces force h=f=1/11 and d+e=10/11. Let L=10/11 and
c=34/121. The EDB and FCB equations imply

    e(L−b)=c,       bg=c.

The AFD equation, after eliminating d, becomes

    eg−L(e+g)+8/11=0.

Multiply by b(L−b) and substitute the two product relations. The result is

    c²−L²c+(8/11)b(L−b)=0
    = −44/14641 · (242b²−220b+51).

But 242b²−220b+51 = 2(11b−5)²+1 is strictly positive for every real b.
There is no real solution. No division by b or L−b was used; either being
zero also immediately contradicts c≠0. This exact obstruction is credited
prior mathematics, not a new counterexample.

It only refutes arbitrary weighted assignments. It does not refute equal
areas, as Section 1 explicitly demonstrates. A successful induction must
prove realizability of the particular restricted unequal assignments it
creates; no such general invariant is supplied here. Stellation-based
equal-area counterexamples introduce separating triangles and therefore
do not meet the target's 4-connectivity hypothesis.

## 5. Equivariant symmetrization: symmetry can force the wrong ansatz

Reflect the exterior triangle by R(x,y)=(1−x−y,y), exchanging C,E and
fixing A, and reverse the ring labels correspondingly. This is a symmetry
of the plane bipyramid problem. In the complete classification of Section 1
it exchanges r and s. Thus a reflection-equivariant equal-area drawing
requires r=s. For even m, r+s=m−1 is odd, so none exists, despite the
existence of m−2 nonsymmetric drawings. For odd m exactly the middle split
r=s provides such a drawing.

In particular, for the octahedron the symmetry exchanges z_+ and z_−.
Their average is the valid drawing z_0 from Section 2, whose face areas are
unequal. Averaging drawings, or imposing every graph symmetry as an ansatz,
cannot provide a general equal-area existence proof. This does not preclude
an asymmetric variational minimizer. A global argument ensuring zero
area-discrepancy, without imposing symmetry, remains missing.

## Precise remaining gap and evidence levels

The universal equal-area statement for arbitrary 4-connected triangulations
outside the explicitly classified family is not proved or disproved. The
five approaches establish the family theorem and sharply identify failed
stronger statements. They are not five independent proofs of the conjecture.

The finite exact checks supplement the elementary universal arguments; they
do not certify arbitrary graphs, reproduce Firsching's graph enumeration,
or constitute a formal proof-assistant verification. All arithmetic in the
portable verifier is rational. Source status is a bounded literature search,
not a proof that no later solution exists. The authored material was created
with extensive AI assistance and has not undergone human peer review.
