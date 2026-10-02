# Independent review request: complete 30006078 packet

Please audit the full source-to-proof chain of all five frozen turns. Proposed disposition is **original unresolved5/5**, with only the scoped partial results in FINAL_RESULT.md.

## Primary source and dependencies

- Official OWR45/2024 PDF: https://ems.press/content/serial-article-files/50758. Petrov contribution with Pan, printed2656–2658, physical36–38; exact question2658.
- Current author excerpt: https://sasha-pt.github.io/papers/pdf/ow_2024.pdf.
- Huber–Kings math/0612611, primitive alternating-trace classes and Lazard/regulator comparison.
- Pappas2006.03668v3 §4.4.2, stable regulator classes.
- Petrov2012.13372v3, Theorem2.4, Proposition3.5, Lemma3.6, Proposition5.1, Proposition7.2 and Corollary7.3.
- Bloch–Kato *L-functions and Tamagawa numbers of motives*, Proposition3.8, Corollary3.8.4, Example3.9, Definition3.10: https://virtualmath1.stanford.edu/~conrad/BSDseminar/refs/BKTamagawa.pdf.

SOURCE_MANIFEST.json and SOURCE_ADDITION_T3.json bind local-only source bytes. The original PDF and source-page-36/37/38.png are in the sibling author source directory, along with full downloaded cited papers and rendered Petrov Proposition5.1 / Bloch–Kato pages. No raw-source upload is requested.

## Highest-risk points to check independently

1. Exact source coefficients, all finite K versus Q_p-only scope, and properness. The report's arbitrary-generator language must be reconciled with the stable primitive regulator convention used here. Degree-one sign normalization remains explicitly unproved.
2. Turn1's passage from block upper triangular trace identities through natural Lazard comparison and finite-index restriction; relative HT subquotient exactness and finite étale de Rham trace descent.
3. Turn2's use of Petrov's filtered flat bundle over K_infinity, proper GAGA after scalar extension, the ungraded identification with D_HT, and distinction between unweighted and weighted Chern characters. Tensor mixed-term cancellation and dual sign.
4. Turn3's twists and spectral-sequence filtrations. Projective-space kernel dimension; elliptic-square cycle matrix, Hodge-weight complement, incoming differentials, rank4/kernel2. No local-system realization is claimed.
5. Turn4's actual continuous determinant root, finite-cover smallness when p|rank, rational-point normalization and HT rigidity. The resulting residual geometric character is finite. Check the precise rationally split commuting-algebra hypothesis; do not promote to arbitrary coefficient fields.
6. Turn5's compatibility of the report's top-degree calculation with trace(alpha), the naturality under smooth complete intersections, rational divisor spanning, and the difference between numerical annihilation and vanishing of a full de Rham class. The top case is credited, not a new proof or a K-generalization.

Please reproduce every author receipt and verify historical manifests, then perform genuinely separate mathematical/algebra controls. The frozen author files should not be edited in place; report mandatory corrections for an additive correction packet. No sixth author search is authorized. The final author manifest binds the entire review candidate; its verified remote WIP head will be supplied with the handoff.
