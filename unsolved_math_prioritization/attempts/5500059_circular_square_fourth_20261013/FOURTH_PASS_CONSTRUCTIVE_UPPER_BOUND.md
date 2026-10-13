# A rational 121-piece square partition with circularity below 1.295516

Problem row 1757 / AMR-054-0059 / 5500059, Most Circular Partition of a Square.
Date: 2026-10-13. Fourth newly documented substantive construction pass in this continuation; the earlier lifetime attempt count is unknown.

## Theorem and scope

There is a complete partition of the square into 121 positive-area closed strictly convex polygons such that each cell's smallest enclosing-circle radius divided by its largest inscribed-disk radius is strictly less than

    U = 1295516/1000000 = 1.295516.

In particular, the unrestricted infimum over finite convex partitions is at most 1.295516. This improves the separately accepted third-pass 121-cell explicit upper bound 1.295864 by 0.000348. It also improves the earlier accepted 100-cell bound 1.296046 and 92-cell bound 1.298322. These comparisons concern explicit upper bounds. They imply no optimality, literature priority, lower-bound improvement, or finite-attainment theorem.

The previously accepted lower constant remains G approximately 1.2886844618704579. The gap between that decimal and this upper bound is approximately 0.00683153813. The unrestricted optimum and finite attainment remain open in this work. The separate near-G boundary cover does not cover the square's interior and is not used in this theorem.

## Complete frozen specification

The complete `rational_partition_certificate.json` has 49,342 bytes and SHA-256

    8f313a6c8e8c4094ac10d954abd1b908e444464e92d4b02e6faaf7e6a2ee5bb9.

It supplies the square [-1,1]^2, common coordinate denominator D=10^12, all 240 integer vertex pairs V_j, all 121 counterclockwise face cycles, and one disk-witness record per face. The record for face i gives integer center A_i, integer enclosing center B_i, and positive radius numerator q_i. The contained witness disk has center A_i/D and radius rho_i=q_i/D. The enclosing witness disk has center B_i/D and radius U rho_i.

These centers are independent; they happen to coincide for the central cell and differ in the other 120 cells. No assumption of concentricity, extremality, tangency to all sides, or tangency between neighboring indisks is made. The final certificate alone defines the complete partition and suffices for geometric verification. No numerical optimizer, historical mesh, or image is a proof premise.

There are 60 pentagons, 48 hexagons, eight heptagons, four octagons, and one central 20-gon. There are 696 total face-vertex incidences, 336 interior edges, and 24 boundary edges. Thus there are 360 edges and Euler characteristic 240-360+121=1.

## Authored topology changes

The starting accepted [third-edition 121-cell certificate](../5500059_circular_square_third_20261013/rational_partition_certificate.json) is 49,594 bytes with SHA-256

    b6642d19ad90e5e9325ecf629b5e48d2226b9598271e2120623556351dbd3ebe.

Keep its vertex labels and face labels. Apply two fourfold edge-flip stages, with all operations listed in `topology_operations.json`. An operation has an old edge (u,v), losing faces (a,b), and gaining faces (c,d), where a traverses u,v; b traverses v,u; c is the third face at u; and d is the third face at v. In face a, remove v. In face b, remove u. In face c, insert v immediately before u. In face d, insert u immediately before v. All other cyclic order is preserved. These instructions describe a change in adjacency; the endpoint coordinates are subsequently optimized and are not frozen to the old edge.

First stage, written as (old edge; losing faces; gaining faces):

- (185,187; 15,16; 29,17)
- (189,191; 18,19; 30,20)
- (193,195; 70,71; 67,69)
- (197,199; 74,72; 68,73)

Second stage:

- (58,201; 97,101; 29,120)
- (59,207; 115,119; 30,120)
- (124,203; 103,107; 67,120)
- (125,205; 109,113; 68,120)

The two stages preserve the number of vertices, faces, and edges. They alter the near-corner cells and central-ring contacts. The central cell acquires four sides. A supplied producer topology replay checks that these eight explicit operations recover every final face cycle exactly from the complete accepted input. This provenance replay is additional evidence; the geometric proof below does not infer coverage from adjacency or Euler characteristic.

## Exact geometric proof

All acceptance comparisons are arbitrary-precision integer comparisons without floating-point tolerances. For integer vectors define det(x,y)=x_x y_y-x_y y_x and write ||x||^2=x_x^2+x_y^2.

### Strict convexity and containment

Every coordinate component lies in [-D,D]. Every face cycle has distinct indices. For every directed edge V to W of a face, and every other vertex Z of the same face, the checker verifies

    det(W-V,Z-V) > 0.

All 2,884 comparisons pass. The minimum positive determinant is

    160383401566530772.

The all-vertex supporting-half-plane test proves that each given cycle bounds a positive-area strictly convex polygon, and excludes self-crossing cycles. All polygons lie in the square because their vertices do and the square is convex.

### Pairwise disjoint interiors

For every one of the 121*120/2 = 7,260 unordered pairs, a directed edge V to W of one polygon satisfies

    det(W-V,Z-V) <= 0

for every vertex Z of the other polygon. The supporting polygon's interior is strictly in the positive half-plane, while the other polygon is wholly in the nonpositive half-plane. Hence their interiors are disjoint. The complete `pair_separation_witnesses.json` records one supporting edge for every pair. The reusable checker additionally computes exact rational intersections by polygon clipping; this is a producer-run replay of earlier independently authored code, not a new independent review.

### Full closed coverage of the square

The exact sum of doubled shoelace areas is

    sum_i sum_(j cyclic in face i) det(V_j,V_(j+1))
      = 8000000000000000000000000 = 8 D^2.

Thus the actual polygon areas sum to four. Polygon boundaries have area zero, and pairwise interiors are disjoint, so their union also has area four. Every polygon lies in the square. The union is a finite union of closed sets and is closed. If a point of the square were omitted, its relatively open complement would contain a neighborhood of positive planar area, including if the point lies on a square edge or corner. This contradicts equality of areas. Therefore the polygons cover every point of the square, including its entire interior and boundary.

As redundant checks, the 336 interior edges pair with opposite orientations, and the 24 remaining edges lie on the square boundary. They corroborate the geometric proof but do not replace pairwise separation or the closed-coverage argument.

### Contained witness disks

For a face i, edge V to W, and E=W-V, put T=det(E,A_i-V). Every edge satisfies

    T > 0,
    T^2 - q_i^2 ||E||^2 > 0.

Thus the center A_i/D is strictly in every inward supporting half-plane, and its distance to every boundary line is greater than rho_i=q_i/D. Its closed disk of radius rho_i is contained in the intersection of those half-planes, hence in the convex polygon. The true inradius r_i is at least rho_i>0.

All 696 edge inequalities pass. The smallest radius numerator is 29350614583. The minimum strict squared-distance slack is

    11903868602776199771750141753138239.

### Enclosing witness disks and strict ratio

With g=1295516 and h=1000000, every vertex V of face i satisfies

    g^2 q_i^2 - h^2 ||V-B_i||^2 > 0.

All 696 inequalities pass. The minimum strict integer slack is

    823068242597106816174189584.

Therefore the finite maximum of the vertex distances from B_i/D is strictly less than U rho_i. A closed disk of that smaller maximum radius contains all vertices and, by convexity, the entire polygon. The true enclosing radius R_i is no greater than that maximum, so R_i<U rho_i. Consequently

    R_i/r_i <= R_i/rho_i < U = 1.295516

for every face. This proves the theorem.

## Discovery, failed direction, and audit status

The bounded numerical search tried ten single edge-orbit flips, nine second-round flips from the best first-round topology, seven third-round flips from the best second-round topology, and a corner-side cascade. The third neighborhood did not improve the selected second-round topology. The corner-side cascade gave a worse numerical objective, approximately 1.3137544820. These outcomes are observations from local solves; they are neither impossibility theorems nor global optimality certificates.

A zero-turn-margin second-round solve had numerical objective approximately 1.295515626145, but rounding exposed collinear central facets. Its exact strict-convexity check failed, so that attempt was rejected. A final solve on the selected topology imposed normalized local turn margins of 10^-6. Its objective was approximately 1.295515626807. The selected coordinates and centers were rounded consistently to denominator 10^12; each radius was floored and then reduced by 100 integer units. The numerical maximum witness ratio of this rounded certificate is approximately 1.295515631253, provided only for orientation. The exact strict inequalities above, not these decimals, establish the theorem.

Complete discovery records, numerical checkpoints and the rejected exact attempt are retained separately. They are not premises of the theorem. The final public certificate is the strict accepted one identified above.

The reusable checker and its negative and benign controls are replayed in normal, -O, and -OO modes. This is producer regression checking using earlier independently authored code. It does not constitute a fresh independent worker audit. Any separate reviewer must bind the final certificate and this proof explicitly. The recovery receipt records actual archive extraction, separate byte-store reconstruction, complete file-hash comparisons, and exact replays against both restored trees.

## Source context and remaining limits

The accepted predecessor construction descends from the source context documented in earlier passes: Mirela Damian and Joseph O'Rourke, *Partitioning Regular Polygons into Circular Pieces I: Convex Partitions*, arXiv:cs/0304023v2, Figure 16 and Section 5.2.

https://arxiv.org/abs/cs/0304023v2

https://arxiv.org/html/cs/0304023v2#S5.SS2

TOPP Problem 59: https://topp.openproblem.net/p59.

This report relies on the previously preserved source audit for that attribution and makes no new source-retrieval or exhaustive priority-search claim. No third-party source text is reproduced. The final rational coordinates and proof are self-contained. The lower-bound theory and near-G boundary-transition theory remain separate from this finite complete-square upper witness.
