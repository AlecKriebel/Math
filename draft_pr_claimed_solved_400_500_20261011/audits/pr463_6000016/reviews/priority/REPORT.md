# Independent priority and original-question audit: PR #463

This audit concerns only problem 6000016, AMR-059-0016, “Stability of Hessian Metrics,” at frozen PR head `982fcf87d60c9f8d4ec853d5dd5f4ad6021a6649`. The parent supplied the eligibility gate: open draft, exact `claimed_solved` status, one of five original subquestions claimed. No status, PR, source snapshot, checkout, index, or service was modified. The early independent hypotheses are recorded separately; no peer mathematical conclusions or previous author priority verdict were used to establish this conclusion.

**Priority recommendation: `already_solved`, subject to the parent's fresh adversarial check of the supplied application chain.** The negative answer is a direct consequence of an exact previously published affine-torus deformation and classical Hessian existence/entire Monge–Ampère results. The family is present in Baues–Goldman's January 2004 version. Delanoë's 1989 prescribed-volume theorem and Jörgens's 1954 disk estimate establish nonexistence of *all* positive definite Hessian metrics on its noncentral fibers. The novelty issue therefore extends beyond the already acknowledged family credit.

This is a recommendation based on **prior theorem coverage**. No publication explicitly naming the 1998 numbered question and announcing its negative answer was located. This audit does not certify historical first priority, continuing openness, or the identity/date of the first person to notice the classical implication. Those limitations do not remove the independently verified implication from the prior literature.

## Exact original question and scope

Furuhata–Matsuzoe–Urakawa, *Open Problems in Affine Differential Geometry and Related Topics*, Interdisciplinary Information Sciences 4 (1998), 125–127, DOI [10.4036/iis.1998.125](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_article/-char/en), item 5(b), printed p.126, attributes the question to Satoru Shimizu. The original page was visually inspected. It asks whether every small affine-structure deformation of a compact Hessian manifold admits a Hessian metric. The stated convention is a positive definite Riemannian metric locally given by a potential Hessian. The question does not fix holonomy or require preservation of a specified metric. Its surrounding hyperbolic special case is already credited to Koszul (1968).

The frozen claim uses `T²=R²/Z²`, `Dᵗ=D⁰+t dx⊗dx⊗∂y`, and the Euclidean Hessian metric at zero. The developing map `(x,y)↦(x,y+t x²/2)` identifies every fiber with a complete affine structure. For every nonzero `t`, its holonomy contains the shear `[[1,0],[t,1]]`. The original direct obstruction integrates the Codazzi identity `∂x gxy−∂y gxx=t gyy`; positivity and periodicity give a contradiction. Priority evaluation must concern this full nonexistence claim, rather than only the absence of a parallel metric.

## Strongest fully inspected historical route

The detailed proof is [APPLICABILITY_CHAIN.md](APPLICABILITY_CHAIN.md), Lemma A. Each substantive old-source dependency was obtained from its original publisher, institutional repository, or author-posted arXiv version, and the decisive pages were visually inspected.

| Dependency | Date and inspected location | What is established |
|---|---|---|
| [Baues–Goldman, arXiv math/0401257v1](https://arxiv.org/abs/math/0401257v1) | 20 January 2004; printed pp.24–25 | The exact developing-map family and its interpretation as a differentiable family of complete marked affine tori. |
| [Baues–Goldman v2](https://arxiv.org/abs/math/0401257v2) | 14 June 2005; printed p.20 | The same family in the later version; do not use the v1 date for a v2 page citation. |
| [Delanoë, *Remarques sur les variétés localement hessiennes*](https://ir.library.osaka-u.ac.jp/repo/ouka/all/7541/ojm26_01_03.pdf) | Osaka J. Math. 26 (1989), 65–69; Théorème 3, §2, p.67; explanatory paragraph p.68 read in text | Any compact positive Hessian metric admits a positive cohomologous replacement with prescribed density determinant, up to a positive constant. |
| [Jörgens, *Über die Lösungen der Differentialgleichung rt−s²=1*](https://link.springer.com/article/10.1007/BF01361114) | Math. Ann. 127 (1954), 130–134; official two-page preview, Satz 1 p.130 | Third-derivative estimates with an `R⁻²` factor; an entire positive Hessian solution with determinant one is quadratic by letting `R→∞`. |

The application verifies compactness, orientation, flatness, torsion-freeness, a parallel volume form, completeness and the entire-plane developing image. A hypothetical Hessian metric is first **replaced** using Delanoë, then lifted to an entire convex potential. It does not assume that the hypothetical original metric is parallel. The quadratic-potential conclusion produces a positive definite constant matrix preserved by shear holonomy. For `H=[[a,b],[b,c]]`, invariance forces `tc=0`, whereas positivity forces `c>0`. This excludes every nonzero parameter.

All conclusions are within the unrestricted positive definite question, including arbitrarily small parameters of both signs. The original potential only needs to exist locally on the torus; the replacement lifts to a global potential on its contractible developing cover. The full plane lies outside the hyperbolic case quoted in 1998. No issue about preserving holonomy, pseudo-Riemannian metrics, or preserving one selected Riemannian metric remains.

Consequently, the result follows from a family available by 20 January 2004 and analytic results published in 1954 and 1989. The integration proof may be a concise exposition, but it does not justify presenting this PR as a novel resolution of an open problem. This audit does not establish the novelty of that particular short proof.

## Separate parallel-volume theorem route

Shima's 2007 monograph, *The Geometry of Hessian Structures*, DOI [10.1142/6241](https://doi.org/10.1142/6241), Corollary 8.6, printed p.164, promises a **replacement** Hessian metric whose Levi-Civita connection is the given affine connection, on a compact oriented Hessian manifold admitting a parallel volume element. Official [Google Books](https://books.google.com/books?id=wLPICgAAQBAJ) search-within-volume results confirm the hypothesis and conclusion at `PA164`. The conditional application is independently given as Lemma B; all hypotheses are checked for this torus and the shear calculation finishes it immediately.

However, neither the publisher requests nor four official edition previews supplied a readable p.164 image. The auditor inspected the returned placeholder and does **not** claim visual inspection of the book page or its proof. This source alone is therefore not the fully verified foundation of the recommendation. Its primary-page limitation is preserved in the receipt.

Fox, *A Schwarz lemma for Kähler affine metrics and the canonical potential of a proper convex cone*, [arXiv 1206.3176v2](https://arxiv.org/abs/1206.3176v2), 4 April 2013, §5.2, printed p.25, was visually inspected and reports the same parallel-volume replacement conclusion, attributing it to Cheng–Yau (1982), Corollary 2.3. That corroboration is consistent with Lemma A. The original 1982 proceedings chapter was not obtained in full; its precise corollary number and original hypotheses were not independently checked. They are not indispensable to the verified Delanoë–Jörgens route.

## Rejected shortcuts and unresolved historical leads

Merely finding the Baues–Goldman family, proving that it has no invariant inner product, or identifying nontrivial unipotent holonomy would have been insufficient: a nonparallel Hessian metric must also be excluded. The old prescribed-volume theorem closes this exact gap.

Shima 1978, *Compact locally Hessian manifolds*, Osaka J. Math. 15, 509–513, DOI [10.18910/8797](https://ir.library.osaka-u.ac.jp/repo/ouka/all/8797/), was read in full text. Its Koszul-form integral criterion is not by itself the required assertion that every parallel-volume affine Hessian structure has a parallel metric. The existence/replacement step cannot be omitted.

Yagi's 1981 chapter, *On Hessian Structures on an Affine Manifold*, DOI [10.1007/978-1-4612-5987-9_24](https://link.springer.com/chapter/10.1007/978-1-4612-5987-9_24), pp.449–459, was available only in its official pp.449–450 preview. A secondary discussion suggested a dimension-two classification, but the relevant original theorem and page were not obtained, so no claimed Yagi classification supports the decision. Nagano–Yagi's 1974 affine-torus classification was identified as a backward citation lead, but its full classification was not relied on. Establishing an earlier precise source for the family would only move the existing coverage date earlier; it is unnecessary to the January 2004 coverage established here.

A recent Liu preprint was searched as a forward literature lead. Any reading that parallel volume makes the **given** Hessian metric parallel is invalid without further hypotheses. The explicit positive Hessian metric `(1+ε cos(2πx))dx²+dy²` on the standard torus, `0<ε<1`, has a parallel affine volume but nonzero `D⁰g`. This caution and its lifted potential are recorded in the application chain. No assertion from that recent preprint is used as a priority foundation, and this audit does not review the preprint as a whole.

## Coverage, limitations and required credits

The authored [SEARCH_COVERAGE.md](SEARCH_COVERAGE.md) records a bounded search of more than fifty queries, versions, original-question history, relevant forward and backward citations, and source access limitations. It is not an exhaustive MathSciNet/zbMATH/citation-database or all-language history search. No individual was contacted. Failure to find an explicit named answer does not prove absence of one or establish novelty.

Any retained explanatory result should credit the 1998 question and its attribution, Baues–Goldman's exact family with version-specific pages and dates, Delanoë's prescribed-volume theorem, Jörgens's two-dimensional entire rigidity, and the broader parallel-volume result's Cheng–Yau/Shima lineage with access qualifications. The priority note should state that the negative answer is a consequence of these classical results and that no historical first-resolution claim is supported.

The parent should submit the fully inspected application chain to a fresh independent adversary before accepting this status recommendation. If that adversary confirms it and the parent corrects `QUEUE.md` to `already_solved`, the user's explicit status filter requires skipping further processing of this PR. This report itself does not change that status or authorize a publication, comment, merge, or other action.

## Artifact boundary

Only the auditor-authored files named in `PUBLIC_OUTPUT_WHITELIST.json` are candidates for public retention. All foreign PDFs, excerpts, full text, preview HTML/JSON, and page images are under `private_sources/` and excluded. `SOURCE_RECEIPT.json` contains bibliographic and integrity metadata only. The report, decision and manifest bind the audit to the frozen PR head and are intended to enable reproduction without copying foreign corpora into public review materials.
