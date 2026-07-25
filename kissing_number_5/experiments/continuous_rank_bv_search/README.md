# Continuous-support rank-aware BV discovery search

## Scope

This folder contains a discovery-only atomic approximation to the
fixed-cardinality \(N=41\) two-/three-point problem.  It was created to avoid
overlearning the historical five-node support.  The default grid has thirteen
rational nodes

\[
 -1,-7/8,\ldots,3/8,1/2,
\]

and 297 determinant-feasible unordered triple orbits.  The script can bisect
intervals adjacent to active pair atoms, giving a nested adaptive refinement,
or use the full 25-node sixteenth grid.

The model imposes:

- exact mass and fixed-cardinality marginal equations;
- nonnegative atomic pair and triple measures;
- the basis-free, full-radial Bachoc--Vallentin coefficient matrix
  \(W_k\succeq0\) at every requested harmonic degree;
- ordinary dimension-five Gegenbauer pair inequalities;
- all ten nontrivial low-harmonic frame-potential matrix inequalities C067;
- centered-skew rank cuts C047/C065 for 27 low-harmonic kernels;
- every contiguous-band common-pair capacity cut on the grid, including
  singleton exact-stratum cuts.  At the delicate endpoint \(p=2/3\), the
  capacity is three; and
- the corrected pointwise weighted capacity integral for every represented
  high threshold.  At contact threshold \(b=1/2\), positive base inner
  products use the universal cap seven rather than being silently omitted.

For a kernel of rank bound \(r\), let \(V,D\) be its centered second and
third trace moments.  The exact condition is

\[
 r(r-1)D^2\le (r-2)^2V^3.
\]

When pair masses are fixed, the program uses a rational constant band just
outside the exact square-root radius.  When pair masses are free, it derives
an exact mass-only rational bound \(V\le U\), then uses a rational slope
\(s\) satisfying

\[
 s^2r(r-1)\ge (r-2)^2U.
\]

Consequently \(|D|\le sV\) is a globally valid outer relaxation on
\(0\le V\le U\).  These rational secants are deliberately conservative.
The output separately evaluates every *sharp* nonlinear rank residual, so a
numerical pseudo-witness is accepted only if those stronger inequalities
also pass.

The `local-baseline` mode lets the thirteen-node pair masses vary while
placing each kernel variance in the rational interval
\([19V_0/20,21V_0/20]\) around the exact all-harmonic baseline value.  The
rank radius is then majorized by the rational chord through upward-rounded
endpoint radii.  This is a valid search over that simultaneous variance
cell, but it is not a cover of all possible pair measures.

The numerical findings and exact bottleneck are summarized in
[`RESULTS.md`](RESULTS.md).

## Reproduction

From `kissing_number_5/`:

```sh
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.continuous_rank_bv_search.test_search -v

PYTHONPATH=. .venv/bin/python \
  experiments/continuous_rank_bv_search/search.py \
  --grid eighth --harmonic-degree 10 --pair-degree 30 \
  --kernel-profile rich --pair-mode free \
  --output experiments/continuous_rank_bv_search/results/eighth_d10.json
```

A nested adaptive refinement is generated from an existing result with:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/continuous_rank_bv_search/search.py \
  --adaptive-from \
    experiments/continuous_rank_bv_search/results/eighth_d10.json \
  --harmonic-degree 10 --pair-degree 30 \
  --kernel-profile rich --pair-mode free \
  --output experiments/continuous_rank_bv_search/results/adaptive_d10.json
```

The older seven-node pair measure can be stress-tested while reoptimizing
all triple masses:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/continuous_rank_bv_search/search.py \
  --grid quarter --harmonic-degree 16 --pair-degree 60 \
  --kernel-profile rich --pair-mode fixed-baseline \
  --output \
    experiments/continuous_rank_bv_search/results/fixed_baseline_d16_stratified.json
```

The independent exact common-pair-capacity pseudodistribution is audited
against all 27 kernels, then can seed the union of its five irregular nodes
with the eighth grid:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/continuous_rank_bv_search/audit_common_pair_witness.py

PYTHONPATH=. .venv/bin/python \
  experiments/continuous_rank_bv_search/audit_capacity_barriers.py

PYTHONPATH=. .venv/bin/python \
  experiments/continuous_rank_bv_search/search.py \
  --grid eighth --harmonic-degree 8 --pair-degree 40 \
  --kernel-profile rich --pair-mode local-warm \
  --warm-from certificates/common_pair_capacity_degree4_pseudodistribution.json \
  --output \
    experiments/continuous_rank_bv_search/results/common_union_d8_stratified.json
```

Each stored floating-point result can be recomputed without CVXPY:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/continuous_rank_bv_search/check_result.py \
  experiments/continuous_rank_bv_search/results/fixed_baseline_d16_stratified.json
```

## Interpretation

Every output is labeled `NUMERICAL EVIDENCE ONLY`.  Solver infeasibility
does not prove a continuous-support theorem, and feasibility produces only
pair/triple marginals, not coordinates or a rank-five Gram matrix.  A genuine
upper bound would still require either:

1. a polynomial dual valid on the whole continuous domain, including the
   sharp nonlinear rank region; or
2. a finite subdivision theorem proving that all pair-variance cells and all
   support cells have been covered.
