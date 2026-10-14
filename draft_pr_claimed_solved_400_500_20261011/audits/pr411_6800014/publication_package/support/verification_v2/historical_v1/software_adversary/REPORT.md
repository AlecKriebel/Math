# Independent software adversary — PR411 / 6800014

**Result: PASS; zero active software component blockers after repair.** The prior FIFO inventory defect below was independently falsified, repaired by the producer, and retested. This is a component verdict; final delivery custody must receive the separate integrity replay described below.

## Scope and claim

I independently refreshed remote PR/queue scope, inspected the root gate and source receipt, and stopped neither on drift nor changed eligibility because all checks passed. Exact source head is `ac8b960bdda61c154cc30d7e3aba70389a9b139e`; PR411 remains open, draft and unmerged on `research/ricci-pinching-6800014`; the exact-head queue row remains `claimed_solved`, author turns `2/5`. All nineteen source-snapshot objects match receipt size, SHA256 and Git blob SHA1; bundle `original_packet/` matches them, and `global_candidate/author_packet/` matched bundle `author_packet/` during component review.

The software hypothesis was that the current three checkers change the original full AST only by replacing each message-free `assert P` with `if not P: raise AssertionError(constant diagnostic)`, preserving predicates, evaluation order, laziness and truth conversion; all mandatory checks survive optimized execution. Package replay must bind the nineteen original objects, nineteen current objects, prose, manifests, six frozen objects, delivered scripts and positive file inventory, and reproduce original normal-mode stdout.

The reviewed provisional whitelist had 50 positive files and SHA256 `b66a6555a2b83c08d7f22aab541fff3d457dea6ebbe33a8c006b0d81d8ab069f`; provisional seal SHA256 was `b64188256753aa1bbfdba12f2cc426762124f72ca8b0cc46fe351d55b1028e87`. This is not the future final seal. The reviewed executable code digests are recorded in `VERDICT.json`.

## Verified guard behavior

An independent reverse transform restored the candidate's mandatory guards into assertions, checked every label and predicate separately, and compared the entire restored AST to the original. It passed for all 19/2/18 original assertion nodes; no assertion message existed and no unrelated AST change was allowed.

Own AST instrumentation returned each evaluated predicate object unchanged, then counted completed predicate evaluations. It reproduced these native Python 3.14.6 / SymPy 1.14.0 results:

| Script | Static original checks | Original normal | Original `-O` | Current normal | Current `-O` |
|---|---:|---:|---:|---:|---:|
| `verify.py` |19|24|0|24|24|
| `check_hessian.py` |2|2|0|2|2|
| `audit/independent_checks.py` |18|28|0|28|28|

All current normal/optimized stdout digests equal the original normal digests. Looped guards account for the 54 runtime checks. Explicit `False and (1/0)` fails by mandatory `AssertionError` without division; `True or (1/0)` passes without division. An independently exercised stateful predicate object had exactly one `__bool__` call and retained object identity through the measuring wrapper. Inspection of `run_checked.py` confirms its wrapper records once and returns the original value, leaving the original `not` to perform truth conversion.

Original optimized execution prints the same success text while evaluating zero assertion predicates. It is therefore expressly **NOT CERTIFIED** validation, regardless of stdout equality.

## Resolved adversarial finding SW-1

In the first provisional runner, the positive inventory added entries only when `path.is_file()` was true. A fresh private bundle copy with `os.mkfifo(bundle / 'unlisted_fifo')` returned exit 0 and `PASS` in both normal and `-O` execution. The FIFO was neither listed nor rejected. This contradicted exact packet inventory certification.

The producer added a mandatory `path.is_dir() or path.is_file()` requirement after symlink rejection, with `nonregular entry excluded from packet` diagnostics, and added native FIFO controls. Independent post-fix FIFO and Unix-domain socket fixtures now fail in both modes at that requirement. The initial false-PASS outputs are retained privately; they are evidence about the prior runner, not the repaired candidate.

## Independent package retesting

I independently reran `reproduce_controls.py` against the repaired 50-file bundle: **38/38 executions matched their stated expectations and required diagnostics**. This includes successful normal/optimized foreign-directory execution and clean relocated whitelist archive extraction with path spaces; byte-corrupted current theorem interval, current manifest claim, frozen proof and metadata, original receipt and candidate checker; missing and extra files; unlisted FIFO; whitelist corruption; direct false predicates in each checker; direct frozen-file corruption; short-circuit traps; and a changed predicate with recomputed candidate manifest, whitelist and seal. That recomputed-hash attack still failed the exact AST relation. Hash corruption controls failed on the named metadata mismatch; direct false predicates failed on mandatory `AssertionError`, so failures were checked for cause and not merely nonzero status.

Ten additional post-fix native execution checks covered two successful baselines, file/dir symlinks, FIFO and Unix-domain socket rejection in both modes. Nine direct `safe_path` cases rejected traversal, absolute paths, repeated separators, leading `./`, trailing separators, empty and non-string paths. Twelve unchanged current/original objects are byte-identical, including both mathematical attempt texts, full historical audit, source audit, frozen metadata and all six frozen files. Each of the three changed document originals is an exact byte prefix of its current document; changes are append-only addenda. Current executable changes meet the independently checked exact AST relation.

An early independent replay was interrupted when my direct import of the runner created its bytecode cache before the module's bytecode setting took effect. The positive inventory correctly rejected that unlisted cache. The producer removed the generated runtime artifact; no source was changed. I repeated the full control suite with `-B`, and retained both the interrupted cause-specific execution and successful fresh runs. Raw logs, fixtures, interpreter environment and private notes stay outside the delivered bundle.

## Custody and limits

Hash checks bind reviewed bytes; they do not prove arbitrary prose semantically. The whitelist includes every positive file except itself and the final seal; the seal hashes the whitelist and its real digest must be authenticated through independent parent custody before execution. This avoids self-hash cycles. A party replacing all executable code, content, whitelist and seal together is outside the documented unkeyed integrity threat model.

`TEST_RESULTS.json` was a producer placeholder during the reviewed provisional bundle executions. It was never treated as evidence of a pass. This verdict uses own executions and diagnostic inspection. Incorporating these three reports and final public result/metadata updates into the 53-file delivery whitelist requires a subsequent normal/optimized integrity replay. That replay must retain the executable code digests in `VERDICT.json`, exact guard relations, 54 checkpoints and immutable original inputs; it does not require changing this report or embedding the future final seal hash within itself.

The digest-only historical source manifest `f5446c816081c5322e4279bcd9a61dca5bfb63cfacf69d105d1587ed9d93b7fb` and pre-layout checker `eccde3c2a903b1fca0f232e7e392d537479ddd3936281a37e87c4f7e7047be97` remain **UNATTESTED** because their byte objects are absent. Six included frozen-object checks do not attest those absent objects. This audit adds zero author proof-search turns, certifies no novelty or historical runtime, does not independently promote mathematical proof, and does not replace later sequential whole-package manuscript adversaries.

Private checkable evidence resides at `private_sources/verification_repair/software_adversary/`: fresh scope, independent reverse AST, byte relation, runtime counts, truth-conversion/laziness fixtures, prior and post-fix raw diagnostics, unsafe-path cases, socket/FIFO fixtures, and the 38-control replay. Public reproduction uses the delivered `reproduce_controls.py` with raw logs outside the package.
