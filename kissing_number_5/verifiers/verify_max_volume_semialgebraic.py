#!/usr/bin/env python3
"""Dependency-free exact verifier for the maximum-volume reduction constants."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path


def add(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * max(len(a), len(b))
    for i, value in enumerate(a):
        out[i] += value
    for i, value in enumerate(b):
        out[i] += value
    return trim(out)


def scale(a: list[Fraction], c: Fraction) -> list[Fraction]:
    return trim([c * value for value in a])


def multiply(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def trim(a: list[Fraction]) -> list[Fraction]:
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def gegenbauer_n4(max_degree: int) -> list[list[Fraction]]:
    """Return normalized P_k^(4), in ascending monomial order."""
    basis = [[Fraction(1)], [Fraction(0), Fraction(1)]]
    for k in range(1, max_degree):
        two_t_pk = [Fraction(0)] + [
            2 * (k + 1) * value for value in basis[k]
        ]
        numerator = add(two_t_pk, scale(basis[k - 1], Fraction(-k)))
        basis.append(scale(numerator, Fraction(1, k + 2)))
    return basis[: max_degree + 1]


def expand_in_triangular_basis(
    polynomial: list[Fraction], basis: list[list[Fraction]]
) -> list[Fraction]:
    remainder = polynomial[:] + [Fraction(0)] * (
        len(basis) - len(polynomial)
    )
    coefficients = [Fraction(0)] * len(basis)
    for k in range(len(basis) - 1, -1, -1):
        coefficient = remainder[k] / basis[k][k]
        coefficients[k] = coefficient
        for j, value in enumerate(basis[k]):
            remainder[j] -= coefficient * value
    assert all(value == 0 for value in remainder)
    return coefficients


def parse_fraction(text: str) -> Fraction:
    return Fraction(text)


def verify(certificate_path: Path) -> dict[str, object]:
    data = json.loads(certificate_path.read_text(encoding="utf-8"))
    assert data["ambient_dimension"] == 5
    assert data["point_count"] == 41
    assert data["projection_dimension"] == 4

    slab = parse_fraction(data["slab_half_width"])
    projected_s = parse_fraction(data["projected_max_inner_product"])
    projected_bound = int(data["projected_code_upper_bound"])
    frame_bound = parse_fraction(data["frame_lower_bound"])

    assert slab == Fraction(1, 5)
    assert (Fraction(1, 2) + slab * slab) / (1 - slab * slab) == projected_s
    assert projected_s == Fraction(9, 16)
    assert projected_bound == 32
    assert (41 - projected_bound) * slab * slab == frame_bound
    assert frame_bound == Fraction(9, 25)

    t_plus_one = [Fraction(1), Fraction(1)]
    t_minus_s = [-projected_s, Fraction(1)]
    t_plus_a = [Fraction(11, 16), Fraction(1)]
    t_plus_b = [Fraction(3, 32), Fraction(1)]
    polynomial = t_plus_one
    for factor in (t_minus_s, t_plus_a, t_plus_a, t_plus_b, t_plus_b):
        polynomial = multiply(polynomial, factor)

    basis = gegenbauer_n4(6)
    actual_coefficients = expand_in_triangular_basis(polynomial, basis)
    expected_coefficients = [
        parse_fraction(value) for value in data["gegenbauer_coefficients"]
    ]
    assert actual_coefficients == expected_coefficients
    assert all(value > 0 for value in actual_coefficients)

    # The factor locations and even multiplicities certify f <= 0 on [-1,s].
    assert Fraction(-1) <= -Fraction(11, 16) <= projected_s
    assert Fraction(-1) <= -Fraction(3, 32) <= projected_s

    f_at_one = sum(polynomial)
    objective = f_at_one / actual_coefficients[0]
    assert objective == parse_fraction(data["lp_objective"])
    assert objective < 33

    subset_count = math.comb(41, 5)
    determinant_lower = (
        frame_bound**4 * (Fraction(41) - 4 * frame_bound) / subset_count
    )
    expected_determinant_lower = parse_fraction(
        data["basis_gram_determinant_lower_bound"]
    )
    assert determinant_lower == expected_determinant_lower
    assert determinant_lower > 0
    eigenvalue_lower = Fraction(256, 625) * determinant_lower
    assert eigenvalue_lower == parse_fraction(
        data["basis_gram_eigenvalue_lower_bound"]
    )

    counts = data["maximum_volume_minor_counts"]
    expected_counts = {
        "zero_nonbasis_columns": 1,
        "one_nonbasis_column": math.comb(36, 1) * math.comb(5, 1),
        "two_nonbasis_columns": math.comb(36, 2) * math.comb(5, 2),
        "three_nonbasis_columns": math.comb(36, 3) * math.comb(5, 3),
        "four_nonbasis_columns": math.comb(36, 4) * math.comb(5, 4),
        "five_nonbasis_columns": math.comb(36, 5) * math.comb(5, 5),
    }
    expected_counts["total"] = sum(expected_counts.values())
    assert counts == expected_counts
    assert counts["total"] == subset_count

    variable_counts = data["variable_counts"]
    assert variable_counts["basis_gram_off_diagonal"] == math.comb(5, 2)
    assert variable_counts["nonbasis_coefficient"] == 36 * 5
    assert variable_counts["total"] == math.comb(5, 2) + 36 * 5
    assert variable_counts["unit_norm_equalities"] == 36
    assert (
        variable_counts["intrinsic_after_norm_equalities"]
        == variable_counts["total"] - 36
    )

    return {
        "status": "PASS",
        "lp_objective": str(objective),
        "projected_code_upper_bound": projected_bound,
        "strict_frame_lower_bound": str(frame_bound),
        "basis_gram_determinant_lower_bound": str(determinant_lower),
        "basis_gram_eigenvalue_lower_bound": str(eigenvalue_lower),
        "semialgebraic_variable_count": variable_counts["total"],
        "maximum_volume_minor_count": counts["total"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificate",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "certificates"
        / "max_volume_semialgebraic_reduction.json",
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate), sort_keys=True))


if __name__ == "__main__":
    main()
