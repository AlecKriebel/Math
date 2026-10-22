# Turn 5: precolored series-parallel replacements and all cores of cycle rank at most four

## Purpose and final disposition

This final turn proves an exact boundary-coloring theorem for triangle-free two-terminal series-parallel networks. It promotes the K4 and prism results to whole networks replacing their edges, and removes the parallel-core caveat from turn 4's at-most-six-branch-vertices result.

In particular, the target holds for every triangle-free planar subcubic graph whose 2-connected blocks have cycle rank at most four. These are partial classes, not the full conjecture. Original 30004033 remains **unsolved after 5/5 substantive author turns**. There is no sixth author search in this packet.

No historical novelty is claimed. The five-color boundary lemma below is a self-contained special case of the terminal-intersection method in Goddard--Xu, *Fractional, Circular, and Defective Coloring of Series-Parallel Graphs*, JGT 81 (2016), 146-153, Theorem 2, first online 6 April 2015, DOI https://doi.org/10.1002/jgt.21868. The original author PDF is https://people.computing.clemson.edu/~goddard/papers/seriesParallel.pdf. Its full relevant theorem and proof were read. The deduction combining that boundary information with the core certificates is supplied explicitly here.

## 1. Exact network convention

A two-terminal series-parallel network has two distinct ordered terminals s,t and is constructed from a single edge by:

- series composition: identify the second terminal of one network with the first of another, with no other common vertex;
- parallel composition: identify corresponding terminals, with otherwise disjoint interiors.

Parallel edges in the construction cause no coloring difficulty; they impose the same disjointness constraint. Networks used inside a target simple graph inherit that graph's simplicity. All networks are finite and connected. In a replacement construction, different edge networks have pairwise disjoint interiors, and there are no extra edges between them. No claim is made for arbitrary choices of two vertices in a K4-minor-free graph without a two-terminal decomposition.

We first prove two terminal-precoloring types for a triangle-free network N:

- Type I: prescribed two-element subsets of {1,...,5} with intersection exactly one, permitted when s,t are nonadjacent;
- Type D: prescribed disjoint two-element subsets, permitted when there is no length-two s-to-t path.

These conditions are sufficient, not claimed to characterize every possible terminal intersection.

## 2. A self-contained (5,2) precoloring lemma

**Lemma 9.** Under the corresponding condition above, every prescribed terminal pair of type I or D extends to a (5,2)-coloring of N.

**Proof by the series-parallel construction.** A single edge only has type D, which is immediate. In a parallel composition, absence of a terminal edge, or absence of a two-edge terminal path, is inherited by every piece. Apply the same type and fixed terminal sets to each piece; their interiors are disjoint.

Consider a series composition N=N_1(s,u) followed by N_2(u,t). For each child, request type D if its terminals are adjacent and type I otherwise. An adjacent pair in a triangle-free child cannot have a length-two path, so every requested child type is legal. For the composite type I there is no additional exclusion. For composite type D, the children cannot both have adjacent terminals, because the two edges through u would be a forbidden length-two s-to-t path.

It remains to choose the two-set at u. By permuting the five colors, the endpoint pair can be put in either canonical form below. Here the child types are ordered left,right.

| Composite type | s-set | t-set | Child types | u-set |
| --- | --- | --- | --- | --- |
| I | 12 | 13 | D,D | 45 |
| I | 12 | 13 | D,I | 34 |
| I | 12 | 13 | I,D | 24 |
| I | 12 | 13 | I,I | 14 |
| D | 12 | 34 | D,I | 35 |
| D | 12 | 34 | I,D | 15 |
| D | 12 | 34 | I,I | 13 |

Every row has exactly the requested intersections. The missing D with D,D case is precisely the prohibited two-edge path. Apply induction to both children with this common u-set. This verifies every construction case and proves the lemma for arbitrary finite networks. QED.

In particular, if the terminals are adjacent, triangle-freeness permits type D; if they are nonadjacent, type I is available. No general graph-wide bound is being used as an unproved precoloring theorem.

## 3. Adding a proper three-coloring gives the exact eight-color boundary

Every two-terminal series-parallel network admits a proper three-coloring with any prescribed **distinct** terminal colors. If its terminals are nonadjacent, it also admits one with any prescribed **equal** terminal color.

For completeness, this follows directly from the construction. A single edge permits distinct colors. In a parallel composition apply the same terminal prescription to each child; a missing terminal edge is missing from each child. In a series composition choose the middle color different from both prescribed endpoint colors (or just different from their common color). Each child then has distinct terminal colors, so induction applies. This argument does not require triangle-freeness.

Use colors 1,...,5 for Lemma 9 and separate colors 6,7,8 for this proper coloring. Assign each vertex the union of its two-set and its single three-color label. This is an (8,3)-coloring. It gives:

**Theorem 10 (network boundary theorem).** For any finite triangle-free two-terminal series-parallel network:

- if s,t are adjacent, every prescribed pair of disjoint triples from {1,...,8} extends;
- if s,t are nonadjacent, every prescribed pair of triples with intersection exactly one or exactly two extends.

For the first statement, combine type D with distinct proper colors. For the second, combine type I with distinct proper colors to get intersection one, or equal proper colors to get intersection two. Initially this produces some terminal triples. Any two ordered pairs of triples with the same intersection size are carried to one another by a permutation of the eight colors: match their intersection, two differences and common complement. Apply that permutation to the whole coloring. This proves the word **every**, which is needed for gluing.

## 4. K4 and prism edges may be replaced by entire networks

**Theorem 11.** Suppose a graph G is obtained from K4 or the triangular prism by replacing each core edge with a two-terminal series-parallel network, subject to the convention in Section 1. If G is triangle-free, it has an (8,3)-coloring.

**Proof.** On the core, let H consist of those pairs for which the corresponding network contains a direct edge between its terminals. H is triangle-free, because its edges also occur in G. Each individual network is triangle-free as a subgraph of G.

Use the seven-template K4 table of turn 3 or the complete prism certificate of turn 4. Core pairs in H receive disjoint triples; all other core-edge pairs receive intersection one or two. Theorem 10 extends those exact branch triples through each edge network. Their interiors are disjoint and there are no extra edges, so the colorings combine. QED.

This covers unbounded network size and unbounded network cycle rank. It does not cover arbitrary attachments to a core subgraph, shared internal vertices between different edge replacements, arbitrary treewidth-three graphs, or all cubic planar graphs. If one wants a member of the original subcubic class, the resulting graph must still have maximum degree at most three; the theorem itself does not silently guarantee that for arbitrary replacements.

## 5. Parallel cubic cores with at most six vertices

We now finish the small-core case left explicit in turn 4. Let G be 2-connected and subcubic, with at least one degree-three vertex. Suppressing maximal degree-two paths gives a connected cubic multigraph K with no cutvertex. It has no loops: a loop would come from a cycle attached through one degree-three vertex, whose third incident edge would lead to the rest of the graph and make that vertex a cutvertex. Parallel edges are retained.

If K has two vertices, its three parallel edges give a theta network. It is series-parallel, as is every subdivision of it.

For four or six vertices, suppose K has parallel edges ab. Their multiplicity is exactly two: three would isolate a,b from every other vertex. Let ax and by be their remaining incident edges. The vertices x,y are distinct. If x=y, that vertex's third edge leads to the remaining vertices, making it a cutvertex.

Remove a,b and add a new edge xy, obtaining K'. It is loopless, cubic and connected, and has no cutvertex. Here is the last point in detail. For a remaining vertex v different from x,y, replace any use of the a,b gadget in a path of K-v by the new edge; connectivity is preserved. When v=x, the a,b gadget in K-x attaches only at y and cannot connect two otherwise separate remaining pieces. Deleting that pendant gadget leaves the remaining graph connected. The case v=y is identical. Thus K'-v is connected for every remaining v.

With four original vertices, K' has two vertices and three parallel edges. Equivalently K itself has two opposite doubled edges and two single cross edges. It is an explicit two-terminal series-parallel graph: between a,b take their two parallel edges and, in parallel, the series route a-x, the doubled x-y edge, y-b.

With six original vertices, K' has four vertices. If K' is simple it is K4. Recovering K means replacing its newly added xy edge by the series-parallel network x-a, two parallel a-b edges, b-y. Subdividing any of these edges keeps that replacement series-parallel. Thus G belongs to Theorem 11's K4 network-replacement class.

If K' is not simple, it has the explicit four-vertex series-parallel form just described. Replacing any edge leaf in a series-parallel construction by a series-parallel network preserves the construction. Hence K, and then its subdivision G, are series-parallel. Lemma 9 supplies a (5,2)-coloring for a suitable two-terminal construction of the resulting triangle-free graph; alternatively the credited Goddard--Xu graph theorem gives the same bound.

Finally, if a six-vertex K has no parallel edges, turn 4's complement classification gives the prism or K_(3,3). Planarity excludes K_(3,3). The simple four-vertex case is K4. This exhausts all connected loopless cubic cores with at most six vertices and no cutvertex; no parallel-edge case is discarded.

## 6. Consequence in terms of cycle rank

**Corollary 12.** Every triangle-free planar subcubic graph whose 2-connected blocks have cycle rank at most four is fractionally 8/3-colorable. In particular this holds for every connected graph in the target class with cycle rank at most four.

For a connected graph, cycle rank means |E|-|V|+1. Subdivision preserves it. A non-cycle 2-connected subcubic graph with b degree-three branch vertices has a cubic core with 3b/2 edges, hence cycle rank b/2+1. Rank at most four is therefore equivalent to b<=6. Section 5 and the core results prove the required coloring for every such block; a cycle is handled directly. Blocks glue at single vertices, where equal-size color sets can be matched by palette refinement/permutation. Bridges and isolated vertices are harmless. Cycle rank is additive across blocks, so the stated whole-graph special case follows.

As a necessary condition, a smallest counterexample to the original conjecture would consequently have at least eight degree-three vertices and cycle rank at least five, in addition to the earlier chain and K4+ exclusions. This does not assert that eight-branch-vertex cores are counterexamples, or that the general source conjecture is false.

The weighted conclusion is exact: the resulting fractional coloring is a probability distribution on independent sets with every vertex marginal at least 3/8. It gives an independent set of weight at least 3/8 of the total for every nonnegative weight assignment.

## 7. Checks and final limitation

`turn5/check_networks_and_cores.py` is a constructive exact checker. It verifies the seven local five-palette choices for all prescribed endpoint pairs; builds colorings for all triangle-free ordered binary series-parallel expressions through five edge leaves; and enumerates loopless cubic multigraphs on two, four and six vertices to check the written classification. Its 1,980 assertions include 273 constructed network colorings. The multigraph enumeration has 1, 10 and 760 total labeled graphs at those sizes, with 1, 7 and 550 connected no-cutvertex cases. Among the six-vertex cases, ten are the excluded K_(3,3) cores, sixty are prisms, 180 reduce to K4 edge networks and 300 to series-parallel cores.

These finite controls supplement the all-network induction and analytic classification; they are not evidence for larger cores. The universal prism theorem also uses turn 4's complete finite positive certificate. Neither solver heuristics nor sampled numerical signs are a proof dependency.

No full proof for general larger cubic planar cores has been obtained, and no graph counterexample has been found. **Original status: unsolved 5/5.** Current subjective full-target completion estimate: 25%, low confidence. The exact remaining gap is the full weighted inequality for arbitrary triangle-free planar subcubic graphs outside the proved core/network classes. Freeze this packet for an independent full source/proof audit; do not add a sixth author search.
