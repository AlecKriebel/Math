#!/usr/bin/env python3
"""Fixed-weight local search for characteristic-2/3 anti-fold survivors.

This is a witness finder, never an exclusion engine.  It searches the exact
quadratic modular equations used by ``search_char3_cp_sat.py`` with
selected/unselected swaps, then replays any zero-defect point through the
physical anti-fold correlations.
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

import search_char3_antifold as char3  # noqa: E402
import search_char3_cp_sat as cp  # noqa: E402


def arrays(case_number: int):
    case = char3.canonical_cases()[case_number]
    # Reuse the authoritative domain without solving.
    _, _, id_variables, _ = char3.build(case, ())
    keys = tuple(sorted(id_variables))
    key_index = {key: index for index, key in enumerate(keys)}
    equations = cp.quadratic_equations(case, set(keys))
    linear = np.zeros((len(equations), len(keys)), dtype=np.int16)
    quadratic = np.zeros(
        (len(equations), len(keys), len(keys)), dtype=np.int16
    )
    constant = np.array(
        [equation.constant for equation in equations], dtype=np.int16
    )
    for row, equation in enumerate(equations):
        for key, value in equation.linear.items():
            linear[row, key_index[key]] = value
        for (left, right), value in equation.quadratic.items():
            i, j = key_index[left], key_index[right]
            quadratic[row, i, j] = value
            quadratic[row, j, i] = value
    return case, keys, equations, constant, linear, quadratic


def exact_values(
    chosen: np.ndarray,
    constant: np.ndarray,
    linear: np.ndarray,
    quadratic: np.ndarray,
) -> np.ndarray:
    vector = chosen.astype(np.int16)
    return (
        constant
        + linear @ vector
        + np.einsum("eij,i,j->e", quadratic, vector, vector) // 2
    )


def defect(values: np.ndarray, modulus: int) -> int:
    residues = np.remainder(values, modulus)
    distances = np.minimum(residues, modulus - residues)
    return int(distances @ distances)


def search(
    case_number: int,
    modulus: int,
    seconds: float,
    seed: int,
    sample_pairs: int,
) -> dict[str, object]:
    case, keys, equations, constant, linear, quadratic = arrays(case_number)
    rng = np.random.default_rng(seed)
    started = time.monotonic()
    best_defect = 10**9
    best_values: list[int] = []
    best_selected: list[list[object]] = []
    iterations = 0
    restarts = 0
    chosen = np.zeros(len(keys), dtype=np.int8)

    while time.monotonic() - started < seconds:
        chosen[:] = 0
        chosen[rng.choice(len(keys), size=39, replace=False)] = 1
        values = exact_values(chosen, constant, linear, quadratic)
        current = defect(values, modulus)
        restart_best = current
        restarts += 1
        stagnant = 0

        while stagnant < 80 and time.monotonic() - started < seconds:
            iterations += 1
            if current < best_defect:
                best_defect = current
                best_values = values.tolist()
                best_selected = [
                    [key[0], key[1]]
                    for key, flag in zip(keys, chosen)
                    if flag
                ]
            if current == 0:
                selected = tuple(
                    key for key, flag in zip(keys, chosen) if flag
                )
                replay = cp.replay(
                    case, selected, equations, modulus
                )
                return {
                    "status": "SAT",
                    "case": case_number,
                    "block": case.block,
                    "q_index": case.index,
                    "modulus": modulus,
                    "seconds": time.monotonic() - started,
                    "iterations": iterations,
                    "restarts": restarts,
                    "best_defect": 0,
                    "model": replay,
                }

            selected_indices = np.flatnonzero(chosen)
            unselected_indices = np.flatnonzero(1 - chosen)
            gradient = linear + np.einsum(
                "eij,j->ei", quadratic, chosen
            )
            total_pairs = len(selected_indices) * len(unselected_indices)
            if sample_pairs >= total_pairs:
                left = np.repeat(
                    selected_indices, len(unselected_indices)
                )
                right = np.tile(
                    unselected_indices, len(selected_indices)
                )
            else:
                left = rng.choice(
                    selected_indices, size=sample_pairs, replace=True
                )
                right = rng.choice(
                    unselected_indices, size=sample_pairs, replace=True
                )
            deltas = (
                -gradient[:, left]
                + gradient[:, right]
                - quadratic[:, left, right]
            )
            candidates = values[:, None] + deltas
            residues = np.remainder(candidates, modulus)
            distances = np.minimum(residues, modulus - residues)
            scores = np.sum(distances * distances, axis=0)
            minimum = int(scores.min())
            good = np.flatnonzero(scores == minimum)

            # Greedy descent with plateau diffusion; a small random kick
            # prevents a deterministic two-cycle.
            if minimum <= current:
                choice = int(rng.choice(good))
            else:
                choice = int(rng.integers(len(left)))
            i, j = int(left[choice]), int(right[choice])
            chosen[i] = 0
            chosen[j] = 1
            values = exact_values(chosen, constant, linear, quadratic)
            current = defect(values, modulus)
            if current < restart_best:
                restart_best = current
                stagnant = 0
            else:
                stagnant += 1

    return {
        "status": "UNKNOWN",
        "case": case_number,
        "block": case.block,
        "q_index": case.index,
        "modulus": modulus,
        "seconds": time.monotonic() - started,
        "iterations": iterations,
        "restarts": restarts,
        "best_defect": best_defect,
        "best_normalized_residuals": best_values,
        "best_selected": best_selected,
        "model": None,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=int, default=0)
    parser.add_argument("--modulus", type=int, default=6)
    parser.add_argument("--seconds", type=float, default=60.0)
    parser.add_argument("--seed", type=int, default=668_423)
    parser.add_argument("--sample-pairs", type=int, default=512)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    char3.factorization_self_test()
    if not 0 <= args.case < 30:
        raise ValueError("case must lie in 0,...,29")
    if args.modulus < 2 or args.seconds <= 0 or args.sample_pairs < 1:
        raise ValueError("invalid search parameter")
    print(
        json.dumps(
            search(
                args.case,
                args.modulus,
                args.seconds,
                args.seed,
                args.sample_pairs,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
