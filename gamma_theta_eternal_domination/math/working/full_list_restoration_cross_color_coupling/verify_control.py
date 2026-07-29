#!/usr/bin/env python3
"""Independent replay of the restoration-ladder equality control.

This implementation imports no campaign code.  Graphs and guard states are
integer masks, and every parameter, family, restricted rank, restoration
row, ladder, completion fan, and completion rank is recomputed.
"""

from __future__ import annotations

import hashlib
import itertools
import json


GRAPH6 = "OYifur}UO]}iTij]tpo]v"
ROOT = (0, 1, 10)
TARGET = 6


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def bits(mask: int):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def state(*vertices: int) -> int:
    return sum(1 << vertex for vertex in vertices)


def state_list(mask: int) -> list[int]:
    return list(bits(mask))


def states(n: int, k: int) -> tuple[int, ...]:
    return tuple(state(*choice) for choice in itertools.combinations(range(n), k))


def decode_graph6(record: str) -> tuple[int, ...]:
    n = ord(record[0]) - 63
    require(0 <= n <= 62, "short graph6")
    payload = []
    for character in record[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, "graph6 character")
        payload.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    require(len(payload) == ((needed + 5) // 6) * 6, "graph6 length")
    require(not any(payload[needed:]), "graph6 padding")
    graph = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if payload[cursor]:
                graph[low] |= 1 << high
                graph[high] |= 1 << low
            cursor += 1
    return tuple(graph)


def dominates(graph: tuple[int, ...], guards: int) -> bool:
    covered = guards
    for guard in bits(guards):
        covered |= graph[guard]
    return covered == (1 << len(graph)) - 1


def independent(graph: tuple[int, ...], chosen: int) -> bool:
    return all(not (graph[vertex] & chosen) for vertex in bits(chosen))


def successors(
    graph: tuple[int, ...], guards: int, attacked: int
) -> tuple[int, ...]:
    require(not guards & (1 << attacked), ("occupied attack", guards, attacked))
    return tuple(
        (guards ^ (1 << guard)) | (1 << attacked)
        for guard in bits(guards)
        if graph[guard] & (1 << attacked)
    )


def greatest_kernel(
    graph: tuple[int, ...], k: int, banned: frozenset[int] = frozenset()
) -> tuple[frozenset[int], dict[int, int], tuple[int, ...]]:
    active = {
        guards
        for guards in states(len(graph), k)
        if guards not in banned and dominates(graph, guards)
    }
    ranks: dict[int, int] = {}
    rounds = []
    rank = 0
    while True:
        deleted = set()
        for guards in active:
            for attacked in range(len(graph)):
                if guards & (1 << attacked):
                    continue
                if not any(
                    endpoint in active
                    for endpoint in successors(graph, guards, attacked)
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


def exact_gamma(graph: tuple[int, ...]) -> int:
    for k in range(1, len(graph) + 1):
        if any(dominates(graph, guards) for guards in states(len(graph), k)):
            return k
    raise AssertionError("gamma")


def exact_i(graph: tuple[int, ...]) -> int:
    for k in range(1, len(graph) + 1):
        if any(
            dominates(graph, guards) and independent(graph, guards)
            for guards in states(len(graph), k)
        ):
            return k
    raise AssertionError("i")


def exact_alpha(graph: tuple[int, ...]) -> int:
    for k in range(len(graph), 0, -1):
        if any(independent(graph, chosen) for chosen in states(len(graph), k)):
            return k
    return 0


def exact_eternal(graph: tuple[int, ...]) -> int:
    for k in range(1, len(graph) + 1):
        kernel, _, _ = greatest_kernel(graph, k)
        if kernel:
            return k
    raise AssertionError("eternal")


def exact_theta(graph: tuple[int, ...]) -> int:
    n = len(graph)
    universe = (1 << n) - 1
    opposite = tuple(universe ^ (1 << vertex) ^ graph[vertex] for vertex in range(n))
    colors = [-1] * n

    def colorable(count: int) -> bool:
        colors[:] = [-1] * n

        def visit(done: int) -> bool:
            if done == n:
                return True
            candidates = [vertex for vertex in range(n) if colors[vertex] < 0]
            vertex = max(
                candidates,
                key=lambda item: (
                    len(
                        {
                            colors[neighbor]
                            for neighbor in bits(opposite[item])
                            if colors[neighbor] >= 0
                        }
                    ),
                    opposite[item].bit_count(),
                ),
            )
            forbidden = {
                colors[neighbor]
                for neighbor in bits(opposite[vertex])
                if colors[neighbor] >= 0
            }
            for color in range(count):
                if color in forbidden:
                    continue
                colors[vertex] = color
                if visit(done + 1):
                    return True
                colors[vertex] = -1
            return False

        return visit(0)

    for count in range(1, n + 1):
        if colorable(count):
            return count
    raise AssertionError("theta")


def complement_neighbors(graph: tuple[int, ...], vertex: int) -> int:
    return ((1 << len(graph)) - 1) ^ (1 << vertex) ^ graph[vertex]


def palette(
    graph: tuple[int, ...], family: frozenset[int], vertex: int
) -> tuple[int, ...]:
    root = state(*ROOT)
    return tuple(
        color
        for color in ROOT
        if graph[color] & (1 << vertex)
        and ((root ^ (1 << color)) | (1 << vertex)) in family
    )


def missed(graph: tuple[int, ...], guards: int) -> tuple[int, ...]:
    covered = guards
    for guard in bits(guards):
        covered |= graph[guard]
    return tuple(vertex for vertex in range(len(graph)) if not covered & (1 << vertex))


def completion(graph: tuple[int, ...], first: int, second: int) -> tuple[int, ...]:
    covered = (1 << first) | (1 << second) | graph[first] | graph[second]
    return tuple(
        vertex
        for vertex in range(len(graph))
        if not covered & (1 << vertex)
    )


def edge_list(graph: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (low, high)
        for high in range(1, len(graph))
        for low in range(high)
        if graph[high] & (1 << low)
    )


def main() -> None:
    graph = decode_graph6(GRAPH6)
    family, _, _ = greatest_kernel(graph, 3)
    root = state(*ROOT)
    require(root in family and independent(graph, root), "root")
    require(palette(graph, family, TARGET) == ROOT, "full target")

    region_mask = complement_neighbors(graph, TARGET)
    region = tuple(bits(region_mask))
    require(region == (5, 7, 9, 11, 13), region)

    restricted = {}
    row_records = []
    witness_count = 0
    root_collisions = 0
    external_witnesses = 0
    noncolliding_completions = 0
    completion_rank_counts: dict[int, int] = {}
    completion_inside_b = 0
    completion_outside_b = 0

    for source in ROOT:
        fixed = root ^ (1 << source)
        banned = frozenset(fixed | (1 << b) for b in region)
        kernel, ranks, rounds = greatest_kernel(graph, 3, banned)
        restricted[str(source)] = {
            "kernel_size": len(kernel),
            "round_sizes": list(rounds),
        }
        if kernel:
            continue

        for predecessor in family:
            if predecessor in banned or ranks.get(predecessor) != 0:
                continue
            for attacked in ROOT:
                if predecessor & (1 << attacked):
                    continue
                for terminal in region:
                    terminal_state = fixed | (1 << terminal)
                    if terminal_state not in family:
                        continue
                    for mover in bits(predecessor & ~terminal_state):
                        if not graph[mover] & (1 << attacked):
                            continue
                        if (
                            (predecessor ^ (1 << mover)) | (1 << attacked)
                            != terminal_state
                        ):
                            continue
                        thirds = [
                            color
                            for color in ROOT
                            if color not in (source, attacked)
                        ]
                        if len(thirds) != 1:
                            continue
                        third = thirds[0]
                        if predecessor != state(terminal, third, mover):
                            continue
                        terminal_palette = palette(graph, family, terminal)
                        if len(terminal_palette) < 2 or attacked not in terminal_palette:
                            continue
                        allowed = [
                            endpoint
                            for endpoint in successors(
                                graph, predecessor, attacked
                            )
                            if endpoint not in banned and dominates(graph, endpoint)
                        ]
                        if allowed:
                            continue
                        alternate = state(attacked, third, mover)
                        if region_mask & (1 << mover) or dominates(graph, alternate):
                            continue

                        witnesses = missed(graph, alternate)
                        require(witnesses, "nondominating alternate")
                        row_records.append(
                            {
                                "source": source,
                                "attacked": attacked,
                                "third": third,
                                "terminal": terminal,
                                "mover": mover,
                                "witnesses": list(witnesses),
                            }
                        )

                        for witness in witnesses:
                            witness_count += 1
                            P = state(witness, third, mover)
                            Z = state(witness, third, attacked)
                            require(
                                successors(graph, predecessor, witness) == (P,),
                                ("first ladder", predecessor, witness),
                            )
                            require(P in family, "first ladder endpoint")
                            require(
                                successors(graph, P, attacked) == (Z,),
                                ("second ladder", P, attacked),
                            )
                            require(Z in family, "second ladder endpoint")

                            if witness == source:
                                root_collisions += 1
                                require(Z == root, "root collision")
                            else:
                                external_witnesses += 1
                                require(
                                    palette(graph, family, witness) == (source,),
                                    ("singleton palette", source, witness),
                                )

                            fan = completion(graph, witness, mover)
                            require(fan, "completion fan empty")
                            require(
                                all(
                                    graph[left] & (1 << right)
                                    for index, left in enumerate(fan)
                                    for right in fan[index + 1 :]
                                ),
                                ("completion fan not clique", witness, mover, fan),
                            )
                            for completion_vertex in fan:
                                if completion_vertex == third:
                                    continue
                                endpoint = state(witness, mover, completion_vertex)
                                require(
                                    successors(graph, P, completion_vertex)
                                    == (endpoint,),
                                    ("completion exchange", P, completion_vertex),
                                )
                                require(endpoint in family, "completion omitted")
                                endpoint_rank = ranks.get(endpoint)
                                require(endpoint_rank == 3, ("completion rank", endpoint_rank))
                                noncolliding_completions += 1
                                completion_rank_counts[endpoint_rank] = (
                                    completion_rank_counts.get(endpoint_rank, 0) + 1
                                )
                                if region_mask & (1 << completion_vertex):
                                    completion_inside_b += 1
                                else:
                                    completion_outside_b += 1

    require(
        restricted
        == {
            "0": {"kernel_size": 0, "round_sizes": [28, 81, 132, 62]},
            "1": {"kernel_size": 150, "round_sizes": [31, 74, 49]},
            "10": {"kernel_size": 0, "round_sizes": [32, 81, 128, 62]},
        },
        restricted,
    )
    require(len(row_records) == 12, ("rows", len(row_records)))
    require(witness_count == 19, witness_count)
    require(root_collisions == 12, root_collisions)
    require(external_witnesses == 7, external_witnesses)
    require(noncolliding_completions == 19, noncolliding_completions)
    require(completion_rank_counts == {3: 19}, completion_rank_counts)
    require(completion_inside_b == 8, completion_inside_b)
    require(completion_outside_b == 11, completion_outside_b)

    parameters = {
        "gamma": exact_gamma(graph),
        "i": exact_i(graph),
        "alpha": exact_alpha(graph),
        "gamma_infinity": exact_eternal(graph),
        "theta": exact_theta(graph),
    }
    require(
        parameters
        == {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        },
        parameters,
    )
    edges = edge_list(graph)
    serialized_edges = "".join(f"{a}-{b}\n" for a, b in edges).encode("ascii")
    result = {
        "schema": "full-list-restoration-cross-color-control-v1",
        "graph6": GRAPH6,
        "graph6_sha256": hashlib.sha256(GRAPH6.encode("ascii")).hexdigest(),
        "edge_list_sha256": hashlib.sha256(serialized_edges).hexdigest(),
        "order": len(graph),
        "size": len(edges),
        "parameters": parameters,
        "greatest_family_size": len(family),
        "root": list(ROOT),
        "target": TARGET,
        "B": list(region),
        "restricted": restricted,
        "outside_B_restoration_rows": len(row_records),
        "witness_incidences": witness_count,
        "root_collisions": root_collisions,
        "external_singleton_palette_witnesses": external_witnesses,
        "noncolliding_completions": noncolliding_completions,
        "completion_rank_counts": {
            str(rank): count for rank, count in completion_rank_counts.items()
        },
        "completion_vertices_inside_B": completion_inside_b,
        "completion_vertices_outside_B": completion_outside_b,
        "rows": row_records,
        "scope": "exact equality control; not a conjecture counterexample",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
