#!/usr/bin/env python3
"""Search for shallow origin halfspaces in a stored numerical code.

For a generic cloud in R^5, a locally extremal direction for the number of
points in an open halfspace can be rotated until its boundary contains four
points.  This diagnostic enumerates all four-point spans and both normal
orientations.  It is a floating-point probe, not a proof of Tukey depth:
degeneracies, nearly dependent quadruples, and near-boundary dot products
must be handled exactly before drawing a theorem.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import numpy as np


STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"


def normal_to_four(rows: np.ndarray) -> np.ndarray:
    cofactors = np.empty(5)
    for column in range(5):
        cofactors[column] = ((-1.0) ** column) * np.linalg.det(
            np.delete(rows, column, axis=1)
        )
    norm = float(np.linalg.norm(cofactors))
    if norm <= 1e-12:
        raise ValueError("numerically dependent quadruple")
    return cofactors / norm


def probe(x: np.ndarray, boundary_tolerance: float = 2e-10) -> dict:
    x = np.asarray(x, dtype=float)
    x /= np.linalg.norm(x, axis=1)[:, None]
    best = None
    dependent = 0
    for subset in itertools.combinations(range(len(x)), 4):
        try:
            normal = normal_to_four(x[list(subset)])
        except ValueError:
            dependent += 1
            continue
        dots = x @ normal
        positive = int(np.sum(dots > boundary_tolerance))
        negative = int(np.sum(dots < -boundary_tolerance))
        boundary = len(x) - positive - negative
        for orientation, (oriented_normal, open_count) in enumerate((
            (normal, positive),
            (-normal, negative),
        )):
            oriented_dots = dots if orientation == 0 else -dots
            key = (open_count, -boundary, subset, orientation)
            candidate = (
                key,
                subset,
                oriented_normal,
                oriented_dots,
            )
            if best is None or key < best[0]:
                best = candidate
    if best is None:
        raise ArithmeticError("no independent four-point subset")
    key, subset, normal, dots = best
    open_count, negative_boundary = key[:2]
    return {
        "status": STATUS,
        "boundary_tolerance": boundary_tolerance,
        "enumerated_quadruples": math_comb(len(x), 4),
        "numerically_dependent_quadruples": dependent,
        "minimum_open_positive_count_found": int(open_count),
        "negative_count": int(np.sum(dots < -boundary_tolerance)),
        "boundary_count": int(-negative_boundary),
        "boundary_indices": [
            int(i) for i in np.flatnonzero(np.abs(dots) <= boundary_tolerance)
        ],
        "generating_quadruple": list(subset),
        "normal_float64": normal.tolist(),
        "signed_dots_float64": dots.tolist(),
    }


def math_comb(n: int, k: int) -> int:
    answer = 1
    for j in range(1, k + 1):
        answer = answer * (n + 1 - j) // j
    return answer


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--n", type=int, default=41)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    with arguments.artifact.open() as stream:
        payload = json.load(stream)
    eligible = [run for run in payload["runs"] if run["n"] == arguments.n]
    if not eligible:
        parser.error("artifact has no run at requested cardinality")
    run = min(eligible, key=lambda item: item["best"]["maximum"])
    result = probe(np.asarray(run["best"]["coordinates_float64"], dtype=float))
    result["source_artifact"] = str(arguments.artifact)
    result["source_seed"] = run["seed"]
    result["source_maximum"] = run["best"]["maximum"]
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    with arguments.output.open("w") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(
        "minimum open-side count found:",
        result["minimum_open_positive_count_found"],
    )
    print("boundary count:", result["boundary_count"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
