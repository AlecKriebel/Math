# Source and scope audit

Checked 3 October 2026. This file records what each source supports; it does not claim an exhaustive bibliography.

## Original question

- Catalogue page: https://www.unsolvedmath.com/problems/30002086 . The web retrieval was inaccessible. A pinned catalogue record was used to identify OWR-11789-007; the mathematical statement was then checked against the original report, rather than accepted from the catalogue.
- Official publisher landing page: https://ems.press/journals/owr/articles/11789 . It identifies *Geometrie*, Oberwolfach Reports 9 (2012), no. 2, 1639–1686, DOI 10.4171/OWR/2012/27. The workshop was 20–26 May 2012; online publication was 20 February 2013. Thus a catalogue label “Geometrie (2013)” reflects the online-publication date, not the report's bibliographic year.
- Original PDF: https://ems.press/content/serial-article-files/46397 . Haslhofer's contribution, joint work with Reto Müller, starts on p. 1668. The normalized shrinker equation, entropy convention, and positive gradient bound (equation (5)) are on p. 1669; the statement that its universal validity remains open is at the beginning of p. 1670. The equation page was also visually checked after rendering the official PDF.
- The author's separate extract is readable through web extraction at https://www.math.utoronto.ca/roberth/papers/Haslhofer_owr_singularities.pdf . A direct download at that address returned a short HTML response, not a valid PDF. The official publisher PDF was successfully retrieved and used instead.

Scope: the source poses the condition in a theorem about four-dimensional shrinkers. The catalogue states it for a complete shrinking Ricci soliton without specifying dimension. The report supports at least the four-dimensional question; the investigation separately labels the stronger all-dimensional formulation and proves neither in full. No scalar-curvature bound, Ricci bound, Kähler hypothesis, or noncompactness assumption may silently be added. The compact case is already vacuous under the actual quantifiers.

## Foundational and historical papers

1. R. Haslhofer and R. Müller, *A compactness theorem for complete Ricci shrinkers*, Geom. Funct. Anal. 21 (2011), 1091–1116. DOI: https://doi.org/10.1007/s00039-011-0137-4 ; preprint: https://arxiv.org/abs/1005.3255 .
   - Section 2, equations (2.1)–(2.7): soliton, scalar, Hamilton identities and potential growth.
   - Lemma 2.1: minimizing basepoint and explicit growth estimates.
   - Theorem 1.2 and subsequent Remark, preprint pp. 3–4: the gradient assumption and the sufficient scalar bound with coefficient strictly below 1/4.
   - Equation (2.16): the additive Hamilton constant equals minus the entropy with the mass-one convention.
   - The requested estimate is not supplied unconditionally by this paper.

2. R. Haslhofer and R. Müller, *A note on the compactness theorem for 4d Ricci shrinkers*, Proc. Amer. Math. Soc. 143 (2015), 4433–4437. DOI: https://doi.org/10.1090/proc/12648 ; preprint: https://arxiv.org/abs/1407.1683 .
   - Introduction and Theorem 1.1, preprint pp. 1–2: orbifold compactness with only an entropy lower bound.
   - Section 2, preprint pp. 2–5: replaces the former localized Gauss–Bonnet argument by a local curvature estimate using Cheeger–Naber and conformal rescaling.
   - Theorem 1.1 does **not** state that the gradient bound holds for every shrinker. Removal of a hypothesis from a theorem by a new proof is not proof of that hypothesis.
   - Estimates (2.1) and (2.4) have constants depending on distance from a minimizing basepoint. They do not automatically give uniform smooth geometry about arbitrary escaping basepoints.

3. F. Fang, J. Man and Z. Zhang, *Complete gradient shrinking Ricci solitons have finite topological type*, C. R. Math. Acad. Sci. Paris 346 (2008), 653–656. Primary sources: https://arxiv.org/abs/0801.0103 and https://www.numdam.org/item/CRMATH_2008__346_11-12_653_0/ .
   - Theorem 1 has additional Ricci bounds or Ricci-lower/injectivity assumptions in the more general Bakry–Émery setting.
   - Theorem 2 assumes bounded scalar curvature for a shrinker.
   - Conjecture 3 asks for general finite topological type.
   - Section 2 supplies the geodesic-integral method. RESULT.md recalculates the unit-cutoff endpoint coefficient exactly.
   - The title must not be used to remove the hypotheses printed in the theorem.

## Recent status checks

4. A. Bertellotti and R. Buzano, *Ends of (singular) Ricci shrinkers*, Selecta Math. (N.S.) 32, article 1 (2026), published online 18 November 2025: https://doi.org/10.1007/s00029-025-01104-y .
   - Introduction following Theorem 1.3: no far-out critical points is an assumption, with bounded scalar curvature or a strict quadratic coefficient below 1/4 supplied as sufficient conditions.
   - Section 5 distinguishes curvature-bounded moduli spaces and the local compactness results.
   - Proposition 3.6 and Appendix A give the product-level-set flow mechanism. The paper does not establish the unrestricted positive gradient lower bound.
   - Full article HTML was inspected. An institutional PDF download returned 403; that unsuccessful download is not presented as evidence.

5. F. He, *Topology of gradient Ricci shrinkers via weighted L2 cohomology*, arXiv:2605.04476v1, 6 May 2026: https://arxiv.org/abs/2605.04476 .
   - Introduction: finite topological type is discussed as an unresolved extension from the Kähler to the general setting.
   - Theorems 1.1–1.4 impose their explicit curvature hypotheses; in particular Theorem 1.4 assumes a Ricci growth bound.
   - This is a recent preprint, not evidence that no later paper exists. It is corroboration of the continuing distinction between general and curvature-restricted geometry.

A current Kähler-specific paper, T. Xu and Z. Zhang, *Compactness and Rigidity of Complete Kähler Ricci Shrinkers*, arXiv:2608.10953, https://arxiv.org/abs/2608.10953 , was also identified. Its abstract is explicitly Kähler-specific; no conclusion about arbitrary Riemannian shrinkers is drawn from it. It is not used as a proof source in RESULT.md.

## Prior-attempt boundary

The live queue row for rank 502 / problem 30002086 was checked on main and read “queued”, 0/5. Exact-ID default-branch code search and exact-ID branch-name search returned no matches. The pinned research-results collection had no matching OWR code or matching exact title in the searches performed. Adjacent Ricci-soliton investigations concern different statements and were not treated as attempts on this problem. These bounded searches do not assert that every historic, deleted, or differently named branch was inspected.

## Local verification and limitations

`checks/check.py` verifies the coefficient expansion, index-form cutoff integrals, weighted Bochner algebra, Gaussian and product controls, summable bump-width bound and center estimates, the scaled cigar's Ricci tensor and Hessian, and metric-rescaling identities. It uses exact SymPy arithmetic, not a numerical search.

The geometric proofs and the smooth infinite bump construction are written out in RESULT.md. The script does not prove a global curvature estimate or the existence/nonexistence of a hypothetical bad shrinking soliton. No full-resolution claim, novelty claim, or publication authorization is contained in this packet.
