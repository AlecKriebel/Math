#!/usr/bin/env python3
"""Clean-room audit for finite-horizon star transport and rank descent.

This program deliberately uses integer masks and synchronous layer snapshots.
It imports no campaign module and shares no transition routine with the
candidate checker.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter


INFINITY = 10**9
FIXED = ("HCOe`Z{", "HCRdnat", "HEjejrr", "GEjbug")


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def masks_of_size(n: int, k: int) -> list[int]:
    return [
        sum(1 << v for v in choice)
        for choice in itertools.combinations(range(n), k)
    ]


def graph6(record: str) -> tuple[int, ...]:
    values = [ord(c) - 63 for c in record]
    if not values or not 0 <= values[0] <= 62:
        raise ValueError("the audit only supports short graph6 records")
    n = values[0]
    stream = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    adj = [0] * n
    cursor = 0
    for upper in range(1, n):
        for lower in range(upper):
            if stream[cursor]:
                adj[lower] |= 1 << upper
                adj[upper] |= 1 << lower
            cursor += 1
    return tuple(adj)


def graph_from_edge_mask(n: int, encoded: int) -> tuple[int, ...]:
    adj = [0] * n
    index = 0
    for u in range(n):
        for v in range(u + 1, n):
            if encoded & (1 << index):
                adj[u] |= 1 << v
                adj[v] |= 1 << u
            index += 1
    return tuple(adj)


def independent(adj: tuple[int, ...], state: int) -> bool:
    return all((adj[v] & (state ^ (1 << v))) == 0 for v in vertices(state))


def dominates(adj: tuple[int, ...], state: int) -> bool:
    covered = state
    for v in vertices(state):
        covered |= adj[v]
    return covered == (1 << len(adj)) - 1


def kernel_ranks(adj: tuple[int, ...], k: int) -> tuple[set[int], dict[int, int]]:
    """Return the greatest family and the literal synchronous deletion rank."""
    all_states = masks_of_size(len(adj), k)
    live = {state for state in all_states if dominates(adj, state)}
    rank = {state: 0 for state in all_states if state not in live}
    round_number = 0
    while True:
        snapshot = frozenset(live)
        doomed: set[int] = set()
        for state in snapshot:
            for target in range(len(adj)):
                target_bit = 1 << target
                if state & target_bit:
                    continue
                defended = False
                for guard in vertices(state & adj[target]):
                    successor = (state ^ (1 << guard)) | target_bit
                    if successor in snapshot:
                        defended = True
                        break
                if not defended:
                    doomed.add(state)
                    break
        if not doomed:
            break
        round_number += 1
        for state in doomed:
            rank[state] = round_number
        live.difference_update(doomed)
    for state in live:
        rank[state] = INFINITY
    return live, rank


def parameters(adj: tuple[int, ...]) -> dict[str, int]:
    n = len(adj)
    gamma = next(
        k
        for k in range(1, n + 1)
        if any(dominates(adj, state) for state in masks_of_size(n, k))
    )
    alpha = max(
        k
        for k in range(1, n + 1)
        if any(independent(adj, state) for state in masks_of_size(n, k))
    )
    independent_domination = next(
        k
        for k in range(1, n + 1)
        if any(
            independent(adj, state) and dominates(adj, state)
            for state in masks_of_size(n, k)
        )
    )
    gamma_infinity = next(
        k for k in range(1, n + 1) if kernel_ranks(adj, k)[0]
    )
    return {
        "gamma": gamma,
        "i": independent_domination,
        "alpha": alpha,
        "gamma_infinity": gamma_infinity,
    }


def printable_rank(value: int) -> int | str:
    return "infinity" if value == INFINITY else value


def state_text(mask: int) -> str:
    return "".join(str(v) for v in vertices(mask))


def edge_hash(adj: tuple[int, ...]) -> str:
    text = "".join(
        f"{u} {v}\n"
        for u in range(len(adj))
        for v in range(u + 1, len(adj))
        if adj[u] & (1 << v)
    )
    return hashlib.sha256(text.encode("ascii")).hexdigest()


def audit_star_pairs(
    adj: tuple[int, ...], k: int, rank: dict[int, int]
) -> Counter:
    n = len(adj)
    sources = [
        state for state in masks_of_size(n, k) if independent(adj, state)
    ]
    counts: Counter = Counter()
    for index, left_source in enumerate(sources):
        for right_source in sources[index + 1 :]:
            common = left_source & right_source
            if not common:
                continue
            distance = (left_source ^ right_source).bit_count() // 2
            outside = ((1 << n) - 1) ^ (left_source | right_source)
            for responder in vertices(common):
                without_responder_left = left_source ^ (1 << responder)
                without_responder_right = right_source ^ (1 << responder)
                for target in vertices(outside):
                    left = without_responder_left | (1 << target)
                    right = without_responder_right | (1 << target)
                    left_rank = rank[left]
                    right_rank = rank[right]
                    counts["comparisons"] += 1
                    if left_rank == INFINITY or right_rank == INFINITY:
                        assert left_rank == right_rank == INFINITY
                        counts["survivor_pairs"] += 1
                    else:
                        assert abs(left_rank - right_rank) <= distance
                        counts["finite_pairs"] += 1
                        if abs(left_rank - right_rank) == distance:
                            counts["sharp_finite_pairs"] += 1
                    # Check the directed horizon implication literally.
                    maximum_finite = max(
                        value
                        for value in rank.values()
                        if value != INFINITY
                    )
                    for first, second in (
                        (left_rank, right_rank),
                        (right_rank, left_rank),
                    ):
                        for horizon in range(maximum_finite + 2):
                            first_in_later = (
                                first == INFINITY or first > horizon + distance
                            )
                            second_in_now = second == INFINITY or second > horizon
                            assert not first_in_later or second_in_now
                            counts["directed_horizon_tests"] += 1
    return counts


def deleting_attacks(
    adj: tuple[int, ...], state: int, state_rank: int, rank: dict[int, int]
) -> list[tuple[int, list[tuple[int, int]]]]:
    attacks = []
    for target in range(len(adj)):
        if state & (1 << target):
            continue
        successors = [
            (guard, (state ^ (1 << guard)) | (1 << target))
            for guard in vertices(state & adj[target])
        ]
        if successors and all(rank[successor] < state_rank for _, successor in successors):
            attacks.append((target, successors))
    return attacks


def audit_descent_on_equality_graph(adj: tuple[int, ...]) -> Counter:
    """Exhaustively check Theorem 4.1 whenever its asymmetry premise occurs."""
    n = len(adj)
    params = parameters(adj)
    k = params["alpha"]
    counts: Counter = Counter()
    if not (
        params["gamma"] == params["gamma_infinity"] == k
        and params["i"] == k
    ):
        return counts
    family, rank = kernel_ranks(adj, k)
    facets = [
        state for state in masks_of_size(n, k) if independent(adj, state)
    ]
    active: set[tuple[int, int]] = set()
    for source in facets:
        for u in vertices(source):
            for x in range(n):
                if source & (1 << x):
                    continue
                successor = (source ^ (1 << u)) | (1 << x)
                if adj[u] & (1 << x) and successor in family:
                    active.add((u, x))
    for u, x in active:
        if (x, u) in active:
            continue
        endpoints = [state for state in facets if state & (1 << x)]
        endpoint_ranks = []
        for endpoint in endpoints:
            reverse = (endpoint ^ (1 << x)) | (1 << u)
            assert dominates(adj, reverse)
            assert 1 <= rank[reverse] < INFINITY
            endpoint_ranks.append(rank[reverse])
        minimum = min(endpoint_ranks)
        for endpoint, endpoint_rank in zip(endpoints, endpoint_ranks):
            reverse = (endpoint ^ (1 << x)) | (1 << u)
            attacks = deleting_attacks(adj, reverse, endpoint_rank, rank)
            assert attacks
            for target, successors in attacks:
                counts["deleting_attacks"] += 1
                hits = (endpoint & adj[target]).bit_count()
                assert hits >= 1
                if hits == 1:
                    q_bit = endpoint & adj[target]
                    assert q_bit != (1 << x)
                    next_endpoint = (endpoint ^ q_bit) | (1 << target)
                    assert independent(adj, next_endpoint)
                    successor = (reverse ^ q_bit) | (1 << target)
                    assert rank[successor] == endpoint_rank - 1
                    counts["single_hit_descents"] += 1
                if endpoint_rank == 1 or endpoint_rank == minimum:
                    assert hits >= 2
                    counts["minimum_or_rank_one_collisions"] += 1
        counts["asymmetric_active_orientations"] += 1
    return counts


def fixed_controls() -> dict[str, object]:
    expected_parameters = {
        "HCOe`Z{": (3, 3, 3, 3),
        "HCRdnat": (3, 3, 3, 3),
        "HEjejrr": (2, 2, 3, 3),
        "GEjbug": (2, 2, 3, 3),
    }
    expected_hashes = {
        "HCOe`Z{": "e2d8e519f7988a345d766d0287aac38cbb5910b1f95d77b6f8c120a15c50a809",
        "HCRdnat": "09a0405fc84f3e030fd63c66d32df142c421971b04bc009210e1a20788e77c18",
        "HEjejrr": "c015a0d48626f97bb8646280d3323b4833fb1378797e76558001836dc2ddc5a4",
        "GEjbug": "c3c3356fbda9f1e2a477c795e31cd1bf96fa5b3ac22489c94ba739d3457bb136",
    }
    summaries: dict[str, object] = {}
    cache: dict[str, tuple[tuple[int, ...], set[int], dict[int, int]]] = {}
    for record in FIXED:
        adj = graph6(record)
        params = parameters(adj)
        observed_tuple = (
            params["gamma"],
            params["i"],
            params["alpha"],
            params["gamma_infinity"],
        )
        assert observed_tuple == expected_parameters[record]
        assert edge_hash(adj) == expected_hashes[record]
        family, rank = kernel_ranks(adj, 3)
        cache[record] = (adj, family, rank)
        triple_audit = audit_star_pairs(adj, 3, rank)
        summaries[record] = {
            "parameters": params,
            "order": len(adj),
            "size": sum(mask.bit_count() for mask in adj) // 2,
            "edge_list_sha256": edge_hash(adj),
            "greatest_triple_family_size": len(family),
            "rank_histogram": {
                str(key): value
                for key, value in sorted(
                    Counter(
                        value
                        for value in rank.values()
                        if 0 < value < INFINITY
                    ).items()
                )
            },
            "triple_star_audit": dict(sorted(triple_audit.items())),
        }

    adj, family, rank = cache["HCOe`Z{"]
    unit_left, unit_right = 0b100000110, 0b110000010
    assert [rank[unit_left], rank[unit_right]] == [1, 2]

    adj2, family2, rank2 = cache["HCRdnat"]
    distance_left = (1 << 0) | (1 << 1) | (1 << 8)
    distance_right = (1 << 3) | (1 << 4) | (1 << 8)
    assert [rank2[distance_left], rank2[distance_right]] == [3, 1]

    adj3, family3, rank3 = cache["HEjejrr"]
    source = (1 << 0) | (1 << 1) | (1 << 2)
    endpoint = (1 << 4) | (1 << 5) | (1 << 8)
    forward = (source ^ (1 << 0)) | (1 << 4)
    reverse = (endpoint ^ (1 << 4)) | (1 << 0)
    assert forward in family3 and rank3[reverse] == 2
    descents = deleting_attacks(adj3, reverse, 2, rank3)
    attack_three = next(item for item in descents if item[0] == 3)
    assert (endpoint & adj3[3]).bit_count() == 1
    assert all(rank3[successor] < 2 for _, successor in attack_three[1])
    assert next(
        rank3[successor]
        for guard, successor in attack_three[1]
        if guard == 8
    ) == 1

    adj4, family4, rank4 = cache["GEjbug"]
    source4 = (1 << 0) | (1 << 1) | (1 << 2)
    endpoint4 = (1 << 3) | (1 << 4) | (1 << 5)
    forward4 = (source4 ^ (1 << 0)) | (1 << 4)
    reverse4 = (endpoint4 ^ (1 << 4)) | (1 << 0)
    assert forward4 in family4 and rank4[reverse4] == 1
    collisions = deleting_attacks(adj4, reverse4, 1, rank4)
    attack_seven = next(item for item in collisions if item[0] == 7)
    assert sorted(vertices(endpoint4 & adj4[7])) == [3, 5]
    assert {rank4[successor] for _, successor in attack_seven[1]} == {0}

    return {
        "graphs": summaries,
        "unit_bound": [rank[unit_left], rank[unit_right]],
        "distance_two_bound": [rank2[distance_left], rank2[distance_right]],
        "single_hit_descent": {
            "reverse_rank": rank3[reverse],
            "attack": attack_three[0],
            "successor_ranks": [
                rank3[successor] for _, successor in attack_three[1]
            ],
        },
        "rank_one_collision": {
            "reverse_rank": rank4[reverse4],
            "attack": attack_seven[0],
            "endpoint_neighbors": sorted(vertices(endpoint4 & adj4[7])),
            "successor_ranks": [
                rank4[successor] for _, successor in attack_seven[1]
            ],
        },
    }


def small_graph_exhaustion() -> dict[str, int]:
    totals: Counter = Counter()
    for n in range(1, 7):
        edge_count = n * (n - 1) // 2
        for encoded in range(1 << edge_count):
            adj = graph_from_edge_mask(n, encoded)
            totals["labeled_graphs"] += 1
            for k in range(1, n + 1):
                _, rank = kernel_ranks(adj, k)
                counts = audit_star_pairs(adj, k, rank)
                totals["guard_sizes"] += 1
                totals["star_comparisons"] += counts["comparisons"]
                totals["directed_horizon_tests"] += counts[
                    "directed_horizon_tests"
                ]
            theorem_counts = audit_descent_on_equality_graph(adj)
            for key, value in theorem_counts.items():
                totals[key] += value
    for key in (
        "asymmetric_active_orientations",
        "deleting_attacks",
        "single_hit_descents",
        "minimum_or_rank_one_collisions",
    ):
        totals.setdefault(key, 0)
    return dict(sorted(totals.items()))


def main() -> None:
    result = {
        "schema": "reverse-rank-descent-hostile-v1",
        "status": "PASS",
        "model": {
            "attacks": "unoccupied vertices only",
            "response": "exactly one adjacent guard moves",
            "kernel": "literal synchronous greatest fixed point",
            "rank_zero": "non-dominating",
            "infinite_rank": "greatest-family survivor",
        },
        "fixed_controls": fixed_controls(),
        "small_graph_exhaustion": small_graph_exhaustion(),
        "scope": {
            "symbolic_proof": (
                "audited separately; finite tests corroborate but do not prove it"
            ),
            "not_established": (
                "survivor reciprocity, elimination of multi-hit collisions, "
                "a complete parameter case, or the gamma-theta conjecture"
            ),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
