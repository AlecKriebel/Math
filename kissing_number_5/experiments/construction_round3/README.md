# Construction Search Round 3: Riemannian Augmented Lagrangian

## Status

**NUMERICAL EVIDENCE ONLY — NOT A CONSTRUCTION CERTIFICATE OR AN UPPER
BOUND.**

No 41-, 42-, 43-, or 44-point code with maximum inner product at most
\(1/2\) was found.  All reported coordinates and diagnostics use binary64
arithmetic.  In particular, a solver basin, a small Riemannian gradient, an
apparently rank-five Gram matrix, or repeated convergence to the same active
graph proves neither feasibility nor nonexistence.

This round is independent of the Euclidean L-BFGS-B and epigraph SLSQP
refinements used in rounds 1 and 2.  It ran 152 fully unrestricted trials:

- 44 asymmetric Gaussian starts (11 for each \(N=41,42,43,44\));
- 44 starts obtained by perturbing the best stored 41-point numerical
  benchmark and inserting points into sampled holes when \(N>41\);
- 60 starts from greedy deletion after rank-five projections of D6, E6, E7,
  and E8 roots, plus coordinate projections of E6;
- four direct warm starts from the best stored round-2 artifacts.

After initialization, every coordinate was released.  The only retained
constraints were the 41--44 unit-norm equations.

## Optimization mechanism

For pair inner products \(s_e=\langle x_i,x_j\rangle\), the exact minimax
epigraph formulation is

\[
 \min \mu,\qquad s_e-\mu\leq0,\qquad x_i\in S^4.
\]

For multipliers \(\lambda_e\geq0\) and penalty \(\rho>0\), the program uses
the Powell--Hestenes--Rockafellar augmented Lagrangian

\[
 L_\rho(X,\mu,\lambda)
 =\mu+\frac1{2\rho}\sum_e
 \left(\max(0,\lambda_e+\rho(s_e-\mu))^2-\lambda_e^2\right).
\]

The epigraph variable is not optimized approximately.  Its stationarity
condition is \(\sum_e w_e=1\), where

\[
 w_e=\max(0,\lambda_e+\rho(s_e-\mu)).
\]

Thus \(\mu\) and \(w\) are obtained by an ordinary projection onto the
simplex.  The remaining objective is minimized on the product manifold
\((S^4)^N\) using Polak--Ribiere+ Riemannian nonlinear conjugate gradients,
projection transport, Armijo line search, and row-normalization retraction.
The multiplier update is \(\lambda\leftarrow w\).

Before the multiplier stages, each unrestricted start is spread using the
Riemannian high-power energy

\[
 \frac1p\log\sum_{i<j}(1-\langle x_i,x_j\rangle)^{-p}
\]

for \(p=2,4,8,16\).  The penalty schedule is

```text
1, 3, 10, 30, 100, 300, 1000, 3000,
10000, 30000, 100000, 300000.
```

The implementation is
[`manifold_augmented_lagrangian.py`](manifold_augmented_lagrangian.py).
Finite-difference tests independently check both analytic Riemannian
gradients.

## Best final values in this round

| \(N\) | round-3 best final maximum | gap above \(1/2\) | start |
|---:|---:|---:|:---|
| 41 | 0.5149946525251737 | 0.0149946525251737 | stored public-41 benchmark |
| 42 | 0.5198232355737906 | 0.0198232355737906 | public-41 plus hole insertion |
| 43 | 0.5262395764127177 | 0.0262395764127177 | random E7 projection |
| 44 | 0.5274711925378671 | 0.0274711925378671 | round-2 layer warm start |

None is feasible.  Round 3 did not improve the stronger public comparison
values already recorded in
[`../random_codes/RESULTS.md`](../random_codes/RESULTS.md), namely
`0.5182411558622624`, `0.5247096018290212`, and
`0.5274577123235323` for \(N=42,43,44\).  Those comparison values also
exceed \(1/2\) and are not exact configurations.

Since no result was at or below \(1/2\), the conditional exact-reconstruction
stage was not entered.

## Recurrent 41-point basin

All 11 asymmetric Gaussian starts at \(N=41\) converged to maximum inner
products in the narrow interval

```text
0.5155570516796980  to  0.5155570523908195
```

with mean `0.5155570520054867`.  Every one had, at tolerance \(10^{-8}\)
below its own numerical maximum, a connected 155-edge graph with degree
histogram

\[
 5^1\,6^3\,7^{14}\,8^{18}\,9^5.
\]

For core seed `2026072300`, the multiplier continuation was:

| stage | numerical maximum | positive multipliers |
|:---|---:|---:|
| high-power \(p=16\) | 0.5301694867228040 | — |
| \(\rho=1\) | 0.5191626357031828 | 178 |
| \(\rho=30\) | 0.5156406912629810 | 159 |
| \(\rho=1000\) | 0.5155572641513104 | 155 |
| \(\rho=30000\) | 0.5155570553874318 | 155 |
| \(\rho=300000\) | 0.5155570518130886 | 155 |

The five positive numerical Gram eigenvalues for seed 0 were

```text
7.927833778445850
8.227612733071263
8.232016836650647
8.304397753318291
8.308138898513950
```

and the largest absolute value among the other 36 computed eigenvalues was
`2.98e-15`.  The basin had 111 pairs strictly below `-0.5` in binary64.

This is a reproducible positive stall gap of about `0.01555705`, not a
rigorous lower bound on the optimum.  Agreement of objectives and active
degree histograms also does not by itself prove that all resulting
configurations are exactly isometric.

## Better imported 41-point benchmark

The stored public benchmark remains better, at
`0.5149946525251737` after round-3 refinement.  Its \(10^{-8}\) active graph
has 153 edges, degree histogram

\[
 0^6\,8^{18}\,9^{10}\,10^6\,12^1,
\]

one 35-vertex component, and six isolated vertices.  Its five positive
numerical Gram eigenvalues are

```text
7.884359360889101
7.992145992517903
7.992145992517907
8.167199730103983
8.964148923971110
```

with computed null-spectrum residual `3.20e-15`.  Thus even the best observed
basin remains about `0.01499465` above feasibility and has numerical
rattlers; neither rigidity nor a prescribed contact graph can be assumed.

## Stored artifacts

The JSON files store every final binary64 coordinate, the complete
optimization history, full Gram spectrum, top inner products, deep-negative
pair count, and explicit zero-based active-edge lists at tolerances
\(10^{-4},10^{-6},10^{-8}\).

| file | runs | SHA-256 |
|:---|---:|:---|
| [`results/portfolio_core.json`](results/portfolio_core.json) | 84 | `4b927239e59bb9d59274f41145a5474a47f9f0af5140c7e9ffb6cec9cdb560cf` |
| [`results/portfolio_asymmetric.json`](results/portfolio_asymmetric.json) | 64 | `0f5f9ae57c675ed524cc508c1791ff6f87fec60af90dd601b3ea8d8609b54883` |
| [`results/portfolio_round2_warm.json`](results/portfolio_round2_warm.json) | 4 | `1d0882e66e9de56cecee0276a894a56166a30ded9e7e30f3019e82b271a44744` |

The core and asymmetric searches took 333.85 and 280.98 seconds of
post-launch wall time, respectively, in the recorded environment.  The
files record Python, NumPy, platform, input paths, parameters, and the
SHA-256 of the public 41-point input.  The round-2 warm artifact additionally
records hashes of both round-2 input files.

## Reproduction and integrity checking

The recorded environment was macOS arm64, Python 3.14.6, and NumPy 2.5.1.
From the project root:

```sh
python3 -m venv /tmp/kissing5-round3-venv
/tmp/kissing5-round3-venv/bin/pip install \
  -r kissing_number_5/experiments/construction_round3/requirements.txt

/tmp/kissing5-round3-venv/bin/python -m unittest \
  kissing_number_5.experiments.construction_round3.test_manifold_augmented_lagrangian \
  -v
```

Replay the three portfolios:

```sh
PY=/tmp/kissing5-round3-venv/bin/python
MOD=kissing_number_5.experiments.construction_round3.manifold_augmented_lagrangian

$PY -m $MOD \
  --n 41 42 43 44 \
  --seeds 0 2026072300 2026072301 \
  --kinds random warm41 d6proj e6proj e7proj e8proj e6coordinate \
  --output /tmp/portfolio_core.json

$PY -m $MOD \
  --n 41 42 43 44 \
  --seeds 2026072302 2026072303 2026072304 2026072305 \
          2026072306 2026072307 2026072308 2026072309 \
  --kinds random warm41 \
  --output /tmp/portfolio_asymmetric.json

$PY -m $MOD \
  --n 41 42 43 44 --seeds 0 --kinds round2best \
  --output /tmp/portfolio_round2_warm.json
```

Elapsed times and platform strings make whole-file byte hashes
nondeterministic across machines.  On the pinned platform the optimization
seeds and all initialization choices are deterministic; final ulps can
still depend on the BLAS and elementary-function implementations.

Recompute all binary64 diagnostics and active graphs from the stored
coordinates:

```sh
$PY -m kissing_number_5.experiments.construction_round3.check_results \
  kissing_number_5/experiments/construction_round3/results/portfolio_core.json \
  kissing_number_5/experiments/construction_round3/results/portfolio_asymmetric.json \
  kissing_number_5/experiments/construction_round3/results/portfolio_round2_warm.json
```

[`check_results.py`](check_results.py) is an integrity checker only.  It
does not use directed rounding, exact arithmetic, or algebraic isolating
intervals, so it is deliberately not placed among the proof verifiers.

## Numerical-boundary warning

The active graph at tolerance \(\varepsilon\) contains pairs with

\[
\langle x_i,x_j\rangle\geq
\max_{k<\ell}\langle x_k,x_\ell\rangle-\varepsilon.
\]

It is not a graph of exact contacts at \(1/2\).  Counts of pairs above or
below \(\pm1/2\) are ordinary binary64 comparisons.  The near-zero Gram
eigenvalues follow mechanically from storing five coordinates and are not
a directed PSD or rank certificate.  All best objectives exceed \(1/2\) by
at least `0.01499`, so rounding cannot plausibly hide feasibility here, but
that observation supplies no bound on configurations outside the searched
basins.
