#!/usr/bin/env python3
"""Independent replay of the full-list three-color coupling controls.

This checker deliberately imports no campaign implementation.  Graphs use
sets of neighbors and guard configurations use sorted tuples, unlike the
candidate's imported packed-bitset transition core.
"""

from __future__ import annotations

import itertools
import json
import math


EQUALITY_GRAPH6 = "OYifur}UO]}iTij]tpo]v"
MMV_GRAPH6 = "IEhbtj{ro"


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    require(record and ord(record[0]) < 126, "short graph6 required")
    order = ord(record[0]) - 63
    require(0 <= order <= 62, ("bad order", order))
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, ("bad graph6 byte", character))
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = math.comb(order, 2)
    require(len(bits) == 6 * ((needed + 5) // 6), "noncanonical payload length")
    require(not any(bits[needed:]), "nonzero graph6 padding")
    neighbors = [set() for _ in range(order)]
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                neighbors[low].add(high)
                neighbors[high].add(low)
            cursor += 1
    adjacency = tuple(frozenset(row) for row in neighbors)
    require(
        all(vertex not in adjacency[vertex] for vertex in range(order)),
        "loop",
    )
    require(
        all(
            (second in adjacency[first]) == (first in adjacency[second])
            for first in range(order)
            for second in range(order)
        ),
        "asymmetric adjacency",
    )
    return adjacency


def state(vertices: tuple[int, ...] | list[int] | set[int]) -> tuple[int, ...]:
    result = tuple(sorted(vertices))
    require(len(result) == len(set(result)), ("repeated guard", result))
    return result


def dominates(
    adjacency: tuple[frozenset[int], ...],
    guards: tuple[int, ...],
) -> bool:
    occupied = set(guards)
    return all(
        vertex in occupied
        or any(vertex in adjacency[guard] for guard in guards)
        for vertex in range(len(adjacency))
    )


def missed(
    adjacency: tuple[frozenset[int], ...],
    guards: tuple[int, ...],
) -> tuple[int, ...]:
    occupied = set(guards)
    return tuple(
        vertex
        for vertex in range(len(adjacency))
        if vertex not in occupied
        and not any(vertex in adjacency[guard] for guard in guards)
    )


def independent(
    adjacency: tuple[frozenset[int], ...],
    vertices: tuple[int, ...],
) -> bool:
    return all(
        second not in adjacency[first]
        for first, second in itertools.combinations(vertices, 2)
    )


def successors(
    adjacency: tuple[frozenset[int], ...],
    guards: tuple[int, ...],
    attacked: int,
) -> tuple[tuple[int, tuple[int, ...]], ...]:
    require(attacked not in guards, ("occupied attack", guards, attacked))
    return tuple(
        (
            guard,
            state((set(guards) - {guard}) | {attacked}),
        )
        for guard in guards
        if attacked in adjacency[guard]
    )


def greatest_family(
    adjacency: tuple[frozenset[int], ...],
    guard_count: int,
    banned: frozenset[tuple[int, ...]] = frozenset(),
) -> tuple[
    frozenset[tuple[int, ...]],
    dict[tuple[int, ...], int],
    tuple[int, ...],
]:
    active = {
        guards
        for guards in itertools.combinations(range(len(adjacency)), guard_count)
        if guards not in banned and dominates(adjacency, guards)
    }
    ranks: dict[tuple[int, ...], int] = {}
    round_sizes: list[int] = []
    rank = 0
    while True:
        deleted = {
            guards
            for guards in active
            if any(
                not any(
                    endpoint in active
                    for _, endpoint in successors(adjacency, guards, attacked)
                )
                for attacked in range(len(adjacency))
                if attacked not in guards
            )
        }
        if not deleted:
            return frozenset(active), ranks, tuple(round_sizes)
        for guards in deleted:
            ranks[guards] = rank
        round_sizes.append(len(deleted))
        active.difference_update(deleted)
        rank += 1


def deletion_witnesses(
    adjacency: tuple[frozenset[int], ...],
    guards: tuple[int, ...],
    banned: frozenset[tuple[int, ...]],
    ranks: dict[tuple[int, ...], int],
) -> tuple[int, ...]:
    current = ranks[guards]
    witnesses: list[int] = []
    for attacked in range(len(adjacency)):
        if attacked in guards:
            continue
        eligible = [
            endpoint
            for _, endpoint in successors(adjacency, guards, attacked)
            if endpoint not in banned and dominates(adjacency, endpoint)
        ]
        if all(endpoint in ranks and ranks[endpoint] < current for endpoint in eligible):
            witnesses.append(attacked)
    return tuple(witnesses)


def exact_gamma(adjacency: tuple[frozenset[int], ...]) -> int:
    for size in range(1, len(adjacency) + 1):
        if any(
            dominates(adjacency, guards)
            for guards in itertools.combinations(range(len(adjacency)), size)
        ):
            return size
    raise AssertionError("no dominating set")


def exact_alpha(adjacency: tuple[frozenset[int], ...]) -> int:
    for size in range(len(adjacency), 0, -1):
        if any(
            independent(adjacency, vertices)
            for vertices in itertools.combinations(range(len(adjacency)), size)
        ):
            return size
    return 0


def exact_independent_domination(
    adjacency: tuple[frozenset[int], ...],
) -> int:
    for size in range(1, len(adjacency) + 1):
        if any(
            independent(adjacency, vertices)
            and dominates(adjacency, vertices)
            for vertices in itertools.combinations(range(len(adjacency)), size)
        ):
            return size
    raise AssertionError("no maximal independent set")


def complement(
    adjacency: tuple[frozenset[int], ...],
) -> tuple[frozenset[int], ...]:
    universe = set(range(len(adjacency)))
    return tuple(
        frozenset(universe - {vertex} - set(adjacency[vertex]))
        for vertex in range(len(adjacency))
    )


def colorable(
    adjacency: tuple[frozenset[int], ...],
    color_count: int,
) -> bool:
    colors = [-1] * len(adjacency)

    def extend(colored: int) -> bool:
        if colored == len(adjacency):
            return True
        candidates = [v for v, color in enumerate(colors) if color < 0]
        vertex = max(
            candidates,
            key=lambda v: (
                len({colors[w] for w in adjacency[v] if colors[w] >= 0}),
                len(adjacency[v]),
                -v,
            ),
        )
        forbidden = {colors[w] for w in adjacency[vertex] if colors[w] >= 0}
        for color in range(color_count):
            if color in forbidden:
                continue
            colors[vertex] = color
            if extend(colored + 1):
                return True
            colors[vertex] = -1
        return False

    return extend(0)


def exact_chromatic(adjacency: tuple[frozenset[int], ...]) -> int:
    for color_count in range(1, len(adjacency) + 1):
        if colorable(adjacency, color_count):
            return color_count
    raise AssertionError("no coloring")


def exact_eternal(adjacency: tuple[frozenset[int], ...]) -> int:
    for guard_count in range(1, len(adjacency) + 1):
        kernel, _, _ = greatest_family(adjacency, guard_count)
        if kernel:
            return guard_count
    raise AssertionError("no eternal family")


def parameters(adjacency: tuple[frozenset[int], ...]) -> dict[str, int]:
    return {
        "gamma": exact_gamma(adjacency),
        "i": exact_independent_domination(adjacency),
        "alpha": exact_alpha(adjacency),
        "gamma_infinity": exact_eternal(adjacency),
        "theta": exact_chromatic(complement(adjacency)),
    }


def complement_neighbors(
    adjacency: tuple[frozenset[int], ...],
    target: int,
) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(adjacency))
        if vertex != target and vertex not in adjacency[target]
    )


def color_ban(
    adjacency: tuple[frozenset[int], ...],
    root: tuple[int, int, int],
    target: int,
    color: int,
) -> frozenset[tuple[int, ...]]:
    fixed = set(root) - {color}
    return frozenset(
        state(fixed | {vertex})
        for vertex in complement_neighbors(adjacency, target)
    )


def palette(
    adjacency: tuple[frozenset[int], ...],
    greatest: frozenset[tuple[int, ...]],
    root: tuple[int, int, int],
    vertex: int,
) -> tuple[int, ...]:
    return tuple(
        color
        for color in root
        if vertex in adjacency[color]
        and state((set(root) - {color}) | {vertex}) in greatest
    )


def audit_transfer_row(
    adjacency: tuple[frozenset[int], ...],
    greatest: frozenset[tuple[int, ...]],
    root: tuple[int, int, int],
    target: int,
    *,
    u: int,
    v: int,
    t: int,
    q: int,
    r: int,
    w: int,
) -> dict[str, object]:
    require(set(root) == {u, v, t}, ("bad root labels", u, v, t))
    require(
        len({u, v, t, q, r, w, target}) == 7,
        ("row collision", u, v, t, q, r, w, target),
    )
    predecessor = state((v, t, q))
    terminal = state((v, t, r))
    secondary_root = state((u, t, r))
    alternate = state((t, q, r))
    witness_q = state((w, t, q))
    witness_r = state((w, t, r))
    first_endpoint = state((u, t, q))
    second_endpoint = state((u, t, w))

    banned = color_ban(adjacency, root, target, u)
    kernel, ranks, rounds = greatest_family(adjacency, 3, banned)
    require(ranks.get(predecessor) == 0, ("not rank zero", u, ranks.get(predecessor)))
    require(
        r in deletion_witnesses(adjacency, predecessor, banned, ranks),
        ("wrong deletion witness", u),
    )
    require(r in complement_neighbors(adjacency, target), ("terminal outside B", u))
    require(q not in complement_neighbors(adjacency, target), ("mover inside B", u))
    require(
        all(item in greatest for item in (
            predecessor,
            terminal,
            secondary_root,
            witness_q,
            witness_r,
            second_endpoint,
        )),
        ("missing retained ladder state", u),
    )
    require(missed(adjacency, alternate) == (w,), ("wrong missed set", u))
    require(not dominates(adjacency, alternate), ("alternate dominates", u))

    first_responders = tuple(
        guard for guard, _ in successors(adjacency, predecessor, w)
    )
    second_responders = tuple(
        guard for guard, _ in successors(adjacency, secondary_root, w)
    )
    require(first_responders == (v,), ("first attack not unique", u, first_responders))
    require(second_responders == (u,), ("second attack not unique", u, second_responders))
    require(
        successors(adjacency, predecessor, w)[0][1] == witness_q,
        ("wrong first ladder endpoint", u),
    )
    require(
        successors(adjacency, secondary_root, w)[0][1] == witness_r,
        ("wrong second ladder endpoint", u),
    )

    transfer_moves = successors(adjacency, witness_q, u)
    require(
        tuple(guard for guard, _ in transfer_moves) == tuple(sorted((w, q))),
        ("wrong transfer responders", u, transfer_moves),
    )
    transfer_endpoints = {guard: endpoint for guard, endpoint in transfer_moves}
    require(transfer_endpoints[w] == first_endpoint, ("wrong w endpoint", u))
    require(transfer_endpoints[q] == second_endpoint, ("wrong q endpoint", u))
    require(first_endpoint not in greatest, ("control first endpoint retained", u))
    require(second_endpoint in greatest, ("control second endpoint absent", u))

    palette_q = palette(adjacency, greatest, root, q)
    palette_r = palette(adjacency, greatest, root, r)
    palette_w = palette(adjacency, greatest, root, w)
    require(u in palette_q, ("primary missing at mover", u))
    require({u, v} <= set(palette_r), ("secondary terminal color missing", u))
    require(v not in palette_q, ("secondary already at mover", u))
    require(v in palette_w, ("secondary not transferred to witness", u))

    return {
        "color": u,
        "secondary": v,
        "mover": q,
        "terminal": r,
        "witness": w,
        "kernel_size": len(kernel),
        "rounds": list(rounds),
        "predecessor_rank": ranks[predecessor],
        "palette_q": list(palette_q),
        "palette_r": list(palette_r),
        "palette_w": list(palette_w),
        "qv_edge": v in adjacency[q],
        "missed_by_alternate": list(missed(adjacency, alternate)),
    }


def equality_control() -> dict[str, object]:
    adjacency = decode_graph6(EQUALITY_GRAPH6)
    root = (0, 1, 10)
    target = 6
    require(independent(adjacency, root), "equality root is not independent")
    greatest, _, unrestricted_rounds = greatest_family(adjacency, 3)
    require(state(root) in greatest, "equality root absent")
    require(palette(adjacency, greatest, root, target) == root, "target not full")
    result_parameters = parameters(adjacency)
    require(
        result_parameters
        == {"gamma": 3, "i": 3, "alpha": 3, "gamma_infinity": 3, "theta": 3},
        ("wrong equality parameters", result_parameters),
    )
    require(len(greatest) == 304, ("wrong equality family size", len(greatest)))

    kernel_records: dict[str, dict[str, object]] = {}
    for color in root:
        banned = color_ban(adjacency, root, target, color)
        kernel, ranks, rounds = greatest_family(adjacency, 3, banned)
        kernel_records[str(color)] = {
            "size": len(kernel),
            "rounds": list(rounds),
            "rank_count": len(ranks),
        }
    require(
        {color: record["size"] for color, record in kernel_records.items()}
        == {"0": 0, "1": 150, "10": 0},
        ("wrong equality kernels", kernel_records),
    )

    row_records = [
        audit_transfer_row(
            adjacency, greatest, root, target,
            u=0, v=1, t=10, q=14, r=11, w=8,
        ),
        audit_transfer_row(
            adjacency, greatest, root, target,
            u=10, v=0, t=1, q=12, r=5, w=4,
        ),
    ]

    safe_ban = color_ban(adjacency, root, target, 1)
    safe_kernel, _, _ = greatest_family(adjacency, 3, safe_ban)
    safe_predecessor = state((0, 3, 10))
    safe_terminal = state((0, 7, 10))
    safe_alternate = state((0, 3, 7))
    require(
        all(item in safe_kernel for item in (safe_predecessor, safe_alternate)),
        "safe predecessor or alternate does not survive",
    )
    require(safe_terminal in greatest, "safe terminal absent from greatest family")
    require(safe_terminal in safe_ban, "safe terminal should be banned")
    require(dominates(adjacency, safe_alternate), "safe alternate does not dominate")

    terminal_palettes = {
        str(vertex): list(palette(adjacency, greatest, root, vertex))
        for vertex in (11, 7, 5)
    }
    require(
        terminal_palettes
        == {"11": [0, 1], "7": [1, 10], "5": [0, 10]},
        ("wrong terminal palette cycle", terminal_palettes),
    )
    return {
        "graph6": EQUALITY_GRAPH6,
        "order": len(adjacency),
        "size": sum(map(len, adjacency)) // 2,
        "parameters": result_parameters,
        "greatest_family_size": len(greatest),
        "unrestricted_deletion_rounds": list(unrestricted_rounds),
        "kernels": kernel_records,
        "terminal_palettes": terminal_palettes,
        "transfer_rows": row_records,
        "safe_color": 1,
        "safe_secondary_alternate": list(safe_alternate),
    }


def gamma_two_control() -> dict[str, object]:
    adjacency = decode_graph6(MMV_GRAPH6)
    root = (0, 1, 2)
    target = 8
    require(independent(adjacency, root), "MMV root is not independent")
    greatest, _, unrestricted_rounds = greatest_family(adjacency, 3)
    require(state(root) in greatest, "MMV root absent")
    require(palette(adjacency, greatest, root, target) == root, "MMV target not full")
    result_parameters = parameters(adjacency)
    require(
        result_parameters
        == {"gamma": 2, "i": 2, "alpha": 3, "gamma_infinity": 3, "theta": 4},
        ("wrong MMV parameters", result_parameters),
    )
    require(len(greatest) == 86, ("wrong MMV greatest family", len(greatest)))

    records = [
        audit_transfer_row(
            adjacency, greatest, root, target,
            u=0, v=1, t=2, q=4, r=9, w=3,
        ),
        audit_transfer_row(
            adjacency, greatest, root, target,
            u=1, v=2, t=0, q=3, r=6, w=5,
        ),
        audit_transfer_row(
            adjacency, greatest, root, target,
            u=2, v=0, t=1, q=5, r=7, w=4,
        ),
    ]
    require(
        [record["kernel_size"] for record in records] == [0, 0, 0],
        ("MMV kernels survive", records),
    )
    require(
        [record["witness"] for record in records]
        == [records[1]["mover"], records[2]["mover"], records[0]["mover"]],
        "MMV witness-mover cycle fails",
    )
    dominating_pairs = [
        list(pair)
        for pair in itertools.combinations(range(len(adjacency)), 2)
        if dominates(adjacency, pair)
    ]
    require(dominating_pairs == [[8, 9]], ("wrong dominating pairs", dominating_pairs))
    return {
        "graph6": MMV_GRAPH6,
        "order": len(adjacency),
        "size": sum(map(len, adjacency)) // 2,
        "parameters": result_parameters,
        "greatest_family_size": len(greatest),
        "unrestricted_deletion_rounds": list(unrestricted_rounds),
        "transfer_rows": records,
        "dominating_pairs": dominating_pairs,
    }


def color_map_audit() -> dict[str, object]:
    maps = [
        images
        for images in itertools.product(range(3), repeat=3)
        if all(images[color] != color for color in range(3))
    ]
    three_cycles = [
        images
        for images in maps
        if images[images[images[0]]] == 0
        and images[images[0]] != 0
    ]
    two_cycles = [images for images in maps if images not in three_cycles]
    require(len(maps) == 8, ("wrong map count", maps))
    require(len(three_cycles) == 2, ("wrong 3-cycle count", three_cycles))
    require(len(two_cycles) == 6, ("wrong 2-cycle count", two_cycles))
    require(
        all(any(images[images[color]] == color for color in range(3)) for images in two_cycles),
        ("not every remaining map has a 2-cycle", two_cycles),
    )
    return {
        "fixed_point_free_maps": len(maps),
        "directed_3_cycles": len(three_cycles),
        "two_cycle_with_tail": len(two_cycles),
        "labeled_maps": [list(images) for images in maps],
    }


def formula_count_audit() -> list[dict[str, int]]:
    records: list[dict[str, int]] = []
    for order in range(10, 17):
        pairs = math.comb(order, 2)
        triples = math.comb(order, 3)
        variables = (
            pairs
            + triples
            + pairs * (order - 2)
            + 3 * triples * (order - 3)
        )
        clauses = (
            67
            + math.comb(order, 4)
            + pairs * (3 * (order - 2) + 1)
            + 11 * triples * (order - 3)
        )
        records.append({
            "order": order,
            "variables": variables,
            "clauses": clauses,
        })
    return records


def theorem_truth_table() -> dict[str, int]:
    """Audit the only logical branch where palette nonmembership is used."""

    admissible = 0
    implication_failures = 0
    forced_second_endpoint = 0
    for qv_edge, first_retained, second_retained in itertools.product(
        (False, True), repeat=3
    ):
        # Closure of K under the unoccupied attack at u, with exactly the
        # physical responders w and q.
        if not (first_retained or second_retained):
            continue
        # A retained first endpoint {u,t,q} dominates the omitted root
        # anchor v.  Since u and t are root nonneighbors of v, qv is then
        # forced.  This is the proof's legitimate retained-state-to-edge
        # implication.
        if first_retained and not qv_edge:
            continue
        admissible += 1
        v_in_q_palette = qv_edge and first_retained
        v_in_w_palette = second_retained  # vw is an accepted C-157 edge.
        if not (v_in_q_palette or v_in_w_palette):
            implication_failures += 1
        if not v_in_q_palette:
            require(not first_retained, "retained first endpoint without Q(q)")
            require(second_retained, "closure did not force second endpoint")
            forced_second_endpoint += 1
    require(implication_failures == 0, "palette-transfer truth table failed")
    return {
        "admissible_rows": admissible,
        "implication_failures": implication_failures,
        "rows_forcing_second_endpoint": forced_second_endpoint,
    }


def main() -> None:
    payload = {
        "schema": "full-list-three-color-coupling-hostile-replay-v1",
        "model": (
            "only unoccupied vertices are attacked; exactly one adjacent "
            "guard moves; closure is tested in one literal family"
        ),
        "theorem_truth_table": theorem_truth_table(),
        "color_maps": color_map_audit(),
        "formula_counts": formula_count_audit(),
        "equality_control": equality_control(),
        "gamma_two_control": gamma_two_control(),
        "scope": (
            "independent controls, local logical branch, map count, and "
            "formula-size audit; no solver UNSAT status is promoted"
        ),
    }
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
