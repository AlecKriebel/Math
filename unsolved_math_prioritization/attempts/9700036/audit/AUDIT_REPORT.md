# Independent audit: SIRSN subnetworks cannot be trees

Target: queue rank 936, problem 9700036, AMR-096-0036.

## Verdict and exact scope

The full target conclusion is supported by prior literature, with the application made explicit in the clarified derivative and the separate source-proof repair note. The recommended disposition is RESOLVED_BY_PRIOR_LITERATURE / already_solved, with 0/5 original search approaches used. Credit for the obstruction theorem belongs to David Aldous (2021). Connecting it to this numbered SIRSN problem is the application made here; neither the source article nor the maintained problem page was found explicitly declaring this numbered item solved.

This is an independent AI mathematical audit, not human peer review or formal proof verification. Its first-review acceptance is limited to the exact clarified application plus the pinned source-proof repair, rather than a claim that every printed detail of the source proof can be used literally. A separate focused review is being requested for these repairs; its outcome is not asserted by this report.

The accepted claim is: under the SIRSN axioms in Aldous's published 2014 definition, almost surely S(1) contains a finite route circuit and in particular cannot be a tree, even with Steiner junctions. The argument also applies to a weak SIRSN with the same finite expected route stretch. It does not settle distinct IDs 9700033 or 9700034, count cycles, or describe their geometry.

The original frozen author files are preserved byte-for-byte. CLARIFICATION.patch changes the application explanation, measurability formulation, source-proof caveat, and audit metadata. It does not alter the corpus identity or attribution. SOURCE_PROOF_REPAIR.md is the complete authored sufficient corollary, including exact constants for the source-proof details discussed below. ACCEPTANCE.json identifies the exact accepted combination and its byte pins.

## Corpus and provenance gate

All three complete corpora were independently hashed and parsed. Exactly one problem record and one catalog record match ID 9700036. The canonical array consists of the complete problem record and the complete report obtained from the problem-number key, serialized with json.dumps(..., sort_keys=True), default separators, and default ASCII escaping. Its 4,328 bytes hash to:

f8fea69167f1dc867d824004c05ab51e0f4bb2bdfa53f35308e52c3f747bae93

That equals the catalog's review hash. Wrapper, projected-record, missing-report, and reversed-array controls all produce a different hash. The old report is literature review only, with no original proof, substantive reduction, or computation to continue. Its unit-speed interpretation and 2011 bibliography are incorrect. No dataset content or complete record is included in this audit package.

The frozen author ZIP is 10,688 bytes, SHA-256 3008e91a1b89b12efe3b3e300e9957585b84d81db715cad3ba340cf38db6be4e. Its external manifest is 1,124 bytes, SHA-256 8d3de572463b79fb308117515b3710fca0fb1075fdcda4f30ebb57666f066a7a. Every archived author member was checked against that manifest and the extracted copy.

## Correct problem and source definitions

The long manuscript is arXiv:1204.0817v1, April 2012, with the target numbered Open Problem 36. The published source is *Scale-invariant random spatial networks*, EJP 19 (2014), article 15, with the target numbered Open Problem 10, Section 8.7.2, printed p.39. The relevant pages and definitions were inspected directly. Sources:

- https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf
- https://emis.de/ft/43138
- https://doi.org/10.1214/EJP.v19-2920

S(lambda) is the network spanned by an independent Poisson sample of intensity lambda. It is not a speed threshold. Every pair of sampled terminals has its designated route, so the sampled network is connected. The permitted routes are simple rectifiable polygonal arcs; infinitely many successive segments may accumulate at their endpoints. Compatibility means that two routes meeting twice agree between the meeting points. The definition requires consistent measurable finite-route laws, Euclidean translation/rotation/scaling covariance, finite mean unit-distance route length Delta, and finite sampled length intensity. The full SIRSN definition adds the remote-route intensity condition; that last condition is not needed for the contradiction.

Finite length intensity is not finite vertex count. A countable polygonal subdivision can have endpoint accumulation, and no artificial local finiteness of Steiner vertices is assumed in the accepted argument. Geometric crossings are junctions of the embedded route union; the 2021 article's Section 3.2 explicitly treats crossing straight segments as potentially destroying an abstract genealogical tree. No overpass convention is silently introduced.

The long manuscript's Appendix A describes a route topology using finite interior turning points and vanishing endpoint-subroute lengths. This topology implies convergence of compact route images in Hausdorff distance. Together with the measurable sampled-route setup in the published definition, it supports the compact-set predicates used in the clarified application.

## Imported theorem and proof audit

The controlling prior theorem is Aldous, *Route lengths in invariant spatial tree networks*, ECP 26 (2021), article 31, Theorem 1.2. The preprint arXiv:2103.00669v1 labels it Theorem 2. Sources:

- https://doi.org/10.1214/21-ECP401
- https://escholarship.org/content/qt25v3q7sd/qt25v3q7sd.pdf
- https://arxiv.org/abs/2103.00669

The result covers invariant planar Poisson tree networks with Steiner junctions. It forces an infinite mean for the typical-pair route length averaged over separations at most r for large r. Its footnote 2 explicitly reduces the symmetry requirement to translation invariance. It neither assumes independent network construction from the Poisson sample nor joint ergodicity. The stronger exact-radius assertion discussed in the paper is not imported.

The main proof in Section 2 was inspected end to end: local balanced-square pairs, the uniform contour lemma, exclusion of a small square, terminal-weighted centroid coloring, and the stationary pair-intensity tail conversion. The theorem page, centroid page, and the balanced-strip definition were also visually inspected. Section 3.1 equation (3.2) was used to verify normalization; Sections 3.2-3.3 were checked for crossing and scope conventions. This does not claim an independent audit of all unrelated examples or every cited book.

The following details require an explicit interpretation or adjustment; they are addressed with exact inequalities in SOURCE_PROOF_REPAIR.md:

1. On printed p.3, balanced strips are written with full coordinate interval [0,1] rather than [0,m]. The intended full-width/full-height strips are necessary for both their stated expected counts and the square-sliding proof. This is a directly observed source typo.
2. The red-count calculation accompanying (2.16) cannot simply repeat the blue calculation with the same constants: blue thresholds 0.09 and 0.89, together with total count up to 1.02, give red upper bounds 1.02, 0.93, and 0.13. The repaired calculation yields common color fractions above 0.21; it does not assume the printed 1/4 conclusion from insufficient displayed arithmetic.
3. The source only sketches Corollary 2.3. The repair retains k/200 distinct good edges from the long-contour argument, extends the contour estimate to color fractions at least 0.20, and subtracts the excluded square's perimeter after recoloring. This gives at least k/2000 good edges outside any square of side ceil(k/1000).
4. The dependence range for short zero-cost circuit events is written explicitly as 2 log k+2. The variance estimate still tends to zero after division by k^4.
5. A centroid that is a terminal is included as a singleton color group. A centroid outside the large square is handled by a clamped grid square. The resulting explicit route threshold is mk/5000, instead of relying on exact alignment in the source's informal centering sentence.

These adjustments establish precisely the sufficient finite-hull corollary. They do not change the established theorem's attribution, assert a newly discovered theorem, or claim that the published paper has been formally corrected by its author or journal.

## Finite-hull and measurability bridge

Straightening a curved tree edge can create crossings. It is therefore not a valid shortcut here and is not used. Retain the original rectifiable arcs and suppress only unmarked degree-two subdivisions when describing a finite combinatorial tree.

For the precise conditioning event, require that every sampled terminal triple x,y,z satisfy R(x,y) subset R(x,z) union R(z,y). This is a countable intersection after a measurable enumeration of the locally finite Poisson sample. Compact-set inclusion is Borel, so the event is measurable; quantification over all triples makes it translation invariant. Every globally tree-valued configuration satisfies it.

To check all larger finite terminal sets, choose a root o within such a set. Any two root routes have a connected initial intersection, by route compatibility. Adjoining a root route to the finite union of earlier root routes attaches one remaining arc along a connected initial subarc. Induction gives a finite rectifiable tree with finitely many essential vertices. Triple inclusion places every other terminal-to-terminal route in that tree, where simplicity makes it the unique connecting arc. Thus cycles involving four or more terminals are not overlooked.

No equivalence between this event and a global infinite-union topological-tree property is asserted. The source proof is applied directly to every finite terminal hull, which is all it uses. A failure of triple inclusion produces a circuit in a finite union of three compatible arcs. Consequently the nullity of the measurable event gives the stated finite-circuit conclusion, as well as excluding all tree configurations.

## Conditioning and Palm normalization

Let A be the measurable invariant event above, with probability p>0. For every bounded local function f of the Poisson process, average translated copies over large squares. Poisson marginal ergodicity makes these averages converge in L1 to E f. Joint translation invariance and invariance of A keep the conditional expectation of every average equal to E[f|A]. Conditional L1 error is at most unconditional error divided by p. Therefore E[f|A]=E f. Bounded local functions determine the point-process law, so the conditional Poisson marginal is unchanged. Joint translation invariance also survives conditioning.

This argument is valid. Merely conditioning on an arbitrary network event would not have been enough; its invariance and the ergodicity of the Poisson marginal are essential. Nothing requires the full random network to be ergodic. One can also avoid invoking a general ergodic theorem: if f depends only on Poisson points in a fixed radius-R window, two translates have zero covariance at separation greater than 2R. The variance of its square average is at most 4||f||_infinity^2 times the area of the radius-2R disk divided by the averaging-square area, and therefore tends to zero. This gives the required L1 convergence directly.

For a finite-area anchor set B, let Z_r(B) sum route lengths over ordered pairs with first terminal in B and displacement of norm at most r. The independent sampling construction, its measurable finite-route kernels, Poisson two-point formula, scaling, and Tonelli give

E Z_r(B) = |B| 2 pi Delta r^3/3.

The expected ordered pair count is |B| pi r^2. The normalized mean is therefore 2 Delta r/3, with separation density 2s/r^2. It is neither nearest-neighbor sampling nor uniform-radius sampling. Unordered counts divide numerator and denominator by two. This agrees with the published normalization (3.2).

After conditioning, independence of routes and Pi and scale invariance may be lost. They are not used again. Nonnegativity gives E[Z_r(B)|A]<=E Z_r(B)/p. The conditional Poisson marginal keeps the same denominator, so the conditional mean is bounded by 2 Delta r/(3p). The finite-hull corollary gives infinite mean under this same conditional stationary law, a contradiction. Thus p=0.

## Independent executable checks and limits

The full external corpora and all four source PDFs were rebound by bytes and SHA-256. Normal and optimized Python executions were run in an isolated relocated directory with copied inputs for both author and clarified packages. Each also passed after controls were restored. Thirty-two tamper controls rejected, including a valid-Python verifier mutation, bound report and metadata changes, source-PDF and whole-corpus mutations, extra files, extra directories, and symlinks. Four canonical-shape controls rejected.

A separately implemented finite checker enumerates 1,441 labeled trees via connected edge subsets rather than the author's Pruefer generator, checking 85,787 binary terminal weightings for centroids. It also examines 771 connected graphs with deterministic unique compatible shortest routes: 145 tree cases satisfy the triple condition and 626 cyclic cases reject it. Fifty-two rational radial-moment identities and five source-constant inequalities pass in normal and optimized modes. These are independent diagnostics and negative controls, not a numerical proof of the infinite-network argument.

The archive and external manifest provide integrity evidence, not an authenticated scholarly endorsement. A self-consistent changed archive cannot establish original provenance; use the external SHA-256 pins in the receipt and supply the manifest pin when replaying the audit verifier. No raw source PDFs, extracted source text, corpus content, or private coordination files are included. No GitHub or queue mutations were performed in this audit.
