# Primary sources and exact scope

Checked 13 October 2026 UTC. This is a bounded source and theorem-scope record. It is not a comprehensive bibliography, a worldwide-openness claim, or an audit of every result in the cited papers. Exact public PDF identities and retrieval times are in [SOURCE_METADATA.json](SOURCE_METADATA.json). The PDFs and source text are not redistributed.

## Alfeld's original questions

Peter Alfeld, “Multivariate splines and the Bernstein–Bézier form of a polynomial,” in *Multivariate Splines and Algebraic Geometry*, Oberwolfach Report 21/2015, printed pp.1143–1146. The workshop took place 19–25 April 2015; the full report is volume 12 (2015), pp.1139–1200. The database title's 2016 label does not change the report's year.

- [Institute record](https://publications.mfo.de/handle/mfo/3469)
- [Institute PDF](https://publications.mfo.de/bitstream/handle/mfo/3469/OWR_2015_21.pdf?isAllowed=y&sequence=1)
- [Publisher PDF](https://ems.press/content/serial-article-files/46567)
- [DOI 10.4171/OWR/2015/21](https://doi.org/10.4171/OWR/2015/21)

The complete four-page Alfeld contribution was read. The target printed p.1146, report-PDF p.8, was visually inspected. Item 16 concerns arbitrary cubic vertex values. Item 17 records a positive quartic theorem under a no-collinear-incident-edges hypothesis. Item 18 asks for failure of universal quartic value-and-gradient interpolation. These statements do not authorize subdivision or altered boundary conditions.

The institute and publisher PDFs have different bytes. The extracted target page and preceding PDF pp.6–7 matched after whitespace normalization; notation was checked visually on the institute copy. No complete-PDF text match is claimed. Other report contributions were not audited.

## Alfeld's expanded article

Peter Alfeld, *Multivariate splines and the Bernstein–Bézier form of a polynomial*, Computer Aided Geometric Design 45 (2016), 2–13. [DOI 10.1016/j.cagd.2015.11.007](https://doi.org/10.1016/j.cagd.2015.11.007); [author-hosted PDF](https://peteralfeld.github.io/home/mfo.pdf).

The inspected twelve-page author copy is an article-in-press proof internally dated 17 December 2015. The page references here refer to that author copy, not final journal pagination. Definition 1 and the spline model on pp.1–2, and Sections 9–10 on pp.8–9, were read. Page 8 was visually inspected.

Definition 1 makes the conforming disk model explicit. Theorem 4 gives quartic vertex value-and-gradient interpolation when no two edges attached to the same vertex are collinear. Conjecture 2, p.8, asks for a quartic failure on some permitted mesh. Conjecture 4, p.9, asks for universal cubic vertex-value interpolation. The neighboring cubic dimension Conjecture 3 is a separate question. The full proofs in this article were not independently re-audited.

## Qiu's cubic counterexample

Junkai Qiu, *A counterexample to vertex interpolation by planar C1 cubic splines*, [arXiv:2609.06364v1](https://arxiv.org/abs/2609.06364v1); [versioned PDF](https://arxiv.org/pdf/2609.06364v1).

The checked arXiv record gives a submission date of 6 September 2026, displays only version 1, and displays no journal reference. This is a dated public-record observation; it does not establish whether review occurred elsewhere.

The complete nine-page PDF and references were read. The coordinate specification and triangles on pp.3–4 and the edge-multiplier table were visually checked during independent verification. Theorem 1, p.2, concerns exactly a fixed finite conforming straight-line triangulation of a polygonal disk, with unrestricted boundary vertex data. The example has 41 vertices and 56 triangles. Its edge-multiplier identity gives noninterpolable scalar data. The paper does not resolve the quartic vertex-jet question or refute the separate cubic dimension conjecture.

The [public ancillary Python file](https://arxiv.org/src/2609.06364v1/anc/verify_forest_cubic_counterexample.py) was read as text during reconstruction, but was never imported or executed. The independent mathematical audit reconstructed from the main-text specification and did not execute the author's program. The example, certificate, and negative cubic answer are credited to Qiu; no new-counterexample or priority claim is made here.

## Davydov and Nürnberger on degree at least four

Oleg Davydov and Günther Nürnberger, *Interpolation by C1 splines of degree q≥4 on triangulations*, Journal of Computational and Applied Mathematics 126 (2000), 159–183. [DOI 10.1016/S0377-0427(99)00350-7](https://doi.org/10.1016/S0377-0427(99)00350-7); [author record](https://oleg-davydov.de/s14.html); [author preprint](https://oleg-davydov.de/s14.pdf).

A complete thirty-page author-hosted preprint was obtained. Pages 1–3 and 9–12 were read for scope and visually inspected because direct text extraction had a broken font encoding. Its proofs and remaining pages were not audited. No identity with the publisher's final article is claimed.

Theorem 3.1, p.11, is a Lagrange-interpolation theorem on a possibly modified triangulation Δ*. The preceding construction permits a Clough–Tocher split or a vertex movement in Case 3. Remark 3.4, p.12, explains Hermite substitutions within that construction. This does not establish arbitrary vertex-jet interpolation on every original fixed mesh.

Remark 3.2(ii) describes failure to extend a spline whose other degrees of freedom have already been fixed. That is an obstruction to a sequential construction, and is not by itself an obstruction to prescribing only the final mesh's vertex jets. Its “degenerate edge” terminology concerns a local collinearity, not a zero-area triangle.

## Davydov and Schumaker on stable quartic interpolation

Oleg Davydov and Larry L. Schumaker, *Stable approximation and interpolation with C1 quartic bivariate splines*, SIAM Journal on Numerical Analysis 39 (2002), 1732–1748. [DOI 10.1137/S0036142901384472](https://doi.org/10.1137/S0036142901384472); [author record](https://oleg-davydov.de/s14b.html); [author preprint](https://oleg-davydov.de/s14b.pdf).

The complete eighteen-page author preprint was obtained; only pp.1–3 were visually read. The initial interpolation problem allows finding a triangulation containing the data sites. The opening discussion considers restricted triangulation classes and changes by refinement or edge swapping. Those inspected portions do not establish universal interpolation on a prescribed fixed mesh. Other results and proofs were not inspected or audited.

## Scott on preserving Hermite interpolation

L. Ridgway Scott, *C1 preserving Hermite interpolants for piecewise polynomials in two dimensions*. [Publisher page](https://www.degruyterbrill.com/document/doi/10.1515/jnma-2024-0101/html); [DOI 10.1515/jnma-2024-0101](https://doi.org/10.1515/jnma-2024-0101). The publisher and author bibliography state online publication on 13 August 2025; the DOI's 2024 segment is not the publication year.

The complete paper was not read or retained. The direct publisher route returned HTTP 405, and the author bibliography route timed out or returned HTTP 502. Publisher-indexed primary-source text exposed the abstract, introduction, Section 5.4, and conclusion. Access restrictions were not bypassed.

Those inspected portions give the C1-preserving construction for degree n≥5. Section 5.4 describes a degree-four analogue lacking the required guarantee and discusses triangulation choice or refinement. Failure of that particular operator to preserve C1 is not a proof that no quartic interpolant exists. No complete resolution of Alfeld's exact quartic assertion follows from these inspected portions.

## Scope of the literature conclusion

The review checked the named primary sources and targeted Alfeld, quartic, function-value, gradient, and counterexample leads. It did not establish a verified complete resolution of the quartic assertion. Older approximation-order and stability papers cited by Qiu were seen in the references but not independently audited here. No claim about their exact theorem statements is needed for the accepted cubic proof.
