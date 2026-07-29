#!/usr/bin/env python3
"""Diagnose which exact-relation strata attract the full-coefficient runs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from d6_weyl_full_coeff_search import D, FullCoefficientModel


def analyze_record(
    model: FullCoefficientModel, payload: dict[str, object]
) -> dict[str, object]:
    coefficients = np.asarray(payload["coefficient_matrix"], dtype=float)
    h = model.h_from_coefficients(coefficients)
    eigenvalues = np.linalg.eigvalsh(h)

    # Balanced scalar-involution stratum: spectrum {-s,+s}, multiplicity 18.
    s_balanced = float(np.mean(eigenvalues[-18:]))
    k_balanced = h / s_balanced
    k1 = np.kron(k_balanced, np.eye(D))
    k2 = np.kron(np.eye(D), k_balanced)
    balanced_involution = np.linalg.norm(
        k_balanced @ k_balanced - np.eye(D * D)
    )
    balanced_anticommutator = np.linalg.norm(k1 @ k2 + k2 @ k1)

    # Weyl-cubic stratum: spectrum {-sqrt(3),1/sqrt(3)} after scaling.
    t_weyl = float(np.mean(eigenvalues[-27:]) * np.sqrt(3))
    k_weyl = h / t_weyl
    _, weyl_involution, weyl_cubic = model.residuals(
        coefficients / t_weyl
    )
    weyl_minpoly = (
        3 * k_weyl @ k_weyl
        + 2 * np.sqrt(3) * k_weyl
        - 3 * np.eye(D * D)
    )

    final_weight = float(payload["weights"][-1])
    x_balanced = s_balanced**2
    balanced_stationarity = (
        x_balanced
        - 1
        + final_weight
        * (x_balanced - 1 / 3)
        * (3 * x_balanced - 1 / 3)
    )
    x_weyl = t_weyl**2
    weyl_stationarity = (
        14 * x_weyl / 3
        - 2
        + 2
        * final_weight
        * (3 * x_weyl**2 - 4 * x_weyl + 1)
        / 9
    )

    if (
        balanced_involution < 1e-4
        and balanced_anticommutator < 1e-3
    ):
        classification = "scaled_adjacent_anticommuting_involution"
    elif (
        np.linalg.norm(weyl_cubic) < 1e-5
        and np.linalg.norm(weyl_minpoly) < 1e-5
    ):
        classification = "scaled_weyl_cubic_wrong_quadratic"
    else:
        classification = "other"

    return {
        "seed": payload["seed"],
        "initialization": payload["initialization"],
        "final_weight": final_weight,
        "classification": classification,
        "reported_involution_norm": payload["final"]["involution_norm"],
        "reported_cubic_norm": payload["final"]["cubic_norm"],
        "coefficient_rank_tolerance_1e-8": payload["final"][
            "coefficient_rank_tolerance_1e-8"
        ],
        "balanced_test": {
            "scale_s": s_balanced,
            "normalized_involution_norm": float(balanced_involution),
            "normalized_adjacent_anticommutator_norm": float(
                balanced_anticommutator
            ),
            "scalar_stationarity_residual": float(balanced_stationarity),
        },
        "weyl_test": {
            "scale_t": t_weyl,
            "normalized_involution_norm": float(
                np.linalg.norm(weyl_involution)
            ),
            "normalized_cubic_norm": float(np.linalg.norm(weyl_cubic)),
            "normalized_wrong_minpoly_norm": float(
                np.linalg.norm(weyl_minpoly)
            ),
            "scalar_stationarity_residual": float(weyl_stationarity),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    model = FullCoefficientModel.build()
    records = [
        json.loads(line)
        for line in args.input.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    diagnostics = [analyze_record(model, record) for record in records]
    counts: dict[str, int] = {}
    for row in diagnostics:
        classification = str(row["classification"])
        counts[classification] = counts.get(classification, 0) + 1
    payload = {
        "input": str(args.input),
        "number_of_runs": len(records),
        "classification_counts": counts,
        "runs": diagnostics,
        "warning": "Numerical diagnostics only; classifications use tolerances.",
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    print(rendered)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
