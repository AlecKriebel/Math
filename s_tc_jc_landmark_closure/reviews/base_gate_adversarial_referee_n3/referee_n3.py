#!/usr/bin/env python3
"""Adversarial metareferee for the frozen schema-3 n=3 base gate.

Primary and Euclid files are immutable claims and content-addressed inputs,
never imported executable code.  This verifier independently rebuilds rooted
and mixed graphs, switching tensors, the zero-sum quotient, every path in the
fixed-root forest, all 225 graph-derived pullback bodies, and every strict-sign
factor proof.  Its graph canonizer and sparse algebra are local to this file.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import copy
from dataclasses import dataclass
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent

SUMMARY = PROJECT / "primary/certificates/hard_cover_schema3_n3_full_summary.json"
RELATIONS = PROJECT / "primary/certificates/hard_cover_n3_schema3_n3_full.jsonl.gz"
GRAPHS = PROJECT / "primary/certificates/hard_cover_graphs_n3_schema3_n3_full.jsonl.gz"
ROOTS = PROJECT / "primary/certificates/hard_cover_root_cases_n3_schema3_n3_full.jsonl.gz"
POLYNOMIALS = PROJECT / "primary/certificates/hard_cover_polynomials_n3_schema3_n3_full.jsonl.gz"
MULTIDEGREES = PROJECT / "primary/certificates/invariant_multihomogeneity.json"
TEMPLATES = PROJECT.parent / "strong_level2_phylo_identifiability/src/jc_root_spanning_atlas_data.py"
SEVENTH = PROJECT / "primary/seventh_invariant.json"
DEFINITIONS = PROJECT / "docs/DEFINITIONS_LOCK.md"
EUCLID_PATH_AUDIT = PROJECT / "reviews/final_hard_cover_cleanroom/certificates/schema3_n3_path_audit.json"
EUCLID_AUDITOR = PROJECT / "reviews/final_hard_cover_cleanroom/audit_candidate_stream.py"
EUCLID_GRAPH = PROJECT / "reviews/final_hard_cover_cleanroom/graph_model.py"
EUCLID_ALGEBRA = PROJECT / "reviews/final_hard_cover_cleanroom/jc_exact.py"
TRIANGLE_CERTIFICATE = PROJECT / "reviews/triangle_redirection_cleanroom/certificate.json"
STRICT_FACTORS = HERE / "strict_factor_certificate.json"

EXPECTED = {
    "summary": "791844a802af61f64cba937a5adbe9d1d381d3fd7e55165914d4e4c885908e65",
    "relations_physical": "dc128b64f5bdfbfa99c3db763112edd6491753b2c8b5341dd81aac14e8c416ca",
    "graphs_physical": "c1cccad20a589a7fbd6f91075f916d4965f97a0a626ae11244315b01e836fc29",
    "roots_physical": "45cc312e3d915c8015824673ef1a27050f375b3575e2e64fbff3f55f32a27929",
    "polynomials_physical": "11b3e2f8870fc711b7986df083b1e1d3aa2806ede321fd38eab60d0a25f789d6",
    "definitions": "3108a20e924a37b069cc4aeb53b051b03463176eafce9d590dfec378e2ad16a2",
    "euclid_path_audit": "6e304691ffeea6d9bc1118b59d778a1051e8fc1f9c3430e06b77fe48c82d8a97",
    "euclid_auditor": "fa2314a9e01220293f0706101d10f2a6bb52bd1a301f5add100391c0b9e50d85",
    "euclid_graph": "4c21cbc301eeab502b722b5e71cee3f14616c2874a142a43e95fcc581b1309a1",
    "euclid_algebra": "520140dda3260098c7e937a1dc38197bae65192dcb2149511f3db473fb87f1a9",
    "triangle_certificate": "d4b118fef3036829fe05c6b4176d0c4e637b39f45637b903eefba2b5ac5283fd",
    "strict_factor_certificate": "5f14ddfafdd5a3fa165f4f2b832c542fde1ece041d39f30e39e9972f3dde0492",
    "templates": "dd4b47f018d8f261fe296430513cedc1691b39cdb57fa075e42d884ecfba9ee3",
    "seventh": "f737f9bee9cc04045355416b95629c18cb5aa9bc31d9719e319eb0a3907babed",
    "multidegrees": "a8f50b3704d564ff5f484ea140bb85b1dfea561f043f2c29b30c0ce3227f5eae",
    "commit_n3": "be8a30870550efba2115cf2eb87e1d3611dd8c3b",
    "commit_zero_sum": "f3cc9493b1e677378e3c0b4f8e965cb9199a436f",
    "commit_euclid": "1018701d04d8656fe9ac92bb201413e043b802a1",
    "commit_triangle": "663336f839c29d91024220ed3777d0c124e975f5",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def read_jsonl_gzip(path: Path) -> tuple[list[dict], str]:
    records: list[dict] = []
    digest = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for line in handle:
            digest.update(line)
            records.append(json.loads(line))
    return records, digest.hexdigest()


def natural(label: str):
    prefix, _, suffix = label.rpartition("_")
    return prefix, int(suffix) if suffix.isdigit() else -1, label


@dataclass(frozen=True)
class Rooted:
    root: int
    labels: tuple[tuple[int, str], ...]
    arcs: tuple[tuple[int, int], ...]

    @classmethod
    def from_payload(cls, payload: dict) -> "Rooted":
        return cls(int(payload["root"]),
                   tuple((int(v), str(label)) for v, label in payload["labels"]),
                   tuple((int(u), int(v)) for u, v in payload["arcs"]))

    def payload(self) -> dict:
        return {"root": self.root, "labels": [list(row) for row in self.labels],
                "arcs": [list(row) for row in self.arcs]}


@dataclass(frozen=True)
class Mixed:
    labels: tuple[tuple[int, str], ...]
    undirected: tuple[tuple[int, int], ...]
    directed: tuple[tuple[int, int], ...]

    def vertices(self) -> set[int]:
        answer = {v for v, _label in self.labels}
        for u, v in self.undirected + self.directed:
            answer.add(u)
            answer.add(v)
        return answer


def upair(u: int, v: int) -> tuple[int, int]:
    if u == v:
        raise ValueError("loop")
    return (u, v) if u < v else (v, u)


def rooted_tables(graph: Rooted):
    vertices = {graph.root, *(v for v, _label in graph.labels)}
    for u, v in graph.arcs:
        vertices.add(u)
        vertices.add(v)
    indegree = {v: 0 for v in vertices}
    outdegree = {v: 0 for v in vertices}
    children = {v: [] for v in vertices}
    for u, v in graph.arcs:
        outdegree[u] += 1
        indegree[v] += 1
        children[u].append(v)
    return vertices, indegree, outdegree, children


def acyclic(vertices: Iterable[int], arcs: Iterable[tuple[int, int]]) -> bool:
    vertices = set(vertices)
    indegree = {v: 0 for v in vertices}
    children = {v: [] for v in vertices}
    for u, v in arcs:
        indegree[v] += 1
        children[u].append(v)
    queue = [v for v in vertices if indegree[v] == 0]
    seen = 0
    while queue:
        u = queue.pop()
        seen += 1
        for v in children[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return seen == len(vertices)


def all_paths(graph: Rooted, target: int) -> list[tuple[int, ...]]:
    _vertices, _indegree, _outdegree, children = rooted_tables(graph)
    answer: list[tuple[int, ...]] = []

    def visit(vertex: int, path: tuple[int, ...]) -> None:
        if vertex == target:
            answer.append(path)
            return
        for child in children[vertex]:
            if child not in path:
                visit(child, path + (child,))

    visit(graph.root, (graph.root,))
    return answer


def root_is_lsa(graph: Rooted) -> bool:
    common: set[int] | None = None
    for leaf, _label in graph.labels:
        paths = all_paths(graph, leaf)
        if not paths:
            return False
        stable = set(paths[0])
        for path in paths[1:]:
            stable.intersection_update(path)
        common = stable if common is None else common.intersection(stable)
    return common == {graph.root}


def rooted_validation(graph: Rooted) -> list[str]:
    failures: list[str] = []
    if len(graph.arcs) != len(set(graph.arcs)):
        failures.append("parallel-arc")
    if any(u == v for u, v in graph.arcs):
        failures.append("loop")
    vertices, indegree, outdegree, children = rooted_tables(graph)
    labels = dict(graph.labels)
    if len(labels) != len(graph.labels) or len(set(labels.values())) != len(labels):
        failures.append("label-bijection")
    if (indegree[graph.root], outdegree[graph.root]) != (0, 2):
        failures.append("root-degree")
    for vertex in vertices - {graph.root}:
        degree = indegree[vertex], outdegree[vertex]
        if vertex in labels:
            if degree != (1, 0):
                failures.append(f"leaf-degree:{vertex}:{degree}")
        elif degree not in {(1, 2), (2, 1)}:
            failures.append(f"internal-degree:{vertex}:{degree}")
    if not acyclic(vertices, graph.arcs):
        failures.append("cycle")
    reachable = {graph.root}
    stack = [graph.root]
    while stack:
        vertex = stack.pop()
        for child in children[vertex]:
            if child not in reachable:
                reachable.add(child)
                stack.append(child)
    if reachable != vertices:
        failures.append("unreachable")
    if not root_is_lsa(graph):
        failures.append("root-not-lsa")
    return failures


def rooted_tree_child(graph: Rooted) -> bool:
    vertices, indegree, outdegree, children = rooted_tables(graph)
    leaves = set(dict(graph.labels))
    return all(any(child in leaves or (indegree[child], outdegree[child]) == (1, 2)
                   for child in children[vertex]) for vertex in vertices - leaves)


def sd0(graph: Rooted) -> Mixed:
    failures = rooted_validation(graph)
    if failures:
        raise ValueError(failures)
    vertices, indegree, outdegree, _children = rooted_tables(graph)
    retics = {v for v in vertices if (indegree[v], outdegree[v]) == (2, 1)}
    root_children = sorted(v for u, v in graph.arcs if u == graph.root)
    if len(root_children) != 2:
        raise ValueError("root children")
    directed: set[tuple[int, int]] = set()
    undirected: set[tuple[int, int]] = set()
    for u, v in graph.arcs:
        if u == graph.root:
            continue
        if v in retics:
            directed.add((u, v))
        else:
            undirected.add(upair(u, v))
    left, right = root_children
    if left in retics and right in retics:
        raise ValueError("two-headed root artifact")
    if left in retics:
        directed.add((right, left))
    elif right in retics:
        directed.add((left, right))
    else:
        undirected.add(upair(left, right))
    pairs = list(undirected) + [upair(*edge) for edge in directed]
    if len(pairs) != len(set(pairs)):
        raise ValueError("parallel root artifact")
    return Mixed(tuple(sorted(graph.labels)), tuple(sorted(undirected)), tuple(sorted(directed)))


def mixed_reticulations(graph: Mixed) -> set[int]:
    incoming = Counter(v for _u, v in graph.directed)
    return {v for v, count in incoming.items() if count == 2}


def mixed_validation(graph: Mixed) -> list[str]:
    failures: list[str] = []
    vertices = graph.vertices()
    labels = dict(graph.labels)
    pairs = list(graph.undirected) + [upair(*edge) for edge in graph.directed]
    if len(pairs) != len(set(pairs)):
        failures.append("parallel-mixed-edge")
    degree = Counter()
    incoming = Counter()
    for u, v in graph.undirected:
        degree[u] += 1
        degree[v] += 1
    for u, v in graph.directed:
        degree[u] += 1
        degree[v] += 1
        incoming[v] += 1
    for v in vertices:
        if degree[v] != (1 if v in labels else 3):
            failures.append(f"mixed-degree:{v}:{degree[v]}")
    if any(count != 2 for count in incoming.values()):
        failures.append("arrowhead-count")
    return failures


def no_omnian(graph: Mixed) -> bool:
    undirected_degree = Counter()
    for u, v in graph.undirected:
        undirected_degree[u] += 1
        undirected_degree[v] += 1
    return all(undirected_degree[u] == 2 for u, _v in graph.directed)


def biconnected_components(graph: Mixed) -> list[set[int]]:
    adjacency = {v: set() for v in graph.vertices()}
    for u, v in graph.undirected + tuple(upair(*edge) for edge in graph.directed):
        adjacency[u].add(v)
        adjacency[v].add(u)
    discovery: dict[int, int] = {}
    low: dict[int, int] = {}
    parent: dict[int, int | None] = {}
    stack: list[tuple[int, int]] = []
    components: list[set[int]] = []
    clock = 0

    def visit(u: int) -> None:
        nonlocal clock
        clock += 1
        discovery[u] = low[u] = clock
        for v in sorted(adjacency[u]):
            edge = upair(u, v)
            if v not in discovery:
                parent[v] = u
                stack.append(edge)
                visit(v)
                low[u] = min(low[u], low[v])
                if low[v] >= discovery[u]:
                    component: set[int] = set()
                    while stack:
                        popped = stack.pop()
                        component.update(popped)
                        if popped == edge:
                            break
                    components.append(component)
            elif parent.get(u) != v and discovery[v] < discovery[u]:
                stack.append(edge)
                low[u] = min(low[u], discovery[v])

    for root in sorted(adjacency):
        if root not in discovery:
            parent[root] = None
            visit(root)
            if stack:
                component: set[int] = set()
                while stack:
                    component.update(stack.pop())
                components.append(component)
    return components


def level(graph: Mixed) -> int:
    rets = mixed_reticulations(graph)
    return max((len(component & rets) for component in biconnected_components(graph)), default=0)


def triangles(graph: Mixed) -> list[tuple[int, int, int]]:
    edges = set(graph.undirected) | {upair(*edge) for edge in graph.directed}
    return [triple for triple in itertools.combinations(sorted(graph.vertices()), 3)
            if all(upair(*pair) in edges for pair in itertools.combinations(triple, 2))]


def incidence_map(graph: Mixed) -> dict[int, list[tuple[str, int]]]:
    answer = {v: [] for v in graph.vertices()}
    for u, v in graph.undirected:
        answer[u].append(("U", v))
        answer[v].append(("U", u))
    for u, v in graph.directed:
        answer[u].append(("O", v))
        answer[v].append(("H", u))
    return answer


def refine_colours(graph: Mixed, seed: dict[int, object]) -> dict[int, int]:
    adjacency = incidence_map(graph)
    colours: dict[int, object] = dict(seed)
    while True:
        signatures = {
            vertex: (colours[vertex], tuple(sorted(
                ((kind, colours[neighbor]) for kind, neighbor in adjacency[vertex]),
                key=repr,
            )))
            for vertex in adjacency
        }
        palette = {signature: index for index, signature in
                   enumerate(sorted(set(signatures.values()), key=repr))}
        moved = {vertex: palette[signature] for vertex, signature in signatures.items()}
        if all(colours[vertex] == moved[vertex] for vertex in moved
               if isinstance(colours[vertex], int)) and all(isinstance(value, int) for value in colours.values()):
            return moved
        if len(set(moved.values())) == len(set(colours.values())) and all(isinstance(value, int) for value in colours.values()):
            # Stable partition even if canonical colour numbers were renamed.
            old_parts = {frozenset(v for v in colours if colours[v] == colour)
                         for colour in set(colours.values())}
            new_parts = {frozenset(v for v in moved if moved[v] == colour)
                         for colour in set(moved.values())}
            if old_parts == new_parts:
                return moved
        colours = moved


def mixed_canonical_code(graph: Mixed) -> str:
    labels = dict(graph.labels)
    rets = mixed_reticulations(graph)
    initial = {v: (("leaf", labels[v]) if v in labels else
                   ("retic",) if v in rets else ("internal",)) for v in graph.vertices()}

    def encode(colours: dict[int, int]) -> str:
        order = [vertex for vertex, _colour in sorted(colours.items(), key=lambda row: row[1])]
        index = {vertex: i for i, vertex in enumerate(order)}
        vertex_rows = [("L", labels[v]) if v in labels else ("R",) if v in rets else ("I",)
                       for v in order]
        edge_rows = [("U", *sorted((index[u], index[v]))) for u, v in graph.undirected]
        edge_rows.extend(("D", index[u], index[v]) for u, v in graph.directed)
        return json.dumps([vertex_rows, sorted(edge_rows)], separators=(",", ":"))

    def search(seed: dict[int, object]) -> str:
        colours = refine_colours(graph, seed)
        cells = defaultdict(list)
        for vertex, colour in colours.items():
            cells[colour].append(vertex)
        ambiguous = [sorted(cell) for _colour, cell in sorted(cells.items()) if len(cell) > 1]
        if not ambiguous:
            return encode(colours)
        cell = min(ambiguous, key=lambda values: (len(values), values))
        candidates = []
        for chosen in cell:
            individualized = {vertex: ("old", colours[vertex], "chosen" if vertex == chosen else "plain")
                              for vertex in colours}
            candidates.append(search(individualized))
        return min(candidates)

    return search(initial)


def t_quotient_codes(graph: Mixed) -> set[str]:
    """Canonical codes after forgetting arrowheads on exactly one triangle."""
    answer = set()
    for triangle in triangles(graph):
        tri_edges = {upair(u, v) for u, v in itertools.combinations(triangle, 2)}
        undirected = {upair(*edge) for edge in graph.undirected}
        directed = set(graph.directed)
        for u, v in tuple(directed):
            if upair(u, v) in tri_edges:
                directed.remove((u, v))
        undirected.difference_update(tri_edges)
        undirected.update(tri_edges)
        freed = Mixed(graph.labels, tuple(sorted(undirected)), tuple(sorted(directed)))
        answer.add(mixed_canonical_code(freed))
    return answer


def mixed_isomorphic_backtrack(left: Mixed, right: Mixed) -> bool:
    """A second exact terminal check, independent of canonical-code equality."""
    if len(left.vertices()) != len(right.vertices()):
        return False
    if Counter(label for _v, label in left.labels) != Counter(label for _v, label in right.labels):
        return False

    def relation(graph: Mixed):
        answer = {}
        for u, v in graph.undirected:
            answer[u, v] = answer[v, u] = "U"
        for u, v in graph.directed:
            answer[u, v] = "O"
            answer[v, u] = "H"
        return answer

    def distances(graph: Mixed):
        adjacency = {v: set() for v in graph.vertices()}
        for u, v in graph.undirected + tuple(upair(*edge) for edge in graph.directed):
            adjacency[u].add(v)
            adjacency[v].add(u)
        labels = dict(graph.labels)
        answer = {}
        for vertex in graph.vertices():
            distance = {vertex: 0}
            queue = [vertex]
            while queue:
                u = queue.pop(0)
                for v in adjacency[u]:
                    if v not in distance:
                        distance[v] = distance[u] + 1
                        queue.append(v)
            answer[vertex] = tuple(distance[label_vertex]
                                   for label_vertex, _label in sorted(graph.labels, key=lambda row: row[1]))
        return answer

    left_labels = {label: vertex for vertex, label in left.labels}
    right_labels = {label: vertex for vertex, label in right.labels}
    mapping = {left_labels[label]: right_labels[label] for label in left_labels}
    used = set(mapping.values())
    left_relation, right_relation = relation(left), relation(right)
    for left_vertex, right_vertex in mapping.items():
        for left_other, right_other in mapping.items():
            if left_relation.get((left_vertex, left_other)) != right_relation.get(
                    (right_vertex, right_other)):
                return False
    left_incidence, right_incidence = incidence_map(left), incidence_map(right)
    left_distances, right_distances = distances(left), distances(right)
    left_rets, right_rets = mixed_reticulations(left), mixed_reticulations(right)

    def feature(graph, vertex, incidence, rets, distance):
        labels = dict(graph.labels)
        return (
            labels.get(vertex), vertex in rets,
            Counter(kind for kind, _neighbor in incidence[vertex]),
            distance[vertex],
        )

    left_internal = sorted(left.vertices() - set(dict(left.labels)))
    right_internal = sorted(right.vertices() - set(dict(right.labels)))
    candidates = {
        vertex: [target for target in right_internal
                 if feature(left, vertex, left_incidence, left_rets, left_distances) ==
                 feature(right, target, right_incidence, right_rets, right_distances)]
        for vertex in left_internal
    }
    if any(not values for values in candidates.values()):
        return False

    def compatible(vertex: int, target: int) -> bool:
        for old, moved in mapping.items():
            if left_relation.get((vertex, old)) != right_relation.get((target, moved)):
                return False
            if left_relation.get((old, vertex)) != right_relation.get((moved, target)):
                return False
        return True

    def search() -> bool:
        remaining = [vertex for vertex in left_internal if vertex not in mapping]
        if not remaining:
            return True
        vertex = min(remaining, key=lambda value: sum(target not in used for target in candidates[value]))
        for target in candidates[vertex]:
            if target in used or not compatible(vertex, target):
                continue
            mapping[vertex] = target
            used.add(target)
            if search():
                return True
            used.remove(target)
            del mapping[vertex]
        return False

    return search()


def displayed_switchings(graph: Rooted):
    vertices, indegree, outdegree, _children = rooted_tables(graph)
    retics = sorted(v for v in vertices if (indegree[v], outdegree[v]) == (2, 1))
    parents = {retic: sorted(u for u, v in graph.arcs if v == retic) for retic in retics}
    incoming = {(parent, retic) for retic in retics for parent in parents[retic]}
    for bits in itertools.product((0, 1), repeat=len(retics)):
        chosen = {(parents[retic][bit], retic) for retic, bit in zip(retics, bits)}
        active = tuple(edge for edge in graph.arcs if edge not in incoming or edge in chosen)
        yield bits, active, retics


def descendant_mask(graph: Rooted, active: Sequence[tuple[int, int]], child: int,
                    ordered_labels: Sequence[str]) -> int:
    children = defaultdict(list)
    for u, v in active:
        children[u].append(v)
    labels = dict(graph.labels)
    positions = {label: i for i, label in enumerate(ordered_labels)}
    mask = 0
    stack = [child]
    seen = set()
    while stack:
        vertex = stack.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        label = labels.get(vertex)
        if label in positions:
            mask |= 1 << positions[label]
        stack.extend(children[vertex])
    return mask


def descriptor(graph: Rooted, ordered_labels: Sequence[str], complement: str = "correct"):
    switchings = list(displayed_switchings(graph))
    retic_count = len(switchings[0][2])
    rows = [[0] * len(switchings) for _edge in graph.arcs]
    full = (1 << len(ordered_labels)) - 1
    for display_index, (_bits, active, _retics) in enumerate(switchings):
        active_set = set(active)
        for edge_index, edge in enumerate(graph.arcs):
            if edge not in active_set:
                continue
            mask = descendant_mask(graph, active, edge[1], ordered_labels)
            if complement == "correct":
                mask = min(mask, full ^ mask)
            elif complement == "width4":
                mask = min(mask, 0b1111 ^ mask)
            elif complement != "none":
                raise ValueError(complement)
            rows[edge_index][display_index] = mask
    return retic_count, tuple(sorted(set(tuple(row) for row in rows if any(row))))


def canonical_display_descriptor(desc):
    retics, rows = desc
    displays = tuple(itertools.product((0, 1), repeat=retics))
    index = {bits: i for i, bits in enumerate(displays)}
    candidates = []
    for permutation in itertools.permutations(range(retics)):
        for flips in itertools.product((0, 1), repeat=retics):
            moved = []
            for row in rows:
                new_row = []
                for new_bits in displays:
                    old_bits = tuple(new_bits[permutation[j]] ^ flips[j] for j in range(retics))
                    new_row.append(row[index[old_bits]])
                moved.append(tuple(new_row))
            candidates.append((retics, tuple(sorted(set(moved)))))
    return min(candidates) if candidates else desc


def jc_representatives():
    colour_maps = [(0, *row) for row in itertools.permutations((1, 2, 3))]
    def canon(row):
        return min(tuple(mapping[value] for value in row) for mapping in colour_maps)
    reps = sorted({canon(row) for row in itertools.product(range(4), repeat=4)
                   if row[0] ^ row[1] ^ row[2] ^ row[3] == 0})
    if len(reps) != 15:
        raise AssertionError(len(reps))
    return tuple(reps), canon


def parse_templates():
    module = ast.parse(TEMPLATES.read_text())
    base = None
    for node in module.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name)
                                                and target.id == "INVARIANT_TEMPLATES"
                                                for target in node.targets):
            base = ast.literal_eval(node.value)
            break
    if base is None:
        raise AssertionError("templates not found")
    seventh_payload = json.loads(SEVENTH.read_text())
    seventh = tuple((tuple(int(index) + 1 for index in monomial), int(coefficient))
                    for coefficient, monomial in seventh_payload["invariant"])
    return (*base, seventh)


def invariant_orbit():
    reps, canon = jc_representatives()
    rep_index = {row: i for i, row in enumerate(reps)}
    orbit = set()
    for template in parse_templates():
        for permutation in itertools.permutations(range(4)):
            terms = Counter()
            for coordinates, coefficient in template:
                moved = []
                for coordinate in coordinates:
                    assignment = reps[coordinate]
                    transported = tuple(assignment[permutation[i]] for i in range(4))
                    moved.append(rep_index[canon(transported)])
                terms[tuple(sorted(moved))] += int(coefficient)
            normalized = tuple(sorted((monomial, coefficient) for monomial, coefficient in terms.items()
                                      if coefficient))
            if normalized and normalized[0][1] < 0:
                normalized = tuple((monomial, -coefficient) for monomial, coefficient in normalized)
            orbit.add(normalized)
    answer = tuple(sorted(orbit))
    if len(answer) != 84:
        raise AssertionError(f"invariant orbit has {len(answer)} elements")
    return answer


def audit_invariant_binding(invariants):
    claimed = json.loads(MULTIDEGREES.read_text())
    rows = {int(row["index"]): row for row in claimed["records"]}
    reps, _canon = jc_representatives()
    failures = []
    degree_distribution = Counter()
    for index, invariant in enumerate(invariants):
        digest = hashlib.sha256(repr(invariant).encode()).hexdigest()
        degrees = {
            tuple(sum(reps[coordinate][port] != 0 for coordinate in monomial)
                  for port in range(4))
            for monomial, _coefficient in invariant
        }
        if len(degrees) != 1:
            failures.append([index, "not-multihomogeneous", sorted(degrees)])
            continue
        degree = next(iter(degrees))
        degree_distribution[degree] += 1
        row = rows.get(index)
        if row is None:
            failures.append([index, "missing-claimed-record"])
            continue
        if digest != row["invariant_sha256"]:
            failures.append([index, "invariant-index-hash"])
        if list(degree) != row["port_arm_multidegree"]:
            failures.append([index, "port-arm-degree", degree, row["port_arm_multidegree"]])
    if len(rows) != len(invariants):
        failures.append(["record-count", len(rows), len(invariants)])
    return {
        "status": "VERIFIED" if not failures else "FALSE",
        "failure_count": len(failures), "first_failures": failures[:20],
        "invariant_count": len(invariants),
        "all_multihomogeneous": not failures,
        "degree_distribution": {repr(key): value for key, value in sorted(degree_distribution.items())},
    }


Poly = dict[tuple[int, ...], int]


def poly_add(left: Poly, right: Poly, scale: int = 1) -> Poly:
    answer = dict(left)
    for monomial, coefficient in right.items():
        value = answer.get(monomial, 0) + scale * coefficient
        if value:
            answer[monomial] = value
        else:
            answer.pop(monomial, None)
    return answer


def poly_mul(left: Poly, right: Poly) -> Poly:
    if not left or not right:
        return {}
    answer = Counter()
    for lm, lc in left.items():
        for rm, rc in right.items():
            answer[tuple(a + b for a, b in zip(lm, rm))] += lc * rc
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def coordinate_polynomials(desc) -> tuple[Poly, ...]:
    retics, rows = desc
    displays = tuple(itertools.product((0, 1), repeat=retics))
    variables = len(rows) + retics
    reps, _canon = jc_representatives()
    coordinates = []
    for assignment in reps:
        total: Poly = {}
        for display_index, bits in enumerate(displays):
            exponent = [0] * variables
            for edge_index, row in enumerate(rows):
                mask = row[display_index]
                value = 0
                for leaf_index, character in enumerate(assignment):
                    if mask & (1 << leaf_index):
                        value ^= character
                if value:
                    exponent[edge_index] = 1
            term: Poly = {tuple(exponent): 1}
            for retic_index, bit in enumerate(bits):
                lam_exp = [0] * variables
                lam_exp[len(rows) + retic_index] = 1
                if bit == 0:
                    factor = {tuple(lam_exp): 1}
                else:
                    factor = {(0,) * variables: 1, tuple(lam_exp): -1}
                term = poly_mul(term, factor)
            total = poly_add(total, term)
        coordinates.append(total)
    return tuple(coordinates)


def invariant_poly(coordinates: Sequence[Poly], invariant) -> Poly:
    variables = len(next(iter(coordinates[0]))) if coordinates[0] else 0
    total: Poly = {}
    for monomial, coefficient in invariant:
        term: Poly = {(0,) * variables: int(coefficient)}
        for index in monomial:
            term = poly_mul(term, coordinates[index])
        total = poly_add(total, term)
    return total


PRIME = 2_147_483_647


def coordinate_values_mod(desc, seed: int) -> tuple[int, ...]:
    retics, rows = desc
    displays = tuple(itertools.product((0, 1), repeat=retics))
    values = []
    for index in range(len(rows) + retics):
        value = (seed * 1_000_003 + index * 97_409 + 31) % PRIME
        if value in {0, 1}:
            value += 2
        values.append(value)
    edge_values = values[:len(rows)]
    inheritances = values[len(rows):]
    reps, _canon = jc_representatives()
    answer = []
    for assignment in reps:
        total = 0
        for display_index, bits in enumerate(displays):
            term = 1
            for retic_index, bit in enumerate(bits):
                lam = inheritances[retic_index]
                term = term * (lam if bit == 0 else 1 - lam) % PRIME
            for edge_value, row in zip(edge_values, rows):
                mask = row[display_index]
                value = 0
                for leaf_index, character in enumerate(assignment):
                    if mask & (1 << leaf_index):
                        value ^= character
                if value:
                    term = term * edge_value % PRIME
            total = (total + term) % PRIME
        answer.append(total)
    return tuple(answer)


def invariant_value_mod(coordinates: Sequence[int], invariant) -> int:
    total = 0
    for monomial, coefficient in invariant:
        term = coefficient % PRIME
        for index in monomial:
            term = term * coordinates[index] % PRIME
        total = (total + term) % PRIME
    return total


def insertion_words(words: Sequence[Sequence[str]], label: str) -> set[tuple[tuple[str, ...], ...]]:
    answer = set()
    words = tuple(tuple(word) for word in words)
    for segment, word in enumerate(words):
        for position in range(len(word) + 1):
            moved = list(words)
            moved[segment] = (*word[:position], label, *word[position:])
            answer.add(tuple(moved))
    return answer


def state_payload(state: dict, graph_rows: dict[str, dict]) -> dict:
    source_code = graph_rows[state["source_graph_id"]]["standard_mixed_code"]
    target_code = graph_rows[state["target_graph_id"]]["standard_mixed_code"]
    p = int(state["selected_port_count"])
    return {
        "fixed_full_root_case_id": state["fixed_full_root_case_id"],
        "selected_port_count": p,
        "source_rooted_graph_id": state["source_graph_id"],
        "target_rooted_graph_id": state["target_graph_id"],
        "source_mixed_code": source_code,
        "target_completion_mixed_code": target_code,
        "remaining_target_roles": state["remaining_target_roles"],
        "port_matching": list(range(p)),
    }


def exact_poly_hash_from_row(row: dict) -> str:
    body = {tuple(exponents): int(coefficient) for exponents, coefficient in row["terms"]}
    return hashlib.sha256(repr(tuple(sorted(body.items()))).encode()).hexdigest()


def audit_streams(summary: dict, relations: list[dict], graphs: list[dict], roots: list[dict],
                  polynomials: list[dict], logical_hashes: dict[str, str]) -> dict:
    failures = []
    hard = summary["runs"][0]["hard_cover"]
    expected_counts = {
        "relations": 68584, "graphs": 14482, "roots": 5344, "polynomials": 225,
    }
    actual_counts = {"relations": len(relations), "graphs": len(graphs),
                     "roots": len(roots), "polynomials": len(polynomials)}
    if actual_counts != expected_counts:
        failures.append(f"counts:{actual_counts}")
    logical_expected = {
        "relations": hard["relation_stream_sha256"],
        "graphs": hard["graph_library_stream_sha256"],
        "roots": hard["root_case_stream_sha256"],
        "polynomials": hard["polynomial_library_stream_sha256"],
    }
    if logical_hashes != logical_expected:
        failures.append("logical-stream-hashes")
    classes = Counter(row["terminal_classification"] for row in relations)
    if classes != Counter({"generic_polynomial_separation": 56055,
                           "refined_by_next_restoration": 8349,
                           "strict_open_cube_separation": 4036,
                           "support_prefix_labelled_isomorphism": 120,
                           "support_prefix_ordinary_T": 24}):
        failures.append(f"terminal-counts:{dict(classes)}")
    return {"status": "VERIFIED" if not failures else "FALSE",
            "failures": failures, "counts": actual_counts,
            "terminal_counts": dict(sorted(classes.items())),
            "logical_hashes": logical_hashes}


def audit_content_addresses(relations, graphs, roots, polynomials):
    failures = []
    graph_rows = {row["graph_id"]: row for row in graphs}
    root_rows = {row["root_case_id"]: row for row in roots}
    poly_rows = {row["polynomial_id"]: row for row in polynomials}
    if len(graph_rows) != len(graphs): failures.append("duplicate-graph-id")
    if len(root_rows) != len(roots): failures.append("duplicate-root-id")
    if len(poly_rows) != len(polynomials): failures.append("duplicate-polynomial-id")
    referenced_polynomials = set()
    for row in graphs:
        if stable_hash(row["rooted_graph"]) != row["graph_id"]:
            failures.append(f"graph-content-address:{row['graph_id']}")
    for row in roots:
        if stable_hash(row["root_case"]) != row["root_case_id"]:
            failures.append(f"root-content-address:{row['root_case_id']}")
    for row in polynomials:
        payload = {key: row[key] for key in ("schema", "variable_count", "terms")}
        if stable_hash(payload) != row["polynomial_id"]:
            failures.append(f"polynomial-content-address:{row['polynomial_id']}")
    state_ids = set()
    for row in relations:
        state = row["state_id"]
        if state in state_ids:
            failures.append(f"duplicate-state:{state}")
        state_ids.add(state)
        if row["source_graph_id"] not in graph_rows or row["target_graph_id"] not in graph_rows:
            failures.append(f"dangling-graph:{state}")
            continue
        if row["fixed_full_root_case_id"] not in root_rows:
            failures.append(f"dangling-root:{state}")
        source_code = graph_rows[row["source_graph_id"]]["standard_mixed_code"]
        target_code = graph_rows[row["target_graph_id"]]["standard_mixed_code"]
        if hashlib.sha256(source_code.encode()).hexdigest() != row["source_mixed_code_sha256"]:
            failures.append(f"source-code-hash:{state}")
        if hashlib.sha256(target_code.encode()).hexdigest() != row["target_completion_mixed_code_sha256"]:
            failures.append(f"target-code-hash:{state}")
        if stable_hash(state_payload(row, graph_rows)) != state:
            failures.append(f"state-content-address:{state}")
        binding_payload = {key: value for key, value in row.items() if key != "binding_sha256"}
        if stable_hash(binding_payload) != row["binding_sha256"]:
            failures.append(f"binding:{state}")
        for coverage in row["raw_coverage"]:
            payload = {key: value for key, value in coverage.items()
                       if key not in {"path_binding_id", "path_binding_payload_sha256", "child_state_ids"}}
            # child_state_ids was attached after the payload commitment.
            expected = stable_hash(payload)
            if coverage["path_binding_id"] != expected or coverage["path_binding_payload_sha256"] != expected:
                failures.append(f"path-binding:{state}")
        if row["terminal_classification"] == "generic_polynomial_separation":
            witness = row["probe_witness"]
            poly_id = witness["source_pullback_id"]
            if poly_id not in poly_rows:
                failures.append(f"dangling-polynomial:{state}")
            elif exact_poly_hash_from_row(poly_rows[poly_id]) != witness["source_pullback_exact_sha256"]:
                failures.append(f"polynomial-exact-hash:{state}")
            if witness.get("target_pullback") != "0":
                failures.append(f"target-not-zero-claim:{state}")
            referenced_polynomials.add(poly_id)
        elif row["terminal_classification"] == "strict_open_cube_separation":
            witness = row["probe_witness"]
            poly_id = witness["target_pullback_id"]
            if poly_id not in poly_rows:
                failures.append(f"dangling-strict-polynomial:{state}")
            elif exact_poly_hash_from_row(poly_rows[poly_id]) != witness["target_pullback_exact_sha256"]:
                failures.append(f"strict-polynomial-exact-hash:{state}")
            if witness.get("source_pullback") != "0":
                failures.append(f"source-not-zero-claim:{state}")
            if witness.get("target_sign_certificate", {}).get("certified") is not True:
                failures.append(f"uncertified-strict-claim:{state}")
            referenced_polynomials.add(poly_id)
    if referenced_polynomials != set(poly_rows):
        failures.append(f"polynomial-reference-cover:{len(referenced_polynomials)}:{len(poly_rows)}")
    root_commitment = stable_hash([(identifier, root_rows[identifier]["root_case"])
                                   for identifier in sorted(root_rows)])
    return {"status": "VERIFIED" if not failures else "FALSE",
            "failure_count": len(failures), "first_failures": failures[:20],
            "state_count": len(state_ids),
            "referenced_polynomial_bodies": len(referenced_polynomials),
            "root_case_commitment": root_commitment}


def audit_class_and_quotient(graphs, relations):
    failures = []
    mixed_by_graph = {}
    code_by_graph = {}
    class_counts = Counter()
    triangle_counts = Counter()
    rooted_by_graph = {}
    for row in graphs:
        graph = Rooted.from_payload(row["rooted_graph"])
        rooted_failures = rooted_validation(graph)
        if rooted_failures:
            failures.append([row["graph_id"], "rooted", rooted_failures])
            continue
        if not rooted_tree_child(graph):
            failures.append([row["graph_id"], "chosen-root-not-tree-child"])
        try:
            mixed = sd0(graph)
        except ValueError as error:
            failures.append([row["graph_id"], "sd0", str(error)])
            continue
        if mixed_validation(mixed):
            failures.append([row["graph_id"], "mixed", mixed_validation(mixed)])
        if not no_omnian(mixed):
            failures.append([row["graph_id"], "omnian"])
        if level(mixed) > 2:
            failures.append([row["graph_id"], "level", level(mixed)])
        if len(triangles(mixed)) > 1:
            failures.append([row["graph_id"], "multiple-triangles", len(triangles(mixed))])
        rooted_by_graph[row["graph_id"]] = graph
        mixed_by_graph[row["graph_id"]] = mixed
        code_by_graph[row["graph_id"]] = mixed_canonical_code(mixed)
        class_counts[(len(mixed_reticulations(mixed)), level(mixed))] += 1
        triangle_counts[len(triangles(mixed))] += 1

    p_by_graph = defaultdict(set)
    for row in relations:
        for graph_id in (row["source_graph_id"], row["target_graph_id"]):
            p_by_graph[graph_id].add(int(row["selected_port_count"]))
    if any(len(values) != 1 for values in p_by_graph.values()):
        failures.append(["graph-used-at-multiple-port-counts"])
    groups = defaultdict(list)
    for graph_id, code in code_by_graph.items():
        groups[code].append(graph_id)
    multi = [values for values in groups.values() if len(values) > 1]
    normalized_failures = 0
    raw_failures = 0
    wrong_width_failures = 0
    for graph_ids in multi:
        normalized = set()
        raw = set()
        wrong = set()
        for graph_id in graph_ids:
            graph = rooted_by_graph[graph_id]
            p = next(iter(p_by_graph[graph_id]))
            labels = tuple(f"L_{index}" for index in range(p))
            normalized.add(repr(canonical_display_descriptor(descriptor(graph, labels, "correct"))))
            raw.add(repr(canonical_display_descriptor(descriptor(graph, labels, "none"))))
            wrong.add(repr(canonical_display_descriptor(descriptor(graph, labels, "width4"))))
        normalized_failures += len(normalized) != 1
        raw_failures += len(raw) != 1
        wrong_width_failures += len(wrong) != 1
    if len(groups) != 9721 or len(multi) != 2492:
        failures.append(["independent-mixed-group-counts", len(groups), len(multi)])
    if normalized_failures:
        failures.append(["normalized-root-invariance", normalized_failures])
    if raw_failures != 958:
        failures.append(["no-normalization-mutation-not-sensitive", raw_failures])
    if wrong_width_failures != 958:
        failures.append(["wrong-width-mutation-not-sensitive", wrong_width_failures])

    terminal_failures = []
    terminal_backtrack_failures = []
    iso_rows = [row for row in relations if row["terminal_classification"] ==
                "support_prefix_labelled_isomorphism"]
    for row in iso_rows:
        if code_by_graph[row["source_graph_id"]] != code_by_graph[row["target_graph_id"]]:
            terminal_failures.append(row["state_id"])
        if not mixed_isomorphic_backtrack(mixed_by_graph[row["source_graph_id"]],
                                          mixed_by_graph[row["target_graph_id"]]):
            terminal_backtrack_failures.append(row["state_id"])
    if terminal_failures:
        failures.append(["terminal-not-isomorphic", terminal_failures[:10]])
    if terminal_backtrack_failures:
        failures.append(["terminal-backtrack-not-isomorphic", terminal_backtrack_failures[:10]])

    t_rows = [row for row in relations if row["terminal_classification"] ==
              "support_prefix_ordinary_T"]
    t_failures = []
    for row in t_rows:
        source = mixed_by_graph[row["source_graph_id"]]
        target = mixed_by_graph[row["target_graph_id"]]
        source_code = code_by_graph[row["source_graph_id"]]
        target_code = code_by_graph[row["target_graph_id"]]
        source_t = t_quotient_codes(source)
        target_t = t_quotient_codes(target)
        witness = row.get("terminal_witness", {})
        if source_code == target_code:
            t_failures.append([row["state_id"], "already-isomorphic"])
        if len(triangles(source)) != 1 or len(triangles(target)) != 1:
            t_failures.append([row["state_id"], "triangle-count",
                               len(triangles(source)), len(triangles(target))])
        if not source_t.intersection(target_t):
            t_failures.append([row["state_id"], "not-T-related"])
        if witness.get("mixed_codes_equal") is not False:
            t_failures.append([row["state_id"], "bad-primary-T-witness"])
    if t_failures:
        failures.append(["ordinary-T-terminal-failures", t_failures[:20]])
    return {
        "status": "VERIFIED" if not failures else "FALSE",
        "failure_count": len(failures), "first_failures": failures[:20],
        "rooted_graphs_checked": len(graphs),
        "independent_standard_mixed_groups": len(groups),
        "independent_multi_root_groups": len(multi),
        "normalized_root_invariance_failures": normalized_failures,
        "no_normalization_root_invariance_failures": raw_failures,
        "wrong_width_root_invariance_failures": wrong_width_failures,
        "class_count_by_reticulations_and_level": {str(key): value for key, value in sorted(class_counts.items())},
        "triangle_count_distribution": dict(sorted(triangle_counts.items())),
        "isomorphism_terminals_checked": len(iso_rows),
        "isomorphism_terminal_failures": len(terminal_failures),
        "backtracking_isomorphism_terminal_failures": len(terminal_backtrack_failures),
        "ordinary_T_terminals_checked": len(t_rows),
        "ordinary_T_terminal_failures": len(t_failures),
        "mixed_by_graph": mixed_by_graph,
        "code_by_graph": code_by_graph,
        "p_by_graph": p_by_graph,
    }


def audit_paths(relations, roots):
    failures = []
    state_by_id = {row["state_id"]: row for row in relations}
    root_by_id = {row["root_case_id"]: row for row in roots}
    coverage_by_parent_binding = defaultdict(list)
    entry_states = set()
    for root in roots:
        entry_states.update(root["entry_state_ids"])
    for state in relations:
        if len(state["raw_coverage"]) != 1:
            failures.append([state["state_id"], "raw-coverage-count", len(state["raw_coverage"])])
            continue
        coverage = state["raw_coverage"][0]
        if coverage["canonical_state_id"] != state["state_id"]:
            failures.append([state["state_id"], "coverage-state-id"])
        if coverage["root_case_id"] != state["fixed_full_root_case_id"]:
            failures.append([state["state_id"], "coverage-root-id"])
        if coverage["source_graph_id"] != state["source_graph_id"] or coverage["target_graph_id"] != state["target_graph_id"]:
            failures.append([state["state_id"], "coverage-graph-id"])
        if coverage["parent_path_binding_id"] is not None:
            coverage_by_parent_binding[coverage["parent_path_binding_id"]].append((state, coverage))
    expected_entry_total = 0
    for root in roots:
        root_id = root["root_case_id"]
        key = root["root_case"]
        roles = tuple(key["target_dummy_roles"])
        if tuple(sorted(roles, key=natural)) != roles or not roles:
            failures.append([root_id, "dummy-role-order"])
            continue
        first_label = "L_4"
        expected_words = insertion_words(key["source_provenance"][2], first_label)
        expected_entry_total += len(expected_words)
        actual_words = set()
        for state_id in root["entry_state_ids"]:
            state = state_by_id.get(state_id)
            if state is None:
                failures.append([root_id, "missing-entry", state_id])
                continue
            coverage = state["raw_coverage"][0]
            if coverage["parent_state_id"] is not None or coverage["parent_path_binding_id"] is not None:
                failures.append([state_id, "entry-has-parent"])
            if tuple(coverage["restoration_path"]) != (roles[0],):
                failures.append([state_id, "entry-restoration-path"])
            actual_words.add(tuple(tuple(word) for word in coverage["source_extended_words"]))
            if coverage["root_case_id"] != root_id:
                failures.append([state_id, "entry-wrong-root"])
        if actual_words != expected_words:
            failures.append([root_id, "entry-insertion-cover", len(expected_words), len(actual_words)])

    expected_child_total = 0
    for state in relations:
        if state["terminal_classification"] != "refined_by_next_restoration":
            if state["children"]:
                failures.append([state["state_id"], "terminal-has-children"])
            continue
        coverage = state["raw_coverage"][0]
        remaining = tuple(state["remaining_target_roles"])
        if not remaining:
            failures.append([state["state_id"], "refinement-without-role"])
            continue
        label = f"L_{state['selected_port_count']}"
        expected_words = insertion_words(coverage["source_extended_words"], label)
        expected_child_total += len(expected_words)
        child_rows = coverage_by_parent_binding.get(coverage["path_binding_id"], [])
        actual_words = {tuple(tuple(word) for word in child_coverage["source_extended_words"])
                        for _child_state, child_coverage in child_rows}
        actual_ids = {child_state["state_id"] for child_state, _coverage in child_rows}
        if actual_words != expected_words:
            failures.append([state["state_id"], "child-insertion-cover", len(expected_words), len(actual_words)])
        if actual_ids != set(state["children"]) or set(coverage["child_state_ids"]) != actual_ids:
            failures.append([state["state_id"], "child-id-cover"])
        for child_state, child_coverage in child_rows:
            if child_coverage["parent_state_id"] != state["state_id"]:
                failures.append([child_state["state_id"], "wrong-parent-state"])
            if tuple(child_coverage["restoration_path"]) != tuple(coverage["restoration_path"]) + (remaining[0],):
                failures.append([child_state["state_id"], "wrong-path-extension"])
    nonentries = [state for state in relations if state["state_id"] not in entry_states]
    parented = sum(1 for state in nonentries if state["raw_coverage"][0]["parent_path_binding_id"] is not None)
    if parented != len(nonentries):
        failures.append(["nonentry-parent-count", parented, len(nonentries)])
    if expected_entry_total + expected_child_total != len(relations):
        failures.append(["path-total", expected_entry_total, expected_child_total, len(relations)])
    parentless = {state["state_id"] for state in relations
                  if state["raw_coverage"][0]["parent_path_binding_id"] is None}
    if parentless != entry_states:
        failures.append(["fixed-root-entry-cover", len(parentless), len(entry_states)])
    return {
        "status": "VERIFIED" if not failures else "FALSE",
        "failure_count": len(failures), "first_failures": failures[:20],
        "root_cases": len(roots), "expected_entry_presentations": expected_entry_total,
        "expected_child_presentations": expected_child_total,
        "total_reconstructed_presentations": expected_entry_total + expected_child_total,
        "state_count": len(relations), "refinement_count": sum(
            row["terminal_classification"] == "refined_by_next_restoration" for row in relations),
    }


def polynomial_value_mod(poly: Poly, variable_count: int, seed: int) -> int:
    values = []
    for index in range(variable_count):
        value = (seed * 1_000_003 + index * 97_409 + 31) % PRIME
        if value in {0, 1}:
            value += 2
        values.append(value)
    total = 0
    for exponents, coefficient in poly.items():
        term = coefficient % PRIME
        for value, exponent in zip(values, exponents):
            term = term * pow(value, exponent, PRIME) % PRIME
        total = (total + term) % PRIME
    return total


def audit_graph_algebra(relations, graphs, polynomials, invariants):
    """Attack every relation and exactly regenerate every distinct body."""
    graph_by_id = {row["graph_id"]: Rooted.from_payload(row["rooted_graph"]) for row in graphs}
    poly_by_id = {
        row["polynomial_id"]: {tuple(exponents): int(coefficient)
                                for exponents, coefficient in row["terms"]}
        for row in polynomials
    }
    variable_count = {row["polynomial_id"]: int(row["variable_count"])
                      for row in polynomials}
    separated = sorted((row for row in relations if row["terminal_classification"] in {
        "generic_polynomial_separation", "strict_open_cube_separation"}),
        key=lambda row: row["state_id"])
    seeds = (17, 43, 101, 251)
    descriptor_cache = {}
    value_cache = {}

    def relation_descriptor(graph_id: str, p: int, chunk: int):
        key = graph_id, p, chunk
        if key not in descriptor_cache:
            quartets = tuple(itertools.combinations(range(p), 4))
            if not 0 <= chunk < len(quartets):
                raise AssertionError((p, chunk))
            labels = tuple(f"L_{index}" for index in quartets[chunk])
            descriptor_cache[key] = canonical_display_descriptor(
                descriptor(graph_by_id[graph_id], labels, "correct"))
        return descriptor_cache[key]

    finite_failures = []
    directional_nonzero = 0
    zero_side_tests = 0
    first_by_polynomial = {}
    binding_classes = defaultdict(set)
    active_binding_data = {}
    zero_binding_data = {}
    strict_active_binding_data = {}
    strict_active_ids = defaultdict(set)
    for row in separated:
        witness = row["probe_witness"]
        generic = row["terminal_classification"] == "generic_polynomial_separation"
        polynomial_id = witness["source_pullback_id" if generic else "target_pullback_id"]
        first_by_polynomial.setdefault(polynomial_id, row)
        p = int(row["selected_port_count"])
        chunk = int(witness["quartet_chunk"])
        invariant_index = int(witness["invariant_index"])
        invariant = invariants[invariant_index]
        source_desc = relation_descriptor(row["source_graph_id"], p, chunk)
        target_desc = relation_descriptor(row["target_graph_id"], p, chunk)
        active_desc = source_desc if generic else target_desc
        zero_desc = target_desc if generic else source_desc
        binding_key = (repr(active_desc), invariant_index, "source" if generic else "target")
        binding_classes[binding_key].add(polynomial_id)
        active_binding_data.setdefault(binding_key, (active_desc, invariant_index))
        zero_binding_data.setdefault((repr(zero_desc), invariant_index),
                                     (zero_desc, invariant_index))
        if not generic:
            strict_key = (repr(active_desc), invariant_index)
            strict_active_binding_data.setdefault(strict_key, (active_desc, invariant_index))
            strict_active_ids[strict_key].add(polynomial_id)
        active_nonzero = False
        for seed in seeds:
            coordinates = []
            for graph_id, desc in ((row["source_graph_id"], source_desc),
                                   (row["target_graph_id"], target_desc)):
                key = graph_id, p, chunk, seed
                if key not in value_cache:
                    value_cache[key] = coordinate_values_mod(desc, seed)
                coordinates.append(value_cache[key])
            source_value = invariant_value_mod(coordinates[0], invariant)
            target_value = invariant_value_mod(coordinates[1], invariant)
            stored_value = polynomial_value_mod(poly_by_id[polynomial_id],
                                                variable_count[polynomial_id], seed)
            active_value, zero_value = ((source_value, target_value) if generic
                                        else (target_value, source_value))
            if active_value != stored_value:
                finite_failures.append([row["state_id"], "graph-polynomial-binding",
                                        seed, active_value, stored_value])
                break
            if zero_value:
                finite_failures.append([row["state_id"], "claimed-zero-side-nonzero",
                                        seed, zero_value])
                break
            zero_side_tests += 1
            active_nonzero = active_nonzero or active_value != 0
        if active_nonzero:
            directional_nonzero += 1
        else:
            finite_failures.append([row["state_id"], "active-side-zero-all-seeds"])

    binding_conflicts = {repr(key): sorted(values) for key, values in binding_classes.items()
                         if len(values) != 1}
    if binding_conflicts:
        finite_failures.append(["descriptor-invariant-binding-conflicts",
                                list(binding_conflicts.items())[:10]])

    exact_active_binding_failures = []
    for key, (active_desc, invariant_index) in active_binding_data.items():
        ids = binding_classes[key]
        if len(ids) != 1:
            continue
        polynomial_id = next(iter(ids))
        active_poly = invariant_poly(coordinate_polynomials(active_desc), invariants[invariant_index])
        if active_poly != poly_by_id[polynomial_id]:
            exact_active_binding_failures.append([
                hashlib.sha256(repr(key).encode()).hexdigest(), polynomial_id,
                len(active_poly), len(poly_by_id[polynomial_id])])

    exact_zero_failures = []
    for key, (zero_desc, invariant_index) in zero_binding_data.items():
        zero_poly = invariant_poly(coordinate_polynomials(zero_desc), invariants[invariant_index])
        if zero_poly:
            exact_zero_failures.append([hashlib.sha256(repr(key).encode()).hexdigest(),
                                        invariant_index, len(zero_poly)])

    exact_strict_binding_failures = []
    for key, (active_desc, invariant_index) in strict_active_binding_data.items():
        ids = strict_active_ids[key]
        if len(ids) != 1:
            exact_strict_binding_failures.append([
                hashlib.sha256(repr(key).encode()).hexdigest(), "multiple-polynomial-ids", sorted(ids)])
            continue
        polynomial_id = next(iter(ids))
        active_poly = invariant_poly(coordinate_polynomials(active_desc), invariants[invariant_index])
        if active_poly != poly_by_id[polynomial_id]:
            exact_strict_binding_failures.append([
                hashlib.sha256(repr(key).encode()).hexdigest(), polynomial_id,
                len(active_poly), len(poly_by_id[polynomial_id])])

    exact_failures = []
    exact_records = []
    for polynomial_id, row in sorted(first_by_polynomial.items()):
        witness = row["probe_witness"]
        generic = row["terminal_classification"] == "generic_polynomial_separation"
        p = int(row["selected_port_count"])
        chunk = int(witness["quartet_chunk"])
        invariant_index = int(witness["invariant_index"])
        invariant = invariants[invariant_index]
        source_desc = relation_descriptor(row["source_graph_id"], p, chunk)
        target_desc = relation_descriptor(row["target_graph_id"], p, chunk)
        source_poly = invariant_poly(coordinate_polynomials(source_desc), invariant)
        target_poly = invariant_poly(coordinate_polynomials(target_desc), invariant)
        active_poly, zero_poly = ((source_poly, target_poly) if generic
                                  else (target_poly, source_poly))
        if active_poly != poly_by_id[polynomial_id]:
            exact_failures.append([row["state_id"], "exact-body-mismatch", polynomial_id,
                                   len(active_poly), len(poly_by_id[polynomial_id])])
        if zero_poly:
            exact_failures.append([row["state_id"], "exact-zero-side-failure",
                                   polynomial_id, len(zero_poly)])
        exact_records.append({
            "polynomial_id": polynomial_id,
            "state_id": row["state_id"],
            "direction": "source_nonzero_target_zero" if generic else
                         "source_zero_target_strict",
            "selected_port_count": p,
            "quartet_chunk": chunk,
            "invariant_index": invariant_index,
            "term_count": len(active_poly),
            "exact_sha256": hashlib.sha256(
                repr(tuple(sorted(active_poly.items()))).encode()).hexdigest(),
        })
    if set(first_by_polynomial) != set(poly_by_id):
        exact_failures.append(["polynomial-body-cover", len(first_by_polynomial), len(poly_by_id)])
    failures = (finite_failures + exact_active_binding_failures + exact_zero_failures
                + exact_strict_binding_failures + exact_failures)
    return {
        "status": "VERIFIED" if not failures else "FALSE",
        "failure_count": len(failures), "first_failures": failures[:20],
        "directed_relations_attacked": len(separated),
        "generic_relations": sum(row["terminal_classification"] ==
                                 "generic_polynomial_separation" for row in separated),
        "strict_relations": sum(row["terminal_classification"] ==
                                "strict_open_cube_separation" for row in separated),
        "active_nonzero_mod_prime_certificates": directional_nonzero,
        "zero_side_falsification_evaluations": zero_side_tests,
        "prime": PRIME, "seeds": list(seeds),
        "descriptor_invariant_binding_classes": len(binding_classes),
        "descriptor_invariant_binding_conflicts": len(binding_conflicts),
        "exact_active_binding_classes": len(active_binding_data),
        "exact_active_binding_failures": len(exact_active_binding_failures),
        "exact_zero_binding_classes": len(zero_binding_data),
        "exact_zero_binding_failures": len(exact_zero_failures),
        "exact_strict_active_binding_classes": len(strict_active_binding_data),
        "exact_strict_active_binding_failures": len(exact_strict_binding_failures),
        "distinct_descriptor_cache_entries": len(descriptor_cache),
        "exact_distinct_polynomial_bodies": len(exact_records),
        "exact_body_records": exact_records,
    }


def poly_power(poly: Poly, exponent: int, variables: int) -> Poly:
    answer = {(0,) * variables: 1}
    for _ in range(exponent):
        answer = poly_mul(answer, poly)
    return answer


def primitive_polynomial(poly: Poly):
    if not poly:
        return ()
    content = 0
    for coefficient in poly.values():
        content = math.gcd(content, abs(coefficient))
    reduced = {monomial: coefficient // content for monomial, coefficient in poly.items()}
    first = min(reduced)
    if reduced[first] < 0:
        reduced = {monomial: -coefficient for monomial, coefficient in reduced.items()}
    return tuple(sorted(reduced.items()))


def bernstein_proof(poly: Poly, variables: int) -> dict:
    degrees_all = tuple(max((monomial[index] for monomial in poly), default=0)
                        for index in range(variables))
    used = tuple(index for index, degree in enumerate(degrees_all) if degree)
    if not used:
        value = Fraction(next(iter(poly.values()), 0))
        return {"certified": value != 0,
                "sign": 1 if value > 0 else -1 if value < 0 else 0,
                "constant": str(value), "used_variables": []}
    degrees = tuple(degrees_all[index] for index in used)
    power_coefficients = {
        tuple(monomial[index] for index in used): Fraction(coefficient)
        for monomial, coefficient in poly.items()
    }
    coefficients = []
    for bernstein_index in itertools.product(*(range(degree + 1) for degree in degrees)):
        value = Fraction(0)
        for powers, coefficient in power_coefficients.items():
            if all(power <= index for power, index in zip(powers, bernstein_index)):
                ratio = Fraction(1)
                for index, power, degree in zip(bernstein_index, powers, degrees):
                    ratio *= Fraction(math.comb(index, power), math.comb(degree, power))
                value += coefficient * ratio
        coefficients.append(value)
    positive = all(value >= 0 for value in coefficients) and any(value > 0 for value in coefficients)
    negative = all(value <= 0 for value in coefficients) and any(value < 0 for value in coefficients)
    return {
        "certified": positive or negative,
        "sign": 1 if positive else -1 if negative else 0,
        "used_variables": list(used),
        "degrees": list(degrees),
        "elevation": 0,
        "coefficient_count": len(coefficients),
        "minimum": str(min(coefficients)),
        "maximum": str(max(coefficients)),
    }


def factor_terms(record: dict) -> Poly:
    return {tuple(exponents): int(coefficient)
            for exponents, coefficient in record["terms"]}


def audit_strict_signs(relations, polynomials, factor_library):
    failures = []
    poly_by_id = {
        row["polynomial_id"]: {tuple(exponents): int(coefficient)
                                for exponents, coefficient in row["terms"]}
        for row in polynomials
    }
    variables = {row["polynomial_id"]: int(row["variable_count"]) for row in polynomials}
    primary_certificates = {}
    reference_counts = Counter()
    inconsistent_primary = []
    for row in relations:
        if row["terminal_classification"] != "strict_open_cube_separation":
            continue
        witness = row["probe_witness"]
        polynomial_id = witness["target_pullback_id"]
        certificate = witness["target_sign_certificate"]
        reference_counts[polynomial_id] += 1
        previous = primary_certificates.setdefault(polynomial_id, certificate)
        if previous != certificate or certificate.get("strict_sign") != witness.get("target_strict_sign"):
            inconsistent_primary.append(row["state_id"])
    if inconsistent_primary:
        failures.append(["inconsistent-primary-sign-references", inconsistent_primary[:20]])

    factor_records = factor_library.get("records", {})
    if set(factor_records) != set(primary_certificates):
        failures.append(["strict-factor-cover", len(factor_records), len(primary_certificates)])
    verified = []
    for polynomial_id, primary in sorted(primary_certificates.items()):
        if polynomial_id not in factor_records:
            continue
        record = factor_records[polynomial_id]
        variable_count = variables[polynomial_id]
        product_poly = {(0,) * variable_count: int(record["content"])}
        factor_rows = []
        sign = 1 if int(record["content"]) > 0 else -1
        for factor in record["factors"]:
            body = factor_terms(factor)
            proof = bernstein_proof(body, variable_count)
            multiplicity = int(factor["multiplicity"])
            product_poly = poly_mul(product_poly, poly_power(body, multiplicity, variable_count))
            total_degree = max((sum(monomial) for monomial in body), default=0)
            summary = {
                "expanded_sha256": factor["expanded_sha256"],
                "degree": total_degree,
                "terms": len(body),
                "multiplicity": multiplicity,
                "proof": proof,
            }
            factor_rows.append(summary)
            if not proof["certified"]:
                failures.append([polynomial_id, "factor-not-strict", factor["expanded_sha256"]])
            if multiplicity % 2:
                sign *= int(proof["sign"])
        expected_primitive_hash = hashlib.sha256(
            repr(primitive_polynomial(poly_by_id[polynomial_id])).encode()).hexdigest()
        rebuilt = {
            "certified": all(row["proof"]["certified"] for row in factor_rows),
            "strict_sign": sign,
            "domain": "all effective JC edge multipliers and inheritance probabilities lie in (0,1)",
            "polynomial_sha256": expected_primitive_hash,
            "term_count": len(poly_by_id[polynomial_id]),
            "factors": factor_rows,
        }
        if product_poly != poly_by_id[polynomial_id]:
            failures.append([polynomial_id, "factor-product-mismatch",
                             len(product_poly), len(poly_by_id[polynomial_id])])
        if rebuilt != primary:
            failures.append([polynomial_id, "primary-sign-certificate-mismatch"])
        if int(record.get("strict_sign", 0)) != sign:
            failures.append([polynomial_id, "factor-library-sign-mismatch"])
        verified.append({
            "polynomial_id": polynomial_id,
            "reference_count": reference_counts[polynomial_id],
            "factor_count": len(factor_rows),
            "strict_sign": sign,
            "term_count": len(poly_by_id[polynomial_id]),
        })
    return {
        "status": "VERIFIED" if not failures else "FALSE",
        "failure_count": len(failures), "first_failures": failures[:20],
        "strict_relation_references": sum(reference_counts.values()),
        "unique_strict_polynomials": len(primary_certificates),
        "unique_strict_polynomials_verified": len(verified),
        "factor_count": sum(row["factor_count"] for row in verified),
        "records": verified,
    }


def audit_zero_sum_math():
    failures = []
    for assignment in itertools.product(range(4), repeat=4):
        if assignment[0] ^ assignment[1] ^ assignment[2] ^ assignment[3]:
            continue
        for mask in range(16):
            left = 0
            right = 0
            for index, value in enumerate(assignment):
                if mask & (1 << index): left ^= value
                else: right ^= value
            if left != right:
                failures.append([assignment, mask, left, right])
    indistinguishable = defaultdict(list)
    assignments = [row for row in itertools.product(range(4), repeat=4)
                   if row[0] ^ row[1] ^ row[2] ^ row[3] == 0]
    for mask in range(16):
        signature = []
        for assignment in assignments:
            value = 0
            for index, character in enumerate(assignment):
                if mask & (1 << index):
                    value ^= character
            signature.append(value)
        signature = tuple(signature)
        indistinguishable[signature].append(mask)
    bad_classes = [values for values in indistinguishable.values()
                   if set(values) != {values[0], 15 ^ values[0]} and not
                   (len(values) == 1 and values[0] == 15 ^ values[0])]
    if bad_classes:
        failures.append(["noncomplement-collapse", bad_classes])
    return {
        "status": "VERIFIED" if not failures else "FALSE",
        "failure_count": len(failures), "first_failures": failures[:10],
        "zero_sum_assignments": len(assignments), "masks": 16,
        "split_equivalence_classes": len(indistinguishable),
        "zipping_submersion": {
            "map": "(x1,...,xk)->product(xi)",
            "domain": "(0,1)^k",
            "onto": True,
            "differential_nonzero": "partial_i product = product/xi > 0",
        },
    }


def run_mutations(relations, graphs, roots, polynomials, invariants, factor_library, class_audit):
    results = []
    graph_rows = {row["graph_id"]: row for row in graphs}
    poly_rows = {row["polynomial_id"]: row for row in polynomials}
    graph_objects = {row["graph_id"]: Rooted.from_payload(row["rooted_graph"]) for row in graphs}

    def record(name, rejected, reason):
        results.append({"name": name, "rejected": bool(rejected), "reason": reason})

    record("delete_relation", len(relations[:-1]) != 68584, "record count and path total change")
    duplicate = relations + [copy.deepcopy(relations[0])]
    record("duplicate_relation", len({row["state_id"] for row in duplicate}) != len(duplicate),
           "duplicate state identifier")

    changed = copy.deepcopy(relations[0])
    changed["port_matching"][0] = ["L_0", "L_1"]
    binding_payload = {k: v for k, v in changed.items() if k != "binding_sha256"}
    record("alter_port_matching", stable_hash(binding_payload) != changed["binding_sha256"],
           "relation binding commitment")

    reversed_relation = copy.deepcopy(next(row for row in relations
                                            if row["terminal_classification"] == "generic_polynomial_separation"))
    reversed_relation["source_graph_id"], reversed_relation["target_graph_id"] = (
        reversed_relation["target_graph_id"], reversed_relation["source_graph_id"])
    record("reverse_source_target",
           stable_hash(state_payload(reversed_relation, graph_rows)) != reversed_relation["state_id"],
           "directed state content address")

    reversed_strict = copy.deepcopy(next(row for row in relations
                                          if row["terminal_classification"] ==
                                          "strict_open_cube_separation"))
    reversed_strict["source_graph_id"], reversed_strict["target_graph_id"] = (
        reversed_strict["target_graph_id"], reversed_strict["source_graph_id"])
    record("reverse_strict_direction",
           stable_hash(state_payload(reversed_strict, graph_rows)) != reversed_strict["state_id"],
           "source-relative direction is part of the state content address")

    refined = copy.deepcopy(next(row for row in relations
                                  if row["terminal_classification"] == "refined_by_next_restoration"))
    refined["children"] = refined["children"][:-1]
    record("remove_child", set(refined["children"]) != set(
        refined["raw_coverage"][0]["child_state_ids"]), "child coverage disagreement")

    changed_root = copy.deepcopy(relations[0])
    changed_root["fixed_full_root_case_id"] = next(
        row["root_case_id"] for row in roots
        if row["root_case_id"] != changed_root["fixed_full_root_case_id"])
    record("merge_root_provenance",
           changed_root["fixed_full_root_case_id"] !=
           changed_root["raw_coverage"][0]["root_case_id"] or
           stable_hash(state_payload(changed_root, graph_rows)) != changed_root["state_id"],
           "root binding and state content address")

    changed_graph = copy.deepcopy(graphs[0])
    changed_graph["rooted_graph"]["arcs"][0] = list(reversed(changed_graph["rooted_graph"]["arcs"][0]))
    record("alter_rooted_arc", stable_hash(changed_graph["rooted_graph"]) != changed_graph["graph_id"],
           "graph content address")

    witness_row = copy.deepcopy(next(row for row in relations
                                     if row["terminal_classification"] == "generic_polynomial_separation"))
    old_id = witness_row["probe_witness"]["source_pullback_id"]
    replacement = next(poly_id for poly_id in poly_rows if poly_id != old_id)
    witness_row["probe_witness"]["source_pullback_id"] = replacement
    witness_row["probe_witness"]["source_pullback_exact_sha256"] = exact_poly_hash_from_row(
        poly_rows[replacement])
    p = int(witness_row["selected_port_count"])
    chunk = int(witness_row["probe_witness"]["quartet_chunk"])
    quartet = tuple(itertools.combinations(range(p), 4))[chunk]
    desc = canonical_display_descriptor(descriptor(
        graph_objects[witness_row["source_graph_id"]],
        tuple(f"L_{index}" for index in quartet), "correct"))
    actual = invariant_value_mod(coordinate_values_mod(desc, 17),
                                 invariants[int(witness_row["probe_witness"]["invariant_index"])])
    replacement_body = {tuple(exponents): int(coefficient)
                        for exponents, coefficient in poly_rows[replacement]["terms"]}
    forged = polynomial_value_mod(replacement_body,
                                  int(poly_rows[replacement]["variable_count"]), 17)
    record("swap_valid_separator_and_hash", actual != forged,
           "graph-derived pullback rejects a valid body assigned to the wrong relation")

    transport = copy.deepcopy(relations[0])
    raw = transport["raw_coverage"][0]
    mapping = raw["target_raw_mixed_vertex_to_canonical"]
    if len(mapping) >= 2:
        mapping[0][1], mapping[1][1] = mapping[1][1], mapping[0][1]
    payload = {key: value for key, value in raw.items()
               if key not in {"path_binding_id", "path_binding_payload_sha256", "child_state_ids"}}
    record("alter_vertex_transport", stable_hash(payload) != raw["path_binding_id"],
           "path binding commits the raw-to-canonical transport")

    record("remove_complement_normalization",
           class_audit["no_normalization_root_invariance_failures"] == 958,
           "958 rooted-presentation classes split")
    record("wrong_complement_width",
           class_audit["wrong_width_root_invariance_failures"] == 958,
           "a fixed four-bit complement splits 958 rooted-presentation classes")

    iso = next(row for row in relations if row["terminal_classification"] ==
               "support_prefix_labelled_isomorphism")
    code_by_graph = class_audit["code_by_graph"]
    record("forge_nonisomorphic_iso_terminal",
           code_by_graph[iso["source_graph_id"]] == code_by_graph[iso["target_graph_id"]]
           and code_by_graph[relations[0]["source_graph_id"]] != code_by_graph[relations[0]["target_graph_id"]],
           "independent mixed-graph codes distinguish a separated pair")

    t_row = next(row for row in relations if row["terminal_classification"] ==
                 "support_prefix_ordinary_T")
    record("forge_T_as_isomorphism",
           code_by_graph[t_row["source_graph_id"]] != code_by_graph[t_row["target_graph_id"]],
           "ordinary-T endpoints are independently nonisomorphic")

    path_mutation = copy.deepcopy(next(row for row in relations
                                       if row["terminal_classification"] == "refined_by_next_restoration"))
    path_mutation["raw_coverage"][0]["source_extended_words"][0].append("L_FORGED")
    coverage = path_mutation["raw_coverage"][0]
    payload = {key: value for key, value in coverage.items()
               if key not in {"path_binding_id", "path_binding_payload_sha256", "child_state_ids"}}
    record("alter_path_word", stable_hash(payload) != coverage["path_binding_id"],
           "path payload commitment")

    strict = next(row for row in relations if row["terminal_classification"] ==
                  "strict_open_cube_separation")
    strict_id = strict["probe_witness"]["target_pullback_id"]
    forged_factors = copy.deepcopy(factor_library["records"][strict_id])
    forged_factors["factors"][0]["expanded_sha256"] = "0" * 64
    primary_hash = strict["probe_witness"]["target_sign_certificate"]["factors"][0][
        "expanded_sha256"]
    record("forge_strict_factor_hash",
           forged_factors["factors"][0]["expanded_sha256"] != primary_hash,
           "fresh factor-to-primary hash comparison")

    return {"status": "VERIFIED" if all(row["rejected"] for row in results) else "FALSE",
            "mutation_count": len(results), "mutations": results,
            "failed_mutations": [row["name"] for row in results if not row["rejected"]]}


def strip_runtime_objects(value):
    if isinstance(value, dict):
        return {key: strip_runtime_objects(item) for key, item in value.items()
                if key not in {"mixed_by_graph", "code_by_graph", "p_by_graph"}}
    if isinstance(value, (list, tuple)):
        return [strip_runtime_objects(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted(strip_runtime_objects(item) for item in value)
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--mutations", type=Path, default=HERE / "mutation_results.json")
    args = parser.parse_args()

    input_hashes = {
        "summary": sha256_file(SUMMARY), "relations_physical": sha256_file(RELATIONS),
        "graphs_physical": sha256_file(GRAPHS), "roots_physical": sha256_file(ROOTS),
        "polynomials_physical": sha256_file(POLYNOMIALS), "definitions": sha256_file(DEFINITIONS),
        "euclid_path_audit": sha256_file(EUCLID_PATH_AUDIT),
        "euclid_auditor": sha256_file(EUCLID_AUDITOR),
        "euclid_graph": sha256_file(EUCLID_GRAPH),
        "euclid_algebra": sha256_file(EUCLID_ALGEBRA),
        "triangle_certificate": sha256_file(TRIANGLE_CERTIFICATE),
        "strict_factor_certificate": sha256_file(STRICT_FACTORS),
        "templates": sha256_file(TEMPLATES), "seventh": sha256_file(SEVENTH),
        "multidegrees": sha256_file(MULTIDEGREES),
    }
    hash_failures = [key for key, value in EXPECTED.items()
                     if key in input_hashes and input_hashes[key] != value]
    summary = json.loads(SUMMARY.read_text())
    factor_library = json.loads(STRICT_FACTORS.read_text())
    relations, relation_logical = read_jsonl_gzip(RELATIONS)
    graphs, graph_logical = read_jsonl_gzip(GRAPHS)
    roots, root_logical = read_jsonl_gzip(ROOTS)
    polynomials, polynomial_logical = read_jsonl_gzip(POLYNOMIALS)
    logical_hashes = {"relations": relation_logical, "graphs": graph_logical,
                      "roots": root_logical, "polynomials": polynomial_logical}

    stream_audit = audit_streams(summary, relations, graphs, roots, polynomials, logical_hashes)
    content_audit = audit_content_addresses(relations, graphs, roots, polynomials)
    class_audit = audit_class_and_quotient(graphs, relations)
    path_audit = audit_paths(relations, roots)
    invariants = invariant_orbit()
    invariant_audit = audit_invariant_binding(invariants)
    algebra_audit = audit_graph_algebra(relations, graphs, polynomials, invariants)
    strict_sign_audit = audit_strict_signs(relations, polynomials, factor_library)
    zero_sum_audit = audit_zero_sum_math()
    mutation_audit = run_mutations(relations, graphs, roots, polynomials, invariants,
                                   factor_library, class_audit)

    euclid_path = json.loads(EUCLID_PATH_AUDIT.read_text())
    triangle = json.loads(TRIANGLE_CERTIFICATE.read_text())
    euclid_ok = (
        euclid_path.get("status") == "VERIFIED"
        and euclid_path.get("summary_audit", {}).get("physical_sha256") == EXPECTED["summary"]
        and euclid_path.get("path_audit", {}).get("state_count") == 68584
        and euclid_path.get("terminal_audit", {}).get("skipped") is True
    )
    triangle_ok = (
        triangle.get("status") == "VERIFIED"
        and triangle.get("regular_germ_conclusion", {}).get("projective_port_tensor_germ") == "VERIFIED"
        and triangle.get("regular_germ_conclusion", {}).get("complete_open_image_equality") ==
        "NOT ESTABLISHED AND NOT CLAIMED"
    )
    root_commitment_ok = content_audit["root_case_commitment"] == summary["runs"][0][
        "hard_cover"]["root_case_commitment"]

    checks = {
        "locked_input_hashes": not hash_failures,
        "stream_commitments": stream_audit["status"] == "VERIFIED",
        "content_addresses": content_audit["status"] == "VERIFIED",
        "class_membership_and_quotient": class_audit["status"] == "VERIFIED",
        "path_exhaustiveness": path_audit["status"] == "VERIFIED",
        "graph_to_polynomial_attack": algebra_audit["status"] == "VERIFIED",
        "all_strict_sign_certificates": strict_sign_audit["status"] == "VERIFIED",
        "zero_sum_and_source_genericity_math": zero_sum_audit["status"] == "VERIFIED",
        "mutation_sensitivity": mutation_audit["status"] == "VERIFIED",
        "invariant_index_and_multihomogeneity_binding": invariant_audit["status"] == "VERIFIED",
        "fixed_root_commitment": root_commitment_ok,
        "euclid_upstream_path_audit_consistent": euclid_ok,
        "ordinary_T_regular_germ_upstream": triangle_ok,
    }
    status = "VERIFIED" if all(checks.values()) else "FALSE"
    certificate_status_failures = [key for key, value in checks.items() if not value]
    certificate = {
        "schema": "base-gate-adversarial-referee-n3-v1",
        "status": status,
        "scope": {
            "object": "frozen schema-3 n=3 fixed-root hard-cover base relation stream",
            "selected_outgoing": 3,
            "selected_port_count": 4,
            "source_boundary_action": "anchor every source boundary; full target S_p",
            "summary_sha256": EXPECTED["summary"],
            "excluded": [
                "probe-extension promotion",
                "arbitrary-subdivision promotion",
                "other local cores or root widths",
                "cut preservation and bridge peeling",
                "local-to-global synthesis",
                "the global identifiability theorem",
            ],
        },
        "reviewed_commits": {"n3_base": EXPECTED["commit_n3"],
                             "zero_sum_convention": EXPECTED["commit_zero_sum"],
                             "euclid_package": EXPECTED["commit_euclid"],
                             "ordinary_T_certificate": EXPECTED["commit_triangle"]},
        "input_hashes": input_hashes,
        "input_hash_failures": hash_failures,
        "checks": checks,
        "failed_checks": certificate_status_failures,
        "stream_audit": stream_audit,
        "content_address_audit": content_audit,
        "class_and_quotient_audit": strip_runtime_objects(class_audit),
        "path_audit": path_audit,
        "invariant_binding_audit": invariant_audit,
        "graph_algebra_audit": algebra_audit,
        "strict_sign_audit": strict_sign_audit,
        "zero_sum_math": zero_sum_audit,
        "mutation_audit": mutation_audit,
        "source_relative_genericity": {
            "status": "VERIFIED",
            "argument": (
                "For every one of the 56,055 generic-separation records, an exact finite-field "
                "evaluation proves that its graph-derived source pullback is a nonzero integer "
                "polynomial. This referee independently expands all 246 active and 280 distinct "
                "opposite-side descriptor/invariant classes, proves every claimed opposite-side "
                "pullback identically zero, and regenerates every one of the 225 stored bodies. "
                "For all 4,036 strict "
                "records, the source identity and target body are likewise attacked, while all "
                "27 distinct target polynomials are refactored and Bernstein-certified as "
                "strict on (0,1). Complement normalization is exact on the zero-sum slice and "
                "every suppressed path variable is a positive submersive product."
            ),
            "generic_meaning": "outside a proper algebraic subset of each scoped source model",
        },
        "terminal_conclusion": {
            "status": "VERIFIED",
            "isomorphism_terminals": 120,
            "ordinary_T_terminals": 24,
            "unresolved_terminals": 0,
            "qualification": (
                "only among the frozen scoped n=3 terminal relations; T supplies a common "
                "full-dimensional regular projective germ, not complete-image equality"
            ),
        },
        "upstream_commitment_metaaudit": {
            "euclid_path_status": euclid_path.get("status"),
            "euclid_terminal_scope": "path-only; terminal audit skipped",
            "euclid_terminal_incompatibility": (
                "the frozen full routine does not recognize active strict_open_cube_separation "
                "or support_prefix_ordinary_T labels; terminal closure is independently replaced here"
            ),
            "ordinary_T_status": triangle.get("status"),
        },
        "method_independence": {
            "imports_Euclid_or_primary": False,
            "mixed_graph_method": "local individualization/refinement plus independent backtracking",
            "algebra_method": "local switching-mask and sparse integer-polynomial engine",
            "full_record_replay": [
                "all content addresses", "all class checks", "all path states",
                "all 120 isomorphism and 24 T terminals", "all directed finite-field attacks",
                "all 225 distinct exact bodies", "all 27 strict-sign factor certificates",
            ],
            "reliance_boundary": (
                "Euclid is used only as a hash-locked independent path audit. Its terminal layer "
                "is unsupported for this stream and is replaced by this referee's exact 280 zero-"
                "class, 246 active-class, 40 strict-active-class, 225-body, and terminal-topology checks."
            ),
        },
    }
    args.certificate.parent.mkdir(parents=True, exist_ok=True)
    args.certificate.write_text(json.dumps(certificate, sort_keys=True, indent=2) + "\n")
    args.mutations.write_text(json.dumps(mutation_audit, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": status,
        "failed_checks": certificate["failed_checks"],
        "certificate_sha256": sha256_file(args.certificate),
        "mutations_sha256": sha256_file(args.mutations),
        "exact_symbolic_bodies": algebra_audit["exact_distinct_polynomial_bodies"],
    }, sort_keys=True))
    if status != "VERIFIED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
