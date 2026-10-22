# Endpoint pressure and bootstrap audit: pass 2

Frozen target E-6322, 2026-10-16. Pass 1's adversarial review was read before this work.

**No unconditional higher-integrability or determinant-positivity theorem was obtained. No benchmark counterexample was obtained.**

New results:

1. `DINI_PRESSURE_BOUND.md`: a quantitative global pressure bound from a Dini modulus of the positive-degree energy-momentum tensor. It includes the boundary and does not assume that the Jacobian has a continuous representative. Dini-continuous Dy is a sufficient special case. This is a conditional theorem, not newly proved regularity of arbitrary minimizers.
2. `BOOTSTRAP_OBSTRUCTIONS.md`: precise admissibility and growth obstacles to applying a conventional Caccioppoli/Gehring argument; a convex tangent-barrier regularization is analyzed quantitatively. Its exact optimal additive growth constant is computed and diverges as epsilon^{-6} when the polynomial-growth coefficient is fixed. Its rank-one Hessian can grow as epsilon^{-4}. Uniform finite energy does not eliminate either issue.
3. `verify_endpoint.py` and `ENDPOINT_CHECKS.json`: reproducible differentiation and optimization checks.

The exact lane separately supplies continuous-tensor/unbounded-pressure and uniformly-positive-Jacobian/no-gradient-gain examples. They are route obstructions, not constitutive minimizers. The variations lane owns the new finite radial comparison and its exact low-Jacobian estimate.

The unresolved step remains an admissibility-preserving estimate that genuinely improves the minimizer's positive-degree strain energy beyond its baseline L^1 control, or another argument that excludes low-Jacobian sets without assuming that improvement.
