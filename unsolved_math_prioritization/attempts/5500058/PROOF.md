# A checkable stripe-coloring family for target 5500058

Date: 2026-10-11. This is a partial result, not a resolution of Graham's
universal triangle conjecture. Novelty is **not established**: Mundinger,
Zimmer, Kiem, Spiegel, and Pokutta (ICML 2025), Section 4.4 and Figure 4,
announce additional stripe-coloring regions that appear to include this
example. The published version says separate descriptions of the triangle results are
in preparation; that is a historical statement of that version, not a
certification that separate papers remain unpublished on 2026-10-11. The proof below is independently authored and self-contained;
it does not import their numerical search or execute their code.

## Review and distribution status

AI-assisted and unrefereed, with an independent internal AI mathematical audit.
Acceptance is scoped to the stated partial theorem; it is not external human
peer review or formal proof-assistant certification. This is not a computational
reproduction package. The proof is self-contained. Programs, raw expanded cases,
datasets, copied source documents and source-derived images are not distributed.
Source hashes authenticate bytes, not correctness, novelty, or current status.
Editorial preparation performed no new mathematical program runs, scholarly
source-body inspection, or literature survey.

## Full target, retained without a quantifier substitution

For every Euclidean planar triangle T, does there exist a function
c_T: R^2 -> {0,1,2} such that for every Euclidean isometry g (translations,
rotations, and reflections), the three vertices of g(T) do not all have the
same color? The function may depend on T. No continuity, measurability,
periodicity, or finite-domain restriction is imposed by the target.

The following theorem supplies entire-plane colorings only for a stated
family. All points, stripe boundaries, and isometries are included.

## General sufficient criterion

Let T have vertices A=(0,0), B=(1,0), C=(x,y), where y>0 and AB is a longest
side. Put a=|B-C|, b=|A-C|. Suppose h>0 satisfies

1. h <= y;
2. a <= 2h;
3. b <= 5h;
4. h^2 [r^2 + (s-rx)^2/y^2] < 1 for each of
   (r,s) in V={(2,2),(2,3),(3,4),(4,4),(4,3),(3,2)}.

Then the coloring c(X,Y)=floor(Y/h) mod 3 of the **whole plane** has no
monochromatic congruent copy of T.

### Proof

The stripe with index j is R x [jh,(j+1)h). Thus two points in distinct
stripes with the same color have vertical separation strictly greater than
2h. If their stripe indices differ by at least 6, the separation is strictly
greater than 5h. Strictness follows from the half-open upper boundary; it
also holds for negative indices.

Assume a congruent copy A',B',C' is monochromatic. Since |B'-C'|=a<=2h,
B' and C' must lie in the same stripe, say index j. Since |A'-C'|=b<=5h,
the stripe of A' is one of j-3,j,j+3.

The case j is impossible. The least projection width of T is its altitude
over its longest side, namely y. For completeness, any strip of width w
containing a triangle of diameter L and area Delta must satisfy
2 Delta <= L w: take the horizontal cross-section through the vertex of
intermediate vertical coordinate. Its length ell is at most L, and the
two triangles above and below that section have total area at most ell*w/2.
Thus every orientation of our T has vertical width at least 2 Delta/L=y.
Three points in one half-open stripe have vertical span strictly below h,
contradicting h<=y.

Consequently the singleton A' is three stripes above or below B',C'.
Reverse the vertical projection direction if necessary so that B',C' have
larger projected coordinates than A'. There is a unit vector u=(u_1,u_2)
in the coordinates of T such that

  r = u dot (B-A)/h,    s = u dot (C-A)/h

satisfy 2<r<4, 2<s<4, and |r-s|<1. These inequalities use only the
locations in the three half-open strips; translations have canceled.
They apply to reflected copies as well as orientation-preserving ones.

The closure of this feasible (r,s) region is the convex hexagon with vertex
set V above. Solving the two projection equations gives

  u = (hr, h(s-rx)/y).

The image of the closed hexagon under this invertible linear map is the
convex hull of its six image vertices. By condition 4 every one of those
vertices has Euclidean norm strictly below 1. Every point of their convex
hull has norm strictly below 1, by the triangle inequality. This contradicts
|u|=1. All possible stripe placements have been excluded. QED.

## Explicit continuum family with a single fixed coloring

The coloring

  c(X,Y) = floor(400Y/77) mod 3

works simultaneously for all triangles A=(0,0), B=(1,0), C=(x,y) with

  849/1000 <= x <= 851/1000,
  349/1000 <= y <= 351/1000.

This rectangle is a separately specified positive-area family of shapes.
It is not substituted for the universal target.

Set h=77/400. Throughout the rectangle, AB=1 is the longest side because

  a^2 <= 73001/500000 < 5929/40000 = (2h)^2 < 1,
  b^2 <= 423701/500000 < 5929/6400 = (5h)^2 < 1.

Also h<349/1000<=y. For each (r,s) the expression in condition 4 is
maximized over this rectangle at y=349/1000 and one of the two endpoint
values of x. The six resulting upper bounds, in the listed order of V, are

  428672629/2436020000,
  1617437129/2436020000,
  9508390661/9744080000,
  428672629/609005000,
  391319929/609005000,
  4156282361/9744080000.

All are strictly below 1; the largest is 9508390661/9744080000 < 0.976.
These are rational inequalities, independently reproducible by elementary
arithmetic. Therefore the criterion applies uniformly to the rectangle.

### Center point certificate

At C=(17/20,7/20), the six squared norms are respectively

  3509/20000, 13189/20000, 77561/80000,
  3509/5000, 6413/10000, 34001/80000.

The largest is 77561/80000 < 1. This particular triangle is slightly
obtuse: (A-C) dot (B-C) = -1/200. Its shortest side is sqrt(58)/20,
less than half its longest side, and its second-longest side sqrt(338)/20
is greater than twice its smallest altitude 7/20. Hence neither explicit
three-color criterion in Aichholzer--Perz (2019), Theorems 3.1 and 3.2,
covers this point. That is a comparison with those specified theorems,
**not** a novelty claim against 2025 or all earlier literature.

## Genuine negative controls and exact counterexamples to overgeneralization

The stripe construction is not universally valid for arbitrary widths or
triangles. For T={(0,0),(1,0),(1/2,1/10)} and h=1/10, use the orthogonal
projection u=(-3/5,-4/5) and add vertical translation 9/100. The three
heights are 9/100,-51/100,-29/100. Their stripe indices are 0,-6,-3,
all color 0. A perpendicular coordinate completes u to a Euclidean
isometry. This is an exact monochromatic copy, not a floating-point hit.

The same coloring's successful avoidance for a different triangle cannot
imply the original universal theorem. Conversely, failure of a stripe
coloring is not an obstruction to every possible three-coloring.

Historical additional exact controls use the right isosceles
triangle with unit legs: width 2/3 succeeds with three colors, while widths
1 and 1/4 fail, and the width-2/3 two-color version fails. A collinear
three-point control always fits in a horizontal stripe. All failed cases
have explicit rational isometry data and exact stripe-index witnesses.

## Status and remaining gap

No full proof or counterexample to the target was found. This is an
independently checkable partial construction with unresolved prior-work
overlap. It may be used as a reconstruction/audit artifact and a test for
future verifiers. It must not be promoted as a novel discovery or a solved
universal target without separate independent proof and novelty review.

Primary comparison sources:
- https://www.eurocg2019.uu.nl/papers/10.pdf (2019, Theorems 3.1 and 3.2)
- https://proceedings.mlr.press/v267/mundinger25a.html (2025, Section 4.4,
  Figure 4, and the published version's historical statement on separate triangle papers)
- https://arxiv.org/html/2512.15516v1#S1.SS4 (December 2025 status discussion)
