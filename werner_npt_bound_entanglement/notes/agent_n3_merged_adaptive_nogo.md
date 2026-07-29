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

There is an exact state-dependent version of this separator.  Normalize
an arbitrary adaptive-frame purification to trace one.  For a
permutation \(\pi\), put
\[
 x_{\pi,i}=\|X_{\pi(i),i}\|_1,\qquad
 s_\pi=\sum_i x_{\pi,i}^2=1-\alpha_\pi,
\]
and, when \(s_\pi>0\), define
\[
 {\mathcal M}_\pi
 =\frac1{\sqrt{s_\pi}}\sum_i
 x_{\pi,i}\,
 \sigma_{\pi(i)}^{(K)}\otimes
 \operatorname{sgn}(X_{\pi(i),i}).                         \tag{38}
\]
The summands within one frame anticommute, so
\[
 {\mathcal M}_\pi^2\preceq I,\qquad
 \langle{\mathcal M}_\pi\rangle=\sqrt{s_\pi}.              \tag{39}
\]
For any two permutations \(\pi,\tau\), the variance inequality applied
to
\(\sqrt{s_\pi}{\mathcal M}_\pi+
  \sqrt{s_\tau}{\mathcal M}_\tau\)
therefore gives the universal joint-frame bound
\[
\boxed{\qquad
 \alpha_\pi+\alpha_\tau
 \geq
 1-\frac12
 \left\|\{
 {\mathcal M}_\pi,{\mathcal M}_\tau
 \}\right\|.
\qquad}                                                     \tag{40}
\]
For an unnormalized purification of trace \(T\), multiply the
right-hand side by \(T^2\) and use the normalized \(x_{\pi,i}/T\).

For completeness, if \(G_i,H_i\) are the two local sign operators,
the anticommutator in (40) contains only two types of terms.  When the
same logical axis is assigned to different sites, it contains the
product \(G_iH_j\).  When different logical axes are assigned to the
same site, it contains the local commutator \([G_i,H_i]\), multiplied
by the corresponding skew Pauli product on \(K\).  Thus (40) is an
explicit finite Gram constraint on the common origin of two adaptive
frames, not a new purity inequality.

Equation (40) is information which none of the six adaptive
inequalities contains separately.  In the formal model,
\({\mathcal M}_\pi=M\), \({\mathcal M}_\tau=N\), and (40) is exactly
the strict contradiction following (36).  This is the smallest live
remnant exposed by the no-go: a successful proof through adaptive
frames must bound the joint anticommutators of the state-dependent sign
frames and show that their aggregate deficit dominates the exterior
correction in (29g).

## 5. The full joint-frame orbit still does not close

The separator (40) kills the saturated model in Section 3, but adding
its full permutation orbit still does not imply the desired exterior
inequality.  Here is an exact second formal survivor.

Keep \(T=1,h=0,p=1/2\).  Let the common self-purity profile be
\[
\begin{array}{c|c}
R&a_R=b_R\\ \hline
\varnothing,\ K123&1\\
K,\ 123&1/2\\
i,\ Kjk&53/100\\
Ki,\ jk&101/200 ,
\end{array}                                                  \tag{41}
\]
and let the crossed profile be
\[
\begin{array}{c|c}
R&q_R\\ \hline
\varnothing&1\\
K&1/2\\
i&51/100\\
Ki&99/200\\
ij&101/200\\
Kij&1/200\\
123&3/200\\
K123&0 .
\end{array}                                                  \tag{42}
\]
All displayed physical indices are distinct where appropriate.

The self sector masses are
\[
\begin{array}{c|c}
R&a_R^{\rm sec}\\ \hline
\varnothing&921/1600\\
Ki&105/1600\\
ij&93/1600\\
K123&85/1600,
\end{array}                                                  \tag{43}
\]
and all others vanish.  The crossed sector masses are
\[
\begin{array}{c|c}
R&q_R^{\rm sec}\\ \hline
\varnothing&303/800\\
K&103/800\\
i&99/800\\
K123&97/800,
\end{array}                                                  \tag{44}
\]
with all others zero.  Thus exact sector positivity and every
Hilbert--Schmidt Cauchy bound hold.

### 5.1 Original adaptive frames and their complete pair orbit

Choose the nine traceless Pauli reductions
\[
 X_{a,i}^{\cal A}=X_{a,i}^{\cal B}
 =-\frac{\sqrt2}{5}\sigma_a.                               \tag{45}
\]
Their squared Hilbert--Schmidt and trace norms are
\[
 \|X_{a,i}\|_2^2=\frac4{25},\qquad
 \|X_{a,i}\|_1^2=\frac8{25}.                               \tag{46}
\]
The two one-site density matrices may be chosen with Bloch vectors
\[
 r_{\cal A}=\left(0,0,\frac{\sqrt6}{10}\right),\qquad
 r_{\cal B}=\left(\frac{2\sqrt3}{15},0,
                        \frac{\sqrt6}{30}\right).          \tag{47}
\]
They have squared lengths \(3/50\) and mutual inner product \(1/50\),
so (41)--(42) hold at levels \(i\) and \(Ki\).  The corresponding
\(Ki\) block is positive; a simple lower bound for its least eigenvalue
is
\[
 \frac14-\frac{\sqrt2}{10}-\frac{\sqrt6}{40}>0.            \tag{48}
\]

Every permutation now has
\[
 \delta_\pi=\frac1{50},\qquad
 \alpha_\pi=\frac1{25},\qquad
 \beta_{\pi,i}=0,\qquad
 d_\pi=\frac1{50}.                                         \tag{49}
\]
For the six Pauli sign frames, direct multiplication shows
\[
 \|\{{\cal M}_\pi,{\cal M}_\tau\}\|
 =
 \begin{cases}
 4\sqrt2/3,&\pi^{-1}\tau\text{ is a three-cycle},\\
 2,&\pi^{-1}\tau\text{ is a transposition}.
 \end{cases}                                                \tag{50}
\]
For a three-cycle, (40) becomes
\[
 \frac2{25}\geq1-\frac{2\sqrt2}{3},                        \tag{51}
\]
which is exact because \(5000>4761\).  For a transposition its
right-hand side is zero.  Hence the entire fifteen-pair orbit of the
joint-frame separator holds.

### 5.2 The separate merged inequalities still hold with all weights

The weighted merged inequalities (5)--(7) also admit exact local
matrix data for (41)--(42).  On the merged block take
\[
 A_b=\frac1{20}\operatorname{diag}(11,9),\qquad
 B_b=\frac1{20}\operatorname{diag}(9,11),
\]
\[
 Z_b=e^{-i\pi/4}
 \begin{pmatrix}0&11/20\\9/20&0\end{pmatrix}.              \tag{52}
\]
Then
\[
\begin{aligned}
\|A_b\|_2^2=\|B_b\|_2^2&=\frac{101}{200},&
\operatorname{Tr}(A_bB_b)&=\frac{99}{200},\\
\|Z_b\|_2^2&=\frac{101}{200},&
\|S_b\|_2^2=\|T_b\|_2^2&=\frac{101}{100},\\
\|S_b\|_1^2=\|T_b\|_1^2&=\frac{101}{50}.
\end{aligned}                                               \tag{53}
\]
On a singleton use the two density matrices with Bloch vectors (47)
and
\[
 Z_s=e^{-i\pi/4}\frac1{20}\operatorname{diag}(1,-1).       \tag{54}
\]
Thus
\[
\begin{aligned}
\|A_s\|_2^2=\|B_s\|_2^2&=\frac{53}{100},&
\operatorname{Tr}(A_sB_s)&=\frac{51}{100},\\
\|Z_s\|_2^2&=\frac1{200},&
\|S_s\|_2^2=\|T_s\|_2^2&=\frac1{100},\\
\|S_s\|_1^2=\|T_s\|_1^2&=\frac1{50}.
\end{aligned}                                               \tag{55}
\]
Both local branch block matrices are positive.  For (52) this follows
from the exact factorization
\(Z_b=A_b^{1/2}(e^{-i\pi/4}X)B_b^{1/2}\).  For (54), the Schur
contraction has norm strictly below one.

By homogeneity set \(y=1\) and write \(x=r\geq0\).  If branch \(X\) or
\(Y\) is assigned to the merged block, the Hilbert--Schmidt gap is
\[
 \delta_{X/Y}(r)=\frac{47}{100}(r^2+1).                    \tag{56}
\]
If branch \(Z\) is assigned there, it is
\[
 \delta_Z(r)=\frac{99}{200}(r^2+1)+\frac{97}{100}r.        \tag{57}
\]
The trace-norm gaps are also nonnegative for every \(r\).  For an
\(X/Y\)-merged assignment,
\[
 \alpha_{X/Y}(r)=
 \begin{cases}
 \dfrac{49}{25}r,
 &r\notin[r_-,r_+],\\[4pt]
 \dfrac{47}{50}(r^2+1),
 &r\in[r_-,r_+],
 \end{cases}
\quad
 r_\pm=\frac{49\pm8\sqrt3}{47}.                            \tag{58}
\]
For a \(Z\)-merged assignment,
\[
 \alpha_Z(r)=
 \begin{cases}
 \dfrac{99}{25}r,
 &r\notin[9/11,11/9],\\[4pt]
 \dfrac{99r^2+194r+99}{100},
 &r\in[9/11,11/9].
 \end{cases}                                                \tag{59}
\]
Every \(\beta\) is nonnegative by the exact trace-norm lemma, and
\(2\delta=\alpha+\sum\beta\).  Thus the full separate weighted
merged-frame system survives.

### 5.3 It remains formally negative

The original adaptive part is now positive but too small:
\[
 D_0=3q_K-2\sum_iq_{Ki}+\sum_iq_i=\frac3{50}.              \tag{60}
\]
The exterior correction is
\[
 E=\sum_{i<j}q_{Kij}-\sum_iq_i+\frac12
 =-\frac{203}{200}.                                        \tag{61}
\]
Therefore
\[
\boxed{\qquad
 D=-\frac{191}{200},\qquad
 Q_3^{\rm formal}=-\frac{191}{800}.
\qquad}                                                     \tag{62}
\]

This second model is again nonphysical.  What it proves is more
specific: even the complete pair orbit of the first joint-frame
separator, together with every separate weighted merged inequality,
does not dominate the exterior correction.

The strictly smaller residual is now clear.  One needs either:

1. a higher joint Gram constraint coupling at least three adaptive
   permutations at once; or
2. a quantitative inequality tying the anticommutator norms in (40)
   to the transition/exterior overlaps in (29g).

Allowing each pairwise anticommutator deficit to float independently is
still insufficient.

## 6. The first three-frame Clifford constraint and a third survivor

The six Pauli frames split into the even and odd permutations.  Let
\({\cal E}\) be the three even frames and \({\cal O}\) the three odd
frames.  Exact Pauli multiplication gives
\[
 \left\|\sum_{\pi\in{\cal E}}{\cal M}_\pi\right\|
 =\left\|\sum_{\pi\in{\cal O}}{\cal M}_\pi\right\|
 =\frac5{\sqrt3}.                                          \tag{63}
\]
A compact exact certificate is obtained before dividing the frames by
\(\sqrt3\): the two integer-Pauli sums have spectrum contained in
\[
 \{-3,-1,3,5\},
\]
and \(5\) occurs.  Thus any common state with equal frame expectation
\(m\) must obey
\[
 3m\leq\frac5{\sqrt3},\qquad m^2\leq\frac{25}{27}.         \tag{64}
\]

The second survivor has \(m^2=24/25\), so (64) excludes it:
\[
 \frac{24}{25}>\frac{25}{27}.
\]
However, the full even/odd orbit of (64) still does not close the
formal relaxation.

Take instead
\[
\begin{array}{c|c}
R&a_R=b_R\\ \hline
\varnothing,\ K123&1\\
K,\ 123&1/2\\
i,\ Kjk&53/100\\
Ki,\ jk&99/200 ,
\end{array}                                                  \tag{65}
\]
and
\[
\begin{array}{c|c}
R&q_R\\ \hline
\varnothing&1\\
K&1/2\\
i&253/500\\
Ki&483/1000\\
ij&99/200\\
Kij&0\\
123&9/500\\
K123&0 .
\end{array}                                                  \tag{66}
\]
The exact self sector masses are
\[
\begin{array}{c|c}
R&a_R^{\rm sec}\\ \hline
\varnothing&183/320\\
Ki&107/1600\\
ij&19/320\\
K123&79/1600,
\end{array}                                                  \tag{67}
\]
and the crossed masses are
\[
\begin{array}{c|c}
R&q_R^{\rm sec}\\ \hline
\varnothing&597/1600\\
K&259/2000\\
i&247/2000\\
Ki&1/1600\\
ij&17/8000\\
K123&949/8000 .
\end{array}                                                  \tag{68}
\]
All omitted masses vanish; in particular all sector and Cauchy
constraints remain exact and nonnegative.

Choose again aligned Pauli reductions, now with
\[
 \sum_a\|X_{a,i}\|_2^2=\frac{23}{50},\qquad
 \sum_a\|X_{a,i}\|_1^2=\frac{23}{25}.                      \tag{69}
\]
For example, take
\[
 X_{a,i}^{\cal A}=X_{a,i}^{\cal B}
 =-\sqrt{\frac{23}{300}}\,\sigma_a.                        \tag{70}
\]
The one-site Bloch vectors can have squared length \(3/50\) and mutual
inner product \(3/250\); one exact choice is
\[
 r_{\cal A}=\left(0,0,\frac{\sqrt6}{10}\right),\qquad
 r_{\cal B}=\left(\frac6{25},0,\frac{\sqrt6}{50}\right).
                                                                    \tag{71}
\]
Consequently every original frame has
\[
 \delta_\pi=d_\pi=\frac1{25},\qquad
 \alpha_\pi=\frac2{25},\qquad
 \beta_{\pi,i}=0,\qquad
 m^2=\frac{23}{25}.                                       \tag{72}
\]
All pairwise joint-frame bounds hold.  The three-frame constraint
(64) also holds, now sharply close to its boundary:
\[
 \frac{23}{25}\leq\frac{25}{27}
 \quad\Longleftrightarrow\quad
 621\leq625.                                               \tag{73}
\]

The separate weighted merged inequalities remain positive.  Their
Hilbert--Schmidt gaps are, after setting \(y=1,x=r\),
\[
 \delta_{X/Y}(r)
 =\frac{47}{100}(r^2+1)+\frac{11}{500}r,\qquad
 \delta_Z(r)
 =\frac{101}{200}(r^2+1)+\frac{483}{500}r.                 \tag{74}
\]
For the trace-norm part, an \(X/Y\)-merged assignment has transition
contribution \(99r/50\).  The remaining two-dimensional Hermitian
difference has squared trace norm either \((r-1)^2\), or
\[
 \frac3{50}(r^2+1)-\frac3{125}r
\]
in its indefinite interval.  Hence its \(\alpha\) gap is respectively
\[
 \frac{101}{50}r
\quad\hbox{or}\quad
 \frac{47}{50}(r^2+1)+\frac{11}{250}r,                    \tag{75}
\]
both nonnegative.  A \(Z\)-merged assignment has no singleton
transition term, so
\[
 \alpha_Z(r)=(r+1)^2-\|rA_b-B_b\|_1^2\geq0                \tag{76}
\]
by the triangle inequality for density matrices.  As before, all
\(\beta\)'s are automatically nonnegative.

Nevertheless,
\[
\boxed{\begin{aligned}
 D_0&=\frac3{25},&
 E&=-\frac{509}{500},\\
 D&=-\frac{449}{500},&
 Q_3^{\rm formal}&=-\frac{449}{2000}.
\end{aligned}}                                             \tag{77}
\]
This third model is formal and nonphysical.

Thus the equal-weight three-frame Clifford constraint does expose
genuinely new common-origin information, but it still does not settle
the exterior inequality.

## 7. The complete frame support hierarchy also survives

In fact, arbitrarily weighting triples, quadruples, or all six frames
cannot exclude the third model.  This is not merely another formal
linear-program observation: the six requested frame expectations have
an exact common **pure-state** realization.

Write
\[
 \widehat M_\pi=\sqrt3\,{\cal M}_\pi,\qquad
 H=\sum_{\pi\in S_3}\widehat M_\pi .                       \tag{78}
\]
Thus every \(\widehat M_\pi\) is the sum of three integer Pauli
strings and \(\widehat M_\pi^2=3I\).  Direct Pauli multiplication gives
the exact spectral certificate
\[
 (H-10I)(H-6I)(H+2I)(H+6I)=0.                             \tag{79}
\]
The eigenvalues \(10\) and \(6\) both occur.  In the computational
basis numbered \(0,\ldots,15\), define the two unit vectors
\[
\begin{aligned}
 u&=\frac{-e_1-e_2-e_4+3e_8}{\sqrt{12}},\\
 w&=\frac{ e_5-e_6-e_9+e_{10}}{2}.
\end{aligned}                                               \tag{80}
\]
They are orthogonal and an exact multiplication gives, for every
\(\pi\in S_3\),
\[
\begin{aligned}
 \langle u,\widehat M_\pi u\rangle&=\frac53,&
 \langle w,\widehat M_\pi w\rangle&=1,&
 \langle u,\widehat M_\pi w\rangle&=0.                    \tag{81}
\end{aligned}
\]
The last equality is also immediate from parity: every frame preserves
computational-basis parity, while \(u\) and \(w\) have opposite parity.

Set
\[
 t=\frac{3(\sqrt{69}-5)}{10}.                              \tag{82}
\]
This lies strictly between zero and one: \(69>25\), while
\(t<1\) is equivalent to \(621<625\).  The pure unit vector
\[
 \psi=\sqrt t\,u+\sqrt{1-t}\,w                            \tag{83}
\]
then obeys, for all six frames,
\[
\begin{aligned}
 \langle\psi,{\cal M}_\pi\psi\rangle
 &=\frac1{\sqrt3}\left(\frac53t+1-t\right)\\
 &=\frac1{\sqrt3}\left(1+\frac23t\right)
 =\frac{\sqrt{23}}5.                                      \tag{84}
\end{aligned}
\]
Its squared expectation is exactly \(23/25\), which is the value
required in (72).

Consequently, for arbitrary real coefficients \(c_\pi\),
\[
 \frac{\sqrt{23}}5\sum_\pi c_\pi
 =
 \left\langle\psi,
 \left(\sum_\pi c_\pi{\cal M}_\pi\right)\psi
 \right\rangle
 \leq
 \lambda_{\max}\left(\sum_\pi c_\pi{\cal M}_\pi\right).
                                                               \tag{85}
\]
Applying the same statement to the negative coefficients gives every
operator-norm support inequality as well.  Thus all arbitrarily
weighted triple, four-frame, five-frame, and six-frame first-moment
constraints hold automatically.  The covariance/Gram matrix
\[
 G_{\pi\tau}
 =
 \left\langle
 ({\cal M}_\pi-m)\psi,\,
 ({\cal M}_\tau-m)\psi
 \right\rangle,\qquad m=\frac{\sqrt{23}}5,                 \tag{86}
\]
is also manifestly positive semidefinite.  Hence an unrestricted
six-frame Gram determinant with its unprescribed cross entries cannot
separate the model either.

There is an even stronger mixed-state observation at the level of the
nine individual Pauli correlators.  Let \(P_{10}\) be the spectral
projection of \(H\) at eigenvalue \(10\).  Polynomial interpolation
from (79) gives
\[
 P_{10}
 =
 \frac{(H-6I)(H+2I)(H+6I)}
 {(10-6)(10+2)(10+6)}.                                    \tag{87}
\]
It has trace three, and exact multiplication gives
\[
 P_{10}\widehat M_\pi P_{10}=\frac53P_{10}
 \quad(\pi\in S_3).                                       \tag{88}
\]
By the site-and-axis permutation symmetry, the state \(P_{10}/3\)
has expectation \(5/9\) on each of the nine Pauli strings entering the
six frames.  Mixing it with \(I/16\) in the proportion
\[
 \frac{3\sqrt{69}}{25}
\]
therefore realizes the third model's individual value
\(\sqrt{23/75}\) exactly.  This last state is mixed, so it does not
settle the pure common-marginal problem; it shows that no linear
support separation of the nine first moments is possible.

The surviving obstruction is consequently finer than a support
function or a free covariance Gram matrix.  It must retain at least
one of:

1. the purity/decomposability of the common vector together with all
   nine individual sign observables;
2. the actual one- and two-block marginals, not merely their six frame
   sums;
3. a direct nonlinear relation between those marginals and the
   transition/exterior overlaps in (29g).

## 8. Exact scope

Established here:

1. the exact weighted merged Gram inequality (5), its trace-norm
   resolution (6)--(7), and the copositive form (8);
2. the smaller branch-marginal target (11);
3. an exact enriched formal model proving that all separate original
   and merged adaptive inequalities are insufficient;
4. an explicit common-origin separator (37) and its general
   state-dependent form (40);
5. a second exact formal survivor showing that the complete pair orbit
   of (40), plus all separate weighted merged inequalities, is still
   insufficient;
6. the first exact three-frame Clifford separator and a third formal
   survivor showing that its equal-weight permutation orbit is still
   insufficient;
7. an exact pure common state proving that the entire arbitrarily
   weighted six-frame support hierarchy and its free Gram completion
   still do not exclude that third survivor.

Not established:

1. no physical pair \({\cal A},{\cal B}\) realizes the formal model;
2. no rank-two matrix with negative \(Q_3\) is produced;
3. no finer pure common-marginal inequality coupling the nine sign
   observables to the exterior overlaps has been proved.
