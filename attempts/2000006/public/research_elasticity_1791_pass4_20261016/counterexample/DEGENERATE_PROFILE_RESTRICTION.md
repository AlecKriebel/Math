# E-6322, pass 4: a restriction on angularly degenerate tangents

Date: 2026-10-16. No singular minimizer or counterexample is claimed.

## 1. Local regular-axis obstruction

Consider the componentwise weighted annular rescalings from `ANNULAR_TANGENT_EXCLUSION.md`, converging in C¹ to a C² weighted-homogeneous profile

\[
U_i(r\theta)=r^{\alpha_i}\phi_i(\theta),\qquad
0<\alpha_1\le\alpha_2\le\alpha_3,\qquad
\gamma=\alpha_1+\alpha_2+\alpha_3-3>0.
\]

Here allow the limiting angular determinant \(j\) to vanish. Assume only that

\[
\eta=2(3\alpha_1+\alpha_2+2\alpha_3-6)>0.
\]

If the original map is a benchmark minimizer, there is **no** angle satisfying all three conditions

\[
\phi_1(\theta_0)=\phi_2(\theta_0)=0,
\qquad j(\theta_0)>0.
\]

Indeed, continuity supplies a neighborhood of that ray where the limiting determinant is bounded below. C¹ annular convergence then makes the original determinants positive on the corresponding supports. The same local variation and normalized third-row stress limit used in the main tangent theorem give

\[
\operatorname{div}\bigl[-2d(\det DU)^{-3}(\operatorname{cof}DU)_3\bigr]=0
\]

on that neighborhood. At the specified angle, the first two gradient rows are tangent to the sphere, so their cross product is a nonzero radial vector. The barrier divergence there equals

\[
6d\kappa\gamma j(\theta_0)^{-3}
 r^{\alpha_1+\alpha_2-3-3\gamma}\ne0,
\]

a contradiction.

Thus every preimage of the third target axis in such a limiting profile must be critical. If no such preimage exists, the statement is vacuous. No global positive-degree or isolated-zero property is inferred merely from a degenerate profile.

This is a necessary local condition on a possible degenerate tangent, not a proof that all such tangents are impossible. More generally, the displayed barrier equation must hold on every open part of the limiting profile where its determinant is positive.

## 2. Rejected diagnostic candidate with genuinely nonaffine compatible trace

This example checks that lower-order angular repair can coexist with all admissibility and boundary requirements. It is then explicitly ruled out by stationarity. It is not proposed as a counterexample.

On \(B_1\), set \(r=|x|\),

\[
y(x)=\bigl(x_1,x_2,x_3^3r^{-3/2}+x_3r\bigr),\qquad y(0)=0.
\]

Both terms in the third component are smooth off the origin, of respective homogeneous degrees \(3/2\) and \(2\). Therefore the map is C¹ on the closed ball, has bounded gradient, and lies in \(W^{1,6}\).

On \(r=1\), its trace is

\[
g(x)=\bigl(x_1,x_2,x_3^3+x_3\bigr).
\]

This is exactly the restriction of the smooth global orientation-preserving diffeomorphism

\[
G(x)=\bigl(x_1,x_2,x_3^3+x_3\bigr),\qquad
\det DG=3x_3^2+1>0.
\]

Writing \(\mu=x_3/r\), direct differentiation gives

\[
J=\det Dy
=r^{1/2}\mu^2\left(3-\frac32\mu^2\right)
+r(1+\mu^2)>0\quad (x\ne0).
\]

Its essential infimum is zero. The leading weighted profile has exponents \((1,1,3/2)\) and a quadratic angular determinant zero along the equator. The second term repairs the actual determinant there.

### Finite barrier energy

For \(0<r<1\),

\[
J\asymp r^{1/2}(\mu^2+r^{1/2}),
\]

with uniform positive comparison constants. Since \(dS=2\pi\,d\mu\) for axisymmetric integrands,

\[
\int_{S^2}J^{-2}\,dS
\asymp r^{-1}\int_{-1}^1(\mu^2+r^{1/2})^{-2}\,d\mu
\asymp r^{-7/4}.
\]

Multiplication by the radial volume factor gives \(r^2r^{-7/4}=r^{1/4}\), which is integrable at zero. All positive-power energy terms are integrable because the gradient is bounded. Hence this is an admissible full-class deformation with the stated smooth nonaffine trace.

This calculation also illustrates why a limiting angular inverse-determinant integral may be infinite although the actual repaired map has finite total energy.

### Explicit failure of stationarity

Let \(f\) denote the third component. Since the first two components are \(x_1,x_2\), the third cofactor row is identically \(e_3\). On the positive third coordinate axis \(x=te_3\),

\[
f(t e_3)=t^{3/2}+t^2,\qquad
J(t e_3)=\frac32t^{1/2}+2t,
\]

\[
\partial_3J(t e_3)=\frac34t^{-1/2}+2.
\]

The third barrier-stress divergence is exactly

\[
6dJ^{-4}\partial_3J
=\frac{8d}{9}t^{-5/2}(1+o(1)).
\]

Meanwhile the positive density \(H(F)=a|F|^6+b|\operatorname{cof}F|^3+c(\det F)^2\) is C² near the bounded range of gradients, and \(D^2y=O(t^{-1/2})\) along the axis. Its third stress divergence is therefore \(O(t^{-1/2})\). It cannot cancel the nonzero barrier term. The candidate fails the classical Euler equation at sufficiently small positive axis points and hence cannot minimize in the full class.

Equivalently, the leading profile has \(\eta=2>0\) and a regular preimage of the third target axis at each pole, violating Section 1.

## 3. Remaining gap

This diagnostic is rejected by a genuine necessary condition; matching integrability and boundary hypotheses never certified it as a minimizer. To evade the present η>0 test, a repaired angularly degenerate tangent would at least need all its third-axis preimages to be critical, or would need to fall outside the stated convergence/profile hypotheses. There is no construction here meeting those requirements together with a full-class comparison certificate. E-6322 remains unresolved.
