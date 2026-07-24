#!/usr/bin/env python3
"""Numerical discovery model for a degree-13 conditional/BV obstruction.

This is floating-point search code, not a verifier.  It uses exact
conditional identities to remove the forced kernels from the degree-zero,
one, and two radial blocks, then maximizes a common eigenvalue margin.
Dual values are recorded to support later exact rational reconstruction.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import importlib.util
import itertools
import json
from pathlib import Path
import sys

import cvxpy as cp
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PAIR_SOURCE = (
    HERE.parent
    / "centered_tight_frame_endpoint"
    / "centered_tight_bv_pseudodistribution.json"
)
RATIONALIZATION = HERE / "conditional_bv_degree12_rationalization.json"

sys.path.insert(0, str(ROOT / "experiments" / "continuous_rank_bv_search"))
import search as shared  # noqa: E402

VERIFIER_PATH = HERE / "verify_conditional_bv_degree12.py"
SPECIFICATION = importlib.util.spec_from_file_location(
    "verify_conditional_bv_degree12", VERIFIER_PATH
)
assert SPECIFICATION is not None and SPECIFICATION.loader is not None
exact = importlib.util.module_from_spec(SPECIFICATION)
SPECIFICATION.loader.exec_module(exact)


def coefficient_blocks(
    nodes: list[Q],
    alpha: list[Q],
    triples: list[tuple[int, int, int]],
    maximum_degree: int,
) -> dict[int, tuple[np.ndarray, np.ndarray, list[int]]]:
    """Return constant, orbit-coefficient, and complement data."""

    orbit_count = len(triples)
    index_of = {node: index for index, node in enumerate(nodes)}
    blocks: dict[int, tuple[np.ndarray, np.ndarray, list[int]]] = {}

    constant = np.zeros((12, 12))
    coefficients = np.zeros((orbit_count, 12, 12))
    for i, weight in enumerate(alpha):
        constant[i, i] = float(weight)
        constant[i, 11] = float(weight)
        constant[11, i] = float(weight)
    constant[11, 11] = 1
    for orbit_index, triple in enumerate(triples):
        values = tuple(nodes[index] for index in triple)
        orbit = sorted(set(itertools.permutations(values)))
        coefficient = 1 / len(orbit)
        for u, v, _t in orbit:
            coefficients[
                orbit_index, index_of[u], index_of[v]
            ] += coefficient
    complement = list(range(3, 12))
    blocks[0] = (
        constant[np.ix_(complement, complement)],
        coefficients[:, complement][:, :, complement],
        complement,
    )

    maximum_index = (maximum_degree + 1) // 2
    exact_coefficient_matrices: dict[
        tuple[Q, Q], list[list[list[Q]]]
    ] = {}
    # The value above is awkward to store orbitwise.  Build the transverse
    # sequences directly for each ordered occurrence instead.
    del exact_coefficient_matrices
    ordered: list[tuple[int, int, int, Q, Q, Q]] = []
    for orbit_index, triple in enumerate(triples):
        values = tuple(nodes[index] for index in triple)
        orbit = sorted(set(itertools.permutations(values)))
        coefficient = Q(1, len(orbit))
        for u, v, t in orbit:
            ordered.append(
                (
                    orbit_index,
                    index_of[u],
                    index_of[v],
                    coefficient,
                    (1 - u * u) * (1 - v * v),
                    t - u * v,
                )
            )
    sequences = {
        (area, displacement): exact.normalized_transverse_sequences(
            area, displacement, maximum_index
        )
        for _orbit, _i, _j, _coefficient, area, displacement in ordered
    }
    for degree in range(1, maximum_degree + 1):
        constant = np.zeros((11, 11))
        coefficients = np.zeros((orbit_count, 11, 11))
        for i, node in enumerate(nodes):
            diagonal = alpha[i]
            if degree % 2:
                diagonal *= 1 - node * node
            constant[i, i] = float(diagonal)
        parity = degree % 2
        sequence_index = degree // 2
        for (
            orbit_index,
            i,
            j,
            coefficient,
            area,
            displacement,
        ) in ordered:
            kernel = sequences[(area, displacement)][parity][
                sequence_index
            ]
            coefficients[orbit_index, i, j] += float(
                coefficient * kernel
            )
        if degree == 1:
            complement = list(range(2, 11))
        elif degree == 2:
            complement = list(range(1, 11))
        else:
            complement = list(range(11))
        blocks[degree] = (
            constant[np.ix_(complement, complement)],
            coefficients[:, complement][:, :, complement],
            complement,
        )
    return blocks


def parse_indices(text: str, upper: int) -> list[int]:
    if text == "all":
        return list(range(upper))
    if text == "none":
        return []
    answer = [int(value) for value in text.split(",") if value]
    assert len(answer) == len(set(answer))
    assert all(0 <= value < upper for value in answer)
    return answer


def serializable(value):
    if value is None:
        return None
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    return value


def solve(
    maximum_degree: int,
    capacity_indices_text: str,
    output_path: Path | None,
) -> dict[str, object]:
    source = json.loads(PAIR_SOURCE.read_text())
    reconstruction = json.loads(RATIONALIZATION.read_text())
    nodes = [Q(value) for value in source["nodes"]]
    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(value) for value in source["triple_orbits"]]
    rows = exact.conditional_rows(nodes, triples, alpha)
    independent_rows = reconstruction["independent_rows"]
    equality_matrix = np.array(
        [
            [float(value) for value in rows[index][0]]
            for index in independent_rows
        ]
    )
    equality_target = np.array(
        [float(rows[index][1]) for index in independent_rows]
    )

    capacity_rows = shared.stratified_capacity_rows(nodes, triples)
    selected_capacity_indices = parse_indices(
        capacity_indices_text, len(capacity_rows)
    )
    selected_capacity_rows = [
        capacity_rows[index] for index in selected_capacity_indices
    ]

    blocks = coefficient_blocks(
        nodes, alpha, triples, maximum_degree
    )
    orbit_count = len(triples)
    nu = cp.Variable(orbit_count)
    margin = cp.Variable()
    nonnegative_constraint = nu >= 0
    equality_constraint = equality_matrix @ nu == equality_target
    margin_lower = margin >= -1
    margin_upper = margin <= 1
    constraints = [
        nonnegative_constraint,
        equality_constraint,
        margin_lower,
        margin_upper,
    ]

    capacity_constraints = []
    for row in selected_capacity_rows:
        constraint = (
            np.array(row["nu_coefficients"], dtype=float) @ nu
            <= float(
                3
                * row["capacity"]
                * sum(alpha[i] for i in row["alpha_indices"])
            )
        )
        constraints.append(constraint)
        capacity_constraints.append(constraint)

    block_constraints: dict[int, cp.Constraint] = {}
    for degree, (constant, coefficients, _complement) in blocks.items():
        size = constant.shape[0]
        matrix = cp.reshape(
            coefficients.reshape(orbit_count, size * size).T @ nu
            + constant.reshape(size * size),
            (size, size),
            order="C",
        )
        constraint = matrix - margin * np.eye(size) >> 0
        constraints.append(constraint)
        block_constraints[degree] = constraint

    problem = cp.Problem(cp.Maximize(margin), constraints)
    problem.solve(
        solver="CLARABEL",
        max_iter=1000,
        tol_gap_abs=1e-10,
        tol_gap_rel=1e-10,
        tol_feas=1e-10,
        verbose=False,
    )
    result: dict[str, object] = {
        "schema": "centered-tight-degree13-reduced-discovery-v1",
        "scope": "FLOATING-POINT DISCOVERY ONLY; NOT A CERTIFICATE",
        "status": problem.status,
        "maximum_degree": maximum_degree,
        "capacity_indices": selected_capacity_indices,
        "objective_margin": (
            None if problem.value is None else float(problem.value)
        ),
        "nu": None if nu.value is None else nu.value.tolist(),
        "dual_nonnegative": serializable(
            nonnegative_constraint.dual_value
        ),
        "dual_equalities": serializable(
            equality_constraint.dual_value
        ),
        "dual_margin_lower": serializable(margin_lower.dual_value),
        "dual_margin_upper": serializable(margin_upper.dual_value),
        "dual_capacities": [
            serializable(constraint.dual_value)
            for constraint in capacity_constraints
        ],
        "dual_blocks": {
            str(degree): serializable(constraint.dual_value)
            for degree, constraint in block_constraints.items()
        },
        "block_complements": {
            str(degree): complement
            for degree, (_constant, _coefficients, complement)
            in blocks.items()
        },
    }
    if output_path is not None:
        output_path.write_text(json.dumps(result, indent=2) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-degree", type=int, default=13)
    parser.add_argument(
        "--capacity-indices",
        default="all",
        help="'all', 'none', or a comma-separated list of row indices",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    print(
        json.dumps(
            solve(
                args.maximum_degree,
                args.capacity_indices,
                args.output,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
