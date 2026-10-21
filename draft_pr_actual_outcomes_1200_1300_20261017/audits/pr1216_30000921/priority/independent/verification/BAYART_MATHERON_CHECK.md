# Independent check: Bayart–Matheron v1 Gaussian specialization

Checkpoint: **2026-10-17 18:34 UTC**. Assigned verification completion: **100%**. This separately authorized cross-challenge was checked without reading any sibling priority report. The earlier frozen VERIFICATION.md was not modified. No Git, publication, or outreach action was taken.

**Verdict: VALID.** Proposition 3.3 of Bayart–Matheron, *Mixing operators and small subsets of the circle*, arXiv:1112.1289v1, implies that differentiation on \(H(\mathbb C)\) is strongly mixing with respect to the **exact law**
\[
F(z)=\sum_{n\ge0}g_n\frac{z^n}{n!},
\qquad g_n\ \text{IID with density }\pi^{-1}e^{-|w|^2}.
\]
Consequently this Gaussian series is almost surely frequently hypercyclic. There is no Banach-space restriction, normalization discrepancy, or independence gap in this specialization.

## Source anchors

The [official v1 record](https://arxiv.org/abs/1112.1289v1) dates submission to **6 December 2011, 14:35:24 UTC**. The [official v1 PDF](https://arxiv.org/pdf/1112.1289v1) and supplied local text were checked. Page numbers below are printed PDF page numbers, also the one-based file pages.

- **pp. 1–2:** Fréchet-space setting; the full-support ergodic-measure implication for almost-sure frequent hypercyclicity is already discussed.
- **p. 8:** Definition 2.1; \(c_0(\mathbb Z_+)\)-mixing is strong mixing.
- **p. 11:** Section 3 explicitly fixes a separable complex Fréchet space.
- **p. 12:** Standard complex Gaussian normalization, the definition of \(\mu_K\), and a sufficient summability criterion for gamma-radonifying operators.
- **p. 13:** Gaussian support equals the closed span of the series vectors; dense range of \(K\) gives full support.
- **p. 14:** Formula (3.1), \(K_E f=\int fE\,dm\), the dense-range / \(m\)-spanning equivalence, Definition 3.2, and the correct identity \(TK_E=K_EM_\phi\).
- **pp. 14–15:** Proposition 3.3, with its conclusion specifically identifying the measure \(\mu_{K_E}\).

Local input SHA-256:

    bayart_matheron2011v1.pdf 876a1afbb75181a96e91d262468ef397b4beb3b73ec3e949df4e88c86efb16bd
    bayart_matheron2011v1.txt 87d72239f49f84b66d44750401df4d4d41683ba25f5cfb623358cc4b9e82265f

## Complete specialization

Set \(X=H(\mathbb C)\), with \(p_R(h)=\sup_{|z|\le R}|h(z)|\), and \(T=D\). This is a complex separable Fréchet space: integer-radius seminorms give its complete topology and polynomials with rational real and imaginary coefficients form a countable dense set. Cauchy's estimate gives \(p_R(Dh)\le p_{R+1}(h)\), so \(D\) is continuous.

Let \(\Omega=\mathbb T\), with its Borel sigma-algebra and normalized Haar probability \(dm=d\theta/(2\pi)\). This is a standard finite measure space with separable \(L^2(m)\). Define
\[
\phi(\lambda)=\lambda,\qquad E(\lambda)(z)=e^{\lambda z}.
\]
The map \(E:\mathbb T\to H(\mathbb C)\) is continuous; indeed
\[
p_R(E(\lambda)-E(\eta))\le R e^R|\lambda-\eta|.
\]
Also \(p_R(E(\lambda))\le e^R\), so \(E\) is measurable and square integrable in every continuous seminorm. Thus it is a vector field in the source's Fréchet-space sense. The eigenfield identity is exact:
\[
DE(\lambda)=\lambda E(\lambda)=\phi(\lambda)E(\lambda).
\]

For \(f\in L^2(m)\), define
\[
(K_Ef)(z)=\int_{\mathbb T}f(\lambda)e^{\lambda z}\,dm(\lambda).
\]
This vector integral exists: \(f\in L^1(m)\), the exponential series converges uniformly on \(\mathbb T\times\{|z|\le R\}\), and termwise integration produces an entire function. Moreover
\[
p_R(K_Ef)\le e^R\|f\|_1\le e^R\|f\|_2.
\]
This proves continuity of the integral operator directly, without requiring a Banach-valued integration theorem or an extra geometric hypothesis on \(H(\mathbb C)\).

The Fourier functions \(e_k(\lambda)=\lambda^k\), \(k\in\mathbb Z\), are an orthonormal basis of \(L^2(m)\). Formula (3.1) is linear in \(f\) and contains **no complex conjugation**. Hence
\[
K_Ee_k
=\sum_{n\ge0}\frac{z^n}{n!}\int_{\mathbb T}\lambda^{n+k}\,dm(\lambda)
=
\begin{cases}
z^{-k}/(-k)!,& k\le0,\\
0,& k>0.
\end{cases} \tag{1}
\]
In particular, \(k=0\) contributes the constant \(1\), not a zero direction. Positive Fourier modes form the unused kernel directions. Choosing the conjugate Fourier basis would only reverse the indexing.

For every \(R\ge0\),
\[
\sum_{k\in\mathbb Z}p_R(K_Ee_k)
=\sum_{n\ge0}\frac{R^n}{n!}
=e^R<\infty. \tag{2}
\]
Every continuous seminorm on \(H(\mathbb C)\) is bounded by \(Cp_R\) for some \(C,R\), so (2) checks the full Fréchet summability criterion on p. 12. More directly, for independent standard complex Gaussian variables \((\gamma_k)_{k\in\mathbb Z}\),
\[
\mathbb E\sum_{n\ge0}|\gamma_{-n}|R^n/n!
=\mathbb E|\gamma_0|\,e^R<\infty.
\]
Apply this at countably many integer radii. The Gaussian series is almost surely absolutely convergent in every defining seminorm, and therefore converges in \(H(\mathbb C)\). This proves that \(K_E\) is gamma-radonifying. It also removes any concern about enumerating the two-sided Fourier basis as a one-sided sequence.

Every monomial \(z^n/n!\) belongs to the range of \(K_E\) by (1); indeed all polynomials belong to that range. Polynomials are dense in \(H(\mathbb C)\), so \(K_E\) has dense range. The p. 14 equivalence gives the required \(m\)-spanning property. Independently, removing a Haar-null set leaves a dense subset of \(\mathbb T\); continuity of \(E\) preserves its closed linear span after removal. The Gaussian support criterion on p. 13 gives full support of \(\mu_{K_E}\).

Choose \(S=c_0(\mathbb Z_+)\). This is a norm-closed ideal in \(\ell^\infty(\mathbb Z_+)\). For every complex \(f\in L^1(m)\), identity \(\phi\) gives
\[
\sigma_f=(fm)\circ\phi^{-1}=fm,
\qquad
\widehat{\sigma_f}(n)=\int_{\mathbb T}\lambda^{-n}f(\lambda)\,dm(\lambda)\longrightarrow0.
\]
The Fourier decay follows, for example, by approximating \(f\) in \(L^1\) by a trigonometric polynomial: the polynomial's sufficiently high Fourier coefficients vanish, while the error of each coefficient is at most the \(L^1\) error. It holds in both directions, so the choice of Fourier sign convention is immaterial. This checks Proposition 3.3(c) for **every** \(L^1\) density, including complex signed densities.

All three hypotheses of Proposition 3.3 are now verified. Its conclusion gives \(D\)-invariance and strong mixing for the specified measure \(\mu_{K_E}\), not merely for some unidentified full-support Gaussian measure. The nearby Banach-space assumptions in Proposition 3.1 concern optional type/cotype criteria; they are not assumptions of Proposition 3.3 and were not used.

## Exact law, normalization, and frequent hypercyclicity

By the p. 12 definition and (1),
\[
\mu_{K_E}
=\operatorname{Law}\!\left(\sum_{k\in\mathbb Z}\gamma_kK_Ee_k\right)
=\operatorname{Law}\!\left(\sum_{n\ge0}\gamma_{-n}\frac{z^n}{n!}\right).
\]
The source normalizes real and imaginary parts to variance \(1/2\), so \(\mathbb E|\gamma_k|^2=1\) and the density is \(\pi^{-1}e^{-|w|^2}\). Normalized Haar measure is important here: it makes the Fourier basis unit norm and gives no \(2\pi\) scale factor. Setting \(g_n=\gamma_{-n}\) proves **exact IID jets**, rather than only a covariance similarity:
\[
F^{(n)}(0)=g_n,\quad
\mathbb E[g_n\overline{g_m}]=\delta_{nm},\quad
\mathbb E[g_ng_m]=0.
\]
In particular,
\[
\mathbb E[F(z)\overline{F(w)}]
=\sum_{n\ge0}\frac{(z\bar w)^n}{(n!)^2},
\qquad
\mathbb E[F(z)F(w)]=0.
\]
The function-valued series is measurable as the almost-sure limit of its measurable partial sums in the metrizable space \(H(\mathbb C)\).

Strong mixing implies ergodicity. Take a countable basis \((U_j)\) of nonempty open subsets of \(H(\mathbb C)\). Full support gives \(\mu_{K_E}(U_j)>0\). Birkhoff's theorem, applied to each indicator and intersected over this **countable** basis, gives on one probability-one event
\[
\frac1N\#\{0\le n<N:D^nF\in U_j\}
\longrightarrow\mu_{K_E}(U_j)>0
\quad\text{for every }j.
\]
Every nonempty open set contains one of these basis elements, proving frequent hypercyclicity. No invertibility of \(D\) is needed. Pulling this measurable full-measure event back through the series map proves the almost-sure assertion for the IID Gaussian coefficients. Full support also makes these frequent hypercyclic functions dense.

As a separate consistency check, \(D\) shifts the IID jet sequence:
\[
D^rF(z)=\sum_{n\ge0}g_{n+r}z^n/n!.
\]
Finite coefficient cylinder events at sufficiently separated shifts are independent. Approximation by such cylinder events yields strong mixing of the coefficient shift and hence its image law, consistent with Proposition 3.3 and the law identification above.

## Qualifications

The extracted p. 17 proof contains an apparent intertwining typo, \(TM_\phi=M_\phi K_E\), whose operator domains do not match. The correctly typed identity \(TK_E=K_EM_\phi\) is already stated on p. 14 and follows directly here by differentiating the integral. This does not create a gap in the specialization.

This is a verified **specialization of a general theorem in the 2011 version**, followed by an explicit calculation and the ergodic theorem. It does not establish that the exact random differentiation example, polynomial obstruction, or annular construction was explicitly stated in that version. No later author-hosted PDF or later remark about Nikula was used to backdate any assertion. The currently served version-specific source and official submission record were checked; a byte-identical historical 2011 PDF was not independently authenticated.
