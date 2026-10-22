# Independent review of the third authored square-circularity edition

Date: 13 October 2026. Problem 5500059 / AMR-054-0059 / TOPP 59.

## Verdict and exact edition

Accepted as a complete, reproducible edition of two explicitly bounded partial results. No blocking mathematical, editorial, scope, privacy or recovery defect was found. This is independent mathematical and computational review, not human peer review or a solution of the unrestricted optimization problem.

Acceptance binds the 29-file third edition identified by [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json), 14,993 bytes, SHA-256 `60b97f3a940c40f3f9296cc89bb54c66321aa86c90bc965555498474604618e8`. Its other 28 files have 4,093,232 bytes in total. The manifest excludes itself. This review is a separate acceptance artifact and does not silently change that frozen inventory.

The first and second editions remain unchanged siblings. All 48 of their public files, including both manifests and the complete proofs and mathematical reviews used here, are byte-pinned dependencies. Altering mathematical content or any bound acceptance identity requires renewed review.

The [complete 121-cell coordinate certificate](rational_partition_certificate.json) has 49,594 bytes and SHA-256 `b6642d19ad90e5e9325ecf629b5e48d2226b9598271e2120623556351dbd3ebe`. Its [complete construction proof](THIRD_PASS_CONSTRUCTIVE_UPPER_BOUND.md) is unchanged: 10,520 bytes, SHA-256 `c96ae0ecb10cd2572786bdaa280fdaecd97ce6f55670ddc6bceed9ea82367a64`.

The separate [56-cell boundary certificate](boundary_patch_certificate.json) has 104,072 bytes and SHA-256 `197d3db0d83859d542761d0fb4b57ba9b5c34aec4f35f09169f6d458db42dc2c`. Its [complete public boundary proof](UNEQUAL_ANGLE_BOUNDARY_CLOSURE.md) has 15,423 bytes and SHA-256 `e4b1cdc34d931d7bb403c677a5a6d63fad5f96d65d632f86cd577528953a7120`; only the dependency paragraph was converted to public sibling links.

## Mathematical conclusions and explicit limits

The complete construction partitions the entire closed square into 121 positive-area strictly convex polygons, with every true circumradius/inradius strictly below 1295864/1000000 = 1.295864. It improves the second edition's explicit bound 1.296046 by 0.000182. Disk centers are independent, and no tangency between neighboring indisks is imposed. These are comparisons of feasible constructions, not optimality or literature-priority claims.

Together with the unchanged lower theory, the accepted finite-partition bracket is

G <= Gamma_fin < 1.295864,

where G=1.288684461870457901325875.... The fixed-N inequality gamma>G+1/(192*25^(N+2)) has a correction tending to zero and does not imply a strict lower bound Gamma_fin>G. The exact optimum, unrestricted finite attainment, and equivalence with arbitrary infinite partitions remain open.

The unequal-angle theorem proves that, for every epsilon>0, a finite family of positive-area convex polygons with disjoint interiors can cover every square-boundary point with all ratios at most G+epsilon while leaving an open neighborhood of the center uncovered. The exact example has 56 finite polygons of ratio strictly below 64439/50000=1.28878, but covers only about 31.9451062% of square area. Neither statement is a square partition or a new complete-square upper bound. The whole-square bound remains 1.295864.

This is the third newly documented substantive pass in the present continuation. Earlier lifetime attempt counts are unknown. The edition does not reset an attempt budget, claim no earlier attempts, or assert novelty.

## Complete proof and dependency review

Both new complete proofs and both fresh independent mathematical reviews were read. The complete unchanged first-edition theory, second-edition quantitative obstruction and corner-chain proof, and their three complete mathematical reviews were also read. The lower constant, corner geometry and radius bounds used by the boundary theorem therefore remain supported by full accessible arguments rather than abbreviated excerpts.

The full-square reasoning is sound: all-vertex supporting inequalities give convexity; supporting lines separate every pair; exact areas sum to the square area; and the finite closed-union argument excludes an omitted point even on an edge or corner. The two witness-disk inequalities correctly give one-sided bounds on the actual inradius and circumradius without requiring either named center to be extremal. The finite maximum vertex distance is strictly smaller than the proposed outer radius, which justifies the strict upper inequality.

For the boundary theorem, the three positive constraint weights certify the unequal-angle envelope on its stated domain 41/50<=t<=u<=1. All square-root signs and the three-contact branch are valid there. The positive baseline-height derivative yields the support inequality without baseline or neighboring-indisk tangency assumptions. Internal tangency of the unique relaxed optimal circle excludes equality for a finite polygon. The reflected obstruction is understood on the reflected parameter domain, not asserted on an unchanged interval.

The second-intersection parameters give complete separator segments, and their scale relation matches the entire shared edge. The finite angle sequence ends at vertical separators. Its derivative and scale estimates retain the required circularity and uniform height bounds. The nonincident separation estimates cover same-side, reflected-side, adjacent-side, corner and opposite-side pair classes. They also prove a strict central gap. Retaining the baseline, separators and independent endpoint supports during sufficiently close finite outer approximation preserves full boundary coverage, incidence, nonoverlap and the central hole. This is a proof about finite polygons for each fixed epsilon, not a substitution of curved cells or an infinite limiting family.

## Fresh exact data verification

A new reviewer-written rational checker imports neither producer nor earlier audit programs. It independently rechecks all 240 vertices, 121 face cycles, every face's all-vertex convexity, every strict disk inequality and all 121 complete margin rows. The minimum convexity determinant is 1275918642918821626240; minimum squared indisk slack is 9607630465643177666148390959368892; minimum enclosing slack is 178213853016329475463288384. There are 696 incidences for each disk inequality. The exact doubled area is 8*10^24.

All 7,260 producer pair separators were independently checked for complete inventory and valid supporting half-planes. All 7,260 independent pair rows were separately checked by recomputing projection intervals and the exact intersections on a separating line. They give 6,916 empty intersections, eight points and 336 segments, and no positive-area intersection. The fresh source audit's different contained-vertex/segment-intersection algorithm and its full controls were also replayed. The topology source checker independently recovers the 100-to-105-to-121 face sequence, including all 24 subdivided edges. The final geometry is self-contained; this provenance check does not claim reconstruction of every edge of the published source figure.

For the boundary certificate the reviewer-written checker independently expands every exact rational similarity, reflection and rotation. All eight canonical types satisfy strict convexity, 960 indisk inequalities and 960 strict enclosing inequalities; tangency is permitted in the indisk inequalities. These produce 56 placed polygons and 7,104 placed vertices. Every polygon lies in the square and strictly excludes its center.

Both full sets of 1,540 boundary-pair records were independently checked. Exact projection and contact reconstruction gives 1,484 empty intersections and 56 shared full edges. The contacting-pair set exactly equals the adjacency induced by consecutive square-side intervals. Each side has 15 intervals, beginning at zero and ending at the exact side length. The complete rational area deficit and minimum center-exterior determinant were recomputed and agree with the audit. These checks positively certify the stated interior omission, rather than merely failing to prove coverage.

Both SVGs are passive illustrations. The partition's 121 ordered polygon lists equal its exact certificate coordinates. The boundary illustration has all 56 normalized placements, rounded only for display to twelve decimal places, and explicitly labels the uncovered interior. Exact deterministic reconstruction, passive-content checks and fresh visual render inspection passed. Neither illustration is used as a geometric proof premise.

## Editorial preservation and public-source boundaries

Every public file matches its manifest entry. All 28 complete source-to-public maps were independently reconstructed in both directions. Four files have editorial changes: removal of one withheld operational digest from the producer regression report, public-link normalization in the two mathematical reviews, and the boundary proof's dependency paragraph. The boundary review correctly rebinds the normalized proof's public byte count and hash. All mathematical statements, full certificates, every pair record and every face margin are preserved. Every local and transitive sibling link resolves to its pinned artifact.

The source/public distinction remains explicit. The producer's replay of a previously independent checker is labeled regression evidence and is not substituted for the fresh mathematical audit. Public mode metadata binds the actual supplied audit outputs. The public payload contains authored proofs, complete mathematical certificates and audits, passive drawings, and public bibliographic metadata. It excludes executable programs, copied source text or PDFs, dataset contents, raw optimization streams, private coordination and hashes identifying withheld operational material.

The existing [source audit](../5500059_circular_square_first_20261013/SOURCE_BOUND_AUDIT.md) remains unchanged. Actual retained PDF bytes for arXiv v1, arXiv v2 and the 2009 evolutionary study were independently recovered and matched their public sizes and SHA-256 identities; their title pages were freshly extracted. Current [arXiv v2 metadata](https://arxiv.org/abs/cs/0304023v2) confirms the authors, title, 8 February 2026 revision and expressly conjectural Section 5.4 status. The PDF's printed 10 February date remains distinct from submission metadata. [TOPP Problem 59](https://topp.openproblem.net/p59) currently lists the problem open and attributes 1.29950 to the complete 92-piece construction. This edition review does not claim a fresh whole-paper audit, exhaustive literature search or literature-priority certification.

## Performed independent recovery

Acceptance was withheld until final preparation and its successful recovery receipt were terminal. The reviewer independently extracted the actual compressed archive and separately reconstructed the complete per-file byte store into fresh locations. Both matched the sealed inventory, including every byte count, SHA-256 and file mode. All 301 retained source-file entries, comprising 259 distinct complete-byte objects, were independently reconstructed through each route. All 48 predecessor public files and the full predecessor inventories remained unchanged.

Across the two independent restoration routes, 72 normal/-O/-OO runs passed: final edition validation, 75 hostile/semantic rejections with seven benign controls, the new reviewer-written exact checker, and nine restored source programs. These include producer regression geometry, fresh partition and boundary geometry, topology, pair validation, both independent and author envelope algebra, author boundary geometry and author boundary controls. Outputs were byte-identical across optimization modes; the restored source outputs also matched their exact retained accepted baselines. Source geometry controls include area-preserving or boundary-preserving overlaps, so area or side coverage alone cannot produce acceptance.

No post-replay change was found in either restored edition, any retained original source or the live sealed edition. These are completed present-day recovery and execution tests, not inferred historical runs. Full proof and witness preservation, reversible normalization and actual restoration support the accepted edition while leaving the original global problem unresolved.
