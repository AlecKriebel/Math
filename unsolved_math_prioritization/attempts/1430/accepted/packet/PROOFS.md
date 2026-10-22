# Authored arguments, reductions, and bounded exact checks

Notation: N=|V(G)|; R(G) is the least positive uniform multiplicity; words contain every vertex. All graphs here are finite, simple, and word-representable unless stated otherwise. Facts explicitly credited to published mathematics are imported theorems, not new results.

## A. Preliminary facts and the parameter

**A1 (heredity).** Deleting all copies of vertices outside S from a representing word leaves a representation of G[S]. In particular R(G[S])<=R(G).

Proof. Every two-letter projection for vertices in S is unchanged.

**A2 (padding).** If w is k-uniform and represents G, prepend the permutation listing its letters in first-occurrence order. The result is a (k+1)-uniform representation of G.

Proof. For an edge whose projection in w is (ab)^k, the added projection is ab, so the new projection is (ab)^(k+1). A nonedge already has a repeated adjacent symbol in its two-letter projection inside w, which remains after the prepend. This proves the claim for all pairs. Repetition pads to any larger multiplicity.

**A3 (maximum copies versus uniform copies).** If an arbitrary representing word has maximum letter count k, it can be made k-uniform without increasing that maximum.

Proof. Prepend the first-occurrence permutation of only the letters whose counts are less than the current maximum k. For an alternating pair, the counts differ by at most one. If both are deficient, their first-occurrence order supplies the correctly ordered two-letter prefix. If just one is deficient, the more frequent letter begins and ends the old alternating projection, and the single added deficient letter preserves alternation. If neither is deficient, nothing changes. Nonalternation of a nonedge survives in the old suffix. Repeat until all deficits vanish. Every step increases some deficient count without exceeding k. Thus minimizing the maximum letter multiplicity gives R(G). Minimizing total length without uniformity is a different question.

A 1-uniform word represents precisely a complete graph. This proves the lower bounds in the small-order examples in STATEMENT_AND_STATUS.md, without computational assumptions.

## B. Approach 1: order dimension and apex extensions

For a poset P, a realizer is a family of linear orders whose common ordered pairs are exactly P; its minimum size is dim(P). The comparability graph joins two distinct elements when one precedes the other in P.

**B1.** The least number of permutations whose concatenation represents a graph H equals the least dimension of a poset having H as its comparability graph.

Proof. In a concatenation of permutations, a pair alternates exactly when it has the same relative order in every permutation. If the relative order changes, a boundary between two consecutive permutations with different orders produces equal consecutive symbols in the projected word. The intersection of the permutation orders is a poset whose comparable pairs are exactly the alternating pairs. Conversely, concatenate any realizer. The same pairwise argument gives precisely its comparability graph.

**B2 (apex identity).** Let G be obtained from H by adjoining a vertex z adjacent to every vertex of H. Then R(G) equals the permutation-representation number in B1.

Proof. In an equal-count two-letter projection, linear alternation is equivalent to cyclic alternation. Therefore rotating a uniform word preserves every edge and nonedge. Rotate a k-uniform representation of G to start at a copy of z. Each cyclic gap following a z contains exactly one occurrence of every other vertex, because that vertex alternates with z. The word has form zP1 zP2 ... zPk with each Pi a permutation of V(H). Removing z gives a permutation representation of H. Conversely insert z before each permutation in such a representation. All old pair relations persist and each old letter alternates with z.

These correspond to the established apex/permutation facts in Halldórsson–Kitaev–Pyatkin. The independent argument above states the cyclic endpoint issue explicitly.

**B3 (imported classical bound and consequence).** Hiraguchi proved dim(P)<=floor(|P|/2) for |P|>=4. See his 1951 paper, printed page 94, statement (7.5), whose scanned page was visually inspected. Consequently every comparability graph G on N>=4 satisfies R(G)<=floor(N/2), by B1. For an apex extension on N>=5, B2 applies the bound to its base of size N-1 and yields R(G)<=floor((N-1)/2). Such graphs cannot defeat the target.

**B4 (calibrating the lower family).** For m>=2 let H have parts A={a1,...,am}, B={b1,...,bm}, with edges ai-bj exactly when i!=j. Add an apex z. The resulting graph has order 2m+1 and R=m.

Construction. For i=1,...,m take the order Li consisting of the a_j with j!=i in increasing index, then bi, then ai, then the b_j with j!=i in increasing index. Concatenate zL1,...,zLm. The intersections of the Li are exactly ai<bj for i!=j: every diagonal ai,bi is reversed by Li and ordered ai<bi by every other Lj; any pair within either part occurs in both relative orders by choosing its two indices. Thus B1–B2 provide an m-uniform representation. The verifier checks this explicit formula for m=2,...,8.

Lower bound for m>=3. Any transitive orientation of the connected bipartite H cannot have a vertex with both an incoming and outgoing edge: a two-edge directed path would force an edge inside one part. Connectivity therefore forces one whole part to be sources and the other sinks. Up to duality, the induced poset is the standard example ai<bj for i!=j. In a realizer, each diagonal incomparable pair must have bi<ai in some order. One linear extension cannot do this for distinct i,j: it would imply bi<ai<bj<aj<bi. Hence at least m orders are necessary. B2 proves the claimed graph lower bound. For m=2 the constructed word gives R<=2, and noncompleteness gives R>=2.

For m=1 the apex graph is a three-vertex path with R=2, not 1. This exception must not be dropped. The proved family attains floor(N/2) at odd N>=5, not automatically at even orders.

**B5 (failed transfer outside comparability).** Orient the path a-b-c as a→b→c. It is semi-transitive, because the missing edge ac prevents a shortcut. Its reachability poset is a total order of dimension 1, whereas R(path)=2. Thus R(G)<=dim(reachability poset of a selected semi-transitive orientation) is false. Taking transitive closure has inserted a nonedge. The general half-order theorem cannot be deduced by that substitution.

## C. Approach 2: stable graph operations

**C1 (disconnected graphs).** If G is the disjoint union of at least two nonempty word-representable graphs Gi, then

R(G)=max(2,R(G1),...,R(Gt)).

Proof. Induced-subgraph restriction gives the component lower bounds; disconnectedness gives the lower bound 2. Pad each component word to k=max(2,R(Gi)) using A2 and concatenate the resulting words. Pairs inside one component retain their projection. A cross-component pair has projection a^k b^k or its reverse, which is nonalternating since k>=2. This proves the upper bound. Omitting the 2 is false for two isolated vertices.

**C2 (true twins).** Adjoining a true twin y of x means yx is an edge and y has exactly the same neighbors as x outside that pair. This operation preserves R.

Proof. In every occurrence of x substitute xy. Projecting onto y and any old vertex other than x gives the old x-projection with x renamed. The xy projection alternates. The old graph is induced, so the upper bound supplied by this substitution matches the lower bound from A1.

**C3 (false twins).** Adjoining a false twin y of x means yx is absent and their other neighborhoods coincide. Its new representation number is max(2,R(G)).

Proof. Pad first to k=max(2,R(G)). Substitute xy at the first k-1 occurrences of x and yx at the last. The xy projection contains yy at the final boundary, so x and y do not alternate. Every other projection again matches the old x-projection. The induced-graph lower bound and noncompleteness give equality.

**C4 (minimal-counterexample restrictions).** If the proposed bound fails for some N>=4, a smallest-order counterexample is connected and twin-free. It is noncomparability and has no apex. It has N>=6 by the explicit witnesses below.

Proof. For components of orders at most 3, R<=2; for any larger proper component, minimality gives its half-order bound. C1 then gives R(G)<=floor(N/2). Twin deletion leaves order N-1>=5, and C2–C3 similarly give a contradiction. B3 excludes comparability graphs. B2 implies that a word-representable graph with an apex has a comparability base, and B3 excludes it. None of these observations ensures that every graph possesses one of the reducible configurations.

## D. Approach 3: compatible nonedge covers

Fix a semi-transitive orientation D of G. Call a uniform word D-compatible if it represents a supergraph of G and the first occurrence of u precedes that of v for each directed edge u→v. Its covered set consists of those nonedges of G that fail to alternate in the word.

**D1.** Concatenating compatible words covers the union of their covered sets while preserving all edges of G.

Proof. On each edge u→v, every block projects to (uv)^k for its own multiplicity k. Their concatenation still alternates. A nonedge covered inside any block keeps that block's equal consecutive pair in its full two-letter projection. This is exactly why orientation compatibility, which is not automatic for arbitrary representations, is needed.

Let c2(D) be the minimum number of D-compatible 2-uniform words whose covered sets include every nonedge. The established star-cover lemma of Halldórsson–Kitaev–Pyatkin supplies one such word covering every nonedge at any chosen vertex. A maximum clique's complement meets all nonedges. Thus c2(D)<=N-omega(G), and D1 gives R(G)<=2c2(D)<=2(N-omega(G)) for a noncomplete graph.

**D2 (dense-clique case).** If omega(G)>=N-floor(N/4)=ceil(3N/4), then R(G)<=floor(N/2). Indeed N-omega(G)<=floor(N/4), so 2(N-omega(G))<=floor(N/2). Hence a smallest counterexample must have a smaller clique.

**D3 (limitation of pure 2-block compression).** The triangular prism on six vertices has R=3. Therefore it cannot be covered with a single compatible 2-word, for any orientation; any successful pure 2-block concatenation has multiplicity at least 4. But the proposed exact upper bound at N=6 is 3. Thus a universal proof which only concatenates whole 2-uniform blocks cannot by itself attain that exact bound at all orders. This does not refute the graph bound or more flexible block constructions.

For the prism, the word 123415263456142536 has three occurrences of every letter and represents triangles 123 and 456 with matching edges 14,25,36. A known theorem of Kitaev's prism paper supplies R>=3. The independent exhaustive check in F also verifies there is no 2-word. These are separate supports for the finite obstruction, not a new prism theorem.

## E. Approach 4: counting and its barrier

Let a=floor(N/2), b=ceil(N/2). There are exactly 2^(ab) labeled bipartite graphs on a fixed bipartition. Each is word-representable, for example because orienting all edges from one part to the other is transitive and linear extensions represent its comparability graph.

If every such graph had R<=k, A2 would give a k-uniform word for each one. The total number of length-kN words is at most N^(kN), and each word defines only one graph. Therefore, whenever

k*N*log2(N) < a*b,

some graph has R>k. This gives a lower bound of asymptotic scale N/(4 log2 N), far short of N/2. It is an existence argument, not an explicit graph construction.

Replacing N^(kN) by the exact uniform-word count W=(kN)!/(k!)^N does not rescue this particular argument at k=floor(N/2). The distinct concatenations of k permutations are uniform words, so W>=(N!)^k. Since N!>=2^(N-1),

log2 W >= k(N-1) >= floor(N/2)*ceil(N/2)=ab

for N>=3. For N=2q the last comparison is q(2q-1)>=q^2; for N=2q+1 it is 2q^2>=q(q+1). Thus the available word count is not smaller than the candidate graph count at the desired threshold. This proves a limitation of raw word counting, not impossibility of a refined counting proof.

The cited September 2026 preprint theorem for bipartite graphs makes the entire class unsuitable for large-order counterexamples to the general half-order bound. A different class or a genuinely stronger structural argument would be required.

## F. Approach 5: finite occurrence constraints and exact small witnesses

For fixed N,k create events (v,i), 1<=i<=k. Seek a total order of these kN events such that (v,1)<...<(v,k). For each pair u,v define A_uv as the chain

(u,1)<(v,1)<(u,2)<(v,2)<...<(u,k)<(v,k),

and A_vu as its reversed starting order. Require A_uv OR A_vu on edges and NOT A_uv AND NOT A_vu on nonedges. This is an exact finite encoding: reading event labels in order yields a representing word, and indexing occurrences in a representing word gives a satisfying order. Replacing nonedge constraints by failure of just one orientation would be unsound.

For k=2, a canonical word introduces labels 0,1,... in first-occurrence order. Every labeled double word becomes one canonical word by renaming its letters, so canonical enumeration preserves graph isomorphism types. The recursive generator appends either any already introduced letter with remaining capacity or the next new letter; hence it visits every canonical word exactly once. The number is (2N)!/(2^N N!), the number of partitions of 2N positions into unlabeled pairs.

SMALL_WITNESSES.json is a collection of authored finite witnesses, not a copied dataset. For each N=1,...,5 it contains exactly every integer edge mask from 0 through 2^(N choose 2)-1. Bit order is lexicographic order on pairs (a,b), 0<=a<b<N. Each entry has length 2N. The verifier checks every pair's alternating projection and separately the equivalent chord-endpoint crossing test. Counts by order are 1,2,8,64,1024, totalling 1,099. The generator used 1,3,15,105,945 canonical words respectively and relabelled them; correctness of the retained witnesses does not depend on trusting that search.

For the six-vertex lower-bound check the verifier actually regenerates all 10,395 canonical double words and cross-checks both edge predicates. Exactly three words in this normalization represent a 3-regular graph, and all three have zero triangles. A triangular prism is 3-regular with two triangles, so no graph isomorphic to it occurs. Its explicit 3-word gives the matching upper bound. The generator's exhaustiveness is justified above; the observed histogram is a bounded computation, with source-level checks retained. It is not a general theorem about untested orders or a proof-assistant certificate.

## Dependencies and exact unresolved step

Imported mathematical results are (i) Hiraguchi's dimension theorem, (ii) the semi-transitive characterization and compatible star-cover lemma, and (iii) credited contemporary bipartite results. The explicit elementary reductions and witnesses can be checked independently of those papers. No source text or PDF is distributed in this packet.

These arguments establish restricted cases and obstructions to five proposed methods. They do not show that every remaining graph has a suitable dimension model, reducible vertex, compatible cover, favorable counting obstruction, or bounded-order representative. Closing one of those gaps is essential before changing the general status from unresolved.
