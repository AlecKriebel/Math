#!/usr/bin/env python3
"""Independent checker for the symmetry-broken 13^2 1^17 CNF."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

from automorphism_orbit_cnf_check import (  # noqa: E402
    independently_build,
    read_dimacs,
)


CHECKER_ID = "ramsey55_order13_two_cycle_symmetry_cnf_checker_v1"
FIXED_VERTICES = tuple(range(26, 43))


def digest(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def independently_expected() -> tuple[int, tuple[tuple[int, ...], ...]]:
    _, orbits, base_clauses = independently_build(13, 2)
    edge_variable = {
        edge: variable
        for variable, orbit in enumerate(orbits, start=1)
        for edge in orbit
    }
    extra: list[tuple[int, ...]] = []
    first_variables: list[int] = []
    for fixed_vertex in FIXED_VERTICES:
        first = edge_variable[(0, fixed_vertex)]
        second = edge_variable[(13, fixed_vertex)]
        first_variables.append(first)
        extra.extend(((first, second), (-first, -second)))
    extra.extend(
        (left, -right)
        for left, right in zip(first_variables, first_variables[1:])
    )
    extra.append((-first_variables[8],))
    return len(orbits), (*base_clauses, *extra)


def check(cnf: Path, metadata_path: Path) -> dict[str, object]:
    started = time.monotonic()
    expected_variables, expected_clauses = independently_expected()
    variables, declared, actual_clauses = read_dimacs(cnf)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    cnf_sha256 = digest(cnf)
    first_mismatch = None
    limit = max(len(expected_clauses), len(actual_clauses))
    for index in range(limit):
        expected = (
            expected_clauses[index] if index < len(expected_clauses) else None
        )
        actual = actual_clauses[index] if index < len(actual_clauses) else None
        if expected != actual:
            first_mismatch = {
                "clause_index": index + 1,
                "expected": list(expected) if expected is not None else None,
                "actual": list(actual) if actual is not None else None,
            }
            break
    metadata_valid = (
        metadata.get("order") == 43
        and metadata.get("clique_size") == 5
        and metadata.get("automorphism_order") == 13
        and metadata.get("cycle_count") == 2
        and metadata.get("fixed_point_count") == 17
        and metadata.get("cycle_type") == "13^2 1^17"
        and metadata.get("variable_count") == expected_variables
        and metadata.get("base_clause_count") == 152_264
        and metadata.get("symmetry_breaking_clause_count") == 51
        and metadata.get("clause_count") == len(expected_clauses)
        and metadata.get("unique_orbit_signature_count") == 76_132
        and metadata.get("cnf_sha256") == cnf_sha256
        and metadata.get("cnf_bytes") == cnf.stat().st_size
        and metadata.get("symmetry_cover", {}).get("normalized_group_sizes")
        == list(range(9))
    )
    valid = (
        variables == expected_variables
        and declared == len(expected_clauses)
        and len(actual_clauses) == len(expected_clauses)
        and first_mismatch is None
        and metadata_valid
    )
    return {
        "checker": CHECKER_ID,
        "valid": valid,
        "claim_scope": (
            "Exact CNF and complete symmetry cover for cycle type "
            "13^2 1^17 only; 13^1 1^30 is outside scope."
        ),
        "variable_count": expected_variables,
        "base_clause_count": 152_264,
        "symmetry_breaking_clause_count": 51,
        "expected_clause_count": len(expected_clauses),
        "actual_clause_count": len(actual_clauses),
        "normalized_group_sizes": list(range(9)),
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
