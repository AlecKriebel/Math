# The even-reduction identity

## 2026-07-28 11:16 PDT

This note records an exact comparison between the tensor endpoint form and
the same endpoint map applied after grouping all copies into one large
system.  It explains the two-copy sum of squares and isolates a stronger
positive-matrix conjecture as a cyclic sum of partial reduction forms.

Throughout this note the local dimension is three.  On the \(i\)-th tensor
factor define
\[
 {\cal R}_i(H)=\operatorname{Tr}_i(H)\otimes I_i-H,
\]
where the identity is inserted back in the \(i\)-th position.  Let
\[
 {\cal L}_i=\operatorname{Id}-\frac12\operatorname{Tr}_i(\,\cdot\,)
 \otimes I_i=\frac12(\operatorname{Id}-{\cal R}_i).
\]
For \(S\subseteq[n]\), write
\({\cal R}_S=\prod_{i\in S}{\cal R}_i\), with
\({\cal R}_\varnothing=\operatorname{Id}\).

Let \({\cal R}_{\rm g}\) and \({\cal L}_{\rm g}\) denote the corresponding
maps after grouping the \(3^n\)-dimensional tensor product into one system:
\[
 {\cal R}_{\rm g}(H)=\operatorname{Tr}(H)I-H,\qquad
 {\cal L}_{\rm g}(H)=H-\frac12\operatorname{Tr}(H)I.
\]

**Proposition 1 (even-reduction identity).**
\[
\boxed{\quad
 {\cal L}_1\cdots{\cal L}_n-2^{1-n}{\cal L}_{\rm g}
 =
 2^{1-n}
 \sum_{\substack{S\subseteq[n]\\ |S|\ {\rm even},\ |S|\ge2}}
 {\cal R}_S .
\quad}
\tag{1}
\]

**Proof.**  The trace-and-replace maps satisfy
\[
 \operatorname{Id}+{\cal R}_i
 =\operatorname{Tr}_i(\,\cdot\,)\otimes I_i.
\]
They commute, and applying all of them traces every local factor.  Hence
\[
 \operatorname{Id}+{\cal R}_{\rm g}
 =\prod_{i=1}^n(\operatorname{Id}+{\cal R}_i).
\tag{2}
\]
Using
\({\cal L}_i=(\operatorname{Id}-{\cal R}_i)/2\) and
\({\cal L}_{\rm g}=(\operatorname{Id}-{\cal R}_{\rm g})/2\), the left side
of (1) is
\[
\begin{aligned}
2^{-n}\left[
\prod_i(\operatorname{Id}-{\cal R}_i)
-\operatorname{Id}+{\cal R}_{\rm g}\right]
&=
2^{-n}\left[
\prod_i(\operatorname{Id}-{\cal R}_i)
+\prod_i(\operatorname{Id}+{\cal R}_i)-2\operatorname{Id}\right]\\
&=
2^{1-n}
\sum_{\substack{S\subseteq[n]\\|S|\ {\rm even},\ |S|\ge2}}
{\cal R}_S.
\end{aligned}
\]
The last equality follows by expanding both products: odd monomials cancel,
the empty monomial is removed, and each nonempty even monomial occurs
twice. \(\square\)

Taking the Hilbert--Schmidt inner product with a Hermitian matrix \(H\)
gives
\[
\boxed{\quad
Q_n(H)-2^{-n}\left(2\operatorname{Tr}H^2-(\operatorname{Tr}H)^2\right)
=
2^{1-n}
\sum_{\substack{S\subseteq[n]\\|S|\ {\rm even},\ |S|\ge2}}
\langle H,{\cal R}_S(H)\rangle .
\quad}
\tag{3}
\]
For a positive matrix of rank at most two with eigenvalues
\(\lambda_1,\lambda_2\), the grouped term is
\[
2^{-n}\left(2\operatorname{Tr}H^2-(\operatorname{Tr}H)^2\right)
=2^{-n}(\lambda_1-\lambda_2)^2.
\tag{4}
\]
Consequently the sharp quantitative endpoint conjecture on positive
rank-two matrices is equivalent to nonnegativity of the even-reduction sum
on the right of (3).  For a rank-two orthogonal projection the grouped term
vanishes, so
\[
Q_n(P)=
2^{1-n}
\sum_{\substack{S\subseteq[n]\\|S|\ {\rm even},\ |S|\ge2}}
\langle P,{\cal R}_S(P)\rangle .
\tag{5}
\]

At \(n=2\), (3) contains only
\(\frac12\langle H,{\cal R}_1{\cal R}_2(H)\rangle\).  For \(H\succeq0\)
this is the previously proved nonnegative double-antisymmetrizer term, so
(3) recovers the sharp two-copy theorem.

At \(n=3\), (5) becomes the genuinely cyclic assertion
\[
Q_3(P)=\frac14\left(
\langle P,{\cal R}_1{\cal R}_2(P)\rangle+
\langle P,{\cal R}_1{\cal R}_3(P)\rangle+
\langle P,{\cal R}_2{\cal R}_3(P)\rangle\right).
\tag{6}
\]
Individual summands in (6) need not be nonnegative.  Thus (1) does not give
a termwise proof; its value is that it identifies the exact cyclic
compensation which an induction or sum-of-squares certificate must retain.

No claim that the right side of (3) is always nonnegative is made here.
That assertion is the live stronger positive-matrix conjecture.
