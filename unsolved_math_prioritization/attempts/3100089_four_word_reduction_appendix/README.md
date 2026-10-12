# Necessary reductions for a hypothetical four word disconnection

This third prose appendix for database problem 3100089 (AMR-030-0089) contains a complete accepted reduction and its complete mathematical audit. It narrows the possible form of a disconnected original-threshold pressing instance with exactly four successful words. It does not prove that such an instance exists, or settle all four-word cases.

It accompanies the [normalization report](../3100089/README.md), [full-state and trajectory-fiber results](../3100089_positive_connectivity_appendix/README.md), [short-neighbor and terminal-coordinate appendix](../3100089_short_neighbor_terminal_appendix/README.md), and [rank-six and unique-overlap appendix](../3100089_rank_six_overlap_appendix/README.md).

## What the reduction proves

All matrices are finite, symmetric, and over F₂. A successful word clears the entire matrix and has length r=rank(A). The original adjacency threshold LCS≥r−4 permits at most four deletions and at most four insertions. Delete the initially zero rows and columns, which can never be pressed. Let m be the remaining number of coordinates, let e=m−r, and let Z be the number of successful words.

Every exact-trajectory fiber has at least e+1 words and lies in one original-threshold component. The accepted short-neighbor theorem separately excludes singleton components in a nonunique instance. Consequently a disconnected instance requires Z≥2 max(2,e+1). If Z=4, then e≤1: all cases with at least two extra nonzero coordinates are excluded in arbitrary rank.

In corank one, e=1, each fiber has two words and becomes one edge of an omission multigraph. A disconnected four-word instance must have exactly two disjoint omission edges. Its four endpoint restrictions are full rank and uniquely pressable, and its coordinate configuration must be the union of two uniquely pressable instructional roots that differ genuinely in one column.

These are necessary conditions only. Two disjoint omission edges do not imply that the full original-threshold graph is disconnected. The suggested statement that every such one-column union has only its original trajectory is unproved. The full-rank four-word case, m=r, also remains unresolved by this reduction.

The separately accepted arbitrary-ambient rank-at-most-six result excludes both residual configurations in ranks at most six. The remaining cases here have rank at least seven. The general original-threshold conjecture remains open in rank seven and above; no four-word classification or novelty claim is made.

## Complete texts and evidence

- [Complete four-word reduction](FOUR_WORD_REDUCTION.md)
- [Complete mathematical audit](FOUR_WORD_REDUCTION_AUDIT.md), including the explicit rank-deficient counterexample to an unrestricted omission-degree identity
- [Accepted scope and limitations](ACCEPTANCE.md)
- [Editorial changes and publication scope](PUBLICATION_SCOPE.md)
- [Public source metadata](SOURCE_METADATA.json) and [closed manifest](MANIFEST.json)

The arbitrary-rank arguments are symbolic. The audit’s complete bounded checks through order five corroborate them; the bounded absence of disjoint omission edges is not used to prove rigidity or a classification. These AI-assisted reviews are unrefereed, not external human peer review or proof-assistant certification. No executable programs or raw verification collections are distributed.
