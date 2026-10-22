# An exact Klein-bottle embedding of K4,4

## Status and purpose

This is an authored finite embedding certificate in the first newly documented investigation of problem 3327 / OPG-172. It is not a solution of the unrestricted simultaneous-obstruction problem and makes no novelty claim. Together with the independently established triangle-free and minimum-degree-four conditions, it excludes targets with at most eight vertices. No complete-bipartite genus formula or obstruction catalogue is needed for this exclusion.

Let N_h be the closed nonorientable surface with h crosscaps, for h >= 1. Write nu(G) for the least positive h admitting an embedding; planar graphs therefore have nu = 1. The Euler genus of an individual orientable embedding is twice its orientable genus. These conventions are distinct.

## Complete signed rotation

The vertex classes are {0,1,2,3} and {4,5,6,7}; all sixteen cross edges and no others are present. The cyclic orders are:

- 0: (6,4,7,5)
- 1: (6,4,7,5)
- 2: (7,4,6,5)
- 3: (4,7,5,6)
- 4: (2,3,1,0)
- 5: (2,0,3,1)
- 6: (2,3,1,0)
- 7: (0,3,1,2)

The negative edges are 04, 07, 16, 17, 24, 27, 34, and 35. All other edges have positive signature.

A signed dart is (u,v,s), where uv is an edge and s is +1 or -1. To advance along a face, put t = s times the signature of uv, and replace the signed dart by (v,w,t), where w is t positions from u in the displayed cyclic order at v. Each geometric face has two opposite signed-dart boundary orbits.

The eight geometric faces, with boundary walks listed up to starting point and reversal, are:

1. (0,4,1,6)
2. (0,4,2,7)
3. (0,5,2,6)
4. (0,5,3,7)
5. (1,4,3,7)
6. (1,5,2,7)
7. (1,5,3,6)
8. (2,4,3,6)

These walks can be checked directly by the signed-dart rule. They use each edge twice in total. The signed rotation specifies vertex disks and edge bands; capping each boundary component with a disk gives a connected closed surface and a cellular embedding. Hence

  chi = 8 - 16 + 8 = 0.

The cycle (0,4,1,5,0) has signature product -1. Local choices of orientation at vertices change the signs on incident edges but do not change any cycle-sign product. An orientable ribbon surface would permit choices making all edge signatures positive, so this negative cycle proves nonorientability. The connected closed nonorientable surface with Euler characteristic zero is N_2. Thus K4,4 embeds in N_2.

For completeness, the usual elementary Euler inequality for a simple triangle-free graph embedded in the projective plane gives m <= 2n-2; K4,4 has 16 > 14 edges. Consequently nu(K4,4)=2. This lower bound is unnecessary for the small-order exclusion: the explicit N_2 upper bound already suffices.

## Small-order exclusion

Assume G is a target for simultaneous minor obstruction to N_h and N_(h+1), with h >= 1, and invoke the separately proved necessary conditions that G is triangle-free and has minimum degree at least four. There is an edge uv. Its endpoint neighborhoods N(u) and N(v) are disjoint by triangle-freeness, and each contains at least four vertices. Therefore |V(G)| >= 8.

If |V(G)|=8, the two neighborhoods partition V(G) into two independent four-vertex sets. Every vertex has at least four neighbors, so every possible cross edge is present. Hence G is K4,4. The certificate embeds this graph in N_2, and adding crosscaps disjoint from the graph embeds it in N_(h+1) for every h >= 1. This contradicts the target requirement.

Every target therefore has at least nine vertices. This argument is also a direct equality-case proof of the Mantel bound in the required special case.

## Exact verification and limits

The companion JSON records the complete rotations, edge signatures, negative cycle, and expected faces. A dependency-free replay independently forms all 64 flags and three fixed-point-free involutions: crossing an edge, crossing a vertex corner, and changing side on a half-edge. The relevant two-involution components count eight vertices, sixteen edges, and eight faces. Orientability is independently checked both by bipartiteness of the full flag graph and by connectivity of the signed orientation double cover. Both establish nonorientability.

Checks include sphere triangle and single-edge embeddings, a projective-plane triangle embedding, a toroidal K4,4 embedding, all eight single-vertex gauge switches, and six rejected malformed or false-claim certificates. The replay gives identical successful output under Python's normal, -O, and -OO modes; it uses explicit exceptions rather than assertions. A separate previously written signed-dart checker also verifies the same embedding.

The certificate was located by a deterministic local signed-rotation walk, with a declared bound of 200,000 proposals; the first certificate occurred at proposal 1,546. Repeating the discovery gives identical output. This search was constructive only and supports no nonexistence claim. No graph catalogue was searched, and no additional candidate was tested in this lane.

The reusable checker supports connected simple graphs with no isolated vertices. It verifies the surface of the supplied cellular embedding, not the graph's minimum genus. Its conditional h=2 face-profile arithmetic is also limited: if G has n vertices and m=2n or 2n+1 edges, and G-e has a cellular N_2 embedding with every face length at least four, then its total face excess over four is respectively two or zero. Excess two permits either one hexagonal face or two pentagonal faces; this is arithmetic, not a realizability proof.
