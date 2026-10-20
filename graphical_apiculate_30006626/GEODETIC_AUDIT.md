# Independent audit: finite geodetic subclass

## Verdict and scope

**PASS, with the explicit arguments below.** For a finite connected simple geodetic graph G, its apex algebra is graphical if and only if G is a block graph. Here geodetic means every pair has a unique shortest path, and block graph means every block is a clique (bridges count as K2 blocks). A singleton is allowed. Subalgebras are nonempty, as usual for this context.

This is a subclass result for Question i), not a characterization of all apiculate graphs, not a resolution of Question ii), and not a novelty claim. No infinite-graph extension is claimed.

The source definition is the problem statement in Oberwolfach Report 8/2026, Problem 14, printed page 534: graphical means that the algebra and each subalgebra are apex algebras of apiculate graphs. The realizing graph must have the same underlying set and the same ternary operation, not necessarily the induced subgraph of G.

## 1. Basic algebraic facts

Write a(u,v,w) for the u-apex relative to v,w. In a geodetic graph, the unique u-v and u-w paths have a common initial segment: divergence followed by reunion would yield two distinct shortest paths to the reunion vertex. Its last vertex is the unique apex. Thus every geodetic graph is apiculate.

For every apiculate graph, the operation recovers intervals exactly:

    x belongs to I(u,v) if and only if a(u,v,x)=x.

Indeed, when x is in I(u,v), the common interval I(u,v) intersect I(u,x) equals I(u,x), whose apex is x. Conversely, every apex lies in I(u,v).

Consequently, any graph realizing an algebra on S has its edges forced: distinct u,v are adjacent exactly when no x in S other than u,v satisfies a(u,v,x)=x. This uses the ordinary unweighted connected graph metric. It excludes the possibility of repairing a proposed realization by choosing other edges.

## 2. An isometric odd cycle gives a four-element obstruction

Suppose C is an isometric cycle of length 2k+1, with k at least 2, in geodetic G. For cycle vertices, the shorter cycle arc is the unique G-geodesic. Thus all their intervals and apex values agree with those of C.

The apex operation of an odd cycle is conservative: its value is one of its three arguments. To see this, start at u. The two shorter arcs to v,w either start in opposite directions, in which case their intersection is just u, or in the same direction, in which case one is an initial segment of the other and the apex is the closer endpoint. Repeated arguments cause no difficulty. Hence every subset of cycle vertices is apex-closed in G.

Select four vertices s0,s1,s2,s3 in cyclic order whose successive arc lengths are

    k, k-1, 1, 1.

These are positive, sum to 2k+1, and are each at most k. This explicitly includes C5, with gaps 2,1,1,1.

For consecutive selected vertices, their unique shortest arc is precisely the gap between them, so their interval contains no other selected vertex. For opposite selected vertices, each of the two arcs contains exactly one other selected vertex, and the shorter arc therefore contains exactly one of them. In particular, both diagonals have a selected interior point and are not forced edges.

The uniquely forced graph on S is therefore C4. But each diagonal interval in C4 contains both other vertices, whereas the original restricted interval contains exactly one. The recovered-interval identity rules out equality of the ternary operations. Thus S is a subalgebra which is not an apiculate algebra, and the apex algebra of G is not graphical.

Important distinction: C4 itself is apiculate. The contradiction is not that C4 fails apiculateness; it is that its apex operation does not equal the restricted operation.

## 3. Graphical plus geodetic implies bridged

A geodetic graph cannot contain an isometric even cycle of length at least four: antipodal cycle vertices would have two different shortest paths. Section 2 excludes every isometric odd cycle of length at least five when the algebra is graphical. Thus there are no isometric cycles longer than triangles, precisely the bridged condition.

The standard bridged-graph fact needed in the next step is that bridged graphs satisfy the triangle condition: for adjacent v,w at equal distance j from a root r, a common neighbor exists at distance j-1. For j=1 this neighbor is r itself.

A public scholarly source verifies both ingredients: B. Bresar, J. Chalopin, V. Chepoi, T. Gologranc and D. Osajda, *Bucolic complexes*, Definitions 2.4 and 2.6. Definition 2.6 gives the equivalence of the no-isometric-cycle formulation and weak modularity with the additional short-cycle exclusions; the triangle condition is part of weak modularity. Source inspected during this audit:

https://pageperso.lis-lab.fr/~jeremie.chalopin/publis/BCCGO-AM13.pdf

## 4. A bridged geodetic graph is a block graph

Fix root r. Each nonroot vertex v has exactly one neighbor p(v) one level closer to r: two such neighbors would produce two shortest r-v paths. These parent edges form the BFS tree.

Every edge joins vertices at the same level or consecutive levels. A consecutive-level edge must be a parent edge. If v,w are adjacent at the same positive level, the triangle condition gives a common predecessor; predecessor uniqueness implies p(v)=p(w).

For a fixed vertex p, consider the graph on its children induced by G. Every connected component of this graph is a clique. Otherwise a shortest path between two nonadjacent vertices in that component has an initial induced two-edge path v-w-z. The nonadjacent v,z would then have distinct shortest paths v-w-z and v-p-z, contradicting geodeticity.

For each child component Q of p, form the clique {p} union Q. These cliques contain all edges of G. Their vertex-clique incidence graph is a tree: every nonroot vertex belongs to exactly one clique above it (the child component of its parent), and every such clique has exactly one parent vertex. The root is its only root; levels orient all incidence edges away from it. Thus G is a tree of cliques attached at single vertices, and its blocks are cliques. This argument also covers bridge blocks, where Q has one vertex.

## 5. Direct converse: closed subsets of block graphs

This proof does not rely on identifying the algebra with a particular published quasi-median-algebra convention.

Let G be a finite connected block graph. Its incidence tree T has one node for every original vertex and one node for every block; a vertex is joined to the blocks containing it. The original vertices on the T-path between u and v are exactly I_G(u,v), in order. In particular G is geodetic.

Take a nonempty apex-closed subset S. The singleton case is immediate. Otherwise let T0 be the minimal subtree of T spanning S. Delete the nodes S from T0, and contract each resulting connected component to one new block node. Retain every node of S. The resulting bipartite graph T' is a tree: contracting pairwise disjoint connected subtrees preserves the tree property. It is bipartite between S and the new nodes because original vertex nodes in T have no direct edges to one another. Each component has at least two boundary vertices in S; a component with at most one would contradict minimality of T0.

Define H on S by making the neighbors of each new block node a clique. Then H is a connected block graph whose vertex-block incidence tree is T'. In particular, H is geodetic and apiculate. Contraction preserves the order of the retained S-nodes along every tree path. Therefore

    I_H(u,v) = S intersect I_G(u,v), for all u,v in S.

For u,v,w in S let x=a_G(u,v,w). Closure gives x in S. In geodetic G, the intersection of the u-v and u-w paths is exactly the u-x path. Intersecting with S and using the displayed interval identity yields

    I_H(u,v) intersect I_H(u,w) = I_H(u,x).

Hence x is also the H-apex, proving that H realizes precisely the restricted algebra. Every nonempty subalgebra therefore has an apiculate realization, as required.

This construction is intentionally not an induced-subgraph construction; omitted vertices may be contracted and new clique edges may arise.

## Audit cautions

- State finite, connected, simple, unweighted graphs explicitly.
- Do not call this a solution of the unrestricted characterization problem.
- Do not use 'C4 is not apiculate' as the obstruction; it is false.
- Do not require the witness subalgebra to be convex or isometrically embedded.
- In the odd-cycle step, isometry alone is insufficient in a general graph to exclude off-cycle shortest paths. Geodeticity supplies that exclusion here.
- The only external structural lemma used in this proof is the bridged triangle condition. The converse and all other steps are proved above.
