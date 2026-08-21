# Exact marked-double exclusion in the fixed-linear \(\delta=2\) row

**Candidate checkpoint:** 2026-07-25T15:01:52Z  
**Status:** complete primary proof with exact dual-CAS checks; independent
hostile audit pending; not peer reviewed.

## 1. Statement

Let
\[
H_4=(P,Q,0)=(pA(p,q),pB(p,q),0),
\qquad \gcd(A,B)=1,
\]
where \(A/B\) has degree three, and put \(R=(H_3)_3\).  Define
\[
\alpha=J(Q,R),\qquad \beta=-J(P,R),\qquad
\gamma=J(P,Q),\qquad
g=\gcd(\alpha,\beta,\gamma).
\]

**Candidate theorem.**  No quartic Keller counterexample in the binary
fixed-linear line-triple-cover row has
\[
g\sim p^2.
\]
In other words, the entire exact-\(\delta=2\) component supported twice
on the marked fixed divisor is excluded.

This is one component of the fixed-linear \(\delta=2\) row, not an
exclusion of every \(\delta=2\) divisor and not a universal quartic
degree bound.

## 2. Normal forms and the Hilbert--Burch shape

Because \(A,B\) are coprime, a target change puts
\[
\begin{aligned}
A&=a_0p^3+a_1p^2q+a_2pq^2,\\
B&=b_0p^3+b_1p^2q+b_2pq^2+q^3.                    \tag{1}
\end{aligned}
\]
Write
\[
R=c_0p^3+c_1p^2q+c_2pq^2+c_3q^3.
\]
In the normalization (1),
\[
[p^0]\alpha=3c_3q^5,\qquad
[p^1](\alpha|_{c_3=0})=-c_2q^4.
\]
Thus
\[
p^2\mid\alpha,\beta,\gamma
\quad\Longleftrightarrow\quad
R=p^2(cp+dq).                                      \tag{2}
\]
The parabolic source group preserving \(p=0\), followed by a scaling,
leaves two forms:
\[
R=p^2q,\qquad R=p^3.                               \tag{3}
\]

For either form define
\[
\begin{aligned}
N_1&=\frac1p(P_q,Q_q,R_q)^T,\\
N_2&=\frac1p\left((P_p,Q_p,R_p)^T-\frac q3N_1\right).
                                                               \tag{4}
\end{aligned}
\]
Both are polynomial columns of component degrees \((2,2,1)\), and
\[
\begin{pmatrix}P_p&P_q\\Q_p&Q_q\\R_p&R_q\end{pmatrix}
=
\begin{pmatrix}N_1&N_2\end{pmatrix}
\begin{pmatrix}q/3&p\\p&0\end{pmatrix}.             \tag{5}
\]
The determinant on the right is \(-p^2\).  On the exact open
\(g\sim p^2\), wedging (5) proves that \(N_1,N_2\) are a minimal
Hilbert--Burch basis.  Consequently the splitting is necessarily
\[
\boxed{\{k_1,k_2\}=\{1,1\}},                        \tag{6}
\]
not the other nominal \(\delta=2\) splitting \(\{2,0\}\).

The degree-seven identity therefore has
\[
(U_r,V_r,W_r)^T=\kappa N_1+\tau N_2.               \tag{7}
\]
If \(\kappa=\tau=0\), the injective degree-six block makes every
nonlinear term binary.  The map is then a plane Keller map of degree at
most four together with a shear, hence an automorphism by the
unconditional plane low-degree theorem.  It remains to exclude a
nonzero tangent.

## 3. The form \(R=p^2q\)

The coefficient of \(r\) in the degree-six identity requires the
curvature contact
\[
K(\kappa N_1+\tau N_2)=\lambda\alpha+\mu\beta.       \tag{8}
\]
Its last two binary coefficients are
\[
[q^5](8)=-\frac{20}{9}a_2\tau^2,\qquad
[pq^4](8)=\frac{40}{3}\tau(a_1\tau+a_2\kappa).
                                                               \tag{9}
\]

### 3.1 \(a_2\ne0\)

Equation (9) gives \(\tau=0\).  If \(\kappa\ne0\), the remaining
coefficients force
\[
\begin{aligned}
40a_0a_2+5a_1^2+4a_1a_2b_2-4a_2^2b_1&=0,\\
5a_0a_1+4a_0a_2b_2-4a_2^2b_0&=0.                  \tag{10}
\end{aligned}
\]
After (10), all three reduced minors have the further common quadratic
\[
G=4a_0p^2+a_1pq-2a_2q^2:                           \tag{11}
\]
\[
\begin{aligned}
\frac{\alpha}{p^2}
 &=\frac{G\{(5a_1+4a_2b_2)p+10a_2q\}}{4a_2^2},\\
\frac{\beta}{p^2}&=-pG,\\
\frac{\gamma}{p^2}
 &=\frac{G(10a_0p^2-5a_1pq-2a_2q^2)}{a_2}.
                                                               \tag{12}
\end{aligned}
\]
Since \(a_2\ne0\), \(G\ne0\).  Thus (8) with a nonzero tangent belongs
to \(\delta\ge4\), not exact \(\delta=2\).

### 3.2 \(a_2=0,\ a_1\ne0\)

The \(pq^4\)-coefficient gives \(\tau=0\); the next two coefficients
give \(\lambda=0\) and \(6a_1\kappa^2=0\).  Hence the tangent is zero.

### 3.3 \(a_2=a_1=0\)

Scale \(a_0=1\) and use \(Q\mapsto Q-b_0P\).  If \(\tau=0\), the
contact equations again give \(\kappa=0\).  If \(\tau\ne0\), they force
\[
b_1=-\frac{2}{75}b_2^2,\qquad
\kappa=-\frac{2}{45}b_2\tau.                       \tag{13}
\]
Put \(t=b_2\).  The degree-six identity uniquely fixes the two
\(r^2\)-coefficients of the first two quadratic components as
\[
\frac{14}{3}\tau^2,\qquad
\frac{32}{10125}t^3\tau^2.                         \tag{14}
\]
Now the maximal-\(r\) part of the degree-five identity is
\[
[r^2]E_5=
-\frac{4\tau^3}{30375}
\left(
404p^3t^3+3150p^2qt^2-27000pq^2t-118125q^3
\right).                                           \tag{15}
\]
In particular
\[
[q^3r^2]E_5=\frac{140}{9}\tau^3\ne0,               \tag{16}
\]
a contradiction.  Binary integration constants, the remaining
quadratic coefficients, and the linear part have lower \(r\)-order and
cannot alter (16).

## 4. The form \(R=p^3\)

Exactness already forces \(a_2\ne0\): if \(a_2=0\), then \(p^3\)
divides all three minors.  Equations (8) give \(\tau=0\).  A nonzero
\(\kappa\) then forces
\[
3a_1^2-4a_1a_2b_2+4a_2^2b_1=0.                    \tag{17}
\]
With
\[
L=a_1p+2a_2q,
\]
the reduced minors become
\[
\begin{aligned}
\frac{\alpha}{p^2}
 &=\frac{3pL\{(3a_1-4a_2b_2)p-6a_2q\}}{4a_2^2},\\
\frac{\beta}{p^2}&=3p^2L,\\
\frac{\gamma}{p^2}&=-\frac{L\,C_3(p,q)}{a_2^2}
                                                               \tag{18}
\end{aligned}
\]
for an explicit cubic \(C_3\).  Since \(a_2\ne0\), \(L\ne0\), so (17)
raises the gcd degree to at least three.  It is disjoint from exact
\(\delta=2\).

The endpoint \(a_1=a_2=0\) is precisely the already separated power
fibre \(P\sim p^4,\ R\sim p^3\), and in any event has \(\delta>2\).

Every nonzero contact therefore either moves to a higher gcd stratum or
contradicts \(E_5\).  The zero-contact plane-plus-shear exit proves the
candidate theorem.

## 5. Verification and disclosure

`verify_marked_double_sympy.py` derives (2)--(18) from the raw
Jacobians.  Its \(E_5\) check retains completely general binary
integration constants, remaining quadratic terms, and linear part, so
the independence asserted in (16) is literal.

`verify_marked_double_pari.gp` independently reconstructs the divided
gradients, common factors, surviving contact family, degree-six solve,
and degree-five obstruction in PARI/GP.  The strict wrapper also checks
that optimized Python cannot bypass assertions.

These exact computations are evidence about the encoded algebra, not
peer review.  Normal-form coverage and the automorphism exit remain
subject to independent hostile checking.  AI systems materially
assisted the discovery, verification, and exposition.
