# Intrinsic consequences of the balanced singlet normal form

## Status

This note translates the six scalar-marginal equations from the
logical Bell normal form into equations on one physical rank-two
matrix and its three common-code companions.  It then gives a
complete variational reduction of any hypothetical negative witness:
after minimizing at fixed product of the two nonzero singular values,
the **same physical matrix** can be put in the balanced Bell form and
satisfies explicit reciprocal-singular Euler--Lagrange equations.
The result is exact, but it does not prove their remaining diagonal
inequality.

After the positive-orientation polar rotation, every possible
three-copy counterexample has a representative \(C_0\) with three
companions \(C_1,C_2,C_3\) such that
\[
 {\cal B}_3(C_\alpha,C_\beta)=0\qquad(\alpha\ne\beta),
\]
where
\[
 {\cal B}_3(C,D)=
 \sum_{S\subseteq\{1,2,3\}}
 \left(-\frac12\right)^{|S|}
 \left\langle\operatorname{Tr}_S C,
 \operatorname{Tr}_S D\right\rangle_{\rm HS}.
\]
Thus the candidate is stationary on its entire four-dimensional
common left/right rank-two pencil.  All four companions also have the
same product of their two nonzero singular values.

The balancing equations do **not** force the two singular values of
the candidate to be equal.  An exact computational-basis example
below has singular-value ratio \(\sqrt2\).  It follows that a proof
cannot replace the filtered frames by isometries or reduce the
remaining problem to rank-two partial isometries.

The exact checker is
`verification/verify_n3_balanced_companion_obstruction.py`; the
linked-filter, singlet-eigenvector, and determinant-critical core
identities are independently audited in
`verification/verify_n3_full_lorentz_normal_form.py`.

## 1. The physical rank-two pencil

Let \(\widehat U,\widehat V:\mathbb C^2\to{\cal H}\) be the two
full-column frames obtained after the determinant-one logical
filters.  They span the original left and right code planes but need
not be isometries.  In the coefficient-matrix convention put
\[
 {\cal C}(M)=\widehat U M\widehat V^\dagger,\qquad M\in M_2.
\tag{1}
\]
Up to the fixed vectorization conjugation, the established two-plane
identity is
\[
 {\cal B}_3({\cal C}(M),{\cal C}(N))
 =
 \langle\operatorname{vec}M,K^\Gamma
 \operatorname{vec}N\rangle.
\tag{2}
\]

Take the normalized Bell matrices corresponding to
\[
\begin{aligned}
w_0&=|\Psi^-\rangle,&w_1&=|\Psi^+\rangle,\\
w_2&=|\Phi^-\rangle,&w_3&=|\Phi^+\rangle,
\end{aligned}
\tag{3}
\]
and denote them by \(M_\alpha\), so that
\[
 \operatorname{vec}M_\alpha=w_\alpha.
\tag{4}
\]
Equivalently, up to irrelevant phases, the four unnormalized
matrices are
\[
 iY,\quad X,\quad Z,\quad I.
\tag{5}
\]
Define
\[
 C_\alpha={\cal C}(M_\alpha),\qquad
 g_{\alpha\beta}={\cal B}_3(C_\alpha,C_\beta).
\tag{6}
\]
The four \(C_\alpha\)'s are not independently chosen: they have the
same two frames and differ only by one logical Pauli matrix.

## 2. What the scalar-marginal equations say

Let \(T=(t_{\mu\nu})\) be the real Pauli transfer matrix, in the
normalization
\[
 e_\mu=\frac{\sigma_\mu}{\sqrt2},\qquad
 t_{\mu\nu}=
 \langle{\cal E}_V(e_\mu),
 \Psi_3^{\otimes3}{\cal E}_{\overline U}(e_\nu)\rangle.
\tag{7}
\]
A direct Pauli multiplication in the Bell basis gives
\[
\begin{aligned}
2g_{01}&=t_{03}-t_{30}+i(-t_{12}+t_{21}),\\
2g_{02}&=-t_{01}+t_{10}+i(t_{23}-t_{32}),\\
2g_{03}&=t_{13}-t_{31}+i(-t_{02}+t_{20}),\\
2g_{12}&=t_{13}+t_{31}+i(t_{02}+t_{20}),\\
2g_{13}&=t_{01}+t_{10}+i(t_{23}+t_{32}),\\
2g_{23}&=t_{03}+t_{30}-i(t_{12}+t_{21}).
\end{aligned}
\tag{8}
\]
Changing phases of the Bell matrices only changes corresponding
row and column phases in this table.

It follows that the two scalar-marginal conditions
\[
 t_{0j}=t_{j0}=0\qquad(1\leq j\leq3)
\tag{9}
\]
are intrinsically the six real equations
\[
\boxed{
\begin{aligned}
\operatorname{Re}g_{01}
&=\operatorname{Re}g_{23}=0,\\
\operatorname{Re}g_{02}
&=\operatorname{Re}g_{13}=0,\\
\operatorname{Im}g_{03}
&=\operatorname{Im}g_{12}=0.
\end{aligned}}
\tag{10}
\]
They are coupled equations on one common rank-two pencil; they are
not separate partial-trace estimates.

## 3. Polar alignment gives full pencil stationarity

On the only nonautomatic orientation chart, the spatial transfer
block has positive determinant.  Its \(SO(3)\) polar rotation makes
it real symmetric positive definite.  In (8), symmetry kills the
remaining singlet--triplet entries:
\[
 g_{0j}=0\qquad(1\leq j\leq3).
\tag{11}
\]
The same logical rotation on both sides diagonalizes that symmetric
block and preserves the singlet.  The remaining triplet--triplet
entries then vanish as well.  Consequently every possible
counterexample can be put in the exact form
\[
 \boxed{\qquad
 {\cal B}_3(C_\alpha,C_\beta)
 =\lambda_\alpha\delta_{\alpha\beta}.
 \qquad}
\tag{12}
\]
Here
\[
\begin{aligned}
2\lambda_0&=s-c_1-c_2-c_3,\\
2\lambda_1&=s+c_1+c_2-c_3,\\
2\lambda_2&=s-c_1+c_2+c_3,\\
2\lambda_3&=s+c_1-c_2+c_3,
\end{aligned}
\tag{13}
\]
after harmless relabeling of the three positive spatial singular
values \(c_j\).  Positivity of the original logical Gram makes the
three triplet values positive.  The unresolved assertion is exactly
\(\lambda_0\geq0\).

Using the coefficient-matrix partial-trace identity, (12) is the
intrinsic cancellation
\[
\boxed{
\sum_{S\subseteq\{1,2,3\}}
\left(-\frac12\right)^{|S|}
\left\langle
\operatorname{Tr}_S C_\alpha,
\operatorname{Tr}_S C_\beta
\right\rangle_{\rm HS}
=0
\quad(\alpha\ne\beta).
}
\tag{14}
\]
For
\[
 C(z)=\sum_{\alpha=0}^3z_\alpha C_\alpha
\tag{15}
\]
one therefore has
\[
 Q_3(C(z))=\sum_{\alpha=0}^3
\lambda_\alpha|z_\alpha|^2.
\tag{16}
\]
Every matrix in this pencil has rank at most two.  Thus \(C_0\) is a
stationary direction for \(Q_3\) on the entire fixed pair of left and
right planes, not merely under changes of its two scalar
coefficients.

There is one more exact common-code invariant.  Put
\[
 G_U=\widehat U^\dagger\widehat U,\qquad
 G_V=\widehat V^\dagger\widehat V.
\tag{17}
\]
For every unnormalized Pauli companion \(\tau_\alpha\),
\[
\prod_{j=1}^2s_j({\cal C}(\tau_\alpha))^2
=\det G_U\,\det G_V\,|\det\tau_\alpha|^2.
\tag{18}
\]
The logical filters in the balancing proof have determinant one, so
\[
 \boxed{\qquad
 s_1({\cal C}(\tau_\alpha))
 s_2({\cal C}(\tau_\alpha))=1
 \qquad(\alpha=0,1,2,3).
 \qquad}
\tag{19}
\]
Thus all four companions have the same singular-value product even
though their individual singular values need not agree.

## 4. Exact obstruction to equal-singular-value reduction

On three qutrits take the orthonormal computational-basis code frames
\[
\begin{aligned}
u_0&=|000\rangle,&u_1&=|111\rangle,\\
v_0&=|002\rangle,&v_1&=|110\rangle.
\end{aligned}
\tag{20}
\]
For
\[
 Y=\bigotimes_{i=1}^3\left(I-\frac12F_i\right),
\tag{21}
\]
the physical logical compression, in the order
\((00,01,10,11)\), is exactly
\[
 K=\operatorname{diag}\left(
\frac14,\frac12,1,\frac14
\right).
\tag{22}
\]
All off-diagonal entries vanish by the computational-basis
contractions.

Use determinant-one filters
\[
\begin{aligned}
R&=\operatorname{diag}(2^{1/8},2^{-1/8}),\\
S&=\operatorname{diag}(2^{-1/8},2^{1/8}).
\end{aligned}
\tag{23}
\]
Then
\[
(R\otimes S)K(R\otimes S)^\dagger
=\operatorname{diag}\left(
\frac14,\frac1{\sqrt2},\frac1{\sqrt2},\frac14
\right),
\tag{24}
\]
whose two marginals are both
\[
\left(\frac14+\frac1{\sqrt2}\right)I_2.
\tag{25}
\]
Thus all six balancing equations hold exactly.

The physical singlet coefficient is, up to an irrelevant scalar
phase,
\[
 C_0
=2^{1/4}|000\rangle\langle110|
-2^{-1/4}|111\rangle\langle002|.
\tag{26}
\]
The two dyads have orthogonal left and right vectors, so the two
nonzero singular values are
\[
 2^{1/4},\qquad2^{-1/4}.
\tag{27}
\]
Their ratio is \(\sqrt2\), not one.  Direct partial contraction gives
\[
 Q_3(C_0)=\sqrt2>0.
\tag{28}
\]
This example lies on the automatic zero-orientation chart; its role
is to disprove an implication from the scalar-marginal equations,
not to approach a negative witness.

## 5. A negative witness has a determinant-normalized critical representative

The natural normalization compatible with the singlet filters is not
the Frobenius norm.  For a rank-two matrix put
\[
 \delta(C)=s_1(C)s_2(C).
\tag{29}
\]
This is the product of the two nonzero singular values.

### Theorem 5.1

If any rank-two \(C\) has \(Q_3(C)<0\), then \(Q_3\) has a negative
global minimizer on
\[
 {\cal M}=\{C:\operatorname{rank}C=2,\ \delta(C)=1\}.
\tag{30}
\]
Every such minimizer obeys the exact Euler--Lagrange equations below.

### Proof

Scale a negative witness so that \(\delta(C)=1\).  In a singular-value
decomposition write
\[
 C=r\,u_1v_1^\dagger+r^{-1}u_2v_2^\dagger,\qquad r\geq1.
\tag{31}
\]
The two diagonal rank-one energies are at least \(1/8\).  The crossed
matrix element is bounded in absolute value by
\[
 \left\|
 \bigotimes_{i=1}^3\left(I-\frac12F_i\right)
 \right\|=\frac{27}{8}.
\tag{32}
\]
Consequently
\[
 Q_3(C)\geq
 \frac18(r^2+r^{-2})-\frac{27}{4},
\tag{33}
\]
uniformly in the four singular vectors.  This tends to infinity as
\(r\to\infty\).  The two Stiefel manifolds and the remaining phase
data are compact, so a global minimizer exists.  It is negative
because the normalized original witness is an admissible point.
\(\square\)

Let \(C^+\) denote the Moore--Penrose inverse and put
\[
 N_C=(C^+)^\dagger.
\tag{34}
\]
On the smooth rank-two manifold,
\[
 d\log\delta(C)[D]
 =\operatorname{Re}\operatorname{Tr}(C^+D)
 =\operatorname{Re}\langle N_C,D\rangle_{\rm HS}.
\tag{35}
\]
The tangent space at \(C=U\Sigma V^\dagger\) consists of all \(D\)
satisfying
\[
 (I-P_U)D(I-P_V)=0.
\tag{36}
\]
Lagrange multipliers therefore give
\[
 {\cal L}(C)-\lambda N_C
 =(I-P_U)\bigl({\cal L}(C)-\lambda N_C\bigr)(I-P_V),
\qquad {\cal L}=L^{\otimes3}.
\tag{37}
\]
Since \(N_C\) is supported from \(V\) to \(U\), this is equivalently
\[
\boxed{
\begin{aligned}
{\cal L}(C)V&=\lambda U\Sigma^{-1},\\
{\cal L}(C)^\dagger U&=\lambda V\Sigma^{-1}.
\end{aligned}}
\tag{38}
\]
Taking the Hilbert--Schmidt inner product with \(C\) gives
\[
 \lambda=\frac12Q_3(C)<0.
\tag{39}
\]
Thus the two code planes are left and right singular planes of the
physical image \({\cal L}(C)\), with reciprocal rather than equal
singular values.

## 6. The critical representative can be balanced without changing it

The determinant normalization makes the Euler--Lagrange equations
compatible with the singlet stabilizer.

### Theorem 6.1 (simultaneous critical Bell form)

If a negative three-copy witness exists, there are full-column frames
\(A,B\) and a negative matrix
\[
 C=A\varepsilon B^\dagger,\qquad
 \varepsilon=iY,\qquad
 \det(A^\dagger A)=\det(B^\dagger B)=1,
\tag{40}
\]
with all of the following properties simultaneously:

1. \(C\) is a global minimizer on (30) and satisfies (38);
2. the associated Pauli transfer matrix is symmetric;
3. determinant-one linked filters, which leave \(C\) unchanged, make
   both logical marginals scalar;
4. a linked logical unitary then diagonalizes the spatial block, so
   the four companion equations (12) hold;
5. in these frames
   \[
   \boxed{\qquad
   A^\dagger{\cal L}(C)B=\lambda\varepsilon,
   \qquad \lambda=\frac12Q_3(C)<0.
   \qquad}
   \tag{41}
   \]

### Proof

Start with the minimizer from Theorem 5.1.  A determinant-one change
of its two logical frames writes it in the form (40).  For a general
factorization \(C=AMB^\dagger\), with
\[
 G_A=A^\dagger A,\qquad G_B=B^\dagger B,
\]
one has
\[
 (C^+)^\dagger
 =A\,G_A^{-1}M^{-\dagger}G_B^{-1}B^\dagger.
\tag{42}
\]
Therefore
\[
 A^\dagger(C^+)^\dagger B=M^{-\dagger}.
\tag{43}
\]
For \(M=\varepsilon\), \(M^{-\dagger}=\varepsilon\).  Projecting
(37) onto the two code planes proves (41).

Equation (2) now says that the logical singlet is an eigenvector of
\(K^\Gamma\).  The first row of (8) and its two cyclic companions show
that this is equivalent to
\[
 T=T^{\mathsf T}.
\tag{44}
\]
Thus the associated logical map \(\Lambda\) is self-adjoint for the
Hilbert--Schmidt inner product.

It remains to make the marginals scalar while preserving both this
self-adjointness and the physical matrix \(C\).  On positive
\(2\times2\) matrices \(P\) with determinant one, minimize
\[
 f(P)=\operatorname{Tr}\bigl(P\Lambda(P)\bigr).
\tag{45}
\]
If \(K\succeq mI\), then
\[
 f(P)=\operatorname{Tr}\bigl(K(P^{\mathsf T}\otimes P)\bigr)
 \geq m(\operatorname{Tr}P)^2.
\tag{46}
\]
Hence the minimization is coercive and has an interior minimizer.
For every traceless Hermitian \(X\), vary
\[
 P(t)=P^{1/2}e^{tX}P^{1/2}.
\tag{47}
\]
Self-adjointness of \(\Lambda\) gives
\[
 0=f'(0)
 =2\operatorname{Tr}\left[
 X\,P^{1/2}\Lambda(P)P^{1/2}
 \right].
\tag{48}
\]
Therefore
\[
 \Lambda(P)=\rho P^{-1}
\tag{49}
\]
for some \(\rho>0\).

Put \(H=P^{1/2}\).  The linked filter changes the logical map to
\[
 \Lambda_H(X)=H\Lambda(HXH)H.
\tag{50}
\]
It remains self-adjoint and satisfies
\[
 \Lambda_H(I)=\rho I.
\tag{51}
\]
Self-adjointness then also gives
\[
 \operatorname{Tr}\Lambda_H(X)=0
\quad\text{for every traceless }X.
\tag{52}
\]
Equations (51)--(52) are exactly both scalar-marginal conditions.

This preservation statement is exact in the Choi convention used
throughout the project.  The Choi matrix of (50) is
\[
 K_H=(\overline H\otimes H)K
 (\overline H\otimes H)^\dagger,
\tag{53}
\]
and hence
\[
 K_H^\Gamma=(H\otimes H)K^\Gamma(H\otimes H).
\tag{54}
\]
Because \(\det H=1\),
\[
 (H\otimes H)|\Psi^-\rangle=|\Psi^-\rangle.
\tag{55}
\]
Thus the same physical rank-two matrix remains the logical singlet
after filtering.  In coefficient-frame notation this is the familiar
two-dimensional identity
\[
 H\varepsilon H^{\mathsf T}
 =(\det H)\varepsilon=\varepsilon.
\tag{56}
\]
Finally the spatial block is real symmetric, and the same \(SO(3)\)
rotation on the two Pauli frames diagonalizes it.  The corresponding
linked \(SU(2)\) unitary also preserves the singlet.  This proves every
item.
\(\square\)

In nonisometric balanced frames, the full plane equations (38) can
be written without pseudoinverses as
\[
\boxed{
\begin{aligned}
{\cal L}(C)B&=\lambda A\,G_A^{-1}\varepsilon,\\
{\cal L}(C)^\dagger A&=\lambda B\,G_B^{-1}\varepsilon^\dagger.
\end{aligned}}
\tag{57}
\]
Together with the diagonal companion cancellations (14), these are
the exact critical equations left by a hypothetical negative
witness.

### Why ordinary Frobenius criticality is different

Minimizing \(Q_3(C)\) at fixed \(\|C\|_2\) also gives a negative
critical point if any negative witness exists.  In isometric SVD
frames its equations are
\[
\boxed{
\begin{aligned}
{\cal L}(C)V&=\mu\,CV=\mu U\Sigma,\\
{\cal L}(C)^\dagger U&=\mu\,C^\dagger U=\mu V\Sigma.
\end{aligned}}
\tag{58}
\]
However, applying the Bell-balancing filters generally changes this
critical matrix inside its two-plane pencil.  Thus an arbitrary
negative balanced point need not satisfy (58).

The obstruction is exact.  In balanced frames, Bell stationarity
gives
\[
 A^\dagger{\cal L}(C)B=\lambda\varepsilon,
\tag{59}
\]
whereas Frobenius criticality would give
\[
 A^\dagger{\cal L}(C)B=\mu G_A\varepsilon G_B.
\tag{60}
\]
For a negative point both multipliers are nonzero.  Hence simultaneous
Bell balance and Frobenius criticality would force
\[
 G_A\varepsilon G_B\ \text{to be proportional to }\varepsilon.
\tag{61}
\]
This is equivalent to equality of the two nonzero singular values of
\(A\varepsilon B^\dagger\).  The exact example (20)--(28) proves that
balance alone does not force (61).

## 7. What remains

Equations (12), (14), and (19) are the precise intrinsic
common-code consequences currently extracted from the filtered
normal form:

1. four rank-two companions share both singular planes;
2. they share the product of their two singular values;
3. they are pairwise orthogonal for the full alternating
   partial-trace form.

For a hypothetical negative global minimizer one may add the
reciprocal-singular Euler--Lagrange equations (38)/(57), with the
same matrix simultaneously in the critical Bell form of
Theorem 6.1.

The remaining theorem is to show that the singlet diagonal
\(\lambda_0\) cannot be negative when all four matrices arise from
one physical qutrit three-copy pair of frames.  The exact example
shows that equality of the two singular values is not an available
shortcut.
