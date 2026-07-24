# Split-Homotopy Construction Audit

Status: **NUMERICAL EVIDENCE ONLY**

This construction round did not find a code with maximal inner product at most
`1/2`, and it did not improve the repository's incumbent numerical objective at
any of `N = 41, 42, 43, 44`.

## Scope and sources

The search starts independently from four exact, materially distinct
40-point codes.  A stored rational row `q` represents the unit vector
`q / sqrt(2)`.  The generator verifies exactly that `q.q = 2` and that
`q.r <= 1` for distinct rows.

| Source | Exact off-diagonal `q.r` histogram |
|---|---|
| D5 | `{-2:20, -1:240, 0:280, 1:240}` |
| L5 | `{-2:12, -3/2:32, -1:192, -1/2:32, 0:272, 1:240}` |
| Q5 | `{-2:10, -8/5:30, -1:180, -3/5:60, 0:250, 2/5:10, 1:240}` |
| R5 | `{-2:6, -8/5:30, -3/2:20, -1:144, -3/5:60, -1/2:28, 0:242, 2/5:10, 1:240}` |

Each source has 240 contact pairs.  The differing exact histograms certify
that the four source Gram matrices are not permutation-equivalent.

## Search mechanism

For `N = 40 + k`, the search selects `k` distinct parents and replaces each
selected point `x` by

`cos(theta/2) x + sin(theta/2) u` and
`cos(theta/2) x - sin(theta/2) u`,

where `u` is an asymmetric seeded tangent direction at `x`.  Variant 0 begins
with a maximum-contact-degree parent and variant 1 with a minimum-degree
parent; later parents are selected by a seeded contact-spread rule.

The deterministic angular schedule is

`[0.06, 0.16, 0.30, 0.48, 0.68, 0.86, 1.02, 1.14]`.

The released source-contact-neighborhood radii are

`[0, 0, 1, 1, 2, 2, 3, all]`.

At each stage the program optimizes the literal epigraph variable for the
largest pairwise inner product, subject to unit-norm constraints and the exact
numerical child-pair equation `child_plus.child_minus = cos(theta)`.  The last
stage releases every coordinate.  A final solve then removes all split-pair
equations and directly optimizes all coordinates.  No smooth approximation to
the maximum defines the objective.

There are 32 paths: four sources, four target cardinalities, and two variants.
The source indices are `D5=0`, `L5=1`, `Q5=2`, and `R5=3`, and the seed is

`2026075100 + 10000*source_index + 100*N + variant`.

The primary run used 140 iterations per constrained stage and 700 iterations
for the final unrestricted stage.  Its recorded wall time was 517.33 seconds.
The best source/cardinality endpoint was subsequently polished for 1200
unrestricted iterations.

## Best result for every source and cardinality

These are the independently re-scanned objectives after the final selected
endpoint polish.

| Source | N | Seed | Variant | Maximum inner product |
|---|---:|---:|---:|---:|
| D5 | 41 | 2026079200 | 0 | 0.5220692609969411 |
| D5 | 42 | 2026079301 | 1 | 0.5351560693764887 |
| D5 | 43 | 2026079400 | 0 | 0.5336181647238063 |
| D5 | 44 | 2026079500 | 0 | 0.5410641543041940 |
| L5 | 41 | 2026089201 | 1 | 0.5213989457472720 |
| L5 | 42 | 2026089301 | 1 | 0.5296784463998796 |
| L5 | 43 | 2026089401 | 1 | 0.5378019985263308 |
| L5 | 44 | 2026089500 | 0 | 0.5404088455748086 |
| Q5 | 41 | 2026099201 | 1 | 0.5208561441862484 |
| Q5 | 42 | 2026099300 | 0 | 0.5275602391804728 |
| Q5 | 43 | 2026099400 | 0 | 0.5345699953677956 |
| Q5 | 44 | 2026099500 | 0 | 0.5382614322685925 |
| R5 | 41 | 2026109200 | 0 | 0.5208561441862484 |
| R5 | 42 | 2026109300 | 0 | 0.5239828168088867 |
| R5 | 43 | 2026109401 | 1 | 0.5322613968039385 |
| R5 | 44 | 2026109501 | 1 | 0.5407921733003946 |

Only the selected R5, `N=42` endpoint improved during the additional polish:
from `0.5239867985216462` to `0.5239828168088867`.

## Global winners within this round

| N | Source | Seed / variant | Parents | Objective | Active pairs at `1e-8` | Gram positive spectrum |
|---:|---|---|---|---:|---:|---|
| 41 | Q5 | 2026099201 / 1 | `[12]` | 0.5208561441862484 | 190 | `8.017702888109881, 8.245574277972517, 8.245574277972528, 8.245574277972533, 8.245574277972555` |
| 42 | R5 | 2026109300 / 0 | `[8,7]` | 0.5239828168088867 | 155 | `8.079522084057242, 8.252673158023784, 8.355291406778099, 8.518277071385874, 8.794236279755017` |
| 43 | R5 | 2026109401 / 1 | `[0,38,16]` | 0.5322613968039385 | 163 | `8.278498291439748, 8.331701083468987, 8.661894629789423, 8.701850173485067, 9.026055821816779` |
| 44 | Q5 | 2026099500 / 0 | `[8,7,25,32]` | 0.5382614322685925 | 177 | `8.055345084022235, 8.660727758256940, 8.947668186163797, 9.020108182810752, 9.316150788746290` |

The maximum absolute Gram eigenvalue outside the five-dimensional positive
part is at most `3.85e-15` for these four stored coordinate arrays.

The corresponding binary64 coordinate hashes are:

| N | SHA-256 |
|---:|---|
| 41 | `e8ec9f934be2716d144569f49a034322733b6ff6f0d427e5dbdb024637022cfb` |
| 42 | `462fbc6280db5d89fca6358be961a999efa028c6232156af39e6e2b32d131b99` |
| 43 | `b600879dfc0f12ab075ec4458370d55aa8dacffad4f932c34ed0ae8d024405c5` |
| 44 | `d4daca4e4fab4a94916de9e7aedf9404fe2968edb848284183ef0eafd3bffb0b` |

## Comparison with repository incumbents

| N | Split result | Prior global record | Excess over record |
|---:|---:|---:|---:|
| 41 | 0.5208561441862484 | 0.5149946525121660 | 0.005861491674082342 |
| 42 | 0.5239828168088867 | 0.5182411558622623 | 0.0057416609466244273 |
| 43 | 0.5322613968039385 | 0.5247096018290192 | 0.0075517949749193125 |
| 44 | 0.5382614322685925 | 0.5274577123235322 | 0.010803719945060242 |

Thus no source/cardinality beat the global record.  In particular, no
candidate reached the required threshold `<= 0.5`.

As a weaker basin-diversity check, sorted off-diagonal Gram descriptors of the
16 polished source/cardinality endpoints were compared against 438 coordinate
arrays found in 22 prior construction JSON files outside this folder.  Every
stored endpoint was distinct from that inventory.  The closest prior
descriptor to each round winner had RMS/max discrepancy:

| N | RMS | Maximum |
|---:|---:|---:|
| 41 | 0.060619171028006555 | 0.2442766600089211 |
| 42 | 0.04910382073653482 | 0.15575660157137805 |
| 43 | 0.009542354120826864 | 0.037136169773920424 |
| 44 | 0.012743159414247666 | 0.04350958018994522 |

This establishes only novelty relative to stored arrays, not mathematical
novelty relative to unstored searches or the literature.

## Solver and independent-verifier audit

The environment was Python 3.14.6, NumPy 2.5.1, SciPy 1.18.0, on
macOS 26.5.2 arm64.

Of 256 constrained stage solves, 236 reported success.  Twenty late-stage
solves reached the iteration limit; their largest split-equation residual was
`4.8194e-5`.  These statuses are not treated as certificates.  All 32 final
unconstrained releases reported success, as did all 16 selected endpoint
polishes.

The independent verifier does not import discovery code.  It:

- reconstructs and exactly checks all four rational source codes and their
  histograms;
- re-normalizes and scans every stored coordinate array;
- recomputes SHA-256 hashes, maximal pairs, Gram spectra, contact graphs,
  connected components, and degree data;
- checks source/cardinality best-selection claims; and
- reports whether any endpoint reaches `1/2`.

Both the full 32-run portfolio and the compact 16-polish artifact pass that
verifier.  Six independent unit tests also pass:

- exact source diagnostics;
- rank-five diagnostics;
- monotone neighborhood release;
- deterministic distinct parent selection;
- partial epigraph preservation of the split-pair equation; and
- the prescribed initial child-pair separation.

Nothing here is an exact construction certificate: all endpoints violate the
kissing constraint by margins much larger than floating-point uncertainty.

## Reproduction

From the repository root:

```sh
PY=./.venv/bin/python
DIR=experiments/four_point_depth_projection/construction_homotopy_deflation

$PY $DIR/split_homotopy_search.py \
  --n 41 42 43 44 \
  --sources D5 L5 Q5 R5 \
  --variants 2 \
  --base-seed 2026075100 \
  --stage-iterations 140 \
  --final-iterations 700 \
  --output $DIR/split_portfolio.json

$PY $DIR/split_extract_best.py \
  $DIR/split_portfolio.json \
  --output $DIR/split_best_configurations.json

$PY -m experiments.four_point_depth_projection.construction_homotopy_deflation.split_polish_selected \
  $DIR/split_best_configurations.json \
  --iterations 1200 \
  --output $DIR/split_polished_best.json

$PY $DIR/split_verify.py \
  $DIR/split_portfolio.json \
  --output $DIR/split_verification.json

$PY $DIR/split_verify.py \
  $DIR/split_polished_best.json \
  --output $DIR/split_polished_verification.json

$PY $DIR/split_compare_inventory.py \
  $DIR/split_polished_best.json \
  --repository . \
  --output $DIR/split_inventory_comparison.json

$PY -m unittest \
  experiments.four_point_depth_projection.construction_homotopy_deflation.split_tests \
  -v
```

Key artifact hashes:

| Artifact | SHA-256 |
|---|---|
| `split_portfolio.json` | `f5948f966bc5441920e4dde7bbc13529c3d1f428933b868479ea3cf39ce48e1f` |
| `split_polished_best.json` | `639cf6516b005a1e7ebc1db98aace782a3da98de3e8403c839b3d398534127b0` |
| `split_verification.json` | `31f0cb7707d4d3bc06da3cc13f86dd22de3dcc27e2296ef89e00e768349c13f0` |
| `split_polished_verification.json` | `047cefe0cabf5299ed02a3bf4e0d9410c8beefc1cef75333dc3918ec1ea9d980` |
| `split_inventory_comparison.json` | `6b2d12b6d6ac583404142d067dd90e30071aa97facd672938f9533137ea745ef` |

## Safe-to-stage files

- `split_homotopy_search.py`
- `split_portfolio.json`
- `split_verify.py`
- `split_verification.json`
- `split_tests.py`
- `split_extract_best.py`
- `split_best_configurations.json`
- `split_polish_selected.py`
- `split_polished_best.json`
- `split_polished_verification.json`
- `split_compare_inventory.py`
- `split_inventory_comparison.json`
- `split_report.md`

No file outside this isolated folder was modified, and no commit was made.
