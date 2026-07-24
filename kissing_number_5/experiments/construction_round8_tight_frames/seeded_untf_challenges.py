#!/usr/bin/env python3
"""UNTF searches seeded by D5-plus-one and the best known 41-point near-miss."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

import d5_basis_checker
import optimize_untf


HERE = Path(__file__).resolve().parent
INHERITED_PATH = (
    HERE.parent
    / "construction_round5_population"
    / "results"
    / "population_portfolio.json"
)
OUTPUT_PATH = HERE / "results" / "seeded_untf_challenges.json"


def optimize_seed(frame: np.ndarray) -> tuple[np.ndarray, list[dict]]:
    records = []
    projected = optimize_untf.project_untf(frame, 500)
    records.append(
        {
            "stage": "projected",
            **optimize_untf.frame_diagnostics(projected),
        }
    )
    optimized = optimize_untf.optimize_general(
        projected,
        [10, 20, 40, 80, 160, 320, 640, 1280],
        150,
    )
    records.append(
        {
            "stage": "continued",
            **optimize_untf.frame_diagnostics(optimized),
        }
    )
    optimized = optimize_untf.optimize_general(
        optimized,
        [1280, 2560, 5120, 10240],
        400,
    )
    records.append(
        {
            "stage": "polished",
            **optimize_untf.frame_diagnostics(optimized),
        }
    )
    return optimized, records


def main() -> None:
    seed = 528142
    rng = np.random.default_rng(seed)
    d5 = (
        np.asarray(d5_basis_checker.oriented_d5_roots(), dtype=float)
        / math.sqrt(2.0)
    )
    records = []
    best_frame = None
    best_value = math.inf

    extras = [
        np.eye(5)[index] for index in range(5)
    ]
    extras.append(np.ones(5) / math.sqrt(5.0))
    extras.extend(
        vector / np.linalg.norm(vector)
        for vector in rng.normal(size=(12, 5))
    )
    for index, extra in enumerate(extras):
        frame, stages = optimize_seed(np.vstack((d5, extra)))
        diagnostics = optimize_untf.frame_diagnostics(frame)
        records.append(
            {
                "source": "D5-plus-one",
                "index": index,
                "extra": extra.tolist(),
                "stages": stages,
                "final": diagnostics,
            }
        )
        print(
            f"D5-plus-one index={index} "
            f"max={diagnostics['maximum_inner_product']:.12f}",
            flush=True,
        )
        if diagnostics["maximum_inner_product"] < best_value:
            best_value = diagnostics["maximum_inner_product"]
            best_frame = frame.copy()

    inherited = json.loads(INHERITED_PATH.read_text())
    near_miss = np.asarray(
        inherited["runs"][0]["best"]["coordinates_float64"], dtype=float
    )
    frame, stages = optimize_seed(near_miss)
    diagnostics = optimize_untf.frame_diagnostics(frame)
    records.append(
        {
            "source": "inherited-N41-near-miss",
            "reported_source_maximum": inherited["runs"][0]["best"]["maximum"],
            "stages": stages,
            "final": diagnostics,
        }
    )
    print(
        f"inherited-near-miss max={diagnostics['maximum_inner_product']:.12f}",
        flush=True,
    )
    if diagnostics["maximum_inner_product"] < best_value:
        best_value = diagnostics["maximum_inner_product"]
        best_frame = frame.copy()

    assert best_frame is not None
    output = {
        "schema": "seeded-untf-41x5-challenges-v1",
        "status": "NUMERICAL EVIDENCE ONLY",
        "seed": seed,
        "records": records,
        "best": {
            **optimize_untf.frame_diagnostics(best_frame),
            "coordinates": best_frame.tolist(),
        },
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n")
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
