# Square-tiling percolation: rigorous partial results and the remaining gap

Problem 10000051 / AMR-099-0051. Status: **PARTIAL, NOT SOLVED**.

## 1. Exact model and source scope

Let Q=[0,1]^2. Fix a finite family T of closed, axis-parallel squares of positive side length, with disjoint interiors and union Q. Assume that no point is incident to four tiles. Write s(t) for the side length of tile t. Color tiles independently black with probability p, with no conditioning or forced boundary colors. Adjacent tiles share a nonempty boundary intersection; under the no-fourfold condition, this agrees with positive-length-side adjacency in a finite tiling. A black horizontal crossing is a finite chain of black tiles connecting the left and right sides of Q. Define q_T(p) as its probability; define v_T(p) for bottom-to-top crossings. Finite union connectivity and graph-chain connectivity agree here. The tile geometry is deterministic, and there is no sampling measure on tilings.

The original lower-bound question asks for c>0 independent of T with q_T(1/2)>c. The small-mesh extension asks whether q_Tn(1/2) tends to 1/2 for every sequence of admissible tilings with max_t s(t) tending to zero. Euclidean maximum diameter differs by the constant sqrt(2), so these mesh conditions are equivalent. This is a deterministic, uniform-over-sequences statement, rather than convergence for a random ensemble of tilings.

Benjamini's 2015 paper [B15, Conjecture 2.2] states the universal lower bound. His October 2015 slides [BS15, PDF pages 22–23] state both the lower bound and the small-mesh extension. The latter pages correspond to zero-based page indices 21–22. The 2018 Benjamini–Kalai paper [BK18, Conjecture 2.1] restates the lower-bound question. The sources allow infinitely many tiles, but do not fix an accumulation-point convention for the crossing event. Peled [P20, Section 8.6] explicitly explains that finite-chain, connected-closure and path-in-closure notions can differ and that his estimates do not establish the closure versions. All unconditional positive-crossing assertions below are for finite tilings; Section 7 makes the countable finite-chain statements explicit.

No full resolution of either original target was located in the bounded literature search through 2026-10-07. The substantial credited partial result is Peled [P20, Corollary 2.10]: a uniform finite-tiling crossing bound at a fixed black probability very close to one. Section 6 gives an explicit consequence of his theorem, not a new proof of the fair-color conjecture. The quenched Voronoi results of Ahlberg–Griffiths–Morris–Tassion concern random Voronoi tessellations and do not cover every deterministic square tiling.

## 2. Finite duality, with the missing symmetry exposed

**Lemma 2.1 (finite Hex alternative).** Exactly one of a black left-right crossing and a white bottom-top crossing occurs.

Proof. The cell-contact dual, with four exterior terminal vertices L,T,R,B attached to the tiles touching the corresponding sides, is a triangulated disk whose outer boundary is the cycle L,T,R,B. To construct the embedding, join each tile center to a point in the relative interior of each shared side, through the tile interior, and join centers across that side. Around an interior tiling vertex, three incident tiles give a triangular dual face; a point lying in just two tiles merely subdivides an edge. Boundary fans and the four corner triangles complete the disk. The no-fourfold assumption excludes quadrilateral interior faces. Give L and R the color black and T and B the color white.

Inside each triangle of this auxiliary triangulation having both colors, draw the segment joining the midpoints of its two differently colored edges. The resulting interfaces have degree two in the interior and have exactly four endpoints, the midpoints of the four outer edges LT,TR,RB,BL. They are disjoint simple paths and loops. The path starting on LT cannot end on RB: the other two endpoints would then have to be joined across it. If it ends on TR, its black bank gives an adjacent black-vertex chain from L to R; if it ends on BL, its white bank gives an adjacent white-vertex chain from T to B. Removing exterior terminals gives the required tile crossing. The bank-chain assertion follows triangle by triangle: two successive same-colored bank vertices are either identical or endpoints of one triangle edge.

Finally two differently colored transverse crossing chains would give disjoint vertex paths connecting alternating boundary terminals in this planar disk, which is impossible by planar separation. Thus the alternatives are exclusive. ∎

Consequently, at every p,

q_T(p)+v_T(1-p)=1.                                              (2.1)

At p=1/2, q_T+v_T=1. Let T^tr be the tiling obtained by exchanging x and y. Then

q_T(1/2)+q_T^tr(1/2)=1.                                       (2.2)

If T has a boundary-direction-swapping symmetry, q_T(1/2)=1/2 exactly. More generally an ensemble of finite tilings invariant in law under transposition has annealed crossing probability exactly 1/2. At least one direction of every fixed finite tiling has crossing probability at least 1/2. Neither assertion supplies a lower bound for a prescribed direction of every T.

**Explicit obstruction to an exact-half argument.** Tile [0,4]^2 with the seven squares specified by (left,bottom,side):

(0,0,2), (2,0,2), (0,2,1), (1,2,2), (3,2,1), (0,3,1), (3,3,1).

Scale by 1/4 to obtain T in Q. The three large squares have side 1/2; the others have side 1/4. They cover Q without overlap and at most three tiles meet at any vertex. Label them A,B,C,D,E,F,G in the order above. Their adjacency lists are

A: B,C,D; B: A,D,E; C: A,D,F; D: A,B,C,E,F,G;
E: B,D,G; F: C,D; G: D,E.

Left boundary tiles are A,C,F; right boundary tiles B,E,G. Exhaustive Boolean evaluation gives the following numbers of horizontal crossing configurations with exactly k black tiles, k=0,...,7:

0, 0, 1, 13, 24, 19, 7, 1.

The corresponding vertical counts are 0,0,2,11,22,20,7,1. There is also a short direct proof of the horizontal probability. If D is black, crossing is equivalent to at least one of {A,C,F} and at least one of {B,E,G} being black. If D is white, the edge A–B is the only connection between the left group and the right group, so both A and B must be black. These groups have disjoint independent colors, giving

q_T(p)=p[1-(1-p)^3]^2+(1-p)p^2.

At p=1/2 this is 49/128+16/128=65/128. Duality gives v_T(1/2)=63/128. The supplied verifier checks the geometry and every one of the 128 configurations using only integer arithmetic. Equivalently the counts specify the exact reliability polynomial

q_T(p)=p^2(1-p)^5+13p^3(1-p)^4+24p^4(1-p)^3
       +19p^5(1-p)^2+7p^6(1-p)+p^7.

This is a counterexample only to the stronger assertion that every finite tiling has probability exactly 1/2. Its fixed mesh does not refute either original conjecture.

## 3. The square geometry gives exact vertex extremal length

For a finite tile metric rho:T→[0,infinity), set A(rho)=sum_t rho(t)^2 and let L_H(rho) be the minimum of sum_{t in gamma}rho(t) over simple horizontal tile paths. Define

VEL_H(T)=sup_{A(rho)>0} L_H(rho)^2/A(rho).

**Theorem 3.1.** VEL_H(T)=VEL_V(T)=1. The extremal metric rho(t)=s(t) attains both values.

Proof. Every horizontal tile path has a connected union projecting onto [0,1]. Its tile projections have lengths s(t), hence sum_{t in gamma}s(t)≥1. Also sum_t s(t)^2=area(Q)=1. Therefore VEL_H≥1.

For the reverse inequality, choose y avoiding the finitely many horizontal tile-edge heights. The tiles intersected by the line [0,1]×{y}, in order, form a horizontal tile path, with each tile appearing once. Hence L_H(rho)≤sum_t rho(t)1_{y in vertical interior of t}. Integrate over y∈[0,1]:

L_H(rho)≤sum_t rho(t)s(t)
        ≤sqrt(sum_t rho(t)^2)sqrt(sum_t s(t)^2)=sqrt(A(rho)).

This proves VEL_H≤1. Exchange x and y for the vertical result. The side-length metric has horizontal line paths of length exactly 1, so it attains the supremum. ∎

No no-fourfold assumption is needed for Theorem 3.1: a generic line crosses positive-length common sides even in a grid. This highlights the limitation of the variational calculation. A theorem converting these deterministic extremal-length identities plus the no-fourfold condition into a uniform fair-color crossing estimate would solve the lower-bound question; no such conversion is proved here. Identical extremal lengths do not imply identical crossing probabilities, as Section 2's example demonstrates.

## 4. Influence and change-of-measure approach

For the increasing Boolean crossing function f_T, let I_i(p) be the probability, over all other tile colors, that tile i is pivotal. The exact identities and bounds are

q_T'(p)=sum_i I_i(p),
q_T(p)(1-q_T(p))≤p(1-p)sum_i I_i(p).                           (4.1)

The first follows by writing the expectation as a multilinear polynomial in individual tile probabilities and differentiating all coordinates. For the second, reveal coordinates one at a time and use the orthogonality of martingale differences. Conditioning on all other coordinates, the conditional variance from resampling coordinate i is p(1-p)(f(omega^{i=1})-f(omega^{i=0}))^2. Variance tensorization (obtained by iterated conditional variance, or the same martingale expansion with conditional Jensen) bounds Var(f) by the sum of these conditional variances. Since f is increasing and Boolean, the squared difference is exactly the pivotal indicator. This gives (4.1).

Thus, wherever 0<q_T(p)<1,

d/dp log(q_T(p)/(1-q_T(p)))≥1/[p(1-p)].                        (4.2)

In particular, integrating from a to b with a<b gives

logit(q_T(b))-logit(q_T(a))≥logit(b)-logit(a).

This is a lower bound on the steepness of the transition. A lower bound at b>1/2 does not yield a useful lower bound at 1/2 through this inequality: the allowable earlier value can be arbitrarily small. A missing upper bound on the accumulated pivotal contribution would be needed to run such a comparison backward.

One always has a weaker finite-size transfer. With N=|T| and b≥1/2, the likelihood ratio of product Bernoulli(b) relative to fair colors is at most (2b)^N. Hence

q_T(1/2)≥q_T(b)/(2b)^N.                                      (4.3)

Cauchy–Schwarz gives the alternative exact inequality

q_T(1/2)≥q_T(b)^2 / [2(b^2+(1-b)^2)]^N.                       (4.4)

Indeed the fair-measure second moment of the likelihood ratio is the denominator. Both bounds depend exponentially on N; neither is uniform over arbitrarily fine tilings. The Boolean AND function, with probabilities b^N and 2^{-N}, confirms that a dimension-free backward transfer cannot follow from monotonicity alone. AND is used only as a logical obstruction to that inference, not as a claimed square-tiling crossing example.

For the seven-square tiling, the exact fair influences, in the specified order, are

23/64, 23/64, 7/64, 33/64, 7/64, 7/64, 7/64.

They sum to 107/64, which is also the derivative at 1/2 of the polynomial in Section 2. Geometry-sensitive pivotal bounds remain absent. In particular, this calculation does not establish that maximum influence vanishes with mesh, and it gives no uniform noise-sensitivity or conformal-invariance conclusion.

## 5. Precisely credited non-elementary input

We use only the following external theorem in the next section. Let S be a finite or countable packing of closed axis-parallel squares with disjoint interiors, where adjacency includes corner touching. If all side lengths are at most D, independently color squares white with probability

r_0=exp(-26).

For a fixed square t, let E(t,a) mean that t is white and is connected by a finite white tile chain to another square whose set-distance from t in the sup norm is at least a. Then

P(E(t,a))≤exp(-a/D).                                          (5.1)

This is the square-packing instance of Peled [P20, Theorem 2.13, equation (7)], with the explicit choice in Section 3, equation (8). In his convention the diameter is the sup-norm diameter, equal to the square's side length. The theorem is substantial; its multiscale proof, including the BK inequality, is a dependency, and is not claimed to have been reproved in this packet. Its exact parameter r_0 is far below 1/2. It cannot be replaced here by 1/2 or even by an arbitrary r<1/2.

## 6. An explicit uniform bound and fine-mesh limit near p=1

Set p_0=1-r_0. Define for integers K≥6

R_K = 4^(K+1) * 2^(-2^(K-2)) / [1-4*2^(-2^(K-2))].            (6.1)

**Theorem 6.1 (consequence of Peled).** Every finite admissible tiling T satisfies

q_T(p_0)≥c_0:=(2/3)(1-exp(-26))^4096>0.                       (6.2)

If max_t s(t)≤2^(-K) with K≥6, then

q_T(p_0)≥1-R_K,                                               (6.3)

and hence q_Tn(p_0)→1 as the maximum side length tends to zero. Monotone coupling gives the same conclusions for every p≥p_0. These conclusions do not address p=1/2.

Proof. Call the rare color white. Let S_k consist of the tiles with side in (2^(-k-1),2^(-k)], k≥0. Area gives

|S_k|≤4^(k+1).                                                (6.4)

Suppose there is a white vertical crossing, and choose a largest tile t on its finite crossing chain. If t∈S_k and k≥6, every tile of that chain has side at most D=2^(-k). The bottom-end tile lies in y≤D and the top-end tile lies in y≥1-D. If the vertical interval of t is [y,y+s], the sup-norm set distances from t to these end tiles have respective lower bounds y-D and 1-D-y-s. At least one is at least (1-2D-s)/2≥(1-3D)/2>1/4. Therefore the crossing implies E(t,1/4) in the subpacking consisting of tiles of side at most D. By (5.1), this event has probability at most exp(-2^(k-2)). A union bound over possible largest tiles gives, whenever all tiles have side at most 2^(-K),

P(white vertical crossing)≤sum_{k≥K}4^(k+1)exp(-2^(k-2)).       (6.5)

For k≥K, the ratio between consecutive summands is 4exp(-2^(k-2)), at most 4exp(-2^(K-2)). Since e>2, the first summand and all ratios are bounded above by their counterparts in (6.1). Thus the sum is at most R_K. Finite duality proves (6.3), and the explicit expression R_K tends to zero.

For arbitrary mesh, let F say all tiles with side greater than 1/64 are black. At most 4096 tiles satisfy that condition, by disjoint areas, so P(F)≥(1-r_0)^4096. Given F, every possible white crossing uses only squares of side at most 1/64. Their colors retain the original independent rare-color law, so the same union bound gives

P(white vertical crossing | F)≤R_6=4096/16383<1/3.

It follows that P(no white vertical crossing)≥(2/3)(1-r_0)^4096. Use finite duality for (6.2). The inequality e>2 also gives c_0>(2/3)(1-2^(-14)) by the elementary Bernoulli inequality, although no sharp constant is claimed. ∎

This is an explicit version of the mechanism behind [P20, Corollary 2.10 and Section 6.3]. The novelty and priority of the elementary constant choices and derived mesh formula are not asserted. The rare-color theorem is exactly where this approach stops before reaching the desired fair-color regime.

## 7. Countable exhaustion: what passes to the limit, and what does not

Let T be a countable collection of closed positive-size squares packed in Q. Let H_fin be the event that a finite black tile chain joins the left and right sides, and define W_fin vertically for white tiles. Use the product Bernoulli measure on the countable tile set. These are measurable events: each is a countable union of cylinder events specified by finite chains.

For m≥1 set T_m={t∈T:s(t)≥1/m}. Disjoint areas imply |T_m|≤m^2. A finite chain has a positive minimum side length, so

H_fin = union_m H(T_m),     P(H_fin)=lim_m P(H(T_m)).           (7.1)

Here H(T_m) is crossing in the finite *packing*, with the original boundary contacts, not in a tiling formed by filling gaps. The union is increasing. The same statement holds for W_fin.

**Proposition 7.1.** For every countable square packing in Q, with white probability r_0=exp(-26),

P(W_fin)≤1-c_0.

If every square has side at most 2^(-K), K≥6, then P(W_fin)≤R_K.

Proof. The rare-white-crossing proof in Section 6 used only disjoint interiors, square geometry and finite crossing witnesses. It therefore applies to every finite T_m, even if T_m does not cover Q and even if four tiles meet at a corner. Pass to the limit with (7.1). Alternatively the maximal-square and dyadic argument works directly, since each finite witness has a largest tile and each dyadic class is finite. ∎

This controls the complement of a white finite-chain crossing. It does **not** prove P(H_fin)≥c_0 for countable tilings. Even when T covers Q, T_m usually has gaps, so the finite Hex alternative is unavailable on T_m. A limit of black paths in a sequence of completed tilings need not produce a finite black chain in T; it can use indefinitely smaller tiles. Replacing that chain by a connected set in the closure changes the event. For any specified countable tiling, a finite black horizontal chain and a finite white vertical chain remain incompatible under the no-fourfold assumption, so P(H_fin)+P(W_fin)≤1. The reverse inequality is the missing infinite Hex alternative, and is not asserted here.

**Proposition 7.2 (conditional finite-to-countable transfer).** Suppose an admissible countable tiling T has:

(i) finite admissible tilings U_n and increasing finite subsets F_n⊂T with union T, such that U_n contains every square of F_n exactly;

(ii) with probability one, either H_fin or W_fin occurs under the chosen product coloring of T.

Give common tiles the same colors and independently color the extra tiles of U_n. If every finite admissible tiling has fair horizontal crossing probability at least c, then P_T(H_fin)≥c.

Proof. On H_fin choose a finite black witnessing chain. It lies in F_n for all sufficiently large n, so every such U_n has a black crossing. On W_fin choose its finite white witness. It likewise lies in F_n eventually, and the finite Hex alternative forbids a black crossing in U_n. Thus the crossing indicators of U_n converge almost surely to 1_{H_fin}, irrespective of the extra colors. Every U_n has the fair product marginal, because common and extra tile colors are independent fair bits. Bounded convergence proves P_T(H_fin)=lim_n q_Un(1/2)≥c. ∎

Both hypotheses are additional, nontrivial conditions; neither is claimed for every countable square tiling. Proposition 7.2 explains exactly what an exhaustion argument must establish. It is not a proof of the original countable version.

## 8. Final scope and unresolved requirements

Established here:

- finite complementary-crossing duality and exact 1/2 for direction-symmetric tilings or symmetry-invariant tiling laws;
- a rigorously checked seven-square obstruction to an exact-half assertion for every finite tiling;
- exact horizontal and vertical vertex extremal length equal to one;
- correct pivotal/interpolation identities and explicit finite-size probability transfers;
- an explicit high-density bound and quantitative small-mesh crossing-to-one statement, dependent on and credited to Peled's theorem;
- finite-chain exhaustion and conditional transfer results for countable tilings.

Not established:

- a fixed-direction universal positive lower bound at p=1/2 for all finite admissible tilings;
- the small-mesh convergence q_Tn(1/2)→1/2 for arbitrary deterministic tiling sequences;
- a resolution of the countable-tiling statement under any of the potentially different accumulation-point crossing conventions.

The exact computation is a finite verification, not sampling and not an asymptotic proof. No Monte Carlo estimate is used. The high-density theorem cannot be promoted to p=1/2 by monotonicity, and the unit extremal-length identity cannot be promoted to rotational invariance of the color law.

## References

[B15] Itai Benjamini, *Percolation and coarse conformal uniformization*, arXiv:1510.05196v2 (2015), Conjecture 2.2, PDF p. 3. https://arxiv.org/abs/1510.05196 . Published in *Contemporary Mathematics* 719 (2018), 39–42, DOI https://doi.org/10.1090/conm/719/14468 .

[BS15] Itai Benjamini, *Uniformization and percolation*, October 2015 slides, PDF pages 22–23. Archived author-hosted file: https://arquivo.pt/noFrame/replay/20201231041529id_/http://www.wisdom.weizmann.ac.il/~itai/conformaltalk1.pdf .

[BK18] Itai Benjamini and Gil Kalai, *Around two theorems and a lemma by Lucio Russo*, *Mathematics and Mechanics of Complex Systems* 6 (2018), no. 2, 69–75, Conjecture 2.1. Publisher PDF: https://msp.org/memocs/2018/6-2/memocs-v6-n2-p01-p.pdf .

[P20] Ron Peled, *On the site percolation threshold of circle packings and planar graphs*, arXiv:2001.10855v1 (2020), Conjecture 2.9, Corollary 2.10, Theorem 2.13, Sections 3, 6.3 and 8.6. https://arxiv.org/abs/2001.10855 .

[AGMT16] Daniel Ahlberg, Simon Griffiths, Robert Morris and Vincent Tassion, *Quenched Voronoi percolation*, arXiv:1501.04075; *Advances in Mathematics* 286 (2016), 889–911. https://arxiv.org/abs/1501.04075 . This related resolution is not a solution of deterministic square-tiling percolation.
