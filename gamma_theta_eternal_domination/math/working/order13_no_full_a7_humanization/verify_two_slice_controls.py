#!/usr/bin/env python3
"""Directly verify the three two-anchor-slice SAT controls.

This checker ignores the SAT move variables.  It reconstructs G and the
selected triple family from each model, checks graph parameters by exhaustive
standard-library routines, and replays every required one-guard response from
the definition.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 13
S = frozenset((0, 1, 2))
PAIRS = tuple(itertools.combinations(range(N), 2))
TRIPLES = tuple(itertools.combinations(range(N), 3))
FAMILY_START = len(PAIRS) + len(PAIRS) * (N - 2) + 1
CONTROLS = {
    "01": frozenset((0, 1)),
    "02": frozenset((0, 2)),
    "12": frozenset((1, 2)),
}


def read_positive(path: Path) -> frozenset[int]:
    positive: set[int] = set()
    seen: set[int] = set()
    status = None
    for raw in path.read_text(encoding="ascii").splitlines():
        fields = raw.split()
        if not fields:
            continue
        if fields[0] == "s":
            status = " ".join(fields[1:])
        elif fields[0] == "v":
            for text in fields[1:]:
                literal = int(text)
                if literal == 0:
                    continue
                variable = abs(literal)
                if variable in seen:
                    raise AssertionError(f"duplicate variable {variable}")
                seen.add(variable)
                if literal > 0:
                    positive.add(variable)
    if status != "SATISFIABLE":
        raise AssertionError(f"{path} has status {status!r}")
    if seen != set(range(1, 9803)):
        raise AssertionError(f"{path} does not assign all 9802 variables")
    return frozenset(positive)


def reconstruct(
    positive: frozenset[int],
) -> tuple[tuple[int, ...], frozenset[frozenset[int]]]:
    h_edges = {
        pair
        for variable, pair in enumerate(PAIRS, start=1)
        if variable in positive
    }
    adjacency = [0] * N
    for u, v in PAIRS:
        if (u, v) in h_edges:
            continue
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    family = frozenset(
        frozenset(state)
        for index, state in enumerate(TRIPLES)
        if FAMILY_START + index in positive
    )
    return tuple(adjacency), family


def dominates(adjacency: tuple[int, ...], state: frozenset[int]) -> bool:
    covered = sum(1 << vertex for vertex in state)
    for vertex in state:
        covered |= adjacency[vertex]
    return covered == (1 << N) - 1


def domination_number(adjacency: tuple[int, ...]) -> int:
    for size in range(1, N + 1):
        if any(
            dominates(adjacency, frozenset(state))
            for state in itertools.combinations(range(N), size)
        ):
            return size
    raise AssertionError


def independent(adjacency: tuple[int, ...], state: frozenset[int]) -> bool:
    return all(
        not adjacency[u] & (1 << v)
        for u, v in itertools.combinations(state, 2)
    )


def independence_number(adjacency: tuple[int, ...]) -> int:
    return max(
        size
        for size in range(N + 1)
        if any(
            independent(adjacency, frozenset(state))
            for state in itertools.combinations(range(N), size)
        )
    )


def independent_domination_number(adjacency: tuple[int, ...]) -> int:
    for size in range(1, N + 1):
        for state in itertools.combinations(range(N), size):
            frozen = frozenset(state)
            if independent(adjacency, frozen) and dominates(adjacency, frozen):
                return size
    raise AssertionError


def colorable_h(adjacency_g: tuple[int, ...], colors: int) -> bool:
    full = (1 << N) - 1
    adjacency_h = tuple(
        (full ^ (1 << vertex)) & ~adjacency_g[vertex]
        for vertex in range(N)
    )
    assignments = [-1] * N

    def search(colored: int) -> bool:
        if colored == N:
            return True
        uncolored = [v for v in range(N) if assignments[v] < 0]
        vertex = max(
            uncolored,
            key=lambda v: sum(
                assignments[w] >= 0
                for w in range(N)
                if adjacency_h[v] & (1 << w)
            ),
        )
        forbidden = {
            assignments[w]
            for w in range(N)
            if adjacency_h[vertex] & (1 << w) and assignments[w] >= 0
        }
        for color in range(colors):
            if color in forbidden:
                continue
            assignments[vertex] = color
            if search(colored + 1):
                return True
            assignments[vertex] = -1
        return False

    return search(0)


def theta(adjacency: tuple[int, ...]) -> int:
    for colors in range(1, N + 1):
        if colorable_h(adjacency, colors):
            return colors
    raise AssertionError


def eternal_kernel(
    adjacency: tuple[int, ...], size: int
) -> frozenset[frozenset[int]]:
    active = {
        frozenset(state)
        for state in itertools.combinations(range(N), size)
        if dominates(adjacency, frozenset(state))
    }
    while True:
        kept = set()
        for state in active:
            good = True
            for attacked in set(range(N)) - state:
                if not any(
                    adjacency[guard] & (1 << attacked)
                    and frozenset((state - {guard}) | {attacked}) in active
                    for guard in state
                ):
                    good = False
                    break
            if good:
                kept.add(state)
        if kept == active:
            return frozenset(active)
        active = kept


def eternal_number(adjacency: tuple[int, ...]) -> int:
    for size in range(domination_number(adjacency), N + 1):
        if eternal_kernel(adjacency, size):
            return size
    raise AssertionError


def signature(adjacency: tuple[int, ...], vertex: int) -> frozenset[int]:
    return frozenset(
        anchor
        for anchor in S
        if not adjacency[vertex] & (1 << anchor)
    )


def response_list(
    family: frozenset[frozenset[int]], target: int
) -> frozenset[int]:
    return frozenset(
        anchor
        for anchor in S
        if frozenset((S - {anchor}) | {target}) in family
    )


def verify_control(tag: str, retained: frozenset[int]) -> dict[str, object]:
    model = HERE / f"closure-radius-2-anchors-{tag}.model"
    adjacency, family = reconstruct(read_positive(model))
    if S not in family:
        raise AssertionError("anchor state absent")
    if not all(dominates(adjacency, state) for state in family):
        raise AssertionError("selected non-dominating state")

    expected_signatures = {
        3: frozenset((0,)),
        4: frozenset((0,)),
        5: frozenset((2,)),
        6: frozenset((2,)),
    }
    for vertex, expected in expected_signatures.items():
        if signature(adjacency, vertex) != expected:
            raise AssertionError((vertex, signature(adjacency, vertex), expected))
    if adjacency[3] & (1 << 4) or adjacency[5] & (1 << 6):
        raise AssertionError("mate edge is in G rather than H")
    if response_list(family, 3) != frozenset((1, 2)):
        raise AssertionError("wrong list at port 3")
    if response_list(family, 5) != frozenset((0, 1)):
        raise AssertionError("wrong list at port 5")
    lists = {target: response_list(family, target) for target in range(3, N)}
    if any(not values or len(values) == 3 for values in lists.values()):
        raise AssertionError("not in exact no-full branch")
    signatures = {target: signature(adjacency, target) for target in range(3, N)}
    encoded = [
        sum(1 << anchor for anchor in signatures[target])
        for target in range(7, N)
    ]
    if encoded != sorted(encoded) or encoded[3] == 0:
        raise AssertionError("signature sorter or neutral cap failed")

    failures: list[tuple[tuple[int, ...], int]] = []
    retained_obligations = 0
    for state in family:
        for attacked in set(range(N)) - state:
            replies = [
                guard
                for guard in state
                if adjacency[guard] & (1 << attacked)
                and frozenset((state - {guard}) | {attacked}) in family
            ]
            if state & S and state & retained:
                retained_obligations += 1
                if not replies:
                    raise AssertionError(
                        f"required closure failed at {sorted(state)}, {attacked}"
                    )
            elif not replies:
                failures.append((tuple(sorted(state)), attacked))
    if not failures:
        raise AssertionError("control accidentally has full eternal closure")
    if any(frozenset(state) & retained for state, _ in failures):
        raise AssertionError("failure is inside a retained anchor slice")
    missing_anchor = next(iter(S - retained))
    missing_slice_failures = [
        (state, attack)
        for state, attack in failures
        if missing_anchor in state and not frozenset(state) & retained
    ]
    if not missing_slice_failures:
        raise AssertionError("no failure in the omitted anchor-only slice")

    parameters = {
        "gamma": domination_number(adjacency),
        "i": independent_domination_number(adjacency),
        "alpha": independence_number(adjacency),
        "gamma_infinity": eternal_number(adjacency),
        "theta": theta(adjacency),
    }
    if parameters != {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 4,
        "theta": 4,
    }:
        raise AssertionError(parameters)
    return {
        "tag": tag,
        "retained_anchor_slices": sorted(retained),
        "selected_family_size": len(family),
        "retained_attack_obligations_checked": retained_obligations,
        "full_closure_failure_count": len(failures),
        "omitted_anchor": missing_anchor,
        "omitted_anchor_slice_failure_count": len(missing_slice_failures),
        "first_full_closure_failures": [
            {"state": list(state), "attack": attack}
            for state, attack in sorted(failures)[:10]
        ],
        "all_failures_outside_retained_slices": True,
        "parameters": parameters,
        "neutral_vertices": [
            vertex for vertex, value in signatures.items() if not value
        ],
        "response_lists": {
            str(vertex): sorted(values) for vertex, values in lists.items()
        },
    }


def main() -> None:
    results = [
        verify_control(tag, retained) for tag, retained in CONTROLS.items()
    ]
    payload = {
        "status": "PASS",
        "scope": (
            "Direct verification that each two-of-three anchor-slice "
            "relaxation has a static (gamma,i,alpha,gamma_infinity,theta)="
            "(3,3,3,4,4) control and fails closure only outside the retained "
            "slices."
        ),
        "controls": results,
    }
    raw = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    (HERE / "two-slice-controls-result.json").write_text(
        raw, encoding="utf-8"
    )
    print(raw, end="")


if __name__ == "__main__":
    main()
