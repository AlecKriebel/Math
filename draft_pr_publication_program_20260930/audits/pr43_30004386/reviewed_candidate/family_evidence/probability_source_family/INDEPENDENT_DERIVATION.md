# Independent probability derivation

Written UTC: 2026-10-02T23:22:16.251146+00:00. This is a checkable independent audit derivation of an existing theorem, not a novelty claim. Canonical compactness, continuity and injectivity were already sealed before the later paper was read. This file supplies the exact missing sphere-probability estimates and repairs identified display issues in the accessible preprint.

Let W={a₁≥a₂≥…≥0, Σaᵢ²≤1} with coordinate topology. Write J(a)=−½log(1−Σaᵢ²) for norm<1 and +∞ for norm=1. Let η_N be decreasing absolute sphere coordinates padded by zeros.

For fixed m and N>m+2 the first m **labeled** coordinates have density

    f_N,m(z)= Γ(N/2)/(π^(m/2)Γ((N−m)/2)) · (1−||z||²)^((N−m−2)/2), ||z||<1.

The prefactor has logarithm o(N), by the fixed-shift Gamma asymptotic. Signs and **ordered** coordinate choices give at most 2^m(N)_m possibilities, with logarithm o(N). The factor (N)_m=N!/(N−m)! is safe; an unordered binomial factor alone misses m!.

Define C(a;m,r)={w∈W:||(w₁,…,w_m)−(a₁,…,a_m)||<r}. This is a neighborhood base. Put a^[m]=(a₁,…,a_m). By union bound, integrating the labeled density on the ball and using ||z||≥(||a^[m]||−r)_+, one obtains

    limsup_N (1/N)log P(η_N∈C(a;m,r))
      ≤ ½log(1−((||a^[m]||−r)_+)²).

If the right side involves 1−1, interpret it by taking radii to zero, rather than evaluating an empty open ball. The density estimate only uses N eventually larger than fixed m+2. At a=0 its upper bound is 0, as required.

For the matching local lower estimate, first suppose x₁≥…≥x_m>0 and ||x||<1. Restrict the first m labeled coordinates to a strict decreasing positive wedge within radius 1/N of x. That wedge has volume at least v_m/(2^m m!N^m): shift the strictly decreasing positive portion of the radius-1/N ball at the origin by x, which remains in the chamber; for N large the norm is below1. On the wedge, ||z||≤||x||+1/N. Conditionally on z, the remaining coordinates are uniform on the residual sphere of radius sqrt(1−||z||²)≤1. Their maximum is less than x_m/2 with probability tending to1 **uniformly** in z. One elementary proof uses Y=G/||G||, a union Gaussian tail bound for max|G_j| at threshold c√d, and Chebyshev for ||G||²/d; for every fixed c>0, P(max|Y_j|≥c)→0. Thus the conditional factor is ≥1/2 for all N large. All specified labeled coordinates are the top m in decreasing order. It follows that, for every fixed r>0,

    liminf_N (1/N)log P(η_N∈C(x;m,r)) ≥ ½log(1−||x||²).

Ties in x cause no loss because the strict wedge still has the stated positive volume. If some x_i=0, choose strictly decreasing positive x^(ε)→x with ||x^(ε)||<1 and a ball about x^(ε) inside the desired fixed neighborhood of x. Apply the preceding estimate, then let ε→0. This explicit limiting step is required; merely replacing x by one arbitrary positive perturbation would change its cost. For finite-rate a, ||a^[m]||<1 and hence

    liminf_N (1/N)log P(η_N∈C(a;m,r)) ≥ ½log(1−||a^[m]||²) ≥ −J(a).

For ||a||=1 the desired bound −J(a)=−∞ is vacuous. Taking r↓0 and then m→∞ in the upper estimate recovers −J(a), including boundary cost+∞. This proves the exact local rates.

To turn these into full bounds without importing a projective-LDP theorem, let F⊂W be closed, hence compact. For any finite c<inf_F J, each a∈F has some m and sufficiently small r whose upper estimate is at most −c. F has a finite cover by these neighborhoods; the finite union preserves limsup≤−c. Let c↑inf_F J (or c→∞). For open G and any a∈G with J(a)<∞, choose one basic neighborhood contained in G; its lower estimate is ≥−J(a). Take the infimum over a∈G; if G has only infinite-rate points the lower bound is trivial. J is lower semicontinuous because its finite-level set is {Σaᵢ²≤1−exp(−2L)}, closed by Fatou. Since W is compact the rate is good. These estimates establish a full LDP on W, speedN.

The characteristic map Φ(a)=κ_a is continuous: for fixed t and m with |t|/sqrt(m+1) small, the tail log has expansion

    log[exp(−(1−Σaᵢ²)t²/6)Π_{i>m}sinc(aᵢt)]
     = −(1−Σ_{i≤m}aᵢ²)t²/6 + R_m(a,t),
    |R_m(a,t)|≤C_t Σ_{i>m}aᵢ⁴≤C_t/(m+1),

uniformly on W. The finite prefix Π_{i≤m}sinc(aᵢt) is continuous, so Φ is weakly continuous even when its limiting prefix is zero. **Do not divide by the full limiting characteristic function at a zero.** Φ is injective by recovering its smallest positive zero π/a₁ and its multiplicity, dividing out only the analytic recovered sinc factors, and iterating. For a=0 there are no zeros. Nonzero tails avoiding individual zeros have absolutely summable log factors, so they introduce no extra zeros. Compactness of W and Hausdorffness of P(R) make Φ a homeomorphism onto compact K.

Because Φ(η_N)=μ_{Θ^(N)}, the preimages of weakly open/closed sets give the full LDP on K. On P(R), extend rate by+∞ off K: K is closed and all μ_{Θ^(N)} lie in K, so the same bounds apply to arbitrary open/closed sets. Its finite-level sets are compact. The only zero is a=0, namelyN(0,1/3). The whole closed canonical ball maps toK, including norm-one infinite-rate laws; the finite domain is Φ({||a||<1}).

For the limit-set assertion, every sequence has a canonical coordinate-convergent subsequence by compactness, and continuity puts its weak limit inK. Conversely, for a∈W choose m(N)=floor(sqrt(N)) (adjust N=1 harmlessly). Keep its first m(N) coefficients and fill the remaining N−m(N) entries by b_N=sqrt((1−Σ_{i≤m(N)}aᵢ²)/(N−m(N))). The unsorted vector has normone, b_N→0, and its sorted absolute coordinates converge coordinatewise toa. For any fixed positive a_j, eventually b_N<a_j; zero coordinates are bounded by b_N and vanishing tails. Continuity proves μ_{θ^(N)}→κ_a. ThusK is exactly the possible Prohorov limit set.

Rate well-definedness for arbitrary signed/reordered ℓ² coefficients follows by the canonicalization and injectivity above. In particular no norm-one law can secretly have a norm<1 representation. Moments cannot replace this argument: every member has the same variance1/3, while coordinate topology permits escape of coefficient norm into Gaussian variance.
