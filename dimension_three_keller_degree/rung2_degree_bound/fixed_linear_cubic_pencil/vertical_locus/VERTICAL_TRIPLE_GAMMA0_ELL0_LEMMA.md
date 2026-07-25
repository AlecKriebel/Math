# Every zero-\(\gamma\), zero-\(\ell\) triple-root vertical chart is impossible

**Recorded (UTC):** 2026-07-25T21:19:29Z.

**Status:** exact lemma, passed an independent dependency-free hostile
audit.  It excludes a sublocus of the frozen row
`Q2-E1-A3-B1-D1-N1`; it does not exclude that row.

This note subsumes the earlier one-chart calculation in
`VERTICAL_TRIPLE_YZ2_GAMMA0_ELL0_LEMMA.md`.

## Statement

Let a normalized quartic Keller candidate have
\[
H_4=(z^4,zq,0)^T,\qquad
H_3=\left(\frac43zW+s q,\ V,\ z^3\right)^T,\qquad
H_2=(A,B,W)^T,                                        \tag{1}
\]
where \(s\ne0\).  Suppose the binary restriction of \(q\) has one triple
root and
\[
W=wz^2.                                                \tag{2}
\]
Then no such candidate is a Keller map.

After the full triple-root parabolic normalization, and after killing the
\(z^3\)-coefficient of \(q\) as explained below, the complete minimal
atlas is
\[
\begin{aligned}
q_C&=x^3+y^2z+\alpha xz^2, &&\alpha\in\mathbb C,\\
q_B&=x^3+xyz,\\
q_E&=x^3+yz^2.
\end{aligned}                                         \tag{3}
\]
The proof is simultaneous on all three charts, including every value of
\(\alpha\) and \(w\).

## 1. Legality of the atlas

Before using target freedom, the three minimal triple-root source charts
are
\[
x^3+y^2z+\alpha xz^2+\beta z^3,\qquad
x^3+xyz+\beta z^3,\qquad
x^3+yz^2.
\]
On the **vertical** companion \((H_3)_3=z^3\), \(\beta\) is removable:
adding a multiple of the first target row to the second replaces
\(q\) by \(q-\beta z^3\).  This alters \(V,B\), and the second linear
row; in particular \(B\) is renamed by a multiple of \(A\), and all
these coefficients remain arbitrary.  Expressing the first cubic row in
the new \(q\) may create a \(z^3\)-term; adding the third target row to
the first removes it.  A final third-row shear removes the
\(z^3\)-coefficient of \(V\).  These last two shears change \(A,B\) by
multiples of \(W\), so they merely rename the unrestricted
\(z^2\)-coefficients of those quadratics.  The first-row shear kills the
free \(bz^3\) summand, not the constrained
\(\frac43zW=\frac43wz^3\) term.

Thus (3) loses no lower jet.  The modulus \(\alpha\) is not normalized or
assumed nonzero.  Likewise \(w\) is arbitrary, including zero.

Condition (2) is exactly the \(\gamma=0,\ell=0\) subcase of
\[
W_0=\gamma x^2,\qquad
W-W_0\in z\mathbb C[x,y]_1+\mathbb Cz^2.
\]
No claim is made here about \(\gamma\ne0\) or \(\ell\ne0\).

## 2. A common complete \(E_6\) solution

Write
\[
A=\sum_{i=0}^5a_i(x^2,xy,y^2,xz,yz,z^2)_i
\]
and write the linear matrix in row-major order as
\[
L=(\ell_{ij})_{1\le i,j\le3}.
\]
Set
\[
\lambda=\ell_{31},\qquad \mu=\ell_{32}.
\]
The legal \(E_7\) gauge removes the \(z^3\)-coefficient of \(V\), leaving
nine general cubic coefficients.

For each chart, the \(E_6\) matrix in those nine coefficients and
\((\lambda,\mu)\) has a literal \(8\times8\) minor:
\[
\begin{array}{c|c}
q&\text{\(E_6\) pivot}\\ \hline
q_C&-2^5\,3^{15}s^8\\
q_B& \phantom{-}2^3\,3^{14}s^8\\
q_E&-2^3\,3^{15}s^8.
\end{array}                                            \tag{4}
\]
In all three cases, direct substitution gives the same three-parameter
solution
\[
\boxed{
V=kq+\frac zs(A-a_5z^2)
       -\frac4{3s}z^2(\lambda x+\mu y).}               \tag{5}
\]
Every \(E_6\) coefficient vanishes after (5).  The nonzero minor (4) and
the three free parameters \(k,\lambda,\mu\) form a rank sandwich, proving
that (5) is the complete solution.  The pivots contain neither
\(\alpha\) nor \(w\), so there is no hidden modulus divisor.

## 3. \(E_5\) kills the whole transverse third row

After (5), take
\[
(b_0,b_1,b_2,b_3,b_4,\lambda,\mu)
\]
as unknowns.  The full \(E_5\) systems have the following literal
\(7\times7\) minors:
\[
\begin{array}{c|c}
q&\text{\(E_5\) pivot}\\ \hline
q_C&2^5\,3^9s^7\\
q_B&2^2\,3^8s^7\\
q_E&2^4\,3^8s^7.
\end{array}                                            \tag{6}
\]
Their unique common solution is
\[
\boxed{
\begin{aligned}
\lambda&=\mu=0,\\
b_0&=a_0k/s,&b_1&=a_1k/s,&b_2&=a_2k/s,\\
b_3&=(a_3k+\ell_{11})/s,&
b_4&=(a_4k+\ell_{12})/s.
\end{aligned}}                                        \tag{7}
\]
Every nonpivot \(E_5\) coefficient also vanishes after (7).

The elimination of the two potentially dangerous third-row entries is
visible without solving the matrices:
\[
\begin{array}{c|c|c}
q&\text{coefficient killing \(\mu\)}
 &\text{coefficient killing \(\lambda\)}\\ \hline
q_C &[x^5]E_5=-3s\mu &[x^3yz]E_5=2s\lambda\\
q_B &[x^5]E_5=-3s\mu &[x^4z]E_5=s\lambda\\
q_E &[x^5]E_5=-3s\mu
 &[x^3z^2]E_5+3[yz^4]E_5=4s\lambda.
\end{array}                                            \tag{8}
\]
Thus the \(\ell_{31}\) survivor seen in an incomplete coefficient
selection is not genuine: the full \(E_5\) system eliminates it.

## 4. \(E_4\) forces dependent linear rows

After (7), the complete nonzero \(E_4\) residual is:
\[
\begin{array}{c|l}
q& E_4\\ \hline
q_C&
9(-k\ell_{12}+s\ell_{22})x^2z^2
-6(-k\ell_{11}+s\ell_{21})yz^3
+3\alpha(-k\ell_{12}+s\ell_{22})z^4\\
q_B&
9(-k\ell_{12}+s\ell_{22})x^2z^2
-3(-k\ell_{11}+s\ell_{21})xz^3
+3(-k\ell_{12}+s\ell_{22})yz^3\\
q_E&
9(-k\ell_{12}+s\ell_{22})x^2z^2
-3(-k\ell_{11}+s\ell_{21})z^4.
\end{array}                                            \tag{9}
\]
Two displayed coefficients in each row give a \(2\times2\) pivot in
\((\ell_{21},\ell_{22})\), respectively
\[
2\cdot3^3s^2,\qquad 3^3s^2,\qquad 3^3s^2.              \tag{10}
\]
Hence every chart satisfies
\[
\ell_{21}=\frac{k}{s}\ell_{11},\qquad
\ell_{22}=\frac{k}{s}\ell_{12}.                        \tag{11}
\]
Together with \(\ell_{31}=\ell_{32}=0\), this makes
\[
\det L
=\ell_{33}(\ell_{11}\ell_{22}-\ell_{12}\ell_{21})
=0.                                                    \tag{12}
\]
But a Keller map has
\(\det L=\det JF(0)\ne0\), a contradiction.
\(\square\)

## 5. Verification and remaining frontier

Run

```text
./verify_vertical_triple_gamma0_ell0_strict.sh
./audit_vertical_triple_gamma0_ell0/verify_strict.sh
```

The SymPy verifier reconstructs the full weighted determinant, all three
complete \(E_6,E_5,E_4\) systems, every pivot in (4), (6), (10), every
residual equation, and the final singularity.

The PARI/GP verifier uses a methodologically different calculation.  It
does not form the weighted determinant.  Instead it reconstructs each
homogeneous identity by exterior multilinearity as a sum of Jacobian
triples, then verifies the same pivots and solutions.

The hostile audit independently rebuilds the three-chart atlas and the
calculation with dependency-free sparse exact arithmetic; its report is
`audit_vertical_triple_gamma0_ell0/REPORT.md`.

This lemma removes the \(\gamma=0,\ell=0\) part of the triple-root
vertical companion.  The following remain outside its scope:

- \(W_0=\gamma x^2\) with \(\gamma\ne0\);
- \(W_0=0\) with a nonzero \(z\)-linear form \(\ell\);
- the other vertical-companion rank families already listed in
  `E8_E4_RANK_LEDGER.md`;
- the \(s=0\) vertical companion.

Exact computer algebra is evidence about the encoded identities, not
peer review.  This note and its verification were materially
AI-assisted.
