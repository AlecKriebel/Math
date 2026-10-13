# A sharp lower bound for the universal-core subclass of C5-semisaturated graphs

Problem 30001654 / OWR-4791-010. Authored first-attempt partial result, 2026-10-10 UTC.

## Scope and main distinction

A finite simple graph is C5-semisaturated if adding any missing edge creates a new copy of C5. Equivalently, the endpoints of every nonedge are joined in the original graph by a simple path of length exactly four. Existing C5 copies are allowed.

The assigned conjecture is ssat(n,C5)=11n/8+O(1). The theorem below proves its lower bound only in a specified subclass. It does not solve the assigned conjecture. A construction below also disproves a stronger optional eventual-equality suggestion in the inspected arXiv:1103.0067v1 of Füredi–Kim, Conjecture 4.1, without contradicting their asymptotic conjecture.

## Theorem

Let G be a C5-semisaturated graph of order n>=5. Let L be the set of vertices whose degree in G is one, and let H=G−L, deleting the original leaves once. Assume H has a universal vertex r. Put epsilon=1 if r is adjacent in G to a leaf and epsilon=0 otherwise. Then

    8e(G) >= 11n − 11 − 3epsilon.

In particular, e(G)>=(11n−14)/8. Equality in the displayed, epsilon-dependent bound holds if and only if G has the following form, for some integer t>=1:

1. Start with t disjoint copies of the four-vertex path P4.
2. Add a vertex r adjacent to every path vertex.
3. Attach exactly one new leaf to every path vertex.
4. If epsilon=1, attach one additional leaf to r.

The two equality families have (n,e)=(8t+1,11t) and (8t+2,11t+1), respectively. The first is the known Füredi–Kim construction. Equality in the weaker bound 8e(G)>=11n−14 occurs precisely for the second family.

## Preliminary facts and deletion convention

G is connected: otherwise adding an edge between components cannot create a cycle. Thus n>=5 implies no isolated vertices.

Distinct leaves have distinct neighbors. Indeed, a simple path between two leaves with the same neighbor can only have length two, whereas their missing edge requires a path of length four.

Every leaf support has degree at least three in G. If leaf x has neighbor v and N_G(v)={x,w}, the nonedge xw has no simple path of length four, since every path starting at x must next visit v and then w.

Consequently H has minimum degree at least two: vertices not supporting leaves retain degree at least two, and each support loses exactly one edge from an original degree at least three. No further leaves appear after this deletion. Hence in this setting deleting the original leaves once agrees with iterative deletion of leaves (and gives the usual nonempty 2-core).

Write F=H−r and q=|V(F)|. Let S be the vertices of F supporting leaves, with s=|S|. Each vertex supports at most one leaf, so |L|=s+epsilon and s<=q. Since r is universal in H and delta(H)>=2, every vertex of F has positive degree in F. The counts are

    n=q+s+1+epsilon,
    e(G)=q+e(F)+s+epsilon.

## Local constraint on marked vertices

Every v in S begins a simple two-edge path in F. To see this, let x be its attached leaf. The edge xr is missing. A simple four-edge path from x to r must have the form x,v,a,b,r. Its internal vertices cannot be leaves. Simplicity excludes r from {v,a,b}, so v,a,b belong to F and va,ab are edges of F.

## Component inequality

For every connected component C of F, let k=|V(C)|, a=|S intersect V(C)| and f=e(C). We prove

    8f >= 3(k+a),

with equality precisely when C is a P4 and all four of its vertices lie in S.

There are no one-vertex components, since delta(F)>=1.

If k=2, the component is a single edge. Neither vertex begins a simple two-edge path inside F, so a=0. Thus 8f=8>6=3(k+a).

If k=3 and C is a path, only its two endpoints begin a simple two-edge path, so a<=2. Hence 8f=16>15>=3(k+a). If it is a triangle, 8f=24>18>=3(k+a).

If k>=4, connectedness and a<=k give

    f >= k−1 >= 3k/4 >= 3(k+a)/8.

For equality throughout, k=4, f=3 and a=4. The component is a four-vertex tree all of whose vertices begin a simple two-edge path. Of the two four-vertex trees, the center of K1,3 does not have this property; therefore C=P4. Conversely a fully marked P4 gives equality.

Summing over components yields 8e(F)>=3(q+s), with the asserted equality classification.

## Completing the lower bound

The vertex and edge counts give

    8e(G)−11n = 8e(F)−3(q+s)−11−3epsilon >= −11−3epsilon.

Equality implies exactly the described graph form. It remains necessary to verify that both classified families actually are semisaturated; necessity alone would not suffice for an equality characterization.

## Full nonedge verification for both families

Write one path as a−b−c−d, with leaf x* attached to each path vertex x, and let r be the common hub. In the second family let r* be its additional leaf. Distinct path blocks meet only at r. Every path vertex starts a simple two-edge path within its P4 block.

We list all types of nonedges. Every displayed path has four edges and five distinct vertices.

1. Two path vertices in different blocks: choose a path neighbor u' of u in its block and a path neighbor v' of v in its block. Then u,u',r,v',v is a four-edge path.

2. Two nonadjacent path vertices in one P4 block: up to reversing a−b−c−d, the possible pairs are (a,c), (a,d), and (b,d). Corresponding paths are a,b,r,d,c; a,b,r,c,d; and b,a,r,c,d.

3. A leaf u* and the hub r: take a simple two-edge path u,v,w in u's block. Then u*,u,v,w,r is a four-edge path.

4. A leaf u* and a different path vertex v. If u and v are in different blocks, choose a path neighbor w of u. Then u*,u,w,r,v works. If u and v are in the same block and u has a path neighbor w different from v, the same path works. The only remaining case is that u is an endpoint and v its unique path neighbor. That v is internal to P4 and has a second path neighbor z different from u; then u*,u,r,z,v works.

5. Two distinct attached leaves u*,v*: their supports are distinct path vertices, and u*,u,r,v,v* is a four-edge path.

6. If present, the hub leaf r* and a path vertex v: choose a simple two-edge path v,w,z within its block. Then r*,r,z,w,v is a four-edge path.

7. If present, the hub leaf r* and a path leaf v*: choose a path neighbor w of v. Then r*,r,w,v,v* is a four-edge path.

All remaining pairs are edges: r is adjacent to every path vertex, each leaf to its support, and consecutive path vertices to each other. This exhausts all nonedges. Thus both families are C5-semisaturated, completing the theorem and equality characterization.

## Consequence for the optional exact formula

Füredi–Kim's Conjecture 4.1 in the inspected arXiv:1103.0067v1 first conjectures the asymptotic formula 11n/8+O(1), then suggests eventual equality in their upper bound (6), ssat(n,C5)<=ceil(11(n−1)/8).

For every t>=1 the second family gives

    ssat(8t+2,C5) <= 11t+1 < 11t+2 = ceil(11((8t+2)−1)/8).

Therefore eventual equality in (6) is false. This is an intercept correction only; it does not disprove the assigned asymptotic conjecture. No claim of first discovery is made without a broader novelty search.

## Exact remaining gap

Nothing above proves that an arbitrary C5-semisaturated graph has a universal vertex in H, nor that an extremal graph can be replaced by one with that property without increasing its size. Either assertion would need a new argument. Graphs without such a universal core vertex are excluded from the theorem, not implicitly discarded. The general matching lower bound remains unproved in this attempt.
