#!/usr/bin/env python3
"""Clean-room hostile replay for the MMV-027 trapped-witness control.

This verifier deliberately uses integer masks throughout.  It imports no
campaign evaluator, search routine, or candidate verifier.  The eternal
families are recomputed literally from the one-guard definition by
synchronous greatest-fixed-point deletion.
"""

from __future__ import annotations

import hashlib
import itertools
import json


GRAPH6 = "JEhbtnm~D]_"
ROOT = (0, 5, 6)
TARGET = 8
SOURCE = 6
SECONDARY = 0
THIRD = 5
MOVER = 2
TERMINAL = 10
FIRST_WITNESS = 3
SECOND_WITNESS = 1


def check(condition: bool, label: object) -> None:
    if not condition:
        raise AssertionError(label)


def decode_short_graph6(text: str) -> tuple[int, ...]:
    check(text and text[0] != "~", "only short graph6 is accepted")
    order = ord(text[0]) - 63
    check(0 <= order <= 62, "bad graph6 order")
    encoded = []
    for char in text[1:]:
        value = ord(char) - 63
        check(0 <= value < 64, ("bad graph6 character", char))
        for place in (5, 4, 3, 2, 1, 0):
            encoded.append((value >> place) & 1)
    required = order * (order - 1) // 2
    check(len(encoded) == 6 * ((required + 5) // 6), "wrong payload length")
    check(all(bit == 0 for bit in encoded[required:]), "nonzero padding")

    adjacency = [0] * order
    cursor = 0
    for later in range(1, order):
        for earlier in range(later):
            if encoded[cursor]:
                adjacency[earlier] |= 1 << later
                adjacency[later] |= 1 << earlier
            cursor += 1
    for vertex, neighbors in enumerate(adjacency):
        check(not (neighbors & (1 << vertex)), "loop")
        for other in range(order):
            check(
                bool(neighbors & (1 << other))
                == bool(adjacency[other] & (1 << vertex)),
                "asymmetric graph",
            )
    return tuple(adjacency)


def mask(vertices) -> int:
    answer = 0
    for vertex in vertices:
        answer |= 1 << vertex
    return answer


def unpack(state: int, order: int) -> list[int]:
    return [vertex for vertex in range(order) if state & (1 << vertex)]


def fixed_size_masks(order: int, size: int):
    for vertices in itertools.combinations(range(order), size):
        yield mask(vertices)


def closed_coverage(adjacency: tuple[int, ...], state: int) -> int:
    covered = state
    rest = state
    while rest:
        bit = rest & -rest
        vertex = bit.bit_length() - 1
        covered |= adjacency[vertex]
        rest ^= bit
    return covered


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    return closed_coverage(adjacency, state) == (1 << len(adjacency)) - 1


def missed(adjacency: tuple[int, ...], state: int) -> list[int]:
    omitted = ((1 << len(adjacency)) - 1) ^ closed_coverage(adjacency, state)
    return unpack(omitted, len(adjacency))


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    rest = state
    while rest:
        bit = rest & -rest
        vertex = bit.bit_length() - 1
        if adjacency[vertex] & (state ^ bit):
            return False
        rest ^= bit
    return True


def move_responses(
    adjacency: tuple[int, ...], state: int, attacked: int
) -> list[tuple[int, int]]:
    attack_bit = 1 << attacked
    check(not (state & attack_bit), ("occupied attack", unpack(state, len(adjacency)), attacked))
    answers = []
    rest = state
    while rest:
        guard_bit = rest & -rest
        guard = guard_bit.bit_length() - 1
        if adjacency[guard] & attack_bit:
            answers.append((guard, (state ^ guard_bit) | attack_bit))
        rest ^= guard_bit
    return answers


def literal_kernel(
    adjacency: tuple[int, ...],
    guard_count: int,
    forbidden: frozenset[int] = frozenset(),
) -> tuple[frozenset[int], dict[int, int], list[int], int]:
    active = {
        state
        for state in fixed_size_masks(len(adjacency), guard_count)
        if state not in forbidden and dominates(adjacency, state)
    }
    initial_size = len(active)
    deletion_rank: dict[int, int] = {}
    round_sizes = []
    rank = 0
    while True:
        doomed = set()
        snapshot = frozenset(active)
        for state in snapshot:
            for attacked in range(len(adjacency)):
                if state & (1 << attacked):
                    continue
                if not any(
                    successor in snapshot
                    for _, successor in move_responses(adjacency, state, attacked)
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return frozenset(active), deletion_rank, round_sizes, initial_size
        for state in doomed:
            deletion_rank[state] = rank
        round_sizes.append(len(doomed))
        active.difference_update(doomed)
        rank += 1


def complement_adjacency(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    all_vertices = (1 << len(adjacency)) - 1
    return tuple(
        all_vertices ^ (1 << vertex) ^ adjacency[vertex]
        for vertex in range(len(adjacency))
    )


def exact_chromatic(adjacency: tuple[int, ...]) -> tuple[int, list[int]]:
    order = len(adjacency)

    def try_colors(limit: int) -> list[int] | None:
        colors = [-1] * order

        def search(colored_count: int) -> bool:
            if colored_count == order:
                return True
            remaining = [v for v in range(order) if colors[v] < 0]
            vertex = max(
                remaining,
                key=lambda v: (
                    len(
                        {
                            colors[w]
                            for w in range(order)
                            if adjacency[v] & (1 << w) and colors[w] >= 0
                        }
                    ),
                    (adjacency[v] & sum(1 << w for w in remaining)).bit_count(),
                    adjacency[v].bit_count(),
                    -v,
                ),
            )
            blocked = {
                colors[w]
                for w in range(order)
                if adjacency[vertex] & (1 << w) and colors[w] >= 0
            }
            for color in range(limit):
                if color in blocked:
                    continue
                colors[vertex] = color
                if search(colored_count + 1):
                    return True
                colors[vertex] = -1
            return False

        return list(colors) if search(0) else None

    for number in range(1, order + 1):
        coloring = try_colors(number)
        if coloring is not None:
            return number, coloring
    raise AssertionError("chromatic search failed")


def exact_parameters(adjacency: tuple[int, ...]) -> tuple[dict[str, int], dict[int, int]]:
    order = len(adjacency)
    gamma = next(
        size
        for size in range(1, order + 1)
        if any(dominates(adjacency, state) for state in fixed_size_masks(order, size))
    )
    alpha = next(
        size
        for size in range(order, 0, -1)
        if any(independent(adjacency, state) for state in fixed_size_masks(order, size))
    )
    independent_domination = next(
        size
        for size in range(1, order + 1)
        if any(
            independent(adjacency, state) and dominates(adjacency, state)
            for state in fixed_size_masks(order, size)
        )
    )
    eternal_sizes = {}
    eternal = None
    for size in range(1, order + 1):
        kernel, _, _, _ = literal_kernel(adjacency, size)
        eternal_sizes[size] = len(kernel)
        if kernel:
            eternal = size
            break
    check(eternal is not None, "no eternal number")
    theta, coloring = exact_chromatic(complement_adjacency(adjacency))
    return (
        {
            "gamma": gamma,
            "i": independent_domination,
            "alpha": alpha,
            "gamma_infinity": eternal,
            "theta": theta,
        },
        {"kernel_1": eternal_sizes.get(1, -1), "kernel_2": eternal_sizes.get(2, -1), "kernel_3": eternal_sizes.get(3, -1), "theta_coloring": coloring},
    )


def complement_neighbors(adjacency: tuple[int, ...], vertex: int) -> set[int]:
    return {
        other
        for other in range(len(adjacency))
        if other != vertex and not (adjacency[vertex] & (1 << other))
    }


def root_palette(
    adjacency: tuple[int, ...], greatest: frozenset[int], root: tuple[int, ...], vertex: int
) -> list[int]:
    root_mask = mask(root)
    return [
        color
        for color in root
        if adjacency[color] & (1 << vertex)
        and ((root_mask ^ (1 << color)) | (1 << vertex)) in greatest
    ]


def color_ban(
    adjacency: tuple[int, ...], root: tuple[int, ...], target: int, color: int
) -> frozenset[int]:
    base = mask(root) ^ (1 << color)
    return frozenset(
        base | (1 << terminal)
        for terminal in complement_neighbors(adjacency, target)
    )


def state(*vertices: int) -> int:
    return mask(vertices)


def deletion_attacks(
    adjacency: tuple[int, ...],
    current: int,
    forbidden: frozenset[int],
    ranks: dict[int, int],
) -> list[int]:
    current_rank = ranks[current]
    witnesses = []
    for attacked in range(len(adjacency)):
        if current & (1 << attacked):
            continue
        usable = [
            successor
            for _, successor in move_responses(adjacency, current, attacked)
            if successor not in forbidden and dominates(adjacency, successor)
        ]
        if all(
            successor in ranks and ranks[successor] < current_rank
            for successor in usable
        ):
            witnesses.append(attacked)
    return witnesses


def main() -> None:
    graph = decode_short_graph6(GRAPH6)
    order = len(graph)
    check(order == 11, "order")
    graph_size = sum(neighbors.bit_count() for neighbors in graph) // 2
    check(graph_size == 34, "size")

    parameters, auxiliary_parameters = exact_parameters(graph)
    check(
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

    greatest, _, unrestricted_rounds, unrestricted_initial = literal_kernel(graph, 3)
    check(len(greatest) == 122, "greatest-family size")
    check(unrestricted_rounds == [], "greatest family should already be closed")
    check(unrestricted_initial == 122, "dominating triples versus kernel")

    root = state(*ROOT)
    check(root in greatest and independent(graph, root), "root")
    check(root_palette(graph, greatest, ROOT, TARGET) == list(ROOT), "full target")
    banned_vertices = complement_neighbors(graph, TARGET)
    check(banned_vertices == {3, 7, 9, 10}, banned_vertices)

    named = {
        "source_predecessor": state(SECONDARY, THIRD, MOVER),
        "source_terminal": state(SECONDARY, THIRD, TERMINAL),
        "secondary_root": state(SOURCE, THIRD, TERMINAL),
        "first_alternate": state(THIRD, MOVER, TERMINAL),
        "trapped_endpoint": state(SOURCE, THIRD, FIRST_WITNESS),
        "witness_q": state(FIRST_WITNESS, THIRD, MOVER),
        "witness_r": state(FIRST_WITNESS, THIRD, TERMINAL),
        "full_source": state(SECONDARY, THIRD, TARGET),
        "middle": state(FIRST_WITNESS, THIRD, TARGET),
        "second_alternate": state(SECONDARY, MOVER, TERMINAL),
        "escape": state(SECONDARY, THIRD, SECOND_WITNESS),
    }
    retained_names = (
        "source_predecessor",
        "source_terminal",
        "secondary_root",
        "trapped_endpoint",
        "witness_q",
        "witness_r",
        "full_source",
        "middle",
        "escape",
    )
    check(all(named[name] in greatest for name in retained_names), "retained states")
    check(missed(graph, named["first_alternate"]) == [FIRST_WITNESS], "first missed set")
    check(missed(graph, named["second_alternate"]) == [SECOND_WITNESS], "second missed set")

    palettes = {
        str(vertex): root_palette(graph, greatest, ROOT, vertex)
        for vertex in (MOVER, TERMINAL, FIRST_WITNESS, SECOND_WITNESS)
    }
    check(
        palettes
        == {
            "2": [5, 6],
            "10": [0, 5, 6],
            "3": [0, 6],
            "1": [5, 6],
        },
        palettes,
    )

    def responders(label: str, attack: int) -> list[int]:
        return [guard for guard, _ in move_responses(graph, named[label], attack)]

    def endpoint(label: str, attack: int, guard: int) -> int:
        options = dict(move_responses(graph, named[label], attack))
        check(guard in options, ("missing move", label, attack, guard))
        return options[guard]

    check(responders("source_predecessor", FIRST_WITNESS) == [SECONDARY], "T attack w")
    check(
        endpoint("source_predecessor", FIRST_WITNESS, SECONDARY) == named["witness_q"],
        "T->w endpoint",
    )
    check(responders("secondary_root", FIRST_WITNESS) == [SOURCE], "F_v attack w")
    check(
        endpoint("secondary_root", FIRST_WITNESS, SOURCE) == named["witness_r"],
        "F_v->w endpoint",
    )
    check(responders("full_source", FIRST_WITNESS) == [SECONDARY], "X_u attack w")
    check(
        endpoint("full_source", FIRST_WITNESS, SECONDARY) == named["middle"],
        "X_u->w endpoint",
    )
    check(
        responders("source_predecessor", TERMINAL) == [SECONDARY, MOVER, THIRD],
        "T attack r responders",
    )
    terminal_endpoints = {
        guard: endpoint("source_predecessor", TERMINAL, guard)
        for guard in responders("source_predecessor", TERMINAL)
    }
    check(terminal_endpoints[MOVER] == named["source_terminal"], "selected terminal")
    check(terminal_endpoints[SECONDARY] == named["first_alternate"], "first alternate")
    check(terminal_endpoints[THIRD] == named["second_alternate"], "second alternate")

    check(responders("full_source", TERMINAL) == [SECONDARY, THIRD], "X_u attack r")
    xu_r_endpoints = {
        guard: endpoint("full_source", TERMINAL, guard)
        for guard in responders("full_source", TERMINAL)
    }
    check(missed(graph, xu_r_endpoints[SECONDARY]) == [FIRST_WITNESS], "v->r misses w")
    # In the theorem's counterfactual y lies in B, so the t->r endpoint
    # would miss y.  In this sharp control xy is an edge, as the theorem
    # concludes, and that endpoint is allowed to dominate.
    check(dominates(graph, xu_r_endpoints[THIRD]), "t->r control endpoint")

    check(
        responders("middle", SECOND_WITNESS) == [FIRST_WITNESS, THIRD, TARGET],
        "M attack y responders",
    )
    middle_endpoints = {
        guard: endpoint("middle", SECOND_WITNESS, guard)
        for guard in responders("middle", SECOND_WITNESS)
    }
    check(missed(graph, middle_endpoints[THIRD]) == [TERMINAL], "t->y misses r")
    check(middle_endpoints[FIRST_WITNESS] in greatest, "w->y retained")
    check(responders_for_state(graph, middle_endpoints[FIRST_WITNESS], SECONDARY) == [TARGET], "return at v")
    check(
        dict(move_responses(graph, middle_endpoints[FIRST_WITNESS], SECONDARY))[TARGET]
        == named["escape"],
        "return endpoint",
    )

    edge_audit = {
        "tr": bool(graph[THIRD] & (1 << TERMINAL)),
        "ty": bool(graph[THIRD] & (1 << SECOND_WITNESS)),
        "uy": bool(graph[SOURCE] & (1 << SECOND_WITNESS)),
        "xy": bool(graph[TARGET] & (1 << SECOND_WITNESS)),
        "wv": bool(graph[FIRST_WITNESS] & (1 << SECONDARY)),
        "wu": bool(graph[FIRST_WITNESS] & (1 << SOURCE)),
        "wt_nonedge": not bool(graph[FIRST_WITNESS] & (1 << THIRD)),
        "wq_nonedge": not bool(graph[FIRST_WITNESS] & (1 << MOVER)),
        "wr_nonedge": not bool(graph[FIRST_WITNESS] & (1 << TERMINAL)),
        "xw_nonedge": not bool(graph[TARGET] & (1 << FIRST_WITNESS)),
        "xr_nonedge": not bool(graph[TARGET] & (1 << TERMINAL)),
        "yv_nonedge": not bool(graph[SECOND_WITNESS] & (1 << SECONDARY)),
        "yq_nonedge": not bool(graph[SECOND_WITNESS] & (1 << MOVER)),
        "yr_nonedge": not bool(graph[SECOND_WITNESS] & (1 << TERMINAL)),
    }
    check(all(edge_audit.values()), edge_audit)
    collision_vertices = {
        SOURCE,
        SECONDARY,
        THIRD,
        TARGET,
        MOVER,
        TERMINAL,
        FIRST_WITNESS,
        SECOND_WITNESS,
    }
    check(len(collision_vertices) == 8, "named collision")

    restricted = {}
    expected_rounds = {
        0: [27, 28, 32, 27, 4],
        5: [18, 17, 29, 50, 5],
        6: [15, 28, 48, 27, 1],
    }
    expected_source_ranks = {0: 1, 5: 3, 6: 0}
    expected_escape_ranks = {0: 2, 5: 2, 6: 0}
    source_forbidden = None
    source_ranks = None
    for color in ROOT:
        forbidden = color_ban(graph, ROOT, TARGET, color)
        kernel, ranks, rounds, initial_size = literal_kernel(graph, 3, forbidden)
        check(not kernel, ("surviving restricted kernel", color))
        check(rounds == expected_rounds[color], ("rounds", color, rounds))
        check(ranks[named["source_predecessor"]] == expected_source_ranks[color], "source rank")
        check(ranks[named["escape"]] == expected_escape_ranks[color], "escape rank")
        restricted[str(color)] = {
            "initial_universe_size": initial_size,
            "kernel_size": len(kernel),
            "round_sizes": rounds,
            "source_rank": ranks[named["source_predecessor"]],
            "escape_rank": ranks[named["escape"]],
            "trapped_endpoint_banned": named["trapped_endpoint"] in forbidden,
        }
        if color == SOURCE:
            source_forbidden = forbidden
            source_ranks = ranks
    check(source_forbidden is not None and source_ranks is not None, "source peeling")
    check(source_ranks[named["source_predecessor"]] == 0, "rank-zero semantics")
    check(
        TERMINAL
        in deletion_attacks(
            graph, named["source_predecessor"], source_forbidden, source_ranks
        ),
        "terminal is not a deletion attack",
    )
    source_terminal_successors = {
        guard: {
            "state": unpack(successor, order),
            "banned": successor in source_forbidden,
            "dominates": dominates(graph, successor),
        }
        for guard, successor in move_responses(
            graph, named["source_predecessor"], TERMINAL
        )
    }
    check(
        source_terminal_successors
        == {
            0: {"state": [2, 5, 10], "banned": False, "dominates": False},
            2: {"state": [0, 5, 10], "banned": True, "dominates": True},
            5: {"state": [0, 2, 10], "banned": False, "dominates": False},
        },
        source_terminal_successors,
    )

    dominating_pairs = [
        unpack(candidate, order)
        for candidate in fixed_size_masks(order, 2)
        if dominates(graph, candidate)
    ]
    check(
        dominating_pairs
        == [[0, 8], [1, 10], [2, 3], [2, 9], [6, 9], [6, 10]],
        dominating_pairs,
    )

    first_witness_set = missed(graph, named["first_alternate"])
    second_witness_set = missed(graph, named["second_alternate"])
    check(set(first_witness_set) & banned_vertices == {FIRST_WITNESS}, "first witness in B")
    check(not (set(second_witness_set) & banned_vertices), "second witness outside B")

    result = {
        "schema": "full-list-cross-ban-rank-hostile-review-v1",
        "verdict_target": "MMV-027 exact control and rank semantics",
        "graph6": GRAPH6,
        "graph6_sha256": hashlib.sha256(GRAPH6.encode("ascii")).hexdigest(),
        "order": order,
        "size": graph_size,
        "parameters": parameters,
        "auxiliary_parameters": auxiliary_parameters,
        "greatest_family_size": len(greatest),
        "greatest_family_initial_size": unrestricted_initial,
        "B": sorted(banned_vertices),
        "palettes": palettes,
        "missed_sets": {
            "first_alternate": first_witness_set,
            "second_alternate": second_witness_set,
        },
        "full_terminal_polarization": {
            "first_meets_B": bool(set(first_witness_set) & banned_vertices),
            "second_meets_B": bool(set(second_witness_set) & banned_vertices),
        },
        "edge_audit": edge_audit,
        "restricted": restricted,
        "source_rank_zero_deletion_attack": TERMINAL,
        "source_rank_zero_responses": source_terminal_successors,
        "dominating_pairs": dominating_pairs,
        "rank_shortcut": {
            "source_color": SOURCE,
            "source_rank": source_ranks[named["source_predecessor"]],
            "escape_rank": source_ranks[named["escape"]],
            "strict_drop": False,
        },
        "scope": "gamma=2 boundary control; not an equality graph and not a conjecture counterexample",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


def responders_for_state(
    adjacency: tuple[int, ...], current: int, attacked: int
) -> list[int]:
    return [guard for guard, _ in move_responses(adjacency, current, attacked)]


if __name__ == "__main__":
    main()
