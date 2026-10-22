# Spectral Thickness of Fibonacci Hamiltonians

- Upstream ID: **30001687**; code: **OWR-4793-001**; queue rank: **620**.
- Disposition: **unsolved** after **5/5** substantive routes.
- No full proof, spectral counterexample, or novel discovery is claimed.

The order-of-magnitude weak-coupling statement is already a theorem: the spectral thickness is bounded above and below by positive constants times `1/lambda`. The unresolved part of this investigation is whether thickness is nonincreasing for every positive coupling. A precise asymptotic constant is a stronger question and is not supplied by the cited theorem.

`PROOF.md` states the exact target, gives elementary obstruction proofs and a conditional finite-gap monotonicity lemma, and identifies the missing uniform estimate. `RESEARCH_LOG.md` records the five distinct routes. `SOURCES.md` identifies the primary sources and the limits of the literature check.

## Reproduce

Requires Python 3, NumPy and SciPy:

```sh
OPENBLAS_NUM_THREADS=1 python compute_controls.py --output replay.json
```

The exact rational controls check 1,536 finite-gap configurations, six middle-third Cantor construction levels, and 120 transfer-matrix identities. Thirty-six finite spectral-approximation cases are exploratory floating-point calculations. They are not interval-certified bounds on infinite-spectrum thickness. Small roundoff differences between numerical-library versions are expected.

The author packet is frozen by `SHA256SUMS`. Fresh independent adversarial review is required before publication; the author phase performed no remote writes.
