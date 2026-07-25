# The nonzero-\(\ell\), nontriple vertical companion is impossible

**Recorded (UTC):** 2026-07-25T21:31:36Z.

**Status:** exact lemma, passed an independent dependency-free hostile
audit. It is not peer reviewed. It excludes a sublocus of the frozen row
`Q2-E1-A3-B1-D1-N1`; it does not exclude that row.

## Statement

Let a normalized quartic Keller candidate have
\[
H_4=(z^4,zq,0)^T,\qquad
H_3=\left(\frac43zW+s q,\ V,\ z^3\right)^T,\qquad
H_2=(A,B,W)^T,
\tag{1}
\]
where \(s\ne0\), \(A,B,W\) are quadratic, and the \(z^3\)-coefficients of
\(q\) and \(V\) have been killed by the legal target shears in
`E8_E4_RANK_LEDGER.md`. Suppose
\[
q_0=q|_{z=0}
\]
is squarefree or has one double root. The degree-six identity forces
\[
W=z^2\omega
\]
after the complete binary degree-five restrictions are imposed.
Equivalently, no Keller map in either nontriple root stratum can have
\[
W=z\ell+\omega z^2,\qquad 0\ne\ell\in\mathbb C[x,y]_1.
\tag{2}
\]

The statement includes all squarefree root-line collisions, the
double-root noncollision locus, and both double-root collision branches
\(\ell\sim x\) and \(\ell\sim y\).

Together with `VERTICAL_ELL_ZERO_NONTRIPLE_LEMMA.md`, this eliminates the
entire \(s\ne0\), nontriple vertical-companion locus. The triple-root and
\(s=0\) branches remain outside the statement.

## 1. Full retained normal forms

After a binary source change, write
\[
q_0=xy(x-y)\quad\text{or}\quad q_0=x^2y,
\tag{3}
\]
and retain every lower-\(z\) modulus:
\[
q=q_0+z(r_{20}x^2+r_{11}xy+r_{02}y^2)
       +z^2(r_{10}x+r_{01}y).
\tag{4}
\]
Write
\[
\ell=ux+vy
\tag{5}
\]
and retain the arbitrary coefficient \(\omega\) in (2). All six
coefficients of each of \(A,B\), all five nonbinary coefficients of \(V\),
and every unrestricted entry of the linear part are also retained below.
No coefficient in (4) or in a lower homogeneous term is assumed nonzero.

Let
\[
\{f,g\}=f_xg_y-f_yg_x.
\]
If
\[
V_0=V|_{z=0},\qquad
\bar L_3=\ell_{31}x+\ell_{32}y,
\]
then direct extraction from the raw determinant gives
\[
E_5|_{z=0}
=s\left(\ell\{q_0,V_0\}
        -q_0\{q_0,\bar L_3\}\right).
\tag{6}
\]
Before using this equation, allow a general binary part
\[
W_0=g_0x^2+g_1xy+g_2y^2.
\]
Direct restriction of the raw degree-six determinant gives
\[
E_6|_{z=0}=-s\,q_0\{q_0,W_0\}.
\]
For either form in (3), the coefficient matrix of
\(K_2\mapsto\{q_0,K_2\}\) has the literal \(3\times3\) minor \(-8\).
Since \(s\ne0\) and the polynomial ring is a domain, this forces
\(W_0=0\), justifying the form \(W=z\ell+\omega z^2\) used below.

Now the binary equation is
\[
\ell\{q_0,V_0\}=q_0\{q_0,\bar L_3\}.
\tag{7}
\]

## 2. The complete binary \(E_5\) kernels

Order the six unknown coefficients by
\[
( [x^3]V_0,[x^2y]V_0,[xy^2]V_0,[y^3]V_0,
   \ell_{31},\ell_{32}).
\tag{8}
\]
Order the equation rows by
\((x^5,x^4y,x^3y^2,x^2y^3,xy^4,y^5)\).

### Squarefree cubic

For \(q_0=xy(x-y)\), the vector \((0,1,-1,0,0,0)\) spans the expected
\((q_0,0)\) kernel. Three \(5\times5\) minors of the coefficient matrix of
(7), all using columns \((0,1,3,4,5)\), are
\[
\begin{array}{c|c}
\text{rows}&\text{minor}\\ \hline
(0,1,2,3,4)&-27u(u^2-4uv-4v^2),\\
(0,1,2,4,5)&27u^2v,\\
(1,2,3,4,5)&27v(4u^2+4uv-v^2).
\end{array}
\tag{9}
\]
If \(uv\ne0\), the middle minor is nonzero. If \(v=0,u\ne0\), the first
minor is \(-27u^3\). If \(u=0,v\ne0\), the last minor is \(-27v^3\).
Thus every nonzero \(\ell\), including each root-line collision, has
rank five and
\[
\boxed{V_0=\kappa q_0,\qquad \bar L_3=0.}
\tag{10}
\]
No coefficient of \(\ell\) was divided out.

### Double-root cubic away from collisions

For \(q_0=x^2y\), on the noncollision locus \(uv\ne0\), a \(5\times5\)
minor on rows \((0,1,2,3,4)\) and columns \((0,2,3,4,5)\) is
\[
\boxed{108uv^2.}
\tag{11}
\]
The known kernel is \((q_0,0)\), so (10) again gives the complete solution.

On this generic kernel, direct degree-four extraction also recovers
\[
E_4|_{z=0}
=-\ell\{q_0,\kappa A_0-sB_0\}.
\tag{12}
\]
The binary map \(K_2\mapsto\{q_0,K_2\}\) has a literal \(3\times3\) minor
\(-8\) for both forms in (3). Since the polynomial ring is a domain and
\(\ell\ne0\), (12) therefore gives
\[
\kappa A_0=sB_0.
\tag{13}
\]
This reproduces the binary \(E_4\) restriction without division. The
decisive degree-six coefficients below are independent of (13), so every
coefficient of \(A\) and \(B\) may remain free in their calculation.

### The two double-root collisions

The generic minor (11) vanishes exactly on the two root lines, and the
kernels genuinely jump. Retain a nonzero scale \(c\) in \(\ell\).

For \(\ell=cx\), the complete rank-four kernel is
\[
\boxed{
V_0=\kappa x^2y+\frac23txy^2,\qquad
\bar L_3=cty.}
\tag{14}
\]
For \(\ell=cy\), it is
\[
\boxed{
V_0=\kappa x^2y+\frac13tx^3,\qquad
\bar L_3=ctx.}
\tag{15}
\]
On \(\ell=cx\), rows \((0,1,2,3)\) and columns \((0,2,3,4)\) give the
literal \(4\times4\) minor \(-54c^3\). On \(\ell=cy\), rows
\((1,2,3,4)\) and columns \((0,2,3,5)\) give \(108c^3\). These prove that
the two displayed directions are the full kernels on \(c\ne0\). The scale
\(c\) and the additional parameter \(t\) are not normalized away.

## 3. Four decisive raw \(E_6\) coefficients

Return to the complete determinant in (1), with (4), arbitrary lower
terms, and the applicable full kernel from Section 2.

On the squarefree branch (10), exact coefficient extraction gives
\[
\boxed{
[x^4yz]E_6=su,\qquad
[xy^4z]E_6=-sv.}
\tag{16}
\]
Since \(s\ne0\), the equations \(E_6=0\) force \(u=v=0\), contradicting
\(\ell\ne0\). This includes every squarefree root collision.

On the double-root noncollision branch (10), the corresponding coefficients
are
\[
\boxed{
[x^4yz]E_6=su,\qquad
[x^3y^2z]E_6=-2sv.}
\tag{17}
\]
Again \(E_6=0\) forces \(u=v=0\). In particular, no specialization of the
five moduli in (4) can rescue the branch.

It remains essential not to import (17) into the two larger collision
kernels. Substituting (14) and (15) separately gives
\[
\begin{array}{c|c}
\text{collision}&\text{raw degree-six coefficient}\\ \hline
\ell=cx&[x^4yz]E_6=sc,\\
\ell=cy&[x^3y^2z]E_6=-2sc.
\end{array}
\tag{18}
\]
Both are independent of \(t\). Since \(s,c\ne0\), each collision branch is
empty.

Equations (16)--(18) contain no lower-\(z\) coefficient of \(q\), no
coefficient of \(A,B\), no lower coefficient of \(V\), no \(\omega\), and
no unrestricted entry of the linear part. They arise before solving any of
those variables. No resultant, denominator clearing, or division by a
modulus occurs.

This proves the lemma. \(\square\)

## 4. Exact verification and scope

Run

```text
/usr/bin/python3 verify_vertical_nonzero_ell_nontriple_sympy.py
./verify_vertical_nonzero_ell_nontriple_strict.sh
```

The supplied checker starts from the raw \(3\times3\) Jacobian determinant.
It:

1. reconstructs (6) with all retained moduli;
2. proves the three squarefree rank charts, the double noncollision rank,
   and both complete collision kernels;
3. reconstructs (12) and the two constant \(-8\) bracket minors; and
4. extracts each coefficient in (16)--(18) while all unrelated variables
   remain symbolic.

The checker refuses optimized Python. It does not import or execute the
discovery-only `derive_vertical_generic_ell_coefficients_sympy.py` or
`explore_vertical_generic_ell_sympy.py` files.

The independent audit in
`audit_vertical_nonzero_ell_nontriple/REPORT.md` reconstructs the complete
raw and exterior \(E_5,E_6\) maps with a dependency-free sparse arithmetic
kernel, verifies all four kernel strata and the omitted \(W_0=0\) step,
and applies negative controls to the collision kernels and raw inputs. Run

```text
./audit_vertical_nonzero_ell_nontriple/verify_strict.sh
```

for that second implementation. Exact symbolic checks are evidence about
the encoded algebra, not peer review. This proof, audit, and their software
were produced with substantial AI assistance.
