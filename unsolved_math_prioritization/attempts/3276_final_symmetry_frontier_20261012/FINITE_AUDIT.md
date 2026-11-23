Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The final structural theorem is independent of a finite computer bound. Earlier through-nine and through-ten results retain their historical scope in unchanged companion editions. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Independent audit: exact full twisted rotational orbits

12 October 2026 UTC. Row 1754 / problem 3276 / OPG-1808. Computational lane of the fifth and final substantive pass.

## Decision and strict scope

**ACCEPT, bounded only, for the final manifest identified in the original operational record.** The frozen author packet passes the independent encoding, pruning, completeness, source-hypothesis, literal-model, positive-model, fresh-execution, mutation, and reconstruction checks listed below. The complete FINITE_PROOF_REVIEW.md supplies the audit's mathematical argument, rather than referring to absent working notes.

Accepted candidate manifest SHA-256: [verified undistributed artifact identity] ([verified original byte count omitted]). The search source remains [verified undistributed artifact identity] ([verified original byte count omitted]).

The accepted finite class has vertices Z/nZ; every arc is preserved by the global action x -> x+1, color c -> c+1 modulo three; the distinguished actual first arc is 0 -> 1 in color zero; cyclic rainbow triangles are forbidden; and no vertex has a monochromatic path to its cyclic predecessor. Candidate and auditor complete exactly orders 3,9,15,21,27,45,81 and obtain zero at each.

This is full colored-tournament symmetry, not an assumption merely on one cycle's periodic word. No new general tournament bound is proved: the previously accepted general bound remains ten. Arbitrary periodic length twelve, arbitrary all-size three-periodic cycles, and the unrestricted target remain unresolved by these computations. The audit does not certify the separate structural lane's all-order theorem. It claims neither priority nor the current status of the literature, and is not a human review, proof-assistant proof, or formal unsatisfiability certificate.

Excluding symmetric induced-minimal counterexamples does not by itself settle the target for every symmetric larger tournament: induced minimization may destroy symmetry. Rainbow-free symmetric tournaments are nonempty and plentiful at order nine; our positive controls explicitly retain them.

## Mathematical and source review

The audit independently read the recovered Georgakopoulos–Sprüssel primary source, *On 3-coloured tournaments*, arXiv:0904.1967v2, https://arxiv.org/pdf/0904.1967v2 . The source PDF and text match the recorded public-source hashes and sizes. Conjecture 1.2, the definition of outgoing monochromatic domination, Lemma 2.1 with its proof, and the general-minimal-counterexample context after Corollary 2.2 were read directly. Lemma 2.1 credits Shen and concerns minimal counterexamples to the general conjecture, not only the later incident-two-colors theorem. Uniqueness refers to the failed-predecessor cycle, not all Hamilton cycles. No source document or text is redistributed.

The orbit encoding is bijective, has no duplicate pair or variable, and includes all six orientation/color choices for every unordered-pair orbit. Color in a reversed orbit uses the specified representative base, not the tail. The fixed first arc is stated as a condition justified by distinguished-cycle labeling and global color naming. No unjustified factor-of-six quotient is used.

Partial assignments contain complete rotational orbits of actual arcs. This makes the candidate's anchored-at-zero cyclic-triangle test and zero-to-predecessor single-color graph searches equivalent to checking all vertices. Both reject only monotone obstructions that cannot disappear upon completion. Omitting all other induced-minimal requirements enlarges the searched class, so a completed zero run still excludes the intended minimal class. The MRV choice is only an ordering heuristic; complete assignment and restoration preserve all solutions without duplicates.

## Independent literal and positive controls

The auditor wrote a separate Python encoder that constructs unordered-pair orbits by applying the cyclic group action, without the candidate's distance formula. It refuses duplicate pair writes and checks every shifted arc. Literal cyclic triangles use all vertex triples, and monochromatic reachability is computed for every source by iterative set unions. This implementation imports no candidate implementation or author oracle.

All 1,302 complete full-action models at orders three and nine are enumerated literally, without pruning. The resulting matrices are pairwise distinct at each order. The counts under neither predicate, rainbow exclusion only, predecessor nonreachability only, and both are:

- n=3: 6,0,3,0; fixed first arc: 1,0,1,0
- n=9: 1296,432,54,0; fixed first arc: 216,72,18,0

Every subset of each complete model's orbits is independently checked under all four predicate combinations. There are 82,992 such completion/subset/rule cases, including 28,530 positive-completion preservation cases. Repeated partial graphs from different completions are counted as preservation cases, not falsely described as distinct models.

Separately, every one of the 2,408 distinct partial vectors at orders three and nine is passed to a compiled candidate bridge. Its entire matrix and all four rejection modes agree with the independent oracle: 9,632 rule comparisons, plus 16 exact raw/fixed complete-count comparisons. The all-unassigned partial graph and every orientation/color alternative are included.

All 432 order-nine rainbow-free full-action models have every vertex as an outgoing universal monochromatic source. The auditor also reconstructs and verifies every byte of the author's three fixture matrices and all listed properties. In particular, (0,2,2,2) is rainbow-free with all nine sources but no single spanning strongly connected color; (0,1,0,0) has predecessor nonreachability and no sources but 18 cyclic rainbow triangles; (0) is the rainbow three-cycle. These prevent an always-zero oracle, a missing rainbow condition, source/sink confusion, or borrowing the stronger color-preserving-transitivity conclusion.

## Completed finite executions and modes

Normal Python, -O, and -OO each freshly execute the auditor's full literal enumeration, all partial-vector comparisons, all source mutations, and all seven finite zero scopes. These are actual separate executions, not three validations of one recorded run. Explicit exceptions supply every failure gate.

The auditor's second complete search uses fixed numerical orbit order, direct group-action expansion, all-triple inspection, and all-source monochromatic reachability. Its zero-scope node counts at 3,9,15,21,27,45,81 are respectively 0,5,7,11,17,29,53; its tested proposals are 0,30,42,66,102,174,318. The initial rainbow triangle rejects n=3 before DFS. These independent counters need not match the candidate's MRV counters.

The entire author's verification script is also freshly replayed in all three Python modes, compiling C++ at -O2 each time. This covers its complete candidate scopes 3,9,15,21,27,45,81; its own separate C++ oracle scopes 15,21,27,45; its n=3,9 literal checks; all examples; nine source mutations; fourteen malformed CLI rejections; and twelve malformed internal-input rejections. Every recorded result matches the frozen original receipt. Candidate MRV node counts are 0,5,1,1,11,19,33. At order 27, it performs eleven nodes and 589 tests.

The candidate's built-in independent C++ search and candidate search share the conceptual MRV ordering, though they have separate implementations and graph predicates. The auditor's group-action Python search supplies a further independent fixed-order route through the same exact finite class. None of these bounded runs establishes an all-order conclusion.

## Hostile controls

Each Python mode compiles and runs twelve actual candidate-source mutations: disable triangle rejection; disable predecessor rejection; test the successor; mix path colors; omit rotated arcs; use the reversed arc tail as the representative color base; omit the last orbit; skip initial rejection; test transitive triples instead of cyclic triples; omit color-two paths; discard the sixth branch; or discard the first branch.

Every mutated binary compiles, terminates normally, and produces a concrete independent matrix, predicate, or exact-count mismatch. The Python validator catches that explicit failure and records it. No compilation error, timeout, crash, empty output, or inability to execute counts as successful detection. The final source is unchanged by these tests because mutations occur only in temporary copies.

Additional scope controls reject general-bound inflation, a claim about arbitrary periodic twelve, an all-order computational claim, a claim settling all symmetric tournaments, omission of the independently completed order 81, dropping the fixed cycle or rainbow condition, and declaring the target resolved. Inventory controls reject modified proof, report, source, numerical receipt, scope, manifest, missing artifact, and extra artifact.

## Integrity correction and preservation

An initial candidate pin was not accepted. Its corruption-test helper copied read-only frozen file modes and then failed with PermissionError when mutating the copied proof. Mathematical runs and source-mutant checks had already passed; that infrastructure exception was not counted as a successful integrity check. The author repaired only temporary-copy permissions and issued a new exact manifest. The superseded identity and pre-freeze receipts, and an explicit development-event record, remain in this audit. Final acceptance uses the repaired candidate and successful post-freeze checks. The original operational record records that only the original checker changed; every mathematical source, example, proof and substantive receipt is byte-identical. The earlier fresh mathematical executions therefore bind to the final source bytes without pretending that the permission-only correction reran those mathematical computations.

Full authored audit prose, code, source identities, fixtures-through-the-author-packet, and exact mode receipts are retained. The external audit pin seals every payload; final self-tests run after read-only freeze. A full-byte archive preserves both the final candidate and this audit with their pins. Bytes are stored, read back, actually extracted into a fresh directory, and verified against the same external pins. Reconstruction and integrity checks do not replace the proof review or fresh computations.

No remote repository write, queue edit, additional research pass, copied primary-source text, dataset content, private personal data, or private coordination material is included in this work.
