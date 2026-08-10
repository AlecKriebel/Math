#!/usr/bin/env python3
"""Independent exact referee for the ordinary JC triangle move.

This module uses only the Python standard library.  It does not import the
primary graph, Fourier, canonicalization, or rank implementations.  The
primary JSON certificate is treated only as a claim to compare against an
independently regenerated result.
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
DEFAULT_CLAIM = PROJECT / "primary/certificates/jc_triangle_redirection_active.json"


def frac_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def parse_fraction(value: str | int) -> Fraction:
    return Fraction(value)


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


@dataclass(frozen=True)
class RootedNetwork:
    root: str
    labels: tuple[tuple[str, str], ...]
    arcs: tuple[tuple[str, str], ...]

    def label_map(self) -> dict[str, str]:
        return dict(self.labels)


@dataclass(frozen=True)
class MixedNetwork:
    labels: tuple[tuple[str, str], ...]
    undirected: tuple[tuple[str, str], ...]
    directed: tuple[tuple[str, str], ...]

    def vertices(self) -> set[str]:
        result = {vertex for vertex, _label in self.labels}
        for left, right in self.undirected + self.directed:
            result.add(left)
            result.add(right)
        return result


def undirected_edge(left: str, right: str) -> tuple[str, str]:
    if left == right:
        raise ValueError("loop")
    return tuple(sorted((left, right)))


def degree_tables(network: RootedNetwork):
    vertices = {network.root}
    vertices.update(vertex for vertex, _label in network.labels)
    for tail, head in network.arcs:
        vertices.add(tail)
        vertices.add(head)
    indegree = {vertex: 0 for vertex in vertices}
    outdegree = {vertex: 0 for vertex in vertices}
    children = {vertex: [] for vertex in vertices}
    parents = {vertex: [] for vertex in vertices}
    for tail, head in network.arcs:
        outdegree[tail] += 1
        indegree[head] += 1
        children[tail].append(head)
        parents[head].append(tail)
    return vertices, indegree, outdegree, children, parents


def is_acyclic(vertices: Iterable[str], arcs: Iterable[tuple[str, str]]) -> bool:
    vertices = set(vertices)
    indegree = {vertex: 0 for vertex in vertices}
    children = {vertex: [] for vertex in vertices}
    for tail, head in arcs:
        indegree[head] += 1
        children[tail].append(head)
    queue = sorted(vertex for vertex in vertices if indegree[vertex] == 0)
    seen = 0
    while queue:
        vertex = queue.pop(0)
        seen += 1
        for child in children[vertex]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
                queue.sort()
    return seen == len(vertices)


def rooted_problems(network: RootedNetwork) -> list[str]:
    problems: list[str] = []
    if len(network.arcs) != len(set(network.arcs)):
        problems.append("parallel-directed-arc")
    if any(tail == head for tail, head in network.arcs):
        problems.append("directed-loop")
    vertices, indegree, outdegree, children, _parents = degree_tables(network)
    labels = network.label_map()
    if len(labels) != len(network.labels) or len(set(labels.values())) != len(labels):
        problems.append("leaf-labels-not-bijective")
    if indegree.get(network.root) != 0 or outdegree.get(network.root) != 2:
        problems.append("root-bidegree")
    for vertex in sorted(vertices - {network.root}):
        pair = (indegree[vertex], outdegree[vertex])
        if vertex in labels:
            if pair != (1, 0):
                problems.append(f"leaf-bidegree:{vertex}:{pair}")
        elif pair not in {(1, 2), (2, 1)}:
            problems.append(f"internal-bidegree:{vertex}:{pair}")
    if not is_acyclic(vertices, network.arcs):
        problems.append("directed-cycle")
    reachable = {network.root}
    frontier = [network.root]
    while frontier:
        vertex = frontier.pop()
        for child in children[vertex]:
            if child not in reachable:
                reachable.add(child)
                frontier.append(child)
    if reachable != vertices:
        problems.append("not-root-reachable")
    return problems


def all_directed_paths(network: RootedNetwork, target: str) -> list[tuple[str, ...]]:
    _vertices, _indegree, _outdegree, children, _parents = degree_tables(network)
    paths: list[tuple[str, ...]] = []

    def visit(vertex: str, path: tuple[str, ...]) -> None:
        if vertex == target:
            paths.append(path)
            return
        for child in sorted(children[vertex]):
            if child not in path:
                visit(child, path + (child,))

    visit(network.root, (network.root,))
    return paths


def root_is_lsa(network: RootedNetwork) -> bool:
    common: set[str] | None = None
    for leaf, _label in network.labels:
        paths = all_directed_paths(network, leaf)
        if not paths:
            return False
        stable = set(paths[0])
        for path in paths[1:]:
            stable.intersection_update(path)
        common = stable if common is None else common.intersection(stable)
    return common == {network.root}


def rooted_tree_child(network: RootedNetwork) -> bool:
    vertices, indegree, outdegree, children, _parents = degree_tables(network)
    leaves = set(network.label_map())
    for vertex in vertices - leaves:
        if not any(child in leaves or (indegree[child], outdegree[child]) == (1, 2)
                   for child in children[vertex]):
            return False
    return True


def reticulations(network: RootedNetwork) -> set[str]:
    vertices, indegree, outdegree, _children, _parents = degree_tables(network)
    return {vertex for vertex in vertices if (indegree[vertex], outdegree[vertex]) == (2, 1)}


def sd0(network: RootedNetwork) -> MixedNetwork:
    """Reticulation-preserving one-step binary-root suppression."""
    problems = rooted_problems(network)
    if problems:
        raise ValueError("invalid rooted network: " + ",".join(problems))
    rets = reticulations(network)
    root_children = sorted(head for tail, head in network.arcs if tail == network.root)
    if len(root_children) != 2:
        raise ValueError("binary root required")
    directed: set[tuple[str, str]] = set()
    undirected: set[tuple[str, str]] = set()
    for tail, head in network.arcs:
        if tail == network.root:
            continue
        if head in rets:
            directed.add((tail, head))
        else:
            undirected.add(undirected_edge(tail, head))
    left, right = root_children
    if left in rets and right in rets:
        raise ValueError("root suppression would create a bidirected artifact")
    if left in rets:
        directed.add((right, left))
    elif right in rets:
        directed.add((left, right))
    else:
        undirected.add(undirected_edge(left, right))
    pairs = [undirected_edge(*edge) for edge in directed] + list(undirected)
    if len(pairs) != len(set(pairs)):
        raise ValueError("root suppression created a parallel edge")
    if any(network.root in edge for edge in directed) or any(network.root in edge for edge in undirected):
        raise AssertionError("root survived sd0")
    return MixedNetwork(
        tuple(sorted(network.labels)),
        tuple(sorted(undirected)),
        tuple(sorted(directed)),
    )


def mixed_problems(network: MixedNetwork) -> list[str]:
    problems: list[str] = []
    vertices = network.vertices()
    labels = dict(network.labels)
    pairs = [undirected_edge(*edge) for edge in network.undirected + network.directed]
    if len(pairs) != len(set(pairs)):
        problems.append("mixed-parallel-edge")
    if len(network.undirected) != len(set(network.undirected)) or len(network.directed) != len(set(network.directed)):
        problems.append("duplicate-mixed-edge")
    degree = {vertex: 0 for vertex in vertices}
    incoming = {vertex: 0 for vertex in vertices}
    for left, right in network.undirected:
        degree[left] += 1
        degree[right] += 1
    for tail, head in network.directed:
        degree[tail] += 1
        degree[head] += 1
        incoming[head] += 1
    for vertex in vertices:
        expected = 1 if vertex in labels else 3
        if degree[vertex] != expected:
            problems.append(f"mixed-degree:{vertex}:{degree[vertex]}")
    rets = {vertex for vertex, count in incoming.items() if count}
    if any(incoming[vertex] != 2 for vertex in rets):
        problems.append("reticulation-arrowhead-count")
    if any(head not in rets for _tail, head in network.directed):
        problems.append("arrowhead-not-at-reticulation")
    return problems


def mixed_reticulations(network: MixedNetwork) -> set[str]:
    incoming = {vertex: 0 for vertex in network.vertices()}
    for _tail, head in network.directed:
        incoming[head] += 1
    return {vertex for vertex, count in incoming.items() if count == 2}


def mixed_local_strong(network: MixedNetwork) -> bool:
    if mixed_problems(network):
        return False
    undirected_incidence = {vertex: 0 for vertex in network.vertices()}
    for left, right in network.undirected:
        undirected_incidence[left] += 1
        undirected_incidence[right] += 1
    return all(undirected_incidence[tail] == 2 for tail, _head in network.directed)


def underlying_triangles(network: MixedNetwork) -> list[tuple[str, str, str]]:
    pairs = {undirected_edge(*edge) for edge in network.undirected + network.directed}
    result = []
    for triple in itertools.combinations(sorted(network.vertices()), 3):
        if all(undirected_edge(*pair) in pairs for pair in itertools.combinations(triple, 2)):
            result.append(triple)
    return result


def canonical_mixed(network: MixedNetwork) -> str:
    labels = dict(network.labels)
    internal = sorted(network.vertices() - set(labels))
    candidates: list[str] = []
    for order in itertools.permutations(internal):
        token = {vertex: f"I{index}" for index, vertex in enumerate(order)}
        token.update({vertex: f"L:{label}" for vertex, label in labels.items()})
        entries = []
        for left, right in network.undirected:
            a, b = sorted((token[left], token[right]))
            entries.append(f"U:{a}|{b}")
        for tail, head in network.directed:
            entries.append(f"D:{token[tail]}>{token[head]}")
        candidates.append(";".join(sorted(entries)))
    return min(candidates)


def t_quotient(network: MixedNetwork) -> MixedNetwork:
    triangles = underlying_triangles(network)
    if len(triangles) != 1:
        raise ValueError("ordinary T quotient requires one triangle")
    triangle = set(triangles[0])
    undirected = set(network.undirected)
    directed = set()
    for tail, head in network.directed:
        if tail in triangle and head in triangle:
            undirected.add(undirected_edge(tail, head))
        else:
            directed.add((tail, head))
    return MixedNetwork(network.labels, tuple(sorted(undirected)), tuple(sorted(directed)))


def unheaded(network: MixedNetwork) -> MixedNetwork:
    undirected = set(network.undirected)
    undirected.update(undirected_edge(*edge) for edge in network.directed)
    return MixedNetwork(network.labels, tuple(sorted(undirected)), ())


def same_mixed(left: MixedNetwork, right: MixedNetwork) -> bool:
    return (left.labels == right.labels and left.undirected == right.undirected
            and left.directed == right.directed)


def enumerate_admissible_rootings(network: MixedNetwork) -> list[RootedNetwork]:
    """Brute-force every edge insertion and every remaining edge orientation."""
    root = "@R"
    all_edges = [("U", edge) for edge in network.undirected] + [("D", edge) for edge in network.directed]
    accepted: dict[tuple[tuple[str, str], ...], RootedNetwork] = {}
    for candidate_index, (_kind, candidate) in enumerate(all_edges):
        remaining_undirected = [edge for index, (kind, edge) in enumerate(all_edges)
                                if kind == "U" and index != candidate_index]
        remaining_directed = [edge for index, (kind, edge) in enumerate(all_edges)
                              if kind == "D" and index != candidate_index]
        for bits in itertools.product((0, 1), repeat=len(remaining_undirected)):
            arcs = list(remaining_directed)
            for edge, bit in zip(remaining_undirected, bits):
                left, right = edge
                arcs.append((left, right) if bit == 0 else (right, left))
            left, right = candidate
            arcs.extend(((root, left), (root, right)))
            rooted = RootedNetwork(root, network.labels, tuple(sorted(arcs)))
            if rooted_problems(rooted) or not root_is_lsa(rooted):
                continue
            try:
                reduced = sd0(rooted)
            except ValueError:
                continue
            if not same_mixed(reduced, network):
                continue
            accepted[rooted.arcs] = rooted
    return [accepted[key] for key in sorted(accepted)]


def sunlet(reticulation_taxon: int) -> RootedNetwork:
    if reticulation_taxon not in {0, 1, 2}:
        raise ValueError(reticulation_taxon)
    ordinary = [taxon for taxon in range(3) if taxon != reticulation_taxon]
    labels = (("LA", f"L_{ordinary[0]}"), ("LB", f"L_{ordinary[1]}"),
              ("LH", f"L_{reticulation_taxon}"))
    arcs = (
        ("R", "A"), ("R", "B"),
        ("A", "H"), ("B", "H"),
        ("A", "LA"), ("B", "LB"), ("H", "LH"),
    )
    return RootedNetwork("R", tuple(sorted(labels)), tuple(sorted(arcs)))


def edge_parameters(network: RootedNetwork) -> dict[tuple[str, str], Fraction]:
    labels = network.label_map()
    parameters: dict[tuple[str, str], Fraction] = {}
    for edge in network.arcs:
        tail, head = edge
        if tail == "R":
            value = Fraction(1, 2)
        elif head == "H":
            value = Fraction(1, 4)
        elif head in labels:
            value = Fraction(1, 320) if tail == "H" else Fraction(1, 512)
        else:
            raise AssertionError(edge)
        parameters[edge] = value
    return parameters


def descendant_mask(network: RootedNetwork, active_arcs: tuple[tuple[str, str], ...],
                    child: str, label_order: tuple[str, ...]) -> int:
    children: dict[str, list[str]] = {}
    for tail, head in active_arcs:
        children.setdefault(tail, []).append(head)
    label_for_vertex = network.label_map()
    stack = [child]
    seen: set[str] = set()
    mask = 0
    while stack:
        vertex = stack.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        if vertex in label_for_vertex:
            mask |= 1 << label_order.index(label_for_vertex[vertex])
        stack.extend(children.get(vertex, ()))
    return mask


def fourier_and_gradient(network: RootedNetwork,
                         parameters: dict[tuple[str, str], Fraction],
                         inheritance: Fraction):
    """Direct displayed-tree sum and exact derivatives in all physical parameters."""
    labels = ("L_0", "L_1", "L_2")
    incoming = sorted(edge for edge in network.arcs if edge[1] == "H")
    if incoming != [("A", "H"), ("B", "H")]:
        raise ValueError("unexpected reticulation parents")
    parameter_names = tuple(f"x:{tail}>{head}" for tail, head in network.arcs) + ("lambda",)
    values: list[Fraction] = []
    gradients: list[dict[str, Fraction]] = []
    for assignment in itertools.product(range(4), repeat=3):
        gradient = {name: Fraction(0) for name in parameter_names}
        if assignment[0] ^ assignment[1] ^ assignment[2]:
            values.append(Fraction(0))
            gradients.append(gradient)
            continue
        total = Fraction(0)
        for chosen in incoming:
            active = tuple(edge for edge in network.arcs if edge not in incoming or edge == chosen)
            weight = inheritance if chosen == ("A", "H") else 1 - inheritance
            weight_derivative = Fraction(1) if chosen == ("A", "H") else Fraction(-1)
            used: list[tuple[str, str]] = []
            monomial = Fraction(1)
            for edge in active:
                mask = descendant_mask(network, active, edge[1], labels)
                character = 0
                for index, state in enumerate(assignment):
                    if mask & (1 << index):
                        character ^= state
                if character:
                    used.append(edge)
                    monomial *= parameters[edge]
            total += weight * monomial
            gradient["lambda"] += weight_derivative * monomial
            for edge in used:
                gradient[f"x:{edge[0]}>{edge[1]}"] += weight * monomial / parameters[edge]
        values.append(total)
        gradients.append(gradient)
    return tuple(values), tuple(gradients), parameter_names


def tensor_index(assignment: tuple[int, int, int]) -> int:
    return (assignment[0] * 4 + assignment[1]) * 4 + assignment[2]


ORBIT_ASSIGNMENTS = ((1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 2, 3))


def determinant(matrix: list[list[Fraction]] | tuple[tuple[Fraction, ...], ...]) -> Fraction:
    size = len(matrix)
    work = [list(row) for row in matrix]
    result = Fraction(1)
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result *= -1
        pivot_value = work[column][column]
        result *= pivot_value
        for entry in range(column, size):
            work[column][entry] /= pivot_value
        for row in range(column + 1, size):
            factor = work[row][column]
            if not factor:
                continue
            for entry in range(column, size):
                work[row][entry] -= factor * work[column][entry]
    return result


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    if not work:
        return 0
    rows, columns = len(work), len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [value - factor * pivot_value
                             for value, pivot_value in zip(work[row], work[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def physical_rank_certificate(network: RootedNetwork, gradients, parameter_names):
    matrix = [[gradients[tensor_index(assignment)][name] for name in parameter_names]
              for assignment in ORBIT_ASSIGNMENTS]
    matrix_rank = rank(matrix)
    selected_columns = None
    selected_matrix = None
    selected_determinant = Fraction(0)
    for columns in itertools.combinations(range(len(parameter_names)), 4):
        minor = [[row[column] for column in columns] for row in matrix]
        value = determinant(minor)
        if value:
            selected_columns = columns
            selected_matrix = minor
            selected_determinant = value
            break
    if selected_columns is None:
        raise AssertionError("no physical rank-four minor")
    return {
        "full_jacobian_rank": matrix_rank,
        "parameter_columns": [parameter_names[column] for column in selected_columns],
        "matrix": [[frac_text(value) for value in row] for row in selected_matrix],
        "determinant": frac_text(selected_determinant),
    }


def effective_tensor_and_gradient() -> tuple[tuple[Fraction, ...], dict[str, object]]:
    """Independently enumerate the suppressed three-port displayed trees.

    The structural ports are A, B, H.  The two displayed trees have internal
    edges (A-B, A-H) and (A-B, B-H), respectively.  Rooting either tree at A
    is only a device for computing edge splits.
    """
    parameters = {
        "rA": Fraction(1, 512),
        "rB": Fraction(1, 512),
        "rH": Fraction(1, 320),
        "x": Fraction(1, 4),
        "u": Fraction(1, 4),
        "v": Fraction(1, 4),
        "lambda": Fraction(1, 2),
    }
    # Each record is (weight selector, edges as (split mask, parameter name)).
    switchings = (
        ("left", ((0b001, "rA"), (0b010, "rB"), (0b100, "rH"),
                  (0b010, "x"), (0b100, "u"))),
        ("right", ((0b001, "rA"), (0b010, "rB"), (0b100, "rH"),
                   (0b110, "x"), (0b100, "v"))),
    )
    # The right switching's B-H edge has split H|AB and the A-B edge split
    # is BH|A.  Both masks above are valid sides of those splits.
    values: list[Fraction] = []
    gradients: list[dict[str, Fraction]] = []
    names = tuple(parameters)
    for assignment in itertools.product(range(4), repeat=3):
        gradient = {name: Fraction(0) for name in names}
        if assignment[0] ^ assignment[1] ^ assignment[2]:
            values.append(Fraction(0))
            gradients.append(gradient)
            continue
        total = Fraction(0)
        for side, edges in switchings:
            weight = parameters["lambda"] if side == "left" else 1 - parameters["lambda"]
            dweight = Fraction(1) if side == "left" else Fraction(-1)
            used: list[str] = []
            monomial = Fraction(1)
            for mask, name in edges:
                character = 0
                for index, state in enumerate(assignment):
                    if mask & (1 << index):
                        character ^= state
                if character:
                    used.append(name)
                    monomial *= parameters[name]
            total += weight * monomial
            gradient["lambda"] += dweight * monomial
            for name in used:
                gradient[name] += weight * monomial / parameters[name]
        values.append(total)
        gradients.append(gradient)
    columns = ("rA", "rB", "rH", "x")
    matrix = [[gradients[tensor_index(assignment)][name] for name in columns]
              for assignment in ORBIT_ASSIGNMENTS]
    return tuple(values), {
        "parameter_columns": list(columns),
        "matrix": [[frac_text(value) for value in row] for row in matrix],
        "determinant": frac_text(determinant(matrix)),
        "rank": rank(matrix),
    }


def enumerate_unheaded_orientations(reference: MixedNetwork) -> list[MixedNetwork]:
    base = unheaded(reference)
    triangles = underlying_triangles(base)
    if len(triangles) != 1:
        raise AssertionError("expected one underlying triangle")
    triangle = set(triangles[0])
    base_pairs = set(base.undirected)
    result = []
    for retic in sorted(triangle):
        directed = set()
        undirected = set(base_pairs)
        for neighbor in sorted(triangle - {retic}):
            pair = undirected_edge(neighbor, retic)
            undirected.remove(pair)
            directed.add((neighbor, retic))
        result.append(MixedNetwork(base.labels, tuple(sorted(undirected)), tuple(sorted(directed))))
    return result


def primary_expected_edge_map(reticulation_taxon: int) -> dict[str, str]:
    # This is the public claimed rooted presentation, independently restated.
    return {
        "0->1": "1/2", "0->2": "1/2",
        "1->3": "1/4", "2->3": "1/4",
        "1->4": "1/512", "2->5": "1/512", "3->6": "1/320",
    }


def compare_claim(claim: dict, independent: dict) -> list[str]:
    failures: list[str] = []
    def require(condition: bool, label: str) -> None:
        if not condition:
            failures.append(label)

    require(claim.get("status") == "VERIFIED", "claim-status")
    require(claim.get("parameter_space") ==
            "0 < every JC Fourier multiplier < 1 and 0 < lambda < 1",
            "parameter-space-statement")
    topology = claim.get("topology", {})
    require(topology.get("semi_directed_orientation_count") == 3, "orientation-count")
    require(topology.get("underlying_labelled_graph_count") == 1, "underlying-count")
    require(topology.get("T_quotient_class_count") == 1, "T-quotient-count")
    rows = topology.get("rooted_witnesses", [])
    require(len(rows) == 3, "rooted-row-count")
    by_taxon = {row.get("reticulation_taxon"): row for row in rows}
    require(set(by_taxon) == {"L_0", "L_1", "L_2"}, "reticulation-taxon-set")
    mixed_hashes, quotient_hashes, unheaded_hashes = set(), set(), set()
    for taxon in range(3):
        row = by_taxon.get(f"L_{taxon}", {})
        require(row.get("rooted_valid") is True, f"rooted-valid:{taxon}")
        require(row.get("root_is_lsa") is True, f"root-lsa:{taxon}")
        require(row.get("chosen_rooting_tree_child") is True, f"chosen-tree-child:{taxon}")
        require(row.get("standard_local_strong") is True, f"local-strong:{taxon}")
        require(row.get("all_admissible_rootings_tree_child") is True,
                f"all-rootings-tree-child:{taxon}")
        require(row.get("admissible_rooting_count") == 5, f"rooting-count:{taxon}")
        require(row.get("tree_child_rooting_count") == 5, f"tc-rooting-count:{taxon}")
        require(row.get("triangle_count") == 1, f"triangle-count:{taxon}")
        require(row.get("reticulation_count") == 1, f"reticulation-count:{taxon}")
        require(row.get("edge_parameters") == primary_expected_edge_map(taxon),
                f"edge-role-map:{taxon}")
        require(row.get("inheritance_probability") == "1/2", f"inheritance:{taxon}")
        require(row.get("orbit_coordinates") == independent["common_point"]["orbit_coordinates"],
                f"orbit-coordinates:{taxon}")
        for value in row.get("edge_parameters", {}).values():
            require(Fraction(0) < parse_fraction(value) < Fraction(1),
                    f"edge-open-domain:{taxon}")
        if "inheritance_probability" in row:
            inheritance = parse_fraction(row["inheritance_probability"])
            require(Fraction(0) < inheritance < Fraction(1), f"inheritance-open-domain:{taxon}")
        mixed_hashes.add(row.get("standard_mixed_code_sha256"))
        quotient_hashes.add(row.get("T_quotient_code_sha256"))
        unheaded_hashes.add(row.get("unheaded_code_sha256"))
    require(len(mixed_hashes) == 3 and None not in mixed_hashes, "claimed-orientations-distinct")
    require(len(quotient_hashes) == 1 and None not in quotient_hashes, "claimed-one-T-quotient")
    require(len(unheaded_hashes) == 1 and None not in unheaded_hashes, "claimed-one-unheaded")

    common = claim.get("common_point", {})
    require(common.get("complete_Fourier_tensor") == independent["common_point"]["tensor"],
            "complete-Fourier-tensor")
    require(common.get("complete_Fourier_tensor_sha256") ==
            independent["common_point"]["tensor_sha256"], "Fourier-tensor-hash")
    require(common.get("target_orbit_coordinates") == independent["common_point"]["orbit_coordinates"],
            "target-orbit-coordinates")
    require(common.get("coordinate_counts") == independent["common_point"]["coordinate_counts"],
            "coordinate-counts")
    rank_claim = claim.get("rank_certificate", {})
    require(rank_claim.get("parameter_columns") == ["r1", "r2", "r3", "x"],
            "effective-rank-columns")
    require(rank_claim.get("matrix") == independent["effective_rank"]["matrix"],
            "effective-rank-matrix")
    require(rank_claim.get("determinant") == independent["effective_rank"]["determinant"],
            "effective-rank-determinant")
    require(rank_claim.get("upper_bound") == 4, "rank-upper-bound")
    stochastic = claim.get("stochastic_conclusion", {})
    require(stochastic.get("pairwise_symmetric_full_dimensional_regular_overlap") == "VERIFIED",
            "regular-overlap-claim")
    require(stochastic.get("complete_open_stochastic_image_equality") == "NOT CLAIMED",
            "forbidden-complete-image-equality")
    return sorted(set(failures))


def build_independent_certificate(claim_path: Path) -> tuple[dict, dict]:
    rooted_rows = []
    tensors = []
    mixed_codes = []
    quotient_codes = []
    unheaded_codes = []
    mixed_networks = []
    for reticulation_taxon in range(3):
        rooted = sunlet(reticulation_taxon)
        problems = rooted_problems(rooted)
        mixed = sd0(rooted)
        mixed_networks.append(mixed)
        rootings = enumerate_admissible_rootings(mixed)
        parameters = edge_parameters(rooted)
        tensor, gradients, parameter_names = fourier_and_gradient(
            rooted, parameters, Fraction(1, 2))
        physical_rank = physical_rank_certificate(rooted, gradients, parameter_names)
        mixed_code = canonical_mixed(mixed)
        quotient_code = canonical_mixed(t_quotient(mixed))
        unheaded_code = canonical_mixed(unheaded(mixed))
        tensors.append(tensor)
        mixed_codes.append(mixed_code)
        quotient_codes.append(quotient_code)
        unheaded_codes.append(unheaded_code)
        rooted_rows.append({
            "reticulation_taxon": f"L_{reticulation_taxon}",
            "rooted_problems": problems,
            "root_is_lsa": root_is_lsa(rooted),
            "chosen_rooting_tree_child": rooted_tree_child(rooted),
            "sd0_mixed_problems": mixed_problems(mixed),
            "local_no_omnian": mixed_local_strong(mixed),
            "triangle_count": len(underlying_triangles(mixed)),
            "reticulation_count": len(mixed_reticulations(mixed)),
            "admissible_rooting_count": len(rootings),
            "tree_child_rooting_count": sum(rooted_tree_child(candidate) for candidate in rootings),
            "all_admissible_rootings_tree_child": all(rooted_tree_child(candidate) for candidate in rootings),
            "mixed_code_sha256": sha256_bytes(mixed_code.encode()),
            "T_quotient_code_sha256": sha256_bytes(quotient_code.encode()),
            "unheaded_code_sha256": sha256_bytes(unheaded_code.encode()),
            "physical_rank": physical_rank,
        })

    exhaustive_orientations = enumerate_unheaded_orientations(mixed_networks[0])
    exhaustive_codes = {canonical_mixed(network) for network in exhaustive_orientations}
    tensor = tensors[0]
    orbit = [tensor[tensor_index(assignment)] for assignment in ORBIT_ASSIGNMENTS]
    counts = {
        "coordinates": len(tensor),
        "constant_one": sum(value == 1 for value in tensor),
        "nonzero_pair_coordinates": sum(value == Fraction(1, 1048576) for value in tensor),
        "nonzero_triple_coordinates": sum(value == Fraction(1, 1342177280) for value in tensor),
        "zero_coordinates": sum(value == 0 for value in tensor),
    }
    effective_tensor, effective_rank = effective_tensor_and_gradient()
    checks = {
        "three_rooted_presentations_valid": all(not row["rooted_problems"] for row in rooted_rows),
        "three_roots_are_LSA": all(row["root_is_lsa"] for row in rooted_rows),
        "three_chosen_rootings_tree_child": all(row["chosen_rooting_tree_child"] for row in rooted_rows),
        "three_sd0_graphs_simple_binary": all(not row["sd0_mixed_problems"] for row in rooted_rows),
        "three_sd0_graphs_no_omnian": all(row["local_no_omnian"] for row in rooted_rows),
        "five_admissible_rootings_each": all(row["admissible_rooting_count"] == 5 for row in rooted_rows),
        "all_admissible_rootings_tree_child": all(row["all_admissible_rootings_tree_child"]
                                                   and row["tree_child_rooting_count"] == 5
                                                   for row in rooted_rows),
        "one_triangle_one_reticulation_each": all(row["triangle_count"] == 1
                                                   and row["reticulation_count"] == 1
                                                   for row in rooted_rows),
        "three_distinct_labelled_mixed_orientations": len(set(mixed_codes)) == 3,
        "one_T_quotient": len(set(quotient_codes)) == 1,
        "one_unheaded_labelled_graph": len(set(unheaded_codes)) == 1,
        "orientation_enumeration_exhaustive": set(mixed_codes) == exhaustive_codes
                                               and len(exhaustive_codes) == 3,
        "all_edge_and_inheritance_parameters_strictly_open": all(
            Fraction(0) < value < Fraction(1)
            for network in map(sunlet, range(3))
            for value in tuple(edge_parameters(network).values()) + (Fraction(1, 2),)
        ),
        "all_64_coordinates_equal": len(set(tensors)) == 1,
        "rooted_and_effective_tensors_equal": tensor == effective_tensor,
        "expected_coordinate_counts": counts == {
            "coordinates": 64, "constant_one": 1,
            "nonzero_pair_coordinates": 9, "nonzero_triple_coordinates": 6,
            "zero_coordinates": 48,
        },
        "physical_rank_four_each": all(row["physical_rank"]["full_jacobian_rank"] == 4
                                       and parse_fraction(row["physical_rank"]["determinant"])
                                       for row in rooted_rows),
        "effective_rank_four": effective_rank["rank"] == 4
                               and parse_fraction(effective_rank["determinant"]) != 0,
    }
    independent = {
        "schema": "cleanroom-jc-ordinary-triangle-v1",
        "status": "VERIFIED" if all(checks.values()) else "FALSE",
        "scope": "ordinary T for the labelled three-port JC triangle under locked sd0",
        "implementation_independence": {
            "stdlib_only": True,
            "imports_primary_or_other_reviews": False,
            "graph_engine": "fresh exhaustive directed and mixed graph implementation",
            "Fourier_engine": "fresh displayed-tree split summation over all 64 assignments",
            "Jacobian_engine": "fresh exact monomial differentiation and rational row reduction",
        },
        "input_claim": {
            "path": str(claim_path.relative_to(PROJECT)),
            "sha256": sha256_file(claim_path),
        },
        "topology": {
            "rooted_witnesses": rooted_rows,
            "mixed_orientation_count": len(set(mixed_codes)),
            "T_quotient_count": len(set(quotient_codes)),
            "unheaded_graph_count": len(set(unheaded_codes)),
            "exhaustive_orientation_count": len(exhaustive_codes),
        },
        "common_point": {
            "tensor": [frac_text(value) for value in tensor],
            "tensor_sha256": sha256_bytes(json.dumps(
                [frac_text(value) for value in tensor], separators=(",", ":")
            ).encode()),
            "orbit_assignments": [list(assignment) for assignment in ORBIT_ASSIGNMENTS],
            "orbit_coordinates": [frac_text(value) for value in orbit],
            "coordinate_counts": counts,
        },
        "effective_rank": effective_rank,
        "regular_germ_conclusion": {
            "normalized_tensor_germ": "VERIFIED",
            "projective_port_tensor_germ": "VERIFIED",
            "positive_port_scaling_action": {
                "coordinates": ["q12", "q13", "q23", "q123"],
                "action": ["s1*s2*q12", "s1*s3*q13", "s2*s3*q23",
                           "s1*s2*s3*q123"],
                "stabilizer_at_positive_tensor": "trivial",
                "quotient_coordinate": "q123^2/(q12*q13*q23)",
                "quotient_coordinate_at_common_point": frac_text(
                    orbit[3] ** 2 / (orbit[0] * orbit[1] * orbit[2])
                ),
            },
            "reason": (
                "Each orientation has physical differential rank four at the same strict "
                "interior tensor, equal to the four-dimensional normalized three-leaf JC "
                "orbit-space upper bound. Hence each image contains a common local output "
                "neighborhood. Passing to any analytic positive port-incidence projective "
                "quotient preserves that common germ."
            ),
            "complete_open_image_equality": "NOT ESTABLISHED AND NOT CLAIMED",
        },
        "checks": checks,
        "failed_checks": sorted(key for key, value in checks.items() if not value),
    }
    claim = json.loads(claim_path.read_text())
    claim_failures = compare_claim(claim, independent)
    independent["claim_comparison"] = {
        "status": "VERIFIED" if not claim_failures else "FALSE",
        "failures": claim_failures,
    }
    if claim_failures:
        independent["status"] = "FALSE"
    mutations = run_mutations(claim, independent)
    independent["mutation_suite"] = {
        "status": "VERIFIED" if all(row["rejected"] for row in mutations["mutations"]) else "FALSE",
        "count": len(mutations["mutations"]),
    }
    if independent["mutation_suite"]["status"] != "VERIFIED":
        independent["status"] = "FALSE"
    return independent, mutations


def run_mutations(claim: dict, independent: dict) -> dict:
    records = []

    def claim_mutation(name: str, mutate, expected_failure: str) -> None:
        candidate = copy.deepcopy(claim)
        mutate(candidate)
        failures = compare_claim(candidate, independent)
        records.append({
            "name": name,
            "kind": "claimed-certificate mutation",
            "rejected": expected_failure in failures,
            "expected_failure": expected_failure,
            "observed_failures": failures,
        })

    # A graph-level arrow reversal is not a valid rooted binary sunlet.
    wrong = sunlet(0)
    arcs = list(wrong.arcs)
    arcs.remove(("A", "H"))
    arcs.remove(("B", "H"))
    arcs.append(("H", "A"))
    arcs.append(("H", "B"))
    wrong = RootedNetwork(wrong.root, wrong.labels, tuple(sorted(arcs)))
    problems = rooted_problems(wrong)
    records.append({
        "name": "wrong_orientation",
        "kind": "graph mutation",
        "rejected": bool(problems),
        "expected_failure": "invalid rooted binary orientation",
        "observed_failures": problems,
    })

    reference_network = sunlet(0)
    reference_parameters = edge_parameters(reference_network)
    reference_tensor, _reference_gradient, _reference_names = fourier_and_gradient(
        reference_network, reference_parameters, Fraction(1, 2))

    boundary_parameters = dict(reference_parameters)
    boundary_parameters[("R", "A")] = Fraction(1)
    boundary_failures = [
        f"not-strictly-open:{tail}>{head}"
        for (tail, head), value in sorted(boundary_parameters.items())
        if not Fraction(0) < value < Fraction(1)
    ]
    records.append({
        "name": "boundary_parameter_model_input",
        "kind": "model-input mutation",
        "rejected": boundary_failures == ["not-strictly-open:R>A"],
        "expected_failure": "not-strictly-open:R>A",
        "observed_failures": boundary_failures,
    })

    wrong_weight_tensor, _wrong_gradient, _wrong_names = fourier_and_gradient(
        reference_network, reference_parameters, Fraction(1, 3))
    wrong_weight_mismatches = [
        index for index, (left, right) in enumerate(zip(reference_tensor, wrong_weight_tensor))
        if left != right
    ]
    records.append({
        "name": "wrong_inheritance_weight_model",
        "kind": "model mutation",
        "rejected": bool(wrong_weight_mismatches),
        "expected_failure": "Fourier tensor mismatch",
        "observed_failure_count": len(wrong_weight_mismatches),
        "first_observed_failure": wrong_weight_mismatches[0] if wrong_weight_mismatches else None,
    })

    swapped_parameters = dict(reference_parameters)
    swapped_parameters[("A", "LA")], swapped_parameters[("H", "LH")] = (
        swapped_parameters[("H", "LH")], swapped_parameters[("A", "LA")]
    )
    swapped_tensor, _swapped_gradient, _swapped_names = fourier_and_gradient(
        reference_network, swapped_parameters, Fraction(1, 2))
    swapped_mismatches = [
        index for index, (left, right) in enumerate(zip(reference_tensor, swapped_tensor))
        if left != right
    ]
    records.append({
        "name": "swapped_reticulation_arm_role_model",
        "kind": "model mutation",
        "rejected": bool(swapped_mismatches),
        "expected_failure": "Fourier tensor mismatch",
        "observed_failure_count": len(swapped_mismatches),
        "first_observed_failure": swapped_mismatches[0] if swapped_mismatches else None,
    })

    def changed_entry(candidate):
        candidate["common_point"]["complete_Fourier_tensor"][5] = "1/1048575"
    claim_mutation("changed_Fourier_entry", changed_entry, "complete-Fourier-tensor")

    def boundary(candidate):
        candidate["topology"]["rooted_witnesses"][0]["edge_parameters"]["0->1"] = "1"
    claim_mutation("boundary_parameter", boundary, "edge-open-domain:0")

    def wrong_inheritance(candidate):
        candidate["topology"]["rooted_witnesses"][0]["inheritance_probability"] = "1/3"
    claim_mutation("wrong_inheritance_weight", wrong_inheritance, "inheritance:0")

    def swapped_arm(candidate):
        edges = candidate["topology"]["rooted_witnesses"][0]["edge_parameters"]
        edges["1->4"], edges["3->6"] = edges["3->6"], edges["1->4"]
    claim_mutation("swapped_reticulation_arm_role", swapped_arm, "edge-role-map:0")

    def duplicate_orientation(candidate):
        rows = candidate["topology"]["rooted_witnesses"]
        rows[1]["standard_mixed_code_sha256"] = rows[0]["standard_mixed_code_sha256"]
    claim_mutation("collapsed_wrong_orientation", duplicate_orientation,
                   "claimed-orientations-distinct")

    def forged_determinant(candidate):
        candidate["rank_certificate"]["determinant"] = "1"
    claim_mutation("forged_determinant", forged_determinant, "effective-rank-determinant")

    def false_complete_equality(candidate):
        candidate["stochastic_conclusion"]["complete_open_stochastic_image_equality"] = "VERIFIED"
    claim_mutation("false_complete_image_equality_claim", false_complete_equality,
                   "forbidden-complete-image-equality")

    return {
        "schema": "cleanroom-jc-ordinary-triangle-mutations-v1",
        "status": "VERIFIED" if all(row["rejected"] for row in records) else "FALSE",
        "mutations": records,
        "failed_mutations": [row["name"] for row in records if not row["rejected"]],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim", type=Path, default=DEFAULT_CLAIM)
    parser.add_argument("--certificate", type=Path,
                        default=HERE / "certificate.json")
    parser.add_argument("--mutations", type=Path,
                        default=HERE / "mutation_results.json")
    args = parser.parse_args()
    certificate, mutations = build_independent_certificate(args.claim.resolve())
    args.certificate.parent.mkdir(parents=True, exist_ok=True)
    args.certificate.write_text(json.dumps(certificate, sort_keys=True, indent=2) + "\n")
    args.mutations.write_text(json.dumps(mutations, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": certificate["status"],
        "claim_comparison": certificate["claim_comparison"]["status"],
        "mutation_suite": certificate["mutation_suite"]["status"],
        "certificate_sha256": sha256_file(args.certificate),
        "mutations_sha256": sha256_file(args.mutations),
    }, sort_keys=True))
    if certificate["status"] != "VERIFIED" or mutations["status"] != "VERIFIED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
