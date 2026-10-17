# Independent acceptance of a rational 92-piece construction

## Result

The finite full-square circularity infimum is at most

649161/500000 = 1.298322.

This is strictly smaller than the 1.29950 complete-square upper bound reported in Damian and O'Rourke's arXiv cs/0304023v2, Table 1, Figure 16, and Section 5.5: https://arxiv.org/abs/cs/0304023v2. This comparison is with an identified source-reported bound. A bounded literature search is not a proof of global novelty, and no optimality or finite-attainment claim follows.

## Exact accepted input

- File identity: rational_partition_certificate.json
- Bytes: 37572
- SHA-256: 7be877a90bf7c08e7c872f461fb4f005d8d47d6d58d888363384df2865941b47
- Square: [-1,1]^2
- Common coordinate denominator: 10^12
- Distinct vertices: 185
- Convex cells: 92
- Claimed ratio: 649161/500000

The input gives vertex integer numerators, counterclockwise cell cycles, a feasible disk center and positive radius for each cell, and a possibly different enclosing-circle center. The declared provenance is an authored optimization of the combinatorial layout in Figure 16. This audit certifies the supplied rational geometry, not the precision of the original figure and not the optimizer's floating-point logs.

The checker was independently implemented from the certificate's mathematical contract; it does not import or execute the producer's checker, optimized floating-point data, mesh extraction, or summaries. All acceptance decisions use arbitrary-precision integers and explicit error branches. Python optimization flags do not disable them.

## Whole-square proof

Write D=10^12. For each listed cell, the checker verifies that all vertex coordinates lie between -D and D, that no vertex repeats within its cycle, that each edge has nonzero length, and that every cell vertex is on or to the left of every oriented edge. Its shoelace area is positive. These support inequalities certify a convex polygon with the declared positive orientation.

For every unordered pair of cells, at least one supporting edge of one cell puts all vertices of the other cell in its closed outer half-plane. Thus the cell interiors are disjoint. This was checked for all 92*91/2 = 4186 pairs; it is not inferred from a drawing or approximate mesh incidence.

The sum of all doubled shoelace areas is exactly

8000000000000000000000000 = 8 D^2,

the doubled area of the square. All cells lie inside the square. Therefore their union has the square's area. Their finite union is closed. If a point of the square were missing, the relative complement would contain a relatively open neighborhood of positive planar area, even at a square edge or corner. That contradicts equal area. Consequently the cells cover every point of the square, not merely almost every point or its boundary.

## Circle proof

For each cell edge from a to b, center I, and radius numerator r>0, set

c = (b_x-a_x)(I_y-a_y) - (b_y-a_y)(I_x-a_x).

The checks require c>0 and c^2 >= r^2 |b-a|^2. Hence the disk of radius r/D centered at I/D lies inside every supporting half-plane and therefore inside the polygon. Across all 528 cell edges, the inequalities are strict; the smallest integer slack is

21267508483484519258859509868261049.

For each cell vertex v and enclosing center C, with G_n=649161 and G_d=500000, the checker verifies

G_d^2 |v-C|^2 <= G_n^2 r^2.

A disk is convex, so containing all polygon vertices contains the whole cell. Across all 528 vertex incidences the inequalities are strict; the smallest integer slack is

804622615113166660805053316.

The true largest indisk has radius at least this witness radius. The true smallest enclosing circle has radius at most G times this witness radius. Thus the true ratio R(P)/r(P) is at most G for every cell. Neither center is required to coincide, and the witnesses need not be optimal circles.

## Adversarial and reproducibility checks

Twelve malformed or mathematically false certificates were independently rejected: reversed cell orientation; omitted cell; duplicate cell; a vertex outside the square; repeated vertex in one cell; oversized indisk; external incenter; external enclosing center; a claimed ratio of one; zero denominator; Boolean denominator; and a changed target square. The duplicate-cell control specifically reaches pairwise overlap rejection; omitting the final cell specifically reaches area rejection.

Two valid transformations were accepted: changing the order of cells together with their disk witnesses, and cyclically rotating each vertex cycle. The checker therefore tests geometry rather than just matching one serialization.

Normal Python, Python -O, and Python -OO produced identical reports, each SHA-256 6197be372930742638f1804805e485083b54196120876397e38edf641d93224f. Exact frozen-input hashing is required before replay. Executable code remains in the private recovery package; the public mathematical certificate and this authored acceptance argument suffice to state the theorem.

## Limits

This establishes an explicit upper bound for an admissible finite partition and hence also for any larger class containing finite partitions. It provides no matching lower bound, no proof that this topology is optimal, no theorem about infinitely many cells, and no solution of the finite-attainment conjecture. A changed certificate requires a new exact audit.
