#!/usr/bin/env python3
"""Exact checks for the higher-rank completion-fan exit normal form."""

from __future__ import annotations

import itertools
import json
import hashlib


CONTROL = "LEhbtnm~D]xln{"


def need(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def choose_masks(order: int, size: int):
    for choice in itertools.combinations(range(order), size):
        yield sum(1 << vertex for vertex in choice)


def members(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def graph_from_code(order: int, code: int) -> tuple[int, ...]:
    adjacency = [0] * order
    for index, (left, right) in enumerate(itertools.combinations(range(order), 2)):
        if code >> index & 1:
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    return tuple(adjacency)


def decode_graph6(record: str) -> tuple[int, ...]:
    words = [ord(character) - 63 for character in record]
    need(words and 0 <= words[0] <= 62, "short graph6 only")
    order = words[0]
    bits = [
        (word >> shift) & 1
        for word in words[1:]
        for shift in range(5, -1, -1)
    ]
    required = order * (order - 1) // 2
    need(len(bits) >= required and not any(bits[required:]), "graph6 payload")
    adjacency = [0] * order
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1
    return tuple(adjacency)


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    return all(
        not adjacency[vertex] & (state ^ (1 << vertex))
        for vertex in members(state)
    )


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in members(state):
        covered |= adjacency[vertex]
    return covered == (1 << len(adjacency)) - 1


def physical_endpoints(adjacency, state: int, attack: int):
    bit = 1 << attack
    need(not state & bit, ("occupied attack", state, attack))
    for guard in members(state):
        if adjacency[guard] & bit:
            yield guard, (state ^ (1 << guard)) | bit


def dominating_triples(adjacency) -> set[int]:
    return {
        state for state in choose_masks(len(adjacency), 3)
        if dominates(adjacency, state)
    }


def greatest_family(adjacency, size: int = 3) -> set[int]:
    alive = {
        state for state in choose_masks(len(adjacency), size)
        if dominates(adjacency, state)
    }
    while True:
        deleted = {
            state
            for state in alive
            if any(
                not any(
                    endpoint in alive
                    for _, endpoint in physical_endpoints(adjacency, state, attack)
                )
                for attack in range(len(adjacency))
                if not state & (1 << attack)
            )
        }
        if not deleted:
            return alive
        alive.difference_update(deleted)


def peel(adjacency, banned: set[int]):
    universe = dominating_triples(adjacency)
    alive = universe - banned
    ranks: dict[int, int] = {}
    round_sizes = []
    rank = 0
    while True:
        deleted = {
            state
            for state in alive
            if any(
                not any(
                    endpoint in alive
                    for _, endpoint in physical_endpoints(adjacency, state, attack)
                )
                for attack in range(len(adjacency))
                if not state & (1 << attack)
            )
        }
        if not deleted:
            return alive, ranks, tuple(round_sizes)
        for state in deleted:
            ranks[state] = rank
        round_sizes.append(len(deleted))
        alive.difference_update(deleted)
        rank += 1


def deletion_witnesses(adjacency, state, banned, kernel, ranks):
    rank = ranks[state]
    result = []
    for attack in range(len(adjacency)):
        if state & (1 << attack):
            continue
        unbanned_dominating = [
            endpoint
            for _, endpoint in physical_endpoints(adjacency, state, attack)
            if endpoint not in banned and dominates(adjacency, endpoint)
        ]
        if not any(
            endpoint in kernel
            or (endpoint in ranks and ranks[endpoint] >= rank)
            for endpoint in unbanned_dominating
        ):
            result.append(attack)
    return tuple(result)


def distance_to_ban(state: int, banned: set[int]) -> int:
    return min(3 - (state & blocked).bit_count() for blocked in banned)


def common_nonneighbors(adjacency, left: int, right: int) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(adjacency))
        if vertex not in (left, right)
        and not adjacency[left] & (1 << vertex)
        and not adjacency[right] & (1 << vertex)
    )


def retained_fan(adjacency, family, left: int, right: int) -> bool:
    return all(
        ((1 << left) | (1 << right) | (1 << witness)) in family
        for witness in common_nonneighbors(adjacency, left, right)
    )


def equality_three(adjacency, family) -> bool:
    order = len(adjacency)
    return (
        not any(dominates(adjacency, pair) for pair in choose_masks(order, 2))
        and any(dominates(adjacency, triple) for triple in choose_masks(order, 3))
        and any(independent(adjacency, triple) for triple in choose_masks(order, 3))
        and not any(independent(adjacency, four) for four in choose_masks(order, 4))
        and bool(family)
    )


def minimum_size(adjacency, predicate) -> int:
    for size in range(1, len(adjacency) + 1):
        if any(predicate(state) for state in choose_masks(len(adjacency), size)):
            return size
    raise AssertionError("minimum not found")


def independence_number(adjacency) -> int:
    for size in range(len(adjacency), -1, -1):
        if any(independent(adjacency, state) for state in choose_masks(len(adjacency), size)):
            return size
    raise AssertionError("alpha not found")


def clique_cover_number(adjacency) -> int:
    order = len(adjacency)
    for count in range(1, order + 1):
        parts: list[list[int]] = [[] for _ in range(count)]

        def extend(vertex: int, used: int) -> bool:
            if vertex == order:
                return True
            for part in range(min(count, used + 1)):
                if all(adjacency[vertex] & (1 << member) for member in parts[part]):
                    parts[part].append(vertex)
                    if extend(vertex + 1, max(used, part + 1)):
                        return True
                    parts[part].pop()
            return False

        if extend(0, 0):
            return count
    raise AssertionError("theta not found")


def parameters(adjacency) -> tuple[int, int, int, int, int]:
    gamma = minimum_size(adjacency, lambda state: dominates(adjacency, state))
    ind_dom = minimum_size(
        adjacency,
        lambda state: independent(adjacency, state) and dominates(adjacency, state),
    )
    alpha = independence_number(adjacency)
    eternal = next(
        size for size in range(1, len(adjacency) + 1)
        if greatest_family(adjacency, size)
    )
    theta = clique_cover_number(adjacency)
    return gamma, ind_dom, alpha, eternal, theta


def audit_exit(
    adjacency,
    family,
    state,
    attack,
    banned,
    kernel,
    ranks,
    anchor_vertices,
    b_vertices,
) -> dict:
    rank = ranks[state]
    state_vertices = tuple(members(state))
    neighbor_set = tuple(
        guard for guard in state_vertices if adjacency[guard] & (1 << attack)
    )
    need(neighbor_set, "dominating state has no physical responder")
    retained = []
    for mover, endpoint in physical_endpoints(adjacency, state, attack):
        if endpoint not in family:
            continue
        need(endpoint not in banned, "distance-two response became banned")
        need(endpoint in ranks and ranks[endpoint] < rank, "response did not descend")
        reverse = list(physical_endpoints(adjacency, endpoint, mover))
        need(reverse == [(attack, state)], ("reverse is not unique", state, attack, mover, reverse))
        anchor_count = sum(1 for anchor in anchor_vertices if endpoint & (1 << anchor))
        # Source-form bans always have exactly two fixed anchors.  A response
        # from a state containing neither has at most one of them.
        need(anchor_count <= 1, "response contains both anchors")
        b_hit = any(endpoint & (1 << vertex) for vertex in b_vertices)
        formula_distance = 3 - anchor_count - int(b_hit)
        need(distance_to_ban(endpoint, banned) == formula_distance, "distance formula")
        need(ranks[endpoint] >= formula_distance - 1, "Johnson floor")
        supported_edges = []
        for stationary in members(endpoint ^ (1 << attack)):
            if adjacency[attack] & (1 << stationary):
                need(retained_fan(adjacency, family, attack, stationary), "supported fan absent")
                supported_edges.append((attack, stationary))
        retained.append(
            {
                "mover": mover,
                "endpoint": list(members(endpoint)),
                "rank": ranks[endpoint],
                "distance": formula_distance,
                "supported_edges": [list(edge) for edge in supported_edges],
            }
        )
    need(retained, "eternal family supplies no retained response")

    if len(neighbor_set) == 1:
        mover = neighbor_set[0]
        endpoint = (state ^ (1 << mover)) | (1 << attack)
        need(endpoint in family and independent(adjacency, endpoint), "singleton exit not independent")
        stationary = tuple(members(state ^ (1 << mover)))
        need(len(stationary) == 2, "wrong stationary pair")
        completion = common_nonneighbors(adjacency, *stationary)
        need(mover in completion and attack in completion, "not a shared completion fan")
    else:
        for row in retained:
            need(
                len(row["supported_edges"]) == len(neighbor_set) - 1,
                "wrong supported-spoke count",
            )
    return {
        "state": list(state_vertices),
        "state_rank": rank,
        "attack": attack,
        "neighbor_set": list(neighbor_set),
        "retained_responses": retained,
    }


def small_census() -> dict:
    graphs = 0
    equality_graphs = 0
    ban_instances = 0
    distance_two_states = 0
    higher_rank_states = 0
    deletion_exits = 0
    singleton_exits = 0
    multi_exits = 0
    rank_two_exits = 0
    rank_two_nonanchor_outside_b = 0
    higher_state_rank_counts: dict[int, int] = {}
    exit_source_rank_counts: dict[int, int] = {}
    for order in range(3, 7):
        for code in range(1 << (order * (order - 1) // 2)):
            graphs += 1
            adjacency = graph_from_code(order, code)
            family = greatest_family(adjacency)
            if not equality_three(adjacency, family):
                continue
            equality_graphs += 1
            for first, second in itertools.combinations(range(order), 2):
                remaining = [v for v in range(order) if v not in (first, second)]
                for selector in range(1, 1 << len(remaining)):
                    b_set = {
                        remaining[index]
                        for index in range(len(remaining))
                        if selector >> index & 1
                    }
                    anchors = (1 << first) | (1 << second)
                    banned = {anchors | (1 << b) for b in b_set}
                    kernel, ranks, _ = peel(adjacency, banned)
                    ban_instances += 1
                    for state in family:
                        if (
                            state not in ranks
                            or not independent(adjacency, state)
                            or state & anchors
                            or distance_to_ban(state, banned) != 2
                        ):
                            continue
                        distance_two_states += 1
                        if ranks[state] < 2:
                            continue
                        higher_rank_states += 1
                        higher_state_rank_counts[ranks[state]] = (
                            higher_state_rank_counts.get(ranks[state], 0) + 1
                        )
                        for attack in deletion_witnesses(
                            adjacency, state, banned, kernel, ranks
                        ):
                            row = audit_exit(
                                adjacency,
                                family,
                                state,
                                attack,
                                banned,
                                kernel,
                                ranks,
                                (first, second),
                                b_set,
                            )
                            deletion_exits += 1
                            exit_source_rank_counts[ranks[state]] = (
                                exit_source_rank_counts.get(ranks[state], 0) + 1
                            )
                            if len(row["neighbor_set"]) == 1:
                                singleton_exits += 1
                            else:
                                multi_exits += 1
                            if ranks[state] == 2:
                                rank_two_exits += 1
                                endpoints = row["retained_responses"]
                                need(
                                    all(item["distance"] <= 2 for item in endpoints),
                                    "rank-two response remained distance three",
                                )
                                if (
                                    attack not in (first, second)
                                    and attack not in b_set
                                ):
                                    rank_two_nonanchor_outside_b += 1
                                    for item in endpoints:
                                        if item["mover"] in b_set:
                                            # Moving the last B-vertex out is allowed
                                            # only if another B-vertex remains.
                                            endpoint_set = set(item["endpoint"])
                                            need(endpoint_set & b_set, "rank-two shell violation")
    return {
        "orders": [3, 4, 5, 6],
        "labeled_graphs": graphs,
        "equality_graphs": equality_graphs,
        "source_form_bans": ban_instances,
        "distance_two_retained_independent_states": distance_two_states,
        "higher_rank_states": higher_rank_states,
        "deletion_exits": deletion_exits,
        "singleton_exits": singleton_exits,
        "multi_exits": multi_exits,
        "rank_two_exits": rank_two_exits,
        "rank_two_nonanchor_outside_B_exits": rank_two_nonanchor_outside_b,
        "higher_state_rank_counts": {
            str(rank): count for rank, count in sorted(higher_state_rank_counts.items())
        },
        "exit_source_rank_counts": {
            str(rank): count for rank, count in sorted(exit_source_rank_counts.items())
        },
    }


def control_audit() -> dict:
    adjacency = decode_graph6(CONTROL)
    family = greatest_family(adjacency)
    root = (0, 5, 6)
    x, u, v, t, r, y, e = 8, 6, 0, 5, 10, 1, 12
    B = {
        vertex
        for vertex in range(len(adjacency))
        if vertex != x and not adjacency[x] & (1 << vertex)
    }
    need(B == {3, 7, 9, 10}, "control B")
    fixed = (1 << v) | (1 << t)
    banned = {fixed | (1 << b) for b in B}
    kernel, ranks, rounds = peel(adjacency, banned)
    need(not kernel and rounds == (20, 53, 90, 34), "control peeling")
    state = (1 << r) | (1 << y) | (1 << e)
    need(state in family and ranks[state] == 2, "control fan state")
    need(distance_to_ban(state, banned) == 2, "control fan distance")
    attacks = deletion_witnesses(adjacency, state, banned, kernel, ranks)
    need(attacks == (0, 3, 5), "control deleting attacks")
    rows = [
        audit_exit(
            adjacency,
            family,
            state,
            attack,
            banned,
            kernel,
            ranks,
            (v, t),
            B,
        )
        for attack in attacks
    ]
    fan = common_nonneighbors(adjacency, r, y)
    need(fan == (e,), "control completion fan")
    cross = (1 << x) | (1 << r) | (1 << y)
    hinge = (1 << x) | (1 << r) | (1 << e)
    need(dominates(adjacency, cross) and cross in family, "control cross state")
    need(ranks[cross] == 2, "control cross rank")
    target_endpoints = {
        mover: endpoint for mover, endpoint in physical_endpoints(adjacency, state, x)
    }
    need(target_endpoints == {y: hinge, e: cross}, "control target responses")
    target_membership = {
        str(mover): {
            "endpoint": list(members(endpoint)),
            "retained": endpoint in family,
            "rank": ranks.get(endpoint),
        }
        for mover, endpoint in target_endpoints.items()
    }
    return {
        "graph6": CONTROL,
        "graph6_sha256": hashlib.sha256(CONTROL.encode("ascii")).hexdigest(),
        "parameters": list(parameters(adjacency)),
        "greatest_family_size": len(family),
        "source_color": u,
        "anchors": [v, t],
        "B": sorted(B),
        "kernel_size": len(kernel),
        "round_sizes": list(rounds),
        "fan": list(fan),
        "fan_state": list(members(state)),
        "fan_rank": ranks[state],
        "deletion_witnesses": list(attacks),
        "exit_rows": rows,
        "cross_state": list(members(cross)),
        "cross_rank": ranks[cross],
        "target_responses": target_membership,
    }


def main() -> None:
    result = {
        "schema": "full-list-higher-rank-fan-normal-form-v1",
        "small_census": small_census(),
        "gamma_two_boundary": control_audit(),
        "status": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
