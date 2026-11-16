# Source-first editorial INITIAL: 23573603

Frozen source pass at 16 November 2026, 14:06:09 UTC. Completion: 100% of this source-first editorial checkpoint; article drafting has not started. No public-copy, W, Sheet, Git, canonical or publication authority is inferred. Wait for root’s concrete authority after this INITIAL is reviewed.

## Reading and informed-role disclosure

I reread all 323 actual controlling TeX lines and all five actual native manuscript pages, visually using the authorized existing original root rasters. The five page images were readable and show the unchanged manuscript, including its title/version, complete abstract, theorem, construction, proof, limitations, authorship disclosure and references. Source/asset/raster hashes and targeted rights reads are in SOURCE_PINS.json. The manuscript necessarily supplies its own proof; this is editorial comprehension, not another proof review.

This is an informed role. Earlier in this session I authored the separate scientific scope review of this same edition, statically read the supplied verifier after that earlier freeze, and read the critical Benjamini and stretched-lattice primary interfaces after the earlier gate. Those exposures cannot be reset and are disclosed. During this new editorial pass I opened no root/peer scientific review findings, archived acceptance, support README, relation-to-prior-work opinion body, checker source/output or native/project program. A source-file inventory exposed names only. Native ACQUIRED metadata exposed the public Zenodo Description, including scientific summary and finite-check counts, after the whole TeX/PDF reading and before this freeze. That permitted metadata exposure is recorded; its counts are not new proof evidence and should not be repeated as public review narrative. No restart or claim of fresh blind independence is made.

## Exact title, edition and complete printed abstract

**A supercritical nonuniqueness example on a graph roughly isometric to the square lattice** — Alec Kriebel, Independent researcher, ORCID 0009-0001-9320-500X. The printed date/version and native version agree: **22 October 2026, version 1.0.0**. Record DOI: **10.5281/zenodo.23573603**. Native creation is 22 October 2026 at 17:57:59.433479 UTC; update 17:57:59.799057 UTC. These do not create a first-priority claim. The native is_published field is absent, not a boolean to invent.

The complete printed abstract, with only line wrapping and TeX math typography normalized, is:

> We give an explicit deterministic graph of maximum degree four, roughly isometric to the square lattice, on which iid bond percolation has at least two infinite clusters with probability greater than one third at parameter 19/20, while its critical probability is at most 9/10. Edges internal to two opposite quadrants are retained; every other lattice edge is replaced by a path of length 100. Elementary dual parity and all-distance path bounds prove the assertions without a lattice threshold formula or a transitivity assumption. The example refutes the explicitly declared all-supercritical interpretation of Benjamini's 2013 Problem 9.6. The original question omits its probability quantifier; no unique author intent, exclusive priority, or current open status is asserted.

The separate native Description is longer, includes archive-workflow/count information and is not another abstract to reproduce wholesale on an article page.

## Precise result and probability quantifiers

The objects are countable, simple, undirected, connected graphs with graph distance. Actual percolation is ordinary Bernoulli **bond** percolation: each actual edge is retained independently with one common parameter p. N∞ is the number of infinite open components. The threshold is p_c(G,o)=inf{p:P_p(o connects to infinity)>0}; connectedness and finite-path forcing make the positive-survival threshold independent of the chosen root.

The theorem constructs **one explicit deterministic graph G** of maximum degree four, roughly isometric to Z² with the stated multiplicative-plus-additive constant **C=100**, such that

- p_c(G) ≤ 9/10 < 19/20;
- P_(19/20)(N∞ ≥ 2) > 2200741829/6461571200 > 1/3;
- at p=9/10 **every vertex** has positive probability of an infinite open cluster.

The threshold upper bound is sufficient; neither the exact threshold nor the exact nonuniqueness probability is computed. The latter is an event of positive probability, not almost-sure multiplicity, exactly two clusters or infinitely many clusters.

The declared interpretation of the source question is: for every admissible bounded-degree graph roughly isometric to Z^d, and for **each fixed** p with p_c(G)<p≤1, almost-sure uniqueness holds. The constructed d=2 graph and p=19/20 contradict this universal interpretation. The source question’s sentence does not state its p-quantifier. No unique missing author intention is claimed; a weaker assertion of uniqueness sufficiently near one is not refuted. Nor is a simultaneous-in-p statement in one coupling required. This qualification belongs beside the main public claim, not hidden in a footnote.

The own editorial logical check is short: 9/10<19/20 and p_c(G)≤9/10 make the displayed parameter strictly supercritical. A positive-probability event with at least two infinite components contradicts the asserted probability-one event of a unique infinite component. No transitive-graph zero–one–infinity law or monotonicity of uniqueness is needed to make that deduction.

## Construction, mechanism and assumptions to preserve

In the nearest-neighbor square lattice, A={(x,y):x≥1,y≥1} and B={(x,y):x≤−1,y≤−1}. Edges with both endpoints in A or both in B stay single edges. Every other edge is replaced by a private path of exactly 100 edges, introducing 99 degree-two vertices. Original vertices retain degree four. The bound is uniform everywhere, not a stretch length increasing with position; no edges are randomly selected while defining G.

A map fixes the original lattice vertices and sends every new chain vertex to a nearer endpoint, with ties chosen consistently. For all vertices x,y,

d_Z²(f(x),f(y)) ≤ d_G(x,y) ≤ 100 d_Z²(f(x),f(y))+100.

The map is onto. These imply the source’s explicit convention C⁻¹d_Z²−C≤d_G≤C d_Z²+C and strict C-net condition with C=100, including chain midpoints. “Roughly isometric” must not silently be replaced by exact isometry or a stronger convention.

The coarse representation has independent probabilities p on retained strong edges and p^100 on weak coarse edges, because the underlying bond sets are disjoint. It is exactly the homogeneous iid model on the subdivided physical graph, not a different inhomogeneous model being substituted for the theorem. Infinite actual/coarse components correspond bijectively, with finite partial-chain branches harmless.

The written argument gives quadrant-corner survival at least 143/245 at p=9/10, then uses survival monotonicity at 19/20. An all-boundary-start/all-length weak-path sum is strictly below 27/107648 at 19/20. Independence of the two strong-quadrant families and the weak-chain family gives the stated positive lower bound. This is not a finite-window barrier or an extrapolation of checker samples. No lattice threshold formula, transitivity, deterministic cluster count or uniqueness-monotonicity theorem is assumed.

## Prior credit and limits

The following are the manuscript’s attributions, not fresh primary-source revalidation in this phase:

- Benjamini’s 30 October 2013 author manuscript supplies Definition 1.25 and Problem 9.6. The published chapter has different pagination; exact publisher-body equivalence is not asserted. Its DOI is a source-question DOI, not this counterexample’s DOI.
- Bounded subdivision, series reduction, dual parity, path counting and independence are established tools. The contribution is the explicit deterministic lattice-rough-isometry example and quantitative proof in the declared model, not a new general probabilistic method.
- Benjamini–Schramm’s older nonuniqueness example has a hyperbolic-sector/enhanced-tree and site-percolation setting. Benjamini–Kozma’s result concerns critical nonuniqueness in a subexponential product setting without the required lattice rough-isometry assertion.
- Teixeira, Candellero–Teixeira and Hutchcroft–Tointon provide high-density uniqueness results with their own geometric, uniformity, decoupling and site/bond hypotheses. A threshold below one there is not automatically p_c. These results are compatible with the weaker near-one interpretation.
- Hilário–Sá–Sanchis–Teixeira use power-of-p coarse probabilities; their cited full-supercritical uniqueness result concerns an annealed stretched-lattice law with averaged translation invariance, ergodicity and finite energy. It is not a theorem for every deterministic angular stretching pattern. No comparison theorem is imported into the present proof.

The paper discloses bounded literature/source coverage and access/version limits rather than exclusive novelty or current worldwide openness. Its earlier PR1348 is described as an unpublished proof source, not an earlier published counterexample. Finite diagnostic controls supplement the unbounded-path/infinite-event/metric proofs. No exact cluster count, almost-sure multiplicity, critical nonuniqueness or simultaneous-in-p law is asserted. The source archive’s detailed check counts and dated internal workflow are not article copy.

## Native files, rights and status

There are exactly two native assets, in the literal API entries order (the separate custom order array is empty):

1. supercritical-nonuniqueness.pdf — 67,272 bytes, five pages; SHA256 4a83d0519b0d3987f8f79daed7d030793bfaeb94c88c0bcfa339c936d81ebcde.
2. supercritical-nonuniqueness-source-and-verification.zip — 103,935 bytes; SHA256 6f89ba6fda4727ae73ae768fa38accc0dbf97bd5ada70fdc34be996de76b9b45.

The ZIP contains 18 inventoried member occurrences, including the sole main.tex and an embedded PDF with the same native PDF hash. Member names/hash metadata were read; the support summaries and programs were not opened in this phase. Any later local reader and download must use unchanged native bytes and preserve PDF-then-ZIP order.

The record-level license is CC BY 4.0. The targeted prose license explicitly covers authored paper, mathematical supporting prose, metadata and source text under CC BY 4.0; authored code is separately MIT-licensed. Third-party bodies are only cited and retain their rights. Do not apply one blanket license to every mixed archive component. Both license notices were read.

AI tools were used extensively across planning, mathematical exploration, proof development/reconstruction, computation, literature work, writing, editing and adversarial checking. Alec Kriebel is the named human author. This is an unrefereed preprint, without conventional independent human or journal peer review, journal acceptance or formal proof-assistant certification. Internal AI reviews do not supply those certifications.

## Editorial boundary after this freeze

If root provides concrete drafting authority, the intended article uses the standard light white/Arial template, complete original abstract, accessible explanation, exact quantitative result, clear p-interpretation and model limits, short prior credit, unchanged local PDF reader/native download order, accurate version/date/DOI/BibTeX/SEO, split rights, AI/unrefereed disclosure and professional substantive collaboration language. Default: no further-research question and follow-up null. No canonical slug/URL, final public copy, assets or deployment is authorized by this note. Stop here until root reviews the actual INITIAL and supplies authority.
