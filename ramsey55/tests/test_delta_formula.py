#!/usr/bin/env python3
"""Independent exhaustive check of the common-neighborhood flip identity."""

from __future__ import annotations

import argparse
import itertools
import json


def objective(adjacency: list[int]) -> int:
    total = 0
    for subset in itertools.combinations(range(len(adjacency)), 5):
        edges = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(subset, 2)
        )
        total += edges in (0, 10)
    return total


def triple_count(adjacency: list[int], vertices: list[int], want_edge: bool) -> int:
    total = 0
    for triple in itertools.combinations(vertices, 3):
        edges = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(triple, 2)
        )
        total += edges == (3 if want_edge else 0)
    return total


def formula_delta(adjacency: list[int], left: int, right: int) -> int:
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
    triangles = triple_count(adjacency, common_neighbors, True)
    independent_triples = triple_count(adjacency, common_nonneighbors, False)
    old_edge = (adjacency[left] >> right) & 1
    return independent_triples - triangles if old_edge else triangles - independent_triples


def flip(adjacency: list[int], left: int, right: int) -> list[int]:
    result = adjacency.copy()
    result[left] ^= 1 << right
    result[right] ^= 1 << left
    return result


def exhaustive_check(n: int) -> dict:
    pairs = list(itertools.combinations(range(n), 2))
    cases = 0
    for encoding in range(1 << len(pairs)):
        adjacency = [0] * n
        for bit, (left, right) in enumerate(pairs):
            if (encoding >> bit) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
        before = objective(adjacency)
        for left, right in pairs:
            expected = objective(flip(adjacency, left, right)) - before
            observed = formula_delta(adjacency, left, right)
            if expected != observed:
                raise AssertionError(
                    f"delta mismatch graph={encoding} pair={left,right}: "
                    f"{observed} != {expected}"
                )
            cases += 1
    return {"n": n, "graphs": 1 << len(pairs), "flip_cases": cases, "status": "PASS"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    args = parser.parse_args()
    print(json.dumps(exhaustive_check(args.n), sort_keys=True))


if __name__ == "__main__":
    main()
