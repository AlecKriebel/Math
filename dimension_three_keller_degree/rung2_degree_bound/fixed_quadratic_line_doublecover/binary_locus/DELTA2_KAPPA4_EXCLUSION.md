# Provisional exclusion of the doubled-root \(\kappa=4\), \(\{2,0\}\) row

**Status:** exact SymPy and PARI/GP replays pass; hostile mathematical
audit pending.  This note is not peer reviewed.

**First recorded release (UTC):** 2026-07-25T12:32:17Z.

## Theorem

No Keller counterexample lies on the exact-\(\delta=2\),
\(\{k_1,k_2\}=\{2,0\}\) sublocus of the doubled nonbranch fixed-root
orbit.

## 1. Complete normal form

Normalize
\[
h=(p+q)^2.
\]
The branch contact at \(p=0\) and the exceptional rank-drop equation
from `DELTA2_HB_STRATIFICATION.md` give
\[
\begin{aligned}
d&=\frac{5b-6a}{3},\\
R&=ap^3+bp^2q+\frac32d\,pq^2+dq^3.                 \tag{1}
\end{aligned}
\]
The exact open set is
\[
b(3a-2b)\ne0.                                      \tag{2}
\]
The swapped contact is conjugate under the squaring-cover stabilizer.

The Hilbert--Burch column is
\[
N=(6p+4q,\,-2q,\,6a-b).                            \tag{3}
\]
With
\[
S=\frac{k}{2}r^2+r(mp+nq),
\]
the full integrated \(E_7\) family is
\[
\begin{aligned}
H_3&=(U_0+(6p+4q)S,\ V_0-2qS,\ R),\\
H_2&=(A_0+rA_1+x_5r^2,\ B_0+rB_1+y_5r^2,\
       T_0+(6a-b)S),
\end{aligned}                                      \tag{4}
\]
with all binary lower coefficients and all entries of the linear part
retained.

## 2. Complete \(E_6\) solve

The first obstruction is
\[
\begin{aligned}
[r^3]E_6=-k^2\{&
6ap^3-18apq^2-12aq^3\\
&-4bp^3-18bp^2q-33bpq^2-22bq^3\}.
\end{aligned}                                      \tag{5}
\]
The \(p^2q\)-coefficient is \(18bk^2\), so (2) gives \(k=0\).

The endpoints of the remaining \([r]E_6\) equation are
\[
4(3a-2b)(-m^2+y_5),\qquad
4n^2(6a+11b).                                      \tag{6}
\]
Thus \(y_5=m^2\).

If \(6a+11b\ne0\), then \(n=0\).  The middle equations form a
rank-two system in \(x_5,X=m^2\).  One minor is
\[
4(6a+11b)(18a+b).                                  \tag{7}
\]
If \(18a+b=0\), a second minor specializes to
\(-124b^2/3\), so the rank remains two.  Hence \(x_5=m=0\).

If \(6a+11b=0\), the exact condition still has \(b\ne0\).  Three middle
equations are proportional to
\[
-4m^2+x_5,\qquad
-56m^2+9n^2+14x_5,\qquad
-59m^2+30mn+11x_5.                                 \tag{8}
\]
They give \(x_5=4m^2,n=0,m=0\).  Therefore in every case
\[
m=n=x_5=y_5=0.                                     \tag{9}
\]

The constant \(E_6\) equation has rank four on (2), with the single
polynomial kernel (3).  A literal nonzero minor is
\[
64b(3a-2b)^2.                                      \tag{10}
\]
Thus
\[
A_1=\lambda(6p+4q),\qquad
B_1=-2\lambda q,\qquad
\ell_{33}=\lambda(6a-b).                           \tag{11}
\]

## 3. Final branches

If \(\lambda=0\), \(E_5\) forces
\(\ell_{13}=\ell_{23}=0\).  Together with (11), the third column of the
linear part vanishes.  Rank two is guarded by
\[
12a(3a-2b),\qquad4(3a-2b)(9a+b).                   \tag{12}
\]

If \(\lambda(6a-b)\ne0\), the third component is
\[
F_3=\lambda(6a-b)r+G_3(p,q).
\]
The same triangularization and degree-four plane-field exit proved in
`DELTA2_KAPPA16_EXCLUSION.md`, Section 4.2, makes the map a polynomial
automorphism.  This uses the unconditional plane degree-\(\le4\)
theorem and the birational Keller theorem, not the full plane Jacobian
Conjecture.

The only residual branch is
\[
\lambda\ne0,\qquad a=\frac b6,\qquad b\ne0.         \tag{13}
\]
The complete rank-six \(E_5\) solution is
\[
\begin{aligned}
\ell_{13}&=\lambda\left(
-12u_0+14u_1-15u_2+\frac{27}{2}u_3\right),\\
\ell_{23}&=\lambda\left(
6u_0-5u_1+6u_2-6u_3+4v_1-3v_3\right),\\
t_0&=\frac14t_2,\qquad t_1=t_2,\\
v_0&=u_0-\frac56u_1+u_2-u_3+\frac56v_1-\frac12v_3,\\
v_2&=-\frac12u_2+\frac34u_3+\frac32v_3.
\end{aligned}                                      \tag{14}
\]
Its pivot determinant is
\[
-36864b^4\lambda^4.                                \tag{15}
\]
After (14),
\[
[r]E_4=6b\lambda^2(p+2q)^3\ne0,                   \tag{16}
\]
a contradiction.

These branches exhaust the locus, proving the theorem.

## 4. Verification and disclosure

Run
```sh
./verify_delta2_kappa4_exclusion_strict.sh
```
for exact SymPy and PARI/GP replays from the full determinant.

This proof was developed with AI assistance.  The work is not peer
reviewed, and exact algebra checks are not peer review.
