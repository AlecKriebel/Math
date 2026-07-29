# The two-copy qutrit bridge: tangent maps and a singular-pencil residual

Scope: exact first-principles resolution of the two-copy qutrit
correlation inequality.  Sections 1--10 record the reductions that led
to the proof.  Sections 11--12 prove the decisive rank-two reduction
inequality, the reversed-Hodge contraction, and finally the complete
two-copy theorem.

## 1. The correlation inequality and its tangent-map adjoint

Let
\[
P=|X_1\rangle\!\rangle\langle\!\langle X_1|
  +|X_2\rangle\!\rangle\langle\!\langle X_2|,
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
For traceless \(A,B\in M_3\), first isolate the correlation inequality
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
This is the tangent (\(z=0\)) part of the complete singular-value dual.
The scalar dual coordinate is restored explicitly in Corollary 12.2.

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
Since \(G_D>0\), the complete tangent (\(z=0\)) part of the two-copy
qutrit problem is exactly equivalent to the following one-matrix
statement:
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
3. In that gauge the complete tangent theorem is equivalent to the
   explicit \(9\times9\) residual (21).
4. The determinant formula (19), the flattening-minor interpretation
   (23)--(24), and the equality obstruction (28)--(31) are exact.

### Conjectural at this stage of the log

The determinant gap (25) is supported by discovery computations but has
no exact proof.  The later argument in Sections 11--12 proves the
original unrestricted two-copy inequality by a different route, and
therefore proves positivity of (21), but it does not prove the stronger
determinant gap (25).

## 7. Exact four-channel Hodge--Fierz reduction

There is a second, substantially more structured reduction of the same
problem.  It shows that the only negative part of the adjoint defect (8)
has rank two.

Use the following real orthogonal basis of \(M_2(\mathbb R)\):
\[
\sigma_0=\begin{pmatrix}1&0\\0&1\end{pmatrix},\quad
\sigma_1=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
\sigma_2=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
\sigma_3=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\tag{32}
\]
Thus \(\sigma_\mu^T\sigma_\mu=I_2\), while
\[
\det\sigma_0=\det\sigma_3=1,\qquad
\det\sigma_1=\det\sigma_2=-1.
\tag{33}
\]
For an arbitrary pair \(Y=(Y_1,Y_2)\), define
\[
\begin{aligned}
L_\mu&=\sum_{r,s=1}^2(\sigma_\mu)_{rs}Y_rX_s^\dagger,\\
R_\mu&=\sum_{r,s=1}^2(\sigma_\mu)_{rs}X_s^\dagger Y_r,\\
C_\mu&=\sum_{r,s=1}^2(\sigma_\mu)_{rs}(Y_r\times X_s),\\
t_\mu&=\operatorname{Tr}L_\mu=\operatorname{Tr}R_\mu ,
\end{aligned}
\tag{34}
\]
where the mixed qutrit cross product is the complex-bilinear map in
(26).  Put
\[
\mathfrak a_\mu
=\|C_\mu\|_2^2+\|L_\mu\|_2^2+\|R_\mu\|_2^2-|t_\mu|^2.
\tag{35}
\]

**Lemma 7.1 (determinant-polarization identity).**
If \(X_1,X_2\) are Hilbert--Schmidt orthonormal, then
\[
\boxed{\qquad
\mathfrak a_0=\mathfrak a_3,\qquad
\mathfrak a_1=\mathfrak a_2,\qquad
\sum_{\mu=0}^3\mathfrak a_\mu=4\sum_{r=1}^2\|Y_r\|_2^2 .
\qquad}
\tag{36}
\]

**Proof.**
For a real \(2\times2\) matrix \(M=(M_{rs})\), define \(L_M,R_M,C_M,t_M\)
by replacing \(\sigma_\mu\) with \(M\) in (34), and put
\[
\mathfrak a(M)=
\|C_M\|^2+\|L_M\|^2+\|R_M\|^2-|t_M|^2.
\]
This is a real homogeneous quadratic form in the four entries of \(M\).
If \(M=pq^T\) has real rank one, set
\[
Y(p)=p_1Y_1+p_2Y_2,\qquad X(q)=q_1X_1+q_2X_2.
\]
Then
\[
(C_M,L_M,R_M,t_M)
=\left(
Y(p)\times X(q),\,
Y(p)X(q)^\dagger,\,
X(q)^\dagger Y(p),\,
\langle X(q),Y(p)\rangle
\right).
\]
The mixed Lagrange identity (27) therefore gives
\[
\mathfrak a(pq^T)=\|Y(p)\|^2\|X(q)\|^2
=\|q\|^2\|Y(p)\|^2,                         \tag{37}
\]
where orthonormality of \(X_1,X_2\) was used in the last equality.

On the other hand,
\[
\mathfrak b(M)=
\sum_{s=1}^2\left\|\sum_{r=1}^2M_{rs}Y_r\right\|^2
\tag{38}
\]
is a quadratic form with the same value as (37) on every real rank-one
matrix.  A homogeneous quadratic polynomial in the four entries of a
\(2\times2\) real matrix which vanishes on every rank-one matrix is a
scalar multiple of its determinant.  (Substitution
\(M=(p_1,p_2)^T(q_1,q_2)\) and coefficient comparison proves this
elementary assertion.)  Hence, for a real scalar \(\kappa\) depending on
\(X,Y\),
\[
\mathfrak a(M)=\mathfrak b(M)+\kappa\det M.                \tag{39}
\]
For every matrix in (32), orthogonality gives
\(\mathfrak b(\sigma_\mu)=\sum_r\|Y_r\|^2\).  The determinant signs (33)
now give
\[
\mathfrak a_0=\mathfrak a_3=N+\kappa,\qquad
\mathfrak a_1=\mathfrak a_2=N-\kappa,\qquad
N=\sum_r\|Y_r\|^2,
\]
which is (36). \(\square\)

The adjoint defect has the following exact form.

**Proposition 7.2 (two-scalar Gram domination).**
\[
\boxed{
\begin{aligned}
&2\sum_r\|Y_r\|^2
-\|(L_0)_0\|^2-\|(R_0)_0\|^2\\
&\quad=
\|C_0\|^2+\|C_1\|^2
+\|(L_1)_0\|^2+\|(R_1)_0\|^2
-\frac13\bigl(|t_0|^2+|t_1|^2\bigr).
\end{aligned}}
\tag{40}
\]
Consequently the tangent part of the two-copy qutrit theorem is
equivalent to the single rank-two-output inequality
\[
\boxed{\quad
|t_0|^2+|t_1|^2
\le3\left(
\|C_0\|^2+\|C_1\|^2+
\|(L_1)_0\|^2+\|(R_1)_0\|^2
\right).
\quad}
\tag{41}
\]

**Proof.**
By (36),
\[
2\sum_r\|Y_r\|^2=\mathfrak a_0+\mathfrak a_1.
\]
Also
\[
\|(L_0)_0\|^2+\|(R_0)_0\|^2
=\|L_0\|^2+\|R_0\|^2-\frac23|t_0|^2
=\mathfrak a_0-\|C_0\|^2+\frac13|t_0|^2.
\]
Subtracting, and using
\[
\mathfrak a_1
=\|C_1\|^2+\|(L_1)_0\|^2+\|(R_1)_0\|^2-\frac13|t_1|^2,
\]
proves (40).  Equation (41) is exactly the assertion that its right-hand
side is nonnegative. \(\square\)

This is not merely another expansion of the alternating partial-trace
formula.  The positive part in (40) is a Gram norm, and the entire
negative part is the squared norm of only two scalar functionals.
Equivalently, if
\[
\mathcal F_XY=(C_0,C_1,(L_1)_0,(R_1)_0),\qquad
\tau_XY=(t_0,t_1),
\tag{42}
\]
then the remaining theorem is
\[
\|\tau_XY\|^2\le3\|\mathcal F_XY\|^2.                     \tag{43}
\]
When the range condition
\(\operatorname{ran}\tau_X^\dagger\subseteq
\operatorname{ran}(\mathcal F_X^\dagger\mathcal F_X)\) holds, (43) is
equivalent, by an elementary Schur complement, to the \(2\times2\)
condition
\[
\boxed{\quad
\tau_X(\mathcal F_X^\dagger\mathcal F_X)^+\tau_X^\dagger
\preceq3I_2 .
\quad}
\tag{44}
\]
Here \(+\) denotes the Moore--Penrose inverse.  Thus (44), together with
the displayed range condition in singular cases, replaces the
\(9\times9\) residual (21) by a two-dimensional generalized-eigenvalue
test.  It remains unproved uniformly in \(X\).

## 8. Singular-pencil form of the two-scalar inequality

Choose an orthonormal singular-pencil frame \((D,Z)\) as in (12)--(13),
and apply the inverse Hadamard rotation
\[
X_1=\frac{D+Z}{\sqrt2},\qquad X_2=\frac{D-Z}{\sqrt2}.
\tag{45}
\]
For an arbitrary \(Y\), similarly put
\[
y=\frac{Y_1+Y_2}{\sqrt2},\qquad
w=\frac{Y_1-Y_2}{\sqrt2}.
\tag{46}
\]
Direct bilinearity gives
\[
\begin{aligned}
C_0&=y\times D+w\times Z,&
C_1&=y\times D-w\times Z,\\
L_1&=yD^\dagger-wZ^\dagger,&
R_1&=D^\dagger y-Z^\dagger w,\\
t_0&=\langle D,y\rangle+\langle Z,w\rangle,&
t_1&=\langle D,y\rangle-\langle Z,w\rangle.
\end{aligned}
\tag{47}
\]
Therefore (41) is exactly the following one-line Hodge inequality:
\[
\boxed{
\begin{aligned}
&2\|y\times D\|^2+2\|w\times Z\|^2\\
&\quad+\|(yD^\dagger-wZ^\dagger)_0\|^2
+\|(D^\dagger y-Z^\dagger w)_0\|^2\\
&\qquad\ge
\frac23\left(
|\langle D,y\rangle|^2+|\langle Z,w\rangle|^2
\right).
\end{aligned}}
\tag{48}
\]
All variables \(D,Z\) in (48) are subject only to the explicit
singular-pencil equations (12)--(13).  This is the smallest current exact
bottleneck: four manifest Hodge/product squares must dominate two scalar
overlaps.  A violation reconstructs an exact counterexample immediately.

## 9. Exact determinant gap for diagonal code planes

The conjectural determinant lower bound (25) can be proved completely
when the code plane has an orthonormal diagonal frame.  This calculation
also proves that the coefficient in (25) is asymptotically sharp.

Let
\[
X_s=\operatorname{diag}(x_{s1},x_{s2},x_{s3}),\qquad
r_i=\sum_{s=1}^2|x_{si}|^2.
\tag{49}
\]
The \(2\times3\) matrix \((x_{si})\) has orthonormal rows.  Its three
column vectors form a Parseval frame in \(\mathbb C^2\), so
\[
0\le r_i\le1,\qquad \sum_i r_i=2.
\tag{50}
\]
Put \(q_i=1-r_i\).  Then \(q_i\ge0\) and \(\sum_iq_i=1\).

The off-diagonal matrix-unit sectors of \(\mathcal T_X^\dagger\mathcal
T_X\) have largest eigenvalue \(1\).  Indeed, for \(i\ne j\) their Gram
matrix is the Gram matrix of the \(i\)-th and \(j\)-th Parseval-frame
columns; its eigenvalues are \(1\) and \(q_k\), where
\(\{i,j,k\}=\{1,2,3\}\).

On diagonal traceless pairs, only the sum of the two diagonal input
vectors occurs.  Hence the largest eigenvalue on that sector is
\[
2\mu_{\max},\qquad
\mu_{\max}=
\lambda_{\max}\!\left(
P_{\mathbf1^\perp}\operatorname{diag}(r_1,r_2,r_3)
P_{\mathbf1^\perp}
\right).
\tag{51}
\]
If \(\nu\) is the smaller eigenvalue of
\(P_{\mathbf1^\perp}\operatorname{diag}(q_i)P_{\mathbf1^\perp}\), then
\(\mu_{\max}=1-\nu\).  Since the two eigenvalues of the latter compression
have sum \(2/3\) and product \(e_2(q)/3\),
\[
e_2(q)=2\nu-3\nu^2.                                      \tag{52}
\]
Moreover
\[
\det\rho_L=\det\rho_R=\prod_i r_i
=\prod_i(1-q_i)=e_2(q)-e_3(q).                            \tag{53}
\]
The diagonal sector dominates the off-diagonal eigenvalue because
\(\mu_{\max}\ge2/3\).  Therefore
\[
\begin{aligned}
2-\|\mathcal T_X\|^2-\det\rho_L
&=2\nu-\bigl(e_2(q)-e_3(q)\bigr)\\
&=\boxed{\,3\nu^2+e_3(q)\,}\ge0.                          \tag{54}
\end{aligned}
\]
Thus (25) holds in this class.  If
\(q=(1-\varepsilon,\varepsilon/2,\varepsilon/2)\), then the quotient of
the two sides of the determinant lower bound tends to \(1\) as
\(\varepsilon\downarrow0\), proving sharpness of the coefficient even
inside the diagonal family.

## 10. Polarized Hodge collapse to one scalar

The two scalar losses in (48) can in fact be combined into one.  The
needed identity is the fully polarized form of (27):
\[
\begin{aligned}
\langle A\times B,C\times E\rangle
={}&\langle A,C\rangle\langle B,E\rangle
  +\langle A,E\rangle\langle B,C\rangle\\
 &-\operatorname{Tr}(A^\dagger C B^\dagger E)
  -\operatorname{Tr}(A^\dagger E B^\dagger C).
\end{aligned}                                             \tag{55}
\]
It follows either by polarizing (27), or directly by contracting the two
Levi--Civita symbols in (26).

Apply (55) to \(A=y,B=Z,C=w,E=D\), and use
\(\langle Z,D\rangle=0\).  With
\[
p=\langle D,y\rangle,\qquad q=\langle Z,w\rangle,
\tag{56}
\]
cyclicity of trace and removal of scalar parts give the exact identity
\[
\boxed{
\begin{aligned}
&\langle (yD^\dagger)_0,(wZ^\dagger)_0\rangle
 +\langle (D^\dagger y)_0,(Z^\dagger w)_0\rangle\\
&\hspace{28mm}
=\frac13\overline p\,q-\langle y\times Z,w\times D\rangle .
\end{aligned}}                                             \tag{57}
\]
Expanding the two differences in (48), inserting (57), and using (27)
once for \((y,D)\) and once for \((w,Z)\) yields:
\[
\boxed{
\begin{aligned}
\mathfrak D_{D,Z}(y,w)
={}&\|y\|^2+\|w\|^2+\|y\times D\|^2+\|w\times Z\|^2\\
 &+2\operatorname{Re}\langle y\times Z,w\times D\rangle
 -\frac13\left|\langle D,y\rangle+\langle Z,w\rangle\right|^2 .
\end{aligned}}                                             \tag{58}
\]
Here \(\mathfrak D_{D,Z}(y,w)\) denotes the left side of (48) minus its
right side.  Thus the tangent part of the qutrit two-copy problem is
equivalently the nonnegativity of (58).  The full scalar-dual coordinate
requires the stronger lower bound established in Section 12.

This form improves the structural bottleneck in two ways.  First, only
one scalar functional remains negative.  Second, the coupled Hodge term
has the reversed order
\(\langle y\times Z,w\times D\rangle\); it cannot be estimated by
treating the two code vectors independently.

For later use, define \(\mathcal C_D(y)=y\times D\).  The positive part
of (58), before its final rank-one subtraction, has block matrix
\[
\mathcal M_0=
\begin{pmatrix}
I+\mathcal C_D^\dagger\mathcal C_D&
\mathcal C_Z^\dagger\mathcal C_D\\
\mathcal C_D^\dagger\mathcal C_Z&
I+\mathcal C_Z^\dagger\mathcal C_Z
\end{pmatrix}.                                             \tag{59}
\]
Discovery calculations suggest the auxiliary contraction
\[
\|\mathcal C_Z^\dagger\mathcal C_D\|\le1
\quad\text{when }\langle D,Z\rangle=0,\ \det D=0,           \tag{60}
\]
but (60) is not yet proved.  Even if established, the remaining exact
task would still be the rank-one domination
\[
\mathcal M_0\succeq
\frac13\,|(D,Z)\rangle\langle(D,Z)|.                        \tag{61}
\]

One tempting one-variable route to (61) is false.  Namely,
\[
\|y\times Z\|^2-\|y\times D\|^2
+\frac23|\langle D,y\rangle|^2\le\|y\|^2                  \tag{62}
\]
does not hold.  The exact orthonormal singular frame
\[
D=E_{11},\qquad Z=E_{22},\qquad y=E_{11}
\]
has left side \(1+2/3=5/3\) and right side \(1\).  Any proof of (58)
must therefore keep the paired \(y,w\) geometry.

## 11. Exact rank-two qutrit reduction inequality

The conjectural cross contraction (60) is true, and it follows from a
dimension-specific operator inequality of independent interest.

**Theorem 11.1.**  Let \(P\) be an orthogonal projection of rank exactly
two on \(\mathbb C^3\otimes\mathbb C^3\), and put
\[
\rho_A=\operatorname{Tr}_B P,\qquad
\rho_B=\operatorname{Tr}_A P.
\]
Then
\[
\boxed{\qquad
P\preceq \rho_A\otimes I+I\otimes\rho_B .
\qquad}                                                    \tag{63}
\]

**Proof.**
Fix a test vector \(\psi\), and denote its reduced operators by
\(\sigma_A,\sigma_B\).  Cyclicity of trace gives
\[
\begin{aligned}
&\langle\psi|
  P-\rho_A\otimes I-I\otimes\rho_B
 |\psi\rangle\\
&\qquad
=\operatorname{Tr}P\,
\bigl(|\psi\rangle\langle\psi|
      -\sigma_A\otimes I-I\otimes\sigma_B\bigr).
\end{aligned}                                             \tag{64}
\]
Local unitaries put
\[
\psi=\sum_{i=1}^3s_i|ii\rangle,\qquad
s_i\ge0.
\]
Write \(x_i=s_i^2\), and order \(x_1\ge x_2\ge x_3\).  On the
off-diagonal vectors \(|ij\rangle\), \(i\ne j\), the operator
\[
\mathcal K_\psi=
|\psi\rangle\langle\psi|-\sigma_A\otimes I-I\otimes\sigma_B
\tag{65}
\]
has eigenvalues
\[
-(x_i+x_j).
\tag{66}
\]
On \(\operatorname{span}\{|11\rangle,|22\rangle,|33\rangle\}\), its
matrix is
\[
H=ss^T-2\operatorname{diag}(x_1,x_2,x_3),
\qquad s=(s_1,s_2,s_3)^T.                                 \tag{67}
\]

Put \(S=x_1+x_2+x_3\).  The matrix \(H+SI\) is positive semidefinite.
Indeed, its diagonal principal minors are \(S-x_i\), its principal
\(2\times2\) minors are \(x_kS\), where \(k\) is the omitted index, and
\[
\det(H+SI)=4x_1x_2x_3.                                   \tag{68}
\]
Thus, if \(\lambda_1(H)\ge\lambda_2(H)\ge\lambda_3(H)\),
\[
\lambda_1(H)+\lambda_2(H)
=\operatorname{Tr}H-\lambda_3(H)
=-S-\lambda_3(H)\le0.                                    \tag{69}
\]

It remains to check that an off-diagonal eigenvalue cannot replace
\(\lambda_2(H)\) and spoil (69).  Put \(m=x_2+x_3\).  If \(m=0\), this
is immediate.  If \(m>0\), the rank-one criterion for
\[
mI-H=mI+2\operatorname{diag}(x_i)-ss^T
\]
says that this matrix is positive semidefinite exactly when
\[
\sum_{i=1}^3\frac{x_i}{m+2x_i}\le1.
\]
Here the difference from one is the manifestly nonnegative quantity
\[
\frac{
x_1(x_2-x_3)^2+2(x_2+x_3)^3
}{
(2x_1+x_2+x_3)(3x_2+x_3)(x_2+3x_3)
}.                                                        \tag{70}
\]
Consequently \(\lambda_1(H)\le m\).  Every eigenvalue in (66) is at
most \(-m\), while (69) controls the two largest eigenvalues inside the
diagonal block.  Hence the sum of the two largest eigenvalues of
\(\mathcal K_\psi\) is nonpositive.

The rank-two Ky Fan variational principle now gives
\[
\operatorname{Tr}(P\mathcal K_\psi)
\le\lambda_1(\mathcal K_\psi)+\lambda_2(\mathcal K_\psi)
\le0.
\]
Together with (64), this proves (63). \(\square\)

The theorem gives the missing cross-product contraction without any
singular-pencil assumption.

**Corollary 11.2.**  If \(D,Z\in M_3\) are Hilbert--Schmidt orthonormal,
then
\[
\boxed{\quad
\mathcal C_D\mathcal C_D^\dagger+
\mathcal C_Z\mathcal C_Z^\dagger\preceq2I,
\qquad
\|\mathcal C_Z^\dagger\mathcal C_D\|\le1.
\quad}                                                     \tag{71}
\]

**Proof.**
Apply the mixed Lagrange identity (27) to
\(\mathcal C_D^\dagger U\) and \(\mathcal C_Z^\dagger U\), and sum.
With the vectorization convention
\(|X\rangle\!\rangle=\sum_{ij}X_{ij}|i\,j\rangle\), the result is the
exact identity
\[
\begin{aligned}
2\|U\|^2
&-\|\mathcal C_D^\dagger U\|^2
 -\|\mathcal C_Z^\dagger U\|^2\\
&=
\langle\!\langle\overline U|
\bigl(\rho_A\otimes I+I\otimes\rho_B-P\bigr)
|\overline U\rangle\!\rangle ,
\end{aligned}
\]
where
\[
P=|D\rangle\!\rangle\langle\!\langle D|
 +|Z\rangle\!\rangle\langle\!\langle Z|
\]
and \(\rho_A,\rho_B\) are its physical marginals.  (The transpose in
the second marginal is already built into this row-vectorization
formula.)  Theorem 11.1 proves that the displayed right side is
nonnegative.  This proves the first inequality in (71).  Set
\(G=\mathcal C_D^\dagger\mathcal C_D\).  The first inequality gives
\[
\begin{aligned}
(\mathcal C_Z^\dagger\mathcal C_D)^\dagger
(\mathcal C_Z^\dagger\mathcal C_D)
&\preceq
\mathcal C_D^\dagger
(2I-\mathcal C_D\mathcal C_D^\dagger)
\mathcal C_D\\
&=2G-G^2
\preceq I,
\end{aligned}
\]
where the last step is \(I-(2G-G^2)=(I-G)^2\succeq0\). \(\square\)

In particular, the block matrix
\[
\begin{pmatrix}
I&\mathcal C_Z^\dagger\mathcal C_D\\
\mathcal C_D^\dagger\mathcal C_Z&I
\end{pmatrix}
\]
is positive semidefinite.  Adding the two diagonal Hodge squares proves
\(\mathcal M_0\succeq0\) in (59).  The only remaining part of the full
two-copy qutrit theorem is therefore the rank-one strengthening (61);
the entire reversed-Hodge cross term itself is now controlled exactly.

## 12. Completion of the two-copy theorem

The rank-one strengthening is also exact, with the better coefficient
\(1/2\) in place of \(1/3\).

**Theorem 12.1 (strong reversed-Hodge inequality).**
For every Hilbert--Schmidt orthonormal pair \(D,Z\in M_3\) and all
\(y,w\in M_3\),
\[
\boxed{
\begin{aligned}
&\|y\|^2+\|w\|^2+\|y\times D\|^2+\|w\times Z\|^2\\
&\qquad
+2\operatorname{Re}\langle y\times Z,w\times D\rangle\\
&\hspace{18mm}\ge
\frac12\left|\langle D,y\rangle+\langle Z,w\rangle\right|^2 .
\end{aligned}}                                             \tag{72}
\]

**Proof.**
Use the operators
\[
A=\mathcal C_D^\dagger\mathcal C_D,\qquad
B=\mathcal C_Z^\dagger\mathcal C_Z,\qquad
K=\mathcal C_Z^\dagger\mathcal C_D.                        \tag{73}
\]
The first inequality in (71) implies
\[
K^\dagger K
=\mathcal C_D^\dagger\mathcal C_Z
 \mathcal C_Z^\dagger\mathcal C_D
\preceq
\mathcal C_D^\dagger
(2I-\mathcal C_D\mathcal C_D^\dagger)
\mathcal C_D
=2A-A^2.
\tag{74}
\]
Consequently
\[
I-K^\dagger K\succeq(I-A)^2.                              \tag{75}
\]
Symmetry of the mixed cross product gives
\(\mathcal C_DZ=\mathcal C_ZD\).  Hence
\[
K^\dagger D
=\mathcal C_D^\dagger\mathcal C_ZD
=\mathcal C_D^\dagger\mathcal C_DZ
=AZ.
\tag{76}
\]
Put
\[
r=Z-K^\dagger D=(I-A)Z,\qquad
R=I+B-K^\dagger K.                                        \tag{77}
\]
Because \(\|Z\|=1\), (75) gives the rank-one chain
\[
R\succeq I-K^\dagger K
\succeq(I-A)^2
\succeq |r\rangle\langle r|.                              \tag{78}
\]

The left side of (72) has the exact completion
\[
\begin{aligned}
\mathcal B(y,w)
&=\|y+Kw\|^2+\|\mathcal C_Dy\|^2+\langle w,Rw\rangle .
\end{aligned}                                             \tag{79}
\]
On the other hand, (76)--(77) give
\[
\langle D,y\rangle+\langle Z,w\rangle
=\langle D,y+Kw\rangle+\langle r,w\rangle .                \tag{80}
\]
Equations (78)--(80), \(\|D\|=1\), and the two-term
Cauchy--Schwarz inequality now yield
\[
\begin{aligned}
\mathcal B(y,w)
&\ge
|\langle D,y+Kw\rangle|^2+|\langle r,w\rangle|^2\\
&\ge
\frac12
\left|\langle D,y\rangle+\langle Z,w\rangle\right|^2.
\end{aligned}
\]
This is (72). \(\square\)

Combining (58) and (72) proves the endpoint theorem.

**Corollary 12.2 (unrestricted two-copy qutrit positivity).**
For every rank-at-most-two \(C\in M_{3^2}\),
\[
\boxed{\qquad
Q_2(C)=
\|C\|_2^2-\frac12\bigl(
\|\operatorname{Tr}_1C\|_2^2+
\|\operatorname{Tr}_2C\|_2^2\bigr)
+\frac14|\operatorname{Tr}C|^2
\ge0.
\qquad}                                                    \tag{81}
\]
Equivalently, the qutrit Werner endpoint is two-copy undistillable.

**Proof.**
For completeness, include the scalar dual variable which was suppressed
in the tangent-map notation (4).  Define
\[
\widehat{\mathcal T}_X(A,B,z)_r
=BX_r+X_rA+\frac z{\sqrt6}X_r .
\]
Its adjoint is
\[
\widehat{\mathcal T}_X^\dagger(Y)
=\left((R_Y)_0,(L_Y)_0,\frac{t_Y}{\sqrt6}\right).
\tag{82}
\]
Thus the full two-copy inequality is equivalent to
\[
2\sum_r\|Y_r\|^2-\|(L_Y)_0\|^2-\|(R_Y)_0\|^2
\ge\frac16|t_Y|^2.                                       \tag{83}
\]
The exact reductions in Sections 7--10 identify the left side of (83)
with (58), and identify \(t_Y\), after the Hadamard rotation, with
\(\langle D,y\rangle+\langle Z,w\rangle\).  By (72), the positive part
of (58) is at least one half of this scalar square.  Therefore
\[
\mathfrak D_{D,Z}(y,w)
\ge
\left(\frac12-\frac13\right)
\left|\langle D,y\rangle+\langle Z,w\rangle\right|^2
\ge\frac16|t_Y|^2.                                        \tag{84}
\]
This is exactly (83), hence proves the full singular-value dual and
therefore (81).  In particular it also proves positivity of the tangent
residual (21). \(\square\)

The proof also explains the zero manifold.  Equality in the original
two-copy inequality forces the scalar in (84) to vanish in addition to
equality in both Cauchy--Schwarz steps of Theorem 12.1.  In particular,
the common-\(2\times2\)-support example (28)--(30) survives because its
scalar overlap sum is zero; a strictly positive gap could never have
captured that family.
