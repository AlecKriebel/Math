#!/usr/bin/env python3
"""Find and exactly reconstruct an integer row-degree moment separator.

The floating LP is used only to discover an exposed face.  The emitted
certificate is reconstructed from an exact rational nullspace and then
checked on all 27,041 integer row types before it is written.
"""

from __future__ import annotations

from fractions import Fraction as Q
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix, hstack, vstack


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


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


def moments(source: dict[str, object]) -> tuple[list[Q], list[list[Q]]]:
    alpha = [Q(value) for value in source["alpha"]]
    matrix = [[Q(0) for _ in range(7)] for _ in range(7)]
    for index, mass in enumerate(alpha):
        matrix[index][index] += mass
    for triple, mass_text in zip(source["triple_orbits"], source["nu"]):
        mass = Q(mass_text)
        orbit = set(itertools.permutations(triple))
        for i, j, _k in orbit:
            matrix[i][j] += mass / len(orbit)
    return alpha, matrix


def primitive_null_vector(matrix: list[list[int]]) -> list[int]:
    work = [[Q(value) for value in row] for row in matrix]
    row = 0
    pivots = []
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
    vector = [Q(0)] * len(work[0])
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    source_path = args.source.resolve()
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    alpha, matrix = moments(source)
    types = row_types()
    pairs = [(i, j) for i in range(7) for j in range(i, 7)]
    features_exact = [
        [1, *degree, *(degree[i] * degree[j] for i, j in pairs)]
        for degree in types
    ]
    target_exact = [
        Q(1),
        *alpha,
        *(matrix[i][j] for i, j in pairs),
    ]
    features = np.asarray(features_exact, dtype=float)
    target = np.asarray([float(value) for value in target_exact])

    feasibility = linprog(
        np.zeros(len(types)),
        A_eq=csc_matrix(features.T),
        b_eq=target,
        bounds=(0, None),
        method="highs",
    )
    if feasibility.success:
        report = {
            "status": "NUMERICALLY_FEASIBLE",
            "warning": "floating discovery result; exact weights not reconstructed",
            "row_types": len(types),
            "active_row_types": int(
                np.count_nonzero(feasibility.x > 1.0e-9)
            ),
            "maximum_equality_residual": float(
                np.max(abs(features.T @ feasibility.x - target))
            ),
        }
        print(json.dumps(report, indent=2))
        return

    # y=y_plus-y_minus, feature(d).y >= 0, and target.y <= -1.
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
    active = np.flatnonzero(abs(features @ separator) < 1.0e-7)
    support = np.flatnonzero(abs(separator) > 1.0e-7)
    # Linear and constant terms can be eliminated using sum(d_i)=40.  The
    # observed sparse facets already use only quadratic terms.
    assert all(index >= 8 for index in support)
    supported_pairs = [pairs[index - 8] for index in support]
    exact_face = [
        [
            types[row][i] * types[row][j]
            for i, j in supported_pairs
        ]
        for row in active
    ]
    coefficients = primitive_null_vector(exact_face)
    expectation = sum(
        coefficient * matrix[i][j]
        for (i, j), coefficient in zip(supported_pairs, coefficients)
    )
    if expectation > 0:
        coefficients = [-value for value in coefficients]
        expectation = -expectation

    values = [
        sum(
            coefficient * degree[i] * degree[j]
            for (i, j), coefficient in zip(supported_pairs, coefficients)
        )
        for degree in types
    ]
    assert min(values) == 0 and expectation < 0
    positive = [value for value in values if value > 0]
    certificate = {
        "schema": "kissing5.centered_quarter_integer_degree_obstruction.v1",
        "status": (
            "exact obstruction to the named pair/triple "
            "pseudodistribution; not an upper bound for spherical codes"
        ),
        "source_certificate": source_path.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "cardinality": 41,
        "grid_numerators_over_four": [-4, -3, -2, -1, 0, 1, 2],
        "row_type_constraints": {
            "degree_sum": 40,
            "weighted_degree_sum": -4,
            "antipode_degree_upper_bound": 1,
        },
        "quadratic_terms": [
            {
                "indices": list(pair),
                "coefficient": coefficient,
            }
            for pair, coefficient in zip(supported_pairs, coefficients)
        ],
        "enumeration": {
            "total_row_types": len(types),
            "row_types_with_antipode": sum(
                degree[0] == 1 for degree in types
            ),
            "row_types_without_antipode": sum(
                degree[0] == 0 for degree in types
            ),
            "zero_count": values.count(0),
            "minimum_positive_value": min(positive),
            "maximum_value": max(values),
        },
        "expected_value": qstr(expectation),
        "discovery": {
            "floating_active_face_size": len(active),
            "floating_support_size": len(support),
        },
    }
    text = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
