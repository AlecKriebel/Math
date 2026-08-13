#!/usr/bin/env python3
"""Exact replay of the local gate disjunction and boundary-ray convexification."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    r, b, d, q, z = sp.symbols("r b d q z", positive=True)
    c = r - 1
    p = c / r
    K = r * c**2 / q

    response_b = sp.cancel(r * b / c * z / (1 + z) - 1)
    response_d = sp.cancel(r * d / c * K / (K + z) - 1)

    assert sp.simplify(
        sp.together(response_b).as_numer_denom()[0]
        - (r * z * (b - p) - c)
    ) == 0
    assert sp.simplify(
        sp.together(response_d).as_numer_denom()[0]
        - (r**2 * c * (d - p) - q * z)
    ) == 0

    lower = c / (r * (b - p))
    upper = r**2 * c * (d - p) / q
    assert sp.cancel(
        upper - lower
        - c * (r**3 * (b - p) * (d - p) - q)
        / (q * r * (b - p))
    ) == 0

    # Abstract leaf/pair boundary rays and the exact cancellation points.
    B, D, eta, eps = sp.symbols("B D eta eps", real=True)
    leaf = sp.Matrix([1 / c, -1])
    pair = sp.Matrix([-eta / c, eta])
    v = sp.Matrix([B, D])
    L = lambda x: sp.cancel(x[1] + c * x[0])
    assert L(leaf) == 0
    assert L(pair) == 0
    assert sp.simplify(v + (-c * B) * leaf) == sp.Matrix([0, D + c * B])
    assert sp.simplify(v + (-D / eta) * pair) == sp.Matrix([(D + c * B) / c, 0])

    # Strong-pair tangency at the hybrid root.
    sigma = sp.symbols("sigma", positive=True)
    pair_b = 2 * (sigma - 1) / (1 + sigma * (r**2 - 1))
    pair_d = 2 * (r * (2 - r) - sigma) / (sigma + 2 * r * c)
    polynomial = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
    sigma_star = (-r**3 + 4 * r**2 - 3 * r - 1) / (2 * c)
    tangent_numerator = sp.factor(
        sp.together((pair_d + c * pair_b).subs(sigma, sigma_star)).as_numer_denom()[0]
    )
    assert sp.rem(tangent_numerator, polynomial, r) == 0
    # Rational isolation shows sigma_star is in (0,1), so pair_b<0; tangency
    # then forces pair_d=-c*pair_b>0.

    print("PASS exact one-module gate disjunction")
    print("PASS exact leaf/pair boundary-ray convexification")
    print("PASS strong-pair tangency modulo the hybrid sextic")


if __name__ == "__main__":
    main()
