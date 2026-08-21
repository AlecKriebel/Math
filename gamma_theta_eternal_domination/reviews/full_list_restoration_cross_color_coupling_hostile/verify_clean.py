#!/usr/bin/env python3
"""Clean-room audit of the C-177 restoration-rebound control.

This program deliberately does not import campaign code.  In contrast with
the candidate's integer-mask transition engine, graph neighborhoods and guard
configurations are represented by Python ``frozenset`` objects, and legal
one-guard moves are constructed directly as set exchanges.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Iterable


GRAPH6 = "OYifur}UO]}iTij]tpo]v"
ROOT = frozenset((0, 1, 10))
TARGET = 6


def insist(condition: bool, detail: object) -> None:
    if not condition:
        raise AssertionError(detail)


def decode_graph6(text: str) -> tuple[frozenset[int], ...]:
    """Decode a short graph6 record into adjacency sets."""

    insist(text and ord(text[0]) < 126, "only short graph6 is used")
    order = ord(text[0]) - 63
    insist(0 <= order <= 62, ("order", order))
    raw_bits: list[int] = []
    for symbol in text[1:]:
        value = ord(symbol) - 63
        insist(0 <= value < 64, ("symbol", symbol))
        raw_bits.extend((value >> shift) & 1 for shift in (5, 4, 3, 2, 1, 0))
    needed = order * (order - 1) // 2
    insist(len(raw_bits) == ((needed + 5) // 6) * 6, "payload length")
    insist(all(bit == 0 for bit in raw_bits[needed:]), "nonzero padding")

    adjacency = [set() for _ in range(order)]
    cursor = 0
    for later in range(1, order):
        for earlier in range(later):
            if raw_bits[cursor]:
                adjacency[earlier].add(later)
                adjacency[later].add(earlier)
            cursor += 1
    return tuple(frozenset(neighbors) for neighbors in adjacency)


def configurations(vertices: Iterable[int], size: int) -> tuple[frozenset[int], ...]:
    return tuple(frozenset(choice) for choice in itertools.combinations(vertices, size))


def is_independent(graph: tuple[frozenset[int], ...], chosen: frozenset[int]) -> bool:
    return all(graph[vertex].isdisjoint(chosen) for vertex in chosen)


def dominates(graph: tuple[frozenset[int], ...], guards: frozenset[int]) -> bool:
    covered = set(guards)
    for guard in guards:
        covered.update(graph[guard])
    return len(covered) == len(graph)


def legal_moves(
    graph: tuple[frozenset[int], ...],
    guards: frozenset[int],
    attacked: int,
) -> tuple[frozenset[int], ...]:
    insist(attacked not in guards, ("occupied attack", sorted(guards), attacked))
    endpoints = []
    for guard in sorted(guards):
        if attacked in graph[guard]:
            endpoints.append((guards - {guard}) | {attacked})
    return tuple(endpoints)


def peel(
    graph: tuple[frozenset[int], ...],
    size: int,
    banned: frozenset[frozenset[int]] = frozenset(),
) -> tuple[
    frozenset[frozenset[int]],
    dict[frozenset[int], int],
    tuple[int, ...],
]:
    """Greatest fixed point and synchronous deletion ranks."""

    universe = {
        guards
        for guards in configurations(range(len(graph)), size)
        if guards not in banned and dominates(graph, guards)
    }
    active = set(universe)
    ranks: dict[frozenset[int], int] = {}
    round_sizes: list[int] = []
    round_index = 0
    while True:
        removed: set[frozenset[int]] = set()
        for guards in active:
            for attacked in set(range(len(graph))) - guards:
                if not any(
                    endpoint in active
                    for endpoint in legal_moves(graph, guards, attacked)
                ):
                    removed.add(guards)
                    break
        if not removed:
            return frozenset(active), ranks, tuple(round_sizes)
        for guards in removed:
            ranks[guards] = round_index
        active.difference_update(removed)
        round_sizes.append(len(removed))
        round_index += 1


def gamma(graph: tuple[frozenset[int], ...]) -> int:
    vertices = range(len(graph))
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, chosen) for chosen in configurations(vertices, size)):
            return size
    raise AssertionError("gamma")


def independent_domination(graph: tuple[frozenset[int], ...]) -> int:
    vertices = range(len(graph))
    for size in range(1, len(graph) + 1):
        if any(
            is_independent(graph, chosen) and dominates(graph, chosen)
            for chosen in configurations(vertices, size)
        ):
            return size
    raise AssertionError("independent domination")


def alpha(graph: tuple[frozenset[int], ...]) -> int:
    vertices = range(len(graph))
    for size in range(len(graph), 0, -1):
        if any(is_independent(graph, chosen) for chosen in configurations(vertices, size)):
            return size
    return 0


def eternal_number(graph: tuple[frozenset[int], ...]) -> int:
    for size in range(1, len(graph) + 1):
        family, _, _ = peel(graph, size)
        if family:
            return size
    raise AssertionError("eternal number")


def clique_cover_number(graph: tuple[frozenset[int], ...]) -> int:
    """Exact clique partition by direct recursive clique assignment."""

    order = len(graph)
    vertices = tuple(range(order))

    def coverable(number_of_parts: int) -> bool:
        parts: list[list[int]] = [[] for _ in range(number_of_parts)]

        def place(position: int) -> bool:
            if position == order:
                return True
            vertex = vertices[position]
            used_empty = False
            for part in parts:
                if not part:
                    if used_empty:
                        continue
                    used_empty = True
                if all(member in graph[vertex] for member in part):
                    part.append(vertex)
                    if place(position + 1):
                        return True
                    part.pop()
            return False

        return place(0)

    for count in range(1, order + 1):
        if coverable(count):
            return count
    raise AssertionError("clique cover")


def missed_vertices(
    graph: tuple[frozenset[int], ...], guards: frozenset[int]
) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(graph))
        if vertex not in guards and all(vertex not in graph[guard] for guard in guards)
    )


def completion_fan(
    graph: tuple[frozenset[int], ...], first: int, second: int
) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(graph))
        if vertex not in (first, second)
        and vertex not in graph[first]
        and vertex not in graph[second]
    )


def root_palette(
    graph: tuple[frozenset[int], ...],
    family: frozenset[frozenset[int]],
    vertex: int,
) -> tuple[int, ...]:
    palette = []
    for color in sorted(ROOT):
        swap = (ROOT - {color}) | {vertex}
        if vertex in graph[color] and swap in family:
            palette.append(color)
    return tuple(palette)


def johnson_distance(
    state: frozenset[int], banned: frozenset[frozenset[int]]
) -> int:
    return min(len(state - target) for target in banned)


def state_status(
    state: frozenset[int],
    kernel: frozenset[frozenset[int]],
    ranks: dict[frozenset[int], int],
) -> str:
    if state in kernel:
        return "kernel"
    return f"rank-{ranks[state]}"


def edge_hash(graph: tuple[frozenset[int], ...]) -> tuple[int, str]:
    edges = [
        (earlier, later)
        for later in range(len(graph))
        for earlier in range(later)
        if earlier in graph[later]
    ]
    encoded = "".join(f"{earlier}-{later}\n" for earlier, later in edges).encode()
    return len(edges), hashlib.sha256(encoded).hexdigest()


def audit_control() -> dict[str, object]:
    graph = decode_graph6(GRAPH6)
    vertices = frozenset(range(len(graph)))
    family, unrestricted_ranks, unrestricted_rounds = peel(graph, 3)
    insist(not unrestricted_ranks or unrestricted_rounds, "unrestricted peel")
    insist(ROOT in family and is_independent(graph, ROOT), "independent retained root")

    target_palette = root_palette(graph, family, TARGET)
    insist(target_palette == tuple(sorted(ROOT)), ("target palette", target_palette))
    region = frozenset(vertices - {TARGET} - graph[TARGET])
    insist(region == frozenset((5, 7, 9, 11, 13)), ("B", sorted(region)))

    restricted: dict[int, tuple[
        frozenset[frozenset[int]],
        dict[frozenset[int], int],
        tuple[int, ...],
        frozenset[frozenset[int]],
    ]] = {}
    for source in sorted(ROOT):
        fixed = ROOT - {source}
        banned = frozenset(fixed | {b} for b in region)
        kernel, ranks, rounds = peel(graph, 3, banned)
        restricted[source] = (kernel, ranks, rounds, banned)

    rows: list[dict[str, object]] = []
    witness_count = 0
    collision_count = 0
    external_count = 0
    cross_positive_finite = 0
    cross_positive_kernel = 0
    completion_count = 0
    completion_rank_counts: dict[int, int] = {}
    completion_inside = 0
    completion_outside = 0
    distance_counts: dict[int, int] = {}
    reverse_attack_response_counts: dict[int, int] = {}
    third_mover_edge_count = 0
    third_mover_nonedge_count = 0

    for source in sorted(ROOT):
        kernel, ranks, _, banned = restricted[source]
        if kernel:
            continue
        fixed = ROOT - {source}
        for predecessor in sorted(family, key=lambda item: tuple(sorted(item))):
            if predecessor in banned or ranks.get(predecessor) != 0:
                continue
            for attacked in sorted(fixed):
                if attacked in predecessor:
                    continue
                third_set = fixed - {attacked}
                insist(len(third_set) == 1, ("third anchor", fixed, attacked))
                third = next(iter(third_set))
                physical = legal_moves(graph, predecessor, attacked)
                initial_unbanned = tuple(
                    endpoint
                    for endpoint in physical
                    if endpoint not in banned and dominates(graph, endpoint)
                )
                if initial_unbanned:
                    continue

                for terminal in sorted(region):
                    banned_endpoint = fixed | {terminal}
                    if banned_endpoint not in family or banned_endpoint not in physical:
                        continue
                    terminal_palette = root_palette(graph, family, terminal)
                    if attacked not in terminal_palette or len(terminal_palette) < 2:
                        continue
                    removed = predecessor - banned_endpoint
                    if len(removed) != 1:
                        continue
                    mover = next(iter(removed))
                    if predecessor != frozenset((terminal, third, mover)):
                        continue
                    alternate = frozenset((attacked, third, mover))
                    if alternate not in physical:
                        continue
                    if mover in region or dominates(graph, alternate):
                        continue

                    # Exact local restoration row.  There are two physical
                    # responders: mover -> attacked and terminal -> attacked.
                    insist(
                        set(physical) == {banned_endpoint, alternate},
                        ("physical restoration responses", predecessor, attacked, physical),
                    )
                    insist(mover not in region, ("mover unexpectedly in B", mover))

                    witnesses = missed_vertices(graph, alternate)
                    insist(witnesses, ("nondominating alternate", alternate))
                    rows.append(
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
                        insist(witness not in region, ("p in B", source, witness))
                        first = frozenset((witness, third, mover))
                        rebound = frozenset((witness, third, attacked))

                        insist(
                            legal_moves(graph, predecessor, witness) == (first,),
                            ("first ladder not physically unique", predecessor, witness),
                        )
                        insist(first in family, ("first ladder omitted", first))
                        insist(
                            legal_moves(graph, first, attacked) == (rebound,),
                            ("second ladder not physically unique", first, attacked),
                        )
                        insist(rebound in family, ("rebound omitted", rebound))

                        # The reverse attack at the mover always has the
                        # attacked-anchor response back to ``first``.  It has
                        # a second physical response exactly when the
                        # deliberately unconstrained third--mover edge is
                        # present.  Never use this reverse attack as a
                        # uniqueness claim.
                        reverse_moves = legal_moves(graph, rebound, mover)
                        insist(first in reverse_moves, ("missing reverse response", rebound))
                        reverse_attack_response_counts[len(reverse_moves)] = (
                            reverse_attack_response_counts.get(len(reverse_moves), 0) + 1
                        )
                        if mover in graph[third]:
                            third_mover_edge_count += 1
                            insist(
                                len(reverse_moves) == 2,
                                ("unconstrained edge response count", reverse_moves),
                            )
                        else:
                            third_mover_nonedge_count += 1
                            insist(
                                len(reverse_moves) == 1,
                                ("unconstrained nonedge response count", reverse_moves),
                            )

                        if witness == source:
                            collision_count += 1
                            insist(rebound == ROOT, ("collision endpoint", rebound))
                        else:
                            external_count += 1
                            insist(
                                root_palette(graph, family, witness) == (source,),
                                ("external palette", source, witness),
                            )

                        # Recompute both cross-color barriers, including the
                        # case in which the state lies in a recipient kernel.
                        for recipient in sorted(fixed):
                            recipient_kernel, recipient_ranks, _, recipient_ban = (
                                restricted[recipient]
                            )
                            insist(rebound not in recipient_ban, ("cross banned", rebound))
                            if rebound in recipient_kernel:
                                cross_positive_kernel += 1
                            else:
                                insist(
                                    recipient_ranks.get(rebound, -1) >= 1,
                                    ("cross rank zero", recipient, rebound),
                                )
                                cross_positive_finite += 1

                        fan = completion_fan(graph, witness, mover)
                        insist(fan, ("empty completion fan", witness, mover))
                        insist(
                            all(
                                right in graph[left]
                                for index, left in enumerate(fan)
                                for right in fan[index + 1 :]
                            ),
                            ("completion not a clique", witness, mover, fan),
                        )
                        insist(
                            all(
                                vertex == third or vertex in graph[third]
                                for vertex in fan
                            ),
                            ("completion outside closed N[third]", third, fan),
                        )

                        for completion in fan:
                            if completion == third:
                                continue
                            independent_endpoint = frozenset((witness, mover, completion))
                            insist(
                                legal_moves(graph, first, completion)
                                == (independent_endpoint,),
                                (
                                    "completion exchange not physically unique",
                                    first,
                                    completion,
                                ),
                            )
                            insist(
                                independent_endpoint in family,
                                ("completion endpoint omitted", independent_endpoint),
                            )
                            distance = johnson_distance(independent_endpoint, banned)
                            distance_counts[distance] = distance_counts.get(distance, 0) + 1
                            if independent_endpoint in kernel:
                                endpoint_rank = None
                            else:
                                endpoint_rank = ranks[independent_endpoint]
                                insist(
                                    endpoint_rank >= 2,
                                    (
                                        "immediate rank-one recurrence",
                                        independent_endpoint,
                                        endpoint_rank,
                                    ),
                                )
                                completion_rank_counts[endpoint_rank] = (
                                    completion_rank_counts.get(endpoint_rank, 0) + 1
                                )
                            completion_count += 1
                            if completion in region:
                                completion_inside += 1
                                insist(distance == 2, ("inside-B distance", distance))
                            else:
                                completion_outside += 1
                                insist(distance == 3, ("outside-B distance", distance))

    rows.sort(
        key=lambda row: (
            row["source"],
            row["attacked"],
            row["terminal"],
            row["mover"],
            row["witnesses"],
        )
    )
    size, sorted_edge_hash = edge_hash(graph)
    parameter_vector = {
        "gamma": gamma(graph),
        "i": independent_domination(graph),
        "alpha": alpha(graph),
        "gamma_infinity": eternal_number(graph),
        "theta": clique_cover_number(graph),
    }
    insist(
        parameter_vector
        == {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        },
        ("parameters", parameter_vector),
    )
    return {
        "schema": "full-list-restoration-cross-color-hostile-clean-v1",
        "candidate_commit": "e2e8809d",
        "graph6": GRAPH6,
        "graph6_sha256": hashlib.sha256(GRAPH6.encode()).hexdigest(),
        "order": len(graph),
        "size": size,
        "edge_list_sha256": sorted_edge_hash,
        "parameters": parameter_vector,
        "greatest_family_size": len(family),
        "root": sorted(ROOT),
        "target": TARGET,
        "B": sorted(region),
        "restricted": {
            str(source): {
                "kernel_size": len(restricted[source][0]),
                "round_sizes": list(restricted[source][2]),
            }
            for source in sorted(ROOT)
        },
        "local_restoration_rows": len(rows),
        "witness_incidences": witness_count,
        "root_collisions": collision_count,
        "external_singleton_palettes": external_count,
        "cross_color_positive_finite_checks": cross_positive_finite,
        "cross_color_kernel_checks": cross_positive_kernel,
        "reverse_attack_response_counts": {
            str(count): reverse_attack_response_counts[count]
            for count in sorted(reverse_attack_response_counts)
        },
        "third_mover_edge_witnesses": third_mover_edge_count,
        "third_mover_nonedge_witnesses": third_mover_nonedge_count,
        "noncolliding_completions": completion_count,
        "completion_rank_counts": {
            str(rank): completion_rank_counts[rank]
            for rank in sorted(completion_rank_counts)
        },
        "completion_distance_counts": {
            str(distance): distance_counts[distance]
            for distance in sorted(distance_counts)
        },
        "completion_vertices_inside_B": completion_inside,
        "completion_vertices_outside_B": completion_outside,
        "rows": rows,
        "verdict": "PASS",
        "scope": "local restoration control only; no C-176 ancestry asserted",
    }


if __name__ == "__main__":
    print(json.dumps(audit_control(), sort_keys=True, separators=(",", ":")))
