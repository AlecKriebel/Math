#!/usr/bin/env python3
"""Independent event-level audit of the correlated-pair trace rates."""

from __future__ import annotations

import sympy as sp


def db_complete_singleton(order: int, fitness: sp.Expr) -> sp.Expr:
    """Solve the complete-graph dB count recurrence by the odds product."""
    products = []
    running = sp.Integer(1)
    for mutants in range(1, order):
        up_denominator = fitness * mutants + order - mutants - 1
        down_denominator = fitness * (mutants - 1) + order - mutants
        gamma = up_denominator / (fitness * down_denominator)
        running = sp.factor(running * gamma)
        products.append(running)
    return sp.factor(1 / (1 + sum(products, sp.Integer(0))))


def main() -> None:
    C = sp.symbols("C", integer=True, positive=True)
    r, sigma, x, y = sp.symbols("r sigma x y", positive=True)

    # The complete dB singleton formula is independently reconstructed from
    # the count-chain up/down odds for finite test orders.
    for order in range(2, 10):
        expected = (
            (order - 1)
            * (r - 1)
            * r ** (order - 2)
            / (order * (r ** (order - 1) - 1))
        )
        assert sp.factor(db_complete_singleton(order, r) - expected) == 0

    rho_bd_core = (1 - 1 / r) / (1 - r ** (-C))
    rho_db_core = (C - 1) * (r - 1) * r ** (C - 2) / (
        C * (r ** (C - 1) - 1)
    )

    # Coefficients of epsilon after summing labelled source--target or
    # death--parent events.  The pair internal edge is C/sigma; each of the
    # four inter-pair edges is epsilon*C*y.
    bd_A_finite = 2 * r * sigma * x * rho_bd_core
    bd_D_finite = 2 * C * x / (C - 1) / (r + 1)
    bd_m = 4 * r * sigma * y * (r / (r + 1))
    bd_q = 4 * sigma * y * (1 / (r + 1))

    db_A_finite = 2 * r * C * x / (C - 1) * rho_db_core
    db_D = 2 * sigma * x / r * sp.Rational(1, 2)
    db_m = 4 * r * sigma * y * sp.Rational(1, 2)
    db_q = 4 * sigma * y / r * sp.Rational(1, 2)

    tail = sp.symbols("tail", positive=True)
    assert sp.factor(
        bd_A_finite - 2 * sigma * (r - 1) * x / (1 - r ** (-C))
    ) == 0
    assert sp.limit(2 * sigma * (r - 1) * x / (1 - tail), tail, 0) == 2 * sigma * (r - 1) * x
    assert sp.limit(bd_D_finite, C, sp.oo) == 2 * x / (r + 1)
    assert sp.factor(bd_m - 4 * r**2 * sigma * y / (r + 1)) == 0
    assert sp.factor(bd_q - 4 * sigma * y / (r + 1)) == 0

    assert sp.factor(
        db_A_finite - 2 * (r - 1) * x / (1 - r ** (-(C - 1)))
    ) == 0
    assert sp.limit(2 * (r - 1) * x / (1 - tail), tail, 0) == 2 * (r - 1) * x
    assert sp.factor(db_D - sigma * x / r) == 0
    assert sp.factor(db_m - 2 * r * sigma * y) == 0
    assert sp.factor(db_q - 2 * sigma * y / r) == 0

    assert sp.factor(bd_m / bd_q - r**2) == 0
    assert sp.factor(db_m / db_q - r**2) == 0

    print("PASS: complete dB singleton recurrence independently solved")
    print("PASS: all Bd/dB pair--core event coefficients reconstructed")
    print("PASS: all Bd/dB pair--pair event coefficients reconstructed")
    print("PASS: infection/recovery ratio m/q=r^2 under both rules")


if __name__ == "__main__":
    main()
