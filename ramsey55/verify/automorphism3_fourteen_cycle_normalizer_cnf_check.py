#!/usr/bin/env python3
"""Independent checker for normalizer-reduced 3^14 1 certificate CNFs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

from automorphism3_fourteen_cycle_degree_cnf_check import (  # noqa: E402
    independent_degree_encoding,
)
from automorphism3_fourteen_cycle_symmetry_cnf_check import (  # noqa: E402
    expected_formula,
)
from automorphism_orbit_cnf_check import (  # noqa: E402
    independently_build,
    read_dimacs,
)


CHECKER_ID = "ramsey55_order3_fourteen_cycle_normalizer_cnf_checker_v1"
CANONICAL_TRIPLES = (
    (False, False, False),
    (True, False, False),
    (True, True, False),
    (True, True, True),
)


def digest(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def independent_normalizer(
    orbits: tuple[tuple[tuple[int, int], ...], ...],
    root_cycles: int,
    first_auxiliary: int,
) -> tuple[tuple[tuple[int, ...], ...], int, dict[str, int]]:
    edge_variable = {
        edge: variable
        for variable, orbit in enumerate(orbits, start=1)
        for edge in orbit
    }

    def triple(cycle: int) -> tuple[int, int, int]:
        return tuple(
            edge_variable[(0, 3 * cycle + offset)]
            for offset in range(3)
        )

    def profile(cycle: int, prefix: range) -> tuple[int, ...]:
        result = [edge_variable[(3 * cycle, 3 * cycle + 1)]]
        for previous in prefix:
            for offset in range(3):
                edge = tuple(
                    sorted((3 * previous, 3 * cycle + offset))
                )
                result.append(edge_variable[edge])
        return tuple(result)

    def compare(
        left: tuple[int, ...],
        right: tuple[int, ...],
        next_variable: int,
    ) -> tuple[list[tuple[int, ...]], int]:
        result: list[tuple[int, ...]] = []
        equal: int | None = None
        for index in range(len(left)):
            left_bit, right_bit = left[index], right[index]
            result.append(
                (left_bit, -right_bit)
                if equal is None
                else (-equal, left_bit, -right_bit)
            )
            if index == len(left) - 1:
                continue
            next_equal = next_variable
            next_variable += 1
            if equal is None:
                result.extend(
                    (
                        (-next_equal, -left_bit, right_bit),
                        (-next_equal, left_bit, -right_bit),
                        (next_equal, left_bit, right_bit),
                        (next_equal, -left_bit, -right_bit),
                    )
                )
            else:
                result.extend(
                    (
                        (-next_equal, equal),
                        (-next_equal, -left_bit, right_bit),
                        (-next_equal, left_bit, -right_bit),
                        (-equal, -left_bit, -right_bit, next_equal),
                        (-equal, left_bit, right_bit, next_equal),
                    )
                )
            equal = next_equal
        return result, next_variable

    output: list[tuple[int, ...]] = []
    for cycle in range(1, 14):
        x0, x1, x2 = triple(cycle)
        output.extend(((x0, -x1), (x1, -x2)))
    groups = (
        tuple(range(1, root_cycles)),
        tuple(range(root_cycles, 14)),
    )
    next_variable = first_auxiliary
    compared_bits = 0
    comparator_count = 0
    for group in groups:
        for left_cycle, right_cycle in zip(group, group[1:]):
            comparator_count += 1
            left = profile(left_cycle, range(left_cycle))
            right = profile(right_cycle, range(left_cycle))
            compared_bits += len(left)
            clauses, next_variable = compare(left, right, next_variable)
            output.extend(clauses)
    expected_clauses = 1_340 if root_cycles == 6 else 1_322
    if len(output) != expected_clauses:
        raise AssertionError("bad independent normalizer clause count")
    return (
        tuple(output),
        next_variable,
        {
            "independent_phase_shift_clauses": 26,
            "residual_block_comparators": comparator_count,
            "lexicographically_compared_bits": compared_bits,
            "residual_block_order_clauses": len(output) - 26,
            "normalizer_auxiliary_variable_count": (
                next_variable - first_auxiliary
            ),
        },
    )


def normalizer_cover_audit() -> dict[str, object]:
    rotations = {
        bits: tuple(
            max(
                tuple(bits[(index + shift) % 3] for index in range(3))
                for shift in range(3)
            )
        )
        for bits in itertools.product((False, True), repeat=3)
    }
    images = set(rotations.values())
    valid = images == set(CANONICAL_TRIPLES) and all(
        image[0] >= image[1] >= image[2] for image in images
    )
    # Sorting is audited over every pair of the eight possible four-bit keys.
    keys = tuple(
        (internal, *triple)
        for internal in (False, True)
        for triple in CANONICAL_TRIPLES
    )
    pair_checks = sum(1 for _ in itertools.product(keys, repeat=2))
    return {
        "valid": valid and pair_checks == 64,
        "three_bit_patterns_checked": len(rotations),
        "canonical_triples": [list(item) for item in sorted(images)],
        "ordered_key_pairs_checked": pair_checks,
    }


def check(cnf: Path, metadata_path: Path) -> dict[str, object]:
    started = time.monotonic()
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    root_cycles = metadata.get("root_neighbor_cycle_count")
    if root_cycles not in (6, 7):
        raise ValueError("invalid root-neighbor case")
    mode = f"{root_cycles}-reduced"
    primary, base_units, _, reduced_count, full_count = expected_formula(mode)
    reduced = base_units[:reduced_count]
    units = base_units[reduced_count:]
    _, orbits, _ = independently_build(3, 14)
    degree, next_variable, final_states = independent_degree_encoding(
        orbits, primary + 1
    )
    normalizer, final_next_variable, normalizer_metadata = (
        independent_normalizer(orbits, root_cycles, next_variable)
    )
    expected = (*reduced, *units, *normalizer, *degree)
    variables, declared, actual = read_dimacs(cnf)
    first_mismatch = None
    for index, pair in enumerate(
        itertools.zip_longest(expected, actual), start=1
    ):
        if pair[0] != pair[1]:
            first_mismatch = {
                "clause_index": index,
                "expected": list(pair[0]) if pair[0] is not None else None,
                "actual": list(pair[1]) if pair[1] is not None else None,
            }
            break
    cover = normalizer_cover_audit()
    expected_variables = final_next_variable - 1
    cnf_sha256 = digest(cnf)
    metadata_valid = (
        metadata.get("order") == 43
        and metadata.get("clique_size") == 5
        and metadata.get("automorphism_order") == 3
        and metadata.get("cycle_count") == 14
        and metadata.get("fixed_point_count") == 1
        and metadata.get("cycle_type") == "3^14 1"
        and metadata.get("base_mode") == mode
        and metadata.get("primary_variable_count") == primary
        and metadata.get("variable_count") == expected_variables
        and metadata.get("full_ramsey_clause_count") == full_count
        and metadata.get("reduced_ramsey_clause_count") == reduced_count
        and metadata.get("root_unit_clause_count") == len(units)
        and metadata.get("normalizer_clause_count") == len(normalizer)
        and all(
            metadata.get("normalizer", {}).get(key) == value
            for key, value in normalizer_metadata.items()
        )
        and metadata.get("degree_clause_count") == len(degree)
        and metadata.get("final_state_variables") == final_states
        and metadata.get("clause_count") == len(expected)
        and metadata.get("total_auxiliary_variable_count")
        == expected_variables - primary
        and metadata.get("cnf_sha256") == cnf_sha256
        and metadata.get("cnf_bytes") == cnf.stat().st_size
    )
    valid = (
        variables == expected_variables
        and declared == len(expected)
        and len(actual) == len(expected)
        and first_mismatch is None
        and metadata_valid
        and cover["valid"]
    )
    return {
        "checker": CHECKER_ID,
        "valid": valid,
        "claim_scope": (
            f"Exact normalizer-reduced root case m={root_cycles} for "
            "cycle type 3^14 1."
        ),
        "root_neighbor_cycle_count": root_cycles,
        "primary_variable_count": primary,
        "variable_count": expected_variables,
        "full_ramsey_clause_count": full_count,
        "reduced_ramsey_clause_count": reduced_count,
        "root_unit_clause_count": len(units),
        "normalizer_clause_count": len(normalizer),
        "degree_clause_count": len(degree),
        "expected_clause_count": len(expected),
        "actual_clause_count": len(actual),
        "normalizer_cover_audit": cover,
        "metadata_valid": metadata_valid,
        "first_mismatch": first_mismatch,
        "cnf_sha256": cnf_sha256,
        "cnf_bytes": cnf.stat().st_size,
        "runtime_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = check(args.cnf, args.metadata)
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
