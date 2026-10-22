# Independent acceptance of the fourth-pass complete square construction

Problem row 1757 / 5500059 / AMR-054-0059. Audit date: 2026-10-13.

## Verdict and frozen objects

Accepted: the supplied 121 closed positive-area polygons form a complete partition of the square, with every genuine angle strictly below pi, and each true circumradius divided by its true inradius strictly below 1295516/1000000 = 1.295516.

This acceptance binds the complete mathematical proof and final certificate. Only publication references are normalized in this edition. The displayed [complete proof](FOURTH_PASS_CONSTRUCTIVE_UPPER_BOUND.md) is 10,705 bytes, SHA-256 `c4d4c05edb06088de0bb2eb3447bdf5818f841594959c5c5343f46a89b17d2ef`; the [complete final certificate](rational_partition_certificate.json) is 49,342 bytes, SHA-256 `8f313a6c8e8c4094ac10d954abd1b908e444464e92d4b02e6faaf7e6a2ee5bb9`.

The result improves the prior explicit 1.295864 bound by 0.000348. It does not establish the unrestricted optimum, attainment of the infimum, a new lower bound, or literature priority. The separate boundary-only constructions are not used to prove this whole-square result.

## Independent implementation and exact geometry

The audit checker was written afresh without importing or copying producer or predecessor checking code. It uses only Python's standard library and arbitrary-precision integers for this construction. The proof and certificate were read in full. Complete prior input, the eight topology operations, and the producer's pair and face-margin tables are retained alongside the independent implementation.

For each directed edge of each supplied face, the checker tests every other vertex against its strict inward supporting half-plane. All 2,884 tests are positive, with minimum determinant 160383401566530772. This proves the supplied order is a simple convex polygonal boundary with genuine, noncollinear vertices. Every coordinate lies in the square. There are 60 pentagons, 48 hexagons, eight heptagons, four octagons and a central 20-gon.

For every one of 7,260 unordered pairs, the independent checker searches both polygons' actual directed edges and finds an exact separating support. It does not use producer pair rows to select those supports. The support-line intersections are also computed exactly: 6,916 pairs are empty, eight meet only at one point, and 336 meet in a segment. The complete pair data record the selected edge and exact intersection endpoints. Thus every pair has disjoint interiors; shared boundaries are permitted.

The sum of doubled integer shoelace areas is exactly 8000000000000000000000000 = 8 times 10^24. With coordinate denominator 10^12 this is square area four. Disjoint interiors and zero-area polygonal boundaries make the union's area equal to four. Since all polygons lie in the square and their finite union is closed, a missing point would have a relatively open omitted neighborhood of positive planar area, even at a square corner or edge. Therefore every point of the square is covered. Coverage is not inferred merely from Euler counts or a drawing.

As redundant checks, all 336 internal edges occur twice with opposite orientations, and the 24 remaining edges form four exact consecutive interval covers of the square sides. The certificate has 240 vertices and 360 edges, giving Euler value 240-360+121=1.

## Disk witnesses and strictness

For each face, the checker independently verifies all signs before squaring the signed distances to its supporting lines. All 696 contained-disk edge tests are strict, with minimum integer slack

11903868602776199771750141753138239.

All 696 enclosing-disk vertex tests are strict, with minimum integer slack

823068242597106816174189584.

Every radius numerator is positive; the smallest is 29350614583. The contained disk therefore bounds the actual inradius from below. The finite maximum distance of the vertices from the enclosing witness center is strictly smaller than 1.295516 times the contained radius. Convexity extends that vertex bound to the whole polygon. This proves the strict ratio bound for the actual extremal radii without requiring either witness to be extremal.

The two centers coincide only for central face 120; they differ for all other 120 faces. No common-center hypothesis or neighboring-disk tangency is used.

## Eight explicit edge flips

The starting accepted 121-cell certificate is retained completely: 49,594 bytes, SHA-256 `b6642d19ad90e5e9325ecf629b5e48d2226b9598271e2120623556351dbd3ebe`.

The independent topology replay checks each old directed edge, both losing faces, the unique third face at each endpoint, and the absence of duplicate inserted endpoints. It then applies all eight specified deletions and insertions. Every final face cycle agrees exactly with the final certificate, including its chosen cyclic start. The central cell changes from 16 to 20 sides. Vertex, edge and face totals are preserved. This checks construction provenance but is not a substitute for the geometric proof.

Every producer separation row was separately checked, including complete pair coverage and edge membership, and all 121 producer face-margin rows were recomputed exactly. They agree. The earlier collinear candidate, retained separately as discovery evidence, independently fails strict convexity. The accepted certificate is the later strict one, not that rejected candidate.

## Controls, modes and recovery

Twelve hostile controls are rejected: reversed face, repeated vertex, out-of-square coordinate, duplicated overlapping polygon, removed face/area gap, zero radius, oversized indisk, invalid incenter, invalid enclosing center, false smaller ratio, an exactly collinear inserted genuine vertex, and incorrect flip gaining faces. Two benign representations pass: cyclic reindexing of every face and exact doubling of all coordinate/radius numerators and the denominator.

The complete exact computation and controls are replayed under normal Python, -O and -OO, with byte-identical output required. No acceptance check is implemented with an optimizable Python assert. The independent pair-intersection table and all complete mathematical inputs are retained. The preservation receipt records actual extraction from the compact archive, separate per-file byte-store reconstruction, complete hash comparisons, and all checker/mode replays from both restored trees.

No remote repository action was taken by this audit.
