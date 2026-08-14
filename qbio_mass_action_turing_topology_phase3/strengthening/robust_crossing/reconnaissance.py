#!/usr/bin/env python3
"""Bounded numerical reconnaissance for primary stationary crossings.

This script is not a proof.  It samples stable four-dimensional matrices with a
negative signed principal minor, constructs diagonal-damping witnesses, and
classifies the earliest sampled loss of stability along J-tD.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


def signed_minor(matrix: np.ndarray, subset: tuple[int, ...]) -> float:
    block = matrix[np.ix_(subset, subset)]
    return ((-1) ** len(subset)) * float(np.linalg.det(block))


def negative_subset(matrix: np.ndarray) -> tuple[int, ...] | None:
    n = matrix.shape[0]
    for size in range(1, n):
        for subset in itertools.combinations(range(n), size):
            if signed_minor(matrix, subset) < -1e-8:
                return subset
    return None


def multiscale_d(subset: tuple[int, ...], n: int, matrix: np.ndarray) -> np.ndarray:
    in_set = set(subset)
    t = 2.0
    for _ in range(50):
        diag = np.array([1.0 / t if i in in_set else t for i in range(n)])
        if np.linalg.det(np.diag(diag) - matrix) < -1e-8:
            return diag
        t *= 2.0
    raise RuntimeError("failed to construct numerical witness")


def first_crossing(matrix: np.ndarray, diag: np.ndarray) -> str:
    # Adaptive dense scan only; output is explicitly reconnaissance.
    grid = np.linspace(0.0, 3.0, 6001)
    previous = np.max(np.real(np.linalg.eigvals(matrix)))
    for value in grid[1:]:
        eig = np.linalg.eigvals(matrix - value * np.diag(diag))
        current = float(np.max(np.real(eig)))
        if previous < 0.0 <= current:
            lead = eig[np.argmax(np.real(eig))]
            return "stationary" if abs(np.imag(lead)) < 1e-5 else "wave"
        previous = current
    return "not_seen"


def main() -> None:
    rng = np.random.default_rng(20260813)
    counts = {"eligible": 0, "stationary": 0, "wave": 0, "not_seen": 0}
    examples: list[dict[str, object]] = []
    attempts = 0
    while counts["eligible"] < 250 and attempts < 200000:
        attempts += 1
        raw = rng.integers(-8, 9, size=(4, 4)).astype(float)
        # Shift left to guarantee Hurwitz while retaining nonnormal structure.
        edge = float(np.max(np.real(np.linalg.eigvals(raw))))
        matrix = raw - (edge + rng.uniform(0.1, 2.0)) * np.eye(4)
        subset = negative_subset(matrix)
        if subset is None:
            continue
        diag = multiscale_d(subset, 4, matrix)
        kind = first_crossing(matrix, diag)
        counts["eligible"] += 1
        counts[kind] += 1
        if kind == "wave" and len(examples) < 5:
            examples.append({"matrix": matrix.tolist(), "subset": subset, "diag": diag.tolist()})
    result = {
        "status": "NUMERICAL_RECONNAISSANCE_ONLY",
        "attempts": attempts,
        "counts": counts,
        "wave_examples_retained": examples,
        "interpretation": (
            "A wave-first path would not refute existence of another primary stationary path; "
            "the universal robust-crossing question remains unproved."
        ),
    }
    out = Path(__file__).with_name("reconnaissance.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
