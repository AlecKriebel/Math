Editorial note: This is the complete authored text. Only references to undistributed operational files, their identities, locations and replay directions have been replaced. All mathematical arguments, exact finite counts, corrections and limitations are retained. The public manifest identifies the actual distributed files.

# Independent acceptance: final divisibility order, core, and separator barriers

## Decision and exact scope

**ACCEPTED after a narrow concluding-scope correction.** The final fixed proof establishes the all-size partial results below. The unrestricted assertion that odd-hole-free graphs are 2-divisible remains unresolved. No sixth substantive pass, novelty claim, best-known-bound claim, remote action, or queue mutation is part of this audit.

Acceptance applies only to the replacement final proof, whose exact external pin, manifest, complete proof and checker identities were independently verified. Their undistributed operational identities are omitted from this prose edition.

The previously supplied pin `[verified identity of undistributed artifact]` is superseded. Comparison of the two manifests shows that only the proof payload changed. The audited edit separates the unconditional k=4 total-order/core bounds from the clique-cutset bounds, which require induced-minimal indivisibility. The actual separator argument already had this hypothesis; the earlier concluding sentence omitted it. The replacement proof retains it explicitly.

`the closed authored source copy` contains exactly the eight final authored files, including the manifest. `the original operational record` is external to that copied packet. The seven required prior authored dependencies are copied unchanged into the closed `the closed dependency copy` tree; this includes the accepted linear-compression correction, so the original exact-core audit's superseded exponential representation-size statement is not revived. Every dependency hash and length is checked before execution. No copied third-party source documents are included.

## 1. Critical decomposition and the antineighborhood theorem

An induced subgraph H with chromatic number q, chosen minimally by vertex deletion, is vertex-critical. The components of its complement give pairwise completely joined induced factors H_i. Their chromatic numbers and clique numbers add. Each factor is itself vertex-critical: deleting a vertex without reducing its own chromatic number would preserve chi(H). A singleton complement component is connected and has both invariants one.

Applying the explicitly imported Gallai theorem to each factor gives |H| >= 2q-t. This does not assume that G is vertex-critical, that G is division-minimal, or that a minimum induced indivisible graph retains the original chromatic number.

For the antineighborhood property, select a factor of minimum clique number r_i and a vertex v in that factor. A maximum k-clique anticomplete to v cannot meet another factor, since all such vertices are adjacent to v. Its intersection with H has at most r_i vertices. Thus the outside count m=n-|H| is at least k-r_i. Since the remaining t-1 factors have positive clique numbers, r_i <= k-t+1. Hence m >= t-1 and n >= 2q-1.

The equality restriction is valid. Equality forces m=t-1 and r_i=k-t+1. If t>=2, minimality of r_i gives t(k-t+1) <= omega(H) <= k, while t<=k. Therefore (t-1)(k-t)<=0 implies t=k. Every factor has clique number one, so vertex-criticality makes each a singleton and q=k. This contradicts the equality statement's hypothesis q>k. Consequently t=1 and m=0: G itself is vertex-critical and has connected complement.

This theorem explicitly concerns nonempty G. Its hypothesis can hold for edgeless graphs of order at least two; the argument still works with k=q=1. The equality conclusion is deliberately restricted to q>k. Empty graphs occur only as computational boundary cases and are not asserted to satisfy the antineighborhood hypothesis.

For an indivisible graph with k>=2, grouping at most 2k-2 proper color classes into two groups would give a division. Thus q>=2k-1. Also, if M(v) had no k-clique, N(v) and {v} union M(v) would be a division: their clique numbers are at most k-1 and max(1,omega(M(v))), respectively. The k>=2 hypothesis is needed for this last maximum to remain below k. Therefore every indivisible graph has n>=4k-3. Equality forces q=2k-1>k, vertex-criticality, and connected complement. C5 verifies the k=2 equality boundary.

These statements are structural consequences of a classical external theorem. They are not presented as new or strongest numerical Folkman bounds.

## 2. Odd-hole-free chromatic-gap theorem

A triangle-free odd-hole-free graph is bipartite: a shortest odd cycle, if any, would be an induced odd cycle of length at least five. A vertex-critical graph with equal chromatic and clique numbers is complete, because deleting a vertex outside a maximum clique would preserve its chromatic number.

In the complement-connected critical decomposition of an odd-hole-free graph, a factor of clique number two would therefore have to be K2, whose complement is disconnected. A factor of clique number three has chromatic number at most four by the explicitly imported CRST theorem; it cannot be K3, so its parameters are (4,3). The only remaining factors are singletons or have clique number at least four. Heredity of odd-hole-freeness justifies applying these facts to all induced factors.

If some factor has clique number at least four, then omega(H)-t >=3, and Gallai yields n>=2q-omega(H)+3>=2q-r+3. Otherwise, writing a for singleton factors and b for the (4,3) factors gives q=a+4b, omega(H)=a+3b, and t=omega(H)-2b. The hypothesis q>=r+2 and omega(H)<=r forces b>=2. This second case gives the strictly stronger n>=2q-r+4.

Equality in n>=2q-r+3 consequently comes only from the first case. It forces G=H, omega(H)=r, and omega(H)-t=3. Exactly one factor has clique number four, and all others are singletons. Thus r>=4 and G=K_(r-4) join J, with J odd-hole-free, vertex-critical, complement connected, omega(J)=4, chi(J)=q-r+4, and |J|=2(q-r+4)-1. This is a necessary equality form, not an existence or sharpness assertion. No missing factor type or equality case was found.

The join of two C5s has (n,q,r)=(10,6,4), violating the proposed order bound if the odd-hole-free hypothesis is removed. The join of two seven-antiholes is an odd-hole-free, chromatic-gap-two benchmark of order fourteen; it satisfies the bound but does not attain equality.

## 3. High-incidence core consequences and the eight-vertex boundary

X is defined using at least three occurrences in the original distinct maximum-clique family. Recomputing incidences inside G[X] would change the object and is not used.

The accepted core theorem supplies chi(G[X])>=2k-3 and omega(G[X]) in {k-1,k}. For k>=5, the core's chromatic gap is at least two, so the preceding theorem yields |X|>=3k-3. When its clique number is k-1, the stronger |X|>=3k-2 follows. In either case equality forces chi(G[X])=2k-3 and the stated join decomposition. The remaining factor has parameters (omega,chi,order)=(4,k+1,2k+1) in the first case and (4,k+2,2k+3) in the second. At k=5 the latter has no singleton join factor. The arithmetic is correct.

For k=4, CRST rules out core clique number three because the accepted chromatic lower bound is five. The existing core order bound is eight. At order eight, the new gap theorem rules out core chromatic number at least six. An induced 5-critical H in the core cannot have a factor of clique number at least four: it would be the only factor and Gallai would require at least nine vertices. The remaining factor equations force exactly one (4,3) factor and one singleton. Their minimum orders seven and one exhaust the entire eight-vertex core. Hence the core is K1 joined to a seven-vertex 4-critical odd-hole-free graph with clique number three and connected complement.

The fixture K1 join anti-C7 satisfies this boundary and is itself divisible: color the universal vertex one color and the rim the other. Its seven maximum K4s give original clique incidences seven at the universal vertex and three at every rim vertex. This illustrates the limitation correctly. A universal vertex inside the core need not be universal in G, and the core's own division is not asserted to extend.

No classification of every possible seven-vertex factor J or realization as the core of an odd-hole-free indivisible graph is established here.

## 4. Clique-cutset consequences and minimality

These results require an induced-minimal indivisible graph, with proper nonedgeless induced subgraphs divided at their own clique numbers. They do not apply to arbitrary indivisible graphs merely because a clique cutset is present.

The accepted separator argument gives each side H_i local clique number k, chromatic number at least 2k-1, and failure of at least one admissible boundary coloring. Its odd-hole-freeness is inherited. The gap theorem therefore yields |H_i|>=3k+1 for k>=4.

For k>=5, equality would produce a universal vertex in H_i through its K_(k-4) join factor. The universal-vertex flexibility argument excludes this. If a universal vertex u is precolored on the clique C, color all new vertices opposite u; admissibility keeps the u-colored subset of C below size k. If u is unprescribed, choose a color used on at most k-2 vertices of C, and color every other new vertex oppositely. Such a choice always exists because |C|<=k-1. The opposite color lies in H_i-u, of clique number k-1. This works also for k=2 and for empty, nonmaximum, and maximum clique boundaries.

Thus |H_i|>=3k+2 for k>=5. Counting C once rather than t times yields n>=s+t(3k+1-s) at k=4 and n>=s+t(3k+2-s) at k>=5. Since s<=k and t>=2, the total bounds are 22 for a k=4 clique cutset, 24 for a k=4 edge cutset, 5k+4 for arbitrary clique cutsets at k>=5, and 6k+2 for edge cutsets there. None excludes all clique cutsets or supplies compatible boundary traces. The old trace-orbit restrictions remain separate necessary conditions.

## 5. External sources and Folkman terminology

The graph's indivisibility is exactly vertex-arrowing (k,k). The no-K_(k+1) restriction bounds its clique number above by k; arrowing guarantees a K_k, so the clique number is exactly k. Its minimum order over all graphs is therefore F_v(k,k;k+1). This is the vertex Folkman convention, not an edge-coloring Folkman number and not perfect divisibility.

Gallai's vertex-critical convention and non-strict order inequality were independently checked in [Stehlik's author-hosted lecture](https://oc.g-scop.grenoble-inp.fr/fichiers/stehlik.pdf), PDF pages 2 and 10. The page-10 glyph was verified in rendered pixels because one web text extraction incorrectly displayed a strict sign. The [primary 2003 publisher abstract](https://www.sciencedirect.com/science/article/pii/S0095895603000698) independently states the Gallai consequence and its strengthening. This audit imports the classical theorem; it does not claim a fresh complete proof audit.

The [CRST author-hosted primary paper](https://thomas.math.gatech.edu/PAP/k4free.pdf), revised August 5, 2009, states the K4-free odd-hole-free four-color theorem as Theorem 1.3 and again as 3.2. Its statement and hypotheses were independently inspected. Its full decomposition proof is not re-audited here.

[Bikov and Nenov's published primary paper](https://www.fmi.uni-sofia.bg/sites/default/files/biblio/fulltext/104-039-053.pdf), Annual of Sofia University 104 (2017), 39–53, Theorem 5.2, gives F_v(4,4;5)>=19. Its definitions, theorem, proof's Algorithm 3.5 dependency, and reported Table 5 were inspected, and the [explicit arXiv v1](https://arxiv.org/pdf/1711.01535v1) agrees. This is an imported computational theorem: its large enumeration was not rerun or independently certified. The source's secondary credit to Xu and Shao for a stronger general lower bound is retained only as attribution; neither its original proof nor full parameter scope was independently checked. No latest-best claim follows.

The three retrieved PDF hashes and byte counts match the authored metadata and are recorded with inspection limits in `the complete scholarly source audit`. Only public metadata and authored analysis are preserved in this packet.

## 6. Independent finite verification

The independent program imports no authored or prior mathematical checker. For every graph on zero through six labelled vertices, it directly tests all pairs in every vertex subset for clique and stable-set membership, derives each induced clique number from these direct tests, and determines each induced chromatic number by enumerating set partitions into stable classes. It independently forms complement components through label merging, enumerates all whole-graph two-colorings, and checks every universal-vertex boundary both by exhaustive extension and by the displayed construction.

It additionally checks all vertex-critical induced subsets, not only the author's selected chi-critical H. The independent graph stream and universal-boundary stream match the authored streams exactly, as do the complete expected data, not merely totals. The exhaustive scope and key totals are:

- 33,868 labelled simple graphs, including empty, disconnected, and edgeless cases.
- 1,722 graphs satisfying the antineighborhood hypothesis, of which 624 have chi>omega.
- 12 antineighborhood equality cases with chi>omega, exactly the labelled C5s.
- 624 indivisible graphs; all have clique number two in this small universe.
- 31,912 odd-hole-free graphs, with no chromatic-gap-two case in the exhaustive small universe.
- 24,312 admissible universal-vertex clique-boundary assignments through order five.
- 580,542 vertex-critical induced-subset instances, including the explicitly harmless empty computational case.

The seven named larger benchmarks are independently reconstructed and colored by a separate backtracking coloring algorithm. Direct clique enumeration checks their clique numbers. The eight-core incidences, the non-odd-hole-free hypothesis control, and the join-of-antiholes example agree with the authored data.

The 25-vertex C5[C5] benchmark is independently reconstructed from adjacency rules. Recursive clique enumeration finds exactly 125 maximum cliques of order four and incidence twenty at every vertex. Every inner block coloring has at least one monochromatic edge; all 32 block colorings induce exactly three nonempty edge-color states. All 243 assignments of these states to the outer C5 force adjacent blocks sharing an edge color and hence a monochromatic K4. This certifies indivisibility. Three colors are needed per block, and a color can appear in at most two blocks, forcing at least eight colors; a separate palette backtracking search finds eight colors. Choosing one vertex from each block gives an induced C5, so this is no odd-hole-free counterexample.

The independent finite arithmetic checks reproduce all 10,814 critical-factor parameter records and 3,213 cutset records with identical stream hashes. These are bounded arithmetic checks of the proof, not claims that all parameter lists are graph-realizable.

Normal Python, -O, and -OO all reproduce identical independent results. The final authored verifier is separately rerun in all three modes on the closed copied inputs and dependencies, with identical outputs matching its expected results. The exhaustive k>=3 indivisibility and core-gap consequences are vacuous in the small graph universe; their acceptance rests on the all-size proofs and external theorem dependencies, not those finite tests.

## 7. Integrity, hostile controls, and terminal boundary

The independent input verifier hardcodes the replacement external-pin and manifest identities, checks their exact lengths, requires the complete eight-file packet, rejects nonregular files and symlink path components, rejects duplicate JSON keys, and verifies every payload. The dependency tree is independently required to contain exactly the seven mandatory files and their necessary directories, with no extras. Closed input copies avoid reliance on a changing broader workspace.

The authored final controls are independently rerun under all three interpreter modes. All 65 required negative controls per mode reject, with a pristine positive control. They include every payload and dependency missing, altered, or symlinked; root and ancestor aliases; missing and changed pins; duplicate JSON keys; narrower or missing scope; source-bound and expected-result changes; wrong executable origin; missing arguments; and a false mathematical obligation. Semantic mutations are re-manifested and re-pinned inside their temporary copies, so those tests reach semantic gates rather than only stale hashes.

The separate independent suite rejects 67 controls per mode. It covers every payload missing, same-size altered, symlinked, or replaced by a directory; every dependency missing, same-size altered, or symlinked; extra file/directory/dangling-symlink inventories; root, ancestor, dependency, and pin-parent symlinks; missing/changed/internal pins; missing arguments; and an injected false mathematical gate in the independent program. The false gate fails in every interpreter mode, producing no success artifact. No acceptance gate uses Python assert. All mutations occur only in disposable copies.

All final original and copied inputs are rehashed after the runs. Authored terminal receipts, replay identities, and the audit's own validation identities are separately recorded. The audit has its own external manifest and seal; those identities fix this report and the exact scripts, copied dependencies, outputs, and metadata reviewed here.

The checks certify this static snapshot and the tested failure modes. They do not certify resistance to concurrent hostile filesystem races, every malformed input representation, or simultaneous replacement of all trusted anchors. Neither they nor the imported historical Folkman result settle the general conjecture.

## Final integration limits

The all-size structural results and imported historical k=4 order lower bound are accepted with their stated hypotheses. The exact signed core constraints are still not proved satisfiable for every odd-hole-free graph. The eight-core boundary is narrowed but not excluded. A clique cutset's traces are still not proved compatible. In particular, use n>=19 and |X|>=8 for any k=4 counterexample, but use 22/24 cutset bounds only after explicitly imposing induced-minimality. Do not turn necessary equality forms into existence statements, import the unchecked general Folkman attribution as audited, claim the external enumeration was reproduced, or revive the superseded exponential-size assessment.
