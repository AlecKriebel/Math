# Hostile exact-byte audit of the both-available entropy--Bellman repair

**Audit date:** 2026-08-12 PDT.  
**Stochastic target:**
`research_notes/proof_first_both_available_current_target_theorem.md`  
**Target SHA-256:**
`157e94cd035dec9a41947129dfcbbab0ebc6e72c01abde6bcf6626052954f1ed`  
**Target size:** 320 lines, 13,664 bytes.  
**Classifier bridge:**
`research_notes/proof_first_quc_classifier_bridge_and_raw_trichotomy.md`  
**Bridge SHA-256:**
`014a317602b60c765dc9a9eb98f0921ba3fd8f779221e271e0dd7f53e245f54c`  
**Bridge size:** 250 lines, 9,259 bytes.

The two targets were atomically frozen before this replay.  This audit does
not edit either target.

## 1. Verdict and exact boundary

**STRICT PASS** for the stochastic theorem and the Q/U/C classifier bridge
at the exact bytes above.

The pass is deliberately scoped.  It proves the negative-reward-or-physical-
exit theorem for a terminal two-active chart in which **both** linkages have
the available-target property.  The bridge proves that every raw Q-, U-, or
C-classified linkage has that property, from every actual carried target.
Consequently the raw available/available stratum is covered.

This does not prove a generic available/shielded theorem, does not delete a
shielded linkage, and does not extend any recurrence result by support
inclusion.  Mixed and shielded/shielded charts remain in their separately
audited pipelines.  Nor does this scoped pass, by itself, certify the full
two-linkage or global T3-2 composition.

No orientation, reaction history, population box, rate vector, or stochastic
path space was enumerated.  The finite raw counts are used only as regression
identities for the classifier partition; all stochastic claims below are
proved symbolically.

## 2. Exact marked factorial identity: pass

Let the current population be $x$ and let $t$ be the actual target of the
preceding labelled reaction.  Then $x\ge t$.  If the next labelled reaction
is $y\to u$, its population endpoint is $x-y+u$ and its new mark is $u$.
For

\[
                 F(x,t)=\sum_i\log((x_i-t_i)!),
\]

factorial cancellation gives exactly

\[
 F(x-y+u,u)-F(x,t)
 =\sum_i\log{(x_i-y_i)!\over(x_i-t_i)!}
 =\log{(x)_t\over(x)_y}.                         \tag{2.1}
\]

The target $u$ disappears from the increment because it is also the new
mark.  Thus parallel labels with common source $y$ have the same marked
reward; aggregating them into

\[
 K_y=\sum_{e:s(e)=y}\kappa_e,
 \qquad p_y={K_y(x)_y\over\Lambda(x)}
\]

loses no label-dependent term.  Since the current mark $t$ is physically
present and every vertex of a strongly connected linkage has an outgoing
label, $p_t>0$.  Pointwise on every enabled source $y$,

\[
 \log{(x)_t\over(x)_y}
 =\log p_t-\log p_y-\log K_t+\log K_y.             \tag{2.2}
\]

Averaging (2.2) gives the displayed identity

\[
 D(x,t)=\log p_t-\sum_y p_y\log p_y
        -\log K_t+\sum_y p_y\log K_y.              \tag{2.3}
\]

There are at most ten binary sources.  Their Shannon entropy is at most
$\log 10$, and the fixed positive rate vector has finite log range.
Therefore

\[
                         D(x,t)\le\log p_t+C_K.       \tag{2.4}
\]

This estimate is uniform in population and requires no lower bound on
$p_t$.

## 3. One-jump positive moments: pass

Equation (2.2), together with $\log p_t\le0$, implies

\[
 \left[\log{(x)_t\over(x)_y}\right]_+
 \le C+\log(1/p_y).                                 \tag{3.1}
\]

For every fixed $q<\infty$,

\[
 \sup_{0<r\le1}r\{1+\log(1/r)\}^{q}<\infty.         \tag{3.2}
\]

Summing (3.1) with weights $p_y$ proves target (1.6).  It is important
that this is a source-weighted assertion: no uniform pointwise bound on a
rare source's logarithmic increment is claimed.  Finitely many target labels
do not change the bound because (2.1) depends on the source and current mark,
not on the next target.

## 4. The Q/U/C classifier really supplies a rare terminal

Let $h=(h_A,h_B,0)$, with $h_A,h_B>0$, scalarize the complete source-order
cell, and let $T_h(L)$ be the proper top block of one available linkage.
The ordered classifier has exactly three available outcomes.

* **Q.**  Choose a top complex $q$ with two active particles.  Binaryity
  gives $q_C=0$.  Any lower $c$ in $L$ but not in $T_h(L)$ satisfies
  $q_C\le c_C$ and $h\cdot q>h\cdot c$.
* **U.**  A top unary complex cannot be $C$: its weight would be zero, so
  nonnegativity of $h$ would make the whole linkage top, contrary to the
  failed flat test.  Hence $q\in\{A,B\}$, again $q_C=0\le c_C$ for any
  lower $c$.
* **C.**  Choose a top $C$-containing complex $q$ and a lower
  $C$-containing complex $c$.  Because the Q test has already failed and
  the top is nonflat, binaryity forces
  $q\in\{A+C,B+C\}$.  Thus $q_C=1\le c_C\in\{1,2\}$, while
  $h\cdot q>h\cdot c$.

All three cases give

\[
                         q_C\le c_C,
 \qquad h\cdot q>h\cdot c.                         \tag{4.1}
\]

Now start from any actual mark $t\in L$.  Strong connectivity gives a
simple directed path

\[
                         t=y_0\to y_1\to\cdots\to y_m=c. \tag{4.2}
\]

This is a physical word: $t$ is enabled at the start, and every prescribed
firing creates the next prescribed source as its actual target.  On success,
the populations telescope to

\[
                         z=x-t+c\ge c.               \tag{4.3}
\]

If a bounded phase, enabled support, active set, shell, or source-order cell
changes on the prefix, the causing physical reaction is retained as a
structural exit.  Otherwise bounded displacement preserves the strict source
comparison.  At $z$, the faster $q$ is enabled: Q and U require no $C$,
while C follows from $z_C\ge c_C\ge q_C$.  Therefore

\[
 p_c(z)\le {\lambda_c(z)\over\lambda_q(z)}
 ={K_c(z)_c\over K_q(z)_q}\longrightarrow0.          \tag{4.4}
\]

This proves the theorem's available-target hypothesis for every actual mark,
every strong orientation, and every fixed positive rate vector.

The earlier C-type obstruction does not contradict (4.4).  It refuted a
pre-mark rule which tried to start from a disabled top source.  The repaired
rule starts from the actual enabled target $t$, travels physically to the
lower $c$, and uses the success endpoint itself to enable $q$.  There is
no activation wait and no conditioning on a future firing.

## 5. Designated-path Bellman recursion: pass

Condition on success through the first $i$ designated labels.  The
population $x_i$ and mark $y_i$ are then deterministic functions of the
episode start.  Let $D_i=D(x_i,y_i)$, and let $a_i$ be the probability
that the next ordinary all-clock jump is the exact designated label.  The
episode stops at the actual endpoint of any deviation.  Hence the first-step
recursion is exactly

\[
 J_m=D_m,
 \qquad J_i=D_i+a_iJ_{i+1}.                         \tag{5.1}
\]

Expanding it gives

\[
 J_0=\sum_{r=0}^m\left(\prod_{i<r}a_i\right)D_r.     \tag{5.2}
\]

Every competing clock is already averaged into $D_i$.  If a competitor
fires, its marked reward is the terminal reward of the current episode; only
its actual endpoint starts the next episode.  Thus (5.1) neither omits nor
double counts a linkage-switch or activation reaction.

Along an escaping sequence, pass to a subsequence on which the finitely many
success-prefix source probabilities converge.  The terminal rarity (4.4)
ensures a first index $j$ with

\[
                         p_{y_j}(x_j)\longrightarrow0. \tag{5.3}
\]

For every $i<j$, the source probability has a positive limit.  Since the
designated label has the fixed conditional fraction
$\kappa_i/K_{y_i}>0$,

\[
                         a_i\ge b_i>0.                \tag{5.4}
\]

At the first rare source, (2.4) gives $D_j\to-\infty$.  If $j=m$, there
is no later tail.  If $j<m$, then

\[
                         a_j={\kappa_j\over K_{y_j}}p_{y_j}
                              \longrightarrow0.        \tag{5.5}
\]

Every $D_r\le C_0:=\max\{C_K,0\}$, so all positive terms after $j$ in
(5.2) contain the factor $a_j$ and are $O(a_j)$.  The finite terms before
$j$ are uniformly bounded above, whereas the coefficient of $D_j$ is
bounded below by $\prod_{i<j}b_i>0$.  Therefore

\[
                         J_0\longrightarrow-\infty.   \tag{5.6}
\]

This covers $j=0$, $j=m$, and the zero-length path $m=0$.  It also
explains why a source probability of $1/\log R$, $1/R$, or an iterated-
log scale causes no loss: the negative term is an unweighted
$\log p_{y_j}$, while only the later positive tail is multiplied by
$p_{y_j}$.

## 6. Uniformity and path exits: pass

Uniformity is sequential, not a claimed minimum over an open probability
simplex.  If a uniform negative margin failed in a fixed chart, an escaping
violating sequence would have a subsequence with fixed mark, linkage, path,
bounded phase, and limiting finite source probabilities.  The first-zero
argument (5.3)--(5.6) contradicts it.  Finiteness of the possible marks and
chosen simple paths then gives a finite rule menu and one finite exceptional
set.

If the deterministic success prefix instead causes a declared structural
exit, there are two possibilities.  An earlier source probability vanishes,
and the same Bellman proof gives coercive negative reward; or every label
probability on the finite prefix is bounded below.  In the latter case the
physical probability of the exit-causing prefix is bounded below.  Because
episode length lies between one and ten reactions, positive episode-start
mass gives positive reaction-count exit flux.  The terminal-chart
localization fixes zero normalized outgoing structural flux, so the second
alternative contradicts terminality.

No deviation feasibility assumption is hidden here.  Only the designated
success states need be deterministic; every deviation stops immediately at
its actual feasible endpoint and is already present in the all-clock
expectation $D_i$.

## 7. Physical time, endpoints, and the proper potential: pass

Every episode has at most ten ordinary jumps.  At each stage the current mark
is an enabled source, so its falling factorial is a positive integer and the
total hazard is at least the minimum positive labelled rate
$\kappa_*>0$.  Each holding time is therefore conditionally dominated by
an exponential of rate $\kappa_*$.  A sum of at most ten such holding times
has uniformly bounded moments of every fixed order.  No upper bound on the
quadratic total rate and no lower bound on a rare designated-label
probability is needed.

The positive part of an episode's total $F$-increment is at most the sum of
the positive one-jump increments.  Section 3, applied at the finitely many
success states, gives all fixed positive endpoint-increment moments.  Its
last population differs from its start by at most ten bounded reaction
vectors and is the actual physical endpoint of its last included jump.

The potential

\[
                         W(x,t)=1+F(x,t)               \tag{7.1}
\]

is nonnegative and proper on the marked state space: marks range over the
finite binary complex set, so $|x|_1\to\infty$ forces some residual
$x_i-t_i\to\infty$, and hence $F(x,t)\to\infty$.  No mark-dependent
correction is needed.  From

\[
 \mathbb E\Delta W\le-2,
 \qquad \sup\mathbb E\tau=C_\tau<\infty,
\]

any $0<\eta\le C_\tau^{-1}$ gives

\[
 \mathbb E[W(X_\tau,T_\tau)-W(x,t)+\eta\tau]\le-1.  \tag{7.2}
\]

The positive endpoint increment and duration are integrable; the negative
increment is bounded below by $1-W(x,t)$ at a fixed start.

## 8. Nonoverlap, Foster handoff, and marked projection: pass

An episode's deviation or final ordinary jump belongs to that episode.  The
jump's actual target selects the next rule only after its endpoint.  Hence
every physical reaction is assigned exactly once.  Since episode length is
between one and ten jumps, a nonzero reaction-count Green trace cannot vanish
under the episode partition.

When both linkages satisfy the bridge, every actual target belongs to one of
them and initializes a valid rule.  All rules use the single proper potential
(7.1), so endpoint reclassification has zero comparison toll.  Estimate
(7.2) has the uniform duration coefficient, drift margin, actual endpoint,
and integrability required by the physical-time state-selected Foster lemma.
If the finite target is visited inside an episode, the hit is recorded then;
finishing that one episode only upper-bounds the hitting time used in drift
accounting.

The arbitrary unmarked start is harmless: in a nonabsorbing class, the first
ordinary reaction supplies its actual target mark, with finite mean holding
time and integrable bounded-jump endpoint.  A finite marked return cycle can
be projected to populations because the population transition rates do not
depend on the mark.  The projected finite occupation measure is invariant for
the physical class.  Binary-network nonexplosion remains an independent
input; it is not inferred from the embedded drift.

## 9. Final disposition

The following hostile checks all pass at the frozen hashes:

1. exact factorial identity and source aggregation;
2. positive one-jump moments;
3. Q/U/C-to-available-target symbolic bridge, including C-type faces;
4. physical path feasibility from every actual mark;
5. unconditioned all-clock Bellman recursion;
6. rare-source and arbitrary-relative-rate uniformity;
7. deviation, structural-exit, and reaction-count accounting;
8. physical duration and actual endpoint integrability;
9. common proper potential and state-selected Foster handoff; and
10. nonoverlap and marked-to-physical projection.

**Final result: STRICT PASS for the scoped both-available theorem and its
exact Q/U/C bridge at the frozen SHA-256 hashes listed above.**
