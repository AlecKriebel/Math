#!/usr/bin/env python3
"""Clean-room graph/switching replay of the reduced cut-word palette.

No project graph, validity, mixed-reduction, or switching module is imported.
The five primitive arc lists are transcribed from the mathematical templates;
all rooted and fixed-mixed-graph predicates are implemented below.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path


PALETTE = ((), (0,), (1,), (0, 1), (1, 0))
CORES = (
    ("cycle", "S", ("X",), (("S", "X"), ("S", "X"))),
    (
        "theta_TR_nested", "P", ("Q",),
        (("U", "V"), ("U", "V"), ("P", "U"), ("P", "Q"), ("V", "Q")),
    ),
    (
        "theta_TR_separated", "P", ("Q",),
        (("U", "V"), ("P", "U"), ("P", "V"), ("U", "Q"), ("V", "Q")),
    ),
    (
        "theta_TT_nested", "P", ("Q", "R"),
        (("U", "V"), ("P", "U"), ("P", "Q"), ("V", "Q"), ("U", "R"), ("V", "R")),
    ),
    (
        "theta_TT_separated", "P", ("Q", "R"),
        (("P", "U"), ("P", "V"), ("U", "Q"), ("V", "Q"), ("U", "R"), ("V", "R")),
    ),
)


def degrees(arcs):
    incoming = Counter()
    outgoing = Counter()
    for tail, head in arcs:
        outgoing[tail] += 1
        incoming[head] += 1
        incoming.setdefault(tail, 0)
        outgoing.setdefault(head, 0)
    return incoming, outgoing


def descendants_without(arcs, start, forbidden=None):
    children = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    reached = set()
    pending = [start]
    while pending:
        vertex = pending.pop()
        if vertex == forbidden or vertex in reached:
            continue
        reached.add(vertex)
        pending.extend(children[vertex])
    return reached


def rooted_valid(arcs, root, leaves):
    vertices = {vertex for edge in arcs for vertex in edge}
    incoming, outgoing = degrees(arcs)
    if len(arcs) != len(set(arcs)) or any(tail == head for tail, head in arcs):
        return False
    if (incoming[root], outgoing[root]) != (0, 2):
        return False
    for vertex in vertices:
        bidegree = incoming[vertex], outgoing[vertex]
        if vertex in leaves:
            if bidegree != (1, 0):
                return False
        elif vertex != root and bidegree not in ((1, 2), (2, 1)):
            return False

    pending = dict(incoming)
    queue = [vertex for vertex in vertices if not pending[vertex]]
    visited = 0
    children = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    while queue:
        vertex = queue.pop()
        visited += 1
        for child in children[vertex]:
            pending[child] -= 1
            if not pending[child]:
                queue.append(child)
    if visited != len(vertices) or descendants_without(arcs, root) != vertices:
        return False

    # The root must be the lowest stable ancestor of all leaves.
    for candidate in vertices - set(leaves) - {root}:
        if not (descendants_without(arcs, root, candidate) & set(leaves)):
            return False

    # Tree-childness of this displayed rooted presentation.
    for vertex in vertices - set(leaves):
        if not any(child in leaves or incoming[child] == 1 for child in children[vertex]):
            return False
    return True


def fixed_mixed_strong(arcs, root, leaves):
    incoming, outgoing = degrees(arcs)
    reticulations = {
        vertex
        for vertex in set(incoming) | set(outgoing)
        if (incoming[vertex], outgoing[vertex]) == (2, 1)
    }
    retained = []
    root_incident = []
    for tail, head in arcs:
        edge = (frozenset((tail, head)), frozenset((head,)) if head in reticulations else frozenset())
        (root_incident if root in edge[0] else retained).append(edge)
    if len(root_incident) != 2:
        return False
    left = next(iter(root_incident[0][0] - {root}))
    right = next(iter(root_incident[1][0] - {root}))
    if left == right:
        return False
    inherited_heads = (root_incident[0][1] & {left}) | (root_incident[1][1] & {right})
    retained.append((frozenset((left, right)), inherited_heads))

    if len({edge[0] for edge in retained}) != len(retained):
        return False
    incidence = defaultdict(list)
    arrowheads = Counter()
    undirected = Counter()
    reticulation_tails = set()
    for endpoints, heads in retained:
        if len(heads) > 1:
            return False
        for vertex in endpoints:
            incidence[vertex].append((endpoints, heads))
        if heads:
            head = next(iter(heads))
            arrowheads[head] += 1
            reticulation_tails.update(endpoints - {head})
        else:
            for vertex in endpoints:
                undirected[vertex] += 1
    for vertex, edges in incidence.items():
        if vertex in leaves:
            if len(edges) != 1:
                return False
        elif len(edges) != 3 or arrowheads[vertex] not in (0, 2):
            return False
    return all(undirected[tail] == 2 for tail in reticulation_tails)


def build(core, words, extras, nonroot):
    name, source, sinks, segments = core
    arcs = []
    leaves = []
    colours = {}
    for segment_index, ((tail, head), word) in enumerate(zip(segments, words)):
        prior = tail
        for position, colour in enumerate(word):
            parent = f"w:{segment_index}:{position}"
            leaf = f"leaf:{len(leaves)}"
            arcs.extend(((prior, parent), (parent, leaf)))
            prior = parent
            leaves.append(leaf)
            colours[leaf] = int(colour)
        arcs.append((prior, head))
    offset = 0
    for sink in sinks:
        leaf = f"leaf:{len(leaves)}"
        arcs.append((sink, leaf))
        leaves.append(leaf)
        colours[leaf] = int(extras[offset])
        offset += 1
    root = source
    if nonroot:
        root = "root"
        leaf = f"leaf:{len(leaves)}"
        arcs.extend(((root, source), (root, leaf)))
        leaves.append(leaf)
        colours[leaf] = int(extras[offset])
    return name, tuple(arcs), root, frozenset(leaves), colours


def switching_splits(arcs, root, leaves):
    incoming, outgoing = degrees(arcs)
    reticulations = tuple(sorted(
        vertex
        for vertex in set(incoming) | set(outgoing)
        if (incoming[vertex], outgoing[vertex]) == (2, 1)
    ))
    parent_edges = {
        reticulation: tuple(
            index for index, (_tail, head) in enumerate(arcs) if head == reticulation
        )
        for reticulation in reticulations
    }
    leaf_index = {leaf: index for index, leaf in enumerate(sorted(leaves))}
    full = frozenset(leaf_index.values())
    answer = []
    for choice in itertools.product((0, 1), repeat=len(reticulations)):
        removed = {
            parent_edges[reticulation][1 - bit]
            for reticulation, bit in zip(reticulations, choice)
        }
        children = defaultdict(list)
        for index, (tail, head) in enumerate(arcs):
            if index not in removed:
                children[tail].append(head)
        memo = {}

        def below(vertex):
            if vertex not in memo:
                value = {leaf_index[vertex]} if vertex in leaf_index else set()
                for child in children[vertex]:
                    value.update(below(child))
                memo[vertex] = frozenset(value)
            return memo[vertex]

        splits = set()
        for index, (_tail, head) in enumerate(arcs):
            if index in removed:
                continue
            side = below(head)
            if side and side != full:
                splits.update((side, full - side))
        answer.append(frozenset(splits))
    return tuple(answer), leaf_index


def doubled_singleton(words, extras):
    locations = {0: [], 1: []}
    for segment, word in enumerate(words):
        for position, colour in enumerate(word):
            locations[colour].append((segment, position))
    for colour in extras:
        locations[colour].append(None)
    if any(not locations[colour] for colour in (0, 1)):
        return None
    result = [list(word) for word in words]
    changed = False
    for colour in (0, 1):
        if len(locations[colour]) != 1:
            continue
        location = locations[colour][0]
        if location is None:
            return None
        segment, position = location
        result[segment].insert(position, colour)
        changed = True
    return tuple(tuple(word) for word in result) if changed else None


def survives(arcs, root, leaves, colours):
    splits_by_switching, leaf_index = switching_splits(arcs, root, leaves)
    zero = frozenset(
        leaf_index[leaf]
        for leaf, colour in colours.items()
        if colour == 0
    )
    one = frozenset(leaf_index.values()) - zero
    return all(zero in splits or one in splits for splits in splits_by_switching)


def audit():
    rows = []
    failures = []
    commitment = hashlib.sha256()
    for core in CORES:
        name, _source, sinks, segments = core
        for nonroot in (False, True):
            extras_count = len(sinks) + int(nonroot)
            counts = Counter()
            survivors = []
            for words in itertools.product(PALETTE, repeat=len(segments)):
                for extras in itertools.product((0, 1), repeat=extras_count):
                    colours = tuple(value for word in words for value in word) + extras
                    balance = Counter(colours)
                    if min(balance[0], balance[1]) >= 2:
                        counts["balanced_compressed_checked"] += 1
                        _name, arcs, root, leaves, actual = build(core, words, extras, nonroot)
                        if rooted_valid(arcs, root, leaves) and fixed_mixed_strong(arcs, root, leaves):
                            counts["valid_balanced_compressed"] += 1
                            if survives(arcs, root, leaves, actual):
                                survivors.append([words, extras, "compressed"])
                    expanded = doubled_singleton(words, extras)
                    if expanded is None:
                        continue
                    _name, arcs, root, leaves, actual = build(core, expanded, extras, nonroot)
                    if rooted_valid(arcs, root, leaves) and fixed_mixed_strong(arcs, root, leaves):
                        counts["valid_singleton_doubled"] += 1
                        if survives(arcs, root, leaves, actual):
                            survivors.append([expanded, extras, "singleton_doubled"])
            record = {
                "core": name,
                "role": "nonroot" if nonroot else "root",
                **dict(sorted(counts.items())),
                "survivor_count": len(survivors),
            }
            rows.append(record)
            commitment.update(json.dumps(record, sort_keys=True, separators=(",", ":")).encode())
            if survivors:
                failures.append({"record": record, "survivors": survivors[:5]})
    return {
        "schema": "stc-jc-reduced-palette-cleanroom-v1",
        "status": "EXACTLY COMPUTED" if not failures else "FALSE",
        "palette": [list(word) for word in PALETTE],
        "families": rows,
        "total_valid_palette_presentations": sum(
            row.get("valid_balanced_compressed", 0)
            + row.get("valid_singleton_doubled", 0)
            for row in rows
        ),
        "survivor_count": sum(row["survivor_count"] for row in rows),
        "record_commitment_sha256": commitment.hexdigest(),
        "failures": failures,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.output.write_text(raw, encoding="utf-8")
    print(json.dumps({
        "status": payload["status"],
        "valid_palette_presentations": payload["total_valid_palette_presentations"],
        "survivors": payload["survivor_count"],
        "sha256": hashlib.sha256(raw.encode()).hexdigest(),
    }, indent=2, sort_keys=True))
    return 0 if payload["status"] == "EXACTLY COMPUTED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
