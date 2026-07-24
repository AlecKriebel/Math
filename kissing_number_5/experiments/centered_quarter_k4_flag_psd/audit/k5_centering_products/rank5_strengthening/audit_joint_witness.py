#!/usr/bin/env python3
"""Independent numerical residual audit for a joint K2/K3/K4 witness.

This script does not call the conic search.  It reconstructs every matrix and
affine row from the exported alpha, nu, and K4 masses, and separately solves
membership LPs over the complete 9,882-row integer degree catalogue.
Numerical success is evidence for a relaxation witness, not an exact
certificate.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from experiments.centered_global_count_milp.search_degree_lift import (
    degree_types,
)
from experiments.centered_quarter_k4_flag_psd.audit.search_full_centering import (
    coefficients,
)
from experiments.continuous_rank_bv_search.search import (
    coefficient_arrays,
    default_kernels,
    gegenbauer_5,
    global_secant_slope,
    harmonic_dimension,
    rank_traces,
    safe_variance_upper,
    stratified_capacity_rows,
    weighted_capacity_rows,
)


INDEPENDENT_MOMENT_INDICES = (
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


def quotient_keep_indices(kernel_vectors: np.ndarray) -> list[int]:
    """Match the coordinate quotient used by the search."""

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


def min_eigenvalue(matrix: np.ndarray) -> float:
    """Smallest eigenvalue after explicitly symmetrizing roundoff."""

    symmetric = (matrix + matrix.T) / 2
    return float(np.linalg.eigvalsh(symmetric)[0])


def max_abs(array: np.ndarray) -> float:
    return float(np.max(np.abs(array))) if array.size else 0.0


def build_row_features(
    rows: np.ndarray,
    alpha: np.ndarray,
    vertex_second: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the 36 normalized row features and their target moments."""

    feature_rows = [np.ones(len(rows))]
    target = [1.0]
    feature_rows.extend(rows[:, color] / 40 for color in range(7))
    target.extend(alpha[color] / 40 for color in range(7))
    for first in range(7):
        for second in range(first, 7):
            feature_rows.append(
                rows[:, first] * rows[:, second] / 1600
            )
            target.append(vertex_second[first, second] / 1600)
    return np.asarray(feature_rows), np.asarray(target)


def row_cone_audit(
    alpha: np.ndarray,
    vertex_second: np.ndarray,
) -> dict[str, object]:
    """Audit membership and relative interior in the full row-moment cone."""

    rows = np.asarray(degree_types(), dtype=float)
    assert rows.shape == (9882, 7)
    features, target = build_row_features(rows, alpha, vertex_second)
    independent = np.asarray(INDEPENDENT_MOMENT_INDICES)
    matrix = features[independent]
    right = target[independent]
    options = {
        "primal_feasibility_tolerance": 1e-9,
        "dual_feasibility_tolerance": 1e-9,
    }

    membership = linprog(
        np.zeros(len(rows)),
        A_eq=matrix,
        b_eq=right,
        bounds=(0, None),
        method="highs",
        options=options,
    )
    answer: dict[str, object] = {
        "catalogue_size": len(rows),
        "feature_count": len(target),
        "independent_feature_count": len(independent),
        "membership_status": int(membership.status),
        "membership_message": membership.message,
    }
    if membership.success:
        weights = np.asarray(membership.x)
        support = np.flatnonzero(weights > 1e-12)
        answer.update(
            {
                "membership_full_feature_max_residual": max_abs(
                    features @ weights - target
                ),
                "membership_min_weight": float(np.min(weights)),
                "membership_min_positive_weight": float(
                    np.min(weights[support])
                ),
                "membership_support_size": int(len(support)),
                "membership_sparse_support": [
                    {
                        "index": int(index),
                        "row": rows[index].astype(int).tolist(),
                        "weight": float(weights[index]),
                    }
                    for index in support
                ],
            }
        )

    # To maximize a uniform floor, write w = u + epsilon * 1.  This avoids
    # materializing a 9,882-square identity constraint.
    augmented_matrix = np.column_stack(
        (matrix, matrix @ np.ones(len(rows)))
    )
    interior = linprog(
        np.r_[np.zeros(len(rows)), -1.0],
        A_eq=augmented_matrix,
        b_eq=right,
        bounds=(0, None),
        method="highs",
        options=options,
    )
    answer.update(
        {
            "relative_interior_status": int(interior.status),
            "relative_interior_message": interior.message,
        }
    )
    if interior.success:
        epsilon = float(interior.x[-1])
        excess = np.asarray(interior.x[:-1])
        weights = excess + epsilon
        support = np.flatnonzero(excess > 1e-12)
        answer.update(
            {
                "relative_interior_uniform_weight_floor": epsilon,
                "relative_interior_full_feature_max_residual": max_abs(
                    features @ weights - target
                ),
                "relative_interior_excess_support_size": int(len(support)),
                "relative_interior_sparse_excess": [
                    {
                        "index": int(index),
                        "row": rows[index].astype(int).tolist(),
                        "excess_weight": float(excess[index]),
                    }
                    for index in support
                ],
            }
        )

    # If exact membership fails, quantify the distance in the unnormalized
    # integer feature coordinates and find a catalogue-valid separating
    # inequality.  The constant mass feature is fixed separately.
    integer_rows = rows.astype(np.int64)
    raw_features = [np.ones(len(rows), dtype=np.int64)]
    raw_target = [1.0]
    raw_features.extend(integer_rows[:, color] for color in range(7))
    raw_target.extend(alpha.tolist())
    for first in range(7):
        for second in range(first, 7):
            raw_features.append(
                integer_rows[:, first] * integer_rows[:, second]
            )
            raw_target.append(vertex_second[first, second])
    raw_features_array = np.asarray(raw_features, dtype=np.int64)
    raw_target_array = np.asarray(raw_target, dtype=float)
    nonconstant = np.asarray(INDEPENDENT_MOMENT_INDICES[1:])
    raw_matrix = raw_features_array[nonconstant]
    raw_right = raw_target_array[nonconstant]
    count = len(nonconstant)

    nearest = linprog(
        np.r_[np.zeros(len(rows)), 1.0],
        A_ub=np.r_[
            np.c_[raw_matrix, -np.ones(count)],
            np.c_[-raw_matrix, -np.ones(count)],
        ],
        b_ub=np.r_[raw_right, -raw_right],
        A_eq=np.c_[
            np.ones((1, len(rows))),
            np.zeros((1, 1)),
        ],
        b_eq=[1.0],
        bounds=(0, None),
        method="highs",
        options=options,
    )
    answer.update(
        {
            "nearest_raw_linf_status": int(nearest.status),
            "nearest_raw_linf_message": nearest.message,
        }
    )
    if nearest.success:
        nearest_weights = np.asarray(nearest.x[:-1])
        nearest_support = np.flatnonzero(nearest_weights > 1e-12)
        answer.update(
            {
                "nearest_raw_linf_distance": float(nearest.x[-1]),
                "nearest_raw_linf_support_size": int(len(nearest_support)),
                "nearest_raw_linf_sparse_support": [
                    {
                        "index": int(index),
                        "row": integer_rows[index].tolist(),
                        "weight": float(nearest_weights[index]),
                    }
                    for index in nearest_support
                ],
            }
        )

    # Maximize y.target - max_row y.row under ||y||_1 <= 1.
    # Variables are y_plus, y_minus, and a free catalogue upper bound z.
    separator = linprog(
        np.r_[-raw_right, raw_right, 1.0],
        A_ub=np.r_[
            np.c_[
                raw_matrix.T,
                -raw_matrix.T,
                -np.ones(len(rows)),
            ],
            np.r_[np.ones(2 * count), 0.0][None, :],
        ],
        b_ub=np.r_[np.zeros(len(rows)), 1.0],
        bounds=[(0, None)] * (2 * count) + [(None, None)],
        method="highs",
        options=options,
    )
    answer.update(
        {
            "separator_status": int(separator.status),
            "separator_message": separator.message,
        }
    )
    if separator.success:
        direction = (
            separator.x[:count] - separator.x[count : 2 * count]
        )
        numerical_gap = float(
            direction @ raw_right - separator.x[-1]
        )
        answer.update(
            {
                "separator_l1_norm": float(np.sum(np.abs(direction))),
                "separator_numerical_gap": numerical_gap,
                "separator_feature_indices": nonconstant.tolist(),
                "separator_direction": direction.tolist(),
            }
        )
        direction_scale = np.max(np.abs(direction))
        if numerical_gap > 0 and direction_scale > 0:
            normalized = direction / direction_scale
            for exponent in range(1, 13):
                scale = 10**exponent
                integer_direction = np.rint(
                    scale * normalized
                ).astype(np.int64)
                catalogue_values = integer_direction @ raw_matrix
                exact_bound = int(np.max(catalogue_values))
                violation = float(
                    integer_direction @ raw_right - exact_bound
                )
                if violation > 0:
                    maximizers = np.flatnonzero(
                        catalogue_values == exact_bound
                    )
                    answer["integer_separator"] = {
                        "rounding_scale": scale,
                        "feature_indices": nonconstant.tolist(),
                        "integer_coefficients": integer_direction.tolist(),
                        "exact_catalogue_bound": exact_bound,
                        "target_violation": violation,
                        "maximizing_row_indices": maximizers.tolist(),
                        "maximizing_rows": integer_rows[maximizers].tolist(),
                    }
                    break
    return answer


def audit(path: Path) -> dict[str, object]:
    folder = Path(__file__).resolve().parent
    root = Path(__file__).resolve().parents[5]
    report = json.loads(path.read_text())
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
    alpha = np.asarray(report["alpha"], dtype=float)
    nu = np.asarray(report["nu"], dtype=float)
    k4 = np.asarray(report["k4"], dtype=float)
    node_values = np.asarray([float(node) for node in nodes])

    pair_marginal_residual = data["pair_marginal"] @ nu - 39 * alpha
    face_residual = data["face_incidence"] @ k4 - nu / 390
    k4_centering_residual = (
        data["centered_matrix"][:, len(triples) :] @ k4
        + data["centered_matrix"][:, : len(triples)] @ nu
    )
    vertex_distinct = (
        np.asarray(data["vertex_distinct"], dtype=float)
        .reshape(49, len(triples))
        @ nu
    ).reshape(7, 7)
    vertex_second = np.diag(alpha) + vertex_distinct
    vertex_block = np.block(
        [
            [vertex_second, alpha[:, None]],
            [alpha[None, :], np.ones((1, 1))],
        ]
    )
    vertex_kernels = np.asarray(
        [
            np.r_[np.ones(7), -40],
            np.r_[node_values, 1],
        ]
    )
    vertex_keep = quotient_keep_indices(vertex_kernels)
    vertex_quotient = vertex_block[np.ix_(vertex_keep, vertex_keep)]

    affine = {
        "alpha_mass_residual": float(np.sum(alpha) - 40),
        "nu_mass_residual": float(np.sum(nu) - 1560),
        "pair_centering_residual": float(1 + node_values @ alpha),
        "pair_marginal_max_residual": max_abs(pair_marginal_residual),
        "k4_face_max_residual": max_abs(face_residual),
        "k4_centering_max_residual": max_abs(k4_centering_residual),
        "minimum_alpha": float(np.min(alpha)),
        "minimum_nu": float(np.min(nu)),
        "minimum_k4": float(np.min(k4)),
    }

    psd_blocks: list[dict[str, object]] = [
        {
            "name": "vertex_full",
            "dimension": int(vertex_block.shape[0]),
            "minimum_eigenvalue": min_eigenvalue(vertex_block),
            "known_kernel_max_residual": max_abs(
                vertex_block @ vertex_kernels.T
            ),
        },
        {
            "name": "vertex_quotient",
            "dimension": int(vertex_quotient.shape[0]),
            "minimum_eigenvalue": min_eigenvalue(vertex_quotient),
        },
    ]

    factor = math.comb(41, 4) / 41
    for color in range(7):
        first = np.asarray(data["edge_first"][color] @ nu, dtype=float)
        distinct = factor * (
            np.asarray(data["edge_flag"][color], dtype=float)
            .reshape(len(categories) ** 2, len(data["orbits"]))
            @ k4
        ).reshape((len(categories), len(categories)))
        second = np.diag(first) + distinct
        block = np.block(
            [
                [second, first[:, None]],
                [first[None, :], np.asarray([[alpha[color]]])],
            ]
        )
        active_profiles = [
            index
            for index in range(len(categories))
            if np.any(data["edge_first"][color, index])
        ]
        active_indices = active_profiles + [len(categories)]
        active = block[np.ix_(active_indices, active_indices)]
        kernels = np.asarray(
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
        keep = quotient_keep_indices(kernels)
        quotient = active[np.ix_(keep, keep)]
        psd_blocks.extend(
            (
                {
                    "name": f"ordered_edge_{nodes[color]}_full",
                    "dimension": int(block.shape[0]),
                    "minimum_eigenvalue": min_eigenvalue(block),
                },
                {
                    "name": f"ordered_edge_{nodes[color]}_active",
                    "dimension": int(active.shape[0]),
                    "minimum_eigenvalue": min_eigenvalue(active),
                    "known_kernel_max_residual": max_abs(
                        active @ kernels.T
                    ),
                },
                {
                    "name": f"ordered_edge_{nodes[color]}_quotient",
                    "dimension": int(quotient.shape[0]),
                    "minimum_eigenvalue": min_eigenvalue(quotient),
                },
            )
        )

    pair_values = np.asarray(
        [
            [float(value) for value in gegenbauer_5(node, 121)]
            for node in nodes
        ]
    )
    pair_moments = 1 + pair_values.T @ alpha
    harmonic = {
        "degree_one_abs_residual": float(abs(pair_moments[1])),
        "minimum_degree_2_through_121": float(np.min(pair_moments[2:])),
        "minimum_degree_2_through_121_index": int(
            np.argmin(pair_moments[2:]) + 2
        ),
    }

    constants, alpha_arrays, nu_arrays = coefficient_arrays(
        nodes, triples, 16
    )
    for degree in range(17):
        expression = constants[degree] + (
            alpha_arrays[degree] @ alpha + nu_arrays[degree] @ nu
        ).reshape((8, 8))
        if degree == 0:
            active = expression[:7, :7]
            kernel = np.asarray(
                [float(node + Q(1, 40)) for node in nodes]
            )[None, :]
            keep = quotient_keep_indices(kernel)
            quotient = active[np.ix_(keep, keep)]
            kernel_residual = max_abs(active @ kernel.T)
        elif degree == 1:
            active = expression[1:7, 1:7]
            kernel = np.ones((1, 6))
            keep = quotient_keep_indices(kernel)
            quotient = active[np.ix_(keep, keep)]
            kernel_residual = max_abs(active @ kernel.T)
        else:
            active = expression[1:7, 1:7]
            quotient = active
            kernel_residual = None
        entry: dict[str, object] = {
            "name": f"bv_degree_{degree}_active",
            "dimension": int(active.shape[0]),
            "minimum_eigenvalue": min_eigenvalue(active),
        }
        if kernel_residual is not None:
            entry["known_kernel_max_residual"] = kernel_residual
        psd_blocks.append(entry)
        psd_blocks.append(
            {
                "name": f"bv_degree_{degree}_quotient",
                "dimension": int(quotient.shape[0]),
                "minimum_eigenvalue": min_eigenvalue(quotient),
            }
        )

    values = np.asarray(
        [
            [float(value) for value in gegenbauer_5(node, 3)]
            for node in nodes
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
        block = np.asarray(
            [
                [
                    1
                    + np.sum(
                        values[:, first]
                        * values[:, second]
                        * alpha
                    )
                    - 41 / rank
                    for second in subset
                ]
                for first in subset
            ]
        )
        psd_blocks.append(
            {
                "name": "pair_frame_" + "_".join(map(str, subset)),
                "dimension": int(block.shape[0]),
                "minimum_eigenvalue": min_eigenvalue(block),
            }
        )

    stratified_slacks = []
    for index, row in enumerate(stratified_capacity_rows(nodes, triples)):
        left = np.asarray(row["nu_coefficients"], dtype=float) @ nu
        right = (
            3
            * row["capacity"]
            * np.sum(alpha[list(row["alpha_indices"])])
        )
        stratified_slacks.append((float(right - left), index))
    weighted_slacks = []
    for index, row in enumerate(weighted_capacity_rows(nodes, triples)):
        left = np.asarray(row["nu_coefficients"], dtype=float) @ nu
        right = 3 * sum(
            capacity * alpha[color]
            for color, capacity in row["capacities"].items()
        )
        weighted_slacks.append((float(right - left), index))
    capacity = {
        "negative_vertex_mass_slack": float(np.sum(alpha[:4]) - 7),
        "positive_vertex_mass_slack": float(np.sum(alpha[5:]) - 6),
        "minimum_stratified_slack": min(stratified_slacks),
        "minimum_weighted_slack": min(weighted_slacks),
    }

    secants = []
    for kernel in default_kernels("rich"):
        variance, centered, _ = rank_traces(
            kernel, nodes, triples, alpha, nu
        )
        variance = float(variance)
        centered = float(centered)
        upper = float(safe_variance_upper(kernel, nodes))
        slope = float(
            global_secant_slope(
                safe_variance_upper(kernel, nodes), kernel.rank
            )
        )
        secants.append(
            {
                "name": kernel.name,
                "rank": kernel.rank,
                "variance": variance,
                "centered_third": centered,
                "variance_lower_slack": variance,
                "variance_upper_slack": upper - variance,
                "centered_band_slack": slope * variance - abs(centered),
                "sharp_rank_residual": (
                    (kernel.rank - 2) ** 2 * variance**3
                    - kernel.rank
                    * (kernel.rank - 1)
                    * centered**2
                ),
            }
        )

    node_squares = node_values**2
    node_products = np.asarray(
        [
            float(nodes[first] * nodes[second] * nodes[third])
            for first, second, third in triples
        ]
    )
    trace_two = 41 * (1 + node_squares @ alpha)
    trace_three = 41 * (
        1 + 3 * node_squares @ alpha + node_products @ nu
    )
    variance = trace_two - 1681 / 5
    centered = (
        trace_three - (123 / 5) * trace_two + 137842 / 25
    )
    spectral_x = int(report["exact_gram_spectral_x_40v"])
    y_bound = math.isqrt(9 * spectral_x**3 // 2)
    fixed_d = Q(report["fixed_gram_centered_third"])
    spectral = {
        "trace_g2": float(trace_two),
        "trace_g3": float(trace_three),
        "variance": float(variance),
        "centered_third": float(centered),
        "x_residual": float(40 * variance - spectral_x),
        "fixed_d_residual": float(centered - float(fixed_d)),
        "endpoint": float(Q(y_bound, 800)),
        "endpoint_slack": float(Q(y_bound, 800) - abs(centered)),
        "sharp_rank5_slack": float(9 * variance**3 - 20 * centered**2),
        "integer_y_nearest": int(round(800 * centered)),
        "integer_y_residual": float(
            800 * centered - round(800 * centered)
        ),
        "integer_discriminant_slack_at_fixed_d": float(
            9 * spectral_x**3
            - 2 * (800 * float(fixed_d)) ** 2
        ),
    }

    source_k4 = np.asarray(
        json.loads((folder / "joint_rowcert_x13.json").read_text())["k4"],
        dtype=float,
    )
    support = source_k4 > 1e-6
    interior = {
        "source_support_size": int(np.sum(support)),
        "minimum_k4_on_source_support": float(np.min(k4[support])),
        "maximum_abs_k4_outside_source_support": float(
            np.max(np.abs(k4[~support]))
        ),
        "minimum_quotient_eigenvalue": min(
            item["minimum_eigenvalue"]
            for item in psd_blocks
            if item["name"].endswith("_quotient")
        ),
    }

    row_cone = row_cone_audit(alpha, vertex_second)
    min_psd = min(psd_blocks, key=lambda item: item["minimum_eigenvalue"])
    min_secant = min(secants, key=lambda item: item["centered_band_slack"])
    return {
        "schema": "kissing5.joint_k4_witness_numerical_audit.v1",
        "source": str(path.relative_to(root)),
        "affine_and_nonnegative": affine,
        "harmonic_pair_moments": harmonic,
        "capacity": capacity,
        "spectral_h1": spectral,
        "interior_support": interior,
        "minimum_psd_block": min_psd,
        "psd_blocks": psd_blocks,
        "minimum_global_secant": min_secant,
        "global_secants": secants,
        "row_cone": row_cone,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("witness", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.witness.resolve())
    output = (
        args.output.resolve()
        if args.output is not None
        else args.witness.with_name(args.witness.stem + "_audit.json")
    )
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "output": str(output),
                "affine_and_nonnegative": result[
                    "affine_and_nonnegative"
                ],
                "spectral_h1": result["spectral_h1"],
                "interior_support": result["interior_support"],
                "minimum_psd_block": result["minimum_psd_block"],
                "minimum_global_secant": result[
                    "minimum_global_secant"
                ],
                "row_cone": {
                    key: value
                    for key, value in result["row_cone"].items()
                    if "support" not in key and "excess" not in key
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
