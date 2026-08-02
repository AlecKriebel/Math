# A uniform no-go for exchangeable active portals

Date: 2026-08-02 (America/Los_Angeles)

No literature search or external contact was used.  Every rate below is
derived directly from the two update rules.  This is a class obstruction,
not a universal theorem about arbitrary weighted graphs.

## 1. Construction and theorem

Fix an integer `Q>=2`.  Take portals `o_1,...,o_Q` and `s` disjoint strong
pairs `(x_i,y_i)`.  For parameters `c>0` and `theta>=0`, put

\[
 w(x_i,y_i)=1,
 \qquad
 w(o_a,x_i)=w(o_a,y_i)={c\over s},
 \qquad
 w(o_a,o_b)={2c\theta\over Q-1}\quad(a\ne b).       \tag{1}
\]

The graph is connected, including when `theta=0`, because every portal is
joined to every blade.  Write

\[
 g={\theta\over1+\theta}\in[0,1),
 \qquad
 x={2c\over1-g}.                                      \tag{2}
\]

Thus `g` is the portal-edge fraction of a portal's weighted degree and `x`
is the total blade load measured in units of the resident blade fraction.

Let

\[
 p=1-{1\over r}                                       \tag{3}
\]

be the common large-complete-graph limit.

**PROVED (all fixed portal counts).**  For every fixed `Q>=2`, `c>0`,
`theta>=0`, and `r>1`, the family (1) cannot asymptotically amplify both
Bd and dB.  More precisely, its rare-mutant establishment bounds satisfy

\[
 \alpha_B>p\quad\Longleftrightarrow\quad x>1
 \quad\Longleftrightarrow\quad 2c+g>1,                \tag{4}
\]

whereas `x>=1` forces

\[
 \alpha_D<p.                                          \tag{5}
\]

At `x=1`, Bd is exactly neutral at the limiting establishment level and dB
is strictly suppressing.  Hence all cases are covered.  Fixation is bounded
above by establishment, so one of the two update rules on the finite graphs
is eventually strictly suppressing relative to its complete-graph baseline.

The proof is uniform in `Q`: no constant in the central comparison degrades
as `Q` grows.  In fact, for every fixed `1<r<=2`, there is a positive gap
depending only on `r`, not on `Q,c,g`.  Put

\[
 x_* = r(2-r),\qquad
 x_m={1+x_*\over2}= {1+2r-r^2\over2}.                 \tag{6}
\]

If `x<=x_m`, the Bd establishment bound is at most `p-delta_B(r)`; if
`x>x_m`, the dB establishment bound is at most `p-delta_D(r)`, where the
positive gaps are given explicitly in Section 6.  This uniform dichotomy
also excludes growing sublinear portal counts whenever the stopped
strong-pair trace remains valid; a concrete graph corollary is stated in
Section 7.

**EXACTLY DERIVED (later sweep).**  At every blade-mutant density
`0<y<1`, averaging over the complete portal-count chain gives a blade
forward/backward rate ratio at least `r^3` under both rules, with strict
inequality when `g>0`.  Thus adding arbitrarily many exchangeable active
portals strengthens the later sweep but cannot repair the incompatible
rare-mutant entrance laws.

## 2. Exact strong-pair trace

A heterotypic blade resolves internally before another external event hits
that blade with probability `1-O(s^{-1})` for fixed `Q`.  Directly from the
two atomic update rules,

\[
 \Pr_B(\hbox{mutant pair}\mid\hbox{one mutant})
 ={r\over r+1}+O(s^{-1}),
 \qquad
 \Pr_D(\hbox{mutant pair}\mid\hbox{one mutant})
 ={1\over2}+O(s^{-1}).                                \tag{7}
\]

Uniform initialization starts at a portal with probability
`Q/(2s+Q)=o(1)`.

Suppose one monomorphic mutant blade is present and all portals are
resident.  Under Bd it starts a portal episode at rate

\[
 e_B={2Qrc\over s}+o(s^{-1})                           \tag{8}
\]

and is erased at successful rate

\[
 d_B={Q(1-g)\over s(r+1)}+o(s^{-1}).                  \tag{9}
\]

Under dB the corresponding rates are

\[
 e_D={Qr(1-g)\over s}+o(s^{-1}),
 \qquad
 d_D={Qc\over rs}+o(s^{-1}).                         \tag{10}
\]

Consequently the episode-to-parent-death ratios are independent of `Q`:

\[
 \kappa_B={2r(r+1)c\over1-g},
 \qquad
 \kappa_D={r^2(1-g)\over c}.                         \tag{11}
\]

Let `K` be the number of mutant portals during an episode.  Keep all states
`0,1,...,Q`, with zero absorbing.  Under Bd the exact changing and successful
child rates at `K=k` are

\[
\begin{aligned}
 d^B_k&=k\left(2c+{(Q-k)g\over Q-1}\right),\\
 u^B_k&={rk(Q-k)g\over Q-1},\\
 b^B_k&=k\,{r^2(1-g)\over r+1}.                       \tag{12}
\end{aligned}
\]

The first term in `d^B_k` is resident-blade reproduction into a mutant
portal.  The remaining up/down terms are the ordered portal edges.  A mutant
portal targets blades at rate `r(1-g)`, and the introduced mutant fixes its
pair with probability `r/(r+1)`, giving `b^B_k`.

For dB, direct fitness-weighted neighbor normalization gives

\[
\begin{aligned}
 d^D_k&=
 k\,{Q-1-g(k-1)\over Q-1+g(r-1)(k-1)},\\
 u^D_k&=
 {rk(Q-k)g\over Q-1+g(r-1)k},\\
 b^D_k&=krc.                                           \tag{13}
\end{aligned}
\]

For example, if a resident portal dies, its mutant portal-neighbor mass is
`rk theta/(Q-1)`, while its total neighbor mass is
`1+theta[Q-k-1+rk]/(Q-1)`.  Substitution of
`theta=g/(1-g)` gives `u^D_k`.  The down rate follows analogously.  A
resident blade endpoint copies a mutant portal at total rate `2krc` over all
blades, and the resulting singleton fixes its pair with probability `1/2`,
giving `b^D_k`.

For `U` in `{B,D}`, let `F^U_k(z)` be the PGF of the number of successful
mutant-blade children before the portal count next hits zero, starting at
`k`.  Then

\[
 F^U_0(z)=1,
\]

\[
 \{d^U_k+u^U_k+b^U_k(1-z)\}F^U_k
 =d^U_kF^U_{k-1}+u^U_kF^U_{k+1},                    \tag{14}
\]

with `u^U_Q=0`.  This tridiagonal system is the exact finite phase-type
episode transform; no portal-count state has been discarded.

The parent may survive an episode and initiate another.  Thus its total
lifetime-offspring PGFs are

\[
 D_B(z)={1\over1+\kappa_B\{1-F^B_1(z)\}},
 \qquad
 D_D(z)={1\over1+\kappa_D\{1-F^D_1(z)\}}.            \tag{15}
\]

Let `q_B,q_D` be their smallest fixed points.  The limiting establishment
bounds from a uniformly selected vertex are

\[
 \alpha_B={r\over r+1}(1-q_B),
 \qquad
 \alpha_D={1\over2}(1-q_D).                          \tag{16}
\]

Equations (12)--(16) are exact for every finite `Q`; their size grows only
linearly with the number of portal-count states.

## 3. A `Q`-uniform Bd barrier

Set

\[
 z_B={1\over r^2}.                                    \tag{17}
\]

At this value the marked-child rate is

\[
 b^B_k(1-z_B)=k(r-1)(1-g).                            \tag{18}
\]

Divide all episode rates by `1-g`, put `h=g/(1-g)`, and let

\[
 t={x\over x+r-1}.                                    \tag{19}
\]

Write `L_B` for the left side of the killed backward generator in (14), so
the true no-mark transform satisfies `L_B F=0`.  Direct substitution of

\[
 \phi_k=t^k,\qquad \phi_0=1                          \tag{20}
\]

gives the exact residual

\[
 (L_B\phi)_k=
 k\phi_k\,{(Q-k)h\over Q-1}
 { (r-1)^2(1-x)\over x(x+r-1)}.                       \tag{21}
\]

The transient matrix `-L_B` is a nonsingular `M`-matrix, so its inverse is
entrywise nonnegative.  Hence (21) and the common boundary value imply

\[
 F^B_1(z_B)\begin{cases}
 \ge t,&x<1,\\
 =1/r,&x=1,\\
 \le t,&x>1.
 \end{cases}                                          \tag{22}
\]

The inequalities needed below are strict away from `x=1`; when `g=0`, the
episode has only state one and equality with `t` holds, but the comparison
with `p` is still strict.

Put `H_B=1-F^B_1(z_B)`.  Since

\[
 \kappa_B=r(r+1)x,                                    \tag{23}
\]

the convex-PGF fixed-point test gives

\[
 \alpha_B>p
 \iff \kappa_BH_B>r^2-1
 \iff xH_B>{r-1\over r}.                             \tag{24}
\]

For `x<1`, (22) gives

\[
 H_B\le {r-1\over x+r-1},
 \qquad
 xH_B<{r-1\over r};                                  \tag{25}
\]

for `x>1` both comparisons reverse.  At `x=1`, equality holds.  This proves
(4) for every `Q` at once.

## 4. A backward-ratio envelope for dB

First work at the Bd threshold

\[
 c_0={1-g\over2}.                                     \tag{26}
\]

For `1<r<=2`, set

\[
 z_D={2-r\over r}.                                    \tag{27}
\]

At (26)--(27), the marked-child rate in the dB episode is

\[
 b^D_k(1-z_D)=k(r-1)(1-g).                            \tag{28}
\]

Let `F_k=F^D_k(z_D)` and define the positive backward ratios

\[
 R_k={F_{k-1}\over F_k}.                              \tag{29}
\]

Writing `a=(r-1)(1-g)` and dividing (13) by `k`, recurrence (14) becomes

\[
 R_k=1+{a+\bar u_k(1-R_{k+1}^{-1})\over\bar d_k},    \tag{30}
\]

where

\[
 \bar d_k={Q-1-g(k-1)\over Q-1+g(r-1)(k-1)},
 \qquad
 \bar u_k={r(Q-k)g\over Q-1+g(r-1)k}.                \tag{31}
\]

Define the explicit envelope

\[
 T_k=1+(r-1){Q-1+g(r-1)(k-1)\over Q-1}.              \tag{32}
\]

At the top state, `R_Q=T_Q`.  Moreover, exact simplification gives

\[
\begin{split}
T_k-&\left[1+{a+\bar u_k(1-T_{k+1}^{-1})\over\bar d_k}\right]\\
&={g^2k(Q-k)(r-1)^3\{Q-1+g(r-1)(k-1)\}\over
(Q-1)\{Q-1-g(k-1)\}\{r(Q-1)+gk(r-1)^2\}}\ge0.       \tag{33}
\end{split}
\]

The map on the right side of (30) is increasing in `R_{k+1}`.  Backward
induction from `Q` therefore proves

\[
 R_k\le T_k,\qquad R_1\le T_1=r.                     \tag{34}
\]

Consequently

\[
 F^D_1(z_D)={1\over R_1}\ge{1\over r},
 \qquad
 H_D(c_0):=1-F^D_1(z_D)\le p.                        \tag{35}
\]

This is the promised `Q`-uniform scalar certificate.  The apparent
high-count advantage of a nearly all-mutant portal network is absorbed by
the increasing envelope (32), while its first component remains exactly
`r`.

## 5. From the boundary to every Bd-amplifying load

For fixed `Q,r,g`, the dB portal-count path itself is independent of `c`.
Conditional on that path, put

\[
 A=\int_0^{\tau_0}K_t\,dt>0.                          \tag{36}
\]

Thinning successful children at `z_D` gives

\[
 H_D(c)=\mathbb E\left[1-e^{-2c(r-1)A}\right].       \tag{37}
\]

For every positive `A`, the function
`c -> (1-e^{-2c(r-1)A})/c` is strictly decreasing.  Thus

\[
 {H_D(c)\over c}\le {H_D(c_0)\over c_0}
 \le {2p\over1-g}\qquad(c\ge c_0).                  \tag{38}
\]

The dB fixed-point test reads

\[
 \alpha_D>p
 \iff
 {H_D(c)\over c}>
 {2(r-1)\over(2-r)r^2(1-g)}.                         \tag{39}
\]

But the right side of (39) is strictly larger than the last member of (38)
because

\[
 r(2-r)=1-(r-1)^2<1.                                 \tag{40}
\]

This proves (5) for `1<r<2`.  The same argument at `r=2` uses `z_D=0` and
gives a positive extinction probability, so `alpha_D<1/2=p`.  For `r>2`,
the entrance factor `1/2` in (16) is already strictly below `p`.

Notice that (35) and monotonicity also prove the stronger implication

\[
 x\ge r(2-r)\quad\Longrightarrow\quad\alpha_D\le p
 \qquad(1<r\le2).                                    \tag{41}
\]

Thus the Bd and dB suppressing regimes overlap on the nonempty interval
`r(2-r)<=x<=1`.

## 6. A parameter- and portal-uniform strict gap

The overlap in (41) yields a gap robust enough for growing parameter
sequences.  Fix `1<r<=2` and define `x_m` by (6).

If `x<=x_m`, (25) gives

\[
 \kappa_BH_B\le
 M_B(r):={r(r+1)x_m(r-1)\over x_m+r-1}<r^2-1.         \tag{42}
\]

Indeed,

\[
 r^2-1-M_B(r)
 ={(r-1)^4(r+1)\over4r-r^2-1}>0.                     \tag{43}
\]

Therefore

\[
 q_B\ge d_B^*(r):={1\over1+M_B(r)}>{1\over r^2},    \tag{44}
\]

and

\[
 \alpha_B\le {r\over r+1}\{1-d_B^*(r)\}
 =p-\delta_B(r),                                     \tag{45}
\]

where, in manifestly positive form,

\[
 \delta_B(r)=
 {r^2-1-M_B(r)\over r(r+1)\{1+M_B(r)\}}>0.          \tag{46}
\]

If `x>x_m`, use `H_D(c)<=H_D(c_0)<=p` for `x<=1`, and
(38) for `x>=1`.  Both cases give

\[
 \kappa_DH_D\le
 M_D(r):={2r^2p\over x_m}
 <{2(r-1)\over2-r}.                                  \tag{47}
\]

For `1<r<2`, the strict gap in (47) is

\[
 {2(r-1)\over2-r}-M_D(r)
 ={2(r-1)^3\over(2-r)(1+2r-r^2)}>0.                  \tag{48}
\]

At `r=2`, simply use the finite value `M_D(2)=8` and the comparison point
`z_D=0`; no division by `2-r` is needed.

It follows that

\[
 q_D\ge d_D^*(r):={1\over1+M_D(r)}>{2-r\over r},    \tag{49}
\]

and

\[
 \alpha_D\le {1\over2}\{1-d_D^*(r)\}
 =p-\delta_D(r),                                     \tag{50}
\]

with the particularly simple positive gap

\[
 \delta_D(r)={ (r-1)^3\over r(3r^2-2r+1)}.          \tag{51}
\]

The fixed-point inequalities used in (44) and (49) are elementary: if an
increasing PGF `D` has `D(z_0)>z_0`, then its smallest fixed point `q` obeys
`q>=D(z_0)`.

## 7. Fixed and growing portal-count graph consequences

For fixed `Q,c,g`, stop the graph chain when it reaches either zero or `K`
monomorphic mutant blades.  Before this stopping time, only `O(K)` blade
introductions and resolutions matter.  The probability of a repeated target,
an external interruption of a resolving pair, or a second parent changing
an already active portal episode is `o(1)` as `s->infinity`.  Deleting
self-loops and using the exact rates (8)--(13) gives entrywise convergence of
the stopped chain to the compound branching trace (14)--(15).  First take
`s->infinity`, then `K->infinity`, and grant immediate fixation at level
`K`.  This proves that fixation is bounded above by (16).  The strict gap in
Sections 3--5 then proves the fixed-`Q` graph theorem.

There is also a clean growing-portal corollary.  Let

\[
 Q_s=o(s),\qquad
 c_s={x_s(1-g_s)\over2},qquad
 0<x_-\le x_s\le x_+<\infty.                         \tag{52}
\]

The portal count `Q_s` may diverge and `g_s` may tend to one at an arbitrary
rate.  Couple the finite graph to its own exact `Q_s`-state trace, rather
than to a fixed limiting portal chain.  Up to a fixed blade cutoff `K`, pair
target collisions cost `O(K^2/s)`.  External interference with a specified
strong-pair resolution costs `O(Q_s/s)`.  While a portal episode is active,
the successful-child hazard per mutant portal is bounded below by a positive
constant times `1-g_s`; the parent-interference rate is bounded above by a
constant times `Q_s(1-g_s)/s`.  Stopping after `K` successful children or
portal extinction therefore makes the total coupling error `O_K(Q_s/s)+o(1)`.
Uniform initialization starts in the portal set with probability `o(1)`.

Hence the stopped trace is valid uniformly under (52).  Apply the uniform
dichotomy (42)--(51): for each fixed `1<r<=2`, either Bd or dB lies below
`p` by a gap depending only on `r`.  The passage from branching survival to
a finite cutoff is uniform as well.  If `q<1` is the extinction probability,
then `q^{Z_t}` is a martingale for the particle count.  Stopping at zero or
the first level at least `K` gives

\[
 \Pr(\tau_K<\tau_0)
 \le {1-q\over1-q^K}
 \le (1-q)+{1\over K};                                \tag{52a}
\]

the last inequality follows from
`q^K/(1+q+...+q^{K-1})<=1/K`.  The critical/subcritical
case follows by the `q->1` limit (or the particle-count supermartingale).
Choose `K` after the uniform gap and then let `s->infinity`.  For `r>2`, dB
fails by its entrance factor.  Thus no sequence satisfying (52), including joint
`Q_s->infinity` and `g_s->1`, is an asymptotically universal simultaneous
amplifier.

The regime `Q_s` comparable with `s`, or unbounded `x_s` without the direct
strong-pair condition `Q_sc_s/s->0`, is not covered by this graph corollary.
In those regimes the portal set has nonvanishing initialization mass or the
protected-pair trace itself can fail.  This is a trace-scale limitation, not
a weakness of the portal-count inequality: (21), (33), and the uniform gaps
hold for every finite `Q,c,g`.

As an additional singular audit, keep `g` fixed and let `Q->infinity` in the
dB boundary episode.  At every fixed portal count, the per-mutant birth,
death, and mark rates tend to

\[
 rg,\qquad1,\qquad(r-1)(1-g).                         \tag{53}
\]

The collision-free branching no-mark equation is

\[
 rgF^2-(r+g)F+1=0,                                   \tag{54}
\]

whose admissible root is `F=1/r`.  Thus the bound (35) becomes sharp as
`Q->infinity`, but the dB amplification threshold remains separated by the
strict factor `1/[r(2-r)]`.  A growing exchangeable portal network therefore
does not open an establishment window.

## 8. Post-establishment audit

Let `0<y<1` be the mutant-blade fraction and average over the fast portal
count.  Under Bd the portal-count birth--death rates are

\[
\begin{aligned}
 U^B_k&=r(Q-k)\left(2cy+{kg\over Q-1}\right),\\
 D^B_k&=k\left(2c(1-y)+{(Q-k)g\over Q-1}\right).      \tag{55}
\end{aligned}
\]

Under dB they are

\[
\begin{aligned}
 U^D_k&=(Q-k)
 {r\{(1-g)y(Q-1)+gk\}\over
  (Q-1)\{1+(r-1)(1-g)y\}+g(r-1)k},\\
 D^D_k&=k
 {{(1-g)(1-y)(Q-1)+g(Q-k)}\over
  (Q-1)\{1+(r-1)(1-g)y\}+g(r-1)(k-1)}.              \tag{56}
\end{aligned}
\]

Both chains are reversible birth--death chains.  Their adjacent stationary
ratios have the common form

\[
 {\pi_{k+1}\over\pi_k}
 ={r(Q-k)(A+gk)\over
   (k+1)\{B+g(Q-k-1)\}},                             \tag{57}
\]

where

\[
 (A,B)=
 \begin{cases}
 (2c(Q-1)y,\,2c(Q-1)(1-y)),&Bd,\\
 ((1-g)(Q-1)y,\,(1-g)(Q-1)(1-y)),&dB.
 \end{cases}                                         \tag{58}
\]

The same `pi` is stationary for the auxiliary rates

\[
 \widetilde U_k=r(Q-k)(A+gk),
 \qquad
 \widetilde D_k=k\{B+g(Q-k)\}.                       \tag{59}
\]

Equating their stationary total up and down rates gives, with `K~pi`,

\[
 B\,\mathbb E K
 =rA\,\mathbb E(Q-K)+(r-1)g\,\mathbb E[K(Q-K)].      \tag{60}
\]

Since `A/B=y/(1-y)` under both rules,

\[
 {\mathbb E K\over\mathbb E(Q-K)}
 \ge {ry\over1-y},                                   \tag{61}
\]

strictly when `g>0`.  Under either update rule the successful mutant-blade
gain/loss ratio is

\[
 R_U(y)=r^2{(1-y)\mathbb E K\over
                 y\mathbb E(Q-K)}\ge r^3>1.          \tag{62}
\]

This calculation retains every portal-count state.  It shows directly that
the no-go is caused by rare-mutant establishment, not by a hidden reverse
drift after establishment.

## 9. Verification and status

- `verify_multiportal_tradeoff.py` checks the exact dB rate conversion, the
  symbolic-`Q,k` Bd barrier residual (21), the top-state equality and
  symbolic-`Q,k` dB envelope gap (33), both uniform-gap factorizations, and
  both stationary adjacent ratios.  It independently builds and solves the
  exact tridiagonal transforms for `Q=2,...,7` at rational parameters.
- `check_finite_multiportal.py` independently constructs every finite atomic
  transition on the exact lumped state `(mutant portals, resident blades,
  heterotypic blades)`.  For example, at
  `Q=3,r=8/5,c=7/20,g=2/5`, the trace predicts
  `Bd=0.387948202767` and `dB=0.306411032031`; the finite-chain averages at
  `s=48`, obtained by numerically solving the exact lumped chain, are
  `Bd=0.385447019575` and `dB=0.309889503147`, respectively.
  The lumping is exact: arbitrary portal permutations, blade permutations,
  and independent endpoint swaps within each blade act transitively on all
  configurations with the same three counts, and every displayed atomic
  transition sum depends only on those counts.  At `Q=2` the generalized
  solver agrees entry-for-entry with the independent two-portal solver.
- `verify_finite_lumping_exact.py` makes that last statement independently
  checkable without floating-point linear algebra: at rational parameters it
  enumerates all 512 labelled subsets of a nine-vertex, three-portal graph,
  aggregates the atomic rates, and verifies exact agreement with the orbit
  generator for both update rules.
- `explore_multiportal.py` is numerical reconnaissance for the limiting
  trace only.  It was used to locate the envelope before the exact proof and
  is not part of the certificate.

**PROVED:** the all-`Q` phase-type trace, the Bd if-and-only-if threshold,
the dB backward-envelope obstruction, the parameter-uniform gap, the fixed
`Q` graph no-go, and the growing sublinear-portal corollary (52).

**EXACTLY COMPUTED:** all transition rates, lifetime-offspring transforms,
barrier residuals, gap factorizations, and the averaged post-establishment
drift inequality.

**OPEN:** portal sets of positive population proportion, nonexchangeable
portal networks, portal-specific blade incidence, and regimes in which the
strong-pair trace does not separate.  This theorem does not establish a
universal upper bound on `R_sim` for arbitrary weighted graph families.
