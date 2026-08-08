#!/usr/bin/env python3
"""Exact replay for the separated-pair first-event obstruction."""

from __future__ import annotations

import sympy as sp


r, x, s = sp.symbols("r x s", positive=True)
R = r**2
c = (r - 1) * r / (r + 1)
d = sp.Rational(1, 2)


def main() -> None:
    # The two first-event gain bounds and their stationary point.
    envelope = c * R * x / (1 + R * x) + d * R / (R + x)
    scale = sp.sqrt(c / d)
    critical = sp.factor((scale * R - 1) / (R - scale))
    derivative = sp.diff(envelope, x)
    assert sp.simplify(derivative.subs(x, critical)) == 0

    maximum = sp.factor(envelope.subs(x, critical))
    claimed = sp.factor(
        R * (R * (1 + scale**2) - 2 * scale) / (2 * (R**2 - 1))
    )
    assert sp.simplify(maximum - claimed) == 0

    # Eliminate the sole radical from M(r)=r-1.
    radical_relation = (r + 1) * s**2 - 2 * r * (r - 1)
    crossing = sp.factor(
        R * (R * (1 + s**2) - 2 * s) - 2 * (R**2 - 1) * (r - 1)
    )
    polynomial = sp.factor(sp.resultant(crossing, radical_relation, s))
    expected = (
        r**10
        - 6 * r**9
        + 9 * r**8
        - 12 * r**7
        + 12 * r**6
        + 12 * r**5
        - 8 * r**4
        - 8 * r**2
        + 4
    )
    assert sp.expand(polynomial - expected) == 0
    assert sp.count_roots(expected, 1, 2) == 1
    lo, hi = sp.Rational(1698, 1000), sp.Rational(1699, 1000)
    assert sp.count_roots(expected, lo, hi) == 1

    exact_crossing = crossing.subs(s, scale)
    assert sp.sign(sp.simplify(exact_crossing.subs(r, lo))) == 1
    assert sp.sign(sp.simplify(exact_crossing.subs(r, hi))) == -1
    assert sp.sign(sp.simplify(exact_crossing.subs(r, 2))) == -1

    # At r=2 the sharp envelope is strictly below the required value one.
    endpoint = sp.simplify(claimed.subs(r, 2))
    assert sp.sign(1 - endpoint) == 1

    # Independent finite exact checks of (5) on arbitrary rational stars.
    # Only the first changing event is needed: later fixation is <= 1.
    tests = [
        (sp.Rational(1, 7), [sp.Rational(2), sp.Rational(3, 5)]),
        (sp.Rational(5, 2), [sp.Rational(1, 3), sp.Rational(9, 4)]),
        (sp.Rational(11, 13), [sp.Rational(7, 2), sp.Rational(4, 9)]),
    ]
    r0 = sp.Rational(2)
    for ai, neighbors in tests:
        edge_sum = sp.Integer(len(neighbors))
        weighted = sum(neighbors)
        x0 = ai * edge_sum / weighted
        bd_gain = r0**2 * x0 / (1 + r0**2 * x0)
        db_gain = r0**2 / (r0**2 + x0)
        combined = sp.Rational(2, 3) * bd_gain + sp.Rational(1, 2) * db_gain
        assert combined <= endpoint

    root = sp.RootOf(expected, 2)  # unique positive root in (1,2)
    assert lo < root < hi
    print("PASS: exact source/target pair conversion rates reconstructed")
    print("PASS: sharp first-event envelope and critical point verified")
    print("PASS: degree-10 crossing polynomial has one root in (1,2)")
    print("R_pair in (1698/1000,1699/1000)")
    print("M(2) =", endpoint)
    print("1-M(2) =", sp.simplify(1 - endpoint))


if __name__ == "__main__":
    main()
