# Interior completion of the fixed near-critical boundary patch

Problem: row 1757 / 5500059 / AMR0540059. Fourth newly documented mathematical pass in this continuation, 2026-10-13. Earlier lifetime count is unknown. No novelty or unrestricted optimality claim.

## Main result

Let P be the exact 56-polygon boundary patch in [the original boundary certificate](../5500059_circular_square_third_20261013/boundary_patch_certificate.json), SHA-256 `197d3db0d83859d542761d0fb4b57ba9b5c34aec4f35f09169f6d458db42dc2c`. Retain every one of its polygons as an entire cell of a finite convex partition of its square.

**Theorem.** If the completed partition has maximum circumradius/inradius ratio strictly below sqrt(2), it contains at least 6,826 additional interior pentagons, and therefore at least 6,882 cells in total.

Here “pentagon” counts genuine sides after deleting collinear intermediate vertices. Arbitrarily many added hexagons do not reduce the required number of pentagons. Added cells with seven or more sides increase that requirement.

For maximum ratio at most 13/10, a more precise identity holds:

    P5 = 6826 + sum_{k>=7} (k-6) Pk + T + 2 V4.           (1)

Pk counts added cells with exactly k genuine sides. T is the number of interior T-junctions, meaning partition vertices lying in the relative interior of a side of one incident cell. V4 is the number of interior vertices incident to four cells. The four square corners and the 56 other vertices on its sides are excluded from T and V4.

In particular, an extension with exactly 6,882 cells would have only pentagons among its 6,826 added cells, no T-junctions anywhere, and no four-cell vertices. This is a necessary condition, not an existence assertion.

The result applies at the patch ceiling 1.28878, at any smaller feasible ceiling, and at the independently certified complete-square upper bounds below 1.3. It rules out retaining this exact patch inside a modest-size completion or filling its interior using only hexagons plus a few exceptional cells. It does NOT rule out a much larger finite completion, changes to the boundary polygons, or approaching G by a different family.

No whole-square upper bound is improved in this pass. The interior remains unfilled.

## 1. Verified geometric data

The proof uses the independently accepted strict convexity, disjoint interiors, complete square-boundary coverage, and full shared-edge incidence of the third-pass certificate. The complete [boundary-cover proof](../5500059_circular_square_third_20261013/UNEQUAL_ANGLE_BOUNDARY_CLOSURE.md) and [independent review](../5500059_circular_square_third_20261013/INDEPENDENT_BOUNDARY_THEORY_REVIEW.md) remain unchanged sibling dependencies.

The new exact checker reconstructs all rational similarities and verifies the following counts and angles directly:

- 56 fixed cells, with 7,104 genuine sides in total.
- 56 shared edges between fixed cells.
- 60 segments on the square boundary, 15 on each side.
- 6,932 exposed inner edges, forming one simple inner boundary cycle (simplicity uses the independently accepted separation).
- At 6,876 vertices of that inner cycle, exactly one fixed cell occurs. Its angle lies strictly between 150 and 180 degrees, so the unfilled domain has a reflex angle strictly between 180 and 210 degrees.
- At the other 56 vertices, two fixed cells occur. The unfilled-domain angle lies strictly between 90 and 135 degrees.

The counts also satisfy

    7104 = 60 + 2*56 + 6932,
    6932 = 6876 + 56.

The previously accepted patch covers approximately 31.9451% of the square area; the exact count result does not use this decimal.

For the exact angle checks, let u and v be the two nonzero rays at a vertex, D=u dot v, and A=|u|^2 |v|^2. The one-cell test is

    D<0 and 4 D^2 > 3 A,

which gives an angle in (150,180) degrees. The two-cell test is

    D<0 and 2 D^2 < A,

which puts the smaller sector in (90,135) degrees. A positive combination u+v is checked against the incident supporting edges of both fixed polygons to verify that this smaller sector, rather than its complement, is the unfilled sector. All these comparisons use exact rational arithmetic.

## 2. Every sufficiently circular polygon has at least five sides

**Lemma.** A convex polygon with m genuine sides, inradius r and circumradius R, satisfies

    R/r >= sec(pi/m).                                    (2)

The centers defining r and R may differ.

**Proof.** A convex m-gon containing a disk of radius r has perimeter at least 2 m r tan(pi/m). To see this, translate every side support inward until it touches the disk. The resulting polygon Q is contained in the original polygon and has k<=m sides. Perimeter is monotone under inclusion for convex sets, for example by the Cauchy width formula. If the consecutive outward-normal gaps of Q are 2a_i, then 0<a_i<pi/2, sum a_i=pi, and

    perimeter(Q)=2r sum tan(a_i) >= 2 k r tan(pi/k)
                >= 2 m r tan(pi/m).

The first inequality is convexity of tan. The second uses that x tan(pi/x) decreases for x>=3; differentiating reduces this to sin(y) cos(y)<y for 0<y<=pi/3.

A convex polygon with at most m vertices in a disk of radius R has perimeter at most 2 m R sin(pi/m). One elementary extremal proof is to maximize perimeter over all convex polygons with at most m vertices in that compact disk. At a maximizing polygon, a genuine vertex in the disk interior can be moved slightly in the direction of the gradient of the sum of its two incident edge lengths. That gradient is nonzero, and strict convexity is preserved for sufficiently small motion, so the perimeter would increase. Thus every genuine vertex of a maximizer is on the circle. For its k<=m vertices, the positive cyclic arc gaps b_i sum to 2pi. Jensen's inequality for sin on [0,pi] gives

    perimeter=2R sum sin(b_i/2) <= 2 k R sin(pi/k)
             <= 2 m R sin(pi/m).

The last monotonicity follows from sin(y)-y cos(y)>0 for 0<y<pi. Degenerate polygons do not exceed the corresponding bound and can also be included by continuity in this compactness argument.

Combining the two perimeter inequalities proves (2). In particular, a triangle has R/r>=2 and a quadrilateral has R/r>=sqrt(2). Therefore ratio below sqrt(2) forces at least five genuine sides. No common disk center, tangency to all original sides, or neighboring-disk tangency is assumed. ∎

Finite convex partitions can be treated as polygonal even if polygonality is not initially stipulated. For any one cell, intersect the four square half-planes with a separating half-plane against each other cell. The intersection equals that cell: a strict excess would contain a relatively interior open patch outside it, which could be covered by neither another cell's interior nor the finite union of cell boundaries. This is the same finite-separation argument used in the accepted earlier pass. It provides a bounded polygon with finitely many sides for every cell.

## 3. Euler's side-deficit inequality, with T-junctions allowed

Consider the planar graph formed by all cell boundaries, subdividing a straight cell side at every partition vertex on it. This bookkeeping does not assume a face-to-face partition. Let N,V,E be its numbers of cells, graph vertices, and graph edges. The graph is connected, and Euler's formula on the square gives

    V-E+N=1.

The graph is connected because a finite subdivision of the disk into convex cells cannot have an isolated boundary component surrounding a hole in a single cell. Equivalently, adding the disk cells one at a time in the associated finite planar cell decomposition gives this Euler relation. Positive-area convex cells are closed topological disks and shared nontrivial interfaces are segments.

There are exactly B=60 graph edges on the outer square boundary. Indeed every boundary point has a relative neighborhood covered by its incident fixed cells: in the interior of a boundary segment one fixed polygon supplies the half-neighborhood; at a subdivision point the two fixed polygons occupy the complementary half-plane sectors along their shared separator; and at a corner the fixed corner cell supplies the quadrant. No added positive-area cell can meet the square boundary, and none can introduce a new vertex there.

The four square corners have degree two. Every other square-boundary vertex has degree three. Every interior graph vertex has degree at least three after unnecessary collinear degree-two graph points have been removed. An interior bend with only two incident convex cells is impossible because their two angles sum to 2pi and cannot both be at most pi unless the interface is straight.

Put

    X = sum_{interior vertices v} (degree(v)-3) >=0.

The degree sum becomes

    2E = 3V-4+X,
    E = 3N+1-X.                                         (3)

Let s_i be the genuine side count of cell i. Let C be the number of extra side incidences created by subdividing genuine straight sides at graph vertices. Thus C>=0 and the total incidence side count is sum s_i+C. Counting edge sides gives

    sum s_i + C = 2E-B = 6N+2-B-2X,
    sum (6-s_i) = B-2+2X+C.                             (4)

This identity explicitly includes T-junctions. They cannot invalidate or weaken the obstruction.

## 4. Applying the exact side budget

The 56 fixed cells contribute

    sum_fixed (s_i-6) = 7104-6*56 = 6768.

Write M=N-56 for the number of added cells. By Section 2, each added cell has at least five sides. Applying (4) with B=60 yields

    sum_added (6-s_i) = 58+6768+2X+C
                     = 6826+2X+C.                     (5)

If Pk counts added k-gons, then

    P5 - sum_{k>=7}(k-6)Pk = 6826+2X+C.                (6)

Consequently P5>=6826, M>=6826, and N>=6882. Even an arbitrarily large all-hexagon fill cannot satisfy (6). This proves the main theorem below sqrt(2).

## 5. Forced local topology at the near-critical ceiling

For completeness, the finer identity (1) uses a simple angle bound with independent disk centers. Normalize an indisk to radius one. If a convex cell has angle a at a vertex, the two incident supporting lines force the incenter to be at distance at least csc(a/2) from that vertex. Any enclosing disk containing both that unit disk and the vertex has radius at least

    (1+csc(a/2))/2.

Thus ratio at most 13/10 implies sin(a/2)>=5/8, and hence a>72 degrees. The latter follows exactly from

    sin(36 degrees)^2=(5-sqrt(5))/8 < 25/64.

This applies to every genuine angle; a collinear incidence angle is 180 degrees and also exceeds 72 degrees.

At each of the 6,876 one-fixed-cell inner vertices, the unfilled sector is reflex but less than 210 degrees. One added convex cell cannot fill a reflex sector, while three added cells would have total angle greater than 216 degrees. Exactly two added cells therefore meet there, both with genuine vertices. At each of the 56 two-fixed-cell shared endpoints the remaining sector is less than 135 degrees; two added angles would exceed 144 degrees. Exactly one added cell fills that sector. Thus all 6,932 original inner-boundary vertices have exactly three incident cells in any completion at this ceiling.

At any other interior graph vertex there can be at most four cells, because five angles would exceed 360 degrees. At a four-cell vertex no cell can be flat there: a flat angle plus three angles greater than 72 degrees would exceed 360 degrees. A degree-three vertex can have at most one flat angle; when it does, it contributes one to C and is precisely a T-junction. Therefore

    X=V4, C=T.

Substituting into (6) gives identity (1).

## 6. What is still needed for completion

The original 56-polygon patch is not rejected geometrically at its 56 shared top endpoints: every remaining wedge there has angle comfortably above the necessary angle threshold. A local angle contradiction would have been incorrect.

The obstruction is the global side budget. The very fine polygonal approximation that gives the excellent boundary ratio also creates thousands of nearly flat vertices along the inner boundary. Preserving those facets forces thousands of compensating pentagons. Replacing the empty region by a small hexagonal core, or by a similarly small Voronoi mesh with only a few nonhexagons, cannot work with this fixed patch.

A viable completion must therefore do at least one of the following:

1. Construct a genuinely large, pentagon-rich graded interior mesh satisfying (1), with verified disk witnesses and full coverage.
2. Redesign the boundary polygons, reducing their actual side counts while keeping the desired radius ceiling and compatible interfaces.
3. Prove an interior construction for a different near-G boundary family whose side-deficit cost is controlled.

No such construction is supplied here. The count is necessary, not sufficient; it does not establish that 6,882 cells suffice, that a larger completion exists, or that the analytic boundary-cover family is globally extendible.

A small numerical exploration of a restricted symmetric pentagonal collar is retained as private experimental evidence only. It is not a lower bound for arbitrary pentagons or a premise of any theorem above. Numerical nonconvergence is not being used as an impossibility proof.

## Dependency and source context

The new statements concern a frozen authored certificate, with its separate independent third-pass acceptance. The accepted boundary-cover theorem remains valid and explicitly leaves the center uncovered. This result places a finite-complexity requirement on preserving its exact witness; it is not a correction to that theorem.

Background reference: Mirela Damian and Joseph O'Rourke, *Partitioning Regular Polygons into Circular Pieces I: Convex Partitions*, arXiv cs/0304023v2, https://arxiv.org/abs/cs/0304023v2. Problem reference: https://topp.openproblem.net/p59. No source text or dataset contents are reproduced, and no exhaustive priority search is claimed.
