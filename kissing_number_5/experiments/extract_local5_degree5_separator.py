#!/usr/bin/env python3
"""Discover an exact finite-cut separator for the local5 degree-5 model.

This is discovery code.  It rationalizes every separated eigenvector,
solves the resulting finite LP numerically, and then asks SymPy's exact
simplex for a rational dual supported on the numerically active rows.
The eventual certificate verifier must check the displayed dual directly
and must not trust either solver.
"""

from fractions import Fraction as Q
from itertools import combinations_with_replacement
import json
import os

import numpy as np
from scipy.optimize import linprog
from sympy import Matrix, Rational
from sympy.solvers.simplex import InfeasibleLPError
from sympy.solvers.simplex import linprog as exact_linprog

from experiments.search_local_hybrid_degree3 import feasible_triples
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
DEGREE = 5
DIRECTION_DENOMINATOR = 100000


def rational_direction(vector):
    pivot = int(np.argmax(np.abs(vector)))
    scaled = vector / vector[pivot]
    answer = tuple(
        Q(float(value)).limit_denominator(DIRECTION_DENOMINATOR)
        for value in scaled
    )
    assert answer[pivot] == 1
    return answer


def quadratic(matrix, direction):
    return sum(
        direction[i] * matrix[i][j] * direction[j]
        for i in range(len(direction))
        for j in range(len(direction))
    )


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


def negate(row):
    return [-value for value in row]


def rank_kernel_interval_exact(
    nodes,
    ordered_counts,
    triples,
    harmonic_weights,
    rank_bound,
    rational_band,
):
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
    assert (
        rank_bound * (rank_bound - 1) * rational_band**2
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
        center - rational_band - constant_trace_three,
        center + rational_band - constant_trace_three,
    )


def build_constraints(
    nodes,
    ordered_counts,
    triples,
    constants,
    coefficients,
    cuts,
    outer_rank_model=False,
):
    variable_count = len(triples)
    incidence = [
        [Q(triple.count(edge_type)) for triple in triples] + [Q(0)]
        for edge_type in range(len(nodes))
    ]
    targets = [
        Q(39 * (count // 2)) for count in ordered_counts
    ]

    inequalities = []

    def upper(row, bound, label):
        inequalities.append((list(row), Q(bound), label))

    def lower(row, bound, label):
        inequalities.append((negate(row), -Q(bound), label))

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
        row = [
            Q(center_count(triple, deep_types)) for triple in triples
        ] + [Q(0)]
        deep_degree = sum(
            ordered_counts[index] for index in deep_types
        )
        high_edges = sum(
            ordered_counts[index] // 2 for index in high_types
        )
        lower(
            row,
            integer_wedge_minimum(deep_degree, N),
            f"threshold-{q}-lower",
        )
        upper(
            row,
            common_center_bound(q) * high_edges,
            f"threshold-{q}-upper",
        )

    mixed_01 = []
    wedge_1 = []
    for triple in triples:
        c0 = triple.count(0)
        c1 = triple.count(1)
        mixed_01.append(Q(c0 * c1))
        wedge_1.append(Q(c1 * (c1 - 1) // 2))
    upper(
        [
            mixed + 2 * wedge
            for mixed, wedge in zip(mixed_01, wedge_1)
        ] + [Q(0)],
        24,
        "colored-clique",
    )
    upper(wedge_1 + [Q(0)], 3, "color-1-wedges")

    pair_square = sum(
        Q(count, N) * node**2
        for count, node in zip(ordered_counts, nodes)
    )
    delta = pair_square - Q(36, 5)
    rank_center = Q(1116, 25) + Q(108, 5) * delta
    rank_band = Q(3, 100) if outer_rank_model else Q(29, 1000)
    if outer_rank_model:
        assert 20 * rank_band**2 > 369 * delta**3
    else:
        assert 20 * rank_band**2 < 369 * delta**3
    cycle = [
        Q(6, N) * nodes[i] * nodes[j] * nodes[k]
        for i, j, k in triples
    ] + [Q(0)]
    lower(cycle, rank_center - rank_band, "C047-lower")
    upper(cycle, rank_center + rank_band, "C047-upper")
    if outer_rank_model:
        for label, kernel_data in (
            (
                "rank-kernel-H01",
                rank_kernel_interval_exact(
                    nodes,
                    ordered_counts,
                    triples,
                    {0: Q(1, 6), 1: Q(5, 6)},
                    6,
                    Q(7, 2),
                ),
            ),
            (
                "rank-kernel-H2",
                rank_kernel_interval_exact(
                    nodes,
                    ordered_counts,
                    triples,
                    {2: Q(1)},
                    14,
                    Q(157, 50),
                ),
            ),
        ):
            row, row_lower, row_upper = kernel_data
            lower(row + [Q(0)], row_lower, f"{label}-lower")
            upper(row + [Q(0)], row_upper, f"{label}-upper")

    for cut_index, (block, direction) in enumerate(cuts):
        constant = quadratic(constants[block], direction)
        values = [
            quadratic(coefficient, direction)
            for coefficient in coefficients[block]
        ]
        margin = Q(0) if block == DEGREE + 1 else Q(1)
        # constant + values*x - margin*z >= 0.
        upper(
            [-value for value in values] + [margin],
            constant,
            f"cut-{cut_index}-block-{block}",
        )

    return incidence, targets, inequalities


def to_float(rows):
    return np.array(
        [[float(value) for value in row] for row in rows],
        dtype=float,
    )


def to_sympy(rows):
    return Matrix(
        [
            [Rational(value.numerator, value.denominator) for value in row]
            for row in rows
        ]
    )


def exact_dual(
    objective,
    equality_rows,
    equality_rhs,
    inequality_rows,
    inequality_rhs,
    active,
):
    # Primal is min c*x with A*x<=b, E*x=f, x_0,...,x_20>=0,
    # and z free.  Put dual inequality multipliers y=-lambda with
    # lambda>=0.  The five equality multipliers mu remain free.
    #
    # -A^T lambda + E^T mu <= c on nonnegative variables,
    # equality on free z.  Minimize the negative dual objective.
    active_rows = [inequality_rows[index] for index in active]
    active_rhs = [inequality_rhs[index] for index in active]
    dual_variable_count = len(active) + len(equality_rows)
    dual_objective = (
        active_rhs
        + [-value for value in equality_rhs]
    )
    dual_inequalities = []
    dual_bounds = []
    for variable in range(len(objective) - 1):
        row = (
            [-active_row[variable] for active_row in active_rows]
            + [
                equality_rows[index][variable]
                for index in range(len(equality_rows))
            ]
        )
        dual_inequalities.append(row)
        dual_bounds.append(objective[variable])
    dual_equalities = [[
        -active_row[-1] for active_row in active_rows
    ] + [
        equality_rows[index][-1] for index in range(len(equality_rows))
    ]]
    dual_equality_rhs = [objective[-1]]
    bounds = (
        [(Q(0), None)] * len(active)
        + [(None, None)] * len(equality_rows)
    )
    value, solution = exact_linprog(
        [Rational(x.numerator, x.denominator) for x in dual_objective],
        to_sympy(dual_inequalities),
        to_sympy([[value] for value in dual_bounds]),
        to_sympy(dual_equalities),
        to_sympy([[value] for value in dual_equality_rhs]),
        bounds=[
            (
                None if lower is None else Rational(
                    lower.numerator, lower.denominator
                ),
                None if upper is None else Rational(
                    upper.numerator, upper.denominator
                ),
            )
            for lower, upper in bounds
        ],
    )
    # exact_linprog minimized b*lambda-f*mu, the negative dual value.
    def as_fraction(item):
        if hasattr(item, "as_numer_denom"):
            numerator, denominator = item.as_numer_denom()
            return Q(int(numerator), int(denominator))
        return Q(int(item))

    fractions = [as_fraction(item) for item in solution]
    return -as_fraction(value), fractions


def main():
    size, nodes, ordered_counts, _, _ = load_certificate()
    assert size == N
    triples = feasible_triples(nodes)
    constants, coefficients = affine_blocks(
        nodes, ordered_counts, triples
    )
    cuts = []
    outer_rank_model = bool(os.environ.get("OUTER_RANK_MODEL"))
    print(
        "rank model:",
        "necessary outer C047 + harmonic-rank intervals"
        if outer_rank_model
        else "historical inner C047 band",
        flush=True,
    )
    for block, constant in enumerate(constants):
        for index in range(len(constant)):
            direction = tuple(
                Q(int(position == index))
                for position in range(len(constant))
            )
            cuts.append((block, direction))

    objective = [Q(0)] * len(triples) + [Q(-1)]
    final = None
    for round_index in range(80):
        equality_rows, equality_rhs, inequalities = build_constraints(
            nodes,
            ordered_counts,
            triples,
            constants,
            coefficients,
            cuts,
            outer_rank_model,
        )
        inequality_rows = [item[0] for item in inequalities]
        inequality_rhs = [item[1] for item in inequalities]
        result = linprog(
            [float(value) for value in objective],
            A_ub=to_float(inequality_rows),
            b_ub=np.array(
                [float(value) for value in inequality_rhs]
            ),
            A_eq=to_float(equality_rows),
            b_eq=np.array(
                [float(value) for value in equality_rhs]
            ),
            bounds=[(0, None)] * len(triples) + [(None, None)],
            method="highs",
        )
        assert result.success, result.message
        values = result.x[:-1]
        margin = result.x[-1]
        print(
            f"round={round_index} cuts={len(cuts)} margin={margin:.12g}",
            flush=True,
        )

        if margin < -1e-5:
            final = (
                result,
                equality_rows,
                equality_rhs,
                inequality_rows,
                inequality_rhs,
                inequalities,
            )
            break

        new_cuts = []
        for block in range(len(constants)):
            matrix = np.array(constants[block], dtype=float)
            for value, coefficient in zip(values, coefficients[block]):
                matrix += value * np.array(coefficient, dtype=float)
            eigenvalues, eigenvectors = np.linalg.eigh(matrix)
            target = 0 if block == DEGREE + 1 else margin
            if eigenvalues[0] < target - 1e-8:
                direction = rational_direction(eigenvectors[:, 0])
                candidate = block, direction
                if candidate not in cuts and candidate not in new_cuts:
                    new_cuts.append(candidate)
        if not new_cuts:
            raise RuntimeError(
                "separation stalled before a negative finite-cut optimum"
            )
        cuts.extend(new_cuts)
    assert final is not None

    (
        result,
        equality_rows,
        equality_rhs,
        inequality_rows,
        inequality_rhs,
        inequalities,
    ) = final
    for method in ("highs-ds", "highs-ipm"):
        alternate = linprog(
            [float(value) for value in objective],
            A_ub=to_float(inequality_rows),
            b_ub=np.array([float(value) for value in inequality_rhs]),
            A_eq=to_float(equality_rows),
            b_eq=np.array([float(value) for value in equality_rhs]),
            bounds=[(0, None)] * len(triples) + [(None, None)],
            method=method,
            options={"presolve": False},
        )
        print(
            f"{method} success={alternate.success} "
            f"margin={None if alternate.x is None else alternate.x[-1]}",
            flush=True,
        )
    numerical_dual_value = sum(
        marginal * float(bound)
        for marginal, bound in zip(
            result.ineqlin.marginals, inequality_rhs
        )
    ) + sum(
        marginal * float(bound)
        for marginal, bound in zip(
            result.eqlin.marginals, equality_rhs
        )
    )
    print(
        f"numerical primal min={result.fun} "
        f"numerical dual={numerical_dual_value}",
        flush=True,
    )
    numerical_lambda_check = -result.ineqlin.marginals
    numerical_mu_check = result.eqlin.marginals
    combined_check = (
        -to_float(inequality_rows).T @ numerical_lambda_check
        + to_float(equality_rows).T @ numerical_mu_check
    )
    print(
        "numerical dual coefficient residuals",
        combined_check[:-1].max(),
        combined_check[:-1].min(),
        "z",
        combined_check[-1],
        flush=True,
    )
    if os.environ.get("NUMERIC_DUAL_ONLY"):
        basis_active = [
            index
            for index, value in enumerate(numerical_lambda_check)
            if value > 1e-12
        ]
        basis_variables = [
            index
            for index, value in enumerate(result.x[:-1])
            if value > 1e-9
        ] + [len(objective) - 1]
        basis_matrix = []
        for variable in basis_variables:
            basis_matrix.append(
                [
                    -inequality_rows[row][variable]
                    for row in basis_active
                ]
                + [
                    equality_rows[row][variable]
                    for row in range(len(equality_rows))
                ]
            )
        basis_rhs = [objective[index] for index in basis_variables]
        exact_basis_solution = to_sympy(basis_matrix).inv() * to_sympy(
            [[value] for value in basis_rhs]
        )

        def sympy_fraction(value):
            numerator, denominator = value.as_numer_denom()
            return Q(int(numerator), int(denominator))

        exact_basis = [
            sympy_fraction(value) for value in exact_basis_solution
        ]
        basis_lambdas = exact_basis[:len(basis_active)]
        basis_mus = exact_basis[len(basis_active):]
        basis_combined = []
        for variable in range(len(objective)):
            value = sum(
                -multiplier * inequality_rows[row][variable]
                for row, multiplier in zip(
                    basis_active, basis_lambdas
                )
            )
            value += sum(
                multiplier * equality_rows[row][variable]
                for row, multiplier in enumerate(basis_mus)
            )
            basis_combined.append(value)
        basis_dual_value = sum(
            -multiplier * inequality_rhs[row]
            for row, multiplier in zip(basis_active, basis_lambdas)
        ) + sum(
            multiplier * equality_rhs[row]
            for row, multiplier in enumerate(basis_mus)
        )
        print(
            "exact basis diagnostic",
            {
                "minimum_lambda": str(min(basis_lambdas)),
                "dual_value": str(basis_dual_value),
                "maximum_nonbasic_coefficient": str(
                    max(
                        basis_combined[index]
                        for index in range(len(objective) - 1)
                        if index not in basis_variables
                    )
                ),
                "z_coefficient": str(basis_combined[-1]),
            },
            flush=True,
        )
        print(
            json.dumps(
                {
                    "exact_basis_certificate": {
                        "active_rows": [
                            {
                                "label": inequalities[row][2],
                                "multiplier": str(multiplier),
                                **(
                                    {
                                        "block": cuts[
                                            int(
                                                inequalities[row][2]
                                                .split("-")[1]
                                            )
                                        ][0],
                                        "direction": [
                                            str(value)
                                            for value in cuts[
                                                int(
                                                    inequalities[row][2]
                                                    .split("-")[1]
                                                )
                                            ][1]
                                        ],
                                    }
                                    if inequalities[row][2].startswith(
                                        "cut-"
                                    )
                                    else {}
                                ),
                            }
                            for row, multiplier in zip(
                                basis_active, basis_lambdas
                            )
                        ],
                        "equality_multipliers": [
                            str(value) for value in basis_mus
                        ],
                        "dual_value": str(basis_dual_value),
                        "nonbasic_coefficients": {
                            str(index): str(basis_combined[index])
                            for index in range(len(objective) - 1)
                            if index not in basis_variables
                        },
                    },
                    "positive_primal_variables": [
                        [index, float(value)]
                        for index, value in enumerate(result.x)
                        if value > 1e-9
                    ],
                    "dual_support": [
                        {
                            "index": index,
                            "label": inequalities[index][2],
                            "lambda": float(value),
                            "slack": float(result.ineqlin.residual[index]),
                        }
                        for index, value in enumerate(
                            numerical_lambda_check
                        )
                        if value > 1e-12
                    ],
                    "equality_multipliers": [
                        float(value) for value in numerical_mu_check
                    ],
                    "combined_coefficients": [
                        float(value) for value in combined_check
                    ],
                },
                indent=2,
            )
        )
        return
    numerical_lambda = -result.ineqlin.marginals
    candidate_active_sets = []
    for dual_threshold, slack_threshold in (
        (1e-9, 1e-9),
        (1e-11, 1e-7),
        (1e-13, 1e-5),
        (0, 1e-3),
    ):
        candidate_active_sets.append(
            [
                index
                for index, (dual, slack) in enumerate(
                    zip(numerical_lambda, result.ineqlin.residual)
                )
                if dual > dual_threshold or slack < slack_threshold
            ]
        )
    candidate_active_sets.append(list(range(len(inequality_rows))))
    exact = None
    for attempt, active in enumerate(candidate_active_sets):
        print(
            f"trying exact dual with {len(active)} rows "
            f"on attempt {attempt}",
            flush=True,
        )
        try:
            dual_value, dual_solution = exact_dual(
                objective,
                equality_rows,
                equality_rhs,
                inequality_rows,
                inequality_rhs,
                active,
            )
        except InfeasibleLPError:
            continue
        exact = active, dual_value, dual_solution
        break
    if exact is None:
        raise RuntimeError("could not recover an exact active-row dual")

    active, dual_value, dual_solution = exact
    lambdas = dual_solution[:len(active)]
    mus = dual_solution[len(active):]
    print(f"exact dual value={dual_value}", flush=True)
    assert dual_value > 0

    # Direct exact dual verification.
    for value in lambdas:
        assert value >= 0
    combined = []
    for variable in range(len(objective)):
        value = sum(
            -multiplier * inequality_rows[row][variable]
            for row, multiplier in zip(active, lambdas)
        )
        value += sum(
            multiplier * equality_rows[row][variable]
            for row, multiplier in enumerate(mus)
        )
        combined.append(value)
    assert all(
        combined[index] <= objective[index]
        for index in range(len(triples))
    )
    assert combined[-1] == objective[-1]
    checked_value = sum(
        -multiplier * inequality_rhs[row]
        for row, multiplier in zip(active, lambdas)
    ) + sum(
        multiplier * equality_rhs[row]
        for row, multiplier in enumerate(mus)
    )
    assert checked_value == dual_value

    payload = {
        "degree": DEGREE,
        "direction_denominator_limit": DIRECTION_DENOMINATOR,
        "triples": [list(triple) for triple in triples],
        "cuts": [
            {
                "block": block,
                "direction": [str(value) for value in direction],
            }
            for block, direction in cuts
        ],
        "active_inequalities": [
            {
                "index": row,
                "label": inequalities[row][2],
                "multiplier": str(multiplier),
            }
            for row, multiplier in zip(active, lambdas)
            if multiplier
        ],
        "equality_multipliers": [str(value) for value in mus],
        "dual_lower_bound_for_minus_margin": str(dual_value),
        "numerical_margin": float(result.x[-1]),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
