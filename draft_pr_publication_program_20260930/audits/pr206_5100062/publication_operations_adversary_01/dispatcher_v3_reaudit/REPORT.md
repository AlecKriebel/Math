# Independent operations dispatcher v3/v4 re-audit

**Final verdict: CLEAN SOURCE VERDICT for exact v4 within the bounded owned-fixture scope.** No mandatory v4 gap remains. The unused v3 has one mandatory parser-output finding, preserved below. This report can supersede only the dispatcher-v2 portion of the previous audit after Root independently adopts v4; the exact five final07 sources and their prior acceptance are unchanged. No actual adoption, gate, ready90, kit, service, API or operational action was used.

## Exact source and independent order

| Source | Bytes | SHA-256 | Verdict |
|---|---:|---|---|
| reviewed v2 | 5148 | 3cce6202317f138d4c37f15dabf58f70492e170113a7cfae2f4a9c4918cecb63 | historical; FIFO blocking independently reproduced |
| requested v3 | 5631 | 94faca0bac216ebbca4e641bfa848bacddaae61f71544b44371361e60f2a3604 | parser-output finding |
| final v4 | 5737 | f927ec97eceeb73aaef7f6eec030b3697596930021efd946c04cccc07f2ecd2e | clean bounded source verdict |

The v3 and v4 originals were read in full and were sealed mode 0444; absolute paths are in REVIEWED_SOURCE_PIN.json and V4_REVIEWED_SOURCE_PIN.json. FULL_V2_V3.diff and FULL_V3_V4.diff preserve every change. FROZEN_PLAN.md was sealed before any v3 byte/diff exposure (4680 bytes, SHA 8655db94d8851312577e4378adfa9544a79a29829d76205b67f781b62a1d7100). V3_FINDING_FROZEN.md was sealed before any v4 byte/diff exposure (1805 bytes, SHA 87f8a5c0c16adeaef89c895c7307a6e1b9e8f98299f35d9c461c8c1afa29de0c). No lifecycle-adversary favorable outcome or Root favorable review was read.

The original final07/v2 REPORT.md, SAFE_MANIFEST.json and SEAL.json match PRESERVED_PRIOR_AUDIT_PINS.json byte for byte. All new files are inside dispatcher_v3_reaudit. Five source buffers were copied only from the prior audit-owned final07 copies and matched the hard-coded accepted hashes. Their contents were not changed.

## Tests and actual runtime binding

The v3 controller launched 46 v3 cases plus one v2 FIFO baseline: 221 child checks. Its actual exit 1 honestly reports the two parser contract failures. Every other v3 assertion passed. The v2 FIFO baseline exceeded its 3-second limit and the owned child was killed; this expected historical unsafe behavior is preserved, including empty raw streams and the timeout record. It is not treated as a passing v3 safety probe or a hidden harness error.

The v4 controller launched **59 bounded child cases with 300 checks; all passed**, controller exit 0 and empty stderr. No v4 child timed out. Each child was invoked with the exact pinned Python 3.14 runtime and -E -S -B -P; the explicit optimized-isolation probe additionally used -O and observed the required sys-only early refusal. Ordinary failed entry cases intentionally exit 1; successful routes/help/SystemExit 0/None exit 0. These expected child failures are part of the passing test suite.

RESULT_v3.json and RESULT_v4.json bind every actual child argv, flags, version/source pin, timeout, exit, raw stdout/stderr, metadata and check count. RUNTIME_BINDINGS.json binds the exact harness/controller byte hashes, controller raw streams/exits/results and resolved interpreter binary identity. The first exploratory parser probe did not separately preserve its exit value and is explicitly marked incomplete/not counted; the same mechanism was then reproduced in complete bound children. An exact additional replay of that initial probe recorded exit 1 with byte-identical raw streams (EXPLORATORY_BOUND_REPLAY.json), while retaining the original exit-field limitation. Raw diagnostics and the incomplete exploratory probe remain preserved. No executed test was silently discarded or relabeled.

## Mechanisms independently checked

- **Authentication and buffers:** wrong adoption basename, stale externally supplied adoption pin, gate/ready/self/source/source-set/mode/symlink tamper reject before compilation. Preflight compiles only common. Every publisher action (stage/inspect/publish/inspect-doi/finalize) and tracker action (append/recover) selects only common plus the requested module; valid confirmation paths preserve the explicit fixed kit string. The kit is never opened or executed. No author offline helper is compiled. Compiled common/selected source buffers are the exact audit-owned final07 bytes; their operational main/context functions are replaced by narrowly bounded synthetic stubs before invocation.
- **Cleanup:** argv values and alias presence/object identities are restored after normal preflight/routes, common/selected compile failure, selected main failure and invalid confirmation. Both preexisting and absent alias states are tested.
- **Static special files:** actual owned FIFO, directory, symlink, wrong-mode and oversized input reject before os.open. Pure lstat stubs additionally reject socket and character-device kinds without creating or opening a device/socket. Bounded regular files are accepted.
- **Replacement races:** the real os.open boundary is interposed only to replace an already-checked owned regular input with an actual FIFO, directory, symlink or oversized file. Actual open flags retain O_NONBLOCK and O_NOFOLLOW. The FIFO returns immediately and fstat rejects its kind; directory/size checks and symlink refusal likewise reject. Every race child finishes under its 3-second bound. No real device, socket service, external file or account is involved.
- **Error bodies/chaining:** chained RuntimeError preflight/publisher failures, OSError tracker failure, common/selected SyntaxError and selected ValueError produce no raw body, cause/context or traceback in user stdout/stderr. Text/bool nonzero SystemExit and KeyboardInterrupt are sanitized to the fixed line containing only the exception type and exit 1. Clean help, SystemExit 0 and SystemExitNone retain exit 0.
- **Parser regression:** invalid adoption-bytes, unknown argument, invalid confirm-id, invalid action and missing required arguments produce exact fixed type-only RuntimeError diagnostics with empty stdout in v4. Help remains clean. The separate early isolation check deliberately runs before dependency imports; invalid flags reject after importing sys alone, with no raw caller/service body.

## Preserved v3 mandatory finding and v4 repair

Default ArgumentParser.error printed raw input before entry() could catch SystemExit. Minimal owned invocation used --adoption-bytes SYNTHETIC_RAW_EXCEPTION_BODY_91; stderr included that exact marker in "invalid int value" plus usage, then the sanitized SystemExit line. An unknown option containing the same marker also printed its raw content. The outer wrapper cannot retract these bytes. Both v3 child exits were1, yet the output contract failed. See runs_v3/parser_bad_int.stderr and runs_v3/parser_unknown.stderr.

V4 adds SafeParser.error, which ignores the supplied parser message and raises a fixed-body RuntimeError. The unchanged entry() prints only "Root PR206 operations failed: RuntimeError" and raises SystemExit 1 without chaining. Independent v4 cases show that neither marker, traceback nor chained context appears. This closes the observed gap under the intended broad type-only operational failure contract. No other functional v3/v4 change appears in the full diff.

## Scope and remaining trust boundary

This is a bounded source re-audit, not an end-to-end service test or a proof against every filesystem/kernel failure. It validates owned local special-file behavior and authenticated dispatcher routing with synthetic context/main stubs. Actual Root adoption, whole-package gate and actual ready90 still require independent future evidence; real service behavior and the mathematical paper are outside this audit. The task-provided actual state is PR206 custody10, 48 completed,32 published, last205, cursor206; this audit made no state change and did not read live receipt/account contents.

No Git command, backend/cache, actual kit or gws execution, HTTP/API/network call, external service or external communication occurred. Child audit hooks report no attempted prohibited transport or outside-folder write. This audit neither creates operational authority nor grants mathematical clearance or release permission.

Source re-audit completion estimate: **100% of the assigned bounded v3/v4 review**, not mathematical truth, case progress or publication readiness.
