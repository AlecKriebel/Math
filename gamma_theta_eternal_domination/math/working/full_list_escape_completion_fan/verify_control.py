#!/usr/bin/env python3
"""Standalone replay of the separated completion-fan boundary control.

This verifier imports no campaign search or transition code.  Graphs are
tuples of frozenset neighborhoods and guard states are sorted tuples.  All
parameters, greatest families, restricted kernels, ranks, attacks, and
completion sets used by NOTE.md are recomputed from the definitions.
"""

from __future__ import annotations

import hashlib
import itertools
import json


GRAPH6 = "LEhbtnm~D]xln{"
S = (0, 5, 6)
X = 8
U, V, T = 6, 0, 5
Q, R, W, Y = 2, 10, 3, 1
D, E = 11, 12


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    require(record and 0 <= ord(record[0]) - 63 <= 62, "short graph6 only")
    order = ord(record[0]) - 63
    payload: list[int] = []
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


def encode_graph6(graph: tuple[frozenset[int], ...]) -> str:
    order = len(graph)
    require(order <= 62, "short graph6 only")
    bits = [
        int(low in graph[high])
        for high in range(1, order)
        for low in range(high)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = "".join(
        chr(
            63
            + sum(
                bits[offset + bit] << (5 - bit)
                for bit in range(6)
            )
        )
        for offset in range(0, len(bits), 6)
    )
    return chr(63 + order) + payload


def states(order: int, size: int):
    yield from itertools.combinations(range(order), size)


def state(*vertices: int) -> tuple[int, ...]:
    return tuple(sorted(vertices))


def dominates(graph, guards) -> bool:
    covered = set(guards)
    for guard in guards:
        covered.update(graph[guard])
    return len(covered) == len(graph)


def missed(graph, guards) -> tuple[int, ...]:
    covered = set(guards)
    for guard in guards:
        covered.update(graph[guard])
    return tuple(
        vertex for vertex in range(len(graph)) if vertex not in covered
    )


def independent(graph, vertices) -> bool:
    chosen = set(vertices)
    return all(not (graph[vertex] & chosen) for vertex in vertices)


def successors(graph, guards, attacked):
    require(attacked not in guards, ("occupied attack", guards, attacked))
    chosen = set(guards)
    return tuple(
        (
            guard,
            tuple(sorted((chosen - {guard}) | {attacked})),
        )
        for guard in guards
        if attacked in graph[guard]
    )


def responders(graph, guards, attacked) -> tuple[int, ...]:
    return tuple(guard for guard in guards if attacked in graph[guard])


def greatest_kernel(graph, size: int, banned=frozenset()):
    active = {
        guards
        for guards in states(len(graph), size)
        if guards not in banned and dominates(graph, guards)
    }
    ranks: dict[tuple[int, ...], int] = {}
    rounds: list[int] = []
    rank = 0
    while True:
        deleted = set()
        for guards in active:
            for attacked in range(len(graph)):
                if attacked in guards:
                    continue
                if not any(
                    endpoint in active
                    for _, endpoint in successors(graph, guards, attacked)
                ):
                    deleted.add(guards)
                    break
        if not deleted:
            return frozenset(active), ranks, tuple(rounds)
        for guards in deleted:
            ranks[guards] = rank
        rounds.append(len(deleted))
        active.difference_update(deleted)
        rank += 1


def deletion_witnesses(graph, guards, banned, ranks):
    require(guards in ranks, ("state has no finite rank", guards))
    rank = ranks[guards]
    result = []
    for attacked in range(len(graph)):
        if attacked in guards:
            continue
        allowed = tuple(
            endpoint
            for _, endpoint in successors(graph, guards, attacked)
            if endpoint not in banned and dominates(graph, endpoint)
        )
        if all(
            endpoint in ranks and ranks[endpoint] < rank
            for endpoint in allowed
        ):
            result.append(attacked)
    return tuple(result)


def exact_gamma(graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, guards) for guards in states(len(graph), size)):
            return size
    raise AssertionError("no dominating set")


def exact_i(graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(
            independent(graph, guards) and dominates(graph, guards)
            for guards in states(len(graph), size)
        ):
            return size
    raise AssertionError("no maximal independent set")


def exact_alpha(graph) -> int:
    for size in range(len(graph), 0, -1):
        if any(independent(graph, chosen) for chosen in states(len(graph), size)):
            return size
    return 0


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


def exact_theta(graph) -> int:
    opposite = complement(graph)
    for count in range(1, len(graph) + 1):
        if colorable(opposite, count):
            return count
    raise AssertionError("no complement coloring")


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


def pair_missed_set(graph, first: int, second: int) -> tuple[int, ...]:
    covered = {first, second} | set(graph[first]) | set(graph[second])
    return tuple(
        vertex for vertex in range(len(graph)) if vertex not in covered
    )


def edge_list(graph) -> tuple[tuple[int, int], ...]:
    return tuple(
        (low, high)
        for high in range(1, len(graph))
        for low in range(high)
        if low in graph[high]
    )


def main() -> None:
    graph = decode_graph6(GRAPH6)
    require(encode_graph6(graph) == GRAPH6, "graph6 round trip")
    greatest, _, unrestricted_rounds = greatest_kernel(graph, 3)

    source = state(V, T, Q)
    terminal = state(V, T, R)
    secondary_root = state(U, T, R)
    first_alternate = state(T, Q, R)
    witness_q = state(W, T, Q)
    witness_r = state(W, T, R)
    second_alternate = state(V, Q, R)
    escape = state(V, T, Y)
    second_source = state(V, R, Y)
    first_completion = state(Q, W, D)
    second_completion = state(R, Y, E)

    require(independent(graph, S), "root not independent")
    require(S in greatest, "root absent")
    require(palette(graph, greatest, S, X) == S, "target not full")
    for guards in (
        source,
        terminal,
        secondary_root,
        witness_q,
        witness_r,
        escape,
        second_source,
        first_completion,
        second_completion,
    ):
        require(guards in greatest, ("retained state absent", guards))

    require(missed(graph, first_alternate) == (W,), "first witness")
    require(missed(graph, second_alternate) == (Y,), "second witness")
    require(
        responders(graph, terminal, Y) == (T,),
        "terminal-to-second-source response not unique",
    )
    require(
        successors(graph, terminal, Y)[0][1] == second_source,
        "wrong second-source endpoint",
    )

    first_fan = pair_missed_set(graph, Q, W)
    second_fan = pair_missed_set(graph, R, Y)
    require(first_fan == (D,), ("first fan", first_fan))
    require(second_fan == (E,), ("second fan", second_fan))
    require(D in graph[T], "first fan not covered by t")
    require(E in graph[V], "second fan not covered by v")
    require(independent(graph, first_completion), "first completion")
    require(independent(graph, second_completion), "second completion")
    require(
        responders(graph, witness_q, D) == (T,),
        "first completion exchange not unique",
    )
    require(
        successors(graph, witness_q, D)[0][1] == first_completion,
        "wrong first completion endpoint",
    )
    require(
        responders(graph, second_source, E) == (V,),
        "second completion exchange not unique",
    )
    require(
        successors(graph, second_source, E)[0][1] == second_completion,
        "wrong second completion endpoint",
    )

    require(Y in graph[W], "control is not the separated wy-edge branch")
    require(T in graph[Q], "control is not the external first-fan branch")
    require(set(first_fan).isdisjoint(second_fan), "fans overlap")

    B = complement_neighbors(graph, X)
    require(B == frozenset((3, 7, 9, 10)), ("wrong B", B))
    restricted = {}
    for color in S:
        banned = color_ban(graph, S, X, color)
        kernel, ranks, rounds = greatest_kernel(graph, 3, banned)
        restricted[color] = {
            "kernel_size": len(kernel),
            "round_sizes": list(rounds),
            "source_rank": ranks.get(source),
            "escape_rank": ranks.get(escape),
            "first_completion_rank": ranks.get(first_completion),
            "second_completion_rank": ranks.get(second_completion),
        }
    require(
        restricted
        == {
            0: {
                "kernel_size": 0,
                "round_sizes": [27, 49, 74, 46],
                "source_rank": 1,
                "escape_rank": 2,
                "first_completion_rank": 3,
                "second_completion_rank": 2,
            },
            5: {
                "kernel_size": 0,
                "round_sizes": [20, 30, 53, 74, 20],
                "source_rank": 3,
                "escape_rank": 2,
                "first_completion_rank": 3,
                "second_completion_rank": 4,
            },
            6: {
                "kernel_size": 0,
                "round_sizes": [20, 53, 90, 34],
                "source_rank": 0,
                "escape_rank": 0,
                "first_completion_rank": 2,
                "second_completion_rank": 2,
            },
        },
        restricted,
    )
    source_ban = color_ban(graph, S, X, U)
    _, source_ranks, _ = greatest_kernel(graph, 3, source_ban)
    require(
        deletion_witnesses(graph, source, source_ban, source_ranks) == (R,),
        "wrong source deletion witness",
    )
    require(
        deletion_witnesses(graph, escape, source_ban, source_ranks) == (W,),
        "wrong escape deletion witness",
    )

    pairs = tuple(
        guards
        for guards in states(len(graph), 2)
        if dominates(graph, guards)
    )
    require(
        pairs == ((0, 8), (5, 12), (6, 10), (11, 12)),
        ("dominating pairs", pairs),
    )

    edges = edge_list(graph)
    serialized_edges = "".join(f"{a}-{b}\n" for a, b in edges).encode("ascii")
    parameters = {
        "gamma": exact_gamma(graph),
        "i": exact_i(graph),
        "alpha": exact_alpha(graph),
        "gamma_infinity": exact_eternal_number(graph),
        "theta": exact_theta(graph),
    }
    require(
        parameters
        == {
            "gamma": 2,
            "i": 2,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 4,
        },
        parameters,
    )

    result = {
        "schema": "full-list-escape-completion-fan-control-v1",
        "model": (
            "unoccupied attacks; exactly one occupied guard moves along "
            "one G-edge; every retained successor stays in the family"
        ),
        "graph6": GRAPH6,
        "graph6_sha256": hashlib.sha256(GRAPH6.encode("ascii")).hexdigest(),
        "order": len(graph),
        "size": len(edges),
        "edge_list_sha256": hashlib.sha256(serialized_edges).hexdigest(),
        "parameters": parameters,
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
            "trapped_witness": W,
            "escape_vertex": Y,
            "source": list(source),
            "escape": list(escape),
        },
        "completion_fans": {
            "q_w": list(first_fan),
            "r_y": list(second_fan),
            "first_state": list(first_completion),
            "second_state": list(second_completion),
            "first_unique_responder": T,
            "second_unique_responder": V,
            "wy_edge": Y in graph[W],
            "qt_edge": T in graph[Q],
            "disjoint": set(first_fan).isdisjoint(second_fan),
        },
        "restricted": {
            str(color): data for color, data in restricted.items()
        },
        "dominating_pairs": [list(pair) for pair in pairs],
        "new_vertex_neighbors": {
            str(D): sorted(graph[D]),
            str(E): sorted(graph[E]),
        },
        "scope": (
            "exact gamma-two boundary; not an equality graph and not a "
            "gamma-theta counterexample"
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
