# Source and scope adjudication: barycentric hyperplanes

Checked 14 October 2026 UTC. Target: row 1779, problem 30004514, source key OWR-1703876-007.

## Finding

The recovered sources remain ready for a credited proof audit. No later primary-source change located in this bounded refresh alters that assessment. Myroshnychenko, Tatarko, and Yaskin (MTY) have a published result in *Advances in Mathematics* 461 (2025), article 110081; its directly inspected author manuscript states a counterexample in every dimension at least five. That dimensional range suffices to refute the universal question over all dimensions at least three, provided the construction is accepted or independently verified. This report verifies attribution, source identity, versions, statements, and hypothesis matching; it does not certify either construction's proof.

Wang, Xiong, and Yang (WXY) separately state examples in every dimension at least three in arXiv:2606.19865v2. Their all-dimensional result remains publicly labeled submitted. It must not be described as a verified journal publication, a new result of this audit, or a theorem certified by checking its title and abstract.

## Exact source and target

The source is Zuzana Patáková's contribution, joint with Martin Tancer and Uli Wagner, “Barycentric cuts through a convex body,” printed pp. 1502–1503 of *Discrete Geometry*, *Oberwolfach Reports* 17 (2020), no. 2/3, pp. 1469–1528, report 30/2020. [EMS metadata](https://ems.press/journals/owr/articles/1703876) records publication on 2 July 2021; the report year is 2020. [Official report PDF](https://ems.press/content/serial-article-files/46867?nt=1), PDF pp. 34–35, was independently viewed and freshly downloaded.

The target is Q2 on printed p. 1502. It specializes Q1 to the body's barycenter, so it inherits both the bound of n+1 distinct hyperplanes and the dimension range n≥3. The imported formulation omitted that dimension range. Restoring it follows the primary source and does not introduce an extra hypothesis.

In explicit notation, the question concerns every integer n≥3 and every compact convex set K⊂R^n with nonempty interior. Its centroid is g=vol_n(K)^{-1}∫_K x dx. The requested hyperplanes H contain g and satisfy vol_{n−1}(K∩H)^{-1}∫_{K∩H} x dvol_{n−1}=g, with the induced Euclidean measure on H. There are no smoothness, strict-convexity, symmetry, or polytope requirements. The section through the interior point g has positive induced volume.

Three independent primary conventions agree:

- OWR p. 1502 explicitly defines convex body as compact, convex, and with nonempty interior, and a barycentric hyperplane by the centroid of its section.
- MTY v2 p. 1 defines the body's centroid using Lebesgue volume; Problem 1 is the n+1 section-centroid question. WXY v2 p. 1 explicitly writes both the n-dimensional body and (n−1)-dimensional section centroid integrals using Hausdorff measure. The standard normalization of these measures cancels in the centroid ratio.
- OWR writes H through p as the zero set of ⟨v,x−p⟩. Hence v and −v specify the same geometric hyperplane. PTW's published SoCG paper p. 62:4 explicitly notes this identification; WXY v2 p. 2 likewise equates two antipodal critical normals with one qualifying section. The requested count is unoriented.

Grünbaum's original 1961 article, [*On some properties of convex sets*](https://doi.org/10.4064/cm-8-1-39-42), printed p. 41, independently corroborates the interior-point question followed by its centroid specialization. Its [public scholarly scan](https://bibliotekanauki.pl/articles/967758.pdf) was inspected at the right half of PDF p. 2. It records the planar case separately. The exact queued target is nevertheless pinned to the later OWR Q2 with its explicit inherited range.

## MTY: statement, version, publication, and access

Sergii Myroshnychenko, Kateryna Tatarko, and Vladyslav Yaskin, [*Answers to questions of Grünbaum and Loewner*](https://doi.org/10.1016/j.aim.2024.110081), *Advances in Mathematics* 461 (February 2025), article 110081.

The current [arXiv record](https://arxiv.org/abs/2404.15188) lists v1 on 23 April 2024 and latest v2 on 7 November 2024. The freshly downloaded [v2 PDF](https://arxiv.org/pdf/2404.15188v2) is 167,961 bytes, SHA-256 970f4af59ffb9cd4d24530b8614c57b4391a269efa966100665dfe9e2fda9b46, exactly matching the recovered source.

Directly inspected locations are p. 1 (definitions and Problem 1), p. 2 (claimed dimensional conclusion), and p. 4 (Theorem 3). The theorem supplies a convex body with centroid at the origin for n≥5 and a strictly positive last coordinate of the section centroid away from normals ±e_n. Those normals describe a single hyperplane. For an exactly-one conclusion, one must also justify that the remaining section centroid is the origin, using the constructed body's axial symmetry or an applicable existence theorem; a vanishing last coordinate alone is not a zero vector. That verification belongs to the construction audit. For the negative n+1 conclusion, the theorem's at-most-one exclusion already has sufficient scope.

Publication identity is independently corroborated by the [publisher's indexed article record](https://www.sciencedirect.com/science/article/pii/S0001870824005978), the [publisher-deposited Crossref record](https://api.crossref.org/works/10.1016/j.aim.2024.110081), [Tatarko's institutional publication list](https://www.math.uwaterloo.ca/~ktatarko/publications.html), and [Yaskin's institutional publication list](https://www.math.ualberta.ca/~vladyaskin/). Crossref lists the same title, three authors, volume, article number, and February 2025 publication date. Its record creation date is 16 December 2024; that field is not treated as an independently verified online-publication date.

The journal PDF was not recovered. Earlier ScienceDirect access returned 403; a current DOI opening returned a tool error. No bypass, purchase, login, or outreach was attempted. Permitted author/institutional full-text routes were checked: Tatarko's and Yaskin's links lead to the arXiv manuscript; Myroshnychenko's current author site and targeted institutional searches exposed no independently recoverable journal PDF. Yaskin lists the journal paper as 11 pages, whereas arXiv v2 has 10 PDF pages. This does not establish a mathematical difference, but neither byte equivalence nor a version-of-record proof comparison is asserted.

No withdrawal or later version appears on the current arXiv page. No correction/retraction relation is present in the retrieved Crossref record, whose relation field is empty and whose update-to/updated-by fields are absent. Bounded exact-title/identifier searches found no relevant primary correction or withdrawal notice. These are qualified negative findings, not an exhaustive certification that no notice exists.

## WXY: all-dimensional manuscript claim

Shouda Wang, Ge Xiong, and Kaiwen Yang, [*A complete solution to the Grünbaum–Loewner centroid problems*](https://arxiv.org/abs/2606.19865v2), v2, 31 July 2026. The latest [arXiv page](https://arxiv.org/abs/2606.19865) still lists only v1 (18 June) and v2. Its current comments credit independent simultaneous work by Wang and by Xiong–Yang. The v2 PDF and current author list must be used instead of stale two-author v1 search snippets.

The fresh [v2 PDF](https://arxiv.org/pdf/2606.19865v2) is 407,327 bytes, SHA-256 21e91319797e8d4b5ececf4d4d8c4c4cc1814bd47422edeb9a3e3ffdfff8b53e, exactly matching the recovered source. Theorem 1.1, p. 2, directly states a smooth strictly convex example for each n≥3 with a single qualifying section. Its regularity is an additional feature of the examples; it does not narrow the original class of bodies in a way that prevents a counterexample from applying. Definitions on p. 1 and the antipodal-normal discussion on p. 2 match the target's measures and count.

[Wang's current author page](https://wsdustcx.github.io/My-website/) labels this work submitted, and the current arXiv record has no journal reference. The [ICERM workshop program](https://icerm.brown.edu/program/Hot%20Topics%20Workshop/htw-26-sgp) also contains the author-announced all-dimensional claim; a talk announcement is not publication or proof certification. No later primary version, withdrawal, correction, or journal publication was found in this bounded refresh. This report leaves the all-dimensional proof to separate inspection.

## Scope and chronology safeguards

- OWR Q1 asks for the existence of some suitable interior point. It does not require that point to be the volume centroid. WXY v2 Remark 1.2, p. 3, continues to describe that separate question as open for n≥4. A negative answer to Q2 does not negate Q1.
- PTW's [SoCG 2020 publication](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2020.62), Corollary 9 and Theorem 10 on p. 62:4, gives respectively three and four barycentric hyperplanes at the maximal Tukey-depth point. That point cannot generally be replaced by the volume centroid. Proposition 11 concerns critical directions for a fixed interior point. The triangular-prism example concerns depth-realizing hyperplanes; Remark 7 explicitly separates it from a counterexample to either centroid/interior-point question.
- A barycentric section is not a demand that H bisect K's volume, and it does not mean that the two half-bodies have equal centroids. OWR Q3 has the stronger bound 2^n−1, visually checked on printed p. 1503.
- [Huang–Myroshnychenko–Tatarko–Yaskin v2](https://arxiv.org/abs/2606.04482v2), dated 4 June 2026, still says the Euclidean dimensions 3 and 4 are open. This predates WXY v1 and v2.
- [Haddad–Jiménez–Villa](https://doi.org/10.1007/s12220-026-02570-2), *Journal of Geometric Analysis* 36 (2026), 321, retains a statement of openness in dimensions 3 and 4. Its publisher records receipt on 16 January, acceptance on 1 August, and publication on 12 August 2026. A later publication date does not make that inherited literature statement a refutation of the July manuscript or establish when the authors last checked it.

## Evidence boundary

All eight recovered scholarly PDFs were rehashed and match their recorded sizes and hashes. The three core PDFs (OWR, MTY v2, WXY v2) were independently redownloaded and match byte-for-byte. Both retained public dataset corpora were rehashed; the target record's source identity and specialization match OWR Q2. Only source metadata, counts/match results, hashes, and authored analysis are included in the public provenance manifest. Source PDFs, extracts, screenshots, raw dataset records, and private working files are excluded.

The remaining source-access limits are the absent MTY journal PDF and absent expanded PTW 2022 journal PDF. The published SoCG paper and accessible author manuscripts suffice for this source/scope adjudication. This report makes no new novelty claim and does not independently certify proof resolution.
