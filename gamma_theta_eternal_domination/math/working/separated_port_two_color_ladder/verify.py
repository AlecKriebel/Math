#!/usr/bin/env python3
"""Independent ordinary-set verifier for the safe-return near-miss."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


N = 11
S = frozenset((0, 1, 2))
A, B, C = 0, 1, 2
X, R, T, Q, V0, V1, Z, W = 3, 4, 5, 6, 7, 8, 9, 10

H_EDGES = frozenset(
    {
        (A, B),
        (A, C),
        (B, C),
        (X, R),
        (R, T),
        (T, Q),
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
)

DESIRED_LISTS = {
    X: frozenset((A, B, C)),
    R: frozenset((A, B)),
    T: frozenset((A, B)),
    Q: frozenset((A, B)),
    V0: frozenset((B, C)),
    V1: frozenset((B, C)),
    Z: frozenset((A, B)),
    W: frozenset((B, C)),
}

THREE_COLORING = {
    A: 0,
    B: 1,
    C: 2,
    X: 2,
    R: 0,
    T: 1,
    Q: 2,
    V0: 1,
    V1: 0,
    Z: 2,
    W: 1,
}


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def h_edge(u: int, v: int) -> bool:
    return u != v and pair(u, v) in H_EDGES


def g_edge(u: int, v: int) -> bool:
    return u != v and not h_edge(u, v)


def h_neighbors(vertex: int) -> frozenset[int]:
    return frozenset(v for v in range(N) if h_edge(vertex, v))


def dominates(state: frozenset[int]) -> bool:
    return all(
        vertex in state or any(g_edge(vertex, guard) for guard in state)
        for vertex in range(N)
    )


def independent(state: frozenset[int]) -> bool:
    return all(
        not g_edge(u, v) for u, v in itertools.combinations(state, 2)
    )


def direct_swap(guard: int, target: int) -> frozenset[int]:
    return (S - {guard}) | {target}


def restricted_kernel() -> tuple[frozenset[frozenset[int]], tuple[int, ...]]:
    banned = {
        direct_swap(guard, target)
        for target, allowed in DESIRED_LISTS.items()
        for guard in S
        if guard not in allowed
    }
    family = {
        frozenset(state)
        for state in itertools.combinations(range(N), 3)
        if frozenset(state) not in banned and dominates(frozenset(state))
    }
    rounds: list[int] = []
    while True:
        dead = set()
        for state in family:
            for attack in set(range(N)) - state:
                if not any(
                    g_edge(guard, attack)
                    and (state - {guard}) | {attack} in family
                    for guard in state
                ):
                    dead.add(state)
                    break
        if not dead:
            return frozenset(family), tuple(rounds)
        rounds.append(len(dead))
        family.difference_update(dead)


def family_audit(family: frozenset[frozenset[int]]) -> int:
    obligations = 0
    for state in family:
        assert dominates(state)
        for attack in set(range(N)) - state:
            obligations += 1
            assert any(
                g_edge(guard, attack)
                and (state - {guard}) | {attack} in family
                for guard in state
            )
    return obligations


def response_lists(
    family: frozenset[frozenset[int]],
) -> dict[int, frozenset[int]]:
    return {
        target: frozenset(
            guard
            for guard in S
            if g_edge(guard, target)
            and direct_swap(guard, target) in family
        )
        for target in set(range(N)) - S
    }


def exact_parameter(kind: str) -> int:
    if kind == "gamma":
        for size in range(1, N + 1):
            if any(
                dominates(frozenset(state))
                for state in itertools.combinations(range(N), size)
            ):
                return size
    elif kind == "alpha":
        for size in range(N, 0, -1):
            if any(
                independent(frozenset(state))
                for state in itertools.combinations(range(N), size)
            ):
                return size
    raise AssertionError(kind)


def graph6_g() -> str:
    bits = []
    for upper in range(1, N):
        for lower in range(upper):
            bits.append(int(g_edge(lower, upper)))
    while len(bits) % 6:
        bits.append(0)
    payload = "".join(
        chr(
            63
            + sum(
                bits[offset + shift] << (5 - shift)
                for shift in range(6)
            )
        )
        for offset in range(0, len(bits), 6)
    )
    return chr(63 + N) + payload


def odd_fan_embeddings(
    lists: dict[int, frozenset[int]],
) -> list[tuple[int, int, int, tuple[int, ...]]]:
    outside = set(range(N)) - S
    found = []
    for omitted in S:
        for positive, hub in itertools.permutations(outside, 2):
            if omitted not in lists[positive] or not h_edge(positive, hub):
                continue
            remaining = outside - {positive, hub}
            for path_order in range(2, len(remaining) + 1, 2):
                for path in itertools.permutations(remaining, path_order):
                    if any(omitted in lists[v] for v in path):
                        continue
                    if (
                        h_edge(hub, path[0])
                        and h_edge(hub, path[-1])
                        and all(
                            h_edge(path[i], path[i + 1])
                            for i in range(len(path) - 1)
                        )
                    ):
                        found.append((omitted, positive, hub, path))
    return found


def family_sha256(family: frozenset[frozenset[int]]) -> str:
    payload = "".join(
        ",".join(map(str, sorted(state))) + "\n"
        for state in sorted(family, key=lambda item: tuple(sorted(item)))
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    assert all(u < v for u, v in H_EDGES)
    assert not any(
        all(h_edge(u, v) for u, v in itertools.combinations(quad, 2))
        for quad in itertools.combinations(range(N), 4)
    )

    family, rounds = restricted_kernel()
    obligations = family_audit(family)
    lists = response_lists(family)
    assert lists == DESIRED_LISTS
    assert len(family) == 109
    assert rounds == (20, 4, 5, 5, 2)
    assert obligations == 872

    gamma = exact_parameter("gamma")
    alpha = exact_parameter("alpha")
    assert gamma == 2
    assert alpha == 3
    assert dominates(frozenset((A, X)))
    assert all(h_neighbors(v) for v in range(N))

    assert all(
        THREE_COLORING[u] != THREE_COLORING[v] for u, v in H_EDGES
    )
    assert len({THREE_COLORING[v] for v in S}) == 3

    bow_tie = frozenset((X, R, W, Z, V1))
    bow_tie_h_edges = frozenset(
        pair(u, v)
        for u, v in itertools.combinations(bow_tie, 2)
        if h_edge(u, v)
    )
    assert bow_tie_h_edges == frozenset(
        {
            pair(X, R),
            pair(X, W),
            pair(R, W),
            pair(Z, V1),
            pair(Z, W),
            pair(V1, W),
        }
    )
    assert all(
        h_neighbors(u) & h_neighbors(v)
        for u, v in itertools.combinations(bow_tie, 2)
    )

    assert h_edge(V0, V1) and h_edge(V1, W) and not h_edge(V0, W)
    assert h_edge(Z, V0) and h_edge(Z, V1) and h_edge(Z, W)
    assert not (h_neighbors(R) & h_neighbors(T))
    assert not (h_neighbors(T) & h_neighbors(Q))

    embeddings = odd_fan_embeddings(lists)
    assert not embeddings
    assert graph6_g() == "JFzvvn{~fM?"

    result = {
        "status": "PASS",
        "labeled_graph6_G": graph6_g(),
        "H_edges": [list(edge) for edge in sorted(H_EDGES)],
        "family": {
            "states": len(family),
            "sha256": family_sha256(family),
            "attack_obligations": obligations,
            "restricted_kernel_deletion_rounds": list(rounds),
        },
        "parameters": {
            "gamma": gamma,
            "alpha": alpha,
            "gamma_infinity": 3,
            "theta": 3,
        },
        "response_lists": {
            str(vertex): sorted(colors) for vertex, colors in lists.items()
        },
        "theta_witness_H_coloring": [
            THREE_COLORING[v] for v in range(N)
        ],
        "dominating_pair_G": [A, X],
        "safe_return": {
            "bow_tie_vertices": sorted(bow_tie),
            "bow_tie_H_edges": [
                list(edge) for edge in sorted(bow_tie_h_edges)
            ],
            "W_a_even_path": [V0, V1, W],
            "repeated_cap": Z,
            "link_positive": R,
        },
        "c_connector_common_H_neighbors": {
            "r_t": sorted(h_neighbors(R) & h_neighbors(T)),
            "t_q": sorted(h_neighbors(T) & h_neighbors(Q)),
        },
        "odd_fan_path_embeddings": embeddings,
        "verifier_sha256": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
    }
    assert result["parameters"] == {
        "gamma": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
