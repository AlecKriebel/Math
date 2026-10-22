# Most Circular Partition of a Square: second authored edition

Problem 5500059 / AMR-054-0059 / TOPP 59. Status: unresolved. Date: 13 October 2026.

This is the second newly documented substantive investigation in the present continuation. The earlier lifetime attempt count is unknown. This label does not establish that no earlier investigations occurred, reset a budget, or imply that an attempt limit has been reached. The first authored edition remains unchanged.

## Complete-square upper-bound witness

The [complete construction proof](IMPROVED_CONSTRUCTIVE_UPPER_BOUND.md) gives a finite partition into 100 positive-area closed convex polygons with worst circularity strictly below

648023/500000 = 1.296046.

The ratio is the smallest-enclosing-circle radius divided by the largest-inscribed-disk radius. Each cell has its own independent rational witnesses for the two centers. Neither coincident centers nor tangency of neighboring indisks is required.

The rational bound improves the first edition's 1.298322 by 0.002276 and the identified source-reported complete-square bound 1.29950 by 0.003454. The new topology splits each of four diagonal octagons in the previous layout into three polygons. The underlying earlier layout is credited to Figure 16 of Damian and O'Rourke, [arXiv cs/0304023v2](https://arxiv.org/abs/cs/0304023v2). This is a comparison of explicitly identified feasible bounds, without an exhaustive-literature or global novelty claim.

All square points, including the interior and boundary, are covered. The proof uses 201 rational vertices, 100 face cycles, 100 pairs of independent disk-center witnesses, all 4,950 separating supports, strict convexity and disk inequalities, and exact area. The finite closed-union argument upgrades equal area to pointwise full-square coverage.

## Reading order

1. [Complete construction proof](IMPROVED_CONSTRUCTIVE_UPPER_BOUND.md), [complete coordinate and disk certificate](rational_partition_certificate.json), and [passive illustration](partition.svg).
2. [All 4,950 pair separators](pair_separation_witnesses.json), [all 100 margin rows](exact_face_margin_table.json), and [exact verification summary](exact_verification_summary.json).
3. [Fresh independent construction acceptance](INDEPENDENT_CONSTRUCTION_REVIEW.md), [exact audit](INDEPENDENT_EXACT_CHECK.json), [all independent pair-intersection results](independent_pair_intersections_and_separations.json), [hostile control outcomes](INDEPENDENT_CONTROL_CHECK.json), and [topology provenance](TOPOLOGY_PROVENANCE_CHECK.json).
4. [Complete finite-complexity proof](QUANTITATIVE_COMPLETION_OBSTRUCTION.md), [independent mathematical review](INDEPENDENT_QUANTITATIVE_REVIEW.md), [independent exact algebra](INDEPENDENT_GAP_ALGEBRA.json), and [author's exact algebra controls](QUANTITATIVE_ALGEBRA_CONTROLS.json).
5. [Complete corner-chain and bridge appendix](CORNER_CHAIN_AND_BRIDGE_OBSTRUCTION.md), [its separate independent acceptance](INDEPENDENT_CORNER_CHAIN_REVIEW.md), [independent exact chain algebra](INDEPENDENT_CHAIN_ALGEBRA.json), and [author's chain algebra controls](CORNER_CHAIN_ALGEBRA_CONTROLS.json).
6. [Earlier independent-checker replay](INDEPENDENT_CHECKER_REPLAY.json), [complete checking guide](CERTIFICATE_GUIDE.md), [scholarly source identities](SOURCE_IDENTITIES.json), [fresh bounded source check](SOURCE_RETRIEVAL_METADATA.json), [integration and acceptance](INTEGRATION_AND_ACCEPTANCE.md), and [public byte manifest](PUBLIC_MANIFEST.json).

The changed construction and the quantitative finite-N theorem have independent mathematical and computational acceptance. These checks are not human peer review. The earlier producer replay remains separately identified.

## Explicit finite-complexity obstruction

Let G=1.288684461870457901325875... be the balancing constant defined and proved in the [unchanged first-edition foundation](../5500059_circular_square_first_20261013/THEORY_REPORT.md). Every square partition into at most N positive-area compact convex cells satisfies

gamma > G + 1/(192 * 25^(N+2)).

The [complete proof](QUANTITATIVE_COMPLETION_OBSTRUCTION.md) first bounds each cell by N+3 sides, proves an explicit eccentric-annulus slack, and propagates that slack through a boundary-crossing envelope. It permits different disk centers and does not require adjacent indisks to touch. Arbitrary compact convex cells in a finite partition are reduced to polygons by the proved side-count argument.

The correction is very weak and tends to zero as N grows. It quantifies the first edition's fixed-N strict gap, without improving the unrestricted finite-partition lower bound. For the infimum Gamma_fin over all finite admissible partitions, the combined accepted results give

G <= Gamma_fin < 1.296046.

The strict construction maximum makes the upper inequality strict. The per-partition lower inequalities do not imply Gamma_fin>G. The first edition's [independent theory acceptance](../5500059_circular_square_first_20261013/INDEPENDENT_THEORY_REVIEW.md) and [bounded source audit](../5500059_circular_square_first_20261013/SOURCE_BOUND_AUDIT.md) remain byte-identical dependencies, not newly redone first-pass results.

## Corner-chain attachment and restricted bridge obstruction

The separately accepted [appendix](CORNER_CHAIN_AND_BRIDGE_OBSTRUCTION.md) attaches the earlier favorable local junction to corner cells, repeats it for any finite chain length, and places four disjoint corner-and-side patches in one square. Finite convex polygonal approximations have ratios at most G+epsilon for every epsilon>0. They leave four middle side gaps and an interior region uncovered. They are not full-square partitions or upper-bound witnesses for the complete-square problem.

Connecting the prescribed reflected constant-angle chains with one boundary cell forces that cell's ratio to be at least 1+1/(4t0^2)>1.36. This is a restricted obstruction for those separator directions; it does not exclude changing the chain angles, inserting multiple bridge cells, or using a different global layout. The complete proof and separate independent review preserve these limits.

## Scope

The exact optimum and attainment over unrestricted finite cell counts remain unresolved. All full-square claims concern finite positive-area compact convex polygonal partitions, with pairwise disjoint interiors and unrestricted Steiner points. No equivalence with an arbitrary infinite partition is assumed. A construction certificate supplies an upper bound; it is not a lower-bound or global optimization certificate.

This authored edition contains proofs, mathematical certificates, an illustration, audits and public scholarly metadata. It excludes copied source documents, source text, datasets, programs, raw optimization streams and private coordination.
