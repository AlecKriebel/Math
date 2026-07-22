#!/usr/bin/env python3
"""Dependency-free exact checker for the exported SIC(21) certificate.

This checker independently parses the sparse JSON, reconstructs A=-xi.g,
checks the exact collision, and verifies det(I+sJg)=1 at 66 exact rational
specializations (three Z-points and 22 scalar values apiece).  The symbolic
proof of the determinant identity is in verify_symbolic.py and the note.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def q(value):
    return Fraction(value)


def evaluate(terms, point):
    answer = Fraction(0)
    for term in terms:
        value = q(term["coefficient"])
        for coordinate, exponent in zip(point, term["powers"]):
            value *= coordinate**exponent
        answer += value
    return answer


def derivative_value(terms, variable_index, point):
    answer = Fraction(0)
    for term in terms:
        exponent = term["powers"][variable_index]
        if not exponent:
            continue
        value = q(term["coefficient"]) * exponent
        for index, (coordinate, power) in enumerate(zip(point, term["powers"])):
            if index == variable_index:
                power -= 1
            value *= coordinate**power
        answer += value
    return answer


def determinant(matrix):
    matrix = [row[:] for row in matrix]
    result = Fraction(1)
    size = len(matrix)
    for column in range(size):
        pivot = next((row for row in range(column, size) if matrix[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            result = -result
        pivot_value = matrix[column][column]
        result *= pivot_value
        for j in range(column, size):
            matrix[column][j] /= pivot_value
        for row in range(column + 1, size):
            multiplier = matrix[row][column]
            if multiplier:
                for j in range(column, size):
                    matrix[row][j] -= multiplier * matrix[column][j]
    return result


def canonical_terms(terms):
    return sorted((tuple(term["powers"]), q(term["coefficient"])) for term in terms)


def main():
    payload = json.loads((HERE / "output" / "sic21_sparse.json").read_text())
    assert payload["format"] == "sic21-sparse-certificate-v1"
    assert payload["field"] == "Q"
    assert len(payload["z_variables"]) == len(payload["xi_variables"]) == 21
    assert len(payload["g"]) == 21
    assert sum(len(component) for component in payload["g"]) == 72
    assert len(payload["A"]) == 72

    # Rebuild -xi.g without symbolic algebra and compare every sparse term.
    expected_A = []
    for index, component in enumerate(payload["g"]):
        for term in component:
            xi_powers = [0] * 21
            xi_powers[index] = 1
            expected_A.append(
                (tuple(xi_powers + term["powers"]), -q(term["coefficient"]))
            )
    assert sorted(expected_A) == canonical_terms(payload["A"])
    assert max(sum(term["powers"]) for term in payload["A"]) == 4
    print("[1/4] sparse certificate: A=-xi.g, 72 terms, total degree four")

    points = [[q(coordinate) for coordinate in point] for point in payload["collision_points"]]
    expected_image = [q(coordinate) for coordinate in payload["common_image"]]
    assert len(points) == 3 and len(set(map(tuple, points))) == 3
    assert [point[0] for point in points] == [Fraction(0), Fraction(1), Fraction(-1)]
    for point in points:
        image = [
            point[index] + evaluate(payload["g"][index], point)
            for index in range(21)
        ]
        assert image == expected_image
    print("[2/4] exact rational three-point collision and separating b=Z_1")

    test_points = [
        [Fraction(0) for _ in range(21)],
        [Fraction((index % 5) - 2, 3) for index in range(21)],
        [Fraction((2 * index % 7) - 3, 5) for index in range(21)],
    ]
    scalar_values = [Fraction(value) for value in range(-10, 12)]
    for point in test_points:
        jacobian = [
            [derivative_value(component, column, point) for column in range(21)]
            for component in payload["g"]
        ]
        for scalar in scalar_values:
            matrix = [
                [
                    (Fraction(1) if row == column else Fraction(0))
                    + scalar * jacobian[row][column]
                    for column in range(21)
                ]
                for row in range(21)
            ]
            assert determinant(matrix) == 1
    print("[3/4] determinant pencil: 66 independent exact rational specializations")

    # At a fixed Z, det(I+sJg) has degree at most 21 in s; the 22 distinct
    # checks therefore prove the entire s-polynomial is one at each test Z.
    assert len(set(scalar_values)) == 22
    print("[4/4] each specialized scalar polynomial certified at degree+1 points")
    print("All dependency-free certificate checks passed.")


if __name__ == "__main__":
    main()

