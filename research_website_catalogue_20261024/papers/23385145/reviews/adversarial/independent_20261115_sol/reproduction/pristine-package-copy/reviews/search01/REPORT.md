# Independent adversarial algorithm/reduction audit

PR 570; problem 30006605 / OWR-14299911-007; frozen head
`417ca52e83cf06b07c388d89c756cfd86473d5b0`. Reviewer family `search01`.
Completed 2026-10-15 UTC. This verifies complete candidate 1/5; it is not a new
discovery attempt or a final historical-priority/package decision.

## Verdict and exact remaining boundary

**PASS for the threshold reduction, implicit optimization, witnesses/all centers,
and stated exact-operation complexity, under the explicit additive-oracle
interface below.** No counterexample or blocking mathematical correction was
found. The proof under that interface is complete; no new conjecture, local
convexity assertion, or unproved optimization lemma remains inside this review.

The imported BDH algorithm is an explicit mathematical dependency. This family
does not independently certify its entire proof or final applicability; that is
a separate review family. Consequently this report alone does not certify the
unconditional headline theorem. If BDH supplies exactly the stated deterministic
interface, the candidate's O(n log^5(2n)) consequence follows. The controls do not
implement or benchmark a fast general median-graph additive oracle.

The exact reviewed input is a finite nonempty connected simple graph, promised
median, supplied by adjacency lists with every edge length 1; weights are
nonnegative finite exact reals. Output is a graph vertex, the exact optimum
multiplicative radius, and all graph-vertex centers. No recognition, continuous
center, nonunit-edge, or infinite-input algorithm is included.

## Independence and object identity

Read the candidate proof, controls, and source-status account before old audit
conclusions. Saved `INDEPENDENCE_CHECKPOINT.md` at 2026-10-15 04:08:39 UTC with
the independently derived threshold equivalence and contraction proof. The
fresh independent suite had finished before the old audit was first read at
04:12:18 UTC. No concurrent reviewer's conclusions were requested or read. The old
audit agrees with this component verdict but was not used to derive it.

All files executed were new scratch copies or this review's own code. Frozen
originals were read only. No Git/index/branch/canonical writes, external-person
communications, other-agent contact, or spawning occurred. Parent-only status
reports were sent. All authored work is in this dedicated directory.

The frozen proof SHA-256 is
`b0b948da64c113dfff1349a2aae48389531c2a8bd719dcdd2ab9483a6fc37d76`;
the frozen author control program is
`77ed594066bbcc5a30129a1748604363c573797f0307268ea4e75c2d0a5589fb`.
All seven entries in the bundle seal and all seven in the old audit seal match.
Full input hashes and equality checks are in
`REPRODUCTION_AND_INPUT_HASHES.json`.

## 1. Target and success criterion

The [official OWR report](https://publications.mfo.de/handle/mfo/4442), Ducoffe,
printed pp. 504-506, defines nonnegative real multiplicative vertex profiles and
vertex centers, then asks for almost-linear weighted centers on bounded
cube-dimension median graphs. Its finite n-vertex complexity setting supports
the candidate's finite algorithmic interpretation. Arbitrary edge lengths are
discussed as a separate extension. Source checks and PDF hashes are recorded in
`SOURCE_CHECKS.md`. The target is not radius-function locality (the distinct Open
problem 2).

For this review, success means a universally justified procedure on those inputs
with the claimed oracle count and exact real-operation bound, plus independent
falsifiable controls checking full feasible sets and complete center sets. Finite
tests support the derivation; they do not replace it. Historical novelty is a
different question and is not decided here.

The empty-support convention needs a brief explicit statement: the candidate
uses max over all vertices, so every radius is zero when every weight is zero.
The later [ESA primary source](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2026.133),
p. 133:6, explicitly makes all vertices centers in that case. This is a consistent
boundary convention, rather than a hidden restriction to positive profiles.

## 2. Exact imported interface

Required assumption A: Given adjacency lists of any finite connected simple
unit-edge median graph G on n vertices and labels a:V->{0,...,n-1}, a deterministic
algorithm returns every value

    E_a(x) = max_{u in V} (d_G(x,u) + a(u))

in O(n log^4(2n)) operations, including all needed preprocessing. No embedding,
cube-dimension bound, supplied Theta classes, or pairwise-distance table may be
an additional input. Integer calculations on these O(log n)-bit labels and the
algorithm's graph data are counted in its advertised model. Re-running its
entire preprocessing for every threshold already fits the candidate's bound.
There is no need to infer a reusable data structure or an unadvertised batched
query guarantee.

This is exactly the interface the candidate attributes to BDH. The parent must
combine this review with the independent BDH source/proof verification before
promoting the unconditional conclusion. No oracle result has been proved by
the finite reference experiments here.

## 3. Independent threshold proof

Set D=n-1. Finite connectivity and unit edges give integer distances in [0,D].
For R>=0 let

    b_R(u) = max {k in {0,...,D}: k w(u) <= R},
    a_R(u) = D - b_R(u).

Zero belongs to the defining set. Because w(u)>=0, membership is an initial
integer interval. For each u and x:

    w(u)d(x,u) <= R
       iff d(x,u) <= b_R(u)
       iff d(x,u) + a_R(u) <= D.

Taking all u constraints gives equality of complete feasible sets:

    {x : r_w(x) <= R} = {x : E_{a_R}(x) <= D}.

This uses only bounded integral distances and nonnegative profile weights; the
median promise enters solely through the fast imported oracle. It preserves
the graph and every zero-weight vertex as an eligible center. There is no
subdivision, product embedding, Helly assertion, or local-unimodality premise.

Boundary attempts to falsify it:

| Case | Exact implication | Result |
| --- | --- | --- |
| w(u)=0, R>=0 | b_R(u)=D, a_R(u)=0; d(x,u)<=D is vacuous | Correct |
| R=0, w(u)>0 | b_R(u)=0, forcing x=u | Correct |
| R=k w(u) | The kth index is included by <= | Correct |
| R/w(u)>D | Clamping at D removes no possible distance | Correct |
| R<0 | Every r_w(x)>=0, so no feasible vertex | Correct |
| n=1 | D=0; only distance and optimum are zero | Correct |
| All weights zero | All vertices feasible at R=0 and all are centers | Correct |
| Exactly one positive weight | Its support vertex is the unique zero-radius center | Correct |

For example, with two vertices and weights 1,3, the optimum is 1 at the second
vertex. The threshold at 1 includes that endpoint exactly; any threshold in
[0,1) excludes both. An implementation that used a strict comparison at a floor
boundary would fail this case. The author uses the correct non-strict bound.

Arbitrary edge lengths would invalidate the integer step: on a two-vertex graph
with an edge of length 1/2 and both weights 1, the true optimum is 1/2 while the
candidate integer threshold at 1/2 disallows distance 1/2. This is an explicit
outside-domain counterexample, confirming why the unit-edge assumption must be
retained. No such edge lengths are included in the theorem or target model.

Finding b_R needs no real floor/division operation. Binary search over the n
integer indices compares k w(u) with R and costs O(log(2n)) exact comparisons.
For w(u)=0 the upper-bound search returns n and thus b_R(u)=n-1. The additive
labels always lie in [0,D], including when input real weights have extreme scale.

## 4. Independent implicit-search proof

Each r_w(x) is an attained maximum, and its minimizing vertex exists because V
is finite and nonempty. Therefore rho=min_x r_w(x) belongs to the multiset

    S = {k w(u): u in V, 0<=k<=D}.

There are n sorted rows, each with n entries and repetitions allowed. Retain an
inclusive interval per row and a feasible incumbent B=D max_u w(u). Any initial
vertex witnesses radius <=B, even if its actual radius has never been evaluated.
The maintained invariant is:

    B is feasible, and either B=rho or an active entry equals rho.

For an active row of length L, its lower middle entry has at least L/2 entries
on each weak side. In particular, even lengths and singleton rows satisfy this
bound. Give its midpoint selection weight L. A weighted median q has at least
M/2 total row length on each weak side, where M is the total active length.
Sorting and taking the first cumulative weight reaching M/2 works: the mass
strictly below its value is less than M/2, even if the chosen position occurs
inside a group of equal values. Thus the mass at or above it is at least M/2;
the mass at or below it is at least M/2 by the cumulative choice.

If q is infeasible, rho>q, and every optimum copy survives removal of <=q. If q
is feasible, rho<=q. Save q if it improves B before removing >=q. If rho=q the
incumbent is now optimal; if rho<q, the optimum copies survive. Ties with an
unchanged incumbent keep its old valid witness. Pruning removes candidates,
not graph vertices, so a saved witness never loses feasibility.

For infeasible q, rows with midpoint <=q have total length >=M/2. At least half
of each such row is removed. For feasible q use midpoint >=q and the symmetric
half. Thus M_next<=3M/4 in either branch. This proof allows any valid weighted
median, all-zero/flat rows, and length-one active rows. No strictly increasing
row hypothesis is used. Since M_0=n^2 and M is an integer, at most

    floor(log_(4/3)(n^2)) + 1

iterations suffice. At termination the invariant forces B=rho, since no active
optimum copy remains. Its saved feasible witness is a center. A final threshold
call at B returns exactly every center, including tied optima. All-zero and n=1
shortcuts return the same answer without any call.

The decision-to-optimization mechanism is correctly credited to [ESA Lemma 2](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2026.133),
p. 133:6, which is stronger than this self-contained comparison-only version.
No novelty claim should be attached to the generic search. Its proof needs no
real division/floor assumptions from the prior version. Optional pinpoint
correction: replace pp. 133:6-133:7 with p. 133:6.

## 5. Complexity, adjacency reading, and arithmetic

At most n midpoint values are sorted each round. Median selection and bounded
binary pruning cost O(n log(2n)); threshold construction costs the same. The
total extra comparison/search overhead is O(n log^2(2n)). With assumption A,
O(log(2n)) feasibility calls and one final all-centers call give
O(n log^5(2n)). The output list has at most n vertices and is absorbed.

The n^2 candidates are conceptual: the actual search stores O(n) endpoints and
midpoint data. It never constructs a distance table. This is an extra-storage
claim for the reduction only; the oracle's total memory is not reconstructed.

Adjacency-list reading is affordable without an input embedding. A median graph
is isometrically embeddable in a hypercube, as also described in the primary OWR
source. Here is an independent size argument for any n-vertex cube subgraph.
Split a cube vertex set by one coordinate into sizes a<=b. Crossing edges form
a matching and number at most a. Inductively its edges number at most

    (a log_2 a + b log_2 b)/2 + a
      = n log_2 n/2 - n H_2(a/n)/2 + a
      <= n log_2 n/2.

The last inequality follows from H_2(p)>=2p on [0,1/2], by concavity between
(0,0) and (1/2,1). Empty slices and the singleton case are immediate. This proves
m<=n log_2(n)/2 for the promised input class; no embedding needs to be found.
The independent finite suite also checks the equivalent integer inequality
2^(2m)<=n^n on every nonempty vertex subset of Q4, without floating point.

All operations on original real weights can compare k w(u) with j w(v), where
k,j are integers in [0,D]. Initial B, pivots and the final optimum can be stored
symbolically as such a pair. Index/length sums have O(log n) bits (M<=n^2).
There is no arbitrary-real addition, root, floor, or division primitive hidden
in this reduction. Sorting, all searches and graph orderings can be made fully
deterministic.

For exact rational input p_u/q_u of at most B bits per component and positive
denominators, cross multiplication compares k p_u q_v with j p_v q_u. Each has
at most 2B+O(log n) bits. The O(n log^2(2n)) real-comparison count is correct;
the bit cost must additionally pay for reading encodings and integer arithmetic.
No bit-complexity bound independent of B, no floating-point guarantee, and no
full bit-level implementation of BDH is claimed. These qualifications matter
and are already correctly stated by the candidate.

## 6. Reproduction and new independent falsification

The frozen author's program was copied into this review's scratch directory and
run there. Its stdout is byte-for-byte equal to the complete frozen
`CONTROL_RESULTS.json`, not merely its status or summary. The author case digest
is `59bd9887a91c84c1ef9dc47b52dedaccb55804387d6e5872dee795ae8b2ca9fa`.
The old audit's full stored author rerun agrees as complete JSON too. The new
copy is `AUTHOR_CONTROLS_RERUN.json`, SHA-256
`249b4f88d22e21887f0b55ef6da8bffba8374ebc0295119dc18ec0756e88ba69`.

Fresh `independent_controls.py` imports no author functions. It differs by using
Floyd-Warshall distances, direct bounded scans for transformed radii, bisect on
explicit test rows, the highest permissible midpoint median, and the last
feasible vertex. It asserts the optimum-survival invariant both before and after
every pruning step. This tests choices different from the author's lowest
cumulative median/first witness, rather than echoing only one execution trace.

The full deterministic output is `INDEPENDENT_CONTROL_RESULTS.json`:

| Test | Count |
| --- | ---: |
| Connected labelled graphs enumerated through n=5 | 772 |
| Median graphs among them, every profile in {0,1,3}^n | 209 graphs |
| Total graph/profile optimizations | 48,641 |
| Median graph/profile optimizations | 46,854 |
| Complete feasible-set comparisons during search | 201,178 |
| Additional complete boundary feasible-set comparisons | 378,199 |
| Zero-optimum cases | 2,844 |
| Multiple-center cases | 21,733 |
| Larger checked median families | 10 |
| Abstract active row states, arbitrary repeated values/lengths | 44,132 |
| Both-outcome local contraction checks, every valid median | 94,134 |
| Abstract end-to-end optimizations, both extreme valid medians | 243,120 |
| Abstract search iterations with invariants checked | 498,009 |
| Nonempty Q4 subset edge-bound checks | 65,535 |

Larger median families include cubes of dimensions 1 through 6, rectangular
products and glued median pieces; their medianity is independently checked by
triple interval intersections. Rational boundaries include scales beyond 4,096
bits, exact candidate values, adjacent midpoints, negative thresholds, thresholds
above the largest candidate, all-zero and singleton-support profiles. The full
JSON includes 49 explicit boundary/glued-family cases with weights, every raw
radius, optimum, all centers, saved witness and pruning trace.

Graph-case digest:
`f268876c4da8485d5b2febdb1de704d21f088891c93076ee023fbc1b1f07c2da`.
Abstract-case digest:
`d6056423524cf149282f100ddb9152fa0be017c1f612aa1a3c8846ae80a30cd6`.

These tests intentionally materialize quadratic rows/distances and use slower
reference oracles. Neither these artifacts nor the author's reference code are
a general fast implementation or an experimental asymptotic bound. Their role
is exact finite falsification of the new reduction/search and output invariants.

## 7. Disposition and reproducibility

No blocking correction or repair is required for the audited reduction/search.
Retain the exact-operation, finite unit-edge input, promise-of-medianity, imported
oracle, no-fast-implementation and historical-priority qualifications in any
summary. Adding the adjacency-list promise directly to the theorem statement
and tightening the ESA page pinpoint would improve precision but change no
mathematics. The candidate was not edited.

Reproduce the independent suite with `python3 independent_controls.py` and
compare its complete JSON to `INDEPENDENT_CONTROL_RESULTS.json`. Reproduce the
author program from `scratch/author_controls.py`, with this review's scratch
directory as the working directory, and compare its complete stdout to
`AUTHOR_CONTROLS_RERUN.json`. `SHA256SUMS` seals authored artifacts, excluding
itself, source PDFs, extracted source text, renders, caches and the scratch author
copy. Input hashes for those relevant sources/copies are separately recorded.
Hashes establish object identity; no formal or human-peer certification is
claimed.
