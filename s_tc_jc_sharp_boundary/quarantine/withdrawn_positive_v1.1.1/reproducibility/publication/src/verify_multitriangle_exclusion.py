#!/usr/bin/env python3
"""Exact primitive audit: weakly tree-child level-2 blobs have at most one triangle.

The mathematical proof is structural.  This script independently checks its sole
finite local case, the theta subdivision with path lengths (1,2,2), by enumerating
all binary acyclic rootings.  It does not import the phylogenetic atlas code.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
CERT = HERE / "certificates" / "multitriangle_exclusion.json"

CORE_VERTICES = ("u", "v", "a", "b")
CORE_EDGES = (("u", "v"), ("u", "a"), ("a", "v"), ("u", "b"), ("b", "v"))
PORT_VERTICES = ("a", "b")


def is_dag_and_reachable(nodes, arcs, root="rho"):
    indeg = Counter(head for _tail, head in arcs)
    children = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    queue = deque(node for node in nodes if indeg[node] == 0)
    seen_order = []
    work = Counter(indeg)
    while queue:
        node = queue.popleft()
        seen_order.append(node)
        for child in children[node]:
            work[child] -= 1
            if work[child] == 0:
                queue.append(child)
    if len(seen_order) != len(nodes):
        return False
    reached = {root}
    queue = deque((root,))
    while queue:
        node = queue.popleft()
        for child in children[node]:
            if child not in reached:
                reached.add(child)
                queue.append(child)
    return reached == set(nodes)


def tree_child(types, arcs):
    children = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    for vertex, kind in types.items():
        if kind in {"S", "T"}:
            if not any(types[child] in {"T", "L"} for child in children[vertex]):
                return False
        elif kind == "R":
            if len(children[vertex]) != 1 or types[children[vertex][0]] == "R":
                return False
    return True


def bidegrees(arcs):
    return Counter(head for _tail, head in arcs), Counter(tail for tail, _head in arcs)


def failure_reason(types, arcs):
    children = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    for vertex in sorted(types):
        if types[vertex] == "R" and children[vertex] and types[children[vertex][0]] == "R":
            return {"kind": "reticulation_child", "witness": vertex}
    for vertex in sorted(types):
        if types[vertex] in {"S", "T"} and children[vertex] and all(
            types[child] == "R" for child in children[vertex]
        ):
            return {"kind": "all_children_reticulate", "witness": vertex}
    raise AssertionError("non-tree-child rooting lacks a certified local witness")


def enumerate_external_rootings():
    records = []
    attempts = 0
    for entry in PORT_VERTICES:
        exit_vertex = "b" if entry == "a" else "a"
        nodes = ("rho", "out", "down") + CORE_VERTICES
        for retics in combinations(CORE_VERTICES, 2):
            types = {"rho": "S", "out": "L", "down": "L"}
            types.update({v: ("R" if v in retics else "T") for v in CORE_VERTICES})
            expected = {"rho": (0, 2), "out": (1, 0), "down": (1, 0)}
            expected.update({v: ((2, 1) if v in retics else (1, 2)) for v in CORE_VERTICES})
            for bits in product((0, 1), repeat=len(CORE_EDGES)):
                attempts += 1
                arcs = [("rho", entry), ("rho", "out"), (exit_vertex, "down")]
                arcs.extend(
                    (left, right) if bit == 0 else (right, left)
                    for (left, right), bit in zip(CORE_EDGES, bits)
                )
                indeg, outdeg = bidegrees(arcs)
                if any((indeg[v], outdeg[v]) != expected[v] for v in nodes):
                    continue
                if not is_dag_and_reachable(nodes, arcs):
                    continue
                is_tc = tree_child(types, arcs)
                records.append({
                    "mode": "root_outside_blob",
                    "root_site": f"port-{entry}",
                    "reticulations": list(retics),
                    "arcs": [list(edge) for edge in arcs],
                    "tree_child": is_tc,
                    "failure": None if is_tc else failure_reason(types, arcs),
                })
    return attempts, records


def enumerate_internal_rootings():
    records = []
    attempts = 0
    for root_edge in CORE_EDGES:
        remaining = tuple(edge for edge in CORE_EDGES if edge != root_edge)
        nodes = ("rho", "la", "lb") + CORE_VERTICES
        for retics in combinations(CORE_VERTICES, 2):
            types = {"rho": "S", "la": "L", "lb": "L"}
            types.update({v: ("R" if v in retics else "T") for v in CORE_VERTICES})
            expected = {"rho": (0, 2), "la": (1, 0), "lb": (1, 0)}
            expected.update({v: ((2, 1) if v in retics else (1, 2)) for v in CORE_VERTICES})
            for bits in product((0, 1), repeat=len(remaining)):
                attempts += 1
                left, right = root_edge
                arcs = [("rho", left), ("rho", right), ("a", "la"), ("b", "lb")]
                arcs.extend(
                    (x, y) if bit == 0 else (y, x)
                    for (x, y), bit in zip(remaining, bits)
                )
                indeg, outdeg = bidegrees(arcs)
                if any((indeg[v], outdeg[v]) != expected[v] for v in nodes):
                    continue
                if not is_dag_and_reachable(nodes, arcs):
                    continue
                is_tc = tree_child(types, arcs)
                records.append({
                    "mode": "root_inside_blob",
                    "root_site": "-".join(root_edge),
                    "reticulations": list(retics),
                    "arcs": [list(edge) for edge in arcs],
                    "tree_child": is_tc,
                    "failure": None if is_tc else failure_reason(types, arcs),
                })
    return attempts, records


def automorphisms():
    answer = []
    edge_set = {frozenset(edge) for edge in CORE_EDGES}
    for swap_poles in (False, True):
        for swap_ports in (False, True):
            mapping = {
                "u": "v" if swap_poles else "u",
                "v": "u" if swap_poles else "v",
                "a": "b" if swap_ports else "a",
                "b": "a" if swap_ports else "b",
            }
            image = {frozenset((mapping[x], mapping[y])) for x, y in CORE_EDGES}
            if image == edge_set:
                answer.append(mapping)
    assert len(answer) == 4
    return tuple(answer)


def canonical_record(record):
    images = []
    for mapping in automorphisms():
        retics = tuple(sorted(mapping[v] for v in record["reticulations"]))
        core_arcs = []
        for tail, head in record["arcs"]:
            if tail in CORE_VERTICES and head in CORE_VERTICES:
                core_arcs.append((mapping[tail], mapping[head]))
            elif tail == "rho" and head in CORE_VERTICES:
                core_arcs.append(("rho", mapping[head]))
            elif tail in CORE_VERTICES and head in {"la", "lb", "down"}:
                core_arcs.append((mapping[tail], "leaf"))
            elif tail == "rho" and head == "out":
                core_arcs.append(("rho", "outgroup"))
        if record["mode"] == "root_outside_blob":
            old = record["root_site"].split("-")[1]
            site = "port-" + mapping[old]
        else:
            left, right = record["root_site"].split("-")
            site = "-".join(sorted((mapping[left], mapping[right])))
        images.append((record["mode"], site, retics, tuple(sorted(core_arcs))))
    return min(images)


def path_length_audit(limit=12):
    triples = []
    for lengths in product(range(1, limit + 1), repeat=3):
        if tuple(sorted(lengths)) != lengths:
            continue
        if sum(length == 1 for length in lengths) > 1:
            continue  # a simple theta cannot have two parallel one-edge paths
        triangle_pairs = [pair for pair in combinations(range(3), 2) if lengths[pair[0]] + lengths[pair[1]] == 3]
        if len(triangle_pairs) >= 2:
            triples.append({"lengths": list(lengths), "triangle_pairs": [list(pair) for pair in triangle_pairs]})
    assert triples == [{"lengths": [1, 2, 2], "triangle_pairs": [[0, 1], [0, 2]]}]
    return triples


def generate_certificate():
    ext_attempts, external = enumerate_external_rootings()
    int_attempts, internal = enumerate_internal_rootings()
    records = external + internal
    assert ext_attempts == 384
    assert int_attempts == 480
    assert len(external) == 4
    assert len(internal) == 21
    assert len(records) == 25
    assert not any(record["tree_child"] for record in records)

    groups = defaultdict(list)
    for index, record in enumerate(records):
        groups[canonical_record(record)].append(index)
    orbit_sizes = sorted(len(indices) for indices in groups.values())
    assert orbit_sizes == [1, 4, 4, 4, 4, 4, 4]

    failure_counts = Counter(record["failure"]["kind"] for record in records)
    assert failure_counts == {"all_children_reticulate": 5, "reticulation_child": 20}

    # Structural obstruction behind the enumeration.
    nonedge = frozenset(("a", "b"))
    all_pairs = {frozenset(pair) for pair in combinations(CORE_VERTICES, 2)}
    edge_pairs = {frozenset(edge) for edge in CORE_EDGES}
    assert all_pairs - edge_pairs == {nonedge}

    compact_records = []
    for index, record in enumerate(records):
        compact = dict(record)
        compact["id"] = index
        compact["canonical_orbit_sha256"] = sha256(repr(canonical_record(record)).encode()).hexdigest()
        compact_records.append(compact)

    orbit_records = []
    for orbit_id, (code, indices) in enumerate(sorted(groups.items(), key=lambda item: item[0])):
        orbit_records.append({
            "id": orbit_id,
            "size": len(indices),
            "member_ids": indices,
            "canonical_code": repr(code),
            "canonical_code_sha256": sha256(repr(code).encode()).hexdigest(),
        })

    return {
        "status": "PROVED",
        "theorem": "Every binary standard semi-directed weakly tree-child level-2 network has at most one triangle in each blob.",
        "structural_reduction": {
            "blob_cycle_rank_equals_reticulation_count": True,
            "level_two_reduced_cores": ["cycle", "theta"],
            "two_triangle_theta_path_lengths": [1, 2, 2],
            "path_length_search_check": path_length_audit(),
            "multi_triangle_simple_core": {
                "vertices": list(CORE_VERTICES),
                "edges": [list(edge) for edge in CORE_EDGES],
                "description": "K4 minus the nonedge a-b",
                "port_vertices": list(PORT_VERTICES),
            },
        },
        "orientation_universe": {
            "raw_binary_orientation_attempts": ext_attempts + int_attempts,
            "root_outside_attempts": ext_attempts,
            "root_inside_attempts": int_attempts,
            "valid_binary_acyclic_rootings": len(records),
            "valid_root_outside_blob": len(external),
            "valid_root_inside_blob": len(internal),
            "tree_child_rootings": 0,
            "automorphism_group_order": len(automorphisms()),
            "rooted_orientation_orbits": len(groups),
            "orbit_size_multiset": orbit_sizes,
            "failure_counts": dict(sorted(failure_counts.items())),
        },
        "conceptual_cases": {
            "adjacent_reticulations": "Either their edge is a reticulation-to-reticulation arc, or the root subdivides it and has two reticulation children.",
            "nonadjacent_reticulations": "They must be a and b. Their incident bridges cannot enter a reticulation. The root is therefore inside the blob; whichever pole is opposite the root edge has both reticulations as children (both poles do when the root subdivides u-v).",
        },
        "records": compact_records,
        "orbits": orbit_records,
    }


def main():
    certificate = generate_certificate()
    CERT.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if CERT.exists():
        assert json.loads(CERT.read_text()) == certificate
    else:
        CERT.write_text(text)
    print(json.dumps({
        "status": certificate["status"],
        "valid_binary_acyclic_rootings": certificate["orientation_universe"]["valid_binary_acyclic_rootings"],
        "rooted_orientation_orbits": certificate["orientation_universe"]["rooted_orientation_orbits"],
        "tree_child_rootings": certificate["orientation_universe"]["tree_child_rootings"],
        "two_triangle_path_lengths": certificate["structural_reduction"]["two_triangle_theta_path_lengths"],
    }, indent=2, sort_keys=True))
    print("MULTI-TRIANGLE EXCLUSION VERIFIED")


if __name__ == "__main__":
    main()
