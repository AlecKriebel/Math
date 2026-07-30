# Triple-Hodge Ky--Fan four duality

## Status

This note gives an exact reformulation of the remaining orthogonal
four-frame triple-Hodge question.  It does **not** prove the resulting
inequality.

Let
\[
 (A_p)_{ai}=2^{-1/2}\varepsilon_{pai},\qquad
 D_t=\sum_{p,q,r}t_{pqr}A_p\otimes A_q\otimes A_r .
\]
The following three assertions are equivalent:

1. for every \(t\in(\mathbb C^3)^{\otimes3}\),
   \[
   \boxed{\quad
   s_1(D_t)^2+s_2(D_t)^2+s_3(D_t)^2+s_4(D_t)^2
   \leq\frac12\|t\|^2 ;
   \quad}                                                \tag{1}
   \]
2. the all-locally-antisymmetric projection has squared norm at most
   \(1/2\) on every normalized bivector of Slater rank at most two;
3. every rank-four orthogonal projection \(P\) on
   \((\mathbb C^3)^{\otimes3}\) satisfies the operator marginal
   inequality
   \[
   \boxed{\quad
   P+\sum_i\widehat{P_i}
   -\sum_{i<j}\widehat{P_{ij}}\succeq0 ,
   \quad}                                                \tag{2}
   \]
   where \(P_i=\operatorname{Tr}_{\widehat i}P\),
   \(P_{ij}=\operatorname{Tr}_{\widehat{ij}}P\), and a hat denotes
   tensoring with identities on the omitted sites.

Because \(D_t\) is skew-symmetric, its singular values occur in
pairs.  If
\[
 \sigma_1\geq\sigma_2\geq\cdots
\]
are the distinct Takagi singular values, (1) is equivalently
\[
 \boxed{\qquad
 \sigma_1^2+\sigma_2^2\leq\frac14\|t\|^2 .
 \qquad}                                                 \tag{3}
\]

The conjecture is sharp.  Product tensors attain (1).  More generally,
the inequality is proved here whenever \(t\) has Schmidt rank at most
two across at least one one-site-versus-two-site cut.  If
\(t=a\otimes x\) and the two-qutrit tensor \(x\) has Schmidt rank at
most two, then equality holds.

The dependency-free exact boundary checker is
`verification/verify_n3_triple_hodge_kyfan4_duality.py`.

## 1. Exterior-algebra equivalence

Put \(H=(\mathbb C^3)^{\otimes3}\), and on \(H\otimes H\) let
\[
 {\mathsf G}={\mathsf A}_1{\mathsf A}_2{\mathsf A}_3,
 \qquad {\mathsf A}_i=\frac{I-F_i}{2}.
\]
The vectors \(\operatorname{vec}(A_p)\) form an orthonormal basis of
the local antisymmetric subspace.  Consequently
\[
 t\longmapsto\operatorname{vec}(D_t)
\]
is a Hilbert-space isometry from \(H\) onto
\(\operatorname{ran}{\mathsf G}\).  In particular,
\[
 \|D_t\|_2=\|t\|.                                       \tag{4}
\]
Because a tensor product of three skew-symmetric matrices is
skew-symmetric,
\[
 D_t^{\mathsf T}=-D_t.                                  \tag{5}
\]

Use normalized wedges
\[
 x\wedge y=\frac{x\otimes y-y\otimes x}{\sqrt2}.
\]
A unit bivector has Slater rank at most two precisely when its
skew coefficient matrix has rank at most four.  Skew Takagi
factorization writes a unit such bivector as
\[
 \omega=\alpha\,e_1\wedge e_2+\beta\,e_3\wedge e_4,
 \qquad |\alpha|^2+|\beta|^2=1,                         \tag{6}
\]
for an orthonormal four-frame.

For fixed \(t\), the largest squared overlap of
\(\operatorname{vec}(D_t)\) with a unit Slater-rank-at-most-two
bivector is the squared norm of the best rank-four skew truncation.
Skew Takagi factorization, or ordinary Eckart--Young followed by the
paired singular-value decomposition, gives exactly
\[
 \max_{\operatorname{Slater\,rank}(\omega)\leq2}
 |\langle\operatorname{vec}(D_t),\omega\rangle|^2
 =\sum_{j=1}^4s_j(D_t)^2
 =2(\sigma_1^2+\sigma_2^2).                             \tag{7}
\]
Maximizing first over \(t\), and using that
\(\operatorname{vec}(D_t)\) runs over the unit sphere of
\(\operatorname{ran}{\mathsf G}\), proves the equivalence of (1)
and the exterior assertion.

For an orthonormal four-frame \(u_0,u_1,w_0,w_1\), put
\[
 z_{01}={\mathsf G}(u_0\otimes w_1),\qquad
 z_{10}={\mathsf G}(u_1\otimes w_0).
\]
Since \(\operatorname{ran}{\mathsf G}\) is globally antisymmetric,
\[
 {\mathsf G}(u\wedge w)=\sqrt2\,{\mathsf G}(u\otimes w). \tag{8}
\]
Applying the exterior assertion to
\[
 \omega=\alpha\,u_0\wedge w_1+\beta\,u_1\wedge w_0
\]
therefore gives the desired stronger crossed Gram estimate
\[
 \boxed{\quad
 \lambda_{\max}
 \operatorname{Gram}(z_{01},z_{10})\leq\frac14 .
 \quad}                                                  \tag{9}
\]
In particular,
\[
 |\langle z_{01},z_{10}\rangle|\leq\frac18.             \tag{10}
\]
Indeed a \(2\times2\) Hermitian matrix \(K\) with
\(0\preceq K\preceq I/4\) has off-diagonal entry of modulus at most
\(1/8\), by applying the operator-norm bound to \(K-I/8\).

Thus (1) is exactly the missing coherent statement, rather than an
unrelated sufficient condition.

## 2. Rank-four projector dual

Define the qutrit antisymmetric channel
\[
 {\cal W}(X)=\frac12\bigl(\operatorname{Tr}(X)I-X^{\mathsf T}\bigr).
                                                               \tag{11}
\]
Up to a harmless full transpose,
\[
 D_t^\dagger D_t
 ={\cal W}^{\otimes3}(|t\rangle\langle t|).             \tag{12}
\]
The channel is self-adjoint up to the same transpose.  Ky--Fan
variation and (12) show that (1) is equivalent to
\[
 \|{\cal W}^{\otimes3}(P)\|_{\rm op}\leq\frac12          \tag{13}
\]
for every rank-four orthogonal projection \(P\).

Expand the three local copies of (11).  Since
\(\operatorname{Tr}P=4\),
\[
\begin{aligned}
8{\cal W}^{\otimes3}(P)
={}&4I-\sum_i\widehat{P_i}^{\,\mathsf T}
       +\sum_{i<j}\widehat{P_{ij}}^{\,\mathsf T}
       -P^{\mathsf T}.                                  \tag{14}
\end{aligned}
\]
The left side is positive.  Hence (13) is equivalent to
\[
 P^{\mathsf T}+\sum_i\widehat{P_i}^{\,\mathsf T}
-\sum_{i<j}\widehat{P_{ij}}^{\,\mathsf T}\succeq0.
\]
Taking the full transpose proves (2).

This formulation isolates the remaining nonlinear geometry:
(2) is false for general positive operators and even for rank-one
projections.  For example, a maximally entangled two-qutrit vector
tensored with a one-site vector gives two eigenvalues \(-1/3\) in
the left side of (2).  Thus a proof must use the common
four-dimensional range of one orthogonal projection.

## 3. Exact deficient-local-rank theorem

### Theorem

Suppose \(t\in(\mathbb C^3)^{\otimes3}\) has Schmidt rank at most two
across at least one one-site-versus-two-site cut.  Then
\[
 \boxed{\qquad
 \sum_{j=1}^4s_j(D_t)^2\leq\frac12\|t\|^2 .
 \qquad}                                                 \tag{15}
\]

### Proof

It is enough to use the third site as the deficient site.  Hodge
covariance under local qutrit unitaries lets us write
\[
 t=x_0\otimes|0\rangle+x_1\otimes|1\rangle,             \tag{16}
\]
where \(x_0,x_1\in(\mathbb C^3)^{\otimes2}\) and
\[
 \|x_0\|^2+\|x_1\|^2=\|t\|^2.                           \tag{17}
\]
Put
\[
 B_r=D_{x_r}
 =\sum_{p,q}(x_r)_{pq}A_p\otimes A_q,\qquad r=0,1.
\]
Each \(B_r\) is complex symmetric, since it is a linear combination
of tensor products of two skew-symmetric matrices.

In the last-site basis, the explicit epsilon matrices put \(D_t\),
up to harmless row and column signs, in the block form
\[
 D_t=\frac1{\sqrt2}
 \begin{pmatrix}
 0&0&B_1\\
 0&0&B_0\\
 -B_1&-B_0&0
 \end{pmatrix}
 =\frac1{\sqrt2}
 \begin{pmatrix}
 0&C\\
 -C^{\mathsf T}&0
 \end{pmatrix},
 \qquad
 C=\begin{pmatrix}B_1\\B_0\end{pmatrix}.                \tag{18}
\]
The first displayed matrix has \(9\times9\) entries, while the second
uses the \(18+9\) decomposition.

The singular values of the off-diagonal matrix in (18) are the
singular values of \(C\), each repeated twice.  Therefore
\[
 \sum_{j=1}^4s_j(D_t)^2
 =\lambda_1(C^\dagger C)+\lambda_2(C^\dagger C),        \tag{19}
\]
where
\[
 C^\dagger C=B_0^\dagger B_0+B_1^\dagger B_1.          \tag{20}
\]

For positive matrices, the sum of the two largest eigenvalues is a
subadditive norm.  The homogeneous sharp double-Hodge spectral lemma
gives
\[
\begin{aligned}
\lambda_1(C^\dagger C)+\lambda_2(C^\dagger C)
&\leq
\sum_{r=0}^1
\left[
\lambda_1(B_r^\dagger B_r)+
\lambda_2(B_r^\dagger B_r)
\right]\\
&\leq\frac12\left(\|x_0\|^2+\|x_1\|^2\right)
=\frac12\|t\|^2 .
\end{aligned}                                           \tag{21}
\]
This proves the theorem. \(\square\)

Consequently, a counterexample to (1), (2), or (9) must have all
three one-body reduced density matrices of \(t\) positive definite.
This is an exact nonlinear boundary exclusion, not a numerical
rank assumption.

## 4. Exact equality family

Suppose
\[
 t=a\otimes x,
\qquad \|a\|=\|x\|=1 .
\]
Hodge covariance lets us take \(a=|0\rangle\), and then
\[
 D_t=A_0\otimes D_x.                                    \tag{22}
\]
The nonzero squared singular values of \(A_0\) are
\((1/2,1/2)\).  If
\(\mu_1\geq\mu_2\geq\cdots\) are the squared singular values of
\(D_x\), (15) gives
\[
 \sum_{j=1}^4s_j(D_t)^2=\mu_1+\mu_2.                    \tag{23}
\]
The established sharp double-Hodge spectral lemma gives
\[
 \mu_1+\mu_2\leq\frac12.                                \tag{24}
\]
Thus (1) holds for every tensor with a one-site factor.

If the coefficient matrix of \(x\) has Schmidt rank at most two,
put its nonzero singular values in the form
\(\sigma_1,\sigma_2\), with
\(\sigma_1^2+\sigma_2^2=1\).  In the exact block decomposition of
the double-Hodge matrix, its diagonal block has eigenvalues
\((1/2,-1/2,0)\).  Therefore
\[
 \mu_1=\mu_2=\frac14,
\]
and (16) is an equality.  In particular every product tensor
attains the constant \(1/2\) in (1).

Unrestricted complex alternating maximization consistently reaches
only this boundary value, and its converged equality tensors factor
at one site.  That observation is discovery evidence only.  The
unresolved theorem is precisely (2), or equivalently (1), on the
full-local-rank locus.
