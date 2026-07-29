# Quantitative fixed-left two-copy stability on the split equality branch

## Status

Let \(U:\mathbb C^2\to\mathbb C^3\otimes\mathbb C^3\) be an
isometry and define the fixed-left endpoint compression by
\[
 \langle W,H_UW\rangle
 =Q_2(UW^\dagger),\qquad
 W:\mathbb C^2\to\mathbb C^3\otimes\mathbb C^3.
 \tag{1}
\]
The qualitative fixed-left rigidity theorem says that \(H_U\) can
have a kernel only when the code plane has a common \(2\times2\)
local support.

This note gives the complete spectrum of \(H_U\) on the other
equality branch which occurs in the proof of that rigidity theorem:
\[
 {\cal U}_{a,b}
 =
 \operatorname{span}\{aE_{11}+bE_{22},E_{33}\},
 \qquad a,b\geq0,\quad a^2+b^2=1.
 \tag{2}
\]
Although this plane has full support when \(ab\ne0\), it is the
full-support limit of the equality case in the rank-two reduction
inequality.  Its exact fixed-left gap is
\[
 \boxed{\qquad
 \lambda_{\min}(H_{{\cal U}_{a,b}})
 =
 \frac{1-\sqrt{1-2a^2b^2}}2.
 \qquad}
 \tag{3}
\]

Write
\[
 \rho_L=\operatorname{Tr}_2P_{\cal U},\qquad
 \rho_R=\operatorname{Tr}_1P_{\cal U}.
 \tag{4}
\]
On (2),
\[
 \rho_L=\rho_R=\operatorname{diag}(a^2,b^2,1).
 \tag{5}
\]
Consequently (3) proves the two quantitative estimates
\[
 \boxed{\quad
 H_{{\cal U}_{a,b}}
 \succeq
 \frac{\det\rho_L+\det\rho_R}{4}\,I,
 \quad}
 \tag{6}
\]
and
\[
 \boxed{\quad
 H_{{\cal U}_{a,b}}
 \succeq
 (2-\sqrt2)\,
 \lambda_{\min}(\rho_L)\lambda_{\min}(\rho_R)\,I.
 \quad}
 \tag{7}
\]
The coefficient \(1/4\) in (6) is asymptotically sharp as
\(b\downarrow0\), and \(2-\sqrt2\) in (7) is attained at
\(a=b=1/\sqrt2\).

Unrestricted complex discovery optimization supports (6)--(7) for
every two-qutrit code plane, with precisely these sharp constants.
No global proof is asserted here.  Thus the exact theorem in this
note identifies the quantitative target and its unavoidable constants;
it does not yet supply the stability theorem needed by the
three-copy Haar argument.

The dependency-free checker
`verification/verify_n2_fixed_left_quantitative_split.py` verifies
the characteristic-polynomial identity and the two sharp algebraic
constants.

## 1. Fixed-left coordinates

Put
\[
 D=\operatorname{diag}(a,b,0),\qquad Z=E_{33}.
 \tag{8}
\]
The two columns \(D,Z\), regarded as vectors in \(M_3\), form an
orthonormal basis of (2).  Write the two columns of \(W\) as
\[
 y=(y_{ij}),\qquad w=(w_{ij}).
 \tag{9}
\]
Using
\[
 Q_2(C)
 =
 \|C\|_2^2
 -\frac12\left(
 \|\operatorname{Tr}_1C\|_2^2+
 \|\operatorname{Tr}_2C\|_2^2
 \right)
 +\frac14|\operatorname{Tr}C|^2,
 \tag{10}
\]
with \(C=Dy^\dagger+Zw^\dagger\), all but three coordinates
diagonalize immediately.

In the ordered three-dimensional block
\[
 (y_{11},y_{22},w_{33}),
 \tag{11}
\]
the matrix is
\[
 M_{a,b}=
 \begin{pmatrix}
 a^2/4+b^2&ab/4&a/4\\
 ab/4&a^2+b^2/4&b/4\\
 a/4&b/4&1/4
 \end{pmatrix}.
 \tag{12}
\]
The remaining fifteen coordinates have the following eigenvalues:
\[
\begin{array}{c|c}
\text{eigenvalue}&\text{multiplicity outside (12)}\\ \hline
1&5\\
1/2&6\\
(1+a^2)/2&2\\
(1+b^2)/2&2.
\end{array}
\tag{13}
\]

## 2. The exceptional three-dimensional block

Direct expansion of the determinant gives the polynomial identity
\[
\begin{aligned}
4\det(xI-M_{a,b})
&-(2x-1)(2x^2-2x+a^2b^2)\\
&=
-x(a^2+b^2-1)(-a^2-b^2+5x-2).
\end{aligned}
\tag{14}
\]
On the unit circle \(a^2+b^2=1\), the eigenvalues of (12) are
\[
 \frac12,\qquad
 \lambda_\pm
 =
 \frac{1\pm\sqrt{1-2a^2b^2}}2.
 \tag{15}
\]
Combining (13)--(15), the complete characteristic polynomial is
\[
\boxed{
\begin{aligned}
\chi_{H_{\cal U}}(x)
={}&(x-1)^5(x-\tfrac12)^7\\
&\cdot
\left(x-\frac{1+a^2}{2}\right)^2
\left(x-\frac{1+b^2}{2}\right)^2\\
&\cdot
\left(x^2-x+\frac{a^2b^2}{2}\right).
\end{aligned}}
\tag{16}
\]
Every displayed eigenvalue other than \(\lambda_-\) is at least
\(1/2\), while \(0\leq\lambda_-\leq(1-1/\sqrt2)/2<1/2\).
This proves (3).

## 3. Sharp determinant and marginal gaps

Put \(t=a^2b^2\in[0,1/4]\).  Rationalizing (3) gives
\[
 \lambda_-=\frac{t}{1+\sqrt{1-2t}}\geq\frac t2.
 \tag{17}
\]
Since both determinants in (5) equal \(t\), equation (17) is (6).
Moreover
\[
 \frac{\lambda_-}{(\det\rho_L+\det\rho_R)/4}
 =
 \frac{2}{1+\sqrt{1-2t}}
 \longrightarrow1
 \quad(t\downarrow0).
 \tag{18}
\]
Thus no larger universal coefficient can hold in (6), even if it is
tested only on the split family.

For (7), put
\[
 m=\min\{a^2,b^2\}\in[0,1/2].
 \tag{19}
\]
Then \(t=m(1-m)\) and
\[
 \frac{\lambda_-}{m^2}
 =
 \frac{1-m}{
 m\left(1+\sqrt{1-2m+2m^2}\right)}.
 \tag{20}
\]
The right side is decreasing on \((0,1/2]\).  Indeed its logarithmic
derivative is
\[
 -\frac1{1-m}-\frac1m
 +\frac{1-2m}{
 \sqrt{1-2m+2m^2}
 \left(1+\sqrt{1-2m+2m^2}\right)}
 <0:
 \tag{21}
\]
the magnitude of the sum of the first two terms is at least \(4\),
whereas the last term is less than \(\sqrt2\).
At \(m=1/2\), (20) equals \(2-\sqrt2\).  Since the product of the two
minimum marginal eigenvalues in (5) is \(m^2\), this proves (7) and
its sharpness.

## 4. Conditional consequence for the Haar boundary filter

The following records exactly how a global version of (6) would enter
the three-copy proof.

Assume, provisionally, that every two-qutrit plane \({\cal U}\) obeys
\[
 H_{\cal U}\succeq
 \frac{\det\rho_L({\cal U})+\det\rho_R({\cal U})}{4}I.
 \tag{22}
\]
Fix a three-copy rank-two matrix \(C\), a site \(i\), and a unit vector
\(z\).  Let \(P_z=I-|z\rangle\langle z|\).  The exact separable
decomposition of the compressed one-site endpoint writes
\[
 Q_3(P_z^{(i)}C)
 =
 \sum_\mu c_\mu Q_2(M_{\mu,z}),
 \qquad c_\mu>0,
 \tag{23}
\]
where each \(M_{\mu,z}\) is obtained from \(C\) by one rank-one local
row contraction and one rank-one local column contraction at site
\(i\).  In particular \(\operatorname{rank}M_{\mu,z}\leq2\).

When \(A_{\mu,z}\) has rank two, orthonormalize its two columns and
call the resulting plane \({\cal U}_{\mu,z}\).  Equation (22) gives
\[
 Q_2(M_{\mu,z})
 \geq
 \frac{
 \det\rho_L({\cal U}_{\mu,z})
 +\det\rho_R({\cal U}_{\mu,z})
 }4\,\|M_{\mu,z}\|_2^2.
 \tag{24}
\]
If \(A_{\mu,z}\) has rank at most one, assign the corresponding
determinant coefficient the value zero; then (24) follows from
two-copy positivity.
Define the nonnegative slice-minor slack
\[
 {\cal D}_i(C)
 =
 {\mathbb E}_z\sum_\mu c_\mu
 \left[
 \det\rho_L({\cal U}_{\mu,z})
 +\det\rho_R({\cal U}_{\mu,z})
 \right]\|M_{\mu,z}\|_2^2.
 \tag{25}
\]
The exact local Haar identity then upgrades the known conditional
sector inequality to
\[
\boxed{
\frac58\left[
\frac14w_{\{i\}}
-\frac12\left(w_{\{i,j\}}+w_{\{i,k\}}\right)
+w_{\{1,2,3\}}
\right]
\geq\frac14{\cal D}_i(C).
}
\tag{26}
\]

Thus (22) would exclude the zero-slack interior Haar equality
quantitatively, rather than only qualitatively.  It still would not,
by itself, prove \(Q_3(C)\geq0\): one additionally needs an inequality
which controls the negative endpoint sector deficit by
\(\sum_i{\cal D}_i(C)\).  Equation (26) isolates that remaining
nonlinear minor inequality without treating the conditioned slices
independently.
