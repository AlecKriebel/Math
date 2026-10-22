# Acceptance of the corrected surreal-derivation reductions

Verdict: ACCEPT_CORRECTED_PARTIAL_REDUCTIONS_AND_OBSTRUCTIONS.

Problem 30003317 / OWR-15181-008. The original question remains unresolved by this work. No novelty or priority claim is made.

AI-assisted, unrefereed authored mathematics with an independent internal AI audit. This is not external human peer review or formal proof-assistant certification.

Only authored mathematical prose, the exact correction, acceptance records and public verification metadata are distributed. No executable code, raw datasets, copied source documents, extracted source text, source images, raw search responses or private coordination material are included. This is not a computational reproduction package.

## Present acceptance and limits

The audit's sole required Lemma 2 scope patch has been applied to a separate copy of the proof. The original 21,310-byte proof has SHA-256 9d446a6b3bf7c37c6e09b037962ab9cf8f5c152cd8507a6567b782b924fb7be8. The corrected pre-editorial proof is 21,364 bytes, SHA-256 7f5390fe1b7a3092022cfdf701a42d242a32bd3bec299682272a754d87e1f6b1. The exact 533-byte correction patch has SHA-256 38abe77afe8848f33ccfd5ea439e43684e87f07dcdb1ce536e7ce030c602e7d4.

The historical conditional audit decision is preserved in full in AUDIT.md. Its condition is fulfilled here; that does not accept the old ambiguous statement, a complete solution, uniqueness, nonuniqueness or a novelty claim. The audit found no second required substantive patch. Its full supplementary mathematical arguments remain available alongside the full corrected proof.

All deductions are accepted relative to the named published structural inputs, particularly dominant-path termination, summability, T4 and the canonical path-sum construction. Neither the full nested-truncation foundations nor the complete cited embedding or general Lie-correspondence machinery is independently proved here. No automated theorem prover was used. This edition performs byte authentication, exact correction and editorial replay, not a new source review or new mathematical proof search.

The exact remaining gap is global: construct a nonzero datum satisfying W, F, L0 and B for at least one D, or rule out every such datum for every D. The original existential problem is not equivalent to examining only the canonical restriction. The bounded literature screen does not certify present-day openness.

## Complete historical patch notes, unchanged

The following notes retain their original imperative wording. The required action they describe has been completed in this edition.

# Required correction and acceptance boundary

The only required textual correction is in Lemma 2 of `proofs/REDUCTIONS.md`.

Replace:

> **Lemma 2 (dominance calculus).** For any surreal derivation D, if a is nonzero and a is not asymptotic in magnitude to 1, then:

with:

> **Lemma 2 (dominance calculus).** For any surreal derivation D, let a be nonzero with |a| either infinite or infinitesimal (equivalently, a is not Archimedean-equivalent to 1). Then:

The exact unified diff is `LEMMA2_SCOPE.patch`. It is intended for an unchanged source file with SHA-256 `9d446a6b3bf7c37c6e09b037962ab9cf8f5c152cd8507a6567b782b924fb7be8`.

The current manuscript defines a∼b by a-b≺b. If its phrase about asymptotic magnitude is read in terms of that relation, a=2 meets the stated hypothesis. Yet b=1/ω is strictly dominated by 2, while D(2)=0 and D(1/ω)=-D(ω)/ω²≠0. Thus the old wording cannot be accepted under that reading.

The original proof already treats exactly the infinite and infinitesimal cases. All later applications are to a non-real leading term after deleting the real coefficient, a nonzero purely infinite logarithm, or a nonconstant monomial term. Equal integration monomials are compared by real proportionality. Therefore the patch changes no downstream conclusion.

For a fully explicit presentation, the detailed audit supplies optional expansions of three compressed steps:

1. W preserves all summable families by finite counting of contributing input monomials and indices at each output monomial.
2. The integration recursion is a coherent union of set-length, set-valued recursions with fixed class parameters. It does not invoke class-valued elementary transfinite recursion. Strict derivative descent forces monomial descent by excluding equal and larger monomials separately.
3. A strongly R-linear automorphism mapping monomials onto monomials has a strongly R-linear inverse, since the inverse monomial map preserves order and normal-form supports.

These expansions justify acceptance; they are not additional assumptions. The corrected partial deductions remain conditional on the published structural results expressly identified in the audit. The original existential problem remains unresolved in this work.

## Exact applied patch

The following JSON string decodes to the complete original unified patch, including every context line and final newline. It applies to the original proofs/REDUCTIONS.md. PROOF.md contains the resulting proof with an editorial wrapper.

```json
"--- a/proofs/REDUCTIONS.md\n+++ b/proofs/REDUCTIONS.md\n@@ -39,7 +39,7 @@\n \n ## 2. Every extension in a fixed family has the same leading derivative\n \n-**Lemma 2 (dominance calculus).** For any surreal derivation D, if a is nonzero and a is not asymptotic in magnitude to 1, then:\n+**Lemma 2 (dominance calculus).** For any surreal derivation D, let a be nonzero with |a| either infinite or infinitesimal (equivalently, a is not Archimedean-equivalent to 1). Then:\n \n     b ≺ a  ⇒  D(b) ≺ D(a),\n     b ∼ a  ⇒  D(b) ∼ D(a).\n"
```
