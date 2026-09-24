# Follow-up priority audit: forward citations

**Later full-text update:** the user supplied Kurose's 2023/2024 article, and
it was read on 24 September 2026 UTC. See the [new comparison](priority_supplied_papers.md).
The earlier access gap below is historical, not the current status of that paper.

**Date:** 2026-09-23. **Final checkpoint:** 13:43:27 UTC. **Completion:** 100% of this bounded citation-following audit, not of an exhaustive historical search.

**Finding:** No explicit earlier negative answer to FMU1998 Question 3(e), and no earlier identification of the proposed sphere–line product as its counterexample, was located. The follow-up substantially expands the citation search but does not establish priority. Several papers explicitly supply the classical radial-gradient ingredient; those are background, not newly discovered machinery.

## Citation coverage

The two seed papers were FMU1998, DOI `10.4036/iis.1998.125`, and Kurose1994, DOI `10.2748/tmj/1178225722`. API snapshots were retrieved on the audit date without authentication or external contact.

| Index | FMU1998 citing records returned | Kurose1994 citing records returned | Examination |
| --- | ---: | ---: | --- |
| OpenAlex | 3 | 77 | All returned titles screened |
| Semantic Scholar | 6 | 89 | All returned titles screened |
| Crossref | Count 0 | Count 57 | Metadata counts only; no citing-paper list returned |
| zbMATH | Unavailable | Unavailable | Both DOI queries returned HTTP 403 |

Thus **175 raw indexed citation records** were title-screened. This is **not 175 distinct papers**, and not 175 full-text readings: the lists overlap and contain separate versions, duplicate records, and malformed metadata. OpenAlex's result totals matched its returned records. Semantic Scholar's citation counts matched its returned arrays. Queries used OpenAlex works `W2025016356` and `W2092081856`, then `filter=cites:<work>&per-page=200`; Semantic Scholar queries requested `citationCount` and the complete returned `citations` arrays for each DOI.

The FMU lists mostly lead to the different Hessian-realization problem: Amari–Armstrong, Han–Wang (covered in the initial audit), and Fujiwara below. Semantic Scholar additionally returns a duplicate Amari–Armstrong preprint, the Hasegawa–Yamauchi tangent-bundle paper, and a malformed “Space of Kähler metrics” record whose bibliographic identity was not resolved. Its date for the Hasegawa–Yamauchi paper is also inconsistent with the printed 2008 source metadata.

There is direct evidence that these lists are incomplete: the 2010 Hasegawa et al. paper below visibly cites FMU1998 in reference [2], yet appears in neither returned FMU citation list. Crossref's zero count therefore cannot be interpreted as absence of citations.

## Primary-text follow-up

**Nine distinct complete primary PDFs, totaling 193 PDF pages including covers, were retrieved and subjected to whole-document keyword screening.** Relevant introductions, theorem statements, hit contexts, and bibliographies were inspected. This does not mean that every proof line in all nine papers was read or independently verified. Search terms included `radial`, `integrab`, `orthogon`, `Furuhata`, `Urakawa`, `open problem`, `counterexample`, `Gauss lemma`, `Levi`, `sphere`, and `Kurose`; mathematical notation and OCR limitations prevent treating absent words as conclusive evidence.

| Primary paper and inspected passages | Relevance and disposition |
| --- | --- |
| **Henmi–Kobayashi (2000), “Hooke’s law in statistical manifolds and divergences,”** [DOI](https://doi.org/10.1017/S002776300000739X), Example 2.2, Definition 4.1, Proposition 4.2, Theorem 4.3. | Example 2.2 expressly identifies the Levi–Civita radial field with the gradient of half squared distance. The later results give radial orthogonality under their curvature condition (S). No printed-question citation or explicit product counterexample was located. This is significant prior background, not evidence for novelty of the radial lemma. |
| **Ay–Amari (2015), “A Novel Approach to Canonical Divergences within Information Geometry,”** [DOI](https://doi.org/10.3390/e17127866), Remark 1 and §6. | Discusses the self-dual squared-distance case and the relation between inverse-exponential-field integrability and geodesic projection. No explicit resolution of 3(e) was located. Publisher PDF checked; the institutional preprint is an additional version, not another counted paper. |
| **Felice–Ay (2021), “Towards a Canonical Divergence within Information Geometry,”** [arXiv:1806.11363v3](https://arxiv.org/abs/1806.11363v3), Theorems II.1–II.2, associated §III discussion, §VI.A, references. | Explicitly states the Riemannian Gauss lemma and radial-gradient identity used here. Its broader divergence and projection discussion is related, but no FMU citation or explicit 3(e) negative answer was located. The broader claims were not independently validated in this priority audit. |
| **Fujiwara (2020), “Dually flat structures induced from monotone metrics on a two-level quantum state space,”** [DOI](https://doi.org/10.1140/epjp/s13360-020-00877-9), introduction and references. | Actual FMU citation concerns existence of Hessian structures for prescribed metrics, not the fixed-connection radial question. |
| **Hasegawa et al. (2010), “Remarks on Conformal-projective Flatness of Tangent Bundles with Some Lift Statistical Structures,”** [DOI](https://doi.org/10.32150/00005906), introduction, theorems, references. | A further actual FMU citation omitted by both citation lists. Concerns lifted structures and Hessian curvature; no radial-integrability answer located. |
| **Uohashi–Ohara–Fujii (2000), “1-conformally flat statistical submanifolds,”** [repository](https://doi.org/10.18910/12027), Theorems 1–2 and references. | Realization of 1-conformally flat structures as submanifolds of flat statistical manifolds, rather than a converse from radial integrability. |
| **Kobayashi–Ohno, “On a constant curvature statistical manifold,”** [arXiv:2008.13394v4](https://arxiv.org/abs/2008.13394v4), introduction, Theorem 2.6, radial-word contexts. | Characterizes constant curvature via projective flatness and conjugate symmetry. “Radial” refers to an affine hypersurface construction, not the distribution in 3(e). |
| **Min–Ri–Kwak (2016), “Constancy of curvature and conformal-projective flatness of statistical manifolds,”** [arXiv:1608.01107v1](https://arxiv.org/abs/1608.01107v1), introduction, theorem statements, references. | Concerns the broader conformal-projective equivalence; no radial-integrability implication or explicit counterexample located. |
| **Kayo (2026), “Equiaffine immersion, projective flatness and quasi-Codazzi structure,”** [arXiv:2605.01703v1](https://arxiv.org/abs/2605.01703v1), introduction, theorem statements, references. | Extends affine-realization criteria to degenerate metrics; no radial-integrability answer located. |

## Remaining gaps and disposition

- **Kurose's 2023/2024 “A certain ODE-system defining the geometric divergence,”** [publisher](https://doi.org/10.1007/s41884-023-00110-3): publisher abstract and all 11 references inspected; full text is subscription-only and was not accessed. It remains a relevant unclosed lead. No paywall bypass was attempted.
- **Hasegawa–Yamauchi (2008), “Conformal-projective flatness of tangent bundle with complete lift statistical structure,”** Differential Geometry–Dynamical Systems 10, 148–158: primary-paper abstract/first-page search extract inspected; publisher, EMIS, and CiteSeer retrieval attempts did not yield an accessible complete PDF. The 2010 paper restates its main theorem, but this is not a substitute for checking its entire text.
- Neither citation graph is exhaustive. Unindexed sources, unresolved metadata, non-English literature, and papers with no seed citation remain possible. This audit does not replace the separate older-source investigation or the live-database follow-up.

**Strongest supported novelty statement:** “An expanded citation and primary-text search located no earlier explicit answer to the printed Question 3(e).” **Unsupported statements:** “first,” “priority established,” or “the problem was demonstrably still open.” The mathematical resolution remains independently checkable; its elementary ingredients were already available in the literature.

## Reproducibility and checkpoints

The [175-row citation inventory](../research/priority_evidence/citation_inventory.csv) and [full-text screening manifest](../research/priority_evidence/fulltext_manifest.json) are preserved with this audit. The latter identifies exactly the nine counted papers, with source URLs, PDF hashes, and keyword counts. Raw API snapshots and retrieval failures are retained in local scratch storage under `tmp/priority_followup_citations/`. An unrelated PDF returned by a stale RIKEN path was detected by its title and excluded; failed HTML responses and duplicate versions were also excluded. Downloaded third-party PDFs are research scratch material, not proposed publication attachments.

- **2026-09-23 13:39 UTC — 50%:** all 175 index records title-screened; six complete primary texts retrieved; relevant divergence literature identified.
- **2026-09-23 13:43:27 UTC — 100%:** nine primary texts screened with relevant passages read; index omissions and remaining access gaps recorded. No direct priority conflict found within this bounded scope.
