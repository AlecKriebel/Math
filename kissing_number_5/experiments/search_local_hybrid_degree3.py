#!/usr/bin/env python3
"""Search integral triple counts for the five-node local-hybrid support.

This is discovery code, not a verifier.  It alternates mixed-integer linear
optimization with separating eigenvector cuts for fixed-N
Bachoc--Vallentin blocks.
"""

import argparse
from fractions import Fraction as Q
from itertools import combinations_with_replacement

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

from verifiers.verify_local_hybrid_barrier import load_certificate
from verifiers.verify_weighted_residual_barrier import (
    center_count,
    harmonic_matrix,
)


N = 41


def feasible_triples(nodes):
    triples = []
    for triple in combinations_with_replacement(range(len(nodes)), 3):
        u, v, t = (nodes[index] for index in triple)
        determinant = 1 + 2 * u * v * t - u * u - v * v - t * t
        if determinant >= 0:
            triples.append(triple)
    return triples


def affine_blocks(total_degree, nodes, ordered_counts, triples):
    constants = []
    coefficients = []
    for harmonic_degree in range(total_degree + 1):
        constant = harmonic_matrix(
            total_degree, harmonic_degree, nodes, ordered_counts, {}
        )
        constants.append(np.array(constant, dtype=float))
        block_coefficients = []
        for triple in triples:
            full = harmonic_matrix(
                total_degree,
                harmonic_degree,
                nodes,
                ordered_counts,
                {triple: 1},
            )
            block_coefficients.append(
                np.array(
                    [
                        [
                            float(full[i][j] - constant[i][j])
                            for j in range(len(constant))
                        ]
                        for i in range(len(constant))
                    ]
                )
            )
        coefficients.append(block_coefficients)
    return constants, coefficients


def exact_blocks(total_degree, nodes, ordered_counts, triples, values):
    counts = {
        triple: int(value)
        for triple, value in zip(triples, values)
        if value
    }
    return [
        harmonic_matrix(total_degree, k, nodes, ordered_counts, counts)
        for k in range(total_degree + 1)
    ]


def solve(
    total_degree=3,
    require_rank_five=False,
    require_color_degree=False,
    max_rounds=80,
):
    size, nodes, ordered_counts, _, _ = load_certificate()
    assert size == N
    edge_counts = np.array([count // 2 for count in ordered_counts])
    triples = feasible_triples(nodes)
    variable_count = len(triples)
    constants, coefficients = affine_blocks(
        total_degree, nodes, ordered_counts, triples
    )
    block_labels = [f"k={k}" for k in range(total_degree + 1)]
    if require_color_degree:
        color_constant = np.array(
            [
                [
                    (
                        ordered_counts[first]
                        if first == second
                        else 0
                    )
                    - ordered_counts[first]
                    * ordered_counts[second]
                    / N
                    for second in range(len(nodes))
                ]
                for first in range(len(nodes))
            ],
            dtype=float,
        )
        color_coefficients = []
        for triple in triples:
            coefficient = np.zeros((len(nodes), len(nodes)))
            for first in range(len(nodes)):
                first_count = triple.count(first)
                coefficient[first, first] = (
                    first_count * (first_count - 1)
                )
                for second in range(first + 1, len(nodes)):
                    value = first_count * triple.count(second)
                    coefficient[first, second] = value
                    coefficient[second, first] = value
            color_coefficients.append(coefficient)
        constants.append(color_constant)
        coefficients.append(color_coefficients)
        block_labels.append("color-degree")

    incidence = np.array(
        [
            [triple.count(edge_type) for triple in triples]
            for edge_type in range(len(nodes))
        ],
        dtype=float,
    )
    targets = 39 * edge_counts

    # A cut is (harmonic degree, unit direction).  Coordinate cuts make the
    # common-margin variable bounded on the first MILP.
    cuts = []
    for harmonic_degree, constant in enumerate(constants):
        for index in range(len(constant)):
            direction = np.zeros(len(constant))
            direction[index] = 1
            cuts.append((harmonic_degree, direction))

    # Exact universal wedge constraints on this support:
    # 270 <= W_{type 0} <= 275 and 294 <= W_{types 0,1} <= 825.
    wedge_0 = np.array(
        [center_count(triple, {0}) for triple in triples], dtype=float
    )
    wedge_01 = np.array(
        [center_count(triple, {0, 1}) for triple in triples], dtype=float
    )
    mixed_01 = np.array(
        [
            sum(
                (
                    triple[0] == 0 and triple[1] == 1,
                    triple[0] == 0 and triple[2] == 1,
                    triple[1] == 0 and triple[2] == 1,
                    triple[0] == 1 and triple[1] == 0,
                    triple[0] == 1 and triple[2] == 0,
                    triple[1] == 1 and triple[2] == 0,
                )
            )
            for triple in triples
        ],
        dtype=float,
    )
    wedge_1 = np.array(
        [center_count(triple, {1}) for triple in triples], dtype=float
    )
    triple_cycle = np.array(
        [
            float(Q(6, N) * nodes[i] * nodes[j] * nodes[k])
            for i, j, k in triples
        ]
    )
    pair_square = sum(
        Q(count, N) * node**2
        for count, node in zip(ordered_counts, nodes)
    )
    delta = pair_square - Q(36, 5)
    rank_center = Q(1116, 25) + Q(108, 5) * delta
    rank_band = Q(1, 100)
    assert 20 * rank_band**2 < 369 * delta**3

    for round_index in range(max_rounds):
        rows = []
        lower = []
        upper = []

        for row, target in zip(incidence, targets):
            rows.append(np.r_[row, 0.0])
            lower.append(target)
            upper.append(target)

        rows.extend(
            (
                np.r_[wedge_0, 0.0],
                np.r_[wedge_01, 0.0],
                np.r_[mixed_01, 0.0],
                np.r_[wedge_1, 0.0],
            )
        )
        lower.extend((270, 294, 0, 0))
        # There are only three type-1 edges.  Since every type-0 degree is
        # at most five, sum_v d_0(v)d_1(v) <= 5 sum_v d_1(v)=30.
        # Also sum_v binom(d_1(v),2) <= binom(3,2)=3.
        upper.extend((275, 825, 30, 3))
        if require_rank_five:
            # T-rank_center is E in the fixed-N form of C047.  The exact
            # rational band |E|<=1/100 lies strictly inside
            # 20 E^2 <= 369 delta^3.
            rows.append(np.r_[triple_cycle, 0.0])
            lower.append(float(rank_center - rank_band))
            upper.append(float(rank_center + rank_band))

        for harmonic_degree, direction in cuts:
            constant_value = (
                direction @ constants[harmonic_degree] @ direction
            )
            coefficient_values = np.array(
                [
                    direction @ coefficient @ direction
                    for coefficient in coefficients[harmonic_degree]
                ]
            )
            # Harmonic blocks seek a common positive margin.  The centered
            # color-degree covariance has the structural null vector
            # (1,...,1), so its cuts impose only nonnegativity.
            margin_coefficient = (
                0.0
                if block_labels[harmonic_degree] == "color-degree"
                else -1.0
            )
            rows.append(np.r_[coefficient_values, margin_coefficient])
            lower.append(-constant_value)
            upper.append(np.inf)

        objective = np.r_[np.zeros(variable_count), -1.0]
        bounds = Bounds(
            np.r_[np.zeros(variable_count), -1.0e5],
            np.r_[np.full(variable_count, 10660.0), 1.0e5],
        )
        integrality = np.r_[np.ones(variable_count), 0]
        result = milp(
            objective,
            integrality=integrality,
            bounds=bounds,
            constraints=LinearConstraint(
                np.array(rows), np.array(lower), np.array(upper)
            ),
            options={
                "time_limit": 20.0,
                "mip_rel_gap": 0.0,
                "presolve": True,
            },
        )
        print(
            "round",
            round_index,
            "status",
            result.status,
            "message",
            result.message,
        )
        if result.x is None:
            return None

        values = np.rint(result.x[:variable_count]).astype(int)
        margin = result.x[-1]
        assert np.array_equal(incidence.astype(int) @ values, targets)
        print(
            "reported margin",
            margin,
            "wedges",
            int(wedge_0 @ values),
            int(wedge_01 @ values),
            "mixed",
            int(mixed_01 @ values),
            "type1",
            int(wedge_1 @ values),
            "rank E",
            float(triple_cycle @ values - float(rank_center)),
        )

        violations = []
        minimum_eigenvalues = []
        for block_index in range(len(constants)):
            matrix = constants[block_index].copy()
            for value, coefficient in zip(
                values, coefficients[block_index]
            ):
                matrix += value * coefficient
            eigenvalues, eigenvectors = np.linalg.eigh(matrix)
            print(" ", block_labels[block_index], "eigenvalues", eigenvalues)
            minimum_eigenvalues.append(eigenvalues[0])
            target = (
                0.0
                if block_labels[block_index] == "color-degree"
                else margin
            )
            if eigenvalues[0] < target - 1.0e-7:
                violations.append(
                    (block_index, eigenvectors[:, 0], eigenvalues[0])
                )

        # Feasibility, rather than optimization of the artificial common
        # margin, is the research question.  Emit the first numerically
        # positive integral incumbent; it will subsequently require exact
        # rational verification.
        numerically_feasible = all(
            (
                eigenvalue > -1.0e-7
                if label == "color-degree"
                else eigenvalue > 1.0e-7
            )
            for label, eigenvalue in zip(
                block_labels, minimum_eigenvalues
            )
        )
        if numerically_feasible:
            counts = {
                triple: int(value)
                for triple, value in zip(triples, values)
                if value
            }
            print("candidate counts")
            for item in counts.items():
                print(item)
            print("exact blocks")
            for harmonic_degree, matrix in enumerate(
                exact_blocks(
                    total_degree, nodes, ordered_counts, triples, values
                )
            ):
                print("k", harmonic_degree)
                for row in matrix:
                    print([str(entry) for entry in row])
            return counts

        for block_index, direction, _ in violations:
            cuts.append((block_index, direction))

    raise RuntimeError("cutting-plane iteration limit reached")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, default=3)
    parser.add_argument("--rank-five", action="store_true")
    parser.add_argument("--color-degree", action="store_true")
    arguments = parser.parse_args()
    solve(
        arguments.degree,
        arguments.rank_five,
        arguments.color_degree,
    )
