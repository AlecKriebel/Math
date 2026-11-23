Editorial note: The complete authored text is preserved below. Only references to undistributed operational artifacts, their identities, locations and replay directions have been replaced with descriptive prose. Mathematical arguments, evidence counts, corrections and limitations are retained. This prose edition identifies its distributed files and public scholarly sources. Historical conditions in the source record are distinguished from current dependency status in ACCEPTANCE_AND_DEPENDENCIES.md.

# Three-color tournament source verification

Recovery verification: The original ledger body below was reconstructed exactly: [verified original byte count omitted], SHA-256 [verified undistributed artifact identity], matching the retained original verification manifest. This added notice makes the present file a distinct edition. All source retrievals, readings, visual checks and search findings below describe the historical inspection on 12 October 2026, completed before 13:04 UTC. At recovery verification, the restored Georgakopoulos–Sprüssel PDF was checked locally against its historical byte count and hash; this was a byte-identity check, not a new retrieval, source-proof reading, or new literature search. No present access to the other historically inspected PDFs is asserted.

Verification date: 12 October 2026 UTC.

## Result and exact scope

No applicable full resolution was identified in this bounded primary-source search. This is a search result, not a proof that the conjecture remains open today. The inspected 2019 paper treats the relevant three-color case as part of its open question; later papers found below concern additional restrictions or different conclusions.

The [Open Problem Garden statement](https://www.openproblemgarden.org/op/monochromatic_reachability_vs_rainbow_triangles), posted 15 July 2008 and retrieved again for this review, asks whether every finite tournament with arcs colored from three colors has either a rainbow **directed 3-cycle**, or one vertex from which every other vertex can be reached by a monochromatic directed path. The path color can vary with the destination. A transitive rainbow triple is not the forbidden configuration. The incoming monochromatic-sink formulation becomes this outgoing formulation upon reversing every arc. This equivalence preserves all color-incidence and cycle-switch conditions.

The problem is credited to B. Sands, N. Sauer and R. Woodrow, *On monochromatic paths in edge-coloured digraphs*, J. Combin. Theory Ser. B 33(3) (1982), 271–275, [DOI](https://doi.org/10.1016/0095-8956(82)90047-8). Attribution is verified through the problem page and subsequent primary papers; an actual original 1982 PDF was not obtained. The attempted publisher PDF response was HTML, not a paper, and is not counted as inspection.

## Core paper: Georgakopoulos–Sprüssel

Agelos Georgakopoulos and Philipp Sprüssel, [*On 3-coloured tournaments*](https://arxiv.org/abs/0904.1967), [v2 PDF](https://arxiv.org/pdf/0904.1967v2).

- arXiv v1: 13 April 2009, 16:53:01 UTC. v2: 17 April 2009, 09:54:06 UTC.
- The title page displays 16 November 2018. PDF metadata contains a 2021 creation date. Neither is a new submission or new mathematical result.
- The [author's current publication list](https://agelos.neocities.org/pubs), read on the verification date, explicitly lists this work as a preprint. No journal publication is asserted here.
- The arXiv v2 comment acknowledges that the main result had appeared earlier. The local-at-most-two-incident-colors theorem is credited to Galeana-Sánchez and Rojas-Monroy, not presented as new to this review or to the 2009 authors.
- Inspection: all nine pages of extracted PDF text read; Section 2 arguments inspected and exact hypotheses checked; page 5 visually checked for Proposition 2.8, Problem 2.1 and Theorem 3.1. Section 3 proof text was read, but this report is not an independent certification of the entire paper.

### Existing unrestricted minimal-counterexample reductions

All references in this subsection are to the 2009 paper. Let D be an induced-subtournament-minimal counterexample to its Conjecture 1.2, and let C be its distinguished directed Hamilton cycle. These results are already in the literature and must be credited accordingly.

1. Lemma 2.1, credited to Shen: each vertex monochromatically reaches every vertex except its predecessor on C. The cycle having this obstruction property is unique up to rotation. This does not assert that D has only one Hamilton cycle.
2. Lemma 2.3: D is also minimal with no vertex reachable monochromatically from all other vertices. This supports applying the argument after reversing all arcs.
3. Proposition 2.4: at each vertex the incoming arcs use at least two colors, and the outgoing arcs use at least two colors.
4. Lemma 2.5: whenever y is not the predecessor of x, x reaches y monochromatically inside the interval-induced subtournament D[xCy]. An arbitrary previously chosen color need not survive the restriction; a uniquely possible color does.
5. Observation 2.6: no vertex can reach x in a color in which x's successor reaches that vertex. Otherwise monochromatic composition violates the predecessor obstruction.
6. Lemma 2.7: at a switch on C with incident colors a and b, the predecessor beats the successor directly, while the successor reaches the predecessor only in the third color.
7. Proposition 2.8: the arcs of C cannot alternate between two colors. Immediately following Problem 2.1 asks about periodic alternation among three colors; it is not resolved by that proposition.
8. Theorem 3.1: every vertex of a minimal counterexample is incident with all three colors. This is stronger than merely saying that some vertex uses all three colors, but it is still a necessary condition, not the conjecture.

## Earlier credit and related restrictions

Hortensia Galeana-Sánchez and Rocío Rojas-Monroy, [*Monochromatic Paths and at Most 2-Coloured Arc Sets in Edge-Coloured Tournaments*](https://link.springer.com/article/10.1007/s00373-005-0618-z), Graphs and Combinatorics 21 (September 2005), 307–317, DOI 10.1007/s00373-005-0618-z. Publisher abstract and bibliographic record inspected; original proof not obtained. It states the monochromatic-sink theorem when each vertex meets at most two colors, with an extra no-rainbow-directed-triangle condition in the three-color case. This independently verifies the credit and hypothesis boundary in the 2009 paper. Acceptance date 26 April 2004 is distinct from publication.

Shen Minggang, [*On monochromatic paths in m-coloured tournaments*](https://www.sciencedirect.com/science/article/pii/0095895688900597), J. Combin. Theory Ser. B 45(1) (August 1988), 108–111, DOI 10.1016/0095-8956(88)90059-7. Publisher abstract/search rendering inspected; direct page retrieval returned 403 and attempted PDF retrieval returned HTML. The abstract excludes **every** rainbow three-vertex tournament, both cyclic and transitive. Its structural lemma is inspected through the explicit reproof in the 2009 primary paper, not through an unreceived original PDF.

M. Melcher and K. B. Reid, [*Monochromatic sinks in nearly transitive arc-colored tournaments*](https://www.sciencedirect.com/science/article/pii/S0012365X10001184), Discrete Mathematics 310(20) (28 October 2010), 2697–2704, DOI 10.1016/j.disc.2010.04.003. Publisher abstract/search rendering only; direct page retrieval returned 403. It establishes subclasses involving upset tournaments and tournaments that become transitive after deleting one vertex. These extra orientation restrictions are not supplied by the target. Aikin–Bland explicitly credits their general hereditary-property Hamiltonian dominating-cycle lemma to this work, with implicit antecedent in Shen.

Laura Pastrana-Ramírez and María del Rocío Sánchez-López, [*Kernels by Monochromatic Directed Paths in 3-Colored Tournaments and Quasi-Tournaments*](https://m-hikari.com/ijcms-2010/33-36-2010/sanchezIJCMS33-36-2010.pdf), Int. J. Contemp. Math. Sciences 5(34) (2010), 1689–1704. Actual 16-page PDF obtained; introduction and Theorem 2.1 statement inspected, not its entire proof. The tournament theorem imposes at most two incoming colors at every vertex and requires all outgoing arcs to use the remaining color whenever two incoming colors occur. Its quasi-tournament results and counterexamples are not results about the unrestricted target.

## Aikin–Bland 2019

Jeremy Aikin and Adam Bland, [*Monochromatic sinks in 3-switched tournaments*](https://ajc.maths.uq.edu.au/pdf/73/ajc_v73_p071.pdf), Australasian Journal of Combinatorics 73(1) (2019), 71–83. Received 4 December 2017; revised 21 August and 24 October 2018. Actual 13-page PDF obtained. Definitions, Questions 1.1–1.2, Theorem 1.3, Lemma 2.2 and selected auxiliary arguments inspected; printed page 72 visually checked. Full proof not independently audited.

A switch on a directed cycle is a vertex where consecutive cycle arcs have different colors. The theorem requires every cycle to have at most three switches, together with no cyclic rainbow triangle. Equivalently, its abstract gives at most two switches on triangles and at most three on longer cycles. Restricting longer cycles is an additional assumption. Three available colors do not limit a long cycle to three switches. The theorem therefore does not prove the target. Question 1.2 explicitly remains open in the paper and includes the three-color case.

## Color-class restriction, 2016

Hortensia Galeana-Sánchez and Rocío Sánchez-López, [*Kernels by monochromatic paths and color-perfect digraphs*](https://doi.org/10.7151/dmgt.1860), Discussiones Mathematicae Graph Theory 36(2) (2016), 309–321; [actual repository PDF](https://bibliotekanauki.pl/articles/31340961.pdf). Received 18 August 2014; revised and accepted 23 June 2015. All 13 pages read as extracted text; statements and definitions checked. This is not a full-proof certification.

The color-class digraph has colors as vertices; a color i points to j when some directed two-arc walk uses i then j. Corollary 19 states an mp-kernel exists for a three-colored digraph if that color-class digraph is not strong. Corollary 20 states the tournament conclusion when the color-class digraph has no directed triangle. This is a global transition restriction, not merely an exclusion of actual rainbow triangles in the tournament. Do not promote the latter statement to an independently verified theorem from this review; proof-text scope and cross-reference issues were noted. Corollary 19 and Theorem 10 were read separately from the later chain of corollaries.

## Later searches and false-positive resolutions

- Nicolas Bousquet, William Lochet and Stéphan Thomassé, [*A proof of the Erdős–Sands–Sauer–Woodrow conjecture*](https://arxiv.org/abs/1703.08123), arXiv v1 23 March 2017; [published](https://www.sciencedirect.com/science/article/pii/S0095895618301175) J. Combin. Theory Ser. B 137 (July 2019), 316–319, DOI 10.1016/j.jctb.2018.11.005. Actual four-page arXiv PDF obtained; definitions and theorem scope inspected, not full proof audited. This solves the existence of a bounded-size monochromatic dominating set depending only on the number of colors. It does not assert a single vertex under the target's forbidden-triangle assumption.
- Raphael Yuster, [*Path-monochromatic bounded depth rooted trees in (random) tournaments*](https://arxiv.org/abs/2404.03752), arXiv v1 4 April 2024; related publication DOI 10.1016/j.disc.2024.114022. Actual 13-page preprint PDF obtained; introduction, main theorem statements and relevant construction inspected, not full proof audited. It treats extremal and random-tournament reachability and depth, not the unrestricted no-rainbow-triangle target.
- Wei Li, Shenggui Zhang, Yandong Bai and Ruonan Li, [*Rainbow Triangles in Arc-Colored Tournaments*](https://link.springer.com/article/10.1007/s00373-021-02313-w), Graphs and Combinatorics 37 (2021), 1271–1290, published 14 May 2021. Publisher abstract inspected only. Additional degree/irregularity conditions force rainbow triangles; this is not a monochromatic-universal-source resolution.
- [*On kernels by rainbow paths in arc-coloured digraphs*](https://www.degruyterbrill.com/document/doi/10.1515/math-2021-0019/html), Open Mathematics 19 (2021), 268–283. Primary indexed introduction inspected; direct HTML retrieval failed and the PDF request yielded an empty HTTP202 response. No actual PDF inspection is claimed. Rainbow-path kernels are distinct from monochromatic-path kernels.
- Ilan Goldfeder and Miguel Tecpa-Galván, [*The theorem of Richardson and its generalizations: a survey*](https://link.springer.com/article/10.1007/s40590-025-00711-1), Boletín de la Sociedad Matemática Mexicana 31, article 32 (27 January 2025). Publisher abstract and references inspected; subscription-only full text was not obtained. This does not provide a verified target-status certificate.

Searches included exact source titles; three-color/three-colour tournament, monochromatic sink/source/reachability, rainbow directed triangle, kernel-by-monochromatic-path, and Sands–Sauer–Woodrow variants; date-focused searches through 2026; and primary citation chains. Search-result crawl timestamps were not used as publication dates. No applicable later full proof or counterexample was found. Inaccessible sources remain inaccessible rather than silently treated as negative evidence.

## Verification artifacts

SOURCE_PDF_METADATA.md contains public titles, URLs, submission/publication dates, page counts, exact PDF byte counts, SHA-256 values, inspection levels and prior-capture matches. the scholarly retrieval history and supplement and SOURCE_REPOSITORY_RETRIEVAL.md contain retrieval outcomes only. Copied papers and derived source text are excluded from this public artifact set.
