#!/usr/bin/env python3
"""Clean-room audit of the rank-zero anchor-restoration control.

This file intentionally imports no campaign implementation.  Graphs and
configurations are represented by integer masks, whereas the candidate
checker uses frozensets.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json


GRAPH6 = "OYifur}UO]}iTij]tpo]v"
N = 16
ROOT_VERTICES = (0, 1, 10)
TARGET = 6
BAN_COLOR = 0
EXPECTED_PARTITION = (
    (0, 2, 5, 11, 14),
    (1, 3, 6, 8, 12),
    (4, 7, 9, 10, 13, 15),
)


def vertices(mask: int) -> tuple[int, ...]:
    return tuple(index for index in range(N) if mask & (1 << index))


def make_mask(items: tuple[int, ...] | list[int] | set[int]) -> int:
    answer = 0
    for item in items:
        answer |= 1 << item
    return answer


def graph6_decode(record: str) -> tuple[int, ...]:
    """Decode the graph6 small-order form into open-neighborhood masks."""

    raw = record.encode("ascii")
    if not raw or raw[0] != N + 63:
        raise AssertionError("unexpected graph6 order header")
    payload: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        if value < 0 or value > 63:
            raise AssertionError("invalid graph6 payload")
        payload.extend((value >> bit) & 1 for bit in (5, 4, 3, 2, 1, 0))

    needed = N * (N - 1) // 2
    if len(payload) < needed or any(payload[needed:]):
        raise AssertionError("invalid graph6 padding")

    adjacency = [0] * N
    cursor = 0
    for right in range(1, N):
        for left in range(right):
            if payload[cursor]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1

    for vertex, neighborhood in enumerate(adjacency):
        if neighborhood & (1 << vertex):
            raise AssertionError("loop in decoded graph")
        for neighbor in vertices(neighborhood):
            if not adjacency[neighbor] & (1 << vertex):
                raise AssertionError("asymmetric decoded adjacency")
    return tuple(adjacency)


def graph6_encode(adjacency: tuple[int, ...]) -> str:
    bits: list[int] = []
    for right in range(1, N):
        for left in range(right):
            bits.append(int(bool(adjacency[left] & (1 << right))))
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(N + 63) + "".join(payload)


def k_masks(k: int) -> tuple[int, ...]:
    return tuple(make_mask(list(choice)) for choice in combinations(range(N), k))


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    work = state
    while work:
        bit = work & -work
        guard = bit.bit_length() - 1
        covered |= adjacency[guard]
        work ^= bit
    return covered == (1 << N) - 1


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    work = state
    while work:
        bit = work & -work
        vertex = bit.bit_length() - 1
        if adjacency[vertex] & (state ^ bit):
            return False
        work ^= bit
    return True


def successors(
    adjacency: tuple[int, ...], state: int, attacked: int
) -> tuple[int, ...]:
    attacked_bit = 1 << attacked
    if state & attacked_bit:
        raise AssertionError("occupied-vertex attack")
    result = []
    work = state & adjacency[attacked]
    while work:
        mover_bit = work & -work
        result.append((state ^ mover_bit) | attacked_bit)
        work ^= mover_bit
    return tuple(result)


def greatest_kernel(
    adjacency: tuple[int, ...], k: int, banned: frozenset[int] = frozenset()
) -> tuple[frozenset[int], dict[int, int], frozenset[int]]:
    initial = frozenset(
        state
        for state in k_masks(k)
        if state not in banned and dominates(adjacency, state)
    )
    active = set(initial)
    deletion_rank: dict[int, int] = {}
    round_index = 0
    while True:
        doomed = set()
        for state in active:
            for attacked in range(N):
                if state & (1 << attacked):
                    continue
                if not any(
                    successor in active
                    for successor in successors(adjacency, state, attacked)
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return frozenset(active), deletion_rank, initial
        for state in doomed:
            deletion_rank[state] = round_index
        active.difference_update(doomed)
        round_index += 1


def response_palette(
    adjacency: tuple[int, ...], family: frozenset[int], root: int, point: int
) -> tuple[int, ...]:
    answer = []
    for color in vertices(root):
        color_bit = 1 << color
        if (
            adjacency[color] & (1 << point)
            and ((root ^ color_bit) | (1 << point)) in family
        ):
            answer.append(color)
    return tuple(answer)


def clique(adjacency: tuple[int, ...], part: int) -> bool:
    work = part
    while work:
        bit = work & -work
        vertex = bit.bit_length() - 1
        if (part ^ bit) & ~adjacency[vertex]:
            return False
        work ^= bit
    return True


def exact_static_parameters(
    adjacency: tuple[int, ...],
) -> tuple[int, int, int, int]:
    dominating_by_size = {}
    independent_by_size = {}
    for size in range(N + 1):
        states = k_masks(size)
        dominating_by_size[size] = tuple(
            state for state in states if dominates(adjacency, state)
        )
        independent_by_size[size] = tuple(
            state for state in states if independent(adjacency, state)
        )

    gamma = next(size for size in range(N + 1) if dominating_by_size[size])
    alpha = max(size for size in range(N + 1) if independent_by_size[size])
    independent_domination = next(
        size
        for size in range(N + 1)
        if any(state in set(dominating_by_size[size]) for state in independent_by_size[size])
    )

    partition_masks = tuple(make_mask(list(part)) for part in EXPECTED_PARTITION)
    if (
        make_mask([vertex for part in EXPECTED_PARTITION for vertex in part])
        != (1 << N) - 1
        or sum(part.bit_count() for part in partition_masks) != N
        or not all(clique(adjacency, part) for part in partition_masks)
    ):
        raise AssertionError("claimed clique partition is invalid")

    # Every independent set meets each clique in at most one vertex.  The
    # independently computed alpha=3 gives theta>=3, and the partition gives
    # theta<=3, so this is an exact clique-cover computation.
    theta = len(partition_masks)
    if alpha != theta:
        raise AssertionError("alpha lower bound and clique cover do not meet")
    return gamma, independent_domination, alpha, theta


def connected(adjacency: tuple[int, ...]) -> bool:
    reached = 1
    frontier = 1
    while frontier:
        bit = frontier & -frontier
        vertex = bit.bit_length() - 1
        frontier ^= bit
        new = adjacency[vertex] & ~reached
        reached |= new
        frontier |= new
    return reached == (1 << N) - 1


def edge_data(adjacency: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], str]:
    edges = tuple(
        (left, right)
        for left in range(N)
        for right in range(left + 1, N)
        if adjacency[left] & (1 << right)
    )
    serialization = ";".join(f"{left}-{right}" for left, right in edges)
    return edges, sha256(serialization.encode("ascii")).hexdigest()


def verify_row(
    *,
    adjacency: tuple[int, ...],
    family: frozenset[int],
    ban: frozenset[int],
    ranks: dict[int, int],
    root: int,
    terminal_palette: tuple[int, ...],
    label: str,
    a: int,
    c: int,
    r: int,
    q: int,
) -> dict[str, object]:
    u = BAN_COLOR
    state = make_mask([c, r, q])
    endpoint = make_mask([a, c, r])
    alternate = make_mask([a, c, q])
    all_named = {u, a, c, r, q, TARGET}
    if len(all_named) != 6:
        raise AssertionError(f"{label}: collision among named vertices")
    if make_mask([u, a, c]) != root:
        raise AssertionError(f"{label}: root roles inconsistent")
    if state not in family or state in ban or ranks.get(state) != 0:
        raise AssertionError(f"{label}: predecessor is not retained, unbanned rank zero")
    if state & (1 << a):
        raise AssertionError(f"{label}: attacked anchor is occupied")
    if endpoint not in family or endpoint not in ban:
        raise AssertionError(f"{label}: selected endpoint is not retained and banned")
    if not adjacency[q] & (1 << a):
        raise AssertionError(f"{label}: selected move lacks its graph edge")
    if (state ^ (1 << q)) | (1 << a) != endpoint:
        raise AssertionError(f"{label}: selected move has wrong endpoint")
    if response_palette(adjacency, family, root, r) != terminal_palette:
        raise AssertionError(f"{label}: terminal palette mismatch")
    if u not in terminal_palette or len(terminal_palette) < 2:
        raise AssertionError(f"{label}: terminal palette is not nonsingleton with u")

    physical_movers = tuple(vertices(state & adjacency[a]))
    live_unbanned = tuple(
        successor
        for successor in successors(adjacency, state, a)
        if successor not in ban and dominates(adjacency, successor)
    )
    if live_unbanned:
        raise AssertionError(f"{label}: named attack does not witness rank-zero deletion")

    return {
        "roles": {"u": u, "a": a, "c": c, "r": r, "q": q},
        "predecessor": vertices(state),
        "attack": a,
        "physical_movers": physical_movers,
        "selected_endpoint": vertices(endpoint),
        "terminal_palette": terminal_palette,
        "alternate": vertices(alternate),
        "alternate_move_edge": bool(adjacency[r] & (1 << a)),
        "alternate_banned": alternate in ban,
        "alternate_dominates": dominates(adjacency, alternate),
        "alternate_retained": alternate in family,
        "rank_zero_unbanned_dominating_successors": len(live_unbanned),
    }


def main() -> dict[str, object]:
    adjacency = graph6_decode(GRAPH6)
    if graph6_encode(adjacency) != GRAPH6:
        raise AssertionError("graph6 round trip failed")
    edges, edge_sha = edge_data(adjacency)
    if len(edges) != 71 or not connected(adjacency):
        raise AssertionError("wrong control graph order/size/connectivity")

    gamma, indep_dom, alpha, theta = exact_static_parameters(adjacency)
    unrestricted = {}
    unrestricted_ranks = {}
    for k in (1, 2, 3):
        kernel, ranks, initial = greatest_kernel(adjacency, k)
        unrestricted[k] = kernel
        unrestricted_ranks[k] = ranks
        if not all(dominates(adjacency, state) for state in kernel):
            raise AssertionError("kernel retained a nondominating state")
        if not kernel.issubset(initial):
            raise AssertionError("kernel escaped its initial universe")
    gamma_infinity = next(k for k in (1, 2, 3) if unrestricted[k])
    if (gamma, indep_dom, alpha, gamma_infinity, theta) != (3, 3, 3, 3, 3):
        raise AssertionError("parameter tuple mismatch")

    family = unrestricted[3]
    obligation_count = 0
    response_edge_count = 0
    for state in family:
        for attacked in range(N):
            if state & (1 << attacked):
                continue
            obligation_count += 1
            answers = tuple(
                successor
                for successor in successors(adjacency, state, attacked)
                if successor in family
            )
            if not answers:
                raise AssertionError("greatest family has an unanswered attack")
            response_edge_count += len(answers)

    root = make_mask(list(ROOT_VERTICES))
    if not independent(adjacency, root) or root not in family:
        raise AssertionError("root is not an independent retained triple")
    full_palette = response_palette(adjacency, family, root, TARGET)
    if full_palette != ROOT_VERTICES:
        raise AssertionError("target is not full")

    complement_link = tuple(
        vertex
        for vertex in range(N)
        if vertex != TARGET and not adjacency[TARGET] & (1 << vertex)
    )
    if complement_link != (5, 7, 9, 11, 13):
        raise AssertionError("complement-link set mismatch")

    per_color = {}
    color_zero_ranks = {}
    color_zero_initial = frozenset()
    color_zero_ban = frozenset()
    for color in ROOT_VERTICES:
        ban = frozenset(
            (root ^ (1 << color)) | (1 << point)
            for point in complement_link
        )
        kernel, ranks, initial = greatest_kernel(adjacency, 3, ban)
        per_color[str(color)] = len(kernel)
        if color == BAN_COLOR:
            color_zero_ranks = ranks
            color_zero_initial = initial
            color_zero_ban = ban
    if per_color != {"0": 0, "1": 150, "10": 0}:
        raise AssertionError("restricted kernel sizes mismatch")
    rank_counts = {
        str(rank): count
        for rank, count in sorted(Counter(color_zero_ranks.values()).items())
    }
    if rank_counts != {"0": 28, "1": 81, "2": 132, "3": 62}:
        raise AssertionError("restricted rank distribution mismatch")
    if len(color_zero_initial) != sum(rank_counts.values()):
        raise AssertionError("restricted peeling did not account for its universe")

    palette_5 = response_palette(adjacency, family, root, 5)
    palette_7 = response_palette(adjacency, family, root, 7)
    if palette_5 != (0, 10) or palette_7 != (1, 10):
        raise AssertionError("named root palettes mismatch")

    attacked_row = verify_row(
        adjacency=adjacency,
        family=family,
        ban=color_zero_ban,
        ranks=color_zero_ranks,
        root=root,
        terminal_palette=palette_5,
        label="attacked-secondary",
        a=10,
        c=1,
        r=5,
        q=7,
    )
    shared_row = verify_row(
        adjacency=adjacency,
        family=family,
        ban=color_zero_ban,
        ranks=color_zero_ranks,
        root=root,
        terminal_palette=palette_5,
        label="shared-secondary",
        a=1,
        c=10,
        r=5,
        q=7,
    )

    if 10 not in palette_5 or attacked_row["physical_movers"] != (5, 7):
        raise AssertionError("attacked-secondary row is not realized")
    if (
        1 in palette_5
        or 10 not in palette_5
        or 1 not in palette_7
        or shared_row["physical_movers"] != (7,)
    ):
        raise AssertionError("shared-secondary restoration row is not realized")

    common_alternate = make_mask([1, 7, 10])
    if (
        attacked_row["alternate"] != vertices(common_alternate)
        or shared_row["alternate"] != vertices(common_alternate)
        or not dominates(adjacency, common_alternate)
        or common_alternate not in color_zero_ban
        or common_alternate in family
    ):
        raise AssertionError("sharp banned alternate status mismatch")
    if bool(7 in complement_link) != bool(common_alternate in color_zero_ban):
        raise AssertionError("ban iff q lies in the complement link failed")

    # This is the literal arbitrary-state restoration check for the shared row:
    # S-T={0,1}, T-S={5,7}, and the two outside palettes cover both anchors.
    shared_predecessor = make_mask([5, 7, 10])
    missing_root = root & ~shared_predecessor
    outside = shared_predecessor & ~root
    outside_palette_union = make_mask(
        [
            color
            for point in vertices(outside)
            for color in response_palette(adjacency, family, root, point)
        ]
    )
    if vertices(missing_root) != (0, 1) or vertices(outside) != (5, 7):
        raise AssertionError("restoration set differences are wrong")
    if missing_root & ~outside_palette_union:
        raise AssertionError("arbitrary-state restoration fails on shared row")

    unrestricted_alt_rank = unrestricted_ranks[3].get(common_alternate)
    if unrestricted_alt_rank is None:
        raise AssertionError("omitted alternate was not deleted from greatest family")

    return {
        "schema": "full-list-anchor-restoration-hostile-clean-v1",
        "candidate_commit": "7a0c7a86",
        "graph": {
            "graph6": GRAPH6,
            "graph6_ascii_sha256": sha256(GRAPH6.encode("ascii")).hexdigest(),
            "roundtrip": True,
            "order": N,
            "size": len(edges),
            "connected": True,
            "edge_list_sha256": edge_sha,
        },
        "parameters": {
            "gamma": gamma,
            "i": indep_dom,
            "alpha": alpha,
            "gamma_infinity": gamma_infinity,
            "theta": theta,
        },
        "unrestricted_kernel_sizes": {
            str(k): len(unrestricted[k]) for k in (1, 2, 3)
        },
        "greatest_eternal_triple_family": {
            "states": len(family),
            "unoccupied_attack_obligations": obligation_count,
            "retained_response_edges": response_edge_count,
        },
        "full_list_setup": {
            "root": ROOT_VERTICES,
            "target": TARGET,
            "target_palette": full_palette,
            "complement_link": complement_link,
            "color_zero_restricted_initial_states": len(color_zero_initial),
            "color_zero_restricted_kernel_states": per_color["0"],
            "color_zero_rank_counts": rank_counts,
            "restricted_kernel_sizes": per_color,
            "terminal_palette": palette_5,
            "mover_palette": palette_7,
        },
        "attacked_secondary_row": attacked_row,
        "shared_secondary_row": shared_row,
        "restoration_audit": {
            "missing_root": vertices(missing_root),
            "outside_vertices": vertices(outside),
            "outside_palette_union": vertices(outside_palette_union),
        },
        "common_alternate": {
            "state": vertices(common_alternate),
            "dominates": True,
            "banned": True,
            "retained": False,
            "unrestricted_deletion_rank": unrestricted_alt_rank,
        },
        "verdict": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
