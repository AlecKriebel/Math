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

### 7.1 The weighted cut is an exact optional coboundary

The geometric weights in `(57)` are forced by a simpler exact identity.
Put `N=n-1` and

\[
 q_k=2^{k-N-1}.                                                \tag{58}
\]

Then `q_(k+1)=2q_k`, `q_(k-1)=q_k/2`, so every holding term in the
rank-weighted storage formula cancels.  In the optional normalization,

\[
 \boxed{\quad
 \mathcal A\{q_{|S|}H(S)\}=2^{|S|-N}C(S).
 \quad}                                                        \tag{59}
\]

Thus the geometrically weighted cut reward is already an exact drift.  It
cannot itself be used as the correction because its boundary data are

\[
 q_0H(\varnothing)=0,\qquad q_nH(V)={3\over2},
 \qquad {1\over n}\sum_iq_1H(\{i\})={q_1\over n}.             \tag{60}
\]

Equivalently, a Bellman certificate for the weighted cut bound is a
slice-linear-plus-conductance boundary extension `R` with the data `(60)`
and

\[
 \mathcal AR(S)\le0\quad(|S|\ge2),\qquad
 \mathcal AR(S)\le\Lambda_n\quad(|S|=1),                     \tag{61}
\]

where `Lambda_n` is the complete weighted-cut value.  Then
`C=qH-R` is an admissible zero-boundary correction and `(59)` proves the
dual reward bound.

The most direct radial extension in `(61)` reduces exactly to the already
refuted rank-dependent additive route.  Hence `(59)` explains both facts
seen computationally: one conductance statistic is the natural storage
variable, but its fixed geometric coefficient is insufficient; an
additional zero-boundary rank profile of `H`, together with the arbitrary
vertex corrector, is essential.  Section 7.4 upgrades this last statement
from discovery evidence to an exact Farkas refutation, even when every rank
constant and every rank-labelled vertex corrector is retained.

### 7.2 Geometric conjugacy back to the Green pseudoflow

The geometric coboundary is part of an exact conjugacy, not merely an
isolated identity.  Let `eta` be a full rank-pair optional Farkas weight and
retain the notation `A_(n-1),R_1,theta` of `(45)--(49)`.  Define

\[
 q_k=2^{k-n},\qquad
 \mu_S=2q_{|S|}\eta_S,\qquad
 I=A_{n-1}+2^{2-n}R_1.                                    \tag{62}
\]

For every slice-quadratic function `F`, with `F(empty)=0`, geometric
conjugacy gives the pointwise identity

\[
 \mathcal A\{q_{|S|}F(S)\}=2q_{|S|}LF(S).                 \tag{63}
\]

The boundary functional of the optional current is

\[
 \sum_S\eta_S\mathcal A(qF)(S)
 =A_{n-1}F(V)+\theta q_1\sum_iF(\{i\}).                    \tag{64}
\]

Since `(49)` gives

\[
 -n\theta q_1=A_{n-1}+2^{2-n}R_1=I,                       \tag{65}
\]

the normalized weights `bar(mu)=mu/I` obey

\[
 \boxed{
 {1\over n}\sum_iF(\{i\})+
 \sum_S\bar\mu_SLF(S)-zF(V)=0,
 \qquad z={A_{n-1}\over I}.}                              \tag{66}
\]

Thus a full optional rank-pair obstruction is exactly a nonnegative
degree-two Green pseudoflow after geometric reweighting.  Moreover,

\[
 {A_{n-1}\over R_1}
 \le {2(n-1)\over (n+1)2^{n-1}-2n}
 \quad\Longleftrightarrow\quad
 z\le{(n-1)2^{n-2}\over n(2^{n-1}-1)}.                    \tag{67}
\]

This removes the apparent sign mismatch at the bottom current: the
singleton defect is precisely the uniform source of total mass `I`.

There is a compact matrix form of every one- and two-mark balance.  Write
`s` for the zero-one column vector of `S`, and put

\[
 d_v(S)=(1-s_v)g_v(S)-s_v\ell_v(S),\qquad
 t_v(S)=(1-s_v)g_v(S)+s_v\ell_v(S)=(1-2s_v)d_v(S).
\]

Since `Ls=d` and

\[
 L(ss^T)=sd^T+ds^T+\operatorname{Diag}(t),
\]

equation `(66)` is equivalent at degree two to

\[
 \boxed{
 \sum_S\bar\mu_S
 \{sd^T+ds^T+\operatorname{Diag}(t)\}
 =z\mathbf1\mathbf1^T-{1\over n}I_n.}                    \tag{68}
\]

In particular, for every `a` with `sum_i a_i=0`,

\[
 \sum_S\bar\mu_S\left[
 2(a\mathbin\cdot s)(a\mathbin\cdot d)+
 \sum_vt_va_v^2\right]
 =-{\|a\|_2^2\over n}.                                    \tag{69}
\]

Equation `(69)` is the exact two-marked collision/variance budget carried
by the rank-pair relaxation.  The now-refuted rank-plus-vertex-plus-`H`
compression retained only its conductance contraction, whereas the full
rank-pair conjecture retains the entire matrix identity `(68)`.

### 7.3 Selection gain versus reversible collision cut

The matrix formulation exposes one further sharp local inequality.  Put

\[
 a_v(S)={x_v(S)\{1-x_v(S)\}\over1+x_v(S)}.
\]

Then the mutant-indicator drift has the exact neutral-plus-selection split

\[
 d=(P-I)s+a.                                                \tag{70}
\]

For stationary mutant mass `M(S)=pi(S)`, reversibility (indeed only
stationarity of `pi`) therefore gives

\[
 LM(S)=Q(S):=\sum_v\pi_va_v(S)\ge0.                         \tag{71}
\]

On the other hand `LH=C`.  Testing `(66)` with `M` and `H` gives

\[
 \sum_S\bar\mu_SQ(S)=z-{1\over n},\qquad
 \sum_S\bar\mu_SC(S)={3z\over2}-{1\over n}.              \tag{72}
\]

The scalar function `a(x)=x(1-x)/(1+x)` is strictly concave on `[0,1]`.
Conditioning the stationary target first on `v notin S` and then on
`v in S`, and using the two oriented cut identities

\[
 \sum_{v\notin S}\pi_vx_v=C,
 \qquad
 \sum_{v\in S}\pi_v(1-x_v)=C,
\]

gives the sharp statewise Jensen bound

\[
 \boxed{
 {Q(S)\over C(S)}\le
 {1-M(S)-C(S)\over1-M(S)+C(S)}
 +{M(S)-C(S)\over2M(S)-C(S)}.}                             \tag{73}
\]

For a connected graph and a transient nonempty proper set, all denominators
in `(73)` are positive.  Equality holds exactly when `x_v(S)` is constant
over `S` and constant over its complement (with respect to the positive
stationary weights).  In particular every complete-graph rank attains
equality.

Finally, put

\[
 \kappa_n=
 {2\{(n-3)2^n+4\}\over(3n-7)2^n+8}.                       \tag{74}
\]

Because the ratio of the two quantities in `(72)` is strictly increasing
in `z>=1/n`, the exact endpoint theorem is equivalently the summed
selection-gain/collision inequality

\[
 \boxed{
 \sum_S\bar\mu_SQ(S)
 \le\kappa_n\sum_S\bar\mu_SC(S).}                         \tag{75}
\]

The complete pseudoflow has equality in `(75)`.  Bound `(73)` alone does
not prove `(75)`: its right side tends to `3/2` across a vanishing
conductance cut, while `kappa_n<2/3`.  The genuinely open ingredient is
therefore an all-rank two-marked flow inequality, not a pointwise or
per-rank cut estimate.

There is also an exact positive-semidefinite representation of the local
gain.  Let `p_v` denote row `v` of `P`, let `Pi=Diag(pi)`, and define the
categorical covariance matrices and their state-dependent mixture by

\[
 D_v=\operatorname{Diag}(p_v)-p_v^Tp_v,qquad
 K_S=\sum_v{\pi_v\over1+x_v(S)}D_v.                          \tag{76}
\]

Every `D_v` is positive semidefinite and annihilates `mathbf1`, and

\[
 \boxed{
 Q(S)=s^TK_Ss
 ={1\over2}\sum_{v,i,j}{\pi_vP_{vi}P_{vj}\over1+x_v(S)}
 (s_i-s_j)^2.}                                             \tag{77}
\]

If `K_0=sum_v pi_vD_v`, stationarity and reversibility give

\[
 K_S\preceq K_0=\Pi-P^T\Pi P\preceq2L_\pi,
 \qquad L_\pi=\Pi(I-P),                                   \tag{78}
\]

where the second comparison is the explicit square

\[
 2L_\pi-K_0=(I-P)^T\Pi(I-P)\succeq0.                       \tag{79}
\]

For zero-one `s`, the associated scalar law of total variance sharpens the
resulting `Q<=2C` bound to the exact SOS decomposition

\[
 \boxed{
 2C(S)-Q(S)=\sum_v\pi_v\left[
 (s_v-x_v)^2+{x_v^2(1-x_v)\over1+x_v}
 \right]\ge0.}                                             \tag{80}
\]

Equations `(76)--(80)` are the promised two-request collision squares.
They are graph-independent and exact, but their factor two is not the sharp
all-rank constant in `(75)`; the missing gain is the transport of this PSD
budget between ranks and the two absorbing boundaries.

### 7.4 Exact failure of one global conductance coefficient

The smallest compressed conjecture suggested by `(59)` is now exactly
decided.  In the original fixation coordinates, allow

\[
 F(S)=a_{|S|}+\sum_{v\in S}b_{|S|,v}+\lambda E_\pi(S),       \tag{81}
\]

with arbitrary rank constants, arbitrary rank-labelled vertex
coefficients, and one scalar `lambda` shared by all ranks.  The 17-vertex
complete-support graph with class sizes `(2,5,10)` and class-edge weights

\[
 \begin{pmatrix}20000000&15&5\\15&9&4500\\5&4500&150\end{pmatrix}
\]

has the exact restricted optimum

\[
 p_{\rm glob}=0.4767015236181397039926\ldots
 >{524288\over1114095}
 =\rho_{\rm dB}(K_{17},2).                                 \tag{82}
\]

The proof is an exact 49-state positive Farkas ray in the 196-state
`S_2 x S_5 x S_10` quotient, together with an independently reconstructed
matching primal potential whose 196 drift inequalities are checked over the
rationals.  See `GLOBAL_CONDUCTANCE_FARKAS_REFUTATION.md` and
`verify_global_conductance_farkas_refutation.py`.

The graph itself is dB-suppressing at fitness two.  Hence `(82)` refutes
only the compressed certificate `(81)`, not the endpoint fixation theorem.
The stronger version with an independent conductance coefficient on every
rank is decided separately in Section 7.9.

### 7.5 Exact audit of the fixed collision-matrix contractions

The matrix balance `(68)` can be contracted with `L_pi` and `K_0` exactly.
This determines what those two fixed PSD tests do and do not provide.
Write `mathscr L` for the evolutionary generator in this subsection, to
distinguish it from the conductance Laplacian `L_pi`.

For `K=L_pi`, the quadratic form is `s^TKs=C(S)`, `K1=0`, and
`Tr(K)=1`.  Thus `(68)` gives

\[
 \sum_S\bar\mu_S\mathscr LC(S)=-{1\over n}.                 \tag{83}
\]

But `C=3M-2H`, `mathscr LM=Q`, and `mathscr LH=C`, so pointwise

\[
 \boxed{\mathscr LC=3Q-2C.}                                \tag{84}
\]

Consequently `(83)` is exactly the linear combination of the two boundary
identities `(72)`.  The constant `L_pi` contraction adds no new inequality.

For `K=K_0=Pi-P^TPi P`, put

\[
 R_0(S)=s^TK_0s=\sum_v\pi_vx_v(1-x_v),
 \qquad
 \chi=\sum_{v,i}\pi_vP_{vi}^2.                             \tag{85}
\]

Then `K_01=0` and `Tr(K_0)=1-chi`, hence

\[
 \boxed{
 \sum_S\bar\mu_S\mathscr LR_0(S)=-{1-\chi\over n}.}      \tag{86}
\]

Looplessness and rowwise Cauchy--Schwarz give the sharp collision bound

\[
 \chi\ge{1\over n-1},                                     \tag{87}
\]

with equality only when every row is uniform on the other `n-1` vertices,
that is, at the complete kernel.

The new drift in `(86)` has an exact two-step response form.  Reversibility
gives `P^TPi P=Pi P^2`; with `d,t` from `(68)`, define

\[
 \mathcal J_2(S)=
 2(\Pi P^2s)\mathbin\cdot d
 +\sum_i\pi_i(P^2)_{ii}t_i.                                \tag{88}
\]

Then

\[
 \boxed{\mathscr LR_0=Q-\mathcal J_2,\qquad
 \sum_S\bar\mu_S\mathcal J_2=z-{\chi\over n}.}           \tag{89}
\]

Neither term in `(89)` has a statewise sign.  On the exact four-vertex
weighted cycle used by the rational verifier, `mathcal J_2=3604/11025>0`
at `S={0,1}`, but `mathcal J_2=-107/3024<0` at `S={2}`; correspondingly
`mathscr LR_0` also has both signs.  Thus PSD of `K_0` does not turn `(86)`
into a direct gain/cut comparison.

For completeness, the entire rank-dependent information supplied by a
fixed symmetric matrix `K` with `K1=0` can be written explicitly.  Put

\[
 R_K(S)=s^TKs,
\]

\[
 \Delta^+_{K,v}=2(Ks)_v+K_{vv},\qquad
 \Delta^-_{K,v}=-2(Ks)_v+K_{vv}.                           \tag{90}
\]

For an arbitrary rank sequence `r_k`,

\[
\begin{aligned}
 \mathscr L\{r_kR_K(S)\}={}&R_K(S)
 [(r_{k+1}-r_k)U+(r_{k-1}-r_k)D]\\
 &+r_{k+1}\sum_{v\notin S}g_v\Delta^+_{K,v}
 +r_{k-1}\sum_{v\in S}\ell_v\Delta^-_{K,v}.              \tag{91}
\end{aligned}
\]

Testing the pseudoflow gives the exact integrated recurrence

\[
 {r_1\operatorname{Tr}K\over n}
 +\sum_S\bar\mu_S\mathscr L\{r_{|S|}R_K(S)\}=0.           \tag{92}
\]

For constant `r`, positivity of the diagonal carré term yields only

\[
 \sum_S\bar\mu_Ss^TKd\le-{\operatorname{Tr}K\over2n}.     \tag{93}
\]

Equations `(91)--(93)` are the strongest sign consequence obtained from
the fixed-matrix contraction using PSD alone.  To reach `kappa_n`, a proof
must control the signed mixed increments in `(91)` after summation against
the one-mark balances.  The exact counterexamples in Sections 7.4 and 7.9
show that neither constant nor arbitrary rank-dependent multipliers of
`L_pi` suffice.  At this stage the combined rank-dependent `L_pi,K_0`
problem was the next candidate; Section 7.13 refutes that compressed space
exactly.

### 7.6 The exact compressed dual and rank-dependent witness repairs

Let `W_H` contain the rank constants, all rank-labelled vertex functions,
and one independent coefficient of `H` on every rank:

\[
 F(S)=a_k+\sum_{i\in S}b_{k,i}+q_kH(S).                    \tag{94}
\]

Since the mass part of `H` already lies in the vertex span, this is the
same space as using one rank-dependent internal-conductance coefficient.
The dual of `(94)` has a particularly small exact description: it consists
of nonnegative `y_S` satisfying the rank-mass equations `(12)`, every
one-mark equation `(14)`, and the single rank-storage equation `(28)` for
each rank.  Conversely those equations annihilate every function in
`W_H`, so this description loses nothing.  Thus the rank-`H` compressed
universal question was

\[
 \boxed{(12),(14),(28),\ y\ge0\quad\Longrightarrow\quad
 z\le\rho_{\rm dB}(K_n,2).}                                \tag{95}
\]

This system exactly repairs the graph which refutes one global coefficient,
but Section 7.9 gives a different graph which refutes `(95)` itself.
On the 17-vertex graph in Section 7.4, its 196-state symmetry quotient has
dimension 63.  A 62-state strictly positive rational dual solution and a
matching rational primal give

\[
 p_{\rm rank-H}=0.463075851135221216402749\ldots
 <{524288\over1114095},                                    \tag{96}
\]

with exact margin
`0.00751956487508311132513730...`.  Every quotient drift inequality is
checked over the rationals by
`verify_rank_dependent_conductance_witness.py`.  This remains a useful exact
finite repair, but it is not a universal result.

There is an equally compact rank recurrence for the collision matrix
`K_0`.  For a fixed symmetric `K` with `K1=0`, define

\[
 X^K_k=\sum_{|S|=k}\bar\mu_SR_K(S)U(S),\qquad
 Y^K_k=\sum_{|S|=k}\bar\mu_SR_K(S)D(S),                    \tag{97}
\]

\[
 P^K_k=\sum_{|S|=k}\bar\mu_S\sum_{v\notin S}g_v
       \Delta^+_{K,v},\qquad
 N^K_k=\sum_{|S|=k}\bar\mu_S\sum_{v\in S}\ell_v
       \Delta^-_{K,v}.                                    \tag{98}
\]

Taking the coefficient of an arbitrary rank multiplier in `(92)` gives

\[
 \boxed{
 {\operatorname{Tr}K\over n}1_{\{k=1\}}
 +X^K_{k-1}+P^K_{k-1}+Y^K_{k+1}+N^K_{k+1}
 -X^K_k-Y^K_k=0.}                                         \tag{99}
\]

All absent terms are zero; the formally redundant `k=n` equation cancels
because `R_K(V)=0`.  For `K=K_0`, the source in `(99)` is
`(1-chi)/n`.  Also, pointwise,

\[
 Q(S)\le R_0(S),\qquad
 R_0(S)-Q(S)=\sum_v{\pi_vx_v^2(1-x_v)\over1+x_v}\ge0.     \tag{100}
\]

The occupation inequality obtained by discarding the remainder in `(100)`
is too weak.  On the exact four-vertex verifier graph,

\[
 {\sum_S\bar\mu_SR_0(S)\over\sum_S\bar\mu_SC(S)}
 ={3763047422347\over5888649661090}>{5\over11}=\kappa_4. \tag{101}
\]

Hence any `K_0` proof must use the rank transport `(99)` and the positive
remainder in `(100)`, not merely `Q<=R_0`.  As a finite check, the
rank-constant plus rank-vertex plus rank-`K_0` space also closes the exact
17-vertex witness, with rational optimum

\[
 p_{\rm rank-K_0}=0.439476931794796785748626\ldots
 <{524288\over1114095}.                                    \tag{102}
\]

The independent exact replay is
`verify_rank_dependent_k0_witness.py`.  The universal implication from
`(99)--(100)` remains open.

### 7.7 Minimal oriented current and gradient form of the combined route

The `L_pi` rank contraction becomes more informative before its two
orientations are summed.  Split the gain at rank `k` into

\[
 Q_k^+=\sum_{|S|=k}\bar\mu_S\sum_{v\notin S}
 {\pi_vx_v(1-x_v)\over1+x_v},\qquad
 Q_k^-=\sum_{|S|=k}\bar\mu_S\sum_{v\in S}
 {\pi_vx_v(1-x_v)\over1+x_v}.                              \tag{103}
\]

For a single state, the response parts of the `M` and `C` drifts obey the
four exact identities

\[
 \begin{array}{c|cc}
 &\hbox{addition}&\hbox{removal}\\ \hline
 M&C+Q^+&Q^--C\\
 C&3Q^+-C&3Q^--C.
 \end{array}                                                \tag{104}
\]

For example,
`2x(1-2x)/(1+x)=3x(1-x)/(1+x)-x`; the other three identities
are equally direct.  Put

\[
 X^M_k=\sum_{|S|=k}\bar\mu_SM(S)U(S),\quad
 Y^M_k=\sum_{|S|=k}\bar\mu_SM(S)D(S),
\]

and define `X^C_k,Y^C_k` in the same way with `C(S)`.  The rank-labelled
stationary-mass tests and rank-labelled cut tests are then exactly

\[
\begin{aligned}
0={}&{1_{\{k=1\}}\over n}
 +X^M_{k-1}+C_{k-1}+Q^+_{k-1}
 +Y^M_{k+1}+Q^-_{k+1}-C_{k+1}\\
&-X^M_k-Y^M_k-z1_{\{k=n\}},                                \tag{105}
\end{aligned}
\]

\[
\begin{aligned}
0={}&{1_{\{k=1\}}\over n}
 +X^C_{k-1}+3Q^+_{k-1}-C_{k-1}
 +Y^C_{k+1}+3Q^-_{k+1}-C_{k+1}\\
&-X^C_k-Y^C_k.                                              \tag{106}
\end{aligned}
\]

These equations include the endpoint cancellations, with absent terms set
to zero.  Summing `(106)` gives `(83)--(84)`, but `(105)--(106)` retain the
signed adjacent-rank information destroyed by the fixed contraction.  The
elementary pointwise cone is

\[
 0\le Q^+\le C,\qquad 0\le Q^-\le {C\over2}.               \tag{107}
\]

The combined `H,K_0` route has a still cleaner positive form.  Define

\[
 \mathcal D(S)=2C(S)-R_0(S)
 =s^T(I-P)^T\Pi(I-P)s
 =\sum_v\pi_v(s_v-x_v)^2,                                  \tag{108}
\]

\[
 \mathcal W(S)=\sum_v{\pi_vx_v^2(1-x_v)\over1+x_v}.        \tag{109}
\]

Then `(80)` is precisely

\[
 \boxed{2C-Q=\mathcal D+\mathcal W,\qquad
        \mathcal D,\mathcal W\ge0.}                        \tag{110}
\]

Rank-dependent `H` and `K_0` coefficients retain `C` and `D` on
every rank.  Therefore the sharp endpoint problem is equivalently the
integrated coercivity inequality

\[
 \boxed{
 (2-\kappa_n)\sum_S\bar\mu_SC(S)
 \le\sum_S\bar\mu_S\{\mathcal D(S)+\mathcal W(S)\}.}       \tag{111}
\]

This is the minimal positive target found by the contraction audit.  The
term `D` is the reversible one-step prediction-error energy tracked
by the combined quadratic certificate; `W` is its nonnegative
fitness-two remainder.  What remains open is a rank-current coercivity
argument proving `(111)` from the **full** two-marked flow.  Section 7.13
shows that even retaining the individual vertex recurrences together with
the two scalar `H,K_0` contractions does not force it.  Dropping the
individual vertex recurrences and keeping only the scalar bounds
`(105)--(107)` is still weaker.

That last obstruction is exact.  Even if the scalar system is augmented by
all elementary event-moment bounds

\[
 0\le X^M_k\le A_k,quad0\le Y^M_k\le R_k,quad
 0\le X^C_k\le\min(X^M_k,A_k-X^M_k),                        \tag{112}
\]

\[
 0\le Y^C_k\le\min(Y^M_k,R_k-Y^M_k),                       \tag{113}
\]

and by the exact singleton/top identities, it admits at `n=3` the rational
point `z=5/9`, whereas the complete baseline is `4/9`.  The complete list of
rational coordinates and an exact replay are in
`verify_oriented_scalar_cone_refutation.py`.  This point is deliberately
**not** claimed to arise from a graph or a pseudoflow; it proves only that
vertex-forgetting destroys indispensable constraints.

### 7.8 Internal-conductance creation and excursion debt

The rank-`H` route alone has an especially simple storage interpretation.
Recall that `E=H-M` is internal stationary conductance.  Equations `(22)`
and `(71)` give the pointwise identity

\[
 \boxed{LE=C-Q.}                                             \tag{114}
\]

Resolve its two orientations by putting

\[
 P(S)=C(S)-Q^+(S)
 =\sum_{v\notin S}{2\pi_vx_v^2\over1+x_v}\ge0,\qquad
 N(S)=Q^-(S)\ge0.                                           \tag{115}
\]

Thus an addition creates internal conductance at rate `P`, while a removal
destroys it at rate `N`, and `LE=P-N`.  Write
`P_k=sum_(|S|=k) bar(mu)_S P(S)` and similarly for `N_k`.  If

\[
 X^E_k=\sum_{|S|=k}\bar\mu_SE(S)U(S),\qquad
 Y^E_k=\sum_{|S|=k}\bar\mu_SE(S)D(S),                       \tag{116}
\]

then the exact rank recurrence is

\[
 \boxed{
 X^E_{k-1}+P_{k-1}+Y^E_{k+1}-N_{k+1}
 -X^E_k-Y^E_k-{z\over2}1_{\{k=n\}}=0.}                    \tag{117}
\]

There is no singleton source because `E({i})=0`; the top term is `z/2`
because `E(V)=1/2`.  Summing gives

\[
 \sum_k(P_k-N_k)={z\over2}.                                \tag{118}
\]

Consequently the endpoint theorem is equivalently

\[
 \boxed{
 (1-\kappa_n)\sum_S\bar\mu_SC(S)
 \le\sum_k(P_k-N_k).}                                      \tag{119}
\]

This is the sharp creation-versus-excursion-debt form of the compressed
rank-`H` implication `(95)`.  It explains why a prefix argument which ignores
debt can fail: `P,N` are separately nonnegative, but only their all-rank
difference is fixed by the boundary.  Section 7.9 shows that even the full
rank-`H` plus arbitrary one-mark system does not control that debt strongly
enough.  The identity remains useful as one component of the combined
rank-`H,K_0` route, but it cannot close the endpoint alone.

### 7.9 Exact failure of rank-dependent conductance plus all one-marks

The implication `(95)` is exactly false.  Take the nine-vertex graph with
five equitable classes of sizes `(1,1,2,2,3)` and class-edge weights

\[
\begin{pmatrix}
10^9&10^{22}&2\,10^9&5\,10^{10}&3000\\
10^{22}&10^9&4\,10^8&2500000000&1\\
2\,10^9&4\,10^8&4\,10^{16}&45\,10^{15}&450000\\
5\,10^{10}&2500000000&45\,10^{15}&4\,10^8&1750000000\\
3000&1&450000&1750000000&8\,10^9
\end{pmatrix}.                                             \tag{120}
\]

Every intervertex weight is positive.  The exact quotient has 142 transient
states, and the invariant rank-constant plus rank-vertex plus rank-`H`
function space has dimension 47.  A 46-state strictly positive rational
Farkas ray and an independently reconstructed matching rational primal give

\[
 p_{\rm rank-H}
 =0.4463122484779187239833287\ldots,                       \tag{121}
\]

whereas

\[
 \rho_{\rm dB}(K_9,2)={1024\over2295}
 =0.44618736383442265795\ldots.                            \tag{122}
\]

Thus

\[
 \boxed{p_{\rm rank-H}-\rho_{\rm dB}(K_9,2)
 =0.0001248846434960660312589405\ldots>0.}                \tag{123}
\]

The reduced exact gap has a 2875-digit numerator and 2879-digit denominator;
the SHA-256 identifier of canonical `numerator/denominator` text is
`54157ebc0d0153a2d86dc928f47495f688d2104b3971ff5cf0127e838ccb9f76`.
The verifier checks the sign by integer comparison, reconstructs both sides
of strong duality, audits all 142 drift inequalities, and independently
checks every labelled-to-quotient row.  See
`RANK_DEPENDENT_CONDUCTANCE_FARKAS_REFUTATION.md` and
`verify_rank_dependent_conductance_farkas_refutation.py`.

This is a route counterexample only; it is not a fixation counterexample.
It proves that one reversible pair direction per rank is insufficient even
with every rank-labelled vertex correction.  The smallest surviving
compressed candidate at this point contained both rank-`H` and rank-`K_0`;
Section 7.13 refutes that candidate too, leaving the full rank-pair matrix.

### 7.10 The combined route as two internal-request flows

The available vertex fields remove the diagonal of any quadratic form.
For a symmetric `K` with `K1=0`, put

\[
 R_K^\circ(S)=s^TKs-\sum_iK_{ii}s_i
 =2\sum_{i<j}K_{ij}s_is_j.                                 \tag{124}
\]

Thus `R_K` and `R_K^circ` generate the same rank-constant plus rank-vertex
plus rank-quadratic potential space.  This gauge makes the combined pair
directions literal internal flows.  Define

\[
 c_{ij}=\pi_iP_{ij},\qquad
 q_{ij}=(P^T\Pi P)_{ij}=\sum_v\pi_vP_{vi}P_{vj}\quad(i\ne j), \tag{125}
\]

and

\[
 E_1(S)=\sum_{i<j}c_{ij}s_is_j,qquad
 E_2(S)=\sum_{i<j}q_{ij}s_is_j.                             \tag{126}
\]

The first statistic records a target--request internal edge; the second
records two independent requests from one stationary target.  Both edge
systems are symmetric and nonnegative.  Modulo vertex fields,

\[
 s^TL_\pi s\equiv-2E_1(S),\qquad
 s^TK_0s\equiv-2E_2(S).                                    \tag{127}
\]

Consequently the live combined restricted primal has the exact function
space

\[
 \mathcal W_{12}=\bigoplus_k
 \operatorname{span}\{1,s_1,\ldots,s_n,E_1,E_2\}\big|_{|S|=k}. \tag{127a}
\]

There are no hidden pair constraints in this description.  Finite LP
duality says that its optimum is the maximum `z` over nonnegative
pseudoflows satisfying exactly the rank-mass equations `(12)`, all
rank-labelled one-mark equations `(14)`, and the two storage rows `(132)`
below.  Thus the exact two-channel compressed conjecture is precisely

\[
 (12),(14),(132),\ \bar\mu\ge0
 \quad\Longrightarrow\quad z\le\rho_{\rm dB}(K_n,2).       \tag{127b}
\]

This is strictly stronger than the refuted rank-`H` implication `(95)` and
strictly weaker than retaining the full pair matrix `(68)`.

Write `x=Ps`, `y=P^2s`, and `r_v=(P^2)_(vv)`.  Reversibility gives
`q_(vi)=pi_v(P^2)_(vi)`.  Hence, on an upward edge with `v notin S`,

\[
 E_1(S\cup v)-E_1(S)=\pi_vx_v,qquad
 E_2(S\cup v)-E_2(S)=\pi_vy_v.                             \tag{128}
\]

For a removal from a state containing `v`, the lost amounts are
`pi_vx_v` and `pi_v(y_v-r_v)`, respectively.  The latter is nonnegative
because it is the sum of `q_(vi)` over the other mutants.  Consequently the
two storage drifts split into nonnegative creation and debt terms:

\[
 LE_a=P_a-N_a\qquad(a=1,2),                                \tag{129}
\]

where

\[
\begin{aligned}
 P_1(S)&=\sum_{v\notin S}{2\pi_vx_v^2\over1+x_v},&
 N_1(S)&=\sum_{v\in S}{\pi_vx_v(1-x_v)\over1+x_v},\\
 P_2(S)&=\sum_{v\notin S}{2\pi_vx_vy_v\over1+x_v},&
 N_2(S)&=\sum_{v\in S}{\pi_v(1-x_v)(y_v-r_v)\over1+x_v}.
\end{aligned}                                               \tag{130}
\]

The first line agrees with `(115)`.  Put
`chi=sum_(v,i)pi_vP_(vi)^2`.  The exact boundary data are

\[
 E_1(\varnothing)=E_2(\varnothing)=E_1(\{i\})=E_2(\{i\})=0,
\quad E_1(V)={1\over2},\quad E_2(V)={1-\chi\over2}.        \tag{131}
\]

For `a=1,2`, define the rank occupations `X^a_k,Y^a_k` by replacing `E`
with `E_a` in `(116)`, and let `P^a_k,N^a_k` be the corresponding
occupations of `(130)`.  Every feasible two-moment pseudoflow therefore
obeys the vector recurrence

\[
\boxed{
 \binom{X^1_{k-1}+P^1_{k-1}+Y^1_{k+1}-N^1_{k+1}-X^1_k-Y^1_k}
       {X^2_{k-1}+P^2_{k-1}+Y^2_{k+1}-N^2_{k+1}-X^2_k-Y^2_k}
 ={z\over2}\binom{1}{1-\chi}1_{\{k=n\}}.}                \tag{132}
\]

All absent terms vanish.  Summation over rank gives

\[
 \sum_k(P^1_k-N^1_k)={z\over2},\qquad
 \sum_k(P^2_k-N^2_k)={z(1-\chi)\over2}.                   \tag{133}
\]

This immediately exposes a sharp complete-kernel deficit.  Rowwise
Cauchy--Schwarz and looplessness give

\[
 \chi-{1\over n-1}
 =\sum_v\pi_v\sum_{i\ne v}\left(P_{vi}-{1\over n-1}\right)^2
 \ge0.                                                     \tag{134}
\]

Combining `(133)--(134)`,

\[
\boxed{
 \sum_k(P^2_k-N^2_k)
 \le {n-2\over n-1}\sum_k(P^1_k-N^1_k),}                 \tag{135}
\]

with exact gap

\[
 {z\over2}\left(\chi-{1\over n-1}\right).               \tag{136}
\]

Equality holds exactly when every row is uniform on the other `n-1`
vertices, namely at the complete kernel.

The fixed-matrix pencil requested by the contraction route now has two
complementary interpretations:

\[
 K(\theta)=L_\pi+\theta K_0,qquad
 R_{K(\theta)}^\circ=-2(E_1+\theta E_2).                   \tag{137}
\]

For `theta>=0`, it is the graph Laplacian with edge conductances
`c_(ij)+theta q_(ij)`, hence an `M`-matrix.  More generally, if
`widehat P=Pi^(1/2)P Pi^(-1/2)`, then

\[
 K(\theta)=\Pi^{1/2}(I-\widehat P)
 [I+\theta(I+\widehat P)]\Pi^{1/2},                        \tag{138}
\]

so `K(theta)` is positive semidefinite for every reversible kernel whenever
`theta>=-1/2`; this universal range is sharp by nearly disconnected
kernels.  For `theta>=0`, put `E_theta=E_1+theta E_2` and similarly
`P_theta,N_theta`.  The exact rank-profile formula is

\[
\begin{aligned}
 L\{u_kE_\theta(S)\}={}&E_\theta(S)
 [(u_{k+1}-u_k)U+(u_{k-1}-u_k)D]\\
 &+u_{k+1}P_\theta(S)-u_{k-1}N_\theta(S).                 \tag{139}
\end{aligned}
\]

Here every storage, creation, and debt term is nonnegative.  Equation
`(139)` is the exact two-channel `M`-matrix/Schur starting point.  Its total
collision deficit `(135)` is sharp, but totals alone do not prove `(119)`:
the remaining obligation is a rankwise coupling which transports the
`N_1` debt using the second channel and the arbitrary one-mark balances.
No such sign is claimed here.

### 7.11 The boundary-neutral Schur mode is traceless and indefinite

The total relation `(135)` suggests separating the complete-aligned part of
the second channel.  Define

\[
 \mathcal E_\perp(S)=E_2(S)-(1-\chi)E_1(S),qquad
 K_\perp=K_0-(1-\chi)L_\pi.                                \tag{140}
\]

Then

\[
 R_{K_\perp}^\circ=-2\mathcal E_\perp,qquad
 \mathcal E_\perp(\varnothing)=\mathcal E_\perp(\{i\})
 =\mathcal E_\perp(V)=0.                                  \tag{141}
\]

Moreover,

\[
 K_\perp\mathbf1=0,qquad \operatorname{Tr}K_\perp=0.     \tag{142}
\]

Thus, unless it vanishes, `K_perp` is necessarily indefinite: a nonzero
positive- or negative-semidefinite symmetric matrix cannot have zero trace.
This is the precise limitation of a proof based only on positive fixed
contractions.  The genuinely new `K_0` information is a traceless,
boundary-neutral correction, not another positive occupation budget.  The
pencil splits as

\[
 K(\theta)=\{1+\theta(1-\chi)\}L_\pi+\theta K_\perp.       \tag{143}
\]

In fact the mode has the exact reversible factorization

\[
 \boxed{K_\perp=L_\pi(P+\chi I)
 =\Pi(I-P)(P+\chi I).}                                    \tag{144}
\]

If `lambda` is an eigenvalue of the self-adjoint reversible kernel, its
generalized multiplier relative to `L_pi` is `lambda+chi`; equivalently the
absolute multiplier is

\[
 (1-\lambda)(\lambda+\chi)
 ={(1+\chi)^2\over4}
 -\left(\lambda-{1-\chi\over2}\right)^2.                  \tag{145}
\]

Thus `K_perp` is positive on nonconstant modes with `lambda>-chi`, negative
on modes with `lambda<-chi`, and zero on the complete kernel, whose
nonconstant eigenvalues all equal `-chi=-1/(n-1)`.  In quadratic form this
is the exact difference of squares

\[
 f^TK_\perp f
 ={(1+\chi)^2\over4}\|f\|_\pi^2
 -\left\|\left(P-{1-\chi\over2}I\right)f\right\|_\pi^2.  \tag{146}
\]

It also gives the sharp fixed cone

\[
 -(1-\chi)L_\pi\preceq K_\perp
 \preceq(1+\chi)L_\pi,                                    \tag{147}
\]

which is just the centered form of `0<=K_0<=2L_pi`.  Hence no contraction
using only this fixed cone can create the missing strict rank transport.

There is also a local formula for its signed forcing.  Put

\[
 R=\operatorname{Diag}(r_v),\qquad
 B=P^2-R-(I-R)P.                                           \tag{148}
\]

Then `B1=0`, and the two-step mutant mass available after deleting the
target decomposes as

\[
 y-Rs=(I-R)x+Bs.                                           \tag{149}
\]

Using the signed coordinate drift `d` from `(68)`, equations `(129)--(130)`
give

\[
\boxed{
 L\mathcal E_\perp(S)
 =\sum_v\pi_vd_v(S)
 \left[(\chi-r_v)x_v(S)+(Bs)_v\right].}                   \tag{150}
\]

The right side vanishes pointwise at the complete kernel.  For a general
kernel it has no pointwise sign, but its occupation integral is exactly
zero for every feasible pseudoflow because all three boundary values in
`(141)` vanish.

Let the rank storage, creation, and debt terms for `E_perp` be the second
channel minus `(1-chi)` times the first channel.  Subtracting the two rows
of `(132)` gives

\[
 X^\perp_{k-1}+P^\perp_{k-1}+Y^\perp_{k+1}-N^\perp_{k+1}
 -X^\perp_k-Y^\perp_k=0                                   \tag{151}
\]

at every rank, including both endpoints, with absent terms zero.  Hence

\[
 \sum_k(P^\perp_k-N^\perp_k)=0.                            \tag{152}
\]

Equation `(151)`, coupled to all individual one-mark recurrences, is the
minimal two-channel Schur problem.  It explains both why rank-`H` alone can
fail and why merely adding a fixed PSD inequality cannot repair it: the
additional channel acts only by moving signed collision excess between
ranks.  Section 7.13 proves that this redistribution still does not control
the first-channel destruction debt universally.

### 7.12 Rank-`K_0` alone is also exactly insufficient

The exact `n=17` certificate `(102)` showed that rank-dependent `K_0`
repairs one particular global-conductance witness.  It does **not** furnish
a universal certificate by itself.  This can now be refuted exactly.

Consider the complete-support equitable graph with class sizes

\[
 (1,1,2,2,3)                                               \tag{153}
\]

and symmetric integer class-weight matrix

\[
\begin{pmatrix}
10^6&3\cdot10^{11}&7\cdot10^{10}&4\cdot10^5&3\cdot10^7\\
3\cdot10^{11}&10&4\cdot10^5&5\cdot10^{10}&5\\
7\cdot10^{10}&4\cdot10^5&3\cdot10^6&11\cdot10^5&9\cdot10^{10}\\
4\cdot10^5&5\cdot10^{10}&11\cdot10^5&17\cdot10^{10}&5\cdot10^{10}\\
3\cdot10^7&5&9\cdot10^{10}&5\cdot10^{10}&36\cdot10^9
\end{pmatrix}.                                             \tag{154}
\]

The restricted potential is

\[
 F(S)=a_k+\sum_{i\in S}b_{k,i}+q_k\,s^TK_0s,
 \qquad k=|S|.                                             \tag{155}
\]

Within-class symmetry gives 142 transient quotient states and 47
independent columns.  An exact 46-state strictly positive rational Farkas
dual, together with its independently reconstructed matching rational
primal, proves

\[
 \min_F {1\over9}\sum_iF(\{i\})
 =0.4539329228798728451964329\ldots
 >{1024\over2295}.                                         \tag{156}
\]

The exact excess is
`0.007745559045450187244363190...`; its reduced numerator and denominator
have 1798 and 1800 decimal digits, and its canonical SHA-256 identifier is

```text
49230606abeb30eafdf1dbe7bfd96b7e35f80bdff7eb7b15efbd759706c4534c
```

Every quotient drift row is checked against a separately labelled
nine-vertex construction.  Thus `(156)` is an exact obstruction to the
rank-`K_0` proof space, not a floating search result.  It is also not a
fixation counterexample.  Together with the independent rank-`H`
refutation `(120)--(123)`, it proves that the next compressed candidate had
to keep both channels rankwise; neither alone can be promoted
to a universal theorem.  The next section refutes even that combined
candidate.

### 7.13 Exact failure of the combined two-channel certificate

The implication `(127b)` is exactly false.  Take the twelve-vertex
complete-support graph with equitable class sizes

\[
 (1,1,2,3,5)                                               \tag{157}
\]

and symmetric integer class-weight matrix

\[
\begin{pmatrix}
1000&5000000000&10000&30&3\\
5000000000&2500&350&44&1200\\
10000&350&26000&4800&80000000\\
30&44&4800&6000000&30000000\\
3&1200&80000000&30000000&10000000
\end{pmatrix}.                                             \tag{158}
\]

The restricted potential space is the full two-channel space

\[
 F(S)=a_k+\sum_{i\in S}b_{k,i}
 +u_kE_1(S)+v_k\,s^TK_0s,\qquad k=|S|.                  \tag{159}
\]

Within-class symmetry gives 286 transient quotient states and 74
independent columns.  An exact 73-state strictly positive rational Farkas
dual and its independently reconstructed matching rational primal prove

\[
 \boxed{
 p_{W_{12}}(P)=0.4600442069423893447745517\ldots
 >{2816\over6141}=\rho_{\rm dB}(K_{12},2).}               \tag{160}
\]

The exact excess is
`0.001486968707574168093229390...`; its reduced numerator and denominator
have 3485 and 3487 decimal digits.  The canonical SHA-256 identifier is

```text
0cc5256b94a446ce0a8d2f8174e8cc081f5c3a0b25ea683d977808f044f94a22
```

Every quotient drift is checked against a separately labelled
twelve-vertex construction.  An independent exact harmonic solve also
gives

\[
 \rho_{\rm dB}(G,2)=0.4215620895939539989012090\ldots
 <{2816\over6141},                                         \tag{161}
\]

with exact suppression margin
`0.03699514864086117778011324...`.  Thus `(160)` is solely a proof-space
counterexample; the graph itself is not an endpoint amplifier.

Consequently the mass equations, every rank one-mark equation, and the two
storage rows `(132)` do not imply the endpoint bound.  Neither a
rank-dependent `theta_k` pencil nor a two-channel Schur/Riccati argument can
close the universal theorem without additional pair information.  The
smallest live quadratic space is now the full rank-pair matrix `(68)`, or
an enlargement with at least one genuinely new graph-dependent pair
direction.  See `COMBINED_W12_FARKAS_REFUTATION.md` and
`verify_combined_w12_farkas_refutation.py`.

### 7.14 The first new full-pair direction gives a sharp covariance square

The exact failure of `W_12` identifies the next matrix contraction rather
than merely deleting a conjecture.  Put

\[
 M(S)=\pi\mathbin\cdot s,\qquad V(S)=M(S)\{1-M(S)\},
 \qquad \mathcal D(S)=2C(S)-R_0(S).                        \tag{162}
\]

Sample a stationary target `v` and then a request `i` from row `P_v`.
For the random variables `S_0=s_v` and `X=x_v(S)`, stationarity and
reversibility give

\[
 \mathbb E S_0=\mathbb E X=M,\qquad
 \mathbb E(S_0X)=M-C,\qquad
 \mathbb E X^2=M-R_0.                                     \tag{163}
\]

Therefore their exact covariance matrix is positive semidefinite:

\[
 \boxed{
 \begin{pmatrix}
 V&V-C\\ V-C&V-R_0
 \end{pmatrix}\succeq0.}                                 \tag{164}
\]

Its determinant is the sharp pair inequality

\[
 \boxed{C(S)^2\le V(S)\mathcal D(S).}                     \tag{165}
\]

Equality holds exactly when `x_v(S)` is affine in `s_v`, equivalently when
the request probability is constant on the mutant side and constant on the
resident side (up to stationary-null vertices).  Every complete-graph rank
has equality.  Thus `(165)` has the correct equality class that the fixed
`L_pi,K_0` cone lacked.

The additional pair direction is simply the rank-one matrix
`pi pi^T`, because its state statistic is `M(S)^2`.  With `d,t` from
`(68)` and `Q=pi dot d`,

\[
 \boxed{L M(S)^2=2M(S)Q(S)+\mathcal V_\pi(S),\qquad
 \mathcal V_\pi(S)=\sum_v\pi_v^2t_v(S)\ge0.}             \tag{166}
\]

This also has a nonnegative rank-current resolution.  Define

\[
\begin{aligned}
 P^3(S)&=\sum_{v\notin S}g_v
       \{2M\pi_v+\pi_v^2\},\\
 N^3(S)&=\sum_{v\in S}\ell_v
       \{2M\pi_v-\pi_v^2\},
\end{aligned}                                              \tag{167}
\]

so `P^3,N^3>=0` and `LM^2=P^3-N^3`.  If `X^3_k,Y^3_k` are the rank
occupations of `M^2U,M^2D`, the exact recurrence is

\[
\boxed{
 {\|\pi\|_2^2\over n}1_{\{k=1\}}
 +X^3_{k-1}+P^3_{k-1}+Y^3_{k+1}-N^3_{k+1}-X^3_k-Y^3_k
 =z1_{\{k=n\}}.}                                         \tag{168}
\]

Summing gives

\[
 \sum_k(P^3_k-N^3_k)=z-{\|\pi\|_2^2\over n}.             \tag{169}
\]

Equations `(164)--(169)` are exact consequences of the full pair matrix,
and the rational verifier checks them independently.  They suggest the
smallest current enlargement after the refuted `W_12` space:

\[
 \mathcal W_{123}=\mathcal W_{12}
 +\operatorname{span}\{M(S)^2\}\quad\hbox{on every rank}. \tag{170}
\]

On the exact twelve-vertex `W_12` refuter this single added direction moves
the numerical restricted optimum below the baseline by more than `0.029`.
It also survived the first multiscale five- and six-class hostile cycles.
These are **NUMERICAL OBSERVATIONS ONLY**, not a universal theorem.  The
next exact obligation is a rankwise `2 by 2` Schur/Riccati estimate combining
`(132)`, `(165)`, and `(168)`.  The full rank-pair matrix remains the
fallback if `W_123` fails.

### 7.15 Exact rank Schur reduction and the transport obstruction

The covariance square remains positive after aggregation over any rank.
Write

\[
 V_k=\sum_{|S|=k}\bar\mu_SV(S),\qquad
 R^0_k=\sum_{|S|=k}\bar\mu_SR_0(S),\qquad
 \mathcal D_k=2C_k-R^0_k.                                 \tag{171}
\]

Summing `(164)` against the nonnegative pseudoflow gives

\[
 \Gamma_k=
 \begin{pmatrix}
 V_k&V_k-C_k\\
 V_k-C_k&V_k-R^0_k
 \end{pmatrix}\succeq0,
 \qquad
 \boxed{C_k^2\le V_k\mathcal D_k.}                        \tag{172}
\]

Equivalently, for every real rank sequence `theta_k`,

\[
 \boxed{
 \mathcal D_k-2\theta_kC_k+\theta_k^2V_k\ge0.}            \tag{173}
\]

This is the exact `2 by 2` Schur inequality, rather than a scalar
relaxation guessed from finite data.  Its best tangent at a fixed rank is
`theta_k=C_k/V_k`, with the convention that the term is zero when
`V_k=0` (then `(172)` forces `C_k=0`).

The new statistic also has a boundary-zero transport form.  Define

\[
\begin{aligned}
 P^M(S)&=\sum_{v\notin S}\pi_vg_v(S),&
 N^M(S)&=\sum_{v\in S}\pi_v\ell_v(S),\\
 B^+(S)&=P^M(S)-P^3(S)
 =\sum_{v\notin S}g_v\pi_v\{1-2M-\pi_v\},\\
 B^-(S)&=N^3(S)-N^M(S)
 =\sum_{v\in S}\ell_v\pi_v\{2M-1-\pi_v\}.
\end{aligned}                                             \tag{174}
\]

Then `LM=P^M-N^M=Q`.  For `V=M-M^2`,

\[
 \boxed{
 LV=B^++B^-=(1-2M)Q-\mathcal V_\pi.}                     \tag{175}
\]

Let `X^V_k,Y^V_k` denote the rank occupations of `VU,VD`, and let
`B^\pm_k` denote those of `(174)`.  Subtracting `(168)` from the
rank-labelled `M` balance gives the exact recurrence

\[
\boxed{
 {1-\|\pi\|_2^2\over n}1_{\{k=1\}}
 +X^V_{k-1}+B^+_{k-1}+Y^V_{k+1}+B^-_{k+1}
 -X^V_k-Y^V_k=0.}                                        \tag{176}
\]

There is no top sink because `V(empty)=V(V)=0`.  More generally, for every
rank profile `lambda_k`,

\[
\begin{aligned}
 L\{\lambda_kV(S)\}={}&V(S)
 [(\lambda_{k+1}-\lambda_k)U
  +(\lambda_{k-1}-\lambda_k)D]\\
 &+\lambda_{k+1}B^+(S)+\lambda_{k-1}B^-(S),\qquad k=|S|,
\end{aligned}                                             \tag{177}
\]

and its integrated boundary source is
`lambda_1(1-||pi||_2^2)/n`.  Equations `(173)` and `(177)` are the
minimal Riccati starting point.  The difficulty is now explicit:
`B^+` and `B^-` are signed adjacent-rank currents.  A proof must pay the
negative quadratic term in `(173)` using their transport, together with
the rank one-mark balances; a static PSD contraction cannot do so.

Indeed, put `a_n=2-kappa_n`.  From `(173)`, any rank profile `theta`
would reduce the target `(111)` to the sufficient residual

\[
 \mathcal R(\theta)=
 \sum_k\{W_k+(2\theta_k-a_n)C_k-\theta_k^2V_k\}\ge0.       \tag{178}
\]

If one discards `(176)--(177)` and optimizes the static tangent rank by
rank, its strongest possible value is

\[
 \sup_\theta\mathcal R(\theta)=
 \sum_k\left\{W_k-a_nC_k+{C_k^2\over V_k}\right\}.        \tag{179}
\]

This static route is **EXACTLY REFUTED** by the same rational twelve-vertex
graph from Section 7.13.  An independent exact Green solve gives

\[
 \sup_\theta\mathcal R(\theta)
 =-0.2524901456099282956184879\ldots<0,                  \tag{180}
\]

while the true full residual in `(111)` is

\[
 \sum_k(\mathcal D_k+W_k-a_nC_k)
 =0.002549972027336616301296108\ldots>0.                 \tag{181}
\]

Both signs are certified over the rationals.  Their canonical
numerator/denominator SHA-256 identifiers are, respectively,

```text
56d33de896c8e6c7d23dfb1712acbbb972647529cbbcec94d12cd5c61832a2e9
e9921c44de22a2f1d274edfe7e95672a803a3e32541b9f1aa5a260a9fe2f2782
```

Thus the sharp covariance square is genuine new structure, but even its
best independent rank tangents lose the theorem by a large exact margin.
This does **not** refute `W_123`: that potential space retains precisely
the transport identity `(177)` which the static relaxation discards.

### 7.16 The third direction is a nonnegative pair flow and an operator square

The signed variance current is not the canonical gauge for the potential
space.  Put

\[
 \sigma=\|\pi\|_2^2,\qquad
 J(S)=\sum_i\pi_i^2s_i,\qquad
 E_3(S)=\sum_{i<j}\pi_i\pi_js_is_j={M(S)^2-J(S)\over2}.    \tag{182}
\]

Because every rank-labelled one-mark is already available, adjoining
`M^2` is exactly equivalent to adjoining `E_3`.  Unlike `V`, the latter is
an internal flow with nonnegative edge weights.  It vanishes at the empty
set and every singleton, and

\[
 E_3(V)={1-\sigma\over2}.
\]

Its increment on adding `v` is `pi_v M`, and the amount lost on removing
`v` is `pi_v(M-pi_v)`.  Hence

\[
\begin{aligned}
 \widetilde P^3(S)&=\sum_{v\notin S}g_v\pi_vM,&
 \widetilde N^3(S)&=\sum_{v\in S}\ell_v\pi_v(M-\pi_v),\\
 LE_3&=\widetilde P^3-\widetilde N^3,&
 \widetilde P^3,\widetilde N^3&\ge0.                     \tag{183}
\end{aligned}
\]

If `\widetilde X^3_k,\widetilde Y^3_k` are the rank occupations of
`E_3U,E_3D`, then

\[
\boxed{
 \widetilde X^3_{k-1}+\widetilde P^3_{k-1}
 +\widetilde Y^3_{k+1}-\widetilde N^3_{k+1}
 -\widetilde X^3_k-\widetilde Y^3_k
 ={z(1-\sigma)\over2}1_{\{k=n\}}.}                       \tag{184}
\]

In particular,

\[
 \sum_k(\widetilde P^3_k-\widetilde N^3_k)
 ={z(1-\sigma)\over2}.                                    \tag{185}
\]

Since `sigma>=1/n`, comparison with the first internal-request channel
in `(133)` gives the second sharp total deficit

\[
\boxed{
 \sum_k(\widetilde P^3_k-\widetilde N^3_k)
 \le {n-1\over n}\sum_k(P^1_k-N^1_k),}                   \tag{186}
\]

with exact gap `z(sigma-1/n)/2`.  Equality means that `pi` is uniform.
Together, the channel-two gap `(136)` and the channel-three gap `(186)`
vanish only for the complete loopless kernel.

The three channels also lift the scalar covariance inequality to a single
graph-independent matrix square.  Define

\[
 L_3=\Pi-\pi\pi^T,\qquad
 D_0=2L_\pi-K_0=(I-P)^T\Pi(I-P),\qquad
 B=I-\mathbf1\pi^T.                                      \tag{187}
\]

For every real `theta`,

\[
\boxed{
 \begin{aligned}
 \mathcal K(\theta)
 &=D_0-2\theta L_\pi+\theta^2L_3\\
 &=\{(I-P)-\theta B\}^T\Pi\{(I-P)-\theta B\}\succeq0.
 \end{aligned}}                                           \tag{188}
\]

The matrices in `(188)` lie exactly in the span of the three cut
Laplacians: `L_3` belongs to `E_3`, `L_pi` to `E_1`, and `K_0` to `E_2`,
with `D_0=2L_pi-K_0`.  On a mutant indicator `s`,

\[
 s^TL_3s=V,\qquad s^TL_\pi s=C,\qquad
 s^TD_0s=\mathcal D.
\]

Thus `(173)` is the binary specialization of an all-vector operator
identity.  Moreover, `K(theta)=0` as a matrix implies

\[
 P=(1-\theta)I+\theta\mathbf1\pi^T.
\]

Looplessness then forces

\[
 \pi_i={1\over n},\qquad
 \theta={n\over n-1},\qquad
 P_{ij}={1\over n-1}\quad(i\ne j).                        \tag{189}
\]

So the operator square has exactly the desired complete-kernel equality
class.  This does not yet prove the endpoint bound: Section 7.15 proves
that independent rankwise use of the square is insufficient.  The live
`W_123` problem is now sharply a three-channel nonnegative-flow transport
theorem using `(132)` and `(184)`, with the full rank-pair matrix as
fallback.

### 7.17 The exact mixed-current Schur cone

The operator square controls the failure of the first and third currents
to remain in their complete-graph ratio.  Put

\[
 \alpha={n-1\over n},\qquad \theta={1\over\alpha}={n\over n-1},
\qquad
 e_v(S)=s_v-x_v-\theta\{s_v-M(S)\}.                       \tag{190}
\]

Then

\[
 K_\theta(S):=\sum_v\pi_ve_v(S)^2
 =\mathcal D(S)-2\theta C(S)+\theta^2V(S)\ge0.            \tag{191}
\]

Recall that, state by state,

\[
 P^1=C-Q^+,\qquad N^1=Q^-,
\]

and let `\widetilde P^3,\widetilde N^3` be the product-mass currents in
`(183)`.  The sole stationary-mass correction is the one-mark debt

\[
 T^-_\pi(S)=\sum_{v\in S}\ell_v\pi_v
             \left(\pi_v-{1\over n}\right).               \tag{192}
\]

Direct substitution into `(183)` gives the two exact identities

\[
\boxed{
\begin{aligned}
 \alpha P^1-\widetilde P^3
   &=-\alpha\sum_{v\notin S}g_v\pi_ve_v,\\
 \alpha N^1-\widetilde N^3-T^-_\pi
   &=-\alpha\sum_{v\in S}\ell_v\pi_ve_v.
\end{aligned}}                                            \tag{193}
\]

Since `0<=g_v,ell_v<=1`, weighted Cauchy--Schwarz yields the statewise
second-order cone

\[
\boxed{
\begin{aligned}
 (\alpha P^1-\widetilde P^3)^2
   &\le\alpha^2P^M K_\theta,\\
 (\alpha N^1-\widetilde N^3-T^-_\pi)^2
   &\le\alpha^2N^M K_\theta.
\end{aligned}}                                            \tag{194}
\]

This survives rank aggregation without loss of form.  If a subscript `k`
denotes occupation against `bar(mu)` and
`K_{\theta,k}=sum_(|S|=k)bar(mu)_S K_theta(S)`, then

\[
\boxed{
\begin{aligned}
 (\alpha P^1_k-\widetilde P^3_k)^2
   &\le\alpha^2P^M_kK_{\theta,k},\\
 (\alpha N^1_k-\widetilde N^3_k-T^-_{\pi,k})^2
   &\le\alpha^2N^M_kK_{\theta,k}.
\end{aligned}}                                            \tag{195}
\]

The term `T^-_pi` is not discarded: it is an oriented response of the
rank-labelled vertex field with coefficients
`pi_v(pi_v-1/n)`, so the exact one-mark balances retain it.  On the
complete kernel, `e_v=T^-_pi=0` and both current ratios in `(193)` are
identities.

Equations `(184)` and `(195)` are the smallest concrete Schur/Riccati
system found in the three-channel space.  They improve the refuted static
tangent by controlling adjacent-rank creation and debt separately.  They
do not yet imply the endpoint sum: the remaining sign is a rank-profile
transport inequality coupling the two cones through the one-mark
recurrence.  No relaxation of `T^-_pi` to an unsigned scalar has been
claimed.

### 7.18 Canonical two-component boundary block

The second pair channel supplies the missing companion to `(193)`.  Put

\[
 \beta={n-2\over n-1}=2-\theta,
 \qquad r_v=(P^2)_{vv},
 \qquad f=(I-P)e,                                         \tag{196}
\]

and retain `chi=sum_v pi_v sum_i P_(vi)^2`.  Since

\[
 f_v=y_v-\beta x_v-(\theta-1)s_v,
 \qquad y=P^2s,                                           \tag{197}
\]

the creation and debt currents in `(130)` obey the exact oriented
identities

\[
\boxed{
\begin{aligned}
 P^2-\beta P^1
   &=\sum_{v\notin S}g_v\pi_v f_v,\\
 N^2-\beta N^1-T^-_r
   &=\sum_{v\in S}\ell_v\pi_v f_v,
\end{aligned}}                                             \tag{198}
\]

where the second one-mark debt is

\[
 T^-_r(S)=\sum_{v\in S}\ell_v\pi_v
 \left({1\over n-1}-r_v\right).                           \tag{199}
\]

Thus the first--third and second--first discrepancies are not two
unrelated scalar currents.  Define the pair-storage vector

\[
 \mathbf G(S)=
 \binom{\alpha E_1(S)-E_3(S)}{E_2(S)-\beta E_1(S)},        \tag{200}
\]

the two one-mark fields

\[
 h^{(1)}_v=\pi_v-{1\over n},\qquad
 h^{(2)}_v={1\over n-1}-r_v,
 \qquad
 \mathbf H(S)=\sum_{v\in S}\pi_v
 \binom{h^{(1)}_v}{h^{(2)}_v},                             \tag{201}
\]

and the nonnegative heterogeneity defects

\[
 \delta=\|\pi\|_2^2-{1\over n},\qquad
 \varepsilon=\chi-{1\over n-1},\qquad
 \mathbf u=\binom{\delta}{-\varepsilon}.                 \tag{202}
\]

Reversibility gives `sum_v pi_v r_v=chi`.  Consequently the endpoint data
line up exactly:

\[
 \boxed{
 \mathbf G(\varnothing)=\mathbf G(\{i\})=0,\quad
 \mathbf G(V)={\mathbf u\over2},\quad
 \mathbf H(V)=\mathbf u,\quad
 {1\over n}\sum_i\mathbf H(\{i\})={\mathbf u\over n}.} \tag{203}
\]

Let `mathbf(A)^+,mathbf(A)^-` be the creation and debt currents of
`mathbf(G)`, and `mathbf(T)^+,mathbf(T)^-` the oriented responses of
`mathbf(H)`.  Equations `(193)` and `(198)` combine into the single
two-component factorization

\[
\boxed{
\begin{aligned}
 \mathbf A^+(S)
  &=\sum_{v\notin S}g_v\pi_v
       \binom{-\alpha e_v}{f_v},\\
 \mathbf A^-(S)-\mathbf T^-(S)
  &=\sum_{v\in S}\ell_v\pi_v
       \binom{-\alpha e_v}{f_v}.
\end{aligned}}                                             \tag{204}
\]

This is the canonical `W_123` current block.  Both orientations are driven
by the same Schur error; all asymmetry is stored in the available one-mark
vector `(201)`.

There are two useful exact gauges.  First,

\[
 \mathbf C=\mathbf G-{1\over2}\mathbf H                 \tag{205}
\]

vanishes at the empty and full states and has uniform-singleton average
`-mathbf(u)/(2n)`.  With

\[
 \mathbf J^+=\mathbf A^+-{1\over2}\mathbf T^+,
 \qquad
 \mathbf J^-=\mathbf A^--{1\over2}\mathbf T^-,           \tag{206}
\]

one has `Lmathbf(C)=mathbf(J)^+-mathbf(J)^-`.  Second, the scalar
combination

\[
 G_*=\varepsilon(\alpha E_1-E_3)
       +\delta(E_2-\beta E_1),
 \qquad
 H_*=\varepsilon H_1+\delta H_2                           \tag{207}
\]

has zero empty, uniform-singleton, and full boundary data.  This is forced
by `(203)`, since `(varepsilon,delta) dot mathbf(u)=0`; it is not a fitted
coefficient from finite data.

For a degree-two pseudoflow, let `mathbf(X)^G_k,mathbf(Y)^G_k` denote the
rank occupations of `mathbf(G)U,mathbf(G)D`, and define the analogous
quantities for `mathbf(H)` and `mathbf(C)`.  The full vector rank balances
are

\[
\boxed{
 \mathbf X^G_{k-1}+\mathbf A^+_{k-1}
 +\mathbf Y^G_{k+1}-\mathbf A^-_{k+1}
 -\mathbf X^G_k-\mathbf Y^G_k
 ={z\mathbf u\over2}1_{\{k=n\}},}                         \tag{208}
\]

\[
\boxed{
 {\mathbf u\over n}1_{\{k=1\}}
 +\mathbf X^H_{k-1}+\mathbf T^+_{k-1}
 +\mathbf Y^H_{k+1}-\mathbf T^-_{k+1}
 -\mathbf X^H_k-\mathbf Y^H_k
 =z\mathbf u1_{\{k=n\}},}                                \tag{209}
\]

and hence

\[
\boxed{
 -{\mathbf u\over2n}1_{\{k=1\}}
 +\mathbf X^C_{k-1}+\mathbf J^+_{k-1}
 +\mathbf Y^C_{k+1}-\mathbf J^-_{k+1}
 -\mathbf X^C_k-\mathbf Y^C_k=0.}                         \tag{210}
\]

All absent endpoint terms are zero.  In particular the total centered
flux is fixed independently of `z`:

\[
 \sum_k(\mathbf J^+_k-\mathbf J^-_k)={\mathbf u\over2n}. \tag{211}
\]

The associated local action is also exact.  For every
`lambda=(lambda_1,lambda_2) in R^2`, put

\[
 \mathfrak a_\lambda(S)
 =\sum_v\pi_v\{-\alpha\lambda_1e_v+\lambda_2f_v\}^2.     \tag{212}
\]

Weighted Cauchy--Schwarz gives, statewise and after rank aggregation,

\[
\boxed{
\begin{aligned}
 \{\lambda\mathbin\cdot\mathbf A^+\}^2
 &\le P^M\mathfrak a_\lambda,\\
 \{\lambda\mathbin\cdot(\mathbf A^--\mathbf T^-)\}^2
 &\le N^M\mathfrak a_\lambda.
\end{aligned}}                                             \tag{213}
\]

Because reversible `P` is self-adjoint on `L^2(pi)` with spectrum in
`[-1,1]`, the action contracts to the original Schur energy sharply:

\[
\boxed{
 \mathfrak a_\lambda(S)
 \le m(\lambda)K_\theta(S),\qquad
 m(\lambda)=\max\{(\alpha\lambda_1)^2,
                   (-\alpha\lambda_1+2\lambda_2)^2\}.}    \tag{214}
\]

Indeed `(212)` applies the affine polynomial
`-alpha lambda_1+lambda_2 t` to `e`, with `t` in `[0,2]`; the maximum of
its squared magnitude is attained at an endpoint.  This produces the
promised two-channel Thomson action without importing any untracked pair
moment.

Finally, `mathbf(u)=0` holds exactly at the complete loopless kernel.  The
condition `delta=0` makes `pi` uniform, while `varepsilon=0` is the rowwise
Cauchy equality in `(134)` and makes every loopless row uniform.  Thus the
boundary block has the correct equality class.

Equations `(208)--(214)` are an exact vector-flow reduction, but not yet a
proof of `(111)`.  A path-network proof must still control the signed
holdings `mathbf(X)^C,mathbf(Y)^C` in `(210)` (or work with the three
original nonnegative pair storages).  Simply deleting those holdings does
not define an `M`-matrix and would repeat the already refuted static
relaxation.  The remaining concrete obligation is a rank-path
Dirichlet/Thomson inequality which couples `(210)` to the nonnegative
storage recurrences `(132),(184)` and pays the reward
`theta^2 V-W-(2theta-a_n)C` in `(178)`.

### 7.19 The mass mode completes the local phase action

The two special mark fields do not by themselves form a dynamically closed
Bellman block.  The missing local coordinate is the rank-centred stationary
mass

\[
 m_k(S)=M(S)-{k\over n},\qquad |S|=k.                     \tag{215}
\]

It produces an especially clean third current.  Put

\[
\begin{aligned}
 R^+_0(S)&=P^1(S)-{k\over n-1}P^M(S),\\
 R^-_0(S)&=N^1(S)-{k-1\over n-1}N^M(S).
\end{aligned}                                             \tag{216}
\]

For an addition target `v notin S` and a removal target `v in S`,
respectively,

\[
 x_v-{k\over n-1}=\theta m_k-e_v,
 \qquad
 x_v-{k-1\over n-1}=\theta m_k-e_v.                       \tag{217}
\]

Consequently, if

\[
 \mathbf R^+=
 \begin{pmatrix}R^+_0\\ \alpha P^1-\widetilde P^3\\
 P^2-\beta P^1\end{pmatrix},
 \qquad
 \mathbf R^-=
 \begin{pmatrix}R^-_0\\ \alpha N^1-\widetilde N^3-T^-_\pi\\
 N^2-\beta N^1-T^-_r\end{pmatrix},                        \tag{218}
\]

then both orientations have the same exact three-phase factorization

\[
\boxed{
 \mathbf R^+(S)=\sum_{v\notin S}g_v\pi_v
 \begin{pmatrix}\theta m_k-e_v\\-\alpha e_v\\f_v\end{pmatrix},
 \qquad
 \mathbf R^-(S)=\sum_{v\in S}\ell_v\pi_v
 \begin{pmatrix}\theta m_k-e_v\\-\alpha e_v\\f_v\end{pmatrix}.} \tag{219}
\]

For `lambda=(lambda_0,lambda_1,lambda_2)`, its exact local action is

\[
\begin{aligned}
 \mathfrak b_\lambda(S)
 &=\sum_v\pi_v\{\lambda_0\theta m_k
 -(\lambda_0+\alpha\lambda_1)e_v+\lambda_2f_v\}^2\\
 &=\lambda_0^2\theta^2m_k^2
 +\|-(\lambda_0+\alpha\lambda_1)e+\lambda_2(I-P)e\|_\pi^2.
                                                               \tag{220}
\end{aligned}
\]

The second equality uses `sum_v pi_v e_v=sum_v pi_v f_v=0`.  Therefore
weighted Cauchy--Schwarz gives

\[
 \{\lambda\mathbin\cdot\mathbf R^+\}^2
 \le P^M\mathfrak b_\lambda,
 \qquad
 \{\lambda\mathbin\cdot\mathbf R^-\}^2
 \le N^M\mathfrak b_\lambda,                              \tag{221}
\]

statewise and after rank aggregation.  Reversible spectral calculus gives
the sharp endpoint envelope

\[
\boxed{
 \mathfrak b_\lambda(S)
 \le \lambda_0^2\theta^2m_k^2
 +\max\{(\lambda_0+\alpha\lambda_1)^2,
 (-\lambda_0-\alpha\lambda_1+2\lambda_2)^2\}K_\theta(S).} \tag{222}
\]

Both terms on the right belong to `W_123`: on a fixed rank,
`m_k^2=M^2-2(k/n)M+k^2/n^2`, and `K_theta` is the three-pair operator
square `(188)`.  Thus `(219)--(222)` give a closed local kinetic metric in
the allowed potential space.  What remains nonlocal is the transfer of its
three phase potentials between adjacent ranks.

This mass coordinate is not cosmetic.  On the exact twelve-vertex combined
refuter, the numerical LP obtained by retaining all three pair directions
but only the two mark fields `(201)` lies above the complete baseline by
about `0.0035984`.  Adding the rank-labelled mass field `(215)` moves the
optimum below baseline by about `0.0298761` and also repairs the stored
nine- and seventeen-vertex witnesses.  These are discovery calculations,
not exact certificates or a universal theorem.  They show that the next
Riccati recursion must carry the mass phase together with the two pair
phases; a pure `2 by 2` mark recursion is already falsified numerically on
the principal hostile case.

### 7.20 Exact block-tridiagonal Bellman transfer

The three-phase action has a canonical first-order transfer.  Put
`N=n-1`, let `e_0=(1,0,0)^T`, and define

\[
 \widehat h_v=
 \begin{pmatrix}1\\h^{(1)}_v\\h^{(2)}_v\end{pmatrix},
 \qquad
 \widetilde h_v=
 \begin{pmatrix}1/N\\h^{(1)}_v\\h^{(2)}_v\end{pmatrix},
 \qquad
 \mathbf Y(S)=\begin{pmatrix}M(S)\\\mathbf H(S)\end{pmatrix}. \tag{223}
\]

The centered pair coordinate on the `k`-slice is

\[
 \mathbf Z_k(S)=
 \begin{pmatrix}
 E_1(S)-{k-1/2\over N}M(S)\\
 \mathbf G(S)-\mathbf H(S)/2
 \end{pmatrix}.                                            \tag{224}
\]

For one addition `T=S union {v}` and one removal `T=S minus {v}`,
the event-level identities are

\[
\boxed{
\begin{aligned}
 \mathbf Y(S\cup v)-\mathbf Y(S)&=\pi_v\widehat h_v,\\
 \mathbf Z_{k+1}(S\cup v)-\mathbf Z_k(S)
 &=\pi_v\{\mathbf z_{k,v}-\widetilde h_v/2\}
   -{M(S)\over N}e_0,\\
 \mathbf Y(S)-\mathbf Y(S\setminus v)&=\pi_v\widehat h_v,\\
 \mathbf Z_k(S)-\mathbf Z_{k-1}(S\setminus v)
 &=\pi_v\{\mathbf z_{k,v}+\widetilde h_v/2\}
   -{M(S)\over N}e_0,
\end{aligned}}                                             \tag{225}
\]

where

\[
 \mathbf z_{k,v}=
 \begin{pmatrix}\theta m_k(S)-e_v\\-\alpha e_v\\f_v\end{pmatrix}. \tag{226}
\]

These formulas include the half-rank shift in the first coordinate; no
endpoint or holding term is suppressed.

Let `c_k in R` and `p_k,q_k in R^3`, and consider the canonical phase
potential

\[
 \Phi(S)=c_k+p_k\mathbin\cdot\mathbf Z_k(S)
                 +q_k\mathbin\cdot\mathbf Y(S),
 \qquad |S|=k.                                             \tag{227}
\]

This lies in `W_123` with rank constants and the three distinguished
one-marks `M,H_1,H_2`.  Define

\[
\begin{aligned}
 \Xi^+_{p,q}(S)
 &=\sum_{v\notin S}g_v\pi_v
   [p\mathbin\cdot(\mathbf z_{k,v}-\widetilde h_v/2)
    +q\mathbin\cdot\widehat h_v],\\
 \Xi^-_{p,q}(S)
 &=\sum_{v\in S}\ell_v\pi_v
   [p\mathbin\cdot(\mathbf z_{k,v}+\widetilde h_v/2)
    +q\mathbin\cdot\widehat h_v].                         \tag{228}
\end{aligned}
\]

Direct substitution of `(225)` gives the exact block-tridiagonal Bellman
operator

\[
\boxed{
\begin{aligned}
 L\Phi(S)={}&U\bigl[c_{k+1}-c_k
 +(p_{k+1}-p_k)\mathbin\cdot\mathbf Z_k
 +(q_{k+1}-q_k)\mathbin\cdot\mathbf Y
 -{p_{k+1,0}\over N}M\bigr]\\
 &+D\bigl[c_{k-1}-c_k
 +(p_{k-1}-p_k)\mathbin\cdot\mathbf Z_k
 +(q_{k-1}-q_k)\mathbin\cdot\mathbf Y
 +{p_{k-1,0}\over N}M\bigr]\\
 &+\Xi^+_{p_{k+1},q_{k+1}}(S)
  -\Xi^-_{p_{k-1},q_{k-1}}(S).
\end{aligned}}                                             \tag{229}
\]

Thus every slice constraint couples only coefficient blocks `k-1,k,k+1`.
In particular, `(229)` is the exact graph-dependent Bellman transfer whose
inverse-positive or Riccati sign would prove feasibility of this canonical
subspace.  Together with an arbitrary residual rank one-mark it is the
full `W_123` Bellman system.

The reason a naive backward Schur complement fails is now algebraic.  Let

\[
 D_*=\operatorname{Diag}(1/N,1,1),\qquad
 \mathbf T^+=\sum_{v\notin S}g_v\pi_v\widehat h_v,
 \qquad
 \mathbf T^-=\sum_{v\in S}\ell_v\pi_v\widehat h_v.
\]

Using `(219)`, the oriented terms split as

\[
\boxed{
 \Xi^+_{p,q}=p\mathbin\cdot\mathbf R^+
 +(q-D_*p/2)\mathbin\cdot\mathbf T^+,
 \qquad
 \Xi^-_{p,q}=p\mathbin\cdot\mathbf R^-
 +(q+D_*p/2)\mathbin\cdot\mathbf T^-.}                   \tag{230}
\]

The kinetic metric `(220)--(222)` is positive only in `p`; `q` is the
one-mark transport momentum and has a zero local quadratic block.  Hence
the first Schur complement which tries to eliminate `q` from the local
action is singular.  Killing both mark currents pointwise would require
`q=D_*p/2=-D_*p/2`, hence `p=0`.  This proves that no local `3 by 3`
Riccati based only on the kinetic action can be valid.  It does **not**
refute `W_123`: the signed `q` holdings in `(229)` are precisely the
nonlocal information that must be retained.

Accordingly, there are now two honest continuations.  One may prove a
rank-path coercivity theorem which supplies a positive `q` block from the
full one-mark transport, or enlarge the pair coordinate to a
rank-dependent spectral matrix `f_k(P)` (and ultimately the full pair
matrix).  Adding another static scalar contraction cannot repair the
singular Schur step.

### 7.21 A positive spectral conjugate and the single remaining current sign

The spectral enlargement has a canonical first member which is already
inside `W_123` and supplies the missing positive holding block.  Work in
reversible coordinates and put

\[
 S_\pi=\Pi^{1/2}P\Pi^{-1/2},\qquad
 T=I-S_\pi,\qquad
 B=I-\sqrt\pi\sqrt\pi^{T},\qquad
 \theta={n\over n-1}.                                    \tag{231}
\]

Here `B` is the orthogonal projection off the stationary vector.  Define

\[
 \mathscr F=\theta B-{1\over2}T,
 \qquad
 K_F=\Pi^{1/2}\mathscr F\Pi^{1/2}
     =\theta(\Pi-\pi\pi^T)-{1\over2}L_\pi.               \tag{232}
\]

Because a reversible Markov kernel has spectrum in `[-1,1]`, the spectrum
of `T` on `sqrt(pi)^perp` lies in `[0,2]`.  Hence the corresponding
eigenvalues of `mathscr F` are

\[
 \theta-{t\over2}\ge\theta-1={1\over n-1}>0.             \tag{233}
\]

Thus `K_F` is positive semidefinite, its kernel is exactly the constants,
and the boundary-zero pair storage

\[
 \mathcal S_F(S)=s^TK_Fs
 =\theta V(S)-{1\over2}C(S)\ge0                         \tag{234}
\]

vanishes only at the empty and full states.  This is a fixed linear
combination of the first and third `W_123` pair channels, not an added
ansatz.  Looplessness gives the exact singleton source

\[
 {1\over n}\sum_v\mathcal S_F(\{v\})
 ={\operatorname {Tr}K_F\over n},\qquad
 \operatorname {Tr}K_F
 =\theta(1-\|\pi\|_2^2)-{1\over2}.                       \tag{235}
\]

Recall the selection vector `a` and event activity `t` from `(68)--(70)`,
and set

\[
 A_F(S)=s^TK_Fa(S),\qquad
 D_F(S)=\sum_v(K_F)_{vv}t_v(S).                           \tag{236}
\]

For `u=Pi^{1/2}(s-M1)`, one has
`Pi^{1/2}d=-Tu+Pi^{1/2}a` and
`Pi^{1/2}e=(T-theta B)u`.  The exact quadratic generator identity is
therefore

\[
\boxed{
 L\mathcal S_F
 =K_\theta-\theta^2V+2A_F+D_F.}                          \tag{237}
\]

Indeed, the quadratic part is
`-2u^T mathscr F T u=u^T(T^2-2 theta T)u`, and the other two
terms are respectively the linear drift and flip diagonal in `(68)`.
This proves `(237)` directly from the labelled chain; it is not a
stationary approximation.

Let `a_n=2-kappa_n` and

\[
 b_n=2\theta-a_n=\kappa_n+{2\over n-1}.                  \tag{238}
\]

The endpoint residual in `(111)` has the exact decomposition

\[
\boxed{\begin{aligned}
 \mathcal D+\mathcal W-a_nC
 &=K_\theta+\mathcal W+b_nC-\theta^2V\\
 &=L\mathcal S_F+\mathcal J_F,\\
 \mathcal J_F
 &:=\mathcal W+b_nC-2A_F-D_F.
\end{aligned}}                                             \tag{239}
\]

Since `mathcal S_F` is zero at both absorbing states, the exact degree-two
pseudoflow balance `(66)` gives

\[
 \sum_S\bar\mu_SL\mathcal S_F(S)
 =-{\operatorname {Tr}K_F\over n}.                       \tag{240}
\]

Consequently the universal fitness-two theorem is **equivalent**, within
the exact rank-pair pseudoflow, to the single integrated current inequality

\[
\boxed{
 \sum_S\bar\mu_S\mathcal J_F(S)
 \ge {\operatorname {Tr}K_F\over n}.}                    \tag{241}
\]

This is sharper than the singular local Riccati formulation: the positive
storage `(234)` supplies a genuine holding block, and `(241)` contains no
discarded pair moment.  It also exposes the precise remaining sign rather
than asserting it.  On the complete kernel equality holds.

For completeness, the exact rank transport behind `(240)` is as follows.
For an addition or removal at `v`, define the signed storage increments

\[
 \Delta_v^+=2(K_Fs)_v+(K_F)_{vv},\qquad
 \Delta_v^-=2(K_Fs)_v-(K_F)_{vv},                         \tag{242}
\]

and the occupied currents

\[
 P^F_k=\sum_{|S|=k}\bar\mu_S\sum_{v\notin S}g_v\Delta_v^+,
 \qquad
 N^F_k=\sum_{|S|=k}\bar\mu_S\sum_{v\in S}\ell_v\Delta_v^- . \tag{243}
\]

If `X^F_k,Y^F_k` are the occupations of `mathcal S_F U` and
`mathcal S_F D`, then, with absent terms zero,

\[
\boxed{
 {\operatorname {Tr}K_F\over n}1_{\{k=1\}}
 +X^F_{k-1}+P^F_{k-1}+Y^F_{k+1}-N^F_{k+1}
 -X^F_k-Y^F_k=0,\quad 1\le k<n.}                         \tag{244}
\]

The holdings `X^F,Y^F` are nonnegative, although the increments in
`(242)` are signed.  Summing `(244)` recovers `(240)`.  A proof of `(241)`
must control these signed adjacent-rank currents; it cannot be replaced by
a pointwise or independent-rank bound.  A numerical diagnostic on the
stored rational twelve-vertex hostile graph finds negative true-Green
contributions of `mathcal J_F` on many intermediate ranks even though their
total exceeds `(235)`; this observation is not used as proof.  Thus `(241)`
is a proved variational reduction and the final sign remains **OPEN**.

### 7.22 The affine spectral remainder is exactly a mass-square gauge

The positivity in `(232)--(234)` does not itself add a new coercive
current.  In fact the remainder in `(239)` has an exact pointwise collapse.
Put

\[
 \mathcal R_F(S)=\theta M(S)^2-
                 \left(\theta-{1\over2}\right)M(S).       \tag{245}
\]

Recall that

\[
 LM=Q,\qquad
 LM^2=2MQ+\mathcal V_\pi,
 \qquad \mathcal V_\pi=\sum_v\pi_v^2t_v,                 \tag{246}
\]

and that `LC=3Q-2C`.  Since

\[
 \mathcal S_F=\theta(M-M^2)-{C\over2},                    \tag{247}
\]

one has

\[
 L\mathcal S_F
 =\left(\theta-{3\over2}\right)Q+C
   -2\theta MQ-\theta\mathcal V_\pi.                     \tag{248}
\]

On the other hand the endpoint residual has the already proved form

\[
 \mathcal D+\mathcal W-a_nC=\kappa_nC-Q.                 \tag{249}
\]

Subtracting `(248)` from `(249)` and using `(239)` gives the exact identity

\[
\boxed{
 \mathcal J_F
 =L\mathcal R_F-(1-\kappa_n)C.}                          \tag{250}
\]

Thus every occurrence of `A_F,D_F,K_theta`, and `mathcal W` in the fixed
affine spectral remainder cancels to a mass-square coboundary plus the
original cut reward.  This is a pointwise identity, not merely an
occupation-law simplification.

Its boundary data make the scope transparent:

\[
 \mathcal R_F(\varnothing)=0,\qquad
 \mathcal R_F(V)={1\over2},\qquad
 {1\over n}\sum_v\mathcal R_F(\{v\})
 =-{\operatorname {Tr}K_F\over n}.                       \tag{251}
\]

Consequently every exact degree-two pseudoflow obeys

\[
 \sum_S\bar\mu_SL\mathcal R_F(S)
 ={z\over2}+{\operatorname {Tr}K_F\over n},              \tag{252}
\]

and `(241)` becomes

\[
 {z\over2}\ge(1-\kappa_n)
 \left({3z\over2}-{1\over n}\right).                    \tag{253}
\]

Direct simplification of `kappa_n` shows that `(253)` is exactly

\[
 z\le{(n-1)2^{n-2}\over n(2^{n-1}-1)}.                  \tag{254}
\]

So `(241)` remains a correct equivalence, but it is not a new route to its
own sign: the fixed affine conjugate merely regauges the original endpoint
inequality.  This also proves a useful no-go statement.  Any next spectral
step whose multiplier lies in the affine span of `B,T` introduces no pair
direction beyond `M^2,C`; after exact Green balance its apparent remainder
has no independent coercivity.  A genuine spectral advance must retain a
non-affine function of `T` (for example a Green/Schur multiplier) or the full
pair matrix, together with its rank transport.

### 7.23 The first non-affine Green--Schur defect

There is a canonical next multiplier, with no fitted parameter.  On the
centered reversible space put

\[
 E=T-\theta B,\qquad F=\theta B-{T\over2},\qquad
 G=EF^{-1}E.                                             \tag{255}
\]

Here and below the inverse is on `sqrt(pi)^perp`.  Since `F` is strictly
positive there, `G` is positive semidefinite and its spectral multiplier is

\[
 g(t)={(t-\theta)^2\over\theta-t/2},\qquad 0<t\le2.      \tag{256}
\]

This is genuinely non-affine in `T`.  It is also rational in the original
coordinates.  Define

\[
 K_E=L_\pi-\theta(\Pi-\pi\pi^T),                         \tag{257}
\]

so that `K_E=Pi^(1/2) E Pi^(1/2)`.  Since `K_F` and `K_E` annihilate the
constant vector,

\[
\boxed{
 K_G=K_E(K_F+\mathbf1\mathbf1^T)^{-1}K_E
     =\Pi^{1/2}G\Pi^{1/2}.}                              \tag{258}
\]

The first equality is independent of the displayed constant-kernel gauge:
on every zero-sum column the inverse solves the quotient `K_F` equation,
and the left `K_E` deletes the possible additive constant.  In particular,
`K_G` has rational entries whenever `P,pi` do.  Equivalently, on the
constant-orthogonal quotient,

\[
 \begin{pmatrix}K_F&K_E\\K_E&K_G\end{pmatrix}\succeq0
\quad\hbox{and has zero Schur complement}.               \tag{259}
\]

The boundary-zero storage

\[
 \mathcal S_G(S)=s^TK_Gs=u^TGu\ge0                      \tag{260}
\]

has uniform-singleton source `Tr(K_G)/n`.  Unlike the affine storage, its
neutral drift contains a true Dirichlet dissipation.  Put

\[
 \mathcal E_G(S)=s^TK_G(I-P)s=u^TGTu\ge0,                \tag{261}
\]

\[
 A_G(S)=s^TK_Ga(S),\qquad
 D_G(S)=\sum_v(K_G)_{vv}t_v(S).                          \tag{262}
\]

Because `G` and `T` commute and have nonnegative spectral multipliers,
`(261)` has the asserted sign, and the labelled quadratic generator law is

\[
\boxed{
 L\mathcal S_G=-2\mathcal E_G+2A_G+D_G.}                \tag{263}
\]

Thus every exact degree-two pseudoflow satisfies the non-affine Thomson
budget

\[
\boxed{
 2\sum_S\bar\mu_S\mathcal E_G(S)
 =2\sum_S\bar\mu_SA_G(S)
  +\sum_S\bar\mu_SD_G(S)+{\operatorname {Tr}K_G\over n}.} \tag{264}
\]

This identity is not a mass-square gauge: its dissipation has spectral
multiplier `t(t-theta)^2/(theta-t/2)` and is strictly positive on every
non-complete spectral mode seen by the state.

The equality class is exact.  One has `K_G=0` if and only if `K_E=0`.  The
diagonal entries in `(257)` are

\[
 (K_E)_{vv}=\theta\pi_v\left(\pi_v-{1\over n}\right).   \tag{265}
\]

Hence `K_E=0` forces `pi_v=1/n` for every `v`; its off-diagonal entries then
force `P_vi=1/(n-1)` for `i\ne v`.  Conversely the complete kernel plainly
has `E=0`.  Therefore

\[
 \boxed{\operatorname {Tr}K_G=0
 \quad\Longleftrightarrow\quad P=P_{K_n}.}               \tag{266}
\]

Equations `(255)--(266)` supply the first full-pair spectral source which
vanishes exactly at the desired equality case and comes with an actual
Dirichlet square.  The remaining analytic obligation is to pay the
selection and flip terms `2A_G+D_G` in `(264)` while retaining adjacent-rank
transport; simply integrating `(263)` would, of course, use the identity in
the wrong direction.

### 7.24 Conditional selection contraction and the two-level remainder

The nonlinear selection vector admits an exact Hilbert decomposition which
interfaces with `(255)`.  For a fixed state, sample `v` from `pi` and write

\[
 S_0=s_v,\qquad X=x_v(S),\qquad
 A=a(X)={X(1-X)\over1+X}.                                \tag{267}
\]

Let `bar(a)_i=E(A | S_0=i)`, put `r=bar(a)_1-bar(a)_0`, and define

\[
 q_0=B\Pi^{1/2}a,\qquad
 \xi_v=\sqrt{\pi_v}\{a_v-\bar a_{s_v}\}.                \tag{268}
\]

Then

\[
\boxed{q_0=r u+\xi,\qquad
 \xi\perp\sqrt\pi,\quad\xi\perp u.}                    \tag{269}
\]

The scalar selection map is one-Lipschitz on `[0,1]`, since

\[
 a'(x)={1-2x-x^2\over(1+x)^2}\in[-1,1].                 \tag{270}
\]

Conditional variance contraction and the covariance matrix `(164)` now
give

\[
\boxed{
 \|\xi\|^2
 =E\{\operatorname {Var}(A\mid S_0)\}
 \le E\{\operatorname {Var}(X\mid S_0)\}
 =\mathcal D-{C^2\over V}.}                              \tag{271}
\]

The right side is interpreted as zero when `V=0`; for a transient state
`V>0`.  It is exactly the optimal covariance-Schur defect `(173)`.  In
spectral notation,

\[
 \mathcal D-{C^2\over V}
 =\min_{\lambda}\|(T-\lambda B)u\|_2^2.                 \tag{272}
\]

There is also a direct `W`-metric bound.  Since `a(x)^2<=x a(x)` and
`F\succeq (n-1)^{-1}B`,

\[
\boxed{
 \|q_0\|^2\le\mathcal W,qquad
 q_0^TF^{-1}q_0\le(n-1)\mathcal W.}                     \tag{273}
\]

Finally the Jensen envelope `(73)` has a quantitative full-pair remainder.
The conditional means of `X` are

\[
 \bar x_0={C\over1-M},\qquad
 \bar x_1=1-{C\over M}.                                 \tag{274}
\]

Put

\[
 Q_2(M,C)=(1-M)a(\bar x_0)+M a(\bar x_1).                \tag{275}
\]

Because `a''(x)=-4/(1+x)^3<=-1/2`, the function
`a(x)+x^2/4` is concave.  Conditional Jensen therefore proves the uniform
estimate

\[
\boxed{
 Q_2(M,C)-Q
 \ge {1\over4}\left(\mathcal D-{C^2\over V}\right).}    \tag{276}
\]

In particular the exact endpoint integrand has the pointwise lower bound

\[
\boxed{
 \kappa_nC-Q\ge
 \kappa_nC-Q_2(M,C)
 +{1\over4}\left(\mathcal D-{C^2\over V}\right).}       \tag{277}
\]

All graph dependence not already paid by the positive Schur variance has
now been compressed to the two-level envelope.  Writing
`lambda=C/V`, it is

\[
 {Q_2\over C}=
 {3-2\lambda+M\lambda
  \over(1+M\lambda)(2-\lambda+M\lambda)}.                \tag{278}
\]

The first term on the right of `(277)` still changes sign, including on
complete-graph ranks; it must be transported between ranks.  Thus `(277)`
does not prove the endpoint theorem by itself.  It isolates the remaining
minimal obstruction as a two-level rank-flow sign, while `(264),(269)--(273)`
provide the non-affine Thomson budget available to pay it.  No further
state-space search is needed to state that obligation.

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
- **PROVED:** the geometric cut coboundary `(59)` and the exact boundary
  extension formulation `(60)--(61)`.
- **PROVED:** the geometric conjugacy `(62)--(67)`, the degree-two matrix
  collision balance `(68)--(69)`, and the sharp local reversible Jensen
  bound `(73)`.
- **PROVED:** the two-request covariance representation `(76)--(77)`, the
  reversible square comparison `(78)--(79)`, and the exact collision SOS
  `(80)`.
- **EXACTLY REFUTED:** the restricted potential with rank constants,
  arbitrary rank-labelled vertex terms, and one global conductance
  coefficient, by the rational primal/dual pair `(81)--(82)`.
- **PROVED:** the fixed `L_pi,K_0` contraction identities `(83)--(93)`,
  including the sharp row-collision source and exact sign-indefinite
  two-step response.
- **PROVED:** the exact compressed rank-`H` dual `(94)--(95)` and the
  rank-dependent collision recurrence `(97)--(100)`.
- **EXACTLY REFUTED:** the universal implication `(95)` from rank mass,
  every rank one-mark balance, and one conductance-storage balance per rank,
  by the exact nine-vertex primal/dual pair `(120)--(123)`.
- **PROVED:** the pure-pair gauge, two internal-request storage laws,
  vector rank recurrence, sharp collision deficit, and fixed-pencil
  `M`-matrix/PSD factorization `(124)--(139)`.
- **PROVED:** the traceless boundary-neutral collision-excess decomposition
  and its exact rank Schur recurrence `(140)--(152)`; this is a reduction,
  not a sign theorem.
- **EXACTLY REFUTED:** the restricted potential with rank constants,
  arbitrary rank-labelled vertex terms, and one `K_0` coefficient per
  rank, by the exact nine-vertex rational primal/dual pair `(153)--(156)`.
- **EXACTLY REFUTED:** the combined rank-`H,K_0` potential with both pair
  coefficients independent on every rank and all rank-labelled one-marks,
  by the exact twelve-vertex rational primal/dual pair `(157)--(160)`.
- **EXACTLY COMPUTED:** the combined-certificate witness is itself strictly
  dB-suppressing at fitness two, by the exact harmonic solve `(161)`.
- **PROVED:** the sharp stationary target/request covariance inequality
  `C^2<=M(1-M)D`, its equality class, the mass-square drift, and the exact
  third-channel rank recurrence `(162)--(169)`.
- **PROVED:** the rank-aggregated covariance matrix, its optimal Schur
  tangent, and the boundary-zero variance-current recurrence
  `(171)--(177)`.
- **EXACTLY REFUTED:** the static rankwise covariance-tangent route, even
  after optimizing every rank coefficient independently, by the exact
  Green residuals `(180)--(181)`.  This does not refute the dynamic
  three-channel space `W_123`.
- **PROVED:** the pure-pair gauge for `M^2`, its nonnegative creation/debt
  recurrence and sharp stationary-mass deficit, and the all-vector
  three-channel operator square with unique complete-kernel equality class
  `(182)--(189)`.
- **PROVED:** the statewise and rank-aggregated mixed-current Schur cones
  `(190)--(195)`, retaining the exact stationary one-mark debt rather than
  replacing it by an unsigned scalar relaxation.
- **PROVED:** the canonical two-component boundary/current block
  `(196)--(214)`.  The first--third and second--first discrepancies are
  driven by `e` and `(I-P)e`, their one-mark debts have exactly the same
  heterogeneity boundary vector, and every scalar projection satisfies the
  sharp reversible Thomson-action bound.  This is a vector-flow reduction,
  not yet the missing rank-path sign theorem.
- **PROVED:** the rank-centred mass/request phase `(215)--(222)`.  It joins
  the two pair discrepancies into a common three-component oriented error
  and has an exact diagonal-mass plus spectral-endpoint kinetic metric
  entirely inside `W_123`.  The adjacent-rank transfer/Riccati sign is open.
- **PROVED:** the exact centered block-tridiagonal Bellman transfer
  `(223)--(230)`.  Its kinetic `p` block is positive, but the one-mark
  momentum `q` block is locally zero; the naive first backward Schur
  complement is therefore singular.  Any valid Riccati proof must retain
  nonlocal one-mark holdings or pass to a larger spectral/full-pair space.
- **PROVED:** the positive spectral conjugate `(231)--(244)`.  The
  boundary-zero `W_123` storage `theta V-C/2` is positive semidefinite and
  converts the full endpoint residual exactly into one integrated current
  sign `(241)`, with its singleton constant, rank transport, and equality
  normalization all explicit.
- **PROVED:** the affine spectral gauge collapse `(245)--(254)`.  The
  remainder in `(241)` is exactly
  `L{theta M^2-(theta-1/2)M}-(1-kappa_n)C`; after integration `(241)` is
  algebraically the endpoint theorem itself.  Hence the affine conjugate
  supplies a positive holding metric but no independent coercive sign.  A
  further spectral contraction must be non-affine or full-pair.
- **PROVED:** the canonical non-affine Green--Schur matrix `(255)--(266)`.
  Its rational quotient formula is PSD, vanishes exactly for the complete
  kernel, and its Green drift has a genuine nonnegative Dirichlet
  dissipation with exact positive source `Tr(K_G)/n` away from equality.
- **PROVED:** the conditional selection decomposition and contractions
  `(267)--(278)`.  Selection heterogeneity is bounded by the optimal
  covariance-Schur variance and by the `W` metric; strong conditional
  Jensen leaves only the explicit two-level envelope plus one quarter of
  that Schur variance.  The remaining sign is an adjacent-rank two-level
  transport problem, not another unexplored static ansatz.
- **PROVED:** the oriented rank-current identities `(103)--(107)` and the
  exact positive gradient reformulation `(108)--(111)` of the combined
  rank-`H,K_0` target.
- **EXACTLY REFUTED:** the vertex-forgotten scalar current cone, even after
  the natural event-moment bounds `(112)--(113)`, by the rational `n=3`
  relaxed point of flux `5/9`.
- **PROVED:** the internal-conductance creation/debt identity
  `(114)--(119)`, an exact reformulation of the now-refuted rank-`H`
  implication and a diagnostic component of the now-refuted combined
  route.
- **EXACTLY COMPUTED:** rank-dependent `H` and, separately, rank-dependent
  `K_0` both repair the exact 17-vertex global-coefficient witness, by the
  matching rational certificates `(96)` and `(102)`.
- **EXACTLY VERIFIED:** an independent rational implementation checks these
  identities and the dual balances on small weighted graphs, checks `(36)`
  on a genuinely directed rational kernel, and checks the new Green/current
  conjugacy and matrix balance without floating arithmetic.
- **NUMERICALLY OBSERVED ONLY:** the full rank-pair primal has remained below
  the complete baseline in the hostile searches in this directory.
- **NUMERICALLY OBSERVED ONLY:** the three-channel space `W_123` repairs the
  exact combined refuter and survived the first multiscale hostile cycle.
- **OPEN:** the universal cut bound `(25)`, hence universal feasibility of
  the rank-pair certificate and the universal fitness-two fixation theorem;
  equivalently, the summed collision inequality `(75)`.  Every tested
  one- and two-channel compression in this note is now exactly refuted.
  The full rank-pair matrix remains live; `W_123` is the smallest unrefuted
  intermediate space, but its universal validity is open.
