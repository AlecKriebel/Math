# Construction Round 5: population energy continuation

## Status

**NUMERICAL EVIDENCE ONLY — NOT A CONSTRUCTION CERTIFICATE OR AN UPPER
BOUND.**

This independent 30-run search found no 41-, 42-, 43-, or 44-point code
with maximum inner product at most \(1/2\).  Every best result remains at
least `0.0149946525` above the threshold, so neither high-precision
verification nor exact-coordinate reconstruction was triggered.

All final binary64 coordinates, seeds, population histories, crossover
assignments, active-edge lists, and Gram spectra are released.  The search
does not imply a lower bound on the best possible maximum inner product.

## Distinct search mechanism

This round is not another augmented-Lagrangian run or D5 deletion surgery.
It evolves a population of completely unrestricted \(N\)-point clouds on
\(S^4\).  For inner products \(s_{ij}\), each local island minimizes

\[
 E_p(X)=\frac1p\log\sum_{i<j}(1-s_{ij})^{-p}
\]

by exact-gradient L-BFGS.  As \(p\) grows, this converges to
\(-\log(1-\max s_{ij})\).  The initialization uses:

- fresh asymmetric Gaussian clouds;
- the exact D5 root configuration with maximin sampled holes added;
- perturbations of every best 41--44 numerical artifact available locally.

To cross two configurations, the second parent is aligned to the first by
all 32 sign choices of its covariance principal frame, Hungarian point
matching, and alternating orthogonal Procrustes refinement.  A child is
then produced by either a random-hyperplane row splice or extrapolating
blend, followed by tangent mutation.  The alignment is used only to define
the crossover: every child coordinate is released during relaxation.
Objective elites, one descriptor-diverse member, and a new random immigrant
are retained at each generation.

The main portfolio used powers

```text
1, 3, 9,
18, 37.4415088, 77.8814768, 162, 336.9735793, 700.9332912, 1458,
2916, 5832, 11664
```

with a population of 10, seven crossover generations, and seeds
`2026072330` through `2026072334` for each cardinality.  The focused 43/44
portfolio used population 12, nine generations, 220 L-BFGS iterations per
stage, and seeds `2026072335` through `2026072339`.  A direct epigraph SLSQP
solve was applied only as a final diagnostic.

## Results

| \(N\) | best round-5 maximum | gap above \(1/2\) | best seed | \(10^{-8}\) active edges |
|---:|---:|---:|---:|---:|
| 41 | 0.5149946525121668 | 0.0149946525121668 | 2026072330 | 153 |
| 42 | 0.5182411558622642 | 0.0182411558622642 | 2026072333 | 172 |
| 43 | 0.5247244770145403 | 0.0247244770145403 | 2026072330 | 172 |
| 44 | 0.5274711925359574 | 0.0274711925359574 | 2026072330 | 182 |

The \(N=41\) output is the known 35-point active-core basin with six
numerical rattlers.  Its active degree histogram is

```text
0^6 8^18 9^10 10^6 12^1.
```

At \(N=42\), seed `2026072333` made a genuine population escape: its best
maximum stayed at `0.5198232355737905` through power 700.9, fell to
`0.5188254164890519` after the power-1458 crossover generation, then
continued to `0.5182748628982106` before SLSQP reached the previously known
`0.5182411558622642` basin.  This calibrates the crossover's ability to
change basins, but it is not a new record.  The 43/44 focused runs did not
match the better public comparison values already documented in
[`../random_codes/RESULTS.md`](../random_codes/RESULTS.md).

The best round-5 contact diagnostics are:

| \(N\) | degree histogram at \(10^{-8}\) | component sizes | pairs below \(-1/2\) |
|---:|:---|:---|---:|
| 41 | \(0^6,8^{18},9^{10},10^6,12^1\) | \(35,1^6\) | 114 |
| 42 | \(0^2,3^1,6^4,7^4,8^7,9^{12},10^8,11^3,12^1\) | \(40,1^2\) | 121 |
| 43 | \(5^8,6^6,7^8,10^{20},12^1\) | \(43\) | 119 |
| 44 | \(6^4,7^4,8^{16},9^{16},10^4\) | \(44\) | 148 |

These are tolerance graphs relative to each configuration's own maximum,
not exact contact graphs at \(1/2\).

## Halfspace-depth diagnostic

The separate
[`tukey_probe_n41.json`](results/tukey_probe_n41.json) checks all 101,270
normals through four points of the best 41-point output.  Its shallowest
floating-point split is

```text
11 positive / 19 boundary / 11 negative.
```

Seventeen boundary residuals are around \(10^{-14}\), two are around
\(1.8\cdot10^{-11}\), and the next absolute dot product is about `0.49245`.
Thus the persistent near miss has a pronounced 11--19--11 layer direction;
it does not challenge the independently certified necessary Tukey-depth-six
condition for a hypothetical 41-code.  The enumeration is only a numerical
probe, because degeneracies and boundary signs have not been certified
exactly.

## Artifacts and integrity

| file | runs | SHA-256 |
|:---|---:|:---|
| [`population_portfolio.json`](results/population_portfolio.json) | 20 | `37ee2140585c18a329a00f79038a0d7bf9e9df51d7685405410ade2d32d58e82` |
| [`population_targeted_n43_n44.json`](results/population_targeted_n43_n44.json) | 10 | `ab26f6cd16a769bec4137983f766c9ba4af544ed0ad3b0491ed7563447ba3c81` |
| [`tukey_probe_n41.json`](results/tukey_probe_n41.json) | one probe | `5271520e08cc2187bb1f1851f36886895133f9d1951188c5e8ee9d8c9629081e` |

The recorded platform was macOS arm64, Python 3.14.6, NumPy 2.5.1, and
SciPy 1.18.0.  The main and focused searches took 120.85 and 66.67 seconds,
respectively.  Whole-file hashes include elapsed time and environment
strings; deterministic seeds do not guarantee identical final ulps across
BLAS implementations.

From the repository root, create the pinned environment and run tests:

```sh
python3 -m venv /tmp/kissing5-round5-venv
/tmp/kissing5-round5-venv/bin/pip install \
  -r kissing_number_5/experiments/construction_round5_population/requirements.txt

/tmp/kissing5-round5-venv/bin/python -m unittest \
  kissing_number_5.experiments.construction_round5_population.test_population_continuation \
  -v
```

Replay the main portfolio:

```sh
PY=/tmp/kissing5-round5-venv/bin/python
MOD=kissing_number_5.experiments.construction_round5_population.population_continuation
BASE=kissing_number_5/experiments

$PY -m $MOD --n 41 42 43 44 \
  --seeds 2026072330 2026072331 2026072332 2026072333 2026072334 \
  --population 10 --generations 7 --iterations 180 \
  --inherit \
    $BASE/construction_round3/results/portfolio_core.json \
    $BASE/construction_round3/results/portfolio_asymmetric.json \
    $BASE/construction_round3/results/portfolio_round2_warm.json \
    $BASE/construction_round4_surgery/results/contact_surgery_portfolio.json \
  --output /tmp/population_portfolio.json
```

Replay the focused batch by changing `--n 43 44`, the seeds to
`2026072335`--`2026072339`, and the parameters to
`--population 12 --generations 9 --iterations 220`.

Recompute every stored norm, maximum, Gram spectrum, negative-pair count,
active edge, and degree histogram independently:

```sh
$PY -m kissing_number_5.experiments.construction_round5_population.check_population \
  kissing_number_5/experiments/construction_round5_population/results/population_portfolio.json

$PY -m kissing_number_5.experiments.construction_round5_population.check_population \
  kissing_number_5/experiments/construction_round5_population/results/population_targeted_n43_n44.json
```

The checker is deliberately outside `verifiers/`: it uses ordinary
binary64 arithmetic and establishes artifact integrity only.  It neither
certifies feasibility nor excludes unsearched configurations.
