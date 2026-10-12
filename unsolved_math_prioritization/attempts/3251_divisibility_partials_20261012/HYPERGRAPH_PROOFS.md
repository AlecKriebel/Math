> Edition note: This complete authored text preserves the mathematical arguments and substantive audit findings. Original operational references and identities of material not distributed here have been replaced with descriptive prose. The independent audits are AI mathematical reviews, not human peer review or formal proof verification.

# Maximum-clique hypergraph reductions for OPG-56230

## Scope

Let a **division** of a finite graph G with clique number r>=2 be a red/blue vertex coloring in which every r-clique meets both colors. The target remains the conjecture that every odd-hole-free graph with an edge has a division. This note does not resolve that conjecture and does not assert research novelty. It proves sparse-incidence sufficient conditions, gives an exact hypergraph-realizability test, and exhibits an infinite chordal family that invalidates a tempting edge-deletion reduction. These results are not a rerun of the previous graph-order-at-most-six screening.

Write M(G) for the r-uniform hypergraph of maximum cliques. A division is precisely a two-coloring of M(G). Maximum and inclusionwise maximal cliques must not be interchanged.

## 1. Exact realizability and the Fano obstruction

For a nonempty r-uniform hypergraph H, its **shadow** S has the same vertices and joins two vertices exactly when some edge of H contains both.

**Proposition 1.** There is a graph G on the same vertex set in which every edge of H is a maximum r-clique if and only if S has no (r+1)-clique. Moreover, H is exactly the family of maximum cliques of some such G if and only if S has no (r+1)-clique and every r-clique of S belongs to H.

**Proof.** Every pair in each edge of H must be an edge of G, so S is a subgraph of G. A forbidden larger clique in S is therefore fatal, and every r-clique of S must also be a maximum clique of G. Conversely, under the respective conditions G=S works. Since H is nonempty, omega(S)>=r. This proves both statements. Isolated vertices cause no difficulty. The proposition does not say that S is odd-hole-free whenever an odd-hole-free supergraph G exists. Section 2 disproves precisely that assertion.

For the Fano plane, take vertices 0,...,6 and triples
012, 034, 056, 135, 146, 236, 245.
Every pair lies in exactly one triple, so S=K7. Consequently these triples cannot even be a subfamily of maximum triangles of a graph. This is a graph-realizability obstruction, not a two-coloring of the Fano plane: the Fano plane itself is not two-colorable. To see the latter without enumeration, every four-element subset contains a line unless its complementary triple is a line. Indeed a line-free four-set has its six pairs on distinct lines, each meeting it in two points, leaving the seventh line in the three-point complement. Every color split has a color class of size at least four; if a four-set is line-free, its three-point complement is a monochromatic line, and a larger line-free color class would have at least ten distinct pairs but only seven lines to contain them. The supplied certificate independently checks all 128 colorings and all 21 pairs.

More generally, any nontrivial r-uniform pair-covering design on more than r vertices has a complete shadow and cannot supply maximum-r-clique constraints directly. A counterexample search using abstract non-two-colorable hypergraphs must test this shadow obstruction before any odd-hole test or graph completion.

## 2. A chordal graph can have an odd hole in its maximum-clique shadow

Fix odd m>=5 and r>=4. On cyclically ordered core vertices c0,...,c_(m-1), take the fan triangulation of the m-cycle: all perimeter edges and all chords c0-ci for 2<=i<=m-2. For each perimeter edge e add r-2 fresh vertices, make them together with the endpoints of e into a K_r, and give the fresh vertices no other neighbors. Call the result G_(m,r).

**Theorem 2.** G_(m,r) is chordal, has clique number r, and its maximum cliques are exactly the m attached K_r's. The graph consisting only of edges that lie in maximum cliques has an induced m-cycle on the core vertices.

**Proof.** First eliminate every fresh vertex, one at a time; its remaining neighbors belong to its attached clique. The remaining fan has the perfect-elimination order c1,c2,...,c_(m-1),c0: at each elimination the remaining neighbors are contained in {c0,c_(i+1)}. An induced cycle of length at least four cannot exist in a graph with such an order, because its earliest eliminated vertex would have two nonadjacent later cycle neighbors. Hence G_(m,r) is chordal and in particular odd-hole-free.

A clique containing a fresh vertex is contained in that vertex's attached K_r. A core-only clique has size at most three, by the fan's elimination order. Since r>=4, exactly the attached K_r's are maximum. Each fan chord is in no attached K_r, so deletion of all edges not belonging to a maximum clique deletes all fan chords while preserving all perimeter edges. Thus the induced core subgraph becomes C_m. This proves the theorem.

These examples do have divisions. Color every core vertex red and every fresh vertex blue. Every maximum clique contains two red vertices and r-2 blue vertices. The point is a limitation on proof strategy: deleting irrelevant edges preserves the division constraints but does not preserve the odd-hole-free hypothesis. This remains false even for chordal input graphs, every odd hole length m>=5, and every r>=4.

The same hypergraph also has a strong odd incidence cycle of length m: choose the m core vertices and the m attached maximum cliques in cyclic order; every chosen clique contains exactly its two consecutive chosen core vertices. Therefore odd-hole-free, and even chordal, graphs need not have balanced maximum-clique hypergraphs. A smaller version is the three-sun, whose central triangle and three edge-attached triangles give a strong incidence triangle.

## 3. Two incidences per vertex suffice

**Theorem 3.** A finite hypergraph whose edges have size at least three and whose vertices belong to at most two edges has a two-coloring. No graph or odd-hole hypothesis is needed.

**Proof.** Form a loopless multigraph D with one real vertex for each hyperedge and one auxiliary vertex z. A hypergraph vertex of incidence two becomes an edge joining its two distinct hyperedges. A hypergraph vertex of incidence one becomes an edge joining its hyperedge to z. Hypergraph vertices of incidence zero may later receive either color. Parallel edges are allowed. Each real vertex has degree equal to its hyperedge size, hence at least three.

Add one extra edge from z to every real vertex of odd degree. All real degrees are now even, and z also has even degree, because the total degree sum is even. In each nontrivial component take an Euler circuit; start at z when z belongs to the component, and otherwise at any real vertex. Color its traversed edges alternately red and blue. At each vertex other than the start, incident edges occur in arrival/departure pairs of opposite colors. If the circuit has odd length, only the start's first/last pair can be equal-colored.

For a real vertex in a component containing z, its augmented degree is at least four and it has half its incident edges of each color. Removing its at most one added edge leaves at least one of each color. In a component not containing z, every real vertex had even degree at least four, no added edges exist, and even the start retains at least degree/2-1>=1 edge of each color. Thus every real vertex sees both colors after deletion of the added edges. Transfer the color of each original dual edge to its corresponding hypergraph vertex. Every hyperedge is bichromatic.

**Corollary.** Every graph of clique number at least three in which each vertex belongs to at most two maximum cliques has a division. Any maximum-clique obstruction in that range has some vertex in at least three maximum cliques. This is stronger than merely ruling out incidence-zero and incidence-one vertices, but it is not a full structural characterization.

## 4. A stronger incidence criterion for larger clique number

**Theorem 4.** A finite hypergraph H has a two-coloring if every subfamily F of its edges satisfies |union F|>=2|F|.

**Proof.** Replace each hyperedge by two labelled copies and match these copies to distinct vertices lying in the copied edge. The stated condition implies Hall's condition for the copied family: if a set of copies represents t distinct edges, it has at most 2t members and its neighborhood has at least 2t vertices. Thus an injective choice of representatives exists. Color the representative of the first copy of every edge red and that of its second copy blue. These representatives are all distinct, so these assignments are consistent. Color remaining vertices arbitrarily.

For completeness, the matching form of Hall's condition follows by the usual alternating-path argument: a maximum partial matching that omits a left vertex has no augmenting path. The reached left vertices then have a neighborhood consisting of fewer matched right vertices, contradicting Hall's condition.

If every edge has size at least r and every vertex has incidence at most floor(r/2), counting incidences gives r|F|<=floor(r/2)|union F|<=r|union F|/2. Thus Theorem 4 applies. Combining with Theorem 3, every non-two-colorable r-uniform hypergraph (r>=3) has a vertex of incidence at least max(3,floor(r/2)+1). A more useful necessary condition is the existence of an explicitly inspectable subfamily with fewer than twice as many vertices as edges.

These are sufficient criteria only. For example, the four three-element stars of K4, regarded as hyperedges on its six edges, violate |union F|>=2|F| for the full family while satisfying Theorem 3.

## 5. Exact computational scope

The certificate inputs specify four independent objects: the Fano triples, the explicit G_(5,4) graph with a claimed perfect-elimination order and shadow-hole witness, a six-uniform incidence-three Hall witness, and the exact hypergraph enumeration bounds. The checker rejects malformed or missing inputs, symlinks, inventory drift, bad hashes, or mismatched result data. It verifies the Fano impossibility and non-two-colorability, enumerates all maximum cliques of G_(5,4), checks its perfect-elimination order, checks its shadow C5, and checks its explicit division. It tests the constructive dual-Euler algorithm on every simple r-uniform hypergraph on a fixed labelled n-vertex set with n<=7, 3<=r<=n, and maximum incidence at most two. There are exactly 11,390 such hypergraphs under these labelled-uniform scope conventions; 6,170 also satisfy the Hall condition. It independently brute-forces a division of every one of the 11,390 and checks all 64 subfamilies of the separate rank-six Hall witness. The finite tests supplement the all-size proofs; they are not an exhaustive search for counterexamples to OPG-56230.

## Literature boundary

The main target is stated at https://www.openproblemgarden.org/op/2_colouring_a_graph_without_a_monochromatic_maximum_clique . The omega=3 case is already covered by the four-color theorem of Chudnovsky, Robertson, Seymour, and Thomas, *K4-free graphs with no odd holes*, Journal of Combinatorial Theory Series B 100 (2010), 313-331, author PDF https://thomas.math.gatech.edu/PAP/k4free.pdf . Their Theorem 1.3 states the four-color result, and the paragraph following Conjecture 1.4 explicitly gives its divisibility consequence. Merging four proper colors into two pairs proves it directly. No proof audit of that external theorem is claimed here; the present structural proofs do not depend on it.
