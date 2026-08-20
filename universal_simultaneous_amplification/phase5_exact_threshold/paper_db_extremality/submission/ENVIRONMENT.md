# Pinned reproduction environment

The release package records and tests the following versions:

| Component | Version | Role |
|---|---:|---|
| Python | 3.14.6 | exact-verifier interpreter |
| SymPy | 1.14.0 | symbolic identities and rational functions |
| python-flint | 0.9.0 | exact rational matrix computations |
| Tectonic | 0.16.9 | deterministic LaTeX compilation |
| Poppler | 26.08.0 | PDF metadata checks and page rendering |

`requirements.txt` pins the two Python libraries. The clean-extraction command

```sh
submission/bootstrap_replay.sh
```

requires Python 3.14.6, creates `.venv-paper1`, installs exactly those library
versions, checks the installed metadata, and runs the full certificate replay.
Set `BOOTSTRAP_PYTHON` to the absolute path of a Python 3.14.6 interpreter when
`python3` resolves to a different version.

Tectonic and Poppler are external document tools, not Python dependencies.
They can be checked with:

```sh
tectonic --version
pdfinfo -v
pdftoppm -v
```

They are needed by `build.sh`, which compiles the PDF, inspects its metadata,
and renders every page for visual review. They are not needed by `replay.sh`,
whose theorem checks use exact arithmetic and do not rely on the generated
PDF.
