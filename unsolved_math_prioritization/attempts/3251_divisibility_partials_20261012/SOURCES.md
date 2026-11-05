# Source frontier audit: OPG-56230 / problem 3251 / ordered row 1753

Checked 12 October 2026. Read-only literature verification within the current work, not a new mathematical research round. No remote files, comments, branches, or publications were changed.

## Outcome and scope

No source located in this bounded search establishes the unrestricted odd-hole-free 2-divisibility conjecture. This is a report of what was found, not an exhaustive absence claim. The strongest safe formulation is: the general statement is explicitly conjectural in the inspected Hoàng arXiv v2, while subsequent located records prove restricted classes or different divisibility statements.

The exact target is a finite simple graph G with at least one edge and no induced odd cycle of length at least five. A 2-division is a partition V(G)=A disjoint-union B with both clique numbers smaller than omega(G). The hereditary definition of 2-divisibility requires this for every induced subgraph with an edge. Because odd-hole-freeness is hereditary, the conjecture for the whole class is equivalent to that hereditary formulation. Edgeless induced subgraphs are exempt, as in the original definition. A maximum clique means maximum cardinality, not an arbitrary inclusion-maximal clique.

## Source ledger

### 1. Original problem page
- URL: https://www.openproblemgarden.org/op/2_colouring_a_graph_without_a_monochromatic_maximum_clique
- Posted by Jon Noel, 25 August 2013; attributes conjecture to Hoàng and McDiarmid.
- Inspection: complete relevant problem statement, explanation, and bibliography, through the public HTML page.
- Scope: no monochromatic maximum clique in a two-colouring of an odd-hole-free graph. Mentions perfect graphs and the claw-free case. Treat its word “non-empty” consistently with the original at-least-one-edge definition; do not create a false isolated-vertex counterexample.
- Status evidence: the page labels the statement a conjecture. The page alone does not establish the latest research status.

### 2. Hoàng–McDiarmid, On the divisibility of graphs
- Discrete Mathematics 242 (2002), 145–156. DOI: https://doi.org/10.1016/S0012-365X(01)00054-1
- Publisher: https://www.sciencedirect.com/science/article/pii/S0012365X01000541
- Institutional record: https://ora.ox.ac.uk/objects/uuid%3Add3ea4e4-85ee-446e-8495-d93e7e152a4d
- Inspection: publisher-indexed abstract and institutional abstract/metadata; original full proof was NOT obtained. Direct publisher retrieval returned an unavailable-site HTML stub; ORA retrieval returned HTTP 403.
- Verified abstract: k-divisibility quantifies over induced subgraphs with at least one edge; claw-free graphs are 2-divisible exactly when odd-hole-free; general equivalence is conjectured.
- Later primary attribution: Hoàng arXiv:1510.02324v3 identifies the claw-free result as original Theorem 1 and substitution closure as original Lemma 3. Those theorem numbers are cross-attributed, not checked against original pages here.

### 3. Chudnovsky–Robertson–Seymour–Thomas, K4-free graphs with no odd holes
- Author PDF: https://thomas.math.gatech.edu/PAP/k4free.pdf
- Cover: 5 October 2001; revised 5 August 2009. Publication: Journal of Combinatorial Theory, Series B 100 (2010), 313–331.
- Inspection: Theorem 1.3, adjacent discussion of Conjecture 1.4, harmonious-cutset Lemma 2.2, decomposition Theorem 3.1, and proof of Theorem 3.2. NOT a re-audit of the full 24-page decomposition proof.
- Theorem 1.3 / 3.2: every K4-free odd-hole-free graph is four-colourable.
- Dependency path: 3.2 uses induction, 2.2 to glue across harmonious cutsets, SPGT 1.1 (or the cited earlier Tucker result) when no seven-antihole occurs, and 3.1 reducing the remaining case to heptagram and T11 types, whose four-colourability is checked there.
- This establishes the target when omega=3 by grouping proper colours {1,2} and {3,4}; each side has clique number at most two. When omega=2, use bipartiteness of triangle-free odd-hole-free graphs separately.

### 4. Chudnovsky–Sivaraman, Perfect divisibility and 2-divisibility
- Inspected author PDF, dated 20 April 2017: https://web.math.princeton.edu/~mchudnov/Perfect2div.pdf
- arXiv record: https://arxiv.org/abs/1704.06667v1 (submitted 21 April 2017).
- Published in Journal of Graph Theory 90 (2019), 54–60; DOI: https://doi.org/10.1002/jgt.22367
- Inspection: full Theorem 2.1 argument, its Lemma 2.1, and the statements/proof-dependency trail of Theorems 3.4–3.7. Printed p3 was visually checked. No byte-identity claim between author, arXiv, and journal versions.
- Theorem 2.1 proves (P5,C5)-free implies 2-divisible. Its proof is elementary, using the connected-set Lemma 2.1 and forbidden P5/C5 configurations; it does not use SPGT or the bull-free perfect-divisibility results.
- Theorem 3.7 concerns perfect weight divisibility for bull-free graphs that are odd-hole-free OR P5-free. It invokes 3.4–3.6; that branch uses SPGT, bull-free structural results, and perfect-graph substitution.
- Local proof typo: “n not in X” after K is chosen inside X2 should read “n not in K”: n is isolated in G[X2] and omega>=2. Definitions should retain the edge exception.

### 5. Hoàng, On the structure of perfectly divisible graphs
- Inspected version: https://arxiv.org/abs/2506.12660v2 and https://arxiv.org/pdf/2506.12660v2 ; v2 dated 17 June 2025.
- Published record: Discrete Mathematics 349 (2026), article 114809; https://doi.org/10.1016/j.disc.2025.114809 . Publication metadata does not certify identity of the version-of-record proof with v2.
- Inspection: relevant full text and PDF p6, visually checked.
- Conjecture 4.6 is the general odd-hole-free/2-divisible equivalence. Conjecture 4.7 says a minimally non-2-divisible graph has no clique cutset. Neither is proved there.
- The proved clique-cutset statements, Theorems 1.4 and 1.5, concern minimally non-PERFECTLY-divisible graphs under additional P5-free or independence-number-at-most-three hypotheses. They cannot be cited as general 2-divisibility gluing theorems.
- The paper flags a flawed older perfect-divisibility cutset argument, and supplies the restricted P5-free repair. These statements concern a different property from the exact target.

### 6. Deng–Wu, On the structure of some classes of hammer-free graphs
- Primary posted record: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6788821 ; https://doi.org/10.2139/ssrn.6788821
- Record says 15 pages, posted 18 May 2026.
- Inspection: indexed SSRN abstract/metadata only. Direct landing-page and delivery-PDF retrieval failed (HTTP 403 or tool fetch error). No theorem numbering, proof audit, PDF hash, or journal-acceptance claim is available here.
- Abstract announces every (hammer, odd-hole)-free graph is 2-divisible. A hammer is a triangle with a pendant two-edge path attached at one triangle vertex.
- The abstract also announces different results for even-hole-free graphs, including 3-divisibility, and a restricted perfect-division statement. None is a full proof of the unrestricted odd-hole-free target.
- Usable as a clearly labelled recent manuscript claim; do not silently promote it to proof-inspected or published-theorem status.

### 7. He–Shi–Wu–Yao, The perfect divisibility and chromatic number of some odd hole-free graphs
- Publication: Discrete Applied Mathematics 387 (15 July 2026), 124–128; https://doi.org/10.1016/j.dam.2026.03.008
- Inspected preprint: https://arxiv.org/abs/2603.09549v1 ; https://arxiv.org/html/2603.09549v1 ; https://arxiv.org/pdf/2603.09549v1 (10 March 2026).
- Inspection: publisher-indexed abstract and metadata; preprint Theorem 1 and its argument. This is not a version-of-record proof audit or complete re-audit of the preprint's other colouring results.
- Theorem 1 proves perfect divisibility for (odd hole, hammer, K2,3)-free graphs, not 2-divisibility of all odd-hole-free graphs.
- Its argument starts with a maximum-degree vertex, uses SPGT to obtain an odd antihole in its antineighbourhood, then forbidden-hammer/K2,3 adjacency analysis and a degree contradiction. Its proof does not invoke the general unproved 2-divisibility clique-cutset conjecture.
- Some introduction text discusses an older P5-free perfect-divisibility theorem and its restricted cutset dependency; do not transfer that discussion to Theorem 1 or the target conjecture.

### 8. Hoàng, On the structure of (banner, odd hole)-free graphs
- Inspected version: https://arxiv.org/abs/1510.02324v3 ; https://arxiv.org/pdf/1510.02324v3 (14 October 2017; first posted 8 October 2015).
- Published Journal of Graph Theory 89 (2018), 395–412.
- Inspection: Section 6, Theorem 6.3 and its dependency statement; not the full 25-page structural proof.
- Theorem 6.3 proves (banner, odd-hole)-free graphs 2-divisible. It uses induction, perfect graphs, the claw-free theorem, SPGT, structural Theorem 3.4 to obtain a homogeneous set, and substitution closure in Lemma 6.1 (attributed to HM2002 Lemma 3).
- The final proof cross-reference says Lemma 7.3 although the needed result is Lemma 6.1; distinguish this apparent numbering slip from the mathematical dependency. Section 7 separately proves perfect divisibility.

### 9. Dong–Song–Xu, 2-divisibility of Some Odd Hole Free Graphs
- Primary publisher: https://link.springer.com/article/10.1007/s10255-022-1110-8
- Acta Mathematicae Applicatae Sinica, English Series 38 (2022), 710–718; published/version of record 1 July 2022.
- Inspection: full publisher abstract and bibliographic metadata; subscription full proof NOT inspected.
- Abstract proves (odd hole,H)-free graphs 2-divisible for H in {dart,racket,bull}. Here dart is diamond plus a leaf at a degree-three vertex, racket is diamond plus a leaf at a degree-two vertex.
- This is a proper later source for the bull-free 2-divisibility subclass. The 2017/2019 Chudnovsky–Sivaraman perfect-divisibility theorem alone would not justify that claim.

### 10. Deng–Chang, On the structure of some classes of (P2 union P3)-free graphs
- Primary publisher: https://link.springer.com/article/10.1007/s00373-025-02926-5
- Graphs and Combinatorics 41, article 63 (2025); published 25 April 2025.
- Inspection: publisher abstract and metadata only; subscription full proof NOT inspected.
- Abstract (a) proves (C5,P2 union P3)-free graphs 2-divisible. This is an additional hereditary subclass. It is not an unrestricted resolution, and it should not be loosely called a superclass of the (P5,C5)-free result: the forbidden-subgraph classes are incomparable.
- Abstract (b) is a distinct perfect-division statement with bull-free, clique-number-at-least-three, and no-homogeneous-set hypotheses.

### 11. Chen–Lan–Zhong, On two conjectures of Hoàng
- Primary record: https://arxiv.org/abs/2605.09293v1 (10 May 2026).
- Inspection: abstract/metadata only.
- Search disambiguation: the two claims are a counterexample to perfect divisibility for all graphs with independence number at most three, and a proof of 3-divisibility for even-hole-free graphs. The abstract does not claim a resolution of odd-hole-free 2-divisibility.

## Exact usable mathematical consequences

1. The at-least-one-edge target and hereditary 2-divisibility of the odd-hole-free class are equivalent, because induced subgraphs preserve odd-hole-freeness.
2. The reverse implication, 2-divisible implies odd-hole-free, is elementary: an induced odd hole has clique number two, and a required division would be a proper two-colouring of an odd cycle.
3. For a graph with omega>=2, chi<=2(omega-1) suffices for a single 2-division by grouping proper colour classes into two groups of at most omega-1 colours each. To infer hereditary 2-divisibility, apply such an inequality to every induced subgraph separately. This derives the omega=3 case from CRST. The separate omega=2 argument is required.
4. Perfect divisibility has only one clique-lowering side; the perfect side need not have smaller clique number. It does not generally imply 2-divisibility: C5 has a perfect division (P4 plus one vertex), all its proper induced subgraphs are perfect, but its edges cannot be properly two-coloured. Thus the two notions must not be substituted in any dependency chain.
5. Theorem 2.1 of Chudnovsky–Sivaraman can be used directly for the (P5,C5)-free subclass. The general clique-cutset exclusion cannot be imported from Hoàng v2 as a theorem.

## Search and inspection limits

Searches included exact paper titles, DOIs, arXiv IDs, the Hoàng–McDiarmid conjecture, odd-hole-free 2-divisibility with 2025/2026 qualifiers, and the named subclasses. Primary landing pages, author PDFs and arXiv versions were preferred. UnsolvedMath search hits were not used as independent status evidence, avoiding circular reliance on a potentially user-edited problem page. No claim of exhaustive literature coverage is made. Subscription-only proofs, the SSRN delivery PDF, and the original HM2002 proof remain uninspected. PDF hashes identify retrieved byte streams, not mathematical correctness or peer-review status.


## Additional citations used in the preserved structural proof

- Song–Xu, *Divisibility and coloring of some P5-free graphs*, Discrete Applied Mathematics 348 (2024), 144–151. Public PDF: https://kam.mff.cuni.cz/~spring/media/papers/4/Divisibility_Coloring_P5_free_JS.pdf . Lemma 2.3 was inspected for prior credit for the homogeneous-set reduction. The edition supplies its own complete module proof, explicitly separating stable modules; the original source proof is not a hidden dependency.
- Chudnovsky–Robertson–Seymour–Thomas, *The strong perfect graph theorem*, Annals of Mathematics 164 (2006), 51–229. Public record: https://arxiv.org/abs/math/0212070 . The classical characterization is used only for the explicitly labelled optional odd-antihole consequence, and the full source proof was not independently audited here.

PUBLIC_SOURCE_METADATA.json records the verified public PDFs from the source-frontier pass and the later prior-credit supplement. A missing PDF hash means no verified PDF-byte claim is made here. These records do not establish byte identity across author, arXiv and journal versions.


## Supplement: Hu–Xu–Zhuang prior art and a distinct MNPD status caveat

An additional primary-source check on 12 October 2026 inspected Qiming Hu, Baogang Xu and Miaoxia Zhuang, *Some properties of minimally nonperfectly divisible graphs*, arXiv:2603.01967v2, revised 5 March 2026. Public record: https://arxiv.org/abs/2603.01967v2 ; full text: https://arxiv.org/html/2603.01967v2 ; PDF: https://arxiv.org/pdf/2603.01967v2 . The primary record has no displayed journal reference or acceptance statement; this is treated as a preprint, with no exhaustive publication-status claim.

All of Section 4 and relevant Section 3 dependency arguments were inspected; printed PDF page 11 was visually checked. Theorem 4.1 gives prior necessary conditions for minimally non-2-divisible graphs, including minimum degree at least 2omega−2. Its paired-neighborhood mechanism overlaps the independently derived local blocking argument in STRUCTURAL_PROOFS.md. The subsequent cutset paragraph gives both pieces the full clique number. Lemma 4.1 gives incompatible boundary traces, and Lemma 4.2 gives maximum-clique blocking at each disagreement vertex for side divisions chosen with minimum disagreement. The complete authored reconstruction and dependency audit appears in [PRIOR_CREDIT_AUDIT.md](PRIOR_CREDIT_AUDIT.md).

These are directly relevant prior results. Our preserved complete arguments are independent derivations, with no novelty claim for the overlapping conditions or for any strengthening. The exact feasible-set intersection formulation and numerical consequences here retain their own complete proofs; the discovery of prior necessary conditions does not close the general gluing gap. Neither Section 4 nor the manuscript's restricted MNPD cutset theorem proves unrestricted MN2D clique-cutset exclusion or odd-hole-free 2-divisibility.

A separate later source, Lizhong Chen's arXiv:2607.25412v2 (4 August 2026), concerns minimally nonperfectly divisible graphs and a different prescribed-perfect-part question. Its claimed computer-assisted theorem was not computationally replayed in this check. The [bounded status caveat](RELATED_STATUS_CAVEAT.md) separates a conditional cutvertex inference for those MNPD constructions from the MN2D target: those graphs contain proper induced five-cycles and are not odd-hole-free. No March MNPD question is being promoted to unqualified October open status here. This caveat does not resolve the current target.
