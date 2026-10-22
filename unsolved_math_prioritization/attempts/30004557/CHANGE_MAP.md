# Change map: corrected release after the five-attempt proof audits

Problem 30004557 / OWR-2654830-012, rank 452. Revision date: 2026-10-03 UTC.

The original five-attempt packet remains byte-for-byte frozen at manifest SHA-256 `6e9c9a13a7dffa99b3e790ab4de28fdd098e564b87b5d31bce79d819ddeca647`. The initial preparation packet remains frozen at manifest SHA-256 `554df04a0a694bc49234aeb92ff84269b72854b7183f76865d1ad7be1357da2b`. This release corrects their subsequent five-attempt mathematical presentation; it performs no additional search or sixth attempt. The attempt log retains its original five entries and timestamps.

## Audit-to-proof map

| Review requirement | Incorporated location | Concrete change |
| --- | --- | --- |
| Full proof audit §1: explicit constructive records and operations | DATA_CONVENTIONS; every attempt's revision notice; Attempt 3 input; Attempt 4 §1; Attempt 5 §1 | States syntax/proof-set hypotheses, raw presentation/equality operations, universal-property factors and preservation comparisons. Distinguishes these supplied data from bare existence. |
| Full proof audit §2: regularity link | Attempt 1, Images and subobjects | Factors a locally surjective matrix through its kernel quotient; its reverse relation is an explicit inverse. This makes it a kernel-pair coequalizer and gives pullback-stable regular epimorphisms. |
| Full proof audit §3: stage dependency | Attempt 2 §C | Graph functions use expanded formulas, and stage-4 relations use stage-3 branch formulas. No same-stage predicate name is a prerequisite. |
| Full proof audit §4; supplement §1: hom-lifts without triangles | Attempt 3 §1 | Writes the correction a_B=F(ε_B)δ_(FB)^(-1), derives L_F and the symmetric L_G, and verifies their hom inverse equations. |
| Supplement §1: normalized counit | Attempt 3 §2 | Derives L_K by conjugation and L_G; defines ν_X:JKX→X as the K-lift of identity. Proves Kν_X=id, naturality and inverse equations. S-presentation transport uses this ν. |
| Full proof audit §5; supplement §2: old-symbol axioms | Attempt 3 §3 | Gives actual coherent graph equivalences for every original multi-ary function and relation. Explicitly handles constants/nullary predicates, mono names and nonchosen structural diagrams. |
| Full proof audit §5; supplement §4: fresh carriers are not C sorts | Attempt 3 §4 | Constructs each branch map from coordinates and formula graph equivalences, then composes with the named presentation cover; proves local coverage and common kernels. |
| Full proof audit §5; supplement §3: canonical comparison and uniqueness | Attempt 3 §4 | Proves the bidirectionally total functional graph from two covers with one kernel. Includes bc=q, identification of an existing p with that graph, branch-local sum formulas and the empty family. |
| Full proof audit §5; supplement §4: both scaffold equations | Attempt 3 §5 | Includes both p_X^T c_X^T=q_X^T and p_X^S c_X^S=q_X^S in the common signature/axioms. Explains derivability of opposite-side definitions and symmetric identification of the same upper theory. |
| Full proof audit §6 | Attempt 4 §§1–2 and result | Attaches the raw-operation hypotheses and the corrected common-span proof to generic-model reconstruction; retains its stronger indexed-semantics premise. |
| Full proof audit §7; supplement §5: effective Yoneda and uniform data | Attempt 5 §1 interface | Includes identity-evaluation hom-lifts, section-index smallness, cover/equality operations, preservation/factorization reflection and assigned covers used uniformly for objects/arrows. |
| Full proof audit §7; supplement §5: graph compactness | Attempt 5 §1, Graph compactness | Uses the combined family (f e_i)_i together with (d_j)_j into Y. Its cross kernel components are graph pullbacks, so the stated compact-kernel operation suffices. No assumption that every subobject is compact. |
| All reviews: preserve original scope/accounting | RESULT; STATUS; all attempt conclusions | Original unresolved/unsolved 5/5, no original counterexample, no global open-status or novelty claim. The original semantic-to-presentation implication remains unproved. |

## Included records

All five corrected attempt documents and DATA_CONVENTIONS are byte-identical to the mathematically reviewed release. The complete source-applicability audit, all-five-attempt proof audit, independent scaffold/graph supplement, and subsequent narrow integration review are in `audits/`. Bibliographic metadata and source hashes are in SOURCE_MANIFEST. The attempt log and finite-control program/output remain unchanged.

This publication copy updates the summary's review status and adds portable integrity verification. Historical workflow status files, local-only receipts, source PDFs/screenshots, extracted texts, corpus data and private context are not included. The earlier frozen research packets remain unchanged. Historical manifest references in the complete reviews identify their original review inputs; the manifest governing this publication copy is AUTHOR_MANIFEST.json.

## Final review state

The full mathematical audit passes the conditional constructions with the stated repairs. The independent supplement verifies those repairs, and INTEGRATION_REVIEW_V2.md passes their integration into the corrected proof text. None establishes the missing implication from the source-intended constructive semantic premise. Original-scope disposition remains unresolved after five substantive attempts.
