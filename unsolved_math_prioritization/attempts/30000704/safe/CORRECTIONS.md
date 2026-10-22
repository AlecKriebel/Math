# Author-side corrections before freeze

2026-10-04 17:29 UTC: Two preliminary symbolic-control runs stopped at the singleton
curvature identity because a simplification-only zero predicate did not reduce
an expression containing 2^(2a), 4^a, and expanded rational terms. Factoring
that exact expression gave zero. The final predicate tries direct factorization and exact rational
combination with power simplification before the original simplifier. The mathematical formula and claim were unchanged. A fresh full
run is recorded in CONTROL_RESULTS.json. This was an author-side control
repair, not independent audit, and its initial failure is preserved here.
