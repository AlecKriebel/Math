# Independent stochastic-construction and truncation adversary report

**Disposition: PASS in the assigned mathematical scope. No blocking mathematical gap found.**

Reviewer: `stochastic_truncation_adversary_01`  
Review performed: 2026-10-15 UTC  
Candidate: frozen `submitted/unsolved_math_prioritization/attempts/30002291/PROOF.md`  
SHA-256: `508f71b81ee669d4934ef1cc9e061c129e47d36359896ad7b3e20574dbfbc539`

This review independently reconstructed Sections 2, 4, and 6 and tested their use in the stated finite-dimensional stable limit. The deterministic impulse/energy assertions in Section 3 and the phase assertion in Section 5 were allowed as explicit dependencies; I checked their needed conditions and the dependence/stability interfaces, including the density mechanism in Section 5. This is not a novelty, source-priority, or source-scope audit. I did not read the submitted inherited independent reviews, any parent reconstruction, or sibling verdicts before or during the derivation. No candidate or parent files were edited; no Git, index, ref, or provider mutation was performed, and no external contact or network lookup was made.

## Exact claim and success criteria

The claim reviewed is (2.4), for deterministic meshes tending to zero and every deterministic finite list of positive observation times. The driver has a simple integer-valued jump measure, predictable compensator `nu_s(dz) ds`, no continuous martingale component, and an all-compensated representation with deterministic global bounds `|b_s| <= B` and `int z^2 nu_s(dz) <= K`. The convolution kernel is the deterministic real kernel `g(x)=1_(x>0) x^alpha f(x)`, with `0<alpha<1/2`, `f` of class C1, nonzero `f(0)`, and the stated exponential bound on both `f` and `f'`.

The success criteria were: a legal infinite-past convolution; a valid square-integrable derivative for the prehistory; a valid drift decomposition after a fixed jump cutoff; an error estimate uniform over the mesh for the omitted small jumps; correct coupling and order of limits for stable convergence relative to the entire original sigma field; and no hidden assumption of independence, stationarity, symmetry, or deterministic compensator. All these criteria are met under the written assumptions.

The hypotheses are substantive. The argument does not cover a random anticipative smoothing kernel, deterministic or predictable time atoms of the compensator, a continuous martingale part, arbitrary singular finite-variation terms, or uncontrolled growth of the characteristics into the past. Random/path-dependent **compensator kernels** are allowed because they remain predictable. The written theorem does not assert random smoothing kernels `g`.

## 1. All-jump compensation and the construction at minus infinity

Write `dM=z*(mu-nu ds)` on bounded intervals. For a deterministic finite interval `(a,t]`, the predictable integrand `z` has

    E int_(a,t] int z^2 nu_s(dz) ds <= K(t-a).

It therefore defines the stated square-integrable compensated integral. The lack of a finite small-jump first absolute moment is harmless: this is an L2 compensated integral, not an absolutely convergent sum of small jumps. For every positive cutoff epsilon,

    int_(|z|>epsilon) |z| nu_s(dz)
       <= epsilon^(-1) int z^2 nu_s(dz) <= K/epsilon.

In particular, the first moment of the large jumps is finite. Simplicity of the jump measure and diffuseness of its compensator in time are relevant: the jump of `M` is the single mark of `mu`, and its predictable quadratic variation is the integral of `z^2` against the compensator. No Poisson assumption is used in this isometry.

For a fixed `t`, let

    H_t(a) = int_(a,t] int g(t-s) z (mu-nu ds)(ds,dz).

If `a'<a<t`, then

    E |H_t(a')-H_t(a)|^2
       <= K int_(t-a)^(t-a') |g(x)|^2 dx.

Since `g` is in L2, this proves the L2 Cauchy property as the lower endpoint tends to minus infinity, independently of the sequence of lower endpoints. The drift integral is absolutely bounded by `B ||g||_1`. These facts justify (2.2) without requiring either an unweighted improper integral of `dM` or a martingale level defined at minus infinity. The explicitly stated bounded-interval/increment interpretation of the two-sided driver is adequate.

The offset `C0` need not have a second moment or be adapted: it cancels from every increment in the statistic. The stochastic terms to which the isometry is applied do have the required second moments.

**Attack result:** no missing first-moment, independent-increment, or remote-past assumption was found.

## 2. Prehistory stochastic Fubini, including the singular endpoint

Let `P_t` be the martingale contribution of `s<0`. For every `u>0`, its candidate derivative uses the deterministic predictable integrand `g'(u-s)z`, which is square-integrable because `u-s>=u>0` and the tail decreases exponentially. A jointly measurable L2 version of `D_u` can be chosen by the stochastic-integral construction. Its integrated second moment is bounded by

    E int_0^T |D_u|^2 du
       <= K int_0^T int_(-infinity)^0 |g'(u-s)|^2 ds du
       = K int_0^infinity min(x,T) |g'(x)|^2 dx.

The exact weight is obtained by setting `r=-s>0` and `x=u+r`: for fixed `x`, the admissible `u` range has length `min(x,T)`. Near zero the integrand is bounded by a constant times `x^(2alpha-1)`, which is integrable precisely for the required `alpha>0`; the exponential derivative tail controls infinity.

In particular,

    int_0^T (E |D_u|^2)^(1/2) du
       <= sqrt(T) (E int_0^T |D_u|^2 du)^(1/2) < infinity.

This is the integrated L2 condition for stochastic Fubini. Equivalently, one can use the bounded linear stochastic-integral map on the predictable L2 space and ordinary Bochner integration in `u`. The deterministic kernel identity is

    g(t-s)-g(-s) = int_0^t g'(u-s) du,  s<0.

The integrated kernel is again square-integrable by Cauchy–Schwarz, so Fubini gives, in L2 and hence as random variables,

    P_t-P_0 = int_0^t D_u du.

The right-hand side defines an absolutely continuous modification on `[0,T]`, with its derivative in L2 in time almost surely. No derivative value or finite derivative second moment at `u=0` is needed. In fact, a pointwise derivative norm may diverge as `u` decreases to zero; its time integral is what the proof correctly controls.

For the drift prehistory, deterministic Fubini and `|b|<=B` give the derivative bound `B ||g'||_1`. Thus the **entire** prehistory, rather than merely a finite portion of its jumps, has the regularity claimed in Section 4.

If `A` is absolutely continuous with square-integrable derivative, each grid interval satisfies

    |A_(i Delta)-A_((i-1)Delta)|^2
       <= Delta int_((i-1)Delta)^(i Delta) |A'_u|^2 du.

Summation proves (4.2) with exponent `1-2alpha>0`. The endpoint roles are distinct and correctly stated: `alpha>0` controls the derivative integrals, while `alpha<1/2` makes this normalized smooth energy vanish.

**Attack result:** stochastic Fubini is justified at the stated level, including the singular endpoint and the infinite past. The exact geometry identity was additionally checked by 2,448 exact rational rectangle cases; that computation is only an algebraic supplement, not a substitute for this stochastic argument.

## 3. Future drift after the large-jump cutoff

For fixed positive epsilon, the compensated large-jump integral is the finite raw jump sum minus its absolutely continuous compensation. Indeed,

    E N_epsilon(T) <= KT/epsilon^2,

so there are finitely many retained jumps almost surely. Its compensating drift is predictable and obeys the deterministic essential bound

    |b_s - int_(|z|>epsilon) z nu_s(dz)| <= B+K/epsilon.

No symmetry is needed. Cancellations of the signed first moment need not be invoked because its absolute value is controlled.

For an arbitrary bounded predictable `h`, use `g(0)=0` and the absolute continuity of `g` to write the future convolution's derivative as

    d/dt int_0^t g(t-s)h_s ds = int_0^t g'(t-s)h_s ds

for almost every `t`. Its absolute value is at most `||h||_infinity ||g'||_1`. This does not differentiate `h` and is valid even when `h` has very irregular sample paths. It applies to `b^epsilon`, yielding the needed negligible energy for each fixed epsilon.

The bound grows as epsilon decreases. That creates no gap because the proof first sends the mesh to zero at a fixed cutoff, and only afterward removes the cutoff. There is no unjustified simultaneous choice of cutoff and mesh.

**Attack result:** the compensation sign, first-moment control, regularity, and order of limits all pass.

## 4. Uniform small-jump energy for a path-dependent compensator

For the small-jump remainder `R^epsilon`, each increment is exactly the stochastic integral over `(0,T]` of

    k_(i,Delta)(s) z 1_(|z|<=epsilon),

where `k` is extended by zero after the increment's terminal time. This integrand is predictable. Time/state/path dependence in `nu_s` does not make the integrand anticipative. The martingale isometry and Tonelli give

    E[Delta^(-2alpha) V_Delta(R^epsilon;T)]
      = E int_0^T int_(|z|<=epsilon)
          [Delta^(-2alpha) sum_i |k_(i,Delta)(s)|^2] z^2 nu_s(dz) ds
      <= C_g,alpha q_epsilon(T),

where

    q_epsilon(T)=E int_0^T int_(0<|z|<=epsilon) z^2 nu_s(dz) ds.

The deterministic Section 3 bound is uniform in both `s` and the mesh. It is used only for `s` in `[0,T]`, exactly its stated domain. At almost every `(omega,s)`, the measure `z^2 nu_s(dz)` is finite and the sets `0<|z|<=epsilon` decrease to the empty set. Therefore their masses decrease to zero. Domination by `K` on a finite time interval gives

    q_epsilon(T) -> 0.

This convergence requires no uniform jump-activity exponent, no intensity bound for all small jumps, and no deterministic rate in epsilon. It remains valid for random kernels whose mass moves toward zero in a path-dependent manner. This proves precisely the uniform-in-mesh error estimate required for truncation.

**Attack result:** no missing independence, rate, or small-jump first-moment assumption was found.

## 5. Stable convergence, marks, and all observation horizons

For fixed epsilon and `T` equal to the largest observation horizon, the retained jump count has predictable intensity bounded by `K/epsilon^2`. Repeated compensation of ordered, strictly increasing times gives the factorial-measure bound in (5.2). The integrand involving all earlier jumps is predictable when the last time is compensated. Iterating the deterministic intensity bound produces the stated product Lebesgue bound. Simplicity excludes same-time duplicate marks.

On `{N_epsilon(T)=m}`, the full ordered time vector is absolutely continuous: its law is a submeasure of the factorial measure. If `H` is **any** bounded variable measurable for the whole original sigma field, the signed measure

    A |-> E[H 1_(N=m) 1_(S in A)]

is absolutely continuous as well, with a finite L1 density. The same remains true after multiplying by bounded measurable functions of the original marks. Hence the weighted Fourier/Riemann–Lebesgue argument applies against all original-field weights, including variables depending on the prehistory, the future, and the predictable coefficients. There is no need for the jump times to have a joint density with the marks, or to remain conditionally absolutely continuous after revealing all of the original field.

The phase dependency therefore supplies independent uniforms relative to the entire original field in exactly the needed stable sense. For unbounded jump sizes one first restricts the finite original mark vector to a compact set, applies bounded continuous approximation there, and then removes this restriction by tightness. No extra moment is needed for this fixed-cutoff continuous-mapping step.

A measurable enumeration of all original jumps can be chosen by positive-time windows and mark-size shells, then chronological ordering inside each finite piece. The bounds ensure these pieces are finite almost surely. There is no need to chronologically enumerate an infinite-activity set starting at zero. Attach one countable independent uniform family to this enumeration on a product extension. Conditional on the original field, the uniforms on any finite, original-measurable set of jump indices remain independent uniforms. This couples the fixed-cutoff limits consistently for every cutoff and every horizon.

One retained time/mark/phase vector up to `T` gives all the fixed observation times jointly. The deterministic impulse and cross-term assertions apply pathwise to every finite configuration of distinct jump times. The indicator `1_(S<=t_j)` is continuous at the realized vector almost surely because compensation excludes jumps at every deterministic `t_j`. A finite random number of jumps is handled by conditioning on the count and then removing its count tail using its finite expectation.

The vanishing smooth/prehistory term may be added to the finite impulse statistic using the reverse triangle inequality for square roots; fixed-cutoff stable convergence supplies the necessary tightness. Thus (6.1) is justified jointly, not merely separately at each horizon.

**Attack result:** no hidden Poisson, independent-increment, time-only stability, or inconsistent-marking assumption was found.

## 6. Direct independent check of the stable converging-together step

Write `A_n(t)=Delta_n^(-2alpha)V_n(X;t)` and define `A_n^epsilon` analogously. Let `Y_n` and `Y_n^epsilon` be their coordinatewise square-root vectors at the `r` horizons. By (6.3), monotonicity of the remainder's accumulated energy, and the small-jump estimate,

    E ||Y_n-Y_n^epsilon||_2 <= sqrt(r C_g,alpha q_epsilon(T)),

uniformly in `n`.

Compensation also gives

    E sum_(0<s<=T) J_s^2 <= KT,

so the full sum is finite almost surely. With the common uniform marks, the nonnegative truncated limits increase to `Z`, and

    E[Z_T-Z_T^epsilon]
       <= f(0)^2 ||W_alpha||_infinity q_epsilon(T).

Consequently their square-root vectors satisfy

    E' ||sqrt(Z)-sqrt(Z^epsilon)||_2
       <= sqrt(r f(0)^2 ||W_alpha||_infinity q_epsilon(T)).

Let `H` be bounded and original-field measurable, and let `phi` be bounded Lipschitz on the finite-dimensional vector space. Insert `Y_n^epsilon` and `sqrt(Z^epsilon)` between `Y_n` and `sqrt(Z)`. The two outside test errors are bounded by `||H||_infinity Lip(phi)` times the two displayed L1 bounds. The middle test error tends to zero for fixed epsilon by (6.1) and the continuous square-root map. Taking the upper limit in `n`, then sending epsilon to zero, proves stable convergence against every such `H` and `phi`. Bounded Lipschitz tests determine the required weak convergence for each bounded original-field weighting. Finally, coordinatewise squaring is a continuous map and recovers (2.4).

This derivation uses no independence between the compensator, jumps, or prehistory; no interchange of the two limiting operations; and no additional tightness assumption. It also explicitly controls the original-field weighted errors, which is the point that an ordinary weak converging-together statement alone would not settle.

**Attack result:** the stable order of limits and the common coupled limits pass.

## 7. Versions and boundary checks

The theorem evaluates countably many mesh points for each deterministic mesh sequence. Integral decompositions and the prehistory modification can therefore be imposed simultaneously at all relevant mesh points and at the finitely many horizons on one event of probability one. For cutoff removal it is enough to choose a deterministic sequence of positive cutoffs decreasing to zero; this also makes all decomposition identities simultaneous. The theorem does not require an unjustified equality at every time on an uncountable family of exceptional sets.

A stronger consistency check is available: the derivative bound in Section 3 implies the deterministic translation estimate

    int_R |g(x+h)-g(x)|^2 dx <= C h^(2alpha+1),  h>0.

Split the integral into a region of length of order `h`, where `|g|<=C x^alpha` applies, and its complement, where the mean value bound gives `C h x^(alpha-1)` and `int_h^infinity x^(2alpha-2) dx` is finite. The isometry therefore gives the same increment-moment bound for the full martingale convolution. The drift has a Lipschitz modification, so Kolmogorov's criterion supplies a continuous modification of the convolution. This extra fact is not needed for the countable-grid claim, but confirms that the pathwise interpretation is consistent.

Other checked cases:

- `K=0` gives no jumps on finite intervals and the zero limiting statistic, with the smooth part vanishing.
- Unbounded but finite realized retained jump sizes are harmless at a fixed cutoff; there are finitely many of them on a fixed horizon.
- Infinite jump activity and a Blumenthal–Getoor boundary value of 2 do not invalidate the finite quadratic-rate/DCT argument.
- Jumps exactly at a size cutoff cause no ambiguity: the sets `|z|>epsilon` and `|z|<=epsilon` partition the marks exactly.
- Mesh endpoints at a jump time do not create a phase discontinuity because `W_alpha(0)=W_alpha(1)`; deterministic observation horizons carry no jumps almost surely.
- Arbitrarily close retained times cause no uniform-spacing assumption: each realized finite configuration has strictly positive minimum spacing, and the deterministic impulse argument is applied pathwise.
- The endpoints `alpha=0` and `alpha=1/2` are excluded for reasons actually used in the proof; the proof does not silently claim either endpoint.
- Compensation with diffuse time, rather than merely nonatomic marginal jump times, is crucial. Allowing predictable time atoms would invalidate the factorial-density mechanism and generally require a different phase statement.

## Final disposition

**PASS.** Within the written hypotheses and the assigned stochastic/truncation scope, the theorem's construction and proof are mathematically supported. The strongest verified result is the stated finite-dimensional fixed-time stable limit for the bounded-characteristic, diffuse-time-compensator pure-jump class with the deterministic kernel (K). There is no remaining stochastic gap identified in Sections 2, 4, or 6 or in their interface with Sections 3 and 5. This disposition makes no claim about novelty, optimality, maximal scope, or any functional topology.

Review completion estimate: **100% of the assigned independent review**. This is not a percentage estimate of mathematical novelty or of a larger research program.
