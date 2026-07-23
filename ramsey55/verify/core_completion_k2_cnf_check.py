#!/usr/bin/env python3
"""Independently reconstruct the delete-(0,1), add-three-vertices CNF."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path


CHECKER_ID = "core_completion_k2_direct_five_subset_cnf_checker_v1"
CORE_ORDER = 40
NEW_ORDER = 3
VARIABLE_COUNT = 123


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
    if order != 42:
        raise ValueError("checker requires a 42-vertex short-graph6 input")
    adjacency = [0] * order
    bit_index = 0
    for right in range(1, order):
        for left in range(right):
            value = line[1 + bit_index // 6] - 63
            if not 0 <= value < 64:
                raise ValueError("invalid graph6 payload")
            if (value >> (5 - bit_index % 6)) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            bit_index += 1
    return adjacency


def delete_zero_one(adjacency: list[int]) -> list[int]:
    originals = list(range(2, 42))
    core = [0] * CORE_ORDER
    for left, old_left in enumerate(originals):
        for right in range(left + 1, CORE_ORDER):
            old_right = originals[right]
            if (adjacency[old_left] >> old_right) & 1:
                core[left] |= 1 << right
                core[right] |= 1 << left
    return core


def variable_for_edge(left: int, right: int) -> int:
    if left < CORE_ORDER:
        return (right - CORE_ORDER) * CORE_ORDER + left + 1
    new_pair_variables = {(0, 1): 121, (0, 2): 122, (1, 2): 123}
    return new_pair_variables[(left - CORE_ORDER, right - CORE_ORDER)]


def reconstruct(core: list[int]) -> set[frozenset[int]]:
    clauses: set[frozenset[int]] = set()
    for vertices in itertools.combinations(range(CORE_ORDER + NEW_ORDER), 5):
        if vertices[-1] < CORE_ORDER:
            continue
        fixed_edges: list[int] = []
        variables: list[int] = []
        for left, right in itertools.combinations(vertices, 2):
            if right < CORE_ORDER:
                fixed_edges.append((core[left] >> right) & 1)
            else:
                variables.append(variable_for_edge(left, right))
        if all(fixed_edges):
            clauses.add(frozenset(-variable for variable in variables))
        if not any(fixed_edges):
            clauses.add(frozenset(variables))
    return clauses


def read_dimacs(path: Path) -> tuple[int, list[frozenset[int]]]:
    variable_count: int | None = None
    declared_clauses: int | None = None
    clauses: list[frozenset[int]] = []
    pending: list[int] = []
    for raw in path.read_text(encoding="ascii").splitlines():
        fields = raw.split()
        if not fields or fields[0] == "c":
            continue
        if fields[0] == "p":
            if len(fields) != 4 or fields[1] != "cnf":
                raise ValueError("invalid DIMACS header")
            variable_count = int(fields[2])
            declared_clauses = int(fields[3])
            continue
        for token in fields:
            literal = int(token)
            if literal:
                pending.append(literal)
            else:
                clauses.append(frozenset(pending))
                pending = []
    if (
        variable_count is None
        or declared_clauses is None
        or pending
        or len(clauses) != declared_clauses
    ):
        raise ValueError("malformed DIMACS")
    return variable_count, clauses


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()

    graph_bytes = args.graph.read_bytes()
    expected = reconstruct(delete_zero_one(decode_graph6(graph_bytes)))
    variables, clauses = read_dimacs(args.cnf)
    actual = set(clauses)
    result = {
        "checker": CHECKER_ID,
        "valid": (
            variables == VARIABLE_COUNT
            and len(clauses) == len(actual)
            and actual == expected
        ),
        "graph_sha256": hashlib.sha256(graph_bytes).hexdigest(),
        "cnf_sha256": hashlib.sha256(args.cnf.read_bytes()).hexdigest(),
        "variable_count": variables,
        "clause_count": len(clauses),
        "unique_clause_count": len(actual),
        "reconstructed_clause_count": len(expected),
        "missing_clause_count": len(expected - actual),
        "extra_clause_count": len(actual - expected),
        "runtime_seconds": time.monotonic() - started,
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
