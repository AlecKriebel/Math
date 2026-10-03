# A Hessian obstruction in a classical affine-torus deformation

Problem 6000016 / AMR-059-0016, “Stability of Hessian Metrics.”

## Result and attribution

**The unrestricted stability assertion has a negative answer.** There is a smooth one-parameter family of complete, torsion-free flat connections on the fixed compact torus whose central member admits a positive-definite Hessian metric and whose every noncentral member admits no such metric.

The affine deformation used below is classical. It is exactly the family of developing maps displayed by **Oliver Baues and William M. Goldman**, *Is the deformation space of complete affine structures on the 2-torus smooth?*, arXiv:math/0401257v2, §5, printed p. 20. Their §4, pp. 14–15, gives the equivalent shear construction with the coordinates interchanged. We supply the short, elementary obstruction to **all** positive-definite Hessian metrics on those noncentral fibers. Neither the family nor historical priority for its application to the stability question is claimed to be new.

The target is Satoru Shimizu's item 5(b) in Furuhata–Matsuzoe–Urakawa (1998), printed p. 126. Its hyperbolic special case is explicitly credited there to Koszul; our example is outside that special case because its developing image is the whole affine plane.

## 1. The affine structures

Write

\[
T^2=\mathbb R^2/\mathbb Z^2,
\qquad X=\partial_x,\quad Y=\partial_y.
\]

The coordinates themselves are understood modulo integers, whereas the vector fields and the forms \(dx,dy\) are globally defined. Let \(D^0\) be the standard flat connection. For any real parameter \(t\), set

\[
D^t=D^0+t\,dx\otimes dx\otimes Y.
\tag{1}
\]

Equivalently, in the global commuting frame,

\[
D^t_X X=tY,\qquad D^t_XY=D^t_YX=D^t_YY=0.
\tag{2}
\]

This is a globally defined connection because the added term is a tensor. It is torsion-free because that tensor is symmetric in its two input slots. Its curvature vanishes: all connection coefficients are constant, and every composition of two connection-coefficient operators vanishes. More explicitly the only nonzero coefficient is \(\Gamma^y_{xx}=t\), while every coefficient with a lower \(y\)-index is zero, so every quadratic term in the curvature formula is zero.

There is also a global developing-map verification. Define

\[
F_t(x,y)=\left(x,y+\frac t2x^2\right).
\tag{3}
\]

This is a diffeomorphism of \(\mathbb R^2\), with inverse \(F_{-t}\) and Jacobian determinant one. Pulling back the standard affine connection by \(F_t\) gives (2): the only second derivative of \(F_t\) is \(\partial_x^2F_t=(0,t)\), and the inverse Jacobian sends \((0,t)\) to \(tY\).

For \((m,n)\in\mathbb Z^2\), put

\[
\rho_t(m,n)(u,v)
=\left(u+m,v+n+tm u+\frac t2m^2\right).
\tag{4}
\]

Then

\[
F_t(x+m,y+n)=\rho_t(m,n)F_t(x,y),
\tag{5}
\]

and \(\rho_t(m,n)\rho_t(p,q)=\rho_t(m+p,n+q)\). Each \(\rho_t(m,n)\) is affine, with linear part

\[
\begin{pmatrix}1&0\\tm&1\end{pmatrix}.
\]

The action is the conjugate by \(F_t\) of the integer-translation action, so it is free and properly discontinuous and has compact quotient. Thus \(F_t\) supplies an affine atlas on the same smooth torus. Its image is all of \(\mathbb R^2\), so the affine structure is complete. Alternatively, its lifted geodesic equations have the global solutions

\[
x(s)=x_0+as,\qquad
y(s)=y_0+bs-\frac t2a^2s^2.
\tag{6}
\]

These are genuine small deformations in the ordinary smooth topology of affine structures. On the fixed torus (1) is a smooth family and \(D^t\to D^0\) in \(C^\infty\). More concretely, choose fixed small open sets with lifts to \(\mathbb R^2\) and use \(F_t\) on these lifts as charts. They vary smoothly with \(t\); on overlap components their affine transition functions are the smoothly varying maps (4).

At \(t=0\), the metric

\[
g_0=dx^2+dy^2
\]

is a positive-definite Hessian metric for \(D^0\): in any lifted affine coordinate neighborhood it is the Hessian of \((x^2+y^2)/2\). A single global potential on the compact torus is neither asserted nor needed.

## 2. A necessary identity for an arbitrary Hessian metric

For a flat torsion-free connection \(D\), any local Hessian metric satisfies the Codazzi identity

\[
(D_Ug)(V,W)=(D_Vg)(U,W).
\tag{7}
\]

Indeed, in affine coordinates \(D_i g_{jk}=\partial_i\partial_j\partial_k\phi\), so the identity follows from equality of mixed derivatives. Both sides are tensorial, so it holds in every frame. Only this necessary implication is used below.

Suppose that a smooth positive-definite Hessian metric \(g\) exists for \(D^t\), and write its lift as

\[
g=A(x,y)\,dx^2+2B(x,y)\,dx\,dy+C(x,y)\,dy^2.
\tag{8}
\]

The three coefficients are smooth and 1-periodic in each variable because these are the coordinates of the fixed smooth quotient, not the developing coordinates. Positivity gives

\[
C(x,y)=g(Y,Y)>0
\tag{9}
\]

everywhere, since \(Y\) never vanishes.

Take \(U=X,V=Y,W=X\) in (7). From (2) and the definition of the covariant derivative of a bilinear form,

\[
\begin{aligned}
(D^t_Xg)(Y,X)
&=X(g(Y,X))-g(D^t_XY,X)-g(Y,D^t_XX)\\
&=\partial_xB-tC,\\
(D^t_Yg)(X,X)
&=Y(g(X,X))-2g(D^t_YX,X)\\
&=\partial_yA.
\end{aligned}
\]

Consequently every candidate metric must satisfy

\[
\partial_xB-\partial_yA=tC.
\tag{10}
\]

This calculation does not assume that \(g\) is translation invariant, parallel, diagonal, close to \(g_0\), or part of a smooth family of metrics.

## 3. The global contradiction

Integrate (10) with respect to the ordinary quotient measure \(dx\,dy\) on a unit square. Periodicity yields

\[
\int_0^1\!\int_0^1 \partial_xB\,dx\,dy=0,
\qquad
\int_0^1\!\int_0^1 \partial_yA\,dx\,dy=0.
\]

Hence

\[
t\int_0^1\!\int_0^1 C(x,y)\,dx\,dy=0.
\tag{11}
\]

The integral is strictly positive by (9). Therefore \(t=0\). This proves that \((T^2,D^t)\) admits no positive-definite Hessian metric for every \(t\ne0\).

In invariant language, the one-form \(\alpha=g(X,\cdot)=A\,dx+B\,dy\) would satisfy

\[
d\alpha=t\,g(Y,Y)\,dx\wedge dy,
\]

and Stokes' theorem gives the same contradiction on the compact torus.

Thus every neighborhood of the standard Hessian affine structure contains non-Hessian affine structures, even among complete volume-preserving affine structures. The complete negative answer concerns the unrestricted question as printed, with “Hessian metric” meaning positive-definite Riemannian Hessian metric. No claim is made about pseudo-Riemannian metrics or deformations with fixed linear holonomy. In particular, the conclusion does not contradict the separate hyperbolic stability result mentioned in the source.

## Verification and limitations

The proof is analytical and valid for arbitrary real \(t\ne0\) and arbitrary smooth candidate \(g\). The accompanying symbolic checker verifies the connection, curvature, developing map, holonomy law, geodesic equations and exact Codazzi expression. These checks are reproducibility controls, not a substitute for the positivity and integration argument. Independent audit status is recorded separately; no human peer-review or novelty claim is implied.

## References

1. H. Furuhata, H. Matsuzoe and H. Urakawa, *Open Problems in Affine Differential Geometry and Related Topics*, Interdisciplinary Information Sciences **4** (1998), 125–127, item 5(b), p. 126. [Article](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_article/-char/en), [original PDF](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en).
2. O. Baues and W. M. Goldman, *Is the deformation space of complete affine structures on the 2-torus smooth?*, [arXiv:math/0401257v2](https://arxiv.org/pdf/math/0401257v2), §4, pp. 14–15, and §5, p. 20. The exact family (3) is displayed on p. 20.
