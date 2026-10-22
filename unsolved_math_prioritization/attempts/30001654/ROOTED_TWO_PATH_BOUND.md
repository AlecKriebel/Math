# A rigorous rooted lower bound for C5-semisaturation

Let G be a finite simple C5-semisaturated graph: each missing edge xy has a simple path of length 4 from x to y in G. Suppose that G has a vertex r such that every vertex other than r is the endpoint of a simple path of length exactly 2 starting at r.

Then

    e(G) >= 11(|V(G)| - 1)/8.

More precisely, if w is the number of nonleaf vertices outside N[r], then

    e(G) >= [11(|V(G)| - 1) + w]/8.

This hypothesis holds in the known 11/8 construction, but it is not proved for arbitrary C5-semisaturated graphs. Thus this is a rigorous restricted theorem, not a resolution of the general conjecture.

## Proof

Write N = N_G(r), W = V(G) minus (N union {r}), and a = |N|. The length-2-path hypothesis implies:

1. G[N] has minimum degree at least 1.
2. Every vertex of W has a neighbor in N.
3. Every leaf of G lies in W.

Let L be the leaves, l = |L|, W0 = W minus L, and w = |W0|. Different leaves have different supports: two leaves with the same neighbor cannot have a simple length-4 path between them. Let S subset N be their distinct supports, so |S| = l.

Every x in L is nonadjacent to r. Its required length-4 path begins x-y, where y is its support, and therefore gives a simple length-3 path from y to r. Let B subset S be the supports that do not start a simple length-2 path entirely inside G[N], and write b = |B|. For y in B, its length-3 path y-z-t-r has t in N and z in W0. In particular z has at least two neighbors in N, namely y and t.

We first show

    e(G[N]) >= 3(a+l)/8 - b/4.                         (1)

Check this component by component. Each connected component has order q >= 2. If q >= 4, it has at least q-1 >= 3q/4 edges, which is at least 3(q+s)/8 for any number s <= q of marked vertices. If q = 2, both vertices fail to start a length-2 path in the component, so its contribution on the right is 3(2+s)/8-s/4 = 3/4+s/8 <= 1. If q = 3, a triangle has three edges and easily satisfies the inequality. A 3-vertex path has two edges. For s <= 2, the right side without its negative correction is at most 15/8 < 2. For s = 3, its middle vertex belongs to B, and the right side is 18/8-1/4 = 2. This proves (1).

Partition W0 into U, whose vertices have exactly one neighbor in N, and V, whose vertices have at least two. Set u = |U|, v = |V|, and h = sum over z in V of |N_G(z) intersect N|. Then w = u+v and h >= 2v. The length-3 paths above associate each member of B with a distinct edge between B and V, so h >= b.

Every vertex of U has a neighbor in W0: it is not a leaf, is not adjacent to r, has exactly one neighbor in N, and cannot be adjacent to a leaf (all leaves have their sole neighbor in N). Consequently e(G[W0]) >= u/2. Therefore

    e(N,W0) + e(G[W0]) >= 3u/2+h
                            >= 3(u+v)/2 + b/4
                            = 3w/2+b/4.               (2)

The second inequality follows from 3h/4 >= 3v/2 and b <= h.

Counting all edges using (1) and (2),

    e(G) = a+l+e(G[N])+e(N,W0)+e(G[W0])
         >= 11(a+l)/8 + 3w/2
         = [11(|V(G)|-1)+w]/8,

as claimed.

## Additional observation

Under the same rooted hypothesis, if G has no leaves, then directly e(G[N]) >= a/2 and (2) with b=0 gives

    e(G) >= 3(|V(G)|-1)/2.

## Structural lemma without the rooted hypothesis

Let A consist of the supports of leaves that have degree 2 after all leaves are removed. Their 2-element neighborhoods in the leaf-deleted core are pairwise intersecting, since the required length-4 path between any two leaves gives a length-2 path between their supports.

A pairwise-intersecting family of 2-element sets either has a common element, or every member is one of {p,q}, {p,s}, {q,s} for three fixed vertices p,q,s. To see this, take intersecting distinct members {p,q},{p,s}. A member avoiding p must be {q,s}; once it exists, every other member belongs to this three-set family.

In the common-element case, write the common vertex as r. Then A is independent. Indeed, if y,z in A are adjacent, their core neighborhoods are {r,z} and {r,y}. There can be no simple length-3 path from y to r, whereas the missing edge from y's leaf to r requires one. Each y in A has its second core neighbor f(y) outside A and admits a simple path f(y)-t-r of length 2 avoiding y.

## Equality and one allowed leaf at the root

For graphs of order n>=5 in this rooted class, equality in e(G) >= 11(n-1)/8 forces w=0. Then b=0, and equality in the component estimate forces every component of G[N] to be a 4-vertex tree with all four vertices marked. The 4-vertex star has a marked center that does not start a length-2 path in G[N], so it is excluded. Consequently every component is P4, and every vertex of N has exactly one pendant leaf. Thus equality consists exactly of the known construction: one root joined to every vertex of disjoint P4 components, and one leaf at every P4 vertex. (Without an order restriction, the one-vertex graph K1 is the additional vacuous equality case.)

There is also a useful corollary. Suppose one leaf x is adjacent to r, and every vertex of G other than r,x is reachable from r by a simple path of length 2. Deleting x preserves C5-semisaturation, because a leaf cannot be an internal vertex of a path between remaining vertices. Applying the theorem to G-x gives

    e(G) >= 1 + 11(n-2)/8 = 11n/8 - 7/4.

The same w/8 improvement applies if w counts the nonleaf vertices outside N[r]. For n>=5, equality in this unstrengthened corollary forces G-x to be the construction just classified, with at least one P4 block. Without an order restriction, K2 is the additional vacuous equality case, since deleting its root leaf gives K1. This corollary is conditional on the stated rooted structure; it makes no claim that every semisaturated graph has such a root.
