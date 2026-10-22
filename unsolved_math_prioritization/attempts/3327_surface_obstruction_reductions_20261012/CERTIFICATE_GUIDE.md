# Independent checking guide for the two finite certificates

The certificates are small authored mathematical objects. Neither is a witness for the original simultaneous-obstruction problem. The checks below specify exact finite tasks and do not depend on trusting a search-program exit code.

## K4,4 on the Klein bottle

Read [the full certificate](K44_N2_CERTIFICATE.json) and [the proof](K44_N2_PROOF.md). Check that its vertex classes are disjoint sets of four vertices, that its sixteen distinct signed edges are exactly their cross pairs, and that each cyclic order lists each neighbor exactly once. Each edge sign must be +1 or −1.

Form the 64 signed darts (u,v,s), where uv is a directed edge and s∈{−1,+1}. Given one such dart, multiply s by the edge signature to obtain t, then move to (v,w,t), where w lies t positions from u in the cyclic order at v. This successor is a permutation. Enumerate every orbit, pairing the two opposite boundary orbits of each geometric face. Check that all 64 darts occur exactly once and that the geometric face walks, up to cyclic shift and reversal, are precisely the eight listed four-cycles.

Count V=8, E=16, F=8, so χ=0. Check the sign product around 0,4,1,5,0 is negative. A negative cycle forbids an orientation choice making every edge band positive. The connected ribbon surface, capped at its boundary circles, is consequently a connected closed nonorientable surface of Euler characteristic zero: N_2. An embedding certificate proves an upper bound; the independent elementary projective-plane density bound establishes the optional matching lower bound in the proof.

For an independent alternative, use flags (v,w,s) with three involutions: edge crossing (v,w,s)↦(w,v,−s·signature(vw)); corner crossing (v,w,s)↦(v,rotation_v[index(w)−s],−s); side crossing (v,w,s)↦(v,w,−s). Two-involution components count vertices, edges and faces, respectively. Check that each involution is fixed-point-free and that the full flag graph is connected. Its failure to be bipartite is another orientability check. These independent conventions give the same eight faces.

Changing the orientation at a vertex reverses its cyclic order and switches all incident edge signs. Such a gauge change must preserve faces and surface type. Sphere, projective-plane and torus controls distinguish genus from orientability. Malformed rotations, missing or repeated edges, invalid signs, and false face-count or orientability claims must be rejected.

## Co-Heawood: no seven-square edge partition

Read [the full certificate](COHEAWOOD_SQUARE_CERTIFICATE.json). Reconstruct the seven Fano lines as distinct sorted triples {a,b,a xor b}, for 1≤a<b≤7. Vertices 0 through 6 represent points 1 through 7; vertices 7 through 13 represent those lines in lexicographic order. Include an edge exactly when the point is not on the line. This determines 14 vertices and 28 edges.

Independently enumerate all simple length-four cycles, identifying cyclic shifts and reversals. Compare the complete list of 21 squares and each square's four-edge bit mask with the certificate. Check degree four, triangle-freeness, at most two common neighbors for every vertex pair, and exactly three squares through each edge.

An Euler-genus-two embedding would have 14 distinct square faces by Euler's formula and degree four. The seven omitted squares would partition the 28 edges. To rule this out, inspect the complete 11-node search tree. At each node recompute the remaining-edge mask and the chosen squares. Among remaining edges, select the one with the fewest eligible squares, with the edge index breaking ties. A square is eligible exactly when all its four edges remain. The child list must include exactly one child for every eligible square, removing that square's edges and appending its index. A dead leaf must have an uncovered edge with no eligible square. All node indices must be reached exactly once, with no missing or extra node, and no remaining-edge-zero success leaf may occur.

The root starts with all 28 edges. Any seven-square partition must follow one of these exhaustive branches. Every branch fails. As an independently structured check, enumerate all 116,280 seven-element subsets of the 21 squares and test whether every edge occurs exactly once; the count of valid partitions is zero.

This proves E≥3 for this graph only. It neither proves E=4 nor supplies an N_3 embedding, an obstruction certificate, or a global theorem that mixed two/three-square graphs admit quadrangulations. The exact N_3 embedding question was not tested here.

## Scope of replay

Both complete finite certificates were replayed independently with explicit failure conditions. The mathematical results are unchanged by Python's normal, -O and -OO modes. The public proof and this guide permit independent implementations; scripts, search logs and private preservation records are outside this prose edition. Replaying a finite certificate does not independently re-prove every cited classification or the universal structural arguments.
