#!/usr/bin/env python3
"""Bounded one/two-swap witness search for the modulo-six jet.

Unlike the baseline local search, this program samples genuine two-out,
two-in moves.  It remains a witness finder only: UNKNOWN is not an
exclusion certificate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
JET = SEARCH / "eliahou_char3_jet"
sys.path[:0] = [str(JET), str(SEARCH)]

import search_char3_antifold as char3  # noqa: E402
import search_char3_cp_sat as cp  # noqa: E402
import search_char3_local as local  # noqa: E402


def score(values: np.ndarray, modulus: int = 6) -> int:
    residues = np.remainder(values, modulus)
    distances = np.minimum(residues, modulus - residues)
    return int(distances @ distances)


def search(
    case_number: int, seconds: float, seed: int, modulus: int
) -> dict:
    case, keys, equations, constant, linear, quadratic = local.arrays(
        case_number
    )
    rng = np.random.default_rng(seed)
    started = time.monotonic()
    chosen = np.zeros(len(keys), dtype=np.int8)
    best = 10**9
    best_values = None
    best_chosen = None
    iterations = 0
    restarts = 0

    while time.monotonic() - started < seconds:
        restarts += 1
        chosen[:] = 0
        chosen[rng.choice(len(keys), 39, replace=False)] = 1
        values = local.exact_values(chosen, constant, linear, quadratic)
        current = score(values, modulus)
        stale = 0

        while stale < 120 and time.monotonic() - started < seconds:
            iterations += 1
            if current < best:
                best = current
                best_values = values.copy()
                best_chosen = chosen.copy()
            if current == 0:
                selected = tuple(
                    key for key, flag in zip(keys, chosen) if flag
                )
                return {
                    "status": "SAT",
                    "case": case_number,
                    "seconds": time.monotonic() - started,
                    "iterations": iterations,
                    "restarts": restarts,
                    "modulus": modulus,
                    "model": cp.replay(
                        case, selected, equations, modulus
                    ),
                }

            inside = np.flatnonzero(chosen)
            outside = np.flatnonzero(1 - chosen)
            gradient = linear + np.einsum(
                "eij,j->ei", quadratic, chosen
            )

            # Full one-out/one-in neighborhood.
            left = np.repeat(inside, len(outside))
            right = np.tile(outside, len(inside))
            deltas1 = (
                -gradient[:, left]
                + gradient[:, right]
                - quadratic[:, left, right]
            )
            candidates1 = values[:, None] + deltas1
            residues1 = np.remainder(candidates1, modulus)
            distances1 = np.minimum(
                residues1, modulus - residues1
            )
            scores1 = np.sum(distances1 * distances1, axis=0)
            min1 = int(scores1.min())

            # Sample 16K two-out/two-in moves.  The exact second-order
            # correction is included, so every accepted move is replayable.
            samples = 16_384
            a = rng.choice(inside, samples, replace=True)
            b = rng.choice(inside, samples, replace=True)
            c = rng.choice(outside, samples, replace=True)
            d = rng.choice(outside, samples, replace=True)
            good = (a != b) & (c != d)
            a, b, c, d = a[good], b[good], c[good], d[good]
            deltas2 = (
                -gradient[:, a]
                - gradient[:, b]
                + gradient[:, c]
                + gradient[:, d]
                + quadratic[:, a, b]
                + quadratic[:, c, d]
                - quadratic[:, a, c]
                - quadratic[:, a, d]
                - quadratic[:, b, c]
                - quadratic[:, b, d]
            )
            candidates2 = values[:, None] + deltas2
            residues2 = np.remainder(candidates2, modulus)
            distances2 = np.minimum(
                residues2, modulus - residues2
            )
            scores2 = np.sum(distances2 * distances2, axis=0)
            min2 = int(scores2.min())

            if min2 < min1 or (min2 == min1 and rng.random() < 0.7):
                candidates = np.flatnonzero(scores2 == min2)
                pick = int(rng.choice(candidates))
                changed = (int(a[pick]), int(b[pick]), int(c[pick]), int(d[pick]))
                next_score = min2
            else:
                candidates = np.flatnonzero(scores1 == min1)
                pick = int(rng.choice(candidates))
                changed = (int(left[pick]), int(right[pick]))
                next_score = min1

            # Greedy/plateau motion, with a random one-swap kick after a
            # strict local rise.  This avoids certifying anything from the
            # heuristic landscape.
            if next_score <= current or rng.random() < 0.015:
                if len(changed) == 2:
                    chosen[changed[0]] = 0
                    chosen[changed[1]] = 1
                else:
                    chosen[changed[0]] = chosen[changed[1]] = 0
                    chosen[changed[2]] = chosen[changed[3]] = 1
            else:
                i = int(rng.choice(inside))
                j = int(rng.choice(outside))
                chosen[i] = 0
                chosen[j] = 1
            values = local.exact_values(
                chosen, constant, linear, quadratic
            )
            new_score = score(values, modulus)
            if new_score < current:
                stale = 0
            else:
                stale += 1
            current = new_score

    assert best_values is not None and best_chosen is not None
    return {
        "status": "UNKNOWN",
        "case": case_number,
        "modulus": modulus,
        "seconds": time.monotonic() - started,
        "iterations": iterations,
        "restarts": restarts,
        "best_defect": best,
        "best_normalized_residuals": best_values.tolist(),
        "best_selected": [
            [key[0], key[1]]
            for key, flag in zip(keys, best_chosen)
            if flag
        ],
        "model": None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, choices=(0, 26), required=True)
    parser.add_argument("--seconds", type=float, default=90)
    parser.add_argument("--seed", type=int, default=668_342)
    parser.add_argument("--modulus", type=int, default=6)
    args = parser.parse_args()
    if args.modulus < 2:
        raise ValueError("modulus must be at least two")
    print(
        json.dumps(
            search(
                args.case, args.seconds, args.seed, args.modulus
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
