# Continuous four-point/edge-conditioned moment search

This directory records a continuous-support upper-bound attempt for the
fixed \(N=41\) five-dimensional kissing problem.

The degree-four moment formulation, exact normalizations, cap/product
flag, harmonic trace cuts, and bottleneck are in
[`FORMULATION.md`](FORMULATION.md).

The factorial strengthening is in
[`FACTORIAL_HIERARCHY.md`](FACTORIAL_HIERARCHY.md).  The exact continuous
rank-five Gram matrix showing why its finite-pool Farkas ray does not
extend to all atoms is in
[`CONTINUOUS_FARKAS_COUNTEREXAMPLE.md`](CONTINUOUS_FARKAS_COUNTEREXAMPLE.md).

## Outcome

The baseline relaxation is feasible.  An existing positive rational 74-atom
mixture of genuine rank-five \(K_6\) Gram matrices induces exact
pair/triple/\(K_4\) measures with masses \(40,1560,59280\).  It passes:

- all continuous Gram-support moment/localizer constraints at every
  polynomial order;
- all edge-conditioned polynomial covariance blocks, by an explicit
  atomwise SOS decomposition;
- the selected closed semialgebraic robust-depth/cap/product row;
- and all 27 sharp degree-at-most-three harmonic rank trace cuts.

The product row is saturated exactly.  Therefore that formulation cannot
have a valid dual objective below 41.  The missing information is
not supplied by higher polynomial degree within a single
edge-conditioned covariance block.

A subsequent strengthening does separate both the 74-atom \(K_6\)
witness and the alternate 53-atom \(K_7\) lift: an integer cap
\(\Gamma\le M\) has higher falling-factorial consequences beyond its
mean and the depth/cap product.  See
[`FACTORIAL_HIERARCHY.md`](FACTORIAL_HIERARCHY.md).  The available K7
pool can be repaired at the univariate cap level by one explicit
rank-five atom, but its first joint depth/cap moment extension is again
infeasible.  These are local-pool obstructions, not a continuous upper
bound.

This is an obstruction to an upper-bound route, not a spherical code and
not a resolution of the kissing-number problem.

## Reproduction

From the repository root:

```sh
PYTHONPATH=. /usr/bin/python3 \
  experiments/continuous_four_point_moment/verify_exact_counterwitness.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  experiments.continuous_four_point_moment.test_verify_exact_counterwitness \
  -v

PYTHONPATH=. /usr/bin/python3 \
  experiments/continuous_four_point_moment/verify_factorial_hierarchy.py

PYTHONPATH=. /usr/bin/python3 \
  experiments/continuous_four_point_moment/verify_factorial_farkas_independent.py

PYTHONPATH=. /usr/bin/python3 \
  experiments/continuous_four_point_moment/audit_full_depth_factorial_rows.py

PYTHONPATH=. /usr/bin/python3 \
  experiments/continuous_four_point_moment/verify_continuous_farkas_counterexample.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  experiments.continuous_four_point_moment.test_factorial_hierarchy \
  experiments.continuous_four_point_moment.test_continuous_farkas_counterexample \
  -v
```

The verifier uses only the Python standard library and exact rational
arithmetic.  It pins the two input certificates by SHA-256.

The optional discovery-only repair search additionally requires
NumPy 1.24.3 and SciPy 1.10.1:

```sh
PYTHONPATH=. /usr/bin/python3 \
  experiments/continuous_four_point_moment/search_factorial_repair.py
```
