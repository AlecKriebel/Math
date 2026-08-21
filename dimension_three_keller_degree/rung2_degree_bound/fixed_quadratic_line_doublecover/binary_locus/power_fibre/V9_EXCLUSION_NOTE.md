# Exclusion of the \(r^3\)-branch on the exceptional power fibre

**Exact candidate checkpoint:** 2026-07-25T11:58:42Z  
**Status:** pending an independent hostile audit; not peer reviewed.

## 1. Scope

Let \(p,q,r\) be source coordinates and translate the map so that its
constant term is zero.  Write
\[
F=L(p,q,r)^T+H_2+H_3+H_4,\qquad L\in\operatorname{GL}_3(\mathbb C),
\]
with each \(H_i\) homogeneous of degree \(i\).  This note treats only the
constant-dependent Hilbert--Burch exception in the binary
fixed-quadratic row:
\[
H_4=(p^4,p^2q^2,0),\qquad (H_3)_3=p^3.              \tag{1}
\]
It proves the following branch statement.

**Candidate lemma.**  On (1), there is no Keller map for which the
coefficient of \(r^3\) in \((H_3)_2\) is nonzero.

The coefficient is denoted \(v_9\) below.  The complementary branch
\(v_9=0\) is not treated here.

## 2. Full \(E_7\) solution

Put
\[
\det\!\left(L+zJH_2+z^2JH_3+z^3JH_4\right)
   =\sum_{j=0}^8 E_jz^j.                            \tag{2}
\]
The Keller condition requires \(E_j=0\) for \(j>0\).

Use binary forms
\[
\begin{aligned}
T_0&=c_0p^2+c_1pq+c_2q^2,&
U_0&=u_0p^3+u_1p^2q+u_2pq^2+u_3q^3,\\
A_0&=x_0p^2+x_1pq+x_2q^2,&
B_0&=y_0p^2+y_1pq+y_2q^2.
\end{aligned}
\]
The complete solution of \(E_7=0\) is
\[
\begin{aligned}
T&=(H_2)_3=T_0+r(t_p p+t_q q)+t_tr^2,\\
U&=(H_3)_1
  =U_0+\frac43rp(t_p p+t_q q)+\frac43t_tpr^2.       \tag{3}
\end{aligned}
\]
The other entries remain general:
\[
\begin{aligned}
V=(H_3)_2={}&v_0p^3+v_1p^2q+v_2pq^2+v_3q^3\\
 &+v_4p^2r+v_5pqr+v_6q^2r+v_7pr^2+v_8qr^2+v_9r^3,\\
A=(H_2)_1={}&A_0+r(a_p p+a_q q)+a_ar^2,\\
B=(H_2)_2={}&B_0+r(b_p p+b_q q)+b_br^2.             \tag{4}
\end{aligned}
\]
No lower coefficient has been specialized.

## 3. Consequences of \(E_6=E_5=0\) when \(v_9\ne0\)

The top \(r\)-coefficients give
\[
[r^3]E_6=\frac{16}{3}p^2q\,t_t^2,                  \tag{5}
\]
and, after \(t_t=0\),
\[
\begin{aligned}
[p^4r^2]E_6&=3v_9(3u_1-4c_1),\\
[p^3qr^2]E_6&=6v_9(3u_2-4c_2),\\
[p^2q^2r^2]E_6&=27v_9u_3.                          \tag{6}
\end{aligned}
\]
Thus
\[
t_t=0,\quad u_1=\frac43c_1,\quad
u_2=\frac43c_2,\quad u_3=0.                         \tag{7}
\]
The next identity is
\[
[r^4]E_5=-4t_qv_9(pt_p+qt_q),                      \tag{8}
\]
so \(t_q=0\).  Then \(E_6=0\) gives
\[
a_a=\frac29t_p^2,\qquad
a_q=\frac49c_1t_p,\qquad
a_p=\frac{12\ell_{33}+t_p(9u_0-8c_0)}9,\qquad
c_2t_p=0.                                           \tag{9}
\]
If \(t_p=0\), the \(q^3r^2\)-coefficient of \(E_5\) is
\(-8c_2^2v_9\); hence \(c_2=0\) in either case.  The remaining
\(r^2\)-coefficients of \(E_5\) give
\[
x_1=\frac43\ell_{32}
       -\frac{c_1(8c_0-9u_0)}9,\qquad
x_2=\frac29c_1^2+\frac{4t_p^3}{81v_9}.              \tag{10}
\]

## 4. The branch \(t_p\ne0\)

The source shear \(r\mapsto r+\alpha p+\beta q\), which preserves (1),
may be chosen to make \(c_0=c_1=0\).  It preserves both \(t_p\ne0\)
and \(v_9\ne0\).  The complete remaining solution of \(E_5=0\) then
contains
\[
\begin{aligned}
v_7&=-\frac{9\ell_{33}v_9}{t_p^2},&
v_8&=0,&
v_6&=\frac23t_p,&
v_5&=-\frac{9\ell_{32}v_9}{t_p^2},\\
\ell_{13}
 &=-\frac49\ell_{31}t_p+\ell_{33}u_0
   +\frac{4t_p^3v_4}{81v_9}+\frac23t_px_0.          \tag{11}
\end{aligned}
\]
After (7), (9)--(11), a single necessary coefficient is
\[
[r^3]E_4=-\frac8{27}q\,t_p^4,                      \tag{12}
\]
which cannot vanish.

## 5. The branch \(t_p=0\)

Equation \(E_5=0\) now gives
\[
c_1\ell_{33}=0,\qquad
\ell_{13}=\ell_{33}\!\left(u_0-\frac89c_0\right).   \tag{13}
\]

If \(c_1\ne0\), then \(\ell_{33}=\ell_{13}=0\), while
\[
[q^2r^2]E_4=\frac43c_1^3v_9\ne0.                   \tag{14}
\]

It remains to take \(c_1=0\).  Successive necessary coefficients of
\(E_4\) give
\[
\ell_{12}=\ell_{32}\!\left(u_0-\frac89c_0\right),
\qquad
[r]E_4=\frac83p^2q\,\ell_{33}^2,                   \tag{15}
\]
so \(\ell_{33}=\ell_{13}=0\).  Finally,
\[
[r^2]E_3=-\frac23\ell_{32}v_9
\left(
8c_0^2p-9c_0u_0p-6\ell_{31}p
+6\ell_{32}q+9x_0p
\right).                                            \tag{16}
\]
If \(\ell_{32}\ne0\), the bracket in (16) cannot vanish because its
\(q\)-coefficient is \(6\ell_{32}\).  If \(\ell_{32}=0\), then
\[
\ell_{12}=\ell_{13}=\ell_{32}=\ell_{33}=0,
\]
so the first and third rows of \(L\) are both supported only in their
first column.  Hence \(\det L=0\), contrary to the Keller condition.

The cases \(t_p\ne0\) and \(t_p=0\) exhaust \(v_9\ne0\), proving the
candidate lemma.

## 6. Exact certificate and disclosure

`verify_power_fibre_v9_sympy.py` reconstructs the full determinant (2),
retains all coefficients in (3)--(4), checks the forced relations
(5)--(11), and verifies the obstructions (12), (14), and (16) exactly
over \(\mathbb Q\).

This note and its verification code were produced with AI assistance.
The exact calculation is evidence about the encoded algebra, not peer
review.  The statement remains explicitly provisional until an
independent hostile reconstruction has checked completeness, legal
normalizations, coefficient conventions, and scope.
