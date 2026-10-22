# Why an arbitrary minimum rigidifying seed need not be globally optimal

This authored appendix is a partial obstruction, not a hardness proof or a claimed new approximation lower bound for every possible algorithm. This AI-assisted manuscript is unrefereed. Acceptance refers to the separate mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

Let G=K_{2,3}, with bipartition A={a,b} and B={x,y,z}. The objective remains minimum |S| such that G+K_S is generically globally rigid in the plane.

1. The minimum size of an ordinary-rigidifying clique is two. G has six edges on five vertices, fewer than the seven required for rigidity. Selecting T=A adds ab. The resulting graph is a Laman graph: start with ab and add x,y,z, each adjacent to a and b. Thus T is a minimum ordinary-rigidifying set.
2. The global pinning optimum is three. Each vertex of B has original degree two and must be selected in any feasible S, since vertices outside S receive no new edges and a globally rigid graph on at least four vertices has minimum degree at least three. Conversely, selecting B creates K5 with only ab missing. This is globally rigid: B is a triangle, and each of a,b is determined by its distances to the triangle's three generic, noncollinear vertices.
3. Every global completion constrained to contain the minimum seed T=A has size five. Such a completion must also contain all three vertices of B. It therefore equals all of V.

Consequently, the strategy “choose an arbitrary minimum ordinary-rigidifying set, then complete it optimally while retaining that set” can return five when the optimum is three. This does not contradict Király–Mihálykó's factor-two guarantee; it shows why their two-stage approximation cannot simply be relabeled an exact algorithm. Nor does it rule out a specially optimized first-stage choice: for example T'={x,y} extends to the optimal S=B.

The same gap persists at arbitrarily large order. Take m disjoint copies of K_{2,3}. The global optimum is 3m: all 3m degree-two vertices are forced, and their clique determines each of the 2m remaining vertices from three distances. The set T of all 2m degree-three vertices is an optimal ordinary-rigidifying set: its clique is rigid, and each remaining vertex is a two-neighbor zero-extension. For m>=2, fewer than two selected vertices in any original component would leave that component disconnected from the rest or attached through a single vertex, which is impossible for a rigid planar graph. The case m=1 was proved above. Retaining T in a global completion forces all 5m vertices. Thus this allowed choice in the two-stage strategy has ratio exactly 5/3.

## Additional five-vertex example

A diamond plus an isolated vertex gives another obstruction. Its ordinary optimum is three: the isolated vertex must be selected and two selected vertices can add only one edge to a five-edge graph, insufficient for rank seven; selecting the two degree-three vertices and the isolate gives the seven-edge Laman fan. Its global optimum is four: the two degree-two vertices and isolate are forced, but selecting those three leaves the original two-vertex separator; adding either degree-three vertex gives a globally rigid graph. Retaining the displayed ordinary seed forces all five vertices.

## Recorded supporting checks

The separate [staging audit](STAGING_AUDIT.md) records exact combinatorial checks of all 32 subsets for one copy of K_(2,3) and all 1,024 subsets for two copies. The ordinary/global/retained optimum triples were (2,3,5) and (4,6,10), with no failed assertions. These finite checks supplement the analytic all-m argument above. Programs and raw outputs are not distributed, and edition preparation did not rerun them.
