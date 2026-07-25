# Exclusion of both marked-critical mixed-companion orbits

**Status:** exact working theorem; independent hostile audit passed at
2026-07-25T08:38:00Z.  This work is not peer reviewed.

**First recorded:** 2026-07-25T08:18:00Z.

## 1. Statement

Let
\[
F=LX+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have total degree four.  Put
\[
p=x^2,\qquad q=y^2+xz,\qquad H_4=(p^2,q^2,0).           \tag{1}
\]
The outer critical pair in (1) contains the unique double-line value
\(p=0\).  There are three companion orbits relative to this marked pair:
triple at the marked value, mixed at the other critical value, and mixed
distinct from both.

### Provisional theorem

Neither mixed orbit can occur for a Keller map:
\[
(H_3)_3=xq
\quad\text{or}\quad
(H_3)_3=x(p-q).                                        \tag{2}
\]

The triple marked orbit \((H_3)_3=x^3\) is not included.

## 2. Complete raw kernels and legal gauges

Write \(P=p^2,Q=q^2,R=(H_3)_3\), and
\[
U=(H_3)_1,\qquad V=(H_3)_2,\qquad W=(H_2)_3.
\]
For either value of \(R\) in (2), the raw degree-seven identity
\[
\operatorname{Jac}(P,Q,W)+\operatorname{Jac}(P,V,R)
 +\operatorname{Jac}(U,Q,R)=0                          \tag{3}
\]
has exact rank \(18\) and nullity \(8\).  In a common monomial order, the
same maximal minor works in both cases:
\[
-5343626510991360.                                     \tag{4}
\]

For \(R=xq\), eight independent kernel directions are the two target
shears
\[
(R,0,0),\qquad(0,R,0),
\]
the three source-translation jets, and
\[
(0,x^3,0),\qquad(0,2zq,xz),\qquad(0,-2zq,y^2).         \tag{5}
\]
Their coefficient matrix has minor \(32\).

For \(R=x(p-q)\), use the same two target shears and three translation
jets, together with
\[
(0,0,p),\qquad(0,-2zq,xz),\qquad(0,2zq,y^2).           \tag{6}
\]
Their coefficient matrix has minor \(64\).

The nullity and independence minors prove completeness.  Removing the
five legal affine/target directions gives the division-free normal forms
\[
\begin{array}{c|c|c}
R&(U,V)&W\\ \hline
xq&
\bigl(0,A x^3+2(w_2-w_3)zq\bigr)&
w_2xz+w_3y^2\\[2mm]
x(p-q)&
\bigl(0,2(w_3-w_2)zq\bigr)&
w_0p+w_2xz+w_3y^2.
\end{array}                                             \tag{7}
\]

## 3. Complete degree-six solves

Let \(d=w_2-w_3\).  Expand the first two components of \(H_2\) in the
ordered basis
\[
p,\ xy,\ xz,\ y^2,\ yz,\ z^2
\]
with coefficients \(a_0,\ldots,a_5\) and
\(b_0,\ldots,b_5\).  Write \(L=(\ell_{ij})\).

In each case the complete \(E_6\) system has rank \(10\) in
\[
a_1,\ldots,a_5,\quad b_1,\ldots,b_5,\quad
\ell_{32},\ell_{33}.
\]
Parameter-free maximal minors are
\[
-100663296\quad(R=xq),\qquad
2717908992\quad(R=x(p-q)).                              \tag{8}
\]
Exact row reduction gives
\[
\begin{gathered}
a_1=0,\quad a_2=a_3,\quad a_4=a_5=0,\\
b_1=0,\quad b_2=b_3,\quad b_4=0,\quad b_5=d^2,\\
\ell_{32}=0,\qquad
\ell_{33}=
\begin{cases}
w_3d,&R=xq,\\
-w_3d,&R=x(p-q).
\end{cases}                                             \tag{9}
\end{gathered}
\]
Substitution of (9) kills the full \(E_6\) polynomial in each case.

## 4. Degree-five zero-column exit

After (9), the complete \(E_5\) system on
\[
\ell_{12},\ell_{13},\ell_{22},\ell_{23}
\]
has a constant maximal minor:
\[
256\quad(R=xq),\qquad2304\quad(R=x(p-q)).               \tag{10}
\]
Its exact solution is
\[
\ell_{12}=\ell_{22}=0,\qquad
(\ell_{13},\ell_{23})=
\begin{cases}
d(a_3,b_3),&R=xq,\\
-d(a_3,b_3),&R=x(p-q).
\end{cases}                                             \tag{11}
\]
Together with \(\ell_{32}=0\) from (9), equation (11) makes the second
column of \(L\) identically zero.  Thus \(\det L=0\), contradicting the
Keller condition.

No parameter was divided out, so \(d=0\) is included in both arguments.

## 5. Verification and disclosure

`verify_marked_mixed_sympy.py` reconstructs both raw systems, complete
kernel and gauge ledgers, constant lower minors, exact row reductions,
converses, and zero-column exits from the determinant.  The hostile
PARI/GP audit independently rebuilds both cases, their orbit ledger,
quotient gauges, constant-rank lower systems, \(d=0\) specializations, and
all converses.

The calculation and exposition were developed with AI assistance.  Exact
checks establish facts about the encoded algebra; they are not peer
review.  The hostile audit found no missing orbit, illegal gauge, rank-drop
branch, hidden division, or scope inflation.
