# Spherical lifts: accepted approach-1 partial results

**The original problem remains UNRESOLVED after approach 1 (1/5).** This proof-only edition preserves the complete authored mathematical report and full independent mathematical audit. It supplies no new square-root upper bound or fixed-dimensional super-square-root lower bound and makes no novelty claim.

Problem 30004900 / OWR-8415356-006 asks whether, in every fixed dimension d, every n-vertex convex polytope inscribed in one Euclidean sphere has extension complexity O_d(sqrt(n)). The source permits constants depending on dimension and imposes no distribution condition on the vertices.

## Accepted partial result

Every full-dimensional d-polytope with n ≥ d+2 vertices is a coordinate projection of a full-dimensional inscribed (d+1)-polytope with exactly n vertices. Choose a sphere radius larger than all input vertex norms, lift each vertex using the square-root height, and choose the sign at one extra vertex to ensure full dimension. Radial exposure proves that all n lifted points are vertices.

Projection monotonicity then gives F_d(n) ≤ I_(d+1)(n), where F and I are the unrestricted and inscribed extremal extension complexities. Together with class inclusion, this makes the two square-root conjecture families, each quantified over every fixed dimension, equivalent. In particular, the inscribed three-dimensional assertion would imply the square-root bound for every polygon.

The dimension shift is essential. This does not establish a same-dimension equivalence or a constant uniform in dimension. The simplex case n=d+1 is excluded from the dimension-raising lift and handled separately by the simplex extension bound.

The same construction puts at least n−1 vertices into any fixed positive-radius spherical cap after scaling. It shows why inscription alone does not supply well-distributed vertices. This is an obstruction to directly transferring methods that need such distribution, not a counterexample to the conjectured bound.

## Reading order

- [APPROACH1.md](APPROACH1.md): the full report and self-contained proofs, unchanged after an edition notice.
- [AUDIT.md](AUDIT.md): the complete mathematical audit, including every edge case, quantifier check and source distinction.
- [SOURCE_LEDGER.md](SOURCE_LEDGER.md): bibliographic facts and historical inspection limits.
- [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json): public scholarly metadata and raw public PDF identities.
- [ACCEPTANCE.json](ACCEPTANCE.json) and [STATUS.json](STATUS.json): the accepted scope, exact unresolved gap and unchanged 1/5 accounting.
- [PROVENANCE.md](PROVENANCE.md): the precise editorial and publication boundary.
- [MANIFEST.json](MANIFEST.json): exact file membership, sizes and hashes for this edition.

## Source scope

The question is in Sauermann's contribution, joint with Kwan and Zhao, to [Oberwolfach Report 53/2021, printed p. 2929](https://ems.press/content/serial-article-files/46931), published in 2022. The established cyclic-polygon result settles dimension two. Kwan–Sauermann–Zhao's random-sphere theorem is probabilistic, and their near-linear lower bound allows the dimension to grow. Neither settles the remaining universal fixed-dimensional question. The source comparison with Shitov's published 147 n^(2/3) polygon bound is limited to the checked theorem statement and publication metadata; it is not presented as a best-available bound.

All retrieval and inspection statements describe the original research and audit on 9 October 2026. Edition preparation did not repeat the PDF retrievals, hash checks, source reading or literature review. The bounded status and attribution checks do not establish exhaustiveness or originality.

## Edition and acceptance boundary

All mathematical report text is unchanged. All mathematical audit paragraphs and substantive source findings are retained; only its original input inventory and administrative history wording are edited. Original private or auxiliary file identities are excluded. Public raw-PDF hashes and sizes are retained without local paths. Copied source documents, renderings, extracted source text, datasets, check programs, fixtures, private sources, private personal data and private coordination material are excluded.

The accepted reduction is proved analytically. No numerical experiment is used to justify a universal statement. This independent AI-assisted audit is not human peer review, journal acceptance or formal proof-assistant verification. Preparing this edition adds no proof-search approach, changes no turn count and edits no queue file.
