# Most Circular Partition of a Square: third authored edition

Problem 5500059 / AMR-054-0059 / TOPP 59. Status: unresolved. Date: 13 October 2026.

This is the third newly documented substantive investigation in the present continuation, giving at least three new passes. The earlier lifetime attempt count is unknown. This label does not reset a budget, establish the absence of earlier attempts, or assert an attempt limit. The first and second authored editions remain unchanged.

## Complete-square upper-bound witness

The [complete construction proof](THIRD_PASS_CONSTRUCTIVE_UPPER_BOUND.md) supplies a partition into 121 positive-area closed strictly convex polygons, each with circularity strictly below

1295864/1000000 = 1.295864.

Circularity means the smallest-enclosing-circle radius divided by the largest-inscribed-disk radius. The two disk centers are independent. No common-center or neighboring-indisk tangency assumption is imposed.

This rational bound improves the [second edition's complete 100-cell witness](../5500059_circular_square_second_20261013/IMPROVED_CONSTRUCTIVE_UPPER_BOUND.md) by 0.000182 and the [first edition's 92-cell witness](../5500059_circular_square_first_20261013/CONSTRUCTIVE_UPPER_BOUND.md) by 0.002458. It is below the source-reported complete-square upper bound 1.29950, whose provenance is documented in the [unchanged source audit](../5500059_circular_square_first_20261013/SOURCE_BOUND_AUDIT.md). These are comparisons of identified feasible bounds; no exhaustive-literature or global novelty claim is made.

The certificate uses 240 rational vertices, 121 face cycles, independent disk-center pairs, all 7,260 pair separators, and 121 exact margin rows. Exact positive areas sum to the square area, and the finite closed-union argument proves coverage of every interior and boundary point. The topology replaces four central dodecagons of the second edition with a nine-cell ring-and-center arrangement, then trisects the eight ring cells to obtain 121 cells. The exact final geometry is sufficient to verify the construction independently of its numerical discovery.

## Reading order

1. [Complete proof](THIRD_PASS_CONSTRUCTIVE_UPPER_BOUND.md), [full rational coordinate certificate](rational_partition_certificate.json), and [passive illustration](partition.svg).
2. [All 7,260 pair-separation witnesses](pair_separation_witnesses.json), [all 121 face-margin rows](exact_face_margin_table.json), and [exact verification summary](exact_verification_summary.json).
3. [Fresh independent mathematical acceptance](INDEPENDENT_CONSTRUCTION_REVIEW.md), [fresh exact geometry and hostile controls](INDEPENDENT_PARTITION_CHECK.json), [all 7,260 independent pair-intersection records](INDEPENDENT_PARTITION_PAIRS.json), and [independent topology reconstruction](INDEPENDENT_TOPOLOGY_CHECK.json).
4. [Complete unequal-angle boundary proof](UNEQUAL_ANGLE_BOUNDARY_CLOSURE.md), [exact 56-cell boundary certificate](boundary_patch_certificate.json), [passive boundary illustration](boundary_cover.svg), and [fresh independent boundary-theory acceptance](INDEPENDENT_BOUNDARY_THEORY_REVIEW.md).
5. [Independent exact boundary audit](INDEPENDENT_BOUNDARY_CHECK.json), [all 1,540 independent boundary-pair records](INDEPENDENT_BOUNDARY_PAIRS.json), [independent envelope algebra](INDEPENDENT_ENVELOPE_ALGEBRA.json), [producer exact boundary check](EXACT_BOUNDARY_CHECK.json), [producer boundary controls](BOUNDARY_CONTROL_CHECK.json), [producer algebra controls](ENVELOPE_ALGEBRA_CHECK.json), and [producer mode replay](BOUNDARY_AUTHOR_MODE_REPLAY.json).
6. [Producer-run construction regression replay](PRIOR_CHECKER_REPLAY.json), [independent producer-pair validation](PRODUCER_PAIR_DATA_VALIDATION.json), [independent mode replay](INDEPENDENT_MODE_REPLAY.json), [fresh public-source metadata](SOURCE_RETRIEVAL_METADATA.json), [independent checking guide](CERTIFICATE_GUIDE.md), [integration and acceptance](INTEGRATION_AND_ACCEPTANCE.md), and [public byte manifest](PUBLIC_MANIFEST.json).

The fresh independent acceptance is mathematical and computational review, not human peer review. The producer replay of the earlier checker is identified separately.

## Unchanged lower-bound dependencies

The [first edition's complete theory](../5500059_circular_square_first_20261013/THEORY_REPORT.md) defines and proves the lower balancing constant G=1.288684461870457901325875..., with its [independent acceptance](../5500059_circular_square_first_20261013/INDEPENDENT_THEORY_REVIEW.md). The [second edition's finite-complexity theorem](../5500059_circular_square_second_20261013/QUANTITATIVE_COMPLETION_OBSTRUCTION.md) and [independent review](../5500059_circular_square_second_20261013/INDEPENDENT_QUANTITATIVE_REVIEW.md) prove, for every partition into at most N positive-area compact convex cells,

gamma > G + 1/(192 * 25^(N+2)).

The correction tends to zero as N grows. For the unrestricted finite-partition infimum Gamma_fin, the accepted results give

G <= Gamma_fin < 1.295864.

The strict upper inequality follows from a single complete finite construction. Strict lower inequalities for each fixed N do not imply Gamma_fin>G. No unrestricted lower-bound improvement is claimed here.

## Complete boundary closure, with the interior still open

The separately accepted [unequal-angle theorem](UNEQUAL_ANGLE_BOUNDARY_CLOSURE.md) proves that for every epsilon>0 a finite disjoint family of positive-area convex polygons inside a square covers every point of its boundary, with each circularity at most G+epsilon. An open neighborhood of the square center remains uncovered. This is not a partition of the square and gives no new whole-square upper bound.

The proof derives the unequal-angle disk-and-feet envelope, verifies its three-contact branch and positive height sensitivity, matches entire separator segments, and uses a finite sequence of angle changes ending at vertical separators. Reflection and rotation remove the second edition's four mid-side gaps. Pair-by-pair geometric estimates and finite polygonal approximation preserve boundary coverage and nonoverlap while explicitly preserving the central hole. The [independent theory review](INDEPENDENT_BOUNDARY_THEORY_REVIEW.md) checks the complete argument rather than substituting symbolic identities for geometry.

The additional exact example has 56 finite convex polygons with ratio strictly below 64439/50000 = 1.28878. Eight canonical polygon types and exact rational similarities specify all 7,104 placed vertices. All 1,540 pairs are separated, all four sides have 15 consecutive covering intervals, and 56 complete shared edges match those adjacencies. Only approximately 31.9451% of square area is covered. The center lies strictly outside every cell, and an exact positive area deficit is recorded. The whole-square bound remains 1.295864; the boundary-only number 1.28878 cannot replace it.

## Scope

The exact optimum and attainment over unrestricted finite cell counts remain unresolved. The admissible partitions are finite positive-area compact convex partitions with disjoint interiors and unrestricted Steiner points. No equivalence with infinite partitions is assumed. Local patches and boundary covers are not full-square upper-bound witnesses unless the entire square, including its interior, is proved covered.

The public edition contains authored proofs, exact mathematical certificates, independent audits, a passive drawing and public source references. Copied sources, dataset contents, executable programs, raw optimization streams and private coordination are excluded. All sibling dependencies are byte-pinned without duplicating their complete proofs here.
