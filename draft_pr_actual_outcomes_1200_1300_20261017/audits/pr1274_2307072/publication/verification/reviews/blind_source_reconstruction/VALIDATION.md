# Finite validation summary

Validation completed at 2026-10-18 01:46:31 UTC. Completion estimate: 98% toward the assigned source-only reconstruction and seal; no remaining mathematical gap identified.

Commands executed from this review folder:

    python3 CHECKS.py
    python3 CHECKS.py > _local/checks-normal.json
    python3 -O CHECKS.py > _local/checks-O.json
    python3 -OO CHECKS.py > _local/checks-OO.json

Every run exited 0 and reported PASS. The three saved runs contain the same exact and numerical results. All checks use explicit conditional exceptions rather than Python assert statements.

Exact rational checks covered n=1 through 40, corresponding to total polynomial degree through 80. They checked the polynomial/geometric input identity at five rational radii squared, the direct origin integral against -H_n, the transform polynomial from monomial integration against the radial integral form, and sample endpoint bounds. The proof of all radii and all degrees remains the analytic argument in REPORT.md.

Direct numerical principal-value checks used polar coordinates centered at the evaluation point, local constant subtraction, 1024 angular midpoints, and 256 radial midpoints. The four polynomial cases had absolute errors below 0.00000335. The singular-input cases at radii 0.125, 0.4, and 0.75 had errors below 0.000298. Those checks directly integrate the source kernel after circular-cutoff cancellation, rather than differentiating the derived Cauchy potential.

Numerical quadrature is corroborating evidence, not a validated error-bound computation. The negative conclusions rest on exact formulas and positive-area essential-norm witnesses.
