# Exact obstruction to a logical block-Gram certificate

## Status

This note exactly disproves a tempting strengthening of the residual
three-component pair-sector inequality.  The strengthening would let the
three pair operators act on three independently chosen vectors in the
two-dimensional code.  It is already false for the computational code
\(\operatorname{span}\{|000\rangle,|111\rangle\}\).

The counterexample is **not** a counterexample to the scalar pair-sector
inequality.  In fact, its ordinary \(3\times3\) scalar deficit matrix is
strictly positive.  The example therefore isolates an essential constraint:
all three physical pair components must be compared on the same complete
code frame, or equivalently on the same logical vector when a columnwise
argument is used.

The dependency-free exact checker is
`verification/verify_n3_pair_sector_logical_block_gram_obstruction.py`.

## 1. The false strengthening

Let \(V:\mathbb C^2\to(\mathbb C^3)^{\otimes3}\) be an isometry.  For
doubly traceless two-site matrices \(B_{\widehat i}\), insert the spectator
identity to obtain \(D_{\widehat i}\).  Put
\[
 b_i=\|B_{\widehat i}\|_2^2,\qquad X_i=D_{\widehat i}V.
\]
The proven scalar target is
\[
 \left\|\sum_i\lambda_iX_i\right\|_2^2
 \leq 2\sum_i|\lambda_i|^2b_i.                         \tag{1}
\]
One might try to prove the stronger block-matrix assertion
\[
 \mathbb M=
 \bigl[\delta_{ij}b_iI_2-X_i^\dagger X_j\bigr]_{i,j=1}^3
 \succeq0.                                               \tag{2}
\]
Taking the trace over the logical qubit in (2) gives exactly the scalar
deficit matrix from (1).  Equivalently, (2) asserts
\[
 \left\|\sum_iD_{\widehat i}Vq_i\right\|^2
 \leq\sum_i b_i\|q_i\|^2
 \quad\text{for all }q_1,q_2,q_3\in\mathbb C^2.          \tag{3}
\]
The trace implication is valid, but (2)--(3) are false.

## 2. Exact counterexample

Let
\[
 V|0\rangle=|000\rangle,\qquad V|1\rangle=|111\rangle.
                                                               \tag{4}
\]
Define
\[
 E=|0\rangle\langle1|,\qquad
 F=|1\rangle\langle0|,\qquad
 Z=\operatorname{diag}(1,-\tfrac12,-\tfrac12).           \tag{5}
\]
All three matrices are traceless.  Take
\[
 \begin{aligned}
 D_{\widehat1}&=I\otimes E\otimes E,
 &B_{\widehat1}&=E\otimes E,\\
 D_{\widehat2}&=\tfrac23F\otimes I\otimes Z,
 &B_{\widehat2}&=\tfrac23F\otimes Z,\\
 D_{\widehat3}&=\tfrac23F\otimes Z\otimes I,
 &B_{\widehat3}&=\tfrac23F\otimes Z.
 \end{aligned}                                           \tag{6}
\]
Every \(B_{\widehat i}\) is doubly traceless, and
\[
 (b_1,b_2,b_3)=(1,\tfrac23,\tfrac23).                    \tag{7}
\]

Now choose three different logical vectors,
\[
 q_1=|1\rangle,\qquad q_2=q_3=|0\rangle.                 \tag{8}
\]
Then all three outputs align:
\[
 D_{\widehat1}Vq_1=|100\rangle,\qquad
 D_{\widehat2}Vq_2=D_{\widehat3}Vq_3=\tfrac23|100\rangle.
                                                               \tag{9}
\]
Consequently
\[
 \left\|\sum_iD_{\widehat i}Vq_i\right\|^2
 =\left(\frac73\right)^2=\frac{49}{9},                  \tag{10}
\]
whereas
\[
 \sum_i b_i\|q_i\|^2=\frac73.                            \tag{11}
\]
Thus the Rayleigh quotient in (3) is exactly \(7/3\), and the quadratic
form of \(\mathbb M\) is
\[
 \frac73-\frac{49}{9}=-\frac{28}{9}<0.                  \tag{12}
\]

## 3. Why the scalar problem survives

On the full logical frame,
\[
 \begin{array}{c|cc}
  &V|0\rangle&V|1\rangle\\ \hline
 X_1&0&|100\rangle\\
 X_2&\tfrac23|100\rangle&0\\
 X_3&\tfrac23|100\rangle&0 .
 \end{array}                                             \tag{13}
\]
Hence
\[
 [\langle X_i,X_j\rangle]_{ij}
 =
 \begin{pmatrix}
 1&0&0\\
 0&4/9&4/9\\
 0&4/9&4/9
 \end{pmatrix}.                                         \tag{14}
\]
The genuine scalar deficit matrix is
\[
 M=
 \begin{pmatrix}
 1&0&0\\
 0&8/9&-4/9\\
 0&-4/9&8/9
 \end{pmatrix},                                         \tag{15}
\]
whose eigenvalues are \(1,4/9,4/3\).  Thus it is positive definite.

The block failure comes from selecting the second logical column for the
first component and the first logical column for the other two.  The scalar
problem never permits this independent logical selection: its Frobenius
inner products sum coherently over the same two code columns.  Therefore a
successful completion of the scalar determinant must retain this common
logical-frame coupling rather than dominate it by a \(6\times6\) block
Gram matrix.
