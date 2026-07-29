# The rank-one two-site boundary floor: an exact shifted Schur reduction

## Status

This note reduces the live rank-one cofactor-floor problem to one
explicit \(9\times9\) Hermitian matrix in a singular-pencil gauge.  It
does **not** prove the resulting matrix positive.

Let \(D,Z\in M_3(\mathbb C)\) be Hilbert--Schmidt orthonormal and put
\[
 |U\rangle
 =|0\rangle_K|D\rangle\!\rangle
  +|1\rangle_K|Z\rangle\!\rangle,\qquad
 R=|U\rangle\langle U|.
\tag{1}
\]
Thus \(\operatorname{Tr}_{12}R=I_K\).  Define
\[
 M(R)=(2E_1-I)(2E_2-I)(R),                               \tag{2}
\]
\[
 \rho_L=DD^\dagger+ZZ^\dagger,\qquad
 \rho_R=D^\dagger D+Z^\dagger Z,                         \tag{3}
\]
and
\[
 \delta=\det\rho_L+\det\rho_R.                           \tag{4}
\]
The numerically suggested sharp inequality is
\[
 \boxed{\qquad M(R)\succeq\delta I_{18}.\qquad}           \tag{5}
\]
The weaker inequality with \(\delta/2\) in place of \(\delta\) is
already sufficient for the current three-copy scalar boundary route.
Neither assertion is proved here.

## 1. Reversed-Hodge matrix

For \(X\in M_3\), let
\[
 {\cal C}_X(Y)=Y\times X,
\qquad
 (Y\times X)_{i\alpha}
 =\epsilon_{ijk}\epsilon_{\alpha\beta\gamma}
   Y_{j\beta}X_{k\gamma}.                                \tag{6}
\]
Set
\[
 A={\cal C}_D^\dagger{\cal C}_D,\qquad
 B={\cal C}_Z^\dagger{\cal C}_Z,\qquad
 K={\cal C}_Z^\dagger{\cal C}_D,                         \tag{7}
\]
and regard \(h=(D,Z)^T\) as a vector in \(M_3\oplus M_3\).

For \(V=(y,w)^T\), the exact reversed-Hodge identity from the
two-copy theorem gives
\[
\begin{aligned}
\frac12\langle V,M(R)V\rangle
={}&\|y\|^2+\|w\|^2+\|y\times D\|^2+\|w\times Z\|^2\\
 &+2\operatorname{Re}\langle y\times Z,w\times D\rangle
 -\frac12|\langle D,y\rangle+\langle Z,w\rangle|^2.
\end{aligned}                                             \tag{8}
\]
Consequently
\[
 \boxed{
 \frac12M(R)\ \simeq\
 G_{D,Z}:=
 \begin{pmatrix}I+A&K\\K^\dagger&I+B\end{pmatrix}
 -\frac12|h\rangle\langle h| .}                          \tag{9}
\]
Here \(\simeq\) is the canonical coefficient-matrix vectorization; in
the row vectorization used in the checker it is literal equality.

For a proposed coefficient \(0<c\le1\), put
\[
 \theta=\frac{c\delta}{2},\qquad \eta=1-\theta.            \tag{10}
\]
Then
\[
 M(R)\succeq c\delta I
 \quad\Longleftrightarrow\quad
 G_{D,Z}-\theta I_{18}\succeq0.                           \tag{11}
\]
The strong conjecture (5) has \(c=1\), \(\theta=\delta/2\);
the sufficient weaker floor has \(c=1/2\),
\(\theta=\delta/4\).

## 2. The \(9\times9\) shifted Schur residual

Write
\[
\begin{aligned}
 H_\theta&=\eta I+A-\frac12|D\rangle\langle D|,\\
 J&=K-\frac12|D\rangle\langle Z|,\\
 L_\theta&=\eta I+B-\frac12|Z\rangle\langle Z|.
\end{aligned}                                             \tag{12}
\]
Thus
\[
 G_{D,Z}-\theta I=
 \begin{pmatrix}H_\theta&J\\J^\dagger&L_\theta\end{pmatrix}.
\tag{13}
\]

Both \(\rho_L,\rho_R\) are positive \(3\times3\) matrices of trace
two.  Arithmetic--geometric mean gives
\[
 0\le\det\rho_L,\det\rho_R\le\frac8{27},
 \qquad 0\le\delta\le\frac{16}{27}.                       \tag{14}
\]
For \(c\le1\), therefore \(\theta\le8/27<1/2\).  Since
\(\|D\|=1\) and \(A\succeq0\),
\[
 H_\theta\succeq\left(\frac12-\theta\right)I\succ0.       \tag{15}
\]
The ordinary Schur complement is consequently lossless:
\[
 \boxed{
 M(R)\succeq c\delta I
 \quad\Longleftrightarrow\quad
 {\cal S}_{\theta}(D,Z):=
 L_\theta-J^\dagger H_\theta^{-1}J\succeq0 .}             \tag{16}
\]
The exact congruence is
\[
\begin{pmatrix}H_\theta&J\\J^\dagger&L_\theta\end{pmatrix}
=
\begin{pmatrix}I&0\\J^\dagger H_\theta^{-1}&I\end{pmatrix}
\begin{pmatrix}H_\theta&0\\0&{\cal S}_\theta\end{pmatrix}
\begin{pmatrix}I&H_\theta^{-1}J\\0&I\end{pmatrix}.         \tag{17}
\]
Thus (16) replaces an \(18\times18\) endpoint inequality by one
explicit \(9\times9\) residual, without a relaxation or an assumed
symmetry of the test vector.

## 3. Singular-pencil gauge

Every complex two-plane in \(M_3\) contains a singular matrix.  After a
unitary change of code frame and independent physical left and right
unitaries, take
\[
 D=\operatorname{diag}(a,b,0),\qquad
 a,b\ge0,\qquad a^2+b^2=1,                               \tag{18}
\]
\[
 Z=
 \begin{pmatrix}
 bc&p&q\\
 r&-ac&s\\
 t&u&d
 \end{pmatrix},
\quad
 |c|^2+|p|^2+|q|^2+|r|^2+|s|^2+|t|^2+|u|^2+|d|^2=1 .
\tag{19}
\]
There are no additional constraints in (19).

In the ordered matrix-unit basis
\[
 (E_{11},E_{12},E_{13},E_{21},E_{22},E_{23},
   E_{31},E_{32},E_{33}),                                \tag{20}
\]
the cross map of \(D\) is
\[
 {\cal C}_D(Y)=
 \begin{pmatrix}
 bY_{33}&0&-bY_{31}\\
 0&aY_{33}&-aY_{32}\\
 -bY_{13}&-aY_{23}&bY_{11}+aY_{22}
 \end{pmatrix}.                                          \tag{21}
\]
It follows that \(A={\cal C}_D^\dagger{\cal C}_D\) has:

- eigenvalue \(0\) on
  \(E_{12},E_{21},aE_{11}-bE_{22}\);
- eigenvalue \(b^2\) on \(E_{13},E_{31}\);
- eigenvalue \(a^2\) on \(E_{23},E_{32}\);
- eigenvalue \(1\) on
  \(E_{33},bE_{11}+aE_{22}\).

Thus \(H_\theta^{-1}\) is diagonal except on
\(\operatorname{span}\{E_{11},E_{22}\}\).  On that subspace set
\[
 v=\binom b a,\qquad d_0=\binom a b .
\]
Then
\[
 H_\theta|_{\{E_{11},E_{22}\}}
 =\eta I_2+vv^T-\frac12d_0d_0^T                         \tag{22}
\]
and
\[
\boxed{
\left.H_\theta^{-1}\right|_{\{E_{11},E_{22}\}}
=\frac1{\kappa_\theta}
\begin{pmatrix}
\eta+a^2-\frac12b^2&-\frac12ab\\
-\frac12ab&\eta+b^2-\frac12a^2
\end{pmatrix},}                                          \tag{23}
\]
where
\[
 \kappa_\theta
 =\eta^2+\frac{\eta}{2}+2a^2b^2-\frac12>0.               \tag{24}
\]
On the remaining seven displayed eigenvectors the inverse
eigenvalues are respectively
\[
 \eta^{-1},\ \eta^{-1},\
 (\eta+b^2)^{-1},\ (\eta+b^2)^{-1},\
 (\eta+a^2)^{-1},\ (\eta+a^2)^{-1},\
 (\eta+1)^{-1}.                                          \tag{25}
\]
Equations (6), (7), (12), and (19), together with (23)--(25), make
every entry of the residual in (16) an explicit rational function of
the eight complex pencil coordinates and \(a,b,\theta\).

The nonlinear shift also has a transparent exact form in this gauge.
Writing \(z_i\) for the rows and \(\zeta_i\) for the columns of \(Z\),
Cauchy--Binet gives
\[
\begin{aligned}
\det\rho_L={}&
 a^2b^2\|z_3\|^2
 {}+a^2\|z_2\wedge z_3\|^2
 {}+b^2\|z_1\wedge z_3\|^2
 {}+|\det Z|^2,\\
\det\rho_R={}&
 a^2b^2\|\zeta_3\|^2
 {}+a^2\|\zeta_2\wedge\zeta_3\|^2
 {}+b^2\|\zeta_1\wedge\zeta_3\|^2
 {}+|\det Z|^2.
\end{aligned}                                             \tag{26}
\]
This is the common-pencil information absent from marginal-only and
independently polarized estimates.

## 4. A scalar alternative

It is sometimes preferable to postpone the final rank-one subtraction.
Define
\[
 {\cal M}_\theta=
 \begin{pmatrix}\eta I+A&K\\K^\dagger&\eta I+B\end{pmatrix}.
\tag{27}
\]
Whenever \({\cal M}_\theta\succ0\), the matrix determinant lemma gives
\[
 G_{D,Z}-\theta I\succeq0
 \quad\Longleftrightarrow\quad
 \langle h,{\cal M}_\theta^{-1}h\rangle\le2.              \tag{28}
\]
Eliminating its first block gives the fully explicit form
\[
\begin{aligned}
 T_\theta&=\eta I+B-K^\dagger(\eta I+A)^{-1}K,\\
 r_\theta&=Z-K^\dagger(\eta I+A)^{-1}D,\\
\langle h,{\cal M}_\theta^{-1}h\rangle
 &=
 \langle D,(\eta I+A)^{-1}D\rangle
 +\langle r_\theta,T_\theta^{-1}r_\theta\rangle .
\end{aligned}                                             \tag{29}
\]
Positivity of \({\cal M}_\theta\), or equivalently of \(T_\theta\),
is part of this alternative formulation and is not asserted here.
The direct residual (16) has no such auxiliary hypothesis.

## 5. Exact and conjectural content

Exact:

1. the endpoint identity (8)--(9);
2. the coefficient normalization (10)--(11);
3. positivity of the eliminated block (15);
4. the lossless \(9\times9\) Schur reduction (16);
5. the singular-gauge inverse (21)--(25);
6. the flattening-volume formula (26).

Conjectural:

1. \({\cal S}_{\delta/2}(D,Z)\succeq0\), equivalent to the
   sharp coefficient-one floor (5);
2. the weaker
   \({\cal S}_{\delta/4}(D,Z)\succeq0\), which is sufficient for the
   current three-copy scalar boundary step.

The dependency-free checker
`verification/verify_n3_rankone_shifted_schur.py` verifies all matrix
identities, constants, and the Schur congruence on an exact rational
singular-pencil instance.
