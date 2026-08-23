# Pinned reproduction environment

The release package records and tests the following versions:

| Component | Version | Role |
|---|---:|---|
| Python | 3.14.6 | exact-verifier interpreter |
| SymPy | 1.14.0 | symbolic identities and rational functions |
| python-flint | 0.9.0 | exact rational matrix computations |
| mpmath | 1.3.0 | pinned SymPy runtime dependency |
| Tectonic | 0.16.9 | deterministic LaTeX compilation |
| Poppler | 26.08.0 | PDF metadata checks and page rendering |

`requirements.txt` records the three exact Python versions.
`requirements-lock.txt` additionally binds every accepted wheel artifact by
SHA-256. The sole certified end-to-end entry point is
`./run_all_referee_checks.sh` at the root of the enclosing reproducibility
package. It safely extracts an exact verified source tree before the internal
bootstrap installs from the lock with `--require-hashes`,
`--only-binary=:all:`, and `--no-deps`; SymPy's runtime dependency is therefore
explicit rather than transitively resolved.

Within that certified route, the internal environment stage is

```sh
submission/bootstrap_replay.sh --certified-package-stage
```

It requires Python 3.14.6, creates a fresh private virtual environment outside
the source tree, installs exactly those verified artifacts, checks their
versions and import origins, scans the bundled Python sources for
optimization-elidable bare assertions, and invokes the internal verifier
runner. Every interpreter command that can import project code uses `-B` and a
fresh command-line `-X pycache_prefix=...`; the controlled cache must remain
empty. The preceding exact-tree scanner is standard-library-only and imports
no project module. The outer launcher first requires exact regular-file and
implied-directory equality and rejects symlinks, special nodes, `__pycache__`,
`.pyc`, and `.pyo`.
Set `BOOTSTRAP_PYTHON` to the absolute path of a Python 3.14.6 interpreter when
`python3` resolves to a different version.

The certified launcher and both internal stages reject optimized Python and
clear inherited Python import/build overrides before any certificate runs.
Arbitrary `PYTHON` overrides are rejected; the internal verifier uses only the
environment freshly provisioned by its caller.
Each scientific condition is an explicit `require` check that remains active
under `python -O`.  The package-level command also executes an intentional
false check, a token-printing fake-interpreter control, and exact-tree hostile
controls before beginning the positive replay. Direct lower-stage execution is
development-only and is not an artifact-integrity certificate.

Tectonic and Poppler are external document tools, not Python dependencies.
The build fixes the Tectonic endpoint to the standard v33 bundle and requires
its cache-recorded content digest to be
`6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c`.
They can be checked with:

```sh
tectonic --version
pdfinfo -v
pdftoppm -v
```

They are needed by `build.sh`, which checks their versions and bundle identity,
compiles the PDF, inspects its metadata, and renders every page for visual
review. They are not needed by the internal verifier stage, whose theorem
checks use exact arithmetic and do not rely on the generated PDF.
