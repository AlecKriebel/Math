#!/usr/bin/env python3
"""Enumerate necessary seven-vertex terminal-cube patterns.

This is a deliberately relaxed local search.  It keeps only the anchors
``a,b,c``, one full target ``x``, and one rainbow terminal for each color.
For each of the 27 possible nonempty nonfull terminal response-list
patterns containing its assigned color, it asks whether some graph on
these seven vertices has a one-guard safe family with exactly those direct
lists.

External vertices and their attacks are omitted.  Consequently, SAT
patterns are only local controls, while an UNSAT pattern is a valid
necessary-pattern exclusion.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


ANCHORS = (0, 1, 2)
X = 3
TERMINALS = (4, 5, 6)
VERTICES = tuple(range(7))
S = frozenset(ANCHORS)
TRIPLES = tuple(frozenset(t) for t in itertools.combinations(VERTICES, 3))
PAIR_UNIVERSE = tuple(itertools.combinations(VERTICES, 2))
UNKNOWN_PAIRS = tuple(
    sorted(
        [
            *(tuple(sorted((a, r))) for a in ANCHORS for r in TERMINALS),
            *itertools.combinations(TERMINALS, 2),
        ]
    )
)


def direct_state(guard: int, target: int) -> frozenset[int]:
    return (S - {guard}) | {target}


def dominates(state: frozenset[int], edges: frozenset[tuple[int, int]]) -> bool:
    for vertex in VERTICES:
        if vertex in state:
            continue
        if not any(tuple(sorted((vertex, guard))) in edges for guard in state):
            return False
    return True


def alpha_at_most_three(edges: frozenset[tuple[int, int]]) -> bool:
    for four in itertools.combinations(VERTICES, 4):
        if all(tuple(sorted(pair)) not in edges for pair in itertools.combinations(four, 2)):
            return False
    return True


def safe_kernel(
    edges: frozenset[tuple[int, int]],
    forbidden: frozenset[frozenset[int]],
) -> tuple[frozenset[frozenset[int]], tuple[int, ...]]:
    current = {
        state
        for state in TRIPLES
        if state not in forbidden and dominates(state, edges)
    }
    rounds: list[int] = []
    while True:
        deleted = set()
        for state in current:
            for attack in VERTICES:
                if attack in state:
                    continue
                if not any(
                    tuple(sorted((guard, attack))) in edges
                    and (state - {guard}) | {attack} in current
                    for guard in state
                ):
                    deleted.add(state)
                    break
        if not deleted:
            return frozenset(current), tuple(rounds)
        rounds.append(len(deleted))
        current.difference_update(deleted)


def edge_name(pair: tuple[int, int]) -> str:
    names = ("a", "b", "c", "x", "r_a", "r_b", "r_c")
    return names[pair[0]] + names[pair[1]]


def list_name(response_list: frozenset[int]) -> str:
    names = "abc"
    return "".join(names[i] for i in sorted(response_list))


def enumerate_patterns() -> dict[str, object]:
    choices = tuple(
        frozenset(choice)
        for choice in ((0,), (0, 1), (0, 2))
    )
    per_terminal = {
        assigned: tuple(
            frozenset({assigned})
            | frozenset(extra)
            for extra in ((), ((assigned + 1) % 3,), ((assigned + 2) % 3,))
        )
        for assigned in ANCHORS
    }
    # Normalize the order to singleton, then the two lexicographic pairs.
    per_terminal = {
        assigned: tuple(sorted(set(values), key=lambda value: (len(value), tuple(value))))
        for assigned, values in per_terminal.items()
    }
    assert len(choices) == 3

    fixed_edges = frozenset(tuple(sorted((X, anchor))) for anchor in ANCHORS)
    records = []
    for lists_tuple in itertools.product(*(per_terminal[i] for i in ANCHORS)):
        response_lists = {
            terminal: lists_tuple[assigned]
            for assigned, terminal in enumerate(TERMINALS)
        }
        required_edges = fixed_edges | frozenset(
            tuple(sorted((anchor, terminal)))
            for terminal, response_list in response_lists.items()
            for anchor in response_list
        )
        forbidden = frozenset(
            direct_state(anchor, terminal)
            for terminal, response_list in response_lists.items()
            for anchor in ANCHORS
            if anchor not in response_list
        )
        required_states = frozenset(
            {S}
            | {direct_state(anchor, X) for anchor in ANCHORS}
            | {
                direct_state(anchor, terminal)
                for terminal, response_list in response_lists.items()
                for anchor in response_list
            }
        )
        free_pairs = tuple(pair for pair in UNKNOWN_PAIRS if pair not in required_edges)
        witness = None
        graphs_tested = 0
        for mask in range(1 << len(free_pairs)):
            edges = set(required_edges)
            edges.update(
                pair
                for bit, pair in enumerate(free_pairs)
                if (mask >> bit) & 1
            )
            frozen_edges = frozenset(edges)
            graphs_tested += 1
            if not alpha_at_most_three(frozen_edges):
                continue
            kernel, rounds = safe_kernel(frozen_edges, forbidden)
            if required_states <= kernel:
                witness = {
                    "edges": [edge_name(pair) for pair in sorted(frozen_edges)],
                    "kernel_size": len(kernel),
                    "deletion_round_sizes": list(rounds),
                }
                break
        records.append(
            {
                "lists": [
                    list_name(response_lists[terminal])
                    for terminal in TERMINALS
                ],
                "status": "SAT_LOCAL_CONTROL" if witness else "UNSAT_LOCAL_EXCLUSION",
                "graphs_tested": graphs_tested,
                "witness": witness,
            }
        )

    return {
        "model": "one-guard-moves; attacks only at unoccupied core vertices",
        "scope": {
            "vertices": ["a", "b", "c", "x", "r_a", "r_b", "r_c"],
            "fixed": [
                "a,b,c are pairwise nonadjacent in G",
                "x is G-adjacent to a,b,c",
                "x is G-nonadjacent to r_a,r_b,r_c",
                "alpha of the seven-vertex induced graph is at most 3",
                "S and every direct state named by a response list survive",
                "every unlisted direct state is banned",
            ],
            "relaxation": "external vertices, external attacks, and external domination are omitted",
        },
        "pattern_count": len(records),
        "unsat_count": sum(record["status"].startswith("UNSAT") for record in records),
        "sat_count": sum(record["status"].startswith("SAT") for record in records),
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = enumerate_patterns()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check is not None:
        expected = args.check.read_text(encoding="utf-8")
        if payload != expected:
            raise SystemExit("mismatch")
        print("PASS")
    elif args.output is not None:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
