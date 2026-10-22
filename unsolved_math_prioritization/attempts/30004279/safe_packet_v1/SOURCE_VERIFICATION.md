# Source verification and prior-work limits

Checked 2026-10-05 UTC. This document distinguishes successful inspection, metadata-only inspection, and blocked inspection. It is not a proof of global openness.

## Problem identity

- Numeric ID: 30004279. Descriptor: OWR-17292-002, *Equivalent Bicommutant Categories from Nonisomorphic Conformal Nets*.
- Requested exact page: https://www.unsolvedmath.com/problems/30004279 . Direct HTTPS returned 403; web opening returned a fetch error. No page content was inspected.
- Original source: https://doi.org/10.4171/OWR/2019/49 . The complete public report PDF was retrieved from the EMS publisher. Henriques's contribution is printed pp. 3075–3076 (PDF pages 23–24); its opening conjecture was checked in extracted text and visually on rendered PDF page 23.
- The original contribution distinguishes the proved fusion-category Morita statement from the proposed conformal-net comparison. It asks for tensor-equivalent bicommutant categories; equality of DHR representation categories is a weaker condition.
- The descriptor's statement/review digests identify a historical imported record but were not recomputed from the raw record. Raw upstream statement and AI-report corpora were unavailable to this worker and uninspected. The original source, rather than any uninspected AI report, governs the mathematical discussion here.

## Primary literature checked

The per-PDF public URLs, exact byte counts, SHA-256 hashes, versions, and inspected sections are in source_metadata.json. Bytes were retrieved privately; none of those PDFs or their extracted text is in this packet. Full-byte retrieval does not mean every page was read line by line.

1. Henriques 1701.02052v2: the finite-index bicommutant/center theorem, the endpoint-normal soliton definition, the four-interval extension test, and the absorbing-object endomorphism algebra were inspected.
2. Henriques–Penneys 1511.05226v2: the bicommutant construction from the separable Hilbert completion of a fusion category was inspected. This supplies Hilb as a bicommutant category; it must not be confused with the commutant construction in the later paper.
3. Henriques–Penneys 2004.08271v1: Theorem B/6.8 was inspected. Morita-equivalent unitary fusion categories, fully faithful representations, and the same permitted hyperfinite-factor type class are essential hypotheses. The definition of bicommutant equivalence also retains positivity.
4. Dong–Xu math/0411499v2: lattice representation classification and mu-index formula were inspected. For the A1 versus E8 comparison the discriminant groups have orders 2 and 1.
5. Kawahigashi–Longo math/0407263v2: Example 2.8 constructs a holomorphic central-charge-8 net. The nearby anticipated loop-group comparison is not used as a theorem here.
6. Del Vecchio–Iovieno–Tanimoto 1811.04501v2: the definition includes half-lines; Proposition 3.5 and Theorem 3.6 apply to the proper solitons used in Approach 5. Their modular-theoretic inequivalence argument is an explicit external theorem dependency.
7. Henriques–Penneys–Tener 2307.13822v1: the general finite-depth classification is a conjecture there, and the proved case concerns commutants of fusion categories. The later journal record, CMP 407 (2026), article 68, was checked at https://doi.org/10.1007/s00220-025-05548-3 . Neither the inspected preprint theorem nor journal abstract asserts equivalence of full soliton categories of different nets.

Additional current primary records checked were the January 2025 Oxford seminar https://www.maths.ox.ac.uk/node/69925 and the May 2026 ICTS seminar https://www.icts.res.in/seminar/2026-05-14/chetan-vuppulury . These discuss constructions of soliton categories and do not constitute a verified resolution of the exact target.

### Material incomplete source

Nivedita's 2026 Oxford thesis, *Towards fully-local 2d chiral CFTs from conformal nets: bicommutant categories and fusion of their modules*, was located at https://ora.ox.ac.uk/objects/uuid%3Ab8ccd774-5979-46bc-98fa-67260cfa7266 . Its primary-repository abstract/metadata announces bicommutant and center statements without finite index or strong additivity. It does not announce cross-net equivalence. The direct page/PDF route returned HTTP 403; the full thesis was not obtained. There is no verified byte count, hash, or inspected page range for that PDF. The absence of a cross-net theorem from an abstract is not evidence of its absence from the thesis. This remains a literature-inspection gap.

### Bounded conclusion

The inspected sources did not verify a resolution of the original target. This is not a claim that no resolution exists, that the problem is globally open, or that any retained lemma is novel. The finite-index assumptions in this packet are retained despite the broader thesis abstract, whose full argument was not inspected.

## Actual prior-attempt checks

Read-only connector checks were made against AlecKriebel/Math:

- PR search, all states: 30004279, bicommutant, and 17292; no matching result returned.
- Branch search: 30004279 and bicommutant; no matching branch returned, pagination cursor null.
- Default-branch code search: 30004279 and bicommutant; no results returned. Such indexing searches alone are not complete evidence.
- The main attempts directory was then actually listed: tree e6e54f78c20bb3854cad94632be838d82c69254b, 62 entries, no target-ID folder.
- The fetched main state.json and history.jsonl contained no target-ID entry. related_target_groups.json returned no target-ID/name match.
- The main queue row was inspected and stated rank 719, queued, 0/5. This is an observation only, not proof that no off-main or unpublished attempt exists.
- Main was observed at commit c5bbb350b24a4a612b1dc64e30f51100c4de2eb0. The connector reads were sampled around that observation; an exhaustive historical-tree or all-branch traversal was not performed. Two full recursive-main-tree fetches failed with transport closure; the narrower attempt-tree listing succeeded.
- Available conversation-history retrieval did not establish a corroborated task-specific earlier attempt. Unrelated material with apparently conflated identifiers was rejected. No such private material is reproduced here.
- A bounded filesystem name/text scan found only catalog/queue copies and this current target workspace, rather than an earlier target-specific research directory. It was not a claim to have searched every inaccessible or remote file.

The upstream raw AI report is still uninspected. It cannot be certified clean of an already attempted idea. No fabricated history or novelty conclusion is inferred from the missing report.
