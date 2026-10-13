# A rational 121-piece square partition with circularity below 1.295864

Problem: row 1757 / AMR-054-0059 / 5500059, Most Circular Partition of a Square.
Date: 2026-10-13. Third newly documented substantive construction pass in this continuation. Earlier lifetime attempt count is unknown.

## Theorem and scope

There is a partition of the square into 121 positive-area closed strictly convex polygons such that every cell's smallest enclosing-circle radius divided by its largest inscribed-disk radius is strictly less than

    U = 1295864/1000000 = 1.295864.

Thus the infimum over all finite convex partitions is at most 1.295864. This improves the separately accepted 100-cell rational upper bound 1.296046 by 0.000182, and the first-pass 92-cell bound 1.298322 by 0.002458. It is also below the complete-square value 1.29950 reported in the source below. These are comparisons of explicit upper bounds, not claims of literature priority or optimality.

The unrestricted infimum and finite attainment remain open in this work. The previously accepted lower constant G is approximately 1.2886844618704579; this construction does not strengthen that lower bound. It proves full closed coverage of the square, including its interior, rather than a boundary-only patch.

## Frozen exact specification

The complete file `rational_partition_certificate.json` is 49,594 bytes and has SHA-256

    b6642d19ad90e5e9325ecf629b5e48d2226b9598271e2120623556351dbd3ebe.

It contains the square [-1,1]^2, common denominator D=10^12, 240 integer coordinate pairs V_j, 121 counterclockwise face cycles, and one disk-witness record for every face. The record for face i consists of an integer incenter A_i, integer enclosing center B_i, and positive integer radius numerator q_i. The witness indisk has center A_i/D and radius rho_i=q_i/D. The enclosing disk has center B_i/D and radius U rho_i.

These two centers are independent and need not coincide. Neither witness is assumed extremal; neither tangency of neighboring indisks nor tangency to all polygon sides is assumed. The exact final certificate alone specifies the construction; the source figure, earlier certificates, numerical optimizer and explanatory image are unnecessary for geometric verification.

## Topology provenance

The starting full certificate is the accepted 100-cell input, SHA-256

    351a1b2bb5c3d922e36e4cd8f6b4c421cdce4fb3f1b05f49dab39268e1355b40.

Its four central dodecagons are faces 25, 38, 39 and 54. Canceling their shared directed edges gives a 40-edge outer cycle. Remove their common central vertex, old vertex 92. In counterclockwise order the eight axis/diagonal vertices on the remaining boundary are old vertices

    [31, 58, 91, 125, 153, 126, 93, 59].

Insert an inner octagon with one vertex on each corresponding ray. The initial radial distance was 0.22; it is only a numerical starting value and is not imposed on the final coordinates. For each of the eight outer arcs between consecutive listed vertices, take that arc and the corresponding two inner-octagon vertices in reverse order as one ring face. Add the inner octagon as a ninth face. This replaces four faces by nine and replaces one vertex by eight: 105 faces and 208 vertices. Consistently relabel the surviving old vertices in increasing order, then the eight new vertices.

The representative ring face, numbered 96 in this intermediate mesh, has boundary cycle

    [31, 34, 36, 44, 49, 58, 201, 200].

Subdivide its edges at zero-based boundary positions 1, 3 and 6, namely (34,36), (44,49) and (201,200). Connect these three new subdivision vertices to a new interior junction. The three new faces are the consecutive outer arcs between the subdivision vertices, each closed through the junction. Apply the same operation to all eight dihedral copies of that ring face. All 24 subdivided edges are distinct. Each split adds four vertices and two faces; the resulting totals are 240 vertices and 121 faces. The three child cycles have respectively five, six and six sides before additional incidence bookkeeping. Neighboring faces include the same new shared subdivision vertices.

The final geometry was optimized after these combinatorial operations. In particular, a vertex originally placed on an old edge is not required to remain collinear with its old endpoints. Every final face is strictly convex. The final graph has 336 interior edges and 24 boundary edges, hence 360 edges in total, and 240-360+121=1. Topology is provenance; the direct exact geometric proof below does not infer coverage from the graph alone.

## Exact geometric verification

For integer vectors write det(u,v)=u_x v_y-u_y v_x. Every acceptance comparison below is an arbitrary-precision integer comparison, without a floating-point tolerance. The full supporting-edge pair list and per-face margins are supplied as additional evidence.

### Strict convexity and containment

Every coordinate component lies in [-D,D]. Each face contains distinct vertex indices. For every directed edge V to W of a face and every other vertex Z of that same face, the exact test is

    det(W-V,Z-V) > 0.

All these inequalities hold, with minimum positive determinant

    1275918642918821626240.

Testing all other vertices, rather than just adjacent turns, proves that the cycle bounds a positive-area strictly convex polygon and excludes a self-crossing cycle. Each cell is contained in the square since all its vertices are there and the square is convex.

### Pairwise disjoint interiors

For each of the 121*120/2 = 7260 unordered pairs of faces, there is a directed edge V to W of one face such that

    det(W-V,Z-V) <= 0

for every vertex Z of the other face. The first face's interior is contained in the strictly positive half-plane. The second face is contained in the nonpositive half-plane. Their interiors are therefore disjoint. The complete list in `pair_separation_witnesses.json` records one such supporting edge for every pair, without omissions or duplicate pairs.

### Full closed coverage

The exact sum of doubled shoelace areas is

    sum_i sum_{j cyclic in face i} det(V_j,V_{j+1})
      = 8000000000000000000000000 = 8 D^2.

The actual cell areas sum to four. Their pairwise interior intersections are empty and their polygon boundaries have area zero, so the union also has area four. All cells lie in the square. Their union is a finite union of closed sets and is therefore closed. If a point of the square were omitted, a relatively open neighborhood in the square would be omitted. Such a neighborhood has positive planar area even at an edge or a corner, contradicting equality of areas. Hence the union covers every point of the square.

As redundant incidence checks, every directed edge occurs once; exactly 336 undirected edges occur twice with opposite orientations; the remaining 24 edges lie on the square boundary. These checks agree with, but do not replace, geometric separation and coverage.

### Inscribed disks

For face i, edge V to W, and E=W-V, put T=det(E,A_i-V). The exact certificate satisfies

    T > 0,
    T^2 - q_i^2 ||E||^2 > 0.

Thus A_i/D lies strictly inside every supporting half-plane and is farther than rho_i=q_i/D from every boundary line. Its disk of radius rho_i is contained in the intersection of these half-planes, which is the polygon. The true inradius r_i therefore satisfies r_i >= rho_i > 0.

There are 696 strict inscribed-disk edge tests. Their minimum squared integer slack is

    9607630465643177666148390959368892.

The smallest positive witness radius numerator is 31731359227.

### Enclosing disks and strict ratio

Set g=1295864 and h=1000000. At every vertex V of face i the exact test is

    g^2 q_i^2 - h^2 ||V-B_i||^2 > 0.

All 696 tests hold. Their minimum integer slack is

    178213853016329475463288384.

Every vertex lies strictly inside the disk centered at B_i/D of radius U rho_i. By convexity of a disk, the entire polygon lies in that disk. More precisely, the finite maximum of its vertex distances is strictly below U rho_i; the polygon is contained in the disk with that smaller maximum radius. Its true enclosing radius R_i is therefore strictly below U rho_i. Consequently

    R_i/r_i <= R_i/rho_i < U = 1.295864

for every cell. This proves the theorem.

## Discovery, exact proof, and audit status

The discovery optimization used shared mesh coordinates with dihedral symmetry and independently variable disk centers and witness radii for each face orbit. Its final numerical objective was approximately 1.2958639276035384. Coordinates and centers were rounded consistently to denominator 10^12, and radius numerators were reduced by 100 after flooring. The numerical maximum witness ratio after rounding is approximately 1.2958639317072347. Neither floating-point figure is used as a proof premise.

The exact integer certification establishes the stated rational bound. A producer-run replay of an earlier independently written checker is additional regression evidence only; it is not a new independent worker audit. Any fresh acceptance must bind this final certificate and proof explicitly. The separate third-pass reviewer owns that independent verdict.

This pass also tested central merges, boundary bisections, ring radii and ring/corner trisection patterns. The experiment ledger records their observed outcomes. Failure to improve in a local solve is not a mathematical impossibility theorem or a global-optimality certificate. The search was stopped after the stated bounded variations and this exact complete witness was frozen.

## Source context and remaining limits

Mirela Damian and Joseph O'Rourke, *Partitioning Regular Polygons into Circular Pieces I: Convex Partitions*, arXiv:cs/0304023v2, revised 2026-02-08, Figure 16 and Section 5.2:

https://arxiv.org/abs/cs/0304023v2

https://arxiv.org/html/cs/0304023v2#S5.SS2

That source's 92-cell layout was the provenance of the earlier authored mesh, not an input required to verify the final coordinates. This report relies on the separately documented source audit for that attribution and does not claim a new source retrieval or exhaustive priority search. TOPP Problem 59 remains the problem reference: https://topp.openproblem.net/p59.

No global lower-bound improvement, unrestricted optimum, finite-attainment theorem, or equivalence with infinite partitions follows from this finite upper witness. The accepted lower-bound and local boundary-transition work remain separate from this complete construction.
