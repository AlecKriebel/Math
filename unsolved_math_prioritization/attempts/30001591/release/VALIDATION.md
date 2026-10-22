# Validation and claim boundaries

- Author self-check only; independent mathematical audit remains pending.
- 43 exact SymPy controls pass, including logarithmic derivatives, curvature, invariant cancellation, Pohozaev identities, energy derivatives, exact threshold brackets, and the quartic cancellation.
- Three deliberately wrong mathematical identities are rejected: wrong invariant-error sign, wrong maximum-curvature sign, and a false nonzero quartic integral discrepancy.
- Controls use explicit exceptions, not removable Python assertions. Normal and optimized replays are compared byte-for-byte.
- The no-stationary-state proof does not assume positivity preservation for a time-dependent gKdV solution. Its even-power sign argument applies only to a stationary ODE profile.
- The compactness argument is cubic only; there is no claimed mass monotonicity for sign-changing solutions with even m.
- The critical ODE logarithmic law requires an exact exponential-tail equivalent stronger than an exponential upper bound.
- The finite-start and perturbed-invariant examples are ODE results, not counterexamples for the incoming PDE solution.
- The signed-integral exclusions assume sufficient L^1 information and do not follow from H^1 convergence alone.
- The target remains unsolved. No five-turn success quota, theorem invention, or numerical asymptotic inference is used.
