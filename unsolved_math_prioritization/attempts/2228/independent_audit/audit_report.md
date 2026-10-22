# Independent audit of EP 642 partial results

Date: 2026-10-06. Problem: UnsolvedMath 2228, EP-642, catalog rank 900.

## Decision

Accept the elementary mathematical results in the exact pinned author packet. The problem remains partial and stalled after three of the five allowed approaches. This audit accepts no full solution, asymptotic improvement, or novelty claim. No mathematical proof correction is needed.

One executable-validation issue requires a separate hardened derivative: the author's assertions disappear under Python optimization. The original is preserved byte-for-byte. The supplied patch replaces its six assertions with explicit exceptions; the corrected checker passes normal, optimized, relocated, and independent-oracle tests. This is a validation correction, not an additional mathematical approach.

The separate acceptance_report.json specifies the exact accepted objects and exclusions. Its acceptance is bounded to the material and checks described here, not an independent certification of the cited papers' complete proofs.

## Exact inputs and preservation

The original archive is 11,900 bytes with SHA-256 970e1d0e9eeee5ff0357c91aabba26f6343955e936167280726a05b0ac68ffdd. Its external manifest is 1,869 bytes with SHA-256 5189f13df28414cb1438e75782e332f0d1db2a26d193f5b6135e195fb537ce82. All eight member names, byte counts, and hashes match. The archive has no duplicate members. The author_original directory in this audit contains the exact original member bytes, and author_external_manifest.json is the exact original manifest.

All three complete input files were rehashed, with exact agreement to the declared byte counts and SHA-256 values. The unique exact-ID problem record was read completely, including its nested fields and existing background triage. The corresponding complete research result was empty. The catalog ID is a string while the problem-record ID is numeric; matching after explicit string conversion selects the same unique problem and rank 900. The complete record/report pair was reserialized as json.dumps([complete_record, reports.get(problem_number, {})], sort_keys=True), using Python's default separators and default ensure_ascii setting. Its SHA-256 is 6d25000c72e7a32ec102c00260446deeca752b3b7d9be7f0fd7b7aa4e9d82220. The statement hash is 77fbe5c358505c7644cfa24b699a7938f7bd44601453f97a5089d26448f0e24c.

Only hashes, sizes, and match results are included. Input contents, source documents, and private coordination files are excluded. The original archive and its external manifest were not edited. The original status still says independent audit pending because historical author bytes are intentionally preserved; this separate report and acceptance record supply the current review outcome.

## Exact target and conventions

The graph is finite, undirected, and simple. A simple cycle C has at least three vertices. A chord is an existing graph edge between two nonconsecutive cycle vertices. Missing edges and geometric intersections do not count. The forbidden condition is q_G(C) >= |C|, including equality. The admissible condition is q_G(C) < |C| for every cycle. The graph order n is distinct from a returned cycle length. The extremal target is one constant K valid for every n, with f(n) <= Kn.

The indexed Erdős tracker discussion supplies this formulation, a clarification of chords, and an open label. A fresh direct history-page request returned HTTP 403. This does not establish successful direct access to either original problem page. An open label and a bounded search are not proofs that all later or unpublished work has been excluded.

## Analytic verification

### The induced-edge and boundary identities

For S=V(C), exactly |S| edges of G[S] are edges of C. Thus q_G(C)=e_G(S)-|S|. The sum of ambient degrees over S is 2e_G(S)+e_G(S,V(G) minus S). Substitution gives

2(q_G(C)-|S|) = sum over v in S of (d_G(v)-4) - e_G(S,V(G) minus S).

Both identities use the original graph. It follows that a forbidden cycle is exactly a cycle whose vertex set induces at least 2|S| edges. There is no hidden assumption that the cycle is induced.

### The constant-core equivalence

Admissibility is hereditary for arbitrary subgraphs, not only induced subgraphs: every cycle surviving in a subgraph has no more chords there than in the original graph. If e(G)<=K|V(G)| holds for all admissible graphs, choose an integer D>2K. Every nonempty graph of minimum degree at least D has e(G)>=D|V(G)|/2>K|V(G)|, so it is not admissible.

Conversely, if an absolute D forces a forbidden cycle, every nonempty subgraph of an admissible graph has minimum degree at most D-1. That is precisely (D-1)-degeneracy. If all admissible graphs are r-degenerate, remove a vertex of current degree at most r repeatedly. Each edge is counted once at its earlier deleted endpoint, yielding e(G)<=r|V(G)|. Choosing K=max(1,r) handles the stated positive-K convention. Empty graphs cause no exception; the minimum-degree statement explicitly concerns nonempty graphs.

All three implications are valid. The equivalence is a reformulation of the open global problem, not a proof of its missing absolute threshold.

### The maximum-degree-four classification

Suppose the maximum degree is at most four and C is forbidden. Then

2|S| <= e_G(S) <= (1/2) sum over v in S of d_G(v) <= 2|S|.

Equality throughout forces every vertex of S to have ambient degree four and the entire boundary of S to be empty. The cycle connects S, so G[S] is one connected component, rather than a union of components. It is four-regular and the cycle is Hamiltonian there. Conversely, a Hamiltonian cycle in a four-regular component on s vertices has 2s-s=s chords. Equality is correctly included in the forbidden condition.

This proof also handles disconnected graphs and isolated vertices. It does not classify graphs of unrestricted maximum degree. In a connected four-regular non-Hamiltonian graph, no forbidden cycle exists.

### The eleven-vertex obstruction

Each of the two old K5 copies loses one edge, giving nine edges and endpoint degrees three. Joining a new vertex z to the four deficient endpoints restores every old degree to four and gives z degree four. There are 11 vertices and 2*9+4=22 edges. Each old copy is connected, both meet z, and no edge joins the old copies; the graph is connected. Removing z leaves exactly two components, so z is a cut vertex.

Deleting any vertex of a Hamiltonian cycle leaves a spanning path on the remaining vertices. Therefore a Hamiltonian graph on at least three vertices cannot have a cut vertex. The example is non-Hamiltonian and hence admissible by the preceding classification. Its minimum degree is four, refuting every proposed universal threshold D<=4. It does not refute D>=5 or the linear upper bound.

Every cycle lies in one of the two six-vertex blocks consisting of z and an old copy: a simple cycle cannot enter both components of G-z without using z twice. Each block has a six-cycle through z and a Hamiltonian path between the missing-edge endpoints of K5 minus that edge. Thus the exact longest length is six. Such a cycle induces all 11 edges in its block, has five chords, and has two boundary edges; its margin is 5-6=-1.

There are 37 cycles per block: K5 minus one edge contributes 22 cycles, and the paths between the missing-edge endpoints contribute 3+6+6=15 cycles through z. The complete graph therefore has 74 cycles, with length distribution 14 triangles, 24 four-cycles, 24 five-cycles, and 12 six-cycles. Independent subset dynamic programming reproduces the count, longest length, and maximum margin -1. Consequently the proposed boundary inequality at D=4 fails even for a longest cycle.

### The complete-bipartite lower bound

A cycle in K_{3,n-3} alternates between the two parts, using k vertices from each with k in {2,3}. Its induced subgraph is K_{k,k}, so it has k^2-2k chords: zero for k=2 and three for k=3, below its length in both cases. For n>=6 this gives an admissible graph with exactly 3n-9 edges. The lower-bound coefficient tends to three, ruling out a global constant K<3. The family is not claimed optimal and is not a superlinear counterexample.

### The precise remaining gap

A cycle qualifies if its ambient degree surplus above four covers its entire boundary. Minimum degree D makes the stronger inequality boundary <= (D-4)|C| sufficient. Neither inequality is proved at an absolute D. A longest cycle prevents an outside vertex from meeting two consecutive cycle vertices, since insertion would lengthen it; this local observation does not bound the total boundary. The obstruction at D=4 says nothing decisive about higher D.

For fixed positive a,c, the ratio a/(log l)^c tends to zero. A lower bound of a*l/(log l)^c on a cycle's chord count therefore cannot alone guarantee chord density at least one. The source theorem chooses some cycle length, without prescribing it. Repeating it does not supply a common cycle or a retention rule for previously obtained chords. The report correctly stops before these unjustified inferences.

## Source verification and limits

Four stored public PDFs were independently rehashed and agree exactly with the original metadata. Three theorem pages were freshly rendered from those pinned PDF bytes and visually inspected, with the corresponding extracted text also checked:

1. Draganić, Methuku, Munhá Correia, and Sudakov, Cycles with many chords, arXiv:2306.09157v2, page 2, Theorem 1.1. For sufficiently large n, at least n(log n)^8 edges force a cycle with at least its length in chords. This gives the asserted O(n(log n)^8) upper bound. The publication is Random Structures & Algorithms 65 (2024), 3-16. The separately hashed published PDF is not substituted for the inspected arXiv version. https://arxiv.org/abs/2306.09157 and https://doi.org/10.1002/rsa.21207

2. Draganić and Girão, Cycles with almost linearly many chords, arXiv:2601.08769v1, page 2, Theorem 1.1. Its constants are absolute, its hypothesis is constant minimum degree, and the chord guarantee retains the polylogarithmic denominator. The introduction explicitly treats even a fixed positive linear fraction of the cycle length as an open target. The current arXiv page identifies v1, submitted January 13, 2026. This audit checks the statement and its use, not the entire proof. https://arxiv.org/abs/2601.08769

3. Letzter, Methuku, and Sudakov, Nearly Hamilton cycles in sublinear expanders, and applications, arXiv:2503.07147, page 30, Corollary 7.2. The sufficient count is n(log n)^130 for sufficiently large n. For large n this is a larger required edge count than exponent eight, so it is a weaker sufficient condition. The current arXiv record identifies v2, revised January 21, 2026; the official publisher record identifies the 2026 Journal of the London Mathematical Society publication, 113, e70452. https://arxiv.org/abs/2503.07147 and https://doi.org/10.1112/jlms.70452

The indexed tracker discussion includes a suggestion that parameter tightening might yield exponent seven. This audit did not verify that suggestion as a proved primary-source update. Accordingly, exponent eight is the strongest bound verified here; no claim of exhaustive best-known status is made. The discussion also mentions denser finite examples than the elementary bipartite family. Neither point contradicts a claim made in the authored proofs. https://www.erdosproblems.com/forum/thread/642

The original 1997 Erdős page and the complete 1996 Chen-Erdős-Staton paper were not inspected in this audit. Their exact historical wording and provenance are not independently certified. The author's historical access failures and repository-search history are preserved as reports of that earlier run, not re-created observations. This audit did not independently rerun the six repository queries and makes no novelty inference from them.

## Executable verification

The original checker was executed from relocated copies in normal and optimized modes. Both regenerate the exact 1,419-byte original results file, SHA-256 79d30b33b5af14045a70875eb1bc6d969eedbda9e0673791403563073c6eaedf. However, optimized execution strips all six assertions. A controlled mutation changing the degree surplus from d(v)-4 to d(v)-5 fails normally yet exits successfully with passed=true under -O. Thus the original optimized run is not accepted as an active validation test.

The corrected derivative keeps the formulas and finite test domain unchanged, replacing assertions with explicit ValueError checks. The patch is supplied, and its regenerated results are byte-identical to the original. The same invalid boundary mutation is rejected normally and under -O.

The independent oracle uses subset dynamic programming for paths starting at their least vertex. A path is closed only when its last vertex neighbors the start. Every undirected simple cycle is counted twice, once per orientation, and the closing-path total is divided by two. This method is distinct from the author's recursive cycle enumeration. Counts by vertex subset are compared, not merely aggregate totals. The oracle separately counts induced edges, boundary edges, and union-find components. It also checks emitted-cycle simplicity, adjacency, canonical orientation, uniqueness, summary fields, K5 equality witnesses, and K5 with an isolated vertex.

The finite graph count is 1+1+2+8+64+1024=1100 for orders zero through five. Six bipartite examples have cycle totals 15, 42, 90, 165, 273, and 420, also checked against 3*binomial(n-3,2)+6*binomial(n-3,3). All these independent comparisons pass normally and under -O.

Five additional semantic mutations are each rejected in both modes: making the forbidden inequality strict, duplicating cycle orientations, misclassifying degree three, dropping the closing-edge requirement, and subtracting the wrong number of cycle edges. Eight package-integrity mutations, each tested normally and under -O, are also rejected: changed original proof, missing original member, extra member, changed status, changed acceptance, changed corrected results, changed manifest, and wrong external manifest pin. The exact public diff reconstructs the corrected checker byte-for-byte. Archive/member hash checks and status checks are distinct from mathematical tests. Hash matching establishes byte identity, not mathematical truth. Finite computation establishes neither the infinite extremal conjecture nor an absolute threshold.

## Final scope

The corrected executable and the elementary partial proofs are accepted. The original is retained for provenance and normal-mode reproducibility; its optimized validation is explicitly not accepted. The exact unresolved work is still the absolute minimum-degree theorem, equivalently a suitable global cycle-boundary inequality or the linear extremal upper bound. No fourth or fifth mathematical approach is claimed. Nothing was published and no repository or queue item was changed by this audit.
