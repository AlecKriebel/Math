# Exact obstruction to the cut-projection route

## Status

The rank-two qutrit projection inequality
\[
 P\preceq \rho_A\otimes I+I\otimes\rho_B
\]
does **not** extend from \(\mathbb C^3\otimes\mathbb C^3\) to
\(\mathbb C^3\otimes\mathbb C^m\).  It already fails for \(m=4\).
Consequently it cannot be applied without an additional hypothesis to
the \(3:(3\cdot3)\) cuts of the three-qutrit pair-sector dual.

There is a second, independent obstruction.  Even if one formally
assumes the false cut inequalities, the sum of their marginal
right-hand sides is not bounded by \(2\operatorname{Tr}(D^\dagger D)\)
for pair-only \(D\).  The sharp pair-sector equality example violates
that proposed intermediate bound by a factor four.

## 1. Exact \(3\times4\) counterexample

Let
\[
 |\psi\rangle
 =\frac1{\sqrt2}|11\rangle+\frac12|22\rangle+\frac12|33\rangle
 \in\mathbb C^3\otimes\mathbb C^4 .
\]
Its reduced states are
\[
 \sigma_A=\operatorname{diag}(1/2,1/4,1/4),\qquad
 \sigma_B=\operatorname{diag}(1/2,1/4,1/4,0).
\]
Put
\[
 {\cal K}_\psi
 =|\psi\rangle\langle\psi|
  -\sigma_A\otimes I_4-I_3\otimes\sigma_B .
\]
On the diagonal Schmidt support, use
\[
 e_1=|11\rangle,\qquad
 e_+=\frac{|22\rangle+|33\rangle}{\sqrt2}.
\]
The restriction of \({\cal K}_\psi\) to
\(\operatorname{span}\{e_1,e_+\}\) is
\[
 \begin{pmatrix}
 -1/2&1/2\\
 1/2&0
 \end{pmatrix}.
\]
It therefore has the positive eigenvalue
\[
 \lambda_+=\frac{\sqrt5-1}{4}
\]
with eigenvector proportional to
\[
 \phi_+
 =e_1+\frac{1+\sqrt5}{2}e_+ .
\]
Let \(\widehat\phi_+=\phi_+/\|\phi_+\|\).  The vector
\[
 \chi=|3,4\rangle
\]
is orthogonal to \(\widehat\phi_+\) and is an eigenvector of
\({\cal K}_\psi\) with eigenvalue \(-1/4\).  Hence
\[
 P=|\widehat\phi_+\rangle\langle\widehat\phi_+|
   +|\chi\rangle\langle\chi|
\]
is an orthogonal rank-two projection.

For \(\rho_A=\operatorname{Tr}_B P\) and
\(\rho_B=\operatorname{Tr}_A P\), cyclicity of trace gives
\[
\begin{aligned}
 &\langle\psi|
  P-\rho_A\otimes I_4-I_3\otimes\rho_B
 |\psi\rangle\\
 &\qquad=\operatorname{Tr}(P{\cal K}_\psi)
 =\lambda_+-\frac14
 =\frac{\sqrt5-2}{4}>0 .
\end{aligned}
\]
Thus
\[
 P\npreceq\rho_A\otimes I_4+I_3\otimes\rho_B .
\]

The precise reason the \(3\times3\) proof breaks is now visible.  In
dimension three on the second side, the second-largest eigenvalue of
\({\cal K}_\psi\) must come from the diagonal Schmidt block or an
off-diagonal line with eigenvalue \(-(x_i+x_j)\).  An unused fourth
column instead supplies the less negative eigenvalues \(-x_i\).
Here the two largest eigenvalues are
\[
 \frac{\sqrt5-1}{4},\qquad -\frac14,
\]
whose sum is positive.

## 2. Pair-tracelessness does not bound the formal marginal sum

Let
\[
 D=E_{01}\otimes E_{01}\otimes I_3 .
\]
This is a valid pair-only dual operator: its only nonzero pair
coefficient is
\[
 B_{12}=E_{01}\otimes E_{01},
\]
which is traceless in each local factor.  Moreover
\[
 D^\dagger D=|11\rangle\langle11|\otimes I_3,\qquad
 \operatorname{Tr}(D^\dagger D)=3.
\]
Its top singular value is \(1\), with multiplicity three.  Choose the
top right singular plane
\[
 P_R=|110\rangle\langle110|+|111\rangle\langle111|.
\]
For each site \(i\), define the unnormalized marginal majorant
\[
 M_i(P_R)
 =(\operatorname{Tr}_{\widehat i}P_R)\otimes I_{\widehat i}
  +I_i\otimes\operatorname{Tr}_iP_R .
\]
A direct basis count gives
\[
 \operatorname{Tr}(D^\dagger D\,M_i(P_R))=8
 \qquad(i=1,2,3).
\]
Consequently
\[
 \sum_{i=1}^3
 \operatorname{Tr}(D^\dagger D\,M_i(P_R))
 =24
 =8\operatorname{Tr}(D^\dagger D),
\]
not at most \(2\operatorname{Tr}(D^\dagger D)=6\).

The corresponding top left singular plane
\[
 P_L=|000\rangle\langle000|+|001\rangle\langle001|
\]
gives the identical calculation with \(DD^\dagger\).  Averaging the
left and right estimates therefore does not repair the factor.

This does not disprove the pair-only Ky--Fan inequality: this \(D\) is
its exact equality example,
\[
 s_1(D)^2+s_2(D)^2=2
 =2\|B_{12}\|_2^2.
\]
It only shows that the proposed route through independently summed
cut marginal majorants loses too much information even on the sharp
boundary.

## 3. The sharp dimension-free replacement has coefficient \(4/3\)

Although coefficient one fails, there is a sharp universal replacement.

**Theorem.**  Let \(P\) be an orthogonal projection of rank at most two
on \(\mathbb C^3\otimes\mathbb C^m\), for arbitrary \(m\).  With
\(\rho_A=\operatorname{Tr}_B P\) and
\(\rho_B=\operatorname{Tr}_A P\),
\[
 \boxed{\qquad
 P\preceq\frac43
 \bigl(\rho_A\otimes I+I\otimes\rho_B\bigr).
 \qquad}                                                   \tag{1}
\]
For \(m\ge4\), the coefficient \(4/3\) is optimal.

**Proof.**
Fix a test vector \(\psi\), put
\[
 {\cal K}_{c,\psi}
 =|\psi\rangle\langle\psi|
  -c(\sigma_A\otimes I+I\otimes\sigma_B),
\]
and write its Schmidt coefficients as \(s_i\), with
\(x_i=s_i^2\).  There are at most three nonzero \(x_i\).
On the diagonal Schmidt block,
\[
 H_c=ss^\dagger-2c\operatorname{diag}(x_i).               \tag{2}
\]
The other eigenvalues are \(-c(x_i+x_j)\), \(-cx_i\), or
zero, according to whether zero, one, or two indices lie outside the
Schmidt support.

Take \(c=4/3\).  If the Schmidt rank is at most two, Cauchy--Schwarz
gives
\[
 ss^\dagger\preceq2\operatorname{diag}(x_i),
\]
so \(H_{4/3}\preceq0\), and every other block is also nonpositive.

Suppose the Schmidt rank is three and order
\(x_1\ge x_2\ge x_3>0\).  The \(c=1\), three-Schmidt-coordinate
calculation in Theorem 11.1 gives
\[
 \lambda_1(H_1)+\lambda_2(H_1)\le0.
\]
Since \(H_{4/3}\preceq H_1\), the same inequality holds for
\(H_{4/3}\).  Moreover
\[
 \frac43x_3I-H_{4/3}\succeq0.                            \tag{3}
\]
Indeed, the rank-one update criterion reduces (3) to
\[
 \frac34\sum_{i=1}^3\frac{x_i}{2x_i+x_3}\le1,
\]
and
\[
 \frac{x_1}{2x_1+x_3}
 +\frac{x_2}{2x_2+x_3}
 +\frac{x_3}{3x_3}
 \le\frac12+\frac12+\frac13=\frac43.
\]
Thus \(\lambda_1(H_{4/3})\le(4/3)x_3\).  Every eigenvalue
outside the diagonal block is at most \(-(4/3)x_3\).
The sum of the two largest eigenvalues of
\({\cal K}_{4/3,\psi}\) is therefore nonpositive: two diagonal
eigenvalues are controlled by their Ky--Fan sum, while a mixed pair is
controlled by (3).

The rank-two Ky--Fan variational principle now gives
\[
 \operatorname{Tr}(P{\cal K}_{4/3,\psi})\le0.
\]
The trace rearrangement used in Theorem 11.1 turns this into (1).

For optimality, let \(0<c<4/3\), choose
\[
 x_1=x_2=\frac{1-\varepsilon}{2},\qquad x_3=\varepsilon,
 \qquad
 0<\varepsilon<\min\left\{\frac13,\frac{4-3c}{3}\right\},
\]
and use the associated Schmidt vector in
\(\mathbb C^3\otimes\mathbb C^4\).  On the symmetric diagonal
subspace spanned by
\[
 e_+=\frac{|11\rangle+|22\rangle}{\sqrt2},\qquad |33\rangle,
\]
the matrix \(H_c\) is
\[
 \begin{pmatrix}
 (1-c)(1-\varepsilon)&\sqrt{\varepsilon(1-\varepsilon)}\\
 \sqrt{\varepsilon(1-\varepsilon)}&(1-2c)\varepsilon
 \end{pmatrix}.                                          \tag{4}
\]
At the spectral parameter \(c\varepsilon\), its characteristic
determinant is
\[
 c\varepsilon(3c-4+3\varepsilon)<0.                      \tag{5}
\]
Hence its larger eigenvalue \(\lambda_+\) satisfies
\(\lambda_+>c\varepsilon\).  The orthogonal unused-column vector
\(|3,4\rangle\) is an eigenvector of
\({\cal K}_{c,\psi}\) with eigenvalue \(-c\varepsilon\).
The projection onto these two eigenvectors therefore has
\[
 \operatorname{Tr}(P{\cal K}_{c,\psi})
 =\lambda_+-c\varepsilon>0.
\]
Thus every coefficient below \(4/3\) fails when \(m\ge4\).
\(\square\)

This sharp repair still does not close the pair-sector proof.  In the
equality example of Section 2, even coefficient one produces a
three-cut marginal sum four times larger than the hoped-for upper
bound; multiplying it by \(4/3\) only increases the loss.

The exact checker is
`verification/verify_n3_cut_projection_extension_obstruction.py`.
