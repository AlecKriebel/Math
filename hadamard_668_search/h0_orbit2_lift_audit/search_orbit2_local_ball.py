#!/usr/bin/env python3
"""Exhaust an exact ternary Hamming ball around a digit-2 point."""

from __future__ import annotations

import argparse
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time

import numpy as np


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import search_orbit2_digit2_sat as orbit2  # noqa: E402
import search_orbit2_digit2_tabu as tabu  # noqa: E402


def center_from_json(path: Path) -> np.ndarray:
    payload = json.loads(path.read_text())
    if "best_affine_coordinates" in payload:
        values = payload["best_affine_coordinates"]
    elif "affine_coordinates" in payload:
        values = payload["affine_coordinates"]
    else:
        values = payload["replay"]["affine_coordinates"]
    center = np.array(values, dtype=np.int16)
    if center.shape != (36,) or np.any((center < 0) | (center > 2)):
        raise ValueError("center is not a 36-trit affine point")
    return center


def search(center: np.ndarray, radius: int) -> dict:
    _, _, _, constants0, linears0, polars0 = orbit2.exact_forms()
    constants = np.array(constants0, dtype=np.int16)
    linears = np.array(linears0, dtype=np.int16)
    polars = np.array(polars0, dtype=np.int16)
    center_values = tabu.values_at(
        center, constants, linears, polars
    )
    bx = np.einsum("eij,j->ei", polars, center)
    gradient = np.remainder(linears + bx, 3)
    best = int(np.count_nonzero(center_values))
    best_point = center.copy()
    best_values = center_values.copy()
    tested = 1
    sphere_counts = {"0": 1}
    started = time.monotonic()

    for distance in range(1, radius + 1):
        indices = np.array(
            list(combinations(range(36), distance)),
            dtype=np.int16,
        )
        sphere_tested = 0
        for delta_values in product((1, 2), repeat=distance):
            delta = np.array(delta_values, dtype=np.int16)
            changes = np.zeros(
                (len(constants), len(indices)), dtype=np.int16
            )
            for position in range(distance):
                variable = indices[:, position]
                changes += (
                    gradient[:, variable] * int(delta[position])
                    + 2
                    * polars[:, variable, variable]
                    * int(delta[position] * delta[position])
                )
            for left in range(distance):
                for right in range(left + 1, distance):
                    changes += (
                        polars[
                            :,
                            indices[:, left],
                            indices[:, right],
                        ]
                        * int(delta[left] * delta[right])
                    )
            candidate_values = np.remainder(
                center_values[:, np.newaxis] + changes, 3
            )
            scores = np.count_nonzero(candidate_values, axis=0)
            minimum = int(scores.min())
            if minimum < best:
                offset = int(np.flatnonzero(scores == minimum)[0])
                point = center.copy()
                point[indices[offset]] = (
                    point[indices[offset]] + delta
                ) % 3
                exact = tabu.values_at(
                    point, constants, linears, polars
                )
                if not np.array_equal(
                    exact, candidate_values[:, offset]
                ):
                    raise AssertionError("sparse ball delta failed replay")
                best = minimum
                best_point = point
                best_values = exact
                if best == 0:
                    replay = tabu.replay(point)
                    tested += sphere_tested + offset + 1
                    sphere_counts[str(distance)] = (
                        sphere_tested + offset + 1
                    )
                    return {
                        "status": "SAT",
                        "radius_reached": distance,
                        "tested": tested,
                        "sphere_counts": sphere_counts,
                        "seconds": time.monotonic() - started,
                        "best_defect": 0,
                        "replay": replay,
                    }
            sphere_tested += len(indices)
        tested += sphere_tested
        sphere_counts[str(distance)] = sphere_tested

    return {
        "status": "UNSAT_IN_BALL",
        "radius_reached": radius,
        "tested": tested,
        "sphere_counts": sphere_counts,
        "seconds": time.monotonic() - started,
        "best_defect": best,
        "best_affine_coordinates": best_point.tolist(),
        "best_active_residuals": best_values.tolist(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--center", type=Path, required=True)
    parser.add_argument("--radius", type=int, default=5)
    args = parser.parse_args()
    if not 1 <= args.radius <= 6:
        raise ValueError("radius must lie from one through six")
    print(
        json.dumps(
            search(center_from_json(args.center), args.radius),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
