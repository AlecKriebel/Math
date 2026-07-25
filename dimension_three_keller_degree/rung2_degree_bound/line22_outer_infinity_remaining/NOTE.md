# Finite companions over the outer-critical-at-infinity line-\((2,2)\) chart

**Status:** exact working theorem; independent hostile audit passed at
2026-07-25T07:01:00Z.  This note is not peer reviewed.

**First recorded:** 2026-07-25T06:38:00Z.

## 1. Statement and orbit ledger

Let
\[
F=LX+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have degree four and constant nonzero Jacobian.  In the
unique-double-line, line-image \((2,2)\) row, put
\[
p=x^2,\qquad q=yz
\]
and consider the outer-critical-at-infinity chart
\[
H_4=((p-aq)^2,q^2,0)^T,\qquad
(H_3)_3=x(p-cq).                                      \tag{1}
\]

The residual stabilizer acts on the two parameters by simultaneous
scaling
\[
(a,c)\longmapsto(\lambda a,\lambda c).                 \tag{2}
\]
Thus the nonzero finite-companion orbits are the points
\([a:c]\in\mathbb P^1\), while \((a,c)=(0,0)\) is a separate fixed
orbit.

### Theorem

There is no Keller map with leading data (1) for any
\((a,c)\ne(0,0)\).

The fixed orbit \((a,c)=(0,0)\), namely
\[
H_4=(p^2,q^2,0),\qquad (H_3)_3=x^3,
\]
was excluded in the separate `line22_marked_critical_infinity`
package.  Consequently, among companions in this outer chart, only
the companion-at-infinity form
\[
(H_3)_3=xq                                             \tag{3}
\]
remains.  It has two residual outer orbits, \(a=0\) and \(a\ne0\).

This theorem does not address (3), the chart with both outer critical
points finite and companion at infinity, or the rank-one-restriction
pencil \(p=x^2,q=y^2+xz\).

## 2. Conventions, gauges, and the complete \(E_7\) converse

Write
\[
U=(H_3)_1,\qquad V=(H_3)_2,\qquad W=(H_2)_3
\]
and
\[
\begin{aligned}
(H_2)_1&=\alpha _0p+\alpha _1xy+\alpha _2xz
 +\alpha _3y^2+\alpha _4q+\alpha _5z^2,\\
(H_2)_2&=\beta _0p+\beta _1xy+\beta _2xz
 +\beta _3y^2+\beta _4q+\beta _5z^2.
\end{aligned}                                          \tag{4}
\]
Let \(L=(\ell _{ij})_{1\le i,j\le3}\).  If
\[
\det JF=\sum_{d=0}^9 E_d
\]
is split into ordinary homogeneous degrees, the Keller condition says
\[
E_d=0\quad(d>0),\qquad E_0=\det L\ne0.                  \tag{5}
\]

The coefficient of \(x^3\) in \(x(p-cq)\) is one.  Target shears
\[
F_1\mapsto F_1+\lambda F_3,\qquad
F_2\mapsto F_2+\mu F_3                                 \tag{6}
\]
therefore remove the \(x^3\) coefficients of \(U,V\).  They leave
\(H_4\) fixed and merely relabel the unrestricted forms (4) and the
first two rows of \(L\).  No source-translation gauge is used below.

The exact raw \(E_7\) ranks, before the two shears (6), are:

| orbit stratum | normalization | raw rank | raw nullity |
|---|---:|---:|---:|
| generic with \(a\ne0\), \(c(3a-c)(3a-2c)\ne0\) | \((a,c)=(1,t)\) | 18 | 8 |
| first resonance | \((1,3)\) | 14 | 12 |
| second resonance | \((2,3)\) | 14 | 12 |
| noncritical triple | \((1,0)\) | 16 | 10 |
| marked mixed | \((0,1)\) | 18 | 8 |

For the generic matrix, the verifier records an \(18\)-minor
\[
-782757789696\,t^4(t-3)^4(2t-3)^6.                    \tag{7}
\]
For the last four rows of the table, recorded maximal minors are,
respectively,
\[
-101559956668416,\quad
-6499837226778624,\quad
25999348907114496,\quad
-50096498540544.                                       \tag{8}
\]
The parametrizations below have exactly the displayed nullities after
the two shear directions are restored.  Equations (7)--(8) therefore
give both inequalities in every raw-rank claim and prove that the
lists are complete kernels, not ansatzes.

## 3. Generic orbit

Assume \(a\ne0\), normalize \(a=1\), and put \(t=c/a\).  In this
section
\[
t(3-t)(3-2t)\ne0.                                      \tag{9}
\]
The complete gauge-fixed \(E_7\) kernel is
\[
\begin{aligned}
W={}&w_0p+w_1xy+w_2xz+w_4q,\\
U={}&Axq+\frac2t w_1(x^2y-y^2z)
             +\frac2t w_2(x^2z-yz^2),\\
V={}&Bxq-\frac2t(w_1y^2z+w_2yz^2).
\end{aligned}                                          \tag{10}
\]
The complete \(E_6\) solution is
\[
\begin{array}{lll}
\alpha _1=-Aw_1/t,&\alpha _2=-Aw_2/t,&
\alpha _3=w_1^2/t^2,\quad\alpha _5=w_2^2/t^2,\\
\beta _1=-Bw_1/t,&\beta _2=-Bw_2/t,&
\beta _3=w_1^2/t^2,\quad\beta _5=w_2^2/t^2,\\
\ell _{32}=-w_1w_4/t,&\ell _{33}=-w_2w_4/t.&
\end{array}                                             \tag{11}
\]
Here and below the unlisted coefficients remain free.

The complete \(E_5\) solution then gives
\[
\begin{aligned}
\ell _{12}&=-\alpha _4w_1/t+2w_1^2w_2/t^3,&
\ell _{13}&=-\alpha _4w_2/t+2w_1w_2^2/t^3,\\
\ell _{22}&=-\beta _4w_1/t+2w_1^2w_2/t^3,&
\ell _{23}&=-\beta _4w_2/t+2w_1w_2^2/t^3.
\end{aligned}                                           \tag{12}
\]
Thus columns two and three of \(L\) are
\[
w_1
\begin{pmatrix}
-\alpha _4/t+2w_1w_2/t^3\\
-\beta _4/t+2w_1w_2/t^3\\
-w_4/t
\end{pmatrix},
\qquad
w_2
\begin{pmatrix}
-\alpha _4/t+2w_1w_2/t^3\\
-\beta _4/t+2w_1w_2/t^3\\
-w_4/t
\end{pmatrix}.                                          \tag{13}
\]
This includes \(w_1=0\), \(w_2=0\), and \(w_1=w_2=0\);
in every case \(\det L=0\), contradicting (5).

## 4. First resonance \(c=3a\ne0\)

Normalize \((a,c)=(1,3)\).  Before \(E_6\), the complete kernel is
\[
\begin{aligned}
W={}&w_0p+w_1xy+w_2xz+w_3y^2+w_4q+w_5z^2,\\
U={}&Axq+(r_1+\tfrac43w_1)x^2y+r_1y^2z
 +(r_2+\tfrac43w_2)x^2z+r_2yz^2\\
 &+\tfrac43w_3xy^2+\tfrac43w_5xz^2,\\
V={}&Bxq+r_1y^2z+r_2yz^2.
\end{aligned}                                           \tag{14}
\]
Degree six contains the squares
\[
[y^5z]E_6=-\frac{16}{3}w_3^2,\qquad
[yz^5]E_6=\frac{16}{3}w_5^2.                            \tag{15}
\]
After \(w_3=w_5=0\), the \(x^5y,x^5z,x^4y^2,x^4z^2,
y^4z^2,y^2z^4\) coefficients first give
\[
\begin{aligned}
\beta _1&=Br_1/2,&\beta _2&=Br_2/2,\\
\alpha _3=\beta _3&=r_1^2/4,&
\alpha _5=\beta _5&=r_2^2/4.
\end{aligned}
\]
The two remaining \(x^2y^3z,x^2yz^3\) coefficients then reduce to
\[
-\frac23(3r_1+2w_1)^2,\qquad
\frac23(3r_2+2w_2)^2.                                  \tag{16}
\]
Thus \(r_i=-2w_i/3\).  The remaining complete \(E_6\)
solution is
\[
\begin{aligned}
\beta _1&=-Bw_1/3,&\beta _2&=-Bw_2/3,&
\beta _3&=w_1^2/9,&\beta _5&=w_2^2/9,\\
\alpha _1&=-Aw_1/3+\tfrac43\ell _{32}+\tfrac49w_1w_4,&
\alpha _2&=-Aw_2/3+\tfrac43\ell _{33}+\tfrac49w_2w_4,\\
\alpha _3&=w_1^2/9,&\alpha _5&=w_2^2/9.
\end{aligned}                                           \tag{17}
\]

Put
\[
s_1=3\ell _{32}+w_1w_4,\quad
s_2=3\ell _{33}+w_2w_4,\quad
K_1=-3A+6B+8w_0.                                       \tag{18}
\]
The remaining four entries of columns two and three are forced by
\[
\begin{aligned}
\ell _{12}&=-\alpha _4w_1/3+2w_1^2w_2/27+(B-A)s_1/9,\\
\ell _{13}&=-\alpha _4w_2/3+2w_1w_2^2/27+(B-A)s_2/9,\\
\ell _{22}&=-\beta _4w_1/3+2w_1^2w_2/27,\\
\ell _{23}&=-\beta _4w_2/3+2w_1w_2^2/27.
\end{aligned}                                           \tag{19}
\]
After (17)--(19), the full degree-five polynomial is exactly
\[
E_5=\frac29x^2yz(s_1y-s_2z)K_1.                        \tag{20}
\]
This gives the division-free equations \(K_1s_1=K_1s_2=0\).

If \(K_1\ne0\), then \(s_1=s_2=0\).  If \(K_1=0\), no
division is made: degree four gives
\[
[y^3z]E_4=-\frac8{27}s_1^2,\qquad
[yz^3]E_4=\frac8{27}s_2^2,                              \tag{21}
\]
so again \(s_1=s_2=0\).  Substitution in (18)--(19) makes
columns two and three \(w_1v,w_2v\), with
\[
v=
\begin{pmatrix}
-\alpha _4/3+2w_1w_2/27\\
-\beta _4/3+2w_1w_2/27\\
-w_4/3
\end{pmatrix}.                                          \tag{22}
\]
Hence \(\det L=0\).

## 5. Second resonance \(2c=3a\ne0\)

Normalize \((a,c)=(2,3)\).  The complete pre-\(E_6\)
kernel is
\[
\begin{aligned}
W={}&w_0p+w_1xy+w_2xz+w_3y^2+w_4q+w_5z^2,\\
U={}&Axq-2r_1x^2y+4r_1y^2z-2r_2x^2z+4r_2yz^2,\\
V={}&Bxq+(-r_1-\tfrac23w_1)x^2y+r_1y^2z\\
 &+(-r_2-\tfrac23w_2)x^2z+r_2yz^2
 -\tfrac23w_3xy^2-\tfrac23w_5xz^2.
\end{aligned}                                           \tag{23}
\]
The coefficients of \(x^2y^4,x^2z^4\) first force
\(w_3=w_5=0\).  The coefficients of \(x^4y^2,x^4z^2\)
then are
\[
\frac23(3r_1+2w_1)^2,\qquad
-\frac23(3r_2+2w_2)^2,                                 \tag{24}
\]
so \(r_i=-2w_i/3\).  The remaining complete \(E_6\)
solution is
\[
\begin{aligned}
\alpha _1&=-Aw_1/3,&\alpha _2&=-Aw_2/3,&
\alpha _3&=4w_1^2/9,&\alpha _5&=4w_2^2/9,\\
\beta _1&=-Bw_1/3-\tfrac23\ell _{32}-\tfrac29w_1w_4,&
\beta _2&=-Bw_2/3-\tfrac23\ell _{33}-\tfrac29w_2w_4,\\
\beta _3&=w_1^2/9,&\beta _5&=w_2^2/9.
\end{aligned}                                           \tag{25}
\]

Use the same \(s_1,s_2\) as in (18), and put
\[
K_2=-3A+6B+8w_0+4w_4.                                  \tag{26}
\]
Degree five solves the remaining entries as
\[
\begin{aligned}
\ell _{12}&=As_1/9-8Bs_1/9-32s_1w_0/27-16s_1w_4/27
 -\alpha _4w_1/3+8w_1^2w_2/27,\\
\ell _{13}&=As_2/9-8Bs_2/9-32s_2w_0/27-16s_2w_4/27
 -\alpha _4w_2/3+8w_1w_2^2/27,\\
\ell _{22}&=As_1/18-Bs_1/3-8s_1w_0/27-4s_1w_4/27
 -\beta _4w_1/3+2w_1^2w_2/27,\\
\ell _{23}&=As_2/18-Bs_2/3-8s_2w_0/27-4s_2w_4/27
 -\beta _4w_2/3+2w_1w_2^2/27,
\end{aligned}                                           \tag{27}
\]
and the full residual is
\[
E_5=-\frac29x^4(s_1y-s_2z)K_2.                         \tag{28}
\]
Again split without dividing.  If \(K_2\ne0\), then
\(s_1=s_2=0\).  If \(K_2=0\), degree four gives
\[
[x^2y^2]E_4=\frac8{27}s_1^2,\qquad
[x^2z^2]E_4=-\frac8{27}s_2^2,                           \tag{29}
\]
with the same conclusion.  The last two columns become \(w_1v,w_2v\),
where now
\[
v=
\begin{pmatrix}
-\alpha _4/3+8w_1w_2/27\\
-\beta _4/3+2w_1w_2/27\\
-w_4/3
\end{pmatrix}.                                          \tag{30}
\]
Thus \(\det L=0\).

## 6. Noncritical triple \(c=0,a\ne0\)

Normalize \((a,c)=(1,0)\).  The complete \(E_7\) kernel is
\[
\begin{aligned}
W={}&w_0p+w_1xy+w_2xz+w_4q,\\
U={}&Axq+(-r_1+\tfrac43w_1)x^2y
 +(r_1-\tfrac43w_1)y^2z\\
 &+(-r_2+\tfrac43w_2)x^2z+(r_2-\tfrac43w_2)yz^2,\\
V={}&Bxq+r_1y^2z+r_2yz^2.
\end{aligned}                                           \tag{31}
\]
Degree six contains
\[
[y^4z^2]E_6=-\frac83w_1^2,\qquad
[y^2z^4]E_6=\frac83w_2^2,                              \tag{32}
\]
so \(w_1=w_2=0\).  Its remaining complete solution is
\[
\begin{aligned}
\alpha _1&=Ar_1/2,&\alpha _2&=Ar_2/2,&
\alpha _3&=r_1^2/4,&\alpha _5&=r_2^2/4,\\
\beta _1&=Br_1/2,&\beta _2&=Br_2/2,&
\beta _3&=r_1^2/4,&\beta _5&=r_2^2/4,\\
\ell _{32}&=r_1w_4/2,&\ell _{33}&=r_2w_4/2.
\end{aligned}                                           \tag{33}
\]
Degree five gives
\[
\begin{aligned}
\ell _{12}&=\alpha _4r_1/2-r_1^2r_2/4,&
\ell _{13}&=\alpha _4r_2/2-r_1r_2^2/4,\\
\ell _{22}&=\beta _4r_1/2-r_1^2r_2/4,&
\ell _{23}&=\beta _4r_2/2-r_1r_2^2/4.
\end{aligned}                                           \tag{34}
\]
The last two columns are \(r_1v,r_2v\), including all zero
specializations, so \(\det L=0\).

## 7. Marked mixed point \(a=0,c\ne0\)

Normalize \((a,c)=(0,1)\).  The complete \(E_7\) kernel is
\[
\begin{aligned}
W&=w_0p+w_1xy+w_2xz+w_4q,\\
U&=Axq,\\
V&=Bxq-2w_1y^2z-2w_2yz^2.
\end{aligned}                                           \tag{35}
\]
The complete \(E_6\) solution is
\[
\begin{aligned}
\alpha _1&=-Aw_1,&\alpha _2&=-Aw_2,&
\alpha _3&=\alpha _5=0,\\
\beta _1&=-Bw_1,&\beta _2&=-Bw_2,&
\beta _3&=w_1^2,&\beta _5&=w_2^2,\\
\ell _{32}&=-w_1w_4,&\ell _{33}&=-w_2w_4.
\end{aligned}                                           \tag{36}
\]
Degree five then forces
\[
\begin{aligned}
\ell _{12}&=-\alpha _4w_1,&
\ell _{13}&=-\alpha _4w_2,\\
\ell _{22}&=-\beta _4w_1+2w_1^2w_2,&
\ell _{23}&=-\beta _4w_2+2w_1w_2^2.
\end{aligned}                                           \tag{37}
\]
Once more the last two columns are \(w_1v,w_2v\), even at
\(w_1=w_2=0\).  Hence \(\det L=0\).

Sections 3--7 exhaust \(\mathbb P^1_{[a:c]}\), proving the theorem.

## 8. Verification and disclosure

`verify_line22_outer_infinity_remaining_sympy.py` reconstructs the raw
\(E_7\) matrices, exact maximal-rank minors, all five complete kernels,
the complete generic coefficient table, every triangular lower solve,
the two division-free resonance reductions, the exceptional squares,
and every determinant exit.

`verify_line22_outer_infinity_remaining_pari.gp`, run through the strict
wrapper, independently forms
\[
\det\!\left(L+T\,JH_2+T^2JH_3+T^3JH_4\right)
\]
inside PARI/GP and checks the solved \(E_6,E_5,E_4\) identities directly.
`test_fail_closed.sh` verifies the Python optimized-mode guard and the
strict wrapper's diagnostic, sentinel, and exit-status behavior.

AI systems materially assisted the discovery, exact calculations, and
exposition.  Exact checks are evidence about the encoded algebra; they
are not peer review.  The accompanying source-specific priority audit is
not a guarantee of worldwide priority.  The hostile audit in
`audit_hostile/REPORT.md` independently reconstructed the full orbit
ledger, all raw ranks, complete kernels and lower converses, both
resonance splits, and every zero-specialization-safe determinant exit.
