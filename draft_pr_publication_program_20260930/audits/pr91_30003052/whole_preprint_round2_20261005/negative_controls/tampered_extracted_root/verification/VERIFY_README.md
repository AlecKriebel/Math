# Finite verification for PR91

Run `run_all.py` with Python 3.9 or later and SymPy 1.14.0 installed in that interpreter. The boundary checker uses only the standard library. A new environment can be prepared explicitly:

```sh
python3 -m venv /tmp/pr91-venv
/tmp/pr91-venv/bin/python -m pip install "sympy==1.14.0"
```

From the directory containing `pr91_note.tex` and `verification/`:

```sh
/tmp/pr91-venv/bin/python -E -B verification/run_all.py --output-dir /tmp/pr91-run
```

The default artifact is `../pr91_note.tex`, resolved relative to the checker directory, independently of the current working directory. An explicit input is also accepted with `--artifact /path/to/pr91_note.tex`. Its SHA-256 identifies the input bytes; it does not certify the manuscript proof.

`--output-dir` must be empty or absent. Omit it to retain results in a newly created temporary directory. The runner passes explicit `--output` paths to each checker and `--details-output` to the boundary checker. It writes `results.json`, six receipts, a boundary event ledger for each mode, and complete process/stream evidence in the chosen output directory. Use an output directory outside the supplied verification directory. The runner refuses nonempty directories, including the supplied verification directory, preserving its included `results.json`.

Both ordinary and `-O` children run with `-E -B`; Python environment variables are removed rather than inherited. The code uses explicit `if/raise` condition guards, and the runner checks child exit codes, receipt/source/input hashes, family totals, and agreement of ordinary and optimized counts.

| Suite | Exact finite controls | Floating diagnostics |
|---|---:|---:|
| Submitted checker, minimally repaired | 473 | 0 |
| Earlier independent checker, minimally repaired | 907 | 0 |
| Independent boundary checker | 774 | 566 |
| Unique controls in each mode | 2,154 | 566 |

The submitted and earlier independent mathematical bodies retain the original computations. Their 80 and 224 radial orbit controls respectively check finite algebraic identities/phase encodings. The boundary suite adds direct complex-function evaluations, coupled norm balls, singular/nilpotent cases, rational group enumeration, endpoint rejection, and examples of finite-sampling limits. Floating checks use the declared tolerance `2e-10*(1+abs(rhs))`; they are diagnostics, not certificates.

`SOURCE_PROVENANCE.json` distinguishes authenticated original hashes, positive minimal repair hashes, and the CLI-adapted public hashes. The included `results.json` records the tested input/source hashes, Python/SymPy versions, actual per-suite counts, and runtime. The public adaptation is tested with native Python 3.9.6 and SymPy 1.14.0. Its six child runs completed in about 7.4 seconds on the recorded host; runtime is machine dependent. Python 3.9+ syntax compatibility is intended; other interpreter/dependency combinations require a fresh run.

These are exact finite algebra controls and sampled floating diagnostics. They do not prove the infinite-dimensional Koopman spectrum, an arbitrary-norm theorem, universal recurrence, continuity, Stone–Weierstrass density, spectral closure, or historical priority. Those conclusions require the written proof and separate scholarly review.

