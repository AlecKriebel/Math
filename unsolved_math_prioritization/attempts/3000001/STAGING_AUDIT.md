# Independent audit of the staging obstruction

Date: 10 October 2026. Problem: 3000001 / AMR-029-0001.

## Verdict and identity

**Accepted.** This is a correct obstruction to choosing an arbitrary minimum ordinary-rigidifying set and then optimizing global completion subject to retaining it. It does not prove hardness or a worst-case lower bound for every possible first-stage choice.

The distributed [staging appendix](STAGING_OBSTRUCTION.md) is 3,793 bytes, SHA-256 `f8046e159aaa20177b3342325eb948a18c9b114a6a0ca90733c9393418448703`. All analytic arguments from the accepted appendix are preserved, and the additional diamond example below is reproduced in it. This is a separate acceptance; it does not modify or broaden the main proof's acceptance. This AI-assisted manuscript is unrefereed. Acceptance refers to the separate mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

## Mathematical check

For G=K_(2,3), with degree-three part A of size two and degree-two part B of size three, G has six edges, below the rank seven required for rigidity on five vertices. A singleton pin set changes no edge. Adding the missing edge on A gives a Laman fan, so the minimum ordinary-rigidifying cardinality is two.

Every globally rigidifying set must contain all of B, because a vertex outside the selected clique retains its incident edges and global rigidity on five vertices requires minimum degree three. Selecting B is sufficient: it gives a triangle on B, and each remaining vertex has distances to its three generic noncollinear vertices. After a congruence aligns the triangle, those three distances uniquely determine either remaining vertex. Therefore the global optimum is exactly three.

If the chosen first-stage set is A, the retained seed and the three forced vertices are disjoint and together are all five vertices. Thus every feasible retained-seed completion has size five, and selecting all five certainly suffices. The alternative two-element seed consisting of two vertices of B really is an ordinary-rigidifying seed: K_(2,3) plus that edge has seven edges and obeys every Laman sparsity inequality. It extends to B, so the appendix correctly avoids a claim that every minimum first stage incurs the obstruction.

For m disjoint copies, all 3m degree-two vertices remain forced. Selecting them gives a complete pin clique and locates each of the remaining 2m vertices from three generic noncollinear neighbors inside the clique. Hence the global optimum is exactly 3m.

The union T of all degree-three parts has 2m vertices. Its clique is rigid, including the K2 base when m=1. Every other vertex can be added by a two-neighbor zero-extension, proving that T rigidifies the graph. For m>=2, a pin set using zero vertices in an original component leaves that component disconnected. A pin set using exactly one vertex in that component attaches its other four vertices to the rest only through the selected vertex. This is a cut vertex and is incompatible with generic planar rigidity. Equivalently, the component can undergo a nontrivial rigid motion fixing its lone selected vertex, while the other components remain fixed. Thus at least two vertices from every original component must be selected, proving the ordinary optimum 2m. The m=1 case was handled separately.

Any globally rigidifying set retaining T must also contain all 3m forced degree-two vertices, so it contains all 5m vertices. The exact ratio for this allowed staged choice is therefore 5/3 at arbitrarily large orders. This is compatible with the credited factor-two approximation and does not imply a hardness result.

The additional diamond-plus-isolated-vertex observation is correct as well. Its ordinary optimum is three: the isolated vertex must be selected and two selected vertices can add only one edge to a five-edge graph, insufficient for rank seven; selecting the two degree-three vertices and the isolate gives the seven-edge Laman fan. Its global optimum is four: the two degree-two vertices and isolate are forced, but selecting those three leaves the original two-vertex separator; adding either degree-three vertex gives a globally rigid graph. Retaining the displayed ordinary seed forces all five vertices.

## Recorded independent computation

The independent audit records execution of a separately written verifier. It checks all 32 subsets for the one-copy graph and all 1,024 subsets for the two-copy graph. Rigidity ranks use the combinatorial Laman matroid with every vertex-subset sparsity constraint. Global rigidity uses exhaustive vertex cuts and exact ranks after every edge deletion. No floating-point or random matrix rank is used.

The reproduced ordinary/global/retained optimum triples are respectively (2,3,5) and (4,6,10), with no failed assertions. Both the displayed first-stage seed and displayed optimal global pin set were independently checked. These computations support but do not replace the analytic proof for all m. Programs and raw outputs are not distributed, and edition preparation did not rerun them.

No required correction was found. No novelty, full-problem resolution, or unrestricted approximation lower bound is certified. The edition distributes the complete analytic argument and aggregate verification metadata.
