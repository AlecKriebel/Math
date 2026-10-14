# Author turn1: Euclidean-to-grid reduction and a verified even witness

**Partial. The odd-rectangle question remains unresolved.** 2026-10-01.

## 1. Exact problem, including unrestricted congruences

The inspected source tile is the3×6 rectangle with a2×2 corner removed. We choose unit cells P={(x,y):0<=x<6,0<=y<3} minus the four cells with x>=4,y<2. The source diagram has row lengths6,4,4 from top to bottom. Rotations and reflections are permitted; each copy is congruent and has area14. No independent dilation is allowed. A common scaling normalizes the unit cell side.

A computational grid model would be incomplete if a positive tiling could use nonlattice translations or non-right-angle rotations. The following elementary reduction closes that issue without assuming edge-to-edge matching.

## 2. Reduction theorem

**Every finite tiling of a rectangle by congruent copies of P can be rigidly moved so that the rectangle has integer side lengths and every tile is an integer translate of one of the eight D4 orientations of P.** Reflections are included.

First align the target rectangle with the coordinate axes. Form the graph whose vertices are tiles and whose edges join tiles sharing a boundary segment of positive length. This graph is connected. To see this, connect points in the interiors of any two tiles by a polygonal path inside the rectangle chosen to avoid the finitely many vertices and junctions of the tile-edge arrangement and to cross edges transversely. Each crossing passes through the interior of a shared straight boundary segment and hence traverses an edge of this graph. There is a tile sharing a positive-length segment with an outer rectangle side. Its two edge directions are parallel to the rectangle axes. Sharing a boundary segment forces the orthogonal edge-direction frames of adjacent tiles to agree up to a quarter-turn. Connectedness propagates this conclusion to every tile. Thus every tile has a D4 orientation relative to the rectangle.

Now put the lower-left rectangle corner at(0,0). Choose a horizontal line through the rectangle that contains no tile vertex. The intersections with tile interiors form finitely many open intervals that partition the line segment except for endpoints. Every such interval has integer length: in its tile's coordinate frame the boundary x-coordinates differ by integers, since that tile is an axis-aligned translate of P. Starting at the left rectangle boundary x=0 and adding those integer lengths shows that every crossing x-coordinate is an integer and that the rectangle width is an integer. Every positive-length vertical tile edge meets some such generic horizontal line, so its x-coordinate is an integer. Applying the same argument to generic vertical lines proves integrality of all horizontal-edge y-coordinates and of the rectangle height. Hence all tile vertices, and therefore their cell translations, lie in Z².

This proof allows T-junctions and partial-edge contacts. It uses finiteness and interior-disjoint congruent tiles covering a rectangle, not an a priori lattice convention. The tile is connected and all its boundary edges are axis-parallel with integer coordinates before congruence. No signed weights, overlaps or holes in the target are allowed.

As a consequence, the original existence question is exactly the discrete problem: find positive integers W,H and disjoint D4-translates of P covering {0,...,W-1}×{0,...,H-1}, with WH/14 odd.

## 3. Independent check of the credited even example

Reid's exact target page displays a66×84 tiling. The bitmap was visually inspected and then transcribed into cell-boundary data: its grid step is10 pixels. Flood fill across absent interior boundaries produces396 components, each containing exactly14 cells. Every component is checked against the complete D4 orbit of P. The resulting mathematical coordinate certificate is in known_even_witness.json, with source URL, source-image hash and explicit attribution.

The standalone verifier uses only that coordinate certificate and the exact tile model. It confirms all tiles lie inside an84×66 rectangle, every cell is covered exactly once, and every placement is an allowed congruent orientation. This establishes the displayed even example independently of the source's verbal claim. It does not reproduce the source's minimality search and does not assert that396 is a freshly proved minimum.

The similarly named14omino01 has a different T-shaped diagram and a known odd tiling. Neither its certificate nor the theorem about it can be substituted for this tile. The original question is a rectangular tiling question, not a self-replicating rep-tile problem.

## Remaining route

The grid reduction makes exact finite algorithms applicable to every allowed congruent tiling. The even certificate supplies a useful positive control. Neither establishes an odd tiling or excludes all odd rectangles. The next attempt will examine additive coloring restrictions on odd target dimensions, followed by exact search or boundary constructions within the resulting domain.

Substantive author turns:1/5. Estimated completion15%. No novelty claim; the even tiling is credited to Reid.
