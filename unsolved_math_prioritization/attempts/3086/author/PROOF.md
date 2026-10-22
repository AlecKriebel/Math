# Exact statement and partial results

## 1. Target and quantifiers

For every integer n >= 1 and every real s > n, ask whether the closed square
S = [0,s]^2 can be contained in a union of n^2+1 closed unit squares. Each covering
square may be translated and independently rotated; overlaps and portions lying
outside S are allowed. The conjecture says no such containment is possible.
Allowing at most n^2+1 squares gives the same question because redundant squares
may be added. Equivalently, if S(N) is the supremum of coverable side lengths with
N unit squares, the conjecture is S(n^2+1)=n. The lower bound is the n-by-n tiling.

The primary problem record is
https://www.openproblemgarden.org/op/covering_a_square_with_unit_squares .
It matches the selected dataset statement exactly after identifying its variables.
The requested UnsolvedMath page could not be retrieved in this inspection.

## 2. Area loss: a necessary condition, not a solution

For tiles Q_1,...,Q_N covering S, let m(x) count the tiles containing x. Integration
of tile indicators, with boundary sets of area zero ignored, gives the identity

    N - s^2 = sum_i area(Q_i \ S) + integral_S (m(x)-1) dx.

For N=n^2+1 and s>n, the right side is nonnegative and strictly less than 1.
Thus the sum of outside areas and the multiplicity-weighted overlap loss must be
less than one. This is an exact identity even when outside pieces overlap: outside
areas are summed with multiplicity, not measured as the area of their union.
It excludes s>sqrt(n^2+1), but by itself cannot exclude arbitrarily small s-n.

## 3. Separated grid points and the number of rotated tiles

Put h=s/n>1 and take the (n+1)^2 points (ih,jh), 0<=i,j<=n.

Any three distinct such points contain two at distance greater than sqrt(2).
Indeed, if a coordinate range includes two grid steps, their distance is at least
2h>sqrt(2). Otherwise all three are among four corners of one h-by-h cell, and
two are diagonal corners, at distance h*sqrt(2)>sqrt(2). A unit square, whose
diameter is sqrt(2), therefore contains at most two grid points.

An axis-parallel unit square contains at most one because its x and y ranges each
have length 1<h. If r of N=n^2+1 covering tiles are not axis-parallel, counting
point-tile incidences gives

    (n+1)^2 <= (N-r) + 2r = N+r,

so r>=2n. In particular, an entirely axis-parallel cover needs at least (n+1)^2
tiles and cannot solve the target problem.

A slightly stronger formulation assigns each grid point to one containing tile.
At least 2n tiles must then receive two points. A pair within one tile must be
horizontal or vertical neighbors: all other pairs have distance greater than
sqrt(2). Writing the tile's angle to the nearest coordinate direction as
0<=theta<=pi/4, fitting a segment of length h parallel to an axis requires
h*cos(theta)<=1 and h*sin(theta)<=1. Hence each of these 2n tiles satisfies
theta>=arccos(1/h). This angular condition does not imply a fixed positive loss
as h decreases to 1.

## 4. A self-contained proof for n=1

Suppose two unit squares cover [0,s]^2 with s>1. A tile cannot contain opposite
corners, whose distance is s*sqrt(2)>sqrt(2), and hence cannot contain three
corners. The four corners must be assigned as disjoint adjacent pairs. By symmetry
take the left pair in one tile and the right pair in the other.

For the left tile, reflect about the target's horizontal midline and choose the
tile axes if necessary so its orthonormal coordinate vectors are
u=(c,t), v=(-t,c), with c>=t>0 and c^2+t^2=1. The case t=0 cannot contain the
left pair at separation s>1. In these coordinates the tile is a product of
two intervals of length 1. Containing (0,0) and (0,s) implies that its upper
u-coordinate is at most 1 and its lower v-coordinate is at least sc-1.
Consequently its intersections with the bottom and top target edges have
lengths at most

    a=(1-sc)/t,       b=(1-st)/c,

respectively. The numerators are nonnegative because the two corners are in
the tile. Their sum satisfies

    a+b = (c+t-s)/(ct)
        < (c+t-1)/(ct)
        = 2/(c+t+1) < 1.

The last identity uses (c+t)^2=1+2ct; the last inequality uses c,t>0. By reflection,
the right tile likewise covers less than one unit of the two horizontal target
edges combined. Their union cannot cover those edges, whose total length is
2s>2. This contradiction proves the n=1 case.

## 5. Exact counterexample to a local grid-length estimate

Use the grid defined in Section 2 of Sriswasdi, arXiv:2609.15876v1: all horizontal
and vertical segments at multiples of h=s/n inside [0,s]^2, including its boundary.
The paper's Lemma 2, on PDF page 2 with its argument on page 3, bounds a
single-sided perimeter tile's grid-intersection length by 3*sqrt(2)/2.
Its single-sided classification asks that exactly one target boundary side
intersect the tile; it does not require that the tile miss the next internal
parallel grid line.

Take the exact parameters

    n=4, h=101/100, s=101/25, delta=1/100, r=sqrt(2)/2,
    cx=2h, cy=r-delta.

Let Q have the four vertices

    (cx,-delta), (cx+r,r-delta),
    (cx,2r-delta), (cx-r,r-delta).

Consecutive side vectors have squared length 2r^2=1 and dot product zero, so Q
is a unit square. Its x-coordinates lie strictly between 0 and s, its highest
y-coordinate is 2r-delta<s, and its lowest is -delta<0. Therefore Q intersects
exactly the bottom target boundary, in a segment of positive length 2delta.

Equivalently Q is given by |x-cx|+|y-cy|<=r. It meets just three grid segments
in positive length:

    y=0:    2delta = 1/50,
    y=h:    2(sqrt(2)-delta-h) = 2sqrt(2)-51/25,
    x=2h:   sqrt(2)-delta = sqrt(2)-1/100.

There are no other vertical intersections because r<h, and there are no other
horizontal intersections because sqrt(2)-delta<2h. These inequalities are
strict. Segment crossings are points of length zero, so the lengths add. Thus

    length(Q intersect grid) = 3sqrt(2)-203/100
                             > 3sqrt(2)/2.

For the strict comparison, both 3sqrt(2)/2 and 203/100 are positive, and their
squares are 9/2 and 41209/10000, with 9/2>41209/10000. The violation is therefore
exact, not a rounded numerical effect. The outside cap has area delta^2=1/10000.

The same construction works for every 1<h<211/200 with delta=1/100, n=4,
and cx=2h, since 2h+delta<53/25<3sqrt(2)/2. It therefore persists for arbitrarily
small positive s-4; the example does not exploit a large epsilon.

If the phrase 'given a covering' in the definitions is read literally, append
the 25 axis-parallel unit squares [i,i+1] x [j,j+1], 0<=i,j<=4. Their union
already covers [0,101/25]^2, giving a finite covering containing Q. Lemma 2's
stated local estimate is independent of the total tile count. We do not exhibit
a 17-tile cover containing Q. A replacement lemma restricted to configurations
compatible with such a cover would require a new justification.

The preprint uses Lemma 2 in its Section 5 grid-count inequality (2), which drives
its subsequent tile-count restrictions. The invalid local estimate prevents us
from treating that derivation as a verified proof. The proposed n=4 conclusion
may still be true. No statement about the truth of that conclusion follows from
this counterexample alone.

## 6. A valid coarse grid estimate and its limitation

For completeness, an elementary estimate survives without the incorrect
single-sided refinement. Consider two parallel lines at distance h>1 that both
meet a unit square. Normalize its orientation by c=cos(theta)>=t=sin(theta)>0.
With the square's leftmost x-coordinate set to zero, the vertical chord-length
function is

    f(x)=x/(ct)                  for 0<=x<=t,
         1/c                     for t<=x<=c,
         (c+t-x)/(ct)            for c<=x<=c+t.

If both x and x+h lie in its projection, then x<=c+t-h<t and x+h>c. Therefore

    f(x)+f(x+h)=(c+t-h)/(ct)
               < (c+t-1)/(ct)=2/(c+t+1)<1.

The unrotated case cannot meet two such lines. Any single chord has length at
most sqrt(2), and a unit square can meet at most two members of a parallel grid
family. Its total intersection length with a rectangular grid of spacing h>1
is consequently at most 2sqrt(2). The whole grid has length 2(n+1)s, so a cover
necessarily satisfies 2(n+1)s<=2sqrt(2)(n^2+1).

This coarse bound, the area budget, and the grid-point/rotation counts do not
resolve the conjecture. For every integer n>=2 the purely scalar choices

    s=n+1/(4n), N=n^2+1, r=2n

satisfy all three constraints. The area loss is 1/2-1/(16n^2), strictly between
0 and 1; the incidence count is an equality. For the length estimate, it suffices
to show (n+1)s<(7/5)(n^2+1), since 7/5<sqrt(2). Multiplying the difference by
20n gives

    8n^3-20n^2+23n-5
      = 8k^3+28k^2+39k+25 > 0, where k=n-2>=0.

These are witnesses of feasibility of the necessary-inequality relaxation,
not placements of tiles or covering counterexamples.

## 7. Literature boundary and remaining problem

The 2009 Januszewski article establishes the n=2 and n=3 cases; its introductory
page and the 2026 Dosa-Langi-Tuza paper both explicitly identify those results.
The latter treats S(6)=2 as Conjecture 1.1, rather than a theorem. The September
preprint's contrary description of that assertion is not adopted here.

This work supplies no proof for n>=4. A successful approach must either construct
a true cover with exact whole-region containment, or strengthen the necessary
conditions to rule out all geometric configurations. In particular, neither the
finite certificate above nor the invalid source estimate establishes the
original all-n claim. The source inspection is dated 2026-10-05 and does not
certify that no other, unindexed proof exists.
