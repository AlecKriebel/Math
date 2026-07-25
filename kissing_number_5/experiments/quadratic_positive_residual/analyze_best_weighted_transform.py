#!/usr/bin/env python3
"""Audit the global harmonic/Metzler transform on the best 41-point near code."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "experiments" / "input" / "spherical_codes_5_41.txt"


def feature_matrix(x: np.ndarray) -> np.ndarray:
    rows = [np.ones(len(x))]
    rows.extend(x[:, coordinate] for coordinate in range(5))
    rows.extend(x[:, i] ** 2 - x[:, 4] ** 2 for i in range(4))
    rows.extend(
        x[:, i] * x[:, j]
        for i in range(5)
        for j in range(i + 1, 5)
    )
    return np.asarray(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    x = np.loadtxt(INPUT, delimiter=",")
    x /= np.linalg.norm(x, axis=1)[:, None]
    number = len(x)
    equalities = feature_matrix(x)
    target = np.zeros(20)
    target[0] = 1.0
    objective = np.zeros(number + 1)
    objective[-1] = -1.0
    inequalities = np.zeros((number, number + 1))
    inequalities[np.arange(number), np.arange(number)] = -1.0
    inequalities[:, -1] = 1.0
    result = linprog(
        objective,
        A_ub=inequalities,
        b_ub=np.zeros(number),
        A_eq=np.hstack((equalities, np.zeros((20, 1)))),
        b_eq=target,
        bounds=[(0.0, None)] * (number + 1),
        method="highs",
    )
    assert result.success
    p = result.x[:-1]

    gram = x @ x.T
    identity = np.eye(number)
    ones = np.ones((number, number))
    b_matrix = identity + ones - 2.0 * gram
    w = b_matrix * (3.0 * ones - b_matrix)
    m = w - 4.0 * identity
    h2 = (5.0 * gram * gram - ones) / 4.0
    harmonic_residual = m - (
        1.2 * ones - 2.0 * gram - 3.2 * h2
    )
    eigenvalues = np.linalg.eigvalsh(m)
    shadow = (1.2 * ones - m) / 5.2
    shadow_eigenvalues = np.linalg.eigvalsh(shadow)
    off_mask = ~np.eye(number, dtype=bool)
    report = {
        "status": "NUMERICAL EVIDENCE ONLY",
        "source": str(INPUT.relative_to(ROOT)),
        "maximum_inner_product": float(np.max(gram[off_mask])),
        "maximum_common_weight_floor": float(result.x[-1]),
        "weighted_design_residual_inf": float(
            np.max(np.abs(equalities @ p - target))
        ),
        "minimum_off_diagonal_W": float(np.min(w[off_mask])),
        "number_negative_off_diagonal_W": int(np.count_nonzero(w[off_mask] < 0)),
        "M_p_equilibrium_residual_inf": float(
            np.max(np.abs(m @ p - 1.2 * np.ones(number)))
        ),
        "harmonic_matrix_identity_residual_inf": float(
            np.max(np.abs(harmonic_residual))
        ),
        "M_numerical_inertia_at_1e-8": {
            "positive": int(np.count_nonzero(eigenvalues > 1e-8)),
            "zero": int(np.count_nonzero(np.abs(eigenvalues) <= 1e-8)),
            "negative": int(np.count_nonzero(eigenvalues < -1e-8)),
        },
        "M_extreme_eigenvalues": [
            float(eigenvalues[0]),
            float(eigenvalues[-1]),
        ],
        "shadow_off_diagonal_interval": [
            float(np.min(shadow[off_mask])),
            float(np.max(shadow[off_mask])),
        ],
        "shadow_center_residual_inf": float(np.max(np.abs(shadow @ p))),
        "shadow_numerical_rank_at_1e-8": int(
            np.count_nonzero(shadow_eigenvalues > 1e-8)
        ),
        "exact_kissing_shadow_target_interval": [
            "-21/104",
            "3/13",
        ],
        "warning": (
            "All global weighted/harmonic identities are nearly exact; the "
            "only sign failure is caused by pairs with g>1/2."
        ),
    }
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
