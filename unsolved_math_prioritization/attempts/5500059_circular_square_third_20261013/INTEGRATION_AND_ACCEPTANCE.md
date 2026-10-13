# Integration and acceptance: third edition

## Accepted complete-square construction

The complete certificate has 49,594 bytes and SHA-256 b6642d19ad90e5e9325ecf629b5e48d2226b9598271e2120623556351dbd3ebe. It supplies 121 closed strictly convex positive-area polygons, all 7,260 pair separations, strict disk margins and exact full-square area. The [complete proof](THIRD_PASS_CONSTRUCTIVE_UPPER_BOUND.md) has 10,520 bytes and SHA-256 c96ae0ecb10cd2572786bdaa280fdaecd97ce6f55670ddc6bceed9ea82367a64. Its rational upper bound is strict: 1295864/1000000 = 1.295864.

The [fresh independent construction review](INDEPENDENT_CONSTRUCTION_REVIEW.md) binds these exact inputs and reviews the full geometry and topology. An independently written segment-arrangement checker computes all 7,260 pair intersections, obtaining 6,916 empty sets, eight points and 336 segments. No positive-area intersection occurs. Independent separating axes corroborate every pair. Integer comparisons verify all 2,760 convexity conditions, 696 indisk inequalities and 696 enclosing-disk inequalities. All 121 pairs of disk centers are independently checked and different in the given certificate.

The separate topology reconstruction verifies all intermediate face cycles and all 24 dihedrally related edge subdivisions. It does not assume that vertices initially placed on an old edge remain collinear after optimization. Topology provenance supports the explanation, while the final exact coordinate certificate and the closed-union proof establish coverage directly.

Seventeen hostile inputs are rejected, including a one-unit area-preserving interior-cell shift, and three benign order/relabeling transformations are accepted. The normal, -O and -OO results agree. The [producer replay](PRIOR_CHECKER_REPLAY.json) remains labeled as regression evidence from a previous independently authored checker; it is not substituted for the fresh mathematical review. Independent computational review is not human peer review.

## Separately accepted boundary closure

The full [unequal-angle proof](UNEQUAL_ANGLE_BOUNDARY_CLOSURE.md) and [fresh independent review](INDEPENDENT_BOUNDARY_THEORY_REVIEW.md) establish a finite disjoint polygon family covering all four sides at circularity at most G+epsilon for every epsilon>0. The open center remains uncovered. The proof includes the verified three-contact envelope branch, positive baseline-height sensitivity without tangency assumptions, exact complete-edge matching, a finite angle sequence, all global pair classes and finite polygonal approximation with fixed boundary endpoints.

The accompanying unchanged boundary certificate is 104,072 bytes, SHA-256 197d3db0d83859d542761d0fb4b57ba9b5c34aec4f35f09169f6d458db42dc2c. It gives 56 finite convex polygons with strict circularity below 64439/50000=1.28878, covering all four sides but only approximately 31.9451% of square area. The [fresh independent exact audit](INDEPENDENT_BOUNDARY_CHECK.json) checks eight canonical types, all 7,104 placed vertices, all 1,540 pairs, 56 matched full edges, 15 consecutive intervals per side, an exact positive area deficit and strict exclusion of the center from every cell. Its full pair data are retained. Thirteen hostile inputs fail and a benign canonical cyclic rotation passes.

This boundary-only achievement removes the earlier four side gaps. It proves no complete-square upper bound near G: the interior-completion problem remains open. In particular 1.28878 must never replace the separate complete-square upper 1.295864. The independent algebra and exact geometric outputs replay in normal, -O and -OO modes and accompany the complete mathematical reviews.

## Scope and unchanged dependencies

The first and second editions are unchanged sibling dependencies. Their complete mathematical and source-audit files are crosslinked and byte-pinned in the [public manifest](PUBLIC_MANIFEST.json). The third complete witness improves the second strict upper bound 1.296046 by 0.000182. Combining it with the unchanged lower theory gives G<=Gamma_fin<1.295864, where G=1.288684461870457901325875.... The fixed-N gap gamma>G+1/(192*25^(N+2)) tends to zero with N and does not strengthen the unrestricted infimum lower bound.

The exact optimum, unrestricted finite attainment and equivalence with infinite partitions remain unresolved. The third newly documented substantive investigation establishes at least three new passes in this continuation; the lifetime count remains unknown. No novelty or exhaustive-priority claim is made. Boundary-only families are not counted as full-square constructions.

## Text normalization and performed recovery

The full new construction proof, rational data, every pair record and every margin row are retained. Audit references to operational locations are normalized to public local or sibling links. Where a public text is normalized, every exact change is reversible and the complete original bytes are preserved. Programs, raw optimization data, copied sources and private coordination remain outside the public edition. Public hashes identify supplied mathematical artifacts, byte-pinned public dependencies or actual publicly identified scholarly sources; withheld operational hashes are not published.

The sealed edition is preserved by an actual compressed archive and a separate complete-file byte store. Both recovery routes are extracted and compared with the full inventory. Retained original source files are reconstructed from complete bytes independently on both routes, and the actual checking programs are rerun on those restored sources. Edition validation and semantic/hostile controls run against the original, archive-restored and byte-store-restored editions in normal, -O and -OO modes. The recovery receipt records those performed checks, exact-byte comparisons and final unchanged-byte verification. Merely creating an archive or rerunning only a live original is insufficient.

This edition supplies complete readable mathematical evidence and accepted partial results. It does not assert that the original optimization problem has been solved.
