# PR421 reproduction adversary report

Sealed candidate prepared 2026-10-12T22:37:03.586161+00:00. Frozen PR head: `d5bf8b5a25cabb177433338fae60af52ebfecf1c`. Exact target: F(a,b,c) with a→a, b→ab, c→bcb and t f t⁻¹=φ(f). Original budget remains1/5;0 new proof-search turns.

The pinned normal-mode programs reproduce their finite checks and expected outputs. Their optimized-mode PASS strings are **not validation**: `python -O` deletes every one of their62 assert predicates. Eight meaningful corruptions are rejected normally and accepted with PASS under optimization. A separate explicit-check candidate repairs this runtime defect; its new independent audit is still pending. This report does not decide global mathematical implications assigned to the other review families.

## Independent criteria, inputs, and byte identity

`CRITERIA_SEAL.json` was written before reading the historical audit verdicts. All three programs were fully read first; all13 supplied source files, including prose inputs and saved outputs, were fully read before executing any verification program. No historical verdict was used as a substitute for the independent criteria or fresh controls.

Every receipt byte count and SHA-256 matches both the source snapshot and the file object at the frozen git head. The final checkpoint rechecks all13 snapshot hashes. `PIN_AND_STATIC_CHECKS.json` records the interpreter and static assertions. All work remains in this review directory and its owned private fixture directory; no branch/index/remote mutation, other-PR work, external outreach, or new proof search occurred.

Interpreter: `/opt/homebrew/opt/python@3.14/bin/python3.14`; `3.14.6 (main, Jun 10 2026, 10:03:53) [Clang 21.0.0 (clang-2100.0.123.102)]`; platform `macOS-26.6.2-arm64-arm-64bit-Mach-O`. `FROZEN_REPLAYS.json` and `REPAIR_REPLAYS.json` record each actual argv, cwd, start timestamp, duration, exit code, stdout/stderr, source hash, removed stale outputs, generated-output hashes and expected-byte comparisons. Runs were invoked by `replay.py --case <case>` and `replay.py --case <case> --tag repair --explicit-checks`, using the recorded interpreter, respectively.

Each program/mode/control starts with its own copied13-file fixture. All three saved/generated JSON output paths are deleted before each run. The author verifier prints its result and does not itself write checks.json; its stdout is compared with pinned checks.json. The geometric independent program prints a summary and writes its complete independent_results.json; the generated file, rather than its shorter stdout, is compared with the pinned output. The algebra program both prints and writes its complete result. Six baselines in each replay set pass; all expected output bytes match. No stale output is counted as a completed run.

## Actual checks and bounds

| Program | Static predicates | Normal predicate evaluations | Frozen -O evaluations | Repaired evaluations in either mode |
|---|---:|---:|---:|---:|
| verify.py |34|160|0|160|
| audit/independent_audit.py |24|142|0|142|
| audit/independent_algebra.py |4|6|0|6|

`EXECUTION_PROBES.json` records36 supplementary instrumented runs, including all62 predicates being reached on the successful baseline. These diagnostic counts do not replace the unmodified canonical replays. The final bytecode diagnostic independently counts34/24/4 normal assertion instructions and0 optimized instructions.

The author verifier checks the exact specified two K squares and two Q squares, endpoints and directed link corners, the3-edge involution, all4 local image links, prescribed tree-collapsed relators, and the14-vertex/32-edge/16-triangle link built as eight cones. It tests all364 possible3-subsets and1001 possible4-subsets of the14 vertices through exact clique enumeration; absence of a4-clique implies absence of every larger clique. It checks the cell vector(1,7,8,2), both inverse-automorphism compositions on all3 free generators,9 specified target relators (2 K +1 HNN +6 products), and4 generator-recovery words. Its17 internal negative controls are16 set-deletion comparisons and one wrong-involution-sign test, not17 independent script replay corruptions.

The independent geometric verifier constructs the8 actual square boundaries and all32 link-edge occurrences, confirms tree connectedness on4 vertices/3 edges, reconstructs16 actual corner triangles from the two3-cubes, checks8 side faces and4 horizontal faces against the specified cells, checks link multiplicities, and enumerates all possible clique sizes3 through14 (16,278 candidate subsets). It checks the unchanged proof byte hash under normal execution. Its17 internal controls comprise deletion of each triangle and the wrong involution sign. A comment mentions addition of missing edges, but no such edge-addition control is implemented.

The independent algebra verifier checks both compositions of φ and ψ on3 generators, evaluates the same9 concrete target relations, and recovers the original a and c from the substituted generators. These are exact finite word calculations for the displayed inputs. They do not by themselves prove the reverse presentation equivalence or arbitrary-word implications.

Under frozen optimization, the author script still builds some incidence data but no longer evaluates its asserted clique tests or target-relator validation calls. The independent geometric script still enumerates its clique dictionary and reconstructs cells, but comparison/rejection gates and proof-byte read are removed. The independent algebra script still computes9 relation normal forms, but its identity/recovery gates are removed. Thus nontrivial computations remaining under -O do not justify its PASS status.

## Corruption controls

| Control | Frozen normal exit | Frozen -O exit/status | Repair normal/-O exits |
|---|---:|---|---|
| verify_fullness | 1 | 0 / PASS | 1 / 1 |
| verify_cube_corner | 1 | 0 / PASS | 1 / 1 |
| verify_stable_sign | 1 | 0 / PASS | 1 / 1 |
| independent_fullness | 1 | 0 / PASS | 1 / 1 |
| independent_cube_corner | 1 | 0 / PASS | 1 / 1 |
| independent_cube_side | 1 | 0 / PASS | 1 / 1 |
| algebra_stable_sign | 1 | 0 / PASS | 1 / 1 |
| proof_byte | 1 | 0 / PASS | 1 / 1 |

All normal failures are the intended AssertionError gates. The local-fullness controls delete a Q link corner before the fullness comparison; the cube-corner controls delete an actual link triangle before the count/flag comparison; the cube-side control alters the p side's vertical endpoint and reaches the side-cell compatibility gate; the stable-letter controls change z=c⁻¹t⁻¹ to z=c⁻¹t and reach relator evaluation; the proof control appends a newline and reaches the byte-hash gate. There are no import, missing-library, syntax, or incidental filesystem failures masquerading as successful controls.

Frozen optimized author runs still print the uncorrupted hardcoded Z link vector and flag=true after a corner deletion, and still print9 target relators verified after the stable-letter sign mutation. The optimized independent geometric proof-byte control prints frozen_proof_hash_matches=true with changed proof bytes. The optimized independent algebra sign control prints PASS while product_d=`CBaabc`, product_e=`bCaacB`, and HNN=`Baab` are nonempty. These failures concern runtime certificate validation, not a detected counterexample to the uncorrupted mathematical construction.

## Separate validation repair and its provenance

The sealed overlay changes Assert(test,msg) to `if not test: raise AssertionError(msg)` and bare Assert(test) to `if not test: raise AssertionError()`. The original test and message ASTs are retained; message expressions execute only on failure, bare exception args remain(), and all original control exception types/args match in diagnostic normal/repaired-normal/repaired-optimized executions. The frozen programs do not reference or shadow AssertionError; these local runs use the unmodified builtins environment.

`explicit_checks.py` generates the overlay and certifies one-for-one correspondence for all62 predicates. It reparses the generated source, confirms the intended transformed AST, inversely restores assert nodes, and verifies equality with the entire original AST with source locations omitted. Thus every other original AST statement and mathematical expression is retained. AST unparse changes formatting, line numbers, and tracebacks; literal traceback identity is not claimed. Neither mathematical data nor proof bytes are changed.

The overlay is held separately under overlay/. `OVERLAY_PROVENANCE.json` records every predicate/message AST and source/output hash. Each repaired replay starts from a fresh frozen copy, applies the same explicit transform (after any intended fixture corruption), and records all transform hashes. All six repaired baselines have byte-identical stdout/generated JSON to their corresponding unmodified frozen baselines; all16 repaired corruption runs fail at their intended gate and leave no generated output. No frozen original is edited. A newly assigned adversary must independently examine this sealed candidate before promotion.

To execute the overlay, copy the frozen packet into a new fixture and replace only its three program paths with the corresponding overlay files, then remove the saved JSON outputs before running. The overlay directory alone does not contain the proof bytes required by the geometric program. The repair scope is exactly these three historical programs; no optimization-safety claim is made for other repository or peer-review scripts.

| Overlay program | SHA-256 |
|---|---|
| verify.py | `e3357a9af58d68c2f450d2901ab71c58ed955112017fe0ec758d1adc3b36ca42` |
| audit/independent_audit.py | `281ebf97900d047447a2a3865f233cfba1c41df6dd6c4e8aaae66150250b1903` |
| audit/independent_algebra.py | `3fda0f889aa454390c6f30c54c842a0a49a5f5a3d1bdea0bce5819711e3dbc96` |

## Historical freeze and portability boundary

The five hashes in INITIAL_WIP_FREEZE.json match their actual git objects at WIP commit `bb7dac6872a680735897b1701a1a41d22e19f562`. ATTEMPT_1.md, verify.py, and checks.json are byte-identical between WIP and published head. SOURCE_GATE.md and RESEARCH_LOG.md differ through the disclosed later source/review updates; their complete diffs are recorded in HISTORICAL_PROVENANCE.json.

Neither independent audit program exists at that WIP commit. The13-file publication packet retains the initial five-file hash manifest, but not the originally local independent program/manifest lookup. The published program directly pins ATTEMPT_1.md and uses paths relative to its own location. Its present behavior is independently pinned and replayed. The claim that earlier independent-script changes affected only portability cannot be independently byte-compared from this supplied history, and the older prose statement that all five current files match the local frozen manifest does not describe the two intentionally updated documentation files.

## Initial failure retained and corrected

The first replay record's bytecode counter recognized only LOAD_ASSERTION_ERROR and falsely counted0 normal assertions on Python3.14, whose assert opcode uses LOAD_COMMON_CONSTANT(AssertionError). INITIAL_FROZEN_REPLAYS.json and private INITIAL_replay.py preserve that diagnostic failure. Final replay.py recognizes both opcodes and the repeated final replay records the correct34/24/4 normal counts. The initial program exits, outputs, and corruption outcomes were valid and are independently repeated. A git query for the pre-publication independent program failed because that file is absent from the WIP commit; that failure remains recorded.

## Strongest result and exact remaining gap

All frozen normal finite-certificate results reproduce exactly at the pinned head; all8 meaningful controls are effective normally. All frozen optimized PASS strings lack every stated predicate gate. The explicit-check overlay is a reproducible validation-only repair that locally executes every predicate and rejects the same controls in both modes, pending a new independent repair adversary.

This family does not independently settle the global semantic proof: reversible group identification, cube-complex theorem hypotheses, CAT(0)/proper/cocompact implications, exact external source identity, and novelty are separate review-family obligations. Finite computations are partial evidence for those obligations. Historical pre-publication independent program bytes remain unavailable in the supplied packet. Reproduction-family completion estimate:100%; this is not a mathematical-discovery completion estimate.
