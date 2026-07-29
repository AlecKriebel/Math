# A two-column Hodge recursion for the scalar common-plane shift

## Status

This note proves the scalar triple-Hodge bound
\[
 \operatorname{Tr}Q_{(3)}\leq\frac49
\]
whenever either singular plane has a one-site tensor factor
\[
 U=x\otimes W,\qquad \dim W=2,
\]
while the other singular plane is arbitrary.  This is strictly broader
than the earlier common-factor chart, which required compatible
factorizations of both planes.

The proof exposes the correct two-column spectral tradeoff.  There are
two inequivalent equality spectra,
\[
 (1/4,1/4)\qquad\hbox{and}\qquad(1/3,1/6),
\]
so neither of the two leading eigenvalues admits the separately
conjectured \(1/6\) bound.

For a general plane, slicing off one qutrit gives the exact recursion
\[
 R_U=\frac12(G\otimes I-H^\Gamma)
\]
with one common positive block Gram \(H\).  The unrestricted scalar
problem is thereby reduced to a sharp two-eigenvalue inequality for
this structured partial-transpose difference.  That last inequality
remains unproved.

The dependency-free checker is
`verification/verify_n3_triple_hodge_two_column_recursion.py`.

## 1. Hodge contractions and the scalar target

Put
\[
 (A_p)_{ai}=2^{-1/2}\varepsilon_{pai}.
\]
For \(u\in(\mathbb C^3)^{\otimes3}\), define
\[
 T_u=\sum_{p,q,r}u_{pqr}A_p\otimes A_q\otimes A_r.
                                                               \tag{1}
\]
For an orthonormal frame \(u_0,u_1\) of a plane \(U\), set
\[
 R_U=T_{u_0}^\dagger T_{u_0}
     +T_{u_1}^\dagger T_{u_1}\succeq0.                  \tag{2}
\]
If \(V\) is another two-plane with orthonormal frame \(v_0,v_1\),
then direct Hodge contraction gives
\[
\begin{aligned}
 \operatorname{Tr}\!\left[
   (P_U\otimes P_V){\mathsf A}_1{\mathsf A}_2{\mathsf A}_3
 \right]
 &=\sum_{a,c}\|T_{u_a}v_c\|^2\\
 &=\operatorname{Tr}(P_VR_U).
\end{aligned}                                             \tag{3}
\]
Consequently
\[
 \operatorname{Tr}Q_{(3)}
 =\frac89\operatorname{Tr}(P_VR_U).                     \tag{4}
\]
Ky--Fan variation shows that the unrestricted scalar bound is exactly
\[
 \boxed{\qquad
 \lambda_1(R_U)+\lambda_2(R_U)\leq\frac12
 \quad\hbox{for every two-plane }U.
 \qquad}                                                  \tag{5}
\]

The sharp single-column triple-skew theorem only gives
\(\lambda_1(R_U)\leq1/3\).  The tempting supplement
\(\lambda_2(R_U)\leq1/6\) is false.  For
\[
 U=\operatorname{span}\{|000\rangle,|001\rangle\},
\]
one finds
\[
 \operatorname{spec}R_U
 =
 \left(
 \underbrace{\frac14,\ldots,\frac14}_{4},
 \underbrace{\frac18,\ldots,\frac18}_{8},
 \underbrace{0,\ldots,0}_{15}
 \right).                                                \tag{6}
\]
Thus only the joint sum in (5) has the correct sharp geometry.

There is an additional exact paired identity.  The triple-Hodge
contraction is alternating:
\[
 T_uv=-T_vu,\qquad T_uu=0.                               \tag{6a}
\]
Put
\[
 p_U=\|T_{u_0}u_1\|^2.
\]
In the frame \(u_0,u_1\), equation (6a) gives
\[
\boxed{\qquad
 P_UR_UP_U=p_UI_U,\qquad 0\leq p_U\leq\frac16.
\qquad}                                                   \tag{6b}
\]
Indeed, the two diagonal entries both equal \(p_U\), while each
off-diagonal entry contains a zero factor.  The last bound is the
sharp single-column theorem applied to \(T_{u_0}u_1\).

The two exact equality branches fit the affine spectral pattern
\[
 \left(\frac14+\frac{p_U}{2},
       \frac14-\frac{p_U}{2}\right):
\]
the balanced branch has \(p_U=0\), while the spiked branch has
\(p_U=1/6\).  This suggests the sharper paired inequalities
\[
\lambda_1(R_U)\stackrel?{\leq}\frac14+\frac{p_U}{2},
\qquad
\lambda_2(R_U)\stackrel?{\leq}\frac14-\frac{p_U}{2}.      \tag{6c}
\]
They would prove (5), but remain conjectural.  Unrestricted complex
discovery searches have not violated them; that numerical observation
is not used in any result of this note.

## 2. A sharp double-Hodge spectral lemma

For a unit two-qutrit vector \(x=(x_{pq})\), put
\[
 D_x=\sum_{p,q}x_{pq}A_p\otimes A_q
\]
and let
\[
 \mu_1\geq\mu_2\geq\cdots\geq0
\]
be the eigenvalues of \(D_x^\dagger D_x\).

### Lemma

\[
 \boxed{\qquad
 \mu_1\leq\frac13,\qquad
 \mu_1+\mu_2\leq\frac12.
 \qquad}                                                  \tag{7}
\]

### Proof

Hodge covariance under local qutrit unitaries reduces the coefficient
matrix of \(x\) to its singular-value form
\[
 \operatorname{diag}(\sigma_1,\sigma_2,\sigma_3),
\qquad
 \sigma_1\geq\sigma_2\geq\sigma_3\geq0,\qquad
 \sum_i\sigma_i^2=1.                                    \tag{8}
\]
On the six off-diagonal matrix units, \(D_x\) has three \(2\times2\)
blocks with eigenvalues
\[
 \pm\frac{\sigma_1}{2},\qquad
 \pm\frac{\sigma_2}{2},\qquad
 \pm\frac{\sigma_3}{2}.                                 \tag{9}
\]
On the diagonal matrix units it is the real symmetric matrix
\[
 B=\frac12
 \begin{pmatrix}
 0&\sigma_3&\sigma_2\\
 \sigma_3&0&\sigma_1\\
 \sigma_2&\sigma_1&0
 \end{pmatrix}.                                         \tag{10}
\]

For a real unit vector \(z\),
\[
\begin{aligned}
 |z^{\mathsf T}Bz|
 &\leq
 \sqrt{\sigma_1^2+\sigma_2^2+\sigma_3^2}\,
 \sqrt{z_1^2z_2^2+z_1^2z_3^2+z_2^2z_3^2}\\
 &\leq\frac1{\sqrt3}.
\end{aligned}                                            \tag{11}
\]
The last inequality follows from
\[
 z_1^2z_2^2+z_1^2z_3^2+z_2^2z_3^2
 \leq\frac13(z_1^2+z_2^2+z_3^2)^2.
\]
Together with \(\sigma_i/2\leq1/2\), this proves the first
inequality in (7).

For the second, note first that
\[
 \operatorname{Tr}B^2=\frac12.                          \tag{12}
\]
Thus the squares of any two eigenvalues of \(B\) sum to at most
\(1/2\), while the squares of any two values from (9) sum to at most
\(\sigma_1^2/2\leq1/2\).

It remains to take one value of each type.  The principal \(2\times2\)
submatrix of \(B\) containing the \(\sigma_1/2\) edge has eigenvalues
\(\pm\sigma_1/2\).  By interlacing, after removing an eigenvalue of
\(B\) of largest absolute value, at least one remaining eigenvalue
has absolute value at least \(\sigma_1/2\).  Hence
\[
 \|B\|_{\rm op}^2+\frac{\sigma_1^2}{4}
 \leq\operatorname{Tr}B^2=\frac12.                      \tag{13}
\]
Every possible pair of singular squares of \(D_x\) therefore sums
to at most \(1/2\).  This proves (7). \(\square\)

## 3. One-factor plane theorem

Suppose
\[
 U=x\otimes W
\]
with \(x\) a unit two-site vector and \(W\) a qutrit two-plane.
Choose an orthonormal frame \(e_0,e_1\) of \(W\).  Equations
(1)--(2) factor as
\[
 R_U
 =D_x^\dagger D_x\otimes
 \left(A_{e_0}^\dagger A_{e_0}
      +A_{e_1}^\dagger A_{e_1}\right).                  \tag{14}
\]
The epsilon identity
\[
 A_p^\dagger A_s
 =\frac12(\delta_{ps}I-|s\rangle\langle p|)             \tag{15}
\]
shows that the second factor in (14) has spectrum
\[
 (1,1/2,1/2).                                           \tag{16}
\]
It follows that
\[
 \lambda_1(R_U)+\lambda_2(R_U)
 =\mu_1+\max\{\mu_2,\mu_1/2\}.                          \tag{17}
\]
Both alternatives are bounded by \(1/2\) using (7):
\[
 \mu_1+\mu_2\leq\frac12,\qquad
 \frac32\mu_1\leq\frac12.
\]
Equations (3)--(5) prove
\[
 \boxed{\qquad
 \operatorname{Tr}Q_{(3)}\leq\frac49
\quad\hbox{for }U=x\otimes W\hbox{ and arbitrary }V.
 \qquad}                                                  \tag{18}
\]
The statement is symmetric in \(U,V\).

The two equality mechanisms are visible without a classification
claim.  If \(x\) has Schmidt rank at most two, the diagonal block
\(B\) in (10) has eigenvalues \((1/2,-1/2,0)\), so the leading
spectrum in (17) is \((1/4,1/4)\).  If \(x\) is maximally entangled,
the leading spectrum is instead \((1/3,1/6)\).  Both saturate (18).

## 4. Exact recursion for a general plane

The factorization above extends to a structured block identity for
an arbitrary plane.  Slice the code at the third site:
\[
 u_a=\sum_{r=0}^2x_{ar}\otimes e_r,\qquad
 x_{ar}\in(\mathbb C^3)^{\otimes2}.                     \tag{19}
\]
Orthonormality is exactly
\[
 \sum_r\langle x_{ar},x_{br}\rangle=\delta_{ab}.         \tag{20}
\]
Define the common \(9\times9\) blocks
\[
 H_{rs}=\sum_{a=0}^1D_{x_{ar}}^\dagger D_{x_{as}},
\qquad
 H=[H_{rs}]_{r,s=0}^2\succeq0,\qquad
 G=\sum_rH_{rr}.                                        \tag{21}
\]
Positivity holds because \(H\) is the Gram matrix of the three block
columns formed from the same two slice families.

Expanding (2) and using (15) gives the lossless identity
\[
\boxed{\qquad
 R_U=\frac12\left(G\otimes I_3-H^{\Gamma_3}\right).
\qquad}                                                  \tag{22}
\]
Thus the unrestricted scalar problem (5) is the following smaller
matrix lemma:
\[
\boxed{
 \lambda_1\!\left(G\otimes I_3-H^{\Gamma_3}\right)
 +\lambda_2\!\left(G\otimes I_3-H^{\Gamma_3}\right)
 \leq1,
}                                                        \tag{23}
\]
where \(H\) has the common double-Hodge Gram form (19)--(21).
Treating \(H\) as an arbitrary positive block matrix is a relaxation:
the shared two-column slices and their Pluecker relations are the
remaining essential constraint.
