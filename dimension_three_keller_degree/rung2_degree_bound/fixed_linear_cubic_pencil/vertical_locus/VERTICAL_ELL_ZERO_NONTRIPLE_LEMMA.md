# The zero-\(\ell\), nontriple vertical companion is impossible

**Recorded (UTC):** 2026-07-25T21:02:00Z.

**Status:** exact lemma, passed independent hostile audit at
2026-07-25T21:07:39Z.  This excludes a sublocus of the frozen row
`Q2-E1-A3-B1-D1-N1`; it does not exclude that row.

## Statement

Let a normalized quartic Keller candidate have
\[
H_4=(z^4,zq,0)^T,\qquad
H_3=\left(\frac43zW+s q,\ V,\ z^3\right)^T,\qquad
H_2=(A,B,W)^T,
\tag{1}
\]
where \(s\ne0\), \(A,B,W\) are quadratic, and the \(z^3\)-coefficient of
\(q\) and \(V\) has been killed by the legal target shears recorded in
`E8_E4_RANK_LEDGER.md`.  Suppose
\[
W=wz^2
\tag{2}
\]
and the binary cubic \(q_0=q|_{z=0}\) is squarefree or has one double root.
Then the determinant identities force the linear part to be singular.
Consequently this locus contains no Keller map.

After a binary source change, the two root types and all their retained
lower moduli are
\[
q_0=xy(x-y)\quad\text{or}\quad q_0=x^2y,
\tag{3}
\]
\[
q=q_0+z(r_{20}x^2+r_{11}xy+r_{02}y^2)
       +z^2(r_{10}x+r_{01}y).
\tag{4}
\]
No coefficient in (4) is assumed nonzero.

This is precisely the nontriple part of the exceptional \(\ell=0\) family
in the vertical-companion ledger.  The triple-root family and the
nonzero-\(\ell\) families remain outside the statement.

## Proof

Write
\[
A=\sum_{i=0}^5a_i(x^2,xy,y^2,xz,yz,z^2)_i
\]
and write the constant linear matrix in row-major order as
\[
L=(\ell_{ij})_{1\le i,j\le3}.
\]
For compactness put
\[
\lambda=\ell_{31},\qquad \mu=\ell_{32}.
\]

### 1. Complete degree-six solve

The source-degree-six part of
\[
\det(L+JH_2+JH_3+JH_4)
\tag{5}
\]
is linear in the nine coefficients of \(V\) and in \(\lambda,\mu\).
For each form in (3), its coefficient matrix has rank eight over
\(\mathbb C(s,r_{20},r_{11},r_{02},r_{10},r_{01})\).  More strongly, it
has a literal \(8\times8\) minor
\[
2^5 3^{11}s^8.
\tag{6}
\]
Hence its solution space has dimension three.  Direct substitution gives
three free parameters \(k,\lambda,\mu\) and the complete solution
\[
\boxed{
V=kq+\frac zs(A-a_5z^2)
      -\frac4{3s}z^2(\lambda x+\mu y).}
\tag{7}
\]
The constant minor proves completeness without dividing by any modulus of
\(q\).

### 2. Degree five kills the transverse linear row

Substitute (7) into the source-degree-five identities.  In the squarefree
case, the coefficients of \(x^4y\) and \(xy^4\) are
\[
s\lambda,\qquad -s\mu.
\tag{8}
\]
In the double-root case, the coefficients of \(x^4y\) and \(x^3y^2\) are
\[
s\lambda,\qquad -2s\mu.
\tag{9}
\]
Since \(s\ne0\), both cases force
\[
\boxed{\lambda=\mu=0.}
\tag{10}
\]

The remaining degree-five equations are linear in the five coefficients
\(b_0,\ldots,b_4\) of \(B\).  Their matrix has the literal constant minor
\[
-2^4 3^5s^5.
\tag{11}
\]
They give
\[
\boxed{
\begin{aligned}
b_0&=a_0k/s,&b_1&=a_1k/s,&b_2&=a_2k/s,\\
b_3&=(a_3k+\ell_{11})/s,&
b_4&=(a_4k+\ell_{12})/s.
\end{aligned}}
\tag{12}
\]
The coefficients \(a_5,b_5,w\) remain arbitrary.

### 3. Degree four makes the first two linear rows dependent

After (10)--(12), two degree-four coefficients suffice.  In the squarefree
case, the coefficients of \(x^2z^2\) and \(y^2z^2\) give
\[
\ell_{21}=\frac{k}{s}\ell_{11},\qquad
\ell_{22}=\frac{k}{s}\ell_{12}.
\tag{13}
\]
In the double-root case, the same equations come from \(x^2z^2\) and
\(xyz^2\).

But (10) says that the third linear row begins with two zero entries.
Therefore
\[
\det L
=\ell_{33}(\ell_{11}\ell_{22}-\ell_{12}\ell_{21})
=0
\tag{14}
\]
by (13).  This contradicts the invertibility of the linear part of a
Keller map.  The claimed locus is empty. \(\square\)

## Scope and remaining frontier

The argument is uniform in every lower-\(z\) modulus of \(q\), all unused
coefficients of \(A,B,W,V\), and every entry of \(L\).  Its constant minors
do not introduce a hidden specialization divisor.

It does not cover:

1. the two double-root collision families with \(\ell\ne0\);
2. the generic nonzero-\(\ell\) family;
3. the triple-root family, including \(W_0\ne0\);
4. the \(s=0\) vertical-companion family.

The nonvertical companion \(G_3=q\) has a separate hostile-audited
exclusion.  The frozen row remains open.

## Exact check and disclosure

Run

```text
/usr/bin/python3 verify_vertical_ell_zero_nontriple_sympy.py
./audit_vertical_ell_zero_nontriple/verify_strict.sh
```

The script reconstructs (5) from raw polynomials for both root types,
checks the two literal minors, proves the three-parameter degree-six
solution by a rank sandwich, and verifies every displayed residual and the
final determinant-zero implication.  The hostile audit independently
reconstructs the same calculation with dependency-free sparse exact
arithmetic; its report is
`audit_vertical_ell_zero_nontriple/REPORT.md`.

This note and its computation were produced with substantial AI
assistance.  They are not peer review.  Exact symbolic checks are evidence
about the encoded algebra, not verification of the universal statement by
the mathematical community.
