# Exact-check reproduction

**Result: passed.** Reproduced on 2026-10-01 at 03:44 UTC (2026-09-30 local time). This is computational reproduction support for the preprint package, not a fresh adversarial review or a formal certificate of the general analytic proof.

Both `independent_checks.py` and the invoked `source_snapshot/checks.py` were inspected before execution. The independent script performs exact symbolic checks, invokes the inspected source script, writes two reproduction outputs in this verification folder, and checks snapshot hashes. The source script performs symbolic calculations and prints JSON. Neither requests network access or modifies snapshot files.

The fresh ignored `.venv/` uses CPython 3.14.6 on macOS ARM64, SymPy 1.14.0, and mpmath 1.3.0, installed from the pinned `requirements.txt`. Python optimization was disabled, so assertions executed; `-B` disabled bytecode writes.

From this verification directory, the reproduction command was equivalent to:

```sh
.venv/bin/python -B independent_checks.py > independent_results.json
```

The independent script and its child source script both exited zero with empty stderr. The checks passed for the auxiliary-circle polynomial derivation and elimination, the cleared rational denominator and ideal-membership certificate, regular-normal edge samples, arbitrary-target and non-orthonormal general-position perturbations, rank-one circle-component checks, and the source script's original sanity checks. The separating value is 16 and the rational denominator is `r**4*t**4`.

`checks_rerun.stdout.json` is byte-for-byte identical to `source_snapshot/checks_output.json`. All 16 snapshot files matched `original_snapshot_manifest.json` before execution and remained unchanged after execution. The preserved snapshot remains the original PR head `a29887ed0e341851d02fa992c26500d4089267be`; the `head` field in the independent output identifies that historical snapshot.

SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| `independent_checks.py` | `337adde27ea231b26f501b751216401f95af747819b7449861267e835c0e55de` |
| `requirements.txt` | `47fd19021144e071cc43b6e265aafada0056abe89724ad95bd6e3a8e37995b94` |
| `independent_results.json` | `e000cec7a78840f0141aeea295930346907dd909037256491704e5f9883a4172` |
| `checks_rerun.stdout.json` | `1bab82a3df95caf30ce8c5a91916625b464e9c71b489f66009e3cb369fea314a` |

`reproduction_manifest.json` records the full environment, timestamps, exit status, all 16 snapshot hashes, and preservation/comparison checks. `independent_run.stderr.txt` and `checks_rerun.stderr.txt` preserve the empty stderr streams. No paper, priority file, source-snapshot byte, Git commit, branch, or remote was changed.

Checkpoint: reproduction-support task 100% complete. This measures completed reproduction work, not the probability of correctness or historical priority of the theorem. Fresh package adversarial review remains a separate step.
