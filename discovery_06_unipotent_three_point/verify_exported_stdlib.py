#!/usr/bin/env python3
"""Dependency-free exact rational checks of the exported Discovery 06 map."""

from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "output" / "unipotent14_sparse.json"


def number(text):
    return Fraction(text)


def evaluate_sparse(terms, point):
    result = Fraction(0)
    for term in terms:
        value = number(term["coefficient"])
        for coordinate, exponent in zip(point, term["powers"]):
            value *= coordinate**exponent
        result += value
    return result


def derivative_value(terms, variable_index, point):
    result = Fraction(0)
    for term in terms:
        exponent = term["powers"][variable_index]
        if exponent == 0:
            continue
        value = number(term["coefficient"]) * exponent
        for index, (coordinate, power) in enumerate(zip(point, term["powers"])):
            value *= coordinate ** (power - (index == variable_index))
        result += value
    return result


def matmul(left, right):
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(len(right))), Fraction(0))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def identity(size):
    return [
        [Fraction(int(row == column)) for column in range(size)]
        for row in range(size)
    ]


def determinant(matrix):
    work = [row[:] for row in matrix]
    value = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value = -value
        pivot_value = work[column][column]
        value *= pivot_value
        for row in range(column + 1, len(work)):
            ratio = work[row][column] / pivot_value
            for entry in range(column, len(work)):
                work[row][entry] -= ratio * work[column][entry]
    return value


def rank(matrix):
    work = [row[:] for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next((item for item in range(row, len(work)) if work[item][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        pivot_value = work[row][column]
        work[row] = [value / pivot_value for value in work[row]]
        for other in range(len(work)):
            if other == row:
                continue
            ratio = work[other][column]
            work[other] = [
                left - ratio * right for left, right in zip(work[other], work[row])
            ]
        row += 1
        if row == len(work):
            break
    return row


def coefficient(m):
    if m % 3 == 0:
        k = m // 3
        return Fraction((-1) ** k * comb(3 * k + 1, k), 2 ** (2 * k + 1))
    if m % 3 == 1:
        k = (m - 1) // 3
        return Fraction(
            (-1) ** (k + 1) * 3 * comb(3 * k + 1, k),
            (3 * k + 1) * 2 ** (2 * k + 1),
        )
    k = (m - 2) // 3
    return Fraction((-1) ** k * comb(3 * k + 4, k + 1), 2 ** (2 * k + 3))


def main():
    payload = json.loads(CERTIFICATE.read_text())
    assert payload["format"] == "unipotent14-sparse-certificate-v1"
    assert len(payload["variables"]) == len(payload["g"]) == 14
    assert sum(len(component) for component in payload["g"]) == 24
    assert len(payload["A"]) == 24
    assert max(sum(term["powers"]) for term in payload["A"]) == 8
    print("[1/4] dimensions and sparsity: 14 coordinates, 24 terms, degree(A)=8")

    points = [[number(value) for value in point] for point in payload["collision_points"]]
    images = []
    for point in points:
        images.append(
            tuple(
                point[index] + evaluate_sparse(component, point)
                for index, component in enumerate(payload["g"])
            )
        )
    expected = tuple(number(value) for value in payload["common_image"])
    assert len(set(map(tuple, points))) == 3
    assert images == [expected] * 3
    print("[2/4] exact exported three-point collision")

    # Independent exact pointwise guards for the determinant pencil and the
    # regular-nilpotent specialization.
    samples = [
        [Fraction(2), Fraction(3), Fraction(5)] + [Fraction(0)] * 11,
        [Fraction(-1), Fraction(2), Fraction(4)] + [Fraction(0)] * 11,
        [Fraction(3), Fraction(-2), Fraction(1)] + [Fraction(0)] * 11,
    ]
    for point in samples:
        jacobian = [
            [derivative_value(component, column, point) for column in range(14)]
            for component in payload["g"]
        ]
        for scalar in range(1, 15):
            pencil = [
                [
                    Fraction(int(row == column)) + scalar * jacobian[row][column]
                    for column in range(14)
                ]
                for row in range(14)
            ]
            assert determinant(pencil) == 1
    point = samples[0]
    jacobian = [
        [derivative_value(component, column, point) for column in range(14)]
        for component in payload["g"]
    ]
    power = identity(14)
    for _ in range(13):
        power = matmul(power, jacobian)
    assert power[0][4] == -3 * point[0] ** 6 * point[1] ** 4 * point[2]
    assert matmul(power, jacobian) == [[Fraction(0)] * 14 for _ in range(14)]
    assert rank(jacobian) == 13
    print("[3/4] exact independent pencil and nilpotency specializations")

    assert all(coefficient(m) != 0 for m in range(1000))
    print("[4/4] closed SIC coefficient formulas are nonzero through m=999")
    print("All dependency-free certificate checks passed.")


if __name__ == "__main__":
    main()
