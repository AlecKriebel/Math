# Scoped acceptance of the cyclic transfer

Review date: 2026-10-09. Problem: 30005118 / OWR-10252930-031. Verdict: ACCEPT for the mathematical scope below; no mathematical correction was required.

The independently reviewed argument proves that same-group cyclic self-sumset recognition is NP-complete for both explicitly listed binary residues and dense characteristic vectors. The restricted hardness conclusion uses odd n, zero in the target, and canonical target representatives strictly below n/2. For an everywhere-nonempty restricted language, the empty-source YES branch is replaced by (3,{0}), exactly as allowed in the certificate.

The retained proof covers finite integer-root normalization, including negative and odd minima; the zero anchor and absence of 2-torsion; both directions of the no-wrap lemma; the total reduction and empty/zero-diameter branches; polynomial sparse encoding; dense hardness from the source construction's bounded numerical universe; and polynomial certificates for sparse NP membership.

The dependency is Theorem 1.2 and the final bounded-universe reduction on manuscript page 23 of Abboud, Fischer, Safier, and Wallheimer, *Recognizing Sumsets is NP-Complete*, arXiv:2410.18661v2, published in SODA 2025, pp.4484–4506, DOI 10.1137/1.9781611978322.153. The source authors receive the integer-hardness construction credit. The elementary cyclic transfer is supplied without a novelty claim. The original target and source theorem pinpoints were inspected; the complete source gadget construction was not independently reproved.

## Exact editions

- CYCLIC_SUMSET_CERTIFICATE.md: 11272 bytes; SHA-256 `7f767eea9e2cf0e8bea67f3762d6116a0ac31d89f64cb2861499ba269d38c3a3`.
- INDEPENDENT_AUDIT.md: 6928 bytes; SHA-256 `2683828c307ecdb427b102fbdd05d8c12b16774f4f2e4660617dcc9da171e319`.

These identities bind the editions actually included here. The original review concerned the full original certificate; exact editorial comparison confirms preservation of its entire mathematical proof and limitations and of the audit's substantive checks. The deleted reproduction and administrative material is not part of this edition's acceptance claim. PROVENANCE.md records the editorial scope, and MANIFEST.json binds the distributed members.

## Limits

A polynomial-time algorithm exists in either stated model if and only if P=NP. No unconditional separation, randomized lower bound, average-case claim, exhaustive novelty certification, new hardness gadget construction, external human peer review, or proof-assistant verification is asserted. The theorem concerns unbounded n given with the input and ordinary self-sums, not restricted sums, unrelated summand sets, compressed circuits or query-only input. New mathematical claims or edits require a fresh review.
