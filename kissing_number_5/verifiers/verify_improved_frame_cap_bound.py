#!/usr/bin/env python3
"""Exact verifier for proofs/improved_frame_cap_bound.md."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Optional


Q = Fraction
ROOT = Path(__file__).resolve().parents[1]


def polynomial_add(a: list[Q], b: list[Q]) -> list[Q]:
    result = [Q(0)] * max(len(a), len(b))
    for index, value in enumerate(a):
        result[index] += value
    for index, value in enumerate(b):
        result[index] += value
    return result


def polynomial_scale(a: list[Q], scalar: Q) -> list[Q]:
    return [scalar * value for value in a]


def polynomial_multiply(a: list[Q], b: list[Q]) -> list[Q]:
    result = [Q(0)] * (len(a) + len(b) - 1)
    for i, first in enumerate(a):
        for j, second in enumerate(b):
            result[i + j] += first * second
    return result


def gegenbauer_4_basis(maximum_degree: int) -> list[list[Q]]:
    basis = [[Q(1)]]
    if maximum_degree == 0:
        return basis
    basis.append([Q(0), Q(1)])
    for k in range(1, maximum_degree):
        shifted = [Q(0)] + basis[k]
        numerator = polynomial_add(
            polynomial_scale(shifted, Q(2 * (k + 1))),
            polynomial_scale(basis[k - 1], Q(-k)),
        )
        basis.append(polynomial_scale(numerator, Q(1, k + 2)))
    return basis


def expand_in_triangular_basis(
    polynomial: list[Q], basis: list[list[Q]]
) -> list[Q]:
    remainder = polynomial[:]
    coefficients = [Q(0)] * len(basis)
    for degree in range(len(basis) - 1, -1, -1):
        coefficient = remainder[degree] / basis[degree][degree]
        coefficients[degree] = coefficient
        for index, value in enumerate(basis[degree]):
            remainder[index] -= coefficient * value
    assert all(value == 0 for value in remainder)
    return coefficients


def verify(certificate_path: Optional[Path] = None) -> dict[str, object]:
    if certificate_path is None:
        certificate_path = (
            ROOT / "certificates" / "improved_frame_cap_bound.json"
        )
    data = json.loads(certificate_path.read_text())
    assert data["schema"] == "improved-frame-cap-bound-v1"
    assert data["ambient_dimension"] == 5
    assert data["projected_dimension"] == 4
    assert data["cardinality"] == 41

    c = Q(data["slab_half_width"])
    s = Q(data["projected_max_inner_product"])
    assert c == Q(37, 200)
    assert s == (Q(1, 2) + c**2) / (1 - c**2)
    assert s == Q(7123, 12877)

    q = [Q(value) for value in data["q_coefficients_ascending"]]
    r = [Q(value) for value in data["r_coefficients_ascending"]]
    assert q == [Q(11, 2000), Q(157, 1000), Q(1729, 2000), Q(329, 200), Q(1)]
    assert r == [Q(2119, 2000), -Q(4013, 2000), Q(1)]
    discriminant = r[1] ** 2 - 4 * r[0] * r[2]
    assert discriminant == Q(data["r_discriminant"])
    assert discriminant < 0

    polynomial = polynomial_multiply(
        [-s, Q(1)],
        polynomial_multiply(polynomial_multiply(q, q), r),
    )
    basis = gegenbauer_4_basis(11)
    coefficients = expand_in_triangular_basis(polynomial, basis)
    expected = [Q(value) for value in data["gegenbauer_coefficients"]]
    assert coefficients == expected
    assert all(coefficient > 0 for coefficient in coefficients)

    value_at_one = sum(polynomial)
    objective = value_at_one / coefficients[0]
    assert objective == Q(data["delsarte_objective"])
    margin = 31 - objective
    assert margin == Q(data["objective_margin_below_31"])
    assert margin > 0
    assert data["projected_code_integer_bound"] == 30

    outside_count = 41 - data["projected_code_integer_bound"]
    frame_bound = outside_count * c**2
    assert outside_count == data["outside_slab_count"] == 11
    assert frame_bound == Q(data["frame_lower_bound"])
    assert frame_bound == Q(15059, 40000)
    assert frame_bound > Q(9, 25)

    # Exact centered localizing determinant from the strengthened support.
    mean = Q(41, 5)
    h = mean - frame_bound
    assert h == Q(312941, 40000)
    # A small-variance D=0 completion z=(a,-a,a,-a,0) remains feasible:
    # take a=1/2, so V=1 and all eigenvalues exceed the cap bound.
    a = Q(1, 2)
    spectrum = [mean + a, mean - a, mean + a, mean - a, mean]
    assert min(spectrum) > frame_bound
    variance = sum((value - mean) ** 2 for value in spectrum)
    third = sum((value - mean) ** 3 for value in spectrum)
    assert variance == 1
    assert third == 0
    localizing_determinant = 5 * h * (h * variance + third) - variance**2
    assert localizing_determinant > 0

    return {
        "status": "PASS",
        "projected_max_inner_product": str(s),
        "minimum_gegenbauer_coefficient": str(min(coefficients)),
        "r_discriminant": str(discriminant),
        "delsarte_objective": str(objective),
        "objective_margin_below_31": str(margin),
        "projected_code_bound": 30,
        "strict_frame_lower_bound": str(frame_bound),
        "previous_frame_lower_bound": str(Q(9, 25)),
        "small_variance_completion_survives": True,
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
