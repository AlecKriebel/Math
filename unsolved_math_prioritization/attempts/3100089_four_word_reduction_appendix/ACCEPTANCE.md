# Accepted reduction and unresolved cases

The full four-word reduction was independently accepted without a mathematical correction. Its complete proof and audit are preserved in this prose edition with only the reference and publication-scope changes described separately. The review is AI-assisted and unrefereed, not proof-assistant verification, external human peer review, or a novelty assessment.

## Exact accepted statements

After deleting permanently zero coordinates, write m for the number of surviving labels, r for full binary rank, e=m−r, and Z for the nonempty successful language size.

1. Every exact trajectory fiber and every original-threshold component contains at least e+1 words. A disconnected nonunique instance therefore has Z≥2 max(2,e+1), using the accepted short-neighbor theorem to exclude singleton components.
2. For a selected full-rank coordinate basis B, Z(A)≥(e+1)Z(A[B]). The full-rank condition is essential: successful local words lift to full success because exactly r legal presses exhaust the ambient rank.
3. When e=1, every trajectory fiber has exactly two words. Fibers define a loopless omission multigraph with Z/2 edges, allowing parallel edges. Vertices are only labels omitted by some successful word. On that domain, the degree of v is the number of successful words of the full-rank restriction omitting v.
4. Every omitted label belongs to the support K of the unique nonzero kernel relation. A fiber pairs an omitted label with the last selected label in K. Labels outside K are never omitted.
5. If Z=4 and the original-threshold graph is disconnected in corank one, its omission multigraph must be exactly two disjoint edges. Every endpoint has degree one, so each corresponding full-rank principal restriction is uniquely pressable.
6. That necessary configuration is a one-column union: two uniquely pressable instructional roots in the Cooper–Whitlatch class agree in every column except one, and their alternate columns are genuinely different. The combined coordinate configuration must possess an additional trajectory with a disjoint omission pair.

The complete audit preserves the explicit matrix with row masks (5,2,5), the Gram matrix of e₀,e₁,e₀. No full word omits label 1, but deleting it gives a rank-one restriction with two successful one-letter words. This proves that the omission-degree identity cannot be extended indiscriminately to rank-deficient restrictions.

## Statements not established

The two-disjoint-edge omission condition is not sufficient for original pressing disconnection. The omission multigraph records only guaranteed within-basis and within-fiber routes; other original-threshold edges could join its components.

The proposed one-column-union trajectory rigidity statement is unproved. Neither full-rank four-word connectivity nor a classification of four-word languages is proved. No counterexample to original Bixby–Flint–Miklós connectivity is produced, and no novelty claim is made.

For a hypothetical disconnected four-word instance, e≥2 is excluded. The remaining forms are e=0, a nonsingular full-coordinate matrix, and e=1 with the necessary disjoint-edge and one-column-union structure. The independent arbitrary-ambient rank-at-most-six result already excludes both forms at ranks at most six. Thus the residual cases have rank at least seven, where the general original-threshold conjecture remains open.

The accepted eight-vertex example in the preceding appendix is full rank and has a connected original four-cycle. It obstructs only the specified unique-overlap move strategy and supplies no original-conjecture counterexample.

## Verification scope

The audit independently checked every symmetric binary matrix of orders zero through five: 33,867 matrices in total. It reports 31,743 pressable matrices, 282,731 successful words, and 202,175 full trajectory fibers, with complete Cartesian-product checks and the detailed basis, omission, kernel, terminal-pair, and root comparisons retained in the full audit.

Among the 1,662 corank-one four-word matrices in that bounded family, none had a disjoint-edge omission graph. This is a bounded fact only and proves neither rigidity nor any arbitrary-rank classification. The 384 genuinely distinct alternate columns among 1,646 uniquely pressable endpoint comparisons show that the root comparison test was nonvacuous.

Five mathematical negative controls and empty-rank conventions were checked. Normal Python, -O, and -OO executions agreed except for their recorded optimization flags. Explicit exceptions enforce the checks. The programs and raw verification records are not distributed, so this prose edition alone is not an executable reproduction bundle. The arbitrary-rank reduction rests on the preserved symbolic arguments, not extrapolation from these checks.
