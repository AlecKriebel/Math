# PR1142 / problem30002112: independent priority and classification audit

Prepared 2026-10-17 UTC. Research family: earlier global spectral bounds, disconnected constructions, spectral prescription, and possible recorded full negative answers. The mathematical candidate is treated as a hypothesis. No candidate proof, earlier acceptance/audit, or sibling review was read.

## Classification

**An earlier recorded full negative answer exists.** Pétiard's 2017 preprint settles boundary dimensions at least three; his 2019 doctoral thesis explicitly includes dimension two. These sources use connected Euclidean hypersurfaces, so they also disprove the estimate when the boundary is required to be connected. The 2020 preprint / 2021 journal paper of Colbois and Provenzano independently recognizes the nonseparation result and cites the thesis. This is much more specific evidence than the observation that a proposed proof uses old tools.

The target is the question at printed p.2036 of Colbois's OWR 33/2012 contribution: for fixed m, could dimensional constants bound the intrinsic boundary eigenvalue after area normalization by a sum of a power of the isoperimetric ratio and a Weyl-order index term? The whole talk, printed pp.2034–2036, was inspected. The sum, the exponent 1+2/m on I, and the Euclidean ambient are explicit there. [Original OWR PDF](https://ems.press/content/serial-article-files/46403).

The result classification does **not** depend on the candidate's two-component cavity being admissible. Prior connected-boundary examples already belong to the original domain class. Nor does the conclusion imply that every possible technical simplification in the candidate is known; novelty of a particular localization or elementary presentation is a different question. The claim of solving this original question for the first time is contradicted by the located record.

## Exact earlier records and their scopes

| Record | Located mathematical content | Priority relevance |
|---|---|---|
| Luc Pétiard, arXiv:1706.09189v1, submitted 2017-06-28 09:53:24 UTC; six pages | Theorem 2, PDF p.2, treats arbitrary continuous functions of I plus a prescribed positive spectral coefficient. The hypersurfaces are smooth, compact, connected, and embedded in Euclidean codimension one. Dimension is m>=3. | Already a full answer for every m>=3, with connected boundary and even a prescribed embeddable diffeomorphism type. |
| Pétiard, 2019 Neuchâtel thesis, DOI 10.35662/unine-thesis-2749 | Theorem 2.1.2, printed p.24 / PDF p.36, explicitly includes m>=2. Its fixed isoperimetric ceiling is independent of the arbitrarily large index. Section 2.2 gives two components; Section 2.3 joins them while preserving the required finite part of the spectrum and volume ratio. | Earlier recorded full answer across the whole requested range m>=2. In dimension two topology may vary. |
| Colbois–Provenzano, arXiv:2010.06172v2, 2020-10-16 | Appendix A, Remark A.5, printed/PDF p.19, identifies the failure of separating I from the index for the ordinary Laplacian and refers to thesis item [37]. | Later primary acknowledgment; also dates public recognition before 2026. |
| Colbois–Provenzano, JLMS 104(5), 2128–2147 (2021), DOI 10.1112/jlms.12493; first online 2021-07-02 | Publisher HTML Appendix A, Remark 4, gives the same acknowledgment with bibliography [37] explicitly identifying the 2019 thesis. | Published recognition by the original question's proposer, not merely an unaffiliated search snippet. |

Primary records: [2017 arXiv version](https://arxiv.org/abs/1706.09189v1), [institutional thesis record](https://libra.unine.ch/handle/20.500.14713/31635), [thesis full text](https://libra.unine.ch/server/api/core/bitstreams/cb35ac23-61a8-402a-9fdb-a1eb4d47c041/content), [2020 v2](https://arxiv.org/abs/2010.06172v2), [2021 publisher text](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.12493).

The 2017 abstract page displays only v1. Its current PDF has a 2022 creation timestamp, consistent with a later repository compilation; submission metadata, rather than that timestamp, establishes the 2017 preprint date. The thesis PDF's own metadata is from March 2019, its title page records the 2019-02-05 defense, and the institutional record gives 2019. The Swiss National Library's bibliography issue dated **2019-07-31** lists this thesis (printed p.32, item 345). Thus the 2019 dating is supported by more than a current webpage's copyright/footer date. The national bibliography is a publication-existence receipt, not an independent check of the theorem. [National bibliography](https://ead.nb.admin.ch/web/sb-pdf/2019/sb201914.pdf).

## Independent bridge to the exact one-based target

This subsection is my deduction from the located results; it is not a copied theorem body.

Fix m>=2, put p=2/m and a=1+p, and let L_k denote the original target's one-based eigenvalues, including all zeros and multiplicities. Let mu_j be the thesis's zero-based eigenvalues. On the connected hypersurfaces used below,

    L_(j+1) = mu_j.

The usable consequence of thesis Theorem 2.1.2 is the following quantifier pattern: after choosing any positive coefficient C, there is a finite ceiling J_C and an index threshold, and at every sufficiently large j one can choose a connected Euclidean hypersurface satisfying I<=J_C whose normalized eigenvalue exceeds 2C j^p. J_C is allowed to depend on C but not on j.

Suppose finite target constants A_m,B_m have been proposed. Choose C>0 so that

    delta := 2C - 2^p max(B_m,0) > 0.

For the resulting J_C, take an allowed j>=1 so large that

    delta j^p > max(A_m,0) J_C^a.

Use (j+1)^p<=2^p j^p. The source's example then satisfies

    L_(j+1) |Sigma|^p
      > 2C j^p
      > max(A_m,0) J_C^a + max(B_m,0)(j+1)^p
      >= A_m I^a + B_m(j+1)^p.

This is a direct contradiction at a legitimate target index. It handles all m>=2, the exact exponent a, the sum of the two terms, and even arbitrary finite signs of the proposed constants. There is no appeal to treating a product bound as a sum bound.

For m>=3 the 2017 theorem gives a shorter route: substitute the continuous function F(t)=A_m t^a and enlarge its free spectral coefficient enough to cover the same one-place indexing shift. The 2019 bounded-I formulation is useful because its dimension-two inclusion is explicit.

The thesis result also yields the candidate's qualitative divergence of the quotient by the **unweighted sum**. For each R>=1 choose C=2^(p+1)R, obtain J_C, and then choose an allowed j so large that J_C^a <= (j+1)^p. Its example has

    L_(j+1)|Sigma|^p / (I^a + (j+1)^p)
      > 2C j^p / (2 (j+1)^p)
      >= C / 2^p
      = 2R.

Taking R to infinity provides a diagonal sequence. No claim is being made that one universal fixed ceiling J works for all R; that stronger assertion is neither required nor supplied by this argument.

Finally, a connected smooth compact embedded Euclidean hypersurface separates its bounded connected side from the unbounded side. Taking the bounded side gives a smooth bounded connected domain with precisely the hypersurface as boundary. Thus the source's boundary examples pass the original connected-domain requirement. They are a subclass of the class allowing two boundary components.

## Adversarial proof and boundary checks

The entire six-page 2017 proof and the thesis's complete Chapter 2 (printed pp.23–30) were read. The mechanism is not just mentioned abstractly. It is assembled in the earlier text:

1. The first-positive-eigenvalue construction is normalized so that the high-gap component has an area determined by the desired coefficient, while its first positive eigenvalue lies above the required part of the sphere's spectrum.
2. The disjoint union with a round sphere has **two** zero eigenvalues. The source explicitly records both and shifts the positive eigenvalues accordingly; there is no discarded zero mode.
3. The sphere bounds a ball of fixed nonzero volume. The union's total area is fixed once the desired coefficient is fixed, so its isoperimetric ratio has a finite ceiling independent of the spectral index. The construction is Euclidean; it does not reuse a varying product ambient as if that were Euclidean codimension one.
4. The narrow attachment argument controls each requested finite portion of the spectrum and the enclosed-volume ratio. Its limiting operator includes a Dirichlet segment contribution. The segment is first chosen short enough that its first mode lies above the finitely many modes being preserved. The extra segment modes are therefore addressed, not silently omitted.
5. The tube produces connected boundary. In m>=3 the original high-gap component can have a fixed embeddable topology, including a sphere. In m=2 the argument allows genus to vary; it does not contradict fixed-genus bounds.

The 1987 primary Anné paper supports the relevant convergence mechanism. Its setup allows an n-dimensional compact piece and a lower-dimensional attached piece; its printed p.275 explicitly includes the codimension-two endpoint-removal case. For the surface attachment, endpoints have codimension two and q=1<n=2, so this is not an excluded limiting dimension. I inspected the introduction, relevant coupling argument and marginal convergence statements, including a render of p.275; I did not independently reconstruct every analytic estimate or the earlier 1984 thesis. The 2019 thesis also supplies the smoothing/quasi-isometry discussion on printed p.25. This audit finds no hidden connectedness or dimension-two escape from the recorded prior result. [Anné primary journal article](https://www.numdam.org/articles/10.24033/asens.1533/).

The strict inequalities used to contradict the proposed estimate leave room for sufficiently small spectral, area, and ratio perturbations during tube attachment. Thus the fact that connected examples approximate the disconnected examples, rather than sharing their first finitely many eigenvalues exactly, is adequate. Eigenvalue convergence is taken with multiplicity.

## What the older general ingredients do and do not establish

| Source or route | Verified role | Classification for this exact question |
|---|---|---|
| CDE, arXiv:0909.5346v1, Theorem 1.4 and full Section 5 | Unbounded area-normalized first positive eigenvalues of embedded hypersurfaces; varying genus for m=2 and fixed embeddable smooth type for m>=3; smoothing follows a C1 embedding. | An old generic input, not by itself a recorded full additive-isoperimetric counterexample. Its statement does not give the required comparison between spectral growth and I. |
| CEG, arXiv:1007.0826v2, Theorem 1.1 | A product upper bound with geometry-dependent coefficient multiplying the index term. | Does not imply the proposed sum bound and does not settle the question affirmatively. |
| CEG Example 3.1 | A connected product domain with two boundary components; the first two one-based eigenvalues are zero. The ambient varies and contains a closed hyperbolic factor. | Genuine disconnected-boundary spectral bookkeeping, but its construction is not a Euclidean domain counterexample. |
| CEG Example 3.2 | Small spherical boundary enclosing the complement of a small ball in a compact ambient manifold; the large complementary volume drives the ambient ratio to zero. | Different ambient and bounded-side convention. The complementary side in Euclidean space is unbounded, so one cannot transfer that example unchanged. |
| Anné spectral attachment theorem, abstract spectral prescriptions, or arbitrary high-gap metrics alone | They can control/prescribe finite spectra or supply high eigenvalues under their own hypotheses. | Without Euclidean codimension-one placement and the right enclosed-volume/isoperimetric control, they leave a gap. Pétiard's actual completed assembly supplies that gap and is the decisive prior record. |
| Fixed-conformal-class and fixed-genus upper bounds | Coefficients depend on conformal geometry or topology. | They do not furnish constants depending only on dimension for all the source's examples. |

The CDE and CEG bodies above were inspected from the supplied primary-source cache; exact cached versions and hashes are pinned. The statements about spectral-prescription searches are limited classifications of the route, not claims that every prescription theorem has been exhaustively searched or read.

## Independence, search record, and limits

The first search batch independently surfaced Pétiard's thesis. `INITIAL_ASSESSMENT.md` was written at the first primary-source checkpoint, before any candidate-proof or other-audit reading. The parent was notified promptly, then informed of the version restriction and published citer. No sibling reports were read, and no external individual was contacted. No Git operation that changes repository state, PR change, release, tracker mutation, or Zenodo action was performed.

`QUERY_LOG.md` records ten actual search batches: 37 query inputs covering English and French, accent/spelling variants, Kröger/Kroger, additive/separated/decoupled formulations, prescription terminology, the arXiv identifier, journal status, and possible corrections. Approximate enclosing time ranges are explicitly distinguished from exact observed UTC pre-dispatch clocks. Raw search responses stay ignored. Primary bodies, rather than third-party abstracts, support the classification.

The historical gap that remains is **earliest priority within the pre-2019 literature**, and any separately published Pétiard journal version or correction not located by these searches. This audit does not certify Pétiard's global firstness, the complete absence of corrections, or an exhaustive bibliography. It does not establish that the exact nested-cavity presentation or a particular localization lemma already appeared earlier. It does establish an earlier recorded answer to the full original mathematical question, sufficiently to defeat a 2026 first-solution claim.

Access/read limitations: the direct Rome institutional mirror PDF request returned HTTP 403; the Wiley journal HTML was readable and the relevant appendix was read. The legacy RERO thesis PDF URL returned HTTP 410; the institutional successor provided the complete thesis. One misleading library-list handle resolved to an unrelated thesis and was excluded. The source-cache CDE file is v1 despite its generic `latest` filename; no claim to have read a different version is made. The 2020 arXiv appendix remark and 2021 publisher remark have different numbering, recorded above. Full Anné analytic verification was not undertaken; the inspected scope is explicitly listed in `READ_RECEIPTS.json`.

## Artifact verification

Public artifacts contain authored analysis, bibliographic facts, actual query inputs, read scopes, and hashes. Source PDF/text/HTML, source renders, retrieval receipts, and copied tool responses are under ignored paths. `SOURCE_HASHES.sha256` pins retained external material and the supplied primary files that were semantically read. `ARTIFACTS.sha256` pins this review's public authored artifacts and the source-hash ledger, excluding itself; it is an external sidecar, not a circular self-hash. Final completion estimate: 100% of this scoped priority/classification audit. This percentage describes audit completion, not a confidence probability or a claim of exhaustive historical search.
