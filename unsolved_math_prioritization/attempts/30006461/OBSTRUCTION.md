# The multiplication-table profile: a nonuniformity gap

**Outcome: unresolved after one Fourier-based approach.** This is a source audit and a collection of elementary obstruction controls. The Fourier reduction itself is established in the related primary literature; no new theorem about the actual multiplication-table profile or historical novelty is claimed.

## 1. Exact target, phase and source boundary

Let

\[
M(n)=\#\{ab:1\le a,b\le n\},\qquad
\delta=1-\frac{1+\log\log2}{\log2}.
\]

The original [OWR 51/2025 contribution, pp.2725–2727](https://ems.press/content/serial-article-files/52435), announces

\[
M(n)=(1+o(1))f_{\rm Mult}\!\left(\left\{\frac{\log\log n}{\log2}\right\}\right)
\frac{n^2}{(\log n)^\delta(\log\log n)^{3/2}}.
\tag{1}
\]

All unmarked logarithms are natural. The phase is \(\log_2(\log n)\), not \(\log_2 n\). On the circle \(\mathbb T=\mathbb R/\mathbb Z\), the report writes

\[
G(x)=\sum_{j\in\mathbb Z}(\log2)^{x+j}
                 (1-e^{-2^{x+j}}),\qquad
f_{\rm Mult}=\mu*\mu'*G,
\tag{2}
\]

for two specific positive measures, and conjectures

\[
\frac{\max_{x\in\mathbb T}f_{\rm Mult}(x)}
     {\min_{x\in\mathbb T}f_{\rm Mult}(x)}>1.
\tag{3}
\]

This is strict nonconstancy of the fixed profile, not a lower bound on its amplitude of a prescribed size. The source gives the upper ratio bound \(<1+2\cdot10^{-7}\). Its displayed definition of \(M(n)\) has \(x\in[n]\), inconsistent with the immediately following prose identifying the entire \(n\)-by-\(n\) multiplication table. The standard set of products above follows that explicit prose; the discrepancy was checked on the rendered original page.

The full [Green–Sawhney manuscript, arXiv:2604.28116v1](https://arxiv.org/abs/2604.28116v1), concerns the **permutation** profile \(f_{\rm Perm}\), with phase \(\{\log_2 k\}\), and says that the multiplication-table paper is forthcoming. Theorem 1.1 and Propositions 1.3–1.4 describe its own measures through Poisson and subset-sum limits. Those measures have not been identified here with the measures in (2). Moreover, its kernel is \(g(x)=G(-x)\), and a positive scalar \(c_0\) occurs in its profile formula. Reflection and positive scaling do not affect constancy, but they must not be suppressed when comparing formulas.

The OWR announcement is the source of (1)–(2). No complete proof of that multiplication-table announcement, or later resolution of (3), was located in this bounded source search. The present attempt does not certify the announced asymptotic independently and does not substitute the proved permutation model for it.

## 2. The known Fourier reduction, with the source sign convention

Set

\[
a=\frac{\log\log2}{\log2}\in(-1,0),\qquad
\widehat\nu(m)=\int_{\mathbb T}e^{-2\pi imx}\,d\nu(x).
\]

The kernel \(G\) is strictly positive and smooth. For example, its defining sum and every differentiated sum converge locally uniformly: the positive-index tail decays geometrically, while the negative-index tail has decay controlled by \((2\log2)^{x+j}\). Unfolding the periodization and substituting \(u=2^t\) gives

\[
\widehat G(m)=\frac1{\log2}\int_0^\infty
 u^{a-2\pi im/\log2-1}(1-e^{-u})\,du
=-\frac1{\log2}\Gamma\!\left(a-\frac{2\pi im}{\log2}\right).
\tag{4}
\]

For completeness, if \(-1<\Re s<0\), integration by parts gives
\(\int_0^\infty u^{s-1}(1-e^{-u})du=-\Gamma(s+1)/s=-\Gamma(s)\);
both boundary terms vanish. The gamma function has no zeros, and the arguments in (4) are not its poles. Thus \(\widehat G(m)\ne0\) for every integer \(m\). This is the reflected version of **Green–Sawhney Lemma 10.1**, not a new discovery.

Let \(A=\mu(\mathbb T)>0\), \(B=\mu'(\mathbb T)>0\), and normalize to probability measures \(\nu=\mu/A\), \(\nu'=\mu'/B\). The finite positive measures in the profile formula then give

\[
\widehat f_{\rm Mult}(m)=AB\,\widehat G(m)\widehat\nu(m)\widehat{\nu'}(m).
\tag{5}
\]

Consequently

\[
f_{\rm Mult}\text{ is constant}
\quad\Longleftrightarrow\quad \nu*\nu'=h,
\tag{6}
\]

where \(h\) is normalized Haar measure on \(\mathbb T\). Indeed, the nonzero coefficients in (5) vanish exactly when those of \(\nu*\nu'\) vanish. A probability measure with that Fourier sequence equals Haar measure, since trigonometric polynomials are dense in the continuous functions. Green–Sawhney already record this reduction for their permutation model in the remarks after Theorem 1.1.

Thus the missing certificate is a **common** nonzero Fourier mode:

\[
\exists m\in\mathbb Z\setminus\{0\}:
\widehat\nu(m)\ne0\quad\hbox{and}\quad\widehat{\nu'}(m)\ne0.
\tag{7}
\]

The nonconstancy of the universal kernel establishes neither factor in (7).

## 3. Why positivity and separate nonuniformity do not close the gap

Here is an exact negative control on the attempted inference. For distinct positive integers \(r,s\) and nonzero real \(b,c\) with \(|b|,|c|<1\), define

\[
d\nu_b(x)=(1+b\cos(2\pi r x))\,dx,\qquad
d\eta_c(x)=(1+c\cos(2\pi s x))\,dx.
\]

Both densities are smooth, strictly positive and nonconstant, and both measures have total mass one. Their nonzero Fourier supports outside zero are respectively \(\{-r,r\}\) and \(\{-s,s\}\). These are disjoint, so

\[
\nu_b*\eta_c=h,\qquad \nu_b*\eta_c*G=\widehat G(0).
\tag{8}
\]

Therefore even proving that each actual boundary measure is individually nonuniform would not, by itself, prove (3). One needs the shared-mode information in (7), or another argument excluding a Haar convolution. These illustrative measures are **not claimed** to be the multiplication-table measures or a counterexample to (3).

## 4. Why finite nonconstant approximants do not suffice

Let

\[
\lambda_q=\frac1q\sum_{j=0}^{q-1}\delta_{j/q}.
\]

Then \(\widehat\lambda_q(m)=1\) when \(q\mid m\), and zero otherwise. Hence \(G*\lambda_q\) is nonconstant for every finite \(q\), because its Fourier coefficient at \(m=q\) is \(\widehat G(q)\ne0\). Nevertheless

\[
G*\lambda_q\longrightarrow\widehat G(0)
\quad\hbox{uniformly as }q\longrightarrow\infty.
\tag{9}
\]

To see this without any asymptotic guess, partition the circle into \(q\) equal intervals. For every Lipschitz function \(\varphi\), the difference between its integral and the left-endpoint average has absolute value at most \(\operatorname{Lip}(\varphi)/(2q)\). Apply this to \(\varphi_x(t)=G(x-t)\), uniformly in \(x\). Thus discrete approximants and visible nonzero coefficients at every finite stage do not certify a nonconstant limit.

A valid quantitative route would require rigorous errors on the **actual** measures. For example, suppose at one fixed nonzero mode \(m\) that certified complex approximations satisfy

\[
|\widehat\nu(m)-z|\le\varepsilon,
\qquad |\widehat{\nu'}(m)-z'|\le\varepsilon',
\qquad |z|>\varepsilon,\quad |z'|>\varepsilon'.
\]

Then (7) follows. More quantitatively, writing \(\operatorname{osc}(f)=\max f-\min f\), one has
\(|\widehat f(m)|\le\operatorname{osc}(f)/2\), by subtracting the midpoint of the range. Since \(\min f\le\int f\), equations (4)–(5) imply

\[
\frac{\max f_{\rm Mult}}{\min f_{\rm Mult}}
\ge 1+\frac{2|\widehat G(m)|}{\widehat G(0)}
 (|z|-\varepsilon)(|z'|-\varepsilon')>1.
\tag{10}
\]

No such pair of certified bounds has been obtained here. In the permutation paper, the explicit limit descriptions themselves involve subset sums with exponential known enumeration cost, and convergence bounds use asymptotic constants and small exponents. The statement of a limit is not a certified finite-stage error. More fundamentally, using those permutation measures in (10) would first require a justified connection to the arithmetic measures in (2). No such connection has been proved in this attempt. No Monte Carlo estimate is offered as a replacement.

## 5. A normalization consequence, conditional on the announced asymptotic

Define

\[
R(n)=\frac{M(n)(\log n)^\delta(\log\log n)^{3/2}}{n^2}.
\]

Assuming (1), the cluster set of \(R(n)\) is exactly
\([\min f_{\rm Mult},\max f_{\rm Mult}]\). Indeed, \(R(n)-f_{\rm Mult}(\{\log_2\log n\})\to0\). For every phase \(t\in[0,1)\), the integers
\(n_j=\lfloor\exp(2^{j+t})\rfloor\) have phases converging to \(t\) on the circle. Continuity gives every value of the profile as a subsequential limit. Conversely, compactness of the circle gives a convergent phase subsequence for every convergent subsequence of \(R(n)\).

It follows that (3) is equivalent to nonconvergence of \(R(n)\), and its ratio is \(\limsup R(n)/\liminf R(n)\). This elementary consequence fixes the exact quantifiers; it is not a proof of the required strict inequality. A finite multiplication table or an unquantified \(o(1)\) term does not determine these limiting extrema.

## 6. Disposition

The attempted Fourier route stops at (7). The negative controls show why kernel nonconstancy, positive measures, separate nonuniformity, and finite-stage nonconstant approximants cannot replace it. The imported full permutation result is useful prior mathematics, but is a different profile theorem.

The exact checker verifies the elementary rational Fourier controls and root-of-unity cancellation; it does not compute either arithmetic measure or decide the target. The full multiplication-table nonconstancy question remains **unsolved in this attempt**. Further progress would require additional rigorous information about the actual arithmetic boundary measures or a direct argument about their convolution, not another assertion that the known reduction is a solution.
