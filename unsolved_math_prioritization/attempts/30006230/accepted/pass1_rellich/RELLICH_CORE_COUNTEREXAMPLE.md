# A counterexample to the proposed solution-free Hardy–Rellich converse

14 October 2026. Authored mathematical argument, shared PASS1. This addresses an explicitly proposed remainder-free interpretation, not the literal solution-dependent remainder in the source theorem.

## Result and exact scope

The implication

\[
A_V[u]\ge D_{V,W}[u]\quad\text{for every }u\in C_c^\infty(B_R\setminus\{0\})
\quad\Longrightarrow\quad B_Q(V,W;R)
\]

is **false** for the proposed regular real-weight class, even with the source side condition

\[
S_Q[V]=(Q-5)V/r^2+3V'/r-V''\ge0.
\]

An exact counterexample has

\[
n=3,\qquad Q=5,\qquad R=e^{12},\qquad
V(r)=1,\qquad W(r)=\frac{\lambda}{r^2}-\frac1{r^4}.
\]

The real constant \(\lambda\) is specified unambiguously by variational definitions below. In particular, it is not a numerically rounded parameter. These weights satisfy \(V>0\), \(V\in C^2(0,R)\), \(W\in C^1(0,R)\), and \(S_5[V]=0\). The core holds for **every original punctured-gauge-ball test**, including tests meeting the entire axis \(x=0\). No positive flux-classical solution of

\[
(r^4 f')'+r^4 Wf=0
\]

exists on the full interval \((0,R)\), with coefficient of \(W\) exactly one.

This disproves the universal assertion in the selected current \(Q\ge4\) range, by one allowed dimension. It does not classify each dimension. It does not resolve the separately retained historical \(Q=3\) branch, the \(W\ge0\) restriction, or a stronger independent-function remainder premise. The source theorem's remainder already assumes a positive ODE solution and is not contradicted.

## 1. Geometry and the exact proposed antecedent

Use the source normalization

\[
\rho=(|x|^4+4t^2)^{1/4},\quad \psi=|x|^2/\rho^2,
\quad L_G=\Delta_x+|x|^2\partial_t^2,
\quad \nabla_G=(\nabla_x,|x|\partial_t).
\]

Here \(x\in\mathbb R^3\), \(t\in\mathbb R\), and \(B_R=\{\rho<R\}\). In this counterexample the exact core is

\[
\int_{B_R}\frac{(L_Gu)^2}{\psi}\,dx\,dt
\ge
\int_{B_R}\left(W(\rho)+\frac4{\rho^2}\right)|\nabla_Gu|^2\,dx\,dt.       \tag{1}
\]

The \(4/\rho^2\) term is precisely \((Q-1)(V/\rho^2-V'/\rho)\), evaluated at \(Q=5,V=1\); no correction term was omitted or changed.

The nonnegative left side is interpreted as an extended integral. In fact, it is finite for every test in this example. On the compact support, \(\rho\) is bounded away from zero, \(L_Gu\) is bounded, and \(1/\psi=\rho^2/|x|^2\). The function \(|x|^{-2}\) is locally integrable in \(\mathbb R^3\). Values on the measure-zero axis do not alter the integral. The right side is finite as well, since all its radial coefficients are bounded on this support. Thus no test is discarded by a finite-energy restriction.

## 2. A strictly positive gap created by the ordinary-mean constraint

Fix \(R=e^{12}\). Let \(\mathcal H\) be the completion of \(C_c^\infty(0,R)\) in the Hilbert norm

\[
\|w\|_{\mathcal H}^2=q_0[w]
:=\int_0^R\bigl(r^4|w'|^2+|w|^2\bigr)\,dr.
\]

Its elements are locally \(H^1\), and derivatives are interpreted weakly. Put

\[
N[w]=\int_0^R r^2|w|^2\,dr,\qquad
m[w]=\int_0^R w\,dr,
\]

and define the exact real numbers

\[
\alpha=\inf_{0\ne w\in\mathcal H}\frac{q_0[w]}{N[w]},\qquad
\beta=\inf_{0\ne w\in\mathcal H,\ m[w]=0}\frac{q_0[w]}{N[w]}.       \tag{2}
\]

Both admissible classes are nonempty; for the second one, take the derivative of any nonzero compact smooth bump. Both infima are finite and positive. For positivity, \(N[w]\le R^2q_0[w]\) suffices.

### Compactness and attainment

The inclusion \(\mathcal H\hookrightarrow L^2((0,R),r^2dr)\) is compact. Indeed, for a \(q_0\)-bounded sequence,

\[
\int_0^\delta r^2|w|^2dr\le\delta^2q_0[w].                    \tag{3}
\]

On each \([\delta,R]\), the same bound controls the usual \(H^1\) norm because \(r^4\ge\delta^4\); the one-dimensional compact inclusion into \(L^2\) applies. A diagonal subsequence followed by (3) gives compactness on the whole interval.

Moreover,

\[
|m[w]|\le R^{1/2}\left(\int_0^R|w|^2dr\right)^{1/2}
\le R^{1/2}\|w\|_{\mathcal H}.                               \tag{4}
\]

Consequently \(\ker m\) is a closed Hilbert subspace. Normalize minimizing sequences by \(N=1\); weak compactness in \(\mathcal H\), compact convergence for \(N\), weak lower semicontinuity, and weak continuity of \(m\) show that both infima in (2) are attained.

### Positivity and simplicity of the unrestricted minimizer

Replacing a minimizer for \(\alpha\) by its absolute value preserves \(q_0\) and \(N\), so there is a nonnegative minimizer \(w_0\). The Euler–Lagrange equation is

\[
-(r^4w_0')'+w_0=\alpha r^2w_0.                             \tag{5}
\]

Interior one-dimensional regularity makes it classical. A zero of a nonnegative solution in the interior has zero derivative; uniqueness for the regular initial-value problem then forces the solution to vanish identically. Thus \(w_0>0\) on \((0,R)\).

Every real minimizer for \(\alpha\) has one strict sign: its absolute value is another nonnegative minimizer and cannot have an interior zero. The minimizer space is one-dimensional. Otherwise a nontrivial linear combination of two independent minimizers could be chosen to vanish at an interior point, contradicting the preceding fact. These arguments also justify the usual simple-ground-state assertion without an endpoint classification theorem.

Since \(w_0\in L^1(0,R)\) by (4), its strict positivity gives \(m[w_0]>0\). If \(\beta=\alpha\), an attained constrained minimizer would be an unrestricted minimizer, hence a nonzero multiple of \(w_0\), impossible when its mean is zero. Therefore

\[
\boxed{\beta>\alpha.}                                      \tag{6}
\]

### An elementary upper bound on \(\alpha\)

Write \(r=e^s\) and \(w(r)=r^{-3/2}y(s)\). For a compactly supported \(y\), integration of the mixed term gives

\[
N[w]=\int y^2ds,\qquad
q_0[w]=\int\left(|y'|^2+\frac94y^2+e^{-2s}y^2\right)ds.     \tag{7}
\]

Use the \(H^1_0\) trial function

\[
y(s)=\begin{cases}
\sin\bigl(\pi(s-2)/10\bigr),&2<s<12,\\
0,&s\le2.
\end{cases}
\]

It yields an element of \(\mathcal H\): its support is away from zero and it has zero trace at \(R\), so ordinary compact smooth approximation applies. Equation (7) implies

\[
\alpha\le\frac94+\frac{\pi^2}{100}+e^{-4}
<\frac{19}{8}<\frac{12}{5}.                               \tag{8}
\]

For example, the strict estimate follows already from \(\pi^2<10\) and \(e^4>50\), giving an upper bound \(2.37<19/8\). The latter exponential estimate follows from the first eight nonnegative terms of its power series.

### The exact coefficient

Define

\[
\boxed{\lambda=\frac{\alpha+\min\{\beta,12/5\}}2.}          \tag{9}
\]

By (6)–(8),

\[
\alpha<\lambda<\beta,\qquad \lambda<12/5<5/2.             \tag{10}
\]

For the stated weight \(W\), the one-dimensional Hardy form is exactly

\[
q_\lambda[w]
=\int_0^Rr^4\bigl(|w'|^2-W|w|^2\bigr)dr
=q_0[w]-\lambda N[w].                                    \tag{11}
\]

Thus

\[
q_\lambda[w]\ge(\beta-\lambda)N[w]\ge0
\quad\text{if }w\in\mathcal H,\ m[w]=0,                  \tag{12}
\]

whereas \(q_\lambda[w_0]=(\alpha-\lambda)N[w_0]<0\).

## 3. Failure of the exact full-interval Bessel property

Since \(w_0\) is in the completion defining \(\mathcal H\), choose \(w_j\in C_c^\infty(0,R)\) converging to it in \(q_0\). Since \(N\le R^2q_0\), this convergence also preserves \(N\). Hence \(q_\lambda[w_j]<0\) for at least one compact smooth test.

If a positive flux-classical \(f\) solved

\[
(r^4 f')'+r^4 Wf=0\quad\text{on }(0,R),
\]

ordinary interior regularity would permit the Picone/ground-state calculation for any \(w\in C_c^\infty(0,R)\):

\[
\int_0^Rr^4\bigl(|w'|^2-Ww^2\bigr)dr
=\int_0^Rr^4 f^2\left|\left(\frac w f\right)'\right|^2dr
\ge0.                                                    \tag{13}
\]

All integrations occur on a compact interior interval, so no endpoint condition is used. The negative compact test contradicts (13). This proves failure of \(B_5(V,W;R)\), at coefficient one and on the specified full interval.

## 4. Exact radial reduction and the constraint that cannot be dropped

For \(d\in C_c^\infty(0,R)\), the gauge-radial function \(u(x,t)=d(\rho(x,t))\) is smooth away from the origin, including at \(x=0,t\ne0\). It has finite energy, as is also immediate from \(L_Gd=\psi(d''+4d'/r)\).

After the positive angular constant is canceled, the difference of the two sides of (1) is

\[
\int_0^R r^4\left(d''+\frac4r d'\right)^2dr
-\int_0^R\left(W+\frac4{r^2}\right)r^4d'^2dr
=q_\lambda[d'].                                          \tag{14}
\]

Here the mixed term gives exactly the displayed \(4/r^2\) correction. The test \(w=d'\) satisfies

\[
\int_0^R w(r)dr=0,                                       \tag{15}
\]

so (12) proves radial core validity. Conversely, a compact smooth \(w\) satisfying (15) has a compact smooth primitive. The radial core therefore sees precisely this codimension-one class, rather than arbitrary one-dimensional compact tests.

## 5. Universal validity, including all angular modes and the axis

We now prove (1) for all original tests, not merely radial ones. The polar measure and angular spectral decomposition used here are the source's \(\alpha=1\), one-vertical-variable formulas. With \(\sigma\) the gauge-sphere variable,

\[
dx\,dt=\frac{r^4}{2\psi}\,dr\,d\Omega,
\quad L_G=\psi\left(\partial_r^2+\frac4r\partial_r+\frac4{r^2}L_\sigma\right).
\]

For a complete orthonormal angular eigenbasis, including all multiplicities, write

\[
-L_\sigma\Phi_{k,j}=\frac{a_k}{4}\Phi_{k,j},
\qquad a_k=k(k+3),\quad k=0,1,\ldots,
\]

and \(u=\sum_{k,j}d_{k,j}(r)\Phi_{k,j}(\sigma)\). The zero mode has \(a_0=0\), and every nonconstant mode satisfies \(a_k\ge4\). Each \(d_{k,j}\) is smooth and compactly supported in a common interior radial interval, since the original test is Cartesian smooth and compactly supported away from the origin and outer boundary.

### Ambient integration by parts and full-test convergence

There is no need to impose an unverified angular boundary condition at the poles. The source eigenfunctions are restrictions of homogeneous Grushin-harmonic polynomials: each \(r^k\Phi_{k,j}\) is Cartesian smooth. This also follows directly from the polynomial formula in source Lemma 2.1. Hence \(\chi(r)\Phi_{k,j}\) is an original Cartesian-smooth compact test whenever \(\chi\in C_c^\infty(0,R)\); division by powers of \(r=\rho\) is harmless away from the origin. The finite angular sums

\[
u_N=\sum_{k\le N,j}d_{k,j}(r)\Phi_{k,j}(\sigma)
\]

are therefore original smooth tests on the same compact radial annulus.

Put \(F=L_Gu/\psi\). Section 1 implies that \(F\) lies in \(L^2(r^4dr\,d\Omega)\). For a radial compact smooth \(\chi\), the symmetry of \(L_G=\operatorname{div}_x\nabla_x+\partial_t(|x|^2\partial_t)\) gives

\[
\begin{aligned}
\int F\chi\Phi_{k,j}\,r^4dr\,d\Omega
&=2\int L_Gu\,\chi\Phi_{k,j}\,dx\,dt\\
&=2\int u L_G(\chi\Phi_{k,j})\,dx\,dt\\
&=\int_0^Rr^4d_{k,j}
 \left(\chi''+\frac4r\chi'-\frac{a_k}{r^2}\chi\right)dr.
\end{aligned}
\]

Radial integration by parts identifies the angular coefficient of \(F\) as
\(d_{k,j}''+4d_{k,j}'/r-a_kd_{k,j}/r^2\). Parseval now gives

\[
A_1[u]=\frac12\sum_{k,j}\int_0^R r^4
\left(d_{k,j}''+\frac4r d_{k,j}'-\frac{a_k}{r^2}d_{k,j}\right)^2dr,       \tag{16}
\]

and both \(A_1[u-u_N]\to0\) and \(\int\psi|u-u_N|^2\to0\).
For the smooth compact difference \(v_N=u-u_N\), ordinary ambient integration by parts and weighted Cauchy–Schwarz imply

\[
\int|\nabla_Gv_N|^2
=-\int v_NL_Gv_N
\le\left(\int\psi v_N^2\right)^{1/2}
   \left(\int\frac{(L_Gv_N)^2}{\psi}\right)^{1/2}
\longrightarrow0.
\]

The coefficient \(K=W+4/r^2\) is bounded on the common compact radial support, so \(D_{1,W}[u_N]\to D_{1,W}[u]\), including for sign-changing \(K\). For each finite sum, angular orthogonality and integration by parts give exactly

\[
D_{1,W}[u_N]=\frac12\sum_{k\le N,j}\int_0^R
\left(W+\frac4{r^2}\right)
\left(r^4d_{k,j}'^2+a_kr^2d_{k,j}^2\right)dr.             \tag{17}
\]

It therefore suffices to prove the nonnegative mode differences for the finite sums and pass to this verified limit. All integrations above are in the original ambient space; the axis has never been removed from the test class.

### The exact mode identity

For a compact smooth \(d\) and \(a=a_k\), subtract its term in (17) from its term in (16). Integration by parts yields

\[
\begin{aligned}
F_a[d]
&=q_\lambda[d']\\
&\quad+a\left\{2\int_0^Rr^2d'^2dr
+(a-2-\lambda)\int_0^Rd^2dr
+\int_0^Rr^{-2}d^2dr\right\}.                            \tag{18}
\end{aligned}
\]

For clarity, before substituting \(W=\lambda/r^2-r^{-4}\), the brace is

\[
2\int r^2d'^2+(a-2)\int d^2-\int Wr^2d^2.
\]

Indeed, the angular square and mixed terms contribute
\(2a\int r^2d'^2+(a^2+2a)\int d^2\); subtracting the angular part of the \(4/r^2\) correction leaves \(a(a-2)\int d^2\). This checks the dimension and correction exactly.

The elementary weighted Hardy identity is

\[
0\le\int_0^R\left(rd'+\frac12d\right)^2dr
=\int_0^Rr^2d'^2dr-\frac14\int_0^Rd^2dr.                 \tag{19}
\]

For \(a\ge4\), the brace in (18) is therefore at least

\[
\left(a-\frac32-\lambda\right)\int_0^Rd^2dr
+\int_0^Rr^{-2}d^2dr\ge0,                               \tag{20}
\]

using \(\lambda<12/5<5/2\). Also \(q_\lambda[d']\ge0\) by (12) and \(m[d']=0\). The zero mode satisfies \(F_0[d]=q_\lambda[d']\ge0\). More explicitly, the same calculation yields the manifest-square identity

\[
\boxed{\begin{aligned}
F_a[d]&=q_\lambda[d']
+2a\int_0^R\left(rd'+\frac12d\right)^2dr\\
&\quad+a\left(a-\frac32-\lambda\right)\int_0^Rd^2dr
+a\int_0^Rr^{-2}d^2dr.
\end{aligned}}                                           \tag{21}
\]

Thus every mode difference is nonnegative. Equations (16)–(17), first for finite sums and then by the convergence just proved, establish the all-test core (1).

The angular bound \(5/2\) here is a sufficient comparison threshold **conditional on the independently proved constrained radial positivity**. It is not asserted to be the sharp coefficient of a pure scale-invariant all-test inequality. That distinction prevents confusion with a different unconstrained scale-invariant angular quotient.

## 6. The precise endpoint obstruction

The side condition controls \(V\), but does not control the negative part of \(W\). Here \(V=1\) already satisfies the side condition exactly. A compact bump with prescribed ordinary integral, concentrated at scale \(\varepsilon\) near zero, can have small leading derivative energy \(\int r^4w'^2\). Nevertheless the negative potential \(-r^{-4}\) contributes \(+\int w^2\) to the Hardy form. It makes the ordinary mean continuous in the form topology, as (4) shows.

Consequently \(\ker m\) is closed and genuinely codimension one. It cannot be dense in the form domain, and the strictly positive principal mode is outside it. The choice \(\alpha<\lambda<\beta\) moves this principal mode below zero while leaving every derivative-of-compact-test mode nonnegative. The angular estimate preserves the all-function core.

This gives an explicit mechanism, rather than only a failure of a proof technique: the real-\(W\) branch permits endpoint confinement that hides one negative Hardy mode from the derivative test class. A density argument using only the \(V\)-energy cannot remove that obstruction.

## 7. Sources, diagnostics, and limitations

The source question is Roychowdhury's paragraph on printed p.606 / PDF p.28 of *Mini-Workshop: Hardy Inequalities in Discrete and Continuum Settings*, Oberwolfach Reports 14/2025. It points to a Hardy statement and a Hardy–Rellich statement but does not display the solution-free core as a separate quantified conjecture. [Official report](https://ems.press/content/serial-article-files/51358?nt=1), [DOI](https://doi.org/10.4171/OWR/2025/14).

The normalization, side condition, \(V'\) correction, and solution-dependent remainder are in Ganguly–Jotsaroop–Roychowdhury, *Hardy and Rellich identities and inequalities for Baouendi–Grushin operators via spherical vector fields*, arXiv:2404.05510v3, Theorem 1.3, p.7. Its polar integration and angular spectrum are in Section 2, pp.10–12, in particular Lemmas 2.1–2.3. The mode comparison is related to the source's symmetrization discussion, Theorem 6.3, pp.33–34; our proof supplies the required comparison directly and does not assume the positive Bessel solution. [Versioned primary PDF](https://arxiv.org/pdf/2404.05510v3).

The historical version v1 stated \(Q\ge3\), while v3 starts at \(Q\ge4\). This counterexample uses \(Q=5\) and makes no claim that the historical lower-dimensional angular-domain arguments follow automatically. [Historical primary PDF](https://arxiv.org/pdf/2404.05510v1).

The companion `check_rellich_counterexample.py` performs explicit runtime checks of the symbolic mode coefficient, threshold ordering, and finite-difference spectral diagnostics. Its checks use conditional exceptions, not Python assertions, and remain active under `python -O` and `python -OO`. `DIAGNOSTICS.json` records numerical evidence only. The exact proof does not depend on finite differences, log-domain truncation, computed eigenvalues, or their rounded values.

No claim is made about scholarly novelty, human peer review, or the entire informal source question. Raw third-party sources and private recovery material are not part of this authored artifact.
