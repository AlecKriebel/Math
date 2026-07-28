# Exact subclasses, boundary vectors, and dimension embedding

## 1. Dimension embedding for witnesses

Let \(V:\mathbb C^3\hookrightarrow\mathbb C^d\) be a coordinate isometry
and use the same subspace on the two sides of one copy.  With
\(|\Phi_d\rangle=\sum_{j=0}^{d-1}|jj\rangle\),
\[
X_{-1/2,d}=I-\tfrac12|\Phi_d\rangle\langle\Phi_d|.
\]
Compression by \(V\otimes\overline V\) gives
\[
(V^\dagger\otimes V^T)X_{-1/2,d}(V\otimes\overline V)
=I-\tfrac12|\Phi_3\rangle\langle\Phi_3|
=X_{-1/2,3}.
\tag{1}
\]
Tensoring the isometry proves: any exact endpoint witness in \(d=3\)
embeds, with the same Schmidt rank and expectation, in every \(d\ge3\).

## 2. A large exact zero family

Let \(p,q\in[d]^n\), and let \(m\) be their Hamming distance.  Define
\[
C=|p\rangle\langle p|+|q\rangle\langle q|.
\tag{2}
\]
If \(p\ne q\), this matrix has rank two.  On site \(i\), the two local
rank-one projectors have the \(2\times2\) Gram matrix, for the one-copy
endpoint form,
\[
H_i=\frac12
\begin{pmatrix}
1&\varepsilon_i\\
\varepsilon_i&1
\end{pmatrix},
\qquad
\varepsilon_i=
\begin{cases}
+1,&p_i=q_i,\\
-1,&p_i\ne q_i.
\end{cases}
\tag{3}
\]
Indeed, a diagonal entry is
\(1-\tfrac12=\tfrac12\); an off-diagonal entry is \(\tfrac12\) for equal
projectors and \(-\tfrac12\) for orthogonal projectors.

The copywise-product Gram formula then gives
\[
\begin{aligned}
Q_{d,n}(C)
&=\sum_{r,s=1}^2\prod_{i=1}^nH_i(r,s)\\
&=2^{1-n}\left(1+\prod_i\varepsilon_i\right)
=2^{1-n}\bigl(1+(-1)^m\bigr).
\end{aligned}
\tag{4}
\]
Thus every odd-distance pair gives an exact nonzero zero vector.  The
boundary exists in every copy number and is not confined to adjacent
computational strings.

## 3. Two-copy positivity for normal rank-two matrices

**Theorem.** If \(C\) is normal and \(\operatorname{rank}C\le2\), then
\[
Q_{d,2}(C)\ge0
\]
for every \(d\ge2\).

**Proof.** A normal rank-two matrix has a spectral decomposition
\[
C=\lambda_1|\phi_1\rangle\langle\phi_1|
 +\lambda_2|\phi_2\rangle\langle\phi_2|,
\qquad \langle\phi_1,\phi_2\rangle=0,
\tag{5}
\]
where the vectors live on the two-copy physical space
\(\mathbb C^d\otimes\mathbb C^d\).

For \(i,j\in\{1,2\}\), let
\[
k_{ij}
=\operatorname{Tr}(\rho_i^{(1)}\rho_j^{(1)})
 +\operatorname{Tr}(\rho_i^{(2)}\rho_j^{(2)}),
\tag{6}
\]
where \(\rho_i^{(a)}\) is the reduced density matrix of \(\phi_i\) on
copy factor \(a\).

For arbitrary unit vectors \(x,y\) on a bipartite space, let \(F_1,F_2\)
swap the corresponding factors between two replicas.  Since the commuting
operators \(I-F_1\) and \(I-F_2\) are positive,
\[
\begin{aligned}
0
&\le
\langle x\otimes y|(I-F_1)(I-F_2)|x\otimes y\rangle\\
&=
1-\operatorname{Tr}(\rho_x^{(1)}\rho_y^{(1)})
 -\operatorname{Tr}(\rho_x^{(2)}\rho_y^{(2)})
 +|\langle x,y\rangle|^2.
\end{aligned}
\tag{7}
\]
Consequently,
\[
0\le k_{12}\le1,\qquad 0\le k_{11},k_{22}\le2.
\tag{8}
\]

Expanding \(Q_{d,2}(C)\) in the two spectral summands gives
\[
Q_{d,2}(C)
=
\begin{pmatrix}\overline{\lambda_1}&\overline{\lambda_2}\end{pmatrix}
G
\begin{pmatrix}\lambda_1\\\lambda_2\end{pmatrix},
\tag{9}
\]
where
\[
G_{ii}=\frac54-\frac12k_{ii},
\qquad
G_{12}=\frac14-\frac12k_{12}.
\tag{10}
\]
Here the empty contraction contributes \(\delta_{ij}\), the two
one-factor contractions contribute \(-k_{ij}/2\), and the full trace
contributes \(1/4\).

Equation (8) implies
\[
G_{11},G_{22}\ge\frac14,\qquad |G_{12}|\le\frac14.
\]
Thus
\[
\det G\ge\frac1{16}-\frac1{16}=0,
\]
and \(G\succeq0\). \(\square\)

The unresolved two-copy portion is therefore confined to genuinely
nonnormal rank-two coefficient matrices.

## 4. Auxiliary-qubit sign localization

Let
\[
C=\sum_{r=0}^1|u_r\rangle\langle v_r|,
\]
introduce \(K\cong\mathbb C^2\), and set
\[
|U\rangle=\sum_r|r\rangle_K|u_r\rangle,\qquad
|V\rangle=\sum_r|r\rangle_K|v_r\rangle.
\]
Then \(C=\operatorname{Tr}_K|U\rangle\langle V|\).  Applying the replica
formula also to the auxiliary contraction gives
\[
Q_{d,n}(C)
=\langle U\otimes V|
F_K\otimes R_n
|U\otimes V\rangle,
\qquad
R_n=(I-\tfrac12F)^{\otimes n}>0.
\tag{11}
\]
Writing \(F_K=\Pi_+^K-\Pi_-^K\),
\[
Q_{d,n}(C)
=
\|(\Pi_+^K\otimes R_n^{1/2})(U\otimes V)\|^2
-
\|(\Pi_-^K\otimes R_n^{1/2})(U\otimes V)\|^2.
\tag{12}
\]
The negative auxiliary subspace has dimension one because
\(\dim K=2\).  This precisely localizes the rank-two obstruction, but
(12) by itself does not compare the two norms and therefore is not an
all-copy proof.
