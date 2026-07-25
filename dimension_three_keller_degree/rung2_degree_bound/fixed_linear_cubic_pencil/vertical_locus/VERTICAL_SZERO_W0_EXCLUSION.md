# The \(s=0,\ W_0=0\) vertical companion is impossible

**Status:** exact independent reconstruction, incorporated into the hostile
PASS in `audit_vertical_a0_w0_zero/REPORT.md`; not peer reviewed.
**Recorded (UTC):** 2026-07-25T22:18:00Z.

This note was produced with substantial AI assistance.  Exact symbolic
checks are evidence about the encoded algebra and are not peer review.

## 1. Statement

Let
\[
F=LX+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow\mathbb A^3_{\mathbb C}
\]
be a quartic Keller map on the triple-vertical fixed-linear cubic-pencil
row.  Use the complete vertical-companion gauge
\[
\begin{aligned}
H_4&=(z^4,zq,0)^T,\\
H_3&=(U,V,z^3)^T,\\
H_2&=(A,B,W)^T,
\end{aligned}                                                    \tag{1}
\]
where \(A,B,W\) are homogeneous quadratics, \(U,V\) are homogeneous
cubics, and \(L=(\lambda_{ij})\) is the linear part.  The degree-seven
identity gives
\[
U=\frac43zW+s q.                                       \tag{2}
\]

Assume
\[
\boxed{s=0,\qquad W_0:=W|_{z=0}=0.}                    \tag{3}
\]
Then \(F\) cannot be Keller.  More precisely, the identities
\[
E_6=E_5=E_4=0
\]
force either \(\det L=0\) or a literal contradiction.

The theorem covers:

1. the squarefree chart \(q_0=xy(x-y)\), with all six lower-\(z\)
   coefficients of \(q\) retained;
2. the double-root chart \(q_0=x^2y\), with the same coefficients retained;
3. all three minimal triple-root charts
   \[
   \begin{aligned}
   q_A&=x^3+y^2z+\alpha xz^2+\beta z^3,\\
   q_B&=x^3+xyz+\beta z^3,\\
   q_C&=x^3+yz^2+\beta z^3.
   \end{aligned}                                       \tag{4}
   \]

The harmless \(\beta z^3\) is retained, although a leading target shear can
remove it.  The second component \(B\), every coefficient of \(V\), and
every entry of \(L\) are unrestricted at the start.

## 2. Raw setup and the complete \(E_6\) solve

Write
\[
W=z(\ell+\omega z),\qquad \ell=\mu x+\nu y.             \tag{5}
\]
For the nontriple charts retain
\[
q=q_0+z(d_0x^2+d_1xy+d_2y^2)+z^2(e_0x+e_1y)+\beta z^3.
\tag{6}
\]
Put
\[
\mathcal J(t)=L+tJH_2+t^2JH_3+t^3JH_4,\qquad
E_j=[t^j]\det\mathcal J(t).                             \tag{7}
\]
With \(U=\frac43zW\), the identities \(E_8=E_7=0\) are automatic.

Starting with a general quadratic \(A\), coefficient comparison in \(E_6\)
has rank five on every chart.  It forces
\[
\boxed{
A=\frac29\ell^2+
z\left(\frac49\omega\ell+
\frac43(\lambda_{31}x+\lambda_{32}y)\right)+\eta z^2.
}                                                       \tag{8}
\]
Thus both the binary part \(A_0\) and the \(z\)-linear part of \(A\) are
fixed exactly.  No tail coefficient of \(q\) is divided out.

The following literal \(5\times5\) minors certify rank five:
\[
\begin{array}{c|c}
\text{chart}&\text{minor}\\ \hline
xy(x-y)&3888\\
x^2y&3888\\
q_A&-104976=-2^4 3^8\\
q_B&-8748=-2^2 3^7\\
q_C&-26244=-2^2 3^8.
\end{array}                                             \tag{9}
\]
The selected source monomials are recorded in the exact checker.  In
particular these ranks cannot drop at \(\alpha=0\), at any value of
\(\beta\), or on a lower-\(z\) tail divisor.

For comparison, the binary restriction of \(E_6\) alone allows an extra
\(\kappa x^2\) in \(A_0\) when \(q_0=x^3\).  The nonbinary term that makes
each chart in (4) minimal supplies the fifth constant pivot and forces
\(\kappa=0\).  This is why it is not valid to study the triple-root binary
restriction in isolation.

## 3. Complete \(E_5\) taxonomy

Substitute (8) into the full raw \(E_5\).

### 3.1 Squarefree and double-root charts

On the squarefree chart,
\[
[x^4z]E_5=\frac49\mu^3,\qquad
[y^4z]E_5=\frac49\nu^3.                                \tag{10}
\]
On the double-root chart,
\[
[x^4z]E_5=\frac49\mu^3,\qquad
[xy^3z]E_5=-\frac89\nu^3.                              \tag{11}
\]
Hence \(\ell=0\) on both.  The remaining equations are exactly
\[
\boxed{
\lambda_{11}=\frac49\omega\lambda_{31},\qquad
\lambda_{12}=\frac49\omega\lambda_{32}.
}                                                       \tag{12}
\]
Substitution of (12) makes every coefficient of \(E_5\) vanish, so no
unstated tail equation has been omitted.

### 3.2 The \(q_A\) chart

Here
\[
[x^2y^2z]E_5=-\frac43\nu^3.                            \tag{13}
\]
After \(\nu=0\),
\[
[x^2yz^2]E_5=\frac89\mu^3.                             \tag{14}
\]
Thus \(\ell=0\), and the residual solution is again exactly (12), uniformly
in \(\alpha,\beta\).

### 3.3 The \(q_B\) chart

Equation (13) still forces \(\nu=0\).  The \(\mu=0\) branch is exactly
(12).  If \(\mu\ne0\), four raw coefficients give the unique remaining
leaf
\[
\boxed{
\begin{aligned}
\lambda_{32}&=-\frac{\mu^2}{9},&
\lambda_{31}&=\frac{\mu\omega}{3},\\
\lambda_{12}&=-\frac{4\mu^2\omega}{81},&
\lambda_{11}&=
\frac{\mu(-12\lambda_{33}+18\eta-4\omega^2)}{27}.
\end{aligned}
}                                                       \tag{15}
\]
For clarity, the four equations before solving are
\[
\begin{aligned}
[x^3z^2]E_5&=\frac{4\mu}{9}(9\lambda_{32}+\mu^2),\\
[yz^4]E_5&=-\frac19(27\lambda_{12}-12\lambda_{32}\omega),\\
[x^2z^3]E_5&=-\frac19(
81\lambda_{12}+24\lambda_{31}\mu-36\lambda_{32}\omega
-8\mu^2\omega),\\
[xz^4]E_5&=\frac19(
27\lambda_{11}-12\lambda_{31}\omega+12\lambda_{33}\mu
-18\eta\mu+8\mu\omega^2).
\end{aligned}                                          \tag{16}
\]
Substitution of (15) annihilates the entire \(E_5\), with \(B,V,\beta\)
still symbolic.

### 3.4 The \(q_C\) chart

Again \(\nu=0\), and \(\mu=0\) returns (12).  The unique nonzero-\(\mu\)
leaf is
\[
\boxed{
\begin{aligned}
\lambda_{32}&=0,&
\lambda_{31}&=\frac{\mu\omega}{3},\\
\lambda_{12}&=\frac{4\mu^3}{81},&
\lambda_{11}&=
\frac{\mu(-12\lambda_{33}+18\eta-4\omega^2)}{27}.
\end{aligned}
}                                                       \tag{17}
\]
It follows from
\[
\begin{aligned}
[x^3z^2]E_5&=4\lambda_{32}\mu,\\
[x^2z^3]E_5&=-\frac19(
81\lambda_{12}-36\lambda_{32}\omega-4\mu^3),\\
[xz^4]E_5&=\frac{8\mu}{9}(-3\lambda_{31}+\mu\omega),\\
[z^5]E_5&=\frac19(
27\lambda_{11}-12\lambda_{31}\omega+12\lambda_{33}\mu
-18\eta\mu+8\mu\omega^2).
\end{aligned}                                          \tag{18}
\]
This substitution also annihilates all of \(E_5\).

Equations (10)--(18), together with their checked converses, are the frozen
finite survivor taxonomy after \(E_5\): one common zero-\(\ell\) leaf and
one nonzero-\(\mu\) leaf on each of \(q_B,q_C\).

## 4. \(E_4\) closes every leaf

### 4.1 The common zero-\(\ell\) leaf

On (12), chart-dependent literal square coefficients are:
\[
\begin{array}{c|c|c}
\text{chart}&\text{first square}&\text{second square}\\ \hline
xy(x-y)&[x^3z]E_4=-\frac43\lambda_{31}^2&
[y^3z]E_4=-\frac43\lambda_{32}^2\\
x^2y&[x^3z]E_4=-\frac43\lambda_{31}^2&
[xy^2z]E_4=\frac83\lambda_{32}^2\\
q_A&[x^2yz]E_4=4\lambda_{32}^2&
[xyz^2]E_4=-\frac83\lambda_{31}^2\\
q_B&[x^2yz]E_4=4\lambda_{32}^2&
[x^2z^2]E_4|_{\lambda_{32}=0}=-\frac43\lambda_{31}^2\\
q_C&[x^2yz]E_4=4\lambda_{32}^2&
[xz^3]E_4=-\frac43\lambda_{31}^2.
\end{array}                                             \tag{19}
\]
Characteristic zero gives
\[
\lambda_{31}=\lambda_{32}=0.
\]
Equation (12) then gives
\(\lambda_{11}=\lambda_{12}=0\).  The first and third rows of \(L\) are
both supported only in the third column:
\[
L_{1\bullet}=(0,0,\lambda_{13}),\qquad
L_{3\bullet}=(0,0,\lambda_{33}).
\]
Therefore \(\det L=0\).

### 4.2 The nonzero-\(\mu\) \(q_B\) leaf

Write
\[
\rho=[x^2y]V,\qquad \sigma=[y^2z]V.
\]
After (15), three coefficients are
\[
\begin{aligned}
c_{400}&=[x^4]E_4
=\frac{4\mu^3}{81}(\mu+9\rho),\\
c_{211}&=[x^2yz]E_4
=-\frac{4\mu^3}{27}(-\mu+\rho-6\sigma),\\
c_{022}&=[y^2z^2]E_4
=\frac{4\mu^3}{243}(\mu+18\sigma).
\end{aligned}                                          \tag{20}
\]
They satisfy the division-free identity
\[
\boxed{
81c_{400}+243c_{211}-729c_{022}=28\mu^4.
}                                                       \tag{21}
\]
Thus \(E_4=0\) forces \(\mu=0\), contradicting the defining branch.

### 4.3 The nonzero-\(\mu\) \(q_C\) leaf

Put \(\theta=[xyz]V\).  After (17),
\[
\begin{aligned}
c_{301}&=[x^3z]E_4
=\frac{4\mu^3}{81}(-2\mu+9\theta),\\
c_{013}&=[yz^3]E_4
=-\frac{4\mu^3}{27}(-\mu+\theta).
\end{aligned}                                          \tag{22}
\]
Now
\[
\boxed{
81c_{301}+243c_{013}=28\mu^4.
}                                                       \tag{23}
\]
Again \(E_4=0\) contradicts \(\mu\ne0\).

This exhausts all five root charts and every \(E_5\) leaf, proving the
theorem.

## 5. Verification

From this directory run

```text
sh verify_vertical_szero_w0_strict.sh
```

The SymPy implementation:

- builds the weighted determinant from the unrestricted raw jets;
- checks \(E_8=E_7=0\);
- verifies every constant rank-five minor and the complete \(E_6\) converse;
- detects a mutation of the \(2/9\) coefficient in \(A_0\);
- reconstructs all \(E_5\) branches and verifies every converse;
- verifies the ten square coefficients in (19); and
- verifies the division-free identities (21) and (23).

The PARI/GP implementation independently uses the exterior
row-polarization formula: it sums the \(4^3\) Jacobian determinants obtained
by choosing one homogeneous jet in each target row.  It rechecks all five
constant \(E_6\) minors, the full branch converses, the \(E_4\) squares, and
both \(28\mu^4\) identities without constructing the weighted Jacobian
determinant used by SymPy.

The strict wrapper requires the exact terminal markers

```text
PASS: s=0, W0=0 vertical companion excluded on 2 nontriple + 3 minimal triple-root charts
VERTICAL_SZERO_W0_PARI_PASS_C5E4A2
PASS: optimized-Python false-pass guard
```

It rejects PARI/GP diagnostics and refuses optimized Python so that the
Python checks cannot be disabled with `python -O`.

## 6. Scope boundary

This theorem closes exactly the \(s=0,\ W_0=0\) family.  It makes no claim
about \(s=0,\ W_0\ne0\), and it does not alter the already separate
\(s\ne0\) vertical-companion results.  No global frozen-row status is
changed by this note.
