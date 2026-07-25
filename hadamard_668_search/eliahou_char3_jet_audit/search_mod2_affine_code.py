#!/usr/bin/env python3
"""Search the exact weight-39 characteristic-2 affine code.

In characteristic two the quadratic anti-fold terms vanish after the
integer equations are divided by their content four.  The twenty
constraints are therefore affine linear.  This search starts from exact
SAT points of that affine code and moves only by weight-preserving null-code
words of weights 2, 4, and 6.  Its objective is the number of nonzero
characteristic-three jet coordinates.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from itertools import combinations
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
from verify_mod2_affine_code import rref_parameterization  # noqa: E402


def gf2_rank(matrix: np.ndarray) -> int:
    work = (matrix.copy() & 1).astype(np.uint8)
    row = 0
    for column in range(work.shape[1]):
        pivots = np.flatnonzero(work[row:, column])
        if not len(pivots):
            continue
        pivot = row + int(pivots[0])
        work[[row, pivot]] = work[[pivot, row]]
        for other in np.flatnonzero(work[:, column]):
            if other != row:
                work[other] ^= work[row]
        row += 1
        if row == work.shape[0]:
            break
    return row


def column_syndromes(linear: np.ndarray) -> list[int]:
    return [
        sum((int(linear[equation, variable]) & 1) << equation
            for equation in range(linear.shape[0]))
        for variable in range(linear.shape[1])
    ]


def null_moves(syndromes: list[int]) -> dict[int, np.ndarray]:
    words: dict[int, set[tuple[int, ...]]] = {
        2: set(),
        4: set(),
        6: set(),
    }
    by_value: dict[int, list[int]] = defaultdict(list)
    for index, value in enumerate(syndromes):
        by_value[value].append(index)
    for bucket in by_value.values():
        words[2].update(combinations(bucket, 2))

    pairs: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for left, right in combinations(range(len(syndromes)), 2):
        pairs[syndromes[left] ^ syndromes[right]].append((left, right))
    for bucket in pairs.values():
        for first, second in combinations(bucket, 2):
            if set(first).isdisjoint(second):
                words[4].add(tuple(sorted(first + second)))

    triples: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
    for triple in combinations(range(len(syndromes)), 3):
        value = (
            syndromes[triple[0]]
            ^ syndromes[triple[1]]
            ^ syndromes[triple[2]]
        )
        triples[value].append(triple)
    for bucket in triples.values():
        for first, second in combinations(bucket, 2):
            if set(first).isdisjoint(second):
                words[6].add(tuple(sorted(first + second)))

    result = {
        weight: np.array(sorted(values), dtype=np.int16).reshape(
            (-1, weight)
        )
        for weight, values in words.items()
    }
    for weight, moves in result.items():
        for move in moves:
            assert len(set(map(int, move))) == weight
            assert not np.bitwise_xor.reduce(
                np.array(
                    [syndromes[int(index)] for index in move],
                    dtype=np.uint32,
                )
            )
    return result


def score(values: np.ndarray) -> int:
    return int(np.count_nonzero(np.remainder(values, 3)))


def quotient_sampler(
    linear: np.ndarray,
    constant: np.ndarray,
) -> tuple[list[list[int]], np.ndarray, np.ndarray]:
    affine = np.remainder(linear, 2).astype(np.uint8)
    rhs = np.remainder(-constant, 2).astype(np.uint8)
    groups_by_syndrome: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for variable in range(linear.shape[1]):
        groups_by_syndrome[
            tuple(map(int, affine[:, variable]))
        ].append(variable)
    groups = list(groups_by_syndrome.values())
    assert all(len(group) in (1, 2) for group in groups)
    quotient = np.array(list(groups_by_syndrome), dtype=np.uint8).T
    augmented = np.vstack(
        [quotient, np.ones((1, len(groups)), dtype=np.uint8)]
    )
    augmented_rhs = np.append(rhs, 1).astype(np.uint8)
    _, _, particular, basis = rref_parameterization(
        augmented, augmented_rhs
    )
    return groups, particular, basis


def initial_point(
    variable_count: int,
    groups: list[list[int]],
    quotient_particular: np.ndarray,
    quotient_basis: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    coefficients = rng.integers(
        0, 2, size=len(quotient_basis), dtype=np.uint8
    )
    parity = quotient_particular.copy()
    if np.any(coefficients):
        parity ^= np.bitwise_xor.reduce(
            quotient_basis[coefficients.astype(bool)], axis=0
        )
    chosen = np.zeros(variable_count, dtype=np.int8)
    zero_pairs = []
    for value, group in zip(parity, groups):
        if len(group) == 1:
            chosen[group[0]] = int(value)
        elif value:
            chosen[group[int(rng.integers(2))]] = 1
        else:
            zero_pairs.append(group)
    missing = 39 - int(chosen.sum())
    assert missing >= 0 and missing % 2 == 0
    doubled = missing // 2
    for offset in rng.choice(
        len(zero_pairs), size=doubled, replace=False
    ):
        chosen[zero_pairs[int(offset)]] = 1
    assert int(chosen.sum()) == 39
    return chosen


def best_move_for_weight(
    values: np.ndarray,
    chosen: np.ndarray,
    gradient: np.ndarray,
    quadratic: np.ndarray,
    moves: np.ndarray,
) -> tuple[int, np.ndarray] | None:
    if not len(moves):
        return None
    weight = moves.shape[1]
    valid = moves[np.sum(chosen[moves], axis=1) == weight // 2]
    if not len(valid):
        return None
    signs = 1 - 2 * chosen[valid]
    deltas = np.sum(
        gradient[:, valid] * signs[np.newaxis, :, :], axis=2
    )
    for left in range(weight):
        for right in range(left + 1, weight):
            deltas += (
                quadratic[:, valid[:, left], valid[:, right]]
                * signs[:, left][np.newaxis, :]
                * signs[:, right][np.newaxis, :]
            )
    candidate_values = values[:, np.newaxis] + deltas
    candidate_scores = np.count_nonzero(
        np.remainder(candidate_values, 3), axis=0
    )
    minimum = int(candidate_scores.min())
    return minimum, valid[candidate_scores == minimum]


def search(case_number: int, seconds: float, seed: int) -> dict:
    case, keys, equations, constant, linear, quadratic = local.arrays(
        case_number
    )
    assert not np.any(np.remainder(quadratic, 2))
    affine = np.remainder(linear, 2).astype(np.uint8)
    augmented = np.vstack(
        [affine, np.ones((1, len(keys)), dtype=np.uint8)]
    )
    rank = gf2_rank(affine)
    augmented_rank = gf2_rank(augmented)
    assert rank == 20 and augmented_rank == 21
    dimension = len(keys) - augmented_rank
    moves = null_moves(column_syndromes(linear))
    groups, quotient_particular, quotient_basis = quotient_sampler(
        linear, constant
    )

    rng = np.random.default_rng(seed)
    started = time.monotonic()
    best_score = 21
    best_values = None
    best_chosen = None
    iterations = 0
    restarts = 0

    while time.monotonic() - started < seconds:
        restarts += 1
        chosen = initial_point(
            len(keys),
            groups,
            quotient_particular,
            quotient_basis,
            rng,
        )
        values = local.exact_values(
            chosen, constant, linear, quadratic
        )
        assert not np.any(np.remainder(values, 2))
        current = score(values)
        stale = 0
        local_steps = 0
        while (
            stale < 250
            and local_steps < 500
            and time.monotonic() - started < seconds
        ):
            iterations += 1
            local_steps += 1
            if current < best_score:
                best_score = current
                best_values = values.copy()
                best_chosen = chosen.copy()
            if current == 0:
                selected = tuple(
                    key for key, flag in zip(keys, chosen) if flag
                )
                replay = cp.replay(case, selected, equations, 6)
                return {
                    "status": "SAT",
                    "case": case_number,
                    "block": case.block,
                    "q_index": case.index,
                    "affine_rank": rank,
                    "weight_parity_rank": augmented_rank,
                    "weight_parity_dimension": dimension,
                    "null_move_counts": {
                        str(weight): len(values)
                        for weight, values in moves.items()
                    },
                    "seconds": time.monotonic() - started,
                    "iterations": iterations,
                    "restarts": restarts,
                    "mod3_defect": 0,
                    "model": replay,
                }

            gradient = linear + np.einsum(
                "eij,j->ei", quadratic, chosen
            )
            candidates = []
            for weight in (2, 4, 6):
                result = best_move_for_weight(
                    values,
                    chosen,
                    gradient,
                    quadratic,
                    moves[weight],
                )
                if result is not None:
                    candidates.append((result[0], weight, result[1]))
            minimum = min(item[0] for item in candidates)
            best_families = [
                item for item in candidates if item[0] == minimum
            ]
            _, _, family = best_families[int(rng.integers(len(best_families)))]
            move = family[int(rng.integers(len(family)))]

            # Prefer descent/plateaux.  Occasional code-preserving uphill
            # moves and random moves prevent a deterministic local cycle.
            if minimum <= current or rng.random() < 0.025:
                chosen[move] ^= 1
            else:
                weight = (2, 4, 6)[int(rng.integers(3))]
                applicable = moves[weight][
                    np.sum(chosen[moves[weight]], axis=1)
                    == weight // 2
                ]
                random_move = applicable[
                    int(rng.integers(len(applicable)))
                ]
                chosen[random_move] ^= 1
            assert int(chosen.sum()) == 39
            values = local.exact_values(
                chosen, constant, linear, quadratic
            )
            assert not np.any(np.remainder(values, 2))
            next_score = score(values)
            if next_score < current:
                stale = 0
            else:
                stale += 1
            current = next_score

    assert best_values is not None and best_chosen is not None
    return {
        "status": "UNKNOWN",
        "case": case_number,
        "block": case.block,
        "q_index": case.index,
        "affine_rank": rank,
        "weight_parity_rank": augmented_rank,
        "weight_parity_dimension": dimension,
        "null_move_counts": {
            str(weight): len(values)
            for weight, values in moves.items()
        },
        "seconds": time.monotonic() - started,
        "iterations": iterations,
        "restarts": restarts,
        "best_mod3_defect": best_score,
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
    parser.add_argument("--seconds", type=float, default=120)
    parser.add_argument("--seed", type=int, default=668_236)
    args = parser.parse_args()
    print(
        json.dumps(
            search(args.case, args.seconds, args.seed), indent=2
        )
    )


if __name__ == "__main__":
    main()
