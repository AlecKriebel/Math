#!/usr/bin/env python3
"""Independent graph and zero-sum JC engine for the final n=4 audit.

Only general-purpose libraries are imported.  No module under ``primary`` or
another review implementation is imported.
"""

from __future__ import annotations

import ast
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import lru_cache
import hashlib
from itertools import combinations, permutations, product
import json
import math
from pathlib import Path
from typing import Iterable

import networkx as nx


def stable_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def stable_hash(value) -> str:
    return hashlib.sha256(stable_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


@dataclass(frozen=True, order=True)
class MixedEdge:
    u: int
    v: int
    head_u: int = 0
    head_v: int = 0

    @staticmethod
    def make(u: int, v: int, heads: Iterable[int] = ()) -> "MixedEdge":
        heads = set(int(x) for x in heads)
        if u < v:
            return MixedEdge(int(u), int(v), int(u in heads), int(v in heads))
        return MixedEdge(int(v), int(u), int(v in heads), int(u in heads))

    def endpoints(self):
        return self.u, self.v

    def heads(self):
        return frozenset(v for v, bit in
                         ((self.u, self.head_u), (self.v, self.head_v)) if bit)

    def head_at(self, vertex: int) -> int:
        if vertex == self.u:
            return self.head_u
        if vertex == self.v:
            return self.head_v
        raise KeyError(vertex)

    def other(self, vertex: int) -> int:
        if vertex == self.u:
            return self.v
        if vertex == self.v:
            return self.u
        raise KeyError(vertex)


@dataclass(frozen=True)
class MixedGraph:
    labels: tuple[tuple[int, str], ...]
    edges: tuple[MixedEdge, ...]

    @property
    def label_map(self):
        return dict(self.labels)

    @property
    def vertices(self):
        answer = set(dict(self.labels))
        for edge in self.edges:
            answer.update(edge.endpoints())
        return tuple(sorted(answer))

    def incidence(self):
        answer = {v: [] for v in self.vertices}
        for edge in self.edges:
            answer[edge.u].append(edge)
            answer[edge.v].append(edge)
        return answer

    def reticulations(self):
        heads = Counter(v for edge in self.edges for v in edge.heads())
        return tuple(sorted(v for v, count in heads.items() if count == 2))


@dataclass(frozen=True)
class RootedGraph:
    root: int
    labels: tuple[tuple[int, str], ...]
    arcs: tuple[tuple[int, int], ...]

    @staticmethod
    def from_payload(payload: dict) -> "RootedGraph":
        return RootedGraph(
            int(payload["root"]),
            tuple(sorted((int(v), str(label)) for v, label in payload["labels"])),
            tuple(sorted((int(u), int(v)) for u, v in payload["arcs"])),
        )

    def payload(self) -> dict:
        return {"root": self.root, "labels": self.labels, "arcs": self.arcs}

    @property
    def label_map(self):
        return dict(self.labels)

    @property
    def vertices(self):
        answer = {self.root, *dict(self.labels)}
        for u, v in self.arcs:
            answer.add(u); answer.add(v)
        return tuple(sorted(answer))

    def degrees(self):
        indegree = {v: 0 for v in self.vertices}
        outdegree = {v: 0 for v in self.vertices}
        for u, v in self.arcs:
            outdegree[u] += 1; indegree[v] += 1
        return indegree, outdegree

    @property
    def graph_id(self):
        return stable_hash(self.payload())


def require(condition: bool, category: str, **details):
    if not condition:
        raise AssertionError(json.dumps({"category": category, **details}, sort_keys=True))


@lru_cache(maxsize=32768)
def validate_rooted(graph: RootedGraph) -> None:
    indegree, outdegree = graph.degrees()
    labels = graph.label_map
    require(len(graph.arcs) == len(set(graph.arcs)), "parallel_rooted_arc")
    require(len(labels) == len(set(labels.values())), "duplicate_label")
    require((indegree[graph.root], outdegree[graph.root]) == (0, 2),
            "root_bidegree")
    for vertex in graph.vertices:
        if vertex == graph.root:
            continue
        degree = indegree[vertex], outdegree[vertex]
        if vertex in labels:
            require(degree == (1, 0), "leaf_bidegree", vertex=vertex, degree=degree)
        else:
            require(degree in {(1, 2), (2, 1)}, "internal_bidegree",
                    vertex=vertex, degree=degree)
    children = defaultdict(list)
    for u, v in graph.arcs:
        children[u].append(v)
    work = dict(indegree)
    queue = deque(sorted(v for v in graph.vertices if work[v] == 0))
    order = []
    while queue:
        vertex = queue.popleft(); order.append(vertex)
        for child in children[vertex]:
            work[child] -= 1
            if work[child] == 0:
                queue.append(child)
    require(len(order) == len(graph.vertices), "directed_cycle")
    reached = {graph.root}; queue = deque([graph.root])
    while queue:
        vertex = queue.popleft()
        for child in children[vertex]:
            if child not in reached:
                reached.add(child); queue.append(child)
    require(reached == set(graph.vertices), "not_root_reachable")


@lru_cache(maxsize=32768)
def root_is_lsa(graph: RootedGraph) -> bool:
    labels = set(graph.label_map)
    children = defaultdict(list)
    for u, v in graph.arcs:
        children[u].append(v)
    for omitted in graph.vertices:
        if omitted == graph.root:
            continue
        reached = {graph.root}; queue = deque([graph.root])
        while queue:
            vertex = queue.popleft()
            for child in children[vertex]:
                if child != omitted and child not in reached:
                    reached.add(child); queue.append(child)
        if not (labels & reached):
            return False
    return True


@lru_cache(maxsize=32768)
def rooted_tree_child(graph: RootedGraph) -> bool:
    indegree, outdegree = graph.degrees()
    labels = set(graph.label_map)
    good = labels | {v for v in graph.vertices
                     if (indegree[v], outdegree[v]) == (1, 2)}
    children = defaultdict(list)
    for u, v in graph.arcs:
        children[u].append(v)
    return all(any(child in good for child in children[v])
               for v in graph.vertices if outdegree[v])


@lru_cache(maxsize=32768)
def sd0(graph: RootedGraph) -> MixedGraph:
    validate_rooted(graph)
    indegree, _ = graph.degrees()
    edges = [MixedEdge.make(u, v, (v,) if indegree[v] == 2 else ())
             for u, v in graph.arcs]
    incident = [edge for edge in edges if graph.root in edge.endpoints()]
    require(len(incident) == 2, "root_incidence")
    retained = [edge for edge in edges if graph.root not in edge.endpoints()]
    first, second = incident
    a, b = first.other(graph.root), second.other(graph.root)
    require(a != b, "root_suppression_loop")
    heads = set()
    if first.head_at(a): heads.add(a)
    if second.head_at(b): heads.add(b)
    retained.append(MixedEdge.make(a, b, heads))
    require(len(retained) == len(set(retained)), "root_suppression_parallel")
    mixed = MixedGraph(graph.labels, tuple(sorted(retained)))
    incidence = mixed.incidence(); labels = mixed.label_map
    for vertex in mixed.vertices:
        require(len(incidence[vertex]) == (1 if vertex in labels else 3),
                "nonbinary_mixed_vertex", vertex=vertex,
                degree=len(incidence[vertex]))
    require(all(len(edge.heads()) <= 1 for edge in mixed.edges),
            "bidirected_mixed_edge")
    return mixed


def mixed_local_strong(mixed: MixedGraph) -> bool:
    incidence = mixed.incidence()
    for edge in mixed.edges:
        if len(edge.heads()) != 1:
            continue
        head = next(iter(edge.heads())); tail = edge.other(head)
        if sum(not local.heads() for local in incidence[tail]) != 2:
            return False
    return True


def triangles(mixed: MixedGraph):
    adjacency = defaultdict(set)
    for edge in mixed.edges:
        adjacency[edge.u].add(edge.v); adjacency[edge.v].add(edge.u)
    answer = []
    vertices = mixed.vertices
    for i, u in enumerate(vertices):
        for j in range(i + 1, len(vertices)):
            v = vertices[j]
            if v not in adjacency[u]:
                continue
            for k in range(j + 1, len(vertices)):
                w = vertices[k]
                if w in adjacency[u] and w in adjacency[v]:
                    answer.append((u, v, w))
    return tuple(answer)


def level_at_most_two(mixed: MixedGraph) -> bool:
    graph = nx.Graph()
    graph.add_nodes_from(mixed.vertices)
    graph.add_edges_from(edge.endpoints() for edge in mixed.edges)
    retics = set(mixed.reticulations())
    return all(len(retics & set(component)) <= 2
               for component in nx.biconnected_components(graph))


@lru_cache(maxsize=32768)
def class_audit(graph: RootedGraph) -> dict:
    validate_rooted(graph)
    mixed = sd0(graph)
    result = {
        "rooted_valid": True,
        "root_is_lsa": root_is_lsa(graph),
        "rooted_tree_child": rooted_tree_child(graph),
        "mixed_local_strong": mixed_local_strong(mixed),
        "level_at_most_two": level_at_most_two(mixed),
        "triangle_count": len(triangles(mixed)),
        "reticulation_count": len(mixed.reticulations()),
    }
    require(all(result[key] for key in (
        "root_is_lsa", "rooted_tree_child", "mixed_local_strong",
        "level_at_most_two")), "graph_outside_locked_class",
        graph_id=graph.graph_id, audit=result)
    return result


def underlying_bridges(mixed: MixedGraph):
    adjacency = defaultdict(set)
    for edge in mixed.edges:
        adjacency[edge.u].add(edge.v); adjacency[edge.v].add(edge.u)
    answer = set()
    for edge in mixed.edges:
        start, goal = edge.u, edge.v
        seen = {start}; stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbour in adjacency[vertex]:
                if {vertex, neighbour} == {start, goal}:
                    continue
                if neighbour not in seen:
                    seen.add(neighbour); stack.append(neighbour)
        if goal not in seen:
            answer.add(tuple(sorted((start, goal))))
    return answer


@lru_cache(maxsize=32768)
def admissible_internal_arcs(graph: RootedGraph):
    mixed = sd0(graph)
    bridges = underlying_bridges(mixed)
    blob_pairs = {tuple(sorted(edge.endpoints())) for edge in mixed.edges
                  if tuple(sorted(edge.endpoints())) not in bridges}
    leaves = set(graph.label_map)
    answer = tuple(sorted((u, v) for u, v in graph.arcs
                          if u != graph.root and v not in leaves
                          and tuple(sorted((u, v))) in blob_pairs))
    require(bool(answer), "no_admissible_internal_arc", graph_id=graph.graph_id)
    return answer


def insert_port(parent: RootedGraph, arc: tuple[int, int], label: str):
    arc = tuple(int(x) for x in arc)
    require(parent.arcs.count(arc) == 1, "insert_nonunique_arc", arc=arc)
    require(label not in parent.label_map.values(), "duplicate_inserted_label",
            label=label)
    new_tree = max(parent.vertices) + 1; new_leaf = new_tree + 1
    arcs = list(parent.arcs); arcs.remove(arc)
    arcs.extend(((arc[0], new_tree), (new_tree, arc[1]), (new_tree, new_leaf)))
    child = RootedGraph(parent.root,
                        tuple(sorted((*parent.labels, (new_leaf, label)))),
                        tuple(sorted(arcs)))
    insertion = {
        "subdivided_parent_arc": list(arc),
        "inserted_tree_vertex": new_tree,
        "inserted_leaf_vertex": new_leaf,
        "inserted_label": label,
    }
    validate_rooted(child)
    require(delete_port(child, insertion) == parent, "delete_does_not_restore_parent")
    return child, insertion


def delete_port(child: RootedGraph, insertion: dict):
    u, v = (int(x) for x in insertion["subdivided_parent_arc"])
    tree = int(insertion["inserted_tree_vertex"])
    leaf = int(insertion["inserted_leaf_vertex"])
    label = str(insertion["inserted_label"])
    required = {(u, tree), (tree, v), (tree, leaf)}
    require(required <= set(child.arcs), "bad_delete_arcs")
    arcs = [arc for arc in child.arcs if arc not in required]; arcs.append((u, v))
    labels = [row for row in child.labels if row != (leaf, label)]
    return RootedGraph(child.root, tuple(sorted(labels)), tuple(sorted(arcs)))


def incidence_graph(mixed: MixedGraph):
    graph = nx.Graph()
    labels = mixed.label_map
    for vertex in mixed.vertices:
        graph.add_node(("v", vertex), kind="vertex", label=labels.get(vertex, ""))
    for index, edge in enumerate(mixed.edges):
        edge_node = ("e", index)
        graph.add_node(edge_node, kind="edge", label="")
        for vertex in edge.endpoints():
            incidence = ("i", index, vertex)
            graph.add_node(incidence,
                           kind="head" if edge.head_at(vertex) else "plain",
                           label="")
            graph.add_edge(("v", vertex), incidence)
            graph.add_edge(incidence, edge_node)
    return graph


def _node_match(left, right):
    return left.get("kind") == right.get("kind") and left.get("label") == right.get("label")


@lru_cache(maxsize=32768)
def unique_mixed_isomorphism(source: MixedGraph, target: MixedGraph):
    matcher = nx.algorithms.isomorphism.GraphMatcher(
        incidence_graph(source), incidence_graph(target), node_match=_node_match)
    mappings = []
    for mapping in matcher.isomorphisms_iter():
        vertex_mapping = tuple(sorted(
            (node[1], image[1]) for node, image in mapping.items()
            if node[0] == "v"
        ))
        if vertex_mapping not in mappings:
            mappings.append(vertex_mapping)
        if len(mappings) > 1:
            break
    require(len(mappings) == 1, "mixed_isomorphism_not_unique",
            count_at_least=len(mappings))
    return mappings[0]


def canonical_representation(mixed: MixedGraph, mapping_rows):
    mapping = {int(a): int(b) for a, b in mapping_rows}
    require(set(mapping) == set(mixed.vertices), "canonical_map_domain")
    require(set(mapping.values()) == set(range(len(mixed.vertices))),
            "canonical_map_codomain")
    labels = tuple(sorted((mapping[v], label) for v, label in mixed.labels))
    edges = []
    for edge in mixed.edges:
        heads = {mapping[v] for v in edge.heads()}
        edges.append(MixedEdge.make(mapping[edge.u], mapping[edge.v], heads))
    return labels, tuple(sorted(edges))


def derive_and_validate_transport(source: RootedGraph, target: RootedGraph,
                                  stored: dict):
    source_mixed = sd0(source); target_mixed = sd0(target)
    require(not triangles(source_mixed) and not triangles(target_mixed),
            "T_transport_in_triangle_free_audit")
    mapping_rows = unique_mixed_isomorphism(source_mixed, target_mixed)
    mapping = dict(mapping_rows)
    canonicalization = stored["canonicalization"]
    source_canonical = tuple(tuple(x) for x in
                             canonicalization["source_raw_to_canonical"])
    target_canonical = tuple(tuple(x) for x in
                             canonicalization["target_raw_to_canonical"])
    require(canonical_representation(source_mixed, source_canonical) ==
            canonical_representation(target_mixed, target_canonical),
            "stored_canonicalization_not_common")
    target_inverse = {int(canonical): int(raw)
                      for raw, canonical in target_canonical}
    induced = tuple(sorted((int(raw), target_inverse[int(canonical)])
                           for raw, canonical in source_canonical))
    require(induced == mapping_rows, "canonicalization_transport_not_unique")

    body = stored["transport"]
    require(tuple(tuple(x) for x in body["vertex_transport"]) == mapping_rows,
            "vertex_transport")
    expected_ports = tuple(sorted(
        (label, target_mixed.label_map[mapping[vertex]])
        for vertex, label in source_mixed.labels))
    require(tuple(tuple(x) for x in body["port_transport"]) == expected_ports,
            "port_transport")
    require(all(left == right for left, right in expected_ports),
            "nonidentity_physical_port_transport")

    source_retics = source_mixed.reticulations()
    target_retics = target_mixed.reticulations()
    require(tuple(body["reticulation_vertices_source"]) == source_retics,
            "source_reticulation_list")
    require(tuple(body["reticulation_vertices_target"]) == target_retics,
            "target_reticulation_list")
    expected_retics = tuple(sorted((v, mapping[v]) for v in source_retics))
    require(tuple(tuple(x) for x in
                  body["reticulation_transport_outside_redirected_triangle"]) ==
            expected_retics, "reticulation_transport")

    target_edges = {edge: index for index, edge in enumerate(target_mixed.edges)}
    expected_permutation = []
    for index, edge in enumerate(source_mixed.edges):
        moved = MixedEdge.make(mapping[edge.u], mapping[edge.v],
                               (mapping[v] for v in edge.heads()))
        require(moved in target_edges, "transported_edge_missing")
        expected_permutation.append((index, target_edges[moved]))
    require(tuple(tuple(x) for x in body["t_quotient_edge_permutation"]) ==
            tuple(expected_permutation), "edge_permutation")
    require(stored["fourier_coordinate_transport"] ==
            "identity_on_fixed_port_labels", "fourier_coordinate_transport")
    return mapping_rows


def transport_restricts(child_mapping, parent_mapping):
    child = dict(child_mapping)
    return all(child.get(source) == target for source, target in parent_mapping)


# ---------------------------------------------------------------------------
# Zero-sum complement-normalized JC descriptors and exact polynomial algebra.

Descriptor = tuple[int, tuple[tuple[int, ...], ...]]
Polynomial = tuple[tuple[tuple[int, ...], int], ...]


@lru_cache(maxsize=32768)
def raw_descriptor(graph: RootedGraph, port_count: int):
    labels = tuple(f"L_{index}" for index in range(port_count))
    require(set(labels) == set(graph.label_map.values()),
            "descriptor_label_set", graph_id=graph.graph_id,
            expected=labels, actual=sorted(graph.label_map.values()))
    indegree, _ = graph.degrees()
    retics = tuple(sorted(v for v in graph.vertices if indegree[v] == 2))
    displays = tuple(product((0, 1), repeat=len(retics)))
    incoming = {r: tuple(i for i, (_u, v) in enumerate(graph.arcs) if v == r)
                for r in retics}
    signatures = [[0] * len(displays) for _ in graph.arcs]
    label_index = {label: index for index, label in enumerate(labels)}
    all_leaves = set(graph.label_map)
    for display_index, choices in enumerate(displays):
        removed = {incoming[r][1 - choice]
                   for r, choice in zip(retics, choices)}
        active = tuple(i for i in range(len(graph.arcs)) if i not in removed)
        children = defaultdict(list)
        for edge_index in active:
            u, v = graph.arcs[edge_index]; children[u].append(v)
        cache = {}

        def visit(vertex):
            if vertex in cache:
                return cache[vertex]
            if vertex in all_leaves:
                value = 1 << label_index[graph.label_map[vertex]]
            else:
                value = 0
                for child in children[vertex]:
                    value |= visit(child)
            cache[vertex] = value
            return value

        for edge_index in active:
            signatures[edge_index][display_index] = visit(graph.arcs[edge_index][1])
    return len(retics), tuple(sorted(tuple(row) for row in signatures if any(row)))


@lru_cache(maxsize=16)
def quartet_combinations(port_count: int):
    return tuple(combinations(range(port_count), 4))


@lru_cache(maxsize=16384)
def canonicalize_rows(retics: int, signatures: tuple[tuple[int, ...], ...]):
    signatures = tuple(sorted(set(tuple(row) for row in signatures if any(row))))
    if not retics:
        return 0, signatures
    displays = tuple(product((0, 1), repeat=retics))
    display_index = {bits: index for index, bits in enumerate(displays)}
    candidates = []
    for permutation in permutations(range(retics)):
        for flips in product((0, 1), repeat=retics):
            moved = []
            for signature in signatures:
                row = [0] * len(displays)
                for old_index, old_bits in enumerate(displays):
                    new_bits = tuple(old_bits[permutation[j]] ^ flips[j]
                                     for j in range(retics))
                    row[display_index[new_bits]] = signature[old_index]
                moved.append(tuple(row))
            candidates.append((retics, tuple(sorted(set(moved)))))
    return min(candidates)


@lru_cache(maxsize=131072)
def quartet_descriptor(graph: RootedGraph, port_count: int, chunk: int):
    quartets = quartet_combinations(port_count)
    require(0 <= chunk < len(quartets), "quartet_chunk", chunk=chunk,
            port_count=port_count)
    quartet = quartets[chunk]
    retics, signatures = raw_descriptor(graph, port_count)
    rows = []
    for signature in signatures:
        moved = []
        for mask in signature:
            restricted = 0
            for new_index, old_index in enumerate(quartet):
                if mask & (1 << old_index):
                    restricted |= 1 << new_index
            # Exact zero-sum split-side quotient.
            moved.append(min(restricted, 0b1111 ^ restricted))
        rows.append(tuple(moved))
    return canonicalize_rows(retics, tuple(rows))


@lru_cache(maxsize=1)
def jc_representatives():
    colour_maps = [(0, *row) for row in permutations((1, 2, 3))]

    def canon(row):
        return min(tuple(mapping[value] for value in row)
                   for mapping in colour_maps)

    answer = tuple(sorted({canon(row) for row in product(range(4), repeat=4)
                           if row[0] ^ row[1] ^ row[2] ^ row[3] == 0}))
    require(len(answer) == 15, "JC_representative_count")
    return answer


def poly_dict(poly: Polynomial):
    return dict(poly)


def poly_tuple(poly: dict):
    return tuple(sorted((tuple(exponent), int(coefficient))
                        for exponent, coefficient in poly.items() if coefficient))


def poly_add(left: dict, right: dict, scale: int = 1):
    answer = dict(left)
    for exponent, coefficient in right.items():
        value = answer.get(exponent, 0) + scale * coefficient
        if value:
            answer[exponent] = value
        else:
            answer.pop(exponent, None)
    return answer


def poly_mul(left: dict, right: dict):
    if not left or not right:
        return {}
    answer = defaultdict(int)
    for a, ca in left.items():
        for b, cb in right.items():
            answer[tuple(x + y for x, y in zip(a, b))] += ca * cb
    return {m: c for m, c in answer.items() if c}


@lru_cache(maxsize=8192)
def coordinate_polynomials(descriptor: Descriptor):
    retics, signatures = descriptor
    displays = tuple(product((0, 1), repeat=retics))
    variables = len(signatures) + retics
    coordinates = []
    for assignment in jc_representatives():
        total = {}
        for display_index, choices in enumerate(displays):
            exponent = [0] * variables
            for variable, signature in enumerate(signatures):
                mask = signature[display_index]
                state = 0
                for leaf_index, character in enumerate(assignment):
                    if mask & (1 << leaf_index):
                        state ^= character
                if state:
                    exponent[variable] = 1
            term = {tuple(exponent): 1}
            for retic_index, choice in enumerate(choices):
                variable = len(signatures) + retic_index
                row = [0] * variables; row[variable] = 1
                factor = ({tuple(row): 1} if choice == 0 else
                          {(0,) * variables: 1, tuple(row): -1})
                term = poly_mul(term, factor)
            total = poly_add(total, term)
        coordinates.append(poly_tuple(total))
    return tuple(coordinates)


@lru_cache(maxsize=32768)
def pullback(descriptor: Descriptor, invariant):
    coordinates = tuple(poly_dict(poly) for poly in coordinate_polynomials(descriptor))
    variables = len(descriptor[1]) + descriptor[0]
    monomial_cache = {(): {(0,) * variables: 1}}

    def monomial(indices):
        indices = tuple(indices)
        if indices not in monomial_cache:
            monomial_cache[indices] = poly_mul(
                monomial(indices[:-1]), coordinates[indices[-1]])
        return monomial_cache[indices]

    answer = {}
    for indices, coefficient in invariant:
        answer = poly_add(answer, monomial(tuple(indices)), int(coefficient))
    return poly_tuple(answer)


def exact_poly_hash(poly: Polynomial):
    return hashlib.sha256(repr(tuple(sorted(poly))).encode()).hexdigest()


def polynomial_record(poly: Polynomial):
    variable_count = len(poly[0][0]) if poly else 0
    payload = {
        "schema": 1,
        "variable_count": variable_count,
        "terms": poly,
    }
    return stable_hash(payload), payload


def parse_literal(path: Path, name: str):
    module = ast.parse(path.read_text())
    for node in module.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                node.targets[0].id == name):
            return ast.literal_eval(node.value)
    raise KeyError(name)


def invariant_orbit(templates):
    representatives = jc_representatives()
    rep_index = {row: index for index, row in enumerate(representatives)}
    colour_maps = [(0, *row) for row in permutations((1, 2, 3))]

    def canon(row):
        return min(tuple(mapping[value] for value in row)
                   for mapping in colour_maps)

    orbit = set()
    for template in templates:
        for leaf_permutation in permutations(range(4)):
            terms = defaultdict(int)
            for indices, coefficient in template:
                moved = []
                for coordinate in indices:
                    assignment = representatives[coordinate]
                    transported = tuple(assignment[leaf_permutation[i]]
                                        for i in range(4))
                    moved.append(rep_index[canon(transported)])
                terms[tuple(sorted(moved))] += int(coefficient)
            normalized = tuple(sorted((m, c) for m, c in terms.items() if c))
            if normalized and normalized[0][1] < 0:
                normalized = tuple((m, -c) for m, c in normalized)
            orbit.add(normalized)
    return tuple(sorted(orbit))


def load_invariants(template_path: Path, seventh_path: Path):
    templates = parse_literal(template_path, "INVARIANT_TEMPLATES")
    seventh_payload = json.loads(seventh_path.read_text())
    seventh = tuple((tuple(int(index) + 1 for index in monomial), int(coefficient))
                    for coefficient, monomial in seventh_payload["invariant"])
    answer = invariant_orbit((*templates, seventh))
    require(len(answer) == 84, "invariant_orbit_count", actual=len(answer))
    return answer
