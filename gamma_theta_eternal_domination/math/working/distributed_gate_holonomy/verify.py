#!/usr/bin/env python3
"""Independent bounded stress audit for the parity theorem.

The human proof in NOTE.md is universal and does not depend on this file.
This checker rebuilds the greatest eternal families of four accepted
equality controls, reconstructs their response lists, and searches their
short physical paths for a violation of Theorem 2.1.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations, permutations
import argparse
import json
from pathlib import Path


CONTROLS = (
    "LFzJbZYhdrDZdM",
    "MFzJbZYhlrDZdMhd_",
    "NFzJbZZhlrDZdMhd|h_",
    "MEXrtIdmdjLQqztC?",
)


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def decode_graph6(record: str) -> tuple[int, set[tuple[int, int]]]:
    order = ord(record[0]) - 63
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    if len(bits) < needed:
        raise ValueError("truncated graph6")
    edges: set[tuple[int, int]] = set()
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                edges.add((low, high))
            cursor += 1
    return order, edges


def greatest_family(
    order: int,
    g_edges: set[tuple[int, int]],
) -> set[frozenset[int]]:
    def g_edge(u: int, v: int) -> bool:
        return u != v and pair(u, v) in g_edges

    def dominates(state: frozenset[int]) -> bool:
        return all(
            vertex in state
            or any(g_edge(vertex, guard) for guard in state)
            for vertex in range(order)
        )

    family = {
        frozenset(state)
        for state in combinations(range(order), 3)
        if dominates(frozenset(state))
    }
    while True:
        remove: set[frozenset[int]] = set()
        for state in family:
            for attacked in range(order):
                if attacked in state:
                    continue
                if not any(
                    g_edge(guard, attacked)
                    and (state - {guard}) | {attacked} in family
                    for guard in state
                ):
                    remove.add(state)
                    break
        if not remove:
            return family
        family.difference_update(remove)


def simple_paths(
    start: int,
    finish: int,
    allowed: set[int],
    h_edges: set[tuple[int, int]],
    max_length: int,
) -> list[tuple[int, ...]]:
    answer: list[tuple[int, ...]] = []

    def visit(path: tuple[int, ...]) -> None:
        if len(path) - 1 > max_length:
            return
        vertex = path[-1]
        if vertex == finish:
            answer.append(path)
            return
        for neighbor in sorted(allowed):
            if neighbor in path or pair(vertex, neighbor) not in h_edges:
                continue
            visit((*path, neighbor))

    visit((start,))
    return answer


def audit_control(record: str, max_length: int) -> dict[str, object]:
    order, g_edges = decode_graph6(record)
    all_pairs = {pair(u, v) for u, v in combinations(range(order), 2)}
    h_edges = all_pairs - g_edges
    family = greatest_family(order, g_edges)
    anchor_set = frozenset((0, 1, 2))
    if anchor_set not in family:
        raise AssertionError("accepted control lost anchor state")
    lists = {
        vertex: frozenset(
            anchor
            for anchor in anchor_set
            if (anchor_set - {anchor}) | {vertex} in family
        )
        for vertex in range(3, order)
    }

    checked_path_pairs = 0
    opposite_parity_candidates = 0
    violations: list[dict[str, object]] = []
    same_parity_examples: list[dict[str, object]] = []

    for a, b, c in permutations((0, 1, 2)):
        wc = {vertex for vertex in range(3, order) if c not in lists[vertex]}
        wa = {vertex for vertex in range(3, order) if a not in lists[vertex]}
        for x0 in sorted(wc):
            for xm in sorted(wc):
                if a not in lists[x0]:
                    continue
                x_paths = simple_paths(x0, xm, wc, h_edges, max_length)
                if not x_paths:
                    continue
                for y0 in sorted(wa):
                    for yn in sorted(wa):
                        if not {x0, xm}.isdisjoint({y0, yn}) or c not in lists[y0]:
                            continue
                        if frozenset((b, x0, y0)) in family:
                            continue
                        if frozenset((b, xm, yn)) in family:
                            continue
                        y_paths = simple_paths(y0, yn, wa, h_edges, max_length)
                        if not y_paths:
                            continue
                        for x_path in x_paths:
                            x_vertices = set(x_path)
                            for y_path in y_paths:
                                if x_vertices.intersection(y_path):
                                    continue
                                checked_path_pairs += 1
                                mismatch = (len(x_path) - len(y_path)) % 2 != 0
                                item = {
                                    "anchors": [a, b, c],
                                    "x_path": list(x_path),
                                    "y_path": list(y_path),
                                }
                                if mismatch:
                                    opposite_parity_candidates += 1
                                    violations.append(item)
                                elif len(same_parity_examples) < 3:
                                    same_parity_examples.append(item)

    if violations:
        raise AssertionError(f"Theorem 2.1 violation in {record}: {violations[0]}")
    return {
        "graph6": record,
        "order": order,
        "greatest_family_size": len(family),
        "path_length_cutoff": max_length,
        "checked_vertex_disjoint_path_pairs": checked_path_pairs,
        "opposite_parity_candidates": opposite_parity_candidates,
        "same_parity_examples": same_parity_examples,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=6)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = {
        "schema": "distributed-gate-holonomy-stress-v1",
        "classification": "bounded stress audit; human theorem is independent",
        "controls": [
            audit_control(record, args.max_length)
            for record in CONTROLS
        ],
        "verdict": "PASS",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check is not None:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        if expected != result:
            raise AssertionError("result mismatch")
    if args.output is not None:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
