Editorial note: The complete authored text follows. Only references to undistributed operational artifacts, identities, byte counts, locations and replay commands are replaced by descriptive prose. Mathematical arguments, full audit findings, evidence counts and limits are retained. The original structural bound-eight application is historical and remains unchanged; the new bound-nine consequence is a separate deduction in BOUND_NINE_DEDUCTION.md. Historical candidate-review conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md.

# Independent audit: interval-propagation tournament search

12 October 2026 UTC. Row 1754 / problem 3276. Third substantive pass.

## Decision

**ACCEPT, bounded only.** The exact frozen candidate passes the independent proof, code, replay, optimization, and hostile-control audit. The unrestricted conjecture remains unresolved by this work.

Candidate manifest: SHA-256 `[verified undistributed artifact identity]`, [verified original byte count omitted], eleven exact-hash files. Search source: SHA-256 `[verified undistributed artifact identity]`, [verified original byte count omitted].

The reviewed finite conclusion is: every nonempty tournament of order at most nine, with arcs colored using at most three colors, contains a directed cyclic rainbow triangle or has a vertex from which every other vertex is reachable by a monochromatic directed path. The color may depend on the destination. Transitive rainbow triples are allowed. The universal vertex is an outgoing source.

## Prior and current scope

The earlier accepted packet, manifest `[verified undistributed artifact identity]`, established the general target through order eight and excluded the single three-periodic cycle-color pattern at lengths 3, 6, and 9. That packet and its recovery acceptance remain separate and unchanged.

The new claim adds **general order nine**, covering all 369 rotation/global-color cycle-word orbits. The periodic scope remains exactly 3, 6, and 9; it is not a new periodic-length result. General order ten and above, periodic length twelve and above, and the unrestricted target are not excluded here. An author's separate order-ten single-word warm-up is not used as evidence for any accepted scope.

## Mathematical review

The auditor independently read Conjecture 1.2 and Lemmas 2.1 and 2.5 in Georgakopoulos and Sprüssel, [On 3-coloured tournaments, arXiv:0904.1967v2](https://arxiv.org/pdf/0904.1967v2), including the section's exact hypotheses and the warning about interval-local colors. The PDF/text hashes and their correspondence were checked, and page 4 was separately extracted from the PDF. No copied source text is included.

The section's assumptions concern the general induced-minimal counterexample, not only the later at-most-two-incident-colors theorem. The interval lemma says that the first vertex of each proper forward interval dominates its last within that induced interval. Its proof follows because every proper induced subtournament must have an outgoing monochromatic source, while every other vertex in the interval has its forbidden predecessor there. This does not preserve an arbitrary color of a path from the whole tournament.

The independent reconstruction in FINITE_PROOF_REVIEW.md proves the candidate's needed invariant: each actual assignment and each mandatory colored reachability is present in every compatible minimal-counterexample completion. All six actual values of a chord are tested. Their surviving domains overapproximate every compatible model, so the actual-edge possibility graph restricted to an interval contains every genuine interval path. A color is rejected only if this local graph lacks the path or if adjoining the required colored reach creates forbidden predecessor reachability. Every compatible model supplies a retained color; a singleton therefore forces a true colored path assertion.

Virtual paths are stored separately from actual tournament arcs. They are neither used in rainbow-triangle tests nor inserted directly as interval-graph edges. Older domains retained during a pass are still supersets and can only weaken pruning. Forced actual assignments and strict relation growth guarantee termination. Positive-length closure retains diagonal cycles without introducing reflexive paths by convention. Uniform color renaming and cyclic rotation preserve the exact conditions; no reflection or arbitrary vertex permutation is used.

Orders one and two are immediate. An induced-minimal counterexample supplies the spanning obstruction cycle credited to Shen, and the proper-interval lemma then applies. Thus complete zero searches for every general cycle-word orbit at orders three through nine suffice for the finite theorem. This reviewed argument is not an all-size exclusion, a proof-assistant theorem, or a SAT/DRAT certificate.

## Fresh independent computations

The audit's reference is separate from the candidate's own oracle. It uses complete adjacency matrices and direct per-color BFS, with interval restriction implemented by an induced matrix. Its tournament primitives derive from the previous independent audit; interval checking, preservation tests, and new hostile fixtures were added independently for this pass.

1. Raw enumeration checks all 46,879 labeled oriented three-colored tournaments of orders one through four. There are no target counterexamples.
2. Literal fixed-cycle enumeration checks 1,892,511 complete assignments over orders three through five, with no partial pruning. Both candidate engines match all 96 raw/canonical, enabled/disabled triangle/predecessor/interval comparisons. This is not enumeration of every labeled tournament at order five.
3. At order five, raw counts for no restrictions, triangle only, predecessor only, both, interval only, triangle-plus-interval, predecessor-plus-interval, and all three are respectively 1,889,568; 743,718; 53,190; 0; 58,158; 47,448; 0; 0. The positive relaxed controls detect an always-zero or indiscriminately overpruned solver.
4. A separate direct-BFS harness checks 551,040 actual-arc proposals and 112,000 virtual-link proposals through order ten, comparing all positive-length closure entries and requiring rejected operations to leave the state unchanged. Explicit fixtures separate virtual paths from actual rainbow arcs and prevent paths from leaving an interval.
5. The harness checks 35,034 sampled complete-model preservation cases through order seven. Every sampled valid model survives propagation from partial actual chords and true global virtual links; forced arcs and paths, and the branch retaining that model, agree with the complete assignment. Each potentially satisfiable relaxed scope has positive controls. Another 6,907 complete assignments failing an interval are required to be rejected, preventing global paths from being mistaken for local witnesses.
6. Literal minimization under all six color permutations and every rotation checks all 29,511 color words of lengths three through nine. Orbit counts are 3, 6, 9, 26, 53, 146, and 369.
7. The auditor freshly reruns the original accepted order-eight search with both original engines: 146 words, 14,944,184 DFS states, 5,728,965 dead states, zero completions. The new search with interval pruning disabled also matches across both engines: 10,201,431 states, 5,728,965 dead states, 4,670,095 forced actual arcs, no virtual additions, and zero completions. The changed state count is consistent with singleton compression; it is not a timed performance claim.
8. The independent suite runs the current full general scope three through nine and periodic 3/6/9 with both engines. At general order nine, both give 369 words, 597,232 states, 337,862 dead states, 530,534 virtual additions, 305,738 forced actual arcs, and zero completions.

The candidate's exact frozen packet was additionally replayed through its own complete replay program, after three-mode seal verification and before another three-mode seal verification. It passed the same larger scope, its 96 oracle comparisons, eight actual source mutations, and sixteen CLI gates. The independent raw oracle stops at fixed-cycle order five and partial-state tests are sampled; larger-order acceptance combines the inspected completeness argument, exact full replay, independent tests, and hostile controls.

## Hostile and optimization gates

The independent full audit passes in normal Python, `-O`, and `-OO`, with identical substantive results. Each mode repeats the full general scope, independent raw oracles, old and new order-eight regressions, sampled-model checks, and actual-source mutations. The optimized receipts explicitly record their interpreter levels and the exact audit-runner hash.

Twelve actual candidate source mutations are detected by concrete failures: wrong predecessor, corrupt triangle distinctness, missing ancestor endpoint, omitted sixth branch, omitted third color, always-false interval paths, always-true interval paths, omitted interval mask, treating virtual reachability as actual possible edges, wrong singleton color, imposing the whole cycle as a proper interval, and treating virtual paths as actual rainbow arcs. Seventeen unsupported CLI scopes and eight corrupt-result scenarios fail explicit gates. No Python assert is used.

A preliminary audit run was canceled before completion while the runner was being tightened to test primitive invariants before recursive hostile mutants. It is not an accepted run and supplies no exclusion evidence. The final hostile-run timeout is a failure of the audit, never a detected mutation or a mathematical exclusion. All successful mutation detections in the accepted evidence are explicit oracle or invariant failures; none is a timeout.

## Reproduction and integrity

FINITE_AUDIT_REPRODUCTION.md preserves the original replay and seal-verification description; executable commands and programs are not distributed. The audit manifest fixes the report, independent test sources, candidate identity, full numerical receipts, and pre/post candidate seal checks. The external pin fixes that manifest. The audit verifier rejects altered mathematical scope, missing finite coverage, nonzero results, lost relaxed controls or regressions, and corrupted/missing/extra artifacts. Post-freeze verification is stored outside the frozen packet.

No remote writes, queue edits, publication action, or additional research pass was performed by this audit. The mathematical status is bounded progress only. There is no novelty or current-literature-status claim.
