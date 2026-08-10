#!/usr/bin/env python3
"""Clean-room structural audit of the schema-3 theta-2 p/q probe stream.

The primary streams are treated only as claimed records.  This program uses
the independent graph implementation in this review directory to reconstruct
standard semi-directed membership, topology classes, insertion children,
per-parent Cartesian child sets, and every stated isomorphism transport.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
import gzip
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from graph_model import (
    RootedGraph, digest, mixed_code, rooted_code, stable_json,
    standard_semidirected_audit, semidirected,
)
from pq_extension import cyclic_blob_arcs
from relation_universe import graph_from_object


SUMMARY = ROOT / "primary/certificates/probe_extension_theta2_schema3_summary.json"
BASE_STATES = ROOT / "primary/certificates/hard_cover_n4_schema3_theta2_full.jsonl.gz"
BASE_GRAPHS = ROOT / "primary/certificates/hard_cover_graphs_n4_schema3_theta2_full.jsonl.gz"
FULL_BASE_AUDIT = HERE / "certificates/schema3_n4_theta2_full_audit.json"
OUT = HERE / "certificates/schema3_n4_theta2_probe_structure_audit.json"
FIRST_FAILURE = HERE / "history/implementation_failures/probe_extension_first_failure.json"


class AuditFailure(RuntimeError):
    pass


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def logical_jsonl_sha(path: Path) -> str:
    """Hash the decompressed JSONL bytes committed by a stream summary."""
    h = hashlib.sha256()
    with gzip.open(path, "rb") as stream:
        for line in stream:
            h.update(line)
    return h.hexdigest()


def jsonl(path: Path):
    with gzip.open(path, "rt") as stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)


def preserve_first_failure(category, **details):
    payload = {
        "schema": 1,
        "status": "FALSE",
        "category": category,
        "details": details,
        "summary_path": str(SUMMARY.relative_to(ROOT)),
        "summary_sha256": sha(SUMMARY),
    }
    payload["normalized_sha256_without_hash"] = digest(payload)
    FIRST_FAILURE.parent.mkdir(parents=True, exist_ok=True)
    if not FIRST_FAILURE.exists():
        FIRST_FAILURE.write_text(stable_json(payload) + "\n")
    raise AuditFailure(stable_json(payload))


def require(condition, category, **details):
    if not condition:
        preserve_first_failure(category, **details)


@dataclass(frozen=True)
class GraphInfo:
    graph: RootedGraph
    raw_sha256: str
    rooted_code: str
    rooted_sha256: str
    mixed_code: str
    mixed_sha256: str
    t_code: str
    t_sha256: str
    cyclic_arcs: tuple
    selected_count: int


def labels_are_consecutive(g: RootedGraph):
    labels = sorted(g.label_map.values())
    return labels == [f"L_{i}" for i in range(len(labels))]


def graph_info(g: RootedGraph, require_consecutive_labels=True) -> GraphInfo:
    audit = standard_semidirected_audit(g)
    require(audit["ok"], "graph outside locked standard S_TC class", audit=audit)
    if require_consecutive_labels:
        require(labels_are_consecutive(g), "selected labels are not consecutive", labels=sorted(g.label_map.values()))
    rcode = rooted_code(g)[0]
    mcode = mixed_code(g)[0]
    tcode = mixed_code(g, True)[0]
    return GraphInfo(
        graph=g,
        raw_sha256=digest({"arcs": g.arcs, "root": g.root, "labels": g.labels}),
        rooted_code=rcode,
        rooted_sha256=digest(rcode),
        mixed_code=mcode,
        mixed_sha256=digest(mcode),
        t_code=tcode,
        t_sha256=digest(tcode),
        cyclic_arcs=tuple(cyclic_blob_arcs(g)),
        selected_count=len([label for label in g.label_map.values() if label.startswith("L_")]),
    )


def load_graph_library(path: Path, require_declared_arcs=False, require_consecutive_labels=True):
    graphs = {}
    raw_ids = {}
    for index, rec in enumerate(jsonl(path)):
        gid = rec["graph_id"]
        require(gid not in graphs, "duplicate graph_id", graph_id=gid, index=index)
        info = graph_info(graph_from_object(rec["rooted_graph"]), require_consecutive_labels)
        require(info.raw_sha256 not in raw_ids, "duplicate exact rooted graph payload under distinct graph IDs", graph_id=gid, prior_graph_id=raw_ids.get(info.raw_sha256))
        raw_ids[info.raw_sha256] = gid
        require(bool(rec.get("rooted_valid")), "primary rooted-valid flag false", graph_id=gid)
        require(bool(rec.get("standard_strong_local")), "primary standard-strong flag false", graph_id=gid)
        if require_declared_arcs:
            require("admissible_internal_arcs" in rec, "probe graph lacks declared admissible arcs", graph_id=gid)
            declared = tuple(tuple(x) for x in rec["admissible_internal_arcs"])
            require(declared == info.cyclic_arcs, "admissible arc set differs from independent blob arcs", graph_id=gid, declared=declared, independent=info.cyclic_arcs)
        graphs[gid] = info
    return graphs


def raw_mixed_representation(g: RootedGraph, vertex_to_position, erase_triangle=False):
    vertices, edges, labels = semidirected(g)
    if erase_triangle:
        # The independent topology test itself uses mixed_code(..., True).
        # Transport records in this stream are all labelled isomorphisms, so
        # this branch is retained only to make the checker explicit.
        raise NotImplementedError("no T terminal occurs in this stream")
    mp = dict(vertex_to_position)
    require(set(mp) == set(vertices), "canonicalization misses vertices", expected=sorted(vertices), actual=sorted(mp))
    require(set(mp.values()) == set(range(len(vertices))), "canonicalization positions are not a bijection", values=sorted(mp.values()))
    colours = tuple(sorted((mp[v], "LEAF:" + labels[v] if v in labels else "INTERNAL") for v in vertices))
    rels = []
    for (u, v), (hu, hv) in edges.items():
        a, b = mp[u], mp[v]
        if a > b:
            a, b, hu, hv = b, a, hv, hu
        rels.append((a, b, hu, hv))
    return colours, tuple(sorted(rels))


def raw_mixed_edges(g: RootedGraph):
    _, edges, _ = semidirected(g)
    return tuple(sorted((u, v, hu, hv) for (u, v), (hu, hv) in edges.items()))


def actual_reticulations(g: RootedGraph):
    indeg, outdeg, _, _ = g.degrees()
    return tuple(sorted(v for v in g.vertices if (indeg[v], outdeg[v]) == (2, 1)))


def validate_transport(source: GraphInfo, target: GraphInfo, canonicalization, transport, context):
    require(source.mixed_code == target.mixed_code, "transport supplied for nonisomorphic mixed graphs", context=context)
    require(canonicalization is not None and transport is not None, "missing isomorphism transport", context=context)
    smap = tuple(tuple(x) for x in canonicalization["source_raw_to_canonical"])
    tmap = tuple(tuple(x) for x in canonicalization["target_raw_to_canonical"])
    sr = raw_mixed_representation(source.graph, smap)
    tr = raw_mixed_representation(target.graph, tmap)
    require(sr == tr, "claimed common canonicalization is not a mixed-graph isomorphism", context=context)
    sinv = {position: vertex for vertex, position in smap}
    tinv = {position: vertex for vertex, position in tmap}
    expected_vertex = tuple(sorted((sinv[p], tinv[p]) for p in sinv))
    stated_vertex = tuple(tuple(x) for x in transport["vertex_transport"])
    require(stated_vertex == expected_vertex, "vertex transport differs from canonicalization-induced map", context=context)
    vertex_map = dict(stated_vertex)
    slabels = source.graph.label_map; tlabels = target.graph.label_map
    for v, label in slabels.items():
        require(tlabels.get(vertex_map[v]) == label, "transport changes a port label", context=context, vertex=v, label=label)
    expected_ports = tuple((f"L_{i}", f"L_{i}") for i in range(source.selected_count))
    require(tuple(tuple(x) for x in transport["port_transport"]) == expected_ports, "port transport is not the complete identity matching", context=context)
    sret = actual_reticulations(source.graph); tret = actual_reticulations(target.graph)
    require(tuple(transport["reticulation_vertices_source"]) == sret, "source reticulation list is wrong", context=context)
    require(tuple(transport["reticulation_vertices_target"]) == tret, "target reticulation list is wrong", context=context)
    expected_retic = tuple(sorted((v, vertex_map[v]) for v in sret))
    require(tuple(tuple(x) for x in transport["reticulation_transport_outside_redirected_triangle"]) == expected_retic, "reticulation transport is wrong", context=context)

    sedges = raw_mixed_edges(source.graph); tedges = raw_mixed_edges(target.graph)
    permutation = tuple(tuple(x) for x in transport["t_quotient_edge_permutation"])
    require(tuple(i for i, _ in permutation) == tuple(range(len(sedges))), "edge transport does not cover source edges once", context=context)
    require(tuple(sorted(j for _, j in permutation)) == tuple(range(len(tedges))), "edge transport does not cover target edges once", context=context)
    for i, j in permutation:
        u, v, hu, hv = sedges[i]
        a, b = vertex_map[u], vertex_map[v]
        if a > b:
            a, b, hu, hv = b, a, hv, hu
        require((a, b, hu, hv) == tedges[j], "edge transport fails to preserve an arrowheaded edge", context=context, source_edge_index=i, target_edge_index=j)


def exact_insert(parent: RootedGraph, insertion):
    arc = tuple(insertion["subdivided_parent_arc"])
    tree = int(insertion["inserted_tree_vertex"])
    leaf = int(insertion["inserted_leaf_vertex"])
    label = str(insertion["inserted_label"])
    require(arc in parent.arcs, "insertion subdivides a nonexistent parent arc", arc=arc)
    require(tree not in parent.vertices and leaf not in parent.vertices and tree != leaf, "inserted vertices are not fresh", arc=arc, tree=tree, leaf=leaf)
    require(label not in parent.label_map.values(), "inserted label already exists", label=label)
    arcs = set(parent.arcs); arcs.remove(arc)
    arcs.update(((arc[0], tree), (tree, arc[1]), (tree, leaf)))
    labels = parent.label_map; labels[leaf] = label
    return RootedGraph.make(arcs, parent.root, labels)


def same_exact_graph(a: RootedGraph, b: RootedGraph):
    return a == b


def load_base_paths(base_graphs):
    base_paths = {}; base_state_count = 0
    for state in jsonl(BASE_STATES):
        if state["terminal_classification"] not in ("support_prefix_labelled_isomorphism", "labelled_isomorphism"):
            continue
        base_state_count += 1
        require(len(state["raw_coverage"]) == 1, "base terminal has more than one path provenance", state_id=state["state_id"], path_count=len(state["raw_coverage"]))
        cov = state["raw_coverage"][0]
        pid = cov["path_binding_id"]
        require(pid not in base_paths, "duplicate base path binding", path_binding_id=pid)
        s = base_graphs[state["source_graph_id"]]; t = base_graphs[state["target_graph_id"]]
        require(s.mixed_code == t.mixed_code, "base terminal is not independently isomorphic", state_id=state["state_id"])
        base_paths[pid] = {
            "state_id": state["state_id"],
            "root_case_id": state["fixed_full_root_case_id"],
            "source": s,
            "target": t,
            "selected_count": state["selected_port_count"],
            "dummy_order": tuple(cov["dummy_order"]),
            "restored_role_to_label": tuple(tuple(x) for x in cov["restored_role_to_label"]),
        }
    require(base_state_count == 132 and len(base_paths) == 132, "wrong base terminal universe", states=base_state_count, paths=len(base_paths))
    return base_paths


def validate_polynomial_library(path: Path):
    polynomials = {}
    for rec in jsonl(path):
        pid = rec["polynomial_id"]
        require(pid not in polynomials, "duplicate primary polynomial id", polynomial_id=pid)
        terms = tuple((tuple(m), int(c)) for m, c in rec["terms"])
        require(all(c for _, c in terms), "zero coefficient in primary polynomial", polynomial_id=pid)
        require(len({m for m, _ in terms}) == len(terms), "duplicate monomial in primary polynomial", polynomial_id=pid)
        require(all(len(m) == int(rec["variable_count"]) for m, _ in terms), "primary polynomial exponent length mismatch", polynomial_id=pid)
        polynomials[pid] = rec
    return polynomials


def validate_probe_states(path: Path, graphs, polynomials):
    states = {}; counts = Counter(); referenced_polynomials = set(); normalized = []
    for rec in jsonl(path):
        sid = rec["state_id"]
        require(sid not in states, "duplicate probe state", state_id=sid)
        sgid, tgid = rec["source_graph_id"], rec["target_graph_id"]
        require(sgid in graphs and tgid in graphs, "probe state references missing graph", state_id=sid, source_graph_id=sgid, target_graph_id=tgid)
        source, target = graphs[sgid], graphs[tgid]
        p = int(rec["selected_port_count"])
        require(source.selected_count == target.selected_count == p, "selected-port count differs from graph labels", state_id=sid, declared=p, source=source.selected_count, target=target.selected_count)
        classification = rec["classification"]
        own_topology = "labelled_isomorphism" if source.mixed_code == target.mixed_code else ("ordinary_T" if source.t_code == target.t_code else "non_T")
        if classification == "labelled_isomorphism":
            require(own_topology == "labelled_isomorphism", "false labelled-isomorphism terminal", state_id=sid, independent_topology=own_topology)
            require(rec["probe_classification"] == "equal_invariant_signature", "isomorphism state lacks equal probe signature", state_id=sid)
            validate_transport(source, target, rec["canonicalization"], rec["transport"], {"state_id": sid, "kind": "terminal"})
        elif classification == "generic_polynomial_separation":
            require(own_topology == "non_T", "polynomial terminal is already isomorphic or T-related", state_id=sid, independent_topology=own_topology)
            require(rec["canonicalization"] is None and rec["transport"] is None, "separated state unexpectedly carries a topology transport", state_id=sid)
            witness = rec["probe_witness"]
            require(witness.get("target_pullback") == "0", "primary witness does not claim a target identity", state_id=sid)
            pid = witness.get("source_pullback_id")
            require(pid in polynomials, "state references missing primary polynomial body", state_id=sid, polynomial_id=pid)
            referenced_polynomials.add(pid)
        else:
            preserve_first_failure("unknown probe terminal classification", state_id=sid, classification=classification)
        counts[(rec["stage"], classification)] += 1
        normalized.append({
            "state_id": sid,
            "stage": rec["stage"],
            "selected_port_count": p,
            "source_rooted_sha256": source.rooted_sha256,
            "target_rooted_sha256": target.rooted_sha256,
            "source_exact_rooted_sha256": source.raw_sha256,
            "target_exact_rooted_sha256": target.raw_sha256,
            "source_mixed_sha256": source.mixed_sha256,
            "target_mixed_sha256": target.mixed_sha256,
            "classification": classification,
            "independent_topology": own_topology,
        })
        states[sid] = rec
    require(referenced_polynomials == set(polynomials), "primary polynomial library has missing or unreferenced bodies", missing=sorted(referenced_polynomials-set(polynomials)), unreferenced=sorted(set(polynomials)-referenced_polynomials))
    return states, counts, digest(sorted(normalized, key=lambda x: x["state_id"]))


def validate_base_metadata(binding, base):
    require(binding["base_state_id"] == base["state_id"], "binding changes base state", probe_path_binding_id=binding["probe_path_binding_id"])
    require(binding["restoration_root_id"] == base["root_case_id"], "binding changes fixed restoration root", probe_path_binding_id=binding["probe_path_binding_id"])
    require(tuple(binding["base_dummy_order"]) == base["dummy_order"], "binding changes base dummy order", probe_path_binding_id=binding["probe_path_binding_id"])
    require(tuple(tuple(x) for x in binding["base_restored_role_to_label"]) == base["restored_role_to_label"], "binding changes restored role/label map", probe_path_binding_id=binding["probe_path_binding_id"])


def validate_child_side(binding, side, graphs, expected_label):
    pgid = binding[f"{side}_parent_graph_id"]
    cgid = binding[f"{side}_child_graph_id"]
    require(pgid in graphs and cgid in graphs, "binding references missing parent/child graph", probe_path_binding_id=binding["probe_path_binding_id"], side=side)
    parent, child = graphs[pgid], graphs[cgid]
    insertion = binding[f"{side}_insertion"]
    require(insertion["inserted_label"] == expected_label, "wrong sequential probe label", probe_path_binding_id=binding["probe_path_binding_id"], side=side, expected=expected_label, actual=insertion["inserted_label"])
    require(tuple(insertion["subdivided_parent_arc"]) in parent.cyclic_arcs, "probe inserted outside active blob segment", probe_path_binding_id=binding["probe_path_binding_id"], side=side, arc=insertion["subdivided_parent_arc"])
    rebuilt = exact_insert(parent.graph, insertion)
    require(same_exact_graph(rebuilt, child.graph), "child graph is not the stated exact arc subdivision", probe_path_binding_id=binding["probe_path_binding_id"], side=side, parent_graph_id=pgid, child_graph_id=cgid)
    require(bool(binding[f"{side}_deletion_exact_parent"]), "primary deletion flag false", probe_path_binding_id=binding["probe_path_binding_id"], side=side)
    return parent, child, tuple(insertion["subdivided_parent_arc"])


def validate_binding_stream(path: Path, states, graphs, base_paths):
    # Pass 1 binds every p path before q records are interpreted.  The file is
    # deliberately not assumed to be topologically ordered.
    binding_ids = set(); state_ids = set(); p_paths = {}; stage_counts = Counter()
    for rec in jsonl(path):
        pid, sid = rec["probe_path_binding_id"], rec["state_id"]
        require(pid not in binding_ids, "duplicate probe path binding", probe_path_binding_id=pid)
        require(sid not in state_ids, "more than one path binding merged into one probe state", state_id=sid, probe_path_binding_id=pid)
        require(sid in states, "binding references missing probe state", state_id=sid, probe_path_binding_id=pid)
        binding_ids.add(pid); state_ids.add(sid); stage_counts[rec["stage"]] += 1
        if rec["stage"] == "A_plus_p":
            p_paths[pid] = {
                "state_id": sid,
                "base_path_binding_id": rec["base_path_binding_id"],
                "source_child_graph_id": rec["source_child_graph_id"],
                "target_child_graph_id": rec["target_child_graph_id"],
                "transport": states[sid]["transport"],
                "classification": states[sid]["classification"],
            }
        elif rec["stage"] != "A_plus_p_plus_q":
            preserve_first_failure("unknown binding stage", probe_path_binding_id=pid, stage=rec["stage"])
    require(state_ids == set(states), "binding/state record sets differ", states_without_bindings=sorted(set(states)-state_ids)[:20], bindings_without_states=sorted(state_ids-set(states))[:20])

    p_seen = defaultdict(set); q_seen = defaultdict(set)
    p_parent_graphs = {}; q_parent_graphs = {}; q_parent_ids = set()
    normalized_bindings = []
    for rec in jsonl(path):
        pid, sid, stage = rec["probe_path_binding_id"], rec["state_id"], rec["stage"]
        state = states[sid]
        require(state["stage"] == stage, "state/binding stage mismatch", probe_path_binding_id=pid, state_id=sid)
        base_pid = rec["base_path_binding_id"]
        require(base_pid in base_paths, "binding references unknown base terminal path", probe_path_binding_id=pid, base_path_binding_id=base_pid)
        base = base_paths[base_pid]; validate_base_metadata(rec, base)

        if stage == "A_plus_p":
            require(rec["parent_probe_path_binding_id"] is None, "p binding has a probe parent", probe_path_binding_id=pid)
            expected_label = f"L_{base['selected_count']}"
            sp, sc, sa = validate_child_side(rec, "source", graphs, expected_label)
            tp, tc, ta = validate_child_side(rec, "target", graphs, expected_label)
            require(sp.rooted_code == base["source"].rooted_code and tp.rooted_code == base["target"].rooted_code, "p parent is not the fixed base relation", probe_path_binding_id=pid, base_path_binding_id=base_pid)
            parent_key = (rec["source_parent_graph_id"], rec["target_parent_graph_id"])
            if base_pid in p_parent_graphs:
                require(p_parent_graphs[base_pid] == parent_key, "one base path acquired multiple rooted parent presentations", base_path_binding_id=base_pid)
            p_parent_graphs[base_pid] = parent_key
            pair = (sa, ta)
            require(pair not in p_seen[base_pid], "duplicate p insertion arc pair", base_path_binding_id=base_pid, pair=pair)
            p_seen[base_pid].add(pair)
            validate_transport(sp, tp, rec["base_canonicalization"], rec["base_transport"], {"probe_path_binding_id": pid, "kind": "base"})
        else:
            parent_pid = rec["parent_probe_path_binding_id"]
            require(parent_pid in p_paths, "q binding references unknown p path", probe_path_binding_id=pid, parent_probe_path_binding_id=parent_pid)
            parent = p_paths[parent_pid]
            require(parent["classification"] == "labelled_isomorphism", "q extends a nonisomorphic p state", probe_path_binding_id=pid, parent_probe_path_binding_id=parent_pid, parent_classification=parent["classification"])
            require(parent["base_path_binding_id"] == base_pid, "q changes its fixed base path", probe_path_binding_id=pid, parent_probe_path_binding_id=parent_pid)
            expected_label = f"L_{graphs[parent['source_child_graph_id']].selected_count}"
            sp, sc, sa = validate_child_side(rec, "source", graphs, expected_label)
            tp, tc, ta = validate_child_side(rec, "target", graphs, expected_label)
            require(rec["source_parent_graph_id"] == parent["source_child_graph_id"] and rec["target_parent_graph_id"] == parent["target_child_graph_id"], "q parent graph IDs do not equal the bound p children", probe_path_binding_id=pid, parent_probe_path_binding_id=parent_pid)
            require(rec["parent_transport"] == parent["transport"], "q does not retain the fixed p transport", probe_path_binding_id=pid, parent_probe_path_binding_id=parent_pid)
            validate_transport(sp, tp, None if parent["transport"] is None else states[parent["state_id"]]["canonicalization"], rec["parent_transport"], {"probe_path_binding_id": pid, "kind": "p-parent"})
            parent_key = (rec["source_parent_graph_id"], rec["target_parent_graph_id"])
            if parent_pid in q_parent_graphs:
                require(q_parent_graphs[parent_pid] == parent_key, "one p path acquired multiple q parent presentations", parent_probe_path_binding_id=parent_pid)
            q_parent_graphs[parent_pid] = parent_key; q_parent_ids.add(parent_pid)
            pair = (sa, ta)
            require(pair not in q_seen[parent_pid], "duplicate q insertion arc pair", parent_probe_path_binding_id=parent_pid, pair=pair)
            q_seen[parent_pid].add(pair)

        require(state["source_graph_id"] == rec["source_child_graph_id"] and state["target_graph_id"] == rec["target_child_graph_id"], "probe state graphs differ from binding children", probe_path_binding_id=pid, state_id=sid)
        source_child = graphs[rec["source_child_graph_id"]]; target_child = graphs[rec["target_child_graph_id"]]
        labels = tuple(f"L_{i}" for i in range(source_child.selected_count))
        normalized_bindings.append({
            "probe_path_binding_id": pid,
            "base_path_binding_id": base_pid,
            "parent_probe_path_binding_id": rec["parent_probe_path_binding_id"],
            "stage": stage,
            "source_parent_rooted_sha256": graphs[rec["source_parent_graph_id"]].rooted_sha256,
            "target_parent_rooted_sha256": graphs[rec["target_parent_graph_id"]].rooted_sha256,
            "source_child_rooted_sha256": source_child.rooted_sha256,
            "target_child_rooted_sha256": target_child.rooted_sha256,
            "source_parent_exact_sha256": graphs[rec["source_parent_graph_id"]].raw_sha256,
            "target_parent_exact_sha256": graphs[rec["target_parent_graph_id"]].raw_sha256,
            "source_child_exact_sha256": source_child.raw_sha256,
            "target_child_exact_sha256": target_child.raw_sha256,
            "source_insertion_arc": list(rec["source_insertion"]["subdivided_parent_arc"]),
            "target_insertion_arc": list(rec["target_insertion"]["subdivided_parent_arc"]),
            "complete_port_matching": [[label, label] for label in labels],
            "classification": state["classification"],
        })

    require(set(p_seen) == set(base_paths), "p stage does not cover every base terminal path", missing=sorted(set(base_paths)-set(p_seen)), extra=sorted(set(p_seen)-set(base_paths)))
    for base_pid, seen in p_seen.items():
        # Any one p record supplied the fixed actual parent presentation.
        example = next(x for x in p_paths.values() if x["base_path_binding_id"] == base_pid)
        # Find parent graph IDs through one second-pass-independent lookup from
        # the already validated binding metadata.
        # The expected count can be read from the fixed parent clean IDs by
        # finding their unique graph-library representatives.
        sgid, tgid = p_parent_graphs[base_pid]
        s_info, t_info = graphs[sgid], graphs[tgid]
        expected = {(a, b) for a in s_info.cyclic_arcs for b in t_info.cyclic_arcs}
        require(seen == expected, "incomplete p Cartesian child set", base_path_binding_id=base_pid, missing=sorted(expected-seen)[:20], extra=sorted(seen-expected)[:20], expected_count=len(expected), actual_count=len(seen))

    allowed_q_parents = {pid for pid, item in p_paths.items() if item["classification"] == "labelled_isomorphism"}
    require(q_parent_ids == allowed_q_parents, "q stage parent set is not exactly the allowed isomorphic p paths", missing=sorted(allowed_q_parents-q_parent_ids)[:20], extra=sorted(q_parent_ids-allowed_q_parents)[:20])
    for parent_pid, seen in q_seen.items():
        sgid, tgid = q_parent_graphs[parent_pid]
        s_info, t_info = graphs[sgid], graphs[tgid]
        expected = {(a, b) for a in s_info.cyclic_arcs for b in t_info.cyclic_arcs}
        require(seen == expected, "incomplete q Cartesian child set", parent_probe_path_binding_id=parent_pid, missing=sorted(expected-seen)[:20], extra=sorted(seen-expected)[:20], expected_count=len(expected), actual_count=len(seen))

    return {
        "binding_count": len(binding_ids),
        "stage_counts": dict(sorted(stage_counts.items())),
        "p_parent_count": len(p_seen),
        "p_child_count": sum(map(len, p_seen.values())),
        "allowed_q_parent_count": len(allowed_q_parents),
        "q_parent_count": len(q_seen),
        "q_child_count": sum(map(len, q_seen.values())),
        "normalized_binding_commitment": digest(sorted(normalized_bindings, key=lambda x: x["probe_path_binding_id"])),
    }


def resolve_stream(summary, name):
    entry = summary["streams"][name]
    path = ROOT / entry["path"]
    require(path.exists(), "referenced probe stream missing", stream=name, path=str(path))
    actual = logical_jsonl_sha(path)
    require(actual == entry["sha256"], "probe logical-stream hash mismatch", stream=name, expected=entry["sha256"], actual=actual)
    return path, int(entry["records"])


def main():
    summary = json.loads(SUMMARY.read_text())
    require(summary["schema"] == "path-bound-common-anchor-probe-extension-v1", "unexpected probe summary schema", schema=summary.get("schema"))
    full_base = json.loads(FULL_BASE_AUDIT.read_text())
    require(full_base["status"] == "VERIFIED", "base n4 terminal audit is not verified", base_status=full_base.get("status"))
    paths = {}; declared_counts = {}
    for name in ("graphs", "states", "bindings", "polynomials"):
        paths[name], declared_counts[name] = resolve_stream(summary, name)

    base_graphs = load_graph_library(BASE_GRAPHS, require_consecutive_labels=False)
    base_paths = load_base_paths(base_graphs)
    graphs = load_graph_library(paths["graphs"], require_declared_arcs=True)
    require(len(graphs) == declared_counts["graphs"], "probe graph count mismatch", declared=declared_counts["graphs"], actual=len(graphs))
    polynomials = validate_polynomial_library(paths["polynomials"])
    require(len(polynomials) == declared_counts["polynomials"], "probe polynomial count mismatch", declared=declared_counts["polynomials"], actual=len(polynomials))
    states, state_counts, state_commitment = validate_probe_states(paths["states"], graphs, polynomials)
    require(len(states) == declared_counts["states"], "probe state count mismatch", declared=declared_counts["states"], actual=len(states))
    binding = validate_binding_stream(paths["bindings"], states, graphs, base_paths)
    require(binding["binding_count"] == declared_counts["bindings"], "probe binding count mismatch", declared=declared_counts["bindings"], actual=binding["binding_count"])

    expected_counts = {tuple(k.split("::")): int(v) for k, v in summary["counts"].items()}
    require(dict(state_counts) == expected_counts, "probe classification totals differ from summary", declared=expected_counts, independent=dict(state_counts))
    cert = {
        "schema": 1,
        "status": "VERIFIED",
        "scope": "schema-3 n4 theta-2 p/q structural stream; algebra is certified separately",
        "inputs": {str(path.relative_to(ROOT)): sha(path) for path in [SUMMARY, BASE_STATES, BASE_GRAPHS, FULL_BASE_AUDIT, *paths.values()]},
        "base_terminal_paths": len(base_paths),
        "probe_graphs": len(graphs),
        "probe_polynomials": len(polynomials),
        "probe_states": len(states),
        "classification_counts": {f"{a}::{b}": n for (a, b), n in sorted(state_counts.items())},
        "normalized_state_commitment": state_commitment,
        "binding_audit": binding,
        "assertions": {
            "standard_stc_membership_regenerated": True,
            "admissible_blob_arcs_regenerated": True,
            "all_p_child_sets_exact": True,
            "only_isomorphic_p_paths_advance_to_q": True,
            "all_q_child_sets_exact": True,
            "sequential_labels_exact": True,
            "fixed_base_and_parent_bindings_retained": True,
            "labelled_isomorphism_transports_semantically_exact": True,
            "no_isomorphism_or_T_hidden_in_separated_states": True,
            "primary_polynomial_cross_references_complete": True,
        },
    }
    cert["normalized_sha256_without_hash"] = digest(cert)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(stable_json(cert) + "\n")
    print(stable_json({"status": cert["status"], "states": len(states), "bindings": binding["binding_count"], "hash": cert["normalized_sha256_without_hash"]}))


if __name__ == "__main__":
    try:
        main()
    except AuditFailure as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
