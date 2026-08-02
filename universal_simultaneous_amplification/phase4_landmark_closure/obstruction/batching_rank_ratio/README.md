# Geometric batching obstruction track

This folder studies the exact interpolation between the conservative
reversed-arrow process and death--birth updating at fitness `r=3/2`.

- `BATCHING_RATIO.md`: derivations, exact finite-class theorems, failed proof
  routes, and the remaining all-order inequality.
- `verify_interpolation_certificates.py`: exact interpolation,
  complete-curve, current, and Poisson-curvature checks.
- `verify_regular_mass_transport.py`: exact occupation transport,
  collision-Green, regular-order-four, modular, and Hessian certificates.
- `verify_committor_sign_counterexample.py`: exact statewise-sign
  counterexample.
- `search_*.py`: numerical falsification tools only; they are not proof.
- `RESEARCH_LOG.md`: timestamped research record.

The principal universal batching-ratio conjecture remains **OPEN**.  The
proved results are exact reductions and finite or structured regular-class
theorems, not a universal upper bound on `R_sim`.
