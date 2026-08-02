#!/usr/bin/env python3
"""Exact certificates for the exchangeable multiportal protected-pair trace."""

from __future__ import annotations

import sympy as sp


def checked_zero(expr: sp.Expr, label: str) -> None:
    value = sp.factor(sp.cancel(expr))
    if value != 0:
        raise AssertionError(f"{label}: {value}")
    print(f"PASS {label}")


def exact_episode_transform(
    portal_count: int,
    rule: str,
    r: sp.Expr,
    c: sp.Expr,
    g: sp.Expr,
    z: sp.Expr,
) -> sp.Expr:
    """Solve the exact tridiagonal marked-child recurrence from count one."""
    matrix = sp.zeros(portal_count)
    rhs = sp.zeros(portal_count, 1)
    q = sp.Integer(portal_count)
    for k_int in range(1, portal_count + 1):
        k = sp.Integer(k_int)
        if rule == "Bd":
            death = k * (2 * c + (q - k) * g / (q - 1))
            birth = r * k * (q - k) * g / (q - 1)
            child = k * r**2 * (1 - g) / (r + 1)
        elif rule == "dB":
            death = (
                k
                * (q - 1 - g * (k - 1))
                / (q - 1 + g * (r - 1) * (k - 1))
            )
            birth = (
                r
                * k
                * (q - k)
                * g
                / (q - 1 + g * (r - 1) * k)
            )
            child = k * r * c
        else:
            raise ValueError(rule)
        row = k_int - 1
        matrix[row, row] = death + birth + child * (1 - z)
        if k_int == 1:
            rhs[row] = death
        else:
            matrix[row, row - 1] = -death
        if k_int < portal_count:
            matrix[row, row + 1] = -birth
    return sp.factor(matrix.inv().multiply(rhs)[0])


def main() -> None:
    r, c, g, x, y = sp.symbols("r c g x y", positive=True)
    q, k = sp.symbols("q k", integer=True, positive=True)

    # The dB rates obtained directly with theta agree with their g form.
    theta = g / (1 - g)
    birth_theta = (
        (q - k)
        * r
        * k
        * theta
        / (q - 1 + theta * (q - k - 1 + r * k))
    )
    birth_g = r * k * (q - k) * g / (q - 1 + g * (r - 1) * k)
    checked_zero(birth_theta - birth_g, "dB portal-birth rate conversion")

    death_theta = (
        k
        * (q - 1 + theta * (q - k))
        / (q - 1 + theta * (q - k + r * (k - 1)))
    )
    death_g = (
        k
        * (q - 1 - g * (k - 1))
        / (q - 1 + g * (r - 1) * (k - 1))
    )
    checked_zero(death_theta - death_g, "dB portal-death rate conversion")

    # Bd exponential barrier at z=1/r^2.  Rates have been divided by 1-g.
    h = g / (1 - g)
    t = x / (x + r - 1)
    # Keep a common symbolic value f_k rather than asking SymPy to simplify
    # powers with a symbolic integer exponent.
    f_now = sp.symbols("f_k", positive=True)
    f_prev, f_next = f_now / t, f_now * t
    death_bar = x + (q - k) * h / (q - 1)
    birth_bar = r * (q - k) * h / (q - 1)
    marked_bar = r - 1
    bd_residual = sp.factor(
        k
        * (
            death_bar * (f_prev - f_now)
            + birth_bar * (f_next - f_now)
            - marked_bar * f_now
        )
    )
    bd_expected = sp.factor(
        k
        * f_now
        * (q - k)
        * h
        / (q - 1)
        * (r - 1) ** 2
        * (1 - x)
        / (x * (x + r - 1))
    )
    checked_zero(bd_residual - bd_expected, "Bd q-uniform exponential barrier")

    # dB backward-ratio envelope at c=(1-g)/2 and z=(2-r)/r.
    a = (r - 1) * (1 - g)
    dbar = (q - 1 - g * (k - 1)) / (
        q - 1 + g * (r - 1) * (k - 1)
    )
    ubar = r * (q - k) * g / (q - 1 + g * (r - 1) * k)

    def envelope(index: sp.Expr) -> sp.Expr:
        return 1 + (r - 1) * (
            q - 1 + g * (r - 1) * (index - 1)
        ) / (q - 1)

    top_ratio = 1 + a / dbar.subs(k, q)
    checked_zero(top_ratio - envelope(q), "dB top-state envelope equality")

    envelope_gap = sp.factor(
        envelope(k)
        - (1 + (a + ubar * (1 - 1 / envelope(k + 1))) / dbar)
    )
    expected_gap = sp.factor(
        g**2
        * k
        * (q - k)
        * (r - 1) ** 3
        * (q - 1 + g * (r - 1) * (k - 1))
        / (
            (q - 1)
            * (q - 1 - g * (k - 1))
            * (r * (q - 1) + g * k * (r - 1) ** 2)
        )
    )
    checked_zero(envelope_gap - expected_gap, "dB q-uniform backward envelope gap")
    checked_zero(envelope(1) - r, "dB envelope starts at r")

    # Uniform two-regime gap used for growing portal counts.
    p = (r - 1) / r
    x_star = r * (2 - r)
    x_mid = (1 + x_star) / 2
    m_bd = sp.factor(r * (r + 1) * x_mid * (r - 1) / (x_mid + r - 1))
    m_db = sp.factor(2 * r**2 * p / x_mid)
    checked_zero(
        (r**2 - 1 - m_bd)
        - (r - 1) ** 4 * (r + 1) / (4 * r - r**2 - 1),
        "uniform Bd test gap",
    )
    checked_zero(
        2 * (r - 1) / (2 - r) - m_db
        - 2 * (r - 1) ** 3 / ((2 - r) * (1 + 2 * r - r**2)),
        "uniform dB test gap",
    )
    d_db_star = sp.factor(1 / (1 + m_db))
    delta_db = sp.factor(p - sp.Rational(1, 2) * (1 - d_db_star))
    checked_zero(
        delta_db - (r - 1) ** 3 / (r * (3 * r**2 - 2 * r + 1)),
        "uniform dB establishment gap",
    )

    # Growing-Q boundary branching audit.
    f_limit = 1 / r
    checked_zero(
        r * g * f_limit**2 - (r + g) * f_limit + 1,
        "growing-Q dB boundary root",
    )

    # Both post-establishment portal chains have this adjacent stationary
    # ratio.  The concrete Bd and dB choices differ only in A and B.
    A, B = sp.symbols("A B", positive=True)
    auxiliary_birth = r * (q - k) * (A + g * k)
    auxiliary_death_next = (k + 1) * (B + g * (q - k - 1))
    generic_ratio = auxiliary_birth / auxiliary_death_next

    bd_ratio = (
        r
        * (q - k)
        * (2 * c * y + g * k / (q - 1))
        / (
            (k + 1)
            * (2 * c * (1 - y) + g * (q - k - 1) / (q - 1))
        )
    )
    checked_zero(
        bd_ratio
        - generic_ratio.subs(
            {A: 2 * c * (q - 1) * y, B: 2 * c * (q - 1) * (1 - y)}
        ),
        "Bd stationary adjacent ratio",
    )

    db_ratio = (
        r
        * (q - k)
        * ((1 - g) * y * (q - 1) + g * k)
        / (
            (k + 1)
            * ((1 - g) * (1 - y) * (q - 1) + g * (q - k - 1))
        )
    )
    checked_zero(
        db_ratio
        - generic_ratio.subs(
            {
                A: (1 - g) * (q - 1) * y,
                B: (1 - g) * (q - 1) * (1 - y),
            }
        ),
        "dB stationary adjacent ratio",
    )

    mean_k, mean_q_minus_k, mean_cut = sp.symbols(
        "mean_k mean_q_minus_k mean_cut", positive=True
    )
    stationary_flow = sp.expand(
        r * A * mean_q_minus_k
        + r * g * mean_cut
        - B * mean_k
        - g * mean_cut
    )
    checked_zero(
        stationary_flow
        - (
            r * A * mean_q_minus_k
            - B * mean_k
            + (r - 1) * g * mean_cut
        ),
        "post-establishment stationary flow identity",
    )

    # Independent exact matrix checks at rational parameters.
    rv, cv, gv = sp.Rational(8, 5), sp.Rational(2, 5), sp.Rational(3, 10)
    for portal_count in range(2, 8):
        fb = exact_episode_transform(
            portal_count, "Bd", rv, cv, gv, 1 / rv**2
        )
        fd = exact_episode_transform(
            portal_count, "dB", rv, cv, gv, (2 - rv) / rv
        )
        if not (0 < fb < 1 and 0 < fd < 1):
            raise AssertionError(f"invalid exact transforms at q={portal_count}")
        print(f"PASS exact tridiagonal transforms q={portal_count}")

    print("ALL MULTIPORTAL CERTIFICATES PASS")


if __name__ == "__main__":
    main()
