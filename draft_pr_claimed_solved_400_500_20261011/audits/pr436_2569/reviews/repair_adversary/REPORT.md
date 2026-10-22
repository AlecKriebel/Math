# Independent adversarial audit of the PR436 verification repair

Scope is the separately repaired verifier overlay for PR436 / problem2569 / KOU-21.60, with frozen source head `c7805ab0804f50c6f4b0d1dda99e433dbb702ae2`. This is existing-claim verification after the five author attempts. It adds zero proof-search attempts. It makes no source-status, priority, publication or PR decision.

The acceptance criteria were sealed at `2026-10-12T21:55:53.260502+00:00`, before reading prior repair verdicts. I fully read the builder, repair runner, reused replay harness, equivalence checker, and all four frozen and four repaired verifier programs before execution. The independent static checker uses an inverse transformation of the actual repaired branches; it does not import the reproduction family's transformer or use that family's verdict as its conclusion.

Verdict: **PASS for the optimization repair, with a diagnostic fidelity difference**. All 82 original test predicates and all other source AST semantics are preserved. All baseline, integrity, exact coverage and mathematical negative-control checks pass. Literal failure-message/exception-argument equivalence does not pass because bare assertions receive location messages. No substantive mathematical or runtime-rejection defect was found. Completion estimate: 100% of this bounded repair audit.

## Byte provenance and unchanged mathematics

All 26 frozen attempt files were independently compared with both the receipt hashes and the actual Git blobs at the pinned source head. Every comparison passed. The repair provenance has SHA-256 `21e2a909dcf22f7799bdf270e79bb4a288b088edc969d0658069ea8194200a85`. The reproduction public manifest has SHA-256 `7076186534c4d462da2659b413c403a4de5f69622cf0a1db90716995ad9b4983`, and all 27 listed files match their lengths and hashes.

The four repaired source hashes are:

| Program | SHA-256 |
|---|---|
| `verify_counterexample.py` | `9c31ef4175d5e8468796ceee814a65385c3dff2bc29490d4b6077c089b3bc112` |
| `verify_controls.py` | `04a8cc2a7d1af2425632859bbf52c9b98c19649e449930d2197d7f4302efaa95` |
| `contributor_checks/check_character_data.py` | `70137337365d8de1ddabf81594c5f020af9622015005085dd37fd97bd75acf42` |
| `independent_audit/independent_audit.py` | `93a8c71dbba6b3dc76b38fc370efdfc19dcd65b49d7242158dd3675b6a3160cd` |

The independent inverse-AST check identifies 15, 2, 18 and 47 explicit failure branches respectively, for 82 total. Each branch has exactly the original test AST under one logical negation, one uncaught `AssertionError` raise, and no else branch. Restoring those branches to the original bare assertions gives an AST identical to the full original program. Thus imports, mathematical constants, rational arithmetic, loops, generators, matrix computations, input paths, output fields and success flags are preserved. Chained comparisons retain their original middle-operand evaluation and short-circuit semantics. The three original explicit order-bound raises also remain present.

There are no residual assertion statements or `__debug__` guards. Recursively compiled repaired code has identical instruction bytes at optimization levels zero and one. The normal/optimized counts of explicit AssertionError loads are respectively 17/17, 2/2, 18/18 and 48/48; their excess over 82 comprises the three pre-existing explicit order-bound raises. No essential source check was moved under an optimization-elided condition.

The repair changes no mathematical claim, formula, expected result or external-input byte. The proof and idempotent coefficients remain bound to the frozen hashes. The `repaired_verification` folder is a code overlay. Its README correctly requires an isolated copy of the pinned original attempt, preserving the proof and coefficient inputs; the parent runner supplies that copy. Directly treating the overlay alone as a complete input package would fail, and its documentation does not claim otherwise.

## Failure diagnostic difference

Literal message equivalence is not satisfied: all 82 original assertions have no message, whereas the builder supplies a source-location string. Originally a failed assertion has empty exception `.args`; the repaired failure has one string argument. This is a diagnostic change, not a predicate, arithmetic, control-flow or acceptance change. There is no message expression with side effects, and the new constant argument is evaluated only on failure. The source does not shadow `AssertionError` or catch those failures.

The repair report's phrase “preserving ordinary assertion behavior” should be understood as preserving tests and failure-versus-success behavior, with this diagnostic addition stated explicitly. If exact exception-argument compatibility is required, a bounded validation-only repair is to emit zero call arguments for `node.msg is None`, and one original message argument otherwise. That would need new separate repair hashes and revalidation. No such change was made to the sealed repair. There is no mathematical or runtime-failure blocker arising from the current messages.

## Fresh private replay and finite-check coverage

All executions use private fixture copies. Historical result files are removed from every new fixture before the run. A successful baseline therefore cannot be accepted merely because an old matching result survived. The interpreter is Python 3.12.14 with SymPy 1.14.0; the symbolic requirements are pinned in the repair package.

Sixteen baseline runs cover the four frozen and four repaired entry points in both normal and optimized modes. Every process exits zero, creates a fresh expected output, and has stdout and JSON bytes exactly equal to the historical frozen result. No pre-existing fixture input changes during execution. Source-normal baseline correctness and repaired-mode correctness are checked separately from the inadequate original optimized-mode success.

For execution coverage, source-normal assertions are reformatted into separate statements in private tracing fixtures without changing their AST. This avoids counting a one-line loop or conditional header as an assertion. Every repaired branch is mapped back to its original source line. Test-entry opcode tracing then counts the first instruction of each condition rather than comprehension loop line events.

The initial line-event experiment is preserved in `EXECUTION_RESULTS.json`; its counts include Python 3.12 inline-comprehension events and do not mean exact predicate-evaluation totals. The initial opcode experiment is preserved in `OPCODE_COVERAGE_AND_NORM_CONTROL.json` and its original script; it recorded zero events because the calling frame's opcode flag was not enabled before installing the tracer. These are audit-instrumentation corrections. The v2 opcode record supersedes both initial coverage totals. No baseline or mathematical-control evidence is affected.

Exact source-normal counts are 14,774 for the author verifier, 17 for controls, 21 for contributor checks and 15,140 for the independent verifier. All four match repaired normal and repaired optimized modes exactly, including the per-site counts. The complete suite executes 29,952 condition evaluations and visits every one of the 82 original assertion sites in each repaired mode. In particular, the author closure check executes for all 14,400 quaternion products, and the independent homomorphism check executes for all 14,400 products. The latter also executes 81 character orthogonality tests, three rational idempotence checks and three central projective rank identities. No finite coverage comparison remains pending.

## Independent mathematical negative controls

These are deliberate private corruptions of already-existing verification inputs/computations, not new proof attempts.

1. Replace the symmetric-cube trace polynomial `x^3-2x` by `x^3-3x`, leaving the constructed quaternion group and test expectations intact. Both repaired modes reject at the exact rationality/integrality check, frozen source line 57. The original normal program rejects; the original optimized program exits zero, writes `all_assertions_passed: true`, and reports norm `8/5` and Frobenius–Schur indicator `0`. This reaches a real mathematical invariant and shows why original optimized byte replay alone cannot establish validation.
2. Double the computed character values, retaining exact integer arithmetic, the quaternion products and the Frobenius–Schur calculation. Its character norm becomes `4` instead of `1`. Both repaired modes reject at the exact norm test, frozen source line 62. The original normal program rejects; the original optimized program exits zero and reports `all_assertions_passed: true` with norm `4`. Rejected repaired runs produce neither a success stdout record nor a fresh result file.

I also inspected the existing reproduction family's ten raw fault records. Their return codes and stdout/stderr hashes match the published record, and all terminate in the intended explicit assertion checks: augmentation rank (line 114), cyclic rank (line 32), weighted character orthogonality (line 29), exact idempotence (line 200), or proof-byte identity (line 269). They are not incidental package-import failures. That inspection supplements, rather than replaces, the two independently executed mathematical controls above.

## Exact remaining scope

The verification repair restores optimization-safe rejection of failed finite invariants and preserves the original computations. Its successful outputs do not themselves establish the theorem-level implication to nonsemiperfectness; that theoretical bridge and source-dependent representation facts belong to the separate mathematical audits. No new proof or literature search was performed here.

All private fixtures, mutation scripts, raw executions and dependency inputs remain under `private_sources/repair_adversary` except the read-only interpreter reused from the reproduction family's existing environment. No sealed original or repaired public output was modified. No external communication, remote write, commit, push, branch change or PR operation was performed by this audit.

## Final execution provenance

The audit records 64 executions, including the preserved initial instrumentation experiments and repeated norm control; their measured process durations total 388.541 seconds. The 16 uninstrumented fresh baselines are distinct from coverage runs. Both new mathematical control families were run against source and repaired code under both modes. Execution commands, UTC start/end times, process durations, statuses and stdout/stderr hashes are retained in the machine records. `EXECUTION_INPUT_MANIFEST.json` pins the actual preserved private input/entry bytes for every recorded run. `RESULT.json` is the final adjudication and the v2 opcode JSON is the authoritative exact coverage record. All 27 sealed reproduction public files and all 26 source-head inputs still match their pins at completion.
