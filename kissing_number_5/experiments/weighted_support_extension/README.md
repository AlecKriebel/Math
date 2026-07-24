# Weighted-support endpoint: six points

This folder isolates one exact boundary stratum of the weighted spherical
two-design branch.

## Certified statement

If the positive support has exactly six points, then all six weights are
\(1/6\) and the support is a regular simplex.  Every further kissing-code
point lies in at least one of six caps of height
\[
\rho=\frac{5+\sqrt{15}}{20}.
\]
The equality pattern in the cap-cover lemma is also determined exactly.

The mathematical proof is in `regular_simplex_extension.md`; the small
standard-library verifier checks the quadratic-field arithmetic and every
vertex case.

Run:

```bash
python3 experiments/weighted_support_extension/verify_simplex_negative_coordinate.py
python3 -m unittest experiments.weighted_support_extension.test_simplex_negative_coordinate
shasum -a 256 -c experiments/weighted_support_extension/MANIFEST.sha256
```

The test suite runs both the valid verifier and a tampered value under
`python -O`.  All proof-critical checks use always-on exceptions.

## Status boundary

This does **not** bound the total number of extension points and does not
resolve the weighted branch.  `simplex_chamber_cap_scan.json` is retained
only as a reproducibility record of a floating-point solver failure.  It is
not a certificate and contributes no evidence to the proved statement.
