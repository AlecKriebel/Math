# Pinned reproduction environment

| Component | Version | Role |
|---|---:|---|
| Python | 3.14.6 | exact-verifier interpreter |
| SymPy | 1.14.0 | exact rational functions, algebraic roots, and Sturm checks |
| mpmath | 1.3.0 | pinned SymPy numerical dependency for displayed-decimal audits |
| Tectonic | 0.16.9 | deterministic LaTeX compilation |
| Poppler | 26.08.0 | PDF metadata checks and page rendering |

`requirements.txt` pins both Python libraries.  The clean-extraction command

```sh
bootstrap_replay.sh
```

requires Python 3.14.6, creates `.venv-paper2` under the extracted project,
installs SymPy 1.14.0 and mpmath 1.3.0 without retaining a pip cache, checks
installed metadata, and runs the complete exact replay.  Set
`BOOTSTRAP_PYTHON` to the absolute
path of a Python 3.14.6 interpreter when `python3` resolves to another version.

Tectonic and Poppler are external document tools, not Python dependencies.
Check them with:

```sh
tectonic --version
pdfinfo -v
pdftoppm -v
```

They are required by `build.sh`, which compiles the PDF, reports metadata, and
renders all pages for visual review.  They are not required by `replay.sh`.
The coefficient verifier uses high-precision root approximations only to
audit displayed decimals; its theorem-bearing root counts, identities,
threshold inequalities, and tangency statements are checked exactly.
