# The local-rank-two boundary of the unrestricted qutrit three-copy problem

## Status

This note uses the exact unrestricted qutrit two-copy theorem to remove
the entire local-rank-deficient boundary of the qutrit three-copy
problem.

Let
\[
 {\cal H}=(\mathbb C^3)^{\otimes3},\qquad
 X_3=I-\frac12|\Phi_3\rangle\langle\Phi_3|,
 \qquad |\Phi_3\rangle=\sum_{a=0}^2|aa\rangle .
\]
If \(C\) has rank at most two, write \(U=\operatorname{ran}C\) and
\(V=\operatorname{ran}C^\dagger\).  For a two-plane
\(W\subseteq{\cal H}\), its local support at site \(i\) is the support
of
\[
 \rho_i^W=\operatorname{Tr}_{\bar i}P_W .
\]

The result is:
\[
\boxed{\quad
 \operatorname{rank}\rho_i^U\leq2
 \ \hbox{or}\
 \operatorname{rank}\rho_i^V\leq2
 \ \hbox{for some }i
 \quad\Longrightarrow\quad Q_3(C)\geq0 .
\quad}                                                     \tag{1}
\]
For a genuine rank-two matrix on three qutrits, a negative witness
must therefore have
\[
 \det\rho_i^U>0,\qquad \det\rho_i^V>0
 \qquad(i=1,2,3).                                        \tag{2}
\]
This is a same-copy statement.  It does not use the long-flag or
copy-doubling reduction to projections.

## 1. A tensoring lemma for two-block positivity

### Lemma 1

Let \(Z\succeq0\) on \(A_0\otimes B_0\) be separable:
\[
 Z=\sum_j R_j\otimes S_j,\qquad R_j,S_j\succeq0.
\]
Let \(T\) on \(A_1\otimes B_1\) be two-block-positive.  Then
\[
 Z\otimes T
\]
is two-block-positive across
\((A_0A_1):(B_0B_1)\).

### Proof

It is enough to treat one summand \(R\otimes S\).  If
\(\operatorname{SR}(\psi)\leq2\), put
\[
 \phi=(R^{1/2}\otimes I_{A_1})
       \otimes(S^{1/2}\otimes I_{B_1})\psi .
\]
Local filtering does not increase Schmidt rank.  In product bases
\((e_a)\) of \(A_0\) and \((f_b)\) of \(B_0\), write
\[
 \phi=\sum_{a,b}e_a\otimes f_b\otimes\phi_{ab}.
\]
Every conditional vector \(\phi_{ab}\in A_1\otimes B_1\) has Schmidt
rank at most two: applying the two local coordinate functionals to a
two-term Schmidt decomposition of \(\phi\) leaves at most two product
terms.  Hence
\[
\begin{aligned}
 \langle\psi|(R\otimes S)\otimes T|\psi\rangle
 &=\langle\phi|I_{A_0B_0}\otimes T|\phi\rangle\\
 &=\sum_{a,b}\langle\phi_{ab}|T|\phi_{ab}\rangle\geq0.
\end{aligned}
\]
Summing over \(j\) proves the lemma. \(\square\)

## 2. The compressed one-site endpoint factor is separable

Let \(W\subseteq\mathbb C^3\) have dimension \(r\leq2\), and let
\(\overline W\) be its coordinatewise conjugate in the basis defining
\(\Phi_3\).  Put
\[
 |\Phi_W\rangle
 =(P_W\otimes I)|\Phi_3\rangle
 =\sum_{a=0}^{r-1}|w_a\rangle\otimes|\overline w_a\rangle
                                                               \tag{3}
\]
for any orthonormal basis \((w_a)\) of \(W\).  Compression on the first
side gives
\[
\begin{aligned}
 Z_W
 &:=(P_W\otimes I)X_3(P_W\otimes I)\\
 &=\left(
 I_W\otimes I_{\overline W}
 -\frac12|\Phi_W\rangle\langle\Phi_W|
 \right)
 +P_W\otimes P_{\overline W^\perp}.                       \tag{4}
\end{aligned}
\]

For \(r=0,1\), separability of (4) is immediate.  For \(r=2\), identify
\(W\) and \(\overline W\) with qubits in the bases used in (3).  Let
\(P_{\nu,s}\) be the rank-one spectral projection of the Pauli matrix
\(\nu\in\{x,y,z\}\) with eigenvalue \(s\in\{+1,-1\}\).  The exact
six-term identity
\[
\boxed{
\begin{aligned}
 I_4-\frac12|\Phi_2\rangle\langle\Phi_2|
 =\frac12\sum_{s=\pm1}\bigl(
 &P_{x,s}\otimes P_{x,-s}
 +P_{y,s}\otimes P_{y,s}\\
 &+P_{z,s}\otimes P_{z,-s}\bigr)
\end{aligned}}                                             \tag{5}
\]
is a separable decomposition.  To check it, use
\[
 |\Phi_2\rangle\langle\Phi_2|
 =\frac12(I\otimes I+X\otimes X-Y\otimes Y+Z\otimes Z).
\]
Equations (4)--(5) prove that \(Z_W\) is separable for every
\(\dim W\leq2\).

## 3. The boundary theorem

### Theorem 2

Let \(C\) be an operator of rank at most two on
\((\mathbb C^3)^{\otimes3}\).  If the range of \(C\) has local support
of dimension at most two at one of the three sites, then
\[
 Q_3(C)\geq0.                                             \tag{6}
\]
The same conclusion holds if the range of \(C^\dagger\) has such a
local support.

### Proof

Permute the sites so that the deficient support is at site \(1\), and
call it \(W\).  The coefficient vector
\[
 |\psi_C\rangle=\operatorname{vec}C
\]
then lies in
\[
 (W\otimes(\mathbb C^3)^{\otimes2})_A
 \otimes((\mathbb C^3)^{\otimes3})_B .
\]
Consequently
\[
\begin{aligned}
  Q_3(C)
  &=\langle\psi_C|X_3^{\otimes3}|\psi_C\rangle\\
  &=\langle\psi_C|
     Z_W\otimes X_3^{\otimes2}|\psi_C\rangle .            \tag{7}
\end{aligned}
\]

The unrestricted qutrit two-copy theorem says exactly that
\(X_3^{\otimes2}\) is two-block-positive.  Equation (4)--(5) says that
\(Z_W\) is separable and positive.  Lemma 1 applied to (7) proves
(6).

Finally,
\[
 Q_3(C^\dagger)=Q_3(C),
\]
because every simultaneous partial trace commutes with adjoints and
the Hilbert--Schmidt norm is adjoint-invariant.  Applying the first
part to \(C^\dagger\) proves the assertion about the right singular
plane. \(\square\)

For a two-plane \(U\), the support of \(\rho_i^U\) is exactly its local
support.  In local dimension three,
\(\operatorname{rank}\rho_i^U\leq2\) is equivalent to
\(\det\rho_i^U=0\).  This proves (1)--(2).

## 4. Consequences and limits

1. The remaining qutrit three-copy problem is an interior problem:
   all six one-site code reductions, three from each singular plane,
   must be positive definite.
2. The theorem is genuinely nonlinear in the common code plane.  It
   is not an averaging or fixed compression of the endpoint map.
3. The argument is same-copy and applies to unequal singular values
   and fully nonnormal matrices.
4. The theorem does not provide a uniform positive gap as a local
   determinant tends to zero.  Exact zero families live on this
   boundary, so such a gap cannot be assumed.
5. Extending (1) to arbitrary local dimensions would require the
   corresponding unrestricted two-copy theorem on the two untouched
   local spaces.  Only the qutrit conclusion is asserted here.
