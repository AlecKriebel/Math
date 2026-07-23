#!/usr/bin/env python3
"""Minimize distance from Eliahou's seed under exact BS spectral/parity layers.

This is not the full base-sequence model.  It imposes the necessary norm
identities at ``z=+1`` and ``z=-1`` together with the complete base-sequence
quad parity theorem, while allowing all raw margin patterns.  Optional root
and compression layers strengthen the relaxation.  Its optimum is therefore
a rigorous lower bound on the Hamming distance from the published seed to any
exact ``BS(84,83)``.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from itertools import product as cartesian_product
import json
from pathlib import Path
import sys

from ortools.sat.python import cp_model

from search_variable_q_cp_sat import (
    add_length_seven_compression_invariants,
    add_quad_product_parities,
    add_small_root_spectral_invariants,
    square,
)
from seed import ELIAHOU_Q, ELIAHOU_S
from variable_q_base import (
    LONG,
    MARGIN_SHARDS,
    SHORT,
    alternating_sum,
    base_quad_products,
    sign_sum,
    special_to_base,
)
from variable_q_compression import pad_to_period, periodic_autocorrelation


SEED = special_to_base(ELIAHOU_S, ELIAHOU_Q)
LENGTHS = (LONG, LONG, SHORT, SHORT)
ENERGY = 2 * (LONG + SHORT)


@dataclass(frozen=True)
class DistanceWitness:
    sequences: tuple[tuple[int, ...], ...]
    distance: int
    ordinary: tuple[int, ...]
    alternating: tuple[int, ...]


def raw_margin_images():
    """Yield every raw labeled margin image of the 288 canonical shards."""

    for shard, (ordinary, alternating) in enumerate(MARGIN_SHARDS):
        for swap_long in (False, True):
            for swap_short in (False, True):
                order = [0, 1, 2, 3]
                if swap_long:
                    order[0], order[1] = order[1], order[0]
                if swap_short:
                    order[2], order[3] = order[3], order[2]
                pairs = [(ordinary[index], alternating[index]) for index in order]
                for negations in cartesian_product((-1, 1), repeat=4):
                    signed = [
                        (row_sum * sign, alt_sum * sign)
                        for (row_sum, alt_sum), sign in zip(
                            pairs, negations, strict=True
                        )
                    ]
                    for reverse_a, reverse_b in cartesian_product(
                        (-1, 1), repeat=2
                    ):
                        raw = signed.copy()
                        raw[0] = (raw[0][0], raw[0][1] * reverse_a)
                        raw[1] = (raw[1][0], raw[1][1] * reverse_b)
                        yield shard, tuple(raw)


def margin_distance(
    target: tuple[tuple[int, int], ...],
    sequences: tuple[tuple[int, ...], ...] = SEED,
) -> int:
    """Exact minimum flips needed to attain one raw margin vector."""

    if len(target) != 4:
        raise ValueError("target must contain four ordinary/alternating pairs")
    current = tuple(
        (sign_sum(sequence), alternating_sum(sequence)) for sequence in sequences
    )
    return sum(
        (
            abs((row_sum + alt_sum) - (current_row + current_alt))
            + abs((row_sum - alt_sum) - (current_row - current_alt))
        )
        // 4
        for (row_sum, alt_sum), (current_row, current_alt) in zip(
            target, current, strict=True
        )
    )


def closest_margin_targets() -> tuple[int, tuple[tuple[int, tuple[tuple[int, int], ...]], ...]]:
    """Return the margin-only distance lower bound and all distinct minimizers."""

    best = 10**9
    witnesses: set[tuple[int, tuple[tuple[int, int], ...]]] = set()
    for shard, target in raw_margin_images():
        distance = margin_distance(target)
        record = (shard, target)
        if distance < best:
            best = distance
            witnesses = {record}
        elif distance == best:
            witnesses.add(record)
    return best, tuple(sorted(witnesses))


def minimum_class_flips(
    sequence: tuple[int, ...], target: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return ``(+->-, -->+)`` counts in even and odd coordinate classes."""

    current = (sign_sum(sequence), alternating_sum(sequence))
    current_classes = (
        (current[0] + current[1]) // 2,
        (current[0] - current[1]) // 2,
    )
    target_classes = (
        (target[0] + target[1]) // 2,
        (target[0] - target[1]) // 2,
    )
    result = []
    for before, after in zip(current_classes, target_classes, strict=True):
        change = (after - before) // 2
        result.append((max(-change, 0), max(change, 0)))
    return tuple(result)  # type: ignore[return-value]


def build_model(
    *,
    small_roots: bool = False,
    compression_7: bool = False,
    compression_7_alternating: bool = False,
) -> tuple[cp_model.CpModel, tuple[list[cp_model.IntVar], ...]]:
    model = cp_model.CpModel()
    sequences = tuple(
        [model.new_bool_var(f"{label}_{index}") for index in range(length)]
        for label, length in zip("abcd", LENGTHS, strict=True)
    )

    ordinary_squares = []
    alternating_squares = []
    for label, bits in zip("abcd", sequences, strict=True):
        bound = len(bits)
        ordinary = model.new_int_var(-bound, bound, f"{label}_ordinary")
        alternating = model.new_int_var(-bound, bound, f"{label}_alternating")
        model.add(ordinary == 2 * sum(bits) - bound)
        model.add(
            alternating
            == sum(
                (1 if index % 2 == 0 else -1) * (2 * bit - 1)
                for index, bit in enumerate(bits)
            )
        )
        ordinary_squares.append(square(model, ordinary, bound, f"{label}_ordinary2"))
        alternating_squares.append(
            square(model, alternating, bound, f"{label}_alternating2")
        )
    model.add(sum(ordinary_squares) == ENERGY)
    model.add(sum(alternating_squares) == ENERGY)
    add_quad_product_parities(model, sequences)

    if small_roots:
        add_small_root_spectral_invariants(model, sequences)
    if compression_7:
        add_length_seven_compression_invariants(model, sequences)
    if compression_7_alternating:
        add_length_seven_compression_invariants(
            model, sequences, coordinate_alternation=True
        )

    differences = []
    for bits, seed in zip(sequences, SEED, strict=True):
        for bit, sign in zip(bits, seed, strict=True):
            model.add_hint(bit, int(sign == 1))
            differences.append(bit.negated() if sign == 1 else bit)
    model.minimize(sum(differences))
    return model, sequences


def _signs(
    solver: cp_model.CpSolver, variables: list[cp_model.IntVar]
) -> tuple[int, ...]:
    return tuple(1 if solver.value(variable) else -1 for variable in variables)


def _small_root_norms(sequences: tuple[tuple[int, ...], ...]) -> tuple[int, int, int]:
    norms = []
    for modulus in (3, 4, 6):
        total = 0
        for sequence in sequences:
            padded = pad_to_period(sequence)
            residues = tuple(
                sum(padded[residue::modulus]) for residue in range(modulus)
            )
            if modulus == 3:
                a = residues[0] - residues[2]
                b = residues[1] - residues[2]
                total += a * a - a * b + b * b
            elif modulus == 4:
                real = residues[0] - residues[2]
                imaginary = residues[1] - residues[3]
                total += real * real + imaginary * imaginary
            else:
                a = residues[0] - residues[2] - residues[3] + residues[5]
                b = residues[1] + residues[2] - residues[4] - residues[5]
                total += a * a + a * b + b * b
        norms.append(total)
    return tuple(norms)  # type: ignore[return-value]


def _compressed_signature(
    sequences: tuple[tuple[int, ...], ...], *, coordinate_alternation: bool
) -> tuple[int, ...]:
    compressed = []
    for sequence in sequences:
        padded = pad_to_period(sequence)
        if coordinate_alternation:
            padded = tuple(
                value if index % 2 == 0 else -value
                for index, value in enumerate(padded)
            )
        compressed.append(
            tuple(sum(padded[residue::7]) for residue in range(7))
        )
    return tuple(
        sum(periodic_autocorrelation(vector, lag) for vector in compressed)
        for lag in range(4)
    )


def verify_witness(
    sequences: tuple[tuple[int, ...], ...],
    *,
    small_roots: bool,
    compression_7: bool,
    compression_7_alternating: bool,
) -> DistanceWitness:
    if len(sequences) != 4 or tuple(map(len, sequences)) != LENGTHS:
        raise ValueError("distance witness has the wrong sequence lengths")
    if any(value not in (-1, 1) for sequence in sequences for value in sequence):
        raise ValueError("distance witness contains a non-sign")
    ordinary = tuple(sign_sum(sequence) for sequence in sequences)
    alternating = tuple(alternating_sum(sequence) for sequence in sequences)
    if sum(value * value for value in ordinary) != ENERGY:
        raise ValueError("ordinary norm identity fails")
    if sum(value * value for value in alternating) != ENERGY:
        raise ValueError("alternating norm identity fails")
    long_products, short_products = base_quad_products(*sequences)
    if long_products != (-1,) + (1,) * 41 or short_products != (1,) * 41:
        raise ValueError("base-sequence quad parity fails")
    if small_roots and _small_root_norms(sequences) != (ENERGY,) * 3:
        raise ValueError("small-root norm propagation fails")
    if compression_7 and _compressed_signature(
        sequences, coordinate_alternation=False
    ) != (ENERGY, 0, 0, 0):
        raise ValueError("primitive-seven compression fails")
    if compression_7_alternating and _compressed_signature(
        sequences, coordinate_alternation=True
    ) != (ENERGY, 0, 0, 0):
        raise ValueError("primitive-fourteen compression fails")
    distance = sum(
        value != seed_value
        for sequence, seed in zip(sequences, SEED, strict=True)
        for value, seed_value in zip(sequence, seed, strict=True)
    )
    return DistanceWitness(sequences, distance, ordinary, alternating)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--small-roots", action="store_true")
    parser.add_argument("--compression-7", action="store_true")
    parser.add_argument("--compression-7-alternating", action="store_true")
    parser.add_argument("--time-limit", type=float, default=300.0)
    parser.add_argument("--max-memory-mb", type=int, default=256)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.time_limit <= 0 or args.max_memory_mb <= 0:
        print("error=time and memory limits must be positive", file=sys.stderr)
        return 2
    model, variables = build_model(
        small_roots=args.small_roots,
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
    status = solver.solve(model)
    print(f"status={solver.status_name(status)}")
    print(f"wall_time={solver.wall_time:.3f}")
    print(f"conflicts={solver.num_conflicts}")
    print(f"branches={solver.num_branches}")
    print(f"best_bound={solver.best_objective_bound}")
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return 1
    sequences = tuple(_signs(solver, variables_) for variables_ in variables)
    witness = verify_witness(
        sequences,
        small_roots=args.small_roots,
        compression_7=args.compression_7,
        compression_7_alternating=args.compression_7_alternating,
    )
    print(f"distance={witness.distance}")
    print(f"ordinary={witness.ordinary}")
    print(f"alternating={witness.alternating}")
    if args.output:
        seed_bytes = json.dumps(
            {"a": SEED[0], "b": SEED[1], "c": SEED[2], "d": SEED[3]},
            separators=(",", ":"),
        ).encode()
        payload = {
            "kind": "variable-q-seed-distance-relaxation",
            "optimal": status == cp_model.OPTIMAL,
            "distance": witness.distance,
            "ordinary_sums": list(witness.ordinary),
            "alternating_sums": list(witness.alternating),
            "layers": {
                "small_roots": args.small_roots,
                "compression_7": args.compression_7,
                "compression_7_alternating": args.compression_7_alternating,
            },
            "seed_base_sha256": hashlib.sha256(seed_bytes).hexdigest(),
            "a": list(witness.sequences[0]),
            "b": list(witness.sequences[1]),
            "c": list(witness.sequences[2]),
            "d": list(witness.sequences[3]),
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
