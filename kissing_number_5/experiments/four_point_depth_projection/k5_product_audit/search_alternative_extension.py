#!/usr/bin/env python3
"""Discovery LP for K5 extensions satisfying all depth/capacity products.

This is discovery code and uses NumPy/SciPy.  Any resulting exact artifact
must be reconstructed and checked by a separate standard-library verifier.
"""

from __future__ import annotations

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
sys.path.insert(0, str(ROOT / "experiments" / "centered_atomic_bv_barrier"))
sys.path.insert(
    0,
    str(
        ROOT
        / "experiments"
        / "four_point_depth_projection"
        / "centered_quarter_pair_depth"
    ),
)

from extend_k5 import parse_enumeration  # noqa: E402
from rationalize import qstr, solve_square  # noqa: E402
from verify import (  # noqa: E402
    critical_roots,
    direction_qualifies,
    event_weights,
    open_cell_samples,
    rational_qualifies,
    root_qualifies,
)


EDGE_POSITIONS = (
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4),
)
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGE_POSITIONS)}


def edge_color(edges: tuple[int, ...], first: int, second: int) -> int:
    if first > second:
        first, second = second, first
    return edges[EDGE_INDEX[first, second]]


def capacity_rows(grid: list[Q]) -> tuple[tuple[int, Q, int], ...]:
    rows = []
    for base_index, base in enumerate(grid):
        for high in (Q(1, 4), Q(1, 2)):
            capacity = None
            if base == -1:
                capacity = 0
            elif base <= 0:
                parameter = 2 * high * high / (1 + base)
                if parameter > 1:
                    capacity = 0
                elif parameter > Q(3, 4):
                    capacity = 1
                elif parameter > Q(2, 3):
                    capacity = 2
                elif parameter > Q(5, 8):
                    capacity = 3
                elif parameter > Q(1, 2):
                    capacity = 4
                elif parameter == Q(1, 2):
                    capacity = 6
            elif high == Q(1, 2):
                capacity = 7
            if capacity is not None and base != -1:
                rows.append((base_index, high, capacity))
    return tuple(rows)


def direction_states(
    base_index: int,
    grid: list[Q],
    triples: list[tuple[int, int, int]],
    nu: list[Q],
) -> tuple[tuple[int, tuple[int, ...]], ...]:
    """Every distinct (required count, ordered half-plane table) state."""

    base = grid[base_index]
    assert base > -1
    occupied = event_weights(base_index, grid, triples, nu)
    event_pairs = set(occupied)
    event_pairs.update(((Q(1), base), (base, Q(1))))
    roots = critical_roots(base, event_pairs)
    states: set[tuple[int, tuple[int, ...]]] = set()

    def add_rational(slope: Q, orientation: int) -> None:
        endpoint_count = sum(
            rational_qualifies(
                first, second, base, slope, orientation
            )
            for first, second in ((Q(1), base), (base, Q(1)))
        )
        table = tuple(
            int(
                rational_qualifies(
                    first, second, base, slope, orientation
                )
            )
            for first in grid
            for second in grid
        )
        states.add((7 - endpoint_count, table))

    def add_root(root, orientation: int) -> None:
        endpoint_count = sum(
            root_qualifies(first, second, base, root, orientation)
            for first, second in ((Q(1), base), (base, Q(1)))
        )
        table = tuple(
            int(root_qualifies(first, second, base, root, orientation))
            for first in grid
            for second in grid
        )
        states.add((7 - endpoint_count, table))

    for sample in open_cell_samples(roots):
        for orientation in (1, -1):
            add_rational(sample, orientation)
    for root in roots:
        for orientation in (1, -1):
            add_root(root, orientation)
    for direction in ((Q(0), Q(1)), (Q(0), Q(-1))):
        endpoint_count = sum(
            direction_qualifies(first, second, base, direction)
            for first, second in ((Q(1), base), (base, Q(1)))
        )
        table = tuple(
            int(direction_qualifies(first, second, base, direction))
            for first in grid
            for second in grid
        )
        states.add((7 - endpoint_count, table))
    return tuple(sorted(states))


def atom_product_features(
    edges: tuple[int, ...],
    base_index: int,
    high_index: int,
    capacity: int,
) -> tuple[np.ndarray, int]:
    """Return half-plane coefficients V[a,b] and the r coefficient.

    The symmetrized row, multiplied by two to clear orientation averaging,
    is

      dot(V,h) + r*R >= 0.
    """

    vector = np.zeros(49, dtype=np.int32)
    gamma_sum = 0
    edge_sum = 0
    for edge_position, (first, second) in enumerate(EDGE_POSITIONS):
        if edges[edge_position] != base_index:
            continue
        edge_sum += 1
        remaining = [
            vertex
            for vertex in range(5)
            if vertex not in (first, second)
        ]
        gamma = []
        for vertex in remaining:
            first_color = edge_color(edges, first, vertex)
            second_color = edge_color(edges, second, vertex)
            gamma.append(
                first_color >= high_index and second_color >= high_index
            )
        gamma_count = sum(gamma)
        gamma_sum += gamma_count
        for oriented_first, oriented_second in (
            (first, second),
            (second, first),
        ):
            for vertex, is_gamma in zip(remaining, gamma):
                first_color = edge_color(edges, oriented_first, vertex)
                second_color = edge_color(edges, oriented_second, vertex)
                coefficient = (
                    13 * capacity
                    - 247 * (gamma_count - int(is_gamma))
                    - 13 * int(is_gamma)
                )
                vector[7 * first_color + second_color] += coefficient
    r_coefficient = 26 * gamma_sum - 2 * capacity * edge_sum
    return vector, r_coefficient


def main() -> None:
    source = json.loads(
        (
            ROOT
            / "certificates"
            / "centered_quarter_bv_pseudodistribution.json"
        ).read_text()
    )
    grid = [Q(value) for value in source["grid"]]
    triples = [tuple(item) for item in source["triple_orbits"]]
    triple_index = {triple: index for index, triple in enumerate(triples)}
    nu = [Q(value) for value in source["nu"]]
    enumeration = (
        ROOT
        / "experiments"
        / "centered_atomic_bv_barrier"
        / "results"
        / "k5_triangle_vectors.csv"
    )
    representatives, features, _header = parse_enumeration(
        enumeration, triple_index
    )
    column_count = len(representatives)
    print(f"representative columns: {column_count}", flush=True)

    equality_rows = []
    equality_columns = []
    equality_values = []
    for column, feature in enumerate(features):
        equality_rows.append(0)
        equality_columns.append(column)
        equality_values.append(1.0)
        counts: dict[int, int] = {}
        for index in feature:
            counts[index] = counts.get(index, 0) + 1
        for index, count in counts.items():
            equality_rows.append(1 + index)
            equality_columns.append(column)
            equality_values.append(float(count))
    equality_matrix = csc_matrix(
        (
            equality_values,
            (equality_rows, equality_columns),
        ),
        shape=(1 + len(triples), column_count),
    )
    equality_target = np.array(
        [1.0] + [float(value / 156) for value in nu]
    )

    families = []
    for base_index, high, capacity in capacity_rows(grid):
        high_index = grid.index(high)
        states = direction_states(
            base_index, grid, triples, nu
        )
        feature_matrix = np.zeros((column_count, 49), dtype=np.int32)
        r_vector = np.zeros(column_count, dtype=np.int32)
        for column, edges in enumerate(representatives):
            feature_matrix[column], r_vector[column] = (
                atom_product_features(
                    edges, base_index, high_index, capacity
                )
            )
        families.append(
            {
                "base_index": base_index,
                "high": high,
                "capacity": capacity,
                "states": states,
                "feature_matrix": feature_matrix,
                "r_vector": r_vector,
            }
        )
        print(
            f"family q={grid[base_index]} b={high} M={capacity}: "
            f"{len(states)} states",
            flush=True,
        )

    cuts: list[np.ndarray] = []
    cut_keys = set()
    solution = None
    for iteration in range(100):
        inequality_matrix = (
            None
            if not cuts
            else -csc_matrix(np.vstack(cuts))
        )
        result = linprog(
            np.zeros(column_count),
            A_ub=inequality_matrix,
            b_ub=None if not cuts else np.zeros(len(cuts)),
            A_eq=equality_matrix,
            b_eq=equality_target,
            bounds=(0, None),
            method="highs",
        )
        print(
            f"iteration {iteration}: success={result.success}, "
            f"cuts={len(cuts)}, message={result.message}",
            flush=True,
        )
        if not result.success:
            raise SystemExit(1)
        solution = result.x
        violations = []
        for family_index, family in enumerate(families):
            expected_features = solution @ family["feature_matrix"]
            expected_r = float(solution @ family["r_vector"])
            for state_index, (required, table) in enumerate(
                family["states"]
            ):
                slack = float(
                    expected_features @ np.array(table)
                    + required * expected_r
                )
                if slack < -1e-7:
                    violations.append(
                        (
                            slack,
                            family_index,
                            state_index,
                            required,
                        )
                    )
        if not violations:
            print(
                f"all rows pass; active="
                f"{np.count_nonzero(solution > 1e-9)}",
                flush=True,
            )
            active = tuple(
                int(index) for index in np.flatnonzero(solution > 1e-9)
            )

            binding_rows = []
            binding_keys = []
            seen_rows = set()
            for family_index, family in enumerate(families):
                for state_index, (required, table) in enumerate(
                    family["states"]
                ):
                    coefficient = (
                        family["feature_matrix"]
                        @ np.array(table, dtype=np.int32)
                        + required * family["r_vector"]
                    ).astype(np.int64)
                    slack = float(coefficient @ solution)
                    if abs(slack) > 1e-6:
                        continue
                    key = coefficient.tobytes()
                    if key in seen_rows:
                        continue
                    seen_rows.add(key)
                    binding_rows.append(coefficient)
                    binding_keys.append(
                        (family_index, state_index, required)
                    )
            print(
                f"distinct binding product rows: {len(binding_rows)}",
                flush=True,
            )

            exact_rows = []
            exact_targets = []
            exact_rows.append([Q(1) for _ in active])
            exact_targets.append(Q(1))
            for triple_index_value in range(len(triples)):
                exact_rows.append(
                    [
                        Q(features[column].count(triple_index_value))
                        for column in active
                    ]
                )
                exact_targets.append(nu[triple_index_value] / 156)
            for row in binding_rows:
                exact_rows.append([Q(int(row[column])) for column in active])
                exact_targets.append(Q(0))

            floating_rows = np.array(
                [[float(value) for value in row] for row in exact_rows]
            )
            _q, _r, row_permutation = qr(
                floating_rows.T, mode="economic", pivoting=True
            )
            independent = tuple(
                int(index) for index in row_permutation[: len(active)]
            )
            assert np.linalg.matrix_rank(
                floating_rows[list(independent)]
            ) == len(active)
            exact_weights = solve_square(
                [exact_rows[index] for index in independent],
                [exact_targets[index] for index in independent],
            )
            assert all(weight > 0 for weight in exact_weights)
            assert all(
                sum(value * weight for value, weight in zip(row, exact_weights))
                == target
                for row, target in zip(exact_rows, exact_targets)
            )

            exact_minimum = None
            zero_rows = []
            for family_index, family in enumerate(families):
                for state_index, (required, table) in enumerate(
                    family["states"]
                ):
                    coefficient = (
                        family["feature_matrix"]
                        @ np.array(table, dtype=np.int32)
                        + required * family["r_vector"]
                    )
                    slack = sum(
                        Q(int(coefficient[column])) * weight
                        for column, weight in zip(active, exact_weights)
                    )
                    assert slack >= 0
                    if exact_minimum is None or slack < exact_minimum:
                        exact_minimum = slack
                    if slack == 0:
                        zero_rows.append(
                            [family_index, state_index, required]
                        )
            assert exact_minimum == 0

            source_path = (
                ROOT
                / "certificates"
                / "centered_quarter_bv_pseudodistribution.json"
            )
            certificate = {
                "schema": (
                    "kissing5.centered_quarter_k5_product_extension.v1"
                ),
                "status": (
                    "exact symmetric local Gram-PSD K5 extension satisfying "
                    "all averaged pair-conditioned depth/capacity product "
                    "rows on the quarter support; not a code and not a "
                    "five-point Lasserre certificate"
                ),
                "source_certificate": source_path.name,
                "source_sha256": hashlib.sha256(
                    source_path.read_bytes()
                ).hexdigest(),
                "enumeration_file": enumeration.name,
                "enumeration_sha256": hashlib.sha256(
                    enumeration.read_bytes()
                ).hexdigest(),
                "normalization": (
                    "atom weights sum to 1; expected triangle counts equal "
                    "nu/156; product rows use the uniform symmetrization of "
                    "each labeled representative"
                ),
                "active_column_indices": list(active),
                "zero_product_row_keys": zero_rows,
                "product_family_summary": [
                    {
                        "base_inner_product": str(
                            grid[family["base_index"]]
                        ),
                        "high_threshold": str(family["high"]),
                        "capacity": family["capacity"],
                        "distinct_direction_states": len(
                            family["states"]
                        ),
                    }
                    for family in families
                ],
                "positive_atom_count": len(active),
                "atoms": [
                    {
                        (
                            "edge_color_indices_"
                            "01_02_03_04_12_13_14_23_24_34"
                        ): list(representatives[column]),
                        "triangle_orbit_indices": list(features[column]),
                        "weight": qstr(weight),
                    }
                    for column, weight in zip(active, exact_weights)
                ],
            }
            output = (
                ROOT
                / "experiments"
                / "four_point_depth_projection"
                / "k5_product_audit"
                / "centered_quarter_k5_product_extension.json"
            )
            output.write_text(
                json.dumps(certificate, indent=2, sort_keys=True) + "\n"
            )
            print(output)
            print(hashlib.sha256(output.read_bytes()).hexdigest())
            return
        violations.sort()
        print(
            "worst violations:",
            violations[: min(10, len(violations))],
            flush=True,
        )
        for _slack, family_index, state_index, _required in violations[:10]:
            key = (family_index, state_index)
            if key in cut_keys:
                continue
            family = families[family_index]
            required, table = family["states"][state_index]
            coefficient = (
                family["feature_matrix"] @ np.array(table, dtype=np.int32)
                + required * family["r_vector"]
            ).astype(float)
            cuts.append(coefficient)
            cut_keys.add(key)
    raise AssertionError("cutting-plane loop did not converge")


if __name__ == "__main__":
    main()
