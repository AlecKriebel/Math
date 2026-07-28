# The two-plane compression bound is false

This note analyzes the proposed bound
\[
2\left\|(P_U\otimes P_V)R_n(P_U\otimes P_V)\right\|_{\rm op}
\mathrel{\stackrel{?}{\leq}}
\operatorname{Tr}\!\left((P_U\otimes P_V)R_n\right),
\qquad
R_n=\left(I-\frac12F\right)^{\otimes n},
\tag{1}
\]
where \(U,V\) are two-dimensional subspaces of
\((\mathbb C^d)^{\otimes n}\).  There is an exact counterexample already
for \(n=2\), supported on two local basis states.  The failure therefore
persists in every \(d\geq2\).

The note also isolates the strictly weaker compression inequality which
is actually equivalent to nonnegativity on equal-Schmidt-coefficient
rank-two matrices.

## 1. Exact two-copy counterexample

Use only the local states \(|0\rangle,|1\rangle\), and put
\[
|s\rangle=\frac{|01\rangle+|10\rangle}{\sqrt2}.
\]
In the two-copy physical space set
\[
U=\operatorname{span}\{u_1,u_2\},
\quad
u_1=|00\rangle,\quad u_2=|s\rangle,
\]
\[
V=\operatorname{span}\{v_1,v_2\},
\quad
v_1=|11\rangle,\quad v_2=|s\rangle.
\tag{2}
\]
The displayed bases are orthonormal.  Let
\[
K=(P_U\otimes P_V)R_2(P_U\otimes P_V)
\]
be represented in the ordered basis
\[
u_1\otimes v_1,\quad
u_1\otimes v_2,\quad
u_2\otimes v_1,\quad
u_2\otimes v_2.
\tag{3}
\]
Then
\[
\boxed{
K=
\begin{pmatrix}
1&0&0&-\frac12\\
0&\frac12&0&0\\
0&0&\frac12&0\\
-\frac12&0&0&\frac34
\end{pmatrix}.}
\tag{4}
\]

### Direct verification of (4)

Write \(F_1,F_2\) for the swaps of the first and second physical
coordinates between the two replicas.  Then
\[
R_2=I-\frac12(F_1+F_2)+\frac14F_1F_2.
\tag{5}
\]
For a product \(x\otimes y\),
\[
\langle x\otimes y|F_i|x\otimes y\rangle
=\operatorname{Tr}(\rho_x^{(i)}\rho_y^{(i)}),
\qquad
\langle x\otimes y|F_1F_2|x\otimes y\rangle
=|\langle x,y\rangle|^2.
\tag{6}
\]
The one-site reductions of \(s\) are both \(I_2/2\).  Formula (6)
therefore gives the diagonal of (4):
\[
1,\quad\frac12,\quad\frac12,\quad\frac34.
\]
For the upper-right entry, the identity and full-swap terms vanish, while
direct expansion of \(s\otimes s\) gives
\[
\langle 00\otimes11|F_1|s\otimes s\rangle
=\langle 00\otimes11|F_2|s\otimes s\rangle
=\frac12.
\]
Thus that entry is \(-\frac12\).  Every other off-diagonal entry vanishes
by the computational-basis expansion.  This proves (4) without numerical
approximation.

The trace and eigenvalues are
\[
\operatorname{Tr}K=\frac{11}{4},
\qquad
\operatorname{spec}(K)
=\left\{
\frac12,\frac12,\frac{7-\sqrt{17}}8,\frac{7+\sqrt{17}}8
\right\}.
\tag{7}
\]
Indeed, only the corner \(2\times2\) block needs to be diagonalized; it
has trace \(7/4\) and determinant \(1/2\).  Consequently
\[
2\|K\|_{\rm op}
=\frac{7+\sqrt{17}}4
>\frac{11}{4}
=\operatorname{Tr}K,
\tag{8}
\]
because \(\sqrt{17}>4\).  This exactly disproves (1).

Nothing in the calculation uses the absence of further local basis
states.  Embedding \(\operatorname{span}\{|0\rangle,|1\rangle\}\) into
\(\mathbb C^d\) gives the same compression for every \(d\geq2\), in
particular for every dimension relevant to the Werner problem.

## 2. Why the failed bound is stronger than necessary

Fix arbitrary orthonormal frames \(u_1,u_2\) of \(U\) and \(v_1,v_2\)
of \(V\), and continue to write \(K\) for the compression of \(R_n\).
For the equal-singular-value coefficient matrix
\[
C=|u_1\rangle\langle v_1|+|u_2\rangle\langle v_2|,
\tag{9}
\]
the crossed matrix-element identity gives
\[
\begin{aligned}
Q_n(C)
={}&\langle u_1\otimes v_1|R_n|u_1\otimes v_1\rangle\\
&+\langle u_2\otimes v_2|R_n|u_2\otimes v_2\rangle\\
&+2\operatorname{Re}
\langle u_1\otimes v_2|R_n|u_2\otimes v_1\rangle.
\end{aligned}
\tag{10}
\]
Define the normalized code-maximally-entangled vector
\[
|\eta\rangle
=\frac{u_1\otimes v_2-u_2\otimes v_1}{\sqrt2}.
\tag{11}
\]
Expansion in the basis (3) gives the exact identity
\[
\boxed{\quad
Q_n(C)=\operatorname{Tr}K-2\langle\eta|K|\eta\rangle.
\quad}
\tag{12}
\]
Thus (1) controls every unit vector of \(U\otimes V\), although (12)
only asks for control of a maximally entangled vector.

Let
\[
\omega_{\rm ME}(K)
=\max\left\{
\langle\eta|K|\eta\rangle:
\|\eta\|=1,
\eta\text{ has Schmidt coefficients }2^{-1/2},2^{-1/2}
\text{ across }U:V
\right\}.
\tag{13}
\]
Every vector in (13) can be put in the form (11): take its equal-weight
Schmidt decomposition
\[
\eta=\frac{x_1\otimes y_1+x_2\otimes y_2}{\sqrt2}
\]
and set \(u_i=x_i,\ v_2=y_1,\ v_1=-y_2\).  Conversely, (11) is plainly
maximally entangled.  It follows from (12) that
\[
\boxed{\quad
2\omega_{\rm ME}(K)\leq\operatorname{Tr}K
\quad}
\tag{14}
\]
for every pair \(U,V\) is exactly the compression inequality needed for
nonnegativity on all rank-two matrices with equal nonzero singular values.
In particular, (14), at every copy number, is sufficient for the
all-copy endpoint theorem by the copy-doubling reduction.

An equivalent framewise form, useful when one particular partial
isometry is fixed, is
\[
2\left|
\langle u_1\otimes v_2|R_n|u_2\otimes v_1\rangle
\right|
\leq
\langle u_1\otimes v_1|R_n|u_1\otimes v_1\rangle
+
\langle u_2\otimes v_2|R_n|u_2\otimes v_2\rangle.
\tag{15}
\]
The absolute value accounts for the arbitrary relative phase in the
choice of the second frame vector.  Requiring (15) for all frames is
equivalent to (14).

## 3. A three-by-three exact formulation of the weaker criterion

The maximization in (13) has a closed finite-dimensional expression.
Choose identifications \(U,V\simeq\mathbb C^2\), and let
\(\sigma_1,\sigma_2,\sigma_3\) be the Pauli matrices.  Define the real
\(3\times3\) correlation matrix
\[
M_{ij}=\operatorname{Tr}\!\left(
K(\sigma_i\otimes\sigma_j)\right).
\tag{16}
\]
Let \(s_1(M)\geq s_2(M)\geq s_3(M)\geq0\) be its singular values, and put
\[
g(M)=s_1(M)+s_2(M)-\operatorname{sgn}(\det M)s_3(M).
\tag{17}
\]
When \(\det M=0\), the last singular value is zero, so the convention for
\(\operatorname{sgn}(0)\) is immaterial.

Then
\[
\boxed{\quad
\omega_{\rm ME}(K)=\frac{\operatorname{Tr}K+g(M)}4.
\quad}
\tag{18}
\]
Consequently, the exact weaker target (14) is
\[
\boxed{\quad
g(M)\leq\operatorname{Tr}K.
\quad}
\tag{19}
\]

### Proof of (18)

Expand \(K\) in the orthogonal Pauli basis:
\[
K=\frac14\sum_{\mu,\nu=0}^3
\operatorname{Tr}\!\left(K(\sigma_\mu\otimes\sigma_\nu)\right)
\sigma_\mu\otimes\sigma_\nu,
\qquad \sigma_0=I_2.
\tag{20}
\]
Both one-party reductions of a maximally entangled unit vector equal
\(I_2/2\), so all terms in (20) having exactly one nonidentity Pauli
matrix have zero expectation.

For the vector \((|00\rangle+|11\rangle)/\sqrt2\), the \(3\times3\)
matrix of Pauli correlations is
\(\operatorname{diag}(1,-1,1)\), which is orthogonal with determinant
\(-1\).  Changing either local orthonormal basis acts on the Pauli
matrices by a real rotation.  Hence the correlation matrices of all
maximally entangled vectors are exactly
\[
\{O\in O(3):\det O=-1\}.
\tag{21}
\]
It follows that
\[
\omega_{\rm ME}(K)
=\frac14\left(
\operatorname{Tr}K+
\max_{\substack{O\in O(3)\\\det O=-1}}
\operatorname{Tr}(M^{\mathsf T}O)
\right).
\tag{22}
\]

For completeness, take a real singular-value decomposition
\(M=A\operatorname{diag}(s_1,s_2,s_3)B^{\mathsf T}\).  Setting
\(Q=A^{\mathsf T}OB\), the determinant constraint on \(Q\) is positive
when \(\det M<0\) and negative when \(\det M>0\).  The maximum of
\(\sum_i s_iQ_{ii}\) is therefore respectively
\[
s_1+s_2+s_3
\quad\text{or}\quad
s_1+s_2-s_3.
\]
Here is an elementary verification of the only nonimmediate case.  If
\(\det Q=-1\), then \(Q\) has eigenvalues
\(-1,e^{i\theta},e^{-i\theta}\) for some \(\theta\), with the degenerate
real cases included.  Hence \(\operatorname{Tr}Q\leq1\).  Since
\(Q_{ii}\leq1\) and \(s_i\geq s_3\),
\[
\begin{aligned}
\sum_i s_iQ_{ii}
&=\sum_i s_i-\sum_i s_i(1-Q_{ii})\\
&\leq \sum_i s_i-s_3(3-\operatorname{Tr}Q)
\leq s_1+s_2-s_3.
\end{aligned}
\]
Equality is attained by \(\operatorname{diag}(1,1,-1)\).  Under the
positive determinant constraint, the bound \(\sum_i s_iQ_{ii}\leq
\sum_i s_i\) follows directly from \(Q_{ii}\leq1\) and is attained by
the identity.
If \(M\) is singular, the sign can be changed in a zero singular
direction.  This proves that the maximum in (22) is (17), and hence
proves (18).

## 4. The counterexample saturates the correct inequality

For the rational compression (4), direct Pauli contraction gives
\[
M=\operatorname{diag}\left(-1,1,\frac34\right).
\tag{23}
\]
Thus
\[
g(M)=1+1+\frac34=\frac{11}{4}=\operatorname{Tr}K.
\tag{24}
\]
Equations (18) and (24) give
\[
\omega_{\rm ME}(K)=\frac{11}{8}
=\frac12\operatorname{Tr}K,
\tag{25}
\]
whereas
\[
\|K\|_{\rm op}=\frac{7+\sqrt{17}}8>\frac{11}{8}.
\]
For example, the maximally entangled code vector
\[
\frac{u_1\otimes v_1-u_2\otimes v_2}{\sqrt2}
\]
has expectation \(11/8\), so (25) is attained.

This explains the obstruction exactly.  The top eigenvector of \(K\)
lies in the span of \(u_1\otimes v_1,u_2\otimes v_2\), but its two code
Schmidt coefficients are unequal.  It is irrelevant to (12).  Replacing
the operator norm by the maximally-entangled numerical radius discards
precisely this spurious direction.

## 5. Resolution supplied by this note

The operator-norm/trace compression route in (1) cannot prove the Werner
endpoint theorem: it is false already at \(n=2\), even on locally
two-dimensional support.

The surviving exact compression problem is (14), equivalently (19).
No proof of (14) for all Werner compressions is given here; such a proof
would, together with the equal-singular-value reduction, settle the
all-copy endpoint problem.  The gain is that (19) depends only on the
\(3\times3\) code-correlation matrix and ignores the local Pauli
coefficients which can enlarge the full operator norm but never
contribute to a maximally entangled code vector.
