#!/usr/bin/env python3
"""Independent hostile replay for the distributed-holonomy note.

This file deliberately imports no campaign evaluator or transition code.
Graphs are decoded into integer bit masks, domination and the greatest
one-guard triple kernel are rebuilt directly from the definition, and
simple complement paths are enumerated by a fresh depth-first search.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "math/working/distributed_gate_holonomy/NOTE.md"
CONTROLS = (
    "LFzJbZYhdrDZdM",
    "MFzJbZYhlrDZdMhd_",
    "NFzJbZZhlrDZdMhd|h_",
    "MEXrtIdmdjLQqztC?",
)
EXPECTED = {
    "LFzJbZYhdrDZdM": (13, 142, 40, 86),
    "MFzJbZYhlrDZdMhd_": (14, 177, 72, 150),
    "NFzJbZZhlrDZdMhd|h_": (15, 216, 120, 246),
    "MEXrtIdmdjLQqztC?": (14, 172, 204, 396),
}
FULL_MASK_CACHE: dict[int, int] = {}


def bits(mask: int):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def decode_graph6(record: str) -> tuple[int, tuple[int, ...]]:
    """Decode the small-order graph6 format without third-party code."""
    if not record or record[0] == "~":
        raise ValueError("only the one-byte order format is expected")
    order = ord(record[0]) - 63
    stream: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 payload")
        stream.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    required = order * (order - 1) // 2
    if len(stream) < required:
        raise ValueError("truncated graph6 record")
    adjacency = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if stream[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return order, tuple(adjacency)


def dominates(state: int, adjacency: tuple[int, ...], full: int) -> bool:
    covered = state
    for guard in bits(state):
        covered |= adjacency[guard]
    return covered == full


def greatest_triple_kernel(
    adjacency: tuple[int, ...],
) -> tuple[set[int], list[int], int]:
    order = len(adjacency)
    full = (1 << order) - 1
    family = {
        sum(1 << vertex for vertex in triple)
        for triple in combinations(range(order), 3)
        if dominates(sum(1 << vertex for vertex in triple), adjacency, full)
    }
    initial_size = len(family)
    round_sizes: list[int] = []
    while True:
        rejected: set[int] = set()
        for state in family:
            for attacked in range(order):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                response = False
                for guard in bits(state):
                    if not (adjacency[guard] & attacked_bit):
                        continue
                    successor = (state ^ (1 << guard)) | attacked_bit
                    if successor in family:
                        response = True
                        break
                if not response:
                    rejected.add(state)
                    break
        if not rejected:
            return family, round_sizes, initial_size
        family -= rejected
        round_sizes.append(len(rejected))


def domination_number(adjacency: tuple[int, ...]) -> int:
    order = len(adjacency)
    full = (1 << order) - 1
    for size in range(1, order + 1):
        for chosen in combinations(range(order), size):
            state = sum(1 << vertex for vertex in chosen)
            if dominates(state, adjacency, full):
                return size
    raise AssertionError("finite graph has no dominating set")


def independent_parameters(adjacency: tuple[int, ...]) -> tuple[int, int]:
    order = len(adjacency)
    maximum = 0
    minimum_maximal = order + 1
    for state in range(1, 1 << order):
        independent = True
        for vertex in bits(state):
            if adjacency[vertex] & state:
                independent = False
                break
        if not independent:
            continue
        size = state.bit_count()
        maximum = max(maximum, size)
        maximal = all(
            state & (1 << outside)
            or adjacency[outside] & state
            for outside in range(order)
        )
        if maximal:
            minimum_maximal = min(minimum_maximal, size)
    return maximum, minimum_maximal


def k_colorable(adjacency: tuple[int, ...], colors: int) -> bool:
    """Fresh saturation-first backtracker; adjacency is the colored graph."""
    order = len(adjacency)
    assigned = [-1] * order
    forbidden = [0] * order

    def search(colored: int) -> bool:
        if colored == order:
            return True
        candidates = [v for v in range(order) if assigned[v] < 0]
        vertex = max(
            candidates,
            key=lambda v: (forbidden[v].bit_count(), adjacency[v].bit_count(), -v),
        )
        allowed = ((1 << colors) - 1) & ~forbidden[vertex]
        while allowed:
            color_bit = allowed & -allowed
            allowed ^= color_bit
            color = color_bit.bit_length() - 1
            assigned[vertex] = color
            changed: list[tuple[int, int]] = []
            conflict = False
            for neighbor in bits(adjacency[vertex]):
                if assigned[neighbor] == color:
                    conflict = True
                    break
                if assigned[neighbor] < 0 and not forbidden[neighbor] & color_bit:
                    changed.append((neighbor, forbidden[neighbor]))
                    forbidden[neighbor] |= color_bit
                    if forbidden[neighbor] == (1 << colors) - 1:
                        conflict = True
                        break
            if not conflict and search(colored + 1):
                return True
            for neighbor, old in reversed(changed):
                forbidden[neighbor] = old
            assigned[vertex] = -1
        return False

    return search(0)


def chromatic_number(adjacency: tuple[int, ...]) -> int:
    for colors in range(1, len(adjacency) + 1):
        if k_colorable(adjacency, colors):
            return colors
    raise AssertionError("finite graph is colorable")


def family_lists(
    order: int,
    family: set[int],
    anchors: tuple[int, int, int] = (0, 1, 2),
) -> dict[int, frozenset[int]]:
    anchor_mask = sum(1 << vertex for vertex in anchors)
    return {
        vertex: frozenset(
            omitted
            for omitted in anchors
            if (anchor_mask ^ (1 << omitted)) | (1 << vertex) in family
        )
        for vertex in range(order)
        if vertex not in anchors
    }


def all_oriented_paths(
    starts: set[int],
    allowed: set[int],
    h_adjacency: tuple[int, ...],
    maximum_length: int,
    include_zero: bool,
) -> list[tuple[int, ...]]:
    answer: list[tuple[int, ...]] = []

    def extend(path: tuple[int, ...], used: int) -> None:
        length = len(path) - 1
        if include_zero or length:
            answer.append(path)
        if length == maximum_length:
            return
        candidates = h_adjacency[path[-1]]
        for vertex in sorted(bits(candidates)):
            bit = 1 << vertex
            if vertex not in allowed or used & bit:
                continue
            extend((*path, vertex), used | bit)

    for start in sorted(starts):
        extend((start,), 1 << start)
    return answer


def enumerate_path_pairs(
    order: int,
    g_adjacency: tuple[int, ...],
    family: set[int],
    *,
    maximum_length: int,
    include_zero: bool,
    require_disjoint: bool,
    require_start_boundary_absent: bool = True,
    require_end_boundary_absent: bool = True,
) -> tuple[int, int, list[dict[str, object]]]:
    full = (1 << order) - 1
    h_adjacency = tuple(
        (full ^ (1 << vertex) ^ g_adjacency[vertex])
        for vertex in range(order)
    )
    response_lists = family_lists(order, family)
    total = 0
    mismatches = 0
    first_examples: list[dict[str, object]] = []

    for a, b, c in permutations((0, 1, 2)):
        wc = {v for v, value in response_lists.items() if c not in value}
        wa = {v for v, value in response_lists.items() if a not in value}
        x_starts = {v for v in wc if a in response_lists[v]}
        y_starts = {v for v in wa if c in response_lists[v]}
        x_paths = all_oriented_paths(
            x_starts, wc, h_adjacency, maximum_length, include_zero
        )
        y_paths = all_oriented_paths(
            y_starts, wa, h_adjacency, maximum_length, include_zero
        )
        for x_path in x_paths:
            x_mask = sum(1 << vertex for vertex in x_path)
            for y_path in y_paths:
                y_mask = sum(1 << vertex for vertex in y_path)
                if require_disjoint and x_mask & y_mask:
                    continue
                start_boundary = (
                    (1 << b) | (1 << x_path[0]) | (1 << y_path[0])
                )
                end_boundary = (
                    (1 << b) | (1 << x_path[-1]) | (1 << y_path[-1])
                )
                if start_boundary.bit_count() != 3 or end_boundary.bit_count() != 3:
                    continue
                if require_start_boundary_absent and start_boundary in family:
                    continue
                if require_end_boundary_absent and end_boundary in family:
                    continue
                total += 1
                mismatch = (len(x_path) - len(y_path)) & 1
                mismatches += mismatch
                if len(first_examples) < 5:
                    first_examples.append(
                        {
                            "anchors": [a, b, c],
                            "x_path": list(x_path),
                            "y_path": list(y_path),
                            "parity_mismatch": bool(mismatch),
                        }
                    )
    return total, mismatches, first_examples


def audit_control(record: str) -> dict[str, object]:
    order, g_adjacency = decode_graph6(record)
    (
        expected_order,
        expected_family,
        expected_positive_pairs,
        expected_inclusive_pairs,
    ) = EXPECTED[record]
    assert order == expected_order
    reached = 1
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        unseen = g_adjacency[vertex] & ~reached
        for neighbor in bits(unseen):
            reached |= 1 << neighbor
            frontier.append(neighbor)
    assert reached == (1 << order) - 1
    family, deletion_rounds, dominating_triples = greatest_triple_kernel(
        g_adjacency
    )
    assert len(family) == expected_family
    anchor_mask = 0b111
    assert anchor_mask in family

    gamma = domination_number(g_adjacency)
    alpha, independent_domination = independent_parameters(g_adjacency)
    full = (1 << order) - 1
    h_adjacency = tuple(
        (full ^ (1 << vertex) ^ g_adjacency[vertex])
        for vertex in range(order)
    )
    theta = chromatic_number(h_adjacency)
    assert (gamma, independent_domination, alpha, theta) == (3, 3, 3, 3)

    positive_count, positive_bad, positive_examples = enumerate_path_pairs(
        order,
        g_adjacency,
        family,
        maximum_length=14,
        include_zero=False,
        require_disjoint=True,
    )
    assert positive_count == expected_positive_pairs
    assert positive_bad == 0
    inclusive_count, inclusive_bad, inclusive_examples = enumerate_path_pairs(
        order,
        g_adjacency,
        family,
        maximum_length=14,
        include_zero=True,
        require_disjoint=True,
    )
    assert inclusive_count == expected_inclusive_pairs
    assert inclusive_bad == 0
    relaxed_count, relaxed_bad, relaxed_examples = enumerate_path_pairs(
        order,
        g_adjacency,
        family,
        maximum_length=14,
        include_zero=True,
        require_disjoint=False,
    )
    no_end_count, no_end_bad, no_end_examples = enumerate_path_pairs(
        order,
        g_adjacency,
        family,
        maximum_length=14,
        include_zero=True,
        require_disjoint=True,
        require_end_boundary_absent=False,
    )
    no_start_count, no_start_bad, no_start_examples = enumerate_path_pairs(
        order,
        g_adjacency,
        family,
        maximum_length=14,
        include_zero=True,
        require_disjoint=True,
        require_start_boundary_absent=False,
    )
    return {
        "graph6": record,
        "order": order,
        "connected": True,
        "parameters": {
            "gamma": gamma,
            "i": independent_domination,
            "alpha": alpha,
            "gamma_infinity": 3,
            "theta": theta,
        },
        "dominating_triples": dominating_triples,
        "kernel_deletion_round_sizes": deletion_rounds,
        "greatest_family_size": len(family),
        "unoccupied_attack_obligations": len(family) * (order - 3),
        "positive_length_disjoint_path_pairs": positive_count,
        "positive_length_disjoint_mismatches": positive_bad,
        "positive_examples": positive_examples,
        "zero_inclusive_disjoint_path_pairs": inclusive_count,
        "zero_inclusive_disjoint_mismatches": inclusive_bad,
        "zero_inclusive_examples": inclusive_examples,
        "intersection_relaxed_path_pairs": relaxed_count,
        "intersection_relaxed_mismatches": relaxed_bad,
        "intersection_relaxed_examples": relaxed_examples,
        "end_boundary_relaxed_path_pairs": no_end_count,
        "end_boundary_relaxed_mismatches": no_end_bad,
        "end_boundary_relaxed_examples": no_end_examples,
        "start_boundary_relaxed_path_pairs": no_start_count,
        "start_boundary_relaxed_mismatches": no_start_bad,
        "start_boundary_relaxed_examples": no_start_examples,
    }


def main() -> None:
    source_root = ROOT / "math/working/distributed_gate_holonomy"
    evidence = {
        "schema": "distributed-gate-holonomy-hostile-v1",
        "note_sha256": sha256(NOTE.read_bytes()).hexdigest(),
        "source_verify_sha256": sha256(
            (source_root / "verify.py").read_bytes()
        ).hexdigest(),
        "source_result_sha256": sha256(
            (source_root / "result.json").read_bytes()
        ).hexdigest(),
        "controls": [audit_control(record) for record in CONTROLS],
    }
    evidence["positive_length_path_pair_sum"] = sum(
        item["positive_length_disjoint_path_pairs"]
        for item in evidence["controls"]
    )
    evidence["zero_inclusive_path_pair_sum"] = sum(
        item["zero_inclusive_disjoint_path_pairs"]
        for item in evidence["controls"]
    )
    evidence["intersection_relaxed_mismatch_sum"] = sum(
        item["intersection_relaxed_mismatches"]
        for item in evidence["controls"]
    )
    evidence["end_boundary_relaxed_mismatch_sum"] = sum(
        item["end_boundary_relaxed_mismatches"]
        for item in evidence["controls"]
    )
    evidence["start_boundary_relaxed_mismatch_sum"] = sum(
        item["start_boundary_relaxed_mismatches"]
        for item in evidence["controls"]
    )
    assert evidence["zero_inclusive_path_pair_sum"] == 878
    evidence["verdict"] = "PASS"
    output = Path(__file__).with_name("evidence.json")
    payload = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
