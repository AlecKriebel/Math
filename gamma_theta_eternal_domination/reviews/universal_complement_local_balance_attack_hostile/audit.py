#!/usr/bin/env python3
"""Clean-room hostile audit for the complement/local-balance working note.

This checker intentionally imports none of the campaign graph/evaluator code.
It checks the named finite examples and exhaustively probes the response-list
and collision statements on all labelled graphs through order five.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import re


CAMPAIGN = Path(__file__).resolve().parents[2]
NOTE = CAMPAIGN / "math/working/universal_complement_local_balance_attack.md"
LOG = (
    CAMPAIGN
    / "math/working/universal_complement_local_balance_attack_evidence/LOG.md"
)
PROBE = (
    CAMPAIGN
    / "math/working/universal_complement_local_balance_attack_evidence/probe.py"
)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def decode_graph6(record: str) -> tuple[int, tuple[int, ...]]:
    values = [ord(char) - 63 for char in record.strip()]
    assert values and 0 <= values[0] < 63
    n = values[0]
    bits: list[int] = []
    for value in values[1:]:
        assert 0 <= value <= 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    assert len(values[1:]) == (needed + 5) // 6
    assert not any(bits[needed:])
    adjacency = [0] * n
    position = 0
    for right in range(1, n):
        for left in range(right):
            if bits[position]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            position += 1
    return n, tuple(adjacency)


def encode_graph6(n: int, adjacency: tuple[int, ...]) -> str:
    assert n < 63
    bits = [
        int(bool(adjacency[left] & (1 << right)))
        for right in range(1, n)
        for left in range(right)
    ]
    while len(bits) % 6:
        bits.append(0)
    chars = [chr(n + 63)]
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        chars.append(chr(value + 63))
    return "".join(chars)


def complement(n: int, adjacency: tuple[int, ...]) -> tuple[int, ...]:
    full = (1 << n) - 1
    return tuple(full ^ (1 << vertex) ^ adjacency[vertex] for vertex in range(n))


def masks_of_size(n: int, size: int):
    for vertices in combinations(range(n), size):
        yield sum(1 << vertex for vertex in vertices)


def is_dominating(n: int, adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in range(n):
        if state & (1 << vertex):
            covered |= adjacency[vertex]
    return covered == (1 << n) - 1


def is_independent(adjacency: tuple[int, ...], state: int) -> bool:
    vertices = [v for v in range(len(adjacency)) if state & (1 << v)]
    return all(not adjacency[left] & (1 << right) for left, right in combinations(vertices, 2))


def gamma(n: int, adjacency: tuple[int, ...]) -> int:
    return next(
        size
        for size in range(n + 1)
        if any(is_dominating(n, adjacency, state) for state in masks_of_size(n, size))
    )


def alpha(n: int, adjacency: tuple[int, ...]) -> int:
    return max(
        size
        for size in range(n + 1)
        if any(is_independent(adjacency, state) for state in masks_of_size(n, size))
    )


def independent_domination(n: int, adjacency: tuple[int, ...]) -> int:
    return next(
        size
        for size in range(n + 1)
        if any(
            is_independent(adjacency, state)
            and is_dominating(n, adjacency, state)
            for state in masks_of_size(n, size)
        )
    )


def colorable(n: int, adjacency: tuple[int, ...], color_count: int) -> bool:
    order = sorted(range(n), key=lambda v: adjacency[v].bit_count(), reverse=True)
    colors = [-1] * n

    def visit(index: int) -> bool:
        if index == n:
            return True
        vertex = order[index]
        forbidden = {
            colors[other]
            for other in range(n)
            if colors[other] >= 0 and adjacency[vertex] & (1 << other)
        }
        for color in range(color_count):
            if color in forbidden:
                continue
            colors[vertex] = color
            if visit(index + 1):
                return True
            colors[vertex] = -1
        return False

    return visit(0)


def theta(n: int, adjacency: tuple[int, ...]) -> int:
    opposite = complement(n, adjacency)
    return next(count for count in range(1, n + 1) if colorable(n, opposite, count))


def greatest_family(
    n: int, adjacency: tuple[int, ...], guard_count: int
) -> set[int]:
    configurations = {
        state
        for state in masks_of_size(n, guard_count)
        if is_dominating(n, adjacency, state)
    }
    current = configurations
    while current:
        successor = {
            state
            for state in configurations
            if all(
                any(
                    state & (1 << guard)
                    and adjacency[attacked] & (1 << guard)
                    and (state ^ (1 << guard) ^ (1 << attacked)) in current
                    for guard in range(n)
                )
                for attacked in range(n)
                if not state & (1 << attacked)
            )
        }
        if successor == current:
            return current
        current = successor
    return set()


def gamma_infinity(n: int, adjacency: tuple[int, ...]) -> int:
    return next(
        guard_count
        for guard_count in range(1, n + 1)
        if greatest_family(n, adjacency, guard_count)
    )


def edge_set(n: int, adjacency: tuple[int, ...]) -> set[tuple[int, int]]:
    return {
        (left, right)
        for left in range(n)
        for right in range(left + 1, n)
        if adjacency[left] & (1 << right)
    }


def triangles(n: int, adjacency: tuple[int, ...]) -> list[tuple[int, int, int]]:
    return [
        triple
        for triple in combinations(range(n), 3)
        if all(adjacency[left] & (1 << right) for left, right in combinations(triple, 2))
    ]


def gf2_rank(rows: list[int]) -> int:
    basis: dict[int, int] = {}
    for original in rows:
        row = original
        while row:
            pivot = row.bit_length() - 1
            if pivot in basis:
                row ^= basis[pivot]
            else:
                basis[pivot] = row
                break
    return len(basis)


def h1_dimension(n: int, adjacency: tuple[int, ...]) -> int:
    edges = sorted(edge_set(n, adjacency))
    positions = {edge: index for index, edge in enumerate(edges)}
    boundaries = [
        sum(1 << positions[edge] for edge in combinations(triple, 2))
        for triple in triangles(n, adjacency)
    ]
    unseen = set(range(n))
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            vertex = stack.pop()
            found = {
                other
                for other in unseen
                if adjacency[vertex] & (1 << other)
            }
            unseen -= found
            stack.extend(found)
    return len(edges) - n + components - gf2_rank(boundaries)


def check_loop(
    n: int,
    adjacency: tuple[int, ...],
    initial: tuple[int, ...],
    steps: tuple[tuple[int, int], ...],
) -> dict[str, object]:
    state = sum(1 << vertex for vertex in initial)
    labels = {vertex: label for label, vertex in enumerate(initial)}
    states = [initial]
    for moved, attacked in steps:
        assert state & (1 << moved)
        assert not state & (1 << attacked)
        assert adjacency[moved] & (1 << attacked)
        state ^= (1 << moved) | (1 << attacked)
        assert is_dominating(n, adjacency, state)
        labels[attacked] = labels.pop(moved)
        states.append(tuple(v for v in range(n) if state & (1 << v)))
    assert state == sum(1 << vertex for vertex in initial)
    return {
        "states": ["".join(map(str, state_vertices)) for state_vertices in states],
        "final_labels": {str(vertex): labels[vertex] for vertex in sorted(labels)},
    }


def list_colorable(
    n: int,
    adjacency: tuple[int, ...],
    vertices: tuple[int, ...],
    lists: dict[int, set[int]],
) -> bool:
    assigned: dict[int, int] = {}
    order = sorted(vertices, key=lambda v: (len(lists[v]), -sum(
        1 for w in vertices if w != v and not adjacency[v] & (1 << w)
    )))

    def visit(index: int) -> bool:
        if index == len(order):
            return True
        vertex = order[index]
        for color in lists[vertex]:
            if any(
                assigned.get(other) == color
                and not adjacency[vertex] & (1 << other)
                for other in assigned
            ):
                continue
            assigned[vertex] = color
            if visit(index + 1):
                return True
            del assigned[vertex]
        return False

    return visit(0)


def response_lists(
    n: int,
    adjacency: tuple[int, ...],
    family: set[int],
    independent_state: int,
) -> tuple[tuple[int, ...], dict[int, set[int]]]:
    private_union = 0
    for guard in range(n):
        if not independent_state & (1 << guard):
            continue
        guard_bit = 1 << guard
        for vertex in range(n):
            closed_intersection = independent_state & (
                adjacency[vertex] | (1 << vertex)
            )
            if closed_intersection == guard_bit:
                private_union |= 1 << vertex
    shared = tuple(v for v in range(n) if not private_union & (1 << v))
    lists = {
        vertex: {
            guard
            for guard in range(n)
            if independent_state & (1 << guard)
            and adjacency[vertex] & (1 << guard)
            and (independent_state ^ (1 << guard) ^ (1 << vertex)) in family
        }
        for vertex in range(n)
        if not independent_state & (1 << vertex)
    }
    return shared, lists


def exhaustive_response_probe() -> dict[str, int]:
    counts = {
        "labelled_graphs": 0,
        "equality_graphs": 0,
        "maximum_independent_states": 0,
        "response_list_vertices": 0,
        "hall_independent_outside_sets": 0,
        "collision_obligations": 0,
    }
    for n in range(1, 6):
        pairs = list(combinations(range(n), 2))
        for edge_mask in range(1 << len(pairs)):
            counts["labelled_graphs"] += 1
            adjacency = [0] * n
            for index, (left, right) in enumerate(pairs):
                if edge_mask & (1 << index):
                    adjacency[left] |= 1 << right
                    adjacency[right] |= 1 << left
            graph = tuple(adjacency)
            domination = gamma(n, graph)
            eternal = gamma_infinity(n, graph)
            if domination != eternal:
                continue
            counts["equality_graphs"] += 1
            independence = alpha(n, graph)
            assert independence == eternal
            family = greatest_family(n, graph, eternal)
            cover = theta(n, graph)
            for state in masks_of_size(n, independence):
                if not is_independent(graph, state):
                    continue
                counts["maximum_independent_states"] += 1
                assert state in family
                shared, lists = response_lists(n, graph, family, state)
                counts["response_list_vertices"] += len(shared)
                assert all(lists.values())
                outside = tuple(
                    vertex
                    for vertex in range(n)
                    if not state & (1 << vertex)
                )
                for subset_size in range(len(outside) + 1):
                    for subset_vertices in combinations(outside, subset_size):
                        subset = sum(1 << vertex for vertex in subset_vertices)
                        if not is_independent(graph, subset):
                            continue
                        counts["hall_independent_outside_sets"] += 1
                        union = set().union(
                            *(lists[vertex] for vertex in subset_vertices)
                        )
                        assert len(union) >= subset_size
                coloring_exists = list_colorable(n, graph, shared, lists)
                assert coloring_exists == (cover == eternal)
                for left, right in combinations(shared, 2):
                    if graph[left] & (1 << right):
                        continue
                    for color in lists[left] & lists[right]:
                        counts["collision_obligations"] += 1
                        alternatives = (
                            lists[left] | lists[right]
                        ) - {color}
                        assert alternatives
    return counts


def main() -> None:
    note_text = NOTE.read_text()
    log_text = LOG.read_text()
    frozen = re.search(
        r"working note\n([0-9a-f]{64})\n\nprobe\n([0-9a-f]{64})",
        log_text,
    )
    assert frozen
    frozen_note_hash, frozen_probe_hash = frozen.groups()

    n, graph = decode_graph6("FCpbO")
    stated_edges = {
        (0, 3), (0, 4), (1, 4), (1, 5),
        (1, 6), (2, 5), (2, 6), (4, 6),
    }
    assert edge_set(n, graph) == stated_edges
    opposite = complement(n, graph)
    assert encode_graph6(n, opposite) == "FzM[g"
    stated_triangles = [
        (0, 1, 2), (0, 5, 6), (1, 2, 3),
        (2, 3, 4), (3, 4, 5), (3, 5, 6),
    ]
    assert triangles(n, opposite) == stated_triangles
    assert h1_dimension(n, opposite) == 1
    parameters = {
        "gamma": gamma(n, graph),
        "i": independent_domination(n, graph),
        "alpha": alpha(n, graph),
        "gamma_infinity": gamma_infinity(n, graph),
        "theta": theta(n, graph),
    }
    assert parameters == {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    parts = ({0, 3}, {1, 4, 6}, {2, 5})
    assert all(
        graph[left] & (1 << right)
        for part in parts
        for left, right in combinations(part, 2)
    )
    assert all(opposite[left] & opposite[right] for left, right in combinations(range(n), 2))

    c4 = tuple(
        sum(1 << other for other in range(4) if (vertex - other) % 4 in (1, 3))
        for vertex in range(4)
    )
    c4_loop = check_loop(
        4, c4, (0, 2), ((0, 1), (2, 3), (3, 0), (1, 2))
    )
    assert c4_loop["final_labels"] == {"0": 1, "2": 0}

    c7 = tuple(
        sum(1 << other for other in range(7) if (vertex - other) % 7 in (1, 6))
        for vertex in range(7)
    )
    c7_loop = check_loop(
        7,
        c7,
        (0, 2, 4),
        ((4, 5), (2, 3), (0, 1), (5, 6), (3, 4), (1, 2), (6, 0)),
    )
    assert c7_loop["final_labels"] == {"0": 2, "2": 0, "4": 1}
    assert {
        "gamma": gamma(7, c7),
        "i": independent_domination(7, c7),
        "alpha": alpha(7, c7),
        "gamma_infinity": gamma_infinity(7, c7),
        "theta": theta(7, c7),
    } == {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 4,
        "theta": 4,
    }

    response_probe = exhaustive_response_probe()
    bindings_match = (
        frozen_note_hash == digest(NOTE)
        and frozen_probe_hash == digest(PROBE)
    )
    normalized_note = re.sub(r"\s+", " ", note_text)
    findings = [
        "No false PROVED statement was found.",
        (
            "The exact one-guard restoration proof of the family-response "
            "Hall condition is valid."
        ),
        (
            "Lemma 8 correctly infers xv in E(G) from domination of "
            "S-v+x in its second branch."
        ),
        (
            "The facet-transport discussion now expressly requires "
            "ridge-component and lower-overlap compatibility."
        ),
    ]
    if not bindings_match:
        findings.append(
            "The evidence log's frozen hashes do not match the reviewed bytes."
        )
    payload = {
        "schema": "universal-complement-local-balance-hostile-audit-v1",
        "verdict": "ACCEPT" if bindings_match else "REVISE",
        "reviewed_hashes": {
            "working_note": digest(NOTE),
            "evidence_log": digest(LOG),
            "evidence_probe": digest(PROBE),
        },
        "evidence_log_frozen_hashes": {
            "working_note": frozen_note_hash,
            "evidence_probe": frozen_probe_hash,
        },
        "evidence_binding": {
            "working_note_matches": frozen_note_hash == digest(NOTE),
            "probe_matches": frozen_probe_hash == digest(PROBE),
        },
        "explicit_FCpbO": {
            "parameters": parameters,
            "H_graph6": encode_graph6(n, opposite),
            "H_edges": len(edge_set(n, opposite)),
            "H_triangles": ["".join(map(str, triple)) for triple in stated_triangles],
            "H1_dimension_mod2": h1_dimension(n, opposite),
        },
        "C4_loop": c4_loop,
        "C7_loop": c7_loop,
        "response_list_probe_through_order_5": response_probe,
        "proof_findings": findings,
        "scope": (
            "Finite checks are falsification evidence only; the analytic proof "
            "audit is recorded in REVIEW.md."
        ),
        "note_contains_no_resolution_claim": (
            "does not prove the gamma--theta conjecture" in normalized_note
            and "No order-13 SAT" in normalized_note
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
