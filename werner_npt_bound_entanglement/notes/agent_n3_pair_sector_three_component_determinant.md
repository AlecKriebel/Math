# The qutrit pair-sector frontier is a single three-component determinant

## Status

This note proves the sharp pair-sector inequality whenever at most two
of the three pair components are present.  Equivalently, it proves
that every \(1\times1\) and \(2\times2\) principal minor of the natural
three-component deficit matrix is nonnegative.

The proof uses the established unrestricted qutrit two-copy endpoint
theorem.  It leaves exactly one scalar obstruction:
\[
 \det M\geq0.                                             \tag{1}
\]
Thus it is a strict reduction of the three-copy pair-sector frontier,
not a proof of the unrestricted pair-sector inequality.

The dependency-free exact checker is
`verification/verify_n3_pair_sector_three_component_determinant.py`.

## 1. A sharp two-site degree-one theorem

On each qutrit operator factor let
\[
 {\cal P}(A)=\frac{\operatorname{Tr}A}{3}I_3,\qquad
 {\cal Q}=I-{\cal P}.                                    \tag{2}
\]
For a two-site coefficient matrix \(C\), write
\[
 \begin{aligned}
 w_0&=\|{\cal P}_1{\cal P}_2C\|_2^2,\\
 w_1&=\|({\cal Q}_1{\cal P}_2+
             {\cal P}_1{\cal Q}_2)C\|_2^2,\\
 w_2&=\|{\cal Q}_1{\cal Q}_2C\|_2^2.
 \end{aligned}                                           \tag{3}
\]
The summands in (3) are orthogonal and
\[
 \|C\|_2^2=w_0+w_1+w_2.                                  \tag{4}
\]
At the qutrit endpoint the two-copy form is
\[
 Q_2(C)=\frac14w_0-\frac12w_1+w_2.                       \tag{5}
\]
Consequently there is the exact identity
\[
 \boxed{\quad
 \frac23\|C\|_2^2-w_1
 =
 \frac23Q_2(C)+\frac12w_0 .
 \quad}                                                   \tag{6}
\]

The unrestricted two-copy endpoint theorem says \(Q_2(C)\geq0\)
whenever \(\operatorname{rank}C\leq2\).  Equation (6) therefore proves
\[
 \boxed{\quad
 \|({\cal Q}_1{\cal P}_2+
       {\cal P}_1{\cal Q}_2)C\|_2^2
 \leq\frac23\|C\|_2^2
 \qquad(\operatorname{rank}C\leq2).
 \quad}                                                   \tag{7}
\]
No estimate was used after (6), apart from the two manifestly
nonnegative quantities on its right.

The constant is sharp.  For example, with
\(E=|0\rangle\langle1|\) and
\(R=|0\rangle\langle0|+|1\rangle\langle1|\), the matrix
\[
 C=E\otimes R                                             \tag{8}
\]
has rank two and squared norm \(2\).  Its exact degree-one component
is \(E\otimes(2I_3/3)\), of squared norm \(4/3\).

## 2. Identity spectators preserve the theorem

Let \(C\) now act on three qutrit copies, and choose two sites \(a,c\)
and spectator site \(b\).  Expand \(C\) in the matrix-unit basis on
the spectator:
\[
 C=\sum_{\mu,\nu=0}^2 E_{\mu\nu}^{(b)}
       \otimes C_{\mu\nu}^{(ac)}.                         \tag{9}
\]
Each \(C_{\mu\nu}\) is a row-and-column compression of \(C\), hence
\[
 \operatorname{rank}C_{\mu\nu}
 \leq\operatorname{rank}C.                               \tag{10}
\]
Orthogonality of the matrix units and (7) give
\[
 \begin{aligned}
 \|(\Pi_1^{(ac)}\otimes I_b)C\|_2^2
 &=\sum_{\mu,\nu}\|\Pi_1^{(ac)}C_{\mu\nu}\|_2^2\\
 &\leq\frac23\sum_{\mu,\nu}\|C_{\mu\nu}\|_2^2
 =\frac23\|C\|_2^2,                                      \tag{11}
 \end{aligned}
\]
where
\[
 \Pi_1^{(ac)}
 ={\cal Q}_a{\cal P}_c+{\cal P}_a{\cal Q}_c.             \tag{12}
\]

Applying the orthogonal projection \({\cal Q}_b\) can only decrease
the norm.  Because it commutes with (12),
\[
 \boxed{\quad
 \|{\cal Q}_b\Pi_1^{(ac)}C\|_2^2
 \leq\frac23\|C\|_2^2
 \qquad(\operatorname{rank}C\leq2).
 \quad}                                                   \tag{13}
\]
But \({\cal Q}_b\Pi_1^{(ac)}\) is exactly the sum of the two
three-copy pair sectors
\[
 {\cal Q}_a{\cal Q}_b{\cal P}_c
 +
 {\cal P}_a{\cal Q}_b{\cal Q}_c.                         \tag{14}
\]
Thus the pair-sector theorem is proved whenever any one of its three
orthogonal components vanishes.

## 3. Dual two-component Gram matrices

Use the spectator notation
\[
 D_{\widehat i}=I_i\otimes B_{\widehat i},               \tag{15}
\]
where \(B_{\widehat i}\) is doubly traceless on the two sites other
than \(i\).  Let
\[
 V:\mathbb C^2\longrightarrow(\mathbb C^3)^{\otimes3}
 \quad\text{be an isometry},\qquad
 X_i=D_{\widehat i}V.                                    \tag{16}
\]
Define
\[
 d_i=2\|B_{\widehat i}\|_2^2-\|X_i\|_2^2,\qquad
 c_{ij}=\langle X_i,X_j\rangle.                          \tag{17}
\]

Primal-dual rank-two duality applied to (13) says that, for every two
distinct components \(i,j\) and every
\(\lambda_i,\lambda_j\in\mathbb C\),
\[
 \|(\lambda_iD_{\widehat i}+
       \lambda_jD_{\widehat j})V\|_2^2
 \leq
 2\bigl(
 |\lambda_i|^2\|B_{\widehat i}\|_2^2+
 |\lambda_j|^2\|B_{\widehat j}\|_2^2\bigr).              \tag{18}
\]
Indeed, the two embedded pair sectors are orthogonal and have
\[
 \|\lambda_iD_{\widehat i}+
       \lambda_jD_{\widehat j}\|_2^2
 =
 3\bigl(
 |\lambda_i|^2\|B_{\widehat i}\|_2^2+
 |\lambda_j|^2\|B_{\widehat j}\|_2^2\bigr),              \tag{19}
\]
while (13) is dual to the Ky--Fan bound with factor \(2/3\).
Finally \(\|DV\|_2^2\leq s_1(D)^2+s_2(D)^2\).

Expanding (18) proves the \(2\times2\) matrix inequality
\[
 \boxed{\quad
 \begin{pmatrix}
 d_i&-c_{ij}\\
 -\overline{c_{ij}}&d_j
 \end{pmatrix}\succeq0 .
 \quad}                                                   \tag{20}
\]
In particular,
\[
 d_i\geq0,\qquad |c_{ij}|^2\leq d_id_j.                  \tag{21}
\]
This is stronger than a bound on the real part of one fixed
interference term: it holds after arbitrary independent complex
rescaling of the two pair coefficients.

## 4. The unique remaining determinant

Put the three components into the Hermitian deficit matrix
\[
 M=
 \begin{pmatrix}
 d_1&-c_{12}&-c_{13}\\
 -\overline{c_{12}}&d_2&-c_{23}\\
 -\overline{c_{13}}&-\overline{c_{23}}&d_3
 \end{pmatrix}.                                         \tag{22}
\]
For arbitrary coefficients
\(\lambda=(\lambda_1,\lambda_2,\lambda_3)\),
\[
 \lambda^\dagger M\lambda
 =
 2\sum_i|\lambda_i|^2\|B_{\widehat i}\|_2^2
 -
 \left\|\sum_i\lambda_iD_{\widehat i}V\right\|_2^2.
                                                               \tag{23}
\]
Since arbitrary scalar coefficients can be absorbed into the
\(B_{\widehat i}\), the full pair-sector theorem is equivalent to
\[
 M\succeq0
 \quad\text{for every }V,B_{\widehat1},B_{\widehat2},
 B_{\widehat3}.                                         \tag{24}
\]

Equation (20) proves every principal minor of \(M\) of order at most
two.  A Hermitian \(3\times3\) matrix is positive semidefinite iff all
of its principal minors are nonnegative.  Hence (24) is now exactly
equivalent to the single inequality
\[
 \boxed{
 \begin{aligned}
 \det M
 ={}&d_1d_2d_3
 -d_1|c_{23}|^2
 -d_2|c_{13}|^2
 -d_3|c_{12}|^2\\
 &\quad
 -2\operatorname{Re}
 \bigl(c_{12}c_{23}\overline{c_{13}}\bigr)
 \geq0.
 \end{aligned}}                                         \tag{25}
\]
If some \(d_i=0\), (21) forces the two incident \(c_{ij}\) to vanish,
and (24) already follows from the remaining \(2\times2\) block.
Therefore the unresolved case may be normalized by \(d_i>0\).  With
\[
 r_{ij}=\frac{c_{ij}}{\sqrt{d_id_j}},                    \tag{26}
\]
it is the triangle inequality
\[
 \boxed{\quad
 1-|r_{12}|^2-|r_{23}|^2-|r_{13}|^2
 -2\operatorname{Re}
   (r_{12}r_{23}\overline{r_{13}})
 \geq0,
 \qquad |r_{ij}|\leq1.
 \quad}                                                   \tag{27}
\]
The three separate bounds \(|r_{ij}|\leq1\) do not imply (27).
The remaining information must therefore use the common origin of
all three \(X_i=D_{\widehat i}V\).

## 5. Consequence for the proof search

Independent two-component estimates are now complete and sharp.  A
counterexample, if one exists, must have all three pair components
nonzero and must violate precisely the cyclic phase/magnitude
condition (25).  A positive proof needs a compatible three-way Gram
completion of the residual norms \(d_i\), or an equivalent bound on
the cycle trace
\[
 \operatorname{Re}
 (c_{12}c_{23}\overline{c_{13}}).
 \tag{28}
\]
No further one-edge Cauchy--Schwarz estimate can close the frontier:
all such information is already exhausted by the \(2\times2\)
principal minors (20).
