# Reducing the boundary patch's interior-completion burden

Problem: row 1757 / 5500059 / AMR0540059. Part of the fourth newly documented mathematical pass, 2026-10-13. No novelty claim.

## Exact constructive result

There is a redesigned family of 56 positive-area convex polygons covering every point of the square boundary, with pairwise disjoint interiors and every circularity strictly below 64439/50000 = 1.28878, whose total number of genuine sides is 588.

The previously accepted 56-cell family had 7,104 genuine sides. The redesigned family keeps the same square, the same cell placements and scales, the same witness indisks and enclosing centers, the same boundary intervals, and the same entire shared segments. Its polygons are obtained by deleting selected supporting half-planes from the originals, so the original polygons are contained in the corresponding redesigned polygons.

The new family still leaves an open neighborhood of the square center uncovered. This is a boundary-only construction and establishes no whole-square upper bound.

The exact certificate is `coarsened_boundary_certificate.json`, 77,009 bytes, SHA-256

    6e7136b295451a6bd8c49c04440f319dce534c94f91484eac21530e53492393e.

Its eight canonical types have respectively

    6, 13, 15, 13, 11, 8, 7, 7

vertices, instead of

    6, 138, 138, 138, 135, 132, 135, 138.

The corner and middle types occur four times each; the other six types occur eight times each. Thus the total is

    4*6 + 8*(13+15+13+11+8+7) + 4*7 = 588.

## 1. Reproducible support-line coarsening

For each original canonical polygon, take the exact rational lines through its successive edges. Mark an edge support mandatory if either endpoint is one of the type's prescribed baseline or shared-segment endpoints. Retaining both incident supports at each prescribed endpoint fixes that endpoint exactly.

Between consecutive mandatory supports, consider forward jumps through the cyclic list of supports. A jump from support i to support j is allowed only when their outward normals have positive determinant, their intersection is finite, and the intersection lies strictly inside the indicated circle of radius gamma=64439/50000. The determinant condition excludes a consecutive normal gap of pi or more. A shortest-path dynamic program selects a sequence of allowable supports from one mandatory support to the next. This is a bounded finite search over the existing rational supports; no new continuous optimization or limiting construction is used.

The algorithm retains a subset of the original supporting half-planes. Their intersection contains the original polygon and hence its unit witness disk. The consecutive retained-line intersections are output as exact rational vertices. The final certificate, rather than the search's correctness, is the construction specification. It is directly checked for boundedness, strict convexity, disk containment and all global incidence requirements.

The discovery algorithm and retained index paths are preserved separately. These are replay/discovery evidence; no claim of globally minimum side count is made. The search was run once and stopped after exact validation of the resulting eight canonical polygons.

## 2. Exact acceptance checks

The copied, previously explicit boundary checker is run against the new certificate as producer-run validation. This is not described as a fresh independent audit. It checks:

- Every canonical polygon is strictly convex, using both consecutive turns and supporting inequalities against every vertex.
- Every polygon contains its displayed unit disk: for a directed edge e and witness center I, the signed distance numerator is positive and its square is at least |e|^2.
- Every vertex lies strictly inside its indicated circle of radius gamma. A disk is convex, so the whole polygon lies in this circle.
- The positive rational similarities and square symmetries give 56 cells lying inside the same square.
- All 1,540 unordered cell pairs have exact separating-axis witnesses.
- Every consecutive pair along a square side has the same two shared-segment endpoints as before and an oppositely oriented full shared edge.
- All four square sides have 15 consecutive boundary intervals with neither gaps nor overlap.
- The square center is outside every polygon, and exact area is strictly less than the square's area.

The independent disk centers are unchanged and need not be extremal. Since each true inradius is at least the witness radius and each true circumradius is strictly less than gamma times that radius, every actual ratio is strictly below gamma. The geometry is proved by these exact inequalities, not by a drawing or a numerical score.

Normal, Python -O and Python -OO replays agree. The exact acceptance output is `COARSENED_BOUNDARY_CHECK.json`. A separate exact topology checker produces `COARSENED_TOPOLOGY_CHECK.json`.

## 3. The remaining interior burden

Apply the side-deficit theorem from [the fixed-patch proof](FIXED_PATCH_INTERIOR_OBSTRUCTION.md) to this redesigned patch. There are still 56 fixed cells and 60 square-boundary segments, but the sum of their genuine sides is now 588. Any finite full-square completion preserving all these redesigned cells, at a circularity ceiling below sqrt(2), therefore requires at least

    588 - 6*56 + 60 - 2 = 310

added pentagons, hence at least 366 total cells.

At a ceiling at most 13/10 the precise identity becomes

    P5 = 310 + sum_{k>=7}(k-6)Pk + T + 2V4.              (1)

The meanings of Pk, T and V4 are the same as in the fixed-original-patch theorem. This reduces the guaranteed pentagon burden from 6,826 to 310. It does not prove that either lower count is attainable, or compare the true minimum number of cells needed by the two different boundary families.

The redesigned inner boundary has 416 edges. At 360 vertices one fixed polygon occurs, and at 56 shared endpoints two fixed polygons occur. The latter endpoints and adjacent supports are unchanged, so their free angles remain strictly between 90 and 135 degrees.

At each of the 360 one-cell vertices, exact rational tests give a polygon angle greater than 144 degrees and less than 180 degrees. Specifically, with D=u dot v and A=|u|^2|v|^2 for the two rays, the checker verifies

    D<0 and 10000 D^2 > 6561 A.

This implies cos(angle)<-81/100. Since 81/100 > (1+sqrt(5))/4 = cos(36 degrees), the angle is greater than 144 degrees. Its free sector is consequently reflex but less than 216 degrees. The earlier angle lemma says that every angle of a cell of ratio at most 13/10 exceeds 72 degrees. Exactly two added cells are therefore required at these 360 vertices, and exactly one at each of the 56 shared endpoints. All original inner-boundary vertices are again forced to be trivalent in a completion.

## 4. Scope of the improvement

This exact repair responds to a concrete obstruction to the original fixed patch: its very fine facets imposed a severe Euler pentagon budget. Coarsening removes most of that artificial budget without sacrificing the certified near-critical ratio or boundary closure.

It does not resolve the central geometric task. A complete interior must still satisfy (1), contain finitely many positive-radius cells with separate valid inradius/circumradius witnesses, and cover the entire remaining domain without overlaps. Recursive inscribed cores or a hexagonal mesh cannot be assumed to achieve that merely because their local shapes look favorable. A pentagon-rich transition arrangement, or another redesign, is still needed.

The fixed-original theorem remains about its own SHA-pinned 7,104-sided witness. The new 588-sided witness is a distinct certificate; its smaller count does not contradict that theorem. Neither certificate improves a known complete-square upper bound by itself.
