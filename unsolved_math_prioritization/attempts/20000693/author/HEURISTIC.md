# Product-moment heuristic with primitive multiplicities and local deletions

## 1. Scope and status

Fix finitely many Dirichlet characters `chi_i` modulo positive integers `q_i`, with arbitrary overlaps and repetitions, and fixed real weights `a_i >= 0`. All moduli and weights are independent of `T`. Define

\[
 I_{\mathbf a}(T)=\int_T^{2T}\prod_i
 |L(1/2+it,\chi_i)|^{2a_i}\,dt.
\]

Zero weights mean that the associated factor is omitted, including at zeros. The all-zero case is exactly `I(T)=T` and is treated separately. Let `psi_i` be the unique primitive character inducing `chi_i`, of conductor `f_i`. The conductor-one primitive character denotes zeta. Group by **equality of primitive characters**, not equality of modulus labels and not conjugacy:

\[
 M_\psi=\sum_{i:\psi_i=\psi}a_i,
 \qquad E=\sum_\psi M_\psi^2.
\]

The characters `psi` in all following products are the distinct classes with positive total weight. Our prediction is a leading asymptotic only. It is a conjecture, obtained from the standard hybrid/random-matrix assumptions. No critical-line high-moment asymptotic is proved here.

## 2. Explicit arithmetic and matrix constants

For each prime `p`, define the analytic power series on `|z|<1`

\[
 B_p(z)=\prod_i(1-\chi_i(p)z)^{-a_i}
       =\sum_{r\ge0}b_p(r)z^r.
\]

Each power is the branch analytic at zero with value 1. There is no branch choice for the original absolute-value moment. The local arithmetic factor is

\[
 J_p=\sum_{r\ge0}\frac{|b_p(r)|^2}{p^r}
 =\frac1{2\pi}\int_0^{2\pi}
       \prod_i|1-\chi_i(p)e^{i\theta}/\sqrt p|^{-2a_i}\,d\theta.
 \tag{1}
\]

Set

\[
 \mathcal A=\lim_{y\to\infty}\prod_{p\le y}(1-p^{-1})^E J_p,
 \qquad
 \mathcal G=\prod_\psi\frac{G(1+M_\psi)^2}{G(1+2M_\psi)},
 \tag{2}
\]

where `G` is the Barnes G-function, normalized by `G(1)=1` and `G(z+1)=Gamma(z)G(z)`. The prime limit is in increasing prime order. In general it is **conditionally**, not absolutely, convergent. Section 4 gives an absolutely convergent regularization and proves that it is a positive finite number.

The requested heuristic is

\[
 \boxed{I_{\mathbf a}(T)\ \sim\
 T\mathcal A\mathcal G(\log T)^E.}
 \tag{H}
\]

Equivalently, at leading order one may replace `(log T)^E` by

\[
 \prod_\psi(\log(f_\psi T))^{M_\psi^2}.
\]

This equivalence uses fixed conductors only. Constants such as `2 pi` inside those logarithms cannot be interpreted as a prediction of lower-order terms. For a fixed nonnegative smooth compactly supported weight `W` inside `(0,infinity)` with positive integral, the analogous prediction replaces `T` by `T integral W`; this too is heuristic.

The literal source integrand has every `a_i=1`. Distinct primitive factors give `E=k`; `k` identical primitive factors give `E=k^2`; multiplicities `(2,1)` give `E=5`. For an outer moment parameter `kappa >= 0` applied to a product with integer multiplicities `e_i`, take `a_i=kappa e_i`; then `E=kappa^2 sum_psi (sum_{i:psi_i=psi}e_i)^2`. The integer multiplicities and outer real parameter have separate roles. Formula (H) also allows independently chosen nonnegative real `a_i`, as a model extrapolation described in Section 6.

## 3. Differing moduli: retain every local factor

The exact elementary identity

\[
 L(s,\chi_i)=L(s,\psi_i)\prod_{p\mid q_i}
                       (1-\psi_i(p)p^{-s})
 \tag{3}
\]

includes a harmless factor 1 at primes dividing `f_i`. Thus all functions with the same primitive inducer share the same primitive-zero factor. Their exponents add to `M_psi`. Their deleted prime factors need not agree and must still be retained separately.

For an explicit common-modulus translation, put `Q=lcm_i q_i` and let `tilde chi_i` be the character modulo `Q` induced by `psi_i`. Then

\[
 L(s,\chi_i)=L(s,\widetilde\chi_i)
 \prod_{\substack{p\mid Q\\p\nmid q_i}}
                  (1-\psi_i(p)p^{-s})^{-1}.
 \tag{4}
\]

These additional factors are **inverse Euler factors**. They must not be called a finite Dirichlet polynomial. On the critical line each denominator is nonzero since `|psi_i(p)p^{-s}|<1`. Multiplying the common-modulus model by their absolute values to powers `2a_i` restores the original moment. Equivalently, (1) uses the actual values `chi_i(p)`, including zero, from the start.

At primes `p|Q`, the common-modulus coefficients have local factor 1. Formula (4) restores precisely the factors for those `i` with `p` not dividing `q_i`, and their common phase must be integrated together in (1). Multiplying separate local expectations would generally be wrong.

Relative to the primitive-core heuristic, let `J_p^*` be (1) with each `chi_i(p)` replaced by `psi_i(p)`. The exact local modification of the proposed leading constant is

\[
 \frac{\mathcal A}{\mathcal A^*}
    =\prod_{p\mid Q}\frac{J_p}{J_p^*}.
 \tag{5}
\]

This is a finite positive factor and does not change `E` or `mathcal G`. Equation (5) is an identity between the defined arithmetic constants; transporting the corresponding moment asymptotic is part of the heuristic, not a theorem.

## 4. Rigorous convergence and positivity of the proposed constant

This section concerns the defined Euler constant, not the moment asymptotic.

Let `A=sum_i a_i>0`. Coefficientwise absolute values in `B_p` are bounded by those of `(1-z)^(-A)`, namely `(A)_r/r!`, which grows polynomially in `r`. Consequently (1) converges for each prime and is strictly positive. Parseval on the circle of radius `p^(-1/2)` proves the equality in (1). Uniformly as `p` tends to infinity,

\[
 J_p=1+p^{-1}|\sum_i a_i\chi_i(p)|^2+O_{\mathbf a}(p^{-2}).
 \tag{6}
\]

Let `S={p:p|Q}`. For `p` outside `S`, set `rho_{psi,phi}=psi overline(phi)` (viewed as a character of a common multiple of the conductors) and define

\[
 H_p=J_p(1-p^{-1})^E
       \prod_{\psi<\phi}|1-\rho_{\psi,\phi}(p)/p|
                          ^{2M_\psi M_\phi}.
 \tag{7}
\]

Here `<` is any fixed ordering of the distinct primitive classes; it has no mathematical effect. Pairing conjugates makes all powers positive real powers and avoids a complex-logarithm ambiguity. At good primes,

\[
 |\sum_\psi M_\psi\psi(p)|^2
 =E+2\sum_{\psi<\phi}M_\psi M_\phi\Re\rho_{\psi,\phi}(p).
\]

The linear terms in (7) therefore cancel and `H_p=1+O_a(p^(-2))`. Thus the product of `H_p` over good primes converges absolutely to a positive number. For distinct primitive `psi,phi`, their product character `rho` is nonprincipal, and its (partial) Dirichlet L-value at 1 is nonzero. Define

\[
 L^S(1,\rho)=\lim_{y\to\infty}
       \prod_{\substack{p\le y\\p\notin S}}(1-\rho(p)/p)^{-1}.
\]

Standard convergence of the nonprincipal Dirichlet Euler product at 1 (e.g. by the prime number theorem in fixed arithmetic progressions) supplies this ordered limit. Then (2) equals the unambiguous positive expression

\[
 \boxed{\mathcal A=
  \prod_{p\in S}(1-p^{-1})^EJ_p\,
  \prod_{p\notin S}H_p\,
  \prod_{\psi<\phi}|L^S(1,\psi\overline\phi)|^{2M_\psi M_\phi}.}
 \tag{8}
\]

All possible conditional convergence is isolated in finitely many standard nonprincipal L-values. A nonreal character and its conjugate are two distinct constituents unless they actually coincide; their cross L-value is nonprincipal. No claim that the unregularized product in (2) converges absolutely is made.

## 5. Heuristic derivation and precisely unproved steps

Use the primitive hybrid Euler--Hadamard decomposition of Heap and Sahay, retaining the elementary deletions (3). For a slowly growing cutoff `X`, the prime component has local phase mean (1). Mertens' theorem and (2) indicate its mean size

\[
 \mathcal A(e^\gamma\log X)^E.
 \tag{9}
\]

For fixed finitely many primes, their phases along `t` are equidistributed jointly, so the finite-prime averaging identity is exact in the long-time limit. Replacing the full growing-cutoff mean by (9) at the same time as `T` grows is part of the hybrid moment model here. We do not infer it by unjustified interchange of limits.

There is one primitive-zero model for each distinct `psi`, with total exponent `M_psi`. Treat distinct primitive-zero models as independent, and use the usual unitary characteristic-polynomial moment. For real `m>=0`, the known random-matrix identity is

\[
 \mathbb E_{U(N)}|\det(I-U)|^{2m}
 =\prod_{j=1}^N\frac{\Gamma(j)\Gamma(j+2m)}{\Gamma(j+m)^2}
 \sim\frac{G(1+m)^2}{G(1+2m)}N^{m^2}.
 \tag{10}
\]

The hybrid normalization therefore predicts for the zero component

\[
 \mathcal G\prod_\psi
 \left(\frac{\log(f_\psi T)}{e^\gamma\log X}\right)^{M_\psi^2}.
 \tag{11}
\]

The essential conjectural inputs are the replacement of primitive zeros by these random matrices, independence **between distinct primitive constituents**, and splitting of prime and zero components at the level of this weighted mean. Combine (9) and (11); the factors `(e^gamma log X)^E` cancel exactly. This yields (H).

Sahay's Conjectures 1.4/1.6 and conditional Theorem 1.7 perform precisely this procedure for nonnegative integer weights at common modulus. Heap supplies the underlying factorwise recipe and multiplicity principle. Our extension of the model to independent nonnegative real weights uses (10); it is a heuristic continuation, not a theorem obtained by analytic continuation from integer moments. The differing-modulus adjustment follows (3)--(5), with its arithmetic constant fixed by (1).

Finite deletions can change the leading constant, so bounding them above and below would establish only a matching order if the primitive-core order were known. Such bounds cannot justify (5) as a theorem about actual moments. Nor does the rigorous convergence of (8) prove the statistical independence assumptions. These distinctions are essential.

## 6. Exact normalizations and adversarial checks

1. **One character, weight 1.** `E=1`, `mathcal G=1`. At `p` not dividing `q`, `J_p=(1-p^(-1))^(-1)`; at `p|q`, `J_p=1`. Hence `mathcal A=phi(q)/q`. The leading term agrees with the standard mean square.
2. **One character, weight 2.** Good-prime `J_p=(1+p^(-1))/(1-p^(-1))^3`, so
   `mathcal A=zeta(2)^(-1) product_{p|q}(1-p^(-1))^3/(1+p^(-1))` and `mathcal G=1/12`. Thus the leading coefficient is `(2 pi^2)^(-1)` times that finite product, as in the fourth moment.
3. **Two distinct primitive characters, each weight 1.** `E=2`; the cross arithmetic factor involves `|L^S(1,psi overline(phi))|^2`. This is consistent with the established two-factor formula; it is not a proof for more factors.
4. **Nonreal character and its conjugate.** `E=2`, not 4. With a primitive quartic character modulo 5, the cross pair character is its nonprincipal square.
5. **Same primitive inducer, different moduli.** The sum of weights is squared. For `zeta(s)L(s,chi_0 mod 2)=zeta(s)^2(1-2^(-s))`, `E=4` and the sole changed local ratio is `(1-1/2)^2/(1+1/2)=1/6`. The predicted leading coefficient is `1/(12 pi^2)`. Using two independent matrices would wrongly produce exponent 2; ignoring the deleted Euler factor would miss the factor 1/6.
6. **Zero weights/all-zero input.** Omitting zero weights commutes with all definitions. For all weights zero, both constants are 1 and (H) becomes the identity `I(T)=T`.
7. **Fractional nonnegative weights.** The local series and phase integral remain well-defined, (6)--(8) hold, and (10) is valid. The critical-line extrapolation still rests on the same statistical hypotheses. Tests below check these local facts and matrix normalizations, not the conjecture for L-functions.

## 7. What is and is not delivered

Delivered: an explicit leading-term heuristic for the source's displayed product and independent fixed nonnegative real powers, for arbitrary fixed Dirichlet moduli, including repeats, principal characters, nonreal characters, and all deleted Euler factors. It has a positive finite arithmetic constant, the correct known normalizations, and transparent conjectural assumptions.

Not delivered: a proof of the asymptotic, a full lower-order moment polynomial, uniformity in growing moduli/degree/weights, shifted or unbalanced complex moments, or negative powers. Negative powers can have nonintegrable singularities at zeros; Heap's printed outer range `k>-1/2` must not be blindly transferred to repeated constituents, whose effective weight is `e_j k`. No negative range is asserted here.

Priority: the model and its principal formula are prior mathematics of Keating--Snaith, Heap and Sahay. The present differing-modulus/real-weight spelling-out and local checks are credited synthesis with no claim of novel mathematical discovery. The source requested a heuristic; a separately posed high-moment theorem remains open in general.
