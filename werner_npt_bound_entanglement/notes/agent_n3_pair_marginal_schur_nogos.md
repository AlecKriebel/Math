# Two exact no-go certificates for the one-plane marginal defect

## Status

This note does **not** prove or disprove the one-plane inequality
\[
 {\cal D}_V:=3(2I-{\cal S}_V)\succeq0.
 \tag{1}
\]
It excludes two direct Schur/Gram mechanisms:

1. the canonical decomposition of \({\cal D}_V\) into three
   two-site marginal defects is not termwise positive, even on the
   standard equality code;
2. no scalar invariant multiplier of the isometry relation can make
   the two-replica Gram operator positive semidefinite.

Both obstructions are exact.  They show that a successful marginal
proof must couple all three physical sites and must use more than the
single scalar consequence of \(V^\dagger V=I_2\).

The dependency-free checker is
`verification/verify_n3_pair_marginal_schur_nogos.py`.

## 1. Notation

Let
\[
 |\boldsymbol V\rangle
 =v_0\otimes|0\rangle_K+v_1\otimes|1\rangle_K,\qquad
 R=|\boldsymbol V\rangle\langle\boldsymbol V|,
 \tag{2}
\]
where \(v_0,v_1\) are orthonormal qutrit triples.  On physical site
\(i\), put
\[
 e_i(X)=I_i\otimes\operatorname{Tr}_iX.
 \tag{3}
\]
The marginal form of the defect is
\[
 {\cal D}_V
 =
 6I+2\sum_i e_i(R)-3\sum_{i<j}e_ie_j(R)-R.
 \tag{4}
\]

## 2. The natural pairwise Schur allocation is indefinite

There is the exact algebraic splitting
\[
 {\cal D}_V=\sum_{i<j}{\cal D}_{ij},
 \qquad
 {\cal D}_{ij}
 =
 2I+e_i(R)+e_j(R)-3e_ie_j(R)-\frac13R.
 \tag{5}
\]
It is tempting to prove the three summands positive separately and
then add them.  This fails sharply.

Take
\[
 v_0=|110\rangle,\qquad v_1=|111\rangle,
 \tag{6}
\]
and use the unnormalized vector
\[
 |\Phi\rangle_{3K}=|0,0\rangle+|1,1\rangle .
 \tag{7}
\]
Then
\[
 R=P_1^{(1)}\otimes P_1^{(2)}
   \otimes|\Phi\rangle\langle\Phi|_{3K}.
 \tag{8}
\]

For the pair \(12\), choose the unit vector
\[
 x_{12}=|00\rangle_{12}\otimes
          \frac{|\Phi\rangle_{3K}}{\sqrt2}.
 \tag{9}
\]
The two positive marginal terms and \(R\) annihilate \(x_{12}\),
while \(e_1e_2(R)\) has eigenvalue \(2\) on it.  Therefore
\[
 \boxed{\quad
 \langle x_{12},{\cal D}_{12}x_{12}\rangle=2-3(2)=-4.
 \quad}
 \tag{10}
\]

For the other two pairs, use computational basis vectors
\[
 x_{13}=|0,1,2,0\rangle_{123K},\qquad
 x_{23}=|1,0,2,0\rangle_{123K}.
 \tag{11}
\]
In each case only the identity and the corresponding twice-traced
marginal survive, with eigenvalues \(2\) and \(-3\).  Hence
\[
 \boxed{\quad
 \langle x_{13},{\cal D}_{13}x_{13}\rangle
 =
 \langle x_{23},{\cal D}_{23}x_{23}\rangle=-1.
 \quad}
 \tag{12}
\]

The full defect for (6) is nevertheless positive semidefinite and
has a nontrivial kernel, as follows from the established
local-support theorem.  Thus positive compensation among all three
terms in (5) is essential even at equality.

## 3. The scalar invariant Gram multiplier cannot work

Let \(F_i\) swap physical site \(i\) between two replicas, and let
\(F_K\) swap the logical qubits.  The exact two-replica identity is
\[
 \langle x,{\cal D}_Vx\rangle
 =
 \langle x\otimes\boldsymbol V|
 F_KH
 |x\otimes\boldsymbol V\rangle ,
 \tag{13}
\]
where
\[
 H=6I-3\sum_iF_i+2\sum_{i<j}F_iF_j-F_1F_2F_3.
 \tag{14}
\]
On the physical sector with \(r\) antisymmetric local swaps,
\[
 h_r=(2,2,6,22),\qquad r=0,1,2,3.
 \tag{15}
\]

The isometry relation supplies the scalar vanishing identity
\[
 \left\langle x\otimes\boldsymbol V\left|
 F_K-\frac12I
 \right|x\otimes\boldsymbol V\right\rangle=0.
 \tag{16}
\]
Indeed,
\[
 \langle F_K\rangle
 =\operatorname{Tr}(\rho_K^x\rho_K^V)
 =\operatorname{Tr}\rho_K^x=\|x\|^2,
 \quad
 \langle I\rangle
 =\|x\|^2\|\boldsymbol V\|^2=2\|x\|^2.
 \]

Consequently the complete scalar invariant one-multiplier family is
\[
 G_t=F_KH+t\left(F_K-\frac12I\right),
 \qquad t\in\mathbb R.
 \tag{17}
\]
Its eigenvalue on logical-swap sign
\(\varepsilon\in\{+1,-1\}\) and physical sector \(r\) is
\[
 \lambda_{\varepsilon,r}
 =
 \varepsilon h_r+t\left(\varepsilon-\frac12\right).
 \tag{18}
\]
Positivity on the \((\varepsilon,r)=(+1,0)\) sector requires
\[
 2+\frac t2\ge0,\qquad\text{hence}\qquad t\ge-4.
 \tag{19}
\]
Positivity on the \((\varepsilon,r)=(-1,3)\) sector requires
\[
 -22-\frac{3t}{2}\ge0,\qquad\text{hence}\qquad
 t\le-\frac{44}{3}.
 \tag{20}
\]
The intervals are disjoint.  Therefore
\[
 \boxed{\quad
 G_t\not\succeq0\quad\text{for every real }t.
 \quad}
 \tag{21}
\]

After averaging under the simultaneous local unitary symmetries, a
quadratic logical multiplier of \(V^\dagger V-I_2\) reduces to (16):
the only covariant quadratic matrix built from \(x\) is a linear
combination of \(\rho_K^x\) and
\((\operatorname{Tr}\rho_K^x)I_K\), and the trace part gives no
independent homogeneous relation.  Thus (21) excludes the scalar
invariant degree-\((2,2)\) Hermitian Gram completion.  It does not
exclude a state-dependent, higher-degree, or non-Gram
Pluecker/Koszul certificate.

## 4. Exact conclusion

What is proved:

1. the decomposition (5);
2. exact negative expectations \(-4,-1,-1\) for its three natural
   summands on one physical equality code;
3. the exact scalar isometry relation (16);
4. infeasibility of the entire Gram family (17).

What remains open:

1. the full coupled operator inequality (1);
2. a global Schur complement using matrix-valued or higher-degree
   isometry information;
3. an exact physical counterexample.
