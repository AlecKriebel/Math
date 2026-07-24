#!/usr/bin/env python3
"""Independent acceptance check for a 237-edge incident-LNS candidate.

This verifier intentionally imports neither the constructive search nor the
fixed-boundary CNF generator.  It decodes graph6 directly, checks that the
metadata names exactly the expected incident-edge neighborhood, confirms that
all other edges stayed fixed, exhaustively recounts forbidden vertex sets, and
optionally evaluates the retained DIMACS CNF under the candidate assignment.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path
from typing import Sequence

VERIFIER_ID = "independent_incident_lns_candidate_v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def graph6_line(path: Path, line_number: int = 1) -> str:
    if line_number < 1:
        raise ValueError("line number must be positive")
    with path.open("r", encoding="ascii", newline="") as stream:
        for current, raw in enumerate(stream, 1):
            if current == line_number:
                line = raw.rstrip("\r\n")
                break
        else:
            raise ValueError(f"graph6 line {line_number} is absent from {path}")
    if line.startswith(">>graph6<<"):
        line = line[10:]
    if not line:
        raise ValueError(f"empty graph6 record in {path}")
    return line


def decode_graph6(line: str) -> tuple[int, ...]:
    first = ord(line[0])
    if first < 63 or first > 125:
        raise ValueError("only short graph6 order records are supported")
    n = first - 63
    required_bits = n * (n - 1) // 2
    required_characters = 1 + (required_bits + 5) // 6
    if len(line) != required_characters:
        raise ValueError(
            f"graph6 length mismatch: expected {required_characters}, got {len(line)}"
        )
    adjacency = [0] * n
    bit_index = 0
    for right in range(1, n):
        for left in range(right):
            value = ord(line[1 + bit_index // 6]) - 63
            if not 0 <= value < 64:
                raise ValueError("invalid graph6 data byte")
            if (value >> (5 - bit_index % 6)) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            bit_index += 1
    return tuple(adjacency)


def parse_vertices(raw: str, n: int) -> tuple[int, ...]:
    try:
        vertices = tuple(sorted({int(value) for value in raw.split(",") if value}))
    except ValueError as error:
        raise ValueError("incident vertices must be comma-separated integers") from error
    if not vertices:
        raise ValueError("at least one incident vertex is required")
    if vertices[0] < 0 or vertices[-1] >= n:
        raise ValueError(f"incident vertex outside 0..{n - 1}")
    return vertices


def expected_incident_edges(
    n: int, incident_vertices: Sequence[int]
) -> tuple[tuple[int, int], ...]:
    incident = frozenset(incident_vertices)
    return tuple(
        (left, right)
        for left in range(n)
        for right in range(left + 1, n)
        if left in incident or right in incident
    )


def edge_present(adjacency: Sequence[int], left: int, right: int) -> bool:
    return bool((adjacency[left] >> right) & 1)


def count_forbidden(adjacency: Sequence[int], k: int) -> tuple[int, int]:
    cliques = 0
    independent_sets = 0
    for vertices in itertools.combinations(range(len(adjacency)), k):
        all_edges = True
        no_edges = True
        for offset, left in enumerate(vertices):
            for right in vertices[offset + 1 :]:
                if edge_present(adjacency, left, right):
                    no_edges = False
                else:
                    all_edges = False
        cliques += int(all_edges)
        independent_sets += int(no_edges)
    return cliques, independent_sets


def normalized_metadata_edges(
    metadata: dict[str, object], n: int
) -> tuple[tuple[int, int], ...]:
    raw_edges = metadata.get("free_edges")
    if not isinstance(raw_edges, list):
        raise ValueError("metadata free_edges must be a list")
    edges: list[tuple[int, int]] = []
    for raw in raw_edges:
        if (
            not isinstance(raw, list)
            or len(raw) != 2
            or not all(isinstance(value, int) for value in raw)
        ):
            raise ValueError("metadata contains a malformed free edge")
        left, right = raw
        if not 0 <= left < right < n:
            raise ValueError(f"metadata contains invalid free edge {raw}")
        edges.append((left, right))
    if edges != sorted(set(edges)):
        raise ValueError("metadata free edges are not unique lexicographic pairs")
    return tuple(edges)


def parse_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variable_count: int | None = None
    declared_clauses: int | None = None
    clauses: list[tuple[int, ...]] = []
    with path.open("r", encoding="ascii") as stream:
        for line_number, raw in enumerate(stream, 1):
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p"):
                fields = line.split()
                if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
                    raise ValueError(f"malformed DIMACS header on line {line_number}")
                if variable_count is not None:
                    raise ValueError("duplicate DIMACS header")
                variable_count = int(fields[2])
                declared_clauses = int(fields[3])
                continue
            if variable_count is None:
                raise ValueError("DIMACS clause precedes header")
            literals = [int(value) for value in line.split()]
            if not literals or literals[-1] != 0 or 0 in literals[:-1]:
                raise ValueError(f"malformed DIMACS clause on line {line_number}")
            clause = tuple(literals[:-1])
            if any(abs(literal) > variable_count for literal in clause):
                raise ValueError(f"out-of-range literal on DIMACS line {line_number}")
            clauses.append(clause)
    if variable_count is None or declared_clauses is None:
        raise ValueError("DIMACS header is absent")
    if len(clauses) != declared_clauses:
        raise ValueError(
            f"DIMACS clause count mismatch: declared {declared_clauses}, "
            f"parsed {len(clauses)}"
        )
    return variable_count, clauses


def unsatisfied_clause_indices(
    clauses: Sequence[Sequence[int]], true_variables: frozenset[int]
) -> list[int]:
    return [
        index
        for index, clause in enumerate(clauses, 1)
        if not any(
            (literal > 0) == (abs(literal) in true_variables)
            for literal in clause
        )
    ]


def run(args: argparse.Namespace) -> dict[str, object]:
    base_line = graph6_line(args.base, args.base_line)
    candidate_line = graph6_line(args.candidate, args.candidate_line)
    base = decode_graph6(base_line)
    candidate = decode_graph6(candidate_line)
    if len(base) != len(candidate):
        raise ValueError("base and candidate graph orders differ")
    n = len(base)
    if not 2 <= args.k <= n:
        raise ValueError(f"k must lie in 2..{n}")

    incident_vertices = parse_vertices(args.incident_vertices, n)
    expected_edges = expected_incident_edges(n, incident_vertices)
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict):
        raise ValueError("metadata root must be an object")
    metadata_edges = normalized_metadata_edges(metadata, n)

    base_sha256 = sha256_file(args.base)
    metadata_checks = {
        "base_file_sha256": metadata.get("base_file_sha256") == base_sha256,
        "base_graph6": metadata.get("base_graph6") == base_line,
        "variable_count": metadata.get("variable_count") == len(metadata_edges),
        "free_edges_exactly_expected": metadata_edges == expected_edges,
    }

    metadata_base_true = metadata.get("base_true_variables")
    if not isinstance(metadata_base_true, list) or not all(
        isinstance(variable, int) for variable in metadata_base_true
    ):
        raise ValueError("metadata base_true_variables must be an integer list")
    observed_base_true = [
        variable
        for variable, (left, right) in enumerate(metadata_edges, 1)
        if edge_present(base, left, right)
    ]
    metadata_checks["base_true_variables"] = metadata_base_true == observed_base_true

    free_edge_set = frozenset(metadata_edges)
    changed_edges: list[tuple[int, int]] = []
    fixed_edge_changes: list[tuple[int, int]] = []
    for left in range(n):
        for right in range(left + 1, n):
            if edge_present(base, left, right) != edge_present(candidate, left, right):
                edge = (left, right)
                changed_edges.append(edge)
                if edge not in free_edge_set:
                    fixed_edge_changes.append(edge)

    candidate_true = frozenset(
        variable
        for variable, (left, right) in enumerate(metadata_edges, 1)
        if edge_present(candidate, left, right)
    )
    cliques, independent_sets = count_forbidden(candidate, args.k)
    degrees = sorted(row.bit_count() for row in candidate)
    edge_count = sum(degrees) // 2
    result: dict[str, object] = {
        "verifier": VERIFIER_ID,
        "base": str(args.base),
        "base_sha256": base_sha256,
        "candidate": str(args.candidate),
        "candidate_sha256": sha256_file(args.candidate),
        "metadata": str(args.metadata),
        "metadata_sha256": sha256_file(args.metadata),
        "n": n,
        "k": args.k,
        "incident_vertices": list(incident_vertices),
        "expected_free_edge_count": len(expected_edges),
        "metadata_free_edge_count": len(metadata_edges),
        "candidate_true_variable_count": len(candidate_true),
        "changed_edge_count": len(changed_edges),
        "changed_free_edge_count": len(changed_edges) - len(fixed_edge_changes),
        "changed_fixed_edge_count": len(fixed_edge_changes),
        "changed_fixed_edges": [list(edge) for edge in fixed_edge_changes],
        "metadata_checks": metadata_checks,
        "metadata_valid": all(metadata_checks.values()),
        "fixed_boundary_valid": not fixed_edge_changes,
        "clique_count": cliques,
        "independent_count": independent_sets,
        "objective": cliques + independent_sets,
        "ramsey_valid": cliques == 0 and independent_sets == 0,
    }

    if args.cnf is not None:
        variable_count, clauses = parse_dimacs(args.cnf)
        unsatisfied = unsatisfied_clause_indices(clauses, candidate_true)
        cnf_sha256 = sha256_file(args.cnf)
        cnf_checks = {
            "variable_count": variable_count == len(metadata_edges),
            "clause_count": metadata.get("clause_count") == len(clauses),
            "cnf_sha256": metadata.get("cnf_sha256") == cnf_sha256,
        }
        result.update(
            {
                "cnf": str(args.cnf),
                "cnf_sha256": cnf_sha256,
                "cnf_clause_count": len(clauses),
                "cnf_checks": cnf_checks,
                "cnf_metadata_valid": all(cnf_checks.values()),
                "cnf_unsatisfied_clause_count": len(unsatisfied),
                "cnf_first_unsatisfied_clause_indices": unsatisfied[:20],
                "cnf_satisfied": not unsatisfied,
            }
        )

    if args.search_json is not None:
        search_output = json.loads(args.search_json.read_text(encoding="utf-8"))
        if not isinstance(search_output, dict):
            raise ValueError("search stdout JSON root must be an object")
        search_output_checks = {
            "mode": search_output.get("mode") == "search",
            "algorithm": search_output.get("algorithm") == "incident_six_lns_v1",
            "graph6": search_output.get("graph6") == candidate_line,
            "C5": search_output.get("C5") == cliques,
            "I5": search_output.get("I5") == independent_sets,
            "E": search_output.get("E") == cliques + independent_sets,
            "edge_count": search_output.get("edge_count") == edge_count,
            "degree_sequence": search_output.get("degree_sequence") == degrees,
            "free_edge_count": search_output.get("free_edge_count")
            == len(metadata_edges),
            "fixed_edge_count": search_output.get("fixed_edge_count")
            == n * (n - 1) // 2 - len(metadata_edges),
            "fixed_edges_preserved": search_output.get("fixed_edges_preserved")
            is True,
            "changed_free_edges": search_output.get("changed_free_edges")
            == len(changed_edges) - len(fixed_edge_changes),
        }
        result.update(
            {
                "search_json": str(args.search_json),
                "search_json_sha256": sha256_file(args.search_json),
                "search_output_checks": search_output_checks,
                "search_output_valid": all(search_output_checks.values()),
            }
        )

    accepted = (
        bool(result["metadata_valid"])
        and bool(result["fixed_boundary_valid"])
        and bool(result["ramsey_valid"])
        and (args.cnf is None or bool(result["cnf_metadata_valid"]))
        and (args.cnf is None or bool(result["cnf_satisfied"]))
        and (args.search_json is None or bool(result["search_output_valid"]))
    )
    result["accepted"] = accepted
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--search-json", type=Path)
    parser.add_argument("--incident-vertices", required=True)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--base-line", type=int, default=1)
    parser.add_argument("--candidate-line", type=int, default=1)
    args = parser.parse_args()
    try:
        result = run(args)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        print(
            json.dumps(
                {"verifier": VERIFIER_ID, "accepted": False, "error": str(error)},
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
