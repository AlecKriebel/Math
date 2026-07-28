#!/usr/bin/env python3
"""Clean-room checks for the coinductive-reciprocity candidate.

This file does not import the candidate programs or the accepted C-138
checker.  It uses integer vertex masks, decodes graph6 directly, constructs
the synchronous greatest triple kernel from the one-guard definition, and
repeats both order-nine mechanism probes from a fresh implementation.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import pathlib
import subprocess


def decode_graph6(record: str) -> tuple[int, ...]:
    values = [ord(char) - 63 for char in record]
    if not values or any(value < 0 or value > 63 for value in values):
        raise ValueError(f"invalid graph6 record: {record!r}")
    n = values[0]
    if n >= 63:
        raise ValueError("only the one-byte graph6 order format is supported")
    bits: list[int] = []
    for value in values[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    if len(bits) < needed or any(bits[needed:]):
        raise ValueError(f"bad graph6 payload or padding: {record!r}")
    adjacency = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if bits[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return tuple(adjacency)


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def state_mask(state: tuple[int, ...] | list[int]) -> int:
    answer = 0
    for vertex in state:
        answer |= 1 << vertex
    return answer


def state_list(mask: int) -> list[int]:
    return list(vertices(mask))


def subset_masks(n: int, size: int) -> tuple[int, ...]:
    return tuple(
        state_mask(list(choice))
        for choice in itertools.combinations(range(n), size)
    )


def is_independent(adjacency: tuple[int, ...], state: int) -> bool:
    return all(adjacency[u] & (state ^ (1 << u)) == 0 for u in vertices(state))


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for guard in vertices(state):
        covered |= adjacency[guard]
    return covered == (1 << len(adjacency)) - 1


def graph_parameters(adjacency: tuple[int, ...]) -> dict[str, int]:
    n = len(adjacency)
    all_masks = range(1, 1 << n)
    independent = [mask for mask in all_masks if is_independent(adjacency, mask)]
    alpha = max(mask.bit_count() for mask in independent)
    maximal_independent = [
        mask
        for mask in independent
        if all(
            adjacency[v] & mask
            for v in range(n)
            if not (mask & (1 << v))
        )
    ]
    i_number = min(mask.bit_count() for mask in maximal_independent)
    gamma = min(
        mask.bit_count() for mask in all_masks if dominates(adjacency, mask)
    )
    return {"gamma": gamma, "i": i_number, "alpha": alpha}


def colorable(adjacency: tuple[int, ...], colors: int) -> bool:
    """DSATUR decision on the graph represented by ``adjacency``."""

    n = len(adjacency)
    assigned = [-1] * n
    neighbor_colors = [set() for _ in range(n)]

    def search(colored: int) -> bool:
        if colored == n:
            return True
        candidates = [v for v in range(n) if assigned[v] < 0]
        vertex = max(
            candidates,
            key=lambda v: (len(neighbor_colors[v]), adjacency[v].bit_count(), -v),
        )
        forbidden = neighbor_colors[vertex]
        for color in range(colors):
            if color in forbidden:
                continue
            assigned[vertex] = color
            changed = []
            for neighbor in vertices(adjacency[vertex]):
                if assigned[neighbor] < 0 and color not in neighbor_colors[neighbor]:
                    neighbor_colors[neighbor].add(color)
                    changed.append(neighbor)
            if search(colored + 1):
                return True
            for neighbor in changed:
                neighbor_colors[neighbor].remove(color)
            assigned[vertex] = -1
        return False

    return search(0)


def clique_cover_number(adjacency: tuple[int, ...]) -> int:
    n = len(adjacency)
    full = (1 << n) - 1
    complement = tuple(
        full ^ (1 << vertex) ^ adjacency[vertex] for vertex in range(n)
    )
    for colors in range(1, n + 1):
        if colorable(complement, colors):
            return colors
    raise AssertionError("coloring search did not terminate")


def greatest_triple_kernel(
    adjacency: tuple[int, ...],
) -> tuple[frozenset[int], dict[int, int], frozenset[int]]:
    n = len(adjacency)
    triples = subset_masks(n, 3)
    dominating = frozenset(state for state in triples if dominates(adjacency, state))
    live = set(dominating)
    ranks: dict[int, int] = {}
    round_number = 1
    while True:
        doomed = set()
        for state in live:
            for attacked in range(n):
                if state & (1 << attacked):
                    continue
                answered = False
                for guard in vertices(state):
                    if not (adjacency[guard] & (1 << attacked)):
                        continue
                    successor = (state ^ (1 << guard)) | (1 << attacked)
                    if successor in live:
                        answered = True
                        break
                if not answered:
                    doomed.add(state)
                    break
        if not doomed:
            break
        for state in doomed:
            ranks[state] = round_number
        live.difference_update(doomed)
        round_number += 1
    assert len(live) + len(ranks) == len(dominating)
    return frozenset(live), ranks, dominating


def deletion_rank(
    state: int,
    kernel: frozenset[int],
    ranks: dict[int, int],
    dominating: frozenset[int],
) -> int | str:
    if state in kernel:
        return "S"
    if state not in dominating:
        return 0
    return ranks[state]


def independent_triples(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        state
        for state in subset_masks(len(adjacency), 3)
        if is_independent(adjacency, state)
    )


def static_equality_filter(adjacency: tuple[int, ...]) -> tuple[int, ...] | None:
    n = len(adjacency)
    independent = independent_triples(adjacency)
    if not independent:
        return None
    if any(
        is_independent(adjacency, state) for state in subset_masks(n, 4)
    ):
        return None
    if any(
        dominates(adjacency, state)
        for size in (1, 2)
        for state in subset_masks(n, size)
    ):
        return None
    assert all(dominates(adjacency, state) for state in independent)
    return independent


def response_list(
    adjacency: tuple[int, ...],
    family: frozenset[int],
    state: int,
    attacked: int,
) -> list[int]:
    return [
        guard
        for guard in vertices(state)
        if adjacency[guard] & (1 << attacked)
        and ((state ^ (1 << guard)) | (1 << attacked)) in family
    ]


def active_edges(
    adjacency: tuple[int, ...],
    independent: tuple[int, ...],
    kernel: frozenset[int],
) -> set[tuple[int, int]]:
    n = len(adjacency)
    active = set()
    for state in independent:
        for guard in vertices(state):
            for target in range(n):
                if state & (1 << target):
                    continue
                successor = (state ^ (1 << guard)) | (1 << target)
                if successor in kernel:
                    active.add((guard, target))
    return active


def check_fcxfo() -> dict[str, object]:
    record = "FCXfO"
    adjacency = decode_graph6(record)
    expected_edges = {
        frozenset(edge)
        for edge in (
            (0, 3),
            (0, 6),
            (1, 4),
            (1, 5),
            (1, 6),
            (2, 4),
            (2, 5),
            (2, 6),
            (4, 6),
        )
    }
    decoded_edges = {
        frozenset((u, v))
        for u in range(7)
        for v in range(u + 1, 7)
        if adjacency[u] & (1 << v)
    }
    assert decoded_edges == expected_edges

    family_states = (
        (0, 1, 2),
        (0, 1, 4),
        (0, 1, 6),
        (0, 2, 4),
        (0, 2, 5),
        (0, 2, 6),
        (0, 4, 5),
        (0, 5, 6),
        (1, 2, 3),
        (1, 3, 4),
        (1, 3, 6),
        (2, 3, 4),
        (2, 3, 5),
        (2, 3, 6),
        (3, 4, 5),
        (3, 5, 6),
    )
    family = frozenset(state_mask(list(state)) for state in family_states)
    obligations = 0
    retained_moves = 0
    for state in family:
        assert dominates(adjacency, state)
        for attacked in range(7):
            if state & (1 << attacked):
                continue
            obligations += 1
            responses = response_list(adjacency, family, state, attacked)
            assert responses
            retained_moves += len(responses)

    u, x, w, a, z = 1, 4, 0, 2, 5
    S = state_mask([u, w, a])
    T = state_mask([x, w, z])
    D = state_mask([x, w, a])
    O = state_mask([u, w, z])
    R = state_mask([u, x, w])
    P = state_mask([a, z, w])
    assert all(state in family for state in (S, T, D, R, P))
    assert O not in family
    lists = {
        "L_S(x)": response_list(adjacency, family, S, x),
        "L_T(u)": response_list(adjacency, family, T, u),
        "L_S(z)": response_list(adjacency, family, S, z),
        "L_T(a)": response_list(adjacency, family, T, a),
    }
    assert lists == {
        "L_S(x)": [u, a],
        "L_T(u)": [z],
        "L_S(z)": [u],
        "L_T(a)": [x, z],
    }
    assert response_list(adjacency, family, S, 3) == [w]
    assert response_list(adjacency, family, T, 3) == [w]
    assert not response_list(adjacency, family, O, 3)

    kernel, ranks, dominating_states = greatest_triple_kernel(adjacency)
    assert O in kernel
    assert state_mask([1, 3, 5]) in kernel
    parameters = graph_parameters(adjacency)
    assert parameters == {"gamma": 3, "i": 3, "alpha": 3}
    theta = clique_cover_number(adjacency)
    assert theta == 3
    assert kernel

    serialization = "\n".join(
        "".join(str(vertex) for vertex in state)
        for state in sorted(family_states)
    )
    return {
        "graph6": record,
        "order": 7,
        "size": len(decoded_edges),
        "parameters": {
            **parameters,
            "gamma_infinity": 3,
            "theta": theta,
        },
        "specified_family_size": len(family),
        "specified_family_sha256": hashlib.sha256(
            serialization.encode()
        ).hexdigest(),
        "specified_family_attack_obligations": obligations,
        "specified_family_retained_moves": retained_moves,
        "specified_family_lists": lists,
        "specified_family_omits_015": O not in family,
        "greatest_family_size": len(kernel),
        "greatest_family_contains_015": O in kernel,
        "greatest_family_contains_135": state_mask([1, 3, 5]) in kernel,
        "dominating_triples": len(dominating_states),
        "finite_rank_states": len(ranks),
    }


def check_gejbug() -> dict[str, object]:
    adjacency = decode_graph6("GEjbug")
    parameters = graph_parameters(adjacency)
    kernel, ranks, dominating_states = greatest_triple_kernel(adjacency)
    independent = independent_triples(adjacency)
    assert parameters == {"gamma": 2, "i": 2, "alpha": 3}
    assert len(kernel) == 41
    assert independent
    S = state_mask([0, 1, 2])
    T = state_mask([3, 4, 5])
    forward = state_mask([1, 2, 4])
    reverse = state_mask([0, 3, 5])
    assert S in kernel and T in kernel and forward in kernel
    assert reverse not in kernel and reverse in dominating_states
    assert ranks[reverse] == 1
    transforms = [
        ((1, 3, 4), (0, 1, 3)),
        ((1, 4, 7), (0, 1, 7)),
        ((3, 4, 7), (0, 3, 7)),
        ((4, 5, 7), (0, 5, 7)),
    ]
    for before, after in transforms:
        assert state_mask(list(before)) in kernel
        assert state_mask(list(after)) not in dominating_states
    return {
        "graph6": "GEjbug",
        "parameters": {**parameters, "gamma_infinity": 3},
        "greatest_family_size": len(kernel),
        "named_forward_survives": forward in kernel,
        "named_reverse_rank": ranks[reverse],
        "four_translated_states_are_nondominating": True,
    }


def check_named_order_nine_controls() -> dict[str, object]:
    strong_adjacency = decode_graph6("HCOeuqr")
    strong_independent = static_equality_filter(strong_adjacency)
    assert strong_independent is not None
    strong_kernel, strong_ranks, strong_dominating = greatest_triple_kernel(
        strong_adjacency
    )
    strong_active = active_edges(
        strong_adjacency, strong_independent, strong_kernel
    )
    survivor = state_mask([0, 5, 7])
    translated = state_mask([0, 3, 5])
    assert (3, 7) in strong_active
    assert survivor in strong_kernel
    assert translated not in strong_dominating
    assert deletion_rank(
        translated, strong_kernel, strong_ranks, strong_dominating
    ) == 0

    shared_adjacency = decode_graph6("HCOe`Z{")
    shared_independent = static_equality_filter(shared_adjacency)
    assert shared_independent is not None
    shared_kernel, shared_ranks, shared_dominating = greatest_triple_kernel(
        shared_adjacency
    )
    u, x = 8, 0
    endpoints = [state for state in shared_independent if state & (1 << x)]
    common_missed = [
        w
        for w in range(9)
        if w not in (u, x)
        and not (shared_adjacency[u] & (1 << w))
        and not (shared_adjacency[x] & (1 << w))
    ]
    ranks = []
    shared_pivot_ranks = []
    for endpoint in endpoints:
        reverse = (endpoint ^ (1 << x)) | (1 << u)
        rank = deletion_rank(
            reverse, shared_kernel, shared_ranks, shared_dominating
        )
        ranks.append(rank)
        if any(endpoint & (1 << w) for w in common_missed):
            shared_pivot_ranks.append(rank)
    assert [state_list(state) for state in endpoints] == [
        [0, 1, 2],
        [0, 1, 5],
        [0, 1, 7],
        [0, 2, 4],
        [0, 4, 5],
    ]
    assert common_missed == [7]
    assert ranks == [1, 1, 2, 0, 0]
    assert shared_pivot_ranks == [2]
    return {
        "strong_replacement": {
            "graph6": "HCOeuqr",
            "active_edge": [3, 7],
            "kernel_state": [0, 5, 7],
            "translated_state": [0, 3, 5],
            "translated_rank": 0,
            "translated_dominates": False,
        },
        "shared_minimum": {
            "graph6": "HCOe`Z{",
            "oriented_edge": [u, x],
            "common_missed_vertices": common_missed,
            "endpoints": [state_list(state) for state in endpoints],
            "all_reverse_ranks": ranks,
            "shared_pivot_reverse_ranks": shared_pivot_ranks,
        },
    }


def check_order_nine_probes(campaign: pathlib.Path) -> dict[str, object]:
    geng = campaign / "tools" / "nauty2_9_3" / "geng"
    records = subprocess.run(
        [str(geng), "-c", "-q", "9"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    assert len(records) == 261_080
    stream_sha256 = hashlib.sha256(
        "".join(f"{record}\n" for record in records).encode("ascii")
    ).hexdigest()
    assert (
        stream_sha256
        == "fe73f2b8aad1a653b6f3bee799efff369cc486688df5aeade62ce0b3b5889eb5"
    )

    strong_totals = {
        "eternal_equality_graphs": 0,
        "active_directed_edges": 0,
        "whole_kernel_transforms": 0,
        "failed_transforms": 0,
    }
    shared_totals = {
        "inactive_oriented_edges": 0,
        "minimum_attained_on_shared_pivot": 0,
        "shared_minimum_violations": 0,
        "actual_one_sided_survivors": 0,
    }
    static_equality_graphs = 0
    first_strong = None
    first_shared = None
    first_actual = None
    for record in records:
        adjacency = decode_graph6(record)
        independent = static_equality_filter(adjacency)
        if independent is None:
            continue
        static_equality_graphs += 1
        kernel, ranks, dominating_states = greatest_triple_kernel(adjacency)
        if not kernel:
            continue
        strong_totals["eternal_equality_graphs"] += 1

        active = active_edges(adjacency, independent, kernel)
        strong_totals["active_directed_edges"] += len(active)
        for guard, target in active:
            for state in kernel:
                if not (state & (1 << target)) or state & (1 << guard):
                    continue
                strong_totals["whole_kernel_transforms"] += 1
                transformed = (state ^ (1 << target)) | (1 << guard)
                if transformed in kernel:
                    continue
                strong_totals["failed_transforms"] += 1
                if first_strong is None:
                    first_strong = {
                        "graph6": record,
                        "active_edge": [guard, target],
                        "kernel_state": state_list(state),
                        "transformed_state": state_list(transformed),
                        "transformed_dominates": transformed in dominating_states,
                        "transformed_deletion_rank": deletion_rank(
                            transformed, kernel, ranks, dominating_states
                        ),
                    }

        for u in range(9):
            for x in vertices(adjacency[u]):
                endpoints = [
                    state for state in independent if state & (1 << x)
                ]
                common_missed = {
                    w
                    for w in range(9)
                    if w not in (u, x)
                    and not (adjacency[u] & (1 << w))
                    and not (adjacency[x] & (1 << w))
                }
                all_ranks = []
                pivot_ranks = []
                for endpoint in endpoints:
                    reverse = (endpoint ^ (1 << x)) | (1 << u)
                    rank = deletion_rank(
                        reverse, kernel, ranks, dominating_states
                    )
                    all_ranks.append(rank)
                    if any(endpoint & (1 << w) for w in common_missed):
                        pivot_ranks.append(rank)
                assert endpoints and pivot_ranks
                if "S" in all_ranks:
                    continue
                shared_totals["inactive_oriented_edges"] += 1
                if min(all_ranks) == min(pivot_ranks):
                    shared_totals["minimum_attained_on_shared_pivot"] += 1
                else:
                    shared_totals["shared_minimum_violations"] += 1
                    if first_shared is None:
                        first_shared = {
                            "graph6": record,
                            "u": u,
                            "x": x,
                            "common_missed_vertices": sorted(common_missed),
                            "endpoints_containing_x": [
                                state_list(state) for state in endpoints
                            ],
                            "all_reverse_ranks": all_ranks,
                            "shared_pivot_reverse_ranks": pivot_ranks,
                        }

                forward_active = any(
                    state & (1 << u)
                    and ((state ^ (1 << u)) | (1 << x)) in kernel
                    for state in independent
                )
                if forward_active:
                    shared_totals["actual_one_sided_survivors"] += 1
                    if first_actual is None:
                        first_actual = {
                            "graph6": record,
                            "u": u,
                            "x": x,
                        }

    assert static_equality_graphs == 2_949
    assert strong_totals == {
        "eternal_equality_graphs": 1_380,
        "active_directed_edges": 28_366,
        "whole_kernel_transforms": 220_086,
        "failed_transforms": 4_108,
    }
    assert shared_totals == {
        "inactive_oriented_edges": 16_366,
        "minimum_attained_on_shared_pivot": 15_944,
        "shared_minimum_violations": 422,
        "actual_one_sided_survivors": 0,
    }
    # Set iteration order is deliberately not coupled to the candidate's
    # tuple-based implementation, so the first incidence inside the first
    # violating graph need not be identical.  The candidate's named
    # incidence is checked literally in check_named_order_nine_controls().
    assert first_strong is not None
    assert first_strong["graph6"] == "HCOeuqr"
    assert first_shared is not None and first_shared["graph6"] == "HCOe`Z{"
    assert first_actual is None
    return {
        "generator": str(geng.relative_to(campaign)),
        "connected_graphs": len(records),
        "stream_sha256": stream_sha256,
        "static_equality_graphs": static_equality_graphs,
        "strong_replacement": {
            "totals": strong_totals,
            "first_violation": first_strong,
        },
        "shared_minimum": {
            "totals": shared_totals,
            "first_violation": first_shared,
            "first_actual_one_sided_survivor": first_actual,
        },
    }


def main() -> None:
    campaign = pathlib.Path(__file__).resolve().parents[2]
    result = {
        "schema": "coinductive-reciprocity-hostile-clean-room-v1",
        "model": {
            "attacks_only_at_unoccupied_vertices": True,
            "exactly_one_guard_moves": True,
            "move_follows_one_graph_edge": True,
            "every_retained_successor_dominates": True,
            "greatest_kernel_deletion_is_synchronous": True,
        },
        "FCXfO": check_fcxfo(),
        "GEjbug": check_gejbug(),
        "named_order_nine_controls": check_named_order_nine_controls(),
        "order_nine_probes": check_order_nine_probes(campaign),
        "scope": {
            "theorem_proved_by_finite_check": False,
            "controls_reproduced_independently": True,
            "greatest_family_reciprocity": "OPEN",
            "gamma_theta_conjecture": "OPEN",
        },
        "status": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
