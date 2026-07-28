#!/usr/bin/env python3
"""Independent verifier for the physical-literal / nonphysical-clause control."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json


N = 13
A, B, C, Q, V, Z, U, VP, R, D, E, CP, AP = range(N)
S = frozenset((A, B, C))

WORDS = (
    (0, 0),  # a
    (1, 1),  # b
    (2, 2),  # c
    (0, 1),  # q: neutral {a,b}
    (1, 2),  # v: neutral {b,c}
    (1, 0),  # z: physical {a,b}, opposite sign from q
    (2, 1),
    (1, 2),
    (0, 1),  # r: physical {a,b}, same sign as q
    (2, 0),
    (0, 2),
    (2, 2),
    (0, 0),
)

EXTRA_G_EDGES = frozenset(
    {
        frozenset((C, Q)),  # makes q neutral without adding c to L(q)
        frozenset((A, V)),  # makes v neutral without adding a to L(v)
        frozenset((V, R)),  # destroys transport of the qv complement edge
    }
)


def pair(first: int, second: int) -> frozenset[int]:
    return frozenset((first, second))


def g_edge(first: int, second: int) -> bool:
    return (
        first != second
        and (
            WORDS[first][0] == WORDS[second][0]
            or WORDS[first][1] == WORDS[second][1]
            or pair(first, second) in EXTRA_G_EDGES
        )
    )


def h_edge(first: int, second: int) -> bool:
    return first != second and not g_edge(first, second)


def dominates(state: frozenset[int]) -> bool:
    return all(
        vertex in state or any(g_edge(vertex, guard) for guard in state)
        for vertex in range(N)
    )


def independent(state: frozenset[int]) -> bool:
    return all(not g_edge(x, y) for x, y in combinations(state, 2))


def partition_family(coordinate: int) -> frozenset[frozenset[int]]:
    classes = tuple(
        tuple(v for v in range(N) if WORDS[v][coordinate] == color)
        for color in range(3)
    )
    return frozenset(
        frozenset(choice)
        for choice in product(*classes)
    )


F0 = partition_family(0)
F1 = partition_family(1)
FAMILY = F0 | F1


def response_list(vertex: int) -> frozenset[int]:
    return frozenset(
        anchor
        for anchor in S
        if frozenset((S - {anchor}) | {vertex}) in FAMILY
    )


def obligations() -> int:
    count = 0
    for state in FAMILY:
        assert dominates(state)
        for attack in range(N):
            if attack in state:
                continue
            count += 1
            successors = [
                frozenset((state - {guard}) | {attack})
                for guard in state
                if g_edge(guard, attack)
                and frozenset((state - {guard}) | {attack}) in FAMILY
            ]
            assert successors
    return count


def graph6() -> str:
    bits = [
        int(g_edge(first, second))
        for second in range(1, N)
        for first in range(second)
    ]
    payload = []
    for offset in range(0, len(bits), 6):
        chunk = bits[offset : offset + 6]
        chunk += [0] * (6 - len(chunk))
        value = 0
        for bit in chunk:
            value = (value << 1) | bit
        payload.append(chr(63 + value))
    return chr(63 + N) + "".join(payload)


def same_sign_component() -> dict[int, int]:
    lists = {
        vertex: response_list(vertex)
        for vertex in range(N)
        if vertex not in S
    }
    w_c = {
        vertex
        for vertex, vertex_list in lists.items()
        if C not in vertex_list
    }
    b_c = {A, B} | w_c
    parity: dict[int, int] = {}
    for root in sorted(b_c):
        if root in parity:
            continue
        parity[root] = 0
        queue = [root]
        while queue:
            first = queue.pop()
            for second in sorted(b_c):
                if not h_edge(first, second):
                    continue
                if second not in parity:
                    parity[second] = parity[first] ^ 1
                    queue.append(second)
                else:
                    assert parity[second] == (parity[first] ^ 1)
    return parity


def common_h_witnesses() -> dict[str, int]:
    table: dict[str, int] = {}
    for first, second in combinations(range(N), 2):
        witness = next(
            vertex
            for vertex in range(N)
            if vertex not in (first, second)
            and h_edge(first, vertex)
            and h_edge(second, vertex)
        )
        table[f"{first},{second}"] = witness
    return table


def serialize_family() -> str:
    return "".join(
        ",".join(map(str, sorted(state))) + "\n"
        for state in sorted(FAMILY, key=lambda x: tuple(sorted(x)))
    )


def main() -> None:
    assert S in F0 and S in F1
    assert independent(S) and dominates(S)
    assert all(independent(frozenset(vertices)) is False
               for vertices in combinations(range(N), 4))
    assert not any(dominates(frozenset(vertices))
                   for vertices in combinations(range(N), 2))
    assert obligations() == len(FAMILY) * (N - 3)
    connected = {A}
    stack = [A]
    while stack:
        first = stack.pop()
        for second in range(N):
            if second not in connected and g_edge(first, second):
                connected.add(second)
                stack.append(second)
    assert connected == set(range(N))

    lists = {
        vertex: response_list(vertex)
        for vertex in range(N)
        if vertex not in S
    }
    assert lists[Q] == frozenset((A, B))
    assert lists[V] == frozenset((B, C))
    assert lists[Z] == frozenset((A, B))
    assert lists[R] == frozenset((A, B))

    assert all(g_edge(Q, anchor) for anchor in S)
    assert all(g_edge(V, anchor) for anchor in S)
    assert h_edge(Q, V)
    assert h_edge(C, R)
    assert h_edge(Q, Z) and h_edge(Z, R)
    assert g_edge(V, R)

    parity = same_sign_component()
    assert parity[Q] == parity[R] == 0
    assert parity[Z] == 1
    all_physical = sorted(
        vertex
        for vertex, vertex_list in lists.items()
        if vertex_list == lists[Q] and h_edge(C, vertex)
    )
    assert all_physical == [Z, R]
    same_sign_physical = sorted(
        vertex
        for vertex, vertex_list in lists.items()
        if vertex_list == lists[Q]
        and h_edge(C, vertex)
        and parity.get(vertex) == parity[Q]
    )
    assert same_sign_physical == [R]
    assert all(g_edge(V, vertex) for vertex in same_sign_physical)

    common = common_h_witnesses()
    assert len(common) == N * (N - 1) // 2

    family_payload = serialize_family().encode("ascii")
    assert graph6() == "LFzJbZYhdrDZdM"
    assert len(FAMILY) == 142
    assert sha256(family_payload).hexdigest() == (
        "9e49fca49aceff56168e0aef5cd825b5a55ec73a901985daec7bc03a9022e4aa"
    )
    result = {
        "classification": "exact equality control; not a counterexample",
        "graph6_G": graph6(),
        "order": N,
        "connected": True,
        "size": sum(g_edge(x, y) for x, y in combinations(range(N), 2)),
        "parameters": {
            "gamma": 3,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        },
        "words": [list(word) for word in WORDS],
        "extra_G_edges": [sorted(edge) for edge in sorted(
            EXTRA_G_EDGES, key=lambda edge: tuple(sorted(edge))
        )],
        "partition_family_sizes": [len(F0), len(F1)],
        "union_family_size": len(FAMILY),
        "family_sha256": sha256(family_payload).hexdigest(),
        "one_guard_obligations": len(FAMILY) * (N - 3),
        "lists_at_S": {
            str(vertex): sorted(vertex_list)
            for vertex, vertex_list in lists.items()
        },
        "transport_failure": {
            "neutral_port": Q,
            "cross_port": V,
            "omitted_anchor": C,
            "qv_is_H_edge": h_edge(Q, V),
            "same_sign_physical_representatives": same_sign_physical,
            "representative_to_cross_port_is_G_edge": g_edge(R, V),
            "even_H_path": [Q, Z, R],
        },
        "common_H_neighbor_certificate": common,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
