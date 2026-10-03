# Turn 5: quantitative interior margin, and the exact rectangular-cover barrier

Fifth and final substantive author turn. Original problem unresolved 5/5.
This turn extends the row argument to strips, proves a three-point theorem
under a uniform strengthened cross-intersection condition, and isolates why
this route does not prove the source's factor-one statement. All claims below
are proved directly; no novelty or full resolution is claimed.

## 1. A classical maximum-determinant normalization

Assume first that K has nonempty interior, and put D=K-K. Choose u,v in D
maximizing |det(u,v)|, and reverse their order if necessary so the maximum
Delta is positive. Compactness gives a maximizer; interior gives Delta>0.
Use u,v as a linear coordinate basis. Maximality, with one vector held fixed,
gives for every w in D

    |det(w,v)| <= Delta,  |det(u,w)| <= Delta.

Thus, in these coordinates,

    conv{(1,0),(0,1),(-1,0),(0,-1)} <= D <= [-1,1]^2.   (1)

Both the horizontal and vertical maximum chord lengths of K are exactly 1:
a chord difference is a point of D, so the upper bound follows from the square;
the two unit coordinate vectors belong to D and yield attaining chords.
Also the coordinate projection widths of K are exactly 1, since those widths
are the respective support values of D. These claims also hold for L=-K.

This is a standard extremal-determinant/conjugate-diameter normalization,
proved here to avoid an uncredited or unchecked black box. For rational
polygons, bilinearity shows the determinant maximum is attained by a pair of
vertices of D, so the basis and transformed coordinates can be chosen rational.

Let C=[(c_x,c_y),(c_x+1,c_y)] be a longest horizontal chord of L, and let
I=[(i_x,i_y),(i_x,i_y+1)] be a longest vertical chord of L. For 0<lambda<1,
convexity gives the closed rectangle

    R_lambda = lambda C + (1-lambda) I <= L,             (2)

with width lambda and height 1-lambda. Indeed each point on the left is a
convex combination of one point of C and one of I. Its lower-left corner is
(lambda c_x+(1-lambda)i_x, lambda c_y+(1-lambda)i_y).

## 2. Positive-width strips under an intersection margin

Let A and B be finite nonempty sets of translation vectors with

    a-b belongs to lambda D for all a in A, b in B.      (3)

In the normalized coordinates, (1) implies |a_x-b_x|<=lambda. Taking cross
extrema in both directions gives

    span_x A + span_x B <= 2 lambda.                    (4)

Therefore one entire family has x-span at most lambda. If each family has its
y-coordinates covered by at most r closed intervals of length 1-lambda,
then the selected family is covered by at most r translates of R_lambda.
Those are contained in translates of -K, so it is r-pierceable.

This is a genuine positive-width strip theorem, with an explicit width and an
explicit construction. It allows arbitrarily many distinct row heights.
It is stronger in a different direction than turn 2's single-strip theorem:
here several strips are allowed, but the uniform margin (3) is required.

For a fixed full-dimensional K and finite configuration, strict intersection
of the interiors of every cross pair implies (3) for some lambda<1. To justify
this, each difference lies in int(D). The interiors of K-K and
int(K)-int(K) coincide for convex bodies, or directly a difference of two
interior points lies in int(D); conversely a point in int(D) can be written
as a difference of interior points: choose epsilon>0 with d/(1-epsilon)
in D, write d/(1-epsilon)=x-y with x,y in K, choose z in int(K), and use
(1-epsilon)x+epsilon z and (1-epsilon)y+epsilon z. Each of the finitely many differences is contained in a smaller
homothetic copy lambda D, and one maximum lambda<1 suffices. Turn 1 supplies
strict intersections for its hypothetical rational counterexample.
Crucially, it supplies no margin bounded away from 1.

## 3. A uniform three-color theorem at factor 3/4

**Theorem.** Let K be a compact convex body in the plane and let A_1,A_2,A_3
be finite sets of translation vectors. If

    a-b belongs to (3/4)(K-K)

for every a,b from different colors, then one family {K+a:a in A_i} is
pierceable by at most three points.

Proof for full-dimensional K. Empty colors are immediate, so assume all are
nonempty. Use Section 1's normalization. More generally take 0<lambda<=3/4
and suppose all cross differences belong to lambda D. For each pair i!=j,
(4) gives span_x A_i+span_x A_j<=2lambda. Thus at most one color has x-span
strictly greater than lambda. The identical argument in y shows that at most
one color has y-span strictly greater than lambda. Of the three colors, at
least one has both spans at most lambda. It lies in a closed lambda-by-lambda
rectangle. Three vertical translates of R_lambda cover that rectangle because

    3(1-lambda) >= lambda.

Use (2) and translation-space duality to obtain three piercing points. QED.

If K is a nonempty segment, all cross-intersecting translates must lie on one
common supporting line: pick one member in each of two nonempty colors, then
use cross intersections to include all remaining members. On that line they
are equal-length intervals. For any two colors the sum of center spans is at
most twice the interval length, so some color's span is at most that length
and that color has a common point. A point K is still easier. Empty K cannot
satisfy nonempty-color cross intersections, and an empty color is trivial.
Thus the stated compact convex case is covered as well.

The proof only uses translations of the one fixed K. It does not replace K by
lambda K in the conclusion. The hypothesis is stronger than ordinary
cross-intersection, which gives differences in D, with factor 1. No optimality
of 3/4 is claimed. The same rectangular proof gives at most k points when
lambda<=k/(k+1), but for k>=4 the known general four-point theorem makes that
observation unimportant.

## 4. Why the rectangular argument cannot simply set lambda=1

At lambda=1, R_lambda degenerates to a horizontal chord: its height is zero.
Strict cross intersections allow lambda arbitrarily close to 1, so compactness
and the rational reduction do not provide the 3/4 threshold.

There is a concrete barrier to the proposed stronger geometric lemma that
every normalized unit square can be covered by three translates of -K. Let

    K=conv{(1/2,0),(0,1/2),(-1/2,0),(0,-1/2)}.

Its difference body satisfies (1) with the displayed coordinate basis, and
K is the closed L1 ball of radius 1/2. The unit square cannot be covered by
three translates of K.

Here is a direct proof. Four square vertices must be covered, so some one of
three balls contains two vertices. Opposite vertices have L1 distance 2 and
cannot share such a ball. By symmetry take the paired vertices to be the
bottom two. The only radius-1/2 ball containing both has center (1/2,0).
This ball misses every point on either vertical square edge except its bottom
endpoint.

If a second ball contains both top vertices, its center is (1/2,1). The third
ball would then have to contain both entire open vertical edges. It cannot:
for example (0,1/4) and (1,3/4) have L1 distance 3/2>1.

Otherwise the remaining two balls individually contain the top-left and top-
right vertices. A ball containing the top-right vertex cannot contain any
point (0,t) with t<1, since their L1 distance is 2-t>1. Hence the ball containing
the top-left vertex must contain the entire open left edge. Closedness forces
it to contain both left endpoints, fixing its center at (0,1/2). Similarly
the other center must be (1,1/2). None of these three balls contains the top
midpoint (1/2,1). Contradiction.

The checker independently certifies a finite version: the 16 boundary points
with quarter-unit coordinates require four translates of this diamond.
This is a counterexample to the unsupported square-cover lemma, not to
Dol'nikov. In particular, a color containing both (0,0) and (1,1) as centers
cannot have the same square-center set as another color under the original
cross hypothesis, because (1,1) is not in D. The bounding-box relaxation loses
precisely such additional cross-color geometry. The known centrally symmetric
case already establishes the original conclusion for this diamond.

## 5. Disposition after five turns

The work now contains complete special-configuration theorems, an exact finite
instance/counterexample semidecision reduction, and an explicit falsification
of a tempting extension. It does not contain a proof or counterexample for
the original arbitrary-real-translation question.

The exact unresolved step is to exploit the full cross-color difference-body
constraints at factor 1 without imposing the three-row condition, a sufficiently
small strip cover, or a uniform 3/4 margin. The maximum-determinant normalization
and two-coordinate width pigeonhole by themselves are insufficient, as Section
4 proves. This route is blocked at that stronger square-cover lemma; a new
mechanism retaining the discarded cross-color geometry would be needed.

Primary references and known body classes remain as in SOURCE_GATE.md. The
2026-10-03 targeted follow-up searches did not establish novelty for these
restricted theorems, and no novelty claim is made. These are research results
for independent audit, not a solved-status or publication decision.
