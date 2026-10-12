# The logarithmic normalization is incompatible with topological conjugacy

**Status: complete obstruction for the explicit topological-conjugacy formulation; broader source question held unresolved, 1/5 approaches. Separate review pending.** No historical-priority claim is made.

For every prime p, multiplication by p and by p(1+p²) on Q_p are conjugate by a surjective isometry, although their p-adic logarithms differ. Thus no invariant of topological conjugacy can have the proposed values on all multiplication maps. The same contradiction uses expanding maps after taking inverses.

Ward's original question calls topological-conjugacy invariance an example of a desired axiom, not a complete definition of every possible entropy-like construction. The theorem below resolves that precise formulation. It does not refute the broader entropy/period program, and it is compatible with Deninger's credited periodic-entropy results on compact algebraic systems.

## 1. Exact setting and source qualification

Fix a prime p. Normalize the valuation by v_p(p)=1 and the metric by |x|_p=p^(−v_p(x)). The scalar λ must belong to Q_p^× for multiplication T_λ:x↦λx to act on Q_p. The branch log_p:C_p^×→C_p satisfies log_p(p)=0 and agrees with the convergent logarithmic power series on 1+p²Z_p. Only values in Q_p^× are needed here.

In [Ward, Six problems in algebraic dynamics, updated December 2006](https://www.imath.kiev.ua/~skolyada/kevin.pdf), Problem F, pp.2–4, the specific local request is for h_p(T_λ)=log_p λ, with topological-conjugacy invariance suggested parenthetically. The preceding discussion concerns Mahler measures and mixed-motive periods; the update already credits progress through Deninger's different algebraic-action construction. Neither an arbitrary number field nor a motive enters the elementary local normalization stated in the question.

The precise pair of requirements tested here is:

1. If a homeomorphism H:Q_p→Q_p satisfies H T_λ H^(−1)=T_μ, then h_p(T_λ)=h_p(T_μ).
2. For every λ∈Q_p^×, h_p(T_λ)=log_p λ.

Topological conjugacy in item 1 means conjugacy by a homeomorphism of the underlying spaces. It does not require H to be an additive-group homomorphism. That stricter category is discussed below rather than silently substituted.

## 2. Shellwise isometric conjugacy

**Lemma.** Suppose λ,μ∈Q_p^× have the same nonzero valuation a. Put u=μ/λ, so |u|_p=1. Define

    H(0)=0,
    H(x)=u^floor(v_p(x)/a) x,    x≠0.          (1)

Then H is a surjective isometry of Q_p and H T_λ=T_μ H.

**Proof.** The power in (1) is an integer, so it is defined even when a or v_p(x) is negative. Multiplication by that power of u leaves the valuation unchanged. Hence the inverse is explicitly

    H^(−1)(0)=0,
    H^(−1)(y)=u^(−floor(v_p(y)/a)) y,    y≠0.

If v_p(x)=v_p(y), the same unit multiplies both numbers, giving |H(x)−H(y)|_p=|x−y|_p. If their valuations differ, both distances equal max{|x|_p,|y|_p} by the ultrametric inequality and preservation of each valuation. The case where one point is zero is immediate. Thus H and its inverse are isometries, including at zero.

For x≠0, v_p(λx)=v_p(x)+a and

    floor((v_p(x)+a)/a)=floor(v_p(x)/a)+1.

This identity holds for negative a as well. Therefore

    H(λx)=u^(floor(v_p(x)/a)+1) λx=μH(x).

It also holds at zero. This proves the lemma. □

The conjugacy also preserves additive Haar measure. Each clopen shell {x:v_p(x)=k} is mapped to itself by multiplication by a fixed unit, which preserves that measure. Decomposing a Borel set into these countably many shells and its zero point proves the assertion. This is a measure-preserving conjugating map; the scalar maps themselves need not preserve Haar measure.

## 3. A nonzero logarithm for every prime, including 2

Set u=1+p². On this principal unit,

    log_p u = Σ(n≥1) (−1)^(n+1) p^(2n)/n.     (2)

The first term has valuation 2. For n≥2,

    v_p(p^(2n)/n)=2n−v_p(n)≥n+1≥3.

Here v_p(n)≤n−1, since p^(v_p(n))≤n and 2^r≥r+1. These valuations also tend to infinity, so the series converges. Its tail is in the closed ideal p³Z_p. Consequently

    log_p(1+p²) ≡ p² mod p³Z_p,
    v_p(log_p(1+p²))=2.                      (3)

In particular the logarithm is nonzero. Using p² avoids any exceptional first-term cancellation at p=2.

**Theorem.** No function satisfying both requirements in Section 1 exists, for any prime p. The incompatibility already occurs within the contracting maps of valuation 1, and also within the expanding maps of valuation −1.

**Proof.** Apply the lemma to λ=p and μ=p(1+p²). The conjugacy simplifies to

    H(x)=(1+p²)^(v_p(x)) x,    x≠0,

with H(0)=0. Requirement 1 makes the two h_p values equal. Requirement 2 instead gives

    h_p(T_p)=0,
    h_p(T_(p(1+p²)))=log_p(1+p²)≠0,

by the logarithm's homomorphism property and (3). This is a contradiction.

Taking inverses preserves the same conjugacy. The multipliers 1/p and 1/[p(1+p²)] both have p-adic absolute value p>1, while their logarithms are 0 and −log_p(1+p²). Thus restricting the normalization to expanding multipliers does not avoid the obstruction. □

In fact, the lemma shows that any invariant under isometric conjugacy must be constant on each nonzero-valuation class of scalar multipliers. The p-adic logarithm is not constant on such classes.

## 4. Why an algebraic-conjugacy restriction is different

The explicit H need not be additive. In the concrete contraction example, H(1)=1 and H(p−1)=p−1, but H(p)=p(1+p²). Thus H(1)+H(p−1)≠H(p).

Every continuous additive map A:Q_p→Q_p is Q_p-linear: additivity gives rational linearity, and continuity extends it from the dense subfield Q to Q_p. A continuous additive automorphism therefore has the form A(x)=cx with c≠0. Such maps commute with all scalar multiplications. Hence additive-group conjugacy between T_λ and T_μ forces λ=μ.

Accordingly, the elementary assignment log_p λ is invariant in that more restrictive category. This observation is not a construction of an entropy with additional dynamical or motivic properties. It explains exactly which category the obstruction uses. No impossibility assertion for every unspecified meaning of entropy-like is justified by the theorem.

## 5. Compatibility with credited p-adic periodic entropy

[Deninger, p-adic entropy and a p-adic Fuglede–Kadison determinant](https://arxiv.org/abs/math/0608539), introduction equations (1.2)–(1.3), defines p-adic periodic entropy using normalized p-adic logarithms of finite fixed-point counts, when the relevant limit exists. Those counts are preserved by any set-theoretic conjugacy. For a scalar with |λ|_p≠1, the only fixed point of every positive iterate on Q_p is zero: λ^n≠1 and (λ^n−1)x=0 imply x=0. Thus this definition gives zero on each local scalar map in the theorem. It does not meet the proposed scalar-logarithm normalization.

The same paper's Theorem 1.1 identifies periodic entropy with the p-adic Mahler measure for the compact algebraic Z^d-action

    X_f = (Z[t_1^(±1),…,t_d^(±1)]/(f))^,

provided the integer Laurent polynomial f has no zero on the p-adic unit torus. The hat denotes Pontryagin duality. This is a credited theorem, not reproved here.

For a concrete comparison, let u=1+p² and f(t)=pt−u. Its root u/p has absolute value p>1, so the nonvanishing hypothesis holds. The p-adic Jensen formula recorded in the same paper, equation (1.6), gives

    m_p(f)=log_p p+log_p(u/p)=log_p u≠0.

Deninger's theorem assigns this value to the associated **compact** system X_f. The local space Q_p is noncompact, and no identification or conjugacy of these two systems is asserted. This compact theorem and the local no-go theorem are fully compatible.

The later [Katagiri work](https://www.jstage.jst.go.jp/article/kodaimath/44/2/44_323/_pdf), published in [Kodai Mathematical Journal 44 (2021), 323–333](https://doi.org/10.2996/kmj44207), gives related formulas for number-field coefficient rings and selected compact solenoids with explicit expansiveness hypotheses. It does not replace Q_p multiplication by an equivalent compact system or supply the impossible local normalization.

## 6. Disposition and checks

The precise topological-conjugacy formulation has a complete negative answer above, proved for all primes with no compactness, smoothness or analytic-conjugacy assumption added. The original parenthetical wording leaves a broader, unspecified entropy/period program, parts of which were already addressed by the credited sources. Therefore the conservative queue recommendation for the unqualified original record is **unsolved, 1/5, with a complete scoped obstruction**. A separately worded target imposing both explicit axioms would be resolved negatively.

The accompanying finite rational and residue-ring controls check the conjugacy, inverse, distance preservation, negative valuations, general nonzero valuation a, and logarithmic leading term. They support the written all-prime argument and do not replace it with finite-precision evidence. Historical priority for this elementary obstruction has not been established. No new theorem concerning mixed motives or their periods is claimed.
