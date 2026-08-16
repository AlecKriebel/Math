#!/usr/bin/env python3
"""Independent exact audit of the graph conventions used by the STC--JC paper.

This program imports no project graph, atlas, canonicalization, or verifier code.
It checks only finite graph statements needed by the definitions gate:

* the lowest-stable-ancestor (LSA) condition and tree-childness;
* the simple (1,2,2) two-triangle theta rooting census;
* the nonstandard parallel (1,1,2) pre-reduction census;
* the Theta sharpness pair's admissible-rooting/LSA counts;
* a root-artifact counterexample to mixing exhaustive parallel/degree-2
  suppression with the narrower local S_TC criterion;
* a literal 2-sub-blob boundary-vertex ambiguity; and
* the unique biconnected, simple, binary two-port level-2 gadget.

All arithmetic is finite integer/Boolean graph arithmetic from the Python
standard library.  The output is deterministic JSON.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


ROOT = "rho"
DEFAULT_PRIOR_ROOT = Path(
    "/Users/alec/Documents/Math/strong_level2_phylo_identifiability/"
    "AUDIT/PRIOR_WORK"
)


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def vertices_of(arcs):
    return {v for edge in arcs for v in edge}


def adjacency(arcs):
    children = defaultdict(list)
    parents = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
        parents[head].append(tail)
    return children, parents


def directed_acyclic(nodes, arcs):
    children, parents = adjacency(arcs)
    indegree = Counter({v: len(parents[v]) for v in nodes})
    queue = deque(sorted(v for v in nodes if indegree[v] == 0))
    seen = []
    while queue:
        vertex = queue.popleft()
        seen.append(vertex)
        for child in sorted(children[vertex]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    return len(seen) == len(nodes)


def reachable_avoiding(nodes, arcs, start, forbidden):
    if start == forbidden:
        return set()
    children, _parents = adjacency(arcs)
    reached = {start}
    queue = deque((start,))
    while queue:
        vertex = queue.popleft()
        for child in children[vertex]:
            if child == forbidden or child in reached:
                continue
            reached.add(child)
            queue.append(child)
    return reached


def root_is_lsa(nodes, arcs, root, leaves):
    """The root is the only vertex lying on every root-to-leaf path."""
    for vertex in nodes:
        if vertex == root:
            continue
        reached = reachable_avoiding(nodes, arcs, root, vertex)
        if not any(leaf in reached for leaf in leaves if leaf != vertex):
            return False
    return True


def rooted_validation(nodes, arcs, types, root=ROOT, require_lsa=True):
    nodes = set(nodes)
    arcs = tuple(arcs)
    if len(arcs) != len(set(arcs)):
        return False, "parallel_arc"
    if any(tail == head for tail, head in arcs):
        return False, "loop"
    if not directed_acyclic(nodes, arcs):
        return False, "directed_cycle"
    children, parents = adjacency(arcs)
    roots = {v for v in nodes if not parents[v]}
    if roots != {root}:
        return False, "root_count"
    for vertex in nodes:
        degree = (len(parents[vertex]), len(children[vertex]))
        expected = {
            "S": (0, 2),
            "T": (1, 2),
            "R": (2, 1),
            "L": (1, 0),
        }[types[vertex]]
        if degree != expected:
            return False, "bidegree"
    reached = reachable_avoiding(nodes, arcs, root, None)
    if reached != nodes:
        return False, "unreachable"
    leaves = {v for v in nodes if types[v] == "L"}
    if require_lsa and not root_is_lsa(nodes, arcs, root, leaves):
        return False, "lsa"
    return True, None


def tree_child(types, arcs):
    children, _parents = adjacency(arcs)
    for vertex, kind in types.items():
        if kind == "L":
            continue
        if not any(types[child] in {"T", "L"} for child in children[vertex]):
            return False
    return True


def tree_child_failure(types, arcs):
    children, _parents = adjacency(arcs)
    for vertex in sorted(types):
        if types[vertex] == "R" and any(
            types[child] == "R" for child in children[vertex]
        ):
            return {"kind": "reticulation_child", "witness": vertex}
    for vertex in sorted(types):
        if types[vertex] in {"S", "T"} and children[vertex] and all(
            types[child] == "R" for child in children[vertex]
        ):
            return {"kind": "all_children_reticulate", "witness": vertex}
    raise AssertionError("non-tree-child graph has no local witness")


def undirected_connected(nodes, edges, removed=None):
    active = set(nodes)
    if removed is not None:
        active.discard(removed)
    if not active:
        return True
    adj = defaultdict(set)
    for left, right in edges:
        if left == removed or right == removed:
            continue
        adj[left].add(right)
        adj[right].add(left)
    start = min(active)
    reached = {start}
    queue = deque((start,))
    while queue:
        vertex = queue.popleft()
        for other in adj[vertex]:
            if other not in reached:
                reached.add(other)
                queue.append(other)
    return reached == active


def biconnected(nodes, edges):
    nodes = set(nodes)
    return (
        len(nodes) >= 3
        and undirected_connected(nodes, edges)
        and all(undirected_connected(nodes, edges, removed=v) for v in nodes)
    )


def noncut_edge(nodes, edges, edge):
    remaining = list(edges)
    remaining.remove(edge)
    return undirected_connected(nodes, remaining)


def path_length_audit(limit=16):
    simple = []
    multigraph = []
    for lengths in product(range(1, limit + 1), repeat=3):
        if tuple(sorted(lengths)) != lengths:
            continue
        triangle_pairs = [
            pair
            for pair in combinations(range(3), 2)
            if lengths[pair[0]] + lengths[pair[1]] == 3
        ]
        if len(triangle_pairs) < 2:
            continue
        row = {
            "lengths": list(lengths),
            "triangle_pairs": [list(pair) for pair in triangle_pairs],
        }
        multigraph.append(row)
        if sum(length == 1 for length in lengths) <= 1:
            simple.append(row)
    assert [row["lengths"] for row in simple] == [[1, 2, 2]]
    assert [row["lengths"] for row in multigraph] == [[1, 1, 2], [1, 2, 2]]
    return {"simple": simple, "allowing_parallel_paths": multigraph}


K4E_VERTICES = ("u", "v", "a", "b")
K4E_EDGES = (("u", "v"), ("u", "a"), ("a", "v"), ("u", "b"), ("b", "v"))


def enumerate_k4e_rootings():
    records = []
    attempts = {"external": 0, "internal": 0}

    # Root outside through one of the two bridge ports.  The other root child is
    # an outgroup leaf, and the opposite port has a downstream leaf.
    for entry in ("a", "b"):
        exit_vertex = "b" if entry == "a" else "a"
        nodes = {ROOT, "out", "down", *K4E_VERTICES}
        for retics in combinations(K4E_VERTICES, 2):
            types = {ROOT: "S", "out": "L", "down": "L"}
            types.update({v: ("R" if v in retics else "T") for v in K4E_VERTICES})
            for bits in product((0, 1), repeat=len(K4E_EDGES)):
                attempts["external"] += 1
                arcs = [(ROOT, entry), (ROOT, "out"), (exit_vertex, "down")]
                arcs.extend(
                    edge if bit == 0 else (edge[1], edge[0])
                    for edge, bit in zip(K4E_EDGES, bits)
                )
                valid, reason = rooted_validation(nodes, arcs, types, require_lsa=False)
                if not valid:
                    continue
                records.append(
                    {
                        "mode": "external",
                        "root_site": f"port-{entry}",
                        "reticulations": list(retics),
                        "arcs": sorted([list(edge) for edge in arcs]),
                        "lsa": root_is_lsa(nodes, arcs, ROOT, {"out", "down"}),
                        "tree_child": tree_child(types, arcs),
                        "failure": None
                        if tree_child(types, arcs)
                        else tree_child_failure(types, arcs),
                    }
                )

    # Root inside one of the five core edges.  The two bridge ports terminate
    # in distinct leaves.
    for root_edge_index, root_edge in enumerate(K4E_EDGES):
        remaining = [
            edge for index, edge in enumerate(K4E_EDGES) if index != root_edge_index
        ]
        nodes = {ROOT, "la", "lb", *K4E_VERTICES}
        for retics in combinations(K4E_VERTICES, 2):
            types = {ROOT: "S", "la": "L", "lb": "L"}
            types.update({v: ("R" if v in retics else "T") for v in K4E_VERTICES})
            for bits in product((0, 1), repeat=len(remaining)):
                attempts["internal"] += 1
                left, right = root_edge
                arcs = [(ROOT, left), (ROOT, right), ("a", "la"), ("b", "lb")]
                arcs.extend(
                    edge if bit == 0 else (edge[1], edge[0])
                    for edge, bit in zip(remaining, bits)
                )
                valid, reason = rooted_validation(nodes, arcs, types, require_lsa=False)
                if not valid:
                    continue
                records.append(
                    {
                        "mode": "internal",
                        "root_site": "-".join(root_edge),
                        "reticulations": list(retics),
                        "arcs": sorted([list(edge) for edge in arcs]),
                        "lsa": root_is_lsa(nodes, arcs, ROOT, {"la", "lb"}),
                        "tree_child": tree_child(types, arcs),
                        "failure": None
                        if tree_child(types, arcs)
                        else tree_child_failure(types, arcs),
                    }
                )

    assert attempts == {"external": 384, "internal": 480}
    assert Counter(row["mode"] for row in records) == {"external": 4, "internal": 21}
    assert len(records) == 25
    assert sum(row["lsa"] for row in records) == 25
    assert not any(row["tree_child"] for row in records)
    assert Counter(row["failure"]["kind"] for row in records) == {
        "reticulation_child": 20,
        "all_children_reticulate": 5,
    }

    core_adjacencies = {frozenset(edge) for edge in K4E_EDGES}
    configuration_counts = Counter()
    root_site_counts = Counter()
    for row in records:
        pair_kind = (
            "adjacent"
            if frozenset(row["reticulations"]) in core_adjacencies
            else "nonadjacent_attachment_pair"
        )
        configuration_counts[
            (
                row["mode"],
                pair_kind,
                row["failure"]["kind"],
            )
        ] += 1
        root_site_counts[(row["mode"], row["root_site"])] += 1

    return {
        "attempts": attempts,
        "valid_binary_acyclic": len(records),
        "lsa_valid": sum(row["lsa"] for row in records),
        "tree_child": sum(row["tree_child"] for row in records),
        "failure_counts": dict(
            sorted(Counter(row["failure"]["kind"] for row in records).items())
        ),
        "configuration_counts": [
            {
                "root_mode": mode,
                "reticulation_pair": pair_kind,
                "tree_child_failure": failure,
                "count": count,
            }
            for (mode, pair_kind, failure), count in sorted(
                configuration_counts.items()
            )
        ],
        "root_site_counts": [
            {"root_mode": mode, "root_site": site, "count": count}
            for (mode, site), count in sorted(root_site_counts.items())
        ],
    }


PARALLEL_EDGES = (
    ("u", "v", "parallel-0"),
    ("u", "v", "parallel-1"),
    ("u", "a", "path-0"),
    ("a", "v", "path-1"),
)


def enumerate_parallel_112_presentations():
    """Audit the old one-leaf pre-reduction multigraph, not a standard topology."""
    raw = []
    for root_edge_index in range(len(PARALLEL_EDGES)):
        remaining = [
            edge for index, edge in enumerate(PARALLEL_EDGES) if index != root_edge_index
        ]
        left, right, edge_id = PARALLEL_EDGES[root_edge_index]
        for retics in combinations(("u", "v", "a"), 2):
            types = {ROOT: "S", "leaf": "L"}
            types.update({v: ("R" if v in retics else "T") for v in ("u", "v", "a")})
            nodes = set(types)
            for bits in product((0, 1), repeat=3):
                arcs = [(ROOT, left), (ROOT, right), ("a", "leaf")]
                arcs.extend(
                    (x, y) if bit == 0 else (y, x)
                    for (x, y, _eid), bit in zip(remaining, bits)
                )
                valid, _reason = rooted_validation(nodes, arcs, types, require_lsa=False)
                if not valid:
                    continue
                raw.append(
                    {
                        "root_edge_copy": edge_id,
                        "arcs": tuple(sorted(arcs)),
                        "lsa": root_is_lsa(nodes, arcs, ROOT, {"leaf"}),
                        "tree_child": tree_child(types, arcs),
                    }
                )
    unique = {row["arcs"]: row for row in raw}
    assert len(raw) == 4
    assert len(unique) == 2
    assert not any(row["lsa"] for row in raw)
    assert not any(row["tree_child"] for row in raw)
    return {
        "status": "pre_reduction_parallel_artifact",
        "edge_copy_records": len(raw),
        "distinct_rooted_dags": len(unique),
        "lsa_valid": 0,
        "tree_child": 0,
        "standard_simple_topology": False,
    }


def combine_mixed_edges(edges):
    """Identify exact parallel mixed edges; reject conflicting arrow patterns."""
    grouped = defaultdict(set)
    for endpoints, heads in edges:
        key = tuple(sorted(endpoints))
        grouped[key].add(tuple(sorted(heads)))
    answer = []
    for endpoints, patterns in sorted(grouped.items()):
        if len(patterns) != 1:
            raise AssertionError((endpoints, patterns))
        answer.append((frozenset(endpoints), frozenset(next(iter(patterns)))))
    return answer


def broad_standard_reduction(arcs, types, labelled_leaves, root=ROOT):
    """Brits-v2-style exhaustive root/parallel/degree-two reduction.

    Arrowheads at surviving endpoints are preserved.  The routine is deliberately
    small and fail-closed; it is used only for the explicit root artifact below.
    """
    mixed = []
    for tail, head in arcs:
        mixed.append((frozenset((tail, head)), frozenset((head,)) if types[head] == "R" else frozenset()))
    incident = [edge for edge in mixed if root in edge[0]]
    assert len(incident) == 2
    others = []
    inherited_heads = set()
    for endpoints, heads in incident:
        other = next(iter(endpoints - {root}))
        others.append(other)
        if other in heads:
            inherited_heads.add(other)
    mixed = [edge for edge in mixed if root not in edge[0]]
    mixed.append((frozenset(others), frozenset(inherited_heads)))
    mixed = combine_mixed_edges(mixed)

    while True:
        nodes = set().union(*(edge[0] for edge in mixed)) if mixed else set()
        candidate = None
        for vertex in sorted(nodes - set(labelled_leaves)):
            incident = [edge for edge in mixed if vertex in edge[0]]
            if len(incident) == 2:
                candidate = vertex
                break
        if candidate is None:
            break
        incident = [edge for edge in mixed if candidate in edge[0]]
        external = [next(iter(endpoints - {candidate})) for endpoints, _heads in incident]
        new_heads = {
            endpoint
            for endpoint, (_endpoints, heads) in zip(external, incident)
            if endpoint in heads
        }
        mixed = [edge for edge in mixed if candidate not in edge[0]]
        if external[0] != external[1]:
            mixed.append((frozenset(external), frozenset(new_heads)))
        mixed = combine_mixed_edges(mixed)
    return tuple(
        sorted(
            (
                tuple(sorted(endpoints)),
                tuple(sorted(heads)),
            )
            for endpoints, heads in mixed
        )
    )


def root_artifact_counterexample():
    """An LSA-valid non-tree-child level-2 rooting reduced to a plain tree.

    This proves that exhaustive artifact elimination cannot be combined with
    an unrestricted "all rooted preimages" definition of S_TC while retaining
    the local outgoing-arrow criterion.
    """
    arcs = (
        (ROOT, "a"),
        (ROOT, "r1"),
        ("a", "r1"),
        ("a", "b"),
        ("r1", "r2"),
        ("b", "r2"),
        ("b", "L1"),
        ("r2", "L2"),
    )
    types = {
        ROOT: "S",
        "a": "T",
        "b": "T",
        "r1": "R",
        "r2": "R",
        "L1": "L",
        "L2": "L",
    }
    nodes = set(types)
    valid, reason = rooted_validation(nodes, arcs, types, require_lsa=True)
    assert valid, reason
    assert not tree_child(types, arcs)
    core_nodes = {ROOT, "a", "b", "r1", "r2"}
    core_edges = [(u, v) for u, v in arcs if u in core_nodes and v in core_nodes]
    assert biconnected(core_nodes, core_edges)
    beta = len(core_edges) - len(core_nodes) + 1
    assert beta == 2
    reduced = broad_standard_reduction(arcs, types, {"L1", "L2"})
    assert reduced == ((('L1', 'L2'), ()),)
    return {
        "rooted_binary": True,
        "root_is_lsa": True,
        "tree_child": False,
        "reticulations": 2,
        "blob_cycle_rank": beta,
        "level_two": True,
        "broad_reduction": [{"endpoints": list(e), "arrowheads": list(h)} for e, h in reduced],
        "reduced_local_arrow_criterion": True,
        "consequence": (
            "Broad exhaustive artifact elimination plus all LSA-valid rooted preimages "
            "makes the local S_TC arrow criterion false."
        ),
    }


def literal_two_subblob_counterexample():
    """The boundary-vertex wording alone does not make contraction degree two.

    The ambient graph is not merely cubic: orienting v1->v0<-v3 and rooting
    through the v2--L2 arm gives an LSA-valid binary tree-child 4-sunlet.
    Its semi-directed local strong criterion also holds, since each arrow tail
    has its other cycle edge and pendant edge undirected.
    """
    cycle = [(f"v{i}", f"v{(i + 1) % 4}") for i in range(4)]
    pendants = [(f"v{i}", f"L{i}") for i in range(4)]
    edges = cycle + pendants
    nodes = vertices_of(edges)
    W = {"v0", "v1"}
    induced = [edge for edge in edges if set(edge) <= W]
    boundary_vertices = {
        vertex
        for vertex in W
        if any(vertex in edge and not set(edge) <= W for edge in edges)
    }
    external_edges = [edge for edge in edges if len(set(edge) & W) == 1]
    assert undirected_connected(W, induced)
    assert all(noncut_edge(nodes, edges, edge) for edge in induced)
    assert boundary_vertices == W
    assert len(external_edges) == 4

    rooted_arcs = (
        (ROOT, "v2"),
        (ROOT, "L2"),
        ("v2", "v1"),
        ("v2", "v3"),
        ("v1", "v0"),
        ("v3", "v0"),
        ("v0", "L0"),
        ("v1", "L1"),
        ("v3", "L3"),
    )
    rooted_types = {
        ROOT: "S",
        "v0": "R",
        "v1": "T",
        "v2": "T",
        "v3": "T",
        "L0": "L",
        "L1": "L",
        "L2": "L",
        "L3": "L",
    }
    valid, reason = rooted_validation(
        set(rooted_types), rooted_arcs, rooted_types, require_lsa=True
    )
    assert valid, reason
    assert tree_child(rooted_types, rooted_arcs)

    retained_arrows = (("v1", "v0"), ("v3", "v0"))
    undirected_edges = {
        frozenset(edge)
        for edge in edges
        if edge not in retained_arrows and tuple(reversed(edge)) not in retained_arrows
    }
    for tail in ("v1", "v3"):
        assert sum(tail in edge for edge in undirected_edges) == 2

    return {
        "graph": "strongly-tree-child four-sunlet",
        "ambient_standard_properties": {
            "binary": True,
            "simple_graph": True,
            "single_nonleaf_blob": True,
            "level": 1,
            "rooted_partner_is_lsa": True,
            "rooted_partner_is_tree_child": True,
            "semi_directed_local_strong_criterion": True,
        },
        "retained_arrows": [list(edge) for edge in retained_arrows],
        "rooted_witness_arcs": [list(edge) for edge in rooted_arcs],
        "W": sorted(W),
        "literal_brits_conditions": True,
        "boundary_vertices": len(boundary_vertices),
        "external_incident_edges": len(external_edges),
        "contracted_vertex_degree": len(external_edges),
        "ordinary_degree_two_suppression_defined": False,
        "consequence": (
            "A usable suppression convention must specify two external incidences "
            "or otherwise define how a higher-degree contraction vertex is suppressed."
        ),
    }


def operational_biconnected_two_port_audit():
    """Enumerate simple biconnected binary gadgets with two external edges."""
    accepted = []
    for order in (2, 4, 6):
        all_edges = list(combinations(range(order), 2))
        for mask in range(1 << len(all_edges)):
            edges = [edge for index, edge in enumerate(all_edges) if mask >> index & 1]
            degrees = Counter(v for edge in edges for v in edge)
            # Vertices 0,1 are the two boundary vertices, each with one external
            # edge and hence internal degree 2.  Every other binary vertex has
            # all three incidences in the gadget.
            if any(degrees[v] != (2 if v in {0, 1} else 3) for v in range(order)):
                continue
            beta = len(edges) - order + 1
            if beta > 2 or not biconnected(set(range(order)), edges):
                continue
            accepted.append({"order": order, "edges": edges, "beta": beta})
    assert len(accepted) == 1
    row = accepted[0]
    assert row["order"] == 4 and row["beta"] == 2 and len(row["edges"]) == 5
    assert (0, 1) not in row["edges"]
    return {
        "labelled_solutions": len(accepted),
        "unique_solution": {
            "order": row["order"],
            "size": len(row["edges"]),
            "cycle_rank": row["beta"],
            "graph": "K4 minus the edge between the two boundary vertices",
        },
        "scope": "biconnected, simple, binary gadget with exactly two external edges",
    }


THETA_DIRECTED = (("A", "C"), ("B", "C"), ("A", "F"), ("E", "F"))
THETA_INTERNAL_UNDIRECTED = (("A", "B"), ("C", "D"), ("D", "E"))
THETA_TYPES = {
    ROOT: "S",
    "A": "T",
    "B": "T",
    "C": "R",
    "D": "T",
    "E": "T",
    "F": "R",
    "L1": "L",
    "L2": "L",
    "L3": "L",
    "L4": "L",
}
THETA_PENDANTS = {
    "N": (("B", "L1"), ("D", "L2"), ("F", "L3"), ("E", "L4")),
    "N_prime": (("E", "L1"), ("D", "L2"), ("F", "L3"), ("B", "L4")),
}


def theta_rooting_audit(name):
    undirected = list(THETA_INTERNAL_UNDIRECTED + THETA_PENDANTS[name])
    directed = list(THETA_DIRECTED)
    nodes = set(THETA_TYPES)
    records = {}
    sites = [("U", edge) for edge in undirected] + [("D", edge) for edge in directed]
    for site_kind, site in sites:
        remaining_u = list(undirected)
        remaining_d = list(directed)
        if site_kind == "U":
            remaining_u.remove(site)
        else:
            remaining_d.remove(site)
        for bits in product((0, 1), repeat=len(remaining_u)):
            arcs = list(remaining_d)
            arcs.extend(
                edge if bit == 0 else (edge[1], edge[0])
                for edge, bit in zip(remaining_u, bits)
            )
            arcs.extend(((ROOT, site[0]), (ROOT, site[1])))
            valid, _reason = rooted_validation(nodes, arcs, THETA_TYPES, require_lsa=False)
            if not valid:
                continue
            code = tuple(sorted(arcs))
            records[code] = {
                "root_site": list(site),
                "lsa": root_is_lsa(nodes, arcs, ROOT, {"L1", "L2", "L3", "L4"}),
                "tree_child": tree_child(THETA_TYPES, arcs),
            }
    rows = list(records.values())
    assert len(rows) == 5
    assert sum(row["lsa"] for row in rows) == 5
    assert sum(row["tree_child"] for row in rows) == 2
    assert all(row["lsa"] for row in rows if not row["tree_child"])
    return {
        "admissible_rootings": len(rows),
        "lsa_valid": sum(row["lsa"] for row in rows),
        "tree_child": sum(row["tree_child"] for row in rows),
        "tree_child_root_sites": sorted(row["root_site"] for row in rows if row["tree_child"]),
        "non_tree_child_lsa_rootings": sum(
            row["lsa"] and not row["tree_child"] for row in rows
        ),
    }


def source_hashes(prior_root):
    selected = {
        "englander_level2_v4": prior_root / "englander_level2_v4.pdf",
        "brits_full_identifiability_v2": prior_root / "brits_full_identifiability_v2.pdf",
        "sullivant_graphical_models_v2": prior_root / "sullivant_graphical_models_v2.pdf",
    }
    return {name: {"path": str(path), "sha256": digest(path)} for name, path in selected.items()}


def build_report(prior_root):
    report = {
        "status": "DEFINITIONS_GATE_FAILS_PENDING_CONVENTION_REPAIR",
        "primary_source_hashes": source_hashes(prior_root),
        "theta_path_lengths": path_length_audit(),
        "simple_122_rootings": enumerate_k4e_rootings(),
        "parallel_112": enumerate_parallel_112_presentations(),
        "root_artifact_counterexample": root_artifact_counterexample(),
        "literal_two_subblob_counterexample": literal_two_subblob_counterexample(),
        "operational_biconnected_two_port": operational_biconnected_two_port_audit(),
        "theta_sharpness_rootings": {
            name: theta_rooting_audit(name) for name in ("N", "N_prime")
        },
        "locked_conclusions": {
            "tree_child_implies_lsa": True,
            "simple_two_triangle_core": "(1,2,2) only",
            "simple_122_has_tree_child_rooting": False,
            "parallel_112_is_standard_topology": False,
            "automatic_triangle_bound": "verified under the narrow simple standard rooting convention",
            "broad_reduction_and_local_S_TC_are_compatible": False,
            "theta_sharpness_membership": "W_TC minus S_TC survives LSA filtering",
            "general_two_subblob_scope": "unresolved until suppression is defined operationally",
        },
    }
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prior-root", type=Path, default=DEFAULT_PRIOR_ROOT)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    report = build_report(args.prior_root)
    print(json.dumps(report, sort_keys=True, indent=None if args.compact else 2))


if __name__ == "__main__":
    main()
