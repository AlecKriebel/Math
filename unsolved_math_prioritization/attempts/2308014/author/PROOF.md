# Positive scalar Hankel symbols: an explicit classification

Problem 2308014 (AMR-022-8014), Function Theory Problem 8.14.

**Disposition:** a full characterization under the standard scalar Hankel convention, recovered from established moment/Hankel theory. This is an authored verification and explicit reconstruction, not a claim of a new theorem or of historical priority. Independent review is pending.

## 1. Conventions and statement

Let T be the unit circle, with normalized Lebesgue measure dm=dθ/(2π). For f in L∞(T), put

    a_n(f) = ∫_T f(z) z^n dm(z),    n=0,1,2,... .

The operator H_f on ℓ²(N₀) has matrix (a_{j+k}(f))_{j,k≥0}. “Positive” means positive semidefinite as a complex Hilbert-space operator. It does not mean that f has nonnegative values, that the matrix entries are nonnegative, or that all minors are nonnegative.

The matrix defines a bounded operator: for finite vectors c,d,

    |Σ_{j,k} a_{j+k} c_k conjugate(d_j)|
      = |∫ f(z)(Σ_k c_k z^k)(Σ_j conjugate(d_j) z^j) dm(z)|
      ≤ ||f||∞ ||c||₂ ||d||₂.

Thus finite sections determine H_f, with ||H_f||≤||f||∞.

Let M be the following explicitly specified class of measures. A member μ is a finite positive Borel measure on (−1,1) for which some finite K≥0 satisfies

    μ({x: 1−|x|≤r}) ≤ Kr     (0<r≤1).                 (E)

This is equivalent to separate O(r) bounds at the two endpoints. It permits arbitrary singular or atomic behavior in the interior. Write m_μ=μ((−1,1)). For z∈T\{−1,1}, define

    g_μ(z) = m_μ + ∫_(−1,1) [1/(1−x/z) − 1/(1−xz)] dμ(x).      (G)

Assign any finite values at z=±1; they have no effect in L∞.

**Theorem.** Exactly the following functions generate positive H_f:

    f(z) = g_μ(z) + z h(z) a.e.,
    where μ∈M and h is the boundary function of an arbitrary H∞(D) function.

The measure μ is unique for each f. The representative g_μ is bounded, with the deliberately nonoptimal bound

    ||g_μ||∞ ≤ m_μ + 50K.

Equivalently, H_f≥0 precisely when the sequence a_n(f) consists of the moments ∫x^n dμ(x) of a positive measure on (−1,1). For f already in L∞, condition (E) follows automatically from this moment property. For constructing all admissible symbols from measures, (E) is essential.

## 2. Necessity: positivity gives the endpoint-controlled moment measure

Suppose H_f≥0 and let M=||H_f||. The Hankel matrix is symmetric; since positivity implies Hermitian symmetry, every a_n is real. Its finite quadratic forms are nonnegative. Hamburger's moment theorem therefore gives a finite positive Borel measure μ on R such that

    a_n = ∫_R x^n dμ(x),     n≥0.

This standard theorem is the only moment-existence theorem used here. A modern source explicitly applying it in this bounded-Hankel setting is Adamo–Neeb–Schober, Definition 2.4 and its following paragraph [ANS].

The even moments satisfy 0≤a_{2n}≤M. If μ had positive mass where |x|≥1+δ for some δ>0, these moments would grow at least as (1+δ)^(2n) times that mass. Hence μ is supported on [−1,1]. Because f∈L¹(T), the Riemann–Lebesgue lemma gives a_{2n}→0. Dominated convergence on [−1,1] shows that μ({−1,1})=0. The measure is unique: equal moments give equal integrals of polynomials, hence of continuous functions on [−1,1], hence equal finite Borel measures.

For a polynomial p(z)=Σ c_j z^j,

    ∫ |p(x)|² dμ(x) = ⟨H_f c,c⟩ ≤ M Σ|c_j|².        (1)

Fix 0<r<1 and approximate k_r(z)=1/(1−rz) by its finite geometric sums. They converge uniformly on [−1,1], and their squared coefficient norms converge to 1/(1−r²). Passing to the limit in (1) gives

    ∫_(−1,1) 1/(1−rx)² dμ(x) ≤ M/(1−r²).

For x≥r, 1−rx≤1−r², so

    μ([r,1)) ≤ M(1−r²) ≤ 2M(1−r).

Using k_−r gives likewise

    μ((−1,−r]) ≤ 2M(1−r).

Consequently (E) holds with K=4M for 0<r<1 after replacing r by the endpoint distance; at r=1 it follows from μ((−1,1))=a₀≤M. This also handles M=0.

This establishes the entire necessity of the measure condition, including endpoint exclusion. No finite-matrix test is substituted for the infinite operator.

## 3. The integral representative really is bounded

Fix z=e^(iθ) with s=|sin θ|>0. Put q=|x| and u=1−q. The difference kernel in (G) has absolute value

    2|x sin θ| / (1−2x cos θ+x²).

Since 2(1−|cos θ|)≥sin² θ,

    1−2x cos θ+x² ≥ u²+q s² ≥ (u²+s²)/5.

For the last inequality, if u≥1/2 then s²≤1≤4u²; if u<1/2 then q>1/2. Thus the kernel is at most 10s/(u²+s²).

Let ν be the pushforward of μ under x↦1−|x|. Condition (E) says ν((0,t])≤Kt for 0<t≤1. It also holds for t>1 because ν has mass at most K and is supported on (0,1]. Split this interval into u≤s and bands 2^j s<u≤2^(j+1)s, j≥0. The first contributes at most 10K. Band j contributes at most

    [10/(2^(2j)s)] · K 2^(j+1)s = 20K 2^(−j).

Summing proves that the integral in (G) has absolute value at most 50K. All integrals are ordinary absolutely convergent integrals for z≠±1. In particular g_μ is a well-defined L∞ function.

The endpoint control has not been replaced by a stronger integrability hypothesis such as ∫(1−x²)^(−1)dμ<∞. That stronger condition would wrongly exclude familiar bounded Hankel examples.

## 4. Its required Fourier coefficients are precisely the moments

First restrict μ to [−r,r], with r<1, and call the resulting measure μ_r. The geometric series converge uniformly for |x|≤r, z∈T, so

    g_(μ_r)(z) = m_(μ_r) + Σ_(n≥1) (∫x^n dμ_r(x))(z^(−n)−z^n).

Therefore

    ∫_T g_(μ_r)(z) z^n dm(z) = ∫x^n dμ_r(x)   for every n≥0.    (2)

All μ_r satisfy (E) with the same K. The representatives are uniformly bounded by m_μ+50K. For z≠±1 their defining integrals converge to that of μ as r↑1, because the kernel is bounded in x on [−1,1] for fixed such z. Dominated convergence in (2), and then in the moment integral, proves

    a_n(g_μ)=∫x^n dμ(x)    for all n≥0.                         (3)

This limiting argument is needed: an uncontrolled interchange of the geometric series with a measure accumulating at ±1 would not suffice.

## 5. All representatives, and sufficiency

For the positive H_f considered in Section 2, equations (3) give a_n(f−g_μ)=0 for all n≥0. In the Fourier convention here, these are exactly the coefficients with indices 0,−1,−2,... . A bounded function whose coefficients with those indices vanish is the boundary function of a bounded analytic function with zero constant term, hence belongs to zH∞.

For completeness, take its Poisson extension. Vanishing of all nonpositive Fourier coefficients makes that extension analytic and zero at the origin; the Poisson bound keeps its norm at most the L∞ norm of the boundary function. Dividing by z remains bounded by Schwarz's lemma (with the zero function treated separately). Radial boundary convergence identifies the original function almost everywhere. Thus f=g_μ+zh as asserted.

Conversely, take μ∈M and h∈H∞. Section 3 makes f=g_μ+zh bounded. The added term has a_n(zh)=0 for every n≥0. Equation (3) then yields, for every finite vector c,

    Σ_{j,k} a_{j+k}(f)c_k conjugate(c_j)
      = ∫_(−1,1) |Σ_k c_k x^k|² dμ(x) ≥ 0.

Since H_f is bounded, density extends this positivity from finite vectors to all ℓ². This proves sufficiency and completes the characterization.

## 6. Other common Hankel conventions

If instead the matrix is (f̂(−j−k−1))_{j,k≥0}, where f̂(n)=∫f(z)z^(−n)dm, it is exactly H_(zf) in the convention above. The classification becomes

    f = z^(−1)g_μ + h,    μ∈M, h∈H∞.

If positive rather than negative Fourier indices are used, replace f(z) by f(conjugate(z)); this reverses the boundary orientation. These changes must be made before comparing a formula in another source. In particular the n=0 and n=1 conventions have different annihilators: zH∞ versus H∞. The source's quotient-space notation is not relied upon to decide that constant-term issue.

## 7. Scope and prior work

The Hamburger/Widom classification and bounded-symbol theory already supply the mathematical content of the problem in this standard interpretation. [ANS] records the measure classification and endpoint criterion, constructs a bounded symbol on the half-plane in Theorem 4.1, and transfers symbols to the circle in equation (21). The proof above gives a direct circle reconstruction so that signs, the constant coefficient, and the admissible measures can all be checked without relying on an implicit convention. No novelty is asserted.

The 2018 list says that no progress had been reported to its editors; that sentence is a historical report, not a present-day impossibility theorem. No inspected primary source explicitly announces “Holland Problem 8.14 solved.” Accordingly the conclusion here is a **verified mathematical reduction to prior theory**, subject to independent audit, rather than a claim about who first resolved the named historical problem. No broader notion of strict positivity, matrix-valued symbol, or multivariable Hankel operator is covered.

[ANS] M. S. Adamo, K.-H. Neeb, J. Schober, *Reflection positivity and Hankel operators—the multiplicity free case*, arXiv:2105.08522v1 (2021), subsequently Journal of Functional Analysis 283 (2022), article 109493. Primary full text: https://arxiv.org/abs/2105.08522 ; DOI: https://doi.org/10.1016/j.jfa.2022.109493 .
