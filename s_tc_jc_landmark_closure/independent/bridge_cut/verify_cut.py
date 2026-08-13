#!/usr/bin/env python3
"""Primitive graph-to-polynomial verification of the JC cut theorem.

The implementation is standalone.  It defines the five primitive directed
cycle/theta cores explicitly, constructs every bounded rooted or incoming-port
completion, performs the narrow root suppression, checks the standard-strong
local criterion, enumerates displayed trees, derives descendant masks, builds
the exact JC Fourier tensor, and searches for strict open-cube flattening
minors.  No historical catalogue, tensor engine, separator table, or
polynomial certificate is imported.

The generated finite certificate supports the arbitrary-subdivision proof in
``PROOF.md``; the combinatorial lift itself is a mathematical argument rather
than a finite computation.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from math import comb
from pathlib import Path

import sympy as sp


G = (0, 1, 2, 3)
BALANCED_SPLITS = ((0, 1), (0, 2), (0, 3))
COMPRESSED_WORDS = ((), (0,), (1,), (0, 1), (1, 0))


def xor_sum(values):
    result = 0
    for value in values:
        result ^= value
    return result


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, length - 1):
            yield (first,) + rest


@dataclass(frozen=True)
class PrimitiveCore:
    name: str
    source: str
    sinks: tuple[str, ...]
    arcs: tuple[tuple[str, str], ...]


# These are the five directed kernels obtained in Lemma 4.1 of PROOF.md.
# Repeated arcs denote distinct kernel paths; every accepted binary completion
# subdivides enough of them that the actual rooted graph has no parallel arcs.
CORES = (
    PrimitiveCore("cycle", "S", ("X",), (("S", "X"), ("S", "X"))),
    PrimitiveCore(
        "theta_TR_nested",
        "P", ("Q",),
        (("U", "V"), ("U", "V"), ("P", "U"), ("P", "Q"), ("V", "Q")),
    ),
    PrimitiveCore(
        "theta_TR_separated",
        "P", ("Q",),
        (("U", "V"), ("P", "U"), ("P", "V"), ("U", "Q"), ("V", "Q")),
    ),
    PrimitiveCore(
        "theta_TT_nested",
        "P", ("Q", "R"),
        (("U", "V"), ("P", "U"), ("P", "Q"), ("V", "Q"), ("U", "R"), ("V", "R")),
    ),
    PrimitiveCore(
        "theta_TT_separated",
        "P", ("Q", "R"),
        (("P", "U"), ("P", "V"), ("U", "Q"), ("V", "Q"), ("U", "R"), ("V", "R")),
    ),
)


def canonical_directed_multigraph(arcs):
    vertices = sorted({vertex for edge in arcs for vertex in edge})
    indegree, outdegree = degree_maps(arcs)
    role_classes = defaultdict(list)
    for vertex in vertices:
        role_classes[(indegree[vertex], outdegree[vertex])].append(vertex)
    ordered_roles = sorted(role_classes)
    best = None
    for blocks in itertools.product(*(itertools.permutations(role_classes[role]) for role in ordered_roles)):
        order = tuple(vertex for block in blocks for vertex in block)
        position = {vertex: index for index, vertex in enumerate(order)}
        code = (
            tuple((role, len(role_classes[role])) for role in ordered_roles),
            tuple(sorted((position[tail], position[head]) for tail, head in arcs)),
        )
        best = code if best is None or code < best else best
    return best


def acyclic_reachable(arcs, source, vertices):
    indegree, _outdegree = degree_maps(arcs)
    children = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    pending = {vertex: indegree[vertex] for vertex in vertices}
    queue = [vertex for vertex in vertices if pending[vertex] == 0]
    seen = []
    while queue:
        vertex = queue.pop()
        seen.append(vertex)
        for child in children[vertex]:
            pending[child] -= 1
            if pending[child] == 0:
                queue.append(child)
    return len(seen) == len(vertices) and reachable(arcs, source) == set(vertices)


def reduce_oriented_paths(paths, directed_edges):
    indegree, outdegree = degree_maps(directed_edges)
    retained = {
        vertex
        for path in paths
        for vertex in path
        if (indegree[vertex], outdegree[vertex]) != (1, 1)
        or vertex in (path[0], path[-1])
    }
    arc_set = set(directed_edges)
    reduced = []
    for path in paths:
        indices = [index for index, vertex in enumerate(path) if vertex in retained]
        for left_index, right_index in zip(indices, indices[1:]):
            segment = path[left_index : right_index + 1]
            if all((segment[index], segment[index + 1]) in arc_set for index in range(len(segment) - 1)):
                reduced.append((segment[0], segment[-1]))
            elif all((segment[index + 1], segment[index]) in arc_set for index in range(len(segment) - 1)):
                reduced.append((segment[-1], segment[0]))
            else:
                raise AssertionError("monotone suppression crossed an orientation event")
    return tuple(reduced)


def derive_primitive_orientations():
    # A length-three representative for each theta path has room for every
    # possible source/sink event (valid paths contain at most two events).
    paths = tuple(
        ("U", f"a{index}", f"b{index}", "V")
        for index in range(3)
    )
    undirected_edges = tuple(
        (path[index], path[index + 1])
        for path in paths
        for index in range(len(path) - 1)
    )
    theta_codes = Counter()
    for bits in itertools.product((0, 1), repeat=len(undirected_edges)):
        arcs = tuple(
            edge if bit == 0 else (edge[1], edge[0])
            for edge, bit in zip(undirected_edges, bits)
        )
        indegree, outdegree = degree_maps(arcs)
        internal = [vertex for path in paths for vertex in path[1:-1]]
        sources = [vertex for vertex in internal if (indegree[vertex], outdegree[vertex]) == (0, 2)]
        sinks = [vertex for vertex in internal if (indegree[vertex], outdegree[vertex]) == (2, 0)]
        if len(sources) != 1:
            continue
        if any((indegree[vertex], outdegree[vertex]) not in ((0, 2), (1, 1), (2, 0)) for vertex in internal):
            continue
        if any((indegree[pole], outdegree[pole]) not in ((1, 2), (2, 1)) for pole in ("U", "V")):
            continue
        reticulation_count = len(sinks) + sum(indegree[pole] == 2 for pole in ("U", "V"))
        if reticulation_count != 2:
            continue
        vertices = {vertex for path in paths for vertex in path}
        if not acyclic_reachable(arcs, sources[0], vertices):
            continue
        reduced = reduce_oriented_paths(paths, arcs)
        theta_codes[canonical_directed_multigraph(reduced)] += 1

    template_theta_codes = {
        canonical_directed_multigraph(core.arcs)
        for core in CORES
        if core.name.startswith("theta")
    }
    if set(theta_codes) != template_theta_codes:
        raise AssertionError("primitive theta orientation derivation does not match templates")

    # Cycle check on a four-cycle: one source, one sink, all other vertices
    # monotone.  Every valid orientation suppresses to two S-to-X paths.
    cycle_vertices = tuple(f"c{index}" for index in range(4))
    cycle_edges = tuple(
        (cycle_vertices[index], cycle_vertices[(index + 1) % 4])
        for index in range(4)
    )
    cycle_codes = Counter()
    cycle_paths_by_events = 0
    for bits in itertools.product((0, 1), repeat=4):
        arcs = tuple(edge if bit == 0 else (edge[1], edge[0]) for edge, bit in zip(cycle_edges, bits))
        indegree, outdegree = degree_maps(arcs)
        sources = [vertex for vertex in cycle_vertices if (indegree[vertex], outdegree[vertex]) == (0, 2)]
        sinks = [vertex for vertex in cycle_vertices if (indegree[vertex], outdegree[vertex]) == (2, 0)]
        if len(sources) != 1 or len(sinks) != 1:
            continue
        if any((indegree[vertex], outdegree[vertex]) not in ((0, 2), (1, 1), (2, 0)) for vertex in cycle_vertices):
            continue
        source, sink = sources[0], sinks[0]
        # Trace the two undirected source-to-sink paths.
        neighbors = defaultdict(list)
        for left, right in cycle_edges:
            neighbors[left].append(right)
            neighbors[right].append(left)
        paths_to_sink = []
        for first in neighbors[source]:
            path = [source, first]
            previous, current = source, first
            while current != sink:
                nxt = next(vertex for vertex in neighbors[current] if vertex != previous)
                path.append(nxt)
                previous, current = current, nxt
            paths_to_sink.append(tuple(path))
        reduced = reduce_oriented_paths(tuple(paths_to_sink), arcs)
        cycle_codes[canonical_directed_multigraph(reduced)] += 1
        cycle_paths_by_events += 1
    template_cycle_code = canonical_directed_multigraph(CORES[0].arcs)
    if set(cycle_codes) != {template_cycle_code}:
        raise AssertionError("primitive cycle orientation derivation does not match template")
    return {
        "status": "EXACTLY COMPUTED",
        "theta_orientation_classes": len(theta_codes),
        "theta_raw_orientations": sum(theta_codes.values()),
        "theta_class_multiplicities": sorted(theta_codes.values()),
        "cycle_orientation_classes": len(cycle_codes),
        "cycle_raw_orientations": cycle_paths_by_events,
        "template_match": True,
    }


@dataclass(frozen=True)
class Network:
    core: str
    role: str
    root: str
    arcs: tuple[tuple[str, str], ...]
    selected: tuple[tuple[str, int], ...]
    full_labels: tuple[tuple[str, int], ...]


def degree_maps(arcs):
    indegree = Counter()
    outdegree = Counter()
    for tail, head in arcs:
        outdegree[tail] += 1
        indegree[head] += 1
        indegree.setdefault(tail, 0)
        outdegree.setdefault(head, 0)
    return indegree, outdegree


def reachable(arcs, start, forbidden=None):
    children = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    result = set()
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex == forbidden or vertex in result:
            continue
        result.add(vertex)
        stack.extend(children[vertex])
    return result


def rooted_valid(network):
    arcs = network.arcs
    labels = dict(network.full_labels)
    vertices = {vertex for edge in arcs for vertex in edge}
    indegree, outdegree = degree_maps(arcs)
    if len(arcs) != len(set(arcs)) or any(tail == head for tail, head in arcs):
        return False
    if (indegree[network.root], outdegree[network.root]) != (0, 2):
        return False
    for vertex in vertices:
        degree = (indegree[vertex], outdegree[vertex])
        if vertex in labels:
            if degree != (1, 0):
                return False
        elif vertex != network.root and degree not in ((1, 2), (2, 1)):
            return False
    pending = dict(indegree)
    queue = [vertex for vertex in vertices if pending[vertex] == 0]
    visited = []
    children = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    while queue:
        vertex = queue.pop()
        visited.append(vertex)
        for child in children[vertex]:
            pending[child] -= 1
            if pending[child] == 0:
                queue.append(child)
    if len(visited) != len(vertices) or reachable(arcs, network.root) != vertices:
        return False
    # Lowest-stable-ancestor condition.
    leaves = set(labels)
    for candidate in vertices - leaves - {network.root}:
        if not (reachable(arcs, network.root, candidate) & leaves):
            return False
    # The displayed rooted presentation itself is tree-child.
    for vertex in vertices - leaves:
        if not any(child in leaves or indegree[child] == 1 for child in children[vertex]):
            return False
    return True


@dataclass(frozen=True)
class MixedEdge:
    endpoints: frozenset[str]
    arrowheads: frozenset[str]


def suppress_root(network):
    indegree, outdegree = degree_maps(network.arcs)
    reticulations = {
        vertex for vertex in set(indegree) | set(outdegree)
        if (indegree[vertex], outdegree[vertex]) == (2, 1)
    }
    retained = []
    incident = []
    for tail, head in network.arcs:
        edge = MixedEdge(frozenset((tail, head)), frozenset((head,)) if head in reticulations else frozenset())
        (incident if network.root in edge.endpoints else retained).append(edge)
    if len(incident) != 2:
        return None
    left = next(iter(incident[0].endpoints - {network.root}))
    right = next(iter(incident[1].endpoints - {network.root}))
    if left == right:
        return None
    inherited = (incident[0].arrowheads & {left}) | (incident[1].arrowheads & {right})
    retained.append(MixedEdge(frozenset((left, right)), inherited))
    return tuple(retained)


def standard_strong(network):
    edges = suppress_root(network)
    if edges is None:
        return False
    labels = dict(network.full_labels)
    if len({edge.endpoints for edge in edges}) != len(edges):
        return False
    incidence = defaultdict(list)
    incoming = Counter()
    undirected = Counter()
    tails = set()
    for edge in edges:
        if len(edge.arrowheads) > 1:
            return False
        for vertex in edge.endpoints:
            incidence[vertex].append(edge)
        if edge.arrowheads:
            head = next(iter(edge.arrowheads))
            incoming[head] += 1
            tails.update(edge.endpoints - {head})
        else:
            for vertex in edge.endpoints:
                undirected[vertex] += 1
    for vertex, adjacent in incidence.items():
        if vertex in labels:
            if len(adjacent) != 1:
                return False
        else:
            if len(adjacent) != 3 or incoming[vertex] not in (0, 2):
                return False
    # This is the proved rooting-independent S_TC criterion: no reticulation
    # tail and no ordinary vertex tails two reticulation edges.
    if any(undirected[tail] != 2 for tail in tails):
        return False
    return True


def build_network(core, selected_count, role, selected_sink_indices, counts, dummy_segments):
    arcs = []
    selected_leaves = []
    dummy_leaves = []
    for segment, ((tail, head), count) in enumerate(zip(core.arcs, counts)):
        chain = [tail]
        for position in range(count):
            parent = f"p{segment}_{position}"
            leaf = f"sel{len(selected_leaves)}"
            chain.append(parent)
            arcs.append((parent, leaf))
            selected_leaves.append(leaf)
        if segment in dummy_segments:
            parent = f"d{segment}"
            leaf = f"dum{len(dummy_leaves)}"
            chain.append(parent)
            arcs.append((parent, leaf))
            dummy_leaves.append(leaf)
        chain.append(head)
        arcs.extend(zip(chain, chain[1:]))

    chosen_sinks = {core.sinks[index] for index in selected_sink_indices}
    for sink in core.sinks:
        if sink in chosen_sinks:
            leaf = f"sel{len(selected_leaves)}"
            selected_leaves.append(leaf)
        else:
            leaf = f"dum{len(dummy_leaves)}"
            dummy_leaves.append(leaf)
        arcs.append((sink, leaf))

    root = core.source
    incoming_leaf = None
    if role != "root":
        root = "audit_root"
        incoming_leaf = "incoming"
        arcs.extend(((root, core.source), (root, incoming_leaf)))
        if role == "incoming":
            selected_leaves.append(incoming_leaf)
        else:
            dummy_leaves.append(incoming_leaf)

    if len(selected_leaves) != selected_count:
        raise AssertionError("selected count mismatch")
    selected = {leaf: index for index, leaf in enumerate(selected_leaves)}
    full = {leaf: index for index, leaf in enumerate(selected_leaves + dummy_leaves)}
    return Network(
        core.name, role, root, tuple(arcs), tuple(sorted(selected.items())), tuple(sorted(full.items()))
    )


def enumerate_networks(selected_count, role):
    """Generate every bounded completion; dummy ports occupy only empty runs."""

    result = []
    attempts = 0
    for core in CORES:
        incoming_selected = int(role == "incoming")
        outgoing_selected = selected_count - incoming_selected
        for sink_count in range(min(len(core.sinks), outgoing_selected) + 1):
            for chosen_sinks in itertools.combinations(range(len(core.sinks)), sink_count):
                ordinary = outgoing_selected - sink_count
                for counts in compositions(ordinary, len(core.arcs)):
                    empty = [index for index, count in enumerate(counts) if count == 0]
                    for dummy_mask in range(1 << len(empty)):
                        dummy = {empty[index] for index in range(len(empty)) if (dummy_mask >> index) & 1}
                        attempts += 1
                        network = build_network(
                            core, selected_count, role, chosen_sinks, counts, dummy
                        )
                        if rooted_valid(network) and standard_strong(network):
                            result.append(network)
    return result, attempts


def displayed_mask_details(network):
    selected = dict(network.selected)
    indegree, outdegree = degree_maps(network.arcs)
    reticulations = tuple(
        sorted(vertex for vertex in set(indegree) | set(outdegree) if (indegree[vertex], outdegree[vertex]) == (2, 1))
    )
    incoming = {
        reticulation: tuple(
            index for index, (_tail, head) in enumerate(network.arcs) if head == reticulation
        )
        for reticulation in reticulations
    }
    all_mask = (1 << len(selected)) - 1
    raw_rows = [[] for _ in network.arcs]
    rows = [[] for _ in network.arcs]
    for choice in itertools.product((0, 1), repeat=len(reticulations)):
        excluded = {
            incoming[reticulation][1 - bit]
            for reticulation, bit in zip(reticulations, choice)
        }
        children = defaultdict(list)
        for edge_index, (tail, head) in enumerate(network.arcs):
            if edge_index not in excluded:
                children[tail].append(head)
        memo = {}

        def descendants(vertex):
            if vertex not in memo:
                mask = (1 << selected[vertex]) if vertex in selected else 0
                for child in children[vertex]:
                    mask |= descendants(child)
                memo[vertex] = mask
            return memo[vertex]

        for edge_index, (_tail, head) in enumerate(network.arcs):
            raw_mask = 0 if edge_index in excluded else descendants(head)
            raw_rows[edge_index].append(raw_mask)
            mask = raw_mask
            if mask not in (0, all_mask):
                complement = all_mask ^ mask
                mask = min(mask, complement)
            else:
                mask = 0
            rows[edge_index].append(mask)
    # Serial edges with the same switching mask row contribute only through
    # the product of their open multipliers.
    signatures = tuple(sorted(set(tuple(row) for row in rows if any(row))))
    groups = {
        signature: [index for index, row in enumerate(rows) if tuple(row) == signature]
        for signature in signatures
    }
    details = {
        "switching_choices": [list(choice) for choice in itertools.product((0, 1), repeat=len(reticulations))],
        "edge_rows": [
            {
                "edge_index": index,
                "arc": list(network.arcs[index]),
                "raw_descendant_masks": list(raw_rows[index]),
                "zero_sum_normalized_masks": list(rows[index]),
            }
            for index in range(len(network.arcs))
        ],
        "effective_row_groups": [
            {"signature": list(signature), "edge_indices": groups[signature]}
            for signature in signatures
        ],
    }
    return signatures, reticulations, details


def displayed_masks(network):
    signatures, reticulations, _details = displayed_mask_details(network)
    return signatures, reticulations


def build_colored_network(core, words, extras, nonroot):
    arcs = []
    leaves = []
    colors = []
    for segment, ((tail, head), word) in enumerate(zip(core.arcs, words)):
        chain = [tail]
        for position, color in enumerate(word):
            parent = f"c{segment}_{position}"
            leaf = f"leaf{len(leaves)}"
            chain.append(parent)
            arcs.append((parent, leaf))
            leaves.append(leaf)
            colors.append(int(color))
        chain.append(head)
        arcs.extend(zip(chain, chain[1:]))
    extra_index = 0
    for sink in core.sinks:
        leaf = f"leaf{len(leaves)}"
        arcs.append((sink, leaf))
        leaves.append(leaf)
        colors.append(int(extras[extra_index]))
        extra_index += 1
    root = core.source
    if nonroot:
        root = "audit_root"
        leaf = f"leaf{len(leaves)}"
        arcs.extend(((root, core.source), (root, leaf)))
        leaves.append(leaf)
        colors.append(int(extras[extra_index]))
    labels = {leaf: index for index, leaf in enumerate(leaves)}
    network = Network(
        core.name,
        "incoming" if nonroot else "root",
        root,
        tuple(arcs),
        tuple(sorted(labels.items())),
        tuple(sorted(labels.items())),
    )
    return network, tuple(colors)


def switching_split_sets(network):
    labels = dict(network.selected)
    indegree, outdegree = degree_maps(network.arcs)
    reticulations = tuple(
        sorted(vertex for vertex in set(indegree) | set(outdegree) if (indegree[vertex], outdegree[vertex]) == (2, 1))
    )
    incoming = {
        reticulation: tuple(index for index, (_tail, head) in enumerate(network.arcs) if head == reticulation)
        for reticulation in reticulations
    }
    all_labels = frozenset(labels.values())
    result = []
    for choice in itertools.product((0, 1), repeat=len(reticulations)):
        excluded = {
            incoming[reticulation][1 - bit]
            for reticulation, bit in zip(reticulations, choice)
        }
        children = defaultdict(list)
        for edge_index, (tail, head) in enumerate(network.arcs):
            if edge_index not in excluded:
                children[tail].append(head)
        memo = {}

        def descendants(vertex):
            if vertex not in memo:
                value = {labels[vertex]} if vertex in labels else set()
                for child in children[vertex]:
                    value.update(descendants(child))
                memo[vertex] = frozenset(value)
            return memo[vertex]

        splits = set()
        for edge_index, (_tail, head) in enumerate(network.arcs):
            if edge_index in excluded:
                continue
            side = descendants(head)
            if side and side != all_labels:
                splits.add(side)
                splits.add(all_labels - side)
        result.append(splits)
    return tuple(result)


def displayed_color_split_by_all(network, colors):
    color_zero = frozenset(index for index, color in enumerate(colors) if color == 0)
    color_one = frozenset(range(len(colors))) - color_zero
    if min(len(color_zero), len(color_one)) < 2:
        return False
    return all(color_zero in splits or color_one in splits for splits in switching_split_sets(network))


def duplicate_singleton_colors(words, extras):
    occurrences = {0: [], 1: []}
    for segment, word in enumerate(words):
        for position, color in enumerate(word):
            occurrences[color].append((segment, position))
    for color in extras:
        occurrences[color].append(None)
    if any(not occurrences[color] for color in (0, 1)):
        return None
    result = [list(word) for word in words]
    changed = False
    for color in (0, 1):
        if len(occurrences[color]) != 1:
            continue
        location = occurrences[color][0]
        if location is None:
            return None
        segment, position = location
        result[segment].insert(position, color)
        changed = True
    return tuple(tuple(word) for word in result) if changed else None


def verify_switching_compression():
    records = []
    failures = []
    for nonroot in (False, True):
        for core in CORES:
            checked = 0
            valid = 0
            doubled = 0
            family_failures = []
            extra_count = len(core.sinks) + int(nonroot)
            for words in itertools.product(COMPRESSED_WORDS, repeat=len(core.arcs)):
                for extras in itertools.product((0, 1), repeat=extra_count):
                    colors = tuple(color for word in words for color in word) + tuple(extras)
                    if set(colors) == {0, 1} and min(Counter(colors).values()) >= 2:
                        checked += 1
                        network, actual_colors = build_colored_network(core, words, extras, nonroot)
                        if rooted_valid(network) and standard_strong(network):
                            valid += 1
                            if displayed_color_split_by_all(network, actual_colors):
                                family_failures.append({"words": words, "extras": extras, "kind": "compressed"})
                    expanded = duplicate_singleton_colors(words, extras)
                    if expanded is None:
                        continue
                    network, actual_colors = build_colored_network(core, expanded, extras, nonroot)
                    if rooted_valid(network) and standard_strong(network):
                        doubled += 1
                        if displayed_color_split_by_all(network, actual_colors):
                            family_failures.append({"words": expanded, "extras": extras, "kind": "singleton_doubled"})
            record = {
                "core": core.name,
                "role": "nonroot" if nonroot else "root",
                "balanced_compressed_checked": checked,
                "valid_balanced_compressed": valid,
                "valid_singleton_doubled": doubled,
                "survivors": family_failures,
            }
            records.append(record)
            failures.extend({"family": f"{core.name}:{nonroot}", **row} for row in family_failures)
    return {
        "status": "EXACTLY COMPUTED" if not failures else "FALSE",
        "families": records,
        "survivor_count": len(failures),
        "failures": failures,
    }


def choice_actions(reticulation_count):
    choices = tuple(itertools.product((0, 1), repeat=reticulation_count))
    position = {choice: index for index, choice in enumerate(choices)}
    actions = set()
    for permutation in itertools.permutations(range(reticulation_count)):
        for flips in itertools.product((0, 1), repeat=reticulation_count):
            actions.add(
                tuple(
                    position[tuple(choice[permutation[index]] ^ flips[index] for index in range(reticulation_count))]
                    for choice in choices
                )
            )
    return tuple(sorted(actions))


def relabel_mask(mask, permutation):
    result = 0
    for new_position, old_position in enumerate(permutation):
        if mask & (1 << old_position):
            result |= 1 << new_position
    return result


def tensor_variants(network, all_leaf_permutations):
    signatures, reticulations = displayed_masks(network)
    actions = choice_actions(len(reticulations))
    permutations = itertools.permutations(range(len(network.selected))) if all_leaf_permutations else (tuple(range(len(network.selected))),)
    candidates = []
    for permutation in permutations:
        relabelled = tuple(tuple(relabel_mask(mask, permutation) for mask in row) for row in signatures)
        for action in actions:
            transformed = tuple(sorted(tuple(row[index] for index in action) for row in relabelled))
            candidates.append((transformed, tuple(permutation), tuple(action)))
    transformed, permutation, action = min(candidates)
    return {transformed: {"leaf_permutation": permutation, "choice_action": action}}, len(reticulations)


def three_port_endpoint_variants(network):
    signatures, reticulations = displayed_masks(network)
    actions = choice_actions(len(reticulations))
    result = {}
    for central in range(3):
        outer = [index for index in range(3) if index != central]
        candidates = []
        for swap in (False, True):
            order = tuple((outer[::-1] if swap else outer) + [central])
            relabelled = tuple(tuple(relabel_mask(mask, order) for mask in row) for row in signatures)
            for action in actions:
                transformed = tuple(sorted(tuple(row[index] for index in action) for row in relabelled))
                candidates.append((transformed, order, tuple(action)))
        transformed, order, action = min(candidates)
        result.setdefault(
            transformed,
            {"leaf_permutation": order, "choice_action": action, "central_original_position": central},
        )
    return result, len(reticulations)


def tensor_hash(signatures, reticulation_count):
    return hashlib.sha256(repr((reticulation_count, signatures)).encode()).hexdigest()


class FourierTensor:
    def __init__(self, signatures, reticulation_count):
        self.signatures = signatures
        self.reticulation_count = reticulation_count
        self.edge_symbols = sp.symbols(f"x0:{len(signatures)}")
        self.lambda_symbols = sp.symbols(f"l0:{reticulation_count}")
        self.symbols = self.edge_symbols + self.lambda_symbols
        self.choices = tuple(itertools.product((0, 1), repeat=reticulation_count))
        self.cache = {}

    def coordinate(self, assignment):
        assignment = tuple(assignment)
        if assignment in self.cache:
            return self.cache[assignment]
        expression = 0
        for choice_index, choice in enumerate(self.choices):
            term = 1
            for bit, inheritance in zip(choice, self.lambda_symbols):
                term *= inheritance if bit == 0 else (1 - inheritance)
            for edge, row in zip(self.edge_symbols, self.signatures):
                if xor_sum(assignment[index] for index in range(len(assignment)) if row[choice_index] & (1 << index)):
                    term *= edge
            expression += term
        expression = sp.Poly(sp.expand(expression), *self.symbols, domain=sp.QQ)
        self.cache[assignment] = expression
        return expression


def bernstein_coefficients(poly, variables):
    variables = tuple(variables)
    if not variables:
        return [Fraction(poly.as_expr())]
    all_symbols = poly.gens
    positions = [all_symbols.index(variable) for variable in variables]
    degrees = [poly.degree(variable) for variable in variables]
    coefficient_map = {monomial: Fraction(coefficient) for monomial, coefficient in poly.terms()}
    values = []
    for beta in itertools.product(*(range(degree + 1) for degree in degrees)):
        total = Fraction(0)
        for monomial, coefficient in coefficient_map.items():
            alpha = [monomial[position] for position in positions]
            # This routine is called only when every polynomial variable is in
            # `variables`, so no residual symbolic coefficient remains.
            if any(monomial[index] for index in range(len(all_symbols)) if index not in positions):
                raise ValueError("residual symbol in scalar Bernstein conversion")
            if any(left > right for left, right in zip(alpha, beta)):
                continue
            multiplier = Fraction(1)
            for left, right, degree in zip(alpha, beta, degrees):
                multiplier *= Fraction(comb(right, left), comb(degree, left))
            total += coefficient * multiplier
        values.append(total)
    return values


def scalar_bernstein_sign(poly):
    variables = tuple(symbol for symbol in poly.gens if poly.degree(symbol) > 0)
    values = bernstein_coefficients(poly, variables)
    if all(value >= 0 for value in values) and any(value > 0 for value in values):
        return 1, values
    if all(value <= 0 for value in values) and any(value < 0 for value in values):
        return -1, values
    if not any(values):
        return 0, values
    return None, values


def factor_sign(poly):
    """Certify a strict sign by exact factorization and Bernstein bounds."""

    constant, factors = sp.factor_list(poly.as_expr(), *poly.gens)
    constant = Fraction(constant)
    if not constant:
        return 0, {"method": "zero"}
    sign = 1 if constant > 0 else -1
    certificate = []
    for expression, exponent in factors:
        factor = sp.Poly(expression, *poly.gens, domain=sp.QQ)
        factor_direction, values = scalar_bernstein_sign(factor)
        if exponent % 2 == 0:
            if factor_direction not in (-1, 1):
                return None, {"method": "factor", "failure": str(expression)}
        else:
            if factor_direction not in (-1, 1):
                return None, {"method": "factor", "failure": str(expression)}
            sign *= factor_direction
        certificate.append(
            {
                "factor": str(expression),
                "exponent": int(exponent),
                "sign": factor_direction,
                "bernstein_min": str(min(values)),
                "bernstein_max": str(max(values)),
                "bernstein_count": len(values),
            }
        )
    return sign, {"method": "factor_bernstein", "constant": str(constant), "factors": certificate}


def residual_poly(poly, retained_symbols, eliminated_symbols, beta, degrees):
    values = defaultdict(Fraction)
    retained_positions = [poly.gens.index(symbol) for symbol in retained_symbols]
    eliminated_positions = [poly.gens.index(symbol) for symbol in eliminated_symbols]
    for monomial, coefficient in poly.terms():
        alpha = [monomial[position] for position in eliminated_positions]
        if any(left > right for left, right in zip(alpha, beta)):
            continue
        multiplier = Fraction(1)
        for left, right, degree in zip(alpha, beta, degrees):
            multiplier *= Fraction(comb(right, left), comb(degree, left))
        retained_monomial = tuple(monomial[position] for position in retained_positions)
        values[retained_monomial] += Fraction(coefficient) * multiplier
    expression = 0
    for monomial, coefficient in values.items():
        term = sp.Rational(coefficient.numerator, coefficient.denominator)
        for symbol, exponent in zip(retained_symbols, monomial):
            term *= symbol ** exponent
        expression += term
    return sp.Poly(expression, *retained_symbols, domain=sp.QQ)


def nonnegative_factor_certificate(poly):
    if poly.is_zero:
        return True, False, {"zero": True}
    constant, factors = sp.factor_list(poly.as_expr(), *poly.gens)
    constant = Fraction(constant)
    if constant < 0:
        return False, False, {"constant": str(constant)}
    strict = constant > 0
    rows = []
    for expression, exponent in factors:
        factor = sp.Poly(expression, *poly.gens, domain=sp.QQ)
        direction, values = scalar_bernstein_sign(factor)
        if exponent % 2:
            if direction != 1:
                return False, False, {"failed_factor": str(expression), "exponent": int(exponent)}
        else:
            # An even factor is nonnegative; strictness additionally requires
            # that it never vanishes in the open cube.
            if direction not in (-1, 1):
                strict = False
        rows.append({"factor": str(expression), "exponent": int(exponent), "sign": direction})
    return True, strict, {"constant": str(constant), "factors": rows}


def inheritance_bernstein_positive(poly, inheritance_symbols):
    inheritance_symbols = tuple(inheritance_symbols)
    edge_symbols = tuple(symbol for symbol in poly.gens if symbol not in inheritance_symbols)
    degrees = [poly.degree(symbol) for symbol in inheritance_symbols]
    rows = []
    strict_count = 0
    for beta in itertools.product(*(range(degree + 1) for degree in degrees)):
        coefficient = residual_poly(poly, edge_symbols, inheritance_symbols, beta, degrees)
        nonnegative, strict, certificate = nonnegative_factor_certificate(coefficient)
        if not nonnegative:
            return None, {"method": "inheritance_bernstein", "failed_index": list(beta), "detail": certificate}
        strict_count += int(strict)
        rows.append({"index": list(beta), "strict": strict, "certificate": certificate})
    if strict_count:
        return 1, {
            "method": "inheritance_bernstein",
            "degrees": degrees,
            "coefficient_count": len(rows),
            "strict_coefficient_count": strict_count,
            "coefficients": rows,
        }
    return None, {"method": "inheritance_bernstein", "failure": "no uniformly strict coefficient"}


SIGN_CACHE = {}


def strict_sign(poly, inheritance_symbols=()):
    poly = sp.Poly(poly.as_expr(), *poly.gens, domain=sp.QQ)
    key = (tuple(poly.terms()), tuple(str(symbol) for symbol in inheritance_symbols))
    if key in SIGN_CACHE:
        return SIGN_CACHE[key]
    result = factor_sign(poly)
    if result[0] is None and inheritance_symbols:
        result = inheritance_bernstein_positive(poly, inheritance_symbols)
    if result[0] is None:
        negative = sp.Poly(-poly.as_expr(), *poly.gens, domain=sp.QQ)
        opposite = factor_sign(negative)
        if opposite[0] is None and inheritance_symbols:
            opposite = inheritance_bernstein_positive(negative, inheritance_symbols)
        if opposite[0] == 1:
            result = (-1, {"negated": opposite[1]})
    SIGN_CACHE[key] = result
    return result


THREE_ASSIGNMENTS = {
    "a": (1, 1, 0),
    "b": (1, 0, 1),
    "c": (0, 1, 1),
    "t": (1, 2, 3),
}


def endpoint_certificate(signatures, reticulation_count):
    # The median bridge-tree component can be an ordinary trivalent vertex.
    # Its sliced local tensor is the constant tensor 1; all physical attenuation
    # belongs to the three incident arms.  It is therefore the unique bounded
    # endpoint with F=G=0 before arm scaling.
    if not signatures and reticulation_count == 0:
        return True, {
            "case": "F_zero_G_zero_ordinary",
            "certificate": {
                "F": "0",
                "G": "0",
                "method": "exact_constant_ordinary_component",
            },
        }
    tensor = FourierTensor(signatures, reticulation_count)
    coordinates = {name: tensor.coordinate(assignment) for name, assignment in THREE_ASSIGNMENTS.items()}
    expression = coordinates["a"] * coordinates["b"] * coordinates["c"] - coordinates["t"] ** 2
    expression = sp.Poly(sp.expand(expression.as_expr()), *tensor.symbols, domain=sp.QQ)
    if expression.is_zero:
        auxiliary = coordinates["a"] - coordinates["b"] * coordinates["c"]
        auxiliary = sp.Poly(sp.expand(auxiliary.as_expr()), *tensor.symbols, domain=sp.QQ)
        sign, certificate = strict_sign(auxiliary, tensor.lambda_symbols)
        return sign == 1, {"case": "F_zero_G_positive", "certificate": certificate}
    sign, certificate = strict_sign(expression, tensor.lambda_symbols)
    return sign == 1, {"case": "F_positive", "certificate": certificate}


def displayed_split_status(signatures, split):
    mask = sum(1 << position for position in split)
    complement = 15 ^ mask
    width = len(signatures[0])
    return tuple(any(row[index] in (mask, complement) for row in signatures) for index in range(width))


def block_minor_candidates(tensor, split):
    left = tuple(split)
    right = tuple(position for position in range(4) if position not in left)
    for character_sum in G:
        pairs = tuple(pair for pair in itertools.product(G, repeat=2) if pair[0] ^ pair[1] == character_sum)
        matrix = []
        for left_pair in pairs:
            row = []
            for right_pair in pairs:
                assignment = [0] * 4
                for position, character in zip(left, left_pair):
                    assignment[position] = character
                for position, character in zip(right, right_pair):
                    assignment[position] = character
                row.append(tensor.coordinate(tuple(assignment)))
            matrix.append(row)
        for rows in itertools.combinations(range(4), 2):
            for columns in itertools.combinations(range(4), 2):
                determinant = matrix[rows[0]][columns[0]] * matrix[rows[1]][columns[1]] - matrix[rows[0]][columns[1]] * matrix[rows[1]][columns[0]]
                determinant = sp.Poly(sp.expand(determinant.as_expr()), *tensor.symbols, domain=sp.QQ)
                if not determinant.is_zero:
                    yield character_sum, rows, columns, determinant


def one_active_certificate(signatures, reticulation_count, split):
    tensor = FourierTensor(signatures, reticulation_count)
    candidates = sorted(
        block_minor_candidates(tensor, split),
        key=lambda row: (len(row[3].terms()), row[0], row[1], row[2]),
    )
    for character_sum, rows, columns, determinant in candidates:
        sign, certificate = strict_sign(determinant, tensor.lambda_symbols)
        if sign in (-1, 1):
            return {
                "character_sum": character_sum,
                "rows": list(rows),
                "columns": list(columns),
                "sign": sign,
                "terms": len(determinant.terms()),
                "polynomial_sha256": hashlib.sha256(repr(determinant.terms()).encode()).hexdigest(),
                "certificate": certificate,
            }
    return None


def collect_tensors(selected_count):
    roles = ("root", "incoming", "outgoing")
    records = {}
    metrics = {}
    for role in roles:
        networks, attempts = enumerate_networks(selected_count, role)
        accepted = 0
        for network in networks:
            variants, reticulation_count = (
                three_port_endpoint_variants(network)
                if selected_count == 3
                else tensor_variants(network, all_leaf_permutations=True)
            )
            for signatures, transport in variants.items():
                key = (reticulation_count, signatures)
                if key not in records:
                    records[key] = (network, transport)
                accepted += 1
        metrics[role] = {
            "attempts": attempts,
            "valid_presentations": len(networks),
            "generated_variants": accepted,
        }
    return records, metrics


def graph_record(network, transport, expected_signatures):
    signatures, reticulations, details = displayed_mask_details(network)
    permutation = tuple(transport["leaf_permutation"])
    action = tuple(transport["choice_action"])
    relabelled = tuple(
        tuple(relabel_mask(mask, permutation) for mask in row)
        for row in signatures
    )
    transported = tuple(
        sorted(tuple(row[index] for index in action) for row in relabelled)
    )
    if transported != expected_signatures:
        raise AssertionError("graph-to-mask transport does not reproduce tensor")
    return {
        "core": network.core,
        "role": network.role,
        "root": network.root,
        "arcs": [list(edge) for edge in network.arcs],
        "selected": dict(network.selected),
        "full_labels": dict(network.full_labels),
        "displayed_tree_compilation": details,
        "reticulations": list(reticulations),
        "transport": {
            key: list(value) if isinstance(value, tuple) else value
            for key, value in transport.items()
        },
        "transport_reproduces_tensor": True,
    }


def verify_endpoint_universe():
    tensors, metrics = collect_tensors(3)
    # Add the ordinary trivalent median component.  It has no internal local
    # edge or inheritance parameter after the three incident arms are split
    # off, so its descendant-mask signature tuple is empty.
    tensors.setdefault((0, ()), None)
    metrics["ordinary_component"] = {
        "attempts": 1,
        "valid_presentations": 1,
        "generated_variants": 1,
    }
    rows = []
    failures = []
    counts = Counter()
    for index, ((reticulation_count, signatures), witness_data) in enumerate(sorted(tensors.items(), key=lambda item: repr(item[0]))):
        witness, transport = (None, None) if witness_data is None else witness_data
        success, certificate = endpoint_certificate(signatures, reticulation_count)
        counts[certificate["case"]] += 1
        if not success:
            failures.append({"index": index, "hash": tensor_hash(signatures, reticulation_count), "certificate": certificate})
        rows.append(
            {
                "id": index,
                "tensor_sha256": tensor_hash(signatures, reticulation_count),
                "reticulation_count": reticulation_count,
                "signatures": [list(row) for row in signatures],
                "witness_graph": (
                    {
                        "core": "ordinary_trivalent_component",
                        "role": "projective_component",
                        "ports": 3,
                        "signatures": [],
                        "transport_reproduces_tensor": True,
                    }
                    if witness is None
                    else graph_record(witness, transport, signatures)
                ),
                "dichotomy": certificate,
            }
        )
    return {
        "status": "EXACTLY COMPUTED" if not failures else "FALSE",
        "metrics": metrics,
        "tensor_count": len(rows),
        "dichotomy_counts": dict(counts),
        "failures": failures,
        "records": rows,
    }


def verify_one_active_universe():
    tensors, metrics = collect_tensors(4)
    # Add the ordinary four-leaf tree as a one-choice descendant-mask tensor.
    tree_signatures = tuple((mask,) for mask in (1, 2, 3, 4, 8, 12))
    tensors.setdefault((0, tree_signatures), None)
    rows = []
    failures = []
    checked_splits = 0
    skipped_common = 0
    for index, ((reticulation_count, signatures), witness_data) in enumerate(sorted(tensors.items(), key=lambda item: repr(item[0]))):
        split_rows = []
        for split in BALANCED_SPLITS:
            status = displayed_split_status(signatures, split)
            if all(status):
                skipped_common += 1
                split_rows.append({"split": list(split), "displayed_by_all": True})
                continue
            certificate = one_active_certificate(signatures, reticulation_count, split)
            checked_splits += 1
            if certificate is None:
                failures.append({"id": index, "split": list(split), "tensor_sha256": tensor_hash(signatures, reticulation_count)})
            split_rows.append(
                {
                    "split": list(split),
                    "displayed_by_all": False,
                    "strict_minor": certificate,
                }
            )
        rows.append(
            {
                "id": index,
                "tensor_sha256": tensor_hash(signatures, reticulation_count),
                "reticulation_count": reticulation_count,
                "signatures": [list(row) for row in signatures],
                "witness_graph": (
                    None
                    if witness_data is None
                    else graph_record(witness_data[0], witness_data[1], signatures)
                ),
                "splits": split_rows,
            }
        )
        if (index + 1) % 25 == 0:
            print(f"one-active {index + 1}/{len(tensors)}", flush=True)
    return {
        "status": "EXACTLY COMPUTED" if not failures else "FALSE",
        "metrics": metrics,
        "tensor_count": len(rows),
        "strict_wrong_split_certificates": checked_splits,
        "common_displayed_splits_skipped": skipped_common,
        "failures": failures,
        "records": rows,
    }


def verify_two_active_identity():
    a, b, c, t, A, B, C, T, z = sp.symbols("a b c t A B C T z")

    def endpoint(assignment, lower):
        aa, bb, cc, tt = (a, b, c, t) if lower else (A, B, C, T)
        nonzero = [index for index, value in enumerate(assignment) if value]
        if not nonzero:
            return 1
        if len(nonzero) == 2:
            zero = next(index for index, value in enumerate(assignment) if not value)
            return (cc, bb, aa)[zero]
        if len(nonzero) == 3 and len(set(assignment)) == 3:
            return tt
        raise AssertionError("not a zero-sum three-port orbit")

    minors = set()
    for total in G:
        pairs = tuple(pair for pair in itertools.product(G, repeat=2) if pair[0] ^ pair[1] == total)
        matrix = []
        for g1, g3 in pairs:
            row = []
            for g2, g4 in pairs:
                separator = g1 ^ g2
                row.append(sp.expand(endpoint((g1, g2, separator), True) * endpoint((g3, g4, separator), False) * (z if separator else 1)))
            matrix.append(row)
        for rows in itertools.combinations(range(4), 2):
            for columns in itertools.combinations(range(4), 2):
                determinant = sp.expand(matrix[rows[0]][columns[0]] * matrix[rows[1]][columns[1]] - matrix[rows[0]][columns[1]] * matrix[rows[1]][columns[0]])
                if determinant:
                    polynomial = sp.Poly(determinant, a, b, c, t, A, B, C, T, z, domain=sp.QQ)
                    terms = tuple(polynomial.terms())
                    negative = tuple(sp.Poly(-determinant, *polynomial.gens, domain=sp.QQ).terms())
                    minors.add(min(terms, negative))

    required = {
        "f1": a * A - z**2 * b * c * B * C,
        "f2": z * T * t - z**2 * b * c * B * C,
        "f3": z * C * (A * t - z * T * b * c),
        "f4": z * c * (z * B * C * t - T * a),
    }
    membership = {}
    for name, expression in required.items():
        polynomial = sp.Poly(sp.expand(expression), a, b, c, t, A, B, C, T, z, domain=sp.QQ)
        membership[name] = min(tuple(polynomial.terms()), tuple(sp.Poly(-expression, *polynomial.gens, domain=sp.QQ).terms())) in minors
    f1, f2, f3, f4 = (required[name] for name in ("f1", "f2", "f3", "f4"))
    identities = {
        "Aa_equals_zTt": sp.expand(a * A - z * T * t - (f1 - f2)),
        "left_F": sp.expand(z**2 * C * T * (a * b * c - t**2) - (z * C * t * (f1 - f2) - a * f3)),
        "right_F": sp.expand(z**2 * c * t * (A * B * C - T**2) - (A * f4 + z * c * T * (f1 - f2))),
    }
    success = all(membership.values()) and all(value == 0 for value in identities.values())
    return {
        "status": "EXACTLY COMPUTED" if success else "FALSE",
        "minor_count_up_to_sign": len(minors),
        "required_minor_membership": membership,
        "identity_remainders": {name: str(value) for name, value in identities.items()},
        "strict_contradiction": "F_left=F_right=0 forces a>=bc and A>=BC; positivity and 0<z<1 give aA>=bcBC>z^2bcBC, contradicting f1=0.",
    }


def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-one-active", action="store_true")
    arguments = parser.parse_args()
    primitive_derivation = derive_primitive_orientations()
    endpoint = verify_endpoint_universe()
    one_active = None if arguments.skip_one_active else verify_one_active_universe()
    two_active = verify_two_active_identity()
    switching = verify_switching_compression()
    status = "EXACTLY COMPUTED" if primitive_derivation["status"] == endpoint["status"] == two_active["status"] == switching["status"] == "EXACTLY COMPUTED" and (one_active is None or one_active["status"] == "EXACTLY COMPUTED") else "FALSE"
    result = {
        "status": status,
        "primitive_cores": [
            {"name": core.name, "source": core.source, "sinks": list(core.sinks), "arcs": [list(edge) for edge in core.arcs]}
            for core in CORES
        ],
        "primitive_orientation_derivation": primitive_derivation,
        "three_port_endpoint_dichotomy": endpoint,
        "one_active_wrong_split": one_active,
        "two_active_crossing": two_active,
        "switching_compression": switching,
        "sign_cache_entries": len(SIGN_CACHE),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": status,
        "endpoint_tensors": endpoint["tensor_count"],
        "endpoint_failures": len(endpoint["failures"]),
        "one_active_tensors": None if one_active is None else one_active["tensor_count"],
        "one_active_failures": None if one_active is None else len(one_active["failures"]),
        "two_active": two_active["status"],
        "switching_compression": switching["status"],
        "certificate_sha256": file_sha256(arguments.output),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
