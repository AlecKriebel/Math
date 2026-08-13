#!/usr/bin/env python3
"""Independent selected-core-retention audit for bounded completions.

This module derives contracted directed cores from this directory's primitive
enumerator.  It does not read the primary core or completion tables.  The
predicate audited here says exactly when a selected restriction *retains the
original primitive core as a strong factor*: every path-sink reticulation port
is selected and the occupied ordinary segments contain a minimum repair.

It does not decide intrinsic S_TC membership after arbitrary induced-network
reductions.  In particular, omitting a cycle sink can delete the reticulation
and reduce the selected restriction to a strong tree.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations, permutations
import json
from typing import Any, Iterable, Iterator, Mapping, Sequence

from graphcanon import ColouredMixedGraph, MixedEdge, canonical_json, canonicalize, digest
from primitive import (
    LocalPresentation,
    _rooted_tree_child,
    _strong_arrow_tail,
    mixed_graph,
    raw_presentations,
    weak_compositions,
)
from rootings import rooting_census


@dataclass(frozen=True)
class ContractedCore:
    core_id: str
    family: str
    event_colors: tuple[str, ...]
    segments: tuple[tuple[int, int], ...]
    entry: int
    sink_events: tuple[int, ...]
    reticulation_events: tuple[int, ...]
    minimum_repairs: tuple[tuple[int, ...], ...]
    provenance: tuple[Any, ...]


def _event_code(
    event_colors: Mapping[str, str], segments: Sequence[tuple[str, str]]
) -> tuple[tuple[Any, ...], dict[str, int]]:
    """Canonical directed-multigraph code and winning event transport."""

    groups: dict[str, list[str]] = defaultdict(list)
    for vertex, color in event_colors.items():
        groups[color].append(vertex)
    colors = tuple(sorted(groups))
    group_orders = [tuple(permutations(sorted(groups[color]))) for color in colors]
    best: tuple[Any, ...] | None = None
    best_map: dict[str, int] | None = None

    def recurse(index: int, order: list[str]) -> None:
        nonlocal best, best_map
        if index < len(colors):
            for block in group_orders[index]:
                recurse(index + 1, order + list(block))
            return
        transport = {vertex: position for position, vertex in enumerate(order)}
        n = len(order)
        adjacency = [[0] * n for _ in range(n)]
        for tail, head in segments:
            adjacency[transport[tail]][transport[head]] += 1
        code = (
            tuple(event_colors[vertex] for vertex in order),
            tuple(adjacency[i][j] for i in range(n) for j in range(n)),
        )
        if best is None or code < best:
            best, best_map = code, transport

    recurse(0, [])
    if best is None or best_map is None:
        raise AssertionError("empty event core")
    return best, best_map


def _contract_presentation(presentation: LocalPresentation) -> dict[str, Any]:
    reticulations = set(presentation.reticulations)
    poles = {"pole_a", "pole_b"} if presentation.core == "theta" else set()
    events = poles | {presentation.entry} | reticulations
    adjacency: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for edge_index, (u, v) in enumerate(presentation.internal_edges):
        adjacency[u].append((edge_index, v))
        adjacency[v].append((edge_index, u))
    arc_set = set(presentation.directed_internal_edges)
    visited: set[int] = set()
    raw_segments: list[tuple[str, str, tuple[str, ...]]] = []
    for start in sorted(events):
        for first_edge, first_vertex in adjacency[start]:
            if first_edge in visited:
                continue
            path = [start]
            edge_path = []
            previous, current, edge_index = start, first_vertex, first_edge
            while True:
                path.append(current)
                edge_path.append(edge_index)
                visited.add(edge_index)
                if current in events:
                    break
                choices = [(index, vertex) for index, vertex in adjacency[current] if vertex != previous]
                if len(choices) != 1:
                    raise AssertionError((presentation.provenance, current, choices))
                edge_index, following = choices[0]
                previous, current = current, following
            directions = []
            for u, v in zip(path, path[1:]):
                if (u, v) in arc_set:
                    directions.append(1)
                elif (v, u) in arc_set:
                    directions.append(-1)
                else:
                    raise AssertionError("unoriented core edge")
            if len(set(directions)) != 1:
                raise AssertionError(("direction change outside retained event", path, directions))
            if directions[0] == 1:
                tail, head = path[0], path[-1]
                ordinary = tuple(path[1:-1])
            else:
                tail, head = path[-1], path[0]
                ordinary = tuple(reversed(path[1:-1]))
            if any(vertex in reticulations or vertex == presentation.entry or vertex in poles for vertex in ordinary):
                raise AssertionError("retained event contracted into segment")
            raw_segments.append((tail, head, ordinary))
    if len(visited) != len(presentation.internal_edges):
        raise AssertionError("not every internal edge was contracted")

    internal_out = Counter(tail for tail, _head in presentation.directed_internal_edges)
    event_colors: dict[str, str] = {}
    for event in events:
        if event == presentation.entry:
            event_colors[event] = "ENTRY"
        elif event in reticulations:
            event_colors[event] = "RETIC_SINK" if internal_out[event] == 0 else "RETIC_BRANCH"
        else:
            event_colors[event] = "TREE_BRANCH"
    code, event_map = _event_code(event_colors, [(tail, head) for tail, head, _ in raw_segments])
    transported_segments = []
    for raw_index, (tail, head, ordinary) in enumerate(raw_segments):
        transported_segments.append((event_map[tail], event_map[head], ordinary, raw_index))
    transported_segments.sort(key=lambda item: (item[0], item[1], item[2]))
    segment_map = {raw_index: index for index, (*_rest, raw_index) in enumerate(transported_segments)}
    occupancy = tuple(
        sorted(segment_map[raw_index] for raw_index, (_tail, _head, ordinary) in enumerate(raw_segments) if ordinary)
    )
    return {
        "code": code,
        "family": presentation.core,
        "event_colors": code[0],
        "segments": tuple((tail, head) for tail, head, _ordinary, _raw in transported_segments),
        "entry": next(index for index, color in enumerate(code[0]) if color == "ENTRY"),
        "sink_events": tuple(index for index, color in enumerate(code[0]) if color == "RETIC_SINK"),
        "reticulation_events": tuple(
            index for index, color in enumerate(code[0]) if color in {"RETIC_SINK", "RETIC_BRANCH"}
        ),
        "ordinary_occupancy": occupancy,
        "provenance": presentation.provenance,
    }


def _presentation_for_occupancy(core: Mapping[str, Any], occupied: Iterable[int]) -> LocalPresentation:
    occupied_set = set(occupied)
    event_names = tuple(f"e{i}" for i in range(len(core["event_colors"])))
    vertices = list(event_names)
    edges: list[tuple[str, str]] = []
    arcs: list[tuple[str, str]] = []
    ordinary_parents: list[str] = []
    for segment_index, (tail_index, head_index) in enumerate(core["segments"]):
        tail, head = event_names[tail_index], event_names[head_index]
        if segment_index in occupied_set:
            middle = f"o{segment_index}"
            vertices.append(middle)
            edges.extend(((tail, middle), (middle, head)))
            arcs.extend(((tail, middle), (middle, head)))
            ordinary_parents.append(middle)
        else:
            edges.append((tail, head))
            arcs.append((tail, head))
    entry = event_names[int(core["entry"])]
    sinks = [event_names[index] for index in core["sink_events"]]
    reticulations = tuple(event_names[index] for index in core["reticulation_events"])
    port_parents = (entry, *ordinary_parents, *sinks)
    return LocalPresentation(
        str(core["family"]),
        len(port_parents),
        tuple(vertices),
        tuple(edges),
        tuple(arcs),
        tuple(port_parents),
        entry,
        tuple(sorted(reticulations)),
        (),
        ("contracted_occupancy", core["core_id"], tuple(sorted(occupied_set))),
    )


def _valid_full_occupancy(core: Mapping[str, Any], occupied: Iterable[int]) -> bool:
    presentation = _presentation_for_occupancy(core, occupied)
    # Reject parallel internal edges before the mixed-graph constructor.
    undirected_pairs = [tuple(sorted(edge)) for edge in presentation.internal_edges]
    if len(set(undirected_pairs)) != len(undirected_pairs):
        return False
    retics = set(presentation.reticulations)
    if not _rooted_tree_child(
        presentation.vertices,
        presentation.directed_internal_edges,
        presentation.port_parents,
        presentation.entry,
        retics,
    ):
        return False
    if not _strong_arrow_tail(
        presentation.vertices,
        presentation.directed_internal_edges,
        presentation.port_parents,
        retics,
    ):
        return False
    graph = mixed_graph(presentation)
    census = rooting_census(graph)
    return bool(census["S_TC"])


def _minimum_repairs(core: Mapping[str, Any]) -> tuple[tuple[int, ...], ...]:
    segment_count = len(core["segments"])
    valid = []
    for size in range(segment_count + 1):
        for subset in combinations(range(segment_count), size):
            if _valid_full_occupancy(core, subset):
                valid.append(subset)
    return tuple(
        subset
        for subset in valid
        if not any(set(other) < set(subset) for other in valid)
    )


def derive_cores(max_probe_ports: int = 7) -> tuple[ContractedCore, ...]:
    representatives: dict[str, dict[str, Any]] = {}
    for port_count in range(3, max_probe_ports + 1):
        for presentation in raw_presentations(port_count):
            contracted = _contract_presentation(presentation)
            core_id = digest(contracted["code"])
            contracted["core_id"] = core_id
            representatives.setdefault(core_id, contracted)
    cores = []
    for core_id in sorted(representatives):
        core = representatives[core_id]
        repairs = _minimum_repairs(core)
        if not repairs:
            raise AssertionError(("core has no strong repair", core_id))
        cores.append(
            ContractedCore(
                core_id=core_id,
                family=core["family"],
                event_colors=tuple(core["event_colors"]),
                segments=tuple(core["segments"]),
                entry=int(core["entry"]),
                sink_events=tuple(core["sink_events"]),
                reticulation_events=tuple(core["reticulation_events"]),
                minimum_repairs=repairs,
                provenance=tuple(core["provenance"]),
            )
        )
    return tuple(cores)


def selected_retains_strong_core(
    core: ContractedCore,
    selected_sink_mask: int,
    selected_ordinary_counts: Sequence[int],
) -> bool:
    if len(selected_ordinary_counts) != len(core.segments):
        raise ValueError("one selected ordinary count is required per segment")
    all_sinks = (1 << len(core.sink_events)) - 1
    occupied = {index for index, count in enumerate(selected_ordinary_counts) if count > 0}
    return selected_sink_mask == all_sinks and any(
        set(repair) <= occupied for repair in core.minimum_repairs
    )


def unreduced_core_retention_test(
    core: ContractedCore,
    selected_sink_mask: int,
    selected_ordinary_counts: Sequence[int],
) -> bool:
    """Graph test that keeps the original contracted core fixed.

    This is intentionally not an induced-network reduction and therefore is
    not an intrinsic S_TC test when selected sinks are omitted.
    """

    all_sinks = (1 << len(core.sink_events)) - 1
    if selected_sink_mask != all_sinks:
        return False
    occupied = {index for index, count in enumerate(selected_ordinary_counts) if count > 0}
    core_record = {
        "core_id": core.core_id,
        "family": core.family,
        "event_colors": core.event_colors,
        "segments": core.segments,
        "entry": core.entry,
        "sink_events": core.sink_events,
        "reticulation_events": core.reticulation_events,
    }
    return _valid_full_occupancy(core_record, occupied)


def sink_omission_reduction_counterexample(
    cores: Sequence[ContractedCore],
) -> dict[str, Any]:
    """Exact witness separating core retention from intrinsic S_TC.

    Start with the directed cycle core whose two entry-to-reticulation paths
    contain respectively one and two ordinary selected ports.  Omit the
    reticulation-sink child.  Ancestor pruning deletes the reticulation; unary
    suppression then gives a rooted binary tree on the three selected leaves.
    """

    cycle_cores = [core for core in cores if core.family == "cycle"]
    if len(cycle_cores) != 1:
        raise AssertionError(("expected one cycle core", len(cycle_cores)))
    core = cycle_cores[0]
    selected_counts = (1, 2)
    if selected_retains_strong_core(core, 0, selected_counts):
        raise AssertionError("sink-omitting cycle unexpectedly retained its core")

    vertices = ("r", "a", "b", "c", "h", "L0", "L1", "L2", "D")
    arcs = (
        ("r", "a"),
        ("a", "h"),
        ("r", "b"),
        ("b", "c"),
        ("c", "h"),
        ("a", "L0"),
        ("b", "L1"),
        ("c", "L2"),
        ("h", "D"),
    )
    selected_leaves = {"L0", "L1", "L2"}

    parents: dict[str, set[str]] = defaultdict(set)
    for tail, head in arcs:
        parents[head].add(tail)
    kept = set(selected_leaves)
    frontier = list(selected_leaves)
    while frontier:
        child = frontier.pop()
        for parent in parents[child]:
            if parent not in kept:
                kept.add(parent)
                frontier.append(parent)
    reduced_arcs = {(tail, head) for tail, head in arcs if tail in kept and head in kept}

    while True:
        indegree = Counter(head for _tail, head in reduced_arcs)
        outdegree = Counter(tail for tail, _head in reduced_arcs)
        suppressible = sorted(
            vertex
            for vertex in kept - selected_leaves - {"r"}
            if indegree[vertex] == 1 and outdegree[vertex] == 1
        )
        if not suppressible:
            break
        vertex = suppressible[0]
        parent = next(tail for tail, head in reduced_arcs if head == vertex)
        child = next(head for tail, head in reduced_arcs if tail == vertex)
        reduced_arcs.remove((parent, vertex))
        reduced_arcs.remove((vertex, child))
        reduced_arcs.add((parent, child))
        kept.remove(vertex)

    indegree = Counter(head for _tail, head in reduced_arcs)
    outdegree = Counter(tail for tail, _head in reduced_arcs)
    roots = [vertex for vertex in kept if indegree[vertex] == 0]
    internal = kept - selected_leaves
    is_binary_tree = (
        roots == ["r"]
        and all(indegree[leaf] == 1 and outdegree[leaf] == 0 for leaf in selected_leaves)
        and outdegree["r"] == 2
        and all(
            vertex == "r" or (indegree[vertex] == 1 and outdegree[vertex] == 2)
            for vertex in internal
        )
        and len(reduced_arcs) == len(kept) - 1
    )
    if not is_binary_tree:
        raise AssertionError(("sink-omission reduction was not a binary tree", reduced_arcs))

    return {
        "core_id": core.core_id,
        "family": "cycle",
        "selected_sink_mask": 0,
        "selected_ordinary_counts": list(selected_counts),
        "selected_retains_strong_core": False,
        "intrinsic_reduced_topology_is_STC": True,
        "full_rooted_vertices": list(vertices),
        "full_rooted_arcs": [list(arc) for arc in arcs],
        "omitted_sink_leaf": "D",
        "selected_leaves": sorted(selected_leaves),
        "reduction": "prune vertices with no selected descendant, then suppress indegree-1/outdegree-1 vertices",
        "reduced_vertices": sorted(kept),
        "reduced_arcs": [list(arc) for arc in sorted(reduced_arcs)],
        "reduced_newick": "(L0,(L1,L2));",
    }


def completion_rows(selected_count: int, cores: Sequence[ContractedCore]) -> Iterator[dict[str, Any]]:
    for core in cores:
        sink_count = len(core.sink_events)
        for sink_mask in range(1 << sink_count):
            selected_sink_count = sink_mask.bit_count()
            ordinary_count = selected_count - selected_sink_count
            if ordinary_count < 0:
                continue
            for counts in weak_compositions(ordinary_count, len(core.segments)):
                retains_core = selected_retains_strong_core(core, sink_mask, counts)
                graph_retains_core = unreduced_core_retention_test(core, sink_mask, counts)
                if retains_core != graph_retains_core:
                    raise AssertionError(
                        ("repair criterion disagrees with fixed-core graph test", core.core_id, sink_mask, counts)
                    )
                selected_occupied = {index for index, count in enumerate(counts) if count > 0}
                # Each repair gives a distinct full-completion presentation.
                # Dummy ports are exactly omitted sinks plus missing segments
                # of that chosen repair.
                # For a cycle and selected_count >= 3 there are at least two
                # selected ordinary ports.  Some segment is therefore already
                # subdivided, so the parallel two-segment core is repaired
                # without an ordinary dummy.  Its two symmetric minimum
                # repairs do not define additional completion relations.
                completion_repairs = (
                    ((None, ()),)
                    if core.family == "cycle" and selected_count >= 3
                    else tuple(enumerate(core.minimum_repairs))
                )
                for repair_index, repair in completion_repairs:
                    dummy_sink_count = sink_count - selected_sink_count
                    dummy_repair_segments = tuple(sorted(set(repair) - selected_occupied))
                    dummy_count = dummy_sink_count + len(dummy_repair_segments)
                    dummy_rule_positive = dummy_count == 0
                    yield {
                        "core_id": core.core_id,
                        "family": core.family,
                        "selected_count": selected_count,
                        "selected_sink_mask": sink_mask,
                        "selected_ordinary_counts": list(counts),
                        "repair_index": repair_index,
                        "repair": list(repair),
                        "dummy_sink_count": dummy_sink_count,
                        "dummy_repair_segments": list(dummy_repair_segments),
                        "dummy_count": dummy_count,
                        "dummy_rule_predicts_retains_strong_core": dummy_rule_positive,
                        "selected_retains_strong_core": retains_core,
                        "unreduced_core_graph_retains_strong_core": graph_retains_core,
                    }


def audit(selected_counts: Iterable[int] = range(3, 7)) -> dict[str, Any]:
    cores = derive_cores()
    per_count = {}
    first_dummy_false_negative = None
    for selected_count in selected_counts:
        rows = list(completion_rows(selected_count, cores))
        bucket = Counter()
        for row in rows:
            retains = bool(row["selected_retains_strong_core"])
            dummy_positive = bool(row["dummy_rule_predicts_retains_strong_core"])
            bucket["retains_strong_core" if retains else "does_not_retain_strong_core"] += 1
            bucket["dummy_rule_positive" if dummy_positive else "dummy_rule_negative"] += 1
            if retains and not dummy_positive:
                bucket["false_negative_under_dummy_rule"] += 1
                if first_dummy_false_negative is None:
                    first_dummy_false_negative = row
            if dummy_positive and not retains:
                bucket["false_positive_under_dummy_rule"] += 1
        per_count[str(selected_count)] = {"presentations": len(rows), **dict(sorted(bucket.items()))}
    return {
        "schema": "selected-core-retention-audit-v2",
        "predicate_name": "selected_retains_strong_core",
        "criterion": (
            "all reticulation sinks selected and occupied ordinary segments contain at least one "
            "minimum repair"
        ),
        "semantic_scope": (
            "retention of the original primitive cycle/theta core as a strong factor; not intrinsic "
            "S_TC membership after arbitrary induced-network reduction"
        ),
        "intrinsic_selected_STC_membership_classified": False,
        "derived_core_count": len(cores),
        "minimum_repair_size_by_core": sorted(
            min(len(repair) for repair in core.minimum_repairs) for core in cores
        ),
        "criterion_matches_unreduced_core_graph_test": True,
        "cores": [
            {
                "core_id": core.core_id,
                "family": core.family,
                "event_colors": list(core.event_colors),
                "segments": [list(segment) for segment in core.segments],
                "entry": core.entry,
                "sink_events": list(core.sink_events),
                "reticulation_events": list(core.reticulation_events),
                "minimum_repairs": [list(repair) for repair in core.minimum_repairs],
                "provenance": json.loads(canonical_json(core.provenance)),
            }
            for core in cores
        ],
        "per_selected_count": per_count,
        "first_dummy_rule_false_negative": first_dummy_false_negative,
        "sink_omission_intrinsic_STC_counterexample": sink_omission_reduction_counterexample(cores),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
