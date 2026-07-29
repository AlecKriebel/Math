# Three-copy anchor: Pauli--exterior and universal-inversion recouplings

## Status

This note does **not** prove unrestricted three-copy positivity.  It gives
three exact, compatible reformulations of the remaining anchored
inequality:

1. a completely-copositive Kraus-frame formula in which the only negative
   output is the one-dimensional logical exterior square;
2. a Pauli/Plücker formula which separates the already-proved positive
   rank-two slack from one residual exterior form;
3. a universal-inversion formula which reduces positivity to one explicit
   weighted Koszul/Bessel inequality between nested antisymmetric frames.

The second formula is strictly more informative than separating the
odd- and even-total-parity brackets.  It retains their cancellation, and
both known transverse zero families saturate it without introducing a
false positive margin.

The independent exact checker is
`verification/verify_n3_exterior_koszul_recoupling.py`.

## 1. The completely-copositive Fierz frame

Fix real computational bases on the physical spaces
\[
 {\cal H}=H_1\otimes H_2\otimes H_3.
\]
On \(M(H_i)\), choose real Hilbert--Schmidt orthonormal bases
\(\mathscr S_i,\mathscr A_i\) of the symmetric and skew-symmetric
matrices.  Thus
\[
 \sum_{S\in\mathscr S_i}|\operatorname{vec}S\rangle
  \langle\operatorname{vec}S|=\frac{I+F_i}{2},
\qquad
 \sum_{A\in\mathscr A_i}|\operatorname{vec}A\rangle
  \langle\operatorname{vec}A|=\frac{I-F_i}{2}.             \tag{1}
\]
For a tensor choice \(R=R_1\otimes R_2\otimes R_3\), let \(r(R)\)
be the number of skew local factors and absorb the scalar
\[
 2^{-3/2}3^{r(R)/2}
                                                               \tag{2}
\]
into \(R\).

Let
\[
 {\cal K}={\cal K}_++{\cal K}_-,\qquad
 {\cal L}={\cal K}_+-{\cal K}_-
                                                               \tag{3}
\]
be the even/odd completely-copositive splitting from
`agent_n3_anchor_qubit_cp.md`.  Equations (1)--(2) give the explicit
Kraus formulas
\[
\begin{aligned}
 {\cal K}_+(X)&=\sum_{r(R)\ {\rm even}}RX^{\mathsf T}R^\dagger,\\
 {\cal K}_-(X)&=\sum_{r(R)\ {\rm odd}}RX^{\mathsf T}R^\dagger .
\end{aligned}                                                \tag{4}
\]
The global transpose parity is
\[
 R^{\mathsf T}=(-1)^{r(R)}R.                                \tag{5}
\]

Now take a singular-value decomposition
\[
 C=s_1|u_1\rangle\langle v_1|
   +s_2|u_2\rangle\langle v_2|,
 \qquad s_1,s_2\geq0,                                       \tag{6}
\]
with both displayed pairs orthonormal.  Put
\[
 U=(u_1,u_2),\qquad V=(v_1,v_2),\qquad
 D=\operatorname{diag}(s_1,s_2),
\qquad
 Z_R=D^{1/2}U^{\mathsf T}RV D^{1/2}.                        \tag{7}
\]

### Proposition 1.1

One has the exact Fierz identity
\[
 \boxed{\qquad
 Q_3(C)=
 \sum_R\left(
   \left\|\frac{Z_R+Z_R^{\mathsf T}}2\right\|_2^2
  -\left\|\frac{Z_R-Z_R^{\mathsf T}}2\right\|_2^2
 \right).
 \qquad}                                                    \tag{8}
\]

#### Proof

For \(E_a=|u_a\rangle\langle v_a|\), a Kraus term in (4) gives
\[
\begin{aligned}
 \langle E_a,R E_b^{\mathsf T}R^\dagger\rangle_{\rm HS}
 &=
 (u_a^\dagger R\overline v_b)(u_b^{\mathsf T}R^\dagger v_a)\\
 &=(-1)^{r(R)}
   \overline{(U^{\mathsf T}RV)_{ab}}\,
   (U^{\mathsf T}RV)_{ba}.
\end{aligned}                                               \tag{9}
\]
The sign in (9) is cancelled by the minus sign with which the odd
Kraus family enters \({\cal L}\).  Summing (9), including the singular
values, gives
\[
 Q_3(C)=\sum_R\langle Z_R,Z_R^{\mathsf T}\rangle_{\rm HS}. \tag{10}
\]
The symmetric and skew-symmetric parts of a complex matrix are
Hilbert--Schmidt orthogonal, proving (8).
\(\square\)

Since a \(2\times2\) skew matrix is one-dimensional, (8) is equivalently
the single weighted exterior domination
\[
\begin{aligned}
 \frac{s_1s_2}{2}\sum_R
 |u_1^{\mathsf T}Rv_2-u_2^{\mathsf T}Rv_1|^2
 \ \leq\ \sum_R\bigg[
 &s_1^2|u_1^{\mathsf T}Rv_1|^2
 +s_2^2|u_2^{\mathsf T}Rv_2|^2\\
 &+\frac{s_1s_2}{2}
 |u_1^{\mathsf T}Rv_2+u_2^{\mathsf T}Rv_1|^2
 \bigg].                                                   \tag{11}
\end{aligned}
\]
Thus every negative direction is carried by the common logical
bivector.  Bounding the summands in (11) separately is invalid; the
same physical Fierz frame occurs on both sides.

### 1.2 The unshifted compound and its two-term exterior split

There is a complementary exterior formula which targets mere
nonnegativity rather than the sharp shifted bound.  Let
\[
 {\cal T}=L_1\otimes L_2\otimes L_3,\qquad
 E_r=|u_r\rangle\langle v_r|,\qquad
 H_{rs}=\langle E_r,{\cal T}(E_s)\rangle_{\rm HS}.         \tag{11a}
\]
The two rank-one matrices \(E_1,E_2\) are Hilbert--Schmidt orthonormal.
With the normalized exterior product,
\[
\boxed{\qquad
 \det H
 =
 \left\langle E_1\wedge E_2,
 (\wedge^2{\cal T})(E_1\wedge E_2)\right\rangle.
\qquad}                                                     \tag{11b}
\]
This follows by expanding
\((E_1\otimes E_2-E_2\otimes E_1)/\sqrt2\); the four terms are
\(H_{11}H_{22},H_{12}H_{21},H_{21}H_{12},H_{22}H_{11}\).
Since the diagonal entries of \(H\) are positive rank-one endpoint
energies, \(\det H\geq0\) is exactly the unshifted \(2\times2\) minor
needed for \(Q_3(C)\geq0\) at every singular-value ratio and phase.

Regroup the two left and two right physical replicas.  If
\[
\begin{aligned}
 u_\wedge&=\frac{u_1\otimes u_2-u_2\otimes u_1}{\sqrt2},&
 u_\odot&=\frac{u_1\otimes u_2+u_2\otimes u_1}{\sqrt2},\\
 v_\wedge&=\frac{v_1\otimes v_2-v_2\otimes v_1}{\sqrt2},&
 v_\odot&=\frac{v_1\otimes v_2+v_2\otimes v_1}{\sqrt2},
\end{aligned}                                               \tag{11c}
\]
then the canonical identity
\[
\boxed{\qquad
 E_1\wedge E_2
 =
 \frac1{\sqrt2}\left(
 u_\wedge\otimes\overline v_\odot
 +u_\odot\otimes\overline v_\wedge
 \right)
\qquad}                                                     \tag{11d}
\]
splits the logical bivector into two orthogonal equal-norm terms.
This is
\[
 \wedge^2(U\otimes\overline V)
 \cong
 (\wedge^2U\otimes\operatorname{Sym}^2\overline V)
 \oplus
 (\operatorname{Sym}^2U\otimes\wedge^2\overline V)
                                                               \tag{11e}
\]
specialized to the common two-frame.

There is also a completely diagonal version of (11b).  Choose an
orthonormal product eigenbasis \(f_\alpha\) of \({\cal T}\), with
eigenvalues \(\lambda_\alpha\), and write
\[
 E_1=\sum_\alpha x_\alpha f_\alpha,\qquad
 E_2=\sum_\alpha y_\alpha f_\alpha.
\]
Then
\[
\boxed{\qquad
 \det H
 =
 \sum_{\alpha<\beta}
 \lambda_\alpha\lambda_\beta
 |x_\alpha y_\beta-x_\beta y_\alpha|^2.
\qquad}                                                     \tag{11f}
\]
For \(L_i(X)=X-\tfrac12\operatorname{Tr}(X)I\), its local identity
direction has eigenvalue \(1-d_i/2\), while every traceless direction
has eigenvalue \(1\).  Hence (11f) is not a sum of positive terms once
\(d_i\geq3\): the negative summands are exactly the Plücker minors
joining opposite identity parities.  A successful proof must use the
rank-one origin of both \(E_r\) to recouple those minors.  The two
equal-norm pieces in (11d) identify the smallest invariant block on
which such an \(S_4\)/Fierz recoupling can act.

## 2. An exact Pauli--exterior reduction

Let
\[
 {\cal A},{\cal B}\in K\otimes H_1\otimes H_2\otimes H_3,
 \qquad K\simeq\mathbb C^2,
                                                               \tag{12}
\]
have the same, possibly unnormalized, \(K\)-marginal
\[
 R=\rho_K^{\cal A}=\rho_K^{\cal B}.
                                                               \tag{13}
\]
Put \(T=\operatorname{Tr}R=\|{\cal A}\|^2=\|{\cal B}\|^2\),
\(p=\operatorname{Tr}R^2\), and
\[
 q_S=\operatorname{Tr}(\rho_{\cal A}^S\rho_{\cal B}^S).
                                                               \tag{14}
\]
The live anchored defect is
\[
 D({\cal A},{\cal B})
 =
 3q_K-2\sum_iq_{Ki}+\sum_{i<j}q_{Kij}
 +\frac{T^2-|\langle{\cal A},{\cal B}\rangle|^2}{2}.
                                                               \tag{15}
\]

This is exactly the sharp singular-value defect, with no hidden
normalization.  Indeed, if
\[
 C=\operatorname{Tr}_K|{\cal A}\rangle\langle{\cal B}|
 =\sum_{r=1}^2s_r|u_r\rangle\langle v_r|
                                                               \tag{15a}
\]
is the matched singular-value purification, then
\[
 \|\operatorname{Tr}_S C\|_2^2=q_{K\cup S}.
                                                               \tag{15b}
\]
Moreover
\[
 p=q_K=s_1^2+s_2^2,\qquad T=s_1+s_2.
                                                               \tag{15c}
\]
Consequently
\[
\boxed{\qquad
 2D({\cal A},{\cal B})
 =8Q_3(C)-(s_1-s_2)^2,
\qquad
 D=4\left[Q_3(C)-\frac18(s_1-s_2)^2\right].
\qquad}                                                       \tag{15d}
\]
Thus \(D\geq0\) is equivalent to the sharp conjectured three-copy
bound, not merely to its equal-singular-value specialization.

Expand the two rank-one projectors in a Pauli basis on \(K\):
\[
\begin{aligned}
 |{\cal A}\rangle\langle{\cal A}|
 &=\frac12\sum_{a=0}^3\sigma_a\otimes X_a^{\cal A},\\
 |{\cal B}\rangle\langle{\cal B}|
 &=\frac12\sum_{a=0}^3\sigma_a\otimes X_a^{\cal B},
\end{aligned}                                                \tag{16}
\]
and put
\[
 X_{a,i}^{\cal A}=\operatorname{Tr}_{\{1,2,3\}\setminus\{i\}}
 X_a^{\cal A},\qquad
 {\bf x}_{\cal A}=\bigoplus_{\substack{1\leq i\leq3\\1\leq a\leq3}}
 X_{a,i}^{\cal A},                                         \tag{17}
\]
with the analogous definitions for \({\cal B}\).  The direct sum has
the real Hilbert--Schmidt inner product; all its entries are Hermitian.
Define
\[
 \delta_{\cal A}=3p-\|{\bf x}_{\cal A}\|^2,\qquad
 \delta_{\cal B}=3p-\|{\bf x}_{\cal B}\|^2.                 \tag{18}
\]
The adaptive-sign-frame theorem proves
\[
 \delta_{\cal A},\delta_{\cal B}\geq0.                      \tag{19}
\]
These are exactly the diagonal strong-positive-rank-two defects in the
normalization used here.

Let
\[
 z={\cal A}\otimes{\cal B},\qquad
 F=F_KF_1F_2F_3,\qquad
 \omega=\frac{I-F}{2}z.                                   \tag{20}
\]

### Proposition 2.1

The anchored defect has the exact coupled decomposition
\[
 \boxed{\qquad
 D({\cal A},{\cal B})
 =
 \frac12\left(
 \delta_{\cal A}+\delta_{\cal B}
 +\|{\bf x}_{\cal A}-{\bf x}_{\cal B}\|^2
 \right)
 +\left\langle\omega,
 \left(I-2\sum_{i=1}^3F_i\right)\omega
 \right\rangle .
 \qquad}                                                    \tag{21}
\]

#### Proof

Introduce the complementary expression
\[
 D_0=3q_K-2\sum_iq_{Ki}+\sum_iq_i.                         \tag{22}
\]
Pauli orthogonality and (13) give
\[
\begin{aligned}
 q_K&=p,\\
 q_{Ki}&=\frac12\sum_{a=0}^3
 \langle X_{a,i}^{\cal A},X_{a,i}^{\cal B}\rangle_{\rm HS},\\
 q_i&=\langle X_{0,i}^{\cal A},X_{0,i}^{\cal B}\rangle_{\rm HS}.
\end{aligned}                                               \tag{23}
\]
The \(a=0\) terms cancel, so
\[
 D_0=3p-\langle{\bf x}_{\cal A},{\bf x}_{\cal B}\rangle
 =\frac12\left(
 \delta_{\cal A}+\delta_{\cal B}
 +\|{\bf x}_{\cal A}-{\bf x}_{\cal B}\|^2\right).          \tag{24}
\]

For \(\{i,j,k\}=\{1,2,3\}\), use
\(F_{Kij}=FF_k\).  Since \(F\) commutes with \(F_k\),
\[
 q_{Kij}-q_k
 =\langle z,(F-I)F_kz\rangle
 =-2\langle\omega,F_k\omega\rangle.                        \tag{25}
\]
Also
\[
 \|\omega\|^2
 =\frac{T^2-|\langle{\cal A},{\cal B}\rangle|^2}{2}.       \tag{26}
\]
Adding (25)--(26) to (24) proves (21).
\(\square\)

On the global-antisymmetric space containing \(\omega\), let \(r\) be
the number of physically antisymmetric replica pairs.  Then
\[
 I-2(F_1+F_2+F_3)
\quad\hbox{has eigenvalue}\quad
 4r-5,
                                                               \tag{27}
\]
namely
\[
\begin{array}{c|rrrr}
r&0&1&2&3\\ \hline
4r-5&-5&-1&3&7.
\end{array}                                                  \tag{28}
\]
Precisely, put
\[
 \Pi_r^{\rm phys}
 =\sum_{\substack{R\subseteq\{1,2,3\}\\|R|=r}}
 \prod_{i\in R}\frac{I-F_i}{2}
 \prod_{i\notin R}\frac{I+F_i}{2},
 \qquad
 \omega_r=\Pi_r^{\rm phys}\omega.                           \tag{28a}
\]
The four vectors \(\omega_r\) are mutually orthogonal.  Since
\(\omega\) is globally antisymmetric, its auxiliary parity is forced to
be opposite to the parity of \(r\).  Equation (27) therefore gives
\[
 \left\langle\omega,(I-2\sum_iF_i)\omega\right\rangle
 =-5\|\omega_0\|^2-\|\omega_1\|^2
  +3\|\omega_2\|^2+7\|\omega_3\|^2.                        \tag{28b}
\]
Thus unrestricted three-copy positivity is reduced to the single
exterior inequality
\[
\boxed{\quad
 5\|\omega_0\|^2+\|\omega_1\|^2
 \leq
 3\|\omega_2\|^2+7\|\omega_3\|^2
 +\frac12\left(
 \delta_{\cal A}+\delta_{\cal B}
 +\|{\bf x}_{\cal A}-{\bf x}_{\cal B}\|^2
 \right).
\quad}                                                       \tag{29}
\]
This is strictly smaller than the original anchor formula in the
following sense: every term outside the four exterior components is
already nonnegative by the proved adaptive-frame theorem.  The remaining
unknown is one explicit domination of the low-parity part of a single
decomposable bivector by those established diagonal slacks.

### 2.1 The six strengthened per-permutation gaps

The nonnegative Pauli term in (21) has a finer decomposition which is a
useful target for a future Koszul contraction.  For
\(\pi\in S_3\), define
\[
\begin{aligned}
 \delta_\pi({\cal A})
 &=p-\sum_{i=1}^3
   \|X_{\pi(i),i}^{\cal A}\|_2^2,\\
 d_\pi({\cal A},{\cal B})
 &=p-\sum_{i=1}^3
   \langle X_{\pi(i),i}^{\cal A},
           X_{\pi(i),i}^{\cal B}\rangle_{\rm HS}.
\end{aligned}                                               \tag{29a}
\]
The per-permutation part of the adaptive-frame proof gives
\[
 \delta_\pi({\cal A}),\delta_\pi({\cal B})\geq0             \tag{29b}
\]
and polarization gives the exact bilinear gap
\[
 \boxed{\qquad
 d_\pi({\cal A},{\cal B})
 =\frac12\left[
 \delta_\pi({\cal A})+\delta_\pi({\cal B})
 +\sum_i
 \|X_{\pi(i),i}^{\cal A}-X_{\pi(i),i}^{\cal B}\|_2^2
 \right]\geq0.
 \qquad}                                                    \tag{29c}
\]
Every ordered pair \((a,i)\) occurs in exactly two permutations, so
\[
 \sum_{\pi\in S_3}\delta_\pi({\cal A})=2\delta_{\cal A},
 \qquad
 \sum_{\pi\in S_3}d_\pi({\cal A},{\cal B})=2D_0.           \tag{29d}
\]

There is also an explicit trace-norm slack inside each
\(\delta_\pi\).  Put
\[
\begin{aligned}
 \alpha_\pi({\cal A})
 &=T^2-\sum_i\|X_{\pi(i),i}^{\cal A}\|_1^2,\\
 \beta_{\pi,i}({\cal A})
 &=\|X_{\pi(i),i}^{\cal A}\|_1^2
   +r_{\pi(i)}^2
   -2\|X_{\pi(i),i}^{\cal A}\|_2^2,
\end{aligned}                                               \tag{29e}
\]
where \(r_a=\operatorname{Tr}X_a^{\cal A}
=\operatorname{Tr}X_a^{\cal B}\).  Anticommuting trace-norm dual
observables give \(\alpha_\pi\geq0\), while the elementary
nontraceless trace-norm inequality gives every \(\beta_{\pi,i}\geq0\).
They satisfy
\[
 2\delta_\pi({\cal A})
 =\alpha_\pi({\cal A})+\sum_i\beta_{\pi,i}({\cal A}).      \tag{29f}
\]
Thus (29c) is a completely explicit sum of the two diagonal
trace-norm gaps and a squared transition-Pauli difference.

In this notation the precise next lemma is
\[
 -\left\langle\omega,(I-2\sum_iF_i)\omega\right\rangle
 \leq\frac12\sum_{\pi\in S_3}d_\pi({\cal A},{\cal B}).
                                                               \tag{29g}
\]
Unlike a sectorwise comparison, (29g) leaves six distinct adaptive
frames available to absorb the two low-parity exterior components.

### 2.2 Transition-Pauli form of the exterior correction

There is a second exact form which may be useful for constructing that
absorption.  Expand the cross operator as
\[
 |{\cal A}\rangle\langle{\cal B}|
 =\frac12\sum_{a=0}^3\sigma_a\otimes Z_a.                 \tag{29h}
\]
The pure-state crossing identity
\[
 \left\|\operatorname{Tr}_S
 |{\cal A}\rangle\langle{\cal B}|\right\|_2^2=q_S          \tag{29i}
\]
and Pauli orthogonality give
\[
\begin{aligned}
 q_{Kij}&=\|\operatorname{Tr}_{ij}Z_0\|_2^2,\\
 q_i&=\frac12\sum_{a=0}^3\|\operatorname{Tr}_iZ_a\|_2^2,\\
 T^2&=\frac12\sum_{a=0}^3\|Z_a\|_2^2,\\
 q_{K123}&=|\operatorname{Tr}Z_0|^2.
\end{aligned}                                               \tag{29j}
\]
Consequently the exterior term in (21) is also
\[
\boxed{\begin{aligned}
 \left\langle\omega,(I-2\sum_iF_i)\omega\right\rangle
={}&
 \sum_{i<j}\|\operatorname{Tr}_{ij}Z_0\|_2^2
 -\frac12\sum_{i=1}^3\sum_{a=0}^3
   \|\operatorname{Tr}_iZ_a\|_2^2\\
 &+\frac14\sum_{a=0}^3\|Z_a\|_2^2
 -\frac12|\operatorname{Tr}Z_0|^2 .
\end{aligned}}                                               \tag{29k}
\]
Thus the missing map in (29g) can equivalently be sought as a Bessel
contraction from the twelve two-party transition-Pauli reductions
\(\operatorname{Tr}_iZ_a\) into the six diagonal adaptive frames and
the positive one-party/global terms in (29k).  This formulation retains
the common origin of all transition operators in the single rank-two
cross operator (29h).

### 2.3 Exact phase polarization and its obstruction

The already-proved diagonal theorem can be polarized without losing any
sector information.  Put
\[
 G=F_K\prod_{i=1}^3(2I-F_i)-2F_K+I,\qquad
 F_{\rm all}=F_KF_1F_2F_3,\qquad
 P_\pm=\frac{I\pm F_{\rm all}}2.                         \tag{29l}
\]
For one vector \({\cal W}\), define
\[
 f({\cal W})=
 \langle{\cal W}\otimes{\cal W},
 G({\cal W}\otimes{\cal W})\rangle.
                                                               \tag{29m}
\]
The strong positive-rank-two theorem is precisely
\[
 f({\cal W})=2\delta_{\cal W}\geq0.                       \tag{29n}
\]
For \(z={\cal A}\otimes{\cal B}\), define
\[
 D_{\rm even}=\frac12\langle z,GP_+z\rangle,\qquad
 D_{\rm odd}=\frac12\langle z,GP_-z\rangle.               \tag{29o}
\]
These are exactly the even- and odd-total-parity brackets, and
\(D=D_{\rm even}+D_{\rm odd}\).

Expanding
\[
 ({\cal A}+e^{i\theta}{\cal B})^{\otimes2}
 =
 {\cal A}^{\otimes2}
 +e^{i\theta}(z+F_{\rm all}z)
 +e^{2i\theta}{\cal B}^{\otimes2}
                                                               \tag{29p}
\]
and averaging the four phases \(1,i,-1,-i\) gives the exact identity
\[
\boxed{\qquad
 \frac14\sum_{\theta\in\{0,\pi/2,\pi,3\pi/2\}}
 f({\cal A}+e^{i\theta}{\cal B})
 =
 2(\delta_{\cal A}+\delta_{\cal B})+8D_{\rm even}.
\qquad}                                                     \tag{29q}
\]
Indeed, the phase average deletes the degree-two cross terms and the
surviving degree-one vector is \(2P_+z\).  Thus diagonal phase
superpositions see the global-symmetric part of the crossed defect
exactly and cannot see \(P_-z={\cal A}\wedge{\cal B}\).

The immediate lower bound
\[
 D_{\rm even}\geq-\frac14(\delta_{\cal A}+\delta_{\cal B})
                                                               \tag{29r}
\]
suggests trying
\[
 D_{\rm even}<0
 \quad\Longrightarrow\quad
 D_{\rm odd}\geq\frac14(\delta_{\cal A}+\delta_{\cal B}).
                                                               \tag{29s}
\]
This conditional strengthening is false by an exact rational
perturbation of the spin-flip boundary.  Use unnormalized vectors on
four qubits.  With the party order \(K,1,2,3\), put
\[
\begin{aligned}
 {\cal A}={}&
 \frac35(|0000\rangle+|0011\rangle)
 +\frac45(|0001\rangle+|0010\rangle)\\
 &+|1100\rangle-|1111\rangle,\\
 {\cal B}={}&
 -|0000\rangle+|0011\rangle+|1100\rangle+|1111\rangle.
\end{aligned}                                               \tag{29t}
\]
Both \(K\)-marginals are \(2I_2\).  Exact contraction gives
\[
\begin{aligned}
 \delta_{\cal A}&=\frac{7696}{625},&
 \delta_{\cal B}&=16,\\
 D_{\rm odd}&=\frac{176}{25},&
 D_{\rm even}&=-\frac{96}{25},&
 D&=\frac{16}{5}>0.
\end{aligned}                                               \tag{29u}
\]
Consequently
\[
 D_{\rm odd}
 -\frac14(\delta_{\cal A}+\delta_{\cal B})
 =-\frac{24}{625}<0.                                      \tag{29v}
\]
Thus even after excluding \(D_{\rm even}\geq0\), the phase lower bound
cannot be closed by an independent odd-parity margin.  The true positive
quantity in this example uses more of the actual phase average than its
zero lower bound.

### 2.4 The five-gamma flag frame and the product-sign obstruction

Introduce a branch qubit \(L\) and
\[
 |{\cal W}\rangle
 =\frac{|0\rangle_L{\cal A}+|1\rangle_L{\cal B}}{\sqrt2}.
                                                               \tag{29w}
\]
On \(L\otimes K\), the five Hermitian unitaries
\[
\Gamma_0=X_L\otimes I_K,\qquad
\Gamma_4=Y_L\otimes I_K,\qquad
\Gamma_a=Z_L\otimes\sigma_a\quad(1\leq a\leq3)             \tag{29x}
\]
are pairwise anticommuting.  Let \(G_0,G_4,G_1,G_2,G_3\) be
pairwise commuting Hermitian contractions on the physical system.
Then the five operators \(\Gamma_\mu\otimes G_\mu\) are pairwise
anticommuting Hermitian contractions.  Lemma 2 of
`agent_qutrit_frame.md` therefore gives the exact simultaneous estimate
\[
\boxed{\begin{aligned}
 &\left(\operatorname{Re}\operatorname{Tr}Z_0G_0\right)^2
 +\left(\operatorname{Im}\operatorname{Tr}Z_0G_4\right)^2\\
 &\qquad
 +\frac14\sum_{a=1}^3
 \left(
 \operatorname{Tr}
 [(X_a^{\cal A}-X_a^{\cal B})G_a]
 \right)^2
 \leq T^2 .
\end{aligned}}                                              \tag{29y}
\]
Here the factor \(1/2\) in the last three expectations comes from the
balanced branch flag.  Taking \(G_0=G_4\) combines the first line into
\[
 |\operatorname{Tr}Z_0G_0|^2.                             \tag{29z}
\]

For a permutation \(\pi\), choose
\[
 G_{\pi(i)}=\operatorname{sgn}
 (X_{\pi(i),i}^{\cal A}-X_{\pi(i),i}^{\cal B})
                                                               \tag{29aa}
\]
on site \(i\), and choose \(G_0=G_4\) in the commutant of these three
local signs.  This is the strongest direct adaptive consequence:
\[
\boxed{\quad
 \sup_{\substack{G=G^\dagger,\ \|G\|\leq1\\
 [G,G_{\pi(i)}]=0\ (i=1,2,3)}}
 |\operatorname{Tr}Z_0G|^2
 +\frac14\sum_i
 \|X_{\pi(i),i}^{\cal A}-X_{\pi(i),i}^{\cal B}\|_1^2
 \leq T^2.
\quad}                                                      \tag{29ab}
\]
In particular one may use the product sign
\(G=\bigotimes_iG_{\pi(i)}\).  The restriction to the common commutant
is essential: the polar optimizer of a two-site transition reduction
need not commute with either overlapping local sign.

There is an exact two-Bell-state obstruction to dropping that
restriction.  Put
\[
 {\cal A}=|\Phi^+\rangle_{K1}|00\rangle_{23},\qquad
 {\cal B}=|\Phi^-\rangle_{K1}|00\rangle_{23},              \tag{29ac}
\]
using the unnormalized Bell vectors.  Their \(K\)-marginals are both
\(I_2\), and \(T=2\).  Take the transition observable \(Z_1\) and the
diagonal observable \(X_1\).  Since
\[
 {\cal B}=Z_1{\cal A},\qquad
 X_KX_1{\cal A}={\cal A},\qquad
 X_KX_1{\cal B}=-{\cal B},                                \tag{29ad}
\]
the two flag-Clifford expectations are both \(2\).  Their squared sum
is \(8\), whereas \(T^2=4\).  There is no contradiction with (29y):
\(Z_1\) and \(X_1\) anticommute, so the two total observables commute
rather than anticommute.  This exact factor-two failure explains why
the five-gamma frame does not by itself control the twelve
overlapping transition reductions in (29k).

## 3. Universal inversion and the Koszul/Bessel target

For a party \(j\), define the local trace-replacement and reduction maps
\[
 E_j(X)=\operatorname{Tr}_j(X)\otimes I_j,\qquad
 R_j=E_j-\operatorname{id}.                                \tag{30}
\]
For a nonempty subset \(T\subseteq\{K,1,2,3\}\), define
\[
 M_T(P)=R_T E_{T^c}(P),\qquad
 R_T=\prod_{j\in T}R_j,\quad E_{T^c}=\prod_{j\notin T}E_j.
                                                               \tag{31}
\]

### Lemma 3.1

For every \(P\succeq0\),
\[
 \boxed{\qquad M_T(P)\succeq0.\qquad}                      \tag{32}
\]

#### Proof

Put \(\rho_T=\operatorname{Tr}_{T^c}P\).  Then
\[
 E_{T^c}(P)=\rho_T\otimes I_{T^c}.                         \tag{33}
\]
For a \(d\)-dimensional local factor, set
\[
 A_{ab}=|a\rangle\langle b|-|b\rangle\langle a|,
 \qquad a<b.
                                                               \tag{34}
\]
A direct matrix-unit contraction gives
\[
 R_j(X)=\sum_{a<b}A_{ab}X^{\mathsf T_j}A_{ab}^\dagger.    \tag{35}
\]
Therefore
\[
 R_T(\rho_T)=
 \sum_{\boldsymbol a}
 A_{\boldsymbol a}\rho_T^{\mathsf T_T}
 A_{\boldsymbol a}^\dagger.                               \tag{36}
\]
Here \(\mathsf T_T\) is the full transpose on every tensor factor on
which \(\rho_T\) lives, not a partial transpose relative to an untransposed
factor.  Hence \(\rho_T^{\mathsf T_T}\succeq0\), and every summand in
(36) is positive.  Tensoring with \(I_{T^c}\) proves (32).
\(\square\)

There are two different reduction maps which must not be confused.
Let
\[
 R_{\rm glob}(X)=\operatorname{Tr}(X)I-X
                                                               \tag{37}
\]
be reduction on the whole four-party space.  For a rank-one
\(P=|{\cal A}\rangle\langle{\cal A}|\), direct expansion of the anchored
operator gives
\[
 M_{\cal A}
 =\frac12R_{\rm glob}(P)
 +\sum_{i<j}R_iR_j(P)+3R_1R_2R_3(P).                     \tag{38}
\]
Since
\[
 R_{\rm glob}
 =E_KE_1E_2E_3-\operatorname{id}
 =\prod_{j\in\{K,1,2,3\}}(I+R_j)-I,
                                                               \tag{39}
\]
Möbius expansion gives the exact universal-inversion identity
\[
 \boxed{\qquad
 2M_{\cal A}
 =
 M_{\{K\}}(P)
 +\sum_{\varnothing\ne S\subseteq\{1,2,3\}}
 \left(M_S(P)-M_{\{K\}\cup S}(P)\right).
 \qquad}                                                    \tag{40}
\]
Indeed, a physical monomial \(R_U\) occurs \(2^{|U|}-1\) times on the
right of (40), while a monomial containing \(R_K\) occurs once.  These
are exactly the coefficients obtained from (38)--(39).

For a second vector \({\cal B}\), the positive operators in (40) have
the exterior-frame evaluation
\[
 \boxed{\qquad
 \langle{\cal B},M_T(P){\cal B}\rangle
 =
 2^{|T|}
 \left\|
 \prod_{j\in T}\frac{I-F_j}{2}
 ({\cal A}\otimes{\cal B})
 \right\|^2.
 \qquad}                                                    \tag{41}
\]
To see this, the replica operator representing \(E_j\) is
\(F_{\rm all}F_j\), while that representing \(R_j\) is
\(F_{\rm all}(F_j-I)\).  Multiplication over all four parties cancels
the global swaps and leaves \(\prod_{j\in T}(I-F_j)\), proving (41).

Consequently the whole remaining theorem is the following one-line
operator Bessel inequality:
\[
\boxed{\qquad
 \sum_{\varnothing\ne S\subseteq\{1,2,3\}}M_{\{K\}\cup S}(P)
 \ \preceq\
 M_{\{K\}}(P)
 +\sum_{\varnothing\ne S\subseteq\{1,2,3\}}M_S(P),
 \qquad \operatorname{rank}P=1,\ \dim K=2.
 \qquad}                                                    \tag{42}
\]
Each term in (42) is already a positive exterior-frame Gram operator by
Lemma 3.1.  The unresolved issue is to construct one common contraction
from the seven \(K\cup S\) frames into the \(K\) frame plus the seven
\(S\) frames.  It cannot be done sector by sector: the exact transverse
boundary in `agent_n3_transverse_anchor_boundary.md` requires cancellation
between different parity levels.

### 3.1 The smaller 8-versus-8 cube for mere nonnegativity

If one targets \(Q_3(C)\geq0\), rather than the sharp
\((s_1-s_2)^2/8\) bound, the operator cube becomes more symmetric.
For a rank-one anchor \(P=|{\cal A}\rangle\langle{\cal A}|\), put
\[
 M_Q(P)=\prod_{i=1}^3(2E_i-I)(P).                         \tag{42a}
\]
For arbitrary vectors
\[
 {\cal A}=\sum_{r=0}^1|r\rangle_K\otimes a_r,\qquad
 {\cal B}=\sum_{r=0}^1|r\rangle_K\otimes b_r,
\]
put
\[
 C=\operatorname{Tr}_K|{\cal A}\rangle\langle{\cal B}|
   =\sum_{r=0}^1|a_r\rangle\langle b_r|.
\]
Then \(\operatorname{rank}C\leq2\), with no condition on the two
\(K\)-marginals, and
\[
 \boxed{\qquad
 \langle{\cal B},M_Q(P){\cal B}\rangle=8Q_3(C).
 \qquad}                                                   \tag{42b}
\]
Indeed, expanding (42a) gives the coefficients
\[
 8q_K-4\sum_iq_{Ki}+2\sum_{i<j}q_{Kij}-q_{K123}.
                                                               \tag{42c}
\]
Here the crossing identity
\[
 q_{K\cup S}
 =\left\|\operatorname{Tr}_S C\right\|_2^2
\]
holds for arbitrary \({\cal A},{\cal B}\).  Conversely, every matrix of
rank at most two has a two-dyad decomposition of the displayed form.
Consequently \(Q_3(C)\geq0\) for every rank-at-most-two \(C\) is
equivalent, in both directions, to
\[
 M_Q(|{\cal A}\rangle\langle{\cal A}|)\succeq0
 \quad\hbox{for every }{\cal A}\in K\otimes H_1\otimes H_2\otimes H_3.
\]
The equal-\(K\)-marginal SVD normalization used in Section 2 is needed
only for the sharp shifted bound, not for this unshifted operator cube.

Allow \(M_\varnothing(P)=E_{K123}(P)=T I\).  Since
\(E_K=I+R_K\), direct factorization of the Boolean cube gives
\[
\boxed{\qquad
 M_Q(P)
 =
 \sum_{S\subseteq\{1,2,3\}}M_S(P)
 -
 \sum_{S\subseteq\{1,2,3\}}M_{\{K\}\cup S}(P).
\qquad}                                                     \tag{42d}
\]
For example,
\[
\begin{aligned}
 \sum_S(M_S-M_{KS})
 &=\sum_SR_SE_{\bar S}(E_K-R_K)P\\
 &=\sum_SR_SE_{\bar S}P
 =\prod_i(E_i+R_i)P
 =\prod_i(2E_i-I)P.
\end{aligned}                                               \tag{42e}
\]
Thus mere three-copy positivity is exactly the equal-cardinality
Koszul-frame domination
\[
\boxed{\qquad
 \sum_{S\subseteq[3]}M_{KS}(P)
 \preceq
 \sum_{S\subseteq[3]}M_S(P).
\qquad}                                                     \tag{42f}
\]

In exterior notation, define the two analysis operators
\[
\begin{aligned}
 {\mathfrak A}_{\cal A}{\cal B}
 &=
 \bigoplus_{S\subseteq[3]}
 2^{|S|/2}\prod_{i\in S}\frac{I-F_i}{2}
 ({\cal A}\otimes{\cal B}),\\
 {\mathfrak B}_{\cal A}{\cal B}
 &=
 \bigoplus_{S\subseteq[3]}
 2^{(|S|+1)/2}\frac{I-F_K}{2}
 \prod_{i\in S}\frac{I-F_i}{2}
 ({\cal A}\otimes{\cal B}).
\end{aligned}                                               \tag{42g}
\]
Equation (42f) is
\[
 {\mathfrak B}_{\cal A}^\dagger{\mathfrak B}_{\cal A}
 \preceq
 {\mathfrak A}_{\cal A}^\dagger{\mathfrak A}_{\cal A}.
                                                               \tag{42h}
\]
Equivalently, on the range of \({\mathfrak A}_{\cal A}\), the rule
\[
 {\mathfrak A}_{\cal A}{\cal B}
 \longmapsto
 {\mathfrak B}_{\cal A}{\cal B}                            \tag{42i}
\]
must be well-defined and contractive.  This is the precise
state-dependent Koszul incidence map still missing.

A contraction diagonal in the subset label \(S\) is rigorously
impossible.  At the normalized spin-flip boundary, the scalar frame
masses
\[
 m_T=\langle{\cal B},M_T(P){\cal B}\rangle
\]
obey
\[
\begin{array}{c|rrrrrrrr}
S&\varnothing&1&2&12&3&13&23&123\\ \hline
m_S&1&1/2&1/2&1/4&1/2&1/4&1/2&1/2\\
m_{KS}&1/2&1/2&1/4&1/2&1/4&1/2&1/2&1 .
\end{array}                                                \tag{42j}
\]
The two rows have the same sum, but \(m_{K123}=2m_{123}\).
At the nilpotent boundary (46),
\[
\begin{array}{c|rrrr}
S&\varnothing&1&2&12\\ \hline
m_S&4&2&4&2\\
m_{KS}&2&4&2&4 ,
\end{array}                                                \tag{42k}
\]
with all entries containing site \(3\) equal to zero.  Again the row
sums agree, while the inequalities at \(S=1,12\) fail by a factor two.
Therefore any valid contraction in (42i) must transfer norm between
different vertices of the subset cube.  A fixed same-\(S\) routing,
even one allowed to depend on the anchor inside each diagonal block,
cannot prove the theorem.

The two equality mechanisms indicate two different exact cube
automorphisms.  At the spin-flip boundary,
\[
 m_{KS}=m_{S^c}\qquad(S\subseteq[3]),                     \tag{42l}
\]
so its scalar routing is complementation of all three bits.  On the
nonzero face of the nilpotent boundary,
\[
 m_{KS}=m_{S\mathbin{\triangle}\{1\}},                    \tag{42m}
\]
so its routing is translation by a single bit.  A common proof therefore
cannot hard-code either boundary permutation.  It needs a
state-dependent Hodge/Koszul map which can interpolate between distinct
affine automorphisms of the cube while controlling the actual frame
vectors, not only their eight squared norms.

### 3.2 The odd-exterior anchor is not positive

The phase split in Section 2.3 exposes a simpler-looking intermediate
operator.  Let \(M_{\rm odd}(P)\) be defined by
\[
 D_{\rm odd}({\cal A},{\cal B})
 =\langle{\cal B},M_{\rm odd}(P){\cal B}\rangle.           \tag{42n}
\]
Exact Möbius expansion gives
\[
\boxed{\qquad
 M_{\rm odd}(P)
 =
 \frac12R_{\rm glob}(P)
 +\frac12\left(
 3R_1R_2R_3
 -R_KR_1R_2-R_KR_1R_3-R_KR_2R_3
 \right)(P).
 \qquad}                                                     \tag{42o}
\]
Equivalently, in the monomial basis of the four commuting local
reductions \(R_j\), its coefficient is \(1/2\) on every singleton and
pair, \(2\) on the physical triple, zero on the three triples
containing \(K\), and \(1/2\) on the four-party monomial.

The tempting assertion \(M_{\rm odd}(P)\succeq0\) is false, already on
qutrit local spaces.  In the party order \(K,1,2,3\), take
\[
\begin{aligned}
 {\cal A}={}&-|0000\rangle+|0120\rangle-|0210\rangle
                 +|1120\rangle,\\
 {\cal B}={}& |1000\rangle-|1120\rangle+|1210\rangle .
\end{aligned}                                               \tag{42p}
\]
Both vectors are real and have support on a single basis vector of the
third physical party, so this is an exact example in
\(K\simeq\mathbb C^2\) and \(H_1=H_2=H_3=\mathbb C^3\).
Direct rational contraction gives
\[
\boxed{\qquad
 D_{\rm odd}({\cal A},{\cal B})=-\frac12.
\qquad}                                                     \tag{42q}
\]
Thus the standalone sector inequality suggested by the odd bracket,
\[
 p_{1,0}+p_{0,1}+13p_{0,3}\geq3p_{1,2},
                                                               \tag{42r}
\]
is an exact false intermediate claim.

This counterexample does **not** disprove three-copy positivity.  For
the same pair,
\[
 D_{\rm even}=8,\qquad D=\frac{15}{2},\qquad
 Q_3\!\left(\operatorname{Tr}_K
 |{\cal A}\rangle\langle{\cal B}|\right)=\frac98.          \tag{42s}
\]
More strongly, the full unshifted anchored operator \(M_Q(P_{\cal A})\)
is positive definite.  On the supported
\(K\otimes H_1\otimes H_2\) space it splits into six positive
\(2\times2\) blocks and one six-dimensional block.  Two of the pair
blocks are
\[
 \begin{pmatrix}8&4\\4&4\end{pmatrix},
\]
and four are
\[
 \begin{pmatrix}8&2\\2&2\end{pmatrix}.
\]
Eliminating two diagonal \(4\)-pivots from the remaining block leaves
\[
 \begin{pmatrix}
 5&-1&1&-1\\
 -1&9&-1&1\\
 1&-1&5&-1\\
 -1&1&-1&1
 \end{pmatrix}.                                            \tag{42t}
\]
The antisymmetric combination of its first and third coordinates has
eigenvalue \(4\).  On the complementary three-dimensional space,
Sylvester's minors are \(6,52,32\), so (42t), and hence the entire
anchor, is positive definite.  Restoring the third qutrit tensors this
operator with
\[
 2I_3-|0\rangle\langle0|\succ0,
\]
and therefore preserves strict positivity.

The obstruction is consequently precise: the odd and even brackets
must cancel.  Neither a universal positive odd anchor nor an independent
odd-parity Plücker contraction can prove (42f).  The state-dependent
eight-vertex Koszul map in (42i) remains the smaller viable target.

## 4. Boundary stress tests

For the fully transverse spin-flip boundary recorded in
`agent_n3_transverse_anchor_boundary.md`,
\[
 p=\frac12,\qquad
 \delta_{\cal A}=\delta_{\cal B}=1,\qquad
 {\bf x}_{\cal A}={\bf x}_{\cal B}.                       \tag{43}
\]
The exterior term in (21) is exactly \(-1\), so both sides cancel:
\[
 D=\frac12(1+1)-1=0.                                     \tag{44}
\]
Thus (21) retains the known qubit spin-flip kernel exactly.

The canonical nilpotent equality
\[
 C=P_2\otimes|0\rangle\langle1|
   \otimes|0\rangle\langle0|
                                                               \tag{45}
\]
has unnormalized matched purifications
\[
\begin{aligned}
 {\cal A}&=|0\rangle_K|000\rangle+|1\rangle_K|100\rangle,\\
 {\cal B}&=|0\rangle_K|010\rangle+|1\rangle_K|110\rangle.
\end{aligned}                                               \tag{46}
\]
Here
\[
 \delta_{\cal A}=\delta_{\cal B}=0,\qquad
 {\bf x}_{\cal A}={\bf x}_{\cal B},\qquad
 \langle\omega,(I-2\sum_iF_i)\omega\rangle=0.             \tag{47}
\]
Thus every term in (21) vanishes separately.  In particular, neither
the Pauli recoupling nor the universal-inversion recoupling creates a
fictitious strict gap at the sparse nilpotent zero.

The inertia-\((2,2)\) completion from
`agent_unrestricted_n3_selfadjoint.md` gives a complementary nonzero
stress test.  Put
\[
\begin{aligned}
 p_1&=|022\rangle,&p_2&=|101\rangle,\\
 n_1&=|120\rangle,&n_2&=|202\rangle,
\end{aligned}
                                                               \tag{48}
\]
and use the normalized matched purifications
\[
\begin{aligned}
 {\cal A}&=\frac12\sum_{r=1}^2|r\rangle_K(p_r+i n_r),\\
 {\cal B}&=\frac12\sum_{r=1}^2|r\rangle_K(p_r-i n_r).
\end{aligned}                                                \tag{49}
\]
They have \(R=I_2/2\) and represent one half of the square-zero
rank-two completion \(H+iB_I\).  Direct contraction of the four basis
strings gives
\[
\begin{aligned}
 q_K&=\frac12,&
 \sum_iq_{Ki}&=1,&
 \sum_{i<j}q_{Kij}&=\frac14,\\
 \sum_iq_i&=\frac54,&
 q_{K123}&=0.
\end{aligned}                                                \tag{50}
\]
Therefore
\[
 D_0=\frac34,\qquad
 \delta_{\cal A}=\delta_{\cal B}=\frac34,\qquad
 {\bf x}_{\cal A}={\bf x}_{\cal B},\qquad
 D-D_0=-\frac12,
                                                               \tag{51}
\]
and
\[
 D=\frac14,\qquad Q_3(C)=\frac1{16}.                       \tag{52}
\]
Rescaling \(C\) by two recovers the previously recorded
\(Q_3(H+iB_I)=1/4\).  Thus the recoupling does not merely recognize
zero manifolds: it also displays the exact \(3/4-1/2\) compensation
which repairs a genuinely negative Hermitian quadrature.

## Exact conclusion

What is proved here:

1. the ccp Fierz identity (8) and its one-dimensional exterior target
   (11);
2. the coupled Pauli--exterior formula (21);
3. the strict reduction to the explicit exterior lemma (29);
4. positivity and the antisymmetric-Kraus representation of every
   universal-inversion output \(M_T(P)\);
5. the operator identity (40) and the equivalent Koszul/Bessel target
   (42);
6. the phase-polarization identity (29q), together with the exact
   counterexample (29t)--(29v) to its tempting conditional completion;
7. the five-gamma flag inequality (29y)--(29ab) and the exact Bell-state
   obstruction to removing its commutation hypothesis;
8. the smaller 8-versus-8 cube (42d)--(42i) for mere nonnegativity and
   exact boundary obstructions to every same-subset contraction;
9. the exact qutrit counterexample (42p)--(42q) to positivity of the
   separated odd-exterior anchor, together with an exact positive
   certificate for the full \(M_Q(P_{\cal A})\);
10. exact compatibility with both transverse zero mechanisms.

What remains unproved is (29), equivalently (42).  A completion must use
the fact that all fifteen exterior frames in (42) come from the same
rank-one tensor \(P\); arbitrary positive operators with the same labels
do not satisfy the inequality.  For mere nonnegativity, the smaller
unproved target is (42f).  The exact counterexample (42p) shows that its
odd-total-parity half is not positive by itself, even though the full
operator is positive definite at that same anchor.
