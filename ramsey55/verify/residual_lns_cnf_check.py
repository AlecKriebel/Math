#!/usr/bin/env python3
"""Independent direct 5-subset audit of a fixed-boundary free-edge CNF."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path


CHECKER_ID = "residual_lns_direct_subset_cnf_checker_v1"


def decode_graph6(raw: bytes) -> list[int]:
    lines = [
        line.strip()
        for line in raw.splitlines()
        if line.strip() and not line.startswith(b"#")
    ]
    if not lines:
        raise ValueError("graph file has no data line")
    line = lines[0]
    if line.startswith(b">>graph6<<"):
        line = line[len(b">>graph6<<") :]
    order = line[0] - 63
    if not 0 <= order <= 62:
        raise ValueError("checker supports only short graph6")
    adjacency = [0] * order
    bit_index = 0
    for right in range(1, order):
        for left in range(right):
            value = line[1 + bit_index // 6] - 63
            if not 0 <= value < 64:
                raise ValueError("invalid graph6 byte")
            if (value >> (5 - bit_index % 6)) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            bit_index += 1
    return adjacency


def parse_edge(text: str) -> tuple[int, int]:
    fields = text.split(",")
    if len(fields) != 2:
        raise argparse.ArgumentTypeError("edge must have form LEFT,RIGHT")
    return int(fields[0]), int(fields[1])


def parse_vertices(text: str) -> tuple[int, ...]:
    return tuple(int(field) for field in text.split(",")) if text else ()


def free_edge_order(
    order: int,
    vertices: tuple[int, ...],
    extra_edges: list[tuple[int, int]],
    incident_vertices: tuple[int, ...] = (),
) -> tuple[tuple[int, int], ...]:
    if any(
        vertex < 0 or vertex >= order
        for vertex in itertools.chain(vertices, incident_vertices)
    ):
        raise ValueError("a free vertex is outside the graph")
    incident = set(incident_vertices)
    edges = {
        tuple(sorted(edge))
        for edge in itertools.chain(
            itertools.combinations(sorted(set(vertices)), 2),
            (
                (left, right)
                for left, right in itertools.combinations(range(order), 2)
                if left in incident or right in incident
            ),
            extra_edges,
        )
    }
    if not edges or any(not 0 <= left < right < order for left, right in edges):
        raise ValueError("invalid free-edge neighborhood")
    return tuple(sorted(edges))


def reconstruct(
    adjacency: list[int],
    free_edges: tuple[tuple[int, int], ...],
    forbidden_size: int,
) -> tuple[list[tuple[int, ...]], int, int]:
    variable = {edge: index for index, edge in enumerate(free_edges, 1)}
    negative: list[tuple[int, ...]] = []
    positive: list[tuple[int, ...]] = []
    for subset in itertools.combinations(range(len(adjacency)), forbidden_size):
        changing: list[int] = []
        fixed_edges = 0
        fixed_nonedges = 0
        for left, right in itertools.combinations(subset, 2):
            edge_variable = variable.get((left, right))
            if edge_variable is not None:
                changing.append(edge_variable)
            elif (adjacency[left] >> right) & 1:
                fixed_edges += 1
            else:
                fixed_nonedges += 1
        if fixed_nonedges == 0:
            negative.append(tuple(-item for item in changing))
        if fixed_edges == 0:
            positive.append(tuple(changing))
    return negative + positive, len(negative), len(positive)


def read_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables: int | None = None
    expected: int | None = None
    clauses: list[tuple[int, ...]] = []
    current: list[int] = []
    for raw in path.read_text(encoding="ascii").splitlines():
        fields = raw.split()
        if not fields or fields[0] == "c":
            continue
        if fields[0] == "p":
            if variables is not None or len(fields) != 4 or fields[1] != "cnf":
                raise ValueError("invalid DIMACS header")
            variables, expected = int(fields[2]), int(fields[3])
            continue
        if variables is None:
            raise ValueError("clause precedes DIMACS header")
        for field in fields:
            literal = int(field)
            if literal:
                if not 1 <= abs(literal) <= variables:
                    raise ValueError("literal outside declared range")
                current.append(literal)
            else:
                clauses.append(tuple(current))
                current = []
    if (
        variables is None
        or expected is None
        or current
        or len(clauses) != expected
    ):
        raise ValueError("malformed DIMACS")
    return variables, clauses


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--forbidden-size", type=int, default=5)
    parser.add_argument("--free-vertices", type=parse_vertices, default=())
    parser.add_argument(
        "--free-incident-vertices",
        type=parse_vertices,
        default=(),
        help="reconstruct every edge incident to a listed vertex as free",
    )
    parser.add_argument(
        "--free-edge", type=parse_edge, action="append", default=[]
    )
    args = parser.parse_args()
    started = time.monotonic()

    graph_bytes = args.graph.read_bytes()
    adjacency = decode_graph6(graph_bytes)
    edges = free_edge_order(
        len(adjacency),
        args.free_vertices,
        args.free_edge,
        args.free_incident_vertices,
    )
    expected, negative_count, positive_count = reconstruct(
        adjacency, edges, args.forbidden_size
    )
    variables, actual = read_dimacs(args.cnf)
    expected_counts = Counter(expected)
    actual_counts = Counter(actual)
    missing = expected_counts - actual_counts
    extra = actual_counts - expected_counts
    valid = (
        variables == len(edges)
        and actual == expected
        and not missing
        and not extra
    )
    result = {
        "checker": CHECKER_ID,
        "valid": valid,
        "graph_sha256": hashlib.sha256(graph_bytes).hexdigest(),
        "cnf_sha256": hashlib.sha256(args.cnf.read_bytes()).hexdigest(),
        "variable_count": variables,
        "expected_variable_count": len(edges),
        "clause_count": len(actual),
        "reconstructed_clause_count": len(expected),
        "clique_clause_count": negative_count,
        "independent_clause_count": positive_count,
        "missing_clause_count": sum(missing.values()),
        "extra_clause_count": sum(extra.values()),
        "exact_order_match": actual == expected,
        "runtime_seconds": time.monotonic() - started,
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
