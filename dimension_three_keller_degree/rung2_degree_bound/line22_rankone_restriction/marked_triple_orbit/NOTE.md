# Exclusion of the marked-critical triple-companion orbit

**Status:** exact audited theorem.  The corrected SymPy certificate and
an independent PARI/GP reconstruction both pass, including fail-closed
tests.  This work is not peer reviewed.

**First recorded:** 2026-07-25T08:46:00Z.

## 1. Statement

Let
\[
F=LX+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have total degree four.  Put
\[
p=x^2,\qquad q=y^2+xz,
\]
and suppose
\[
H_4=(p^2,q^2,0),\qquad (H_3)_3=x^3.                    \tag{1}
\]
Thus one outer critical point and the triple cubic companion are both at
the unique double-line value of the quadratic pencil.

### Theorem

No Keller map has the leading data (1).

## 2. Complete degree-seven gauge

Write \(P=p^2,Q=q^2,R=x^3\) and
\[
U=(H_3)_1,\qquad V=(H_3)_2,\qquad W=(H_2)_3.
\]
The raw degree-seven coefficient matrix for
\[
\operatorname{Jac}(P,Q,W)+\operatorname{Jac}(P,V,R)
 +\operatorname{Jac}(U,Q,R)=0                          \tag{2}
\]
has rank \(8\) and nullity \(18\).  A fixed maximal minor is
\[
483729408.                                             \tag{3}
\]

Five legal kernel directions are the two target shears by \(R\) and the
three source-translation jets.  Thirteen normal directions, together with
those five gauges, have coefficient minor \(-2048/27\).  Hence every
solution of (2) has the complete normal form
\[
\begin{aligned}
U={}&A\,xq+\frac43\{w_1x^2y+(w_2-w_3)x^2z
                    +w_4xyz+w_5xz^2\},\\
V={}&B_1x^2y+B_2x^2z+B_3xyz+B_4xz^2+B_5y^2z
                    +B_6yz^2+B_7z^3,\\
W={}&w_1xy+w_2xz+w_3y^2+w_4yz+w_5z^2,\\
R={}&x^3.                                               \tag{4}
\end{aligned}
\]
No modulus or coefficient is divided out in obtaining (4).

## 3. Degree-six compatibility tree

Put
\[
d=w_2-w_3,\qquad K=4w_3-3A.                            \tag{5}
\]
The complete \(E_6\) system is affine linear in the lower coefficients.
Its coefficient matrix has constant rank \(4\), with parameter-free minor
\[
10368.
\]
Exact left-kernel compatibility first gives
\[
w_5^2=0,\qquad 3Aw_5+2w_4^2=0,
\]
and hence
\[
w_4=w_5=0.                                             \tag{6}
\]
After (6), the remaining compatibility is exactly
\[
\begin{gathered}
Aw_1=0,\qquad Ad=0,\\
KB_1=KB_2=KB_3=KB_6=KB_7=0,\qquad
K(B_4-B_5)=0.                                         \tag{7}
\end{gathered}
\]
The two equations involving \(B_6\) independently yield
\[
KB_6+2Aw_1=0,\qquad-KB_6+3Aw_1=0,
\]
so (7) uses characteristic zero essentially and loses no branch.

We close the two branches \(K\ne0\) and \(K=0\) separately.

## 4. The open branch \(K\ne0\)

Equation (7) gives
\[
B_1=B_2=B_3=B_6=B_7=0,\qquad B_4=B_5=:C.               \tag{8}
\]

If \(A\ne0\), (7) also gives \(w_1=d=0\).  If \(A=0\),
then \(w_3\ne0\), and the complete \(E_5\) compatibility contains
\[
w_1^3,\qquad d^3,
\]
so again \(w_1=d=0\).  Thus both subbranches reduce without division to
\[
H_3=(A\,xq,C\,zq,x^3),\qquad W=w_3q,\qquad
4w_3-3A\ne0.                                           \tag{9}
\]

For \(C\ne0,A\ne0\), the complete \(E_6,E_5,E_4\) solves successively
give
\[
\ell_{12}=\ell_{32}=0,\qquad
\ell_{33}=\frac12Cw_3,\qquad
\ell_{22}=0.                                          \tag{10}
\]
The generic \(E_5\) pivot here is proportional to
\(CA^2(3A-4w_3)^4\), so it cannot be specialized to \(A=0\).
On the fresh \(A=0,C\ne0\) chart, \(E_5\) has rank \(6\) rather than
\(8\) and leaves \(\ell_{32},\ell_{33}\) free.  Literal \(E_4\)
coefficients then give, successively,
\[
\frac43(2\ell_{33}-Cw_3)^2,\qquad
-\frac83\ell_{32}^2,\qquad
4w_3\ell_{22}.
\]
Since \(K=4w_3\ne0\), these recover (10).  Thus the second column of
\(L\) vanishes on both \(A\)-charts.

For \(C=0\), the literal \(E_5\) coefficients and \(K\ne0\) give
\[
\ell_{12}=\ell_{13}=0.
\]
If \(A\ne0\), the same identity gives
\(\ell_{32}=\ell_{33}=0\).  If \(A=0\), two \(E_4\)
coefficients are
\[
\frac{16}{3}\ell_{33}^2,\qquad
-\frac{8}{3}\ell_{32}^2
\quad\text{after }\ell_{33}=0,
\]
and give the same conclusion.  In either case \(\det L=0\).

## 5. The resonant branch \(K=0,\ A\ne0\)

Now
\[
w_3=w_2=\frac34A,\qquad w_1=0.
\]
Degree-five compatibility reduces the general cubic \(V\) to
\[
V=B_1x^2y+B_2x^2z+Czq.                                \tag{11}
\]
The lower system must first be split into the two open charts
\(B_1\ne0\) and \(B_1=0,B_2\ne0\).  Fixed \(E_5\) pivots on these
charts are respectively
\[
-1728A^2B_1,\qquad 3456A^2B_2,
\]
and fixed \(E_4\) pivots are
\[
\frac{243}{64}A^9B_1,\qquad
-\frac{243}{32}A^9B_2.
\]
On either chart the resulting literal \(E_3\) rows give
\[
[xyz]E_3-[y^3]E_3=-\frac38A^3B_2^2,
\qquad
[x^2y]E_3\big|_{B_2=0}=\frac3{16}A^3B_1^2.
\]
Thus the entire open stratum \((B_1,B_2)\ne(0,0)\) is impossible.

The closed stratum \(B_1=B_2=0\) is rebuilt before solving; it is not a
specialization of either open-chart solution.  If \(C=0\), a fresh
\(E_5\) pivot \(576A^2\) forces
\[
\ell_{12}=\ell_{13}=\ell_{32}=\ell_{33}=0,
\]
and hence \(\det L=0\).  If \(C\ne0\), fresh \(E_5\) has rank \(4\) and
gives
\[
\ell_{12}=\ell_{32}=0,\qquad
\ell_{33}=\frac38AC,\qquad
a_3=\frac{2\ell_{13}}{C},                             \tag{12}
\]
where \(\ell_{13}\) is genuinely free.  Here \(a_3\) denotes the
coefficient of \(y^2\) in \((H_2)_1\).  Fresh \(E_4\) gives
\[
b_1=0,\qquad b_2=b_3,\qquad b_4=0,\qquad b_5=C^2/4
\]
while still leaving \(\ell_{13}\) free.  Finally the literal residual
has
\[
[x^2z]E_3=[xy^2]E_3=\frac34A^2\ell_{22},
\]
and therefore
\[
\ell_{22}=0,
\]
so the second column of \(L\) is zero.  This fresh closed-chart argument
is essential: the earlier provisional formula
\(\ell_{13}=-A^2B_2/8\) was false on this rank-drop stratum.

## 6. The resonant branch \(K=A=0\)

Here \(w_3=0\).  Before specialization, exact \(E_5\) compatibility
contains
\[
w_1^3,\qquad w_2^3,
\]
and hence \(w_1=w_2=0\).  Thus
\[
H_3=(0,V,x^3),\qquad W=0,                              \tag{13}
\]
with the seven coefficients of \(V\) still arbitrary.

After the constant-rank \(E_6\) solve, the nine nonzero \(E_5\)
coefficients are
\[
\begin{array}{rclcrcl}
-3B_1a_3&=&0,&&6B_2a_3&=&0,\\
-3B_3a_3+6\ell_{12}&=&0,&&
6B_3a_3+6\ell_{12}&=&0,\\
(12B_4-6B_5)a_3-12\ell_{13}&=&0,&&
6B_5a_3-12\ell_{13}&=&0,\\
-3B_6a_3&=&0,&&12B_6a_3&=&0,\\
18B_7a_3&=&0.&&&&
\end{array}                                           \tag{14}
\]
They give an exhaustive product-ideal split.

If \(a_3=0\), the paired rows in (14) force
\(\ell_{12}=\ell_{13}=0\).  The residual \(E_4\) contains
\[
\frac{16}{3}\ell_{33}^2,\qquad
-\frac{8}{3}\ell_{32}^2
\quad\text{after }\ell_{33}=0.
\]
Therefore \(\ell_{32}=\ell_{33}=0\), and \(\det L=0\).

If \(a_3\ne0\), (14) forces the unique exceptional shape
\[
V=Czq,\qquad
\ell_{12}=0,\qquad \ell_{13}=\frac12Ca_3.             \tag{15}
\]
There are no other seven-parameter leaves.  The same two \(E_4\)
squares force \(\ell_{33}=\ell_{32}=0\).  If \(C=0\), (15) already
gives \(\det L=0\).  On the remaining chart \(Ca_3\ne0\), a fresh
\(E_4\) pivot \(648a_3^4\) gives
\[
b_1=0,\qquad b_2=b_3,\qquad b_4=0,\qquad b_5=C^2/4.
\]
The literal residual coefficient
\[
[x^3]E_3=-3a_3\ell_{22}
\]
forces \(\ell_{22}=0\), so the second column of \(L\) vanishes.  Thus
the provisional claim that \(E_5\) always forces \(a_3=0\) is replaced
by the exhaustive split (14)--(15).

Sections 4--6 exhaust the projective compatibility tree (7), so the
theorem follows.

## 7. Verification and disclosure

`verify_marked_triple_sympy.py` reconstructs the raw kernel and legal
gauge, the full degree-six compatibility ideal, every generic and
rank-drop lower branch, all stated fixed pivots and converses, and each
square or zero-column exit directly from the weighted Jacobian
determinant.  The independent
`audit_hostile/independent/verify_marked_triple_pari.gp` reconstruction
uses PARI/GP and explicitly targets every specialization hazard found
during hostile review.

AI systems materially assisted discovery, computation, verification, and
exposition.  Exact checks establish facts about the encoded algebra; they
are not peer review.
