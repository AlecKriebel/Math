# Verification scope

Run from any directory:

`python3 verification/check.py`

The script uses only Python's standard library and deterministic input. Its
output is `result.json` (capture stdout yourself when replaying). It verifies:

* exact rational support/variance calculations for noisy response slices;
* numerical midpoint integration against the exact tangent-loss formulas;
* 700 rational order-statistic controls for the guarded-neighbor theorem;
* a counterexample to the same radius control when the guard is omitted;
* finite binomial tails and the exact rate-exponent algebra;
* weighted Gaussian characteristic-function factorization and cutoff bounds;
* a finite deterministic pilot localization control;
* the first twelve polynomial derivative recurrences behind the flat-jet proof.

No learning-curve simulation, full data experiment, external corpus or theorem
prover is used. Floating-point checks are sanity checks, not rigorous interval
certificates. The complete mathematical arguments are in `RESULT.md`; the
script does not establish current literature status or dimension-free noisy
consistency. The exact-control seed is recorded in source.
