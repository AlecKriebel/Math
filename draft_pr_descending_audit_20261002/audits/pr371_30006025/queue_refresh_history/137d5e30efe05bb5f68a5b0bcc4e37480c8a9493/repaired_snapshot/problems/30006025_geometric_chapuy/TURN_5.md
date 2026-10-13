# Turn 5: sparse bounded-stretch repairs under the source length law

## Result and source law

This final author turn gives a probabilistic consequence of the **direct-realization** perimeter obstruction, not a counterexample to the source's broad geometric-bijection request. That request remains unresolved after five turns.

For a cubic one-face map of genus g let E=6g−3. The source normalization is face perimeter 12g, so the sum of edge lengths is 6g. The published Barazer–Giacchetto–Liu paper, *Length spectrum of large genus random metric maps*, Forum Math. Sigma 13(2025), e70, Section 1.2 (printed page 5) and Section 6, identifies the length law as

    X_e = ℓ_e/(6g),      (X_1,...,X_E) ~ Dirichlet(1,...,1).     (1)

This is the established metric-map model, not a newly proposed distribution. It can be sampled by independent exponential edge lengths followed by normalization; the paper credits the proportion/sum independence to Lukács. Its PDF and hashes were already bound by the source gate. The argument below works for any graph law, possibly conditioned on its combinatorial type, provided (1) holds conditionally. No assumption of independent chosen repair locations is needed.

Define

    s_g = (π/3)√(1−1/g),      δ_g = s_g−1.

Turn 4 proves δ_g>0 for g≥12 and δ_g>1/25 for g≥100. A direct realization means the same finite one-face graph cellularly embedded with positive piecewise geodesic edges and positive incident sectors in a smooth closed curvature−1 genus-g surface. The complement is an intrinsic disk. Its boundary counts every edge twice. Therefore any realized output lengths satisfy

    ∑_e (ℓ′_e−ℓ_e) / (6g) ≥ δ_g.                           (2)

The fixed curvature, full-surface area, one-face and same-edge-correspondence assumptions in turn 4 remain in force.

## Exact elementary broken-stick lemma

Let X have the law in (1), with any positive integer E. Write X_(1)≥...≥X_(E), and let T_{E,k}=X_(1)+...+X_(k) for 1≤k≤E, with T_{E,0}=0. Let H_m=∑_{j=1}^m 1/j and H_0=0. Then

    E[T_{E,k}] = (k/E)(1+H_E−H_k).                          (3)

This is a classical Dirichlet order-statistic identity; an elementary proof is included so the new obstruction needs no unproved order-statistic input.

**Proof.** Let Y_1,...,Y_E be independent Exp(1) variables, S=∑Y_i, and X_i=Y_i/S. The change of variables y_i=s x_i, with x_E=1−∑_{i<E}x_i, has Jacobian s^(E−1). Its joint density is e^(−s)s^(E−1) on s>0 times the uniform density in simplex coordinates after normalization. Thus S and X are independent, E[S]=E, and X has (1).

For the increasing exponential order statistics Y_[1]≤...≤Y_[E], the minimum has exponential rate E. Given which coordinate is minimal and its value, the residual differences of the other variables are again independent Exp(1), by memorylessness. Iterating gives independent spacings with respective means 1/E, 1/(E−1), ..., 1. In particular the expected j-th largest variable is

    E[Y_(j)] = H_E−H_{j−1}.

Therefore the sum of the k largest exponentials has mean

    ∑_{j=1}^k (H_E−H_{j−1}) = k(1+H_E−H_k).

Division by S preserves their ordering, and that sum equals S T_{E,k}. Independence gives E[S T]=E E[T], proving (3). The deterministic E=1 case agrees with the formula. ∎

For an independent exact finite control, the checker also uses the simplex-volume identity

    P(X_{i_1}>t,...,X_{i_r}>t) = (1−rt)_+^(E−1)

and inclusion-exclusion for the event that at least j coordinates exceed t. Integration gives

    E[X_(j)] = ∑_{r=j}^E (−1)^(r−j) C(r−1,j−1) C(E,r)/(rE).   (4)

For E=1 interpret the integrand on 0≤t<1 in the usual way; its integral is 1. Formula (3) is proved above for every E, while equality with (4) is independently checked on the declared finite range.

## Theorem 5.1: adaptive sparse-repair probability bound

Fix g≥12, a deterministic integer 0≤k≤E, and a deterministic factor C≥1. Allow a repair rule to inspect the entire graph, all lengths, any decorated-tree data and any auxiliary randomness. It may choose at most k edges adaptively. On unchosen edges require ℓ′_e=ℓ_e; on chosen edges allow any positive output length with ℓ′_e≤Cℓ_e, including decreases. Suppose the rule seeks a direct realization satisfying (2).

For every measurable such rule, its success probability obeys

    P(success) ≤ min{1, ((C−1)/δ_g) (k/E)(1+H_E−H_k)}        (5)

when k≥1. For k=0 or C=1 success is impossible. Equivalently, the same bound applies to the outer probability that any output in this repair class can succeed.

**Proof.** For any choice I of at most k changed edges, even if I depends on all data,

    ∑_e (ℓ′_e−ℓ_e)/(6g)
       ≤ (C−1)∑_{e∈I} X_e
       ≤ (C−1)T_{E,k}.                                  (6)

Combining (2) and (6), success implies the measurable event (C−1)T_{E,k}≥δ_g. For C>1, Markov's inequality and (3) prove (5). If C=1 or k=0 the left side of (6) is nonpositive, contradicting δ_g>0. The pointwise containment proves the outer-probability version without needing to assert measurability of an unrestricted geometric existence event. ∎

This remains valid for arbitrary adaptive angle choices and arbitrary searches over admissible embeddings, since only the necessary total-length increase is used. It is a necessary obstruction, not a characterization of realizability when (5) is uninformative.

## Corollary 5.2: changing o(g) edges by a bounded factor fails with high probability

Consider g→∞ and any sequences k_g≤6g−3 and C_g≥1. If, with the expression defined as zero when k_g=0,

    (C_g−1) (k_g/E) [1+log(E/k_g)] → 0,                  (7)

then the success probability of every allowed sequence of rules tends to zero, uniformly over those rules. In particular this holds if C_g is bounded and k_g=o(g).

**Proof.** For 1≤k≤E,

    H_E−H_k = ∑_{j=k+1}^E 1/j ≤ ∫_k^E dt/t = log(E/k).

Theorem 5.1 and δ_g→π/3−1>0 prove the first assertion. If r_g=k_g/E→0, then r_g[1+log(1/r_g)]→0, proving the bounded-factor special case. No limit law or concentration assumption for the selected edges has been invoked. For g≥100 an entirely rational finite-genus version of (5) is

    P(success) ≤ min{1, 25(C−1)(k/E)(1+H_E−H_k)}.         (8)

∎

For example a one-edge repair with C_g=o(E/log E) has success probability tending to zero. The result concerns the original absolute scale ℓsum=6g; normalization of all output lengths after the repair would change all edges and is outside the sparse class.

## Corollary 5.3: necessary expected stretch without a fixed cap

Suppose a measurable rule changes at most k≥1 edges and succeeds almost surely, but no deterministic cap is imposed. Put C(X)=max_e ℓ′_e/ℓ_e. Then

    E[C] ≥ 1 + δ_g E/[k(1+H_E−H_k)],                    (9)

with an infinite expectation permitted.

**Proof.** A positive required increase implies C>1. Inequality (6) applied pointwise with this random C yields C≥1+δ_g/T_{E,k}. Since T>0 almost surely, Jensen's inequality for 1/t and (3) give (9), also in the extended-expectation sense. ∎

Thus an almost-sure sparse repair must pay an increasing stretch cost when k=o(E). This does not rule out such unbounded corrections. A single edge can in principle absorb an order-g total-length increase if its factor is allowed to be large; our theorem does not claim such an output is geometrically possible or impossible.

## Final scope and unresolved gap

These five turns isolate several failures of particularly direct geometric recipes: fixed algebraic-angle holonomy, a thick regular-dessin model, exact perimeter preservation, and sparse bounded-factor length repair. They neither settle every geometric adaptation nor produce the controlled random-surface construction sought in Louf's Question 4. A viable construction may alter a positive fraction of lengths, use large distortions on a few edges, change the correspondence or geometry, or use a weaker asymptotic comparison. Even satisfying all necessary bounds here gives no sufficiency theorem or Weil–Petersson law.

The original disposition is **unsolved, five substantive author turns completed**. There is no sixth author search in this packet. No historical novelty is claimed for the credited bijections, Dirichlet sampler, transcendence inputs, dessins, systole classification, Poisson limit or isoperimetric inequality. The scoped deductions are supplied with their exact hypotheses for independent review.

## Exact checks and dependencies

`verify_turn5.py` uses only the standard library. It checks (3) against the independent inclusion-exclusion integrals (4), the integer inclusion-exclusion coefficients, exact harmonic monotonicity, and (6) for declared finite rational-vector/subset controls. It uses no random simulation and does not infer a probability theorem from bounded tests. The all-E proofs, Markov bound and asymptotic argument are in this file.

Primary law: https://doi.org/10.1017/fms.2025.31
Geometric input: https://arxiv.org/abs/1409.7681
Original target: https://ems.press/journals/owr/articles/14298589
