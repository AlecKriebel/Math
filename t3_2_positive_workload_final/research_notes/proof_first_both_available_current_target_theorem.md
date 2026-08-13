# The both-available all-clock current-target theorem

**Proof-first scoped theorem, 2026-08-12 PDT.**  This note closes only the
terminal two-active chart in which **both** active linkages are in the
available branch of the certified top-complex alternative.  It does not
claim that an available linkage can be paired generically with a shielded
linkage; those interfaces are treated by the pair-specific physical-time
theorems in the residual union.

No orientation, reaction history, population box, or rate parameter is
enumerated below.  The proof uses one exact marked one-jump identity, a
finite directed path supplied by strong connectivity, and an all-clock
Bellman recursion.

## 1. Marked chain and exact one-jump identity

Fix a reduced binary network, a closed irreducible population class, one
orientation of each linkage, and positive labelled rate constants.  For a
complex \(y\), let

\[
 K_y=\sum_{e:\,s(e)=y}\kappa_e,
 \qquad
 \lambda_y(x)=K_y(x)_y,
 \qquad
 \Lambda(x)=\sum_z\lambda_z(x),
 \qquad
 p_y(x)={\lambda_y(x)\over\Lambda(x)}.                 \tag{1.1}
\]

Terms with \(p_y=0\) are read as zero.  Parallel labels are retained inside
\(K_y\); conditional on source \(y\), their target is selected with
probability \(\kappa_e/K_y\).

After a labelled physical reaction with target \(t\), mark the state by
\(t\).  Necessarily \(x\ge t\).  On the marked state space put

\[
              F(x,t)=\sum_i\log((x_i-t_i)!).              \tag{1.2}
\]

If the next labelled reaction is \(e:y\to u\), then its actual endpoint is
\((x-y+u,u)\), and the factorial cancellation is exact:

\[
 F(x-y+u,u)-F(x,t)=\log{(x)_t\over(x)_y}.                 \tag{1.3}
\]

Consequently the expected increment of one ordinary embedded all-clock
jump from \((x,t)\) is

\[
\begin{aligned}
 D(x,t)
 &=\sum_y p_y(x)\log{(x)_t\over(x)_y}\\
 &=\log p_t(x)-\sum_y p_y(x)\log p_y(x)
   -\log K_t+\sum_y p_y(x)\log K_y .
\end{aligned}                                             \tag{1.4}
\]

Here \(t\) is enabled because it is physically present.  Since the source
set and rates are fixed and there are at most ten binary complexes,

\[
                         D(x,t)\le \log p_t(x)+C_K         \tag{1.5}
\]

with a finite constant depending only on the labelled rate vector.  The
same formula also shows that the positive part of the one-jump increment
has every fixed moment after source-rate weighting:

\[
 \sum_y p_y(x)\left[\log{(x)_t\over(x)_y}\right]_+^q
 \le C_q\sum_y p_y(x)
          \left\{1+\log{1\over p_y(x)}\right\}^{q}
 \le C_q'.                                             \tag{1.6}
\]

Indeed, write the logarithm using (1.4) source by source and use
\(r(1+\log(1/r))^q\le C_q\).  Finitely many labelled targets do not alter
this estimate.

## 2. Available target paths and the episode rule

Fix a terminal two-active chart, including its exact enabled-source set,
bounded-coordinate phase, and compact tied source-ratio cell.  For each
linkage \(L\), the available alternative supplies a terminal complex
\(c_L\) whose source probability tends to zero on every escaping sequence
in that chart, and, from every actual target \(t\in L\), a simple directed
path

\[
          t=y_0\longrightarrow y_1\longrightarrow\cdots
                    \longrightarrow y_m=c_L,              \tag{2.1}
\]

possibly ending earlier at a declared lower-shell, support, bounded-box, or
active-set exit.  Every prescribed source is physical: the preceding
reaction creates it as its actual target.  Simple paths have length at most
\(|L|-1\le9\).  The finite chart fixes one path for each possible marked
target, with any deterministic graph ordering.

Starting at \((x,t)\), run (2.1) with **all physical clocks retained**.
At stage \(i<m\), take the next ordinary physical jump.

* If it is the designated labelled edge \(y_i\to y_{i+1}\), continue.
* If any other labelled reaction fires, stop immediately at that reaction's
  actual population endpoint and actual target mark.
* If the path reaches \(c_L\), take one final ordinary all-clock jump and
  stop at its actual endpoint and mark.
* Any declared structural exit is recorded at the physical reaction which
  causes it and stops the episode.

Thus an episode contains between one and ten ordinary jumps.  It never
waits for a selected linkage to activate and never conditions on a future
reaction.

## 3. All-clock Bellman estimate

Consider an escaping sequence of episode starts \((x_n,t_n)\) which remains
in one fixed chart and one fixed path (2.1).  Let \(x_{i,n}\) be the
deterministic population obtained after the first \(i\) prescribed edges,
and abbreviate

\[
 D_{i,n}=D(x_{i,n},y_i),\qquad
 a_{i,n}={\kappa_{y_i\to y_{i+1}}(x_{i,n})_{y_i}
                    \over\Lambda(x_{i,n})}.               \tag{3.1}
\]

Let \(J_{i,n}\) be the expected total \(F\)-increment from stage \(i\),
including the ordinary jump at that stage and stopping on its deviation.
At \(c_L\), the final ordinary jump gives \(J_{m,n}=D_{m,n}\); before it,
the Markov property and the literal stopping rule give

\[
                      J_{i,n}=D_{i,n}+a_{i,n}J_{i+1,n}.
                                                               \tag{3.2}
\]

This identity already includes every competing clock.  In particular, the
deviation which may switch linkages is part of \(D_{i,n}\), not an omitted
activation toll.

The available-target hypothesis says precisely that a designated success
path which does not first cause a declared structural exit satisfies

\[
                       p_{c_L}(x_{m,n})\longrightarrow0.    \tag{3.3}
\]

Let \(j\) be the first path index for which
\(p_{y_j}(x_{j,n})\to0\), after passing to a subsequence.  For \(i<j\),
compactness of the fixed source-ratio chart and finiteness of the path give

\[
                         a_{i,n}\ge b_i>0.                 \tag{3.4}
\]

Equation (1.5) gives \(D_{j,n}\to-\infty\), while every
\(D_{i,n}\le C_0:=\max\{C_K,0\}\).  If \(j=m\), there is no tail after
the rare source.  If \(j<m\), then
\(a_{j,n}\le C p_{y_j}(x_{j,n})\), because the designated label is
one of the labels with source \(y_j\).  Iterating (3.2), the positive tail
after \(j\) is bounded by

\[
 a_{j,n}\sum_{r=0}^{m-j-1}C_0
       \le C\,p_{y_j}(x_{j,n})\longrightarrow0.            \tag{3.5}
\]

The nonvanishing product of the preceding \(a_{i,n}\)'s multiplies
\(D_{j,n}\to-\infty\).  Hence

\[
                            J_{0,n}\longrightarrow-\infty. \tag{3.6}
\]

If the selected designated path causes a structural exit at stage \(k\)
before reaching \(c_L\), apply the same first-vanishing-source argument to
the prefix.  Either some \(p_{y_j}(x_{j,n})\to0\), in which case (3.2)--(3.6)
again give coercive negative reward, or every designated-label probability
on the finite prefix is bounded below.  In the latter case the probability
of following the prefix to its exit-causing reaction is bounded below by a
positive constant.  Thus a normalized recurrent trace of episode starts has
positive structural-exit flux.  This proves the exact dichotomy

\[
 \text{coercive negative all-clock reward}
 \quad\hbox{or}\quad
 \text{positive physical structural-exit flux}.            \tag{3.7}
\]

The argument is uniform on a fixed compact chart cell.  Equivalently, if
uniform coercivity failed, a violating sequence would admit a subsequence
with fixed path and limiting source ratios, and the preceding proof would
contradict it.  Since there are finitely many target marks, linkages, and
simple paths, there is a finite menu of statewise episode rules.  On the
nonexit part of a terminal chart, outside a finite set, the selected rule
satisfies

\[
                 \mathbb E_{x,t}\Delta F\le-2.             \tag{3.8}
\]

This conclusion is insensitive to whether the rare probability is
\(1/\log R\), \(1/R\), or an iterated-log scale: (3.6) uses only that it
tends to zero and never divides by it.

## 4. Positive moments, physical duration, and a proper potential

Each episode contains at most ten physical jumps.  Estimate (1.6), applied
successively at the prescribed states, gives for every fixed \(q<\infty\)

\[
        \sup \mathbb E[((\Delta F)^+)^q]<\infty.            \tag{4.1}
\]

At every stage the marked source is enabled, so its propensity is a positive
integer falling factorial times a fixed positive rate.  Thus the total
hazard is at least the minimum labelled rate \(\kappa_*>0\).  A sum of at
most ten exponential holding times with conditional means at most
\(\kappa_*^{-1}\) has moments of every fixed order, and

\[
                        \sup\mathbb E\tau^q<\infty.         \tag{4.2}
\]

The endpoint is the actual physical endpoint of the last included jump and
has bounded population displacement from the start.

The marked factorial potential itself is nonnegative and proper.  Indeed,
\(F\ge0\), and \(t\) ranges over the finite binary complex set, so if
\(|x|_1\to\infty\), then at least one \(x_i-t_i\to\infty\).  Put simply

\[
                         W(x,t)=1+F(x,t).                   \tag{4.3}
\]

No mark-dependent linear or logarithmic correction is inserted.  This point
is essential when the negative scale is only an iterated logarithm.

Let \(C_\tau=\sup\mathbb E\tau<\infty\), supplied by (4.2), and choose any
fixed \(0<\eta\le C_\tau^{-1}\).  Equations (3.8) and (4.2) then give

\[
 \mathbb E[W(X_\tau,T_\tau)-W(x,t)+\eta\tau]
                         \le-1                             \tag{4.4}
\]

outside a finite set, for some fixed \(\eta>0\).  Sequential coercivity over
the finite rule menu supplies the same \(\eta\) and right-hand margin for the
whole chart.  The endpoint and duration in (4.4) are integrable: (4.1)
controls the positive endpoint increment, while the endpoint potential is
nonnegative.

## 5. Both-available composition and nonoverlap

Assume both linkages satisfy the available-target hypothesis.  Then the
actual target of every physical reaction belongs to an available linkage
and starts one of the episodes in Section 2.  Concatenate episodes at their
actual stopping endpoints.  Since every episode contains between one and
ten jumps, episode-start count and physical reaction count differ by at most
a fixed factor.  Thus a nonzero reaction-count Green trace cannot disappear
under the episode partition.  If a designated success path leaves the chart
before reaching its rare terminal, the exit-causing jump is retained and
the conclusion is structural-exit flux instead of (4.4).  On a terminal
chart that flux is zero; hence the negative alternative applies to its
recurrent source trace.

Pathwise, every jump is counted exactly once.  If a competitor fires during
an episode, that jump is the terminal jump of the current episode; its
increment is already present in \(D_{i,n}\).  Only **after** that endpoint is
reached does its actual target mark choose the next episode.  The same jump
is not counted again.  This is precisely why the conditional-activation
counterexample does not apply: the proof never conditions on that competitor
and then tries to charge it to the episode it creates.

Equation (4.4) is in the exact form required by the physical-time
state-selected Foster lemma: one proper \(W\), a uniform positive duration
coefficient and drift margin, full physical clocks, and integrability at the
actual endpoint.  In a surrounding finite chart cover, reclassify that
endpoint under the same \(W\); no comparison toll occurs.  A hit of the
finite target is recorded immediately if it occurs inside an episode while
that one episode may finish for drift accounting.

If these both-available rules cover all unbounded states of the reachable
marked class, or if every complementary chart supplies the corresponding
common-\(W\) Foster rule, the lemma gives finite mean hitting of a finite
marked target.  Propagating the mark through one finite return cycle and
projecting its finite occupation measure to populations then gives an
invariant probability for the physical irreducible class.  Together with
binary-network nonexplosion, this implies physical positive recurrence.  For
the local atlas application, only the preceding negative-or-exit alternative
is needed: either outcome contradicts a terminal escaping chart.

An arbitrary unmarked initial state causes no seam.  In a nonabsorbing active
class, take its first ordinary physical jump and use that jump's actual target
as the initial mark; from a fixed state this has finite mean duration and
integrable endpoint.  An absorbing state is already recurrent.

### Theorem 5.1

Let a reduced weakly reversible binary network have at most three dynamic
species and exactly two active linkage classes.  In any terminal two-active
chart in which both linkages satisfy the available-target hypothesis of
Section 2, every fixed strongly connected orientation and every positive
labelled rate vector admit one proper marked potential and a finite menu of
all-clock state-selected stopping rules satisfying the following exact
alternative: either (4.4) holds, or the episode records a physical
structural-exit jump.  Thus a terminal both-available chart cannot carry an
escaping fixed-class occupation.  When the surrounding finite chart cover
reclassifies every exit under the same marked potential, the physical-time
state-selected Foster lemma gives positive recurrence of the class.

The theorem covers arbitrary relative rarity of the two linkages, including
\(1/\log R\), \(1/R\), and iterated-log source scales.  It does **not** cover
an available linkage paired with a linkage that is not available in the same
chart.  That case requires the pair-specific residual theorems and is outside
this note.
