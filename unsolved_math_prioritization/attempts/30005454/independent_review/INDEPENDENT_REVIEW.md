# Independent final review: critical WARM on the line,30005454

**Verdict: PASS for the five-turn scoped partial package. No mandatory mathematical correction. The original full temporal convergence conjecture remains unsolved5/5.**

Reviewed2026-10-01. Author manifest SHA-256:`6c830f90b49df30406de2d6e5e5eaccfcdc3c14235b92e3d3e7e0158f2a74e00`. `RESULT.md` SHA:`c73be94dc16dce80b054f7161d92c6ffc8d17350bc1b531f9ec893ca02c76117`. Strongest partial theorem, `turns/TURN_5.md`, SHA:`15c8dd2b4e7c898f8531e25079334ba71772a992ef95e02768f6ae61a8ac9f5f`. All13 frozen files and three source PDFs matched their hashes.

The reviewer independently studied an adjacent alpha>1 lattice question, but supplied no proof ingredient to this alpha=1 line package. Sharing the OWR source was coordination only. This review does not certify historical novelty, human peer review, or the full conjecture.

## Source and precise initialization

The exact question is Conjecture2 of Kleptsyn's contribution to [OWR12/2023](https://ems.press/content/serial-article-files/47008), printed p655. Its observable is the normalized edge tally, despite an indexing slip in the displayed conjecture. Its graph is the nearest-neighbor line, every vertex clock has rate1, and reinforcement exponent is1. It is an interacting edge-urn process, not a random walk.

The source does not specify the initial-count convention next to the conjecture. The inspected [Couzinie–Hirsch primary paper, arXiv2010.03347v2](https://arxiv.org/abs/2010.03347v2), explicitly sets every initial tally to1; its Theorem2.2(3) covers alpha<1, not the critical value. The [longer workshop collection](https://www.matrix-inst.org.au/wp_Matrix2016/wp-content/uploads/2023/Aletti.pdf) repeats the omission. The submitted claims consistently use the standard unit initialization. No result for arbitrary unspecified or zero initial weights is inferred.

## 1. Harmonic martingales and growth

With h(n)=H_(n-1), a jump from n to n+1 changes h by exactly1/n. Multiplying the birth rate by that increment gives the displayed sum of two reciprocal neighboring pair counts. The compensated process is therefore an exact martingale. Its optional quadratic variation is bounded pathwise by sum_n1/n²; compensator equality gives a uniform L2 bound. The convergence assertions follow without presupposing positive limiting proportions.

The individual count is bounded by its two endpoint clocks, and a two-edge count by three clocks; the lower pair bound uses the middle clock. All bookkeeping is pathwise. Countably many Poisson strong laws and martingale convergence events can be intersected once, giving the asserted statements at every fixed index without a uniform-in-space bound.

The exponent2/3 lower bound follows by integrating the reciprocal three-clock upper bounds. For the improvement to exponent1, the exponential of the compensated harmonic count is absolutely continuous and comparable to the original count by finite pathwise constants. The scalar inequality R'≥2R/(CR+(2+epsilon)t) and the subsolution Kt^beta are valid. Choosing pathwise constants for this deterministic differential comparison is legitimate; it is not a stochastic coupling conditioned on a future event. Letting beta approach1 gives logarithmic growth exponent1, while correctly leaving the lower linear rate unproved.

## 2. Existing limits, zeros, and ergodicity

If all normalized limits exist, adjacent zeros would make a reciprocal term arbitrarily large on the logarithmic scale, contradicting the two-clock growth upper bound. Positive limits satisfy the displayed equilibrium relation by logarithmic Cesaro averaging. If one limit is zero, the corresponding logarithmic exponent is the sum of the reciprocal neighboring limits. Since each neighbor is at most2, the exponent bound forces both neighbors to equal2; the equilibrium relation then propagates the alternating0,2 profile. The all-positive case likewise reduces to an alternating profile by boundedness of the two-sided line.

For an actual pathwise limiting profile, the even-site value is a measurable shift-two invariant function of the iid marked-clock environment. The translation-covariant graphical construction gives the required ergodicity. Shift-one invariance then forces that deterministic value to equal its complement, hence1. The same argument is correctly applied to pathwise liminf/limsup envelopes, producing complementary deterministic bounds without forcing them equal.

No ergodicity assertion is made about an arbitrary weak subsequential law. That distinction is essential and is respected.

## 3. Local entropy identities and adjacent-sum convergence

Translation invariance gives E lambda_i=1 exactly: after shifting one summand, the two local fractions sum to1. Hence E N_i=t+1 and the normalized pair mean is2.

The log-pair generator identity is correct. The key translated expectation is

E[(lambda_0+lambda_1)/S_0]=E[N_0(1/S_(-1)+1/S_0)²].

After subtracting the normalization derivative and using the two mean identities, this is the weighted square defect. The Taylor remainder is nonnegative and bounded by3E(S_0^-2)/2. Integrating the Poisson lower bound gives the finite sum sum_(n≥0)(n+2)^-2. Jensen's upper bound on E log T then proves integrability of the local weighted dissipation. There is no infinite spatial entropy sum.

The second harmonic-entropy identity has no Taylor error. The algebra

(T-2)²/(2T)=T/2-2+2/T

and E T=2 give its derivative exactly. The classical harmonic bounds0≤h(n)-log n≤gamma give a nondecreasing quantity between0 and gamma. Thus the pair-error integral is finite in expectation and, by Tonelli, almost surely at every fixed index.

The conversion from finite integral to convergence is justified. The normalized count-noise martingales have finite total expected bracket and converge. On each finite neighborhood, eventual clock bounds put the relevant pair sums away from0 and counts in a fixed compact interval. The local defect functions are Lipschitz there, normalized drift is bounded, and the entire late martingale oscillation tends to0. Therefore recurring positive defects would occupy infinitely many disjoint intervals of a common positive logarithmic-time length, contradicting their finite integrals. This handles the jump paths without falsely assuming ordinary differentiability.

Consequently every fixed adjacent normalized sum tends almost surely to2. Finite spatial telescoping identifies one remaining time-dependent alternating phase. This statement alone supplies no growing-window control; the fifth turn derives such a bound separately.

## 4. Diffusion and flux reductions

The staggered affine-variable formula, the two directed-coefficient sum1/2, and the logarithmic conservative flux all check algebraically. The full drift is cooperative in the stated variables. The positivity-preserving comparison with constant staggered equilibria is valid under the displayed bounded positive deterministic hypotheses; it does not give the stochastic process a uniform spatial ellipticity bound.

The linear Fourier rate is sin²(theta/2), and the even-cycle gap sin²(pi/L) does vanish with growing L. The finite periodic conserved quantity is sum_i(-1)^i log z_i, equivalently the sum of the stated staggered log coordinates. It is not an exactly conserved stochastic log product.

The harmonic-difference identity correctly makes convergence of the specified boundary-flux integral equivalent to the desired full unit-model limit. The supplied L2 counterexample correctly explains why squared-integrability and vanishing integrands do not establish that condition. No unsupported L2-to-L1 or boundary-integral convergence step is used.

## 5. Deterministic almost-sure homogenizing subsequence

This strongest partial theorem passes the following detailed checks.

**Reciprocal estimate.** The Poisson identity E[1/(2+P(t))]=(t-1+exp(-t))/t² is correct, and multiplication by t+1 is at most1 because(1+t)exp(-t)≤1. It yields the stated uniform E(1/T) bound, including t=0 separately. Cauchy–Schwarz then gives both absolute pair-error and reciprocal-error estimates with the displayed constants.

**Orthogonal block martingales.** Distinct edge martingales have disjoint jumps, though their histories are dependent. Continuous compensators add no cross jumps. Their predictable cross variations are zero, so the L2 block-average bound is proportional to1/L. Independence of edge histories is neither available nor needed.

**Boundary and spatial errors.** Even block length cancels every interior reciprocal term and leaves precisely the two endpoints. The logarithmic-time expected boundary error is bounded by the integral of sqrt(2D), hence by sqrt(2gamma tau)/L. The maximum phase discrepancy in a deterministic block is bounded pathwise by the sum of its adjacent-pair errors, so its expectation is at most2L sqrt(D). This estimate is valid at indices growing with time because translation invariance is applied at each deterministic time; fixed-window convergence is not being silently made uniform.

**Deterministic time selection.** Nonnegative integrability implies liminf tau D(tau)=0. Therefore one can choose increasing deterministic tau_n≥n², separated by more than1, with tau_nD(tau_n)≤n^-16. This is an existential deterministic selection from the law, not an explicit computable calendar sequence or a sample-dependent stopping time. The least even L_n≥n³sqrt(tau_n) obeys the stated ceiling bounds.

The resulting bounds are respectively O(n^-4) for the martingale square, O(n^-3) for the boundary absolute value, and at most2n^-5+4n^-9 for the maximum local phase error. All sums converge. Tonelli therefore supplies one probability-one event on which all three errors vanish. No independence between selected times is required.

**Endpoints and logarithms.** With epsilon1/10, a phase near0 forces each paired harmonic difference below the fixed negative bound involving log(1/9)+gamma; near2 forces the opposite sign. Those bounds are strict, and contradict convergence of the block harmonic average to0. Thus the selected phases eventually stay in a compact subinterval of(0,2). The whole growing block then has counts at least(t_n+1)epsilon/2, so h(m)-log m→gamma is uniform throughout it. Equal numbers of even and odd terms cancel gamma, and the logarithm has a uniform Lipschitz bound on the relevant interval. The block average therefore differs from half the log phase ratio by a quantity tending to0, forcing phase1.

Finally the already simultaneous adjacent-sum theorem propagates the selected-time limit to every fixed positive and negative edge. Changing t_n+1 to t_n is harmless. The conclusion is exactly one deterministic sequence with simultaneous almost-sure convergence at all fixed edges.

Nothing in this argument bounds the selected-time gaps. It does not exclude intervening excursions, establish a positive pathwise lower linear rate, or prove convergence of the boundary flux. Thus the full target correctly stays unresolved.

## Reproducibility and disposition

The independently written standard-library checker passes **11,678 exact finite assertions**. It checks harmonic generators, translated finite-average entropy identities, diffusion/flux algebra, exact boundary telescoping, Poisson reciprocal series coefficients, phase-error recurrences, deterministic ceiling/exponent bounds, and clock bookkeeping. These support, but do not replace, the probability arguments audited above.

The author's77,754 exact-control receipt replayed byte-for-byte in an isolated copy. All13 frozen author hashes and three primary PDF hashes matched. No simulation, floating probability estimate, or external executable is used as mathematical evidence.

Publication may present these as independently reviewed partial results with original status unsolved5/5. The unit-initialization and full-time-limit gaps must remain visible. There is no sixth author search turn, no novelty assertion, and no unqualified critical-line solution in this verdict.
