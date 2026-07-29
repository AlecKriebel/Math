# Three-copy transverse determinant: an exact coupled-sector boundary

## Status

This note does **not** prove unrestricted three-copy positivity.  It records
an exact obstruction that every determinant, anchor-map, or Pluecker proof
must retain.

The corrected exterior defect splits algebraically into an odd-total-parity
bracket and an even-total-parity bracket.  It is tempting to prove the two
brackets separately.  The even bracket is false, by the fully transverse
rank-two family below.  At the displayed point the two brackets are exactly
\(1/2\) and \(-1/2\), while the true defect and \(Q_3\) both vanish.

The same example gives:

* disjoint, indeed orthogonal, left and right singular planes;
* a nonnormal square-zero rank-two coefficient matrix;
* an exact one-dimensional kernel of the \(4\times4\) two-plane matrix;
* an exact kernel vector of the state-dependent anchor operator.

The independent rational checker is
`verification/verify_n3_transverse_anchor_boundary.py`.

## 1. Replica-sector conventions

Let
\[
 {\cal A},{\cal B}\in K\otimes H_1\otimes H_2\otimes H_3,\qquad
 K\simeq\mathbb C^2,
\]
be normalized, put \(z={\cal A}\otimes{\cal B}\), and let
\[
 \Pi_i^\pm=\frac{I\pm F_i}{2}
\]
on the two replicas of party \(i\).  If \(k\in\{0,1\}\) and
\(R\subseteq\{1,2,3\}\), define
\[
 p_{k,R}
 =
 \left\|
 \Pi_K^{(-1)^k}
 \prod_{i\in R}\Pi_i^-
 \prod_{i\notin R}\Pi_i^+\,z
 \right\|^2,
 \qquad
 p_{k,r}=\sum_{|R|=r}p_{k,R}.                         \tag{1}
\]
Here \(\Pi_K^{(-1)^0}=\Pi_K^+\) and
\(\Pi_K^{(-1)^1}=\Pi_K^-\).

The corrected exterior operator from the sharp three-copy conjecture is
\[
 W=
 4F_K\sum_{i<j}\Pi_i^-\Pi_j^-
 \frac{I-F_KF_1F_2F_3}{2}.                              \tag{2}
\]
On a sector with auxiliary parity \(k\) and \(r\) physical minus signs,
its eigenvalue is
\[
 4(-1)^k\binom r2+\mathbf1_{\{k+r\ {\rm odd}\}}.
\]
Therefore
\[
\begin{aligned}
 \langle z,Wz\rangle
 &=
 \underbrace{p_{1,0}+p_{0,1}+13p_{0,3}-3p_{1,2}}_{D_{\rm odd}}\\
 &\quad+
 \underbrace{4p_{0,2}-12p_{1,3}}_{D_{\rm even}}.          \tag{3}
\end{aligned}
\]
The labels on the two brackets refer to the parity of the total number
\(k+r\) of antisymmetric replica pairs.

Equivalently, if
\[
 q_S=\operatorname{Tr}(\rho_{\cal A}^S\rho_{\cal B}^S)
     =\langle z,F_Sz\rangle ,
\]
then expansion of (2) gives the useful anchor form
\[
 \boxed{
 \langle z,Wz\rangle
 =
 3q_K-2\sum_iq_{Ki}+\sum_{i<j}q_{Kij}
 +\frac{1-|\langle{\cal A},{\cal B}\rangle|^2}{2}.
 }                                                        \tag{4}
\]
For fixed \({\cal A}\), this is
\[
 \langle{\cal B},M_{\cal A}{\cal B}\rangle,
\]
where
\[
 \boxed{
 M_{\cal A}
 =
 \frac12(I-|{\cal A}\rangle\langle{\cal A}|)
 +3\widehat\rho_K^{\cal A}
 -2\sum_i\widehat\rho_{Ki}^{\cal A}
 +\sum_{i<j}\widehat\rho_{Kij}^{\cal A}.
 }                                                        \tag{5}
\]
The hat means that the reduced density matrix is tensored with the
identity on the complementary parties and embedded back in the original
party order.

Universal positivity of (5) is exactly the live balanced anchor-map form
of the unrestricted problem; it is not assumed below.

## 2. Exact fully transverse family

All four local spaces are qubits in this construction.  On the three
physical qubits put
\[
\begin{aligned}
 u_1&=\frac{|000\rangle+|011\rangle}{\sqrt2},&
 u_2&=\frac{|100\rangle-|111\rangle}{\sqrt2},\\
 v_1&=\frac{|011\rangle-|000\rangle}{\sqrt2},&
 v_2&=\frac{|100\rangle+|111\rangle}{\sqrt2}.
\end{aligned}                                             \tag{6}
\]
Both displayed pairs are orthonormal and
\[
 \operatorname{span}\{u_1,u_2\}
 \perp
 \operatorname{span}\{v_1,v_2\}.                          \tag{7}
\]
Thus
\[
 C=|u_1\rangle\langle v_1|+|u_2\rangle\langle v_2|         \tag{8}
\]
has rank two, \(C^2=0\), and genuinely transverse left and right planes.

Introduce the equal-Schmidt purifications
\[
 {\cal A}=\frac{|0\rangle u_1+|1\rangle u_2}{\sqrt2},
 \qquad
 {\cal B}=\frac{|0\rangle v_1+|1\rangle v_2}{\sqrt2}.       \tag{9}
\]
Their \(K\)-marginals are both \(I_2/2\).  If
\[
 \varepsilon=
 \begin{pmatrix}0&1\\-1&0\end{pmatrix},
\]
then
\[
 {\cal B}=\varepsilon^{\otimes4}\overline{\cal A}.         \tag{10}
\]

Direct Walsh inversion of the sixteen swap moments gives
\[
\begin{array}{c|rrrr}
 &r=0&r=1&r=2&r=3\\ \hline
 k=0&5/16&3/8&1/16&0\\
 k=1&1/8&1/16&0&1/16 .
\end{array}                                                \tag{11}
\]
Consequently
\[
 \boxed{
 D_{\rm odd}=\frac12,\qquad
 D_{\rm even}=-\frac12,\qquad
 \langle z,Wz\rangle=0.
 }                                                        \tag{12}
\]
In particular, the candidate inequality
\[
 3p_{1,3}\le p_{0,2}
\]
fails by the exact factor three:
\[
 3p_{1,3}=\frac3{16}>\frac1{16}=p_{0,2}.                  \tag{13}
\]
The odd-total sectors supply exactly the missing \(1/2\).

## 3. Exact two-plane and anchor spectra

Let \(E_{ab}=|u_a\rangle\langle v_b|\).  The matrix of the endpoint
form on their span is
\[
 H_{ab,cd}={\cal B}_3(E_{ab},E_{cd}).
\]
Direct partial-trace contraction yields
\[
 \boxed{
 H=
 \begin{pmatrix}
 1/4&0&0&-1/4\\
 0&3/4&0&0\\
 0&0&3/4&0\\
 -1/4&0&0&1/4
 \end{pmatrix}.
 }                                                        \tag{14}
\]
Hence
\[
 \operatorname{spec}H=\{0,1/2,3/4,3/4\},                 \tag{15}
\]
and the kernel is spanned by
\(\operatorname{vec}I_2=(1,0,0,1)^T\), which reconstructs (8).
Thus \(Q_3(C)=0\) exactly.

The state-dependent operator (5) has the equally simple exact spectrum
\[
 \boxed{
 \operatorname{spec}M_{\cal A}
 =
 \{0,\ (1/2)^{\times5},\ 1^{\times8},\ (3/2)^{\times2}\}.
 }                                                        \tag{16}
\]
Its kernel is precisely \(\mathbb C{\cal B}\).  This shows why adding a
strict margin or proving the two parity brackets separately cannot work.

More generally, for three physical qubits and any isometry
\(U:\mathbb C^2\to(\mathbb C^2)^{\otimes3}\), the balanced purification
\[
 {\cal A}_U=\frac{|0\rangle U|0\rangle+|1\rangle U|1\rangle}{\sqrt2}
\]
obeys
\[
 M_{{\cal A}_U}\,
 \varepsilon^{\otimes4}\overline{{\cal A}_U}=0.            \tag{17}
\]
This follows directly because, on a qubit,
\[
 X-\frac12\operatorname{Tr}(X)I
\]
is the orthogonal projection onto traceless matrices.  Its third tensor
power is positive semidefinite, and the spin-flipped vector represents
the missing fully traceless component.  Equation (17) explains the large
zero manifold seen in discovery searches.  The special choice (6) makes
the two physical singular planes orthogonal and gives the transparent
rational data (11)--(16).

## Consequence

A successful transverse determinant proof must compare the odd and even
total-parity sectors jointly.  Neither
\[
 D_{\rm odd}\ge0,\qquad D_{\rm even}\ge0
\]
as two independent goals nor the stronger local estimate
\(3p_{1,3}\le p_{0,2}\) can prove the theorem.  At a generic embedded
qubit boundary, the determinant has a genuine zero direction generated
by the four-party spin flip.
