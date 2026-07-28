#!/usr/bin/env python3
"""Standalone exact replay of the MMV-027 trapped-escape control.

This file imports no campaign search, transition, parameter, or certificate
code.  Graphs are adjacency frozensets and guard configurations are sorted
tuples.  Every game kernel and parameter used by NOTE.md is recomputed from
the one-guard definition.
"""

from __future__ import annotations

import hashlib
import itertools
import json


GRAPH6 = "JEhbtnm~D]_"
S = (0, 5, 6)
X = 8
U, V, T = 6, 0, 5
Q, R, W, Y = 2, 10, 3, 1


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    require(record and 0 <= ord(record[0]) - 63 <= 62, "short graph6 only")
    order = ord(record[0]) - 63
    payload = []
    for character in record[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, "invalid graph6 character")
        payload.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    require(len(payload) == ((needed + 5) // 6) * 6, "payload length")
    require(not any(payload[needed:]), "nonzero graph6 padding")
    adjacency = [set() for _ in range(order)]
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if payload[cursor]:
                adjacency[low].add(high)
                adjacency[high].add(low)
            cursor += 1
    graph = tuple(frozenset(row) for row in adjacency)
    require(
        all(vertex not in graph[vertex] for vertex in range(order)),
        "loop",
    )
    require(
        all(
            (second in graph[first]) == (first in graph[second])
            for first in range(order)
            for second in range(order)
        ),
        "asymmetry",
    )
    return graph


def states(order: int, size: int):
    yield from itertools.combinations(range(order), size)


def dominates(graph, state) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(graph[guard])
    return len(covered) == len(graph)


def missed(graph, state) -> tuple[int, ...]:
    covered = set(state)
    for guard in state:
        covered.update(graph[guard])
    return tuple(vertex for vertex in range(len(graph)) if vertex not in covered)


def independent(graph, state) -> bool:
    state_set = set(state)
    return all(not (graph[vertex] & state_set) for vertex in state)


def successors(graph, state, attacked):
    require(attacked not in state, ("occupied attack", state, attacked))
    state_set = set(state)
    return tuple(
        (
            guard,
            tuple(sorted((state_set - {guard}) | {attacked})),
        )
        for guard in state
        if attacked in graph[guard]
    )


def greatest_kernel(graph, size: int, banned=frozenset()):
    active = {
        state
        for state in states(len(graph), size)
        if state not in banned and dominates(graph, state)
    }
    ranks = {}
    rounds = []
    rank = 0
    while True:
        deleted = set()
        for state in active:
            for attacked in range(len(graph)):
                if attacked in state:
                    continue
                if not any(
                    successor in active
                    for _, successor in successors(graph, state, attacked)
                ):
                    deleted.add(state)
                    break
        if not deleted:
            return frozenset(active), ranks, tuple(rounds)
        for state in deleted:
            ranks[state] = rank
        rounds.append(len(deleted))
        active.difference_update(deleted)
        rank += 1


def deletion_witnesses(graph, state, banned, ranks):
    require(state in ranks, ("state has no finite rank", state))
    rank = ranks[state]
    answers = []
    for attacked in range(len(graph)):
        if attacked in state:
            continue
        allowed = tuple(
            successor
            for _, successor in successors(graph, state, attacked)
            if successor not in banned and dominates(graph, successor)
        )
        if all(
            successor in ranks and ranks[successor] < rank
            for successor in allowed
        ):
            answers.append(attacked)
    return tuple(answers)


def exact_gamma(graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, state) for state in states(len(graph), size)):
            return size
    raise AssertionError("no dominating set")


def exact_alpha(graph) -> int:
    for size in range(len(graph), 0, -1):
        if any(independent(graph, state) for state in states(len(graph), size)):
            return size
    return 0


def exact_i(graph) -> int:
    for size in range(1, len(graph) + 1):
        for state in states(len(graph), size):
            if independent(graph, state) and dominates(graph, state):
                return size
    raise AssertionError("no maximal independent set")


def exact_eternal_number(graph) -> int:
    for size in range(1, len(graph) + 1):
        kernel, _, _ = greatest_kernel(graph, size)
        if kernel:
            return size
    raise AssertionError("no eternal family")


def complement(graph):
    universe = set(range(len(graph)))
    return tuple(
        frozenset(universe - {vertex} - set(graph[vertex]))
        for vertex in range(len(graph))
    )


def colorable(graph, color_count: int) -> bool:
    colors = [-1] * len(graph)

    def visit(done: int) -> bool:
        if done == len(graph):
            return True
        uncolored = [
            vertex for vertex, color in enumerate(colors) if color < 0
        ]
        vertex = max(
            uncolored,
            key=lambda item: (
                len(
                    {
                        colors[neighbor]
                        for neighbor in graph[item]
                        if colors[neighbor] >= 0
                    }
                ),
                len(graph[item]),
            ),
        )
        forbidden = {
            colors[neighbor]
            for neighbor in graph[vertex]
            if colors[neighbor] >= 0
        }
        for color in range(color_count):
            if color in forbidden:
                continue
            colors[vertex] = color
            if visit(done + 1):
                return True
            colors[vertex] = -1
        return False

    return visit(0)


def exact_chromatic(graph) -> int:
    for count in range(1, len(graph) + 1):
        if colorable(graph, count):
            return count
    raise AssertionError("no coloring")


def complement_neighbors(graph, vertex) -> frozenset[int]:
    return frozenset(
        other
        for other in range(len(graph))
        if other != vertex and other not in graph[vertex]
    )


def color_ban(graph, root, target, color):
    fixed = set(root) - {color}
    return frozenset(
        tuple(sorted(fixed | {terminal}))
        for terminal in complement_neighbors(graph, target)
    )


def palette(graph, greatest, root, vertex):
    return tuple(
        color
        for color in root
        if vertex in graph[color]
        and tuple(sorted((set(root) - {color}) | {vertex})) in greatest
    )


def responder_set(graph, state, attacked):
    return tuple(
        guard for guard in state if attacked in graph[guard]
    )


def parameters(graph):
    return {
        "gamma": exact_gamma(graph),
        "i": exact_i(graph),
        "alpha": exact_alpha(graph),
        "gamma_infinity": exact_eternal_number(graph),
        "theta": exact_chromatic(complement(graph)),
    }


def main() -> None:
    graph = decode_graph6(GRAPH6)
    greatest, _, unrestricted_rounds = greatest_kernel(graph, 3)
    require(S in greatest, "root absent")
    require(independent(graph, S), "root not independent")
    require(palette(graph, greatest, S, X) == S, "target not full")

    B = complement_neighbors(graph, X)
    require(B == frozenset((3, 7, 9, 10)), ("wrong B", B))
    require(R in B and W in B and Q not in B and Y not in B, "B placement")

    source_predecessor = tuple(sorted((V, T, Q)))
    source_terminal = tuple(sorted((V, T, R)))
    secondary_root = tuple(sorted((U, T, R)))
    first_alternate = tuple(sorted((T, Q, R)))
    trapped_endpoint = tuple(sorted((U, T, W)))
    witness_q = tuple(sorted((W, T, Q)))
    witness_r = tuple(sorted((W, T, R)))
    full_source = tuple(sorted((V, T, X)))
    middle = tuple(sorted((W, T, X)))
    second_alternate = tuple(sorted((V, Q, R)))
    escape = tuple(sorted((V, T, Y)))

    for state in (
        source_predecessor,
        source_terminal,
        secondary_root,
        trapped_endpoint,
        witness_q,
        witness_r,
        full_source,
        middle,
        escape,
    ):
        require(state in greatest, ("retained state absent", state))

    require(missed(graph, first_alternate) == (W,), "first witness")
    require(missed(graph, second_alternate) == (Y,), "second witness")
    require(not dominates(graph, first_alternate), "first alternate dominates")
    require(not dominates(graph, second_alternate), "second alternate dominates")

    expected_palettes = {
        Q: (5, 6),
        R: (0, 5, 6),
        W: (0, 6),
        Y: (5, 6),
    }
    actual_palettes = {
        vertex: palette(graph, greatest, S, vertex)
        for vertex in expected_palettes
    }
    require(actual_palettes == expected_palettes, actual_palettes)

    edge_checks = {
        "tr": R in graph[T],
        "ty": Y in graph[T],
        "xy": Y in graph[X],
        "uy": Y in graph[U],
        "xw_nonedge": W not in graph[X],
        "xr_nonedge": R not in graph[X],
        "wr_nonedge": R not in graph[W],
        "wv": V in graph[W],
    }
    require(all(edge_checks.values()), edge_checks)

    require(
        responder_set(graph, full_source, W) == (V,),
        "full-source attack at w not unique",
    )
    require(
        successors(graph, full_source, W)[0][1] == middle,
        "wrong middle endpoint",
    )
    middle_responders = responder_set(graph, middle, Y)
    require(set(middle_responders) == {W, T, X}, middle_responders)
    middle_endpoints = {
        guard: endpoint
        for guard, endpoint in successors(graph, middle, Y)
    }
    require(
        missed(graph, middle_endpoints[T]) == (R,),
        "t->y endpoint should miss r",
    )
    require(
        middle_endpoints[X] not in greatest
        and missed(graph, middle_endpoints[X]) == (4,),
        "control should omit the x->y branch",
    )
    require(
        middle_endpoints[W] in greatest,
        "w->y escape predecessor absent",
    )
    require(
        responder_set(graph, middle_endpoints[W], V) == (X,),
        "w->y branch return not unique",
    )
    require(
        successors(graph, middle_endpoints[W], V)[0][1] == escape,
        "wrong w->y branch escape",
    )

    kernel_data = {}
    for color in S:
        banned = color_ban(graph, S, X, color)
        kernel, ranks, rounds = greatest_kernel(graph, 3, banned)
        kernel_data[color] = {
            "kernel_size": len(kernel),
            "round_sizes": list(rounds),
            "source_rank": ranks.get(source_predecessor),
            "escape_rank": ranks.get(escape),
            "trapped_endpoint_banned": trapped_endpoint in banned,
        }
        require(not kernel, ("restricted kernel survives", color))

    require(
        kernel_data
        == {
            0: {
                "kernel_size": 0,
                "round_sizes": [27, 28, 32, 27, 4],
                "source_rank": 1,
                "escape_rank": 2,
                "trapped_endpoint_banned": True,
            },
            5: {
                "kernel_size": 0,
                "round_sizes": [18, 17, 29, 50, 5],
                "source_rank": 3,
                "escape_rank": 2,
                "trapped_endpoint_banned": False,
            },
            6: {
                "kernel_size": 0,
                "round_sizes": [15, 28, 48, 27, 1],
                "source_rank": 0,
                "escape_rank": 0,
                "trapped_endpoint_banned": False,
            },
        },
        kernel_data,
    )
    source_ban = color_ban(graph, S, X, U)
    _, source_ranks, _ = greatest_kernel(graph, 3, source_ban)
    require(
        R in deletion_witnesses(
            graph, source_predecessor, source_ban, source_ranks
        ),
        "r is not a source deletion witness",
    )

    dominating_pairs = [
        list(state)
        for state in states(len(graph), 2)
        if dominates(graph, state)
    ]
    result = {
        "schema": "full-list-cross-ban-rank-control-v1",
        "model": (
            "unoccupied attacks; exactly one occupied guard moves along "
            "one G-edge; every retained successor remains in the family"
        ),
        "graph6": GRAPH6,
        "graph6_sha256": hashlib.sha256(GRAPH6.encode("ascii")).hexdigest(),
        "order": len(graph),
        "size": sum(map(len, graph)) // 2,
        "parameters": parameters(graph),
        "greatest_family_size": len(greatest),
        "unrestricted_deletion_rounds": list(unrestricted_rounds),
        "root": list(S),
        "target": X,
        "B": sorted(B),
        "row": {
            "source_color": U,
            "secondary_color": V,
            "third_color": T,
            "mover": Q,
            "terminal": R,
            "first_witness": W,
            "second_witness": Y,
            "source_predecessor": list(source_predecessor),
            "trapped_endpoint": list(trapped_endpoint),
            "escape": list(escape),
        },
        "palettes": {
            str(vertex): list(colors)
            for vertex, colors in actual_palettes.items()
        },
        "edge_checks": edge_checks,
        "restricted": {
            str(color): data for color, data in kernel_data.items()
        },
        "dominating_pairs": dominating_pairs,
        "scope": (
            "exact boundary control; gamma=2, so not a gamma-theta "
            "counterexample and not a strict-rank theorem"
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
