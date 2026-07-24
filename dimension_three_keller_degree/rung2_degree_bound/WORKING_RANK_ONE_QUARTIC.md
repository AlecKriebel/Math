# Working theorems: rank-one quartic Jacobian part

**Status:** complete proof under the stated hypotheses and independently
adversarially audited.  This is not peer reviewed, and the completed
source-specific priority search is not a guarantee of worldwide priority.

**Recorded:** 2026-07-24T23:31:14Z.

## 1. The theorem

Let
\[
F=X+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow\mathbb A^3_{\mathbb C},
\]
where \(H_i\) is homogeneous of degree \(i\).  Suppose
\[
\det JF=1,\qquad \operatorname{rank}JH_4\le1
\]
over \(\mathbb C(X_1,X_2,X_3)\).

### Theorem

The matrices \(JH_3\) and \(JH_4\) are simultaneously strictly triangular
after a linear conjugation.  Consequently \(F\) is a polynomial
automorphism.

The result concerns the mixed cubic--quartic map itself.  It is stronger
than applying the known homogeneous theorem to either summand separately.

## 2. Homogeneous determinant identities

For the more general normalization
\[
F=X+H_2+H_3+H_4,
\]
put
\[
A=JH_2,\qquad B=JH_3,\qquad C=JH_4.
\]
Define
\[
e_2(M)=\frac{(\operatorname{tr}M)^2-\operatorname{tr}(M^2)}2,
\qquad
s(M,N)=\operatorname{tr}M\operatorname{tr}N-\operatorname{tr}(MN),
\]
and let \(\Delta\) be the symmetric trilinear polarization of determinant,
normalized by \(\Delta(M,M,M)=\det M\).

The homogeneous degrees \(1,\ldots,9\) in
\(\det(I+A+B+C)-1\) are:
\[
\begin{array}{rcl}
1&:&\operatorname{tr}A=0,\\
2&:&\operatorname{tr}B+e_2(A)=0,\\
3&:&\operatorname{tr}C+s(A,B)+\det A=0,\\
4&:&e_2(B)+s(A,C)+3\Delta(A,A,B)=0,\\
5&:&s(B,C)+3\Delta(A,A,C)+3\Delta(A,B,B)=0,\\
6&:&e_2(C)+\det B+6\Delta(A,B,C)=0,\\
7&:&3\Delta(A,C,C)+3\Delta(B,B,C)=0,\\
8&:&3\Delta(B,C,C)=0,\\
9&:&\det C=0.
\end{array}
\tag{1}
\]
These follow directly from
\[
\det(I+M)=1+\operatorname{tr}M+e_2(M)+\det M
\]
and polarization.  No Jacobian-Conjecture hypothesis is used.

## 3. A nilpotent matrix pencil

Set \(A=0\).  Equations (1) give
\[
\begin{gathered}
\operatorname{tr}B=\operatorname{tr}C=0,\qquad
e_2(B)=s(B,C)=0,\\
e_2(C)+\det B=0,\qquad
\operatorname{tr}(\operatorname{adj}B\,C)=0,\qquad
\operatorname{tr}(\operatorname{adj}C\,B)=0,\qquad
\det C=0.
\end{gathered}
\tag{2}
\]
Since \(\operatorname{rank}C\le1\),
\[
e_2(C)=\operatorname{adj}C=\det C=0.
\]
Therefore
\[
\det B=0,
\]
and \(B\) is nilpotent.  For every scalar \(t\), (2) yields
\[
\operatorname{tr}(B+tC)
=e_2(B+tC)
=\det(B+tC)
=0.
\]
Hence the entire pencil
\[
\boxed{B+tC\text{ is nilpotent for every }t.}
\tag{3}
\]

Rank at most one and common homogeneity imply
\[
H_4=a\,h,\qquad
C=a\,v^T,\qquad v=\nabla h,\qquad v^Ta=0
\tag{4}
\]
for a constant vector \(a\) and a quartic form \(h\).

## 4. Triangularizing the cubic part

The homogeneous dimension-three theorem of de Bondt and van den Essen
states that a homogeneous map \(H:\mathbb C^3\to\mathbb C^3\) with
nilpotent \(JH\) is linearly triangularizable.  See:

M. de Bondt and A. van den Essen,
*The Jacobian Conjecture: linear triangularization for homogeneous
polynomial maps in dimension three*, J. Algebra 294 (2005), 294--306,
DOI 10.1016/j.jalgebra.2005.04.018.

Apply it to \(H_3\).  In suitable coordinates,
\[
B=
\begin{pmatrix}
0&0&0\\
p&0&0\\
q&r&0
\end{pmatrix}.
\tag{5}
\]

### Rank \(B=2\)

Here \(pr\ne0\) in the function field.  The characteristic polynomial of
the rank-one perturbation \(B+tav^T\), together with (3), gives
\[
v^Ta=v^TBa=v^TB^2a=0.
\tag{6}
\]
For \(a=(a_1,a_2,a_3)^T\), direct calculation from (5) gives
\[
\det[a,Ba,B^2a]=a_1^3p^2r.
\tag{7}
\]
If \(C=0\), the already triangular \(B\) finishes the proof.  Otherwise
\(v\ne0\), so (6)--(7) force \(a_1=0\).

If \(a_2=0\), (6) gives \(v_3=0\).  If \(a_2\ne0\), first
\(v^TBa=0\) gives \(v_3=0\), and then \(v^Ta=0\) gives \(v_2=0\).
In both cases \(C=av^T\) is strictly lower triangular in the same basis as
\(B\).

### Rank \(B\le1\)

If \(B=0\), then \(F=X+ah\) with \(D_a h=0\), a triangular shear.  Assume
from now on that \(\operatorname{rank}B=1\).

Common homogeneity now gives
\[
H_3=b\,g,\qquad B=b\,u^T,\qquad u=\nabla g,\qquad u^Tb=0.
\tag{8}
\]
Equation \(s(B,C)=0\), with both traces zero, becomes
\[
\operatorname{tr}(BC)
=(u^Ta)(v^Tb)=0.
\tag{9}
\]

If \(a,b\) are dependent, (4), (8) give a common shear direction and an
immediate triangular flag.  Suppose they are independent.

- If \(u^Ta=0\), the flag
  \[
  0\subset\langle a\rangle\subset\langle a,b\rangle
  \subset\mathbb C^3
  \]
  is common: both matrices kill \(a\), both carry
  \(\langle a,b\rangle\) into \(\langle a\rangle\), and both carry the
  whole space into \(\langle a,b\rangle\).
- If \(v^Tb=0\), the same statement holds for
  \(0\subset\langle b\rangle\subset\langle a,b\rangle\).

Thus \(B,C\) are simultaneously strictly triangular in every case.
\(\square\)

## 5. An invariant-image-line extension with \(H_2\ne0\)

Return to
\[
F=X+H_2+H_3+H_4,\qquad H_4=a\,h.
\]
The image line of \(JH_4\) is the constant line \(\mathbb C a\).

### Proposition

If
\[
A a\in\mathbb C[X]a,\qquad B a\in\mathbb C[X]a,
\tag{10}
\]
then \(F\) is a polynomial automorphism.

### Proof

Choose coordinates with \(a=e_3\), and write
\[
A e_3=\alpha e_3,\qquad B e_3=\beta e_3,
\]
where \(\alpha,\beta\) are homogeneous of degrees \(1,2\).  The first two
components of \(H_2,H_3\) are independent of \(X_3\), and
\[
JF=
\begin{pmatrix}
I_2+\bar A+\bar B&0\\
*&1+\alpha+\beta+v_3
\end{pmatrix}.
\]
The Keller identity factors as
\[
1=\det(I_2+\bar A+\bar B)(1+\alpha+\beta+v_3).
\tag{11}
\]
Both factors are units in \(\mathbb C[X]\), hence constants.  Their constant
terms are \(1\), and comparison of homogeneous degrees gives
\[
\alpha=\beta=v_3=0,\qquad \det(I_2+\bar A+\bar B)=1.
\tag{12}
\]
Thus every nonlinear component is independent of \(X_3\), and
\[
F(X_1,X_2,X_3)=
\bigl(G(X_1,X_2),\,X_3+\phi(X_1,X_2)\bigr),
\]
where \(G:\mathbb A^2\to\mathbb A^2\) is a Keller map of degree at most
\(3\).  The established plane low-degree theorem makes \(G\) an
automorphism, so the displayed triangular extension is an automorphism.
\(\square\)

This proposition uses a plane result only as an established input; it makes
no conditional appeal to the plane Jacobian Conjecture.

## 6. Exact obstruction to global simultaneous triangularization

The nine determinant identities do not force \(A,B,C\) to be simultaneously
triangularizable.  The explicit automorphism
\[
F(X_1,X_2,X_3)=
\left(X_1+X_2^2,\,
X_2+(X_1+X_2^2)^2,\,
X_3\right)
\tag{13}
\]
is a composition of two shears and has homogeneous pieces
\[
H_2=(X_2^2,X_1^2,0),\quad
H_3=(0,2X_1X_2^2,0),\quad
H_4=(0,X_2^4,0).
\]
Here \(\operatorname{rank}C=1\), but the \(X_1\)- and \(X_2\)-coefficient
matrices of
\[
A=
\begin{pmatrix}
0&2X_2&0\\
2X_1&0&0\\
0&0&0
\end{pmatrix}
\]
are \(2E_{21}\) and \(2E_{12}\).  Their only common invariant line in
\(\mathbb C^3\) is \(\mathbb C e_3\), and there is no common invariant
two-plane containing it: on
\(\mathbb C^3/\mathbb C e_3\) they generate the irreducible two-dimensional
matrix action.  Hence no constant linear conjugacy simultaneously
triangularizes \(A,B,C\).

This example blocks the tempting route “rank-one \(C\) plus the nine
identities implies a common flag.”  A valid extension of the theorem must use
additional information, such as the invariant-image-line condition (10).

## 7. Scope and next obstruction

The two proved exclusions are:
\[
H_2=0,\quad \operatorname{rank}JH_4\le1,
\]
and
\[
\operatorname{rank}JH_4\le1,\quad
\mathbb C a\text{ invariant under }JH_2,JH_3.
\]
It does **not** exclude:

- a nonzero quadratic homogeneous part violating (10);
- generic rank \(JH_4=2\);
- total-degree-four maps whose homogeneous pieces cannot be separated by
  a linear normalization.

The automorphism (13) shows that the remaining \(A=JH_2\) terms cannot be
handled by simultaneous triangularization alone.
