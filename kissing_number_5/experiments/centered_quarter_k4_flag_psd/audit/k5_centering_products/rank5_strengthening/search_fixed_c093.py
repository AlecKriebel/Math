#!/usr/bin/env python3
"""K4 ordered-flag search with the all-harmonic C093 K2/K3 marginal fixed."""

from __future__ import annotations

from fractions import Fraction as Q
import json
import math
from pathlib import Path

import cvxpy as cp
import numpy as np

from experiments.centered_quarter_k4_flag_psd.audit.search_full_centering import (
    coefficients,
)


def main() -> None:
    root = Path(__file__).resolve().parents[5]
    folder = Path(__file__).resolve().parent
    source = json.loads(
        (
            root
            / "certificates/centered_quarter_bv_pseudodistribution.json"
        ).read_text()
    )
    data = coefficients(source)
    alpha_q = [Q(value) for value in source["alpha"]]
    nu_q = [Q(value) for value in source["nu"]]
    alpha = np.array([float(value) for value in alpha_q])
    nu = np.array([float(value) for value in nu_q])
    grid = np.array([float(value) for value in data["grid"]])
    categories = data["categories"]
    size = 41

    # Audit the K2 -> K3 pointwise centering rows exactly before solving.
    edge_first6 = np.rint(6 * data["edge_first"]).astype(np.int64)
    for color in range(7):
        first_q = [
            sum(
                (
                    Q(int(edge_first6[color, category, triple]), 6)
                    * nu_q[triple]
                    for triple in range(len(nu_q))
                ),
                Q(0),
            )
            for category in range(len(categories))
        ]
        assert sum(first_q) == 39 * alpha_q[color]
        assert sum(
            first_q[index] * Q(data["grid"][first])
            for index, (first, _) in enumerate(categories)
        ) == -(1 + Q(data["grid"][color])) * alpha_q[color]
        assert sum(
            first_q[index] * Q(data["grid"][second])
            for index, (_, second) in enumerate(categories)
        ) == -(1 + Q(data["grid"][color])) * alpha_q[color]

    k4 = cp.Variable(len(data["orbits"]), nonneg=True)
    margin = cp.Variable()
    constraints = [
        data["face_incidence"] @ k4 == nu / 390,
        data["centered_matrix"][:, len(nu) :] @ k4
        == -data["centered_matrix"][:, : len(nu)] @ nu,
        k4 >= margin,
    ]

    factor = math.comb(size, 4) / size
    edge_kernels = []
    for color in range(7):
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
                    np.array([[alpha[color]]]),
                ],
            ]
        )
        constraints.append(block >> 0)
        edge_kernels.append(
            (
                np.r_[np.ones(len(categories)), -39],
                np.r_[
                    [grid[first] for first, _ in categories],
                    1 + grid[color],
                ],
                np.r_[
                    [grid[second] for _, second in categories],
                    1 + grid[color],
                ],
            )
        )

    problem = cp.Problem(cp.Maximize(margin), constraints)
    value = problem.solve(
        solver="CLARABEL",
        tol_feas=2e-7,
        tol_gap_abs=2e-7,
        tol_gap_rel=2e-7,
        max_iter=500,
        verbose=True,
    )
    report = {
        "schema": "kissing5.k4_flag_fixed_c093_search.v1",
        "status": problem.status,
        "objective_minimum_k4_mass": (
            None if value is None else float(value)
        ),
        "fixed_marginal": (
            "C093 exact centered all-degree BV witness with its certified "
            "27 rank bands"
        ),
        "trace_g2": str(
            Q(41)
            * (
                1
                + sum(
                    mass * node * node
                    for mass, node in zip(
                        alpha_q, map(Q, source["grid"])
                    )
                )
            )
        ),
        "welch_bound": str(Q(1681, 5)),
    }
    if k4.value is not None:
        weights = np.array(k4.value)
        face_residual = data["face_incidence"] @ weights - nu / 390
        centered_residual = (
            data["centered_matrix"][:, len(nu) :] @ weights
            + data["centered_matrix"][:, : len(nu)] @ nu
        )
        minimum_eigenvalue = math.inf
        maximum_kernel_residual = 0.0
        for color in range(7):
            first = data["edge_first"][color] @ nu
            distinct = factor * (
                data["edge_flag"][color].reshape(
                    len(categories) * len(categories), len(data["orbits"])
                )
                @ weights
            ).reshape((len(categories), len(categories)))
            block = np.block(
                [
                    [np.diag(first) + distinct, first[:, None]],
                    [first[None, :], alpha[color : color + 1, None]],
                ]
            )
            minimum_eigenvalue = min(
                minimum_eigenvalue, np.linalg.eigvalsh(block)[0]
            )
            for kernel in edge_kernels[color]:
                maximum_kernel_residual = max(
                    maximum_kernel_residual,
                    float(np.max(np.abs(block @ kernel))),
                )
        report.update(
            {
                "minimum_k4_mass": float(np.min(weights)),
                "positive_k4_orbits_at_1e-10": int(
                    np.sum(weights > 1e-10)
                ),
                "maximum_face_residual": float(
                    np.max(np.abs(face_residual))
                ),
                "maximum_centered_k3_residual": float(
                    np.max(np.abs(centered_residual))
                ),
                "minimum_edge_block_eigenvalue": float(
                    minimum_eigenvalue
                ),
                "maximum_edge_kernel_residual": (
                    maximum_kernel_residual
                ),
                "k4": weights.tolist(),
            }
        )
    output = folder / "fixed_c093_search.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                key: value
                for key, value in report.items()
                if key != "k4"
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
