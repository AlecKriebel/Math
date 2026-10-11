# Independent challenge audit: Gaussian-zero moderate-deviation bounds

Date: 2026-10-11 UTC. Problem: 30000964 / OWR-1970-002.

## Verdict and exact accepted scope

**ACCEPT the non-sharp two-sided theorem (A) in the pinned proof below. No mathematical correction is required for that theorem. The sharp requested rate remains unresolved by this packet.**

The accepted statement is for a fixed real-valued h in C_c^2(C), with H=||Delta h||_2>0, and every positive sequence c=c(r) satisfying c→infinity and c/r→0:

\[
-\frac{\zeta(3)}2\leq
\liminf\frac{\log P(Y_r>c)}{c^2}\leq
\limsup\frac{\log P(Y_r>c)}{c^2}\leq
-\frac{3\zeta(3)}{\pi^2},
\qquad
Y_r=\frac{rZ_0(h_r)}{\frac14\sqrt{\zeta(3)/\pi}\,H}.
\]

Replacing h by -h gives the same conclusions for P(Y_r<-c). Acceptance does not assert a rate-function limit, the sharp value -1/2, a counterexample, novelty, a uniform theorem for r-dependent test functions, or a current literature-wide open-status claim. The proof is an authored deduction using established Gaussian inequalities; it is not a theorem imported wholesale from the cited sources.

Audited original proof before editorial redaction: 16,841 bytes, SHA-256 `a6eb5388d2aeadfdc804e3eddef0a5bc9a84529e9cd6ea0227eea7c1e00ee0f5`.

The complete frozen proof was read after receipt of that pin. The proof bytes were independently checked before and after the review. The sections below reconstruct the sensitive steps rather than accepting the creator's conclusion or numerical evidence.

## Primary-source and scope checks

- Chen, Dafnis and Paouris, [arXiv:1306.2410v2](https://arxiv.org/abs/1306.2410v2), Theorem 1(i), printed pp. 1–2: both statement pages were rendered and visually inspected, alongside extracted text. The theorem permits nonnegative measurable block functions under the covariance domination condition. It does not require independence, positive correlations, or a nonsingular full joint covariance. Its general diagonal blocks specialize to identity blocks here. This review relies on the established theorem, not a new audit of its entire proof.
- Nazarov and Sodin, [arXiv:1003.4251v1](https://arxiv.org/abs/1003.4251v1), Lemmas 2.1–2.2, printed pp. 5–6: the log-covariance identity and its short chaos derivation were read; p. 6 was rendered and visually inspected. The conjugation in the correlation coefficient was checked in the page image. The present field is jointly proper complex Gaussian, as required for the identity used here.
- [Official Oberwolfach report](https://ems.press/journals/owr/articles/1970), printed p. 1368: text and page image were inspected. The first question has lower endpoint r/(log r)^2, not (log r)^2. The separate question concerning general stationary fields is outside this audit.
- Tsirelson [Part IV, arXiv:1810.05673v2](https://arxiv.org/abs/1810.05673v2), Theorem 1.5 and Corollary 1.6: the restrictions were read in extracted text; the corollary page was also visually inspected. Tsirelson [Part V, arXiv:1909.03238v2](https://arxiv.org/abs/1909.03238v2), p. 3, equations (1.5)–(1.6), was read in text and image. These retain c(log r)^2/r→0 in dimension two. In particular c=r/log r is outside their quoted range, even though it belongs to the requested new range.

These are exact-version applicability checks. This reviewer did not reproduce the creator's entire modern-literature search, audit every proof in the cited papers, or inspect the full source corpus. The accompanying manifest records PDF byte pins and exact inspection limits.

## 1. Normalization and covariance constants

Let w=Delta h, G(z)=exp(-|z|^2/2)F(z), and X(z)=log|G(z)|+gamma/2. At each point |G(z)|^2 has the exponential distribution of mean one. Therefore X has mean zero, finite absolute moments of every fixed order, and variance zeta(2)/4=pi^2/24.

The distributional zero identity is Delta log|F|=2pi times the zero-counting measure. Since Delta(|z|^2/2)=2, integration against h(z/r) and two integrations by parts give

\[
Z_0(h_r)=\frac{1}{2\pi r^2}\int w(z/r)X(z)\,dA(z).
\]

The added gamma/2 makes no change because the integral of Delta h is zero. This is valid for compactly supported C^2 tests, by the distributional identity and approximation; logarithmic zero singularities are locally integrable. Fubini also gives finite absolute expectation of the weighted log integral.

Set S_r=integral w(z/r)X(z)dA(z). The stated normalization is Y_r=S_r/(ar), with a=2pi sigma H=(sqrt(pi zeta(3))/2)H, so a^2=pi zeta(3)H^2/4.

For the normalized coherent vectors the squared correlation is exp(-|z-y|^2). Applying the log-covariance identity and integrating its nonnegative series gives

\[
\int_{\mathbb C}\operatorname{Cov}(X(0),X(u))\,dA(u)
=\frac14\sum_{m\ge1}\frac{1}{m^2}\frac\pi m
=\frac{\pi\zeta(3)}4.
\]

The covariance kernel is integrable. After scaling one coordinate, the inner product of w with its translate by u/r tends to H^2 and is bounded in absolute value by H^2. Dominated convergence therefore gives Var(S_r)/r^2→a^2, with no assumption that w is nonnegative. All factors of pi, r, and two agree.

## 2. The tight frame and complex-to-real conversion

The monomial realization of k_z has unit norm. Direct Gaussian monomial integration gives the weak frame identity

\[
\int |k_z\rangle\langle k_z|\,dA(z)=\pi I.
\]

This is an identity on the coefficient Hilbert space, not the invalid assertion that an infinite vector of independent standard Gaussians is itself Hilbert-space valued. The field is represented by the isonormal process W(k_z).

For unit vectors u_i and positive b_i, put Ue_i=sqrt(b_i)u_i. The frame bound UU*≤pi I is equivalent to U*U≤pi I. Writing R_ij=E eta_i conjugate(eta_j), this says B^(1/2)RB^(1/2)≤pi I, hence R≤pi B^(-1).

For a proper complex Gaussian vector, form real blocks xi_i=sqrt(2)(Re eta_i,Im eta_i). Each diagonal covariance block is I_2. Up to a harmless coordinate ordering/conjugation convention, their covariance is the realification of R, with off-diagonal blocks

\[
\begin{pmatrix}\Re R_{ij}&-\Im R_{ij}\\\Im R_{ij}&\Re R_{ij}\end{pmatrix}.
\]

Realification preserves positive-semidefinite order. The required real bound is consequently T≤diag((pi/b_i)I_2). **There is no extra factor two in the exponent pi/b_i.** Scaling to identity real covariance already accounts for the component variance 1/2. Negative or complex off-diagonal correlations cause no problem.

## 3. Continuum limit, signed weights, and logarithmic singularities

For a fixed compact rectangle D and a finite partition into cells Q_i, the Bochner averages bar(k_i) exist because k_z is norm-continuous. For every Hilbert vector f, scalar Cauchy–Schwarz on each cell gives

\[
\sum_i d_i|\langle f,\bar k_i\rangle|^2
\leq\int_D|\langle f,k_z\rangle|^2dA(z)
\leq\pi\|f\|^2.
\]

Thus b_i=d_i||bar(k_i)||^2 and u_i=bar(k_i)/||bar(k_i)|| satisfy precisely the preceding frame hypothesis. Zero averages can be omitted. At sufficiently fine mesh no cell average vanishes, because all have norms uniformly tending to one. In particular b_i/d_i→1 uniformly.

Uniform norm-continuity on D gives sup over z in Q_i of ||u_i-k_z||→0. Under the same isonormal coupling, eta_i=W(u_i) and G(z)=W(k_z) therefore approach one another uniformly in L^2. To pass through the logarithm, use the clipped function

\[
\ell_L(x)=\max(-L,\min(L,\log|x|)),\qquad \ell_L(0)=-L.
\]

It is bounded and continuous, indeed Lipschitz for each fixed L. The expectation of the clipped difference tends to zero uniformly as mesh tends to zero. The two unclipped tails have a common marginal complex-normal distribution, with a finite second log moment; their first-moment tail contributions tend to zero uniformly as L tends to infinity. Hence the log differences tend uniformly to zero in L^1. This handles zeros and near-zeros without assuming a samplewise Riemann integrability property for log|G|.

The L^1 difference between the discrete sum and integral can now be split into: the error b_i-d_i; the modulus-of-continuity error for v; and the log-evaluation error just proved. Each tends to zero, since D has finite area and v is continuous and bounded. Signed v and signed lambda change none of these estimates.

For p_i=pi/b_i, the block function is the nonnegative measurable exponential of lambda b_i v(z_i)X_i. Its p_i-th moment is finite exactly when pi lambda v(z_i)>-2. The stated symmetric condition pi|lambda|||v||_infinity<2 is sufficient for all cells and both signs. Applying Gaussian Hölder yields the author's discrete bound.

From L^1 convergence choose an almost surely converging subsequence. Fatou's lemma for the nonnegative exponentials has the required direction:

\[
E\exp(\lambda\int vX)\leq\liminf E\exp(\lambda\sum_i b_iv(z_i)X_i).
\]

**Uniform integrability of those exponentials is unnecessary.** The deterministic upper bounds converge by b_i/d_i→1 and Riemann integration, proving the continuum Laplace bound. The partition limit is performed for each fixed v and lambda; no uniform control over expanding D or over the later moving parameters is being presumed.

## 4. Upper-tail optimization and uniform remainder

For s near zero, the marginal log-MGF has expansion

\[
K(s)=\frac{\pi^2}{48}s^2+O(|s|^3).
\]

The continuum bound then gives

\[
\log Ee^{\lambda S_r}\leq\frac{\pi^3}{48}\lambda^2r^2H^2
+C_h|\lambda|^3r^2.
\]

The cubic estimate is uniform for lambda in a sufficiently small interval depending only on fixed h. With lambda=kappa c/(ar), its contribution divided by c^2 is O_h(c/r), tending to zero for the entire asserted range. The quadratic coefficient is beta kappa^2/2, where beta=pi^2/(6zeta(3)). Chernoff gives -kappa+beta kappa^2/2; minimizing at kappa=1/beta yields -3zeta(3)/pi^2. No logarithmic restriction has entered this argument.

## 5. Signed trace-class operator and a genuine infinite-dimensional tilt

For fixed r, the rank-one operator integral defining A_r is a Bochner integral in trace class: the trace norm of each projector is one, and the weight has finite absolute integral. Thus A_r is self-adjoint, ||A_r||_1≤r^2||w||_1, and the frame identity gives -M I≤A_r≤M I, where M=pi||w||_infinity.

Trace-class Fubini gives the stated double-integral formula for D_r=Tr A_r^2. More explicitly,

\[
\frac{D_r}{r^2}=\int e^{-|u|^2}\langle w,w(\cdot+u/r)\rangle_{L^2}\,dA(u)
\longrightarrow\pi H^2.
\]

The inner product may change sign at finite r, but its absolute value is bounded by H^2, and D_r itself is nonnegative by its trace-square representation. Hence no false positivity assumption about w is used. D_r is strictly positive for all sufficiently large r.

Here is a full justification of the measure change, including the implicit joint representation. Diagonalize A_r on the Hilbert space, with eigenvalues alpha_j and isonormal coordinates eta_j=W(e_j). The map from a self-adjoint trace-class operator B to its centered Gaussian quadratic form is continuous into L^1, with norm bound at most 2||B||_1. Applying that map to the integral representation and to the spectral approximations of A_r proves, on the same Gaussian probability space,

\[
Q_r=\sum_j\alpha_j(|\eta_j|^2-1)
\quad\text{in }L^1.
\]

This is a joint construction with the field, stronger than a bare equality in distribution. Absolute eigenvalue summability also gives almost sure absolute convergence of the series. For |t|M<1, choose p>1 with p|t|M<1. Finite partial sums Q_N satisfy

\[
\log Ee^{ptQ_N}=\sum_{j\leq N}[-pt\alpha_j-\log(1-pt\alpha_j)].
\]

The sum is uniformly bounded in N, since each summand is bounded by a constant times alpha_j^2 on that fixed parameter interval. Thus e^{tQ_N} is uniformly integrable. Taking the limit proves the determinant normalization and convergent trace expansion, not merely a formal product expression.

Finite-coordinate tilted characteristic functions factor in the eigenbasis, showing independent proper complex coordinates with variances (1-t alpha_j)^(-1). Kernel coordinates remain unchanged. The finite densities converge in L^1, so these characteristic functions identify the full tilted isonormal process with covariance C_t=(I-tA_r)^(-1). Its law is centered and proper; no random vector in ell^2 is asserted. Absolute continuity also preserves the original almost sure entire-function version.

The covariance has **I-tA_r**, not I-2tA_r, because a standard proper complex coordinate has density pi^(-1)exp(-|z|^2). Equivalently, the quadratic form in identity-variance real coordinates carries the factor 1/2. For |t|M≤1/2 the covariance spectrum lies in [2/3,2], exactly as claimed.

## 6. Tilted mean, variance, and entropy

Resolvent expansion gives C_t=I+tA_r+R_t with ||R_t||≤2t^2M^2 for |t|M≤1/2. A scalar logarithm Taylor estimate on the resulting compact positive variance interval gives

\[
\log\langle C_tk_z,k_z\rangle
=t\langle A_rk_z,k_z\rangle+O_h(t^2),
\]

uniformly in z and r. Scaling each marginal complex Gaussian gives E_t X(z)=(1/2)log v_t(z). Integrating against w(z/r), and using absolute integrability for the error and trace-class Fubini for the linear term, yields E_t S_r=tD_r/2+O_h(t^2r^2). This computation is valid for signed w.

For the tilted normalized pair, its squared correlation is |K_t(z,y)|^2/(v_t(z)v_t(y)) in [0,1]. The exact log-covariance series implies

\[
|\operatorname{Cov}_t(X(z),X(y))|
\leq \frac{\zeta(2)}{4}\frac{|K_t(z,y)|^2}{v_t(z)v_t(y)}
\leq\zeta(2)|K_t(z,y)|^2.
\]

The proof uses the weaker valid lower bound v_t≥1/2. Applying the original frame identity to C_tk_z gives integral |K_t(z,y)|^2dA(y)=pi||C_tk_z||^2≤4pi. Absolute values on both weight factors and one compact support restriction then give the stated uniform Var_t S_r=O_h(r^2). Fubini is justified first by the finite area and uniformly bounded log second moments. This proves concentration without claiming spatial mixing or stationarity of the tilted field.

For m≥2, the spectral bound |Tr A_r^m|≤M^(m-2)D_r justifies differentiation of the log-MGF locally. Therefore

\[
H(P_t\mid P)=tL'_r(t)-L_r(t)
=\sum_{m\ge2}\frac{m-1}{m}t^m\operatorname{Tr}A_r^m
=\frac{t^2D_r}{2}+O_h(|t|^3D_r).
\]

As an independent factor check, the relative entropy of one tilted proper complex coordinate is v-1-log v, with v=(1-t alpha)^(-1). Its expansion starts at t^2alpha^2/2, agreeing with the formula above. Negative eigenvalues do not change the validity or nonnegativity of total entropy.

## 7. Lower-tail transfer and every moving-parameter error

Fix epsilon>0; put b_r=arc and t_r=2(1+epsilon)b_r/D_r. Then t_r=O_h(c/r)→0, so every preceding covariance and entropy bound eventually applies. The linear part of the mean is exactly (1+epsilon)b_r. Its remainder relative to b_r is

\[
O_h(t_r^2r^2/b_r)=O_h(c/r)=o(1).
\]

Consequently the tilted mean exceeds b_r by at least epsilon b_r/2 for large r. The variance bound and Chebyshev imply P_t(S_r>b_r)=1-O_{h,epsilon}(c^(-2))→1. This covers arbitrarily slowly growing c and the strict inequality threshold.

Coarse-graining relative entropy to E_r={S_r>b_r} gives

\[
H(P_t\mid P)\geq p_r\log(1/q_r)-\log2,
\quad p_r=P_t(E_r),\quad q_r=P(E_r).
\]

Its rearrangement is log q_r≥-(H+log2)/p_r. Since p_r→1, c^2→infinity, and the entropy remainder divided by c^2 is O_h(c/r), the limit lower bound is

\[
-\frac{2(1+\epsilon)^2a^2}{\pi H^2}
=-\frac{\zeta(3)}2(1+\epsilon)^2.
\]

Taking epsilon down to zero only after the liminf is legitimate. There is no hidden need for a rate in D_r/r^2→pi H^2, no need for c to dominate log r, and no interchange of the epsilon and r limits.

## 8. Limits of acceptance and independent finite controls

The constants are approximately -0.601028451579797 and -0.3653814847007192, leaving a genuine gap containing -1/2. The upper proof pays the variance factor pi^2/(6zeta(3)); the lower proof shifts the statistic through only its first nonconstant Gaussian chaos. Neither proof supplies the missing sharp moving-parameter log-MGF estimate. Fixed-order cumulants, fixed-c convergence, or small pointwise correlations do not provide that estimate by themselves.

A separately written finite numerical check was also performed. It checks the two constants and Chernoff optimization, realification spectra and frame domination for a genuinely complex finite Gram matrix, and a signed radial example h(z)=(1-|z|^2)_+^3. For that C_c^2 test, w(s)=-12+48s-36s^2 on [0,1], integral w=0, and H^2=96pi/5. In the monomial basis the operator is exactly diagonal, permitting an independent finite-radius check of trace, norm signs, trace-square scaling, and the entropy factor for both tilt signs.

Final controls pass at r=2,4,8,16,32,64. The trace-square ratios increase from 0.303377 to 0.998212. The initial smoke test used an unjustified numerical threshold 0.996 at r=32, where the actual ratio is 0.993020; the tested range was extended to r=64 rather than treating that arbitrary threshold as a theorem. This was a numerical-test expectation error, not a counterexample or proof failure. No Monte Carlo tail result or machine-checked proof claim is made.

## 9. Scope of this audit

This audit is mathematical acceptance of the exact partial theorem, not resolution of the original sharp problem. The published proof and audit differ from their reviewed originals only by nonmathematical editorial redactions; their byte identities are recorded in EDITORIAL_METADATA.json.
