# Code-output compression and the erasure-decoupled square-zero gap

## Status

This note does **not** prove the unrestricted square-zero theorem.  It
gives an exact one-code operator formulation of that theorem and proves
a uniform spectral gap on the one-site erasure-decoupled locus.

Let
\[
 {\cal H}=(\mathbb C^3)^{\otimes3},\qquad K=\mathbb C^2,
\]
and define
\[
 L(A)=A-\frac12\operatorname{Tr}(A)I_3,\qquad
 \Phi(A)=\operatorname{Tr}(A)I_3-\frac12A.
\]
For an isometry \(W:K\to{\cal H}\), with columns \(w_0,w_1\), put
\[
 |\Psi_W\rangle=\sum_{b=0}^1|b\rangle_K|w_b\rangle,\qquad
 M_W=(\operatorname{id}_K\otimes\Phi^{\otimes3})
       (|\Psi_W\rangle\langle\Psi_W|).
\tag{1}
\]

The first result eliminates the second two-plane:
\[
\boxed{
 Q_3(UBW^\dagger)\geq0
 \quad\hbox{for every }U^\dagger W=0,\ B\in M_2
 \iff
 P_{K\otimes W^\perp}M_WP_{K\otimes W^\perp}\succeq0.}
\tag{2}
\]

The second result is a strict theorem on a natural interior locus.  Say
that \(W\) is **one-site erasure decoupled** if
\[
 \operatorname{Tr}_{\widehat i}|w_a\rangle\langle w_b|
 =\delta_{ab}\frac{I_3}{3}
 \quad(i=1,2,3;\ a,b=0,1).
\tag{3}
\]
Then
\[
\boxed{
 P_{K\otimes W^\perp}M_WP_{K\otimes W^\perp}
 \succeq\frac12P_{K\otimes W^\perp}.}
\tag{4}
\]
Consequently the endpoint Gram \(G(U,W)\) on
\(\operatorname{Hom}(\operatorname{ran}W,\operatorname{ran}U)\)
satisfies
\[
\boxed{G(U,W)\succeq\frac12I_4,\qquad
       \det G(U,W)\geq\frac1{16}.}
\tag{5}
\]
The same conclusion holds if \(U\), rather than \(W\), is
erasure decoupled.

This proves, on the erasure-decoupled locus, the currently conjectured
product-determinant strengthening
\[
\boxed{
 \det G(U,W)\geq
 \frac{3^{18}}{2^{22}}
 \prod_{i=1}^3
 \det\rho_i^U\,\det\rho_i^W,\qquad
 \rho_i^U=\operatorname{Tr}_{\widehat i}(UU^\dagger).}
\tag{6}
\]
It does not prove (6), or even \(\det G\geq0\), for general orthogonal
two-planes.

The dependency-free rational checker is
`verification/verify_n3_squarezero_code_output_compression.py`.

## 1. Exact code-output identity

For \(z_0,z_1\in{\cal H}\), set
\[
 |z\rangle=\sum_{b=0}^1|b\rangle_K|z_b\rangle,\qquad
 C_z=\sum_{b=0}^1|z_b\rangle\langle w_b|.
\tag{7}
\]
The local identity
\[
\begin{aligned}
 \langle x|\Phi(|w\rangle\langle w'|)|x'\rangle
 &=
 \langle x|x'\rangle\langle w'|w\rangle
 -\frac12\langle x|w\rangle\langle w'|x'\rangle\\
 &=
 \left\langle
 |x\rangle\langle w|,
 L(|x'\rangle\langle w'|)
 \right\rangle_{\rm HS}
\end{aligned}
\tag{8}
\]
tensorizes over the three physical sites.  Expanding (1) in its
logical matrix blocks therefore gives
\[
\boxed{\langle z|M_W|z\rangle=Q_3(C_z).}
\tag{9}
\]

Now assume \(U^\dagger W=0\).  For \(B\in M_2\), take
\[
 z_b=UB|b\rangle.
\tag{10}
\]
Then \(C_z=UBW^\dagger\) and
\(|z\rangle\in K\otimes W^\perp\).  Conversely, every vector in
\(K\otimes W^\perp\) has two physical components \(z_0,z_1\).
Their span has dimension at most two, so it is contained in the range
of an isometry \(U:K\to W^\perp\), after padding when necessary.
The two coordinate columns form a matrix \(B\) satisfying (10).
This proves both directions of (2).

For a fixed \(U\), the map
\[
 J_U:\operatorname{vec}(B)\longmapsto
 \sum_b|b\rangle_KUB|b\rangle
\tag{11}
\]
is an isometry, and
\[
 G(U,W)=J_U^\dagger M_WJ_U.
\tag{12}
\]
Thus (2) is also an exact principal-compression formulation of every
four-dimensional crossed endpoint Gram.

## 2. Inclusion-exclusion output on the orthogonal complement

Write
\[
 \rho_{KS}^W
 =\operatorname{Tr}_{\widehat S}
   |\Psi_W\rangle\langle\Psi_W|.
\]
Since \(W\) is an isometry,
\(\rho_K^W=I_K\).  Expanding the three local maps
\(\Phi=E-\tfrac12\operatorname{id}\), where
\(E(A)=\operatorname{Tr}(A)I\), gives
\[
\boxed{
\begin{aligned}
 M_W={}&I_{K{\cal H}}
 -\frac12\sum_i
   \bigl(\rho_{Ki}^W\otimes I_{\widehat i}\bigr)\\
 &+\frac14\sum_{i<j}
   \bigl(\rho_{Kij}^W\otimes I_{\widehat{\{i,j\}}}\bigr)
 -\frac18|\Psi_W\rangle\langle\Psi_W|.
\end{aligned}}
\tag{13}
\]
All tensor factors in (13) are embedded in their original party
order.

Let
\[
 P_\perp=I_K\otimes P_{W^\perp}.
\]
The physical support of \(|\Psi_W\rangle\) is \(\operatorname{ran}W\),
so
\[
 P_\perp|\Psi_W\rangle=0.
\tag{14}
\]
Consequently (13) reduces losslessly to
\[
\boxed{
\begin{aligned}
 P_\perp M_WP_\perp
 =P_\perp\left[
 I-\frac12\sum_i\rho_{Ki}^W\otimes I_{\widehat i}
 +\frac14\sum_{i<j}
 \rho_{Kij}^W\otimes I_{\widehat{\{i,j\}}}
 \right]P_\perp .
\end{aligned}}
\tag{15}
\]
This is the promised one-code formulation: the independent plane
\(U\) and coefficient matrix \(B\) have disappeared.

## 3. Uniform gap under erasure decoupling

Under (3),
\[
 \rho_{Ki}^W
 =\sum_{a,b}|a\rangle\langle b|\otimes
   \operatorname{Tr}_{\widehat i}|w_a\rangle\langle w_b|
 =\frac13I_K\otimes I_3.
\tag{16}
\]
After embedding in \(K\otimes{\cal H}\), every summand in the first
sum of (15) is \(I/3\).  Hence the identity and one-site terms in
(15) equal \(I/2\).  Every two-site reduction is positive, so
\[
\begin{aligned}
 P_\perp M_WP_\perp
 &=
 \frac12P_\perp
 +\frac14\sum_{i<j}
 P_\perp
 \bigl(\rho_{Kij}^W\otimes
 I_{\widehat{\{i,j\}}}\bigr)
 P_\perp\\
 &\succeq\frac12P_\perp.
\end{aligned}
\tag{17}
\]
This proves (4).  Compressing (17) with the isometry \(J_U\) proves
(5).  Finally,
\[
 Q_3(C^\dagger)=Q_3(C)
\tag{18}
\]
follows either from the partial-trace formula or from adjoint
preservation of \(L^{\otimes3}\).  Applying the already proved result
to \(C^\dagger=WB^\dagger U^\dagger\) proves the assertion when \(U\)
is erasure decoupled.

### 3.1 Dimension-uniform form

The preceding gap mechanism is not special to qutrits.  Let
\[
 {\cal H}_d=(\mathbb C^d)^{\otimes3},\qquad d\geq3,
\]
retain
\[
 \Phi_d(A)=\operatorname{Tr}(A)I_d-\frac12A,
\]
and assume the dimension-\(d\) erasure condition
\[
 \operatorname{Tr}_{\widehat i}|w_a\rangle\langle w_b|
 =\delta_{ab}\frac{I_d}{d}.
\tag{19}
\]
The code-output identity (9), the inclusion-exclusion formula (13),
and annihilation of the rank-one term on \(K\otimes W^\perp\) are
unchanged.  Now each embedded one-site output equals \(I/d\), while
the pair outputs remain positive.  Therefore
\[
\boxed{
\begin{aligned}
 P_\perp M_W^{(d)}P_\perp
 &=
 \left(1-\frac{3}{2d}\right)P_\perp\\
 &\quad+\frac14\sum_{i<j}
 P_\perp\bigl(\rho_{Kij}^W\otimes
 I_{\widehat{\{i,j\}}}\bigr)P_\perp\\
 &\succeq
 \left(1-\frac{3}{2d}\right)P_\perp .
\end{aligned}}
\tag{20}
\]
Consequently, for every orthogonal two-code \(U\),
\[
\boxed{
 G_d(U,W)\succeq
 \left(1-\frac{3}{2d}\right)I_4.}
\tag{21}
\]
At \(d=3\), this is exactly (4)--(5).  This dimension-uniform
decomposition is potentially useful beyond the qutrit determinant
program: its strict part is independent of the copywise pair-output
geometry.

## 4. Product determinant consequence and equality

Every \(\rho_i^U\) is positive and has trace two.  Arithmetic--geometric
mean on its three eigenvalues gives
\[
 \det\rho_i^U\leq\left(\frac23\right)^3=\frac8{27},
\tag{22}
\]
with equality exactly when \(\rho_i^U=2I_3/3\).  The same holds for
\(W\).  Therefore
\[
 \frac{3^{18}}{2^{22}}
 \prod_i\det\rho_i^U\det\rho_i^W
 \leq
 \frac{3^{18}}{2^{22}}
 \left(\frac8{27}\right)^6
 =\frac1{16}.
\tag{23}
\]
Equation (5) now proves (6).

When \(W\) is erasure decoupled, equality in (6) requires and is
equivalent to all of the following:

1. \(\rho_i^U=2I_3/3\) for every \(i\) (the corresponding statement
   for \(W\) already follows from (3));
2. \(G(U,W)=I_4/2\);
3. every positive pair-output compression vanishes:
   \[
   J_U^\dagger
   \bigl(\rho_{Kij}^W\otimes
   I_{\widehat{\{i,j\}}}\bigr)J_U=0
   \quad(i<j).
   \tag{24}
   \]

Indeed, equality in (20) gives the balanced marginals.  Since every
eigenvalue of \(G\) is at least \(1/2\), equality
\(\det G=1/16\) forces all four eigenvalues to equal \(1/2\).
The positive-summand decomposition (17) then gives (21), and the
converse is immediate.
