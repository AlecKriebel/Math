#!/usr/bin/env python3
"""Bounded exact ternary tabu search on the 18 orbit-2 quadrics."""

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


def values_at(
    point: np.ndarray,
    constants: np.ndarray,
    linears: np.ndarray,
    polars: np.ndarray,
) -> np.ndarray:
    return np.remainder(
        constants
        + linears @ point
        + 2 * np.einsum("i,eij,j->e", point, polars, point),
        3,
    )


def replay(affine: np.ndarray) -> dict:
    profiles, origin, basis, _, _, _ = orbit2.exact_forms()
    placement = orbit2.second.lift_affine_point(
        origin, basis, tuple(map(int, affine))
    )
    first = orbit2.second.symbolic_first_digits(
        orbit2.first_digit_equations(profiles), placement
    )
    second = orbit2.second.direct_second_digits(profiles, placement)
    if first != (0,) * 20 or second != (0,) * 20:
        raise AssertionError("tabu witness failed direct lower-digit replay")
    displayed = orbit2.second.displayed_values(profiles, placement)
    digits = tuple(
        orbit2.second.lambda_digits(value, 10) for value in displayed
    )
    digit_counts = tuple(
        sum(row[digit] != 0 for row in digits) for digit in range(10)
    )
    masks_a, masks_b = orbit2.second.masks_from_trits(
        profiles, placement
    )
    aggregate = orbit2.labelled_aggregate(masks_a, masks_b)
    return {
        "affine_coordinates": tuple(map(int, affine)),
        "placement_trits": placement,
        "masks_a": masks_a,
        "masks_b": masks_b,
        "displayed_exact_values": displayed,
        "lambda_digits_through_9": digits,
        "digit_residual_counts": digit_counts,
        "row_margin_aggregate": aggregate,
        "row_margin_catalog_member": (
            aggregate in orbit2.row_sum_catalog()
        ),
    }


def search(seconds: float, seed: int, restart_updates: int) -> dict:
    _, _, _, constants0, linears0, polars0 = orbit2.exact_forms()
    constants = np.array(constants0, dtype=np.int16)
    linears = np.array(linears0, dtype=np.int16)
    polars = np.array(polars0, dtype=np.int16)
    rng = np.random.default_rng(seed)
    variables = linears.shape[1]
    single_variables = np.tile(np.arange(variables), 2)
    single_deltas = np.repeat((1, 2), variables)
    pair_i = []
    pair_j = []
    pair_di = []
    pair_dj = []
    for i in range(variables):
        for j in range(i + 1, variables):
            for di in (1, 2):
                for dj in (1, 2):
                    pair_i.append(i)
                    pair_j.append(j)
                    pair_di.append(di)
                    pair_dj.append(dj)
    pair_i = np.array(pair_i)
    pair_j = np.array(pair_j)
    pair_di = np.array(pair_di, dtype=np.int16)
    pair_dj = np.array(pair_dj, dtype=np.int16)

    started = time.monotonic()
    best = 19
    best_point = None
    best_values = None
    updates = 0
    restarts = 0
    while time.monotonic() - started < seconds:
        point = rng.integers(0, 3, variables, dtype=np.int16)
        values = values_at(point, constants, linears, polars)
        tabu = np.zeros(variables, dtype=np.int64)
        for _ in range(restart_updates):
            current = int(np.count_nonzero(values))
            if current < best:
                best = current
                best_point = point.copy()
                best_values = values.copy()
                if best == 0:
                    result = replay(point)
                    return {
                        "status": "SAT",
                        "seconds": time.monotonic() - started,
                        "updates": updates,
                        "restarts": restarts,
                        "best_defect": 0,
                        "replay": result,
                    }

            bx = np.einsum("eij,j->ei", polars, point)
            gradient = np.remainder(linears + bx, 3)
            single_change = (
                gradient[:, single_variables]
                * single_deltas[np.newaxis, :]
                + 2
                * polars[
                    :, single_variables, single_variables
                ]
                * (single_deltas * single_deltas)[np.newaxis, :]
            )
            moved = np.remainder(
                values[:, np.newaxis] + single_change, 3
            )
            scores = np.count_nonzero(moved, axis=0)

            # When close, exhaust all 2,520 genuine two-coordinate moves.
            if current <= 3:
                pair_change = (
                    gradient[:, pair_i] * pair_di[np.newaxis, :]
                    + gradient[:, pair_j] * pair_dj[np.newaxis, :]
                    + 2
                    * polars[:, pair_i, pair_i]
                    * (pair_di * pair_di)[np.newaxis, :]
                    + 2
                    * polars[:, pair_j, pair_j]
                    * (pair_dj * pair_dj)[np.newaxis, :]
                    + polars[:, pair_i, pair_j]
                    * (pair_di * pair_dj)[np.newaxis, :]
                )
                pair_moved = np.remainder(
                    values[:, np.newaxis] + pair_change, 3
                )
                pair_scores = np.count_nonzero(pair_moved, axis=0)
                pair_minimum = int(pair_scores.min())
                if pair_minimum < int(scores.min()):
                    choices = np.flatnonzero(
                        pair_scores == pair_minimum
                    )
                    move = int(rng.choice(choices))
                    point[pair_i[move]] = (
                        point[pair_i[move]] + pair_di[move]
                    ) % 3
                    point[pair_j[move]] = (
                        point[pair_j[move]] + pair_dj[move]
                    ) % 3
                    values = pair_moved[:, move]
                    updates += 1
                    if time.monotonic() - started >= seconds:
                        break
                    continue

            allowed = (
                tabu[single_variables] <= updates
            ) | (scores < best)
            ranked = np.where(allowed, scores, 127)
            minimum = int(ranked.min())
            choices = np.flatnonzero(ranked == minimum)
            move = int(rng.choice(choices))
            variable = int(single_variables[move])
            point[variable] = (
                point[variable] + int(single_deltas[move])
            ) % 3
            values = moved[:, move]
            tabu[variable] = updates + 7 + int(rng.integers(6))
            updates += 1
            if time.monotonic() - started >= seconds:
                break
        restarts += 1

    assert best_point is not None and best_values is not None
    return {
        "status": "UNKNOWN",
        "seconds": time.monotonic() - started,
        "updates": updates,
        "restarts": restarts,
        "best_defect": best,
        "best_affine_coordinates": best_point.tolist(),
        "best_active_residuals": best_values.tolist(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=120)
    parser.add_argument("--seed", type=int, default=668_202)
    parser.add_argument("--restart-updates", type=int, default=2000)
    args = parser.parse_args()
    print(
        json.dumps(
            search(args.seconds, args.seed, args.restart_updates),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
