#!/usr/bin/env python3
"""Independent graph audit for the proposed JC Omega move.

This file intentionally does not import any discovery-project module.  It reads
only the published machine-readable certificate and rebuilds validation,
standard semi-directed reduction, mixed-graph canonicalization, blob/cycle
statistics, and admissible rooting enumeration from the Python standard
library.

An edge is represented by its two endpoints and the subset of endpoints at
which an arrowhead is retained.  Ordinary undirected edges have no arrowheads;
the semi-directed networks considered here have one arrowhead per directed
edge.  The more general representation makes suppression unambiguous.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, Iterator, List, Mapping, Sequence, Set, Tuple


@dataclass(frozen=True)
class MixedEdge:
    ends: FrozenSet[str]
    arrowheads: FrozenSet[str]

    @staticmethod
    def make(u: str, v: str, arrowheads: Iterable[str] = ()) -> "MixedEdge":
        if u == v:
            raise ValueError(f"loop at {u}")
        ends = frozenset((u, v))
        arrows = frozenset(arrowheads)
        if not arrows <= ends:
            raise ValueError("an arrowhead must lie at an endpoint")
        return MixedEdge(ends, arrows)

    def other(self, vertex: str) -> str:
        if vertex not in self.ends:
            raise KeyError(vertex)
        return next(iter(self.ends - {vertex}))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def degrees(arcs: Sequence[Tuple[str, str]]) -> Tuple[Dict[str, int], Dict[str, int]]:
    indegree: Dict[str, int] = defaultdict(int)
    outdegree: Dict[str, int] = defaultdict(int)
    for tail, head in arcs:
        outdegree[tail] += 1
        indegree[head] += 1
        indegree.setdefault(tail, 0)
        outdegree.setdefault(head, 0)
    return dict(indegree), dict(outdegree)


def is_acyclic(vertices: Iterable[str], arcs: Sequence[Tuple[str, str]]) -> bool:
    vertices = set(vertices)
    indegree = {v: 0 for v in vertices}
    children: Dict[str, List[str]] = {v: [] for v in vertices}
    for tail, head in arcs:
        indegree[head] += 1
        children[tail].append(head)
    queue = deque(v for v in vertices if indegree[v] == 0)
    seen = 0
    while queue:
        vertex = queue.popleft()
        seen += 1
        for child in children[vertex]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    return seen == len(vertices)


def validate_rooted(
    root: str,
    arcs: Sequence[Tuple[str, str]],
    leaf_labels: Mapping[str, int],
) -> Dict[str, object]:
    vertices = {vertex for arc in arcs for vertex in arc}
    indegree, outdegree = degrees(arcs)
    errors: List[str] = []
    if len(arcs) != len(set(arcs)):
        errors.append("parallel directed arcs")
    if root not in vertices or (indegree[root], outdegree[root]) != (0, 2):
        errors.append("root does not have bidegree (0,2)")
    for vertex in sorted(vertices):
        pair = (indegree[vertex], outdegree[vertex])
        if vertex in leaf_labels:
            if pair != (1, 0):
                errors.append(f"leaf {vertex} has bidegree {pair}")
        elif vertex != root and pair not in ((1, 2), (2, 1)):
            errors.append(f"internal {vertex} has bidegree {pair}")
    if set(leaf_labels.values()) != set(range(1, len(leaf_labels) + 1)):
        errors.append("leaf labels are not a bijection to [n]")
    if not is_acyclic(vertices, arcs):
        errors.append("directed cycle")
    children: Dict[str, List[str]] = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)

    def reachable(removed: str | None = None) -> Set[str]:
        if root == removed:
            return set()
        seen = {root}
        queue = deque((root,))
        while queue:
            vertex = queue.popleft()
            for child in children[vertex]:
                if child == removed or child in seen:
                    continue
                seen.add(child)
                queue.append(child)
        return seen

    if reachable() != vertices:
        errors.append("not every vertex is reachable from the root")
    for vertex in sorted(vertices - {root} - set(leaf_labels)):
        if not (set(leaf_labels) & reachable(vertex)):
            errors.append(f"root is not the lowest stable ancestor; {vertex} lies below it")
    return {
        "valid": not errors,
        "errors": errors,
        "vertices": len(vertices),
        "arcs": len(arcs),
        "tree_vertices": sorted(
            v for v in vertices if v != root and v not in leaf_labels
            and (indegree[v], outdegree[v]) == (1, 2)
        ),
        "reticulations": sorted(
            v for v in vertices if (indegree[v], outdegree[v]) == (2, 1)
        ),
    }


def merge_parallel(edges: Iterable[MixedEdge]) -> List[MixedEdge]:
    grouped: Dict[FrozenSet[str], Set[str]] = defaultdict(set)
    for edge in edges:
        grouped[edge.ends].update(edge.arrowheads)
    return [MixedEdge(ends, frozenset(arrows)) for ends, arrows in grouped.items()]


def incidence(edges: Sequence[MixedEdge]) -> Dict[str, List[MixedEdge]]:
    result: Dict[str, List[MixedEdge]] = defaultdict(list)
    for edge in edges:
        for endpoint in edge.ends:
            result[endpoint].append(edge)
    return dict(result)


def suppress_vertex(edges: Sequence[MixedEdge], vertex: str) -> List[MixedEdge]:
    inc = incidence(edges).get(vertex, [])
    if len(inc) != 2:
        raise ValueError(f"cannot suppress degree-{len(inc)} vertex {vertex}")
    left, right = inc
    u, v = left.other(vertex), right.other(vertex)
    if u == v:
        # The two-edge digon is exactly a parallel-edge artifact.  Removing the
        # degree-two vertex leaves no additional simple edge to insert.
        return merge_parallel(edge for edge in edges if edge not in inc)
    arrows = set()
    if u in left.arrowheads:
        arrows.add(u)
    if v in right.arrowheads:
        arrows.add(v)
    retained = [edge for edge in edges if edge not in inc]
    retained.append(MixedEdge.make(u, v, arrows))
    return merge_parallel(retained)


def standard_semi_directed_reduction(
    root: str,
    arcs: Sequence[Tuple[str, str]],
    leaf_labels: Mapping[str, int],
) -> Tuple[List[MixedEdge], Dict[str, int]]:
    indegree, outdegree = degrees(arcs)
    reticulations = {v for v in indegree if (indegree[v], outdegree[v]) == (2, 1)}
    edges = [
        MixedEdge.make(tail, head, (head,) if head in reticulations else ())
        for tail, head in arcs
    ]
    edges = suppress_vertex(edges, root)
    labels = dict(leaf_labels)
    while True:
        inc = incidence(edges)
        candidates = sorted(v for v, adjacent in inc.items() if v not in labels and len(adjacent) == 2)
        if not candidates:
            break
        edges = suppress_vertex(edges, candidates[0])
    return merge_parallel(edges), labels


def edge_token(edge: MixedEdge, names: Mapping[str, str]) -> str:
    u, v = sorted((names[x] for x in edge.ends))
    arrows = ",".join(sorted(names[x] for x in edge.arrowheads))
    return f"{u}--{v}>{arrows}"


def canonical_mixed_encoding(edges: Sequence[MixedEdge], labels: Mapping[str, int]) -> str:
    vertices = sorted({v for edge in edges for v in edge.ends})
    internals = [v for v in vertices if v not in labels]
    leaf_names = {v: f"L{labels[v]:04d}" for v in labels}
    best: str | None = None
    for ordering in itertools.permutations(internals):
        names = dict(leaf_names)
        names.update({v: f"I{i:04d}" for i, v in enumerate(ordering)})
        candidate = ";".join(sorted(edge_token(edge, names) for edge in edges))
        if best is None or candidate < best:
            best = candidate
    assert best is not None
    return best


def undirected_adjacency(edges: Sequence[MixedEdge]) -> Dict[str, Set[str]]:
    adj: Dict[str, Set[str]] = defaultdict(set)
    for edge in edges:
        u, v = tuple(edge.ends)
        adj[u].add(v)
        adj[v].add(u)
    return dict(adj)


def biconnected_components(edges: Sequence[MixedEdge]) -> List[Set[str]]:
    """Tarjan edge-stack algorithm, returned as vertex sets."""
    adj = undirected_adjacency(edges)
    discovery: Dict[str, int] = {}
    low: Dict[str, int] = {}
    parent: Dict[str, str | None] = {}
    stack: List[Tuple[str, str]] = []
    components: List[Set[str]] = []
    clock = 0

    def visit(u: str) -> None:
        nonlocal clock
        clock += 1
        discovery[u] = low[u] = clock
        for v in sorted(adj[u]):
            if v not in discovery:
                parent[v] = u
                stack.append((u, v))
                visit(v)
                low[u] = min(low[u], low[v])
                if low[v] >= discovery[u]:
                    component: Set[str] = set()
                    while stack:
                        a, b = stack.pop()
                        component.update((a, b))
                        if (a, b) == (u, v):
                            break
                    components.append(component)
            elif parent.get(u) != v and discovery[v] < discovery[u]:
                low[u] = min(low[u], discovery[v])
                stack.append((u, v))

    for start in sorted(adj):
        if start not in discovery:
            parent[start] = None
            visit(start)
    return components


def simple_cycles(edges: Sequence[MixedEdge]) -> Set[Tuple[str, ...]]:
    adj = undirected_adjacency(edges)
    vertices = sorted(adj)
    found: Set[Tuple[str, ...]] = set()

    def normalize(cycle: Sequence[str]) -> Tuple[str, ...]:
        options = []
        values = list(cycle)
        for direction in (values, list(reversed(values))):
            for shift in range(len(values)):
                options.append(tuple(direction[shift:] + direction[:shift]))
        return min(options)

    for start in vertices:
        def walk(current: str, path: List[str], used: Set[str]) -> None:
            for nxt in sorted(adj[current]):
                if nxt == start and len(path) >= 3:
                    found.add(normalize(path))
                elif nxt > start and nxt not in used:
                    walk(nxt, path + [nxt], used | {nxt})
        walk(start, [start], {start})
    return found


def reticulation_vertices(edges: Sequence[MixedEdge]) -> Set[str]:
    incoming: Dict[str, int] = defaultdict(int)
    for edge in edges:
        for vertex in edge.arrowheads:
            incoming[vertex] += 1
    return {vertex for vertex, count in incoming.items() if count == 2}


def semi_directed_statistics(edges: Sequence[MixedEdge], labels: Mapping[str, int]) -> Dict[str, object]:
    cycles = simple_cycles(edges)
    retics = reticulation_vertices(edges)
    blobs = biconnected_components(edges)
    nontrivial = [blob for blob in blobs if len(blob) >= 3]
    return {
        "vertices": len({v for edge in edges for v in edge.ends}),
        "edges": len(edges),
        "reticulations": sorted(retics),
        "cycle_lengths": sorted(len(cycle) for cycle in cycles),
        "triangle_count": sum(len(cycle) == 3 for cycle in cycles),
        "nontrivial_blob_count": len(nontrivial),
        "reticulations_per_nontrivial_blob": sorted(sum(v in retics for v in blob) for blob in nontrivial),
        "level": max((sum(v in retics for v in blob) for blob in nontrivial), default=0),
        "internal_degrees": {
            v: len(incidence(edges)[v])
            for v in sorted(incidence(edges)) if v not in labels
        },
    }


def strong_tree_child_local_test(edges: Sequence[MixedEdge], labels: Mapping[str, int]) -> Dict[str, object]:
    inc = incidence(edges)
    violations = []
    for vertex in sorted(inc):
        if vertex in labels:
            continue
        outgoing = sum(
            bool(edge.arrowheads) and vertex not in edge.arrowheads
            for edge in inc[vertex]
        )
        undirected = sum(not edge.arrowheads for edge in inc[vertex])
        if outgoing and undirected != 2:
            violations.append({
                "vertex": vertex,
                "outgoing_reticulation_edges": outgoing,
                "incident_undirected_edges": undirected,
            })
    return {
        "criterion": "every node with an outgoing edge has two incident undirected edges",
        "strongly_tree_child": not violations,
        "violations": violations,
    }


def directed_arcs_for_choice(
    edges: Sequence[MixedEdge], split_edge: MixedEdge, bits: Sequence[int]
) -> Tuple[str, List[Tuple[str, str]]]:
    root = "__AUDIT_ROOT__"
    u, v = sorted(split_edge.ends)
    arcs: List[Tuple[str, str]] = [(root, u), (root, v)]
    bit_iterator = iter(bits)
    for edge in edges:
        if edge == split_edge:
            continue
        a, b = sorted(edge.ends)
        if not edge.arrowheads:
            arcs.append((a, b) if next(bit_iterator) == 0 else (b, a))
        elif len(edge.arrowheads) == 1:
            head = next(iter(edge.arrowheads))
            arcs.append((edge.other(head), head))
        else:
            raise ValueError("a bidirected artifact cannot be rooted as a standard edge")
    return root, arcs


def tree_child(arcs: Sequence[Tuple[str, str]], root: str, labels: Mapping[str, int]) -> bool:
    indegree, outdegree = degrees(arcs)
    children: Dict[str, List[str]] = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    tree_or_leaf = {
        vertex for vertex in indegree
        if vertex in labels or (indegree[vertex], outdegree[vertex]) == (1, 2)
    }
    return all(any(child in tree_or_leaf for child in children[vertex])
               for vertex in indegree if outdegree[vertex] > 0)


def enumerate_rootings(edges: Sequence[MixedEdge], labels: Mapping[str, int]) -> List[Dict[str, object]]:
    results: List[Dict[str, object]] = []
    for split_edge in sorted(
        edges,
        key=lambda edge: (sorted(edge.ends), sorted(edge.arrowheads)),
    ):
        # A suppressed root can lie in the interior of an edge that retains an
        # arrowhead: deleting that edge and adding root-to-endpoint arcs
        # restores, for example, a root having one reticulation child.  Such a
        # placement is not automatically admissible; the bidegree and DAG
        # checks below decide it.
        orientable = sum(not edge.arrowheads for edge in edges if edge != split_edge)
        for bits in itertools.product((0, 1), repeat=orientable):
            root, arcs = directed_arcs_for_choice(edges, split_edge, bits)
            validation = validate_rooted(root, arcs, labels)
            if validation["valid"]:
                results.append({
                    "root_edge": sorted(split_edge.ends),
                    "arcs": [list(arc) for arc in sorted(arcs)],
                    "tree_child": tree_child(arcs, root, labels),
                })
    return results


def load_networks(certificate: Mapping[str, object]) -> Dict[str, Dict[str, object]]:
    result: Dict[str, Dict[str, object]] = {}
    encodings = certificate["network_encodings"]
    models = certificate["root_models"]
    for model_name, model in models.items():
        encoding = encodings[str(model["census_index"])]
        labels = dict(zip(encoding["leaves_in_port_order"], model["port_labels"]))
        result[model_name] = {
            "root": encoding["root"],
            "arcs": [tuple(arc) for arc in encoding["arcs_in_parameter_order"]],
            "labels": labels,
        }
    return result


def audit(certificate_path: Path) -> Dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    networks = load_networks(certificate)
    reductions: Dict[str, Tuple[List[MixedEdge], Dict[str, int]]] = {}
    records: Dict[str, object] = {}
    for name, network in networks.items():
        validation = validate_rooted(network["root"], network["arcs"], network["labels"])
        edges, labels = standard_semi_directed_reduction(
            network["root"], network["arcs"], network["labels"]
        )
        reductions[name] = (edges, labels)
        rootings = enumerate_rootings(edges, labels)
        records[name] = {
            "rooted_validation": validation,
            "chosen_rooting_tree_child": tree_child(
                network["arcs"], network["root"], network["labels"]
            ),
            "standard_reduction": {
                "edges": [
                    {
                        "ends": sorted(edge.ends),
                        "arrowheads": sorted(edge.arrowheads),
                    }
                    for edge in sorted(edges, key=lambda item: (sorted(item.ends), sorted(item.arrowheads)))
                ],
                "canonical_encoding": canonical_mixed_encoding(edges, labels),
                "statistics": semi_directed_statistics(edges, labels),
                "strong_tree_child_local_test": strong_tree_child_local_test(edges, labels),
            },
            "rootings": {
                "admissible_count": len(rootings),
                "tree_child_count": sum(record["tree_child"] for record in rootings),
                "all_tree_child": all(record["tree_child"] for record in rootings),
                "first_non_tree_child_witness": next(
                    (record for record in rootings if not record["tree_child"]), None
                ),
            },
        }
    names = sorted(reductions)
    isomorphism = {}
    for left_index, left in enumerate(names):
        for right in names[left_index + 1:]:
            left_encoding = records[left]["standard_reduction"]["canonical_encoding"]
            right_encoding = records[right]["standard_reduction"]["canonical_encoding"]
            isomorphism[f"{left}__{right}"] = left_encoding == right_encoding
    source_target_pairs = [
        ("N16_source", "N16_target"),
        ("N26_source", "N26_target"),
    ]
    conclusion = "OMEGA-B" if all(
        not records[name]["rootings"]["all_tree_child"] for name in records
    ) else "UNRESOLVED"
    return {
        "status": "EXACTLY COMPUTED",
        "implementation": "Python standard library; no discovery imports",
        "input": {
            "path": str(certificate_path),
            "sha256": sha256(certificate_path),
        },
        "networks": records,
        "pairwise_standard_semi_directed_isomorphism": isomorphism,
        "source_target_nonisomorphic": {
            f"{left}__{right}": not isomorphism[f"{left}__{right}"]
            for left, right in source_target_pairs
        },
        "gate_a_conclusion": conclusion,
        "gate_a_reason": (
            "Each standard semi-directed Omega topology has an admissible rooting "
            "that is not tree-child, equivalently it violates the local strong-tree-child "
            "criterion.  It is therefore outside the exact class of the 2025 theorem."
            if conclusion == "OMEGA-B" else
            "The strong-tree-child hypothesis has not yet resolved the collision."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.certificate.resolve())
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
