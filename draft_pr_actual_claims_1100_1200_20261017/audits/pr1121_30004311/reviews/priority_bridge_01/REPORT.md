# Focused prior-implication adversary report: PR1121 / Problem 30004311

**Finding: no PRIORFULL bridge established in this bounded review.** I found no checked published theorem-plus-specialization that already supplies the full negative answer to Cedó’s OWR 51/2019, Problem 9. This is not a novelty certificate and not a claim that no earlier answer exists.

The strongest verified conclusion is more specific: the named orthogonal/embedding constructions have two trivial factors; the named nontrivial-factor constructions either fail the group hypotheses or, under those hypotheses, reduce to two trivial factors. Three general elimination arguments were derived in this audit and independently checked by the parent reviewer. They should be described as **new audit derivations**, never as earlier published solutions.

## Claim and success criterion

The target is the existence of a finite nontrivial simple left brace B with metabelian multiplicative group, all multiplicative Sylow subgroups abelian, and no asymmetric-product presentation whose two factors are trivial. The submitted order-20,000 example and its primary-triple-star obstruction are accepted mathematical inputs here. A PRIORFULL finding would require a published construction/classification theorem, explicit admissible data satisfying every hypothesis, and a checked obstruction to every two-trivial-factor presentation. General framework resemblance, a different displayed formula, a paper abstract, and search absence do not meet that standard.

## Route results

| Family | Body inspected | Result and exact gap |
|---|---|---|
| [1705.08493v1](https://arxiv.org/abs/1705.08493v1), Theorem 3.3 | §§3, 5, 6 | Starting from a simple two-trivial-factor seed, a finite metabelian A-group output still has two trivial factors; complete flattening derivation in CHECKABLE_BRIDGES.md §3. Starting from a seed outside that class is circular for this priority question. |
| Same paper, Theorem 5.3 | §5.1 | Derived length n+1≥3; target metabelianity fails. |
| Same paper, Theorem 5.7 | §§5.2–5.3 | The required order-p linear map makes a p-subgroup nonabelian. The abelian-Sylow hypothesis fails. |
| [1807.06408v1](https://arxiv.org/abs/1807.06408v1) | §2, §3 setup and Theorem 3.3; §5 non-simple extension; §6 construction and Theorem 6.2 | The constructions explicitly use trivial T and S. They provide known positive examples, not the target counterexample. |
| [2001.08905v1](https://arxiv.org/abs/2001.08905v1) | §2 and §3 construction, Proposition 3.3 and Theorem 3.4 | The embedding is additive only; its constructed T and S are explicitly trivial. Embedding the additive group of a radical-ring brace does not embed its brace multiplication or triple-star witness. |
| [2401.12904v2](https://arxiv.org/abs/2401.12904v2), Theorem 4.5 | Entire §4 setup, theorem, Remark 4.6 | Generally nontrivial A1 is retained. Finite metabelian A-group hypotheses force α(A)=1, producing a nonzero socle and contradicting simplicity; CHECKABLE_BRIDGES.md §2. |
| Same paper, Theorem 5.3 | §5 | Reuses 1705 §5.2; its p-Sylow is nonabelian. The R named in this construction is a trivial brace, not the submitted radical-ring primary brace. |
| [1511.08477v3](https://arxiv.org/abs/1511.08477v3), Theorem 4.2; [1610.00477v1](https://arxiv.org/abs/1610.00477v1), Proposition 2.7 | Matched-product definitions and hypotheses; simplicity results and explicit §4 example | General theorem recovers the submitted brace operations, with every compatibility checked symbolically. It does not assert simplicity. The available general simplicity theorem assumes simple factors, false for R and H here. |
| 1610 §3 H families and §4 nested Example 4.3 | Explicit formulas | A-group H factors have f=id and zero primary triple star; standard iterated products have a published two-trivial-factor rewriting. The explicit nested Example 4.3 also flattens by the scalar q-coordinate; this is an audit derivation. |

The detailed proofs are in [CHECKABLE_BRIDGES.md](CHECKABLE_BRIDGES.md). These eliminations do not show that primary triple-star nonvanishing is necessary for a negative answer; another intrinsic obstruction in an uninspected construction could still establish priority.

## Later work and citation checks

The body of [2112.07271v1](https://arxiv.org/abs/2112.07271v1), especially §§4–5, constructs its new simple-brace family as T⋊°H with both factors explicitly trivial; 2401 Remark 4.6 also identifies the previous solution family as two-trivial-factor products. Its simple-solution property should not be confused with a universal simple-brace classification.

I inspected the relevant discussion and references in [Vendramin’s survey, 2311.07112v3](https://arxiv.org/abs/2311.07112v3), and the main construction statements in three current 2026 sources. In [2609.24640v1](https://arxiv.org/abs/2609.24640v1), Theorem 3.2 makes the additive group nonabelian whenever its deformation map κ is nonzero. With κ=0 it returns its input brace; its displayed seed reuses 1705 §5.2 and has a nonabelian same-prime Sylow. Thus that construction supplies no target bridge. [2607.17125v2](https://arxiv.org/abs/2607.17125v2) addresses cyclic multiplicative Sylows; its nontrivial simple cases have nonabelian additive group. Neither statement is being inferred merely from its title.

A final embedding search identified [2609.20401v1](https://arxiv.org/abs/2609.20401v1), posted 17 September 2026. Its Theorem 4.4 supplies simplicity permanence for a kernel-wreath construction. Direct inspection of Theorem 3.1 and Lemma 3.2 gives an additional audit elimination: every classical-brace output with abelian multiplicative Sylows either has a proper normal Hall subgroup or is the nonsimple order-4 exception. The support-based proof, valid for arbitrary seeds, is in CHECKABLE_BRIDGES.md §6. Thus the new construction does not give a full-target bridge either. This is a new audit deduction from that source, not a theorem attributed to it.

OpenAlex citing lists were retrieved for the four named source records, using the corresponding journal/merged records: 29 citing entries for 1705, 12 for 1807, 8 for 2001, and zero indexed citations for the merged 2401/2025 record at retrieval. Metadata was used only to discover leads. Those counts are not completeness evidence; the index misses recent/preprint references and includes irrelevant citations. The ledger records which leads had actual bodies inspected.

## Version and access limits

Current arXiv records were opened on 17 October 2026: the named four remain v1 (23 May 2017), v1 (17 July 2018), v1 (24 January 2020), and v2 (8 June 2024). Versioned PDFs were freshly retrieved and hash-receipted. The 2025 version of record for the fourth paper is identified by DOI [10.1016/j.jpaa.2025.108025](https://doi.org/10.1016/j.jpaa.2025.108025). **The final journal body was not inspected:** web access failed and the direct PDF request returned HTTP 403. All theorem-number/formula arguments above are pinned to arXiv v2. This is a material access limitation, not a statement that the versions are identical.

The original 2016 Catino–Colazzo–Stefanelli body was not separately retrieved; the full general theorem was checked in the named sources that restate it. No unseen final journal revision, inaccessible source body, unindexed preprint, or informal communication is ruled out. No external individual was contacted.

## Disposition

**PRIORFULL: not established. PRIORPARTIAL/framework overlap: verified.** The matched-product formalism and earlier ingredients are published. An exact earlier theorem guaranteeing the new primary-ring coupling’s simplicity and the universal exclusion of two trivial factors remains unlocated. The audit has finite scope; it neither verifies nor denies global historical novelty. Do not promote this report to a blanket novelty claim.
