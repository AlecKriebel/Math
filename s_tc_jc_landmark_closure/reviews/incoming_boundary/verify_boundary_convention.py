#!/usr/bin/env python3
"""Exact independent audit of the incoming-boundary convention.

This verifier does not import either atlas implementation.  It reads two
machine-readable primitive records only as graph encodings, independently
enumerates all binary rootings of their standard mixed graphs, computes
literal and ordinary-triangle-quotient canonical codes, and checks the full
boundary group action.
"""

from __future__ import annotations

import gzip
import hashlib
import itertools
import json
from collections import defaultdict, deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
PRIMITIVES = PROJECT / "independent" / "decorated_atlas" / "certificates" / "p4_labelled_primitives.jsonl.gz"
ROOT_PROBE = PROJECT / "reviews" / "root_probe" / "incoming_coverage_certificate.json"
SOURCE_HASH = "25e272478915938e49b980ad172aa4f590f44fba8d0c50aaecf826fef7f46623"
TARGET_HASH = "2e3b531105573999bd129e4cfa105136cf074cf2924481e9d5f9aba13ae1932f"
PORT_MAP = (2, 3, 0, 1)  # source physical label i is attached to target rooted port PORT_MAP[i]


def stable(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value) -> str:
    if not isinstance(value, bytes):
        value = (value if isinstance(value, str) else stable(value)).encode()
    return hashlib.sha256(value).hexdigest()


def load_pair() -> tuple[dict, dict]:
    found = {}
    with gzip.open(PRIMITIVES, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            if row.get("graph_hash") in {SOURCE_HASH, TARGET_HASH}:
                found[row["graph_hash"]] = row
    if set(found) != {SOURCE_HASH, TARGET_HASH}:
        raise AssertionError(("primitive record missing", sorted(found)))
    return found[SOURCE_HASH], found[TARGET_HASH]


def edge_data(record: dict):
    directed = []
    undirected = []
    for kind, a, b in record["canonical_edges"]:
        if kind == "A":
            directed.append((int(a), int(b)))
        elif kind == "U":
            undirected.append((int(a), int(b)))
        else:
            raise AssertionError(("unknown edge kind", kind))
    return tuple(directed), tuple(undirected)


def physical_leaf_map(record: dict, target: bool = False) -> dict[int, int]:
    rooted_port_to_vertex = {int(k): int(v) for k, v in record["port_label_vertices"].items()}
    if not target:
        return {vertex: port for port, vertex in rooted_port_to_vertex.items()}
    inverse = {target_port: source_physical for source_physical, target_port in enumerate(PORT_MAP)}
    return {vertex: inverse[port] for port, vertex in rooted_port_to_vertex.items()}


def triangle_vertices(record: dict) -> frozenset[int] | None:
    directed, undirected = edge_data(record)
    edges = {tuple(sorted(e)) for e in (*directed, *undirected)}
    vertices = sorted({v for e in edges for v in e})
    triangles = [frozenset(c) for c in itertools.combinations(vertices, 3)
                 if all(tuple(sorted(e)) in edges for e in itertools.combinations(c, 2))]
    if len(triangles) > 1:
        raise AssertionError(("more than one triangle in witness", triangles))
    return triangles[0] if triangles else None


def canonical_code(record: dict, *, target: bool, triangle_quotient: bool) -> str:
    directed, undirected = edge_data(record)
    tri = triangle_vertices(record) if triangle_quotient else None
    mixed = []
    for a, b in directed:
        mixed.append(("U", min(a, b), max(a, b)) if tri and a in tri and b in tri else ("A", a, b))
    mixed.extend(("U", min(a, b), max(a, b)) for a, b in undirected)
    leaves = physical_leaf_map(record, target=target)
    vertices = sorted({v for _, a, b in mixed for v in (a, b)})
    internal = [v for v in vertices if v not in leaves]
    p = len(leaves)
    best = None
    for order in itertools.permutations(internal):
        relabel = {v: leaves[v] for v in leaves}
        relabel.update({v: p + i for i, v in enumerate(order)})
        edges = []
        for kind, a, b in mixed:
            aa, bb = relabel[a], relabel[b]
            edges.append((kind, aa, bb) if kind == "A" else (kind, min(aa, bb), max(aa, bb)))
        code = (p, tuple(sorted(edges)))
        if best is None or code < best:
            best = code
    assert best is not None
    return stable(best)


def is_dag(vertices: set[int], arcs: tuple[tuple[int, int], ...]) -> bool:
    indeg = {v: 0 for v in vertices}
    out = defaultdict(list)
    for a, b in arcs:
        indeg[b] += 1
        out[a].append(b)
    q = deque(v for v in vertices if indeg[v] == 0)
    seen = 0
    while q:
        v = q.popleft()
        seen += 1
        for w in out[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                q.append(w)
    return seen == len(vertices)


def rootable_ports(record: dict) -> tuple[int, ...]:
    fixed, ordinary = edge_data(record)
    port_to_vertex = {int(k): int(v) for k, v in record["port_label_vertices"].items()}
    leaves = set(port_to_vertex.values())
    retics = {b for _a, b in fixed}
    vertices0 = {v for edge in (*fixed, *ordinary) for v in edge}
    result = []
    for port, leaf in sorted(port_to_vertex.items()):
        incident = [e for e in ordinary if leaf in e]
        if len(incident) != 1:
            continue
        cut = incident[0]
        neighbor = cut[1] if cut[0] == leaf else cut[0]
        rest = [e for e in ordinary if e != cut]
        root = max(vertices0) + 1
        vertices = set(vertices0) | {root}
        for bits in itertools.product((0, 1), repeat=len(rest)):
            arcs = list(fixed) + [(root, leaf), (root, neighbor)]
            arcs.extend((b, a) if bit else (a, b) for bit, (a, b) in zip(bits, rest))
            indeg = defaultdict(int)
            out = defaultdict(list)
            for a, b in arcs:
                indeg[b] += 1
                out[a].append(b)
            if indeg[root] != 0 or len(out[root]) != 2:
                continue
            if any(indeg[v] != 1 or out[v] for v in leaves):
                continue
            good = True
            for v in vertices0 - leaves:
                expected = (2, 1) if v in retics else (1, 2)
                if (indeg[v], len(out[v])) != expected:
                    good = False
                    break
                if not any(child in leaves or child not in retics for child in out[v]):
                    good = False
                    break
                if v in retics and any(child in retics for child in out[v]):
                    good = False
                    break
            if not good or not is_dag(vertices, tuple(arcs)):
                continue
            reached = {root}
            q = [root]
            while q:
                v = q.pop()
                for w in out[v]:
                    if w not in reached:
                        reached.add(w)
                        q.append(w)
            if reached != vertices:
                continue
            result.append(port)
            break
    return tuple(result)


def record_from_mixed_witness(mixed: dict, role_to_physical: dict[str, int]) -> dict:
    nodes = sorted(node["id"] for node in mixed["nodes"])
    index = {name: i for i, name in enumerate(nodes)}
    labels = {node["id"]: node["label"] for node in mixed["nodes"] if node["label"] is not None}
    edges = []
    for edge in mixed["edges"]:
        a, b = edge["ends"]
        heads = edge["arrowheads"]
        if not heads:
            edges.append(["U", index[a], index[b]])
        elif heads == [a]:
            edges.append(["A", index[b], index[a]])
        elif heads == [b]:
            edges.append(["A", index[a], index[b]])
        else:
            raise AssertionError(("unsupported arrowhead record", edge))
    port_vertices = {}
    for vertex, role in labels.items():
        if role not in role_to_physical:
            raise AssertionError(("unmapped boundary role", role))
        port_vertices[str(role_to_physical[role])] = index[vertex]
    return {
        "schema": "independent-mixed-witness-record-v1",
        "canonical_edges": edges,
        "canonical_graph": {"order_size": len(nodes)},
        "port_label_vertices": port_vertices,
        "port_count": len(port_vertices),
        "core": "theta",
        "node_name_to_index": index,
    }


def all_rooting_census(record: dict) -> tuple[int, int]:
    fixed, ordinary = edge_data(record)
    port_vertices = set(int(v) for v in record["port_label_vertices"].values())
    retics = {b for _a, b in fixed}
    vertices0 = {v for edge in (*fixed, *ordinary) for v in edge}
    admissible = 0
    strong = 0
    for cut_kind, cut in [("U", e) for e in ordinary] + [("A", e) for e in fixed]:
        rest = [e for e in ordinary if not (cut_kind == "U" and e == cut)]
        retained_fixed = [e for e in fixed if not (cut_kind == "A" and e == cut)]
        root = max(vertices0) + 1
        vertices = set(vertices0) | {root}
        a0, b0 = cut
        for bits in itertools.product((0, 1), repeat=len(rest)):
            arcs = list(retained_fixed) + [(root, a0), (root, b0)]
            arcs.extend((b, a) if bit else (a, b) for bit, (a, b) in zip(bits, rest))
            indeg = defaultdict(int)
            out = defaultdict(list)
            for a, b in arcs:
                indeg[b] += 1
                out[a].append(b)
            if indeg[root] or len(out[root]) != 2:
                continue
            if any(indeg[v] != 1 or out[v] for v in port_vertices):
                continue
            valid = True
            for v in vertices0 - port_vertices:
                if (indeg[v], len(out[v])) != ((2, 1) if v in retics else (1, 2)):
                    valid = False
                    break
            if not valid or not is_dag(vertices, tuple(arcs)):
                continue
            reached = {root}
            q = [root]
            while q:
                v = q.pop()
                for w in out[v]:
                    if w not in reached:
                        reached.add(w)
                        q.append(w)
            if reached != vertices:
                continue
            admissible += 1
            # Tree-childness is imposed on internal vertices only.  Including
            # boundary leaves here makes every valid rooting fail vacuously,
            # because a leaf has no child.
            tree_child = all(
                any(child in port_vertices or child not in retics for child in out[v])
                for v in vertices0 - port_vertices
            )
            no_rr = all(not any(child in retics for child in out[v]) for v in retics)
            if tree_child and no_rr:
                strong += 1
    return admissible, strong


def ordinary_t_no_common_search() -> dict:
    rows = []
    with gzip.open(PRIMITIVES, "rt") as handle:
        rows = [json.loads(line) for line in handle]
    source_rows = []
    for record in rows:
        source_rows.append((
            canonical_code(record, target=False, triangle_quotient=True),
            canonical_code(record, target=False, triangle_quotient=False),
            set(rootable_ports(record)),
            record["graph_hash"],
        ))
    global PORT_MAP
    original = PORT_MAP
    matches = []
    comparisons = 0
    try:
        for permutation in itertools.permutations(range(4)):
            PORT_MAP = permutation
            inverse = {target_port: source_physical for source_physical, target_port in enumerate(permutation)}
            for target in rows:
                target_roots = {inverse[x] for x in rootable_ports(target)}
                target_t = canonical_code(target, target=True, triangle_quotient=True)
                target_literal = canonical_code(target, target=True, triangle_quotient=False)
                for source_t, source_literal, source_roots, source_hash in source_rows:
                    comparisons += 1
                    if source_t == target_t and source_literal != target_literal and not (source_roots & target_roots):
                        matches.append({
                            "source": source_hash,
                            "target": target["graph_hash"],
                            "port_map": list(permutation),
                            "source_rootable": sorted(source_roots),
                            "target_rootable": sorted(target_roots),
                        })
    finally:
        PORT_MAP = original
    return {
        "primitive_record_count": len(rows),
        "boundary_permutation_count": 24,
        "ordered_comparisons": comparisons,
        "ordinary_T_no_common_incoming_matches": matches,
    }


def group_action_certificate(p: int) -> dict:
    perms = tuple(itertools.permutations(range(p)))
    fixed = tuple(q for q in perms if q[0] == 0)
    relative = set()
    fibers = defaultdict(int)
    for alpha in perms:
        alpha_inverse = {value: i for i, value in enumerate(alpha)}
        for beta in perms:
            rel = tuple(alpha_inverse[value] for value in beta)
            relative.add(rel)
            fibers[rel] += 1
    return {
        "degree": p,
        "full_group_size": len(perms),
        "fixed_incoming_subgroup_size": len(fixed),
        "simultaneous_assignment_pairs": len(perms) ** 2,
        "relative_orbit_size": len(relative),
        "relative_fiber_sizes": sorted(set(fibers.values())),
        "witness_permutation": list(PORT_MAP),
        "witness_in_full_group": PORT_MAP in relative,
        "witness_in_fixed_incoming_subgroup": PORT_MAP in fixed,
    }


def main() -> None:
    # First preserve and independently correct the proposed ordinary-T
    # witness from the research log.
    proposed_source, proposed_target = load_pair()
    for side, record in (("source", proposed_source), ("target", proposed_target)):
        if not all(record["validation"].values()):
            raise AssertionError((side, record["validation"]))
        if int(record["port_count"]) != 4 or record["core"] != "theta":
            raise AssertionError((side, record["port_count"], record["core"]))

    proposed_source_roots = rootable_ports(proposed_source)
    target_roots_in_target_labels = rootable_ports(proposed_target)
    inverse = {target_port: source_physical for source_physical, target_port in enumerate(PORT_MAP)}
    proposed_target_roots = tuple(sorted(inverse[x] for x in target_roots_in_target_labels))
    proposed_t_related = (
        canonical_code(proposed_source, target=False, triangle_quotient=True)
        == canonical_code(proposed_target, target=True, triangle_quotient=True)
    )
    if proposed_source_roots != (0, 1) or proposed_target_roots != (1, 2) or not proposed_t_related:
        raise AssertionError(("proposed-witness audit changed", proposed_source_roots, proposed_target_roots, proposed_t_related))

    # The genuine minimal witness is the TT-nested support with two physical
    # label assignments whose admissible rootable boundary sets are disjoint.
    root_probe = json.loads(ROOT_PROBE.read_text())
    witness = root_probe["counterexample"]
    role_names = ("incoming", "repair:p0e2", "sink:X1", "sink:X2")
    source_role_to_physical = dict(zip(role_names, range(4)))
    target_role_to_physical = {"incoming": 2, "repair:p0e2": 3, "sink:X1": 0, "sink:X2": 1}
    source = record_from_mixed_witness(witness["mixed_graph"], source_role_to_physical)
    target = record_from_mixed_witness(witness["mixed_graph"], target_role_to_physical)
    source_roots = rootable_ports(source)
    target_roots = rootable_ports(target)
    if source_roots != (0, 1) or target_roots != (2, 3):
        raise AssertionError(("minimal-witness rootable sets", source_roots, target_roots))
    if set(source_roots) & set(target_roots):
        raise AssertionError("minimal witness unexpectedly has a common incoming")
    source_rooting_census = all_rooting_census(source)
    target_rooting_census = all_rooting_census(target)
    if source_rooting_census != (9, 9) or target_rooting_census != (9, 9):
        raise AssertionError(("unexpected rooting census", source_rooting_census, target_rooting_census))

    search = ordinary_t_no_common_search()
    if search["ordinary_T_no_common_incoming_matches"]:
        raise AssertionError(("ordinary-T witness unexpectedly exists", search["ordinary_T_no_common_incoming_matches"][:3]))

    certificate = {
        "schema": "incoming-boundary-minimal-counterexample-v2",
        "status": "EXACTLY_COMPUTED",
        "source_record": source,
        "target_record": target,
        "source_role_to_physical": source_role_to_physical,
        "target_role_to_physical": target_role_to_physical,
        "relative_target_permutation": [2, 3, 0, 1],
        "source_rootable_physical_boundaries": list(source_roots),
        "target_rootable_physical_boundaries": list(target_roots),
        "common_rootable_physical_boundaries": [],
        "source_rooting_census": {"admissible": source_rooting_census[0], "strong_tree_child": source_rooting_census[1]},
        "target_rooting_census": {"admissible": target_rooting_census[0], "strong_tree_child": target_rooting_census[1]},
        "group_action": group_action_certificate(4),
        "minimality": (
            "At p=3 the only rigid strong support is the one-reticulation cycle; "
            "each presentation has two rootable boundaries, and two 2-subsets "
            "of a 3-set intersect. The first disjoint-rootability case is p=4."
        ),
        "ordinary_T_if_available_search": search,
        "withdrawn_proposed_ordinary_T_witness_audit": {
            "source_hash": SOURCE_HASH,
            "target_hash": TARGET_HASH,
            "port_map": list(PORT_MAP),
            "ordinary_T_related": proposed_t_related,
            "source_rootable_physical_boundaries": list(proposed_source_roots),
            "target_rootable_physical_boundaries": list(proposed_target_roots),
            "common_rootable_physical_boundaries": sorted(set(proposed_source_roots) & set(proposed_target_roots)),
            "verdict": "FALSE_AS_NO_COMMON_INCOMING_WITNESS",
        },
        "conclusion": (
            "There is no theorem reducing every standard semi-directed relation "
            "to a common admissible incoming boundary. The complete relative "
            "boundary action is S_p; rooted incoming status is provenance only."
        ),
        "primitive_input_sha256": digest(PRIMITIVES.read_bytes()),
        "root_probe_input_sha256": digest(ROOT_PROBE.read_bytes()),
    }
    certificate["body_sha256"] = digest(certificate)
    output = HERE / "encodings" / "minimal_no_common_incoming.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(certificate, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": "PASS",
        "output": str(output),
        "body_sha256": certificate["body_sha256"],
        "source_rootable": source_roots,
        "target_rootable": target_roots,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
