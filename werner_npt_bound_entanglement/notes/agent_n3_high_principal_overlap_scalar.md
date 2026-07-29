# The high-principal-overlap region of the three-skew scalar bound

## Status

This note proves the scalar three-skew bound for every pair of qutrit
code planes whose total squared principal overlap is at least one.  It
is a direct global consequence of the sharp triple-skew stable-rank
theorem; it is not a structured-family assumption.

Let
\[
 {\cal H}=(\mathbb C^3)^{\otimes3},\qquad
 {\mathsf A}=\prod_{i=1}^3\frac{I-F_i}{2}.
\]
For two rank-two orthogonal projections \(P_U,P_V\) on \({\cal H}\),
put
\[
 r_3(U,V)=\operatorname{Tr}\bigl[(P_U\otimes P_V){\mathsf A}\bigr],
 \qquad
 \gamma(U,V)=\operatorname{Tr}(P_UP_V).
\]
The number \(\gamma=\cos^2\theta_1+\cos^2\theta_2\) is the sum of the
squared cosines of the two principal angles between the planes.

The theorem is
\[
\boxed{\qquad
 r_3(U,V)\leq\frac{4-\gamma(U,V)}6.
\qquad}                                                    \tag{1}
\]
Consequently,
\[
\boxed{\qquad
 \gamma(U,V)\geq1
 \ \Longrightarrow\
 r_3(U,V)\leq\frac12.
\qquad}                                                    \tag{2}
\]
In the logical-feature normalization
\[
 Q_{(3)}=\frac89P_{U\otimes V}{\mathsf A}P_{U\otimes V},
\]
this gives the quantitative margin
\[
\boxed{\qquad
 \frac49-\operatorname{Tr}Q_{(3)}
 \geq\frac4{27}\bigl(\gamma(U,V)-1\bigr)
 \quad(\gamma\geq1).
\qquad}                                                    \tag{3}
\]
Thus the still-unproved scalar part of the corrected common-plane
floor is confined to the strict low-overlap region
\(\gamma<1\).

The dependency-free checker is
`verification/verify_n3_high_principal_overlap_scalar.py`.

## Proof

Use the normalized qutrit Hodge matrices
\[
 (A_p)_{ai}=2^{-1/2}\varepsilon_{pai}
\]
and, for \(t\in{\cal H}\), define
\[
 D_t=\sum_{p,q,r}t_{pqr}A_p\otimes A_q\otimes A_r.
\]
The exact epsilon contraction gives
\[
 \langle t\otimes x,{\mathsf A}(t\otimes x)\rangle
 =\|D_tx\|^2.                                             \tag{4}
\]
The sharp triple-skew theorem says, for unit \(t\),
\[
 \|D_t\|_{\mathrm{op}}^2\leq\frac16.                     \tag{5}
\]
The alternating triple contraction also obeys
\[
 D_tt=0.                                                  \tag{6}
\]
Indeed, interchanging the two triples of contracted indices changes
the sign of all three epsilon tensors and hence changes the sign of
the contraction, while the product of the two copies of \(t\) is
unchanged.

For any unit \(x\), write
\[
 x=\langle t,x\rangle t+x_\perp,\qquad x_\perp\perp t.
\]
Equations (5)--(6) give the strengthened pointwise estimate
\[
\boxed{\qquad
 \langle t\otimes x,{\mathsf A}(t\otimes x)\rangle
 =\|D_tx_\perp\|^2
 \leq\frac16\left(1-|\langle t,x\rangle|^2\right).
\qquad}                                                    \tag{7}
\]

Choose arbitrary orthonormal frames
\[
 P_U=\sum_{a=0}^1|u_a\rangle\langle u_a|,
 \qquad
 P_V=\sum_{c=0}^1|v_c\rangle\langle v_c|.
\]
Summing (7) over the four pairs gives
\[
\begin{aligned}
 r_3(U,V)
 &=\sum_{a,c}
   \langle u_a\otimes v_c,
   {\mathsf A}(u_a\otimes v_c)\rangle\\
 &\leq\frac16\sum_{a,c}
   \left(1-|\langle u_a,v_c\rangle|^2\right)\\
 &=\frac16\left(4-\operatorname{Tr}P_UP_V\right).
\end{aligned}
\]
This proves (1), and (2) is immediate.

Finally,
\[
 \operatorname{Tr}Q_{(3)}=\frac89r_3(U,V).
\]
Substituting (1) and simplifying gives
\[
 \frac49-\operatorname{Tr}Q_{(3)}
 \geq
 \frac49-\frac4{27}(4-\gamma)
 =\frac4{27}(\gamma-1),
\]
which proves (3). \(\square\)

## Equality information and limitation

Equality in (1) forces equality in all four pointwise estimates (7).
Whenever \(v_c\) has a nonzero component orthogonal to \(u_a\), that
component must be a top right singular vector of \(D_{u_a}\), and
\(u_a\) must lie in the completely classified biseparable equality
orbit of the sharp triple-skew theorem.

This simultaneous equality condition is substantially more rigid than
the scalar principal-angle condition alone, but its full four-pair
classification is not proved here.  In particular, (1) does not settle
the region \(\gamma<1\); exact scalar equality examples occur there,
including pairs of orthogonal code planes.

