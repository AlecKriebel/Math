# Independent primary-source review

Checked 2026-10-01. Exact target 30003216 / OWR-14750-001. The original disposition remains unsolved, five substantive author turns consumed.

## Original formulation

I read the full Ku contribution in OWR42/2016, printed p.2422, and visually inspected its displayed equation and final paragraph. The method computes a coarse conforming primary solution, then a fine H(div) flux. This is hybridization of mesh sizes. The announced flux estimator combines mixed-method terms with higher-order additions, but the contribution does not state their local formula, a marking/coupling rule or a delta policy. Its scalar right-hand side is printed against a vector test function. [Official MFO source](https://publications.mfo.de/bitstream/handle/mfo/3546/OWR_2016_42.pdf?isAllowed=y&sequence=1).

## Published equation and estimator distinction

Ku–Lee–Sheen, ESAIM:M2AN51(2017),1303–1316, equation(2.6) on p.1305 supplies the test-function divergence, including the boundary pairing for nonzero Dirichlet data. I checked that equation visually and read §5.1, including the hypotheses of Theorem5.2 on p.1311. Its recovery estimator controls the primary energy error under the relative flux-accuracy assumption m(H). It is not an inspected formula for the OWR local augmented flux estimator. The author uses homogeneous Dirichlet data, so the boundary term vanishes legitimately. [Full primary PDF](https://www.numdam.org/item/10.1051/m2an/2016062.pdf); [current archive record](https://archive.numdam.org/articles/10.1051/m2an/2016062/).

## Credited later and classical inputs

- Adhikari–Kim–Lee–Sheen, Numerical Methods for PDE40(2024),e23120, §3.2 already gives the augmented-Lagrangian Uzawa interpretation. The full primary copy and publisher text support the author's credit. [NSF primary copy](https://par.nsf.gov/servlets/purl/10535958); [publisher](https://onlinelibrary.wiley.com/doi/abs/10.1002/num.23120).
- Carstensen–Hoppe's 2006 institutional primary text explicitly requires data reduction in addition to bulk marking for its convergent algorithm. I inspected this discussion and the estimator/refinement statements. The author does not import it as an unconditional theorem for the hybrid flux: Turn2 states a conditional transfer, and Turns3–4 provide their own convergence arguments. [Primary copy](https://edoc.hu-berlin.de/bitstreams/b245c06f-a852-485c-bac4-20ffe662986c/download).
- Durán, arXiv1103.3718, Theorem3.2 and preceding definition apply to a bounded domain star-shaped with respect to a ball and zero-mean L2 data. The author's affine mean correction removes the zero-mean restriction without imposing an unintended normal boundary condition. [Primary paper](https://arxiv.org/abs/1103.3718).
- Guermond's RT notes, Lemma16.2 and Theorem16.4, apply to the H1 vector lift used here and give the commuting projection and mesh-uniform local stability. [Chapter16](https://people.tamu.edu/~guermond/M661_FALL_2023/chap16.pdf).
- Guermond's scalar elliptic notes, Theorem27.26, give homogeneous-Dirichlet H2 regularity on a convex domain for the identity coefficient. This is used only in Turn5, not on arbitrary nonconvex polygons. [Chapter27](https://people.tamu.edu/~guermond/M661_FALL_2017/chap27.pdf).

All seven local primary PDF hashes match the frozen source manifest. The equations and hypotheses required by the proofs were inspected; no adaptive-convergence conclusion is inferred from a title or abstract.

## Current access limits

The publisher's indexed 2026 preview confirms the forthcoming JCAM486, November2026,117609 article on an iterative reduced-mixed method and describes an adaptive construction. Direct opening returned403 during this independent check; the full article was not obtained. Its exact theorem or equivalence to the OWR procedure is therefore not certified. [Publisher preview](https://www.sciencedirect.com/science/article/abs/pii/S0377042726002529). This preserves, rather than closes, the stated source-identification gap.

No novelty or comprehensive historical-openness conclusion follows from this audit. Downloaded PDFs, extracted full texts and rendered pages are excluded from the portable review.
