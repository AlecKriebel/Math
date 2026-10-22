# A localized Gaussian-witness lower bound for rough fractional Lévy area

**Accepted rough-range proof after independent AI mathematical audit, 10 October 2026.** Together with [ALL_H_COROLLARY.md](ALL_H_COROLLARY.md) and [AREA_CONVENTION_CHECK.md](AREA_CONVENTION_CHECK.md), this establishes the original full-range lower-bound target. AI-assisted and unrefereed; no formal proof-assistant or novelty certification is claimed.

## 1. Exact claim and prior scope

Fix (H\in(1/4,1/2)). Let (B^1,B^2) be independent standard fractional Brownian motions, meaning centered continuous Gaussian processes with covariance
\[
 R_H(s,t)=\tfrac12(s^{2H}+t^{2H}-|t-s|^{2H}).
\]
Let (X_T=\int_0^T B^1_s\,dB^2_s) be their canonical iterated integral. For every (T>0) and integer (n\ge1), put
\[
 \mathcal G_{T,n}=\sigma(B^i_{jT/n}:i=1,2,\ j=1,\ldots,n).
\]
We prove that there is (c_H>0), depending only on (H), such that
\[
 \|X_T-E[X_T\mid\mathcal G_{T,n}]\|_2
 \ge c_H T^{2H}n^{1/2-2H}. \tag{1}
\]
The same bound holds for every square-integrable, \(\mathcal G_{T,n}\)-measurable approximation. The constant is not asserted sharp. This is an all-(n) inequality, not only a positive asymptotic lower limit.

This is the rough-range residual of Neuenkirch's question in *Rough Paths and PDEs*, OWR 41/2012, pp. 2524–2525, DOI [10.4171/owr/2012/41](https://doi.org/10.4171/owr/2012/41). The quantity is the indicated iterated integral, without replacing it by twice an antisymmetric area. The Brownian case has known exact RMS error (T/(2\sqrt n)). Neuenkirch–Shalaiko, *The maximum rate of convergence for the approximation of the fractional Lévy area at a single point*, J. Complexity 33 (2016), 107–117, DOI [10.1016/j.jco.2015.09.008](https://doi.org/10.1016/j.jco.2015.09.008), already give the corresponding asymptotic optimal rate for (H>1/2).

The only stochastic-area input below is the known (L^2) convergence, for fixed (T), of the left sums
\[
 X_T^{(m)}=\sum_{k=0}^{m-1}B^1_{kT/m}
       (B^2_{(k+1)T/m}-B^2_{kT/m})
 \longrightarrow X_T. \tag{2}
\]
For the stated rough range this follows from Neuenkirch–Tindel–Unterberger, *Discretizing the fractional Lévy area*, SPA 120 (2010), 223–254, DOI [10.1016/j.spa.2009.10.007](https://doi.org/10.1016/j.spa.2009.10.007); the inspected [arXiv version](https://arxiv.org/abs/0902.0497), Theorem 1.1, p. 3, explicitly gives its squared error as a finite constant times (T^{4H}m^{1-4H}+o(m^{1-4H})). We use convergence, not a lower bound for those sums. No lower estimate for optimal approximation is assumed.

## 2. A normalized real Gaussian representation

Write (\widehat h(\xi)=\int_{\mathbb R}e^{-it\xi}h(t)\,dt). Define
\[
 D_H=\int_{\mathbb R}|e^{i\xi}-1|^2|\xi|^{-1-2H}\,d\xi.
\]
It is finite and positive for (0<H<1): near zero the integrand is (O(|\xi|^{1-2H})), and at infinity it is (O(|\xi|^{-1-2H})). Let (\mathcal K) be the real Hilbert space of (L^2(\mathbb R;\mathbb C)) functions (u) satisfying (u(-\xi)=\overline{u(\xi)}), with real inner product
\[
 \langle u,v\rangle_{\mathcal K}=\int_{\mathbb R}u(\xi)\overline{v(\xi)}\,d\xi.
\]
This integral is real by the symmetry. Set
\[
 K_t(\xi)=D_H^{-1/2}(e^{it\xi}-1)|\xi|^{-H-1/2}.
\]
The squared distance between (K_t) and (K_s) is (|t-s|^{2H}), by change of variable, and (K_0=0). Polarization gives (\langle K_t,K_s\rangle=R_H(s,t)) for nonnegative times. Thus, for independent real isonormal processes (W_1,W_2) over (\mathcal K), (B^i_t=W_i(K_t)) realizes exactly the required law.

It suffices to prove (1) on this realization. Equation (2) constructs (X_T) from the path in (L^2); hence the joint law of the observations and (X_T), and therefore its minimum mean-square approximation error, agrees with the original model. The witness variables introduced below need not be measurable with respect to the original path. Their availability on a representation with the same joint law is sufficient for the Cauchy–Schwarz lower bound.

For a real compactly supported function (h) of the regularity used below, with (h(0)=0), define
\[
 u_h(\xi)=\frac{\sqrt{D_H}}{2\pi}|\xi|^{H+1/2}\overline{\widehat h(\xi)}. \tag{3}
\]
Provided (\int|\xi|^{2H+1}|\widehat h(\xi)|^2d\xi<\infty), this belongs to (\mathcal K). Fourier inversion gives the exact identity
\[
 E[B^i_tW_i(u_h)]
 =\langle K_t,u_h\rangle
 =\frac1{2\pi}\int(e^{it\xi}-1)\widehat h(\xi)\,d\xi
 =h(t). \tag{4}
\]
The conjugation in (3) fixes the Fourier-sign convention. All the functions used below have absolutely integrable Fourier transforms, so this use of inversion is classical.

## 3. Two explicit cell functions and a uniform Gram bound

Define, on the whole real line,
\[
 \phi(x)=\begin{cases}x^4(1-x)^4,&0\le x\le1,\\0,&\text{otherwise},\end{cases}
 \qquad f=\phi',\qquad g=\phi.
\]
Then (f,g) are real, supported in ([0,1]), and vanish at both endpoints. Their first two derivatives also vanish at both endpoints. They lie in (W^{3,1}(\mathbb R)); in particular (f'''=\phi'''') and (g'''=\phi''') are integrable piecewise polynomials, without boundary delta masses. Three integrations by parts give, for (r=f,g),
\[
 |\widehat r(\eta)|\le\|r\|_1,
 \qquad |\widehat r(\eta)|\le\|r'''\|_1|\eta|^{-3}\quad(\eta\ne0). \tag{5}
\]
The deterministic area pairing is strictly positive:
\[
 a:=\int_0^1 f(x)g'(x)\,dx=\int_0^1(\phi'(x))^2\,dx=\frac4{45045}>0. \tag{6}
\]
Only positivity is needed; the rational evaluation is optional and checkable by polynomial integration.

Put (\alpha=2H+1\in(3/2,2)). For (r=f,g), the periodized spectral density
\[
 P_r(\theta)=\sum_{\ell\in\mathbb Z}
    |\theta+2\pi\ell|^\alpha|\widehat r(\theta+2\pi\ell)|^2,
 \qquad -\pi\le\theta\le\pi,
\]
is bounded. Here the central summand is at most (\pi^\alpha\|r\|_1^2). For (|\ell|\ge1), (5) and (|\theta+2\pi\ell|\ge\pi(2|\ell|-1)) give the summable bound
\(|r'''\|_1^2[\pi(2|\ell|-1)]^{\alpha-6}\).
In particular a fully specified upper bound is
\[
 \overline P_r=\pi^\alpha\|r\|_1^2+
 2\|r'''\|_1^2\pi^{\alpha-6}
 \left(1+\frac1{2(5-\alpha)}\right). \tag{7}
\]
Indeed the positive decreasing series over odd integers is at most its first term plus the integral from 1 to infinity. Thus (0<\overline P_r<\infty).

For a cell length (\Delta>0) and integer (j), let
\[
 r_j(t)=\Delta^H r(t/\Delta-j),\qquad u^r_j=u_{r_j}.
\]
The factors of (Delta) cancel exactly in the Gram matrix:
\[
 \langle u^r_j,u^r_k\rangle
 =\frac{D_H}{4\pi^2}\int_{\mathbb R}|\eta|^\alpha
     |\widehat r(\eta)|^2e^{i(j-k)\eta}\,d\eta. \tag{8}
\]
For any finitely supported real vector ((b_j)), periodization and Parseval for the finite trigonometric polynomial imply
\[
 \left\|\sum_j b_ju^r_j\right\|_{\mathcal K}^2
 \le \frac{D_H\overline P_r}{4\pi^2}
        \int_{-\pi}^{\pi}\left|\sum_jb_je^{ij\theta}\right|^2d\theta
 =M_r\sum_jb_j^2,\qquad
 M_r:=\frac{D_H}{2\pi}\overline P_r. \tag{9}
\]
Tonelli applies before periodization because the relevant integrand is nonnegative. This establishes a uniform upper Gram bound, independent of the number and size of cells. It does not assert a lower bound for arbitrary linear combinations of fBm increments, a statement known to fail when (H<1/2).

## 4. The Gaussian witness is invisible to the entire observation sigma-field

Fix (T>0,n\ge1), and set (\Delta=T/n). For (j=0,\ldots,n-1), define
\[
 U_j=W_1(u^f_j),\qquad V_j=W_2(u^g_j),\qquad
 Y=\sum_{j=0}^{n-1}U_jV_j. \tag{10}
\]
All (f_j,g_j) vanish at every grid point (k\Delta), including 0 and (T). By (4), every (U_j,V_j) has zero covariance with every observed coordinate. The whole vector consisting of the (U_j,V_j) and observations is jointly centered Gaussian. Consequently ((U_0,\ldots,U_{n-1},V_0,\ldots,V_{n-1})) is independent of the entire observation vector. Thus (Y) is independent of (mathcal G_{T,n}). Also (E[Y]=0), since (W_1) and (W_2) are independent.

Let (A=(E[U_jU_k])) and (C=(E[V_jV_k])). They are positive semidefinite real symmetric matrices, with (A\le M_f I) and (C\le M_g I) by (9). Independence between the two components gives
\[
 E[Y^2]=\sum_{j,k}A_{jk}C_{jk}=\operatorname{tr}(AC)
 \le M_f\operatorname{tr}(C)\le nM_fM_g. \tag{11}
\]
For the middle inequality, (operatorname{tr}((M_fI-A)C)\ge0), because it is the trace of the positive semidefinite matrix (C^{1/2}(M_fI-A)C^{1/2}). This step does not require entrywise nonnegative covariances.

## 5. Exact covariance with the canonical iterated integral

For fixed (j), apply component independence and (4) to the finite sum in (2):
\[
 E[X_T^{(m)}U_jV_j]
 =\sum_{k=0}^{m-1} f_j(kT/m)
      [g_j((k+1)T/m)-g_j(kT/m)]. \tag{12}
\]
As (m\to\infty), the right side converges to the ordinary Riemann–Stieltjes integral (int_0^T f_j(t)g'_j(t)dt), because the functions are continuously differentiable. The left side converges to (E[X_TU_jV_j]) by (2) and Cauchy–Schwarz; (U_jV_j\in L^2) by Gaussian moments and component independence. Hence
\[
 E[X_TU_jV_j]=\int_0^T f_j(t)g'_j(t)dt
 =\Delta^{2H}a. \tag{13}
\]
Summing this finite identity gives
\[
 E[X_TY]=na\Delta^{2H}. \tag{14}
\]
There is no rough path integration by parts or stochastic Fubini assertion hidden in this step; (12) is a finite identity, followed by a known (L^2) limit and an ordinary deterministic Riemann-sum limit.

## 6. Conclusion, explicit constant, and scope

For every (F\in L^2(\mathcal G_{T,n})), independence and centering yield (E[FY]=0). Therefore (11), (14), and Cauchy–Schwarz give
\[
 na\Delta^{2H}=E[(X_T-F)Y]
 \le\|X_T-F\|_2\sqrt{nM_fM_g}.
\]
Thus (1) holds with the explicit positive choice
\[
 c_H=\frac{a}{\sqrt{M_fM_g}}
 =\frac{2\pi a}{D_H\sqrt{\overline P_f\overline P_g}}>0. \tag{15}
\]
Taking (F=E[X_T\mid\mathcal G_{T,n}]) proves the requested lower bound for optimal conditional expectation. Together with the already known upper rate, it proves order-optimality in the entire residual (1/4<H<1/2). The proof directly includes (n=1); no asymptotic-to-finite-(n) interpolation is necessary.

The harmonic representation, witness estimate, and Gram bound themselves hold more broadly. No claim of a new result for (H\ge1/2) is made, and the present statement is restricted to the assigned residual. There is no conclusion at (H=1/4), where the canonical (L^2) area input (2) fails, nor at (H=1), where (D_H) ceases to be finite. No optimal asymptotic constant or limiting error law is proved. No result for adaptive or arbitrary nonequidistant sampling is asserted.

## 7. Independently audited checkpoints

1. Verify the Fourier conjugation in (3) and the exact standard-fBm normalization (D_H).
2. Verify both compactly supported polynomial cell functions belong to (W^{3,1}), including endpoint distributional derivatives.
3. Verify the powers of (Delta) cancel in (8), while (13) has (Delta^{2H}).
4. Verify bounded periodization and the uniform Gram bound do not import the false rough-range increment lower bound.
5. Verify joint Gaussian independence from both sampled components, and mean zero of the product witness.
6. Verify (2) is a legitimate input for the exact target area and applies for every (H\in(1/4,1/2)).
7. Verify the PSD trace argument despite potentially signed off-diagonal covariances.
8. Verify that the external Gaussian witness is legitimate for an (L^2) error lower bound on the law of ((X_T,\mathcal G_{T,n})).
9. Verify the exact target normalization and the all-(n), all-(T) quantifiers. Numerics are not a substitute for any of these steps.
