# Exclusion of the unmarked \(a_3=\tfrac12\) contact family

**Exact candidate checkpoint:** 2026-07-25T13:37:05Z  
**Status:** complete primary proof; pending independent hostile audit; not peer
reviewed.

## 1. Scope

This note treats one genuine contact component inside the unmarked
exact-\(\delta=1\) part of the binary fixed-linear row.  In normalized
coordinates its leading data are
\[
\begin{aligned}
P&=p\left(pq^2+\frac12q^3\right),\\
Q&=p\left(p^3+p^2q-\frac18q^3\right),\\
R&=p^3+\frac34p^2q+
   \left(4z+\frac18\right)pq^2+zq^3.              \tag{1}
\end{aligned}
\]
The common Hilbert--Burch divisor is \(q\).

**Candidate theorem.**  No Keller map has leading data (1) on the exact
\(\delta=1\) open.  Consequently this entire one-parameter contact family
contains no Keller counterexample.

This is not an exclusion of the other unmarked contact components.

## 2. Exact open and tangent

Put
\[
\alpha=J(Q,R),\qquad\beta=-J(P,R),\qquad
\gamma=J(P,Q).
\]
After division by \(q\),
\[
\frac{\gamma}{q}=-\frac12p^2(2p+q)^2(4p+q).       \tag{2}
\]
Evaluating \((\alpha/q,\beta/q)\) at its three possible roots gives
\[
\begin{array}{c|c}
\text{root}&(\alpha/q,\beta/q)\text{ after removing the fourth power}\\
\hline
p=0&(-3z/8,-3z/2)\\
q=-2p&(-6z,-24z)\\
q=-4p&(-5(64z-1)/4,-4(64z-1)).
\end{array}                                        \tag{3}
\]
Thus (1) has exact \(\delta=1\) precisely on
\[
z(64z-1)\ne0.                                      \tag{4}
\]

The divided directional gradient is
\[
N=q^{-1}\left(\partial_q-\frac14\partial_p\right)(P,Q,R),
\]
namely
\[
\begin{aligned}
N_1&=\frac18(16p^2+8pq-q^2),\\
N_2&=-\frac1{32}(24p^2+12pq-q^2),\\
N_3&=\frac1{32}(64z-1)(4p+q).                     \tag{5}
\end{aligned}
\]
It is the unique degree-one tangent on this stratum.  The contact identity
is
\[
K_N=\frac12\alpha-\frac5{32}\beta.
\]
If the tangent parameter is zero, the injective lower syzygy block gives
the all-binary plane exit.  On the nonzero branch, rescale the source
coordinate \(r\) so that the tangent parameter is \(1\).

## 3. Legal lower gauges

Write
\[
\begin{aligned}
U_0&=\sum_{i=0}^3u_ip^{3-i}q^i,&
V_0&=\sum_{i=0}^3v_ip^{3-i}q^i,\\
T_0&=t_0p^2+t_1pq+t_2q^2.
\end{aligned}
\]
Target shears by the third component set \(u_0=v_0=0\), since the
\(p^3\)-coefficient of \(R\) is \(1\).  A source shear
\(r\mapsto r+ap+bq\) changes \(T_0\) by a multiple of
\((ap+bq)N_3\).  Because of (4), this sets \(t_0=t_2=0\).
The target shears can then be repeated to restore \(u_0=v_0=0\).
No coefficient divisor other than the exact-open factors in (4) is used.

Let the first two entries of \(H_2\) be
\[
\begin{aligned}
A&=A_0+r(x_3p+x_4q)+x_5r^2,\\
B&=B_0+r(y_3p+y_4q)+y_5r^2.
\end{aligned}
\]
The complete \(E_6=0\) solution in this gauge is
\[
\begin{gathered}
v_1=-\frac38u_1,\qquad
t_1=\frac{64z-1}{16}u_1,\\
x_5=-\frac14,\qquad y_5=\frac5{64},\\
x_3=-u_1+2u_2,\quad
x_4=\frac{u_1-4u_2+48u_3}{16},\\
y_3=\frac{3u_1+16v_2}{8},\quad
y_4=-\frac{u_1+16v_2-192v_3}{64},\\
\ell_{33}=-\frac{64z-1}{32}u_1.                  \tag{6}
\end{gathered}
\]

## 4. The lower collapse

The coefficient of \(r\) in \(E_5\) has rank two and gives
\[
u_2=\frac34u_1+4u_3,\qquad
v_2=-\frac14u_1+4v_3.                             \tag{7}
\]
The constant-\(r\) coefficient then gives
\[
\begin{aligned}
x_0&=8(-\ell_{13}-2u_1u_3+2x_2),\\
x_1&=\frac14(-16\ell_{13}+u_1^2-16u_1u_3+32x_2),\\
y_0&=\frac1{16}(-128\ell_{23}-u_1^2-256u_1v_3+256y_2),\\
y_1&=\frac1{32}(-128\ell_{23}-3u_1^2-128u_1v_3+256y_2),\\
\ell_{31}&=\frac1{16}\left(64\ell_{32}+(64z-1)u_1^2\right).
                                                               \tag{8}
\end{aligned}
\]
All coefficients not displayed remain free.  The \(r\)-coefficient of
\(E_4\) now vanishes identically.  Put
\[
\begin{aligned}
M_1&=\ell_{11}-4\ell_{12}+2u_1\ell_{13},\\
M_2&=\ell_{21}-4\ell_{22}+2u_1\ell_{23}.
\end{aligned}
\]
The constant-\(r\) part of \(E_4\) is
\[
\frac1{256}\bigl(A_z(p,q)M_1+B_z(p,q)M_2\bigr),   \tag{9}
\]
where
\[
\begin{aligned}
A_z={}&(2048z+112)(p^4+p^3q)+(576z+30)p^2q^2\\
     &+(32z+1)pq^3-24zq^4,\\
B_z={}&384(p^4+p^3q)+(-512z+104)p^2q^2\\
     &+(-256z+4)pq^3-96zq^4.
\end{aligned}
\]
The determinant of their \(pq^3,q^4\) coefficients is
\(-9216z^2\), nonzero on (4).  Hence \(M_1=M_2=0\).
Equations (6) and (8) now give the literal kernel vector
\[
L\begin{pmatrix}1\\-4\\2u_1\end{pmatrix}
=\begin{pmatrix}M_1\\M_2\\0\end{pmatrix}=0.        \tag{10}
\]
The vector in (10) is nonzero, contradicting \(L\in\mathrm{GL}_3\).

## 5. Verification and disclosure

`verify_unmarked_half_sympy.py` reconstructs the full weighted
determinant with every undisplayed coefficient retained and checks
(2)--(10).  A separate PARI/GP replay is required by the strict wrapper.

Exact scripts certify the encoded algebra.  They do not prove the
normal-form classification outside this family, replace peer review, or
establish scholarly priority.  AI systems materially assisted the
discovery, verification, and exposition.
