#!/usr/bin/env python3
"""Joint quarter-grid K2/K3/K4 search with all centering identities at K4.

This is numerical discovery code, not a proof certificate.  In addition to
the original ordered-edge covariance blocks, it imposes:

* the vertex-flag covariance block and both pointwise centering kernels;
* all K2 -> K3 pointwise centering identities;
* all K3 -> K4 pointwise centering identities; and
* the three pointwise kernels of every ordered-edge Schur block.

The variables remain only exchangeable K2/K3/K4 orbit marginals.  Feasibility
therefore does not assert that a 41-point code, or even a globally consistent
exchangeable array, exists.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import itertools
import json
import math
from pathlib import Path

import cvxpy as cp
import numpy as np

from experiments.centered_quarter_k4_flag_psd.search import (
    EDGES,
    EDGE_INDEX,
    enumerate_orbits,
    face_types,
    flag_coefficients,
)


def edge(pattern: tuple[int, ...], first: int, second: int) -> int:
    return pattern[EDGE_INDEX[tuple(sorted((first, second)))]]


def triangle_edge_map(triple: tuple[int, int, int]):
    return {(0, 1): triple[0], (0, 2): triple[1], (1, 2): triple[2]}


def oriented_triangle_types(
    triples: tuple[tuple[int, int, int], ...]
) -> tuple[tuple[int, int, int], ...]:
    answer = set()
    for triple in triples:
        edges = triangle_edge_map(triple)
        for permutation in itertools.permutations(range(3)):
            i, j, k = permutation
            answer.add(
                (
                    edges[tuple(sorted((i, j)))],
                    edges[tuple(sorted((i, k)))],
                    edges[tuple(sorted((j, k)))],
                )
            )
    return tuple(sorted(answer))


def coefficients(source: dict):
    grid = tuple(Q(value) for value in source["grid"])
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {
        triple: index for index, triple in enumerate(triples)
    }
    categories = tuple(itertools.product(range(len(grid)), repeat=2))
    category_index = {
        category: index for index, category in enumerate(categories)
    }
    orbits, labeled = enumerate_orbits(source)

    face_incidence = np.zeros((len(triples), len(orbits)))
    edge_flag = [
        np.zeros((len(categories), len(categories), len(orbits)))
        for _ in grid
    ]
    for column, pattern in enumerate(orbits):
        for face in face_types(pattern):
            face_incidence[triple_index[face], column] += 1
        blocks = flag_coefficients(
            pattern, len(grid), category_index, True
        )
        for color in range(len(grid)):
            edge_flag[color][:, :, column] = blocks[color]

    pair_marginal = np.zeros((len(grid), len(triples)))
    edge_first = np.zeros(
        (len(grid), len(categories), len(triples))
    )
    vertex_distinct = np.zeros((len(grid), len(grid), len(triples)))
    for triple_column, triple in enumerate(triples):
        for color in triple:
            pair_marginal[color, triple_column] += 1 / 3
        edges = triangle_edge_map(triple)
        for i, j, k in itertools.permutations(range(3)):
            q = edges[tuple(sorted((i, j)))]
            first = edges[tuple(sorted((i, k)))]
            second = edges[tuple(sorted((j, k)))]
            edge_first[
                q, category_index[(first, second)], triple_column
            ] += 1 / 6
            vertex_distinct[
                q, first, triple_column
            ] += 1 / 6

    oriented_types = oriented_triangle_types(triples)
    oriented_index = {
        pattern: index for index, pattern in enumerate(oriented_types)
    }
    oriented_mass = np.zeros((len(oriented_types), len(triples)))
    for column, triple in enumerate(triples):
        edges = triangle_edge_map(triple)
        for i, j, k in itertools.permutations(range(3)):
            pattern = (
                edges[tuple(sorted((i, j)))],
                edges[tuple(sorted((i, k)))],
                edges[tuple(sorted((j, k)))],
            )
            oriented_mass[oriented_index[pattern], column] += 1 / 6

    # For an ordered K4 labeling (i,j,k,l), record the base ordered-triangle
    # type and the three colors from the base vertices to l.  There are 24
    # such labelings per unordered K4, with no normalization inside this
    # coefficient: C(N,4)/N supplies the physical scale.
    extension_count = np.zeros((len(oriented_types), len(orbits)))
    extension_sum = np.zeros(
        (len(oriented_types), 3, len(orbits))
    )
    for column, pattern in enumerate(orbits):
        for i, j, k, extension in itertools.permutations(range(4)):
            oriented = (
                edge(pattern, i, j),
                edge(pattern, i, k),
                edge(pattern, j, k),
            )
            row = oriented_index[oriented]
            extension_count[row, column] += 1
            for center_index, center in enumerate((i, j, k)):
                extension_sum[row, center_index, column] += float(
                    grid[edge(pattern, center, extension)]
                )

    # Collapse relabeling duplicates among the 609 apparent K3-centering
    # rows.  At N=41 the flag factor is the integer 2470.  Multiplication by
    # 24 clears both quarter-grid values and the 1/6 orientation average, so
    # the deduplication key is an exact integer vector.
    flag_factor = math.comb(41, 4) // 41
    centered_rows: dict[tuple[int, ...], np.ndarray] = {}
    grid_float = np.array([float(value) for value in grid])
    for row, (first, second, third) in enumerate(oriented_types):
        for center, incident in enumerate(
            ((first, second), (first, third), (second, third))
        ):
            target = (
                -1
                - grid_float[incident[0]]
                - grid_float[incident[1]]
            )
            combined = np.r_[
                target * oriented_mass[row],
                -flag_factor * extension_sum[row, center],
            ]
            integral = np.rint(24 * combined).astype(np.int64)
            assert np.max(np.abs(24 * combined - integral)) < 1e-10
            centered_rows.setdefault(tuple(integral.tolist()), integral)
    centered_matrix = np.array(tuple(centered_rows.values()), dtype=float)

    return {
        "grid": grid,
        "triples": triples,
        "categories": categories,
        "orbits": orbits,
        "labeled": labeled,
        "face_incidence": face_incidence,
        "edge_flag": edge_flag,
        "edge_first": edge_first,
        "pair_marginal": pair_marginal,
        "vertex_distinct": vertex_distinct,
        "oriented_types": oriented_types,
        "oriented_mass": oriented_mass,
        "extension_count": extension_count,
        "extension_sum": extension_sum,
        "centered_matrix": centered_matrix,
    }


def solve(level: str, solver: str, verbose: bool, output: Path) -> dict:
    root = Path(__file__).resolve().parents[3]
    source = json.loads(
        (root / "certificates/centered_quarter_bv_pseudodistribution.json")
        .read_text()
    )
    data = coefficients(source)
    grid_q = data["grid"]
    grid = np.array([float(value) for value in grid_q])
    triples = data["triples"]
    categories = data["categories"]
    orbits = data["orbits"]
    size = 41

    alpha = cp.Variable(len(grid), nonneg=True)
    nu = cp.Variable(len(triples), nonneg=True)
    k4 = cp.Variable(len(orbits), nonneg=True)
    margin = cp.Variable()
    constraints = [
        cp.sum(alpha) == size - 1,
        1 + grid @ alpha == 0,
        data["pair_marginal"] @ nu == (size - 2) * alpha,
        data["face_incidence"] @ k4
        == 4 * nu / ((size - 1) * (size - 2)),
        alpha >= margin,
        nu >= margin,
    ]

    flag_factor = math.comb(size, 4) / size

    # Vertex flag: d_a(i) counts the neighbors of color a at vertex i.
    vertex_second = cp.diag(alpha) + cp.reshape(
        data["vertex_distinct"].reshape(
            len(grid) * len(grid), len(triples)
        )
        @ nu,
        (len(grid), len(grid)),
        order="C",
    )
    vertex_block = cp.bmat(
        [
            [vertex_second, cp.reshape(alpha, (len(grid), 1), order="C")],
            [
                cp.reshape(alpha, (1, len(grid)), order="C"),
                np.ones((1, 1)),
            ],
        ]
    )
    if level in ("vertex", "triple", "edge", "full"):
        constraints.append(vertex_block >> 0)
        vertex_kernels = (
            np.r_[np.ones(len(grid)), -(size - 1)],
            np.r_[grid, 1.0],
        )
        for kernel in vertex_kernels:
            constraints.append(vertex_block @ kernel == 0)

    edge_blocks = []
    edge_kernels = []
    for q in range(len(grid)):
        first = data["edge_first"][q] @ nu
        flat_flag = data["edge_flag"][q].reshape(
            len(categories) * len(categories), len(orbits)
        )
        distinct = flag_factor * cp.reshape(
            flat_flag @ k4,
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
                    cp.reshape(alpha[q], (1, 1), order="C"),
                ],
            ]
        )
        edge_blocks.append(block)
        constraints.append(block >> 0)
        kernels = (
            np.r_[np.ones(len(categories)), -(size - 2)],
            np.r_[
                [grid[first_color] for first_color, _ in categories],
                1 + grid[q],
            ],
            np.r_[
                [grid[second_color] for _, second_color in categories],
                1 + grid[q],
            ],
        )
        edge_kernels.append(kernels)

        # Bottom rows are precisely the K2 -> K3 pointwise centering
        # identities.  Add them separately at the "pair" level.
        if level in ("pair", "vertex", "triple", "edge", "full"):
            for kernel in kernels:
                constraints.append(block[-1, :] @ kernel == 0)
        if level == "edge":
            for kernel in kernels:
                constraints.append(block @ kernel == 0)

    # Every ordered base triple has N-3 extensions.  Centering supplies one
    # exact weighted extension sum for each of its three base vertices.
    if level in ("triple", "edge", "full"):
        base_mass = data["oriented_mass"] @ nu
        # The extension-count equations follow from the K4 -> K3 face
        # marginal.  The integer matrix below is the deduplicated set of all
        # 609 oriented, centered extension-sum equations.
        constraints.append(
            data["centered_matrix"][:, : len(triples)] @ nu
            + data["centered_matrix"][:, len(triples) :] @ k4
            == 0
        )

    problem = cp.Problem(cp.Maximize(margin), constraints)
    options = {}
    if solver == "SCS":
        options = {
            "eps": 2e-7,
            "max_iters": 1_000_000,
            "normalize": True,
            "acceleration_lookback": 10,
        }
    elif level in ("triple", "edge", "full"):
        # The exact centering identities force large kernels in every Schur
        # block.  Clarabel's default 1e-8 feasibility target can terminate
        # with NumericalError on this deliberately singular system even when
        # the residual is already around 1e-6.
        options = {
            "tol_feas": 2e-7,
            "tol_gap_abs": 2e-7,
            "tol_gap_rel": 2e-7,
            "max_iter": 500,
        }
    value = problem.solve(solver=solver, verbose=verbose, **options)

    report = {
        "schema": "kissing5.centered_quarter_k4_full_centering_search.v1",
        "status": problem.status,
        "solver": solver,
        "level": level,
        "objective_pair_triple_margin": (
            None if value is None else float(value)
        ),
        "labeled_psd_k4": data["labeled"],
        "k4_orbit_count": len(orbits),
        "ordered_triangle_type_count": len(data["oriented_types"]),
        "distinct_centered_k3_rows": len(data["centered_matrix"]),
        "edge_kernel_conditions": (
            "implied by K2/K3 and K3/K4 pointwise centering"
            if level == "full"
            else "explicit" if level == "edge" else "diagnostic only"
        ),
    }
    if alpha.value is not None:
        alpha_value = np.array(alpha.value)
        nu_value = np.array(nu.value)
        k4_value = np.array(k4.value)
        report.update(
            {
                "minimum_alpha": float(np.min(alpha_value)),
                "minimum_nu": float(np.min(nu_value)),
                "minimum_k4": float(np.min(k4_value)),
                "positive_k4_orbits_at_1e-9": int(
                    np.sum(k4_value > 1e-9)
                ),
                "alpha": alpha_value.tolist(),
                "nu": nu_value.tolist(),
                "k4": k4_value.tolist(),
            }
        )

        # Independent residual summaries, evaluated from the returned arrays.
        equality_residuals = [
            abs(np.sum(alpha_value) - (size - 1)),
            abs(1 + grid @ alpha_value),
            float(
                np.max(
                    np.abs(
                        data["pair_marginal"] @ nu_value
                        - (size - 2) * alpha_value
                    )
                )
            ),
            float(
                np.max(
                    np.abs(
                        data["face_incidence"] @ k4_value
                        - 4
                        * nu_value
                        / ((size - 1) * (size - 2))
                    )
                )
            ),
        ]
        if level in ("triple", "edge", "full"):
            base_mass_value = data["oriented_mass"] @ nu_value
            equality_residuals.append(
                float(
                    np.max(
                        np.abs(
                            flag_factor
                            * data["extension_count"]
                            @ k4_value
                            - (size - 3) * base_mass_value
                        )
                    )
                )
            )
            for center in range(3):
                target = []
                for first, second, third in data["oriented_types"]:
                    incident = (
                        (first, second)
                        if center == 0
                        else (first, third)
                        if center == 1
                        else (second, third)
                    )
                    target.append(
                        -1 - grid[incident[0]] - grid[incident[1]]
                    )
                equality_residuals.append(
                    float(
                        np.max(
                            np.abs(
                                flag_factor
                                * data["extension_sum"][:, center, :]
                                @ k4_value
                                - np.array(target) * base_mass_value
                            )
                        )
                    )
                )
        report["maximum_linear_equality_residual"] = max(
            equality_residuals
        )

        # Rebuild the numerical flag blocks without trusting CVXPY values.
        vertex_first_value = alpha_value
        vertex_second_value = np.diag(alpha_value) + (
            data["vertex_distinct"].reshape(
                len(grid) * len(grid), len(triples)
            )
            @ nu_value
        ).reshape((len(grid), len(grid)))
        vertex_numeric = np.block(
            [
                [vertex_second_value, vertex_first_value[:, None]],
                [vertex_first_value[None, :], np.ones((1, 1))],
            ]
        )
        report["minimum_vertex_block_eigenvalue"] = float(
            np.linalg.eigvalsh(vertex_numeric)[0]
        )
        vertex_kernel_residual = 0.0
        for kernel in (
            np.r_[np.ones(len(grid)), -(size - 1)],
            np.r_[grid, 1.0],
        ):
            vertex_kernel_residual = max(
                vertex_kernel_residual,
                float(np.max(np.abs(vertex_numeric @ kernel))),
            )
        report["maximum_vertex_kernel_residual"] = vertex_kernel_residual

        minimum_edge_eigenvalue = math.inf
        maximum_edge_kernel_residual = 0.0
        for q in range(len(grid)):
            first_value = data["edge_first"][q] @ nu_value
            distinct_value = flag_factor * (
                data["edge_flag"][q].reshape(
                    len(categories) * len(categories), len(orbits)
                )
                @ k4_value
            ).reshape((len(categories), len(categories)))
            second_value = np.diag(first_value) + distinct_value
            edge_numeric = np.block(
                [
                    [second_value, first_value[:, None]],
                    [first_value[None, :], alpha_value[q : q + 1, None]],
                ]
            )
            minimum_edge_eigenvalue = min(
                minimum_edge_eigenvalue,
                float(np.linalg.eigvalsh(edge_numeric)[0]),
            )
            for kernel in edge_kernels[q]:
                maximum_edge_kernel_residual = max(
                    maximum_edge_kernel_residual,
                    float(np.max(np.abs(edge_numeric @ kernel))),
                )
        report["minimum_ordered_edge_block_eigenvalue"] = (
            minimum_edge_eigenvalue
        )
        report["maximum_ordered_edge_kernel_residual"] = (
            maximum_edge_kernel_residual
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ("alpha", "nu", "k4")},
                     indent=2, sort_keys=True))
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--level",
        choices=("baseline", "pair", "vertex", "triple", "edge", "full"),
        default="full",
    )
    parser.add_argument(
        "--solver", choices=("CLARABEL", "SCS"), default="CLARABEL"
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    default_output = (
        Path(__file__).resolve().parent
        / "results"
        / f"{args.level.lower()}_{args.solver.lower()}.json"
    )
    solve(args.level, args.solver, args.verbose, args.output or default_output)


if __name__ == "__main__":
    main()
