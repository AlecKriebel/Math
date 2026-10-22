# Detached diagnostic validation revision 1

This revision addresses tooling durability only. All initial sealed artifacts in `../corner_cohomology_adversary/` are preserved verbatim. It changes no mathematical proof, lemma, interpretation, or initial report. The original `CHECKS.py` was copied into this new folder as the starting point; no initial report or other family report was copied or edited.

## Issue and historical scope

The initial checker used 19 Python `assert` statements. Python optimization can remove those statements, so the initial positive result is historical evidence from its recorded **normal-mode** run. It does not establish that validations remained active under `-O` or `-OO`. The initial checker also wrote a runtime timestamp into `CHECK_RESULTS.json` automatically; replaying it in place could overwrite its sealed result. The new runs below do not retroactively upgrade or replace the initial execution record.

`INPUT_BINDING.json` binds the exact initial code, report, result and output manifest by relative path, byte count and SHA256. The initial manifest binds the rest of the initial public seal. Every initial manifest member and every input binding was verified before and after the revised replay.

## Concrete revision

The new `CHECKS.py` keeps the original finite algorithms and replaces every optimization-sensitive validation statement with `require(condition, meaningful_message)`. The helper raises `RuntimeError` explicitly. The 19 predicates were preserved, including the multiline Pauli comparison. No Python `assert` statement remains in the revised checker.

Default execution emits deterministic JSON to stdout and writes no result or fixture file. The optional `--output NEW_PATH` uses exclusive file creation and refuses an existing path. Mathematical result data contains no execution timestamp. Actual UTC start/end observations, Python version, mode, exit status and output hashes belong to the separate `VALIDATION_RUNS.json` record.

`--false-sentinel` deliberately calls `require(False, ...)` before producing any positive result. This tests whether an explicitly false validation survives optimization. It is a diagnostic negative test and is expected to exit nonzero.

`RUN_VALIDATION.py` is an authored replay driver using only the Python standard library. It runs normal, `-O`, and `-OO` positive checks; verifies byte-identical stdout; compares their mathematical fields with the historical normal-mode result after removing the old timestamp; runs the false sentinel in all three modes; tests explicit new-file output; and tests refusal and preservation of an existing temporary output file. Temporary files are created only within this detached folder and are removed. Its default output is stdout. Its optional saved record and deterministic-result paths also use exclusive creation.

## Actual run and result

The recorded replay started at **2026-10-18T02:47:24.662556Z** and ended at **2026-10-18T02:47:32.072053Z**, using Python 3.14.6. The three positive executions each exited 0, produced no stderr, and emitted the same **1,172-byte** deterministic JSON result:

    SHA256 b3c1a857fb30eb51ae613770ccba066290f56fa83d34f59e8dfd222a5bb341a5

The intentionally false validation exited 1 in every mode with the expected `RuntimeError` and no positive stdout. The output-file refusal test also exited nonzero, with `FileExistsError`, and preserved the existing file. Per-run actual UTC times and hashes are recorded separately in `VALIDATION_RUNS.json`. The revised finite result is in `DETERMINISTIC_RESULTS.json` and agrees with the mathematical fields of the historical normal-mode result.

These are finite diagnostic checks. They do not formally verify the infinite-dimensional C*-algebra proof or change its external mathematical inputs.

## Reproduction

From this revision folder, the following commands print results and do not replace saved results:

```text
python3 CHECKS.py
python3 -O CHECKS.py
python3 -OO CHECKS.py
python3 RUN_VALIDATION.py
```

The negative diagnostic is `python3 -OO CHECKS.py --false-sentinel`; an exit status of 1 with the documented intentional error is its successful outcome. For new saved outputs, pass explicitly selected filenames that do not exist. `RUN_VALIDATION.py --record NEW_RUN.json --deterministic-output NEW_RESULT.json` performs the full replay and creates those files exclusively.

## Exposure and completion

This revision used root’s tooling feedback, the previously authored initial checker and report context, the initial result, and its seal metadata. No other family’s or root’s mathematical report was read. No new source material was queried. The mathematical lemmas retain exactly the independence and exposure qualifications of the initial report; this tooling revision adds no mathematical independence claim.

Completion estimate: **100% toward this diagnostic validation durability revision**. There was no candidate, git/index, remote, publication, or external-individual mutation or communication. Exact authored public output membership, bytes, and SHA256 values are in `OUTPUT_MANIFEST.json`; the manifest excludes itself and private or temporary files.
