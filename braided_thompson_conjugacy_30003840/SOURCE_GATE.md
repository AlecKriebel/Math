# Source and prior-attempt gate

Problem **30003840 / OWR-16167-010**, queue rank **441**. Checked 2026-10-03 UTC.

## Exact target

Decide conjugacy in each of the two groups **F_br and T_br**. A solution only for V_br is insufficient. The source is Yuri Santos Rego's contribution, joint work with Kai-Uwe Bux, *Spraiges, 3-manifolds, and conjugacy for a braided Thompson group*, in Oberwolfach Report 26/2018, printed pp. 1594–1598. Question 48 is on pp. 1597–1598. The workshop took place 3–9 June 2018; the later publication date in some catalog metadata does not change the problem's date.

- DOI: https://doi.org/10.4171/OWR/2018/26
- Original report: https://ems.press/content/serial-article-files/46748
- Exact catalog URL attempted: https://www.unsolvedmath.com/problems/30003840

The exact live page was inaccessible: web opening failed; direct HTTP and the cloud browser returned 403 Forbidden, with the browser visibly displaying “This request was blocked.” No live page contents were inferred. The exact statement was instead verified against the original report and the immutable `ulamai/UnsolvedMath` corpus at revision `37e53eabe540fb458758e198be61634bd02ee008`. Recomputed SHA-256 values:

- problems.json: `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`
- research_results.json: `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`

The problem row matches both identifiers and the title. No research-results record keyed by this code exists. Full-value exact-ID/code checks found no matching research record; broader braided-Thompson hits concern other questions. Imported literature summaries are source leads, not the user's own attempts or verified proofs.

## Meaning of the groups

Use the natural map pi: V_br -> V induced by replacing a braid with its permutation. Here F_br = pi^(-1)(F); its diagrams have pure braids. T_br = pi^(-1)(T); its braid permutations preserve cyclic order. This is Witzel's BT, not the differently defined punctured-surface group often denoted T*.

The common kernel K = ker(pi) consists of diagrams (T,p,T), with p pure. It is the direct limit of pure braid groups along strand-cloning maps, not the usual limit formed by adjoining an unbraided strand. The F extension splits by the braid-free copy of F. These definitions are checked in Witzel, Section 5.2, and Zaremsky, Sections 1.1–1.2.

## Dated primary-literature check

1. **Bux–Santos Rego, OWR 2018**, Theorem 44 and Question 48. Theorem 44 announces decidability in V_br. Question 48 explicitly asks about F_br and T_br, and the following paragraph states that adapting the method is unclear. The V result is credited, never counted as a new solution here.
2. **Stefan Witzel**, *Classifying spaces from Ore categories with Garside families*, https://arxiv.org/abs/1710.02992 . Section 5.2 defines BT using cyclically permuting braids; the main theorem concerns finiteness properties, not conjugacy.
3. **T. Brady, J. Burillo, S. Cleary, M. Stein**, *Pure braid subgroups of braided Thompson's groups*, Publ. Mat. 52 (2008), 57–89; https://arxiv.org/abs/math/0603548 . Definitions and effective presentations.
4. **M. C. B. Zaremsky**, *On normal subgroups of the braided Thompson groups*, Groups Geom. Dyn. 12 (2018), 65–92; https://ems.press/content/serial-article-files/29861 . Section 1 gives K, the split F extension, and the four standard abelian characters. These established facts are credited inputs.
5. **K.-U. Bux, D. Sonkin**, *Some Remarks on the Braided Thompson Group BV*, https://arxiv.org/abs/0807.0061 . Effective diagram operations and the word problem. Its warning about unbounded strand counts is relevant to, but does not resolve, conjugacy.
6. **N. Franco, J. González-Meneses**, *Computation of Centralizers in Braid Groups and Garside Groups*, Rev. Mat. Iberoam. 19 (2003), 367–384; https://doi.org/10.4171/RMI/352 ; https://arxiv.org/abs/math/0201243 . Computes finite generating sets of fixed-strand braid centralizers.
7. **J. Aroca**, https://arxiv.org/abs/1807.09503 . Decidability concerns V_n(H) with H a subgroup of a finite symmetric group. It does not state the present braided subgroup result.
8. **M. Cumplido**, *Pure infinitely braided Thompson groups*, https://arxiv.org/abs/2311.12763 , published 2024. The stated results concern bi-orderability and generators, not a solution of this question.
9. **Yuri Santos Rego's research page**, https://ysantosrego.github.io/research-and-publications/ , checked 2026-10-03, lists the Bux joint preprint on conjugacy in a braided Thompson group and links the same OWR report. It supplies no claim that Question 48 is solved.

10. **J. Belk, F. Matucci**, *Conjugacy and Dynamics in Thompson's Groups*, Geometriae Dedicata 169 (2014), 239–261; https://arxiv.org/abs/0708.4250 ; https://doi.org/10.1007/s10711-013-9853-2 . This gives a unified solution of conjugacy for the classical groups F, T and V. Its classical F algorithm is the credited quotient input in Attempt 4, not a solution of the braided problem.

Searches for the exact question, F_br/T_br conjugacy, braided Thompson conjugacy, and 2025/2026 variants found no primary source establishing general decidability for these two groups. This is a dated, bounded literature search, not proof that no such result exists.

## Prior-user-attempt gate

Fresh default-branch QUEUE.md read: rank 441 is `queued`, `0/5`. Blob `42d850b073e3f3a5adf8303e985a0933260efa51`.

The complete main-branch campaign tree was read: 9,376 entries, not truncated, tree `cc37a9319691521a4c363ecf97e0d18a9ec9336f`; no path matches the numeric ID, OWR code, or braided-Thompson topic. The root tree was also inspected. GitHub code, PR (all states), and commit searches separately using `30003840`, `OWR-16167-010`, and `braided Thompson` returned no hits. These are bounded negative checks; no nonexistent history is invented. No earlier user attempt was identified.

## Budget and success criterion

Proceed with five substantive mathematical attempts unless a complete solution is obtained sooner. Source checks, tests, review and packaging are not extra attempts. A full claim would need a terminating yes/no algorithm for both groups (or a proved undecidability result for the relevant target). Search procedures that halt only on conjugate pairs, subgroup reductions, quotient obstructions, and solved special cases do not meet that criterion. Downloaded source papers, corpus copies and access-error screenshots stay outside the public packet.
