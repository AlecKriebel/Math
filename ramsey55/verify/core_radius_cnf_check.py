#!/usr/bin/env python3
"""Independent clause-by-clause checker for aggregate core-radius CNFs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path
from typing import Iterator

from direct_ramsey_cnf_check import independent_counter, independent_edge_table


CHECKER_ID = "ramsey55_core_radius_direct_structural_checker_v1"


def decode_graph6(path: Path) -> list[int]:
    lines = [
        line.strip()
        for line in path.read_text(encoding="ascii").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if len(lines) != 1:
        raise ValueError("base graph must have exactly one graph6 data line")
    raw = lines[0]
    order = ord(raw[0]) - 63
    if not 0 <= order <= 62:
        raise ValueError("only short graph6 is supported")
    adjacency = [0] * order
    bit = 0
    for right in range(1, order):
        for left in range(right):
            value = ord(raw[1 + bit // 6]) - 63
            if not 0 <= value < 64:
                raise ValueError("invalid graph6 payload")
            if (value >> (5 - bit % 6)) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            bit += 1
    return adjacency


def validated_boundary(
    adjacency: list[int],
    graph_bytes: bytes,
    boundary: dict[str, object],
) -> set[tuple[int, int]]:
    order = len(adjacency)
    graph_lines = [
        line.strip()
        for line in graph_bytes.decode("ascii").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if (
        len(graph_lines) != 1
        or boundary.get("order") != order
        or boundary.get("base_file_sha256")
        != hashlib.sha256(graph_bytes).hexdigest()
        or boundary.get("base_graph6") != graph_lines[0]
    ):
        raise ValueError("boundary base graph6/order/hash mismatch")
    raw_edges = boundary.get("free_edges")
    if not isinstance(raw_edges, list):
        raise ValueError("boundary free-edge list is missing")
    edges: list[tuple[int, int]] = []
    for raw in raw_edges:
        if (
            not isinstance(raw, list)
            or len(raw) != 2
            or type(raw[0]) is not int
            or type(raw[1]) is not int
            or not 0 <= raw[0] < raw[1] < order
        ):
            raise ValueError("noncanonical boundary edge")
        edges.append((raw[0], raw[1]))
    if edges != sorted(set(edges)) or boundary.get("variable_count") != len(edges):
        raise ValueError("boundary edges are duplicated, unsorted, or miscounted")
    incident = boundary.get("incident_free_vertices")
    induced = boundary.get("induced_free_vertices")
    if not isinstance(incident, list) or induced != []:
        raise ValueError("boundary is not pure incident-vertex mode")
    vertices = tuple(int(value) for value in incident)
    if vertices != tuple(sorted(set(vertices))):
        raise ValueError("incident vertices are not canonical")
    selected = set(vertices)
    exact = {
        edge
        for edge in itertools.combinations(range(order), 2)
        if edge[0] in selected or edge[1] in selected
    }
    if set(edges) != exact:
        raise ValueError("boundary is not the exact incident edge set")
    return set(edges)


def expected_formula(
    adjacency: list[int],
    free_edges: set[tuple[int, int]],
    radius: int,
) -> tuple[int, int, Iterator[tuple[int, ...]], dict[str, int]]:
    order = len(adjacency)
    edge_table = independent_edge_table(order)
    core_edges = tuple(
        edge
        for edge in itertools.combinations(range(order), 2)
        if edge not in free_edges
    )
    differences = tuple(
        (
            -edge_table[(left, right)]
            if (adjacency[left] >> right) & 1
            else edge_table[(left, right)]
        )
        for left, right in core_edges
    )
    counter_clauses, next_variable = independent_counter(
        differences, radius, len(edge_table) + 1
    )

    def clauses() -> Iterator[tuple[int, ...]]:
        for vertices in itertools.combinations(range(order), 5):
            variables = tuple(
                edge_table[(left, right)]
                for left, right in itertools.combinations(vertices, 2)
            )
            yield tuple(-variable for variable in variables)
            yield variables
        yield from counter_clauses

    ramsey_count = 2 * math.comb(order, 5)
    counts = {
        "primary_variable_count": len(edge_table),
        "auxiliary_variable_count": next_variable - 1 - len(edge_table),
        "core_edge_count": len(core_edges),
        "free_boundary_edge_count": len(free_edges),
        "ramsey_clause_count": ramsey_count,
        "counter_clause_count": len(counter_clauses),
    }
    return (
        next_variable - 1,
        ramsey_count + len(counter_clauses),
        clauses(),
        counts,
    )


def check(
    cnf: Path,
    graph: Path,
    boundary_metadata: Path,
    generation_metadata: Path,
    radius: int,
) -> dict[str, object]:
    started = time.monotonic()
    graph_bytes = graph.read_bytes()
    adjacency = decode_graph6(graph)
    boundary = json.loads(boundary_metadata.read_text(encoding="utf-8"))
    metadata = json.loads(generation_metadata.read_text(encoding="utf-8"))
    free_edges = validated_boundary(adjacency, graph_bytes, boundary)
    expected_variables, expected_clauses, expected, counts = expected_formula(
        adjacency, free_edges, radius
    )
    digest = hashlib.sha256()
    declared_variables: int | None = None
    declared_clauses: int | None = None
    current: list[int] = []
    actual_count = 0
    first_mismatch: dict[str, object] | None = None

    with cnf.open("rb") as stream:
        for line_number, raw in enumerate(stream, start=1):
            digest.update(raw)
            fields = raw.decode("ascii").split()
            if not fields or fields[0] == "c":
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
                    actual_count += 1
                    try:
                        wanted = next(expected)
                    except StopIteration:
                        wanted = None
                    observed = tuple(current)
                    if first_mismatch is None and observed != wanted:
                        first_mismatch = {
                            "clause_index": actual_count,
                            "line_number": line_number,
                            "expected": list(wanted) if wanted is not None else None,
                            "actual": list(observed),
                        }
                    current = []
    missing = sum(1 for _ in expected)
    cnf_sha256 = digest.hexdigest()
    metadata_matches = (
        metadata.get("cnf_sha256") == cnf_sha256
        and metadata.get("radius") == radius
        and metadata.get("base_graph_sha256")
        == hashlib.sha256(graph_bytes).hexdigest()
        and metadata.get("boundary_metadata_sha256")
        == hashlib.sha256(boundary_metadata.read_bytes()).hexdigest()
        and metadata.get("variable_count") == expected_variables
        and metadata.get("clause_count") == expected_clauses
        and all(metadata.get(key) == value for key, value in counts.items())
    )
    valid = (
        declared_variables == expected_variables
        and declared_clauses == expected_clauses
        and actual_count == expected_clauses
        and not current
        and not missing
        and first_mismatch is None
        and metadata_matches
    )
    result: dict[str, object] = {
        "checker": CHECKER_ID,
        "valid": valid,
        "radius": radius,
        "cnf_sha256": cnf_sha256,
        "cnf_bytes": cnf.stat().st_size,
        "declared_variable_count": declared_variables,
        "expected_variable_count": expected_variables,
        "declared_clause_count": declared_clauses,
        "actual_clause_count": actual_count,
        "expected_clause_count": expected_clauses,
        "missing_expected_clause_count": missing,
        "metadata_matches": metadata_matches,
        **counts,
        "runtime_seconds": time.monotonic() - started,
    }
    if first_mismatch is not None:
        result["first_mismatch"] = first_mismatch
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--boundary-metadata", type=Path, required=True)
    parser.add_argument("--generation-metadata", type=Path, required=True)
    parser.add_argument("--radius", type=int, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = check(
            args.cnf,
            args.graph,
            args.boundary_metadata,
            args.generation_metadata,
            args.radius,
        )
    except (OSError, ValueError, KeyError, UnicodeError) as error:
        result = {
            "checker": CHECKER_ID,
            "valid": False,
            "error": str(error),
        }
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
