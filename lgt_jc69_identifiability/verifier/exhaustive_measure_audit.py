#!/usr/bin/env python3
"""Exact normalization and topology checks for the exhaustive genealogy measure."""
from __future__ import annotations

import sympy as s


def main() -> None:
    lam, t1, t2, u, v, z = s.symbols(
        "lambda t1 t2 u v z", positive=True
    )

    # Before t1, each unordered sampled pair is selected at aggregate rate lambda.
    no_first = s.exp(-3 * lam * t1)
    first_each = s.integrate(lam * s.exp(-3 * lam * u), (u, 0, t1))
    assert s.simplify(no_first + 3 * first_each - 1) == 0
    print("PASS first-event partition has total mass one")

    # After a first coalescence at u, absorption below t1 or survival to t1
    # is a complete conditional partition. Movements are already marginalized.
    absorb_below = s.integrate(
        lam * s.exp(-lam * (v - u)), (v, u, t1)
    )
    survive_t1 = s.exp(-lam * (t1 - u))
    assert s.simplify(absorb_below + survive_t1 - 1) == 0
    print("PASS post-coalescence absorption/survival partition has mass one")

    # Conditional movement kernel for the identity of the ancestrally
    # unoccupied branch.
    a = s.Rational(1, 3) + s.Rational(2, 3) * s.exp(-3 * lam * z / 2)
    b = s.Rational(1, 3) - s.Rational(1, 3) * s.exp(-3 * lam * z / 2)
    P = s.Matrix([[a, b, b], [b, a, b], [b, b, a]])
    Q = lam / 2 * s.Matrix([[-2, 1, 1], [1, -2, 1], [1, 1, -2]])
    assert P.subs(z, 0) == s.eye(3)
    assert all(s.simplify(sum(P.row(i)) - 1) == 0 for i in range(3))
    assert s.simplify(s.diff(P, z) - P * Q) == s.zeros(3)
    print("PASS three-state CTMC kernel, row sums, and Kolmogorov equation")

    # The topology-dependent table at t1 has row sum one.
    rho = s.symbols("rho", positive=True)
    rows = [
        ((1 - rho) / 3, (2 + rho) / 3),
        ((2 + rho) / 6, (4 - rho) / 6),
        ((2 + rho) / 6, (4 - rho) / 6),
    ]
    assert all(s.simplify(left + right - 1) == 0 for left, right in rows)
    print("PASS topology-dependent t1 outcome table has unit row sums")

    # A continuing pair above t1 transfers before t2 or coalesces at t2.
    above_density = 2 * lam * s.exp(-2 * lam * (v - t1))
    above_transfer = s.integrate(above_density, (v, t1, t2))
    above_point = s.exp(-2 * lam * (t2 - t1))
    assert s.simplify(above_transfer + above_point - 1) == 0
    print("PASS two-lineage process above t1 has total mass one")

    # Joint density for a second transfer-coalescence below t1.
    first_density = lam * s.exp(-3 * lam * u)
    joint = first_density * s.exp(-lam * (v - u)) * lam
    assert s.simplify(joint - lam**2 * s.exp(-lam * (2 * u + v))) == 0
    print("PASS absolute-time density for second transfer-coalescence")

    # Topology depends only on the first sampled-pair coalescence.
    T1 = s.simplify(no_first + first_each)
    T2 = s.simplify(first_each)
    T3 = s.simplify(first_each)
    assert s.simplify(T1 - (s.Rational(1, 3) + s.Rational(2, 3) * no_first)) == 0
    assert s.simplify(T2 - (s.Rational(1, 3) - s.Rational(1, 3) * no_first)) == 0
    assert s.simplify(T3 - T2) == 0
    assert s.simplify(T1 + T2 + T3 - 1) == 0
    print("PASS exact gene-tree topology probabilities")

    print("ALL EXHAUSTIVE-MEASURE CHECKS PASSED")


if __name__ == "__main__":
    main()
