#!/usr/bin/env python3
"""Discover the exact integer degree-moment separator.

This is discovery code and requires NumPy/SciPy.  The independent verifier in
``verifiers/`` uses only exact standard-library arithmetic.
"""

from __future__ import annotations

from fractions import Fraction as Q
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix, hstack, vstack


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
CERTIFICATE = (
    ROOT
    / "certificates"
    / "centered_quarter_integer_degree_obstruction.json"
)


def row_types() -> list[tuple[int, ...]]:
    answer = []
    for d0 in range(2):
        for d1 in range(41 - d0):
            for d2 in range(41 - d0 - d1):
                for d3 in range(41 - d0 - d1 - d2):
                    remainder = 40 - d0 - d1 - d2 - d3
                    for d5 in range(remainder + 1):
                        twice_d6 = (
                            -4 + 4 * d0 + 3 * d1 + 2 * d2 + d3 - d5
                        )
                        if twice_d6 < 0 or twice_d6 % 2:
                            continue
                        d6 = twice_d6 // 2
                        d4 = remainder - d5 - d6
                        if d4 >= 0:
                            answer.append(
                                (d0, d1, d2, d3, d4, d5, d6)
                            )
    return answer


def primitive_null_vector(matrix: list[list[int]]) -> list[int]:
    """Return the primitive vector spanning a corank-one rational nullspace."""
    work = [[Q(value) for value in row] for row in matrix]
    row = 0
    pivots: list[int] = []
    for column in range(len(work[0])):
        pivot = next(
            (index for index in range(row, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        scale = work[row][column]
        work[row] = [value / scale for value in work[row]]
        for index in range(len(work)):
            if index != row and work[index][column]:
                scale = work[index][column]
                work[index] = [
                    value - scale * pivot_value
                    for value, pivot_value in zip(work[index], work[row])
                ]
        pivots.append(column)
        row += 1
    free = [
        column
        for column in range(len(work[0]))
        if column not in pivots
    ]
    assert len(free) == 1
    vector = [Q(0) for _ in work[0]]
    vector[free[0]] = 1
    for index, column in reversed(list(enumerate(pivots))):
        vector[column] = -sum(
            work[index][other] * vector[other] for other in free
        )
    denominator = math.lcm(*(value.denominator for value in vector))
    integers = [int(value * denominator) for value in vector]
    divisor = math.gcd(*(abs(value) for value in integers))
    return [value // divisor for value in integers]


def main() -> None:
    source = json.loads(SOURCE.read_text())
    alpha = [Q(value) for value in source["alpha"]]
    nu = [Q(value) for value in source["nu"]]
    moments = [[Q(0) for _ in range(7)] for _ in range(7)]
    for index, mass in enumerate(alpha):
        moments[index][index] += mass
    for triple, mass in zip(source["triple_orbits"], nu):
        orbit = set(itertools.permutations(triple))
        for i, j, _k in orbit:
            moments[i][j] += mass / len(orbit)

    types = row_types()
    pairs = [(i, j) for i in range(7) for j in range(i, 7)]
    features = np.array(
        [
            [1, *degree, *(degree[i] * degree[j] for i, j in pairs)]
            for degree in types
        ],
        dtype=float,
    )
    target = np.array(
        [
            1,
            *(float(value) for value in alpha),
            *(float(moments[i][j]) for i, j in pairs),
        ]
    )

    # y=y_plus-y_minus; enforce P(d)=feature(d).y >= 0 and E[P]<=-1.
    constraints = hstack(
        [-csc_matrix(features), csc_matrix(features)],
        format="csc",
    )
    constraints = vstack(
        [
            constraints,
            csc_matrix(np.r_[target, -target].reshape(1, -1)),
        ],
        format="csc",
    )
    result = linprog(
        np.ones(2 * features.shape[1]),
        A_ub=constraints,
        b_ub=np.r_[np.zeros(len(types)), -1],
        bounds=(0, None),
        method="highs",
    )
    assert result.success
    separator = (
        result.x[: features.shape[1]]
        - result.x[features.shape[1] :]
    )
    active = np.flatnonzero(abs(features @ separator) < 1e-7)
    support = np.flatnonzero(abs(separator) > 1e-7)
    assert len(active) == 16 and len(support) == 17
    assert all(index >= 8 for index in support)

    supported_pairs = [pairs[index - 8] for index in support]
    exact_matrix = [
        [types[index][i] * types[index][j] for i, j in supported_pairs]
        for index in active
    ]
    coefficients = primitive_null_vector(exact_matrix)
    expectation = sum(
        coefficient * moments[i][j]
        for (i, j), coefficient in zip(supported_pairs, coefficients)
    )
    if expectation > 0:
        coefficients = [-value for value in coefficients]
        expectation = -expectation

    expected = json.loads(CERTIFICATE.read_text())
    expected_terms = [
        (tuple(item["indices"]), item["coefficient"])
        for item in expected["quadratic_terms"]
    ]
    assert list(zip(supported_pairs, coefficients)) == expected_terms
    assert expectation == Q(expected["expected_value"]) < 0
    print(
        json.dumps(
            {
                "row_types": len(types),
                "active_types": len(active),
                "support_terms": len(support),
                "expected_value": str(expectation),
                "quadratic_terms": expected["quadratic_terms"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
