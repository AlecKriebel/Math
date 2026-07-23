#!/usr/bin/env python3
"""Exact verification of a mass-41 two-point LP pseudo-distribution.

The computation uses only fractions.Fraction.  It checks all low-degree
Gegenbauer moments needed by the accompanying analytic tail proof, plus every
rational comparison used in that proof.
"""

from fractions import Fraction as Q


N = 41
COUNTS = (176, 262, 652, 550)
NODES = (Q(-77, 100), Q(-11, 25), Q(-9, 100), Q(499, 1000))
WEIGHTS = tuple(Q(count, N) for count in COUNTS)
CHECK_DEGREE = 53


def zonal_values(t: Q, degree: int) -> list[Q]:
    """Return normalized dimension-five Gegenbauer values P_0(t),...,P_d(t)."""

    if degree < 0:
        raise ValueError("degree must be nonnegative")
    if degree == 0:
        return [Q(1)]

    values = [Q(1), t]
    for k in range(2, degree + 1):
        values.append(
            (
                (2 * k + 1) * t * values[k - 1]
                - (k - 1) * values[k - 2]
            )
            / (k + 2)
        )
    return values


def verify() -> dict[str, object]:
    """Run every exact check and return a small deterministic summary."""

    assert all(count > 0 and count % 2 == 0 for count in COUNTS)
    assert sum(COUNTS) == N * (N - 1)
    assert sum(WEIGHTS, Q(0)) == N - 1
    assert all(Q(-1) <= t < Q(1, 2) for t in NODES)

    values = tuple(zonal_values(t, CHECK_DEGREE) for t in NODES)
    moments = [
        Q(1)
        + sum(
            (WEIGHTS[i] * values[i][k] for i in range(len(NODES))),
            Q(0),
        )
        for k in range(1, CHECK_DEGREE + 1)
    ]
    minimum = min((value, k) for k, value in enumerate(moments, 1))
    assert minimum == (Q(1027, 16000), 2)
    assert all(value > Q(1, 16) for value in moments)

    # Rational audits for q_i^(-3/2) < U_i, q_i = 1 - t_i^2.
    q_values = tuple(Q(1) - t * t for t in NODES)
    upper_bounds = (Q(4), Q(7, 5), Q(51, 50), Q(31, 20))
    assert all(
        q > 0 and q**3 > Q(1) / upper**2
        for q, upper in zip(q_values, upper_bounds, strict=True)
    )
    weighted_q_upper = sum(
        (weight * upper for weight, upper in zip(WEIGHTS, upper_bounds, strict=True)),
        Q(0),
    )
    assert weighted_q_upper == Q(129417, 2050)

    # pi < 22/7 and 2*pi < 44/7 < (251/100)^2 imply
    # pi^2*sqrt(2*pi)/4 < 31/5.
    assert Q(44, 7) < Q(251, 100) ** 2
    analytic_constant_upper = Q(22, 7) ** 2 * Q(251, 100) / 4
    assert analytic_constant_upper < Q(31, 5)
    tail_numerator_upper = Q(31, 5) * weighted_q_upper
    assert tail_numerator_upper == Q(4011927, 10250)
    assert tail_numerator_upper < 392
    assert 392**2 < 54**3

    return {
        "mass": Q(1) + sum(WEIGHTS, Q(0)),
        "minimum_moment": minimum[0],
        "minimum_moment_degree": minimum[1],
        "weighted_q_upper": weighted_q_upper,
        "tail_numerator_upper": tail_numerator_upper,
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
