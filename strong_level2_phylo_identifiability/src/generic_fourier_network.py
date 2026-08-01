"""Generic exact/modular displayed-tree Fourier evaluation for rooted DAGs."""

from __future__ import annotations

from itertools import product


def reticulation_vertices(vertices):
    return tuple(sorted(vertex for vertex, color in vertices.items() if color in {"R", "X"}))


def incoming_edge_indices(edges, reticulation):
    return tuple(index for index, (_tail, head) in enumerate(edges) if head == reticulation)


def selected_edge_indices(vertices, edges, choices):
    excluded = set()
    for reticulation, choice in zip(reticulation_vertices(vertices), choices):
        incoming = incoming_edge_indices(edges, reticulation)
        assert len(incoming) == 2
        excluded.add(incoming[1 - choice])
    return tuple(index for index in range(len(edges)) if index not in excluded)


def descendant_labels(edges, selected, leaf_labels):
    children = {}
    for index in selected:
        parent, child = edges[index]
        children.setdefault(parent, []).append(child)
    cache = {}

    def descend(vertex):
        if vertex in cache:
            return cache[vertex]
        if vertex in leaf_labels:
            answer = frozenset((leaf_labels[vertex],))
        else:
            answer = frozenset().union(*(descend(child) for child in children.get(vertex, ())))
        cache[vertex] = answer
        return answer

    return {index: descend(edges[index][1]) for index in selected}


def precompute_displayed_trees(vertices, edges, leaf_labels):
    reticulations = reticulation_vertices(vertices)
    trees = []
    for choices in product((0, 1), repeat=len(reticulations)):
        selected = selected_edge_indices(vertices, edges, choices)
        trees.append((choices, selected, descendant_labels(edges, selected, leaf_labels)))
    return reticulations, tuple(trees)


def evaluate_jc_coordinates(
    vertices,
    edges,
    leaf_labels,
    assignments,
    edge_parameters,
    inheritance_parameters,
    modulus=None,
):
    """Evaluate zero-sum JC Fourier coordinates exactly or modulo a prime."""
    reticulations, trees = precompute_displayed_trees(vertices, edges, leaf_labels)
    assert set(inheritance_parameters) == set(reticulations)
    outputs = []
    for assignment in assignments:
        by_leaf = {index + 1: character for index, character in enumerate(assignment)}
        total = 0
        for choices, selected, descendants in trees:
            term = 1
            for reticulation, choice in zip(reticulations, choices):
                inheritance = inheritance_parameters[reticulation]
                term *= inheritance if choice == 0 else 1 - inheritance
                if modulus is not None:
                    term %= modulus
            for edge_index in selected:
                character = 0
                for leaf in descendants[edge_index]:
                    character ^= by_leaf[leaf]
                if character:
                    term *= edge_parameters[edge_index]
                    if modulus is not None:
                        term %= modulus
            total += term
            if modulus is not None:
                total %= modulus
        outputs.append(total)
    return tuple(outputs)

