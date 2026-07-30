# An exact obstruction to an inertia-only proof of the compensated residual

## Status

The two-pair full-dual residual admits the primal form
\[
 {\cal F}(C)=2Q_3(C)+3w_{011}(C),                       \tag{1}
\]
where \(w_{011}\) is the squared Hilbert--Schmidt mass in the sector
which is scalar on site \(1\) and traceless on sites \(2,3\).

For a rank-two \(C=A+iB\), both Hermitian quadratures \(A,B\) have at
most two positive and at most two negative eigenvalues.  This note
shows that this inertia information alone cannot prove
\({\cal F}(C)\geq0\): there is an exact Hermitian operator of inertia
\((2,2)\) on which \({\cal F}\) is strictly negative.

Consequently any Hermitian-quadrature proof must use the coupled
condition
\[
 \operatorname{rank}(A+iB)\leq2,                        \tag{2}
\]
not merely separate spectral constraints on \(A\) and \(B\).

The dependency-free checker is
`verification/verify_n3_compensated_inertia_obstruction.py`.

## 1. The operator

On one qutrit put
\[
 R=|0\rangle\langle0|.
 \tag{3}
\]
On sites \(2,3\), define
\[
 K=R\otimes I-I\otimes R,                               \tag{4}
\]
and on three sites define
\[
 \boxed{\qquad H=R\otimes K.\qquad}                     \tag{5}
\]

The spectrum of \(K\) is immediate in the computational basis:
\[
\begin{array}{c|c|c}
\text{vectors}&\text{eigenvalue}&\text{multiplicity}\\ \hline
|0j\rangle,\ j=1,2&+1&2\\
|j0\rangle,\ j=1,2&-1&2\\
\text{all remaining basis vectors}&0&5.
\end{array}                                             \tag{6}
\]
Tensoring with \(R\) only adds zero directions.  Hence
\[
 \boxed{\operatorname{rank}H=4,\qquad
        \operatorname{inertia}H=(2,2).}                 \tag{7}
\]

## 2. Exact negative value

Let
\[
 L(A)=A-\frac12\operatorname{Tr}(A)I.
 \tag{8}
\]
Since \(\|R\|_2^2=\operatorname{Tr}R=1\),
\[
 Q_1(R)=\langle R,L(R)\rangle=\frac12.                  \tag{9}
\]

Write
\[
 p=\frac13I,\qquad q=R-\frac13I.
 \tag{10}
\]
Then
\[
 K=3(q\otimes p-p\otimes q).                            \tag{11}
\]
Thus \(K\) lies entirely in the one-traceless-factor sector of the
two-site scalar/traceless decomposition.  On that sector
\(L^{\otimes2}\) has eigenvalue \(-1/2\).  Since
\[
 \|K\|_2^2=4,                                           \tag{12}
\]
we get
\[
 Q_2(K)=-\frac12\|K\|_2^2=-2.                          \tag{13}
\]
Tensor factorization now gives
\[
 Q_3(H)=Q_1(R)Q_2(K)=-1.                               \tag{14}
\]

The component of \(K\) which is traceless on both sites vanishes by
(11).  Therefore
\[
 w_{011}(H)=0.                                          \tag{15}
\]
Substitution into (1) yields the exact obstruction
\[
 \boxed{\qquad {\cal F}(H)=-2.\qquad}                   \tag{16}
\]

## 3. Consequence

Every Hermitian quadrature of a rank-two complex matrix has inertia at
most \((2,2)\), but (16) shows that the compensated form is not
nonnegative on that entire inertia cone.  In particular, an argument
of the form
\[
 C=A+iB,\qquad
 {\cal F}(C)={\cal F}(A)+{\cal F}(B),
 \tag{17}
\]
cannot close by proving separate inertia-only lower bounds for
\({\cal F}(A)\) and \({\cal F}(B)\).

The obstruction does **not** disprove the physical rank-two
inequality.  It identifies exactly what such a proof must retain:
the common factorization, complex-structure identity, or equivalent
determinantal relations enforcing (2).
