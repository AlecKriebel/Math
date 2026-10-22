# Independent audit: unit-rate planar empires, 9700022

Date: 2026-10-10 UTC.

## Verdict

**PASS AS RIGOROUS PARTIAL RESULTS; FINITE-TIME HEGEMONY REMAINS OPEN.**

This publication edition preserves the complete independent analytic review.
The accepted analytic proofs require no mathematical correction; editorial
changes only reconcile review status and the distribution boundary. The
public proof identities are:

- PARTIAL_RESULTS.md: 10,290 bytes; SHA-256 `5e955ddca0959cf2cdd29aef13396d390562fef85f6f51df4b2e3a2f3b4bee11`.
- CONTOUR_GAP.md: 9,738 bytes; SHA-256 `c22210ae0127f6eccc735b723df9a26956add7c7fc20f231a99828b7543d37de`.

During the original audit, every listed author artifact matched its declared
hash and byte count. No mathematical defect requiring a correction was
identified, and no author file was edited during that audit. This verdict does not certify a proof of the original conjecture,
a globally constructed process beyond the stated interval, or completeness of
the literature search.

The accepted scope consists of:

1. The exact unit-current-pair finite-graph generator and its marked-Poisson
   realization; a local infinite-volume construction whenever the proposal
   graph has finite components.
2. Simultaneous absence of infinite empires on the square-cell start through
   the closed interval `[0, log 2]`, including the critical endpoint.
3. The exact initial-clique projection and the positive two-interface covariance.
4. The finite-volume suppressed-process Feynman–Kac identity, correct
   outer-boundary event with holes permitted, and honeycomb incidence bound.
5. The 14-edge, three-collinear-hexagon repeated-label witness.
6. The factor-two time correction to the explicitly defined idealized source
   chain, with its limited effect on transient occupation integrals.

This manuscript and its independent mathematical audit are AI-assisted and
unrefereed. No external human peer review, journal acceptance, or formal
proof-assistant certification is claimed. No novelty or bibliographic
priority is claimed for the elementary tools.

## Mathematical review

### A. Current pairs and marked proposals

At a partition into current blocks, a pair with multiplicity `m` is offered
`m` independent proposal streams. Each carries acceptance probability `1/m`,
so its accepted intensity is exactly one. The relevant multiplicity includes
every original edge joining those blocks, whether that edge has previously
proposed or not. Rejected proposals do not retire an original edge. Both
details are necessary and are correctly stated in the packet.

An accepted merger has a supporting proposal edge. Induction therefore keeps
each empire inside one connected component of the proposal graph. The
comparison direction gives a nonpercolation interval only: percolation of the
larger proposal clusters does not imply percolation of the thinner process.

The audit tested a three-vertex triangle after one initial merger: the two
remaining interfaces represent a single current pair and have total rate one,
not two. A mark `3/4` is rejected when `m=2`, even if just one of the two
interfaces has proposed. A later mark `1/4` on the same edge can be accepted.

### B. Locality, adaptedness, and the closed endpoint

The proof does not assume an infinite chronological ordering of all events.
For a finite-component proposal horizon `T`, each component contains finitely
many initial vertices and edges, and hence finitely many proposals up to `T`.
Every boundary edge leaving that component has no proposal before `T`.
Chronological construction within components is consequently legitimate.

Future exposure is a proof device, not extra information used by the dynamics.
For any earlier time `s`, restrict to each component of the proposal graph at
`s`. No event through `s` crosses its boundary. Induction over its finite
chronological proposal list gives exactly the same block partition whether
computed alone, inside a larger horizon component, or in a finite larger
domain. In computing `m`, all original edges between current blocks are
present in each computation. Thus the partition at `s` is determined by the
past marked processes. The left-limit acceptance factors are predictable,
and the accepted pair intensity remains `m * (1/m) = 1`.

Finite proposal components at `T` give finiteness simultaneously for every
earlier time; separate deterministic-time null events need not be combined
over uncountably many times. Square-lattice critical nonpercolation supplies
this event at `T=log 2`. Infinite expected component size at criticality is
irrelevant to almost-sure finiteness of each component. Local nonexplosion is
what is proved; there is no claim of a finite total event count across the
whole plane. The stated maximum-degree variants use strict inequalities and
keep triangular cells and hexagonal cells distinct.

The packet correctly avoids claiming that a hegemony-time infimum must be
strictly larger than `log 2`: an infimum need not be attained. It also avoids
silently extending this construction beyond a percolating proposal horizon.

### C. Clique projection and dependence

For an initial clique, each two different marked blocks lie in two different
full current blocks that remain adjacent along an original marked interface.
There is precisely one merger of that full pair, at rate one. All other full
mergers either leave the marked partition unchanged or correspond to one
other marked-pair merger. The restricted generator is therefore exactly the
Kingman generator; outside mergers do not add an extra marked-pair rate.

The three-cell computation satisfies the full finite Kolmogorov equations,
not only a finite list of Taylor coefficients. At `t=log 2` it gives joint
survival `5/16`, the product of marginal survivals `1/4`, and covariance
`1/16`. This rejects independent surviving interfaces. An arbitrary marked
set cannot replace a clique: the two endpoints of a three-vertex path have
initial marked-merger rate zero, not one.

### D. Suppression and Feynman–Kac

Since coalescence is irreversible, keeping all forbidden interfaces alive
through time `t` is the same as remaining in the allowed state set at `t`.
A current merger exits that state set exactly when its pair is represented
by at least one forbidden edge. Multiple forbidden edges for the same pair
give one killing transition. Thus the killed generator is the suppressed
generator minus the diagonal distinct-pair killing count.

This proves the stated identity for every bounded final-state function in
finite volume. The coarse bounds follow from `1 <= k_F <= |F|`; the
independent-edge expression is a lower bound, not an upper Peierls estimate.

For a contour, every cross-side initial adjacency is forbidden, and every
remaining allowed merger is entirely on one side. The suppressed generator
is the sum of the two side generators. Their independent construction and
the factorization used after the incidence inequality are justified.
Independence is a property of the suppressed law, not the original law
conditioned on survival. On a triangle at `t=log 2`, the outside pair merges
with probability `1/2` under suppression but `3/5` conditional on survival of
the two crossing interfaces. The packet does not confuse these laws.

The finite-volume limitation is material. No unproved infinite-volume
Feynman–Kac identity or limiting contour estimate is promoted as a theorem.

### E. Outer boundaries, holes, and honeycomb incidence

A simple honeycomb circuit is a Jordan curve made of initial sides. The
inside cells that meet it in a side cover its entire inside boundary layer.
Under suppression, the connected region containing `b` cannot cross the
curve. If it contains every such cell, its unbounded complementary component
has exactly that curve as boundary, although bounded holes may remain.
Conversely, having this outer boundary requires every inner incident cell to
belong to the region. Thus the packet's indicator represents the correct
outer-boundary event. A six-cell ring provides a direct check: its outer
boundary has 18 edges and its central hole has a separate six-edge boundary.

At a honeycomb vertex, the two successive contour sides share one of their
two cell labels, because only three cells meet there. Merging labels preserves
this shared vertex in the bipartite incidence graph. The cyclic edge walk
visits every incident region, so the graph is connected. The bound
`k_C >= I+J-1` follows. It is sharp for one interior hexagon and its six
exterior neighbors; replacing it by `I+J` is false.

The trivalence assumption is essential. A two-by-two square-cell block has
eight boundary edges, four interior incident cells and eight exterior
incident cells. Its incidence graph has four components, and the honeycomb
bound would incorrectly require at least eleven edges. The packet restricts
the proposition to honeycomb contours, as required.

### F. Repetition witness

Independent integer-coordinate polygon construction, with shared sides
cancelled and boundary cycles walked explicitly, verifies that three
collinear hexagons have one simple 14-edge outer circuit. It has three
distinct inside labels, ten distinct outside labels, and four maximal
inside-label runs. The central cell is the repeated label. The contrast
between three distinct labels and `n-3=4` occurrences is exact and does not
depend on floating-point geometry.

This is an illustration of the acknowledged label-identification obstacle,
not a counterexample to hegemony or a claim to rediscover an overlooked
conclusive failure of the original paper.

### G. Idealized chain time normalization

For initial total `N`, the initial alive state has total exit intensity `2N`:
`N` from deaths and `N` from killing. Its survival probability is therefore
`exp(-2Nt)`. The literal source expression without time acceleration would
give `exp(-Nt)`. The discrepancy is genuine.

For each token, survival without removal through `t` has probability
`u=exp(-2t)`; safe removal by then has probability `(1-u)/2`. Independence of
these competing token events gives the packet's full joint expression and
the corrected time `2t`. This also verifies the fictitious zero state's
positive limiting mass `2^(-N)`. Its occupation integral is infinite and is
properly excluded from the transient formula.

For every state with positive total count, changing variables from `2t` to
`t` introduces exactly a factor `1/2` in addition to the state weight. The
displayed beta-integral expression is correct. This preserves convergence
of the relevant idealized occupation series; it does not establish that the
idealized count process describes the planar process.

## Recorded primary-source comparison

The following source observations come from the author review and independent
audit on 10 October 2026. Edition preparation performed no new scholarly-source
retrieval, source-file rehash, visual inspection, or literature search.

During that audit, the full retained ten-page 2010 paper was read, and its pages 6 and 7 were
visually checked against the algebra. The author PDF and maintained problem
page were independently reopened. Section 3 explicitly presents a heuristic;
section 3.1 identifies repeated region labels and additional nonconsecutive
adjacencies as obstacles. The audited packet preserves those qualifications.
The source's displayed rates and equation (9) confirm the time correction.
The paper also cautions against inferring refinement couplings from pointwise
rate inequalities alone. The packet instead constructs its coupling directly.

The critical square-lattice endpoint was independently checked in
Bollobás–Riordan, section 4, Theorem 8 and its proof. The maintained page
continues to present the unit-rate question; that is not an exhaustive
literature-status certificate. The 2017 Poissonian-coloring paper has a
different point-deletion/nearest-point dynamics. The unrelated Gauss-sums retrieval was correctly excluded as evidence for
this problem.

Public sources:

- Aldous, Ong, Zhou, *Empires and percolation: stochastic merging of adjacent
  regions*, J. Phys. A 43 (2010), 025001:
  https://www.stat.berkeley.edu/~aldous/Papers/me123.pdf
  and https://doi.org/10.1088/1751-8113/43/2/025001
- Aldous's maintained problem page:
  https://www.stat.berkeley.edu/~aldous/Research/OP/empires.html
- Bollobás–Riordan, *A short proof of the Harris–Kesten Theorem*:
  https://arxiv.org/html/math/0410359v3
- Aldous's distinct 2017 model: https://arxiv.org/abs/1701.00131

## Recorded independent exact verification

The independently written checker imported no author code and used integer
or rational arithmetic. During the recorded audit, normal and Python `-O`
runs each passed 258,074 explicit checks; their reports agreed apart from
the optimization flag. This is historical aggregate metadata. Programs and
raw outputs are not distributed and were not rerun during edition preparation.
Coverage included:

- Every simple graph on one through five labeled vertices: 1,099 graphs and
  21,930 connected-block partitions; exact thinned generators and all initial
  clique restrictions.
- Every nonempty forbidden-edge set at every viable state on graphs of order
  at most four: 2,465 distinct-pair killing and diagonal checks; 2,476
  vertex-cut tensor-generator checks.
- All fixed translation classes of connected polyhexes through six cells:
  1,059 shapes, 1,060 boundary cycles, and several label-identification maps.
  The exact polygon walks also test hole and repeated-label examples.
- Full polynomial forward equations and exact integrated probabilities for
  63 initial idealized death-chain states, including zero in either initial
  coordinate; 1,232 positive-count occupation integrals.
- 12,960 proposal-component/horizon comparisons across exhaustive four-vertex
  edge orders at three rational mark levels.
- Eleven explicit negative controls, all detected. They reject original-edge
  rates, proposed-only denominators, retiring rejected edges, nonclique
  Kingman projections, interface independence, conflating suppression with
  survival conditioning, the missing time change, occurrence/distinct-label
  equality, ignoring holes, the stronger incidence bound, and extending the
  honeycomb incidence statement to square contours.

During the recorded audit, the author's normal and optimized checks were
also rerun and each output byte-matched its corresponding sealed report.
All recorded input/source byte identities were independently verified.
The analytic verdict depends on no omitted program, raw output, or dataset.
Finite exact checks support, but do not replace, the mathematical arguments
above or prove any infinite-volume hegemony statement.

## Final scope boundary

The construction and diagnostics are accepted unchanged. The missing
contour-uniform estimate for the actual process remains missing, and
post-threshold infinite-volume construction remains outside these results.
General finite-time hegemony is **OPEN** for the target question. No
finite-time hegemony theorem, counterexample, or post-threshold global
construction is certified.
