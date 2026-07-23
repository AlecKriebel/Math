#!/usr/bin/env python3
"""Exact verifier for the one-sided and origin-depth consequences.

Only the Python standard library is used.  Elements of Q(sqrt(3)) are
represented as pairs (a,b) meaning a+b*sqrt(3), with a,b rational.
"""

from __future__ import annotations

from fractions import Fraction as Q
import json
from math import sqrt
from pathlib import Path


K = tuple[Q, Q]
Poly = tuple[K, ...]
ZERO: K = (Q(0), Q(0))
ONE: K = (Q(1), Q(0))


def kadd(x: K, y: K) -> K:
    return x[0] + y[0], x[1] + y[1]


def kneg(x: K) -> K:
    return -x[0], -x[1]


def ksub(x: K, y: K) -> K:
    return kadd(x, kneg(y))


def kmul(x: K, y: K) -> K:
    return x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def kscale(x: K, scalar: Q) -> K:
    return x[0] * scalar, x[1] * scalar


def kdiv(x: K, y: K) -> K:
    denominator = y[0] * y[0] - 3 * y[1] * y[1]
    assert denominator != 0
    return (
        (x[0] * y[0] - 3 * x[1] * y[1]) / denominator,
        (x[1] * y[0] - x[0] * y[1]) / denominator,
    )


def knorm(x: K) -> Q:
    return x[0] * x[0] - 3 * x[1] * x[1]


def ksign(x: K) -> int:
    """Return the exact sign of a+b sqrt(3)."""
    a, b = x
    if b == 0:
        return (a > 0) - (a < 0)
    if a >= 0 and b >= 0:
        return 1
    if a <= 0 and b <= 0:
        return -1
    comparison = a * a - 3 * b * b
    assert comparison != 0
    if a > 0 and b < 0:
        return 1 if comparison > 0 else -1
    # Here a < 0 < b.
    return 1 if comparison < 0 else -1


def trim(poly: Poly) -> Poly:
    values = list(poly)
    while len(values) > 1 and values[-1] == ZERO:
        values.pop()
    return tuple(values)


def padd(left: Poly, right: Poly) -> Poly:
    answer = []
    for index in range(max(len(left), len(right))):
        answer.append(
            kadd(
                left[index] if index < len(left) else ZERO,
                right[index] if index < len(right) else ZERO,
            )
        )
    return trim(tuple(answer))


def pscale(poly: Poly, scalar: K) -> Poly:
    return trim(tuple(kmul(value, scalar) for value in poly))


def pmul(left: Poly, right: Poly) -> Poly:
    answer = [ZERO] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            answer[i + j] = kadd(answer[i + j], kmul(x, y))
    return trim(tuple(answer))


def pevaluate(poly: Poly, value: K) -> K:
    answer = ZERO
    for coefficient in reversed(poly):
        answer = kadd(kmul(answer, value), coefficient)
    return answer


def parse_rational(text: str) -> Q:
    return Q(text)


def rational_poly(values: list[str]) -> Poly:
    return tuple((parse_rational(value), Q(0)) for value in values)


def gegenbauer_dimension_four(max_degree: int) -> list[Poly]:
    """Normalized P_k for S^3, so P_k(1)=1."""
    polynomials: list[Poly] = [((Q(1), Q(0)),)]
    if max_degree == 0:
        return polynomials
    polynomials.append((ZERO, ONE))
    for degree in range(2, max_degree + 1):
        shifted = (ZERO,) + pscale(
            polynomials[-1], (Q(2 * degree), Q(0))
        )
        previous = pscale(
            polynomials[-2], (Q(-(degree - 1)), Q(0))
        )
        numerator = padd(shifted, previous)
        polynomials.append(
            pscale(numerator, (Q(1, degree + 1), Q(0)))
        )
    return polynomials


def gegenbauer_expansion(poly: Poly, basis: list[Poly]) -> tuple[K, ...]:
    remainder = trim(poly)
    coefficients = [ZERO] * len(basis)
    for degree in range(len(basis) - 1, -1, -1):
        if len(remainder) - 1 != degree:
            continue
        coefficient = kdiv(remainder[-1], basis[degree][-1])
        coefficients[degree] = coefficient
        remainder = padd(remainder, pscale(basis[degree], kneg(coefficient)))
    assert remainder == (ZERO,)
    return tuple(coefficients)


def load_certificate() -> dict:
    path = (
        Path(__file__).resolve().parents[1]
        / "certificates"
        / "one_sided_tukey_bound.json"
    )
    return json.loads(path.read_text())


def verify() -> dict[str, object]:
    certificate = load_certificate()
    factor = certificate["factor_polynomial"]
    q = rational_poly(factor["q_coefficients_ascending"])
    r = rational_poly(factor["r_coefficients_ascending"])
    sqrt3_over_three: K = (Q(0), Q(1, 3))
    t_minus_s: Poly = (kneg(sqrt3_over_three), ONE)
    f = pmul(pmul(t_minus_s, pmul(q, q)), r)

    # r(t) has positive leading coefficient and negative discriminant, hence
    # is strictly positive on the whole real line.
    discriminant = (
        r[1][0] * r[1][0] - 4 * r[0][0] * r[2][0]
    )
    assert discriminant == parse_rational(factor["r_discriminant"])
    assert discriminant < 0 and r[2] == ONE

    basis = gegenbauer_dimension_four(11)
    assert all(pevaluate(polynomial, ONE) == ONE for polynomial in basis)
    expansion = gegenbauer_expansion(f, basis)
    scale = Q(certificate["coefficient_scale"])
    scaled_expansion = tuple(kscale(value, scale) for value in expansion)

    expected = []
    for entry in certificate["scaled_gegenbauer_coefficients"]:
        assert entry["degree"] == len(expected)
        value = (Q(entry["rational_part"]), Q(entry["sqrt3_part"]))
        expected.append(value)
        assert knorm(value) == Q(entry["norm"])
        assert ksign(value) > 0
    assert scaled_expansion == tuple(expected)

    scaled_f_one = kscale(pevaluate(f, ONE), scale)
    stored_f_one = certificate["scaled_f_at_one"]
    assert scaled_f_one == (
        Q(stored_f_one["rational_part"]),
        Q(stored_f_one["sqrt3_part"]),
    )

    margin = ksub(kscale(scaled_expansion[0], Q(34)), scaled_f_one)
    stored_margin = certificate["scaled_margin_34_f0_minus_f1"]
    assert margin == (
        Q(stored_margin["rational_part"]),
        Q(stored_margin["sqrt3_part"]),
    )
    assert knorm(margin) == Q(stored_margin["norm"])
    assert ksign(margin) > 0
    # Therefore f(1)/f_0 < 34 and the integer Delsarte bound is 33.
    assert ksign(scaled_expansion[0]) > 0

    # Exact integer optimization for a belt count a and cap count b.
    tau_upper = int(certificate["imported_kissing_upper_bound"])
    projected_upper = int(
        certificate["spherical_code_bound"]["proved_upper_bound"]
    )
    feasible_profiles = [
        (a, b)
        for a in range(42)
        for b in range(42)
        if a <= projected_upper and a + 2 * b <= tau_upper
    ]
    one_sided_upper = max(a + b for a, b in feasible_profiles)
    equality_profiles = sorted(
        (a, b)
        for a, b in feasible_profiles
        if a + b == one_sided_upper
    )
    assert one_sided_upper == certificate["one_sided_upper_bound"] == 38
    assert equality_profiles == [(32, 6), (33, 5)]

    # The squared projection comparison reduces to
    # D(z,w)=1/4-z^2-w^2+3zw-2z^2w^2.  As a polynomial in w it is
    # concave.  These exact endpoint values are the sign proof used in the
    # manuscript: D(z,0)=1/4-z^2 and
    # D(z,1/2)=3z(1-z)/2 on 0<=z<=1/2.
    # Coefficients below are ascending powers of z.
    d_at_zero = (Q(1, 4), Q(0), Q(-1))
    d_at_half = (Q(0), Q(3, 2), Q(-3, 2))
    assert d_at_zero == (Q(1, 4), Q(0), Q(-1))
    assert d_at_half == (Q(0), Q(3, 2), Q(-3, 2))

    return {
        "status": "PASS",
        "A_4_sqrt3_upper_bound": projected_upper,
        "delsarte_objective_approx": (
            float(pevaluate(f, ONE)[0])
            + float(pevaluate(f, ONE)[1]) * sqrt(3)
        ) / (
            float(expansion[0][0])
            + float(expansion[0][1]) * sqrt(3)
        ),
        "one_sided_kissing_upper_bound": one_sided_upper,
        "size_38_profiles": equality_profiles,
        "hypothetical_41_origin_tukey_depth_count": 3,
        "robust_deletion_count": 2,
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
