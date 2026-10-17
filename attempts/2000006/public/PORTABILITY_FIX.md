# Optimization-safe public replay

This is a packaging-only correction. All 109 accepted mathematical and public-metadata artifacts remain byte-identical, and E-6322 remains UNSOLVED 5/5. No new mathematical research pass was performed.

The earlier portable wrappers used Python assertion statements as release gates. Python optimization could remove those gates and disable inherited checker assertions. The revised wrappers use explicit exception checks for manifest semantics, file sets, safe paths, byte counts, hashes, child exit status, output identity, adapter check lists and unchanged-package validation.

Each checker is launched without optimization flags, with interpreter-environment flags ignored, and with an explicit check that its optimization level is zero. PYTHONOPTIMIZE is removed from the subprocess environment. This matters for the unchanged final exact script's nested historical exact replays: their direct interpreter launches inherit the sanitized environment and retain their original assertions. Generated result files are removed from disposable copies before execution, so an early successful exit cannot reuse a stale historical output as a fresh computation.

Use replay.py for the supported historical replay. Directly invoking an original assertion-based checker with optimization enabled is not a supported verification route.

The included test_release_guards.py exercises six modes: normal, -O, -OO, inherited PYTHONOPTIMIZE=1, inherited PYTHONOPTIMIZE=2, and -OO combined with inherited PYTHONOPTIMIZE=1. Every mode includes a clean full replay and rejection controls for same-length terminal-status corruption, unexpected and missing files, malformed and wrongly typed manifests, false manifest status, false final and nested exact identities, nonzero child exit, zero exit without generated output, and changed child output.

The mathematical-identity, child-exit and output controls deliberately reseal their isolated fixtures. The verifier must first accept those fixtures' updated hashes, after which the replay must reject their invalid execution or computation. This distinguishes active semantic checks from rejection caused merely by stale hashes. The accepted payload itself is never changed by these controls.

All six clean replays pass with identical output; all 66 negative cases are rejected. RELEASE_GUARD_RESULTS.json records the 72 controls without copying subprocess tracebacks or temporary paths. REPLAY_RESULTS.json remains the concise auxiliary-computation record. Neither successful record resolves the mathematical benchmark.
