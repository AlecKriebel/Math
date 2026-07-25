# Exceptional unmarked-double exclusion in the fixed-linear row

**Candidate checkpoint:** 2026-07-25T18:40:21Z
**Status:** complete primary proof on the full exceptional component, with
exact dual-CAS checks; independent hostile audit pending; not peer
reviewed.

## 1. Statement and normal form

Let
\[
H_4=(P,Q,0)=(pA(p,q),pB(p,q),0),\qquad R=(H_3)_3,
\]
and suppose
\[
\gcd(J(Q,R),-J(P,R),J(P,Q))\sim q^2,              \tag{1}
\]
where \(q=0\) is unmarked and is distinct from the fixed divisor
\(p=0\).

Normalize the value of the cubic pencil at \(q=0\).  The constant and
linear \(q\)-jets of the three minors force
\[
\begin{aligned}
A&=a_3q^3,\\
B&=p^3+b_1p^2q+b_2pq^2+b_3q^3,\\
R&=c_0\left(
p^3+\frac34b_1p^2q+
\left(\frac34b_2-\frac3{32}b_1^2\right)pq^2
\right)+c_3q^3.                                   \tag{2}
\end{aligned}
\]
Scale \(a_3=1\) and remove \(b_3\) by adding a multiple of \(A\) to
\(B\).

The exceptional Hilbert--Burch divisor is
\[
3b_1^2-8b_2=0.                                    \tag{3}
\]

**Candidate theorem.**  No quartic Keller counterexample satisfies
(1)--(3).

The complementary \(\{1,1\}\) component
\(3b_1^2-8b_2\ne0\) remains separate.

## 2. The exceptional tangent

Write \(b=b_1\), so
\[
\begin{aligned}
P&=pq^3,\\
Q&=p\left(p^3+bp^2q+\frac38b^2pq^2\right),\\
R&=c_0\left(p^3+\frac34bp^2q+\frac3{16}b^2pq^2\right)
   +c_3q^3.                                       \tag{4}
\end{aligned}
\]
Set
\[
N=\frac1{q^2}
\left(\partial_q-\frac b4\partial_p\right)(P,Q,R)^T.
\]
Then
\[
N=\left(
3p-\frac b4q,\,
-\frac3{16}b^3p,\,
-\frac3{64}(b^3c_0-64c_3)
\right)^T.                                        \tag{5}
\]
It is a syzygy of the three minors, and
\[
\begin{pmatrix}P_p&P_q\\Q_p&Q_q\\R_p&R_q\end{pmatrix}
=
\begin{pmatrix}N&(P_p,Q_p,R_p)^T\end{pmatrix}
\begin{pmatrix}0&q^2\\1&b/4\end{pmatrix}.          \tag{6}
\]
The change determinant is \(-q^2\); hence (5) is the degree-zero
Hilbert--Burch column and the splitting is \(\{2,0\}\).

The curvature of \(N\) is
\[
\begin{aligned}
C(N)=-\frac{3b}{2048}\big(&
3b^5c_0pq^2+12b^4c_0p^2q+16b^3c_0p^3\\
&-48b^3c_3q^3-768b^2c_3pq^2\\
&-3072bc_3p^2q-4096c_3p^3\big).                  \tag{7}
\end{aligned}
\]
For \(b\ne0\), it cannot vanish unless \(c_0=c_3=0\), which would make
\(R=0\).  Thus the \(r\)-part of the degree-seven multiplier is zero,
and every contact has
\[
S=(mp+nq)N.                                       \tag{8}
\]

## 3. Complete nonzero-contact solve

Put
\[
T=b^3c_0-256c_3.                                  \tag{9}
\]
The first two contact coefficients are
\[
-\frac{3b}{64}m^2T,\qquad
-\frac{3b}{256}m(3bm+8n)T.                       \tag{10}
\]
If \(T\ne0\), these and the remaining four equations give
\[
m=0,\qquad
\lambda=bn^2,\qquad
\mu=-\frac3{64}b^4n^2.                            \tag{11}
\]
If \(T=0\), then \(c_3=b^3c_0/256\) and \(c_0c_3\ne0\).  After the
values of \(\lambda,\mu\) in (11) are inserted, two remaining
coefficients are
\[
\frac9{16384}b^7c_0m^2,\qquad
\frac9{8192}b^7c_0mn,                             \tag{12}
\]
so (11) again holds.  Hence every nonzero contact is \(S=nqN\).

Retain every binary integration constant in \(H_3,H_2\), every
\(r\)-linear term in the first two components of \(H_2\), and the full
linear part.  None affects the \(r^2\)-coefficient of \(E_5\).  Its four
binary coefficients are
\[
\left(
\frac{3b n^3T}{64},\,
\frac{9b^2 n^3T}{256},\,
\frac{9b^3 n^3T}{1024},\,
-\frac{9b^4c_3n^3}{64}
\right).                                          \tag{13}
\]
For \(b n\ne0\), these cannot vanish simultaneously.  Indeed, the
first three force \(T=0\), while the last then forces \(c_3=0\), and
(9) would force \(c_0=0\).  Thus every nonzero contact is obstructed at
\(E_5\).

## 4. Zero contact

The shifted degree-six syzygy can retain
\[
(A_r,B_r,\ell_{33})=\eta N.                       \tag{14}
\]
If \(N_3\ne0\) and \(\eta\ne0\), the third component of the map has a
nonzero linear \(r\)-coefficient.  A triangular source change isolates
\(r\), and the remaining plane Keller map over \(\mathbb C(r)\) is
birational by the unconditional plane low-degree theorem.  The map is
therefore an automorphism.

It remains to consider \(N_3=0\), namely
\[
c_3=\frac1{64}b^3c_0.                             \tag{15}
\]
Here \(b c_0\ne0\), and diagonal scaling gives
\[
b=c_0=1,\qquad
R=\left(p+\frac14q\right)^3.                       \tag{16}
\]
Retain general binary cubics in the first two components of \(H_3\),
general binary quadratics in all components of \(H_2\), and a general
linear part with \(\ell_{33}=0\).  The six \(E_5\) equations are linear
and have rank six.  After solving them with all seven free parameters
retained, the coefficient of \(r\) in \(E_4\) is the literal polynomial
\[
\frac9{64}\eta^2
\left(p+\frac14q\right)^3.                         \tag{17}
\]
Thus \(\eta\ne0\) is impossible.  If \(\eta=0\), every nonlinear term
is binary; after composing with the inverse linear part, the map is a
plane Keller map plus a triangular shear and is an automorphism.

This excludes the open subchart \(b_1\ne0\).

## 5. The endpoint \(b_1=0\)

At \(b_1=0\), exact gcd \(q^2\) forces \(c_3\ne0\); otherwise all three
minors acquire an additional factor \(p^3\).  Scale \(c_3=1\) and put
\(d=c_0\).  The endpoint is
\[
 P=pq^3,\qquad Q=p^4,\qquad R=dp^3+q^3,           \tag{18}
\]
with minors
\[
 \alpha=12p^3q^2,\quad
 \beta=3q^2(3dp^3-q^3),\quad
 \gamma=-12p^4q^2.                               \tag{19}
\]
Their gcd is exactly \(q^2\), and the degree-zero Hilbert--Burch
direction is
\[
 N=(3p,0,3)^T.                                    \tag{20}
\]

Write \(U=(H_3)_1,V=(H_3)_2,T=(H_2)_3\).  After (19) is divided by
\(3q^2\), the complete \(E_7\) equation is
\[
 4p^3U_r+(3dp^3-q^3)V_r-4p^4T_r=0.               \tag{21}
\]
Since \(V_r\) has degree two, divisibility by \(p^3\) in (21) first
forces \(V_r=0\), and then \(U_r=pT_r\).  Consequently the complete
solution is parameterized by
\[
 f=mp+nq+\rho r,\qquad
 U_r=3pf,\quad V_r=0,\quad T_r=3f.                \tag{22}
\]

Retain all binary coefficients in \(H_3,H_2\), all six possible
\(r\)-dependent coefficients in the first two entries of \(H_2\), and
the full linear matrix \(L=(\ell_{ij})\).  Let \(u_3,v_3\) denote the
\(q^3\)-coefficients of the binary parts of \(U,V\), and set
\[
\begin{aligned}
C_3&=-3d\ell_{23}+3d\ell_{33}v_3
      -4\ell_{13}+4\ell_{33}u_3,\\
D_3&=-\ell_{23}+\ell_{33}v_3,\\
C_2&=-3d\ell_{22}+3d\ell_{32}v_3
      -4\ell_{12}+4\ell_{32}u_3,\\
D_2&=-\ell_{22}+\ell_{32}v_3.                    \tag{23}
\end{aligned}
\]
The three nonzero projective charts in \([m:n:\rho]\) are exhaustive.
The exact lower equations reduce as follows.

- If \(\rho\ne0\), the \(E_6\) coefficients force
  \(v_1=v_2=0\) and determine every \(r\)-dependent quadratic
  coefficient.  After the four lower \(E_5\) pivots,
  \[
  E_5=-3C_3p^3q^2+3D_3q^5,\qquad
  [r]E_4=3\rho C_2p^3-3\rho D_2q^3.              \tag{24}
  \]
- If \(\rho=0,m\ne0\), scale \(m=1\) and write \(n=t\).  One
  \(E_5\) coefficient first forces the remaining \(E_6\) parameter to
  zero.  The residual \(E_5\) is the first polynomial in (24), and
  after \(C_3=D_3=0\),
  \[
  E_4=3C_2(p^4+tp^3q)-3D_2(pq^3+tq^4).           \tag{25}
  \]
- If \(\rho=m=0,n\ne0\), scale \(n=1\).  The corresponding \(E_5\)
  pivot again removes the last \(E_6\) parameter.  After its four
  lower pivots,
  \[
  [r]E_4=-3C_3p^3+3D_3q^3.
  \]
  On \(C_3=D_3=0\), the remaining equation is
  \[
  E_4=3C_2p^3q-3D_2q^4.                           \tag{26}
  \]

Thus every nonzero chart forces \(C_3=D_3=C_2=D_2=0\).  Equations
(23) then say
\[
\begin{aligned}
(\ell_{13},\ell_{23},\ell_{33})
  &=\ell_{33}(u_3,v_3,1),\\
(\ell_{12},\ell_{22},\ell_{32})
  &=\ell_{32}(u_3,v_3,1).
\end{aligned}                                     \tag{27}
\]
The second and third columns of \(L\) are proportional, contradicting
\(\det L\ne0\).

Finally suppose \(m=n=\rho=0\).  The complete \(E_6\) solve is
\[
(A_r,B_r,\ell_{33})=\ell_{33}(p,0,1).             \tag{28}
\]
If \(\ell_{33}\ne0\), the third component is
\(\ell_{33}r+h(p,q)\), and the plane-field exit applies.  If
\(\ell_{33}=0\), every nonlinear term is binary, so invertibility of
\(L\) again isolates a coordinate and gives the same exit.  This
excludes the endpoint and proves the candidate theorem.

## 6. Verification and disclosure

`verify_unmarked_double_k20_sympy.py` reconstructs (2), the
determinant-\(q^2\) Hilbert--Burch basis, the curvature, all contact
coefficients, the full-lower independence in (13), and the rank-six
\(E_5\)/literal-\(E_4\) calculation in (17).  At \(b_1=0\), it also
certifies the rank-12 complete \(E_7\) system, retains every lower
coefficient, and checks all three projective charts (24)--(27) plus
the full zero-contact solve (28).

`verify_unmarked_double_k20_pari.gp` independently rebuilds every raw
Jacobian and determinant coefficient in PARI/GP and substitutes a
seven-parameter solution of the \(E_5\) system before checking (17).
It independently reconstructs the endpoint weighted determinant and
all four endpoint branches.
The strict wrapper rejects optimized Python or PARI runs that do not
reach their terminal certificate.

These checks are evidence about the encoded algebra, not peer review.
The normal-form quotient, projective chart exhaustion, and zero-contact
plane-field exit require hostile review.  AI systems materially assisted
this work.
