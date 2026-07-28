#!/usr/bin/env python3
"""Finite abstract audit of the fixed-pivot repair recurrence.

This is not the proof of the all-order theorem.  It independently exhausts
all labeled isolate-free bipartite link graphs through order six and checks
the exact closure rule used in Theorems 2.1 and 3.2.
"""

from __future__ import annotations

import itertools
import json


def bipartition(adjacency):
    colors = {}
    components = {}
    component = 0
    for root in range(len(adjacency)):
        if root in colors:
            continue
        colors[root] = 0
        components[root] = component
        stack = [root]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if other not in colors:
                    colors[other] = 1 - colors[vertex]
                    components[other] = component
                    stack.append(other)
                elif colors[other] == colors[vertex]:
                    return None
        component += 1
    return colors, components


def repair_closure(adjacency, source, target):
    orientations = {(source, target)}
    while True:
        added = set()
        for left, right in orientations:
            for left_neighbor in adjacency[left]:
                for right_neighbor in adjacency[right]:
                    new_orientation = (right_neighbor, left_neighbor)
                    if (
                        right_neighbor == left_neighbor
                        or left_neighbor in adjacency[right_neighbor]
                        or (left_neighbor, right_neighbor) in orientations
                    ):
                        return orientations, True
                    if new_orientation not in orientations:
                        added.add(new_orientation)
        if not added:
            return orientations, False
        orientations.update(added)


def evaluate():
    rows = []
    totals = {
        "bipartite_isolate_free_graphs": 0,
        "oriented_nonedge_roots": 0,
        "same_component_roots": 0,
        "separated_component_roots": 0,
        "checkerboard_pairs_checked": 0,
    }
    for order in range(2, 7):
        edges = list(itertools.combinations(range(order), 2))
        row = {
            "order": order,
            "bipartite_isolate_free_graphs": 0,
            "oriented_nonedge_roots": 0,
            "same_component_roots": 0,
            "separated_component_roots": 0,
            "checkerboard_pairs_checked": 0,
        }
        for mask in range(1 << len(edges)):
            adjacency = [set() for _ in range(order)]
            for offset, (left, right) in enumerate(edges):
                if (mask >> offset) & 1:
                    adjacency[left].add(right)
                    adjacency[right].add(left)
            if any(not neighbors for neighbors in adjacency):
                continue
            partition = bipartition(adjacency)
            if partition is None:
                continue
            colors, components = partition
            row["bipartite_isolate_free_graphs"] += 1

            for source in range(order):
                for target in range(order):
                    if source == target or target in adjacency[source]:
                        continue
                    row["oriented_nonedge_roots"] += 1
                    orientations, inconsistent = repair_closure(
                        adjacency, source, target
                    )
                    if components[source] == components[target]:
                        row["same_component_roots"] += 1
                        if not inconsistent:
                            raise AssertionError(
                                "same-component repair closure stayed consistent"
                            )
                        continue

                    row["separated_component_roots"] += 1
                    if inconsistent:
                        raise AssertionError(
                            "separated-component repair closure became inconsistent"
                        )
                    for left in range(order):
                        if components[left] != components[source]:
                            continue
                        for right in range(order):
                            if components[right] != components[target]:
                                continue
                            if (
                                colors[left] == colors[source]
                                and colors[right] == colors[target]
                            ):
                                expected = (left, right)
                            elif (
                                colors[left] != colors[source]
                                and colors[right] != colors[target]
                            ):
                                expected = (right, left)
                            else:
                                continue
                            row["checkerboard_pairs_checked"] += 1
                            if expected not in orientations:
                                raise AssertionError(
                                    "missing checkerboard orientation"
                                )
        rows.append(row)
        for key in totals:
            totals[key] += row[key]

    return {
        "schema": "repair-square-abstract-closure-audit-v1",
        "status": "PASS",
        "scope": (
            "finite bookkeeping audit through link order six; "
            "the all-order proof is in NOTE.md"
        ),
        "rows": rows,
        "totals": totals,
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
