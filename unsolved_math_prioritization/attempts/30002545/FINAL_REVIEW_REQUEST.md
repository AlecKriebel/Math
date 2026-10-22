# Independent review request: full first-turn candidate

Please audit the exact original request and TURN_1.md, not merely the known limit. The source demands a simple combinatorial proof with no generating functions or induction and without assuming convergence. The candidate provides a finite static-bijection and slot-symmetry proof of p_n=(2n−1)/(3n) for n≥2 and handles n=1 separately.

## Primary source and credit

- Original OWR report, complete question on printed p707: https://ems.press/content/serial-article-files/46502
- Bóna–Pittel, arXiv:2108.04989v2, Example 2.3: corrected total-leaf formula, obtained there by generating functions. The original source's (2n+1)!!/3 is a typo, not our premise.
- Janson, arXiv:0803.1129v1, sections 1–2: contour bijection, leaf/plateau equality, equations (1.2), (1.6), and exchangeability. The official corrigendum credits Koganov (1996); its PDF download failed 502, while its primary search excerpt was readable.
- Janson–Kuba–Panholzer, arXiv:0805.4084v1, section 3.1 Theorems 1–2 and Remark 4: Gessel's ternary correspondence and plateau/empty-middle-slot equality. Their optional induction-based verification is replaced in the candidate by an explicit static interval inverse.

All PDFs except the unavailable corrigendum and all raw target records are local audit inputs in the source directory, with hashes/reading scope pinned in SOURCE_MANIFEST.json. No full-paper audit beyond those relevant portions is claimed. Numerical conclusions and bijections are known. Judge the credited reconstruction without assigning historical priority.

## Adversarial checks

1. Confirm that decreasing labels on [n] are bijectively replaced by increasing labels on {0,…,n−1}; the source is neither unlabeled Catalan nor binary-tree sampling.
2. Check the laminar pair-interval inverse of the plane contour, including that no label pair crosses, sibling order, uniformity and the root exception.
3. Check the distinct, laminar maximal components I_i of entries at least i. Every included label must occur twice there; each of the three gaps must equal the component of its minimum. Check that parent-by-inclusion recovers precisely a ternary tree and that the forward contour's subtree components are maximal.
4. Verify the plateau/empty-middle-slot correspondence and the global cyclic slot action. No free-action assumption is used. Verify total slots minus occupied slots without invoking an enumeration recurrence.
5. Examine the proof-style issue directly: recursive finite traversal code is not the mathematical induction proof excluded by the question; the written bijection inverses use finite containment descriptions. If you find a hidden inductive dependency that violates the requested method, explain it explicitly rather than approving only the known numerical limit.
6. Assess disposition honestly: a full literature-derived proof presentation is not a new theorem. Decide whether the packet meets the source request and state any priority/status uncertainty.

Run python verify_turn1.py and compare stdout byte-exactly with TURN_1_CHECKS.json. Independent checks should be separately written. Verify every file/hash in FINAL_FROZEN_MANIFEST.json. Preserve all frozen bytes; put required corrections in separate review artifacts. Do not undertake new author search while auditing.
