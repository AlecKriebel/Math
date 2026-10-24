# Scope and attribution review — 24 October 2026

Reviewed independently from the full published manuscript and its README, dependencies, priority note and metadata. Earlier inventory reviews were not read. This is an AI-assisted adversarial scope review, not independent human refereeing or exhaustive novelty certification.

## Verdict

**PASS for the narrowly stated expected-degree result and a faithful explanatory webpage**, subject to the separate proof and certificate audits passing. The manuscript's historical qualifications are substantively appropriate. No authenticated contrary publication or source-scope contradiction was found in this bounded review.

**HOLD for any stronger public claims** of historical firstness, a new general electrical/forest method, a negative result for Cayley or unimodular graphs, an exact computed expectation for the square, journal acceptance, formal verification, or human peer review. Such claims are not established by this release or this review.

## Exact permitted public wording

Headline:

> Free spanning-forest degree can decrease under squaring

Short explanation:

> Adding all distance-two shortcuts to an infinite symmetric graph can reduce the average number of edges selected at a vertex by its free uniform spanning forest. For the binary grandparent graph, the paper proves an expected degree above 3.22; for its simple square, it certifies an expected degree below 3.21.

Technical statement:

> For the binary grandparent graph G, E[deg FUSF(G)(o)] = (24 − √2)/7. For its simple square G², E[deg FUSF(G²)(o)] ≤ 3208526010913748780/10¹⁸ < 3.21. The graph G has degree 8 and nonunimodular full automorphism group; G² has degree 40. Both are infinite, connected, locally finite, simple and vertex-transitive.

Historical positioning, immediately accompanied by the convention and scope:

> Under the explicitly stated convention b_F(X) = E[deg FUSF(X)(o)]/2 − 1, this is a counterexample to the unrestricted vertex-transitive square-invariance assertion in Abért's Question 24 (2010). The example is nonunimodular; the paper makes no counterexample claim for the unimodular subclass or the known Cayley case.

Status:

> Alec Kriebel · Preprint v1.0.0 · 22 October 2026 · DOI 10.5281/zenodo.23575190. The preprint has not undergone formal independent human peer review. AI tools were extensively involved in the research, proof development, verification, writing and internal review.

For a compact card, prefer the headline and “A nonunimodular vertex-transitive counterexample, with an exact calculation and a finite rational certificate.” Put the Abért claim on the detailed page where its convention and limitations fit naturally.

## Primary-source checks

All links below were checked on **24 October 2026**. Downloaded body hashes are recorded in `primary-sources/download-manifest.json`; the five previously cited bodies match the release's recorded SHA256 hashes exactly.

1. **Abért, Some questions, 2 November 2010, printed p.4, Question 24.** The actual seven-page source was read in full. It expressly uses arbitrary vertex-transitive graphs, then states square equality for Cayley graphs because the quantity is group-dependent. It supplies no normalization formula. The introduction and preceding sections contain no global unimodularity restriction; the neighboring questions explicitly distinguish unimodular cases. Therefore the manuscript's scope reading is supported. Its title “Some questions” does not establish the problem remained open in October 2026. The present question is answered through the stated forest-degree interpretation; a webpage should not silently substitute a different nonunimodular invariant. [Author-hosted original](https://www.renyi.hu/~abert/questions.pdf)

2. **BLPS, Uniform spanning forests (2001), corrected author body dated 27 January 2009.** Read finite electrical minimization and Theorem 4.1, the opening of §5, and Propositions 7.1–7.2/Theorems 7.3 and 7.8. Free and wired are distinct limiting constructions. The manuscript's fixed finite-support flows give valid bounds in every sufficiently large finite free network, and the free marginal identity then gives the claimed infinite upper bound. No wired minimizer is used by that argument. This is an established electrical/exhaustion mechanism, not a new one. [Corrected author body](https://rdlyons.pages.iu.edu/pdf/usf.pdf), [published DOI](https://doi.org/10.1214/aop/1008956321)

3. **Tang, Weights of uniform spanning forests on nonunimodular transitive graphs.** Read arXiv v2 §2.3 and all §5.2 (printed pp.40–49), including its proofs and remarks. It defines the same grandparent family, establishes FUSF connectivity and branching, and uses finite local resistance estimates. The specific complete expected-degree comparison with the simple square does not occur in that subsection. The cited v2 carries an arXiv stamp of 3 December 2020 and an internal title date of 4 December 2020; the release's arXiv version date is identifiable. The final journal PDF endpoint returned HTML again, so no claim about uninspected final-body additions is warranted. [Inspected v2](https://arxiv.org/pdf/1908.09889v2), [journal DOI](https://doi.org/10.1214/21-EJP709)

4. **Pete–Timár, The free uniform spanning forest is disconnected in some virtually free groups, depending on the generator set.** Read the v2 introduction and Theorems 1.1–1.3. It gives the formula Edeg = 2 + 2β₁⁽²⁾ on Cayley graphs and explicitly contrasts expected-degree invariance with component-count dependence. Its component/lightness results do not state the target square comparison. The release credits this distinction correctly. Final journal-body coverage has not been established here. [Inspected v2, 24 January 2021](https://arxiv.org/pdf/2006.06387v2), [journal DOI](https://doi.org/10.1214/22-AOP1581)

5. **Gaboriau, Invariant percolation and harmonic Dirichlet functions (2005).** The actual arXiv v3 §2.4 begins with a transitive unimodular action; Proposition 2.9 and Definition 2.10 retain that setting. The release appropriately refrains from identifying an unspecified nonunimodular tracial invariant with its b_F. This source cannot be used to erase the unimodularity hypothesis when claiming invariance. [Inspected v3, 25 May 2005](https://arxiv.org/pdf/math/0405458v3), [journal DOI](https://doi.org/10.1007/s00039-005-0539-2)

6. **Additional check: Lyons–Peres, Probability on Trees and Networks, corrected body dated 8 November 2020.** Read Example 7.1, related §7.9 notes, §8.2/Exercise 8.1, pp.346–348, the closing invariance discussion in §10.8, and grandparent-related Exercise 10.51. The book already describes the graph, its non-Cayley nature, and the identification of its full automorphism group with the end stabilizer. It attributes the examples to Trofimov (1985). The manuscript's direct verification is useful but cannot be advertised as a new structural discovery. The inspected passages do not give the target square comparison. This narrows one prior coverage gap; it is not a full-book audit. [Author-hosted corrected book](https://rdlyons.pages.iu.edu/prbtree/book_corr.pdf)

7. **Additional check: Pete, Probability and Geometry on Groups, 3 April 2024.** Read the relevant portions of §11 on harmonic Dirichlet functions, free/wired forests, and Theorem 11.8. They reinforce the free/wired and Cayley-degree distinction; no target square comparison was found there. [Author-hosted lecture notes](https://math.bme.hu/~gabor/PGG.pdf)

## Adversarial interpretation checks

- **Does degree 8 to degree 40 make the result tautological?** No. Those are degrees of the underlying graphs. The result concerns expected degrees in different random forest laws; the site must keep these quantities distinct.
- **Does adding edges imply forest expected degree must increase?** The individual probabilities of old edges can fall, while new edges become available. Summing both contributions is essential. The certificate sums flows to all 40 square-neighbors, rather than just the old eight.
- **Is the square expectation known exactly?** No. The displayed rational number is an upper bound from feasible currents; the currents are not asserted optimal. Use “at most” or “below,” never equality, a bare numerical estimate, or a chart implying an exact point value.
- **Is this a result about a finite graph?** No. The finite graph is a witness for an infinite statement. An illustrative finite ball should be labeled a truncation; its forest law or average degree is not the target infinite law.
- **Does “uniform spanning tree” describe the infinite construction without qualification?** No. Explain it through limits of finite uniform spanning trees with free boundary. Avoid suggesting a uniform distribution over all infinite spanning trees.
- **Does a nonunimodular transitive subgroup suffice to establish the graph's scope?** No. The paper explicitly recovers the parent map from the graph and thus identifies the full group; its argument is also consistent with the known book description.
- **Does the forest-derived name resolve all possible meanings of L²-Betti number?** No. Retain b_F and the displayed convention when making the historical connection. The directly proved mathematical content is unequal expected degrees.
- **Can the new website say the general unimodular problem is open?** This review does not establish its present status. Say only that the preprint does not provide a negative result for that subclass.

## Priority and publication limits

The bounded searches used grandparent/grandmother, expected FUSF degree, resistance, square/graph power, Betti, Abért/Abert Question 24, and exact candidate value/title terms. They produced established sources and many irrelevant hits, but no authenticated earlier publication of this complete comparison. This is not evidence sufficient for “first,” “previously unsolved until 2026,” “16-year-old problem solved,” or “new method.” Tang and Pete–Timár final journal bodies, unindexed literature, talks, theses and all alternatives in terminology remain coverage limits. Outside expert input could improve historical priority assessment; no outreach was prepared or initiated.

The public Zenodo API independently returned record 23575190, DOI `10.5281/zenodo.23575190`, version `1.0.0`, publication date `2026-10-22`, author Alec Kriebel with the stated ORCID, and resource subtype `preprint`. It lists the PDF and source/verification ZIP. The API capture is `zenodo-public-metadata.json`. This authenticates the public record's metadata, not mathematical correctness or peer review. [Public record](https://zenodo.org/records/23575190), [public API](https://zenodo.org/api/records/23575190)

The frozen description still uses “proposed deposit”; the website can accurately call it a published preprint/deposit, while preserving unrefereed status. No amendment to the immutable source package is necessary for the webpage.

## Release boundary

This review did not execute the current verifier or independently rederive every recurrence; those are separate requested audits. It did read the complete manuscript and test the free-exhaustion transfer, graph-scope interpretation, and source claims. The headline is permitted only if those other audits agree. Locally downloaded scholarly PDFs/text are reference-only and excluded from Git by this folder's `.gitignore`; do not bundle them in the website. The report, log and link/hash manifest are sufficient review artifacts.
