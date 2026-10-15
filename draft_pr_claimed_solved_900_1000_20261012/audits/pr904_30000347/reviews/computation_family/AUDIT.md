# PR 904 / problem 30000347: independent computational adversarial audit

## 2026-10-13T03:14:04.793967+00:00: independent plan checkpoint

Completion estimate: 10% of this computational audit. Only `frozen_packet/PROOF.md` has been inspected at this point; no prior audit or submitted implementation has been read. Claim under test: the constructed simple tripartite-spoke graph has all three original terminal distances 3, its minimum edge blocker equals the vertex-cover number of H, and subdividing every Q-edge twice gives tau(H)=|E(Q)|+tau(Q). The finite-connectivity extension should retain these optima and admit cover-spoke deletions giving exactly distance 4.

Independent falsification design:

1. Use independently written adjacency-set BFS and full deletion-subset enumeration for small supplied tripartitions, including isolates, single-edge-type counterexamples outside the stated assumptions, and deletion sets containing arbitrary middle edges. For every feasible deletion set, enumerate every endpoint choice for deleted middle edges where practical and verify the no-larger cover conversion.
2. Use a separate integer set-cover dynamic recursion built from BFS-enumerated geodesics to check exact blocking optima, and brute vertex-cover enumeration to check both equalities on all nonempty labelled Q with up to four vertices. Check empty Q handling and very large binary budgets without budget-dependent graph expansion.
3. Add disjoint terminal backup paths, check original geodesics and arbitrary backup-edge deletion, and test that every original cover deletion produces finite terminal distance exactly four, including graphs whose remaining nonterminal vertices are disconnected.
4. Read and copy the submitted verification suites only after this independent design. Run them on disposable working copies with command/output capture. Test optimized-Python/assert erasure separately; a suite that silently passes after losing required checks is not equivalent evidence.
5. Inspect manifest and certificate boundaries, deliberately mutate artifact bytes, proof text, and graph/output data where supported, and check whether an integrity gate fails closed. Finite enumerations will be reported as consistency evidence, not a substitute for the universal proof.

No original files, queue entries, or external records will be edited. No external communication is in scope. Child review artifacts remain in this assigned folder; the parent owns publication and repository checkpoints.

## 2026-10-13T03:16:18.237791+00:00: structural checkpoint

Completion estimate: 50%. Fresh independent structural suite passed; see `independent_structural_results.json`. It checks 2,112 deletion subsets, 7,982 arbitrary endpoint-extraction choices, 16,224 single-backup-edge deletion perturbations, 71 nonempty source graphs through four vertices, 16,042 subdivision covers, and 355 budgets including 4,096-bit values. No counterexample was found. Submitted files have now been copied to `submitted_working_copy`; further runs and mutations will use copies, leaving the original untouched.

## 2026-10-13T03:19:35.361717+00:00: completed computational audit checkpoint

Completion estimate: 100% of this computational audit. **No mathematical counterexample or required repair found.** This conclusion is conditional on the explicitly stated simple undirected, supplied-tripartition, unit traversal length, three-pair demand model. Priority and identification of the historical open question are separate audits.

### Strongest result and proof mechanism independently checked

The universal reduction is elementary and its two charging arguments survive arbitrary deletion patterns. In the subdivision lemma, each original edge contributes at least one gadget vertex, and an edge uncovered by the old-vertex set contributes a second; adding one endpoint per such edge yields a source cover no larger than |X|-m. In the spoke lemma, an original length-three geodesic corresponds bijectively to a cross-part H-edge. Every edge deletion that hits it charges to an endpoint of that H-edge, so choosing an endpoint of each deleted middle edge always produces an H-cover of cardinality at most |F|. Repeated endpoints decrease this cardinality. The finite-connectivity paths cannot introduce a path of length at most three; deleting an H-cover's spokes leaves each four-edge backup path intact. The lower bound ignores backup deletions without weakening the original edge-path hitting obligation. None of these universal arguments relies on finite enumeration.

Boundary cases checked: isolates; missing cross-part edge types as negative controls; empty source graphs via a fixed valid yes-instance; arbitrary middle/spoke mixtures; every endpoint choice in fresh small-graph tests; nonminimum covers and source cover extraction; 4,096-bit source budgets; and single backup-edge deletions. A missing edge type can make the corresponding original distance four or infinite, which confirms the lemma's stated premise is necessary. The edgeless-source rule does not require constructing its n-vertex graph, and the budget B=m+k has at most max(bitlen(m),bitlen(k))+1 bits. Positive rational deletion costs require exact addition and comparison; the bit length of a product of input denominators is at most their total encoded length, so this is a polynomial certificate check. Neither finite terminal connectivity nor the extension proof claims connectivity of every remaining nonterminal vertex.

### Reproduction

All commands were run from `/Users/alec/Documents/Math` using Python 3.14.6, standard library only, with no source-code imports from the submitted checkers in the fresh suite. The review path is `draft_pr_claimed_solved_900_1000_20261012/audits/pr904_30000347/reviews/computation_family`.

Commands, each exiting zero:

- `python3 <review>/independent_structural_checks.py` -> `independent_structural_results.json`.
- `python3 -O <review>/independent_structural_checks.py` -> `independent_structural_results_optimized.json`; all guards remain active.
- `python3 <review>/submitted_working_copy/verify_publication.py` -> `replay_normal.json`.
- `python3 -O <review>/submitted_working_copy/verify_publication.py` -> `replay_optimized.json`, byte-identical JSON output to normal gate.
- `python3 <review>/submitted_working_copy/mutation_tests.py` -> `submitted_mutation_results.json`; all 100 mutation cases rejected.
- `python3 <review>/optimization_and_integrity_controls.py` -> `optimization_and_integrity_results.json`; seven additional controls passed.

The supported gate verified all 24 payload files, all fixed anchors, the original manifests, and exact archive/directory byte equivalence. It replayed the three mathematical suites in disposable copies and obtained every recorded deterministic field and count, including the author's 165,952 deletion subsets and 3,375 (2,2,2)-part exact optima, the first audit's 756 endpoint-ordering cases, and the fresh controls' 862,464 deletion subsets, 903,892 cover extractions, and 32,298 suboptimal backup-extension deletion subsets. Both supported gate modes retained the original published results without rewriting them. Afterward all 25 original packet files and the working-copy files remained byte-identical, as recorded in `audit_result.json`.

### Assertion erasure and integrity limitations

A deliberately wrong hitting-set solver substituted into a disposable raw author checker raises a mathematical AssertionError in ordinary Python but reports PASS under direct `python -O` execution. This is a real limitation of invoking the raw scripts under optimization, not a defect in the documented publication gate. The gate uses explicit `require` guards (which optimization retains), verifies the scripts' bytes and anchors, and invokes `sys.executable -I <script>` without `-O`. A separate `PYTHONOPTIMIZE=2` sentinel control confirmed that this exact child-command shape uses optimization level zero and retains assertions. Supported ordinary and optimized gate runs both reproduced the suites. Therefore the documented publication commands are sound; future packaging must preserve this gate or replace raw mathematical asserts with explicit guards before offering direct optimized raw-script execution.

Additional attacks confirmed that changing a mathematical output plus its public-manifest hash still fails against the frozen manifest, and a byte-identical symlink substituted for a proof payload is rejected, in both ordinary and optimized modes. Hashes provide consistency against the trusted verifier and its anchors, not authenticity against an adversary replacing the entire verifier and all trust anchors. The package states that limitation correctly. The certificate is the mathematical edge-deletion list checked by BFS; the finite computation package is supplementary evidence and is not a formal proof-assistant certificate.

Exact remaining gap for this family: **none within the stated computational/structural audit scope**. Acceptance of priority or a claim that this was still open at the time of discovery requires the separate literature audit. No global files, queue entries, branch state, or external records were changed by this review.
