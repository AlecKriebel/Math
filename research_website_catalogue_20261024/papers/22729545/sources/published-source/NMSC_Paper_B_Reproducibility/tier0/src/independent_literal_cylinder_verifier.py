#!/usr/bin/env python3
"""Recompute literal cylinders by complete hidden-route assignments.

This implementation imports neither Paper B nor the finite-atlas builder.  It
starts from raw arc lists, constructs every root-to-sample route, takes their
Cartesian product, and unions the actual first-/second-merger cylinders.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
from typing import Mapping, Sequence

from record_schema import make_record, write_jsonl


SCHEMA = "nmsc-independent-literal-cylinder-manifest-v1"
JOB = "independent_literal_cylinders"


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def language_digest(value: object) -> str:
    return sha256(canonical(value).encode()).hexdigest()


def construct_graph(case: Mapping[str, object]) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = [
        ("TOP", "ROOT"), ("ROOT", "S"), ("ROOT", "O")
    ]
    repair = set(case["repair"])
    probe_segment = int(case["probe_segment"])
    position = str(case["probe_position"])
    for segment, arc in enumerate(case["core_arcs"]):
        tail, head = map(str, arc)
        chain = [tail]
        if segment == probe_segment and position == "above-anchor":
            chain.append("ZPORT")
        if segment in repair:
            chain.append(f"R{segment}")
        if segment == probe_segment and position != "above-anchor":
            chain.append("ZPORT")
        chain.append(head)
        edges.extend(zip(chain, chain[1:]))
        if segment in repair:
            edges.append((f"R{segment}", f"L{segment}"))
        if segment == probe_segment:
            edges.append(("ZPORT", "Z"))
    for sink in case["sinks"]:
        edges.append((str(sink), f"C_{sink}"))
    transport = case["transport"]
    return [
        (str(transport.get(tail, tail)), str(transport.get(head, head)))
        for tail, head in edges
    ]


def routes(
    edges: Sequence[tuple[str, str]], source: str, target: str
) -> tuple[tuple[int, ...], ...]:
    outgoing: dict[str, list[int]] = {}
    for edge_id, (tail, _) in enumerate(edges):
        outgoing.setdefault(tail, []).append(edge_id)
    found: list[tuple[int, ...]] = []

    def visit(node: str, path: tuple[int, ...], seen: frozenset[str]) -> None:
        if node == target:
            found.append(path)
            return
        for edge_id in outgoing.get(node, ()):
            head = edges[edge_id][1]
            if head not in seen:
                visit(head, path + (edge_id,), seen | {head})

    visit(source, (), frozenset({source}))
    return tuple(found)


def chamber(
    edge_id: int,
    edges: Sequence[tuple[str, str]],
    ranks: Mapping[str, int],
) -> list[int]:
    tail, head = edges[edge_id]
    return [int(ranks[head]), int(ranks[tail])]


def enumerate_language(case: Mapping[str, object]) -> list[dict[str, object]]:
    edges = construct_graph(case)
    labels = tuple(sorted(map(str, case["labels"])))
    ranks = {str(key): int(value) for key, value in case["ranks"].items()}
    if any(ranks[tail] <= ranks[head] for tail, head in edges):
        raise ValueError("manifest ranks are not a strict temporal extension")
    route_sets = {label: routes(edges, "TOP", label) for label in labels}
    if any(not value for value in route_sets.values()):
        raise ValueError("manifest sample has no route")
    records: dict[str, dict[str, object]] = {}
    # The complete product is intentional: this is a different computation
    # from the builder's pairwise reachability union.
    for assignment_tuple in product(*(route_sets[label] for label in labels)):
        assignment = dict(zip(labels, assignment_tuple))
        for left, right in combinations(labels, 2):
            for first in set(assignment[left]).intersection(assignment[right]):
                row = {
                    "event": "first_merger",
                    "pair": [left, right],
                    "open_chamber": chamber(first, edges, ranks),
                    "no_unlisted_selected_merger": True,
                }
                records[canonical(row)] = row
        for triple in combinations(labels, 3):
            for pair in combinations(triple, 2):
                left, right = pair
                third = next(label for label in triple if label not in pair)
                left_path, right_path = assignment[left], assignment[right]
                for first in set(left_path).intersection(right_path):
                    for continuation in (left_path, right_path):
                        first_position = continuation.index(first)
                        for second in continuation[: first_position + 1]:
                            if second not in assignment[third]:
                                continue
                            row = {
                                "event": "first_then_second_merger",
                                "first_pair": [left, right],
                                "third": third,
                                "first_open_chamber": chamber(
                                    first, edges, ranks
                                ),
                                "second_open_chamber": chamber(
                                    second, edges, ranks
                                ),
                                "no_unlisted_selected_merger": True,
                            }
                            records[canonical(row)] = row
    return [records[key] for key in sorted(records)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    if manifest.get("schema") != SCHEMA:
        raise SystemExit("unexpected literal-cylinder manifest schema")
    cases = manifest.get("cases", [])
    if len(cases) != 5 or len({row.get("case_id") for row in cases}) != 5:
        raise SystemExit("manifest must contain one unique case per core")
    output = []
    for case in cases:
        language = enumerate_language(case)
        observed_digest = language_digest(language)
        observed_count = len(language)
        first = language[0] if language else None
        expected = (
            observed_digest == case["expected_literal_language_sha256"]
            and observed_count == case["expected_literal_language_count"]
            and first == case["first_literal_cylinder"]
        )
        output.append(
            make_record(
                job=JOB,
                case_input=case,
                status="PASS" if expected else "BLOCKING",
                graph={
                    "core_arcs": case["core_arcs"],
                    "repair": case["repair"],
                    "probe_segment": case["probe_segment"],
                    "probe_position": case["probe_position"],
                    "transport": case["transport"],
                    "ranks": case["ranks"],
                },
                exact_witness={
                    "literal_language_count": observed_count,
                    "literal_language_sha256": observed_digest,
                    "first_literal_cylinder": first,
                    "enumeration": "Cartesian product of complete hidden-route assignments",
                },
                declared_quotient_orbit={
                    "role": "literal cylinder recomputation only",
                    "raw_route_assignments_not_observed": True,
                },
                notes=(
                    "Independent route-assignment enumeration reproduced the "
                    "actual first-/second-merger cylinder language."
                ),
            )
        )
    write_jsonl(args.out, output)
    print(f"INDEPENDENT_LITERAL_CYLINDERS_OK cases={len(output)}")


if __name__ == "__main__":
    main()
