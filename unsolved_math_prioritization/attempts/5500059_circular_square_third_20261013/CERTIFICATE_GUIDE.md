# Independent checking guide: the complete 121-piece partition

This guide describes checks on the complete coordinate data, all pair witnesses and every face margin without requiring the original numerical optimizer or any supplied program. The [full authored proof](THIRD_PASS_CONSTRUCTIVE_UPPER_BOUND.md) explains why the checks imply a valid complete-square upper bound.

## Exact geometry and input discipline

Read [rational_partition_certificate.json](rational_partition_certificate.json). The target is [-1,1]^2. Its common denominator is D=10^12; divide all vertex, center and witness-radius numerators by D. Each counterclockwise face is one closed polygon. There are 240 distinct vertices, 121 faces, 121 disk-witness records and 696 face-vertex incidences. The enclosing disk of each face has radius U times the witness indisk radius, where U=1295864/1000000.

Reject noninteger or Boolean-valued numerators and indices, nonpositive denominators or radii, invalid face indices, repeated vertices in a face, duplicate vertex locations, unused vertices and an undeclared square. Every vertex must lie inside the square. The two disk-center witnesses may differ and need not be optimal centers.

For every oriented edge V to W and every other vertex Z of that face, require det(W-V,Z-V)>0. Check all other vertices, not merely adjacent turns. This certifies the entire ordered polygon as a strictly convex counterclockwise cycle. The doubled shoelace area must be positive.

## All pairs, exact area and pointwise coverage

[The pair-separation certificate](pair_separation_witnesses.json) has exactly one row for every unordered face pair, all 7,260 of them. Require no repeated or missing pair. Its supporting face must be a member of that pair, and its oriented edge must occur in that face. Every vertex of the other face must be in the nonpositive half-plane of that edge; the supporting face's interior is in the positive half-plane. Thus the pair interiors are disjoint.

The [fresh independent pair records](INDEPENDENT_PARTITION_PAIRS.json) separately contain the exact intersection hull and separating-axis data for every pair. To recompute an intersection, take all vertices of either polygon that lie in the other, all exact segment-intersection points, and their convex hull. There are 6,916 empty intersections, eight points and 336 segments; none has positive area. The fresh axes supply a redundant independent separation check.

The exact doubled area sum must equal 8D^2=8000000000000000000000000. Containment, pairwise disjoint interiors and equal area imply full area coverage. A finite union of closed polygons is closed; any omitted point in the square, including on a side or corner, would have a relatively open neighborhood of positive area outside the union. Hence every square point is covered.

Redundant incidence checks give 336 interior undirected edges, each used twice in opposite directions, and 24 boundary edges used once. Those boundary intervals must consecutively cover all four sides. There are 360 undirected edges, and 240-360+121=1. These counts do not replace the geometric nonoverlap and area proof.

## Strict disk inequalities

For a face with incenter numerator A, enclosing-center numerator B and radius numerator q>0, set T=det(W-V,A-V) for each oriented edge. Require T>0 and

T^2-q^2|W-V|^2>0.

These inequalities place a disk of radius q/D inside the polygon. For every vertex V require

1295864^2 q^2-1000000^2|V-B|^2>0.

The finite maximum vertex distance from B/D is strictly less than Uq/D, so a strictly smaller enclosing disk exists. The true inradius is at least q/D and true enclosing radius is below Uq/D. Their quotient is strictly below U. This remains valid with different disk centers and does not require neighbor-disk tangency.

Recompute all 121 rows of [the exact margin table](exact_face_margin_table.json): face size, doubled area, minimum all-vertex convexity determinant, minimum squared indisk slack and minimum enclosing slack. The global minimum convexity determinant is 1275918642918821626240; minimum indisk slack is 9607630465643177666148390959368892; minimum enclosing slack is 178213853016329475463288384; smallest radius numerator is 31731359227. There are 696 inequalities of each disk type and 2,760 strict convexity tests.

Compare the recomputed results with [the producer summary](exact_verification_summary.json) and [fresh independent exact audit](INDEPENDENT_PARTITION_CHECK.json). Floating-point discovery and orientation figures prove no inequality.

## Passive illustration and hostile controls

[partition.svg](partition.svg) has exactly 121 polygon elements, with the certificate's ordered coordinates represented exactly at twelve decimal places. It contains no script, event handler, link, external resource, entity declaration, animation or foreign object. It is an optional drawing; the proof uses exact coordinate data.

The fresh independent geometry checker rejects 17 false or malformed constructions, including an area-preserving shift of an interior cell and its two disk centers. Three benign transformations remain valid: cyclic face rotations, simultaneous face/witness reorder and global vertex relabeling. The edition also checks semantic scope, every margin and pair record, reversible text maps, the complete retained-source byte store, crosslinks, sibling byte identities and the SVG's passive content. Normal, -O and -OO checks agree; acceptance conditions do not depend on removable assertions.

These are feasibility and reproducibility checks. They do not prove global optimality, finite attainment or literature priority. The [independent topology report](INDEPENDENT_TOPOLOGY_CHECK.json) reconstructs the described 100-to-105-to-121 sequence from the complete certificates, while geometric acceptance remains self-contained.

## Separate exact boundary-cover certificate

[boundary_patch_certificate.json](boundary_patch_certificate.json) is a different witness with a different schema. Its exact rationals are strings of integers or fractions. Eight canonical types list each full strictly convex polygon, unit-indisk center, enclosing-circle center and prescribed endpoints. The 56 placements specify a positive rational scale, baseline translation, optional reflection and quarter-turn rotation. Apply the translation and scale, reflect x to S-x if specified, then repeatedly replace (x,y) with (S-y,x); reverse polygon orientation after a reflection. All placed coordinates must lie in [0,S]^2.

Check that each canonical cycle equals its strict counterclockwise convex hull. Each directed edge must contain the unit disk in its inward half-plane: its inward determinant is positive and its square is at least the edge's squared length. Equality in this indisk condition is allowed. Each vertex's squared distance from the separately listed outer center must be strictly below (64439/50000)^2. Positive similarities transfer these disk bounds and strict circularity to all placed cells. There are 960 canonical edge/vertex tests of each kind and 7,104 placed vertices.

Recompute projection intervals for every polygon on the listed exact separating axes. Each of the 1,540 unordered pairs must have a valid nonoverlap interval ordering. Do not infer nonoverlap from area alone or accept incomplete or duplicate producer pair rows. The [independent boundary pairs](INDEPENDENT_BOUNDARY_PAIRS.json) separately search the axes and record exact contact geometry: 1,484 pairs are empty and 56 share a segment. At every contact the segment must be a complete edge of each polygon, and the full set of contacting pairs must equal the adjacency induced by consecutive square-boundary intervals.

Extract actual polygon edges on each of the four square sides. Fifteen intervals on each side must run consecutively from 0 to S with no gap or overlap. The square center (S/2,S/2) must violate an inward half-plane inequality strictly for every polygon. The summed exact positive area must be strictly less than S^2. Thus an open neighborhood of the center is uncovered: this is a boundary cover, not a square partition.

The [independent boundary audit](INDEPENDENT_BOUNDARY_CHECK.json) retains the exact positive doubled-area deficit and least positive center-exterior determinant. Its 13 rejected hostile controls include an extra translated interior copy that leaves all boundary coverage and individual disk data intact but creates overlap. A benign cyclic rotation passes. The author separately supplies [exact checks](EXACT_BOUNDARY_CHECK.json), [controls](BOUNDARY_CONTROL_CHECK.json) and [algebra identities with mutations](ENVELOPE_ALGEBRA_CHECK.json). The symbolic envelope identities supplement the complete analytic proof and [independent mathematical review](INDEPENDENT_BOUNDARY_THEORY_REVIEW.md).

The passive [boundary illustration](boundary_cover.svg) is generated from all 56 exact placements after normalizing the square side to 1. Coordinates are rounded to twelve decimal places for display, with error at most 1/(2*10^12) per normalized component. The center is plainly labeled uncovered. The drawing is never used as an exact geometric witness, and its smaller boundary-only ratio is not a whole-square upper bound.
