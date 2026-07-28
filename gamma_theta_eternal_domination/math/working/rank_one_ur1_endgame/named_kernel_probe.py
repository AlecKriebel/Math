#!/usr/bin/env python3
"""Discovery probe for finite attack trees on the eight fresh-witness labels.

For each assignment of the still optional named edges, compute the greatest
one-guard kernel using only attacks at named vertices.  A triple is initially
deleted when it misses a named vertex.  This deliberately ignores every
external vertex, so deletion of a required state is a sound local
contradiction, while survival proves nothing.
"""

from __future__ import annotations

import argparse
import collections
import itertools
import json


NAMES = ("u", "x", "p", "q", "r", "a", "b", "c")
INDEX = {name: position for position, name in enumerate(NAMES)}


def pair(left, right):
    return tuple(sorted((INDEX[left], INDEX[right])))


def fixed_edges(case):
    present = {
        pair("u", "x"),
        pair("u", "r"),
        pair("u", "a"),
        pair("p", "r"),
        pair("p", "b"),
        pair("q", "r"),
        pair("q", "c"),
        pair("x", "a"),
    }
    if case == "AQ1":
        present.add(pair("x", "r"))
    absent = {
        pair("x", "p"),
        pair("x", "q"),
        pair("p", "q"),
        pair("a", "r"),
        pair("a", "p"),
        pair("a", "q"),
        pair("b", "u"),
        pair("b", "r"),
        pair("b", "q"),
        pair("c", "u"),
        pair("c", "r"),
        pair("c", "p"),
    }
    if case == "QQ1":
        absent.add(pair("x", "r"))
    return present, absent


def kernel(edges):
    vertices = range(len(NAMES))
    states = tuple(itertools.combinations(vertices, 3))
    surviving = {
        state
        for state in states
        if all(
            target in state
            or any(tuple(sorted((guard, target))) in edges for guard in state)
            for target in vertices
        )
    }
    ranks = {state: 0 for state in states if state not in surviving}
    round_number = 0
    deleting_rows = {}
    while True:
        remove = {}
        for state in surviving:
            occupied = set(state)
            for target in vertices:
                if target in occupied:
                    continue
                successors = [
                    tuple(sorted((occupied - {guard}) | {target}))
                    for guard in state
                    if tuple(sorted((guard, target))) in edges
                ]
                if all(successor not in surviving for successor in successors):
                    remove[state] = (target, successors)
                    break
        if not remove:
            break
        round_number += 1
        for state, row in remove.items():
            surviving.remove(state)
            ranks[state] = round_number
            deleting_rows[state] = row
    return surviving, ranks, deleting_rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("QQ1", "AQ1"), required=True)
    parser.add_argument("--force-absent", action="append", default=[])
    arguments = parser.parse_args()
    present, absent = fixed_edges(arguments.case)
    for item in arguments.force_absent:
        left, right = item.split(",")
        absent.add(pair(left, right))
    all_pairs = set(itertools.combinations(range(len(NAMES)), 2))
    optional = sorted(all_pairs - present - absent)
    required = {
        tuple(sorted(INDEX[name] for name in state))
        for state in (
            ("x", "p", "q"),
            ("x", "b", "q"),
            ("x", "p", "c"),
            ("u", "b", "c"),
            ("r", "b", "c"),
            ("a", "p", "q"),
        )
    }
    bad_assignments = []
    surviving_assignments = []
    for bits in range(1 << len(optional)):
        edges = set(present)
        edges.update(
            edge for offset, edge in enumerate(optional) if bits & (1 << offset)
        )
        surviving, ranks, rows = kernel(edges)
        failed = sorted(required - surviving)
        row = {
            "present_optional": [
                [NAMES[left], NAMES[right]]
                for left, right in optional
                if tuple(sorted((left, right))) in edges
            ],
            "failed_required": [
                [NAMES[vertex] for vertex in state] for state in failed
            ],
            "ranks": {
                "".join(NAMES[vertex] for vertex in state): ranks[state]
                for state in failed
            },
        }
        if failed:
            bad_assignments.append(row)
        else:
            surviving_assignments.append(row)
    result = {
        "schema": "rank-one-ur1-named-kernel-probe-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "case": arguments.case,
        "forced_absent": arguments.force_absent,
        "optional_edges": [
            [NAMES[left], NAMES[right]] for left, right in optional
        ],
        "assignments": 1 << len(optional),
        "locally_contradictory": len(bad_assignments),
        "locally_surviving": len(surviving_assignments),
        "failure_signatures": [
            {
                "failed_required": json.loads(signature),
                "count": count,
            }
            for signature, count in sorted(
                collections.Counter(
                    json.dumps(row["failed_required"], sort_keys=True)
                    for row in bad_assignments
                ).items()
            )
        ],
        "surviving_examples": surviving_assignments[:20],
        "bad_examples": bad_assignments[:20],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
