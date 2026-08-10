#!/usr/bin/env python3
"""Clean-room exact verifier for the root/probe adversarial review.

This module intentionally imports no project modules.  It uses only the Python
standard library and derives its finite graph universes from degree, DAG,
root-suppression, and tree-child definitions.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, Iterator, List, Mapping, Optional, Sequence, Set, Tuple


Node = str
EdgeKey = Tuple[Node, Node]
Arc = Tuple[Node, Node]


def edge_key(u: Node, v: Node) -> EdgeKey:
    if u == v:
        raise ValueError("loop")
    return (u, v) if u < v else (v, u)


def powerset(items: Sequence[str]) -> Iterator[FrozenSet[str]]:
    for mask in range(1 << len(items)):
        yield frozenset(items[i] for i in range(len(items)) if mask & (1 << i))


def canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class NodeData:
    reticulation: bool = False
    label: Optional[str] = None

    @property
    def leaf(self) -> bool:
        return self.label is not None


@dataclass
class MixedGraph:
    """Simple mixed graph; an edge stores the endpoints carrying arrowheads."""

    nodes: Dict[Node, NodeData]
    edges: Dict[EdgeKey, FrozenSet[Node]]

    def copy(self) -> "MixedGraph":
        return MixedGraph(dict(self.nodes), dict(self.edges))

    def add_node(self, node: Node, *, reticulation: bool = False, label: Optional[str] = None) -> None:
        if node in self.nodes:
            raise ValueError(f"duplicate node {node}")
        self.nodes[node] = NodeData(reticulation=reticulation, label=label)

    def add_edge(self, u: Node, v: Node, arrows: Iterable[Node] = ()) -> bool:
        key = edge_key(u, v)
        marks = frozenset(arrows)
        if not marks.issubset(key):
            raise ValueError("arrowhead not on edge")
        if key in self.edges:
            return False
        self.edges[key] = marks
        return True

    def degree(self, node: Node) -> int:
        return sum(node in key for key in self.edges)

    def neighbors(self, node: Node) -> List[Node]:
        ans = []
        for u, v in self.edges:
            if u == node:
                ans.append(v)
            elif v == node:
                ans.append(u)
        return sorted(ans)

    def incident(self, node: Node) -> List[Tuple[EdgeKey, FrozenSet[Node]]]:
        return sorted((key, marks) for key, marks in self.edges.items() if node in key)

    def is_binary_shape(self) -> bool:
        for node, data in self.nodes.items():
            want = 1 if data.leaf else 3
            if self.degree(node) != want:
                return False
        return True

    def record(self) -> dict:
        return {
            "nodes": [
                {
                    "id": node,
                    "reticulation": data.reticulation,
                    "label": data.label,
                }
                for node, data in sorted(self.nodes.items())
            ],
            "edges": [
                {"ends": list(key), "arrowheads": sorted(marks)}
                for key, marks in sorted(self.edges.items())
            ],
        }


@dataclass(frozen=True)
class Rooting:
    site: EdgeKey
    arcs: FrozenSet[Arc]
    tree_child: bool

    def record(self) -> dict:
        return {
            "site": list(self.site),
            "arcs": [list(arc) for arc in sorted(self.arcs)],
            "tree_child": self.tree_child,
        }


def arc_degrees(nodes: Iterable[Node], arcs: Iterable[Arc]) -> Tuple[Dict[Node, int], Dict[Node, int]]:
    indeg = {node: 0 for node in nodes}
    outdeg = {node: 0 for node in nodes}
    for u, v in arcs:
        outdeg[u] += 1
        indeg[v] += 1
    return indeg, outdeg


def is_dag(nodes: Iterable[Node], arcs: Iterable[Arc]) -> bool:
    nodes = list(nodes)
    indeg, _ = arc_degrees(nodes, arcs)
    children: Dict[Node, List[Node]] = defaultdict(list)
    for u, v in arcs:
        children[u].append(v)
    queue = deque(sorted(node for node in nodes if indeg[node] == 0))
    seen = 0
    while queue:
        u = queue.popleft()
        seen += 1
        for v in children[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return seen == len(nodes)


def reachable_from(root: Node, arcs: Iterable[Arc]) -> Set[Node]:
    children: Dict[Node, List[Node]] = defaultdict(list)
    for u, v in arcs:
        children[u].append(v)
    seen = {root}
    queue = deque([root])
    while queue:
        u = queue.popleft()
        for v in children[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return seen


def is_lsa_valid(nodes: Mapping[Node, NodeData], arcs: FrozenSet[Arc], root: Node) -> bool:
    leaves = {node for node, data in nodes.items() if data.leaf}
    if not leaves:
        return False
    children: Dict[Node, List[Node]] = defaultdict(list)
    for u, v in arcs:
        children[u].append(v)
    for blocked in nodes:
        if blocked == root:
            continue
        seen = {root}
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in children[u]:
                if v == blocked or v in seen:
                    continue
                seen.add(v)
                queue.append(v)
        if not (leaves & seen):
            return False
    return True


def is_tree_child(nodes: Mapping[Node, NodeData], arcs: FrozenSet[Arc], root: Node = "ROOT") -> bool:
    children: Dict[Node, List[Node]] = defaultdict(list)
    for u, v in arcs:
        children[u].append(v)
    for node, data in nodes.items():
        if data.leaf:
            continue
        if node == root or not data.reticulation:
            if not any(not nodes[child].reticulation for child in children[node]):
                return False
        else:
            if len(children[node]) != 1 or nodes[children[node][0]].reticulation:
                return False
    return True


def sd0_from_rooting(nodes: Mapping[Node, NodeData], arcs: FrozenSet[Arc], root: Node = "ROOT") -> Optional[MixedGraph]:
    if root not in nodes:
        return None
    children = sorted(v for u, v in arcs if u == root)
    if len(children) != 2:
        return None
    mixed = MixedGraph({node: data for node, data in nodes.items() if node != root}, {})
    for u, v in arcs:
        if root in (u, v):
            continue
        marks = (v,) if nodes[v].reticulation else ()
        if not mixed.add_edge(u, v, marks):
            return None
    a, b = children
    marks = tuple(x for x in (a, b) if nodes[x].reticulation)
    if not mixed.add_edge(a, b, marks):
        return None
    return mixed


def mixed_equal(a: MixedGraph, b: MixedGraph) -> bool:
    return a.nodes == b.nodes and a.edges == b.edges


def enumerate_rootings(graph: MixedGraph) -> List[Rooting]:
    """Enumerate all narrow admissible rootings from the definitions."""
    if not graph.is_binary_shape():
        return []
    ans: List[Rooting] = []
    base_nodes = dict(graph.nodes)
    rooted_nodes = dict(base_nodes)
    rooted_nodes["ROOT"] = NodeData()
    for site, site_marks in sorted(graph.edges.items()):
        a, b = site
        required_site_marks = frozenset(x for x in site if graph.nodes[x].reticulation)
        if site_marks != required_site_marks:
            continue
        fixed: Set[Arc] = {("ROOT", a), ("ROOT", b)}
        variable: List[EdgeKey] = []
        impossible = False
        for key, marks in graph.edges.items():
            if key == site:
                continue
            u, v = key
            if len(marks) == 0:
                variable.append(key)
            elif len(marks) == 1:
                head = next(iter(marks))
                tail = v if head == u else u
                fixed.add((tail, head))
            else:
                impossible = True
                break
        if impossible:
            continue
        for bits in itertools.product((0, 1), repeat=len(variable)):
            arcs = set(fixed)
            for (u, v), bit in zip(variable, bits):
                arcs.add((u, v) if bit == 0 else (v, u))
            frozen = frozenset(arcs)
            indeg, outdeg = arc_degrees(rooted_nodes, frozen)
            good = indeg["ROOT"] == 0 and outdeg["ROOT"] == 2
            for node, data in graph.nodes.items():
                if data.leaf:
                    good = good and indeg[node] == 1 and outdeg[node] == 0
                elif data.reticulation:
                    good = good and indeg[node] == 2 and outdeg[node] == 1
                else:
                    good = good and indeg[node] == 1 and outdeg[node] == 2
            if not good or not is_dag(rooted_nodes, frozen):
                continue
            if reachable_from("ROOT", frozen) != set(rooted_nodes):
                continue
            if not is_lsa_valid(rooted_nodes, frozen, "ROOT"):
                continue
            recovered = sd0_from_rooting(rooted_nodes, frozen)
            if recovered is None or not mixed_equal(recovered, graph):
                continue
            tc = is_tree_child(rooted_nodes, frozen)
            ans.append(Rooting(site=site, arcs=frozen, tree_child=tc))
    unique = {(r.site, r.arcs): r for r in ans}
    return [unique[key] for key in sorted(unique, key=lambda x: (x[0], sorted(x[1])))]


def local_tail_criterion(graph: MixedGraph) -> bool:
    """Definition-side arrow-tail condition, without assuming sufficiency."""
    if not graph.is_binary_shape():
        return False
    for key, marks in graph.edges.items():
        if len(marks) != 1:
            if marks:
                return False
            continue
        head = next(iter(marks))
        if not graph.nodes[head].reticulation:
            return False
        u, v = key
        tail = v if head == u else u
        if graph.nodes[tail].reticulation:
            return False
        other = [(k, m) for k, m in graph.incident(tail) if k != key]
        if len(other) != 2 or any(m for _, m in other):
            return False
    for node, data in graph.nodes.items():
        arrow_count = sum(node in marks for _, marks in graph.incident(node))
        if data.reticulation and arrow_count != 2:
            return False
        if not data.reticulation and arrow_count != 0:
            return False
    return True


def strong_from_census(graph: MixedGraph) -> Tuple[bool, List[Rooting]]:
    roots = enumerate_rootings(graph)
    return bool(roots) and all(root.tree_child for root in roots), roots


@dataclass(frozen=True)
class Segment:
    id: str
    tail: Node
    head: Node
    path: int


@dataclass
class EventCore:
    family: str
    placement: str
    node_roles: Dict[Node, str]
    segments: List[Segment]

    def record(self) -> dict:
        return {
            "family": self.family,
            "placement": self.placement,
            "node_roles": dict(sorted(self.node_roles.items())),
            "segments": [
                {"id": s.id, "tail": s.tail, "head": s.head, "path": s.path}
                for s in sorted(self.segments, key=lambda x: x.id)
            ],
            "canonical_key": canonical_event_key(self.node_roles, self.segments),
        }


def event_role_groups(node_roles: Mapping[Node, str]) -> List[List[Node]]:
    groups: Dict[str, List[Node]] = defaultdict(list)
    for node, role in node_roles.items():
        groups[role].append(node)
    return [sorted(groups[role]) for role in sorted(groups)]


def canonical_event_key(node_roles: Mapping[Node, str], segments: Sequence[Segment]) -> str:
    groups = event_role_groups(node_roles)
    best: Optional[str] = None
    for choices in itertools.product(*(list(itertools.permutations(group)) for group in groups)):
        order = [node for group_order in choices for node in group_order]
        index = {node: i for i, node in enumerate(order)}
        role_word = ",".join(node_roles[node] for node in order)
        matrix = [[0 for _ in order] for _ in order]
        for seg in segments:
            matrix[index[seg.tail]][index[seg.head]] += 1
        word = role_word + ";" + ",".join(str(x) for row in matrix for x in row)
        if best is None or word < best:
            best = word
    assert best is not None
    return best


def ordered_path_assignments(events: Sequence[Node]) -> Iterator[Tuple[Tuple[Node, ...], Tuple[Node, ...], Tuple[Node, ...]]]:
    seen = set()
    for allocation in itertools.product(range(3), repeat=len(events)):
        buckets = [[event for event, path in zip(events, allocation) if path == i] for i in range(3)]
        perm_lists = [list(itertools.permutations(bucket)) for bucket in buckets]
        for paths in itertools.product(*perm_lists):
            key = tuple(tuple(path) for path in paths)
            if key not in seen:
                seen.add(key)
                yield key  # type: ignore[misc]


def derive_theta_event_cores() -> List[EventCore]:
    raw: List[EventCore] = []
    cases = [
        ("TT", {"A": "branch_tree", "B": "branch_tree", "S": "source", "X1": "sink", "X2": "sink"}, ("S", "X1", "X2")),
        ("TR", {"A": "branch_tree", "B": "branch_retic", "S": "source", "X1": "sink"}, ("S", "X1")),
    ]
    degree_targets = {
        "branch_tree": (1, 2),
        "branch_retic": (2, 1),
        "source": (0, 2),
        "sink": (2, 0),
    }
    for family, roles, events in cases:
        for paths in ordered_path_assignments(events):
            undirected: List[Tuple[str, Node, Node, int]] = []
            for pidx, path in enumerate(paths):
                vertices = ("A",) + tuple(path) + ("B",)
                for j, (u, v) in enumerate(zip(vertices, vertices[1:])):
                    undirected.append((f"p{pidx}e{j}", u, v, pidx))
            for bits in itertools.product((0, 1), repeat=len(undirected)):
                segments = []
                for (sid, u, v, pidx), bit in zip(undirected, bits):
                    tail, head = (u, v) if bit == 0 else (v, u)
                    segments.append(Segment(sid, tail, head, pidx))
                indeg = {node: 0 for node in roles}
                outdeg = {node: 0 for node in roles}
                for seg in segments:
                    outdeg[seg.tail] += 1
                    indeg[seg.head] += 1
                if any((indeg[node], outdeg[node]) != degree_targets[role] for node, role in roles.items()):
                    continue
                if not is_dag(roles, [(s.tail, s.head) for s in segments]):
                    continue
                if reachable_from("S", [(s.tail, s.head) for s in segments]) != set(roles):
                    continue
                occupied_paths = [sum(event in path for event in events) for path in paths]
                if family == "TT":
                    placement = "separated" if sorted(occupied_paths) == [1, 1, 1] else "nested"
                else:
                    placement = "nested" if any(x == 2 for x in occupied_paths) else "separated"
                raw.append(EventCore(family, placement, dict(roles), segments))
    by_key: Dict[str, EventCore] = {}
    for core in raw:
        by_key.setdefault(canonical_event_key(core.node_roles, core.segments), core)
    return [by_key[key] for key in sorted(by_key)]


def derive_two_reticulate_branch_candidates() -> List[EventCore]:
    """Exhaust the excluded RR branch case instead of assuming it away."""
    roles = {"A": "branch_retic", "B": "branch_retic", "S": "source"}
    degree_targets = {
        "branch_retic": (2, 1),
        "source": (0, 2),
    }
    raw = []
    for paths in ordered_path_assignments(("S",)):
        undirected: List[Tuple[str, Node, Node, int]] = []
        for pidx, path in enumerate(paths):
            vertices = ("A",) + tuple(path) + ("B",)
            for j, (u, v) in enumerate(zip(vertices, vertices[1:])):
                undirected.append((f"p{pidx}e{j}", u, v, pidx))
        for bits in itertools.product((0, 1), repeat=len(undirected)):
            segments = []
            for (sid, u, v, pidx), bit in zip(undirected, bits):
                tail, head = (u, v) if bit == 0 else (v, u)
                segments.append(Segment(sid, tail, head, pidx))
            indeg = {node: 0 for node in roles}
            outdeg = {node: 0 for node in roles}
            for seg in segments:
                outdeg[seg.tail] += 1
                indeg[seg.head] += 1
            if any((indeg[node], outdeg[node]) != degree_targets[role] for node, role in roles.items()):
                continue
            arcs = [(s.tail, s.head) for s in segments]
            if not is_dag(roles, arcs) or reachable_from("S", arcs) != set(roles):
                continue
            raw.append(EventCore("RR", "forbidden", dict(roles), segments))
    by_key = {
        canonical_event_key(core.node_roles, core.segments): core
        for core in raw
    }
    return [by_key[key] for key in sorted(by_key)]


def derive_cycle_event_core() -> EventCore:
    roles = {"S": "source", "X1": "sink"}
    segments = [Segment("p0e0", "S", "X1", 0), Segment("p1e0", "S", "X1", 1)]
    return EventCore("cycle", "unique", roles, segments)


def graph_from_core(core: EventCore, occupied: FrozenSet[str], *, include_sinks: Optional[FrozenSet[str]] = None) -> Optional[MixedGraph]:
    graph = MixedGraph({}, {})
    retic_nodes = {node for node, role in core.node_roles.items() if role in {"sink", "branch_retic"}}
    for node in core.node_roles:
        graph.add_node(node, reticulation=node in retic_nodes)
    for seg in core.segments:
        chain = [seg.tail]
        if seg.id in occupied:
            pnode = f"P:{seg.id}"
            graph.add_node(pnode)
            chain.append(pnode)
        chain.append(seg.head)
        for u, v in zip(chain, chain[1:]):
            arrows = (v,) if graph.nodes[v].reticulation else ()
            if not graph.add_edge(u, v, arrows):
                return None
        if seg.id in occupied:
            leaf = f"L:repair:{seg.id}"
            graph.add_node(leaf, label=f"repair:{seg.id}")
            if not graph.add_edge(chain[1], leaf):
                return None
    graph.add_node("L:incoming", label="incoming")
    if not graph.add_edge("S", "L:incoming"):
        return None
    sinks = sorted(node for node, role in core.node_roles.items() if role == "sink")
    selected_sinks = frozenset(sinks) if include_sinks is None else include_sinks
    for sink in sinks:
        if sink not in selected_sinks:
            continue
        leaf = f"L:sink:{sink}"
        graph.add_node(leaf, label=f"sink:{sink}")
        if not graph.add_edge(sink, leaf):
            return None
    return graph


def mixed_automorphism_count(graph: MixedGraph, limit: int = 100000) -> int:
    signatures: Dict[Tuple[object, ...], List[Node]] = defaultdict(list)
    for node, data in graph.nodes.items():
        incident = graph.incident(node)
        signatures[(
            data.label,
            data.reticulation,
            graph.degree(node),
            sum(node in marks for _, marks in incident),
            sum(not marks for _, marks in incident),
        )].append(node)
    groups = [sorted(group) for _, group in sorted(signatures.items(), key=lambda kv: repr(kv[0]))]
    original = frozenset((key, marks) for key, marks in graph.edges.items())
    count = 0
    tried = 0
    for permuted_groups in itertools.product(*(itertools.permutations(group) for group in groups)):
        mapping = {}
        for group, image in zip(groups, permuted_groups):
            mapping.update(zip(group, image))
        transformed = set()
        for (u, v), marks in graph.edges.items():
            nu, nv = mapping[u], mapping[v]
            transformed.add((edge_key(nu, nv), frozenset(mapping[x] for x in marks)))
        tried += 1
        if frozenset(transformed) == original:
            count += 1
        if tried > limit:
            raise RuntimeError("automorphism limit exceeded")
    return count


def all_tree_endpoint_leaves(graph: MixedGraph, rooting: Rooting) -> List[Node]:
    children: Dict[Node, List[Node]] = defaultdict(list)
    for u, v in rooting.arcs:
        children[u].append(v)
    found: Set[Node] = set()
    stack = ["ROOT"]
    while stack:
        node = stack.pop()
        if node != "ROOT" and graph.nodes[node].leaf:
            found.add(node)
            continue
        for child in children[node]:
            if child != "ROOT" and graph.nodes[child].reticulation:
                continue
            stack.append(child)
    return sorted(found)


def displayed_split_deck(graph: MixedGraph) -> List[dict]:
    retics = sorted(node for node, data in graph.nodes.items() if data.reticulation)
    incoming: Dict[Node, List[EdgeKey]] = {}
    for retic in retics:
        incoming[retic] = sorted(key for key, marks in graph.incident(retic) if retic in marks)
        if len(incoming[retic]) != 2:
            return []
    leaves = {node: data.label for node, data in graph.nodes.items() if data.leaf}
    all_labels = frozenset(label for label in leaves.values() if label is not None)
    deck = []
    for choices in itertools.product((0, 1), repeat=len(retics)):
        deleted = {incoming[r][1 - choice] for r, choice in zip(retics, choices)}
        kept_edges = [key for key in graph.edges if key not in deleted]
        adjacency: Dict[Node, List[Node]] = defaultdict(list)
        for u, v in kept_edges:
            adjacency[u].append(v)
            adjacency[v].append(u)
        connected = set()
        if graph.nodes:
            start = next(iter(graph.nodes))
            queue = deque([start])
            connected.add(start)
            while queue:
                u = queue.popleft()
                for v in adjacency[u]:
                    if v not in connected:
                        connected.add(v)
                        queue.append(v)
        is_tree = len(kept_edges) == len(graph.nodes) - 1 and len(connected) == len(graph.nodes)
        splits = []
        if is_tree:
            for blocked in kept_edges:
                u0, _ = blocked
                side = {u0}
                queue = deque([u0])
                while queue:
                    u = queue.popleft()
                    for v in adjacency[u]:
                        if edge_key(u, v) == blocked or v in side:
                            continue
                        side.add(v)
                        queue.append(v)
                labels_a = frozenset(leaves[node] for node in side if node in leaves)
                labels_b = all_labels - labels_a
                canonical = min(tuple(sorted(labels_a)), tuple(sorted(labels_b)))
                splits.append(list(canonical))
        deck.append({
            "retained_parent_edge_index": list(choices),
            "is_tree": is_tree,
            "splits": sorted(splits),
        })
    return deck


def audit_repairs_and_roots(core: EventCore) -> dict:
    segment_ids = sorted(seg.id for seg in core.segments)
    rows = []
    graphs: Dict[FrozenSet[str], MixedGraph] = {}
    for occupied in powerset(segment_ids):
        graph = graph_from_core(core, occupied)
        if graph is None:
            rows.append({
                "occupied": sorted(occupied),
                "simple_binary": False,
                "tail_criterion": False,
                "rooting_count": 0,
                "tree_child_rooting_count": 0,
                "intrinsic_strong": False,
            })
            continue
        graphs[occupied] = graph
        strong, rootings = strong_from_census(graph)
        rows.append({
            "occupied": sorted(occupied),
            "simple_binary": graph.is_binary_shape(),
            "tail_criterion": local_tail_criterion(graph),
            "rooting_count": len(rootings),
            "tree_child_rooting_count": sum(r.tree_child for r in rootings),
            "intrinsic_strong": strong,
        })
    tail_sets = [
        frozenset(row["occupied"])
        for row in rows
        if row["simple_binary"] and row["tail_criterion"]
    ]
    minimal_repairs = sorted(
        (s for s in tail_sets if not any(t < s for t in tail_sets)),
        key=lambda s: (len(s), sorted(s)),
    )
    mismatches = []
    for row in rows:
        occupied = frozenset(row["occupied"])
        proposed = any(repair.issubset(occupied) for repair in minimal_repairs)
        row["contains_minimum_repair"] = proposed
        if proposed != row["intrinsic_strong"]:
            mismatches.append({
                "occupied": sorted(occupied),
                "proposed": proposed,
                "intrinsic_strong": row["intrinsic_strong"],
            })
    sink_count = sum(role == "sink" for role in core.node_roles.values())
    supports = []
    root_failures = []
    all_tree_endpoint_test_count = 0
    endpoint_sites: Set[EdgeKey] = set()
    for repair in minimal_repairs:
        graph = graphs[repair]
        roots = enumerate_rootings(graph)
        roots_by_site: Dict[EdgeKey, int] = defaultdict(int)
        for rooting in roots:
            roots_by_site[rooting.site] += 1
            for leaf in all_tree_endpoint_leaves(graph, rooting):
                all_tree_endpoint_test_count += 1
                incident = [key for key in graph.edges if leaf in key]
                assert len(incident) == 1
                site = incident[0]
                endpoint_sites.add(site)
                if roots_by_site.get(site, 0) == 0:
                    # The complete root list has already been computed; use it,
                    # not traversal order through the current loop.
                    if not any(candidate.site == site for candidate in roots):
                        root_failures.append({
                            "repair": sorted(repair),
                            "starting_site": list(rooting.site),
                            "endpoint_leaf": graph.nodes[leaf].label,
                            "endpoint_site": list(site),
                        })
        supports.append({
            "repair": sorted(repair),
            "outgoing_support_size": sink_count + len(repair),
            "pointwise_automorphism_count": mixed_automorphism_count(graph),
            "rooting_count": len(roots),
            "displayed_split_deck": displayed_split_deck(graph),
            "graph": graph.record(),
        })
    return {
        "core": core.record(),
        "occupancy_rows": rows,
        "minimum_repairs": [sorted(x) for x in minimal_repairs],
        "criterion_mismatches_with_all_sinks_present": mismatches,
        "supports": supports,
        "root_move_failures": root_failures,
        "all_tree_endpoint_test_count": all_tree_endpoint_test_count,
        "distinct_all_tree_endpoint_sites": [list(site) for site in sorted(endpoint_sites)],
    }


def k4_minus_edge_graphs() -> List[MixedGraph]:
    # Degree-three branch vertices A,B and degree-two path vertices C,D.
    core_edges = [edge_key("A", "B"), edge_key("A", "C"), edge_key("C", "B"), edge_key("A", "D"), edge_key("D", "B")]
    leaf_edges = [edge_key("C", "L:C"), edge_key("D", "L:D")]
    all_edges = core_edges + leaf_edges
    base_nodes = ["A", "B", "C", "D"]
    graphs = []
    for retics in itertools.combinations(base_nodes, 2):
        retic_set = frozenset(retics)
        incident = {r: [e for e in all_edges if r in e] for r in retics}
        for chosen in itertools.product(*(list(itertools.combinations(incident[r], 2)) for r in retics)):
            marks: Dict[EdgeKey, Set[Node]] = {e: set() for e in all_edges}
            for r, edges in zip(retics, chosen):
                for edge in edges:
                    marks[edge].add(r)
            graph = MixedGraph({}, {})
            for node in base_nodes:
                graph.add_node(node, reticulation=node in retic_set)
            graph.add_node("L:C", label="port:C")
            graph.add_node("L:D", label="port:D")
            valid = True
            for edge in all_edges:
                if not graph.add_edge(*edge, marks[edge]):
                    valid = False
            if valid:
                graphs.append(graph)
    unique: Dict[bytes, MixedGraph] = {}
    for graph in graphs:
        unique[canonical_json_bytes(graph.record())] = graph
    return [unique[key] for key in sorted(unique)]


def audit_k4_minus_edge() -> dict:
    rows = []
    tc_total = 0
    rooting_total = 0
    for idx, graph in enumerate(k4_minus_edge_graphs()):
        roots = enumerate_rootings(graph)
        tc = [r for r in roots if r.tree_child]
        rooting_total += len(roots)
        tc_total += len(tc)
        rows.append({
            "index": idx,
            "reticulations": sorted(n for n, d in graph.nodes.items() if d.reticulation),
            "arrowheads": [
                {"ends": list(edge), "at": sorted(marks)}
                for edge, marks in sorted(graph.edges.items()) if marks
            ],
            "admissible_rootings": len(roots),
            "tree_child_rootings": len(tc),
        })
    return {
        "marking_count": len(rows),
        "admissible_rooting_count": rooting_total,
        "tree_child_rooting_count": tc_total,
        "rows": rows,
    }


def cycle_sink_omission_counterexample(cycle: EventCore) -> dict:
    # Use either minimum one-segment repair, then intrinsically reduce after
    # omitting the unique sink: the surviving selected restriction is the
    # two-boundary tree.  Construct that reduced mixed graph directly and
    # census all of its rootings.
    repaired = graph_from_core(cycle, frozenset({cycle.segments[0].id}))
    assert repaired is not None
    reduced = MixedGraph({}, {})
    reduced.add_node("L:incoming", label="incoming")
    reduced.add_node("L:repair", label="repair:selected")
    reduced.add_edge("L:incoming", "L:repair")
    roots = enumerate_rootings(reduced)
    return {
        "interpretation": "ordinary intrinsic S_TC after full selected reduction",
        "full_core": repaired.record(),
        "selected_labels": ["incoming", "repair:selected"],
        "omitted_sink": "sink:X1",
        "reduced_selected_graph": reduced.record(),
        "admissible_rootings": len(roots),
        "tree_child_rootings": sum(r.tree_child for r in roots),
        "intrinsic_strong": bool(roots) and all(r.tree_child for r in roots),
        "preserves_cycle_core": False,
        "sink_plus_repair_criterion": False,
    }


def audit_event_universe() -> dict:
    cycle = derive_cycle_event_core()
    theta = derive_theta_event_cores()
    rr = derive_two_reticulate_branch_candidates()
    audits = [audit_repairs_and_roots(cycle)] + [audit_repairs_and_roots(core) for core in theta]
    return {
        "derivation": {
            "cycle_core_count": 1,
            "theta_core_count": len(theta),
            "two_reticulate_branch_class_count": len(rr),
            "theta_families": [f"{core.family}-{core.placement}" for core in theta],
            "all_event_cores": [cycle.record()] + [core.record() for core in theta],
            "unexpected_two_reticulate_branch_cores": [core.record() for core in rr],
        },
        "core_audits": audits,
        "sink_omission_semantic_counterexample": cycle_sink_omission_counterexample(cycle),
        "k4_minus_edge": audit_k4_minus_edge(),
    }


def summarize(certificate: dict) -> dict:
    audits = certificate["core_audits"]
    return {
        "theta_core_count": certificate["derivation"]["theta_core_count"],
        "two_reticulate_branch_class_count": certificate["derivation"]["two_reticulate_branch_class_count"],
        "core_names": [
            f"{row['core']['family']}-{row['core']['placement']}" for row in audits
        ],
        "minimum_repair_sizes": [
            [len(repair) for repair in row["minimum_repairs"]] for row in audits
        ],
        "support_sizes": [
            [support["outgoing_support_size"] for support in row["supports"]] for row in audits
        ],
        "support_stabilizers": [
            [support["pointwise_automorphism_count"] for support in row["supports"]] for row in audits
        ],
        "intrinsic_criterion_mismatch_count": sum(
            len(row["criterion_mismatches_with_all_sinks_present"]) for row in audits
        ),
        "root_move_failure_count": sum(len(row["root_move_failures"]) for row in audits),
        "root_move_endpoint_test_count": sum(row["all_tree_endpoint_test_count"] for row in audits),
        "k4_minus_edge_tree_child_rootings": certificate["k4_minus_edge"]["tree_child_rooting_count"],
        "sink_omission_is_intrinsically_strong": certificate["sink_omission_semantic_counterexample"]["intrinsic_strong"],
        "sink_omission_preserves_core": certificate["sink_omission_semantic_counterexample"]["preserves_cycle_core"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("root_probe_certificate.json"))
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    certificate = audit_event_universe()
    certificate["schema"] = "root-probe-clean-room-v1"
    certificate["summary"] = summarize(certificate)
    payload = canonical_json_bytes(certificate)
    args.output.write_bytes(payload)
    if args.summary:
        print(json.dumps(certificate["summary"], indent=2, sort_keys=True))
    print(f"certificate_sha256={sha256_bytes(payload)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
