# Braid coefficient audit

Read `AUDIT.md` for the mathematical result, attribution, and unresolved scope; `INDEPENDENT_REVIEW.md` records the separate adversarial assessment.

Run `python check_coefficients.py` or `python -O check_coefficients.py` with Python 3 and its standard library. Output should equal `CHECKS.json` (also recorded as `CHECKS_OPTIMIZED.json`). The checker performs exact integer/rational computations; it requires no network, source PDFs, data files, credentials, or third-party dependencies.

The package establishes a scoped computational upper bound using established theory. It does not claim a novel algorithm, an optimal bound, or full resolution of the original informal complexity question. Literature inspection is bounded and finite tests are not a general proof.
