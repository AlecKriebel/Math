#!/usr/bin/env python3
"""Add exact fixed-vertex degree-lemma clauses to a prime-orbit Ramsey CNF."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path

from automorphism_orbit_cnf import (
    CLIQUE_SIZE,
    GENERATOR_ID as ORBIT_GENERATOR_ID,
    ORDER,
    canonical_permutation,
    edge_orbit_table,
    ramsey_signatures,
)


GENERATOR_ID = "ramsey55_prime_automorphism_fixed_degree_cnf_generator_v1"
DEGREE_LOWER = 18
DEGREE_UPPER = 24


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def ramsey_clauses(
    signatures: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    clauses: list[tuple[int, ...]] = []
    for signature in signatures:
        clauses.append(signature)
        clauses.append(tuple(-variable for variable in signature))
    return tuple(clauses)


def fixed_vertex_degree_records(
    orbits: tuple[tuple[tuple[int, int], ...], ...],
    first_fixed_vertex: int,
) -> tuple[dict[str, object], ...]:
    records: list[dict[str, object]] = []
    for vertex in range(first_fixed_vertex, ORDER):
        weighted_variables: list[tuple[int, int]] = []
        for variable, orbit in enumerate(orbits, start=1):
            weight = sum(vertex in edge for edge in orbit)
            if weight:
                weighted_variables.append((variable, weight))
        if sum(weight for _, weight in weighted_variables) != ORDER - 1:
            raise AssertionError("incident orbit weights do not sum to 42")
        invalid_count = 0
        allowed_histogram: Counter[int] = Counter()
        for values in itertools.product(
            (False, True), repeat=len(weighted_variables)
        ):
            degree = sum(
                weight for (_, weight), value in zip(weighted_variables, values)
                if value
            )
            if DEGREE_LOWER <= degree <= DEGREE_UPPER:
                allowed_histogram[degree] += 1
            else:
                invalid_count += 1
        records.append(
            {
                "vertex": vertex,
                "weighted_variables": [
                    {"variable": variable, "weight": weight}
                    for variable, weight in weighted_variables
                ],
                "assignment_count": 1 << len(weighted_variables),
                "allowed_assignment_count": sum(allowed_histogram.values()),
                "invalid_assignment_count": invalid_count,
                "allowed_degree_histogram": {
                    str(degree): allowed_histogram[degree]
                    for degree in sorted(allowed_histogram)
                },
            }
        )
    return tuple(records)


def degree_clauses(
    records: tuple[dict[str, object], ...],
) -> tuple[tuple[int, ...], ...]:
    clauses: list[tuple[int, ...]] = []
    for record in records:
        raw_variables = record["weighted_variables"]
        if not isinstance(raw_variables, list):
            raise AssertionError("malformed internal degree record")
        weighted_variables = [
            (int(item["variable"]), int(item["weight"]))
            for item in raw_variables
            if isinstance(item, dict)
        ]
        if len(weighted_variables) != len(raw_variables):
            raise AssertionError("malformed weighted variable")
        vertex_clause_count = 0
        for values in itertools.product(
            (False, True), repeat=len(weighted_variables)
        ):
            degree = sum(
                weight for (_, weight), value in zip(weighted_variables, values)
                if value
            )
            if DEGREE_LOWER <= degree <= DEGREE_UPPER:
                continue
            clauses.append(
                tuple(
                    -variable if value else variable
                    for (variable, _), value in zip(weighted_variables, values)
                )
            )
            vertex_clause_count += 1
        if vertex_clause_count != record["invalid_assignment_count"]:
            raise AssertionError("degree clause count mismatch")
    return tuple(clauses)


def write_cnf(
    path: Path,
    variable_count: int,
    clauses: tuple[tuple[int, ...], ...],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {variable_count} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, required=True)
    parser.add_argument("--cycles", type=int, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    if args.cnf.exists() or args.metadata.exists():
        raise SystemExit("refusing to overwrite output")

    permutation = canonical_permutation(args.prime, args.cycles)
    edge_variable, orbits = edge_orbit_table(permutation)
    signatures = ramsey_signatures(edge_variable)
    base_clauses = ramsey_clauses(signatures)
    first_fixed_vertex = args.prime * args.cycles
    degree_records = fixed_vertex_degree_records(orbits, first_fixed_vertex)
    added_clauses = degree_clauses(degree_records)
    clauses = base_clauses + added_clauses
    write_cnf(args.cnf, len(orbits), clauses)

    orbit_histogram = Counter(len(orbit) for orbit in orbits)
    signature_histogram = Counter(len(signature) for signature in signatures)
    source = Path(__file__).resolve()
    orbit_source = Path(__file__).with_name("automorphism_orbit_cnf.py")
    metadata = {
        "generator": GENERATOR_ID,
        "orbit_generator_dependency": ORBIT_GENERATOR_ID,
        "order": ORDER,
        "clique_size": CLIQUE_SIZE,
        "automorphism_order": args.prime,
        "cycle_count": args.cycles,
        "fixed_point_count": ORDER - first_fixed_vertex,
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
        "unique_orbit_signature_count": len(signatures),
        "signature_size_histogram": {
            str(size): signature_histogram[size]
            for size in sorted(signature_histogram)
        },
        "ramsey_clause_count": len(base_clauses),
        "degree_lemma": {
            "degree_lower": DEGREE_LOWER,
            "degree_upper": DEGREE_UPPER,
            "basis": (
                "R(4,5)=R(5,4)=25 implies 18<=degree(v)<=24 in every "
                "(5,5;43)-graph."
            ),
            "scope": "fixed vertices of the prescribed automorphism",
            "records": list(degree_records),
            "clause_count": len(added_clauses),
        },
        "clause_count": len(clauses),
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": sha256_file(args.cnf),
        "cnf_bytes": args.cnf.stat().st_size,
        "generator_path": str(source),
        "generator_sha256": sha256_file(source),
        "orbit_generator_path": str(orbit_source.resolve()),
        "orbit_generator_sha256": sha256_file(orbit_source),
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {key: value for key, value in metadata.items() if key != "edge_orbits"},
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
