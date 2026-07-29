#!/usr/bin/env python3
"""Clean-room verifier for candidate C-173.

This file deliberately imports no campaign search or candidate-verifier code.
It uses only the Python standard library and reconstructs every graph/game
object directly from the definition.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


G6 = "LEhbtnm~D]xln{"
ROOT = (0, 5, 6)
TARGET = 8
SOURCE_COLOR = 6
V_COLOR = 0
T_ANCHOR = 5
Q = 2
R = 10
W = 3
Y = 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(text: str) -> list[int]:
    raw = [ord(ch) - 63 for ch in text.strip()]
    require(raw and 0 <= raw[0] <= 62, "only small graph6 headers supported")
    n = raw[0]
    bits: list[int] = []
    for word in raw[1:]:
        require(0 <= word <= 63, "invalid graph6 character")
        bits.extend((word >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    require(len(bits) >= needed, "truncated graph6 payload")
    require(all(bit == 0 for bit in bits[needed:]), "nonzero graph6 padding")
    adj = [0] * n
    pos = 0
    for high in range(1, n):
        for low in range(high):
            if bits[pos]:
                adj[low] |= 1 << high
                adj[high] |= 1 << low
            pos += 1
    return adj


def encode_graph6(adj: list[int]) -> str:
    n = len(adj)
    require(n <= 62, "only small graph6 headers supported")
    bits = []
    for high in range(1, n):
        for low in range(high):
            bits.append((adj[low] >> high) & 1)
    while len(bits) % 6:
        bits.append(0)
    words = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        words.append(chr(value + 63))
    return chr(n + 63) + "".join(words)


def subsets_of_size(n: int, size: int):
    for vertices in itertools.combinations(range(n), size):
        mask = sum(1 << vertex for vertex in vertices)
        yield mask


def vertices(mask: int) -> tuple[int, ...]:
    return tuple(index for index in range(mask.bit_length()) if mask >> index & 1)


def is_independent(mask: int, adj: list[int]) -> bool:
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        remaining ^= bit
        if adj[vertex] & remaining:
            return False
    return True


def is_dominating(mask: int, adj: list[int]) -> bool:
    covered = mask
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        remaining ^= bit
        covered |= adj[vertex]
    return covered == (1 << len(adj)) - 1


def parameter_values(adj: list[int]) -> tuple[int, int, int]:
    n = len(adj)
    gamma = n
    independent_domination = n
    alpha = 0
    for mask in range(1 << n):
        count = mask.bit_count()
        independent = is_independent(mask, adj)
        if independent:
            alpha = max(alpha, count)
            maximal = all(
                mask >> vertex & 1 or adj[vertex] & mask
                for vertex in range(n)
            )
            if maximal:
                independent_domination = min(independent_domination, count)
        if count < gamma and is_dominating(mask, adj):
            gamma = count
    return gamma, independent_domination, alpha


def colorable(adj: list[int], colors: int) -> tuple[bool, list[int] | None]:
    """Exact DSATUR backtracking for the graph represented by adj."""
    n = len(adj)
    assignment = [-1] * n
    degrees = [mask.bit_count() for mask in adj]

    def search(colored: int) -> bool:
        if colored == n:
            return True
        choices = []
        for vertex in range(n):
            if assignment[vertex] >= 0:
                continue
            seen = {
                assignment[neighbor]
                for neighbor in range(n)
                if adj[vertex] >> neighbor & 1 and assignment[neighbor] >= 0
            }
            choices.append((len(seen), degrees[vertex], -vertex, vertex, seen))
        _, _, _, vertex, forbidden = max(choices)
        for color in range(colors):
            if color in forbidden:
                continue
            assignment[vertex] = color
            if search(colored + 1):
                return True
            assignment[vertex] = -1
        return False

    possible = search(0)
    return possible, assignment[:] if possible else None


def clique_cover_number(adj: list[int]) -> tuple[int, list[int]]:
    n = len(adj)
    full = (1 << n) - 1
    complement = [full ^ (1 << vertex) ^ adj[vertex] for vertex in range(n)]
    for colors in range(1, n + 1):
        possible, assignment = colorable(complement, colors)
        if possible:
            assert assignment is not None
            return colors, assignment
    raise AssertionError("coloring search failed")


def dominating_states(adj: list[int], k: int) -> set[int]:
    return {
        mask for mask in subsets_of_size(len(adj), k)
        if is_dominating(mask, adj)
    }


def legal_successors(
    state: int, attack: int, adj: list[int], allowed: set[int]
) -> list[int]:
    result = []
    guards = state
    while guards:
        bit = guards & -guards
        guard = bit.bit_length() - 1
        guards ^= bit
        if adj[guard] >> attack & 1:
            endpoint = (state ^ bit) | (1 << attack)
            if endpoint in allowed:
                result.append(endpoint)
    return sorted(result)


def greatest_family(adj: list[int], k: int) -> set[int]:
    alive = dominating_states(adj, k)
    while True:
        bad = set()
        for state in alive:
            for attack in range(len(adj)):
                if state >> attack & 1:
                    continue
                if not legal_successors(state, attack, adj, alive):
                    bad.add(state)
                    break
        if not bad:
            return alive
        alive -= bad


def eternal_number(adj: list[int]) -> tuple[int, set[int]]:
    gamma, _, _ = parameter_values(adj)
    for k in range(gamma, len(adj) + 1):
        family = greatest_family(adj, k)
        if family:
            return k, family
    raise AssertionError("full vertex set must be eternal")


def restricted_peeling(
    adj: list[int], k: int, banned: set[int]
) -> tuple[set[int], dict[int, int], tuple[int, ...]]:
    alive = dominating_states(adj, k) - banned
    ranks: dict[int, int] = {}
    round_sizes = []
    round_index = 0
    while True:
        bad = set()
        for state in alive:
            for attack in range(len(adj)):
                if state >> attack & 1:
                    continue
                if not legal_successors(state, attack, adj, alive):
                    bad.add(state)
                    break
        if not bad:
            return alive, ranks, tuple(round_sizes)
        for state in bad:
            ranks[state] = round_index
        round_sizes.append(len(bad))
        alive -= bad
        round_index += 1


def attack_witnesses(
    state: int,
    rank: int,
    adj: list[int],
    banned: set[int],
    ranks: dict[int, int],
    kernel: set[int],
) -> list[int]:
    witnesses = []
    dominating = dominating_states(adj, state.bit_count())
    for attack in range(len(adj)):
        if state >> attack & 1:
            continue
        endpoints = legal_successors(state, attack, adj, dominating)
        if all(
            endpoint in banned
            or (endpoint in ranks and ranks[endpoint] < rank)
            or endpoint not in dominating
            for endpoint in endpoints
        ):
            # legal_successors above already restricts to dominating endpoints.
            # Kernel and same/higher-rank endpoints therefore block witnessing.
            if not any(
                endpoint in kernel
                or (endpoint in ranks and ranks[endpoint] >= rank)
                for endpoint in endpoints
                if endpoint not in banned
            ):
                witnesses.append(attack)
    return witnesses


def common_nonneighbors(a: int, b: int, adj: list[int]) -> set[int]:
    n = len(adj)
    return {
        vertex
        for vertex in range(n)
        if vertex not in (a, b)
        and not (adj[a] >> vertex & 1)
        and not (adj[b] >> vertex & 1)
    }


def is_clique(items: set[int], adj: list[int]) -> bool:
    return all(
        adj[a] >> b & 1
        for a, b in itertools.combinations(sorted(items), 2)
    )


def mask_of(*items: int) -> int:
    return sum(1 << item for item in items)


def unique_physical_response(
    state: int, attack: int, expected: int, adj: list[int]
) -> None:
    require(not (state >> attack & 1), f"attack {attack} is occupied")
    movers = [
        guard for guard in vertices(state)
        if adj[guard] >> attack & 1
    ]
    require(movers == [expected], f"wrong movers for {vertices(state)}->{attack}: {movers}")


def control_audit() -> dict:
    adj = decode_graph6(G6)
    n = len(adj)
    require(encode_graph6(adj) == G6, "graph6 round trip failed")
    edges = [
        (a, b) for a in range(n) for b in range(a + 1, n)
        if adj[a] >> b & 1
    ]
    require(len(edges) == 50, "edge count")
    gamma, ind_dom, alpha = parameter_values(adj)
    eternal, family = eternal_number(adj)
    theta, coloring = clique_cover_number(adj)
    require((gamma, ind_dom, alpha, eternal, theta) == (2, 2, 3, 3, 4), "parameters")
    require(len(family) == 200, "greatest triple family size")
    unrestricted_kernel, _, unrestricted_rounds = restricted_peeling(adj, 3, set())
    require(unrestricted_kernel == family and unrestricted_rounds == (), "unrestricted peeling")
    require(all(is_dominating(state, adj) for state in family), "family domination")
    require(
        all(
            legal_successors(state, attack, adj, family)
            for state in family
            for attack in range(n)
            if not (state >> attack & 1)
        ),
        "family closure",
    )

    root = mask_of(*ROOT)
    require(is_independent(root, adj), "root is not independent")
    require(root in family, "root absent from greatest family")
    for color in ROOT:
        require(adj[color] >> TARGET & 1, "target is not graph-adjacent to root")
        require((root ^ (1 << color)) | (1 << TARGET) in family, "root swap missing")
    ban_region = {
        vertex for vertex in range(n)
        if vertex != TARGET and not (adj[TARGET] >> vertex & 1)
    }
    require(ban_region == {3, 7, 9, 10}, "wrong ban region")

    expected_rounds = {
        0: (27, 49, 74, 46),
        5: (20, 30, 53, 74, 20),
        6: (20, 53, 90, 34),
    }
    expected_named_ranks = {
        0: (1, 2, 3, 2),
        5: (3, 2, 3, 4),
        6: (0, 0, 2, 2),
    }
    peelings = {}
    source = mask_of(V_COLOR, Q, T_ANCHOR)
    escape = mask_of(V_COLOR, Y, T_ANCHOR)
    first_state = mask_of(Q, W, 11)
    second_state = mask_of(R, Y, 12)
    for color in ROOT:
        fixed = root ^ (1 << color)
        banned = {fixed | (1 << b) for b in ban_region}
        kernel, ranks, rounds = restricted_peeling(adj, 3, banned)
        require(not kernel, f"color {color} kernel nonempty")
        require(rounds == expected_rounds[color], f"color {color} deletion rounds")
        require(
            tuple(ranks[state] for state in (source, escape, first_state, second_state))
            == expected_named_ranks[color],
            f"color {color} named ranks",
        )
        peelings[color] = (banned, kernel, ranks, rounds)

    banned, kernel, ranks, _ = peelings[SOURCE_COLOR]
    require(source in family and escape in family, "source or escape not retained")
    require(ranks[source] == ranks[escape] == 0, "rank-zero source/escape")
    require(
        attack_witnesses(source, 0, adj, banned, ranks, kernel) == [R],
        "source deletion witness",
    )
    require(
        attack_witnesses(escape, 0, adj, banned, ranks, kernel) == [W],
        "escape deletion witness",
    )

    terminal = mask_of(V_COLOR, T_ANCHOR, R)
    alt = mask_of(T_ANCHOR, Q, R)
    h_state = mask_of(V_COLOR, Q, R)
    lq = mask_of(W, T_ANCHOR, Q)
    lr = mask_of(W, T_ANCHOR, R)
    j_state = mask_of(V_COLOR, R, Y)
    secondary_root = mask_of(SOURCE_COLOR, T_ANCHOR, R)
    target_state = mask_of(V_COLOR, T_ANCHOR, TARGET)
    trapped_target_state = mask_of(W, T_ANCHOR, TARGET)
    require(
        all(state in family for state in (
            terminal,
            secondary_root,
            target_state,
            trapped_target_state,
            lq,
            lr,
        )),
        "corridor state absent",
    )
    require(not is_dominating(alt, adj), "C-168 alternate unexpectedly dominates")
    missed_alt = {
        z for z in range(n)
        if not any(z == guard or adj[guard] >> z & 1 for guard in vertices(alt))
    }
    require(missed_alt == {W}, "wrong C-168 missed set")
    require(W in ban_region, "w is not trapped")
    require(not is_dominating(h_state, adj), "C-171 H unexpectedly dominates")
    missed_h = {
        z for z in range(n)
        if not any(z == guard or adj[guard] >> z & 1 for guard in vertices(h_state))
    }
    require(missed_h == {Y}, "wrong C-171 missed set")
    require(Y not in ban_region, "y did not escape the ban")
    require(j_state in family, "second completion source absent")

    require(
        (source ^ (1 << Q)) | (1 << R) == terminal,
        "selected q-to-r corridor endpoint",
    )
    require(adj[Q] >> R & 1, "selected q-to-r corridor move is not physical")
    require(terminal in banned, "selected corridor endpoint is not banned")
    require(terminal in family, "selected q-to-r response not retained")
    unique_physical_response(target_state, W, V_COLOR, adj)
    require(
        (target_state ^ (1 << V_COLOR)) | (1 << W) == trapped_target_state,
        "wrong trapped target endpoint",
    )
    unique_physical_response(terminal, Y, T_ANCHOR, adj)

    first = common_nonneighbors(Q, W, adj)
    second = common_nonneighbors(R, Y, adj)
    require(first == {11} and second == {12}, "completion sets")
    require(is_clique(first, adj) and is_clique(second, adj), "completion clique")
    require(first.isdisjoint(second), "fans not separated")
    require(adj[W] >> Y & 1 and adj[Q] >> T_ANCHOR & 1, "separated-branch edges")
    require(all((d == T_ANCHOR or adj[T_ANCHOR] >> d & 1) for d in first), "first coverage")
    require(all(adj[V_COLOR] >> e & 1 for e in second), "second coverage")

    require(first_state in family and second_state in family, "completion state absent")
    unique_physical_response(lq, 11, T_ANCHOR, adj)
    unique_physical_response(j_state, 12, V_COLOR, adj)
    require(ranks[first_state] == ranks[second_state] == 2, "completion ranks")

    dominating_pairs = [
        vertices(mask)
        for mask in subsets_of_size(n, 2)
        if is_dominating(mask, adj)
    ]
    require(
        dominating_pairs == [(0, 8), (5, 12), (6, 10), (11, 12)],
        "dominating-pair list",
    )

    edge_text = "".join(f"{a} {b}\n" for a, b in edges)
    claimed_edges = [
        (low, high)
        for high in range(1, n)
        for low in range(high)
        if adj[low] >> high & 1
    ]
    claimed_edge_text = "".join(f"{a}-{b}\n" for a, b in claimed_edges)
    claimed_edge_hash = hashlib.sha256(claimed_edge_text.encode()).hexdigest()
    require(
        claimed_edge_hash
        == "511e0296f81a58a19134a4b118422e111fd5127889c8cfda159cec880cde7a58",
        "reported edge-list hash",
    )
    require(
        vertices(mask_of(*[v for v in range(n) if adj[11] >> v & 1]))
        == (0, 1, 4, 5, 7, 8, 10),
        "vertex 11 neighborhood",
    )
    require(
        vertices(mask_of(*[v for v in range(n) if adj[12] >> v & 1]))
        == (0, 2, 3, 4, 5, 6, 7, 8, 9),
        "vertex 12 neighborhood",
    )
    return {
        "graph6": G6,
        "graph6_sha256": hashlib.sha256(G6.encode()).hexdigest(),
        "edge_list_sha256_claimed_format": claimed_edge_hash,
        "edge_list_sha256_clean_format": hashlib.sha256(edge_text.encode()).hexdigest(),
        "n": n,
        "m": len(edges),
        "parameters": [gamma, ind_dom, alpha, eternal, theta],
        "theta_coloring": coloring,
        "greatest_family_size": len(family),
        "ban_region": sorted(ban_region),
        "restricted_rounds": {str(k): list(v) for k, v in expected_rounds.items()},
        "named_ranks_by_color": {
            str(k): list(v) for k, v in expected_named_ranks.items()
        },
        "source_escape_ranks": [ranks[source], ranks[escape]],
        "completion_sets": [sorted(first), sorted(second)],
        "completion_ranks": [ranks[first_state], ranks[second_state]],
        "dominating_pairs": [list(pair) for pair in dominating_pairs],
        "missed_alt": sorted(missed_alt),
        "missed_h": sorted(missed_h),
    }


def rank_floor_exhaustive() -> dict:
    """Audit all labeled graphs, k, and nonempty k-configuration bans for n<=4.

    It suffices to inspect the literal greatest family: every state belonging
    to any eternal family belongs to that union/greatest fixed point.
    """
    graph_count = 0
    ban_count = 0
    checked_states = 0
    for n in range(1, 5):
        pairs = list(itertools.combinations(range(n), 2))
        for code in range(1 << len(pairs)):
            adj = [0] * n
            for index, (a, b) in enumerate(pairs):
                if code >> index & 1:
                    adj[a] |= 1 << b
                    adj[b] |= 1 << a
            graph_count += 1
            for k in range(1, n + 1):
                configs = list(subsets_of_size(n, k))
                family = greatest_family(adj, k)
                if not family:
                    continue
                for ban_code in range(1, 1 << len(configs)):
                    banned = {
                        state for index, state in enumerate(configs)
                        if ban_code >> index & 1
                    }
                    kernel, ranks, _ = restricted_peeling(adj, k, banned)
                    ban_count += 1
                    for state in family:
                        if state not in ranks:
                            continue
                        distance = min(
                            k - (state & banned_state).bit_count()
                            for banned_state in banned
                        )
                        require(
                            ranks[state] >= distance - 1,
                            (
                                f"rank floor failed n={n}, graph={code}, k={k}, "
                                f"state={vertices(state)}, rank={ranks[state]}, "
                                f"distance={distance}"
                            ),
                        )
                        checked_states += 1
    return {
        "orders": [1, 2, 3, 4],
        "labeled_graphs": graph_count,
        "nonempty_bans": ban_count,
        "finite_rank_states_checked": checked_states,
        "status": "PASS",
    }


def main() -> None:
    result = {
        "control": control_audit(),
        "rank_floor_exhaustive": rank_floor_exhaustive(),
        "verdict": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
