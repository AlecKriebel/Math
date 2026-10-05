# Source and prior-work review

Checked October 5, 2026. This is a bounded literature review, not certification that no solution exists anywhere.

## Primary target

Miklós Abért, [Some questions](https://www.renyi.hu/~abert/questions.pdf), November 2, 2010, Question 5 on printed page 2, credited to Abért and Bálint Virág. The cover date and relevant question were visually checked. The object is the full depth-n binary-tree automorphism group. The question asks for its minimum law length and suggests the power word of length 2^n. It is more specific than merely requesting an asymptotic order.

The catalog landing page was attempted first. Web retrieval was unavailable; a direct request subsequently returned HTTP 403. No attempt was made to bypass that denial. Identification instead uses the author-hosted primary PDF and verified pinned public data.

## Direct later treatment

Henry Bradford, [Quantifying lawlessness in finitely generated groups](https://doi.org/10.1515/jgth-2022-0113), Journal of Group Theory 27(1) (2024), 31–59. The inspected [author manuscript](https://api.repository.cam.ac.uk/server/api/core/bitstreams/fd15be02-36ce-4a0d-8a47-2653cd3c8715/content) is dated June 14, 2023. Proposition 6.4 supplies the constructive linear lower bound; Question 10.3 leaves the shortest-law problem open and discusses the power-word candidate. Its W_n has n+1 wreath factors. Our Proposition 3 is credited to this result. The journal metadata was checked against the author's publications page; the final journal article itself was not retrieved.

## Later papers with related titles or methods

Henry Bradford and Jacob Willis, [Groups of arbitrary lawlessness growth](https://arxiv.org/abs/2503.23582), v2 dated April 12, 2026. The full PDF was retrieved and its introduction, definitions, Lemma 2.6, sparse-wreath construction and principal results inspected. It constructs finitely generated infinite groups with prescribed lawlessness growth; the inspected statements do not determine L_n for the finite binary wreath tower. The appearance of wreath products is not a resolution of this target.

Jorge Fariña-Asategui, [On a question of Abért and Virág](https://arxiv.org/abs/2505.23142), submitted May 29, 2025; the public record identifies a 2026 Proceedings of the American Mathematical Society online-first publication. The inspected arXiv manuscript's Question 1 concerns dimensions of normal subgroups of positive-dimensional tree groups. Theorem A gives counterexamples to that question; Theorem C and Corollary 5 treat self-similarity and qualitative lawlessness. None of these statements gives the finite-depth minimum here. The similar title must not be counted as a solution of Question 5.

Abért and Virág, [Dimension and randomness in groups acting on rooted trees](https://www.math.toronto.edu/~balint/tg14.pdf), inspected author manuscript dated February 11, 2003; published in Journal of the American Mathematical Society 18 (2005), 157–192. Its word-map discussion, especially Proposition 4.1 and Theorem 4.4, concerns random infinite-tree actions and dimensions of word-map kernels. Qualitative lawlessness alone does not give the sharp finite-depth rate.

## Correction to the imported prior analysis

The complete pinned prior-report corpus contains an entry for AMR-011-0005. It identifies the same target and does not claim a solution. Its comparison of generic small-group law bounds with 2^n uses incompatible size parameters.

Andreas Thom, [About the length of laws for finite groups](https://arxiv.org/abs/1508.07730), inspected v2 dated September 5, 2015, Proposition 3.1 gives an O((log M)^(3/2)) bound for nilpotent groups of size at most M; Proposition 3.2 gives O((log M)^(9/2)) for solvable groups. Since |W_n| = 2^(2^n-1), these bound expressions become O(2^(3n/2)) and O(2^(9n/2)), respectively. They therefore do not improve the elementary O(2^n) power-law upper bound. This is a scale comparison of available guarantees, not a lower bound on every word obtained by those methods.

## Actual repository checks

The inspected main snapshot was 6144d964777214c6963a915288c18fcf97b42026. Its 62-entry attempts directory has no entry for 1200005. Exact numeric-ID and code searches found no matching PR, and numeric-ID commit and branch searches found none. A title search found no matching PR. Broader wreath-product PR results concern different targets. The related-target grouping file contains no selected target. Default-branch code search found no selected indexed result; that alone is not absence evidence. The actual queue row is queued / 0/5, separately from these searches.

The public source record and prior-report entry were read in full from corpus bytes matching the repository's immutable manifest. No claim is made about deleted refs, unpublished working trees, private attempts, or unindexed content. The supplied context did not identify an additional private attempt.

The most relevant currently inspected later source still states the exact question rather than resolving it. This investigation independently produces only the scoped partial results and finite certificates in the accompanying proofs. Historical novelty and present worldwide open status are not asserted.
