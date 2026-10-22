# Rank six connectivity and an obstruction to unique overlap iteration

This second prose appendix for database problem 3100089 (AMR-030-0089) presents two accepted partial results with their complete mathematical audits. It accompanies the [normalization report](../3100089/README.md), [positive-connectivity appendix](../3100089_positive_connectivity_appendix/README.md), and [short-neighbor and terminal-coordinate appendix](../3100089_short_neighbor_terminal_appendix/README.md) for [draft PR #1313](https://github.com/AlecKriebel/Math/pull/1313).

## Results and exact scope

All matrices are finite, symmetric, and over F₂. A legal press at a current diagonal-one coordinate v updates the full matrix M to M+(Me_v)(Me_v)ᵀ. A successful word clears the full matrix and has length r=rank(A). The original threshold is LCS≥r−4, allowing at most four deletions and at most four insertions.

1. Every successfully pressable rank-six matrix, with any finite number of labelled coordinates, has a connected original-threshold successful-word graph of diameter at most six. The proof handles omitted labels, duplicate quotient vectors, zero coordinates, and singular ambient matrices. Together with the previously accepted lower-rank theorem, original-threshold connectivity holds in every rank at most six.
2. A specified eight-vertex matrix has exactly four successful words. Its graph under all contiguous substitutions with uniquely pressable one-end instructional-root truncations has two disjoint edges, even without an edit-budget restriction. Its original-threshold graph is a connected four-cycle. Thus iterating only those unique-overlap moves cannot establish general connectivity.

The rank-six proof uses a symbolic arbitrary-ambient reduction followed by a completely checked finite positive lemma covering 98,304 root/vector pairs and 98,306 edges. Its mathematical dependencies are the accepted full-state/fiber lemmas and terminal/signature theorem, including the imported Bixby–Flint–Miklós pressability-existence theorem. It does not use the short-neighbor theorem. The finite lemma is computer-assisted and the raw witnesses are not distributed in this prose edition; every positive replay cannot be reproduced from these prose files alone.

The obstruction is fully hand-checkable from its four words and complete 18-row reduced branch tree. It obstructs a specified proof strategy and is not a counterexample to the original conjecture. The general original-threshold conjecture for rank seven and above remains open. No classification of all four-word languages or novelty claim is made.

## Complete texts

- [Arbitrary-ambient rank-six proof](RANK_SIX_CONNECTIVITY.md)
- [Complete rank-six acceptance audit](RANK_SIX_AUDIT.md)
- [Exact finite verification contract](FINITE_VERIFICATION_CONTRACT.md)
- [Unique-overlap obstruction proof](UNIQUE_OVERLAP_OBSTRUCTION.md)
- [Complete obstruction audit](UNIQUE_OVERLAP_AUDIT.md)
- [Acceptance and limitations](ACCEPTANCE.md)
- [Editorial changes and publication scope](PUBLICATION_SCOPE.md)
- [Public source metadata](SOURCE_METADATA.json) and [closed manifest](MANIFEST.json)

The audits are AI-assisted and unrefereed. They are not proof-assistant certification, external human peer review, or a novelty assessment. This appendix is a complete prose edition of the two proofs and substantive audits, not an executable reproduction bundle.
