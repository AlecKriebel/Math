# Independent checking guide: the complete 100-piece partition

This edition supplies a complete mathematical coordinate certificate, every pair-separation witness, every cell's exact margin summary, and an authored drawing. The original optimization and checker programs are not needed to read or independently implement these finite checks.

## Interpret the exact geometry

Read [rational_partition_certificate.json](rational_partition_certificate.json). The target square is [-1,1]^2 and the coordinate denominator is D=10^12. Divide every vertex numerator, disk-center numerator and positive indisk-radius numerator by D. Each counterclockwise face list gives one closed convex polygon. The enclosing disk radius is G times the listed indisk radius, with G=648023/500000. The two centers may differ. All faces and witnesses are listed: this is a full-square construction, not a boundary strip.

The expected counts are 201 distinct vertices, 100 faces, and 576 vertex-edge incidences. Indices are zero-based. Reject noninteger numerators, Boolean values masquerading as integers, zero or negative denominators/radii, invalid indices, duplicate vertices in a face, or an undeclared target square. Every listed vertex must be used and lie inside the square.

## Convexity, disjointness and exact coverage

For each edge V to W and every other vertex U of that face, require det(W-V,U-V)>0. This checks the entire supporting half-plane, not merely local turns, and establishes strict convexity of the specified cycle. The shoelace doubled area must be positive.

Read [pair_separation_witnesses.json](pair_separation_witnesses.json). Require one row for each of the 4,950 unordered face pairs, with no duplicates. Its supporting face must be one of the pair, and its specified oriented edge must actually occur in that face. Every vertex U of the other face must satisfy det(W-V,U-V)<=0. The supporting face's interior lies in the opposite open half-plane. Thus the interiors are disjoint. Alternatively, find a separating edge afresh for each pair; both approaches were checked.

Compute the sum of doubled shoelace areas directly from the coordinate certificate. It must equal 8D^2 exactly. All faces lie in the square and have pairwise disjoint interiors, so their union has area four. A finite union of closed polygons is closed. Any missing point of the square, including an edge or corner point, would have a relatively open neighborhood of positive area outside that union. Equal area therefore implies pointwise coverage of the whole square.

As a redundant incidence check, count 276 interior undirected edges, each used twice in opposite directions, and 24 boundary edges, each used once and lying along a square side. There are 300 undirected edges total, and 201-300+100=1.

## Disk inequalities and strict circularity

For face i let A be its indisk-center numerator, B its enclosing-center numerator and q>0 its radius numerator. For every edge V to W set T=det(W-V,A-V). Require T>0 and

T^2-q^2|W-V|^2>0.

The disk of center A/D and radius q/D is then inside every supporting half-plane. For every vertex V require

648023^2 q^2-500000^2|V-B|^2>0.

The convex hull lies strictly within the enclosing disk. The true inradius is at least q/D, and the true enclosing radius is strictly less than Gq/D. Hence the true ratio is strictly less than G for all 100 faces, without having to compute either optimal circle.

Recompute each row of [exact_face_margin_table.json](exact_face_margin_table.json), including vertex count, doubled area and the three minimum positive margins. The global strict-convexity determinant is at least 1047226246554168952791. The least squared indisk slack is 25059339088594949021238019471065531; the least enclosing slack is 1015689497729169821880099209; the smallest radius numerator is 41861305589. The [verification summary](exact_verification_summary.json) and [independent-checker replay](INDEPENDENT_CHECKER_REPLAY.json) must agree with these recomputed values. Floating-point diagnostic ratios do not establish any inequality.

## Diagram and controls

[partition.svg](partition.svg) uses the exact listed coordinates at twelve decimal places. Check that it has exactly 100 polygons with the same ordered vertices. It contains no script, event handler, link, external resource, embedded foreign object, animation, entity declaration or executable content. It is an optional illustration; the mathematical proof depends on the coordinate and inequality certificates.

An independently written checker accepted the geometry and rejected twelve malformed or false constructions; benign face reorderings and cyclic changes of each face's starting vertex remained valid. The edition also checks the complete pair witnesses, per-face margins, summary data and SVG against the coordinates. Checker acceptance and rejection are explicit and remain effective in normal, -O and -OO Python modes.

These checks certify one finite feasible construction. They do not certify optimality, finite attainment, an exhaustive search of all partitions, or literature priority. The construction modifies the Figure 16 layout of Damian and O'Rourke by splitting four diagonal octagons; the rational coordinates and disk witnesses are newly authored.
