# Positivity and admissible repair: shared pass 4

The frozen target is unchanged: arbitrary positive coefficients, every permitted smooth complete diffeomorphic trace, all full-class minimizers, and a determinant bound over the entire domain.

- `MIXED_MOMENT_VARIATION.md`: minimality forces the mixed inverse-cube moment integral J_v J_y^{-3} to be finite for every same-trace rank-one-connected endpoint with J_v>=0. The endpoint may itself have infinite barrier energy. This gives an exact localized positive-energy budget and proves that the coefficient 2 of the barrier source cannot be eliminated by taking smaller variation amplitudes.
- `REFERENCE_CEILINGS_AND_LOCALIZATION.md`: the fixed full trace imposes a volume ceiling on every reference's minimum singular value. The local ceiling shrinks with average J. Barrier-normalized affine excess loses uniform unweighted strain coercivity, and baseline local sphere traces need not permit Lipschitz replacements.
- `SINGLE_DIRECTION_REPAIR_OBSTRUCTION.md`: a C^1 finite-energy identity-trace radial homeomorphism admits no uniformly positive-Jacobian repair in any fixed target direction. Its unchanged two-coordinate volume marginals are unbounded. The map is explicitly nonminimizing; this rules out a class-level repair-existence shortcut, not a minimizer-specific theorem.
- `verify_repairs.py` and `REPAIR_CHECKS.json`: supplementary exact checks.

No existence of a uniformly positive same-slice repair is assumed. The mixed moment reduces to the baseline inverse-square moment when the endpoint is y itself. No unconditional inverse-cube bound, higher-gradient integrability, or epsilon-regularity theorem follows yet. E-6322 remains unresolved.
