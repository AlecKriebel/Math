# The nonzero-\(A\) rank-one triple-companion branch

**Status (2026-07-25 UTC).**  Exact theorem-level exclusion, independently
reconstructed in PARI/GP.  This note covers only the \(A\ne0\) branch of the
rank-one fixed-divisor \(e=2\) triple companion.  It does not by itself claim
the full rank-one theorem.

## Statement

Put
\[
 q=y^2+xz,\qquad
 H_4=(x^4,x^2q,0),\qquad R=x^3 .
\]
After the legal top-degree gauges, the \(A\ne0\) branch has
\[
\begin{aligned}
 W&=w_1xy+w_2xz+w_3y^2,\\
 U&=Axq+\frac43xW,\\
 V&=C_0x^2z+C_1xy^2+C_2xyz+C_3xz^2\\
   &\quad+\frac{w_1(3A-4w_3)}{9A}y^3
       +\frac{(w_2-w_3)(3A-4w_3)}{9A}y^2z .
\end{aligned}
\]
There are no quadratic first and second coordinates and no linear part
\(L\) for which
\[
 F=H_4+(U,V,R)+(H_{2,1},H_{2,2},W)+L
\]
has nonzero constant Jacobian determinant.

Since the constant term of \(\det JF\) is \(\det L\), it is enough below to
obtain either a literal contradiction or \(\det L=0\).

## Normalizing \(A\)

No root extraction is needed.  For \(A\ne0\), replace \(F\) by
\[
 G(X)=\operatorname{diag}(A^{-4},A^{-4},A^{-3})F(AX).
\]
This fixes \(H_4\) and \(R=x^3\), sends \(Axq\) to \(xq\), and divides every
other coefficient in \(U,V,W\) by \(A\).  Also
\[
 \det JG=A^{-8}\det JF,
\]
so the Keller property is unchanged.  We therefore set \(A=1\).

Write \(w=w_1\), \(v=w_2\), and \(s=w_3\).  We use zero-based coefficient
labels
\[
 (a_0,\ldots,a_5),\ (b_0,\ldots,b_5)
\]
for the monomial order
\[
 (x^2,xy,xz,y^2,yz,z^2)
\]
in the first two quadratic coordinates.  Write \(L=(\ell_{ij})\).

After solving the constant-pivot \(E_6\) system, the \(y^5\)-coefficient of
the degree-five Jacobian identity is
\[
 \frac{2}{27}s(v-s)(4s-3)(4s+3).                 \tag{1}
\]
Thus four closed branches cover the entire parameter space:
\[
 s=0,\qquad v=s,\qquad s=\frac34,\qquad s=-\frac34.
\]

## 1. The branch \(s=0\)

Polynomial left syzygies of \(E_5\) give \(v^2=0\), hence \(v=0\).  After
this fresh specialization they give
\[
 wC_3=0.                                         \tag{2}
\]

If \(w=0\), then \(W=0\).  This leaf is uniform in all four \(C_i\); no
localization by \(C_3\), \(C_2\), or \(C_0-C_1\) is needed.  After \(E_6\),
three literal \(E_5\)-coefficients are
\[
 -2\ell_{33},\qquad X+\ell_{32},\qquad -2X+\ell_{32},
 \quad
 X=3C_1C_2-3C_2a_3-3b_4.
\]
Consequently \(\ell_{32}=\ell_{33}=0\).  The third coordinate is
\[
 F_3=x^3+\ell_{31}x+\text{constant},
\]
and therefore
\[
 \det JF=(3x^2+\ell_{31})
 \det\begin{pmatrix}
 \partial_yF_1&\partial_zF_1\\
 \partial_yF_2&\partial_zF_2
 \end{pmatrix}.
\]
The nonunit \(3x^2+\ell_{31}\) cannot divide a nonzero constant.

It remains to take \(w\ne0\), so (2) gives \(C_3=0\).  A fresh \(E_5\)
solve followed by two literal \(E_4\)-coefficients gives
\[
 [y^4]E_4=\frac{w^2(w-6C_2)}3,\qquad
 [x^2z^2]E_4=-\frac{w(2w-3C_2)(w-C_2)}3.
\]
The first sets \(C_2=w/6\), while the second becomes
\[
 -\frac5{12}w^3\ne0.
\]

## 2. The equal branch \(v=s\)

Assume first \(s\ne0,3/4\); the omitted values belong respectively to the
previous and plus branches.  Polynomial \(E_5\) compatibilities give
\[
 C_3s(4s-3)=0,\qquad
 s(4s-3)(6C_2+4sw-w)=0.
\]
After substituting the forced values, a remaining compatibility is
\[
 s\,w(4s-3)(4s+3)=0.                             \tag{3}
\]
The value \(s=-3/4\) is the minus branch.  Away from both resonances,
(3) gives \(w=0\), and then \(C_2=C_3=0\).

Let \(D=C_0-C_1\).  If \(D\ne0\), the recomputed \(E_5\) system gives
\[
 \ell_{32}=0,\qquad \ell_{33}=sD.
\]
The \(E_4\)-coefficients
\[
 [x^3z]E_4=\frac{s(4s-3)}3\ell_{12},
 \qquad
 [x^4]E_4\big|_{\ell_{12}=0}=-3\ell_{22}
\]
give \(\ell_{12}=\ell_{22}=0\), and hence \(\det L=0\).

At the fresh rank drop \(D=0\), \(E_5\) gives
\(\ell_{32}=\ell_{33}=0\), while
\[
 [x^3z]E_4=\frac{s(4s-3)}3\ell_{12},\qquad
 [x^2yz]E_4=-\frac{2s(4s-3)}3\ell_{13}.
\]
Thus \(\ell_{12}=\ell_{13}=0\), again making \(\det L=0\).

## 3. The plus branch \(s=3/4\)

An \(E_5\) compatibility is
\[
 -\frac1{12}(4v-3)^2,
\]
so \(v=3/4\).  On this diagonal, the remaining compatibilities include
\[
 wC_3,\qquad w(3C_2+w).
\]
If \(w\ne0\), then \(C_3=0\), \(C_2=-w/3\), and a fresh \(E_4\)
coefficient is
\[
 [y^3z]E_4=-\frac12w^2,
\]
a contradiction.

Take \(w=0\).  On the \(C_3\ne0\) chart, the recomputed \(E_4\) identity
contains
\[
 [yz^3]E_4=3C_3^2.
\]
At \(C_3=0,C_2\ne0\), a fresh solve contains
\[
 [y^3z]E_4=\frac32C_2^2.
\]
It remains only to treat \(C_2=C_3=0\).

### Plus aligned, \(D=C_0-C_1\ne0\)

Put \(C_1=C\), and set
\[
 t=\ell_{32},\qquad r=\ell_{33},\qquad
 h=b_2-b_3-\ell_{13}.
\]
The \(E_5\) solution is polynomial after localizing only by \(D\):
\[
\begin{gathered}
 a_1=\frac43t,\quad
 a_2=C+D-\frac hD+\frac43r,\quad
 a_3=C-\frac hD,\quad a_4=a_5=0,\\
 b_1=\ell_{12},\quad b_2=b_3+\ell_{13}+h,\quad
 b_4=b_5=0.
\end{gathered}
\]
Define
\[
\begin{aligned}
 P&=-3CD-3D^2+4Dr+6h,\\
 Q&=-3CD+6D^2-8Dr+6h,\\
 H&=-CD+2h.
\end{aligned}
\]
Four exact \(E_4\)-coefficients are
\[
 -\frac{tP}{3D},\qquad -\frac{tQ}{3D},\qquad
 -\frac{(3D-4r)P}{6D},\qquad
 -\frac{(3D-4r)H}{2D}.                           \tag{4}
\]
Moreover
\[
 P-Q=3D(4r-3D).
\]
If \(t\ne0\), the first two equations in (4) give \(r=3D/4\).  If
\(t=0\) but \(r\ne3D/4\), the last two give \(P=H=0\); substituting
\(H=0\) into \(P\) gives \(D(4r-3D)=0\), a contradiction.  Hence always
\[
 r=\frac34D,
\]
and (4) reduces to \(tH=0\).

The remaining two \(E_4\)-equations solve
\[
\begin{aligned}
 \ell_{22}&=\frac{t(-6a_0+4\ell_{31})}{9}
              +\frac{h\ell_{12}}D,\\
 \ell_{23}&=Db_3-Ch+\frac{h^2+h\ell_{13}}D+\frac{2t^2}{9}.
\end{aligned}
\]
If \(t\ne0\), then \(H=0\), but
\[
 [xyz]E_3=-\frac23t^2,
\]
a contradiction.

If \(t=0\), the exact determinant has a factor \(\ell_{12}\).  Thus
\(\ell_{12}=0\) is already singular.  If \(\ell_{12}\ne0\), then
\[
 [x^2z]E_3=\frac{3\ell_{12}H}{4D}
\]
forces \(H=0\).  The \(x^3\)-equation in \(E_3\) solves \(a_0\), the
\(xz\)-equation in \(E_2\) forces \(\ell_{13}=h\), and then
\[
 [xy]E_2=-\frac34\ell_{12}^2,
\]
a contradiction.

### Plus aligned, \(D=0\)

This chart is recomputed without a \(D\)-pivot.  Put
\(\alpha=C-2a_3\).  Four \(E_4\)-coefficients are
\[
 -\frac{t(3\alpha+4r)}3,\quad
 -\frac{t(3\alpha-8r)}3,\quad
 \frac{2r(3\alpha+4r)}3,\quad
 2r\alpha.                                       \tag{5}
\]
If \(r\ne0\), the last equation gives \(\alpha=0\), and the third then
gives \(r=0\), impossible.  Thus \(r=0\), and (5) reduces to
\(t\alpha=0\).  The other two equations give
\[
\ell_{22}=(C-a_3)\ell_{12}
          +\frac{t(-6a_0+4\ell_{31})}{9},
\qquad
\ell_{23}=(C-a_3)\ell_{13}+\frac{2t^2}{9}.
\]
For \(t=0\), the last two columns of \(L\) are proportional and
\(\det L=0\).  For \(t\ne0\), \(\alpha=0\), while
\([xyz]E_3=-2t^2/3\).

## 4. The minus branch \(s=-3/4\)

Polynomial \(E_5\) compatibilities include
\[
 9C_2=w(4v+9),\qquad
 72C_3=16v^2+72v+45.
\]
After these substitutions, a remaining compatibility is
\[
 \frac5{144}(4v+3)^3.
\]
Hence
\[
 v=-\frac34,\qquad C_2=\frac23w,\qquad C_3=0.
\]
This is exactly the equal-minus intersection.

For \(w\ne0\), recompute first with \(D\ne0\) and then at the fresh
rank drop \(D=0\).  In both charts two \(E_4\)-coefficients have the
literal difference
\[
 [x^2yz]E_4-[xy^3]E_4=\frac{10}{81}w^4,
\]
a contradiction.

For \(w=0,D\ne0\), \(E_5\) gives
\[
 \ell_{32}=0,\qquad \ell_{33}=-\frac34D.
\]
Then
\[
 [x^3z]E_4=\frac32\ell_{12},\qquad
 [x^4]E_4\big|_{\ell_{12}=0}=-3\ell_{22},
\]
so \(\det L=0\).

At \(w=0,D=0\), the fresh \(E_5\) system gives
\(\ell_{32}=\ell_{33}=0\), and
\[
 [x^3z]E_4=\frac32\ell_{12},\qquad
 [x^2yz]E_4=-3\ell_{13}.
\]
Again \(\det L=0\).

## Coverage

Equation (1) is a closed four-set cover.  The intersection \(s=v=0\)
is included in the uniform \(W=0\) computation.  The equal branch's two
exceptional values are treated from scratch in the plus and minus
sections.  Each plus/minus branch itself forces \(v=s\), so there is no
unexamined off-diagonal resonance.  Every divisor used in a pivot
(\(w\), \(C_3\), \(C_2\), or \(D\)) has its zero locus recomputed as a
fresh system.

This proves the statement.

## Disclosure

This result was developed with AI assistance.  It is not peer reviewed.
The exact PARI/GP checks are evidence about the encoded algebra, not peer
review or a substitute for independent mathematical scrutiny.
