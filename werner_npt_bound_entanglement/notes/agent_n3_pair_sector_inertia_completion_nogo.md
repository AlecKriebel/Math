# Residual inertia cannot certify the scalar three-cycle determinant

## Status

This note gives an exact obstruction to an inertia-only completion of
the remaining three-component pair-sector argument.

For a \(3\times3\) array of logical \(2\times2\) blocks, let
\[
 {\mathfrak s}(A)=(\operatorname{Tr}A)I_2-A
\]
be the logical spin flip, applied blockwise.  The physical residual
has the identity
\[
 {\mathbb N}+{\mathfrak s}_K({\mathbb N})=M\otimes I_2.
 \tag{1}
\]
It was natural to ask whether a bound
\(\operatorname{ind}_-{\mathbb N}\leq2\), together with the already
proved nonnegative principal minors of \(M\) of orders one and two,
forces \(\det M\geq0\).

The answer is **no**, even under substantially stronger formal
assumptions.  The example below has

* \(\operatorname{ind}_-{\mathbb N}=1\);
* every two-component \(4\times4\) principal block of
  \({\mathbb N}\) positive semidefinite;
* a common positive Gram representation
  \({\mathbb N}=\operatorname{diag}(b_iI_2)-X^\dagger X\);
* the exact spin-flip completion (1);
* all scalar principal minors of \(M\) of orders one and two strictly
  positive;

but
\[
 \boxed{\det M=-\frac{49}{32}<0.}
 \tag{2}
\]

This is not a physical Werner counterexample: the common Gram vectors
are not asserted to arise as \(X_i=D_{\widehat i}V\) from
doubly-traceless qutrit pair coefficients.  Its point is sharper and
purely logical.  Even a proof of the conjectural physical ceiling
\(\operatorname{ind}_-{\mathbb N}\leq2\) cannot, by itself, finish
the scalar determinant.  A successful argument must use additional
physical common-code geometry.

The dependency-free checker is
`verification/verify_n3_pair_sector_inertia_completion_nogo.py`.

## 1. A general logical embedding

Let \(H\in M_m(\mathbb C)\) be Hermitian and put
\[
 P_0=|0\rangle\langle0|,\qquad P_1=|1\rangle\langle1|,
 \qquad {\mathbb N}=H\otimes P_0.
 \tag{3}
\]
Since
\[
 {\mathfrak s}(P_0)=P_1,
 \]
blockwise spin flip gives
\[
 {\mathfrak s}_K({\mathbb N})=H\otimes P_1,
 \qquad
 {\mathbb N}+{\mathfrak s}_K({\mathbb N})=H\otimes I_2.
 \tag{4}
\]
Moreover,
\[
 \operatorname{ind}_-({\mathbb N})
 =\operatorname{ind}_-(H),
 \tag{5}
\]
because the second logical sector is a zero block.

Thus the spin-flip identity transfers no sign information from
\({\mathbb N}\) to \(H\) beyond the inertia already present in
\(H\).  In particular, any one-negative scalar matrix becomes a
one-negative logical residual.

## 2. Exact \(3\times3\) obstruction

Take
\[
 M=
 \begin{pmatrix}
 1&-\frac34&-\frac34\\
 -\frac34&1&-\frac34\\
 -\frac34&-\frac34&1
 \end{pmatrix}.
 \tag{6}
\]
Its one-by-one principal minors equal \(1\), and every two-by-two
principal minor equals
\[
 1-\left(\frac34\right)^2=\frac7{16}>0.
 \tag{7}
\]
On the vector \({\bf 1}=(1,1,1)^{\mathsf T}\), \(M\) has eigenvalue
\(-1/2\).  On \({\bf 1}^{\perp}\), it has eigenvalue \(7/4\).
Consequently
\[
 \operatorname{inertia}(M)=(2,1,0),\qquad
 \det M=-\frac12\left(\frac74\right)^2=-\frac{49}{32}.
 \tag{8}
\]

Set
\[
 {\mathbb N}=M\otimes P_0.
 \tag{9}
\]
Equations (5) and (8) give
\[
 \operatorname{inertia}({\mathbb N})=(2,1,3).
 \tag{10}
\]
For every pair of component indices, the corresponding principal
block of \({\mathbb N}\) is
\[
 \begin{pmatrix}1&-\frac34\\-\frac34&1\end{pmatrix}
 \otimes P_0\succeq0.
 \tag{11}
\]
So even positivity of all two-component *logical* residuals, which
is stronger than positivity of their scalar traces, does not repair
the implication.

## 3. A common Gram residual

The example can also be put in the exact formal shape of the physical
residual.  Choose
\[
 b_1=b_2=b_3=2,\qquad
 G=2I_6-{\mathbb N}.
 \tag{12}
\]
On the \(P_0\) logical sector, \(G\) is \(2I_3-M\), with eigenvalues
\[
 \frac52,\quad\frac14,\quad\frac14.
 \]
On the \(P_1\) sector it is \(2I_3\).  Hence \(G\succeq0\).  There
therefore exist common vectors \(X_1,X_2,X_3\), each with two logical
columns, whose block Gram matrix is
\[
 [X_i^\dagger X_j]_{i,j}=G.
 \tag{13}
\]
With these vectors,
\[
 {\mathbb N}_{ij}
 =\delta_{ij}b_iI_2-X_i^\dagger X_j.
 \tag{14}
\]
The diagonal Gram blocks are
\[
 X_i^\dagger X_i=2I_2-P_0
 =\operatorname{diag}(1,2)\preceq2I_2,
 \tag{15}
\]
so the usual individual contraction constraint is also satisfied.

Equations (4), (7), (10), (11), and (14) show that none of the
following data can prove the missing scalar determinant:

1. a negative-index bound as strong as one;
2. the blockwise spin-flip identity;
3. all one- and two-component scalar inequalities;
4. positivity of every two-component logical residual;
5. existence of one common positive Gram matrix and the individual
   budget bounds.

What remains available is precisely the nonlinear physical
realizability condition
\[
 X_i=(I_i\otimes B_{\widehat i})V
 \]
with one common qutrit code isometry \(V\) and three doubly-traceless
pair coefficients.  Any useful inertia theorem must retain that
factorization quantitatively rather than discard it after forming
the Gram matrix.
