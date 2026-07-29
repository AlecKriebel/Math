# The complete determinant-normalized Hessian at a hypothetical negative critical point

## Status

Assume, for contradiction, that the unrestricted three-copy endpoint
has a negative rank-two witness.  The determinant-normalized critical
reduction gives a negative global minimizer \(C\) with
\[
s_1(C)s_2(C)=1.
\]
This note derives its complete constrained second variation.

The fixed two-plane pencil can be solved globally in closed form.  It
contains no new physical restriction: the necessary and sufficient
conditions for the singlet to minimize that pencil are exactly three
strict rank-one tests already implied by positivity of the ordinary
logical Gram \(K\).

The first genuinely physical second-order datum occurs when both
singular planes move.  For every pair of left/right leakage directions
it obeys the sharp inequality
\[
\boxed{\qquad
\bigl(|p|+|q|\bigr)^2\leq ab.
\qquad}
\]
Here \(p\) is the ordinary crossed quadratic response and \(q\) is
the second-fundamental-form pairing with the normal residual of
\(L^{\otimes3}(C)\).  This is an exact nonlinear constraint coupling
the two plane motions; bounding the two terms separately loses the
critical geometry.

No contradiction with a negative critical value has yet been
derived.  The remaining problem is now an explicit normal-residual
inequality rather than an unconstrained rank-two search.

## 1. Critical data and tangent coordinates

Write the singular-value decomposition
\[
C=U\Sigma V^\dagger,\qquad
\Sigma=\begin{pmatrix}r&0\\0&r^{-1}\end{pmatrix},
\qquad r\geq1,
\tag{1}
\]
and put
\[
P_U=UU^\dagger,\qquad P_V=VV^\dagger.
\tag{2}
\]
Let
\[
{\cal L}=L^{\otimes3},\qquad
\lambda=\frac12Q_3(C)<0.
\tag{3}
\]
The determinant-normalized Euler--Lagrange equations are
\[
\begin{aligned}
{\cal L}(C)V&=\lambda U\Sigma^{-1},\\
{\cal L}(C)^\dagger U&=\lambda V\Sigma^{-1}.
\end{aligned}
\tag{4}
\]
Consequently
\[
\boxed{\qquad
{\cal L}(C)
=\lambda U\Sigma^{-1}V^\dagger+R,
\qquad
R=(I-P_U){\cal L}(C)(I-P_V).
\qquad}
\tag{5}
\]
The matrix \(R\) is the normal residual.

There is already a useful scalar consequence of (4).  Put
\[
C_i=u_iv_i^\dagger,\qquad
a=Q_3(C_1),\quad b=Q_3(C_2),\quad
c=\langle C_1,{\cal L}(C_2)\rangle.
\tag{6}
\]
The two diagonal entries of (4) give
\[
\boxed{
\lambda=r^2a+c=\overline c+r^{-2}b.
}
\tag{7}
\]
Hence
\[
c\in\mathbb R,\qquad b=r^4a.
\tag{8}
\]
The rank-one spectral bounds
\[
\frac18\leq a,b\leq\frac{27}{8}
\tag{9}
\]
therefore imply the compact critical restriction
\[
\boxed{\qquad
1\leq r^4\leq27.
\qquad}
\tag{10}
\]
Moreover, a negative multiplier forces
\[
c=\lambda-r^2a<-\sqrt{ab},
\tag{11}
\]
and indeed
\[
\boxed{\qquad
|c|^2-ab=\lambda^2-2\lambda r^2a>0.
\qquad}
\tag{12}
\]
Thus every hypothetical negative critical point must exhibit a
strict reverse-Cauchy defect between its two singular rank-one
components.  The off-diagonal entries of (4) add
\[
\langle u_1v_2^\dagger,{\cal L}(C)\rangle
=
\langle u_2v_1^\dagger,{\cal L}(C)\rangle=0.
\tag{13}
\]

Choose orthonormal complements \(U_\perp,V_\perp\).  A general
first-order tangent is described by
\[
A\in M_2,\qquad
X: \mathbb C^2\to U^\perp,\qquad
Z:V^\perp\to\mathbb C^2,
\tag{14}
\]
and has the form
\[
\boxed{
D=D_A+D_X+D_Z,
}
\tag{15}
\]
where
\[
\begin{aligned}
D_A&=UAV^\dagger,\\
D_X&=U_\perp X\Sigma V^\dagger,\\
D_Z&=U\Sigma ZV_\perp^\dagger.
\end{aligned}
\tag{16}
\]
The first-order determinant constraint is
\[
\boxed{\qquad
\operatorname{Re}\operatorname{Tr}(\Sigma^{-1}A)=0.
\qquad}
\tag{17}
\]

## 2. Exact second variation

Take Stiefel geodesics with initial velocities
\[
U'(0)=U_\perp X,\qquad
V'(0)=V_\perp Z^\dagger.
\tag{18}
\]
Their second derivatives can be chosen as
\[
U''(0)=-UX^\dagger X,\qquad
V''(0)=-VZZ^\dagger.
\tag{19}
\]
Write
\[
M(t)=\Sigma+tA+\frac{t^2}{2}B+O(t^3).
\tag{20}
\]
Because the moving frames remain isometric,
\[
s_1(C(t))s_2(C(t))=|\det M(t)|.
\tag{21}
\]
The second-order determinant constraint is therefore
\[
\boxed{\qquad
\operatorname{Re}\operatorname{Tr}(\Sigma^{-1}B)
=
\operatorname{Re}\operatorname{Tr}
\bigl((\Sigma^{-1}A)^2\bigr).
\qquad}
\tag{22}
\]

Direct differentiation gives
\[
\begin{aligned}
C''(0)={}&
UBV^\dagger
-UX^\dagger X\Sigma V^\dagger
-U\Sigma ZZ^\dagger V^\dagger\\
&+2U_\perp XAV^\dagger
+2UAZV_\perp^\dagger
+2U_\perp X\Sigma ZV_\perp^\dagger.
\end{aligned}
\tag{23}
\]
The middle two terms are tangent and pair to zero with the
Euler--Lagrange residual.  Using (5) and (22), one obtains the complete
constrained Hessian.

### Theorem 2.1

For every \(A,X,Z\) satisfying (17),
\[
\boxed{
\begin{aligned}
\frac12\frac{d^2}{dt^2}Q_3(C(t))\bigg|_{t=0}
={}&Q_3(D)
+\lambda\operatorname{Re}\operatorname{Tr}
\bigl((\Sigma^{-1}A)^2\bigr)\\
&-\lambda\bigl(\|X\|_2^2+\|Z\|_2^2\bigr)\\
&+2\operatorname{Re}
\left\langle
R,\,
U_\perp X\Sigma ZV_\perp^\dagger
\right\rangle_{\rm HS}.
\end{aligned}}
\tag{24}
\]
Since \(C\) is a global minimizer on the determinant slice, the
right-hand side is nonnegative.

Equation (24) is independent of the choices of orthonormal
complements.  The last line is the second fundamental form of the
rank-two determinantal manifold paired with the normal residual.

## 3. The fixed-pencil problem is exactly solvable

Pass to the simultaneous critical Bell frame.  Choose phases of the
orthonormal magic Bell matrices \(M_\alpha\) so that
\[
2\det\left(\sum_{\alpha=0}^3z_\alpha M_\alpha\right)
=\sum_{\alpha=0}^3z_\alpha^2.
\tag{25}
\]
The singlet is \(z=(1,0,0,0)\), after an irrelevant common scaling.
The critical companion equations diagonalize the pencil:
\[
Q_3\left(\sum_\alpha z_\alpha C_\alpha\right)
=\sum_{\alpha=0}^3\lambda_\alpha|z_\alpha|^2,
\qquad \lambda_0<0.
\tag{26}
\]

Normalize the determinant constraint to
\[
\left|\sum_{\alpha=0}^3z_\alpha^2\right|=1.
\tag{27}
\]
The reverse triangle inequality gives
\[
|z_0|^2
\leq1+\sum_{j=1}^3|z_j|^2.
\tag{28}
\]
Therefore
\[
\boxed{
\sum_{\alpha=0}^3\lambda_\alpha|z_\alpha|^2
\geq
\lambda_0+
\sum_{j=1}^3(\lambda_j+\lambda_0)|z_j|^2.
}
\tag{29}
\]
It follows that the singlet is a global minimizer on its entire
fixed-plane determinant slice if and only if
\[
\boxed{\qquad
\lambda_j+\lambda_0\geq0
\quad(j=1,2,3).
\qquad}
\tag{30}
\]
Necessity follows by taking
\[
z_0=\sqrt{1+t^2},\qquad z_j=it.
\tag{31}
\]
If one sum in (30) is negative, (31) even makes the pencil energy
tend to \(-\infty\).

For a physical compression the inequalities in (30) are strict and
contain no new tensor information.  Indeed, \(z_0=1,z_j=i\) has
\[
\sum_\alpha z_\alpha^2=0,
\tag{32}
\]
so its logical coefficient matrix has rank one.  Its energy is
\[
\lambda_0+\lambda_j>0
\tag{33}
\]
because \(K\succ0\), equivalently because every physical rank-one
coefficient has the strict \(1/8\) floor.

The local Hessian makes the same separation transparent.  Write a
small companion coordinate as \(z_j=x_j+iy_j\).  After eliminating
the second-order singlet coordinate using (27), the quadratic term is
\[
\boxed{\qquad
(\lambda_j-\lambda_0)x_j^2
+(\lambda_j+\lambda_0)y_j^2.
\qquad}
\tag{34}
\]
The first coefficient is automatic from \(\lambda_j>0>\lambda_0\);
the second is exactly (33).

Thus neither the fixed-pencil global problem nor its Hessian can
exclude a negative physical singlet.  The code planes must move.

## 4. The sharp two-plane leakage inequality

Set \(A=0\) in (24).  For fixed \(X,Z\), define
\[
\begin{aligned}
a&=Q_3(D_X)-\lambda\|X\|_2^2,\\
b&=Q_3(D_Z)-\lambda\|Z\|_2^2,\\
p&=\langle D_X,{\cal L}(D_Z)\rangle_{\rm HS},\\
q&=\left\langle
R,U_\perp X\Sigma ZV_\perp^\dagger
\right\rangle_{\rm HS}.
\end{aligned}
\tag{35}
\]
Replace \(X,Z\) by \(\alpha X,\beta Z\), where
\(\alpha,\beta\in\mathbb C\).  Equation (24) becomes
\[
\boxed{
a|\alpha|^2+b|\beta|^2
+2\operatorname{Re}\left(
\overline\alpha\beta p+\alpha\beta q
\right)\geq0.
}
\tag{36}
\]
The phase difference and phase sum of \(\alpha,\beta\) can be chosen
independently.  Hence both cross terms can be made negative
simultaneously.  Minimizing their phases and then their magnitudes
proves the exact equivalence
\[
\boxed{
\begin{aligned}
a&\geq0,\qquad b\geq0,\\
\bigl(|p|+|q|\bigr)^2&\leq ab.
\end{aligned}}
\tag{37}
\]

This is stronger than either separate estimate
\[
|p|^2\leq ab,\qquad |q|^2\leq ab.
\tag{38}
\]
The ordinary cross response \(p\) and the normal curvature \(q\)
consume one common Hessian budget.  Equivalently,
\[
\boxed{\qquad
\left|
\left\langle
R,U_\perp X\Sigma ZV_\perp^\dagger
\right\rangle
\right|
\leq
\sqrt{
\bigl(Q_3(D_X)-\lambda\|X\|^2\bigr)
\bigl(Q_3(D_Z)-\lambda\|Z\|^2\bigr)}
-|\langle D_X,{\cal L}(D_Z)\rangle|.
\qquad}
\tag{39}
\]
Every rank-at-most-two normal direction can be written as
\[
U_\perp X\Sigma ZV_\perp^\dagger.
\tag{40}
\]
Thus (39) is an explicit family of nonlinear inequalities controlling
the entire normal residual \(R\).

## 5. Complete Hessian versus the leakage restriction

Theorem 2.1 also retains mixed core/leakage directions.  Put
\[
D_{\rm out}=D_X+D_Z.
\tag{41}
\]
Then (24) splits as
\[
\begin{aligned}
{\mathfrak H}(A,X,Z)
={}&{\mathfrak H}_{\rm core}(A)
+{\mathfrak H}_{\rm out}(X,Z)\\
&+2\operatorname{Re}
\langle D_A,{\cal L}(D_{\rm out})\rangle.
\end{aligned}
\tag{42}
\]
In the magic Bell coordinates, the core form on the phase quotient is
strictly positive, with the six eigenvalues displayed in (34).
Therefore the full Hessian is equivalently the Schur-complement
strengthening of (37) obtained by minimizing (42) over the six real
companion coordinates.  If
\[
\ell_j=\langle C_j,{\cal L}(D_{\rm out})\rangle,
\tag{43}
\]
the amount subtracted from the outside form is
\[
\boxed{\qquad
\sum_{j=1}^3
\left[
\frac{(\operatorname{Re}\ell_j)^2}{\lambda_j-\lambda_0}
+
\frac{(\operatorname{Im}\ell_j)^2}{\lambda_j+\lambda_0}
\right],
\qquad}
\tag{44}
\]
with the normalization of the magic companion matrices fixed by
(25).

The leakage-only inequality (37) is the cleanest frame-independent
necessary condition.  The full Schur complement (44) is stronger,
but it requires the three companion couplings in addition to
\(R,p,a,b\).

## 6. Remaining finite object

A hypothetical negative endpoint therefore produces finite critical
data
\[
\left(
r,\lambda,R,\lambda_1,\lambda_2,\lambda_3;
{\cal L}|_{\text{left/right leakage spaces}}
\right)
\tag{45}
\]
obeying:

1. the reciprocal-singular first-order equations (4);
2. the strict fixed-pencil gaps \(\lambda_j+\lambda_0>0\);
3. the complete Hessian (24);
4. the sharp coupled leakage inequality (37);
5. the companion Schur complement (44).

What remains is to combine these relations with the explicit
three-fold partial-trace structure of \({\cal L}\).  Positivity of the
abstract logical Gram explains (30) but does not imply the normal
residual bound (37).  The latter is the first second-order condition
that genuinely sees how the common rank-two code planes sit inside
the three-qutrit tensor product.
