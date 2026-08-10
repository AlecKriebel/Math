#!/usr/bin/env python3
"""Clean-room switching audit for the arbitrary pointwise cut argument.

The finite census is paired with an explicit run-compression lemma recorded
in the output.  It imports no historical graph, switching, Fourier, or rank
code and enforces the literal one-root-suppression convention.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Mapping, Sequence

from graph_conventions import rooted_checks, suppress_root_once, validate_literal_standard
from tensor_models import Core, load_cores


DEFAULT_PROJECT = Path(
    "/Users/alec/Documents/Math/strong_level2_phylo_identifiability"
)

SHORT_WORDS = {
    0: ((),),
    1: ((0,), (1,)),
    2: ((0, 1), (1, 0)),
}
BASE_WORDS = ((), (0,), (1,), (0, 1), (1, 0))


def file_hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def build_theta(
    core: Core, words: Sequence[Sequence[int]], nonroot: bool
):
    arcs: list[tuple[str, str]] = []
    leaves: list[str] = []
    colours: list[int] = []
    for segment, ((tail, head), word) in enumerate(zip(core.arcs, words)):
        chain = [tail]
        for position, colour in enumerate(word):
            parent = f"P_{segment}_{position}"
            leaf = f"L_{len(leaves)}"
            chain.append(parent)
            arcs.append((parent, leaf))
            leaves.append(leaf)
            colours.append(int(colour))
        chain.append(head)
        arcs.extend(zip(chain, chain[1:]))
    # Sink and incoming colours are supplied later because they are varied
    # independently of the segment words.
    sink_leaves = []
    for sink in core.sinks:
        leaf = f"L_{len(leaves)}"
        arcs.append((sink, leaf))
        leaves.append(leaf)
        sink_leaves.append(leaf)
    root = core.source
    incoming = None
    if nonroot:
        root = "AUDIT_ROOT"
        incoming = f"L_{len(leaves)}"
        arcs.extend(((root, core.source), (root, incoming)))
        leaves.append(incoming)
    labels = {leaf: index for index, leaf in enumerate(leaves, 1)}
    return root, tuple(arcs), labels, tuple(colours), tuple(sink_leaves), incoming


def build_cycle(words: Sequence[Sequence[int]], nonroot: bool):
    arcs: list[tuple[str, str]] = []
    leaves: list[str] = []
    colours: list[int] = []
    for side, word in enumerate(words):
        chain = ["S"]
        for position, colour in enumerate(word):
            parent = f"P_{side}_{position}"
            leaf = f"L_{len(leaves)}"
            chain.append(parent)
            arcs.append((parent, leaf))
            leaves.append(leaf)
            colours.append(int(colour))
        chain.append("X")
        arcs.extend(zip(chain, chain[1:]))
    sink_leaf = f"L_{len(leaves)}"
    arcs.append(("X", sink_leaf))
    leaves.append(sink_leaf)
    root = "S"
    incoming = None
    if nonroot:
        root = "AUDIT_ROOT"
        incoming = f"L_{len(leaves)}"
        arcs.extend(((root, "S"), (root, incoming)))
        leaves.append(incoming)
    labels = {leaf: index for index, leaf in enumerate(leaves, 1)}
    return root, tuple(arcs), labels, tuple(colours), (sink_leaf,), incoming


def literal_valid(root: str, arcs, labels) -> bool:
    rooted = rooted_checks(root, arcs, labels)
    if not rooted["valid"]:
        return False
    mixed, _reticulations = suppress_root_once(root, arcs)
    return bool(validate_literal_standard(mixed, labels)["valid_standard_strong"])


def switching_splits(arcs, labels):
    indegree = Counter(head for _tail, head in arcs)
    outdegree = Counter(tail for tail, _head in arcs)
    reticulations = tuple(
        sorted(
            vertex
            for vertex in set(indegree) | set(outdegree)
            if (indegree[vertex], outdegree[vertex]) == (2, 1)
        )
    )
    incoming = {
        vertex: tuple(
            index for index, (_tail, head) in enumerate(arcs) if head == vertex
        )
        for vertex in reticulations
    }
    all_labels = frozenset(labels.values())
    result = []
    for choice in itertools.product((0, 1), repeat=len(reticulations)):
        excluded = {
            incoming[vertex][1 - bit]
            for vertex, bit in zip(reticulations, choice)
        }
        children: dict[str, list[str]] = defaultdict(list)
        for index, (tail, head) in enumerate(arcs):
            if index not in excluded:
                children[tail].append(head)
        memo: dict[str, frozenset[int]] = {}

        def descendants(vertex: str) -> frozenset[int]:
            if vertex in memo:
                return memo[vertex]
            value = {labels[vertex]} if vertex in labels else set()
            for child in children[vertex]:
                value.update(descendants(child))
            memo[vertex] = frozenset(value)
            return memo[vertex]

        splits = set()
        for index, (_tail, head) in enumerate(arcs):
            if index in excluded:
                continue
            side = descendants(head)
            if side and side != all_labels:
                splits.add(side)
                splits.add(all_labels - side)
        result.append(splits)
    return tuple(result)


def displayed_by_all(switchings, colours: Sequence[int]) -> bool:
    side = frozenset(index + 1 for index, colour in enumerate(colours) if not colour)
    other = frozenset(range(1, len(colours) + 1)) - side
    if min(len(side), len(other)) < 2:
        raise ValueError("the split is not balanced")
    return all(side in splits or other in splits for splits in switchings)


def duplicate_global_singletons(
    words: Sequence[Sequence[int]], extras: Sequence[int]
):
    occurrences = {0: [], 1: []}
    for segment, word in enumerate(words):
        for position, colour in enumerate(word):
            occurrences[colour].append((segment, position))
    for colour in extras:
        occurrences[colour].append(None)
    if any(not occurrences[colour] for colour in (0, 1)):
        return None
    result = [list(word) for word in words]
    changed = False
    for colour in (0, 1):
        if len(occurrences[colour]) != 1:
            continue
        location = occurrences[colour][0]
        if location is None:
            return None
        segment, position = location
        result[segment].insert(position, colour)
        changed = True
    return tuple(tuple(word) for word in result) if changed else None


def census_family(
    identifier: str,
    segment_count: int,
    extra_count: int,
    builder,
):
    metrics = Counter()
    common_rows = []
    class_cache = {}
    switching_cache = {}

    def prepare(words):
        counts = tuple(len(word) for word in words)
        if counts not in class_cache:
            neutral = tuple(tuple(0 for _ in word) for word in words)
            root, arcs, labels, _ordinary, _sink_leaves, _incoming = builder(neutral)
            class_cache[counts] = literal_valid(root, arcs, labels)
            if class_cache[counts]:
                switching_cache[counts] = switching_splits(arcs, labels)
        return class_cache[counts]

    for counts in itertools.product(range(3), repeat=segment_count):
        words_options = tuple(SHORT_WORDS[count] for count in counts)
        neutral = tuple(tuple(0 for _ in range(count)) for count in counts)
        if not prepare(neutral):
            metrics["literal_invalid_compressed_occupancies"] += 1
            continue
        metrics["literal_valid_compressed_occupancies"] += 1
        switchings = switching_cache[counts]
        for words in itertools.product(*words_options):
            ordinary = tuple(colour for word in words for colour in word)
            for extras in itertools.product((0, 1), repeat=extra_count):
                colours = ordinary + extras
                metrics["compressed_colourings"] += 1
                colour_counts = Counter(colours)
                if set(colours) != {0, 1} or min(colour_counts.values()) < 2:
                    continue
                metrics["balanced_compressed_colourings"] += 1
                if displayed_by_all(switchings, colours):
                    common_rows.append(
                        {"kind": "compressed", "words": words, "extras": extras}
                    )

    for base_words in itertools.product(BASE_WORDS, repeat=segment_count):
        for extras in itertools.product((0, 1), repeat=extra_count):
            words = duplicate_global_singletons(base_words, extras)
            if words is None or not prepare(words):
                continue
            counts = tuple(len(word) for word in words)
            colours = tuple(colour for word in words for colour in word) + extras
            metrics["singleton_doubled_colourings"] += 1
            if displayed_by_all(switching_cache[counts], colours):
                common_rows.append(
                    {"kind": "singleton_doubled", "words": words, "extras": extras}
                )
    return {
        "identifier": identifier,
        **dict(sorted(metrics.items())),
        "splits_displayed_by_every_switching": len(common_rows),
        "failure_rows": common_rows,
    }


def audit(project: Path) -> dict[str, object]:
    core_path = (
        project / "AUDIT/INDEPENDENT_IMPLEMENTATION/level2_orientation_core_audit.json"
    )
    cores = load_cores(json.loads(core_path.read_text()))
    rows = []
    for nonroot in (False, True):
        for core in cores:
            if core.reticulation_count == 1:
                rows.append(
                    census_family(
                        f"{core.name}:{'nonroot' if nonroot else 'root'}",
                        2,
                        1 + int(nonroot),
                        lambda words, nonroot=nonroot: build_cycle(words, nonroot),
                    )
                )
            else:
                rows.append(
                    census_family(
                        f"{core.name}:{'nonroot' if nonroot else 'root'}",
                        len(core.arcs),
                        len(core.sinks) + int(nonroot),
                        lambda words, core=core, nonroot=nonroot: build_theta(
                            core, words, nonroot
                        ),
                    )
                )
    failures = sum(int(row["splits_displayed_by_every_switching"]) for row in rows)
    return {
        "input": {str(core_path): file_hash(core_path)},
        "literal_standard_convention_enforced": True,
        "families": rows,
        "total_splits_displayed_by_every_switching": failures,
        "run_compression_lift": {
            "status": "PROVED",
            "statement": (
                "From an arbitrary two-colour port word, keep at most one "
                "occurrence of each colour on each segment in their directed "
                "order.  If a colour then occurs globally only once but the "
                "original balanced split had it at least twice, retain a second "
                "occurrence on that same segment.  This produces one of the "
                "enumerated compressed or singleton-doubled restrictions.  Any "
                "split displayed by every full switching would remain displayed "
                "by every switching after restriction, so a zero finite survivor "
                "count excludes arbitrary words."
            ),
            "external_component_case": (
                "Choose a minimal bridge-tree component containing both colours. "
                "At its central ordinary vertex or blob, mixed child components "
                "are recursively excluded; hence the retained incident ports are "
                "monochromatic.  If one colour occurs at only one incident port, "
                "the candidate split lies wholly beyond that bridge and the "
                "minimal component was not central.  Thus the blob census applies "
                "with both colours represented at least twice; ordinary-tree "
                "centres give the usual crossing quartet directly."
            ),
        },
        "conclusion": (
            "PROVED" if not failures else "FALSE"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = audit(arguments.project.resolve())
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "conclusion": result["conclusion"],
                "families": len(result["families"]),
                "total_splits_displayed_by_every_switching": result[
                    "total_splits_displayed_by_every_switching"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
