# Citation evidence and mechanism comparisons

Checked 2026-10-13 UTC. The manifest binds retrieved bytes and identifies private source paths. “Fulltext” means a complete document was retrieved and the relevant portions were read, not that every sentence was independently verified. Public summaries below are original analytical notes, not reproduced source text. No raw paper, extracted text, image or API response is public.

## Direct primary anchors

- **OWR2025**, [report PDF](https://ems.press/content/serial-article-files/52249), Meier contribution pp. 1624-1626. Printed p. 1625 was visually inspected on PDF page35. It fixes a suitable energy, proves regularity for homotopy minimizers, and poses Question 1 for harmonic spheres. This supports a dated source binding, not a present-day openness claim.
- **MVW_V1**, [arXiv v1 PDF](https://arxiv.org/pdf/2503.08553v1), Question 1.9; Definition 3.1; Definition 6.1; Theorem 3.2/Corollary 3.3. General energies explicitly include E_+^2 and KS. Locality is every point's neighborhood, every relatively compact Lipschitz subdomain, and every same-trace W1,2 competitor. Theorem 3.2 instead assumes every sphere biLipschitz reparametrization. References[20]-[22],[25],[29],[31] initiate the backward graph.

## Reparametrization/energy-area family

- **LW_PLATEAU**, [author PDF](https://www.mi.uni-koeln.de/~alytchak/preprints/Plateau.pdf), Theorem 6.8/Lemma 6.9 pp. 31-32, visually checked p. 31. The complete-target KS distortion constant is2sqrt(2)+sqrt(6). Its hypothesis minimizes over all disc biLipschitz homeomorphisms, which can move boundary values. The introduction p. 7 distinguishes the classical inner-product derivative method from non-Euclidean normed tangents. The sphere stress argument supplies its pointwise SL(2)-minimality premise by matrix convexity, so the sharper constant applies to the companion theorem; the global sphere argument is still required.
- **LW_ENAREA**, [author PDF](https://www.mi.uni-koeln.de/~alytchak/preprints/enarea.pdf), Definition 3.1; Lemma 3.1; Lemma 4.1; Section 3.3. The key pointwise hypothesis is SL(2)-minimality. The equivalence with energy-area equality uses all reparametrizations. Matrix convexity and polar decomposition supply the stationarity-to-SL(2)-minimality argument once T(s)=0; the known sharper pointwise KS bound therefore applies. See PUBLICATION_REVIEW_CORRECTIONS.md at the package root.
- **FW_MORREY**, [primary preprint](https://arxiv.org/pdf/1910.06534), Proposition 1.1, Theorem 1.2/1.4, Corollary 1.3. The domain metric or parameterization is varied to approach energy-area equality. A conformal neighborhood of the boundary is not identical to fixing its parametrized trace. This does not negate local scalar saturation.
- **SW_HOMOTOPY**, [primary preprint](https://arxiv.org/pdf/2012.15530), introduction and relative1-homotopy framework. Its minimization and topological comparison family differs from the candidate's local-only property. It is a dependency of MVW's existence machinery, not an authenticated negative example.

## Fixed-trace regularity and forward primary followups

- **LW_REGULARITY**, [primary preprint](https://arxiv.org/pdf/1512.01060), Definition 1.1 and Theorems1.3/1.4. The definition uses fixed traces and establishes Holder regularity. Equivalence of quasi-harmonic classes across comparable energies allows the quasi-minimizing factor to change; this does not identify their1-minimizers.
- **LW_CANONICAL**, [primary preprint](https://arxiv.org/pdf/1701.06346), introduction, Theorem 1.2 and sphere parameterization Section 6. The minimization is among spanning/parameterizing maps. Its canonical quasiconformal representatives are consistent with the candidate's failure of global minimality.
- **CS_MAXIMAL**, [primary preprint](https://arxiv.org/pdf/1909.10385), introduction, Section 2.1.5 and Section 6. It studies canonical energy-minimizing parameterizations and maximal metric surfaces. No exact compact-sphere local-minimizer counterexample was matched in the inspected portions.
- **NR_POLYHEDRAL**, [primary preprint](https://arxiv.org/pdf/2107.07422), introduction and minimal-disc dependency paragraph. Polyhedral approximation and one-sided uniformization are different existence problems. Its citation of LW does not imply the local-harmonic-sphere conclusion.

## Hopf/stress family with checked target restrictions

- **KS1993**, [publisher full PDF](https://intlpress.com/site/pub/files/_fulltext/journals/cag/1993/0001/0004/CAG-1993-0001-0004-a004.pdf), Chapter2 introduction, Lemma 2.3.1/Theorem 2.3.2 pp. 624-627. NPC comparison yields the parallelogram identity needed for a bilinear pullback tensor. This restriction is explicit and essential to that theorem. The companion's angular stress on arbitrary seminorms is a different construction.
- **BM2021**, [NSF-hosted primary article](https://par.nsf.gov/servlets/purl/10326826), Theorem 1.2/1.3 and Section 2.2. The target is a locally CAT(kappa) sphere; KS/Dirichlet energy is used. Its conformal degree-one harmonic homeomorphisms do not prohibit the candidate with operator-norm energy.
- **SAGMAN2023**, [primary preprint](https://arxiv.org/pdf/2303.04471), Section 2.3. The complete target is explicitly an NPC length space. Its metric Hopf statement is downstream of KS1993 Theorem 2.3.2; it is not an unrestricted complete-target theorem.
- **MS2023**, [primary preprint](https://arxiv.org/pdf/2301.00249), Section 2.1. The same NPC restriction precedes the Hopf formula. Products of R-trees and their minimal maps are important classical stress precedents, but their curvature hypothesis cannot silently be dropped.

## Calibration and older/smooth analogues

- **PANKKA2020**, [journal full PDF](https://www.acadsci.fi/mathematica/Vol45/vol45pp0975-0990.pdf), Theorem 1.6 and Section 2. Closed-form comparison is made with continuous homological competitors. It is established calibration background; those assumptions differ from arbitrary same-trace W1,2 maps into the compact sphere.
- **HPP2021**, [primary preprint](https://arxiv.org/pdf/2106.11871), Section 5/Theorem 5.1. Calibrated conformal curves in Euclidean targets minimize the relevant energy. It supplies direct primary evidence for standard energy/form comparisons. The candidate additionally arranges a globally exact form on a compact sphere and justifies Sobolev boundary invariance.
- **LI2014**, [journal full PDF](https://www.impan.pl/shop/en/publication/transaction/download/product/87919), Sections2.2/3. A smooth nondegenerate Finsler-map energy and its F-stress tensor are used. Its conformality-to-homothety assertion is not the arbitrary-target KS sphere distortion claim.
- **NISHIKAWA2010**, [institutional full note](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1720-04.pdf), introduction and metric/energy definitions. Smooth strongly pseudoconvex complex Finsler geometry has separate variational notions. The related2015 [publisher DOI](https://doi.org/10.1142/S0129167X15410104) was only a preview/discovery lead here; it uses dbar-energy. Do not credit it as an inspected generic KS theorem.
- **SOULTANIS2016**, [institutional thesis fulltext](https://helda.helsinki.fi/server/api/core/bitstreams/c81e895c-bc7e-4fda-b9b4-3f8c85ec0a8e/content), introductory Part3. p-energy minimizers in homotopy families and NPC targets are the relevant themes. The author is Elefterios Soultanis; the private retrieval filename is a provisional label and does not identify the author.

## Explicit metadata-only and access gaps

- [Sacks-Uhlenbeck1981 publisher record](https://annals.math.princeton.edu/1981/113-1/p01) authenticates author/title/date/pages, but the original fulltext download was unsuccessful. Credit the classical conformality result, also stated in MVW, rather than claiming its smooth-target special case as new. The sphere stress calculation independently recovers this special case.
- [Harvey-Lawson1982 DOI](https://doi.org/10.1007/BF02392726) and [McShane1934 DOI](https://doi.org/10.1090/S0002-9904-1934-05978-0) identify standard background. Fulltexts were not authenticated in this run; the candidate gives the actual extension/calibration arguments, and later primary calibration proofs were inspected.
- [Reshetnyak1968 publisher record](https://link.springer.com/article/10.1007/BF01040913) is subscription metadata with outgoing references. No theorem-level exclusion or exact-match claim is made from its title. The fulltext remains an older-source priority gap.
- [MVW2026 DOI](https://doi.org/10.1515/crelle-2026-0042), [author bibliography](https://people.math.ethz.ch/~damameier/research.html), [ETH handle](https://hdl.handle.net/20.500.11850/801644) and Crossref metadata authenticate publication identity. They do not authenticate the final question's status or scope. Direct final HTML/PDF/XML endpoints returned zero bytes.

CITATION_GRAPH.json records checked backward edges and bounded metadata-only forward edges. All metadata-only citers not followed to primary text remain discovery leads, not exclusions.71 query strings and the access protocol are in QUERY_LOG.md. No first-priority or exhaustive-coverage claim is supported.

## Final published-bibliography followups

- **BL2018/2020**, [primary preprint](https://arxiv.org/pdf/1802.08905), Theorem 0.1, Definition 1.1 and Section 1. The target is compact locally CAT(1); harmonicity is formulated with a small target-ball competitor class. Its bilinear pullback tensor/Hopf argument is curvature-dependent. Bubble-tree energy quantization is a different conclusion.
- **PARKER1996**, [author-hosted primary PDF](https://users.math.msu.edu/users/parker/harmonicmaps.pdf), introduction pp. 595-597, energy equation(0.1), Proposition 1.1 and main theorem context. The full39-page PDF was available through the web reader, though direct downloads returned a short HTML denial. Compact Riemannian targets and ordinary Dirichlet energy are explicit. The counterexamples concern convergence of sequences, not the submitted operator-norm sphere or arbitrary-metric KS distortion.

Crossref references4 and29 list these works. This is a metadata-only citation relation; the comparison of their mathematical assumptions is based on their own inspected primary text. The final MVW theorem/question still remains uninspected.

Release revision 2026-10-14T03:51:52.926694+00:00: root repaired R1/R2 after reviewer01; the initial sealed report is in history/initial_revision. See package-root PUBLICATION_REVIEW_CORRECTIONS.md.
