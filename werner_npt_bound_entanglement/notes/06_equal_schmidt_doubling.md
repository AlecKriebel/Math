# Equal Schmidt coefficients are sufficient for the all-copy question

Let \(\mathcal B_n\) denote the Hermitian sesquilinear form whose quadratic
form is \(Q_{d,n}\).  It tensor-factorizes:
\[
\mathcal B_{n+m}(A\otimes B,C\otimes D)
=\mathcal B_n(A,C)\mathcal B_m(B,D).
\tag{1}
\]
This follows either from the tensor definition of \(X^{\otimes(n+m)}\) or
directly from the subset-contraction formula.

## 1. Fixed-span determinant criterion

Let \(C_1,C_2\) be linearly independent rank-one matrices and define
\[
H_{rs}=\mathcal B_n(C_r,C_s),\qquad r,s\in\{1,2\}.
\tag{2}
\]
Then
\[
Q_{d,n}(z_1C_1+z_2C_2)=z^\dagger H z.
\tag{3}
\]
Each diagonal entry is strictly positive when \(C_r\ne0\), by the rank-one
bound.  Hence this two-term span contains a negative vector if and only if
\[
\det H<0.
\tag{4}
\]
This also gives an exact witness without diagonalizing \(H\).  Writing
\[
H=\begin{pmatrix}a&b\\\overline b&d\end{pmatrix},
\]
take
\[
C=dC_1-\overline b\,C_2.
\tag{5}
\]
Then
\[
Q_{d,n}(C)=d\det H<0.
\tag{6}
\]

## 2. Copy-doubling theorem

**Theorem.** If there is a negative Schmidt-rank-at-most-two vector at
some copy number \(n\), then there is a negative Schmidt-rank-two vector
with equal nonzero Schmidt coefficients at copy number \(2n\).

**Proof.** Take a singular-value decomposition of the negative coefficient
matrix and absorb its two positive singular values into the coefficients:
\[
C=z_1C_1+z_2C_2,\qquad
C_r=|u_r\rangle\langle v_r|,
\tag{7}
\]
where \(u_1,u_2\) are orthonormal and \(v_1,v_2\) are orthonormal.  The
matrix \(H\) from (2) is not positive semidefinite because
\(z^\dagger H z<0\).  Its diagonal entries are positive, so
\(\det H<0\).

On \(2n\) copies define
\[
D=C_1\otimes C_2-C_2\otimes C_1.
\tag{8}
\]
Its two left vectors
\[
u_1\otimes u_2,\qquad u_2\otimes u_1
\]
are orthonormal, as are its two right vectors
\[
v_1\otimes v_2,\qquad v_2\otimes v_1.
\]
Thus (8) is already a singular-value decomposition, up to the sign of the
second right vector, and both nonzero singular values of \(D\) equal one.

Using (1),
\[
\begin{aligned}
Q_{d,2n}(D)
&=H_{11}H_{22}+H_{22}H_{11}
  -H_{12}H_{21}-H_{21}H_{12}\\
&=2\left(H_{11}H_{22}-|H_{12}|^2\right)
=2\det H<0.
\end{aligned}
\tag{9}
\]
This proves the claim. \(\square\)

## 3. Consequence

The endpoint is two-block-positive at every copy number if and only if it
is nonnegative, at every copy number, on coefficient matrices whose two
nonzero singular values are equal.  Equivalently, after scaling, it is
enough to test rank-two partial isometries
\[
C=|u_1\rangle\langle v_1|+|u_2\rangle\langle v_2|
\tag{10}
\]
with both displayed pairs orthonormal.

This is a reduction of the all-copy existence question, not a proof of
positivity: the left and right two-planes in (10) may still be arbitrary,
fully supported, and entangled across copies.
