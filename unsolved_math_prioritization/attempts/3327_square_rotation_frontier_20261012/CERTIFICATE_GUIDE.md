# Independent checking guide: square orbits and signed rotations

This guide specifies exact semantic checks for the three complete authored certificates. It does not replace the full [co-Heawood proof](COHEAWOOD_GENUS_REPORT.md) or [structural proof](STRUCTURAL_REPORT.md).

## Reconstruct the graph

List the seven triples of nonzero vectors in F2^3 whose XOR is zero in lexicographic order. Label points p by p−1 and lines by 7 through 13. Join exactly the nonincident pairs. Check 14 vertices, 28 edges, degree four, and 21 distinct squares. Deletion removes (0,10). Contraction identifies 10 with 0, removes that edge, and has 13 vertices, 27 edges, three triangles and eighteen squares.

## Compact square-orbit proof

Read the [complete orbit certificate](COHEAWOOD_SQUARE_ORBIT_CERTIFICATE.json). Independently enumerate every unoriented graph square and compare its exact list. Enumerate all 168 independent ordered basis images of F2^3, reconstruct their point/line permutations, and verify that every induced square permutation comes from an actual graph automorphism.

For each triple of square indices, intersect the cyclic-link orders permitted by its corners at each vertex. At degree four the complete unoriented cyclic-order list has three elements. Regenerate the 84 forbidden triple masks and compare the full list. For these degree-four links, a required-pair graph extends to C4 exactly when it contains neither a three-star nor a triangle.

Check each level of canonical compatible-set orbit representatives, including level zero. Each representative must be the least mask in its full verified orbit, have the stated size, avoid every forbidden triple, and represent a disjoint orbit. For every representative and every absent square, inspect the extension. A bad extension must contain a forbidden triple; every good extension must map to a listed representative at the next level. Compare the exact next-level set, not only its cardinality. This gives induction over every compatible set. The level counts are 1, 1, 4, 14, 39, 83, 128, 119, 67, 17, 2, 0. The corresponding full-set counts are 1, 21, 210, 1246, 4725, 11655, 18438, 17874, 9765, 2604, 252, 0.

Thus eleven square faces cannot coexist. With bipartite face lengths at least four, 56≥6F−2f4 and f4≤10 imply F≤12, giving E≥4. The proof must reject omitted representatives, automorphisms or forbidden triples and altered squares even when no digest check is consulted.

## Exact embedding replays

Read the [N4 certificate](COHEAWOOD_N4_CERTIFICATE.json) and [deletion torus certificate](COHEAWOOD_DELETE_0_10_TORUS_CERTIFICATE.json). Validate the complete reconstructed graph vertex/edge sets, each neighbor rotation, and every ±1 edge signature. On signed darts (u,v,s), multiply s by sign(uv) to get t and move to (v,w,t), where w lies t positions after u in v's rotation. Pair opposite directed boundary orbits and verify total face-edge incidence 2m. Independently use three flag involutions or reconstruct the disk-and-band surface to confirm a closed connected surface.

For the original graph check ten quadrangles, one hexagon, one decagon, and χ=−2. Verify the certificate's negative cycle has sign product −1. The surface is N4, so ν≤4, establishing E=ν=4 with the preceding lower bound.

For the deletion check twelve quadrangles, one hexagon, and χ=0. Verify its sign potential p satisfies sign(uv)=p(u)p(v) on every edge. Its surface is orientable, hence the torus. This alone is not a proof that no Klein-bottle embedding exists.

## Deletion uniqueness and contraction exclusion

Enumerate every 12-element subset of the deletion's eighteen squares: 18,564 cases. At each vertex require distinct selected corners contained in an entire cyclic order on its incident edges. Exactly one subset survives. Its fourteen local orders are forced. Normalize each order modulo reversal; the facial square equation sign(vi,vi+1)=ti ti+1 then forces all 27 signatures. Compare these rotations and signs to the exact torus certificate. The sole normalized Euler-genus-two completion is orientable, excluding N2. Adding a crosscap to the torus establishes ν=3.

For the contraction enumerate both Euler-genus-two face profiles: 55,692 choices of two triangles and twelve squares; 43,758 choices of three triangles and ten squares. At the degree-six vertex test all sixty unoriented cyclic orders. Each degree-four vertex has three choices. No selection is corner compatible, so E≥3. The unspecified pentagonal face in the second profile need not be assumed simple. Nothing here decides between E=3 and E=4 for the contraction.

Required controls distinguish disconnected partial paths (allowed) from proper link cycles (disallowed), allow a whole degree-three triangular link, and reject a triangular proper link at degree four or six. Embedding controls reject missing or repeated edges, wrong graph geometry, invalid signatures, repeated rotation neighbors and false genus, face or orientability claims. Switching a vertex rotation and its incident signs must preserve the surface. All finite replays use explicit failures and run in normal, -O and -OO modes.

## Unbounded theorem boundary

The rotation-block surgery, exact-cover equivalence, strict alternation, and pentagon conclusions are proved in full prose. Finite signed-wheel and square-cover controls test their algebra and hypotheses; they are not exhaustive proofs for all graphs or all genera. The [independent audit](INDEPENDENT_AUDIT.md) states the accepted mathematical boundary.
