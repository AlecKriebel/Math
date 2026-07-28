#!/usr/bin/env python3
"""Clean-room replay of the two fixed collision-endgame controls.

This checker deliberately does not import the candidate evaluator.  Graphs
are represented by integer adjacency masks, configurations by integer masks,
and the synchronous kernel is rebuilt directly from the one-guard rule.
"""

from __future__ import annotations

import hashlib
import itertools
import json


def graph6_masks(text: str) -> tuple[int, ...]:
    """Decode a small graph6 record to one adjacency mask per vertex."""
    data = [ord(ch) - 63 for ch in text]
    if not data or not (0 <= data[0] < 63):
        raise ValueError("only single-byte graph6 orders are accepted")
    n = data[0]
    bitstream = "".join(f"{word:06b}" for word in data[1:])
    needed = n * (n - 1) // 2
    if len(bitstream) < needed or "1" in bitstream[needed:]:
        raise ValueError("malformed or noncanonical graph6 payload")
    rows = [0] * n
    cursor = 0
    for second in range(1, n):
        for first in range(second):
            if bitstream[cursor] == "1":
                rows[first] |= 1 << second
                rows[second] |= 1 << first
            cursor += 1
    return tuple(rows)


def masks_of_size(n: int, k: int) -> tuple[int, ...]:
    return tuple(
        sum(1 << v for v in choice)
        for choice in itertools.combinations(range(n), k)
    )


def vertices(mask: int) -> tuple[int, ...]:
    out: list[int] = []
    while mask:
        bit = mask & -mask
        out.append(bit.bit_length() - 1)
        mask ^= bit
    return tuple(out)


def is_independent(rows: tuple[int, ...], state: int) -> bool:
    return all((rows[v] & state & ~(1 << v)) == 0 for v in vertices(state))


def is_dominating(rows: tuple[int, ...], state: int) -> bool:
    covered = state
    for v in vertices(state):
        covered |= rows[v]
    return covered == (1 << len(rows)) - 1


def missed_vertices(rows: tuple[int, ...], state: int) -> tuple[int, ...]:
    covered = state
    for v in vertices(state):
        covered |= rows[v]
    return vertices(((1 << len(rows)) - 1) ^ covered)


def one_guard_successors(
    rows: tuple[int, ...], state: int, target: int
) -> tuple[tuple[int, int], ...]:
    if state & (1 << target):
        raise ValueError("attacks must be unoccupied")
    answer: list[tuple[int, int]] = []
    for guard in vertices(state):
        if rows[guard] & (1 << target):
            answer.append((guard, (state ^ (1 << guard)) | (1 << target)))
    return tuple(answer)


def greatest_kernel(
    rows: tuple[int, ...], k: int
) -> tuple[frozenset[int], dict[int, int]]:
    n = len(rows)
    live = {state for state in masks_of_size(n, k) if is_dominating(rows, state)}
    deletion_rank: dict[int, int] = {}
    round_index = 1
    while True:
        previous = frozenset(live)
        removed: set[int] = set()
        for state in previous:
            for target in range(n):
                if state & (1 << target):
                    continue
                if not any(
                    successor in previous
                    for _, successor in one_guard_successors(
                        rows, state, target
                    )
                ):
                    removed.add(state)
                    break
        if not removed:
            return frozenset(live), deletion_rank
        for state in removed:
            deletion_rank[state] = round_index
        live.difference_update(removed)
        round_index += 1


def minimum_subset_size(rows: tuple[int, ...], predicate) -> int:
    for k in range(1, len(rows) + 1):
        if any(predicate(state) for state in masks_of_size(len(rows), k)):
            return k
    raise AssertionError("full vertex set must be a witness")


def graph_parameters(
    rows: tuple[int, ...],
) -> tuple[dict[str, int], frozenset[int], dict[int, int]]:
    n = len(rows)
    gamma = minimum_subset_size(rows, lambda s: is_dominating(rows, s))
    independent_sets = {
        k: tuple(
            s for s in masks_of_size(n, k) if is_independent(rows, s)
        )
        for k in range(1, n + 1)
    }
    alpha = max(k for k, states in independent_sets.items() if states)
    indep_dom = minimum_subset_size(
        rows, lambda s: is_independent(rows, s) and is_dominating(rows, s)
    )
    kernels: dict[int, tuple[frozenset[int], dict[int, int]]] = {}
    eternal = None
    for k in range(1, n + 1):
        kernels[k] = greatest_kernel(rows, k)
        if eternal is None and kernels[k][0]:
            eternal = k
    assert eternal is not None
    triple_kernel, triple_ranks = kernels[3]
    return (
        {
            "gamma": gamma,
            "i": indep_dom,
            "alpha": alpha,
            "gamma_infinity": eternal,
        },
        triple_kernel,
        triple_ranks,
    )


def extended_rank(
    rows: tuple[int, ...],
    family: frozenset[int],
    deletion_rank: dict[int, int],
    state: int,
) -> int | str:
    if state in family:
        return "infinity"
    if not is_dominating(rows, state):
        return 0
    return deletion_rank[state]


def active(
    rows: tuple[int, ...],
    family: frozenset[int],
    source: int,
    target: int,
) -> bool:
    n = len(rows)
    for base in masks_of_size(n, 3):
        if not (base & (1 << source)) or base & (1 << target):
            continue
        if not is_independent(rows, base):
            continue
        successor = (base ^ (1 << source)) | (1 << target)
        if rows[source] & (1 << target) and successor in family:
            return True
    return False


def edge_list(rows: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (u, v)
        for u in range(len(rows))
        for v in range(u + 1, len(rows))
        if rows[u] & (1 << v)
    )


def edge_hash(rows: tuple[int, ...]) -> str:
    payload = "\n".join(f"{u} {v}" for u, v in edge_list(rows)) + "\n"
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def local_control(
    record: str, u: int, x: int, p: int, q: int, r: int
) -> dict[str, object]:
    rows = graph6_masks(record)
    params, family, ranks = graph_parameters(rows)
    endpoint = (1 << x) | (1 << p) | (1 << q)
    reverse = (1 << u) | (1 << p) | (1 << q)
    responses = []
    for guard, successor in one_guard_successors(rows, reverse, r):
        responses.append(
            {
                "guard": guard,
                "state": list(vertices(successor)),
                "rank": extended_rank(rows, family, ranks, successor),
                "missed": list(missed_vertices(rows, successor)),
            }
        )
    common = [
        c
        for c in range(len(rows))
        if c not in {x, r}
        and not rows[x] & (1 << c)
        and not rows[r] & (1 << c)
    ]
    return {
        "graph6": record,
        "order": len(rows),
        "size": len(edge_list(rows)),
        "edge_list": [list(edge) for edge in edge_list(rows)],
        "edge_list_sha256": edge_hash(rows),
        "parameters": params,
        "greatest_triple_family_size": len(family),
        "reverse_rank": extended_rank(rows, family, ranks, reverse),
        "endpoint_hits": [v for v in vertices(endpoint) if rows[r] & (1 << v)],
        "reverse_movers": [entry["guard"] for entry in responses],
        "successors": responses,
        "common_nonneighbors_xr_excluding_endpoints": common,
        "xr_dominates": is_dominating(rows, (1 << x) | (1 << r)),
        "activity": {
            "p_to_r": active(rows, family, p, r),
            "r_to_p": active(rows, family, r, p),
            "q_to_r": active(rows, family, q, r),
            "r_to_q": active(rows, family, r, q),
        },
    }


def main() -> None:
    gejbug = local_control("GEjbug", 0, 4, 3, 5, 7)
    static = local_control("GCOedo", 6, 0, 2, 1, 7)

    assert gejbug["parameters"] == {
        "gamma": 2,
        "i": 2,
        "alpha": 3,
        "gamma_infinity": 3,
    }
    assert gejbug["greatest_triple_family_size"] == 41
    assert gejbug["reverse_rank"] == 1
    assert gejbug["endpoint_hits"] == [3, 5]
    assert gejbug["reverse_movers"] == [0, 3, 5]
    assert [row["rank"] for row in gejbug["successors"]] == [0, 0, 0]
    assert [row["missed"] for row in gejbug["successors"]] == [[4], [6], [2]]
    assert gejbug["common_nonneighbors_xr_excluding_endpoints"] == []
    assert gejbug["xr_dominates"] is True
    assert gejbug["activity"] == {
        "p_to_r": True,
        "r_to_p": False,
        "q_to_r": True,
        "r_to_q": False,
    }

    assert static["parameters"] == {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 4,
    }
    assert static["greatest_triple_family_size"] == 0
    assert static["reverse_rank"] == 1
    assert static["endpoint_hits"] == [0, 2]
    assert static["reverse_movers"] == [2]
    assert static["successors"] == [
        {"guard": 2, "state": [1, 6, 7], "rank": 0, "missed": [5]}
    ]

    static_rows = graph6_masks("GCOedo")
    source = (1 << 5) | (1 << 6) | (1 << 7)
    failed = (1 << 0) | (1 << 5) | (1 << 7)
    assert is_independent(static_rows, source)
    assert not is_dominating(static_rows, failed)
    assert missed_vertices(static_rows, failed) == (1,)

    result = {
        "schema": "multi-hit-collision-hostile-clean-room-v1",
        "status": "VERIFIED_FIXED_CONTROLS",
        "model": {
            "attacks": "unoccupied vertices only",
            "move": "exactly one guard along one graph edge",
            "kernel": "literal synchronous greatest fixed point",
            "rank_zero": "non-dominating",
        },
        "GEjbug": gejbug,
        "GCOedo": {
            **static,
            "independent_private_witness_source": [5, 6, 7],
            "failed_forward_state": [0, 5, 7],
            "failed_forward_missed": [1],
        },
        "scope": {
            "proves": "only the two fixed graph controls",
            "does_not_prove": "any symbolic collision lemma",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
