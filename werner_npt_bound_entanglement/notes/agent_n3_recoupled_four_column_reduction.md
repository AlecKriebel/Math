# Four-column reduction of the grouped rank-two recoupled problem

## Status

This note gives an exact \(4\times4\) Gram reduction of the recoupled
inequality when both grouped coefficient matrices have rank at most
two.  It also disproves the most natural Gram--Schur strengthening by
an exact rank-\((2,2)\) example.

The true reduced inequality remains open.  The reduction identifies
the term which cannot be discarded: the transpose-antisymmetric part
of one \(4\times4\) cross matrix.

The independent exact checker is
`verification/verify_n3_recoupled_four_column_nogo.py`.

## 1. Low-rank factorization

Let
\[
 {\cal K}=M_{27}(\mathbb C),\qquad
 Z=2I-3\Pi _2 ,
 \tag{1}
\]
where \(\Pi _2\) is the orthogonal projection onto the qutrit
three-copy sector with exactly two traceless factors.  In the
computational matrix-unit basis, \(Z\) is real symmetric.

Let \(A,B\in M_{27}\) have rank at most two and choose factorizations
\[
 A=XY^\dagger,\qquad B=UV^\dagger,
 \qquad X,Y,U,V:\mathbb C^2\longrightarrow\mathbb C^{27}.
 \tag{2}
\]
Zero columns cover the rank-one case.  Define four-column matrices
\[
\begin{aligned}
 E_{ij}&=\overline{x_i}\otimes u_j,\\
 F_{ij}&=\overline{y_i}\otimes v_j,
 \qquad i,j\in\{0,1\},
\end{aligned}
 \tag{3}
\]
with column order \(00,01,10,11\).  Thus
\[
 M:=\overline A\otimes B=EF^\dagger
 \tag{4}
\]
after regrouping its row indices and column indices.

Put
\[
 G_E=E^\dagger ZE,\qquad
 G_F=F^\dagger ZF,\qquad
 H=E^\dagger Z\overline F.
 \tag{5}
\]
All three matrices in (5) are only \(4\times4\).

## 2. Exact trace identity

The recoupled grouped-product expectation is
\[
 {\cal R}(A,B)
 =
 \frac12\operatorname{Tr}
 \left[
 (M-M^{\mathsf T})^\dagger
 Z(M-M^{\mathsf T})Z
 \right].
 \tag{6}
\]
Expanding (6), using (4), and cyclically moving the four-column
factors gives
\[
\begin{aligned}
 \operatorname{Tr}(M^\dagger ZMZ)
 &=\operatorname{Tr}(G_EG_F),\\
 \operatorname{Tr}(M^\dagger ZM^{\mathsf T}Z)
 &=\operatorname{Tr}(H\overline H).
\end{aligned}
 \tag{7}
\]
The other two terms are their conjugates.  Both quantities in (7)
are real, so
\[
 \boxed{\qquad
 {\cal R}(A,B)
 =
 \operatorname{Tr}(G_EG_F)
 -
 \operatorname{Tr}(H\overline H).
 \qquad}
 \tag{8}
\]

Write
\[
 H_{\rm s}=\frac{H+H^{\mathsf T}}2,\qquad
 H_{\rm a}=\frac{H-H^{\mathsf T}}2.
 \tag{9}
\]
The two parts are Frobenius-orthogonal, and direct entrywise
contraction gives
\[
 \operatorname{Tr}(H\overline H)
 =\|H_{\rm s}\|_2^2-\|H_{\rm a}\|_2^2.
 \tag{10}
\]
Consequently grouped rank-two recoupled positivity is exactly the
following \(4\times4\) tensor-grid inequality:
\[
 \boxed{\qquad
 \operatorname{Tr}(G_EG_F)+\|H_{\rm a}\|_2^2
 \ \geq\ \|H_{\rm s}\|_2^2.
 \qquad}
 \tag{11}
\]

Equivalently,
\[
 {\cal R}(A,B)
 =
 \left(\operatorname{Tr}(G_EG_F)-\|H\|_2^2\right)
 +\frac12\|H-H^{\mathsf T}\|_2^2.
 \tag{12}
\]
Formula (12) shows exactly what is lost by applying an ordinary
cross-Gram contraction.

If singular-value factorizations are used in (2), then the four
columns of \(E\) and \(F\) are separately orthogonal and have the
same squared norms \(s_it_j\).  Thus (11) has no hidden large
ambient matrix: its remaining data are two weighted tensor-grid
four-frames and their three \(4\times4\) \(Z\)-compressions.

## 3. Exact no-go to the stronger contraction

Let \(E_{ab}=|a\rangle\langle b|\), and set
\[
 D=\operatorname{diag}(-1,1,0),\qquad
 P=\operatorname{diag}(1,1,0).
 \tag{13}
\]
Take
\[
\boxed{
\begin{aligned}
 A&=E_{01}\otimes E_{00}\otimes D,\\
 B&=E_{01}\otimes E_{11}\otimes P.
\end{aligned}}
 \tag{14}
\]
Both matrices have rank exactly two and squared Frobenius norm two.

Choose the evident two-term factorizations of (14).  In the column
order \(00,01,10,11\), exact contraction with \(Z\) gives
\[
G_E=
\begin{pmatrix}
 2/3&0&0&1/3\\
 0&1&0&0\\
 0&0&1&0\\
 1/3&0&0&2/3
\end{pmatrix},
\qquad
G_F=
\begin{pmatrix}
 2/3&0&0&-1/3\\
 0&1&0&0\\
 0&0&1&0\\
 -1/3&0&0&2/3
\end{pmatrix},
 \tag{15}
\]
and
\[
H=
\begin{pmatrix}
 1/3&0&0&-2/3\\
 0&1&0&0\\
 0&0&-1&0\\
 2/3&0&0&-1/3
\end{pmatrix}.
 \tag{16}
\]
Therefore
\[
\begin{aligned}
 \operatorname{Tr}(G_EG_F)&=\frac83,\\
 \|H\|_2^2&=\frac{28}{9},\\
 \operatorname{Tr}(G_EG_F)-\|H\|_2^2&=-\frac49.
\end{aligned}
 \tag{17}
\]
This disproves the proposed stronger contraction
\[
 \|E^\dagger Z\overline F\|_2^2
 \leq\operatorname{Tr}
 \bigl((E^\dagger ZE)(F^\dagger ZF)\bigr)
 \tag{18}
\]
even when both grouped matrices have rank exactly two.

The discarded term is not a small correction:
\[
 \frac12\|H-H^{\mathsf T}\|_2^2=\frac{16}{9}.
 \tag{19}
\]
Equations (12), (17), and (19) give
\[
 \boxed{\qquad {\cal R}(A,B)=\frac43>0. \qquad}
 \tag{20}
\]
After normalizing both \(A\) and \(B\), the expectation is \(1/3\).
Thus (14) is an exact obstruction to a proof strategy, not a negative
recoupled witness.

## 4. The exterior Gram matrix need not be positive

There is a second tempting strengthening of the true problem.  For
orthonormal singular frames, define the \(4\times4\) exterior matrix
\[
 {\cal W}_{ij,kl}
 =
 \langle e_{ij}\wedge\overline f_{ij},
 (Z\otimes Z)
 (e_{kl}\wedge\overline f_{kl})\rangle.
 \tag{21}
\]
The actual Schmidt coefficients test \({\cal W}\) only on vectors
\[
 (s_1,s_2)\otimes(t_1,t_2),\qquad s_i,t_j\geq0.
 \tag{22}
\]
Requiring \({\cal W}\succeq0\) would be sufficient, but it is false.

Use computational strings in site order \(1,2,3\), and take the four
ordered two-frames
\[
\begin{aligned}
 X&=(|021\rangle,|011\rangle),&
 Y&=(|001\rangle,|021\rangle),\\
 U&=(|112\rangle,|122\rangle),&
 V&=(|122\rangle,|102\rangle).
\end{aligned}
 \tag{23}
\]
Direct exact contraction gives, in order \(00,01,10,11\),
\[
 \boxed{\qquad
 {\cal W}=
 \begin{pmatrix}
 4&0&0&0\\
 0&0&2&0\\
 0&2&0&0\\
 0&0&0&4
 \end{pmatrix}.
 \qquad}
 \tag{24}
\]
Its eigenvalues are
\[
 -2,\quad2,\quad4,\quad4,
 \tag{25}
\]
and a negative eigenvector is
\[
 (0,1,-1,0)^{\mathsf T}.
 \tag{26}
\]
When reshaped as a \(2\times2\) coefficient matrix, (26) has rank
two.  It is therefore not an admissible product of the two Schmidt
coefficient vectors.

Indeed, on the required product ray,
\[
\begin{aligned}
 &\bigl((s_1,s_2)\otimes(t_1,t_2)\bigr)^{\mathsf T}
 {\cal W}
 \bigl((s_1,s_2)\otimes(t_1,t_2)\bigr)\\
 &\qquad
 =4\left(
 s_1^2t_1^2+s_2^2t_2^2+s_1s_2t_1t_2
 \right)\geq0.
\end{aligned}
 \tag{27}
\]
Thus ordinary matrix positivity loses exactly the surviving
two-factor Segre constraint.

## 5. Remaining lemma

The grouped rank-two conjecture is now the explicit inequality (11).
Any proof must retain the common tensor-grid origin (3) and the
positive compensation \(\|H_{\rm a}\|_2^2\).  Neither a bound on the
three Gram matrices independently nor the ordinary Frobenius
cross-Gram contraction (18) can suffice.

Equivalently, it is enough—and in the singular-frame formulation
necessary—to prove positive-Segre copositivity of the exterior matrix
\({\cal W}\).  Equations (24)--(27) show that replacing this by
\({\cal W}\succeq0\) is invalid.

At the canonical rank-two zero obtained by replacing \(D\) in (14)
with \(P\), one has \(H_{\rm a}=0\) and equality in (18).  Hence both
terms in (12) are individually sharp, while the phase-flipped
example (14) proves that they must be coupled globally.
