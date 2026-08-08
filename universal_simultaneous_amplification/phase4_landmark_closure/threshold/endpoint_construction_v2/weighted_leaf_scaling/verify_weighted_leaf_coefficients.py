#!/usr/bin/env python3
"""Exact algebra certificate for weighted common- and distinct-hub leaves."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    r, tau, a, z, x = sp.symbols("r tau a z x", positive=True)
    p = (r - 1) / r

    # Common-hub killed branching equation and its endpoint roots.
    killed = r**2 * z**2 - (r**2 + 1 + r * (r - 1) * a) * z + 1
    assert sp.factor(killed.subs({a: 0, z: 1 / r**2})) == 0
    assert sp.factor(killed.subs({a: 0, z: 1})) == 0
    ell_zero = 1 - 1 / r**2
    assert sp.factor(ell_zero / p - 1 - 1 / r) == 0
    assert sp.factor(1 / p - 1 - 1 / (r - 1)) == 0

    # Solve the exact limiting local chains for one distinct decorated hub.
    ub10, ub01, ub11 = sp.symbols("ub10 ub01 ub11")
    mark_b = (r - 1) / (1 + tau)
    solution_b = sp.solve(
        [
            sp.Eq(
                ub10,
                (mark_b + r * tau / (1 + tau) * ub11)
                / (mark_b + r * tau / (1 + tau) + 2),
            ),
            sp.Eq(ub01, r * ub11 / (r + tau / (1 + tau))),
            sp.Eq(ub11, (mark_b + ub01) / (mark_b + 1)),
        ],
        [ub10, ub01, ub11],
        simplify=True,
    )
    expected_ub10 = (
        (r - 1)
        * (r**2 * tau**2 + 2 * r**2 * tau + r**2 + r * tau**2 - r + tau**2)
        / ((r * tau + r + 2 * tau + 1) * (r**2 * tau + r**2 - r + tau**2))
    )
    expected_ub01 = r * (r - 1) * (tau + 1) / (r**2 * tau + r**2 - r + tau**2)
    assert sp.factor(solution_b[ub10] - expected_ub10) == 0
    assert sp.factor(solution_b[ub01] - expected_ub01) == 0

    ud10, ud01, ud11 = sp.symbols("ud10 ud01 ud11")
    solution_d = sp.solve(
        [
            sp.Eq(ud10, ((r - 1) + ud11) / (r + 1)),
            sp.Eq(
                ud01,
                (r * tau / (1 + r * tau) * ud11)
                / (1 + r * tau / (1 + r * tau)),
            ),
            sp.Eq(
                ud11,
                ((r - 1) + ud01 / (1 + r * tau))
                / ((r - 1) + 1 / (1 + r * tau)),
            ),
        ],
        [ud10, ud01, ud11],
        simplify=True,
    )
    expected_ud10 = (
        (r - 1)
        * (2 * r**2 * tau + r + 1)
        / (r * (r + 1) * (2 * r * tau - 2 * tau + 1))
    )
    expected_ud01 = tau * (r - 1) / (2 * r * tau - 2 * tau + 1)
    assert sp.factor(solution_d[ud10] - expected_ud10) == 0
    assert sp.factor(solution_d[ud01] - expected_ud01) == 0

    # Reconstruct the ordinary-singleton generator residuals from the exact
    # orbit rates before simplifying the Poisson corrections.
    C, i = sp.symbols("C i", positive=True)
    c = C - 1
    w = tau * C
    up_b = r * i * (c - i) / c
    down_b = i * ((c - i) / c + 1 / (c + w))
    activate_b = r * i / c
    residual_b = up_b * p - down_b * (r - 1) + activate_b * expected_ub10
    source_b_from_rates = sp.factor(sp.limit(C * residual_b / i, C, sp.oo))

    up_d = (c - i) * r * i / (r * i + c - i)
    down_d = i * (c - i + 1) / (r * (i - 1) + c - i + 1)
    activate_d = r * i / (r * i + c - i + w)
    residual_d = up_d * p - down_d * (r - 1) + activate_d * expected_ud10
    source_d_from_rates = sp.factor(sp.limit(C * residual_d / i, C, sp.oo))

    # Local initialization terms plus ordinary-singleton Poisson corrections.
    local_b = sp.factor((expected_ub10 + expected_ub01) / p - 2)
    source_b = sp.factor(r * expected_ub10 - (r - 1) / (1 + tau))
    assert sp.factor(source_b_from_rates - source_b) == 0
    full_b = sp.factor(local_b + source_b / (r - 1) ** 2)
    expected_b = -(
        (2 * tau + 1) * (r * tau**3 - 2 * r * tau - r + 2 * tau**3 + tau**2)
    ) / (
        (tau + 1)
        * (r * tau + r + 2 * tau + 1)
        * (r**2 * tau + r**2 - r + tau**2)
    )
    assert sp.factor(full_b - expected_b) == 0

    local_d = sp.factor((expected_ud10 + expected_ud01) / p - 2)
    source_d = sp.factor(-r * (r - 1) + r * expected_ud10 / (1 + tau))
    assert sp.factor(source_d_from_rates - source_d) == 0
    # The final +1 subtracts the complete-dB baseline coefficient -p/C.
    full_d = sp.factor(local_d + source_d / (r - 1) ** 2 + 1)
    expected_d = -(
        r**2 * tau**2
        + r**2 * tau
        + r * tau**2
        + r
        - 2 * tau**2
        - 2 * tau
        + 1
    ) / ((r + 1) * (tau + 1) * (2 * r * tau - 2 * tau + 1))
    assert sp.factor(full_d - expected_d) == 0

    endpoint_b = sp.factor(full_b.subs(r, sp.Rational(3, 2)))
    endpoint_d = sp.factor(full_d.subs(r, sp.Rational(3, 2)))
    assert sp.factor(
        endpoint_b
        + 4
        * (tau - 1)
        * (2 * tau + 1)
        * (7 * tau**2 + 9 * tau + 3)
        / ((tau + 1) * (7 * tau + 5) * (4 * tau**2 + 9 * tau + 3))
    ) == 0
    assert sp.factor(
        endpoint_d + (7 * tau**2 + tau + 10) / (10 * (tau + 1) ** 2)
    ) == 0
    assert full_b.subs({r: sp.Rational(3, 2), tau: sp.Rational(5, 2)}) == sp.Rational(
        -2216, 3535
    )
    assert full_d.subs({r: sp.Rational(3, 2), tau: sp.Rational(5, 2)}) == sp.Rational(
        -45, 98
    )

    separator = sp.factor(full_d + (r - 1) * full_b)
    numerator, denominator = sp.together(separator).as_numer_denom()
    shifted = sp.Poly(sp.expand(-numerator.subs(r, x + sp.Rational(3, 2))), x, tau)
    assert all(coefficient > 0 for _, coefficient in shifted.terms())
    assert sp.factor(denominator.subs({r: sp.Rational(3, 2), tau: 1})) > 0

    print("distinct-heavy tau=5/2: Bd=-2216/3535, dB=-45/98")
    print(f"positive shifted separator coefficients: {len(shifted.terms())}")
    print("PASS exact weighted-leaf coefficient and dominance certificate")


if __name__ == "__main__":
    main()
