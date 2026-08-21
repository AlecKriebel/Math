# Provisional exclusion of the \(\kappa=16/3\), \(\{2,0\}\) row

**Status:** exact SymPy and PARI/GP replays pass; hostile mathematical
audit pending.  This note is not peer reviewed.

**First recorded release (UTC):** 2026-07-25T12:25:43Z.

## Theorem

No Keller counterexample lies on the exact-\(\delta=2\),
\(\{k_1,k_2\}=\{2,0\}\) stratum consisting of one fixed-root incidence
and one ramification contact at orbit modulus \(\kappa=16/3\).

## 1. Rational orbit representative

Use
\[
h=3p^2+4pq+q^2=(p+q)(3p+q).                       \tag{1}
\]
Its invariant is \(4^2/(3\cdot1)=16/3\).  This is a diagonal-stabilizer
representative of the normalized interior orbit, not a new
normalization of the lower coefficients.

Choose the fixed root \(p+q\) and contact at \(p=0\).  Up to the
stabilizer and swap, the complete family is
\[
R=(p+q)(ap^2+2bpq+bq^2).                           \tag{2}
\]
The local valuation table in `DELTA2_HB_STRATIFICATION.md` gives the
exact open set
\[
b(a-b)(a+3b)\ne0.                                  \tag{3}
\]
The three factors respectively exclude the opposite ramification
contact, a doubled chosen root, and the other fixed root.

The \(r^1\) Hilbert--Burch column is
\[
N=(4p+q,\,-3q,\,a-b).                              \tag{4}
\]
Consequently the full integrated \(E_7\) family is
\[
\begin{aligned}
S&=\frac{k}{2}r^2+r(mp+nq),\\
H_3&=(U_0+(4p+q)S,\ V_0-3qS,\ R),\\
H_2&=(A_0+rA_1+x_5r^2,\ B_0+rB_1+y_5r^2,\
       T_0+(a-b)S),
\end{aligned}                                      \tag{5}
\]
with every binary lower coefficient and all nine entries of the linear
part retained.

## 2. Complete \(E_6\) solve

The earliest coefficient is
\[
[r^3]E_6=
6k^2(p+q)\{2apq+aq^2+3bp^2+4bpq+2bq^2\}.          \tag{6}
\]
Its \(p^2\)-coefficient inside braces is \(3b\ne0\), so
\[
k=0.                                               \tag{7}
\]

After (7), the endpoint coefficients of \([r]E_6\) are
\[
-12b(-3m^2+4y_5),\qquad12n^2(a+2b).                \tag{8}
\]
Thus \(y_5=3m^2/4\).

If \(a+2b\ne0\), equation (8) gives \(n=0\).  The four middle
coefficients are then a linear system in \(x_5\) and \(X=m^2\); a
decisive minor is
\[
192(a-b)(a+2b),                                    \tag{9}
\]
which is nonzero by (3) and the current case.  Hence
\(x_5=m=0\), and then \(y_5=0\).

On the divisor \(a=-2b\), no division is used.  Three middle
coefficients, after \(y_5=3m^2/4\), are proportional to
\[
\begin{aligned}
-3m^2+4x_5,\qquad
-21m^2+12n^2+28x_5,\qquad
-5m^2+4mn+4x_5.
\end{aligned}                                      \tag{10}
\]
They successively give \(x_5=3m^2/4\), \(n=0\), and \(m=0\).
Therefore in all cases
\[
m=n=x_5=y_5=0.                                     \tag{11}
\]

The constant part of \(E_6\) is now the homogeneous
\(\mathcal M_1\) system.  Its complete solution is
\[
A_1=\lambda(4p+q),\qquad
B_1=-3\lambda q,\qquad
\ell_{33}=\lambda(a-b).                            \tag{12}
\]
Two rank-four minors covering \(b\ne0\) are
\[
2304b^2(11a+25b),\qquad
20736b(a-5b)(a+2b).                                \tag{13}
\]

## 3. Final split

If \(\lambda=0\), \(E_5=0\) is a rank-two system in
\(\ell_{13},\ell_{23}\).  Covering minors include
\[
-432ab,\qquad-144b(a+2b).                          \tag{14}
\]
Since \(b\ne0\), they cannot vanish simultaneously.  Hence
\(\ell_{13}=\ell_{23}=0\); (12) also gives \(\ell_{33}=0\), so the
linear part has a zero third column.

If \(\lambda\ne0\), condition (3) gives \(a-b\ne0\), and
\[
F_3=\lambda(a-b)r+G_3(p,q).                        \tag{15}
\]
The triangular source change
\[
w=r+\frac{G_3}{\lambda(a-b)}
\]
makes the third component \(w\).  As in
`DELTA2_KAPPA16_EXCLUSION.md`, Section 4.2, the first two components
retain degree at most four in \(p,q\): their old \(r\)-coefficients are
binary affine-linear and are multiplied by \(G_3\) of degree at most
three.

Over \(\mathbb C(w)\) this is a plane Keller map of degree at most four.
The unconditional plane low-degree theorem gives generic degree one
after algebraic base change; generic degree descends, so the
three-variable map is birational.  The birational Keller theorem then
makes it a polynomial automorphism.  This uses no form of the full plane
Jacobian Conjecture.

The two values of \(\lambda\) exhaust the family, proving the theorem.

## 4. Verification and disclosure

Run
```sh
./verify_delta2_kappa16over3_exclusion_strict.sh
```
to replay the full determinant independently in SymPy and PARI/GP.
The scripts verify the encoded algebra, not the cited plane and
birational Keller theorems.

This proof was developed with AI assistance.  It is not peer reviewed,
and exact computer algebra is not peer review.
