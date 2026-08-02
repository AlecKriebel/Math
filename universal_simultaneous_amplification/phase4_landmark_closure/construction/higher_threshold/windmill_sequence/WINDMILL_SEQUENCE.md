# The heterogeneous-windmill sequence: a dB threshold of two and its Bd cost

Date: 2026-08-02 (America/Los_Angeles)

No literature search or external contact was used.  The trace equations and
asymptotic statements below are derived from the two update rules.  Numerical
searches are explicitly separated from proofs.

## 1. Outcome

The certified finite dB windmills at fitness `3/2`, `7/4`, and `9/5` do have
a scalable explanation.

**PROVED (dB-only asymptotic theorem).**  There is one fitness-independent,
computably explicit family of rational weighted pair windmills `W_N`, with
`2N+1` vertices, such that for every fixed `r>1`,

\[
 \rho_{\rm dB}(W_N,r)\longrightarrow {1\over2}.                 \tag{1}
\]

Consequently this family dB-amplifies every fixed `1<r<2` for all sufficiently
large `N`, and dB-suppresses every fixed `r>2`.  Thus the exact open limiting
interval of this windmill family is `(1,2)`.  No endpoint claim at `r=2` is
made.

The same family is unusable for simultaneous amplification:

\[
 \rho_{\rm Bd}(W_N,r)\longrightarrow0                           \tag{2}
\]

for every fixed `r>1`.  This is proved by a first-handoff bound, not inferred
from finite scans.

Topological support completion with dynamically negligible edges preserves
(1)--(2), but it does not repair local diffuseness: the collision functional
still tends to one.  Replacing pairs by growing clique blades does become
diffuse, but is dB-suppressing.  A non-clique growing diffuse replacement that
retains the dB booster mechanism while repairing Bd remains **OPEN**.

## 2. Pair windmills

There is one center `o` and `q` disjoint blades.  Blade `j` has vertices
`x_j,y_j`, with

\[
 w(o,x_j)=w(o,y_j)=a_j,
 \qquad w(x_j,y_j)=b_j.                         \tag{3}
\]

Put

\[
 p_j={a_j\over A},\quad A=\sum_j a_j,
 \qquad \lambda_j={a_j\over b_j}.               \tag{4}
\]

The strong-pair regime is `max_j lambda_j -> 0`.  Between rare outer events,
each pair is monomorphic.  A dB mutant introduced into an isolated pair fixes
with probability `1/2`; a Bd mutant fixes with probability `r/(r+1)`.  The
corresponding reverse probabilities are `1/2` and `1/(r+1)`.

Encode a monomorphic state by the center type `c` and the set `S` of mutant
blades.  Write

\[
 P_S=\sum_{j\in S}p_j,\quad
 \Lambda_S=\sum_{j\in S}\lambda_j.              \tag{5}
\]

## 3. Strong-pair dynamics

### 3.1 [PROVED] Leading death--birth hazards

After deleting a common global clock factor, the center-flip rates and the
successful blade-conversion hazards are

\[
\begin{array}{c|c}
\text{change}&\text{rate}\\ \hline
(0,S)\to(1,S)&{rP_S\over rP_S+P_{S^c}}\\[2mm]
(1,S)\to(0,S)&{P_{S^c}\over rP_S+P_{S^c}}\\[2mm]
(1,S)\to(1,S\cup\{j\})&r\lambda_j,\quad j\notin S\\
(0,S)\to(0,S\setminus\{j\})&\lambda_j/r,\quad j\in S.
\end{array}                                                     \tag{6}
\]

For example, when a resident blade vertex dies while the center is mutant,
the center wins the parent competition with probability
`r a_j/(b_j+r a_j)=r lambda_j+O(lambda_j^2)`.  There are two possible deaths,
and the introduced mutant fixes the pair with probability `1/2`, giving the
third line of (6).  The other lines follow identically from the dB rule.

Table (6) is deliberately called a hazard table, not the literal trace on
`(c,S)`.  During the order-one resolution of a heterotypic pair the center
can also die, so the return to the monomorphic state space can change both
coordinates.  This does not alter the leading probability `1/2` that the
pair resolves in either direction: after the first rare center-to-pair copy,
the identity of the first blade vertex to die is symmetric, and any further
center-to-pair copy has probability `O(max lambda_j)`.  The center coordinate
then mixes again before the next rare blade change.  Section 4 therefore
derives the blade generator directly rather than asserting an exact
`(c,S)`-trace that omits compound returns.

### 3.2 [PROVED BOUND; RETRACTED AS AN EXACT TRACE] Birth--death

The tempting isolated-excursion Bd rates are

\[
\begin{array}{c|c}
\text{change}&\text{rate}\\ \hline
(0,S)\to(1,S)&2r\Lambda_S\\
(1,S)\to(0,S)&2\Lambda_{S^c}\\
(1,S)\to(1,S\cup\{j\})&{r^2\over r+1}p_j,\quad j\notin S\\[1mm]
(0,S)\to(0,S\setminus\{j\})&{1\over r+1}p_j,\quad j\in S.
\end{array}                                                     \tag{7}
\]

Table (7) is useful reconnaissance but is **not an exact Bd trace**.  A center
birth into a blade occurs at order-one rate, so another center birth can occur
before that pair resolves.  Multiple excursions may overlap; the lumping
used for dB is invalid under Bd.  This issue was found during hostile audit
and the exact-trace claim was retracted.

The part needed below is rigorous.  With one fixed mutant blade `i` and a
resident center, mutant-pair births seed the center at leading rate
`2r lambda_i`.  Resident-center births target blade `i` at rate `p_i`.
After the first such introduction, the isolated reverse pair fixes with
probability `1/(r+1)`; further resident-center births only help erasure, while
mutant-pair seeding during that excursion is `o(1)`.  Thus

\[
 \Pr\{\hbox{seed center before erasure}\}
 \le 2r(r+1){\lambda_i\over p_i}+o(1).            \tag{7a}
\]

`search_windmill_macro.py` solves the separated dB generator represented by
(6), and retains (7) only as a labeled Bd diagnostic.  The independent
verifier checks convergence of its fixation values against the full subset
chain; it is a diagnostic supplement to the direct reduction below.

## 4. [PROVED] Fast-center dB reduction

Write

\[
 \lambda_j=\eta\ell_j
\tag{8}
\]

and send `eta -> 0` with `p,ell` fixed.  Conditional on a nonabsorbing blade
set `S`, the center equilibrates first.  Its mutant probability is

\[
 \pi(S)={rP_S\over rP_S+P_{S^c}}.                \tag{9}
\]

If the equilibrated center is mutant, a resident blade `j` receives a mutant
copy at leading rate `2r eta ell_j`; the pair subsequently becomes mutant
with probability `1/2`, even if the center changes during that excursion.
Its successful-conversion rate is therefore `r eta ell_j`.  The reverse
successful-conversion rate, conditional on a resident center, is
`eta ell_j/r`.  Averaging these two hazards using (9), then multiplying all
rates out of state `S` by the same positive factor, gives the blade-only
chain

\[
\boxed{
\begin{aligned}
 S\to S\cup\{j\}&:\quad R\ell_jP_S,\qquad j\notin S,\\
 S\to S\setminus\{j\}&:\quad \ell_jP_{S^c},\qquad j\in S,
\end{aligned}
\qquad R=r^3.}                                    \tag{10}
\]

This is a rank-one biased voter chain: `p_i` is the parent weight and
`ell_j` is the target clock.  Formula (10) is exact in the successive trace
limit and retains the entire path to absorption.

## 5. [PROVED] One booster squares fitness

Start with any finite chain (10), with old parent weights `p_i` and target
rates `ell_i`.  Add a new site `star`.  Let its parent weight dominate the
old total, and let its target clock be faster by an additional dominance
factor:

\[
 {p_\star\over\sum_i p_i}\longrightarrow\infty,
 \qquad
 {\ell_\star\min_i p_i
  \over p_\star\max_i\ell_i}\longrightarrow\infty.             \tag{11}
\]

The minimum in (11) is essential: it makes the new site fast even when the
old mutant or resident set consists only of the smallest-parent-weight site.

Conditional on the old set `S`, the fast new site has stationary mutant odds

\[
 {\Pr(\star=1\mid S)\over\Pr(\star=0\mid S)}
 ={RP_S\over P_{S^c}}.                           \tag{12}
\]

The new parent weight dominates every old replacement.  Averaging an old
target's two transition rates using (12) gives, up to a common state clock,

\[
 S\to S\cup\{j\}:R^2\ell_jP_S,qquad
 S\to S\setminus\{j\}:\ell_jP_{S^c}.             \tag{13}
\]

Thus eliminating one booster replaces `R` by `R^2`.  Empty and full old
states correspond to global extinction and fixation, so absorption
probabilities converge as well.  Choose the finite separations recursively
so the newest booster is eliminated first, then the next newest under the
already-squared fitness.  Repeating with `k` such boosters replaces `R` by

\[
 R^{2^k}=r^{3\,2^k}.                              \tag{14}
\]

All limits above are finite-state singular perturbations.  On any compact
fitness interval bounded away from one, convergence is uniform: after every
fast two-state averaging, all remaining changing rates and denominators are
continuous and bounded away from zero on the finite transient state space.

## 6. [PROVED] The dB threshold-two construction

For `N>=4`, take

\[
 q_N=N,\qquad k_N=\lfloor\sqrt N\rfloor,
 \qquad m_N=N-k_N.                                \tag{15}
\]

For the finitely many smaller indices use the unit-weight pair windmill;
they play no asymptotic role.  Begin with `m_N` ordinary blade sites having
unnormalized parent weight and target clock

\[
 \widetilde p_i=\ell_i=1.
\]

Given integers `K_h>=2`, add booster `h=1,...,k_N` recursively by

\[
\begin{split}
 \widetilde p_{m_N+h}&=K_h\sum_{i<m_N+h}\widetilde p_i,\\
 \ell_{m_N+h}
 &=K_h\,{\widetilde p_{m_N+h}\max_{i<m_N+h}\ell_i
              \over\min_{i<m_N+h}\widetilde p_i},
 \qquad
 p_i={\widetilde p_i\over\sum_j\widetilde p_j}.
\end{split}                                                     \tag{15a}
\]

Both dominance ratios in (11) are then exactly `K_h`.  Sending `K_1` to
infinity, then choosing `K_2` sufficiently large for that choice, and so on,
implements the successive limits of Section 5.  For the homogeneous ordinary
block, fixation from one mutant under effective fitness `Q` is

\[
 F_m(Q)={1-Q^{-1}\over1-Q^{-m}}.                  \tag{16}
\]

By Sections 4--5, the fixation probability of every ordinary mutant blade
can be made arbitrarily close to

\[
 F_{m_N}\!\left(r^{3\,2^{k_N}}\right).            \tag{17}
\]

Here is a canonical, fitness-independent choice of all finite scales.  Put
`epsilon_N=1/N` and use the rational compact interval

\[
 I_N=[1+1/N,\lfloor\sqrt N\rfloor].                \tag{18}
\]

Enumerate the integer tuples `(K_1,...,K_{k_N})` by maximum entry and then
lexicographically.  For each tuple, solve the finite chain (10) exactly and
write `Phi_{N,i}(r)` for fixation from blade `i`.  Choose the first tuple
satisfying

\[
 \left|\Phi_{N,i}(r)
 -F_{m_N}\!\left(r^{3\,2^{k_N}}\right)\right|<\epsilon_N
 \quad(i\le m_N,\ r\in I_N).                     \tag{18a}
\]

The successive-limit lemma and compact-uniform convergence guarantee that
this enumeration terminates.  Now set `a_j=widetilde p_j`,
`lambda_j=eta ell_j`, and `b_j=a_j/lambda_j`.  Let `L_N(r)` be the exact
`eta -> 0` limit of the uniformly averaged singleton fixation probability of
this full windmill.  It includes the finite entrance dynamics of an initially
heterotypic pair.  Enumerate `H=1,2,...` and choose the first `eta_N=1/H`
such that, throughout `I_N`,

\[
 \left|\rho_{\rm dB}(W_N(\eta_N),r)-L_N(r)\right|<\epsilon_N,
 \qquad
 \max_j\lambda_j<N^{-3},\qquad
 \max_{i\le m_N}{\lambda_i\over p_i}<N^{-3}.     \tag{18b}
\]

This second enumeration also terminates by the finite-state singular-limit
lemma.  All displayed weights are positive rational numbers and depend on
`N`, not on the eventual fitness.

The two searches above are exact decision procedures, not numerical tests.
The macro fixation values, `L_N`, and the full-chain fixation value are
rational functions of `r`: solve their finite absorbing systems over
`Q(r)`, and obtain `L_N` either from its finite limiting entrance chain or by
canceling the lowest power of `eta`.  Their denominators are nonzero for
`r>0`, because a connected finite chain is absorbed almost surely.  Their
sign is certified by a Sturm no-root count and one rational evaluation.
Each absolute-value test in (18a)--(18b) is consequently two strict
polynomial inequalities on the rational closed interval `I_N`; Sturm's
theorem decides both, including the endpoints.  Thus (15a), the stated
enumeration order, and the first-passing rule are a complete algorithmic
definition of `W_N`.  A compact closed-form tower would improve presentation,
but is not needed for explicit computability.

It remains to audit the uniform-singleton entrance carefully.  In the
`eta=0` entrance chain, start with one mutant at a vertex of blade `i` and a
resident center.  At a center death the mutant is selected with probability

\[
 q_i(r)={r p_i\over2+(r-1)p_i}.
\]

Ignoring deaths elsewhere, the next relevant death is at the center with
probability `1/3` and at one of the two blade vertices with probability
`2/3`.  Hence the probability that the center first becomes mutant before
the pair resolves is

\[
 h_i(r)={q_i(r)\over2+q_i(r)}\le {r p_i\over4}.   \tag{18c}
\]

On the complementary event, the two possible resolving blade deaths are
symmetric.  If `u_i(r)` is fixation from either singleton vertex of pair `i`,
then

\[
 \left|u_i(r)-\tfrac12\Phi_{N,i}(r)\right|\le h_i(r).           \tag{18d}
\]

Let `z_N(r)` be the limiting fixation value from a mutant center; only
`0<=z_N<=1` is needed.  Summing (18d), using `sum_i p_i=1`, gives the exact
population-level comparison

\[
 \left|L_N(r)-{z_N(r)+\sum_{i=1}^N\Phi_{N,i}(r)\over2N+1}\right|
 \le {r\over2(2N+1)}.                            \tag{18e}
\]

In particular, since every fixation value is at most one,

\[
 L_N(r)\le {N+1+r/2\over2N+1}.                   \tag{18f}
\]

Equations (18b) and (18f), uniformly for `r in I_N`, imply
`limsup rho_dB<=1/2`, because `sup I_N=O(sqrt(N))`.  Conversely, the ordinary
blades, (18a), and (18e) give the explicit lower bound

\[
 \rho_{\rm dB}(W_N,r)
 \ge {m_N\{F_{m_N}(r^{3\,2^{k_N}})-\epsilon_N\}-r/2\over2N+1}
       -\epsilon_N.                               \tag{19}
\]

The remaining diagonal quantifiers are also uniform.  For `r in I_N`,

\[
 r^{3\,2^{k_N}}
 \ge(1+1/N)^{3\,2^{k_N}},\qquad
 \log (1+1/N)^{3\,2^{k_N}}
 \ge {3\,2^{k_N}\over2N}\longrightarrow\infty. \tag{19a}
\]

Since `F_m(Q)>=1-Q^{-1}` for `Q>1`, its infimum in (19) tends to one;
also `m_N/N->1`, `sup I_N/N->0`, and `epsilon_N->0`.  The upper and lower
bounds therefore converge uniformly to `1/2` on `I_N`.  For every fixed
`r>1`, eventually `1+1/N<=r<=floor(sqrt(N))`, so the already chosen graph
`W_N` satisfies these bounds.  This proves (1) with the required order
`exists {W_N}`, `forall r`, `exists N_0(r)`, `forall N>=N_0(r)`.

Since the complete dB baseline tends to `1-1/r`, (1) gives strict asymptotic
amplification exactly when `1<r<2`, and strict suppression when `r>2`.

## 7. [PROVED] The same sequence kills Bd

Use the ordinary-blade scale condition already built into (18b),

\[
 {\lambda_i\over p_i}\le N^{-3}.                  \tag{20}
\]

Multiplying every `lambda_j` by a common smaller `eta_N` leaves the dB chain
(10) unchanged after time rescaling, which is why (20) was compatible with
the canonical selection in Section 6.

Suppose ordinary blade `i` is mutant and fixed, while the center and every
other blade are resident.  The rigorous excursion bound (7a) gives

\[
 \Pr\{\hbox{seed center before erasure}\}
 \le2r(r+1){\lambda_i\over p_i}+o(1).            \tag{21}
\]

Global fixation is impossible without that seed.  The ordinary blades make
up `1-o(1)` of all vertices, their contribution is `O_r(N^{-3})`, and the
center plus `k_N=o(N)` booster blades have vanishing initial mass.  The
rare-edge coupling transfers the same bound to the full windmill.  Therefore
`rho_Bd(W_N,r)->0`, proving (2).

This also explains the large Bd deficits of the certified finite dB
windmills: dB rewards large reproductive value `p_i/lambda_i`, while (21)
penalizes exactly its reciprocal.

### 7.1 [PROVED] Reversing the ratio destroys dB

One might instead impose `lambda_i/p_i -> infinity` on the density-one
ordinary blades, hoping to make the Bd center-seeding race favorable while
leaving a small exceptional booster set to drive dB fixation.  This cannot
work.  The exact two-state stopping calculation in
`MODIFIED_SCALE_AUDIT.md` proves, directly from the full dB rule, that a
singleton on blade `i` has fixation probability at most

\[
 3r(r+1){p_i\over\lambda_i}\qquad(\lambda_i\le1).              \tag{21a}
\]

The mutant must seed the resident center before the same center erases its
pair; no booster can act before that handoff.  Thus if the ratio diverges on
`N-o(N)` blades, their average dB contribution tends zero, while the booster
and center starts have vanishing population mass.  The proposed reversed
scale has `rho_dB -> 0` and is rigorously falsified.

### 7.2 [PROVED] Balanced ratios cannot be guarded by strong pairs

`BALANCED_GUARD_AUDIT.md` treats the remaining finite-ratio regime
`lambda_i/p_i -> c in (0,infinity)`.  Exact singleton handoff probabilities
give the necessary positive-margin window

\[
 {r-1\over2r}<c<{r^2(2-r)\over2(r-1)},           \tag{21b}
\]

which closes at
`r=(1+sqrt(2)+sqrt(2sqrt(2)-1))/2=1.8832035...`.
More decisively, no mesoscopic block of resident strong pairs can make
post-handoff fixation tend one under both rules.  dB requires its total
`sum lambda` to diverge in order to receive an offspring before center
reversion; Bd requires the same sum to vanish in order not to kill the mutant
center first.  The proof grants the first offspring immediate success and so
already covers overlapping introductions and arbitrary later sweeps.

### 7.3 [PROVED] Growing cliques do not repair the guard

The exponential reverse-stability of a mutant clique also fails to evade the
same first-establishment bottleneck.  `CLIQUE_GUARD_AUDIT.md` derives the
exact forward and reverse clique probabilities and all leading module rates.
If clique `j` has size `s_j` and per-vertex external/internal ratio
`theta_j`, dB fixation after a center seed forces
`sum_j s_j theta_j -> infinity`; Bd persistence of that center forces the
same sum to tend zero.  The reverse clique probability becomes exponentially
small only after establishment, too late to affect this contradiction.

## 8. Support completion and diffuse replacements

### 8.1 [PROVED] Negligible completion does not help

All missing edges may be added with positive rational weights below the
next rare scale.  The standard finite-state rare-event coupling makes the
fixation perturbation `o(1)`, so (1)--(2) survive and the support becomes
complete.

This does not satisfy the local-diffuseness condition.  At an ordinary pair
vertex,

\[
 P(\text{internal partner})={b_i\over b_i+a_i+o(b_i)}=1-o(1).
\tag{22}
\]

Since ordinary pair vertices have asymptotic density one, the collision
functional obeys

\[
 c(W_N)={1\over |V|}\sum_{u,v}P_{uv}^2\longrightarrow1,          \tag{23}
\]

not zero.  Any completion strong enough to force `c->0` must remove (22) and
therefore lies outside the proved pair trace.

For completeness, the temperature condition itself is not the problem.  The
two vertices of blade `j` have

\[
 t_{x_j}=t_{y_j}={1\over1+\lambda_j}+{p_j\over2},
 \qquad
 t_o=2\sum_j{\lambda_j\over1+\lambda_j}.          \tag{23a}
\]

Since `sum p_j=1`, the pair-vertex contribution to uniform mean
`|t-1|` is at most `(1+2 sum lambda_j)/(2N+1)`, and the single center also has
vanishing uniform mass under the chosen trace scale.  Thus `t->1` in uniform
`L^1`, while (23) shows `c->1`.  The windmill reaches the asymptotically
isothermal corridor but fails normalized local diffuseness maximally.

### 8.2 [PROVED NO-GO FOR THE NATURAL CLIQUE REPLACEMENT]

Replace every pair blade by a unit clique of size `s`, still separated from
the center on a rarer scale.  Its isolated dB singleton fixation average is

\[
 \alpha_s^{\rm dB}(r)
 ={s-1\over s}
 {1-r^{-1}\over1-r^{-(s-1)}}
 =\left(1-{1\over s}\right)\left(1-{1\over r}\right)
  +O_r(r^{-s}).                                   \tag{24}
\]

Even granting probability one for every later macro handoff, uniform
fixation is at most (24), apart from the negligible center mass.  If both the
number and size of blades diverge, this is below the complete-population dB
baseline by order `1/s`, whereas the complete finite-size correction is only
order `1/(qs)`.  Thus growing clique blades are eventually dB-suppressing.

The clique replacement has diverging support degree, `c->0`, and can be made
asymptotically isothermal, but it loses the local `1/2` establishment factor
that creates the threshold two.

### 8.3 Open diffuse branch

The arguments above do not exclude every non-clique growing diffuse blade.
A successful replacement would need all of the following simultaneously:

1. support degree diverging and normalized collision tending to zero;
2. local dB establishment exceeding the order-`1/s` complete-module loss;
3. the booster squaring mechanism after module resolution;
4. a Bd center-seeding probability not bounded by the reciprocal
   reproductive-value loss in (21);
5. control of the full post-establishment sweep.

No tested replacement met these requirements.  This general branch remains
**OPEN**, not universally excluded.

## 9. Verification and status

- `search_windmill_macro.py` builds and solves the separated dB generator
  represented by (6) and an explicitly nonrigorous Bd isolated-excursion
  surrogate.
- `verify_windmill_macro.py` checks convergence of that dB reduction against
  full subset chains, verifies the booster algebra and homogeneous formula
  symbolically, and tests representative finite booster hierarchies.
- `MODIFIED_SCALE_AUDIT.md` and `BALANCED_GUARD_AUDIT.md` give exact
  first-handoff obstructions for, respectively, divergent and finite
  ordinary ratios.
- `CLIQUE_GUARD_AUDIT.md` proves that exponentially persistent growing
  cliques cannot evade the post-seed coupling contradiction.

**PROVED:** the dB leading hazards and rank-one reduced chain, the Bd
first-handoff bound, booster squaring, the computably explicit dB limit `1/2`,
the Bd limit zero, the exact dB obstruction to reversing the ordinary scale,
the balanced-ratio handoff window and strong-pair guard no-go, failure of
negligible support completion to make `c->0`, the growing-clique guard no-go,
and the growing-clique replacement no-go.

**NUMERICALLY OBSERVED:** direct balanced trace searches through eight blades
at `r=1.51` remained below the infinite complete baseline; this is not used
in the proofs.

**OPEN:** the `r=2` finite correction, a simple closed-form diagonal scale
tower, and all non-clique diffuse replacements.
