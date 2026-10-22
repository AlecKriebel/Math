# Independent acceptance of the 100 cell square construction

Problem: row 1757 / 5500059 / AMR0540059. Review date: 2026-10-13.

## Verdict and frozen inputs

Accepted. There is a complete partition of the square into 100 positive-area strictly convex polygons whose maximum circumradius-to-inradius ratio is strictly less than 648023/500000 = 1.296046. This establishes a genuine whole-square upper bound. It does not establish the optimum, attainment at the optimum, a global lower-bound improvement, an infinite-partition equivalence, or literature priority.

Acceptance binds the complete, unchanged inputs below:

- `rational_partition_certificate.json`: 41041 bytes; SHA-256 `351a1b2bb5c3d922e36e4cd8f6b4c421cdce4fb3f1b05f49dab39268e1355b40`.
- `IMPROVED_CONSTRUCTIVE_UPPER_BOUND.md`: 9008 bytes; SHA-256 `ed34e0dbfd0941f4306ef156037e5c6ca2030b0ad27190369ec7a9db528dff20`.
- The complete prior 92-cell certificate used only for topology provenance has SHA-256 `7be877a90bf7c08e7c872f461fb4f005d8d47d6d58d888363384df2865941b47`.
- The producer's complete separation list has SHA-256 `de1e5a954bce606d8b917f09f1a792270ba3a73df745c989712be0abad275e65`.

The full mathematical inputs are supplied in this edition or linked to the sibling first edition. Acceptance does not depend on the optimizer, a picture, summaries of the certificate, or the earlier acceptance of a different certificate.

## Independent implementation and exact results

The fresh geometric checker was written for this review. It imports neither the producer's code nor the old independent checker. Its central non-overlap algorithm is exact rational Sutherland-Hodgman polygon clipping, not a replay of the producer's supporting-edge acceptance loop. Python arbitrary-precision integers and `fractions.Fraction` are used throughout. Every acceptance test raises an explicit exception rather than using an assertion that optimization could remove.

For every face, a separately constructed monotone-chain convex hull equals the supplied counterclockwise cycle up to cyclic rotation, with every listed point an extreme hull vertex. This verifies strict convexity, positive area, absence of repeated points, and absence of self-crossing cycles. All 201 points lie in the stated square. All 100 faces pass. The redundant all-edge/all-other-vertex minimum determinant is exactly 1047226246554168952791, agreeing with the proof.

All 4950 unordered face pairs are actually intersected using rational half-plane clipping. The results are 4672 empty intersections, two point intersections, and 276 segment intersections. Every intersection has exactly zero area. In addition, the checker independently finds an integer projection axis and separating threshold for each of the 4950 pairs. These full results are in [the complete independent pair-intersection and separation certificate](independent_pair_intersections_and_separations.json); this is independently generated evidence, not a renamed producer list. A third check validates each of the producer's 4950 rows, its supporting directed edge, and every tested vertex, and verifies that no pair is omitted or duplicated.

The doubled integer shoelace area is exactly 8000000000000000000000000 = 8 * 10^24. With common denominator 10^12, the sum of cell areas is exactly four. The cells lie in the square and have pairwise disjoint interiors, so their finite union has the square's area. Their union is closed. Any omitted point, including a boundary point or corner, would have a relatively open missing neighborhood of positive planar area. Thus area equality gives pointwise coverage of the entire square, not merely an almost-everywhere cover.

Edge incidence independently gives 276 oppositely oriented paired interior edges, 24 boundary edges lying on square sides, 300 total edges, and Euler characteristic 201 - 300 + 100 = 1. These are redundant consistency checks, not substitutes for the geometric non-overlap and coverage arguments.

For every directed face edge, the checker verifies that the indicated incenter is strictly inside the supporting half-plane and that its exact squared distance to the line exceeds the proposed squared radius. All 576 inequalities pass; the minimum cross-multiplied integer slack is 25059339088594949021238019471065531. The least positive radius numerator is 41861305589.

For every face vertex, its squared distance from the independently specified enclosing center is strictly less than (648023/500000)^2 times the squared witness inradius. All 576 inequalities pass; the minimum cross-multiplied integer slack is 1015689497729169821880099209. Convexity of a disk extends vertex containment to the whole polygon. These strict vertex inequalities and a positive lower bound on the true inradius imply the claimed strict ratio. Neither witness center must be extremal, and they need not coincide.

The full numerical-free output is [the complete exact audit](INDEPENDENT_EXACT_CHECK.json).

## Adversarial controls

The fresh checker rejects 17 deliberately invalid certificates:

1. Negative coordinate denominator.
2. A floating-point coordinate replacing an integer.
3. A Boolean face index.
4. A vertex one integer unit outside the square.
5. A reversed polygon.
6. A self-crossing vertex order.
7. A repeated vertex in a cycle.
8. Zero witness radius.
9. An oversized indisk.
10. An incenter moved outside its cell.
11. An enclosing center moved so vertices are missed.
12. The impossible claimed ratio one.
13. A missing disk witness.
14. A missing cell, rejected for failed coverage.
15. Replacement of a face by an equal-area face, creating both a hole and an overlap while preserving total area.
16. Translation of one interior face, its incenter, and its enclosing center by one integer coordinate unit, preserving its area and all its individual disk data but causing a positive-area overlap.
17. Incorrect square metadata.

The two area-preserving controls specifically establish that area equality alone cannot fool the checker. Three benign transformations are accepted: cyclic rotation of every face, reversal of the paired face/witness list, and consistent global vertex relabeling. Full observed outcomes and rejection reasons are retained in [the complete control outcomes](INDEPENDENT_CONTROL_CHECK.json). They are algorithm tests; they are not substitutes for the complete exact acceptance run.

## Topology and source provenance

The exact graph of the final certificate has four new degree-three interior junctions, numbered 188, 192, 196, and 200. For each junction, canceling the three child faces' internal edges and removing the new subdivision vertices reconstructs one old octagon. These are old faces 15, 16, 69, and 70. Contracting all four junctions and removing the other new subdivision vertices recovers every one of the original 92 face cycles exactly. The old coordinates independently verify the four octagons are dihedral copies.

For the representative old cycle [18,38,48,54,52,46,42,25], the subdivided edges are precisely (38,48), (52,46), and (25,18). The replacements add sixteen vertices and eight faces, giving 201 vertices and 100 faces. The full reconstruction is retained in [the complete topology reconstruction](TOPOLOGY_PROVENANCE_CHECK.json). This audits the stated combinatorial provenance without assuming that the newly optimized subdivision vertices remain collinear with their old endpoints; they need not, and the final strict convexity checks show that they do not create artificial straight angles in these faces.

The primary source was checked again on 2026-10-13: Mirela Damian and Joseph O'Rourke, *Partitioning Regular Polygons into Circular Pieces I: Convex Partitions*, arXiv cs/0304023v2, revised 2026-02-08, https://arxiv.org/abs/cs/0304023v2. Its Section 5.2 and Figure 16 identify the 92-piece construction and reported ratio 1.29950: https://arxiv.org/html/cs/0304023v2#S5.SS2. This corroborates the source attribution and the comparison of reported bounds. No source image or copied source document is needed for the new construction's proof. The preserved first-pass source audit supplies source context. This review does not independently reconstruct every edge of the published Figure 16; the exact new-to-old authored topology contraction is independently checked here. The final certificate is self-contained, so this provenance limit does not affect acceptance of its geometry.

The exact new bound is 0.002276 below the previous authored bound 1.298322 and below the source's reported 1.29950. These statements compare explicit bounds. They are not exhaustive priority or novelty claims.

## Reproducibility and recovery

Mode verification replays the complete fresh geometry audit with controls, the topology audit, and the exact lower-gap and separate corner-chain algebra audits normally and under Python -O and -OO, requiring byte-identical output for each script across modes. The lower-gap geometry itself is reviewed separately in [the independent quantitative review](INDEPENDENT_QUANTITATIVE_REVIEW.md).

The independent audit preservation receipt records actual extraction by both routes, exact agreement of every restored path, byte count and SHA-256, and fresh checker replay against the restored full certificate. The preservation claim is limited to the checks recorded in that receipt; merely constructing an archive is not counted as successful restoration.
