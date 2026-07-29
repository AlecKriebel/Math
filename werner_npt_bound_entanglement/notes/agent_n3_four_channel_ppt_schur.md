# Three-copy four-channel Gram reduction

## Status

This note does **not** prove unrestricted three-copy positivity.  It
compresses the non-Hermitian remainder to one explicit reversed Schur
complement.  The reduction is exact over the complex numbers and in
arbitrary local dimensions.

The main point is that the four logical Fierz channels do not merely
satisfy an inequality.  Their signed sum is exactly twice the partial
transpose of one positive Gram operator.  Consequently the unresolved
geometry is:

\[
 \begin{pmatrix}A&B\\ B^\dagger&D\end{pmatrix}\succeq0
 \quad\Longrightarrow\quad
 \begin{pmatrix}A&B^\dagger\\ B&D\end{pmatrix}\stackrel{?}{\succeq}0
                                                               \tag{1}
\]

for the special blocks produced by the three-fold Fierz channel.  The
first matrix is positive for free.  The second one is the complete
three-copy problem.

The exact checker is
`verification/verify_n3_four_channel_ppt_schur.py`.

## 1. Weighted physical Fierz frame

Fix real computational bases on
\[
 {\cal H}=H_1\otimes H_2\otimes H_3.
\]
For each \(H_i\), choose real Hilbert--Schmidt orthonormal bases
\(\mathscr S_i,\mathscr A_i\) of symmetric and skew-symmetric matrices.
Use the locally weighted frame
\[
 \widehat{\mathscr R}_i
 =
 \{S/\sqrt2:S\in\mathscr S_i\}
 \mathbin{\mathop{\cup}}
 \{\sqrt{3/2}\,A:A\in\mathscr A_i\},                       \tag{2}
\]
and let \(\mathscr R\) be its three-fold tensor-product frame.

The corresponding completely positive map is
\[
 \begin{aligned}
 \widetilde\Phi_i(X)
 &=\sum_{R_i\in\widehat{\mathscr R}_i}R_i^\dagger X R_i\\
 &=\operatorname{Tr}(X)I-\frac12X^{\mathsf T}.             \tag{3}
 \end{aligned}
\]
Indeed,
\[
 \sum_{S\in\mathscr S_i}SXS^\dagger
 =\frac12(\operatorname{Tr}(X)I+X^{\mathsf T}),\qquad
 \sum_{A\in\mathscr A_i}A^\dagger XA
 =\frac12(\operatorname{Tr}(X)I-X^{\mathsf T}),            \tag{4}
\]
and (3) follows from the weights in (2).  Put
\[
 \widetilde\Phi
 =\widetilde\Phi_1\otimes\widetilde\Phi_2
  \otimes\widetilde\Phi_3.                                 \tag{5}
\]

Let \(K=\mathbb C^2\), and write an anchor and a test matrix as
\[
 U=(u_0,u_1),\qquad V=(v_0,v_1):
 K\longrightarrow{\cal H}.                                \tag{6}
\]
The coefficient matrix
\[
 C=UV^\dagger=\sum_{a=0}^1|u_a\rangle\langle v_a|          \tag{7}
\]
has rank at most two.  Conversely, every rank-at-most-two matrix has
such a factorization.

There is no loss in assuming
\[
 U^\dagger U=I_2.                                         \tag{8}
\]
If \(U\) has two independent columns, an invertible filter on \(K\)
orthonormalizes them.  Since all physical maps act as the identity on
\(K\), the anchored output changes by an invertible congruence on
\(K\), which preserves positivity.  If \(U\) has dependent columns,
\(C\) has rank at most one and the established strict rank-one theorem
applies.  Equivalently, the dependent case follows by continuity from
the full-rank case.

## 2. One positive Gram operator

Identify an \({\cal H}\)-by-\(2\) matrix with a vector in
\({\cal H}\otimes K\), column by column.  Define
\[
 \boxed{\qquad
 G_U
 =
 \sum_{R\in\mathscr R}
 |R^\dagger\overline U\rangle\!\rangle
 \langle\!\langle R^\dagger\overline U|.
 \qquad}                                                   \tag{9}
\]
It is positive by construction.  If
\[
 |\overline{\mathcal U}\rangle
 =\sum_{a=0}^1|\overline u_a\rangle\otimes|a\rangle,
                                                               \tag{10}
\]
then (3) gives the intrinsic formula
\[
 G_U
 =
 (\widetilde\Phi\otimes\operatorname{id}_K)
 (|\overline{\mathcal U}\rangle
   \langle\overline{\mathcal U}|).                         \tag{11}
\]

Introduce the four real logical matrices
\[
 \tau_0=I,\qquad
 \tau_1=X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 \tau_2=Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad
 \tau_3=\epsilon=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
                                                               \tag{12}
\]
For an \({\cal H}\)-by-\(2\) matrix \(W\), let
\[
 {\mathsf S}_\tau W=W\tau^\dagger,\qquad
 \Gamma_\tau={\mathsf S}_\tau^\dagger G_U{\mathsf S}_\tau.
                                                               \tag{13}
\]
Thus
\[
 \langle V,\Gamma_\tau V\rangle
 =
 \sum_{R\in\mathscr R}
 \left|\operatorname{Tr}
  (\tau^\dagger U^{\mathsf T}RV)\right|^2.                 \tag{14}
\]

### Theorem 2.1 (exact four-channel collapse)

With partial transpose on the logical factor \(K\),
\[
 \boxed{\qquad
 \Gamma_I+\Gamma_X+\Gamma_Z-\Gamma_\epsilon
 =2G_U^{\Gamma_K}.
 \qquad}                                                   \tag{15}
\]
Consequently
\[
 \boxed{\qquad
 Q_3(UV^\dagger)
 =\langle V,G_U^{\Gamma_K}V\rangle.
 \qquad}                                                   \tag{16}
\]
In particular, unrestricted three-copy positivity is equivalent to
\[
 G_U^{\Gamma_K}\succeq0
 \quad\hbox{for every isometry }U:K\longrightarrow{\cal H}.
                                                               \tag{17}
\]

#### Proof

Write \(G_U\), as a \(2\)-by-\(2\) logical block matrix, in the form
\[
 G_U=\begin{pmatrix}A&B\\B^\dagger&D\end{pmatrix}.         \tag{18}
\]
Direct conjugation by the four matrices in (12) gives
\[
 \begin{aligned}
 &G_U+XG_UX+ZG_UZ-\epsilon^\dagger G_U\epsilon\\
 &\hspace{25mm}
 =2\begin{pmatrix}A&B^\dagger\\B&D\end{pmatrix}
 =2G_U^{\Gamma_K}.                                        \tag{19}
 \end{aligned}
\]
Under column vectorization, the four conjugations in (19) are exactly
the operators \(\Gamma_\tau\) in (13), proving (15).

For \(M_R=U^{\mathsf T}RV\), the normalized orthogonal basis
\[
 I/\sqrt2,\quad X/\sqrt2,\quad Z/\sqrt2,\quad
 \epsilon/\sqrt2
\]
splits \(M_R\) into its transpose-symmetric and transpose-skew parts.
The exact Fierz identity therefore reads
\[
 2Q_3(UV^\dagger)
 =
 \sum_R\left(
 |\operatorname{Tr}M_R|^2
 +|\operatorname{Tr}(XM_R)|^2
 +|\operatorname{Tr}(ZM_R)|^2
 -|\operatorname{Tr}(\epsilon^\dagger M_R)|^2
 \right).                                                  \tag{20}
\]
Equations (14)--(15) turn (20) into (16).  Since \(V\) is arbitrary,
(16) proves (17).
\(\square\)

There is a useful consistency check with the original endpoint map
\[
 \Phi_i(X)=\operatorname{Tr}(X)I-\frac12X.                 \tag{21}
\]
Because \(\widetilde\Phi_i=\Phi_i\circ{\mathsf T}_i\), total
transposition in \({\cal H}\otimes K\) gives
\[
 \boxed{\qquad
 G_U^{\Gamma_K}
 =
 (\Phi_1\otimes\Phi_2\otimes\Phi_3\otimes
  \operatorname{id}_K)
 (|\mathcal U\rangle\langle\mathcal U|),
 \qquad
 |\mathcal U\rangle=\sum_a|u_a\rangle|a\rangle.
 \qquad}                                                   \tag{22}
\]
Thus (15) is a Gram realization of the two-dimensional-code
formulation, not a relaxation of it.

## 3. The exact reversed Schur complement

The blocks in (18) are explicitly
\[
 \begin{aligned}
 A&=\widetilde\Phi(|\overline u_0\rangle
                    \langle\overline u_0|),\\
 B&=\widetilde\Phi(|\overline u_0\rangle
                    \langle\overline u_1|),\\
 D&=\widetilde\Phi(|\overline u_1\rangle
                    \langle\overline u_1|).
 \end{aligned}                                             \tag{23}
\]
The established rank-one lower bound implies, for the normalization
(8),
\[
 A\succeq\frac18I,\qquad D\succeq\frac18I,                \tag{24}
\]
so both diagonal blocks are invertible.

Since \(G_U\succeq0\), its ordinary Schur complement gives
\[
 D-B^\dagger A^{-1}B\succeq0,
 \qquad\hbox{equivalently}\qquad
 \|A^{-1/2}BD^{-1/2}\|\leq1.                              \tag{25}
\]
The desired partial-transpose positivity is instead exactly
\[
 \boxed{\qquad
 D-BA^{-1}B^\dagger\succeq0,
 \qquad\hbox{equivalently}\qquad
 \|A^{-1/2}B^\dagger D^{-1/2}\|\leq1.
 \qquad}                                                   \tag{26}
\]
Thus the entire remaining non-Hermitian geometry is the reversal
\[
 B^\dagger A^{-1}B
 \quad\longleftrightarrow\quad
 BA^{-1}B^\dagger.                                        \tag{27}
\]
Equation (26), with the three explicit blocks (23), is a single
operator inequality.  It is strictly smaller than separately
controlling the four logical Fierz channels, because their complete
signed interaction has already been eliminated by (15).

There is no pointwise Schur certificate at the level of a single
physical frame element.  A summand of (9) is
\[
 |W_R\rangle\!\rangle\langle\!\langle W_R|,
 \qquad W_R=R^\dagger\overline U.                          \tag{28}
\]
Whenever \(W_R\) has matrix rank two, the partial transpose of this
rank-one projector has a negative eigenvalue
\(-s_1(W_R)s_2(W_R)\).  One may choose the symmetric local frames so
that an invertible tensor-product element occurs, in which case (8)
ensures such a rank-two summand.  Therefore positivity, if true, must
come from a recoupling between different \(R\)'s.

## 4. Compatibility with the established normal theorem

For completeness, the Gram reduction is consistent with the normal
theorem already proved independently in
`agent_unrestricted_n3_selfadjoint.md`.  Its shortest deduction from
the established self-adjoint result is as follows.

### Proposition 4.1

If \(C\) is normal and \(\operatorname{rank}C\leq2\), then
\[
 Q_3(C)\geq0.                                              \tag{29}
\]

#### Proof

Write the spectral decomposition
\[
 C=\lambda_1P_1+\lambda_2P_2,                             \tag{30}
\]
where \(P_1,P_2\) are orthogonal rank-one projections.  Put
\[
 h_{ab}=\langle P_a,L^{\otimes3}(P_b)\rangle_{\rm HS}.     \tag{31}
\]
Because \(L^{\otimes3}\) is self-adjoint and preserves adjoints, the
matrix \(h=(h_{ab})\) is real symmetric.  If
\(r_a=|\lambda_a|\), then
\[
 Q_3(C)
 =h_{11}r_1^2+h_{22}r_2^2
 2h_{12}\operatorname{Re}(\overline\lambda_1\lambda_2).
                                                               \tag{32}
\]
For fixed \(r_1,r_2\), the minimum over the relative phase occurs at
\(\operatorname{Re}(\overline\lambda_1\lambda_2)
=\pm r_1r_2\).  The two endpoints in (32) are respectively
\[
 Q_3(r_1P_1+r_2P_2),\qquad
 Q_3(r_1P_1-r_2P_2),                                     \tag{33}
\]
and both matrices in (33) are self-adjoint of rank at most two.
Their nonnegativity proves (29).
\(\square\)

Hence a three-copy counterexample, if one exists, is necessarily
genuinely nonnormal.  In the Gram formulation it must violate the
reversed contraction (26), despite satisfying the ordinary contraction
(25).

## 4.2 The reversed-Schur problem is an interior six-determinant problem

The unrestricted qutrit two-copy theorem removes the whole
local-support boundary of (26).  Let
\[
 {\cal U}=\operatorname{ran}C,\qquad
 {\cal V}=\operatorname{ran}C^\dagger
\]
be the left and right singular planes of a rank-two matrix, and let
\[
 \rho_i^{\cal U}=\operatorname{Tr}_{\bar i}P_{\cal U},
 \qquad
 \rho_i^{\cal V}=\operatorname{Tr}_{\bar i}P_{\cal V}.
\tag{33a}
\]
Then
\[
 \boxed{\qquad
 Q_3(C)<0
 \quad\Longrightarrow\quad
 \det\rho_i^{\cal U}>0,\quad
 \det\rho_i^{\cal V}>0
 \quad(i=1,2,3).
 \qquad}
\tag{33b}
\]

Here is the exact mechanism.  If, for example,
\(\operatorname{rank}\rho_1^{\cal U}\leq2\), the first physical
row-support of \(C\) lies in a subspace \(W\subseteq\mathbb C^3\) of
dimension at most two.  Compressing the first endpoint factor to that
row-support gives
\[
 Z_W=(P_W\otimes I)X_3(P_W\otimes I).
\tag{33c}
\]
This operator is separable across the first row/column pair.  For
\(\dim W=2\), an explicit decomposition is
\[
\begin{aligned}
 I_4-\frac12|\Phi_2\rangle\langle\Phi_2|
 =\frac12\sum_{s=\pm1}\bigl(
 &P_{x,s}\otimes P_{x,-s}
 +P_{y,s}\otimes P_{y,s}\\
 &+P_{z,s}\otimes P_{z,-s}\bigr),
\end{aligned}
\tag{33d}
\]
plus the manifest product term on the unused column direction.  The
remaining operator \(X_3^{\otimes2}\) is two-block-positive by the
unrestricted qutrit two-copy theorem.  A separable positive factor
tensor a two-block-positive factor remains two-block-positive: after
local square-root filtering, conditioning on a product basis of the
separable factor leaves Schmidt-rank-at-most-two vectors for the second
factor.  Hence \(Q_3(C)\geq0\).

If instead a right singular plane has deficient local support, apply
the same argument to \(C^\dagger\), using \(Q_3(C^\dagger)=Q_3(C)\).
Since a positive qutrit reduction has rank at most two exactly when its
determinant vanishes, (33b) follows.

Thus the reversed Schur complement (26) only remains to be controlled
for isometric anchors with all three local reductions positive definite,
and a negative test vector would necessarily have a right singular
plane with the same property.  The complete proof of the tensoring
lemma and the compressed-factor decomposition is recorded in
`agent_n3_local_support_boundary.md`.

## 5. Exact obstruction to a local-determinant spectral gap

For qutrit local spaces, a natural attempted strengthening of (17) is
\[
 M_Q(P_{\mathcal U})
 \stackrel{?}{\succeq}
 \frac32\left(\sum_{i=1}^3\det\rho_i\right)I,             \tag{34}
\]
where
\[
 \rho_i=\operatorname{Tr}_{K\bar i}
 |\mathcal U\rangle\langle\mathcal U|,
 \qquad \operatorname{Tr}\rho_i=2.                        \tag{35}
\]
This would extend positivity from the local-qubit boundary, since all
three determinants vanish there.  In fact every constant strictly
larger than \(1\) in place of \(3/2\) is false.

For \(t>0\), take
\[
 \begin{aligned}
 u_0(t)&=\frac{|111\rangle+t|222\rangle}{\sqrt{1+t^2}},\\
 u_1(t)&=\frac{|100\rangle+t|200\rangle}{\sqrt{1+t^2}},\\
 |\mathcal U\rangle&=|0\rangle_Ku_0+|1\rangle_Ku_1.
 \end{aligned}                                             \tag{36}
\]
The two columns are orthonormal.  Their local code reductions satisfy
\[
 \det\rho_1=0,\qquad
 \det\rho_2=\det\rho_3=\frac{t^2}{(1+t^2)^2}.              \tag{37}
\]
On the invariant subspace with ordered coordinate set
\[
\begin{aligned}
 &(0,1,1,1),\ (1,2,0,0),\ (0,2,1,1),\\
 &(1,1,0,0),\ (0,1,2,2),\ (0,2,2,2),
\end{aligned}                                               \tag{38}
\]
the corresponding block of
\[
 M_Q(P_{\mathcal U})=\prod_{i=1}^3(2E_i-I)
 (|\mathcal U\rangle\langle\mathcal U|)                   \tag{39}
\]
has a characteristic-polynomial factor
\[
 (1+t^2)^2\lambda^2
 -4(1+t^2)^2\lambda+8t^2.                                \tag{40}
\]
Thus one exact eigenvalue is
\[
 \lambda_-(t)
 =2-\frac{2\sqrt{1+t^4}}{1+t^2}.                         \tag{41}
\]
Dividing by (37) gives
\[
\frac{\lambda_-(t)}{\sum_i\det\rho_i}
=\frac{2(1+t^2)}
 {1+t^2+\sqrt{1+t^4}}
\longrightarrow1\qquad(t\longrightarrow0).               \tag{42}
\]
Consequently no universal determinant-gap coefficient larger than
\(1\) can hold.

For a particularly short exact certificate, set \(t=1\).  The block
in (38) is then
\[
 \begin{pmatrix}
 9/2&-1/2&0&1/2&0&-1/2\\
 -1/2&3/2&1&-1/2&0&1/2\\
 0&1&3&0&0&0\\
 1/2&-1/2&0&3/2&1&-1/2\\
 0&0&0&1&3&0\\
 -1/2&1/2&0&-1/2&0&9/2
 \end{pmatrix}.                                            \tag{43}
\]
The vector
\[
 x=(0,-1-\sqrt2,1,-1-\sqrt2,1,0)^{\mathsf T}              \tag{44}
\]
is an exact eigenvector with eigenvalue \(2-\sqrt2\).  In particular,
\[
 \|x\|^2=8+4\sqrt2,\qquad
 \langle x,M_Q(P_{\mathcal U})x\rangle=8.                 \tag{45}
\]
But the right side of (34), evaluated on \(x\), is
\[
 \frac32\left(\frac12\right)(8+4\sqrt2)
 =6+3\sqrt2>8.                                            \tag{46}
\]
Thus (34) fails, with exact spectral ratio
\[
 \frac{\lambda_{\min}M_Q(P_{\mathcal U})}
 {\sum_i\det\rho_i}
 \leq4-2\sqrt2<\frac32.                                  \tag{47}
\]
This does not challenge \(M_Q(P_{\mathcal U})\succeq0\);
the displayed eigenvalue is positive.  It only rules out the proposed
determinant gap and shows that any valid Hodge-determinant completion
can have coefficient at most \(1\).

There is a stronger exact obstruction: no strictly positive constant
can multiply the unconditioned sum of local determinants.  Let
\[
 |\Omega_3\rangle_{12}
 =\frac1{\sqrt3}\sum_{a=0}^2|aa\rangle,\qquad
 |\Phi_2\rangle_{K3}=|00\rangle+|11\rangle,               \tag{48}
\]
and take the isometric anchor
\[
 |\mathcal U\rangle
 =|\Omega_3\rangle_{12}\otimes|\Phi_2\rangle_{K3}.         \tag{49}
\]
Equivalently, its columns are
\[
 u_0=|\Omega_3\rangle_{12}|0\rangle_3,\qquad
 u_1=|\Omega_3\rangle_{12}|1\rangle_3.                    \tag{50}
\]
The local code reductions are
\[
 \rho_1=\rho_2=\frac23I_3,\qquad
 \rho_3=\operatorname{diag}(1,1,0),
 \qquad
 \sum_i\det\rho_i=\frac{16}{27}>0.                        \tag{51}
\]
Nevertheless the anchored operator factorizes exactly:
\[
\begin{aligned}
 M_Q(P_{\mathcal U})
 &=
 \left[(2E_1-I)(2E_2-I)P_{\Omega_3}\right]
 \otimes
 \left[(2E_3-I)P_{\Phi_2}\right]\\
 &=
 \left(\frac83I_{12}+P_{\Omega_3}\right)
 \otimes
 \left(2I_{K3}-P_{\Phi_2}\right).                         \tag{52}
\end{aligned}
\]
Here \(P_{\Phi_2}\) has eigenvalue \(2\) on
\(|\Phi_2\rangle\), so the second factor in (52) has a nonzero kernel.
Thus
\[
 \lambda_{\min}M_Q(P_{\mathcal U})=0
 \quad\text{while}\quad
 \sum_i\det\rho_i=\frac{16}{27}.                          \tag{53}
\]
Every proposed bound
\[
 M_Q(P_{\mathcal U})\succeq
 c\left(\sum_i\det\rho_i\right)I
\]
therefore fails for every \(c>0\).  A viable Hodge correction must
vanish on this tensor-factorized zero family; an unconditioned scalar
sum of the three local determinants cannot do so.
