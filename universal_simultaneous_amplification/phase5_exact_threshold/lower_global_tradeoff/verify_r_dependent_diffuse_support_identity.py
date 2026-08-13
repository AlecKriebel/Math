#!/usr/bin/env python3
"""Exact symbolic replay for the fitness-dependent diffuse support identity.

This verifies algebra only.  In particular it does not assert K_r >= 0 or a
universal finite-graph separator.
"""

from __future__ import annotations

import sympy as sp


def main() -> None:
    r, x, u, t, q, h, A = sp.symbols(
        "r x u t q h A", positive=True
    )

    p0 = (r - 1) / r
    b = p0 + x
    s = p0 + u

    # The two scalar expansions used in the endpoint balance identities.
    assert sp.factor(
        (b * x / q - ((r - 1) * x + r * x**2 / q)).subs(
            q, 1 / r - x
        )
    ) == 0
    assert sp.factor(
        (s * u / h - ((r - 1) * u + r * u**2 / h)).subs(
            h, 1 / r - u
        )
    ) == 0

    # Pure scalar completion underlying the expectation identity.
    lhs = r * t * x**2 / q + r * u**2 / ((r - 1) * h) - r * u * A
    K = 4 * t * x**2 / ((r - 1) * q) - h * A**2
    rhs = (
        r * (r - 1) * K / 4
        + r * h / (r - 1) * (u / h - (r - 1) * A / 2) ** 2
    )
    assert sp.factor(lhs - rhs) == 0

    # At r=2 this is exactly the previous square normalization.
    old_square = h * (A - 2 * u / h) ** 2 / 2
    new_square_at_two = (
        r * h / (r - 1) * (u / h - (r - 1) * A / 2) ** 2
    ).subs(r, 2)
    assert sp.factor(old_square - new_square_at_two) == 0

    # Deterministic two-cycle boundary factorization.
    kappa = sp.symbols("kappa", positive=True)
    q1 = (kappa * r + 1) / (r * (kappa + r))
    q2 = (kappa + r) / (r * (kappa * r + 1))
    b1, b2 = 1 - q1, 1 - q2
    assert sp.factor(kappa * b1 - r * q1 * b2) == 0
    assert sp.factor(b2 / kappa - r * q2 * b1) == 0
    # The dB solution is (b2,b1).
    assert sp.factor(b2 - r * (1 - b2) * kappa * b1) == 0
    assert sp.factor(b1 - r * (1 - b1) * b2 / kappa) == 0
    p1, p2 = 1 / (1 + kappa), kappa / (1 + kappa)
    beta = sp.factor(p1 * b1 + p2 * b2)
    sigma = sp.factor(p1 * b2 + p2 * b1)
    two_cycle_T = sp.factor((p0 - sigma) - (r - 1) * (beta - p0))
    expected_two_cycle_T = (
        (kappa - 1) ** 2
        * (r - 1)
        / (r * (kappa + r) * (kappa * r + 1))
    )
    assert sp.factor(two_cycle_T - expected_two_cycle_T) == 0

    # Pair--leaf score and square-minus-sextic completion.
    z = sp.symbols("sigma", positive=True)
    pair_B = 2 * (z - 1) / (1 + z * (r**2 - 1))
    pair_D = 2 * (r * (2 - r) - z) / (z + 2 * r * (r - 1))
    F = (r - 1) * z**2 + (r**3 - 4 * r**2 + 3 * r + 1) * z + r * (2 * r - 3)
    denominator = (2 * r * (r - 1) + z) * (1 + z * (r**2 - 1))
    support = sp.factor(pair_D + (r - 1) * pair_B)
    assert sp.factor(support + 2 * r * F / denominator) == 0

    polynomial = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
    linear = 2 * (r - 1) * z + r**3 - 4 * r**2 + 3 * r + 1
    assert sp.expand(4 * (r - 1) * F - (linear**2 - polynomial)) == 0

    # General moment/tangency algebra for an integrated quadratic.
    AA, BB, CC, zstar = sp.symbols("AA BB CC zstar")
    integrated = AA * z**2 + BB * z + CC
    tangent_substitution = {BB: -2 * AA * zstar, CC: AA * zstar**2}
    assert sp.factor(integrated.subs(tangent_substitution)) == AA * (z - zstar) ** 2

    print(f"two-cycle T_r = {expected_two_cycle_T}")
    print("PASS arbitrary-r scalar square completion")
    print("PASS deterministic two-cycle factorization")
    print("PASS pair support and square-minus-sextic identity")
    print("PASS integrated-charge tangent moment conditions")
    print("OPEN sign of K_r and nonlinear cross-fitness upper theorem")


if __name__ == "__main__":
    main()
