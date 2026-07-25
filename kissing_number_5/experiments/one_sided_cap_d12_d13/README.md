# Degree-12/13 one-sided cap search

This folder tests whether the exact degree-11 result \(B(5)\leq34\) can be
strengthened to \(B(5)\leq33\) with the same axisymmetric
Bachoc--Vallentin kernel family.

All outputs here are discovery artifacts unless accompanied by a separate
exact rational certificate and verifier.  In particular, solver objectives
and dense floating-point audits are not mathematical proofs.

The search samples:

- the full three-dimensional Gram domain;
- both determinant-zero sheets;
- the contact face \(t=1/2\);
- pole strata;
- a dense symmetry slice \(u=v\);
- a dedicated dense full slice \(u=0\), which was active in preliminary
  degree-12 and degree-13 solves;
- asymmetric fixed-ratio height slices.

The audit uses different grids and different height ratios.  A candidate is
eligible for rationalization only if its audited objective is strictly below
34 with enough margin to survive rational Gram-factor extraction and exact
closed-domain Bernstein verification.

Example:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/one_sided_cap_d12_d13/search.py \
  --degree 12 \
  --output experiments/one_sided_cap_d12_d13/results/degree12.npz \
  --report experiments/one_sided_cap_d12_d13/results/degree12_report.json
```

`scan_degree11_robustness.py` separately asks whether the *certified*
degree-11 kernel remains useful on the enlarged cap
\(-\varepsilon\leq u\leq1\).  Its output is still numerical evidence only;
an enlarged-cap theorem would require a new exact closed-domain audit.

That audit succeeded at \(\varepsilon=1/300\).  The theorem-strength
artifacts are deliberately outside this discovery folder:

- `../../certificates/one_sided_cap_degree11_robust_1_over_300.json`;
- `../../verifiers/verify_one_sided_cap_degree11_robust.py`;
- `../../tests/test_one_sided_cap_degree11_robust.py`;
- `../../proofs/one_sided_cap_degree11_robust.md`.

The exact targets are \(F\leq-121/125\) off the diagonal and
\(F(u,u,1)\leq3291/100\), giving objective
\(16939/484=35-1/484\).  The exploratory scans remain discovery history and
are not dependencies of the exact verifier.
