# Terminal-chart Green--Foster duality with charged seams

**Proof-first composition lemma, 2026-08-12 PDT.**  This note gives a
self-contained theorem for composing local negative-or-exit episodes which
use different chart potentials.  It never forms a statewise-switched
Lyapunov function.  Instead, an infinite-mean-return hypothesis produces a
killed embedded Green occupation; finite terminal localization selects one
positive trace; and the proof uses only the one potential attached to that
trace.

There is one indispensable interface which must be stated rather than
assumed: zero *unweighted* structural-exit flux does not by itself control
the potential recharged while the path is outside a chart.  The required
quantity is a normalized **seam charge**.  Bounded episode words, uniformly
geometric finite phases, and uniform positive endpoint moments give a short
way to verify this charge, but only when they also cover every omitted
reentry phase.  Section 8 gives an irreducible counterexample showing that
local endpoint moments alone do not suffice.

The theorem below is an abstract composition result.  A network proof may
cite it only after its terminal-localization and seam-charge hypotheses have
been checked for the actual physical trace.

## 1. The certified embedded Green object

Let \(Y=(Y_n)_{n\ge0}\) be the embedded chain of genuine
population-changing transitions on a countable irreducible state space
\(E\).  Parallel physical labels may be retained.  Zero-displacement clocks
are not embedded jumps because they do not change the CTMC state.

Fix \(o\in E\), an increasing finite exhaustion \(D_m\uparrow E\), and

\[
 T_o^+=\inf\{n\ge1:Y_n=o\},\qquad
 \sigma_m=\inf\{n\ge0:Y_n\notin D_m\},\qquad
 \tau_m=T_o^+\wedge\sigma_m.                                \tag{1.1}
\]

If \(\mathbb E_oT_o^+=\infty\), then \(\tau_m\uparrow T_o^+\) and

\[
                         t_m:=\mathbb E_o\tau_m\longrightarrow\infty.
                                                                    \tag{1.2}
\]

For a labelled transition \(e\) enabled at \(x\), put

\[
 \nu_m(x,e)={1\over t_m}\,
  \mathbb E_o\sum_{n<\tau_m}
    {\bf1}_{\{Y_n=x,E_{n+1}=e\}}.                            \tag{1.3}
\]

Then \(\nu_m\) is a probability measure on labelled transitions.  For
every finite \(K\subset E\), irreducibility supplies, from each \(x\in K\),
a fixed positive-probability path to \(o\) before returning to \(x\).
Consequently the number of visits to \(x\) before \(\tau_m\) is uniformly
geometrically bounded, and

\[
             \sum_{x\in K,e}\nu_m(x,e)\longrightarrow0.      \tag{1.4}
\]

For every bounded \(f:E\to\mathbb R\), pathwise telescoping gives

\[
 \sum_{x,e}\nu_m(x,e)\{f(x+\zeta_e)-f(x)\}
 ={\mathbb E_o[f(Y_{\tau_m})-f(o)]\over t_m}
 \longrightarrow0.                                         \tag{1.5}
\]

Thus an infinite mean return produces an escaping probability occupation
with exact asymptotic finite-partition balance.  No time normalization and
no bound on mass-action intensities is used.

If a faster neutral source layer has infinite raw count while the first
changing layer is slower, one applies the same construction to the exact
physical trace at that next layer.  A finite killed Green matrix contracts
the intervening neutral phase.  A layer with bounded expected count is
deleted; a layer with diverging count is normalized by that count.  Since
the source flag is finite, this lexicographic procedure terminates.  In the
rest of the note, **Green trace** means either (1.3) or one such certified
source-layer trace.  A certified slower trace includes the analogue of
(1.4): its normalized start count on every fixed finite state set tends to
zero.

## 2. What finite terminal localization proves

Push a Green trace to finitely many chart nodes after fixing its discrete
data and one member of a finite compact ratio cover.  Let \(F_m(a,b)\) be
the normalized expected number of retained transitions from node \(a\) to
node \(b\).  Indicator tests in (1.5) give, after subsequence extraction,

\[
       \sum_b F(a,b)=\sum_bF(b,a)\qquad(a\text{ a chart node}). \tag{2.1}
\]

The directed graph of positive limiting flows is a finite circulation.
Its condensation is acyclic.  Summing (2.1) over a source component shows
that the component has zero outgoing flow; removing it and iterating shows
that no positive-flow edge can join distinct strongly connected components.
Hence some positive-mass component has zero limiting structural-exit flux.

Inactive-coordinate boxes and compact ratio cells are handled by an
\(\varepsilon\)-localization and a diagonal limit.  Every omitted transition
must be retained as a named exit -- box exit, active-set promotion, support
or flag change, shell crossing, or structural-rank change.  The resulting
trace has an expected retained count \(r_m\to\infty\) and exit count \(q_m\)
satisfying

\[
                              {q_m\over r_m}\longrightarrow0. \tag{2.2}
\]

Equation (2.2) is the exact content of **unweighted terminality**.  It is
enough for bounded rewards.  It is not by itself enough for an unbounded
chart potential.

## 3. Nonoverlapping episode traces

Fix one terminal chart component and one function

\[
                              V:E\longrightarrow[0,\infty).  \tag{3.1}
\]

Only this \(V\) will be used.  It need not agree with the potential attached
to any other chart.

On each killed physical path choose, recursively and without overlap,
stopping-time episode intervals

\[
  \sigma_{m,0}<\rho_{m,0}\le\sigma_{m,1}<\rho_{m,1}
       \le\cdots\le\sigma_{m,N_m-1}<\rho_{m,N_m-1}\le\tau_m. \tag{3.2}
\]

Here every start and endpoint is a stopping time for the physical-path
filtration, and \(\{j<N_m\}\) is measurable at
\({\cal F}_{\sigma_{m,j}}\).  Thus conditional episode estimates may be
summed over the random episode list without an anticipative selection.

The reaction causing an episode exit is included in that episode.  Its
actual endpoint is \(Y_{\rho_{m,j}}\); it is never counted again as the
first transition of the next episode.  Put

\[
 A_m=\mathbb E N_m,\qquad
 D_{m,j}=V(Y_{\rho_{m,j}})-V(Y_{\sigma_{m,j}}).               \tag{3.3}
\]

Let \(Q_m\) be the expected number of episodes which record a named
structural exit.

The retained trace count transfers to episode starts under the following
elementary condition.  If the episodes tile the retained trace except for
one uniformly integrable partial episode, every episode contains at least
one trace event, and its conditional expected trace length is at most
\(L<\infty\), then

\[
             A_m\le r_m,\qquad r_m\le L A_m+O(1).              \tag{3.4}
\]

Thus \(A_m\to\infty\), and (2.2) implies

\[
                              {Q_m\over A_m}\longrightarrow0. \tag{3.5}
\]

The same conclusion holds when a bounded word is followed by a finite
phase whose reaction count is dominated uniformly by a geometric random
variable.  More generally, (3.4) itself is the exact interface needed from
the trace theorem.  A rare source layer whose physical waiting count is not
uniformly bounded must first be promoted to its own certified Green trace;
it may not be discarded using (3.4).

## 4. The seam charge

The intervals in (3.2) need not be adjacent.  Define the positive recharge
across the omitted gap after episode \(j\) by

\[
 G_{m,j}=\bigl[V(Y_{\sigma_{m,j+1}})
                    -V(Y_{\rho_{m,j}})\bigr]^+               \tag{4.1}
\]

and define the total entrance/seam charge

\[
 B_m=V(Y_{\sigma_{m,0}})
       +\sum_{j<N_m-1}G_{m,j},                                \tag{4.2}
\]

with \(B_m=0\) when \(N_m=0\).  A direct pathwise telescoping identity gives

\[
 \begin{split}
  \sum_{j<N_m}D_{m,j}
   &=V(Y_{\rho_{m,N_m-1}})-V(Y_{\sigma_{m,0}})\\
   &\quad-
     \sum_{j<N_m-1}
       \{V(Y_{\sigma_{m,j+1}})-V(Y_{\rho_{m,j}})\}\\
   &\ge-B_m.
 \end{split}                                                   \tag{4.3}
\]

The load-bearing weighted terminality condition is

\[
                              {\mathbb E B_m\over A_m}
                                      \longrightarrow0.       \tag{4.4}
\]

Unlike a comparison inequality between two chart potentials, (4.4) is
needed only on the single Green trace selected in Section 2.  It says that
the selected potential cannot be recharged at linear order during the
vanishing family of omitted seams.

## 5. Local negative-or-exit contract

Assume the finite menu of episode rules divides starts outside a finite set
into **drift starts** and **exit starts**.  There are constants

\[
              \delta>0,\qquad \varepsilon>0,\qquad p>1,
              \qquad C_p<\infty                              \tag{5.1}
\]

such that, conditional on the episode-start sigma field,

\[
 \begin{array}{ll}
 \mathbb E[D_{m,j}\mid{\cal F}_{\sigma_{m,j}}]\le-\delta,
     &\text{at a drift start},\\[2mm]
 \mathbb P\{\text{the episode records a structural exit}
                \mid{\cal F}_{\sigma_{m,j}}\}\ge\varepsilon,
     &\text{at an exit start},\\[2mm]
 \mathbb E[((D_{m,j})^+)^p\mid{\cal F}_{\sigma_{m,j}}]\le C_p,
     &\text{at every start}.
 \end{array}                                                   \tag{5.2}
\]

The first line may be replaced by the stronger physical-time inequality

\[
 \mathbb E[D_{m,j}+\eta\theta_{m,j}\mid
                    {\cal F}_{\sigma_{m,j}}]\le-\delta,       \tag{5.3}
\]

where \(\theta_{m,j}\ge0\) is the episode duration.  The duration term can
simply be dropped in the embedded Green contradiction.

Finite exceptional start states have \(o(A_m)\) occupation by (1.4).
They may be added to the exit-start count provided their positive endpoint
increments satisfy the last line of (5.2).

## 6. Terminal Green--Foster duality

> **Theorem 6.1 (charged-seam terminal duality).**  Suppose an infinite-mean
> embedded return produces a terminal trace satisfying (3.2)--(3.5).  If
> one chart potential and its physical all-clock episode menu satisfy the
> seam condition (4.4) and the local contract (5.2), then that terminal
> trace cannot exist.

### Proof

Let \(K_m\) be the expected number of exit starts and finite-exception
starts.  Every exit start has conditional probability at least
\(\varepsilon\) of contributing to the recorded exit count.  Therefore

\[
 K_m\le\varepsilon^{-1}Q_m+o(A_m)=o(A_m).                    \tag{6.1}
\]

Sum conditional expectations over the random, adapted episode list.  The
drift starts contribute at most

\[
                         -\delta(A_m-K_m).                    \tag{6.2}
\]

At an exceptional start, discard the negative part.  Conditional
Hölder in (5.2) gives

\[
 \mathbb E[(D_{m,j})^+\mid{\cal F}_{\sigma_{m,j}}]
                         \le C_p^{1/p}.                       \tag{6.3}
\]

Hence all exceptional starts contribute at most
\(C_p^{1/p}K_m=o(A_m)\).  Combining this with (6.2),

\[
 \limsup_{m\to\infty}{1\over A_m}
   \mathbb E\sum_{j<N_m}D_{m,j}\le-\delta.                   \tag{6.4}
\]

On the other hand, (4.3)--(4.4) give

\[
 \liminf_{m\to\infty}{1\over A_m}
   \mathbb E\sum_{j<N_m}D_{m,j}\ge0,                         \tag{6.5}
\]

a contradiction. \(\square\)

The proof never evaluates a second chart potential.  It also never follows
an exit and then assigns the exit transition to a new Lyapunov rule.  The
exit transition is charged once by the old episode; any later reentry is
represented explicitly in \(B_m\).

### Corollary 6.2 (finite library with different potentials)

Suppose a certified finite terminal localization has chart components
\(\mathfrak C_1,\ldots,\mathfrak C_J\).  Component \(j\) may use its own
nonnegative potential \(V_j\).  Suppose either the desired positive
recurrence of the fixed class has already been established by an independent
classwise theorem, or every positive terminal trace either

1. is impossible in its fixed communicating class by a supplied invariant;
2. satisfies Theorem 6.1 using only \(V_j\).

In the first alternative the supplied classwise conclusion is already
available.  In the second, the embedded chain has finite expected positive
return to \(o\); the CTMC hypotheses in Section 9 then give physical
positive recurrence.

Indeed, in the first alternative there is nothing to prove.  In the second,
infinite mean embedded return would give one positive terminal component by
Sections 1--2, and both displayed cases are impossible.  Notice that a
theorem supplying only an arbitrary invariant probability for a
continuous-time chain is not silently treated as an invariant probability
for its embedded jump chain: an independently routed result must prove the
desired classwise recurrence itself.  No function of the form
\(V_{\alpha(x)}(x)\) is constructed.

## 7. Practical verification of the seam condition

The following criterion is sufficient for (4.4).

> **Lemma 7.1 (geometric-seam criterion).**  Suppose every gap in (4.1)
> begins with a recorded structural exit, so the expected number of gaps is
> at most \(Q_m+O(1)\).  Suppose, conditional on each gap entrance, its total
> positive \(V\)-recharge \(G\) satisfies
> 
> \[
>                              \mathbb E G\le C_G              \tag{7.1}
> \]
> 
> uniformly, and suppose
> 
> \[
>                 \mathbb E V(Y_{\sigma_{m,0}})=o(A_m).       \tag{7.2}
> \]
> 
> Then (3.5) implies (4.4).

The proof is immediate:

\[
 \mathbb E B_m\le o(A_m)+C_G\{Q_m+O(1)\}=o(A_m).             \tag{7.3}
\]

Condition (7.1) follows, for example, when the omitted reentry phase contains
a number \(R\) of physical subepisodes with a uniform conditional geometric
tail, and every subepisode has a uniformly bounded conditional \(p\)-th
moment, for some \(p>1\), of its positive \(V\)-increment.  If \(a_k\) is
that positive increment and \(\{k\le R\}\) is measurable before subepisode
\(k\), conditional Hölder and Tonelli give

\[
 \mathbb E G\le\sum_{k\ge1}\mathbb E[
                   {\mathbf{1}}_{\{k\le R\}}a_k]
       \le C_p^{1/p}\sum_{k\ge1}\mathbb P\{k\le R\}
       =C_p^{1/p}\mathbb ER\le C_G.                          \tag{7.4}
\]

Thus (7.1) holds without independence.  The predictable-entry qualification
prevents a retrospectively selected large increment from entering the sum.

Condition (7.2) is the one initial-boundary term.  It can be certified by a
lower-cut averaging argument, by a uniformly integrable entrance kernel, or
by closing the trace cyclically and proving that the resulting positive
closing toll is \(o(A_m)\).  It does **not** follow from unweighted terminal
flow alone.

There is an exact measure-theoretic version of the required endpoint
uniform integrability.  Under the preceding hypothesis that every omitted
gap begins a new chart run, let \({\cal R}_m\) contain the first episode of
every maximal consecutive run, and define the normalized boundary
subprobability

\[
 \beta_m(H)={1\over A_m}\,
   \mathbb E\sum_{j\in{\cal R}_m}{\bf1}_{\{Y_{\sigma_{m,j}}\in H\}}.
                                                                  \tag{7.5}
\]

Zero unweighted entry/exit flux gives only \(\beta_m(E)\to0\).  The precise
additional condition is

\[
 \lim_{R\to\infty}\limsup_{m\to\infty}
       \int_{\{V>R\}}V\,d\beta_m=0.                              \tag{7.6}
\]

Indeed,

\[
 \int V\,d\beta_m
 \le R\beta_m(E)+\int_{\{V>R\}}V\,d\beta_m\longrightarrow0,       \tag{7.7}
\]

first in \(m\) and then in \(R\).  Since
\[
 B_m\le\sum_{j\in{\cal R}_m}V(Y_{\sigma_{m,j}}),
\]
condition (7.6) implies (4.4).  A convenient stronger hypothesis is, for
some \(\gamma>0\),

\[
                  \sup_m\int V^{1+\gamma}\,d\beta_m<\infty.      \tag{7.8}
\]

Hölder and \(\beta_m(E)\to0\) then imply (7.7).  This is the rigorous sense
in which a **positive chart-entry endpoint moment** closes the composition.
It concerns the new chart's potential value at rare entries.  It is strictly
stronger than the last line of (5.2), which controls only the positive
increment of an episode already running in that chart.

In an application, bounded designated paths and finite bounded-coordinate
phases should be appended inside the episode, not hidden in a chart handoff.
Their all-fixed positive endpoint moments establish (5.2), while a uniform
geometric phase establishes (3.4).  A phase whose expected reaction count
diverges belongs to the next source-layer Green trace and must be normalized
there.  These rules make every physical transition either an episode
transition, a contracted neutral transition with zero \(V\)-charge, or an
explicit term of \(B_m\).

## 8. Why zero exit flux and local moments are not enough

The seam condition cannot be deleted.  Here is an irreducible transient
counterexample with bounded jumps and one-step episodes.

Enumerate a ray by alternating blocks

\[
 A_{m,0},A_{m,1},\ldots,A_{m,m},
 B_{m,0},B_{m,1},\ldots,B_{m,m}\qquad(m=1,2,\ldots).        \tag{8.1}
\]

On this ray take the nearest-neighbour birth--death chain which moves one
place to the right with probability \(p=3/4\) and one place to the left with
probability \(q=1/4\), with reflection at the first state.  The chain is
irreducible and transient.  Its expected positive return to the first state
is infinite.

Use the two chart labels \(A\) and \(B\).  On an \(A\)-block put

\[
                           V_A(A_{m,k})=2m-k,                  \tag{8.2}
\]

and on a \(B\)-block put

\[
                           V_B(B_{m,k})=2m-k.                  \tag{8.3}
\]

For the \(A\)-trace extend \(V_A\) by zero off the \(A\)-blocks, and do the
analogous thing for \(V_B\).  Thus each is one nonnegative function on the
whole state space, not a new function chosen at every block.  Each is proper
on its own chart: throughout the \(m\)-th block its value lies between \(m\)
and \(2m\).

At every nonboundary point of either block, the corresponding one-step
potential drift is

\[
                  p(-1)+q(+1)=q-p=-\tfrac12.                 \tag{8.4}
\]

At the two endpoints of a block, declare the cross-block move a structural
exit.  Every positive increment of a one-step episode which already starts
inside its selected chart is at most one.  The large incoming increment is
instead the seam toll isolated below.  Up to distance \(R\), there are only
\(O(\sqrt R)\) block boundaries but
\(\Theta(R)\) expected transition occupation.  Therefore both chart traces
have zero normalized unweighted exit flux and strict local negative drift,
with bounded episode length and every positive increment moment.

For completeness, stop the chain on hitting either the first state or the
state at distance \(R\).  With \(r=q/p=1/3\), the gambler's-ruin probability
of reaching \(R\) from distance one is

\[
                 {1-r\over1-r^R}\longrightarrow1-r>0.         \tag{8.5}
\]

On this event at least \(R-1\) jumps occur.  It also visits every intervening
site, so each chart contributes \(\Omega(R)\) occupation because its blocks
fill an asymptotically positive fraction of the ray.  Conversely, optional stopping
of position minus \((p-q)n\) gives expected stopped length at most
\(R/(p-q)\).  Hence the killed Green mass is \(\Theta(R)\).  The expected
number of visits to any fixed site before this stopping time is bounded by
the full transient-walk Green constant, uniformly in the site and \(R\).
There are \(O(\sqrt R)\) block endpoints and asymptotically half of the
remaining sites have each chart label.  This proves both the stated
positive-mass and zero-exit-fraction estimates.

Nevertheless the chain is transient.  On entering the next block, its chart
potential is recharged from zero to a value between \(m\) and \(2m\).
Summed through the first
\(M\) blocks, the seam charge is

\[
                         \sum_{m\le M}m=\Theta(M^2),           \tag{8.6}
\]

On the event in (8.5), every intervening block is crossed, so the expected
charge in (8.6) is \(\Theta(R)\), the same order as the episode count.  Thus
(4.4) fails exactly.  This example
also shows why a finite chart graph whose cross-edge *frequency* vanishes
does not permit potentials to be switched for free.

## 9. CTMC closure

Assume the embedded chain is the genuine jump chain of a nonexplosive CTMC.
If every nonabsorbing state has total changing-transition rate at least
\(\lambda_*>0\), then a return using \(N\) embedded jumps has conditional
expected physical duration at most \(N/\lambda_*\).  Corollary 6.2 therefore
gives finite expected physical return.  A finite reaction network has such
a lower bound on a fixed nontrivial class whenever every enabled falling
factorial is an integer at least one and the positive labelled rates have a
positive minimum.

The standard return-cycle occupation measure then yields an invariant
probability, and irreducibility gives positive recurrence.  Nonexplosion is
a separate input; for binary networks it follows from the linear bound on
all population-increasing source rates.

## 10. Publication checklist

A use of Theorem 6.1 must pin all of the following.

1. The killed labelled Green occupation or exact slower source-layer trace.
2. A finite terminal localization with positive retained trace mass and
   zero unweighted exit fraction.
3. A nonoverlapping physical episode partition, including activation and
   exit-causing transitions once.
4. Bounded or uniformly geometric trace length, or the literal comparison
   (3.4).
5. One potential on the selected terminal component, a uniform drift margin
   or uniform exit probability, and a uniform positive endpoint moment.
6. The weighted seam condition (4.4), preferably via Lemma 7.1.
7. Actual physical endpoints and, for CTMC recurrence, physical-duration
   integrability and nonexplosion.

Items 1--5 without item 6 are not a Green/Foster composition theorem.  The
counterexample in Section 8 is an exact obstruction, not a technicality.
