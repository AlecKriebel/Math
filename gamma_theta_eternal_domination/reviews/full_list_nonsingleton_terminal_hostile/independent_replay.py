#!/usr/bin/env python3
"""Clean-room replay of the cyclic-corridor boundary control.

This file intentionally imports no campaign module and shares no transition
code with the candidate verifier.  Configurations are packed integer masks.
"""

from __future__ import annotations

import itertools
import json
from typing import Iterable


GRAPH6 = "OQifur}UO]}iTij]tpo}v"
ROOT = (0, 1, 10)
TARGET = 6


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(text: str) -> tuple[int, tuple[int, ...]]:
    data = [ord(char) - 63 for char in text.strip()]
    require(data and 0 <= data[0] <= 62, "only short graph6 headers are used")
    n = data[0]
    stream: list[int] = []
    for value in data[1:]:
        require(0 <= value <= 63, "invalid graph6 payload")
        stream.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    need = n * (n - 1) // 2
    require(len(stream) >= need, "truncated graph6 payload")
    adjacency = [0] * n
    position = 0
    for high in range(1, n):
        for low in range(high):
            if stream[position]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            position += 1
    require(all(bit == 0 for bit in stream[need:]), "nonzero graph6 padding")
    return n, tuple(adjacency)


def vertices(mask: int) -> tuple[int, ...]:
    answer: list[int] = []
    while mask:
        bit = mask & -mask
        answer.append(bit.bit_length() - 1)
        mask ^= bit
    return tuple(answer)


def packed(items: Iterable[int]) -> int:
    answer = 0
    for item in items:
        answer |= 1 << item
    return answer


def is_dominating(mask: int, adjacency: tuple[int, ...], all_vertices: int) -> bool:
    covered = mask
    for vertex in vertices(mask):
        covered |= adjacency[vertex]
    return covered == all_vertices


def missed_vertices(mask: int, adjacency: tuple[int, ...], n: int) -> tuple[int, ...]:
    covered = mask
    for vertex in vertices(mask):
        covered |= adjacency[vertex]
    return vertices(((1 << n) - 1) ^ covered)


def configurations(n: int, size: int) -> tuple[int, ...]:
    return tuple(packed(choice) for choice in itertools.combinations(range(n), size))


def peel(
    universe: Iterable[int],
    adjacency: tuple[int, ...],
    n: int,
) -> tuple[frozenset[int], dict[int, int], tuple[int, ...]]:
    """Synchronous greatest-fixed-point deletion from the definition."""

    active = set(universe)
    rank: dict[int, int] = {}
    round_sizes: list[int] = []
    current_rank = 0
    all_vertices = (1 << n) - 1
    while True:
        doomed: list[int] = []
        for state in sorted(active):
            unoccupied = all_vertices ^ state
            failed = False
            for attacked in vertices(unoccupied):
                response_exists = False
                for mover in vertices(state):
                    if adjacency[mover] & (1 << attacked):
                        successor = (state ^ (1 << mover)) | (1 << attacked)
                        if successor in active:
                            response_exists = True
                            break
                if not response_exists:
                    failed = True
                    break
            if failed:
                doomed.append(state)
        if not doomed:
            return frozenset(active), rank, tuple(round_sizes)
        for state in doomed:
            rank[state] = current_rank
        active.difference_update(doomed)
        round_sizes.append(len(doomed))
        current_rank += 1


def exact_gamma(adjacency: tuple[int, ...], n: int) -> tuple[int, tuple[int, ...]]:
    all_vertices = (1 << n) - 1
    for size in range(1, n + 1):
        for state in configurations(n, size):
            if is_dominating(state, adjacency, all_vertices):
                return size, vertices(state)
    raise AssertionError("finite nonempty graph has no dominating set")


def exact_alpha(adjacency: tuple[int, ...], n: int) -> tuple[int, tuple[int, ...]]:
    for size in range(n, 0, -1):
        for state in configurations(n, size):
            if all((adjacency[v] & state) == 0 for v in vertices(state)):
                return size, vertices(state)
    raise AssertionError("finite nonempty graph has no independent set")


def colorable(
    adjacency: tuple[int, ...],
    color_count: int,
) -> tuple[int, ...] | None:
    """Exact DSATUR-style backtracking, independently implemented."""

    n = len(adjacency)
    colors = [-1] * n
    degrees = tuple(mask.bit_count() for mask in adjacency)

    def recurse(colored_count: int, largest_used: int) -> tuple[int, ...] | None:
        if colored_count == n:
            return tuple(colors)
        candidates = [v for v in range(n) if colors[v] < 0]

        def priority(vertex: int) -> tuple[int, int, int]:
            neighbor_colors = {
                colors[w]
                for w in vertices(adjacency[vertex])
                if colors[w] >= 0
            }
            return len(neighbor_colors), degrees[vertex], -vertex

        vertex = max(candidates, key=priority)
        forbidden = {
            colors[w]
            for w in vertices(adjacency[vertex])
            if colors[w] >= 0
        }
        upper = min(color_count - 1, largest_used + 1)
        for color in range(upper + 1):
            if color in forbidden:
                continue
            colors[vertex] = color
            result = recurse(colored_count + 1, max(largest_used, color))
            if result is not None:
                return result
            colors[vertex] = -1
        return None

    return recurse(0, -1)


def exact_chromatic(adjacency: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    for count in range(1, len(adjacency) + 1):
        witness = colorable(adjacency, count)
        if witness is not None:
            return count, witness
    raise AssertionError("coloring search failed")


def response_palette(
    root: int,
    target: int,
    greatest_family: frozenset[int],
    adjacency: tuple[int, ...],
) -> tuple[int, ...]:
    palette: list[int] = []
    for color in vertices(root):
        successor = (root ^ (1 << color)) | (1 << target)
        if adjacency[color] & (1 << target) and successor in greatest_family:
            palette.append(color)
    return tuple(palette)


def legal_moves(
    state: int,
    attacked: int,
    adjacency: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    answer: list[tuple[int, int]] = []
    for mover in vertices(state):
        if adjacency[mover] & (1 << attacked):
            answer.append((mover, (state ^ (1 << mover)) | (1 << attacked)))
    return tuple(answer)


def main() -> None:
    n, adjacency = decode_graph6(GRAPH6)
    require(n == 16, "unexpected graph order")
    all_vertices = (1 << n) - 1
    edge_count = sum(mask.bit_count() for mask in adjacency) // 2
    require(edge_count == 71, "unexpected graph size")

    root = packed(ROOT)
    require(all((adjacency[v] & root) == 0 for v in ROOT), "root is not independent")

    gamma, gamma_witness = exact_gamma(adjacency, n)
    alpha, alpha_witness = exact_alpha(adjacency, n)
    dominating_triples = tuple(
        state
        for state in configurations(n, 3)
        if is_dominating(state, adjacency, all_vertices)
    )
    greatest, unrestricted_rank, unrestricted_rounds = peel(
        dominating_triples, adjacency, n
    )
    require(greatest, "no eternal triple family")
    gamma_infinity = 3 if gamma == 3 else None

    complement = tuple(
        (all_vertices ^ (1 << v) ^ adjacency[v]) for v in range(n)
    )
    theta, complement_coloring = exact_chromatic(complement)

    require((gamma, alpha, gamma_infinity, theta) == (3, 3, 3, 3), "parameter mismatch")
    require(len(dominating_triples) == 304, "dominating-triple count mismatch")
    require(len(greatest) == 304, "greatest-family size mismatch")
    require(not unrestricted_rank and not unrestricted_rounds, "unexpected unrestricted deletion")
    require(root in greatest, "root absent from greatest family")

    target_palette = response_palette(root, TARGET, greatest, adjacency)
    require(target_palette == ROOT, "target is not full")

    physical_link = vertices(complement[TARGET])
    require(physical_link == (5, 7, 9, 11, 13), "physical link mismatch")
    physical_edges: list[tuple[int, int]] = []
    for a, b in itertools.combinations(physical_link, 2):
        if complement[a] & (1 << b):
            physical_edges.append((a, b))
    require(physical_edges == [(5, 7), (5, 9), (11, 13)], "link-edge mismatch")

    restricted: dict[int, dict[str, object]] = {}
    restricted_sets: dict[int, frozenset[int]] = {}
    restricted_ranks: dict[int, dict[int, int]] = {}
    expected_kernel = {0: 0, 1: 150, 10: 0}
    expected_rounds = {
        0: (26, 81, 132, 62),
        1: (28, 74, 49),
        10: (29, 81, 128, 62),
    }
    expected_start_rank = {0: 1, 1: None, 10: 1}
    for color in ROOT:
        ban = frozenset(
            (root ^ (1 << color)) | (1 << z) for z in physical_link
        )
        universe = tuple(state for state in dominating_triples if state not in ban)
        kernel, ranks, rounds = peel(universe, adjacency, n)
        start = (root ^ (1 << color)) | (1 << TARGET)
        require(len(kernel) == expected_kernel[color], f"kernel size mismatch: {color}")
        require(rounds == expected_rounds[color], f"round profile mismatch: {color}")
        observed_start_rank = None if start in kernel else ranks[start]
        require(
            observed_start_rank == expected_start_rank[color],
            f"start rank mismatch: {color}",
        )
        restricted_sets[color] = kernel
        restricted_ranks[color] = ranks
        restricted[color] = {
            "ban_states": len(ban),
            "initial_states": len(universe),
            "kernel_states": len(kernel),
            "deletion_rounds": list(rounds),
            "start_rank": observed_start_rank,
        }

    rows = (
        {
            "color": 0,
            "approach": 14,
            "mover": 14,
            "terminal": 11,
            "secondary": 1,
            "expected_palette": (0, 1),
            "expected_missed": (8,),
            "expected_predecessor_rank": 0,
            "secondary_survives": False,
        },
        {
            "color": 1,
            "approach": 3,
            "mover": 3,
            "terminal": 7,
            "secondary": 10,
            "expected_palette": (1, 10),
            "expected_missed": (),
            "expected_predecessor_rank": None,
            "secondary_survives": True,
        },
        {
            "color": 10,
            "approach": 12,
            "mover": 12,
            "terminal": 5,
            "secondary": 0,
            "expected_palette": (0, 10),
            "expected_missed": (4,),
            "expected_predecessor_rank": 0,
            "secondary_survives": False,
        },
    )

    audited_rows: list[dict[str, object]] = []
    for specification in rows:
        color = int(specification["color"])
        approach = int(specification["approach"])
        mover = int(specification["mover"])
        terminal_vertex = int(specification["terminal"])
        secondary = int(specification["secondary"])
        anchors = root ^ (1 << color)
        start = anchors | (1 << TARGET)
        predecessor = anchors | (1 << mover)
        terminal_state = anchors | (1 << terminal_vertex)
        secondary_state = (
            (predecessor ^ (1 << secondary)) | (1 << terminal_vertex)
        )
        ban = frozenset(
            anchors | (1 << z) for z in physical_link
        )

        require(start in greatest and predecessor in greatest, "retained approach states missing")
        require(approach == mover, "named approach attack differs from mover")
        require(
            adjacency[TARGET] & (1 << approach),
            "target guard cannot make named approach move",
        )
        require(
            (start ^ (1 << TARGET)) | (1 << approach) == predecessor,
            "approach occupancy mismatch",
        )
        require(
            adjacency[mover] & (1 << terminal_vertex),
            "corridor mover cannot enter terminal",
        )
        require(terminal_state in greatest and terminal_state in ban, "terminal membership mismatch")
        require(predecessor not in ban, "predecessor is banned")

        rank = (
            None
            if predecessor in restricted_sets[color]
            else restricted_ranks[color][predecessor]
        )
        require(rank == specification["expected_predecessor_rank"], "predecessor rank mismatch")

        palette = response_palette(root, terminal_vertex, greatest, adjacency)
        require(palette == specification["expected_palette"], "terminal palette mismatch")
        require(secondary_state not in ban, "secondary response is silently banned")
        missed = missed_vertices(secondary_state, adjacency, n)
        require(missed == specification["expected_missed"], "missed-witness mismatch")
        survives = secondary_state in restricted_sets[color]
        require(survives is specification["secondary_survives"], "secondary survival mismatch")
        require(
            (secondary_state in greatest) == (missed == ()),
            "greatest-family/dominating status mismatch",
        )

        move_audit: list[dict[str, object]] = []
        for responding_guard, successor in legal_moves(
            predecessor, terminal_vertex, adjacency
        ):
            move_audit.append(
                {
                    "mover": responding_guard,
                    "successor": list(vertices(successor)),
                    "dominates": is_dominating(successor, adjacency, all_vertices),
                    "in_ban": successor in ban,
                    "in_greatest": successor in greatest,
                    "in_kernel": successor in restricted_sets[color],
                    "missed": list(missed_vertices(successor, adjacency, n)),
                }
            )

        quartet = (TARGET, color, mover, terminal_vertex)
        missing = [
            (a, b)
            for a, b in itertools.combinations(quartet, 2)
            if not adjacency[a] & (1 << b)
        ]
        require(missing == [(TARGET, terminal_vertex)], "diamond mismatch")

        audited_rows.append(
            {
                "color": color,
                "start": list(vertices(start)),
                "predecessor": list(vertices(predecessor)),
                "predecessor_rank": rank,
                "terminal": list(vertices(terminal_state)),
                "palette": list(palette),
                "secondary_response": list(vertices(secondary_state)),
                "secondary_missed": list(missed),
                "secondary_survives": survives,
                "moves_at_terminal_attack": move_audit,
                "diamond_unique_missing_edge": [TARGET, terminal_vertex],
            }
        )

    named_vertices = set(ROOT)
    named_vertices.add(TARGET)
    named_vertices.update(int(row["mover"]) for row in rows)
    named_vertices.update(int(row["terminal"]) for row in rows)
    named_vertices.update((8, 4))
    require(len(named_vertices) == 12, "named occupancy collision")

    require(
        {color for color, data in restricted.items() if data["kernel_states"] == 0}
        == {0, 10},
        "exactly two kernels should be empty",
    )

    output = {
        "schema": "full-list-nonsingleton-hostile-clean-replay-v1",
        "graph6": GRAPH6,
        "order": n,
        "size": edge_count,
        "parameters": {
            "gamma": gamma,
            "gamma_witness": list(gamma_witness),
            "alpha": alpha,
            "alpha_witness": list(alpha_witness),
            "gamma_infinity": gamma_infinity,
            "theta": theta,
            "complement_coloring": list(complement_coloring),
        },
        "dominating_triples": len(dominating_triples),
        "greatest_eternal_triple_family": len(greatest),
        "root": list(ROOT),
        "target": TARGET,
        "target_palette": list(target_palette),
        "physical_link": list(physical_link),
        "physical_link_edges": [list(edge) for edge in physical_edges],
        "restricted": {str(key): value for key, value in restricted.items()},
        "rows": audited_rows,
        "named_distinct_vertices": sorted(named_vertices),
        "empty_restricted_kernels": [0, 10],
        "all_three_empty": False,
        "verdict": "PASS_CONTROL",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
