# The global fixed-left second-kernel frontier: an intrinsic distance and the correct tangent gap

## Status

Let \({\cal U}\subset \mathbb C^3\otimes\mathbb C^3\) be a
two-plane, let \(U:\mathbb C^2\to\mathbb C^3\otimes\mathbb C^3\)
be an isometry onto it, and define
\[
 \langle W,H_UW\rangle=Q_2(UW^\dagger).
 \tag{1}
\]
This note gives two exact reductions of the proposed global estimate
\[
 \lambda_2(H_U)\ \stackrel{?}{\geq}\
 c\,\operatorname{dist}_2({\cal U},{\sf Fac})^4.
 \tag{2}
\]
Here \({\sf Fac}\) is the union of the two fixed-factor rulings and
eigenvalues are ordered increasingly.

First, the distance in (2) is exactly a one-body spectral deficit:
\[
 \boxed{\quad
 \operatorname{dist}_2({\cal U},{\sf Fac})^2
 =4-2M,\qquad
 M=\max\{\lambda_{\max}(\rho_L),\lambda_{\max}(\rho_R)\},
 \quad}
 \tag{3}
\]
where
\[
 \rho_L=\operatorname{Tr}_R P_{\cal U},\qquad
 \rho_R=\operatorname{Tr}_L P_{\cal U}.
 \tag{4}
\]

Second, \(\lambda_2(H_U)\) is exactly the second singular-value
defect of an augmented local-orbit tangent map.  This removes the
rank-two variable \(W\) from the remaining modulus.

An initially attractive simplification is false.  If the scalar
trace channel is omitted, the second singular value can saturate
away from \({\sf Fac}\).  The exact plane
\[
 {\cal U}=\operatorname{span}\{E_{11},E_{22}\}
 \tag{5}
\]
has \(M=1\), hence distance squared \(2\), but the unaugmented
contraction operator has second largest eigenvalue exactly \(2\).
Thus the scalar rank-one correction in \(H_U\) is essential.

The global estimate (2) is not proved here.  Equations (3) and (12)
below identify its correct finite-dimensional form, while (5)
rigorously disproves the stronger raw-contraction route.

## 1. Exact distance to the factor-plane union

Let \(P=P_{\cal U}\).  A plane in the left fixed-factor ruling has
projection
\[
 Q_{a,F}=|a\rangle\langle a|\otimes P_F,
 \tag{6}
\]
where \(a\in\mathbb C^3\) is a unit vector and \(P_F\) has rank two.
For fixed \(a\), put
\[
 K_a=(\langle a|\otimes I)P(|a\rangle\otimes I).
 \tag{7}
\]
This positive \(3\times3\) matrix has rank at most two.  Therefore
\[
 \max_{\operatorname{rank}P_F=2}\operatorname{Tr}(P Q_{a,F})
 =\max_{\operatorname{rank}P_F=2}\operatorname{Tr}(K_aP_F)
 =\operatorname{Tr}K_a
 =\langle a,\rho_La\rangle.
 \tag{8}
\]
Maximizing over \(a\) gives
\[
 \max_{Q\ {\rm in\ the\ left\ ruling}}\operatorname{Tr}(PQ)
 =\lambda_{\max}(\rho_L).
 \tag{9}
\]
The right ruling gives \(\lambda_{\max}(\rho_R)\).  Since \(P,Q\)
both have rank two,
\[
 \|P-Q\|_2^2
 =\operatorname{Tr}P+\operatorname{Tr}Q-2\operatorname{Tr}(PQ)
 =4-2\operatorname{Tr}(PQ).
 \tag{10}
\]
Equations (8)--(10) prove (3).  Notice that no local-support or
genericity assumption is involved.

## 2. The augmented tangent-map identity

Write \(u_0,u_1\) for the columns of \(U\).  Let
\[
 {\cal G}=M_3^0\oplus M_3^0\oplus\mathbb C
 \tag{11}
\]
with its Hilbert--Schmidt direct-sum norm, and define
\[
 \widehat{\cal T}_U(A,B,z)
 =
 \left(
   (B\otimes I+I\otimes A+zI/\sqrt6)u_r
 \right)_{r=0}^1 .
 \tag{12}
\]
Transposes may be inserted in one local factor according to the
vectorization convention; they do not change singular values.

For \(W=(w_0,w_1)\), put
\[
\begin{aligned}
 L_W&=\sum_rw_ru_r^\dagger,&
 R_W&=\sum_ru_r^\dagger w_r,\\
 t_W&=\operatorname{Tr}L_W=\operatorname{Tr}R_W,&
 X_0&=X-\tfrac13\operatorname{Tr}(X)I.
\end{aligned}
\tag{13}
\]
The adjoint of (12) is
\[
 \widehat{\cal T}_U^\dagger W
 =\bigl((R_W)_0,(L_W)_0,t_W/\sqrt6\bigr).
 \tag{14}
\]
The coefficient-matrix formula for \(Q_2\) gives
\[
\begin{aligned}
 Q_2(UW^\dagger)
 &=
 \|W\|_2^2
 -\frac12\bigl(\|L_W\|_2^2+\|R_W\|_2^2\bigr)
 +\frac14|t_W|^2\\
 &=
 \|W\|_2^2
 -\frac12\left(
   \|(L_W)_0\|_2^2+\|(R_W)_0\|_2^2+\frac16|t_W|^2
 \right).
\end{aligned}
\tag{15}
\]
Consequently
\[
 \boxed{\qquad
 2H_U=2I_{18}-\widehat{\cal T}_U
                    \widehat{\cal T}_U^\dagger .
 \qquad}
 \tag{16}
\]
The established two-copy theorem is exactly
\(\|\widehat{\cal T}_U\|_{\rm op}^2\leq2\).

Let \(s_1\geq s_2\geq\cdots\) be the singular values of
\(\widehat{\cal T}_U\).  Since (12) has a 17-dimensional domain,
(16) gives the exact spectral identity
\[
 \boxed{\qquad
 \lambda_2(H_U)=1-\frac12s_2(\widehat{\cal T}_U)^2.
 \qquad}
 \tag{17}
\]
Combining (3) and (17), the candidate constant \(c=1/1280\) is
equivalent to the explicit augmented tangent inequality
\[
 \boxed{\qquad
 2-s_2(\widehat{\cal T}_U)^2
 \geq\frac1{160}(2-M)^2 .
 \qquad}
 \tag{18}
\]
Thus (18), not a gap for the two uncentered contraction maps, is the
correct remaining local modulus.

## 3. Exact obstruction to the unaugmented route

Define the unaugmented contraction map by
\[
 {\cal F}_UW=(L_W,R_W),
 \qquad S_U={\cal F}_U^\dagger{\cal F}_U.
 \tag{19}
\]
Equations (13)--(15) show
\[
 \boxed{\qquad
 S_U=2(I-H_U)+\frac12|\Psi_U\rangle\langle\Psi_U|,
 \qquad
 \Psi_U=(u_0,u_1).
 \qquad}
 \tag{20}
\]

Take \(u_0=E_{11}\), \(u_1=E_{22}\).  Direct exact contraction gives
\[
\begin{aligned}
 \chi_{H_U}(x)&=x(x-1)^8(x-\tfrac12)^9,\\
 \chi_{S_U}(x)&=x^8(x-1)^8(x-2)^2.
\end{aligned}
\tag{21}
\]
In particular,
\[
 \lambda_2^\downarrow(S_U)=2.
 \tag{22}
\]
The two eigenvectors at eigenvalue \(2\) are simply
\[
 W^{(1)}=(E_{11},0),\qquad
 W^{(2)}=(0,E_{22}).
 \tag{23}
\]
On the other hand,
\[
 \rho_L=\rho_R=\operatorname{diag}(1,1,0),
 \qquad M=1,
 \tag{24}
\]
so (3) gives
\[
 \operatorname{dist}_2({\cal U},{\sf Fac})^2=2.
 \tag{25}
\]
It follows that no inequality of the form
\[
 2-\lambda_2^\downarrow(S_U)\geq
 c(2-M)^p
 \tag{26}
\]
can hold with \(c>0\), for any positive exponent \(p\).

The failure has a transparent origin.  The two vectors (23) saturate
the two raw marginal contractions independently.  The trace channel
couples them: subtracting the rank-one term in (20) leaves only one
augmented saturation direction.  Indeed, (21) gives
\(\lambda_2(H_U)=1/2\), fully consistent with a positive global
second-kernel modulus.

## 4. Equality and near-factor behavior

Equation (3) shows
\[
 M=2\quad\Longleftrightarrow\quad{\cal U}\in{\sf Fac}.
\tag{27}
\]
The exact fixed-left nullity theorem then gives
\[
 s_2(\widehat{\cal T}_U)^2=2
 \quad\Longleftrightarrow\quad{\cal U}\in{\sf Fac}.
\tag{28}
\]
Thus both sides of (18) have the same zero set.  On the complete
common-\(2\times2\)-support boundary, the established estimate
\[
 \lambda_2(H_U)\geq\frac1{1280}
 \operatorname{dist}_2({\cal U},{\sf Fac})^4
\tag{29}
\]
already proves (18).  What remains is the unrestricted full-support
case, with the augmented scalar channel retained.

