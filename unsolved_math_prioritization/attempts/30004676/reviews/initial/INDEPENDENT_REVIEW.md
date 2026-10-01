# Independent partial-lemma checkpoint: 30004676

Reviewed 2026-10-01 UTC. Frozen mathematical artifact: `PARTIAL.md`, SHA-256 `16039e2409de331bead57262612c12e3ac08359669df4de7075804fd2917a002`.

## Verdict and accounting

**PASS as the stated conditional same-map lifting lemma.** No mathematical correction is required in the frozen lemma. This is not a proof of Puzarenko's original converse, not a proof that the additional cover hypothesis follows from the original assumptions, and not a novelty certification. The full target remains unresolved by this artifact. This review is a partial-check checkpoint while further substantive research continues, not an instruction to end the attempt early.

The pre-interruption substantive-attempt count is unknown and must remain explicitly unknown until recovered. It is not reset to zero. This source audit, independent checking, and review consume no new substantive proof-search approach or author turn.

## Source match and convention boundary

Puzarenko's contribution in [OWR 21/2021, pp. 1181–1182](https://ems.press/content/serial-article-files/46899) explicitly works with well-founded KPU structures in finite signatures. Its weaker notion requires a surjection with Δ pullbacks of signature relations, including equality. Its strong reducibility uses one surjection whose pullbacks of all definable Σ predicates are Σ. The report credits implication (1)⇒(2) and presents the converse as conjectural. The frozen statement correctly keeps the distinction. The source pages were checked as text and rendered images. The [publisher record](https://ems.press/journals/owr/articles/7155442) distinguishes the 2021 workshop from publication on 25 August 2022.

The lemma explicitly fixes a finite relational KPU language, set/urelement and membership predicates, the necessary collection scheme for that language, and a parameter-allowing convention. Those restrictions are part of the conditional result. They must not be removed when summarizing it. “Internal Σ predicates” here means predicates defined and evaluated over B, not merely relations which themselves happen to be elements of B; the theorem's formula-by-formula statement has the required broader meaning.

## Closure and formal translation

The convention is standard: [Barwise, *Admissible Sets and Structures*, Chapter I, Definitions 2.2–2.3 and 4.1, Theorem 4.3](https://api.pageplace.de/preview/DT0400.9781316731697_A29773274/preview-9781316731697_A29773274.pdf) defines KPU relative to its language, includes Δ₀-Collection with parameters, and derives Σ-to-Σ₁ normalization. The relevant material is printed pp. 10–11 and 15–17. The preview was inspected; no full book is redistributed.

For a Σ₁ predicate `exists u theta(z,u,p)` with Δ₀ theta, collection on an internal A-set c gives an internal witness set d for every z in c. Therefore the displayed equivalence (1) is valid. Its right side has only the leading existential d unbounded, with a Δ₀ matrix; finite witness tuples can be encoded using pairing. Empty c is covered by the empty witness set. This verifies the only potentially problematic normal-form closure. Under the generated-Σ syntax, bounded universal closure is also included in the grammar itself.

The translation uses only fixed Σ definitions of atomic pullbacks and their complements, finite Boolean operations, existential quantification, and bounded quantification over the chosen internal cover. It never assumes a definable graph for the external surjection ν or a simultaneous truth predicate for arbitrary B-formulas. The finite collection of parameters in the atomic definitions and in C can be retained throughout each translation.

## Adversarial semantic audit

All induction clauses preserve truth along the **same** ν:

- Atomic and negated atomic cases use both halves of the Δ hypothesis. Equality is equality of images, not identity of representatives.
- Unbounded existential quantification uses surjectivity in the reverse direction; no internal choice function is needed.
- Bounded existential quantification needs coverage to find a representative of a B-witness, and containment to ensure an A-witness represents a genuine B-member.
- Bounded universal quantification needs containment in the B-to-A direction, and coverage in the A-to-B direction. An under-cover can spuriously validate a universal statement; an over-cover can spuriously invalidate it.
- Totality is essential even when the bounded formula is vacuously true: an empty family of covers would make the leading existential c false. For a B-empty set or urelement, exact coverage forces an internal empty A-set cover and ordinary vacuity applies.
- Nonfunctionality causes no problem. Every allowed cover is exact, so every allowed choice yields the same truth value. Duplicate representatives likewise do not matter. The proof is not asserting a definable single-valued selector.
- For each fixed B-parameter tuple, surjectivity provides a finite tuple of representatives. The induction is valid for every such choice. It does not invoke global choice.
- Negation of a Δ₀ formula can be put into bounded positive syntax with negated atoms. Translating it and the original formula yields complementary Σ predicates, establishing the claimed Δ conclusion.

No hidden application of collection to an external inverse-image class occurs. Collection is used only after the additional hypothesis provides an internal A-set bound. The asserted exactness of the image of a cover is deliberately a semantic hypothesis, not a purported Σ formula obtained for free.

## Independent finite controls

The author's `check_covers.py` was inspected, not executed. Its loop sizes independently reproduce the recorded 89,556-assertion total. All seven hashes in `MANIFEST.json` match the frozen files.

A separately authored standard-library program, `independent_cover_check.py`, passes **62,706** assertions. It exhausts 68 small surjections, uneven and duplicate representation fibers, all associated finite exact covers and unary truth sets; tests nested bounded formulas, unbounded existential quantification, Boolean operations, equality, sort predicates, and alternative parameter representatives; and rejects under-coverage, over-coverage, missing totality, and literal representative equality. A separate finite truth-table control checks the logical form of the witness-set collection equivalence. `INDEPENDENT_CHECKS.json` records the results and checker hash.

These finite structures are not admissible models. The diagnostics do not verify KPU, existence of internal A-sets, Σ-definability of C, or the original conjecture. Acceptance of the conditional lemma rests on the symbolic syntactic and semantic induction above, not the check count.

## Remaining boundary

The new hypothesis remains substantial: one total Σ relation selecting exact internal set covers for every interpreted membership fiber. Atomic Δ interpretability does not itself provide such a relation. Nor is the hypothesis shown to follow from the original global property about all interpretable admissibles. The package also does not establish atomic interpretability of J(A) in A; the universal semidecidable predicate's complement cannot be inserted as a free negative atomic definition. The original converse therefore remains a research target.

Independent review completion: **100% for this frozen conditional lemma and source scope**. No original-target completion percentage, attempt-counter change, publication, or final research stopping decision is certified here. No new proof-search route was pursued in this review.
