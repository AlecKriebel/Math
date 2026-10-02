# Turn 5: a critical convex statistic, but a large gap from another type

Problem 30003472 / OWR-15427-014. **Fifth and final substantive author turn.**

**Two outcomes, both essential:** the convex-position probability can have the critical counting scale n^(−3n+O(n)) even for a purely singular measure giving positive probability to every finite type. Nevertheless, the same construction has a very large max/min type-probability gap, because it contains a positive-weight component with few possible sampled types. It is **not a counterexample or a surviving unsolved instance** of the original question.

The unrestricted original target remains unresolved after **5/5** turns. No sixth author search is included.

## 1. Final theorem

For every β>0 there is a compactly supported Borel probability measure μ_β on the plane with the following properties:

1. It is purely singular with respect to area, charges no line, and has topological support equal to the closed unit disk. Every finite realizable simple order type therefore has positive probability.
2. Its convex-position probability satisfies

       p_{μ_β}(conv_n) = n^(−βn) exp(O_β(n)).             (1)

3. There is a constant c_β>0 such that, for every n≥3,

       max_ω p_{μ_β}(ω) / min_ω p_{μ_β}(ω)
         ≥ 4096 (c_β n³)^n.                            (2)

In particular β=3 places the convex statistic at the usual n^(−3n+O(n)) order-type counting scale, while (2) still proves a much larger-than-exponential gap. The useful heavy type need not be the convex one.

All constants may depend on β and on the fixed seed component. These results make no assertion of a size threshold uniform over arbitrary measures. Historical novelty of the construction is not certified.

## 2. A credited fractal seed and its binary coding

Use the Erdős–Szekeres measure constructed in [Goaoc et al., Limits of Order Types](https://arxiv.org/pdf/1811.02236), §3.4, Lemma 3.15 and Proposition 17. An explicit admissible choice is a=1/4 and b=1/16 in the two affine contractions

    f_0(x,y)=(a x,b y),
    f_1(x,y)=(1−a+a x,1−b+b y),

with independent fair binary digits. The condition in Lemma 3.15 holds because

    b=1/16 ≤ a(1−2a)(1−2b)=7/64.

Call the resulting compactly supported probability measure σ. The cited construction says that, for lexicographically increasing distinct binary sequences u<v<w, the orientation of their three image points is determined by whether the common-prefix length of u,v is smaller or larger than that of v,w. Those two lengths are distinct. In particular, no three distinct support points are collinear. The coding is injective and nonatomic, so σ charges no line.

Its support has area zero: at depth j it is covered by 2^j rectangles with both side lengths at most a^j, so its Hausdorff dimension is at most log(2)/log(4)=1/2. Proposition 17 supplies

    p_σ(conv_m) = 2^(−m²/8+O(m log m)).                  (3)

We only need the consequence that there exist κ>0 and D≥1 with

    p_σ(conv_m) ≤ D^m exp(−κm²),   m≥0.                 (4)

Increasing D handles the finitely many small m, and m=0 is assigned probability one. This use of the source does **not** depend on the regularity argument of its Lemma 3.16 discussed in earlier turns.

There is also a useful support-complexity fact that follows directly from the binary coding. Sort n sampled sequences lexicographically and contract all unary vertices of their finite distinguishing trie. The result is an ordered full binary tree with n leaves. For any three leaves in increasing order, their two relevant lowest common ancestors lie on the middle leaf's ancestor chain; which is deeper is unchanged by contracting unary vertices. Thus the compressed tree determines every orientation sign.

There are Catalan(n−1) ordered full binary trees with n leaves. Consequently the number S_n of unlabeled order types with positive σ-probability satisfies

    S_n ≤ Catalan(n−1) ≤ 4^(n−1),
    max_ω p_σ(ω) ≥ 4^(1−n).                             (5)

No assertion that distinct trees give distinct unlabeled types is needed.

## 3. Infinitely many convexly separated neighborhoods

We need countably many small balls B_j such that every finite choice of one point from distinct balls is in convex position. Here is an explicit construction.

Put x_j=2^(−j), p_j=(x_j,x_j²), and let B_j be the closed Euclidean ball centered at p_j with radius x_j²/128. Define the affine functional

    L_i(x,y)=y−2x_i x+x_i²−x_i²/16.

At p_i its value is −x_i²/16. For j≠i, writing z=x_i/x_j gives

    L_i(p_j)/x_j² = (1−z)²−z²/16.

Here z is a power of two different from one. For z≤1/2 the minimum is 15/64 at z=1/2; for z≥2 the minimum is 3/4 at z=2. Thus L_i(p_j)≥15x_j²/64. The coefficient vector of L_i has norm at most √2<2. Perturbing p_j within B_j changes L_i by at most x_j²/64.

Therefore L_i is strictly negative throughout B_i and strictly positive throughout every other B_j. Each B_i is strictly separated from the convex hull of all the other balls by its own line. Every finite transversal is consequently in strictly convex position. All these balls lie inside the open unit disk.

## 4. The singular full-type-support mixture

Set α=β+1>1, Z_α=Σ_{j≥1}j^(−α), and

    w_j=j^(−α)/Z_α.

Choose positive homothetic images σ_j of the fixed seed σ as follows:

* σ_{2j−1} is supported inside B_j
* enumerate a countable basis of rational open balls whose closures lie in the open unit disk, and place σ_{2j} inside the jth such ball

The seed is compact, so each placement is possible with a sufficiently small positive homothety. Define

    μ_β = Σ_{j≥1} w_j σ_j.                              (6)

Every component is line-null, hence so is μ_β. It is carried by a countable union of area-null compact sets, so it is purely singular. Every open subset of the open unit disk contains a basis ball with a positive-weight component. All components lie in that disk, and its closure is therefore exactly the topological support.

Every finite simple configuration can be positively rescaled into the open unit disk and thickened to disjoint stable neighborhoods preserving all its orientations. Each neighborhood has positive μ_β-mass. Hence every finite simple type has positive probability. If desired, enumerating a basis of the whole plane instead gives a version with full planar support; none of the probability estimates below changes.

## 5. Lower bound for the convex probability

For a given n, select the n odd components indexed by 2j−1 with n≤j≤2n−1. Their weights are all at least Z_α^(−1)(4n)^(−α). The event that the n latent component labels visit these n components once each has probability at least

    n! [Z_α^(−1)(4n)^(−α)]^n.

Every resulting point set is convex by §3, regardless of its positions inside the component balls. Thus

    p_{μ_β}(conv_n)
      ≥ [Z_α^(−1) 4^(−α) e^(−1)]^n n^(−(α−1)n),       (7)

using n!≥(n/e)^n. The latent-label events are disjoint even if some unrelated component supports overlap.

## 6. Upper bound via occupancies and a positive generating series

Write p_m=p_σ(conv_m), taking p_0=1. If the complete sample is convex, the subsample with any one component label must be convex too. Conditional on the label occupancies, the component subsamples are independent and are homothetic copies of σ. Consequently

    p_{μ_β}(conv_n) ≤ n! [z^n] G(z),
    G(z)=Π_{j≥1} F(w_j z),
    F(t)=Σ_{m≥0} p_m t^m/m!.                            (8)

All coefficients are nonnegative. Since p_m≤1, F(t)≤exp(t) for t≥0, so the infinite product is finite and at most exp(z). Tonelli's theorem justifies the occupancy expansion. No formal exchange involving a conditionally convergent series is used.

For 0≤t≤1, log F(t)≤t. For t≥1, (4) and m!≥1 give

    F(t) ≤ Σ_{m≥0} exp(−κm²+m log(Dt)).

Completing the square bounds the last sum by a constant times
exp((log(Dt))²/(4κ)), because sums of translates of a Gaussian over the nonnegative integers are uniformly bounded. Therefore, for a fixed C_1,

    log F(t) ≤ C_1(1+log t)²,   t≥1.                    (9)

For sufficiently large z put H=(z/Z_α)^(1/α)≥2, so w_jz=(H/j)^α. Splitting at j=H gives

    log G(z)
      ≤ C_1 Σ_{j≤H} [1+α log(H/j)]²
         + H^α Σ_{j>H} j^(−α).

The first sum is at most its decreasing-function integral on (0,H), namely

    H ∫_0^1 [1+α log(1/u)]² du
      = H(1+2α+2α²).

The tail is at most 2^(α−1)H/(α−1), by integration from floor(H)≥H/2. It follows that, for some fixed B>0,

    log G(z) ≤ B z^(1/α)                                (10)

for all sufficiently large real z.

For a_n=[z^n]G(z), positivity of coefficients gives a_n≤G(z)/z^n for every z>0. Set z=(αn/B)^α, which lies in the regime of (10) for large n. Then

    p_{μ_β}(conv_n) ≤ n! exp(αn) [B/(αn)]^(αn)
                    ≤ [exp(α)(B/α)^α]^n n^(−(α−1)n).   (11)

Equations (7) and (11) prove (1), since α−1=β. The constants in these estimates do not depend on n. Increasing the upper constant covers any omitted finite initial range.

## 7. Why this same family has a large type-probability gap

A general component observation is useful. If μ≥wν for some probability measure ν and fixed w>0, and ν supports at most S_n simple n-types, then

    max_ω p_μ(ω) ≥ w^n/S_n.

Indeed one ν-type has probability at least 1/S_n, and the event that all n observations come from that component has weight w^n. Combining with min p_μ≤1/T_n gives

    max p_μ / min p_μ ≥ T_n w^n/S_n.                    (12)

Zero-probability types make the desired comparison immediate; the constructed mixture has none.

Apply (12) to any fixed σ_j component of (6), say j=1, and use (5) and the Turn 1 bound T_n≥1024(n!)³/128^n. We obtain

    max p_{μ_β} / min p_{μ_β}
      ≥ 4096 (n!)³ (w_1/512)^n
      ≥ 4096 [w_1 n³/(512e³)]^n,                       (13)

proving (2). For large n the heavy type in this argument cannot be the convex one, whose probability obeys (1).

More generally, a positive-weight component with S_n≤C^n n^(pn), p<3, yields an eventual gap of order [c n^(3−p)]^n. This is another sufficient mechanism, not a claim that every singular measure has such a component.

## 8. Exact meaning of the critical case and final gap

The classical counting scale is T_n=n^(3n+O(n)); see the primary counting discussion in [Goaoc–Welzl](https://arxiv.org/pdf/2003.08456), §1.3.1. The lower side was reproved explicitly in Turn 1. For β=3, equation (1) shows that the convex probability can occupy this same leading scale even with no zero-probability types and no absolutely continuous component.

This rules out a proposed universal dichotomy that convex probability must always be separated from the counting scale by a nonzero n log n exponent. It does **not** rule out an exponential comparison based on finer constants, and it certainly does not refute the original max/min question: (13) explicitly resolves every measure constructed here.

After five turns, the remaining task is still to prove or refute a universal exponential max/min comparison for arbitrary line-null measures, in particular purely singular full-type-support measures not known to admit any of the sufficient structures proved here. A measure-independent size threshold has not been obtained in the special-class results. The source's unquantified size parameter remains documented in SOURCE_GATE.md.

The same-type route in Turn 4 is universal but critical; the density, parabolic-product and low-support-component routes are rigorous but scoped. None is silently promoted to the unrestricted original claim. Final disposition: **exhausted, unresolved 5/5**. Completion estimate **30%**, subjective; it measures structural understanding, not a claimed fraction of a complete proof. No further author-search turn is authorized by this packet.
