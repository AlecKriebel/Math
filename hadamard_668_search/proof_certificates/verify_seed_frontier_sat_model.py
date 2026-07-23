#!/usr/bin/env python3
"""Independently verify a SAT model emitted for an exported frontier CNF."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from variable_q_base import (  # noqa: E402
    alternating_sum,
    base_quad_products,
    sign_sum,
)
from variable_q_compression import (  # noqa: E402
    pad_to_period,
    periodic_autocorrelation,
)
from verify_variable_q_seed_quad_radius import check_radius  # noqa: E402
from verify_variable_q_seed_radius import SEED  # noqa: E402


ENERGY = 334
ROOT_COEFFICIENT_PAIRS = {
    3: ((1, 0, -1), (0, 1, -1), -1),
    4: ((1, 0, -1, 0), (0, 1, 0, -1), 0),
    6: ((1, 0, -1, -1, 0, 1), (0, 1, 1, 0, -1, -1), 1),
}


def _parse_model(path: Path) -> dict[int, bool]:
    assignment: dict[int, bool] = {}
    status = None
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("s "):
            status = line[2:].strip()
        if not line.startswith("v "):
            continue
        for entry in line[2:].split():
            literal = int(entry)
            if literal == 0:
                continue
            variable = abs(literal)
            value = literal > 0
            if variable in assignment and assignment[variable] != value:
                raise ValueError("SAT output assigns one variable both ways")
            assignment[variable] = value
    if status != "SATISFIABLE":
        raise ValueError("solver output does not report SATISFIABLE")
    return assignment


def _verify_dimacs(
    path: Path, expected_sha256: str, assignment: dict[int, bool]
) -> tuple[int, int]:
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("CNF checksum differs from metadata")
    variables = clauses = None
    observed_clauses = 0
    with path.open("r", encoding="ascii") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line or line[0] == "c":
                continue
            if line.startswith("p "):
                fields = line.split()
                if len(fields) != 4 or fields[1] != "cnf":
                    raise ValueError("invalid DIMACS header")
                variables, clauses = int(fields[2]), int(fields[3])
                continue
            literals = [int(entry) for entry in line.split()]
            if not literals or literals[-1] != 0:
                raise ValueError(f"unterminated clause at line {line_number}")
            observed_clauses += 1
            if not any(
                assignment.get(abs(literal)) == (literal > 0)
                for literal in literals[:-1]
            ):
                raise ValueError(
                    f"SAT assignment falsifies clause at line {line_number}"
                )
    if variables is None or clauses is None:
        raise ValueError("missing DIMACS header")
    if observed_clauses != clauses:
        raise ValueError("DIMACS clause count differs from header")
    if any(variable not in assignment for variable in range(1, variables + 1)):
        raise ValueError("SAT assignment is incomplete")
    return variables, clauses


def _small_root_norms(
    sequences: tuple[tuple[int, ...], ...]
) -> tuple[int, int, int]:
    totals = []
    for modulus, (
        first_pattern,
        second_pattern,
        cross_sign,
    ) in ROOT_COEFFICIENT_PAIRS.items():
        total = 0
        for sequence in sequences:
            first = sum(
                first_pattern[index % modulus] * value
                for index, value in enumerate(sequence)
            )
            second = sum(
                second_pattern[index % modulus] * value
                for index, value in enumerate(sequence)
            )
            total += (
                first * first
                + cross_sign * first * second
                + second * second
            )
        totals.append(total)
    return tuple(totals)  # type: ignore[return-value]


def _compression_signature(
    sequences: tuple[tuple[int, ...], ...],
    *,
    coordinate_alternation: bool,
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


def _verify_sorted_quad_orbits(
    flips: tuple[tuple[bool, ...], ...]
) -> int:
    comparisons = 0
    for first_index, second_index in ((0, 1), (2, 3)):
        length = len(flips[first_index])
        groups: dict[tuple, list[int]] = {}
        for left in range(length // 2):
            right = length - 1 - left
            coordinates = (
                (first_index, left),
                (first_index, right),
                (second_index, left),
                (second_index, right),
            )
            key = (
                first_index,
                left % 12,
                right % 12,
                tuple(
                    SEED[index][coordinate]
                    for index, coordinate in coordinates
                ),
            )
            mask = sum(
                int(flips[index][coordinate]) << bit
                for bit, (index, coordinate) in enumerate(coordinates)
            )
            groups.setdefault(key, []).append(mask)
        for orbit in groups.values():
            if orbit != sorted(orbit):
                raise ValueError("exchangeable quad masks are not sorted")
            comparisons += max(0, len(orbit) - 1)
    return comparisons


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
        if metadata.get("kind") != "seed-frontier-root-cnf":
            raise ValueError("wrong metadata kind")
        assignment = _parse_model(args.model)
        variables, clauses = _verify_dimacs(
            args.cnf, metadata["cnf_sha256"], assignment
        )
        cursor = 1
        flip_groups = []
        sequences = []
        for seed in SEED:
            flips = tuple(
                assignment[variable]
                for variable in range(cursor, cursor + len(seed))
            )
            cursor += len(seed)
            flip_groups.append(flips)
            sequences.append(
                tuple(
                    -value if flip else value
                    for value, flip in zip(seed, flips, strict=True)
                )
            )
        sequence_tuple = tuple(sequences)
        flip_tuple = tuple(flip_groups)
        target = tuple(tuple(pair) for pair in metadata["target"])
        observed_target = tuple(
            (sign_sum(sequence), alternating_sum(sequence))
            for sequence in sequence_tuple
        )
        if observed_target != target:
            raise ValueError("decoded sequence has the wrong fixed margins")
        distance = sum(flip for group in flip_tuple for flip in group)
        if not metadata["minimum_distance"] <= distance <= metadata["radius"]:
            raise ValueError("decoded sequence has the wrong Hamming distance")
        long_products, short_products = base_quad_products(*sequence_tuple)
        if long_products != (-1,) + (1,) * 41:
            raise ValueError("decoded long endpoint-quad products fail")
        if short_products != (1,) * 41:
            raise ValueError("decoded short endpoint-quad products fail")
        if _small_root_norms(sequence_tuple) != (ENERGY,) * 3:
            raise ValueError("decoded small-root norms fail")

        records = {
            (record.shard, record.target): record
            for record in check_radius(metadata["radius"]).targets
        }
        record = records[(metadata["shard"], target)]
        long_distance = sum(flip for group in flip_tuple[:2] for flip in group)
        short_distance = sum(flip for group in flip_tuple[2:] for flip in group)
        if (
            record.long_distance is None
            or record.short_distance is None
            or long_distance < record.long_distance
            or short_distance < record.short_distance
        ):
            raise ValueError("decoded pair distance violates a lower bound")

        comparisons = 0
        if metadata.get("exchangeable_quad_symmetry") is True:
            comparisons = _verify_sorted_quad_orbits(flip_tuple)
        if metadata.get("compression") in {"z7", "both"}:
            if _compression_signature(
                sequence_tuple, coordinate_alternation=False
            ) != (ENERGY, 0, 0, 0):
                raise ValueError("decoded primitive-7 compression fails")
        if metadata.get("compression") in {"z14", "both"}:
            if _compression_signature(
                sequence_tuple, coordinate_alternation=True
            ) != (ENERGY, 0, 0, 0):
                raise ValueError("decoded primitive-14 compression fails")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(
        f"PASS: SAT assignment satisfies all {clauses} CNF clauses and "
        "independent frontier checks"
    )
    print(f"variables={variables} distance={distance}")
    print(f"margins={observed_target}")
    print(f"small_root_norms={_small_root_norms(sequence_tuple)}")
    print(
        f"pair_distance=({long_distance},{short_distance}) "
        f"sorted_quad_comparisons={comparisons}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
