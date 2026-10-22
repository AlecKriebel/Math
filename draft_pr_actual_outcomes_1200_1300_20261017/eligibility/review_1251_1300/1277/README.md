# Shapiro unweighted polynomial conjecture

Problem 2200015, row 1661. **Classification: DISPROVED, a prior published result.**

This packet gives a complete, table-free reconstruction of the counterexample of Olga Katkova, Boris Shapiro, and Anna Vishnyakova, *In search of Newton-type inequalities*, Section 5, arXiv:2403.12200v1, p. 20. Their work was published in *Journal of Mathematical Analysis and Applications* 538(1) (2024), article 128349, [DOI 10.1016/j.jmaa.2024.128349](https://doi.org/10.1016/j.jmaa.2024.128349). No novelty or priority claim is made.

## Mathematical result

Shapiro's [Conjecture 10, arXiv:1503.05295v1, p. 4](https://arxiv.org/pdf/1503.05295v1), selects every nonnegative unweighted difference c_k = a_k² − a_{k−1}a_{k+1}, including zero differences, with zero-extended endpoint coefficients. Its proposed real-root upper bound is the number of parity changes in the increasing list of selected indices.

- The exact seed P(x) = (1+x)^13(38x² − 89x + 83) has strictly positive coefficients, exactly 13 real roots counting multiplicity, and parity count 11. It is a positive scalar multiple of KSV's published seed.
- The ratios at indices 8, 9 and 10 are 27/28, 140/243 and 99/100. They are positive and below one. The corresponding unweighted differences are negative.
- The table-free perturbation with D = 10^7 has strictly positive coefficients and exactly 13 distinct simple negative roots, while its parity count is at most 11. Thus the failure also holds when real roots are counted distinctly.
- The source labels the selected list starting with k_1 but prints i = 0 under its parity sequence. The proof uses the actual defined list; it does not add an undefined k_0.

The weighted conjecture and KSV's higher-degree primitive construction are outside this packet's scope.

## Read the packet

- [PROOF.md](PROOF.md): the complete accepted proof, preserved byte-for-byte.
- [AUDIT.md](AUDIT.md): the accepted mathematical audit with only mapped nonmathematical wording changes and an explicit review-status disclosure.
- [ACCEPTANCE_BINDING.json](ACCEPTANCE_BINDING.json): exact proof and audit identities, scope and acceptance boundary.
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public scholarly-source titles and URLs, PDF hashes and sizes, and the recorded source-inspection and access history.
- [EDITORIAL_MAP.json](EDITORIAL_MAP.json): exact UTF-8 byte ranges, replacement text and hashes, with removed workflow text omitted.
- [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json): the closed artifact list and file identities. It lists itself without a self-digest, avoiding circular hashing.

The proof is 8,274 bytes, SHA-256 `4957c7cedcb79ae7529cbb641bf61dcb7610d03507b8d1e17504d99a4f9ecd75`.

## Sources and review boundary

The mathematical pages inspected in the recorded audit were Shapiro's arXiv v1, p. 4, and [KSV's arXiv v1, Section 5, p. 20](https://arxiv.org/pdf/2403.12200v1). The audit checked journal publication metadata on [Shapiro's publication list](https://staff.math.su.se/shapiro/Articles/). The journal-version PDF was unavailable to that audit; the publisher endpoint returned HTTP 403. No journal-PDF inspection is claimed.

This proof and audit are AI-assisted. No external human review, peer review of this packet, or formal proof certification is claimed. Acceptance records the mathematical audit's conclusion. Packet preparation checked identity, editorial scope, and preservation; it did not perform a new mathematical audit or repeat source inspection.

The unchanged proof's reference to an accompanying checker describes its original audit context. No executable checker, raw coefficient table, exact-check dataset, copied source PDF, extracted source text, source image, or private provenance is distributed here. The symbolic argument is self-contained and requires none of those files.
