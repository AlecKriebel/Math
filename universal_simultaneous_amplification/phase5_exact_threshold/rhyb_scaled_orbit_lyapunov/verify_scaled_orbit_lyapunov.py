#!/usr/bin/env python3
"""Exact replay for the scaled-orbit Lyapunov and two-cycle obstruction."""

from __future__ import annotations

import sympy as sp


r, kappa, z, u, v = sp.symbols("r kappa z u v", positive=True)
Q = sp.Rational


def mean(vector):
    return sp.factor((vector[0] + kappa * vector[1]) / (1 + kappa))


def dB_map(vector):
    first = r * kappa * vector[1] / (1 + r * kappa * vector[1])
    second = r * vector[0] / kappa / (1 + r * vector[0] / kappa)
    return sp.factor(first), sp.factor(second)


def verify_scalar_lyapunov_algebra():
    """Check the exact scalar identities behind the general proof."""

    h, s = sp.symbols("h s", positive=True)
    transform = u / (h + s * u)

    # The equality h+s=1 is the only relation used to put the image on the
    # segment joining u and one.
    segment_form = u + s * u * (1 - u) / (1 - s + s * u)
    assert sp.factor(transform.subs(h, 1 - s) - segment_form) == 0

    # Conditional orbit identity and its strict convexity.
    orbit_integrand = z * (r * z - (r - 1)) / (r * (1 - z))
    assert sp.factor(sp.diff(orbit_integrand, z, 2) - 2 / (r * (1 - z) ** 3)) == 0


def verify_two_cycle():
    c = r - 1
    q = (
        (kappa * r + 1) / (r * (kappa + r)),
        (kappa + r) / (r * (kappa * r + 1)),
    )
    survival = (1 - q[1], 1 - q[0])

    # Bd endpoint equations with P the swap and t=(kappa,1/kappa).
    assert sp.factor(kappa * (1 - q[0]) - r * q[0] * (1 - q[1])) == 0
    assert sp.factor((1 - q[1]) / kappa - r * q[1] * (1 - q[0])) == 0
    assert all(
        sp.factor(left - right) == 0
        for left, right in zip(dB_map(survival), survival)
    )

    y0 = tuple(sp.factor(c * entry) for entry in q)
    y1 = dB_map(y0)
    y2 = dB_map(y1)

    D1 = kappa**2 + kappa * r**2 + r - 1
    D2 = kappa**2 * (r - 1) + kappa * r**2 + 1
    D3 = (
        kappa**2 * (r - 1)
        + kappa * r * (2 * r - 1)
        + r**2 * (r - 1)
        + 1
    )
    D4 = (
        kappa**2 * (r**2 * (r - 1) + 1)
        + kappa * r * (2 * r - 1)
        + r
        - 1
    )

    ratio_sum = kappa + 1 / kappa
    A0 = r**4 - 2 * r**3 + r + 1
    B0 = r**5 - r**4 - 3 * r**2 + 3 * r + 2
    endpoint_formula = (
        kappa**2
        * (kappa - 1) ** 2
        * (r - 1)
        * (A0 * ratio_sum + B0)
        / (r * (kappa + r) * (kappa * r + 1) * D1 * D2)
    )
    assert sp.factor(mean(y1) - mean(survival) - endpoint_formula) == 0

    A = r**4 - 2 * r**3 + r - 1
    B = r * (2 * r**4 - 2 * r**3 - 4 * r - 1)
    C = r**6 + 3 * r**4 - 6 * r**3 - 4 * r**2 - 4 * r + 2
    H = A * ratio_sum**2 + B * ratio_sum + C - 2 * A
    reversal_formula = (
        -kappa**3
        * (kappa - 1) ** 2
        * (r - 1) ** 3
        * H
        / (D1 * D2 * D3 * D4)
    )
    assert sp.factor(mean(y2) - mean(y1) - reversal_formula) == 0

    # Palindromic reduction of the original quartic in kappa.
    cleared_H = sp.factor(kappa**2 * H)
    assert sp.Poly(cleared_H, kappa).degree() == 4
    coefficients = sp.Poly(cleared_H, kappa).all_coeffs()
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(coefficients, [A, B, C, B, A])
    )

    # Exact interval signs.  Every polynomial below has positive
    # nonconstant coefficients after r=3/2+v, hence is increasing on
    # 0<=v<=1/100.  Its right endpoint retains the displayed strict sign.
    derivative_at_two = sp.factor(4 * A + B)
    H_at_two = sp.factor(2 * A + 2 * B + C)
    negative_polynomials = [A, derivative_at_two, H_at_two]
    expected_right_values = [
        -Q(117704599, 100000000),
        -Q(50178754149, 5000000000),
        -Q(19376852101199, 1000000000000),
    ]
    for polynomial, expected in zip(negative_polynomials, expected_right_values):
        shifted = sp.Poly(sp.expand(polynomial.subs(r, Q(3, 2) + v)), v)
        ascending = list(reversed(shifted.all_coeffs()))
        assert ascending[0] < 0
        assert all(coefficient > 0 for coefficient in ascending[1:])
        assert sp.factor(polynomial.subs(r, Q(151, 100))) == expected < 0

    # Endpoint positivity for every r>=3/2.
    shifted_A0 = sp.Poly(sp.expand(A0.subs(r, Q(3, 2) + v)), v)
    shifted_floor = sp.Poly(sp.expand((2 * A0 + B0).subs(r, Q(3, 2) + v)), v)
    assert all(coefficient > 0 for coefficient in shifted_A0.all_coeffs())
    assert all(coefficient > 0 for coefficient in shifted_floor.all_coeffs())

    # Concrete rational sawtooth and positive endpoint gap.
    point = {r: Q(3, 2), kappa: Q(2)}
    first_drop = sp.factor((mean(y0) - mean(y1)).subs(point))
    reversal = sp.factor((mean(y2) - mean(y1)).subs(point))
    endpoint = sp.factor((mean(y1) - mean(survival)).subs(point))
    assert first_drop == Q(67, 3780)
    assert reversal == Q(1, 405)
    assert endpoint == Q(23, 3780)
    return first_drop, reversal, endpoint


def main():
    verify_scalar_lyapunov_algebra()
    first_drop, reversal, endpoint = verify_two_cycle()
    print("PASS exact scaled-orbit Lyapunov and two-cycle obstruction")
    print("fitness interval: [3/2, 151/100]")
    print(f"r=3/2, kappa=2 first drop: {first_drop}")
    print(f"r=3/2, kappa=2 immediate reversal: {reversal}")
    print(f"r=3/2, kappa=2 endpoint gap: {endpoint}")


if __name__ == "__main__":
    main()
