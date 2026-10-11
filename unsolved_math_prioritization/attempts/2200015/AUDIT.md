# Acceptance: row 1661 / problem 2200015

**Verdict: ACCEPTED as a reconstruction of a prior published disproof.** No mathematical defect was found in the seed report or the D=10^7 symbolic certificate. The correct credit is Katkova-Shapiro-Vishnyakova (2024), *In search of Newton-type inequalities*, Section 5, arXiv:2403.12200v1 p. 20; published in *JMAA* 538(1), 128349, [DOI](https://doi.org/10.1016/j.jmaa.2024.128349). This audit does not claim a new disproof.

## Findings

- Shapiro's Conjecture 10, arXiv:1503.05295v1 p. 4, selects all nonnegative unweighted differences c_k=a_k^2-a_{k-1}a_{k+1}; it does not select only strictly positive differences and does not use the weighted Conjecture 9 expression.
- P=(1+x)^13(38x^2-89x+83) is exactly 720720 times the published seed. All coefficients are positive, by a_k=binom(15,k)((k-9)^2+2).
- The quadratic discriminant is -4695. The seed has exactly 13 real roots counting multiplicity, but only one distinct real root.
- The ratios q_8,q_9,q_10 are respectively 27/28, 140/243, 99/100. They are positive and below 1; it is c_k, or q_k-1, that is negative. Any description saying the ratios themselves are negative should be corrected. Neither reviewed mathematical report makes that error.
- The seed's only negative differences are at 8,9,10, and no difference is zero. The seed parity count is exactly 11. PROOF.md gives a table-free quartic sign argument for the complete sign pattern as well as the sufficient parity-deletion argument.
- The D=10^7 certificate has a valid uniform coefficient estimate, strict positivity, and strict ratio stability. It proves a polynomial with 13 distinct real roots and v<=11. Its denominator-cleared integer polynomial additionally has exactly the same sign pattern and v=11 under independent exact arithmetic.
- The separate D=10^6 integer witness also independently passes exact coefficient positivity, difference-sign, parity-count, and rational-root checks. The table-free quantitative proof is for the D=10^7 witness.
- Shapiro's author publication list confirms KSV's JMAA publication. This audit inspected the arXiv v1 mathematical text, not the journal-version PDF. The publisher endpoint returned 403; the publication status is not inferred from that failed request.

## Scope and reproducibility

PROOF.md is the full self-contained, table-free proof. A separately retained, independently authored Python standard-library checker corroborated the exact arithmetic. Recorded runs under normal Python, -O, and -OO all passed and produced byte-identical outputs. Validation guards used explicit exceptions, not removable assertions. No source-author code or previously supplied checker was executed. The checker and its detailed outputs are not included in this public packet.

The audit preserved its supplied source inputs byte-for-byte. Packet preparation checked preservation of those inputs and the complete accepted audit. It checked file identities and the recorded outcomes; it did not rerun the mathematical checker or repeat the scholarly-source inspections. The proof is unchanged. The exact nonmathematical edits to this report are recorded in EDITORIAL_MAP.json.

Source versions, inspection scope, publication-status evidence, and access limits are in SOURCE_METADATA.json. ACCEPTANCE_BINDING.json identifies the original accepted report, this editorial edition, and the unchanged proof by digest. PUBLIC_MANIFEST.json lists the public artifacts. The packet contains authored mathematical prose and public-source verification metadata; it omits copied source documents, source text and images, dataset contents, programs, raw check tables, and private provenance.

## Qualification of the source indexing typo

The printed selected-index list starts with k_1, while the parity sequence's lower index is printed i=0. This is an indexing typo, not a defined extra term. The audit uses the parity changes in the actual increasing list of selected indices. KSV restates and disproves that same convention. The explicit simple-root witness separately resolves any ambiguity about counting multiplicities.

## Recommended mathematical classification

DISPROVED; prior published result, with an independently accepted explicit degree-15 counterexample and a table-free distinct-root robustness certificate. The scope is the exact unweighted Conjecture 10 / problem 2200015.

## Review status

This proof and audit are AI-assisted. No external human review, peer review, or formal proof certification is claimed. Acceptance is the outcome of the documented mathematical audit; it does not establish an independent human endorsement. Packet preparation is an editorial and integrity check, not a further mathematical review.
