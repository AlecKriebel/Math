Editorial note: Complete authored proof or audit prose is preserved below. Only operational artifact identities, byte counts, locations and obsolete replay directions have been replaced; all mathematical arguments, finite scopes and limitations remain. The public manifest identifies the actual distributed edition.

# Maximum-clique boundary flexibility from sparse outside incidence

## Scope and status

The unrestricted conjecture that every finite nonedgeless odd-hole-free graph has a two-coloring with no monochromatic maximum clique remains unresolved here. This packet gives an all-size boundary-extension theorem, a stronger necessary condition for any indivisible graph, an exact low-incidence mixed-constraint lemma, and precisely bounded computational regression checks. It makes no novelty claim and uses no unproved external mathematical input.

For a finite simple graph G, write k=omega(G). A division means a red/blue coloring in which every maximum k-clique is bichromatic. We use maximum cliques, not inclusionwise maximal cliques. Let d_M(v) be the number of distinct maximum cliques containing v. A boundary coloring of a clique C is admissible if it does not already make a k-clique monochromatic; equivalently, both color classes of C have size at most k-1.

## 1. Exact mixed-constraint lemma

A mixed hypergraph has a finite vertex set and a finite labelled family of edges. Repeated copies of an edge are permitted and count separately toward incidence. Each edge has one of three demands:

- B: the edge must be bichromatic.
- 0: the edge must not be entirely color 0.
- 1: the edge must not be entirely color 1.

The last two demands are called one-sided. A component is a connected component of the edge-intersection structure, with its incident vertices. Isolated vertices impose no constraints. A pure odd-cycle component consists of an odd number of size-two edges forming a cycle; each of its vertices has incidence exactly two. The odd length is at least three; parallel size-two edges form an even two-cycle.

**Lemma 1.** Suppose every edge has size at least two and every vertex has incidence at most two. The mixed hypergraph is unsatisfiable if and only if some pure odd-cycle component has demand B on every edge.

**Proof.** Such an all-B odd cycle is plainly unsatisfiable: its size-two constraints require a proper two-coloring of an odd cycle.

Conversely, consider each incidence component separately. If it is a pure odd cycle with at least one one-sided edge e, delete e and alternate colors along the resulting even-length path. Its endpoints have the same color. Choose the global color swap so that this common color is opposite e's forbidden color. All other edges are bichromatic, and e satisfies its one-sided demand.

For every other component we produce a coloring that makes every edge bichromatic, thereby satisfying all three demand types. Construct the loopless dual multigraph D. Each hyperedge becomes a real vertex. Each original vertex of incidence two becomes an edge between its two incident real vertices. Each original vertex of incidence one becomes an edge between its real vertex and a new auxiliary vertex z. Thus each real degree is its hyperedge size, at least two. Add one auxiliary edge to z at every odd-degree real vertex. All degrees become even, including z by degree-sum parity.

If z has positive degree, start an Euler circuit at z. At every real vertex the incident edges occur in oppositely colored arrival/departure pairs when successive circuit edges receive alternating colors. A real vertex of original degree two has no added edge and retains one of each color. A real vertex of even degree at least four has no added edge and retains at least two of each. A real vertex of odd degree has original degree at least three, augmented degree at least four, and after its one added edge is removed it retains at least one of each.

If z is isolated, no added edges or incidence-one vertices exist and every real degree is even. If some real vertex has degree at least four, start the Euler circuit there. Only the start can have an equal-colored first/last pair when the circuit length is odd, and its two color counts are then d/2+1 and d/2-1; both are positive. Every other real vertex has balanced positive counts. If all real degrees are two, the connected dual is a cycle. We already handled the odd case, so here it is even and alternating colors work at every vertex.

Transfer the colors of the original dual edges to the corresponding hypergraph vertices. Each hyperedge sees both colors, as required. Components with no edges and isolated vertices may be colored arbitrarily. This proves both directions. □

This sharpens the previously checked rank-at-least-three incidence-two lemma. The rank-two exception is exact; it is not a claim that all rank-two incidence-two families are colorable.

## 2. Precoloring a small exceptional set in an abstract hypergraph

**Lemma 2.** Let every edge of H have size at least r, where r>=3. Let P be any set of at most r-2 vertices. If every vertex outside P has incidence at most two, every prescribed coloring of P extends to a bichromatic coloring of all edges. The incidences of vertices in P are unrestricted.

**Proof.** Discard any edge already meeting both prescribed colors. For each remaining edge, delete its vertices in P. The residual edge has size at least two. Give it demand B if it met no prescribed vertex, and otherwise the one-sided demand forbidding the color it saw in P. Residual vertex incidence remains at most two. Every residual size-two edge came from deleting at least one prescribed vertex, since each original edge had size at least three, so it is one-sided. Therefore no pure odd-cycle component can have all demands B. Lemma 1 supplies the required extension. □

The bound |P|<=r-2 is sharp for abstract hypergraphs, even when the unconstrained family itself is two-colorable. Let |P|=r-1, let V={v1,...,vr} be disjoint from P, and take edges P union {vi}, for each i, together with V. Every vi has incidence two. If P is entirely red, all vi are forced blue, contradicting the demand on V. Nevertheless, a mixed coloring of P and a mixed coloring of V colors the whole family.

This sharp abstract obstruction cannot be imported into the graph problem. Its shadow is the complete graph on P union V, of order 2r-1. Consequently its r-edges cannot even all be maximum r-cliques in any graph realizing their pair incidences. This explicit realizability failure is part of the result, not an odd-hole-free counterexample.

## 3. Full clique-boundary extension in graphs

**Theorem 3 (clique-boundary flexibility).** Let G be any finite simple graph with k=omega(G)>=3, and let C be any clique, possibly empty. Suppose d_M(v)<=2 for every vertex v outside C. Every admissible red/blue coloring of C extends to a division of G.

No odd-hole assumption is required, and no incidence restriction is imposed on the boundary vertices.

**Proof.** First suppose both color classes in C have size at most k-2. Discard every maximum clique already meeting both colors of C. Remove C from each remaining maximum clique. At least two vertices remain. Give the residual edge demand B if it met no colored vertex, and otherwise the one-sided demand forbidding the prescribed color it met. Every residual vertex is outside C and thus has incidence at most two. A residual edge of size two is one-sided, because k>=3 and at least one vertex was removed. Lemma 1 extends the coloring.

It remains to handle a color class P of C of size k-1. Since k>=3 and |C|<=k, at most one color class can have this size. Call its color red, and define F to be the common open neighborhood of every vertex in P. The set F is stable: two adjacent vertices of F, together with P, would form a (k+1)-clique. It is disjoint from P. Every vertex of C outside P belongs to F, and admissibility gives it the other color. Every vertex of F is forced blue by the maximum clique P union {v}. Prescribe blue to all of F; this agrees with the original boundary coloring.

Now discard every maximum clique meeting both P and F, as it already has both colors. A remaining maximum clique disjoint from P contains at most one vertex of F, since F is stable, so at least k-1>=2 vertices remain uncolored. A remaining maximum clique meeting P is disjoint from F. It cannot contain all k-1 vertices of P, because its last vertex would then belong to F. Thus it contains at most k-2 colored vertices and again leaves at least two uncolored vertices.

All still-uncolored vertices lie outside C and retain incidence at most two in the residual constraints. As before, use demand B for a clique meeting no prescribed color and a one-sided demand otherwise. Every residual size-two edge is one-sided, because its original maximum clique had size k>=3. Lemma 1 applies. Combining its coloring with the prescribed colors on P union F extends the original boundary coloring and divides every maximum clique. □

The stable common-neighborhood step is the graph-realizability fact that fails in the sharp abstract hypergraph construction. It is why Theorem 3 reaches every admissible clique boundary rather than stopping at r-2 vertices.

## 4. Consequences for the remaining obstruction

**Corollary 4.** Every indivisible finite graph with clique number at least three has two nonadjacent vertices each lying in at least three maximum cliques.

**Proof.** Let X={v:d_M(v)>=3}. If X is a clique, choose an admissible coloring of X: any coloring suffices when |X|<k, and choose a mixed coloring when |X|=k. Theorem 3 extends it to a division. Therefore in an indivisible graph X is not a clique, so X contains two nonadjacent vertices. □

The condition is necessary, not sufficient: two nonadjacent high-incidence vertices do not certify indivisibility.

For a clique-separator side of clique number k>=3 that forbids any admissible coloring of its boundary C, Theorem 3 implies that some vertex outside C belongs to at least three maximum cliques of that side. If the side's clique number is below the global threshold k, it imposes no maximum-k-clique constraint at all. In particular, for a size-two separator at k=4, both an equal-only side and a different-only side must have a vertex of maximum-clique incidence at least three away from the separator.

These statements restrict boundary-forcing candidates. They neither construct such candidates nor prove that odd-hole-free clique-separator sides always have compatible boundary colorings. The original unrestricted target remains open within this work.

## 5. Exact computational scope

The checker constructs its objects from first principles, checks every returned coloring, and compares satisfiability with a separate exhaustive Boolean-coloring oracle. It uses exceptions and explicit condition checks; no Python assertion is an acceptance gate.

- Mixed constraints: all multisets of subsets of size at least two of a fixed labelled n-vertex set, for every 0<=n<=5, with maximum vertex incidence at most two. Each multiset is listed in nondecreasing order in the fixed subset order. Its edge occurrences are labelled by position, and every assignment of one of B, 0, 1 to each occurrence is tested. Thus differently ordered demands on repeated copies are distinct tested cases. Empty families and isolated vertices are included. The exact total is 1,910 edge multisets and 72,348 demand-labelled cases, including 147 unsatisfiable cases. This is not a simple-hypergraph-only enumeration.
- Graph boundaries: every simple graph on the fixed labelled vertex sets of orders 0 through 6, for a total of 33,868 graphs. Maximum cliques and all clique boundaries are enumerated. For every graph with k>=3 and every boundary containing all vertices with d_M>=3, all admissible labelled boundary colorings are passed through the constructive extension algorithm and checked against the brute-force oracle. There are 400,508 eligible graph-boundary pairs, 1,593,435 tested boundary colorings, and 631,800 executions of the k-1-color-class/common-neighborhood branch.
- Explicit mixed odd-cycle fixtures have lengths 3, 5, 7, 9. Each all-B cycle is rejected; changing any one edge to either one-sided demand rescues it, for 48 checked rescues.
- Explicit abstract sharpness/realizability fixtures use r=3,4,5. The fixed monochromatic P is blocked, the unrestricted hypergraph is two-colorable, all outside incidences are two, and the shadow is K_(2r-1).

The recursive multiset enumerator may select the current edge again but never an earlier edge. Each legal multiset has exactly one such nondecreasing sequence. Every prefix retains incidence at most two, so capacity pruning loses no case. The graph enumeration uses every bit mask on the n choose 2 possible edges exactly once. The mandatory expected-results file records every per-order count and deterministic SHA-256 hashes of the exact mixed-case and graph-boundary-case streams. These finite tests supplement the proofs. In particular, testing graphs through order six is not a counterexample search at the much larger known necessary orders.

## 6. Replay and integrity boundary

The original replay required three mandatory inputs: the packet directory, its separate external pin, and the externally recorded digest of that pin. It was repeated under normal Python, -O, and -OO. The separate external pin fixes the original manifest's byte count and digest; the original manifest fixes every original payload file, including this proof, mandatory inputs and expected results, and the checker. That checker requires exactly those files plus the manifest, rejects unexpected files and directories, requires regular files, rejects symlink components in the packet and pin paths, and rejects a checker launched from a different packet. The pin must lie outside the packet. This prose edition does not distribute those original programs or replay records.

External post-freeze receipts record actual replay outputs and negative controls. Those checks certify this pinned static packet and the tested mutations; they do not claim protection against concurrent filesystem races or malicious replacement of every external trust anchor. No remote repository or queue is changed by this packet.

## Dependencies and source boundary

The proof is self-contained and extends the locally audited incidence-two Euler construction and exact maximum-clique-shadow realizability analysis. It does not invoke the published omega-three coloring theorem, any March 2026 minimal-non-two-divisible preprint, or an unverified clique-cutset closure claim. The names of prior local packets are provenance only; no prior file is a runtime dependency of this checker. No claim of publication priority or exhaustive literature coverage is made.
