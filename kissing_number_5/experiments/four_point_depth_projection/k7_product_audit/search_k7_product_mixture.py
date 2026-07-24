#!/usr/bin/env python3
"""Search and exactify a product-valid rank-five K7 mixture.

Discovery uses SciPy/HiGHS only to select an active set.  The returned
weights are reconstructed over ``fractions.Fraction`` and every marginal
and product inequality is then checked exactly before a certificate is
written.

The input catalog need not be complete.  A feasible mixture is nevertheless
an exact positive construction on the explicitly authenticated atoms; an
infeasible result is only a statement about the supplied catalog.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog
from scipy.sparse import csc_matrix


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
DEFAULT_POOL = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "k7"
    / "results"
    / "direct_k7_from_51.csv"
)
sys.path.insert(0, str(ROOT))

from experiments.four_point_depth_projection.k5_product_audit.verify_product_extension_independent import (  # noqa: E402
    capacity_families,
    direction_states,
)


PAIRS = tuple(itertools.combinations(range(7), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}


def edge_color(edges: np.ndarray, first: int, second: int) -> int:
    return int(edges[PAIR_INDEX[tuple(sorted((first, second)))]])


def parse_pool(path: Path) -> tuple[str, np.ndarray, np.ndarray]:
    lines = path.read_text().splitlines()
    assert lines and lines[0].startswith("# ")
    records = np.array(
        [[int(field) for field in line.split(",")] for line in lines[1:]],
        dtype=np.uint8,
    )
    assert records.ndim == 2 and records.shape[1] == 56
    return lines[0], records[:, :21], records[:, 21:]


def product_features(
    all_edges: np.ndarray,
    base_index: int,
    high_index: int,
    capacity: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Return exact compressed coefficients for all 49 depth tables.

    Conditional on a fixed edge, a K7 face samples five of the 39 residual
    global vertices.  Singleton and ordered-distinct-pair retention
    probabilities are 5/39 and 10/741.  Clearing denominators in

        C + I <= M H + r Gamma - r M

    gives the sampled inequality

        741 c + 78 i <= 78 M h + 78 r g - 10 r M.
    """

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
                vertex for vertex in range(7) if vertex not in (first, second)
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
                for vertex, is_gamma in zip(remaining, gamma, strict=True):
                    first_color = edge_color(edges, oriented_first, vertex)
                    second_color = edge_color(edges, oriented_second, vertex)
                    # 78 M h - 741 c - 78 i, with c=h*g-i.
                    coefficient = (
                        78 * capacity
                        - 741 * (gamma_count - int(is_gamma))
                        - 78 * int(is_gamma)
                    )
                    vector[7 * first_color + second_color] += coefficient
        # Sum 78 r g - 10 r M over both orientations of every base edge.
        required_coefficients[column] = (
            156 * gamma_sum - 20 * capacity * edge_sum
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
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    left - factor * right
                    for left, right in zip(
                        augmented[row], augmented[column], strict=True
                    )
                ]
    return [row[-1] for row in augmented]


def qstring(value: Q) -> str:
    return str(value)


def build_equalities(
    triangle_faces: np.ndarray,
    nu: list[Q],
) -> tuple[csc_matrix, np.ndarray]:
    column_count = len(triangle_faces)
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
    target = np.array([1.0] + [float(Q(7) * value / 312) for value in nu])
    return equality, target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", type=Path, default=DEFAULT_POOL)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()
    pool = args.pool.resolve()

    source = json.loads(SOURCE.read_text())
    grid = tuple(Q(value) for value in source["grid"])
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    nu = [Q(value) for value in source["nu"]]
    alpha = [Q(value) for value in source["alpha"]]
    header, edges, triangle_faces = parse_pool(pool)
    column_count = len(edges)
    print(f"pool columns={column_count}", flush=True)

    equality, equality_target = build_equalities(triangle_faces, nu)
    families: list[dict[str, object]] = []
    for base_index, high_index, capacity in capacity_families(grid):
        states, coverage, _feasible = direction_states(
            base_index, grid, triples
        )
        vectors, r_vector = product_features(
            edges, base_index, high_index, capacity
        )
        families.append(
            {
                "base_index": base_index,
                "high_index": high_index,
                "capacity": capacity,
                "states": states,
                "coverage": coverage,
                "vectors": vectors,
                "r_vector": r_vector,
            }
        )
        print(
            f"family q={grid[base_index]} b={grid[high_index]} "
            f"M={capacity}: {len(states)} states",
            flush=True,
        )

    # First report the unconstrained triangle-marginal solution's product
    # violations.  With --audit-only this is the sole numerical operation.
    direct_result = linprog(
        np.zeros(column_count),
        A_eq=equality,
        b_eq=equality_target,
        bounds=(0, None),
        method="highs",
    )
    if not direct_result.success:
        raise RuntimeError(direct_result.message)

    cuts: list[np.ndarray] = []
    cut_keys: set[tuple[int, int]] = set()
    solution = direct_result.x
    for iteration in range(200):
        violations: list[tuple[float, int, int, int]] = []
        for family_index, family in enumerate(families):
            expected_table = solution @ family["vectors"]
            expected_r = float(solution @ family["r_vector"])
            for state_index, (required, table) in enumerate(family["states"]):
                slack = float(
                    expected_table @ np.array(table) + required * expected_r
                )
                if slack < -1e-7:
                    violations.append(
                        (slack, family_index, state_index, required)
                    )
        violations.sort()
        print(
            f"iteration={iteration} cuts={len(cuts)} "
            f"active={np.count_nonzero(solution > 1e-9)} "
            f"violations={len(violations)}"
            + (
                f" worst={violations[0]}"
                if violations
                else ""
            ),
            flush=True,
        )
        if not violations:
            break
        if args.audit_only:
            return
        for _slack, family_index, state_index, required in violations[:30]:
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
        inequality = -csc_matrix(np.vstack(cuts))
        result = linprog(
            np.zeros(column_count),
            A_ub=inequality,
            b_ub=np.zeros(len(cuts)),
            A_eq=equality,
            b_eq=equality_target,
            bounds=(0, None),
            method="highs",
            options={
                "dual_feasibility_tolerance": 1e-9,
                "primal_feasibility_tolerance": 1e-9,
            },
        )
        print(f"  solve success={result.success}: {result.message}", flush=True)
        if not result.success:
            raise RuntimeError(
                "the supplied (possibly incomplete) pool is infeasible for "
                f"{len(cuts)} discovered product cuts: {result.message}"
            )
        solution = result.x
    else:
        raise RuntimeError("cut loop did not converge")

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
        exact_targets.append(Q(7) * nu[face] / 312)

    binding_keys: list[tuple[int, int, int]] = []
    seen: set[bytes] = set()
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
            exact_rows.append(
                [Q(int(coefficient[column])) for column in active]
            )
            exact_targets.append(Q(0))
            binding_keys.append((family_index, state_index, required))
    print(
        f"active={len(active)} candidate_binding={len(binding_keys)}",
        flush=True,
    )

    floating = np.array([[float(value) for value in row] for row in exact_rows])
    rank = np.linalg.matrix_rank(floating)
    if rank < len(active):
        raise RuntimeError(
            f"active solution is not a vertex: rank={rank}, active={len(active)}"
        )
    _q, _r, permutation = qr(floating.T, mode="economic", pivoting=True)
    independent = tuple(int(index) for index in permutation[: len(active)])
    exact_weights = solve_square(
        [exact_rows[index] for index in independent],
        [exact_targets[index] for index in independent],
    )
    if not all(weight > 0 for weight in exact_weights):
        raise RuntimeError("exact reconstruction contains a nonpositive weight")
    assert all(
        sum(
            value * weight
            for value, weight in zip(row, exact_weights, strict=True)
        )
        == target
        for row, target in zip(exact_rows, exact_targets, strict=True)
    )

    zero_keys = []
    minimum_positive = None
    for family_index, family in enumerate(families):
        for state_index, (required, table) in enumerate(family["states"]):
            coefficient = (
                family["vectors"] @ np.array(table, dtype=np.int32)
                + required * family["r_vector"]
            )
            slack = sum(
                Q(int(coefficient[column])) * weight
                for column, weight in zip(active, exact_weights, strict=True)
            )
            assert slack >= 0, (
                family_index,
                state_index,
                required,
                slack,
            )
            if slack == 0:
                zero_keys.append([family_index, state_index, required])
            elif minimum_positive is None or slack < minimum_positive:
                minimum_positive = slack
    assert minimum_positive is not None

    edge_counts = [[0] * 7 for _ in active]
    for atom_index, column in enumerate(active):
        for color in edges[column]:
            edge_counts[atom_index][int(color)] += 1
    exact_edge_marginal = [
        sum(
            Q(counts[color]) * weight
            for counts, weight in zip(
                edge_counts, exact_weights, strict=True
            )
        )
        for color in range(7)
    ]
    assert exact_edge_marginal == [
        Q(21) * value / 40 for value in alpha
    ]

    certificate = {
        "schema": "kissing5.rank5_k7_product_extension.v1",
        "status": (
            "exact positive mixture over an explicit rank-five K7 pool "
            "matching alpha/40, nu/1560, and all 560 currently proved "
            "edge-conditioned depth/common-pair product rows"
        ),
        "scope_warning": (
            "the discovery pool is not a complete enumeration of all "
            "quarter-grid rank-five K7 atoms; this positive local mixture "
            "is not a global 41-point code or an overlapping-face/Lasserre "
            "certificate"
        ),
        "source_certificate": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "pool_file": str(pool.relative_to(ROOT)),
        "pool_sha256": hashlib.sha256(pool.read_bytes()).hexdigest(),
        "pool_header": header,
        "normalization": (
            "weights sum to one; expected K7 edge counts are 21*alpha/40; "
            "expected K7 triangle counts are 7*nu/312; product rows use "
            "singleton retention 5/39 and ordered-distinct-pair retention "
            "10/741, hence 741c+78i <= 78Mh+78rg-10rM"
        ),
        "positive_atom_count": len(active),
        "active_pool_indices": list(active),
        "zero_product_row_keys": zero_keys,
        "minimum_positive_twice_symmetrized_slack": qstring(
            minimum_positive
        ),
        "product_family_summary": [
            {
                "base_inner_product": str(grid[family["base_index"]]),
                "high_threshold": str(grid[family["high_index"]]),
                "capacity": family["capacity"],
                "distinct_direction_states": len(family["states"]),
            }
            for family in families
        ],
        "atoms": [
            {
                "edge_color_indices_"
                "01_02_03_04_05_06_12_13_14_15_16_"
                "23_24_25_26_34_35_36_45_46_56": [
                    int(value) for value in edges[column]
                ],
                "triangle_orbit_indices": [
                    int(value) for value in triangle_faces[column]
                ],
                "weight": qstring(weight),
            }
            for column, weight in zip(active, exact_weights, strict=True)
        ],
    }
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
        print(args.output)
        print(hashlib.sha256(args.output.read_bytes()).hexdigest())
    else:
        print(encoded)


if __name__ == "__main__":
    main()
