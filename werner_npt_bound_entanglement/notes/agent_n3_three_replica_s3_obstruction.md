# Exact qutrit obstruction to the naive three-replica \(S_3\) certificate

## Status

This note does **not** disprove unrestricted three-copy positivity.  It
disproves a natural proof mechanism suggested by
\(\bigwedge^3\mathbb C^2=0\): multiply the unshifted quartic by
\(\|{\cal A}\|^2\), represent it on three replicas
\({\cal A}\otimes{\cal B}\otimes{\cal A}\), and seek a positive
three-replica permutation-algebra Gram operator.

The obstruction is exact.  On one \(S_3\)-isotypic block the required
Gram operator has eigenvalues
\[
 9,\qquad -\frac{27}{2}.                                  \tag{1}
\]
The block requires alternating three-tensors at two physical sites, so
it first exists in local dimension three.  It is absent when every
physical site is a qubit.  Thus it pinpoints a genuinely qutrit
obstruction rather than contradicting the established qubit theorem.

The independent checker is
`verification/verify_n3_three_replica_s3_obstruction.py`.

## 1. The three-replica lift

On two replicas put
\[
 G_{12}=F_K^{12}\prod_{i=1}^3(2I-F_i^{12}).               \tag{2}
\]
For vectors \({\cal A},{\cal B}\in K\otimes H_1\otimes H_2\otimes
H_3\), the unshifted target is
\[
 \langle{\cal A}\otimes{\cal B},
 G_{12}({\cal A}\otimes{\cal B})\rangle\geq0.             \tag{3}
\]
After multiplying by \(\|{\cal A}\|^2\), introduce
\[
 Z={\cal A}_1\otimes{\cal B}_2\otimes{\cal A}_3.          \tag{4}
\]
Let
\[
 {\mathbb F}_{13}
 =F_K^{13}F_1^{13}F_2^{13}F_3^{13},\qquad
 {\mathbb P}_+=\frac{I+{\mathbb F}_{13}}2.                \tag{5}
\]
Because replicas 1 and 3 both carry \({\cal A}\),
\({\mathbb P}_+Z=Z\), and hence
\[
 \|{\cal A}\|^2
 \langle{\cal A}\otimes{\cal B},
 G_{12}({\cal A}\otimes{\cal B})\rangle
 =
 \langle Z,{\mathbb P}_+G_{12}{\mathbb P}_+Z\rangle.
                                                               \tag{6}
\]

It is tempting to prove (6) by showing
\({\mathbb P}_+G_{12}{\mathbb P}_+\succeq0\), perhaps after adding
the vanishing three-fold antisymmetrizer on \(K\).  The next section
shows that this is impossible.

## 2. The exact bad \(S_3\) block

Use the three irreducible real representations of \(S_3\):
\[
 [3]\quad\hbox{(trivial)},\qquad
 [111]\quad\hbox{(sign)},\qquad
 [21]\quad\hbox{(standard)}.
                                                               \tag{7}
\]
On the standard representation choose reflection matrices for the
transpositions \((12)\) and \((13)\):
\[
 a=
 \begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad
 b=
 \begin{pmatrix}
 -\frac12&\frac{\sqrt3}{2}\\
 \frac{\sqrt3}{2}&\frac12
 \end{pmatrix}.                                           \tag{8}
\]
On the sign representation both transpositions act as \(-1\).

Consider the isotypic block
\[
 [21]_K\otimes[111]_{H_1}\otimes[111]_{H_2}
 \otimes[21]_{H_3}.                                      \tag{9}
\]
It exists when \(\dim K\geq2\), \(\dim H_1,\dim H_2\geq3\),
and \(\dim H_3\geq2\).  The sign representation is absent from
\((\mathbb C^2)^{\otimes3}\), because it is
\(\bigwedge^3\mathbb C^2=0\).

The two sign factors in (9) contribute
\[
 (2-(-1))(2-(-1))=9
                                                               \tag{10}
\]
to (2).  Therefore on the remaining
\([21]_K\otimes[21]_{H_3}\) factor,
\[
 G_{12}=9\,a\otimes(2I-a),\qquad
 {\mathbb P}_+=\frac{I+b\otimes b}{2}.                    \tag{11}
\]

Rotate both standard factors so that \(b\) is diagonal.  In that basis
\[
 b=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad
 a=
 \begin{pmatrix}
 -\frac12&\frac{\sqrt3}{2}\\
 \frac{\sqrt3}{2}&\frac12
 \end{pmatrix}.                                           \tag{12}
\]
The \(+1\) eigenspace of \(b\otimes b\) is spanned by
\(|00\rangle,|11\rangle\).  Compressing (11) to this
two-dimensional range gives
\[
 \left.{\mathbb P}_+G_{12}{\mathbb P}_+\right|_{\rm ran
 {\mathbb P}_+}
 =
 \frac94
 \begin{pmatrix}
 -5&-3\\
 -3&3
 \end{pmatrix}.                                           \tag{13}
\]
The inner matrix has trace \(-2\) and determinant \(-24\), hence
eigenvalues \(4,-6\).  Its negative and positive eigenvectors may be
chosen as
\[
 3|00\rangle+|11\rangle,\qquad |00\rangle-3|11\rangle,
                                                               \tag{13a}
\]
respectively.  This proves (1) and identifies the precise Young
covariant which a nonlinear realizability inequality must control.

The three-fold antisymmetrizer on \(K\) vanishes identically and
therefore has no effect on this standard \(K\)-block.  Terms containing
\(I-{\mathbb F}_{13}\) also vanish after the compression in (13).
Thus neither of the two immediate three-replica relations repairs the
negative eigenvalue.

## 3. Consequence for cubic Hermitian sums of squares

The holomorphic degree-three monomial vector for a putative certificate
is
\[
 {\cal A}\otimes{\cal A}\otimes{\cal B}
 \in\operatorname{Sym}^2({\cal H})\otimes{\cal H}.        \tag{14}
\]
Its distinct symmetric coordinates are linearly independent
monomials.  Therefore a Hermitian sum of squares of holomorphic cubic
forms has a positive-semidefinite Gram matrix on
\(\operatorname{Sym}^2({\cal H})\otimes{\cal H}\).  Equality with the
lifted polynomial (6) fixes that Gram form by coefficient
polarization.  Its permutation-invariant compression contains (13),
which is indefinite.

Consequently:
\[
\boxed{\quad
\text{The lifted unshifted polynomial has no Hermitian SOS
certificate made only of holomorphic cubic forms.}
\quad}                                                     \tag{15}
\]
Equivalently, a successful three-replica proof cannot consist solely of
making the repeated-\({\cal A}\) Gram operator positive in the
\(S_3\) permutation algebra.  It must use a genuinely nonlinear
state-dependent incidence map, higher-degree multipliers, or a
different inequality.

This obstruction does not produce vectors \({\cal A},{\cal B}\) with
negative (3).  A negative direction in the linear span
\(\operatorname{Sym}^2({\cal H})\otimes{\cal H}\) need not be a
decomposable Veronese vector
\({\cal A}\otimes{\cal A}\otimes{\cal B}\).  The distinction is
exactly the remaining nonlinear realizability issue.

## Exact conclusion

What is proved:

1. the repeated-replica compression (6);
2. the exact qutrit isotypic block (9);
3. its rational compressed matrix (13) and negative eigenvalue
   \(-27/2\);
4. the impossibility of the naive cubic \(S_3\)-algebra Hermitian SOS;
5. the obstruction first requires two local sign representations and
   hence disappears on all-qubit physical support.

What is not proved:

1. no physical rank-two counterexample is obtained;
2. higher-degree or state-dependent Koszul certificates remain open;
3. unrestricted three-copy positivity remains unresolved.
