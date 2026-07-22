#!/usr/bin/env python3
"""Joint primitive-7/primitive-14 compression filter for ``BS(84,83)``.

For a sign sequence ``X``, let ``U`` be its factor-12 compression modulo
seven and let ``V`` be the same compression after coordinate alternation
``X_i -> (-1)^i X_i``.  Each pair ``(U_r,V_r)`` has a tiny exact alphabet
determined by the even- and odd-coordinate sign counts inside that residue
cell.  A base sequence must make both compressed quadruples periodically
complementary with signature ``(334,0,0,0)``.

This is a finite necessary-condition filter.  A feasible cell witness is not
an exact base sequence; an infeasible shard model does rule out that shard.
Models are solved sequentially with one worker and a conservative memory cap.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import sys
from typing import Sequence

from ortools.sat.python import cp_model

from run_variable_q_shards import parse_shards
from seed import validate_sign_sequence
from variable_q_base import (
    LONG,
    MARGIN_SHARDS,
    SHORT,
)
from variable_q_compression import periodic_autocorrelation


MODULUS = 7
ENERGY = 2 * (LONG + SHORT)
TARGET_SIGNATURE = (ENERGY, 0, 0, 0)
LENGTHS = (LONG, LONG, SHORT, SHORT)


@dataclass(frozen=True)
class JointWitness:
    shard: int
    ordinary: tuple[tuple[int, ...], ...]
    alternated: tuple[tuple[int, ...], ...]


def joint_cell_pairs(length: int, residue: int) -> tuple[tuple[int, int], ...]:
    """Return every exact ``(ordinary, alternated)`` residue-cell sum."""

    if length not in (LONG, SHORT):
        raise ValueError(f"length must be {LONG} or {SHORT}")
    if not 0 <= residue < MODULUS:
        raise ValueError("residue must lie in 0..6")
    positions = tuple(range(residue, length, MODULUS))
    positive_parity = sum(index % 2 == 0 for index in positions)
    negative_parity = len(positions) - positive_parity
    positive_sums = range(-positive_parity, positive_parity + 1, 2)
    negative_sums = range(-negative_parity, negative_parity + 1, 2)
    return tuple(
        sorted(
            {
                (left + right, left - right)
                for left in positive_sums
                for right in negative_sums
            }
        )
    )


def joint_compress(sequence: Sequence[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return the raw and coordinate-alternated length-seven compressions."""

    validate_sign_sequence(sequence)
    if len(sequence) not in (LONG, SHORT):
        raise ValueError(f"sequence length must be {LONG} or {SHORT}")
    ordinary = tuple(
        sum(sequence[index] for index in range(residue, len(sequence), MODULUS))
        for residue in range(MODULUS)
    )
    alternated = tuple(
        sum(
            (1 if index % 2 == 0 else -1) * sequence[index]
            for index in range(residue, len(sequence), MODULUS)
        )
        for residue in range(MODULUS)
    )
    return ordinary, alternated


def compressed_signature(vector: Sequence[int]) -> tuple[int, int, int, int]:
    values = tuple(vector)
    if len(values) != MODULUS:
        raise ValueError("compressed vector must have length seven")
    return tuple(periodic_autocorrelation(values, lag) for lag in range(4))  # type: ignore[return-value]


def summed_signature(vectors: Sequence[Sequence[int]]) -> tuple[int, ...]:
    if len(vectors) != 4:
        raise ValueError("exactly four compressed vectors are required")
    signatures = tuple(compressed_signature(vector) for vector in vectors)
    return tuple(sum(signature[lag] for signature in signatures) for lag in range(4))


def _product(
    model: cp_model.CpModel,
    left: cp_model.IntVar,
    right: cp_model.IntVar,
    name: str,
) -> cp_model.IntVar:
    result = model.new_int_var(-144, 144, name)
    model.add_multiplication_equality(result, (left, right))
    return result


def build_model(
    shard: int,
) -> tuple[
    cp_model.CpModel,
    tuple[tuple[list[cp_model.IntVar], ...], tuple[list[cp_model.IntVar], ...]],
]:
    """Build the exact joint compression relaxation for one margin shard."""

    if not 0 <= shard < len(MARGIN_SHARDS):
        raise ValueError(f"shard must lie in 0..{len(MARGIN_SHARDS) - 1}")
    model = cp_model.CpModel()
    raw_vectors: list[list[cp_model.IntVar]] = []
    alt_vectors: list[list[cp_model.IntVar]] = []
    for label, length in zip("abcd", LENGTHS, strict=True):
        raw = []
        alt = []
        for residue in range(MODULUS):
            pairs = joint_cell_pairs(length, residue)
            raw_cell = model.new_int_var(
                min(pair[0] for pair in pairs),
                max(pair[0] for pair in pairs),
                f"{label}_raw_{residue}",
            )
            alt_cell = model.new_int_var(
                min(pair[1] for pair in pairs),
                max(pair[1] for pair in pairs),
                f"{label}_alt_{residue}",
            )
            model.add_allowed_assignments((raw_cell, alt_cell), pairs)
            raw.append(raw_cell)
            alt.append(alt_cell)
        raw_vectors.append(raw)
        alt_vectors.append(alt)

    ordinary_margins, alternating_margins = MARGIN_SHARDS[shard]
    for raw, alt, ordinary, alternating in zip(
        raw_vectors,
        alt_vectors,
        ordinary_margins,
        alternating_margins,
        strict=True,
    ):
        model.add(sum(raw) == ordinary)
        model.add(sum(alt) == alternating)

    for layer_name, vectors in (("raw", raw_vectors), ("alt", alt_vectors)):
        for lag, target in enumerate(TARGET_SIGNATURE):
            terms = [
                _product(
                    model,
                    vector[index],
                    vector[(index + lag) % MODULUS],
                    f"{layer_name}_paf_{lag}_{which}_{index}",
                )
                for which, vector in enumerate(vectors)
                for index in range(MODULUS)
            ]
            model.add(sum(terms) == target)

    # The primary cell sums are the only genuine choices; multiplication
    # auxiliaries are consequences.
    model.add_decision_strategy(
        [cell for vector in (*raw_vectors, *alt_vectors) for cell in vector],
        cp_model.CHOOSE_MIN_DOMAIN_SIZE,
        cp_model.SELECT_MIN_VALUE,
    )
    return model, (tuple(raw_vectors), tuple(alt_vectors))


def decode_witness(
    solver: cp_model.CpSolver,
    shard: int,
    variables: tuple[
        tuple[list[cp_model.IntVar], ...], tuple[list[cp_model.IntVar], ...]
    ],
) -> JointWitness:
    raw, alt = variables
    witness = JointWitness(
        shard,
        tuple(tuple(solver.value(cell) for cell in vector) for vector in raw),
        tuple(tuple(solver.value(cell) for cell in vector) for vector in alt),
    )
    verify_witness(witness)
    return witness


def verify_witness(witness: JointWitness) -> None:
    """Independently check a joint compressed witness using integers."""

    if not 0 <= witness.shard < len(MARGIN_SHARDS):
        raise ValueError("witness shard is out of range")
    if len(witness.ordinary) != 4 or len(witness.alternated) != 4:
        raise ValueError("witness must contain four vectors in each layer")
    ordinary_margins, alternating_margins = MARGIN_SHARDS[witness.shard]
    for which, (raw, alt, length) in enumerate(
        zip(witness.ordinary, witness.alternated, LENGTHS, strict=True)
    ):
        if len(raw) != MODULUS or len(alt) != MODULUS:
            raise ValueError("every compressed vector must have length seven")
        if any(
            (raw[residue], alt[residue]) not in joint_cell_pairs(length, residue)
            for residue in range(MODULUS)
        ):
            raise ValueError(f"sequence {which} contains an impossible cell pair")
        if sum(raw) != ordinary_margins[which]:
            raise ValueError(f"sequence {which} has the wrong ordinary margin")
        if sum(alt) != alternating_margins[which]:
            raise ValueError(f"sequence {which} has the wrong alternating margin")
    if summed_signature(witness.ordinary) != TARGET_SIGNATURE:
        raise ValueError("ordinary compressed PAF signature is not complementary")
    if summed_signature(witness.alternated) != TARGET_SIGNATURE:
        raise ValueError("alternated compressed PAF signature is not complementary")


def solve_shard(
    shard: int,
    *,
    time_limit: float = 30.0,
    max_memory_mb: int = 256,
) -> tuple[str, JointWitness | None, cp_model.CpSolver]:
    if time_limit <= 0 or max_memory_mb <= 0:
        raise ValueError("time and memory limits must be positive")
    model, variables = build_model(shard)
    validation = model.validate()
    if validation:
        raise ValueError(f"invalid joint-compression model: {validation}")
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 1
    solver.parameters.max_memory_in_mb = max_memory_mb
    status = solver.solve(model)
    name = solver.status_name(status)
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return name, None, solver
    return name, decode_witness(solver, shard, variables), solver


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--shards",
        default="213",
        help="all (156 alternation representatives), 0-287, or comma list",
    )
    parser.add_argument("--time-limit", type=float, default=30.0)
    parser.add_argument("--max-memory-mb", type=int, default=256)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.time_limit <= 0 or args.max_memory_mb <= 0:
        print("error=time and memory limits must be positive", file=sys.stderr)
        return 2
    try:
        shards = parse_shards(args.shards)
    except ValueError as error:
        print(f"error={error}", file=sys.stderr)
        return 2

    records = []
    for ordinal, shard in enumerate(shards, 1):
        status, witness, solver = solve_shard(
            shard,
            time_limit=args.time_limit,
            max_memory_mb=args.max_memory_mb,
        )
        record: dict[str, object] = {
            "shard": shard,
            "ordinary_margins": list(MARGIN_SHARDS[shard][0]),
            "alternating_margins": list(MARGIN_SHARDS[shard][1]),
            "status": status,
            "wall_time": solver.wall_time,
            "conflicts": solver.num_conflicts,
            "branches": solver.num_branches,
        }
        if witness is not None:
            record["ordinary_compression"] = [list(vector) for vector in witness.ordinary]
            record["alternated_compression"] = [list(vector) for vector in witness.alternated]
        records.append(record)
        print(
            f"attempt={ordinal}/{len(shards)} shard={shard} status={status} "
            f"wall_time={solver.wall_time:.3f} branches={solver.num_branches}",
            flush=True,
        )

    payload = {
        "kind": "joint-primitive-7-14-compression-search",
        "base_lengths": list(LENGTHS),
        "workers": 1,
        "max_memory_mb": args.max_memory_mb,
        "time_limit_per_shard": args.time_limit,
        "records": records,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote={args.output}")
    infeasible = sum(record["status"] == "INFEASIBLE" for record in records)
    unknown = sum(record["status"] == "UNKNOWN" for record in records)
    print(f"infeasible={infeasible} feasible={len(records)-infeasible-unknown} unknown={unknown}")
    return 1 if unknown else 0


if __name__ == "__main__":
    raise SystemExit(main())
