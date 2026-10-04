# Noisy nonlinear single-index regression: scoped consistency and the remaining gap

Problem 30003790 / OWR-16161-003. Author investigation, 4 October 2026.
Disposition: **unsolved** for the efficient geometric objective described below.
No claim of mathematical novelty is made for the elementary lemmas in this note.

## 1. Exact source and the scope issue

Klock's contribution to the 2018 Oberwolfach report, pp. 1192–1194, studies
`Y = F(X) + ε`, where `F(X) = g(t(X))` and `t(X)` is the closest-point
coordinate on an unknown smooth simple curve. The covariate distribution can
fill a tube around the curve. The proposal learns tangents from response slices
and uses their scalar projections to select neighbors. Its last paragraph asks
for a modification consistent under nonzero response noise. [S1]

This is a curved-index problem. Consistency of an ordinary linear single-index
estimator does not settle it. We distinguish two success criteria:

* **Literal fixed-dimensional consistency:** risk tends to zero, allowing a
  dimension-dependent statistical rate and extra regularity assumptions.
* **Source-motivated efficient geometric consistency:** eliminate the fixed-noise
  error while preserving useful high-dimensional sample guarantees, rather than
  simply recovering ambient-dimensional nonparametric regression.

Section 5 proves a positive result for the first criterion under explicitly
listed assumptions. It is a genuine tangent-neighbor modification, but its
sample guarantee is cursed by dimension. The short OWR question does not state
an explicit formal rate requirement; therefore calling the *literal* question
unconditionally unsolved would be too strong. Conversely, promoting Section 5
as a resolution of the high-dimensional research problem would hide its central
limitation. We retain `unsolved` rather than silently choose the easier scope.

The latest directly relevant primary result located is Wu–Maggioni, JMLR
27(155), 1–75 (August 2026). Theorem 3 has a decaying one-dimensional estimation
term plus a geometry/noise term independent of sample size. Remark 4(iii),
p. 18, explicitly leaves removal of the latter to further geometric work. The
2019 arXiv version of Kereta–Klock–Naumova also retains a curvature/noise term
in equation (23), pp. 13–14. These are upper bounds, not information-theoretic
lower bounds for all estimators. Neither inspected theorem closes the strong
criterion. This limited literature check is not a certificate of global openness.
[S2, S3]

## 2. Route 1: exact response-slice nonlocality and tangent loss

Let `0 < b < L < π/4`, `0 < r < 1`, and let independent variables satisfy
`T ~ Unif[-L,L]`, `R ~ Unif[-r,r]`, and `ε ~ Unif[-b,b]`. Put

`γ(t) = (cos t, sin t)`, `X = (1+R)γ(T)`, `F(X)=T`, and `Y=T+ε`.

This is a smooth, arclength-parametrized curved-index model with a genuine
two-dimensional tubular distribution. Since `1+R>0`, the unique closest point
of `X` on this arc is `γ(T)`. The response noise is centered and independent.

Condition on `A_h = {|Y| ≤ h/2}`, where `b+h/2 < L`. In coordinates `(Y,ε)`,
the joint density before conditioning is constant on the rectangle
`[-h/2,h/2] × [-b,b]`: the constraint `T=Y-ε ∈ [-L,L]` is automatic.
Consequently, conditioned on `A_h`, `Y` and `ε` are independent uniforms on
those intervals. Therefore

`support(T | A_h) = [-b-h/2, b+h/2]`,

`Var(T | A_h) = b²/3 + h²/12`.                                      (1)

The latent length tends to `2b`, not zero. This is a population fact, so merely
increasing the number of observations in the same narrow response interval
cannot repair it.

There is also an exact geometric limitation on representing one slice by a
single tangent. Write `a(T)=γ'(T)=(-sin T, cos T)` and
`sinc(u)=sin(u)/u`, with `sinc(0)=1`. Independence gives

`E[exp(iqT) | A_h] = sinc(qb) sinc(qh/2)`.

For a single unit vector `v`, expansion of the square gives

`inf_v E[||v-a(T)||² | A_h] = 2[1-sinc(b)sinc(h/2)]`.                 (2)

To remove any eigenvector-sign ambiguity, let `P_v=vvᵀ`. The largest eigenvalue
of `E[a(T)a(T)ᵀ | A_h]` equals
`[1+sinc(2b)sinc(h)]/2`; the product is positive under our angle restriction.
Hence

`inf_v E[||P_v-a(T)a(T)ᵀ||_F² | A_h] = 1-sinc(2b)sinc(h)`.           (3)

The limiting lower bounds in (2) and (3) are strictly positive. They apply to
one vector per response slice, including a vector learned from an independent
training sample. They do **not** apply to an estimator allowed to use each
point's own `X` to refine the tangent. Nor do they directly lower-bound
regression prediction risk. The example refutes only the proposed mechanism
that arbitrarily narrow raw response bins must have vanishing tangent error.

## 3. Route 2: deconvolution identifies clean conditional moments

Let `Z=F(X)` and assume, for this route only, that `ε` is independent of `X`
and its law is **known**. For a bounded scalar weight `W=W(X)`, define finite
signed measures

`ν_W(B)=E[W 1{Z∈B}]`, `λ_W(B)=E[W 1{Y∈B}]`.

The convolution identity `λ_W=ν_W * P_ε` follows by conditioning on `X`.
Using the convention `ν̂(u)=∫exp(iuz)dν(z)`, it becomes

`λ̂_W(u)=ν̂_W(u) φ_ε(u)`.                                           (4)

If `φ_ε` is nowhere zero, (4) identifies `ν_W`. Applying this to `W=1`,
each coordinate of `X`, and each entry of `XXᵀ`, identifies all clean-slice
unnormalized first and second moments. Thus response noise alone does not
create a population impossibility for recovering those moments.

Here is a quantitative elementary statistical version. Suppose
`ε ~ N(0,σ²)`, `σ>0` known, `|W|≤M`, and `ν_W` has an `L²(R)` density.
For independent data define

`L_n(u)=n⁻¹ Σ W_i exp(iuY_i)`,

`v_n(z)=(2π)⁻¹ ∫_{-U_n}^{U_n} exp(-iuz) L_n(u) exp(σ²u²/2) du`.

Pointwise complex variance is bounded by `M²/n`. Plancherel and Tonelli imply

`E||v_n-ν_W||²_2 ≤ M² U_n exp(σ²U_n²)/(πn)`
`                   + (2π)⁻¹ ∫_{|u|>U_n}|ν̂_W(u)|²du`.              (5)

With `U_n = sqrt(log n/(2σ²))`, both terms vanish. In (5), `ν_W` on the
left denotes its density. The bandlimited stochastic error and the omitted
Fourier tail have disjoint frequency support, so no extra factor of two is
needed. A signed estimate is allowed; positivity is not required for this
`L²` convergence assertion.

For any **fixed** bounded interval `I`, Cauchy–Schwarz yields
`|∫_I(v_n-ν_W)| ≤ |I|^(1/2)||v_n-ν_W||_2`. Normalizing by an estimated
positive slice mass then consistently estimates its covariance. At a clean
level `Z=z`, all points lie in the affine normal hyperplane to the curve,
provided the link is injective. If that conditional covariance has a unique
zero eigenvalue and a positive gap, its null line is the tangent. These facts
explain a possible mechanism, but they do not complete a shrinking-slice
algorithm.

**Exact gap:** the source does not supply a known Gaussian noise law. We have
not established uniform shrinking-window moment control, denominator bounds,
stable tangent-field reconstruction and out-of-sample assignment at useful
dimension-independent rates under the source's general noise assumptions.
An arbitrary estimate of the unknown noise characteristic function cannot
simply be divided into (4) without controlling its errors and small values.
This route is conditional partial progress, not a complete candidate.

## 4. Route 3: pilot denoising gives an exact localization lemma

Suppose `F(x)=g(t(x))`, where the monotone link satisfies
`|g(t)-g(u)| ≥ m|t-u|` with `m>0`. Let an independent pilot `p_n` satisfy
`sup_x |p_n(x)-F(x)| ≤ δ_n` on the support. Partition the **pilot predictions**
into intervals of width `h_n`. If `x,x'` fall in the same pilot interval,

`m|t(x)-t(x')| ≤ |F(x)-F(x')| ≤ h_n+2δ_n`.                           (6)

Thus every such slice has latent diameter at most `(h_n+2δ_n)/m`. This
bound is deterministic on the pilot event and valid even at bin boundaries.
If `h_n,δ_n→0`, the geometric width obstruction disappears.

Equation (6) does not prove that the whole estimator is consistent: spectral
gaps, enough samples in each useful cell, geometry estimation and test-point
assignment remain. More importantly, a uniformly consistent pilot already
solves a substantial part of the regression problem. An ambient-dimensional
pilot is available under stronger standard design/smoothness assumptions but
reintroduces the curse of dimensionality. Cross-fitting removes response reuse;
it does not produce a pilot accuracy theorem. No dimension-efficient pilot
with the required guarantee has been supplied here.

## 5. Route 4: a fully proved fixed-dimensional consistency safeguard

The following theorem supplies an honest weaker positive answer. It deliberately
does not require the estimated tangent field itself to converge.

**Theorem (vanishing Euclidean guard).** Let `D≥1` be fixed. Assume:

1. The support `K⊂R^D` has finite diameter `B`.
2. For constants `c,r_0>0`, `P_X(B(x,r))≥c r^D` for all `x∈K` and
   `0<r≤r_0`.
3. `|F(x)-F(z)|≤H||x-z||^s` on `K`, with `0<s≤1`.
4. Observations are iid, `E[ε|X]=0`, and `E[ε²|X]≤σ²<∞`.

Use an independent training part to build any measurable vector field
`a_n:K→R^D` with `||a_n(z)||≤1`. This may be produced by the source's
level-set/tangent algorithm, with a fixed convention for empty or singular
cells. On a separate regression sample of size `n`, use only its covariates
to order neighbors of `x` by

`d_n(x,z)=|a_n(z)ᵀ(x-z)|+λ_n||x-z||`, `0<λ_n≤1`.                    (7)

Break ties independently of the regression responses. Average the `k_n`
responses selected by (7). Write this estimate as `F̂_n(x)`. If `k_n→∞`,
`k_n/n→0`, and `(k_n/n)^(1/D)/λ_n→0`, then

`E[(F̂_n(X)-F(X))²] → 0`.

Consequently its sample-conditional integrated risk converges to zero in
probability. This holds for arbitrary fixed nonzero response-noise variance.

**Proof.** Let `R_k^E(x)` be the Euclidean distance to the `k`th nearest
regression covariate. Cauchy–Schwarz gives the deterministic sandwich

`λ||x-z|| ≤ d_n(x,z) ≤ (1+λ)||x-z||`.                               (8)

At least `k` covariates have `d_n` distance at most `(1+λ)R_k^E`.
Every selected covariate therefore has Euclidean distance at most

`R_k^G(x) ≤ (1+λ) R_k^E(x)/λ`.                                      (9)

This argument uses only order statistics; symmetry and a triangle inequality
for `d_n` are unnecessary.

Set `r_n=(2k/(cn))^(1/D)` and take `n` large enough that `r_n≤r_0`.
The number `N_r` of covariates in `B(x,r_n)` is binomial with mean
`μ≥2k`. The multiplicative Chernoff inequality gives

`P(R_k^E(x)>r_n) ≤ P(N_r<k) ≤ exp(-μ/8) ≤ exp(-k/4)`.               (10)

Conditional on the training part and all regression covariates, the selection
depends on no regression noise. Its averaged noise has mean zero and variance
at most `σ²/k`. On the good event in (10), Hölder continuity and (9) bound the
absolute conditional bias by `H(2r_n/λ)^s`; on the bad event it is at most
`HB^s`. The cross term with noise has zero conditional expectation. Uniformly
for `x∈K`,

`E[(F̂_n(x)-F(x))²] ≤ σ²/k`
`  + H²[(2r_n/λ)^(2s)+B^(2s)exp(-k/4)]`.                            (11)

The right-hand side tends to zero under the stated conditions. Integrate over
an independent test `X`. If `R(S)` denotes conditional integrated risk, then
`E R(S)→0`, so Markov's inequality gives `R(S)→0` in probability. ∎

For example, `k_n=floor(n^(1/2))` and `λ_n=n^(-1/(4D))` give

`E[(F̂_n(X)-F(X))²] = O(n^(-1/2)+n^(-s/(2D)))`.                     (12)

Constants depend on the displayed design and smoothness parameters. The
preprocessing and a brute-force neighbor search are finite polynomial-time
operations if the tangent estimator is. However, (12) deteriorates with `D`;
to reach a given small error, its sample bound can be exponential in `D`.
Computational polynomiality in `(n,D)` must not be confused with a
dimension-efficient sample bound. We have proved neither optimality nor novelty
of this safeguard. The lower-mass and Hölder assumptions are explicit additions,
not assertions about every distribution allowed by the short source report.

Using the second sample's responses to choose its neighbors would invalidate
the variance step. Likewise, setting `λ_n=0` removes (9); adding an arbitrarily
tiny guard without the displayed rate condition is insufficient for this proof.

## 6. Route 5: higher-order jets and a fixed-width obstruction

A higher-order geometric fit can reduce approximation error, but a fixed
polynomial order on a slice of nonvanishing latent width does not automatically
remove bias. For an elementary exact obstruction, put

`ψ(t)=0` for `t≤0`, and `ψ(t)=exp(-1/t²)` for `t>0`.

The graphs `η_0(t)=(t,0)` and `η_1(t)=(t,ψ(t))` are smooth regular curves
and have identical derivatives of every finite order at `t=0`. Repeated
differentiation expresses `ψ^(j)(t)` as a polynomial in `1/t` times
`exp(-1/t²)`, whose limit is zero at the origin. Nevertheless
`||η_1(b)-η_0(b)||=exp(-1/b²)>0` for every fixed `b>0`.

Their arclength reparametrizations also agree to every order at zero: the
arclength correction is flat, as follows from
`sqrt(1+ψ'(t)²)-1`, and inversion preserves this flat correction locally.
Thus even unlimited knowledge of a single Taylor jet need not determine a
smooth curved segment of fixed width. This only blocks arguments that rely
on a local jet without spatial information. It does not rule out polynomial
fits using observations throughout the interval, increasing-degree approximation,
splines, or extra analyticity assumptions.

To complete a higher-order route one must prove that the noise-blurred data
identify and stably estimate the extra geometry, with an approximation error
that actually vanishes and statistical/computational constants that remain
acceptable. Neither a fixed-order Taylor bound nor the smallness of curvature
alone supplies that missing theorem.

## 7. Verified conclusions and stopping point

Five distinct mechanisms were examined: raw slicing, Fourier deconvolution,
pilot-denoised slicing, guarded neighbor selection, and higher-order geometry.
Equations (1)–(6) and Theorem (7)–(12) are scoped mathematical results with
proofs above. The attached checks test formulas and finite controls, not the
unproved high-dimensional conclusion.

The strongest positive result is the guarded estimator's fixed-dimensional
consistency. The strongest negative result is a strictly positive per-slice
tangent-projector loss in an explicit curved tube model. Neither establishes
an impossibility for general estimators. The remaining substantive research gap
is a noise-robust way to learn the nonlinear coordinate/tangent geometry and
predict consistently at useful dimension-efficient sample cost under clearly
specified model assumptions. No complete candidate meeting that criterion was
obtained in this five-route investigation.

## References

[S1] T. Klock, with Ž. Kereta, M. Maggioni and V. Naumova, “Estimation of
Nonlinear Single Index Models,” in *Nonlinear Data: Theory and Algorithms*,
Oberwolfach Report 20/2018, pp. 1192–1194.
https://doi.org/10.4171/OWR/2018/20

[S2] Ž. Kereta, T. Klock and V. Naumova, “Nonlinear generalization of the
monotone single index model,” *Information and Inference* 10(3), 987–1029
(2021), https://doi.org/10.1093/imaiai/iaaa013. The inspected accessible text
was arXiv:1902.09024v2 (5 September 2019), especially §4.1, equation (23).
https://arxiv.org/abs/1902.09024v2

[S3] Y. Wu and M. Maggioni, “Conditional Regression for the Nonlinear
Single-Variable Model,” *Journal of Machine Learning Research* 27(155),
1–75 (2026), Theorem 3 and Remark 4(iii), pp. 17–18.
https://www.jmlr.org/papers/v27/24-2004.html
Matching current preprint metadata: https://arxiv.org/abs/2411.09686v4
