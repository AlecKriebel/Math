#!/usr/bin/env python3
"""Independent floating-point recomputation of construction-search output.

This audit detects serialization or reporting mistakes.  It does not turn
approximate coordinates into an exact construction or an impossibility
certificate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "construction_scan.json"


def family_data(name: str) -> tuple[np.ndarray, np.ndarray]:
    if name == "belt":
        return np.array([1.0, 1.0, 1.0, 1.0, -4.0]), np.zeros(5)
    if name == "two_caps":
        return np.array([-1.0, -1.0, -1.0, -1.0, 4.0]), np.zeros(5)
    if name == "shifted_cap":
        return (
            np.array([1.0, 1.0, 1.0, 1.0, -4.0]),
            np.array([0.0, 0.0, 0.0, 0.0, 5.0]),
        )
    raise AssertionError(f"unknown family: {name}")


def q_values(x: np.ndarray, diagonal: np.ndarray, linear: np.ndarray) -> np.ndarray:
    return np.sum(diagonal * x * x, axis=1) + x @ linear


def audit() -> dict[str, object]:
    payload = json.loads(RESULTS.read_text())
    assert payload["status"] == "NUMERICAL EVIDENCE ONLY"
    summaries: dict[str, object] = {}
    for family, results in payload["results"].items():
        diagonal, linear = family_data(family)
        best = math.inf
        for result in results:
            x = np.array(result["coordinates"], dtype=float)
            assert x.shape == (payload["parameters"]["number"], 5)
            norm_error = float(np.max(np.abs(np.sum(x * x, axis=1) - 1.0)))
            gram = x @ x.T
            np.fill_diagonal(gram, -math.inf)
            maximum = float(np.max(gram))
            minimum_q = float(np.min(q_values(x, diagonal, linear)))
            assert norm_error < 2e-12
            assert abs(maximum - result["maximum_inner_product"]) < 2e-12
            assert abs(minimum_q - result["minimum_q"]) < 2e-12
            # Every recorded run is a near miss, not a 41-point construction.
            assert maximum > 0.5
            best = min(best, maximum)
        summaries[family] = {
            "runs": len(results),
            "best_maximum_inner_product": best,
        }
    return {"status": "PASS (FLOATING-POINT DISCOVERY AUDIT)", "families": summaries}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
