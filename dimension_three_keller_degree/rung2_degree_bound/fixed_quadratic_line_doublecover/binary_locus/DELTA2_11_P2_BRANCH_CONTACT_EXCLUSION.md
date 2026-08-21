# Provisional exclusion of the \(h=p^2\), branch-contact
\(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T13:12:34Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## 1. Theorem and exact open

No Keller counterexample in the binary fixed-quadratic
line-double-cover row lies on
\[
h=p^2,\qquad
R=Ap^3+Cpq^2+Dq^3,\qquad D\ne0.                  \tag{1}
\]
This is the exact-\(\delta=2\), \(\{1,1\}\) mechanism consisting of
the baseline contribution at the doubled fixed root \(p=0\) and the
ramification contact at \(q=0\), with \(p\nmid R\).

Indeed, for \(P=p^4,Q=p^2q^2\),
\[
\gcd(J(Q,R),-J(P,R),J(P,Q))=2pq.                  \tag{2}
\]
The mutation \(D=0\) has gcd \(2p^2q\) and is routed to
\(\delta\ge3\).  The values \(A=0\) and \(C=0\) remain in (1) and are
treated separately below.

## 2. Generic contact injectivity

Put
\[
\Lambda=27AD^2+4C^3.
\]
On \(\Lambda\ne0\), a polynomial basis of the two \(E_7\) tangents is
\[
\begin{aligned}
N_1={}&(36D^2p^2,\,
4C^2p^2-6CDpq+18D^2q^2,\,\Lambda p),\\
N_2={}&(-24CDp^2,\,
18ADp^2+4C^2pq-12CDq^2,\,\Lambda q).              \tag{3}
\end{aligned}
\]
As in the companion simple-fixed-root proof, lift the coefficient of
\(r\) in \(E_6\) to a linear map
\[
\Theta:\ (X,Y,Z,x_5,y_5)\longmapsto S_5,\qquad
(X,Y,Z)=(s^2,st,t^2).                              \tag{4}
\]
The determinant of its first five coefficient rows is
\[
-71663616\,C^2D^6\Lambda^3.                       \tag{5}
\]
Thus \(\Theta\) is injective when \(CD\Lambda\ne0\), so every
\(r\)-dependent nonlinear coefficient vanishes.

The divisor \(\Lambda=0,C\ne0\) is recomputed from a fresh tangent
basis:
\[
\begin{aligned}
\widetilde N_1={}&\left(
2p^2,\frac{2C^2}{9D^2}p^2-\frac{C}{3D}pq+q^2,0
\right),\\
\widetilde N_2={}&\left(
0,\frac{2}{3D}p^2,\frac{2C}{3D}p+q
\right).
\end{aligned}                                      \tag{6}
\]
The corresponding determinant is
\[
-12288C^2.                                         \tag{7}
\]
Hence the pivot divisor introduces no contact survivor.

## 3. The \(C=0\) split

Suppose first that \(C=0\) and \(AD\ne0\).  A tangent basis is
\[
\left(\frac4{3A}p^2,\frac2{3A}q^2,p\right),\qquad
\left(0,\frac2{3D}p^2,q\right).                    \tag{8}
\]
The lifted contact matrix has rank four; a decisive minor is
\[
\frac{8192}{9A^2}.
\]
Its kernel is spanned by
\[
(0,9AD/4,0,0,1),
\]
whose Veronese obstruction is
\[
Y^2-XZ=\frac{81}{16}A^2D^2\ne0.                  \tag{9}
\]
Thus no actual tangent survives.

At the endpoint \(A=C=0\), so \(R=Dq^3\), the contact matrix has rank
three and kernel
\[
\left\langle
(1,0,0,1,0),\ (0,3D/2,0,0,1)
\right\rangle.                                    \tag{10}
\]
For \(\lambda K_1+\mu K_2\), the Veronese equation is
\[
\frac94D^2\mu^2=0.
\]
Therefore exactly one contact line remains:
\[
\begin{aligned}
(U_r,V_r,T_r)&=k(2p^2,q^2,0),\\
([r^2]H_{2,1},[r^2]H_{2,2})&=(k^2,0).             \tag{11}
\end{aligned}
\]
The \(k=0\) branch is the established all-binary automorphism exit.

## 4. Complete lower solve at \(R=Dq^3\)

Retain arbitrary binary parts
\[
U_0,V_0\in\mathbb C[p,q]_3,\qquad
T_0,A_0,B_0\in\mathbb C[p,q]_2,
\]
both linear-in-\(r\) coefficients of \(A,B\), and all nine entries of
the linear part \(L=(\ell_{ij})\).  Write their coefficients as
\[
U_0=\sum u_ip^{3-i}q^i,\quad
V_0=\sum v_ip^{3-i}q^i,\quad
T_0=t_0p^2+t_1pq+t_2q^2.
\]

On \(Dk\ne0\), the constant \(E_6\) system has rank six; a decisive
minor is
\[
-124416D^5k.
\]
Its complete solution includes
\[
\begin{aligned}
[r]A&=k\left(\frac32u_0-v_2\right)p+ku_1q,\\
[r]B&=k\left(-\frac{t_1}{3D}+\frac32v_0\right)p
       +kv_1q,\\
\ell_{33}&=kt_0,\qquad u_2=0.                     \tag{12}
\end{aligned}
\]
The remaining coefficient of \(r\) in \(E_5\) is
\[
-\frac32k^2q^2
\left(-6Dp^2v_0+3Dq^2u_0-6Dq^2v_2+4p^2t_1\right).
                                                               \tag{13}
\]
It gives
\[
t_1=\frac32Dv_0,\qquad u_0=2v_2.                 \tag{14}
\]

The constant \(E_5\) system has rank five, with decisive minor
\[
5184D^4k^3.
\]
Its compatibility coefficient is
\[
3Dkv_0^2,
\]
so \(v_0=t_1=0\).  The complete solution then gives
\[
\begin{aligned}
x_1&=u_1v_2,& y_1&=v_1v_2,\\
\ell_{13}&=k(x_0-v_2^2),&
\ell_{23}&=ky_0,&
\ell_{31}&=t_0v_2.                                \tag{15}
\end{aligned}
\]

Define
\[
M_0=k\ell_{11}-v_2\ell_{13},\qquad
M_3=k\ell_{21}-v_2\ell_{23}.
\]
After the full \(E_6,E_5\) solution,
\[
E_4=D(6M_3p^2q^2-3M_0q^4),                       \tag{16}
\]
and
\[
L(k,0,-v_2)^T=(M_0,M_3,0)^T.                     \tag{17}
\]
Because \(D\ne0\), \(E_4=0\) forces \(M_0=M_3=0\).
Equation (17) then gives a nonzero right-kernel vector of \(L\),
contradicting the Keller condition \(\det L\ne0\).

This proves the theorem.

## 5. Verification

Run

```text
./verify_delta2_11_p2_branch_contact_strict.sh
```

The strict wrapper requires whitelisted transcripts from SymPy and
PARI/GP.  Both reconstruct the generic and \(\Lambda=0\) contact
determinants, the \(C=0\) Veronese split, the endpoint survivor, and
the full \(E_6,E_5,E_4\) lower solve.

The all-binary field/descent exit is recorded in
`../../WORKING_FIXED_CUBIC_LINE_ROW.md`, Section 4.  The scripts verify
the encoded algebra, not that cited theorem.

This proof was developed with AI assistance.
