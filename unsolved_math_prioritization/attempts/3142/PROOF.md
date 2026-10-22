# An exact degree five family for the third power of the third subdivision

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The complete written proof and the complete 96-entry numerical coloring table are retained. The table, the XOR graph definition, and the four proved constraints make the positive eight-color certificate independently checkable by hand. This is not an executable computational reproduction package: code, raw exhaustive computation records and search outputs, copied source documents and images, and private coordination material are omitted. The historical exhaustive checks are reported as authenticated supporting metadata; their original executions are not rerun or supplied as an executable replay. The all-positive-t theorem and the lower bounds rest on the written arguments, not finite testing or failed searches.

The general 2 Delta + 1 conjecture remains unresolved by this work. No novelty, priority, exhaustive literature-survey, or current-openness claim is made.

All computational and source-inspection statements below describe the earlier accepted work. Editorial preparation performed no new mathematical execution, scholarly-source retrieval, source text extraction, or visual source inspection.

## Result and scope

For every integer t >= 1, the graph H_t defined below is a finite, connected,
nonbipartite, simple, 5-regular graph on 16t vertices, and

    chi(H_t^(3/3)) = 8.

The base graph H_1 is the explicitly defined 5-regular Clebsch graph C. Its
incoming-singleton simultaneous coloring number is exactly 16, although its
unrestricted simultaneous coloring number is 8. Thus a strategy that insists on
one color on every set of incoming incidences cannot prove the desired bound
2 Delta + 1 = 11 even on this base graph. This is an obstruction to that stronger
strategy, not a counterexample to the original conjecture.

The original assertion for every finite simple graph of maximum degree Delta >= 2
is unresolved by this work. No novelty claim, current-best-bound claim, complete
literature search, or worldwide openness certification is made. The result here
is a restricted theorem with a complete explicit finite certificate and an
elementary proof for the infinite family.

## Definition and credited background

Replace every edge uv of G by the path u, (u,v), (v,u), v. Write S_3(G) for the
resulting subdivision. The graph G^(3/3) has all vertices of S_3(G), with two
distinct vertices adjacent exactly when their distance in S_3(G) is at most
three. The fraction does not cancel.

Mozafari-Nia and Nejad Iradmusa [1, Theorem 1.6] identify this coloring problem
with simultaneous coloring of vertices and incidences. Their Conjecture 1.7 is
the precise 2 Delta + 1 target. Their introduction credits the previously proved
Delta <= 4 cases and records the general 3 Delta bound. The same paper treats
forests, cycles, complete graphs, k-degenerate graphs, complete bipartite graphs,
and regular bipartite graphs. Those results are prior work, not results of this
attempt. In particular, Theorem 3.1 gives Delta + 2k for k-degenerate graphs;
Theorem 3.6 improves the 3-degenerate case for Delta >= 5. Theorem 4.9 treats
k-regular bipartite graphs with k >= 4. The result below does not purport to
replace any of those theorems.

We use the elementary incoming-color observation underlying [1, Lemma 2.1] and
the square-coloring interpretation in [1, Theorem 1.11 and Corollary 2.7]. Proofs
of the exact statements needed here are included, so the certificate does not
depend on interpreting an uninspected reduction.

## Exact constraints from subdivision distances

A color is assigned to each terminal u and each ordered adjacent pair (u,v).
For a vertex u, write O(u) for the colors of arcs (u,v), and I(u) for the colors
of arcs (v,u). Proper coloring is equivalent to the following four requirements:

1. Adjacent terminals have different colors.
2. The color of u belongs to neither O(u) nor I(u).
3. The outgoing colors at each u are pairwise distinct.
4. O(u) and I(u) are disjoint for each u.

Here is a direct distance justification. Adjacent original vertices are distance
three in the subdivision; nonadjacent original vertices are at least distance
six. A terminal is within distance three of an internal vertex exactly when it
is an endpoint of that internal vertex's original edge. Two internal vertices
from distinct edges sharing an original endpoint have distances two, three, or
four through that endpoint: respectively both are near it, exactly one is near
it, or neither is near it. The first two cases are exactly a common tail or two
consecutive arcs. Opposite arcs on the same original edge are distance one. An
alternative route through a complete original edge has length at least five,
so it adds no missing adjacency at radius three. For distinct arcs (u,v) and
(w,z), the complete conflict criterion is therefore

    u = w, or v = w, or z = u.

This proves the stated equivalence, including terminal constraints. It is not
incidence coloring alone and it is not total coloring.

## The base graph and its geometry

Let the vertex set of C be {0,1,...,15}, interpreted as four-bit vectors. The
operation XOR is vector addition over the two-element field. Put

    S = {1, 2, 4, 8, 15},
    E(C) = {{x,y}: x XOR y belongs to S}.

All generators are distinct and nonzero, so C is simple and 5-regular, with 40
edges. It is connected because the four unit vectors are generators. The cycle

    0, 1, 3, 7, 15, 0

has length five, so C is not bipartite.

Every nonzero vector outside S has weight two or three. Each weight-two vector
is the sum of its two unit vectors, and each weight-three vector is the sum of
15 and the unit vector in its missing coordinate. Thus the ten unordered pairs
of distinct elements of S give exactly the ten nonzero vectors outside S, each
once. Two nonadjacent vertices of C consequently have exactly two distinct
common neighbors. In particular C has diameter two. Deleting vertex 0 leaves
a graph of diameter at most two: among the two common neighbors of any
nonadjacent remaining pair, at least one survives. Hence the square of C - 0
is a complete graph on 15 vertices.

## A complete eight color certificate

The following table assigns colors 0 through 7. Column T is the color of the
terminal x. Column s is the color of the internal vertex (x, x XOR s).

| x | T | s=1 | s=2 | s=4 | s=8 | s=15 |
|---|---|---|---|---|---|---|
| 0 | 5 | 3 | 6 | 1 | 0 | 4 |
| 1 | 2 | 7 | 5 | 1 | 4 | 0 |
| 2 | 2 | 5 | 7 | 1 | 4 | 3 |
| 3 | 4 | 0 | 3 | 1 | 6 | 2 |
| 4 | 3 | 2 | 5 | 7 | 4 | 6 |
| 5 | 4 | 0 | 3 | 6 | 7 | 5 |
| 6 | 4 | 3 | 0 | 6 | 7 | 2 |
| 7 | 0 | 5 | 2 | 7 | 4 | 6 |
| 8 | 3 | 2 | 5 | 4 | 7 | 1 |
| 9 | 5 | 0 | 6 | 7 | 3 | 1 |
| 10 | 1 | 3 | 0 | 7 | 6 | 2 |
| 11 | 0 | 5 | 2 | 4 | 7 | 1 |
| 12 | 6 | 3 | 7 | 0 | 1 | 5 |
| 13 | 0 | 4 | 5 | 2 | 1 | 6 |
| 14 | 3 | 4 | 2 | 5 | 1 | 6 |
| 15 | 2 | 0 | 3 | 6 | 1 | 7 |

For direct checking, the incoming color sets I(x), in vertex order 0 through 15,
are:

    {7}, {3,6}, {0,6}, {5,7}, {0,1}, {1,2}, {1,5}, {1,3},
    {0,6}, {2,4}, {4,5}, {3,6}, {2,4}, {3,7}, {0,7}, {4,5}.

These are the incoming sets recorded in the accepted certificate description.
Equivalently they can be read directly from the table by taking the s-column
in row x XOR s. Each row
has five distinct outgoing colors. Those colors and its terminal color are
disjoint from I(x), and adjacent terminal entries are unequal. These are exactly
the four constraints proved above. Thus chi(C^(3/3)) <= 8.

An independently written verifier also constructs the actual 96-vertex
subdivision and calculates all distances by Floyd-Warshall. It checks the
certificate on all 720 edges of the third power, and compares the distance and
arc criteria on all 4,560 unordered vertex pairs. This is a finite, exhaustive
check of this certificate, not an enumeration of all graphs of a given order.

## Lower bound via incoming colors

Lemma. If G is d-regular with d >= 2 and chi(G^(3/3)) <= d+2, then the square
G^2 has a proper coloring with at most d+2 colors.

Proof. At u, the d outgoing internal vertices and terminal u form a clique of
size d+1. Every incoming internal vertex is adjacent to all of them. With at
most d+2 colors, the incoming vertices must therefore all have one common
color h(u). (They are nonempty because d >= 2.) If u and v are adjacent, their
opposite arcs have colors h(v) and h(u), so h(u) differs from h(v). If u and v
have a common neighbor w, the outgoing arcs (w,u) and (w,v) have colors h(u)
and h(v), so these also differ. Hence h is a proper coloring of G^2. This is
the regular-graph case of the mechanism in [1, Lemma 2.1]. End of proof.

Since C has diameter two, C^2 is K_16. The lemma rules out seven colors on
C^(3/3). Together with the table, this proves chi(C^(3/3)) = 8.

## The exact obstruction to singleton incoming colors

Write chi_vi,1(G) for the minimum palette size under the additional restriction
that every I(u) contains only one color, following [1, Definition 1.3]. The
argument defining h above does not require a d+2 palette once this restriction
is imposed. Therefore chi_vi,1(C) >= chi(C^2) = 16.

There is a matching explicit 16-color construction. Color arc (u,v) with v,
and color terminal v with v XOR 3. Outgoing colors are distinct, all incoming
colors at v equal v, and no outgoing color equals v. The terminal color v XOR 3
equals neither v nor a neighbor of v, because 3 is nonzero and is not in S.
Finally XOR by 3 is a permutation, so adjacent terminals have different
colors. The four constraints hold. Consequently

    chi_vi,1(C) = 16, while chi_vi(C) = 8.

This does not refute a strategy allowing two or more incoming colors. The
eight-color certificate itself uses at most two incoming colors at every
vertex, with one incoming color at vertex 0 and two at every other vertex.

## Pulling back a coloring

Lemma. Let f: V(H) -> V(G) be a graph homomorphism that is injective on the
neighbors of each vertex. Then chi(H^(3/3)) <= chi(G^(3/3)).

Proof. Given a coloring c of G^(3/3), assign terminal x the color c(f(x)), and
arc (x,y) the color c(f(x),f(y)). Adjacent terminals map to adjacent terminals,
and endpoints of arcs map to their endpoints. Distinct outgoing arcs at x
map to distinct outgoing arcs at f(x), by local injectivity. Consecutive arcs
map to consecutive, distinct arcs; equality would force the images of two
adjacent vertices to coincide in a loopless graph. The exact four constraints
therefore hold after pullback. End of proof.

In particular this applies to every graph covering map. Local injectivity is
an actual hypothesis: a homomorphism from a two-leaf star onto an edge would
identify its two outgoing arcs, so arbitrary graph homomorphisms do not
suffice for this pullback rule.

## The infinite family

For t >= 1, let H_t have vertices (x,i), with 0 <= x <= 15 and i in Z/tZ.
For each edge {u,v} of C other than {0,2}, insert the edge {(u,i),(v,i)} for
every i. Replace the copies of {0,2} by

    {(0,i),(2,i+1)} for every i in Z/tZ.

These edges define a simple graph: a repeated edge would repeat its base edge,
and each listed base edge supplies a matching between its endpoint fibers.
Every vertex has one neighbor over each of the five neighbors of its image in
C. Thus projection (x,i) -> x is a covering map, H_t is 5-regular, and H_t has
16t vertices and 40t edges. The pullback lemma and the table give an eight-color
upper bound for every t.

The subgraph of unit-vector edges is a four-dimensional cube. Removing the edge
{0,2} does not disconnect it, because that edge has the alternate cube path
0,1,3,2. Thus C - {0,2} is connected. Every layer of H_t using the untwisted
edges is consequently connected, and the twisted edges join layer i to i+1.
It follows that H_t is connected. The five-cycle 0,1,3,7,15,0 uses no twisted
edge and survives in each layer, so H_t is nonbipartite.

Within any layer, the vertices with x != 0 induce a copy of C - 0. Its square
is K_15 by the earlier two-common-neighbor argument. Thus H_t^2 contains a
15-clique. If H_t^(3/3) admitted seven colors, the regular-graph lemma would
give a seven-coloring of H_t^2, a contradiction. Therefore

    chi(H_t^(3/3)) = 8 for all t >= 1.

This infinite conclusion follows from the proof. The separate direct distance
checks for all integers 1 <= t <= 16 only corroborate the implementation.

The same square clique also gives chi_vi,1(H_t) >= 15. Pulling back the
16-color singleton construction gives chi_vi,1(H_t) <= 16, because all arcs
entering a lifted vertex map to arcs entering one base vertex. Thus the
singleton-incoming restriction exceeds the target bound 11 throughout this
infinite family, even though the unrestricted answer is always 8. No claim
distinguishing 15 from 16 is made for t > 1.

## Remaining gap

The construction covers a particular explicit family and, for the upper bound,
all graphs admitting a locally injective homomorphism into C. It supplies no
such homomorphism for an arbitrary graph. It does not prove the target even
for all 5-regular graphs, let alone all finite simple graphs with Delta >= 2.
The present result also does not improve the recorded 3 Delta bound in full
generality. The singleton obstruction excludes only a stronger auxiliary
coloring requirement; the original 2 Delta + 1 conjecture survives it.

## References

[1] M. Mozafari-Nia and M. Nejad Iradmusa, Simultaneous coloring of vertices and
incidences of graphs, Australasian Journal of Combinatorics 85(3) (2023),
287-307. https://ajc.maths.uq.edu.au/pdf/85/ajc_v85_p287.pdf

[2] Open Problem Garden, Chromatic number of frac 3 3 power of graph.
https://www.openproblemgarden.org/op/chromatic_number_of_frac_3_3_power_of_graph
