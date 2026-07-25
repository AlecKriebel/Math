#!/usr/bin/env python3
"""Discovery SDP for the average row energy with a universal coarse-bin cut.

The finite node grid and floating-point solver make every result from this
script numerical evidence only.  A useful dual must later be reconstructed
exactly and verified on every continuous semialgebraic bin cell.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
import sys

import cvxpy as cp
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "continuous_rank_bv_search"))
import search as bv  # noqa: E402


N = 41

# Coefficients are in lexicographic order (a,b), 0 <= a <= b < 5.
COARSE_COEFFICIENTS = (
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


def category(node: Q) -> int:
    """The five boundary-safe categories used by the integer-row lemma."""

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
    raise ValueError(f"node outside kissing range: {node}")


def refined_category(node: Q) -> int:
    """Seven-bin refinement with additional universal cumulative caps."""

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
    raise ValueError(f"node outside kissing range: {node}")


def coarse_row_types() -> tuple[tuple[int, ...], ...]:
    """All integer five-bin rows allowed by the proved local bounds."""

    rows = []
    for a in range(6):
        for b in range(41 - a):
            if a + b < 7:
                continue
            for c in range(41 - a - b):
                remainder = 40 - a - b - c
                for e in range(min(15, remainder) + 1):
                    d = remainder - e
                    if d + e >= 6:
                        rows.append((a, b, c, d, e))
    assert len(rows) == 32136
    return tuple(rows)


def solve(
    nodes: tuple[Q, ...],
    harmonic_degree: int,
    pair_degree: int,
    use_capacities: bool,
    use_coarse_lift: bool,
    use_rank_bands: bool,
    h1_variance_interval: tuple[Q, Q] | None,
    refined_facet_paths: tuple[Path, ...],
    rank_cells: tuple[tuple[str, Q, Q], ...],
    antipode_pairs: int | None,
    requested_solver: str,
) -> dict[str, object]:
    orbits = bv.feasible_orbits(nodes)
    m = len(nodes)
    alpha = cp.Variable(m, nonneg=True, name="alpha")
    nu = cp.Variable(len(orbits), nonneg=True, name="nu")
    constraints: list[cp.Constraint] = [
        cp.sum(alpha) == N - 1,
        cp.sum(nu) == (N - 1) * (N - 2),
    ]
    antipode_index = nodes.index(Q(-1))
    deep_indices = [
        index for index, node in enumerate(nodes) if node < Q(-1, 2)
    ]
    # A 41-code has at most 18 antipodal pairs.  Its graph of pairs with
    # inner product below -1/2 is triangle-free with independence number at
    # most 20, and hence has at least 23 edges.
    constraints.extend(
        (
            alpha[antipode_index] <= Q(36, 41),
            cp.sum(alpha[deep_indices]) >= Q(46, 41),
        )
    )
    if antipode_pairs is not None:
        if not 0 <= antipode_pairs <= 18:
            raise ValueError("antipode-pair branch must lie in 0..18")
        residual_independence = 20 - antipode_pairs
        maximum_deep_edges = (
            antipode_pairs + residual_independence**2 + 1
        )
        constraints.extend(
            (
                alpha[antipode_index] == Q(2 * antipode_pairs, 41),
                cp.sum(alpha[deep_indices])
                <= Q(2 * maximum_deep_edges, 41),
            )
        )

    delta = Q(1, 300)
    negative = [i for i, node in enumerate(nodes) if node < -delta]
    positive = [i for i, node in enumerate(nodes) if node > delta]
    constraints.extend(
        (
            cp.sum(alpha[negative]) >= 7,
            cp.sum(alpha[positive]) >= 6,
            cp.sum(alpha[positive]) <= 23,
        )
    )
    for index in range(m):
        multiplicities = np.asarray(
            [triple.count(index) / 3 for triple in orbits],
            dtype=float,
        )
        constraints.append(multiplicities @ nu == (N - 2) * alpha[index])

    constants, alpha_arrays, nu_arrays = bv.coefficient_arrays(
        nodes, orbits, harmonic_degree
    )
    blocks = []
    degree_zero_active = None
    for degree in range(harmonic_degree + 1):
        size = m + 1
        expression = constants[degree] + cp.reshape(
            alpha_arrays[degree] @ alpha + nu_arrays[degree] @ nu,
            (size, size),
            order="C",
        )
        active = (
            expression[:m, :m]
            if degree == 0
            else expression[1:m, 1:m]
        )
        constraints.append(active >> 0)
        blocks.append(active)
        if degree == 0:
            degree_zero_active = active

    assert degree_zero_active is not None
    category_indices = [
        [index for index, node in enumerate(nodes) if category(node) == cat]
        for cat in range(5)
    ]
    pairs = [(i, j) for i in range(5) for j in range(i, 5)]
    coarse_expression = 0
    coarse_scale = max(abs(value) for value in COARSE_COEFFICIENTS)
    for coefficient, (left, right) in zip(
        COARSE_COEFFICIENTS, pairs, strict=True
    ):
        coarse_expression += (coefficient / coarse_scale) * cp.sum(
            degree_zero_active[
                np.ix_(category_indices[left], category_indices[right])
            ]
        )
    # Coefficients were already divided by ``coarse_scale`` above.
    constraints.append(coarse_expression >= 0)
    refined_category_indices = [
        [
            index
            for index, node in enumerate(nodes)
            if refined_category(node) == cat
        ]
        for cat in range(7)
    ]
    refined_facet_expressions = []
    expected_refined_pairs = [
        (left, right)
        for left in range(7)
        for right in range(left, 7)
    ]
    for facet_path in refined_facet_paths:
        facet = json.loads(facet_path.read_text())
        if facet["schema"] not in {
            "kissing5.refined_seven_bin_row_facet_discovery.v1",
            "kissing5.refined_seven_bin_row_facet_discovery.v2",
        }:
            raise ValueError(f"unexpected facet schema in {facet_path}")
        facet_pairs = [tuple(pair) for pair in facet["pairs"]]
        if facet_pairs != expected_refined_pairs:
            raise ValueError(f"unexpected pair order in {facet_path}")
        coefficients = [int(value) for value in facet["coefficients"]]
        coefficient_scale = max(abs(value) for value in coefficients)
        expression = 0
        for coefficient, (left, right) in zip(
            coefficients, facet_pairs, strict=True
        ):
            expression += (coefficient / coefficient_scale) * cp.sum(
                degree_zero_active[
                    np.ix_(
                        refined_category_indices[left],
                        refined_category_indices[right],
                    )
                ]
            )
        # Coefficients were already divided by ``coefficient_scale`` above.
        constraints.append(expression >= 0)
        refined_facet_expressions.append((facet_path.name, expression))
    coarse_weights = None
    caro_wei_expression = None
    row_types: tuple[tuple[int, ...], ...] = ()
    if use_coarse_lift:
        row_types = coarse_row_types()
        degree_array = np.asarray(row_types, dtype=float)
        coarse_weights = cp.Variable(
            len(row_types), nonneg=True, name="coarse_row_weights"
        )
        constraints.append(cp.sum(coarse_weights) == 1)
        if antipode_pairs is not None:
            maximum_core_degree = max(1, 20 - antipode_pairs)
            forbidden = [
                index
                for index, row in enumerate(row_types)
                if row[0] > maximum_core_degree
            ]
            if forbidden:
                constraints.append(cp.sum(coarse_weights[forbidden]) == 0)
        # On the quarter grid, coarse category A is exactly the graph of
        # inner products below -1/2.  Its independence number is at most
        # 20.  Caro--Wei gives alpha(G) >= sum_v 1/(d_v+1), so the uniform
        # row distribution must satisfy the following exact linear bound.
        caro_wei_expression = cp.sum(
            cp.multiply(
                np.asarray(
                    [1 / (row[0] + 1) for row in row_types],
                    dtype=float,
                ),
                coarse_weights,
            )
        )
        constraints.append(caro_wei_expression <= Q(20, 41))
        for left in range(5):
            for right in range(left, 5):
                target = cp.sum(
                    degree_zero_active[
                        np.ix_(
                            category_indices[left],
                            category_indices[right],
                        )
                    ]
                )
                constraints.append(
                    (
                        degree_array[:, left] * degree_array[:, right]
                    )
                    @ coarse_weights
                    / 1600
                    == target / 1600
                )

    pair_values = np.asarray(
        [
            [
                float(value)
                for value in bv.gegenbauer_5(node, pair_degree)
            ]
            for node in nodes
        ]
    )
    for degree in range(1, pair_degree + 1):
        constraints.append(1 + pair_values[:, degree] @ alpha >= 0)
        if antipode_pairs is not None and degree % 2:
            unpaired = 41 - 2 * antipode_pairs
            if degree == 1:
                upper_moment = Q(unpaired * (unpaired + 1), 2 * 41)
            else:
                upper_moment = Q(unpaired * unpaired, 41)
            constraints.append(
                1 + pair_values[:, degree] @ alpha
                <= float(upper_moment)
            )
    constraints.extend(bv.pair_frame_constraints(nodes, alpha))
    rank_band_count = 0
    if use_rank_bands:
        for kernel in bv.default_kernels("rich"):
            variance, centered_third, _ = bv.rank_traces(
                kernel, nodes, orbits, alpha, nu
            )
            upper = bv.safe_variance_upper(kernel, nodes)
            slope = bv.global_secant_slope(upper, kernel.rank)
            constraints.extend(
                (
                    variance >= 0,
                    variance <= float(upper),
                    centered_third <= float(slope) * variance,
                    centered_third >= -float(slope) * variance,
                )
            )
            rank_band_count += 1
    h1_chord_record = None
    if h1_variance_interval is not None:
        lower, upper = h1_variance_interval
        h1 = bv.Kernel("H1", ((1, Q(1)),))
        variance, centered_third, _ = bv.rank_traces(
            h1, nodes, orbits, alpha, nu
        )
        slope, intercept, lower_radius, upper_radius = (
            bv.rational_radius_chord(lower, upper, h1.rank)
        )
        constraints.extend(
            (
                variance >= float(lower),
                variance <= float(upper),
                centered_third
                <= float(slope) * variance + float(intercept),
                centered_third
                >= -float(slope) * variance - float(intercept),
            )
        )
        h1_chord_record = {
            "variance_lower": str(lower),
            "variance_upper": str(upper),
            "slope": str(slope),
            "intercept": str(intercept),
            "lower_radius": str(lower_radius),
            "upper_radius": str(upper_radius),
        }
    rank_cell_records = []
    kernels_by_name = {
        kernel.name: kernel for kernel in bv.default_kernels("rich")
    }
    for kernel_name, lower, upper in rank_cells:
        if kernel_name not in kernels_by_name:
            raise ValueError(f"unknown rank-cell kernel {kernel_name!r}")
        if not 0 <= lower < upper:
            raise ValueError(f"invalid rank cell [{lower},{upper}]")
        kernel = kernels_by_name[kernel_name]
        variance, centered_third, _ = bv.rank_traces(
            kernel, nodes, orbits, alpha, nu
        )
        slope, intercept, lower_radius, upper_radius = (
            bv.rational_radius_chord(lower, upper, kernel.rank)
        )
        constraints.extend(
            (
                variance >= float(lower),
                variance <= float(upper),
                centered_third
                <= float(slope) * variance + float(intercept),
                centered_third
                >= -float(slope) * variance - float(intercept),
            )
        )
        rank_cell_records.append(
            {
                "kernel": kernel_name,
                "rank": kernel.rank,
                "variance_lower": str(lower),
                "variance_upper": str(upper),
                "slope": str(slope),
                "intercept": str(intercept),
                "lower_radius": str(lower_radius),
                "upper_radius": str(upper_radius),
            }
        )

    capacity_count = 0
    if use_capacities:
        for row in bv.stratified_capacity_rows(nodes, orbits):
            left = np.asarray(row["nu_coefficients"], dtype=float) @ nu
            right = 3 * row["capacity"] * cp.sum(
                alpha[list(row["alpha_indices"])]
            )
            constraints.append(left <= right)
            capacity_count += 1
        for row in bv.weighted_capacity_rows(nodes, orbits):
            left = np.asarray(row["nu_coefficients"], dtype=float) @ nu
            right = 3 * sum(
                capacity * alpha[index]
                for index, capacity in row["capacities"].items()
            )
            constraints.append(left <= right)
            capacity_count += 1

    energy = np.asarray([float(node * node) for node in nodes]) @ alpha
    problem = cp.Problem(cp.Maximize(energy), constraints)
    solver_used = requested_solver
    try:
        if solver_used == "SCS":
            value = problem.solve(
                solver=solver_used,
                eps=2.0e-7,
                max_iters=500_000,
                acceleration_lookback=20,
                verbose=False,
            )
        else:
            value = problem.solve(
                solver=solver_used,
                max_iter=5000,
                tol_gap_abs=1.0e-10,
                tol_gap_rel=1.0e-10,
                tol_feas=1.0e-10,
                verbose=False,
            )
    except cp.error.SolverError:
        if requested_solver != "CLARABEL":
            raise
        # This is discovery code.  Dense collections of nearly parallel
        # exact row facets occasionally defeat Clarabel's numerical
        # equilibration, so retain a clearly recorded SCS fallback.
        solver_used = "SCS"
        value = problem.solve(
            solver=solver_used,
            eps=2.0e-7,
            max_iters=500_000,
            acceleration_lookback=20,
            verbose=False,
        )
    record: dict[str, object] = {
        "schema": "kissing5.coarse_bin_average_energy_search.v1",
        "warning": (
            "NUMERICAL DISCOVERY ONLY: finite atomic support and "
            "floating-point conic solve"
        ),
        "solver": solver_used,
        "grid": [str(node) for node in nodes],
        "harmonic_degree": harmonic_degree,
        "pair_degree": pair_degree,
        "capacity_rows": capacity_count,
        "coarse_integer_lift": use_coarse_lift,
        "coarse_row_type_count": len(row_types),
        "rank_outer_band_count": rank_band_count,
        "h1_variance_chord": h1_chord_record,
        "additional_rank_variance_chords": rank_cell_records,
        "refined_seven_bin_facets": [
            path.name for path in refined_facet_paths
        ],
        "status": problem.status,
        "objective_average_row_energy": (
            None if value is None else float(value)
        ),
        "target": 36 / 5,
        "antipode_pair_branch": antipode_pairs,
    }
    if alpha.value is not None and nu.value is not None:
        record["coarse_cut_value"] = float(coarse_expression.value)
        record["alpha"] = [float(value) for value in alpha.value]
        record["nu"] = [float(value) for value in nu.value]
        record["minimum_bv_eigenvalues"] = [
            float(np.linalg.eigvalsh(np.asarray(block.value))[0])
            for block in blocks
        ]
        record["minimum_pair_moment"] = float(
            min(
                1 + pair_values[:, degree] @ alpha.value
                for degree in range(1, pair_degree + 1)
            )
        )
        record["refined_seven_bin_facet_values"] = {
            name: float(expression.value)
            for name, expression in refined_facet_expressions
        }
        record["deep_graph_caro_wei_average"] = (
            None
            if caro_wei_expression is None
            else float(caro_wei_expression.value)
        )
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--grid",
        choices=("quarter", "eighth", "sixteenth"),
        default="quarter",
    )
    parser.add_argument("--harmonic-degree", type=int, default=16)
    parser.add_argument("--pair-degree", type=int, default=120)
    parser.add_argument("--without-capacities", action="store_true")
    parser.add_argument("--coarse-lift", action="store_true")
    parser.add_argument("--rank-bands", action="store_true")
    parser.add_argument("--h1-variance-lower", type=Q)
    parser.add_argument("--h1-variance-upper", type=Q)
    parser.add_argument(
        "--refined-facet",
        action="append",
        type=Path,
        default=[],
        help="exact seven-bin facet JSON; may be repeated",
    )
    parser.add_argument(
        "--rank-cell",
        action="append",
        default=[],
        metavar="KERNEL:LOWER:UPPER",
        help="additional exact outer chord for one kernel variance cell",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--antipode-pairs", type=int)
    parser.add_argument(
        "--solver", choices=("CLARABEL", "SCS"), default="CLARABEL"
    )
    args = parser.parse_args()
    interval = None
    if (
        args.h1_variance_lower is not None
        or args.h1_variance_upper is not None
    ):
        if (
            args.h1_variance_lower is None
            or args.h1_variance_upper is None
        ):
            parser.error("both H1 variance endpoints are required")
        interval = (args.h1_variance_lower, args.h1_variance_upper)
    rank_cells = []
    for specification in args.rank_cell:
        try:
            name, lower_text, upper_text = specification.split(":")
            rank_cells.append((name, Q(lower_text), Q(upper_text)))
        except (ValueError, ZeroDivisionError):
            parser.error(
                "--rank-cell must have form KERNEL:LOWER:UPPER"
            )
    result = solve(
        bv.parse_grid(args.grid),
        args.harmonic_degree,
        args.pair_degree,
        not args.without_capacities,
        args.coarse_lift,
        args.rank_bands,
        interval,
        tuple(args.refined_facet),
        tuple(rank_cells),
        args.antipode_pairs,
        args.solver,
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
