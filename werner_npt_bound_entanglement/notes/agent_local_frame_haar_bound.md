# A sharp local-frame average bound for multiquadratic tensors

## Status

This note proves a basis-invariant replacement for the failed
fixed-Hodge-frame estimate.

Let `\(V_i=\mathbb C^3\)` and
\[
 f\in\bigotimes_{i=1}^n\operatorname{Sym}^2V_i.
\]
For local unitaries `\(g_i\in U(3)\)`, define
\[
 C_f(g_1,\ldots,g_n)
 =
 \sum_{k_1,\ldots,k_n=0}^2
 \left|
 f(g_1e_{k_1},g_1e_{k_1};\ldots;
   g_ne_{k_n},g_ne_{k_n})
 \right|.
 \tag{1}
\]
Then
\[
 \boxed{\qquad
 \mathbb E_{g_1,\ldots,g_n}C_f(g_1,\ldots,g_n)
 \geq\|f\|_2.
 \qquad}
 \tag{2}
\]
Consequently,
\[
 \boxed{\qquad
 \sup_{g_1,\ldots,g_n}C_f(g_1,\ldots,g_n)
 \geq\|f\|_2.
 \qquad}
 \tag{3}
\]

The constant one is sharp.  It is attained by a tensor product of
rank-one symmetric squares.

For the four-qutrit Hodge problem, the determinant polynomial sees only
the component of the raw polarized determinant tensor that is symmetric
under each of the four local label swaps.  Applying (3) to that component
is exact and automatic.  The unresolved issue is that complement balance
fixes the norm of the **raw** tensor at one, while the locally symmetric
component can have smaller norm: it is `\(\sqrt{5/12}\)` for the exact
balanced graph code and one for repetition.  Local frame changes commute
with the label swaps and cannot recover the inaccessible components.

## 1. A scalar quadratic estimate

Let `\(x\)` be uniformly distributed on the unit sphere of
`\(\mathbb C^3\)`.  If `\(A=A^T\)` is a complex symmetric matrix, then
\[
 \boxed{\qquad
 \mathbb E_x|x^TAx|\geq\frac13\|A\|_2.
 \qquad}
 \tag{4}
\]

### Proof

Take a standard circular complex Gaussian vector
`\(g=(g_1,g_2,g_3)\)`, normalized by
`\(\mathbb E|g_i|^2=1\)`.  Write
\[
 g=rx,
 \tag{5}
\]
where `\(x\)` is uniform on the unit sphere, `\(r\)` is independent of
`\(x\)`, and
\[
 \mathbb E r^2=3.
 \tag{6}
\]
Since the polynomial is homogeneous of degree two,
\[
 \mathbb E|g^TAg|=3\,\mathbb E|x^TAx|.
 \tag{7}
\]

By a unitary congruence, which preserves both the Gaussian law and the
Frobenius norm, write
\[
 g^TAg=\sum_{j=1}^3\lambda_jg_j^2,
 \qquad \lambda_j\geq0.
 \tag{8}
\]
Put `\(Z=\sum_j\lambda_jg_j^2\)`.  Its two-dimensional characteristic
function is radial.  Along a real radial parameter `\(t\)`, direct
Gaussian integration gives
\[
 \phi_Z(t)
 =\mathbb E e^{it\operatorname{Re}Z}
 =\prod_{j=1}^3(1+\lambda_j^2t^2)^{-1/2}.
 \tag{9}
\]
The elementary product inequality
\[
 \prod_j(1+\lambda_j^2t^2)
 \geq1+t^2\sum_j\lambda_j^2
 \tag{10}
\]
therefore gives
\[
 \phi_Z(t)
 \leq
 \left(1+t^2\sum_j\lambda_j^2\right)^{-1/2}.
 \tag{11}
\]

For a circular complex random variable `\(W\)` with finite first moment,
angular averaging of the elementary Fourier representation of the
Euclidean norm gives
\[
 \mathbb E|W|
 =c\int_0^\infty\frac{1-\phi_W(t)}{t^2}\,dt,
 \tag{12}
\]
where the positive universal constant `\(c\)` is independent of
`\(W\)`.  Only comparison is needed here, so its value is irrelevant.
The right side of (11) is the characteristic function of
\[
 W_0=\left(\sum_j\lambda_j^2\right)^{1/2}g_1^2.
 \]
Equations (11)--(12) imply
\[
 \mathbb E|Z|
 \geq\mathbb E|W_0|
 =\left(\sum_j\lambda_j^2\right)^{1/2}
 =\|A\|_2,
 \tag{13}
\]
because `\(\mathbb E|g_1^2|=\mathbb E|g_1|^2=1\)`.  Combining
(7) and (13) proves (4).  Equality holds when at most one
`\(\lambda_j\)` is nonzero. `\(\square\)`

## 2. The Hilbert-valued one-site lemma

Let `\(K\)` be a finite-dimensional Hilbert space and
\[
 T:\operatorname{Sym}^2\mathbb C^3\longrightarrow K
 \tag{14}
\]
be linear.  Then
\[
 \boxed{\qquad
 \mathbb E_x\|T(x\otimes x)\|_K
 \geq\frac13\|T\|_{\mathrm{HS}}.
 \qquad}
 \tag{15}
\]

### Proof

Put `\(M=T^\dagger T\succeq0\)`.  For a positive operator `\(M\)` define
\[
 \Phi(M)=
 \mathbb E_x
 \sqrt{\langle x^{\otimes2},M x^{\otimes2}\rangle}.
 \tag{16}
\]
The square root is concave, so `\(\Phi\)` is concave on the positive
cone.  If
\[
 M=\sum_a\mu_a|h_a\rangle\langle h_a|,
 \qquad \mu_a\geq0,\quad\|h_a\|=1,
 \tag{17}
\]
and `\(\tau=\operatorname{Tr}M\)`, concavity gives
\[
 \Phi(M)
 \geq
 \sqrt{\tau}\sum_a\frac{\mu_a}{\tau}
 \Phi(|h_a\rangle\langle h_a|).
 \tag{18}
\]
Identify each unit vector `\(h_a\in\operatorname{Sym}^2\mathbb C^3\)`
with a symmetric matrix of Frobenius norm one.  The scalar estimate (4)
gives
\[
 \Phi(|h_a\rangle\langle h_a|)\geq\frac13.
 \tag{19}
\]
Therefore
\[
 \Phi(M)\geq\frac13\sqrt{\operatorname{Tr}M}
 =\frac13\|T\|_{\mathrm{HS}},
 \]
which is (15). `\(\square\)`

## 3. Tensorization

Contract `\(f\)` successively against independent unit vectors
`\(x_i^{\otimes2}\)`.  Before the `\(i\)`-th contraction, regard the
current tensor as a linear map from
`\(\operatorname{Sym}^2V_i\)` into the Hilbert tensor product of the
remaining factors.  Lemma (15), conditionally on all earlier choices,
loses at most a factor `\(1/3\)` in expected norm.  Iterating gives
\[
 \boxed{\qquad
 \mathbb E_{x_1,\ldots,x_n}
 \left|
 f(x_1,x_1;\ldots;x_n,x_n)
 \right|
 \geq3^{-n}\|f\|_2.
 \qquad}
 \tag{20}
\]

Now let `\(g_i\)` be independent Haar unitaries.  Each individual column
`\(g_ie_k\)` is uniformly distributed on the unit sphere.  Correlations
between different columns do not matter after taking the expectation of
the sum in (1).  Hence
\[
\begin{aligned}
 \mathbb E_g C_f(g)
 &=3^n\,
 \mathbb E_{x_1,\ldots,x_n}
 \left|f(x_1,x_1;\ldots;x_n,x_n)\right|\\
 &\geq\|f\|_2.
\end{aligned}
\tag{21}
\]
This proves (2), and (3) follows because a supremum dominates an
average.

For
\[
 f=(a_1\otimes a_1)\otimes\cdots\otimes(a_n\otimes a_n),
 \tag{22}
\]
one has
\[
 C_f(g)=
 \prod_{i=1}^n\sum_{k=0}^2
 |\langle a_i,g_ie_k\rangle|^2
 =\prod_i\|a_i\|^2
 =\|f\|_2
 \tag{23}
\]
for every local frame.  Thus the constant in (2)--(3) is sharp.

## 4. Application and remaining obstruction

Let `\(T_{A,B}\)` be the raw polarized determinant tensor,
\[
 T_{A,B}
 =\frac12(a_Ad_B+a_Bd_A-b_Ac_B-b_Bc_A),
 \tag{24}
\]
where `\(A,B\in\{0,1,2\}^4\)` label products of local Hodge forms.
It is symmetric under the simultaneous exchange `\(A\leftrightarrow B\)`,
but it need not be symmetric under exchanging `\(A_i\leftrightarrow
B_i\)` at one site.

Let
\[
 f=P_+^{(1)}P_+^{(2)}P_+^{(3)}P_+^{(4)}T
 \in\bigotimes_{i=1}^4\operatorname{Sym}^2\mathbb C^3
 \tag{25}
\]
be the locally symmetric component.  Diagonal Hodge evaluation
annihilates all other local label-swap sectors, so
\[
 C(U;g_1,\ldots,g_4)=C_f(g_1,\ldots,g_4).
 \tag{26}
\]
The theorem gives the exact invariant lower bound
\[
 \boxed{\qquad
 \sup_{g_1,\ldots,g_4}C(U;g_1,\ldots,g_4)
 \geq\|f\|_2.
 \qquad}
 \tag{27}
\]

On the complement-balanced slice, exact computations indicate
\[
 \|T\|_2^2=1,
 \tag{28}
\]
but this does not imply `\(\|f\|_2\geq1\)`.  Local frame actions commute
with all four label swaps, so they cannot move norm from the other seven
even label sectors into (25).  Exact examples are
\[
\begin{array}{c|c|c}
\text{code}&\|T\|_2^2&\|f\|_2^2\\ \hline
\text{repetition}&1&1\\
\text{balanced graph}&1&5/12.
\end{array}
\tag{29}
\]
Thus (27) alone does not settle the balanced four-copy inequality.
The remaining task is a strengthened estimate for the special
five-dimensional affine Pluecker family of locally symmetric tensors,
or an exact identity transferring the inaccessible raw-sector norm into
a larger diagonal `\(\ell^1\)` average.

## Research log

- **2026-07-28 19:31 PDT.** Proved the sharp scalar quadratic
  first-moment estimate (4) by Gaussian characteristic-function
  comparison.
- **2026-07-28 19:38 PDT.** Extended it by concavity to Hilbert-valued
  quadratic maps and tensorized it, proving the universal local-frame
  average bound (2).
- **2026-07-28 19:43 PDT.** Identified the exact limitation for the Hodge
  application: only the all-locally-symmetric label sector is accessible
  to diagonal evaluation.
