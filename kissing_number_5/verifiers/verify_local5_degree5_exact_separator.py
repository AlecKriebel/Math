#!/usr/bin/env python3
"""Verify the exact finite-cut separator on the local five-node support.

The JSON certificate stores only fourteen small rational cut directions and
an active basis.  This verifier rebuilds every affine inequality, solves the
19 by 19 active dual system over ``Fraction``, and checks the resulting dual
certificate directly.  It does not invoke an LP or SDP solver.

This is a support- and band-specific relaxation result.  In particular, the
rank-moment band used here is a strict inner band of C047, not a replacement
for the full nonlinear C047 feasible interval.
"""

from fractions import Fraction as Q
from itertools import combinations_with_replacement
import json
from math import comb
from pathlib import Path

try:
    from verifiers.verify_local_hybrid_barrier import (
        common_center_bound,
        load_certificate as load_pair_certificate,
        zonal_values,
    )
    from verifiers.verify_weighted_residual_barrier import (
        center_count,
        harmonic_matrix,
    )
except ModuleNotFoundError:  # Direct execution from this directory.
    from verify_local_hybrid_barrier import (
        common_center_bound,
        load_certificate as load_pair_certificate,
        zonal_values,
    )
    from verify_weighted_residual_barrier import (
        center_count,
        harmonic_matrix,
    )


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT / "certificates" / "local5_degree5_exact_separator.json"
)
N = 41
DEGREE = 5


def quadratic(matrix, vector):
    return sum(
        vector[i] * matrix[i][j] * vector[j]
        for i in range(len(vector))
        for j in range(len(vector))
    )


def solve_square(matrix, right):
    """Solve a nonsingular rational square system by Gauss--Jordan."""

    size = len(matrix)
    assert size and all(len(row) == size for row in matrix)
    assert len(right) == size
    augmented = [
        [Q(value) for value in row] + [Q(value)]
        for row, value in zip(matrix, right)
    ]
    for column in range(size):
        pivot = next(
            row
            for row in range(column, size)
            if augmented[row][column]
        )
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        scale = augmented[column][column]
        augmented[column] = [
            value / scale for value in augmented[column]
        ]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    value - scale * pivot_value
                    for value, pivot_value in zip(
                        augmented[row], augmented[column]
                    )
                ]
    return [augmented[row][-1] for row in range(size)]


def feasible_triples(nodes):
    triples = []
    for triple in combinations_with_replacement(range(len(nodes)), 3):
        u, v, t = (nodes[index] for index in triple)
        determinant = 1 + 2 * u * v * t - u * u - v * v - t * t
        if determinant >= 0:
            triples.append(triple)
    return tuple(triples)


def affine_blocks(nodes, ordered_counts, triples):
    constants = []
    coefficients = []
    for harmonic_degree in range(DEGREE + 1):
        constant = harmonic_matrix(
            DEGREE, harmonic_degree, nodes, ordered_counts, {}
        )
        constants.append(constant)
        block_coefficients = []
        for triple in triples:
            full = harmonic_matrix(
                DEGREE,
                harmonic_degree,
                nodes,
                ordered_counts,
                {triple: 1},
            )
            block_coefficients.append(
                [
                    [
                        full[i][j] - constant[i][j]
                        for j in range(len(constant))
                    ]
                    for i in range(len(constant))
                ]
            )
        coefficients.append(block_coefficients)

    # The last block is the centered covariance of the five colored degree
    # columns.  Its affine variables are the unordered triangle counts.
    color_constant = [
        [
            (
                Q(ordered_counts[first])
                if first == second
                else Q(0)
            )
            - Q(
                ordered_counts[first] * ordered_counts[second], N
            )
            for second in range(len(nodes))
        ]
        for first in range(len(nodes))
    ]
    color_coefficients = []
    for triple in triples:
        coefficient = [
            [Q(0) for _ in nodes] for _ in nodes
        ]
        for first in range(len(nodes)):
            first_count = triple.count(first)
            coefficient[first][first] = Q(
                first_count * (first_count - 1)
            )
            for second in range(first + 1, len(nodes)):
                value = Q(first_count * triple.count(second))
                coefficient[first][second] = value
                coefficient[second][first] = value
        color_coefficients.append(coefficient)
    constants.append(color_constant)
    coefficients.append(color_coefficients)
    return constants, coefficients


def harmonic_dimension(degree):
    return comb(degree + 4, 4) - (
        comb(degree + 2, 4) if degree >= 2 else 0
    )


def rank_kernel_affine(
    nodes,
    ordered_counts,
    triples,
    harmonic_weights,
    rank_bound,
    outer_band,
):
    maximum_degree = max(harmonic_weights)

    def kernel(t):
        values = zonal_values(t, maximum_degree)
        return sum(
            coefficient * values[degree]
            for degree, coefficient in harmonic_weights.items()
        )

    assert rank_bound == sum(
        harmonic_dimension(degree) for degree in harmonic_weights
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
        rank_bound * (rank_bound - 1) * outer_band**2
        > (rank_bound - 2) ** 2 * variance**3
    )
    constant_trace_three = (
        N * diagonal**3 + 3 * diagonal * pair_square
    )
    row = [
        6 * node_values[i] * node_values[j] * node_values[k]
        for i, j, k in triples
    ]
    return (
        row,
        center - outer_band - constant_trace_three,
        center + outer_band - constant_trace_three,
    )


def load_certificate(path=CERTIFICATE):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["schema"] == (
        "local5-degree5-finite-cut-exact-separator-v1"
    )
    assert data["dimension"] == 5
    assert data["cardinality"] == N
    assert Q(data["maximum_inner_product"]) == Q(1, 2)
    assert data["total_degree"] == DEGREE
    nodes = tuple(Q(value) for value in data["nodes"])
    ordered_counts = tuple(data["ordered_pair_counts"])
    rank_band = Q(data["rank_band"])
    rank_band_mode = data.get("rank_band_mode", "inner")
    assert rank_band_mode in {"inner", "outer"}
    basic = tuple(data["basic_triple_indices"])
    active = tuple(data["active_inequalities"])

    size, pair_nodes, pair_counts, _, _ = load_pair_certificate()
    assert size == N
    assert nodes == pair_nodes
    assert ordered_counts == pair_counts
    assert len(active) == 14
    assert len(basic) == 18
    assert len(set(basic)) == len(basic)
    return (
        data.get("variant", "historical-inner-band"),
        nodes,
        ordered_counts,
        rank_band,
        rank_band_mode,
        basic,
        active,
    )


def build_equalities(ordered_counts, triples):
    rows = [
        [Q(triple.count(edge_type)) for triple in triples] + [Q(0)]
        for edge_type in range(len(ordered_counts))
    ]
    targets = [
        Q((N - 2) * (count // 2)) for count in ordered_counts
    ]
    return rows, targets


def build_active_inequalities(
    nodes,
    ordered_counts,
    triples,
    constants,
    coefficients,
    rank_band,
    rank_band_mode,
    active_items,
):
    """Return the active rows in the convention A(x,z) <= b."""

    rows = []
    bounds = []
    labels = []
    triple_variable_count = len(triples)

    pair_square = sum(
        Q(count, N) * node**2
        for count, node in zip(ordered_counts, nodes)
    )
    delta = pair_square - Q(36, 5)
    rank_center = Q(1116, 25) + Q(108, 5) * delta
    if rank_band_mode == "inner":
        # Every point in this interval satisfies C047, but C047 also permits
        # two thin outer slivers.
        assert 20 * rank_band**2 < 369 * delta**3
    else:
        # The full C047 interval lies strictly inside this rational interval,
        # so these two linear bounds are necessary for every realization.
        assert 20 * rank_band**2 > 369 * delta**3
    cycle = [
        Q(6, N) * nodes[i] * nodes[j] * nodes[k]
        for i, j, k in triples
    ]

    for item in active_items:
        kind = item["kind"]
        if kind == "threshold_upper":
            q = Q(item["q"])
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
            row = [
                Q(center_count(triple, deep_types))
                for triple in triples
            ] + [Q(0)]
            high_edges = sum(
                ordered_counts[index] // 2 for index in high_types
            )
            bound = Q(common_center_bound(q) * high_edges)
            label = f"threshold-{q}-upper"
        elif kind == "colored_clique":
            row = []
            for triple in triples:
                count0 = triple.count(0)
                count1 = triple.count(1)
                row.append(
                    Q(count0 * count1 + count1 * (count1 - 1))
                )
            row.append(Q(0))
            bound = Q(4 * ordered_counts[1])
            label = "colored-clique"
        elif kind == "c047_lower":
            row = [-value for value in cycle] + [Q(0)]
            bound = -(rank_center - rank_band)
            label = f"C047-{rank_band_mode}-band-lower"
        elif kind in {"rank_kernel_lower", "rank_kernel_upper"}:
            weights = {
                int(degree): Q(coefficient)
                for degree, coefficient in item[
                    "harmonic_weights"
                ].items()
            }
            kernel_row, lower_bound, upper_bound = rank_kernel_affine(
                nodes,
                ordered_counts,
                triples,
                weights,
                int(item["rank_bound"]),
                Q(item["outer_band"]),
            )
            if kind == "rank_kernel_lower":
                row = [-value for value in kernel_row] + [Q(0)]
                bound = -lower_bound
            else:
                row = list(kernel_row) + [Q(0)]
                bound = upper_bound
            label = f"{kind}-{item['name']}"
        elif kind == "quadratic_cut":
            block = int(item["block"])
            direction = tuple(Q(value) for value in item["direction"])
            assert 0 <= block < len(constants)
            assert len(direction) == len(constants[block])
            constant = quadratic(constants[block], direction)
            values = [
                quadratic(coefficient, direction)
                for coefficient in coefficients[block]
            ]
            # Harmonic blocks require q^T H q >= z.  The color covariance
            # block (index DEGREE+1) only requires q^T Cov q >= 0.
            margin_coefficient = (
                Q(0) if block == DEGREE + 1 else Q(1)
            )
            row = [-value for value in values] + [margin_coefficient]
            bound = constant
            label = f"quadratic-block-{block}"
        else:
            raise AssertionError(f"unknown active inequality: {kind}")
        assert len(row) == triple_variable_count + 1
        rows.append(row)
        bounds.append(bound)
        labels.append(label)
    return rows, bounds, labels, delta, rank_center


def verify(path=CERTIFICATE):
    (
        variant,
        nodes,
        ordered_counts,
        rank_band,
        rank_band_mode,
        basic,
        active_items,
    ) = load_certificate(path)
    triples = feasible_triples(nodes)
    assert triples == (
        (0, 0, 4),
        (0, 1, 4),
        (0, 2, 3),
        (0, 2, 4),
        (0, 3, 3),
        (0, 3, 4),
        (1, 1, 4),
        (1, 2, 3),
        (1, 2, 4),
        (1, 3, 3),
        (1, 3, 4),
        (2, 2, 2),
        (2, 2, 3),
        (2, 2, 4),
        (2, 3, 3),
        (2, 3, 4),
        (2, 4, 4),
        (3, 3, 3),
        (3, 3, 4),
        (3, 4, 4),
        (4, 4, 4),
    )
    assert set(basic) == set(range(len(triples))) - {6, 7, 10}

    constants, coefficients = affine_blocks(
        nodes, ordered_counts, triples
    )
    equality_rows, equality_targets = build_equalities(
        ordered_counts, triples
    )
    (
        inequality_rows,
        inequality_bounds,
        labels,
        delta,
        rank_center,
    ) = build_active_inequalities(
        nodes,
        ordered_counts,
        triples,
        constants,
        coefficients,
        rank_band,
        rank_band_mode,
        active_items,
    )

    # Primal: minimize -z, with x_t >= 0, z free, Ax <= b, Ex=f.
    objective = [Q(0)] * len(triples) + [Q(-1)]
    basis_variables = list(basic) + [len(triples)]
    unknown_count = len(inequality_rows) + len(equality_rows)
    assert len(basis_variables) == unknown_count == 19
    dual_system = []
    dual_right = []
    for variable in basis_variables:
        dual_system.append(
            [
                -row[variable] for row in inequality_rows
            ]
            + [
                row[variable] for row in equality_rows
            ]
        )
        dual_right.append(objective[variable])
    solution = solve_square(dual_system, dual_right)
    lambdas = solution[:len(inequality_rows)]
    mus = solution[len(inequality_rows):]

    # Direct exact dual audit.
    assert all(multiplier > 0 for multiplier in lambdas)
    combined = []
    for variable in range(len(objective)):
        coefficient = sum(
            -multiplier * row[variable]
            for multiplier, row in zip(lambdas, inequality_rows)
        )
        coefficient += sum(
            multiplier * row[variable]
            for multiplier, row in zip(mus, equality_rows)
        )
        combined.append(coefficient)
    assert combined[-1] == objective[-1]
    assert all(
        combined[index] == objective[index] for index in basic
    )
    nonbasic = {
        index: combined[index]
        for index in range(len(triples))
        if index not in basic
    }
    assert set(nonbasic) == {6, 7, 10}
    assert all(value < 0 for value in nonbasic.values())

    dual_lower_bound = sum(
        -multiplier * bound
        for multiplier, bound in zip(lambdas, inequality_bounds)
    ) + sum(
        multiplier * target
        for multiplier, target in zip(mus, equality_targets)
    )
    assert dual_lower_bound > 0

    # Boundary audit: the support uses <= 1/2, triangle feasibility includes
    # determinant zero, all primal counts are merely nonnegative, and the
    # dual inequalities are non-strict.  Strictness is needed only in the
    # final exact rational lower bound.
    assert max(nodes) < Q(1, 2)
    assert all(
        1
        + 2 * nodes[i] * nodes[j] * nodes[k]
        - nodes[i] ** 2
        - nodes[j] ** 2
        - nodes[k] ** 2
        >= 0
        for i, j, k in triples
    )

    return {
        "feasible_triangle_types": len(triples),
        "active_inequalities": len(inequality_rows),
        "active_labels": tuple(labels),
        "minimum_dual_multiplier": min(lambdas),
        "nonbasic_coefficients": nonbasic,
        "dual_lower_bound_for_minus_margin": dual_lower_bound,
        "dual_lower_bound_decimal": float(dual_lower_bound),
        "pair_square_excess": delta,
        "rank_center": rank_center,
        "rank_band": rank_band,
        "rank_band_mode": rank_band_mode,
        "variant": variant,
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
