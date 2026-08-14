#!/usr/bin/env python3
"""Exact replay for the positive set-memory obstruction."""

from __future__ import annotations

import sympy as sp


def assert_zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.together(expr)) == 0, sp.factor(sp.together(expr))


def geometric_conditional_mean() -> None:
    r = sp.symbols("r", positive=True)
    a = r - 1

    # K has geometric law with success probability 1/r.
    mean_k = r
    probability_k1 = 1 / r
    probability_adverse = a / r
    conditional_mean = (mean_k - probability_k1) / probability_adverse
    assert_zero(conditional_mean - (r + 1))


def exact_soft_rows() -> None:
    r, x = sp.symbols("r x", positive=True)
    a = r - 1

    # x is the deterministic hole fraction of a coverage tester.
    clean_hit = 1 - x
    adverse_nohit = x**2 / (r - a * x)
    adverse_hit = 1 - adverse_nohit

    assert_zero(
        adverse_hit - clean_hit
        - r * x * (1 - x) / (r - a * x)
    )
    assert_zero(
        (r + 1) * clean_hit - adverse_hit
        - r**2 * (1 - x) ** 2 / (r - a * x)
    )

    # No-hit has the opposite order because it is the affine complement.
    clean_nohit = x
    assert_zero(
        clean_nohit - adverse_nohit
        - r * x * (1 - x) / (r - a * x)
    )


def positive_order_preservation() -> None:
    r = sp.symbols("r", positive=True)
    a = r - 1
    u0, u1, d0, d1 = sp.symbols("u0 u1 d0 d1", nonnegative=True)
    v0 = u0 + d0
    v1 = u1 + d1

    handoff = sp.Matrix([[u0, a * v0], [u1, a * v1]]) / r
    clean = handoff[:, 0]
    adverse = handoff[:, 1]
    assert (
        adverse - a * clean - a * sp.Matrix([d0, d1]) / r
    ).applyfunc(sp.factor) == sp.zeros(2, 1)

    n00, n01, n10, n11 = sp.symbols(
        "n00 n01 n10 n11", nonnegative=True
    )
    continuation = sp.Matrix([[n00, n01], [n10, n11]])
    propagated = continuation * (adverse - a * clean)
    expected = a * continuation * sp.Matrix([d0, d1]) / r
    assert (propagated - expected).applyfunc(sp.factor) == sp.zeros(2, 1)


def complete_router_rank_one() -> None:
    r, alpha = sp.symbols("r alpha", positive=True)
    a = r - 1
    beta = 1 - alpha
    handoff = sp.Matrix([[alpha, a * alpha], [beta, a * beta]]) / r
    assert_zero(handoff.det())
    assert handoff.rank() == 1


def spectral_bound() -> None:
    r, u0, u1, theta0, theta1 = sp.symbols(
        "r u0 u1 theta0 theta1", positive=True
    )
    a = r - 1
    handoff = sp.Matrix(
        [[u0, a * theta0 * u0], [u1, a * theta1 * u1]]
    ) / r

    assert_zero(
        handoff.det()
        - a * u0 * u1 * (theta1 - theta0) / r**2
    )
    assert_zero(handoff.trace() - (u0 + a * theta1 * u1) / r)

    determinant_over_trace_squared = sp.factor(
        handoff.det() / handoff.trace() ** 2
    )
    assert_zero(
        determinant_over_trace_squared
        - a * u0 * u1 * (theta1 - theta0)
        / (u0 + a * theta1 * u1) ** 2
    )

    # AM--GM gap behind inequality (24).
    amgm_gap = (u0 + a * theta1 * u1) ** 2 - 4 * a * theta1 * u0 * u1
    assert_zero(amgm_gap - (u0 - a * theta1 * u1) ** 2)

    q = sp.symbols("q", positive=True)
    s = sp.sqrt(r + 1)
    q_star = (s - 1) / (s + 1)
    assert_zero(q_star / (1 + q_star) ** 2 - r / (4 * (r + 1)))

    # q/(1+q)^2 is increasing on the physical interval 0<q<1.
    assert_zero(
        sp.diff(q / (1 + q) ** 2, q)
        - (1 - q) / (1 + q) ** 3
    )


def main() -> None:
    geometric_conditional_mean()
    exact_soft_rows()
    positive_order_preservation()
    complete_router_rank_one()
    spectral_bound()
    print("PASS clean/adverse monotone coupling and submodular interval")
    print("PASS exact soft hit/complement orientation")
    print("PASS positive continuation preserves the one-factor floor")
    print("PASS complete positive routing is rank one")
    print("PASS exact two-state spectral bound")


if __name__ == "__main__":
    main()
