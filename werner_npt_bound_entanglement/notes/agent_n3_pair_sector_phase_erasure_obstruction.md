# Exact obstruction to erasing the three-cycle phase

## Status

This note gives an exact physical code plane and exact doubly
traceless pair coefficients for which the phase-forgotten deficit
matrix
\[
 M^{\rm abs}_{ii}=d_i,\qquad
 M^{\rm abs}_{ij}=-|c_{ij}|\quad(i\ne j)                 \tag{1}
\]
is not positive semidefinite.

This does **not** disprove the pair-sector theorem.  For the same
code and coefficients, the genuine physical quadratic deficit is
strictly positive.  The result proves that replacing the gauge-
invariant cycle phase by its worst possible value is too strong.
Consequently an eventual determinant proof must retain the exact
phase of
\[
 c_{12}c_{23}\overline{c_{13}}.                          \tag{2}
\]

The dependency-free exact checker is
`verification/verify_n3_pair_sector_phase_erasure_obstruction.py`.

## 1. Exact code

Let
\[
\begin{aligned}
u={}&\frac1{\sqrt5}\left(
 (1+i)|000\rangle+i|110\rangle+(1-i)|011\rangle
 \right),\\
v={}&\frac1{\sqrt5}\left(
 (1+i)|111\rangle+i|001\rangle+(1-i)|100\rangle
 \right).
\end{aligned}                                            \tag{3}
\]
Their supports are disjoint and each unnormalized numerator has
squared norm \(2+1+2=5\).  Hence \(V=(u,v)\) is an isometry.

## 2. Exact pair coefficients

Index each two-qutrit matrix by
\[
 00,01,02,10,11,12,20,21,22.                            \tag{4}
\]
The following three matrices are specified by their diagonal vectors
and their only off-diagonal entries:
\[
\begin{aligned}
B_{\widehat1}:&\quad
 (57,-60,3,-60,57,3,3,3,-6),\\
&\quad (B_{\widehat1})_{0,4}
 =(B_{\widehat1})_{4,0}=360;\\[1mm]
B_{\widehat2}:&\quad
 (-183i,-9+186i,9-3i,-9+186i,-183i,\\
&\hspace{27mm}9-3i,9-3i,9-3i,-18+6i),\\
&\quad (B_{\widehat2})_{1,3}
 =(B_{\widehat2})_{3,1}=117-225i;\\[1mm]
B_{\widehat3}:&\quad
 (-135-125i,126+127i,9-2i,126+127i,\\
&\hspace{27mm}-135-125i,9-2i,9-2i,9-2i,-18+4i),\\
&\quad (B_{\widehat3})_{0,4}
 =(B_{\widehat3})_{4,0}=-243-81i.
\end{aligned}                                            \tag{5}
\]
Every omitted entry is zero.

Each diagonal array in (5), reshaped as a \(3\times3\) array, has all
row and column sums zero.  Every off-diagonal entry changes both local
indices.  Therefore both partial traces of every \(B_{\widehat i}\)
vanish exactly.

Embed them as
\[
 D_{\widehat1}=I_1\otimes B_{\widehat1},\qquad
 D_{\widehat2}=I_2\otimes B_{\widehat2},\qquad
 D_{\widehat3}=I_3\otimes B_{\widehat3}.                 \tag{6}
\]
The second expression uses the natural site order \(1,3\) inside
\(B_{\widehat2}\).

Their squared norms are
\[
 \|B_{\widehat1}\|_2^2=272970,\qquad
 \|B_{\widehat2}\|_2^2=265680,\qquad
 \|B_{\widehat3}\|_2^2=263610.                           \tag{7}
\]

## 3. The exact component Gram

Put \(X_i=D_{\widehat i}V\) and
\[
 H_{ij}=\langle X_i,X_j\rangle.                          \tag{8}
\]
Direct exact contraction gives
\[
H=
\begin{pmatrix}
1069992/5&
165996-60408i/5&
126144-106680i\\
165996+60408i/5&
1071126/5&
758094/5-71262i/5\\
126144+106680i&
758094/5+71262i/5&
213644
\end{pmatrix}.                                           \tag{9}
\]
The physical denominator is
\[
 2\sum_i\|B_{\widehat i}\|_2^2=1604520.                 \tag{10}
\]

Now twist only the \(13\) edge by
\[
 \zeta=e^{i\pi/4}=\frac{1+i}{\sqrt2}.                   \tag{11}
\]
The resulting artificial quadratic numerator is
\[
 N_\zeta
 =
 \operatorname{Tr}H+
 2\operatorname{Re}
 \left(H_{12}+H_{23}+\zeta H_{13}\right).               \tag{12}
\]
Equations (9)--(12) give
\[
\boxed{\quad
 N_\zeta-1604520
 =
 -\frac{1637114}{5}+232824\sqrt2>0.
\quad}                                                   \tag{13}
\]
The sign is exact: multiplying by \(5\), both sides to be compared
are positive, and
\[
 2(1164120)^2-(1637114)^2
 =30208499804>0.                                        \tag{14}
\]

For any three complex numbers,
\[
 \operatorname{Re}(c_{12}+c_{23}+\zeta c_{13})
 \leq |c_{12}|+|c_{23}|+|c_{13}|.                       \tag{15}
\]
Thus (13) implies
\[
 \operatorname{Tr}H+2\sum_{i<j}|H_{ij}|
 >
 2\sum_i\|B_{\widehat i}\|_2^2.                         \tag{16}
\]
Equivalently,
\[
 (1,1,1)M^{\rm abs}(1,1,1)^T<0.                        \tag{17}
\]
This proves the claimed exact failure of phase erasure.

## 4. The physical cycle remains positive

Without the artificial twist, the genuine deficit at the same
coefficient vector is
\[
\begin{aligned}
&2\sum_i\|B_{\widehat i}\|_2^2
 -\left[
 \operatorname{Tr}H+
 2\operatorname{Re}(H_{12}+H_{23}+H_{13})
 \right]\\
&\hspace{35mm}=\frac{375674}{5}>0.                       \tag{18}
\end{aligned}
\]
Hence (5) is not a pair-sector counterexample.  The positive gap is
large; what fails is specifically the inconsistent choice of three
edge phases.

The component-index phase gauge can make two edges real and negative
in the deficit matrix, but the phase of their product around the
triangle is invariant.  Formula (13) shows quantitatively that this
one invariant cannot be discarded even when all local coefficients
and the code are exact algebraic data.

## 5. Consequence

The earlier two-component theorem controls the magnitude of every
individual \(c_{ij}\).  This example proves that the three magnitudes
together still overestimate the dangerous direction.  Therefore a
valid Gram completion must be phase-coherent around the whole cycle,
or equivalently must control the signed term
\[
 -2\operatorname{Re}
 (c_{12}c_{23}\overline{c_{13}})
 \tag{19}
\]
in the determinant itself.  An absolute-value \(M\)-matrix argument,
even with optimally sharp edge contractions, cannot settle the
frontier.
