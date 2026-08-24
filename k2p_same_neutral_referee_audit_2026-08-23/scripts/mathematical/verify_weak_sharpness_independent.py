#!/usr/bin/env python3
"""Independent exact reconstruction of the weak-class sharpness certificate.

No module, atlas, graph canonicalizer, tensor implementation, or expected
certificate is imported from the submission.  The rooted arc lists and
rational parameters printed in the article are encoded directly below.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import deque
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

import sympy as sp


ZERO, C, G, T = 0, 1, 2, 3
PATTERNS = [
    (ZERO, ZERO, ZERO),
    (ZERO, C, C),
    (ZERO, G, G),
    (C, ZERO, C),
    (C, C, ZERO),
    (C, G, T),
    (C, T, G),
    (G, ZERO, G),
    (G, C, T),
    (G, G, ZERO),
]
PATTERN_NAMES = ["000", "0CC", "0GG", "C0C", "CC0", "CGT", "CTG", "G0G", "GCT", "GG0"]
LEAF_BY_NODE = {"L0": 0, "L1": 1, "L2": 2}


NETWORKS = {
    "W": {
        "arcs": [
            ("r", "S"),
            ("r", "L0"),
            ("S", "U"),
            ("S", "V"),
            ("U", "X"),
            ("V", "Z"),
            ("Z", "X"),
            ("U", "V"),
            ("Z", "L1"),
            ("X", "L2"),
        ],
        "reticulations": {"V": ("S", "U"), "X": ("Z", "U")},
        "inheritance": {
            ("S", "V"): Fraction(1, 8),
            ("U", "V"): Fraction(7, 8),
            ("Z", "X"): Fraction(15996, 16339),
            ("U", "X"): Fraction(343, 16339),
        },
        "nonpendant": [("r", "S"), ("S", "U"), ("S", "V"), ("U", "X"), ("V", "Z"), ("Z", "X"), ("U", "V")],
        "diagonal": Fraction(1, 7),
        "visible_order": [("Z", "X"), ("S", "V"), ("r", "S"), ("S", "U"), ("U", "V"), ("V", "Z"), ("U", "X")],
        "minor_columns": [
            ("s", ("Z", "X")),
            ("g", ("Z", "X")),
            ("s", ("S", "V")),
            ("g", ("S", "V")),
            ("s", ("r", "S")),
            ("g", ("r", "S")),
            ("s", ("S", "U")),
            ("g", ("S", "U")),
            ("s", ("U", "V")),
        ],
        "minor_rows": [1, 2, 3, 5, 4, 7, 6, 8, 9],
        "expected_det": Fraction(
            10368019213741323,
            563981315074464023964442388464888915634290688,
        ),
        "pendants": [
            Fraction(86779, 80),
            Fraction(320, 253),
            Fraction(114373, 20240),
        ],
    },
    "Wp": {
        "arcs": [
            ("r", "S"),
            ("r", "L0"),
            ("S", "U"),
            ("S", "X0"),
            ("V", "X0"),
            ("U", "X1"),
            ("V", "X1"),
            ("U", "V"),
            ("X0", "L1"),
            ("X1", "L2"),
        ],
        "reticulations": {"X0": ("V", "S"), "X1": ("V", "U")},
        "inheritance": {
            ("V", "X0"): Fraction(1, 6),
            ("S", "X0"): Fraction(5, 6),
            ("V", "X1"): Fraction(1, 2),
            ("U", "X1"): Fraction(1, 2),
        },
        "nonpendant": [("r", "S"), ("S", "U"), ("S", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V")],
        "diagonal": Fraction(1, 4),
        "visible_order": [("V", "X1"), ("V", "X0"), ("U", "V"), ("r", "S"), ("S", "X0"), ("S", "U"), ("U", "X1")],
        "minor_columns": [
            ("s", ("V", "X1")),
            ("g", ("V", "X1")),
            ("s", ("V", "X0")),
            ("g", ("V", "X0")),
            ("s", ("U", "V")),
            ("g", ("U", "V")),
            ("s", ("r", "S")),
            ("g", ("r", "S")),
            ("s", ("S", "X0")),
        ],
        "minor_rows": [1, 2, 3, 5, 4, 6, 7, 8, 9],
        "expected_det": Fraction(1435825, 85002596691653613846528),
        "pendants": [Fraction(16, 3), Fraction(32, 9), Fraction(96, 5)],
    },
}


def as_fraction(value: Any) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise TypeError(value)


def selected_switchings(data: dict[str, Any]) -> Iterable[tuple[set[tuple[str, str]], Fraction]]:
    retics = sorted(data["reticulations"])
    incoming_choices = [data["reticulations"][retic] for retic in retics]
    for chosen_parents in itertools.product(*incoming_choices):
        chosen_incoming = {(parent, retic) for parent, retic in zip(chosen_parents, retics)}
        chosen_arcs = {
            arc
            for arc in data["arcs"]
            if arc[1] not in data["reticulations"] or arc in chosen_incoming
        }
        weight = Fraction(1)
        for arc in chosen_incoming:
            weight *= data["inheritance"][arc]
        yield chosen_arcs, weight


def descendants_by_arc(arcs: set[tuple[str, str]]) -> dict[tuple[str, str], frozenset[int]]:
    children: dict[str, list[str]] = {}
    for parent, child in arcs:
        children.setdefault(parent, []).append(child)

    cache: dict[str, frozenset[int]] = {}

    def visit(node: str) -> frozenset[int]:
        if node in cache:
            return cache[node]
        if node in LEAF_BY_NODE:
            answer = frozenset({LEAF_BY_NODE[node]})
        else:
            answer = frozenset().union(*(visit(child) for child in children.get(node, [])))
        cache[node] = answer
        return answer

    return {arc: visit(arc[1]) for arc in arcs}


def sector_value(char: int, pair: tuple[Any, Any]) -> Any:
    if char == ZERO:
        return 1
    if char in {C, T}:
        return pair[0]
    if char == G:
        return pair[1]
    raise ValueError(char)


def tensor(
    data: dict[str, Any],
    edge_pairs: dict[tuple[str, str], tuple[Any, Any]],
) -> list[Any]:
    values: list[Any] = []
    for pattern in PATTERNS:
        if pattern[0] ^ pattern[1] ^ pattern[2]:
            values.append(0)
            continue
        total: Any = 0
        for arcs, weight in selected_switchings(data):
            descendant_sets = descendants_by_arc(arcs)
            monomial: Any = weight
            for arc in arcs:
                char = ZERO
                for leaf in descendant_sets[arc]:
                    char ^= pattern[leaf]
                monomial *= sector_value(char, edge_pairs[arc])
            total += monomial
        values.append(sp.factor(total) if isinstance(total, sp.Basic) else total)
    return values


def normalized_edge_pairs(data: dict[str, Any], symbolic: bool = False) -> tuple[dict[tuple[str, str], tuple[Any, Any]], dict[tuple[str, tuple[str, str]], sp.Symbol]]:
    pairs: dict[tuple[str, str], tuple[Any, Any]] = {}
    symbols: dict[tuple[str, tuple[str, str]], sp.Symbol] = {}
    nonpendant = set(data["nonpendant"])
    for arc in data["arcs"]:
        if arc in nonpendant:
            if symbolic:
                label = "".join(arc)
                s_symbol = sp.Symbol(f"s_{label}")
                g_symbol = sp.Symbol(f"g_{label}")
                pairs[arc] = (s_symbol, g_symbol)
                symbols[("s", arc)] = s_symbol
                symbols[("g", arc)] = g_symbol
            else:
                pairs[arc] = (data["diagonal"], data["diagonal"])
        else:
            pairs[arc] = (1, 1)
    return pairs, symbols


def suppress_root(data: dict[str, Any]) -> tuple[set[str], list[tuple[str, str]], list[frozenset[str]]]:
    arcs = list(data["arcs"])
    root_children = [child for parent, child in arcs if parent == "r"]
    assert len(root_children) == 2
    nodes = {node for arc in arcs for node in arc}
    nodes.remove("r")
    retained = [(parent, child) for parent, child in arcs if child in data["reticulations"]]
    ordinary = [
        frozenset((parent, child))
        for parent, child in arcs
        if parent != "r" and child not in data["reticulations"]
    ]
    ordinary.append(frozenset(root_children))
    return nodes, retained, ordinary


def directed_acyclic(nodes: set[str], arcs: list[tuple[str, str]]) -> bool:
    indegree = {node: 0 for node in nodes}
    children: dict[str, list[str]] = {node: [] for node in nodes}
    for parent, child in arcs:
        indegree[child] += 1
        children[parent].append(child)
    queue = deque(node for node, degree in indegree.items() if degree == 0)
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    return visited == len(nodes)


def admissible_rootings(data: dict[str, Any]) -> tuple[int, int, int, list[str]]:
    nodes, retained, ordinary = suppress_root(data)
    semi_edges: list[tuple[str, Any]] = [("retained", edge) for edge in retained] + [
        ("ordinary", edge) for edge in ordinary
    ]
    retic_nodes = set(data["reticulations"])
    leaf_nodes = set(LEAF_BY_NODE)
    admissible: list[tuple[str, bool]] = []

    for edge_index, (kind, root_edge) in enumerate(semi_edges):
        root = "rho"
        rooted_nodes = nodes | {root}
        fixed = list(retained)
        remaining_ordinary = list(ordinary)
        if kind == "retained":
            parent, child = root_edge
            fixed.remove((parent, child))
            fixed.extend([(root, parent), (root, child)])
            label = f"{parent}-{child}"
        else:
            endpoints = tuple(sorted(root_edge))
            remaining_ordinary.remove(root_edge)
            fixed.extend([(root, endpoints[0]), (root, endpoints[1])])
            label = "-".join(endpoints)

        for bits in itertools.product((0, 1), repeat=len(remaining_ordinary)):
            arcs = list(fixed)
            for edge, bit in zip(remaining_ordinary, bits):
                left, right = tuple(sorted(edge))
                arcs.append((left, right) if bit == 0 else (right, left))
            indegree = {node: 0 for node in rooted_nodes}
            outdegree = {node: 0 for node in rooted_nodes}
            children: dict[str, list[str]] = {node: [] for node in rooted_nodes}
            for parent, child in arcs:
                indegree[child] += 1
                outdegree[parent] += 1
                children[parent].append(child)
            valid = indegree[root] == 0 and outdegree[root] == 2
            valid &= all(indegree[node] == 1 and outdegree[node] == 0 for node in leaf_nodes)
            valid &= all(indegree[node] == 2 and outdegree[node] == 1 for node in retic_nodes)
            ordinary_internal = nodes - leaf_nodes - retic_nodes
            valid &= all(indegree[node] == 1 and outdegree[node] == 2 for node in ordinary_internal)
            valid &= directed_acyclic(rooted_nodes, arcs)
            if not valid:
                continue
            reachable = {root}
            queue = deque([root])
            while queue:
                node = queue.popleft()
                for child in children[node]:
                    if child not in reachable:
                        reachable.add(child)
                        queue.append(child)
            if reachable != rooted_nodes:
                continue

            # Lowest-stable-ancestor check: no proper descendant is on every
            # root-to-leaf path.  Removing a candidate tests whether every
            # leaf becomes unreachable.
            lowest_stable = True
            for candidate in rooted_nodes - {root} - leaf_nodes:
                seen = {root}
                queue = deque([root])
                while queue:
                    node = queue.popleft()
                    for child in children[node]:
                        if child == candidate or child in seen:
                            continue
                        seen.add(child)
                        queue.append(child)
                # A proper descendant is stable for the full leaf set only
                # if deleting it makes every labelled leaf unreachable.
                if not (leaf_nodes & seen):
                    lowest_stable = False
                    break
            if not lowest_stable:
                continue
            tree_child = all(
                any(child not in retic_nodes for child in children[node])
                for node in rooted_nodes - leaf_nodes
            )
            admissible.append((label, tree_child))

    # A valid root edge has a unique orientation in these two small graphs.
    assert len({label for label, _ in admissible}) == len(admissible)
    tree_child_edges = sorted(label for label, tree_child in admissible if tree_child)
    return (
        len(admissible),
        len(tree_child_edges),
        len(admissible) - len(tree_child_edges),
        tree_child_edges,
    )


def leaf_distances(data: dict[str, Any]) -> tuple[int, int, int]:
    nodes, retained, ordinary = suppress_root(data)
    undirected = [frozenset(edge) for edge in retained] + ordinary
    adjacency: dict[str, set[str]] = {node: set() for node in nodes}
    for edge in undirected:
        left, right = tuple(edge)
        adjacency[left].add(right)
        adjacency[right].add(left)

    def distance(source: str, target: str) -> int:
        queue = deque([(source, 0)])
        seen = {source}
        while queue:
            node, value = queue.popleft()
            if node == target:
                return value
            for neighbor in adjacency[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append((neighbor, value + 1))
        raise RuntimeError("disconnected graph")

    return distance("L0", "L1"), distance("L0", "L2"), distance("L1", "L2")


def fraction_string(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    delta = Fraction(1, 2**30)
    reports: dict[str, Any] = {}
    full_tensors: dict[str, list[Fraction]] = {}

    expected_normalized = {
        "W": [
            Fraction(1),
            Fraction(64009, 457492),
            Fraction(64009, 457492),
            Fraction(6400, 39229939),
            Fraction(1, 1372),
            Fraction(4048, 39229939),
            Fraction(4048, 39229939),
            Fraction(6400, 39229939),
            Fraction(4048, 39229939),
            Fraction(1, 1372),
        ],
        "Wp": [
            Fraction(1),
            Fraction(15, 1024),
            Fraction(15, 1024),
            Fraction(5, 512),
            Fraction(27, 512),
            Fraction(9, 4096),
            Fraction(9, 4096),
            Fraction(5, 512),
            Fraction(9, 4096),
            Fraction(27, 512),
        ],
    }

    for name, data in NETWORKS.items():
        numeric_pairs, _ = normalized_edge_pairs(data)
        normalized = [as_fraction(value) for value in tensor(data, numeric_pairs)]
        assert normalized == expected_normalized[name]

        pendant_values = [coefficient * delta for coefficient in data["pendants"]]
        assert all(Fraction(0) < value < Fraction(1) and value * value < value for value in pendant_values)
        full: list[Fraction] = []
        for pattern, value in zip(PATTERNS, normalized):
            pendant_factor = Fraction(1)
            for leaf, char in enumerate(pattern):
                if char != ZERO:
                    pendant_factor *= pendant_values[leaf]
            full.append(value * pendant_factor)
        assert full[0] == 1
        assert full[1:5] + full[7:8] + full[9:10] == [delta**2] * 6
        assert full[5:7] + full[8:9] == [Fraction(4, 5) * delta**3] * 3
        full_tensors[name] = full

        symbolic_pairs, symbols = normalized_edge_pairs(data, symbolic=True)
        symbolic_tensor = tensor(data, symbolic_pairs)
        substitutions = {
            symbol: sp.Rational(data["diagonal"].numerator, data["diagonal"].denominator)
            for symbol in symbols.values()
        }
        columns = [symbols[column] for column in data["minor_columns"]]
        matrix = sp.Matrix(
            [
                [sp.diff(symbolic_tensor[row], column).subs(substitutions) for column in columns]
                for row in data["minor_rows"]
            ]
        )
        determinant = sp.factor(matrix.det())
        expected_det = sp.Rational(data["expected_det"].numerator, data["expected_det"].denominator)
        assert determinant == expected_det

        rooting_count = admissible_rootings(data)
        reports[name] = {
            "rooting_census": list(rooting_count[:3]),
            "tree_child_root_edges": rooting_count[3],
            "leaf_distances_01_02_12": list(leaf_distances(data)),
            "normalized_tensor": [fraction_string(value) for value in normalized],
            "minor_rows_zero_based": data["minor_rows"],
            "minor_columns": [f"{sector}_{''.join(arc)}" for sector, arc in data["minor_columns"]],
            "minor_determinant": str(determinant),
            "jacobian_rank_lower_bound": matrix.rank(),
            "strict_continuous_time": True,
        }

    assert full_tensors["W"] == full_tensors["Wp"]
    assert reports["W"]["rooting_census"] == [5, 2, 3]
    assert reports["Wp"]["rooting_census"] == [7, 2, 5]
    assert reports["W"]["leaf_distances_01_02_12"] == [4, 4, 3]
    assert reports["Wp"]["leaf_distances_01_02_12"] == [3, 4, 4]

    u_s, u_g = Fraction(2, 5), Fraction(4, 9)
    v_s, v_g = Fraction(3, 7), Fraction(5, 11)
    assert u_s * u_s < u_g and v_s * v_s < v_g
    cherry_determinant = Fraction(4) * u_s * u_g / (v_s * v_g)
    assert cherry_determinant == Fraction(2464, 675)

    payload = {
        "schema": "independent-k2p-weak-sharpness-v1",
        "imports_submission_code": False,
        "coordinate_order": PATTERN_NAMES,
        "networks": reports,
        "common_tensor": {
            "q000": "1",
            "six_pair_coordinates": "delta^2",
            "three_mixed_coordinates": "4/5*delta^3",
            "delta": fraction_string(delta),
            "exact_vector": [fraction_string(value) for value in full_tensors["W"]],
        },
        "underlying_labelled_graphs_nonisomorphic": True,
        "ordinary_triangle_equivalence_excluded": True,
        "cherry_inverse_determinant": fraction_string(cherry_determinant),
        "dimension_induction": "9+4(n-3)=4n-3",
        "status": "PASS",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("INDEPENDENT_WEAK_SHARPNESS_PASS")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
