# Discovery worklog

This log records exact structural reductions, exploratory computations, and failed universal lemmas. Floating-point experiments are explicitly marked exploratory and are never used as final evidence.

## 2026-08-04: initialization

- Began parallel universal-proof and counterexample search.
- No literature was searched during discovery.
- Initial focus: molecularity/support closure, finite-step restoring paths, exact shell/generator identities, and small weakly reversible cycle enumeration.

## Exact failed lemmas recorded

1. Uncorrected one-step entropy drift fails on `0 -> A+B -> B -> 0` at `(n,0)`.
2. One-step total-count drift fails on the same boundary ray.
3. The most obvious coercive quadratic correction cannot repair that ray.
4. A universal finite-degree factorial-polynomial stationary ansatz already fails in the `0 <-> A` calibration unless exponential factors are allowed.

## Structural identity retained

Every enabled state transition lifts a directed complex-graph cycle.  If
`y->y'` fires from `x=r+y` and `y'=y_1->...->y_m=y` is a directed return path,
then the same reaction word is enabled successively from `r+y_j` and returns
exactly to `x`.  This is checked by `src/class_analyzer.py::lifted_cycle`.
