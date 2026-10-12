Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The structural proof retains its original through-nine premise; the separately accepted through-ten application appears in BOUND_TEN_DEDUCTION.md. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Candidate evidence: incidence-domain propagation through order ten

12 October 2026 UTC. Queue row 1754 / problem 3276 / OPG-1808. Fourth confirmed pass.

## Result and status

The completed exact reduced searches recorded in this packet exclude all necessary induced-minimal-counterexample states at orders three through ten. Subject to independent acceptance of this packet, the finite conclusion is:

Every nonempty tournament of order at most ten, with arcs colored from a palette of at most three colors, contains a directed cyclic rainbow triangle or has a vertex reaching every other vertex by a monochromatic directed path. The path color can depend on the target.

The order-ten run covers all 1,002 canonical cycle words, representing all 59,049 raw three-color cycle words under color permutation and rotation. It is a general-order result, not an inference from a strict periodic word. The unrestricted conjecture, every general order above ten, and any all-size strict-periodic exclusion remain unresolved by this work. No novelty, current-literature-status, proof-assistant, or formal SAT/DRAT-certificate claim is made.

## Added constraint and soundness

The earlier accepted interval engine retained actual arc assignments, avoided actual cyclic rainbow triangles and forbidden predecessor reachability, and propagated necessary proper-interval paths. The new rule uses the credited source requirements that each vertex has all three colors incident and at least two incoming and two outgoing colors.

For every actual chord domain, it temporarily tests each value against the possible incident color sets at both endpoints. It removes a value only if fixing it leaves an endpoint without all three possible incident colors, two possible incoming colors, or two possible outgoing colors. Iterating these deletions is sound: any compatible completion's actual values continue to witness every required color. This is a necessary relaxation, not a claim that independent color possibilities can all be realized simultaneously. Actual-edge domain sets supply incidence and interval possibilities; virtual path assertions supply neither actual incident colors nor actual rainbow edges.

The full reduction, soundness, finite termination, symmetry argument, and conversion of the reduced exclusion to the finite tournament theorem are in `FINITE_PROOFS.md`. The primary dependencies are Georgakopoulos–Sprüssel, *On 3-coloured tournaments*, arXiv:0904.1967v2, Lemma 2.1 (crediting Shen), Lemma 2.5, Proposition 2.4, and Theorem 3.1. Source hashes and inspection history are recorded without redistributing the PDF or extracted text.

## Exact bounded counters

Both closure engines run every general order three through ten and strict periodic lengths three, six, and nine. One inserts an ancestor-by-descendant product; the other runs Warshall closure after insertion. They must agree on all counters, not only zero answers.

- General order eight: 146 canonical words, 7,358 DFS states, 4,152 dead states, zero completions.
- General order nine: 369 canonical words, 173,163 DFS states, 95,923 dead states, 168,840 virtual path insertions, 185,994 forced actual arcs, zero completions.
- General order ten: 1,002 canonical words, 9,944,675 DFS states, 5,547,193 dead states, 9,509,336 virtual path insertions, 10,626,003 forced actual arcs, zero completions.

Counts are totals over attempted branches; repeated deductions in different branches are counted repeatedly. The accepted earlier interval packet used 597,232 order-nine states. The new order-nine tree has 173,163 states. This is a search-tree comparison, not an independently controlled speed claim. The all-order incidence rule is credited necessary structure; this packet's computational extension is finite.

## Independent positive and hostile checks

- The literal complete-completion oracle independently enumerates every labeled fixed-cycle completion at orders three, four, and five: 27, 2,916, and 1,889,568 respectively. This does not enumerate every labeled tournament at order five. Direct complete-adjacency graph searches test the constraints with no partial-state pruning.
- All 192 combinations of raw/canonical cycle-word scope, four enabled/disabled conditions, three orders, and two candidate engines match that oracle. At order five the incidence-only control has 240 raw completions and eight canonical completions. With incidence disabled, earlier positive controls persist: 47,448 raw interval-and-rainbow completions allowing predecessor reachability, and 53,190 raw predecessor-only completions.
- The independent literal symmetry oracle tests every raw word through length ten against all six color permutations and all rotations, confirming 1,002 representatives at length ten.
- The inherited-and-extended direct-BFS harness checks 131,200 actual-arc proposals (105,041 accepted and 26,159 rejected), 128,000 virtual-link proposals, and 69,264 propagation preservation checks against complete models. Jointly impossible or unsampled scopes are not presented as positive controls. Among the sampled small-order models, six incidence-only models are positive; the dedicated next check supplies much broader nonvacuous incidence coverage.
- The independent incidence harness tests all 1,296 directed colored four-edge stars, of which 144 satisfy the predicate. It then uses 3,000 known incidence-satisfying tournaments of orders five through ten and 12,000 arbitrary actual-edge domain boxes containing them. Every known model survives, every surviving domain remains a subset of the input, and a second sweep is idempotent. It observes 30,174 deleted options and 14,264 newly singleton domains, so the test exercises actual pruning. An impossible all-red box is rejected.
- Eleven actual candidate-source mutations are detected: wrong predecessor; wrong triangle predicate; omitted ancestor endpoint; always-false and always-true possible interval reach; wrong forced color; missing sixth chord branch; treating the entire cycle as a proper interval; ignoring incidence; requiring three incoming colors; and omitting the selected candidate's incidence contribution.
- Sixteen malformed or unsupported CLI scopes fail. Eleven result mutations fail, including omitted order coverage, inflated bound, periodic laundering, absent incidence, omitted words, nonzero completions, oracle mismatches, weak preservation controls, and a false orbit count.

The two closure engines share the surrounding candidate search. The literal completion oracle stops at fixed-cycle order five; the larger-order incidence harness samples known models and is not exhaustive. The all-order pruning proofs and complete bounded executions, rather than those tests alone, support the candidate order-ten result.

## Execution and incomplete exploratory scopes

`the original operational record` records exactly what was executed, with source/result bindings. The full bounded C++ scopes were actually executed with both closure engines. Their results were collected alongside one full small-scope control pass including genuine source mutations. Normal, `-O`, and `-OO` validation receipts exercise the explicit recorded-result gates; they are not mislabeled as three complete expensive order-ten replays. The original replay program provided full fresh reproduction; executable programs and commands are not distributed in this prose edition.

Separate feasibility runs of the previous interval engine at general ten and periodic twelve, and the new incidence engine at periodic twelve, were interrupted without a result. They are explicitly marked incomplete in `the original operational record`. They contribute no exclusion evidence. No periodic-twelve or other larger bound is claimed. These interrupted genuine exploratory scopes are distinct from timeouts guarding deliberately corrupted source mutations; a hostile-control timeout is a failure, never mathematical exclusion evidence.

The prior accepted interval packet remains unchanged at manifest SHA-256 `[verified undistributed artifact identity]`. No repository, queue, or publication state was changed in this lane. A final external manifest pin fixes this candidate for independent review.
