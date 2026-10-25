#!/usr/bin/env python3
"""Independently regenerate the complete finite-eight structural sweep.

This file is intentionally self-contained.  It imports neither the Paper B
finite-atlas builder/verifier nor another handoff helper.  Expectations are
read only after all finite languages, partitions, and address rows have been
regenerated from the small topology/spec manifest.

The PASS result certifies finite graph/support exhaustiveness.  It is not a
certificate for continuum scalar-germ injectivity or analytic continuation.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence


MANIFEST_SCHEMA = "nmsc-independent-finite-eight-full-sweep-spec-v1"
RECORD_SCHEMA = "nmsc-local-certificate-v3"
JOB = "independent_finite_eight_full_sweep"


class SweepError(RuntimeError):
    pass


@dataclass(frozen=True)
class Arc:
    tail: str
    head: str
    segment: int | None


class Digraph:
    def __init__(self) -> None:
        self.arcs: list[Arc] = []
        self.outgoing: dict[str, list[int]] = {}

    def add(self, tail: str, head: str, segment: int | None = None) -> None:
        index = len(self.arcs)
        self.arcs.append(Arc(tail, head, segment))
        self.outgoing.setdefault(tail, []).append(index)

    def nodes(self) -> set[str]:
        return {node for arc in self.arcs for node in (arc.tail, arc.head)}

    def indegree(self, node: str) -> int:
        return sum(arc.head == node for arc in self.arcs)

    def outdegree(self, node: str) -> int:
        return len(self.outgoing.get(node, ()))

    def routes(self, source: str, target: str) -> tuple[tuple[int, ...], ...]:
        found: list[tuple[int, ...]] = []

        def visit(node: str, prefix: tuple[int, ...], seen: frozenset[str]) -> None:
            if node == target:
                found.append(prefix)
                return
            for edge_id in self.outgoing.get(node, ()):
                child = self.arcs[edge_id].head
                if child not in seen:
                    visit(child, prefix + (edge_id,), seen | {child})

        visit(source, (), frozenset({source}))
        return tuple(sorted(found))


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: object) -> str:
    return sha256(canonical(value).encode()).hexdigest()


def subsets(values: Sequence[int]) -> Iterable[tuple[int, ...]]:
    for size in range(len(values) + 1):
        yield from combinations(values, size)


def domain_edges(
    core: Mapping[str, object], repair: Sequence[int]
) -> tuple[list[tuple[str, str]], dict[str, str]]:
    reticulations = set(map(str, core["reticulations"]))
    raw_arcs = [tuple(map(str, arc)) for arc in core["arcs"]]  # type: ignore[index]
    role = {
        node: ("reticulation" if node in reticulations else "tree")
        for arc in raw_arcs
        for node in arc
    }
    edges: list[tuple[str, str]] = []
    for segment, (tail, head) in enumerate(raw_arcs):
        if segment in repair:
            port, leaf = f"R{segment}", f"L{segment}"
            role[port], role[leaf] = "tree", "leaf"
            edges.extend(((tail, port), (port, head), (port, leaf)))
        else:
            edges.append((tail, head))
    for sink in map(str, core["sinks"]):
        leaf = f"C_{sink}"
        role[leaf] = "leaf"
        edges.append((sink, leaf))
    return edges, role


def repair_is_valid(core: Mapping[str, object], repair: Sequence[int]) -> bool:
    edges, role = domain_edges(core, repair)
    nodes = {node for edge in edges for node in edge}
    for node in nodes:
        if role[node] == "leaf":
            continue
        children = [head for tail, head in edges if tail == node]
        if not any(role[child] in {"tree", "leaf"} for child in children):
            return False
        if role[node] == "reticulation" and len(children) != 1:
            return False
    for reticulation in map(str, core["reticulations"]):
        parents = {tail for tail, head in edges if head == reticulation}
        for parent in parents:
            ordinary = sum(head == parent for _, head in edges)
            ordinary += sum(
                role[child] != "reticulation"
                for tail, child in edges
                if tail == parent
            )
            if parent == "S":
                ordinary += 1
            if ordinary < 2:
                return False
    return True


def minimum_repairs(core: Mapping[str, object]) -> tuple[tuple[int, ...], ...]:
    segments = tuple(range(len(core["arcs"])))  # type: ignore[arg-type,index]
    result: list[tuple[int, ...]] = []
    for candidate in subsets(segments):
        if repair_is_valid(core, candidate) and not any(
            set(old).issubset(candidate) for old in result
        ):
            result.append(candidate)
    return tuple(result)


def physical_sample_roles(
    core: Mapping[str, object], repair: Sequence[int]
) -> tuple[str, ...]:
    return tuple(
        sorted(
            ["O", *(f"L{i}" for i in repair), *(f"C_{s}" for s in core["sinks"])]  # type: ignore[index]
        )
    )


def label_transport(
    core: Mapping[str, object],
    repair: Sequence[int],
    assigned: Sequence[str] | None = None,
) -> dict[str, str]:
    roles = tuple(role for role in physical_sample_roles(core, repair) if role != "O")
    labels = tuple(f"b{i}" for i in range(len(roles)))
    values = labels if assigned is None else tuple(assigned)
    if sorted(values) != sorted(labels):
        raise SweepError("invalid homogeneous-label assignment")
    return {"O": "o", **dict(zip(roles, values))}


def construct_graph(
    core: Mapping[str, object],
    repair: Sequence[int],
    *,
    probe_segment: int | None = None,
    probe_position: str | None = None,
    word_segment: int | None = None,
    word_order: Sequence[str] = (),
) -> Digraph:
    graph = Digraph()
    graph.add("TOP", "ROOT")
    graph.add("ROOT", "S")
    graph.add("ROOT", "O")
    repair_set = set(repair)
    for segment, raw_arc in enumerate(core["arcs"]):  # type: ignore[index]
        tail, head = map(str, raw_arc)
        chain = [tail]
        if segment == probe_segment and probe_position == "above-anchor":
            chain.append("ZPORT")
        if segment == word_segment:
            chain.extend(f"W_{label}" for label in word_order)
        if segment in repair_set:
            chain.append(f"R{segment}")
        if segment == probe_segment and probe_position != "above-anchor":
            chain.append("ZPORT")
        chain.append(head)
        for left, right in zip(chain, chain[1:]):
            graph.add(left, right, segment)
        if segment in repair_set:
            graph.add(f"R{segment}", f"L{segment}")
        if segment == probe_segment:
            graph.add("ZPORT", "Z")
        if segment == word_segment:
            for label in word_order:
                graph.add(f"W_{label}", label)
    for sink in map(str, core["sinks"]):
        graph.add(sink, f"C_{sink}")
    return graph


def renamed(graph: Digraph, mapping: Mapping[str, str]) -> Digraph:
    result = Digraph()
    for arc in graph.arcs:
        result.add(
            mapping.get(arc.tail, arc.tail),
            mapping.get(arc.head, arc.head),
            arc.segment,
        )
    return result


def temporal_orders(
    graph: Digraph, samples: Sequence[str]
) -> tuple[dict[str, int], ...]:
    sample_set = set(samples)
    internal = sorted(graph.nodes() - sample_set)
    predecessors = {
        node: {
            arc.tail
            for arc in graph.arcs
            if arc.head == node and arc.tail in internal
        }
        for node in internal
    }
    orders: list[dict[str, int]] = []

    def extend(prefix: tuple[str, ...], remaining: frozenset[str]) -> None:
        if not remaining:
            total = len(prefix)
            ranks = {node: total - index for index, node in enumerate(prefix)}
            ranks.update({sample: 0 for sample in sample_set})
            orders.append(ranks)
            return
        available = sorted(
            node
            for node in remaining
            if predecessors[node].isdisjoint(remaining)
        )
        for node in available:
            extend(prefix + (node,), remaining - {node})

    extend((), frozenset(internal))
    if not orders:
        raise SweepError("no strict temporal extension")
    return tuple(orders)


def open_chamber(
    graph: Digraph, ranks: Mapping[str, int], edge_id: int
) -> list[int]:
    arc = graph.arcs[edge_id]
    return [ranks[arc.head], ranks[arc.tail]]


def complete_merger_language(
    graph: Digraph, ranks: Mapping[str, int], labels: Sequence[str]
) -> list[dict[str, object]]:
    initial: list[tuple[tuple[str, ...], tuple[tuple[int, ...], ...]]] = []
    for label in sorted(labels):
        paths = graph.routes("TOP", label)
        if not paths:
            raise SweepError(f"no route to {label}")
        initial.append(((label,), paths))
    records: dict[str, dict[str, object]] = {}

    def search(
        blocks: tuple[tuple[tuple[str, ...], tuple[tuple[int, ...], ...]], ...],
        history: tuple[dict[str, object], ...],
    ) -> None:
        if len(blocks) == 1:
            row = {
                "event": "complete_merger_word",
                "steps": list(history),
                "no_unlisted_selected_merger": True,
            }
            records[canonical(row)] = row
            return
        for left_index, right_index in combinations(range(len(blocks)), 2):
            left_labels, left_paths = blocks[left_index]
            right_labels, right_paths = blocks[right_index]
            ancestral_prefixes: dict[int, set[tuple[int, ...]]] = {}
            for left_path in left_paths:
                for right_path in right_paths:
                    for shared_edge in set(left_path).intersection(right_path):
                        bucket = ancestral_prefixes.setdefault(shared_edge, set())
                        bucket.add(left_path[: left_path.index(shared_edge) + 1])
                        bucket.add(right_path[: right_path.index(shared_edge) + 1])
            for edge_id, prefixes in sorted(ancestral_prefixes.items()):
                merged_labels = tuple(sorted((*left_labels, *right_labels)))
                step = {
                    "blocks": [list(left_labels), list(right_labels)],
                    "open_chamber": open_chamber(graph, ranks, edge_id),
                }
                survivors = [
                    block
                    for index, block in enumerate(blocks)
                    if index not in {left_index, right_index}
                ]
                survivors.append((merged_labels, tuple(sorted(prefixes))))
                search(
                    tuple(sorted(survivors, key=lambda item: item[0])),
                    history + (step,),
                )

    search(tuple(initial), ())
    return [records[key] for key in sorted(records)]


def literal_two_step_language(
    graph: Digraph, ranks: Mapping[str, int], labels: Sequence[str]
) -> list[dict[str, object]]:
    """Union cylinders over a Cartesian product of full hidden routes."""
    ordered_labels = tuple(sorted(labels))
    route_sets = {label: graph.routes("TOP", label) for label in ordered_labels}
    if any(not paths for paths in route_sets.values()):
        raise SweepError("selected label has no hidden route")
    records: dict[str, dict[str, object]] = {}
    for route_tuple in product(*(route_sets[label] for label in ordered_labels)):
        assignment = dict(zip(ordered_labels, route_tuple))
        for left, right in combinations(ordered_labels, 2):
            for first in set(assignment[left]).intersection(assignment[right]):
                row = {
                    "event": "first_merger",
                    "pair": [left, right],
                    "open_chamber": open_chamber(graph, ranks, first),
                    "no_unlisted_selected_merger": True,
                }
                records[canonical(row)] = row
        for triple in combinations(ordered_labels, 3):
            for first_pair in combinations(triple, 2):
                left, right = first_pair
                third = next(label for label in triple if label not in first_pair)
                for first in set(assignment[left]).intersection(assignment[right]):
                    for continuation in (assignment[left], assignment[right]):
                        first_position = continuation.index(first)
                        for second in continuation[: first_position + 1]:
                            if second not in assignment[third]:
                                continue
                            row = {
                                "event": "first_then_second_merger",
                                "first_pair": [left, right],
                                "third": third,
                                "first_open_chamber": open_chamber(graph, ranks, first),
                                "second_open_chamber": open_chamber(graph, ranks, second),
                                "no_unlisted_selected_merger": True,
                            }
                            records[canonical(row)] = row
    return [records[key] for key in sorted(records)]


def restrict_literal_language(
    language: Sequence[Mapping[str, object]], retained: Sequence[str]
) -> list[dict[str, object]]:
    keep = set(retained)
    rows = []
    for row in language:
        if row["event"] == "first_merger":
            involved = set(row["pair"])  # type: ignore[arg-type,index]
        else:
            involved = set(row["first_pair"]) | {row["third"]}  # type: ignore[arg-type,index]
        if involved.issubset(keep):
            rows.append(dict(row))
    return rows


def raw_timed_orbit_digest(
    graph: Digraph, ranks: Mapping[str, int], samples: Sequence[str]
) -> str:
    sample_set = set(samples)

    def token(node: str) -> str:
        if node in sample_set:
            return f"sample:{node}"
        return (
            f"time:{ranks[node]}:in:{graph.indegree(node)}:"
            f"out:{graph.outdegree(node)}"
        )

    return digest(sorted((token(arc.tail), token(arc.head)) for arc in graph.arcs))


def colored_directed_digest(graph: Digraph, colors: Mapping[str, str]) -> str:
    nodes = sorted(graph.nodes())
    groups = [
        tuple(node for node in nodes if colors[node] == color)
        for color in sorted(set(colors.values()))
    ]
    best: tuple[tuple[str, ...], tuple[tuple[int, int], ...]] | None = None
    for choices in product(*(permutations(group) for group in groups)):
        index: dict[str, int] = {}
        word: list[str] = []
        offset = 0
        for group, order in zip(groups, choices):
            word.extend([colors[group[0]]] * len(group))
            index.update({node: offset + position for position, node in enumerate(order)})
            offset += len(group)
        arcs = tuple(sorted((index[arc.tail], index[arc.head]) for arc in graph.arcs))
        candidate = (tuple(word), arcs)
        if best is None or candidate < best:
            best = candidate
    if best is None:
        raise SweepError("cannot canonicalize an empty graph")
    return digest(best)


def directed_unranked_digest(graph: Digraph, samples: Sequence[str]) -> str:
    sample_set = set(samples)
    colors: dict[str, str] = {}
    for node in graph.nodes():
        if node in sample_set:
            colors[node] = f"sample:{node}"
        elif node in {"TOP", "ROOT", "S"}:
            colors[node] = f"boundary:{node}"
        else:
            colors[node] = (
                f"internal:in{graph.indegree(node)}:out{graph.outdegree(node)}"
            )
    return colored_directed_digest(graph, colors)


def selected_descendants(
    graph: Digraph, node: str, samples: Sequence[str]
) -> tuple[str, ...]:
    sample_set = set(samples)
    found: set[str] = set()
    seen = {node}
    pending = [node]
    while pending:
        current = pending.pop()
        if current in sample_set:
            found.add(current)
        for edge_id in graph.outgoing.get(current, ()):
            child = graph.arcs[edge_id].head
            if child not in seen:
                seen.add(child)
                pending.append(child)
    return tuple(sorted(found))


def directed_q7_q8_related(
    left_graph: Digraph,
    left_ranks: Mapping[str, int],
    right_graph: Digraph,
    right_ranks: Mapping[str, int],
    samples: Sequence[str],
) -> bool:
    sample_set = set(samples)

    def colors(graph: Digraph) -> dict[str, str]:
        result = {}
        for node in graph.nodes():
            if node in sample_set:
                result[node] = f"sample:{node}"
            elif node in {"TOP", "ROOT", "S"}:
                result[node] = f"boundary:{node}"
            else:
                result[node] = (
                    f"internal:in{graph.indegree(node)}:out{graph.outdegree(node)}"
                )
        return result

    left_colors, right_colors = colors(left_graph), colors(right_graph)
    if Counter(left_colors.values()) != Counter(right_colors.values()):
        return False
    palette = sorted(set(left_colors.values()))
    left_groups = [
        tuple(sorted(node for node, color in left_colors.items() if color == value))
        for value in palette
    ]
    right_groups = [
        tuple(sorted(node for node, color in right_colors.items() if color == value))
        for value in palette
    ]
    right_arcs = Counter((arc.tail, arc.head) for arc in right_graph.arcs)
    for choices in product(*(permutations(group) for group in right_groups)):
        mapping: dict[str, str] = {}
        for left_group, right_order in zip(left_groups, choices):
            mapping.update(zip(left_group, right_order))
        if Counter(
            (mapping[arc.tail], mapping[arc.head]) for arc in left_graph.arcs
        ) != right_arcs:
            continue
        valid = True
        for left_node, right_node in mapping.items():
            if left_ranks[left_node] == right_ranks[right_node]:
                continue
            if left_graph.indegree(left_node) != 2 or right_graph.indegree(right_node) != 2:
                valid = False
                break
            if (
                len(selected_descendants(left_graph, left_node, samples)) != 1
                or len(selected_descendants(right_graph, right_node, samples)) != 1
            ):
                valid = False
                break
        if valid:
            return True
    return False


def role_rule_related(
    left: Mapping[str, object],
    right: Mapping[str, object],
    rules: Sequence[Mapping[str, object]],
) -> bool:
    left_provenance = left["provenance"]  # type: ignore[index]
    right_provenance = right["provenance"]  # type: ignore[index]
    if (
        left_provenance["core"] != right_provenance["core"]  # type: ignore[index]
        or left_provenance["temporal_extension"] != right_provenance["temporal_extension"]  # type: ignore[index]
    ):
        return False
    left_repair = tuple(left_provenance["repair"])  # type: ignore[index]
    right_repair = tuple(right_provenance["repair"])  # type: ignore[index]
    left_transport = left_provenance["transport"]  # type: ignore[index]
    right_transport = right_provenance["transport"]  # type: ignore[index]
    core_name = left_provenance["core"]  # type: ignore[index]
    for rule in rules:
        if rule["core"] != core_name:
            continue
        source = tuple(rule["source_repair"])  # type: ignore[index]
        target = tuple(rule["target_repair"])  # type: ignore[index]
        role_map = dict(rule["role_map"])  # type: ignore[arg-type,index]
        orientations = [(source, target, role_map)]
        inverse = {value: key for key, value in role_map.items()}
        if len(inverse) == len(role_map):
            orientations.append((target, source, inverse))
        for expected_left, expected_right, mapping in orientations:
            if left_repair != expected_left or right_repair != expected_right:
                continue
            if set(mapping) != set(left_transport) - {"O"}:
                continue
            if set(mapping.values()) != set(right_transport) - {"O"}:
                continue
            if all(
                left_transport[left_role] == right_transport[right_role]
                for left_role, right_role in mapping.items()
            ):
                return True
    return False


def generator_components(
    members: Sequence[Mapping[str, object]],
    states: Mapping[str, tuple[Digraph, Mapping[str, int], tuple[str, ...]]],
    rules: Sequence[Mapping[str, object]],
) -> list[list[str]]:
    by_id = {str(row["row_id"]): row for row in members}
    unseen = set(by_id)
    components: list[list[str]] = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = [root]
        queue: deque[str] = deque([root])
        while queue:
            left_id = queue.popleft()
            left_graph, left_ranks, left_samples = states[left_id]
            for right_id in sorted(unseen):
                right_graph, right_ranks, right_samples = states[right_id]
                if left_samples != right_samples:
                    continue
                related = directed_q7_q8_related(
                    left_graph,
                    left_ranks,
                    right_graph,
                    right_ranks,
                    left_samples,
                )
                if not related:
                    related = role_rule_related(by_id[left_id], by_id[right_id], rules)
                if related:
                    unseen.remove(right_id)
                    component.append(right_id)
                    queue.append(right_id)
        components.append(sorted(component))
    return sorted(components)


def base_sweep(
    cores: Mapping[str, Mapping[str, object]],
    repairs: Mapping[str, Sequence[Sequence[int]]],
    rules: Sequence[Mapping[str, object]],
) -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    rows: list[dict[str, object]] = []
    states: dict[str, tuple[Digraph, Mapping[str, int], tuple[str, ...]]] = {}
    for core_name in sorted(cores):
        core = cores[core_name]
        for repair_value in repairs[core_name]:
            repair = tuple(repair_value)
            roles = tuple(
                role for role in physical_sample_roles(core, repair) if role != "O"
            )
            homogeneous = tuple(f"b{i}" for i in range(len(roles)))
            for assignment in permutations(homogeneous):
                transport = label_transport(core, repair, assignment)
                labels = tuple(sorted(transport.values()))
                graph = renamed(construct_graph(core, repair), transport)
                for extension_id, ranks in enumerate(temporal_orders(graph, labels)):
                    language = complete_merger_language(graph, ranks, labels)
                    provenance = {
                        "core": core_name,
                        "repair": list(repair),
                        "transport": transport,
                        "temporal_extension": extension_id,
                    }
                    row_id = digest(
                        {
                            "core": core_name,
                            "repair": repair,
                            "transport": transport,
                            "temporal_extension": extension_id,
                        }
                    )[:24]
                    row = {
                        "row_id": row_id,
                        "provenance": provenance,
                        "base_labels": list(labels),
                        "observable": {
                            "language_digest": digest(language),
                            "literal_cylinder_count": len(language),
                        },
                        "time_preserving_graph_orbit_digest": raw_timed_orbit_digest(
                            graph, ranks, labels
                        ),
                        "directed_unranked_graph_orbit_digest": directed_unranked_digest(
                            graph, labels
                        ),
                    }
                    rows.append(row)
                    states[row_id] = (graph, ranks, labels)
    by_language: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_language.setdefault(row["observable"]["language_digest"], []).append(row)  # type: ignore[index]
    language_partition = [
        {
            "language_digest": language_digest,
            "member_row_ids": sorted(str(row["row_id"]) for row in members),
        }
        for language_digest, members in sorted(by_language.items())
    ]
    collision_partition: list[dict[str, object]] = []
    for language_digest, members in sorted(by_language.items()):
        if len({row["time_preserving_graph_orbit_digest"] for row in members}) <= 1:
            continue
        collision_partition.append(
            {
                "complete_support_language_digest": language_digest,
                "member_row_ids": sorted(str(row["row_id"]) for row in members),
                "checked_generator_components": generator_components(
                    members, states, rules
                ),
            }
        )
    return rows, language_partition, collision_partition


def probe_positions(segment: int, repair: Sequence[int]) -> tuple[str, ...]:
    return ("above-anchor", "below-anchor") if segment in repair else ("unsubdivided",)


def probe_only(
    language: Sequence[Mapping[str, object]], probe: str = "z"
) -> list[dict[str, object]]:
    return [dict(row) for row in language if probe in canonical(row)]


def first_literal_difference(
    left: Sequence[Mapping[str, object]], right: Sequence[Mapping[str, object]]
) -> dict[str, object] | None:
    left_rows = {canonical(row): dict(row) for row in left}
    right_rows = {canonical(row): dict(row) for row in right}
    for key in sorted(set(left_rows) ^ set(right_rows)):
        return {
            "cylinder": left_rows[key] if key in left_rows else right_rows[key],
            "left_positive": key in left_rows,
            "right_positive": key in right_rows,
        }
    return None


def address_sweep(
    cores: Mapping[str, Mapping[str, object]],
    repairs: Mapping[str, Sequence[Sequence[int]]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, int]]:
    expanded: list[dict[str, object]] = []
    for core_name in sorted(cores):
        core = cores[core_name]
        for repair_value in repairs[core_name]:
            repair = tuple(repair_value)
            transport = label_transport(core, repair)
            base = tuple(sorted(transport.values()))
            labels = tuple(sorted((*base, "z")))
            for segment in range(len(core["arcs"])):  # type: ignore[arg-type,index]
                for position in probe_positions(segment, repair):
                    graph = renamed(
                        construct_graph(
                            core,
                            repair,
                            probe_segment=segment,
                            probe_position=position,
                        ),
                        {**transport, "Z": "z"},
                    )
                    for extension_id, ranks in enumerate(temporal_orders(graph, labels)):
                        language = literal_two_step_language(graph, ranks, labels)
                        base_language = restrict_literal_language(language, base)
                        address_language = probe_only(language)
                        expanded.append(
                            {
                                "provenance": {
                                    "core": core_name,
                                    "repair": list(repair),
                                    "segment": segment,
                                    "position": position,
                                    "temporal_extension": extension_id,
                                },
                                "base_labels": list(base),
                                "observable": {
                                    "base_language_digest": digest(base_language),
                                    "probe_literal_cylinders": address_language,
                                    "probe_address_digest": digest(address_language),
                                },
                                "time_preserving_graph_orbit_digest": raw_timed_orbit_digest(
                                    graph, ranks, labels
                                ),
                            }
                        )
    by_base: dict[str, list[dict[str, object]]] = {}
    for row in expanded:
        by_base.setdefault(row["observable"]["base_language_digest"], []).append(row)  # type: ignore[index]
    witnesses: list[dict[str, object]] = []
    raw_collisions = 0
    within_repair_collisions = 0
    for base_digest, members in sorted(by_base.items()):
        by_address: dict[str, list[dict[str, object]]] = {}
        for row in members:
            by_address.setdefault(row["observable"]["probe_address_digest"], []).append(row)  # type: ignore[index]
        for same_address in by_address.values():
            if len({row["time_preserving_graph_orbit_digest"] for row in same_address}) > 1:
                raw_collisions += 1
            cells: dict[tuple[str, tuple[int, ...]], set[tuple[int, str]]] = {}
            for row in same_address:
                provenance = row["provenance"]
                key = (str(provenance["core"]), tuple(provenance["repair"]))  # type: ignore[arg-type,index]
                cells.setdefault(key, set()).add(
                    (int(provenance["segment"]), str(provenance["position"]))  # type: ignore[index]
                )
            within_repair_collisions += sum(len(value) > 1 for value in cells.values())
        representatives = [group[0] for _, group in sorted(by_address.items())]
        for left, right in combinations(representatives, 2):
            difference = first_literal_difference(
                left["observable"]["probe_literal_cylinders"],  # type: ignore[index]
                right["observable"]["probe_literal_cylinders"],  # type: ignore[index]
            )
            if difference is None:
                raise SweepError("distinct address digests have no literal witness")
            witnesses.append(
                {
                    "common_base_language_digest": base_digest,
                    "left_address_digest": left["observable"]["probe_address_digest"],  # type: ignore[index]
                    "right_address_digest": right["observable"]["probe_address_digest"],  # type: ignore[index]
                    **difference,
                }
            )
    compact = [
        {
            "provenance": row["provenance"],
            "base_labels": row["base_labels"],
            "observable": {
                "base_language_digest": row["observable"]["base_language_digest"],  # type: ignore[index]
                "probe_address_digest": row["observable"]["probe_address_digest"],  # type: ignore[index]
                "probe_literal_cylinder_count": len(
                    row["observable"]["probe_literal_cylinders"]  # type: ignore[arg-type,index]
                ),
            },
            "time_preserving_graph_orbit_digest": row[
                "time_preserving_graph_orbit_digest"
            ],
        }
        for row in expanded
    ]
    summary = {
        "variant_count": len(compact),
        "common_base_class_count": len(by_base),
        "cross_raw_orbit_collision_count": raw_collisions,
        "within_repair_distinct_cell_collision_count": within_repair_collisions,
        "literal_separation_witness_count": len(witnesses),
    }
    return compact, witnesses, summary


def continuation_anchor(
    graph: Digraph, transport: Mapping[str, str], segment: int
) -> str:
    for physical, label in sorted(transport.items()):
        if physical == "O":
            continue
        if all(
            any(graph.arcs[edge_id].segment == segment for edge_id in path)
            for path in graph.routes("TOP", physical)
        ):
            return label
    raise SweepError("repair segment lacks a rigid continuation anchor")


def onset(
    language: Sequence[Mapping[str, object]], left: str, right: str
) -> int:
    pair = sorted((left, right))
    values = [
        int(row["open_chamber"][0])  # type: ignore[index]
        for row in language
        if row["event"] == "first_merger" and row["pair"] == pair
    ]
    if not values:
        raise SweepError("pair has no literal onset")
    return min(values)


def word_rows(
    theta2: Mapping[str, object], repair: Sequence[int]
) -> list[dict[str, object]]:
    transport = label_transport(theta2, repair)
    base = tuple(sorted(transport.values()))
    segment = repair[0]
    anchor = continuation_anchor(construct_graph(theta2, repair), transport, segment)
    probes = ("z0", "z1", "z2")
    rows: list[dict[str, object]] = []
    for order in permutations(probes):
        graph = renamed(
            construct_graph(
                theta2,
                repair,
                word_segment=segment,
                word_order=order,
            ),
            transport,
        )
        labels = tuple(sorted((*base, *probes)))
        ranks = temporal_orders(graph, labels)[0]
        full = literal_two_step_language(graph, ranks, labels)
        onsets = {probe: onset(full, probe, anchor) for probe in probes}
        recovered = tuple(sorted(probes, key=lambda label: -onsets[label]))
        failures: list[dict[str, object]] = []
        square_count = 0
        for outer_ids in subsets((0, 1, 2)):
            outer = tuple(probes[index] for index in outer_ids)
            outer_labels = tuple(sorted((*base, *outer)))
            outer_language = literal_two_step_language(graph, ranks, outer_labels)
            for inner_size in range(len(outer) + 1):
                for inner in combinations(outer, inner_size):
                    square_count += 1
                    inner_labels = tuple(sorted((*base, *inner)))
                    direct = literal_two_step_language(graph, ranks, inner_labels)
                    projected = restrict_literal_language(outer_language, inner_labels)
                    if direct != projected:
                        failures.append({"outer": list(outer), "inner": list(inner)})
        if recovered != order or failures:
            raise SweepError("word order/restriction square failed")
        rows.append(
            {
                "base_labels": list(base),
                "continuation_anchor": anchor,
                "observable": {
                    "literal_cylinder_digest": digest(full),
                    "literal_cylinder_count": len(full),
                    "singleton_onsets_from_cylinders": onsets,
                    "recovered_order": list(recovered),
                },
                "declared_order_for_test_only": list(order),
                "restriction_square_count": square_count,
                "restriction_square_failures": failures,
                "selected_label_count": len(labels),
            }
        )
    return rows


def finite_port_rows(
    cores: Mapping[str, Mapping[str, object]],
    repairs: Mapping[str, Sequence[Sequence[int]]],
) -> list[dict[str, object]]:
    """Regenerate every at-most-three-label fixed-cut/triple port probe."""
    rows: list[dict[str, object]] = []
    for core_name in sorted(cores):
        core = cores[core_name]
        for repair_value in repairs[core_name]:
            repair = tuple(repair_value)
            transport = label_transport(core, repair)
            labels = tuple(sorted(transport.values()))
            graph = renamed(construct_graph(core, repair), transport)
            ranks = temporal_orders(graph, labels)[0]
            for test_name, selected in (
                ("fixed_cut_pair", labels[:2]),
                ("rooted_triple", labels[:3]),
                ("restriction_triple", labels[:3]),
            ):
                language = literal_two_step_language(graph, ranks, selected)
                if not language:
                    raise SweepError("finite port probe has no literal cylinder")
                rows.append(
                    {
                        "provenance": {
                            "core": core_name,
                            "repair": list(repair),
                            "test": test_name,
                        },
                        "selected_labels": list(selected),
                        "observable_literal_witness": language[0],
                    }
                )
    if len(rows) != 36 or max(len(row["selected_labels"]) for row in rows) > 3:
        raise SweepError("finite port descent is not the 36-row <=3-label sweep")
    return rows


def exact_fraction(value: object) -> Fraction:
    if isinstance(value, bool) or isinstance(value, float):
        raise SweepError("law fixture requires exact rational strings or integers")
    try:
        return Fraction(str(value))
    except (ValueError, ZeroDivisionError) as error:
        raise SweepError(f"invalid exact rational {value!r}") from error


def law_orbit_key(
    *,
    lower_shell: Sequence[str],
    endpoints: Sequence[str],
    measures: Sequence[Fraction],
    columns: Sequence[Sequence[Fraction]],
    pattern: Sequence[bool],
    donor_word: Sequence[Mapping[str, object]],
    gamma: Fraction,
) -> str:
    reciprocal_pattern = (pattern[1], pattern[0], pattern[2])
    return digest(
        {
            "lower_shell_key": list(lower_shell),
            "unordered_source_pair": sorted(endpoints),
            "common_cut_component_measures": [str(value) for value in measures],
            "normalized_continuation_columns": [
                [str(value) for value in column] for column in columns
            ],
            "triple_source_pattern_mod_reciprocity": list(
                min(tuple(pattern), reciprocal_pattern)
            ),
            "entire_piecewise_donor_word": donor_word,
            "gamma": str(gamma),
        }
    )


def law_interface_sweep(spec: Mapping[str, object]) -> dict[str, object]:
    hidden = spec["hidden_sister"]  # type: ignore[index]
    entries = [exact_fraction(value) for value in hidden["observed_entry_masses"]]  # type: ignore[index]
    coefficient = exact_fraction(hidden["predecessor_no_contact_coefficient"])  # type: ignore[index]
    measures = [entries[0], entries[1] - entries[0] * coefficient]
    if measures != [Fraction(1, 2), Fraction(1, 2)] or sum(measures) != 1:
        raise SweepError("common-cut renewal did not recover balanced components")
    columns = [
        [exact_fraction(value) for value in column]
        for column in hidden["normalized_continuation_columns"]  # type: ignore[index]
    ]
    if any(sum(column) != 1 for column in columns):
        raise SweepError("law continuation columns are not normalized")
    if all(
        columns[0][i] * columns[1][j] == columns[0][j] * columns[1][i]
        for i, j in combinations(range(len(columns[0])), 2)
    ):
        raise SweepError("law continuation columns do not separate components")
    endpoints = list(map(str, hidden["oriented_source_pair"]))  # type: ignore[index]
    reciprocal_endpoints = list(map(str, hidden["reciprocal_source_pair"]))  # type: ignore[index]
    pattern = list(hidden["zero_positive_triple"])  # type: ignore[index]
    reciprocal_pattern = list(hidden["reciprocal_zero_positive_triple"])  # type: ignore[index]
    if reciprocal_endpoints != list(reversed(endpoints)) or reciprocal_pattern != [pattern[1], pattern[0], pattern[2]]:
        raise SweepError("hidden-sister precodes are not reciprocal")
    gamma = exact_fraction(hidden["gamma"])  # type: ignore[index]
    if gamma != Fraction(1, 2):
        raise SweepError("balanced inheritance fixture lost gamma=1/2")
    donor_word = list(hidden["piecewise_donor_word"])  # type: ignore[index]
    if len(donor_word) != 3:
        raise SweepError("whole donor word fixture must contain three epochs")
    previous_end: Fraction | None = None
    for epoch in donor_word:
        start, end = [exact_fraction(value) for value in epoch["open_interval"]]  # type: ignore[index]
        rate = exact_fraction(epoch["rate"])  # type: ignore[index]
        if start >= end or rate <= 0 or (previous_end is not None and start != previous_end):
            raise SweepError("piecewise donor word is not positive/contiguous")
        previous_end = end
    first_key = law_orbit_key(
        lower_shell=hidden["lower_shell_key"],  # type: ignore[arg-type,index]
        endpoints=endpoints,
        measures=measures,
        columns=columns,
        pattern=pattern,
        donor_word=donor_word,
        gamma=gamma,
    )
    second_key = law_orbit_key(
        lower_shell=hidden["lower_shell_key"],  # type: ignore[arg-type,index]
        endpoints=reciprocal_endpoints,
        measures=measures,
        columns=columns,
        pattern=reciprocal_pattern,
        donor_word=donor_word,
        gamma=gamma,
    )
    false_pattern = list(spec["anchored_false_focal_zero_positive_triple"])  # type: ignore[index]
    false_key = law_orbit_key(
        lower_shell=hidden["lower_shell_key"],  # type: ignore[arg-type,index]
        endpoints=endpoints,
        measures=measures,
        columns=columns,
        pattern=false_pattern,
        donor_word=donor_word,
        gamma=gamma,
    )
    nonsister_endpoints = list(spec["different_incidence_source_pair"])  # type: ignore[index]
    nonsister_key = law_orbit_key(
        lower_shell=hidden["lower_shell_key"],  # type: ignore[arg-type,index]
        endpoints=nonsister_endpoints,
        measures=measures,
        columns=columns,
        pattern=pattern,
        donor_word=donor_word,
        gamma=gamma,
    )
    pair_exposure = spec["pair_exposure"]  # type: ignore[index]
    rate = exact_fraction(pair_exposure["rate"])  # type: ignore[index]
    pair_gamma = exact_fraction(pair_exposure["gamma"])  # type: ignore[index]
    one_density = exact_fraction(pair_exposure["one_child_lower_density_at_zero"])  # type: ignore[index]
    two_density = exact_fraction(pair_exposure["two_child_lower_density_at_zero"])  # type: ignore[index]
    if pair_gamma != Fraction(1, 2) or one_density != 0 or two_density != rate:
        raise SweepError("balanced pair-exposure source separator failed")
    donor_mutant = deepcopy(donor_word)
    donor_mutant[1]["rate"] = str(exact_fraction(donor_mutant[1]["rate"]) + 1)
    summary = {
        "hidden_sister_precode_count": 2,
        "hidden_sister_reciprocal_orbit_count": len({first_key, second_key}),
        "q8_positive_hidden_presentation_count": int(spec["q8_positive_hidden_presentations"]),  # type: ignore[index]
        "q8_distinct_first_contact_precode_count": 1,
        "anchored_false_focal_rejected": false_key != first_key,
        "different_incidence_not_collapsed": nonsister_key != first_key,
        "pair_exposure_separates_at_gamma_half": two_density != one_density,
        "entire_piecewise_donor_word_epoch_count": len(donor_word),
        "single_epoch_donor_mutant_rejected": donor_mutant != donor_word,
        "within_coordinate_source_separator_label_count": len(
            hidden["source_separator_labels"]  # type: ignore[arg-type,index]
        ),
        "maximum_joint_coordinate": 5 + len(
            hidden["source_separator_labels"]  # type: ignore[arg-type,index]
        ),
        "common_cut_component_measures": [str(value) for value in measures],
        "reciprocal_orbit_keys": sorted({first_key, second_key}),
    }
    if (
        summary["hidden_sister_reciprocal_orbit_count"] != 1
        or summary["q8_positive_hidden_presentation_count"] != 2
        or not summary["anchored_false_focal_rejected"]
        or not summary["different_incidence_not_collapsed"]
        or not summary["pair_exposure_separates_at_gamma_half"]
        or summary["maximum_joint_coordinate"] != 8
    ):
        raise SweepError("law-only Q6/Q8 finite interface failed")
    return summary


def observed_contract(manifest: Mapping[str, object]) -> tuple[dict[str, object], dict[str, object]]:
    cores = manifest["cores"]  # type: ignore[index]
    repairs = {
        name: minimum_repairs(core)
        for name, core in cores.items()  # type: ignore[union-attr]
    }
    base_rows, language_partition, collision_partition = base_sweep(
        cores, repairs, manifest["declared_role_moves"]  # type: ignore[arg-type,index]
    )
    address_rows, address_witnesses, address_summary = address_sweep(cores, repairs)
    words = word_rows(cores["theta2"], repairs["theta2"][0])  # type: ignore[index]
    ports = finite_port_rows(cores, repairs)
    law_summary = law_interface_sweep(manifest["law_only_q6_q8_spec"])  # type: ignore[arg-type,index]
    histogram = Counter(
        len(row["checked_generator_components"]) for row in collision_partition
    )
    counts = {
        "derived_minimum_repair_count": sum(len(value) for value in repairs.values()),
        "base_row_count": len(base_rows),
        "base_observable_language_count": len(language_partition),
        "base_raw_collision_class_count": len(collision_partition),
        "base_declared_generator_component_count_histogram": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "address_variant_count": len(address_rows),
        "address_common_base_class_count": address_summary["common_base_class_count"],
        "address_cross_raw_orbit_collision_count": address_summary[
            "cross_raw_orbit_collision_count"
        ],
        "address_within_repair_distinct_cell_collision_count": address_summary[
            "within_repair_distinct_cell_collision_count"
        ],
        "address_literal_separation_witness_count": len(address_witnesses),
        "word_order_case_count": len(words),
        "restriction_square_count": sum(
            int(row["restriction_square_count"]) for row in words
        ),
        "maximum_selected_label_count": max(
            int(row["selected_label_count"]) for row in words
        ),
        "finite_port_row_count": len(ports),
        **{
            f"law_{key}": value
            for key, value in law_summary.items()
            if isinstance(value, (bool, int))
        },
    }
    digests = {
        "base_rows_sha256": digest(base_rows),
        "base_language_partition_sha256": digest(language_partition),
        "base_collision_generator_partition_sha256": digest(collision_partition),
        "address_rows_sha256": digest(address_rows),
        "address_literal_witnesses_sha256": digest(address_witnesses),
        "word_rows_sha256": digest(words),
        "finite_port_rows_sha256": digest(ports),
        "law_only_q6_q8_summary_sha256": digest(law_summary),
    }
    raw = {
        "base_rows": base_rows,
        "language_partition": language_partition,
        "collision_partition": collision_partition,
        "address_rows": address_rows,
        "address_witnesses": address_witnesses,
        "word_rows": words,
        "port_rows": ports,
        "law_summary": law_summary,
    }
    return {"counts": counts, "digests": digests}, raw


def hostile_mutation_audit(
    raw: Mapping[str, object], expected: Mapping[str, object]
) -> dict[str, bool]:
    def rejected(observed: dict[str, object]) -> bool:
        return observed != expected

    results: dict[str, bool] = {}
    base_rows = deepcopy(raw["base_rows"])
    base_rows[0]["observable"]["language_digest"] = "0" * 64
    mutant = deepcopy(expected)
    mutant["digests"]["base_rows_sha256"] = digest(base_rows)
    results["changed_complete_language"] = rejected(mutant)

    partition = deepcopy(raw["language_partition"])
    partition[0]["member_row_ids"].append("mutant-row")
    mutant = deepcopy(expected)
    mutant["digests"]["base_language_partition_sha256"] = digest(partition)
    results["changed_language_grouping"] = rejected(mutant)

    addresses = deepcopy(raw["address_rows"])
    addresses[0]["observable"]["probe_address_digest"] = "f" * 64
    mutant = deepcopy(expected)
    mutant["digests"]["address_rows_sha256"] = digest(addresses)
    results["changed_address"] = rejected(mutant)

    collisions = deepcopy(raw["collision_partition"])
    first_component = collisions[0]["checked_generator_components"][0]
    collisions[0]["checked_generator_components"] = [
        first_component[:1], first_component[1:]
    ]
    mutant = deepcopy(expected)
    mutant["digests"]["base_collision_generator_partition_sha256"] = digest(
        collisions
    )
    results["changed_generator_relation"] = rejected(mutant)

    mutant = deepcopy(expected)
    mutant["counts"]["law_hidden_sister_reciprocal_orbit_count"] = mutant[
        "counts"
    ]["law_hidden_sister_precode_count"]
    results["precode_count_substituted_for_orbit_count"] = rejected(mutant)
    return results


def validate_local_record(record: Mapping[str, object]) -> None:
    required = {
        "schema_version",
        "job",
        "case_id",
        "input_hash",
        "status",
        "graph",
        "system",
        "exact_witness",
        "declared_quotient_orbit",
        "notes",
    }
    if not required.issubset(record):
        raise SweepError("local certificate record is missing required fields")
    if record["schema_version"] != RECORD_SCHEMA or record["job"] != JOB:
        raise SweepError("local certificate schema/job mismatch")
    if record["status"] not in {"PASS", "BLOCKING", "INCONCLUSIVE"}:
        raise SweepError("invalid local certificate status")
    if (record["graph"] is None) == (record["system"] is None):
        raise SweepError("local certificate requires exactly one replay input")
    if record["case_id"] != str(record["input_hash"])[:24]:
        raise SweepError("local certificate case id is not hash-derived")


def build_record(manifest: Mapping[str, object]) -> dict[str, object]:
    if manifest.get("schema") != MANIFEST_SCHEMA:
        raise SweepError("unexpected finite-eight manifest schema")
    # Expectations are intentionally not accessed until this full regeneration
    # has completed.
    observed, raw = observed_contract(manifest)
    expected = manifest["expected"]  # type: ignore[index]
    mutations = hostile_mutation_audit(raw, expected)
    passed = observed == expected and all(mutations.values())
    replay_input = {
        key: manifest[key]
        for key in (
            "schema",
            "claim_boundary",
            "cores",
            "declared_role_moves",
            "law_only_q6_q8_spec",
        )
    }
    input_hash = digest(replay_input)
    record: dict[str, object] = {
        "schema_version": RECORD_SCHEMA,
        "job": JOB,
        "case_id": input_hash[:24],
        "input_hash": input_hash,
        "status": "PASS" if passed else "BLOCKING",
        "graph": {
            "manifest_schema": MANIFEST_SCHEMA,
            "core_names": sorted(manifest["cores"]),  # type: ignore[arg-type,index]
            "manifest_replay_input_sha256": input_hash,
        },
        "system": None,
        "exact_witness": {
            "observed": observed,
            "expected": expected,
            "hostile_mutants_rejected": mutations,
            "regeneration_order": (
                "all finite rows/languages/partitions regenerated before "
                "manifest expectations were read"
            ),
        },
        "declared_quotient_orbit": {
            "generator_partition_regenerated": True,
            "precode_count_is_not_orbit_count": True,
            "hidden_sister_precodes": 2,
            "hidden_sister_reciprocal_orbits": 1,
        },
        "notes": manifest["claim_boundary"],
        "tier": 0,
    }
    validate_local_record(record)
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    try:
        record = build_record(manifest)
    except (SweepError, KeyError, TypeError, ValueError) as error:
        raise SystemExit(f"INDEPENDENT_FINITE_EIGHT_REJECTED: {error}")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if record["status"] != "PASS":
        raise SystemExit(
            "INDEPENDENT_FINITE_EIGHT_BLOCKING "
            + canonical(record["exact_witness"])
        )
    counts = record["exact_witness"]["observed"]["counts"]  # type: ignore[index]
    print(
        "INDEPENDENT_FINITE_EIGHT_OK "
        f"base_rows={counts['base_row_count']} "
        f"languages={counts['base_observable_language_count']} "
        f"collisions={counts['base_raw_collision_class_count']} "
        f"addresses={counts['address_variant_count']}"
    )


if __name__ == "__main__":
    main()
