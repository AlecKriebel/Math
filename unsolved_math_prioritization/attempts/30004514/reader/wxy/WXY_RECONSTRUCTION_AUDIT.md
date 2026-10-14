# Supplementary reconstruction of the Wang-Xiong-Yang counterexamples

Date: 14 October 2026. Subject: centroid-preserving hyperplane sections in every dimension at least three.

## Result and scope

The proof in Shouda Wang, Ge Xiong, and Kaiwen Yang, *A complete solution to the Grünbaum-Loewner centroid problems*, [arXiv:2606.19865v2](https://arxiv.org/abs/2606.19865v2), was read in full. Its main construction has been independently reconstructed below, including the low-dimensional cases, the spectral normalization, the exact centroid constraint, and the stability argument. No substantive mathematical obstruction was found in this verification. The result is credited entirely to those authors.

This is an authored proof audit, not a journal acceptance, formal proof-assistant certificate, or assertion that all cited literature was re-proved. The manuscript remains a submitted preprint: its July 31, 2026 version and three-author attribution must be preserved. The pivotal calculation quoted from Rubin is reconstructed here rather than accepted solely on that citation. Standard spherical harmonic decomposition, the Funk-Hecke theorem, Sobolev embedding on a compact sphere, and elementary differential calculus remain explicit background prerequisites.

The universal queued question was already answered negatively by the earlier Myroshnychenko-Tatarko-Yaskin examples in dimensions at least five, published in [Advances in Mathematics 461 (2025), 110081](https://doi.org/10.1016/j.aim.2024.110081). Consequently, acceptance or rejection of this supplementary all-dimensional audit does not determine the negative disposition of that universal question. The contribution of this supplementary result is coverage of dimensions three and four and an especially transparent perturbative mechanism.

## 1. Exact geometric reduction

Let a positive radial function on the unit sphere define

\[
K_\rho=\{ru: u\in S^{n-1},\ 0\le r\le\rho(u)\}.
\]

Write \(d\sigma_j\) for ordinary Euclidean surface measure on \(S^j\), and define the unnormalized hemisphere operator

\[
(Tq)(u)=\int_{\theta\cdot u\ge0}q(\theta)\,d\sigma_{n-1}(\theta).
\]

For a body with centroid zero, its half-space volume is

\[
A_K(u)=\frac1n T(\rho^n)(u).
\]

For a tangent vector \(v\perp u\), differentiation of the moving hemisphere gives

\[
D_vA_K(u)=\frac1n\int_{S^{n-1}\cap u^\perp}
 (\theta\cdot v)\rho(\theta)^n\,d\sigma_{n-2}(\theta)
=\int_{K\cap u^\perp}x\cdot v\,d\mathcal H^{n-1}(x).
\]

The sign is positive: replacing \(u\) by \(u+sv\) admits an infinitesimal band of width \(s\theta\cdot v\) into the positive hemisphere. The factor \(1/n\) agrees with the section moment, whose polar radial integral is \(\int_0^\rho r^{n-1}\,dr\). In particular, it is not a section-volume or half-body-centroid condition.

The section moment is a vector in \(u^\perp\), so its pairing with every tangent vector vanishes exactly when the moment itself is zero. Since \(K\) contains a ball about zero, all these central sections have positive induced \((n-1)\)-volume. Thus critical points of \(A_K\) are precisely the unit normals of centroid-preserving central sections.

Finally \(A_K(-u)=\operatorname{vol}_n(K)-A_K(u)\). Critical points occur in antipodal pairs, and each pair gives one unoriented geometric hyperplane. An affine hyperplane whose section centroid is zero necessarily contains zero: the average of points in an affine hyperplane remains in that hyperplane. There are consequently no additional noncentral sections to count.

This verifies the target interpretation used in WXY Lemma 2.1 and the last paragraph of its theorem proof. For their smooth constructed examples the displayed calculation is direct. The extension to arbitrary convex bodies used for the universal lower bound follows from the same moving-hemisphere formula with continuous positive radial data; it is also the established result cited in their Lemma 2.1.

## 2. The weighted twist exists and is genuinely smooth

Fix \(n\ge3\), and put

\[
w(t)=(1-t^2)^{(n-1)/2},\qquad
W=\int_0^1w(t)\,dt,\qquad
s(t)=W^{-1}\int_0^tw(\tau)\,d\tau\quad(0\le t\le1).
\]

Choose a smooth step \(b\) that is zero on \(( -\infty,0]\), one on \([1,\infty)\), and rises smoothly between them. One explicit choice on \(0<z<1\) is

\[
b(z)=\frac{e^{-1/z}}{e^{-1/z}+e^{-1/(1-z)}}.
\]

The authored formula

\[
a(r)=\pi\bigl(b(6r-1)+b(6r-4)\bigr),\qquad 0\le r\le1,
\]

realizes the smooth graph required in WXY Lemma 3.7. It is zero near zero, equals \(\pi\) near \(1/2\), equals \(2\pi\) near one, and satisfies

\[
a(r+1/2)=a(r)+\pi\quad(0\le r\le1/2).
\]

Define \(\alpha(t)=a(s(|t|))\) on \([-1,1]\). Although absolute value is nonsmooth at zero, \(a\circ s\) is constant in a neighborhood of zero. Although \(w\), and thus \(s\), need not be smooth through the endpoint one in even ambient dimensions, \(a\circ s\) is constant near that endpoint too. The resulting even \(\alpha\) is therefore globally smooth, including in dimension four.

Changing variables from \(t\) to \(s\) proves the exact cancellation

\[
\int_{-1}^1 w(t)e^{i\alpha(t)}\,dt
=2W\int_0^1e^{ia(r)}\,dr=0.
\]

The last equality pairs \(r\) with \(r+1/2\); it is exact and requires no numerical approximation.

## 3. A two-critical-point function with zero first moment

Use coordinates \(u=(x_1,x_2,y,t)\), with \(y\in\mathbb R^{n-3}\). Rotate the \((x_1,x_2)\)-plane through angle \(\alpha(t)\), holding \(y,t\) fixed. Call this sphere map \(\Phi\). Its explicit inverse rotates through \(-\alpha(t)\), so it is a smooth diffeomorphism. Since \(\alpha\) is even, \(\Phi(-u)=-\Phi(u)\).

The function

\[
f(u)=x_1\cos\alpha(t)-x_2\sin\alpha(t)=x_1\circ\Phi(u)
\]

is smooth and odd. Composing a height function with a diffeomorphism preserves both its critical-point set up to inverse image and Hessian nondegeneracy. Thus \(f\) has exactly two nondegenerate critical points. For this particular phase, \(\alpha\) vanishes near \(t=0\), so these points are exactly \(\pm e_1\), with the usual height-function local maximum and minimum.

For the first moment, write

\[
u=(\sqrt{1-t^2}\,v,t),\qquad v\in S^{n-2}.
\]

The latitude Jacobian is

\[
d\sigma_{n-1}=(1-t^2)^{(n-3)/2}\,d\sigma_{n-2}(v)\,dt.
\]

For a horizontal coordinate \(u_i\), the product \(u_if(u)\) supplies two factors of \(\sqrt{1-t^2}\). Its integral is therefore a linear combination of the real and imaginary parts of the cancellation in Section 2, with the weight exponent \((n-1)/2\), and is zero. The altitude coordinate gives an odd function of \(t\), and also integrates to zero. Hence

\[
\int_{S^{n-1}}u f(u)\,d\sigma_{n-1}(u)=0.
\]

Equivalently, the degree-one spherical harmonic projection of \(f\) is zero. No change-of-variables assumption that \(\Phi\) preserves measure is needed in this argument; the moment is calculated in the original latitude coordinates.

### The dimensions three and four

- For \(n=3\), the \(y\)-coordinate is absent and the latitude fiber is \(S^1\). There are still two rotation coordinates and one independent altitude coordinate. Here \(W=2/3\) and \(s(t)=(3t-t^3)/2\).
- For \(n=4\), the fiber is \(S^2\), \(W=3\pi/16\), and
  \[
  s(t)=\frac{2}{3\pi}\left(3\arcsin t+t(5-2t^2)\sqrt{1-t^2}\right).
  \]
  The apparent endpoint nonsmoothness is removed by the phase plateau described above.

Nothing in the construction is a dimensional lifting from a five-dimensional example, and no non-intersection body is required. The mechanism needs the three coordinates just described, explaining the actual \(n\ge3\) restriction.

## 4. The hemisphere inverse: direct normalization check

WXY Lemma 3.1 quotes the hemisphere eigenvalue formula from Boris Rubin, [*Inversion and characterization of the hemispherical transform*, J. Anal. Math. 77 (1999), 105-128](https://doi.org/10.1007/BF02791259). The publisher record was checked, but that original article's full proof was not inspected in this lane. The required formula can instead be derived as follows.

Set \(\gamma=(n-2)/2>0\), and let \(C_m^\gamma\) be the Gegenbauer polynomial. Funk-Hecke, with unnormalized surface measure, gives the eigenvalue on spherical harmonics of degree \(m\):

\[
\lambda_m=
\frac{|S^{n-2}|}{C_m^\gamma(1)}
\int_0^1 C_m^\gamma(t)(1-t^2)^{\gamma-1/2}\,dt.
\]

The Gegenbauer differential equation has divergence form

\[
\frac{d}{dt}\left((1-t^2)^{\gamma+1/2}(C_m^\gamma)'(t)\right)
=-m(m+2\gamma)(1-t^2)^{\gamma-1/2}C_m^\gamma(t).
\]

For \(m\ge1\), the boundary term at one vanishes and consequently

\[
\lambda_m=\frac{|S^{n-2}|(C_m^\gamma)'(0)}
 {m(m+n-2)C_m^\gamma(1)}.
\]

For odd \(m\), the elementary coefficients
\(C_m^\gamma(1)=(2\gamma)_m/m!\) and
\((C_{2k+1}^\gamma)'(0)=2\gamma(-1)^k(\gamma+1)_k/k!\)
give

\[
\lambda_1=\frac{|S^{n-2}|}{n-1},\qquad
\frac{\lambda_{m+2}}{\lambda_m}=-\frac{m}{m+n}.
\]

The base value and recurrence yield exactly

\[
\lambda_m=\pi^{(n-2)/2}(-1)^{(m-1)/2}
\frac{\Gamma(m/2)}{\Gamma((m+n)/2)}\quad(m\text{ odd}).
\]

Every odd eigenvalue is nonzero, and its reciprocal grows only like \(m^{n/2}\). The first eigenvalue is the volume of the unit ball in \(\mathbb R^{n-1}\), so the degree-one normalization agrees independently with integrating a coordinate function over a hemisphere.

If \(f=\sum f_{m,k}Y_{m,k}\) is smooth and odd, define
\(h_{m,k}=f_{m,k}/\lambda_m\) in odd degrees, with all even coefficients zero. Smoothness of \(f\) implies square-summable coefficients with arbitrary polynomial weights. Polynomial growth of \(\lambda_m^{-1}\) preserves this property. The sphere's Sobolev characterization and embedding therefore give \(h\in C^\infty\). The bounded integral operator \(T\) has \(Th=f\) first in \(L^2\), then pointwise by continuity. This also verifies convergence, rather than treating an infinite expansion as only formal algebra.

Since \(\lambda_1\ne0\), the absence of a degree-one component passes from \(f\) to \(h\). Thus

\[
Th=f,\qquad h\text{ smooth and odd},\qquad \int u h(u)\,d\sigma_{n-1}(u)=0.
\]

## 5. The needed operator bound is a same-order bound

The inverse need not be bounded from \(C^2\) to \(C^2\); no such assertion is used. It is applied once to the fixed smooth \(f\). The perturbation calculation uses only boundedness of the forward transform \(T:C^2\to C^2\).

This forward bound has a short direct verification. On each sufficiently small sphere chart choose a smooth rotation \(R(u)\) carrying a fixed pole to \(u\). Then

\[
Tq(u)=\int_{\theta\cdot e_n\ge0}q(R(u)\theta)\,d\sigma_{n-1}(\theta).
\]

Differentiation up to any fixed order occurs inside an integral over a fixed compact hemisphere. On a finite atlas the derivatives of these rotations are bounded, yielding \(\|Tq\|_{C^k}\le C(n,k)\|q\|_{C^k}\). This independently checks the content of WXY Lemmas 3.2-3.3 without having to differentiate an indicator distribution repeatedly.

The paper's compact-group proof was also checked. Right-invariant differentiation commutes with the right translations \(\xi\mapsto\xi\eta\) used there. A bound with coefficient exactly the measure's mass uses the norm defined by that invariant frame; an arbitrary equivalent \(C^k\) norm merely changes the harmless multiplicative constant. The theorem needs only boundedness.

## 6. Exact centroid and global strict convexity

Take the smooth \(h\) above and set

\[
\rho_\varepsilon(u)=(1+\varepsilon h(u))^{1/(n+1)}.
\]

For all sufficiently small positive \(\varepsilon\), its base is positive. The resulting radial set is bounded, closed, and contains a positive-radius Euclidean ball. Its boundary is a smooth embedded radial graph.

Polar integration gives an exact, not asymptotic, moment identity:

\[
\int_{K_\varepsilon}x\,dx
=\frac1{n+1}\int_{S^{n-1}}u\rho_\varepsilon(u)^{n+1}\,d\sigma_{n-1}
=\frac1{n+1}\int u(1+\varepsilon h(u))\,d\sigma_{n-1}=0.
\]

Its volume is positive, hence its ordinary volume centroid is exactly zero. The exponent \(1/(n+1)\), rather than \(1/n\), is essential for this exact cancellation.

The radial function tends to one in \(C^2\). The paper's second-fundamental-form expression is positive definite for a sufficiently small perturbation of the sphere. For an explicit local-to-global justification, put \(q=1/\rho_\varepsilon\) and define the positively homogeneous gauge
\(p(x)=|x|q(x/|x|)\), with \(p(0)=0\). On tangent vectors at a unit vector, its Hessian is

\[
D^2p|_{u^\perp}=\nabla_S^2q+q\,g_S.
\]

This is positive definite because \(q\) is \(C^2\)-close to one; the radial direction is the Hessian kernel. Every line not passing through zero therefore has convex restriction. Across zero the one-sided slopes have the correct ordering because \(q\) is positive. Thus \(p\) is globally convex and \(K_\varepsilon=\{p\le1\}\) is a convex body. Positive tangential Hessian gives positive curvature, and no nontrivial boundary segment can occur. This establishes strict convexity globally, not only positivity of a local formula.

The amount by which \(\varepsilon\) must be reduced may depend on the fixed dimension and on the constructed function. The assertion is existence separately in each dimension; it requires no dimension-uniform bound.

## 7. Stability preserves exactly one hyperplane

Taylor expansion in \(C^2\) gives

\[
(1+\varepsilon h)^{n/(n+1)}
=1+\frac{n}{n+1}\varepsilon h+R_\varepsilon,
\qquad \|R_\varepsilon\|_{C^2}=O(\varepsilon^2).
\]

All derivatives involved are bounded because the smooth scalar power is evaluated on a fixed positive interval and \(h\) is fixed and smooth. Applying the forward transform bound gives

\[
A_{K_\varepsilon}=
\frac{|S^{n-1}|}{2n}+\frac{\varepsilon}{n+1}f
+\frac1nTR_\varepsilon.
\]

Consequently

\[
g_\varepsilon:=\frac{n+1}{\varepsilon}
\left(A_{K_\varepsilon}-\frac{|S^{n-1}|}{2n}\right)
\longrightarrow f\quad\text{in }C^2.
\]

The constant subtracted need not equal half the perturbed body's actual volume; additive constants have no effect on critical points. The error after division by \(\varepsilon\) is \(O(\varepsilon)\), exactly as required.

WXY Lemmas 3.5-3.6 prove stability of the number of critical points, not merely the openness of the Morse property. Their proof was checked: local existence uses the implicit function theorem and an open-and-closed continuation argument with nonzero boundary gradients; local uniqueness follows from the invertible limiting Hessian; the compact complement supplies a positive lower bound for the gradient and rules out other critical points.

For this specific function an even simpler independent argument is available. Around \(+e_1\) and \(-e_1\), where \(\alpha\) vanishes, \(f\) is the usual height function and has strictly negative and strictly positive definite local Hessians, respectively. Choose disjoint small coordinate balls and a positive difference between the critical value and boundary values. A sufficiently small \(C^2\) perturbation preserves definite Hessians, and a sufficiently small \(C^0\) perturbation ensures an interior extremum in each ball. Definite Hessians make each extremum unique. Outside the balls, compactness gives a positive gradient lower bound, preserved under \(C^1\) perturbation. Thus \(g_\varepsilon\), and hence \(A_{K_\varepsilon}\), has exactly two critical points.

By Section 1, the two points form one antipodal pair and yield exactly one hyperplane whose induced section centroid is the body's volume centroid. This completes the all-dimensional construction.

## 8. Coverage of the rest of the manuscript

- Pages 1-3: definitions, exact claim, authorship, distinction from the arbitrary-interior-point question, and outline checked.
- Pages 4-6: the derivative-to-section-moment identity, elementary existence of at least one centroidal section, hemisphere formula, harmonic first-moment interpretation, radial convexity and Taylor estimates checked. The global convexity step was made explicit above.
- Pages 7-8: the planar supplement was read and checked. Its lower bound uses the anti-periodic radial difference with zero first moment to force at least three antipodal zero pairs; its equilateral-triangle upper bound permits only the three side-parallel chord directions. These planar statements are not needed for the \(n\ge3\) counterexamples.
- Pages 8-11: odd spectral inversion and forward \(C^k\) boundedness checked and independently reconstructed above.
- Pages 12-14: local and compact-manifold critical-count stability checked, with a simpler sufficient argument given above for the constructed function.
- Pages 14-16: phase cancellation, smoothness at the two latitude endpoints, the odd twist diffeomorphism, and every first-moment weight checked.
- Pages 16-17: positivity, regularity, exact centroid, rescaled \(C^2\) approximation, and unoriented affine-hyperplane counting checked.
- Page 18: reference identities consulted; this is not a claim to have read all 23 cited works.

All 18 pages were inspected through the local PDF's extracted text. Pages 9 and 14-17 were additionally rendered and inspected visually to verify the eigenvalue, phase graph, latitude powers, and final scaling formulas.

## 9. Verification limits and diagnostic evidence

The source PDF inspected was 407327 bytes, SHA-256 `21e91319797e8d4b5ececf4d4d8c4c4cc1814bd47422edeb9a3e3ffdfff8b53e`, labeled arXiv:2606.19865v2, July 31, 2026, 18 pages. No claim of journal publication is made.

The companion authored script `verify_normalizations.py` performs 80 exact symbolic checks of the eigenvalue normalization, for dimensions 3 through 10 and odd harmonic degrees 1 through 19. It also checks the two displayed low-dimensional latitude primitives symbolically. Numerical quadrature checks the explicitly defined phase cancellation in dimensions 3, 4, 5, and 8; the maximum observed residual was approximately \(1.50\times10^{-15}\). Results are in `NORMALIZATION_CHECKS.json`.

Those finitely many checks are diagnostics, not the proof of an infinite-dimensional assertion. The general recurrence, smooth inversion argument, exact phase cancellation, and compact perturbation argument above supply the mathematical justification. No numerical body, explicit admissible value of \(\varepsilon\), or finite spectral truncation is asserted to be the counterexample itself.

The remaining prerequisites are standard harmonic and differential analysis, identified explicitly in Section 1 and Sections 4-7. The full original proofs in Rubin's 1999 article, the cited spherical-harmonic books, and every historical reference were not independently audited. The submitted-preprint publication status is unaffected by a successful mathematical reconstruction.

## Recommended use

It is supported to say that the WXY submitted preprint gives an all-dimensional counterexample construction whose main proof has passed this independent reconstruction, including dimensions three and four, subject to the standard prerequisites stated here. It is not supported to call the paper journal-verified, to attribute its theorem to this audit, or to claim formal proof certification. The already-published higher-dimensional MTY result remains sufficient for the original universal question.
