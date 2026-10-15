# Independent adversarial stochastic-family review of PR 764

Frozen PR head: `88acf20cdd5b4fe8605dab7eb27733b7deda1c47`.
Problem: 30005453 / OWR-12697708-006.
Review date: 2026-10-14 UTC.

## Verdict

**PASS for the candidate's strictly positive equilibrium theorem and its
simultaneous coordinatewise almost-sure convergence conclusion.** No
stochastic analytic gap, unstated spatial lower-rate bound, improper stopping
argument, or invalid infinite-dimensional compactness assumption was located.
The proof also verifies the advertised extension to arbitrary deterministic
positive integer initial counts, finite on each edge, without a uniform bound
on that array. No original artifact has been edited.

**FALSE for literal uniqueness among all nonnegative equilibria.** The
alternating 2/0 arrays on the integer line give a counterexample for every
0<alpha<1, with a positive denominator at every vertex. The author's v2
expressly acknowledges this distinction. The positive theorem must be
described as a corrected formulation, rather than a proof of the literal
unrestricted uniqueness sentence. The supplied counterexample independently
settles that literal uniqueness assertion negatively. These are two logically
distinct outcomes.

This is a mathematical verdict. No priority, novelty, publication readiness,
human peer review, or formal proof-assistant certification is asserted.

## Input, independence and method

The first mathematical input read was the frozen author_v2/PROOF.md.
INDEPENDENT_DERIVATION.md was saved at 05:02:17 UTC, before consulting any
historical audit conclusions. It reconstructs the infinite graphical
construction, predictable intensity, exact H transform, normalized martingale
law, noncircular lower growth, scaled vertex dynamics, diagonal extraction
and convergence argument. Only after that checkpoint were the frozen source
review, first audit and acceptance report read. Their conclusions agree with
the independently saved stochastic derivation. The equilibrium and rigidity
dependencies were subsequently rechecked; those supplementary crosschecks
are not presented as an independent deterministic-family review.

No code from the author or earlier reviewers was imported or invoked by
independent_controls.py. The controls derive the local intensity and bracket
from incident counts and rational rates. They are diagnostics supporting
arithmetic and boundary checks, not a numerical substitute for the analytic
proof. Neither this review nor its controls initiate a fresh proof-search turn.

## Exact verified hypothesis

The graph is countable, undirected and simple, has uniformly bounded degree,
and may be disconnected. Isolated vertices are discarded. Rates satisfy
0<p_v<=P<infinity, with infimum permitted to be zero. The reinforcement
exponent is 0<=alpha<1. Each initial edge count is a fixed positive finite
integer. The edge selection rule is proportional to its count raised to
alpha. The verified result gives a unique equilibrium positive on every edge
and almost-sure convergence of N_e(t)/t to it for all edges simultaneously.
Convergence is coordinatewise, without a spatially uniform random threshold
or spatially uniform positive lower bound. Empty edge sets give the unique
empty array and vacuous convergence.

## Infinite construction and compensator

The finite causal ancestor argument in the independent derivation supplies
the omitted detail behind the author's usual graphical construction. For
a fixed local query, a predecessor chain has at most D+1 choices per step
and strictly ordered Poisson times. Its expected length-n count is bounded
by a factorial tail, while every node has finitely many predecessors on a
finite horizon. Infinite ancestry is excluded by the finitely branching tree
lemma. Countable intersections construct all coordinates. Global total clock
rate need not be finite. Arbitrarily large remote initial counts do not alter
this causal bound.

In the natural, nonanticipating filtration, the edge intensity is
lambda=N(t-)^alpha q with q=p_u/S_u(N(t-))+p_v/S_v(N(t-)). Both lambda and q
are bounded by p_u+p_v. Predictable left limits are correctly used. Because
H(n+1)-H(n)=n^(-alpha), its exact compensated decomposition is

    H(N(t))-H(N(0))=Q(t)+M(t),
    <M>(t)=integral N(t-)^(-alpha) q(t) dt <= Q(t) <= 2Pt.

Thus finite-horizon square integrability follows directly; there is no hidden
localization gap. The process L=integral (1+Q)^(-1)dM has bracket expectation
at most one. L2 martingale convergence and integration by parts give M/Q->0
on Q->infinity by weighted Cesaro convergence. This works with random Q
dependent on M. No independent time-change hypothesis is smuggled in.

## Lower growth and scaled representation

Endpoint-clock strong laws first give each edge's upper asymptotic growth
bound. Only finitely many incident edges enter one fixed edge's denominators,
so their upper bounds yield q(t)>=k_e t^(-alpha) after a neighborhood-specific
finite random time. Here k_e>0 even when the global rate infimum is zero.
This independently establishes Q->infinity and its t^(1-alpha) lower scale.
Integral comparison for H and M/Q->0 then prove the claimed positive
coordinatewise linear lower growth bound. The same identities give Q=O(t^c)
and M/t^c->0, without circularly assuming convergence of N/t.

The vertex quantities A_v=c t^(-c) integral p_v/S_v(N) satisfy
X_uv^c=A_u+A_v+o(1). Every coordinate has a common limiting upper bound
(2P)^c and its own positive limiting lower bound ell_v. In logarithmic time,
a'_v=c[p_v/S_v(X)-a_v] almost everywhere. For fixed v, the finite incident
edge set and its individual lower growth bounds bound this derivative after
a finite random time. Neither derivative bounds nor those times are asserted
uniformly in v. The H(N(0)) offset is a finite coordinate constant and
vanishes under scaling, so unbounded positive initial arrays cause no gap.

## Limiting trajectories and completion

Coordinatewise eventual bounds and equicontinuity suffice for Arzela-Ascoli
on each compact interval, then a countable diagonal subsequence over vertices
and intervals. They produce a positive classical complete trajectory b on
all real times with a common upper bound. If r_e(t)->0, it is uniformly small
on a translated compact logarithmic interval because that interval's smallest
physical time tends to infinity. The finite incident sums and strictly
positive limiting coordinates permit uniform convergence of denominators
and their reciprocals. Passing to integral equations gives the correct
vertex dynamics. Supremum-norm compactness is never required.

Section 7's deterministic dependency is applicable precisely because the
trajectory is positive, bounded above in all coordinates, and complete in
both time directions. Its fixed-coordinate upper/lower strip argument uses
a space-time supremum only to select an approximate extremum. It neither
differentiates an infinite supremum nor assumes one is attained. The lower
strip estimate uses reciprocal monotonicity, avoiding an unjustified global
lower bound on the current denominator. Backward integration contradicts
the fixed positive derivative bound unless b=z. A separated sequence in
one coordinate would then contradict extraction at time zero. This proves
actual convergence, not just one equilibrium subsequence.

## Boundary and falsification checks

* Alpha=0 is treated separately by uniform choice and Poisson thinning.
  The limit is p_u/d(u)+p_v/d(v), and positive-equilibrium uniqueness is direct.
* Alpha=1 is correctly excluded. Positive alternating equilibria on even
  cycles falsify a critical uniqueness extension.
* Initially zero edges cannot be added at alpha>0: they stay zero.
* No negative-exponent, unbounded-degree, loop/multigraph, fractional-initial-
  count, or uniform spatial convergence extension is promoted by this review.
* Countably many independent disjoint edges with unit endpoint rates have
  unbounded count fluctuations at each fixed positive integer time almost
  surely. Positive probability of arbitrarily large Poisson counts and
  infinitely many independent coordinates prove this. Thus the author's
  refusal to claim common spatial random bounds is mathematically necessary.
* Disjoint edges with endpoint rates 2^(-k) have positive limiting coordinates
  2^(1-k) whose infimum is zero. This tests the nonuniform-rate boundary.
* On the doubly infinite path with unit rates, each 2/0 alternating array
  has incident denominator 2^alpha. Active edges receive rate two, zero
  edges receive zero, and the all-ones array is a third fixed point.

## Primary-source scope check

The official report's equilibrium definition and Conjecture 1 do not expressly
require positivity on every edge. Its model gives initial counts without
imposing unit initialization. This prevents attributing the corrected positive
scope to an explicit report convention.
[OWR report, printed pages 654–655](https://ems.press/content/serial-article-files/47008).
The 2021 author manuscript expressly sets alpha>=0 and unit initialization;
its nonvanishing equilibrium class is distinguished in the proof.
[Couzinié–Hirsch v2, page 3](https://arxiv.org/pdf/2010.03347v2).
Both complete PDFs were freshly retrieved with hashes matching the historical
source receipts. The three relevant rendered pages were visually inspected.
Third-party source bodies, extracted text and rendered pages are private scratch
and excluded from the closed public review. Source retrieval is metadata only.

## Exact remaining gap

No proof repair is needed for the stated positive theorem or the integer-initial-
count extension. The unrestricted uniqueness assertion is false, so a manuscript
cannot honestly frame the positive theorem as proving that literal assertion.
The author v2 already records this correction. Current-literature priority is
outside this mathematical-family verdict and remains for the separate priority
audit. A paper proving the positive formulation must retain that distinction,
the initialization and exponent scope, and coordinatewise convergence language.
