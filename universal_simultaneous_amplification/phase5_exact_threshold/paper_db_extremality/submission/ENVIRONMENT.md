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
SHA-256.  Bootstrap installs from that lock with `--require-hashes`,
`--only-binary=:all:`, and `--no-deps`; SymPy's runtime dependency is therefore
explicit rather than transitively resolved. The clean-extraction command

```sh
submission/bootstrap_replay.sh
```

requires Python 3.14.6, clears and recreates `.venv-paper1`, installs exactly
those verified artifacts, checks their versions and import origins, scans the
bundled Python sources for optimization-elidable bare assertions, and runs the
full certificate replay.
Set `BOOTSTRAP_PYTHON` to the absolute path of a Python 3.14.6 interpreter when
`python3` resolves to a different version.

The referee launcher, bootstrap, and direct replay reject optimized Python and
clear inherited Python import/build overrides before any certificate runs.
Each scientific condition is an explicit `require` check that remains active
under `python -O`.  The package-level command also executes an intentional
false check and requires a nonzero status before beginning the positive replay.

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
review. They are not needed by `replay.sh`, whose theorem checks use exact
arithmetic and do not rely on the generated PDF.
