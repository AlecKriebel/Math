# Proof-only edition notice

The original question remains **UNRESOLVED after approach 1 (1/5)**. The complete authored report below is preserved byte-for-byte, including every mathematical statement, proof, source comparison and limitation. The exact lift raises dimension from d to d+1 only when n ≥ d+2; the simplex case is handled separately. The equivalence concerns the two families of assertions over all fixed dimensions, not equality of their same-dimension extremal functions.

This edition adds no universal upper bound, fixed-dimensional super-square-root lower bound or novelty claim. The source inspections described below occurred during the original research and audit on 9 October 2026. Packaging did not repeat those inspections or conduct a new literature review. See [AUDIT.md](AUDIT.md) for the complete mathematical audit and [PROVENANCE.md](PROVENANCE.md) for the edition boundary. This is not an additional proof-search approach.

---

# Spherical lifts and worst case extension complexity

Problem 30004900 / OWR-8415356-006. Approach 1 of 5. Checked 9 October 2026.

## Result and scope

The requested square-root upper bound remains unresolved by this approach. We establish an elementary exact reduction: every full-dimensional d-polytope with n ≥ d+2 vertices is the coordinate projection of an inscribed, full-dimensional (d+1)-polytope with exactly n vertices. Consequently, the square-root conjecture for inscribed polytopes in every fixed dimension is equivalent to the square-root conjecture for arbitrary polytopes in every fixed dimension. In particular, an affirmative answer for inscribed 3-polytopes would give the square-root bound for every convex polygon.

The proof below is self-contained. The reduction is elementary, and no novelty is claimed. It yields neither a new universal upper bound nor a super-square-root lower bound. Its purpose is to identify the strength of the source question and an obstacle to extending results that require well-distributed vertices.

## Exact mathematical target and source

For each fixed integer d ≥ 2, is there a constant C_d such that

    xc(P) ≤ C_d sqrt(n)

for every d-dimensional convex polytope P having exactly n vertices on one Euclidean sphere? Here xc(P) is the smallest number of facets of a polytope E for which a linear projection maps E onto P. Facets and dimension are understood relative to the affine hull. An affine-image definition gives the same parameter, since a constant coordinate can be added without adding facets.

This formulation preserves all hypotheses in Lisa Sauermann's contribution, joint work with Matthew Kwan and Yufei Zhao, “[Focus] On the extension complexity of low-dimensional polytopes,” in *Combinatorial Optimization*, Oberwolfach Report 53/2021, printed pp. 2927–2929; the question is on printed p. 2929, PDF p. 37. The report was published in 2022, DOI [10.4171/owr/2021/53](https://doi.org/10.4171/owr/2021/53). The [official PDF](https://ems.press/content/serial-article-files/46931) was inspected, including a fresh rendering of that page. The constant may depend on d; the dimension does not grow with n.

The relevant established results are those of Kwan, Sauermann and Zhao, *Extension complexity of low-dimensional polytopes*, [arXiv:2006.08836v3](https://arxiv.org/abs/2006.08836v3), 23 March 2022; published in *Transactions of the American Mathematical Society* 375 (2022), 4209–4250, DOI [10.1090/tran/8614](https://doi.org/10.1090/tran/8614).

- Theorem 1.3 gives xc(P) ≤ 24 sqrt(n) for cyclic polygons. This already settles the source question in dimension 2.
- Theorem 1.1 gives the square-root order with probability tending to one for convex hulls of independent uniform points on a sphere in each fixed dimension. Its quantifier is probabilistic, not universal.
- Theorem 1.4 gives near-linear extension complexity with dimension allowed to grow. It does not refute a bound whose constant depends on a fixed dimension.

These statements were checked in the manuscript, rather than inferred from the title. The bounded status search found no full resolution of the remaining worst-case question. It is not an exhaustive certification of the literature.

For comparison, Shitov's *Sublinear extensions of polygons* gives the general polygon upper bound 147 n^(2/3). Its publisher record now identifies a published article in *Proceedings of the London Mathematical Society* 132 (2026), e70137, first published 8 April 2026, DOI [10.1112/plms.70137](https://doi.org/10.1112/plms.70137); the abstract agrees with [arXiv:1412.0728v2](https://arxiv.org/abs/1412.0728v2). This is a verified available bound, not a claim that a bounded search proves no stronger result exists.

## Projection monotonicity

**Lemma 1.** If P = L(Q) for a linear map L, then xc(P) ≤ xc(Q).

**Proof.** Let E be an extension of Q with xc(Q) facets and let T map E onto Q. Then L composed with T maps E onto P. The same E is therefore an extension of P with the same number of facets. ∎

No nonnegative-rank theorem or assumptions about the facets of Q are needed for this argument.

## A lift with the same number of vertices

**Theorem 2.** Let P = conv{v_1, …, v_n} be a full-dimensional polytope in R^d, where the listed points are its distinct vertices and n ≥ d+2. There exists a full-dimensional polytope Q in R^(d+1) with exactly n vertices, all on one sphere, such that the coordinate projection π(x,t) = x satisfies π(Q) = P.

**Proof.** Choose R > max_i ||v_i|| and write

    h_i = sqrt(R² − ||v_i||²) > 0.

Relabel the vertices so that v_1, …, v_(d+1) are affinely independent. Initially lift these d+1 points to

    w_i = (v_i,h_i),   1 ≤ i ≤ d+1.

Their affine hull H has dimension d: an affine dependence between the lifted points would project to a dependence between the original points. Moreover, H is the graph of a unique affine function f on R^d satisfying f(v_i) = h_i for 1 ≤ i ≤ d+1.

At v_(d+2), the two possible lifted heights are h_(d+2) and −h_(d+2). They are different, since h_(d+2) > 0. At most one equals f(v_(d+2)). Choose the other height, giving a point w_(d+2) outside H. For every remaining index i > d+2, set w_i = (v_i,h_i). Let

    Q = conv{w_1, …, w_n}.

Every w_i has Euclidean norm R, so these points lie on the common sphere centered at the origin. They are distinct because their first d coordinates are distinct. Each w_i is an exposed vertex: the linear functional z ↦ w_i · z has value R² at w_i, whereas for j ≠ i,

    w_i · w_j = R² − ||w_i − w_j||²/2 < R².

Thus Q has exactly the n listed vertices. The first d+1 span H and w_(d+2) is outside H, so dim Q = d+1. Finally, linear maps commute with convex hulls, giving

    π(Q) = conv{π(w_i): 1 ≤ i ≤ n} = conv{v_i: 1 ≤ i ≤ n} = P.

This proves every assertion. ∎

The choice of height sign is essential for the stated full-dimensional conclusion. For example, if the vertices of a square centered at the origin are all lifted with positive heights to a centered sphere, their heights are identical and the lift remains two-dimensional. Flipping one height gives full dimension. Neither a generic-position assumption nor an additional vertex is required.

### The simplex exception

If n = d+1, the input is a simplex. A polytope with d+1 vertices cannot have dimension d+1, so Theorem 2 must not be asserted in that case. For the asymptotic consequence, no lift is needed: a d-simplex itself has d+1 facets, and hence xc(P) ≤ d+1. Every simplex also has a circumsphere, but that observation is not required for the bound.

## Consequences for the conjecture

For n ≥ d+1, define F_d(n) to be the supremum of xc(P) over all d-dimensional n-vertex polytopes, and I_d(n) the corresponding supremum over those whose vertices lie on a common sphere. These suprema are finite because every n-vertex polytope is an image of the (n−1)-simplex and therefore has extension complexity at most n.

For n ≥ d+2, Lemma 1 and Theorem 2 give

    F_d(n) ≤ I_(d+1)(n).

The class inclusion also gives I_d(n) ≤ F_d(n). In particular, for n ≥ d+2,

    I_d(n) ≤ F_d(n) ≤ I_(d+1)(n) ≤ F_(d+1)(n).

**Corollary 3.** The following two families of assertions are equivalent:

1. For every fixed d ≥ 2, I_d(n) = O_d(sqrt(n)).
2. For every fixed d ≥ 2, F_d(n) = O_d(sqrt(n)).

**Proof.** Assertion 2 immediately implies assertion 1 by restriction. Suppose assertion 1 holds. For fixed d, Theorem 2 and Lemma 1 imply F_d(n) ≤ C_(d+1) sqrt(n) whenever n ≥ d+2. The case n = d+1 has F_d(d+1) ≤ d+1 and can be absorbed by taking, for example, the larger constant max{C_(d+1), sqrt(d+1)}. If the assumed asymptotic bound only starts at a larger threshold, its finitely many exceptions can likewise be absorbed using F_d(n) ≤ n. This proves assertion 2. ∎

The dimension shift matters. This does not prove equivalence between I_d and F_d at the same dimension, nor does it produce a dimension-independent constant. For a single fixed d, it proves that the inscribed bound in dimension d+1 is at least strong enough to imply the unrestricted bound in dimension d. In particular, the case I_3(n) = O(sqrt(n)) implies F_2(n) = O(sqrt(n)) for arbitrary polygons; the already established result for I_2 does not give this implication.

The reduction also transfers any super-square-root lower-bound sequence in a fixed dimension d to inscribed polytopes in the fixed dimension d+1, with no increase in vertex count. No such sequence is constructed in this approach. Transferring a sequence whose dimension already grows with n still leaves a growing-dimensional sequence.

## Concentrated vertices retain the obstruction

**Corollary 4.** Fix a spherical cap angular radius 0 < θ < π/2. In Theorem 2, after replacing the coordinate projection by a scaled coordinate map, Q can be chosen on the unit sphere so that at least n−1 of its vertices lie in the cap of angular radius θ centered at the north pole.

**Proof.** Choose ε > 0 so small that ε max_i ||v_i|| < sin θ. Apply the construction of Theorem 2 to εP with R = 1. Every positive-height lift has height

    sqrt(1 − ε²||v_i||²) > cos θ,

so lies in the specified cap. The construction uses negative height for at most one index. It still has full dimension and exactly n vertices. The linear map (x,t) ↦ x/ε maps Q onto P. ∎

Thus a square-root bound valid for all such concentrated inscribed configurations would already imply the unrestricted lower-dimensional square-root bound. Uniform distribution of the sphere points cannot be assumed or obtained merely from the inscription hypothesis. This is an obstruction to transferring a proof that requires well-distributed points without a new argument; it is not evidence that the conjectured bound is false.

## Checks and stopping point

The proof checks positivity of every lifted height, distinctness and exposedness of all n vertices, full dimension, exact projection, the direction of extension-complexity monotonicity, and the n = d+1 exception. The additional cap statement uses the same construction and is part of this single approach.

No numerical experiment is used to justify a universal assertion. Bounded searches of the main paper and public literature did not locate an attribution for this exact elementary lifting statement. That negative search does not establish originality. The statement and proof are recorded as an independently verified observation, with no new-result claim.

Exactly one substantive approach has been completed. The remaining target is a worst-case upper bound for fixed dimension d ≥ 3, or a verified fixed-dimensional counterexample. Neither is supplied here. The appropriate status is **partial structural reduction, original problem unresolved**, with **1/5 approaches used**.
