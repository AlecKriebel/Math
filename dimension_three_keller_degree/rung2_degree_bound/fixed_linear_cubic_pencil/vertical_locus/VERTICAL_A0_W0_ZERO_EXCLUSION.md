# The zero-\(a\), zero-\(W_0\) vertical companion is impossible

**Recorded (UTC):** 2026-07-25T22:12:00Z.

**Status:** exact theorem, passed an independent hostile reconstruction
with a second symbolic parameterization and a PARI/GP exterior expansion.
It is not peer reviewed. It excludes a sublocus of frozen row
`Q2-E1-A3-B1-D1-N1`; it does not exclude that row.

## Statement

Let a normalized quartic Keller candidate over \(\mathbb C\) have
\[
H_4=(z^4,zq,0)^T,\qquad
H_3=\left(\frac43zW,\ V,\ z^3\right)^T,\qquad
H_2=(A,B,W)^T,                                      \tag{1}
\]
where \((z^3,q)\) is a minimal cubic pencil and the \(z^3\)-coefficient
of \(V\) has been removed by a legal target shear.  Suppose
\[
W|_{z=0}=0.                                          \tag{2}
\]
Then the homogeneous determinant identities \(E_6=E_5=E_4=0\) force
the linear part of the map to be singular.  Consequently no Keller map
occurs on this locus.

In the notation of `E8_E4_RANK_LEDGER.md`, this is the complete
\(a=0,W_0=0\) vertical-companion family.  The separate family
\(a=0,W_0\ne0\) is not addressed.

## 1. Complete retained atlas

Write
\[
W=z(ux+vy+wz).                                       \tag{3}
\]
After a binary source change and the leading target shear that removes
\([z^3]q\), the nontriple charts are
\[
\begin{aligned}
q_{\rm sf}&=xy(x-y)+z(r_{20}x^2+r_{11}xy+r_{02}y^2)
                 +z^2(r_{10}x+r_{01}y),\\
q_{\rm dbl}&=x^2y+z(r_{20}x^2+r_{11}xy+r_{02}y^2)
                 +z^2(r_{10}x+r_{01}y).              \tag{4}
\end{aligned}
\]
All five displayed tail moduli are retained.  The complete minimal
triple-root atlas is
\[
\begin{aligned}
q_C&=x^3+y^2z+\alpha xz^2,\\
q_B&=x^3+xyz,\\
q_E&=x^3+yz^2.                                       \tag{5}
\end{aligned}
\]
The missing triple-root shape is binary in \(x,z\), hence is precisely
the nonminimal boundary.  Thus (4)--(5) cover the whole locus in the
statement.

Write
\[
\begin{aligned}
A={}&A_{20}x^2+A_{11}xy+A_{02}y^2
       +A_{10}xz+A_{01}yz+A_{00}z^2,\\
L_i={}&\ell_{i1}x+\ell_{i2}y+\ell_{i3}z
\end{aligned}                                        \tag{6}
\]
for the first quadratic row and the rows of the linear part.  Every
coefficient of \(B,V,L\), as well as every coefficient in (3)--(6), is
left arbitrary in the calculation.

## 2. The universal degree-six solve

On each chart, five displayed coefficients of the raw \(E_6\) identity
form a constant nonsingular linear system in
\[
(A_{20},A_{11},A_{02},\ell_{31},\ell_{32}).            \tag{7}
\]
The selected monomials and determinants are
\[
\begin{array}{c|c|r}
\text{chart}&\text{monomials }x^iy^jz^k&\det\\ \hline
q_{\rm sf}&
(303),(213),(033),(204),(024)&-1728\\
q_{\rm dbl}&
(303),(213),(123),(204),(114)&-6912\\
q_C&(114),(303),(213),(015),(204)&-186624\\
q_B&(303),(213),(015),(105),(204)&15552\\
q_E&(105),(303),(213),(006),(204)&-46656.
\end{array}                                           \tag{8}
\]
Here \((ijk)\) abbreviates \(x^iy^jz^k\).  Exact solution, followed by
substitution into every coefficient of \(E_6\), gives on all five charts
\[
\boxed{
\begin{aligned}
A_{20}&=\frac29u^2,&
A_{11}&=\frac49uv,&
A_{02}&=\frac29v^2,\\
\ell_{31}&=\frac{9A_{10}-4uw}{12},&
\ell_{32}&=\frac{9A_{01}-4vw}{12}.
\end{aligned}}                                       \tag{9}
\]
Thus no \(E_6\) rank divisor or specialization of a tail modulus is
suppressed.

## 3. The degree-five compatibility split

Substitute (9) into the complete raw \(E_5\) identity.

For the squarefree and double-root charts, respectively,
\[
\begin{array}{c|cc}
q_{\rm sf}&[x^4z]E_5=\frac49u^3&
[y^4z]E_5=\frac49v^3\\[1mm]
q_{\rm dbl}&[x^4z]E_5=\frac49u^3&
[xy^3z]E_5=-\frac89v^3.
\end{array}                                           \tag{10}
\]
Hence \(u=v=0\) on both nontriple charts.

On \(q_C\),
\[
[x^2y^2z]E_5=-\frac43v^3,\qquad
[x^2yz^2]E_5\big|_{v=0}=\frac89u^3,                  \tag{11}
\]
so again \(u=v=0\).

On \(q_B\), the first equation
\[
[x^2y^2z]E_5=-\frac43v^3                             \tag{12}
\]
gives \(v=0\).  The remaining two compatibility equations are
\[
\begin{aligned}
[x^3z^2]E_5\big|_{v=0}
  &=\frac{u}{9}(27A_{01}+4u^2),\\
-\frac13[x^2z^3]E_5+[yz^4]E_5\big|_{v=0}
  &=-\frac{2u}{27}(-9A_{10}+8uw).
\end{aligned}                                        \tag{13}
\]
Consequently either \(u=0\), or
\[
A_{10}=\frac89uw,\qquad A_{01}=-\frac4{27}u^2.        \tag{14}
\]

On \(q_E\), (12) again gives \(v=0\), while
\[
\begin{aligned}
[xz^4]E_5\big|_{v=0}
  &=\frac{2u}{9}(-9A_{10}+8uw),\\
[yz^4]E_5\big|_{v=0}&=-uA_{01}.
\end{aligned}                                        \tag{15}
\]
Thus either \(u=0\), or
\[
A_{10}=\frac89uw,\qquad A_{01}=0.                    \tag{16}
\]
Equations (10)--(16) are compatibility identities: they contain no
coefficient of \(B,V,L\), and no division by a tail modulus occurs.

## 4. The zero-\(\ell\) branch

First take \(u=v=0\), on any of the five charts.  The complete \(E_5\)
identity then gives
\[
\ell_{11}=\frac13A_{10}w,\qquad
\ell_{12}=\frac13A_{01}w.                             \tag{17}
\]
Selected raw \(E_4\) coefficients now force
\(A_{10}=A_{01}=0\):
\[
\begin{array}{c|cc}
q_{\rm sf}&[x^3z]E_4=-\frac34A_{10}^2&
[y^3z]E_4=-\frac34A_{01}^2\\
q_{\rm dbl}&[x^3z]E_4=-\frac34A_{10}^2&
[xy^2z]E_4=\frac32A_{01}^2\\
q_C&[x^2yz]E_4=\frac94A_{01}^2&
[xyz^2]E_4=-\frac32A_{10}^2\\
q_B&[x^2yz]E_4=\frac94A_{01}^2&
[x^2z^2]E_4\big|_{A_{01}=0}=-\frac34A_{10}^2\\
q_E&[x^2yz]E_4=\frac94A_{01}^2&
[xz^3]E_4=-\frac34A_{10}^2.
\end{array}                                           \tag{18}
\]
Equations (9), (17), and (18) give
\[
\ell_{11}=\ell_{12}=\ell_{31}=\ell_{32}=0.            \tag{19}
\]
The first and third rows of \(L\) are therefore both multiples of
\((0,0,1)\), so \(\det L=0\).

## 5. The two exceptional nonzero-\(u\) branches

It remains to exclude (14) and (16), where \(u\ne0\).

On the \(q_B\) branch (14), the full \(E_5\) identity solves
\[
\ell_{11}=\frac23A_{00}u-\frac49\ell_{33}u
           -\frac4{27}uw^2,\qquad
\ell_{12}=-\frac4{81}u^2w.                            \tag{20}
\]
Three \(E_4\) coefficients are
\[
\begin{aligned}
[x^4]E_4&=\frac4{81}u^3(9[x^2y]V+u),\\
[y^2z^2]E_4&=\frac4{243}u^3(18[yz^2]V+u),\\
[x^2yz]E_4&=-\frac4{27}u^3
 \bigl([x^2y]V-6[yz^2]V-u\bigr).
\end{aligned}                                        \tag{21}
\]
Their vanishing would give
\[
[x^2y]V=-u/9,\qquad [yz^2]V=-u/18,
\]
but the last parenthesis in (21) would then be \(-7u/9\), a
contradiction.

On the \(q_E\) branch (16), \(E_5=0\) gives
\[
\ell_{11}=\frac23A_{00}u-\frac49\ell_{33}u
           -\frac4{27}uw^2,\qquad
\ell_{12}=\frac4{81}u^3.                              \tag{22}
\]
Two raw \(E_4\) coefficients are
\[
\begin{aligned}
[x^3z]E_4&=\frac4{81}u^3(9[xyz]V-2u),\\
[yz^3]E_4&=-\frac4{27}u^3([xyz]V-u).
\end{aligned}                                        \tag{23}
\]
Their simultaneous vanishing would require
\([xyz]V=2u/9=u\), again impossible for \(u\ne0\).

Every branch therefore either reaches (19) or is contradicted directly
by \(E_4\).  Finally, because all \(H_i\) have degree at least two,
\(JF(0)=L\).  A Keller map must have
\(\det L=\det JF(0)\ne0\), contrary to (19).  This proves the theorem.
\(\square\)

## 6. Exact verification and scope

Run

```text
./verify_vertical_a0_w0zero_strict.sh
./audit_vertical_a0_w0_zero/verify_strict.sh
```

The checker starts from the raw \(3\times3\) determinant on all five
charts.  It retains all five nontriple tail moduli, every lower jet, and
the triple-chart modulus \(\alpha\).  It verifies the five constant
minors in (8), substitutes (9) into every \(E_6\) coefficient, and checks
all identities (10)--(23), with fail-closed mutations.

The hostile report is
`audit_vertical_a0_w0_zero/REPORT.md`. Its derivation was completed before
the candidate was opened; it retains the \(z^3\)-coefficients removed here
by legal shears and independently replays the five-chart calculation.

The calculation contains no resultant, denominator clearing, numerical
specialization, or generic-rank assumption. It is an exact check of the
encoded algebra, not peer review. This note, audit, and their software were
produced with substantial AI assistance.
