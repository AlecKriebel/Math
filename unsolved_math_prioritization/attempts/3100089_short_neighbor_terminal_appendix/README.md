# Short neighbors and terminal black coordinates for successful pressing

This appendix for database problem 3100089 (AMR-030-0089) contains complete proofs and substantive mathematical audits of two further partial results. It supplements the existing [normalization report](../3100089/README.md), [positive-connectivity appendix](../3100089_positive_connectivity_appendix/README.md), and [projection obstruction](../3100089_projection_obstruction/README.md) associated with [draft PR #1313](https://github.com/AlecKriebel/Math/pull/1313).

## Results and exact thresholds

All matrices are finite, symmetric, and over F₂. A legal press at a current diagonal-one coordinate v changes M to M+(Me_v)(Me_v)ᵀ. A successful word clears the full matrix and has length r=rank(A). The original threshold LCS≥r−4 permits up to four deletions and up to four insertions, not four operations total.

1. Every successful word in a nonunique successfully pressable matrix has a distinct successful word with LCS≥r−4, in arbitrary rank and ambient dimension. Four is sharp. This excludes isolated words and proves original-threshold connectivity whenever there are at most three successful words.
2. Original-threshold connectivity follows for nonsingular matrices of rank at most six. In rank six it also holds when the distinct nonzero quotient-coordinate images form a basis, allowing arbitrary duplicates and zero coordinates. No assertion is made for arbitrary ambient rank-six configurations with extra distinct quotient directions.
3. An initially black coordinate v is last in every successful word containing it if and only if Ae_v=diag(A), equivalently its radical-quotient image is the canonical vector. The converse is constructive and includes both parity branches in the full ambient matrix.
4. At the auxiliary threshold LCS≥2, separated components impose two precise signature families on cross-component successful first labels; the only rank-six strings are 011111, 101111, and 100011. Failure of the signature gives a constructive bridge of at most four auxiliary edges.

The auxiliary threshold agrees with the original threshold exactly at rank six. Above rank six, its bridge theorem is weaker and does not prove the original conjecture. The general original connectivity conjecture remains unresolved by these results. No novelty claim is made.

## Complete texts

- [Short-neighbor proof](SHORT_NEIGHBOR_THEOREM.md), all nine sections
- [Short-neighbor audit](SHORT_NEIGHBOR_AUDIT.md), including the self-contained arbitrary-ambient reconstruction and full proofs of the three-word, nonsingular rank-six, and basis-plus-duplicates corollaries
- [Terminal-coordinate proof](TERMINAL_COORDINATE_THEOREM.md), all five sections including the constructive auxiliary bridge
- [Terminal-coordinate audit](TERMINAL_COORDINATE_AUDIT.md), including complete proof review, aggregate computational scope, and explicit hypothesis counterexamples
- [Acceptance and precise limitations](ACCEPTANCE.md)
- [Editorial changes and external-input scope](PUBLICATION_SCOPE.md)
- [Public source metadata](SOURCE_METADATA.json) and [closed artifact manifest](MANIFEST.json)

The reviews are AI-assisted and unrefereed, not external human peer review or proof-assistant certification. Two named external inputs are used: Cooper–Whitlatch's unique-pressability characterization and Bixby–Flint–Miklós's pressability-existence theorem. Neither is reproved here; no withdrawn connectivity theorem is imported. Finite computations corroborate the full symbolic proofs and are not extrapolated to arbitrary order. This prose edition is not a self-contained executable reproduction bundle.
