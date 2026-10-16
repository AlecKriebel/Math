# Actual-package applicability correction

This additive implementation correction supersedes only the prior final `release_binding.py` pin. The prior report, 27 control groups, exact source snapshots, `FINAL_SOURCE_BINDINGS.json`, and original 2,512-payload repair seal remain unchanged. This is internal implementation evidence, not independent review or actual release authority. Case estimate: **65%**, as reported by the root after the second scientific review; this shard adds no discovery percentage for this implementation fix.

## Actual-package defects and repairs

Root review correctly found that the previous top-level export guard rejected actual snapshot B's `manuscript.log`. This 14,573-byte compiler log is outside `SOURCE_MANIFEST.json`, but is one of the second whole-package review's 230 frozen files, with SHA256 `868ac21e46287f930b3b42b1c4015752fb1b4dc736b291cd11a4ec28f2ef6936`. The repair adds only the known `manuscript.log` basename, and only after `public_exports()` has successfully read and hashed its explicit cleared case-relative `preprint/manuscript.log` export-manifest pin. The guard still rejects arbitrary added top-level files even when someone includes their pins in that manifest. A missing, stale or symlinked compiler-log pin fails.

While building the actual-package control, this shard also found that whole02's sealed `FROZEN_INPUTS.json` stores `core` as a basename-to-pin object, while whole01's `FROZEN_BYTES.json` stores a list. The previous parser supported only the first review's list shape. The new parser explicitly normalizes both existing shapes, preserves exact seven-name equality, and requires the assessment's frozen bindings to agree. The direct old-source failure is retained in `PRE_FIX_ACTUAL_REVIEW_FAILURE.json`, with traceback and stdout/stderr. No scientific/reviewer byte was changed to accommodate the parser.

## Controls and preserved evidence

All **seven new exact-source groups passed** in `PROBE_RESULTS.json`. The current binding source is compiled directly from its retained exact bytes; no operative source text or AST is rewritten. All copied package/log edits occur only in owned synthetic fixtures.

- All 230 actual B frozen files were hashed against whole02's actual freeze. Its complete 16-file top-level membership was copied unchanged. The old exact binding rejects the compiler log; the new exact binding accepts it with its explicit export pin.
- Omitting that pin still rejects the actual compiler log.
- `UNREVIEWED.txt` and `.env` remain rejected, including when explicitly added to the synthetic manifest.
- Changed compiler-log bytes and symlinked compiler logs are rejected.
- The actual whole01 seal, additive report correction, actual root resolution, and actual final whole02 seal all validate as two sequential reviews with one exact-current clean review. Every listed sealed payload is read and hashed, including the final whole02 provenance additions.
- The existing exact-source publication, append and fresh read-only checks still complete with one synthetic stage, one publish and one append.

The prior repair manifest SHA256 remains `29dde1f64a90d07c48c38ec80566acd592873358cd38ebc09e7c34559ed6acfa`; all its 2,512 payloads were rehashed unchanged. All original six helper01 source copies and scientific B bytes remain unchanged. Every deliberately failing outcome, old-source failure and controlled altered log is retained. No live provider, Git/index/ref/database/queue, secret, environment/cache or external communication action occurred. All Python used the standard runtime with `-B`.

## Updated source pin and interface

`release_binding.py`: **33,660 bytes**, SHA256 `208b080ef950a6bd136050720f55b099a596ca9ecfd0068ebfc92138a474a600`. The other three assigned operative sources retain their prior pins. `FINAL_SOURCE_BINDINGS.json` here records all four current pins, the exact prior seal, actual whole02 seal and unchanged B/log evidence.

Callable signatures and returned binding keys are unchanged. `SCHEMA_ADDENDUM.json` records the two normalized freeze forms and the narrow compiler-log export rule. The native implementation agent and root were informed of the changed binding source hash before a new source review. A new independent review of all six final sources remains required; no actual clearance was created.
