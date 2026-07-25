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

from verifiers.verify_local_hybrid_barrier import (
    common_center_bound,
    integer_wedge_minimum,
    load_certificate,
    threshold_test_points,
    zonal_values,
)
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


def common_pair_capacity(p):
    """Universal S^2 capacity from the common-pair projection hierarchy."""

    if p > 1:
        return 0
    if p > Q(3, 4):
        return 1
    if p > Q(2, 3):
        return 2
    if p > Q(5, 8):
        return 3
    if p > Q(1, 2):
        return 4
    if p == Q(1, 2):
        return 6
    return None


def common_pair_capacity_rows(nodes, ordered_counts, triples):
    """Historical cumulative rows only; not the full pointwise hierarchy.

    The candidate found with these rows is REFUTED by exact base-color
    strata.  Corrected discovery code is in
    ``search_common_pair_capacity_stratified.py``.
    """

    answer = []
    for base_threshold in (node for node in nodes if node <= 0):
        for high_threshold in (node for node in nodes if node > 0):
            if base_threshold == -1:
                capacity = 0
                p = None
            else:
                p = 2 * high_threshold**2 / (1 + base_threshold)
                capacity = common_pair_capacity(p)
            if capacity is None:
                continue
            row = np.array(
                [
                    sum(
                        (
                            nodes[triple[0]] <= base_threshold
                            and nodes[triple[1]] >= high_threshold
                            and nodes[triple[2]] >= high_threshold,
                            nodes[triple[1]] <= base_threshold
                            and nodes[triple[0]] >= high_threshold
                            and nodes[triple[2]] >= high_threshold,
                            nodes[triple[2]] <= base_threshold
                            and nodes[triple[0]] >= high_threshold
                            and nodes[triple[1]] >= high_threshold,
                        )
                    )
                    for triple in triples
                ],
                dtype=float,
            )
            upper = capacity * sum(
                count // 2
                for node, count in zip(nodes, ordered_counts)
                if node <= base_threshold
            )
            answer.append(
                (
                    base_threshold,
                    high_threshold,
                    p,
                    capacity,
                    row,
                    upper,
                )
            )
    return tuple(answer)


def rank_kernel_interval(
    nodes,
    ordered_counts,
    triples,
    harmonic_weights,
    rank_bound,
    rational_band,
):
    """A rational outer interval from the rank spectral-moment inequality.

    For K=sum_k a_k(P_k(<x_i,x_j>)) with arbitrary real a_k, K is symmetric
    and has rank at most the sum of the corresponding harmonic dimensions.
    The centered third spectral moment D therefore obeys

        r(r-1) D^2 <= (r-2)^2 V^3.

    Pair data fix tr(K), tr(K^2), and hence V.  Only tr(K^3) depends on the
    triangle variables, so any rational band outside the square-root bound
    gives two valid linear constraints.
    """

    maximum_degree = max(harmonic_weights)

    def kernel(t):
        values = zonal_values(t, maximum_degree)
        return sum(
            coefficient * values[degree]
            for degree, coefficient in harmonic_weights.items()
        )

    diagonal = kernel(Q(1))
    node_values = tuple(kernel(node) for node in nodes)
    pair_square = sum(
        Q(count) * value**2
        for count, value in zip(ordered_counts, node_values)
    )
    trace_one = N * diagonal
    trace_two = N * diagonal**2 + pair_square
    variance = trace_two - trace_one**2 / rank_bound
    center = (
        Q(3) * trace_one * trace_two / rank_bound
        - Q(2) * trace_one**3 / rank_bound**2
    )
    assert variance >= 0
    assert (
        rank_bound * (rank_bound - 1) * rational_band**2
        > (rank_bound - 2) ** 2 * variance**3
    )
    constant_trace_three = (
        N * diagonal**3 + 3 * diagonal * pair_square
    )
    row = np.array(
        [
            float(6 * node_values[i] * node_values[j] * node_values[k])
            for i, j, k in triples
        ],
        dtype=float,
    )
    return (
        row,
        float(center - rational_band - constant_trace_three),
        float(center + rational_band - constant_trace_three),
    )


def solve(
    total_degree=3,
    require_rank_five=False,
    require_color_degree=False,
    require_common_pair_capacity=False,
    support="local5",
    integer=True,
    lp_warm_start=False,
    rank_outer_band=None,
    max_rounds=80,
):
    if support == "local5":
        size, nodes, ordered_counts, _, _ = load_certificate()
        assert size == N
    elif support == "six":
        nodes = (
            Q(-157, 200),
            Q(-39, 50),
            Q(-9, 20),
            Q(-1, 10),
            Q(-19, 200),
            Q(99, 200),
        )
        ordered_counts = (32, 132, 264, 130, 522, 560)
    else:
        raise ValueError(f"unknown support {support!r}")
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

    # Exact universal wedge constraints on this support.
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
    threshold_constraints = []
    for q in threshold_test_points(nodes):
        deep_types = {
            index
            for index, node in enumerate(nodes)
            if node < 0 and node * node >= q
        }
        high_types = {
            index
            for index, node in enumerate(nodes)
            if node >= 2 * q - 1
        }
        deep_degree = sum(
            ordered_counts[index] for index in deep_types
        )
        high_edges = sum(
            ordered_counts[index] // 2 for index in high_types
        )
        row = np.array(
            [
                center_count(triple, deep_types)
                for triple in triples
            ],
            dtype=float,
        )
        lower = integer_wedge_minimum(deep_degree, N)
        upper = common_center_bound(q) * high_edges
        threshold_constraints.append((row, lower, upper))
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
    if rank_outer_band is None:
        rank_band = (
            Q(29, 1000) if support == "local5" else Q(19, 625)
        )
        # Historical construction search: this is a sufficient inner
        # interval for C047, not a necessary relaxation of all C047 points.
        assert 20 * rank_band**2 < 369 * delta**3
    else:
        rank_band = Q(rank_outer_band)
        # A rational outer interval is a valid necessary linear relaxation
        # of the exact square-root C047 interval.
        assert 20 * rank_band**2 > 369 * delta**3
    rank_kernel_constraints = (
        (
            "H0/6+5H1/6",
            rank_kernel_interval(
                nodes,
                ordered_counts,
                triples,
                {0: Q(1, 6), 1: Q(5, 6)},
                6,
                Q(7, 2),
            ),
        ),
        (
            "H2",
            rank_kernel_interval(
                nodes,
                ordered_counts,
                triples,
                {2: Q(1)},
                14,
                Q(157, 50),
            ),
        ),
    )
    common_pair_constraints = (
        common_pair_capacity_rows(nodes, ordered_counts, triples)
        if require_common_pair_capacity
        else ()
    )

    current_integer = integer and not lp_warm_start
    for round_index in range(max_rounds):
        rows = []
        lower = []
        upper = []

        for row, target in zip(incidence, targets):
            rows.append(np.r_[row, 0.0])
            lower.append(target)
            upper.append(target)

        for row, row_lower, row_upper in threshold_constraints:
            rows.append(np.r_[row, 0.0])
            lower.append(row_lower)
            upper.append(row_upper)
        for _, _, _, capacity, row, row_upper in common_pair_constraints:
            rows.append(np.r_[row, 0.0])
            lower.append(0)
            upper.append(row_upper)
        if support == "local5":
            rows.extend(
                (
                    np.r_[mixed_01 + 2 * wedge_1, 0.0],
                    np.r_[wedge_1, 0.0],
                )
            )
            lower.extend((0, 0))
            # A color-{0,1} neighborhood is a color-4 equidistant clique:
            # every other closing color gives a non-PSD 3 by 3 Gram matrix.
            # Its size is at most five by rank.  Thus d_0+d_1<=5 at each
            # vertex.  Hence
            #
            #   d_0 d_1 + d_1(d_1-1)
            #       = d_1(d_0+d_1-1) <= 4d_1.
            #
            # Summing gives W_01+2W_11<=4D_1=24.  Also W_11<=3.
            upper.extend((24, 3))
        else:
            # Pfender's row inequality makes the union of the first two
            # colors have degree at most four.  Its total degree is exactly
            # 4N, hence it is 4-regular and has exactly 41*binom(4,2)
            # centered wedges.
            rows.append(np.r_[wedge_01, 0.0])
            lower.append(246)
            upper.append(246)
        if require_rank_five:
            # T-rank_center is E in the fixed-N form of C047.  The selected
            # exact rational band lies strictly inside
            # 20 E^2 <= 369 delta^3.
            rows.append(np.r_[triple_cycle, 0.0])
            lower.append(float(rank_center - rank_band))
            upper.append(float(rank_center + rank_band))
            for _, (row, row_lower, row_upper) in rank_kernel_constraints:
                rows.append(np.r_[row, 0.0])
                lower.append(row_lower)
                upper.append(row_upper)

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
        integrality = np.r_[
            (
                np.ones(variable_count)
                if current_integer
                else np.zeros(variable_count)
            ),
            0,
        ]
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

        values = (
            np.rint(result.x[:variable_count]).astype(int)
            if current_integer
            else result.x[:variable_count]
        )
        margin = result.x[-1]
        if current_integer:
            assert np.array_equal(
                incidence.astype(int) @ values, targets
            )
        else:
            assert np.allclose(incidence @ values, targets, atol=1.0e-5)
        print(
            "reported margin",
            margin,
            "wedges",
            float(wedge_0 @ values),
            float(wedge_01 @ values),
            "mixed",
            float(mixed_01 @ values),
            "type1",
            float(wedge_1 @ values),
            "rank E",
            float(triple_cycle @ values - float(rank_center)),
        )
        if require_rank_five:
            for label, (row, row_lower, row_upper) in (
                rank_kernel_constraints
            ):
                value = float(row @ values)
                print(
                    " rank-kernel",
                    label,
                    "value",
                    value,
                    "interval",
                    (row_lower, row_upper),
                )
        if common_pair_constraints:
            print(" common-pair capacities")
            for (
                base_threshold,
                high_threshold,
                p,
                capacity,
                row,
                row_upper,
            ) in common_pair_constraints:
                print(
                    "  ",
                    base_threshold,
                    high_threshold,
                    "p",
                    p,
                    "capacity",
                    capacity,
                    "value",
                    float(row @ values),
                    "upper",
                    row_upper,
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
            if integer and not current_integer:
                print(
                    "continuous warm start is feasible; retaining cuts and "
                    "switching to integral counts"
                )
                current_integer = True
                continue
            counts = {
                triple: (
                    int(value) if current_integer else float(value)
                )
                for triple, value in zip(triples, values)
                if abs(value) > 1.0e-8
            }
            print("candidate counts")
            for item in counts.items():
                print(item)
            if current_integer:
                print("exact blocks")
                for harmonic_degree, matrix in enumerate(
                    exact_blocks(
                        total_degree,
                        nodes,
                        ordered_counts,
                        triples,
                        values,
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
    parser.add_argument("--common-pair-capacity", action="store_true")
    parser.add_argument(
        "--support", choices=("local5", "six"), default="local5"
    )
    parser.add_argument("--continuous", action="store_true")
    parser.add_argument("--lp-warm-start", action="store_true")
    parser.add_argument(
        "--rank-outer-band",
        help=(
            "rational outer half-width for C047, e.g. 3/100; "
            "must strictly contain the exact interval"
        ),
    )
    arguments = parser.parse_args()
    solve(
        arguments.degree,
        arguments.rank_five,
        arguments.color_degree,
        arguments.common_pair_capacity,
        arguments.support,
        not arguments.continuous,
        arguments.lp_warm_start,
        arguments.rank_outer_band,
    )
