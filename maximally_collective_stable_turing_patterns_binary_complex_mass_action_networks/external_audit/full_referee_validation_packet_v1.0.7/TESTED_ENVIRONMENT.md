# Tested environment and prerequisites

The packet is platform-neutral source, but the convenience scripts target a
Unix-like shell.  The complete replay requires:

- Python with assertions enabled (never use `python -O`);
- `pdflatex` and Biber, with TikZ, biblatex, AMS, and standard LaTeX packages;
- Poppler's `pdffonts`;
- GNU `sha256sum` (on macOS, install GNU coreutils);
- `awk`, `cmp`, `find`, `grep`, `sort`, `tail`, and `xargs`.

Install the Python requirements from `repository/requirements.txt` in a clean
virtual environment.  The final detached release replay passed with:

| Package | Version |
|---|---:|
| matplotlib | 3.7.1 |
| numpy | 1.24.3 |
| pandas | 2.3.3 |
| pypdf | 6.10.0 |
| pytest | 8.4.2 |
| scipy | 1.10.1 |
| sympy | 1.14.0 |

The successful document build used Biber 2.17.  The replay checks required
commands and Python minimum versions before doing substantive work.  Record the
actual versions used in the referee report; do not silently treat an unavailable
stage as passed.

The full numerical-illustration stage is intentionally slower than the exact
symbolic verifiers.  `FINAL_RELEASE_QUICK=1` is useful for diagnostics but is
not a substitute for the complete referee run.
