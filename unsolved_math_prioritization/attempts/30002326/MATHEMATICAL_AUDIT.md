# Independent audit of the all-order homometric flower bound

Problem 30002326 / OWR-12481-016. 10 October 2026.

## Verdict and artifact identity

**ACCEPTED AS A PARTIAL RESULT.** No mathematical correction is required to the submitted report. Its exact all-order construction, cone calculation, flower localization and graph-uniform flower obstruction are valid under the explicitly stated operational min–max convention. Neither direction of the original sublinearity question is resolved. Novelty and exhaustive current literature status are not certified.

The audited manuscript, *An all-order flower bound for disjoint homometric sets*, is exactly 16,408 bytes with SHA-256 `08315917ceb034e6041b684903c971fb5b0d1b6004dd21fb558c7012daeb764c`.

Provenance limitation: the original manuscript was recovered and matches its independently recorded byte count and SHA-256 exactly. The original full working bundle and its complete historical verification record were not restored. Six previously inspected public PDFs were recovered with matching identities, and the BKNS arXiv v2 source was independently retrieved. The independent audit has a separate verified inventory and fresh diagnostic records. Missing historical files are not represented as freshly verified.

This is an independent internal AI mathematical and source-credit audit. The AI-assisted note and audit are unrefereed; no external human peer review, journal acceptance of this audit, or formal proof-assistant certification is claimed. The published external theorems are credited and relied upon within their stated scope. This edition retains every substantive audit section below; its preparation adds no source-inspection or mathematical-replay claim.

## 1. Exact scope

For connected finite simple unweighted G, let h(G) be the maximum common size of disjoint A,B with identical multisets of ambient distances between unordered distinct pairs. Define h(n) as the minimum of h(G) over connected graphs of order n. The equal sizes, disjointness, ambient metric and distance multiplicities are retained throughout.

Axenovich–Özkahya explicitly define a minimum of maxima. Connectedness comes from the original connected-graph question. The isolated Oberwolfach sentence omits its size clause. The report does not presume equivalence with the differently quantified maximum k such that every connected n-vertex graph has a pair of exactly size k. Its caution is appropriate. Ordered pairs with diagonal entries give equivalent distance information when the equal cardinalities are kept.

An affirmative answer to h(n)=o(n) would require a vanishing upper ratio for every sufficiently large integer n. A negative answer would require a fixed positive lower ratio for the extremal function along an unbounded sequence. The artifact only proves a linear-leading-term upper bound and an obstruction inside its own construction class.

## 2. Flower geometry and the threshold-four localization

For F(H,m), H is nonempty, the path has vertices p_0,...,p_{m-1}, m≥2, and p_0 is adjacent to every core vertex. The exact ambient distances are

- d(p_i,p_j)=|i−j|;
- d(u,p_i)=i+1 for u in H;
- d(u,v)=1 for core edges and 2 for core nonedges.

A path excursion into H can return only through p_0, so it never shortens a tail distance. The core formula works for disconnected H as well. Thus C=H∪{p_0,p_1} is isometric with diameter at most two. For equal-size subsets of C, induced edge count determines the multiplicity of distance one, while the remaining pairs have distance two. Hence homometry is equivalent to equal induced edge counts in C. This proves h(F)≥t(C). Any u in H extends the tail to an isometric path on m+1 vertices, proving h(F)≥floor((m+1)/2).

For the upper bound take a disjoint homometric pair A,B of common size at least four. If no used tail vertex is beyond p_1, their union lies in C. Otherwise put the largest used tail vertex p_j, j≥2, in A. If A also met H, it would contain distance j+1, while B has no distance exceeding j. Therefore A lies entirely on the path.

Its maximal distance is at least three and occurs once, between its two extremes. If B meets H, it also meets the tail, since core distances are at most two. If p_i is B's largest tail vertex, its maximal distance is i+1≥3. Exactly |B∩H| pairs have this distance: p_i with each core vertex. No path–path or core–core pair can contribute. Equality of multiplicities therefore forces |B∩H|=1. Thus A∪B lies in the tail plus a single core vertex.

Consequently, writing L=max(t(C),floor((m+1)/2)),

L≤h(F)≤max(3,L).

The equality h(F)=L follows when L≥3, and therefore for m≥5. This argument fully accounts for disconnected cores, root usage, and largest-distance multiplicity.

The threshold is sharp for this localization statement. For H=P_3 and m=3, the whole core and whole tail are homometric triples, each with distances 1,1,2, but their union fits neither localization. Here h(F)=3 and L=2. The earlier Axenovich–Özkahya arXiv version states threshold two in Lemma 17; the revised author version already states threshold four in Lemma 12. The report correctly acknowledges that prior revision. [Earlier version](https://arxiv.org/abs/1203.1158), [revised author version](https://web.cs.hacettepe.edu.tr/~ozkahya/pub/homsets.pdf).

## 3. Exact cone twins: both root states and j=0

Let C be the cone with universal root r over odd cliques Q_0,...,Q_k, where a_0=1, k≥2 and a_j>4(1+Σ_{i<j}a_i(a_i+1)). Set q=Σ_{i=1}^k a_i.

The lower bound t(C)≥(q−k)/2 follows by splitting a_i−1 vertices of each Q_i, i≥1, equally into two sets and omitting r and Q_0. Equal clique counts give equal induced edge counts.

For any equal-order, equal-edge-count disjoint pair, let x_i,y_i be its counts in Q_i, z_i=x_i+y_i, d_i=x_i−y_i, u_i=a_i−z_i. The number U of unused vertices is q+2−2h. The desired upper bound is equivalent to U≥k+2.

### Root unused

The equal-order equation is Σd_i=0. Twice the edge difference is Σd_i(z_i−1), so Σd_i z_i=0. If all d_i=0, every z_i is even, leaving an omission in each of k+1 odd cliques and one at the root.

Otherwise choose the largest index j with d_j≠0 and put T=Σ_{i<j}a_i(a_i+1). Cancellation gives

|d_j|z_j≤Σ_{i<j}|d_i|z_i≤Σ_{i<j}a_i²≤T,

hence z_j≤T. The case j=0 would force z_0=0, contradicting d_0≠0. Therefore j≥1, and u_j>3T+4. There are j preceding positive clique orders, so T≥2j; in particular u_j≥j+1. The later k−j cliques have equal counts and each omit a vertex. Including the unused root gives U≥(j+1)+(k−j)+1=k+2.

### Root in A

By symmetry this covers either used-root state. Now Σd_i=−1 and Σz_i=2h−1. The root contributes h−1 edges to A. Therefore the exact equation is

0=Σd_i(z_i−1)+2(h−1)=Σ(d_i+1)z_i.

Define e_i=d_i+1, so Σe_i=k. Let j be the largest index with e_j≠0. It exists, and cancellation with |e_i|≤a_i+1 again yields z_j≤T. If j=0, the equation forces z_0=0, hence e_0=1 and Σe_i=1. This is impossible for k≥2.

For j≥1 put S=Σ_{i<j}a_i. Since e_i≤z_i+1,

k=Σ_{i≤j}e_i≤S+T+j+1≤2T+1,

using j≤S and 2S≤T. Thus u_j>3T+4>2T+3≥k+2. No omitted-vertex assertion about the later cliques is needed in this case. The proof is sound even when some e_i are negative.

All cases yield t(C)=(q−k)/2. The k≥2 condition cannot be discarded: for cliques of orders 1 and 13, the root plus six vertices of the large clique and seven other large-clique vertices each span 21 edges. This gives t(C)=7, whereas the improperly extended formula gives 6. Our count-vector tests exercise root unused, root in A and root in B separately.

## 4. All-order construction and exact rounding

The recurrence b_0=1, b_j=5+4Σ_{i<j}b_i(b_i+1) gives positive odd integers, beginning 1,13,741,2,200,029. For S_j=Σ_{i≤j}b_i,

S_j+1≤4S_{j−1}²+5S_{j−1}+6≤6(S_{j−1}+1)².

The first inequality uses Σb_i²≤(Σb_i)². Starting from S_0+1=2, induction gives S_j+1≤12^(2^j)/6.

Choosing k=floor(log_2(log_12 n)) is exactly choosing the integer with 12^(2^k)≤n<12^(2^(k+1)). For n≥20736 it gives k≥2. Put s=floor((n−k+1)/4), q=k+2s and m=n−q. The total of the first k minimal clique orders is at most n/6−2, whereas q>n/2+k/2−3/2. Thus the last clique can be enlarged to make the core order exactly q. Its order is at least b_k, remains odd because q≡k modulo two, and preserves every growth inequality.

Also n≥12^(2^k)≥4k, while q≤(n+k+1)/2. Therefore m≥(n−k−1)/2≥3n/8−1/2≥5. Connectivity and the vertex count q+m=n are immediate. The tail's parameter counts vertices, not edges.

The cone C has root p_0 and singleton clique Q_0={p_1}. Its exact twin number is s. Localization gives h(G_n)=max(s,floor((m+1)/2)). Write n−k=4t+r. For r=0 the two bounds equal t. For r=1 or 2 they are t and t+1. For r=3 both equal t+1. Thus in every residue class

h(G_n)=floor((n−k+3)/4).

Since k=(log log n)/(log 2)+O(1), the claimed natural-logarithm upper bound follows. This is a valid interpolation at every large integer order, not merely a subsequence argument. The asymptotic ratio remains 1/4.

## 5. External theorem, uniformity and structural restrictions

The required external result is exactly Theorem 1.1 of Bollobás–Kittipassorn–Narayanan–Scott: for each ε>0 there is an N depending only on ε such that every graph X with r>N vertices has t(X)≥r/2−εr. Its quantifiers are uniform over graphs; no sparsity, connectedness or randomness hypothesis is imposed. The 2013 author preprint and the independently retrieved arXiv v2 state the same result. The audit checks the statement and its application, not a new independent proof of that long published theorem. The 2015 journal publication metadata agree. [Primary arXiv v2](https://arxiv.org/abs/1312.1680v2), [journal article](https://doi.org/10.1016/j.ejc.2015.03.005).

For fixed ε choose R so that t(X)≥r/2−εr−R/2 for every finite r, absorbing the finitely many small orders. Applying this to C, of order q+2, and combining with the path lower bound yields

h(F(H,m))≥max(q,m)/2−ε(n+2)−R/2−1.

The localization upper bound is at most max(q,m)/2+3. Dividing by n, then letting n grow and ε decrease, proves h(F(H,m))=max(q,m)/2+o(n) uniformly over all cores and splits q+m=n. This includes bounded q and unbalanced tails. Since max(q,m)≥n/2, every such flower has limiting lower ratio at least 1/4; the all-order construction attains that limit. No universal lower bound for all connected graphs follows.

If S is any ambient two-distance subset, encode one distance as edges of an auxiliary graph. Equal-order equal-edge-count twins then have identical distance multisets in G, so h(G)≥|S|/2−o(|S|). Uniformity excludes linearly large such subsets from any hypothetical h(G_n)=o(n) sequence. A closed neighborhood has ambient diameter at most two, implying maximum degree o(n). A geodesic of D edges yields twin sets of size floor((D+1)/2), implying diameter o(n). These are necessary conditions, not existence or nonexistence proofs.

The arbitrary-multicolour extension is posed as a further problem in §5 of the cited paper. It cannot be substituted for the proven two-colour/equal-edge-count result.

## 6. Convention caution and prior credit

In the report's join example, the four-vertex star side and the triangle-plus-isolated-vertex side each have three edges. Their triple edge-count sets are respectively {0,2} and {1,3}, so no homometric triple pair can be chosen inside those specified sides. This does not prove global inequivalence of conventions. Indeed label the star center 0, leaves 1,2,3, triangle 4,5,6 and the remaining vertex 7. In the complete join the disjoint triples {0,1,2} and {3,4,7} both have two edges and are homometric. The submitted caution is exact.

The connected question and kite mechanism are due to Albertson–Pach–Young. The flower localization and odd-clique homometric construction are due to Axenovich–Özkahya, whose Theorem 2 is stated for infinitely many orders and whose proof credits inspiration to Caro–Yuster's equal-edge-count clique example. The stronger-hypothesis cone calculation and all-order interpolation are independently verified here without a priority claim.

Alon's Theorem 2.1 gives c(log n)²/(log log n)² as a connected-graph lower bound. That exact-size lower-bound theorem also implies the operational min–max lower bound, without requiring global equivalence of conventions. It is compatible with this construction. [Alon's paper](https://web.math.princeton.edu/~nalon/PDFS/extremalIII4.pdf), [Albertson–Pach–Young](https://doi.org/10.26493/1855-3974.174.027), [Oberwolfach source](https://doi.org/10.4171/owr/2013/18).

## 7. Fresh independent diagnostics

All computational evidence listed here was rerun after recovery. It supplements the all-order proofs rather than replacing them.

- Every labeled core of order 1–5 and each tail order 2–7 was checked, for 6,594 flowers. A separately written program used Floyd–Warshall ambient distances and direct comparisons of all 59,191,308 nonempty disjoint equal-order pairs. It found 1,492,940 homometric pairs, including 43,240 of order at least four. Every localization, sandwich and asserted equality passed. There were 35 permitted small-exception flowers, including the sharp P_3 example. Optimized ordinary and NDEBUG builds agree exactly.
- Exact integer checks cover all 179,265 n from 20736 through 200000, 1,613 threshold-neighbor cases through threshold index 14, and 588 deterministic random integers up to 9,995 bits. Recurrence bounds were tested through index 15. Actual clique orders, positivity, parity, growth, path size and the rounded formula all passed.
- Six cones, including two with more than 2.2 million vertices, were exhaustively checked in count-vector space for all assignments capable of exceeding the claimed optimum. The root was explicitly unused, in A and in B. All 1,633,610 potentially improving assignments were rejected; lower-bound witnesses were checked. This is exact compressed enumeration, not sampling of vertices. Python normal, -O and -OO receipts agree apart from their recorded mode.
- Control examples show the k=1 cone extension fails and confirm both the specified-pair noninheritance and other global triples in the eight-vertex graph.
- The recovered manuscript's exact bytes match its original external pin. A new externally pinned audit inventory and assertion-independent verifier bind current files, source metadata, accepted scope and check receipts. All 21 mutation controls were rejected in each of normal, -O and -OO Python. They test corruption, closure, schema and unsupported scope promotion. Integrity verification does not itself prove mathematics.

The earlier original-package replays were successful before the interruption, but are not included as fresh reproduced evidence because the original complete package is missing.

## 8. Accepted and excluded claims

Accepted:

1. Exact h(G_n)=floor((n−floor(log_2(log_12 n))+3)/4) for every n≥20736.
2. Threshold-four flower localization; h(F)=L when L≥3, including m≥5.
3. The exact cone formula under k≥2, positive odd clique orders and the stated growth.
4. Uniform flower asymptotics and limiting minimum ratio 1/4 within that class.
5. Necessary degree, diameter and two-distance-subset restrictions.
6. The limited noninheritance example and qualified attribution.

Excluded:

- either a proof or disproof of h(n)=o(n);
- a global positive linear lower bound for all connected graphs;
- localization at sizes two or three without exceptions;
- the cone formula at k=1;
- equivalence or inequivalence of the two global exact-size conventions;
- an unrestricted multicolour theorem;
- novelty or exhaustive current-status certification;
- a claim to have recovered or freshly reverified every file in the lost original package.

The manuscript is mathematically accepted within these explicit partial-result boundaries.
