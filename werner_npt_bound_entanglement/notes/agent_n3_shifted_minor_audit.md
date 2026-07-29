# Three-copy arbitrary-rank-two shifted-minor audit

**Status (2026-07-28 21:45 PDT).**  The sharp three-copy inequality
\[
Q_3(C)\geq\frac18(s_1-s_2)^2,\qquad \operatorname{rank}C\leq2,
\tag{1}
\]
remains unproved.  This note records an exact two-plane reduction and two
exact obstructions to tempting stronger intermediate inequalities.  The
first obstruction disproves the unshifted cyclic even-reduction route.
The second shows that the live shifted minor cannot be proved by routing its
crossed entry through the ordinary matched Gram entry.

No floating-point calculation below is used as a certificate.

## 1. Exact even-reduction identity

Put
\[
E(C)=3\|C\|_2^2-2\sum_{i=1}^3\|\operatorname{Tr}_iC\|_2^2
+ \sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2.
\tag{2}
\]
Direct comparison of coefficients in the partial-trace expansion gives
\[
\boxed{\quad
8Q_3(C)=2\|C\|_2^2-|\operatorname{Tr}C|^2+2E(C).
\quad}
\tag{3}
\]
If the nonzero singular values are \(s_1,s_2\), then (1) is therefore
equivalent to
\[
\boxed{\quad
2E(C)+(s_1+s_2)^2-|\operatorname{Tr}C|^2\geq0.
\quad}
\tag{4}
\]
Thus \(E(C)\geq0\) would be sufficient, but it is stronger than the live
target: the trace/nuclear-norm defect in (4) is essential.

## 2. Exact refutation of \(E(C)\geq0\)

In three qutrits set
\[
P_2=\operatorname{diag}(1,1,0),\qquad
N=|0\rangle\langle1|,\qquad R=|0\rangle\langle0|,
\]
and
\[
C=P_2\otimes N\otimes R.
\tag{5}
\]
The rank is \(2\), and the two nonzero singular values are both one.  Direct
tensor contraction gives
\[
\|C\|_2^2=2,
\]
\[
\bigl(\|\operatorname{Tr}_1C\|_2^2,
\|\operatorname{Tr}_2C\|_2^2,
\|\operatorname{Tr}_3C\|_2^2\bigr)=(4,0,2),
\]
and
\[
\bigl(\|\operatorname{Tr}_{12}C\|_2^2,
\|\operatorname{Tr}_{13}C\|_2^2,
\|\operatorname{Tr}_{23}C\|_2^2\bigr)=(0,4,0).
\]
Consequently
\[
\boxed{\quad E(C)=6-12+4=-2.\quad}
\tag{6}
\]
This is not a counterexample to (1).  Tensor factorization gives
\[
Q_3(C)=Q_1(P_2)Q_1(N)Q_1(R)=0,
\tag{7}
\]
and (4) is saturated:
\[
2E(C)+(s_1+s_2)^2-|\operatorname{Tr}C|^2=-4+4=0.
\]
The independent exact verifier is
`verification/verify_n3_even_reduction_obstruction.py`.

## 3. Invariant two-plane shifted minor

Write a singular-value decomposition
\[
C=s_1|u_1\rangle\langle v_1|
+ s_2|u_2\rangle\langle v_2|,
\tag{8}
\]
with both displayed pairs orthonormal.  On two physical replicas define
\[
Y=\bigotimes_{i=1}^3\left(I-\frac12F_i\right),\qquad
N=8Y=\bigotimes_{i=1}^3(2I-F_i),\qquad M=N-I\succeq0.
\tag{9}
\]
Let \(x_{ab}=u_a\otimes v_b\), with conjugation placed according to the
fixed vectorization convention.  Since
\(\langle x_{12},x_{21}\rangle=0\), set
\[
g_1=\langle x_{11},Mx_{11}\rangle,\qquad
g_2=\langle x_{22},Mx_{22}\rangle,\qquad
h=\langle x_{12},Nx_{21}\rangle.
\tag{10}
\]
Then \(g_1,g_2\geq0\), and the rank-one replica formula gives
\[
8Q_3(C)
=s_1^2(1+g_1)+s_2^2(1+g_2)
+2s_1s_2\operatorname{Re}h.
\tag{11}
\]
Allowing an arbitrary relative phase of the second singular summand and
using the elementary copositivity criterion shows that the sharp inequality
(1), uniformly over that phase, is exactly
\[
\boxed{\quad |h|\leq1+\sqrt{g_1g_2}.\quad}
\tag{12}
\]
Equivalently, if
\[
K=(U^\dagger\otimes V^\dagger)N(U\otimes V),
\tag{13}
\]
then (12) is the shifted anti-diagonal minor
\[
|K_{12,21}|
\leq
1+\sqrt{(K_{11,11}-1)(K_{22,22}-1)}.
\tag{14}
\]
This is the live exact two-plane target.

## 4. Why ordinary Gram routing fails

Because \(M\succeq0\), a natural attempt is to introduce the ordinary
matched entry
\[
d=\langle x_{11},Nx_{22}\rangle
\tag{15}
\]
and try to prove \(|h|\leq1+|d|\), followed by
\(|d|\leq\sqrt{g_1g_2}\).  The first inequality is false by an exact
computational-basis code.

On three qubits (and hence embedded in three qutrits), take
\[
u_1=|000\rangle,\quad u_2=|001\rangle,\quad
v_1=|110\rangle,\quad v_2=|111\rangle.
\tag{16}
\]
The two pairs are orthonormal.  Matrix elements of one local factor are
\[
\langle a,b|(2I-F)|c,d\rangle
=2\delta_{ac}\delta_{bd}-\delta_{ad}\delta_{bc}.
\tag{17}
\]
Multiplying the three local factors gives
\[
g_1=g_2=3,\qquad h=-4,\qquad d=0.
\tag{18}
\]
Thus the true shifted inequality is sharp,
\[
|h|=4=1+\sqrt{3\cdot3},
\]
while the proposed bridge would assert \(4\leq1\).

This example also explains the complement mechanism that a successful
exterior proof must retain.  At the first two sites the crossed matrix
element uses the identity contraction of weight \(2\), while at the third
site it uses the swap contraction of weight \(-1\).  The matched norms
collect the complementary nonempty branches, but their *ordinary inner
product* is zero.  A proof must compare the full complementary norms
without collapsing them to their matched inner product.

## 5. Discovery evidence, kept separate

An unrestricted complex Stiefel search in \(d=3,n=3\) found no negative
\(Q_3\) value in 1,000 general and 540 normal independent starts.  With
the singular values fixed, minima at nine ratios matched
\(\frac18(s_1-s_2)^2\) to floating-point precision.  Interior log-determinant
barriers stayed positive and approached common-local-qubit equality
boundaries as the barrier was removed.  These facts motivated (12), but
they are not evidence in the proof layer.

The exact conclusions of this note are only (3)--(4), the counterexample
(5)--(7), the equivalence (12), and the obstruction (16)--(18).

## 6. Exact phase obstruction to a fixed-center Gram certificate

A tempting strengthening of (12) is the fixed-center disk
\[
 \boxed{\qquad |h+1|^2\leq g_1g_2. \qquad}                 \tag{19}
\]
If true, (19) would imply the live estimate by the triangle inequality.
It is false for the simplest possible reason: it is not covariant under
the independent phase freedom of the two singular flags.

Use the exact basis grid (16)--(18), for which
\[
 (g_1,g_2,h)=(3,3,-4).
\]
Replace only the second right frame vector by
\[
 v_2'=-v_2.
\]
The pair \((v_1,v_2')\) is still orthonormal.  Both diagonal quantities
\(g_1,g_2\) are unchanged, while the crossed entry changes sign:
\[
 (g_1',g_2',h')=(3,3,4).
\]
Consequently
\[
 |h'+1|^2=25>9=g_1'g_2'.                                  \tag{20}
\]
This is an exact counterexample to (19).  More generally,
\(v_2\mapsto e^{i\theta}v_2\) rotates \(h\) while leaving \(g_1,g_2\)
fixed.  Hence no Gram construction with a fixed scalar center can prove
the phase-invariant target (12).

The same grid simultaneously saturates both viable phase-covariant
boundaries:
\[
 |h|=1+\sqrt{g_1g_2}=4,
 \qquad
 |h|^2=(1+g_1)(1+g_2)=16.                                 \tag{21}
\]
The second equality is the determinant-zero condition for
\[
 \begin{pmatrix}
  1+g_1&h\\ \overline h&1+g_2
 \end{pmatrix}.                                           \tag{22}
\]
Thus a proof of mere three-copy nonnegativity may target the weaker
phase-covariant minor (22), whereas a proof of the sharp singular-value
bound must retain the stronger radius \(1+\sqrt{g_1g_2}\).  In either
case the exterior correction must transform with the phase of \(h\);
a fixed \(+1\) cannot be the missing Plücker term.
