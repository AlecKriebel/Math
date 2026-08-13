# Proof-first fixed-class composition of the hard family

## 1. Scope

This note records the analytic composition theorem needed after the local
hard stopped kernels have been proved.  It deliberately treats the local
theorems as black boxes.  It does not enumerate supports, orientations,
descriptors, or reaction words, and it does not infer an analytic statement
from a finite search.

The conclusion below is conditional on two inputs.

1. An exhaustive descriptor proposition assigns every realizable
   nonpassing asymptotic descriptor of a hard support pair to one of the
   stated local physical kernels.
2. Each assigned kernel satisfies the publication contract in Section 4
   for the *same pair-fixed population potential*.

The repaired generalized kernel, the ordinary one-active interface, and the
two exceptional all-active switch kernels are intended to discharge the
second input.  Until each of them has an independent proof-level audit, the
result below is a composition theorem rather than a certification of those
inputs.

The point of the note is that no further probabilistic or Foster argument is
needed once these two inputs are available.  In particular, no exhaustion of
long reaction histories is part of the global proof.

## 2. Fixed network, fixed class, and one population potential

Fix a bimolecular stochastic mass-action network with three dynamically
active species, two strongly connected active linkage classes, fixed
positive rate constants, and a closed irreducible population class
\(\Gamma\).  Constants may depend on this fixed network, its rates, and
\(\Gamma\), but never on the current population.

Choose one vector \(\ell\in\mathbb R^3\) for the entire support pair and put

\[
 F_\ell(x)=K_\ell+\sum_{i=1}^3\log(x_i!)+\ell\mathbin\cdot x,
 \qquad W_\ell(x)=F_\ell(x)^4,                       \tag{2.1}
\]

where \(K_\ell\) is fixed once and is large enough that \(F_\ell\ge1\).
This is a proper function on \(\mathbb N_0^3\).  Indeed, if
\(N=|x|_1\), some coordinate is at least \(N/3\), so its factorial term
grows like \((N/3)\log N\), whereas the negative part of
\(\ell\cdot x\) is only linear in \(N\).

The admissible choice of \(\ell\) is pair-specific, not chart-specific.

* On an ordinary common-factorial pair, use the correction required by its
  all-active top linkage; this may be zero, a reversible detailed-balance
  correction, or the fixed directed-triple correction.
* On an \(H_b\)-switch pair, use the one detailed-balance correction of the
  reversible top linkage.  It must be the same vector in the shell episode
  and in every lower-dimensional episode.
* On an \(H_w\)-switch pair, use \(\ell=0\).

The auxiliary workloads \(H_b\) and \(H_w\) may be used to construct or
analyze a stopping rule.  They are not substituted for \(W_\ell\) at a
gluing endpoint.  Likewise, a shell-dependent normalization constant in a
stationary law is not allowed to become a shell-dependent additive term in
\(F_\ell\).

Different support pairs may use different potentials.  A common potential
is required only across all charts and all endpoints of one fixed physical
network.

## 3. The reachable reflected-debt lift

Fix a reference population \(x^\circ\in\Gamma\).  Starting from
\((x^\circ,0)\), update one mark for each species after every physical jump
\(x\mapsto x+\zeta\) by

\[
 D_i^+=(D_i+\zeta_i)^+,
 \qquad H_i=X_i-D_i.                                  \tag{3.1}
\]

Let \(\widehat\Gamma\) be the marked states reachable from
\((x^\circ,0)\).  Pathwise,

\[
 0\le D_i\le X_i,
 \qquad H_i(t)\le H_i(0)=x_i^\circ.                  \tag{3.2}
\]

To check (3.2), if \(D_i+\zeta_i\ge0\), then \(H_i\) is unchanged; if
\(D_i+\zeta_i<0\), reflection sets \(D_i^+=0\) and strictly lowers
\(H_i\).  Consequently the all-zero-debt set

\[
 \widehat K_0=\{(x,0)\in\widehat\Gamma\}
 \subseteq\{(x,0):0\le x_i\le x_i^\circ\}            \tag{3.3}
\]

is finite.

The lift creates no explosion and no new randomness: the mark is a
deterministic update attached to each physical reaction.  Moreover
\(\widehat W(x,d)=W_\ell(x)\) is proper on
\(\widehat\Gamma\), since a fixed population \(x\) has only finitely many
marks satisfying \(0\le d_i\le x_i\).

The debt is used only to decide whether an old-active service theorem is
eligible.  Every local kernel must evolve the actual marks along its
physical path.  In particular, an exact return of the physical population
need not be an exact return of the debt mark.  This causes no gluing toll
because \(W_\ell\) depends only on the physical population.

The correct zero-debt statement is sequencewise.  If a chart selects a
coordinate \(V\) whose population diverges, then \(D_V=0\) would imply
\(V=H_V\le x_V^\circ\), a contradiction.  If another coordinate diverges
instead, the state must be reclassified into its actual descriptor; it is
not legitimate to call the whole zero-\(D_V\) face finite.  This
reclassification is part of the access hypothesis in Section 6.

## 4. Publication contract for a local stopped kernel

Let \(B_\alpha\subseteq\widehat\Gamma\) be the marked start domain of a
local chart.  A local result is usable in the global proof only if it gives,
outside a finite subset of that domain, a stopping time
\(\tau_\alpha>0\) satisfying all of the following requirements.

### 4.1 Physical law

The stopping rule is adapted to the original physical filtration and
retains every enabled reaction and its actual mass-action clock.  It includes
the reaction which causes a service, return, shell exit, or moving-boundary
exit.  Its endpoint is the actual population \(X_{\tau_\alpha}\), and the
debt marks have been updated along the entire physical path.

Analytic erasure of an exact physical self return is permitted only as a
renewal identity.  The reconstructed stopping time must retain the elapsed
holding times and every boundary hit.  Erasure must not reset, identify, or
weight a debt mark.

If the physical population returns exactly while its debt mark changes, a
physical renewal remains valid only when the remainder of that local
stopping rule is mark-blind after the initial eligibility check.  Otherwise
the return is not regenerative on the marked state space and must be kept as
a genuine marked transition.

### 4.2 Strong-Markov interface

The rule is defined from every state in its stated domain, not only from a
formal asymptotic point.  It is strong-Markov compatible, and

\[
 \mathbb E_z\{W_\ell(X_{\tau_\alpha})+\tau_\alpha\}<\infty.          \tag{4.1}
\]

The constants and integrability estimates are uniform along every
divergent sequence in one fixed chart, after the network, rates, class, and
chart have been fixed.

### 4.3 Complete common-potential drift

There are chart constants \(\eta_\alpha>0\) and
\(\delta_\alpha>0\) such that

\[
 \mathbb E_z\!\left[
 W_\ell(X_{\tau_\alpha})-W_\ell(x)
       +\eta_\alpha\tau_\alpha
 \right]\le-\delta_\alpha.                         \tag{4.2}
\]

Every terminal branch is included in (4.2), including upward returns,
rare moving-boundary exits, shell exits, and random overshoots.  A bare
probability estimate for such an exit is insufficient; its endpoint must be
weighted by the actual \(W_\ell\)-cost.

A theorem that proves only a workload decrement, only an unpowered
factorial decrement, or only a negative conditional mean after deleting
competing clocks does not satisfy (4.2).

### 4.4 Endpoint rule

After \(\tau_\alpha\), the global selector starts again from the same actual
marked state.  It may choose a generator-good rule or another local chart.
There is no demand that the endpoint return to the incoming axis, shell,
base mark, or descriptor.

Thus a handoff is a reclassification, not an extra comparison inequality.
The cost of reaching the handoff is already present in (4.2), and the next
episode starts with exactly the same value of \(W_\ell\).  This convention
prevents a circular definition in which an all-active theorem assumes a
lower-dimensional recurrence theorem which in turn assumes the all-active
theorem.

If a local proof internally appends another kernel before asserting (4.2),
it must independently prove that this finite or regenerative concatenation
terminates and has (4.1).  It may not appeal to the global recurrence theorem
being proved here.

## 5. A fixed-class random-time Foster theorem

The following is the only global probabilistic theorem needed.

> **Theorem 5.1 (common-potential physical-time Foster theorem).**
> Let \(Z\) be a nonexplosive CTMC on a countable state space \(E\), and
> let \(W:E\to[0,\infty)\) be proper.  Suppose that for a finite set
> \(K\),
> \[
> E\setminus K=G\mathbin{\dot\cup}B.                 \tag{5.1}
> \]
> Assume that, for some \(a>0\),
> \[
> {\cal L}W\le-a\quad\hbox{on }G,                    \tag{5.2}
> \]
> and that every \(z\in B\) has a strong-Markov stopping time
> \(\tau_z>0\) with
> \[
> \mathbb E_z[W(Z_{\tau_z})+\tau_z]<\infty,
> \qquad
> \mathbb E_z[W(Z_{\tau_z})-W(z)+\eta\tau_z]
> \le-\delta                                        \tag{5.3}
> \]
> for fixed \(0<\eta\le a\) and \(\delta>0\).  Interpret (5.2) through
> the extended generator, localized on finite \(W\)-sublevels.  Then
> \[
> \mathbb E_z\tau_K<\infty\qquad(z\in E).             \tag{5.4}
> \]

### Proof

From a point of \(G\), run until the first entrance into \(B\cup K\).
Localized Dynkin applied to (5.2) gives

\[
 \mathbb E[W(Z_\sigma)-W(z)+\eta\sigma]\le0.         \tag{5.5}
\]

It also gives \(\mathbb E\sigma\le W(z)/a\), so this entrance time is
finite almost surely unless \(K\) has already been reached.  At an entrance
to \(B\), append the state-selected physical episode from (5.3), and then
repeat.  If \(K\) is visited during an episode, record that target hit; the
episode may be completed for drift accounting because its full duration
only upper-bounds the target time.

For clarity, removal of the finite-sublevel localization on this good
segment needs no separate moment assumption: \(W\ge0\), the stopped drift
has one sign, and Fatou's lemma gives (5.5).  Endpoint integrability for the
exceptional segment is the separate hypothesis in (5.3).

At every completed exceptional macroepisode, the conditional expectation
of the increment of \(W+\eta t\) is at most \(-\delta\).  Stopping after
at most \(m\) such episodes and using \(W\ge0\) gives

\[
 \delta\,\mathbb E(N\wedge m)
 +\eta\,\mathbb E S_{N\wedge m}
 \le W(z)+\delta,                                    \tag{5.6}
\]

where \(N\) is the terminal episode index and \(S_j\) the accumulated
physical time.  Monotone convergence yields a finite expected episode count
and finite expected time to \(K\).  A start in \(G\) which reaches \(K\)
without an exceptional episode is covered directly by (5.5).  This proves
(5.4). \(\square\)

No embedded reaction-count drift occurs in this proof.  Exact self loops
may contain arbitrarily many physical jumps; only their physical duration
and their net common-potential increment enter (5.3).

## 6. From descriptor theorems to the statewise hypotheses

For a fixed hard support pair, assume the following finite descriptor
coverage statement.

> **Coverage hypothesis.** Every sequence
> \(z_n=(x_n,d_n)\in\widehat\Gamma\) with
> \(W_\ell(x_n)\to\infty\) has a subsequence of one of the following
> forms:
>
> 1. it is a realizable passing descriptor and
>    \({\cal L}W_\ell(x_n)\to-\infty\);
> 2. it lies in the genuine start domain of a local kernel satisfying
>    Section 4; or
> 3. its nominal local service coordinate has zero debt, in which case
>    (3.2) forces a different actual descriptor, and that reclassified
>    subsequence satisfies item 1 or 2.

“Genuine start domain” is load-bearing.  If a local theorem begins at a
no-fast base, a bounded-energy shell core, or an activated wedge, then the
coverage theorem must show that the current population is already in that
domain or supply a separate all-reaction entrance kernel satisfying the same
contract.  Merely proving that such a base is reachable does not suffice.

The coverage hypothesis implies the statewise assumptions of Theorem 5.1.
Choose

\[
 \eta=\min\{a,\eta_\alpha:\alpha\text{ is a local chart}\},
 \qquad
 \delta=\min_\alpha\delta_\alpha.                   \tag{6.1}
\]

These minima are positive because the chart library for a fixed pair is
finite.  Reducing \(\eta_\alpha\) to \(\eta\) preserves (4.2).

Let \(G\) be the states with \({\cal L}W_\ell\le-a\), and let \(B\) be
the states admitting a contracted episode with (5.3).  If infinitely many
states lay outside \(G\cup B\), properness would allow a sequence among
them with \(W_\ell\to\infty\).  The coverage hypothesis would give a
subsequence in \(G\) or \(B\), a contradiction.  Hence the uncovered set
is finite and may be added to \(K\).  The same bad-sequence argument turns
the sequencewise endpoint estimates into the statewise integrability in
(5.3).

This is a compactness-by-contradiction argument on a countable proper state
space.  It does not assert that a tight coordinate has finite support, and
it does not require a uniform finite inactive phase box.

## 7. Instantiation by the hard local theorem library

The local library must be invoked at the level of its proved analytic
hypotheses, not by the name of a pair selector.

### 7.1 Ordinary common-factorial branch

For a pair with a corrected-factorial common potential, the repaired hard
kernel must cover every historically consistent positive-debt generalized
start and every dormant stopped phase assigned to it.  Its exact-return
renewal, physical boundary, endpoint moments, duration moments, and
fourth-power estimate must together give (4.1)--(4.2) for the chosen
\(\ell\).

The exact higher-dimensional handoff is path-labelled, not endpoint-labelled.
Only an outer-base path which begins and ends with \(I=R=0\), without first
crossing a cutoff while an excursion is open, belongs to the promotion
kernel \(P\).  If a \(U\)-, \(I\)-, or \(R\)-cutoff is first crossed while
the excursion is open, that path belongs to the auxiliary boundary kernel
\(B\), even if a later cleanup happens to leave \(I=R=0\).  Its
boundary-causing reaction and endpoint \(W_\ell\)-cost must be included in
(4.2), after which the actual endpoint is reclassified.

The remaining one-active, enabled-access, closed-shell, and all-active
descriptors use their already proved row-local common-\(W_\ell\) kernels.
Passing descriptors use the powered factorial generator estimate.  The
classification proposition, not a search over histories, supplies
exhaustion.

In particular, an exact Family-II row which lies outside the generalized
kernel's stated support must be assigned its own proved row-local episode.
Set membership or similarity of its normalized graph is not a substitute
for that analytic assignment.

### 7.2 The \(H_b\) switch

Choose the detailed-balance \(\ell\) of the reversible all-active top.
The guard-free killed-shell theorem must start from every all-active bad
state, either by its core renewal estimate or by its separately negative
pointwise complement, and must stop with (4.2) for
\(W_\ell\).  A lower-dimensional endpoint is simply reclassified under the
same \(W_\ell\).

The shell theorem is not allowed to normalize \(F_\ell\) differently on
different invariant shells.  Nor may it use recurrence of the lower chart
to justify the first-lower-reaction stopping time.  Its killed renewal and
duration estimates must stand on their own.

### 7.3 The \(H_w\) switch

Use \(\ell=0\).  The compound-activation/fractional-return theorem must
give (4.2) for \(W_0\) from both the dormant and already activated regions,
including seed failures, deaths, upper exits, overshoots, and physical
duration.  The auxiliary height and fluid service integral are proof tools;
the endpoint scalar is still \(W_0\).

### 7.4 What is not an input

A recurrence theorem for a different support pair cannot be used as a local
handoff theorem: the physical support pair never changes when its population
hits a boundary.  Previously closed pair families establish the exhaustion
of the global atlas, but they do not control an endpoint of a hard pair.

Similarly, the certified all-one-active pair theorem cannot automatically
be cited as a row theorem inside a mixed-profile pair.  What is usable is
its underlying all-reaction local interface, and only with the exact
pair-fixed correction \(\ell\) required here.  If the published audited
statement covers only \(\ell=0\), an arbitrary-\(\ell\) row-local
corollary must be proved before it can be used on a nonzero-correction hard
pair.

## 8. Hard-family recurrence theorem

> **Theorem 8.1 (conditional hard-family closure).**
> Fix a remaining hard support pair, arbitrary strongly connected
> orientations of its two linkage supports, arbitrary positive rate
> constants, and a closed irreducible population class \(\Gamma\).  Assume
> the descriptor coverage hypothesis of Section 6 and the Section 4
> contract for every assigned local kernel, with the pair-fixed
> \(W_\ell\) of Section 2.  Then the physical mass-action CTMC is
> nonexplosive and positive recurrent on \(\Gamma\).

### Proof

First, nonexplosion is independent of the Foster construction.  A reaction
which increases total population has source molecularity zero or one,
because every target has molecularity at most two.  Therefore its
propensity is bounded by \(C(1+|x|_1)\), after summing over the finite
reaction set.  Localize at total-population levels and apply Gronwall to
obtain a finite first moment on every finite time interval.  The probability
of reaching level \(m\) before a fixed time tends to zero as
\(m\to\infty\).  Inside a fixed total-population sublevel there are only
finitely many physical states and their total rates are bounded, so
quadratic population-nonincreasing reactions cannot cause an explosion
there.  Hence the chain is nonexplosive.

Work next on the reachable marked lift from Section 3.  Section 6 gives a
finite set \(K\supseteq\widehat K_0\), a generator-good set, and a
state-selected local episode satisfying Theorem 5.1 everywhere else.
The theorem gives finite mean physical hitting of \(K\) from every
reachable marked state.

If \(\Gamma\) is an absorbing singleton, the conclusion is immediate.
Otherwise, start from a state of the finite marked target, take one ordinary
physical jump, and apply the same hitting result from its marked successor.
There are only finitely many target states and finitely many reaction
successors, so the conditional mean time of every positive
target-to-target cycle is bounded uniformly over the finite target.  The
successive positive returns to \(K\) define a finite stochastic trace.
Choose a recurrent state \(k\) of that trace.  Its discrete trace-return
time has finite mean; summing the uniformly bounded physical cycle means
shows that the marked process has finite mean positive return to \(k\).
The standard return-cycle construction therefore gives an invariant
probability \(\widehat\pi\) for the marked process.  If
\(f\) is a finitely supported physical test function, then
\(\widehat{\cal L}(f\circ\mathrm{pr})=({\cal L}f)\circ\mathrm{pr}\),
because reaction rates do not depend on the marks.  Hence the projection of
\(\widehat\pi\) is an invariant probability for the physical chain on
\(\Gamma\).  Equivalently, the physical return to
\(\mathrm{pr}(k)\) occurs no later than the marked return to \(k\), so that
physical state has finite mean positive return directly.  Irreducibility of
the physical class implies positive recurrence of every population state in
\(\Gamma\). \(\square\)

Combining Theorem 8.1 with an independently verified exhaustive support
reduction and the already proved complementary pair theorems gives the
full three-species/two-linkage recurrence theorem.  That final step is a
finite classification corollary; the analytic proof of Theorem 8.1 does not
depend on how the classification was found.

## 9. Proof-dependency audit before publication

The composition is complete only if each answer below is affirmative.

1. **Common scalar.** Is one literal vector \(\ell\), one additive constant
   \(K_\ell\), and one \(W_\ell\) used on every descriptor of the fixed
   pair?
2. **Actual start access.** Does every divergent realizable bad sequence
   start in a proved kernel domain, or is there an independently proved
   all-reaction entrance episode?
3. **Positive debt.** Is a positive-debt hypothesis derived from the
   reachable lift, with zero debt reclassified rather than silently
   discarded?
4. **Physical reconstruction.** Do all renewed self loops retain time,
   internal boundaries, and the actual debt evolution?
5. **Complete endpoints.** Are upward, lower-dimensional, simultaneous,
   and moving-boundary endpoints charged by endpoint-weighted
   \(W_\ell\)-estimates?
6. **No recursive handoff.** Does every local theorem prove its own complete
   stopping inequality without invoking the global recurrence conclusion?
7. **Uniform chart constants.** After fixing rates and the class, are
   positive drift and duration constants uniform along every divergent
   sequence in the chart?
8. **Finite target.** Is the target finite in the marked state space, rather
   than only compact in a scaled or shell coordinate?
9. **Physical time.** Is every duration estimate for the CTMC clock rather
   than an embedded fast-jump count?
10. **Nonexplosion first.** Is strong Markov/Dynkin usage supported by the
    independent linear population-growth argument rather than inferred from
    recurrence afterward?

These are logical proof obligations, not additional finite searches.
