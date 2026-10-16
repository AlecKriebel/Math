# Independent audit obstruction: finite energy does not make the Piola stress integrable

Date: 2026-10-16. This is an admissible-map example, not a minimizer and not a counterexample to E-6322.

On the unit ball in three dimensions, put

\[
y(x_1,x_2,x_3)=(x_1,x_2,x_3r),\qquad r=|x|.
\]

The third component is homogeneous of degree two and has bounded second derivatives away from the origin. Its gradient extends Lipschitz-continuously through the origin. Thus \(y\in C^{1,1}(\overline B_1)\). Its boundary trace is the identity, and

\[
F=Dy=\begin{pmatrix}1&0&0\\0&1&0\\u&v&J\end{pmatrix},\quad
u=x_1x_3/r,\quad v=x_2x_3/r,\quad
J=r+x_3^2/r.
\]

These expressions apply away from zero; \(F(0)=\operatorname{diag}(1,1,0)\). Since \(r\le J\le2r\), the inverse-square determinant is integrable in three dimensions. The gradient is bounded, so every positive-power term of E-6322 is integrable as well. The essential infimum of \(J\) is zero.

In fact \(y\) is a homeomorphism of the closed ball onto itself: for each fixed \((x_1,x_2)\), the map \(x_3\mapsto x_3\sqrt{x_1^2+x_2^2+x_3^2}\) is strictly increasing on its vertical interval and fixes the two endpoints. This extra topological fact does not make the map minimizing.

The cofactor matrix is

\[
C=\operatorname{cof}F=\begin{pmatrix}J&0&-u\\0&J&-v\\0&0&1\end{pmatrix}.
\]

Writing \(P=DW(F)\), differentiation with respect to \(F_{33}\) gives the exact identity

\[
P_{33}=6a|F|^4J+6b|C|J+2cJ-2dJ^{-3}.
\]

The first three terms are bounded. The last term is not absolutely integrable, since

\[
\int_{B_\delta}J^{-3}\,dx
=\left(\int_{S^2}(1+\theta_3^2)^{-3}\,dS\right)
\int_0^\delta r^{-1}\,dr=+\infty.
\]

Consequently \(DW(Dy)\notin L^1\), although both stress products \(PF^T\) and \(F^TP\) are integrable under the target energy bound. A compactly supported smooth additive perturbation whose gradient equals \(e_3\otimes e_3\) near zero also destroys positive determinant for every sufficiently small parameter of one sign: there \(\det(F+t e_3\otimes e_3)=J+t\).

This verifies three safeguards independently:

1. Energy finiteness alone cannot justify the ordinary Piola weak equation or two-sided additive variations.
2. A conditional positivity theorem assuming \(J\in C^{1,1}\) must not be restated as one assuming merely \(y\in C^{1,1}\). Here \(J\) is Lipschitz but not differentiable at zero.
3. Smooth compatible trace, topological injectivity, and finite energy still do not suffice without the minimizer property. The identity is the unique full-class minimizer for this trace, by strict polyconvex Jensen and the null-Lagrangian identities.

No external theorem or numerical approximation is needed for these computations.
