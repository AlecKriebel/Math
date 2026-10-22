# Independent adversarial mathematical review: deterministic kernel and truncation

Frozen candidate: `../submitted/unsolved_math_prioritization/attempts/30002291/PROOF.md` relative to this review directory. SHA-256: `508f71b81ee669d4934ef1cc9e061c129e47d36359896ad7b3e20574dbfbc539`.

Review scope: Sections 2–4 and 6–7; Section 5 was read to identify precisely the phase input used by Section 6. I did not read the candidate's inherited `independent_review/`, the parent's reconstruction, or sibling verdicts. I used only the frozen proof and my own derivations. No external source or novelty assessment is part of this report.

## Verdict and strongest verified claim

**PASS for the assigned mathematical scope. No fatal gap or false boundary assertion was found under the candidate's stated hypotheses.** The deterministic energy, phase indexing, prehistory smoothing, finite-jump localization, and sequential small-jump removal arguments are valid for every deterministic positive mesh sequence tending to zero and every finite list of positive deterministic observation horizons. The strict range `0<alpha<1/2` is used correctly. The deterministic-time counterexample is valid and genuinely separates a deterministic phase from the uniform-phase law.

The strongest verified claim is the proposed sufficient-conditions finite-dimensional stable limit, conditional on the Section 5 phase statement; I also checked the mathematical mechanism giving that statement from a deterministically bounded diffuse jump intensity and found no defect. The proof does not establish a functional topology, a maximal driver class, or novelty, and this review makes none of those claims.

The exact proof obligation left outside my assigned specialization is independent source-scope/novelty review. There is no mathematical repair required in the assigned sections. Several optional clarifications below make the proof more directly checkable, but they do not add hypotheses or change the result.

## 1. Exact target and boundary conventions

The driver has bounded predictable drift and compensator `nu_s(dz) ds`, with deterministic uniform bounds `|b_s|<=B` and `int z^2 nu_s(dz)<=K`. Its jump measure has at most one nonzero mark per time and no continuous martingale part. The kernel is real-valued, `g(x)=x_+^alpha f(x)`, taking value zero for `x<=0`, with `0<alpha<1/2`, `f(0)!=0`, and exponentially bounded `f,f'`. All large jumps are compensated, so the ordinary drift changes when large jumps are exposed as an uncompensated finite sum.

The statistic stops at `N=floor(t/Delta)`, not at a rounded-up horizon. Its proposed limit includes jumps in `(0,t]`. For fixed positive `s<t`, the stop index eventually includes every fixed number of post-jump increments. The finitely many deterministic horizons have no jumps almost surely by the diffuse compensator. This suffices; no uniform claim over moving horizons or over jump times converging to a horizon is needed.

The candidate can choose any version of the convolution defined at deterministic times: the countably many grid points from one prescribed deterministic mesh sequence agree almost surely with the modifications used in the proof. There is no hidden requirement to prove a globally continuous version of the future jump convolution.

## 2. Kernel bounds reconstructed

For positive `x`,

`g'(x)=alpha*x^(alpha-1)*f(x)+x^alpha*f'(x)`.

The exponential hypothesis implies a finite global constant `C_g` with

`|g(x)|<=C_g x^alpha`, `|g'(x)|<=C_g x^(alpha-1)`.

For the derivative inequality, the second term is controlled because `sup_(x>=0) x exp(-cx)<infinity`. Near zero, `g'` is integrable because `alpha>0`. At infinity it decays exponentially, so `g,g'` are in the stated spaces. In particular,

`I_T := int_0^infinity min(x,T)|g'(x)|^2 dx < infinity`

because its near-zero integrand is `O(x^(2alpha-1))`. No unweighted `L2` claim for `g'` near zero is being made. Such a claim would be false in this alpha range; the candidate does not need it.

For `s/Delta=j+u`, `j=floor(s/Delta)` and `0<=u<1`, nonzero impulse increments begin exactly at `i=j+1`. Put `i=j+ell`. Their arguments are exactly

`i*Delta-s=Delta*(ell-u)`,

`(i-1)*Delta-s=Delta*(ell-1-u)`.

Thus the claimed `W_alpha(u)` indexing is correct. In particular, an exact grid hit has `u=0` and its first contribution is the next interval, with value `Delta^alpha f(Delta)`. It is not shifted to the preceding interval, and no half-open-time convention changes it because `g(0)=0`.

The first two nonzero increments are bounded by a constant times `Delta^alpha`. For `ell>=3`, the entire derivative integration interval is at least `Delta*(ell-2)` from zero. Since `alpha-1<0`,

`|k_(j+ell,Delta)(s)| <= C_g Delta^alpha (ell-2)^(alpha-1)`.

The convergent series `sum ell^(2alpha-2)` proves the energy bound uniformly over `Delta>0`, `s in [0,T]`, and `T`. Enlarging a finite horizon to the whole positive impulse tail only increases its energy. Neither the number of grid intervals nor `T` enters its constant.

## 3. W_alpha, endpoints, and a stronger independent approximation

Write

`d_ell(u)=(ell-u)_+^alpha-(ell-1-u)_+^alpha`.

The first two summands are continuous on `[0,1]`. The derivative bound gives a uniformly summable majorant for all later summands. Hence `W_alpha=sum d_ell^2` is bounded and continuous. At the endpoints, `d_1(1)=0` and `d_ell(1)=d_(ell-1)(0)` for `ell>=2`, proving `W_alpha(1)=W_alpha(0)`. This is actual periodic continuity, not merely an almost-everywhere convention. A phase approaching `1` therefore gives the same limiting value as one approaching `0`.

For `M-u>0`, there is also a useful sharper tail estimate, directly by Cauchy–Schwarz over unit intervals:

`sum_(ell>M) d_ell(u)^2 <= alpha^2 int_(M-u)^infinity x^(2alpha-2) dx`

`= alpha^2/(1-2alpha) * (M-u)^(2alpha-1).`                                      (A)

I independently reconstructed the single-impulse claim using a different decomposition. Set

`p(x)=x_+^alpha`, `r(x)=g(x)-f(0)p(x)`.

On `(0,1)`, continuity of `f'` gives `r'(x)=O(x^alpha)`. At infinity,

`r'(x)=-alpha f(0)x^(alpha-1)+O((x^(alpha-1)+x^alpha)e^(-cx))`.

Therefore `r` is absolutely continuous, zero on the negative half-line, and **`r' in L2(R)`**. Its failure to decay at infinity is harmless; only its derivative is used. For every shifted grid and every finite collection of its intervals,

`sum_i |r(i*Delta-s)-r((i-1)*Delta-s)|^2 <= Delta ||r'||_2^2`.

Consequently its normalized increment-vector norm is at most

`epsilon_Delta = Delta^(1/2-alpha)||r'||_2 ->0`.                               (B)

Let `M_alpha=sup W_alpha<infinity`. The normalized squared-energy error between `g` and `f(0)p`, over any finite horizon, is bounded by

`(2|f(0)|sqrt(M_alpha)+epsilon_Delta)*epsilon_Delta`.                          (C)

This bound is uniform in the impulse position, phase, and horizon. For `s<=t-eta` and `Delta<eta/2`, the omitted pure-power tail after `N=floor(t/Delta)` has `M-u=(N*Delta-s)/Delta >= eta/(2Delta)`. By (A), its normalized energy is at most

`alpha^2/(1-2alpha)*(2Delta/eta)^(1-2alpha)`.

Together with (C), this proves the candidate's single-impulse formula uniformly over impulses separated from the terminal horizon by any fixed `eta`. It also proves it for every individual fixed `0<s<t`, without any assumption that the phases converge. This independently verifies both arbitrary deterministic meshes and phase-endpoint cases.

## 4. Cross-impulse localization

For fixed `eta>0` and `Delta<eta/2`, every grid increment whose right endpoint exceeds `s+eta` samples `g'` only at arguments at least `eta-Delta`. Direct Cauchy–Schwarz gives

`Delta^(-2alpha) sum_(i*Delta>s+eta) |k_i(s)|^2`

`<= Delta^(1-2alpha) int_(eta-Delta)^infinity |g'(x)|^2 dx ->0`.                (D)

The integral is finite because its lower endpoint stays away from zero. The candidate's discrete-tail proof gives the same conclusion using its global derivative bound.

For a finite list of distinct impulse times, choose disjoint right neighborhoods shorter than half the minimum positive separation. For sufficiently small meshes, the retained grid endpoint sets are disjoint. A later impulse has no contribution before its jump because `g=0` on nonpositive arguments. Formula (D) bounds discarded normalized norms, and the uniform total-energy bound bounds the retained norms. Cauchy–Schwarz then makes every normalized cross inner product vanish. Random amplitudes cause no problem: at each fixed truncation there are finitely many almost surely finite amplitudes, so this is a pathwise finite sum, without a need for higher moments or a deterministic minimum gap.

This argument does not assert uniform localization as the jump separation tends to zero together with the mesh. Fixed-epsilon finite truncation is what makes that stronger assertion unnecessary.

## 5. Negative history and absolutely continuous terms

Let `y=-s>0`. The isometric derivative estimate for the prehistory martingale is exactly

`E int_0^T |D_u|^2 du <= K int_0^T int_0^infinity |g'(u+y)|^2 dy du`.

Changing variables `x=u+y`, the allowed `u` interval has length `min(x,T)`, yielding exactly `K I_T`. Thus the weight in the candidate is correct; there is no missing factor, missing integration range, or near-zero divergence. The candidate derivative exists in `L2` for every `u>0`. Its value at `u=0` need not exist.

For a directly checkable example `g(x)=x^alpha e^(-x)`, the stronger infinite-horizon weighted integral has the exact value

`int_0^infinity x |g'(x)|^2 dx = alpha*Gamma(2alpha)/2^(2alpha+1)`.

It is finite for every stated alpha. At `alpha=1/4` it equals `sqrt(pi)/(8sqrt(2))`. This provides an independent check on the singularity cancellation in the weighted integral.

The standard square-integrable stochastic Fubini condition follows since

`int_0^T (int_(s<0)|g'(u-s)|^2 ds)^(1/2) du <= sqrt(T I_T)`.

The stochastic integral map is a bounded linear map from the deterministic `L2(ds)` space to `L2(P)` under the bound `K`; the displayed integrability allows interchanging that map with the time integral. It identifies prehistory increments with `int_0^t D_u du` in `L2` at every fixed time. The resulting version has almost surely square-integrable derivative and is absolutely continuous. The prehistory drift derivative is bounded by `B||g'||_1`.

For any bounded measurable future drift `h`, no time regularity of `h` is needed. Since `g(0)=0` and `g' in L1`,

`d/dt int_0^t g(t-s)h_s ds = int_0^t g'(t-s)h_s ds`

almost everywhere, bounded by `||h||_infinity ||g'||_1`. There is no boundary term `g(0)h_t`.

Finally, for any absolutely continuous `A` with `A' in L2(0,T)`,

`Delta^(-2alpha) sum_(i<=T/Delta)|A(iDelta)-A((i-1)Delta)|^2`

`<= Delta^(1-2alpha) int_0^T |A'_u|^2 du ->0`.

This includes an infinite collection of negative-history jumps: the entire past is smoothed at once, and is not being incorrectly replaced by a finite sum of impulses. Its possible singular derivative at time zero is controlled by the weight above.

## 6. The finite-truncation argument and its precise order of limits

On `(0,T]`, write the large-jump process as an uncompensated finite sum and retain the compensated small-jump martingale. The remaining predictable drift is exactly

`b^epsilon_s=b_s-int_(|z|>epsilon) z nu_s(dz)`.

It satisfies `|b^epsilon|<=B+K/epsilon`, because `|z|<=z^2/epsilon` on this region. The dependence on epsilon is allowed: first take `n->infinity` at fixed epsilon. The candidate never takes an unjustified simultaneous limit with a mesh-dependent epsilon.

For each epsilon, the large-jump count is finite almost surely with expected count at most `KT/epsilon^2`. All the preceding deterministic statements apply pathwise to its finite impulse sum. In a finite list of observation horizons, no exposed jump lies exactly at a horizon almost surely; every other jump eventually stays on its fixed side of that horizon for the purpose of including its first fixed number of impulses. The same independent phase marks can be used for all horizons.

For completeness, the phase input is mathematically consistent with this general driver. A predictable counting intensity bounded by `K/epsilon^2` gives an m-fold factorial time measure dominated by `(K/epsilon^2)^m` times ordered Lebesgue measure, by compensating the last jump and iterating. Hence the ordered time vector on the event of exactly m jumps has a Lebesgue density. Multiplication by any bounded variable measurable with respect to the entire original sigma field preserves absolute continuity of the resulting finite signed measure. Riemann–Lebesgue therefore kills all nonzero Fourier coefficients for arbitrary real meshes tending to zero. The torus continuity of W established above is exactly what this argument needs. Conditioning on the entire sigma field does not incorrectly make the phases independent at finite n; it supplies weighted L1 densities for the asymptotic Fourier argument.

For the residual small-jump convolution, its increment kernel is deterministic in time and predictable as an integrand. The diffuse compensator and one-mark-per-time condition give the usual `L2` isometry. Summing the individual increment second moments requires no independence of increments. Tonelli followed by the uniform deterministic bound gives

`sup_n E[Delta_n^(-2alpha)V_n(R^epsilon;T)]`

`<= C E int_0^T int_(|z|<=epsilon) z^2 nu_s(dz) ds ->0`.

The convergence follows by dominated convergence: the integrand decreases to zero because the mark space excludes zero and its full second moment is finite, and is bounded by deterministic `K`. State dependence or path dependence of the compensator does not interfere.

Passing through square roots is a correct way to avoid an unproved uniform bound on cross terms between the original statistic and the small-jump remainder. The Euclidean reverse triangle inequality gives the candidate's bound simultaneously at each fixed horizon. For bounded Lipschitz vector tests, its contribution is at most a constant times the square root of the last displayed expectation. That bound is uniform in n. The truncated limiting sums can be marked on a common independent product extension; their tails vanish almost surely since

`E sum_(0<s<=T) J_s^2 <= KT`, and `W_alpha` is bounded.

First taking n to infinity, then epsilon to zero proves convergence against every bounded original-sigma-field weight. Squaring the nonnegative square-root vector is continuous and recovers the stated stable finite-dimensional convergence. There is no omitted tightness requirement for a process topology because only finitely many coordinates are asserted.

## 7. Endpoint and counterexample attacks

### Alpha endpoints

At `alpha=1/2`, the tail terms of W are asymptotic to `alpha^2/ell`, so W diverges. Also the exponent `1-2alpha` in the absolutely-continuous energy estimate is zero. A generic smooth contribution need not vanish under that normalization. Both mechanisms show why this endpoint cannot be silently included.

At `alpha=0`, the stated kernel has a discontinuity at zero when `f(0)!=0`, and a derivative-only convolution argument must account for that boundary term. The present proof uses `alpha>0` correctly and makes no endpoint claim. A separately formulated alpha-zero theorem may hold with the usual semimartingale quadratic variation; it is not a consequence of the argument as written. Negative alpha has additional singular-at-jump issues and is outside scope.

Constants may diverge as alpha approaches either excluded endpoint. The theorem fixes alpha and does not require uniformity over alpha, so this is not a gap.

### Deterministic-time driver

Take one unit jump at deterministic `s>0`, any admissible kernel with `f(0)!=0`, and `Delta_n=s/n`. Then every phase is zero, and the single-impulse result at any fixed `t>s` gives the deterministic limit `f(0)^2 W_alpha(0)`. This driver intentionally violates the diffuse-compensator condition.

For `alpha=1/4`, the first summand at zero is 1, so `W_(1/4)(0)>=1`. At `u=1/2`, the first summand is `1/sqrt(2)`. Every later interval is in `(0,infinity)` and Cauchy–Schwarz gives

`sum_(ell>=2) d_ell(1/2)^2 <= (1/16) int_(1/2)^infinity x^(-3/2) dx = sqrt(2)/8`.

Therefore `W_(1/4)(1/2)<=5/(4sqrt(2))<1`, the strict inequality being exactly `25<32` after squaring positive numbers. The two values differ, and continuity gives disjoint neighborhoods with differing W values and positive uniform probability. Thus `W_(1/4)(U)` is nonconstant and cannot have the deterministic zero-phase law. This fully verifies the intended counterexample rather than merely showing phases fail to converge.

The replay uses rational root intervals and the exact infinite-series tail estimate (A), obtaining

- `W_(1/4)(0)` in `[1.1161772403284722, 1.1239897403284722]`;
- `W_(1/4)(1/2)` in `[0.8715964720705305, 0.8794166126591537]`.

These decimal displays describe exact rational enclosures stored in the receipt; floating-point arithmetic decides no assertion.

## 8. Optional clarifications and exact remaining gap

No change is necessary to make the assigned mathematical argument valid. Useful optional additions would be:

1. State the impulse substitution `i=floor(s/Delta)+ell` explicitly next to (3.3), and make the positive-argument convention `g(0)=0` explicit once.
2. Add either the tail integral (A) or the `r=g-f(0)x_+^alpha` decomposition as a short independently checkable uniform control. This also makes arbitrary nonmonotone mesh sequences transparent.
3. Spell out that the Fubini integrability bound is `sqrt(T I_T)` and that no derivative at time zero is being asserted.
4. Emphasize the sequential order `n->infinity` before `epsilon->0`; the bound on `b^epsilon` is intentionally not uniform in epsilon.

The remaining gap is not an unresolved kernel or probability estimate in these sections. It is the separate historical/scope question and any desired extension beyond the written hypotheses. A proposal to include deterministic compensator atoms, `alpha=1/2`, continuous martingales, uncontrolled singular drift, or a functional topology would require new work and is not verified here.

## 9. Replay and provenance

Authored artifacts are `REPORT.md`, `RESEARCH_LOG.md`, `exact_controls.py`, `replay_receipt.json`, and `authored_manifest.json`. The executable checks use only Python's standard library, exact integer arithmetic and `fractions.Fraction`. No Monte Carlo, external source download, inherited script, or sibling-review data was used. Run from any directory:

`python3 /Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr234_30002291/initial_review_20261015/kernel_adversary_01/exact_controls.py`

The actual completed replay receipt records UTC times, platform/interpreter, script hash, frozen proof hash, exact rational W enclosures, and each PASS. This review directory is the only write target. The third-party/frozen candidate remains read-only and is referred to by hash; no full third-party material is republished in the authored output. No Git, index, reference, provider, email, or external-message operation was used.
