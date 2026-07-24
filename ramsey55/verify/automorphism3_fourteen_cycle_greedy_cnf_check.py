#!/usr/bin/env python3
"""Independent checker for greedy-normalized 3^14 1 case CNFs."""

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


CHECKER_ID = "ramsey55_order3_fourteen_cycle_greedy_cnf_checker_v1"


def digest(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def independent_oriented_profile(
    edge_variable: dict[tuple[int, int], int],
    candidate: int,
    prefix: range,
    shift: int,
) -> tuple[int, ...]:
    result = [edge_variable[(3 * candidate, 3 * candidate + 1)]]
    for previous in prefix:
        for offset in range(3):
            edge = tuple(
                sorted(
                    (
                        3 * previous,
                        3 * candidate + (offset + shift) % 3,
                    )
                )
            )
            result.append(edge_variable[edge])
    return tuple(result)


def independent_lex_ge(
    left: tuple[int, ...],
    right: tuple[int, ...],
    next_variable: int,
) -> tuple[list[tuple[int, ...]], int]:
    output: list[tuple[int, ...]] = []
    previous_equal: int | None = None
    for index, (left_bit, right_bit) in enumerate(zip(left, right)):
        output.append(
            (left_bit, -right_bit)
            if previous_equal is None
            else (-previous_equal, left_bit, -right_bit)
        )
        if index == len(left) - 1:
            continue
        current_equal = next_variable
        next_variable += 1
        if previous_equal is None:
            output.extend(
                (
                    (-current_equal, -left_bit, right_bit),
                    (-current_equal, left_bit, -right_bit),
                    (current_equal, left_bit, right_bit),
                    (current_equal, -left_bit, -right_bit),
                )
            )
        else:
            output.extend(
                (
                    (-current_equal, previous_equal),
                    (-current_equal, -left_bit, right_bit),
                    (-current_equal, left_bit, -right_bit),
                    (
                        -previous_equal,
                        -left_bit,
                        -right_bit,
                        current_equal,
                    ),
                    (
                        -previous_equal,
                        left_bit,
                        right_bit,
                        current_equal,
                    ),
                )
            )
        previous_equal = current_equal
    return output, next_variable


def independent_greedy_normalizer(
    orbits: tuple[tuple[tuple[int, int], ...], ...],
    root_cycles: int,
    first_auxiliary: int,
) -> tuple[tuple[tuple[int, ...], ...], int, dict[str, int]]:
    edge_variable = {
        edge: variable
        for variable, orbit in enumerate(orbits, start=1)
        for edge in orbit
    }
    output: list[tuple[int, ...]] = []
    reference_internal = edge_variable[(0, 1)]
    for cycle in range(1, root_cycles):
        output.append(
            (
                reference_internal,
                -edge_variable[(3 * cycle, 3 * cycle + 1)],
            )
        )
    next_variable = first_auxiliary
    comparator_count = 0
    self_count = 0
    competitor_count = 0
    compared_bits = 0
    groups = (
        tuple(range(1, root_cycles)),
        tuple(range(root_cycles, 14)),
    )
    for group in groups:
        for index, current in enumerate(group):
            prefix = range(current)
            left = independent_oriented_profile(
                edge_variable, current, prefix, 0
            )
            comparisons: list[tuple[int, ...]] = [
                independent_oriented_profile(
                    edge_variable, current, prefix, shift
                )
                for shift in (1, 2)
            ]
            self_count += 2
            for later in group[index + 1 :]:
                comparisons.extend(
                    independent_oriented_profile(
                        edge_variable, later, prefix, shift
                    )
                    for shift in range(3)
                )
                competitor_count += 3
            for right in comparisons:
                clauses, next_variable = independent_lex_ge(
                    left, right, next_variable
                )
                output.extend(clauses)
                comparator_count += 1
                compared_bits += len(left)
    metadata = {
        "reference_internal_max_clauses": root_cycles - 1,
        "profile_comparator_count": comparator_count,
        "self_phase_comparator_count": self_count,
        "competing_block_phase_comparator_count": competitor_count,
        "lexicographically_compared_bits": compared_bits,
        "greedy_normalizer_clause_count": len(output),
        "greedy_normalizer_auxiliary_variable_count": (
            next_variable - first_auxiliary
        ),
    }
    return tuple(output), next_variable, metadata


def greedy_cover_audit() -> dict[str, object]:
    patterns = tuple(itertools.product((False, True), repeat=3))
    rotation_maxima = {
        pattern: max(
            tuple(
                pattern[(offset + shift) % 3]
                for offset in range(3)
            )
            for shift in range(3)
        )
        for pattern in patterns
    }
    valid = all(
        maximum >= pattern
        for pattern, maximum in rotation_maxima.items()
    )
    return {
        "valid": valid,
        "phase_patterns_checked": len(patterns),
        "phase_maxima": [
            {"pattern": list(pattern), "maximum": list(maximum)}
            for pattern, maximum in rotation_maxima.items()
        ],
        "inductive_block_argument": (
            "A finite set of remaining oriented block profiles always has a "
            "lexicographic maximum; move one maximizer to the current "
            "position and continue without changing the fixed prefix."
        ),
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
    greedy, final_next_variable, greedy_metadata = (
        independent_greedy_normalizer(
            orbits, root_cycles, next_variable
        )
    )
    expected = (*reduced, *units, *greedy, *degree)
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
    cover = greedy_cover_audit()
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
        and all(metadata.get(key) == value for key, value in greedy_metadata.items())
        and metadata.get("degree_clause_count") == len(degree)
        and metadata.get("final_state_variables") == final_states
        and metadata.get("total_auxiliary_variable_count")
        == expected_variables - primary
        and metadata.get("clause_count") == len(expected)
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
            f"Exact greedy-normalized root case m={root_cycles} for "
            "cycle type 3^14 1."
        ),
        "root_neighbor_cycle_count": root_cycles,
        "primary_variable_count": primary,
        "variable_count": expected_variables,
        "full_ramsey_clause_count": full_count,
        "reduced_ramsey_clause_count": reduced_count,
        "root_unit_clause_count": len(units),
        **greedy_metadata,
        "degree_clause_count": len(degree),
        "expected_clause_count": len(expected),
        "actual_clause_count": len(actual),
        "greedy_cover_audit": cover,
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
