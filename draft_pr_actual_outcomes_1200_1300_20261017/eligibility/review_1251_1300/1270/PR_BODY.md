## Credited negative resolution

Publishes the proof reconstruction, mathematical audit, scoped acceptance, and public verification metadata for **2200014 / AMR-021-0014**, Conjecture 9 in Shapiro's polynomial problem list.

The conjecture is false. **Katkova, Shapiro and Vishnyakova (2024)** are credited for the disproof and primitive family in [In search of Newton-type inequalities, Section 5](https://arxiv.org/pdf/2403.12200v1#page=20). Their work was published in *Journal of Mathematical Analysis and Applications* 538(1), article 128349, [DOI 10.1016/j.jmaa.2024.128349](https://doi.org/10.1016/j.jmaa.2024.128349).

Our exact degree-24 reconstruction is
`R(x) = (38x^2 - 188x + 326) product_{j=1}^{22}(10^6 x + 10^6 + j)`.
It has strictly positive integer coefficients and exactly **22 distinct simple negative real roots**, while the selected weighted-index parity sequence has **at most 20 changes**. This disproves the bound both for distinct roots and for roots counted with multiplicity.

## Exact scope and proof

For a real polynomial of actual degree n with every coefficient strictly positive, the statistic is `c_k = (k+1)a_k^2 - k a_{k-1}a_{k+1}`, with the two auxiliary endpoint coefficients zero. Only strictly positive c_k are retained, in increasing index order; the count is of consecutive parity changes, with no cyclic closing comparison.

The full self-contained symbolic proof includes the compact coefficient formula, explicit uniform relative perturbation bound below 1/2000, robust weighted-sign inequalities, parity-subsequence argument, and complete root factorization. No omitted arithmetic program, table, or numeric certificate is needed. The audit's exact parity equality of 20 and complete sign pattern are supplemental finite cross-checks; the sufficient symbolic bound already proves the counterexample.

[Shapiro's original Conjecture 9](https://arxiv.org/pdf/1503.05295v1#page=4) is credited there to Forsgård and Shapiro. No novelty, construction-priority, or minimum-degree claim is made.

The finite-product endpoint correction applies **only to the inspected arXiv:2403.12200v1**. The publisher PDF was not inspected. The corrected finite formulas have the same limiting values, and the self-contained proof does not depend on the misindexed products.

## Review and verification limits

This proof reconstruction and separate mathematical audit are AI-assisted. Acceptance does not establish external human peer review, journal acceptance of this reconstruction, or formal proof-assistant certification.

- Exactly **seven files, 184,894 bytes**, added under `unsolved_math_prioritization/attempts/2200014/`.
- The complete normalized symbolic proof is preserved. The exact editorial map records the formatting and disclosure changes; all 38 displayed equations in the proof and audit are byte-identical to the audited originals.
- Recorded export-integrity validation passed normal Python, -O and -OO, with 25 tamper cases rejected in all three modes. The final normal-mode check was repeated before upload. Integrity checks do not independently prove the mathematics.
- All seven remote files were read back in full and matched the approved UTF-8 content and Git blob identities. Root and ancestor trees match the exact expected tree; every sibling and `QUEUE.md` is unchanged.
- Public manifest SHA-256: `24950d55b9b2f98b5622ea0adc5940d0d07a69d54535a0b0a626482f67f2fc55`.
- Commit: `04d220746dd5e5475c821ac1c2626e7ac5d3d884`.
- Exact Git tree: `eaaf3bc643895c22fe1475c939149bdda15a4d33`.

This public edition excludes copied source documents/text/images, datasets, raw coefficient and weighted-difference arrays, programs, numeric certificates, and private coordination material. Source hashes, byte counts, public URLs, match results, and retrieval/inspection boundaries are recorded as metadata.

This is a draft publication. GitHub CI is separate from local integrity validation; zero actual CI jobs means **NOT_RUN**, not a passing result.
