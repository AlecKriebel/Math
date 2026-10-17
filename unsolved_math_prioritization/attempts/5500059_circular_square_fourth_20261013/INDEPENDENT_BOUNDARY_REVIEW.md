# Independent audit of the fixed-patch obstruction and exact coarsening

Problem row 1757 / 5500059 / AMR-054-0059. Audit date: 2026-10-13.

## Verdict and precise scope

Accepted, with no mathematical correction required:

1. Preserving the exact original 56-cell boundary patch in any finite convex square partition whose maximum circularity is strictly below sqrt(2) forces at least 6,826 additional pentagons and at least 6,882 cells in total.
2. The newly coarsened exact 56-cell patch has only 588 genuine sides, retains strict circularity below 64439/50000 = 1.28878 and complete square-boundary coverage, and still leaves an open central neighborhood uncovered. Preserving this new patch under the same ceiling forces at least 310 additional pentagons and at least 366 total cells.
3. At a ceiling at most 13/10, the stated exact pentagon identities, including T-junction and four-cell-vertex terms, hold for the respective patches.

These are two different frozen boundary families. The count reduction is a reduction of the proved necessary side budget, not a comparison of their unknown true minimum completion sizes. Neither boundary construction covers the square interior. Neither count is asserted sufficient or attainable. There is no unrestricted lower-bound improvement, obstruction to approaching G with other families, or solution of finite attainment.

## Complete frozen inputs

The audit binds the complete mathematical inputs. This edition only normalizes publication references and lists the displayed public identities:

- [the complete fixed-patch proof](FIXED_PATCH_INTERIOR_OBSTRUCTION.md): 13,958 bytes; SHA-256 `e1f9436039d038bf173718e212d914156ace642fb6d03e54fdf0a60a68165b69`.
- [the complete coarsened-patch proof](COARSENED_BOUNDARY_REPAIR.md): 7,840 bytes; SHA-256 `dc121e309b3409aae3acf711662ed2215042ac3c1d806c3f7b0520aeb0b775b9`.
- [the original boundary certificate](../5500059_circular_square_third_20261013/boundary_patch_certificate.json): 104,072 bytes; SHA-256 `197d3db0d83859d542761d0fb4b57ba9b5c34aec4f35f09169f6d458db42dc2c`.
- [the coarsened boundary certificate](coarsened_boundary_certificate.json): 77,009 bytes; SHA-256 `6e7136b295451a6bd8c49c04440f319dce534c94f91484eac21530e53492393e`.
- The complete accepted [third-pass boundary proof](../5500059_circular_square_third_20261013/UNEQUAL_ANGLE_BOUNDARY_CLOSURE.md), SHA-256 `e4b1cdc34d931d7bb403c677a5a6d63fad5f96d65d632f86cd577528953a7120`, and its complete [independent acceptance](../5500059_circular_square_third_20261013/INDEPENDENT_BOUNDARY_THEORY_REVIEW.md) are unchanged sibling dependencies. Both complete mathematical texts were retained and read.

The current finite-certificate and side-budget conclusions are additionally checked directly; their verification does not require a fresh reproof of the earlier analytic near-G family or its lower constant.

## Free-center polygon side lemma

The proof of R/r >= sec(pi/m) is valid for independent actual incenter and circumcenter.

First, shift every supporting line of an m-gon toward an actual radius-r indisk until tangent. Their intersection is bounded, contains the disk and lies inside the original polygon. After any redundant constraints are removed it is a tangential k-gon, k<=m. Consecutive outer-normal gaps are less than pi, and their half-gaps a_i sum to pi. Its perimeter is 2r times the sum of tan(a_i), at least 2kr tan(pi/k), which is at least 2mr tan(pi/m). Convex perimeter is monotone under inclusion. The monotonicity of x tan(pi/x) follows from sin(y)cos(y)<y.

Second, maximize perimeter among convex polygons with at most m vertices inside an actual radius-R enclosing disk. The compactness argument is legitimate when degenerate configurations are included. A genuine vertex of a nondegenerate maximizer cannot lie inside the disk: the gradient of its two incident edge lengths is nonzero, and a small movement increasing perimeter preserves local strict convexity. A maximizer can therefore be taken cyclic. Concavity of sin on [0,pi], applied to its half-arc gaps, gives perimeter at most 2kR sin(pi/k), at most 2mR sin(pi/m). The last monotonicity follows from sin(y)-y cos(y)>0. Degenerate cases satisfy the same bound by continuity.

Combining the two bounds proves the lemma. In particular, triangles require ratio at least two and quadrilaterals at least sqrt(2). Every added cell under the strict sqrt(2) ceiling consequently has at least five genuine sides.

The finite-polygon reduction is also sound. Separating a chosen full-dimensional convex cell from the interiors of every other cell, and intersecting those half-planes with the square, produces a polygon containing it. Any strict excess would include an interior point of that polygon outside the chosen closed cell. Such a point lies strictly on its side of every separating line and hence outside every other cell, contradicting coverage. Thus the cell equals the finite half-plane intersection.

## Connected planar graph and the exact deficit identity

After splitting sides at every partition vertex and removing unnecessary collinear degree-two points, the boundary graph is connected. A particularly direct justification is to connect interior points of any two cells by a generic polygonal path in the square, avoiding the finite vertex set and crossing edges transversely. The path crosses a chain of cells sharing nontrivial segments. Thus the cell-adjacency graph is connected; because each cell boundary is connected and adjacent boundaries intersect, their union is connected.

No added positive-area cell can meet the outer square boundary. In the interior of every fixed boundary edge the fixed cell fills a one-sided neighborhood. At a noncorner subdivision point, the two incident fixed cells have the same full separator and fill complementary sectors of the square half-plane. At a square corner the fixed corner cell fills the quadrant. These facts follow from the exact full-edge incidence and strict polygon geometry, and hold for both certificates. Hence the boundary graph has exactly B=60 boundary edges, four degree-two corners, and 56 degree-three noncorner boundary vertices.

Write X for the sum of degree(v)-3 over interior graph vertices and C for the number of flat side incidences created by side subdivision. Both are nonnegative. The usual planar Euler formula and degree sum are

V-E+N=1,   2E=3V-4+X.

Therefore E=3N+1-X. If s_i counts genuine sides, then sum s_i+C=2E-B, so

sum (6-s_i)=B-2+2X+C.

This counts T-junctions correctly rather than assuming a face-to-face partition. The original fixed cells have excess side count 7104-6*56=6768; the coarsened ones have excess 588-6*56=252. The added-cell identities are consequently

P5 = 6826 + sum_(k>=7)(k-6)Pk + 2X+C

and

P5 = 310 + sum_(k>=7)(k-6)Pk + 2X+C,

respectively. Hexagons contribute zero, and cells with seven or more sides increase the required pentagon count.

## The sharper identity at ceiling 13/10

If a cell angle is a and its indisk has radius one, the vertex is at distance at least csc(a/2) from the incenter. Any enclosing disk of radius R containing that unit disk and the vertex satisfies R>=1+|O-I| and R>=|O-v|; adding and using the triangle inequality gives 2R>=1+|I-v|. Thus ratio <=13/10 forces sin(a/2)>=5/8 and hence a>72 degrees. The exact comparison sin(36 degrees)^2=(5-sqrt(5))/8<25/64 verifies the strict angle threshold.

Five such angles cannot meet at an interior vertex. Four cells cannot include a flat angle, because 180+3*72 exceeds 360. A degree-three vertex has at most one flat incident cell; when present it contributes exactly one subdivision incidence and is a T-junction. Consequently X=V4 and C=T. This proves both reported precise identities. It also shows why neither arbitrary extra hexagons nor hidden T-junctions can remove the deficit.

At the original patch's 6,876 one-cell inner vertices the fixed angle is in (150,180) degrees, leaving a reflex angle below 210. Exactly two added cells are required at a ceiling <=1.3. The coarsened patch has 360 analogous vertices, with fixed angle in (144,180), leaving a reflex angle below 216; again precisely two added cells are required. At the common 56 two-cell endpoints, the free angle is in (90,135), so precisely one added cell fits at this ceiling. These are necessary local incidence counts, not existence claims.

## Fresh exact certificate checks

A new standard-library rational checker reconstructs all eight types and all 56 similarities for each certificate; no producer verification code is imported. It performs 128,166 strict supporting-half-plane tests on the original canonical polygons and 722 on the coarsened ones. Every canonical edge contains the indicated unit disk; equality is allowed for valid indisk tangencies. Every canonical vertex is strictly inside the proposed enclosing disk. Positive rational similarities and square symmetries transfer these facts to the placed cells. All eight types retain distinct witness centers.

The checker independently derives candidate separating axes from actual outer-to-inner edges, rather than using the producer's pair choices, and computes projections for all 1,540 pairs in each patch. In both cases exactly 1,484 pairs are empty and 56 intersect in a whole shared segment; there are no isolated point contacts or partial-edge contacts. The complete independent pair tables record every result and all exact segment endpoints. Producer pair rows are also verified separately.

Each square side has exactly 15 consecutive actual polygon edges. The original inner boundary has 6,932 edges and the coarsened one 416. Each is a connected degree-two cycle; the independently certified pair intersections rule out crossings. The original vertex split is 6,876 plus 56; the coarsened split is 360 plus 56. At two-cell vertices the positive ray combination u+v is checked to lie in the exterior sector of both fixed cells, ensuring the tested smaller angle is the unfilled sector.

All angle claims are checked with rational sign and squared inequalities. For original one-cell vertices: D<0 and 4D^2>3A. For coarsened ones: D<0 and 10000D^2>6561A; 81/100>cos(36 degrees) follows by squaring 56/25>sqrt(5). For two-cell free sectors: D<0 and 2D^2<A.

The exact covered area is strictly less than square area for both certificates. The square center strictly violates a support inequality for each cell, so a whole central neighborhood is uncovered.

## Coarsening provenance and limits

The two certificates have exactly the same placements, scales, centers and prescribed endpoints. Every original canonical vertex satisfies every new canonical support, with 10,146 inequalities checked. Every one of the 80 new canonical supports is exactly an old edge line with the correct inward side. Thus each new polygon contains its original polygon and is obtained from retained original supports. Full pair verification independently confirms that this expansion introduces no overlap and preserves the entire shared segments.

The bounded support-subset search is treated as discovery evidence. The final certificate proves the construction even without trusting that search. No minimum-support or global-optimality claim is accepted or needed.

## Controls, modes and preservation

Ten hostile boundary controls reject reversed cycles, a false smaller ratio, invalid disk centers, a missing boundary cell, a duplicate placement, zero scale, an out-of-square translation, a duplicated overlapping pair, and a falsely designated square center. A benign cyclic reindexing of every canonical cycle passes.

Both complete checkers and all controls run in normal, -O and -OO modes with byte-identical output. Complete frozen inputs, exact pair tables and independently authored implementation are preserved. The external receipt records actual archive extraction, independent per-file byte-store reconstruction, full hash matching, and all mode replays from both restored trees. No remote writes were made by this audit.
