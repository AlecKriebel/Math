# Function Theory 6.31: rigorous partial results and the unresolved gap

**Status: unsolved.** This document proves auxiliary results and a restricted-class rate theorem. It does not improve Duren's estimate for every member of S, establish its sharpness, or certify novelty of the auxiliary results.

## 1. Exact target and conventions

Let D={z: |z|<1}, and let S consist of holomorphic injective functions f:D→C with f(0)=0 and f′(0)=1. Write f(z)=Σ_{n≥1}a_n z^n. The source asks how much the known implication

    (1-r)^2 f(r)=λ+O((1-r)^δ), λ≠0, δ>0
    ⇒ a_n/n=λ+O(1/log n)

can be improved as r↑1 and n→∞. The constants may depend on f, λ, δ and the constant in the radial hypothesis. The radial hypothesis concerns the complex value f(r), along the positive radius only. Neither a two-dimensional asymptotic expansion nor a uniform bound over all of S is assumed.

Hayman–Lingham, arXiv:1809.07200v2, printed pp.128–129, Problem/Update 6.31, gives this formulation and reports no progress. Its reference [208] is P. L. Duren, *Estimation of coefficients of univalent functions by a Tauberian remainder theorem*, J. London Math. Soc. (2) 8 (1974), 279–282, DOI 10.1112/jlms/s2-8.2.279. The source-backed logarithmic theorem is background, not reproved here.

Put k(z)=z/(1-z)^2 and B(z)=(1-z)^2 f(z)/z, with the removable value B(0)=1. If B(z)=Σ_{j≥0}b_jz^j, ordinary power-series multiplication gives, for every n≥1,

    a_n/n = Σ_{j=0}^{n-1}(1-j/n)b_j.                      (1)

The radial hypothesis yields

    B(r)=λ+O((1-r)^ε), ε=min(δ,1).                       (2)

The loss to ε=1 comes from division by r; it must not be suppressed when δ>1. Equation (1) is a Cesàro mean of the partial sums of B's coefficients. An improvement for general S must exploit more than Abel convergence alone.

## 2. Approach 1: isolate the univalence obstruction

For any real u>0 define

    F_u(z)=z/(1-z)^2 + u z^2/(1+z)^2.

It is normalized and holomorphic in D. As r↑1,

    (1-r)^2 F_u(r)=r+u r^2(1-r)^2/(1+r)^2=1+O(1-r).

For n≥2 its coefficients satisfy

    [z^n]F_u / n = 1+u(-1)^(n-2)(1-1/n),

which has two different subsequential limits. Thus the radial hypothesis by itself does not even imply coefficient convergence.

This is deliberately not a counterexample in S. In fact

    F_u′(z) = ((1+z)^4+2uz(1-z)^3)/((1-z)^3(1+z)^3).

On the real interval (-1,0), the numerator has limiting value -16u at -1 and value 1 at 0. The intermediate value theorem gives an interior critical point, so F_u is not locally injective. This explicitly diagnoses the failure rather than leaving univalence untested.

**Exact remaining gap:** find an admissible mechanism in S that both preserves the radial error and controls or produces the phase cancellation responsible for slow coefficient convergence. Analytic examples outside S do not resolve this.

## 3. Approach 2: two-dimensional remainder control

### Proposition 1 (conditional angular transfer)

Suppose a holomorphic normalized f satisfies, for some λ∈C, C>0 and η>0,

    |f(z)-λ k(z)| ≤ C |1-z|^(-2+η),  z∈D.              (3)

Then

    a_n/n-λ = O(n^(-η))          if 0<η<1,
              O((log n)/n)     if η=1,
              O(1/n)           if η>1.                (4)

No univalence is needed for this conditional proposition.

**Proof.** Let E=f-λk and r=1-1/n, n≥2. Cauchy's coefficient formula gives

    |[z^n]E| ≤ r^(-n) C/(2π) ∫_{-π}^{π}|1-r e^(it)|^(-2+η) dt.

Here r^(-n)≤4. With s=1/n and r≥1/2,

    |1-r e^(it)|^2=s^2+2r(1-cos t)≥s^2+2t^2/π^2.

For 0<η<1, scaling t=s v bounds the integral by O(s^(-1+η)); the integral of (1+v^2)^(-1+η/2) on the real line is finite. At η=1, the bound is O(log(1/s)). For 1<η<2 it is O(1), by splitting |t|≤s and |t|>s. For η≥2 the integrand in (3) is bounded by 2^(η-2), again giving O(1). Since [z^n]k=n, division by n proves (4). □

**Exact remaining gap:** (3) is stronger than a radial estimate, even after capping the radial exponent at 1. No deduction of (3), or a substitute integrated estimate strong enough for (4), has been proved from the original S hypothesis. This proposition therefore cannot be promoted to the target theorem.

## 4. Approach 3: coefficient moments and an exact 1/n obstruction

### Proposition 2 (weighted absolute coefficient criterion)

For B above, suppose 0<s≤1 and

    M_s=Σ_{j≥1} j^s |b_j| <∞.

Let L=Σ_{j≥0}b_j. Then B(r)→L and

    |a_n/n-L|≤M_s n^(-s).                               (5)

If M_1<∞, put M=Σ_{j≥1}j b_j. Then more precisely

    a_n/n=L-M/n+o(1/n).                                 (6)

Moreover the coefficient-moment hypothesis itself implies

    (1-r)^2 f(r)=L+O((1-r)^s).

**Proof.** Absolute convergence follows since j^s≥1 for j≥1. Subtract L from (1):

    a_n/n-L = -Σ_{j≥n}b_j -(1/n)Σ_{j<n}j b_j.

For j≥n, 1≤(j/n)^s; for j<n, j/n≤(j/n)^s. The triangle inequality gives (5). For s=1, adding M/n leaves

    (1/n)Σ_{j≥n}(j-n)b_j,

whose modulus is at most n^(-1)Σ_{j≥n}j|b_j|=o(1/n). Finally, for 0≤r<1, 1-r^j≤min(1,j(1-r))≤j^s(1-r)^s. Hence |B(r)-L|≤M_s(1-r)^s; multiply by r and use 1-r≤(1-r)^s. □

### Proposition 3 (a genuine S example prohibiting universal o(1/n))

For 0<c≤1, define

    f_c(z)=c z/(1-z)^2+(1-c)z/(1-z).

Then f_c∈S and

    a_n=cn+(1-c),
    (1-r)^2 f_c(r)=c+(1-2c)(1-r)-(1-c)(1-r)^2.           (7)

In particular f_{1/2}(z)=((1-z)^(-2)-1)/2 satisfies the original hypothesis with λ=1/2, δ=2, but

    a_n/n-λ=1/(2n)                                      (8)

exactly. Thus no conclusion o(1/n) can hold for every f under the original assumptions, including the subcase δ=2.

**Proof of univalence.** Set w=(1-z)^(-1), which maps D bijectively onto Re w>1/2. Then

    f_c(z)=c w^2+(1-2c)w+(c-1).

If distinct w_1,w_2 in that half-plane had equal images, their sum would satisfy c(w_1+w_2)+(1-2c)=0. But its real part is strictly greater than c+1-2c=1-c≥0, a contradiction. Normalization and (7) follow by direct expansion. □

The example does not prove that O(1/n) holds in general, and it does not show that Duren's logarithmic rate is sharp. The weighted coefficient criterion is sufficient, not known here to be necessary or implied by the radial condition.

**Exact remaining gap:** establish a positive weighted absolute moment (or a comparably effective cancellation estimate) for B from the original hypotheses. The argument currently assumes the key additional regularity.

## 5. A self-contained positive-real-part representation

We use the following standard representation, recording its short proof to make the geometric arguments checkable.

### Lemma 4 (Herglotz representation)

If p is holomorphic in D, Re p>0 and p(0)=1, there is a probability measure μ on the unit circle, parameterized by -π<θ≤π, such that

    p(z)=∫ (1+e^(-iθ)z)/(1-e^(-iθ)z) dμ(θ).             (9)

**Proof.** Write u=Re p. For 0<ρ<1 the measures u(ρe^(iθ))dθ/(2π) have total mass u(0)=1 and are positive. Along a sequence ρ↑1 they have a weakly convergent subsequence on the compact circle, with probability limit μ. For fixed z∈D, the Poisson formula in the circle of radius ρ expresses u(z) as the integral of the Poisson kernel with parameter z/ρ against that measure. Uniform convergence of those kernels to the kernel with parameter z, together with weak convergence, yields

    u(z)=∫ Re((1+e^(-iθ)z)/(1-e^(-iθ)z))dμ(θ).

The integral in (9) defines a holomorphic function with this real part and value 1 at zero. Its difference from p is an imaginary constant, and that constant is zero at zero. □

## 6. Approach 4: starlike geometric rigidity

### Proposition 5

If f∈S is starlike about zero, and (1-r)^2 f(r)→λ≠0, then f=k and λ=1. Hence its coefficient remainder a_n/n-λ is identically zero.

**Proof.** For starlike f, p(z)=zf′(z)/f(z), continued at zero, has positive real part and p(0)=1. By Lemma 4 and integration from zero,

    log(f(z)/z)=-2∫ log(1-e^(-iθ)z)dμ(θ),               (10)

where the analytic logarithms vanish at zero. Put s=1-r and T=log(1/s). For r sufficiently near 1,

    -log 2 ≤ log(1/|1-e^(-iθ)r|) ≤ T.

After division by T, the integrand tends to 1 at θ=0 and to 0 elsewhere, and is uniformly bounded in absolute value. Dominated convergence and (10) imply

    lim_{r↑1} log|f(r)/r|/(2 log(1/(1-r)))=μ({0}).       (11)

The assumed nonzero quadratic radial limit makes the left side 1. Thus μ({0})=1; since μ is a probability measure, it equals the point mass at zero. Substitution in (10) gives f(z)=z/(1-z)^2. □

**Exact remaining gap:** arbitrary f∈S need not be starlike. For such f, zf′/f need not have positive real part, so the positive probability representation and its atom-rigidity argument are unavailable. Applying this rigidity beyond the starlike subclass would be unjustified.

## 7. Approach 5: a polynomial rate in a genuine nontrivial subclass

Define the explicitly restricted class

    C_0={normalized holomorphic f on D : Re((1-z)^2 f′(z))>0 on D}.

The subscript here only names this document's class; it is not an assertion about all close-to-convex functions. In particular we do not equate C_0 with the full close-to-convex class.

### Theorem 6 (restricted-class improvement)

Every f∈C_0 belongs to S. Suppose in addition

    (1-r)^2 f(r)=λ+O((1-r)^δ), λ≠0, δ>0.

Then λ is real, 0<λ≤1. Writing ε=min(δ,1),

    a_n/n-λ = O(n^(-ε))       if 0<ε<1,
              O((log n)/n)  if ε=1.                    (12)

If the representing measure of p=(1-z)^2f′ is invariant under θ↦-θ, then the stronger endpoint-inclusive bound holds:

    a_n/n-λ=O(n^(-ε)), 0<ε≤1.                           (13)

The theorem includes many functions besides k; the examples f_c from Proposition 3 lie in this class.

**Step 1: univalence.** Let w=z/(1-z), mapping D onto the convex half-plane Re w>-1/2, and set F(w)=f(w/(1+w)). Then F′(w)=p(w/(1+w)), whose real part is positive. For distinct w_1,w_2 in the half-plane,

    (F(w_2)-F(w_1))/(w_2-w_1)
      =∫_0^1 F′(w_1+t(w_2-w_1))dt

has positive real part. It is nonzero, so f is injective. The given normalization establishes f∈S.

**Step 2: identify λ as an atom.** By Lemma 4, p has a probability representation (9), and

    f(z)=∫ f_θ(z)dμ(θ),
    f_θ(z)=∫_0^z (1+e^(-iθ)t)/((1-e^(-iθ)t)(1-t)^2)dt. (14)

All integrals and power-series manipulations on compact subdisks are justified by uniform kernel bounds. On the real radius,

    |(1+e^(-iθ)t)/(1-e^(-iθ)t)|≤(1+t)/(1-t).

Consequently, with s=1-r,

    s^2 |f_θ(r)|≤s^2∫_0^r(1+t)/(1-t)^3 dt=r≤1.

When θ=0, f_0=k and s^2f_0(r)=r→1. When θ≠0, the first kernel in (14) is bounded for 0≤t≤1, so f_θ(r)=O_θ(s^(-1)) and s^2f_θ(r)→0. Dominated convergence gives λ=μ({0})=:c. The assumption λ≠0 implies c>0.

Put ν=μ-cδ_0 and f_ν=f-ck. The measure ν is positive with no atom at zero. By the radial hypothesis,

    s^2 f_ν(1-s)=cs+O(s^δ)=O(s^ε).                    (15)

**Step 3: radial growth controls mass near the atom.** For 0<s<1/4, |θ|≤s and 1-2s≤t≤1-s,

    Re((1+e^(-iθ)t)/(1-e^(-iθ)t))
      =(1-t^2)/|1-e^(-iθ)t|^2
      ≥s/(4s^2+θ^2)≥1/(5s).

Also (1-t)^(-2)≥1/(4s^2). The real part of the integrand in (14) is nonnegative everywhere on the real interval. Restricting that integral to this t-interval and these θ therefore gives

    s^2 Re f_ν(1-s)≥ν({|θ|≤s})/20.

Together with (15), this proves

    ν({|θ|≤s})≤A s^ε                                  (16)

for all sufficiently small positive s, with a constant A depending on f and the radial bound. There is no cancellation in this step because ν is positive.

**Step 4: compute the coefficient kernel.** Expanding (14) gives

    a_n/n=∫ K_n(θ)dμ(θ),
    K_n(θ)=1/n+(2/n^2)Σ_{j=1}^{n-1}(n-j)e^(-ijθ).      (17)

The direct triangle estimate gives |K_n|≤1. For q=e^(-iθ)≠1, a finite geometric-sum identity gives

    K_n(θ)=(1+q)/(n(1-q))
                 -2q(1-q^n)/(n^2(1-q)^2).             (18)

Let d=|1-q|. If nd≥1, (18) yields |K_n|≤2/(nd)+4/(n^2d^2)≤6/(nd). Since d≥2|θ|/π on [-π,π],

    |K_n(θ)|≤min(1,3π/(n|θ|)).                         (19)

At θ=0, K_n(0)=1. Thus

    a_n/n-c=∫K_n(θ)dν(θ).                              (20)

**Step 5: summation over angular scales.** The contribution of |θ|≤1/n is O(n^(-ε)) by (16). On each shell 2^j/n<|θ|≤2^(j+1)/n lying in a fixed small arc, (19) and (16) bound the absolute contribution by

    C n^(-ε) 2^(j(ε-1)).

For ε<1 these form a uniformly bounded geometric sum. For ε=1 there are O(log n) shells, each O(1/n). The complement of that fixed arc contributes O(1/n). This proves (12).

For the symmetric case the imaginary part integrates to zero. Directly from (17),

    Re K_n(θ)=|Σ_{j=0}^{n-1}e^(ijθ)|^2/n^2
       ≤min(1,4/(n^2|1-e^(iθ)|^2))
       ≤min(1,π^2/(n^2θ^2)).                           (21)

The same shell argument now has ratio 2^(ε-2), summable for every 0<ε≤1, and the complementary arc contributes O(1/n^2). This proves (13). □

**Exact remaining gap:** there is no proof here that a general normalized univalent f satisfying the radial hypothesis has Re((1-z)^2f′(z))>0, or has another positive representation yielding (16) and (20). The class restriction is substantial; replacing it by membership in S is the unresolved step.

## 8. Final mathematical assessment

The five approach families establish:

1. An exact nonunivalent analytic obstruction and the location of its critical point.
2. A power-rate implication under an additional angular remainder estimate.
3. A weighted-coefficient criterion, a two-term expansion, and an exact admissible 1/n lower obstruction at δ=2.
4. Complete rigidity for the starlike subclass.
5. A polynomial coefficient rate for C_0, with a sharper symmetric-measure endpoint.

None proves a better rate for the entire original class S or a matching logarithmic lower example in that class. The logarithmic-versus-power gap remains unresolved in this package. All novelty assertions are withheld. The control program checks finite algebraic and numerical instances only; the proofs above, not the finite checks, justify the infinite statements.
