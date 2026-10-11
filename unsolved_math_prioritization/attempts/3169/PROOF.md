# Full written counterexample proof: geodesic cycles and Tutte's theorem

Record 3169 / OPG-500. Audit date: 2026-10-11 UTC.

This is an AI-assisted, unrefereed internal AI audit of a prior public candidate. It is not human peer review or formal proof-assistant certification. The source construction and the C09/C10 arguments are credited to vibemathing at commit a41fe59b4535851ea55f6e868e938b9aaf81e924. No new discovery, novelty or priority is claimed. This prose edition is not a computational reproduction package.

For the graph H below, every strictly positive real edge-length assignment admits a nonperipheral geodesic cycle, including all shortest-path ties. OPG-500 is answered negatively at the locally accepted written-proof level.

This document and AUDIT.md are complementary parts of one completed audit, partitioned for reading. They are not two independent audits. Sections 2–7 retain the complete accepted mathematical reconstruction, including finite-graph definitions, the all-ties proof, extraction, the separate C09 route, and formalization limits. Original section numbers are retained; the source statement and provenance are in AUDIT.md §1. Historical computational claims in these sections describe the completed audit; their data and programs are not distributed here.

## 2. Graph and every combinatorial hypothesis

Let B = {0,1,2,3} induce a complete graph. For each i in B, add y_i = 7−i, adjacent precisely to B minus {i}. There are no edges between the y_i. Thus the graph H has 8 vertices and 18 edges, in the fixed order

01, 02, 03, 04, 05, 06, 12, 13, 14, 15, 17, 23, 24, 26, 27, 35, 36, 37.

The labels matter: y_0=7, y_1=6, y_2=5, y_3=4. No vector from a different apex labeling is silently reused.

**3-connectivity.** After deleting at most two vertices, at least two core vertices survive and form a connected clique. Every surviving apex originally had three core neighbors, so it still has at least one surviving core neighbor. Therefore the remainder is connected. Since H has eight vertices, this proves 3-connectivity. The exact check independently confirms all 1+8+28=37 such deletions.

**Induced cycles.** Every cycle has at least two core vertices, because the apices are independent. A cycle with exactly two core vertices and length greater than three must alternate between these vertices and two apices, and the edge between the core vertices is a chord. With at least three core vertices, any cycle longer than a triangle has two nonconsecutive core vertices, producing a chord. Indeed three vertices in a cycle of length at least four cannot be pairwise consecutive. Thus every induced cycle is a triangle.

There are four core triangles B minus {i}. Deleting one isolates y_i, while the remaining core vertex i and the other three apices form a star. These four triangles are separating.

Every remaining triangle is {y_i,a,b}, with a,b distinct in B minus {i}. Deleting it leaves two adjacent core vertices. Each remaining apex loses at most two of its three core neighbors, and therefore attaches to that surviving pair. Its complement is connected. There are 4 times 3 = 12 such triangles, and these are exactly the peripheral cycles.

Two independent complete cycle enumerations agree: ordered vertex permutations, canonicalized up to rotation and reversal; and every one of the 2^18 edge subsets, recognizing nonempty connected 2-regular supports. They give 239 simple cycles, with length counts 16, 33, 60, 76, 48 and 6 for lengths 3 through 8. The cycle-space rank is 18−8+1=11, also checked by exact binary elimination.

## 3. Metric lemmas, without genericity or hidden effectiveness assumptions

Fix an arbitrary vector w in (0,infinity)^18. All paths below are ordinary finite graph paths and their lengths are sums of edge lengths. Between any two vertices a shortest path exists: there are finitely many simple paths, and removing a repeated-vertex closed subwalk strictly shortens a walk because all edge lengths are positive. A subpath of a shortest path is shortest between its endpoints, since replacing it by a shorter path would give a shorter walk, hence a no-longer simple path.

Call an edge uv **tight** when w(uv)=d_H(u,v), and let T be the spanning subgraph of all tight edges.

**Lemma 1: T is connected and preserves all vertex distances.** Every edge on a shortest path is tight: a strictly shorter path between the endpoints of a nontight edge could replace that edge and shorten the whole route. Hence for every vertex pair some shortest H-path lies entirely in T. The inclusion of path families gives d_H ≤ d_T, and the exhibited shortest H-path gives d_T ≤ d_H. Thus d_T=d_H.

**Lemma 2: a nontight edge forces a geodesic complementary-path cycle.** Let uv be nontight and let P be any shortest u-v path. Its length is strictly less than w(uv), so it does not contain uv. It is simple and all its edges are tight. The union P∪uv is a simple cycle. Every vertex of that cycle belongs to P. For any two such vertices, their P-subpath is globally shortest and is one of the two cycle arcs. Thus the cycle is geodesic, even with arbitrarily many shortest-path ties. No claim that all geodesic-cycle edges are tight is made or needed.

**Lemma 3: strict shortcut splitting.** In any finite positive-length graph, let a cycle C fail geodesicity. Then some vertices x,y of C have a simple path P of length less than their intrinsic C-distance, that distance being the smaller of the two cycle-arc lengths. Split P at its successive visits to C. If every segment between successive visits had length at least the intrinsic C-distance between its endpoints, summing and using the triangle inequality for the intrinsic cycle metric would imply length(P) ≥ d_C(x,y), a contradiction. Therefore a segment Q has length less than both C-arcs A,B between its endpoints, and its internal vertices lie outside C. It cannot be an edge of C, since that edge cannot be shorter than the intrinsic C-distance of its endpoints. Thus A∪Q and B∪Q are simple cycles and

C = (A∪Q) XOR (B∪Q)

as edge incidence vectors over F_2. Both children have strictly smaller length than C, because length(Q)<length(B) and length(Q)<length(A), respectively.

**Lemma 4: geodesic cycles span the cycle space.** There are finitely many simple cycles. Induct in their finite order by length, grouping equal lengths rather than assuming that real numbers are well ordered. If a cycle is geodesic, it is already a generator. Otherwise Lemma 3 expresses it as a sum of two strictly shorter cycles, each already in the geodesic span. This proves the assertion. The same argument works inside T. By Lemma 1 every T-geodesic cycle is H-geodesic.

For completeness, the dimension of the binary cycle space of a connected finite graph is m−n+1. A spanning tree has n−1 edges. Each remaining edge supplies a fundamental cycle with a distinct non-tree edge coordinate; these cycles are independent. Cancelling those coordinates from an arbitrary even edge set leaves an even edge set in a tree, which is empty by successively removing leaves. Thus these fundamental cycles form a basis. Simple cycles span all even edge sets by the same elementary decomposition, so this agrees with the cycle space used above.

## 4. Universal all-ties contradiction

Suppose, for contradiction, that all H-geodesic cycles are peripheral. Form T as in Lemma 1. Write F=T[B], let f be its number of edges, and let N_i be the neighbors of y_i in T. Put n_i=|N_i|, and let c_i and e_i be the number of connected components and edges, respectively, in F[N_i].

**F has no triangle.** If three core edges are tight, each vertex pair on that triangle has its direct edge as a shortest path. That core triangle is geodesic, yet it is nonperipheral by §2. This contradicts the supposition.

**N_i dominates F−i.** Take any j≠i. If y_i j is tight then j belongs to N_i. Otherwise Lemma 2 supplies a geodesic cycle consisting of y_i j and a shortest complementary path. Under the supposition this cycle must be one of the twelve peripheral triangles. Its third vertex k lies in N_i, and the edge jk is tight and belongs to F. Thus either j is in N_i or it has an F−i neighbor in N_i. In particular N_i is nonempty and meets every connected component of F−i.

Each F[N_i] is a triangle-free graph on at most three vertices, hence is a forest, so e_i=n_i−c_i. Because T is connected on eight vertices,

beta(T) = f + sum_i n_i − 7.

Its triangles are exactly the apex triangles indexed by edges of F[N_i]. There is no core triangle and no triangle with two apices. Consequently its triangle count is sum_i e_i. By Lemma 4 and the supposition, its cycle space is generated by some of its peripheral triangles. A generating family cannot have fewer members than the dimension. Without assuming independence, we obtain

f + sum_i n_i − 7 ≤ sum_i (n_i−c_i),

or equivalently

f + sum_i c_i − 7 ≤ 0.                                    (1)

A triangle-free graph on four vertices is either a forest or the four-cycle: any cycle has length four, and any additional edge on the same four vertices creates a triangle.

If F is a four-cycle, f=4 and each c_i≥1, so the left side of (1) is at least 1, a contradiction.

If F is a forest, let c=cc(F)=4−f and d_i=deg_F(i). Deleting vertex i changes the component count to c+d_i−1. This formula includes isolated vertices: deleting one removes its component. Since N_i meets every component of F−i, and no edge of F[N_i] can join different components of F−i,

c_i ≥ c+d_i−1.

Summing and using sum_i d_i=2f gives

f + sum_i c_i − 7 ≥ f+4c+2f−4−7
                         = 3f+4(4−f)−11
                         = 5−f ≥ 2,

because a forest on four vertices has f≤3. This is again a contradiction.

These cases exhaust all F. The originally arbitrary strictly positive real assignment therefore always has a nonperipheral geodesic cycle. Ties have not been perturbed or discarded at any step. This completes the theorem.

## 5. Constructive witness extraction and its scope

For a fixed length vector compute the distances, T, F and N_i.

1. If F contains a triangle, return that core triangle. Its tight edges prove geodesicity; deleting it isolates the corresponding apex.
2. Otherwise, if N_i fails to dominate a vertex j of F−i, return y_i j plus a shortest complementary path. The edge y_i j is nontight. This cycle cannot be a triangle, because its middle vertex would supply the missing neighbor in N_i adjacent to j in F. It therefore has length at least four, is chorded in H, and is nonperipheral.
3. Otherwise let W be the binary span of all triangles in T. The rank inequality just proved shows beta(T)>number of T-triangles≥dim(W). Thus at least one simple T-cycle lies outside W; otherwise all simple cycles would span only W. Select one of minimum weighted length from the finite nonempty family of outside cycles. If it were not T-geodesic, Lemma 3 would split it into two strictly shorter T-cycles. Since W is closed under XOR, at least one child would remain outside W, contradicting minimality. The selected cycle is therefore T-geodesic, hence H-geodesic, and it is not a triangle because every T-triangle belongs to W. By §2 it is nonperipheral.

This is a mathematical existence construction over arbitrary real weights. It does not pretend to decide comparison of arbitrary oracle-free real representations. The executable extractor accepts exact positive rational numbers only. A descending implementation terminates because it stays in the finite family of at most 239 simple H-cycles and strictly decreases length, not because all positive real numbers form a well order.

## 6. Separate audit of C09's perturbation route

C09 offers a second sound mathematical route, but it shares the geodesic-generation lemma with C10 and is not a wholly separate mathematical trust domain.

For the finite family of pairs of distinct simple paths with the same ordered endpoints, let a be the difference of their 0/1 edge incidence vectors. This vector is nonzero, because a simple path's edge set and ordered endpoints determine its traversal. Let b_j=2^j in the fixed edge order. The highest nonzero coefficient of a has magnitude one and its contribution dominates the sum of all smaller powers; hence a·b is nonzero. Choose epsilon>0 smaller than every |a·w|/(2|a·b|) whose numerator is nonzero. There are finitely many positive bounds, so such epsilon exists; if there are none, choose any epsilon>0. Then w'=w+epsilon b is positive, every formerly strict path comparison retains its sign, and every former tie becomes unequal. In particular shortest paths become unique.

Every originally nongeodesic cycle had a path strictly shorter than both arcs, and those strict comparisons survive. Thus no new geodesic cycle is created. If all geodesic cycles were peripheral before perturbation, they still would be afterward.

Under unique shortest paths, a nontight edge can belong to at most one geodesic cycle: the complementary endpoint arc of any such cycle must be the unique shortest endpoint path. Geodesic generation requires at least 11 distinct geodesic cycles. Since only 12 cycles are peripheral, at most one peripheral triangle is missing. Each core edge belongs to precisely two peripheral triangles, so all core edges are tight except possibly the edge of that sole missing triangle. A single core edge is contained in only two of the four core triangles. Some core triangle therefore has all three edges tight, is geodesic and is nonperipheral, a contradiction.

The independently reconstructed CNF has 18 variables and 76 clauses: 66 pairwise clauses forcing at most one missing peripheral triangle, six implications from both incident geodesic triangles to core-edge tightness, and four clauses forbidding a fully tight core triangle. Exhaustive checks of all 262,144 Boolean assignments find zero satisfying assignments; the reduced 832 eligible face/tight assignments each retain a concrete violated clause. This does not replace the real-weight perturbation proof above.

The uniqueness requirement must not be omitted. Assign length 3 to core edges and 1 to spokes. A core edge then has length 3 but distance 2 and belongs to two geodesic peripheral triangles. Exactly 22 cycles are geodesic: 12 peripheral triangles and 10 bad cycles, comprising six four-cycles and four six-cycles. All four core triangles are nongeodesic. This also disproves the tempting weaker test that merely eliminating the core triangles would suffice.

## 7. Definition clarification and source-fragment limits

For a finite graph realized by closed positive-length intervals, vertex-pair geodesicity of a cycle implies all-points geodesicity. Given any two points x,y on the cycle, take an ambient shortest path, subdividing at x,y if needed. A simple shortest path exists in this finite subdivided graph. Each excursion outside the cycle has endpoints at original cycle vertices. Replace it by a no-longer cycle arc, using vertex-pair geodesicity. This yields a cycle walk from x to y no longer than the ambient shortest path. Removing backtracking gives a cycle arc no longer than that path, while the ambient distance cannot exceed any cycle arc. Hence equality holds. The reverse implication follows by restricting to vertices.

Therefore describing the all-points condition as “stronger” is misleading for this finite target. No equivalence for arbitrary infinite topological cycles is asserted, and none is needed.

C11's prose correctly distinguishes a propositional contradiction and abstract minimum-outside-span lemmas from the actual graph/metric theorem. C12 correctly removes a supplied-minimum hypothesis by a finite-list argument, while retaining completeness, strict decrease, span closure and graph faithfulness as separate obligations. The written proof here supplies those mathematical bridges, and the 4,770 symbolic external-path split rows verify their finite graph incidence/length identities for H. This does **not** establish that the source author's Lean terms elaborate, their axiom closure, any source-specific kernel admission, or any unrelated finite-linear-characterization claim. Those formal/tooling questions remain outside this acceptance.

Further source inspection and historical finite-check coverage appear in AUDIT.md.
