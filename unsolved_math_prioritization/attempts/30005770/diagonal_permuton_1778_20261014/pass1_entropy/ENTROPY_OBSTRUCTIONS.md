# Entropy and counterexample audit for the diagonal permuton conjecture

## Outcome and exact scope

Fix a nonempty permutation α, put τ = α ⊖ 1, and sample Π_n exactly uniformly from Av_n(τ). This note does **not** prove or disprove the assertion that μ_{Π_n} tends weakly in probability to μ_I = Law(U,U). It establishes precise barriers to stronger pointwise claims and to two coarse entropy strategies, together with an exact finite-cut reduction. No fixed-pattern counterexample to the stated target is obtained.

All constructions below use fixed forbidden patterns. A separate separable-permutation example concerns a different class and is explicitly only a counterexample to a proposed general inference, not to the target.

## 1. Exponential growth and sum closure

Write a_n = |Av_n(τ)|, with a_0 = 1. A pattern ending in its minimum cannot be a nontrivial direct sum. Consequently, an occurrence of τ in σ ⊕ ρ would have to lie entirely in one summand. Thus Av(τ) is direct-sum closed and

    a_{p+q} ≥ a_p a_q.

The exponential upper bound for avoidance of a fixed pattern is the Stanley–Wilf theorem. Fekete's lemma therefore gives

    1 ≤ λ := lim a_n^(1/n) = sup a_n^(1/n) < ∞,
    a_n ≤ λ^n.

For later use, for every 0 < η < λ there is c_η > 0 such that a_k ≥ c_η (λ−η)^k for every k ≥ 0. Indeed the bound with constant 1 holds for all sufficiently large k, and the finitely many smaller positive values can be absorbed into c_η.

Primary source for the exponential bound: Marcus–Tardos, *Excluded permutation matrices and the Stanley–Wilf conjecture*, Corollary 2, p.2, and its proof via Theorem 9, p.5: https://www.renyi.hu/~tardos/submatrix.pdf . The complete displayed statements and associated reduction were inspected. The argument for existence of λ here is the elementary sum-closure/Fekete argument, not an additional literature assumption.

## 2. Upper off-diagonal points have full exponential growth

Assume additionally that α does not begin with its maximum; equivalently τ(1) < |τ|. Then prepending a new global maximum preserves τ-avoidance. Any occurrence using that new point would have its first selected entry largest, which contradicts τ(1) < |τ|.

For every 1 ≤ i ≤ j ≤ n, the map

    (σ, η, ρ) ↦ σ ⊕ (1 ⊖ η) ⊕ ρ,

with lengths i−1, j−i, n−j respectively, is injective, preserves τ-avoidance, and places the value j at position i. Therefore

    |{π ∈ Av_n(τ) : π(i)=j}| ≥ a_{i−1} a_{j−i} a_{n−j}.                 (2.1)

Using the uniform lower bound from Section 1 and a_n ≤ λ^n gives, simultaneously for every i ≤ j,

    P(Π_n(i)=j) ≥ c_η^3 (λ−η)^(n−1) / λ^n.

Letting n → ∞ and then η ↓ 0 proves the stronger uniform statement

    lim_{n→∞} min_{1≤i≤j≤n} P(Π_n(i)=j)^(1/n) = 1.                    (2.2)

Thus no upper off-diagonal point can have exponentially small occupation probability. In particular, for any fixed 0 < ε < 1,

    lim P(max_i |Π_n(i)−i| ≥ ε n)^(1/n) = 1.

This rules out exponential concentration of the maximum displacement. It does not rule out concentration of the permuton's mass.

The nonrare-region conclusion is already present in Madras–Yıldırım, Theorem 1(b), p.5. Formula (2.1) is an elementary direct-sum proof sufficient for the needed barrier; no novelty is claimed. Source: https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i4p13/pdf/ . Their full definition of rarity and both parts of Theorem 1 were inspected.

### A positive-probability extreme point is still not a permuton counterexample

At i=1,j=n, deletion of the first point gives an exact bijection, so

    P(Π_n(1)=n) = a_{n−1}/a_n.                                       (2.3)

Madras–Yıldırım Theorem 15 states the ratio limit a_n/a_{n−1} → λ whenever either endpoint of the forbidden pattern is its minimum or maximum. It therefore applies to every τ here. Under the additional nonmaximum-first-entry assumption, (2.3) yields

    P(Π_n(1)=n) → 1/λ > 0.

The complete statement of their Theorem 15 was inspected; this is a credited application, not an independent audit of the older source cited for its proof. For example, the already-covered target τ=231 exhibits precisely this phenomenon.

A point in the top-left corner contributes only 1/n to μ_π. Even an extreme displacement of order n for that point does not force a positive lower bound on d_BL. The positive probability in (2.3) is therefore **not** the required failure certificate for the conjecture.

## 3. Diagonal neighborhoods always have full exponential growth

The following applies to any nonempty direct-sum-closed permutation class C with finite exponential growth λ, not merely Av(τ). Let c_n=|C_n| and assume C contains one permutation of every size.

Fix ε>0. Let N_n(ε) count members with d_BL(μ_π,μ_I)<ε. For any fixed k, form a direct sum of q=⌊n/k⌋ arbitrary members of C_k and an arbitrary remainder member of C_r, r=n−qk. The choices are injective since the block boundaries are fixed. They give c_k^q c_r permutations.

Every permutation square lies within |x−y|≤k/n. Coupling a point (X,Y) with (X,X), whose law is μ_I because the X-marginal is uniform, gives

    d_BL(μ_π,μ_I) ≤ E|X−Y| ≤ k/n.

Hence, for all sufficiently large n,

    N_n(ε) ≥ c_k^⌊n/k⌋ c_r.

Take nth roots, let n→∞, and then k→∞. The upper bound N_n(ε)≤c_n gives

    lim N_n(ε)^(1/n) = λ.                                           (3.1)

In fact (3.1) remains true with ε=ε_n↓0 whenever n ε_n→∞. Choose block sizes k_n→∞ with k_n=o(n) and k_n/n<ε_n; the remainder is o(n), and log c_{k_n}/k_n→log λ.

The point of (3.1) is a limitation: finding full exponential growth near the proposed diagonal limit cannot identify the uniform limit. A probability is a ratio of counts; matching nth-root growth on numerator and denominator leaves the subexponential ratio uncontrolled.

### A fully proved non-target example invalidates that inference

Let S be the smallest class containing the singleton and closed under direct and skew sums. This is the class usually called separable permutations. It is a permutation class: any pattern of a direct or skew sum is a direct or skew sum of patterns of its summands, after empty pieces are discarded. It excludes 2413, because 2413 is neither a nontrivial direct sum nor a nontrivial skew sum; induction on the construction tree proves avoidance. Thus it has finite exponential growth, and it is direct-sum closed. Section 3 applies to S.

It is also invariant under complement, since complement exchanges direct and skew sums. Let Π_n be uniform in S_n, and set

    D(μ)=∫|x−y| dμ(x,y).

Reflection of the permuton through y=1/2 corresponds exactly to complement under the square convention. For every x,y,

    |x−y| + |x−(1−y)| ≥ |2x−1|.

The uniform X-marginal and complement invariance imply

    2 E D(μ_{Π_n}) ≥ ∫_0^1 |2x−1| dx = 1/2,
    E D(μ_{Π_n}) ≥ 1/4.

Since 0≤D≤1, the estimate E D ≤ 1/8 + (7/8)P(D>1/8) gives

    P(D(μ_{Π_n})>1/8) ≥ 1/7.

The function |x−y|/√2 has sup norm at most 1 and Lipschitz constant 1, and vanishes on the diagonal. Therefore

    P(d_BL(μ_{Π_n},μ_I)>1/(8√2)) ≥ 1/7                            (3.2)

for every n. This class simultaneously satisfies (3.1) and fails diagonal concentration by (3.2). No pre-existing theorem about random separable limits is needed for this example.

This is **not** a counterexample to Av(α⊖1). Its sole purpose is to invalidate the inference “sum closure plus full exponential growth in diagonal neighborhoods proves the uniform diagonal limit.”

## 4. Exact reduction from permuton distance to finite cut masses

For any permuton μ define

    c_μ(t)=μ([0,t]×(t,1]),   0≤t≤1,
    M(μ)=sup_t c_μ(t),
    D(μ)=∫|x−y| dμ.

Uniform marginals imply that the opposite crossing rectangle has equal mass:

    μ((t,1]×[0,t])=c_μ(t).

The function c_μ is 1-Lipschitz. To see this for s<t, write c_μ(t)−c_μ(s) as the mass gained in (s,t]×(t,1] minus the mass lost in [0,s]×(s,t]. Each term lies in [0,t−s], so their difference lies in [−(t−s),t−s]. Also c_μ(0)=c_μ(1)=0.

Tonelli's theorem gives

    D(μ)=2∫_0^1 c_μ(t)dt.

Since a 1-Lipschitz nonnegative function with boundary values zero and height M contains a triangle of area M² under its graph,

    2 M(μ)^2 ≤ D(μ) ≤ 2 M(μ).                                      (4.1)

The coupling and test function already used give

    D(μ)/√2 ≤ d_BL(μ,μ_I) ≤ D(μ).                                 (4.2)

It follows that the target is equivalent to M(μ_{Π_n})→0 in probability. Equivalently, it suffices to show c_{μ_{Π_n}}(t)→0 in probability for every t in any fixed dense subset of [0,1]. For each prescribed tolerance, a fixed finite mesh and the 1-Lipschitz bound reduce the supremum to finitely many cut events. This avoids an unjustified union bound over n² point probabilities.

At the grid cut t=k/n,

    c_{μ_π}(k/n) = (1/n)|{i≤k : π(i)>k}|,

exactly under the square convention; boundaries have zero permuton mass.

The unresolved task is therefore the positive-mass estimate, for each fixed t∈(0,1) and ε>0,

    P(|{i≤⌊tn⌋ : Π_n(i)>⌊tn⌋}| ≥ ε n) → 0.                       (4.3)

No estimate in Sections 1–3 proves (4.3).

## 5. Why an independent-quadrant entropy bound is insufficient

Let b_r=|Av_r(α)| and suppose |α|≥2, so its finite growth rate λ_α is positive. For completeness, any nonempty pattern is either direct-sum indecomposable or skew-sum indecomposable: a nontrivial direct-sum cut prevents a nontrivial skew-sum cut. Its avoidance class is therefore closed under at least one of these operations, so Fekete gives the growth limit; Marcus–Tardos gives finiteness. Also Av(α) is contained in Av(τ), so λ_α≤λ. For a τ-avoider with π(i)=j let

    r=|{p<i : π(p)>j}|.

The northwest subpermutation has size r and must avoid α: otherwise that occurrence followed by (i,j) would form τ. Each of the other three quadrant subpermutations avoids τ. Allocating positions and values independently therefore gives the valid upper bound

    |{π∈Av_n(τ): π(i)=j, NW size=r}|
    ≤ binom(i−1,r) binom(n−i,n−j−r)
      × binom(n−j,r) binom(j−1,i−1−r)
      × b_r a_{i−1−r} a_{n−j−r} a_{j−i+r}.                       (5.1)

Terms with impossible cell sizes are zero. Each actual permutation has a unique choice of the four position/value allocations and of the four internal patterns, so (5.1) cannot undercount. It overcounts because it ignores forbidden occurrences spanning cells.

Set i=j=⌊n/2⌋ and r=⌊c n⌋ for fixed 0<c<1/2. Stirling's formula and the avoidance growth limits show that the nth root of the right-hand side tends to the exponential of

    log λ + 2 h(2c) − c log(λ/λ_α),                               (5.2)

where h(u)=−u log u−(1−u)log(1−u). Since

    2 h(2c) / c → ∞ as c↓0,

(5.2) strictly exceeds log λ for every sufficiently small fixed c>0, no matter what fixed finite ratio λ/λ_α is. Dividing this upper bound by a_n gives an exponentially growing, hence vacuous, upper bound on the relevant probability.

This does not assert that the actual constrained count has that large an exponent. It establishes exactly that the local avoidance requirements and independent allocations used in (5.1) do not themselves supply the needed exponential gap near the diagonal. A successful counting proof must recover additional intercell compatibility, a more efficient encoding, or subexponential information.

## 6. What has and has not been established

Established with complete arguments here:

1. A direct injection yielding full exponential growth of every upper point probability when α is not maximum-first.
2. With the credited ratio theorem, a positive limiting probability of a single extreme upper-left point in those same target cases.
3. Full exponential growth inside arbitrarily small fixed diagonal neighborhoods for every sum-closed exponentially bounded class, and an explicit non-target class disproving the inference from that fact to concentration.
4. Exact bounded-Lipschitz, transport-cost, and crossing-cut estimates reducing the target to (4.3).
5. A valid quadrant-count inequality and a proof that its independent-cell entropy relaxation is vacuous for small positive crossing density.

Not established:

- No positive-probability asymptotic departure in d_BL for any fixed target pattern τ=α⊖1.
- No proof of (4.3) for arbitrary fixed α.
- No new covered family beyond the already credited literature.
- No conclusion that a speed-n large-deviation theorem for positive permuton mass is impossible: Section 2 only rules out such a statement for individual-point occupation/maximal displacement.
- No claim of novelty or literature-exhaustive openness.

The decisive gap is control of a positive fraction of crossing points under the exact uniform law. Exceptional single points, maximum-displacement estimates, full growth-rate equalities, and independent quadrant enumeration do not bridge that gap.
