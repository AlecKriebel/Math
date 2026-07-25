#!/usr/bin/env python3
"""Randomized exact Newton steps for the 18 ternary quadrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import search_orbit2_digit2_sat as orbit2  # noqa: E402
import search_orbit2_digit2_tabu as tabu  # noqa: E402


def affine_solve(
    matrix: np.ndarray, rhs: np.ndarray
) -> tuple[np.ndarray, np.ndarray] | None:
    rows, columns = matrix.shape
    work = np.column_stack((matrix % 3, rhs % 3)).astype(np.int16)
    pivot_columns = []
    row = 0
    for column in range(columns):
        choices = np.flatnonzero(work[row:, column])
        if not len(choices):
            continue
        pivot = row + int(choices[0])
        work[[row, pivot]] = work[[pivot, row]]
        inverse = 1 if work[row, column] == 1 else 2
        work[row] = (work[row] * inverse) % 3
        for other in range(rows):
            if other != row and work[other, column]:
                work[other] = (
                    work[other]
                    - work[other, column] * work[row]
                ) % 3
        pivot_columns.append(column)
        row += 1
        if row == rows:
            break
    if any(
        not np.any(work[index, :-1]) and work[index, -1]
        for index in range(row, rows)
    ):
        return None
    free = [
        column
        for column in range(columns)
        if column not in pivot_columns
    ]
    particular = np.zeros(columns, dtype=np.int16)
    for equation, pivot in enumerate(pivot_columns):
        particular[pivot] = work[equation, -1]
    basis = np.zeros((len(free), columns), dtype=np.int16)
    for index, free_column in enumerate(free):
        basis[index, free_column] = 1
        for equation, pivot in enumerate(pivot_columns):
            basis[index, pivot] = -work[equation, free_column] % 3
    assert np.array_equal(matrix @ particular % 3, rhs % 3)
    assert not np.any(matrix @ basis.T % 3)
    return particular, basis


def search(
    seconds: float,
    seed: int,
    samples: int,
    initial_path: Path | None,
) -> dict:
    _, _, _, constants0, linears0, polars0 = orbit2.exact_forms()
    constants = np.array(constants0, dtype=np.int16)
    linears = np.array(linears0, dtype=np.int16)
    polars = np.array(polars0, dtype=np.int16)
    rng = np.random.default_rng(seed)
    initial = (
        np.array(
            json.loads(initial_path.read_text())[
                "best_affine_coordinates"
            ],
            dtype=np.int16,
        )
        if initial_path is not None
        else None
    )
    started = time.monotonic()
    iterations = 0
    restarts = 0
    best = 19
    best_point = None
    best_values = None

    while time.monotonic() - started < seconds:
        if initial is not None:
            point = initial.copy()
            initial = None
        else:
            point = rng.integers(0, 3, 36, dtype=np.int16)
        for _ in range(80):
            values = tabu.values_at(
                point, constants, linears, polars
            )
            defect = int(np.count_nonzero(values))
            if defect < best:
                best = defect
                best_point = point.copy()
                best_values = values.copy()
                if best == 0:
                    return {
                        "status": "SAT",
                        "seconds": time.monotonic() - started,
                        "iterations": iterations,
                        "restarts": restarts,
                        "best_defect": 0,
                        "replay": tabu.replay(point),
                    }

            jacobian = np.remainder(
                linears
                + np.einsum("eij,j->ei", polars, point),
                3,
            )
            solved = affine_solve(jacobian, -values)
            if solved is None:
                break
            particular, basis = solved
            coefficients = rng.integers(
                0, 3, size=(samples, len(basis)), dtype=np.int16
            )
            deltas = (
                particular[np.newaxis, :]
                + coefficients @ basis
            ) % 3
            # The affine term is exactly -values.  Only the quadratic
            # Newton error remains at each candidate.
            candidate_values = np.remainder(
                2
                * np.einsum(
                    "ni,eij,nj->en",
                    deltas,
                    polars,
                    deltas,
                    optimize=True,
                ),
                3,
            )
            scores = np.count_nonzero(candidate_values, axis=0)
            minimum = int(scores.min())
            choices = np.flatnonzero(scores == minimum)
            choice = int(rng.choice(choices))
            point = (point + deltas[choice]) % 3
            exact = tabu.values_at(
                point, constants, linears, polars
            )
            if not np.array_equal(exact, candidate_values[:, choice]):
                raise AssertionError("Newton remainder replay failed")
            iterations += 1
            if time.monotonic() - started >= seconds:
                break
        restarts += 1

    assert best_point is not None and best_values is not None
    return {
        "status": "UNKNOWN",
        "seconds": time.monotonic() - started,
        "iterations": iterations,
        "restarts": restarts,
        "samples_per_step": samples,
        "best_defect": best,
        "best_affine_coordinates": best_point.tolist(),
        "best_active_residuals": best_values.tolist(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=120)
    parser.add_argument("--seed", type=int, default=668_204)
    parser.add_argument("--samples", type=int, default=256)
    parser.add_argument("--initial", type=Path)
    args = parser.parse_args()
    print(
        json.dumps(
            search(
                args.seconds, args.seed, args.samples, args.initial
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
