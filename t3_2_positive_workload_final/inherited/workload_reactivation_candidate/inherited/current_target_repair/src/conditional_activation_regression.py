#!/usr/bin/env python3
"""Exact branch formula for the failed conditional-activation lemma."""
from __future__ import annotations
from fractions import Fraction
from math import factorial, log


def source_probabilities(x: int) -> tuple[Fraction, Fraction, Fraction]:
    den = x * x + 1
    return (Fraction(1, den), Fraction(x, den), Fraction(x * (x - 1), den))


def potential(x: int) -> float:
    return log(factorial(x + 2))


def expected_conditional_payoff(n: int) -> float:
    """Condition on 0->2A, then use path 2A->A->0 plus a final jump."""
    if n < 2:
        raise ValueError("n must be at least two")
    pre = potential(n)
    m = n + 2
    p0, p1, p2 = map(float, source_probabilities(m))
    x = m - 1
    q0, q1, q2 = map(float, source_probabilities(x))
    y = x - 1
    r0, r1, r2 = map(float, source_probabilities(y))
    final = r0 * potential(y + 2) + (r1 + r2) * potential(y - 1)
    at_a = q0 * potential(x + 2) + q2 * potential(x - 1) + q1 * final
    endpoint = p0 * potential(m + 2) + p1 * potential(m - 1) + p2 * at_a
    return endpoint - pre


def exact_log_coefficients(n: int) -> dict[int, Fraction]:
    """Return exact coefficients c_j in sum c_j log(n+j)."""
    N = n
    d0 = N * N + 1
    d1 = N * N + 2 * N + 2
    d2 = N * N + 4 * N + 5
    D = d0 * d1 * d2
    return {
        2: Fraction(-N * N * (N + 1) ** 2 * (N + 2), D),
        3: Fraction(N**5 + 6*N**4 + 13*N**3 + 18*N**2 + 16*N + 10, D),
        4: Fraction(2 * (N**4 + 3*N**3 + 5*N**2 + 5*N + 3), D),
        5: Fraction(2*N*N + 5*N + 4, d1 * d2),
        6: Fraction(1, d2),
    }


def coefficient_formula_value(n: int) -> float:
    return sum(float(c) * log(n + j) for j, c in exact_log_coefficients(n).items())


def self_test() -> None:
    for n in (10, 100, 1000, 10_000):
        a = expected_conditional_payoff(n)
        b = coefficient_formula_value(n)
        assert abs(a - b) < 2e-10
        assert a > 0
    # The scaled values approach 7 from below/above slowly and are already
    # safely positive and close on these exact deterministic checkpoints.
    vals = [n*n*coefficient_formula_value(n)/log(n) for n in (1_000, 10_000, 100_000)]
    assert all(v > 5 for v in vals)
    assert abs(vals[-1] - 7) < 0.2


if __name__ == "__main__":
    self_test()
    print("conditional_activation_counterexample.py self-test: OK")
