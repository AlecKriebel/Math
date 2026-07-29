# The orthogonal-triple \(3/4\) constant is sharp

## Status

This note proves a sharp two-copy inequality which governs the
one-site-factorized boundary of the three-copy orthogonal-triple
problem.  It also gives an exact three-qubit equality construction.
It does **not** prove the global three-copy inequality.

For operators on \(n\) tensor factors, write
\[
 {\cal B}_n(A,B)
 =
 \sum_{S\subseteq[n]}
 \left(-\frac12\right)^{|S|}
 \left\langle\operatorname{Tr}_S A,
              \operatorname{Tr}_S B\right\rangle_{\rm HS},
 \qquad
 Q_n(A)={\cal B}_n(A,A).
 \tag{1}
\]
The live orthogonal-triple conjecture is
\[
 \left|{\cal B}_3(P_w,|u\rangle\langle v|)\right|^2
 \leq
 \frac34 Q_3(P_w)Q_3(|u\rangle\langle v|)
 \tag{2}
\]
for mutually orthonormal \(w,u,v\).

The independent exact checker is
`verification/verify_n3_orthogonal_triple_three_quarter_sharpness.py`.

## 1. A sharp two-copy theorem

Use the vectorization convention
\(\langle\!\langle A|B\rangle\!\rangle
=\operatorname{Tr}(A^\dagger B)\).

### Theorem 1

Let \(U,V\in M_2(\mathbb C)\) represent two orthonormal maximally
entangled two-qubit vectors, and let \(W\in M_2(\mathbb C)\) satisfy
\(\|W\|_2=1\).  Put
\[
 A=|W\rangle\!\rangle\langle\!\langle W|,
 \qquad
 B=|U\rangle\!\rangle\langle\!\langle V|.
 \tag{3}
\]
Then
\[
 \boxed{
 |{\cal B}_2(A,B)|^2
 \leq
 \frac34 Q_2(A)Q_2(B).}
 \tag{4}
\]
The constant \(3/4\) is attained.

#### Proof

Common local unitaries preserve every contraction in (1).  They put
the orthonormal maximally entangled pair into the form
\[
 U=\frac{I}{\sqrt2},\qquad V=\frac{X}{\sqrt2},
 \tag{5}
\]
up to an irrelevant scalar phase on \(V\).  Indeed, after sending
\(U\) to \(I/\sqrt2\), the matrix \(\sqrt2V\) is a traceless unitary.
A unitary conjugation diagonalizes its Pauli direction, and a final
one-qubit basis rotation sends that direction to \(X\).

Expand
\[
 W=\frac1{\sqrt2}(aI+bX+cY+dZ),
 \qquad
 |a|^2+|b|^2+|c|^2+|d|^2=1.
 \tag{6}
\]
Set
\[
 t=|\operatorname{Im}(\overline a b)|,
 \qquad
 D=a^2-b^2-c^2-d^2.
 \tag{7}
\]
A direct partial trace gives
\[
 Q_2(B)=\frac12,\qquad
 {\cal B}_2(A,B)
 =i\operatorname{Im}(\overline a b).
 \tag{8}
\]
Moreover,
\[
 \det W=\frac D2.
 \tag{9}
\]
The two reductions of the pure state
\(|W\rangle\!\rangle\) have common purity
\(1-2|\det W|^2\).  Hence
\[
 Q_2(A)
 =\frac54-\operatorname{Tr}(WW^\dagger)^2
 =\frac14+\frac12|D|^2.
 \tag{10}
\]

It remains to relate the phase interference \(t\) to \(D\).  Let
\(p=|a|^2+|b|^2\).  First,
\[
 p\geq2t.
 \tag{11}
\]
Writing \(r=\operatorname{Re}(\overline a b)\), one also has
\[
 |a^2-b^2|^2=p^2-4r^2\geq4t^2.
 \tag{12}
\]
Since
\[
 |c^2+d^2|\leq |c|^2+|d|^2=1-p,
 \tag{13}
\]
the reverse triangle inequality, (11), and (12) yield
\[
 |D|
 \geq \max\{0,\,2t-(1-p)\}
 \geq \max\{0,\,4t-1\}.
 \tag{14}
\]

If \(0\leq t\leq1/4\), then
\[
 \frac38Q_2(A)-t^2
 \geq\frac3{32}-\frac1{16}>0.
 \tag{15}
\]
If \(1/4\leq t\leq1/2\), (10) and (14) give
\[
 \begin{aligned}
 \frac38Q_2(A)-t^2
 &\geq
 \frac3{32}+\frac3{16}(4t-1)^2-t^2\\
 &=\frac{(8t-3)^2}{32}\geq0.
 \end{aligned}
 \tag{16}
\]
Equations (8), (15), and (16) prove (4).
\(\square\)

### Equality conditions

Equality in (4) occurs precisely when, after the harmless
normalizations used in (5),
\[
 \begin{gathered}
 |a|=|b|=\sqrt{\frac38},\qquad
 \operatorname{Re}(\overline a b)=0,\\
 |c|^2+|d|^2=\frac14,\qquad
 |c^2+d^2|=\frac14,
 \end{gathered}
 \tag{17}
\]
and \(c^2+d^2\) has the same phase as \(a^2-b^2\).

Indeed, equality in (16) forces \(t=3/8\), while equality throughout
(11)--(14) forces \(p=3/4\), equal moduli for \(a,b\), quadrature
phase, equality in (13), and equality in the reverse triangle
inequality.  Conversely these conditions give
\[
 t=\frac38,\qquad |D|=\frac12,
 \qquad Q_2(A)=\frac38,
 \tag{18}
\]
and hence equality in (4).

This classification is useful structurally: the \(3/4\) boundary is
not a numerical accident.  It is the unique balance point between
phase interference and the determinant forced by normalization.

## 2. Exact three-qubit equality

Choose
\[
 U=\frac I{\sqrt2},\qquad
 V=\frac X{\sqrt2},
 \tag{19}
\]
and
\[
 W=\frac1{\sqrt2}
 \left(
 \sqrt{\frac38}\,I
 i\sqrt{\frac38}\,X
 \frac12Y
 \right).
 \tag{20}
\]
These matrices have Hilbert--Schmidt norm one and
\(\langle\!\langle U|V\rangle\!\rangle=0\).  Equations
(8)--(10) give exactly
\[
 Q_2(P_W)=\frac38,\qquad
 Q_2(|U\rangle\!\rangle\langle\!\langle V|)=\frac12,\qquad
 {\cal B}_2(P_W,|U\rangle\!\rangle\langle\!\langle V|)
 =\frac{3i}{8}.
 \tag{21}
\]

Now add an orthogonal one-qubit flag:
\[
 w=|0\rangle\otimes|W\rangle\!\rangle,\qquad
 u=|1\rangle\otimes|U\rangle\!\rangle,\qquad
 v=|1\rangle\otimes|V\rangle\!\rangle.
 \tag{22}
\]
The three vectors are mutually orthonormal.  The form (1) tensorizes,
and on the flag qubit
\[
 Q_1(P_0)=Q_1(P_1)=\frac12,\qquad
 {\cal B}_1(P_0,P_1)=-\frac12.
 \tag{23}
\]
Consequently
\[
 \boxed{
 Q_3(P_w)=\frac3{16},\qquad
 Q_3(|u\rangle\langle v|)=\frac14,\qquad
 {\cal B}_3(P_w,|u\rangle\langle v|)
 =-\frac{3i}{16}.}
 \tag{24}
\]
Therefore
\[
 \frac{
 |{\cal B}_3(P_w,|u\rangle\langle v|)|^2
 }{
 Q_3(P_w)Q_3(|u\rangle\langle v|)
 }
 =
 \frac34.
 \tag{25}
\]

Thus any proof of (2) must retain the constant \(3/4\), and its
equality analysis must include a locally flagged two-copy
determinant/interference balance.  A counterexample, if one exists,
must exceed a boundary which is already exactly saturated in local
dimension two.

## 3. What remains

Theorem 1 completely settles the maximally-entangled-pair slice after
one orthogonal local flag.  It does not control an arbitrary
orthonormal tripartite triple, because the three one-site reduced
channels then share a genuinely three-party rank-one Stinespring
origin rather than a common product flag.

The exact global target remains (2).  The new strictly smaller
question suggested by the proof is whether the scalar determinant
penalty in (14) has a three-site analogue coupling all three
transition channels of one orthonormal triple.  Separate channel
versions cannot suffice; the common-origin no-go models in
`agent_n3_intersection_common_origin_moment.md` already rule that out.
