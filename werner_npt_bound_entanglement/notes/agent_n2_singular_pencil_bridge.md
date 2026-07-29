# The two-copy qutrit bridge: tangent maps and a singular-pencil residual

Scope: exact first-principles reduction of the unresolved two-copy qutrit
correlation inequality.  The result is a single explicit \(9\times9\)
Hermitian residual in a canonical matrix-pencil gauge.  The residual has
not yet been proved positive, so this note does **not** claim the two-copy
theorem.

## 1. The correlation inequality and its tangent-map adjoint

Let
\[
P=|X_1\rangle\!\rangle\langle\!\langle X_1|
  |X_2\rangle\!\rangle\langle\!\langle X_2|,
\qquad
\langle X_r,X_s\rangle_{\rm HS}=\delta_{rs},
\tag{1}
\]
be a rank-two projection on \(\mathbb C^3\otimes\mathbb C^3\).  Put
\[
\rho_L=\sum_{r=1}^2X_rX_r^\dagger,\qquad
\rho_R=\sum_{r=1}^2X_r^\dagger X_r.
\tag{2}
\]
For traceless \(A,B\in M_3\), the desired inequality is
\[
\left|\sum_r\langle BX_r,X_rA\rangle\right|^2
\le
\left(2\|A\|_2^2-\operatorname{Tr}\rho_R A^\dagger A\right)
\left(2\|B\|_2^2-\operatorname{Tr}\rho_L B^\dagger B\right).
\tag{3}
\]
Transposing \(A\) merely changes the vectorization convention.

Define the orbit tangent map
\[
\mathcal T_X(A,B)
=\bigl(BX_1+X_1A,\;BX_2+X_2A\bigr),
\qquad (A,B)\in M_3^0\oplus M_3^0.
\tag{4}
\]
Expanding the square in (4) shows that (3), for all phases and relative
scalings of \(A,B\), is exactly equivalent to
\[
\boxed{\quad \|\mathcal T_X\|_{\rm op}^2\le2.\quad}
\tag{5}
\]

There is a useful adjoint form.  For \(Y=(Y_1,Y_2)\in M_3\oplus M_3\), set
\[
L_Y=\sum_rY_rX_r^\dagger,\qquad
R_Y=\sum_rX_r^\dagger Y_r,\qquad
t_Y=\operatorname{Tr}L_Y=\operatorname{Tr}R_Y.
\tag{6}
\]
Then
\[
\mathcal T_X^\dagger(Y)
=\left((R_Y)_0,(L_Y)_0\right),
\qquad M_0=M-\frac{\operatorname{Tr}M}{3}I,
\tag{7}
\]
up to interchanging the two displayed components.  Hence (5) is
equivalent to the compact cross-marginal inequality
\[
\boxed{\quad
\left\|L_Y-\frac{t_Y}{3}I\right\|_2^2
+\left\|R_Y-\frac{t_Y}{3}I\right\|_2^2
\le2\sum_r\|Y_r\|_2^2 .
\quad}
\tag{8}
\]

This is also an anchored swap inequality.  Regard
\[
X=\sum_r|X_r\rangle\otimes|r\rangle_K,\qquad
Y=\sum_r|Y_r\rangle\otimes|r\rangle_K .
\tag{9}
\]
The frame condition in (1) is
\(\rho_K^X=I_2\).  The swap trick gives
\[
(8)\quad\Longleftrightarrow\quad
\left\langle Y\otimes X\left|
I-F_L-F_R+\frac23F_LF_RF_K
\right|Y\otimes X\right\rangle\ge0.
\tag{10}
\]
Since
\(\langle F_K\rangle=\|Y\|^2\) and
\(\langle I\rangle=2\|Y\|^2\) under the anchor
\(\rho_K^X=I_2\), \(I\) in (10) can equivalently be replaced by
\(2F_K\).

Equation (10) isolates the obstruction very sharply: the unique
antisymmetric \(K\)-channel must be controlled coherently by all three
symmetric \(K\)-channels.  Routing only the trace channel loses a factor
two.

## 2. Every two-plane has a singular member

The determinant
\[
p(s,t)=\det(sX_1+tX_2)
\tag{11}
\]
is a homogeneous cubic in two complex variables.  It has a nonzero
projective zero.  A unitary change of code basis therefore produces an
orthonormal frame \((D,Z)\) for the same plane with
\(\det D=0\).

Apply independent left and right unitaries to the matrix pencil.  They
preserve (5), so the singular member may be put in the form
\[
D=\operatorname{diag}(a,b,0),
\qquad a,b\ge0,\qquad a^2+b^2=1.
\tag{12}
\]
The second frame vector has the exact parametrization
\[
Z=
\begin{pmatrix}
bc&p&q\\
r&-ac&s\\
t&u&d
\end{pmatrix},
\qquad
|c|^2+|p|^2+|q|^2+|r|^2+|s|^2+|t|^2+|u|^2+|d|^2=1.
\tag{13}
\]
Conversely, (12)--(13) give every orthonormal frame in this gauge.
Thus the unrestricted two-plane problem has no further hidden
Pluecker constraint after (13): the common-plane geometry is now encoded
exactly by these eight complex coordinates and the one sphere equation.

## 3. Exact \(9\times9\) Schur-complement residual

For \(X\in M_3\), define
\[
\mathcal S_X(Y)=\bigl((YX^\dagger)_0,(X^\dagger Y)_0\bigr),
\qquad \mathcal S_X:M_3\longrightarrow M_3^0\oplus M_3^0.
\tag{14}
\]
Equation (8) says
\[
\left\|\begin{bmatrix}\mathcal S_D&\mathcal S_Z\end{bmatrix}\right\|^2
\le2.
\tag{15}
\]
In the ordered matrix-unit basis
\[
(E_{11},E_{12},E_{13},E_{21},E_{22},E_{23},
  E_{31},E_{32},E_{33}),
\tag{16}
\]
put
\[
G_D=2I_9-\mathcal S_D^\dagger\mathcal S_D.
\tag{17}
\]
A direct calculation gives
\[
G_D=
\begin{pmatrix}
2-\frac43a^2&0&0&0&\frac23ab&0&0&0&0\\
0&1&0&0&0&0&0&0&0\\
0&0&1+b^2&0&0&0&0&0&0\\
0&0&0&1&0&0&0&0&0\\
\frac23ab&0&0&0&2-\frac43b^2&0&0&0&0\\
0&0&0&0&0&1+a^2&0&0&0\\
0&0&0&0&0&0&1+b^2&0&0\\
0&0&0&0&0&0&0&1+a^2&0\\
0&0&0&0&0&0&0&0&2
\end{pmatrix}.
\tag{18}
\]
In particular,
\[
\det G_D
=\frac83(1+a^2b^2)(1+a^2)^2(1+b^2)^2>0.
\tag{19}
\]

The full defect in (15) is the block matrix
\[
\mathcal G(D,Z)=
\begin{pmatrix}
G_D&-\mathcal S_D^\dagger\mathcal S_Z\\
-\mathcal S_Z^\dagger\mathcal S_D&
2I_9-\mathcal S_Z^\dagger\mathcal S_Z
\end{pmatrix}.
\tag{20}
\]
Since \(G_D>0\), the complete two-copy qutrit problem is exactly
equivalent to the following one-matrix statement:
\[
\boxed{\quad
\mathcal R_{a,b,Z}:=
2I_9-\mathcal S_Z^\dagger\mathcal S_Z
-\mathcal S_Z^\dagger\mathcal S_D
G_D^{-1}
\mathcal S_D^\dagger\mathcal S_Z
\succeq0
\quad}
\tag{21}
\]
for every (12)--(13).

This is a strict reduction: the original optimization over a pair of
traceless \(3\times3\) matrices and a two-plane is replaced by positivity
of one explicit \(9\times9\) Hermitian matrix on the eight-complex-
dimensional sphere (13).  Formula (18) makes its only inverse elementary.
For example, on the \(E_{11},E_{22}\) block,
\[
\left.G_D^{-1}\right|_{\{E_{11},E_{22}\}}
=\frac{3}{4(1+a^2b^2)}
\begin{pmatrix}
2-\frac43b^2&-\frac23ab\\
-\frac23ab&2-\frac43a^2
\end{pmatrix}.
\tag{22}
\]

## 4. The transverse determinant gap suggested by the residual

The two local flattening volumes are
\[
\Delta_L=\det(DD^\dagger+ZZ^\dagger),\qquad
\Delta_R=\det(D^\dagger D+Z^\dagger Z).
\tag{23}
\]
By Cauchy--Binet, each is an exact sum of squared \(3\times3\) minors:
\(\Delta_L\) for the \(3\times6\) horizontal flattening
\([D\ Z]\), and \(\Delta_R\) for the \(6\times3\) vertical flattening
\([D^T\ Z^T]^T\).  Hence
\[
\Delta_L=0\Longleftrightarrow
\dim(\text{common left support})\le2,
\qquad
\Delta_R=0\Longleftrightarrow
\dim(\text{common right support})\le2.
\tag{24}
\]

Unrestricted complex optimization of the discovery layer consistently
suggests the stronger operator inequality
\[
\boxed{\quad
2I_{16}-\mathcal T_X^\dagger\mathcal T_X
\ \stackrel{?}{\succeq}\
\frac{\Delta_L+\Delta_R}{2}\,I_{16}.
\quad}
\tag{25}
\]
The observed ratio approaches \(1\), so the coefficient \(1/2\) appears
sharp.  This is **not a theorem**.  Its value is structural: it says that
the exact nonlinear information missing from the double-reduction
Cauchy estimate may be precisely the sum of the two qutrit flattening
volumes.  It also predicts that equality is confined to common local
two-dimensional support, where \(\Delta_L=\Delta_R=0\).

## 5. Exact obstruction to a simpler Hodge gap

Let the qutrit mixed cross product be
\[
(X\times Y)_{i\alpha}
=\sum_{j,k,\beta,\gamma}
\epsilon_{ijk}\epsilon_{\alpha\beta\gamma}
X_{j\beta}Y_{k\gamma}.
\tag{26}
\]
It obeys the exact Lagrange identity
\[
\|X\times Y\|_2^2
=\|X\|_2^2\|Y\|_2^2
-\|XY^\dagger\|_2^2-\|X^\dagger Y\|_2^2
+|\langle X,Y\rangle|^2.
\tag{27}
\]
It is tempting to lower-bound the defect in (5) by a positive multiple
of \(\|D\times Z\|^2\).  That is impossible, even on exact equality
frames.

Take
\[
D=\operatorname{diag}\left(\frac35,\frac45,0\right),\qquad
Z=\operatorname{diag}\left(\frac45,-\frac35,0\right),
\tag{28}
\]
and
\[
A=B=\frac12\operatorname{diag}(-1,1,0).
\tag{29}
\]
Then \(D,Z\) are Hilbert--Schmidt orthonormal,
\(\|A\|^2+\|B\|^2=1\), and
\[
\|BD+DA\|^2+\|BZ+ZA\|^2=1+1=2.
\tag{30}
\]
Thus (5) is an equality.  Nevertheless,
\[
D\times Z=\frac7{25}E_{33}\ne0.
\tag{31}
\]
The correct Hodge quantity therefore cannot be the full mixed cross
product.  The nonzero component in (31) lies entirely inside the common
\(2\times2\) core.  Any successful exterior certificate must remove that
core component and retain the two flattening volumes (23), or an
equivalent transverse incidence tensor.

## 6. Precise status

### Exact

1. The correlation inequality, tangent-map norm bound (5), adjoint
   inequality (8), and anchored swap form (10) are equivalent.
2. Every code plane admits the singular-pencil gauge (12)--(13).
3. In that gauge the complete theorem is equivalent to the explicit
   \(9\times9\) residual (21).
4. The determinant formula (19), the flattening-minor interpretation
   (23)--(24), and the equality obstruction (28)--(31) are exact.

### Conjectural

The determinant gap (25) is supported by discovery computations but has
no exact proof.  In particular, neither (21) nor the original unrestricted
two-copy inequality is claimed proved here.

