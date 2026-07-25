# Results: adaptive rank-aware BV search

## Status

**NUMERICAL BARRIER, NOT AN UPPER BOUND AND NOT A CODE.**

The corrected common-pair capacity hierarchy eliminates both imported
pseudodistributions, but reoptimization repairs the obstruction.  The
strongest well-resolved finite witness in this folder uses the seven-node
quarter grid, fixes the exact C039 pair masses, and reoptimizes all 51 triple
orbit masses.  It simultaneously passes:

- full-radial BV matrices through harmonic degree 16;
- ordinary pair moments through degree 60;
- all ten nontrivial C067 frame matrices;
- all 18 contiguous-band/exact-stratum capacity rows on this grid;
- both corrected pointwise weighted capacity rows, including positive-\(q\)
  contact capacity seven;
- exact rational outer bands for 27 C047/C065 kernels; and
- every corresponding sharp nonlinear centered-skew inequality when
  evaluated on the returned numerical masses.

The independent numerical checker, which imports no solver state, reports:

| quantity | quarter grid, BV 0–16 |
|---|---:|
| minimum active BV eigenvalue | `2.0167481630760174e-06` |
| minimum ordinary pair moment | `0.0015403744311606182` |
| minimum C067 frame eigenvalue | `0.00974574025010888` |
| minimum rank outer-band slack | `0.10286422514906622` |
| minimum sharp rank residual | `0.4109055867031327` |
| minimum stratified capacity slack | `0.0` |
| minimum weighted capacity slack | `23.41261235575225` |
| maximum marginal error | `2.913225216616411e-13` |
| minimum pair/triple mass | `0.4700957044 / 0.0652311220` |

The zero stratified slack is a capacity-zero boundary equality, not a
negative numerical tolerance.

The thirteen-node eighth-grid local refinement also returns a
simultaneously feasible numerical point through harmonic degree 16.  Its
independently recomputed figures are:

| quantity | eighth grid, BV 0–16 |
|---|---:|
| minimum active BV eigenvalue | `4.96278626464727e-11` |
| minimum ordinary pair moment | `0.002069141483278969` |
| minimum C067 frame eigenvalue | `0.009695278670385221` |
| minimum rank outer-band slack | `0.11606599992251959` |
| minimum sharp rank residual | `0.429888407765503` |
| minimum stratified / weighted capacity slack | `0.0 / 0.0` |
| maximum marginal error | `1.3216094885137863e-12` |

This second point is far too close to the BV boundary to rationalize from
the stored decimal masses.  It is useful only as evidence that support
refinement does not reveal an obvious contradiction.

Raising the fixed-pair quarter-grid calculation to degree 24 produced active
BV eigenvalues as small as `2.50e-09`, but the solver's reported common
margin was `-1.14e-06`.  That run is deliberately classified as
**inconclusive numerical evidence**, not feasibility.

## Exact adversarial audits

`audit_capacity_barriers.py` uses only `fractions.Fraction`.  It finds:

- C039 fails the exact stratum
  \(q=-1/4,b=1/2,p=2/3,M=3\), with normalized slack
  \[
  -\frac{1864186060539}{50000000000000}.
  \]
  The endpoint capacity is three, not two.
- The later five-node common-pair witness has minimum singleton-stratum
  slack \(-720/41\) at \(q=-9/100,b=499/1000\), and its corrected weighted
  inequality has slack \(-1248/41\).
- In particular, its named \(q=-11/25,b=499/1000,M=1\) stratum also fails:
  in unordered-count normalization \(n_{244}-E_2=219-131=88\).

Separately, `audit_common_pair_witness.py` proves with exact rational
arithmetic that the same five-node witness passes all 27 listed sharp
centered-skew kernel inequalities.  Its least residual among this family is
the Gram kernel \(H_1\):

\[
\frac{346957839801844443}{25000000000000000}>0.
\]

Thus the corrected capacity mechanism is genuinely independent of the
sampled rank-skew family.

## A locally excluded basin

The union of the thirteen eighth-grid nodes and the five irregular
common-pair-witness nodes has 18 nodes and 749 feasible triple orbits.
Constraining all 27 kernel variances to the simultaneous five-percent cells
around that witness, then imposing the corrected capacities and BV through
degree 8, gives numerical optimum

```text
-0.03683188267046746
```

for the common PSD/pair-moment margin.  CLARABEL reports `optimal`, and the
returned minimum active BV eigenvalue is `-0.036831888556397914`.  This
excludes only that finite support and simultaneous variance cell
numerically.  It is not a global result.

## Exact bottleneck

The present route does not numerically exclude mass 41.  The main barrier is
not merely the old five-node support:

1. a reoptimized quarter-grid measure survives corrected capacities, 27
   sharp rank tests, and full-radial BV through degree 16 with visible
   margin;
2. a substantially richer thirteen-node measure survives the same checks,
   albeit close to the BV boundary;
3. only finitely many harmonic degrees and 27 kernel combinations were
   tested; and
4. there is no theorem mapping an arbitrary continuous pair/triple measure
   to either atomic grid while preserving the inequalities with controlled
   error.

A plausible certificate architecture would partition the scalar variances
of a selected rank-kernel family into rational cells.  On each cell, rational
chords majorize the sharp \(V^{3/2}\) radius, making the centered-skew
conditions linear.  A continuous-domain dual would then combine:

- matrix-polynomial BV multipliers;
- a nonnegative multiplier measure for the pointwise base-stratum capacity
  domination;
- ordinary pair/frame multipliers; and
- cell-bound multipliers.

For a rigorous proof, every variance cell and the full continuous
\((u,v,t)\) domain must be covered, with exact PSD and polynomial
nonnegativity certificates.  The current atomic outputs provide no such
coverage theorem.  Any dual extracted only from these grids could be
violated between nodes.

## Reproduction

From `kissing_number_5/`:

```sh
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.continuous_rank_bv_search.test_search -v

PYTHONPATH=. .venv/bin/python \
  experiments/continuous_rank_bv_search/audit_capacity_barriers.py

PYTHONPATH=. .venv/bin/python \
  experiments/continuous_rank_bv_search/audit_common_pair_witness.py

PYTHONPATH=. .venv/bin/python \
  experiments/continuous_rank_bv_search/check_result.py \
  experiments/continuous_rank_bv_search/results/fixed_baseline_d16_stratified.json

PYTHONPATH=. .venv/bin/python \
  experiments/continuous_rank_bv_search/check_result.py \
  experiments/continuous_rank_bv_search/results/eighth_d16_local_stratified.json
```

Pinned discovery environment:

```text
Python 3.14
cvxpy 1.9.2
numpy 2.5.1
scipy 1.18.0
solver CLARABEL
```

The convex searches are deterministic and use no random seed.
