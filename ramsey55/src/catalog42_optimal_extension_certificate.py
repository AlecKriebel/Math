#!/usr/bin/env python3
"""Generate an exact-two-neighbourhood enumeration CNF for a fixed 42-core.

Each Boolean primary variable says whether the new vertex is adjacent to one
core vertex.  A relaxation variable is definitionally true exactly when the
new vertex completes a core clique or independent four-set.  A sequential
counter permits at most two such conflicts.  Blocking the supplied primary
assignments leaves an UNSAT formula precisely when they are every extension
with at most two conflicts.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import tempfile
from pathlib import Path

from direct_ramsey_cnf import COUNTER_ID, allocate_sequential_counter
from graph_io import decode_graph6, encode_graph6, validate_simple


GENERATOR_ID = "ramsey55_catalog42_optimal_extension_enumeration_cnf_v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def catalog_lines(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="ascii").splitlines()
        if line.strip() and not line.startswith("#")
    ]


def extension_constraints(
    adjacency: list[int],
) -> list[tuple[str, tuple[int, ...], tuple[int, ...]]]:
    validate_simple(adjacency)
    result: list[tuple[str, tuple[int, ...], tuple[int, ...]]] = []
    for vertices in itertools.combinations(range(len(adjacency)), 4):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
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


def parse_model(bits: str, order: int) -> tuple[bool, ...]:
    if len(bits) != order or set(bits) - {"0", "1"}:
        raise ValueError(f"model must be exactly {order} binary digits")
    return tuple(bit == "1" for bit in bits)


def model_cost(
    model: tuple[bool, ...],
    constraints: list[tuple[str, tuple[int, ...], tuple[int, ...]]],
) -> int:
    return sum(
        not any(model[abs(literal) - 1] == (literal > 0) for literal in clause)
        for _, _, clause in constraints
    )


def extend_graph(
    core: list[int], model: tuple[bool, ...]
) -> list[int]:
    if len(core) != len(model):
        raise ValueError("model length does not match core order")
    result = list(core) + [0]
    new_vertex = len(core)
    for vertex, adjacent in enumerate(model):
        if adjacent:
            result[vertex] |= 1 << new_vertex
            result[new_vertex] |= 1 << vertex
    validate_simple(result)
    return result


def homogeneous_five_sets(
    adjacency: list[int],
) -> list[tuple[str, tuple[int, ...]]]:
    result: list[tuple[str, tuple[int, ...]]] = []
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        if edge_count == 10:
            result.append(("clique", vertices))
        elif edge_count == 0:
            result.append(("independent", vertices))
    return result


def write_cnf(
    path: Path,
    clauses: list[tuple[int, ...]],
    variable_count: int,
    comments: list[str],
) -> dict[str, object]:
    path.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    byte_count = 0
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=path.name + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            for comment in comments:
                data = f"c {comment}\n".encode("ascii")
                stream.write(data)
                digest.update(data)
                byte_count += len(data)
            header = f"p cnf {variable_count} {len(clauses)}\n".encode("ascii")
            stream.write(header)
            digest.update(header)
            byte_count += len(header)
            for clause in clauses:
                data = (
                    " ".join(map(str, clause))
                    + (" " if clause else "")
                    + "0\n"
                ).encode("ascii")
                stream.write(data)
                digest.update(data)
                byte_count += len(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)
    return {
        "cnf_sha256": digest.hexdigest(),
        "cnf_bytes": byte_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--line", type=int, required=True)
    parser.add_argument("--model", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()

    lines = catalog_lines(args.catalog)
    if not 1 <= args.line <= len(lines):
        raise ValueError("catalog line is out of range")
    core = decode_graph6(lines[args.line - 1])
    if len(core) != 42:
        raise ValueError("expected an order-42 core")
    models = [parse_model(bits, 42) for bits in args.model]
    if len(models) != 2 or len(set(models)) != 2:
        raise ValueError("exactly two distinct models are required")

    constraints = extension_constraints(core)
    next_variable = 43
    relaxation_variables: list[int] = []
    definition_clauses: list[tuple[int, ...]] = []
    for _, _, clause in constraints:
        relaxation = next_variable
        next_variable += 1
        relaxation_variables.append(relaxation)
        # r is true exactly when every literal of the original clause is false.
        definition_clauses.append(clause + (relaxation,))
        definition_clauses.extend(
            (-relaxation, -literal) for literal in clause
        )
    counter, next_variable = allocate_sequential_counter(
        relaxation_variables,
        2,
        next_variable,
        "extension_conflicts_at_most_2",
    )
    counter_clauses = list(counter.clauses())
    blocking_clauses = [
        tuple(
            -(vertex + 1) if model[vertex] else vertex + 1
            for vertex in range(42)
        )
        for model in models
    ]
    clauses = definition_clauses + counter_clauses + blocking_clauses
    variable_count = next_variable - 1

    model_records: list[dict[str, object]] = []
    for bits, model in zip(args.model, models, strict=True):
        cost = model_cost(model, constraints)
        extended = extend_graph(core, model)
        conflicts = homogeneous_five_sets(extended)
        if cost != 2 or len(conflicts) != 2:
            raise ValueError("supplied model does not have exactly two conflicts")
        model_records.append(
            {
                "bits": bits,
                "extension_cost": cost,
                "extended_graph6": encode_graph6(extended),
                "edge_count": sum(row.bit_count() for row in extended) // 2,
                "degree_sequence": sorted(row.bit_count() for row in extended),
                "conflicts": [
                    {"colour": colour, "vertices": list(vertices)}
                    for colour, vertices in conflicts
                ],
            }
        )

    catalog_sha256 = sha256_file(args.catalog)
    comments = [
        f"generator {GENERATOR_ID}",
        f"catalog_sha256 {catalog_sha256}",
        f"catalog_line {args.line}",
        f"core_graph6 {lines[args.line - 1]}",
        "variables 1..42 are new-vertex adjacency bits",
        "one definitional conflict variable follows per core K4 or I4",
        f"counter_encoding {COUNTER_ID}",
        "final two clauses block the recorded primary assignments",
    ]
    written = write_cnf(args.output, clauses, variable_count, comments)
    metadata = {
        "generator": GENERATOR_ID,
        "catalog_path": str(args.catalog.resolve()),
        "catalog_sha256": catalog_sha256,
        "catalog_line": args.line,
        "core_graph6": lines[args.line - 1],
        "core_edge_count": sum(row.bit_count() for row in core) // 2,
        "primary_variable_count": 42,
        "constraint_count": len(constraints),
        "clique_constraint_count": sum(
            kind == "clique" for kind, _, _ in constraints
        ),
        "independent_constraint_count": sum(
            kind == "independent" for kind, _, _ in constraints
        ),
        "relaxation_variable_count": len(relaxation_variables),
        "definition_clause_count": len(definition_clauses),
        "counter_encoding": COUNTER_ID,
        "counter_auxiliary_variable_count": counter.auxiliary_count,
        "counter_clause_count": len(counter_clauses),
        "conflict_bound": 2,
        "blocking_clause_count": len(blocking_clauses),
        "variable_count": variable_count,
        "clause_count": len(clauses),
        "models": model_records,
        "enumeration_semantics": (
            "Removing the final two blocking clauses yields exactly the "
            "one-vertex extensions with at most two forbidden five-sets. "
            "UNSAT after both blocks proves the recorded primary assignments "
            "are the complete such set."
        ),
        "cnf_path": str(args.output.resolve()),
        **written,
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(
        json.dumps(metadata, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(metadata, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
