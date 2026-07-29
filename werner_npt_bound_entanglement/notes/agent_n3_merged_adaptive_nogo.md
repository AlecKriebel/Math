# Three-copy merged adaptive frames: the exact weighted lemma and a common-origin no-go

## Status

**2026-07-29 05:30 PDT.**  Applying the positive rank-at-most-two
three-party theorem to
\[
 H_{x,y}=x|{\cal A}\rangle\langle{\cal A}|
        +y|{\cal B}\rangle\langle{\cal B}|
\]
under the three merged groupings
\[
 (K H_i)\mid H_j\mid H_k
\]
gives eighteen exact nonlinear Gram inequalities.  Their full
trace-norm refinements are recorded below for all \(x,y\geq0\).

These inequalities do **not**, even jointly, imply the missing exterior
inequality (29g) of `agent_n3_exterior_koszul_recoupling.md`.  Section 3
gives an exact rational formal marginal model which satisfies:

1. normalization, complementary self-purity identities, and all
   Hilbert--Schmidt Cauchy bounds;
2. nonnegative exact self and crossed swap-sector masses;
3. positive one-block density matrices for every adaptive frame used;
4. all six original adaptive-sign and trace-norm inequalities, at
   equality;
5. all eighteen merged inequalities, including their weighted
   trace-norm versions for every \(x,y\geq0\);

but has formal
\[
 D_0=0,\qquad E=-1,\qquad D=D_0+E=-1,
 \qquad Q_3^{\rm formal}=-\frac14.
\]

This is **not a physical rank-two matrix and not a Werner witness**.
It is an exact no-go for a proof using the separate adaptive inequalities
alone.

Section 4 identifies the first common-origin constraint which the model
violates.  Two of its saturated adaptive frames would force a common
state to be a \(+1\) eigenvector of two Hermitian unitaries \(M,N\), but
\[
 \|\{M,N\}\|=\frac{4\sqrt2}{3}<2.
\]
This gives an explicit joint-frame quadratic inequality separating the
formal model.  Thus the next live lemma must couple different adaptive
permutations; treating their trace-norm gaps independently necessarily
loses essential information.

The independent exact checker is
`verification/verify_n3_merged_adaptive_nogo.py`.

## 1. The exact weighted merged-frame lemma

Let
\[
 {\cal A},{\cal B}\in
 K\otimes H_1\otimes H_2\otimes H_3,
 \qquad
 \|{\cal A}\|^2=\|{\cal B}\|^2=T,
\]
and put \(h=\langle{\cal A},{\cal B}\rangle\).  Fix any partition of
the four parties into three blocks
\[
 {\cal R}=(R_1,R_2,R_3).
\]
For a block \(R\), define
\[
\begin{aligned}
 A_R&=\operatorname{Tr}_{R^c}|{\cal A}\rangle\langle{\cal A}|,\\
 B_R&=\operatorname{Tr}_{R^c}|{\cal B}\rangle\langle{\cal B}|,\\
 Z_R&=\operatorname{Tr}_{R^c}|{\cal A}\rangle\langle{\cal B}|,\\
 S_R&=Z_R+Z_R^\dagger,\qquad
 T_R=i(Z_R-Z_R^\dagger).
\end{aligned}                                                   \tag{1}
\]
Take \(x,y\geq0\) and purify the positive rank-at-most-two operator
\[
 H_{x,y}=x|{\cal A}\rangle\langle{\cal A}|
        +y|{\cal B}\rangle\langle{\cal B}|
\]
by the branch qubit \(L\):
\[
 |\Psi_{x,y}\rangle
 =\sqrt{x}|0\rangle_L{\cal A}
  +\sqrt{y}|1\rangle_L{\cal B}.                              \tag{2}
\]
The three branch-Pauli operators reduced to \(R\) are
\[
 \sqrt{xy}\,S_R,\qquad
 \sqrt{xy}\,T_R,\qquad
 xA_R-yB_R.                                                  \tag{3}
\]
The squared Hilbert--Schmidt norm of the branch marginal is
\[
 p_L(x,y)=T^2(x^2+y^2)+2xy|h|^2.                            \tag{4}
\]

Choose distinct blocks \(R_s,R_t,R_d\), assigning the branch \(X,Y,Z\)
axes to them in that order.  The per-permutation part of the strong
positive rank-two theorem gives
\[
\boxed{\begin{aligned}
 \delta_{s,t\mid d}(x,y)
 :={}&p_L(x,y)
 -xy\|S_{R_s}\|_2^2
 -xy\|T_{R_t}\|_2^2
 -\|xA_{R_d}-yB_{R_d}\|_2^2\\
 &\geq0 .
\end{aligned}}                                               \tag{5}
\]
This is the exact weighted Gram inequality, not a polarization
heuristic.

The adaptive trace-norm proof gives the stronger resolved identity
\[
 2\delta_{s,t\mid d}
 =\alpha_{s,t\mid d}+\beta_s+\beta_t+\beta_d,               \tag{6}
\]
where every term on the right is nonnegative and
\[
\begin{aligned}
 \alpha_{s,t\mid d}
={}&T^2(x+y)^2
 -xy\|S_{R_s}\|_1^2
 -xy\|T_{R_t}\|_1^2
 -\|xA_{R_d}-yB_{R_d}\|_1^2,\\
 \beta_s
={}&xy\|S_{R_s}\|_1^2
 +4xy(\operatorname{Re}h)^2
 -2xy\|S_{R_s}\|_2^2,\\
 \beta_t
={}&xy\|T_{R_t}\|_1^2
 +4xy(\operatorname{Im}h)^2
 -2xy\|T_{R_t}\|_2^2,\\
 \beta_d
={}&\|xA_{R_d}-yB_{R_d}\|_1^2
 +T^2(x-y)^2
 -2\|xA_{R_d}-yB_{R_d}\|_2^2.
\end{aligned}                                               \tag{7}
\]
Indeed, \(\alpha\geq0\) is the anticommuting-contraction estimate and
the three \(\beta\)'s are the nontraceless trace-norm inequalities.
Adding (7) cancels all trace norms and gives (6) directly.

Expanding the last Hilbert--Schmidt norm in (5) shows that (5) for all
\(x,y\geq0\) is equivalent to the sharp copositive \(2\times2\)
condition
\[
\boxed{\quad
 \frac{\|S_{R_s}\|_2^2+\|T_{R_t}\|_2^2}{2}
 \leq
 |h|^2+\operatorname{Tr}(A_{R_d}B_{R_d})
 +\sqrt{
  (T^2-\|A_{R_d}\|_2^2)
  (T^2-\|B_{R_d}\|_2^2)} .
\quad}                                                       \tag{8}
\]
For the program in question, use the three partitions
\[
 (K i)\mid j\mid k
\]
and all six assignments in each.  Equations (5)--(7), rather than only
their sums, are the strongest direct consequences of the established
adaptive proof.

## 2. A smaller exact form of the target

Assume now that the \(K\)-marginals of \({\cal A},{\cal B}\) coincide,
and use the notation
\[
 q_R=\operatorname{Tr}(A_RB_R),\qquad
 p=q_K,\qquad
 E=\sum_{i<j}q_{Kij}-\sum_iq_i+\frac{T^2-|h|^2}{2}.         \tag{9}
\]
Let \(Y_1,Y_2,Y_3\) be the unweighted branch-Pauli operators
\[
\begin{aligned}
Y_1&=|{\cal A}\rangle\langle{\cal B}|
    +|{\cal B}\rangle\langle{\cal A}|,\\
Y_2&=i(|{\cal A}\rangle\langle{\cal B}|
      -|{\cal B}\rangle\langle{\cal A}|),\\
Y_3&=|{\cal A}\rangle\langle{\cal A}|
    -|{\cal B}\rangle\langle{\cal B}|.
\end{aligned}                                               \tag{10}
\]
Direct expansion eliminates all one-site diagonal overlaps and gives
the following compact equivalent of the sharp crossed defect:
\[
\boxed{\begin{aligned}
 D({\cal A},{\cal B})
={}&3p+\frac{T^2-|h|^2}{2}
 -\sum_i\bigl(\|A_{Ki}\|_2^2+\|B_{Ki}\|_2^2\bigr)\\
&+\sum_i\|(Y_3)_{Ki}\|_2^2
 +\frac14\sum_i\left(
   \|(Y_1)_i\|_2^2+\|(Y_2)_i\|_2^2\right).
\end{aligned}}                                               \tag{11}
\]
For example,
\[
 \|(Y_3)_R\|_2^2
 =\|A_R\|_2^2+\|B_R\|_2^2-2q_R
\]
and
\[
 \|(Y_1)_i\|_2^2+\|(Y_2)_i\|_2^2
 =4q_{Kjk}.
\]
Substitution in (11) gives
\[
 D=3q_K-2\sum_iq_{Ki}+\sum_{i<j}q_{Kij}
   +\frac{T^2-|h|^2}{2},
\]
as required.  Thus a merged-frame proof can be phrased without the
four exterior parity sectors: it must prove the single marginal
inequality (11).

## 3. An exact enriched formal countermodel

Index subsets of the four parties by
\(\{K,1,2,3\}\).  Set
\[
 T=1,\qquad h=0,\qquad \rho_K^{\cal A}=\rho_K^{\cal B}
 =\frac12I_2,\qquad p=\frac12.                              \tag{12}
\]
Give the two formal self-purity profiles the same values
\[
 a_\varnothing=a_{K123}=b_\varnothing=b_{K123}=1,\qquad
 a_R=b_R=\frac12
\quad(\varnothing\ne R\ne K123).                            \tag{13}
\]
Set the crossed overlaps to
\[
\begin{array}{c|c}
R&q_R\\ \hline
\varnothing&1\\
K,\ i,\ Ki,\ ij&1/2\\
Kij,\ 123,\ K123&0 .
\end{array}                                                 \tag{14}
\]
Here \(i,j\) are distinct physical sites.

### 3.1 Exact sector positivity

The self swap-sector transform of (13) is
\[
 a^{\rm sec}_\varnothing=\frac9{16},\qquad
 a^{\rm sec}_R=\frac1{16}
\quad(|R|=2\ \hbox{or}\ R=K123),
                                                               \tag{15}
\]
with all other masses zero.  The crossed transform of (14) is
\[
 q^{\rm sec}_\varnothing=\frac38,\qquad
 q^{\rm sec}_{K}
 =q^{\rm sec}_{1}
 =q^{\rm sec}_{2}
 =q^{\rm sec}_{3}
 =q^{\rm sec}_{K123}
 =\frac18,                                                   \tag{16}
\]
with all other masses zero.  Hence every exact two-replica sector mass
is nonnegative.  Also \(q_R\leq\sqrt{a_Rb_R}\) for every \(R\).

### 3.2 The original adaptive frames

The following one-block matrices realize every norm used by the six
original adaptive inequalities:
\[
 X_{0,i}^{\cal A}=X_{0,i}^{\cal B}=\frac12I_2,\qquad
 X_{a,i}^{\cal A}=X_{a,i}^{\cal B}
 =-\frac1{\sqrt{12}}\sigma_a
\quad(a=1,2,3).                                             \tag{17}
\]
They obey
\[
 \|X_{a,i}\|_2^2=\frac16,\qquad
 \|X_{a,i}\|_1^2=\frac13,\qquad
 \operatorname{Tr}X_{a,i}=0.                               \tag{18}
\]
Thus for every permutation
\[
 \delta_\pi=\frac12-3\cdot\frac16=0,\qquad
 \alpha_\pi=1-3\cdot\frac13=0,\qquad
 \beta_{\pi,i}=0.                                          \tag{19}
\]
The \({\cal A}\) and \({\cal B}\) matrices coincide, so every polarized
gap \(d_\pi({\cal A},{\cal B})\) is zero and hence \(D_0=0\).

These are not merely norm tables.  The formal \(Ki\)-marginal
\[
 \rho_{Ki}
 =\frac14I_4-\frac1{2\sqrt{12}}
  \sum_{a=1}^3\sigma_a\otimes\sigma_a                     \tag{20}
\]
is positive.  Its triplet eigenvalue is
\[
 \frac14-\frac1{4\sqrt3}>0
\]
and its singlet eigenvalue is
\[
 \frac14+\frac3{4\sqrt3}>0.
\]

### 3.3 All weighted merged frames

For a merged block \(Ki\), take
\[
 A_{Ki}=B_{Ki}=\frac12I_2,\qquad
 D_*=\frac1{\sqrt2}\operatorname{diag}(1,-1),\qquad
 Z_{Ki}=\frac{1-i}{2}D_* .                                 \tag{21}
\]
Then
\[
 S_{Ki}=T_{Ki}=D_*,\qquad
 \|D_*\|_2^2=1,\qquad \|D_*\|_1^2=2.                       \tag{22}
\]
For either singleton block in \((Ki)\mid j\mid k\), take
\[
 A_j=B_j=\frac12I_2,\qquad Z_j=0.                           \tag{23}
\]
Equations (21)--(23) have exactly the purities and crossed overlaps in
(13)--(14).  Moreover the branch-block density
\[
 \frac12\left(
 I_L\otimes I+
 X_L\otimes D_*+
 Y_L\otimes D_*
 \right)                                                    \tag{24}
\]
is positive: \((X_L+Y_L)\otimes D_*\) is a Hermitian unitary.

Now keep arbitrary \(x,y\geq0\).  If branch \(Z\) is assigned to the
merged block, (5)--(7) give
\[
\begin{aligned}
\delta&=\frac{(x+y)^2}{2},&
\alpha&=4xy,&
\beta_d&=(x-y)^2,
\end{aligned}                                               \tag{25}
\]
and all other \(\beta\)'s vanish.  If branch \(X\) or \(Y\) is assigned
to the merged block, they give
\[
\begin{aligned}
\delta&=\frac{x^2+y^2}{2},&
\alpha&=2xy,&
\beta_d&=(x-y)^2,
\end{aligned}                                               \tag{26}
\]
again with the other \(\beta\)'s zero.  In both cases
\(2\delta=\alpha+\sum\beta\).  Therefore all six assignments in each
of the three merged groupings, including the complete weighted
trace-norm family, hold for every \(x,y\geq0\).

### 3.4 The target is nevertheless negative

Equations (12)--(14) give
\[
\begin{aligned}
 D_0
 &=3q_K-2\sum_iq_{Ki}+\sum_iq_i
 =\frac32-3+\frac32=0,\\
 E
 &=\sum_{i<j}q_{Kij}-\sum_iq_i+\frac{T^2-|h|^2}{2}
 =0-\frac32+\frac12=-1.
\end{aligned}                                               \tag{27}
\]
Consequently
\[
 \boxed{\qquad D=-1,\qquad Q_3^{\rm formal}=-\frac14.\qquad} \tag{28}
\]
This proves that the separate adaptive inequalities do not dominate
the exterior correction.  Since unrestricted three-copy positivity is
not disproved, the data (12)--(24) cannot arise from one common pair of
global vectors.  The next section finds an explicit incompatibility.

## 4. The first violated common-origin condition

For the data (17), every trace-norm and anticommuting-contraction step
is saturated.  Equality is more rigid than the scalar equations
(19).

Use Pauli matrices \(X,Y,Z\) on \(K\) and on each physical two-level
support.  For the identity assignment define
\[
 M=-\frac1{\sqrt3}
 \left(X_KX_1+Y_KY_2+Z_KZ_3\right),                       \tag{29}
\]
and for the cyclic assignment define
\[
 N=-\frac1{\sqrt3}
 \left(Y_KY_1+Z_KZ_2+X_KX_3\right).                       \tag{30}
\]
The three summands in either operator anticommute, so
\[
 M^2=N^2=I.                                                \tag{31}
\]
In the formal model every one of the three sign expectations in each
frame is \(1/\sqrt3\).  Saturation of the anticommuting-contraction
bound would therefore force a realizing unit vector \({\cal A}\) to
satisfy
\[
 M{\cal A}={\cal A},\qquad N{\cal A}={\cal A}.             \tag{32}
\]

This is impossible.  Direct Pauli multiplication gives
\[
 \{M,N\}=\frac23\,J,                                       \tag{33}
\]
where
\[
\begin{aligned}
J={}&-Z_KZ_1+X_1X_3+Y_1Y_2\\
   &-X_KX_2+Z_2Z_3-Y_KY_3
\end{aligned}                                               \tag{34}
\]
and
\[
 J^3=8J.                                                    \tag{35}
\]
Hence
\[
 \|\{M,N\}\|\leq\frac{4\sqrt2}{3}<2.                       \tag{36}
\]
But (32) would give
\[
 \langle{\cal A},\{M,N\}{\cal A}\rangle=2,
\]
a contradiction.

More generally, for every unit vector \(\psi\), put
\[
 m=\langle\psi,M\psi\rangle,\qquad
 n=\langle\psi,N\psi\rangle.
\]
Since
\[
 (aM+bN)^2=(a^2+b^2)I+ab\{M,N\},
\]
choosing \(a=m,b=n\) and using (36) gives the explicit nonlinear
joint-frame compatibility inequality
\[
\boxed{\qquad
 m^2+n^2\leq1+\frac{2\sqrt2}{3}<2.
\qquad}                                                     \tag{37}
\]
The formal model asks for \(m=n=1\), so (37) separates it exactly.

Equation (37) is information which none of the six adaptive
inequalities contains separately.  It is the smallest live remnant
exposed by this no-go: a successful proof through adaptive frames must
control the joint Gram matrix of different state-dependent sign
frames.  The remaining difficulty is to construct an analogue of
(37) for arbitrary, noncommuting sign observables and to show that its
aggregate deficit dominates the exterior correction in (29g).

## 5. Exact scope

Established here:

1. the exact weighted merged Gram inequality (5), its trace-norm
   resolution (6)--(7), and the copositive form (8);
2. the smaller branch-marginal target (11);
3. an exact enriched formal model proving that all separate original
   and merged adaptive inequalities are insufficient;
4. an explicit common-origin separator (37).

Not established:

1. no physical pair \({\cal A},{\cal B}\) realizes the formal model;
2. no rank-two matrix with negative \(Q_3\) is produced;
3. (37) has not yet been generalized to the arbitrary adaptive signs
   needed for a proof of unrestricted three-copy positivity.
