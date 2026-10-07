# Torus spinorial infimum: author packet

**Original problem 30005600 / OWR-14297736-006 remains unresolved after 5/5 substantive approaches. Independent review is pending.**

Start with `PROOF.md`. It specifies the exact spin, kernel, conformal and area conventions, credits the known b≥2π regime, preserves five mathematical routes and identifies the unproved sharp lower bounds. The main elementary partial computes the full first-positive eigenvalue for a nonconstant one-variable conformal-factor family with an explicit all-sector condition. It is not a solution of the original conjecture and carries no novelty claim.

Files:

- `PROOF.md`: complete arguments, gaps and primary citations
- `RESEARCH_LOG.md`: five approach records and completion estimates
- `STATUS.json`: machine-readable scoped disposition
- `SOURCES.json`: public-source/corpus hashes, sizes and inspection scope, without source contents
- `check_exact.py`, `EXACT_CHECKS.json`: portable exact arithmetic controls
- `search_conformal.py`, `SEARCH_RESULTS.json`: non-certified numerical Rayleigh--Ritz search and all resulting parameters
- `READINESS.json`: exact claim, source and bounded duplicate gate

## Reproduction

Run `python check_exact.py` from any directory using the file's path. It prints the frozen exact-control result; `python -O` prints the same result, since checks do not depend on assertions. These finite controls are not formal analytic verification.

The numerical search requires NumPy and SciPy. Run `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python search_conformal.py`. It overwrites `SEARCH_RESULTS.json` beside itself. For replay, use a disposable copy if preserving the freeze. The recorded run used Python's available runtime, NumPy 2.3.5 and SciPy 1.17.0. Minor last-digit and optimizer-path differences across BLAS/library versions are expected. Floating-point quadrature is not interval certified, and the variational discretization supplies no lower-bound certificate.

The initial search contains 287 factor evaluations and 14 optimizations, which used 1,666 objective evaluations in the recorded run, plus controls and refinements. No finite search result is treated as proof of the conjecture.

The source PDFs, extracted texts, source-page image, raw catalogue record and detailed coordination/retrieval material are separate and excluded from this author packet. No queue edit, remote publication, DOI, release, or outreach was performed. Any later review or correction should be preserved separately rather than rewriting this freeze.
