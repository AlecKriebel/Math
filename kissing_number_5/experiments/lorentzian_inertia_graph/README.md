# Lorentzian inertia graph experiment

This directory contains discovery code for the exact countermodel in
`certificates/lorentzian_rank6_interval_countermodel.json`.

The search minimizes
\[
4\max_{i<j}\langle y_i,y_j\rangle
-\min_{i<j}\langle y_i,y_j\rangle
\]
over 41 unit directions in \(\mathbb R^5\).  A value below 3 permits a
scale \(s\) such that
\[
A=(K-sJ)/(1-s)
\]
has diagonal one and off-diagonal entries in \((-3,0)\).

Discovery environment:

- Python 3;
- NumPy 2.5.1;
- SciPy 1.18.0;
- deterministic seed `72541`.

Re-run the numerical discovery with:

```sh
.venv/bin/python experiments/lorentzian_inertia_graph/search_range_surrogate.py \
  --seed 72541 --starts 6 --iterations 400
```

The printed floating-point coordinates are not a certificate.  The
committed object was independently rounded through a rational
stereographic parametrization, and the standard-library verifier proves
all stated properties from the exact rational certificate:

```sh
python3 verifiers/verify_lorentzian_inertia_graph.py
python3 -m unittest tests.test_lorentzian_inertia_graph -v
```
