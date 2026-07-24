# Construction round 10: general rank-five metrics on finite root shells

## Status

**NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE.**

This round found no 41-, 42-, 43-, or 44-point configuration whose recomputed
maximum inner product is at most \(1/2\).  It produced no exact or
interval-certified candidate and does not change the rigorous bounds
\[
40\leq\tau(5)\leq44.
\]

The portfolio contains 120 structured runs: ten deterministic seeds for each
of \(N=41,42,43,44\) and each of the E6, D6, and D7 root shells.  Twelve of the
best structured images were then released into unrestricted coordinates and
polished.  A separate six-run audit challenged the discrete local minima by
exhaustively deleting one to three points from larger-cardinality outputs.

## Mechanism

For a shell \(R\subset\mathbb R^m\), the structured coordinates are
\[
x_r=\frac{rB}{\lVert rB\rVert},\qquad B\in\mathbb R^{m\times5}.
\]
Equivalently, \(BB^{\mathsf T}\) is a PSD metric of rank at most five.  The
five nonzero singular values of \(B\) are free, so this search strictly
contains orthogonal hyperplane projection as a special case.

Each trajectory alternates:

1. an exact-cardinality discrete subset heuristic on the entire mapped shell;
2. analytic-gradient smooth-minimax optimization of the general matrix \(B\);
3. fresh greedy deletion and one-swap challenges under the new metric.

The selected points are finally released from the common-map constraint,
given deterministic asymmetric perturbations, optimized on
\((S^4)^N\), and polished by direct epigraph SQP.  Both the continuous and
discrete stages are nonconvex heuristics.

## Results

The table gives the best structured value and the best value after
unrestricted refinement.  The last column compares the latter with the best
numerical value already stored elsewhere in this repository.

| \(N\) | best structured | unrestricted round-10 best | prior numerical best | round-10 gap above \(1/2\) |
|---:|---:|---:|---:|---:|
| 41 | 0.5424740979369884 | 0.5220692609969377 | 0.5149946525121668 | 0.0220692609969377 |
| 42 | 0.5420280931836461 | 0.5343035874522938 | 0.5182411558622623 | 0.0343035874522938 |
| 43 | 0.5680492861305548 | 0.5366600203477839 | 0.5247096018290212 | 0.0366600203477839 |
| 44 | 0.5679865766440254 | 0.5274711925362580 | 0.5274577123235323 | 0.0274711925362580 |

Thus round 10 sets no numerical record.  Its 44-point endpoint returns, to the
reported active graph and Gram spectrum, to the familiar round-4/5/6/9 basin.

The compact summary recomputes the literal binary64 maximizing pairs, stores
each maximum in decimal and hexadecimal floating representation, and records
the number of pairs within \(10^{-8}\) of that maximum.  For the best released
endpoints:

| \(N\) | binary64 maximum hex | literal maximizing pair(s) | \(10^{-8}\)-active edges |
|---:|:---|:---|---:|
| 41 | `0x1.0b4ca984751cep-1` | (1,39), (32,37) | 190 |
| 42 | `0x1.11903d647c74bp-1` | (17,25) | 188 |
| 43 | `0x1.12c51a28edc95p-1` | (2,20), (12,30) | 159 |
| 44 | `0x1.0e10b4430cfa5p-1` | (0,29) | 182 |

These are exact statements about the stored binary64 arrays, not exact
statements about real algebraic coordinates.

## Near-miss analysis

The direct 41-point E6 starts repeatedly converged to all 40 roots in the D5
slice plus one E6 half-root.  The metric has numerical singular values
\[
1.0396426442^4,\quad0.8225403877,
\]
and its \(10^{-8}\)-top graph is a 10-edge star with 30 isolated vertices.
This highly structured endpoint remains `0.0424740979` above the target.

More importantly, the structured 42-point search found a smaller value than
the direct 41-point search.  Exhaustive deletion from the 42-point output
immediately supplies a better structured 41-point child.  This explicitly
demonstrates a multi-swap trap in the discrete N=41 stage; it is not evidence
for a 41-point obstruction.  Reoptimizing and releasing the cross-cardinality
children returns the same weak unrestricted basins:

| target \(N\) | larger source | best final cross-cardinality value |
|---:|---:|---:|
| 41 | 42 | 0.5220692609969371 |
| 42 | 43 or 44 | 0.5423261445466410 |
| 43 | 44 | 0.5411611830417189 |

The N=43 released endpoint has one isolated vertex in its \(10^{-8}\)-active
graph.  This is another numerical reminder that local activity or jamming
cannot be assumed in a universal upper-bound proof.

## Reproduction

From the repository root, create an isolated environment and run:

```bash
python3 -m venv /tmp/kissing5-round10
/tmp/kissing5-round10/bin/pip install -r \
  experiments/construction_round10/requirements.txt

/tmp/kissing5-round10/bin/python -m \
  experiments.construction_round10.rank5_metric_subset_search \
  --n 41 42 43 44 --families E6 D6 D7 \
  --seeds 2026072400 2026072401 2026072402 2026072403 2026072404 \
          2026072405 2026072406 2026072407 2026072408 2026072409 \
  --alternations 3 --map-iterations 350 --polish-top 3 \
  --output \
  experiments/construction_round10/results/metric_subset_portfolio.json

/tmp/kissing5-round10/bin/python -m \
  experiments.construction_round10.cross_cardinality_challenge \
  experiments/construction_round10/results/metric_subset_portfolio.json \
  --output \
  experiments/construction_round10/results/cross_cardinality_challenge.json
```

The stored main artifact records Python 3.14.6, NumPy 2.5.1, SciPy 1.18.0,
and the macOS platform string.  Verify the arrays and regenerate the compact
summary with:

```bash
/tmp/kissing5-round10/bin/python -m \
  experiments.construction_round10.check_results \
  experiments/construction_round10/results/metric_subset_portfolio.json

/tmp/kissing5-round10/bin/python -m \
  experiments.construction_round10.check_cross_results \
  experiments/construction_round10/results/metric_subset_portfolio.json \
  experiments/construction_round10/results/cross_cardinality_challenge.json

/tmp/kissing5-round10/bin/python -m \
  experiments.construction_round10.analyze_portfolio \
  experiments/construction_round10/results/metric_subset_portfolio.json \
  --output experiments/construction_round10/results/portfolio_summary.json

/tmp/kissing5-round10/bin/python -m \
  experiments.construction_round10.extract_best_configurations \
  experiments/construction_round10/results/metric_subset_portfolio.json \
  --output \
  experiments/construction_round10/results/best_configurations.json

/tmp/kissing5-round10/bin/python -m unittest \
  experiments.construction_round10.test_rank5_metric_subset_search -v
```

The checkers independently re-enumerate the root shells, reconstruct every
structured image from its stored root indices and matrix, renormalize every
released coordinate array, recompute maxima and Gram spectra, and verify
coordinate hashes.  They certify internal consistency of the floating-point
artifacts only.

## Artifacts

- `results/metric_subset_portfolio.json`: all 120 structured and 12 released
  runs, coordinates, maps, histories, diagnostics, seeds, and environment;
- `results/portfolio_summary.json`: compact independently recomputed maxima,
  literal binary64 maximizers, hashes, and comparison with prior numerics;
- `results/best_configurations.json`: the four concrete best binary64
  coordinate arrays, one for each requested cardinality;
- `results/cross_cardinality_challenge.json`: all exhaustive deletion
  challenges and their reoptimized coordinates;
- `SHA256SUMS`: hashes for programs, tests, and result payloads;
- `RESEARCH_LOG.md`: timestamped decisions and failure analysis.

No result in this folder is used as a rigorous lower or upper bound.
