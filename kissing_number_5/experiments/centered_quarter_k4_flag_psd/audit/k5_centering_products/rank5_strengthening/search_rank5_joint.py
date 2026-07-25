#!/usr/bin/env python3
"""Rank-strengthened joint quarter-grid K2/K3/K4 ordered-flag search."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
import math
from pathlib import Path

import cvxpy as cp
import numpy as np

from experiments.centered_quarter_k4_flag_psd.audit.search_full_centering import (
    coefficients,
)
from experiments.centered_global_count_milp.search_degree_lift import (
    degree_types,
)
from experiments.continuous_rank_bv_search.search import (
    coefficient_arrays,
    default_kernels,
    gegenbauer_5,
    global_secant_slope,
    pair_frame_constraints,
    rational_radius_chord,
    rank_traces,
    safe_variance_upper,
    stratified_capacity_rows,
    weighted_capacity_rows,
)


# Exact inequalities valid on the complete 9,882-row catalogue.  They are
# redundant with the row-weight lift but materially improve conditioning near
# faces of its moment cone.  A tuple is (feature coefficients, exact bound),
# where the 36 unnormalized features are
#   1, d_0,...,d_6, d_0^2,d_0d_1,...,d_6^2
# in upper-triangular lexicographic order.
ROW_CONE_MOMENT_CUTS = (
    (
        {
            5: 8125,
            4: 7929,
            3: -1465,
            30: -308,
            33: -79,
            26: -248,
            28: -144,
            27: -514,
            31: -290,
            21: 32,
            24: 287,
            23: 30,
            2: 10000,
            22: -61,
            18: 22,
            20: -876,
        },
        45024,
    ),
    (
        {
            5: 92540,
            6: 5301,
            4: 89207,
            3: -8895,
            30: -3351,
            33: -843,
            26: -2702,
            28: -1670,
            27: -5644,
            31: -3158,
            21: 253,
            24: 2725,
            2: 100000,
            22: -845,
            18: 175,
            20: -8704,
        },
        563867,
    ),
)


def quotient_keep_indices(kernel_vectors: np.ndarray) -> list[int]:
    """Rows retained after deleting pivots for known exact kernels."""

    matrix = np.asarray(kernel_vectors, dtype=float).T
    rank = int(np.linalg.matrix_rank(matrix))
    pivots: list[int] = []
    for row in range(matrix.shape[0]):
        candidate = pivots + [row]
        if np.linalg.matrix_rank(matrix[candidate, :]) > len(pivots):
            pivots.append(row)
        if len(pivots) == rank:
            break
    assert len(pivots) == rank
    return [row for row in range(matrix.shape[0]) if row not in pivots]


def solve(
    profile: str,
    solver: str = "CLARABEL",
    spectral_x: int | None = None,
    seek_interior: bool = False,
    spectral_d: Q | None = None,
    interior_psd_floor: float = 5e-7,
    interior_row_floor: float = 5e-8,
    interior_k4_floor: float = 5e-9,
    maximize_interior_floor: bool = False,
    h2_lower: Q | None = None,
    h2_upper: Q | None = None,
) -> dict:
    root = Path(__file__).resolve().parents[5]
    folder = Path(__file__).resolve().parent
    source = json.loads(
        (
            root
            / "certificates/centered_quarter_bv_pseudodistribution.json"
        ).read_text()
    )
    data = coefficients(source)
    nodes = tuple(Q(value) for value in data["grid"])
    triples = data["triples"]
    categories = data["categories"]
    size = 41
    use_harmonics = profile in (
        "harmonic",
        "full",
        "rowcone",
        "rowsupport",
        "rowrefine",
        "rowcert",
        "rowcutsupport",
    )
    use_global_strengthening = profile in (
        "full",
        "rowcone",
        "rowsupport",
        "rowrefine",
        "rowcert",
        "rowcutsupport",
    )
    use_integer_row_cone = profile in (
        "rowcone",
        "rowsupport",
        "rowrefine",
        "rowcert",
        "rowcutsupport",
    )

    alpha = cp.Variable(len(nodes), nonneg=True)
    nu = cp.Variable(len(triples), nonneg=True)
    # Keep the raw solver values for the large K4 nonnegative vector.  Using
    # a nonneg variable attribute makes CVXPY clip thousands of tiny negative
    # entries on recovery, which can hide material affine residuals.
    k4 = cp.Variable(len(data["orbits"]))
    margin = cp.Variable()
    constraints = [
        cp.sum(alpha) == 40,
        cp.sum(nu) == 1560,
        1 + np.array([float(node) for node in nodes]) @ alpha == 0,
        data["pair_marginal"] @ nu == 39 * alpha,
        data["face_incidence"] @ k4 == nu / 390,
        data["centered_matrix"][:, len(triples) :] @ k4
        + data["centered_matrix"][:, : len(triples)] @ nu
        == 0,
        k4 >= 0,
        alpha >= margin,
        nu >= margin,
        # Exact Welch/frame-potential necessity for rank at most five.
        size
        * (
            1
            + np.array([float(node * node) for node in nodes])
            @ alpha
        )
        >= size * size / 5,
    ]

    # Centered vertex flag.
    vertex_second = cp.diag(alpha) + cp.reshape(
        data["vertex_distinct"].reshape(
            len(nodes) * len(nodes), len(triples)
        )
        @ nu,
        (len(nodes), len(nodes)),
        order="C",
    )
    vertex_block = cp.bmat(
        [
            [
                vertex_second,
                cp.reshape(alpha, (len(nodes), 1), order="C"),
            ],
            [
                cp.reshape(alpha, (1, len(nodes)), order="C"),
                np.ones((1, 1)),
            ],
        ]
    )
    constraints.extend(
        (
            vertex_block >> 0,
            vertex_block
            @ np.r_[np.ones(len(nodes)), -40]
            == 0,
            vertex_block
            @ np.r_[[float(node) for node in nodes], 1]
            == 0,
        )
    )
    quotient_blocks: list[cp.Expression] = []
    vertex_kernels = np.array(
        [
            np.r_[np.ones(len(nodes)), -40],
            np.r_[[float(node) for node in nodes], 1],
        ]
    )
    vertex_keep = quotient_keep_indices(vertex_kernels)
    quotient_blocks.append(vertex_block[vertex_keep, :][:, vertex_keep])

    integer_degree_types: tuple[tuple[int, ...], ...] = ()
    integer_degree_weights = None
    if use_integer_row_cone:
        # This is the exact convex hull of all integral quarter-grid degree
        # rows satisfying pointwise centering, robust depth on both sides,
        # the antipodal-row symmetry, and the exact d_(-3/4) and contact
        # degree bounds.  The second-moment equations identify
        #
        #   E[d_i d_j] = diag(alpha) + E[d_i(d_j-delta_ij)]
        #
        # with the centered vertex flag matrix above.
        all_integer_degree_types = degree_types()
        assert len(all_integer_degree_types) == 9882
        if profile == "rowsupport":
            # Sixteen rows selected by an L-infinity projection of the
            # surviving full-profile witness onto the exact 9,882-row
            # moment cone.  Feasibility on this inner cone is automatically
            # feasibility for the complete row cone.
            support_indices = (
                1289,
                5055,
                6534,
                6602,
                6705,
                8023,
                8123,
                8788,
                8902,
                9037,
                9381,
                9460,
                9836,
                9856,
                9857,
                9864,
            )
            integer_degree_types = tuple(
                all_integer_degree_types[index] for index in support_indices
            )
        elif profile == "rowrefine":
            discovery = json.loads(
                (folder / "joint_rowcone_x13.json").read_text()
            )
            support_indices = tuple(
                index
                for index, weight in enumerate(
                    discovery["integer_degree_weights"]
                )
                if weight > 1e-4
            )
            assert len(support_indices) == 101
            integer_degree_types = tuple(
                all_integer_degree_types[index] for index in support_indices
            )
        elif profile == "rowcutsupport":
            # Union of four sparse HiGHS supports: two exact membership
            # representations and the nearest row-cone projections of the
            # first two explicitly separated SDP iterates.
            support_indices = (
                1409,
                1513,
                1797,
                1850,
                3296,
                3438,
                3589,
                5048,
                5205,
                5261,
                6395,
                6396,
                6615,
                6705,
                7389,
                7689,
                7796,
                7807,
                7830,
                7922,
                7934,
                7960,
                8023,
                8123,
                8637,
                8767,
                8786,
                8788,
                8913,
                8914,
                8923,
                8937,
                8942,
                9037,
                9049,
                9060,
                9075,
                9148,
                9162,
                9204,
                9318,
                9343,
                9417,
                9846,
                9856,
                9857,
                9864,
            )
            integer_degree_types = tuple(
                all_integer_degree_types[index] for index in support_indices
            )
        elif profile == "rowcert":
            # Full-rank Caratheodory support returned by an independent
            # HiGHS membership LP for the fixed X=13, D=3/25 interior
            # iterate.  The LP used all 9,882 catalogue columns and matched
            # all 36 normalized moments to 9.3e-12.
            support_indices = (
                3438,
                5048,
                6395,
                6705,
                7689,
                7807,
                7960,
                8023,
                8123,
                8788,
                8913,
                8923,
                8942,
                9037,
                9075,
                9856,
                9857,
                9864,
            )
            integer_degree_types = tuple(
                all_integer_degree_types[index] for index in support_indices
            )
        else:
            integer_degree_types = all_integer_degree_types
        degree_array = np.asarray(integer_degree_types, dtype=float)
        integer_degree_weights = cp.Variable(
            len(integer_degree_types),
            name="integer_degree_weights",
        )
        constraints.append(integer_degree_weights >= 0)
        moment_left = [cp.sum(integer_degree_weights)]
        moment_right = [1]
        moment_left.extend(
            degree_array[:, color] @ integer_degree_weights / 40
            for color in range(len(nodes))
        )
        moment_right.extend(alpha[color] / 40 for color in range(len(nodes)))
        for first_color in range(len(nodes)):
            for second_color in range(first_color, len(nodes)):
                moment_left.append(
                    (
                        degree_array[:, first_color]
                        * degree_array[:, second_color]
                    )
                    @ integer_degree_weights
                    / 1600
                )
                moment_right.append(
                    vertex_second[first_color, second_color] / 1600
                )

        # The 36 degree features have exact row rank 18.  The omitted
        # equations follow from the two pointwise-centering kernels and
        # the antipodal triple identities already imposed by the feasible
        # K3 orbit list.  Keeping an independent feature basis avoids an
        # exactly singular conic equality system.  Full 36-row residuals
        # are evaluated in the output below.
        independent_moment_indices = (
            0,
            5,
            6,
            4,
            3,
            30,
            33,
            26,
            28,
            27,
            31,
            21,
            24,
            23,
            2,
            22,
            18,
            20,
        )
        constraints.extend(
            moment_left[index] == moment_right[index]
            for index in independent_moment_indices
        )
        constraints.append(
            # If E_{-1} is the number of unordered antipodal pairs,
            # alpha_{-1}=2 E_{-1}/41 and E_{-1}<=18.
            41 * alpha[0] <= 36
        )
        unnormalized_targets: list[cp.Expression | int] = [1]
        unnormalized_targets.extend(alpha[color] for color in range(len(nodes)))
        for first_color in range(len(nodes)):
            for second_color in range(first_color, len(nodes)):
                unnormalized_targets.append(
                    vertex_second[first_color, second_color]
                )
        unnormalized_row_features = [np.ones(len(degree_array))]
        unnormalized_row_features.extend(
            degree_array[:, color] for color in range(len(nodes))
        )
        for first_color in range(len(nodes)):
            for second_color in range(first_color, len(nodes)):
                unnormalized_row_features.append(
                    degree_array[:, first_color]
                    * degree_array[:, second_color]
                )
        for coefficients_by_feature, exact_bound in ROW_CONE_MOMENT_CUTS:
            catalogue_values = sum(
                coefficient * unnormalized_row_features[index]
                for index, coefficient in coefficients_by_feature.items()
            )
            assert int(np.max(catalogue_values)) <= exact_bound
            constraints.append(
                sum(
                    coefficient * unnormalized_targets[index]
                    for index, coefficient in coefficients_by_feature.items()
                )
                <= exact_bound
            )

    # Ordered-edge covariance blocks.  The K3 centering rows imply their
    # top kernel equations; direct PSD is still imposed.
    factor = math.comb(size, 4) / size
    for color in range(len(nodes)):
        first = data["edge_first"][color] @ nu
        distinct = factor * cp.reshape(
            data["edge_flag"][color].reshape(
                len(categories) * len(categories), len(data["orbits"])
            )
            @ k4,
            (len(categories), len(categories)),
            order="C",
        )
        second = cp.diag(first) + distinct
        block = cp.bmat(
            [
                [
                    second,
                    cp.reshape(first, (len(categories), 1), order="C"),
                ],
                [
                    cp.reshape(first, (1, len(categories)), order="C"),
                    cp.reshape(alpha[color], (1, 1), order="C"),
                ],
            ]
        )
        constraints.append(block >> 0)
        active_profiles = [
            index
            for index in range(len(categories))
            if np.any(data["edge_first"][color, index])
        ]
        active_indices = active_profiles + [len(categories)]
        active_block = block[active_indices, :][:, active_indices]
        edge_kernels = np.array(
            [
                np.r_[np.ones(len(active_profiles)), -39],
                np.r_[
                    [
                        float(nodes[categories[index][0]])
                        for index in active_profiles
                    ],
                    1 + float(nodes[color]),
                ],
                np.r_[
                    [
                        float(nodes[categories[index][1]])
                        for index in active_profiles
                    ],
                    1 + float(nodes[color]),
                ],
            ]
        )
        edge_keep = quotient_keep_indices(edge_kernels)
        quotient_blocks.append(
            active_block[edge_keep, :][:, edge_keep]
        )

    if use_harmonics:
        # Ordinary two-point positivity through the exact finite range used
        # before the C093 analytic tail.
        pair_values = np.array(
            [
                [float(value) for value in gegenbauer_5(node, 121)]
                for node in nodes
            ]
        )
        for degree in range(1, 122):
            moment = 1 + pair_values[:, degree] @ alpha
            constraints.append(moment == 0 if degree == 1 else moment >= 0)

        # Full-radial BV blocks through degree 16, including the forced
        # centered W0 and W1 kernels.
        constants, alpha_arrays, nu_arrays = coefficient_arrays(
            nodes, triples, 16
        )
        for degree in range(17):
            expression = constants[degree] + cp.reshape(
                alpha_arrays[degree] @ alpha
                + nu_arrays[degree] @ nu,
                (len(nodes) + 1, len(nodes) + 1),
                order="C",
            )
            if degree == 0:
                active = expression[: len(nodes), : len(nodes)]
                kernel = np.array(
                    [float(node + Q(1, 40)) for node in nodes]
                )
                constraints.extend((active >> 0, active @ kernel == 0))
                keep = quotient_keep_indices(kernel[None, :])
                quotient_blocks.append(active[keep, :][:, keep])
            elif degree == 1:
                active = expression[1 : len(nodes), 1 : len(nodes)]
                constraints.extend(
                    (active >> 0, active @ np.ones(len(nodes) - 1) == 0)
                )
                keep = quotient_keep_indices(
                    np.ones((1, len(nodes) - 1))
                )
                quotient_blocks.append(active[keep, :][:, keep])
            else:
                active = expression[1 : len(nodes), 1 : len(nodes)]
                constraints.append(active >> 0)
                quotient_blocks.append(active)

        constraints.extend(pair_frame_constraints(nodes, alpha))

    rank_band_count = 0
    rank_expressions: dict[str, tuple[cp.Expression, cp.Expression]] = {}
    if use_global_strengthening:
        # Exact robust vertex marginals and exact local cap rows.
        constraints.extend((cp.sum(alpha[:4]) >= 7, cp.sum(alpha[5:]) >= 6))
        for row in stratified_capacity_rows(nodes, triples):
            constraints.append(
                np.array(row["nu_coefficients"], dtype=float) @ nu
                <= 3
                * row["capacity"]
                * cp.sum(alpha[list(row["alpha_indices"])])
            )
        for row in weighted_capacity_rows(nodes, triples):
            constraints.append(
                np.array(row["nu_coefficients"], dtype=float) @ nu
                <= 3
                * sum(
                    capacity * alpha[index]
                    for index, capacity in row["capacities"].items()
                )
            )

        # Universal global secants of all 27 sharp harmonic-rank bands.
        for kernel in default_kernels("rich"):
            variance, centered, _ = rank_traces(
                kernel, nodes, triples, alpha, nu
            )
            rank_expressions[kernel.name] = (variance, centered)
            upper = safe_variance_upper(kernel, nodes)
            slope = global_secant_slope(upper, kernel.rank)
            constraints.extend(
                (
                    variance >= 0,
                    variance <= float(upper),
                    centered <= float(slope) * variance,
                    centered >= -float(slope) * variance,
                )
            )
            rank_band_count += 1

    h2_chord = None
    if h2_lower is not None or h2_upper is not None:
        if h2_lower is None or h2_upper is None:
            raise ValueError("both H2 cell endpoints are required")
        if not (0 <= h2_lower < h2_upper):
            raise ValueError("H2 cell must satisfy 0 <= lower < upper")
        if "H2" not in rank_expressions:
            raise ValueError("H2 cell requires global rank strengthening")
        h2_slope, h2_intercept, lower_radius, upper_radius = (
            rational_radius_chord(
                h2_lower,
                h2_upper,
                rank=14,
                scale=10**12,
            )
        )
        h2_variance, h2_centered = rank_expressions["H2"]
        constraints.extend(
            (
                h2_variance >= float(h2_lower),
                h2_variance <= float(h2_upper),
                h2_centered
                <= float(h2_slope) * h2_variance
                + float(h2_intercept),
                h2_centered
                >= -float(h2_slope) * h2_variance
                - float(h2_intercept),
            )
        )
        h2_chord = {
            "lower": str(h2_lower),
            "upper": str(h2_upper),
            "slope": str(h2_slope),
            "intercept": str(h2_intercept),
            "lower_radius_upper_bound": str(lower_radius),
            "upper_radius_upper_bound": str(upper_radius),
        }

    spectral_y_bound = None
    if spectral_x is not None:
        if spectral_x < 0:
            raise ValueError("--spectral-x must be nonnegative")
        node_squares = np.array(
            [float(node * node) for node in nodes], dtype=float
        )
        node_products = np.array(
            [
                float(nodes[i] * nodes[j] * nodes[k])
                for i, j, k in triples
            ],
            dtype=float,
        )
        trace_two_expression = size * (
            1 + node_squares @ alpha
        )
        trace_three_expression = size * (
            1 + 3 * node_squares @ alpha + node_products @ nu
        )
        gram_variance_expression = (
            trace_two_expression - Q(size * size, 5)
        )
        gram_centered_expression = (
            trace_three_expression
            - Q(3 * size, 5) * trace_two_expression
            + Q(2 * size**3, 25)
        )
        # For exact global quarter-grid edge counts,
        #
        #   X = 40 V = 5 sum_k k^2 E_k - 11808
        #
        # is a nonnegative integer.  On a fixed X branch the sharp
        # rank-five inequality 20D^2 <= 9V^3 is exactly the linear band
        #
        #   |800 D| <= floor(sqrt(9 X^3 / 2)).
        spectral_y_bound = math.isqrt(9 * spectral_x**3 // 2)
        assert (
            2 * spectral_y_bound**2 <= 9 * spectral_x**3
            and 2 * (spectral_y_bound + 1) ** 2 > 9 * spectral_x**3
        )
        constraints.extend(
            (
                gram_variance_expression == spectral_x / 40,
                gram_centered_expression <= spectral_y_bound / 800,
                gram_centered_expression >= -spectral_y_bound / 800,
            )
        )
        if spectral_d is not None:
            constraints.append(
                gram_centered_expression == float(spectral_d)
            )

    interior_margin = None
    if seek_interior:
        if integer_degree_weights is None:
            raise ValueError("--interior requires an integer row-cone profile")
        interior_margin = cp.Variable(name="interior_margin")
        source_k4 = np.array(
            json.loads(
                (folder / "joint_rowcert_x13.json").read_text()
            )["k4"],
            dtype=float,
        )
        k4_support = np.flatnonzero(source_k4 > 1e-6)
        constraints.append(margin >= 0.5)
        if maximize_interior_floor:
            constraints.append(interior_margin >= 0)
            constraints.extend(
                block
                - interior_margin * np.eye(block.shape[0])
                >> 0
                for block in quotient_blocks
            )
            objective = interior_margin
        else:
            constraints.extend(
                (
                    interior_margin == 0.05,
                    # Keep the full K4 cone available.  Restricting to the
                    # discovery support made stronger quotient floors
                    # artificially infeasible.
                    k4 >= interior_k4_floor,
                    integer_degree_weights >= interior_row_floor,
                )
            )
            constraints.extend(
                block
                - interior_psd_floor * np.eye(block.shape[0])
                >> 0
                for block in quotient_blocks
            )
            objective = margin
    else:
        objective = margin
    problem = cp.Problem(cp.Maximize(objective), constraints)
    if solver == "CLARABEL":
        clarabel_options = {}
        tolerance = 1e-4 if profile == "rowcone" else 2e-7
        feasibility_tolerance = (
            5e-6
            if maximize_interior_floor
            else 2e-6
            if seek_interior
            else min(tolerance, 1e-6)
        )
        gap_tolerance = 5e-4 if seek_interior else tolerance
        value = problem.solve(
            solver=solver,
            max_iter=500,
            tol_feas=feasibility_tolerance,
            tol_gap_abs=gap_tolerance,
            tol_gap_rel=gap_tolerance,
            verbose=True,
            **clarabel_options,
        )
    elif solver == "SCS":
        value = problem.solve(
            solver=solver,
            max_iters=100000,
            eps=2e-6,
            acceleration_lookback=20,
            verbose=True,
        )
    else:
        raise ValueError(f"unsupported solver {solver}")
    report = {
        "schema": "kissing5.rank_strengthened_k4_flag_search.v1",
        "profile": profile,
        "solver": solver,
        "status": problem.status,
        "objective_pair_triple_margin": (
            None if value is None else float(value)
        ),
        "ordinary_pair_degrees": (
            "1..121" if use_harmonics else "Welch only"
        ),
        "bv_degrees": (
            "0..16" if use_harmonics else "none"
        ),
        "pair_frame_psd_subsets": (
            10 if use_harmonics else 0
        ),
        "global_rank_band_secants": rank_band_count,
        "h2_sharp_chord_cell": h2_chord,
        "exact_gram_spectral_x_40v": spectral_x,
        "exact_gram_spectral_y_bound": spectral_y_bound,
        "fixed_gram_centered_third": (
            None if spectral_d is None else str(spectral_d)
        ),
        "interior_objective": seek_interior,
        "maximize_interior_floor": maximize_interior_floor,
        "interior_quotient_psd_blocks": (
            len(quotient_blocks) if seek_interior else 0
        ),
        "interior_psd_floor": (
            interior_psd_floor if seek_interior else None
        ),
        "interior_row_floor": (
            interior_row_floor if seek_interior else None
        ),
        "interior_k4_floor": (
            interior_k4_floor if seek_interior else None
        ),
        "integer_degree_row_cone": use_integer_row_cone,
        "explicit_exact_row_cone_moment_cuts": (
            len(ROW_CONE_MOMENT_CUTS) if use_integer_row_cone else 0
        ),
        "integer_degree_row_types": len(integer_degree_types),
        "independent_integer_degree_moment_rows": (
            18 if use_integer_row_cone else 0
        ),
        "complete_integer_degree_row_catalogue": (
            9882 if use_integer_row_cone else 0
        ),
        "antipodal_edge_bound": (
            "E_-1 <= 18" if use_integer_row_cone else "not imposed"
        ),
    }
    if alpha.value is not None:
        alpha_value = np.array(alpha.value)
        nu_value = np.array(nu.value)
        k4_value = np.array(k4.value)
        trace_g2 = float(
            size
            * (
                1
                + sum(
                    alpha_value[index] * float(node * node)
                    for index, node in enumerate(nodes)
                )
            )
        )
        trace_g3 = float(
            size
            * (
                1
                + 3
                * sum(
                    alpha_value[index] * float(node * node)
                    for index, node in enumerate(nodes)
                )
                + sum(
                    nu_value[index]
                    * float(nodes[triple[0]])
                    * float(nodes[triple[1]])
                    * float(nodes[triple[2]])
                    for index, triple in enumerate(triples)
                )
            )
        )
        gram_variance = trace_g2 - size * size / 5
        gram_centered_third = (
            trace_g3
            - (3 * size / 5) * trace_g2
            + 2 * size**3 / 25
        )
        report.update(
            {
                "trace_g2": trace_g2,
                "trace_g3": trace_g3,
                "gram_rank5_variance": gram_variance,
                "gram_rank5_centered_third": gram_centered_third,
                "gram_rank5_sharp_residual": (
                    9 * gram_variance**3
                    - 20 * gram_centered_third**2
                ),
                "minimum_alpha": float(np.min(alpha_value)),
                "minimum_nu": float(np.min(nu_value)),
                "minimum_k4": float(np.min(k4_value)),
                "positive_k4_at_1e-9": int(np.sum(k4_value > 1e-9)),
                "objective_interior_margin": (
                    None
                    if interior_margin is None
                    else float(interior_margin.value)
                ),
                "interior_k4_support_size": (
                    None
                    if not seek_interior
                    else int(len(k4_value))
                ),
                "discovery_k4_support_size": (
                    None
                    if not seek_interior
                    else int(len(k4_support))
                ),
                "alpha": alpha_value.tolist(),
                "nu": nu_value.tolist(),
                "k4": k4_value.tolist(),
            }
        )
        if h2_chord is not None:
            h2_kernel = next(
                kernel
                for kernel in default_kernels("rich")
                if kernel.name == "H2"
            )
            h2_variance_value, h2_centered_value, _ = rank_traces(
                h2_kernel,
                nodes,
                triples,
                alpha_value,
                nu_value,
            )
            h2_line_value = (
                float(Q(h2_chord["slope"])) * float(h2_variance_value)
                + float(Q(h2_chord["intercept"]))
            )
            report.update(
                {
                    "h2_variance": float(h2_variance_value),
                    "h2_centered_third": float(h2_centered_value),
                    "h2_chord_slack": float(
                        h2_line_value - abs(float(h2_centered_value))
                    ),
                    "h2_sharp_residual": float(
                        144 * float(h2_variance_value) ** 3
                        - 182 * float(h2_centered_value) ** 2
                    ),
                }
            )
        if integer_degree_weights is not None:
            degree_weight_value = np.array(integer_degree_weights.value)
            degree_array = np.asarray(integer_degree_types, dtype=float)
            row_second = np.einsum(
                "r,ri,rj->ij",
                degree_weight_value,
                degree_array,
                degree_array,
            )
            vertex_second_value = (
                np.diag(alpha_value)
                + (
                    np.asarray(data["vertex_distinct"], dtype=float).reshape(
                        len(nodes) * len(nodes), len(triples)
                    )
                    @ nu_value
                ).reshape((len(nodes), len(nodes)))
            )
            report.update(
                {
                    "active_integer_degree_rows_at_1e-9": int(
                        np.sum(degree_weight_value > 1e-9)
                    ),
                    "minimum_integer_degree_weight": float(
                        np.min(degree_weight_value)
                    ),
                    "integer_degree_mass_residual": float(
                        abs(np.sum(degree_weight_value) - 1)
                    ),
                    "integer_degree_first_moment_max_residual": float(
                        np.max(
                            abs(degree_array.T @ degree_weight_value - alpha_value)
                        )
                    ),
                    "integer_degree_second_moment_max_residual": float(
                        np.max(abs(row_second - vertex_second_value))
                    ),
                    "antipodal_edge_count_from_alpha": float(
                        size * alpha_value[0] / 2
                    ),
                    "integer_degree_weights": degree_weight_value.tolist(),
                    "integer_degree_types": [
                        list(degree) for degree in integer_degree_types
                    ],
                }
            )
    suffix = (
        f"_x{spectral_x}" if spectral_x is not None else ""
    )
    if seek_interior:
        if maximize_interior_floor:
            floor_tag = f"_maxfloor_c{len(ROW_CONE_MOMENT_CUTS)}"
        else:
            floor_tag = (
                f"_p{interior_psd_floor:.0e}"
                f"_r{interior_row_floor:.0e}"
                f"_k{interior_k4_floor:.0e}"
            ).replace("-", "m")
        suffix += "_interior" + floor_tag
    if spectral_d is not None:
        suffix += "_d" + str(spectral_d).replace("/", "_")
    if h2_chord is not None:
        suffix += (
            "_h2_"
            + str(h2_lower).replace("/", "_")
            + "_"
            + str(h2_upper).replace("/", "_")
        )
    output = folder / f"joint_{profile}{suffix}.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                key: value
                for key, value in report.items()
                if key
                not in (
                    "alpha",
                    "nu",
                    "k4",
                    "integer_degree_types",
                    "integer_degree_weights",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        choices=(
            "welch",
            "harmonic",
            "full",
            "rowcone",
            "rowsupport",
            "rowrefine",
            "rowcert",
            "rowcutsupport",
        ),
        default="full",
    )
    parser.add_argument(
        "--solver",
        choices=("CLARABEL", "SCS"),
        default="CLARABEL",
    )
    parser.add_argument(
        "--spectral-x",
        type=int,
        help=(
            "fix the exact integer X=40V and impose the corresponding "
            "sharp rank-five spectral band"
        ),
    )
    parser.add_argument(
        "--interior",
        action="store_true",
        help=(
            "hold pair/triple margin above 0.5 and maximize a common "
            "positive floor on K4 atoms and row weights"
        ),
    )
    parser.add_argument(
        "--spectral-d",
        type=Q,
        help=(
            "fix the H1 centered third trace moment D to an exact "
            "rational value inside the selected X branch"
        ),
    )
    parser.add_argument(
        "--interior-psd-floor",
        type=float,
        default=5e-7,
        help="absolute eigenvalue floor on every quotient PSD block",
    )
    parser.add_argument(
        "--interior-row-floor",
        type=float,
        default=5e-8,
        help="absolute lower bound on each selected integer-row weight",
    )
    parser.add_argument(
        "--interior-k4-floor",
        type=float,
        default=5e-9,
        help="absolute lower bound on each selected K4 support mass",
    )
    parser.add_argument(
        "--maximize-interior-floor",
        action="store_true",
        help="maximize a common absolute eigenvalue floor on quotient blocks",
    )
    parser.add_argument(
        "--h2-lower",
        type=Q,
        help="closed lower endpoint of a sharp H2 chord cell",
    )
    parser.add_argument(
        "--h2-upper",
        type=Q,
        help="closed upper endpoint of a sharp H2 chord cell",
    )
    args = parser.parse_args()
    if args.spectral_d is not None and args.spectral_x is None:
        parser.error("--spectral-d requires --spectral-x")
    solve(
        args.profile,
        args.solver,
        args.spectral_x,
        args.interior,
        args.spectral_d,
        args.interior_psd_floor,
        args.interior_row_floor,
        args.interior_k4_floor,
        args.maximize_interior_floor,
        args.h2_lower,
        args.h2_upper,
    )


if __name__ == "__main__":
    main()
