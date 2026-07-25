# The \(x^3+yz^2\), zero-\(\gamma\), zero-\(\ell\) vertical chart is impossible

**Recorded (UTC):** 2026-07-25T21:12:00Z.

**Status:** exact lemma, passed a dependency-free hostile audit.  It
excludes only the chart stated below; it does not close the frozen row
`Q2-E1-A3-B1-D1-N1`.

## Statement

Let a normalized quartic Keller candidate have
\[
H_4=(z^4,zq,0)^T,\qquad
H_3=\left(\frac43zW+s q,\ V,\ z^3\right)^T,\qquad
H_2=(A,B,W)^T,                                        \tag{1}
\]
where \(s\ne0\), and take the triple-root chart
\[
q=x^3+yz^2,\qquad W=wz^2.                              \tag{2}
\]
Then the Keller determinant identities force the linear part to be
singular.  Consequently this chart contains no Keller map.

Here \(w\) is arbitrary, including \(w=0\).  Every coefficient of the
quadratics \(A,B\), every allowed coefficient of the cubic \(V\), and
every entry of the linear matrix is initially retained.

## Normalization and scope

The triple-root parabolic atlas has three minimal charts.  Equation (2)
is its \(C=B=0,E\ne0\) chart.  A \(y\)-shear and an \(x\)-translation
remove the other coefficients of \(q\), and scaling normalizes the
\(yz^2\)-coefficient; there is no remaining modulus of \(q\).  These
operations only rescale the unrestricted coefficient \(w\).

The legal target shear which kills the independent \(bz^3\) summand in
the first cubic row changes \(A\) by a multiple of \(W\), and the shear
which kills the \(z^3\)-coefficient of \(V\) changes \(B\) by a multiple
of \(W\).  The constrained term
\(\frac43zW=\frac43wz^3\) remains in the first cubic row.
Thus they merely rename the retained \(z^2\)-coefficients \(a_5,b_5\).
No lower jet is specialized.

The hypothesis \(W=wz^2\) is precisely the
\(\gamma=0,\ell=0\) subcase after this normalization.  No claim is made
here about the other two triple-root charts, \(W_0\ne0\), or
\(\ell\ne0\).

## Proof

Write
\[
A=\sum_{i=0}^5a_i(x^2,xy,y^2,xz,yz,z^2)_i
\]
and write the constant linear matrix in row-major order as
\[
L=(\ell_{ij})_{1\le i,j\le3}.
\]
Put
\[
\lambda=\ell_{31},\qquad\mu=\ell_{32}.
\]
The legal \(E_7\) gauge removes the \(z^3\)-coefficient of \(V\).

### 1. Complete \(E_6\) solution

Let \(V\) initially have all nine remaining cubic coefficients.  The
\(E_6\) coefficient matrix in those nine coefficients and
\((\lambda,\mu)\) has rank eight.  A literal \(8\times8\) minor is
\[
-2^3\,3^{15}s^8.                                      \tag{3}
\]
The complete three-parameter solution is
\[
\boxed{
V=kq+\frac zs(A-a_5z^2)
       -\frac4{3s}z^2(\lambda x+\mu y).}               \tag{4}
\]
Indeed (4) annihilates every \(E_6\) coefficient and contains the three
free parameters \(k,\lambda,\mu\); together with (3), this is a rank
sandwich proving completeness.

### 2. The full \(E_5\) system kills both transverse entries

After (4), there are exactly seven nonzero \(E_5\) coefficients.  They
form a square linear system in
\[
(b_0,b_1,b_2,b_3,b_4,\lambda,\mu)
\]
with determinant
\[
\boxed{2^4\,3^8s^7.}                                  \tag{5}
\]
Since \(s\ne0\), its unique solution is
\[
\boxed{
\begin{aligned}
\lambda&=\mu=0,\\
b_0&=a_0k/s,&b_1&=a_1k/s,&b_2&=a_2k/s,\\
b_3&=(a_3k+\ell_{11})/s,&
b_4&=(a_4k+\ell_{12})/s.
\end{aligned}}                                        \tag{6}
\]

In particular, the apparently surviving parameter
\(\lambda=\ell_{31}\) is already eliminated by \(E_5\).  Concretely, the
coefficients of \(x^3z^2\) and \(yz^4\) are
\[
-9a_1k+9b_1s+\lambda s,\qquad
3a_1k-3b_1s+\lambda s.                                \tag{7}
\]
The first plus three times the second is \(4\lambda s\), so
\(\lambda=0\).  Separately, the coefficient of \(x^5\) is
\(-3\mu s\).

### 3. \(E_4\) makes the first two linear rows dependent

After (6), every \(E_4\) coefficient vanishes except
\[
\begin{aligned}
[x^2z^2]E_4&=9(-k\ell_{12}+s\ell_{22}),\\
[z^4]E_4&=-3(-k\ell_{11}+s\ell_{21}).
\end{aligned}                                         \tag{8}
\]
Their coefficient matrix in \((\ell_{21},\ell_{22})\) has determinant
\[
27s^2,
\]
and hence
\[
\ell_{21}=\frac{k}{s}\ell_{11},\qquad
\ell_{22}=\frac{k}{s}\ell_{12}.                        \tag{9}
\]

Together with \(\ell_{31}=\ell_{32}=0\), equation (9) gives
\[
\det L
=\ell_{33}(\ell_{11}\ell_{22}-\ell_{12}\ell_{21})
=0.                                                    \tag{10}
\]
But a Keller map has
\(\det L=\det JF(0)\ne0\).  This contradiction proves the lemma.
\(\square\)

## Verification and disclosure

Run

```text
./verify_vertical_triple_yz2_gamma0_ell0_strict.sh
./audit_vertical_triple_yz2_gamma0_ell0/verify_strict.sh
```

The strict runner executes:

- a SymPy reconstruction of the complete \(E_6\) matrix, the minors
  (3), (5), the unique \(E_5\) solve, all residual equations, (8), and
  \(\det L=0\);
- an independent PARI/GP exterior-multilinear reconstruction of
  \(E_6,E_5,E_4\), without forming the weighted determinant used by the
  SymPy verifier, including both pivot determinants and the decisive
  coefficients.

Neither verifier assumes \(w\ne0\) or \(k\ne0\).  Exact computer algebra
is evidence about the encoded identities, not peer review.  This note
and its verification were materially AI-assisted.  The independent
hostile reconstruction and its negative controls are documented in
`audit_vertical_triple_yz2_gamma0_ell0/REPORT.md`.
