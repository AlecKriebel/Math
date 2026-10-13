# Three terminal shortest path blocking is NP complete

## Result and scope

For a finite simple undirected graph with unit edge lengths and three distinct
terminals r, s, t, consider deleting a minimum number of edges so that each of
the three terminal distances increases by at least one. The decision problem is
NP-complete, even when all three original terminal distances equal 3 and every
edge has deletion cost 1. Consequently, the version with positive, binary-encoded
rational deletion costs is NP-complete in its decision form and NP-hard in its
optimization form as well.

This note gives a direct reduction from Vertex Cover. The precise model is the
undirected triangle case of Blocking Shortest Paths (BSP) posed by Stefan Krause
in Oberwolfach Report 50/2005, pp. 2856–2858 [1], and discussed in his dissertation,
Section 4.3 [2]. It does not concern directed graphs, arbitrary path-length
thresholds, or weighted traversal lengths. The proof is self-contained apart from
the classical NP-completeness of Vertex Cover [3]. No claim of bibliographic
priority is made.

## Definitions and membership in NP

Write d_G(u,v) for the number of edges in a shortest u–v path; put d_G(u,v)=∞
when no such path exists. The input terminals are assumed pairwise connected in
the original graph. A blocker is a set F⊆E(G) such that

    d_(G−F)(x,y) ≥ d_G(x,y)+1

for {x,y}∈{{r,s},{r,t},{s,t}}. Thus disconnection is permitted, and ∞ is larger
than any finite integer. Equivalently, F meets every original shortest path for
every terminal pair. Deleting edges cannot create a shorter path, so this
hitting condition is both necessary and sufficient.

The decision version additionally gives a nonnegative integer budget B and asks
whether a blocker with |F|≤B exists. A certificate is an edge list. Its size and
validity, and all three distance comparisons, can be checked by breadth-first
search before and after deletion, in polynomial time. This proves membership
in NP. With rational deletion costs and a rational budget, exact rational
addition and comparison also take polynomial time in the input bit length.

Let τ(J) denote the minimum cardinality of a vertex cover of a graph J. A vertex
cover meets every edge in at least one endpoint.

## Lemma 1  A tripartite vertex cover instance

Let Q=(V,E) be any finite simple undirected graph, with n vertices and m edges.
Choose an order (u_e,v_e) of the endpoints of each e∈E. Replace that edge by

    u_e — b_e — c_e — v_e,

where b_e and c_e are new vertices used only for e. Delete the original edge.
Call the resulting graph H. It is tripartite with explicitly supplied independent
parts

    A=V,   B={b_e:e∈E},   C={c_e:e∈E}.

It has n+2m vertices and 3m edges, and

    τ(H)=m+τ(Q).

Proof. If S is a vertex cover of Q, extend S by one new vertex for each edge e:
choose c_e if u_e∈S and v_e∉S; choose b_e if u_e∉S and v_e∈S; if both endpoints
belong to S, choose either b_e or c_e. The case in which neither belongs to S
cannot arise. All three edges replacing e are covered. Thus this extension is a
vertex cover of H of size |S|+m, proving τ(H)≤m+τ(Q).

Conversely, let X be any vertex cover of H, and put S=X∩V. Each middle edge
b_ec_e requires at least one of b_e,c_e to belong to X. Moreover, if neither
u_e nor v_e belongs to S, covering u_eb_e and c_ev_e requires both new vertices.
Let q be the number of edges of Q with neither endpoint in S. Since different
edge gadgets have disjoint new vertices,

    |X| ≥ |S|+m+q.

Add one arbitrary endpoint of each of these q uncovered edges to S, obtaining a
vertex cover S′ of Q. Repeated choices only reduce its size, so

    τ(Q) ≤ |S′| ≤ |S|+q ≤ |X|−m.

Taking an optimal X proves the reverse inequality and hence the identity. ∎

If m≥1, H has at least one edge between each pair of its three parts: every
gadget contributes an A–B edge, a B–C edge, and a C–A edge. This will ensure that
all three terminal distances in the next construction are exactly 3.

## Lemma 2  Terminal spokes realize vertex cover

Let H=(W,J) be any finite simple tripartite graph with supplied partition
W=A⊔B⊔C. Assume that each of A–B, A–C, and B–C contains at least one edge.
Add three new vertices r,s,t and add precisely these terminal edges:

- r is adjacent to every vertex in A;
- s is adjacent to every vertex in B;
- t is adjacent to every vertex in C.

There are no other new edges. Call this graph G_H. Give every edge, both old and
new, unit length and unit deletion cost. For w∈W, write p(w) for its part's
terminal and e_w={p(w),w} for its unique terminal spoke.

Then all three terminal distances in G_H equal 3. More precisely, for distinct
parts U,V with terminals a,b, the shortest a–b paths are exactly

    a — u — v — b     with u∈U, v∈V, uv∈J.

Indeed, terminals are nonadjacent and their neighborhoods are disjoint. Thus
there is no terminal path of length 1 or 2. The assumed cross-part edge supplies
a path of length 3. Any path of length 3 must start with a spoke into U, end with
a spoke from V, and use one H-edge between those two interior vertices. This
also excludes unwanted terminal shortcuts and proves the claimed complete
characterization, not merely the existence of selected geodesics.

Let opt(G_H) be the minimum blocker size for the three terminal pairs. Then

    opt(G_H)=τ(H).

Proof. Given any vertex cover X of H, delete the spokes {e_w:w∈X}. Every terminal
geodesic is indexed by an H-edge uv, and X contains u or v. Therefore the deleted
spokes meet every such geodesic. This gives a blocker of size |X| and proves
opt(G_H)≤τ(H).

Conversely, let F be any blocker in G_H, allowing F to contain arbitrary H-edges
as well as spokes. Form a set X⊆W as follows:

1. For each deleted spoke e_w∈F, put w into X.
2. For each deleted H-edge uv∈F∩J, put one arbitrarily chosen endpoint into X.

Each deleted edge contributes at most one vertex, so |X|≤|F|. For an H-edge uv,
the corresponding terminal path has edge set {e_u,uv,e_v}. Since F blocks that
path, it contains at least one of these edges. In the spoke cases, X contains
the corresponding endpoint; in the middle-edge case, X contains the endpoint
chosen in step 2. Hence X covers uv. This holds for every H-edge, making X a
vertex cover and proving τ(H)≤|F|. Minimize over F to obtain equality. ∎

The converse explicitly handles the possibility of deleting middle edges. No
infinite-cost edges, protected edges, parallel edges, or large-cost gadgets are
needed.

## Theorem  NP completeness with distance three and unit costs

Take an arbitrary Vertex Cover decision instance (Q,k), where Q is a finite
simple graph and k is a nonnegative integer. We may restrict to instances with
m=|E(Q)|≥1: the omitted edgeless cases are trivially yes and can be handled
separately. Equivalently, a total reduction may send every edgeless instance to
any fixed yes-instance satisfying the target restrictions.

Construct H by Lemma 1, then G_H by Lemma 2, and give the BSP instance budget

    B=m+k.

The assumptions of Lemma 2 hold because m≥1. Its three terminals are distinct,
pairwise nonadjacent, and at original pairwise distance exactly 3. All graph
edges have unit length and unit deletion cost. The two identities give

    Q has a vertex cover of size at most k
    ⇔ τ(Q)≤k
    ⇔ τ(H)≤m+k
    ⇔ opt(G_H)≤B.

The graph has exactly n+2m+3 vertices and n+5m edges. It can be written in
O(n+m) time from the input adjacency list, apart from standard representation
costs. The budget m+k is computed in polynomial bit time. There is no unary
expansion of the input budget, and no graph-size dependence on its magnitude.
Thus this is a polynomial many-one reduction.

Vertex Cover is NP-complete [3], so the restricted unit-cost BSP decision
problem is NP-hard. Membership in NP was proved above, completing the proof.
Allowing positive rational deletion costs includes all unit-cost instances, so
the same hardness and NP-membership classification holds for that version.
A polynomial-time exact optimization algorithm would decide the budget version;
therefore both optimization variants are NP-hard. ∎

## Optional finite connectivity strengthening

The main theorem uses the standard BSP convention permitting disconnected
terminal pairs. The reduction can also be made to admit cheap feasible solutions
with finite distances, if desired. Add to G_H a fresh internally vertex-disjoint
path of length 4 between each terminal pair, with no other incident edges on the
nine new internal vertices. Keep every deletion cost equal to 1.

These added paths create no terminal path of length at most 3: a simple path
using any new internal vertex must traverse a whole four-edge added path between
two terminals. Therefore the original terminal geodesics remain exactly those
in Lemma 2. Every blocker in this enlarged graph still maps to an H-cover of no
greater cardinality, by ignoring deletions on the new paths and using Lemma 2's
mapping on the original edges. Conversely, deleting the spokes of an H-cover
leaves all added paths intact. Its terminal distances are at least 4 because
all original geodesics are blocked, and at most 4 via the added paths. They are
therefore exactly 4. The optimum for the at-least-one-increase problem remains
τ(H). The budgeted variant that additionally requires all terminal distances
to stay finite, or even to increase exactly from 3 to 4, is consequently NP-hard
and is in NP. This paragraph asserts terminal connectivity, not connectivity
of every vertex of the remaining graph.

## Computational verification

The accompanying standard-library Python script independently enumerates
shortest paths using BFS labels and tests deleted-graph distances by BFS. It
also checks exact optimum equalities using integer hitting-set recursion and
brute-force vertex cover. The recorded run passed:

- All 165,952 edge-deletion subsets for 145 small tripartite graphs, including
  every subset rather than only minimum blockers;
- No-larger-cover extraction for all 89,975 feasible blockers in that suite;
- Exact optimum equality for all 3,375 tripartite graphs with part sizes (2,2,2)
  and at least one edge of every cross-part type;
- The composed reduction for all 1,094 nonempty labelled graphs on two through
  five vertices, including 6,484 budget comparisons;
- 66 cover-deletion checks for the optional finite-distance extension.

These finite computations are consistency checks. The universal claims follow
from the lemmas and reduction, not from enumeration.

## References

[1] Stefan Krause, “Increasing distances in graphs,” in Combinatorial
Optimization, Oberwolfach Report 50/2005, pp. 2856–2858. Report DOI:
https://doi.org/10.4171/OWR/2005/50 . Publisher PDF:
https://ems.press/content/serial-article-files/46024?nt=1 .

[2] Stefan Krause, Increasing Distances in Graphs, doctoral dissertation,
Technische Universität Braunschweig, 24 February 2006. See the definition on
printed p. 2, Section 4.3 on printed pp. 34–36, and Theorem 9.3 on printed
pp. 83–84. Institutional-library mirror:
https://webdoc.sub.gwdg.de/ebook/dissts/Braunschweig/Krause2006.pdf .

[3] Richard M. Karp, “Reducibility Among Combinatorial Problems,” in Complexity
of Computer Computations, 1972, pp. 85–103. The classical Node Cover problem is
Vertex Cover in the terminology used here; see the Main Theorem and item 5
on printed p. 94. DOI: https://doi.org/10.1007/978-1-4684-2001-2_9 .
Inspected university-hosted scan:
https://cgi.di.uoa.gr/~sgk/teaching/grad/handouts/karp.pdf .
