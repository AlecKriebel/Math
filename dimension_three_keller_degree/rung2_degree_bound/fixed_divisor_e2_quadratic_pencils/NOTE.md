# Two mixed-companion exits in the fixed-divisor \(e=2\) row

## Status

**Audited theorem.**  The exact SymPy certificate and a
methodologically independent PARI/GP reconstruction both pass, together
with fail-closed injection tests.

This note is not peer reviewed.  The exact checks certify the algebra encoded
in the accompanying scripts; they are evidence, not peer review.  AI systems
assisted with the symbolic exploration, case organization, proof drafting,
and verification code.  Every asserted identity below is intended to have an
exact, fail-closed certificate.

## Theorem

Let \(K\) be a field of characteristic zero.  Write a degree-four polynomial
map, after translating away its constant term, as
\[
F=LX+H_2+H_3+H_4,
\]
where \(H_j\) is homogeneous of degree \(j\).  Suppose that, after linear
source and target changes, its leading form and the third component of
\(H_3\) are one of
\[
\begin{array}{c|c}
H_4&R=(H_3)_3\\ \hline
(x^4,x^2yz,0)&xyz,\\[2mm]
\bigl(x^4,x^2(y^2+xz),0\bigr)&x(y^2+xz).
\end{array}
\tag{1}
\]
Then \(\det JF\) cannot be a nonzero constant.

Equivalently, the mixed cubic companion \(R=xq\) is excluded for both
canonical all-vertical fixed-divisor pencils
\[
H_4=(p^2,pq,0),\qquad
\langle p,q\rangle=\langle x^2,yz\rangle
\quad\hbox{or}\quad
\langle x^2,y^2+xz\rangle .
\tag{2}
\]

The theorem concerns the separate fixed-divisor row \(e=2\).  It is not an
assertion about the genuine \(e=0\) line-\((2,2)\) outer-cover packages.

## Weighted Jacobian identities

Introduce a bookkeeping parameter \(s\) and put
\[
\mathcal J(s)=
L+sJH_2+s^2JH_3+s^3JH_4.
\]
Write \(E_j=[s^j]\det\mathcal J(s)\).  The Keller condition says
\[
E_1=\cdots=E_9=0,\qquad \det L\ne0.
\tag{3}
\]
The top equation \(E_7=0\) is linear in the two unspecified cubic
components and the quadratic third component.  All quadratic first and
second components remain arbitrary throughout the proof.

## 1. The rank-two pencil

Take
\[
p=x^2,\qquad q=yz,\qquad
H_4=(p^2,pq,0),\qquad R=xq.
\]
The raw \(E_7\) matrix has size \(36\times26\), rank \(14\), and nullity
\(12\).  Five kernel directions are legal gauges: two target shears by
\(R\), and the three source-translation directions.  The other seven
directions give the complete normal form
\[
\begin{aligned}
U&=4Cx^2y+4Dx^2z,\\
V&=Ax^3+Cy^2z+Dyz^2+w_3xy^2+w_5xz^2,\\
W&=w_0x^2+w_3y^2+w_4yz+w_5z^2,
\end{aligned}
\tag{4}
\]
where \(H_3=(U,V,R)\) and \((H_2)_3=W\).

The exact left kernel of the \(E_6\) coefficient matrix gives precisely the
two nonzero compatibility equations
\[
Cw_3=0,\qquad Dw_5=0.
\tag{5}
\]
If \(C\ne0,D=0\), substitute \(w_3=0\); a polynomial left syzygy of the
\(E_5\) matrix has value \(-12C^3\), a contradiction.  If \(CD\ne0\),
substitute \(w_3=w_5=0\); the same calculation again gives
\(-12C^3=0\).  The involution \(y\leftrightarrow z\) preserves
\(p,q,R\) and interchanges the \(C\)- and \(D\)-only branches.  Hence
\[
C=D=0.
\tag{6}
\]

On (6), the complete \(E_6\) solve includes
\[
\begin{gathered}
a_1=a_2=a_3=a_5=0,\qquad
b_1=\ell_{32},\quad b_2=\ell_{33},\\
b_3=-w_3w_4,\qquad b_5=-w_4w_5,
\end{gathered}
\tag{7}
\]
using \(L=(\ell_{ij})\).  Four literal coefficients of \(E_5\) are
\[
\begin{array}{c|c}
x^4y&4(\ell_{22}+w_4\ell_{32})\\
x^4z&-4(\ell_{23}+w_4\ell_{33})\\
x^2y^2z&-\ell_{12}\\
x^2yz^2&\ell_{13}.
\end{array}
\tag{8}
\]
Thus the last two entries of the first row vanish and the last two entries
of the second row are \(-w_4\) times those of the third row.  Therefore
\(\det L=0\), contradicting (3).

## 2. The rank-one pencil

Now take
\[
p=x^2,\qquad q=y^2+xz,\qquad
H_4=(p^2,pq,0),\qquad R=xq.
\]
Again the raw \(E_7\) matrix has rank \(14\) and nullity \(12\), with the
same five-dimensional legal gauge space.  A complete seven-parameter
normal complement is
\[
\begin{aligned}
U={}&4Cx^2y+4Dx^2z,\\
V={}&Cyq+Dzq+(w_2-w_3)x^2z+w_4xyz+w_5xz^2,\\
W={}&w_0x^2+w_2xz+w_3y^2+w_4yz+w_5z^2.
\end{aligned}
\tag{9}
\]
The exact \(E_6\) compatibility ideal is
\[
Dw_5=0,\qquad Cw_5+Dw_4=0.
\tag{10}
\]

If \(D\ne0\), equations (10) give \(w_4=w_5=0\).  A polynomial
left syzygy of \(E_5\) then has value \(24D^3\), impossible.

If \(D=0,C\ne0\), equations (10) give \(w_5=0\).  Two
cross-multiplied polynomial left syzygies of \(E_5\) give
\[
\begin{aligned}
f&=C^3+2C^2w_4-2Cw_4^2+w_4^3=0,\\
g&=(C+2w_4)(w_4^2-3C^2)=0.
\end{aligned}
\tag{11}
\]
Their exact resultant is
\[
\operatorname{Res}_{w_4}(f,g)=-250C^9,
\tag{12}
\]
again impossible.  Hence \(C=D=0\).

It remains to show that this closed normal stratum forces
\(\det L=0\).  The \(E_5\) system has four exhaustive charts.

- If \(w_4\ne0\), a rank-six minor is \(768w_4^2\).
- If \(w_4=0,w_5\ne0\), a rank-six minor is \(-4096w_5^2\).

In either chart the complete solve gives
\[
\ell_{12}=\ell_{13}=0,\qquad
\ell_{22}=-w_3\ell_{32},\qquad
\ell_{23}=-w_3\ell_{33},
\tag{13}
\]
so \(\det L=0\).

On \(w_4=w_5=0\), put \(d=w_2-w_3\).  If \(d=0\), a constant
rank-four minor of \(E_5\) is \(64\), and (13) again follows.  Suppose
\(d\ne0\).  A rank-four \(E_5\) minor is \(-64d^2\), and the complete
solve puts
\[
L=
\begin{pmatrix}
\ell_{11}&0&\ell_{13}\\
\ell_{21}&-w_3\ell_{32}&\ell_{23}\\
\ell_{31}&\ell_{32}&\ell_{33}
\end{pmatrix}.
\tag{14}
\]
Set \(M=\ell_{23}+w_3\ell_{33}\).  Two literal coefficients of \(E_4\)
are
\[
[x^4]E_4=-\frac4d\,\ell_{32}M,\qquad
[x^3z]E_4=\frac1d\,\ell_{13}\ell_{32}.
\tag{15}
\]
But
\[
\det L
=-\ell_{32}\bigl(
\ell_{11}M-\ell_{13}(\ell_{21}+w_3\ell_{31})
\bigr).
\tag{16}
\]
Both products on the right vanish by (15), so \(\det L=0\).  This
contradicts (3) and completes the proof.

## What this does and does not close

The mixed companion \(R=xq\) is now excluded for the two canonical
fixed-divisor \(e=2\) pencils.  The triple
companion \(R=xp=x^3\) remains a separate lower-identity problem for each
pencil.  Consequently this note does not yet close the full
fixed-divisor \(e=2\) row and does not change the current universal
total-degree lower bound by itself.
