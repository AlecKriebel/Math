#!/usr/bin/env python3
"""Generate an exact Ramsey CNF under a prescribed prime-order automorphism."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path


GENERATOR_ID = "ramsey55_prime_automorphism_orbit_cnf_generator_v1"
ORDER = 43
CLIQUE_SIZE = 5


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def canonical_permutation(prime: int, cycle_count: int) -> tuple[int, ...]:
    if not is_prime(prime):
        raise ValueError("automorphism order must be prime")
    if cycle_count < 1 or prime * cycle_count > ORDER:
        raise ValueError("invalid number of prime cycles")
    moved = prime * cycle_count
    permutation = list(range(ORDER))
    for cycle in range(cycle_count):
        first = cycle * prime
        for offset in range(prime):
            permutation[first + offset] = first + (offset + 1) % prime
    if any(permutation[index] != index for index in range(moved, ORDER)):
        raise AssertionError("fixed-point construction failed")
    return tuple(permutation)


def edge_orbit_table(
    permutation: tuple[int, ...],
) -> tuple[dict[tuple[int, int], int], tuple[tuple[tuple[int, int], ...], ...]]:
    unseen = set(itertools.combinations(range(ORDER), 2))
    orbits: list[tuple[tuple[int, int], ...]] = []
    while unseen:
        seed = min(unseen)
        orbit: set[tuple[int, int]] = set()
        edge = seed
        while edge not in orbit:
            orbit.add(edge)
            left, right = permutation[edge[0]], permutation[edge[1]]
            edge = (left, right) if left < right else (right, left)
        canonical = tuple(sorted(orbit))
        unseen.difference_update(canonical)
        orbits.append(canonical)
    orbits.sort(key=lambda orbit: orbit[0])
    table: dict[tuple[int, int], int] = {}
    for variable, orbit in enumerate(orbits, start=1):
        for edge in orbit:
            if edge in table:
                raise AssertionError("edge occurs in two orbits")
            table[edge] = variable
    if len(table) != math.comb(ORDER, 2):
        raise AssertionError("edge-orbit table is incomplete")
    return table, tuple(orbits)


def ramsey_signatures(
    edge_variables: dict[tuple[int, int], int],
) -> tuple[tuple[int, ...], ...]:
    signatures: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(ORDER), CLIQUE_SIZE):
        signatures.add(
            tuple(
                sorted(
                    {
                        edge_variables[(left, right)]
                        for left, right in itertools.combinations(vertices, 2)
                    }
                )
            )
        )
    return tuple(sorted(signatures))


def write_cnf(
    path: Path,
    variable_count: int,
    signatures: tuple[tuple[int, ...], ...],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {variable_count} {2 * len(signatures)}\n")
        for signature in signatures:
            stream.write(" ".join(map(str, signature)) + " 0\n")
            stream.write(" ".join(str(-variable) for variable in signature) + " 0\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, required=True)
    parser.add_argument("--cycles", type=int, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()

    permutation = canonical_permutation(args.prime, args.cycles)
    edge_variables, orbits = edge_orbit_table(permutation)
    signatures = ramsey_signatures(edge_variables)
    write_cnf(args.cnf, len(orbits), signatures)
    signature_histogram = Counter(len(signature) for signature in signatures)
    orbit_histogram = Counter(len(orbit) for orbit in orbits)
    source = Path(__file__).resolve()
    metadata = {
        "generator": GENERATOR_ID,
        "order": ORDER,
        "clique_size": CLIQUE_SIZE,
        "automorphism_order": args.prime,
        "cycle_count": args.cycles,
        "fixed_point_count": ORDER - args.prime * args.cycles,
        "permutation": list(permutation),
        "variable_count": len(orbits),
        "edge_orbit_count": len(orbits),
        "edge_orbit_size_histogram": {
            str(size): orbit_histogram[size] for size in sorted(orbit_histogram)
        },
        "edge_orbits": [
            {
                "variable": variable,
                "edges": [list(edge) for edge in orbit],
            }
            for variable, orbit in enumerate(orbits, start=1)
        ],
        "five_set_count": math.comb(ORDER, CLIQUE_SIZE),
        "unreduced_ramsey_clause_count": 2 * math.comb(ORDER, CLIQUE_SIZE),
        "unique_orbit_signature_count": len(signatures),
        "clause_count": 2 * len(signatures),
        "signature_size_histogram": {
            str(size): signature_histogram[size]
            for size in sorted(signature_histogram)
        },
        "reduction_justification": (
            "Edges in one orbit have equal color under the prescribed "
            "automorphism. A five-set is homogeneous exactly when all distinct "
            "edge-orbit variables among its pairs have one truth value. Identical "
            "orbit signatures therefore induce duplicate clauses."
        ),
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": sha256_file(args.cnf),
        "cnf_bytes": args.cnf.stat().st_size,
        "generator_path": str(source),
        "generator_sha256": sha256_file(source),
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: value for key, value in metadata.items() if key != "edge_orbits"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
