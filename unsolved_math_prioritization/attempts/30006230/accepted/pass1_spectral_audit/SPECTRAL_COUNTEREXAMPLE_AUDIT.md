# Independent audit: a real-weight Hardy–Rellich core counterexample

## Verdict and exact scope

**PASS for the explicitly stated, remainder-free Hardy–Rellich core implication with real-valued W.** The construction below gives an inequality for every source test, including tests crossing the degeneracy axis, although the coefficient-one Q-dimensional Bessel equation has no positive solution on the full interval. It is not merely a radial-test example.

This is a negative result for a precisely stated interpretation. The source theorem also contains a remainder involving a positive solution already present in its forward hypothesis. Dropping that remainder to formulate a solution-free converse is an interpretive choice, not a quotation of a separately stated converse theorem. This audit does not settle a version requiring W to be positive, a version with additional endpoint assumptions, or a stronger inequality with an independently specified remainder. No novelty or human peer-review claim is made.

Take n=3, Q=n+2=5, R=exp(12), V=1, and

\[
 W(r)=\lambda r^{-2}-r^{-4},\qquad 0<r<R.
\]

The positive number lambda is defined variationally below. It satisfies lambda<12/5. Both weights have the required interior regularity, V is strictly positive, and

\[
 (Q-5)V/r^2+3V'/r-V''=0.
\]

W is permitted to be real-valued and is negative near zero. That sign feature is material to this construction.

## 1. Exact variational space and the strict gap

Let H be the completion of real C_c^infinity(0,R) in the Hilbert norm whose square is

\[
 E(v)=\int_0^R(r^4|v'|^2+|v|^2)\,dr.
\]

Define

\[
 N(v)=\int_0^Rr^2|v|^2\,dr,\qquad m(v)=\int_0^Rv\,dr,
\]

and

\[
 \alpha=\inf_{H\setminus\{0\}}\frac{E(v)}{N(v)},\qquad
 \beta=\inf_{(H\cap\ker m)\setminus\{0\}}\frac{E(v)}{N(v)}.
\]

There are nonzero smooth compactly supported members of ker m, for example two disjoint bumps with their integrals balanced. Thus both infima are over nonempty sets and are finite. N(v)>0 for every nonzero member of H: H identifies with a subspace of L^2(0,R), with its weak derivative defined locally on (0,R).

The mean is continuous on H because |m(v)| <= sqrt(R) E(v)^(1/2). This is the ordinary, unweighted integral. Replacing it by a weighted mean would change the problem and invalidate the derivative argument.

The embedding H into L^2((0,R),r^2 dr) is compact. For an E-bounded sequence,

\[
 \int_0^\delta r^2|v|^2\,dr\le\delta^2 E(v).
\]

On [delta,R], the same bound gives ordinary H^1 boundedness, since r^4>=delta^4. Rellich compactness on that interval, a diagonal subsequence, and the displayed uniform tail estimate prove compactness on (0,R). The trace at R is zero for H because it is a completion of compact tests and the norm controls H^1 near R. No trace condition at zero needs to be assumed or inferred.

Weak lower semicontinuity, compactness for N, and weak continuity of m show that both infima are attained after normalization N=1.

Every unrestricted minimizer has one strict sign on (0,R). Indeed, taking the absolute value preserves E and N; the absolute value belongs to H by the usual H^1 truncation argument on bounded subintervals and approximation in this norm. Its Euler–Lagrange equation is

\[
 -(r^4v')'+v=\alpha r^2v.
\]

The coefficients are regular on every interior interval, so the nonnegative minimizer is C^2 there. A zero at an interior point would also have zero derivative; uniqueness for the linear ODE would force it to vanish identically. Thus its absolute value is strictly positive. The original minimizer, also continuous on every interior interval, cannot change sign. It has a finite, nonzero ordinary integral.

Consequently beta>alpha. Otherwise a beta-minimizer with m=0 would also be an unrestricted alpha-minimizer, contradicting the preceding sign property. A separate assertion of first-eigenvalue simplicity is unnecessary.

## 2. An exact upper bound and an admissible lambda

For compact tests, integration by parts gives

\[
 \int r^4|v'|^2-\frac94\int r^2v^2
 =\int\left(r^2v'+\frac32rv\right)^2\ge0.
\]

The inequality extends to H, so alpha>=9/4. To bound alpha above, put t=log r and v(r)=r^(-3/2)h(log r). For compactly supported h,

\[
 \frac{E(v)}{N(v)}
 =\frac94+
 \frac{\int(|h'|^2+e^{-2t}h^2)\,dt}{\int h^2\,dt}.
\]

Choose h(t)=sin(pi(t-2)/10) on [2,12], and zero elsewhere. This piecewise H^1 function belongs to the relevant completion: it is continuous at both endpoints and vanishes there, including at r=R. Smooth compactly supported approximation is legitimate. Its quotient gives

\[
 \alpha\le\frac94+\frac{\pi^2}{100}+e^{-4}
 <\frac94+\frac1{10}+\frac1{50}
 =\frac{237}{100}<\frac{19}{8}<\frac{12}{5}.
\]

The strict rational bound uses pi^2<10 and e^4>50; no approximate eigenvalue is used. Set

\[
 \lambda=\frac{\alpha+\min\{\beta,12/5\}}2.
\]

Then alpha<lambda<beta and lambda<12/5. In particular,

\[
 q_\lambda(v):=E(v)-\lambda N(v)\ge0\quad(m(v)=0),
\]

while q_lambda is negative on some member of C_c^infinity(0,R). For the latter assertion, start with an alpha-minimizer and approximate it in H; E and N are continuous in that norm. This explicitly obtains the compact test needed below.

## 3. Full-interval positive-solution obstruction

For these weights the coefficient-one Bessel equation is exactly

\[
 (r^4f')'+(\lambda r^2-1)f=0.
\]

If a strictly positive flux-classical solution existed on (0,R), local regularity would give the usual classical solution there. For every compact test v, the ground-state identity would then give

\[
 q_\lambda(v)=\int_0^R r^4f^2\left|(v/f)'\right|^2\,dr\ge0.
\]

This contradicts the compact negative test from Section 2. No boundary value, integrability, boundedness, or limiting behavior of f at either endpoint is used. Thus the obstruction concerns precisely positivity on the entire open interval, with the coefficient of W equal to one.

## 4. Exact Grushin angular normalization

Write rho=(|x|^4+4t^2)^(1/4), psi=|x|^2/rho^2, and L_G=Delta_x+|x|^2 partial_t^2. In the polar variables (r,phi,omega), n=3 gives

\[
 d\Omega=(\sin\phi)^{3/2}\,d\phi\,d\omega,
 \quad dx\,dt=\frac{r^4}{2\psi}\,dr\,d\Omega,
 \quad L_G=\psi\left(\partial_r^2+\frac4r\partial_r+
 \frac4{r^2}L_\sigma\right).
\]

Use a complete orthonormal basis Phi_(k,j) of the source spherical-harmonic spaces. Here j records multiplicity and

\[
 -4L_\sigma\Phi_{k,j}=\mu_k\Phi_{k,j},\qquad
 \mu_k=k(k+3),\quad k=0,1,\ldots.
\]

Thus the first nonradial parameter is mu_1=4, not the spherical eigenvalue 1 before the factor 4 is applied. For a finite spherical sum with radial coefficients d_(k,j), compactly supported in (0,R), exact orthogonality gives

\[
 A(u):=\int\frac{(L_Gu)^2}{\psi}
 =\frac12\sum_{k,j}\int r^4
 \left(d''+\frac4r d'-\frac{\mu_k}{r^2}d\right)^2dr,
\]

and, for any radial K bounded on the common support,

\[
 \int K|\nabla_Gu|^2
 =\frac12\sum_{k,j}\int K r^4
 \left(|d'|^2+\frac{\mu_k}{r^2}d^2\right)dr.
\]

The factor one-half is retained in both formulas. It cancels in the inequality, but omitting it from only one form would be incorrect.

## 5. Exact mode defect and the first angular mode

The required core has K=W+4/r^2=(lambda+4)/r^2-1/r^4. Twice its defect in a single mode is

\[
 F_\mu[d]=\int\left\{
 r^4|d''|^2+(2\mu-\lambda)r^2|d'|^2+|d'|^2
 +\mu(\mu-\lambda-2)d^2+\mu r^{-2}d^2\right\}dr.
\]

For verification directly from the unintegrated square, the difference between the unintegrated mode defect and the displayed integrand is the derivative of

\[
 4r^3(d')^2-2\mu r^2dd'-2\mu rd^2.
\]

All boundary terms vanish for compact d. The crucial decomposition is

\[
 \begin{split}
 F_\mu[d]={}&q_\lambda(d')
 +2\mu\int(rd'+d/2)^2dr\\
 &+\mu(\mu-3/2-\lambda)\int d^2dr
 +\mu\int r^{-2}d^2dr.
 \end{split}
\]

Here d' is smooth and compactly supported and its **ordinary integral** is zero. Therefore q_lambda(d')>=0 by the strict-gap construction, in every angular mode, not only in the radial mode. For mu=0 this already proves the defect nonnegative. For every mu>=4, lambda<12/5 implies

\[
 \mu-3/2-\lambda>4-3/2-12/5=1/10.
\]

Every term in the decomposition is nonnegative. In particular the first nonradial mode is controlled with a strict margin.

A useful audit distinction: if one discards the constrained improvement and instead uses only the two scale-invariant weighted Hardy bounds, a weaker sufficient cap for the first angular mode is 169/68. That number is not an obstruction to the present construction and does not disprove the sufficient cap 5/2 when q_lambda(d')>=0 is retained. The actual cap 12/5 lies below both numbers. No sharpness claim about any of these caps is needed or established.

## 6. Every source test, including the degeneracy axis

Let u be any real C_c^infinity(B_R minus the origin) source test. Its support lies in a compact annulus a<=rho<=b<R. Since L_Gu is bounded and rho<=b,

\[
 \frac{(L_Gu)^2}{\psi}\le C|x|^{-2}
\]

on this bounded support. The singularity |x|^(-2) is locally integrable in x in R^3. Thus every source test in this chosen dimension has finite A(u), including tests that do not vanish on the axis x=0. The proof need not invoke the extended-infinite-energy convention here. K is bounded on the annulus, so its right-hand side is finite as well.

The coefficients d_(k,j)(r)=integral u(r,sigma)Phi_(k,j)(sigma)dOmega are smooth and supported in one common compact subinterval of (0,R). Radial differentiation under the angular integral is legitimate because u is smooth and all radial derivatives are bounded on the compact annulus.

Each finite sum u_N is a genuine ambient smooth source test, even at the axis. The source basis consists of spherical harmonic polynomials in x/r multiplied by Gegenbauer polynomials in 2t/r^2. These are smooth wherever rho>0. No axis cutoff is imposed.

The exact coefficients of L_Gu/psi are

\[
 d''+4d'/r-\mu_kd/r^2.
\]

One can justify this without making an unproved assertion about angular boundary domains: test ambient self-adjointness of L_G against chi(rho)Phi_(k,j), which is itself a smooth compact test. Convert the two ambient integrals with the displayed polar Jacobian, then integrate in r. The resulting distributional identity has smooth radial coefficients and gives the stated equality. All ambient integrations are legitimate across x=0 because the original operator has smooth divergence-form coefficients.

Parseval, followed by integration in r, now gives A(u-u_N)->0 and

\[
 \int\psi|u-u_N|^2\,dx\,dt\longrightarrow0.
\]

For w=u-u_N, ambient integration by parts and Cauchy–Schwarz give

\[
 \int|\nabla_Gw|^2
 =-\int wL_Gw
 \le\left(\int\psi w^2\right)^{1/2}
 \left(\int\frac{(L_Gw)^2}{\psi}\right)^{1/2}
 \longrightarrow0.
\]

Thus the gradients converge in L^2. Since K is bounded on the common annulus, integral K|gradient_G u_N|^2 tends to integral K|gradient_G u|^2, even though K changes sign. Apply Section 5 to u_N and pass to the limit. This proves

\[
 \int_{B_R}\frac{(L_Gu)^2}{\psi}\,dx\,dt
 \ge\int_{B_R}\left[W(\rho)+\frac4{\rho^2}\right]
 |\nabla_Gu|^2\,dx\,dt
\]

for **every** source test u. Together with Section 3, this proves the claimed counterexample in its exact stated scope.

## 7. Source/version pins and audit evidence

The source was inspected in the recovered arXiv:2404.05510v3 PDF and its text extraction: Theorem 1.3 on PDF p.7; polar coordinates and the Jacobian on pp.10–11; harmonic completeness, eigenvalues, and ambient smoothness on pp.11–13; Bessel-pair definitions on p.14. The polar and spectral facts used here are credited to that source. Their implementation in the counterexample and the full-test passage above were independently checked.

- Debdip Ganguly, K. Jotsaroop, Prasun Roychowdhury, *Hardy and Rellich identities and inequalities for Baouendi-Grushin operators via spherical vector fields*, [arXiv:2404.05510v3](https://arxiv.org/abs/2404.05510v3), [exact PDF](https://arxiv.org/pdf/2404.05510v3).
- arXiv revision date: 3 October 2026. PDF printed date: 6 October 2026. These are distinct metadata.
- Inspected PDF bytes: 453540. SHA-256: `3d3ab4146e39f5390d1b3460ea4da9f0b5360550337fa7311aaf6a22aa5daf98`.
- Original question: Prasun Roychowdhury's contribution in *Mini-Workshop: Hardy Inequalities in Discrete and Continuum Settings*, Oberwolfach Reports 22 (2025), no.1, 579–614, final paragraph of printed p.606 / PDF p.28. [DOI:10.4171/OWR/2025/14](https://doi.org/10.4171/OWR/2025/14).

The accompanying diagnostic script checks the exact total derivative, the constrained/angular split, the square completion, and rational cap comparisons using explicit runtime exceptions rather than removable assertions. It does not compute alpha or beta, establish compactness, check an infinite family numerically, or replace any analytic part of this audit. The manifest separately pins the reviewed authored proof and diagnostics. No copied source document is included in this audit deliverable.
