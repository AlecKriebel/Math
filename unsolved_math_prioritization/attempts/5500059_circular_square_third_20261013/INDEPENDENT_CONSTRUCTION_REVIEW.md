# Independent acceptance of the third-pass 121-cell construction

Problem row 1757 / 5500059 / AMR0540059. Review date: 2026-10-13.

## Verdict and exact binding

Accepted: the supplied 121 strictly convex polygons partition the entire square and every cell has circumradius/inradius strictly below 1295864/1000000 = 1.295864. The bound improves the previously accepted explicit 1.296046 by 0.000182. This is an upper-bound comparison, not an optimality, finite-attainment, unrestricted lower-bound, or literature-priority claim.

Acceptance binds the unchanged complete files:

- [the complete rational certificate](rational_partition_certificate.json): 49,594 bytes, SHA-256 `b6642d19ad90e5e9325ecf629b5e48d2226b9598271e2120623556351dbd3ebe`.
- [the complete construction proof](THIRD_PASS_CONSTRUCTIVE_UPPER_BOUND.md): 10,520 bytes, SHA-256 `c96ae0ecb10cd2572786bdaa280fdaecd97ce6f55670ddc6bceed9ea82367a64`.
- The complete accepted 100-cell certificate used only for topology provenance: SHA-256 `351a1b2bb5c3d922e36e4cd8f6b4c421cdce4fb3f1b05f49dab39268e1355b40`.

The geometric proof does not depend on discovery code, numerical objectives, a drawing, or previously accepted certificates.

## Fresh implementation and independent exact geometry

The fresh exact geometry checker imports no producer checker and no previous audit checker. Its intersection algorithm is different from the earlier clipping audit: it enumerates all contained vertices and all exact segment intersections, then takes their convex hull. These are exactly the possible extreme points of the intersection of convex polygons. An independently generated separating-axis witness gives a second check for every pair. All arithmetic is integer or Python Fraction, and no acceptance condition uses an optimization-removable assertion.

The 240 distinct vertices are within the square [-1,1]^2 at denominator 10^12. In every supplied face, every other vertex is strictly to the left of every directed edge. This verifies the exact face ordering and strict convexity, and excludes self-crossing cycles. All 2,760 such tests pass, with minimum determinant 1275918642918821626240.

All 7,260 unordered polygon pairs are actually intersected. There are 6,916 empty intersections, eight point intersections, and 336 segment intersections. Every intersection has area zero, and an exact separating axis is independently found for every pair. The complete newly computed pair records are preserved in [the complete independent pair records](INDEPENDENT_PARTITION_PAIRS.json).

The sum of doubled coordinate-numerator areas is exactly 8000000000000000000000000 = 8 * 10^24, hence the sum of actual areas is four. Containment and pairwise zero-area intersections imply that the closed finite union has full square area. If any point of the square were omitted, its relatively open complement would contain positive area even at a side or corner. Therefore there are no omitted points. Independently checking every square-side interval confirms exact complete coverage of all four sides.

There are 336 oppositely paired interior edges and 24 square-boundary edges, with no unmatched interior edges. The Euler characteristic is 240 - 360 + 121 = 1. These combinatorial counts corroborate but do not replace the geometric area and nonoverlap proof.

## Separate disk centers and strict circularity

Every witness radius is a positive integer numerator; the minimum is 31731359227. For each of the 696 edges, the incenter is in the inward half-plane and its squared distance to the supporting line strictly exceeds the squared witness radius. The minimum cross-multiplied slack is 9607630465643177666148390959368892. Thus every witness disk is genuinely contained.

For each of the 696 vertices, its squared distance from the indicated enclosing center is strictly below the square of 1.295864 times the witness radius. The minimum integer slack is 178213853016329475463288384. The incenter and enclosing center are numerically different in all 121 cells and were checked separately. No concentricity or mutual disk tangency is assumed.

A convex disk containing all vertices contains the polygon. Because the finite maximum vertex distance is strictly below the proposed enclosing radius, each actual circumradius is strictly below that radius. Its actual inradius is at least the witness radius. These two one-sided facts prove the strict ratio bound without requiring either named center to be extremal.

## Hostile controls and optimization modes

Seventeen invalid inputs are rejected: negative denominator, floating coordinate, Boolean face index, outside-square vertex, reversed face, crossed face, repeated face vertex, zero radius, oversized indisk, outside incenter, bad enclosing center, impossible ratio one, missing witness, missing corner cell, duplicated overlapping cell, area-preserving one-unit translation of an interior cell and both its disk centers, and false square metadata. The translation control preserves that cell's area and disk inequalities and is rejected for a positive-area overlap, demonstrating why area alone is insufficient.

Three benign changes pass: cyclic face rotations, paired face/witness reorder, and global vertex relabeling. The complete audit and these controls give byte-identical outputs under Python normal, -O, and -OO. These controls test the implementation and supplement, rather than substitute for, the complete exact certificate verification.

## Independently reconstructed topology

The separate topology checker starts from the full accepted 100-cell input. Canceling the four stated dodecagons' internal edges independently recovers the 40-edge outer boundary and unique shared center 92. Its eight axis/diagonal boundary vertices are exactly [31,58,91,125,153,126,93,59]. Removing the old center and adding the described ring reconstructs the 105-cell intermediate graph, including its representative ring cycle [31,34,36,44,49,58,201,200].

Working backwards from the final certificate, eight new degree-three junctions are recovered at indices 211,215,219,223,227,231,235,239. Canceling each group's internal edges and removing the subdivision vertices recovers all 105 intermediate face cycles exactly. The 24 subdivided edges coincide with the exact dihedral orbit of (34,36), (44,49), (201,200), checked using exact coordinate symmetries. Each group has child side counts five, six, six. This verifies the complete authored 100-to-105-to-121 combinatorial provenance without assuming old-edge collinearity after optimization.

The source attribution to Damian and O'Rourke's reported 92-piece construction relies on the preserved prior source audit; this review makes no new independent reconstruction of the published figure or new source-retrieval claim. The accepted final coordinates are self-contained, so that provenance boundary does not affect the geometric verdict.

## Scope and recovery

The separate near-G boundary cover is audited separately and must never be read as a full-square construction. This acceptance concerns the explicit full-square upper 1.295864. It does not close the remaining gap above the previously accepted lower constant G approximately 1.2886844618704579.

The final audit preservation receipt records complete-file hashes, actual archive extraction, independent byte-store reconstruction, byte-for-byte agreement of restored trees, and reruns against restored inputs. Merely writing an archive is not counted as recovery.
