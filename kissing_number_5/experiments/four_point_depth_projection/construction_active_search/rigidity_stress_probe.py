#!/usr/bin/env python3
"""Numerical equilibrium-stress probe for the stored N=41 active core."""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import linprog


STATUS = "NUMERICAL EVIDENCE ONLY — NOT AN EXACT STRESS CERTIFICATE"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("rigidity_stress_probe.json"),
    )
    arguments = parser.parse_args()
    repository = Path(__file__).resolve().parents[3]
    source = repository / "experiments/input/spherical_codes_5_41.txt"
    x = np.loadtxt(source, delimiter=",")
    x /= np.linalg.norm(x, axis=1)[:, None]
    gram = x @ x.T
    np.fill_diagonal(gram, -np.inf)
    maximum = float(np.max(gram))
    edges = np.argwhere(np.triu(gram >= maximum - 1e-8, k=1))
    degrees = np.bincount(edges.ravel(), minlength=len(x))
    core_indices = np.flatnonzero(degrees > 0)
    core = x[core_indices]
    core_gram = core @ core.T
    np.fill_diagonal(core_gram, -np.inf)
    core_maximum = float(np.max(core_gram))
    core_edges = np.argwhere(
        np.triu(core_gram >= core_maximum - 1e-8, k=1)
    )

    # Column e=ij is the tangent gradient of <x_i,x_j>.
    gradient = np.zeros((len(core) * 5, len(core_edges)))
    for edge_index, (first, second) in enumerate(core_edges):
        product = float(core_gram[first, second])
        gradient[5 * first : 5 * (first + 1), edge_index] = (
            core[second] - product * core[first]
        )
        gradient[5 * second : 5 * (second + 1), edge_index] = (
            core[first] - product * core[second]
        )

    edge_count = len(core_edges)
    # Variables are edge weights and their common lower bound t.
    inequalities = np.zeros((edge_count, edge_count + 1))
    inequalities[np.arange(edge_count), np.arange(edge_count)] = -1.0
    inequalities[:, -1] = 1.0
    equalities = np.zeros((len(core) * 5 + 1, edge_count + 1))
    equalities[:-1, :-1] = gradient
    equalities[-1, :-1] = 1.0
    equality_rhs = np.zeros(len(core) * 5 + 1)
    equality_rhs[-1] = 1.0
    objective = np.zeros(edge_count + 1)
    objective[-1] = -1.0
    solution = linprog(
        objective,
        A_ub=inequalities,
        b_ub=np.zeros(edge_count),
        A_eq=equalities,
        b_eq=equality_rhs,
        bounds=[(0.0, None)] * edge_count + [(None, None)],
        method="highs",
        options={
            "dual_feasibility_tolerance": 1e-9,
            "primal_feasibility_tolerance": 1e-9,
        },
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    weights = solution.x[:-1]
    residual = gradient @ weights
    forces = residual.reshape(len(core), 5)
    singular_values = np.linalg.svd(gradient, compute_uv=False)
    result = {
        "status": STATUS,
        "source": str(source.relative_to(repository)),
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "active_tolerance": 1e-8,
        "maximum_inner_product": maximum,
        "active_core_indices": [int(value) for value in core_indices],
        "active_core_edge_count": int(edge_count),
        "active_core_edges": [
            [int(first), int(second)] for first, second in core_edges
        ],
        "edge_weights": [float(value) for value in weights],
        "minimum_weight": float(np.min(weights)),
        "maximum_weight": float(np.max(weights)),
        "weight_sum": float(np.sum(weights)),
        "equilibrium_residual_2norm": float(np.linalg.norm(residual)),
        "maximum_vertex_force_2norm": float(
            np.max(np.linalg.norm(forces, axis=1))
        ),
        "tangent_gradient_rank_binary64": int(
            np.linalg.matrix_rank(gradient)
        ),
        "stress_space_dimension_binary64": int(
            edge_count - np.linalg.matrix_rank(gradient)
        ),
        "smallest_gradient_singular_values": [
            float(value) for value in singular_values[-12:]
        ],
        "solver": {
            "success": bool(solution.success),
            "status": int(solution.status),
            "message": str(solution.message),
            "reported_common_lower_bound": float(solution.x[-1]),
        },
    }
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(
        f"edges={edge_count} min_weight={np.min(weights):.17g} "
        f"residual={np.linalg.norm(residual):.3g}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
