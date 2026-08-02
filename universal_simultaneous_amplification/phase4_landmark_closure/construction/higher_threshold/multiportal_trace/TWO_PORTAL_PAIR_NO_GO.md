# A two-portal protected-pair no-go

Date: 2026-08-02 (America/Los_Angeles)

No literature search or external contact was used.  All rates below are
derived directly from the Bd and dB rules.  This is a class theorem, not a
universal obstruction for arbitrary graphs.

## 1. Construction and conclusion

Fix graph parameters `c>0` and `theta>=0`, independent of fitness.  For each
integer `s>=1`, take two portals `o_1,o_2` and `s` disjoint pair blades
`(x_i,y_i)`.  The nonzero weights are

\[
 w(x_i,y_i)=1,
 \qquad
 w(o_a,x_i)=w(o_a,y_i)={c\over s}\quad(a=1,2),
 \qquad
 w(o_1,o_2)=2c\theta .                         \tag{1}
\]

The graph is connected.  When `theta>0`, a one-portal mutant episode can
infect the second portal before either portal returns to the resident type;
the simultaneous-two-portal state therefore survives in the limiting trace.
Put

\[
 g={\theta\over1+\theta}\in[0,1).              \tag{2}
\]

Thus `g` is the fraction of a portal's Bd target weight carried by the other
portal, while `1-g` is its total blade fraction.

**PROVED (two-portal class obstruction).**  Let a uniformly selected initial
vertex carry the only mutant.  For every fixed `r>1`, `c>0`, and
`theta>=0`, at least one update rule has

\[
 \limsup_{s\to\infty}\rho_U(G_s,r)<p,            \tag{3a}
\]

where

\[
 p=1-{1\over r},                                \tag{3}
\]

is the common large-complete-graph limit.  Consequently this family cannot
eventually amplify both rules.  More precisely, if the Bd limiting
establishment bound exceeds `p`, then

\[
 2c+g>1,                                        \tag{4}
\]

and (4) forces the dB limiting establishment bound to be strictly
below `p` whenever `1<r<2`.  For `r>=2`, the initial dB strong-pair entrance
factor is already at most `p`.

The conclusion remains true if global fixation is granted immediately upon
reaching any diverging number of mutant blades.  It therefore does not rely
on identifying branching establishment with fixation.

The same proof is uniform when `c_s` stays in a compact subset of
`(0,infinity)` and `g_s` stays in `[0,1-epsilon]`.  Hence allowing the two
graph parameters to vary with `s` inside such a compact set does not evade
the obstruction: pass to a convergent subsequence and use the strict gap in
(3a).  Singular boundary scales `c_s->0`, `c_s->infinity`, or `g_s->1`
are not included in this corollary.

**EXACTLY DERIVED (post-establishment audit).**  The averaged blade-density
drift is nevertheless toward fixation for both rules.  If `y` is the mutant
blade fraction, the forward/backward rate ratios are

\[
 R_B(y)=r^3
 {2c\{1+(r-1)y\}+gr\over2c\{1+(r-1)y\}+g}>1,   \tag{5}
\]

and

\[
 R_D(y)=r^3
 {1+(r-1)\{y+g(1-y)\}\over
  1+(r-1)y(1-g)}>1.                             \tag{6}
\]

Thus the failure is entirely at rare-mutant establishment, not at the later
sweep.  Coupling the two portals strengthens the sweep but does not reconcile
the two entrance laws.

## 2. Strong-pair reduction

Give every vertex its independent continuous-time event clock.  Common
state-dependent factors do not affect absorption probabilities.  A
heterotypic blade resolves before another external event hits that blade
with probability `1-O(1/s)`.  Directly from the two update rules,

\[
 \Pr_B(\hbox{mutant pair}\mid\hbox{one mutant})
   ={r\over r+1}+O(s^{-1}),
 \qquad
 \Pr_D(\hbox{mutant pair}\mid\hbox{one mutant})
   ={1\over2}+O(s^{-1}).                        \tag{7}
\]

The reverse resolution probabilities are `1/(r+1)+O(1/s)` and
`1/2+O(1/s)`.  Uniform initialization lands in a blade with probability
`s/(s+1)`, so the two portal initial states contribute only `o(1)`.

Here is the precise stopped-limit statement used below.  Call a blade clean
when both of its endpoints have the same type.  For a fixed integer `K`, stop
the process when the number of clean mutant blades is zero or at least `K`.
Rescale time by `s` and collapse the order-one intervals during which a blade
is heterotypic or at least one portal is mutant.  Starting from one clean
mutant blade, the stopped process converges in law to a continuous-time
single-type branching process in which each individual

- initiates an independent portal episode at the leading rate `s e_U`;
- dies at the leading rate `s d_U`; and
- creates during each episode a batch with PGF `F_U` below.

This convergence follows directly from four uniform estimates below the
cutoff.  First, a heterotypic blade resolves in order-one time and suffers an
external intervention with probability `O(K/s)`.  Second, the two-state
portal episode has a finite mean duration (indeed an exponential tail),
uniformly while at most `K` blades are mutant.  Third, the rate at which a
second lineage starts an episode during an existing one is `O(K/s)`, and a
new child lands in an already-mutant blade with probability `O(K/s)`.
Finally, after deleting those exceptional events, every displayed rare rate
differs from its limiting per-individual rate by `O(K/s)` after the time
rescaling.  The killed limiting chain has finitely many population levels and
finite expected event count before it reaches `0` or `[K,infinity)`, so these
one-event errors sum to `o(1)`.  This proves convergence of the stopped
hitting probability, not merely of finite-dimensional marginals.

Let `H_{U,K}` be the limiting branching probability of reaching at least
`K` individuals before extinction.  Fixation of the finite graph requires
this stopped event, apart from an `o(1)` contribution from initial portal
mutants.  Consequently

\[
 \limsup_{s\to\infty}\rho_U(G_s,r)
 \le a_U H_{U,K},
 \qquad
 a_B={r\over r+1},\quad a_D={1\over2}.          \tag{7a}
\]

As `K->infinity`, `H_{U,K}` decreases to the survival probability of the
nonexplosive branching process.  Its family tree is Galton--Watson with
total-lifetime offspring PGF `D_U`, so this limit is `1-q_U`, where `q_U` is
the smallest fixed point of `D_U`.  Thus (7a) gives the establishment upper
bounds (15) and (23).  No assertion that establishment implies fixation is
made anywhere in the proof.

## 3. Exact Bd episode

Start with one monomorphic mutant blade and two resident portals.  The blade
seeds either portal at total rate

\[
 e_B={4rc\over s}+o(s^{-1}).                    \tag{8}
\]

The two resident portals erase it at total successful rate

\[
 d_B={2(1-g)\over s(r+1)}+o(s^{-1}).             \tag{9}
\]

Once exactly one portal is mutant, retain portal counts `1` and `2`.  Put

\[
 \beta_B={r^2(1-g)\over r+1},
 \qquad a_0=2c+g,
 \qquad a_1=rg.                                 \tag{10}
\]

The complete episode table is

\[
\begin{array}{c|c}
\text{event}&\text{rate}\\ \hline
1\to0&a_0\\
1\to2&a_1\\
2\to1&4c\\
\text{successful child from state }k&k\beta_B.
\end{array}                                     \tag{11}
\]

For example, the `2c` part of `a_0` is the total resident-blade birth rate
into the lone mutant portal, and the `g` part is reproduction by the resident
portal across the portal edge.  A mutant portal reproduces across that edge
at rate `rg`.  Its total birth rate into blades is `r(1-g)`, and the newly
introduced mutant fixes its pair with probability `r/(r+1)`, giving
`beta_B`.

Let `F_B(q)` be the probability generating function of the number of
successful mutant-blade children before the portals next hit zero, starting
from portal count one.  First-event conditioning on (11), with `u=1-q`,
gives

\[
 F_B(q)=
 {a_0(4c+2\beta_Bu)\over
  (a_0+a_1+\beta_Bu)(4c+2\beta_Bu)-4ca_1}.       \tag{12}
\]

The parent survives an episode and can initiate another one.  Hence the PGF
of its total lifetime offspring is

\[
 D_B(q)={1\over1+\kappa_B\{1-F_B(q)\}},
 \qquad
 \kappa_B={e_B\over d_B}\longrightarrow
 {2r(r+1)c\over1-g}.                            \tag{13}
\]

Its extinction probability `q_B` is the smallest root of

\[
 q_B=D_B(q_B).                                  \tag{14}
\]

The limiting Bd establishment probability from a uniformly selected vertex
is therefore

\[
 \alpha_B={r\over r+1}(1-q_B).                 \tag{15}
\]

The condition `alpha_B>p` is `q_B<1/r^2`.  A PGF is convex, so its smallest
fixed point lies below `q_0<1` exactly when `D(q_0)<q_0`.  Exact substitution
of `q_0=1/r^2` into (12)--(13) has positive denominator and numerator

\[
 (r-1)^2(r+1)(2c+g-1)(2c+2g+r-1).              \tag{16}
\]

The second variable factor is positive.  This proves the exact Bd criterion
(4).

## 4. Exact dB episode

With both portals resident, their deaths seed either portal from the mutant
blade at total rate

\[
 e_D={2r(1-g)\over s}+o(s^{-1}),                \tag{17}
\]

and resident portals erase the mutant blade at successful rate

\[
 d_D={2c\over rs}+o(s^{-1}).                    \tag{18}
\]

Define

\[
 h=1+(r-1)g,
 \qquad a={rg\over h},
 \qquad b_0={1-g\over h},
 \qquad \beta_D=rc.                             \tag{19}
\]

Here `a+b_0=1`.  The portal episode, including the simultaneous state, is

\[
\begin{array}{c|c}
\text{event}&\text{rate}\\ \hline
1\to0&1\\
1\to2&a\\
2\to1&2b_0\\
\text{successful child from state }k&k\beta_D.
\end{array}                                     \tag{20}
\]

For instance, when the resident portal dies in state one, the other portal
has fitness-weighted edge mass `r theta`, while resident blades have mass
one after normalization; this gives `a=r theta/(1+r theta)=rg/h`.

The episode PGF and total-lifetime offspring PGF are

\[
 F_D(q)={b_0+\beta_Du\over
 (1+a+\beta_Du)(b_0+\beta_Du)-ab_0},            \tag{21}
\]

\[
 D_D(q)={c\over c+r^2(1-g)\{1-F_D(q)\}}.        \tag{22}
\]

Let `q_D` be the smallest root of `q_D=D_D(q_D)`.  The dB limiting
establishment bound is

\[
 \alpha_D={1\over2}(1-q_D).                    \tag{23}
\]

For `1<r<2`, `alpha_D>p` is equivalent to

\[
 q_D<q_{0,D}={2-r\over r}.                      \tag{24}
\]

Cross-multiplying `q_{0,D}-D_D(q_{0,D})` leaves only positive probabilistic
denominators and a sign polynomial `E_r(c,g)`.  Set

\[
 x=c-{1-g\over2}.                               \tag{25}
\]

Exact simplification gives the following certificate:

\[
\begin{split}
E_r\left({1-g\over2}+x,g\right)
=-{ }&(1-g)(r-1)
 \left[r^2+g^2+r(r-1)^2g(1-g)\right]\\
&-2\{1+(r-1)g\}
 \left[r\{(r-1)^2+1\}(1-g)+2g\right]x\\
&-4(r-1)\{1+(r-1)g\}x^2 .                     \tag{26}
\end{split}
\]

Moreover,

\[
 \alpha_D>p\iff E_r(c,g)>0.                    \tag{27}
\]

If Bd amplifies, (4) says `x>0`.  Every term on the right side of (26) is
then strictly negative.  Hence dB does not amplify.  This proves the class
obstruction for `1<r<2`.  If `r=2`, (23) is strictly below `1/2=p`; if
`r>2`, its entrance factor `1/2` is already below `p`.

For completeness, the strict-gap cases proving (3a) are exhaustive.  If
`2c+g<1`, (16) gives `alpha_B<p`.  If `2c+g=1`, then `x=0` and the first
line of (26) gives `alpha_D<p`.  If `2c+g>1`, then `x>0` and all three lines
of (26) give `alpha_D<p`.  Since fixation is bounded above by the
corresponding establishment probability and the complete baselines converge
to `p`, one of the two finite graphs is eventually strictly suppressing.

At the requested reconnaissance fitness `r=8/5`, (26) specializes to

\[
 E_{8/5}=
 -{12(3g+5)\over25}x^2
 +{4(3g+5)(11g-136)\over625}x
 +{3(g-1)(53g^2+72g+320)\over625},              \tag{28}
\]

which is manifestly negative for `x>=0` and `0<=g<1`.

## 5. Post-establishment drift, without a one-portal shortcut

Now let a fraction `y` of the blades be mutant and average only over the
fast portal chain.  For Bd the portal-count birth--death chain has rates

\[
\begin{array}{c|c}
0\to1&4rcy\\
1\to0&2c(1-y)+g\\
1\to2&2rcy+rg\\
2\to1&4c(1-y).
\end{array}                                     \tag{29}
\]

For dB they are

\[
\begin{array}{c|c}
0\to1&\displaystyle {2ry\over ry+1-y+\theta}\\[2mm]
1\to0&\displaystyle {1-y+\theta\over ry+1-y+\theta}\\[2mm]
1\to2&\displaystyle {r(y+\theta)\over r(y+\theta)+1-y}\\[2mm]
2\to1&\displaystyle {2(1-y)\over r(y+\theta)+1-y}.
\end{array}                                     \tag{30}
\]

Both three-state chains are reversible because they are birth--death chains.
Writing their stationary portal count as `K`, their adjacent stationary
ratios give `E[K]/E[2-K]` directly.  A resident blade gains at a rate
proportional to `r^2 E[K]` relative to the loss coefficient multiplying
`E[2-K]` under both update rules.  Substitution yields (5)--(6).  In
particular both ratios are at least `r^3`, uniformly for `0<y<1`.

This calculation includes state `K=2`; replacing it by isolated one-portal
excursions would miss the `g`-dependent factors in (5)--(6).

## 6. Verification and status

- `verify_two_portal_tradeoff.py` reconstructs both episode PGFs, the exact
  Bd threshold numerator, the shifted dB certificate, its `r=8/5`
  specialization, and both post-establishment drift ratios using exact
  symbolic arithmetic.
- `verify_finite_lumping_exact.py` independently enumerates all 256 labelled
  mutant subsets for a rational eight-vertex instance.  From the atomic
  vertex rules it proves strong lumpability into the 30 portal/blade-count
  states and checks every Bd and dB quotient rate with exact fractions.
- `check_finite_two_portal.py` builds the exact finite lumped chain on portal
  count and the counts of resident, heterotypic, and mutant blades, then
  solves its absorption equations numerically.  This is an independent
  atomic-update audit of the limiting trace.  The lumping is exact: portal
  exchange, permutation of the blades, and independent endpoint exchange
  within every blade act transitively on configurations with the same four
  counts, and the displayed transition sums depend only on those counts.
- `search_two_portal.py` performs the labeled numerical reconnaissance.

**PROVED:** the exact two-portal rare-mutant trace and the no-overlap theorem
for the homogeneous protected-pair class (1).

**EXACTLY COMPUTED:** the portal episode PGFs, the two establishment sign
tests, and the post-establishment averaged drift ratios.

**NUMERICALLY OBSERVED:** finite-size convergence in the independent lumped
chain and the coarse `r=8/5` search margins.

**OPEN:** singular parameter scales, two nonexchangeable portals,
portal-specific blade incidence, or a growing internal portal network.  This
class theorem does not settle the global value of `R_sim`.
