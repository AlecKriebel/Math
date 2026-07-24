#!/usr/bin/env python3
"""Persistent MILP search with exact global row-type counts and PSD cuts.

This is discovery code.  Its eigenvector cuts are floating-point and neither
an infeasible solver status nor a surviving count vector is a proof.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
import sys

import highspy
import numpy as np
from scipy.sparse import csr_matrix, lil_matrix


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "continuous_rank_bv_search"))
import search as bv  # noqa: E402


def degree_types() -> tuple[tuple[int, ...], ...]:
    """Rows satisfying centering, robust depth, antipodes, and contact degree."""
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
                        if d4 < 0:
                            continue
                        degree = (d0, d1, d2, d3, d4, d5, d6)
                        if d0 + d1 + d2 + d3 < 7 or d5 + d6 < 6:
                            continue
                        if d6 > 15:
                            continue
                        # Projecting the -3/4 neighbours of a vertex into
                        # its orthogonal R^4 gives unit vectors with mutual
                        # inner products at most -1/7.  A strictly obtuse
                        # set in R^4 has at most five vectors.
                        if d1 > 5:
                            continue
                        if d0 and not (
                            d1 == 0 and d2 == d6 and d3 == d5
                        ):
                            continue
                        answer.append(degree)
    return tuple(answer)


def primitive_integer_vector(vector: np.ndarray, scale: int = 10000) -> np.ndarray:
    integers = np.rint(vector / np.max(abs(vector)) * scale).astype(np.int64)
    divisor = 0
    for value in integers:
        divisor = math.gcd(divisor, abs(int(value)))
    if divisor:
        integers //= divisor
    return integers


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=30)
    parser.add_argument("--harmonic-degree", type=int, default=16)
    parser.add_argument("--pair-degree", type=int, default=200)
    parser.add_argument("--time-limit", type=float, default=180)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--exclude-edge-vector",
        action="append",
        default=[],
        metavar="E0,E1,...,E6",
        help=(
            "repeatable exact no-good cut excluding one seven-entry "
            "integer edge-count vector"
        ),
    )
    parser.add_argument(
        "--exclude-spectral-x",
        action="append",
        default=[],
        type=int,
        metavar="X",
        help="repeatable exact no-good cut setting the selector for X=40V to zero",
    )
    args = parser.parse_args()

    nodes = bv.parse_grid("quarter")
    orbits = bv.feasible_orbits(nodes)
    types = degree_types()
    degree_array = np.asarray(types, dtype=np.int64)
    edge_count = 7
    triple_count = len(orbits)
    type_count = len(types)
    type_offset = edge_count + triple_count
    spectral_offset = type_offset + type_count
    # X=40V is an integer and 0<=X<=5002.  For Y=800D, the sharp
    # rank-five skew inequality is exactly 2Y^2<=9X^3.  One binary selector
    # per possible X turns this nonlinear integer condition into a finite
    # exact MILP lift.
    spectral_x_values = tuple(range(5003))
    spectral_y_bounds = tuple(
        math.isqrt(9 * value**3 // 2) for value in spectral_x_values
    )
    assert all(
        2 * bound**2 <= 9 * value**3
        and 2 * (bound + 1) ** 2 > 9 * value**3
        for value, bound in zip(spectral_x_values, spectral_y_bounds)
    )
    forbidden_edge_vectors = []
    for text in args.exclude_edge_vector:
        vector = tuple(int(value) for value in text.split(","))
        if len(vector) != edge_count or any(value < 0 for value in vector):
            parser.error(
                "--exclude-edge-vector requires seven nonnegative integers"
            )
        forbidden_edge_vectors.append(vector)
    forbidden_spectral_x = sorted(set(args.exclude_spectral_x))
    if any(
        value < 0 or value >= len(spectral_x_values)
        for value in forbidden_spectral_x
    ):
        parser.error("--exclude-spectral-x is outside the selector range")
    nogood_offset = spectral_offset + len(spectral_x_values)
    nogood_width = 2 * edge_count
    variable_count = (
        nogood_offset + nogood_width * len(forbidden_edge_vectors)
    )
    edge_upper_bounds = (18, 820, 820, 820, 820, 820, 307)

    rows: list[list[tuple[int, float]]] = []
    lower: list[float] = []
    upper: list[float] = []

    def add(
        entries: list[tuple[int, float]],
        low: float,
        high: float,
    ) -> None:
        rows.append(entries)
        lower.append(low)
        upper.append(high)

    add([(i, 1) for i in range(edge_count)], 820, 820)
    add([(i, i - 4) for i in range(edge_count)], -82, -82)
    add(
        [(edge_count + i, 1) for i in range(triple_count)],
        10660,
        10660,
    )
    for i in range(edge_count):
        add(
            [(i, -39)]
            + [
                (edge_count + orbit_index, triple.count(i))
                for orbit_index, triple in enumerate(orbits)
                if triple.count(i)
            ],
            0,
            0,
        )

    add(
        [
            (spectral_offset + index, 1)
            for index in range(len(spectral_x_values))
        ],
        1,
        1,
    )
    # Exact disjunctive no-goods.  For each forbidden edge vector, at
    # least one selected binary certifies either E_i <= value_i-1 or
    # E_i >= value_i+1.  The big-M constants come from the explicit
    # edge-variable bounds, so no other feasible integer vector is lost.
    for vector_index, vector in enumerate(forbidden_edge_vectors):
        offset = nogood_offset + nogood_width * vector_index
        add(
            [(offset + index, 1) for index in range(nogood_width)],
            1,
            highspy.kHighsInf,
        )
        for index, (value, maximum) in enumerate(
            zip(vector, edge_upper_bounds)
        ):
            low_binary = offset + 2 * index
            high_binary = low_binary + 1
            low_big_m = maximum - value + 1
            high_big_m = value + 1
            add(
                [(index, 1), (low_binary, low_big_m)],
                -highspy.kHighsInf,
                value - 1 + low_big_m,
            )
            add(
                [(index, 1), (high_binary, -high_big_m)],
                value + 1 - high_big_m,
                highspy.kHighsInf,
            )
    # X=5*sum(k^2 E_k)-11808.
    add(
        [
            (index, 5 * (index - 4) ** 2)
            for index in range(edge_count)
        ]
        + [
            (spectral_offset + index, -value)
            for index, value in enumerate(spectral_x_values)
            if value
        ],
        11808,
        11808,
    )
    # Y=3636864-2160*sum(k^2 E_k)+75*sum(abc T_abc).
    # The two rows impose |Y|<=floor(sqrt(9X^3/2)).
    add(
        [
            (index, -2160 * (index - 4) ** 2)
            for index in range(edge_count)
        ]
        + [
            (
                edge_count + orbit_index,
                75 * math.prod(value - 4 for value in triple),
            )
            for orbit_index, triple in enumerate(orbits)
        ]
        + [
            (spectral_offset + index, -bound)
            for index, bound in enumerate(spectral_y_bounds)
            if bound
        ],
        -highspy.kHighsInf,
        -3636864,
    )
    add(
        [
            (index, 2160 * (index - 4) ** 2)
            for index in range(edge_count)
        ]
        + [
            (
                edge_count + orbit_index,
                -75 * math.prod(value - 4 for value in triple),
            )
            for orbit_index, triple in enumerate(orbits)
        ]
        + [
            (spectral_offset + index, -bound)
            for index, bound in enumerate(spectral_y_bounds)
            if bound
        ],
        -highspy.kHighsInf,
        3636864,
    )
    add([(type_offset + i, 1) for i in range(type_count)], 41, 41)
    for i in range(edge_count):
        add(
            [(i, -2)]
            + [
                (type_offset + index, int(degree[i]))
                for index, degree in enumerate(types)
                if degree[i]
            ],
            0,
            0,
        )

    for i in range(edge_count):
        for j in range(i, edge_count):
            entries: list[tuple[int, float]] = []
            if i == j:
                entries.append((i, -2))
            for orbit_index, triple in enumerate(orbits):
                ordered = set(itertools.permutations(triple))
                placements = sum(
                    first == i and second == j
                    for first, second, _third in ordered
                )
                coefficient = 6 * placements // len(ordered)
                if coefficient:
                    entries.append(
                        (edge_count + orbit_index, -coefficient)
                    )
            entries.extend(
                (
                    type_offset + index,
                    int(degree[i] * degree[j]),
                )
                for index, degree in enumerate(types)
                if degree[i] * degree[j]
            )
            add(entries, 0, 0)

    pair_values = np.asarray(
        [
            [float(value) for value in bv.gegenbauer_5(node, args.pair_degree)]
            for node in nodes
        ]
    )
    for degree in range(2, args.pair_degree + 1):
        add(
            [
                (index, pair_values[index, degree])
                for index in range(edge_count)
                if pair_values[index, degree]
            ],
            -20.5,
            highspy.kHighsInf,
        )
    for capacity in bv.stratified_capacity_rows(nodes, orbits):
        add(
            [
                (edge_count + index, float(value))
                for index, value in enumerate(capacity["nu_coefficients"])
                if value
            ]
            + [
                (index, -capacity["capacity"])
                for index in capacity["alpha_indices"]
            ],
            -highspy.kHighsInf,
            0,
        )
    for capacity in bv.weighted_capacity_rows(nodes, orbits):
        add(
            [
                (edge_count + index, float(value))
                for index, value in enumerate(capacity["nu_coefficients"])
                if value
            ]
            + [
                (index, -capacity)
                for index, capacity in capacity["capacities"].items()
            ],
            -highspy.kHighsInf,
            0,
        )

    # Exact rank-five spectral outer band.  For the five eigenvalues of G,
    # V=tr(G^2)-1681/5 and
    # D=tr(G^3)-(123/5)tr(G^2)+137842/25 obey
    # 20D^2 <= 9V^3.  The filtered row types have off-diagonal row square
    # energy at most 41/4, hence V<=2501/20 and therefore |D|<=8V.
    #
    # With edge colors k=-4,...,2 and triangle color products abc,
    # multiplying D-8V<=0 and -D-8V<=0 by 800 gives the two integral rows
    # below.
    add(
        [
            (index, -2960 * (index - 4) ** 2)
            for index in range(edge_count)
        ]
        + [
            (
                edge_count + orbit_index,
                75 * math.prod(value - 4 for value in triple),
            )
            for orbit_index, triple in enumerate(orbits)
        ],
        -highspy.kHighsInf,
        -5526144,
    )
    add(
        [
            (index, 1360 * (index - 4) ** 2)
            for index in range(edge_count)
        ]
        + [
            (
                edge_count + orbit_index,
                -75 * math.prod(value - 4 for value in triple),
            )
            for orbit_index, triple in enumerate(orbits)
        ],
        -highspy.kHighsInf,
        1747584,
    )

    matrix = lil_matrix((len(rows), variable_count), dtype=float)
    for row_index, entries in enumerate(rows):
        for column, value in entries:
            matrix[row_index, column] += value
    matrix = csr_matrix(matrix)

    highs = highspy.Highs()
    highs.setOptionValue("output_flag", False)
    highs.setOptionValue("time_limit", args.time_limit)
    highs.setOptionValue("mip_rel_gap", 0.0)
    column_lower = np.zeros(variable_count)
    column_upper = np.r_[
        edge_upper_bounds,
        np.full(triple_count, 10660),
        np.full(type_count, 41),
        np.ones(len(spectral_x_values)),
        np.ones(nogood_width * len(forbidden_edge_vectors)),
    ]
    for value in forbidden_spectral_x:
        column_upper[spectral_offset + value] = 0
    highs.addVars(variable_count, column_lower, column_upper)
    highs.changeColsIntegrality(
        variable_count,
        np.arange(variable_count, dtype=np.int32),
        np.full(
            variable_count,
            int(highspy.HighsVarType.kInteger),
            dtype=np.uint8,
        ),
    )
    highs.addRows(
        len(rows),
        np.asarray(lower),
        np.asarray(upper),
        len(matrix.data),
        matrix.indptr.astype(np.int32),
        matrix.indices.astype(np.int32),
        matrix.data,
    )

    constants, alpha_arrays, nu_arrays = bv.coefficient_arrays(
        nodes, orbits, args.harmonic_degree
    )
    frame_dimensions = (1, 5, 14, 30)
    frame_subsets = (
        (1,),
        (0, 1),
        (2,),
        (0, 2),
        (1, 2),
        (0, 1, 2),
        (3,),
        (0, 3),
        (1, 3),
        (0, 1, 3),
    )
    frame_values = np.asarray(
        [
            [float(value) for value in bv.gegenbauer_5(node, 3)]
            for node in nodes
        ]
    )
    cut_keys: set[tuple[int, ...]] = set()
    history = []
    solution = None

    def add_cut(coefficients: np.ndarray, target: float) -> bool:
        scale = max(np.max(abs(coefficients)), abs(target), 1.0)
        coefficients = coefficients / scale
        target /= scale
        key = tuple(np.rint(coefficients * 10**10).astype(np.int64))
        if key in cut_keys:
            return False
        cut_keys.add(key)
        indices = np.flatnonzero(abs(coefficients) > 1.0e-14).astype(
            np.int32
        )
        highs.addRow(
            target,
            highspy.kHighsInf,
            len(indices),
            indices,
            coefficients[indices],
        )
        return True

    for iteration in range(args.iterations):
        highs.run()
        model_status = highs.getModelStatus()
        candidate = highs.getSolution()
        info = highs.getInfo()
        if not candidate.value_valid:
            record = {
                "iteration": iteration,
                "status": highs.modelStatusToString(model_status),
                "cuts": len(cut_keys),
                "mip_nodes": int(info.mip_node_count),
            }
            history.append(record)
            print(json.dumps(record), flush=True)
            break

        solution = np.rint(candidate.col_value).astype(np.int64)
        edge_counts = solution[:edge_count]
        triple_counts = solution[edge_count:type_offset]
        alpha = 2 * edge_counts / 41
        nu = 6 * triple_counts / 41
        violations = []
        new_cuts = 0

        for degree in range(args.harmonic_degree + 1):
            size = edge_count + 1
            gram = constants[degree] + np.reshape(
                alpha_arrays[degree] @ alpha
                + nu_arrays[degree] @ nu,
                (size, size),
            )
            eigenvalues, eigenvectors = np.linalg.eigh(gram)
            for eigenvalue, eigenvector in zip(
                eigenvalues, eigenvectors.T
            ):
                if eigenvalue >= -1.0e-7:
                    continue
                z = primitive_integer_vector(eigenvector)
                constant = float(z @ constants[degree] @ z)
                coefficients = np.zeros(variable_count)
                for index in range(edge_count):
                    coefficient_matrix = np.reshape(
                        alpha_arrays[degree][:, index], (size, size)
                    )
                    coefficients[index] = (
                        2 * float(z @ coefficient_matrix @ z) / 41
                    )
                for index in range(triple_count):
                    coefficient_matrix = np.reshape(
                        nu_arrays[degree][:, index], (size, size)
                    )
                    coefficients[edge_count + index] = (
                        6 * float(z @ coefficient_matrix @ z) / 41
                    )
                value = constant + coefficients @ solution
                if value < -1.0e-5 and add_cut(coefficients, -constant):
                    new_cuts += 1
                violations.append(float(eigenvalue))

        for subset in frame_subsets:
            rank = sum(frame_dimensions[index] for index in subset)
            constant_entry = 1 - 41 / rank
            gram = np.asarray(
                [
                    [
                        constant_entry
                        + np.sum(
                            frame_values[:, first]
                            * frame_values[:, second]
                            * alpha
                        )
                        for second in subset
                    ]
                    for first in subset
                ]
            )
            eigenvalues, eigenvectors = np.linalg.eigh(gram)
            for eigenvalue, eigenvector in zip(
                eigenvalues, eigenvectors.T
            ):
                if eigenvalue >= -1.0e-7:
                    continue
                z = primitive_integer_vector(eigenvector)
                constant = constant_entry * int(np.sum(z)) ** 2
                coefficients = np.zeros(variable_count)
                for index in range(edge_count):
                    feature = np.asarray(
                        [
                            frame_values[index, degree]
                            for degree in subset
                        ]
                    )
                    coefficients[index] = (
                        2 * float((z @ feature) ** 2) / 41
                    )
                value = constant + coefficients @ solution
                if value < -1.0e-5 and add_cut(coefficients, -constant):
                    new_cuts += 1
                violations.append(float(eigenvalue))

        active_types = [
            {
                "degree": list(types[index]),
                "count": int(value),
            }
            for index, value in enumerate(
                solution[type_offset:spectral_offset]
            )
            if value
        ]
        selected_spectral_x = [
            value
            for value, selected in zip(
                spectral_x_values, solution[spectral_offset:]
            )
            if selected
        ]
        assert len(selected_spectral_x) == 1
        record = {
            "iteration": iteration,
            "status": highs.modelStatusToString(model_status),
            "cuts": len(cut_keys),
            "new_cuts": new_cuts,
            "mip_nodes": int(info.mip_node_count),
            "worst_psd_eigenvalue": min(violations, default=0.0),
            "edge_counts": edge_counts.tolist(),
            "active_triple_counts": int(np.count_nonzero(triple_counts)),
            "active_degree_types": active_types,
            "spectral_x_40V": selected_spectral_x[0],
        }
        history.append(record)
        print(json.dumps(record), flush=True)
        if not violations or new_cuts == 0:
            break

    output = {
        "schema": "kissing5.centered_global_degree_count_cutting_plane.v1",
        "warning": (
            "NUMERICAL DISCOVERY ONLY: floating eigenvector cuts and MILP "
            "status are not an exact certificate"
        ),
        "degree_type_count": type_count,
        "exact_rank_five_spectral_band": "|D|<=8V",
        "exact_rank_five_spectral_lift": "2*(800D)^2<=9*(40V)^3",
        "excluded_edge_vectors": [
            list(vector) for vector in forbidden_edge_vectors
        ],
        "excluded_spectral_x": forbidden_spectral_x,
        "harmonic_degree": args.harmonic_degree,
        "pair_degree": args.pair_degree,
        "iterations": history,
        "final_edge_counts": (
            None if solution is None else solution[:edge_count].tolist()
        ),
        "final_triple_counts": (
            None
            if solution is None
            else solution[edge_count:type_offset].tolist()
        ),
        "final_degree_type_counts": (
            None
            if solution is None
            else solution[type_offset:spectral_offset].tolist()
        ),
    }
    if args.output:
        args.output.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
