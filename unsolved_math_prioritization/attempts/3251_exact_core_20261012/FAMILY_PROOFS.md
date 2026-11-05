Editorial note: The complete authored proof or audit is preserved below. Changes replace only operational artifact identities, byte counts, locations and original replay directions. All mathematical arguments, exact finite scopes and substantive limitations remain. This edition's public manifest identifies the distributed prose.

# A chordal obstruction to naive recursion on the high-incidence core

## Exact scope

For every integer k >= 3, this note constructs a connected chordal finite simple graph G_k with clique number k and a precoloring of its exact high-incidence set X which is a division of G_k[X] at its own clique number k but does not extend to a division of G_k. Here a division means a two-coloring avoiding monochromatic maximum-cardinality cliques. A vertex is high-incidence when it belongs to at least three distinct maximum cliques of the original graph.

This is a counterexample to an intermediate extension heuristic, not to odd-hole-free 2-divisibility. Every G_k is explicitly divisible. The core is perfect: it is the disjoint union of K_k and K_(k-1). In particular, the statement does not contradict the previously accepted sufficient condition that the prescribed core coloring avoid every monochromatic (k-1)-clique. The precoloring below has two such cliques. Nor does it concern an induced-minimal indivisible graph, since this graph is divisible.

No novelty claim is made. This is an elementary construction requiring no external mathematical theorem. The prior high-incidence extension theorem is useful context but is not needed to prove any assertion about this family.

## 1. Construction and exact maximum-clique incidence

Take four pairwise disjoint sets A, P, L, M, each of size k-1, and five further vertices u, b, c, d, e. Thus |V(G_k)| = 4k+1. Put an edge between two vertices exactly when they occur together in at least one of the following eight sets:

1. A union {u}
2. A union {b}
3. A union {c}
4. P union {u}
5. P union {d}
6. P union {e}
7. L union {b}
8. M union {b}.

All eight sets are distinct k-cliques. These are exactly the maximum cliques, and there is no larger clique. To see this directly, a clique containing a vertex of L or M lies in the corresponding displayed set, since such a vertex has no neighbors outside that set. A clique containing d or e lies in P plus that vertex, and one containing c lies in A plus c. After excluding these cases, a clique using P lies in P plus u, because u is the only remaining neighbor outside P. A clique using A lies in A plus at most one of u or b, which are nonadjacent. Any remaining clique lies in {u,b}, a stable pair. This covers every clique and proves both assertions.

Consequently every vertex of A and P belongs to exactly three maximum cliques; b belongs to exactly three; u belongs to exactly two; and c,d,e and the vertices of L and M each belong to exactly one. Therefore the exact high-incidence set is

    X = A union P union {b}.

It has 2k-1 vertices. Its induced graph is the disjoint union of the k-clique A union {b} and the (k-1)-clique P. Thus omega(G_k[X]) = chi(G_k[X]) = k. Every induced subgraph of this core is again a disjoint union of at most two cliques, and its clique and chromatic numbers coincide (including the empty graph convention), so the core is perfect.

## 2. Connectedness and an explicit elimination certificate

The graph is connected: u joins the A and P blocks; b joins A to L and M; c,d,e attach to A or P.

A perfect elimination order is: all vertices of L, then all of M, then d, e, c, then all of P, then b, then u, then all of A. Within each listed set any order may be used. At elimination, each L or M vertex has its remaining neighbors in its own clique together with b. The later neighbors of d and e are P, and those of c are A. After d,e are gone, each P vertex has its later neighbors in P union {u}. After L,M are gone, the later neighbors of b are A. The later neighbors of u are A; the final A block is a clique. Thus every eliminated vertex has a clique as its set of later neighbors.

This certificate proves directly that G_k has no induced cycle of length at least four: the earliest eliminated vertex on such a cycle would have two later cycle-neighbors which are adjacent, a forbidden chord. In particular G_k is chordal and odd-hole-free. This argument does not import a perfect-graph theorem.

## 3. A valid core division which cannot extend

Color every vertex of A blue, and color b and every vertex of P red. This is a division of G_k[X] at its own clique number k: its unique maximum clique A union {b} is bichromatic. The red P clique has size only k-1.

In any extension, the maximum clique A union {u} forces u red. The maximum clique P union {u} simultaneously forces u blue. No extension exists. Notice that u has incidence exactly two and that all other unprescribed vertices have incidence one. The obstruction therefore persists in the precise low-incidence setting of the accepted extension results. It is a two-clique unit-propagation conflict, rather than a spurious abstract hypergraph or an induced odd hole.

This refutes each of these proposed universal statements, even for a connected chordal graph:

- Every division of the exact high-incidence core at its own clique number extends.
- Every division of that core extends when its clique number equals that of the whole graph.
- Perfectness of the high-incidence core makes every core division extend.

The statements must retain the word "every": the construction does not refute existence of an extendible division of the core, or divisibility when the core is perfect.

## 4. Exact projection of the family onto its core

More strongly, prescribe any two-coloring of X. It extends if and only if both of the following conditions hold:

(i) A union {b} is bichromatic;
(ii) A and P are not monochromatic in opposite colors.

Necessity of (i) is immediate. If (ii) fails, the two cliques through u force opposite colors on u. For sufficiency, choose u to avoid the monochromatic color of A if A is monochromatic, and to avoid the monochromatic color of P if P is monochromatic. These requirements agree if both occur, by (ii); if neither occurs, either color works. Choose c opposite A's color when A is monochromatic, and choose d,e opposite P's color when P is monochromatic; if the relevant set is mixed, either color works. Finally color each of L and M using both colors, possible because k-1 >= 2. Every one of the eight exact maximum cliques is now bichromatic.

There are 2^(2k-1) core colorings. Exactly 2^k violate (i), since one may choose the common color of A union {b} in two ways and then color the k-1 vertices of P arbitrarily. Thus 2^(2k-1)-2^k are divisions of the core. Among these divisions exactly two violate (ii): choose the monochromatic color of A, give P the opposite color, and give b the opposite color of A to satisfy (i). Hence precisely

    2^(2k-1) - 2^k - 2

core divisions extend, and precisely two fail. In particular, at k=4 the 17-vertex graph has seven high-incidence vertices; 112 of the 128 core colorings are core divisions, 110 extend, and two fail.

Every G_k is divisible, for example by choosing both A and P bichromatic, coloring each of L and M bichromatically, and coloring u,b,c,d,e arbitrarily. This also gives an explicit extension-compatible core division. The obstruction cannot be used to claim a counterexample to the target conjecture.

## 5. Bounded verification and limits

The accompanying checker reconstructs the graph independently from the eight named clique bags, computes its maximum cliques by a general maximal-clique algorithm, computes all original incidences, checks connectedness and the complete elimination certificate, and verifies the exact core induced graph. It checks every core coloring for each integer 3 <= k <= 8 against a separate depth-first Boolean extension oracle which reads the computed maximum-clique list and makes no use of the projection formula. Returned full colorings are checked against every computed maximum clique. The exact universe is 43,680 core colorings of six specifically constructed labelled graphs; it is not an enumeration of all graphs of any order. A mandatory case-stream digest binds the exact tested labels and colorings.

For the k=3 and k=4 fixtures it also inspects every vertex subset of odd cardinality at least five, testing the induced subgraph for connectedness and degree two. This is a separate exhaustive odd-hole check on those two graphs only. At larger k the all-size elimination proof and its checked certificates supply the odd-hole-free claim. A separately stored explicit k=4 edge-list fixture and its bad core coloring must agree exactly with the construction and be rejected by the independent extension oracle.

All acceptance checks use explicit exceptions, not Python assertions, and are run under normal Python, -O, and -OO. Manifest and external-pin validation require regular nonsymlink files, safe nonsymlink directory ancestors, exact file inventory, exact byte lengths, and exact SHA-256 hashes. Negative tests use disposable copies, including missing/tampered files, extra entries, root and ancestor symlinks, duplicate-key JSON, wrong scope and expected-count mutations re-manifested and re-pinned to reach semantic checks, and false graph/witness mutations. This provides checks of those exact failure modes, not a claim of protection against concurrent hostile filesystem races or replacement of all trust anchors.

The general target remains unresolved. No queue, repository, publication, or remote-state action is part of this packet. No assertion is made that 4k+1 vertices or 2k-1 core vertices are minimal for this kind of intermediate obstruction.
