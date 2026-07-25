# An Exact Barrier for Two-Point Linear Programming

This note proves that ordinary Delsarte linear programming, even at unbounded
degree with an absolutely convergent Schoenberg expansion, cannot establish
\(A(5,1/2)<41\).  It is a limitation theorem, not an upper bound and not a
spherical-code construction.

## Normalization

Let
\[
P_k(t)=\frac{C_k^{3/2}(t)}{C_k^{3/2}(1)}
\]
be the dimension-five zonal polynomials, so \(P_k(1)=1\).  They satisfy
\[
P_0(t)=1,\qquad P_1(t)=t,
\]
and, for \(k\geq2\),
\[
(k+2)P_k(t)=(2k+1)tP_{k-1}(t)-(k-1)P_{k-2}(t).
\tag{1}
\]

## Exact pseudo-distance distribution

Define the finite positive measure
\[
\mu=\delta_1+
 \frac{176}{41}\delta_{-77/100}
+\frac{262}{41}\delta_{-11/25}
+\frac{652}{41}\delta_{-9/100}
+\frac{550}{41}\delta_{499/1000}.
\tag{2}
\]
Its total mass is \(41\).  Every atom other than \(1\) lies strictly below
\(1/2\).  Moreover, the off-diagonal weights multiplied by \(41\) are the even
integers \(176,262,652,550\), whose sum is \(41\cdot40\).  Thus (2) passes the
elementary total-pair and ordered-pair parity checks for a 41-point distance
distribution.  It need not, and is not claimed to, arise from an actual code.

We prove
\[
M_k:=\int P_k(t)\,d\mu(t)>0
\qquad(k\geq1).
\tag{3}
\]

Exact rational evaluation using (1) gives
\[
M_k>\frac1{16}\qquad(1\leq k\leq53),
\]
with minimum
\[
M_2=\frac{1027}{16000}.
\tag{4}
\]
The standard-library verifier checks (4) and every rational comparison below.

For \(-1<t<1\), the Gegenbauer integral representation is
\[
P_k(t)=\frac2\pi\int_0^\pi
\left(t+i\sqrt{1-t^2}\cos\phi\right)^k\sin^2\phi\,d\phi.
\tag{5}
\]
This identity also follows directly by binomial expansion and beta-integral
evaluation.  Put \(q=1-t^2\).  Since
\[
\left|t+i\sqrt q\cos\phi\right|^2=1-q\sin^2\phi,
\]
the inequalities \(1-x\leq e^{-x}\) and
\[
\frac{2\phi}{\pi}\leq\sin\phi\leq\phi
\qquad(0\leq\phi\leq\pi/2)
\]
give
\[
\begin{aligned}
|P_k(t)|
&\leq \frac2\pi\int_0^\pi
e^{-kq\sin^2\phi/2}\sin^2\phi\,d\phi\\
&\leq \frac4\pi\int_0^\infty
\phi^2e^{-2kq\phi^2/\pi^2}\,d\phi\\
&=\frac{\pi^2\sqrt{2\pi}}{4(kq)^{3/2}}.
\end{aligned}
\tag{6}
\]

For the four nontrivial atoms \(t_i\), exact rational comparisons yield
\[
(1-t_i^2)^{-3/2}
<
\left(4,\frac75,\frac{51}{50},\frac{31}{20}\right)_i.
\]
Consequently
\[
\sum_iw_i(1-t_i^2)^{-3/2}
<\frac{129417}{2050}.
\tag{7}
\]
The classical identity
\[
0<\int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx=\frac{22}{7}-\pi
\]
proves \(\pi<22/7\).  Also \(44/7<(251/100)^2\), and direct rational
comparison gives
\[
\frac{\pi^2\sqrt{2\pi}}4<\frac{31}{5}.
\tag{8}
\]
Combining (6)--(8),
\[
\sum_iw_i|P_k(t_i)|
<
\frac{4011927}{10250\,k^{3/2}}
<
\frac{392}{k^{3/2}}.
\tag{9}
\]
Finally \(392^2<54^3\).  The right side of (9) is therefore strictly below
one for \(k\geq54\), and
\[
M_k\geq1-\sum_iw_i|P_k(t_i)|>0.
\]
Together with (4), this proves (3) for every degree.

## LP consequence

Let
\[
f(t)=\sum_{k=0}^d f_kP_k(t)
\]
be a Delsarte auxiliary polynomial satisfying
\[
f_0>0,\qquad f_k\geq0,\qquad
f(t)\leq0\quad(-1\leq t\leq1/2).
\]
By (3),
\[
\int f\,d\mu=\sum_{k=0}^df_kM_k\geq41f_0.
\]
All nontrivial atoms of \(\mu\) lie in the sign interval, so also
\[
\int f\,d\mu\leq f(1).
\]
Therefore \(f(1)/f_0\geq41\), and no such polynomial proves a strict upper
bound below 41.

The same argument applies to an infinite expansion with \(f_k\geq0\) and
\(\sum_kf_k=f(1)<\infty\): the standard bound \(|P_k(t)|\leq1\) gives uniform
absolute convergence and justifies termwise integration.  No assertion is made
for a merely formal or conditionally convergent series.

## What this does and does not eliminate

The witness has no atom at \(1/2\), so contact-count parity or upper-bound
constraints that permit zero contacts do not repair the ordinary two-point
relaxation.  This statement does **not** cover a universally proved positive
lower bound or a rowwise contact constraint.  A preliminary calculation also
suggests compatibility with Pfender's standard row-sum generators, but that
extension lies outside the theorem proved here pending a separate
source-normalization audit.

The measure (2) has not been extended to a three-point distribution.  It does
not address genuine three-point marginal consistency, local cap-occupancy
inequalities, or the rank-at-most-five Gram constraint.  Those are precisely
the types of information a successful upper bound must add.

## Reproduction

Run:

```sh
python3 verifiers/verify_two_point_barrier.py
python3 -m unittest tests.test_two_point_barrier -v
```
