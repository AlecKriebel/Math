#!/usr/bin/env python3
"""Rationalize the centered quarter-grid pair/triple pseudodistribution.

Discovery utility.  It uses SciPy only to select a well-conditioned pivot
set; every correction and every stored coefficient is then computed with
``fractions.Fraction``.  The separate standard-library verifier does not
trust this program.
"""

from __future__ import annotations

from fractions import Fraction as Q
import argparse
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.linalg import qr


N = 41
ROUNDING_DENOMINATOR = 10**12


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def determinant(u: Q, v: Q, t: Q) -> Q:
    return 1 + 2 * u * v * t - u * u - v * v - t * t


def feasible_orbits(nodes: tuple[Q, ...]) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        triple
        for triple in itertools.combinations_with_replacement(
            range(len(nodes)), 3
        )
        if determinant(*(nodes[index] for index in triple)) >= 0
    )


def solve_square(matrix: list[list[Q]], rhs: list[Q]) -> list[Q]:
    size = len(rhs)
    work = [
        [Q(entry) for entry in row] + [Q(value)]
        for row, value in zip(matrix, rhs)
    ]
    for column in range(size):
        pivot = next(
            row
            for row in range(column, size)
            if work[row][column] != 0
        )
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [entry / scale for entry in work[column]]
        for row in range(size):
            if row == column:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    entry - scale * pivot_entry
                    for entry, pivot_entry in zip(
                        work[row], work[column]
                    )
                ]
    return [work[index][-1] for index in range(size)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    default_source_path = (
        root
        / "experiments"
        / "continuous_rank_bv_search"
        / "results"
        / "centered_quarter_local_d16.json"
    )
    default_output_path = (
        root
        / "certificates"
        / "centered_quarter_bv_pseudodistribution.json"
    )
    source_path = (args.source or default_source_path).resolve()
    output_path = (args.output or default_output_path).resolve()
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    nodes = tuple(Q(value) for value in source["grid"])
    orbits = feasible_orbits(nodes)
    assert tuple(map(tuple, source["triple_orbits"])) == orbits

    variable_count = len(nodes) + len(orbits)
    rows: list[list[Q]] = []
    right_sides: list[Q] = []

    row = [Q(0)] * variable_count
    for index in range(len(nodes)):
        row[index] = 1
    rows.append(row)
    right_sides.append(Q(N - 1))

    row = [Q(0)] * variable_count
    for index, node in enumerate(nodes):
        row[index] = node
    rows.append(row)
    right_sides.append(Q(-1))

    for node_index in range(len(nodes)):
        row = [Q(0)] * variable_count
        row[node_index] = -(N - 2)
        for orbit_index, orbit in enumerate(orbits):
            row[len(nodes) + orbit_index] = Q(
                orbit.count(node_index), 3
            )
        rows.append(row)
        right_sides.append(Q(0))

    # Exact centered-design kernels.  In W_0 the full radial vector
    # f(u)=u (including f(1)=1 at the diagonal atom) must vanish.  In W_1
    # the constant radial vector on the six active nodes must vanish.
    for node_index, node in enumerate(nodes):
        row = [Q(0)] * variable_count
        row[node_index] = node + 1
        for orbit_index, orbit in enumerate(orbits):
            ordered = sorted(set(itertools.permutations(orbit)))
            coefficient = Q(1, len(ordered))
            for first, second, _third in ordered:
                if first == node_index:
                    row[len(nodes) + orbit_index] += (
                        coefficient * nodes[second]
                    )
        rows.append(row)
        right_sides.append(Q(0))

    active_indices = tuple(range(1, len(nodes)))
    for node_index in active_indices:
        node = nodes[node_index]
        row = [Q(0)] * variable_count
        row[node_index] = 1 - node * node
        for orbit_index, orbit in enumerate(orbits):
            ordered = sorted(set(itertools.permutations(orbit)))
            coefficient = Q(1, len(ordered))
            for first, second, third in ordered:
                if first == node_index and second in active_indices:
                    row[len(nodes) + orbit_index] += coefficient * (
                        nodes[third] - nodes[first] * nodes[second]
                    )
        rows.append(row)
        right_sides.append(Q(0))

    # Remove dependent equations before choosing correction pivots, while
    # retaining the full list for the exact post-correction audit.
    all_rows = rows
    all_right_sides = right_sides
    independent_rows: list[list[Q]] = []
    independent_right_sides: list[Q] = []
    current_rank = 0
    for row, target in zip(rows, right_sides):
        candidate = independent_rows + [row]
        floating_candidate = np.array(
            [[float(value) for value in item] for item in candidate]
        )
        candidate_rank = int(np.linalg.matrix_rank(floating_candidate))
        if candidate_rank > current_rank:
            independent_rows.append(row)
            independent_right_sides.append(target)
            current_rank = candidate_rank
    rows = independent_rows
    right_sides = independent_right_sides

    floating_matrix = np.array(
        [[float(value) for value in row] for row in rows]
    )
    _q, _r, permutation = qr(
        floating_matrix, mode="economic", pivoting=True
    )
    pivot_indices = tuple(int(index) for index in permutation[: len(rows)])
    assert np.linalg.matrix_rank(
        floating_matrix[:, list(pivot_indices)]
    ) == len(rows)

    floating_values = tuple(source["alpha"]) + tuple(source["nu"])
    values = [
        Q(round(float(value) * ROUNDING_DENOMINATOR), ROUNDING_DENOMINATOR)
        for value in floating_values
    ]
    residual = [
        target
        - sum(coefficient * value for coefficient, value in zip(row, values))
        for row, target in zip(rows, right_sides)
    ]
    pivot_matrix = [
        [row[index] for index in pivot_indices] for row in rows
    ]
    correction = solve_square(pivot_matrix, residual)
    for index, delta in zip(pivot_indices, correction):
        values[index] += delta

    assert all(
        sum(coefficient * value for coefficient, value in zip(row, values))
        == target
        for row, target in zip(all_rows, all_right_sides)
    )
    assert all(value > 0 for value in values)
    alpha = values[: len(nodes)]
    nu = values[len(nodes) :]
    assert sum(nu) == (N - 1) * (N - 2)

    certificate = {
        "schema": "kissing5.centered_quarter_bv_pseudodistribution.v1",
        "status": (
            "exact centered pair/triple relaxation witness; not a code"
        ),
        "source_numerical_result": str(source_path.relative_to(root)),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "dimension": 5,
        "cardinality": N,
        "maximum_inner_product": "1/2",
        "grid": [qstr(value) for value in nodes],
        "triple_orbits": [list(orbit) for orbit in orbits],
        "alpha": [qstr(value) for value in alpha],
        "nu": [qstr(value) for value in nu],
        "rounding_denominator": ROUNDING_DENOMINATOR,
        "pivot_variable_indices": list(pivot_indices),
        "exact_constraints": [
            "sum(alpha)=40",
            "1+sum(alpha_t*t)=0",
            "marginal_i=39*alpha_i for every node",
            "sum(nu)=1560",
            "the centered W_0 radial kernel is exact",
            "the centered W_1 constant-radial kernel is exact",
        ],
    }
    output_path.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    )
    print(output_path)
    print(hashlib.sha256(output_path.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
