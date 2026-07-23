#!/usr/bin/env python3
"""Describe exact residual conflicts and local flip barriers."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

from graph_io import read_graph

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))
from exhaustive_verify import count_forbidden  # noqa: E402


def violating_sets(adjacency: list[int]) -> list[dict]:
    violations = []
    for subset in itertools.combinations(range(len(adjacency)), 5):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(subset, 2)
        )
        if edge_count == 10:
            violations.append({"type": "K5", "vertices": list(subset)})
        elif edge_count == 0:
            violations.append({"type": "I5", "vertices": list(subset)})
    return violations


def triple_count(adjacency: list[int], vertices: list[int], edges_wanted: int) -> int:
    return sum(
        sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(triple, 2)
        )
        == edges_wanted
        for triple in itertools.combinations(vertices, 3)
    )


def delta(adjacency: list[int], left: int, right: int) -> dict:
    n = len(adjacency)
    common_neighbors = [
        vertex
        for vertex in range(n)
        if vertex not in (left, right)
        and (adjacency[left] >> vertex) & 1
        and (adjacency[right] >> vertex) & 1
    ]
    common_nonneighbors = [
        vertex
        for vertex in range(n)
        if vertex not in (left, right)
        and not ((adjacency[left] >> vertex) & 1)
        and not ((adjacency[right] >> vertex) & 1)
    ]
    triangles = triple_count(adjacency, common_neighbors, 3)
    independent_triples = triple_count(adjacency, common_nonneighbors, 0)
    old_edge = bool((adjacency[left] >> right) & 1)
    change = (
        independent_triples - triangles
        if old_edge
        else triangles - independent_triples
    )
    return {
        "pair": [left, right],
        "operation": "delete" if old_edge else "add",
        "common_neighbor_triangles": triangles,
        "common_nonneighbor_independent_triples": independent_triples,
        "delta_E": change,
    }


def seed_distance(adjacency: list[int], seed: list[int]) -> dict:
    if len(adjacency) != len(seed) + 1:
        raise ValueError("seed must have one fewer vertex")
    changed = []
    for left in range(len(seed)):
        for right in range(left + 1, len(seed)):
            if ((adjacency[left] >> right) & 1) != ((seed[left] >> right) & 1):
                changed.append([left, right])
    new_vertex = len(seed)
    neighbors = [
        vertex
        for vertex in range(len(seed))
        if (adjacency[new_vertex] >> vertex) & 1
    ]
    return {
        "changed_core_edge_count": len(changed),
        "changed_core_edges": changed,
        "new_vertex": new_vertex,
        "new_vertex_degree": len(neighbors),
        "new_vertex_neighbors": neighbors,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("--seed-graph", type=Path)
    args = parser.parse_args()
    adjacency = read_graph(args.graph)
    conflicts = violating_sets(adjacency)
    objective = len(conflicts)
    conflict_pairs = sorted(
        {
            pair
            for conflict in conflicts
            for pair in itertools.combinations(conflict["vertices"], 2)
        }
    )
    moves = [delta(adjacency, *pair) for pair in conflict_pairs]
    moves.sort(key=lambda item: (item["delta_E"], item["pair"]))
    result = {
        "n": len(adjacency),
        "C5": sum(item["type"] == "K5" for item in conflicts),
        "I5": sum(item["type"] == "I5" for item in conflicts),
        "E": objective,
        "violations": conflicts,
        "conflict_union": sorted(
            {vertex for item in conflicts for vertex in item["vertices"]}
        ),
        "conflict_intersection": sorted(
            set(conflicts[0]["vertices"]).intersection(
                *(set(item["vertices"]) for item in conflicts[1:])
            )
            if conflicts
            else set()
        ),
        "moves_within_conflicts": moves,
        "best_single_flip_result_E": objective + min(
            (item["delta_E"] for item in moves), default=0
        ),
        "full_counter_crosscheck": sum(count_forbidden(adjacency, 5)),
    }
    if args.seed_graph:
        result["seed_distance"] = seed_distance(
            adjacency, read_graph(args.seed_graph)
        )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
