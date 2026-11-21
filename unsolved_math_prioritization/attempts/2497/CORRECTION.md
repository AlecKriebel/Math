# Correction to the boundary of the density proof

This addendum corrects incomplete exceptional-pair lists in an earlier candidate. The original correction is pinned at SHA-256 c1ed8229057061f12977da29ced08357aa90ecba56a8b02e7d173ff4f3dca0d2 (2,137 bytes). This public copy changes only workflow and provenance wording; its own byte identity appears in MANIFEST.json.

**Corrected scope.** For coprime integers p > q ≥ 2, the three proved density ranges leave (4,3), (5,3), (5,2), (7,2), and (9,2), in addition to the separately known fully representable pair (3,2). The omitted pair was (4,3). This list describes the boundary of this proof, not a claim that all these cases remain unresolved in the literature.

Indeed, all q ≥ 4 are covered. With q = 3, the uncovered coprime possibilities 3 < p < 7 are p = 4 and 5. With q = 2, the uncovered coprime possibilities 2 < p < 11 are p = 3, 5, 7, and 9. These exhaust the complement of the three stated ranges.

Search-indexed text of the [Erdős Problem 1110 tracker](https://www.erdosproblems.com/1110) credits Yu–Chen with coprime failures also for (4,3) and (7,2). Neither extension follows from this density proof. The full primary theorem in Wang-Xing Yu and Yong-Gao Chen, “On a conjecture of Erdős and Lewin,” Journal of Number Theory 238 (2022), 763–778, [DOI 10.1016/j.jnt.2021.09.018](https://doi.org/10.1016/j.jnt.2021.09.018), remains uninspected; the attribution is reported at tracker level, not independently certified from that theorem. Direct tracker retrieval returned HTTP 403; the attribution was inspected through a search-indexed snapshot. This is an access-history statement from the 11 October 2026 audit.

The antichain-counting argument, density-zero conclusion for representable integers in the three stated ranges, and density-one induction producing infinitely many pairwise-coprime failures in those ranges are unchanged. No broader resolution or novelty is claimed.

The acceptance report incorporates this correction. Public bibliographic metadata, source-access limitations and the original correction pin appear in SOURCE_PINS.json. This correction and its review were AI-assisted; no external human review or formal proof-assistant certification has been obtained.
