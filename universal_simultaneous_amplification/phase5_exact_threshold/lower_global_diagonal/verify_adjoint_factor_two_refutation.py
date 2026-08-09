#!/usr/bin/env python3
"""Exact replay for the symmetric-W adjoint factor-two counterexample."""

from fractions import Fraction

import sympy as sp


F = Fraction


def symbolic_limit() -> None:
    r, gamma, theta = sp.symbols("r gamma theta", positive=True)
    A = 1 - gamma
    T = 1 + A * theta / gamma

    bA = sp.Integer(1)
    bC = 1 - T / r
    beta = sp.factor(A * bA + gamma * bC)
    assert sp.factor(beta - (1 - (gamma + A * theta) / r)) == 0

    sC = (r - 1) / r
    sigma = sp.factor(gamma * sC)
    assert sp.factor(sigma - gamma * (r - 1) / r) == 0

    baseline = (r - 1) / r
    gain = sp.factor(beta - baseline)
    cost = sp.factor(baseline - sigma)
    assert sp.factor(gain - A * (1 - theta) / r) == 0
    assert sp.factor(cost - A * (r - 1) / r) == 0
    assert sp.factor(cost / gain - (r - 1) / (1 - theta)) == 0
    assert sp.factor(
        (cost - 2 * gain).subs(r, 2)
        - A * (theta - sp.Rational(1, 2))
    ) == 0

    # The limiting B-coordinate of the dB positive branch.
    H = A * theta * (r - 1) / (r * gamma)
    x = sp.symbols("x")
    b_equation = sp.expand(
        x - r**2 * (1 - theta) * (1 - x) * (x + H)
    )
    assert sp.degree(b_equation, x) == 2


def matrices():
    p = [F(6493, 7000), F(1, 1000), F(1, 14)]
    W = [
        [F(1, 1000), F(980), F(7, 25)],
        [F(980), F(1), F(1)],
        [F(7, 25), F(1), F(1000)],
    ]
    delta = [sum(p[j] * W[i][j] for j in range(3)) for i in range(3)]
    P = [[p[j] * W[i][j] / delta[i] for j in range(3)] for i in range(3)]
    R = [[p[j] * P[j][i] / p[i] for j in range(3)] for i in range(3)]
    t = [sum(R[i]) for i in range(3)]

    assert sum(p) == 1
    assert all(
        W[i][j] == W[j][i] > 0 for i in range(3) for j in range(3)
    )
    assert all(sum(P[i]) == 1 for i in range(3))
    assert all(
        p[i] * P[i][j] == p[j] * R[j][i]
        for i in range(3)
        for j in range(3)
    )
    assert sum(p[i] * t[i] for i in range(3)) == 1
    return p, P, R, t


def box(center_strings, integer_radii):
    centers = [F(value) for value in center_strings]
    radii = [F(value, 10**8) for value in integer_radii]
    return (
        [center - radius for center, radius in zip(centers, radii)],
        [center + radius for center, radius in zip(centers, radii)],
    )


def matvec(matrix, vector):
    return [
        sum(matrix[i][j] * vector[j] for j in range(3))
        for i in range(3)
    ]


def exact_interval_certificate() -> None:
    p, P, R, t = matrices()

    q_lower, q_upper = box(
        [
            "0.10007400874271313",
            "0.99802218643427953",
            "0.62476550479407289",
        ],
        [283, 1, 938],
    )
    h_lower, h_upper = box(
        [
            "0.99803836212282937",
            "0.21910476890768346",
            "0.50131062575520824",
        ],
        [1, 174, 227],
    )

    def bd_map(q):
        Pq = matvec(P, q)
        return [
            t[i] / (t[i] + 2 * (1 - Pq[i]))
            for i in range(3)
        ]

    def db_map(h):
        Rh = matvec(R, h)
        return [
            F(1) / (1 + 2 * (t[i] - Rh[i]))
            for i in range(3)
        ]

    for lower, upper, fixed_map in [
        (q_lower, q_upper, bd_map),
        (h_lower, h_upper, db_map),
    ]:
        assert all(F(0) < lower[i] < upper[i] < F(1) for i in range(3))
        image_lower = fixed_map(lower)
        image_upper = fixed_map(upper)
        assert all(image_lower[i] >= lower[i] for i in range(3))
        assert all(image_upper[i] <= upper[i] for i in range(3))

    # L - 2G = 2 E_p q + E_p h - 3/2.  The upper corners give
    # an exact upper bound because every coefficient is positive.
    upper_factor_two = (
        2 * sum(p[i] * q_upper[i] for i in range(3))
        + sum(p[i] * h_upper[i] for i in range(3))
        - F(3, 2)
    )
    claimed = -F(182920163290948548677, 700000000000000000000)
    assert upper_factor_two == claimed
    assert upper_factor_two < 0

    # This member obeys the still-open sharper inequality with a robust gap.
    upper_beta_plus_sigma_minus_one = 1 - sum(
        p[i] * (q_lower[i] + h_lower[i]) for i in range(3)
    )
    assert upper_beta_plus_sigma_minus_one < 0


def main() -> None:
    symbolic_limit()
    exact_interval_certificate()
    print("PASS exact symmetric-W adjoint factor-two refutation")


if __name__ == "__main__":
    main()
