# Majid--Markl Hecke gluing no-go at the exceptional phase

**Date:** 2026-07-29
**Scope:** the associative Hecke gluing
\(\mathbin{\oplus_{\mathfrak q}}\), including arbitrary positive
one-site metrics; and the full operator-valued gluing form of
Majid--Markl Theorem 2.7 when the color summands are orthogonal
**Status:** exact no-go theorems; not a no-go for unrestricted
operator-valued mixed blocks outside the stated gluing geometry

## 1. Conclusion

Majid and Markl introduced an associative operation that glues two
Hecke Yang--Baxter operators on \(X\) and \(Y\) into one on
\(X\oplus Y\).  This is an obvious literature candidate for adjoining a
two-dimensional sector to the known four-dimensional exceptional
solution.

It cannot produce a unitary exceptional matrix.  There are two exact
levels to the obstruction.

> **Theorem A.** Let \(|\mathfrak q|=1\) and
> \(\mathfrak q\neq\pm1\), and let \(X,Y\) be nonzero complex vector
> spaces.  No positive-definite inner product on \(X\oplus Y\) makes
> the Majid--Markl glued operator
> \(R\mathbin{\oplus_{\mathfrak q}}R'\) unitary for the induced tensor
> product inner product.

The obstruction is entirely in one mixed two-dimensional slice and is
independent of the two input operators.

> **Theorem B.** Let \(\lambda,\mu\in\mathbb C^\times\) be distinct,
> with \(\lambda+\mu\ne0\).  No operator of the full
> Majid--Markl Theorem 2.7 form on a nontrivial orthogonal Hilbert direct
> sum \(X\oplus Y\) is both unitary and annihilated by
> \((z-\lambda)(z-\mu)\).

Theorem B allows arbitrary operator-valued \(U,S,T\) in the mixed
blocks.  The quadratic relation forces
\[
T=(\lambda+\mu)I,\qquad
SU=-\lambda\mu I,\qquad
US=-\lambda\mu I.
\]
Unitarity forces \(T=0\), a contradiction.  Thus the full
operator-valued compatibility system does not repair the canonical
gluing when the color summands are orthogonal.

For the normalization used in this project, put
\[
Q=e^{i\pi/3},\qquad
\mathfrak q=e^{i\pi/6}.
\]
Multiplying an exceptional operator with spectrum \(\{-1,Q\}\) by
\(e^{-i\pi/6}\) gives the Majid--Markl Hecke spectrum
\[
\{\mathfrak q,-\mathfrak q^{-1}\}.
\]
The scalar phase does not affect unitarity, so the theorem rules out the
standard associative gluing mechanism at exactly the required
exceptional parameter.

These results identify a named literature construction inside the
broader colored direct-sum audit in
`notes/track_additive_constructions.md`.  They do not exclude arbitrary
unitary mixed blocks with both color-changing directions present, nor
do they exclude a Theorem 2.7 algebraic operator that becomes unitary
only for a local metric in which \(X\) and \(Y\) are nonorthogonal.

## 2. Exact mixed block

Majid--Markl, Theorem 2.4, uses the Hecke convention
\[
(\mathcal R-\mathfrak q I)
(\mathcal R+\mathfrak q^{-1}I)=0
\]
and defines
\[
\begin{aligned}
(R\mathbin{\oplus_{\mathfrak q}}R')(x\otimes y)
   &=y\otimes x,\\
(R\mathbin{\oplus_{\mathfrak q}}R')(y\otimes x)
   &=x\otimes y+
     (\mathfrak q-\mathfrak q^{-1})y\otimes x
\end{aligned}
\tag{1}
\]
for \(x\in X\), \(y\in Y\).

Fix nonzero \(x\) and \(y\), and abbreviate
\[
c=\mathfrak q-\mathfrak q^{-1}.
\]
On the ordered span
\((x\otimes y,y\otimes x)\), equation (1) has the matrix
\[
C_{\mathfrak q}
=
\begin{pmatrix}
0&1\\
1&c
\end{pmatrix}.
\tag{2}
\]
When \(|\mathfrak q|=1\),
\[
c=2i\operatorname{Im}\mathfrak q
\]
is purely imaginary, and it is nonzero when
\(\mathfrak q\neq\pm1\).

## 3. Product-metric obstruction

Allow an arbitrary positive-definite inner product on \(X\oplus Y\);
the decomposition need not be orthogonal.  Put
\[
A=\|x\|^2\|y\|^2>0,\qquad
B=|\langle x,y\rangle|^2\geq0.
\]
The two mixed simple tensors have Gram matrix
\[
G=
\begin{pmatrix}
A&B\\
B&A
\end{pmatrix}.
\tag{3}
\]
In particular, their cross inner product is real.  From (1),
\[
\begin{aligned}
\bigl\|
(R\mathbin{\oplus_{\mathfrak q}}R')(y\otimes x)
\bigr\|^2
&=\|x\otimes y+c\,y\otimes x\|^2\\
&=(1+|c|^2)A+
  2\operatorname{Re}(cB)\\
&=(1+|c|^2)A\\
&>A
=\|y\otimes x\|^2.
\end{aligned}
\tag{4}
\]
Thus the glued operator fails even norm preservation, for every
positive one-site metric.  This proves the theorem.

At the exceptional normalization,
\[
\mathfrak q=\frac{\sqrt3+i}{2},
\qquad c=i,
\]
so the squared norm in (4) doubles.

## 4. Full operator-valued gluing with orthogonal colors

Majid--Markl Theorem 2.7 considers arbitrary invertible maps
\[
U:X\otimes Y\longrightarrow Y\otimes X,\qquad
S:Y\otimes X\longrightarrow X\otimes Y
\]
and a map
\[
T:Y\otimes X\longrightarrow Y\otimes X.
\]
On the mixed space
\[
(X\otimes Y)\oplus(Y\otimes X)
\]
their operator has block matrix
\[
\mathcal Q_{\rm mix}
=
\begin{pmatrix}
0&S\\
U&T
\end{pmatrix}.
\tag{5}
\]
This is the complete mixed-block form in their theorem, before any of
its Yang--Baxter compatibility equations are imposed.

Suppose
\[
(\mathcal Q_{\rm mix}-\lambda I)
(\mathcal Q_{\rm mix}-\mu I)=0.
\tag{6}
\]
Write
\[
a=\lambda+\mu,\qquad b=\lambda\mu.
\]
The four blocks of
\(\mathcal Q_{\rm mix}^2-a\mathcal Q_{\rm mix}+bI=0\)
give
\[
\begin{aligned}
SU+bI&=0,\\
S(T-aI)&=0,\\
(T-aI)U&=0,\\
US+T^2-aT+bI&=0.
\end{aligned}
\tag{7}
\]
Since \(U\) and \(S\) are invertible, the middle equations force
\[
T=aI.
\tag{8}
\]
The first equation gives \(SU=-bI\), hence also \(US=-bI\);
the last equation is then automatic.

Now give \(X\oplus Y\) an inner product for which \(X\perp Y\).
The two mixed color sectors are orthogonal.  If
\(\mathcal Q_{\rm mix}\) is unitary, its upper-left block in
\(\mathcal Q_{\rm mix}^*\mathcal Q_{\rm mix}=I\) gives
\[
U^*U=I,
\]
and its upper-right block gives
\[
U^*T=0.
\tag{9}
\]
Invertibility of \(U\) therefore forces \(T=0\).  Combining with (8)
gives
\[
\lambda+\mu=0.
\tag{10}
\]
This proves Theorem B.

For the exceptional roots \(\{-1,Q\}\),
\[
\lambda+\mu=Q-1=\frac{-1+i\sqrt3}{2}\ne0.
\]
Thus Theorem B applies.  In the
Majid--Markl-scaled roots
\(\{\mathfrak q,-\mathfrak q^{-1}\}\), their sum is
\(\mathfrak q-\mathfrak q^{-1}=i\), again nonzero.

The proof uses neither the detailed Yang--Baxter compatibility equations
(I)--(VI)\('\) nor the internal operators on \(X^{\otimes2}\) and
\(Y^{\otimes2}\).  It is therefore a complete no-go for the orthogonal
Hilbert-space realization of the entire Theorem 2.7 architecture.

## 5. Relation to the existing additive audit

The mixed block (2) is scalar on the internal \(X\otimes Y\) factors and
therefore belongs to the scalar-natural colored direct-sum ansatz
excluded in Section 3 of `notes/track_additive_constructions.md`.
That earlier calculation solved the full mixed-color braid equations in
the project's \(\{-1,Q\}\) normalization.  The present argument adds two
things:

1. it explicitly audits the associative gluing construction in the
   prior Hecke literature;
2. it rules out unitarization of the canonical construction by **any**
   positive one-site metric, not only the initially chosen orthogonal
   direct-sum metric;
3. it rules out all operator-valued Theorem 2.7 mixed blocks when the
   color summands are orthogonal.

The remaining colored \(d=6\) problem must either allow both off-diagonal
mixed-color outputs outside the triangular form (5), or use a
nonorthogonal algebraic color splitting.  Neither possibility is a
Majid--Markl orthogonal gluing.

## 6. Exact replay

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_majid_markl_gluing_no_go.py
```

The verifier checks the normalization change, the Hecke polynomial of
the canonical mixed block, the exact product-Gram defect, and the
general operator-block polynomial/unitarity contradiction.  Its retained
output is
`results/majid_markl_gluing_no_go_exact.txt`.

## 7. Primary source

- S. Majid and M. Markl, *Glueing operation for R-matrices, quantum
  groups and link-invariants of Hecke type*, Theorems 2.4 and 2.7,
  arXiv:hep-th/9308072; Math. Proc. Cambridge Philos. Soc. **119**
  (1996), 139--166.
