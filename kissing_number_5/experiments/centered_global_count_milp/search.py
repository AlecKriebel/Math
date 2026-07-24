#!/usr/bin/env python3
"""Mixed-integer cutting-plane search for global edge/triple count shadows."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "continuous_rank_bv_search"))
import search as bv  # noqa: E402


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
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--harmonic-degree", type=int, default=16)
    parser.add_argument("--pair-degree", type=int, default=200)
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    nodes = bv.parse_grid("quarter")
    orbits = bv.feasible_orbits(nodes)
    node_count = len(nodes)
    orbit_count = len(orbits)
    variable_count = node_count + orbit_count

    equality_rows: list[np.ndarray] = []
    equality_targets: list[float] = []
    lower_rows: list[np.ndarray] = []
    lower_targets: list[float] = []
    upper_rows: list[np.ndarray] = []
    upper_targets: list[float] = []

    def blank() -> np.ndarray:
        return np.zeros(variable_count)

    row = blank()
    row[:node_count] = 1
    equality_rows.append(row)
    equality_targets.append(820)
    row = blank()
    row[:node_count] = np.arange(-4, 3)
    equality_rows.append(row)
    equality_targets.append(-82)
    row = blank()
    row[node_count:] = 1
    equality_rows.append(row)
    equality_targets.append(10660)
    for index in range(node_count):
        row = blank()
        row[index] = -39
        row[node_count:] = [
            triple.count(index) for triple in orbits
        ]
        equality_rows.append(row)
        equality_targets.append(0)

    row = blank()
    row[:4] = 1
    lower_rows.append(row)
    lower_targets.append(144)
    # The graph of pairs with inner product strictly below -1/2 is
    # triangle-free and has independence number at most 20, hence has at
    # least 23 edges.  On the quarter grid these are exactly colors 0 and 1.
    row = blank()
    row[:2] = 1
    lower_rows.append(row)
    lower_targets.append(23)
    row = blank()
    row[5:7] = 1
    lower_rows.append(row)
    lower_targets.append(123)

    pair_values = np.asarray(
        [
            [float(value) for value in bv.gegenbauer_5(node, args.pair_degree)]
            for node in nodes
        ]
    )
    for degree in range(2, args.pair_degree + 1):
        row = blank()
        row[:node_count] = pair_values[:, degree]
        lower_rows.append(row)
        lower_targets.append(-20.5)

    for capacity in bv.stratified_capacity_rows(nodes, orbits):
        row = blank()
        row[node_count:] = capacity["nu_coefficients"]
        row[list(capacity["alpha_indices"])] -= capacity["capacity"]
        upper_rows.append(row)
        upper_targets.append(0)
    for capacity in bv.weighted_capacity_rows(nodes, orbits):
        row = blank()
        row[node_count:] = capacity["nu_coefficients"]
        for index, value in capacity["capacities"].items():
            row[index] -= value
        upper_rows.append(row)
        upper_targets.append(0)

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

    def add_lower_cut(coefficients: np.ndarray, target: float) -> bool:
        scale = max(np.max(abs(coefficients)), abs(target), 1.0)
        coefficients = coefficients / scale
        target /= scale
        key = tuple(np.rint(coefficients * 10**10).astype(np.int64))
        if key in cut_keys:
            return False
        cut_keys.add(key)
        lower_rows.append(coefficients)
        lower_targets.append(target)
        return True

    for iteration in range(args.iterations):
        constraints = [
            LinearConstraint(
                np.asarray(equality_rows),
                np.asarray(equality_targets),
                np.asarray(equality_targets),
            ),
            LinearConstraint(
                np.asarray(lower_rows),
                np.asarray(lower_targets),
                np.full(len(lower_rows), np.inf),
            ),
            LinearConstraint(
                np.asarray(upper_rows),
                np.full(len(upper_rows), -np.inf),
                np.asarray(upper_targets),
            ),
        ]
        upper_bounds = np.r_[
        # If there are r antipodal pairs, the remaining vertices have a
        # triangle-free deep-pair graph with independence number at most
        # 20-r (otherwise representatives of the r pairs and such an
        # independent set give 21 projective lines).  For r=19 the three
        # remaining vertices would have independence number at most one,
        # forcing a triangle.  Thus r <= 18.
        np.asarray([18, 820, 820, 820, 820, 820, 820]),
            np.full(orbit_count, 10660),
        ]
        result = milp(
            np.zeros(variable_count),
            integrality=np.ones(variable_count),
            bounds=Bounds(np.zeros(variable_count), upper_bounds),
            constraints=constraints,
            options={"time_limit": args.time_limit, "mip_rel_gap": 0},
        )
        if result.x is None:
            history.append(
                {
                    "iteration": iteration,
                    "status": result.message,
                    "cuts": len(cut_keys),
                }
            )
            print(json.dumps(history[-1]), flush=True)
            break
        solution = np.rint(result.x).astype(np.int64)
        edge_counts = solution[:node_count]
        triple_counts = solution[node_count:]
        alpha = 2 * edge_counts / 41
        nu = 6 * triple_counts / 41

        violations = []
        new_cuts = 0
        for degree in range(args.harmonic_degree + 1):
            size = node_count + 1
            matrix = constants[degree] + np.reshape(
                alpha_arrays[degree] @ alpha
                + nu_arrays[degree] @ nu,
                (size, size),
            )
            eigenvalues, eigenvectors = np.linalg.eigh(matrix)
            for eigenvalue, eigenvector in zip(
                eigenvalues, eigenvectors.T
            ):
                if eigenvalue >= -1.0e-7:
                    continue
                z = primitive_integer_vector(eigenvector)
                constant = float(z @ constants[degree] @ z)
                coefficients = blank()
                for index in range(node_count):
                    coefficient_matrix = np.reshape(
                        alpha_arrays[degree][:, index], (size, size)
                    )
                    coefficients[index] = (
                        2 * float(z @ coefficient_matrix @ z) / 41
                    )
                for index in range(orbit_count):
                    coefficient_matrix = np.reshape(
                        nu_arrays[degree][:, index], (size, size)
                    )
                    coefficients[node_count + index] = (
                        6 * float(z @ coefficient_matrix @ z) / 41
                    )
                value = constant + coefficients @ solution
                if value < -1.0e-5 and add_lower_cut(
                    coefficients, -constant
                ):
                    new_cuts += 1
                violations.append(
                    {
                        "family": f"BV{degree}",
                        "eigenvalue": float(eigenvalue),
                        "integer_cut_value": float(value),
                    }
                )

        for subset in frame_subsets:
            rank = sum(frame_dimensions[index] for index in subset)
            constant_entry = 1 - 41 / rank
            matrix = np.asarray(
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
            eigenvalues, eigenvectors = np.linalg.eigh(matrix)
            for eigenvalue, eigenvector in zip(
                eigenvalues, eigenvectors.T
            ):
                if eigenvalue >= -1.0e-7:
                    continue
                z = primitive_integer_vector(eigenvector)
                constant = constant_entry * int(np.sum(z)) ** 2
                coefficients = blank()
                for index in range(node_count):
                    feature = np.asarray(
                        [frame_values[index, degree] for degree in subset]
                    )
                    coefficients[index] = (
                        2 * float((z @ feature) ** 2) / 41
                    )
                value = constant + coefficients @ solution
                if value < -1.0e-5 and add_lower_cut(
                    coefficients, -constant
                ):
                    new_cuts += 1
                violations.append(
                    {
                        "family": f"frame{subset}",
                        "eigenvalue": float(eigenvalue),
                        "integer_cut_value": float(value),
                    }
                )

        worst = min(
            (item["eigenvalue"] for item in violations),
            default=0.0,
        )
        record = {
            "iteration": iteration,
            "cuts": len(cut_keys),
            "new_cuts": new_cuts,
            "worst_psd_eigenvalue": worst,
            "edge_counts": edge_counts.tolist(),
            "active_triple_counts": int(np.count_nonzero(triple_counts)),
        }
        history.append(record)
        print(json.dumps(record), flush=True)
        if not violations:
            break
        if new_cuts == 0:
            record["status"] = "stalled: only duplicate/numerically weak cuts"
            break

    output = {
        "schema": "kissing5.centered_global_count_cutting_plane.v1",
        "warning": (
            "NUMERICAL DISCOVERY ONLY: floating eigenvector cuts and MILP "
            "status are not an exact certificate"
        ),
        "harmonic_degree": args.harmonic_degree,
        "pair_degree": args.pair_degree,
        "iterations": history,
        "final_edge_counts": (
            None if solution is None else solution[:node_count].tolist()
        ),
        "final_triple_counts": (
            None if solution is None else solution[node_count:].tolist()
        ),
    }
    if args.output:
        args.output.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
