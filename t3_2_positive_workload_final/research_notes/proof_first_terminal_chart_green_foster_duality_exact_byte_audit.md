# Exact-byte hostile audit of charged-seam terminal Green--Foster duality

**Independent proof-first audit, 2026-08-12 PDT.**  This audit freezes

```text
research_notes/proof_first_terminal_chart_green_foster_duality.md
SHA-256 899aa11e15d3e23f629bf06cdfac3a05a47915f5a90378bb8d91982ae0ed6211
561 lines, 21781 bytes
```

There are two separate verdicts.

1. The abstract charged-seam theorem is **STRICT PASS** at these exact bytes.
   The target states explicitly that episode starts and ends are recursively
   selected stopping times and that the event that episode (j) exists is
   measurable at its start.
2. The currently frozen T3-2 local branch theorems do **NOT** establish the
   seam hypothesis (4.4), (7.6), or (7.8).  They control positive increments
   of episodes already running in a chart, whereas the theorem needs uniform
   integrability of the incoming chart potential at rare boundary entries.

The first verdict validates the new abstract repair.  The second forbids its
use as a completed T3-2 composition until a weighted boundary estimate, a
global common potential, or an equivalent global flow argument is supplied.

## 1. Killed Green object and finite circulation

For a nested finite exhaustion, the killed return time increases to the
positive return time.  Monotone convergence therefore gives a diverging
normalizer under the infinite-mean-return hypothesis.  The labelled
occupation in (1.3) has total mass one.

For each fixed state, irreducibility supplies a simple positive-probability
path to the reference state before a new visit to the fixed state.  Killing
can only shorten that attempt.  The visit count is consequently dominated by
a geometric random variable uniformly in the exhaustion, proving finite-set
escape after normalization.

Bounded indicator tests telescope with an endpoint error bounded by
$2\lVert f\rVert_\infty/t_m$.  Pushing those tests to a finite chart
partition gives a limiting circulation.  A finite directed acyclic
condensation cannot carry a nonzero circulation across components: summing
balance over a source component makes its outgoing flow zero, and induction
removes every cross-component edge.  Thus a positive terminal component with
zero unweighted exit fraction is valid, subject to the explicitly stated
retained-mass/localization interface.

This argument proves only unweighted terminality.  The target correctly does
not turn it into an unbounded-potential balance.

## 2. Episode-count transfer and adapted summation

If the nonoverlapping episodes tile the retained trace up to one uniformly
integrable partial episode, contain at least one retained event, and have
conditional expected retained length at most $L$, then

\[
 A_m\le r_m\le LA_m+O(1).
\]

Hence $A_m\to\infty$, and an exit episode count bounded by the retained
structural-exit count satisfies $Q_m/A_m\to0$.  The target correctly warns
that a phase with a divergent waiting count cannot be hidden in this step.

For the proof of Theorem 6.1, predictability is load bearing.  The target now
states stopping-time starts and
\(\{j<N_m\}\in{\cal F}_{\sigma_{m,j}}\), so conditional expectations may be
summed over the random list by deterministic truncation followed by monotone
or dominated convergence.  Exit starts have total expected count at most
$\varepsilon^{-1}Q_m$; finite-state exceptions are $o(A_m)$.  The
uniform positive $p$-moment bounds their discarded positive contribution.
Thus

\[
 \limsup_m {1\over A_m}{\mathbb E}\sum_{j<N_m}D_{m,j}\le-\delta.
\]

Without predictability a retrospectively selected list would not support
this conditional summation.  The exact target has removed that ambiguity.

## 3. Exact seam telescope

For every finite episode list, exact telescoping gives

\[
 \sum_jD_{m,j}
 =V(Y_{\rho_{N-1}})-V(Y_{\sigma_0})
  -\sum_j\{V(Y_{\sigma_{j+1}})-V(Y_{\rho_j})\}.
\]

Since $V\ge0$, deleting the terminal value and retaining only positive gap
recharges gives the lower bound $-B_m$.  Therefore
${\mathbb E}B_m/A_m\to0$ yields the opposing normalized lower bound
zero and contradicts the local negative bound.  No second chart potential is
evaluated and no exit jump is counted twice.

Lemma 7.1 is also correct.  If each gap begins with a recorded exit, the
number of gaps is at most the exit count plus one.  Uniform conditional mean
recharge and a sublinear initial value give ${\mathbb E}B_m=o(A_m)$.
A uniformly geometric number of adapted subepisodes with uniformly bounded
conditional positive moments has bounded total mean recharge.  More exactly,
if the event that subepisode $k$ occurs is measurable before that subepisode,
conditional Lyapunov/Hölder and Tonelli give

\[
 {\mathbb E}G
 \le \sum_{k\ge1}{\mathbb E}[{\bf1}_{\{k\le R\}}a_k]
 \le C_p^{1/p}\sum_{k\ge1}{\mathbb P}\{k\le R\}
 =C_p^{1/p}{\mathbb E}R.
\]

Thus the corrected argument needs no independence and does not use the
invalid unconditioned estimate
${\mathbb E}[{\bf1}_Aa]\le C^{1/p}{\mathbb P}(A)$ when $A$ is selected after
observing $a$.

The boundary-subprobability formulation is the precise general criterion.
Unweighted terminality gives only $\beta_m(E)\to0$.  Tail uniform
integrability (7.6) gives $\int V\,d\beta_m\to0$, while (7.8) implies it
by Hölder:

\[
 \int V\,d\beta_m
 \le\left(\int V^{1+\gamma}d\beta_m\right)^{1/(1+\gamma)}
      \beta_m(E)^{\gamma/(1+\gamma)}.
\]

This is strictly stronger than a moment bound on $(\Delta V)^+$ after
an episode has already started.

## 4. Counterexample replay

The alternating-block birth--death example is valid.  A right-biased nearest
neighbour chain with $p=3/4,q=1/4$ is irreducible and transient.  Killing at
distance $R$ or the first state gives gambler's-ruin probability

\[
 {1-q/p\over1-(q/p)^R}\longrightarrow {2\over3}
\]

of reaching $R$, and optional stopping bounds the expected killed length by
$R/(p-q)$.  Thus the Green mass is $\Theta(R)$.

Blocks of lengths $2,2,3,3,\ldots$ have only $O(\sqrt R)$ boundary sites
up to distance $R$, while both chart labels occupy a positive fraction of
the remaining sites.  Transience bounds expected visits to each site
uniformly.  Hence both chart traces have positive normalized occupation and
zero normalized unweighted exit count.

On the (m)-th block, the corresponding potential is (2m-k), so its value
lies between (m) and (2m).  It is therefore proper on the union of blocks
with that chart label.  Inside a block it has one-step drift (q-p=-1/2),
positive increment at most one, and one-step episodes.  But the next block
entry recharges the new chart's potential by an amount of order its block
index.
Through $M\asymp\sqrt R$ blocks the total charge is
$\sum_{m\le M}m=\Theta(R)$, with positive probability bounded away
from zero.  It is the same order as the episode count.  Thus the example
really satisfies the unweighted/local-moment inputs and fails exactly at
(4.4).

## 5. T3-2 interface verdict

The frozen both-available and Bellman/Flat0 results provide actual endpoints,
bounded or geometric episode counts, physical-duration moments, and uniform
moments of positive **episode increments**.  The finite terminal circulation
provides vanishing **unweighted** entry and exit fractions.

Those statements do not bound the value of the newly selected marked
factorial or branch-specific potential at an incoming chart boundary.  In the
notation of Section 7 they do not establish (7.6) or (7.8), and therefore do
not establish (4.4).  The counterexample shows this is a logical obstruction,
not a missing cosmetic estimate.

A publication-safe full composition still needs at least one of:

1. one common proper potential across every branch actually traversed;
2. an explicit boundary-entry tail estimate (7.6), or a higher boundary
   moment (7.8), for every terminal chart potential; or
3. a global flow/separation proof which retains the compensating high-value
   boundary flux instead of discarding it with its vanishing count.

Corollary 6.2 now separates its alternatives exactly: a supplied classwise
theorem may establish the desired recurrence directly; otherwise every
positive terminal trace must be ruled out by an invariant obstruction or by
Theorem 6.1.  It explicitly refuses to treat an arbitrary CTMC invariant
probability as an invariant law of the embedded jump chain.  The former scope
ambiguity is therefore repaired.

## 6. Render and final verdict

The exact target rendered independently to MathJax HTML and through Tectonic
using Pandoc's single-backslash TeX-math reader.  The default PDF has ten
letter-sized pages.  Tectonic reported only two harmless underfull boxes (the
wrapped title and one prose paragraph), with no overfull box, missing glyph,
clipped display, or compilation error.

**ABSTRACT THEOREM: STRICT PASS.**

**CURRENT T3-2 APPLICATION: STRICT FAIL AT THE UNPROVED WEIGHTED SEAM.**
