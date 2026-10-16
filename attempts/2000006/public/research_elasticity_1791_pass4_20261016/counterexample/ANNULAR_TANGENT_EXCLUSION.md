# E-6322, pass 4: stability under annular weighted blow-up convergence

Date: 2026-10-16. The frozen benchmark remains unchanged. No counterexample or proof of the full benchmark is claimed.

## 1. Main result

Let \(y\) be a full-class local \(W^{1,6}\) minimizer, or a global minimizer, for E-6322. Fix \(x_0\in\Omega\), and use its continuous representative to set \(y_0=y(x_0)\). Let

\[
A=\{z\in\mathbb R^3:1/2<|z|<2\}.
\]

There cannot exist positive exponents

\[
0<\alpha_1\le\alpha_2\le\alpha_3,\qquad s=\alpha_1+\alpha_2+\alpha_3>3,
\]

and a sequence \(r_k\downarrow0\) such that the componentwise weighted rescalings

\[
Y_{k,i}(z)=r_k^{-\alpha_i}\bigl(y_i(x_0+r_kz)-y_{0,i}\bigr)
\]

converge in \(C^1(\overline A)\) to

\[
U_i(z)=|z|^{\alpha_i}\phi_i(z/|z|),\qquad
\phi\in C^2(S^2;\mathbb R^3),
\]

with \(\det DU>0\) throughout \(\overline A\).

Here convergence in \(C^1\) includes that each sufficiently late \(Y_k\) belongs to \(C^1(\overline A)\). No regularity of \(y\) at \(x_0\), or on every intervening annulus, is assumed. The limit's strictly positive angular Jacobian is an explicit hypothesis.

This rules out such a tangent even along a subsequence. It is stronger than requiring a full weighted \(C^2\) asymptotic expansion: no convergence of second derivatives, no quantitative remainder rate, and no differentiation of an error term are required.

## 2. Finite energy restricts the exponents

Put \(m=\alpha_1\), \(\gamma=s-3\), and

\[
D_k=\operatorname{diag}(r_k^{\alpha_1-1},r_k^{\alpha_2-1},r_k^{\alpha_3-1}).
\]

At the physical point \(x_0+r_kz\),

\[
Dy=D_kDY_k,\qquad \det Dy=r_k^\gamma\det DY_k.
\]

The nonzero limiting first row supplies a constant \(c_0>0\) such that

\[
\int_{x_0+r_kA}|Dy|^6\,dx\ge c_0r_k^{6m-3}.
\]

The left side tends to zero by absolute continuity of the integral. Therefore \(m>1/2\); equality would leave a nonzero lower bound, and a smaller exponent would make it diverge.

Similarly, \(\det DY_k\) is uniformly bounded above and bounded away from zero on \(\overline A\), so

\[
\int_{x_0+r_kA}(\det Dy)^{-2}\,dx\ge c_1r_k^{3-2\gamma}
=c_1r_k^{9-2s}.
\]

Again this tends to zero, giving \(s<9/2\).

No disjointness of the annuli is needed: each lies in a ball whose radius tends to zero.

## 3. Weak Euler equations are justified on the rescaled annuli

For all sufficiently large \(k\), the physical map is \(C^1\) on \(x_0+r_k\overline A\) and its determinant has a positive minimum there. On the support of any smooth compactly supported additive variation, sufficiently small variation parameters preserve positive determinant. The gradients and their perturbed values remain in a compact subset of \(GL^+(3)\); differentiation of the energy is consequently justified.

Thus, with \(P(F)=DW(F)\), each row obeys the distributional equation

\[
\operatorname{div}_z\bigl[P(D_kDY_k)\bigr]_i=0\quad\text{in }A.
\]

This follows directly by rescaling the weak physical equation. We do not claim a classical Euler equation for \(y\) or \(Y_k\), nor use one across \(x_0\).

All limiting equations below are obtained by dividing the stress by a scalar power of \(r_k\), using uniform convergence of its coefficient fields, and passing against a fixed compactly supported test function. Second derivatives of the approximating maps never enter.

## 4. Barrier-dominated third-row range

Set

\[
\eta=2(3\alpha_1+\alpha_2+2\alpha_3-6).
\]

Assume first that \(\eta>0\). The third row of the barrier stress scales exactly as

\[
[P^{\rm bar}(D_kDY_k)]_3
=r_k^{\tau_3}\bigl[-2d(\det DY_k)^{-3}(\operatorname{cof}DY_k)_3\bigr],
\]

where

\[
\tau_3=\alpha_1+\alpha_2-2-3\gamma.
\]

The entire positive-energy third row is \(O(r_k^{4m+\alpha_3-5})\) uniformly on \(\overline A\). The exponent difference is precisely \(\eta\). Hence division by \(r_k^{\tau_3}\) and passage to the limit give

\[
\operatorname{div}\bigl[-2d(\det DU)^{-3}(\operatorname{cof}DU)_3\bigr]=0
\quad\text{in }A.
\]

This is impossible for the stated limit. The positive-degree argument from pass 2 supplies an angle \(\theta_0\) with \(\phi_1=\phi_2=0\). Along that ray, writing \(\det DU=r^\gamma j(\theta)\) and \((\operatorname{cof}DU)_3=\kappa r^{\alpha_1+\alpha_2-2}\theta_0\), the barrier divergence is

\[
6d\kappa\gamma j(\theta_0)^{-3}
 r^{\alpha_1+\alpha_2-3-3\gamma},
\]

whose coefficient is nonzero. Since the limit is \(C^2\), this pointwise contradiction also contradicts its weak equation on the annulus.

## 5. Strain-dominated first-row range

Assume \(\eta\le0\). The pass-3 exponent algebra gives

\[
\alpha_2>m,\qquad 1/2<m<1,\qquad s+3m<6.
\]

Divide the first stress row by \(r_k^{5m-5}\). Its sixth-power part converges uniformly to

\[
6a|\nabla U_1|^4\nabla U_1.
\]

The remaining parts vanish uniformly, with the following strictly positive relative exponents:

- correction from the other rows inside \(|F|^4p_1\): \(2(\alpha_2-m)\);
- cofactor-cubic stress: \(3(\alpha_2-m)\);
- determinant-square stress: \(2s-6m\);
- inverse-determinant stress: \(2(6-s-3m)\).

Thus

\[
\operatorname{div}(|\nabla U_1|^4\nabla U_1)=0\quad\text{in }A.
\]

The limit is exactly weighted-homogeneous. Homogeneity extends this scalar equation to every point of the punctured ball. The complete pass-3 scalar argument now applies:

- For \(1/2<m<3/5\), its spherical identity forces \(U_1=0\), contradicting positive determinant.
- For \(m=3/5\), the angular factor of \(U_1\) is constant; positive local degree rules out its being one-signed.
- For \(3/5<m<1\), the scalar stress flux at the puncture is \(O(r^{5m-3})\to0\). The scalar equation extends weakly across the puncture, and scalar 6-harmonic interior first-derivative regularity contradicts its nonzero degree-\(m<1\) homogeneity.

The scalar regularity source is Uhlenbeck (1977), printed p.222, already retrieved and visually verified in pass 3. It is applied to the scalar limit only, never directly to the full elasticity system.

Both ranges yield a contradiction, proving the result.

## 6. Dependence on the previous audited arguments

The third-row ray calculation and topology are proved in pass 2, `ANISOTROPIC_STATIONARITY_OBSTRUCTION.md`, SHA-256 `a7c90e5d46dc30e280ef4753437feddf0248184e9f29789c13b35a90cadc44fb`.

The complete first-row exponent and scalar argument is proved in pass 3, `EXACT_WEIGHTED_CORE_EXCLUSION.md`, SHA-256 `f610c0060a11207093d42ee03daa697c98e401471da0136d4d26a1d582a10774`.

The new step here is the weak annular stress limit: it removes exact representation of the actual map and replaces it by subsequential \(C^1\) convergence of weighted rescalings.

## 7. Essential limitations

Finite energy does **not** automatically make the limiting angular determinant positive in this asymptotic setting. The exact-core argument factored one fixed angular integral out of the radial integral. Here the rescaled angular inverse-determinant integrals may grow while being multiplied by the vanishing factor \(r_k^{9-2s}\).

Thus the theorem does not exclude an angularly degenerate limiting profile repaired by lower-order terms, nor convergence weaker than the specified annular \(C^1\) convergence, nor a boundary-only singularity. No theorem providing these tangents for arbitrary minimizers has been established. The conclusion is a restriction on possible singular structures, not resolution of E-6322.
