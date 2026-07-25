#!/usr/bin/env python3
"""Discovery search for a type-conditional centered/tight BV witness.

This program uses floating-point SDP.  Its output is not a certificate.
The intended exact verifier is separate and uses only rational arithmetic.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import itertools
import json
from pathlib import Path
import sys

import cvxpy as cp
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "continuous_rank_bv_search"))
import search as shared  # noqa: E402


def transverse_value(area: float, displacement: float, degree: int) -> float:
    if degree == 0:
        return 1.0
    if degree == 1:
        return displacement
    transformed = 4 * displacement * displacement / area - 2
    even = [1.0, (4 * displacement * displacement / area - 1) / 3]
    odd = [
        displacement,
        2 * displacement**3 / area - displacement,
    ]
    sequence = odd if degree % 2 else even
    while len(sequence) <= degree // 2:
        current = 2 * (len(sequence) - 1) + (degree % 2)
        sequence.append(
            (
                transformed * (current + 1) * sequence[-1]
                - (current - 1) * sequence[-2]
            )
            / (current + 3)
        )
    return sequence[degree // 2]


def conditional_rows(nodes, triples, alpha):
    rows = [([Q(1)] * len(triples), Q(1560), "total")]
    for base_index, base in enumerate(nodes):
        coefficients = [[], [], [], []]
        for triple in triples:
            values = tuple(nodes[index] for index in triple)
            orbit = sorted(set(itertools.permutations(values)))
            accumulators = [Q(0)] * 4
            for u, v, t in orbit:
                if t == base:
                    accumulators[0] += 1
                    accumulators[1] += u
                    accumulators[2] += u * u
                    accumulators[3] += u * v
            for row, value in zip(
                coefficients,
                (value / len(orbit) for value in accumulators),
            ):
                row.append(value)
        targets = (
            39 * alpha[base_index],
            alpha[base_index] * (-1 - base),
            alpha[base_index] * (Q(36, 5) - base * base),
            alpha[base_index] * Q(31, 5) * base,
        )
        for name, row, target in zip(
            ("mass", "first", "square", "cross"),
            coefficients,
            targets,
        ):
            rows.append((row, target, f"{base_index}:{name}"))
    return rows


def solve(
    maximum_degree: int,
    output_path: Path | None,
    solver: str = "CLARABEL",
) -> dict:
    source = json.loads(
        (
            ROOT
            / "experiments"
            / "centered_tight_frame_endpoint"
            / "centered_tight_bv_pseudodistribution.json"
        ).read_text()
    )
    nodes = tuple(Q(value) for value in source["nodes"])
    alpha = tuple(Q(value) for value in source["alpha"])
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    size = len(nodes)
    nu = cp.Variable(len(triples), nonneg=True)
    margin = cp.Variable()
    constraints = [margin >= -1, margin <= 1]

    for row, target, _name in conditional_rows(nodes, triples, alpha):
        constraints.append(
            np.array([float(value) for value in row]) @ nu
            == float(target)
        )

    capacity_rows = shared.stratified_capacity_rows(nodes, triples)
    for row in capacity_rows:
        constraints.append(
            np.array(row["nu_coefficients"], dtype=float) @ nu
            <= float(
                3
                * row["capacity"]
                * sum(alpha[i] for i in row["alpha_indices"])
            )
        )
    weighted_rows = shared.weighted_capacity_rows(nodes, triples)
    for row in weighted_rows:
        constraints.append(
            np.array(row["nu_coefficients"], dtype=float) @ nu
            <= float(
                3
                * sum(
                    capacity * alpha[index]
                    for index, capacity in row["capacities"].items()
                )
            )
        )

    index_of = {node: index for index, node in enumerate(nodes)}
    terms = []
    for orbit_index, triple in enumerate(triples):
        values = tuple(nodes[index] for index in triple)
        orbit = sorted(set(itertools.permutations(values)))
        coefficient = 1 / len(orbit)
        for u, v, t in orbit:
            area = float((1 - u * u) * (1 - v * v))
            displacement = float(t - u * v)
            terms.append(
                (
                    orbit_index,
                    index_of[u],
                    index_of[v],
                    coefficient,
                    area,
                    displacement,
                )
            )

    full_zero = np.zeros((size + 1, size + 1), dtype=object)
    for i, weight in enumerate(alpha):
        full_zero[i][i] = float(weight)
        full_zero[i][-1] = float(weight)
        full_zero[-1][i] = float(weight)
    full_zero[-1][-1] = 1.0
    for orbit_index, i, j, coefficient, _area, _displacement in terms:
        full_zero[i][j] += coefficient * nu[orbit_index]
    full_zero = cp.bmat(full_zero.tolist())

    zero_kernels = np.column_stack(
        (
            np.r_[[-1 / 40] * size, 1],
            np.r_[[float(node) for node in nodes], 1],
            np.r_[
                [float(node * node - Q(1, 5)) for node in nodes],
                float(Q(4, 5)),
            ],
        )
    )
    zero_basis = np.linalg.qr(zero_kernels, mode="complete")[0][:, 3:]
    constraints.extend(
        (
            full_zero >> 0,
            zero_basis.T @ full_zero @ zero_basis
            >> margin * np.eye(size - 2),
        )
    )

    for degree in range(1, maximum_degree + 1):
        matrix = np.zeros((size, size), dtype=object)
        for i, node in enumerate(nodes):
            matrix[i][i] = float(
                alpha[i] * (1 - node * node)
                if degree % 2
                else alpha[i]
            )
        for orbit_index, i, j, coefficient, area, displacement in terms:
            matrix[i][j] += (
                coefficient
                * transverse_value(area, displacement, degree)
                * nu[orbit_index]
            )
        matrix = cp.bmat(matrix.tolist())
        if degree == 1:
            kernels = np.column_stack(
                (np.ones(size), np.array([float(node) for node in nodes]))
            )
            basis = np.linalg.qr(kernels, mode="complete")[0][:, 2:]
        elif degree == 2:
            kernel = np.array(
                [float(1 - node * node) for node in nodes]
            )[:, None]
            basis = np.linalg.qr(kernel, mode="complete")[0][:, 1:]
        else:
            basis = np.eye(size)
        constraints.extend(
            (
                matrix >> 0,
                basis.T @ matrix @ basis
                >> margin * np.eye(basis.shape[1]),
            )
        )

    problem = cp.Problem(cp.Maximize(margin), constraints)
    try:
        if solver.upper() == "SCS":
            raise cp.error.SolverError("SCS requested")
        problem.solve(
            solver="CLARABEL",
            max_iter=500,
            tol_gap_abs=1e-8,
            tol_gap_rel=1e-8,
            tol_feas=1e-8,
            verbose=False,
        )
    except cp.error.SolverError:
        problem.solve(
            solver="SCS",
            eps=2e-6,
            max_iters=200000,
            acceleration_lookback=20,
            verbose=False,
        )
    record = {
        "schema": "conditional-tight-bv-discovery-v1",
        "status": problem.status,
        "maximum_harmonic_degree": maximum_degree,
        "solver": solver,
        "margin": None if problem.value is None else float(problem.value),
        "nu": None if nu.value is None else nu.value.tolist(),
        "scope": "floating discovery only; not a matrix or certificate",
    }
    if output_path is not None:
        output_path.write_text(json.dumps(record, indent=2) + "\n")
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, default=8)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--solver", choices=("CLARABEL", "SCS"), default="CLARABEL")
    args = parser.parse_args()
    print(json.dumps(solve(args.degree, args.output, args.solver), indent=2))


if __name__ == "__main__":
    main()
