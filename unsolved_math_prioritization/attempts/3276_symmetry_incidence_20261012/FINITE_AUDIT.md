Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The structural proof retains its original through-nine premise; the separately accepted through-ten application appears in BOUND_TEN_DEDUCTION.md. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Independent audit: actual-incidence tournament search

12 October 2026 UTC. Queue row 1754 / problem 3276 / OPG-1808. Fourth substantive pass.

## Decision

**ACCEPT, bounded only.** The exact frozen candidate passes independent source-hypothesis, proof, implementation, complete bounded-execution and hostile-control review. Both full general-ten closure engines completed with matching counters; the normal/-O/-OO targeted suites pass with identical substantive results. The unrestricted conjecture remains unresolved by this work.

Candidate manifest SHA-256: `[verified undistributed artifact identity]`. Candidate search SHA-256: `[verified undistributed artifact identity]`, [verified original byte count omitted]. Candidate identity and the complete exact inventory are recorded in the original operational record.

The accepted finite conclusion is: every nonempty tournament on at most ten vertices, with arcs colored from a palette of at most three colors, either contains a directed cyclic rainbow triangle or has an outgoing vertex reaching every other vertex by a monochromatic directed path. The color can depend on the destination. A transitive rainbow triple is allowed.

The prior accepted general bound is nine. Its separate interval-search manifest `[verified undistributed artifact identity]` and independent audit remain unchanged. Periodic controls remain exactly lengths 3, 6 and 9. General orders above ten, periodic twelve, all-size strict-periodic exclusion and the unrestricted conjecture are not established. There is no novelty, current-literature-status, human-review, proof-assistant or formal unsatisfiability-certificate claim.

## Proof and source review

FINITE_PROOF_REVIEW.md reconstructs every required pruning invariant and the finite completeness argument. The auditor independently read the exact general-conjecture hypotheses in the recovered Georgakopoulos–Sprüssel primary source, checked the PDF/text hashes, and freshly extracted PDF pages 3–5. Proposition 2.4 and Theorem 3.1 apply to an induced-minimal counterexample to Conjecture 1.2, rather than only the special no-three-incident-colors theorem discussed elsewhere in the paper. The Hamilton cycle makes incoming and outgoing edge sets nonempty; Proposition 2.4 consequently forces at least two colors in each direction. Theorem 3.1 forces all three incident colors.

The new implementation uses actual fixed arcs and actual pair domains only. It removes a pair's entire possible contribution before testing a selected direction/color, checks both endpoints, and restores only the retained domain. A real full model continues to witness all required categories, so its selected value cannot be removed. The union predicate is intentionally weaker than simultaneous realizability; surviving alternatives are never advertised as a satisfying assignment. Virtual paths are excluded from incident categories, triangle edges and actual interval possibility graphs.

The full source diff from the accepted interval engine was inspected. Six-way actual branching, positive-length closure, predecessor tests, strict proper-interval locality, color normalization, cycle rotation and the finite-restart measure remain sound. Actual forced arcs and virtual path assertions remain separate. The stale interval graph during a sweep is a safe overapproximation. Complete zero search at every order, combined with the induced-minimal reduction, yields the finite tournament result.

The source results remain credited dependencies. This audit does not independently recertify every proof in the paper or infer the current state of the literature.

## Independent finite and positive controls

The independent reference extends the already accepted auditor's complete-matrix/BFS implementation. The new incidence predicate is evaluated directly on complete adjacency, with no domain pruning. The new domain harness was written separately from both candidate incidence harnesses and uses Boolean support recomputation rather than the candidate count accumulator.

- All 46,879 labeled three-colored oriented tournaments of orders 1–4 are checked directly; none violates the target.
- All 1,892,511 labeled fixed-cycle completions across orders 3–5 are enumerated without partial pruning. This is not all labeled tournaments at order five. Both candidate engines are checked on every raw/canonical and four-condition enabled/disabled combination, giving 192 comparisons.
- The order-five raw incidence-only count is 240; its canonical count is eight. Incidence-disabled positive controls include 47,448 triangle-plus-interval completions and 53,190 predecessor-only completions. Positive relaxed models prevent an always-zero answer or unjustified universal rejection from passing.
- The independent inherited BFS harness tests 551,040 actual-arc proposals and 112,000 virtual links, including positive cycles and rejection nonmutation. It checks 35,034 complete-model preservation cases and rejects 6,907 complete models lacking an interval-local path. Incidence is disabled in these interval-isolation controls; the separate incidence controls below cover the new rule.
- Literal group minimization checks all six color permutations and all rotations for 88,560 raw cycle words of lengths 3–10. At length ten, all 59,049 words yield exactly 1,002 representatives.
- Every directed colored star with zero through five edges is checked against the complete incidence predicate: 9,331 cases. Exact one-vertex dynamic programming explores 14,000 arbitrary star-domain boxes, with 10,943 realizable boxes and 33,097 supported selected values. It chooses one value per actual edge, explicitly respecting incompatible direction/color alternatives on that edge.
- The independently recomputed endpoint filter agrees on 19,500 arbitrary partial-actual domain boxes through order fifteen, including 5,039 rejections and 2,355 surviving boxes with genuine pruning. Across the latter it records 10,678 removed options. Arbitrary virtual relations do not affect the output, domains never grow, and a second filter call is idempotent. These are local filter tests, not complete tournament-search exclusions at orders eleven through fifteen.
- A further 900 independently generated incidence-satisfying tournaments of orders 5–10 supply 7,200 random domain boxes containing the known model. Every actual model value survives. The generator uses balanced cyclic orientations and random colors with actual-incidence rejection sampling; it does not uniformly enumerate tournaments. It intentionally tests the incidence preservation theorem independently of the other constraints.
- With the new incidence rule disabled, both engines exactly reproduce the old accepted general-nine result, including 369 words, 597,232 states, 337,862 dead states, 530,534 virtual additions, 305,738 forced actual arcs and zero completions. The original old engine is freshly executed for the comparison.

## Full execution scopes

The normal/-O/-OO independent targeted suites each execute the entire general 3–9 scope, periodic lengths 3/6/9, all independent references, both old-nine regression engines, domain/BFS controls, actual source mutations and CLI gates. Their substantive results must match exactly. They do not claim general-ten execution inside those receipts.

Two separate source-locked C++ executions cover the complete general-ten scope, one incremental ancestor-product engine and one fresh Warshall engine. The code bytes were locked before launch and match the final frozen candidate. The final receipt binds the completed executions to that candidate manifest. This collection method is not misdescribed as three expensive Python-mode ten replays; The original standalone replay program provides equivalent two-engine reproduction in the original packet; it is not distributed here.

Both larger engines report 1,002 words, two cycle-initialization rejections, 9,944,675 DFS states, 5,547,193 dead states, 9,509,336 virtual additions, 10,626,003 forced actual arcs and zero completions. All general orders 3–10, rather than only the largest order, were completely executed. Periodic words and explicit selected-word scopes cannot substitute for general coverage.

The author’s entire fixed small-scope/control bundle was also freshly replayed in normal Python, covering both general 3–9 engines, periodic 3/6/9, its 192 literal-oracle comparisons, both original harnesses, eleven actual source mutations and sixteen CLI gates. Every recorded field matched the frozen candidate, and candidate hashes matched before and after. That receipt explicitly omits general ten.

Both full engines share the surrounding search code. The literal complete-model oracle stops at fixed-cycle order five, and the larger domain/model tests are finite samples. The reviewed all-order preservation proof and actual complete bounded executions are essential to the conclusion; the sampled controls alone do not prove it.

## Hostile controls and optimization

Each targeted suite executes eighteen actual source-code mutations covering predecessor direction, cyclic-triangle distinctness, a lost closure ancestor, omitted sixth branch, omitted third cycle color, always-false or always-true interval paths, interval-mask escape, virtual paths as interval edges, wrong forced color, an improper full interval, virtual paths as triangle edges, disabled incidence, an overstrong incoming-color requirement, omitted selected-value support, retained incompatible pair alternatives, a reversed endpoint category, and virtual paths used as incident colors.

A mutation is detected only by an explicit executed oracle or invariant failure. Any hostile-process timeout fails the audit rather than counting as detection. The suites also reject seventeen malformed/unsupported candidate or oracle CLI scopes and twelve corrupt-result scenarios. Additional final-ten semantic mutations reject omitted or duplicate engines, a nonzero answer, periodic or selected-word laundering, missing incidence, omitted word coverage and an inflated order.

Normal Python, `-O` and `-OO` use explicit failure gates; no Python assertion supplies a needed check. The receipts bind the optimization mode and runner bytes, so recorded-result validation cannot silently be substituted for the executed targeted suite.

## Incomplete work and integrity boundary

The author's previous no-incidence general-ten feasibility run, old periodic-twelve feasibility run and new incidence periodic-twelve run were interrupted without conclusions. Preliminary control-development attempts also failed their nonvacuity gates and were replaced by the honestly scoped final controls. These are recorded as incomplete or failed development checks, never exclusion evidence.

The final audit manifest seals authored reports, code, source identities and numerical receipts. An external pin seals the manifest. Post-freeze normal/-O/-OO verifier receipts remain outside the frozen packet; they exercise exact-inventory, mathematical-scope and copied-artifact corruption gates. Candidate and prior accepted packets are rechecked before and after audit execution.

No remote write, queue edit, publication action or additional research pass belongs to this audit. The deliverable contains no copied source documents, dataset contents, private personal data or private coordination material. Full artifact bytes are retained for rollback recovery; hashes do not substitute for those bytes or for actual computations.
