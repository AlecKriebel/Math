# PR1156 / 30003650: independent priority and preparation-recovery audit

A complete public theorem already covers the candidate's main maximal-rank result, including singular matrices. Its proof also yields the candidate's fixed-ordinary-rank equality directly. This establishes mathematical duplication of the scoped result; it does not establish who first discovered or publicly disclosed it. No new publication or DOI was created by this audit.

The witness is Alper Ferudun, *The Maximal Finite CP-Plus-Rank Equals the Maximal CP-Rank*, EulerSolve OWR-15957-003, version 1.0, with [public paper and source](https://eulersolve.org/papers/owr-15957-003/) and [Zenodo DOI 10.5281/zenodo.23350364](https://doi.org/10.5281/zenodo.23350364). The complete four-page PDF, LaTeX source, proof notes, public metadata and DOI files were inspected; this conclusion does not rest on a title or abstract match. Primary bodies and renderings are retained privately; SOURCE_PINS.json records reproducible URL/hash pins.

## Scope established independently

Before reading the old internal mathematical audit, I read the whole 11,301-byte candidate at immutable head `57c07523247d0de1a2fbb76f3243d0369caff682`, path `unsolved_math_prioritization/attempts/30003650/PROOF.md`, SHA-256 `a2486250c2ddd7dc0e75cbf7275c59628a7b24f1f227e6432890369de96bacdb`, and Dickinson's original contribution in [Oberwolfach Report 52/2017](https://ems.press/content/serial-article-files/46715), printed pp. 3082–3083.

The original explicitly asks two separate questions: the maximum finite pointwise difference, and the maximum finite cp-plus-rank. The candidate fully answers the latter by `p_n^+ = p_n` for every `n >= 1`, in terms of the ordinary CP-rank maximum. It includes singular matrices with finite positive-factor rank and asserts the equality separately on every exact ordinary-rank stratum. The pointwise-gap extremum remains unresolved. An explicit numerical formula for every `p_n` is unnecessary for this answer to the second question. The combined partial label and generic no-novelty disclaimer do not negate its full scoped mathematical content.

## Checkable mathematical identity with the public theorem

Ferudun Theorem 1 states the all-order maximum equality and attainment. Its Lemma 3 supplies the essential boundary-inclusive step: for a minimal positive factor `A = BB^T`, choose a unit positive Perron vector `x`, set `P = xx^T`, and take small `s > 0` so `(I-sP)B > 0`. With Perron eigenvalue `lambda > 0`, the Gram matrix is

`A_s = A - lambda*(2s-s^2)*P`.

The positive Perron lift of Bomze–Dickinson–Still returns from `A_s` to `A` without adding columns. It gives

`cp^+(A) <= cp(A_s) <= cp^+(A_s) <= cp^+(A)`.

Thus both deformed ranks equal the original finite positive-factor rank. Since `I-sP` is invertible, ordinary rank is preserved. This does not use ambient interior semicontinuity and includes singular factors. The PDF's mathematical pages 2–3 were also inspected as images.

The candidate uses `I-tJ` instead of a Perron projector. Both exploit the same mechanism: a small subtraction keeps the given factor positive, while the inverse map is strictly positive and pulls an arbitrary minimal nonnegative factor back to a positive factor. For the Perron map, `(I-sP)^(-1) = I + s/(1-s)*P > 0`. These are different choices of the positive rank-one direction, with the same essential proof obligation and conclusion.

The fixed-rank statement is a direct inference from the published proof, even though it is not separately named there. Fix `1 <= r <= n`. Every finite cp-plus-rank at ordinary rank `r` is, by Lemma 3, an ordinary CP-rank at rank `r`, so `P_(n,r)^+ <= P_(n,r)`. Conversely choose an ordinary-rank-`r` matrix attaining `P_(n,r)`: this exists because CP-rank is a bounded integer and the stratum is nonempty. The public proof's positive smoothing `(I+tJ)D` works at this chosen matrix as well. The map is invertible, has the same number of columns, and its Gram matrix tends to the original. Closedness of bounded ordinary-CP-rank sets supplies equality of both factor ranks for sufficiently small positive `t`, still at ordinary rank `r`. Hence `P_(n,r)^+ >= P_(n,r)`. This is a complete literature-to-claim bridge, with no hidden assumption that the exact-rank stratum is closed.

## Public identity and chronology bounds

The provider and Zenodo PDFs are byte-identical: 63,633 bytes, SHA-256 `d727573c2b43edc1acba59007e172c6745a248c6466769d21b205d96b0a1657e`. The source archives are also byte-identical: 26,233 bytes, SHA-256 `f21945c142468e806b952350675f2f478c3ae3ac318e6e9ce0f87b2ec44ad5d0`. The verification report and archived files match both provider SHA-256 declarations and Zenodo MD5 declarations. Public Zenodo record 23350364 identifies Ferudun as creator, version 1.0, created `2026-10-13T19:49:12.777825+00:00`; DataCite returns the same title, author and DOI in the findable state, with registration `2026-10-13T19:49:14.000Z`.

The candidate commit records October 10, 2026. The provider page records October 13, 2026. These are different kinds of metadata and do not prove first public visibility, independent discovery, copying, or causal provenance. The source archive self-records provider commit `c6e7f41b4eb6ce876feb83e7eb626be1b243fd7e`; no repository-origin or chronology conclusion was inferred from this self-record alone. The public package's preparation notes contain pre-deposit wording; the current public API and matching files settle its present deposited state.

Fresh bounded public searches demonstrate why numeric-ID-only checking is insufficient: a public Zenodo query for `30003650` returned zero records, while `"OWR-15957-003"` and `"Maximal Finite CP-Plus-Rank"` each returned the one matching record 23350364. Each query was limited to 25 results, with no cursor traversal. A fresh GET of the EulerSolve paper index contains the same theorem, corpus alias and DOI. HTTP statuses and response hashes are preserved. A web-tool DOI redirect failure was not treated as a 404: the direct public Zenodo API and DataCite API both returned HTTP 200.

## Other primary sources and exact remaining scope

The [complete BDS author manuscript dated November 4, 2014](https://api.newton.ac.uk/website/v0/events/preprints/NI14088), corresponding to [LAA 482 (2015), 191–206](https://doi.org/10.1016/j.laa.2015.05.021), proves the positive Perron lift in Theorem 4.8, the interior two-sided identity in Theorem 4.9, and the interior maximum plus the general one-extra-column bracket in Theorem 5.1. Its paragraph before Lemma 5.2 leaves the all-order equality open there. This earlier paper alone is not a complete boundary-inclusive prior theorem.

[Pfeffer–Samper, DOI 10.1007/s00454-023-00620-y](https://doi.org/10.1007/s00454-023-00620-y), published January 24, 2024, Section 2.7, proves closedness of bounded ordinary-CP-rank sets and describes interior order-five cp/cp-plus strata. The inspected section does not replace the full all-order singular-domain step. [Lai–Yoshise (2022)](https://doi.org/10.1007/s10589-022-00417-4) and [Behling et al. (2026)](https://doi.org/10.1007/s10957-026-02950-2) supply factorization and stationary-point results, not universal minimal positive-width/nonexistence theorems. Their relevant definitions, hypotheses and theorem passages were checked in complete primary PDFs. Exact-phrase and mechanism searches covered cp-plus rank, positive congruence, singular factors and strict positive factorization. This bounded review found no stronger all-order primary theorem before the verified public witness; it is not an exhaustive literature or worldwide priority certificate.

## Earlier preparation recovery and exposure disclosure

Read-only authenticated GitHub inspection at main pin `dc6cbb7f5cc9218141a41916f4ce63a14b520810` recovered the earlier program inventory. PR1156 was classified partial/unsolved because the combined gap question remained unanswered; it was not in that program's eleven publication entries. The program's audits directory has fourteen entries through PR1155 and no PR1156 audit. The suggested `draft_pr_actual_claims_1100_1200_20261017/audits/pr1156_30003650` path returned a real authenticated API 404; its path-history query returned an empty list. No earlier prepared PR1156 package was recovered in that bounded program check. This does not exclude preparation elsewhere.

After sealing the scope and independently checking the public full proof, I read the pinned candidate's older MATHEMATICAL_AUDIT.md and the provider's source-provenance and proof-audit notes. Their novelty conclusions were not adopted as evidence. Raw private/account publication recertification belongs to the parent workflow and was not performed here. No outreach, service mutation, Git/index/ref mutation, publication/deposit creation or original/captured code execution occurred.

The completed finding is therefore **an existing exact public theorem and a valid direct fixed-rank bridge**, with an identified public DOI/file identity. The unresolved work is historical-priority investigation or wider gap research, not a missing mathematical proof of the scoped maximum equality.
