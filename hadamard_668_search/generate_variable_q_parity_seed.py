#!/usr/bin/env python3
"""Generate a BS(84,83) shard state satisfying all endpoint XOR parities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from ortools.sat.python import cp_model

from search_variable_q_cp_sat import (
    add_alternating_sum,
    add_endpoint_product_parities,
    add_sign_sum,
)
from variable_q_base import (
    LONG,
    MARGIN_SHARDS,
    SHORT,
    base_correlations,
    base_to_special,
)


def build_model(
    shard: int,
) -> tuple[cp_model.CpModel, tuple[list[cp_model.IntVar], ...]]:
    model = cp_model.CpModel()
    sequences = tuple(
        [model.new_bool_var(f"{label}_{index}") for index in range(length)]
        for label, length in zip("abcd", (LONG, LONG, SHORT, SHORT), strict=True)
    )
    ordinary, alternating = MARGIN_SHARDS[shard]
    for bits, row_sum, alt_sum in zip(
        sequences, ordinary, alternating, strict=True
    ):
        add_sign_sum(model, bits, row_sum)
        add_alternating_sum(model, bits, alt_sum)
    add_endpoint_product_parities(model, sequences)
    return model, sequences


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shard", type=int, required=True)
    parser.add_argument("--random-seed", type=int, default=668)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--max-memory-mb",
        type=int,
        default=2048,
        help="CP-SAT memory cap in MiB (conservative default for a 16 GiB host)",
    )
    parser.add_argument(
        "--output", type=Path, default=Path("output/variable_q_parity_seed.json")
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if (
        not 0 <= args.shard < len(MARGIN_SHARDS)
        or args.workers <= 0
        or args.max_memory_mb <= 0
    ):
        print("error=invalid shard, worker count, or memory cap", file=sys.stderr)
        return 2
    print(f"workers={args.workers} max_memory_mb={args.max_memory_mb}")
    model, variables = build_model(args.shard)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    solver.parameters.random_seed = args.random_seed
    status = solver.solve(model)
    print(f"status={solver.status_name(status)}")
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return 2

    sequences = tuple(
        tuple(1 if solver.value(variable) else -1 for variable in bits)
        for bits in variables
    )
    correlations = base_correlations(*sequences)
    half_residuals = tuple(value // 2 for value in correlations[1:])
    if any(value % 2 for value in half_residuals):
        raise AssertionError("endpoint-parity seed has an odd half-residual")
    s, q = base_to_special(*sequences)
    ordinary, alternating = MARGIN_SHARDS[args.shard]
    payload = {
        "kind": "variable-q-bs-84-83-endpoint-parity-seed",
        "exact": not any(correlations[1:]),
        "hadamard_verified": False,
        "shard": args.shard,
        "ordinary_sums": list(ordinary),
        "alternating_sums": list(alternating),
        "a": list(sequences[0]),
        "b": list(sequences[1]),
        "c": list(sequences[2]),
        "d": list(sequences[3]),
        "s": list(s),
        "q": list(q),
        "base_correlations": list(correlations),
        "half_base_residuals_1_through_83": list(half_residuals),
        "energy_half_base": sum(value * value for value in half_residuals),
        "odd_half_residual_count": 0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"energy_half={payload['energy_half_base']}")
    print(f"output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
