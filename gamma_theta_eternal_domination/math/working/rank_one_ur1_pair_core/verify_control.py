#!/usr/bin/env python3
"""Standalone verifier for two sharp QQ1 collision controls.

This file imports no search code.  It decodes two fixed graph6 records,
computes the static parameters and literal greatest one-guard kernels,
and checks the complete named rank-one collision.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter


CONTROLS = {
    "dominating-ux": "Mslamztl~fnny~]~_",
    "nondominating-ux": "NslalntvXzn^{~n||^w",
}
NAMES = {"u": 0, "x": 1, "p": 2, "q": 3, "r": 4, "b": 5, "c": 6}


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    values = [ord(char) - 63 for char in record]
    if not values or not (0 <= values[0] <= 62):
        raise ValueError("only short graph6 records are supported")
    order = values[0]
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    needed = order * (order - 1) // 2
    if len(bits) < needed or any(bits[needed:]):
        raise ValueError("truncated or nonzero-padded graph6 record")
    graph = [set() for _ in range(order)]
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                graph[left].add(right)
                graph[right].add(left)
            cursor += 1
    return tuple(frozenset(row) for row in graph)


def subsets(order: int, size: int):
    return tuple(
        frozenset(choice) for choice in itertools.combinations(range(order), size)
    )


def independent(graph, state) -> bool:
    return all(right not in graph[left] for left, right in itertools.combinations(state, 2))


def dominates(graph, state) -> bool:
    return all(
        vertex in state or bool(graph[vertex] & state)
        for vertex in range(len(graph))
    )


def kernel(graph, size: int):
    family = {
        state for state in subsets(len(graph), size) if dominates(graph, state)
    }
    ranks = {}
    round_number = 0
    removed_by_round = []
    while True:
        removed = set()
        for state in family:
            for target in range(len(graph)):
                if target in state:
                    continue
                if not any(
                    target in graph[guard]
                    and state - {guard} | {target} in family
                    for guard in state
                ):
                    removed.add(state)
                    break
        if not removed:
            return family, ranks, removed_by_round
        round_number += 1
        for state in removed:
            ranks[state] = round_number
        family.difference_update(removed)
        removed_by_round.append(len(removed))


def minimum_size(order: int, predicate) -> int:
    for size in range(1, order + 1):
        if any(predicate(state) for state in subsets(order, size)):
            return size
    raise AssertionError("no witness")


def graph_digest(graph) -> str:
    text = "\n".join(
        f"{left} {right}"
        for left in range(len(graph))
        for right in range(left + 1, len(graph))
        if right in graph[left]
    ) + "\n"
    return hashlib.sha256(text.encode("ascii")).hexdigest()


def clique_partition(graph):
    """Return a minimum partition of the vertices into G-cliques."""

    order = len(graph)
    vertices = sorted(
        range(order),
        key=lambda vertex: (len(graph[vertex]), vertex),
    )

    for count in range(1, order + 1):
        parts: list[list[int]] = [[] for _ in range(count)]

        def extend(offset: int, used: int) -> bool:
            if offset == order:
                return True
            vertex = vertices[offset]
            for color in range(min(used + 1, count)):
                if color == used and used == count:
                    continue
                if all(member in graph[vertex] for member in parts[color]):
                    parts[color].append(vertex)
                    if extend(offset + 1, max(used, color + 1)):
                        return True
                    parts[color].pop()
            return False

        if extend(0, 0):
            return [sorted(part) for part in parts if part]
    raise AssertionError("singleton partition must exist")


def evaluate_record(label: str, record: str):
    graph = decode_graph6(record)
    order = len(graph)
    gamma = minimum_size(order, lambda state: dominates(graph, state))
    independent_domination = minimum_size(
        order,
        lambda state: independent(graph, state) and dominates(graph, state),
    )
    alpha = max(
        size
        for size in range(1, order + 1)
        if any(independent(graph, state) for state in subsets(order, size))
    )
    partition = clique_partition(graph)
    theta = len(partition)
    kernels = {}
    for size in (1, 2, 3):
        kernels[size] = kernel(graph, size)
    gamma_infinity = next(
        size for size in (1, 2, 3) if kernels[size][0]
    )
    family, ranks, waves = kernels[3]

    u, x, p, q, r, b, c = (NAMES[name] for name in NAMES)
    T = frozenset({x, p, q})
    B = frozenset({u, p, q})
    required_edges = {
        frozenset(edge)
        for edge in (
            (u, x), (u, r), (p, r), (q, r), (p, b), (q, c),
            (x, b), (x, c), (b, c), (u, p), (u, q),
        )
    }
    required_nonedges = {
        frozenset(edge)
        for edge in (
            (x, p), (x, q), (p, q), (x, r),
            (b, u), (b, r), (b, q),
            (c, u), (c, r), (c, p),
        )
    }

    def has_edge(edge) -> bool:
        left, right = tuple(edge)
        return right in graph[left]

    if not all(has_edge(edge) for edge in required_edges):
        raise AssertionError("missing a required collision edge")
    if any(has_edge(edge) for edge in required_nonedges):
        raise AssertionError("present required collision nonedge")
    if not independent(graph, T) or T not in family:
        raise AssertionError("T is not a retained independent triple")
    if not dominates(graph, B) or ranks.get(B) != 1:
        raise AssertionError("B does not have literal rank one")

    successors = []
    for guard in sorted(B & graph[r]):
        successor = B - {guard} | {r}
        successors.append(
            {
                "guard": guard,
                "state": sorted(successor),
                "dominates": dominates(graph, successor),
                "rank": ranks.get(successor, 0),
            }
        )
    if [row["guard"] for row in successors] != [u, p, q]:
        raise AssertionError("wrong QQ1 mover set")
    if any(row["dominates"] or row["rank"] != 0 for row in successors):
        raise AssertionError("a deleting successor is not rank zero")

    completions = []
    for third in range(order):
        source = frozenset({u, b, third})
        target = frozenset({x, b, third})
        if len(source) == 3 and independent(graph, source):
            completions.append(
                {
                    "third": third,
                    "source_retained": source in family,
                    "forward_retained": target in family,
                }
            )
    if not completions or not all(
        row["source_retained"] and row["forward_retained"]
        for row in completions
    ):
        raise AssertionError("u->x activity failed on an independent completion")
    if B in family:
        raise AssertionError("the reverse x->u endpoint unexpectedly survives")

    dominating_pairs = [
        sorted(state) for state in subsets(order, 2) if dominates(graph, state)
    ]
    common_ux_nonneighbors = [
        vertex
        for vertex in range(order)
        if vertex not in (u, x)
        and vertex not in graph[u]
        and vertex not in graph[x]
    ]
    repair_square = None
    if label == "dominating-ux":
        if [u, x] not in dominating_pairs or common_ux_nonneighbors:
            raise AssertionError("the first control must have dominating {u,x}")
        boundary = "gamma=2<alpha=gamma_infinity=3; {u,x} dominates"
    elif label == "nondominating-ux":
        if [u, x] in dominating_pairs or common_ux_nonneighbors != [10]:
            raise AssertionError("the second control must have unique ux witness 10")
        if len(dominating_pairs) != 23:
            raise AssertionError("the second control must have 23 other dominating pairs")
        w = common_ux_nonneighbors[0]
        t_completions = [
            vertex
            for vertex in range(order)
            if vertex not in (u, w)
            and vertex not in graph[u]
            and vertex not in graph[w]
        ]
        z_completions = [
            vertex
            for vertex in range(order)
            if vertex not in (x, w)
            and vertex not in graph[x]
            and vertex not in graph[w]
        ]
        if t_completions != [c] or z_completions != [13]:
            raise AssertionError("wrong unique repair-square completions")
        t = t_completions[0]
        z = z_completions[0]
        square_edges = ((u, x), (x, t), (t, z), (z, u))
        square_nonedges = ((u, t), (x, z))
        if not all(right in graph[left] for left, right in square_edges):
            raise AssertionError("missing repair-square cycle edge")
        if any(right in graph[left] for left, right in square_nonedges):
            raise AssertionError("present repair-square diagonal")
        if any(
            endpoint in graph[w]
            for endpoint in (u, x, t, z)
        ):
            raise AssertionError("repair-square pivot is not independent")
        square_states = {
            "S": frozenset({u, w, t}),
            "T": frozenset({x, w, z}),
            "D": frozenset({x, w, t}),
            "O": frozenset({u, w, z}),
            "R": frozenset({u, x, w}),
            "P": frozenset({t, z, w}),
        }
        expected_membership = {
            "S": True,
            "T": True,
            "D": True,
            "O": False,
            "R": True,
            "P": True,
        }
        if {
            name: state in family for name, state in square_states.items()
        } != expected_membership:
            raise AssertionError("wrong repair-square family membership")
        if ranks.get(square_states["O"]) != 3:
            raise AssertionError("the omitted repair corner must have rank three")
        repair_square = {
            "w": w,
            "t": t,
            "z": z,
            "cycle": [u, x, t, z, u],
            "states": {
                name: {
                    "vertices": sorted(state),
                    "retained": state in family,
                    "rank": (
                        "stable"
                        if state in family
                        else ranks.get(state, 0)
                    ),
                }
                for name, state in square_states.items()
            },
            "orientations": {
                "u_to_x": True,
                "x_to_u": False,
                "z_to_t": True,
                "t_to_z": False,
            },
        }
        boundary = (
            "gamma=2<alpha=gamma_infinity=3; {u,x} is nondominating "
            "but 23 other pairs dominate"
        )
    else:
        raise AssertionError(label)

    return {
        "label": label,
        "status": "VERIFIED",
        "graph6": record,
        "graph6_sha256": hashlib.sha256(record.encode("ascii")).hexdigest(),
        "edge_list_sha256": graph_digest(graph),
        "order": order,
        "size": sum(map(len, graph)) // 2,
        "parameters": {
            "gamma": gamma,
            "i": independent_domination,
            "alpha": alpha,
            "gamma_infinity": gamma_infinity,
            "theta": theta,
        },
        "minimum_clique_partition": partition,
        "greatest_triple_family_size": len(family),
        "triple_deletion_wave_sizes": waves,
        "triple_positive_rank_histogram": {
            str(key): value
            for key, value in sorted(Counter(ranks.values()).items())
        },
        "collision": {
            "labels": NAMES,
            "T": sorted(T),
            "B": sorted(B),
            "B_rank": ranks[B],
            "deleting_attack": r,
            "successors": successors,
            "active_u_to_x_completions": completions,
            "reverse_x_to_u_survives": B in family,
        },
        "dominating_pairs": dominating_pairs,
        "common_ux_nonneighbors": common_ux_nonneighbors,
        "repair_square": repair_square,
        "sharp_boundary": boundary,
    }


def evaluate():
    return {
        "schema": "rank-one-QQ1-collision-controls-v1",
        "status": "VERIFIED",
        "controls": {
            label: evaluate_record(label, record)
            for label, record in CONTROLS.items()
        },
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
