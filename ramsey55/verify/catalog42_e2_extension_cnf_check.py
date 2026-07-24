#!/usr/bin/env python3
"""Independent structural checker for fixed-core E <= 2 extension CNFs."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from catalog42_optimal_extension_check import (
    COUNTER_ID,
    decode_short_graph6,
    extension_constraints,
    independent_counter,
)


CHECKER_ID = "ramsey55_catalog42_e2_extension_structural_checker_v1"
GENERATOR_ID = "ramsey55_catalog42_e2_extension_cnf_v1"


def contains_clique(adjacency: list[int], needed: int) -> bool:
    """Independent recursive-bitset clique existence check."""

    def search(candidates: int, remaining: int) -> bool:
        if remaining == 0:
            return True
        if candidates.bit_count() < remaining:
            return False
        while candidates:
            if candidates.bit_count() < remaining:
                return False
            bit = candidates & -candidates
            vertex = bit.bit_length() - 1
            candidates ^= bit
            if search(candidates & adjacency[vertex], remaining - 1):
                return True
        return False

    return search((1 << len(adjacency)) - 1, needed)


def complement(adjacency: list[int]) -> list[int]:
    mask = (1 << len(adjacency)) - 1
    return [
        mask & ~(neighbors | (1 << vertex))
        for vertex, neighbors in enumerate(adjacency)
    ]


def expected_formula(
    core: list[int],
) -> tuple[int, list[tuple[int, ...]], dict[str, int]]:
    constraints = extension_constraints(core)
    next_variable = 43
    relaxations: list[int] = []
    definitions: list[tuple[int, ...]] = []
    for _, _, clause in constraints:
        relaxation = next_variable
        next_variable += 1
        relaxations.append(relaxation)
        definitions.append(clause + (relaxation,))
        definitions.extend((-relaxation, -literal) for literal in clause)
    counter, next_variable = independent_counter(relaxations, 2, next_variable)
    clauses = definitions + counter
    counts = {
        "primary_variable_count": 42,
        "constraint_count": len(constraints),
        "clique_constraint_count": sum(
            kind == "clique" for kind, _, _ in constraints
        ),
        "independent_constraint_count": sum(
            kind == "independent" for kind, _, _ in constraints
        ),
        "relaxation_variable_count": len(relaxations),
        "definition_clause_count": len(definitions),
        "counter_auxiliary_variable_count": next_variable
        - 1
        - 42
        - len(relaxations),
        "counter_clause_count": len(counter),
        "variable_count": next_variable - 1,
        "clause_count": len(clauses),
    }
    return next_variable - 1, clauses, counts


def check(
    catalog: Path,
    catalog_line: int,
    cnf: Path,
    metadata_path: Path,
) -> dict[str, object]:
    started = time.monotonic()
    catalog_bytes = catalog.read_bytes()
    lines = [
        line.strip()
        for line in catalog_bytes.decode("ascii").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if not 1 <= catalog_line <= len(lines):
        raise ValueError("catalog line out of range")
    core = decode_short_graph6(lines[catalog_line - 1])
    if len(core) != 42:
        raise ValueError("core order is not 42")
    variable_count, wanted_clauses, counts = expected_formula(core)
    wanted = iter(wanted_clauses)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    digest = hashlib.sha256()
    declared_variables: int | None = None
    declared_clauses: int | None = None
    observed_count = 0
    current: list[int] = []
    first_mismatch: dict[str, object] | None = None
    generator_seen = False
    with cnf.open("rb") as stream:
        for line_number, raw in enumerate(stream, start=1):
            digest.update(raw)
            fields = raw.decode("ascii").split()
            if not fields:
                continue
            if fields[0] == "c":
                generator_seen = generator_seen or fields[1:] == [
                    "generator",
                    GENERATOR_ID,
                ]
                continue
            if fields[0] == "p":
                if (
                    declared_variables is not None
                    or len(fields) != 4
                    or fields[1] != "cnf"
                ):
                    raise ValueError("invalid DIMACS header")
                declared_variables = int(fields[2])
                declared_clauses = int(fields[3])
                continue
            if declared_variables is None:
                raise ValueError("clause precedes DIMACS header")
            for field in fields:
                literal = int(field)
                if literal:
                    if abs(literal) > declared_variables:
                        raise ValueError("literal outside declared range")
                    current.append(literal)
                else:
                    observed_count += 1
                    expected = next(wanted, None)
                    observed = tuple(current)
                    if first_mismatch is None and observed != expected:
                        first_mismatch = {
                            "clause_index": observed_count,
                            "line_number": line_number,
                            "expected": (
                                list(expected) if expected is not None else None
                            ),
                            "actual": list(observed),
                        }
                    current = []
    missing_count = sum(1 for _ in wanted)
    cnf_sha256 = digest.hexdigest()
    catalog_sha256 = hashlib.sha256(catalog_bytes).hexdigest()
    metadata_matches = (
        metadata.get("generator") == GENERATOR_ID
        and metadata.get("catalog_sha256") == catalog_sha256
        and metadata.get("catalog_line") == catalog_line
        and metadata.get("core_graph6") == lines[catalog_line - 1]
        and metadata.get("counter_encoding") == COUNTER_ID
        and metadata.get("conflict_bound") == 2
        and metadata.get("cnf_sha256") == cnf_sha256
        and metadata.get("cnf_bytes") == cnf.stat().st_size
        and all(metadata.get(key) == value for key, value in counts.items())
    )
    core_has_clique = contains_clique(core, 5)
    core_has_independent = contains_clique(complement(core), 5)
    valid = (
        not core_has_clique
        and not core_has_independent
        and generator_seen
        and declared_variables == variable_count
        and declared_clauses == len(wanted_clauses)
        and observed_count == len(wanted_clauses)
        and not current
        and missing_count == 0
        and first_mismatch is None
        and metadata_matches
    )
    return {
        "checker": CHECKER_ID,
        "valid": valid,
        "catalog_line": catalog_line,
        "catalog_sha256": catalog_sha256,
        "core_clique5_found": core_has_clique,
        "core_independent5_found": core_has_independent,
        "cnf_sha256": cnf_sha256,
        "cnf_bytes": cnf.stat().st_size,
        "declared_variable_count": declared_variables,
        "declared_clause_count": declared_clauses,
        "observed_clause_count": observed_count,
        "missing_expected_clause_count": missing_count,
        "first_mismatch": first_mismatch,
        "metadata_matches": metadata_matches,
        **counts,
        "runtime_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--line", type=int, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = check(args.catalog, args.line, args.cnf, args.metadata)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
