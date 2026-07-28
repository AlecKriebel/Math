# Arbitrary two-planes in the qutrit repetition subspace

## Checkpoint

This note closes an all-copy subclass which directly tests the negative
three-point Gram direction of the one-copy endpoint kernel.  Although the
one-copy kernel on three mutually orthogonal qutrit states is indefinite,
coherent repetition of those three states cannot activate a negative
rank-two code projection.

Let
\[
 {\cal G}_n=\operatorname{span}\{
 e_0,e_1,e_2\},\qquad e_a=|a\rangle^{\otimes n}.
\]

### Theorem

Every rank-two orthogonal projection \(P\) supported on \({\cal G}_n\)
satisfies \(Q_n(P)\geq0\).  More precisely, write
\[
 P=I_{{\cal G}_n}-|z\rangle\langle z|,
 \qquad z=\sum_{a=0}^2z_ae_a,\qquad
 \sum_a|z_a|^2=1,
\]
and put \(s=\sum_a|z_a|^4\).  Then
\[
\boxed{
 Q_n(P)=
 \begin{cases}
 (1-s)(1-2^{1-n}),&n\ \mathrm{odd},\\[1mm]
 1-s+2^{2-n},&n\ \mathrm{even}.
 \end{cases}}
\tag{1}
\]
Consequently, for odd \(n\geq3\), equality holds exactly when \(z\) is
one of the three repetition basis vectors.  For even \(n\), the minimum
is \(2^{2-n}\), again attained exactly at those three vectors.  At
\(n=1\), every rank-two qutrit projection is an equality case.

### Proof

Let \(E_{ab}=|a\rangle\langle b|\) on one qutrit.  The endpoint
sesquilinear form is
\[
 {\cal B}_n(C,D)
 =\langle C,{\cal L}^{\otimes n}(D)\rangle_{\rm HS},
 \qquad {\cal L}(X)=X-\frac12\operatorname{Tr}(X)I_3.
\]
On one-site matrix units,
\[
 {\cal B}_1(E_{ab},E_{cd})
 =\delta_{ac}\delta_{bd}
  -\frac12\delta_{ab}\delta_{cd}.                 \tag{2}
\]
Since
\[
 |e_a\rangle\langle e_b|=E_{ab}^{\otimes n},
\]
the form tensorizes.  If \(M=(M_{ab})\) is the coefficient matrix of an
operator supported on \({\cal G}_n\), (2) gives
\[
\begin{aligned}
Q_n(M)
={}&\sum_{a\ne b}|M_{ab}|^2\\
&+2^{-n}\left[
 \sum_a|M_{aa}|^2
+(-1)^n\sum_{a\ne c}\overline{M_{aa}}M_{cc}
\right].
\end{aligned}                                             \tag{3}
\]
For \(M=I-|z\rangle\langle z|\), put \(p_a=|z_a|^2\).  Then
\[
\sum_{a\ne b}|M_{ab}|^2
=\sum_{a\ne b}p_ap_b=1-s,                                 \tag{4}
\]
\[
\sum_a|M_{aa}|^2
=\sum_a(1-p_a)^2=1+s,                                     \tag{5}
\]
and \(\sum_aM_{aa}=2\).  Therefore the square bracket in
(3) is \(4\) when \(n\) is even, whereas for odd \(n\) it is
\[
2(1+s)-4=-2(1-s).                                         \tag{6}
\]
Substitution proves (1).

Finally \(1/3\leq s\leq1\), and \(s=1\) holds exactly when one \(p_a\)
equals one.  The equality and minimum statements follow immediately.
\(\square\)

### Significance and limitation

For the three one-copy projectors \(p_a=|a\rangle\langle a|\), the Gram
matrix \(({\cal B}_1(p_a,p_b))_{a,b}\) has diagonal \(1/2\), off-diagonal
\(-1/2\), and hence a negative all-ones eigenvector.  Formula (1) shows
exactly why the most direct coherent repetition encoding of this local
negative direction still cannot produce a Werner witness.

The calculation uses the qutrit-specific fact that a two-plane in the
three-dimensional repetition subspace is the orthogonal complement of
one vector.  It does not control arbitrary two-dimensional codes in
\((\mathbb C^3)^{\otimes n}\).
