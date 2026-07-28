# Constructive-witness search (independent subproblem)

## 2026-07-28 08:03 PDT — exact coefficient-matrix reduction

Fix the vectorization convention
\[
  |C\rangle=\sum_{a,b}C_{a,b}|a\rangle_A|b\rangle_B,
  \qquad a,b\in\{0,\ldots,d-1\}^n .
\]
For \(S\subseteq[n]\), define the simultaneous diagonal contraction
\[
  (\mathcal T_S C)_{a_{S^c},b_{S^c}}
  =\sum_{x_S}C_{(x_S,a_{S^c}),(x_S,b_{S^c})}.
\]
A direct index contraction gives the exact identity
\[
 \langle C|X_{\alpha,d}^{\otimes n}|C\rangle
 =Q_{n,\alpha}(C)
 :=\sum_{S\subseteq[n]}\alpha^{|S|}
       \|\mathcal T_S C\|_F^2.                 \tag{1}
\]
Thus all explicit dependence on \(d\) disappears from the coefficients; \(d\)
only specifies the size of the tensor indices.  Equivalently,
\[
 Q_{n,\alpha}(C)=
 \langle C,\mathcal L_\alpha^{\otimes n}(C)\rangle_F,\qquad
 \mathcal L_\alpha(A)=A+\alpha\operatorname{Tr}(A)I_d. \tag{2}
\]
At the critical endpoint,
\[
 Q_{n,-1/2}(C)=
 \sum_{S\subseteq[n]}(-1/2)^{|S|}
 \|\mathcal T_S C\|_F^2.                       \tag{3}
\]
The Schmidt rank of \(|C\rangle\) is exactly the ordinary matrix rank of \(C\).
Consequently the witness search is precisely minimization of (1) over
\(C=UV^T\), where \(U,V\) have two columns.

The discovery program `discovery/agent_witness_altmin.cpp` implements (2) and
alternately solves the two exact (floating-point in the program) compressed
eigenvalue problems obtained by fixing \(U\) and fixing \(V\).  Its output is
only conjecture-generation data, never proof.

For later exact two-term searches, let
\[
 D_r=a_rb_r^T,\qquad C=z_1D_1+z_2D_2,
\]
and define the Hermitian \(2\times2\) matrix
\[
 G_{rs}=\sum_{S\subseteq[n]}\alpha^{|S|}
 \langle\mathcal T_SD_r,\mathcal T_SD_s\rangle_F.                 \tag{1a}
\]
Then
\[
 Q_{n,\alpha}(C)=z^\dagger Gz.
\]
Thus this fixed two-term span contains a negative vector exactly when
\(\det G<0\) (the diagonal rank-one expectations are positive in the regime
at hand).  If \(|G_{12}|^2>G_{11}G_{22}\), an explicit exact choice is
\[
 C=G_{22}D_1-\overline{G_{12}}D_2,
\quad
 Q_{n,\alpha}(C)
 =G_{22}\bigl(G_{11}G_{22}-|G_{12}|^2\bigr)<0.                   \tag{1b}
\]
This is the determinant certificate used by the integer search programs.
The asserted strict positivity of the diagonal has a short direct check:
since \(X_{\alpha,d}=(I+\alpha F)^\Gamma\), for
\(D=ab^T\) and \(-1/2\le\alpha<0\),
\[
 Q_{n,\alpha}(D)
 =\langle a\otimes\overline b|
   (I+\alpha F)^{\otimes n}|a\otimes\overline b\rangle
 \ge(1+\alpha)^n\|a\|^2\|b\|^2>0.
\]

For \(n=2\), reshape \(a_r,b_r\) as \(d\times d\) matrices \(A_r,B_r\).
There is then a particularly small exact formula:
\[
\begin{aligned}
 Q_{2,\alpha}(C)
 ={}&\left\|\sum_r a_rb_r^T\right\|_F^2\\
 &+\alpha\left(
 \left\|\sum_rA_r^TB_r\right\|_F^2+
 \left\|\sum_rA_rB_r^T\right\|_F^2\right)\\
 &+\alpha^2\left|\sum_r\operatorname{Tr}(A_r^TB_r)\right|^2.
                                                                    \tag{1c}
\end{aligned}
\]
No reality assumption is made here: the transposes are ordinary
transposes, while every displayed Frobenius norm supplies the complex
conjugation.  Formula (1c) follows directly by writing out
\(\mathcal T_{\{1\}}C=\sum_rA_r^TB_r\) and
\(\mathcal T_{\{2\}}C=\sum_rA_rB_r^T\).

### Check of (1)

On one selected site,
\[
 P_d=\frac1d\sum_{x,y}|x,x\rangle\langle y,y|,
\]
so
\[
 \langle C|(P_d)_i|C\rangle
 =d^{-1}\|\mathcal T_{\{i\}}C\|_F^2.
\]
The same independent contraction on every site in \(S\) gives
\[
 \left\langle C\left|\bigotimes_{i\in S}P_d^{(i)}
 \right|C\right\rangle=d^{-|S|}\|\mathcal T_SC\|_F^2.
\]
Multiplication by \((\alpha d)^{|S|}\) in the tensor expansion proves
(1).

## Exact obstruction: copywise-product two-term vectors never work

Consider the broad structured ansatz
\[
 C=\sum_{r=1}^2\bigotimes_{i=1}^n
       (a_{r,i}b_{r,i}^T).                     \tag{4}
\]
This is the coefficient matrix of a two-term vector in which each of the four
Schmidt factors is itself a product over copies.  For every
\(\alpha\ge -1/2\),
\[
 Q_{n,\alpha}(C)\ge0.                           \tag{5}
\]

**Proof.**  Put \(A_{r,i}=a_{r,i}b_{r,i}^T\), and define a \(2\times2\)
Hermitian matrix
\[
 H_i(r,s)=\langle A_{r,i},A_{s,i}\rangle_F
 +\alpha\,\overline{\operatorname{Tr}A_{r,i}}\,
                 \operatorname{Tr}A_{s,i}.
\]
For \(z\in\mathbb C^2\),
\[
 z^*H_i z=Q_{1,\alpha}\left(\sum_rz_rA_{r,i}\right).
\]
The matrix in parentheses has rank at most two.  For every rank-at-most-two
matrix \(A\),
\[
 |\operatorname{Tr}A|
 \le\|A\|_*\le\sqrt2\|A\|_F,
\]
and hence
\[
 Q_{1,\alpha}(A)=\|A\|_F^2+\alpha|\operatorname{Tr}A|^2\ge0
 \quad(\alpha\ge-1/2).
\]
Therefore each \(H_i\) is positive semidefinite.  Expanding (1) for (4)
factor by factor gives
\[
 Q_{n,\alpha}(C)=\sum_{r,s=1}^2\prod_{i=1}^nH_i(r,s)
 ={\bf1}^*\left(H_1\circ\cdots\circ H_n\right){\bf1}.
\]
The Hadamard product is positive semidefinite (it is a principal compression
of the tensor product of the \(H_i\)), proving (5). \(\square\)

This rules out the most natural GHZ-type/copywise-product constructive
search, including arbitrary complex local factors and unequal amplitudes.
Any endpoint witness must have genuine entanglement *within copies on at
least one of the four global Schmidt factors*; merely correlating two
copywise product terms cannot suffice.

## 2026-07-28 08:21 PDT — stronger one-sided product-space obstruction

The preceding obstruction admits a substantially stronger operator proof.

**Proposition.**  Let \(\alpha\ge-1/2\).  Suppose a Schmidt-rank-two vector
has a presentation
\[
 |\psi\rangle
 =\left(\bigotimes_{i=1}^n|a_{1,i}\rangle\right)|b_1\rangle
 +\left(\bigotimes_{i=1}^n|a_{2,i}\rangle\right)|b_2\rangle,       \tag{6}
\]
where \(b_1,b_2\in(\mathbb C^d)^{\otimes n}\) are completely arbitrary
(and can be highly entangled among the copies).  Then
\[
 \langle\psi|X_{\alpha,d}^{\otimes n}|\psi\rangle\ge0.             \tag{7}
\]
The analogous statement holds with \(A\) and \(B\) exchanged.

**Proof.** For each site define
\[
 W_i:\mathbb C^2\longrightarrow\mathbb C^d,\qquad
 W_i|r\rangle=|a_{r,i}\rangle,
\]
and
\[
 K_i=(W_i^\dagger\otimes I)X_{\alpha,d}(W_i\otimes I)
 \quad\text{on }\mathbb C^2\otimes\mathbb C^d.
\]
Every vector in the image of \(W_i\otimes I\) has Schmidt rank at most two.
The one-copy trace inequality proved above therefore shows \(K_i\succeq0\).
Hence \(K_1\otimes\cdots\otimes K_n\succeq0\).

Let
\[
 J:\mathbb C^2\longrightarrow(\mathbb C^2)^{\otimes n},
 \qquad J|r\rangle=|r\rangle^{\otimes n}.
\]
The \(r,s\) operator block (on all the \(B\) systems) of
\[
 (J^\dagger\otimes I)(K_1\otimes\cdots\otimes K_n)(J\otimes I)
\]
is
\[
 \bigotimes_i\langle r|K_i|s\rangle
 =\bigotimes_i\langle a_{r,i}|X_{\alpha,d}|a_{s,i}\rangle.
\]
Consequently its quadratic form on
\(\sum_r|r\rangle|b_r\rangle\) is exactly the left side of (7).
It is a compression of a positive semidefinite operator, proving (7).
\(\square\)

In coefficient-matrix language, if either the two-dimensional column space
or the two-dimensional row space of \(C\) has a basis consisting of tensors
that are product over the \(n\) copies, then \(C\) cannot be a witness.
Thus a counterexample to all-copy undistillability must use *both* a column
space and a row space not spanned by two fully decomposable tensors.  This
eliminates even ansätze in which only one side is given arbitrary within-side
entanglement.

At \(\alpha=-1/2\), the one-copy equality used in this proof is sharp:
for nonzero rank-at-most-two \(A\),
\[
 Q_{1,-1/2}(A)=0
\]
if and only if \(A\) is a nonzero scalar times a rank-two orthogonal
projection.  Indeed, equality must hold both in
\(|\operatorname{Tr}A|\le\|A\|_*\) and in
\(\|A\|_*\le\sqrt2\|A\|_F\).  The first forces the left and right singular
vectors to agree up to one common phase, and the second forces the two
nonzero singular values to agree.

## 2026-07-28 08:44 PDT — stress test, stronger local-support theorem, equality

The preceding compression has no hidden orthogonality assumption.  In fact,
the product-basis formulation is a corollary of the following stronger
statement.

**Local-support theorem.** Let \(S_i\subseteq\mathbb C^d\) have
\(\dim S_i\le2\).  For every (not necessarily Schmidt-rank-two) vector
\[
 |\psi\rangle\in
 \left(\bigotimes_{i=1}^n S_i\right)_A
 \otimes\left(\bigotimes_{i=1}^n\mathbb C^d\right)_B
\]
and every \(\alpha\ge-1/2\),
\[
 \langle\psi|X_{\alpha,d}^{\otimes n}|\psi\rangle\ge0.             \tag{8}
\]
The same holds after exchanging \(A\) and \(B\).

**Proof with all maps explicit.** Choose an isometric inclusion
\(V_i:\mathbb C^{s_i}\to\mathbb C^d\), where \(s_i=\dim S_i\), and regroup
the tensor factors in the interleaved order
\[
 (A_1B_1)(A_2B_2)\cdots(A_nB_n).
\]
Set
\[
 \widehat X_i=(V_i^\dagger\otimes I_{B_i})
 X_{\alpha,d}(V_i\otimes I_{B_i}).
\]
For arbitrary \(z_i\in\mathbb C^{s_i}\otimes\mathbb C^d\), the coefficient
matrix of \((V_i\otimes I)z_i\) has rank at most \(s_i\le2\).  Hence the
one-copy trace inequality gives
\(\langle z_i|\widehat X_i|z_i\rangle\ge0\), so
\(\widehat X_i\succeq0\).  Therefore
\[
 \bigotimes_i\widehat X_i\succeq0.
\]
If \(\widehat\psi=((\bigotimes_iV_i^\dagger)\otimes I)\psi\), with the
harmless regrouping permutation understood, then exactly
\[
 \langle\psi|X_{\alpha,d}^{\otimes n}|\psi\rangle
 =\left\langle\widehat\psi\left|
 \bigotimes_i\widehat X_i\right|\widehat\psi\right\rangle\ge0.
\]
This proves (8).

For (6), take \(S_i=\operatorname{span}\{a_{1,i},a_{2,i}\}\).  This remains
valid if these two local vectors are nonorthogonal, proportional, or
unnormalized.  The opposite-side tensors \(b_1,b_2\) never enter the
positivity argument and are completely arbitrary.

For completeness, the earlier label-compression proof can be written as one
literal congruence.  Define \(W_i|r\rangle=a_{r,i}\),
\(K_i=(W_i^\dagger\otimes I)X(W_i\otimes I)\), and
\[
 J|r\rangle=|r\rangle^{\otimes n}.
\]
For \(z=\sum_r|r\rangle|b_r\rangle\), after the same interleaving
permutation,
\[
 |\psi\rangle=((\bigotimes_iW_i)\otimes I)(J\otimes I)|z\rangle
\]
and
\[
 \langle\psi|X^{\otimes n}|\psi\rangle
 =\langle z|(J^\dagger\otimes I)
       (\bigotimes_iK_i)(J\otimes I)|z\rangle.
\]
No \(W_i^\dagger W_i=I\) is used.  This checks both the nonorthogonal case
and every operator-block index order.  The script
`discovery/agent_witness_product_verify.py` independently checks this
identity with integer arithmetic for \(d=n=3\), nonorthogonal local vectors,
and two arbitrary entangled opposite-side tensors.

### Exact equality statement for the local-support theorem

For \(\alpha>-1/2\), each \(\widehat X_i\) is positive definite.  Indeed, for
a nonzero coefficient matrix \(A\) of rank at most two,
\[
 \|A\|_F^2+\alpha|\operatorname{Tr}A|^2
 \ge
 \begin{cases}
 (1+2\alpha)\|A\|_F^2,&-1/2<\alpha<0,\\
 \|A\|_F^2,&\alpha\ge0.
 \end{cases}
\]
Thus (8) is strict for every nonzero \(\psi\).

At \(\alpha=-1/2\), \(\widehat X_i\) is positive definite when
\(\dim S_i\le1\).  When \(\dim S_i=2\), its kernel is the one-dimensional
space spanned by
\[
 |\omega_{S_i}\rangle
 =\sum_{k=1}^2|s_{i,k}\rangle_A|\overline{s_{i,k}}\rangle_B,       \tag{9}
\]
where \(\{s_{i,1},s_{i,2}\}\) is any orthonormal basis of \(S_i\).
This follows from the one-copy equality classification: the coefficient
matrix must be a scalar multiple of the orthogonal projection \(P_{S_i}\).
Consequently equality in (8) holds exactly when, in interleaved order,
\[
 |\psi\rangle\in
 \sum_{\substack{i\in[n]\\\dim S_i=2}}
 \left(\bigotimes_{j<i}(S_j\otimes B_j)\right)
 \otimes\operatorname{span}\{|\omega_{S_i}\rangle\}
 \otimes\left(\bigotimes_{j>i}(S_j\otimes B_j)\right).            \tag{10}
\]
Equation (10) is just the standard kernel formula for a tensor product of
positive semidefinite operators.

In particular, the endpoint infimum is at most zero for every \(d\ge2,n\):
with \(P_2=|0\rangle\langle0|+|1\rangle\langle1|\), the coefficient matrix
\[
 C=P_2\otimes(|0\rangle\langle0|)^{\otimes(n-1)}
\]
has rank exactly two and
\[
 Q_{n,\alpha}(C)
 =2(1+2\alpha)(1+\alpha)^{n-1}.                                  \tag{10a}
\]
It is therefore an exact zero vector at \(\alpha=-1/2\).  This also checks
that any uniform endpoint lower bound, if true, must be sharp.

### What this says about low bond dimension

The extension is stronger than a bond-dimension statement: arbitrary
within-\(A\) entanglement and arbitrary tensor-network bond dimension are
allowed, provided the joint physical support of the two \(A\)-side Schmidt
vectors has dimension at most two at every site.  Equivalently, if
\[
 a_1,a_2\in S_1\otimes\cdots\otimes S_n,\qquad \dim S_i\le2,
\]
then no witness is possible, regardless of their internal tensor rank.

Bond dimension alone does **not** extend this compression proof.  A
bond-two tensor can have a three-dimensional physical support at an interior
site.  For example,
\[
 |000\rangle+|011\rangle+|120\rangle
\]
has Schmidt rank two across each consecutive cut (and hence an
open-boundary bond-two representation), but its middle-site support is all
of \(\mathbb C^3\).  The corresponding local compression can then contain the negative
maximally entangled direction of \(X_{-1/2,3}\).  Thus the exact sufficient
condition furnished by this method is local physical support at most two,
not merely virtual bond dimension at most two.  This is a limitation of the
argument, not evidence that a full-support bond-two witness exists.

## 2026-07-28 09:02 PDT — mixed-side local supports

There is a further useful strengthening: the compressed side can be chosen
independently at each copy.

**Mixed-support theorem.**  Let \(S_i,T_i\subseteq\mathbb C^d\), and suppose
\[
 |\psi\rangle\in\bigotimes_{i=1}^n(S_i\otimes T_i)
\]
in interleaved \(A_iB_i\) order.  If
\[
 \min(\dim S_i,\dim T_i)\le2\qquad\text{for every }i,              \tag{11}
\]
then for every \(\alpha\ge-1/2\),
\[
 \langle\psi|X_{\alpha,d}^{\otimes n}|\psi\rangle\ge0.             \tag{12}
\]

Indeed, every vector in \(S_i\otimes T_i\) has Schmidt rank at most
\(\min(\dim S_i,\dim T_i)\le2\).  Thus the compression of \(X_{\alpha,d}\)
to \(S_i\otimes T_i\) is positive semidefinite; tensor the \(n\) local
compressions.  This proof is indifferent to which side is the smaller one
at each site.

There is also a quantitative version.  Put
\(k_i=\min(\dim S_i,\dim T_i)\).  For \(-1/2\le\alpha<0\), the rank-\(k_i\)
trace bound gives the local operator inequality
\[
 X_{\alpha,d}\big|_{S_i\otimes T_i}\succeq(1+\alpha k_i)I.
\]
Consequently
\[
 \langle\psi|X_{\alpha,d}^{\otimes n}|\psi\rangle
 \ge\left(\prod_i(1+\alpha k_i)\right)\|\psi\|^2.                 \tag{12a}
\]
For \(\alpha\ge0\), the analogous lower bound is simply \(\|\psi\|^2\).
In particular, (12) is uniformly strict above the endpoint.

For \(\alpha>-1/2\), (12) is strict for nonzero \(\psi\).  At the endpoint,
the local compression on \(S_i\otimes T_i\) has a kernel precisely when
\[
 \dim(S_i\cap\overline{T_i})=2.                                  \tag{13}
\]
To see the conjugation in (13) explicitly, choose isometric basis matrices
\(V_i,W_i\) for \(S_i,T_i\).  A coefficient matrix in this local subspace is
\[
 C=V_iZW_i^T.
\]
Hence \(\operatorname{ran}C\subseteq S_i\) and
\(\operatorname{ran}C^\dagger\subseteq\overline{T_i}\).  Endpoint equality
requires \(C\) to be a scalar multiple of a rank-two orthogonal projection,
so its range must be a two-plane
\(R_i\subseteq S_i\cap\overline{T_i}\).  Under (11), such a plane is unique
when it exists.  The local kernel is then spanned by
\[
 |\omega_{R_i}\rangle=\sum_{k=1}^2|r_{i,k}\rangle
 |\overline{r_{i,k}}\rangle .
\]
The global equality space is the sum of tensor-factor kernels exactly as in
(10).

For a rank-two coefficient matrix, let \(\mathcal U\) be its column
two-plane and let \(\mathcal V\) be the corresponding two-plane of physical
\(B\)-side Schmidt factors.  Let \(S_i\) and \(T_i\) be their minimal
one-site supports (the spans of all mode-\(i\) fibers of vectors in
\(\mathcal U\) and \(\mathcal V\), respectively).  A necessary condition for
a witness is now
\[
 \text{there is a site }i\text{ with }\dim S_i\ge3
 \text{ and }\dim T_i\ge3.                                       \tag{14}
\]
For \(d=3\), both local supports must be full on at least one common copy.
Thus it is not enough to give the \(A\) and \(B\) Schmidt planes full support
on disjoint sets of copies.

## Exact two-copy obstruction for positive coefficient matrices

Another natural ansatz is a Schmidt-rank-two coefficient matrix that is,
up to a scalar phase, positive semidefinite.  It cannot be a two-copy
endpoint witness.

**Proposition.** If \(H\succeq0\) and \(\operatorname{rank}H\le2\), viewed as
an operator on \(\mathbb C^d\otimes\mathbb C^d\), then, for every
\(\alpha\ge-1/2\),
\[
 Q_{2,\alpha}(H)\ge0.                                              \tag{15}
\]
The same is true for \(C=e^{i\theta}H\).  For nonzero \(H\) and
\(\alpha>-1/2\), the inequality is strict.  At \(\alpha=-1/2\), equality
holds exactly when
\[
 H=\lambda P_{\mathcal S},\qquad \lambda>0,
\]
where the two-plane \(\mathcal S\) has one of the forms
\[
 \mathcal S=a\otimes T\quad\text{or}\quad
 \mathcal S=T\otimes b,\qquad \dim T=2.                            \tag{16}
\]

**Proof.**  Let \(F_1,F_2\) swap, respectively, the first and second tensor
factors between two replicas.  The swap trick gives
\[
 \|\operatorname{Tr}_1H\|_F^2
 +\|\operatorname{Tr}_2H\|_F^2
 =\operatorname{Tr}\big[(H\otimes H)(F_1+F_2)\big].
\]
The commuting involutions \(F_1,F_2\) obey
\[
 I+F_1F_2-F_1-F_2=(I-F_1)(I-F_2)\succeq0.
\]
Therefore
\[
 \|\operatorname{Tr}_1H\|_F^2+\|\operatorname{Tr}_2H\|_F^2
 \le(\operatorname{Tr}H)^2+\operatorname{Tr}(H^2).                \tag{17}
\]
For \(-1/2\le\alpha<0\), substitution into the two-copy contraction formula
and use of the negative sign of \(\alpha\) yields
\[
\begin{aligned}
 Q_{2,\alpha}(H)
 &=\operatorname{Tr}(H^2)
 +\alpha\left(
 \|\operatorname{Tr}_1H\|_F^2+\|\operatorname{Tr}_2H\|_F^2\right)
 +\alpha^2(\operatorname{Tr}H)^2\\
 &\ge(1+\alpha)\left[
 \operatorname{Tr}(H^2)+\alpha(\operatorname{Tr}H)^2\right]\ge0,
\end{aligned}
\]
where the last inequality uses \(\operatorname{rank}H\le2\) and
\(\alpha\ge-1/2\).  For \(\alpha\ge0\), nonnegativity is immediate term by
term in (1).  At the endpoint, the displayed lower bound becomes
\[
\frac12\operatorname{Tr}(H^2)-\frac14(\operatorname{Tr}H)^2.
\]

For equality, the two nonzero eigenvalues of \(H\) must agree, so
\(H=\lambda P_{\mathcal S}\) with \(\dim\mathcal S=2\), and equality must
hold in (17).  The latter says that the double-antisymmetric projection
\(\frac14(I-F_1)(I-F_2)\) annihilates
\(\mathcal S\otimes\mathcal S\).  In particular, for every
\(u\in\mathcal S\), all \(2\times2\) minors of the matrix reshaping of \(u\)
vanish; hence every vector in \(\mathcal S\) is a product vector.  Write two
independent generators as \(a\otimes b\) and \(c\otimes e\).  If both
\(\{a,c\}\) and \(\{b,e\}\) were independent, their sum would have matrix
rank two, a contradiction.  Thus one factor is common, giving exactly
(16).  The converse is immediate, so the equality classification is exact.
\(\square\)

This rules out a full-support, internally entangled class not covered merely
by guessing product Schmidt factors.  The proof uses the special two-replica
swap inequality and does not by itself tensorize to \(n\ge3\).

## Discovery-only search record

These calculations are recorded only to prevent repetition; none is used as
evidence for an all-copy claim.

- `agent_witness_altmin.cpp` performs real floating-point alternating
  minimization over \(C=UV^T\).  With \(d=3,\alpha=-1/2\), independent
  restarts for \(n=2,3,4\) converged to values between roughly
  \(-4.5\cdot10^{-17}\) and \(2.5\cdot10^{-13}\), i.e. numerical versions
  of the exact zero families, and never to a resolved negative value.
- The same search at
  \(\alpha\in\{-0.49,-0.45,-0.40,-0.34\}\) and \(n=2,3,4\) returned positive
  values.  Several outputs exactly matched, to floating precision, the
  normalized product-family value coming from (10a).  The method is
  nonconvex and real-only, so this is not a certificate.
- `agent_witness_sparse.cpp` uses exact signed integer arithmetic at the
  endpoint.  For two rank-one terms \(C_1,C_2\), it computes
  \[
    R_{rs}=2^n\langle C_r,\mathcal L_{-1/2}^{\otimes n}(C_s)\rangle
    \in\mathbb Z
  \]
  and checks the exact negative-span criterion
  \(R_{12}^2>R_{11}R_{22}\).  Random sparse searches included nearby and
  independent factors plus Hermitian spans \(uu^T,vv^T\).  Runs comprised
  \(10^6\) trials each at \(n=3,4\) and \(5\cdot10^5\) trials at \(n=5\),
  with support at most ten and coefficients in
  \(\{\pm1,\pm2\}\); no negative span appeared.  Boundary ratio one was
  repeatedly attained by exact zero/product families.
- After proving (14), an exact rank filter was added that retains only
  samples having a common copy with full three-dimensional local support on
  both sides.  Corrected runs of \(3\cdot10^5\) trials at each of
  \(n=2,3,4\) again found no negative span.  Their best squared cross ratios
  were approximately \(0.9811,0.9800,0.9858\), respectively (the compared
  integer determinants, not these decimal displays, were used by the
  program).  This filter removes the ubiquitous theorem-forced equality
  strata but does not make the random sample exhaustive.
- `agent_witness_sparse_complex.cpp` repeats the filtered search over
  Gaussian-integer factors with coefficients in
  \(\{\pm1,\pm i,\pm1\pm i\}\).  It computes the full Hermitian cross term
  \(R_{12}\in\mathbb Z[i]\) and tests
  \(|R_{12}|^2>R_{11}R_{22}\) exactly.  Corrected nonproportional runs of
  \(3\cdot10^5\) trials at each of \(n=2,3,4\) found no negative span; their
  best ratios were approximately \(0.9499,0.9647,0.9741\).  If the exact
  determinant test ever succeeds, the program prints the explicit
  Gaussian-integer witness
  \(C=R_{22}C_1-\overline{R_{12}}C_2\).
- `agent_witness_signed_permutations.cpp` exhaustively checks the
  \(d=3,n=2\) ansatz in which all four within-side factors are
  vectorizations of signed permutation matrices.  These are internally
  maximally entangled and have full local support, so they deliberately
  evade (14).  Among all \(2{,}437{,}632\) nondegenerate pairs of rank-one
  terms, the exact determinant test found no negative span; the largest
  squared cross ratio was only \(1/4\).  This is an exact classification of
  that finite ansatz, not of general two-copy vectors.
- `agent_witness_product_verify.py` evaluates the nonorthogonal
  one-sided-product compression in two independent ways.  Its fixed
  \(d=n=3\) test gives
  \(2^nQ=31262\) in both contractions.

The useful negative lesson is structural: searches that allow a zero family
will be strongly attracted to it, so an unconstrained local optimizer is a
poor detector of a hypothetical shallow negative well.  Any future search
should quotient out the equality strata and enforce the necessary
full-local-support condition (14) on both sides.
