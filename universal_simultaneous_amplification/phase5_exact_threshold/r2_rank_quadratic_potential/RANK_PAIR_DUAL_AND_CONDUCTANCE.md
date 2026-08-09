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
`L_pi` suffice.  The combined rank-dependent `L_pi,K_0` problem remains
open.

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
argument proving `(111)`.  Dropping the individual vertex recurrences and
keeping only the scalar bounds `(105)--(107)` is far too weak, so any
continued-fraction or `M`-matrix proof must remain vertex marked.

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
compressed space contains both rank-`H` and rank-`K_0`; the full rank-pair
matrix remains the unconditional fallback.

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
below.  Thus the sharp surviving compressed conjecture is precisely

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
minimal surviving Schur problem.  It explains both why rank-`H` alone can
fail and why merely adding a fixed PSD inequality cannot repair it: the
additional channel acts only by moving signed collision excess between
ranks.  A closure must prove that this zero-total redistribution controls
the first-channel destruction debt in `(119)`.

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
- **PROVED:** the oriented rank-current identities `(103)--(107)` and the
  exact positive gradient reformulation `(108)--(111)` of the combined
  rank-`H,K_0` target.
- **EXACTLY REFUTED:** the vertex-forgotten scalar current cone, even after
  the natural event-moment bounds `(112)--(113)`, by the rational `n=3`
  relaxed point of flux `5/9`.
- **PROVED:** the internal-conductance creation/debt identity
  `(114)--(119)`, an exact reformulation of the now-refuted rank-`H`
  implication and a surviving component of the combined route.
- **EXACTLY COMPUTED:** rank-dependent `H` and, separately, rank-dependent
  `K_0` both repair the exact 17-vertex global-coefficient witness, by the
  matching rational certificates `(96)` and `(102)`.
- **EXACTLY VERIFIED:** an independent rational implementation checks these
  identities and the dual balances on small weighted graphs, checks `(36)`
  on a genuinely directed rational kernel, and checks the new Green/current
  conjugacy and matrix balance without floating arithmetic.
- **NUMERICALLY OBSERVED ONLY:** the full rank-pair primal has remained below
  the complete baseline in the hostile searches in this directory.
- **OPEN:** the universal cut bound `(25)`, hence universal feasibility of
  the rank-pair certificate and the universal fitness-two fixation theorem;
  equivalently, the summed collision inequality `(75)`.  The smallest live
  compressed potential has separate rank-dependent coefficients for both
  `H` and `K_0`; otherwise the full rank-pair matrix is required.
