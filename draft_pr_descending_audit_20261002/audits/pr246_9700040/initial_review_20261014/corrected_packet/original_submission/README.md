# 9700040 — drift-jump stationary joint law

**Unreviewed first-turn full candidate.** Read PROOF.md for the exact model and all-index joint probability formula. The construction and computation use classical patience sorting, RSK, skew Jacobi–Trudi and exponential Schur specialization, all credited in SOURCES.md. The already known two-particle density is a control, not a claimed discovery.

The formula has fixed-size factorial determinants and an explicit Poisson-tail certificate. It gives arbitrary-precision rational bounds for any rational joint-survival query. For example:

```sh
python stationary_law.py --x 1 2 --indices 2 3 --cutoff 18
python verify_exact.py
```

Only Python's standard library is needed. The first query is P(X2>1, X3>2); its certified interval is approximately [0.7963516175945655,0.7963516175952137], with exact rational endpoints in exact_receipt.json. Decimal displays are not certificates. The second command reproduces the exact author receipt. There are no external executable dependencies or simulations.

The independent review must check the literal source scope as well as stationary dynamics, uniqueness, RSK prefix counting, fixed-dimension transposition and the truncation certificate. No historical novelty, proposer acceptance, efficient large-index computation, or human peer review is claimed.
