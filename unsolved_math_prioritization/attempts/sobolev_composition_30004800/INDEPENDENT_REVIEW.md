# Independent second mathematical review: row 1888 / 30004800

Date: 2026-10-21 UTC. Scope: the exact composition question and the complete dependency chain establishing it, not all ancillary sharpness or literature-priority assertions in the 24-page manuscript. 

## Verdict

PASS for the intended full-Fourier, real-input interpretation of the original question. Ferudun's October 9, 2026 unrefereed preprint supplies an attributed existing solution, not a new solution produced by the reviewers. I independently re-derived Sections 2–6 needed for Theorems 1.1, 1.2 and Corollary 1.3(b), including the explicit exponents and finite-smoothness integral bounds. No mathematical gap or missing hypothesis in this dependency chain was found. This verdict is a substantive proof audit, not a claim of journal peer review or mathematical-community acceptance.

The literal printed N^2 exponential-index formulation is not the intended full Fourier norm: the exponentials with these indices are not a basis. The result being accepted uses Z^2 and absolute squares. These are explicit mathematical interpretation corrections, not an authenticated author erratum. Under a literal quadrant-only interpretation, take phi=A cos(x1-2x2)+B cos(2x1-x2) and G(u)=u+u^2. Its quadrant input coefficients vanish, whereas G(phi) has a nonzero (1,1) coefficient if AB is nonzero. Thus the literal misprint has a counterexample; it is not a counterexample to the accepted intended question.

## Independently verified chain

1. Define c_l by normalized Haar integration and m_l=sup_t |c_l(phi(t))|, with X norm equal to the weighted l^2 norm of m. For s>d/2, Cauchy–Schwarz gives ||m||_1<=K_s ||m||_s. All members consequently have continuous, absolutely convergent Fourier representatives. Composition is well-defined for real-valued representatives, and their values lie in [-K_s r,K_s r] on an X-ball of radius r. No regularity in the parameter t is needed.

2. Absolute convergence permits the Fourier product identity. Taking the supremum only after the coefficientwise triangle inequality gives env(uv)<=env(u)*env(v). The weight inequality yields ||a*b||_s<=c_s(||a||_s||b||_1+||a||_1||b||_s). Induction gives the manuscript's convolution-power estimate k c_s^(k-1)||a||_1^(k-1)||a||_s. These estimates do not incorrectly substitute the supremum of Sobolev norms for the envelope norm.

3. The lattice-cube argument gives a tail bound sum_{|l|>rho}m_l <= C_T(1+rho)^(-sigma)||m||_s, sigma=s-d/2>0. Its comparison 1+max(rho-sqrt(d)/2,0)>=(1+rho)/(1+sqrt(d)/2) holds in both cases. Thus the cutoff can be chosen uniformly on the unit ball, not separately for each family or parameter. Splitting on a symmetric Euclidean ball preserves real-valuedness of the low part.

4. For the high part, the exponential series has a nonnegative convolution majorant v. The cutoff ensures c_s |lambda| ||m_H||_1<=1, hence ||v||_s<=e|lambda| and c_s||v||_1<=e-1. No smallness of the high part in weighted l^2 is assumed.

5. For the low part U=exp(i lambda psi_L), real-valuedness gives |U|=1 and consequently every Fourier coefficient is bounded by 1, uniformly over the whole family. The derivative identity and a coordinate of maximum absolute frequency give e_l<=sqrt(d) nu/|l| max_{|k|<=rho}e_{l-k}, where nu=|lambda| sum |k|m_k. Iterating N times is legitimate when |l|>=2(N-1)rho; all denominators then stay positive and at least |l|/2. It follows that the envelope is bounded by min(1,(R/|l|)^N), including the separately treated zero mode and R=0 case.

6. The dyadic-shell sums for this profile converge for N=ceil(s+d/2+1/2). The l^2 exponent has margin at least 1; the l^1 exponent N-d is a positive integer, hence at least 1. The printed bounds on both norms dominate the ball and shell sums. Combining U+UV gives ||exp(i lambda psi)||_X <= e||p||_s+e c_s |lambda| ||p||_1.

7. For 0<=theta<=1 with theta<sigma, nu<=|lambda|K_{s-theta}(1+rho)^(1-theta). The radius grows at most as (1+|lambda|)^kappa, kappa=1+(1-theta)/sigma. It dominates the cutoff because kappa-1/sigma=1-theta/sigma>0. The second assembly term has exponent 1+d kappa, bounded by (s+d/2)kappa because sigma kappa=sigma+1-theta>=1. The claimed polynomial bound and its constant therefore follow, including sigma=1 where theta=1 is forbidden and the limiting exponent is only an infimum.

8. To recover a homogeneous estimate, enlarge the index set to [0,1] times the original set and apply the exponential bound to tau phi/r. The identity exp(i lambda u)-1=i lambda u int_0^1 exp(i tau lambda u) d tau provides one factor ||phi||_X. In particular, the final estimate is not merely a bound on the unit ball.

9. The integral/composition step is valid for arbitrary index sets. For fixed t and l, scalar Fubini is justified by |exp(i lambda phi)-1|<=|lambda|K_s r. For fixed l, the envelope of the difference is a supremum of continuous functions of lambda, hence lower semicontinuous and Borel measurable even for an uncountable index set. One takes the coefficientwise supremum under the scalar integral, then weighted l^2 Minkowski; the assumed first weighted moment of the representing measure dominates this integral. There is no hidden assumption of parameter measurability and no illicit exchange of supremum with an equality or Parseval identity.

10. Choose a compactly supported C^k function H agreeing with G on the attained real interval. H(0)=0. Fourier inversion represents H by exponential differences. Repeated integration by parts gives the integrable moment when k>M+2, which alone proves the smooth-G question. The stated improvement k>M+3/2 also checks: Cauchy–Schwarz splits off (1+|lambda|)^(M+1-k), whose squared integral is 2/(2k-2M-3), while Plancherel controls the other factor by 2^(k-1)sqrt(2pi)(||H||_2+||H^(k)||_2). The printed constants match these estimates.

11. On the original two-dimensional torus with orthonormal basis (2pi)^(-1)exp(i l.x), the original coefficient is 2pi times c_l. Thus N_s=4pi^2||.||_X^2, the unit ball corresponds to r=1/(2pi), and squaring the homogeneous X estimate gives N_s(G(phi))<=C_B^2 N_s(phi). The constant depends on G and s after fixing an allowed theta, not on the family or its time interval. G'(0) nonzero is not needed; the result covers it as a special case.

## Boundary and residual questions

The audit establishes the originally requested smooth real-input composition inequality, including its input-norm-squared factor. It does not assert that the Einstein–Maxwell application has independently been proved here. Exact minimal regularity of G and optimal exponential growth in the low-regularity range are additional questions, not residual gaps in the original smooth-G question. Ancillary lower-bound results in Sections 7–9 were not required for, and are not certified by, this acceptance.

Ordinary complex-valued inputs cannot be silently substituted in the real-input exponential argument: unimodularity is essential. The manuscript separately handles smooth functions of real and imaginary parts by a multivariable Fourier representation; this is not an unstated requirement of the original target. Its real sine/cosine product-basis comparison uses blocks of at most four coefficients and is valid with its stated factor; arbitrary unitary rotations within full eigenspaces are not automatically equivalent for this envelope norm.

## Source identification and integrity

Original source: Chrusciel, Quo Vadis, Mathematical GR?, OWR 18 (2021), section 3.3, equations (10)–(11), https://doi.org/10.4171/OWR/2021/40 and https://arxiv.org/abs/2112.02126 . Original preprint wording explicitly includes the homogeneous factor and the coefficientwise time supremum.

Prior solution: Alper Ferudun, A Composition Estimate for Fourier Series with the Supremum in Time Inside the Sum, and a Question of Chrusciel, October 9, 2026, https://eulersolve.org/papers/owr-8415343-001/ . Its unrefereed status must be preserved.

The three inspected PDF hashes and sizes were independently recomputed:
- Claim manuscript: 269262 bytes; SHA-256 0dd8169c738142b17b1cf151f39d79b94ffa74522b74ebc487d47f831ee7c555.
- Original arXiv source: 138766 bytes; SHA-256 70efa259dbb75a5a568d508101cfccb78cc91f78d91c3e0da9ef2d766083d4bd.
- Publisher report: 1295115 bytes; SHA-256 6f260196006d0b22157e91804245d560b5f5e255a1ca1581556376e6682d4742.

No claimant verification report was used as evidence that the proof is correct; the acceptance above rests on re-deriving the mathematical dependency chain from the manuscript and comparing the original question.
