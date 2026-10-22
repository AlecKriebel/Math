# Conditional literal noisy consistency established

Problem 30003790 / OWR-16161-003. Corrected release v2, 4 October 2026.

**Established:** fixed-dimensional expected integrated squared-error consistency,
and sample-conditional integrated-risk convergence in probability, under the
bounded-continuous regression and conditionally centered uniformly finite-variance
model stated in Section 5A. This holds for arbitrary Borel covariate designs.

**Not established:** coverage of every distribution permitted by the original,
incompletely specified model. Dimension-efficient geometric rates are a separate
unproved objective, not an extra requirement in the literal source question.

Conservative queue disposition remains **unsolved, 5/5** because full source-model
coverage has not been verified. This label does not negate the affirmative
bounded-model consistency result. No novelty claim is made.

## 1. Source scope, correction and review chronology

Klock's contribution to the 2018 Oberwolfach report, pp. 1192–1194, studies
`Y = F(X) + ε`, where `F(X) = g(t(X))` and `t(X)` is a closest-point
coordinate on an unknown smooth simple curve. Covariates may fill a tube.
The method estimates tangents from response slices and uses their scalar
projections for neighbor selection. The final paragraph asks for a modification
consistent with nonzero response noise. It does not impose an explicit
dimension-efficient rate in that question. [S1]

The original author packet treated failure to obtain dimension-efficient learning
as a reason to withhold a positive literal consistency conclusion. That framing
is superseded. Its fixed-dimensional guard theorem already gave a conditional
positive answer under additional design assumptions. A subsequent auxiliary
proof removes the lower-mass and bounded-support restrictions and has now been
accepted by a fresh independent audit. The exact accepted theorem and proof are
preserved without modification in `AUXILIARY_THEOREM.md`; its historical
not-yet-audited banner is superseded by the acceptance record described below.
Section 5A explicitly states the accepted joint-independence interpretation.

This is a curved-index problem, but the safeguard does not need to recover the
tangent field accurately. It ranks all regression covariates using both the
tangent term and a Euclidean term, with independent regression labels. Bare
consistency is distinct from useful dimension-efficient rates. Generic
nearest-neighbor regression consistency is longstanding, including Stone's
1977 results; the specific safeguarded ordering is proved here without a claim
of novelty or an assertion that every such extension follows from Stone. [S4]

Wu–Maggioni, JMLR 27(155), 1–75 (August 2026), Theorem 3 and Remark 4(iii),
pp. 17–18, retain a geometry/noise term independent of sample size.
Kereta–Klock–Naumova's inspected 2019 preprint does so in equation (23),
pp. 13–14. Neither upper bound is an impossibility theorem for other estimators;
these source comparisons do not negate the affirmative consistency theorem
below. This targeted check is not a certificate of global openness. [S2, S3]

The original freeze, both audits and all their recorded controls remain unchanged
under `../history/`. `../CHANGE_LEDGER.md` identifies the corrections and exact
stale statements superseded; `../AUTHOR_V1_TO_CORRECTED_V2.diff` records every
change to the author packet. The present corrected assembly awaits release-binding
review and has not been published.

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
each coordinate of `X`, and each entry of `XXᵀ` requires finite weighted
measures: assume `E||X||²<∞` for simultaneous identification of these moments.
Under that assumption it identifies all clean-slice unnormalized first and
second moments. Thus response noise alone does not
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

For simultaneous quantitative application to coordinates and `XXᵀ`, bounded
`X` suffices to bound all weights. Alternatively assume `E||X||⁴<∞` and
replace `M²` by `E[W²]` separately for each weight. In either case, every
weighted clean measure used must have its own `L²` density.

For any **fixed** bounded interval `I`, Cauchy–Schwarz yields
`|∫_I(v_n-ν_W)| ≤ |I|^(1/2)||v_n-ν_W||_2`. If the true clean slice mass
is positive, normalize using `max(estimated_mass,η_n)` for deterministic
`η_n>0` tending to zero. The resulting normalized moments and covariance
converge in probability; no expectation guarantee for the ratio is inferred.

For the geometric nullspace conclusion, require unique **interior** closest-point
projection, an injective link and finite conditional second moments. For almost
every clean level at which these conditional laws and hypotheses hold, first-order
optimality gives `(X-γ(t))ᵀγ'(t)=0` conditionally. The conditional support is
therefore in the affine normal hyperplane. If its covariance has rank `D-1`,
with a positive gap above the zero eigenvalue, its null line is the tangent.
Endpoint projection caps are not covered: orthogonality can fail there even
with an injective link. These facts do not complete a shrinking-slice algorithm.

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

## 5. Route 4: independently accepted general safeguard

### 5A. Accepted auxiliary theorem and implementation scope

The exact accepted theorem/proof is `AUXILIARY_THEOREM.md`, SHA256
`072aba944c908baf44bb86d6c9a3d1c87444b5f779c53a14b4a9648d9595351c`.
Its mathematical content is unchanged. The fresh independent acceptance is
`../history/auxiliary-independent-audit/AUDIT.md`, SHA256
`954dedd9ec67d2819b211aa6cbb6f33cd578977175fb1478ede820aa3f4aab6f`.
This corrected release incorporates that accepted object with the following
complete model and interpretation; it does not attribute the auxiliary proof
to the original five-route author freeze.

Fix a finite dimension `D≥1` and an arbitrary Borel probability law `P` on
`R^D`, with support `K`. The regression pairs `(X_i,Y_i)` are iid,
`X_i~P`, and `Y_i=F(X_i)+ε_i`. Assume `F` is bounded and continuous on
`K` in its relative topology, and

`E[ε_i|X_i]=0`, `E[ε_i²|X_i]≤σ²<∞` almost surely,

with one common finite bound. For each `n`, the auxiliary training object
`T_n` is independent of the regression data. The field `a_n(T_n,z)` is
jointly measurable in training data and covariate, with norm at most one.
The test point `X~P` is independent of the **joint** observed-data sigma-field
`S_n=σ(T_n,(X_1,Y_1),…,(X_n,Y_n))`. Pairwise independence is not substituted
for this joint independence.

Choose deterministic integers `1≤k_n≤n` with `k_n→∞` and `k_n/n→0`.
Let `R_n(x)` be the kth Euclidean-neighbor distance among **all n** regression
covariates. Rank all n candidates lexicographically by `(d_n(x,X_i),i)`, where

`d_n(x,X_i)=|a_n(T_n,X_i)ᵀ(x-X_i)|+λ_n(x)||x-X_i||`.

Select exactly `k_n` distinct indices and average their responses. The accepted
choices are (A) fixed `λ_n(x)=λ` with `0<λ≤1`, or (B)
`λ_n(x)=min(1,sqrt(R_n(x)+1/n))`. Then

`E[(F̂_n(X)-F(X))²]→0`, `E[R(S_n)]→0`, and `R(S_n)→0` in probability,

where `R(S_n)=∫_K(F̂_n(x)-F(x))²dP(x)`. In case B, `λ_n(X)→0` in
probability. No design density, lower-mass condition, compact support or
covariate moments are required. Bounded continuity of `F` and the uniform
conditional noise bound are retained. No rate, almost-sure or uniform
consistency, tangent recovery, or growing-dimension conclusion is asserted.

The field assignment on the regression sample uses `T_n` and `X_i` only,
never `Y_i`; merely holding out the labels and then using them to assign
response slices would not suffice. Deterministic sample-index ties use no
responses. No unverified coarse-segment filter is retained before the all-n
ranking. These are part of the accepted construction, not optional cautions.

This gives an affirmative answer to literal noisy consistency under the stated
bounded-continuous, conditionally centered uniformly finite-variance model.
A compact tubular support on which `F=g∘t` is continuous, with independent
centered finite-variance noise, is a covered special case. The short report
does not fully specify boundedness/integrability or noise identification;
coverage of every interpretation of its model is therefore not established.
Dimension-efficient geometry learning remains a distinct unproved question.

### 5B. Original quantitative theorem, with formal clarifications

The earlier quantitative theorem remains valid under its stronger design
assumptions and provides an explicit dimension-dependent bound. It does not
require the estimated tangent field itself to converge. Section 5A is broader
for consistency and is the current principal finding.

**Theorem (vanishing Euclidean guard).** Let `D≥1` be fixed. Assume:

1. The support `K⊂R^D` has finite diameter `B`.
2. For constants `c,r_0>0`, `P_X(B(x,r))≥c r^D` for all `x∈K` and
   `0<r≤r_0`.
3. `|F(x)-F(z)|≤H||x-z||^s` on `K`, with `0<s≤1`.
4. Observations are iid, `E[ε|X]=0`, and `E[ε²|X]≤σ²<∞`.

Use an independent training part `T_n` to build a field `a_n(T_n,z)` jointly
measurable in training data and covariate, with `||a_n(T_n,z)||≤1`. For
brevity write this as `a_n(z)` below. The test point is independent of the
joint training/regression data. This may be produced by the source's
level-set/tangent algorithm, with a fixed convention for empty or singular
cells. On a separate regression sample of size `n`, use only its covariates
to order neighbors of `x` by

`d_n(x,z)=|a_n(z)ᵀ(x-z)|+λ_n||x-z||`, `0<λ_n≤1`.                    (7)

Rank all n regression covariates by `(d_n(x,X_i),i)`, breaking ties by
deterministic sample index. Field assignment and neighbor selection use no
regression responses. Average the `k_n` responses selected by (7). Write this estimate as `F̂_n(x)`. If `k_n→∞`,
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

## 7. Current findings and conservative disposition

Five author mechanisms were examined. The original freeze and the original
five-turn ledger remain unchanged in history. This release applies the first
audit's scoped corrections and incorporates the separately developed auxiliary
proof only after its fresh independent acceptance.

The strongest positive finding is Section 5A: an explicit fixed-dimensional
safeguard gives expected integrated squared-error consistency and sample-conditional
integrated-risk convergence in probability for arbitrary Borel designs under
bounded continuity and conditionally centered uniformly finite-variance noise.
It is a genuine modification retaining the tangent term if desired. This is an
affirmative literal bounded-model result, not merely an unproved proposal.

The strongest restricted negative result remains the nonzero per-slice tangent
projector loss for an explicit curved tube. It is not an impossibility theorem
for arbitrary covariate-refined estimators. Known-noise deconvolution and pilot
localization are useful conditional lemmas with the stated moment, interior
projection and statistical gaps.

Queue status is conservatively `unsolved`, 5/5 author turns, solely because
coverage of the underspecified original model has not been established. There
is no added dimension-efficiency condition on the literal source question.
Dimension-efficient geometric rates remain separately unproved. Neither
mathematical novelty nor complete current-literature coverage is asserted.
Generic regression consistency should be credited to its established literature,
including Stone (1977), rather than presented as a new discovery. [S4]

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

[S4] Charles J. Stone, “Consistent Nonparametric Regression,” *Annals of
Statistics* 5(4), 595–620 (1977), especially Section 3, Theorem 2 and
Corollary 3. https://doi.org/10.1214/aos/1176343886
The auxiliary audit checked the primary scan. Stone's general nearest-neighbor
consistency results supply historical context, not an automatic proof for the
specific data-dependent guard and deterministic tie convention used here.
