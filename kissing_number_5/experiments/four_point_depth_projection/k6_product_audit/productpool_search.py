#!/usr/bin/env python3
"""Discovery/exactification search for a product-valid K6 mixture.

This uses SciPy only to find an active set.  The selected weights are then
reconstructed and all equalities and inequalities checked with Fraction.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog
from scipy.sparse import csc_matrix, vstack


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
POOL = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "results"
    / "direct_k6_5000.csv"
)
sys.path.insert(0, str(ROOT))

from experiments.four_point_depth_projection.k5_product_audit.verify_alternative_extension import (  # noqa: E402
    capacity_rows,
    direction_states,
)


PAIRS = tuple((i, j) for i in range(6) for j in range(i + 1, 6))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}


def edge_color(edges: np.ndarray, first: int, second: int) -> int:
    return int(edges[PAIR_INDEX[tuple(sorted((first, second)))]])


def parse_pool() -> tuple[str, np.ndarray, np.ndarray]:
    lines = POOL.read_text().splitlines()
    header = lines[0]
    records = np.array(
        [[int(field) for field in line.split(",")] for line in lines[1:]],
        dtype=np.uint8,
    )
    assert records.shape == (137296, 35)
    return header, records[:, :15], records[:, 15:]


def product_features(
    all_edges: np.ndarray,
    base_index: int,
    high_index: int,
    capacity: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Compressed coefficients for every direction-membership table."""

    count = len(all_edges)
    vectors = np.zeros((count, 49), dtype=np.int32)
    required_coefficients = np.zeros(count, dtype=np.int32)
    for column, edges in enumerate(all_edges):
        gamma_sum = 0
        edge_sum = 0
        vector = vectors[column]
        for position, (first, second) in enumerate(PAIRS):
            if int(edges[position]) != base_index:
                continue
            edge_sum += 1
            remaining = [
                vertex for vertex in range(6) if vertex not in (first, second)
            ]
            gamma = [
                edge_color(edges, first, vertex) >= high_index
                and edge_color(edges, second, vertex) >= high_index
                for vertex in remaining
            ]
            gamma_count = sum(gamma)
            gamma_sum += gamma_count
            for oriented_first, oriented_second in (
                (first, second),
                (second, first),
            ):
                for vertex, is_gamma in zip(remaining, gamma):
                    first_color = edge_color(edges, oriented_first, vertex)
                    second_color = edge_color(edges, oriented_second, vertex)
                    # 39 M H2 - 494 C2 - 39 I2.
                    coefficient = (
                        39 * capacity
                        - 494 * (gamma_count - int(is_gamma))
                        - 39 * int(is_gamma)
                    )
                    vector[7 * first_color + second_color] += coefficient
        # 78 r G - 8 r M E.
        required_coefficients[column] = (
            78 * gamma_sum - 8 * capacity * edge_sum
        )
    return vectors, required_coefficients


def solve_square(matrix: list[list[Q]], target: list[Q]) -> list[Q]:
    size = len(matrix)
    assert size and all(len(row) == size for row in matrix)
    augmented = [row[:] + [value] for row, value in zip(matrix, target)]
    for column in range(size):
        pivot = next(
            row for row in range(column, size) if augmented[row][column] != 0
        )
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    left - factor * right
                    for left, right in zip(augmented[row], augmented[column])
                ]
    return [row[-1] for row in augmented]


def qstring(value: Q) -> str:
    return str(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    source = json.loads(SOURCE.read_text())
    grid = [Q(value) for value in source["grid"]]
    triples = [tuple(item) for item in source["triple_orbits"]]
    nu = [Q(value) for value in source["nu"]]
    header, edges, triangle_faces = parse_pool()
    column_count = len(edges)
    print(f"pool columns={column_count}", flush=True)

    equality_row = [0] * column_count
    equality_column = list(range(column_count))
    equality_value = [1.0] * column_count
    for column, faces in enumerate(triangle_faces):
        for face in faces:
            equality_row.append(1 + int(face))
            equality_column.append(column)
            equality_value.append(1.0)
    equality = csc_matrix(
        (equality_value, (equality_row, equality_column)),
        shape=(52, column_count),
    )
    equality_target = np.array(
        [1.0] + [float(value / 78) for value in nu]
    )

    families = []
    for base_index, high, capacity in capacity_rows(grid):
        states = direction_states(base_index, grid, triples, nu)
        vectors, r_vector = product_features(
            edges, base_index, grid.index(high), capacity
        )
        families.append(
            {
                "base_index": base_index,
                "high": high,
                "capacity": capacity,
                "states": states,
                "vectors": vectors,
                "r_vector": r_vector,
            }
        )
        print(
            f"family q={grid[base_index]} b={high} M={capacity}: "
            f"{len(states)} states",
            flush=True,
        )

    cuts: list[np.ndarray] = []
    cut_keys: set[tuple[int, int]] = set()
    solution = None
    for iteration in range(100):
        inequality = None if not cuts else -csc_matrix(np.vstack(cuts))
        result = linprog(
            np.zeros(column_count),
            A_ub=inequality,
            b_ub=None if not cuts else np.zeros(len(cuts)),
            A_eq=equality,
            b_eq=equality_target,
            bounds=(0, None),
            method="highs",
            options={"dual_feasibility_tolerance": 1e-9},
        )
        print(
            f"iteration={iteration} success={result.success} cuts={len(cuts)} "
            f"active={0 if not result.success else np.count_nonzero(result.x > 1e-9)}",
            flush=True,
        )
        if not result.success:
            raise RuntimeError(result.message)
        solution = result.x

        violations = []
        for family_index, family in enumerate(families):
            expected_table = solution @ family["vectors"]
            expected_r = float(solution @ family["r_vector"])
            for state_index, (required, table) in enumerate(family["states"]):
                slack = float(expected_table @ np.array(table) + required * expected_r)
                if slack < -1e-7:
                    violations.append(
                        (slack, family_index, state_index, required)
                    )
        if not violations:
            print("all numerical rows pass", flush=True)
            break
        violations.sort()
        print("worst", violations[:5], flush=True)
        for _slack, family_index, state_index, required in violations[:20]:
            key = (family_index, state_index)
            if key in cut_keys:
                continue
            family = families[family_index]
            _stored_required, table = family["states"][state_index]
            coefficient = (
                family["vectors"] @ np.array(table, dtype=np.int32)
                + required * family["r_vector"]
            ).astype(np.int64)
            cuts.append(coefficient)
            cut_keys.add(key)
    else:
        raise RuntimeError("cut loop did not converge")
    assert solution is not None

    active = tuple(int(index) for index in np.flatnonzero(solution > 1e-9))
    exact_rows: list[list[Q]] = [[Q(1) for _ in active]]
    exact_targets = [Q(1)]
    for face in range(51):
        exact_rows.append(
            [
                Q(sum(int(value) == face for value in triangle_faces[column]))
                for column in active
            ]
        )
        exact_targets.append(nu[face] / 78)

    binding_rows = []
    binding_keys = []
    seen = set()
    for family_index, family in enumerate(families):
        for state_index, (required, table) in enumerate(family["states"]):
            coefficient = (
                family["vectors"] @ np.array(table, dtype=np.int32)
                + required * family["r_vector"]
            ).astype(np.int64)
            slack = float(coefficient @ solution)
            if abs(slack) > 1e-6:
                continue
            key = coefficient.tobytes()
            if key in seen:
                continue
            seen.add(key)
            binding_rows.append(coefficient)
            binding_keys.append((family_index, state_index, required))
            exact_rows.append([Q(int(coefficient[column])) for column in active])
            exact_targets.append(Q(0))
    print(f"active={len(active)} binding={len(binding_rows)}", flush=True)

    floating = np.array([[float(value) for value in row] for row in exact_rows])
    _q, _r, permutation = qr(floating.T, mode="economic", pivoting=True)
    independent = tuple(int(index) for index in permutation[: len(active)])
    assert np.linalg.matrix_rank(floating[list(independent)]) == len(active)
    exact_weights = solve_square(
        [exact_rows[index] for index in independent],
        [exact_targets[index] for index in independent],
    )
    assert all(weight > 0 for weight in exact_weights)
    assert all(
        sum(value * weight for value, weight in zip(row, exact_weights)) == target
        for row, target in zip(exact_rows, exact_targets)
    )

    minimum = None
    zeros = []
    for family_index, family in enumerate(families):
        for state_index, (required, table) in enumerate(family["states"]):
            coefficient = (
                family["vectors"] @ np.array(table, dtype=np.int32)
                + required * family["r_vector"]
            )
            slack = sum(
                Q(int(coefficient[column])) * weight
                for column, weight in zip(active, exact_weights)
            )
            assert slack >= 0
            minimum = slack if minimum is None or slack < minimum else minimum
            if slack == 0:
                zeros.append([family_index, state_index, required])
    assert minimum == 0

    certificate = {
        "schema": "kissing5.rank5_k6_product_extension.v1",
        "status": (
            "exact positive mixture over the available rank-five K6 pool "
            "matching the centered quarter-grid triangle marginal and all "
            "560 depth/common product rows"
        ),
        "scope_warning": (
            "the discovery pool comes from 5000 sampled positive-definite K5 "
            "bases and is not a complete enumeration of all quarter-grid K6 atoms"
        ),
        "source_certificate": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "pool_file": str(POOL.relative_to(ROOT)),
        "pool_sha256": hashlib.sha256(POOL.read_bytes()).hexdigest(),
        "pool_header": header,
        "normalization": (
            "weights sum to one; expected K6 triangle counts are nu/78; "
            "product rows use singleton retention 4/39 and ordered-distinct-"
            "pair retention 2/247"
        ),
        "positive_atom_count": len(active),
        "active_pool_indices": list(active),
        "zero_product_row_keys": zeros,
        "product_family_summary": [
            {
                "base_inner_product": str(grid[family["base_index"]]),
                "high_threshold": str(family["high"]),
                "capacity": family["capacity"],
                "distinct_direction_states": len(family["states"]),
            }
            for family in families
        ],
        "atoms": [
            {
                "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45": [
                    int(value) for value in edges[column]
                ],
                "triangle_orbit_indices": [
                    int(value) for value in triangle_faces[column]
                ],
                "weight": qstring(weight),
            }
            for column, weight in zip(active, exact_weights)
        ],
    }
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
        print(args.output)
        print(hashlib.sha256(args.output.read_bytes()).hexdigest())
    else:
        print(encoded)


if __name__ == "__main__":
    main()
