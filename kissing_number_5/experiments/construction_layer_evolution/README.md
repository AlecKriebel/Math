# Latitude-layer and evolutionary construction search

Status: **NUMERICAL EVIDENCE ONLY — NOT A CONSTRUCTION CERTIFICATE**

This experiment maintains a two-sided construction challenge for
`N=41,42,43,44`.  It is deliberately separate from the split-point,
low-rank-deflation, and thermal searches elsewhere in the repository.

Its three macro mechanisms are:

1. two-to-eight unequal latitude layers around an axis, initialized by
   independently rotated and perturbed `S^3` subcodes and optimized with tied
   layer heights before all coordinates are released; a companion portfolio
   inherits the exact latitude decompositions of all four known 40-point
   codes (including the `D5` `(8,24,8)` decomposition), inserts new points in
   inherited or new layers, and then breaks the inherited symmetry;
2. evolutionary latitude-block crossover between the exact `D5`, `L5`, `Q5`,
   and `R5` 40-point codes and unrelated layer/random basins;
3. variable-cardinality `remove-k/add-(k+1)` moves for every `k=2,...,6`.
   Deletions are the largest blockers of a sampled insertion hole.  The
   `k+1` new points are jointly optimized against the retained core, after
   which all points are released.

No antipodality, symmetry, contact graph, or finite inner-product alphabet is
preserved after initialization.  The smooth searches use binary64 arithmetic.
Every saved endpoint is normalized again and audited from its coordinates by
an independent verifier.  A reported maximum above `1/2` is a near miss, not
a lower-bound construction.  If a run ever reports a value at or below
`1/2`, exact/algebraic reconstruction and interval verification are required
before the claim can move beyond numerical evidence.

## Production outcome

The consolidated deterministic seeds `2026072403` and `2026072404` made 96
free latitude starts, 64 source-decomposition layer starts, 24 unrelated
random starts, all 160 prescribed surgery moves, 56 heterogeneous crossovers,
152 equal-cardinality crossovers, 72 intergenerational literal-epigraph
polishes, and 48 final literal-epigraph polishes.  The independently
recomputed best maxima were

| `N` | maximum inner product | originating mechanism |
|---:|---:|---|
| 41 | 0.5155656485808731 | evolutionary latitude-block crossover |
| 42 | 0.5199641730896757 | free latitude-layer release |
| 43 | 0.5261397477047198 | evolutionary latitude-block crossover |
| 44 | 0.5274711925360355 | evolutionary latitude-block crossover |

All four exceed `1/2`, so this experiment found no new kissing configuration
and attempted no exact/algebraic reconstruction.  The 41-point near miss has
155 edges within `5e-4` of its maximum, a connected active graph with degree
histogram `{5:1, 6:5, 7:10, 8:20, 9:5}`, numerical Gram rank five, and frame
eigenvalues approximately
`(8.306041, 8.306041, 8.232763, 8.232763, 7.922393)`.

Several 42- and 43-point endpoints have isolated vertices in their active
graphs.  This is evidence of an optimization basin with an undersettled core,
not an obstruction theorem.  A broader command using seed `2026072404`,
16 layer starts, 10 crossovers, 3 generations, and 160-iteration
intergenerational polishing was killed by the shared host (exit 137) before
producing an artifact; it is not counted as a failed geometric attempt.

## Reproduce

From the repository root, using the pinned discovery environment:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 .venv/bin/python \
  experiments/construction_layer_evolution/layer_evolution_search.py \
  --seed 2026072401 \
  --layer-starts 8 --layer-counts 2,3,4,5,6,7,8 \
  --layer-minimum 1 --source-layer-starts 2 --random-starts 3 \
  --crossovers 6 --generations 2 --population 8 \
  --rotation-trials 80 --hole-samples 3500 \
  --max-iterations 100 --evolution-polish-iterations 120 \
  --output experiments/construction_layer_evolution/portfolio_single_seed.json

# The exact production arguments for each retained seed are stored under
# command_arguments in the two seed portfolios.  After reproducing them:
.venv/bin/python \
  experiments/construction_layer_evolution/consolidate_portfolios.py \
  experiments/construction_layer_evolution/portfolio_seed_2026072403.json \
  experiments/construction_layer_evolution/portfolio_seed_2026072404.json \
  --output experiments/construction_layer_evolution/portfolio.json

.venv/bin/python \
  experiments/construction_layer_evolution/verify_portfolio.py \
  experiments/construction_layer_evolution/portfolio.json \
  --write-report experiments/construction_layer_evolution/verification_report.json

.venv/bin/python -m unittest \
  experiments/construction_layer_evolution/test_layer_evolution.py \
  experiments/construction_layer_evolution/test_verify_portfolio.py
```

`verification_report.json` records the SHA-256 digest of the exact portfolio
bytes.  The verifier reconstructs all four 40-point parents in exact rational
arithmetic and independently recomputes every saved maximum, coordinate hash,
Gram and frame spectrum, pair quantile, and active graph.  It does not import
the discovery program.  It also checks the hashes of both constituent seed
portfolios.  `ARTIFACT_HASHES.txt` pins the principal search, result, and
verification artifacts.
