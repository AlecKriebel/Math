# Small explicit mathematical examples

These are small illustrations, not exported datasets or original case streams. They are independently checked from the descriptions below. They do not exhibit a k>=3 indivisible graph or a forcing separator side.

## Equality join

The five-cycle on vertices 0,1,2,3,4 has edges {0,1}, {1,2}, {2,3}, {3,4}, {0,4}. Add a universal vertex 5 adjacent to all five. This K1 join C5 has (n,q,r)=(6,4,3), giving n=2q-r+1. The five-cycle itself has (5,3,2). The equality classification concerns the whole graph, not just an induced five-cycle.

## Seven-antihole

On vertices 0 through 6 take every pair except consecutive pairs of the cycle 0,1,2,3,4,5,6,0. The resulting complement of C7 has (n,q,r)=(7,4,3), has no induced C5 and attains n=2q-r+2. It does not witness sharpness for the forcing-side large chromatic gap.

## Mixed triangle and repeated edges

The three size-two edges {0,1}, {1,2}, {0,2} with demands B,B,B are unsatisfiable. Replace the last demand by 0, meaning not all color 0: the coloring (1,0,1) satisfies the demands. Replacing it by 1 is satisfied by (0,1,0). Two labelled copies of {0,1} with opposing one-sided demands 0 and 1 are simultaneously satisfied by (0,1); the repeated pair is not an odd-cycle obstruction.

## Abstract sharpness at rank three

Let P={0,1}, V={2,3,4}, and take edges {0,1,2}, {0,1,3}, {0,1,4}, {2,3,4}. The fixed all-red P forces V all blue and fails. The unrestricted coloring (0,1,0,0,1) satisfies every edge. Each vertex of V has incidence two, and the shadow is K5. The four listed triples cannot all be maximum triangles of a graph with that shadow.

## An almost-monochromatic K4 boundary

Take maximum cliques {0,1,2,3} and {0,1,2,4}, with all pairs from those cliques and no others. On boundary {0,1,2,3}, prescribe colors (0,0,0,1). The common neighborhood of P={0,1,2} is F={3,4}; it is stable, and both its vertices are forced to color 1. Thus (0,0,0,1,1) extends. Every vertex outside the boundary has maximum-clique incidence one. This explicitly illustrates the k-1 branch of the clique-boundary proof.

## Why a nonclique boundary needs the stronger hypothesis

Take the four maximum triangles {0,1,2}, {0,3,4}, {1,5,6}, {2,7,8}, with every pair from these triangles and no other edges. Boundary P={3,4,5,6,7,8} is not a clique. Prescribing all of P color 0 forces 0,1,2 all color 1, which fails on the central triangle. Every vertex outside P has maximum-clique incidence two. This does not contradict clique-boundary flexibility: P is not a clique. Nor does it satisfy the core criterion, because prescribed P contains monochromatic (k-1)-cliques. The graph itself is divisible, for example by (0,0,1,0,1,0,1,0,1).

## Numerical frontier at k=4

The unrestricted indivisible-order barrier is 3k=12. Each minimal-indivisible clique-cutset side also needs at least 12 vertices. Two sides sharing an edge therefore need at least 12+12-2=22 vertices. For any nonempty clique cutset of size s<=4 and t>=2 components, s+t(12-s)>=20. Core necessary conditions in this third pass are |X|>=6, chi(G[X])>=5 and omega(G[X])>=3, with X not a clique; induced minimality strengthens only the last inequality to omega(G[X])=4. No stronger subsequent-pass core-order bound is claimed here.
