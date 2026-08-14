#!/usr/bin/env python3
"""Exact replay for the regular action/support combination obstruction."""

from __future__ import annotations

import sympy as sp


def assert_zero(expr: sp.Expr) -> None:
    expanded = sp.expand_log(expr, force=True)
    assert sp.factor(sp.cancel(sp.simplify(expanded))) == 0, sp.factor(
        sp.cancel(sp.simplify(expanded))
    )


def coeff(expr: sp.Expr, epsilon: sp.Symbol, order: int) -> sp.Expr:
    return sp.factor(
        sp.diff(expr, epsilon, order).subs(epsilon, 0) / sp.factorial(order)
    )


def average(weight: sp.Matrix, value: sp.Matrix) -> sp.Expr:
    return sp.Add(*(weight[i] * value[i] for i in range(value.rows)))


def main() -> None:
    r, lam, epsilon = sp.symbols("r lam epsilon", real=True)
    c = r - 1

    one = sp.ones(2, 1)
    f = sp.Matrix([1, -1])
    pi = sp.Rational(1, 2) * one
    pmat = sp.Matrix(
        [
            [(1 + lam) / 2, (1 - lam) / 2],
            [(1 - lam) / 2, (1 + lam) / 2],
        ]
    )
    assert pmat * one == one
    assert pmat * f == lam * f

    avec = one + epsilon * f
    da = sp.diag(*avec)
    rmat = da.inv() * pmat * da
    tvec = da.inv() * pmat * avec
    pweight = sp.Matrix([pi[i] * avec[i] for i in range(2)])

    q0 = 1 / r
    q_first = c * (lam - 1) / (r * (r - lam))
    q_second = -(
        (lam - 1) * c * (r - lam**2) / (r * (r - lam) ** 2)
    )
    h_second = lam * (lam - 1) * c**2 / (r * (r - lam) ** 2)

    qvec = q0 * one + epsilon * q_first * f + epsilon**2 * q_second * one
    hvec = q0 * one - epsilon * q_first * f + epsilon**2 * h_second * one
    bvec = one - qvec
    svec = one - hvec

    # The truncated analytic branches solve both endpoint equations through
    # exactly the order used in every subsequent coefficient.
    bd_residual = sp.Matrix(
        [
            tvec[i] * bvec[i] - r * qvec[i] * (pmat * bvec)[i]
            for i in range(2)
        ]
    )
    db_residual = sp.Matrix(
        [
            svec[i] - r * hvec[i] * (rmat * svec)[i]
            for i in range(2)
        ]
    )
    for residual in (bd_residual, db_residual):
        for entry in residual:
            for order in range(3):
                assert_zero(coeff(entry, epsilon, order))

    scaled_input = c * qvec
    rscaled = rmat * scaled_input
    first_image = sp.Matrix(
        [r * rscaled[i] / (1 + r * rscaled[i]) for i in range(2)]
    )

    target = average(pweight, scaled_input - svec)
    scaled_slack = average(pweight, scaled_input - first_image)

    target_ratio = r * (r + c * lam) / c
    slack_ratio = r + (3 * r - 5) * lam + (r - 2) ** 2 * lam**2 / r
    assert_zero(coeff(target, epsilon, 2) - q_first**2 * target_ratio)
    assert_zero(
        coeff(scaled_slack, epsilon, 2) - q_first**2 * slack_ratio
    )

    def dphi(left: sp.Expr, right: sp.Expr) -> sp.Expr:
        ratio = (1 - left) / (1 - right)
        return ratio - 1 - sp.log(ratio)

    cross = svec - bvec
    bregman_b = sp.Add(
        *(
            pi[i] * tvec[i] * dphi(svec[i], bvec[i])
            for i in range(2)
        )
    ) / r
    kinetic_b = average(pi, cross.multiply_elementwise(pmat * cross)) / 2
    delta_b = bregman_b - kinetic_b

    scalar_b = sp.Add(
        *(
            pi[i]
            * tvec[i]
            * (
                dphi(svec[i], bvec[i])
                - cross[i] ** 2 / (2 * qvec[i])
            )
            for i in range(2)
        )
    ) / r
    pb = pmat * bvec
    edge_b = sp.Add(
        *(
            pi[i]
            * cross[i]
            * (pb[i] * cross[i] / bvec[i] - (pmat * cross)[i])
            for i in range(2)
        )
    ) / 2

    reverse_cross = bvec - svec
    bregman_d = sp.Add(
        *(
            pi[i] * avec[i] ** 2 * dphi(bvec[i], svec[i])
            for i in range(2)
        )
    ) / r
    weighted_cross = avec.multiply_elementwise(reverse_cross)
    kinetic_d = average(
        pi, weighted_cross.multiply_elementwise(pmat * weighted_cross)
    ) / 2
    delta_d = bregman_d - kinetic_d

    scalar_d = sp.Add(
        *(
            pi[i]
            * avec[i] ** 2
            * (
                dphi(bvec[i], svec[i])
                - reverse_cross[i] ** 2 / (2 * hvec[i])
            )
            for i in range(2)
        )
    ) / r
    as_ground = avec.multiply_elementwise(svec)
    pas = pmat * as_ground
    edge_d = sp.Add(
        *(
            pi[i]
            * weighted_cross[i]
            * (
                pas[i] * weighted_cross[i] / as_ground[i]
                - (pmat * weighted_cross)[i]
            )
            for i in range(2)
        )
    ) / 2

    full_ratio = 2 * (r - lam)
    scalar_ratio = 2 * c
    edge_ratio = 2 * (1 - lam)
    for full in (delta_b, delta_d):
        assert_zero(coeff(full, epsilon, 2) - q_first**2 * full_ratio)
    for scalar in (scalar_b, scalar_d):
        assert_zero(coeff(scalar, epsilon, 2) - q_first**2 * scalar_ratio)
    for edge in (edge_b, edge_d):
        assert_zero(coeff(edge, epsilon, 2) - q_first**2 * edge_ratio)
    for full, scalar, edge in (
        (delta_b, scalar_b, edge_b),
        (delta_d, scalar_d, edge_d),
    ):
        for order in range(3):
            assert_zero(coeff(full - scalar - edge, epsilon, order))

    # Full-remainder architecture.  A is the sum of the two limiting action
    # coefficients and B is the limiting scaled-first coefficient.
    acoef, bcoef = sp.symbols("A B", real=True)
    full_identity = sp.Poly(
        sp.expand(
            target_ratio
            - 2 * acoef * (r - lam)
            - bcoef * slack_ratio
        ),
        lam,
    )
    assert_zero(full_identity.coeff_monomial(lam**2) + bcoef * (r - 2) ** 2 / r)
    after_b_zero = sp.Poly(full_identity.as_expr().subs(bcoef, 0), lam)
    assert_zero(after_b_zero.coeff_monomial(lam) - (r + 2 * acoef))
    forced_a = -r / 2
    assert_zero(
        after_b_zero.coeff_monomial(1).subs(acoef, forced_a) - r**3 / c
    )

    # Resolved architecture.  As and Ae aggregate the scalar and Picone
    # coefficients; B0 is the scaled-first coefficient.
    scalar_coef, edge_coef, bzero = sp.symbols("As Ae B0", real=True)
    resolved_identity = sp.Poly(
        sp.expand(
            target_ratio
            - 2 * c * scalar_coef
            - 2 * (1 - lam) * edge_coef
            - bzero * slack_ratio
        ),
        lam,
    )
    assert_zero(
        resolved_identity.coeff_monomial(lam**2)
        + bzero * (r - 2) ** 2 / r
    )
    after_bzero_zero = sp.Poly(resolved_identity.as_expr().subs(bzero, 0), lam)
    assert_zero(after_bzero_zero.coeff_monomial(lam) - (r + 2 * edge_coef))

    print("PASS analytic physical endpoint tangent through quadratic order")
    print("PASS exact T, scaled-first, and full-action coefficients")
    print("PASS exact scalar/Picone resolved coefficients")
    print("PASS regular nonnegative-combination obstruction")


if __name__ == "__main__":
    main()
