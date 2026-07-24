# History-biased high-temperature construction search

Status: **NUMERICAL EVIDENCE ONLY — no threshold configuration was found.**

## Outcome

Eight deterministic high-temperature population runs covered
\(N=41,42,43,44\).  Every run drove the inherited near-maximum graph overlap
to zero before quenching, so the experiment did not merely make local
perturbations inside the recorded basins.  Nevertheless, no quenched
candidate improved its starting record:

| \(N\) | inherited and retained best |
|---:|---:|
| 41 | 0.51499465251216603 |
| 42 | 0.51824115586226238 |
| 43 | 0.52470960182901927 |
| 44 | 0.52745771232353222 |

These are binary64 scans, not exact-real claims.  No array reached \(1/2\),
and this finite failure implies no upper bound.

## Mechanism

For unit rows \(X=(x_1,\ldots,x_N)\), the unmodified target energy is the
literal kissing-threshold hinge

\[
 E(X)=\sum_{i<j}\max(\langle x_i,x_j\rangle-1/2,0)^2.
\]

Each population walker follows Riemannian Euler–Maruyama steps on this
energy.  During hot stages, the objective also includes a temporary
history-dependent penalty on every edge in the inherited near-maximum graph:

\[
 b\sum_{ij\in E_0}
 \max\bigl(\langle x_i,x_j\rangle-(m_0-\delta),0\bigr)^2.
\]

The bias is then reduced to zero.  Noise combines independent tangent fields
with periodic coherent neighborhood kicks.  At each stage, population
resampling retains both the lowest threshold-energy walkers and the walkers
least similar to the inherited graph.  All twelve walkers retained distinct
quantized-Gram fingerprints at every recorded stage.

This differs from the earlier four-replica local-kick calculation: it uses
population annealing, stochastic gradient dynamics, explicit history bias,
coherent graph moves, and diversity resampling.  It is intentionally capable
of destroying the known graph rather than merely equilibrating around it.

After cooling, six archive representatives per run are polished by direct
epigraph SQP with all-pair constraint generation.  The working set contains
the 240 largest pairs; after each solve every pair is rescanned and the
working set is replaced.  This reduced dense solver memory under concurrent
machine load.  Returned arrays are always evaluated by a literal full-pair
scan, regardless of solver status.

## Deterministic portfolio

The mild/strong seeds were:

```text
N=41  2026075100  2026075101
N=42  2026075200  2026075201
N=43  2026075300  2026075301
N=44  2026075400  2026075401
```

Each run used 12 walkers, seven temperature stages, and six polished archive
states.  The mild schedule used history-bias coefficients
`4,4,2,0.5,0,0,0`; the strong schedule used
`12,12,6,2,0,0,0`.  Full temperatures, step sizes, noise scales, and step
counts are stored in `thermal_portfolio.json`.

The best non-inherited quenched maxima were:

| \(N\) | mild | strong |
|---:|---:|---:|
| 41 | 0.5170891098968629 | 0.5217824144158912 |
| 42 | 0.5241712212676627 | 0.5276834140636067 |
| 43 | 0.5273411070040114 | 0.5312651145729301 |
| 44 | 0.5368719389365934 | 0.5394632263025694 |

Some constraint-generation quenches collapsed rows and returned a maximum of
one.  Those failures are retained explicitly in the JSON and never selected.
They do not affect the independently rescanned minima.

For every run, the minimum Jaccard similarity between a population graph and
the inherited graph was exactly zero.  Final polished Gram matrices differed
from the inherited labeled Gram matrices by as much as 1.79–2.00 in maximum
entry, confirming large basin traversal.  These diagnostics show that the
negative result is not merely local stationarity; they do not establish
search completeness.

## Reproduction and verification

The recorded discovery environment is Python 3.14.6, NumPy 2.5.1, and SciPy
1.18.0.  The complete run can be reproduced from the repository root with:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
PYTHONPATH=. ./.venv/bin/python \
  experiments/four_point_depth_projection/construction_homotopy_deflation/thermal_population_escape.py \
  --n 41 42 43 44 --regimes mild strong \
  --population-size 12 --polish-count 6 --max-iterations 1600 \
  --seed-base 2026075100 \
  --output experiments/four_point_depth_projection/construction_homotopy_deflation/thermal_portfolio.json

/usr/bin/python3 \
  experiments/four_point_depth_projection/construction_homotopy_deflation/thermal_verify.py \
  experiments/four_point_depth_projection/construction_homotopy_deflation/thermal_portfolio.json \
  --output experiments/four_point_depth_projection/construction_homotopy_deflation/thermal_verification.json

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
PYTHONPATH=experiments/four_point_depth_projection/construction_homotopy_deflation \
  ./.venv/bin/python -m unittest -v thermal_tests
```

The production trajectories were executed as four per-cardinality jobs under
machine memory pressure; their elapsed times sum to 114.72 seconds.  The
seed rule and schedules are identical to the one-command reproduction above.

`thermal_verify.py` uses only the Python standard library.  It checks the
warm-source SHA-256, seed rule, every baseline/candidate/best coordinate
hash, every pairwise maximum, threshold energy, violating-pair count, run and
global threshold flags, and consolidated minimum selection.  It deliberately
does not certify stochastic trajectory histories or solver optimality.
Seven regression and tamper tests pass.

Principal artifact SHA-256 hashes:

```text
thermal_population_escape.py  141b92a649bf2591fa571639f6dba94ecac7aaa790c55e2028d97b3790878486
thermal_consolidate.py         4ecac407da731e8604fd08ef9f8f06b415a241dc47aaf458b3980f79cd1bae0f
thermal_portfolio.json         ba03880c9e0d988320e345fb4271f3cd3eecf48d46491662bf455bcb25c194f7
thermal_verify.py              2eade51e2ffad0f6653dbf8f8b90d4154a7851c78a47f794399d2ca3b986a992
thermal_verification.json      887595f8799ffa59769e3452abeff276c671c37707d16fcc314ba53bdfd5e2e9
thermal_tests.py               ae1d1090e3c819d99be091583483a13ed1922cd42d60022e3dfcf35dc4fda402
```

No exact or interval reconstruction was triggered because every candidate
remained above \(1/2\).

## Safe staging scope

The seven `thermal_*` files in this folder are safe to stage together:

- `thermal_population_escape.py`
- `thermal_consolidate.py`
- `thermal_portfolio.json`
- `thermal_verify.py`
- `thermal_verification.json`
- `thermal_tests.py`
- `thermal_report.md`

No file outside this isolated folder was modified by this mechanism.
