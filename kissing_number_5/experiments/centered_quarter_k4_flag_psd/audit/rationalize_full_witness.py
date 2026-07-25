#!/usr/bin/env python3
"""Convert the numerical full-centering witness to exact rational marginals.

The affine system is integral after harmless row scalings.  We freeze the
nonpivot variables on a 10^-16 grid and solve a well-conditioned 171 by 171
integer pivot system exactly with PARI/GP.  This script only certifies the
linear identities and positivity; PSD is checked separately.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np
from scipy.linalg import qr

from experiments.centered_quarter_k4_flag_psd.audit.search_full_centering import (
    coefficients,
)


def affine_system(data: dict) -> tuple[np.ndarray, np.ndarray]:
    alpha_count = 7
    triple_count = len(data["triples"])
    orbit_count = len(data["orbits"])
    variable_count = alpha_count + triple_count + orbit_count
    rows: list[np.ndarray] = []
    rhs: list[int] = []

    def add(row: np.ndarray, value: int = 0) -> None:
        rows.append(row)
        rhs.append(value)

    grid4 = np.array(
        [round(4 * float(value)) for value in data["grid"]],
        dtype=np.int64,
    )

    row = np.zeros(variable_count, dtype=np.int64)
    row[:alpha_count] = 1
    add(row, 40)

    row = np.zeros(variable_count, dtype=np.int64)
    row[:alpha_count] = grid4
    add(row, -4)

    # Three times the K3 -> K2 marginal equation.
    for color in range(alpha_count):
        row = np.zeros(variable_count, dtype=np.int64)
        row[color] = -117
        for column, triple in enumerate(data["triples"]):
            row[alpha_count + column] = triple.count(color)
        add(row)

    # 390 times the K4 -> K3 face equation.
    face_incidence = np.rint(data["face_incidence"]).astype(np.int64)
    k4_offset = alpha_count + triple_count
    for triple in range(triple_count):
        row = np.zeros(variable_count, dtype=np.int64)
        row[alpha_count + triple] = -1
        row[k4_offset:] = 390 * face_incidence[triple]
        add(row)

    # 24 times the first-endpoint K2 -> K3 centering identity.  Exchange
    # symmetry makes the second-endpoint row identical, while the count row
    # is already the pair marginal above.
    edge_first6 = np.rint(6 * data["edge_first"]).astype(np.int64)
    for color in range(alpha_count):
        row = np.zeros(variable_count, dtype=np.int64)
        row[color] = 24 + 6 * grid4[color]
        for category, (first, _) in enumerate(data["categories"]):
            row[
                alpha_count : alpha_count + triple_count
            ] += edge_first6[color, category] * grid4[first]
        add(row)

    # These rows already have their denominator 24 cleared.
    for centered in data["centered_matrix"].astype(np.int64):
        row = np.zeros(variable_count, dtype=np.int64)
        row[alpha_count:] = centered
        add(row)

    return np.array(rows, dtype=np.int64), np.array(rhs, dtype=np.int64)


def pari_solve(matrix: np.ndarray, rhs: np.ndarray) -> list[Q]:
    rows = ";".join(
        ",".join(str(int(value)) for value in row) for row in matrix
    )
    vector = ",".join(str(int(value)) for value in rhs)
    program = (
        f"A=[{rows}];b=[{vector}]~;"
        "x=matsolve(A,b);"
        "for(i=1,#x,print(x[i]));quit\n"
    )
    process = subprocess.run(
        ["gp", "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
    )
    values = [
        Q(line.strip())
        for line in process.stdout.splitlines()
        if line.strip()
    ]
    if len(values) != matrix.shape[0]:
        raise RuntimeError(
            f"PARI returned {len(values)} values for {matrix.shape[0]} rows"
        )
    return values


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    audit = Path(__file__).resolve().parent
    source_path = (
        root / "certificates/centered_quarter_bv_pseudodistribution.json"
    )
    numerical_path = audit / "results/full_clarabel.json"
    source = json.loads(source_path.read_text())
    numerical = json.loads(numerical_path.read_text())
    data = coefficients(source)
    matrix, rhs = affine_system(data)

    # Select independent rows, then a numerically well-conditioned set of
    # pivot columns.  Exact substitution below verifies that this numerical
    # selection did in fact have full rank.
    _, row_factor, row_permutation = qr(
        matrix.T.astype(float), pivoting=True, mode="economic"
    )
    diagonal = np.abs(np.diag(row_factor))
    rank = int(np.sum(diagonal > diagonal[0] * 1e-10))
    independent_rows = row_permutation[:rank]
    independent = matrix[independent_rows]
    independent_rhs = rhs[independent_rows]
    _, column_factor, column_permutation = qr(
        independent.astype(float), pivoting=True, mode="economic"
    )
    if abs(column_factor[rank - 1, rank - 1]) < 1e-6:
        raise RuntimeError("selected pivot matrix is numerically singular")
    pivot_columns = np.array(column_permutation[:rank])
    free_columns = np.array(column_permutation[rank:])

    alpha_count = 7
    triple_count = len(data["triples"])
    approximate = np.array(
        numerical["alpha"] + numerical["nu"] + numerical["k4"],
        dtype=float,
    )
    denominator = 10**16
    free_numerators = np.rint(
        denominator * approximate[free_columns]
    ).astype(object)
    pivot_matrix = independent[:, pivot_columns]
    free_matrix = independent[:, free_columns]
    scaled_rhs = np.array(
        [
            int(independent_rhs[row]) * denominator
            - sum(
                int(coefficient) * int(value)
                for coefficient, value in zip(
                    free_matrix[row], free_numerators
                )
            )
            for row in range(rank)
        ],
        dtype=object,
    )
    pivot_scaled = pari_solve(pivot_matrix, scaled_rhs)

    exact = [Q(0) for _ in range(matrix.shape[1])]
    for column, numerator in zip(free_columns, free_numerators):
        exact[int(column)] = Q(int(numerator), denominator)
    for column, scaled in zip(pivot_columns, pivot_scaled):
        exact[int(column)] = scaled / denominator

    # Do not trust the rank selection or PARI output: verify every original
    # (including redundant) affine equation directly over Fraction.
    for row, target in zip(matrix, rhs):
        value = sum(
            (Q(int(coefficient)) * variable)
            for coefficient, variable in zip(row, exact)
            if coefficient
        )
        assert value == int(target)
    assert min(exact) > 0

    alpha = exact[:alpha_count]
    nu = exact[alpha_count : alpha_count + triple_count]
    k4 = exact[alpha_count + triple_count :]
    result = {
        "schema": "kissing5.centered_quarter_k4_full_exact_linear.v1",
        "status": (
            "exact positive K2/K3/K4 marginals satisfying all affine "
            "pointwise-centering identities; PSD checked separately"
        ),
        "source_numerical_result": str(
            numerical_path.relative_to(root)
        ),
        "source_numerical_sha256": hashlib.sha256(
            numerical_path.read_bytes()
        ).hexdigest(),
        "rounding_denominator": denominator,
        "affine_row_count": len(matrix),
        "affine_rank": rank,
        "pivot_count": len(pivot_columns),
        "minimum_alpha_float": float(min(alpha)),
        "minimum_nu_float": float(min(nu)),
        "minimum_k4_float": float(min(k4)),
        "alpha": [str(value) for value in alpha],
        "nu": [str(value) for value in nu],
        "k4": [str(value) for value in k4],
    }
    output = audit / "results/full_exact_linear_witness.json"
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output.write_text(encoded)
    print(
        json.dumps(
            {
                key: value
                for key, value in result.items()
                if key not in ("alpha", "nu", "k4")
            },
            indent=2,
            sort_keys=True,
        )
    )
    print("sha256=" + hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
