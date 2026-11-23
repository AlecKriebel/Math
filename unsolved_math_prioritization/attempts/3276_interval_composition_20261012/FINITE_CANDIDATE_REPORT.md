Editorial note: The complete authored text follows. Only references to undistributed operational artifacts, identities, byte counts, locations and replay commands are replaced by descriptive prose. Mathematical arguments, full audit findings, evidence counts and limits are retained. The original structural bound-eight application is historical and remains unchanged; the new bound-nine consequence is a separate deduction in BOUND_NINE_DEDUCTION.md. Historical candidate-review conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md.

# Candidate evidence: proper-interval propagation through order nine

12 October 2026 UTC. Queue row 1754 / problem 3276 / OPG-1808. Third substantive pass.

## Result and status

The recorded exact search excludes all necessary reduced minimal-counterexample states at orders 3 through 9. Subject to independent acceptance of this packet, the resulting finite theorem is:

Every nonempty tournament of order at most nine, whose arcs use at most three colors, contains a directed cyclic rainbow triangle or has a vertex reaching every other vertex along a monochromatic directed path. The path color may depend on the target.

The general order-nine scope covers all 369 canonical cycle words and all surviving chord assignments. It is not inferred from the periodic pattern. The unrestricted conjecture and all general orders above nine remain unresolved by this work. There is no claim of novelty, current literature status, a proof-assistant certificate, or a formal SAT/DRAT certificate.

## What changed

The previous accepted packet used only actual chord assignments, cyclic-rainbow exclusion, and forbidden predecessor reachability. The present packet adds the credited proper-interval property of an induced-minimal counterexample (Georgakopoulos–Sprüssel, Lemma 2.5), along with sound color-composition propagation.

Each partial state retains mandatory monochromatic reachability assertions. For a proper cyclic interval, possible real chord arcs overapproximate all compatible completions. A color is retained only if its real-arc possibility graph has an interval-local path and adjoining that color's endpoint reachability does not create a forbidden predecessor reach. An empty color set rejects the branch; a singleton forces a path assertion and its transitive consequences. Virtual path assertions are never confused with actual arcs or used as interval-graph edges. Full proof and stale-domain justification are in `FINITE_PROOFS.md`.

## Fresh bounded search

Both mandatory-reachability engines run every general order 3 through 9 and the periodic patterns at 3, 6, and 9. One updates an ancestor-by-descendant product; the other recomputes Warshall closure on the old mandatory relation plus the new assertion. They give identical full counters, not only identical zero answers.

At general order eight: 146 canonical cycle words, 18,583 DFS nodes, 10,552 dead nodes, zero completed states. At general order nine: 369 words, 597,232 DFS nodes, 337,862 dead nodes, 530,534 virtual assertions inserted, 305,738 forced actual arcs, zero completed states. Counts refer to attempted states across the whole DFS; a deduction counted in separate branches is counted each time.

The previous accepted order-eight search had 14,944,184 DFS states. The smaller present tree reflects both stronger constraints and forced-singleton compression; this comparison is not an independently timed speed claim.

## Independent and hostile checks

- The separate literal oracle enumerates every labeled fixed-cycle completion at orders 3, 4, and 5 without partial-state pruning: respectively 27, 2,916, and 1,889,568 completions. This is **not** enumeration of every labeled tournament at order five. It separately tests rainbow, predecessor, and interval conditions by complete adjacency matrices and direct BFS.
- Both candidate engines match that oracle in all 96 combinations of order, raw/canonical cycle-word scope, enabled/disabled conditions, and engine. Literal permutation/rotation minimization independently checks the canonical cycle-word counts 3, 6, and 9.
- Relaxed controls are genuinely satisfiable. For example, at order five, 47,448 raw completions satisfy the interval and cyclic-rainbow restrictions with predecessor reachability allowed; 53,190 satisfy predecessor nonreachability alone with interval and cyclic-rainbow restrictions disabled. An always-zero or indiscriminately overpruned search fails these checks.
- The direct-BFS harness checks 131,200 actual arc proposals, accepting 105,041 and rejecting 26,159; it verifies accepted reachability matrices and immutability on rejection. It additionally checks 128,000 virtual-link proposals, including positive-length diagonal cycles, against direct BFS.
- The harness performs 69,202 completion-preservation checks. Every sampled fully assigned model satisfying a selected relaxed scope must survive propagation from a random subset of its actual chords plus only virtual assertions already true in that model. Forced arcs, forced reachabilities, and the retained branch containing that model are checked against the complete model. Nonzero full-model controls occur for each scope that can be satisfied; the joint target-forbidden scopes are explicitly not presented as nonvacuous positive controls.
- Eight actual candidate-code mutations are detected: wrong predecessor, corrupted triangle test, omitted ancestor endpoint, always-false interval possibilities, always-true interval possibilities, wrong forced reach color, omitted sixth chord branch, and treating the whole cycle as a proper interval.
- Sixteen malformed or unsupported CLI scopes fail explicitly. Eight corrupt-result mutations are rejected, including missing general coverage, inflated bound, periodic-to-general laundering, omitted words, nonzero completions, and weakened controls.

A preliminary audit attempt stalled on an intentionally corrupted closure update, whose propagation no longer made progress. That attempt was stopped and is not a successful replay. The hostile checks were reordered to test closure invariants before recursive mutant searches. A timeout guard applies only to hostile mutant processes; hitting it fails the audit and supplies no exclusion evidence. The actual candidate searches have no time or node cap.

Full fresh replays passed under ordinary Python, `-O`, and `-OO`; all three successful, source-bound execution receipts are included in the frozen packet. Each recorded receipt refers to a full fresh replay, including source mutations and explicit gates. Integrity verification separately detects six changed packet files; verification alone does not rerun the searches.

## Dependencies and reproducibility

The mathematical source is [Georgakopoulos–Sprüssel, On 3-coloured tournaments, arXiv:0904.1967v2](https://arxiv.org/pdf/0904.1967v2), Lemma 2.1 (crediting Shen) and Lemma 2.5. The exact primary PDF and extracted text were locally re-inspected, and their hashes and sizes are in `the original operational record`; neither source document is redistributed. The reduction and short interval proof are reconstructed in our own words.

This candidate's completeness argument and full bounded executions are needed for the order-nine conclusion. The independent raw oracle stops at fixed-cycle order five; the harness samples partial states rather than exhaustively enumerating them. These limitations are not hidden by the full-scope zero counts.

The earlier accepted finite packet remains unchanged with manifest SHA-256 `[verified undistributed artifact identity]`. It still supports its earlier through-eight and periodic-nine claims. No queue, remote, or publication writes were performed in this computational lane.
