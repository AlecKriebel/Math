# Brownian first-visit supporting diagnostics

These five diagnostic families support the accompanying research note. A successful diagnostic run is not a proof or a publication approval. `reference/JOINT_LAW.md` is the byte-exact September 30 submitted candidate, preserved for replay; its pending-review and priority header is historical. The current manuscript and `../priority_and_provenance.md` contain the corrected attribution and current bounded-audit conclusions.

The direct Brownian proof uses killed-interval kernels, strong Markov stopping times, Tonelli, and compact-support moment determinacy. The following distinct diagnostic families supplement that argument:

| Script | What its receipt actually checks |
|---|---|
| `sources/author_verify.py` | 8,520 exact finite/algebraic diagnostics; the upstream diagnostic guard was repaired to survive optimization. |
| `sources/older_independent_checks.py` | 46,056 earlier exact normalization/order/ODE/Taylor checks. |
| `sources/independent_global_race.py` | 61 exact finite-cycle global-race and correlated-moment checks. |
| `sources/joint_clock_and_moment_controls.py` | 11,777 exact checks, including 2,052 weighted continuous-time finite-cycle configurations and three falsifying clock controls. |
| `sources/check_image_and_spectral_flux.py` | 180 image-versus-spectral flux cases and 120 explicit Laplace/singleton identities at 105 decimal digits. |

These counts describe different checks and must not be added into a purported proof score. The exact finite-state checks do not prove convergence to the continuum ownership law. The high-precision comparisons are diagnostics, without certified quadrature, rigorous truncation bounds, or a uniform numerical-error certificate. There is no Monte Carlo in these scripts. None establishes historical priority.

The scripts require Python 3.11 or later and were reproduced with Python 3.14.6. Four families require only the standard library. The scalar script requires mpmath 1.3.0. The declared and checked library environment also includes SymPy 1.14.0; the curated scripts do not use SymPy algebra. Existing interpreters and versions used in preparation are recorded in the actual run receipt. No installer or environment mutation is performed.

Run on a POSIX system using an existing interpreter and an existing library interpreter, specifying a **new output directory outside this verification source tree**. The process-group custody runner uses POSIX group APIs; the individual diagnostic scripts use platform-neutral Python:

```text
python run_diagnostics.py --stdlib-python /path/to/existing/python --library-python /path/to/existing/library-python --output-directory ../my_diagnostic_run
```

If the current interpreter already has the declared libraries, both interpreter options may be omitted. Each child has a 45-second timeout, an isolated process group, captured output, and a recorded actual PID, time, exit status, reap, and group-absence check. The runner tests every suite normally and with `-O`, compares the complete scientific receipt against its source baseline, and tests every real diagnostic guard with a true condition and a false condition in both modes. It writes output only into the separate run directory and authenticates the full source tree before and after every successful child. Cleanup also runs after communication exceptions; each termination/reap attempt is bounded. Any unresolved constructor outcome or process group is reported as failure.

Live PIDs, timestamps, interpreter strings, optimization flags, and paths can change on reproduction. Script SHA256 fields also change when the explicitly disclosed portable source derivative changes; they are separately authenticated against the full source manifest. Scientific values, test groups, counts, and reference-proof hashes are compared exactly. `DIAGNOSTIC_SPECIFICATIONS.json` lists the precisely excluded top-level live or derivative-identity fields. It does not discard scientific numerical differences.

Portability adaptations change only proof-file paths, output routing, and the scalar PID attribution. The older checker prints its receipt rather than writing beside its source. The scalar checker prints its full receipt, including all cases, rather than writing `RESULT.json` beside its source; its PID is called `actual_process_PID`, so future runs are not attributed to ROOT. The exact joint-clock script is unchanged. Full upstream sources, pins, and unified derivative diffs are retained in the package source_history folder; no third-party paper body is included.

The complete mathematical proof is in the manuscript. The bounded priority audit and its limitations are described in `../priority_and_provenance.md`. No checker decides historical priority or conventional human peer-review status.
