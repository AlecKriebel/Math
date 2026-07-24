#!/usr/bin/env python3
"""Find and exactly reconstruct a noncentered integer-row moment mixture.

HiGHS is used only to select a small support from the complete 855,168-row
superset.  The emitted weights are then solved and checked with
``fractions.Fraction`` against every exact first and second moment.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix

from verifiers.verify_fixed41_noncentered_integer_degree_obstruction import (
    pair_moment_matrix,
    row_types,
)


def solve_rectangular(
    matrix: list[list[Q]], rhs: list[Q]
) -> list[Q]:
    """Solve an overdetermined full-column-rank rational system."""

    rows = [
        [Q(value) for value in row] + [Q(target)]
        for row, target in zip(matrix, rhs, strict=True)
    ]
    variable_count = len(matrix[0])
    pivot_row = 0
    pivots = []
    for column in range(variable_count):
        pivot = next(
            (
                index
                for index in range(pivot_row, len(rows))
                if rows[index][column]
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for index in range(len(rows)):
            if index == pivot_row or not rows[index][column]:
                continue
            scale = rows[index][column]
            rows[index] = [
                value - scale * pivot_value
                for value, pivot_value in zip(
                    rows[index], rows[pivot_row], strict=True
                )
            ]
        pivots.append(column)
        pivot_row += 1
    if len(pivots) != variable_count:
        raise ValueError("selected support columns are dependent")
    for row in rows:
        if all(value == 0 for value in row[:-1]) and row[-1] != 0:
            raise ValueError("selected floating support is not exactly feasible")
    solution = [Q(0)] * variable_count
    for row_index, column in enumerate(pivots):
        solution[column] = rows[row_index][-1]
    return solution


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", type=Path, default=here / "candidate_exact.json"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=here / "integer_row_mixture.json",
    )
    args = parser.parse_args()
    source_bytes = args.source.read_bytes()
    source = json.loads(source_bytes)
    rows = row_types()
    row_array = np.asarray(rows, dtype=np.int16)
    pairs = [(i, j) for i in range(7) for j in range(i, 7)]
    features = np.empty((len(rows), 36), dtype=np.float64)
    features[:, 0] = 1
    features[:, 1:8] = row_array
    for offset, (i, j) in enumerate(pairs, start=8):
        features[:, offset] = (
            row_array[:, i].astype(np.int32)
            * row_array[:, j].astype(np.int32)
        )

    alpha = [Q(value) for value in source["alpha"]]
    moments = pair_moment_matrix(source)
    target_exact = [
        Q(1),
        *alpha,
        *(moments[i][j] for i, j in pairs),
    ]
    result = linprog(
        np.zeros(len(rows)),
        A_eq=csc_matrix(features.T),
        b_eq=np.asarray([float(value) for value in target_exact]),
        bounds=(0, None),
        method="highs",
        options={"presolve": True},
    )
    if not result.success:
        raise RuntimeError("row-moment LP is infeasible: " + result.message)
    active = np.flatnonzero(result.x > 1.0e-9)
    selected = [rows[int(index)] for index in active]
    exact_matrix = [
        [
            Q(1)
            if equation == 0
            else (
                Q(row[equation - 1])
                if equation < 8
                else Q(
                    row[pairs[equation - 8][0]]
                    * row[pairs[equation - 8][1]]
                )
            )
            for row in selected
        ]
        for equation in range(36)
    ]
    weights = solve_rectangular(exact_matrix, target_exact)
    if not all(weight > 0 for weight in weights):
        raise ValueError("exactly reconstructed support is not positive")
    for equation, target in enumerate(target_exact):
        observed = sum(
            exact_matrix[equation][index] * weights[index]
            for index in range(len(weights))
        )
        if observed != target:
            raise ValueError(f"exact moment mismatch at equation {equation}")

    payload = {
        "schema": "kissing5.noncentered_integer_degree_mixture.v1",
        "status": (
            "exact first/second integer row-moment mixture for the named "
            "pair/triple witness; not a global code"
        ),
        "source_certificate": args.source.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "cardinality": 41,
        "grid_numerators_over_four": [-4, -3, -2, -1, 0, 1, 2],
        "row_type_constraints": {
            "degree_sum": 40,
            "antipode_degree_upper_bound": 1,
            "negative_degree_lower_bound": 7,
            "positive_degree_lower_bound": 6,
            "contact_degree_upper_bound": 15,
            "minus_three_quarters_degree_upper_bound": 5,
        },
        "complete_row_type_count": len(rows),
        "floating_maximum_residual": float(
            np.max(abs(features.T @ result.x - np.asarray(
                [float(value) for value in target_exact]
            )))
        ),
        "atoms": [
            {
                "degree_vector": list(row),
                "weight": str(weight),
            }
            for row, weight in zip(selected, weights, strict=True)
        ],
    }
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": "PASS",
                "complete_row_types": len(rows),
                "positive_atoms": len(weights),
                "minimum_weight": str(min(weights)),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
