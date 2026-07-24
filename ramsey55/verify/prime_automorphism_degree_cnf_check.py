#!/usr/bin/env python3
"""Independently reconstruct a prime-orbit CNF plus fixed-degree clauses."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from collections import Counter
from pathlib import Path

import automorphism_orbit_cnf_check as orbit_check


CHECKER_ID = "ramsey55_prime_automorphism_fixed_degree_cnf_checker_v1"
ORDER = 43
DEGREE_LOWER = 18
DEGREE_UPPER = 24


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def degree_data(
    orbits: tuple[tuple[tuple[int, int], ...], ...],
    first_fixed_vertex: int,
) -> tuple[tuple[tuple[int, ...], ...], list[dict[str, object]]]:
    clauses: list[tuple[int, ...]] = []
    records: list[dict[str, object]] = []
    for vertex in range(first_fixed_vertex, ORDER):
        incidence: list[tuple[int, int]] = []
        for variable, orbit in enumerate(orbits, start=1):
            multiplicity = 0
            for left, right in orbit:
                multiplicity += left == vertex or right == vertex
            if multiplicity:
                incidence.append((variable, multiplicity))
        if sum(weight for _, weight in incidence) != ORDER - 1:
            raise AssertionError("incident multiplicities do not sum to 42")
        allowed: Counter[int] = Counter()
        invalid = 0
        for assignment in itertools.product((0, 1), repeat=len(incidence)):
            degree = sum(
                weight * value
                for (_, weight), value in zip(incidence, assignment)
            )
            if DEGREE_LOWER <= degree <= DEGREE_UPPER:
                allowed[degree] += 1
            else:
                invalid += 1
                clauses.append(
                    tuple(
                        -variable if value else variable
                        for (variable, _), value in zip(incidence, assignment)
                    )
                )
        records.append(
            {
                "vertex": vertex,
                "weighted_variables": [
                    {"variable": variable, "weight": weight}
                    for variable, weight in incidence
                ],
                "assignment_count": 1 << len(incidence),
                "allowed_assignment_count": sum(allowed.values()),
                "invalid_assignment_count": invalid,
                "allowed_degree_histogram": {
                    str(degree): allowed[degree] for degree in sorted(allowed)
                },
            }
        )
    return tuple(clauses), records


def check(cnf: Path, metadata_path: Path) -> dict[str, object]:
    started = time.monotonic()
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict):
        raise ValueError("metadata is not an object")
    prime = metadata.get("automorphism_order")
    cycles = metadata.get("cycle_count")
    if type(prime) is not int or type(cycles) is not int:
        raise ValueError("cycle type missing")

    permutation, orbits, ramsey_clauses = orbit_check.independently_build(
        prime, cycles
    )
    first_fixed_vertex = prime * cycles
    added_clauses, degree_records = degree_data(orbits, first_fixed_vertex)
    expected = ramsey_clauses + added_clauses
    variables, declared, actual = orbit_check.read_dimacs(cnf)

    orbit_histogram = Counter(len(orbit) for orbit in orbits)
    signatures = ramsey_clauses[0::2]
    signature_histogram = Counter(len(signature) for signature in signatures)
    serialized_orbits = [
        {
            "variable": variable,
            "edges": [list(edge) for edge in orbit],
        }
        for variable, orbit in enumerate(orbits, start=1)
    ]
    degree_metadata = metadata.get("degree_lemma")
    metadata_valid = (
        metadata.get("order") == ORDER
        and metadata.get("clique_size") == 5
        and metadata.get("fixed_point_count") == ORDER - first_fixed_vertex
        and metadata.get("permutation") == list(permutation)
        and metadata.get("variable_count") == len(orbits)
        and metadata.get("edge_orbit_count") == len(orbits)
        and metadata.get("edge_orbits") == serialized_orbits
        and metadata.get("edge_orbit_size_histogram")
        == {str(size): orbit_histogram[size] for size in sorted(orbit_histogram)}
        and metadata.get("five_set_count") == math.comb(ORDER, 5)
        and metadata.get("unique_orbit_signature_count") == len(signatures)
        and metadata.get("signature_size_histogram")
        == {
            str(size): signature_histogram[size]
            for size in sorted(signature_histogram)
        }
        and metadata.get("ramsey_clause_count") == len(ramsey_clauses)
        and isinstance(degree_metadata, dict)
        and degree_metadata.get("degree_lower") == DEGREE_LOWER
        and degree_metadata.get("degree_upper") == DEGREE_UPPER
        and degree_metadata.get("scope")
        == "fixed vertices of the prescribed automorphism"
        and degree_metadata.get("records") == degree_records
        and degree_metadata.get("clause_count") == len(added_clauses)
        and metadata.get("clause_count") == len(expected)
        and metadata.get("cnf_sha256") == sha256_file(cnf)
        and metadata.get("cnf_bytes") == cnf.stat().st_size
    )
    first_mismatch: dict[str, object] | None = None
    for index, (wanted, observed) in enumerate(
        itertools.zip_longest(expected, actual), start=1
    ):
        if wanted != observed:
            first_mismatch = {
                "clause_index": index,
                "expected": list(wanted) if wanted is not None else None,
                "actual": list(observed) if observed is not None else None,
            }
            break
    valid = (
        variables == len(orbits)
        and declared == len(expected)
        and len(actual) == len(expected)
        and first_mismatch is None
        and metadata_valid
    )
    return {
        "checker": CHECKER_ID,
        "valid": valid,
        "automorphism_order": prime,
        "cycle_count": cycles,
        "fixed_point_count": ORDER - first_fixed_vertex,
        "variable_count": len(orbits),
        "ramsey_clause_count": len(ramsey_clauses),
        "degree_clause_count": len(added_clauses),
        "expected_clause_count": len(expected),
        "actual_clause_count": len(actual),
        "fixed_vertex_degree_records": degree_records,
        "metadata_valid": metadata_valid,
        "first_mismatch": first_mismatch,
        "cnf_sha256": sha256_file(cnf),
        "cnf_bytes": cnf.stat().st_size,
        "runtime_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    if args.result.exists():
        raise SystemExit("refusing to overwrite result")
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
