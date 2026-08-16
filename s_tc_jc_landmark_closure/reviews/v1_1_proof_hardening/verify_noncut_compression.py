#!/usr/bin/env python3
"""Independent bounded falsifier for the noncut word-compression lemma.

This file deliberately imports no project graph, core, or canonicalization
code.  The five primitive templates are transcribed as abstract segment
endpoints, minimum repairs, and mandatory path-sink children.  Every strong
two-coloured occupancy word of total size at most eight is checked.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path


@dataclass(frozen=True)
class Core:
    name: str
    segments: tuple[tuple[str, str], ...]
    repairs: tuple[tuple[int, ...], ...]
    sinks: tuple[str, ...]


CORES = (
    Core("cycle", (("S", "X"), ("S", "X")), ((0,), (1,)), ("X",)),
    Core(
        "theta0",
        (("S", "U"), ("S", "V"), ("U", "X"), ("V", "X"), ("U", "V")),
        ((2, 3), (3, 4)),
        ("X",),
    ),
    Core(
        "theta1",
        (("S", "U"), ("S", "X"), ("V", "X"), ("U", "V"), ("U", "V")),
        ((2, 3), (2, 4)),
        ("X",),
    ),
    Core(
        "theta2",
        (
            ("S", "U"), ("S", "V"), ("U", "X0"),
            ("V", "X0"), ("U", "X1"), ("V", "X1"),
        ),
        ((2, 3), (2, 5), (3, 4), (4, 5)),
        ("X0", "X1"),
    ),
    Core(
        "theta3",
        (
            ("S", "U"), ("S", "X0"), ("V", "X0"),
            ("U", "X1"), ("V", "X1"), ("U", "V"),
        ),
        ((2,), (4,)),
        ("X0", "X1"),
    ),
)


def weak_compositions(total: int, bins: int):
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for suffix in weak_compositions(total - first, bins - 1):
            yield (first,) + suffix


def labels(words, sink_colours):
    ordinary = [
        (("segment", segment, position), colour)
        for segment, word in enumerate(words)
        for position, colour in enumerate(word)
    ]
    sinks = [(("sink", index, 0), colour) for index, colour in enumerate(sink_colours)]
    return ordinary + sinks


def select_compression(core: Core, words, sink_colours):
    occupied = {index for index, word in enumerate(words) if word}
    repairs = [repair for repair in core.repairs if set(repair) <= occupied]
    if not repairs:
        raise ValueError("not a strong occupancy")
    repair = min(repairs)
    selected = {("segment", segment, 0) for segment in repair}
    selected.update(("sink", index, 0) for index in range(len(core.sinks)))
    colour_of = dict(labels(words, sink_colours))

    for colour in (0, 1):
        while sum(colour_of[item] == colour for item in selected) < 2:
            adjacent = []
            for item in sorted(selected):
                if colour_of[item] != colour or item[0] != "segment":
                    continue
                _, segment, position = item
                for candidate_position in (position - 1, position + 1):
                    candidate = ("segment", segment, candidate_position)
                    if (
                        0 <= candidate_position < len(words[segment])
                        and candidate not in selected
                        and colour_of[candidate] == colour
                    ):
                        adjacent.append(candidate)
            candidates = adjacent or [
                item for item, value in sorted(colour_of.items())
                if value == colour and item not in selected
            ]
            if not candidates:
                raise AssertionError("a colour occurring twice lost its second actual label")
            selected.add(candidates[0])
    return repair, tuple(sorted(selected)), colour_of


def graph_for_selection(core: Core, selected):
    selected_set = set(selected)
    edges = []
    leaf_vertex = {}
    for segment, (left, right) in enumerate(core.segments):
        ports = sorted(
            item for item in selected_set if item[0] == "segment" and item[1] == segment
        )
        chain = [left]
        for item in ports:
            attachment = f"p:{segment}:{item[2]}"
            leaf = f"leaf:{item!r}"
            chain.append(attachment)
            edges.append((attachment, leaf, False))
            leaf_vertex[item] = leaf
        chain.append(right)
        edges.extend((u, v, True) for u, v in zip(chain, chain[1:]))
    for index, sink in enumerate(core.sinks):
        item = ("sink", index, 0)
        if item in selected_set:
            leaf = f"leaf:{item!r}"
            edges.append((sink, leaf, False))
            leaf_vertex[item] = leaf
    simple_pairs = [tuple(sorted((u, v))) for u, v, _ in edges]
    if len(simple_pairs) != len(set(simple_pairs)):
        raise AssertionError("selected repair failed to resolve a parallel core pair")
    return edges, leaf_vertex


def component_without(edges, removed_index, start):
    adjacency = {}
    for index, (u, v, _is_core) in enumerate(edges):
        if index == removed_index:
            continue
        adjacency.setdefault(u, []).append(v)
        adjacency.setdefault(v, []).append(u)
    seen = {start}
    stack = [start]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency.get(vertex, ()): 
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return seen


def validate(core: Core, repair, selected, colour_of):
    if len(selected) != len(set(selected)):
        raise AssertionError("a taxon was selected more than once")
    if len(selected) > 8:
        raise AssertionError("eight-port compression bound exceeded")
    for colour in (0, 1):
        if sum(colour_of[item] == colour for item in selected) < 2:
            raise AssertionError("singleton colour in compressed restriction")
    for segment in repair:
        if not any(item[0] == "segment" and item[1] == segment for item in selected):
            raise AssertionError("minimum repair segment was lost")
    for index in range(len(core.sinks)):
        if ("sink", index, 0) not in selected:
            raise AssertionError("path-sink child was lost")

    edges, leaf_vertex = graph_for_selection(core, selected)
    all_vertices = {vertex for edge in edges for vertex in edge[:2]}
    all_leaves = set(leaf_vertex.values())
    colour_leaf_sets = {
        colour: {leaf_vertex[item] for item in selected if colour_of[item] == colour}
        for colour in (0, 1)
    }
    for index, (u, _v, is_core) in enumerate(edges):
        side = component_without(edges, index, u)
        if len(side) == len(all_vertices):
            continue
        side_leaves = side & all_leaves
        if is_core:
            raise AssertionError("a primitive-core edge became a bridge")
        if side_leaves in colour_leaf_sets.values() or (all_leaves - side_leaves) in colour_leaf_sets.values():
            raise AssertionError("compressed restriction made the proposed split a cut")


def enumerate_and_check():
    counts = {}
    examples = {}
    for core in CORES:
        checked = 0
        max_ordinary = 8 - len(core.sinks)
        for ordinary_count in range(max_ordinary + 1):
            for lengths in weak_compositions(ordinary_count, len(core.segments)):
                for flat_colours in product((0, 1), repeat=ordinary_count):
                    words = []
                    cursor = 0
                    for length in lengths:
                        words.append(tuple(flat_colours[cursor:cursor + length]))
                        cursor += length
                    for sink_colours in product((0, 1), repeat=len(core.sinks)):
                        full = labels(words, sink_colours)
                        if any(sum(value == colour for _item, value in full) < 2 for colour in (0, 1)):
                            continue
                        if not any(set(repair) <= {i for i, word in enumerate(words) if word}
                                   for repair in core.repairs):
                            continue
                        repair, selected, colour_of = select_compression(core, words, sink_colours)
                        validate(core, repair, selected, colour_of)
                        checked += 1
                        examples.setdefault(core.name, (repair, selected, colour_of))
        counts[core.name] = checked
    return counts, examples


def mutation_tests(examples):
    rejected = []
    for core in CORES:
        repair, selected, colour_of = examples[core.name]
        tests = []
        tests.append(("duplicate_taxon", selected + (selected[0],)))
        repair_item = next(item for item in selected if item[0] == "segment" and item[1] in repair)
        tests.append(("drop_repair", tuple(item for item in selected if item != repair_item)))
        sink_item = next(item for item in selected if item[0] == "sink")
        tests.append(("drop_sink", tuple(item for item in selected if item != sink_item)))
        colour = colour_of[selected[0]]
        singleton = tuple(item for item in selected if colour_of[item] != colour) + (selected[0],)
        tests.append(("singleton_colour", singleton))
        for name, mutated in tests:
            try:
                validate(core, repair, mutated, colour_of)
            except (AssertionError, KeyError):
                rejected.append(f"{core.name}:{name}")
            else:
                raise AssertionError(f"mutation survived: {core.name}:{name}")
    return rejected


def manuscript_regressions():
    manuscript = Path(__file__).resolve().parents[2] / "source" / "paper" / "main.tex"
    text = manuscript.read_text(encoding="utf-8")
    forbidden = (
        "take one representative from every monochromatic run",
        "duplicate a representative",
        "duplicate a taxon",
        "A split displayed by every full switching would remain displayed after this restriction",
    )
    hits = [phrase for phrase in forbidden if phrase in text]
    if hits:
        raise AssertionError(f"withdrawn compression language returned: {hits}")
    required = ("Noncut-preserving word compression", "No taxon is duplicated")
    missing = [phrase for phrase in required if phrase not in text]
    if missing:
        raise AssertionError(f"compression proof language missing: {missing}")


def main():
    counts, examples = enumerate_and_check()
    rejected = mutation_tests(examples)
    manuscript_regressions()
    print("VERIFIED: independent noncut-preserving compression audit")
    print("bounded strong two-colour occupancies:", counts)
    print("mutations rejected:", len(rejected))


if __name__ == "__main__":
    main()
