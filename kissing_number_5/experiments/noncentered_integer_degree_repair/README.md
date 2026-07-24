# Exact repair of the noncentered integer-row obstruction

## Scope

This directory contains an exact rational mass-41 pair/triple
pseudodistribution.  It is **not** a spherical code and is **not** a
41-by-41 Gram matrix.  Its purpose is to prove that a broad collection of
pair/triple, local-cap, rank-moment, and finite-population row constraints
is still insufficient to prove \(\tau(5)\le40\).

The final source is `candidate_exact_6.json`.  It has seven rational
inner-product nodes and 51 positive triangle orbits.  The exact certificate
`all_harmonics_certificate_6.json` proves:

- every ordinary dimension-five Gegenbauer moment is positive;
- every full-radial Bachoc--Vallentin matrix is positive semidefinite;
- degrees \(1,\ldots,599\) and pair degrees \(1,\ldots,129\) are checked
  directly with rational arithmetic;
- explicit parity-limit perturbation bounds cover all remaining degrees.

The certificate `integer_row_mixture_6.json` gives 26 positive rational
integer degree-row atoms.  Their first moments and complete \(7\times7\)
second-moment matrix equal those induced by the pair/triple source exactly.
Every atom obeys the currently proved row constraints.  A dependency-free
enumerator checks that these are drawn from all 855,168 admissible integer
rows, rather than a guessed pool.

The consolidated verifier additionally checks:

- robust negative/positive mass, antipode, deep-edge, and local degree rows;
- 18 stratified and two weighted common-capacity inequalities;
- ten low-harmonic frame blocks by every principal minor;
- 27 sharp finite-rank cubic residuals.

## Reproduction

From the repository root:

```sh
PYTHONPATH=. python3 \
  experiments/noncentered_integer_degree_repair/verify_repaired_barrier.py
PYTHONPATH=. python3 -m unittest \
  experiments.noncentered_integer_degree_repair.test_repaired_barrier \
  tests.test_fixed41_bv_all_harmonics \
  tests.test_noncentered_integer_degree_mixture
```

The verifier uses `fractions.Fraction` throughout the proof-bearing path.
The floating JSON files and the search/cutting scripts record discovery
history only.

## What the certificate proves

It refutes the proposed implication

> all pair/two-rooted three-point harmonic inequalities, the recorded cap
> and frame inequalities, the 27 scalar sharp-rank inequalities, and every
> first/second integer row-degree moment imply nonexistence at mass 41.

The missing information is global common-source compatibility: overlapping
rooted flags, a global rank-five Gram realization, or a different universal
inequality that cannot be represented by these marginal constraints.
