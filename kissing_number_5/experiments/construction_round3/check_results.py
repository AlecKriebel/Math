#!/usr/bin/env python3
"""Recompute binary64 diagnostics stored by the round-3 search.

This is an integrity checker for numerical discovery artifacts.  It is not
an exact verifier and cannot turn a floating-point candidate into a kissing
configuration or turn failed searches into an upper bound.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from .manifold_augmented_lagrangian import EVIDENCE_STATUS, diagnostics


def check_file(path: Path) -> dict:
    payload = json.loads(path.read_text())
    if payload["evidence_status"] != EVIDENCE_STATUS:
        raise AssertionError(f"{path}: missing numerical-evidence disclaimer")
    best: dict[int, tuple[float, int]] = {}
    for index, run in enumerate(payload["runs"]):
        x = np.asarray(run["coordinates_float64"], dtype=float)
        recomputed = diagnostics(x)
        stored = run["final_diagnostics"]
        if int(run["n"]) != len(x) or recomputed["n"] != len(x):
            raise AssertionError(f"{path}: bad cardinality in run {index}")
        scalar_keys = (
            "max_inner_product",
            "gap_above_one_half",
            "minimum_inner_product",
            "maximum_squared_norm_error",
            "gram_null_spectrum_max_abs",
        )
        for key in scalar_keys:
            if not math.isclose(
                float(recomputed[key]),
                float(stored[key]),
                rel_tol=2e-13,
                abs_tol=2e-13,
            ):
                raise AssertionError(f"{path}: run {index}, mismatch in {key}")
        exact_keys = (
            "number_pairs_above_one_half",
            "number_pairs_strictly_below_minus_one_half",
            "coordinate_little_endian_float64_sha256",
        )
        for key in exact_keys:
            if recomputed[key] != stored[key]:
                raise AssertionError(f"{path}: run {index}, mismatch in {key}")
        for tolerance in ("1e-04", "1e-06", "1e-08"):
            if (
                recomputed["active_graphs"][tolerance]
                != stored["active_graphs"][tolerance]
            ):
                raise AssertionError(
                    f"{path}: run {index}, active graph {tolerance} changed"
                )
        n = int(run["n"])
        value = float(recomputed["max_inner_product"])
        if n not in best or value < best[n][0]:
            best[n] = (value, index)

    for n, (value, index) in best.items():
        recorded = payload["best_by_n"][str(n)]
        if int(recorded["run_index"]) != index or not math.isclose(
            float(recorded["max_inner_product"]), value, abs_tol=1e-15
        ):
            raise AssertionError(f"{path}: best-by-N record is stale for N={n}")
    return {
        "path": str(path),
        "runs": len(payload["runs"]),
        "best_by_n": {
            str(n): {"max_inner_product": value, "run_index": index}
            for n, (value, index) in sorted(best.items())
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", type=Path, nargs="+")
    args = parser.parse_args()
    print(
        json.dumps(
            {
                "status": EVIDENCE_STATUS,
                "checked": [check_file(path) for path in args.files],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
