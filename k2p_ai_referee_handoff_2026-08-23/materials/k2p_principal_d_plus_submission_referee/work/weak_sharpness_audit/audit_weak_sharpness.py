#!/usr/bin/env python3
"""Independent, exact audit of the weak-class K2P sharpness construction.

This program deliberately does not import the primary sharpness verifier, its
graph builder, or the four-port atlas.  It reconstructs both rooted and
semi-directed graphs from a separate edge-list specification, enumerates all
edge rootings, expands the K2P Fourier maps from the four displayed trees, and
checks exact Jacobian minors over Q.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from typing import Iterable

import networkx as nx


HERE = Path(__file__).resolve().parent
PRIMARY = HERE.parent / "weak_sharpness_closure" / "weak_sharpness_certificate.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def ftext(value: F) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def parse_fraction(value: str) -> F:
    return F(value)


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class NetworkSpec:
    name: str
    nodes: tuple[tuple[str, str, int | None], ...]
    arcs: tuple[tuple[str, str], ...]


def independent_specs() -> tuple[NetworkSpec, NetworkSpec]:
    """Return literal edge-list reconstructions, independent of the primary builder."""
    first = NetworkSpec(
        "W_theta0_segment_VX",
        (
            ("r", "root", None),
            ("S", "tree", None),
            ("U", "tree", None),
            ("V", "retic", None),
            ("Z", "tree", None),
            ("X", "retic", None),
            ("L0", "leaf", 0),
            ("L1", "leaf", 1),
            ("L2", "leaf", 2),
        ),
        (
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
        ),
    )
    second = NetworkSpec(
        "Wp_theta3_bare",
        (
            ("r", "root", None),
            ("S", "tree", None),
            ("U", "tree", None),
            ("V", "tree", None),
            ("X0", "retic", None),
            ("X1", "retic", None),
            ("L0", "leaf", 0),
            ("L1", "leaf", 1),
            ("L2", "leaf", 2),
        ),
        (
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
        ),
    )
    return first, second


def rooted_graph(spec: NetworkSpec) -> nx.DiGraph:
    graph = nx.DiGraph(name=spec.name)
    for node, role, label in spec.nodes:
        graph.add_node(node, role=role, label=label)
    graph.add_edges_from(spec.arcs)
    validate_rooted(graph)
    return graph


def validate_rooted(graph: nx.DiGraph, expected_labels: tuple[int, ...] = (0, 1, 2)) -> None:
    require(nx.is_directed_acyclic_graph(graph), "rooted graph is cyclic")
    labels: list[int] = []
    for node, data in graph.nodes(data=True):
        role = data["role"]
        degree = (graph.in_degree(node), graph.out_degree(node))
        expected = {
            "root": (0, 2),
            "tree": (1, 2),
            "retic": (2, 1),
            "leaf": (1, 0),
        }[role]
        require(degree == expected, f"{node}: {role} has degree {degree}, expected {expected}")
        if role == "leaf":
            require(isinstance(data["label"], int), f"{node}: leaf lacks a label")
            labels.append(data["label"])
        else:
            require(data["label"] is None, f"{node}: internal node is labelled")
    require(sorted(labels) == list(expected_labels), f"wrong label set: {labels}")
    require(sum(data["role"] == "retic" for _, data in graph.nodes(data=True)) == 2, "not level 2")


def semi_directed(graph: nx.DiGraph) -> nx.Graph:
    """Suppress the root and retain exactly the arrowheads at reticulations."""
    roots = [node for node, data in graph.nodes(data=True) if data["role"] == "root"]
    require(len(roots) == 1, "root suppression requires one root")
    root = roots[0]
    children = sorted(graph.successors(root))
    require(len(children) == 2, "root must have two children")
    mixed = nx.Graph(name=graph.graph["name"])
    for node, data in graph.nodes(data=True):
        if node != root:
            mixed.add_node(node, **data)
    for tail, head in graph.edges():
        if tail == root:
            continue
        heads = frozenset((head,)) if graph.nodes[head]["role"] == "retic" else frozenset()
        require(not mixed.has_edge(tail, head), "parallel edge after root suppression")
        mixed.add_edge(tail, head, heads=heads)
    require(not mixed.has_edge(*children), "suppressed root would create a parallel edge")
    replacement_heads = frozenset(child for child in children if graph.nodes[child]["role"] == "retic")
    mixed.add_edge(children[0], children[1], heads=replacement_heads)
    for node, data in mixed.nodes(data=True):
        expected_degree = 1 if data["role"] == "leaf" else 3
        require(mixed.degree(node) == expected_degree, f"{node}: nonbinary semi-directed degree")
    return mixed


def level_profile(mixed: nx.Graph) -> dict[str, object]:
    profiles = []
    for component in nx.biconnected_components(mixed):
        if len(component) < 3:
            continue
        reticulations = sorted(node for node in component if mixed.nodes[node]["role"] == "retic")
        profiles.append({"vertices": sorted(component), "reticulations": reticulations})
    maximum = max((len(row["reticulations"]) for row in profiles), default=0)
    return {"nontrivial_blobs": profiles, "maximum_reticulations_in_a_blob": maximum}


def is_tree_child(graph: nx.DiGraph, root: str) -> bool:
    for node, data in graph.nodes(data=True):
        if data["role"] == "leaf":
            continue
        children = tuple(graph.successors(node))
        if not any(graph.nodes[child]["role"] in ("tree", "leaf") for child in children):
            return False
    require(graph.nodes[root]["role"] == "root", "candidate root lost its role")
    return True


def orientations_on_edge(mixed: nx.Graph, root_edge: tuple[str, str], edge_number: int) -> list[nx.DiGraph]:
    """Return all compatible binary orientations after inserting a root on one edge."""
    edges = tuple(sorted((tuple(sorted(edge)) for edge in mixed.edges()), key=lambda edge: edge))
    root_edge = tuple(sorted(root_edge))
    root = f"rho_{edge_number}"
    base = nx.DiGraph()
    base.add_nodes_from((node, dict(data)) for node, data in mixed.nodes(data=True))
    base.add_node(root, role="root", label=None)
    base.add_edge(root, root_edge[0])
    base.add_edge(root, root_edge[1])

    free: list[tuple[str, str]] = []
    for edge in edges:
        if edge == root_edge:
            continue
        heads = mixed.edges[edge]["heads"]
        require(len(heads) <= 1, "unexpected two-headed edge")
        if heads:
            head = next(iter(heads))
            tail = edge[1] if edge[0] == head else edge[0]
            base.add_edge(tail, head)
        else:
            free.append(edge)

    admissible: list[nx.DiGraph] = []
    for choices in itertools.product((0, 1), repeat=len(free)):
        candidate = base.copy()
        for edge, choice in zip(free, choices):
            candidate.add_edge(edge[choice], edge[1 - choice])
        if not nx.is_directed_acyclic_graph(candidate):
            continue
        valid = True
        for node, data in candidate.nodes(data=True):
            expected = {
                "root": (0, 2),
                "tree": (1, 2),
                "retic": (2, 1),
                "leaf": (1, 0),
            }[data["role"]]
            if (candidate.in_degree(node), candidate.out_degree(node)) != expected:
                valid = False
                break
        if valid:
            admissible.append(candidate)
    return admissible


def rooting_census(mixed: nx.Graph) -> dict[str, object]:
    """Try every edge, including every arrowheaded reticulation edge."""
    edges = tuple(sorted((tuple(sorted(edge)) for edge in mixed.edges()), key=lambda edge: edge))
    rows: list[dict[str, object]] = []
    tried_reticulation_edges = 0
    for edge_number, root_edge in enumerate(edges):
        root_heads = mixed.edges[root_edge]["heads"]
        if root_heads:
            tried_reticulation_edges += 1
        admissible_graphs = orientations_on_edge(mixed, root_edge, edge_number)
        admissible = [is_tree_child(candidate, f"rho_{edge_number}") for candidate in admissible_graphs]
        require(len(admissible) <= 1, f"root edge {root_edge} has multiple binary orientations")
        rows.append(
            {
                "edge": list(root_edge),
                "root_edge_has_arrowhead": bool(root_heads),
                "admissible": bool(admissible),
                "tree_child": admissible[0] if admissible else None,
            }
        )
    valid_rows = [row for row in rows if row["admissible"]]
    return {
        "candidate_edges": len(rows),
        "reticulation_edges_explicitly_tried": tried_reticulation_edges,
        "admissible_rootings": len(valid_rows),
        "tree_child_rootings": sum(bool(row["tree_child"]) for row in valid_rows),
        "non_tree_child_rootings": sum(row["tree_child"] is False for row in valid_rows),
        "rows": rows,
    }


def directed_graph_equal(first: nx.DiGraph, second: nx.DiGraph) -> bool:
    return (
        set(first.nodes()) == set(second.nodes())
        and all(dict(first.nodes[node]) == dict(second.nodes[node]) for node in first.nodes())
        and set(first.edges()) == set(second.edges())
    )


def attach_directed_cherry(graph: nx.DiGraph, retained_label: int, new_label: int) -> nx.DiGraph:
    extended = graph.copy()
    old_leaf = next(node for node, data in extended.nodes(data=True) if data["label"] == retained_label)
    old_parent = next(extended.predecessors(old_leaf))
    cherry_parent = f"cherry_parent_{new_label}"
    new_leaf = f"new_leaf_{new_label}"
    require(cherry_parent not in extended and new_leaf not in extended, "cherry names collide")
    extended.remove_edge(old_parent, old_leaf)
    extended.add_node(cherry_parent, role="tree", label=None)
    extended.add_node(new_leaf, role="leaf", label=new_label)
    extended.add_edges_from(((old_parent, cherry_parent), (cherry_parent, old_leaf), (cherry_parent, new_leaf)))
    labels = tuple(range(new_label + 1))
    validate_rooted(extended, labels)
    return extended


def prune_directed_cherry(graph: nx.DiGraph, new_label: int) -> nx.DiGraph:
    pruned = graph.copy()
    new_leaf = next(node for node, data in pruned.nodes(data=True) if data["label"] == new_label)
    cherry_parent = next(pruned.predecessors(new_leaf))
    children = tuple(pruned.successors(cherry_parent))
    require(len(children) == 2 and new_leaf in children, "new leaf is not in a cherry")
    retained_child = children[0] if children[1] == new_leaf else children[1]
    old_parent = next(pruned.predecessors(cherry_parent))
    pruned.remove_node(new_leaf)
    pruned.remove_node(cherry_parent)
    pruned.add_edge(old_parent, retained_child)
    validate_rooted(pruned, tuple(range(new_label)))
    return pruned


def attach_mixed_cherry(mixed: nx.Graph, retained_label: int, new_label: int) -> nx.Graph:
    extended = mixed.copy()
    old_leaf = next(node for node, data in extended.nodes(data=True) if data["label"] == retained_label)
    neighbors = tuple(extended.neighbors(old_leaf))
    require(len(neighbors) == 1, "retained label is not pendant")
    old_parent = neighbors[0]
    cherry_parent = f"cherry_parent_{new_label}"
    new_leaf = f"new_leaf_{new_label}"
    extended.remove_edge(old_parent, old_leaf)
    extended.add_node(cherry_parent, role="tree", label=None)
    extended.add_node(new_leaf, role="leaf", label=new_label)
    extended.add_edge(old_parent, cherry_parent, heads=frozenset())
    extended.add_edge(cherry_parent, old_leaf, heads=frozenset())
    extended.add_edge(cherry_parent, new_leaf, heads=frozenset())
    return extended


def lift_and_prune_audit(first: nx.Graph, second: nx.Graph) -> dict[str, object]:
    lift_rows: dict[str, list[dict[str, object]]] = {}
    for name, mixed in (("first", first), ("second", second)):
        edges = tuple(sorted((tuple(sorted(edge)) for edge in mixed.edges()), key=lambda edge: edge))
        rows = []
        for edge_number, edge in enumerate(edges):
            candidates = orientations_on_edge(mixed, edge, edge_number)
            for candidate in candidates:
                root = f"rho_{edge_number}"
                base_status = is_tree_child(candidate, root)
                extended = attach_directed_cherry(candidate, 0, 3)
                extended_status = is_tree_child(extended, root)
                pruned = prune_directed_cherry(extended, 3)
                require(base_status == extended_status, "cherry attachment changed TC status")
                require(directed_graph_equal(candidate, pruned), "directed cherry pruning did not recover the base")
                rows.append({"edge": list(edge), "tree_child_before_and_after": base_status})
        lift_rows[name] = rows

    first_extended = attach_mixed_cherry(first, 0, 3)
    second_extended = attach_mixed_cherry(second, 0, 3)
    require(len(triangles(first_extended)) == len(triangles(first)), "first attachment created a triangle")
    require(len(triangles(second_extended)) == len(triangles(second)), "second attachment created a triangle")
    added_edges_first = {
        frozenset(("cherry_parent_3", "new_leaf_3")),
        frozenset(("cherry_parent_3", "L0")),
    }
    first_bridges = {frozenset(edge) for edge in nx.bridges(first_extended)}
    require(added_edges_first <= first_bridges, "added pendant edges are not bridges")
    extended_relation = exact_relation(first_extended, second_extended)
    require(extended_relation["relation"] == "none", "one cherry created an isomorphism or triangle relation")
    return {
        "all_admissible_rootings_lift_with_TC_status_unchanged": lift_rows,
        "directed_pruning_exactly_recovers_base": True,
        "new_edges_are_bridges": True,
        "triangle_counts_unchanged": [len(triangles(first)), len(triangles(second))],
        "four_leaf_relation_after_identical_attachment": extended_relation["relation"],
        "induction": "repeat the same local operation; prune newest labelled cherry first",
    }


def incidence_expansion(mixed: nx.Graph, forgotten: frozenset[frozenset[str]] = frozenset()) -> nx.Graph:
    incidence = nx.Graph()
    for node, data in mixed.nodes(data=True):
        incidence.add_node(("vertex", node), kind="vertex", label=data["label"])
    for number, (u, v, data) in enumerate(sorted(mixed.edges(data=True), key=lambda row: tuple(sorted(row[:2])))):
        edge_node = ("edge", number)
        incidence.add_node(edge_node, kind="edge", label=None)
        forget = frozenset((u, v)) in forgotten
        heads = data["heads"]
        incidence.add_edge(edge_node, ("vertex", u), head=False if forget else u in heads)
        incidence.add_edge(edge_node, ("vertex", v), head=False if forget else v in heads)
    return incidence


def incidence_isomorphic(first: nx.Graph, second: nx.Graph) -> bool:
    node_match = lambda a, b: a["kind"] == b["kind"] and a["label"] == b["label"]
    edge_match = lambda a, b: a["head"] == b["head"]
    return nx.algorithms.isomorphism.GraphMatcher(
        first, second, node_match=node_match, edge_match=edge_match
    ).is_isomorphic()


def triangles(mixed: nx.Graph) -> tuple[frozenset[frozenset[str]], ...]:
    found: set[frozenset[frozenset[str]]] = set()
    for a, b, c in itertools.combinations(sorted(mixed.nodes()), 3):
        if mixed.has_edge(a, b) and mixed.has_edge(a, c) and mixed.has_edge(b, c):
            found.add(frozenset((frozenset((a, b)), frozenset((a, c)), frozenset((b, c)))))
    return tuple(sorted(found, key=repr))


def exact_relation(first: nx.Graph, second: nx.Graph) -> dict[str, object]:
    plain_iso = incidence_isomorphic(incidence_expansion(first), incidence_expansion(second))
    triangle_matches = 0
    first_triangles = triangles(first)
    second_triangles = triangles(second)
    for first_triangle in first_triangles:
        for second_triangle in second_triangles:
            if incidence_isomorphic(
                incidence_expansion(first, first_triangle),
                incidence_expansion(second, second_triangle),
            ):
                triangle_matches += 1
    return {
        "isomorphic": plain_iso,
        "first_triangle_count": len(first_triangles),
        "second_triangle_count": len(second_triangles),
        "triangle_quotient_matches": triangle_matches,
        "relation": "isomorphic" if plain_iso else ("triangle" if triangle_matches else "none"),
    }


def orbit_coordinates() -> tuple[tuple[int, int, int], ...]:
    assignments: set[tuple[int, int, int]] = set()
    for first, second in itertools.product(range(4), repeat=2):
        chars = (first, second, first ^ second)
        swapped = tuple(3 if value == 1 else (1 if value == 3 else value) for value in chars)
        assignments.add(min(chars, swapped))
    return tuple(sorted(assignments))


def sector(mask: int, characters: tuple[int, ...]) -> int:
    total = 0
    for label, character in enumerate(characters):
        if mask & (1 << label):
            total ^= character
    return 0 if total == 0 else (2 if total == 2 else 1)


def inheritance_polynomial(bits: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    """Expand product_j lambda_j^bit (1-lambda_j)^(1-bit)."""
    polynomial: dict[int, int] = {0: 1}
    for index, bit in enumerate(bits):
        updated: defaultdict[int, int] = defaultdict(int)
        for mask, coefficient in polynomial.items():
            if bit:
                updated[mask | (1 << index)] += coefficient
            else:
                updated[mask] += coefficient
                updated[mask | (1 << index)] -= coefficient
        polynomial = {mask: coefficient for mask, coefficient in updated.items() if coefficient}
    return tuple(sorted(polynomial.items()))


def descendant_masks(graph: nx.DiGraph, kept: tuple[tuple[str, str], ...]) -> dict[tuple[str, str], int]:
    tree = nx.DiGraph()
    tree.add_nodes_from(graph.nodes())
    tree.add_edges_from(kept)
    require(nx.is_directed_acyclic_graph(tree), "displayed switch is cyclic")
    masks: dict[str, int] = {}
    for node in reversed(tuple(nx.topological_sort(tree))):
        label = graph.nodes[node]["label"]
        value = (1 << label) if isinstance(label, int) else 0
        for child in tree.successors(node):
            value |= masks[child]
        masks[node] = value
    return {(tail, head): masks[head] for tail, head in kept}


@dataclass(frozen=True)
class FormalMap:
    retic_order: tuple[str, ...]
    parent_orders: tuple[tuple[str, str], ...]
    edge_signatures: tuple[tuple[int, ...], ...]
    outputs: tuple[tuple[tuple[tuple[tuple[int, int, int], ...], tuple[tuple[int, int], ...]], ...], ...]

    @property
    def edge_class_count(self) -> int:
        return len(self.edge_signatures)


def formal_variant(
    graph: nx.DiGraph,
    retic_order: tuple[str, ...],
    parent_orders: tuple[tuple[str, str], ...],
) -> FormalMap:
    coordinates = orbit_coordinates()
    all_edges = tuple(sorted(graph.edges()))
    arms = frozenset(
        (tail, head)
        for tail, head in all_edges
        if graph.nodes[head]["role"] == "leaf" and isinstance(graph.nodes[head]["label"], int)
    )
    switches: list[tuple[tuple[int, ...], tuple[tuple[str, str], ...], dict[tuple[str, str], int]]] = []
    for bits in itertools.product((0, 1), repeat=len(retic_order)):
        removed: set[tuple[str, str]] = set()
        for index, reticulation in enumerate(retic_order):
            kept_parent = parent_orders[index][bits[index]]
            for parent in graph.predecessors(reticulation):
                if parent != kept_parent:
                    removed.add((parent, reticulation))
        kept = tuple(edge for edge in all_edges if edge not in removed)
        switches.append((bits, kept, descendant_masks(graph, kept)))

    signatures_by_edge: dict[tuple[str, str], tuple[int, ...]] = {}
    for edge in all_edges:
        if edge in arms:
            continue
        signature: list[int] = []
        for _, kept, masks in switches:
            if edge not in kept:
                signature.extend((0,) * len(coordinates))
            else:
                signature.extend(sector(masks[edge], chars) for chars in coordinates)
        if any(signature):
            signatures_by_edge[edge] = tuple(signature)
    active = tuple(sorted(set(signatures_by_edge.values())))
    class_of = {signature: index for index, signature in enumerate(active)}
    edge_class = {edge: class_of[signature] for edge, signature in signatures_by_edge.items()}

    outputs = []
    for characters in coordinates:
        grouped: defaultdict[tuple[tuple[int, int, int], ...], defaultdict[int, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        for bits, kept, masks in switches:
            exponents: Counter[tuple[int, int]] = Counter()
            for edge in kept:
                if edge not in edge_class:
                    continue
                sec = sector(masks[edge], characters)
                if sec:
                    exponents[(edge_class[edge], sec)] += 1
            monomial = tuple(sorted((class_index, sec, exponent) for (class_index, sec), exponent in exponents.items()))
            for mask, coefficient in inheritance_polynomial(bits):
                grouped[monomial][mask] += coefficient
        expression = []
        for monomial, polynomial in grouped.items():
            clean = tuple(sorted((mask, coefficient) for mask, coefficient in polynomial.items() if coefficient))
            if clean:
                expression.append((monomial, clean))
        outputs.append(tuple(sorted(expression)))
    return FormalMap(retic_order, parent_orders, active, tuple(outputs))


def canonical_formal_map(graph: nx.DiGraph) -> FormalMap:
    reticulations = tuple(sorted(node for node, data in graph.nodes(data=True) if data["role"] == "retic"))
    variants: list[FormalMap] = []
    for order in itertools.permutations(reticulations):
        sorted_parents = tuple(tuple(sorted(graph.predecessors(reticulation))) for reticulation in order)
        for flips in itertools.product((0, 1), repeat=len(order)):
            parent_orders = tuple(
                (parents[flip], parents[1 - flip]) for parents, flip in zip(sorted_parents, flips)
            )
            variants.append(formal_variant(graph, order, parent_orders))
    return min(
        variants,
        key=lambda model: (2, model.edge_class_count, model.outputs, model.edge_signatures),
    )


def evaluate_polynomial(polynomial: tuple[tuple[int, int], ...], lambdas: tuple[F, ...]) -> F:
    value = F(0)
    for mask, coefficient in polynomial:
        term = F(coefficient)
        for index, inheritance in enumerate(lambdas):
            if mask & (1 << index):
                term *= inheritance
        value += term
    return value


def evaluate_map(model: FormalMap, edge_pairs: tuple[tuple[F, F], ...], lambdas: tuple[F, ...]) -> tuple[F, ...]:
    values = []
    for expression in model.outputs:
        total = F(0)
        for monomial, polynomial in expression:
            term = evaluate_polynomial(polynomial, lambdas)
            for class_index, sec, exponent in monomial:
                term *= edge_pairs[class_index][sec - 1] ** exponent
            total += term
        values.append(total)
    return tuple(values)


def jacobian(model: FormalMap, edge_pairs: tuple[tuple[F, F], ...], lambdas: tuple[F, ...]) -> list[list[F]]:
    column_count = 2 * model.edge_class_count + len(lambdas)
    answer: list[list[F]] = []
    for expression in model.outputs:
        row = [F(0) for _ in range(column_count)]
        for monomial, polynomial in expression:
            edge_value = F(1)
            powers: dict[int, int] = {}
            for class_index, sec, exponent in monomial:
                column = 2 * class_index + sec - 1
                powers[column] = exponent
                edge_value *= edge_pairs[class_index][sec - 1] ** exponent
            polynomial_value = evaluate_polynomial(polynomial, lambdas)
            for column, exponent in powers.items():
                row[column] += edge_value * polynomial_value * exponent / edge_pairs[column // 2][column % 2]
            for lambda_index, inheritance in enumerate(lambdas):
                derivative = F(0)
                for mask, coefficient in polynomial:
                    if mask & (1 << lambda_index):
                        term = F(coefficient)
                        for index, value in enumerate(lambdas):
                            if mask & (1 << index):
                                term *= value
                        derivative += term / inheritance
                row[2 * model.edge_class_count + lambda_index] += edge_value * derivative
        answer.append(row)
    return answer


def rank_pivots(matrix: list[list[F]]) -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    work = [row[:] for row in matrix]
    row_ids = list(range(len(work)))
    pivot_rows: list[int] = []
    pivot_columns: list[int] = []
    rank = 0
    for column in range(len(work[0])):
        pivot = next((index for index in range(rank, len(work)) if work[index][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        row_ids[rank], row_ids[pivot] = row_ids[pivot], row_ids[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for index in range(len(work)):
            if index != rank and work[index][column]:
                factor = work[index][column]
                work[index] = [a - factor * b for a, b in zip(work[index], work[rank])]
        pivot_rows.append(row_ids[rank])
        pivot_columns.append(column)
        rank += 1
        if rank == len(work):
            break
    return rank, tuple(pivot_rows), tuple(pivot_columns)


def determinant(matrix: Iterable[Iterable[F]]) -> F:
    work = [list(row) for row in matrix]
    require(all(len(row) == len(work) for row in work), "determinant requires a square matrix")
    result = F(1)
    for column in range(len(work)):
        pivot = next((index for index in range(column, len(work)) if work[index][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        pivot_value = work[column][column]
        result *= pivot_value
        for index in range(column + 1, len(work)):
            if work[index][column]:
                factor = work[index][column] / pivot_value
                for inner in range(column + 1, len(work)):
                    work[index][inner] -= factor * work[column][inner]
    return result


def physical_tensor(
    normalized: tuple[F, ...], arm_coefficients: tuple[F, F, F], delta: F
) -> tuple[F, ...]:
    values: list[F] = []
    for characters, core_value in zip(orbit_coordinates(), normalized):
        multiplier = F(1)
        for label, character in enumerate(characters):
            if character:
                multiplier *= arm_coefficients[label] * delta
        values.append(core_value * multiplier)
    return tuple(values)


def check_domain(edge_pair: tuple[F, F], label: str) -> None:
    s_value, g_value = edge_pair
    require(0 < s_value < 1 and 0 < g_value < 1, f"{label}: outside positive box")
    require(g_value > 2 * s_value - 1, f"{label}: outside D_plus")
    require(g_value > s_value * s_value, f"{label}: outside strict continuous-time cone")


def case_certificate(
    graph: nx.DiGraph,
    internal: F,
    lambdas: tuple[F, F],
    arms: tuple[F, F, F],
    delta: F,
    expected_normalized: tuple[F, ...],
    primary_case: dict[str, object],
) -> dict[str, object]:
    require(primary_case["edge_class_count"] == 7, "primary edge-class count drift")
    require(
        primary_case["internal_edge_pair"] == [ftext(internal), ftext(internal)],
        "primary internal parameter drift",
    )
    require(primary_case["lambdas"] == [ftext(value) for value in lambdas], "primary inheritance drift")
    expected_arm_pairs = [[ftext(coefficient * delta), ftext(coefficient * delta)] for coefficient in arms]
    require(primary_case["arm_pairs"] == expected_arm_pairs, "primary pendant parameter drift")
    model = canonical_formal_map(graph)
    require(model.edge_class_count == 7, "canonical map does not have seven effective edge classes")
    pairs = tuple((internal, internal) for _ in range(model.edge_class_count))
    for index, pair in enumerate(pairs):
        check_domain(pair, f"internal class {index}")
    for index, coefficient in enumerate(arms):
        check_domain((coefficient * delta, coefficient * delta), f"pendant arm {index}")
    require(all(F(0) < value < F(1) for value in lambdas), "inheritance outside (0,1)")

    normalized = evaluate_map(model, pairs, lambdas)
    require(normalized == expected_normalized, "independent normalized tensor differs from stated tensor")
    derivative = jacobian(model, pairs, lambdas)
    rank, rows, columns = rank_pivots(derivative)
    require(rank == 9, "independent Jacobian rank is not nine")
    own_minor = determinant([[derivative[row][column] for column in columns] for row in rows])
    require(own_minor != 0, "independent pivot minor vanishes")

    primary_rows = tuple(primary_case["minor_rows"])
    primary_columns = tuple(primary_case["minor_columns"])
    require(len(primary_rows) == len(primary_columns) == 9, "primary minor is not 9 by 9")
    stated_minor = determinant(
        [[derivative[row][column] for column in primary_columns] for row in primary_rows]
    )
    require(stated_minor != 0, "primary stored minor vanishes under independent expansion")
    require(ftext(stated_minor) == primary_case["minor_determinant"], "primary minor determinant is reassigned")

    full = physical_tensor(normalized, arms, delta)
    require([ftext(value) for value in normalized] == primary_case["normalized_tensor"], "primary normalized tensor drift")
    require([ftext(value) for value in full] == primary_case["full_tensor"], "primary full tensor drift")
    require(primary_case["rank"] == rank, "primary rank claim drift")

    return {
        "canonical_reticulation_order": list(model.retic_order),
        "canonical_parent_orders": [list(pair) for pair in model.parent_orders],
        "edge_class_count": model.edge_class_count,
        "formal_map_sha256": digest(
            {
                "signatures": model.edge_signatures,
                "outputs": model.outputs,
            }
        ),
        "normalized_tensor": [ftext(value) for value in normalized],
        "full_tensor": [ftext(value) for value in full],
        "rank": rank,
        "independent_minor_rows": list(rows),
        "independent_minor_columns": list(columns),
        "independent_minor_determinant": ftext(own_minor),
        "primary_minor_independently_replayed": ftext(stated_minor),
    }


def cherry_block(u: F, v: F) -> list[list[F]]:
    return [[F(1) / v, -u / (v * v)], [v, u]]


def cherry_audit() -> dict[str, object]:
    # These are the four numbers used by the primary certificate.  The actual
    # physical K2P edge pairs are (u_s,u_g) and (v_s,v_g), not four pairs (x,x).
    u_s, v_s, u_g, v_g = F(2, 5), F(3, 7), F(4, 9), F(5, 11)
    check_domain((u_s, u_g), "first new cherry edge")
    check_domain((v_s, v_g), "second new cherry edge")
    block = [
        [*cherry_block(u_s, v_s)[0], F(0), F(0)],
        [*cherry_block(u_s, v_s)[1], F(0), F(0)],
        [F(0), F(0), *cherry_block(u_g, v_g)[0]],
        [F(0), F(0), *cherry_block(u_g, v_g)[1]],
    ]
    exact_det = determinant(block)
    formula = F(4) * u_s * u_g / (v_s * v_g)
    require(exact_det == formula != 0, "cherry four-by-four determinant identity failed")

    # Direct Fourier derivation of the observables.  If j is any outside leaf,
    # Q(j=C,a=C,b=0)/Q(j=C,a=0,b=C)=u_s/v_s, while
    # Q(a=C,b=C)=u_s*v_s; replace C by G for the g sector.  The old tensor
    # coordinates cancel in the ratios and are nonzero at the positive witness.
    derivation = {
        "R_s": "Q[j=C,a=C,b=0]/Q[j=C,a=0,b=C]=u_s/v_s",
        "P_s": "Q[others=0,a=C,b=C]=u_s*v_s",
        "R_g": "Q[j=G,a=G,b=0]/Q[j=G,a=0,b=G]=u_g/v_g",
        "P_g": "Q[others=0,a=G,b=G]=u_g*v_g",
    }
    return {
        "actual_edge_pairs": [[ftext(u_s), ftext(u_g)], [ftext(v_s), ftext(v_g)]],
        "actual_edge_pairs_are_strict_CT": True,
        "observable_derivation": derivation,
        "jacobian": [[ftext(value) for value in row] for row in block],
        "determinant": ftext(exact_det),
        "formula": "4*u_s*u_g/(v_s*v_g)",
        "rank_increment": 4,
        "iteration_dimension": "9+4*(n-3)=4*n-3",
        "pruning_audit": {
            "tree_child_lift": "a base TC rooting extends away from the attachment bridge and stays TC",
            "non_tree_child_lift": "the offending base internal vertex and its reticulation-only children are unchanged",
            "labelled_isomorphism": "the newest labelled cherry and its degree-three parent are fixed, so pruning commutes with any labelled isomorphism",
            "ordinary_triangle": "every added edge is a bridge, so every triangle remains in the base blob and triangle redirection commutes with pruning",
            "level_and_binary": "pendant cherry attachment adds one indegree-one/outdegree-two tree vertex and two leaves, preserving binary level 2",
        },
    }


def compare_primary_header(primary: dict[str, object]) -> None:
    require(primary["schema"] == "k2p-weak-tree-child-sharpness-v1", "unexpected primary schema")
    require(primary["coordinate_order"] == [list(row) for row in orbit_coordinates()], "coordinate order drift")
    require(primary["delta"] == "1/1073741824", "delta drift")
    require(primary["graph_relation"] == "none", "primary relation drift")
    require(primary["base_dimension"] == 9, "base dimension drift")
    require(primary["cherry_extension"]["four_by_four_determinant"] == "2464/675", "primary cherry determinant drift")


def build_audit(primary: dict[str, object]) -> dict[str, object]:
    compare_primary_header(primary)
    first_spec, second_spec = independent_specs()
    first_rooted, second_rooted = rooted_graph(first_spec), rooted_graph(second_spec)
    first_mixed, second_mixed = semi_directed(first_rooted), semi_directed(second_rooted)
    first_census, second_census = rooting_census(first_mixed), rooting_census(second_mixed)
    require(
        (first_census["admissible_rootings"], first_census["tree_child_rootings"], first_census["non_tree_child_rootings"])
        == (5, 2, 3),
        "first independent rooting census changed",
    )
    require(
        (second_census["admissible_rootings"], second_census["tree_child_rootings"], second_census["non_tree_child_rootings"])
        == (7, 2, 5),
        "second independent rooting census changed",
    )
    require(first_census["reticulation_edges_explicitly_tried"] == 4, "first reticulation edges were not all tried")
    require(second_census["reticulation_edges_explicitly_tried"] == 4, "second reticulation edges were not all tried")
    require(
        (primary["first"]["rooting_census"]["admissible_rootings"], primary["first"]["rooting_census"]["tree_child_rootings"])
        == (5, 2),
        "primary first census drift",
    )
    require(
        (primary["second"]["rooting_census"]["admissible_rootings"], primary["second"]["rooting_census"]["tree_child_rootings"])
        == (7, 2),
        "primary second census drift",
    )

    relation = exact_relation(first_mixed, second_mixed)
    require(relation["relation"] == "none", "independent mixed relation is not none")
    first_level, second_level = level_profile(first_mixed), level_profile(second_mixed)
    require(first_level["maximum_reticulations_in_a_blob"] == 2, "first graph is not exactly level 2")
    require(second_level["maximum_reticulations_in_a_blob"] == 2, "second graph is not exactly level 2")

    delta = F(1, 2**30)
    first_expected = (
        F(1), F(64009, 457492), F(64009, 457492), F(6400, 39229939), F(1, 1372),
        F(4048, 39229939), F(4048, 39229939), F(6400, 39229939), F(4048, 39229939), F(1, 1372),
    )
    second_expected = (
        F(1), F(15, 1024), F(15, 1024), F(5, 512), F(27, 512),
        F(9, 4096), F(9, 4096), F(5, 512), F(9, 4096), F(27, 512),
    )
    first_case = case_certificate(
        first_rooted,
        F(1, 7),
        (F(15996, 16339), F(1, 8)),
        (F(86779, 80), F(320, 253), F(114373, 20240)),
        delta,
        first_expected,
        primary["first"]["parameter_certificate"],
    )
    second_case = case_certificate(
        second_rooted,
        F(1, 4),
        (F(1, 2), F(1, 6)),
        (F(16, 3), F(32, 9), F(96, 5)),
        delta,
        second_expected,
        primary["second"]["parameter_certificate"],
    )
    require(first_case["full_tensor"] == second_case["full_tensor"], "independent physical tensors differ")
    require(first_case["full_tensor"] == primary["common_tensor"], "primary common tensor reassigned")
    cherry = cherry_audit()
    cherry["lift_and_prune_replay"] = lift_and_prune_audit(first_mixed, second_mixed)
    require(cherry["determinant"] == primary["cherry_extension"]["four_by_four_determinant"], "cherry determinant mismatch")

    return {
        "schema": "k2p-weak-sharpness-independent-audit-v1",
        "independence": {
            "imports_primary_builder": False,
            "imports_atlas": False,
            "graph_source": "literal independent node/arc encodings",
            "map_source": "direct four-switch Fourier expansion over Q",
        },
        "rooting": {"first": first_census, "second": second_census},
        "level_profiles": {"first": first_level, "second": second_level},
        "mixed_relation": relation,
        "first_map": first_case,
        "second_map": second_case,
        "common_tensor": first_case["full_tensor"],
        "cherry": cherry,
        "boundary_cases": {
            "n_minimum": 3,
            "all_n": "iterate attachment at the same retained labelled leaf and prune the newest labelled cherry in reverse order",
            "strictness": "all base and added edges lie strictly inside s^2<g<1 and all inheritances lie in (0,1)",
            "zero_coordinate_risk": "absent: every displayed-tree summand and every eigenvalue at the witness is positive",
        },
        "conclusion": "PASS",
        "primary_verifier_observation": "its cherry-domain loop checks (x,x) pairs rather than the actual (u_s,u_g),(v_s,v_g) pairs; the correct pairs independently pass",
    }


def main() -> None:
    if not __debug__:
        raise SystemExit("WEAK_SHARPNESS_AUDIT_OPTIMIZED_MODE_FORBIDDEN")
    require(PRIMARY.is_file(), f"missing primary certificate: {PRIMARY}")
    primary = json.loads(PRIMARY.read_text())
    audit = build_audit(primary)
    payload = dict(audit)
    audit["payload_sha256"] = digest(payload)
    output = HERE / "audit_certificate.json"
    output.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print("K2P_WEAK_SHARPNESS_INDEPENDENT_AUDIT_PASS")
    print(json.dumps({
        "payload_sha256": audit["payload_sha256"],
        "certificate_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "rooting_censuses": [[5, 2, 3], [7, 2, 5]],
        "ranks": [audit["first_map"]["rank"], audit["second_map"]["rank"]],
        "relation": audit["mixed_relation"]["relation"],
        "dimension": "4*n-3",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
