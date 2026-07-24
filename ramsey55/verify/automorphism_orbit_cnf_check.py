#!/usr/bin/env python3
"""Independent structural checker for prime-automorphism Ramsey CNFs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from collections import Counter
from pathlib import Path


CHECKER_ID = "ramsey55_prime_automorphism_independent_cnf_checker_v1"
N = 43
K = 5


def digest(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as handle:
        for data in iter(lambda: handle.read(1_048_576), b""):
            state.update(data)
    return state.hexdigest()


def independently_build(
    prime: int, cycles: int
) -> tuple[
    tuple[int, ...],
    tuple[tuple[tuple[int, int], ...], ...],
    tuple[tuple[int, ...], ...],
]:
    if prime < 2 or any(prime % divisor == 0 for divisor in range(2, math.isqrt(prime) + 1)):
        raise ValueError("nonprime automorphism order")
    if cycles < 1 or prime * cycles > N:
        raise ValueError("invalid cycle count")
    image = list(range(N))
    for block in range(cycles):
        base = block * prime
        image[base : base + prime] = [
            base + (position + 1) % prime for position in range(prime)
        ]

    edge_to_representative: dict[tuple[int, int], tuple[int, int]] = {}
    orbit_sets: dict[tuple[int, int], set[tuple[int, int]]] = {}
    for initial in itertools.combinations(range(N), 2):
        generated: set[tuple[int, int]] = set()
        current = initial
        for _ in range(prime):
            generated.add(current)
            transformed = image[current[0]], image[current[1]]
            current = tuple(sorted(transformed))
        representative = min(generated)
        orbit_sets.setdefault(representative, set()).update(generated)
        edge_to_representative[initial] = representative
    representatives = sorted(orbit_sets)
    variable_of = {
        representative: index
        for index, representative in enumerate(representatives, start=1)
    }
    edge_variable = {
        edge: variable_of[representative]
        for edge, representative in edge_to_representative.items()
    }
    orbits = tuple(tuple(sorted(orbit_sets[representative])) for representative in representatives)

    patterns: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(N), K):
        patterns.add(
            tuple(
                sorted(
                    {
                        edge_variable[edge]
                        for edge in itertools.combinations(vertices, 2)
                    }
                )
            )
        )
    clauses: list[tuple[int, ...]] = []
    for pattern in sorted(patterns):
        clauses.append(pattern)
        clauses.append(tuple(-variable for variable in pattern))
    return tuple(image), orbits, tuple(clauses)


def read_dimacs(path: Path) -> tuple[int, int, tuple[tuple[int, ...], ...]]:
    variables: int | None = None
    declared: int | None = None
    clauses: list[tuple[int, ...]] = []
    pending: list[int] = []
    with path.open("r", encoding="ascii") as handle:
        for number, line in enumerate(handle, start=1):
            fields = line.split()
            if not fields or fields[0] == "c":
                continue
            if fields[0] == "p":
                if variables is not None or fields[:2] != ["p", "cnf"] or len(fields) != 4:
                    raise ValueError(f"invalid header at line {number}")
                variables, declared = int(fields[2]), int(fields[3])
                continue
            if variables is None:
                raise ValueError("clause before header")
            for raw in fields:
                literal = int(raw)
                if literal:
                    if abs(literal) > variables:
                        raise ValueError("literal out of bounds")
                    pending.append(literal)
                else:
                    if not pending:
                        raise ValueError("unexpected empty clause")
                    clauses.append(tuple(pending))
                    pending = []
    if variables is None or declared is None or pending:
        raise ValueError("incomplete DIMACS")
    return variables, declared, tuple(clauses)


def check(cnf: Path, metadata_path: Path) -> dict[str, object]:
    started = time.monotonic()
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    prime = metadata.get("automorphism_order")
    cycles = metadata.get("cycle_count")
    if type(prime) is not int or type(cycles) is not int:
        raise ValueError("metadata cycle type missing")
    permutation, orbits, expected = independently_build(prime, cycles)
    variables, declared, actual = read_dimacs(cnf)
    patterns = expected[0::2]
    signature_histogram = Counter(len(pattern) for pattern in patterns)
    orbit_histogram = Counter(len(orbit) for orbit in orbits)
    serialized_orbits = [
        {
            "variable": variable,
            "edges": [list(edge) for edge in orbit],
        }
        for variable, orbit in enumerate(orbits, start=1)
    ]
    cnf_sha256 = digest(cnf)
    metadata_valid = (
        metadata.get("order") == N
        and metadata.get("clique_size") == K
        and metadata.get("fixed_point_count") == N - prime * cycles
        and metadata.get("permutation") == list(permutation)
        and metadata.get("variable_count") == len(orbits)
        and metadata.get("edge_orbit_count") == len(orbits)
        and metadata.get("edge_orbits") == serialized_orbits
        and metadata.get("edge_orbit_size_histogram")
        == {str(size): orbit_histogram[size] for size in sorted(orbit_histogram)}
        and metadata.get("five_set_count") == math.comb(N, K)
        and metadata.get("unreduced_ramsey_clause_count") == 2 * math.comb(N, K)
        and metadata.get("unique_orbit_signature_count") == len(patterns)
        and metadata.get("clause_count") == len(expected)
        and metadata.get("signature_size_histogram")
        == {
            str(size): signature_histogram[size]
            for size in sorted(signature_histogram)
        }
        and metadata.get("cnf_sha256") == cnf_sha256
        and metadata.get("cnf_bytes") == cnf.stat().st_size
    )
    first_mismatch: dict[str, object] | None = None
    for index, pair in enumerate(itertools.zip_longest(expected, actual), start=1):
        if pair[0] != pair[1]:
            first_mismatch = {
                "clause_index": index,
                "expected": list(pair[0]) if pair[0] is not None else None,
                "actual": list(pair[1]) if pair[1] is not None else None,
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
        "fixed_point_count": N - prime * cycles,
        "variable_count": len(orbits),
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
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
