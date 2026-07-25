#!/usr/bin/env python3
"""High-accuracy LP/eigenvector-cut search for quarter-grid row energy.

This is discovery code.  HiGHS handles the 32,136-row integer moment lift
as a pure sparse LP.  BV and frame PSD conditions are imposed by repeatedly
adding violated eigenvector inequalities.  The final output audits every
original PSD block and every linear residual; it is still numerical evidence,
not an exact or continuous-support certificate.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "continuous_rank_bv_search"))
import search as bv  # noqa: E402


N = 41
NODES = bv.parse_grid("quarter")
ORBITS = bv.feasible_orbits(NODES)
M = len(NODES)
BASE_VARIABLES = M + len(ORBITS)


@dataclass
class LinearRow:
    indices: np.ndarray
    values: np.ndarray
    bound: float
    name: str


def sparse_row(
    base: np.ndarray,
    bound: float,
    name: str,
    weight_values: np.ndarray | None = None,
) -> LinearRow:
    indices = np.flatnonzero(base)
    values = base[indices]
    if weight_values is not None:
        weight_indices = np.flatnonzero(weight_values)
        indices = np.r_[indices, BASE_VARIABLES + weight_indices]
        values = np.r_[values, weight_values[weight_indices]]
    return LinearRow(
        indices.astype(np.int32),
        values.astype(float),
        float(bound),
        name,
    )


def rows_to_matrix(
    rows: list[LinearRow], variable_count: int
) -> tuple[coo_matrix, np.ndarray]:
    row_indices: list[np.ndarray] = []
    column_indices: list[np.ndarray] = []
    entries: list[np.ndarray] = []
    for row_index, row in enumerate(rows):
        row_indices.append(
            np.full(len(row.indices), row_index, dtype=np.int32)
        )
        column_indices.append(row.indices)
        entries.append(row.values)
    if not rows:
        return coo_matrix((0, variable_count)), np.zeros(0)
    matrix = coo_matrix(
        (
            np.concatenate(entries),
            (
                np.concatenate(row_indices),
                np.concatenate(column_indices),
            ),
        ),
        shape=(len(rows), variable_count),
    ).tocsc()
    return matrix, np.asarray([row.bound for row in rows])


def coarse_row_array() -> np.ndarray:
    rows = []
    for deep in range(6):
        for negative in range(41 - deep):
            if deep + negative < 7:
                continue
            for central in range(41 - deep - negative):
                remainder = 40 - deep - negative - central
                for contact in range(min(15, remainder) + 1):
                    positive = remainder - contact
                    if positive + contact >= 6:
                        rows.append(
                            (deep, negative, central, positive, contact)
                        )
    answer = np.asarray(rows, dtype=np.int16)
    if len(answer) != 32136:
        raise RuntimeError(f"unexpected coarse row count {len(answer)}")
    return answer


def five_category(node: Q) -> int:
    delta = Q(1, 300)
    if node <= Q(-3, 4):
        return 0
    if node < -delta:
        return 1
    if node <= delta:
        return 2
    if node < Q(1, 2):
        return 3
    if node == Q(1, 2):
        return 4
    raise ValueError(node)


def seven_category(node: Q) -> int:
    delta = Q(1, 300)
    if node == -1:
        return 0
    if node <= Q(-3, 4):
        return 1
    if node <= Q(-1, 2):
        return 2
    if node < -delta:
        return 3
    if node <= delta:
        return 4
    if node < Q(1, 2):
        return 5
    if node == Q(1, 2):
        return 6
    raise ValueError(node)


def block_affine_arrays(
    harmonic_degree: int,
) -> list[tuple[np.ndarray, np.ndarray, np.ndarray]]:
    constants, alpha_arrays, nu_arrays = bv.coefficient_arrays(
        NODES, ORBITS, harmonic_degree
    )
    answer = []
    size = M + 1
    for degree in range(harmonic_degree + 1):
        constant = constants[degree]
        alpha = alpha_arrays[degree].reshape(size, size, M)
        nu = nu_arrays[degree].reshape(size, size, len(ORBITS))
        if degree == 0:
            answer.append(
                (
                    constant[:M, :M],
                    alpha[:M, :M, :],
                    nu[:M, :M, :],
                )
            )
        else:
            answer.append(
                (
                    constant[1:M, 1:M],
                    alpha[1:M, 1:M, :],
                    nu[1:M, 1:M, :],
                )
            )
    return answer


def scalar_affine(
    constant: np.ndarray,
    alpha: np.ndarray,
    nu: np.ndarray,
    vector: np.ndarray,
) -> tuple[float, np.ndarray]:
    value = float(vector @ constant @ vector)
    alpha_coeff = np.einsum("i,ija,j->a", vector, alpha, vector)
    nu_coeff = np.einsum("i,ijn,j->n", vector, nu, vector)
    return value, np.r_[alpha_coeff, nu_coeff]


def aggregate_affine(
    alpha: np.ndarray,
    nu: np.ndarray,
    mapping: list[int],
    left: int,
    right: int,
) -> np.ndarray:
    left_indices = [
        index for index, category in enumerate(mapping) if category == left
    ]
    right_indices = [
        index for index, category in enumerate(mapping) if category == right
    ]
    alpha_coeff = np.sum(
        alpha[np.ix_(left_indices, right_indices, range(M))],
        axis=(0, 1),
    )
    nu_coeff = np.sum(
        nu[np.ix_(left_indices, right_indices, range(len(ORBITS)))],
        axis=(0, 1),
    )
    return np.r_[alpha_coeff, nu_coeff]


def rank_affine(
    kernel: bv.Kernel,
) -> tuple[float, np.ndarray, float, np.ndarray]:
    rank = kernel.rank
    diagonal = kernel.diagonal
    values = kernel.values(NODES)
    trace_one = Q(N) * diagonal
    trace_two_constant = Q(N) * diagonal**2
    trace_two_alpha = np.asarray(
        [float(Q(N) * value**2) for value in values]
    )
    variance_constant = float(
        trace_two_constant - trace_one**2 / rank
    )
    variance = np.r_[trace_two_alpha, np.zeros(len(ORBITS))]
    trace_three_constant = Q(N) * diagonal**3
    trace_three_alpha = 3 * float(diagonal) * trace_two_alpha
    trace_three_nu = np.asarray(
        [
            float(Q(N) * values[i] * values[j] * values[k])
            for i, j, k in ORBITS
        ]
    )
    centered_constant = float(
        trace_three_constant
        - Q(3) * trace_one * trace_two_constant / rank
        + Q(2) * trace_one**3 / rank**2
    )
    centered_alpha = (
        trace_three_alpha
        - float(Q(3) * trace_one / rank) * trace_two_alpha
    )
    centered = np.r_[centered_alpha, trace_three_nu]
    return variance_constant, variance, centered_constant, centered


def add_rank_cell(
    inequalities: list[LinearRow],
    kernel: bv.Kernel,
    lower: Q,
    upper: Q,
) -> dict[str, str | int]:
    vc, v, dc, d = rank_affine(kernel)
    slope, intercept, lower_radius, upper_radius = (
        bv.rational_radius_chord(lower, upper, kernel.rank)
    )
    # lower <= vc+v.x <= upper
    inequalities.append(
        sparse_row(-v, vc - float(lower), f"{kernel.name}:V-lower")
    )
    inequalities.append(
        sparse_row(v, float(upper) - vc, f"{kernel.name}:V-upper")
    )
    # |dc+d.x| <= slope*(vc+v.x)+intercept
    inequalities.append(
        sparse_row(
            d - float(slope) * v,
            float(slope) * vc + float(intercept) - dc,
            f"{kernel.name}:D-upper",
        )
    )
    inequalities.append(
        sparse_row(
            -d - float(slope) * v,
            float(slope) * vc + float(intercept) + dc,
            f"{kernel.name}:D-lower",
        )
    )
    return {
        "kernel": kernel.name,
        "rank": kernel.rank,
        "lower": str(lower),
        "upper": str(upper),
        "slope": str(slope),
        "intercept": str(intercept),
        "lower_radius": str(lower_radius),
        "upper_radius": str(upper_radius),
    }


def frame_blocks(alpha_value: np.ndarray):
    values = np.asarray(
        [
            [float(value) for value in bv.gegenbauer_5(node, 3)]
            for node in NODES
        ]
    )
    dimensions = (1, 5, 14, 30)
    subsets = (
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
    for subset in subsets:
        rank = sum(dimensions[index] for index in subset)
        size = len(subset)
        constant = np.ones((size, size)) - N / rank
        coefficients = np.empty((size, size, M))
        for row, first in enumerate(subset):
            for column, second in enumerate(subset):
                coefficients[row, column] = (
                    values[:, first] * values[:, second]
                )
        matrix = constant + np.einsum(
            "ija,a->ij", coefficients, alpha_value
        )
        yield subset, constant, coefficients, matrix


def build_initial_model(
    harmonic_degree: int,
    pair_degree: int,
    facet_paths: tuple[Path, ...],
    use_caro_wei: bool,
    use_rank_cells: bool,
    antipode_pairs: int | None,
    custom_rank_cells: tuple[tuple[str, Q, Q], ...],
) -> tuple[
    np.ndarray,
    list[LinearRow],
    list[LinearRow],
    np.ndarray,
    list[tuple[np.ndarray, np.ndarray, np.ndarray]],
    list[dict[str, object]],
]:
    coarse_rows = coarse_row_array()
    variable_count = BASE_VARIABLES + len(coarse_rows)
    equalities: list[LinearRow] = []
    inequalities: list[LinearRow] = []

    base = np.zeros(BASE_VARIABLES)
    base[:M] = 1
    equalities.append(sparse_row(base, 40, "pair-mass"))
    base = np.zeros(BASE_VARIABLES)
    base[M:] = 1
    equalities.append(sparse_row(base, 1560, "triple-mass"))
    for index in range(M):
        base = np.zeros(BASE_VARIABLES)
        base[index] = -39
        base[M:] = np.asarray(
            [triple.count(index) / 3 for triple in ORBITS]
        )
        equalities.append(sparse_row(base, 0, f"marginal-{index}"))

    blocks = block_affine_arrays(harmonic_degree)
    _, w0_alpha, w0_nu = blocks[0]
    mapping5 = [five_category(node) for node in NODES]
    five_pairs = [
        (left, right)
        for left in range(5)
        for right in range(left, 5)
    ]
    coarse_features = np.column_stack(
        [
            coarse_rows[:, left].astype(float)
            * coarse_rows[:, right].astype(float)
            / 1600
            for left, right in five_pairs
        ]
    )
    for pair_index, (left, right) in enumerate(five_pairs):
        target = aggregate_affine(
            w0_alpha, w0_nu, mapping5, left, right
        )
        equalities.append(
            sparse_row(
                -target / 1600,
                0,
                f"coarse-moment-{left}-{right}",
                coarse_features[:, pair_index],
            )
        )
    equalities.append(
        sparse_row(
            np.zeros(BASE_VARIABLES),
            1,
            "coarse-weight-mass",
            np.ones(len(coarse_rows)),
        )
    )

    # Universal pair-mass and graph bounds.
    base = np.zeros(BASE_VARIABLES)
    base[0] = 1
    inequalities.append(sparse_row(base, 36 / 41, "antipode-pairs"))
    if antipode_pairs is not None:
        if not 0 <= antipode_pairs <= 18:
            raise ValueError("antipode-pair branch must lie in 0..18")
        equalities.append(
            sparse_row(
                base,
                Q(2 * antipode_pairs, 41),
                "fixed-antipode-pair-branch",
            )
        )
    base = np.zeros(BASE_VARIABLES)
    base[[0, 1]] = -1
    inequalities.append(sparse_row(base, -46 / 41, "deep-edge-count"))
    if antipode_pairs is not None:
        residual_independence = 20 - antipode_pairs
        # If a=20-r, the residual core has 2a+1 vertices, is
        # triangle-free, and has independence number and maximum degree
        # at most a.  The exact odd-core lemma gives e_core <= a^2+1.
        maximum_deep_edges = (
            antipode_pairs + residual_independence**2 + 1
        )
        base = np.zeros(BASE_VARIABLES)
        base[[0, 1]] = 1
        inequalities.append(
            sparse_row(
                base,
                Q(2 * maximum_deep_edges, 41),
                "branched-deep-edge-upper",
            )
        )
        maximum_core_degree = max(1, residual_independence)
        forbidden = np.asarray(
            [row[0] > maximum_core_degree for row in coarse_rows],
            dtype=float,
        )
        if np.any(forbidden):
            inequalities.append(
                sparse_row(
                    np.zeros(BASE_VARIABLES),
                    0,
                    "branched-deep-degree-upper",
                    forbidden,
                )
            )
    base = np.zeros(BASE_VARIABLES)
    base[:4] = -1
    inequalities.append(sparse_row(base, -7, "negative-tail"))
    base = np.zeros(BASE_VARIABLES)
    base[[5, 6]] = -1
    inequalities.append(sparse_row(base, -6, "positive-tail"))
    base = np.zeros(BASE_VARIABLES)
    base[[5, 6]] = 1
    inequalities.append(sparse_row(base, 23, "positive-quarter-cap"))

    # Caro--Wei on the deep graph degree distribution.
    if use_caro_wei:
        inequalities.append(
            sparse_row(
                np.zeros(BASE_VARIABLES),
                20 / 41,
                "deep-caro-wei",
                np.asarray([1 / (row[0] + 1) for row in coarse_rows]),
            )
        )

    # Ordinary two-point moments.
    pair_values = np.asarray(
        [
            [float(value) for value in bv.gegenbauer_5(node, pair_degree)]
            for node in NODES
        ]
    )
    for degree in range(1, pair_degree + 1):
        base = np.zeros(BASE_VARIABLES)
        base[:M] = -pair_values[:, degree]
        inequalities.append(
            sparse_row(base, 1, f"pair-harmonic-{degree}")
        )
        if antipode_pairs is not None and degree % 2:
            unpaired = 41 - 2 * antipode_pairs
            if degree == 1:
                upper_moment = Q(unpaired * (unpaired + 1), 2 * 41)
            else:
                upper_moment = Q(unpaired * unpaired, 41)
            base = np.zeros(BASE_VARIABLES)
            base[:M] = pair_values[:, degree]
            inequalities.append(
                sparse_row(
                    base,
                    float(upper_moment - 1),
                    f"odd-core-upper-{degree}",
                )
            )

    # Common-pair capacities.
    for row_index, row in enumerate(
        bv.stratified_capacity_rows(NODES, ORBITS)
    ):
        base = np.zeros(BASE_VARIABLES)
        base[M:] = np.asarray(row["nu_coefficients"], dtype=float)
        base[list(row["alpha_indices"])] -= 3 * row["capacity"]
        inequalities.append(
            sparse_row(base, 0, f"stratified-capacity-{row_index}")
        )
    for row_index, row in enumerate(
        bv.weighted_capacity_rows(NODES, ORBITS)
    ):
        base = np.zeros(BASE_VARIABLES)
        base[M:] = np.asarray(row["nu_coefficients"], dtype=float)
        for index, capacity in row["capacities"].items():
            base[index] -= 3 * capacity
        inequalities.append(
            sparse_row(base, 0, f"weighted-capacity-{row_index}")
        )

    # The universal five-bin facet.
    coarse_coefficients = (
        178581,
        357162,
        349742,
        4892,
        -779258,
        178581,
        349742,
        4892,
        -779258,
        176761,
        42272,
        -775478,
        3511,
        -18728,
        854161,
    )
    coarse_scale = max(abs(value) for value in coarse_coefficients)
    functional = np.zeros(BASE_VARIABLES)
    for coefficient, (left, right) in zip(
        coarse_coefficients, five_pairs, strict=True
    ):
        functional += (coefficient / coarse_scale) * aggregate_affine(
            w0_alpha, w0_nu, mapping5, left, right
        )
    inequalities.append(sparse_row(-functional, 0, "coarse-facet"))

    # Exact exhaustive seven-bin facets.
    mapping7 = [seven_category(node) for node in NODES]
    seven_pairs = [
        (left, right)
        for left in range(7)
        for right in range(left, 7)
    ]
    for path in facet_paths:
        facet = json.loads(path.read_text())
        if [tuple(pair) for pair in facet["pairs"]] != seven_pairs:
            raise ValueError(f"unexpected pair list in {path}")
        coefficients = [int(value) for value in facet["coefficients"]]
        scale = max(abs(value) for value in coefficients)
        functional = np.zeros(BASE_VARIABLES)
        for coefficient, (left, right) in zip(
            coefficients, seven_pairs, strict=True
        ):
            functional += (coefficient / scale) * aggregate_affine(
                w0_alpha, w0_nu, mapping7, left, right
            )
        inequalities.append(
            sparse_row(-functional, 0, f"facet:{path.name}")
        )

    kernels = {kernel.name: kernel for kernel in bv.default_kernels("rich")}
    rank_cells = []
    if use_rank_cells:
        specifications = custom_rank_cells or (
            ("H1", Q(2), Q(5, 2)),
            ("H0+14H2", Q(7, 5), Q(8, 5)),
        )
        rank_cells = [
            add_rank_cell(inequalities, kernels[name], lower, upper)
            for name, lower, upper in specifications
        ]

    objective = np.zeros(variable_count)
    objective[:M] = -np.asarray(
        [float(node * node) for node in NODES]
    )
    return (
        objective,
        equalities,
        inequalities,
        coarse_rows,
        blocks,
        rank_cells,
    )


def solve_with_eigen_cuts(
    harmonic_degree: int,
    pair_degree: int,
    facet_paths: tuple[Path, ...],
    maximum_iterations: int,
    use_caro_wei: bool,
    use_rank_cells: bool,
    antipode_pairs: int | None,
    custom_rank_cells: tuple[tuple[str, Q, Q], ...],
) -> dict[str, object]:
    (
        objective,
        equalities,
        inequalities,
        coarse_rows,
        blocks,
        rank_cells,
    ) = build_initial_model(
        harmonic_degree,
        pair_degree,
        facet_paths,
        use_caro_wei,
        use_rank_cells,
        antipode_pairs,
        custom_rank_cells,
    )
    variable_count = len(objective)
    cut_names: set[str] = set()
    history = []
    result = None
    converged = False

    for iteration in range(maximum_iterations):
        a_eq, b_eq = rows_to_matrix(equalities, variable_count)
        a_ub, b_ub = rows_to_matrix(inequalities, variable_count)
        result = linprog(
            objective,
            A_ub=a_ub,
            b_ub=b_ub,
            A_eq=a_eq,
            b_eq=b_eq,
            bounds=(0, None),
            method="highs",
            options={
                "dual_feasibility_tolerance": 1.0e-9,
                "primal_feasibility_tolerance": 1.0e-9,
                "ipm_optimality_tolerance": 1.0e-10,
            },
        )
        if not result.success:
            return {
                "status": "NUMERICALLY_INFEASIBLE_OR_SOLVER_FAILURE",
                "solver_message": result.message,
                "iteration": iteration,
                "history": history,
            }
        alpha = result.x[:M]
        nu = result.x[M:BASE_VARIABLES]
        new_cuts: list[LinearRow] = []
        minimum_bv = []
        for degree, (constant, alpha_coeff, nu_coeff) in enumerate(blocks):
            matrix = (
                constant
                + np.einsum("ija,a->ij", alpha_coeff, alpha)
                + np.einsum("ijn,n->ij", nu_coeff, nu)
            )
            eigenvalues, eigenvectors = np.linalg.eigh(
                (matrix + matrix.T) / 2
            )
            minimum_bv.append(float(eigenvalues[0]))
            for eigen_index, eigenvalue in enumerate(eigenvalues):
                if eigenvalue >= -1.0e-8:
                    continue
                vector = eigenvectors[:, eigen_index]
                constant_value, coefficients = scalar_affine(
                    constant, alpha_coeff, nu_coeff, vector
                )
                name = (
                    f"bv-{degree}-{iteration}-{eigen_index}-"
                    f"{hash(tuple(np.round(vector, 10)))}"
                )
                if name not in cut_names:
                    new_cuts.append(
                        sparse_row(
                            -coefficients,
                            constant_value,
                            name,
                        )
                    )
                    cut_names.add(name)

        minimum_frame = []
        for subset, constant, coefficients, matrix in frame_blocks(alpha):
            eigenvalues, eigenvectors = np.linalg.eigh(
                (matrix + matrix.T) / 2
            )
            minimum_frame.append(float(eigenvalues[0]))
            for eigen_index, eigenvalue in enumerate(eigenvalues):
                if eigenvalue >= -1.0e-8:
                    continue
                vector = eigenvectors[:, eigen_index]
                constant_value = float(vector @ constant @ vector)
                alpha_cut = np.einsum(
                    "i,ija,j->a", vector, coefficients, vector
                )
                base = np.r_[alpha_cut, np.zeros(len(ORBITS))]
                name = (
                    f"frame-{subset}-{iteration}-{eigen_index}-"
                    f"{hash(tuple(np.round(vector, 10)))}"
                )
                if name not in cut_names:
                    new_cuts.append(
                        sparse_row(-base, constant_value, name)
                    )
                    cut_names.add(name)

        equality_residual = np.max(abs(a_eq @ result.x - b_eq))
        inequality_violation = np.max(a_ub @ result.x - b_ub)
        history.append(
            {
                "iteration": iteration,
                "objective_average_row_energy": float(-result.fun),
                "new_eigenvector_cuts": len(new_cuts),
                "minimum_bv_eigenvalue": min(minimum_bv),
                "minimum_frame_eigenvalue": min(minimum_frame),
                "maximum_equality_residual": float(equality_residual),
                "maximum_linear_inequality_violation": float(
                    inequality_violation
                ),
            }
        )
        print(json.dumps(history[-1]), flush=True)
        if not new_cuts:
            converged = True
            break
        inequalities.extend(new_cuts)

    assert result is not None
    a_eq, b_eq = rows_to_matrix(equalities, variable_count)
    a_ub, b_ub = rows_to_matrix(inequalities, variable_count)
    alpha = result.x[:M]
    nu = result.x[M:BASE_VARIABLES]
    weights = result.x[BASE_VARIABLES:]
    linear_slacks = b_ub - a_ub @ result.x
    equality_residuals = a_eq @ result.x - b_eq
    rank_audit = {}
    for kernel in bv.default_kernels("rich"):
        variance, centered, residual = bv.exact_rank_values(
            kernel, NODES, ORBITS, alpha, nu
        )
        rank_audit[kernel.name] = {
            "variance": variance,
            "centered_third": centered,
            "sharp_residual": residual,
        }
    final_bv_eigenvalues = []
    for degree, (constant, alpha_coeff, nu_coeff) in enumerate(blocks):
        matrix = (
            constant
            + np.einsum("ija,a->ij", alpha_coeff, alpha)
            + np.einsum("ijn,n->ij", nu_coeff, nu)
        )
        eigenvalues = np.linalg.eigvalsh((matrix + matrix.T) / 2)
        final_bv_eigenvalues.append(
            {
                "degree": degree,
                "minimum_eigenvalue": float(eigenvalues[0]),
                "maximum_eigenvalue": float(eigenvalues[-1]),
            }
        )
    worst_linear = sorted(
        (
            {
                "name": row.name,
                "slack": float(slack),
            }
            for row, slack in zip(inequalities, linear_slacks, strict=True)
        ),
        key=lambda item: item["slack"],
    )[:20]

    return {
        "schema": "kissing5.coarse_bin_energy_lp_eigen_cut_search.v1",
        "warning": (
            "NUMERICAL EVIDENCE ONLY: finite quarter grid and floating "
            "eigenvector cuts; not an exact or continuous upper bound"
        ),
        "status": (
            "NUMERICALLY_FEASIBLE"
            if converged
            else "NUMERICALLY_NEAR_FEASIBLE_ITERATION_LIMIT"
        ),
        "solver": "SciPy HiGHS",
        "scipy_version": __import__("scipy").__version__,
        "grid": [str(node) for node in NODES],
        "harmonic_degree": harmonic_degree,
        "pair_degree": pair_degree,
        "coarse_row_types": len(coarse_rows),
        "refined_facets": [path.name for path in facet_paths],
        "rank_cells": rank_cells,
        "deep_graph_caro_wei": use_caro_wei,
        "antipode_pair_branch": antipode_pairs,
        "objective_average_row_energy": float(-result.fun),
        "target": 36 / 5,
        "alpha": alpha.tolist(),
        "nu": nu.tolist(),
        "active_coarse_rows": [
            {
                "row": coarse_rows[index].astype(int).tolist(),
                "weight": float(weight),
            }
            for index, weight in enumerate(weights)
            if weight > 1.0e-9
        ],
        "history": history,
        "final_bv_block_eigenvalues": final_bv_eigenvalues,
        "residual_audit": {
            "maximum_equality_residual": float(
                np.max(abs(equality_residuals))
            ),
            "maximum_linear_inequality_violation": float(
                max(0, -np.min(linear_slacks))
            ),
            "minimum_variable": float(np.min(result.x)),
            "minimum_linear_slack": float(np.min(linear_slacks)),
            "worst_linear_slacks": worst_linear,
        },
        "rank_sharp_audit": rank_audit,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--harmonic-degree", type=int, default=16)
    parser.add_argument("--pair-degree", type=int, default=200)
    parser.add_argument(
        "--refined-facet", action="append", type=Path, default=[]
    )
    parser.add_argument("--maximum-iterations", type=int, default=100)
    parser.add_argument("--without-caro-wei", action="store_true")
    parser.add_argument("--without-rank-cells", action="store_true")
    parser.add_argument("--antipode-pairs", type=int)
    parser.add_argument(
        "--rank-cell",
        action="append",
        default=[],
        metavar="KERNEL:LOWER:UPPER",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    custom_rank_cells = []
    for specification in args.rank_cell:
        try:
            name, lower_text, upper_text = specification.split(":")
            custom_rank_cells.append((name, Q(lower_text), Q(upper_text)))
        except (ValueError, ZeroDivisionError):
            parser.error(
                "--rank-cell must have form KERNEL:LOWER:UPPER"
            )
    result = solve_with_eigen_cuts(
        args.harmonic_degree,
        args.pair_degree,
        tuple(args.refined_facet),
        args.maximum_iterations,
        not args.without_caro_wei,
        not args.without_rank_cells,
        args.antipode_pairs,
        tuple(custom_rank_cells),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
