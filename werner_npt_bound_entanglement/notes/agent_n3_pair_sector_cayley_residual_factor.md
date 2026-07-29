# Cayley residual factorization of the pair-sector determinant

## Status

This note gives two lossless algebraic rewrites of the remaining
three-component determinant
\[
 \det M\geq0
\]
and exactly disproves the most immediate termwise-positive reading of
the first rewrite.

The scalar three-cycle can be expressed through three positive
physical residual Grams and two coherent cubic contractions of the
same logical frame.  Independently, polarizing Cayley--Hamilton on the
three logical residuals expresses \(\det M\) as three pair terms minus
one coherent cubic term.

The pair terms in the latter formula are **not** individually
nonnegative.  An exact qutrit code with exact doubly-traceless pair
coefficients has
\[
 \Delta_{12}=-\frac{14}{81},
\]
while its genuine scalar deficit is strictly positive and
\[
 \det M=\frac89.
\]
Thus any proof through the polarized formula must retain the logical
spin-flip compensation and the cubic term.

This is a proof-mechanism obstruction, not a negative pair-sector or
Werner witness.  The dependency-free checker is
`verification/verify_n3_pair_sector_cayley_residual_factor.py`.

## 1. Common-frame notation

Let
\[
 V:\mathbb C^2\longrightarrow(\mathbb C^3)^{\otimes3}
\]
be an isometry.  For the three doubly-traceless pair coefficients put
\[
 D_{\widehat i}=I_i\otimes B_{\widehat i},\qquad
 X_i=D_{\widehat i}V,\qquad
 b_i=\|B_{\widehat i}\|_2^2.
\]
Write
\[
 A_{ij}=X_i^\dagger X_j,\qquad
 c_{ij}=\operatorname{Tr}A_{ij},
\]
and define the logical residuals
\[
 E_i=b_iI_2-A_{ii},\qquad
 d_i=\operatorname{Tr}E_i
     =2b_i-\operatorname{Tr}A_{ii}.                    \tag{1}
\]
The scalar deficit matrix is
\[
 M_{ii}=d_i,\qquad M_{ij}=-c_{ij}\quad(i\ne j).         \tag{2}
\]

Both the logical and physical residuals are positive:
\[
 E_i\succeq0,\qquad
 R_i:=b_iI_{27}-X_iX_i^\dagger\succeq0.                \tag{3}
\]
Indeed,
\[
\begin{aligned}
 X_iX_i^\dagger
 &=D_{\widehat i}VV^\dagger D_{\widehat i}^\dagger\\
 &\preceq D_{\widehat i}D_{\widehat i}^\dagger
 =I_i\otimes B_{\widehat i}B_{\widehat i}^\dagger\\
 &\preceq \|B_{\widehat i}\|_{\rm op}^2I
 \preceq b_iI.
\end{aligned}
\]
The logical assertion follows in the same way from
\(X_i^\dagger X_i\preceq b_iI_2\).

For each fixed residual label \(i\), define
\[
 g^{(i)}_{jk}
 =\operatorname{Tr}\!\left(X_j^\dagger R_iX_k\right).
                                                               \tag{4}
\]
Then
\[
 G^{(i)}=[g^{(i)}_{jk}]_{j,k=1}^3\succeq0,              \tag{5}
\]
because it is the scalar Gram matrix of the three matrices
\(R_i^{1/2}X_j\).  Direct expansion gives the exact common-frame
identity
\[
 \boxed{
 g^{(i)}_{jk}
 =b_i c_{jk}-\operatorname{Tr}(A_{ji}A_{ik}).
 }                                                       \tag{6}
\]

## 2. Polarized Cayley--Hamilton on the logical residuals

For arbitrary \(2\times2\) matrices \(K_1,K_2,K_3\),
\[
\begin{aligned}
 \operatorname{Tr}K_1\operatorname{Tr}K_2\operatorname{Tr}K_3
={}&
 \operatorname{Tr}(K_1K_2)\operatorname{Tr}K_3\\
&+\operatorname{Tr}(K_1K_3)\operatorname{Tr}K_2\\
&+\operatorname{Tr}(K_2K_3)\operatorname{Tr}K_1\\
&-\operatorname{Tr}(K_1K_2K_3)
 -\operatorname{Tr}(K_1K_3K_2).
\end{aligned}                                           \tag{7}
\]
This is the complete polarization of Cayley--Hamilton in dimension
two, equivalently the contraction of
\(\bigwedge^3\mathbb C^2=0\).

Apply (7) to \(E_1,E_2,E_3\).  Since the \(E_i\) are Hermitian, the
two ordered cubic traces are complex conjugates.  Define
\[
 \Delta_{ij}
 =\operatorname{Tr}(E_iE_j)-|c_{ij}|^2.                 \tag{8}
\]
Substitution into the ordinary scalar determinant formula gives
\[
\boxed{
\begin{aligned}
 \det M
={}&d_3\Delta_{12}+d_2\Delta_{13}+d_1\Delta_{23}\\
 &\quad
 -2\operatorname{Re}\!\left[
   \operatorname{Tr}(E_1E_2E_3)
   +c_{12}c_{23}c_{31}\right].
\end{aligned}}                                          \tag{9}
\]
No inequality has been used.  Formula (9) is a lossless
common-logical-plane reformulation of the determinant.

The relation with the already proved two-component minors is
instructive.  Let
\[
 {\mathfrak s}(H)=(\operatorname{Tr}H)I_2-H
\]
be the logical spin flip.  Since \(E_j\succeq0\), also
\({\mathfrak s}(E_j)\succeq0\), and
\[
\boxed{
 d_id_j-|c_{ij}|^2
 =
 \Delta_{ij}
 +\operatorname{Tr}\!\left(E_i{\mathfrak s}(E_j)\right).
 }                                                       \tag{10}
\]
Thus positivity of the true \(2\times2\) scalar minor does not imply
\(\Delta_{ij}\geq0\): the missing amount can lie entirely in the
spin-flipped logical channel.

## 3. Exact physical residual expansion of the scalar cycle

Apply (7) instead to
\[
 K_1=A_{12},\qquad K_2=A_{23},\qquad K_3=A_{31}.
\]
Put
\[
 T_+=\operatorname{Tr}(A_{12}A_{23}A_{31}),\qquad
 T_\times=\operatorname{Tr}(A_{12}A_{31}A_{23}).        \tag{11}
\]
The first cubic is also
\[
 T_+=\operatorname{Tr}\!\left(
 X_1X_1^\dagger X_2X_2^\dagger X_3X_3^\dagger
 \right);
\]
the second is the genuinely crossed logical contraction.

Using (6) in the three quadratic trace terms of (7) yields
\[
\boxed{
\begin{aligned}
 c_{12}c_{23}c_{31}
={}&b_2|c_{13}|^2+b_1|c_{23}|^2+b_3|c_{12}|^2\\
&-g^{(2)}_{13}c_{31}
 -g^{(1)}_{32}c_{23}
 -g^{(3)}_{21}c_{12}\\
&-T_+-T_\times .
\end{aligned}}                                          \tag{12}
\]
Every \(G^{(i)}\) in this identity is a positive physical residual
Gram.  Equation (12) therefore retains substantially more common
origin than an independent bound on the three scalar edges.

Combining (12) with the determinant formula gives another lossless
form:
\[
\boxed{
\begin{aligned}
 \det M
={}&d_1d_2d_3
 -(d_1+2b_1)|c_{23}|^2
 -(d_2+2b_2)|c_{13}|^2\\
& -(d_3+2b_3)|c_{12}|^2\\
&+2\operatorname{Re}\!\left(
 g^{(2)}_{13}c_{31}
 +g^{(1)}_{32}c_{23}
 +g^{(3)}_{21}c_{12}
 +T_++T_\times
 \right).
\end{aligned}}                                          \tag{13}
\]
Equations (9) and (13) are equivalent; they expose complementary
logical and physical residual structures.  Neither formula has yet
been turned into a global positive certificate.

## 4. Exact physical counterexample to \(\Delta_{ij}\geq0\)

Let
\[
 V|0\rangle=|000\rangle,\qquad
 V|1\rangle=|110\rangle.                                \tag{14}
\]
On one qutrit define
\[
 Z=\operatorname{diag}(1,-1,0),\qquad
 E=|1\rangle\langle0|,\qquad
 T=|1\rangle\langle2|.                                  \tag{15}
\]
All three are traceless.  Take
\[
\begin{aligned}
 B_{\widehat1}
 &=\frac23 Z\otimes E+\frac13T\otimes T,\\
 B_{\widehat2}
 &=\frac23 Z\otimes E+\frac13T\otimes T,\\
 B_{\widehat3}
 &=T\otimes T,                                          \tag{16}
\end{aligned}
\]
where in each line the tensor factors are the two nonspectator sites
in increasing order.  Every summand is a tensor product of traceless
matrices, hence every \(B_{\widehat i}\) is doubly traceless.
Orthogonality of the displayed summands gives
\[
 b_1=b_2=b_3=1.                                         \tag{17}
\]

The \(T\otimes T\) terms annihilate both code columns.  Direct action
therefore gives
\[
\begin{array}{c|cc}
 &V|0\rangle&V|1\rangle\\ \hline
 X_1&\frac23|001\rangle&-\frac23|111\rangle\\
 X_2&\frac23|001\rangle&-\frac23|111\rangle\\
 X_3&0&0.
\end{array}                                              \tag{18}
\]
Consequently
\[
\begin{aligned}
 A_{11}=A_{12}=A_{21}=A_{22}&=\frac49I_2,\\
 A_{i3}=A_{3i}&=0,
\end{aligned}
\]
and
\[
 E_1=E_2=\frac59I_2,\qquad E_3=I_2.                    \tag{19}
\]
Thus
\[
 (d_1,d_2,d_3)=\left(\frac{10}{9},\frac{10}{9},2\right),
 \qquad
 c_{12}=\frac89,\quad c_{13}=c_{23}=0.                 \tag{20}
\]

The failed pair term is
\[
\boxed{
 \Delta_{12}
 =2\left(\frac59\right)^2-\left(\frac89\right)^2
 =-\frac{14}{81}<0.
}                                                        \tag{21}
\]
Yet the true pair minor is strictly positive:
\[
 d_1d_2-|c_{12}|^2
 =\frac{4}{9}.                                          \tag{22}
\]
The missing spin-flip contribution in (10) is \(50/81\).

The full scalar deficit is
\[
 M=
\begin{pmatrix}
10/9&-8/9&0\\
-8/9&10/9&0\\
0&0&2
\end{pmatrix}\succ0,                                    \tag{23}
\]
with eigenvalues \(2/9,2,2\) and
\[
\boxed{\det M=\frac89>0.}                               \tag{24}
\]
Formula (9) checks the compensation exactly:
\[
\begin{aligned}
 d_3\Delta_{12}+d_2\Delta_{13}+d_1\Delta_{23}
 &=\frac{172}{81},\\
 \operatorname{Tr}(E_1E_2E_3)&=\frac{50}{81},\\
 c_{12}c_{23}c_{31}&=0,
\end{aligned}
\]
and hence
\[
 \frac{172}{81}-2\frac{50}{81}=\frac89.
\]

## 5. Consequence for the determinant program

The positive matrices \(E_i\), the positive physical residuals
\(R_i\), and the three positive residual Grams \(G^{(i)}\) are all
available simultaneously.  Nevertheless, neither the logical
Cayley pair terms \(\Delta_{ij}\) nor the unflipped logical residual
block can be declared positive separately.

A successful use of (9) must combine
\[
 \Delta_{ij},
 \quad
 \operatorname{Tr}(E_i{\mathfrak s}(E_j)),
 \quad\text{and}\quad
 \operatorname{Re}\!\left[
 \operatorname{Tr}(E_1E_2E_3)+c_{12}c_{23}c_{31}
 \right]
\]
before taking signs.  Equivalently, a successful use of (13) must
combine the three positive residual Grams with both ordered cubic
contractions \(T_+\) and \(T_\times\).  Bounding the six displayed
pieces independently discards exactly the common logical spin-flip
geometry seen in (21)--(24).
