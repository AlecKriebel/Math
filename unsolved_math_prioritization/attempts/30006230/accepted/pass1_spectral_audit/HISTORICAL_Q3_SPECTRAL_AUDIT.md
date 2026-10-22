# Independent audit: a positive-weight counterexample in the historical Q=3 range

## Verdict and scope

**PASS for the proposed solution-free Hardy–Rellich core in the historical n=1, Q=3 range.** This second construction uses strictly positive V and W, and satisfies the source side condition. Its antecedent holds for every original punctured-ball test: infinite-energy tests hold automatically, and the proof below covers all finite-energy tests without deleting the axis.

This statement concerns an explicitly proposed remainder-free converse. It does not contradict the source's forward theorem, which assumes a positive Bessel solution and includes a solution-dependent remainder. The historical version arXiv:2404.05510v1 includes Q=3; the inspected current v3 starts at Q=4. Thus this positive-weight counterexample does not resolve the positive-weight question in the current dimension range. The previously accepted Q=5 real-weight counterexample and its audit are unchanged.

The data are

\[
 n=1,\quad Q=3,\quad R=1,\quad
 V(r)=r^{3/4},\quad W(r)=\lambda r^{3/4},
\]

with lambda defined exactly in Section 1. Both weights are strictly positive and smooth on (0,1). The side condition is

\[
 S_3[V]=-2V/r^2+3V'/r-V''
 =\frac7{16}r^{-5/4}>0.
\]

## 1. Variational definition and positive-solution obstruction

Put b=11/4 and p(r)=r^b. Let H be the completion of real C_c^infinity(0,1) in the norm

\[
 E(v)^{1/2},\qquad E(v)=\int_0^1p(r)|v'(r)|^2\,dr,
\]

and put N(v)=integral p v^2 and m(v)=integral v, where the latter is the ordinary unweighted mean. For compact tests,

\[
 |v(r)|^2\le E(v)\int_r^1s^{-b}ds
 =E(v)\frac{r^{1-b}-1}{b-1}.
\]

Consequently N(v)<=E(v)/(2(b+1))=2E(v)/15, and E is a genuine Hilbert norm with a continuous inclusion into L^2(p dr). Its completion consists of locally H^1 functions with zero trace at 1. The displayed inequality passes to representatives by local convergence and gives uniform tail control

\[
 \int_0^\delta p|v|^2\le\frac{E(v)\delta^2}{2(b-1)}.
\]

This estimate and local Rellich compactness prove that H embeds compactly into L^2(p dr).

The ordinary mean is also continuous. For compact tests, integration by parts and Cauchy–Schwarz give

\[
 m(v)=-\int_0^1r v'(r)dr,\qquad
 |m(v)|\le E(v)^{1/2}
 \left(\int_0^1r^{2-b}dr\right)^{1/2}=2E(v)^{1/2}.
\]

This extended functional is indeed the ordinary integral of the represented function: the pointwise estimate above gives the uniform L^1 tail bound

\[
 \int_0^\delta|v(r)|dr
 \le \frac{E(v)^{1/2}}{\sqrt{b-1}}
 \int_0^\delta r^{(1-b)/2}dr
 =\frac{8E(v)^{1/2}}{\sqrt{b-1}}\delta^{1/8}.
\]

Together with local convergence, this proves continuity into L^1 and identifies m without an endpoint convention.

Define

\[
 \alpha=\inf_{v\in H\setminus\{0\}}E(v)/N(v),\qquad
 \beta=\inf_{v\in(H\cap\ker m)\setminus\{0\}}E(v)/N(v).
\]

The constrained set is nonempty, both values are finite and positive, and both minima are attained by weak compactness, the compact inclusion for N, and continuity of m. As in the Q=5 audit, taking the absolute value of an unrestricted minimizer preserves both forms. The resulting nonnegative minimizer solves

\[
 -(pv')'=\alpha pv
\]

on the open interval and is strictly positive by interior ODE uniqueness. Thus every unrestricted real minimizer has a strict sign and a nonzero ordinary integral. An attained zero-mean minimizer cannot also minimize the unrestricted quotient, so beta>alpha.

The trial v(r)=1-r^2 belongs to H. Its truncation near zero has extra derivative energy O(epsilon^(b-1)), which tends to zero; its zero trace at 1 permits ordinary approximation there. Direct integration gives

\[
 E(v)=\frac{16}{23},\qquad N(v)=\frac{512}{10695},\qquad
 \alpha\le\frac{465}{32}<16.
\]

Set

\[
 \lambda=\frac{\alpha+\min\{\beta,16\}}2.
\]

Then 0<alpha<lambda<beta and lambda<16. Accordingly q_lambda(v)=E(v)-lambda N(v) is nonnegative on ker m, but it is negative on some compact smooth test by approximation of an unrestricted minimizer in H.

The exact Q-dimensional Bessel equation is

\[
 (pf')'+\lambda pf=0.
\]

Any strictly positive flux-classical solution on the entire interval (0,1) would give the compact-test identity

\[
 q_\lambda(v)=\int_0^1pf^2\left|(v/f)'\right|^2dr\ge0,
\]

contradicting the negative compact test. This uses no condition on f at either endpoint, and the coefficient of W is exactly one.

## 2. Independent n=1 polar calculation

The low-dimensional angular structure is established here directly, rather than imported from a theorem restricted to n>=2. On the two sheets indexed by epsilon=sign(x), set

\[
 x=\epsilon r\sqrt{\sin\phi},\qquad
 t=\frac{r^2}{2}\cos\phi,\qquad 0<\phi<\pi.
\]

Write s_phi=sin(phi). Direct calculation of the Jacobian gives

\[
 |dx\,dt|=\frac{r^2}{2\sqrt{s_\phi}}\,dr\,d\phi,
 \qquad \psi=x^2/r^2=s_\phi.
\]

Give the two-sheet angular space the measure

\[
 d\Omega=\sqrt{\sin\phi}\,d\phi
\]

on each sheet, with counting measure in epsilon. Thus dx dt=r^2 dr dOmega/(2psi). The gradient and the divergence-form operator calculated in these coordinates are

\[
 |\nabla_Gu|^2=\psi\left(|u_r|^2+\frac4{r^2}|u_\phi|^2\right),
\]

\[
 L_G=\psi\left(\partial_r^2+\frac2r\partial_r+
 \frac4{r^2}L_\sigma\right),\qquad
 L_\sigma=\partial_\phi^2+\frac12\cot\phi\,\partial_\phi.
\]

These formulas hold on both open sheets. Subsequent integrations are justified in ambient coordinates, so no unproved boundary condition at their joining points is imposed.

## 3. A complete angular basis and its exact spectrum

Set z=cos(phi). Under this change, dOmega=(1-z^2)^(-1/4)dz on either sheet. Decompose L^2 of the two sheets into the even and odd subspaces under epsilon reversal.

The even functions

\[
 \Phi_{2m}(\epsilon,\phi)=c_{2m}C_m^{1/4}(\cos\phi),
 \qquad m=0,1,\ldots,
\]

form an orthonormal basis of the even sector after choosing positive normalizers c_(2m). This follows from Gegenbauer orthogonality for the weight (1-z^2)^(-1/4); their spans contain all polynomials, which are dense in this finite weighted L^2 space.

The odd functions

\[
 \Phi_{2m+1}(\epsilon,\phi)
 =c_{2m+1}\epsilon\sqrt{\sin\phi}\,
 C_m^{3/4}(\cos\phi)
\]

form an orthonormal basis of the odd sector. Dividing an odd function by (1-z^2)^(1/4) identifies its norm with the weighted norm for (1-z^2)^(1/4). Gegenbauer polynomials with parameter 3/4 are complete for precisely that weight. This argument covers every odd L^2 function, without requiring boundedness of the quotient at the endpoints.

For a function g(z), the even angular differential expression is

\[
 L_\sigma g=(1-z^2)g''-\frac32zg'.
\]

For h(z)=(1-z^2)^(1/4), direct differentiation gives

\[
 L_\sigma(hg)
 =h\left((1-z^2)g''-\frac52zg'-\frac12g\right).
\]

The Gegenbauer differential equations now yield

\[
 -4L_\sigma\Phi_k=a_k\Phi_k,\qquad a_k=k(k+1).
\]

In particular the first nonradial parameter is a_1=2. This calculation establishes the full spectrum needed for the proof, including the odd sector.

Each r^k Phi_k extends to an ambient polynomial. For k=2m it is a constant multiple of r^(2m) C_m^(1/4)(2t/r^2); Gegenbauer parity leaves only powers r^(4j)=(x^4+4t^2)^j. For k=2m+1 the same argument gives x times such a polynomial with parameter 3/4. These polynomials satisfy L_G(r^k Phi_k)=0 on x!=0 by the displayed differential equation, hence everywhere by polynomial continuity. It follows that chi(rho)Phi_k is an ambient smooth compact test whenever chi is compactly supported inside (0,1).

The ambient polynomial extension is important: arbitrary unrelated boundary conditions on the two angular sheets would give a different operator and would not justify the original test class.

## 4. Exact mode identity and an elementary nonradial bound

For a compact radial coefficient d and a=a_k, cancel the common positive factor one-half in the polar decomposition. The mode defect for the proposed core is

\[
 \begin{split}
 F_a[d]={}&\int r^{11/4}\left(d''+\frac2r d'-\frac a{r^2}d\right)^2dr\\
 &-\int\left(\lambda r^{3/4}+\frac12r^{-5/4}\right)
 \left(r^2(d')^2+a d^2\right)dr.
 \end{split}
\]

The one-half coefficient in the correction is exactly

\[
 (Q-1)(V/r^2-V'/r)=\frac12r^{-5/4}.
\]

Integration by parts gives the identity

\[
 F_a[d]=q_\lambda(d')+a\left[
 2\int r^{3/4}(d')^2+
 \left(a-\frac{13}{16}\right)\int r^{-5/4}d^2
 -\lambda\int r^{3/4}d^2\right].
\]

The integrand difference before integration is the derivative of

\[
 2r^{7/4}(d')^2-2ar^{3/4}dd'-\frac{5a}{4}r^{-1/4}d^2.
\]

Because d' has zero ordinary integral, q_lambda(d')>=0. For a=0 this proves the mode inequality.

For a>=2, set y=r^(3/8)d. All these functions are smooth and compactly supported in (0,1). A second exact integration by parts gives

\[
 2\int r^{3/4}(d')^2+
 \left(a-\frac{13}{16}\right)\int r^{-5/4}d^2
 =2\int(y')^2+\left(a-\frac{41}{32}\right)\int r^{-2}y^2.
\]

The inverse-square coefficient is at least 23/32>0. Dirichlet Poincare on (0,1) therefore yields a lower bound 2pi^2 integral y^2. Since lambda<16<2pi^2, the entire angular bracket is nonnegative, with a strict margin for nonzero d. No comparison theorem for Bessel zeros is required. Every angular mode is controlled.

## 5. Every original test and the degeneracy axis

Let u be an arbitrary real C_c^infinity(B_1 minus the origin) test. Its support lies in a compact annulus a<=rho<=b<1. The right side of the core is finite because all radial weights are bounded there. If the nonnegative left integral A_V(u)=integral V(L_Gu)^2/psi is infinite, the claimed inequality holds automatically.

It remains to treat every finite-energy test. V is bounded above and below by positive constants on this annulus, so finiteness of A_V is equivalent to finiteness of A_1. In n=1, finite energy is a real restriction on an individual smooth test, but it is not an extra restriction on the quantified inequality. For example, a nonzero value of u_xx at the axis creates a divergent integral of |x|^(-2). No axis avoidance assumption is made.

Expand u in the complete basis from Section 3, with coefficients d_k(r). They are smooth and have common compact radial support. The finite sums u_N are ambient smooth source tests by the polynomial-extension argument, and they include the axis in their domain.

For F=L_Gu/psi, finite energy means F belongs to L^2(r^2 dr dOmega). Test the ambient self-adjointness of L_G=partial_x^2+partial_t(x^2 partial_t) against chi(rho)Phi_k. The test is ambient smooth, so this step crosses the axis legitimately. Convert the resulting integrals by the exact Jacobian and integrate in r. This identifies the k-th angular coefficient of F as

\[
 d_k''+2d_k'/r-a_kd_k/r^2.
\]

Parseval and radial integration give

\[
 A_1(u-u_N)\longrightarrow0,
 \qquad \int\psi|u-u_N|^2\longrightarrow0.
\]

For w=u-u_N, ambient integration by parts gives

\[
 \int|\nabla_Gw|^2
 \le\left(\int\psi w^2\right)^{1/2}A_1(w)^{1/2}
 \longrightarrow0.
\]

The weighted left forms also converge, since V is bounded on the common annulus. The right forms converge because their coefficient K=lambda r^(3/4)+(1/2)r^(-5/4) is bounded there and the gradients converge in L^2. For each finite sum, ambient orthogonality gives the exact diagonal forms used in Section 4. Apply the nonnegative mode inequality and pass to the limit. This proves the proposed core for every finite-energy test, and therefore for every original source test.

This addresses the low-dimensional angular and axis gates directly. It does not infer their validity merely from the historical paper's dimension declaration.

## 6. Sources, reproducibility, and limits

- Historical source: Ganguly, Jotsaroop, Roychowdhury, *Hardy and Rellich identities and inequalities for Grushin operators via spherical vector fields and Bessel pairs*, [arXiv:2404.05510v1](https://arxiv.org/abs/2404.05510v1), [exact PDF](https://arxiv.org/pdf/2404.05510v1), 8 April 2024. Theorem 1.3 is on PDF p.6; this version includes n>=1, Q>=3.
- Inspected historical PDF: 391909 bytes; SHA-256 `28c09a2ce130ec8ed0d4a2e95c19e0416c6513b4f0b272bba485bae28bc9451e`.
- Current source: [arXiv:2404.05510v3](https://arxiv.org/abs/2404.05510v3), Theorem 1.3, PDF p.7, starts at Q>=4. Its narrower range is not silently extended here.
- Original informal question: Roychowdhury's contribution in *Mini-Workshop: Hardy Inequalities in Discrete and Continuum Settings*, printed p.606 / PDF p.28, [DOI:10.4171/OWR/2025/14](https://doi.org/10.4171/OWR/2025/14).

The companion exact-algebra script checks the angular differential conjugation, even and odd eigenvalue formulas, mode total derivative, elementary first-mode transformation, trial quotient, mean-continuity constant, and side-condition coefficient. These are runtime checks using explicit exceptions, including under Python optimization. They supplement the analytic proof rather than certify an infinite-dimensional result by numerical sampling. No eigenvalue approximation is used. Raw source PDFs and extracted source text are not included in the audit deliverable.

This establishes a positive-weight counterexample in the historical range for the selected solution-free core. It does not establish a counterexample with positive weights in Q>=4, a classification of all dimensions, a result for a stronger independently specified remainder, or resolution of every interpretation of the informal source question.
