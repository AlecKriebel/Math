# The exact rank-pair dual and its reversible conductance storage law

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note gives an exact primal/dual formulation of the live
rank-dependent quadratic-potential route at fitness two.  It also proves a
new conductance-storage identity which turns the two-marked part of the dual
into a literal cache-cut occupation term.

These statements are **PROVED**.  The final endpoint inequality for the
resulting nonnegative two-moment pseudoflows remains **OPEN**.  In
particular, the numerical feasibility tests in this directory are not a
universal theorem.

## 1. Kernel, rates, and the slice-quadratic space

Let `G` be a connected loopless undirected weighted graph on `V`, with
`|V|=n`, and put

\[
 P_{vi}={w_{vi}\over d_v},\qquad x_v(S)=P_{vS}.
\]

The common factor `1/n` in the dB transition probabilities is suppressed.
At fitness two, write

\[
 g_v(S)={2x_v(S)\over1+x_v(S)}\quad(v\notin S),\qquad
 \ell_v(S)={1-x_v(S)\over1+x_v(S)}\quad(v\in S),                 \tag{1}
\]

and

\[
 U(S)=\sum_{v\notin S}g_v(S),\qquad
 D(S)=\sum_{v\in S}\ell_v(S).                                  \tag{2}
\]

Thus the unscaled transient generator is

\[
 (LF)(S)=\sum_{v\notin S}g_v(S)\{F(S\cup v)-F(S)\}
 +\sum_{v\in S}\ell_v(S)\{F(S\setminus v)-F(S)\}.              \tag{3}
\]

For `0<=k<=n`, let `W_k` be the restrictions to the `k`-slice of
multilinear polynomials of degree at most two.  Equivalently, `W_k` is
spanned by

\[
 1,\qquad 1_{\{a\in S\}},\qquad
 1_{\{a,b\subseteq S\}}\quad(a<b).                              \tag{4}
\]

Let `W` be the direct sum of these spaces over the nonempty slices, with
`F(\varnothing)=0` fixed.

## 2. Exact primal and dual

The live primal relaxation is

\[
 p_*(P)=\min_{F\in W}{1\over n}\sum_aF(\{a\})                    \tag{5}
\]

subject to

\[
 F(V)=1,\qquad LF(S)\le0\quad(\varnothing\ne S\ne V).           \tag{6}
\]

The inequalities imply `F>=h`, where `h` is the true fixation harmonic
function.  Hence the primal is bounded below; it is feasible, for example,
with `F(S)=1` on every nonempty state.  Finite-dimensional LP duality
therefore applies without adding the numerically useful but mathematically
redundant inequalities `F(S)>=0`.

Let

\[
 c(T)={1\over n}1_{\{|T|=1\}}.
\]

The exact dual is

\[
 \boxed{\quad p_*(P)=\max z\quad}                               \tag{7}
\]

over a free scalar `z` and weights

\[
 y_S\ge0\qquad(\varnothing\ne S\ne V)                          \tag{8}
\]

such that

\[
 \boxed{\quad c+L^Ty-z\,\delta_V\ \perp\ W.\quad}             \tag{9}
\]

Thus `(9)` is not full statewise conservation.  On every rank it imposes
exact conservation of mass, of every one-vertex marked moment, and of every
two-vertex marked moment.  The dual objects are consequently nonnegative
two-moment pseudoflows.

The orientation in `(7)--(9)` is important.  To prove the desired
rank-pair certificate it is necessary and sufficient to prove

\[
 z\le \rho_{\rm dB}(K_n,2)
 ={(n-1)2^{n-2}\over n(2^{n-1}-1)}                              \tag{10}
\]

for every feasible pseudoflow.  Constructing one feasible pseudoflow at
the complete value would give a lower bound on `(5)`, not the needed upper
bound.

The true Green occupation measure started from a uniform singleton obeys
full statewise conservation and is dual-feasible with `z` equal to the true
fixation probability.  Hence `(7)` is indeed a relaxation of the exact
fixation problem.

## 3. Rank mass and marked recurrences

Put

\[
 A_k=\sum_{|S|=k}y_SU(S),\qquad
 R_k=\sum_{|S|=k}y_SD(S),                                    \tag{11}
\]

with absent boundary terms set to zero.  Testing `(9)` against the rank
constant gives, for `1<=k<=n`,

\[
 1_{\{k=1\}}+A_{k-1}+R_{k+1}-A_k-R_k-z1_{\{k=n\}}=0.          \tag{12}
\]

In particular,

\[
 z=A_{n-1}=1-R_1,
 \qquad A_k-R_{k+1}=z\quad(1\le k<n).                         \tag{13}
\]

For a vertex `a`, the exact one-mark balance on rank `k` is

\[
\begin{aligned}
0={}&{1_{\{k=1\}}\over n}
 +\sum_{|S|=k-1}y_S
 \bigl(1_{\{a\in S\}}U(S)+1_{\{a\notin S\}}g_a(S)\bigr)\\
&+\sum_{\substack{|S|=k+1\\a\in S}}y_S\{D(S)-\ell_a(S)\}
 -\sum_{\substack{|S|=k\\a\in S}}y_S\{U(S)+D(S)\}
 -z1_{\{k=n\}}.                                             \tag{14}
\end{aligned}
\]

For distinct `a,b`, the two-mark balance is

\[
\begin{aligned}
0={}&\sum_{|S|=k-1}y_S\bigl[
 1_{\{a,b\subseteq S\}}U(S)
 +1_{\{a\in S,b\notin S\}}g_b(S)
 +1_{\{b\in S,a\notin S\}}g_a(S)\bigr]\\
&+\sum_{\substack{|S|=k+1\\a,b\in S}}
 y_S\{D(S)-\ell_a(S)-\ell_b(S)\}\\
&-\sum_{\substack{|S|=k\\a,b\in S}}y_S\{U(S)+D(S)\}
 -z1_{\{k=n\}}.                                             \tag{15}
\end{aligned}
\]

Equations `(12)`, `(14)`, and `(15)` are exactly equivalent to `(9)`.

For later use, if `b=(b_a)` and `B_b(S)=sum_(a in S)b_a`, define

\[
 G_b(S)=\sum_{a\notin S}b_ag_a(S),\qquad
 Q_b(S)=\sum_{a\in S}b_a\ell_a(S).                           \tag{16}
\]

Then, for an arbitrary rank sequence `q_k`,

\[
\begin{aligned}
L\{q_{|S|}B_b(S)\}
={}&B_b(S)\bigl[(q_{k+1}-q_k)U(S)
 +(q_{k-1}-q_k)D(S)\bigr]\\
&+q_{k+1}G_b(S)-q_{k-1}Q_b(S),\qquad k=|S|.                  \tag{17}
\end{aligned}
\]

This is the precise family of one-mark identities available for a
rank-dependent reversible Poisson correction.

## 4. Reversible conductance storage

Normalize the reversible stationary law by `sum_i pi_i=1`, and put

\[
 c_{ij}=\pi_iP_{ij}=\pi_jP_{ji}.                              \tag{18}
\]

For a mutant set `S`, define stationary mass, internal conductance, storage,
and cut by

\[
 M(S)=\sum_{i\in S}\pi_i,\qquad
 E(S)=\sum_{\{i,j\}\subseteq S}c_{ij},                        \tag{19}
\]

\[
 H(S)=M(S)+E(S),\qquad
 C(S)=\sum_{i\in S,j\notin S}c_{ij}=M(S)-2E(S).              \tag{20}
\]

Both `H` and `C` are slice-quadratic.  If `v` is added to or removed from
`S`, reversibility gives

\[
 H(S\cup v)-H(S)=\pi_v\{1+x_v(S)\},                          \tag{21}
\]

with the negative of the same expression for a removal.  Consequently the
fitness-two denominators in `(1)` cancel exactly:

\[
\begin{aligned}
LH(S)
&=\sum_{v\notin S}2\pi_vx_v(S)
 -\sum_{v\in S}\pi_v\{1-x_v(S)\}\\
&=2C(S)-C(S)=C(S).                                           \tag{22}
\end{aligned}
\]

This is the conductance-storage law.  Since

\[
 {1\over n}\sum_aH(\{a\})={1\over n},\qquad H(V)={3\over2}, \tag{23}
\]

testing the dual against the global function `H` gives

\[
 \boxed{\quad {1\over n}+\sum_Sy_SC(S)={3\over2}z.\quad}     \tag{24}
\]

Therefore the desired endpoint bound `(10)` is equivalent, inside the
rank-pair relaxation, to the sharp occupation-cut inequality

\[
 \sum_Sy_SC(S)
 \le {3\over2}{(n-1)2^{n-2}\over n(2^{n-1}-1)}-{1\over n}.   \tag{25}
\]

For rank-local use, define

\[
 X_k=\sum_{|S|=k}y_SH(S)U(S),\quad
 Y_k=\sum_{|S|=k}y_SH(S)D(S),\quad
 C_k=\sum_{|S|=k}y_SC(S).                                   \tag{26}
\]

The rank-weighted form of `(22)` is

\[
\begin{aligned}
L\{q_{|S|}H(S)\}
={}&H(S)\bigl[(q_{k+1}-q_k)U(S)
 +(q_{k-1}-q_k)D(S)\bigr]\\
&+C(S)\{2q_{k+1}-q_{k-1}\}.                                 \tag{27}
\end{aligned}
\]

Equating the coefficient of every `q_k` yields the full rank-cut
recurrence, including its endpoints:

\[
 \boxed{\quad
 {1_{\{k=1\}}\over n}+X_{k-1}+2C_{k-1}
 +Y_{k+1}-C_{k+1}-X_k-Y_k
 -{3z\over2}1_{\{k=n\}}=0.
 \quad}                                                       \tag{28}
\]

Here all absent boundary quantities are zero.  In particular,

\[
 {1\over n}+Y_2-C_2-X_1-Y_1=0,\qquad
 X_{n-1}+2C_{n-1}={3z\over2}.                                \tag{29}
\]

Summing `(28)` over `k` recovers `(24)`.

## 5. Relation to the two-labelled pin formulation

The cut in `(20)` is a literal two-label event: sample a stationary target
`v`, then a replacement request `i~P_v`, and ask whether exactly one of
`v,i` lies in the cache.  Formula `(21)` says that `H` stores the target
mark together with its internal request collision; `(22)` says its drift is
the cache/complement request cut.

This is the occupation-flow analogue of the standard common-pin response
written in terms of a marked request count and cache occupancy.  The
adjacent-rank terms `+2C_(k-1)` and `-C_(k+1)` in `(28)` are respectively
the mutant-addition and resident-restoration weights at fitness two.  The
remaining problem is to combine these cut terms with the arbitrary
one-mark balances `(14)` or `(17)`—possibly through a rank-dependent
reversible Poisson equation—to prove `(25)`.

## 6. A row-stochastic tangent/SOS decomposition

There is a second exact bridge which does not use reversibility.  For any
loopless row-stochastic kernel, put

\[
 \tau_i=\sum_vP_{vi},\qquad T(S)=\sum_{i\in S}\tau_i,
 \qquad e(S)=\sum_{v,i\in S}P_{vi},                            \tag{30}
\]

and, on the `k`-slice,

\[
 Z_k(S)={k(k-1)\over n-1}-e(S).                               \tag{31}
\]

The statistic `e` is a single symmetric pair statistic, since its
coefficient on the unordered pair `{i,j}` is `P_ij+P_ji`.  Also

\[
\sum_{v\in S}\left(x_v-{k-1\over n-1}\right)=-Z_k(S),
\]

\[
\sum_{v\notin S}\left(x_v-{k\over n-1}\right)
=T(S)-k+Z_k(S).                                               \tag{32}
\]

For the uncorrected optional potential `G_0(S)=1+k/n`, its cleared
submartingale drift is

\[
 B(S)=-{n+k-1\over n}U(S)+{2(n+k-2)\over n}D(S).              \tag{33}
\]

Define

\[
 \alpha_k={2(n-1)^2\over n(n+k-1)},\qquad
 \beta_k={4(n-1)^2\over n(n+k-2)},                            \tag{34}
\]

\[
 \gamma_k=\beta_k-\alpha_k
 ={2(n-1)^2(n+k)\over n(n+k-2)(n+k-1)}>0.                    \tag{35}
\]

Then the following identity is exact:

\[
\boxed{
\begin{aligned}
B(S)={}&-\alpha_k\{T(S)-k\}+\gamma_kZ_k(S)\\
&+\alpha_k\sum_{v\notin S}
 {\left(x_v-{k\over n-1}\right)^2\over1+x_v}
 +\beta_k\sum_{v\in S}
 {\left(x_v-{k-1\over n-1}\right)^2\over1+x_v}.
\end{aligned}}                                               \tag{36}
\]

Indeed, for `g(x)=2x/(1+x)`,

\[
g(x)=g(a)+{2(x-a)\over(1+a)^2}
-{2(x-a)^2\over(1+a)^2(1+x)},                                \tag{37}
\]

and substituting `a=k/(n-1)` outside and `a=(k-1)/(n-1)`
inside gives `(36)` using `(32)`.

Thus every non-SOS first-order error of the complete radial potential is
carried by exactly one vertex statistic, `T-k`, and one pair statistic,
`Z_k`.  This explains why the compressed numerical certificate with
arbitrary rank-labelled vertex corrections plus `e(S)` repairs the exact
additive Farkas obstruction.  It does not yet prove that the correction
drifts can absorb the first line of `(36)` at every state.

## 7. Optional Farkas currents and the exact endpoint ratio

The same relaxation has a useful current form after the standard optional
transform.  Put

\[
 Q(S)=2^{-|S|}G(S),\qquad G_0(S)=1+{|S|\over n}.              \tag{38}
\]

If `C` is a slice-quadratic correction with

\[
 C(\varnothing)=C(V)=0,qquad {1\over n}\sum_iC(\{i\})=0,    \tag{39}
\]

the positively cleared drift operator is

\[
\begin{aligned}
(\mathcal AC)(S)={}&\sum_{v\notin S}g_v
 \{C(S\cup v)-2C(S)\}\\
&+\sum_{v\in S}\ell_v
 \{4C(S\setminus v)-2C(S)\}.                               \tag{40}
\end{aligned}
\]

The base drift `mathcal A G_0` is `(33)`.  A Farkas obstruction to the
baseline certificate would be weights `eta_S>=0` on transient states such
that

\[
 \sum_S\eta_S(\mathcal AC)(S)=0                              \tag{41}
\]

for every correction `(39)`, while `sum_S eta_S B(S)<0`.
These optional Farkas weights are distinct from the Green pseudoflow `y` in
Sections 2--4 and have a free overall scale.

Set `eta_empty=eta_V=0`.  On the hypercube edge from a `k`-set `S` to
`T=S union {v}`, define the signed current

\[
 j(S,v)=\eta_Sg_v(S)-2\eta_T\ell_v(T)
 ={2\{\eta_Sx_v-\eta_T(1-x_v)\}\over1+x_v}.                  \tag{42}
\]

Pairing the two directions of every edge gives the exact identity

\[
 \boxed{\quad
 \sum_S\eta_S(\mathcal AC)(S)
 =\sum_{S,v\notin S}j(S,v)\{C(S\cup v)-2C(S)\}.
 \quad}                                                       \tag{43}
\]

Let `O_k` be the lower-end marginal of `j` on the `k`-slice and `I_k`
the upper-end marginal from interface `k-1`.  Equation `(41)` says

\[
 I_k(\phi)=2O_k(\phi)                                        \tag{44}
\]

for every degree-at-most-two slice test `phi` and `2<=k<=n-1`.
At rank one the same statement holds modulo the singleton boundary
constraint: there is a scalar `theta` such that

\[
 -2\eta_{\{i\}}-2O_1(\{i\})=\theta\quad\hbox{for every }i.   \tag{45}
\]

Write `J_k` for the total current on interface `k`, and put

\[
 R_1=\sum_i\eta_{\{i\}},\qquad
 A_{n-1}=\sum_{|S|=n-1}\eta_S.                              \tag{46}
\]

Then

\[
 J_0=-2R_1,qquad J_{n-1}=A_{n-1},                           \tag{47}
\]

\[
 J_{k-1}=2J_k\quad(2\le k\le n-1),                          \tag{48}
\]

and

\[
 J_0-2J_1=n\theta.                                           \tag{49}
\]

Since the edge increment of `G_0` is

\[
G_0(k+1)-2G_0(k)=-{n+k-1\over n},                            \tag{50}
\]

`(43)` and the finite geometric sum in `(48)` give

\[
\boxed{
 \sum_S\eta_SB(S)
 ={2(n-1)\over n}R_1
 -{(n+1)2^{n-1}-2n\over n}A_{n-1}.}                          \tag{51}
\]

Consequently the exact remaining endpoint-current inequality is

\[
\boxed{
 {A_{n-1}\over R_1}
 \le {2(n-1)\over (n+1)2^{n-1}-2n}.}                         \tag{52}
\]

There is no normalization `A_(n-1)+R_1=1` in this Farkas formulation.
Equation `(52)` is scale invariant and exactly matches the endpoint ratio
found in the rank-dependent additive Farkas audit.

The reversible storage gives a further exact current recurrence.  Define

\[
 h_k=O_k(H),\qquad c_k=\sum_{|S|=k}\eta_SC(S).                \tag{53}
\]

Using `(21)`, `(42)`, and `(44)` gives

\[
 2h_{k+1}=h_k+2(c_k-c_{k+1})\quad(1\le k\le n-2).            \tag{54}
\]

At rank one,

\[
 h_1=-c_1-\theta/2,qquad
 h_1+2c_1=c_1+{R_1+J_1\over n}.                              \tag{55}
\]

At the upper boundary,

\[
 H(V\setminus v)+2C(V\setminus v)={3\over2},                \tag{56}
\]

so iteration of `(54)` yields

\[
\boxed{
 {3A_{n-1}\over2}
 ={c_1+(R_1+J_1)/n\over2^{n-2}}
 +\sum_{k=2}^{n-1}{c_k\over2^{n-1-k}},
 \qquad J_1=2^{n-2}A_{n-1}.}                                \tag{57}
\]

Every `c_k` is nonnegative.  Therefore `(57)` by itself gives a lower,
not an upper, endpoint estimate.  A proof of `(52)` must use the remaining
individual one-mark/two-mark balances to upper-control the weighted cut
production in `(57)`.

## 8. Exact scope

- **PROVED:** the finite LP dual `(7)--(9)` and the moment recurrences
  `(12)`, `(14)`, `(15)`.
- **PROVED:** the conductance-storage identity `(22)`, its global occupation
  law `(24)`, and its full rank recurrence `(28)`.
- **PROVED:** the row-stochastic tangent/SOS decomposition `(36)`; its only
  linear defects are temperature and the single internal-flow pair moment.
- **PROVED:** the optional edge-current factorization `(42)--(43)`, the
  exact endpoint ratio `(51)--(52)`, and the boundary-aware cut-production
  identity `(57)`.
- **EXACTLY VERIFIED:** an independent rational implementation checks these
  identities and the dual balances on small weighted graphs, and checks
  `(36)` on a genuinely directed rational kernel.
- **NUMERICALLY OBSERVED ONLY:** the full rank-pair primal has remained below
  the complete baseline in the hostile searches in this directory.
- **OPEN:** the universal cut bound `(25)`, hence universal feasibility of
  the rank-pair certificate and the universal fitness-two fixation theorem.
