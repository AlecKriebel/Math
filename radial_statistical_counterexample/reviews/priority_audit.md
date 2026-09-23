# Priority audit: radial orthogonality and dual 1-conformal flatness

Audit date: 2026-09-23 UTC (2026-09-22 in America/Los_Angeles).
Reviewer: independent literature-audit agent, working without external contact.
Scope: the explicit negative answer to item 3(e) in Furuhata–Matsuzoe–Urakawa (1998), including the Levi–Civita product example and the non-self-dual extension.

## Finding

**No explicit earlier negative answer to item 3(e), or earlier identification of this particular product as its counterexample, was found in this bounded search.** That is a search result, not proof of priority. Publication as a concise *negative answer to the printed question* is supported, subject to the separate mathematical verification. Publication as a certified first resolution of a problem known to remain open in 2026 is **not** supported by this audit.

The argument uses established ingredients. Kurose's 1994 criterion already makes the non-flatness obstruction a classical projective-curvature issue. The non-self-dual example also uses a known construction: it is exactly a statistical structure with cubic form divisible by the metric. Neither ingredient should be presented as a newly discovered general theory.

The live database page could not be inspected: both the web reader and a direct HTTP request were unsuccessful, with the latter returning a Vercel Security Checkpoint. The repository's catalog entry for `AMR-059-0011` / `6000011` records `upstream_status: partially_solved`. That local flag does not identify a theorem or prove that a relevant resolution already exists. It does prevent treating the database as verified evidence of present open status. The original printed question, rather than an inferred database status, should anchor the paper.

Recommended wording: “We give an explicit negative answer to Question 3(e) as printed in [FMU98]. A focused literature search found no earlier explicit answer, but the argument uses classical Riemannian and statistical-geometric facts.” Avoid “first,” “long-standing unresolved,” and priority guarantees.

## Primary sources examined and their implications

1. **H. Furuhata, H. Matsuzoe, H. Urakawa, *Open Problems in Affine Differential Geometry and Related Topics*, Interdisciplinary Information Sciences 4(2) (1998), 125–127.** [Publisher and DOI](https://doi.org/10.4036/iis.1998.125), [original PDF](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf). Item 3(e) on p.126 was visually inspected. It specifies radial orthogonal complements on a punctured convex neighborhood, asks whether their integrability implies 1-conformal flatness of the dual, and has no printed exclusion of Levi–Civita structures. The workshop occurred in December 1996; the source publication date is 1998. Some later references give 1999, but the publisher and original volume favor 1998.

2. **T. Kurose, *On the divergences of 1-conformally flat statistical manifolds*, Tohoku Mathematical Journal 46 (1994), 427–433.** [Publisher and DOI](https://doi.org/10.2748/tmj/1178225722), [PDF](https://www.jstage.jst.go.jp/article/tmj1949/46/3/46_3_427/_pdf). Section 1, p.428 supplies the definition and Proposition 1, identifying 1-conformal flatness with projective flatness and symmetric Ricci of the dual. Page 429 also states the constant-curvature consequence of simultaneous projective flatness in dimension at least three. These facts predate the printed problem. No assertion there was found answering the later radial-integrability question.

3. **T. Kurose, *Conformal-Projective Geometry of Statistical Manifolds*, Interdisciplinary Information Sciences 8(1) (2002), 89–100.** [Publisher and DOI](https://doi.org/10.4036/iis.2002.89), [PDF](https://www.jstage.jst.go.jp/article/iis/8/1/8_1_89/_pdf). Publisher abstract and all-page OCR were screened. The work studies two-function conformal-projective transformations, curvature criteria, and umbilical hypersurfaces. It distinguishes that broader notion from 1-conformal flatness. No radial-integrability resolution was located; the eight-item reference list does not cite FMU98. OCR screening is less reliable than line-by-line visual reading and is recorded as such.

4. **K. Uohashi, A. Ohara, T. Fujii, *Foliations and divergences of flat statistical manifolds*, Hiroshima Mathematical Journal 30(3) (2000), 403–414.** [Journal issue](https://www.math.sci.hiroshima-u.ac.jp/hmj/v30.3/index.html), [primary PDF](https://www.math.sci.hiroshima-u.ac.jp/hmj/v30.3/P403-414.pdf), DOI `10.32917/hmj/1206124606`. Full text was retrieved and screened. Its setting starts with a Hessian domain and concerns level hypersurfaces, their orthogonal foliation, dual geodesics, and divergences. No counterexample to item 3(e) was located. Similar terminology does not make its ambient-flat setting equivalent to the question audited here.

5. **R. Ueno, *Geodesic Connectedness on Statistical Manifolds with Divisible Cubic Forms*, arXiv:2503.10024v2 (6 June 2025).** [Versioned full text](https://arxiv.org/html/2503.10024v2). Section 3, Proposition 3.5 and equation (3.6) give the exact mechanism used by the candidate's non-self-dual example. If \(C=\operatorname{sym}(d\sigma\otimes g)\), then
   \[
   \widetilde g=e^\sigma g,\qquad
   \nabla^{\widetilde g}_XY=\nabla_XY+d\sigma(X)Y+d\sigma(Y)X.
   \]
   For the candidate set \\(g=h_1=e^t h_0\), \\(\sigma=-t\). Then \\(\widetilde g=h_0\) and the displayed identity is exactly \\(\nabla^1=\nabla^0+dt\otimes\mathrm{Id}+\mathrm{Id}\otimes dt\). This is a direct matching calculation, not a priority claim by Ueno about item 3(e). The full text contains no `radial` or `orthog` match and no FMU98 reference. The published version is **“Geodesic connectedness on statistical manifolds with cubic forms divisible by the metric,” Information Geometry 9 (2026), 81–102**, [DOI](https://doi.org/10.1007/s41884-025-00185-0), online 6 December 2025. Its full text was paywalled; proposition numbering above refers specifically to the inspected preprint.

6. **Q. Han, G. Wang, *Hessian surfaces and local Lagrangian embeddings*, Annales de l'Institut Henri Poincaré C, Analyse Non Linéaire 35 (2018), 675–685.** [Primary PDF](https://ems.press/content/serial-article-files/16782?nt=1), [DOI](https://doi.org/10.1016/j.anihpc.2017.07.003). The introduction explicitly cites FMU98 for the question whether Riemannian metrics admit Hessian structures; it is discussing a different question in the same list. Thus this prominent citation and its solution should not be misidentified as a resolution of 3(e). Full text was retrieved and the relevant passage inspected.

7. **S.-I. Amari, J. Armstrong, *Curvature of Hessian manifolds*, Differential Geometry and its Applications 33 (2014), 1–12.** [Institutional author record](https://kclpure.kcl.ac.uk/portal/en/publications/curvature-of-hessian-manifolds), [author-hosted preprint](https://bsi-ni.brain.riken.jp/database/file/325/330.pdf), [DOI](https://doi.org/10.1016/j.difgeo.2014.01.001). The record and preprint introduction concern existence and curvature obstructions for Hessian metrics, rather than the fixed radial distribution of 3(e). This is another nearby citation, not a located anticipation.

Further leads located but not fully inspected: Kurose's 1999 *1-conformally flat statistical manifolds and their realization in affine space* (Fukuoka University Science Reports 29, 209–219); Matsuzoe's 2010 survey (DOI `10.2969/aspm/05710303`, Project Euclid full-text route did not yield accessible text); the 2001 affine-geometry problem-list/bibliography. These are explicit coverage limitations, not negative findings about their full contents. A specialist's historical knowledge could improve this part of the audit; no contact or outreach was prepared or initiated.

## Search record

Searches were conducted through the web search tool on the audit date, with exact-title, exact-problem, terminology, author-combination, and citation-following routes. Results were filtered for primary papers, publisher pages, and author/institutional repositories before making substantive claims. Discovery hits on aggregators were used only to find primary sources. Repeated retrievals and peripheral navigation queries are omitted below; the following are the exact substantive query strings.

```text
"Open problems in affine differential geometry" "3" Furuhata Matsuzoe Urakawa
"radial" "1-conformally flat" statistical manifold integrable
"Open Problems in Affine Differential Geometry and Related Topics" jstage
"statistical" "distribution" "integrable" "Kurose"
"conformally flat" "integrable" "Furuhata" "problem"
"AMR-059-0011"
"Kurose" "Conformally" "Statistical" 1994
"statistical manifold" "radial" "integrability"
"statistical manifold" "geodesic" "orthogonal" "integrable" "conformally"
"statistical manifolds" "radial" "orthogonal"
"geodesic" "integrable" "Matsuzoe" "problem"
"Open problems in affine differential geometry" "3(e)"
"Open problems in affine differential geometry" "conformal"
"6000011" math
"radial distributions" "statistical"
"1-conformally flat" "counterexample"
"integrability" "Kurose" "geodesic"
"statistical manifold" "integrability" "geodesics"
"radial" "1-conformal"
"Statistical manifolds and affine differential geometry" Matsuzoe 2010 pdf
"1-conformally flat statistical manifolds and their realization in affine space"
"Furuhata" "Matsuzoe" "Urakawa" "integrable"
"Kurose" "1-conformally" "Riemannian" "curvature"
"Matsuzoe" "Statistical manifolds and affine differential geometry" pdf 303 321
"1-conformally" "Levi-Civita"
Kurose 1999 209 219 conformally statistical realization
Matsuzoe 2010 statistical manifolds affine differential geometry projecteuclid
"radial" "statistical" "Frobenius"
"radial" "statistical" "Gauss lemma"
"Integrable Radial Distributions"
"Furuhata" "Matsuzoe" "Urakawa" counterexample
"Geodesic Connectedness on Statistical Manifolds with Divisible Cubic Forms"
"conformally flat" "orthogonal distribution" statistical
"statistical manifold" "orthogonal complement" "geodesic" integrable
"statistical manifold" "every distribution"
"1-conformally flat" "negative"
"Furuhata" "Matsuzoe" "Urakawa" "solved"
"10.4036/iis.1998.125" -site:jstage.jst.go.jp -site:link.springer.com
"Open problems in affine differential geometry" -site:scribd.com -site:researchgate.net -site:math.sci.hokudai.ac.jp -site:jstage.jst.go.jp
"Kurose" "radial" "distribution"
"statistical" "integrability of" "radial"
"Curvature of Hessian manifolds" Amari Armstrong 2014
"Foliations and divergences of flat statistical manifolds" Uohashi Ohara Fujii
```

No exhaustive MathSciNet, zbMATH, Google Scholar, non-English, unpublished-work, or forward-citation audit was performed. Search indexing is particularly weak for scanned older articles. Failure to find an explicit answer is not proof that none exists.

## Checkpoints and residual gap

- Initial source checkpoint: **35% of this bounded audit complete**. Original publisher identified; Kurose's pre-existing criterion established the major known ingredient.
- 2026-09-23T03:33:58Z: **75% complete**. Database access limitation and local partial-status flag recorded; Ueno's matched construction identified.
- 2026-09-23T03:37:48Z: **100% of the bounded audit complete**. Nearby citation families and orthogonal-foliation literature screened; no explicit anticipation located. Remaining historical gap: unknown partial result behind the database flag and uninspected older/full-text literature.

**Disposition:** no located direct priority conflict; priority remains unproved. Release only the checkable mathematical result with restrained historical wording and clear attribution of known machinery.
