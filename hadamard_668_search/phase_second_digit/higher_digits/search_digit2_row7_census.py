#!/usr/bin/env python3
"""Fast quadratic census of digit-2 points and delayed row-7 values.

This instrumental search tests the hypothesis that the eighteen active
second-digit quadrics force the delayed E1-origin digit-3 row to be nonzero.
It never treats a bounded failure to find a point as a proof.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import search_lambda_prefix_tabu as exact  # noqa: E402
import solve_full_second_digit_sat as quadratic  # noqa: E402


def quadratic_state(constants, linears, polars, point):
    values = (
        constants
        + linears @ point
        + 2
        * np.einsum(
            "i,eij,j->e", point, polars, point, optimize=True
        )
    ) % 3
    gradients = (
        linears + np.einsum("eij,j->ei", polars, point)
    ) % 3
    return values, gradients


def search(
    candidate_index: int,
    seconds: float,
    seed: int,
    restart_updates: int,
    maximum_hits: int,
) -> dict[str, object]:
    (
        profiles,
        origin,
        basis,
        constants,
        linears,
        polars,
    ) = quadratic.exact_forms(candidate_index)
    constants = np.array(constants, dtype=np.int16)
    linears = np.array(linears, dtype=np.int16)
    polars = np.array(polars, dtype=np.int16)
    diagonals = np.diagonal(polars, axis1=1, axis2=2)
    rng = np.random.default_rng(seed)
    started = time.monotonic()
    deadline = started + seconds
    updates = 0
    restarts = 0
    hits: dict[str, dict[str, object]] = {}
    best_quadratic = len(constants) + 1

    while (
        time.monotonic() < deadline
        and len(hits) < maximum_hits
    ):
        point = rng.integers(0, 3, 36, dtype=np.int16)
        values, gradients = quadratic_state(
            constants, linears, polars, point
        )
        tabu_until = np.zeros(36, dtype=np.int64)
        for _ in range(restart_updates):
            energy = int(np.count_nonzero(values))
            best_quadratic = min(best_quadratic, energy)
            if energy == 0:
                affine = tuple(map(int, point))
                placement = quadratic.second.lift_affine_point(
                    origin, basis, affine
                )
                displayed = quadratic.second.displayed_values(
                    profiles, placement
                )
                digits = tuple(
                    quadratic.second.lambda_digits(value, 5)
                    for value in displayed
                )
                if any(row[2] for row in digits):
                    raise AssertionError(
                        "a quadratic hit failed exact digit-2 replay"
                    )
                placement_hash = exact.prefix.compact_hash(placement)
                if placement_hash not in hits:
                    hits[placement_hash] = {
                        "affine_coordinates": affine,
                        "affine_coordinates_sha256": (
                            exact.prefix.compact_hash(affine)
                        ),
                        "placement_trits_sha256": placement_hash,
                        "delayed_e1_origin_digit3": int(digits[7][3]),
                        "digit3_nonzero_rows": sum(
                            row[3] != 0 for row in digits
                        ),
                        "updates_at_first_hit": updates,
                    }
                    print(
                        f"hit={len(hits)} row7={digits[7][3]} "
                        f"digit3_nonzero="
                        f"{sum(row[3] != 0 for row in digits)} "
                        f"updates={updates}",
                        flush=True,
                    )
                # Diversify by six coordinates before resuming.
                for variable in rng.choice(36, 6, replace=False):
                    point[variable] = rng.integers(0, 3)
                values, gradients = quadratic_state(
                    constants, linears, polars, point
                )
                tabu_until[:] = 0

            changes_one = (gradients + 2 * diagonals) % 3
            changes_two = (2 * gradients + 2 * diagonals) % 3
            changes = np.concatenate(
                (changes_one, changes_two), axis=1
            )
            energies = np.count_nonzero(
                (values[:, None] + changes) % 3, axis=0
            )
            move_variables = np.tile(np.arange(36), 2)
            move_deltas = np.repeat((1, 2), 36)
            allowed = (
                tabu_until[move_variables] <= updates
            ) | (energies == 0)
            ranked = np.where(allowed, energies, 32767)
            choices = np.flatnonzero(ranked == ranked.min())
            move = int(rng.choice(choices))
            variable = int(move_variables[move])
            delta = int(move_deltas[move])
            point[variable] = (point[variable] + delta) % 3
            values = (values + changes[:, move]) % 3
            gradients = (
                gradients + delta * polars[:, :, variable]
            ) % 3
            tabu_until[variable] = (
                updates + 7 + int(rng.integers(0, 5))
            )
            updates += 1
            if time.monotonic() >= deadline:
                break
        restarts += 1

    candidate = quadratic.second.CANDIDATES[candidate_index]
    result = {
        "schema": "lp333-order3-digit2-row7-bounded-census-v1",
        "scope": (
            "Bounded stochastic census of exact digit-2 points and the "
            "delayed E1-origin digit-3 value; absence is not a proof."
        ),
        "label": candidate[0],
        "candidate_index": candidate_index,
        "status": "BOUNDED_COMPLETE",
        "seconds": seconds,
        "seed": seed,
        "updates": updates,
        "restarts": restarts,
        "best_quadratic_residual_count": best_quadratic,
        "distinct_digit2_hits": len(hits),
        "row7_zero_hits": sum(
            hit["delayed_e1_origin_digit3"] == 0
            for hit in hits.values()
        ),
        "hits": tuple(hits.values()),
    }
    result["semantic_sha256"] = exact.prefix.compact_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=int, choices=range(5), required=True)
    parser.add_argument("--seconds", type=float, default=300)
    parser.add_argument("--seed", type=int, default=668)
    parser.add_argument("--restart-updates", type=int, default=200000)
    parser.add_argument("--maximum-hits", type=int, default=8)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = search(
        args.candidate,
        args.seconds,
        args.seed,
        args.restart_updates,
        args.maximum_hits,
    )
    payload = json.dumps(result, indent=2)
    if args.output is not None:
        args.output.write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()
