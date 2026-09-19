# Serial compilation runner audit and repairs

Timestamp: 2026-09-19T03:55:33.271144+00:00.

## Result and scope

The bounded runner repair is complete (**100% of this subtask**). No Lean build was launched during this runner audit. Actual package-wide Lean acceptance and the missing final group theorem remain separate obligations.

Changed only `scripts/build_serial.py`, `scripts/check.py`, `docs/OFFLINE_GUIDE.md`, and `docs/TRUST_REPORT.md`, plus these audit records.

## Defects repaired

1. The original serial helper deleted an object only immediately before compiling that module. A failed prerequisite could therefore leave stale descendant objects. The runner now invalidates `.olean` and `.ilean` objects for the entire selected import closure before starting.
2. `subprocess.run` timeout could kill Lake while leaving its Lean child running. All commands now run in new POSIX sessions; timeout or interruption terminates the entire process group, escalating to KILL. A TERM-resistant descendant was tested.
3. The runner now rejects compiler exit zero without the expected new object and removes partial outputs on errors/timeouts. Missing executables are recorded as failures. Exceptions or source mutation invalidate all selected objects.
4. Project modules compile in exact topological closure order with `-j1`; the unsupported Lean 4.19 `-M6000` option was removed. Project source hashes must remain fixed throughout the run. In-progress and aborted summaries cannot report success.
5. `check.py` calls the serial builder directly, applying timeouts per module rather than timing out the whole package. No parallel `lake build` is used for project compilation. Full static inventory, actual transitive axiom queries, and elaborated statement queries remain required. Failed builds stop before those queries.
6. Dependency checks now reject untracked changes, plus ignored untracked Lean source outside `.lake`. Normal ignored Lake build/cache artifacts remain allowed. This closes the source-shadow gap identified in the earlier table review.

## Fresh-build semantics

`--fresh-project` explicitly requests the default behavior: selected project objects are rebuilt from source while pinned upstream objects are preserved. The old `--fresh` requested a full dependency-source rebuild; it now fails explicitly with guidance rather than silently changing meaning. No full upstream dependency source rebuild is claimed. The separate optional `lean4checker --fresh` flag retains its original same-kernel replay meaning.

The standalone `build_serial.py` helper performs compilation only. Use `check.py` for dependency-pin checks, static-inventory checks, actual axiom inspection, and statement output. Neither runner supplies the missing BCH construction or unconditional automorphism-count theorem; `complete_formalization` remains false and the default final gate still exits nonzero.

## Validation

- Python syntax compilation passed for both scripts.
- Existing runner self-tests passed (four source-rejection and four axiom-output rejection controls).
- Temporary-project tests verified exact selected closure, full upfront stale-object invalidation, preservation of unselected objects, failed-import blocking, partial-object cleanup, timeout handling, missing-output/executable rejection, and source-mutation rejection.
- A real subprocess hierarchy with a TERM-resistant child stopped writing after the parent command timed out, demonstrating process-group termination.
- Temporary Git repositories verified ignored build artifacts are accepted and both ignored and unignored untracked Lean source are rejected.
- Mocked integration controls verified serial invocation, continued axiom/statement inspection on success, blocked inspection after failure, the still-closed default final gate, and explicit rejection of unsupported full-fresh mode or invalid timeout.

See `runner_negative_controls.json`, `runner_integration_controls.json`, and `runner_repair_sources.json`. These are Python runner controls, not mathematical proof checks or independent Lean-kernel validation. Process-group behavior is POSIX-specific, matching this macOS audit environment.
