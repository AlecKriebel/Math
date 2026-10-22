# Third documented pass: complete small-order surface-frontier exclusion

Target: problem 3327 / OPG-172. This is part of the third newly documented substantive pass. The lifetime attempt count is unknown, and the unrestricted existence problem remains unresolved.

## Result and scope

**Finite theorem.** Let G be a connected simple quartic, triangle-free, K_(2,3)-free graph on at most15 vertices, with each edge in two or three squares. If every two-square edge belongs to at least four pentagons and every three-square edge belongs to at least two pentagons, then G has Euler genus two.

Consequently every h=2 simultaneous obstruction, and every ordinary Euler hopper of Euler genus four, has at least16 vertices. This uses the accepted necessary conditions from the first and second reports. It does not exclude higher orders, higher genera, or the orientably simple Euler-critical route. No example or minor-minimality claim is made. Three-connectivity is not needed by the enumeration: a larger class is exhausted.

The finite theorem is computer-assisted, with an explicit complete generation argument, exact search counts, a deterministic replay, adjacency certificates for every square-rich completion, and independently checked square-disk embeddings or bipartitions. Counts are of rooted labeled completions under the canonical root pattern below, not of isomorphism classes. No preexisting catalog, random search, graph-name lookup, isomorphism oracle, or failed embedding heuristic is used.

## 1. Complete root-pattern reduction

Choose any vertex r and label its four neighbors1,2,3,4. They are independent because G is triangle-free. Let W be the remaining n−5 vertices. To each w in W assign its label L(w)=N(w) intersect {1,2,3,4}.

- K_(2,3)-freeness applied to the pair r,w gives |L(w)|<=2.
- At most one w has any given two-element label {i,j}; otherwise i,j have the three common neighbors r and the two such vertices.
- Let P be the simple graph on {1,2,3,4} whose edges are the occurring two-element labels. Its degree at i is exactly the number of graph squares through ri. Thus every degree of P is2 or3.
- Therefore P is one of C4, K4 minus one edge, or K4, with p=4,5,6 edges, respectively. Relabeling the four neighbors gives one fixed representative of each type.
- Each i has three neighbors in W. Its two-element labels account for deg_P(i), so exactly3−deg_P(i) singleton labels {i} occur. This number is0 or1. The total number of singleton vertices is12−2p.
- The remaining z=(n−5)−p−(12−2p)=n+p−17 vertices have empty labels. They are precisely the vertices at graph distance at least three from r, or in a different component if connectedness is not imposed during generation. They are included, not silently discarded.

Thus every graph in the claimed class admits a labeling with exactly the initial adjacency used by the generator. Vertices having the same empty label are separately labeled, so no branch is removed by an unproved symmetry assumption. A negative z makes that root pattern impossible.

The only unknown edges are within W. A vertex with label of size k must acquire4−k such neighbors. Unknown edges are forbidden between intersecting labels by triangle-freeness; subsequent triangle and codegree checks enforce the same conditions globally.

## 2. Exact branching and sound pruning

The generator processes W vertices in increasing order. When it reaches i, all edges from i to earlier vertices are already fixed. If its residual degree is d, it visits every d-element subset of later vertices eligible for adjacency. Each chosen edge is individually checked for a triangle or a new pair of vertices with three common neighbors. These properties can never be repaired by adding more edges, so rejecting such a branch is sound.

Adding ij creates a triangle exactly when N(i) intersects N(j). The only codegrees that increase are those for pairs (j,x), x in N(i), and (i,y), y in N(j). Each increases by one; the code rejects an edge if one of these old codegrees is already at least two.

After each completed row, a necessary available-neighbor test is applied: every unfinished vertex must have at least its residual degree many later-or-unfinished vertices to which an individually legal edge could still be added. This ignores conflicts between future edges and is therefore an upper bound, not a claim that all individually legal choices coexist. If the bound is too small, no completion exists. The independent audit can omit this optimization.

At a leaf all vertices have degree four, and all simple-graph, triangle and codegree restrictions have been enforced. Every completion consistent with the root pattern occurs exactly once because its higher-numbered neighbor set fixes each row branch uniquely. Different root patterns or relabelings can represent isomorphic graphs; this does not affect completeness.

The completed graph is then checked for two or three squares at every edge. All such surviving adjacencies are retained. Pentagons are exhaustively enumerated, and the omitted-square exact-cover criterion from the accepted second report is tested. Every retained adjacency is also checked to be connected.

Orders below12 are already impossible: twelve nonbacktracking two-step walks from a quartic root require at least six outside vertices, since each receives at most two. Thus n>=11. At n=11 every vertex belongs to six squares, so the total vertex-square incidence66 would have to be divisible by four, a contradiction.

## 3. Exact finite counts

The columns below give: order n; root type p; completions before the all-edge square filter; survivors of that filter; certified Euler-genus-two survivors; zero-pentagon survivors.

| n | p | completions | square survivors | E=2 certificate | no pentagons |
|---|---|---:|---:|---:|---:|
|12|4|0|0|0|0|
|12|5|1|1|1|0|
|12|6|0|0|0|0|
|13|4|2|2|2|0|
|13|5|0|0|0|0|
|13|6|0|0|0|0|
|14|4|43|4|4|0|
|14|5|56|0|0|0|
|14|6|42|6|0|6|
|15|4|1464|24|24|0|
|15|5|1386|0|0|0|
|15|6|360|0|0|0|

There are3354 completed labeled graphs,37 square-filter survivors,31 certified square-disk surfaces of Euler characteristic zero, and six remaining graphs with no pentagons. The latter are directly verified bipartite and hence fail the accepted pentagon condition. Their previously known co-Heawood identity and genus/minor data are not needed or recomputed.

All31 covering survivors also pass the numerical pentagon filter. The specific retained square-disk certificates are orientable for19 survivors and nonorientable for12. These are types of the supplied surfaces, not assertions of the graphs' minimum nonorientable genera. The Euler-genus-two conclusion follows from the supplied surface and the quartic triangle-free density lower bound.

The complete deterministic search visits65625 recursive nodes and122723 combination branches, including immediately rejected branches. Per-pattern counts and complete square-rich graph adjacencies are in [ENUMERATION_CERTIFICATE.json](ENUMERATION_CERTIFICATE.json). That certificate also retains the adjacency and outcome of every square-rich leaf, without storing large failed search trees.

## 4. Human-readable order12 proof and witness

At n=12, the C4 pattern requires z=−1 and is impossible. The K4 pattern has six pair vertices and one empty-label vertex x. Every pair vertex needs two neighbors within W. Its only possibilities are its complementary pair and x; both are forced. This would give x six neighbors, contradicting quarticity.

For the five-pair pattern choose the missing label{1,2}. The labels of vertices5 through11 are, in order:

{1,3}, {1,4}, {2,3}, {2,4}, {3,4}, {1}, {2}.

Each pair vertex needs two W-neighbors and has exactly two allowed choices, forcing all its edges. The singleton degrees then force the entire graph. Its adjacency is:

0: 1,2,3,4
1: 0,5,6,10
2: 0,7,8,11
3: 0,5,7,9
4: 0,6,8,9
5: 1,3,8,11
6: 1,4,7,11
7: 2,3,6,10
8: 2,4,5,10
9: 3,4,10,11
10: 1,7,8,9
11: 2,5,6,9

It has15 squares. Omit the three squares(0,3,9,4), (1,5,11,6), and(2,7,10,8). They partition its twelve three-square edges. The other twelve squares supply a closed torus square-disk certificate, hence E=2. Its48 pentagons emphasize that pentagon richness alone is insufficient.

## 5. Certificate verification and boundaries

A separate verification harness reruns the complete generation and compares all exact outputs, then independently enumerates every survivor's squares and pentagons using vertex subsets and permutations rather than the generator's depth-first cycle enumeration. The publication payload contains this full mathematical generation argument, finite counts, exact graph certificates and verification metadata; executable discovery and checking programs are retained separately. It verifies adjacency, quarticity, triangle-freeness, codegrees, connectivity, exact-cover multiplicities, two disks per edge and a connected C4 link at every vertex. No bare solver exit code is treated as a genus certificate.

The six negative survivors are excluded by an independently verified bipartition and empty pentagon set; their failed exact-cover searches are auxiliary and not needed for the finite theorem. Four hostile certificate mutations must be rejected: duplicate adjacency, a missing omitted square, a false pentagon count, and a duplicated omitted square. Essential checks raise exceptions and do not rely on Python assertions. Normal, -O and -OO replays are required and recorded separately.

The mathematical dependencies are the [first structural report](../3327_surface_obstruction_reductions_20261012/STRUCTURAL_REPORT.md), [second square-selection and pentagon report](../3327_square_rotation_frontier_20261012/STRUCTURAL_REPORT.md), and [second independent mathematical audit](../3327_square_rotation_frontier_20261012/INDEPENDENT_AUDIT.md). No new external source was retrieved. No enumeration claim or count is supplied for order 16 or higher.

The result remains a finite lower bound. A future graph with no exact cover would only establish E>=3 until its actual embedding and all required deletions/contractions are certified. OPG-172 is not solved here.
