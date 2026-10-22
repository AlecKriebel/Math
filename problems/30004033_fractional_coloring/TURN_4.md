# Turn 4: all triangle-free triangular-prism subdivisions

## Purpose and disposition

The four-branch-vertex construction leaves larger cubic planar cores. This turn treats the next simple cubic planar core, the triangular prism, with a complete finite certificate for its endpoint-color constraints and an all-length extension proof. It proves an (8,3)-coloring for **every triangle-free subdivision of the triangular prism**, including arbitrary path lengths and parities. This is not a graph-order-limited search.

Combined with turn 3, it covers every 2-connected triangle-free subcubic graph whose suppressed degree-three core is simple and has at most six vertices, and graphs built from such blocks by gluing at cutvertices. It does not cover arbitrary larger or parallel-edge cores. Original target remains unresolved, 4/5 substantive author turns. No historical novelty is claimed.

## 1. The core and the exact finite statement

Label the prism's vertices 0,...,5, with triangles 012 and 345 and matching edges 03,14,25. Use this exact edge order:

    01,02,12,34,35,45,03,14,25.

For a positive-length edge subdivision, let H contain precisely the prism edges left unsubdivided. Triangle-freeness of the subdivision implies that H has neither core triangle. Conversely, those are the only possible 3-cycles: a cycle using a genuinely subdivided edge has length at least four unless a shorter core cycle existed. The prism has no other triangles. Thus exactly

    (2^3-1)^2 * 2^3 = 392

labeled masks H are possible.

**Finite certificate claim.** For every one of these masks, there are triples C_0,...,C_5 from {1,...,8} such that, for each prism edge ij,

    |C_i intersect C_j| = 0       if ij is in H,
    |C_i intersect C_j| in {1,2}  otherwise.                 (1)

Only the nine core-edge pairs are constrained; there is no asserted condition on the other six pairs.

## 2. The complete certificate and verifier

`turn4/prism_certificates.json` contains an explicit list of six triples for each of the 54 symmetry orbits of the 392 masks. It is the positive mathematical certificate. The discovery code `explore_prism.py` is not trusted for exhaustiveness or feasibility by the verifier.

The standalone exact verifier `verify_prism.py` does the following:

1. Enumerates all 720 permutations of six vertices and retains precisely the 12 preserving the prism edge set
2. Independently tests each of the 512 edge masks for a triangle by checking every three-vertex subset, giving exactly 392 valid masks
3. Defines a mask's canonical representative as its least integer image under these 12 automorphisms, giving exactly 54 representatives
4. Checks that the certificate contains exactly one palette assignment for each representative, with no missing or extra representative
5. Verifies the cardinality, palette membership and all nine intersection constraints for every representative assignment
6. For every one of the 392 labeled masks, finds an automorphism carrying its representative to it, transports the palette triples, and verifies all nine constraints again

All operations use finite sets and exact integers; there is no floating-point tolerance, LP status, SAT status or sampling assumption. This is a full finite proof of (1), encoded as a checkable certificate. The checker passes 7,086 assertions. Its orbit reduction is only compression: it reconstructs and checks every labeled case explicitly.

The discovery routine used arc consistency and a small deterministic backtracking search over the 56 palette triples, fixing the first triple by global color symmetry. It found positive assignments for every orbit in 320 search nodes. This node count is provenance, not a substitute for the independent standalone verifier. The fixed certificate does not depend on its running time.

## 3. Arbitrary subdivision lengths

**Theorem 8.** Every finite triangle-free subdivision of the triangular prism has an (8,3)-coloring.

**Proof.** Form H as in Section 1 and assign the six branch triples from the certified instance of (1). A length-one path has disjoint endpoints. Every replacement path of length at least two has endpoint intersection one or two. The exact integer path-extension theorem proved in turn 3 therefore extends its endpoints along its actual length. The nine paths have mutually disjoint interiors and their only common vertices are the already prescribed branch vertices. Combining the extensions gives an (8,3)-coloring of the whole subdivision. QED.

Choosing one of the eight colors uniformly gives an independent set containing every vertex with probability 3/8. Therefore the theorem proves the universal weighted independent-set inequality on this class, and not merely the uniform-weight bound.

Theorem 8 does not claim that a graph containing such a subdivision as a subgraph is colorable: additional edges or attachments may impose constraints absent from the certificate. It makes no assertion that the bound is sharp on the prism-subdivision subclass.

## 4. A core-size consequence, with its exact restriction

Let G be a 2-connected triangle-free subcubic graph. If every vertex has degree two, G is a cycle, already covered in turn 1. Otherwise suppress every maximal path whose internal vertices have degree two. The resulting connected cubic multigraph K is the degree-three core. This operation may create parallel edges; they cannot be discarded or silently replaced by a simple graph.

Suppose specifically that K is simple and has at most six vertices. The number of vertices is even, because its degree sum is three times the number of vertices. A simple cubic graph needs at least four vertices.

- With four vertices, K is necessarily K4.
- With six vertices, its complement is a simple 2-regular graph. Such a graph is either a 6-cycle or two disjoint triangles. The complement in the former case is the triangular prism; in the latter it is K_(3,3). The latter is nonplanar: a simple bipartite planar graph on six vertices has at most eight edges, whereas K_(3,3) has nine.

Since suppression preserves planarity, the only possible simple cores are K4 and the triangular prism. Turns 3 and 4 therefore prove the target for G. The colorings also glue over cutvertices (by matching the fixed vertex's color set), so the same conclusion holds for graphs whose nontrivial 2-connected blocks have this property or are cycles; bridges and isolated vertices pose no problem.

The restriction that K be simple is essential to this deduction. A small cubic **multigraph** core may have parallel paths whose boundary demands interact. It has not yet been classified here. Likewise a simple cubic planar core with eight or more branch vertices is outside the finite certificate. No maximum order is claimed for the subdivision graphs themselves; their paths can be arbitrarily long.

## 5. Remaining route

A useful final-turn direction is to understand series-parallel two-terminal edge replacements and the parallel-core cases, while preserving the exact precoloring requirements. Existing series-parallel fractional-coloring theorems must be used with their terminal hypotheses, not just as a graph-wide chromatic bound. Even a successful replacement theorem would leave general larger simple cubic planar cores unresolved.

Original target: unresolved 4/5. Current subjective full-target completion estimate: 22%, low confidence. This is a research estimate, not a mathematical fraction proved. All earlier frozen proof bytes and their qualifications remain unchanged.
