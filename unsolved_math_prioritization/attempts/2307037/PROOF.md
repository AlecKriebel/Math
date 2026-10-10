# A fixed-area exceptional set for positive squared-pole sums

**Target:** 2307037 / AMR-022-7037, Hayman–Lingham Problem 7.37.
**Status:** Complete affirmative deduction from established theorems, accepted by an independent internal AI-assisted mathematical audit. The manuscript and audit are unrefereed. This note makes no priority or novelty claim.

## Theorem

Let
\[
g(z)=\sum_{j=1}^{n}\frac{\lambda_j}{(z-z_j)^2},\qquad
z_j\in\mathbb C,\quad \lambda_j>0,\quad \sum_j\lambda_j=1.
\]
There is a compact set \(S=S(g)\subset\mathbb C\), of planar Lebesgue measure exactly \(\pi\), such that, simultaneously for every real \(R>1\),
\[
\int_{\{|z|<R\}\setminus S}|g(z)|\,dA(z)
\le 2\pi\log R+\pi(\log 2+e^{-1}). \tag{1}
\]
The integral in (1) is an ordinary nonnegative Lebesgue integral. In particular, it is finite. No restriction on the locations or separation of the poles is imposed.

## Two established inputs and conventions

Write \(D_r=\{z:|z|<r\}\), and use unnormalized planar area \(dA=dx\,dy\). The Beurling transform is normalized by
\[
Tf(z)=-\frac1\pi\operatorname{pv}\int_{\mathbb C}
                   \frac{f(w)}{(w-z)^2}\,dA(w).
\]
For an indicator of a bounded measurable set this is defined almost everywhere, for example through its standard \(L^2\) realization. At a point outside the closure of its support, the integral is absolutely convergent and needs no principal value.

**Input A (Eremenko–Hamilton).** For every measurable \(E\subset D_1\),
\[
\int_{D_1\setminus E}|T1_E|\,dA
\le |E|\log\frac\pi{|E|}. \tag{2}
\]
Use the continuous value zero when \(|E|=0\). The displayed estimate occurs on printed page 2794 of [EH], following Theorem 1; its proof ends on page 2797. The authors state it for a compact ambient set of logarithmic capacity one, which includes the closed unit disk. Boundaries of disks have zero area, so the open-disk version above follows. There is no additive term in this input.

**Input B (quadrature set from positive masses).** Given finitely many points \(a_j\in\mathbb R^2\) and positive numbers \(m_j\), let \(B_j\) be the open disk of area \(m_j\) centered at \(a_j\). Their smash sum \(\Omega=B_1\oplus\cdots\oplus B_n\) is a bounded open set containing every \(B_j\), with
\[
|\partial\Omega|=0,\qquad |\Omega|=\sum_jm_j,
\qquad
\int_\Omega h\,dA=\sum_jm_jh(a_j) \tag{3}
\]
for every real-valued integrable harmonic function \(h\) on \(\Omega\). Connectedness is not required. These facts follow from [LP]: definition (4), Proposition 2.12, Corollary 2.13, Lemma 2.15, Lemma 6.1, and Proposition 6.6. Proposition 6.6 states the corresponding inequality for integrable superharmonic functions; apply it to \(h\) and \(-h\) to obtain (3).

For clarity about regularity assumptions in this application: finite sums of disk indicators are bounded, compactly supported and continuous almost everywhere, and take only nonnegative integer values. Thus they satisfy Proposition 2.12's density-gap hypothesis, with any fixed \(0<\lambda<1\). That proposition supplies a null boundary; Corollary 2.13 supplies area additivity. These facts allow iteration of the binary smash sum and Lemma 6.1. Boundedness follows from Lemma 2.15. There is no disjointness, smallness, connectedness or ambient-unit-disk hypothesis in these results.

## 1. Construct one exceptional set and identify its exterior field

First combine repeated poles, adding their positive coefficients. This leaves the rational function and its normalization unchanged. It also makes the list of poles and coefficients intrinsic to \(g\).

Apply Input B with \(a_j=z_j\) and \(m_j=\pi\lambda_j\). The disks \(B_j\) have radii \(\sqrt{\lambda_j}\). Set
\[
S=\overline\Omega.
\]
Because \(\Omega\) is bounded and \(|\partial\Omega|=0\), this set is compact and
\[
|S|=|\Omega|=\sum_j\pi\lambda_j=\pi. \tag{4}
\]
It contains an open neighborhood of each pole.

Fix \(z\notin S\). The function \(w\mapsto(w-z)^{-2}\) is holomorphic on a neighborhood of \(\overline\Omega\), bounded there, and hence integrable on \(\Omega\). Its real and imaginary parts are harmonic. Applying (3) to both parts gives
\[
\int_\Omega\frac{dA(w)}{(w-z)^2}
 =\sum_j\frac{\pi\lambda_j}{(z_j-z)^2}
 =\pi g(z).
\]
The last equality uses \((z_j-z)^2=(z-z_j)^2\). Consequently
\[
T1_\Omega(z)=-g(z)\qquad (z\in\mathbb C\setminus S). \tag{5}
\]
This is a pointwise equality of absolutely convergent integrals on the entire complement of \(S\), not just the unbounded component. No boundary differentiation or principal-value interpretation of \(g\) is used.

The set \(S\) is now fixed, before any radius \(R\) is selected.

## 2. A localization bound for an arbitrary finite-area set

Scaling (2) gives, for a measurable \(E\subset D_L\) of area \(a\),
\[
\int_{D_L\setminus E}|T1_E|\,dA
\le a\log\frac{\pi L^2}{a}. \tag{6}
\]
Indeed, under \(z=L\zeta\), the degree-minus-two kernel and the area element cancel, giving \(T1_E(L\zeta)=T1_{E/L}(\zeta)\); integrating contributes the remaining factor \(L^2\).

Fix any \(R>1\), and put
\[
L=\sqrt2R,\qquad E=\Omega\cap D_L,\qquad
F=\Omega\setminus D_L,\qquad a=|E|.
\]
Then \(0\le a\le\pi\) and \(|F|=\pi-a\). On \(D_R\setminus S\) all relevant kernels are absolutely integrable, so (5), linearity and the triangle inequality imply
\[
\int_{D_R\setminus S}|g|\,dA
\le \int_{D_R\setminus S}|T1_E|\,dA
   +\int_{D_R\setminus S}|T1_F|\,dA. \tag{7}
\]
Since \(D_R\setminus S\subset D_L\setminus E\), the first term is at most
\[
a\log\frac{2\pi R^2}{a}. \tag{8}
\]

For the second term, a direct polar-coordinate calculation gives, whenever \(|w|=\rho>R\),
\[
\int_{D_R}\frac{dA(z)}{|z-w|^2}
=\int_0^R\frac{2\pi r}{\rho^2-r^2}\,dr
=\pi\log\frac{\rho^2}{\rho^2-R^2}. \tag{9}
\]
Here the angular integral is \(2\pi/(\rho^2-r^2)\), obtainable by the geometric-series expansion of the Poisson kernel. For every \(w\in F\), \(\rho\ge\sqrt2R\), so (9) is at most \(\pi\log2\). Tonelli's theorem and the defining normalization of \(T\) therefore give
\[
\begin{aligned}
\int_{D_R\setminus S}|T1_F|\,dA
&\le\frac1\pi\int_F\int_{D_R}\frac{dA(z)}{|z-w|^2}\,dA(w)\\
&\le (\pi-a)\log2. \tag{10}
\end{aligned}
\]
The separation \(L-R>0\) also directly justifies the ordinary-integral realization of \(T1_F\) throughout \(D_R\).

Combining (7)–(10) yields
\[
\begin{aligned}
\int_{D_R\setminus S}|g|\,dA
&\le a\log\frac{2\pi R^2}{a}+(\pi-a)\log2\\
&=2a\log R+\pi\log2+a\log\frac\pi a\\
&\le2\pi\log R+\pi\log2+\frac\pi e.
\end{aligned}
\]
For the last line, \(\log R>0\), \(a\le\pi\), and \(t\log(1/t)\le1/e\) on \([0,1]\), with the endpoint value defined by continuity. The latter inequality follows by differentiating \(-t\log t\), whose maximum occurs at \(t=e^{-1}\). This proves (1) for every \(R>1\) with the same set \(S\). Only the auxiliary decomposition of \(\Omega\) changes with \(R\). \(\square\)

## 3. The logarithmic coefficient cannot be decreased

Take \(g(z)=z^{-2}\). For any measurable \(S\) of area \(\pi\) and any \(R>1\),
\[
\int_{D_R\setminus S}|z|^{-2}\,dA\ge2\pi\log R. \tag{11}
\]
To verify this without assuming finiteness, write \(A=D_R\setminus D_1\). On \(D_1\), \(|z|^{-2}\ge1\); on \(A\), \(|z|^{-2}\le1\). Moreover,
\[
|S\cap A|\le|S\setminus D_1|=\pi-|S\cap D_1|=|D_1\setminus S|.
\]
Thus the integral gained on \(D_1\setminus S\) is at least the finite integral lost on \(S\cap A\), and
\[
\int_{D_R\setminus S}|z|^{-2}\,dA
\ge\int_A|z|^{-2}\,dA=2\pi\log R.
\]
This argument remains valid if the left side is infinite. Letting \(R\to\infty\) rules out any coefficient smaller than \(2\pi\) with a finite additive constant. We make no optimality claim for the additive constant in (1).

## References and scope of attribution

[EH] A. Eremenko and D. H. Hamilton, *On the area distortion by quasiconformal mappings*, Proceedings of the American Mathematical Society 123 (1995), 2793–2797. DOI: https://doi.org/10.1090/S0002-9939-1995-1283548-8 . Author-hosted PDF: https://www.math.purdue.edu/~eremenko/dvi/hamilt.pdf . The sharp transform estimate is their result, building on Astala's area-distortion theorem.

[LP] Lionel Levine and Yuval Peres, *Scaling limits for internal aggregation models with multiple sources*, Journal d'Analyse Mathématique 111 (2010), 151–219. DOI: https://doi.org/10.1007/s11854-010-0015-2 . Inspected author manuscript, May 1, 2009: https://lionellevine.github.io/scalinglimit.pdf . Versioned preprint: https://arxiv.org/abs/0712.3378v2 . The quadrature-set existence and regularity inputs are established results; the authors explicitly credit Sakai and the partial-balayage literature.

[HL] W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*, arXiv:1809.07200v2, Problem 7.37, PDF pages 172–173 (printed 171–172): https://arxiv.org/abs/1809.07200v2 .

The exact-target deduction above uses the extra quadrature construction and a localization argument. The downstream area-distortion theorem alone is not substituted for the squared-pole problem. Bounded searches do not certify that this combination is historically new or has never appeared elsewhere. This AI-assisted deduction has passed the independent internal mathematical audit in AUDIT.md. The manuscript and audit are unrefereed and have not undergone external human peer review.
