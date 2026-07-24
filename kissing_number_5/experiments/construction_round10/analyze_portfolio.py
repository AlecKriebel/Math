#!/usr/bin/env python3
"""Produce a compact, independently recomputed round-10 summary."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


PRIOR_NUMERICAL_BEST = {
    41: 0.5149946525121668,
    42: 0.5182411558622623,
    43: 0.5247096018290212,
    44: 0.5274577123235323,
}


def analyze_coordinates(raw: list[list[float]]) -> dict:
    x = np.asarray(raw, dtype=float)
    norms = np.linalg.norm(x, axis=1)
    x = x / norms[:, None]
    gram = x @ x.T
    ii, jj = np.triu_indices(len(x), 1)
    values = gram[ii, jj]
    maximum = float(np.max(values))
    maximizers = np.flatnonzero(values == maximum)
    exact_pairs = [
        [int(ii[index]), int(jj[index])] for index in maximizers
    ]
    return {
        "maximum_inner_product_binary64": maximum,
        "maximum_inner_product_float_hex": maximum.hex(),
        "exact_binary64_maximizing_pairs": exact_pairs,
        "pairs_within_1e-8_of_maximum": int(
            np.sum(values >= maximum - 1e-8)
        ),
        "unit_norm_residual_after_renormalization": float(
            np.max(np.abs(np.sum(x * x, axis=1) - 1.0))
        ),
        "coordinate_little_endian_float64_sha256": hashlib.sha256(
            np.asarray(x, dtype="<f8").tobytes()
        ).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    payload = json.loads(arguments.portfolio.read_text())
    if not payload.get("completed"):
        raise SystemExit("portfolio is not complete")
    summary: dict = {
        "evidence_status": "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE",
        "portfolio_sha256": hashlib.sha256(
            arguments.portfolio.read_bytes()
        ).hexdigest(),
        "structured_run_count": len(payload["structured_runs"]),
        "polished_run_count": len(payload["polished_runs"]),
        "best_by_n": {},
        "exact_or_certified_candidate_found": False,
    }
    for n in sorted(int(value) for value in payload["best_by_n"]):
        structured = [
            run for run in payload["structured_runs"] if run["n"] == n
        ]
        structured.sort(
            key=lambda run: run["structured_diagnostics"][
                "maximum_inner_product"
            ]
        )
        polished = [
            run for run in payload["polished_runs"] if run["n"] == n
        ]
        polished.sort(
            key=lambda run: run["final_diagnostics"]["maximum_inner_product"]
        )
        best_structured = structured[0]
        best_polished = polished[0]
        structured_analysis = analyze_coordinates(
            best_structured["structured_coordinates_float64"]
        )
        polished_analysis = analyze_coordinates(
            best_polished["coordinates_float64"]
        )
        root_type_histogram: dict[str, int] = {}
        for label in best_structured["selected_root_labels"]:
            kind = label["kind"]
            root_type_histogram[kind] = root_type_histogram.get(kind, 0) + 1
        value = polished_analysis["maximum_inner_product_binary64"]
        summary["best_by_n"][str(n)] = {
            "best_structured": {
                "family": best_structured["family"],
                "seed": best_structured["seed"],
                "root_type_histogram": root_type_histogram,
                "map_singular_values": best_structured[
                    "map_singular_values"
                ],
                "map_condition_number": (
                    best_structured["map_singular_values"][0]
                    / best_structured["map_singular_values"][-1]
                ),
                **structured_analysis,
            },
            "best_after_unrestricted_refinement": {
                "source_family": best_polished["source_family"],
                "source_seed": best_polished["source_seed"],
                "chosen_endpoint": best_polished["chosen_endpoint"],
                **polished_analysis,
            },
            "gap_above_one_half": value - 0.5,
            "difference_from_prior_numerical_best": (
                value - PRIOR_NUMERICAL_BEST[n]
            ),
            "meets_kissing_threshold_binary64": value <= 0.5,
        }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )


if __name__ == "__main__":
    main()
