# Grushin Bessel converses: accepted branchwise results

**Independently integration-reviewed reader edition, 14 October 2026.** Complete authored proofs, accepted audits, source-scope analysis, and reproducible diagnostics for the converse question discussed by Roychowdhury in Oberwolfach Report 14/2025, printed p.606. Tracking reference: row 1780 / 30006230.

The principal results are accepted at their explicitly stated scopes. The original informal Hardy–Rellich question still needs a noncircular formulation to be selected. This is a substantive branchwise answer, **not an unqualified claim that the original source question is solved**. The precise distinction is in [the final source-scope adjudication](scope_adjudication/SOURCE_RESOLUTION_SCOPE.md).

## Results at a glance

1. **Hardy, regular leading weight:** both source displays are equivalent to the exact full-interval Q-dimensional Bessel property for every Q ≥ 3, V > 0, and real W, without extra endpoint hypotheses. The radial-gradient display is quantified over all source tests.
2. **Proposed Hardy–Rellich core, current dimensions:** necessity holds for Q ≥ 4 and W ≥ 0 under the stated side condition. The global classical side condition allows extension from V > 0 to V ≥ 0.
3. **Proposed core, unrestricted real potential:** an exact Q = 5 all-test counterexample disproves the universal necessity assertion, even with V > 0 and the source side condition. This is not a classification of every fixed dimension.
4. **Proposed core, historical Q = 3:** necessity fails even with strictly positive V and W and a strictly positive side condition. The historical two-sheet angular analysis is proved directly.
5. **One fixed independent positive remainder function:** for Q ≥ 3, V > 0, and real W, this stronger proposed antecedent implies the exact positive-solution property. The given function is a supersolution and need not be the exact solution obtained.
6. **Literal degenerate weights:** both Hardy necessities fail even with W > 0 when V has an interior zero, under the stated flux-classical convention. The global classical Hardy–Rellich side condition forces V to be either everywhere positive or identically zero; the zero case is classified exactly.

Every claim retains the geometry, regularity, signs, side condition, test class, integral convention, and solution convention in its manuscript. See [the precise scope summary](PROVED_AND_REMAINING.md).

## Suggested reading order

- [Final acceptance index](accepted/pass1_audit/ACCEPTANCE_INDEX.md): compact mathematical classification and report map.
- [Source-resolution scope adjudication](scope_adjudication/SOURCE_RESOLUTION_SCOPE.md): what the results do and do not answer in the source.
- [Regular Hardy proof](accepted/pass1_hardy/HARDY_CONVERSE_PROOF.md).
- [Nonnegative-potential core proof](accepted/pass1_hardy/NONNEGATIVE_RELLICH_CONVERSE.md) and [nonnegative-leading-weight corollary](accepted/pass1_hardy/NONNEGATIVE_LEADING_WEIGHT_COROLLARY.md).
- [Q = 5 real-potential counterexample](accepted/pass1_rellich/RELLICH_CORE_COUNTEREXAMPLE.md) and [its spectral audit](accepted/pass1_spectral_audit/SPECTRAL_COUNTEREXAMPLE_AUDIT.md).
- [Historical Q = 3 positive-potential counterexample](accepted/pass1_rellich/historical_q3/HISTORICAL_Q3_POSITIVE_W_COUNTEREXAMPLE.md) and [its spectral audit](accepted/pass1_spectral_audit/HISTORICAL_Q3_SPECTRAL_AUDIT.md).
- [Fixed-independent-function proof](accepted/pass1_hardy/INDEPENDENT_FUNCTION_RELLICH_CONVERSE.md).
- [Degenerate-weight addendum](accepted/pass1_audit/DEGENERATE_WEIGHT_ADDENDUM.md) and [independent review](accepted/pass1_hardy/DEGENERATE_WEIGHT_REVIEW.md).
- [Sources and version distinctions](SOURCES.md), [validation instructions](VALIDATION.md), and [publication-safety boundary](PUBLICATION_SAFETY.md).

## What is preserved

All included author proofs, acceptance reports, diagnostic programs and original manifests are exact byte copies. Their relative directory structure is retained inside `accepted/`. The earlier formulation audit is preserved in `source_context/`, and the final source-scope review in `scope_adjudication/`. [The artifact map](ORIGINAL_ARTIFACTS.json) identifies every unchanged original and its hash. No original mathematical file has been edited.

Earlier reports are historical snapshots. Statements such as “unattempted,” “outside this audit,” or “current positive-W question unresolved” describe the coverage of that earlier file. They must be read alongside the final acceptance index and source-scope adjudication, which record the later accepted supplements. They are not current gaps in the frozen principal assertions.

The added reader documents, package validator and replay harness are editorial/reproducibility material. The package does not introduce another proof pass, a novelty claim, human peer review, or an exhaustive current-openness certificate. Diagnostics supplement the analytical proofs; they do not establish universal inequalities.

## Independent integration review

[The integration acceptance report](review/INDEPENDENT_INTEGRATION_ACCEPTANCE.md) verifies the full authored package and records editorial validator hardening, exact prior pins, fresh diagnostic replay, link checks and tamper controls. All 59 original artifacts remain byte-identical. Operational disposition: **DEFERRED, 1/5**, for source formulation selection; the frozen branchwise mathematical results retain their acceptance.
