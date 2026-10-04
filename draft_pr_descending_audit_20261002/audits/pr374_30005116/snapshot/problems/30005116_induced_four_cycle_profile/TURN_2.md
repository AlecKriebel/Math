# Turn 2: density-preserving replacement for complete joins, and non-multipartite ties

**Original 30005116 / OWR-10252930-028 unresolved; second substantive author turn.** This turn extends the exact bound to a non-multipartite class, then combines it with the credited triangle-stability theorem. It also exhibits explicit non-multipartite graphs attaining the proposed construction value. Such ties are not counterexamples to the source conjecture, which asserts attainability by its construction, not uniqueness.

Write F(x)=3[(1−x)²−L(1−x)] for the proposed profile proved optimal in the multipartite class in turn 1. The exact source remains the unrestricted induced-C4 problem above edge density 1/2.

## 1. A credited elementary bound, with a direct proof

Use the following graphon notation only as a convenient way to state exact limiting densities. A graphon is a symmetric measurable W:[0,1]²→[0,1]. Sample four independent uniform points and, conditional on them, include each of the six possible edges independently with its W probability. Let c(W) be the probability that the resulting four-vertex graph is C4, and p(W)=∫W its edge probability. Thus c is the **unlabeled induced density** used by the source.

For every W,

    c(W) ≤ (3/2)p(W)².                                 (1)

This is the C4 case of Liu–Mubayi–Reiher Proposition 6.1 and Theorem 1.16, not a new unrestricted bound. Here is a direct proof that also fixes normalization. In any four-vertex graph, let M be the number of its three perfect matchings that are present. If the graph is an induced C4 then M=2; otherwise the indicator of being C4 is zero and M≥0. Hence 1_C4≤M/2 pointwise. Each of the three matching events consists of two edges on disjoint sampled vertices and therefore has probability p(W)². Taking expectations proves (1).

When 0≤p≤1/2, a complete bipartite graphon with part proportions u,v satisfying u+v=1 and 2uv=p attains equality. Its C4 density is 6u²v²=3p²/2. A complete bipartite component together with isolated vertices can also attain (1); equality does not require using every vertex in the component.

## 2. Theorem: a valid fixed-density replacement within complete joins

Suppose [0,1] is partitioned into finitely or countably many measurable blocks B_i of masses w_i>0 summing to 1. Assume W=1 almost everywhere between distinct blocks. Inside B_i, after normalizing its measure to 1, let its edge density and induced-C4 density be p_i and c_i. Assume

    p_i ≤ 1/2       for every i.                        (2)

No triangle-free, regular, bipartite or finite-step hypothesis is imposed on the internal graphons. Then

    c(W) ≤ F(p(W)).                                    (3)

There is an explicit complete multipartite replacement V with **exactly the same edge density** and c(V)≥c(W).

**Proof.** Put q_i=1−p_i and Q=∑w_i²q_i. The global edge density is 1−Q. An induced C4 sampled from a complete join can either lie in one block or use two vertices in each of two blocks. The occupancy patterns 3+1, 2+1+1 and 1+1+1+1 each give a vertex of degree three and cannot induce C4. Thus

    c(W)=∑_i w_i⁴ c_i
           +6∑_{i<j} w_i²w_j² q_iq_j.                 (4)

Replace the internal graphon of B_i by a complete bipartite graphon with proportions

    u_i=(1+√(1−2p_i))/2,    v_i=(1−√(1−2p_i))/2.

These are nonnegative by (2), sum to 1, and have 2u_iv_i=p_i. The global replacement V is complete multipartite, with independent-part masses w_i u_i,w_i v_i; zero masses are omitted. Its Q is unchanged, and (1) gives the exact gain identity

    c(V)−c(W)=∑_i w_i⁴[(3/2)p_i²−c_i] ≥0.             (5)

Turn 1 now proves c(V)≤F(1−Q). The countable case follows either by monotone convergence in (4)–(5) and continuity of the moments, or by merging the tail of the replacement part vector into one part and taking the tail mass to zero. The changes in its second and fourth moments tend to zero, and L is continuous by turn 1. ∎

The exact total deficit is the sum of two independently nonnegative terms. If z_j denotes the refined masses of V, then

    F(p(W))−c(W)
      =3[∑_j z_j⁴−L(Q)]
         +∑_i w_i⁴[(3/2)p_i²−c_i].                   (6)

Unlike unconstrained Lagrangian symmetrization, this operation really preserves the prescribed edge density. Its scope is restricted by the existence of the stated complete-join partition; an arbitrary graph need not have one.

### Finite-graph consequence, with a uniform error

Suppose a finite graph G has a vertex partition with all edges between distinct blocks and e(G[B_i])≤|B_i|²/4 in each block. Its usual adjacency graphon has p=2e(G)/n²=(1−1/n)x(G), and satisfies (2). Sampling with replacement differs from uniform sampling of four distinct vertices only on a collision event, whose probability is at most 6/n. Consequently, for n≥4,

    ρ(C4,G) ≤ F((1−1/n)x(G))+6/n.                      (7)

The bound is uniform in the number and sizes of blocks. In particular, it applies when every block is triangle-free, by Mantel's theorem, but triangle-freeness is not necessary.

## 3. Consequence for all asymptotic triangle minimizers

Let g_3(x) be the established minimum triangle-density function. If n→∞, x(G_n)→x and

    ρ(K3,G_n)−g_3(x(G_n)) →0,

then

    limsup ρ(C4,G_n) ≤ F(x).                            (8)

This is a deduction using **Pikhurko–Razborov's prior structural theorem**, not a new proof of triangle stability.

The exact input is Oleg Pikhurko and Alexander Razborov, *Asymptotic Structure of Graphs with the Minimum Number of Triangles*, Combin. Probab. Comput.26(2017),138–160, DOI10.1017/S0963548316000110, first published online4May2016. Their Theorem1.1 on printed140 was visually checked; the construction H_{a,n} is defined on139. For every ε>0, their theorem gives δ>0,n_0 such that a graph with triangle density at most g_3(a)+δ, where a is its actual edge density, can be changed into some H∈H_{a,n} by modifying at most ε binom(n,2) adjacencies.

Each H is a complete join of independent blocks and one triangle-free block; more specifically, that last block has |V_t||V_{t+1}| edges on |V_t|+|V_{t+1}| vertices. It therefore satisfies the hypothesis of (7). The number of changed induced-C4 vertex sets is at most the number of changed edges times binom(n−2,2). Dividing by binom(n,4) gives the exact bound

    |ρ(C4,G_n)−ρ(C4,H_n)| ≤6ε.                          (9)

The source construction has x(H_n)=x(G_n)+o(1) when the latter tends to fixed x<1. By continuity of F and (7), limsup c(G_n)≤F(x)+6ε. Since ε is arbitrary, (8) follows. For x=1 the assertion follows directly because every induced C4 has a missing edge; for x=0 it follows from (1). The same argument covers knot densities, without treating a rounded zero part as a positive one.

Equivalently, a fixed positive violation of the proposed C4 value at a fixed x cannot be achieved by a sequence whose triangle excess tends to zero. More precisely, for any fixed x∈(0,1) and η>0 there are δ>0,n_0 such that every n≥n_0 graph with |x(G)−x|<δ and

    ρ(C4,G) ≥ F(x(G))+η

has triangle excess at least δ above g_3(x(G)). Otherwise a contradicting sequence with both density error and triangle excess tending to zero violates (8). No effective numerical value of δ is claimed; the credited stability input uses removal/compactness arguments.

This does **not** prove every C4 maximizer has minimum triangle density. Proving such a reduction, or controlling the positive-triangle-excess regime, remains part of the original gap.

## 4. Explicit non-multipartite ties, with positive edit separation

Fix an intermediate x∈(1/2,1) which is not a knot 1−1/r. In the notation of turn 1, the proposed multipartite vector consists of r≥2 copies of a and one b, where 0<b<a and ra+b=1.

Keep r−1 independent blocks of mass a, joined completely to one another and to a remaining block U of mass a+b. Inside U use a complete bipartite component with part masses u,v and an isolated set of mass z, measured in the whole graphon, where

    uv=ab,       u+v+z=a+b,       u,v>0,       z≥0.      (10)

Such choices form a continuum: choose u∈[b,a], put v=ab/u, and z=a+b−u−v. The inequality z≥0 is equivalent to (u−a)(u−b)≤0. Interior choices have z>0; in particular u=v=√(ab) gives z=(√a−√b)²>0.

The original two parts of masses a,b and this new internal component have the same internal edge contribution 2ab and induced-C4 contribution 6a²b². Their total block mass is unchanged. Formula (4) therefore proves the new graphon has **exactly the same x and F(x)** as the source construction. It is extremal within the class of Section2 and attains the conjectured unrestricted value; we do not assume that value is the unrestricted maximum.

This graphon is genuinely non-multipartite. Its induced density of K2 plus an isolated vertex is

    6uvz=6abz>0.                                       (11)

Only a triple with one vertex from each of the u,v,z sets has exactly one edge. A complete multipartite graphon has no such triple. If ε is the L1 edit distance to any complete multipartite graphon, a common sampled triple changes its induced graph only if one of its three edge states changes; coupling these states gives a probability at most 3ε. Hence

    ε ≥ 2abz>0.                                        (12)

This also bounds the infimum over all vertex relabelings. There is additionally a positive induced-paw density 24(r−1)a·abz, but (11) already gives the required separation.

For a fully rational example, take r=2,a=4/9,b=1/9 and u=v=2/9,z=1/9. The new graphon is the blow-up of a paw with masses (4,2,2,1)/9, where the mass-4 block is the triangle vertex also incident to the pendant edge. Direct exact counts give

    edge density       =16/27,
    induced C4 density =64/243,
    triangle density   =32/243,
    one-edge triple density =8/243,
    edit distance from any multipartite graphon ≥8/729.

The triangle density also equals that of the proposed (4,4,1)/9 complete tripartite graphon. This flexibility lies within the prior Pikhurko–Razborov family, which already allows arbitrary triangle-free internal graphs with a fixed edge count. It is not a new family of triangle minimizers or a counterexample to the source. Its role here is to make explicit that a uniqueness-based multipartite reduction would be false.

## 5. Scope of progress and checks

The original remains unresolved after two turns. We now know the proposed bound on every complete join with internal densities at most1/2, and on every asymptotic triangle-minimizing sequence using a credited structural theorem. We also have exact non-multipartite ties and a quantitative obstruction to uniqueness. The missing class consists of hosts not covered by that join replacement or by triangle stability; no claim excludes them.

`verify_turn2.py` independently enumerates four-vertex matching inequalities, directly integrates selected finite-step graphons using exact fractions, checks the join-count identity and low-density bound, and verifies the rational non-multipartite tie family and edit constants. Bounded checks are supplementary. The universal replacement proof and the precise external stability hypothesis are given above.

Prior input and credit: https://arxiv.org/abs/2106.16203v2 ; https://pikhurko.github.io/E/PikhurkoRazborov17cpc.pdf ; https://doi.org/10.1017/S0963548316000110 .
