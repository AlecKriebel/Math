#!/usr/bin/env python3
"""Exact checks for the Tverberg degree-two moment barrier."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def assemble(blocks):
    out = []
    for block_row in blocks:
        for i in range(len(block_row[0])):
            out.append(sum((block[i] for block in block_row), []))
    return out


def multiply_polynomial(poly, factor):
    out = {}
    for exponent, coefficient in poly.items():
        for variable, value in factor.items():
            new_exponent = list(exponent)
            if variable is not None:
                new_exponent[variable] += 1
            key = tuple(new_exponent)
            out[key] = out.get(key, F(0)) + coefficient * value
    return out


def interval_product(number_of_lower_factors):
    # Variables are A,B,C.  An upper factor is 1+X and a lower factor
    # is 1/2-X.  By symmetry only the number of lower factors matters.
    poly = {(0, 0, 0): F(1)}
    for variable in range(3):
        if variable < number_of_lower_factors:
            factor = {None: F(1, 2), variable: F(-1)}
        else:
            factor = {None: F(1), variable: F(1)}
        poly = multiply_polynomial(poly, factor)
    return poly


def moment_coefficients(poly):
    # Each variable has exponent at most one. Map 0,1,2,3 distinct
    # variables to the moments 1,u,v,w.
    out = [F(0)] * 4
    for exponent, coefficient in poly.items():
        assert all(value in (0, 1) for value in exponent)
        out[sum(exponent)] += coefficient
    return out


def verify(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["schema"] == "tverberg-degree-two-counterexample-v1"
    n = data["block_size"]
    assert n == 6
    d, a, b, c = (data[name] for name in ("D", "A", "B", "C"))
    assert all(len(matrix) == n and all(len(row) == n for row in matrix)
               for matrix in (d, a, b, c))
    assert d == [[5 if i == j else -1 for j in range(n)] for i in range(n)]

    matrix = assemble([
        [d, a, b],
        [transpose(a), d, c],
        [transpose(b), transpose(c), d],
    ])
    size = 3 * n
    assert matrix == transpose(matrix)
    assert [sum(row) for row in matrix] == [0] * size
    assert sum(matrix[i][i] for i in range(size)) == 90
    square = matmul(matrix, matrix)
    assert square == [[18 * matrix[i][j] for j in range(size)]
                      for i in range(size)]
    assert all(matrix[i][i] == 5 for i in range(size))
    off_diagonal = {
        matrix[i][j] for i in range(size) for j in range(size) if i != j
    }
    assert off_diagonal == {-4, -1, 2}
    assert max(F(value, 5) for value in off_diagonal) == F(2, 5) < F(1, 2)

    expected = [
        [F(1), F(3), F(3), F(1)],
        [F(1, 2), F(0), F(-3, 2), F(-1)],
        [F(1, 4), F(-3, 4), F(0), F(1)],
        [F(1, 8), F(-3, 4), F(3, 2), F(-1)],
    ]
    actual = [
        moment_coefficients(interval_product(lower_count))
        for lower_count in range(4)
    ]
    assert actual == expected

    # Calibration at m=0, M=I/5.
    u, v, w = F(0), F(0), F(1, 25)
    moments = [F(1), u, v, w]
    assert all(sum(c0 * m0 for c0, m0 in zip(row, moments)) > 0
               for row in actual)

    return {
        "status": "PASS",
        "order": size,
        "rank": 5,
        "maximum_inner_product": "2/5",
        "interval_factor_moment_coefficients": [
            [str(value) for value in row] for row in actual
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificate",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "certificates"
        / "tverberg_moment_counterexample.json",
    )
    print(json.dumps(verify(parser.parse_args().certificate), sort_keys=True))


if __name__ == "__main__":
    main()
