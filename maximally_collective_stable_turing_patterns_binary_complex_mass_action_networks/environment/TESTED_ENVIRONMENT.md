# Tested release environment

Release qualification for version 1.0.10 uses one pinned document route and one
exactly recorded Python stack.  This file distinguishes that qualification
environment from the broader lower bounds in `../requirements.txt`.

## Python

- CPython 3.9.6, assertions enabled;
- the exact packages in `../requirements-tested.txt`;
- `PYTHONHASHSEED=0`, `MPLBACKEND=Agg`, `TZ=UTC`, and `LC_ALL=C`;
- one BLAS thread through `OPENBLAS_NUM_THREADS`, `OMP_NUM_THREADS`,
  `MKL_NUM_THREADS`, `VECLIB_MAXIMUM_THREADS`, and `NUMEXPR_NUM_THREADS`.

The lower-bound file `requirements.txt` describes compatible exploratory
environments.  It is not the environment used to qualify reproducible release
artifacts.

## TeX

- TinyTeX 2022.04 / TeX Live 2022;
- pdfTeX 3.141592653-2.6-1.40.24;
- preloaded `pdflatex` format dated 2022-04-04;
- LaTeX2e 2021-11-15 patch level 1;
- Biber 2.17 and biblatex 3.17.

The recovered package versions are recorded in
`texlive-2022.04.lock.txt`.  `check_toolchain.sh` checks the engine, Biber,
Python, and the load-bearing package versions before a release replay opens its
log.  A newer TeX Live installation is not release-equivalent: TeX Live 2026
was independently observed to change supplement pagination and PDF extraction.

Version 1.0.7 PDFs identified an xdvipdfmx/Tectonic producer even though its
replay invoked pdfLaTeX.  They remain immutable historical artifacts.  Version
1.0.10 qualification intentionally rebuilds all active PDFs with the single
pdfLaTeX/Biber route above; byte identity to historical v1.0.7 PDFs is neither
expected nor claimed.

## Determinism boundary

Exact JSON and generated TeX artifacts must match their shipped SHA-256
baseline byte for byte.  Numerical integrations are checked within the stated
solver/refinement tolerances.  PDFs are checked for the pinned producer,
pagination, fonts, and semantic content rather than against historical PDF
bytes.
