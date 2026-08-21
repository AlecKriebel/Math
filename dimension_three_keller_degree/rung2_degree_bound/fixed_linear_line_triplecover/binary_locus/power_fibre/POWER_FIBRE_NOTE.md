# The binary fixed-linear power fibre contains no Keller counterexample

**Exact candidate checkpoint:** 2026-07-25T12:48:06Z  
**Status:** complete primary proof; pending independent hostile audit; not peer
reviewed.

## 1. Statement

Let
\[
F=L(p,q,r)^T+H_2+H_3+H_4,\qquad L\in\operatorname{GL}_3(\mathbb C),
\]
be a degree-four Keller map with zero constant term.  This note treats the
power-fibre exception in the binary fixed-linear line-triple-cover row.
After leading source and target changes, it is
\[
H_4=(p^4,pC_3(p,q),0),\qquad (H_3)_3=p^3,          \tag{1}
\]
where \(C_3\) is a binary cubic coprime to \(p^3\).

**Candidate theorem.**  Every Keller map on (1) is a polynomial
automorphism.  Equivalently, the binary fixed-linear power fibre contains
no Keller counterexample.

## 2. Normalization and the complete \(E_7\) solution

Coprimality says that the \(q^3\)-coefficient of \(C_3\) is nonzero.  A
source shear preserving \(p\), followed by a target scaling, gives
\[
C_3=d_0p^3+d_1p^2q+q^3,\qquad
D=(C_3)_q=d_1p^2+3q^2.                              \tag{2}
\]
No restriction is placed on \(d_0,d_1\).

Write
\[
\det(L+zJH_2+z^2JH_3+z^3JH_4)=\sum_{j=0}^8E_jz^j.
\]
Put \(L=(\ell_{ij})\), and write
\[
\begin{aligned}
T_0&=c_0p^2+c_1pq+c_2q^2,&
U_0&=u_0p^3+u_1p^2q+u_2pq^2+u_3q^3,\\
A_0&=x_0p^2+x_1pq+x_2q^2,&
B_0&=y_0p^2+y_1pq+y_2q^2.
\end{aligned}
\]
The top multipliers are
\[
\alpha=-3p^3D,\qquad \beta=0,\qquad \gamma=4p^4D.
\]
Thus the complete \(E_7=0\) solution is
\[
\begin{aligned}
(H_2)_3&=T_0+r(t_p p+t_q q)+t_t r^2,\\
(H_3)_1&=U_0+\frac43rp(t_p p+t_q q)+\frac43t_tpr^2,  \tag{3}
\end{aligned}
\]
while \((H_3)_2\) remains general:
\[
(H_3)_2=V_0+r(v_4p^2+v_5pq+v_6q^2)
+r^2(v_7p+v_8q)+v_9r^3.                            \tag{4}
\]
The other quadratic entries remain general:
\[
\begin{aligned}
(H_2)_1&=A_0+r(a_p p+a_q q)+a_ar^2,\\
(H_2)_2&=B_0+r(b_p p+b_q q)+b_br^2.
\end{aligned}
\]

## 3. Exclusion of \(v_9\ne0\)

The first forcing coefficients are
\[
[r^3]E_6=\frac83pt_t^2D,\qquad
[r^4]E_5=-4t_qv_9(pt_p+qt_q).                      \tag{5}
\]
Since \(D\ne0\), \(t_t=t_q=0\).  The remaining top coefficients give
\[
u_1=\frac43c_1,\quad u_2=\frac43c_2,\quad u_3=0,
\quad a_a=\frac29t_p^2.                             \tag{6}
\]
Then
\[
[r^0]E_6=\frac13p^2D
\left\{
-9a_p p^2-9a_qpq-8c_0p^2t_p+4c_1pqt_p+4c_2q^2t_p
+12\ell_{33}p^2+9p^2t_pu_0
\right\}.                                           \tag{7}
\]
Equation (7) fixes \(a_p,a_q\) and gives \(c_2t_p=0\).
The \(q^3\)-coefficient of \([r^2]E_5\) is
\(-8c_2^2v_9\), so \(c_2=0\); its \(pq^2\)-coefficient is then
\(-4t_p^3/3\), so \(t_p=0\).

The remaining \(E_5\) equations fix
\[
x_1=\frac43\ell_{32}
-\frac{c_1(8c_0-9u_0)}9,\qquad x_2=\frac29c_1^2,  \tag{8}
\]
and give
\[
c_1\ell_{33}=0,\qquad
\ell_{13}=\ell_{33}\!\left(u_0-\frac89c_0\right).  \tag{9}
\]
Now
\[
[q^2r^2]E_4=\frac43c_1^3v_9,                       \tag{10}
\]
so \(c_1=0\).  The remaining \(r^2\)-coefficient of \(E_4\) gives
\[
\ell_{12}=\ell_{32}\!\left(u_0-\frac89c_0\right).
\]
The next necessary identity is
\[
[r]E_4=\frac43\ell_{33}^2pD,                       \tag{11}
\]
hence \(\ell_{33}=\ell_{13}=0\).  Finally,
\[
[r^2]E_3=-\frac23\ell_{32}v_9
\left(8c_0^2p-9c_0u_0p-6\ell_{31}p
+6\ell_{32}q+9x_0p\right).                         \tag{12}
\]
Thus \(\ell_{32}=0\); the first and third rows of \(L\) are then both
supported in the first column.  This contradicts \(\det L\ne0\).

## 4. Exclusion of \(v_9=0\) with nonzero \(r^2\)-coefficient

Put
\[
\ell=v_7p+v_8q\ne0.
\]
The \(q^4\)-coefficient of \([r]E_6\) gives \(t_q=0\).
Coefficient comparison, separately on \(v_8\ne0\) and
\(v_8=0,v_7\ne0\), gives exactly (6).  Equation (7) remains valid.
Together with \(c_2t_p=0\), the coefficient
\[
[pq^2r^2]E_5
=-\frac43t_p(3c_2v_8+t_p^2)                       \tag{13}
\]
forces \(t_p=0\).

Now
\[
[r]E_5=\frac23\ell K,                              \tag{14}
\]
where
\[
\begin{aligned}
K={}&(8c_0c_1-9c_1u_0-12\ell_{32}+9x_1)p^3\\
 &+(16c_0c_2-4c_1^2-18c_2u_0+18x_2)p^2q\\
 &-12c_1c_2pq^2-8c_2^2q^3.
\end{aligned}
\]
Since the polynomial ring is a domain and \(\ell\ne0\), \(K=0\).
Consequently \(c_2=0\) and (8) holds.  The constant-\(r\) part of
\(E_5\) is \(p^2D/3\) times the linear factor in (9), so (9) follows
again.

If \(v_8\ne0\), then
\[
[q^3r]E_4=\frac89c_1^3v_8,
\]
so \(c_1=0\); next \([pq^2r]E_4=4\ell_{33}^2\).
If \(v_8=0,v_7\ne0\), (9) gives
\(c_1\ell_{33}=0\), while
\[
[pq^2r]E_4=\frac49
\left(2c_1^3v_7+3c_1\ell_{33}v_6+9\ell_{33}^2\right).
\]
This also forces \(c_1=\ell_{33}=0\).  In either case the remaining
\(E_4\) relation fixes
\[
\ell_{12}=\ell_{32}\!\left(u_0-\frac89c_0\right),
\]
and \([r]E_3\) contains respectively
\[
-\frac83\ell_{32}^2v_8q^2
\quad\text{or}\quad
-\frac83\ell_{32}^2v_7pq.
\]
Thus \(\ell_{32}=0\), and \(L\) is singular.  No Keller map lies on
this branch.

## 5. The zero \(r^2\)-coefficient and the automorphism exits

It remains to take
\[
v_9=v_7=v_8=0.
\]
The top equations give \(t_q=0,a_a=2t_p^2/9\), followed by
\[
[r^2]E_5=-\frac49pt_p^3D.                          \tag{15}
\]
Hence \(t_p=t_q=t_t=a_a=0\).

The third component is
\[
F_3=\ell_{33}r+G(p,q),\qquad
G=p^3+c_0p^2+c_1pq+c_2q^2+\ell_{31}p+\ell_{32}q.  \tag{16}
\]
If \(\ell_{33}\ne0\), the triangular coordinate \(w=F_3\) eliminates
\(r\) and leaves a plane Keller map over \(\mathbb C(w)\) of degree at
most \(6\).

If \(\ell_{33}=0\), \(G\) has no critical point, since a critical point
would make the full Jacobian determinant vanish.  Solving \(G_q=G_p=0\)
shows:

- \(c_2\ne0\) always gives a critical point;
- \(c_2=0,c_1\ne0\) always gives a critical point;
- therefore \(c_1=c_2=0\) and \(\ell_{32}\ne0\).

Thus \(w=G\) is a triangular coordinate replacing \(q\).  The remaining
plane map in \(p,r\) has degree at most \(10\); the ceiling comes from
the term \(pC_3(p,q)\) after the degree-three substitution for \(q\).

Both \(6\) and \(10\) are far below the established unconditional plane
counterexample bound: Guccione--Guccione--Horruitiner--Valqui
(`arXiv:2204.14178`) prove over every algebraically closed
characteristic-zero field that a nonautomorphic plane Keller map cannot
have either of these degrees.  After base change to
\(\overline{\mathbb C(w)}\), the plane map has generic degree one.
Hence \(F\) is birational, and the classical birational Keller theorem
makes \(F\) a polynomial automorphism.  This uses a proved finite plane
degree bound, not the unresolved plane Jacobian Conjecture.

## 6. Verification and disclosure

`verify_general_power_fibre_sympy.py` reconstructs the full determinant,
checks every forcing coefficient above, retains the moduli \(d_0,d_1\),
and symbolically verifies the plane degree ceilings \(6\) and \(10\).
Independently, `verify_general_power_fibre_pari.gp` rebuilds the Jacobian
and weighted determinant directly in PARI/GP, replays all three branch
terminals, guards the \(d_1\)-modulus and a sign mutation, and recomputes
both plane degrees.  `verify_general_power_fibre_strict.sh` requires both
engines and rejects optimized Python before accepting the suite.

The scripts verify the encoded algebra and degree counts.  They do not
prove the cited plane lower bound or birational Keller theorem.  This work
was produced with AI assistance, is not peer reviewed, and remains a
candidate until an independent hostile audit has checked normalization
completeness, all zero divisors, and both automorphism exits.
