#!/usr/bin/env python3
"""Independent exact checker for the symmetry-reduced 3^14 1 CNFs."""

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

from automorphism_orbit_cnf_check import independently_build, read_dimacs  # noqa: E402


CHECKER_ID = "ramsey55_order3_fourteen_cycle_symmetry_cnf_checker_v1"
FIXED_VERTEX = 42
CYCLE_COUNT = 14


def digest(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def independent_root_variables(
    orbits: tuple[tuple[tuple[int, int], ...], ...],
) -> tuple[int, ...]:
    variable_of = {
        edge: variable
        for variable, orbit in enumerate(orbits, start=1)
        for edge in orbit
    }
    return tuple(variable_of[(3 * cycle, FIXED_VERTEX)] for cycle in range(14))


def independent_symmetry_clauses(
    variables: tuple[int, ...], mode: str
) -> tuple[tuple[int, ...], ...]:
    if mode != "cover":
        if mode not in {"6", "7", "6-reduced", "7-reduced"}:
            raise ValueError(f"unsupported mode in metadata: {mode!r}")
        adjacent = int(mode.split("-", 1)[0])
        return tuple(
            (variable,) if index < adjacent else (-variable,)
            for index, variable in enumerate(variables)
        )
    return (
        *((left, -right) for left, right in zip(variables, variables[1:])),
        (variables[5],),
        (-variables[7],),
    )


def independent_simplification(
    clauses: tuple[tuple[int, ...], ...],
    variables: tuple[int, ...],
    adjacent: int,
) -> tuple[tuple[int, ...], ...]:
    assignment = {
        variable: index < adjacent
        for index, variable in enumerate(variables)
    }
    result: list[tuple[int, ...]] = []
    seen: set[tuple[int, ...]] = set()
    for clause in clauses:
        satisfied = False
        residual: list[int] = []
        for literal in clause:
            value = assignment.get(abs(literal))
            if value is None:
                residual.append(literal)
            elif value == (literal > 0):
                satisfied = True
                break
        if satisfied:
            continue
        item = tuple(residual)
        if item not in seen:
            seen.add(item)
            result.append(item)
    return tuple(result)


def symmetry_cover_audit() -> dict[str, object]:
    """Exhaustively audit the degree/complement/block normalization."""
    degree_allowed = [
        m for m in range(CYCLE_COUNT + 1) if 18 <= 3 * m <= 24
    ]
    normalized = sorted({min(m, CYCLE_COUNT - m) for m in degree_allowed})
    prefix_satisfying: list[int] = []
    for length in range(CYCLE_COUNT + 1):
        bits = tuple(index < length for index in range(CYCLE_COUNT))
        ordered = all(
            bits[index] or not bits[index + 1]
            for index in range(CYCLE_COUNT - 1)
        )
        range_units = bits[5] and not bits[7]
        if ordered and range_units:
            prefix_satisfying.append(length)

    # Exhaustively check all labeled root neighborhoods.  Each allowed subset
    # can be complemented if necessary and then sorted by a cycle permutation.
    labeled_allowed = 0
    normalized_lengths: set[int] = set()
    for bits in itertools.product((False, True), repeat=CYCLE_COUNT):
        m = sum(bits)
        if m not in degree_allowed:
            continue
        labeled_allowed += 1
        normalized_lengths.add(min(m, CYCLE_COUNT - m))
    valid = (
        degree_allowed == [6, 7, 8]
        and normalized == [6, 7]
        and prefix_satisfying == [6, 7]
        and normalized_lengths == {6, 7}
        and labeled_allowed
        == sum(
            __import__("math").comb(CYCLE_COUNT, m) for m in degree_allowed
        )
    )
    return {
        "valid": valid,
        "degree_allowed_m": degree_allowed,
        "complement_normalized_m": normalized,
        "cover_formula_prefix_lengths": prefix_satisfying,
        "labeled_allowed_root_neighborhoods_checked": labeled_allowed,
    }


def expected_formula(
    mode: str,
) -> tuple[
    int,
    tuple[tuple[int, ...], ...],
    tuple[int, ...],
    int,
    int,
]:
    _, orbits, full_base_clauses = independently_build(3, 14)
    root_variables = independent_root_variables(orbits)
    if mode.endswith("-reduced"):
        base_clauses = independent_simplification(
            full_base_clauses,
            root_variables,
            int(mode.split("-", 1)[0]),
        )
    else:
        base_clauses = full_base_clauses
    extra = independent_symmetry_clauses(root_variables, mode)
    return (
        len(orbits),
        (*base_clauses, *extra),
        root_variables,
        len(base_clauses),
        len(full_base_clauses),
    )


def check(cnf: Path, metadata_path: Path) -> dict[str, object]:
    started = time.monotonic()
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    mode = metadata.get("mode")
    if type(mode) is not str:
        raise ValueError("metadata mode is missing")
    (
        expected_variables,
        expected_clauses,
        root_variables,
        base_count,
        full_base_count,
    ) = expected_formula(mode)
    variables, declared, actual_clauses = read_dimacs(cnf)
    first_mismatch = None
    for index, pair in enumerate(
        itertools.zip_longest(expected_clauses, actual_clauses), start=1
    ):
        if pair[0] != pair[1]:
            first_mismatch = {
                "clause_index": index,
                "expected": list(pair[0]) if pair[0] is not None else None,
                "actual": list(pair[1]) if pair[1] is not None else None,
            }
            break
    cover = symmetry_cover_audit()
    cnf_sha256 = digest(cnf)
    extra_count = len(expected_clauses) - base_count
    metadata_valid = (
        metadata.get("order") == 43
        and metadata.get("clique_size") == 5
        and metadata.get("automorphism_order") == 3
        and metadata.get("cycle_count") == 14
        and metadata.get("fixed_point_count") == 1
        and metadata.get("fixed_vertex") == FIXED_VERTEX
        and metadata.get("cycle_type") == "3^14 1"
        and metadata.get("variable_count") == expected_variables
        and metadata.get("unique_orbit_signature_count")
        == full_base_count // 2
        and metadata.get("base_clause_count") == base_count
        and metadata.get("full_base_clause_count") == full_base_count
        and metadata.get("root_simplification", {}).get("applied")
        == mode.endswith("-reduced")
        and metadata.get("symmetry_breaking_clause_count") == extra_count
        and metadata.get("clause_count") == len(expected_clauses)
        and metadata.get("root_cycle_variables") == list(root_variables)
        and metadata.get("degree_reduction", {}).get("allowed_m_before_complement")
        == [6, 7, 8]
        and metadata.get("degree_reduction", {}).get("normalized_m") == [6, 7]
        and metadata.get("cnf_sha256") == cnf_sha256
        and metadata.get("cnf_bytes") == cnf.stat().st_size
    )
    valid = (
        variables == expected_variables
        and declared == len(expected_clauses)
        and len(actual_clauses) == len(expected_clauses)
        and first_mismatch is None
        and metadata_valid
        and cover["valid"]
    )
    return {
        "checker": CHECKER_ID,
        "valid": valid,
        "claim_scope": (
            "Exact CNF and complete root-neighborhood symmetry cover for "
            "cycle type 3^14 1 only."
        ),
        "mode": mode,
        "variable_count": expected_variables,
        "unique_orbit_signature_count": full_base_count // 2,
        "base_clause_count": base_count,
        "full_base_clause_count": full_base_count,
        "symmetry_breaking_clause_count": extra_count,
        "expected_clause_count": len(expected_clauses),
        "actual_clause_count": len(actual_clauses),
        "root_cycle_variables": list(root_variables),
        "symmetry_cover_audit": cover,
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
