# Finite vertical intersections: a partial exclusion and the remaining gap

**Target:** 10000043 / AMR-099-0043, Benjamini's Open Problem 9.49.
**Status:** unresolved. This note excludes uniformly bounded fiber intersections, not all finite fiber intersections. No novelty claim is made; separate adversarial review is pending.
**Prepared:** 30 September 2026, gpt-6-astra at xhigh reasoning.

Let G be an infinite, connected, countable, locally finite simple graph. The model is independent Bernoulli **bond** percolation with a fixed parameter p on the **Cartesian** product G x Z. Assume p_c(G)=1 for bond percolation. Write F_v={v} x Z and C(x) for the open cluster of x. These conventions follow the original notes, pp. 5, 32–33 and 76; a bounded-degree assumption is not imposed.

The original question asks whether every infinite cluster that meets a fiber must meet it infinitely often. The results below leave exactly the possible clusters whose intersections with all fibers are finite but have unbounded sizes as the base vertex varies.

## 1. Infinite intersections propagate between fibers

**Lemma.** On G x Z at any fixed p>0, almost surely every open cluster C satisfies one of the following alternatives:

- C meets every fiber F_v in infinitely many vertices;
- C meets every fiber F_v in finitely many vertices, where zero is allowed.

This statement does not require p_c(G)=1.

**Proof.** It is enough to show that infinite intersection propagates across a fixed adjacent pair u,w in G. Reveal all percolation edges in the graph obtained by deleting the entire fiber F_w. Conditional on these edges, consider any of its clusters D that meets F_u infinitely often. There are infinitely many distinct edges joining D to F_w, one from each of those vertices of F_u. They are independent Bernoulli(p) edges not included in the revealed graph. Almost surely infinitely many are open. This conclusion holds simultaneously for all such D, since the revealed graph has only countably many clusters.

Suppose an original cluster C met F_u infinitely but F_w only finitely. Removing the finite set C intersect F_w splits C into finitely many components: the graph is locally finite, so only finitely many edges are incident to the deleted set. One of the remaining components D meets F_u infinitely. It is a cluster of the revealed graph, because any open path avoiding F_w that leaves D would also enlarge the original cluster C. The preceding conditional argument supplies infinitely many open edges from D to F_w, forcing C to meet F_w infinitely, a contradiction.

Take the countable intersection of the probability-one conclusions for all oriented base edges. Connectedness of G then propagates any infinite fiber intersection to every base vertex. QED.

Thus a counterexample to the target cannot mix finite and infinite fiber intersections. Its intersections must all be finite.

## 2. Capped exploration and independent domination on the base

**Proposition.** If p_c(G)=1 and 0<=p<1, then, almost surely, no infinite open cluster C satisfies

\[
\sup_{v\in V(G)} |C\cap F_v|<\infty.
\]

**Proof.** Fix an integer M>=1 and a starting vertex x=(v_0,n_0). Explore its cluster by a deterministic breadth-first search, with the following modification: accept at most M vertices in any one fiber. Start by accepting x. When an edge from an accepted vertex is queried and found open, accept its other endpoint if that endpoint was not previously accepted and its fiber has fewer than M accepted vertices. Otherwise ignore that proposed addition. Process every accepted vertex and each of its incident edges; never query the same product edge twice.

Fix a base edge e={u,v}. Every queried horizontal edge above e has its height in the set of heights of accepted vertices in F_u or in F_v. Each of those two sets has size at most M. Consequently at most 2M distinct horizontal edges above e are ever queried.

Implement the exploration by deferred decisions. For every base edge e, prepare an independent reservoir

\[
X_{e,1},\ldots,X_{e,2M},\qquad X_{e,j}\sim\operatorname{Bernoulli}(p).
\]

On the j-th previously unqueried horizontal edge above e, use X_{e,j} as its state. Use independent Bernoulli(p) variables for newly queried vertical edges. The choice of the next query depends only on past revealed states. Therefore this procedure has exactly the law of the capped exploration in the original independent product-edge model. Unqueried product edges may be completed independently afterward. The reservoir limit cannot be exceeded by the preceding deterministic count.

Define a base-edge configuration by

\[
Y_e=\max_{1\le j\le2M}X_{e,j}.
\]

The variables Y_e are independent Bernoulli variables with common parameter

\[
q_M=1-(1-p)^{2M}<1.
\]

Whenever the exploration reaches a new base vertex across a horizontal edge above e, that edge was found open, so Y_e=1. Vertical moves do not change the base vertex. Hence the projection of every accepted vertex belongs to the Y-open component of v_0. As p_c(G)=1, this base component is finite almost surely. At most M accepted vertices lie above each of its vertices, so the capped exploration is finite almost surely.

On the event that the entire actual cluster C(x) has at most M vertices in every fiber, the cap never excludes a vertex of C(x). Breadth-first search then explores all of C(x). This uses local finiteness, which makes the queue fair and ensures that every vertex at finite graph distance is eventually processed. It follows that

\[
\mathbb P_p\bigl(|C(x)|=\infty\text{ and }|C(x)\cap F_v|\le M
\text{ for all }v\bigr)=0.
\]

There are only countably many starting vertices x and positive integers M. Taking their union proves the proposition. QED.

The argument only dominates the capped exploration. It does not condition the percolation measure on the global fiber-size event; such conditioning would generally destroy independence.

**Corollary.** For p_c(G)=1 and a fixed 0<p<1, almost surely any infinite cluster failing the requested property has

\[
|C\cap F_v|<\infty\quad\text{for every }v,
\qquad
\sup_v|C\cap F_v|=\infty.
\]

For p=0 there are no infinite clusters. For p=1 the connected product graph is one cluster and every fiber intersection is infinite. Thus neither endpoint presents an additional issue.

## 3. Known uniqueness and cutset cases

Whenever percolation on G x Z has a unique infinite cluster, it meets every fiber infinitely almost surely. To see this, there is some vertex with positive probability of belonging to an infinite cluster, since the graph is countable and an infinite cluster exists almost surely. The FKG inequality and a finite path then give positive percolation probability at every vertex. The law is ergodic under vertical translations: finite cylinder events become independent under sufficiently large shifts, and approximation extends mixing to all events. The ergodic theorem gives positive density of infinite-cluster vertices along each fiber. Under uniqueness, all of these vertices belong to that one cluster.

[Benjamini–Kozma, Theorem 2](https://alea.math.cnrs.fr/articles/v10/10-02.pdf) proves that there is at most one infinite cluster on G x Z when there is a fixed finite K such that every finite set in G can be separated from infinity by deleting at most K edges. Their **Lemma 7** proves the requested fiber-intersection property directly under this hypothesis. These are published prior results, not results of this attempt. In arXiv version 2 the same fiber lemma is numbered 5.

The published counterexample in their Theorem 1 does not answer the present question negatively. Its base graph contains copies of Z^d for large d, so its base critical probability is at most p_c(Z^d)<1. Its subexponential growth and strong amenability do not replace the hypothesis p_c(G)=1.

## 4. Why the missing uniformity cannot be inserted for free

The base condition p_c(G)=1 does not imply the uniformly bounded cutset hypothesis. Here is an elementary example. Start with a rooted binary tree and replace every edge from original level n-1 to original level n by a path of length 2^n, for n>=1. Call the resulting locally finite degree-at-most-three graph T_*.

For any fixed p<1, the probability that the root reaches the original level n is at most

\[
2^n p^{\sum_{j=1}^n2^j}
=2^n p^{2^{n+1}-2}\longrightarrow0.
\]

An infinite root cluster must reach all original levels, since the finite subgraph before each level has finitely many vertices. Thus the root has zero infinite-cluster probability for every p<1. Connectedness and finite-energy opening of a fixed path imply the same at every vertex; hence p_c(T_*)=1.

On the other hand, let A_n contain the root and all subdivided paths up through original level n. From A_n there are 2^(n+1) edge-disjoint infinite rays, one through each outgoing original edge at that level. Any edge set separating every vertex of A_n from infinity must intersect every one of these rays. Its cardinality is therefore at least 2^(n+1), so no uniform K exists. This is a counterexample to the attempted cutset implication, **not** to the original fiber question.

There is also a probabilistic obstruction to replacing the cap M in Section 2 by unbounded deterministic capacities M_v. The induced bounds on base-edge opening probabilities would approach 1, while p_c(G)=1 excludes only a fixed common Bernoulli parameter below 1. Even on a ray, independent edge probabilities

\[
q_n=1-2^{-(n+1)},\qquad n\ge1,
\]

are all below 1 but give an infinite open path from the root with probability

\[
\prod_{n=1}^{\infty}q_n\ge
1-\sum_{n=1}^{\infty}2^{-(n+1)}=\tfrac12>0.
\]

The inequality follows first for finite products, or directly from the union bound, then by continuity. The homogeneous critical probability of the underlying ray is still 1. This explains exactly why the capped-exploration proof does not extend merely from finite intersection sizes at each vertex.

## 5. Remaining gap

The unresolved case is an infinite cluster with finite intersection with every vertical fiber but unbounded intersection sizes across the base graph. Neither the original assumption p_c(G)=1 nor finite-energy modifications in this analysis provide the uniform control needed to exclude it. The stronger cutset theorem does not cover all admissible graphs, as the stretched-tree example shows.

No counterexample to Benjamini's question, proof of its universal assertion, or exhaustive current-literature certification is claimed. The finite checker tests the capped deferred-decision coupling on a small product graph and exact probability calculations; it cannot decide an infinite-volume existence statement.
