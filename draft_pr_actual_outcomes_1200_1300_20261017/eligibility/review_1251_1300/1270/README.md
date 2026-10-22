# Credited negative resolution of the weighted parity conjecture

Problem 2200014 / AMR-021-0014, Conjecture 9 in Shapiro's polynomial problem list.

The conjecture is false. Katkova, Shapiro and Vishnyakova, *In search of Newton-type inequalities* (2024), Section 5, are credited for the disproof and primitive family. This edition gives an exact finite reconstruction and an explicit simple-root perturbation. It makes no novelty, construction-priority, or minimum-degree claim.

The integer polynomial

\[
R(x)=(38x^2-188x+326)\prod_{j=1}^{22}(10^6x+10^6+j)
\]

has actual degree 24, all coefficients strictly positive, and exactly 22 distinct simple negative real roots. Its selected weighted-index parity sequence has at most 20 changes. Thus it disproves the proposed bound whether real roots are counted distinctly or with multiplicity.

## What the proof establishes

For \(f(x)=\sum_{k=0}^{n}a_kx^k\), the statistic uses

\[
c_k=(k+1)a_k^2-k a_{k-1}a_{k+1},\qquad a_{-1}=a_{n+1}=0.
\]

Only indices with \(c_k>0\) are selected, in increasing order; consecutive parity changes are counted. The weighting, strict selection, coefficient hypothesis, actual degree, and endpoint convention are essential.

[PROOF.md](PROOF.md) contains the complete self-contained symbolic argument. It derives the compact coefficient formula for the repeated-root polynomial, an explicit uniform relative perturbation bound below 1/2000, three robust weighted-sign inequalities, the parity-subsequence argument, and the complete root factorization. No omitted arithmetic program, table, or numeric certificate is needed.

[REPORT.md](REPORT.md) preserves the mathematical audit, primitive-family normalization, source comparison, and reproducibility history. Its exact parity equality of 20 and complete sign pattern are additional audited finite cross-checks; the symbolic proof's bound of at most 20 already proves the counterexample.

[ACCEPTANCE.json](ACCEPTANCE.json) fixes the accepted scope and review limits. [EDITORIAL_MAP.json](EDITORIAL_MAP.json) records the exact formatting repairs and public-edition edits with UTF-8 ranges, hashes, replacements, and preserved ranges. Every displayed equation in the original proof and audit is unchanged.

[SOURCE_VERIFICATION.json](SOURCE_VERIFICATION.json) records public source titles, versioned URLs, PDF hashes and sizes, retrieval and inspection history, publication evidence, and supplemental verification match results. [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) names the closed seven-file public set and hashes the other six members; the manifest's own identity is pinned separately in the preparation records.

## Attribution and source-version limits

- [Shapiro, arXiv:1503.05295v1, p. 4](https://arxiv.org/pdf/1503.05295v1#page=4): original Conjecture 9, credited there to Forsgård and Shapiro.
- [Katkova, Shapiro and Vishnyakova, arXiv:2403.12200v1, Section 5](https://arxiv.org/pdf/2403.12200v1#page=20): prior disproof and primitive family. Published in *Journal of Mathematical Analysis and Applications* 538(1) (2024), article 128349, [DOI 10.1016/j.jmaa.2024.128349](https://doi.org/10.1016/j.jmaa.2024.128349).

The finite-product endpoint correction is restricted to the inspected arXiv version. The publisher PDF was not inspected. The corrected finite formulas have the same limits used by KSV, and the self-contained counterexample proof does not rely on the misindexed products.

## Review and distribution

This is an AI-assisted proof reconstruction with a separate AI-assisted mathematical audit. Acceptance is not external human peer review, journal acceptance of this reconstruction, or formal proof-assistant certification.

The public edition contains authored mathematics and permitted verification metadata. Raw coefficient and weighted-difference tables, numeric certificates, programs, datasets, source documents, extracted source text, source images, and private coordination material are excluded. The omitted finite certificates are supplemental; the full symbolic proof is present.
