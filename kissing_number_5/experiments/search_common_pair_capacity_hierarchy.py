#!/usr/bin/env python3
"""Discovery reoptimization with cumulative common-pair capacity cuts.

The five-node mode invokes the existing integral cutting-plane model with
the new hierarchy enabled.  The seven-node mode keeps the exact all-harmonic
pair measure fixed and reoptimizes its triple orbit weights against
degree-four BV blocks and every nontrivial hierarchy row.

This historical search omits exact base-stratum/arbitrary-subset rows and
its reported barriers are refuted.  It is retained for reproduction only.
Corrected discovery code is in
``search_common_pair_capacity_stratified.py``.
"""

import argparse
from fractions import Fraction as Q
from itertools import permutations
import json
from pathlib import Path

import cvxpy as cp
import numpy as np

from experiments.search_local_hybrid_degree3 import solve as solve_local
from verifiers.verify_common_pair_capacity_hierarchy import (
    capacity_for_thresholds,
    qualifying_edge_count,
)
from verifiers.verify_fixed41_bv_degree5 import z_matrix


ROOT = Path(__file__).resolve().parents[1]
SEVEN_SOURCE = (
    ROOT
    / "certificates"
    / "fixed41_bv_fullradial_k16_pseudodistribution.json"
)


def fraction_matrix_to_float(matrix):
    return np.array(
        [[float(value) for value in row] for row in matrix],
        dtype=float,
    )


def seven_node_reoptimization():
    source = json.loads(SEVEN_SOURCE.read_text(encoding="utf-8"))
    nodes = tuple(Q(value) for value in source["grid"])
    alpha = tuple(Q(value) for value in source["alpha"])
    triples = tuple(tuple(item) for item in source["triples"])
    source_nu = np.array(
        [float(Q(value)) for value in source["nu"]], dtype=float
    )

    nu = cp.Variable(len(triples), nonneg=True)
    margin = cp.Variable()
    constraints = []

    for index in range(len(nodes)):
        coefficients = np.array(
            [triple.count(index) / 3 for triple in triples],
            dtype=float,
        )
        constraints.append(
            coefficients @ nu == float(39 * alpha[index])
        )

    hierarchy = []
    for base_threshold in (node for node in nodes if node <= 0):
        for high_threshold in (node for node in nodes if node > 0):
            p, capacity = capacity_for_thresholds(
                base_threshold, high_threshold
            )
            if capacity is None:
                continue
            coefficients = np.array(
                [
                    qualifying_edge_count(
                        triple,
                        nodes,
                        base_threshold,
                        high_threshold,
                    )
                    / 3
                    for triple in triples
                ],
                dtype=float,
            )
            right = float(
                capacity
                * sum(
                    weight
                    for node, weight in zip(nodes, alpha)
                    if node <= base_threshold
                )
            )
            constraints.append(coefficients @ nu <= right)
            hierarchy.append(
                (
                    base_threshold,
                    high_threshold,
                    p,
                    capacity,
                    coefficients,
                    right,
                )
            )

    for harmonic_degree in range(5):
        radial_degree = 4 - harmonic_degree
        constant = z_matrix(
            harmonic_degree,
            radial_degree,
            Q(1),
            Q(1),
            Q(1),
        )
        for node, weight in zip(nodes, alpha):
            for point in (
                (Q(1), node, node),
                (node, Q(1), node),
                (node, node, Q(1)),
            ):
                addition = z_matrix(
                    harmonic_degree, radial_degree, *point
                )
                for row in range(radial_degree + 1):
                    for column in range(radial_degree + 1):
                        constant[row][column] += (
                            weight * addition[row][column]
                        )

        coefficients = []
        for triple in triples:
            values = tuple(nodes[index] for index in triple)
            orbit = tuple(sorted(set(permutations(values))))
            matrix = [
                [Q(0) for _ in range(radial_degree + 1)]
                for _ in range(radial_degree + 1)
            ]
            for point in orbit:
                addition = z_matrix(
                    harmonic_degree, radial_degree, *point
                )
                for row in range(radial_degree + 1):
                    for column in range(radial_degree + 1):
                        matrix[row][column] += (
                            addition[row][column] / len(orbit)
                        )
            coefficients.append(fraction_matrix_to_float(matrix))

        affine = fraction_matrix_to_float(constant)
        for variable, coefficient in zip(nu, coefficients):
            affine = affine + variable * coefficient
        constraints.append(
            affine
            - margin * np.eye(radial_degree + 1)
            >> 0
        )

    problem = cp.Problem(cp.Maximize(margin), constraints)
    # The exact source witness is a strict warm start.
    nu.value = source_nu
    result = problem.solve(
        solver="CLARABEL",
        tol_gap_abs=1.0e-9,
        tol_feas=1.0e-9,
        tol_gap_rel=1.0e-9,
        max_iter=500,
    )
    print("status", problem.status)
    print("degree-four common PSD margin", result)
    if nu.value is None:
        return None
    print("minimum orbit weight", float(np.min(nu.value)))
    for (
        base_threshold,
        high_threshold,
        p,
        capacity,
        coefficients,
        right,
    ) in hierarchy:
        left = float(coefficients @ nu.value)
        print(
            "hierarchy",
            base_threshold,
            high_threshold,
            "p",
            p,
            "capacity",
            capacity,
            "slack",
            right - left,
        )
    return nu.value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--support",
        choices=("five", "seven"),
        required=True,
    )
    arguments = parser.parse_args()
    if arguments.support == "five":
        solve_local(
            total_degree=4,
            require_rank_five=True,
            require_color_degree=True,
            require_common_pair_capacity=True,
            support="local5",
            integer=True,
            lp_warm_start=True,
            rank_outer_band="3/100",
        )
    else:
        seven_node_reoptimization()


if __name__ == "__main__":
    main()
