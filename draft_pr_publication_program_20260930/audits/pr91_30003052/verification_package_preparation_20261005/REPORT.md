# Verification preparation handoff

**Code and finite-control verification complete; final manuscript receipt is parent-owned.** The six public support files are frozen at 2026-10-05T19:38:45.029756+00:00 in `frozen_support_files/`, with byte counts and SHA-256 hashes in `PUBLIC_SUPPORT_FILE_MANIFEST.json`. The manifest excludes itself and the final manuscript/current-input receipt. Completion estimate: **95% of verification package preparation**; the parent explicitly accepted the remaining final artifact binding.

Public directory: `publication_package_v1/publicfiles/verification/`. It contains `verify.py`, `independent_checks.py`, `boundary_checks.py`, `run_all.py`, `SOURCE_PROVENANCE.json`, and `VERIFY_README.md`. It intentionally has no `results.json` yet. The parent will run the frozen wrapper once manuscript edits end and copy that current-input compact receipt.

The submitted and earlier independent mathematical bodies are byte-identical to the positive minimal repair bodies. Their `ck` ASTs are unchanged. The stdlib boundary mathematical body is also byte-identical to its audited origin. Adaptations add explicit artifact/output CLI, remove the boundary checker's unnecessary optimization prohibition, and clarify receipt scope. All four public Python files have zero `ast.Assert` nodes; all condition guards use explicit `if/raise`. Authenticated originals and minimal repairs retained their recorded hashes; `ADAPTATION_AUDIT.json` and `PREPARATION_RESULTS.json` record these checks.

The actual outer positive invocation was `/usr/bin/python3 -E -B`, runner PID **50586**. Python reported **3.9.6**, SymPy **1.14.0** on the native interpreter path. `sys.executable` resolved to `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`; that actual child argv is recorded without relabeling. No PYTHONPATH was injected or inherited, and no dependency was installed. The wrapper was launched from the unrelated private preparation cwd with no `--artifact` override, verifying the default manuscript path one level above `verification/`.

| Checker | Ordinary PID | Optimized PID | Controls in each mode |
|---|---:|---:|---:|
| Submitted | 50587 | 50606 | 473 exact finite algebra |
| Earlier independent | 50591 | 50611 | 907 exact finite algebra |
| Boundary | 50605 | 50615 | 1,340 = 774 exact/discrete + 566 floating |

All six children exited 0, had zero stderr bytes, and retained identical checker-source hashes. Each suite's ordinary/optimized receipt bytes are identical. Complete per-child argv, cwd, PID, UTC start/end, exit status, source snapshots, and full binary streams reside in `positive_all/*/execution.json` and adjacent files. The outer record and all supplied source snapshots are in `executions/positive_all/`. The total outer wall time was about 7.4 seconds. Maximum recorded floating error was `1.2775558388966601e-11`, below `2e-10*(1+abs(rhs))`; floating controls are diagnostics, not certificates.

The earlier actual positive input SHA-256 was `28bb22de40351846d5a1514e39d8a7ae758aad369c4d4a5373b88d9f03dfba09`. The parent manuscript subsequently changed, so this private receipt must not be represented as the current manuscript receipt. `finalize_preparation.py` detected that mismatch and refused to copy a stale public result. No mathematical checks depend on the manuscript content; its hash identifies bytes only.

Private optimized false-control copies failed for the intended explicit guard: submitted PID **49604**, independent PID **49624**, both exit 1, empty stdout, and `AssertionError: PRIVATE_DELIBERATELY_FALSE_CONTROL`. These modified false controls remain private and are not original replays. The optimized wrapper also rejected the nonempty public verification directory as an output destination, PID **52157**, exit 1; a before/after SHA comparison confirmed every public file unchanged. Records are under `executions/false_*_optimized/` and `executions/nonempty_output_refusal_optimized/`.

The strongest result is verified preservation and runtime reproduction of these finite controls, with optimization-safe fail-closed behavior. They do not prove the infinite-dimensional spectral theorem, universal arbitrary-norm validity, analytic continuity/density/recurrence arguments, spectral closure, or priority. No Git, PR, branch, release, outreach, Zenodo, Sheet, UI, PDF authoring/compiling, or original mutation was performed. Only the assigned public verification directory and this private sibling folder were written.

For final binding, run the existing wrapper using a new empty private output directory after the parent manuscript is frozen, then copy that directory's compact `results.json` to the public verification directory. Refresh the parent package's support manifest after adding the receipt; the frozen code hashes should remain unchanged unless the parent repairs code.

