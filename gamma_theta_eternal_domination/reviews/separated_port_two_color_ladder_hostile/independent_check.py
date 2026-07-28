#!/usr/bin/env python3
"""Clean-room bit-mask audit of the separated-port finite control.

This checker deliberately does not import the search code or the target
verifier.  It decodes the Graph6 record, reconstructs the graph, and runs
the one-guard fixed-point computation using integer masks.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


GRAPH6 = "JFzvvn{~fM?"
N = 11
A, B, C, X, R, S_MID, Q, V0, V1, Z, W = range(N)
ANCHORS = (A, B, C)
ANCHOR_MASK = sum(1 << v for v in ANCHORS)

EXPECTED_H_EDGES = {
    (A, B),
    (A, C),
    (B, C),
    (X, R),
    (R, S_MID),
    (S_MID, Q),
    (Q, V1),
    (V0, V1),
    (R, V0),
    (V0, Z),
    (V1, Z),
    (Z, W),
    (X, W),
    (R, W),
    (V1, W),
}

EXPECTED_LISTS = {
    X: frozenset((A, B, C)),
    R: frozenset((A, B)),
    S_MID: frozenset((A, B)),
    Q: frozenset((A, B)),
    V0: frozenset((B, C)),
    V1: frozenset((B, C)),
    Z: frozenset((A, B)),
    W: frozenset((B, C)),
}

H_COLORING = (0, 1, 2, 2, 0, 1, 2, 1, 0, 2, 1)


def decode_graph6(record: str) -> tuple[int, tuple[int, ...]]:
    raw = record.encode("ascii")
    assert raw and 63 <= raw[0] <= 125
    order = raw[0] - 63
    assert order <= 62
    bit_stream: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        assert 0 <= value < 64
        bit_stream.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    assert len(bit_stream) >= needed
    assert all(bit == 0 for bit in bit_stream[needed:])
    adjacency = [0] * order
    cursor = 0
    for upper in range(1, order):
        for lower in range(upper):
            if bit_stream[cursor]:
                adjacency[upper] |= 1 << lower
                adjacency[lower] |= 1 << upper
            cursor += 1
    return order, tuple(adjacency)


ORDER, G_ADJ = decode_graph6(GRAPH6)
ALL = (1 << ORDER) - 1
H_ADJ = tuple(ALL ^ (1 << v) ^ G_ADJ[v] for v in range(ORDER))
G_CLOSED = tuple(G_ADJ[v] | (1 << v) for v in range(ORDER))


def vertices(mask: int) -> tuple[int, ...]:
    return tuple(v for v in range(ORDER) if mask & (1 << v))


def masks_of_size(size: int) -> list[int]:
    return [
        sum(1 << v for v in combination)
        for combination in itertools.combinations(range(ORDER), size)
    ]


def dominates(mask: int) -> bool:
    covered = 0
    for guard in vertices(mask):
        covered |= G_CLOSED[guard]
    return covered == ALL


def independent(mask: int) -> bool:
    for vertex in vertices(mask):
        if G_ADJ[vertex] & mask:
            return False
    return True


def greatest_kernel(
    size: int, banned: frozenset[int] = frozenset()
) -> tuple[frozenset[int], tuple[int, ...]]:
    current = {
        state
        for state in masks_of_size(size)
        if state not in banned and dominates(state)
    }
    rounds: list[int] = []
    while True:
        survivors: set[int] = set()
        for state in current:
            safe = True
            for attack in vertices(ALL ^ state):
                attack_bit = 1 << attack
                responses = False
                for guard in vertices(state):
                    if G_ADJ[guard] & attack_bit:
                        successor = (state ^ (1 << guard)) | attack_bit
                        if successor in current:
                            responses = True
                            break
                if not responses:
                    safe = False
                    break
            if safe:
                survivors.add(state)
        if survivors == current:
            return frozenset(current), tuple(rounds)
        rounds.append(len(current) - len(survivors))
        current = survivors


def direct_swap(guard: int, target: int) -> int:
    return (ANCHOR_MASK ^ (1 << guard)) | (1 << target)


def restricted_family() -> tuple[frozenset[int], tuple[int, ...]]:
    banned = frozenset(
        direct_swap(guard, target)
        for target, allowed in EXPECTED_LISTS.items()
        for guard in ANCHORS
        if guard not in allowed
    )
    return greatest_kernel(3, banned)


def response_lists(family: frozenset[int]) -> dict[int, frozenset[int]]:
    return {
        target: frozenset(
            guard
            for guard in ANCHORS
            if (G_ADJ[guard] & (1 << target))
            and direct_swap(guard, target) in family
        )
        for target in range(ORDER)
        if target not in ANCHORS
    }


def family_obligations(family: frozenset[int]) -> int:
    obligations = 0
    for state in family:
        assert state.bit_count() == 3
        assert dominates(state)
        for attack in vertices(ALL ^ state):
            obligations += 1
            attack_bit = 1 << attack
            legal = []
            for guard in vertices(state):
                if G_ADJ[guard] & attack_bit:
                    successor = (state ^ (1 << guard)) | attack_bit
                    if successor in family:
                        legal.append((guard, successor))
            assert legal
            for guard, successor in legal:
                assert guard in vertices(state)
                assert not (state & attack_bit)
                assert G_ADJ[guard] & attack_bit
                assert (state ^ successor).bit_count() == 2
                assert successor.bit_count() == 3
                assert dominates(successor)
    return obligations


def exact_gamma() -> int:
    for size in range(1, ORDER + 1):
        if any(dominates(mask) for mask in masks_of_size(size)):
            return size
    raise AssertionError("finite graph has no dominating set")


def exact_alpha() -> int:
    for size in range(ORDER, 0, -1):
        if any(independent(mask) for mask in masks_of_size(size)):
            return size
    raise AssertionError("finite graph has no independent vertex")


def h_edge(u: int, v: int) -> bool:
    return bool(H_ADJ[u] & (1 << v))


def odd_fan_exists(lists: dict[int, frozenset[int]]) -> bool:
    outside = tuple(v for v in range(ORDER) if v not in ANCHORS)
    for omitted in ANCHORS:
        positive = tuple(v for v in outside if omitted in lists[v])
        avoiding = frozenset(v for v in outside if omitted not in lists[v])
        for p in positive:
            for hub in outside:
                if hub == p or not h_edge(p, hub):
                    continue
                starts = avoiding - {hub}
                for start in starts:
                    if not h_edge(hub, start):
                        continue
                    stack = [(start, (start,))]
                    while stack:
                        endpoint, path = stack.pop()
                        edge_length = len(path) - 1
                        if (
                            edge_length >= 1
                            and edge_length % 2 == 1
                            and h_edge(hub, endpoint)
                        ):
                            return True
                        for nxt in avoiding:
                            if nxt == hub or nxt in path:
                                continue
                            if h_edge(endpoint, nxt):
                                stack.append((nxt, path + (nxt,)))
    return False


def family_digest(family: frozenset[int]) -> str:
    triples = sorted(vertices(state) for state in family)
    payload = "".join(
        ",".join(str(vertex) for vertex in triple) + "\n"
        for triple in triples
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assert ORDER == N
    actual_h_edges = {
        (u, v)
        for u in range(ORDER)
        for v in range(u + 1, ORDER)
        if h_edge(u, v)
    }
    assert actual_h_edges == EXPECTED_H_EDGES

    family, restricted_rounds = restricted_family()
    lists = response_lists(family)
    assert len(family) == 109
    assert restricted_rounds == (20, 4, 5, 5, 2)
    assert lists == EXPECTED_LISTS
    obligations = family_obligations(family)
    assert obligations == 872
    assert family_digest(family) == (
        "34ad69cf11195558c2743fcb6332c2d4cef0750f7eb95be715aa892fd9733eb6"
    )

    unrestricted_kernels = {}
    for size in (1, 2, 3):
        kernel, rounds = greatest_kernel(size)
        unrestricted_kernels[size] = (len(kernel), rounds)
    assert unrestricted_kernels[1][0] == 0
    assert unrestricted_kernels[2][0] == 0
    assert unrestricted_kernels[3][0] > 0

    gamma = exact_gamma()
    alpha = exact_alpha()
    assert gamma == 2
    assert alpha == 3
    assert dominates((1 << A) | (1 << X))
    assert all(H_ADJ[v] for v in range(ORDER))

    assert all(
        H_COLORING[u] != H_COLORING[v]
        for u, v in EXPECTED_H_EDGES
    )
    assert {H_COLORING[v] for v in ANCHORS} == {0, 1, 2}
    assert not any(
        all(h_edge(u, v) for u, v in itertools.combinations(quad, 2))
        for quad in itertools.combinations(range(ORDER), 4)
    )

    bow_tie = (X, R, W, Z, V1)
    bow_edges = {
        (min(u, v), max(u, v))
        for u, v in itertools.combinations(bow_tie, 2)
        if h_edge(u, v)
    }
    assert bow_edges == {
        (X, R),
        (X, W),
        (R, W),
        (Z, W),
        (V1, Z),
        (V1, W),
    }
    for u, v in itertools.combinations(bow_tie, 2):
        assert H_ADJ[u] & H_ADJ[v]

    assert h_edge(V0, V1)
    assert h_edge(V1, W)
    assert not h_edge(V0, W)
    assert h_edge(Z, V0) and h_edge(Z, V1) and h_edge(Z, W)
    assert not (H_ADJ[R] & H_ADJ[S_MID])
    assert not (H_ADJ[S_MID] & H_ADJ[Q])
    assert not odd_fan_exists(lists)

    gamma_root = Path(__file__).resolve().parents[2]
    target_dir = gamma_root / "math/working/separated_port_two_color_ladder"
    target_hashes = {
        name: sha256(target_dir / name)
        for name in ("NOTE.md", "RESEARCH_LOG.md", "verify.py", "result.json")
    }

    result = {
        "status": "PASS",
        "model": {
            "attacks_only_unoccupied": True,
            "exactly_one_guard_moves": True,
            "move_uses_G_edge": True,
            "every_retained_state_dominates": True,
        },
        "graph": {
            "graph6_G": GRAPH6,
            "order": ORDER,
            "H_edges": [list(edge) for edge in sorted(actual_h_edges)],
        },
        "parameters": {
            "gamma": gamma,
            "alpha": alpha,
            "gamma_infinity": 3,
            "theta": 3,
        },
        "restricted_family": {
            "states": len(family),
            "deletion_rounds": list(restricted_rounds),
            "attack_obligations": obligations,
            "sha256": family_digest(family),
            "response_lists": {
                str(target): sorted(allowed)
                for target, allowed in lists.items()
            },
        },
        "unrestricted_kernel_sizes": {
            str(size): count
            for size, (count, _rounds) in unrestricted_kernels.items()
        },
        "unrestricted_kernel_rounds": {
            str(size): list(rounds)
            for size, (_count, rounds) in unrestricted_kernels.items()
        },
        "bow_tie_H_edges": [list(edge) for edge in sorted(bow_edges)],
        "c_connector_cap_sets_empty": True,
        "odd_fan_embedding_absent": True,
        "target_sha256": target_hashes,
        "checker_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
