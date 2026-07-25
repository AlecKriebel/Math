#!/usr/bin/env python3
"""Numerical discovery search for factorial-moment K7 repairs.

This program is deliberately separate from the exact verifiers.  It uses
SciPy/HiGHS to test an incomplete 1,782-column pool, then appends the
explicit rank-five atom from the proof note.  Solver status is discovery
evidence only.
"""

from __future__ import annotations

from fractions import Fraction as Q
import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import csc_matrix, lil_matrix


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from experiments.four_point_depth_projection.k5_product_audit.verify_product_extension_independent import (  # noqa: E402
    capacity_families,
    direction_states,
)


SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
POOL = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "k7"
    / "results"
    / "direct_k7_from_51.csv"
)
PAIRS = tuple(itertools.combinations(range(7), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}


def edge_color(edges, first, second):
    return int(edges[PAIR_INDEX[tuple(sorted((first, second)))]])


def parse_pool():
    lines = POOL.read_text().splitlines()
    records = np.array(
        [[int(field) for field in line.split(",")] for line in lines[1:]],
        dtype=np.uint8,
    )
    assert records.shape == (1782, 56)
    return records[:, :21], records[:, 21:]


def build_equalities(faces, nu):
    row = [0] * len(faces)
    column = list(range(len(faces)))
    value = [1.0] * len(faces)
    for atom, atom_faces in enumerate(faces):
        for face in atom_faces:
            row.append(1 + int(face))
            column.append(atom)
            value.append(1.0)
    matrix = csc_matrix(
        (value, (row, column)), shape=(52, len(faces))
    )
    target = np.array([1.0] + [float(Q(7) * item / 312) for item in nu])
    return matrix, target


def synthetic_atom(triples):
    edges = np.full(21, 4, dtype=np.uint8)

    def set_color(first, second, color):
        edges[PAIR_INDEX[tuple(sorted((first, second)))]] = color

    for vertex in range(2, 6):
        set_color(0, vertex, 6)
        set_color(1, vertex, 6)
    for first in (2, 3):
        for second in (4, 5):
            set_color(first, second, 6)
    triple_index = {triple: index for index, triple in enumerate(triples)}
    faces = []
    for first, second, third in itertools.combinations(range(7), 3):
        faces.append(
            triple_index[
                tuple(
                    sorted(
                        (
                            edge_color(edges, first, second),
                            edge_color(edges, first, third),
                            edge_color(edges, second, third),
                        )
                    )
                )
            ]
        )
    return edges, np.array(sorted(faces), dtype=np.uint8)


def generalized_binomial(value, degree):
    answer = Q(1)
    for offset in range(degree):
        answer *= Q(value - offset, offset + 1)
    return answer


def differences(values):
    result = []
    while values:
        result.append(values[0])
        values = [
            values[index + 1] - values[index]
            for index in range(len(values) - 1)
        ]
    return result


def cap_estimator_values(capacity, left, right):
    coefficients = differences(
        [
            generalized_binomial(value, left)
            * generalized_binomial(capacity - value, right)
            for value in range(left + right + 1)
        ]
    )
    values = []
    for observed in range(6):
        values.append(
            sum(
                coefficient
                * Q(math.comb(39, degree), math.comb(5, degree))
                * math.comb(observed, degree)
                for degree, coefficient in enumerate(coefficients)
            )
        )
    denominator = math.lcm(*(value.denominator for value in values))
    return np.array(
        [int(value * denominator) for value in values], dtype=np.int64
    )


def cap_rows(edges, grid, triples):
    del grid, triples
    rows = []
    seen = set()
    for base, high, capacity in capacity_families(GRID):
        histogram = np.zeros((len(edges), 6), dtype=np.int16)
        for atom, atom_edges in enumerate(edges):
            for position, (first, second) in enumerate(PAIRS):
                if int(atom_edges[position]) != base:
                    continue
                common = sum(
                    edge_color(atom_edges, first, vertex) >= high
                    and edge_color(atom_edges, second, vertex) >= high
                    for vertex in range(7)
                    if vertex not in (first, second)
                )
                histogram[atom, common] += 1
        for total in range(1, 6):
            for left in range(total + 1):
                right = total - left
                row = histogram @ cap_estimator_values(
                    capacity, left, right
                )
                divisor = 0
                for value in row:
                    divisor = math.gcd(divisor, abs(int(value)))
                if divisor > 1:
                    row //= divisor
                key = row.tobytes()
                if np.any(row) and key not in seen:
                    seen.add(key)
                    rows.append(row)
    return np.vstack(rows)


def product_feature_blocks(edges, base, high, capacity):
    vectors = np.zeros((len(edges), 49), dtype=np.int32)
    required_vector = np.zeros(len(edges), dtype=np.int32)
    for atom, atom_edges in enumerate(edges):
        common_sum = 0
        edge_sum = 0
        for position, (first, second) in enumerate(PAIRS):
            if int(atom_edges[position]) != base:
                continue
            edge_sum += 1
            remaining = [
                vertex
                for vertex in range(7)
                if vertex not in (first, second)
            ]
            common_flags = [
                edge_color(atom_edges, first, vertex) >= high
                and edge_color(atom_edges, second, vertex) >= high
                for vertex in remaining
            ]
            common = sum(common_flags)
            common_sum += common
            for oriented_first, oriented_second in (
                (first, second),
                (second, first),
            ):
                for vertex, is_common in zip(remaining, common_flags):
                    first_color = edge_color(
                        atom_edges, oriented_first, vertex
                    )
                    second_color = edge_color(
                        atom_edges, oriented_second, vertex
                    )
                    vectors[atom, 7 * first_color + second_color] += (
                        78 * capacity
                        - 741 * (common - int(is_common))
                        - 78 * int(is_common)
                    )
        required_vector[atom] = (
            156 * common_sum - 20 * capacity * edge_sum
        )
    return vectors, required_vector


def product_rows(edges, grid, triples):
    rows = []
    for base, high, capacity in capacity_families(grid):
        states, _coverage, _feasible = direction_states(
            base, grid, triples
        )
        vectors, required_vector = product_feature_blocks(
            edges, base, high, capacity
        )
        for required, table in states:
            rows.append(
                vectors @ np.array(table, dtype=np.int32)
                + required * required_vector
            )
    assert len(rows) == 560
    return np.vstack(rows)


def solve_nonnegative(equalities, target, rows=None):
    return linprog(
        np.zeros(equalities.shape[1]),
        A_ub=None if rows is None else -csc_matrix(rows),
        b_ub=None if rows is None else np.zeros(len(rows)),
        A_eq=equalities,
        b_eq=target,
        bounds=(0, None),
        method="highs",
        options={
            "primal_feasibility_tolerance": 1e-9,
            "dual_feasibility_tolerance": 1e-9,
        },
    )


def joint_family_zero_system(edges, equalities, target, grid):
    """Add a degree-five joint representing measure for family zero."""

    base, high, capacity = capacity_families(grid)[0]
    keys = [
        (left, total - left)
        for total in range(6)
        for left in range(total + 1)
    ]
    local = np.zeros((len(keys), len(edges)))
    for atom, atom_edges in enumerate(edges):
        for position, (first, second) in enumerate(PAIRS):
            if int(atom_edges[position]) != base:
                continue
            remaining = [
                vertex
                for vertex in range(7)
                if vertex not in (first, second)
            ]
            depth = sum(
                grid[edge_color(atom_edges, first, vertex)]
                + grid[edge_color(atom_edges, second, vertex)]
                < 0
                for vertex in remaining
            )
            common = sum(
                edge_color(atom_edges, first, vertex) >= high
                and edge_color(atom_edges, second, vertex) >= high
                for vertex in remaining
            )
            for row, (left, right) in enumerate(keys):
                local[row, atom] += (
                    math.comb(depth, left) * math.comb(common, right)
                )
    domain = [
        (depth, common)
        for common in range(capacity + 1)
        for depth in range(7, 40 - common)
    ]
    variable_count = len(edges) + len(domain)
    matrix = lil_matrix((52 + len(keys), variable_count))
    rhs = np.zeros(52 + len(keys))
    matrix[:52, : len(edges)] = equalities
    rhs[:52] = target
    for row, (left, right) in enumerate(keys, start=52):
        degree = left + right
        ratio = (
            1.0
            if degree == 0
            else math.comb(5, degree) / math.comb(39, degree)
        )
        matrix[row, : len(edges)] = -local[row - 52]
        matrix[row, len(edges) :] = [
            ratio
            * math.comb(depth, left)
            * math.comb(common, right)
            for depth, common in domain
        ]
    return csc_matrix(matrix), rhs


source = json.loads(SOURCE.read_text())
GRID = tuple(Q(value) for value in source["grid"])


def main():
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    nu = tuple(Q(value) for value in source["nu"])
    original_edges, original_faces = parse_pool()
    original_equalities, target = build_equalities(original_faces, nu)
    original_cap = cap_rows(original_edges, GRID, triples)
    original = solve_nonnegative(
        original_equalities, target, original_cap
    )

    new_edges, new_faces = synthetic_atom(triples)
    augmented_edges = np.vstack((original_edges, new_edges))
    augmented_faces = np.vstack((original_faces, new_faces))
    augmented_equalities, target = build_equalities(augmented_faces, nu)
    augmented_cap = cap_rows(augmented_edges, GRID, triples)
    augmented_product = product_rows(augmented_edges, GRID, triples)
    augmented_rows = np.vstack((augmented_cap, augmented_product))
    repaired = solve_nonnegative(
        augmented_equalities, target, augmented_rows
    )

    joint_matrix, joint_target = joint_family_zero_system(
        augmented_edges, augmented_equalities, target, GRID
    )
    joint = solve_nonnegative(joint_matrix, joint_target)

    report = {
        "status": "NUMERICAL EVIDENCE ONLY",
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "solver": "SciPy linprog / HiGHS",
        "original_pool": {
            "columns": len(original_edges),
            "distinct_cap_rows": len(original_cap),
            "cap_factorial_feasible": bool(original.success),
            "solver_message": original.message,
        },
        "one_atom_repair": {
            "columns": len(augmented_edges),
            "distinct_cap_rows": len(augmented_cap),
            "product_rows": len(augmented_product),
            "feasible": bool(repaired.success),
            "active_weights": (
                int(np.count_nonzero(repaired.x > 1e-9))
                if repaired.success
                else None
            ),
            "new_atom_weight": (
                float(repaired.x[-1]) if repaired.success else None
            ),
            "minimum_row_slack": (
                float(np.min(augmented_rows @ repaired.x))
                if repaired.success
                else None
            ),
            "solver_message": repaired.message,
        },
        "joint_family_zero": {
            "family": "q=-3/4, b=1/4, M=6",
            "moment_degree": 5,
            "feasible": bool(joint.success),
            "solver_message": joint.message,
        },
        "scope": (
            "incomplete finite K7 discovery pool; solver status is not "
            "a continuous nonexistence proof"
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
