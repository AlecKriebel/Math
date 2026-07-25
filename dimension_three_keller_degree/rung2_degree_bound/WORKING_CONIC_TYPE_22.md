# Working theorem: the conic-image \((2,2)\) stratum

**Status:** proved and independently adversarially audited, including the
full degree-six exclusion.  This is not peer reviewed.  The source-specific
priority search is not a guarantee of worldwide priority.

**Recorded:** 2026-07-24T23:59:52Z.

## 1. Statement

Let \(F=L_0X+H_2+H_3+H_4\) be a total-degree-four Keller map over
\(\mathbb C\).  Assume that, after target coordinates,
\[
H_4=\operatorname{Ver}(p,q)=(p^2,pq,q^2),
\tag{1}
\]
where \(p,q\) are coprime nonproportional homogeneous quadrics.

Put
\[
D=\nabla p\times\nabla q,\qquad
n=(q^2,-2pq,p^2)^T.
\tag{2}
\]

### Theorem

There is no such Keller map if the pencil \(\langle p,q\rangle\) has no
double-line member.

More precisely, the degree-eight and degree-seven identities first force
linear forms \(\ell,m\) and a constant \(3\times2\) matrix \(M\) such that
\[
\boxed{
H_4+H_3+H_2
=
\operatorname{Ver}(p+\ell,q+m)+M(p,q).
}
\tag{3}
\]
The degree-six identity then contradicts the Keller condition.

If the pencil has a unique double-line member \(L^2\), the degree-eight
identity instead permits the exact normal components
\[
n\cdot H_3
=cL^j\Phi_{(7-j)/2}(p,q),
\qquad j\in\{1,3,5,7\},
\tag{4}
\]
where \(\Phi_k\) is a binary form of degree \(k\).

Thus a conic-image \((2,2)\) leading part compatible with a quartic Keller
map must lie in the unique-double-line exceptional locus.

## 2. Primitive-fibre and homogeneous first-integral lemmas

Under coprimality, if the pencil has at most one double-line member, its
generic conic is geometrically integral.  Indeed, suppose every pencil
member is singular.  If the pencil is not binary, choose a rank-two member
and diagonalize it to \(X_1^2+X_2^2\).  Write the other member as the
symmetric matrix
\[
Q=
\begin{pmatrix}
a&b&c\\
b&d&e\\
c&e&f
\end{pmatrix}.
\]
Then
\[
\det\!\left(
\begin{pmatrix}1&0&0\\0&1&0\\0&0&0\end{pmatrix}
+tQ\right)
=ft+\bigl(f(a+d)-c^2-e^2\bigr)t^2+(\det Q)t^3.
\]
If this vanishes identically, \(f=0\), \(c^2+e^2=0\), and
\(\det Q=0\).  If \(c=e=0\), both quadrics are binary and their projective
pencil is a line in \(\mathbb P(\operatorname{Sym}^2\mathbb C^2)\); that
line meets the Veronese conic of squares.  If \(c\ne0\), then
\(e=\pm ic\), and \(\det Q=0\) becomes
\[
a-d\pm2ib=0.
\]
In the corresponding sign, \(Q\) is divisible by
\(X_1\pm iX_2\), which also divides \(X_1^2+X_2^2\).  Thus the determinant
calculation forces either:

- both quadrics to be binary, in which case their projective pencil meets
  the Veronese conic of double lines in two points counted with
  multiplicity; or
- a common linear factor \(X_1+iX_2\) or \(X_1-iX_2\), contradicting
  coprimality.

The binary intersection cannot be supported at a single double line:
the tangent line to the Veronese at \(L^2\) consists entirely of binary
quadrics divisible by \(L\), again contradicting coprimality.  Hence a
coprime binary pencil has two distinct double-line members, contrary to the
at-most-one hypothesis.

Thus
\[
\mathbb C(p/q)
\quad\text{is relatively algebraically closed in}\quad
\mathbb C(\mathbb P^2).
\tag{5}
\]
This applies both to the no-double-line branch and to the unique-double-line
branch used below.

We also need a homogeneous first-integral lemma.  Let \(p,q\) have common
degree \(d>0\), let \(R\ne0\) be homogeneous of degree \(e\), and suppose
\(D(R)=0\).  For
\[
g=\gcd(d,e),\qquad a=d/g,\qquad b=e/g,
\]
the degree-zero function \(w=R^a/q^b\) is algebraic over
\(\mathbb C(p/q)\).

Indeed, nonproportional \(p,q\) are algebraically independent: a polynomial
relation, split into scaling-homogeneous pieces, would make \(p/q\)
algebraic over \(\mathbb C\), hence constant.  Thus \(D\ne0\).  The kernel
of a nonzero derivation of \(\mathbb C(X_1,X_2,X_3)\) has transcendence
degree at most two; otherwise the full function field would be algebraic
over the kernel and the characteristic-zero derivation would vanish.
The kernel contains \(\mathbb C(p,q)\), so \(R\), and hence \(w\), is
algebraic over \(\mathbb C(p,q)=\mathbb C(p/q,q)\).

Writing \(E=\mathbb C(\mathbb P^2)\), the homogeneous element \(q\) is
transcendental over \(E\), as scaling fixes \(E\) and produces infinitely
many multiples of \(q\).  Were \(w\) transcendental over
\(\mathbb C(p/q)\), the pair \(p/q,w\) would be a transcendence basis of
\(E\); adjoining \(q\) would make \(p/q,w,q\) algebraically independent,
contradicting the preceding algebraicity.

## 3. Degree eight

Let \(C=JH_4\).  Direct minors give
\[
\operatorname{adj}(C)=2D\,n^T.
\tag{6}
\]
For \(B=JH_3\), the degree-eight Keller identity is
\[
\operatorname{tr}(\operatorname{adj}(C)B)=0.
\]
Since \(D(n)=0\), (6) becomes
\[
D(n\cdot H_3)=0.
\tag{7}
\]

Set \(S=n\cdot H_3\), a homogeneous form of degree \(7\).  If \(S\ne0\),
then
\[
\frac{S^2}{q^7}
\]
is degree zero and invariant under \(D\).  The case \((d,e)=(2,7)\) of the
homogeneous first-integral lemma and then (5) show that it belongs to
\(\mathbb C(p/q)\).  Weil divisors give
\[
2\operatorname{div}(S)=u^*B_7
\]
for an effective degree-seven divisor \(B_7\) on the base of the pencil.
Every odd coefficient of \(B_7\) forces the corresponding conic to be a
double line.

With no double line, all coefficients would be even, contradicting degree
seven.  Hence \(S=0\).  The syzygy module of
\[
(q^2,-2pq,p^2)
\]
is generated by
\[
(2p,q,0),\qquad(0,p,2q).
\]
Degree comparison therefore gives unique linear forms \(\ell,m\) with
\[
H_3=
\bigl(2p\ell,\ q\ell+pm,\ 2qm\bigr)
=d\operatorname{Ver}_{(p,q)}(\ell,m).
\tag{8}
\]

If there is one double line, relative algebraic closedness forbids a
second.  The odd coefficient supported there can be
\(j=1,3,5,7\); halving all remaining even coefficients gives exactly (4).

## 4. Degree seven

Put
\[
\theta=q\ell-pm.
\]
An independent exterior expansion of the degree-seven determinant gives
\[
\operatorname{Jac}
\bigl(p,q,n\cdot H_2-\theta^2\bigr)=0.
\tag{9}
\]
Since
\[
n\cdot\operatorname{Ver}(\ell,m)=\theta^2,
\]
set
\[
K=H_2-\operatorname{Ver}(\ell,m).
\]
The form \(n\cdot K\) has degree \(6\).  The case \((d,e)=(2,6)\) of the
first-integral lemma, followed by (5), now yields
\[
n\cdot K=\Phi_3(p,q)
\tag{10}
\]
for a binary cubic \(\Phi_3\).

Every binary cubic on the right side of (10) can be written
\[
n\cdot M(p,q)
\]
for a constant \(3\times2\) matrix \(M\).  After subtracting it, the same
two syzygy generators show that the remaining quadratic vector is itself a
constant linear combination of \(p,q\), which can be absorbed into \(M\).
Thus
\[
H_2=\operatorname{Ver}(\ell,m)+M(p,q).
\tag{11}
\]
Combining (1), (8), and (11) proves (3).

## 5. Degree six excludes the normal form

Let \(R\) be the \(2\times3\) matrix whose rows are \(d\ell\) and \(dm\),
put
\[
P=p+\ell,\qquad Q=q+m,\qquad A=L_0-MR,
\]
and define
\[
\Phi(s,t)=\operatorname{Ver}(s,t)+M(s,t).
\]
The normal form (3) rewrites the entire map exactly as
\[
F=AX+\Phi(P,Q).
\tag{12}
\]

Set
\[
b_1=\Phi_s(P,Q),\quad b_2=\Phi_t(P,Q),\qquad
k_1=\nabla P,\quad k_2=\nabla Q.
\]
Then
\[
JF=A+b_1k_1^T+b_2k_2^T.
\]
Multilinearity of the determinant, or rank-two Cauchy--Binet, gives for
every constant \(A\), without any invertibility hypothesis,
\[
\begin{aligned}
\det JF={}&\det A
+k_1^T\operatorname{adj}(A)b_1
+k_2^T\operatorname{adj}(A)b_2\\
&+\bigl(b_1\times b_2\bigr)\cdot
A\bigl(k_1\times k_2\bigr).
\end{aligned}
\tag{13}
\]
The two adjugate terms have degree at most three.  The degree-two part of
\(k_1\times k_2\) is \(D=\nabla p\times\nabla q\), while the degree-four
part of \(b_1\times b_2\) is \(2n\).  Hence the degree-six Keller identity
is
\[
n^TAD=0.
\tag{14}
\]

For the rows of \(A\), choose linear forms \(h_i\) with
\(\nabla h_i^T\) equal to row \(i\), and write
\[
\delta(h)=D\cdot\nabla h,\qquad
f_i=\delta(h_i),\qquad
W=\delta\bigl((\mathbb C^3)^*\bigr),\qquad
U=\langle p,q\rangle.
\]
Equation (14) is
\[
q^2f_1-2pqf_2+p^2f_3=0.
\tag{15}
\]
Since \(p,q\) are coprime and all \(f_i\) are quadratic, the syzygies of
\((q^2,-2pq,p^2)\) give constants \(c,d\) such that
\[
f_1=cp,\qquad
f_2=\frac{cq+dp}{2},\qquad
f_3=dq.
\tag{16}
\]
If \(\delta\) is injective, (16) has only two possibilities: either
\(A=0\), or \(U\subseteq W\).

It remains to check that the second possibility never occurs.  Section 2
provides a nonsingular pencil member; call it \(q\).  The operator
\[
T=q^{-1}p
\]
is self-adjoint for the nondegenerate symmetric form \(q\).  A repeated
diagonal eigenspace, or a size-two plus size-one decomposition with one
eigenvalue, makes \(p-\lambda q\) rank one; the scalar case makes \(p,q\)
proportional.  Thus the absence of a double line leaves exactly three
self-adjoint Jordan types.  Standard Jordan-chain normalization over
\(\mathbb C\), together with a pencil change, gives:

1. Three distinct eigenvalues:
   \[
   q=X^2+Y^2+Z^2,\qquad
   p=aX^2+bY^2+cZ^2,\qquad a,b,c\ \text{distinct}.
   \]
   Here
   \[
   W=\langle YZ,XZ,XY\rangle,\qquad W\cap U=0.
   \]
2. One size-two block and one distinct eigenvalue:
   \[
   q=2XY+Z^2,\qquad p=Y^2+Z^2.
   \]
   Here
   \[
   D=4\bigl(Z(Y-X),YZ,-Y^2\bigr),\qquad
   W=\langle XZ,YZ,Y^2\rangle,\qquad W\cap U=0.
   \]
3. One size-three block:
   \[
   q=2XZ+Y^2,\qquad p=2YZ.
   \]
   Here
   \[
   D=4\bigl(XZ-Y^2,YZ,-Z^2\bigr),\qquad
   W=\langle XZ-Y^2,YZ,Z^2\rangle,\qquad
   W\cap U=\langle p\rangle.
   \]

In every case the three components of \(D\) are linearly independent, so
\(\delta\) is injective, while \(U\nsubseteq W\).  Equations (15)--(16)
therefore force \(A=0\).  But then (12) factors through the two functions
\((P,Q)\), so \(JF\) has rank at most two everywhere, contradicting the
Keller condition.  This proves the no-double-line exclusion.

## 6. Sharpness of the degree-eight exception

Take
\[
p=X_1^2,\qquad q=X_2^2+X_3^2,\qquad
H_3=(0,0,X_1^3).
\]
The pencil has the unique double line \(p=X_1^2\), and
\[
n\cdot H_3=X_1^7\ne0
\]
satisfies (7).  Thus the no-double-line hypothesis cannot be removed from
the tangency conclusion.  This is a leading-identity example, not a Keller
map.
