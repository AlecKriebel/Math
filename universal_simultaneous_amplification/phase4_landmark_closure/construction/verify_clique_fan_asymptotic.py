#!/usr/bin/env python3
"""Exact symbolic checks for the clique-fan rare-process coefficient."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    r, sigma, M, epsilon, x = sp.symbols(
        "r sigma M epsilon x", positive=True
    )
    q = (r - 1) / r
    beta = M * r * sigma
    hub0 = sp.cancel(beta * q / (1 + beta * q))
    leaf1 = sp.cancel(-q - sigma / r + sigma / (1 + M * sigma * (r - 1)))

    # Check the constant and first-order coefficients of
    # u=(1-u)(b*u+a*v), with the exact first-order b,a expansions.
    u = q + epsilon * leaf1
    v = hub0
    b = r - epsilon * r * (r - 1 + sigma)
    a = epsilon * r / M
    residual = sp.expand(u - (1 - u) * (b * u + a * v))
    assert sp.simplify(residual.coeff(epsilon, 0)) == 0
    assert sp.simplify(residual.coeff(epsilon, 1)) == 0
    assert sp.simplify(hub0 - (1 - hub0) * beta * q) == 0

    coefficient = sp.factor(leaf1 + hub0 / M)
    expected = sp.factor(
        -q - sigma / r + sigma * r / (1 + M * sigma * (r - 1))
    )
    assert sp.simplify(coefficient - expected) == 0

    substituted = sp.factor(expected.subs(sigma, x / M))
    sign_numerator = sp.factor(substituted * M * r * (1 + x * (r - 1)))
    polynomial = -x**2 + ((r + 1) - M * (r - 1)) * x - M
    assert sp.simplify(sign_numerator - (r - 1) * polynomial) == 0
    assert sp.simplify(expected.subs(sigma, 1 / M) + q * (1 - 1 / M)) == 0

    print("PASS rare-process first-order equations")
    print("PASS comparison coefficient identity")
    print("PASS quadratic sign numerator identity")
    print("PASS regular-spoke specialization")


if __name__ == "__main__":
    main()
