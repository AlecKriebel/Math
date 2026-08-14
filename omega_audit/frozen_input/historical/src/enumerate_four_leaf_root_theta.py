"""Enumerate root-spanning simple four-leaf theta networks from the core atlas.

This is the first finite slice of the local JC atlas.  Every outgoing port is a
single labelled leaf, the unique root lies in the theta blob, and exactly four
ports are present.  The script quotients independently by unlabelled and
leaf-labelled directed graph isomorphism using exhaustive colour-preserving
permutations; no specialized phylogenetic package is used.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import permutations, product
import json

from enumerate_theta_orientation_cores import enumerate_cores, weak_compositions


def build_network(core, subdivision_counts):
    vertices = dict(core["vertex_types"])
    edges = []
    ordinary = []
    for segment_index, (segment, count) in enumerate(
        zip(core["directed_segments"], subdivision_counts)
    ):
        chain = [segment["tail"]]
        for index in range(count):
            vertex = f"P{segment_index}_{index}"
            vertices[vertex] = "T"
            ordinary.append(vertex)
            chain.append(vertex)
        chain.append(segment["head"])
        edges.extend(zip(chain, chain[1:]))

    port_parents = ordinary + sorted(vertex for vertex, color in vertices.items() if color == "X")
    leaves = []
    for index, parent in enumerate(port_parents):
        leaf = f"L{index}"
        vertices[leaf] = "L"
        leaves.append(leaf)
        edges.append((parent, leaf))
    return vertices, tuple(edges), tuple(leaves)


def valid_binary_strong(vertices, edges):
    indegree = Counter(head for _tail, head in edges)
    outdegree = Counter(tail for tail, _head in edges)
    if len(edges) != len(set(edges)):
        return False
    if any((head, tail) in set(edges) for tail, head in edges):
        return False
    for vertex, color in vertices.items():
        degree = (indegree[vertex], outdegree[vertex])
        if color == "S" and degree != (0, 2):
            return False
        if color == "T" and degree != (1, 2):
            return False
        if color in {"R", "X"} and degree != (2, 1):
            return False
        if color == "L" and degree != (1, 0):
            return False

    children = defaultdict(list)
    for tail, head in edges:
        children[tail].append(head)
    for vertex, color in vertices.items():
        if color in {"S", "T"}:
            if not any(vertices[child] in {"T", "L"} for child in children[vertex]):
                return False
        if color in {"R", "X"}:
            if vertices[children[vertex][0]] in {"R", "X"}:
                return False
    return True


def adjacency_code(order, edges):
    index = {vertex: i for i, vertex in enumerate(order)}
    size = len(order)
    matrix = [0] * (size * size)
    for tail, head in edges:
        matrix[index[tail] * size + index[head]] += 1
    return tuple(matrix)


def colour_groups(vertices, leaf_labels=None):
    groups = defaultdict(list)
    for vertex, color in vertices.items():
        if color == "L" and leaf_labels is not None:
            key = f"L{leaf_labels[vertex]}"
        elif color in {"R", "X"}:
            # Branch and path-sink reticulations are roles in the reduced
            # template, not vertex colours in a rooted-network isomorphism.
            key = "R"
        else:
            key = color
        groups[key].append(vertex)
    return [(key, tuple(sorted(groups[key]))) for key in sorted(groups)]


def canonical_code(vertices, edges, leaf_labels=None):
    groups = colour_groups(vertices, leaf_labels)
    best = None
    for choices in product(*(tuple(permutations(group)) for _color, group in groups)):
        order = tuple(vertex for choice in choices for vertex in choice)
        code = tuple(color for color, group in groups for _ in group) + adjacency_code(order, edges)
        if best is None or code < best:
            best = code
    return best


def leaf_automorphisms(vertices, edges, leaves):
    groups = colour_groups(vertices)
    baseline_order = tuple(vertex for _color, group in groups for vertex in group)
    baseline = adjacency_code(baseline_order, edges)
    position = {vertex: index for index, vertex in enumerate(leaves)}
    actions = set()
    for choices in product(*(tuple(permutations(group)) for _color, group in groups)):
        order = tuple(vertex for choice in choices for vertex in choice)
        if adjacency_code(order, edges) != baseline:
            continue
        mapping = dict(zip(baseline_order, order))
        actions.add(tuple(position[mapping[leaf]] for leaf in leaves))
    return actions


def labelled_canonical_codes(vertices, edges, leaves):
    codes = {}
    for labels in permutations((1, 2, 3, 4)):
        assignment = dict(zip(leaves, labels))
        code = canonical_code(vertices, edges, assignment)
        codes.setdefault(code, assignment)
    return codes


def semi_directed_triangle_count(vertices, edges):
    # Forget orientation and suppress only the global root S, which has two
    # neighbours.  Count simple undirected triples; parallel root-artifact
    # edges are retained as multiplicities but do not create a 3-vertex cycle.
    undirected = Counter(tuple(sorted(edge)) for edge in edges if "L" not in {vertices[edge[0]], vertices[edge[1]]})
    neighbours = []
    for edge, multiplicity in list(undirected.items()):
        if "S" in edge:
            other = edge[0] if edge[1] == "S" else edge[1]
            neighbours.extend((other,) * multiplicity)
            del undirected[edge]
    assert len(neighbours) == 2
    undirected[tuple(sorted(neighbours))] += 1
    internal = sorted(vertex for vertex, color in vertices.items() if color != "L" and vertex != "S")
    count = 0
    for triple in permutations(internal, 3):
        if not (triple[0] < triple[1] < triple[2]):
            continue
        if all(undirected[tuple(sorted(pair))] for pair in ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2]))):
            count += 1
    return count


def enumerate_networks():
    _raw, cores = enumerate_cores()
    unlabelled = {}
    expansion_count = 0
    for core_index, core in enumerate(cores):
        sink_count = sum(color == "X" for color in core["vertex_types"].values())
        ordinary_count = 4 - sink_count
        segment_count = len(core["directed_segments"])
        for counts in weak_compositions(ordinary_count, segment_count):
            expansion_count += 1
            vertices, edges, leaves = build_network(core, counts)
            if not valid_binary_strong(vertices, edges):
                continue
            code = canonical_code(vertices, edges)
            if code in unlabelled:
                continue
            leaf_actions = leaf_automorphisms(vertices, edges, leaves)
            labelled = labelled_canonical_codes(vertices, edges, leaves)
            assert len(labelled) == 24 // len(leaf_actions)
            unlabelled[code] = {
                "core_index": core_index,
                "core_signature": {
                    "branch_types": core["branch_types"],
                    "path_events": core["path_event_sequences_U_to_V"],
                },
                "subdivision_counts_by_directed_segment": list(counts),
                "vertices": vertices,
                "edges": [list(edge) for edge in edges],
                "leaves": list(leaves),
                "leaf_automorphism_order": len(leaf_actions),
                "leaf_automorphisms": [list(action) for action in sorted(leaf_actions)],
                "labelled_isomorphism_classes": len(labelled),
                "triangle_count_after_root_suppression": semi_directed_triangle_count(vertices, edges),
            }
    return expansion_count, list(unlabelled.values())


def main():
    expansion_count, networks = enumerate_networks()
    by_core = Counter(network["core_index"] for network in networks)
    labelled_by_core = Counter()
    triangle_counts = Counter()
    for network in networks:
        labelled_by_core[network["core_index"]] += network["labelled_isomorphism_classes"]
        triangle_counts[network["triangle_count_after_root_suppression"]] += 1
    summary = {
        "raw_ordinary_port_distributions": expansion_count,
        "unlabelled_root_spanning_simple_four_leaf_networks": len(networks),
        "unlabelled_by_theta_core_index": dict(sorted(by_core.items())),
        "labelled_by_theta_core_index": dict(sorted(labelled_by_core.items())),
        "total_leaf_labelled_isomorphism_classes": sum(labelled_by_core.values()),
        "unlabelled_by_triangle_count": dict(sorted(triangle_counts.items())),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
