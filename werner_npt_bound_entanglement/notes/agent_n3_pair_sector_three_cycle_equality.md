# A genuine three-component equality and its cycle SOS

## Status

This note gives an exact pair-sector equality in which all three pair
components are nonzero.  Its \(3\times3\) deficit matrix has positive
\(2\times2\) principal minors but zero full determinant.  The equality
therefore lives on the genuinely cyclic frontier isolated in
`agent_n3_pair_sector_three_component_determinant.md`; it is not a
two-component face in disguise.

The example also exactly disproves the normalized row-contraction
strengthening
\[
 \frac{|c_{ij}|}{\sqrt{d_id_j}}+
 \frac{|c_{ik}|}{\sqrt{d_id_k}}\leq1.                    \tag{1}
\]
Thus neither fixed normalized diagonal dominance nor an independent
two-edge residual contraction can prove the determinant theorem.

The construction belongs to a sparse family for which the determinant
reduces to one ordinary Cauchy--Schwarz inequality.  This identifies a
concrete local three-cycle motif which a global SOS would have to
assemble coherently.

The dependency-free exact checker is
`verification/verify_n3_pair_sector_three_cycle_equality.py`.

## 1. The code plane and pair coefficients

Use sites \(1,2,3\), and let
\[
 u=|000\rangle,\qquad
 v=\frac{|110\rangle+|012\rangle}{\sqrt2}.               \tag{2}
\]
The map \(V:\mathbb C^2\to(\mathbb C^3)^{\otimes3}\) with columns
\((u,v)\) is an isometry.

Put
\[
 \begin{aligned}
 Z&=\operatorname{diag}(1,-1,0),\\
 S&=\operatorname{diag}(1,0,-1),\\
 E&=|2\rangle\langle0|,\qquad
 F=|1\rangle\langle0|.
 \end{aligned}                                           \tag{3}
\]
All four matrices are traceless.  Define
\[
 \begin{aligned}
 D_{\widehat1}&=I\otimes Z\otimes E,
 &B_{\widehat1}&=Z\otimes E,\\
 D_{\widehat2}&=Z\otimes I\otimes E+
                  F\otimes I\otimes S,
 &B_{\widehat2}&=Z\otimes E+F\otimes S,\\
 D_{\widehat3}&=F\otimes Z\otimes I,
 &B_{\widehat3}&=F\otimes Z.
 \end{aligned}                                           \tag{4}
\]
Each \(B_{\widehat i}\) is doubly traceless on its two
non-spectator sites.  Moreover,
\[
 \|B_{\widehat1}\|_2^2=2,\qquad
 \|B_{\widehat2}\|_2^2=4,\qquad
 \|B_{\widehat3}\|_2^2=2.                                \tag{5}
\]
The two summands of \(B_{\widehat2}\) are Hilbert--Schmidt
orthogonal.

## 2. Exact contraction

Let \(X_i=D_{\widehat i}V\).  On the two code columns,
\[
 \begin{array}{c|cc}
 &u&v\\ \hline
 X_1&|002\rangle&-|112\rangle/\sqrt2\\
 X_2&|002\rangle+|100\rangle&-\sqrt2\,|112\rangle\\
 X_3&|100\rangle&-|112\rangle/\sqrt2 .
 \end{array}                                             \tag{6}
\]
Consequently
\[
 \|X_1\|_2^2=\frac32,\qquad
 \|X_2\|_2^2=4,\qquad
 \|X_3\|_2^2=\frac32,                                    \tag{7}
\]
and
\[
 c_{12}=2,\qquad c_{23}=2,\qquad c_{13}=\frac12.         \tag{8}
\]
The residual diagonal entries
\[
 d_i=2\|B_{\widehat i}\|_2^2-\|X_i\|_2^2                 \tag{9}
\]
are therefore
\[
 (d_1,d_2,d_3)=\left(\frac52,4,\frac52\right).           \tag{10}
\]

The full deficit matrix is
\[
 M=
 \begin{pmatrix}
 5/2&-2&-1/2\\
 -2&4&-2\\
 -1/2&-2&5/2
 \end{pmatrix}.                                         \tag{11}
\]
It has the exact Gram/SOS factorization
\[
 \boxed{\quad
 M=
 \begin{pmatrix}1\\-2\\1\end{pmatrix}
 \begin{pmatrix}1&-2&1\end{pmatrix}
 \frac32
 \begin{pmatrix}1\\0\\-1\end{pmatrix}
 \begin{pmatrix}1&0&-1\end{pmatrix}.
 \quad}                                                   \tag{12}
\]
Thus, for arbitrary \(\lambda\in\mathbb C^3\),
\[
 \lambda^\dagger M\lambda
 =
 |\lambda_1-2\lambda_2+\lambda_3|^2
 +\frac32|\lambda_1-\lambda_3|^2.                        \tag{13}
\]
In particular,
\[
 \operatorname{spec}M=\{0,3,6\},\qquad
 \ker M=\mathbb C(1,1,1).                                \tag{14}
\]
Every \(2\times2\) principal determinant equals \(6\), while
\(\det M=0\).

The kernel has a direct output meaning.  Equation (6) gives
\[
 \begin{aligned}
 (D_{\widehat1}+D_{\widehat2}+D_{\widehat3})u
 &=2|002\rangle+2|100\rangle,\\
 (D_{\widehat1}+D_{\widehat2}+D_{\widehat3})v
 &=-2\sqrt2\,|112\rangle.
 \end{aligned}                                           \tag{15}
\]
Hence the squared output norm is \(8+8=16\), exactly equal to
\[
 2\sum_i\|B_{\widehat i}\|_2^2=2(2+4+2)=16.              \tag{16}
\]
This is a true equality of the three-component Ky--Fan problem.

## 3. Exact obstruction to normalized diagonal dominance

At the middle row, (1) becomes
\[
 \frac2{\sqrt{4(5/2)}}+
 \frac2{\sqrt{4(5/2)}}
 =\frac4{\sqrt{10}}>1,                                  \tag{17}
\]
because \(16>10\).  Nevertheless \(M\succeq0\) by (12).

The failure is invariant under independent rescaling of the three
pair components in the sense relevant to the full theorem: such a
rescaling sends \(M\) to a diagonal congruence of (11), preserving
positive semidefiniteness, while no fixed normalization of the three
rows captures the kernel relation.  A successful Gram completion must
therefore select its diagonal scaling from the whole three-cycle.

## 4. The sparse cycle family

The preceding equality is the sharp point of a larger exact family.
Let
\[
 \begin{aligned}
 Z&=\operatorname{diag}(z_0,z_1,z_2),
 &z_0+z_1+z_2&=0,\\
 T&=\operatorname{diag}(a,b,c),
 &a+b+c&=0,\\
 S&=\operatorname{diag}(a,c,b),
 \end{aligned}                                           \tag{18}
\]
with real entries.  Keep the code (2), and replace (4) by
\[
 \begin{aligned}
 D_{\widehat1}&=I\otimes Z\otimes E,\\
 D_{\widehat2}&=T\otimes I\otimes E+
                  F\otimes I\otimes S,\\
 D_{\widehat3}&=F\otimes Z\otimes I .
 \end{aligned}                                           \tag{19}
\]
Direct contraction gives the symmetric deficit matrix
\[
 M(d,e,x,z)=
 \begin{pmatrix}
 d&-x&-z\\
 -x&e&-x\\
 -z&-x&d
 \end{pmatrix},                                         \tag{20}
\]
where
\[
 \begin{aligned}
 d&=z_0^2+\frac32z_1^2+2z_2^2,\\
 e&=2a^2+2b^2+4c^2,\\
 x&=z_0a+z_1b,\\
 z&=\frac12z_1^2.
 \end{aligned}                                           \tag{21}
\]
The antisymmetric outer mode has eigenvalue \(d+z\).  On the symmetric
outer mode and the middle component, the determinant is
\[
 e(d-z)-2x^2.                                            \tag{22}
\]
Consequently
\[
 \boxed{\quad
 \det M=(d+z)\bigl(e(d-z)-2x^2\bigr).
 \quad}                                                   \tag{23}
\]
Substituting (21) gives
\[
 e(d-z)-2x^2
 =
 2\left[
 (a^2+b^2+2c^2)(z_0^2+z_1^2+2z_2^2)
 -(z_0a+z_1b)^2
 \right]\geq0.                                           \tag{24}
\]
Indeed,
\[
 (z_0a+z_1b)^2
 \leq(a^2+b^2)(z_0^2+z_1^2)
 \leq
 (a^2+b^2+2c^2)(z_0^2+z_1^2+2z_2^2).                   \tag{25}
\]
Thus the full cyclic determinant is controlled by one local
profile-overlap Cauchy inequality.

The equality (3)--(4) is obtained from
\[
 (z_0,z_1,z_2)=(1,-1,0),\qquad
 (a,b,c)=(1,-1,0).                                      \tag{26}
\]
Both inequalities in (25) then saturate.

## 5. Structural implication

The two squares in (13) are a discrete second difference and an
outer antisymmetric difference.  Formula (24) shows their origin:
the dangerous cycle is an overlap between two traceless local
profiles, while the unused third profile coordinates provide the
Cauchy residual.

A global proof could therefore succeed by decomposing arbitrary
three-component contractions into orthogonal copies of this motif,
or by replacing that decomposition with a coordinate-free Gram map
whose local fibers are (24).  What is already excluded is any proof
which treats the two edges incident to one component as independent
normalized contractions.
