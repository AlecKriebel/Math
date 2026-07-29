# The full three-copy problem as one reversed-Schur orientation inequality

## Status

This note gives an exact same-copy reduction of the **full**
unrestricted three-copy endpoint.  It does not prove the remaining
inequality.

For two left and two right singular vectors, compress the positive
replica filter
\[
 Y=\bigotimes_{i=1}^3\left(I-\frac12F_i\right)
\]
to the resulting logical two-qubit space.  Write the strictly positive
compression in \(2\times2\) logical blocks as
\[
 K=\begin{pmatrix}A&B\\ B^\dagger&D\end{pmatrix}\succ0.
\]
The endpoint theorem is equivalent to positivity of a logical partial
transpose of \(K\).  The new observation is that its determinant has
the exact form
\[
 \boxed{\quad
 \frac{\det K^\Gamma}{\det A\det D}
 =
 \det(I-X^\dagger X)
 +\|X\|_2^2-\|Z\|_2^2,
 \quad}
\]
where
\[
 X=A^{-1/2}BD^{-1/2},\qquad
 Z=A^{-1/2}B^\dagger D^{-1/2}.
\]
Since \(K\succ0\), \(X\) is a strict contraction.  Consequently the
whole unrestricted three-copy problem is precisely
\[
 \boxed{\qquad
 \|Z\|_2^2-\|X\|_2^2
 \leq
 (1-s_1(X)^2)(1-s_2(X)^2).
 \qquad}
\]
The right side is the ordinary positive Gram slack.  The left side is
the sole reversal/orientation defect.

This reduction includes the scalar, one-body, and pair components
together; it is not a pair-sector relaxation.  It also identifies
several automatic positive charts and gives an exact abstract
counterexample showing that positivity and the spectral interval of
the physical replica filter do not, by themselves, control the
orientation defect.  A proof must still use the common tensor origin
of \(A,B,D\).

The dependency-free exact checker is
`verification/verify_n3_full_reversed_schur_orientation.py`.

## 1. Logical compression and block convention

Let
\[
 U,V:\mathbb C^2\longrightarrow
 (\mathbb C^3)^{\otimes3}
\]
be isometries, and define
\[
 K(U,V)
 =(U^\dagger\otimes V^\dagger)
 Y(U\otimes V).
\tag{1}
\]
Every local factor in \(Y\) has eigenvalues \(1/2\) and \(3/2\), so
\[
 Y\succeq\frac18I,\qquad K(U,V)\succeq\frac18I_4.
\tag{2}
\]
In particular \(K\) and both diagonal logical blocks below are
invertible.

Order the logical basis by the first qubit and write
\[
 K=\begin{pmatrix}A&B\\B^\dagger&D\end{pmatrix},
\qquad A,D\in M_2,\quad A,D\succ0.
\tag{3}
\]
Partial transpose on the first logical qubit gives
\[
 K^{\Gamma_1}
 =\begin{pmatrix}A&B^\dagger\\B&D\end{pmatrix}.
\tag{4}
\]
Partial transpose on the second qubit is the full transpose of (4).
Thus the two partial transposes have the same determinant and are
positive simultaneously.

The established two-plane reduction says
\[
 Q_3(C)\geq0\quad(\operatorname{rank}C\leq2)
\quad\Longleftrightarrow\quad
 K(U,V)^\Gamma\succeq0\quad\hbox{for every }U,V.
\tag{5}
\]
Because a partial transpose of a strictly positive two-qubit operator
is strictly block-positive, it has at most one negative eigenvalue and
cannot have a negative and a zero eigenvalue simultaneously.
Consequently
\[
 K^\Gamma\succeq0
\quad\Longleftrightarrow\quad
 \det K^\Gamma\geq0.
\tag{6}
\]

## 2. Exact reversed-Schur determinant identity

### Lemma 2.1

Let (3) be any strictly positive \(4\times4\) Hermitian block matrix
with \(2\times2\) blocks.  Put
\[
 X=A^{-1/2}BD^{-1/2},\qquad
 Z=A^{-1/2}B^\dagger D^{-1/2}.
\tag{7}
\]
Then
\[
\boxed{
\begin{aligned}
\frac{\det K}{\det A\det D}
 &=
 1-\|X\|_2^2+|\det X|^2
 =\det(I-X^\dagger X),\\
\frac{\det K^\Gamma}{\det A\det D}
 &=
 1-\|Z\|_2^2+|\det Z|^2,\\
\det K^\Gamma
 &=
 \det K+\det A\det D
 \bigl(\|X\|_2^2-\|Z\|_2^2\bigr).
\end{aligned}}
\tag{8}
\]
Moreover,
\[
 |\det X|=|\det Z|.
\tag{9}
\]

### Proof

The ordinary Schur complement gives
\[
\begin{aligned}
\det K
 &=\det A\det(D-B^\dagger A^{-1}B)\\
 &=\det A\det D\,
 \det\!\left(
 I-D^{-1/2}B^\dagger A^{-1}BD^{-1/2}
 \right)\\
 &=\det A\det D\,\det(I-X^\dagger X).
\end{aligned}
\tag{10}
\]
For a \(2\times2\) matrix \(T\),
\[
 \det(I-T^\dagger T)
 =1-\operatorname{Tr}(T^\dagger T)+|\det T|^2.
\tag{11}
\]
This proves the first line of (8).

Apply the same calculation to (4):
\[
\begin{aligned}
\det K^\Gamma
 &=\det A\det(D-BA^{-1}B^\dagger)\\
 &=\det A\det D\,
 \det(I-Z^\dagger Z),
\end{aligned}
\tag{12}
\]
which proves the second line.  Finally,
\[
 |\det X|
 =
 \frac{|\det B|}{\sqrt{\det A\det D}}
 =
 \frac{|\det B^\dagger|}{\sqrt{\det A\det D}}
 =|\det Z|.
\tag{13}
\]
Subtracting the first two formulas proves the last line of (8).
\(\square\)

There is a version avoiding matrix square roots:
\[
\boxed{
\begin{aligned}
\det K^\Gamma-\det K
=\det A\det D\bigl[
 &\operatorname{Tr}(D^{-1}B^\dagger A^{-1}B)\\
 &-\operatorname{Tr}(D^{-1}BA^{-1}B^\dagger)
\bigr].
\end{aligned}}
\tag{14}
\]
This is often the most convenient exact-algebra form.

## 3. Exact equivalence for the unrestricted endpoint

Positivity of \(K\) and (10) imply
\[
 I-X^\dagger X\succ0.
\tag{15}
\]
Thus \(s_1(X)<1\), and
\[
 \det(I-X^\dagger X)
 =(1-s_1(X)^2)(1-s_2(X)^2)>0.
\tag{16}
\]
Combining (5)--(8) gives the promised lossless statement.

### Theorem 3.1

Unrestricted qutrit three-copy endpoint positivity is equivalent to
\[
\boxed{
\|A^{-1/2}B^\dagger D^{-1/2}\|_2^2
-
\|A^{-1/2}BD^{-1/2}\|_2^2
\leq
\det\!\left(
 I-D^{-1/2}B^\dagger A^{-1}BD^{-1/2}
\right)}
\tag{17}
\]
for every physical compression (1).

Equivalently, with \(X,Z\) from (7),
\[
 \boxed{\qquad
 \|Z\|_2^2-\|X\|_2^2
 \leq(1-s_1(X)^2)(1-s_2(X)^2).
 \qquad}
\tag{18}
\]

The right side in (18) is exactly
\[
 \frac{\det K}{\det A\det D};
\tag{19}
\]
it measures the distance from singularity of the ordinary positive
Gram matrix.  No matrix-valued Schur inequality remains.  A violation
of (18) is exactly a negative three-copy Werner witness after taking
the negative eigenvector of \(K^\Gamma\).

## 4. Automatic charts

Equation (18) holds immediately whenever
\[
 \|Z\|_2\leq\|X\|_2.
\tag{20}
\]
In particular the orientation defect vanishes in each of the
following cases:

1. \(A=D\), because then \(Z=X^\dagger\);
2. more generally \(D=tA\) for a positive scalar \(t\);
3. \(B=B^\dagger\);
4. \(B=-B^\dagger\);
5. \(B=e^{i\theta}H\) for a Hermitian \(H\).

These are statements about the logical Gram blocks, not assumptions
on the original coefficient matrix.  They expose the remaining locus
as genuinely reversed and nonnormal: its reversed normalized
coherence must have strictly larger Hilbert--Schmidt norm than the
ordinary normalized coherence.

## 5. Exact abstract obstruction

The common physical origin of the three blocks is indispensable.
Positivity of \(K\), even together with the exact spectral interval
of the physical filter, does not imply (18).

Take
\[
 m=\frac12,\qquad
 |\Phi_2\rangle=|00\rangle+|11\rangle,\qquad
 K_*=mI_4+|\Phi_2\rangle\langle\Phi_2|.
\tag{21}
\]
Then
\[
 \operatorname{spec}K_*=
 \left(\frac52,\frac12,\frac12,\frac12\right),
\tag{22}
\]
which lies inside the physical filter interval
\([1/8,27/8]\).  In the block convention (3),
\[
 A=\begin{pmatrix}3/2&0\\0&1/2\end{pmatrix},\quad
 D=\begin{pmatrix}1/2&0\\0&3/2\end{pmatrix},\quad
 B=\begin{pmatrix}0&1\\0&0\end{pmatrix}.
\tag{23}
\]
Partial transpose gives
\[
 \operatorname{spec}K_*^\Gamma
 =\left(\frac32,\frac32,\frac32,-\frac12\right),
\tag{24}
\]
so
\[
 \det K_*=\frac5{16},\qquad
 \det K_*^\Gamma=-\frac{27}{16}.
\tag{25}
\]
Here
\[
 \det A\det D=\frac9{16},\qquad
 \det(I-X^\dagger X)=\frac59,\qquad
 \|Z\|_2^2-\|X\|_2^2=\frac{32}{9}.
\tag{26}
\]
Thus the ordinary Schur slack is positive, but the orientation defect
overwhelms it exactly.

The example is not asserted to be a compression (1).  It proves that
a successful argument cannot use only:

* positivity of the logical Gram;
* its universal lower and upper spectral bounds; or
* the ordinary Schur contraction.

The remaining physical lemma is precisely to control the orientation
defect in (18) using the shared three-fold tensor compression.

## Research log

- **2026-07-29 15:20 PDT.** Reduced the full two-plane
  partial-transpose determinant to the ordinary positive Gram
  determinant minus one scalar reversed-coherence orientation defect.
  Isolated the exact inequality (18), its automatic charts, and the
  abstract spectral-interval obstruction (21)--(26).
