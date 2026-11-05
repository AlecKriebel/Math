Editorial note: This is the complete authored text. Only references to undistributed operational files, their identities, locations and replay directions have been replaced. All mathematical arguments, exact finite counts, corrections and limitations are retained. The public manifest identifies the actual distributed files.

# Linear signed-core projection and chordal realization of every bounded-degree tree

## Scope and status

This is the complementary component of the fifth and final substantive pass for problem 3251 / ordered row 1753. It is a partial structural result and an explicit correction of one complexity statement in the fourth pass. The unrestricted claim that every odd-hole-free graph with an edge has a two-coloring avoiding monochromatic maximum-cardinality cliques remains unresolved. No novelty or minimality claim is made. No sixth pass, queue change, remote action, or publication is part of this packet.

A finite simple graph G has clique number k>=3 and original maximum-clique family M. Put X={v: v occurs in at least three members of M}, and fix any prescribed set P containing X. All incidences below are counted in this original family, never recomputed from an induced graph or a residual formula. Write m=|M| and L=sum(Q in M)|Q|. The accepted fourth-pass exact-extension and signed-tree theorems, pinned together with their acceptance report, are the mathematical dependency. The same arguments work for an explicitly supplied finite family of distinct sets of sizes at least three when each vertex outside P occurs in at most two sets.

## 1. The full low-incidence dual multigraph

Construct D_P with one node for each original clique Q in M. For every vertex z outside P:

- If z has incidence two, make one edge joining its two distinct containing clique nodes and label this edge by z.
- If z has incidence one, mark its unique containing node.
- If z has incidence zero, do nothing.

Edges with the same ends are retained as distinct parallel edges. There are no loops, since the original sets contain vertices without repetition. A tree component means a connected component with exactly one fewer edges than nodes, including a single isolated node with no edges. Parallel edges therefore prevent a component from being a tree. A component is unmarked when none of its nodes is marked.

The fourth-pass definition of a P-tree is a nonempty subfamily F in which each outside-P vertex occurring in F occurs in exactly two selected members, and the corresponding multigraph on F is a tree.

**Theorem 1 (component closure).** The P-trees are exactly the node sets of the unmarked tree components of D_P.

**Proof.** Let F be a P-tree. An outside-P vertex of incidence one cannot occur in a selected clique, because it cannot have two selected occurrences. Thus F contains no marked node. If a selected node Q is incident to a dual edge labeled z, the other containing clique Q' must also be selected: z already occurs in Q and needs two selected occurrences; globally it has precisely these two. Hence F is closed under every edge of D_P. It is therefore a union of entire connected components. Its selected multigraph is connected, so this union is exactly one component. The selected and full component edge sets coincide. The P-tree condition says this component is a tree.

Conversely let C be an unmarked tree component. Every outside-P vertex in one of its cliques has incidence two (incidence one would mark that clique), and its other containing clique belongs to C because the dual edge joins it. Hence each such vertex occurs exactly twice in C. These occurrences induce exactly the edges of C, which is a tree. Thus C is a P-tree. QED.

In particular, there are at most m P-trees. The one-node case is exactly an original maximum clique entirely contained in P. This theorem does not require odd-hole-freeness, connectedness of G, uniform rank, or that P equal X.

## 2. Exact linear-size projection onto P

For each unmarked tree component C choose either bipartition A_C,B_C. Let S_C be the union of Q intersect P over Q in A_C, and T_C the analogous union over B_C. If S_C and T_C intersect, discard this component: its two signed matching prescriptions require the same prescribed vertex to have opposite colors. Otherwise associate the two complementary clauses

    (OR over x in S_C of x) OR (OR over x in T_C of not x),
    (OR over x in S_C of not x) OR (OR over x in T_C of x).

Here x is the Boolean color of its vertex, so the first clause forbids S_C all 0 and T_C all 1, and the second forbids the complementary pattern. The disjunction over an empty set is false. For a one-node component, one side is empty and these are exactly the two nonmonochromatic-clique clauses. All unions remove repeated vertices within a side.

**Theorem 2 (exact compression).** A coloring alpha of P extends to a division of G if and only if it satisfies the conjunction Phi_P of these clause pairs. The formula has at most 2m clauses and at most 2L total literal occurrences. It can be constructed in O(n+L) time and space from the explicit original clique-incidence list, using ordinary integer-indexed graph and incidence representations.

**Proof.** The accepted signed-tree theorem says that alpha fails exactly when it matches a signed P-tree. By Theorem 1, the underlying tree must be one of the unmarked tree components. A component whose two boundary unions overlap cannot match any alpha. For any other component the two possible bipartition orientations give exactly the two forbidden patterns above. This proves equivalence.

Different connected components have disjoint clique-node sets. For a component C, |S_C|+|T_C| is at most the number of P incidences in its clique nodes. Summing this quantity over the retained components is at most L; two clauses per component therefore have total length at most 2L. There are at most m components. To construct the formula, collect vertex incidences, add dual edges and marks, and find connected components with their edge counts. Test treehood by edge count and connectedness; bipartition each retained tree by traversal. Scan P incidences in those nodes and use per-vertex component-index stamps and side bits to form unions and detect overlap without rescanning all P for each component. All these operations take O(n+L), since m<=L for nonempty sets. Isolated graph vertices can be included in the O(n) term. QED.

This is an explicit formula on original prescribed vertices, not just an implicit separation oracle. A failed coloring can be certified by its violated component and orientation; the full component itself is the accepted signed-tree certificate. Any propagation certificate extracted by the fourth-pass procedure is necessarily one of these complete components, by Theorem 1. It is not merely some proper subtree.

The compression does not solve the unrestricted conjecture: satisfiability of the resulting signed CNF is still to be established for the special formulas arising from odd-hole-free graphs. The known O(2^|X|(n+L)) input-list decision bound remains valid and can now be implemented by evaluating a once-built formula rather than rerunning propagation for every core assignment. Outputting a completion from a successful assignment still uses the accepted constructive extension theorem. Maximum-clique enumeration from a graph encoding is not asserted polynomial.

**Corollary 3 (a universally extendible class).** If every dual component is marked, is not a tree, or has intersecting bipartition boundary unions, every coloring of P extends. In particular the graph is divisible. The statement applies without odd-hole-freeness.

For an unmarked tree component of t nodes in a k-uniform family, its number of prescribed incidences, with multiplicity, is exactly

    kt - 2(t-1) = (k-2)t+2.

This is an incidence identity, not necessarily the number of distinct prescribed vertices. It follows by subtracting the two incidences of each of the t-1 outside-P edge vertices. In the nonuniform case replace kt by the sum of the node-set sizes.

## 3. Correction to the fourth-pass complexity statement

The fourth-pass the complete proof, Section 3, says of the signed-core tree constraint system: "It can be exponentially large if explicitly enumerated". Under that proof's own standing assumptions P contains X and each outside-P vertex has original incidence at most two, this statement is incorrect for its defined tree system: Theorem 1 proves at most m underlying trees, and Theorem 2 proves a 2m-clause, 2L-literal bound. The acceptance report's corresponding description of an exponentially large system is superseded on this point.

The fourth-pass exact propagation theorem, obstruction characterization, extraction bound, and mathematical soundness and completeness of the signed clauses remain intact. No change to their frozen files is made. General families of subtrees of a graph can indeed be exponentially numerous, but the requirement of two selected occurrences for EVERY outside-P vertex closes the selected set under all dual edges, excluding those proper subtrees. This correction is expressed as an all-size proof, not a conclusion from bounded enumeration.

the complete authored correction isolates the exact corrected claim and dependency identities for attachment beside the unchanged original. The verifier independently enumerates selected subfamilies on a finite exhaustive universe and compares the original P-tree definition with the complete-component characterization, in addition to checking existential color extension.

## 4. Every bounded-degree tree is realizable in a connected chordal graph

**Theorem 4 (realization).** Fix k>=3 and any finite nonempty tree T with t nodes and maximum degree at most k. There is a connected chordal graph G(T,k) with clique number k whose exact high-incidence set X has

    c = (k-2)t+2

vertices. Its dual graph D_X has T as its unique unmarked component; every other component is a marked isolated node. The two signed assignments furnished by T are exactly the nonextendible colorings of X. Thus precisely 2^c-2 core colorings extend, the whole graph is divisible, and its obstruction component can have arbitrary size and branching allowed by degree k.

**Construction.** For every tree edge ab create a distinct vertex z_ab. At each tree node a create a disjoint set C_a of k-deg_T(a) fresh vertices. Make the base bag Q_a=C_a union {z_ab:ab incident with a} a k-clique. For every x in the disjoint union C of these C_a, add two further support bags, each consisting of x and its own k-1 fresh private vertices. Distinct support bags have disjoint private sets. Join two graph vertices exactly when they occur together in one of these bags.

**Exact clique family and chordality.** Form a bag tree H from T by adding, at node a, two leaf nodes for the two support bags belonging to each x in C_a. Each adjacent pair of bags in H intersects in a single vertex. For each graph vertex, its containing bag nodes form a connected subtree of H: the two endpoints of one base edge for z_ab; a base node and its two support leaves for x; or a single support node for a private vertex.

Here is a direct elimination argument. Take a leaf bag B of the current bag tree with neighbor B'. Every vertex in B minus B' occurs in no other remaining bag: connectedness of its bag occurrences would otherwise force it into B'. Its remaining neighbors therefore lie in B, a clique. Eliminate B minus B' in any order, then delete leaf B from the bag tree. Repeat until the final bag, whose vertices form a clique. The same connected-occurrence property persists at each step. This is a perfect elimination order, so an induced cycle of length at least four is impossible: its earliest removed vertex would have adjacent later cycle-neighbors.

This argument also proves that every graph clique is contained in a displayed bag. At the first eliminated vertex of a nonempty clique, all its other vertices lie in that vertex's elimination bag, which is a subset of an original displayed bag. The displayed bags are distinct and each has k vertices; thus they are exactly the maximum cliques and the graph has clique number k. Since all bags are cliques of size at least three and adjacent bags meet, their union graph is connected.

**Incidences and projection.** Each x in C belongs to precisely its base bag and two support bags, so has original incidence three. Each z_ab belongs to its two base bags and has incidence two. Each support-private vertex has incidence one. Therefore X=C exactly. In D_X each base edge yields its T edge; each support bag is isolated and marked by its private vertices. No other dual edges or marks occur. Hence the unique unmarked component is T. Its boundary sets are disjoint unions of the mutually disjoint C_a on the two bipartition sides; their union is all X. The sole complementary pair of clauses forbids exactly two full assignments on X. Theorems 1 and 2 now prove the count 2^c-2.

For completeness, the graph has a direct division. Root the tree of bags H at any node. Color the root bag using both colors. When a child bag is visited, its intersection with earlier bags is its single separator vertex; color one of the other k-1 vertices oppositely and the remaining new vertices arbitrarily. Connected occurrences ensure that these are precisely its new vertices, so this extends consistently and makes each bag bichromatic. All maximum cliques are bags. Thus global divisibility does not depend only on a finite computation or an inference from the core count.

Finally, sum_a deg_T(a)=2(t-1) gives c=kt-2(t-1). The graph's number of vertices is t-1+(2k-1)c, its number of maximum cliques is t+2c, and its number of edges is (t+2c) binom(k,2): distinct bags intersect in at most one vertex, so no graph edge is counted twice. Its induced core graph is the disjoint union of the cliques C_a (empty C_a omitted).

For t>=2 the core clique number is k-1, attained at each tree leaf. The two bad core assignments monochromatically color these leaf cliques, so they are not divisions of the core at its own clique number. This realization therefore does not strengthen the fourth-pass counterexample to arbitrary core-division extension; it establishes arbitrary obstruction geometry inside connected chordal graphs. One-node T is the ordinary nonmonochromatic K_k constraint. Odd-hole-freeness by itself cannot impose a constant bound on obstruction-component order or path length.

## 5. Bounded verification and integrity boundary

The exact finite universes, counts, and stream hashes are fixed in the mandatory scope record and the exact expected-results record. The exhaustive set-family and graph universe comprises 1,078 rank-tagged uniform families on at most five vertices (90,569 eligible partial colorings), 37 nonuniform families on at most four vertices (1,891 eligible partial colorings), and all 1,100 labelled graphs on at most five vertices, of which 660 have clique number at least three (149,013 eligible partial colorings). Before the coloring checks, every selected subfamily is compared with the component characterization for every eligible prescribed set. Nineteen specifically constructed tree-realization graphs, with orders up to 118, contribute 79,016 exact-core colorings, of which exactly 38 fail. These are specific fixtures, not an enumeration of all graphs or all trees of those orders. A separate general Davis-Putnam Boolean elimination independently obtains their exact core projection. Successful realization colorings receive an explicit full-graph witness checked against the reconstructed maximum cliques. The checks compare the original selected-subfamily tree definition to the dual-component criterion, compare compressed clauses with an independent exhaustive whole-coloring oracle, check returned component certificates, and include parallel-edge, marked-component, intersecting-boundary, singleton, cycle, and deliberately out-of-scope cases. Realization fixtures reconstruct all maximum cliques from graph adjacency independently of the bags and check complete elimination orders and exact original incidences. The tested fixtures do not substitute for the all-size proofs.

The mandatory verifier arguments are the source-root argument, the external-pin argument, the external-pin-digest argument and the dependency-root argument. The external pin fixes the manifest and complete packet inventory; the verifier checks nonsymlink file types and path ancestors, exact bytes and SHA-256 values, duplicate JSON keys, and fixed semantic scope. No mathematical or integrity gate uses Python assert. Normal Python, -O and -OO must agree. Disposable-copy controls test declared hostile mutations and leave the frozen sources unchanged.

This is static snapshot integrity with an externally retained trust anchor. It does not claim security against concurrent hostile filesystem races, coordinated replacement of all anchors, or exhaustive malformed-input attacks. The unrestricted target remains unresolved.
