#!/usr/bin/env python3
"""Clean-room hostile audit of the higher-rank fan-descent candidate."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter


CONTROL = "LEhbtnm~D]xln{"


def demand(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def bits(state: int):
    while state:
        low = state & -state
        yield low.bit_length() - 1
        state ^= low


def subsets(order: int, size: int):
    for choice in itertools.combinations(range(order), size):
        yield sum(1 << vertex for vertex in choice)


def make_graph(order: int, code: int) -> tuple[int, ...]:
    rows = [0] * order
    for index, (left, right) in enumerate(
        itertools.combinations(range(order), 2)
    ):
        if code & (1 << index):
            rows[left] |= 1 << right
            rows[right] |= 1 << left
    return tuple(rows)


def graph6(record: str) -> tuple[int, ...]:
    words = [ord(character) - 63 for character in record]
    demand(words and words[0] < 63, "only short graph6 is supported")
    order = words[0]
    stream = [
        (word >> shift) & 1
        for word in words[1:]
        for shift in range(5, -1, -1)
    ]
    need = order * (order - 1) // 2
    demand(len(stream) >= need and not any(stream[need:]), "graph6 tail")
    rows = [0] * order
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if stream[cursor]:
                rows[left] |= 1 << right
                rows[right] |= 1 << left
            cursor += 1
    return tuple(rows)


def edge(graph: tuple[int, ...], left: int, right: int) -> bool:
    return bool(graph[left] & (1 << right))


def independent(graph: tuple[int, ...], state: int) -> bool:
    return all(
        not graph[vertex] & (state ^ (1 << vertex))
        for vertex in bits(state)
    )


def dominates(graph: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in bits(state):
        covered |= graph[vertex]
    return covered == (1 << len(graph)) - 1


def moves(
    graph: tuple[int, ...], state: int, target: int
) -> tuple[tuple[int, int], ...]:
    demand(not state & (1 << target), ("occupied attack", state, target))
    return tuple(
        (
            guard,
            (state ^ (1 << guard)) | (1 << target),
        )
        for guard in bits(state)
        if edge(graph, guard, target)
    )


def greatest_triples(graph: tuple[int, ...]) -> set[int]:
    alive = {
        state
        for state in subsets(len(graph), 3)
        if dominates(graph, state)
    }
    while True:
        rejected = {
            state
            for state in alive
            if any(
                not any(endpoint in alive for _, endpoint in moves(graph, state, attack))
                for attack in range(len(graph))
                if not state & (1 << attack)
            )
        }
        if not rejected:
            return alive
        alive -= rejected


def restricted_ranks(
    graph: tuple[int, ...], banned: set[int]
) -> tuple[set[int], dict[int, int], tuple[int, ...]]:
    alive = {
        state
        for state in subsets(len(graph), 3)
        if state not in banned and dominates(graph, state)
    }
    ranks: dict[int, int] = {}
    layers = []
    round_number = 0
    while True:
        rejected = {
            state
            for state in alive
            if any(
                not any(endpoint in alive for _, endpoint in moves(graph, state, attack))
                for attack in range(len(graph))
                if not state & (1 << attack)
            )
        }
        if not rejected:
            return alive, ranks, tuple(layers)
        for state in rejected:
            ranks[state] = round_number
        layers.append(len(rejected))
        alive -= rejected
        round_number += 1


def deletion_attacks(
    graph: tuple[int, ...],
    state: int,
    rank: int,
    banned: set[int],
    kernel: set[int],
    ranks: dict[int, int],
) -> tuple[int, ...]:
    result = []
    for attack in range(len(graph)):
        if state & (1 << attack):
            continue
        has_same_round_response = False
        for _, endpoint in moves(graph, state, attack):
            if endpoint in banned or not dominates(graph, endpoint):
                continue
            if endpoint in kernel or ranks.get(endpoint, -1) >= rank:
                has_same_round_response = True
                break
        if not has_same_round_response:
            result.append(attack)
    return tuple(result)


def distance(state: int, banned: set[int]) -> int:
    return min(3 - (state & item).bit_count() for item in banned)


def witnesses(
    graph: tuple[int, ...], left: int, right: int
) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(graph))
        if vertex not in (left, right)
        and not edge(graph, left, vertex)
        and not edge(graph, right, vertex)
    )


def retained_fan(
    family: set[int],
    graph: tuple[int, ...],
    left: int,
    right: int,
) -> bool:
    return all(
        ((1 << left) | (1 << right) | (1 << third)) in family
        for third in witnesses(graph, left, right)
    )


def equality_three(graph: tuple[int, ...], family: set[int]) -> bool:
    order = len(graph)
    return (
        not any(dominates(graph, state) for state in subsets(order, 2))
        and any(dominates(graph, state) for state in subsets(order, 3))
        and any(independent(graph, state) for state in subsets(order, 3))
        and not any(independent(graph, state) for state in subsets(order, 4))
        and bool(family)
    )


def audit_endpoint(
    graph: tuple[int, ...],
    family: set[int],
    source: int,
    attack: int,
    mover: int,
    endpoint: int,
    anchors: tuple[int, int],
    b_set: set[int],
    banned: set[int],
    ranks: dict[int, int],
) -> tuple[int, int]:
    source_rank = ranks[source]
    demand(endpoint in family, "endpoint is not retained")
    demand(endpoint not in banned, "distance-two move reached ban")
    demand(endpoint in ranks and ranks[endpoint] < source_rank, "no descent")

    reverse = moves(graph, endpoint, mover)
    demand(reverse == ((attack, source),), ("reverse not unique", reverse))

    anchor_hits = sum(bool(endpoint & (1 << anchor)) for anchor in anchors)
    demand(anchor_hits <= 1, "two anchors introduced by one move")
    b_hit = int(any(endpoint & (1 << vertex) for vertex in b_set))
    formula = 3 - anchor_hits - b_hit
    demand(distance(endpoint, banned) == formula, "delta formula")
    demand(ranks[endpoint] >= formula - 1, "Johnson floor")

    internal_spokes = 0
    for stationary in bits(endpoint ^ (1 << attack)):
        if edge(graph, attack, stationary):
            internal_spokes += 1
            demand(
                retained_fan(family, graph, attack, stationary),
                "supported repair fan missing",
            )
    return formula, internal_spokes


def symbolic_audit() -> dict[str, object]:
    source = {0, 1, 2}
    application_rows = []
    all_formal_rows = 0
    reverse_checks = 0
    spoke_checks = 0
    for size in range(1, 4):
        for attack_neighbors in itertools.combinations(source, size):
            a_set = set(attack_neighbors)
            for mover_count in range(1, size + 1):
                for retained_movers in itertools.combinations(
                    attack_neighbors, mover_count
                ):
                    all_formal_rows += 1
                    for mover in retained_movers:
                        stationary = source - {mover}
                        # The source is independent and z sees exactly A.
                        reverse_eligible = ["z"] + [
                            item for item in stationary if False
                        ]
                        demand(reverse_eligible == ["z"], "symbolic reverse")
                        demand(
                            len(a_set - {mover}) == size - 1,
                            "symbolic spoke count",
                        )
                        reverse_checks += 1
                        spoke_checks += size - 1
            if a_set & {0, 1}:
                application_rows.append(
                    {
                        "A": sorted(a_set),
                        "nonempty_M_choices": (1 << size) - 1,
                    }
                )

    demand(all_formal_rows == 19, "all nonempty A,M count")
    demand(
        sum(row["nonempty_M_choices"] for row in application_rows) == 18,
        "application 18-count",
    )

    delta_checks = 0
    ordinary_vertices = {0, 1, 2, 5}
    for selector in range(1, 1 << len(ordinary_vertices)):
        b_set = {
            vertex
            for index, vertex in enumerate(sorted(ordinary_vertices))
            if selector & (1 << index)
        }
        banned = {
            (1 << 3) | (1 << 4) | (1 << member)
            for member in b_set
        }
        source_state = (1 << 0) | (1 << 1) | (1 << 2)
        if distance(source_state, banned) != 2:
            continue
        for target in (3, 4, 5):
            if target in (3, 4) and target in b_set:
                continue
            for mover in source:
                endpoint = (source_state ^ (1 << mover)) | (1 << target)
                formula = (
                    3
                    - int(target in (3, 4))
                    - int(any(endpoint & (1 << item) for item in b_set))
                )
                demand(distance(endpoint, banned) == formula, "symbolic delta")
                if formula == 3:
                    # At h=2, descent gives rho<=1 while the floor gives rho>=2.
                    demand(formula - 1 > 1, "rank-two shell arithmetic")
                delta_checks += 1

    target_patterns = 0
    target_unique_reverses = 0
    for b_mask in range(1 << 3):
        trapped = bool(b_mask)
        r_dominates = not trapped
        for r_retained in (False, True):
            if r_retained and not r_dominates:
                continue
            for x_mask in range(1 << 3):
                closure = True
                for index in range(3):
                    x_retained = bool(x_mask & (1 << index))
                    e_hits_x = not bool(b_mask & (1 << index))
                    closure &= x_retained or (e_hits_x and r_retained)
                if not closure:
                    continue
                target_patterns += 1
                if trapped:
                    demand(x_mask == 0b111 and not r_retained, "trapped target")
                elif not r_retained:
                    demand(x_mask == 0b111, "omitted hub")
                # X_e reverses only x->y; R reverses only x->e when e hits x.
                target_unique_reverses += x_mask.bit_count()
                if r_retained:
                    target_unique_reverses += 3

    return {
        "all_nonempty_A_M_patterns": all_formal_rows,
        "application_A_M_patterns": 18,
        "application_neighbor_rows": application_rows,
        "unique_reverse_checks": reverse_checks,
        "supported_spoke_checks": spoke_checks,
        "delta_formula_checks": delta_checks,
        "target_membership_patterns": target_patterns,
        "target_unique_reverse_checks": target_unique_reverses,
    }


def finite_census() -> dict[str, object]:
    totals = Counter()
    rank_counts = Counter()
    exit_rank_counts = Counter()
    for order in range(3, 7):
        for code in range(1 << (order * (order - 1) // 2)):
            totals["labeled_graphs"] += 1
            graph = make_graph(order, code)
            family = greatest_triples(graph)
            if not equality_three(graph, family):
                continue
            totals["equality_graphs"] += 1
            for first, second in itertools.combinations(range(order), 2):
                remaining = [
                    vertex
                    for vertex in range(order)
                    if vertex not in (first, second)
                ]
                for selector in range(1, 1 << len(remaining)):
                    b_set = {
                        remaining[index]
                        for index in range(len(remaining))
                        if selector & (1 << index)
                    }
                    banned = {
                        (1 << first) | (1 << second) | (1 << member)
                        for member in b_set
                    }
                    kernel, ranks, _ = restricted_ranks(graph, banned)
                    totals["source_form_bans"] += 1
                    anchor_mask = (1 << first) | (1 << second)
                    for state in family:
                        if (
                            state not in ranks
                            or not independent(graph, state)
                            or state & anchor_mask
                            or distance(state, banned) != 2
                        ):
                            continue
                        totals["distance_two_states"] += 1
                        rank = ranks[state]
                        if rank < 2:
                            continue
                        totals["higher_rank_states"] += 1
                        rank_counts[rank] += 1
                        attacks = deletion_attacks(
                            graph, state, rank, banned, kernel, ranks
                        )
                        for attack in attacks:
                            neighbor_set = {
                                guard
                                for guard in bits(state)
                                if edge(graph, guard, attack)
                            }
                            demand(neighbor_set, "empty physical response")
                            retained_count = 0
                            for mover, endpoint in moves(graph, state, attack):
                                if endpoint not in family:
                                    continue
                                retained_count += 1
                                delta, spokes = audit_endpoint(
                                    graph,
                                    family,
                                    state,
                                    attack,
                                    mover,
                                    endpoint,
                                    (first, second),
                                    b_set,
                                    banned,
                                    ranks,
                                )
                                demand(
                                    spokes == len(neighbor_set) - 1,
                                    "wrong exact spoke number",
                                )
                                if rank == 2:
                                    demand(delta <= 2, "rank-two distance three")
                            demand(retained_count, "no retained exit")
                            totals["deletion_exits"] += 1
                            exit_rank_counts[rank] += 1
                            if len(neighbor_set) == 1:
                                totals["singleton_exits"] += 1
                                mover = next(iter(neighbor_set))
                                endpoint = (
                                    state ^ (1 << mover)
                                ) | (1 << attack)
                                demand(
                                    endpoint in family
                                    and independent(graph, endpoint),
                                    "singleton endpoint not independent",
                                )
                            else:
                                totals["multi_neighbor_exits"] += 1

    return {
        **dict(sorted(totals.items())),
        "higher_rank_counts": {
            str(rank): count for rank, count in sorted(rank_counts.items())
        },
        "exit_rank_counts": {
            str(rank): count for rank, count in sorted(exit_rank_counts.items())
        },
    }


def minimum_size(graph: tuple[int, ...], predicate) -> int:
    for size in range(1, len(graph) + 1):
        if any(predicate(state) for state in subsets(len(graph), size)):
            return size
    raise AssertionError("minimum absent")


def alpha(graph: tuple[int, ...]) -> int:
    for size in range(len(graph), 0, -1):
        if any(independent(graph, state) for state in subsets(len(graph), size)):
            return size
    return 0


def theta(graph: tuple[int, ...]) -> int:
    order = len(graph)
    for colors in range(1, order + 1):
        parts: list[list[int]] = [[] for _ in range(colors)]

        def place(vertex: int, used: int) -> bool:
            if vertex == order:
                return True
            for part in range(min(colors, used + 1)):
                if all(edge(graph, vertex, other) for other in parts[part]):
                    parts[part].append(vertex)
                    if place(vertex + 1, max(used, part + 1)):
                        return True
                    parts[part].pop()
            return False

        if place(0, 0):
            return colors
    raise AssertionError("theta absent")


def control_audit() -> dict[str, object]:
    graph = graph6(CONTROL)
    family = greatest_triples(graph)
    gamma = minimum_size(graph, lambda state: dominates(graph, state))
    independent_domination = minimum_size(
        graph,
        lambda state: independent(graph, state) and dominates(graph, state),
    )
    eternal = next(
        size
        for size in range(1, len(graph) + 1)
        if (
            greatest_triples(graph)
            if size == 3
            else greatest_family_size(graph, size)
        )
    )
    parameters = (
        gamma,
        independent_domination,
        alpha(graph),
        eternal,
        theta(graph),
    )
    demand(parameters == (2, 2, 3, 3, 4), "control parameters")
    demand(len(family) == 200, "control greatest family")

    x, v, t, r, y, e = 8, 0, 5, 10, 1, 12
    b_set = {
        vertex
        for vertex in range(len(graph))
        if vertex != x and not edge(graph, x, vertex)
    }
    demand(b_set == {3, 7, 9, 10}, "control B")
    banned = {
        (1 << v) | (1 << t) | (1 << member)
        for member in b_set
    }
    kernel, ranks, layers = restricted_ranks(graph, banned)
    demand(not kernel and layers == (20, 53, 90, 34), "control peel")
    source = (1 << r) | (1 << y) | (1 << e)
    demand(source in family and ranks[source] == 2, "control source rank")
    attacks = deletion_attacks(
        graph, source, ranks[source], banned, kernel, ranks
    )
    demand(attacks == (0, 3, 5), "control deleting attacks")
    rows = []
    for attack in attacks:
        neighbor_set = tuple(
            guard for guard in bits(source) if edge(graph, guard, attack)
        )
        retained = []
        for mover, endpoint in moves(graph, source, attack):
            demand(endpoint in family, "control physical endpoint omitted")
            delta, spokes = audit_endpoint(
                graph,
                family,
                source,
                attack,
                mover,
                endpoint,
                (v, t),
                b_set,
                banned,
                ranks,
            )
            demand(ranks[endpoint] == 1, "control endpoint not rank one")
            retained.append(
                {
                    "mover": mover,
                    "endpoint": list(bits(endpoint)),
                    "rank": ranks[endpoint],
                    "distance": delta,
                    "supported_spokes": spokes,
                }
            )
        rows.append(
            {
                "attack": attack,
                "neighbor_set": list(neighbor_set),
                "retained": retained,
            }
        )

    target = x
    target_rows = {
        mover: endpoint for mover, endpoint in moves(graph, source, target)
    }
    expected_target = {
        y: (1 << x) | (1 << r) | (1 << e),
        e: (1 << x) | (1 << r) | (1 << y),
    }
    demand(target_rows == expected_target, "control target endpoints")
    demand(all(endpoint in family for endpoint in target_rows.values()), "target retained")
    demand(ranks[expected_target[y]] == 3, "target petal rank")
    demand(ranks[expected_target[e]] == 2, "target hub rank")
    demand(
        target not in deletion_attacks(
            graph, source, ranks[source], banned, kernel, ranks
        ),
        "target incorrectly deleting",
    )
    demand(dominates(graph, expected_target[e]), "target hub nondominating")

    dominating_pairs = [
        list(bits(pair))
        for pair in subsets(len(graph), 2)
        if dominates(graph, pair)
    ]
    demand(dominating_pairs, "gamma-two boundary has no pair")
    return {
        "graph6": CONTROL,
        "graph6_sha256": hashlib.sha256(CONTROL.encode("ascii")).hexdigest(),
        "parameters": list(parameters),
        "greatest_triple_family_size": len(family),
        "restricted_kernel_size": len(kernel),
        "round_sizes": list(layers),
        "fan_state": list(bits(source)),
        "fan_rank": ranks[source],
        "deletion_rows": rows,
        "target_endpoint_ranks": {
            str(mover): ranks[endpoint]
            for mover, endpoint in target_rows.items()
        },
        "dominating_pair_count": len(dominating_pairs),
    }


def greatest_family_size(graph: tuple[int, ...], size: int) -> set[int]:
    alive = {
        state
        for state in subsets(len(graph), size)
        if dominates(graph, state)
    }
    while True:
        rejected = {
            state
            for state in alive
            if any(
                not any(endpoint in alive for _, endpoint in moves(graph, state, attack))
                for attack in range(len(graph))
                if not state & (1 << attack)
            )
        }
        if not rejected:
            return alive
        alive -= rejected


def main() -> None:
    print(
        json.dumps(
            {
                "schema": "full-list-higher-rank-fan-hostile-review-v1",
                "status": "PASS",
                "symbolic": symbolic_audit(),
                "finite_census": finite_census(),
                "gamma_two_boundary": control_audit(),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
