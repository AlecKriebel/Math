# Five-attempt result: constructive definitional extensions and Morita equivalence

Problem 30004557 / OWR-2654830-012, rank 452. Date: 3 October 2026.

**Outcome: no full resolution of the original constructive claim, after 5/5 substantive written attempts.** This corrected release incorporates the full proof audit and independent narrow supplement without adding a sixth attempt. No counterexample to it was obtained. The ordinary coherent Morita characterization is established prior work, credited to Dimitris Tsementzis; it is not counted as a new resolution of the source's constructive-mathematics question.

## Source and the corrected scope

The source is Henri Lombardi, *Geometric theories for constructive algebra*, in [Oberwolfach Report 34/2020](https://doi.org/10.4171/OWR/2020/34), pp. 1744–1747, question p. 1746. The source fixes finitary coherent/dynamical rules, then lists positive definitions, unique-existence functions and Bishop-style finite sort constructions.

The external constructive setting is material. The general aims on OWR p. 1744 concern constructive treatment of geometric theories/toposes and avoiding nonpredicative definitions. Lombardi–Mahboubi, [*Valuative lattices and spectra*, arXiv:2210.16558v3](https://arxiv.org/abs/2210.16558v3), English p. E19, explicitly describes Bishop-style external reasoning; pp. E20–E22 provide the extension rules. The source does not choose a named formal foundational system or formally define constructive Morita equivalence. We neither ignore the external constructive scope nor invent a mandatory formal-system or proof-assistant task.

Tsementzis's [2015 preprint](https://arxiv.org/abs/1507.02302v1) and [published article](https://doi.org/10.1017/jsl.2017.59) give the familiar coherent characterization. The current primary restatement in D’Arienzo–Pagano–McInnis, [arXiv:2011.14056v2](https://arxiv.org/abs/2011.14056v2), §6.3, cites the journal theorem as Theorem 3.9. The accessible preprint's numbers and inhabited-base-sort restrictions must not be silently transferred or suppressed. An independent applicability audit rejected original-scope closure from that literature comparison alone.

## Substantive attempts

1. `ATTEMPT_1.md`: constructs finite proof-carrying quotient presentations and coherent relation matrices; derives composition, limits, images, subobjects, quotients and disjoint stable sums. Empty sorts and contexts are treated directly.
2. `ATTEMPT_2.md`: gives an explicit old-language proof translation, conservativity, a uniformly finite-stage presentation library, and amalgamation of finite zigzags into common extension spans after renaming.
3. `ATTEMPT_3.md`: from actual inverse functors on the presented pretoposes, constructs a two-copy category and a common finite extension with explicit comparison graphs, avoiding common-skeleton and quotient-representative choices.
4. `ATTEMPT_4.md`: proves the analogous conditional reconstruction from pseudonaturally equivalent model semantics in every presented constructive pretopos by evaluating at the generic models.
5. `ATTEMPT_5.md`: derives a finite-cover reconstruction under a specified constructive coherent-sheaf interface, and proves that a tempting representative-selection shortcut would imply excluded middle. The needed sheaf/interface theorem is not established from the original premise.

The full independent proof audit passes the conditional constructions with explicit data and presentation repairs; a separate independent supplement verifies those repairs. The separate narrow integration review passes the corrected text; its full report is also included. The complete reports are in `audits/`, including the original source-applicability HOLD. Familiar categorical-completion ideas are not represented as historically new.

## Exact remaining step

Show that the source-intended constructive Morita equivalence supplies either:

- the pseudonatural model equivalences on all presented constructive pretoposes used in attempt 4; or
- a constructive classifying-sheaf comparison with the uniform finite-cover/compact-kernel operations, effective Yoneda hom-lifts, preservation data and equality evidence stated in Attempt 5.

Neither implication is proved here. A small presented pretopos is not generally a Grothendieck topos, so a semantic premise quantified only over Grothendieck toposes cannot simply be evaluated at it. Conversely, a bare equivalence of categories of Bishop-set models supplies neither that evaluation nor the required naturality. A full positive conclusion must establish the relevant comparison constructively, rather than rename the desired syntactic relation as the semantic premise.

The missing implication is not asserted to be false or historically open. This packet records what this campaign established and failed to establish, not a global literature-status theorem.

## Audited hypotheses and incorporated repairs

All conditional theorems include [DATA_CONVENTIONS.md](DATA_CONVENTIONS.md). The raw-presentation operations, proof-indexed sets, universal-property factors and preservation comparisons are substantive hypotheses. Their availability is not inferred from classical existence statements.

Attempt 3 now states original multi-ary and nullary symbol graph axioms, effective hom-lifts without triangle assumptions, a K-normalized counit, literal maps from fresh scaffold carriers, and both canonical comparison equations. Attempt 5 derives graph compactness from the combined finite cover of the target and retains a uniform effective interface. Attempt 1 explicitly closes the regular-epimorphism link. See [CHANGE_MAP.md](CHANGE_MAP.md) for exact audit-to-proof mappings.

## Conventions and corrections retained

- Nullary products and empty sorts are explicitly permitted; no element is added to an old empty sort.
- Finite stages may add set-indexed families; finite depth of each individual symbol is not used as a substitute for a global stage bound.
- Change-of-environment functors are **pretopos functors**. Merely regular/Barr-exact functors need not preserve finite coproducts.
- Equivalence data means functors both ways and supplied natural inverse isomorphisms. Fully faithful plus essentially surjective is not silently upgraded by a choice principle.
- Quotient maps are never assumed to have extensional sections.
- Original formulas and source PDFs are not redistributed; the public source manifest contains bibliographic records and hashes only.

## Accounting and integrity

The initial source-applicability packet recorded 0/5 because it contained preparation, literature comparison and checks. Its manifest and the subsequent independent HOLD are preserved unchanged. The five attempts here start after that HOLD and are five substantive mathematical documents, not five retrieval, checking or packaging actions.

Exact live catalogue-page reading remains blocked. Pinned-corpus hashes and the original report were checked; the earlier bounded prior-attempt gate found no exact target attempt. The full proof audit, independent supplement and narrow integration review pass the conditional arguments under their stated hypotheses. This research note records the unresolved original claim and those conditional results; it does not announce a solution.
