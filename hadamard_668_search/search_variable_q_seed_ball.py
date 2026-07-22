#!/usr/bin/env python3
"""Exact unsharded BS(84,83) search near Eliahou's published base seed.

Unlike the shard-213 checkpoint experiment, this model fixes no ordinary or
alternating margins.  It searches the raw 334 labeled signs within a Hamming
ball around the published seed and imposes all 83 base-sequence correlation
equations.  Thus an ``INFEASIBLE`` status excludes the full raw ball at the
selected radius, across every margin shard.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from ortools.sat.python import cp_model

from construction import goethals_seidel, verify_hadamard
from search_variable_q_cp_sat import equality_literal
from seed import special_quadruple, summed_aperiodic_correlations
from variable_q_base import (
    LONG,
    base_correlations,
    base_to_special,
)
from variable_q_seed_distance import SEED, build_model as build_relaxation


def build_model(
    radius: int,
    *,
    compression_7: bool = False,
    compression_7_alternating: bool = False,
) -> tuple[cp_model.CpModel, tuple[list[cp_model.IntVar], ...]]:
    if radius < 0:
        raise ValueError("radius must be nonnegative")
    model, sequences = build_relaxation(
        small_roots=True,
        compression_7=compression_7,
        compression_7_alternating=compression_7_alternating,
    )
    model.clear_objective()
    for lag in range(1, LONG):
        terms = []
        for label, bits in zip("abcd", sequences, strict=True):
            terms.extend(
                equality_literal(
                    model,
                    bits[index],
                    bits[index + lag],
                    f"{label}{label}_seed_ball_{lag}_{index}",
                )
                for index in range(len(bits) - lag)
            )
        model.add(sum(terms) == len(terms) // 2)

    differences = [
        bit.negated() if seed_value == 1 else bit
        for bits, seed in zip(sequences, SEED, strict=True)
        for bit, seed_value in zip(bits, seed, strict=True)
    ]
    model.add(sum(differences) <= radius).with_name(
        "maximum_published_seed_hamming_distance"
    )
    return model, sequences


def _signs(
    solver: cp_model.CpSolver, variables: list[cp_model.IntVar]
) -> tuple[int, ...]:
    return tuple(1 if solver.value(variable) else -1 for variable in variables)


def save_exact(
    path: Path,
    sequences: tuple[tuple[int, ...], ...],
    radius: int,
) -> None:
    correlations = base_correlations(*sequences)
    if correlations != (334,) + (0,) * 83:
        raise AssertionError("seed-ball solver output failed exact base correlations")
    s, q = base_to_special(*sequences)
    special = summed_aperiodic_correlations(special_quadruple(s, q))
    if any(special[1:]):
        raise AssertionError("seed-ball output failed exact special correlations")
    matrix = goethals_seidel(special_quadruple(s, q))
    verify_hadamard(matrix)
    distance = sum(
        value != seed_value
        for sequence, seed in zip(sequences, SEED, strict=True)
        for value, seed_value in zip(sequence, seed, strict=True)
    )
    if distance > radius:
        raise AssertionError("decoded candidate lies outside the requested ball")
    payload = {
        "kind": "exact-variable-q-seed-ball-solution",
        "length": 167,
        "hadamard_order": 668,
        "hadamard_verified": True,
        "published_seed_hamming_distance": distance,
        "a": list(sequences[0]),
        "b": list(sequences[1]),
        "c": list(sequences[2]),
        "d": list(sequences[3]),
        "s": list(s),
        "q": list(q),
        "base_correlations": list(correlations),
        "special_correlations": list(special),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--radius", type=int, required=True)
    parser.add_argument("--compression-7", action="store_true")
    parser.add_argument("--compression-7-alternating", action="store_true")
    parser.add_argument("--time-limit", type=float, default=300.0)
    parser.add_argument("--max-memory-mb", type=int, default=1024)
    parser.add_argument("--random-seed", type=int, default=668)
    parser.add_argument(
        "--output", type=Path, default=Path("output/variable_q_seed_ball_exact.json")
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.radius < 0 or args.time_limit <= 0 or args.max_memory_mb <= 0:
        print("error=radius must be nonnegative and limits positive", file=sys.stderr)
        return 2
    model, variables = build_model(
        args.radius,
        compression_7=args.compression_7,
        compression_7_alternating=args.compression_7_alternating,
    )
    validation = model.validate()
    if validation:
        print(f"error=invalid model: {validation}", file=sys.stderr)
        return 2
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = 1
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    solver.parameters.random_seed = args.random_seed
    status = solver.solve(model)
    print(f"radius={args.radius}")
    print(f"workers=1 max_memory_mb={args.max_memory_mb}")
    print(f"status={solver.status_name(status)}")
    print(f"wall_time={solver.wall_time:.3f}")
    print(f"conflicts={solver.num_conflicts}")
    print(f"branches={solver.num_branches}")
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return 2 if status == cp_model.INFEASIBLE else 1
    sequences = tuple(_signs(solver, variables_) for variables_ in variables)
    save_exact(args.output, sequences, args.radius)
    print(f"wrote={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
