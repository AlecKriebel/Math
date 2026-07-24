#!/usr/bin/env python3
"""Independent checker for degree-strengthened 3^14 1 case CNFs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
import time
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

from automorphism3_fourteen_cycle_symmetry_cnf_check import (  # noqa: E402
    expected_formula,
)
from automorphism_orbit_cnf_check import (  # noqa: E402
    independently_build,
    read_dimacs,
)


CHECKER_ID = "ramsey55_order3_fourteen_cycle_degree_cnf_checker_v1"


def digest(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def independent_degree_terms(
    orbits: tuple[tuple[tuple[int, int], ...], ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    variable_of: dict[tuple[int, int], int] = {}
    for index, orbit in enumerate(orbits, start=1):
        for edge in orbit:
            if edge in variable_of:
                raise AssertionError("overlapping edge orbits")
            variable_of[edge] = index
    result: list[tuple[tuple[int, int], ...]] = []
    for representative in range(0, 42, 3):
        multiplicity: dict[int, int] = {}
        for other in range(43):
            if other == representative:
                continue
            edge = tuple(sorted((representative, other)))
            variable = variable_of[edge]
            multiplicity[variable] = multiplicity.get(variable, 0) + 1
        terms = tuple(sorted(multiplicity.items()))
        if (
            len(terms) != 41
            or sum(multiplicity.values()) != 42
            or Counter(multiplicity.values()) != Counter({1: 40, 2: 1})
        ):
            raise AssertionError("bad independent degree expression")
        result.append(terms)
    return tuple(result)


def _negate(reference: int | bool) -> int | bool:
    return not reference if type(reference) is bool else -reference


def _emit(
    output: list[tuple[int, ...]], atoms: tuple[int | bool, ...]
) -> None:
    if any(atom is True for atom in atoms):
        return
    clause: list[int] = []
    for atom in atoms:
        if atom is False:
            continue
        literal = int(atom)
        if -literal in clause:
            return
        if literal not in clause:
            clause.append(literal)
    output.append(tuple(clause))


def independent_degree_encoding(
    orbits: tuple[tuple[tuple[int, int], ...], ...],
    first_auxiliary: int,
) -> tuple[tuple[tuple[int, ...], ...], int, list[list[int]]]:
    output: list[tuple[int, ...]] = []
    next_variable = first_auxiliary
    final_states: list[list[int]] = []
    for terms in independent_degree_terms(orbits):
        previous: dict[int, int | bool] = {
            threshold: False for threshold in range(1, 26)
        }
        for primary, weight in terms:
            current: dict[int, int] = {}
            for threshold in range(1, 26):
                state = next_variable
                next_variable += 1
                current[threshold] = state
                old = previous[threshold]
                augmented: int | bool = (
                    True if threshold <= weight else previous[threshold - weight]
                )
                _emit(output, (_negate(old), state))
                _emit(output, (-primary, _negate(augmented), state))
                _emit(output, (-state, old, primary))
                _emit(output, (-state, old, augmented))
            previous = current
        output.extend(((int(previous[18]),), (-int(previous[25]),)))
        final_states.append([int(previous[18]), int(previous[25])])
    return tuple(output), next_variable, final_states


def check(cnf: Path, metadata_path: Path) -> dict[str, object]:
    started = time.monotonic()
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    root_cycles = metadata.get("root_neighbor_cycle_count")
    if root_cycles not in (6, 7):
        raise ValueError("invalid root-neighbor case")
    mode = f"{root_cycles}-reduced"
    (
        primary_count,
        base_and_units,
        _,
        reduced_count,
        full_count,
    ) = expected_formula(mode)
    reduced = base_and_units[:reduced_count]
    units = base_and_units[reduced_count:]
    _, orbits, _ = independently_build(3, 14)
    degree_clauses, next_variable, final_states = independent_degree_encoding(
        orbits, primary_count + 1
    )
    expected = (*reduced, *units, *degree_clauses)
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
    expected_variables = next_variable - 1
    cnf_sha256 = digest(cnf)
    metadata_valid = (
        metadata.get("order") == 43
        and metadata.get("clique_size") == 5
        and metadata.get("automorphism_order") == 3
        and metadata.get("cycle_count") == 14
        and metadata.get("fixed_point_count") == 1
        and metadata.get("cycle_type") == "3^14 1"
        and metadata.get("base_mode") == mode
        and metadata.get("primary_variable_count") == primary_count
        and metadata.get("variable_count") == expected_variables
        and metadata.get("full_ramsey_clause_count") == full_count
        and metadata.get("reduced_ramsey_clause_count") == reduced_count
        and metadata.get("root_unit_clause_count") == len(units)
        and metadata.get("constrained_moved_vertex_orbits") == 14
        and metadata.get("terms_per_degree_expression") == 41
        and metadata.get("weight_histogram_per_expression")
        == {"1": 40, "2": 1}
        and metadata.get("weight_sum_per_expression") == 42
        and metadata.get("degree_interval") == [18, 24]
        and metadata.get("auxiliary_variable_count")
        == expected_variables - primary_count
        and metadata.get("degree_clause_count") == len(degree_clauses)
        and metadata.get("final_state_variables") == final_states
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
    )
    return {
        "checker": CHECKER_ID,
        "valid": valid,
        "claim_scope": (
            f"Exact normalized root case m={root_cycles} for cycle type "
            "3^14 1, including independently rebuilt weighted degree bounds."
        ),
        "root_neighbor_cycle_count": root_cycles,
        "primary_variable_count": primary_count,
        "variable_count": expected_variables,
        "full_ramsey_clause_count": full_count,
        "reduced_ramsey_clause_count": reduced_count,
        "root_unit_clause_count": len(units),
        "degree_clause_count": len(degree_clauses),
        "expected_clause_count": len(expected),
        "actual_clause_count": len(actual),
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
