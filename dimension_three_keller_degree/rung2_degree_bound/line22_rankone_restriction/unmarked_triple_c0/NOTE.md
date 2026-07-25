# Exclusion of the unmarked triple-companion orbit

**Status:** exact working theorem; independent hostile audit passed at
2026-07-25T08:32:00Z.  This work is not peer reviewed.

**First recorded:** 2026-07-25T08:02:00Z.

## 1. Statement

Let
\[
F=LX+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have total degree four.  Put
\[
p=x^2,\qquad q=y^2+xz
\]
and suppose
\[
H_4=\bigl((p-q)^2,(p+q)^2,0\bigr),\qquad
(H_3)_3=x^3.                                           \tag{1}
\]
This is the \(c=0\) row in the unmarked-critical family of the
rank-one-restriction unique-double-line pencil.

### Provisional theorem

No Keller map has the leading data (1).

The statement is confined to this joint orbit.  It does not include the
marked-critical rows or the finite \(c^2=9\) resonance.

## 2. Complete degree-seven kernel

Write
\[
P=(p-q)^2,\qquad Q=(p+q)^2,\qquad R=x^3,
\]
\[
U=(H_3)_1,\qquad V=(H_3)_2,\qquad W=(H_2)_3.
\]
The raw degree-seven identity
\[
E_7=\operatorname{Jac}(P,Q,W)
 +\operatorname{Jac}(P,V,R)
 +\operatorname{Jac}(U,Q,R)=0                         \tag{2}
\]
is a \(36\times26\) linear coefficient system.  It has exact rank \(16\);
a fixed maximal minor is
\[
3194799993706229268480.                                \tag{3}
\]

Ten independent kernel directions consist of two target-shear directions,
the three source-translation jets, and five normal directions.  In that
order they are
\[
\begin{gathered}
(x^3,0,0),\quad(0,x^3,0),\\
\partial_y(P,Q,R),\quad\partial_z(P,Q,R),\quad
\partial_x(P,Q,R),                                    \tag{4}\\
\bigl(-z(p-q),z(p+q),0\bigr),\quad(0,0,p),\\
\left(\frac83y(p-q),0,xy\right),\quad
\left(\frac83z(p-q),0,xz\right),\quad
\left(-\frac83z(p-q),0,y^2\right).
\end{gathered}
\]
Their coefficient matrix has minor \(-4096/9\).  Since the nullity of
(2) is \(26-16=10\), the list is complete.

Affine source translation removes the three jets in (4), while target
shears adding the third component to the first two remove the first two
directions.  These operations preserve the Keller condition and only
relabel lower homogeneous pieces.  Hence the complete normal form is
\[
\begin{aligned}
U&=(p-q)\left(\frac83w_1y+
 \left[-S+\frac83(w_2-w_3)\right]z\right),\\
V&=S z(p+q),\\
W&=w_0p+w_1xy+w_2xz+w_3y^2,\\
R&=x^3.                                                \tag{5}
\end{aligned}
\]

## 3. Degree-six compatibility and complete solve

Write the first two components of \(H_2\) in the ordered basis
\[
p,\ xy,\ xz,\ y^2,\ yz,\ z^2
\]
with coefficients \(a_0,\ldots,a_5\) and
\(b_0,\ldots,b_5\).  Let \(L=(\ell_{ij})\).

After (5), the complete \(E_6\) system is affine linear in the twelve
variables
\[
a_1,\ldots,a_5,\quad b_1,\ldots,b_5,\quad
\ell_{32},\ell_{33}.                                   \tag{6}
\]
Its coefficient matrix has constant rank \(10\); a parameter-free
\(10\times10\) minor is
\[
7925422620672.                                         \tag{7}
\]
Exact left-kernel compatibility contains
\[
w_1(w_2-w_3),\qquad (w_2-w_3)^2.                       \tag{8}
\]
Thus \(w_2=w_3\) over \(\mathbb C\).

After that substitution, exact row reduction gives the complete solution
\[
\begin{aligned}
a_1&=0,&
a_2&=a_3-\frac{16}{9}w_1^2,&
a_4&=-\frac43Sw_1,&
a_5&=\frac14S^2,\\
b_1&=0,&
b_2&=b_3,&
b_4&=0,&
b_5&=\frac14S^2,                                      \tag{9}\\
\ell_{32}&=\frac23w_1(w_0-w_2),&
\ell_{33}&=\frac12Sw_2-\frac16w_1^2.
\end{aligned}
\]
The parameters \(a_3,b_3\) are free.  Substitution of (9) annihilates
every coefficient of \(E_6\), so no lower branch is lost.

## 4. Degree-five exit

Substituting (9) into the full degree-five identity, an exact left-kernel
compatibility is
\[
\frac89w_1^3=0.                                       \tag{10}
\]
Therefore \(w_1=0\).  Equations (9) now give
\[
\ell_{32}=0.                                          \tag{11}
\]

The remaining \(E_5\) polynomial is
\[
\begin{split}
6x^2\{&
Sa_3(x^2y+xyz+y^3)+Sb_3(x^2y-xyz-y^3)\\
&+\ell_{12}(x^3+x^2z+xy^2)
-2\ell_{13}(x^2y+xyz+y^3)\\
&+\ell_{22}(x^3-x^2z-xy^2)
-2\ell_{23}(x^2y-xyz-y^3)\}.                           \tag{12}
\end{split}
\]
The coefficients of \(x^5,x^4y,x^4z,x^3yz\) form a constant
four-variable minor
\[
20736.
\]
Their complete solution is
\[
\ell_{12}=\ell_{22}=0,\qquad
2\ell_{13}=Sa_3,\qquad 2\ell_{23}=Sb_3.                \tag{13}
\]
Together, (11) and (13) make the second column of \(L\) zero.  Hence
\[
\det L=0,
\]
contradicting the nonzero constant Jacobian of a Keller map.

## 5. Verification and disclosure

`verify_unmarked_triple_sympy.py` reconstructs the full raw kernel, all
legal gauges, both lower coefficient systems, the compatibility
polynomials, parameter-free minors, complete converses, and the zero-column
exit directly from the determinant.  The hostile PARI/GP audit independently
reconstructs the determinant, raw kernel, a literal degree-six square
syzygy, an integer degree-five row syzygy, both complete lower solves, and
the zero-column exit.

The result was developed with AI assistance.  The exact calculation is
evidence about the encoded algebra, not peer review.  The hostile audit
found no algebraic defect, hidden division, rank-drop branch, or scope
inflation.
