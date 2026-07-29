# A quantitative stationary Haar gap from one-site marginals

## Status

Let \(C\) be a normalized rank-two qutrit three-copy matrix which is a
stationary point of the endpoint quotient, and put
\[
 q=Q_3(C)<0,\qquad \delta=-q>0.
 \tag{1}
\]
For a physical site \(i\), let
\[
 \rho_i^L=\operatorname{Tr}_{\widehat i}(CC^\dagger),
 \qquad \operatorname{Tr}\rho_i^L=1.
 \tag{2}
\]
Write the eigenvalues of \(\rho_i^L\) as
\[
 \lambda_1\geq\lambda_2\geq\lambda_3\geq0.
 \tag{3}
\]
The local Haar bracket is
\[
 g_i=
 \frac14w_{\{i\}}
 -\frac12\left(w_{\{i,j\}}+w_{\{i,k\}}\right)
 +w_{\{1,2,3\}}.
 \tag{4}
\]

This note proves the exact quantitative estimate
\[
\boxed{
 g_i\geq
 \begin{cases}
 \displaystyle
 \frac{16\delta}{15}\,
 \frac{(\lambda_1-\frac12)^3}
 {(\lambda_1-\lambda_2)(\lambda_1-\lambda_3)},
 &\lambda_1>\frac12,\\[4mm]
 0,&\lambda_1\leq\frac12.
 \end{cases}}
 \tag{5}
\]
The same statement holds with the right one-site marginal
\(\rho_i^R\).

Thus every negative stationary point whose left or right marginal has
largest eigenvalue greater than \(1/2\) has an explicit strictly
positive Haar slack at that site.  The estimate becomes silent
precisely in the balanced region
\[
 \rho_i^{L,R}\preceq\frac12I_3.
 \tag{6}
\]
In particular, it cannot by itself exclude the maximally mixed
Haar-equality geometry \(\rho_i^{L,R}=I_3/3\).  This is an exact
obstruction, not a numerical limitation: the abstract one-site
canonical inequality supplies no positive lower bound in (5)
throughout (6), and at \(I_3/3\) its zero value is attainable.
Common-code two-copy stability is therefore genuinely necessary in
the balanced region.

The dependency-free checker
`verification/verify_n3_stationary_haar_marginal_gap.py` verifies the
local Haar coefficients and the simplex integral in (5).

## 1. The stationary one-site form

Define the Hermitian form
\[
 h_i(A,B)
 =
 \left\langle A^{(i)}C,
 {\cal L}^{\otimes3}(B^{(i)}C)\right\rangle_{\rm HS},
 \qquad A,B\in M_3,
 \tag{7}
\]
and the positive normalization form
\[
 {\cal N}_i(A,B)=\operatorname{Tr}(A^\dagger B\rho_i^L).
 \tag{8}
\]
Stationarity under arbitrary complex left local filters gives
\[
 h_i(A,I)=q\,{\cal N}_i(A,I)
 \qquad(A\in M_3).
 \tag{9}
\]
If \(\operatorname{rank}A\leq2\), the range of \(A^{(i)}C\) has
deficient local support.  The established support-boundary theorem
therefore gives
\[
 h_i(A,A)=Q_3(A^{(i)}C)\geq0.
 \tag{10}
\]

Put
\[
 {\cal H}_0=\{B:\operatorname{Tr}(B\rho_i^L)=0\}.
 \tag{11}
\]
The exact canonical-form lemma for a Hermitian form which is
nonnegative on the determinantal hypersurface says that
\[
 h_i(tI+B,tI+B)
 =
 -\delta|t|^2+H_i(B,B),
 \qquad B\in{\cal H}_0,
 \tag{12}
\]
where
\[
 H_i(B,B)\geq\delta\,r(B)^2
 \tag{13}
\]
and \(r(B)\) is the largest modulus of an eigenvalue of \(B\).
For completeness, (13) follows by applying (10) to
\(B-\lambda I\), where \(\lambda\) is each eigenvalue of \(B\).

## 2. Pointwise rank-one and rank-two filters

For a unit vector \(z\), put
\[
 R_z=|z\rangle\langle z|,\qquad
 P_z=I-R_z,\qquad
 r_z=\langle z,\rho_i^Lz\rangle.
 \tag{14}
\]
The weighted scalar part of \(P_z\) is \(1-r_z\), and
\[
 P_z-(1-r_z)I
 \quad\hbox{has eigenvalues}\quad
 r_z,r_z,-(1-r_z).
 \tag{15}
\]
Equations (12)--(13) therefore give
\[
\boxed{\qquad
 h_i(P_z,P_z)\geq
 \delta(2r_z-1)_+.
 \qquad}
 \tag{16}
\]
Likewise, the weighted scalar part of \(R_z\) is \(r_z\), while
\[
 R_z-r_zI
 \quad\hbox{has eigenvalues}\quad
 1-r_z,-r_z,-r_z,
 \tag{17}
\]
and hence
\[
\boxed{\qquad
 h_i(R_z,R_z)\geq
 \delta(1-2r_z)_+.
 \qquad}
 \tag{18}
\]

The two inequalities are equivalent after Haar averaging.  Indeed,
the exact one-site averages of the filtered endpoint form have
scalar/traceless eigenvalues
\[
\begin{array}{c|cc}
&\text{scalar}&\text{traceless}\\ \hline
{\mathbb E}_z\,h_i(P_z\cdot,P_z\cdot)&0&5/8\\
{\mathbb E}_z\,h_i(R_z\cdot,R_z\cdot)&1/6&7/24.
\end{array}
\tag{19}
\]
Consequently
\[
 {\cal L}
 =
 3\left(
 {\mathbb E}{\cal F}_{P_z}
 -
 {\mathbb E}{\cal F}_{R_z}
 \right)
 \tag{20}
\]
as one-site quadratic forms.  In sector notation,
\[
\begin{aligned}
 {\mathbb E}_z h_i(P_z,P_z)&=\frac58g_i,\\
 {\mathbb E}_z h_i(R_z,R_z)&=\frac58g_i+\frac\delta3.
\end{aligned}
\tag{21}
\]
The second line also follows immediately from
\(q=3({\mathbb E}h_i(P_z)-{\mathbb E}h_i(R_z))\).

Average (16):
\[
 \boxed{\qquad
 \frac58g_i
 \geq
 \delta\,{\mathbb E}_z(2r_z-1)_+.
 \qquad}
 \tag{22}
\]
Since \({\mathbb E}(1-2r_z)=1/3\),
\[
 {\mathbb E}(1-2r_z)_+
 =
 \frac13+{\mathbb E}(2r_z-1)_+.
 \tag{23}
\]
Thus averaging (18) and using the second line of (21) gives exactly
the same inequality (22), with no loss.

## 3. Exact Haar integration

In an eigenbasis of \(\rho_i^L\), write
\[
 p_j=|z_j|^2,\qquad
 r_z=\lambda_1p_1+\lambda_2p_2+\lambda_3p_3.
 \tag{24}
\]
For a Haar qutrit vector, \((p_1,p_2,p_3)\) is uniform on the simplex
\[
 p_j\geq0,\qquad p_1+p_2+p_3=1,
 \tag{25}
\]
with constant density \(2\).

If \(\lambda_1\leq1/2\), the integrand in (22) vanishes.  Suppose
\(\lambda_1>1/2\).  Then \(\lambda_2,\lambda_3<1/2\).  In coordinates
\(p_1=1-p_2-p_3\), the positive region is the triangle
\[
 (\lambda_1-\lambda_2)p_2
 +(\lambda_1-\lambda_3)p_3
 <\lambda_1-\frac12.
 \tag{26}
\]
Integrating the affine tent over this triangle gives
\[
\boxed{\qquad
 {\mathbb E}_z(2r_z-1)_+
 =
 \frac{
 2(\lambda_1-\frac12)^3
 }{
 3(\lambda_1-\lambda_2)(\lambda_1-\lambda_3)
 }.
 \qquad}
 \tag{27}
\]
Substitution of (27) into (22) proves (5).

## 4. A global value refinement

Define
\[
 F(\rho)=
 \begin{cases}
 \displaystyle
 \frac{(\lambda_1-\frac12)^3}
 {(\lambda_1-\lambda_2)(\lambda_1-\lambda_3)},
 &\lambda_1>\frac12,\\[3mm]
 0,&\lambda_1\leq\frac12.
 \end{cases}
 \tag{28}
\]
Because the same \(g_i\) is bounded using either the left or the right
marginal, put
\[
 S(C)=\sum_{i=1}^3
 \max\{F(\rho_i^L),F(\rho_i^R)\}.
 \tag{29}
\]
If \(w_k\) denotes the total scalar/traceless sector mass of degree
\(k\), direct elimination using \(\sum_kw_k=1\) gives
\[
\begin{aligned}
 \sum_{i=1}^3g_i
 &=\frac14w_1-w_2+3w_3\\
 &=\frac13-\frac{8\delta}{3}-\frac34w_1
 \leq\frac{1-8\delta}{3}.
\end{aligned}
\tag{30}
\]
On the other hand, summing (5) gives
\[
 \sum_i g_i\geq\frac{16\delta}{15}S(C).
 \tag{31}
\]
Combining (30)--(31) proves the explicit stationary-value bound
\[
\boxed{\qquad
 -Q_3(C)=\delta
 \leq
 \frac1{8+\frac{16}{5}S(C)}.
 \qquad}
\tag{32}
\]
Thus the universal lower bound \(-1/8\) improves strictly at every
stationary point having an unbalanced marginal.  Approaching
\(-1/8\) forces all six largest marginal eigenvalues toward at most
\(1/2\).  Equation (32) does not prevent a negative value when all
six marginals are balanced.

## 5. What this does and does not control

The common-code equality analysis proves the stronger qualitative
fact \(g_i>0\) at every negative stationary point, including the
balanced region (6).  Equation (5) is the first explicit relation
between that strict bracket, the negative value \(\delta\), and a
one-site marginal.

It also shows exactly why marginal eigenvalues alone cannot finish
the proof.  When \(\rho_i^L\preceq I/2\), the canonical rank-two
filter inequality permits every \(P_z\) to lie on its boundary.
At the central point \(\rho=I_3/3\), this is realized by the abstract
Hermitian form
\[
h(A,B)
 =
 2\delta\,{\cal N}(A,B)
 -3\delta\,
 \overline{{\cal N}(I,A)}{\cal N}(I,B).
 \tag{33}
\]
It has \(h(A,I)=-\delta{\cal N}(A,I)\), is nonnegative for
\(\operatorname{rank}A\leq2\) by the sharp rank-two overlap
\[
 |{\cal N}(I,A)|^2\leq\frac23{\cal N}(A,A),
 \tag{34}
\]
and satisfies \(h(P_z,P_z)=0\) for every \(z\).
The missing quantitative input must see that all these filters arise
from one common rank-two coefficient matrix.  A fixed-left two-copy
determinant gap, followed by a common-origin inequality for its
averaged slice minors, is one precise mechanism capable of supplying
that information.
