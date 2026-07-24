# Deterministic alternating-Gram construction audit

Status: **NUMERICAL EVIDENCE ONLY — no 41–44 point kissing
configuration was found.**

## Scope

This experiment is a construction search, not an upper-bound argument.  It
uses no symmetry assumption.  Its iterates alternate between:

1. the diagonal-one/off-diagonal half-space constraints
   \(G_{ii}=1,\ G_{ij}\leq 1/2\), using clipping, weighted active corrections,
   and optional Dykstra residual memory; and
2. the nonconvex set of PSD matrices of rank at most five, using spectral
   truncation followed by positive diagonal congruence normalization.

When progress stagnates, a seeded random block of high off-diagonal entries is
lowered simultaneously and the result is reprojected.  Thus the perturbations
act in Gram-entry space and break many active constraints at once.  This
mechanism is distinct from the repository's smooth epigraph/max-inner-product
optimizers.

The projection method is heuristic: alternating projection onto a nonconvex
rank set has no completeness guarantee, and failure to find a code proves no
upper bound.

## Coordinate inventory

`gram_inventory.py` recursively inspected all five-dimensional \(N=41,\ldots,44\)
coordinate arrays in `experiments/construction*/results/*.json`, plus the
standalone 41-point text file.  It recomputed norms, Gram matrices, spectra,
active graphs, and hashes without trusting stored objective metadata.

It found 312 coordinate occurrences representing 276 distinct normalized
binary64 arrays.  Six-dimensional compression results were excluded by the
shape rule.  The strongest warm starts were:

| \(N\) | recomputed maximum | selected source |
|---:|---:|---|
| 41 | 0.51499465251216603 | `experiments/input/spherical_codes_5_41.txt` |
| 42 | 0.51824115586226238 | round 9 core-rattler, `runs[1].best` |
| 43 | 0.52472447701452274 | round 9 core-rattler, `runs[2].best` |
| 44 | 0.52747119253595742 | round 6 bundle, `runs[19].best` |

The N=44 coordinate array also occurs in earlier artifacts; the inventory JSON
uses the lexicographically first tied occurrence, while the search deliberately
loads the round 6 occurrence.  Their normalized coordinate hashes agree.

## Production search

Command, from the repository root:

```text
./.venv/bin/python experiments/four_point_depth_projection/construction_active_search/gram_search.py \
  --n 41 42 43 44 \
  --restarts 20 \
  --iterations 5000 \
  --seed-base 2026072300 \
  --kick-period 240 \
  --checkpoint-period 1000 \
  --output experiments/four_point_depth_projection/construction_active_search/gram_search_results.json
```

The seed formula is

\[
  2026072300+100(N-41)+r,\qquad 0\leq r<20.
\]

Thus the four seed ranges are 2026072300–2026072319,
2026072400–2026072419, 2026072500–2026072519, and
2026072600–2026072619.  All five schedules defined in `gram_search.py` were
used four times for each cardinality.  The run performed 400,000 spectral
projection iterations and took 187.06 seconds in the recorded environment.

No restart strictly beat its cardinality's stored baseline.  No recomputed
maximum was at most \(1/2\).  Three over-relaxed N=41 restarts continued to
improve after hundreds or thousands of iterations, so the implementation was
not merely returning every perturbed initial condition; their minima were
still between 0.5180555 and 0.5180737.

## Independently recomputed final data

The best result for each cardinality is therefore its warm start:

| \(N\) | maximum | violating pairs | violation \(L^2\) | near-max edges |
|---:|---:|---:|---:|---:|
| 41 | 0.51499465251216603 | 171 | 0.18569883046441427 | 153 |
| 42 | 0.51824115586226238 | 208 | 0.25318569398374190 | 173 |
| 43 | 0.52472447701452274 | 214 | 0.33415175264925806 | 172 |
| 44 | 0.52747119253595742 | 214 | 0.39690309890619770 | 182 |

Here “near-max” means within \(10^{-8}\) of that configuration's maximum,
not within \(10^{-8}\) of \(1/2\).

The nonzero Gram spectra, in ascending order, are:

- N=41:
  \(7.892099139799012,\ 7.978755189667493,\ 7.978755189667493,\
  8.186173294652813,\ 8.964217186213187\).
- N=42:
  \(7.897396266328203,\ 8.028965556568080,\ 8.500063220041064,\
  8.680341958086068,\ 8.893232998976588\).
- N=43:
  \(8.398831498874182,\ 8.411565372183215,\ 8.411565372183519,\
  8.411565372184370,\ 9.366472384574730\).
- N=44:
  \(8.591207584335590,\ 8.638240736552044,\ 8.638240736552046,\
  9.059275580015976,\ 9.073035362544351\).

The largest absolute null-spectrum values were respectively
\(2.99,4.04,3.42,3.43\) times \(10^{-15}\).  The near-max active-graph
component sizes were:

- N=41: \(35,1,1,1,1,1,1\);
- N=42: \(40,1,1\);
- N=43: \(43\);
- N=44: \(44\).

Full degree histograms, coordinates, per-run objectives, checkpoints, source
hashes, and coordinate hashes are stored in `gram_search_results.json`.

## Verification

Run:

```text
./.venv/bin/python experiments/four_point_depth_projection/construction_active_search/gram_verify.py
./.venv/bin/python experiments/four_point_depth_projection/construction_active_search/gram_tests.py -v
```

The verifier independently reconstructs every final Gram matrix from the
stored coordinates and checks unit norms, all pairwise products, the rank-five
null spectrum, PSD tolerance, violation counts and norms, active graph data,
coordinate hashes, source-file hashes, seed formulas, and threshold booleans.
It does not import the projection implementation.  All seven regression and
tamper tests pass.  A separate full 5,000-iteration replay of N=41 restart 4,
seed 2026072304, exactly reproduced best iteration 4381, maximum
0.5180555052478174, and coordinate hash
`beb69f93e9135d0724c24a9575043e140322e07ba1af5ccec29bf02f043a060d`.

Artifact SHA-256 hashes at verification time:

- `gram_search_results.json`:
  `a0263ef3efa3591fbbd78fdbb8d86e2a82987aa1a7b4e3ac645690d7ed569fcc`;
- `gram_inventory.json`:
  `dcb622950e9d5c2a4711baf6f04be8df3cbb6512b7972a124581ce2b9edef504`;
- `gram_verification.json`:
  `39f0273be154325fc89840699e11f7a010ec43ef143ce68c6de25957d9fea739`.

Since no threshold candidate was found, no exact-coordinate certificate was
produced.
