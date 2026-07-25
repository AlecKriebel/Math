#!/usr/bin/env python3
"""Discover and write an exact rational degree-13 dual certificate.

This program consumes floating-point dual matrices, replaces them by
rational Gram factors, repairs the equality multipliers with a small LP,
and accepts output only after exact rational sign checks.  The separate
standard-library verifier does not import NumPy, CVXPY, or this script.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import cvxpy as cp
import numpy as np


HERE = Path(__file__).resolve().parent
DISCOVERY = HERE / "degree13_reduced_discovery.json"
OUTPUT = HERE / "fixed_atomic_degree13_dual_certificate.json"

VERIFIER_PATH = HERE / "verify_fixed_atomic_degree13_obstruction.py"
SPECIFICATION = importlib.util.spec_from_file_location(
    "verify_fixed_atomic_degree13_obstruction", VERIFIER_PATH
)
assert SPECIFICATION is not None and SPECIFICATION.loader is not None
verifier = importlib.util.module_from_spec(SPECIFICATION)
SPECIFICATION.loader.exec_module(verifier)
Q = verifier.Q


def main() -> None:
    discovery_bytes = DISCOVERY.read_bytes()
    discovery = json.loads(discovery_bytes)
    assert discovery["schema"] == (
        "centered-tight-degree13-reduced-discovery-v1"
    )
    assert discovery["maximum_degree"] == 13
    assert discovery["capacity_indices"] == list(range(48))
    assert discovery["objective_margin"] < 0

    source_bytes = verifier.PAIR_SOURCE.read_bytes()
    source = json.loads(source_bytes)
    nodes = [Q(value) for value in source["nodes"]]
    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(value) for value in source["triple_orbits"]]
    all_rows = verifier.helper.conditional_rows(nodes, triples, alpha)
    reconstruction = json.loads(
        (HERE / "conditional_bv_degree12_rationalization.json").read_text()
    )
    row_indices = [
        int(index) for index in reconstruction["independent_rows"]
    ]
    equality_rows = [all_rows[index] for index in row_indices]

    complements = verifier.expected_complements()
    factor_denominator = 10**10
    eigenvalue_threshold = 10**-7
    factors_by_degree: dict[int, list[list[Q]]] = {}
    for degree in range(14):
        numerical_matrix = np.array(
            discovery["dual_blocks"][str(degree)], dtype=float
        )
        eigenvalues, eigenvectors = np.linalg.eigh(numerical_matrix)
        factors = []
        for index, eigenvalue in enumerate(eigenvalues):
            if eigenvalue <= eigenvalue_threshold:
                continue
            vector = (
                np.sqrt(eigenvalue) * eigenvectors[:, index]
            )
            rational = [
                Q(round(value * factor_denominator), factor_denominator)
                for value in vector
            ]
            if any(rational):
                factors.append(rational)
        if factors:
            factors_by_degree[degree] = factors
    assert {
        degree: len(factors)
        for degree, factors in factors_by_degree.items()
    } == {
        0: 2,
        1: 3,
        2: 3,
        3: 3,
        4: 2,
        5: 1,
        7: 1,
        8: 1,
        9: 1,
        13: 1,
    }

    capacity_denominator = 10**10
    active_capacity_indices = [27, 33, 38, 42, 43, 45]
    capacity_dual = [Q(0)] * 48
    for index in active_capacity_indices:
        capacity_dual[index] = Q(
            round(
                discovery["dual_capacities"][index]
                * capacity_denominator
            ),
            capacity_denominator,
        )
    assert all(value > 0 for value in capacity_dual if value)

    radial_coefficients, radial_constant = (
        verifier.dual_coefficients(
            nodes,
            alpha,
            triples,
            factors_by_degree,
            complements,
        )
    )
    capacity_rows = verifier.exact_capacity_rows(
        nodes, alpha, triples
    )
    capacity_coefficients = [
        sum(
            capacity_dual[index] * capacity_rows[index][0][orbit]
            for index in range(48)
        )
        for orbit in range(len(triples))
    ]
    capacity_constant = sum(
        capacity_dual[index] * capacity_rows[index][1]
        for index in range(48)
    )

    equality_matrix = np.array(
        [
            [float(value) for value in row[0]]
            for row in equality_rows
        ]
    )
    equality_target = np.array(
        [float(row[1]) for row in equality_rows]
    )
    base_slacks = np.array(
        [
            float(
                capacity_coefficients[orbit]
                - radial_coefficients[orbit]
            )
            for orbit in range(len(triples))
        ]
    )
    fixed_constant = float(radial_constant + capacity_constant)
    equality_dual_variable = cp.Variable(len(equality_rows))
    minimum_slack_variable = cp.Variable()
    target_objective = 3e-6
    problem = cp.Problem(
        cp.Maximize(minimum_slack_variable),
        [
            base_slacks
            + equality_matrix.T @ equality_dual_variable
            >= minimum_slack_variable,
            fixed_constant
            + equality_target @ equality_dual_variable
            <= -target_objective,
        ],
    )
    problem.solve(
        solver="CLARABEL",
        max_iter=1000,
        tol_gap_abs=1e-12,
        tol_gap_rel=1e-12,
        tol_feas=1e-12,
        verbose=False,
    )
    assert equality_dual_variable.value is not None

    equality_denominator = 10**15
    equality_dual = [
        Q(round(value * equality_denominator), equality_denominator)
        for value in equality_dual_variable.value
    ]
    orbit_slacks = [
        capacity_coefficients[orbit]
        - radial_coefficients[orbit]
        + sum(
            equality_dual[index]
            * equality_rows[index][0][orbit]
            for index in range(len(equality_rows))
        )
        for orbit in range(len(triples))
    ]
    dual_objective = (
        radial_constant
        + capacity_constant
        + sum(
            dual * row[1]
            for dual, row in zip(equality_dual, equality_rows)
        )
    )
    assert all(slack > 0 for slack in orbit_slacks)
    assert dual_objective < 0

    certificate = {
        "schema": "centered-tight-fixed-atomic-degree13-dual-v1",
        "status": (
            "EXACT DUAL CERTIFICATE FOR A FIXED ATOM TABLE; "
            "NOT A UNIVERSAL CODE OBSTRUCTION"
        ),
        "scope_warning": (
            "the eleven nodes and their pair multiplicities are assumptions"
        ),
        "maximum_bv_degree": 13,
        "source_pair_certificate": verifier.PAIR_SOURCE.name,
        "source_pair_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "source_discovery": DISCOVERY.name,
        "source_discovery_sha256": hashlib.sha256(
            discovery_bytes
        ).hexdigest(),
        "conditional_row_indices": row_indices,
        "factor_denominator": factor_denominator,
        "block_complements": {
            str(degree): complement
            for degree, complement in complements.items()
        },
        "block_factor_numerators": {
            str(degree): [
                [
                    int(value * factor_denominator)
                    for value in factor
                ]
                for factor in factors
            ]
            for degree, factors in factors_by_degree.items()
        },
        "capacity_dual_denominator": capacity_denominator,
        "capacity_dual_numerators": {
            str(index): int(
                capacity_dual[index] * capacity_denominator
            )
            for index in active_capacity_indices
        },
        "equality_dual_denominator": equality_denominator,
        "equality_dual_numerators": [
            int(value * equality_denominator)
            for value in equality_dual
        ],
        "exact_minimum_orbit_slack": str(min(orbit_slacks)),
        "exact_dual_objective": str(dual_objective),
        "rationalization": {
            "eigenvalue_threshold": eigenvalue_threshold,
            "target_dual_objective_upper_bound": -target_objective,
            "floating_repair_status": problem.status,
            "floating_repair_minimum_slack": float(problem.value),
        },
    }
    OUTPUT.write_text(json.dumps(certificate, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": "WROTE EXACT CERTIFICATE",
                "output": str(OUTPUT),
                "minimum_orbit_slack": str(min(orbit_slacks)),
                "dual_objective": str(dual_objective),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
