#!/usr/bin/env python3
"""Clean-room replay of all induced two-vertex extensions of the core.

The generator and static filter are independently derived.  Only the six
static survivors enter the ordinary-set one-guard kernel implementation.
No code is imported from the target search.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


OLD_N = 9
N = 11
VERTICES = tuple(range(N))
ANCHORS = frozenset((0, 1, 2))
BASE_H = frozenset(
    {
        (0, 1),
        (0, 2),
        (1, 2),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 8),
        (7, 8),
        (4, 7),
    }
)
HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
TARGET_DIR = CAMPAIGN / "math" / "working" / "gamma3_port_identification_proof"
TARGET_SOURCE = TARGET_DIR / "two_vertex_extensions.py"
TARGET_RESULT = TARGET_DIR / "two_vertex_extensions_result.json"


def pair(u: int, v: int) -> tuple[int, int]:
    assert u != v
    return (u, v) if u < v else (v, u)


def old_adjacency() -> tuple[int, ...]:
    masks = [0] * N
    for u, v in BASE_H:
        masks[u] |= 1 << v
        masks[v] |= 1 << u
    return tuple(masks)


BASE_MASKS = old_adjacency()
OLD_TRIANGLES = tuple(
    triple
    for triple in itertools.combinations(range(OLD_N), 3)
    if all(pair(u, v) in BASE_H for u, v in itertools.combinations(triple, 2))
)


def decode(code: int) -> tuple[int, int, bool, tuple[int, ...]]:
    neighbors_9 = code & ((1 << OLD_N) - 1)
    neighbors_10 = (code >> OLD_N) & ((1 << OLD_N) - 1)
    mutual = bool((code >> (2 * OLD_N)) & 1)
    reconstructed = (
        neighbors_9
        | (neighbors_10 << OLD_N)
        | (int(mutual) << (2 * OLD_N))
    )
    assert reconstructed == code

    masks = list(BASE_MASKS)
    masks[9] = neighbors_9
    masks[10] = neighbors_10
    for old in range(OLD_N):
        if neighbors_9 & (1 << old):
            masks[old] |= 1 << 9
        if neighbors_10 & (1 << old):
            masks[old] |= 1 << 10
    if mutual:
        masks[9] |= 1 << 10
        masks[10] |= 1 << 9
    return neighbors_9, neighbors_10, mutual, tuple(masks)


def no_k4_extension(
    neighbors_9: int, neighbors_10: int, mutual: bool
) -> bool:
    # The fixed old graph has no K4.  A K4 with one new vertex consists of
    # that vertex plus an old triangle.  A K4 with both new vertices exists
    # exactly when they are adjacent and their common old neighborhood
    # contains an old H-edge.
    for triangle in OLD_TRIANGLES:
        triangle_mask = sum(1 << v for v in triangle)
        if neighbors_9 & triangle_mask == triangle_mask:
            return False
        if neighbors_10 & triangle_mask == triangle_mask:
            return False
    if mutual:
        common = neighbors_9 & neighbors_10
        if any(
            common & (1 << u) and common & (1 << v)
            for u, v in BASE_H
        ):
            return False
    return True


def every_pair_has_common_h_neighbor(h: tuple[int, ...]) -> bool:
    return all(
        h[u] & h[v]
        for u, v in itertools.combinations(VERTICES, 2)
    )


def h_edges(h: tuple[int, ...]) -> frozenset[tuple[int, int]]:
    return frozenset(
        (u, v)
        for u, v in itertools.combinations(VERTICES, 2)
        if h[u] & (1 << v)
    )


def g_neighbors(h: tuple[int, ...]) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(
            v
            for v in VERTICES
            if v != u and not (h[u] & (1 << v))
        )
        for u in VERTICES
    )


def dominates(state: frozenset[int], g: tuple[frozenset[int], ...]) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(g[guard])
    return len(covered) == N


def independent(
    state: frozenset[int], g: tuple[frozenset[int], ...]
) -> bool:
    return all(
        v not in g[u] for u, v in itertools.combinations(sorted(state), 2)
    )


def exact_gamma(g: tuple[frozenset[int], ...]) -> int:
    for size in range(1, N + 1):
        if any(
            dominates(frozenset(state), g)
            for state in itertools.combinations(VERTICES, size)
        ):
            return size
    raise AssertionError("gamma")


def exact_alpha(g: tuple[frozenset[int], ...]) -> int:
    for size in range(N, 0, -1):
        if any(
            independent(frozenset(state), g)
            for state in itertools.combinations(VERTICES, size)
        ):
            return size
    raise AssertionError("alpha")


def greatest_triple_kernel(
    g: tuple[frozenset[int], ...],
) -> tuple[frozenset[frozenset[int]], dict[frozenset[int], int], Counter[int]]:
    alive = {
        frozenset(state)
        for state in itertools.combinations(VERTICES, 3)
        if dominates(frozenset(state), g)
    }
    deletion_rank: dict[frozenset[int], int] = {}
    histogram: Counter[int] = Counter()
    round_number = 1
    while True:
        dead = set()
        for state in alive:
            for attack in set(VERTICES) - state:
                if not any(
                    attack in g[guard]
                    and (state - {guard}) | {attack} in alive
                    for guard in state
                ):
                    dead.add(state)
                    break
        if not dead:
            return frozenset(alive), deletion_rank, histogram
        for state in dead:
            deletion_rank[state] = round_number
        histogram[round_number] = len(dead)
        alive.difference_update(dead)
        round_number += 1


def has_k4_bruteforce(h: tuple[int, ...]) -> bool:
    return any(
        all(h[u] & (1 << v) for u, v in itertools.combinations(quad, 2))
        for quad in itertools.combinations(VERTICES, 4)
    )


def graph6_for_g(h: tuple[int, ...]) -> str:
    bits = [
        0 if h[i] & (1 << j) else 1
        for j in range(1, N)
        for i in range(j)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    body = "".join(
        chr(
            63
            + sum(
                bits[start + offset] << (5 - offset)
                for offset in range(6)
            )
        )
        for start in range(0, len(bits), 6)
    )
    return chr(63 + N) + body


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assert len(BASE_H) == 9
    assert OLD_TRIANGLES == ((0, 1, 2),)
    assert not any(
        all(pair(u, v) in BASE_H for u, v in itertools.combinations(quad, 2))
        for quad in itertools.combinations(range(OLD_N), 4)
    )

    static_survivors = []
    decoded_cases = 0
    for code in range(1 << 19):
        neighbors_9, neighbors_10, mutual, h = decode(code)
        decoded_cases += 1
        if not no_k4_extension(neighbors_9, neighbors_10, mutual):
            continue
        if not every_pair_has_common_h_neighbor(h):
            continue

        # A generic check, independent of the specialized K4 filter, is
        # cheap on the six survivors.
        assert not has_k4_bruteforce(h)
        assert h_edges(h) & {
            pair(u, v)
            for u, v in itertools.combinations(range(OLD_N), 2)
        } == BASE_H

        g = g_neighbors(h)
        gamma = exact_gamma(g)
        alpha = exact_alpha(g)
        assert (gamma, alpha) == (3, 3)

        kernel, ranks, histogram = greatest_triple_kernel(g)
        assert not kernel
        assert ranks[ANCHORS] == 2
        static_survivors.append(
            {
                "code": code,
                "graph6_G": graph6_for_g(h),
                "H_neighbors_9": [
                    v for v in VERTICES if h[9] & (1 << v)
                ],
                "H_neighbors_10": [
                    v for v in VERTICES if h[10] & (1 << v)
                ],
                "gamma": gamma,
                "alpha": alpha,
                "kernel_size": len(kernel),
                "reference_state_deletion_rank": ranks[ANCHORS],
                "deletion_round_histogram": {
                    str(round_number): count
                    for round_number, count in sorted(histogram.items())
                },
            }
        )

    assert decoded_cases == 1 << 19
    assert len(static_survivors) == 6

    target = json.loads(TARGET_RESULT.read_text(encoding="utf-8"))
    assert target["scope"] == {
        "extensions": 524288,
        "new_order": 11,
        "old_induced_H_exact": True,
        "old_order": 9,
    }
    assert target["counts"] == {
        "eternal_equality_3": 0,
        "exact_old_response_lists": 0,
        "full_x_in_greatest_family": 0,
        "static_gamma_alpha_3": 6,
    }
    assert target["source_sha256"] == sha256(TARGET_SOURCE)

    target_records = target["static_records"]
    assert [record["code"] for record in static_survivors] == [
        record["code"] for record in target_records
    ]
    for independent_record, target_record in zip(
        static_survivors, target_records
    ):
        for field in (
            "code",
            "graph6_G",
            "H_neighbors_9",
            "H_neighbors_10",
            "kernel_size",
            "reference_state_deletion_rank",
        ):
            assert independent_record[field] == target_record[field]

    result = {
        "status": "PASS",
        "implementation": (
            "clean-room 19-bit generator, specialized independently proved "
            "K4 filter, generic static checks, and ordinary-set one-guard "
            "kernel"
        ),
        "coverage": {
            "decoded_cases": decoded_cases,
            "factorization": "2^(9+9+1)",
            "old_induced_H_exact": True,
            "static_gamma_alpha_3": len(static_survivors),
        },
        "static_survivors": static_survivors,
        "conclusion": (
            "All six static gamma=alpha=3 extensions have empty greatest "
            "eternal triple kernels; the anchor triple is deleted in "
            "simultaneous round two in every case."
        ),
        "target_sha256": {
            "two_vertex_extensions.py": sha256(TARGET_SOURCE),
            "two_vertex_extensions_result.json": sha256(TARGET_RESULT),
        },
    }
    output = HERE / "two_vertex_addendum_result.json"
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
