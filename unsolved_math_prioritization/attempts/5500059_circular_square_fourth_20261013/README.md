# Most Circular Partition of a Square: fourth authored edition

Problem 5500059 / AMR-054-0059 / TOPP 59. Status: unresolved. Date: 13 October 2026.

This is the fourth newly documented substantive investigation in the present continuation, giving at least four new passes. The earlier lifetime attempt count is unknown. This label does not reset a budget or establish an attempt limit. The first, second and third authored editions remain unchanged.

## Complete-square upper bound

The [complete construction proof](FOURTH_PASS_CONSTRUCTIVE_UPPER_BOUND.md) supplies a partition into 121 positive-area closed strictly convex polygons, each with circularity strictly below

1295516/1000000 = 1.295516.

Circularity is the smallest-enclosing-circle radius divided by the largest-inscribed-disk radius. Their centers are independent. The theorem does not assume common disk centers or tangency between neighboring indisks.

This improves the [third edition's complete 121-cell witness](../5500059_circular_square_third_20261013/THIRD_PASS_CONSTRUCTIVE_UPPER_BOUND.md) by 0.000348. It also improves the [second edition's 100-cell witness](../5500059_circular_square_second_20261013/IMPROVED_CONSTRUCTIVE_UPPER_BOUND.md) and the [first edition's 92-cell witness](../5500059_circular_square_first_20261013/CONSTRUCTIVE_UPPER_BOUND.md). These compare explicit feasible bounds and establish no global novelty or optimality.

The exact witness has 240 rational vertices, 121 face cycles, 7,260 unordered pair separators, 696 disk-edge inequalities, 696 enclosing-vertex inequalities, and 121 per-face margin records. Exact positive areas sum to the square area. Pairwise disjoint interiors and the finite closed-union argument prove coverage of every interior and boundary point.

Eight explicit edge flips in two fourfold stages relate the previous and new face cycles. They preserve the total cell count while changing the central cell from a 16-gon to a 20-gon. The final rational certificate defines the geometry without relying on the numerical discovery procedure or the topology history.

## Two distinct boundary-only results

The [fixed-patch obstruction](FIXED_PATCH_INTERIOR_OBSTRUCTION.md) proves that any finite convex completion preserving every cell of the [third edition's exact 56-cell boundary patch](../5500059_circular_square_third_20261013/boundary_patch_certificate.json), with maximum circularity below sqrt(2), needs at least 6,826 additional interior pentagons and at least 6,882 cells in total. Genuine polygon sides are counted after removing collinear intermediate vertices. At ceiling at most 13/10, the exact identity is

P5 = 6826 + sum_{k>=7}(k-6)Pk + T + 2V4.

Here Pk counts added k-gons, T counts interior T-junctions, and V4 counts four-cell interior vertices. The theorem allows arbitrary T-junctions and non-face-to-face partitions. It is a necessary count, not an existence theorem.

The [coarsened boundary construction](COARSENED_BOUNDARY_REPAIR.md) supplies a distinct 56-cell boundary cover, still with each ratio strictly below 64439/50000 = 1.28878, but reducing its total genuine side count from 7,104 to 588. It keeps the complete outer boundary coverage and shared separators, and leaves an open neighborhood of the square center uncovered. Its necessary completion burden drops to at least 310 additional pentagons and at least 366 total cells, with identity

P5 = 310 + sum_{k>=7}(k-6)Pk + T + 2V4

at ceiling at most 13/10. The smaller requirement does not establish that 366 cells suffice or that a completion exists.

Neither boundary patch is a partition of the square. Neither provides a whole-square upper bound. The boundary-only number 1.28878 cannot replace the complete-square bound 1.295516. The two certificates are distinct, so the coarsening result does not contradict the fixed-original-patch theorem.

## Reading order and exact witnesses

1. [Complete-square proof](FOURTH_PASS_CONSTRUCTIVE_UPPER_BOUND.md), [rational partition certificate](rational_partition_certificate.json), and [passive full-square illustration](partition.svg).
2. [Complete pair-separation witnesses](pair_separation_witnesses.json), [per-face margins](exact_face_margin_table.json), [exact summary](exact_verification_summary.json), [eight topology operations](topology_operations.json), and [producer topology replay](TOPOLOGY_REPLAY.json).
3. [Full independent construction review](INDEPENDENT_CONSTRUCTION_REVIEW.md), [fresh independent construction check](INDEPENDENT_CONSTRUCTION_CHECK.json), [complete independent pair-separation witnesses](INDEPENDENT_PAIR_SEPARATIONS.json), and [producer regression replay](PRIOR_CHECKER_REPLAY.json).
4. [Fixed-original-patch proof](FIXED_PATCH_INTERIOR_OBSTRUCTION.md) and [exact topology count](EXACT_TOPOLOGY_CHECK.json).
5. [Coarsened-patch proof](COARSENED_BOUNDARY_REPAIR.md), [full rational boundary certificate](coarsened_boundary_certificate.json), [producer exact boundary check](COARSENED_BOUNDARY_CHECK.json), [producer topology count](COARSENED_TOPOLOGY_CHECK.json), and [passive boundary-only illustration](coarsened_boundary_cover.svg).
6. [Full independent boundary review](INDEPENDENT_BOUNDARY_REVIEW.md), [independent exact boundary audit](INDEPENDENT_BOUNDARY_CHECK.json), [all original-patch pair records](INDEPENDENT_ORIGINAL_BOUNDARY_PAIRS.json), [all coarsened-patch pair records](INDEPENDENT_COARSENED_BOUNDARY_PAIRS.json), [independent mode replay](INDEPENDENT_MODE_REPLAY.json), and [producer boundary mode replay](BOUNDARY_AUTHOR_MODE_REPLAY.json).
7. [Checking guide](CERTIFICATE_GUIDE.md), [integration and acceptance](INTEGRATION_AND_ACCEPTANCE.md), [source context](SOURCE_CONTEXT_METADATA.json), and [public byte manifest](PUBLIC_MANIFEST.json).

Independent computational and mathematical review does not mean human peer review. Producer regression checks using previously authored code are identified separately.

## Unchanged lower bound and remaining question

The [first edition's theory](../5500059_circular_square_first_20261013/THEORY_REPORT.md), with its [independent review](../5500059_circular_square_first_20261013/INDEPENDENT_THEORY_REVIEW.md), gives G=1.288684461870457901325875.... The [second edition's fixed-complexity theorem](../5500059_circular_square_second_20261013/QUANTITATIVE_COMPLETION_OBSTRUCTION.md) gives, for every partition into at most N positive-area compact convex cells,

gamma > G + 1/(192 * 25^(N+2)).

For the unrestricted finite-partition infimum Gamma_fin, the accepted results give

G <= Gamma_fin < 1.295516.

The strict lower bound for each fixed N does not prove Gamma_fin>G because its correction tends to zero. The [third edition's boundary-cover theorem](../5500059_circular_square_third_20261013/UNEQUAL_ANGLE_BOUNDARY_CLOSURE.md) remains valid, with the entire interior-completion question separate.

The exact optimum and attainment over unrestricted finite cell counts remain unresolved. No equivalence with infinite partitions, exhaustive priority claim, or solution to the original problem is asserted. Complete sibling proofs and certificates are byte-pinned as dependencies rather than duplicated.
