# A sharp quantitative no-switching inequality for factor-plane pencils

## Status

This note proves an exact quantitative version of one algebraic step in
the three-copy Haar-equality exclusion.  Let \(f_\mu\) and \(g_\nu\)
be the two families of quadratic Plücker polynomials which test the two
possible factor types of a contracted two-plane.  If
\[
 a(z)=\sum_\mu |f_\mu(z)|^2,\qquad
 b(z)=\sum_\nu |g_\nu(z)|^2,
\]
then
\[
 \boxed{\qquad
 \mathbb E_z[a(z)b(z)]
 \geq \frac25\,\mathbb E_z a(z)\,\mathbb E_z b(z).
 \qquad}                                                   \tag{1}
\]
The constant \(2/5\) is sharp.

Thus a factor-plane pencil cannot switch rapidly between its two
factor types while keeping the product of their Plücker defects small:
small averaged product forces one complete family of minors to have
small averaged mass.

This is a genuine quantitative common-origin constraint.  It uses
that both minor families are homogeneous quadratics in the same
contraction variable \(z\).  Pointwise estimates which regard the
two families independently do not imply (1).

The result does not yet settle unrestricted three-copy positivity.
The remaining stability step is to derive either

1. lower bounds for both \(\mathbb E a\) and \(\mathbb E b\) from the
   one-site marginal floor at a negative minimizer; or
2. an upper bound for \(\mathbb E(ab)\) from the simultaneous
   near-kernel block Grams.

The dependency-free checker
`verification/verify_n3_factor_pencil_product_gap.py` audits the
symmetrizer identity, the dimensions producing \(2/5\), and an exact
sharp example.

## 1. The scalar quadratic inequality

Let \(V=\mathbb C^3\), and identify a homogeneous quadratic
polynomial with a tensor \(f\in\operatorname{Sym}^2V\):
\[
 f(z)=\langle \overline z^{\otimes2},f\rangle.
 \tag{2}
\]
Write \(P_4\) for the orthogonal projection of \(V^{\otimes4}\) onto
\(\operatorname{Sym}^4V\).  Since \(z^{\otimes4}\) is symmetric, the
tensor representing the product polynomial \(f(z)g(z)\) is
\[
 P_4(f\otimes g).
 \tag{3}
\]

### Lemma 1

For every \(f,g\in\operatorname{Sym}^2V\),
\[
\boxed{
\begin{aligned}
 6\|P_4(f\otimes g)\|^2
 ={}&\|f\|^2\|g\|^2+|\langle f,g\rangle|^2\\
 &+4\operatorname{Tr}(\rho_f\rho_g),
\end{aligned}}
\tag{4}
\]
where
\[
 \rho_f=\operatorname{Tr}_2|f\rangle\langle f|,
 \qquad
 \rho_g=\operatorname{Tr}_2|g\rangle\langle g|.
\tag{5}
\]
In particular,
\[
 \|P_4(f\otimes g)\|^2
 \geq\frac16\|f\|^2\|g\|^2.
\tag{6}
\]

### Proof

The tensor \(f\otimes g\) is invariant under the subgroup
\[
 S_{\{1,2\}}\times S_{\{3,4\}}\subset S_4.
\]
Consequently the \(24\) terms in the full symmetrizer collapse into
the six choices of the two output positions occupied by the first
quadratic tensor:
\[
 \|P_4(f\otimes g)\|^2
 =
 \frac16\sum_{\substack{A\subset\{1,2,3,4\}\\|A|=2}}
 \langle f\otimes g,U_A(f\otimes g)\rangle.
\tag{7}
\]
The unchanged partition contributes
\(\|f\|^2\|g\|^2\), and the exchanged partition contributes
\(|\langle f,g\rangle|^2\).  Each of the four crossing partitions
contributes
\[
 \sum_{i,j,k,\ell}
 \overline{f_{ij}}f_{ik}\,
 \overline{g_{k\ell}}g_{j\ell}
 =
 \operatorname{Tr}(\rho_f\rho_g).
\tag{8}
\]
Both reduced operators in (5) are positive semidefinite, so
\(\operatorname{Tr}(\rho_f\rho_g)\geq0\).  Equations (7)--(8) prove
(4), and discarding the last two nonnegative terms proves (6).
\(\square\)

Let \(z\) be Haar-uniform on the unit sphere of \(\mathbb C^3\).
For \(h\in\operatorname{Sym}^kV\),
\[
 \mathbb E_z|\langle\overline z^{\otimes k},h\rangle|^2
 =
 \frac{\|h\|^2}{\dim\operatorname{Sym}^kV}.
\tag{9}
\]
Here
\[
 \dim\operatorname{Sym}^2V=6,\qquad
 \dim\operatorname{Sym}^4V=15.
\tag{10}
\]
Applying (9) to (3) and then using (6) gives
\[
\begin{aligned}
 \mathbb E|f(z)g(z)|^2
 &=\frac1{15}\|P_4(f\otimes g)\|^2\\
 &\geq\frac1{90}\|f\|^2\|g\|^2\\
 &=\frac25\,
 \mathbb E|f(z)|^2\,\mathbb E|g(z)|^2.
\end{aligned}
\tag{11}
\]

The constant is sharp.  Take orthonormal vectors \(e_1,e_2\) and
\[
 f=e_1^{\otimes2},\qquad g=e_2^{\otimes2}.
\tag{12}
\]
Then \(\langle f,g\rangle=0\) and
\(\rho_f\rho_g=0\), so equality holds in (6) and (11).

## 2. Vector-valued Plücker families

Let \((f_\mu)_\mu\) and \((g_\nu)_\nu\) be arbitrary finite families
in \(\operatorname{Sym}^2\mathbb C^3\), and put
\[
 a(z)=\sum_\mu|f_\mu(z)|^2,\qquad
 b(z)=\sum_\nu|g_\nu(z)|^2.
\tag{13}
\]
Applying (11) to every pair \((\mu,\nu)\) and summing proves
\[
\begin{aligned}
 \mathbb E[a(z)b(z)]
 &=\sum_{\mu,\nu}\mathbb E|f_\mu(z)g_\nu(z)|^2\\
 &\geq\frac25
 \left(\sum_\mu\mathbb E|f_\mu(z)|^2\right)
 \left(\sum_\nu\mathbb E|g_\nu(z)|^2\right),
\end{aligned}
\]
which is (1).

## 3. Application to contracted singular planes

Let
\[
 {\boldsymbol X}\in
 H_1\otimes H_2\otimes H_3\otimes K,
 \qquad
 H_i\simeq\mathbb C^3,\quad K\simeq\mathbb C^2,
\tag{14}
\]
encode a two-dimensional singular plane, and contract the first
physical factor:
\[
 X(z)=(\langle z|\otimes I){\boldsymbol X}
 \in H_2\otimes H_3\otimes K.
\tag{15}
\]
Regard \(X(z)\) first as a \(3\times6\) matrix across
\[
 H_2:(H_3\otimes K)
\]
and then as a \(3\times6\) matrix across
\[
 H_3:(H_2\otimes K).
\]
Let \(f_\mu(z)\) be all \(2\times2\) minors of the first flattening
and \(g_\nu(z)\) all \(2\times2\) minors of the second.  Every minor
is a homogeneous quadratic in \(z\).

The first minor family vanishes identically at \(z\) exactly when
\(X(z)\) has a fixed \(H_2\) factor; the second vanishes exactly when
it has a fixed \(H_3\) factor.  Therefore (1) is the sharp averaged
inequality
\[
 \boxed{\quad
 \mathbb E_z
 \left[
 \|\wedge^2_{H_2}X(z)\|^2
 \,\|\wedge^2_{H_3}X(z)\|^2
 \right]
 \geq
 \frac25
 \mathbb E_z\|\wedge^2_{H_2}X(z)\|^2\,
 \mathbb E_z\|\wedge^2_{H_3}X(z)\|^2.
 \quad}
\tag{16}
\]
Here each squared wedge norm means the sum of squared flattening
minors, with the same convention on both sides.

At exact zero, (16) recovers the irreducibility argument used in the
Haar-equality proof: if the product vanishes for every \(z\), then
one complete minor family vanishes identically.  Quantitatively, it
prevents a near-zero product from being explained by alternating
between the two factor types on different regions of
\(\mathbb{CP}^2\).
