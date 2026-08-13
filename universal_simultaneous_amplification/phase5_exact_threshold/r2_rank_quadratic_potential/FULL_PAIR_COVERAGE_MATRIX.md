# The literal full-pair coverage matrix and its first Loewner obstruction

Date: 2026-08-13 (America/Los_Angeles)

## Status

This note lifts the stationary coverage-deficit current to the literal
pair matrix.  The matrix renewal law, its rank-weighted Poisson identity,
and the positive test-set Gram representation of the concavity remainder
are **PROVED**.

Their canonical target-labelled Loewner strengthening is **EXACTLY
REFUTED** by a regular four-vertex rational graph.  Its trace remains
strictly positive and is exactly the desired endpoint gap.  Thus the
counterexample refutes only the matrix ordering, not the fitness-two
maximality conjecture.

## 1. Eventwise pair renewal

Let `A` be a proper nonempty state of the fair-geometric union dual and
write `s=1_A`.  Use the zero-diagonal ordered-pair matrix

\[
 \mathsf P(A)=ss^T-\operatorname {Diag}(s).                \tag{1}
\]

When the active target is `v in A`, put `b=s-e_v`.  Let `J` be the set of
previous holes hit at least once by the row-`v` burst, and write `j=1_J`.
The output indicator is `s'=b+j`, with `b` and `j` having disjoint support.
Consequently

\[
\boxed{
 \mathsf P(A')-\mathsf P(A)
 =-be_v^T-e_vb^T+bj^T+jb^T+jj^T-\operatorname {Diag}(j).}
                                                               \tag{2}
\]

Define the two creation matrices

\[
 \mathsf C^{(1)}(A)=\sum_{v\in A}E_v[bj^T+jb^T],          \tag{3}
\]

\[
 \mathsf C^{(2)}(A)=\sum_{v\in A}E_v
       [jj^T-\operatorname {Diag}(j)].                    \tag{4}
\]

Summing the first two terms of `(2)` over `v in A` gives
`-2 P(A)`.  Thus the full pair matrix has the exact generator law

\[
\boxed{
 \mathcal L\mathsf P=-2\mathsf P+
 \mathsf C^{(1)}+\mathsf C^{(2)}.}                        \tag{5}
\]

This is the literal matrix form of pair deletion, cross-pair creation, and
hole-pair creation.  No edge coefficient has yet been contracted.

## 2. Exact map to the scalar burst current

Put `N=n-1`, let `K` be the loopless complete kernel, and define

\[
 K_{ij}={1\over N}\mathbf1_{\{i\ne j\}},\qquad R=P-K.     \tag{6}
\]

The symmetric edge-discrepancy matrix is

\[
 \mathsf E=-(R+R^T),\qquad
 \mathsf E_{ij}={2\over N}-P_{ij}-P_{ji}\quad(i\ne j),
 \qquad \mathsf E_{ii}=0.                                \tag{7}
\]

For the Frobenius product `X:Y=Tr(X^T Y)`, the internal-edge deficit is

\[
 Z_P(A)={1\over2}\mathsf E:\mathsf P(A).                 \tag{8}
\]

Equations `(3)--(4)` retain exactly the scalar creations from the coverage
formulation:

\[
 C_a(A)={1\over2}\mathsf E:\mathsf C^{(a)}(A),
 \qquad a=1,2.                                           \tag{9}
\]

Indeed, `(3)` counts one newly hit hole against every retained occupied
vertex, while `(4)` counts jointly hit unordered hole pairs.  Contracting
`(5)` by `E/2` is therefore precisely
`L Z_P=-2Z_P+C_1+C_2`.

Let `U_h` be the exact complete-Green rank weight, where `h=|A^c|`, and
write `h'=|(A')^c|`.  Before contraction its commutator is

\[
 \mathsf R_U(A)=\sum_{v\in A}E_v
 [(U_{h'}-U_h)\mathsf P(A')].                            \tag{10}
\]

The matrix-valued Poisson identity is

\[
\boxed{
 \mathcal L(U_h\mathsf P)
 =-2U_h\mathsf P+U_h(\mathsf C^{(1)}+\mathsf C^{(2)})
  +\mathsf R_U.}                                         \tag{11}
\]

For the stationary dual law `Pi`, put

\[
 \overline{\mathsf B}=E_\Pi[
 U_h(\mathsf C^{(1)}+\mathsf C^{(2)})+\mathsf R_U].      \tag{12}
\]

Stationarity in `(11)` gives the exact full-pair balance

\[
\boxed{
 \overline{\mathsf B}=2E_\Pi[U_h\mathsf P(A)].}          \tag{13}
\]

In particular `Bbar` is symmetric and has zero diagonal.  Its discrepancy
contraction is the scalar mixed burst current:

\[
 {1\over2}\mathsf E:\overline{\mathsf B}
 =E_\Pi[U_h(C_1+C_2)+\mathcal R_U]=2E_\Pi[U_hZ_P].       \tag{14}
\]

## 3. The concavity remainder is a positive full-pair test Gram

Let `r_v^T=e_v^TR` be row `v` of the complete-kernel deviation.  For
`v in A` and `H=A^c`, define

\[
\begin{split}
 \mathsf T_v(A)=\sum_{k=1}^{h}c_k{2\over(1+k/N)^2}
 \sum_{\substack{S\subseteq H\\|S|=k}}
 {1_S1_S^T\over1+P_{vS}}\succeq0.                       \tag{15}
\end{split}
\]

This is rational whenever `P` is rational.  Because `v notin S`,

\[
 r_v^T1_S=P_{vS}-{k\over N}.                             \tag{16}
\]

Hence the target-`v` part of the exact dispersion is

\[
 \mathcal V_v(A)=r_v^T\mathsf T_v(A)r_v\ge0,
 \qquad
 \mathcal V_P(A)=\sum_{v\in A}\mathcal V_v(A).          \tag{17}
\]

Equivalently, the vertex-pair matrix

\[
 \mathsf W(A)=\sum_{v\in A}\sum_{k,S}
 {2c_k\over(1+k/N)^2(1+P_{vS})}
 \operatorname {Diag}(r_v)1_S1_S^T\operatorname {Diag}(r_v)
 \succeq0                                                \tag{18}
\]

satisfies `1^T W(A) 1=V_P(A)`.  Thus `(15)` and `(18)` are two exact
matrix lifts of the same positive remainder: the first keeps the active
target label and the second keeps the tested vertex-pair labels.

Let

\[
 \overline d_v=E_\Pi[\mathbf1_{\{v\in A\}}\mathcal V_v(A)],
 \qquad
 \mathsf D_{\mathcal V}=\operatorname {Diag}(\overline d_v)\succeq0.
                                                               \tag{19}
\]

Then `Tr(D_V)=E_Pi V_P`.

## 4. An exact target-matrix contraction

Combining the pair current with the target-labelled Gram gives the
canonical symmetric matrix

\[
\boxed{
 \mathsf Q_P=2\mathsf D_{\mathcal V}
 +\operatorname {Sym}(R\overline{\mathsf B}^{,T}),
 \qquad \operatorname {Sym}(X)={X+X^T\over2}.}           \tag{20}
\]

Since `Bbar` is symmetric and `E=-(R+R^T)`, its trace is exactly the
negative of the circulation-corrected SID residual:

\[
\boxed{
 E_\Pi[U_h(C_1+C_2)+\mathcal R_U-2\mathcal V_P]
 =-\operatorname {Tr}\mathsf Q_P.}                       \tag{21}
\]

Thus the fitness-two upper theorem is equivalently

\[
 \operatorname {Tr}\mathsf Q_P\ge0.                     \tag{22}
\]

More precisely, the exact coverage comparison gives

\[
 \boxed{
 \rho_{\rm dB}(K_n,2)-\rho_{\rm dB}(P,2)
 ={1\over2}\operatorname {Tr}\mathsf Q_P.}               \tag{23}
\]

Equation `(20)` is not a scalar lower envelope or an affine spectral
gauge.  It is the literal full-pair burst current paired with the exact
row/test Gram before the final trace.

## 5. The first Loewner strengthening is exactly false

The most direct matrix strengthening of `(22)` is

\[
 \mathsf Q_P\succeq0.                                    \tag{24}
\]

It is false even when the original graph is regular.  On the weighted
complete graph with edge weights

\[
 (w_{01},w_{02},w_{03},w_{12},w_{13},w_{23})
 =(1,1,2,2,1,1),                                         \tag{25}
\]

every degree is four, and the exact stationary dual calculation gives

\[
 \mathsf Q_P=
 \begin{pmatrix}
 {1\over1148}&{375\over36736}&{375\over36736}&-{1461\over91840}\\
 {375\over36736}&{1\over1148}&-{1461\over91840}&{375\over36736}\\
 {375\over36736}&-{1461\over91840}&{1\over1148}&{375\over36736}\\
 -{1461\over91840}&{375\over36736}&{375\over36736}&{1\over1148}
 \end{pmatrix}.                                         \tag{26}
\]

Its leading two-by-two principal minor is

\[
 \det\mathsf Q_P[\{0,1\}]
 =-{2849\over27541504}<0,                                \tag{27}
\]

so `(24)` fails.  Nevertheless

\[
 \operatorname {Tr}\mathsf Q_P={1\over287}>0,           \tag{28}
\]

which agrees exactly with twice the already verified SID gap
`V_P-E_Pi(U_hZ_P)=1/574`.  The graph therefore satisfies the desired
endpoint comparison strictly.

This separates the live trace theorem from its first matrix-ordering
strengthening.  Pair labels cannot be certified independently in Loewner
order; the proof must retain cancellation among target modes when taking
the final trace, or introduce a genuinely nonlocal matrix Poisson metric.
The independent exact replay is `verify_full_pair_coverage_matrix.py`.
