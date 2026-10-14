# Historical Q=3: a positive-W counterexample to the proposed Hardy–Rellich converse

14 October 2026. A separate historical-range result in shared PASS1. The previously completed Q=5 counterexample is unchanged.

## Result and interpretation

The proposed remainder-free Hardy–Rellich converse is false in the historical dimension \(Q=3\), **even for strictly positive \(V\) and \(W\)** and a strictly positive side condition. An exact counterexample is

\[
n=1,\quad Q=3,\quad R=1,\quad
V(r)=r^{3/4},\quad W(r)=\lambda r^{3/4},
\]

with an exact variationally specified constant \(\lambda\) below. It satisfies

\[
S_3[V]=-2V/r^2+3V'/r-V''=\frac7{16}r^{-5/4}>0.             \tag{1}
\]

For every original test \(u\in C_c^\infty(B_1\setminus\{0\})\), the proposed solution-free core holds:

\[
\int_{B_1}V(\rho)\frac{(L_Gu)^2}{\psi}\,dx\,dt
\ge
\int_{B_1}\left[W(\rho)+2\left(\frac{V(\rho)}{\rho^2}-\frac{V'(\rho)}\rho\right)\right]
|\nabla_Gu|^2\,dx\,dt.                                  \tag{2}
\]

Nevertheless there is no positive flux-classical solution on \((0,1)\) of

\[
(r^{11/4}f')'+\lambda r^{11/4}f=0.                        \tag{3}
\]

Thus the exact coefficient-one \(B_3(V,W;1)\) property fails. The coefficients in (2) are exactly the source normalization, with

\[
W+2(V/r^2-V'/r)=\lambda r^{3/4}+\tfrac12r^{-5/4}.
\]

The word “proposed” is essential: this is a solution-free remainder-free interpretation of the informal question, not the literal source theorem's positive-solution-dependent remainder. The historical v1 range includes \(Q=3\); current v3 starts at \(Q=4\). The proof below constructs the \(n=1\) angular basis and verifies its applicability to all original tests directly, rather than assuming that the newer source's dimension range extends.

## 1. One-dimensional constrained spectral gap

Write \(p(r)=r^{11/4}\). Let \(\mathcal H\) be the completion of \(C_c^\infty(0,1)\) in the norm

\[
q_0[w]^{1/2},\qquad q_0[w]=\int_0^1p|w'|^2dr,
\]

and put

\[
N[w]=\int_0^1p|w|^2dr,\qquad m[w]=\int_0^1w\,dr.
\]

For compact smooth \(w\), the weighted Hardy identity gives

\[
q_0[w]\ge\frac{49}{64}\int_0^1r^{3/4}|w|^2dr.             \tag{4}
\]

Indeed, expand \(\int r^{11/4}(w'+7w/(8r))^2\). This proves that the completion is a space of functions, controls local \(H^1\), and makes \(N\) continuous. The ordinary integral is continuous in this norm because

\[
m[w]=-\int_0^1r w'\,dr,\qquad |m[w]|^2\le
\left(\int_0^1r^{-3/4}dr\right)q_0[w]=4q_0[w].            \tag{5}
\]

This extension is the ordinary Lebesgue integral, not merely an abstract functional: since a compact test vanishes near 1,

\[
\int_0^1|w(r)|dr\le\int_0^1s|w'(s)|ds\le2q_0[w]^{1/2}.
\]

Thus completion also gives convergence in \(L^1\).

The inclusion \(\mathcal H\hookrightarrow L^2(p\,dr)\) is compact. On a bounded \(q_0\) set, (4) gives the uniform tail estimate

\[
\int_0^\delta p|w|^2dr
\le\frac{64}{49}\delta^2q_0[w].                          \tag{6}
\]

On each \([\delta,1]\), the \(q_0\) bound and (4) control usual \(H^1\), so ordinary compactness and then (6) prove the assertion.

Define the two finite, positive Rayleigh thresholds

\[
\alpha=\inf_{0\ne w\in\mathcal H}\frac{q_0[w]}{N[w]},
\qquad
\beta=\inf_{0\ne w\in\mathcal H,\ m[w]=0}
\frac{q_0[w]}{N[w]}.                                    \tag{7}
\]

The second class is nonempty because it contains derivatives of nonzero compact smooth bumps. Normalize minimizing sequences by \(N=1\). Compactness, weak lower semicontinuity, and the closedness of \(\ker m\) show that both infima are attained. In particular, no unattained spectral infimum is used.

An unrestricted minimizer can be chosen nonnegative by replacing it by its absolute value. Its interior Euler–Lagrange equation is

\[
-(p w')'=\alpha p w.                                    \tag{8}
\]

Interior regularity and uniqueness for the initial-value problem imply that a nonnegative nonzero minimizer is strictly positive: an interior zero would also have zero derivative and force the solution to vanish. For any other real minimizer, its absolute value is likewise a minimizer and strictly positive. Thus every unrestricted minimizer has a strict constant sign and nonzero ordinary integral. If \(\beta=\alpha\), an attained constrained minimizer would be an unrestricted minimizer with zero mean, a contradiction. Hence

\[
\boxed{\beta>\alpha>0.}                                 \tag{9}
\]

### An exact trial bound and exact parameter choice

The trial function \(w(r)=1-r^2\) belongs to \(\mathcal H\). At zero, a cutoff on \((\varepsilon,2\varepsilon)\) has added derivative cost \(O(\varepsilon^{7/4})\); at 1, the function's linear vanishing makes the standard boundary-cutoff cost \(O(\varepsilon)\). Subsequent smoothing away from the endpoints gives compact smooth approximation in \(q_0\).

Its Rayleigh quotient is exactly

\[
\frac{\int_0^1 4r^{19/4}dr}
 {\int_0^1r^{11/4}(1-r^2)^2dr}
=\frac{16/23}{4/15-8/23+4/31}
=\frac{465}{32}<16.                                    \tag{10}
\]

Set

\[
\boxed{\lambda=\frac{\alpha+\min\{\beta,16\}}2.}          \tag{11}
\]

Then

\[
0<\alpha<\lambda<\beta,\qquad \lambda<16.                \tag{12}
\]

No numerical eigenvalue approximation is part of this definition. For

\[
q_\lambda[w]=q_0[w]-\lambda N[w],
\]

we have \(q_\lambda[w]\ge0\) on \(\mathcal H\cap\ker m\), while it is negative on an unrestricted minimizer. Compact approximation produces a compact smooth test with negative \(q_\lambda\).

If a positive solution of (3) existed, the compactly supported ground-state identity would give

\[
q_\lambda[w]=\int_0^1p f^2\left|(w/f)'\right|^2dr\ge0
\quad(w\in C_c^\infty(0,1)),                             \tag{13}
\]

contradicting that negative test. This proves the precise failure of \(B_3\) without imposing any endpoint condition on the proposed positive solution.

## 2. A complete angular basis for n=1, proved directly

Here \(x,t\in\mathbb R\),

\[
\rho=(x^4+4t^2)^{1/4},\quad\psi=x^2/\rho^2,
\quad L_G=\partial_x^2+x^2\partial_t^2.
\]

Away from the axis use the two coordinate sheets

\[
x=s r\sqrt{\sin\varphi},\qquad t=\tfrac12r^2\cos\varphi,
\qquad s\in\{+1,-1\},\quad0<\varphi<\pi.
\]

Direct change of variables and the chain rule give

\[
dx\,dt=\frac{r^2}{2\psi}\,dr\,d\Omega,
\qquad d\Omega=\sin^{1/2}\varphi\,d\varphi
\quad\text{on each sheet},                              \tag{14}
\]

\[
L_G=\psi\left(\partial_r^2+\frac2r\partial_r+
\frac4{r^2}\mathcal L\right),
\qquad
\mathcal L=\partial_\varphi^2+\tfrac12\cot\varphi\,\partial_\varphi.
                                                                  \tag{15}
\]

The angular Hilbert space is the direct sum of the two sheet spaces. Decompose it into functions even and odd under \(s\mapsto-s\).

### Polynomial construction and completeness

For \(\gamma>-1\), let \(P_m^{(\gamma)}(z)\) be a real orthogonal polynomial of degree \(m\) for the weight \((1-z^2)^\gamma\) on \((-1,1)\). These polynomials form a complete orthogonal system: continuous functions are dense for the finite positive measure, and ordinary polynomials approximate continuous functions uniformly. The weight is even, so \(P_m^{(\gamma)}\) has parity \(m\).

A direct integration by parts shows that

\[
\mathcal J_\gamma=(1-z^2)\partial_z^2-(2\gamma+2)z\partial_z
\]

is symmetric on polynomials in that weighted space. The boundary term contains \((1-z^2)^{\gamma+1}\) and vanishes. Since \(\mathcal J_\gamma\) preserves polynomial degree and has leading coefficient \(-m(m+2\gamma+1)\) in degree \(m\), orthogonality implies

\[
\mathcal J_\gamma P_m^{(\gamma)}
=-m(m+2\gamma+1)P_m^{(\gamma)}.                           \tag{16}
\]

Take \(z=\cos\varphi\). The even sector has measure
\((1-z^2)^{-1/4}dz\), so a complete even angular basis is

\[
\Phi_{2m}(s,\varphi)=c_m P_m^{(-1/4)}(\cos\varphi).
\]

Here and below the real positive constants normalize the two-sheet \(L^2\) norm. For the odd sector, multiplication by
\(g(z)=(1-z^2)^{1/4}=\sqrt{\sin\varphi}\)
is an onto isometry from the weight-\(+1/4\) space to the weight-\(-1/4\) space. Thus a complete odd angular basis is

\[
\Phi_{2m+1}(s,\varphi)
=\widetilde c_m s\sqrt{\sin\varphi}\,
 P_m^{(1/4)}(\cos\varphi).
\]

They are the usual even/odd Gegenbauer formulas with parameters \(1/4\) and \(3/4\), but the argument above proves the needed completeness without citing an \(n\ge2\) result.

In the \(z\) coordinate, \(\mathcal L=\mathcal J_{-1/4}\). Direct differentiation also gives

\[
\mathcal L(gP)=g\left(\mathcal J_{1/4}P-\tfrac12P\right).
\]

Therefore the complete real orthonormal basis just constructed satisfies

\[
-4\mathcal L\Phi_k=a_k\Phi_k,
\qquad a_k=k(k+1),\quad k=0,1,\ldots.                   \tag{17}
\]

In particular, every nonconstant mode has \(a_k\ge2\).

### Ambient smoothness, including the axis

Each \(r^k\Phi_k\) is a polynomial in \(x,t\). Indeed, parity of the degree-\(m\) polynomial means its monomials have degrees \(m-2j\). In the even case, multiplying by \(r^{2m}\) turns them into

\[
(2t)^{m-2j}r^{4j}=(2t)^{m-2j}(x^4+4t^2)^j.
\]

In the odd case, multiplying by \(r^{2m+1}s\sqrt{\sin\varphi}\) gives the same polynomials multiplied by \(x\). Equation (15) shows these are Grushin-harmonic polynomials, first away from the axis and then everywhere by polynomial continuity.

Consequently \(\chi(r)\Phi_k\) is Cartesian smooth on the entire punctured plane for every compact smooth radial \(\chi\). This is the key fact that allows ambient integration by parts across the axis. We have not selected or imposed a pole boundary condition on an abstract angular differential operator.

## 3. Exact finite-mode inequality

Let \(d\in C_c^\infty(0,1)\) and \(a=a_k\). Apart from the common positive factor \(1/2\) from (14), its mode difference in (2) is

\[
\begin{aligned}
F_a[d]&=\int_0^1 r^{11/4}
  \left(d''+\frac2r d'-\frac a{r^2}d\right)^2dr\\
&\quad-\int_0^1\left(\lambda r^{3/4}+\tfrac12r^{-5/4}\right)
 (r^2d'^2+a d^2)dr.
\end{aligned}                                          \tag{18}
\]

Integration by parts, with no endpoint terms, gives exactly

\[
\boxed{\begin{aligned}
F_a[d]&=q_\lambda[d']+a B_a[d],\\
B_a[d]&=2\int_0^1r^{3/4}d'^2dr
 +(a-\tfrac{13}{16})\int_0^1r^{-5/4}d^2dr
 -\lambda\int_0^1r^{3/4}d^2dr.
\end{aligned}}                                         \tag{19}
\]

In particular \(F_0[d]=q_\lambda[d']\). The derivative \(d'\) has zero ordinary integral, so \(q_\lambda[d']\ge0\) by (7) and (12).

For the angular bracket put \(y=r^{3/8}d\), another compact smooth test on \((0,1)\). Expanding and integrating its mixed term gives

\[
B_a[d]=2\int_0^1|y'|^2dr
 +(a-\tfrac{41}{32})\int_0^1r^{-2}y^2dr
 -\lambda\int_0^1y^2dr.                                \tag{20}
\]

For \(a\ge2\), its inverse-square coefficient is at least \(23/32>0\). The ordinary Dirichlet Poincaré inequality on \((0,1)\) yields

\[
B_a[d]\ge(2\pi^2-\lambda)\int_0^1y^2dr\ge0,             \tag{21}
\]

since \(\lambda<16<2\pi^2\). One may obtain the Poincaré inequality directly by the ground-state identity with the positive function \(\sin(\pi r)\); no Bessel zero estimate is needed. Thus \(F_a[d]\ge0\) for every angular mode.

For completeness, in the power-weight calculation the coefficient of \(\int r^{b-2}d^2\) before specializing \(b=3/4\) is \(a(a-b^2+5b-4)\). At \(b=3/4\) it is \(a(a-13/16)\). This checks the weight derivative correction in (18)–(19) explicitly.

## 4. Extension to every original source test

For a source test \(u\), the right side of (2) is finite: its compact support lies in a radial annulus where \(V,W,V'\) and all other radial coefficients are bounded. The left side is a nonnegative extended integral. If it is infinite, (2) is automatic. The axis is not removed from the test class.

Suppose therefore that \(A_V[u]<\infty\). On the common compact radial annulus, \(V\) and \(1/V\) are bounded. Thus the unweighted energy \(A_1[u]\) is finite too. Put

\[
u=\sum_{k\ge0}d_k(r)\Phi_k,\qquad
u_N=\sum_{k=0}^N d_k(r)\Phi_k.
\]

Every \(d_k\) is compact smooth in the same annulus, by differentiation under the angular integral; radial derivatives of the Cartesian-smooth pullback are bounded there. Each \(u_N\) is an original Cartesian-smooth compact test by Section 2, and its \(L_Gu_N\) contains the factor \(\psi\), so it has finite energy.

Let \(F=L_Gu/\psi\). Finiteness of \(A_1[u]\) means that \(F\in L^2(r^2dr\,d\Omega)\). For \(\chi\in C_c^\infty(0,1)\), ambient integration by parts is legitimate because \(\chi(r)\Phi_k\) is a smooth test across the axis:

\[
\begin{aligned}
\int F\chi\Phi_k\,r^2dr\,d\Omega
&=2\int L_Gu\,\chi\Phi_k\,dx\,dt\\
&=2\int u L_G(\chi\Phi_k)\,dx\,dt\\
&=\int_0^1r^2d_k
 \left(\chi''+\frac2r\chi'-\frac{a_k}{r^2}\chi\right)dr.
\end{aligned}
\]

A radial integration by parts identifies the coefficient of \(F\) as
\(d_k''+2d_k'/r-a_kd_k/r^2\). Completeness and Parseval therefore show

\[
A_V[u]=\frac12\sum_{k\ge0}\int_0^1 r^{11/4}
 \left(d_k''+\frac2r d_k'-\frac{a_k}{r^2}d_k\right)^2dr,
\]

as well as \(A_V[u-u_N]\to0\) and \(\int\psi|u-u_N|^2\to0\). The boundedness of \(1/V\) on the common annulus also gives \(A_1[u-u_N]\to0\).

For the original smooth compact difference \(v_N=u-u_N\),

\[
\int|\nabla_Gv_N|^2=-\int v_NL_Gv_N
\le\left(\int\psi v_N^2\right)^{1/2}A_1[v_N]^{1/2}
\longrightarrow0.                                     \tag{22}
\]

Thus the right side of (2) converges from \(u_N\) to \(u\). For finite sums, its exact diagonal expression is

\[
D_{V,W}[u_N]=\frac12\sum_{k=0}^N\int_0^1
 \left(\lambda r^{3/4}+\tfrac12r^{-5/4}\right)
 (r^2d_k'^2+a_kd_k^2)dr.
\]

This follows either from the polar gradient formula and angular orthogonality or from ambient integration by parts for each pair of polynomial modes. Section 3 proves \(A_V[u_N]\ge D_{V,W}[u_N]\). The verified convergence proves (2) for every finite-energy original test and hence for all tests under the extended-energy convention.

## 5. Endpoint mechanism and source boundary

The original radial derivative substitution gives precisely the mean-zero class: if \(w=d'\) with \(d\) compact smooth, then \(\int w=0\); conversely, every compact smooth mean-zero \(w\) has a compact smooth primitive. Equation (5) shows this is a closed constraint in the relevant energy norm. The lowest positive one-dimensional eigenmode is excluded, creating the strict gap (9).

In this historical dimension, the side condition allows the effective leading weight \(p=r^{11/4}\), whose exponent is below 3. A normalized mean-correcting bump at scale \(\varepsilon\) has derivative energy proportional to \(\varepsilon^{-1/4}\), rather than tending to zero. Unlike the Q=5 real-W example, no negative potential tail is needed: \(W>0\) everywhere. The historical dimensional distinction has a substantive consequence.

The informal question occurs in Roychowdhury's contribution on printed p.606 / PDF p.28 of Oberwolfach Report 14/2025. [Official report](https://ems.press/content/serial-article-files/51358?nt=1), [DOI](https://doi.org/10.4171/OWR/2025/14).

The historical framework, Theorem 1.3, and side condition are in Ganguly–Jotsaroop–Roychowdhury, *Hardy and Rellich identities and inequalities for Grushin operators via spherical vector fields and Bessel pairs*, arXiv:2404.05510v1, especially setup p.2, theorem p.6, and polar/spectral material in Section 2. [Historical primary PDF](https://arxiv.org/pdf/2404.05510v1). The current revision begins at \(Q\ge4\). [Current primary PDF](https://arxiv.org/pdf/2404.05510v3). The explicit two-sheet argument above independently verifies the historical \(n=1\) spectral and test-domain steps needed here; it does not infer an explanation for the source's later change in range.

This is an authored proof for a precisely stated proposed core and historical dimension. It is not a claim about novelty, human peer review, or all interpretations of the source's solution-dependent Hardy–Rellich question. The companion diagnostic script checks the exact algebra and low-degree polynomial identities; the proof does not depend on numerical computation.
