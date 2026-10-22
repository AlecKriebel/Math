# Independent audit of rainbow quadrilateral partial results

## Verdict and exact scope

The frozen seven-file authored package for problem 2315, EP-810, selection rank 903, passes this independent audit as a scoped partial-result package after five of five approaches. Its mathematical arguments are valid under their stated hypotheses. No mandatory mathematical or provenance correction was found, so there is no correction patch or derivative of the author's files. The original author ZIP and all seven original payload members are preserved byte-for-byte.

The strongest accepted result is a uniform negligible-edge-deletion theorem: every edge-colored n-vertex graph whose four-cycles are all rainbow has a spanning properly colored subgraph obtained by deleting o(n^2) edges, without adding colors. Consequently the all-sufficiently-large-size positive-density question is equivalent to the explicitly stated balanced bipartite, proper, at-most-s-palette version. This does not settle that density question.

The original problem remains unresolved by this attempt. Acceptance does not certify a full solution, historical novelty, priority, exhaustive literature coverage, human peer review, or formal proof-assistant verification. The mathematical review imports two credited standard theorems rather than independently reproving their published proofs.

The precise acceptance is stated separately in EXACT_ACCEPTANCE.md and EXACT_ACCEPTANCE.json. The original package's author-stage statements that an independent audit was pending remain unchanged as historical statements; the separate acceptance records this audit's later disposition.

## Frozen object and identity checks

The reviewed author archive is RAINBOW_QUADRILATERAL_2315_AUTHOR_SAFE_FREEZE.zip: 15,279 bytes, SHA-256 2cc0a33b99299d2581cdd4bec4c13e804c5d5537953ab2344bcbdbd8ed1d9a5c. Its external manifest has 2,199 bytes and SHA-256 958facb1869ac5d64c91c1099ca1cc874d4968f09408c1f8117db543808e2124. Independent reads confirmed both pins, all seven listed member byte counts and hashes, unique safe member names, regular non-executable member modes, and ZIP CRC integrity.

All three full input files were read and parsed independently, rather than substituting a selected-record excerpt for a full-file hash. The full catalog and problem list each contain 15,458 records; the full research-results dictionary contains 6,701 entries. Exactly one problem record and one catalog record match ID 2315. The complete exact-ID record and complete inherited report were inspected; the inherited report is empty. The existing background was dated literature triage, not a substantive inherited proof attempt.

The complete pair serialization was Python json.dumps([complete_problem_record, research_results.get(problem_number, {})], sort_keys=True), using default separators and ensure_ascii=True, encoded as UTF-8. Its 3,182 bytes have SHA-256 24ede0f07db766f52b18824edefc6d93deabae359eca0e137733f0c5291b1afb. The statement hash independently equals 32ba9c7103337c765a6124d5a91ac1e6cd06078dc7db39f5a732520378e05117. Full-input hashes, counts, source-PDF pins, and match results are in AUDIT_VERIFICATION_METADATA.json. No dataset record or inherited source content is included.

These checks authenticate reviewed bytes. They are not mathematical proofs and do not establish novelty.

## Exact original problem and conventions

Burr, Erdos, Graham, and Sos define their extremal anti-Ramsey function on printed page 264 using all copies of the target as subgraphs; they explicitly exclude an induced-only reading. The relevant C4 discussion on printed page 273 concerns chi_s(n, epsilon n^2, C4) <= n for a sufficiently small fixed positive epsilon. Independent PDF text extraction and a fresh rendering of page 273 confirm both the quadratic exponent and the weak palette inequality, which OCR alone can misread. [1]

The author therefore correctly uses arbitrary edge colorings, at most n colors, and every C4 subgraph, including cycles with chords. Properness is an additional property proved after deletion, not an original assumption. The imported exact statement explicitly asks for every sufficiently large integer n. The original paper's displayed asymptotic discussion agrees with the target but is not presented here as a separately explicit modern quantifier block. Integer rounding in the edge count does not change the existence of a positive fixed density after decreasing the constant if necessary.

A palette bound refers to available colors, not to requiring every palette element to occur and not to saying that the graph's minimum possible palette equals the bound. This distinction also governs the source comparison below.

## Properization theorem

Consider a monochromatic adjacent pair uv and vw. The graph is simple, so u, v, w are distinct. A second common neighbor z of u and w would be distinct from all three and form the four-cycle u-v-w-z-u. That cycle repeats the color of uv and vw, contrary to the hypothesis. Thus the original common-neighbor set of u and w is exactly {v}.

In the auxiliary graph, A, B, and C are disjoint labeled copies of the original vertex set. The A-B and B-C edge sets are copies of original adjacency, in the indicated orientations. An A-C edge records an ordered pair of distinct endpoints of a monochromatic wedge. Every such A-C edge has exactly one B-neighbor by the preceding original-graph argument. Any triangle in this tripartite auxiliary graph uses an A-C edge, so there are at most n(n-1) triangles, even if the same unordered endpoint pair appears in both orders. Identical original labels in different parts cause no unwanted triangle: an A-C edge requires distinct endpoints, and loops are absent in the original graph.

Use the triangle-removal lemma with epsilon_aux=eta/9 on N=3n vertices. Its deletion allowance is (eta/9)(3n)^2=eta n^2. The ratio n(n-1)/(3n)^3 is at most 1/(27n), uniformly over the original graph and every palette. For each fixed eta, choose n large enough that this ratio satisfies the lemma's triangle threshold. Different conventions counting labeled versus unlabeled triangle copies alter only a fixed factor in that threshold and do not affect the stated conclusion. Fox's introduction and graph-removal theorem supply the needed quantified removal statement and credit the triangle case to Ruzsa and Szemeredi. [3]

The transfer of a deletion set is valid in each of its three cases. Deleting an A-B edge deletes its corresponding first original wedge edge. Deleting a B-C edge deletes its second original edge. Deleting an A-C edge deletes uv, where the unique common neighbor v is fixed in the original graph. That uniqueness ensures that the last prescription hits the original wedge represented by any triangle using the A-C edge. Each deleted auxiliary edge maps to one original edge, so taking a union can only reduce the number of deletions.

If an original monochromatic wedge survived, its original auxiliary triangle would have been hit by a removed auxiliary edge, whose image is one of the two allegedly surviving wedge edges. This contradiction proves properness. Removing edges creates no new C4, hence preserves the rainbow condition. No recoloring is performed. The graph retains all n vertices, and no palette-dependent threshold has entered the proof.

The theorem is therefore accepted with its full uniform quantifiers. It is an asymptotic existence argument using triangle removal, not a supplied efficient deletion algorithm or a proof that properly rainbow-C4-colored graphs are sparse.

## Extremal and all-size consequences

For fixed n, the finite extremal maxima E_R(n) and E_B(n) exist; colors may be taken from a labeled n-element palette. Because B implies R, E_B(n)<=E_R(n). For each eta>0, the properization theorem applied to an R-extremizer gives E_B(n)>=E_R(n)-eta n^2 for every sufficiently large n. This establishes the claimed uniform o(n^2) difference.

A nonnegative sequence E_R(n)/n^2 has a positive lower limit exactly when it is eventually bounded below by some positive constant. This is the all-large-n affirmative target. Subtracting o(1) leaves its equivalence with the B version intact. Its negation is lower limit zero. A universal little-o estimate would imply that negation, but is a stronger assertion; the note correctly refrains from silently replacing a lower-limit claim by a full limit.

For the forward balanced reduction, start separately at each sufficiently large integer s. Properization with eta=epsilon/2 retains at least epsilon s^2/2 edges. Some cut retains at least half of these, hence epsilon s^2/4 edges. Delete non-crossing edges and pad each side to exactly s vertices. Properness and the rainbow condition are hereditary, and the palette stays at most s. Thus beta=epsilon/4 works for every sufficiently large s.

Conversely, at every sufficiently large N choose s=floor(N/2), take the asserted graph with parts of size s, and add at most one isolated vertex. For N>=3, s>=N/3, so its edge count is at least beta N^2/9 and its palette is at most s<=N. This construction covers every sufficiently large N rather than only an unbounded subsequence. Both density losses are fixed constants, so positive density is preserved.

## Literal palette wording in the 2023 source

Gyárfás and Sárközy define B-colorings to be proper with every C4 rainbow, exactly as in the note. They define q_B(G) to be the minimum number of colors in such a coloring. Their Question 1.3, printed page 112, literally assumes balanced parts of size s and q_B(G)=s. The accepted Corollary 3 instead assumes the existence of a B-coloring with at most s colors. [2]

These formulations must not be called literally identical merely by allowing unused palette elements: adding unused colors does not change a minimum. The frozen note uses its own at-most-s formulation consistently, and its contextual sentence linking this with the B-density question does not use an equality-of-minima assertion in a proof. No mathematical repair is required. This audit accepts the proved at-most-s formulation only and does not certify an additional equivalence with the literal equality hypothesis in Question 1.3. Nor does it identify the exact negation of EP-810 with the full universal sparsity assertion asked in that source.

## Hypergraph projection and failed converse

A linear tripartite 3-uniform hypergraph with parts X, Y, Z projects each triple {x,y,z} to xy colored z. Two different triples cannot project to the same xy, since they would share x and y. Two incident projected edges cannot share color z, since their triples would then share an endpoint and z. The projection is thus a simple proper bipartite edge coloring.

If a projected C4 were non-rainbow, its four distinct edge triples would use four X/Y vertices and at most three Z vertices. Thus four hyperedges would lie on at most seven vertices. A (7,4)-free hypergraph excludes this, proving the forward implication.

For the converse counterexample, the path x1-y1-x2-y2-x3 has four edges colored a,b,a,b. It is proper and has no C4 at all. Its four associated triples use three X vertices, two Y vertices, and two colors, for exactly seven vertices. Pair intersections are respectively {y1}, {a}, empty, {x2}, {b}, and {y2}; each has size at most one. Thus the hypergraph is linear and tripartite but fails the (7,4)-free condition. Adding unused vertices or color labels does not remove these four edges on seven vertices.

The 2023 source discusses the two relevant projections of its configuration C14, including the alternating four-edge path, and distinguishes the A, B, and combined C variants. Its Proposition 1.6 equates the combined C sparsity conjecture with the (7,4) conjecture. The note correctly does not substitute that result for a B-only equivalence. [2]

## Cyclic affine-label obstruction

The theorem has exactly the stated restricted domain: both vertex classes are copies of Z/mZ; the two coefficients are units; the offset is arbitrary; and the color is an arbitrary function of the single affine residue. Unit multiplication separately permutes the two vertex classes and preserves the edge count, reducing the labels to f(u+v+z).

Use representatives from {0,...,m-1}^2. Gowers's finite multidimensional Szemeredi theorem, Theorem 10.3, applies to the fixed four-point integer square and produces a positive integer dilation. The original Furstenberg-Katznelson theorem is the credited source of the multidimensional result. The audit checked the finite statement rather than inferring positivity or a finite-grid quantifier from an ambiguous extracted line in the older source. [4,5]

For completeness, the note's upgrade from one finite grid size to all sufficiently large m is justified explicitly. Choose a square size L supplied by the finite theorem at density delta/2. Tile the lower-left kL by kL square inside an m by m square by L by L tiles, where k=floor(m/L). The discarded boundary has fewer than 2Lm points. If all tiles had density less than delta/2, the original set would contain fewer than (delta/2)m^2+2Lm points, contradicting density at least delta once m>4L/delta. Hence one tile supplies the required square.

All four square coordinates are genuine integer representatives, and 1<=d<m, so the two row vertices and the two column vertices remain distinct modulo m. They define four present edges of a C4. The off-diagonal affine inputs both equal u+v+d+z modulo m, forcing equal colors regardless of the output function. This contradicts the rainbow hypothesis. The density threshold depends only on delta and the fixed pattern, so the little-o conclusion is uniform in the coefficients, offset, and output function.

The proof uses no primality assumption. It gives no claim about nonunit coefficients, general Latin squares, or growing-dimensional vector-space labels. No quantitative rate is asserted.

## Complete blowups and codegrees

In K_{s,t}, s,t>=2, disjoint edges complete a C4 on their four endpoints. For edges meeting at one endpoint, a second vertex in that endpoint's part completes a C4. Thus every distinct pair of edges must have different colors in an R-coloring. Exactly st colors are necessary and sufficient.

A fixed h-vertex seed containing an edge has a K_{t,t} in its complete uniform t-fold blowup. For t>=2 the blowup therefore needs at least t^2 colors even if arbitrary recoloring is allowed. When t>h this exceeds the total ht vertices. This invalidates only that complete uniform amplification scheme. Isolated-vertex padding retains edges and colors but changes m/n^2 to m/N^2, so an arbitrarily widely separated sequence of sizes does not by padding alone prove a uniform positive density.

For the codegree bound, any pair with d>=2 common neighbors contains a K_{2,d} as a subgraph, whether or not there are additional edges. It therefore requires 2d colors. For d<=1 the universal bound D=max(1,floor(q/2)) is valid, including q=0,1,2,3. The number of unordered wedges is both sum_v binom(deg(v),2) and the sum of all unordered-pair codegrees. Cauchy-Schwarz gives sum_v deg(v)^2>=4m^2/n for n>=1, hence

2m^2/n-m <= n(n-1)D/2.

Multiplying by n and solving the quadratic gives

m <= n(1+sqrt(1+4(n-1)D))/4.

For q=n, D=n/2+O(1), yielding leading coefficient sqrt(2)/4=1/(2sqrt(2)). The inequality is sound but not sharpness-certified and does not rule out every small positive density. These deductions are analytic checks, not an executable certificate.

## Source review and dated scope

All six recorded public-source PDFs match their frozen byte counts and hashes. The audit freshly extracted text from those exact PDFs and freshly rendered and inspected the original 1989 printed page 273, the 2023 printed page 112, and Gowers's manuscript page 51. The other relevant imported theorem statements and surrounding definitions were read in fresh PDF extractions. Full proofs of the removal lemma, ergodic theorem, hypergraph regularity, and the planar paper were not independently reproved.

The arXiv metadata for Proper edge colorings of planar graphs with rainbow C4-s confirms version 2 was submitted on 29 August 2025. Its title-page date is 3 September 2025, and its journal reference is Journal of Graph Theory 107 (2024), 833-846; these are different date fields, not a reason to relabel the version. Its introduction still discusses the B-coloring density question. Its stated results concern planar and outerplanar host graphs and do not supply the required dense arbitrary-host result. The arXiv record also says a proof error in the earlier version's Theorem 1.4(i) was corrected in version 2; none of those planar bounds is imported into the present proofs. [6]

The three 2026 abstract-level checks were independently repeated on their versioned or current arXiv abstract pages. The March 19 manuscript by Bucic, Chen, and Ma states its principal result for odd cycles of length at least nine. The June 29 Li-Ning-Xie manuscript and July 7 Yang manuscript concern P4, not C4. The report's narrow scope descriptions are supported. Their full proofs were not audited and the abstracts are not evidence of exhaustive absence of a C4 solution. [7-9]

A fresh web request to the Erdos tracker returned HTTP 403. The UnsolvedMath page remained inaccessible through the web tool. The audit does not claim direct tracker access or reclassify either access failure as an open-status confirmation. The historical exact-record triage, the bounded current literature checks, and the absence of a full proof in this package are distinct kinds of evidence. No bypass was attempted.

## Bounded repository check and five-approach limit

Independent read-only connector searches for exact ID 2315 and EP-810 in default-branch code and commits, a branch search for 2315, and a combined pull-request search for the ID, EP number, and rainbow-quadrilateral phrase returned no matches in AlecKriebel/Math. These fresh checks are consistent with the corresponding author-stage metadata. The broader author-stage search for 810 or quadrilateral was not replayed; its recorded results are historical metadata, not newly certified search results.

These are bounded searches, not an exhaustive examination of every branch, commit, diff, issue, or manuscript. They establish no novelty clearance. This audit performed no GitHub write or publication.

The five recorded mathematical approaches are the properization reduction, hypergraph comparison, cyclic affine obstruction, complete-blowup/padding obstruction, and codegree count. The review verifies them and their cited premises; it does not open a sixth solution attempt. The remaining density gap is stated explicitly after every approach and in the final task statement.

## Publication-safe boundary and acceptance limits

The safe audit archive contains the unchanged authored original, this authored mathematical review, the separate exact acceptance, public bibliographic links, and verification metadata only. It excludes raw PDFs, source text extractions, source images, raw corpus contents, private source locations, credentials, and private coordination material. No executable solver or verifier is included. Byte hashing, JSON parsing, PDF extraction, and ZIP integrity checks are technical identity/inspection operations, not normal or optimized mathematical proof-validation runs.

No full solution, global current-open certification, automatic novelty conclusion, merge, release, or external submission is accepted. The final disposition is UNSOLVED_SCOPED_PARTIALS_ACCEPTED, five of five approaches. The narrower claims in the separate exact acceptance are the only mathematical claims approved by this audit.

## Public references

[1] S. A. Burr, P. Erdos, R. L. Graham, and V. T. Sos, Maximal Antiramsey Graphs and the Strong Chromatic Number, Journal of Graph Theory 13 (1989), 263-282. https://doi.org/10.1002/jgt.3190130302 ; https://users.renyi.hu/~p_erdos/1989-10.pdf

[2] A. Gyarfas and G. N. Sarkozy, Less Strong Chromatic Indices and the (7,4)-Conjecture, Studia Scientiarum Mathematicarum Hungarica 60 (2023), 109-122. https://doi.org/10.1556/012.2023.01539 ; https://www.renyi.hu/~gyarfas/Cikkek/204_studia.pdf

[3] J. Fox, A new proof of the graph removal lemma, Annals of Mathematics 174 (2011), 561-579, arXiv:1006.1300v2. https://arxiv.org/abs/1006.1300v2 ; https://annals.math.princeton.edu/2011/174-1/p17

[4] H. Furstenberg and Y. Katznelson, An ergodic Szemeredi theorem for commuting transformations, Journal d'Analyse Mathematique 34 (1978), 275-291. https://doi.org/10.1007/BF02790016 ; https://www.cs.umd.edu/~gasarch/TOPICS/vdw/ergodicsz.pdf

[5] W. T. Gowers, Hypergraph regularity and the multidimensional Szemeredi theorem, Annals of Mathematics 166 (2007), 897-946, Theorem 10.3 in arXiv:0710.3032v1. https://arxiv.org/abs/0710.3032v1

[6] A. Gyarfas, R. R. Martin, M. Ruszinko, and G. N. Sarkozy, Proper edge colorings of planar graphs with rainbow C4-s, arXiv:2408.09059v2. https://arxiv.org/abs/2408.09059v2

[7] M. Bucic, K. Chen, and J. Ma, On a maximal anti-Ramsey conjecture of Burr, Erdos, Graham, and Sos, arXiv:2603.18952v1. https://arxiv.org/abs/2603.18952v1

[8] M. Li, B. Ning, and T. Xie, Two problems of Burr, Erdos, Graham, and Sos on maximal anti-Ramsey functions for P4, arXiv:2606.30505. https://arxiv.org/abs/2606.30505

[9] Z. Yang, On the maximal anti-Ramsey problem of Burr, Erdos, Graham, and Sos for P4, arXiv:2607.05896v1. https://arxiv.org/abs/2607.05896v1
