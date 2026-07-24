#!/usr/bin/env python3
"""Independent checker for fixed-core at-most-two extension enumeration CNFs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path
from typing import Iterator, Sequence


CHECKER_ID = "ramsey55_catalog42_optimal_extension_structural_checker_v1"
GENERATOR_ID = "ramsey55_catalog42_optimal_extension_enumeration_cnf_v1"
COUNTER_ID = "forward_sequential_threshold_at_most_v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def decode_short_graph6(text: str) -> list[int]:
    line = text.strip()
    order = ord(line[0]) - 63
    if not 0 <= order <= 62:
        raise ValueError("only short graph6 is supported")
    needed = order * (order - 1) // 2
    if 6 * (len(line) - 1) < needed:
        raise ValueError("truncated graph6")
    adjacency = [0] * order
    bit = 0
    for right in range(1, order):
        for left in range(right):
            value = ord(line[1 + bit // 6]) - 63
            if not 0 <= value < 64:
                raise ValueError("invalid graph6 byte")
            if (value >> (5 - bit % 6)) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            bit += 1
    return adjacency


def independent_counter(
    literals: Sequence[int], bound: int, first_auxiliary: int
) -> tuple[list[tuple[int, ...]], int]:
    count = len(literals)
    if bound < 0:
        return [()], first_auxiliary
    if bound >= count:
        return [], first_auxiliary
    if bound == 0:
        return [(-literal,) for literal in literals], first_auxiliary
    width = bound + 1
    rows: list[list[int]] = []
    next_variable = first_auxiliary
    for prefix in range(1, count + 1):
        length = min(prefix, width)
        rows.append(list(range(next_variable, next_variable + length)))
        next_variable += length
    clauses: list[tuple[int, ...]] = []
    for index, literal in enumerate(literals):
        current = rows[index]
        clauses.append((-literal, current[0]))
        if index == 0:
            continue
        previous = rows[index - 1]
        clauses.extend(
            (-previous[threshold], current[threshold])
            for threshold in range(len(previous))
        )
        clauses.extend(
            (-literal, -previous[threshold - 1], current[threshold])
            for threshold in range(1, len(current))
        )
    clauses.append((-rows[-1][-1],))
    return clauses, next_variable


def extension_constraints(
    adjacency: list[int],
) -> list[tuple[str, tuple[int, ...], tuple[int, ...]]]:
    result: list[tuple[str, tuple[int, ...], tuple[int, ...]]] = []
    for vertices in itertools.combinations(range(len(adjacency)), 4):
        edge_count = 0
        for left, right in itertools.combinations(vertices, 2):
            edge_count += (adjacency[left] >> right) & 1
        if edge_count == 6:
            result.append(
                (
                    "clique",
                    vertices,
                    tuple(-(vertex + 1) for vertex in vertices),
                )
            )
        elif edge_count == 0:
            result.append(
                (
                    "independent",
                    vertices,
                    tuple(vertex + 1 for vertex in vertices),
                )
            )
    return result


def conflicts(adjacency: list[int]) -> list[tuple[str, tuple[int, ...]]]:
    result: list[tuple[str, tuple[int, ...]]] = []
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        edge_count = 0
        for left, right in itertools.combinations(vertices, 2):
            edge_count += (adjacency[left] >> right) & 1
        if edge_count == 10:
            result.append(("clique", vertices))
        elif edge_count == 0:
            result.append(("independent", vertices))
    return result


def extend(core: list[int], bits: str) -> list[int]:
    if len(bits) != len(core) or set(bits) - {"0", "1"}:
        raise ValueError("invalid model bits")
    result = list(core) + [0]
    added = len(core)
    for vertex, bit in enumerate(bits):
        if bit == "1":
            result[vertex] |= 1 << added
            result[added] |= 1 << vertex
    return result


def expected_formula(
    core: list[int], model_bits: list[str]
) -> tuple[int, list[tuple[int, ...]], dict[str, int]]:
    constraints = extension_constraints(core)
    next_variable = 43
    relaxation_variables: list[int] = []
    definition: list[tuple[int, ...]] = []
    for _, _, clause in constraints:
        relaxation = next_variable
        next_variable += 1
        relaxation_variables.append(relaxation)
        definition.append(clause + (relaxation,))
        for literal in clause:
            definition.append((-relaxation, -literal))
    counter, next_variable = independent_counter(
        relaxation_variables, 2, next_variable
    )
    blocks = [
        tuple(
            -(vertex + 1) if bits[vertex] == "1" else vertex + 1
            for vertex in range(42)
        )
        for bits in model_bits
    ]
    clauses = definition + counter + blocks
    counts = {
        "primary_variable_count": 42,
        "constraint_count": len(constraints),
        "clique_constraint_count": sum(
            kind == "clique" for kind, _, _ in constraints
        ),
        "independent_constraint_count": sum(
            kind == "independent" for kind, _, _ in constraints
        ),
        "relaxation_variable_count": len(relaxation_variables),
        "definition_clause_count": len(definition),
        "counter_auxiliary_variable_count": next_variable
        - 1
        - 42
        - len(relaxation_variables),
        "counter_clause_count": len(counter),
        "blocking_clause_count": len(blocks),
        "variable_count": next_variable - 1,
        "clause_count": len(clauses),
    }
    return next_variable - 1, clauses, counts


def check(
    catalog: Path,
    line_number: int,
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
    if not 1 <= line_number <= len(lines):
        raise ValueError("catalog line out of range")
    core = decode_short_graph6(lines[line_number - 1])
    if len(core) != 42:
        raise ValueError("core order is not 42")
    core_conflicts = conflicts(core)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    raw_models = metadata.get("models")
    if not isinstance(raw_models, list) or len(raw_models) != 2:
        raise ValueError("metadata must record exactly two models")
    model_bits = [str(record.get("bits")) for record in raw_models]
    if len(set(model_bits)) != 2:
        raise ValueError("metadata models are not distinct")
    variable_count, expected_clauses, counts = expected_formula(core, model_bits)

    model_checks: list[dict[str, object]] = []
    constraints = extension_constraints(core)
    for bits, record in zip(model_bits, raw_models, strict=True):
        extended_conflicts = conflicts(extend(core, bits))
        violated = []
        values = tuple(bit == "1" for bit in bits)
        for kind, vertices, clause in constraints:
            if not any(
                values[abs(literal) - 1] == (literal > 0)
                for literal in clause
            ):
                violated.append((kind, vertices + (42,)))
        recorded_conflicts = [
            (str(item.get("colour")), tuple(item.get("vertices", [])))
            for item in record.get("conflicts", [])
        ]
        valid = (
            len(violated) == 2
            and extended_conflicts == violated
            and recorded_conflicts == violated
            and record.get("extension_cost") == 2
        )
        model_checks.append(
            {
                "bits": bits,
                "extension_cost": len(violated),
                "full_graph_conflict_count": len(extended_conflicts),
                "record_matches": valid,
            }
        )

    digest = hashlib.sha256()
    declared_variables: int | None = None
    declared_clauses: int | None = None
    observed_count = 0
    current: list[int] = []
    expected = iter(expected_clauses)
    first_mismatch: dict[str, object] | None = None
    generator_seen = False
    with cnf.open("rb") as stream:
        for line_number_in_file, raw in enumerate(stream, start=1):
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
                    wanted = next(expected, None)
                    observed = tuple(current)
                    if first_mismatch is None and observed != wanted:
                        first_mismatch = {
                            "clause_index": observed_count,
                            "line_number": line_number_in_file,
                            "expected": list(wanted) if wanted is not None else None,
                            "actual": list(observed),
                        }
                    current = []
    missing_count = sum(1 for _ in expected)
    cnf_sha256 = digest.hexdigest()

    metadata_matches = (
        metadata.get("generator") == GENERATOR_ID
        and metadata.get("catalog_sha256")
        == hashlib.sha256(catalog_bytes).hexdigest()
        and metadata.get("catalog_line") == line_number
        and metadata.get("core_graph6") == lines[line_number - 1]
        and metadata.get("counter_encoding") == COUNTER_ID
        and metadata.get("conflict_bound") == 2
        and metadata.get("cnf_sha256") == cnf_sha256
        and metadata.get("cnf_bytes") == cnf.stat().st_size
        and all(metadata.get(key) == value for key, value in counts.items())
    )
    valid = (
        not core_conflicts
        and all(check["record_matches"] for check in model_checks)
        and generator_seen
        and declared_variables == variable_count
        and declared_clauses == len(expected_clauses)
        and observed_count == len(expected_clauses)
        and not current
        and missing_count == 0
        and first_mismatch is None
        and metadata_matches
    )
    return {
        "checker": CHECKER_ID,
        "valid": valid,
        "catalog_line": line_number,
        "core_forbidden_count": len(core_conflicts),
        "model_checks": model_checks,
        "declared_variable_count": declared_variables,
        "expected_variable_count": variable_count,
        "declared_clause_count": declared_clauses,
        "expected_clause_count": len(expected_clauses),
        "observed_clause_count": observed_count,
        "missing_expected_clause_count": missing_count,
        "first_mismatch": first_mismatch,
        "metadata_matches": metadata_matches,
        "cnf_sha256": cnf_sha256,
        "cnf_bytes": cnf.stat().st_size,
        **counts,
        "runtime_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--line", type=int, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = check(args.catalog, args.line, args.cnf, args.metadata)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
