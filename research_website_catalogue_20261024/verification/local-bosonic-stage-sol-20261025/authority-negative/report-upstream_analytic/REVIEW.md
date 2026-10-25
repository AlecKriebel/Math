# Complete independent analytic audit of the pinned EPnI dependency

**Status: COMPLETE. Verdict: PASS for the full pinned finite-energy EPnI theorem, and therefore for the exact finite-block vacuum-environment inequality needed by Zenodo 23203100.**

I found no substantive mathematical fault or unresolved central proof gap after reading and independently reconstructing the complete 32-page source, including every central argument in Sections 3–6. This is an analytic dependency clearance, not an inference from a theorem label, a favorable prior review, numerical samples, or a claimed formal build. The downstream capacity proofs of Zenodo 23203100 are outside this assignment; clearing their EPnI premise does not independently audit those other arguments.

## 1. Source, scope, independence, and success criteria

The audited source is OpenAI, *The entropy photon-number inequality*, September 24, 2026, 32 pages, at the exact Git commit

`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

Official pinned source:

<https://raw.githubusercontent.com/openai/math/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-entropy-photon-number-inequality-September-24-2026/paper.pdf>

The locally audited PDF is `papers/23203100/sources/primary/.cache/openai-epni-pinned.pdf`, SHA-256

`d826f8ebe18596419871100e79611868dff2a45a4aa157433c58e6f49a234d82`.

I verified that hash and the 32-page count. I independently extracted the PDF with `pdftotext -layout`; the result is byte-for-byte identical to the supplied 1,807-line text, SHA-256

`cee103be8f23d7ba1737dee0bd21d6048c338f40b4e802ce6010c244f57d94a9`.

I read all 1,807 lines, including the introductory statements, the full proofs in Sections 2–6, the Section 7 broadcast interface, and references. I also visually inspected complete PDF pages 21–25 to verify complex conjugations, signs, dissipator parentheses, and the final cancellation against the rendered equations. In particular the means in the weak-convolution correction are complex conjugated, as they must be; text extraction alone does not expose the bars reliably.

I read the complete original Guha–Erkmen–Shapiro EPnI note, arXiv:0710.5666v2, three pages/217 extracted lines, to check the original product-port hypothesis and vacuum-port interface. Its Section II.B explicitly permits arbitrary states within each group, requires only a product between the two groups, and defines the same entropy photon number. Its Minimum Output Entropy Conjecture 2 has the required vacuum-port interpretation.

No other current or historical review report, opposing-family report, favorable acceptance wrapper, or formal-verification summary was read as evidence. No children were spawned. No external person was contacted and no outreach was prepared. No paper source, repository branch, Git state, release, website, spreadsheet, or deployment was changed. All authored artifacts are in this audit folder.

**Exact target VE.** For every finite integer (n\geq1), every (n\)-mode state (\rho) with finite total mean photon number, every (t\in[0,1]), and a fresh independent (n\)-mode vacuum environment,

\[
\frac1n S\bigl(\mathcal L_t^{\otimes n}(\rho)\bigr)
\geq g\!\left(t g^{-1}\!\left(\frac{S(\rho)}n\right)\right),
\qquad g(r)=(r+1)\log(r+1)-r\log r.
\]

Internal entanglement among the modes of (\rho) is allowed. The conclusion must not be restricted to Gaussian, diagonal, passive, separable, or product inputs, and must include arbitrary finite energy rather than a hidden fourth-moment condition. The success criterion was a substantive validation of the actual upstream proof of this claim or of its stronger two-input theorem; merely reciting Theorem 1.1 or substituting an unproved equivalent inequality was insufficient.

The audited proof establishes the stronger two-input Theorem 1.1. The exact remaining central gap for this dependency is **none identified**. This assessment does not assert machine-checked formal verification; no Lean build or installation was attempted.

## 2. Proof mechanism and where its burden is discharged

| Family/mechanism | Actual mathematical content checked | Status / exact gap |
|---|---|---|
| Scalar and operator interpolation, pp. 8–13 | Parallel sums, two logarithmic-mean operations, a holomorphic inverse construction, a Stieltjes representation, and an exact scalar minimization | Verified analytically; no central gap identified |
| Regularized minimization, pp. 14–17 | Negative witness, compactness/coercivity, Gibbs majorant, fourth-to-seventh-moment regularity | Verified analytically; no central gap identified |
| Local entropy Hessian, pp. 17–19 | Finite-eigenblock variation and Gibbs variational duality; exact factors of (h_i,w_i,\lambda_i,1-\kappa) | Verified analytically; no universal channel contraction is assumed |
| Product-port variance and weak convolution, pp. 19–23 | Orthogonal conditional-expectation subspaces; noncommutative weak commutators; replacement correction and mean control | Verified analytically; within-port entanglement is retained |
| Stationarity and limit, pp. 23–26 | Weighted trace-class covariance; exact entropy-production identity; energy cancellation; finite-test identification of thermal limits | Verified analytically; no input-energy convergence or semigroup entropy derivative is assumed |
| Finite reproducibility controls | Matrix-map interpolation; scalar singular cases; internally entangled multimode convolution/covariance; finite-Fock CCR boundary correction | All passed; controls only, not a proof for arbitrary states |

The potential circularity is specifically avoided at two points. The key interpolation lemma is proved through complex function theory and parallel sums without using an entropy inequality. The Hessian comparison is derived only at actual regularized minimizers of a hypothetical negative functional. It is not introduced as an unsupported universal channel statement. Consequently the proof does not move EPnI into an equivalent conjectural optimizer lemma.

## 3. Compactness, negative witness, and Gibbs regularity

### 3.1 Finite-energy boundary and the regularization order

Lemma 2.2, pp. 6–7, supplies compactness of the fixed oscillator-energy sublevel and entropy continuity on that sublevel. The tail estimate is sufficient: if (q\) is the probability outside a number cutoff, then (q\leq E/(K+1)), and the high-sector entropy contribution is at most (qn g(E/(qn))\to0). The two-block pinching cost is at most the binary entropy. Finite-dimensional compression then gives the required continuity. This is a finite-mode oscillator fact; it would not follow for an arbitrary Hamiltonian without a suitable partition-function bound, but here the number-sector degeneracy grows polynomially.

A hypothetical strictly violating finite-energy pair can therefore be replaced by normalized finite-number cutoffs, with both input and output entropies converging and a strict violation surviving. Passive total-number preservation gives the common output energy bound needed in this reduction. If both input entropies were zero the claimed right side would be zero, so a strict witness necessarily has at least one positive entropy photon number.

Section 4.1 fixes positive thermal references (r_i\) near the witness entropy photon numbers, adds an independent thermal port of small weight (\lambda_D>0), then chooses (\varepsilon>0\) to preserve negativity and the two strict slack inequalities (4.2), then a small replacement fraction (\kappa>0), and finally (\zeta>0). This order works even when one witness entropy is zero, since (g(r)/h(r)\to0) as (r\downarrow0), with (h(r)=\log(1+1/r)>0). The third port provides positive slack for both (r_i) and (r_i+1). The additional upper bound on (\kappa) in Proposition 5.4 depends only on previously fixed parameters. All these parameters remain fixed while (\zeta\downarrow0).

The objective is

\[
J_\zeta=\frac{S(\rho_0)-ng(r_0)}{h_0}
-\sum_i w_i\frac{S(\rho_i)-ng(r_i)}{h_i}
+\varepsilon\sum_i\frac{w_i}{h_i}D(\rho_i\Vert\tau_{r_i})
+\zeta\sum_i\operatorname{Tr}\rho_iW_i^4,
\]

where (w_i=(1-\kappa)\lambda_i), (r_0=\sum_{s=1,2,D}\lambda_s r_s), and (\rho_0=(1-\kappa)\gamma+\kappa\tau_{r_0}). The fixed witness makes every sufficiently small-(\zeta) minimum at most a common negative constant.

### 3.2 Actual attainment and the logarithm identity

Expanding thermal relative entropy gives the variable terms

\[
\frac{S(\rho_0)}{h_0}
-\sum_i\frac{(1+\varepsilon)w_i}{h_i}S(\rho_i)
+\varepsilon\sum_iw_i E_i
+\zeta\sum_i\operatorname{Tr}\rho_iW_i^4.
\]

The positive linear energy terms dominate the logarithmic entropy growth for each fixed finite (n). Thus upper sublevels have input energy bounds uniform in (\zeta), and fourth-moment bounds for fixed positive (\zeta). Entropy continuity, trace-norm continuity of product/channel maps, and lower semicontinuity of the two positive penalties give attainment. The sign of the output entropy term is favorable for coercivity.

The replacement guarantees (\rho_0\geq\kappa\tau_{r_0}). The logarithm resolvent order gives (0\leq H_0=-\log\rho_0\leq CW_0) as forms. Slicing through the passive unitary with the other inputs fixed consequently gives (0\leq T_iH_0\leq C_iW_i).

At a minimum, replace only the output entropy by its cross entropy against the fixed (H_0). Relative-entropy nonnegativity makes this a majorant tangent at the minimum. It is still minimized by the chosen input. Dividing by the positive input entropy coefficient identifies that input uniquely as the Gibbs state of

\[
K_i=\frac{h_i}{(1+\varepsilon)w_i}
\left(\frac{1-\kappa}{h_0}T_iH_0+\varepsilon w_iN_i+\zeta W_i^4\right).
\]

This is an exact variational majorization argument, so it does not assume differentiability of entropy at an infinite-dimensional boundary. Its consequence is the exact identity (4.4):

\[
\frac{(1+\varepsilon)w_i}{h_i}H_i
=\frac{1-\kappa}{h_0}T_iH_0+\varepsilon w_iN_i+\zeta W_i^4+c_iI.
\]

### 3.3 The fourth-to-seventh-moment argument really closes

Lemma 4.1 is needed because a mere fourth-moment penalty would not by itself justify all subsequent unbounded traces. For a form (K=kW^4+W^{1/2}BW^{1/2}), with (B\) bounded positive and (k>0), let

\[
C=kI+W^{-3/2}BW^{-3/2},\qquad U=W^{-2}C^{-1}W^{-2}.
\]

Then (U\) is compact, positive and injective, and the closed form with domain (D(W^2)) corresponds to (K=U^{-1}). Inverse comparison (U\leq k^{-1}W^{-4}) gives polynomial counting of the eigenvalues (u_j\) of (K); no invalid operator monotonicity of the exponential is used.

The form eigenvalue equation, in number coordinates and after multiplying by (W^{-1/2}), gives

\[
kW^{7/2}\psi_j=u_jW^{-1/2}\psi_j-BW^{1/2}\psi_j.
\]

The right side is square summable. Also (\|W^2\psi_j\|^2\leq u_j/k), so (\|W^{7/2}\psi_j\|\) is polynomially bounded in (u_j). Exponential Gibbs weights and polynomial eigenvalue counting then imply (\operatorname{Tr}\rho W^7<\infty). The bound need not be uniform as (\zeta\to0), and the later limit does not require it to be uniform. Total-number preservation supplies the same seventh-moment property for the output. This is the necessary regularity upgrade, not an assumption.

## 4. Entropy-Hessian duality and all scale factors

Work at one minimum. Write (\rho_s=\operatorname{diag}(p_{s,l})), with (p_{s,l}>0), and define

\[
\|Z\|_s^2=\sum_{l,r}h_s\ell(p_{s,l},p_{s,r})|Z_{lr}|^2,
\qquad v_s(l,r)=\frac{\log(p_{s,l}/p_{s,r})}{h_s}.
\]

The centering projection subtracts (\operatorname{Tr}\rho_sZ\). Centered finite eigenblocks, including their constant identity tails, are dense. Frequency multipliers preserve them because every diagonal coordinate has frequency zero.

The Gibbs identity makes the one-input objective difference exactly

\[
J_\zeta(\widetilde\rho_i)-J_\zeta(\rho_i)
=\frac{(1+\varepsilon)w_i}{h_i}D(\widetilde\rho_i\Vert\rho_i)
-\frac1{h_0}D(\widetilde\rho_0\Vert\rho_0)\geq0.
\]

For a traceless Hermitian finite input eigenblock (A), the two-sided perturbation (\rho_i+tA\) is admissible: its selected eigenvectors have finite seventh moment. Its relative entropy is (t^2Q_i(A)/2+o(t^2)), where (Q_i(A)=\sum|A_{lr}|^2/\ell(p_l,p_r)).

For a centered finite output test (Z), the Gibbs variational lower bound with exponential (\exp(\log\rho_0+tZ)) is legitimate. It changes a finite eigenblock and multiplies the remaining block by a scalar. Its log partition function has second derivative (\|Z\|_0^2/h_0), so comparison gives (4.12), with

\[
\alpha=\frac{(1+\varepsilon)w_ih_0}{h_i}:
\quad 2(1-\kappa)\operatorname{Tr}AT_iZ-\alpha Q_i(A)
\leq\frac{\|Z\|_0^2}{h_0}.
\]

Taking the constrained dual over trace-zero (A) yields

\[
(1-\kappa)^2\|T_iZ-\langle T_iZ\rangle_iI\|_i^2
\leq(1+\varepsilon)w_i\|Z\|_0^2.
\]

The trace constraint is continuous in (Q_i), and finite-eigenblock truncation followed by a trace correction is dense. With (L_iZ=(T_iZ-\langle T_iZ\rangle_iI)/\sqrt{\lambda_i}), this is precisely

\[
\|L_iZ\|_i^2\leq\frac{1+\varepsilon}{1-\kappa}\|Z\|_0^2.
\]

I checked the factors explicitly. There is no missing (\lambda_i), no interchange of a joint and a component Hessian, and no need for a bounded inverse of the full density operator. Extension to actual bounded slices follows from complete positivity, Schwarz, the arithmetic-norm approximation, and (\rho_0\geq(1-\kappa)\gamma).

## 5. The analytic interpolation burden is proved, not assumed

### 5.1 Comparison-preserving operations

For a diagonal family (X), comparison means (Q_{X,0}(Z)\geq\sum_iw_iQ_{X,i}(L_iZ)). Positive sums preserve it. Pointwise limits preserve it because a source test uses finitely many parameter tuples, while target sums use Fatou. Parallel sum preserves it by minimizing (X|u|^2+Y|v|^2) over (u+v=z), applying the two comparisons to the source minimizers, and minimizing separately on each target coordinate. Source minimizers remain in the test space by multiplier invariance. No compatibility between the maps and diagonal multipliers is smuggled in.

The two integral identities in (3.6) construct both (\ell(X,Y)) and (XY/\ell(X,Y)) from positive sums and parallel sums. Applying them to (mf(x)e^{\pm x}) and to (mf(y)e^{\pm y}), where (f(x)=x/\sinh x), gives the three known weights (m,ms,mt), (s=f(x)^2,t=f(y)^2). There is no unsupported multiplication-of-weights rule.

### 5.2 Holomorphic inverse and Stieltjes representation

The difficult step is Lemma 3.2, pp. 10–12. For real (x\geq0), (B(f(x)^2)=x\coth x). The source establishes its analytic extension using

\[
s=(u/\sin u)^2,\qquad B(s)=u\cot u.
\]

For (u=p+iq), (q>0), choose the connected domain (0<p<p_*(q)\), with (p_*\tan p_*=-q\tanh q). The map (a(u)=\sin u/u) maps this domain into the fourth quadrant. Both component signs were checked directly: for (p<\pi/2), (\tan p/p>1>\tanh q/q) gives the imaginary sign; the curved boundary equation gives the real sign. Its finite boundary maps to the coordinate axes, its corners to 1 and 0, and 

\[
|a(p+iq)|\geq \frac{\sinh q}{\sqrt{\pi^2+q^2}}\to\infty
\]

uniformly as (q\to\infty). It is therefore proper into that quadrant. It has no critical point because

\[
\operatorname{Im}(u\cot u)
=\frac{q\sin(2p)-p\sinh(2q)}{\cosh(2q)-\cos(2p)}<0,
\]

while (a'(u)=0\) would require (u\cot u=1). Properness and the inverse function theorem make it a covering; connectedness and the simply connected target make it one-sheeted. This is a valid global inverse mechanism, not an unjustified local inversion continued past branch points.

Taking (u=a^{-1}(s^{-1/2})\) gives (\operatorname{Im}B<0) in the upper half-plane. The boundary parametrizations (u=iq) for (0<s<1) and (u=p\in(0,\pi)) for (s>1) identify its real continuation. The (u^2) expansion at (s=1) gives (B(1)=1,B'(1)=-1).

I also checked the two Herglotz conversions. With the representing measure supported on the nonpositive axis,

\[
G(s)=\frac{B(s)-1}{1-s}
=\beta+\int_{(-\infty,0]}\frac{d\mu(r)}{(1-r)(s-r)}.
\]

Then (H=sG) has nonnegative imaginary part, since (\operatorname{Im}(s/(s-r))\geq0) for (r\leq0). It has no zero in the upper half-plane by the harmonic minimum principle and its positive real-axis values. Thus (R=1/(sG)) is positive on (s>0) and maps the upper half-plane to the lower. Applying the representation again, positivity as (s\to\infty) eliminates the linear term and supplies an integrable Stieltjes measure. Finally direct differentiation on (0<s<1) gives

\[
-B'(s)=\tfrac12\bigl(1/s+R(s)\bigr),
\]

and analytic continuation extends it. The (1/(2s)) term guarantees strict positivity. These steps prove the required Stieltjes property of the derivative; merely knowing that (-B) is Pick would not alone have sufficed, and the paper does not make that shortcut.

### 5.3 Final scalar minimization, including singular cases

The extra weight is defined by

\[
E^{-1}=\frac2m\int_0^1[-B'(\theta s+(1-\theta)t)]\,d\theta.
\]

Its Stieltjes representation builds it from inversions of positive sums of (m,ms,mt), so comparison is preserved. The scalar quadratic in (3.18), after expansion, is

\[
Q(\xi,\phi)=\frac{ma}{2}|\xi|^2
+m\left(\frac a2+e\right)|\phi|^2
-m(x-y)\operatorname{Re}(\xi\overline\phi),
\quad a=b(x)+b(y),\ e=E/m.
\]

Its minimum is (\frac m2[a-(x-y)^2/(a+2e)]|\xi|^2), equal to

\[
m\frac{f(x)f(y)}{f(x+y)}|\xi|^2.
\]

The calculation uses (b(z)^2=f(z)^2+z^2) and the hyperbolic addition formula. The paper separately treats (x=y), (x=-y\ne0), and (x=y=0); I checked those branches. They give respectively (mb(x)), (mf(x)^2), and (m), so no removable singularity is discarded. Applying the four comparisons to the source minimizing decomposition and then the target coordinatewise minima proves Theorem 3.1. This analytic burden is closed within the source.

## 6. Application of the interpolation and the weak quantum identity

The two arithmetic weights (R_{s,\pm}=\frac v2\coth(h_sv/2)\pm v/2) give the two orders (\operatorname{Tr}\rho ZZ^\dagger) and (\operatorname{Tr}\rho Z^\dagger Z). For the three independent input ports, centered one-port subspaces are mutually orthogonal in each arithmetic inner product. Their projections are the centered slices. This proves the sum-of-slice-variances inequality. It needs independence between ports, and makes no statement of independence between modes within a port.

The component Hessian estimate and the two scalar slack inequalities (4.2) supply comparison for the constant weight families (r_s) and (r_s+1). Applying Theorem 3.1 with (m=1/h_s,x=h_sv/2,y=-h_s/2) therefore gives

\[
F_s(v)=\frac1{h_s}\frac{f(h_sv/2)f(-h_s/2)}{f(h_s(v-1)/2)}
=\frac{b_s(v)-(r_s+1/2)v}{1-v}.
\]

It is continuous, strictly positive, and bounded above and below by positive constants depending only on the fixed reference. Its limits at (+\infty,-\infty) are (r_s,r_s+1). The associated logarithmic mean is exactly (\ell(p_l,p_r)F_s(v)=\ell(r_sp_l,(r_s+1)p_r)). Centered test-space invariance holds despite the infinite identity tail, because all its diagonal entries have the same zero frequency. Ambient target spaces may be the full matrix spaces; target minimizers need not preserve centering.

Put (\mu_s=(\operatorname{Tr}\rho_sd_{s,j})_j), (d'_s=d_s-\mu_s I), and (e'_s=\operatorname{Tr}\rho_sN_s-|\mu_s|^2). The defects are

\[
q_{s,j}(Z)=(r_s+1)\operatorname{Tr}\rho_s(d'_{s,j})^\dagger Z
-r_s\operatorname{Tr}\rho_sZ(d'_{s,j})^\dagger.
\]

In the eigenbasis, set (K_{lr}=(r_s+1)p_r-r_sp_l). The coefficient identity

\[
\frac{K_{lr}}{h_s\ell(p_l,p_r)}=(1-v)F_s(v)
\]

makes the representing vector ((1-v)d'_{lr}), and gives

\[
\|q_s\|_{F_s,*}^2=\sum_{j,l,r}(1-v)K_{lr}|d'_{j,lr}|^2.
\]

All crossed and uncrossed logarithmic sums are absolutely summable: (H_s\leq CW_s^4), (d'\) shifts number by one, and the seventh moment controls the resulting fifth moments. For the uncrossed term one uses (\langle W^4\rangle\langle W\rangle\leq\langle W^5\rangle). Thus the dual norm identity is not just a formal divergent series.

For weak convolution, write the uncentered defect as a creation expectation plus (r_s) times a commutator expectation. Under rotation, (d_s^\dagger=\sqrt{\lambda_s}d_0^\dagger+\) discarded terms. Discarded commutators with a retained bounded observable have zero weak trace; the retained coefficient is (\sum_s\lambda_sr_s=r_0). Finite energy makes (d\rho,\rho d,d^\dagger\rho,\rho d^\dagger) trace class by Hilbert–Schmidt factorization. Cutting off the discarded annihilator in its own number basis justifies cyclicity and then trace-norm passage to the unbounded operator. No domain invariance of an arbitrary bounded test under (d^\dagger) is required.

The thermal port has zero defect. Direct centering of the replacement gives the exact additional term

\[
q_{0,j}(Z)=\sum_iw_iq_{i,j}(L_iZ)
+\kappa(1-\kappa)\overline{(\mu_\gamma)_j}
\operatorname{Tr}[(\gamma-\tau_{r_0})Z].
\]

This correction cannot be omitted for nonzero means. The between-branch variance bounds its scalar functional in both arithmetic metrics. The two-weight logarithmic-mean operation then bounds it in the base metric; the uniform lower bound on (F_0) converts this to the (F_0) metric. Hence, with (A_*^2=\sum_iw_i\|q_i\|_{F_i,*}^2), (M_*^2=\sum_iw_i|\mu_i|^2),

\[
\|q_0\|_{F_0,*}\leq A_*+\sqrt{2\kappa}\,C_0M_*.
\]

Young's inequality and (\kappa\leq\varepsilon^2/[4(\varepsilon+2)C_0^2]) give

\[
\|q_0\|_{F_0,*}^2\leq A_*^2+\tfrac\varepsilon2(A_*^2+M_*^2).
\]

The bound is uniform in the minimizing states and (\zeta), because its constants use only the fixed thermal references and (\varepsilon).

## 7. Weighted stationarity, exact cancellation, and identification of the limit

### 7.1 Unbounded generator pairings are justified

The generator is the trace-class expression

\[
\delta_s=\sum_j\bigl[(r_s+1)\mathcal D[d_{s,j}]\rho_s
+r_s\mathcal D[d_{s,j}^\dagger]\rho_s\bigr].
\]

Let (T=W^3\rho W^3). It is trace class. Each term of (W^2\delta W^2) is bounded factors around (T), for example

\[
W^2d\rho d^\dagger W^2=(W^2dW^{-3})T(W^{-3}d^\dagger W^2),
\quad W^2d^\dagger d\rho W^2=(d^\dagger dW^{-1})TW^{-1}.
\]

Number cutoffs converge in this weighted trace norm. Partial trace is continuous in the required weighted norms because ((W_0^k\otimes I)W_{\rm tot}^{-k}) is bounded with norm at most one. The rotation preserves total number. These observations upgrade the elementary finite-sector covariance to

\[
\delta_0=(1-\kappa)\sum_i\Phi_i(\delta_i),\qquad
\operatorname{Tr}\delta_0H_0=(1-\kappa)\sum_i\operatorname{Tr}\delta_iT_iH_0.
\]

The fixed thermal port and replacement thermal have zero generator. Slicing against unbounded (H_0) is justified by decomposing (W_i^2\delta_iW_i^2) into positive and negative trace-class parts and conjugating back; these give positive inputs with finite fourth moment. Since (W^{-2}H_sW^{-2}) is bounded, all claimed logarithmic traces have a precise form pairing.

Pairing the exact Gibbs identity with (\delta_i) is therefore legitimate and gives (6.4). It is algebraic stationarity, so the argument never assumes that (\rho_i+t\delta_i) is a positive two-sided perturbation, or differentiates entropy along an unbounded semigroup.

### 7.2 Entropy-production identity and the sign of every energy term

Set (\sigma_s=\operatorname{Tr}\delta_sH_s/h_s). Eigenbasis evaluation gives

\[
\sigma_s=-\sum_{j,l,r}vK_{lr}|d'_{j,lr}|^2.
\]

Subtracting from the norm formula leaves (\sum K_{lr}|d'_{j,lr}|^2=e'_s-nr_s), using the exact CCR. Thus

\[
\sigma_s=\|q_s\|_{F_s,*}^2-(e'_s-nr_s).
\]

The absolute logarithmic summability established above justifies the rearrangement. Centering changes only diagonal terms and they have (v=0).

The number drift is (\operatorname{Tr}\delta_iN_i=-(e'_i-nr_i)-|\mu_i|^2). The fourth-moment drift polynomial is

\[
P_i(N)=(r_i+1)N[N^4-(N+1)^4]
+r_i(N+n)[(N+2)^4-(N+1)^4].
\]

Its degree-five coefficients cancel and its degree-four coefficient is exactly (-4), independently of (r_i,n). It is consequently bounded above on the nonnegative integers, uniformly in the state and (\zeta).

Port independence gives (e'_\gamma=\sum_i\lambda_ie'_i+\lambda_Dnr_D). The two-branch mixture has the extra mean variance, so

\[
e'_0-nr_0=\sum_iw_i(e'_i-nr_i)
+\kappa(1-\kappa)|\mu_\gamma|^2.
\]

Substitute these identities into (6.4). The coefficient of each (w_i(e'_i-nr_i)) is exactly (-1+(1+\varepsilon)-\varepsilon=0). The resulting identity is

\[
0=\|q_0\|_{F_0,*}^2-(1+\varepsilon)A_*^2
-\varepsilon M_*^2-\kappa(1-\kappa)|\mu_\gamma|^2+\zeta P.
\]

The previous defect estimate and (P\leq C) give

\[
0\leq-\tfrac\varepsilon2(A_*^2+M_*^2)+C\zeta.
\]

Both input defect lists and both input means therefore tend to zero. This is the strict margin that would fail if the relative-entropy penalty, normalization, or mean correction were mishandled.

### 7.3 The limit is the full multimode thermal state

The energy bound uniform in (\zeta) gives trace-norm convergent input subsequences. For a fixed finite number-basis matrix (Z), its centered (F_i) norm is bounded uniformly in the minimizing state by a fixed constant times (\|Z\|). Defect convergence and mean convergence therefore give vanishing uncentered defects on these tests. Both (d_j^\dagger Z) and (Zd_j^\dagger) are bounded finite rank, so trace-norm convergence passes the identities to the limit without passing any unbounded first or second moments.

The limiting state satisfies, entrywise,

\[
(r_i+1)d_j\widehat\rho_i=r_i\widehat\rho_i d_j\quad\text{for every }j.
\]

For multi-indices (p,b), this gives the recurrence

\[
(r_i+1)\sqrt{p_j}\,\widehat\rho_{p,b}
=r_i\sqrt{b_j}\,\widehat\rho_{p-e_j,b-e_j}.
\]

If (p_j>b_j), iteration reaches a zero right side; if (p_j<b_j), use self-adjointness. Thus every off-diagonal matrix entry vanishes. Diagonal entries have ratio (r_i/(r_i+1)) in every coordinate, and trace one fixes the product geometric normalization. The limiting state is (\tau_{r_i}), including the absence of within-port correlations. This identifies the entire state, rather than only its marginals or first moments.

Continuity of the channel and thermal mixing identify the output limit as (\tau_{r_0}). Common energy bounds give convergence of all three entropies. The entropy portion of (J_\zeta) tends to zero, while both penalties are nonnegative. Consequently (\liminf J_\zeta\geq0) along this subsequence, contradicting the common strictly negative upper bound. The proof neither needs convergence of input energies nor disappearance of the penalties. Only (\zeta) tends to zero.

## 8. Adversarial checks and meaningful boundary cases

| Attempted failure mode | Check and outcome |
|---|---|
| The proof only treats faithful, finite-moment original inputs | False: those properties belong to auxiliary minima. The original witness is reduced by energy-bounded number cutoffs, preserving strict violation. |
| Product structure is imposed within an input port | No such step found. Orthogonality and energy identities use independence only between ports. Matrix recurrence identifies the eventual product thermal limit without assuming it. |
| Local inverse branches hide a global branch point in Lemma 3.2 | Properness, absence of critical points, and the one-sheeted covering argument supply the global inverse. |
| A Pick derivative is asserted Stieltjes without justification | The extra (G\mapsto sG\mapsto1/(sG)) construction and differential identity prove the specific derivative representation. |
| Multiplication of comparison weights is used illicitly | The needed weights are built by positive sums, parallel sums, and pointwise limits; the final product-looking expression is the scalar minimum. |
| Centering destroys frequency-multiplier invariance | Every diagonal entry has zero frequency, including the infinite identity tail. The centering condition is preserved. |
| One-input Hessians are incorrectly summed as a joint Hessian | They are used separately with scalar slack. Arithmetic variance supplies the summed comparisons independently. |
| Unbounded commutators are treated as bounded operators | The proof works with trace-class weak pairings, cutoffs, and finite-energy factorization. |
| Output replacement is treated as if it preserved centered convolution exactly | The nonzero mean correction is present and explicitly bounded. |
| A finite Fock truncation silently assumes the exact CCR | The analytic proof uses full Fock space. Our numerical controls explicitly include the finite boundary correction; see below. |
| Fourth moments are presumed to control every needed trace | Gibbs regularity upgrades each minimum to seventh moment, and weighted trace estimates are proved. |
| Stationarity assumes an inadmissible two-sided generator variation | It pairs an already proved exact Gibbs identity with a weighted trace-class expression; no such variation is used. |
| Vanishing centered defects permits arbitrary displaced thermal limits | The separate (M_*^2) term forces means to zero. |
| Trace convergence is used to pass energy or means | The proof passes only fixed finite number-basis tests; the means vanish by a separate quantitative estimate. |
| Zero input entropy or a vacuum environment is excluded by (r_i>0) | The positive references are auxiliary and may be chosen close to zero; the original inputs remain arbitrary. |
| (t=0,1) are missed by the interior proof | They are exact identities and treated separately. |
| Infinite mode number is silently allowed | The theorem and this clearance require every fixed finite (n). No infinite-mode statement is asserted. |

## 9. Reproducible controls and their limits

`verification.py` uses only NumPy and the standard library. The runtime path and results are recorded in `verification_results.json`. It does not search for or assume a positive answer and uses a fixed seed.

1. **249 scalar minimization cases**, including (x=y), (x=-y), and zero cases: maximum normalized error (3.765\times10^{-15}).
2. **600 arbitrary complex matrix-map interpolation cases.** Each map is scaled to satisfy all four hypotheses as actual operator inequalities; the largest hypothesis norm is (0.999999999999001), and the largest target-weight operator norm is (0.6329251185<1). These are finite counterexample searches, not a proof of interpolation.
3. **Internally entangled multimode weak convolution and generator covariance.** There are two modes per input port. The port-A state has a partial-transpose eigenvalue (-0.2619160171), so it is internally entangled. Inputs have total-number support at most four; calculations take place in the entire total-number-at-most-five sector, dimension 126. The sector has enough room for the single creation appearing in these expressions; this is not a local cutoff replacing the CCR. Sixteen complex-observable weak-convolution comparisons have maximum absolute error (2.824\times10^{-16}). The generator-covariance Frobenius residual is (3.719\times10^{-15}).
4. **Faithful non-number-diagonal finite-Fock controls.** A finite unitary rotates a geometric spectrum and gives a nonzero mean. The defect norm is evaluated from its dual weights and separately from ((1-v)K); the entropy production is evaluated directly from the dissipator and matrix logarithm. The exact finite-dimensional identity is

   \[
   \sigma=\|q\|^2-\bigl(e'-r\operatorname{Tr}\rho[d,d^\dagger]\bigr).
   \]

   Since (\operatorname{Tr}\rho[d,d^\dagger]=1-D\rho_{D-1,D-1}), the residual of the infinite-Fock formula at cutoff (D) must be (-rD\rho_{D-1,D-1}). All nine cases at dimensions 12, 32, 64 and references (r=0.1,1.3,4) match that exact boundary correction; corrected residuals are below (2\times10^{-11}). This control deliberately detects the common false finite-matrix version of the CCR.
5. **Exact rational bookkeeping** verifies the canceled centered-energy coefficients and the leading (-4N^4) moment drift for independent parameter choices. The full general cancellation and leading coefficient are derived in Sections 7.2 above; the finite rational cases are regression controls.

These checks support reproducibility and expose sign, conjugation, normalization, noncommutativity, and truncation mistakes. Finite samples are not the reason for accepting the theorem. The arbitrary-input conclusion rests on the analytic arguments reconstructed in Sections 3–7.

## 10. Exact interface delivered to Zenodo 23203100

Take (\rho_A=\rho), (\rho_B=|0\rangle\langle0|^{\otimes n}), and (\eta=t) in the substantively audited Theorem 1.1. The environment is independent and has zero energy and entropy. The retained state is (\mathcal L_t^{\otimes n}(\rho)). Since (g^{-1}(0)=0), Theorem 1.1 gives

\[
g^{-1}\!\left(S(\mathcal L_t^{\otimes n}(\rho))/n\right)
\geq t g^{-1}\!\left(S(\rho)/n\right).
\]

Applying increasing (g) gives exactly VE. Finite input energy guarantees finite input and output entropies, so the inverse and monotonicity step have no extended-real ambiguity. Arbitrary internal entanglement is covered by the source proof. Endpoints (t=0,1) give equality, and zero input entropy gives the valid nonnegativity bound. If downstream formulas use bits, replace (S,g\) together by (S/\log2,g/\log2); their entropy photon number and the claim are unchanged.

**Strongest result cleared:** the full pinned two-input EPnI for arbitrary independent finite-energy (n)-mode states, every fixed finite (n), and every transmissivity; in particular the exact vacuum-port bound with no product restriction inside the signal input.

**Exact remaining dependency gap:** none identified in this audit. No premise-conditional narrowing of the published upstream claim is needed on the basis of this analytic review. No claim is made here about other upstream revisions, infinite-energy inputs, infinitely many modes, correlated input ports, mode-dependent transmissivities, or the remaining capacity arguments in Zenodo 23203100.

**Completion estimate:** 100% of this assigned analytic dependency audit. Acceptance is an independent mathematical review assessment, not a declaration that a formal proof assistant has compiled the source.
 