"""Independent path-bound support-plus-one/two extension enumerator."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

from graph_model import (
    RootedGraph, biconnected_components, decorated_mixed_relation, digest,
    rooted_code, stable_json, standard_semidirected_audit,
    validate_standard_strong,
)


def cyclic_blob_arcs(g: RootedGraph):
    undirected = [tuple(sorted(e)) for e in g.arcs]
    cyclic_components = []
    for comp in biconnected_components(g.vertices, undirected):
        vertices = {x for e in comp for x in e}
        if len(comp) >= len(vertices):
            cyclic_components.append({tuple(sorted(e)) for e in comp})
    if len(cyclic_components) != 1:
        raise ValueError(("expected exactly one active blob", len(cyclic_components)))
    cyclic_edges = cyclic_components[0]
    arcs = [e for e in g.arcs if tuple(sorted(e)) in cyclic_edges]
    if not arcs: raise ValueError("no active blob")
    return tuple(sorted(arcs))


def insert_on_arc(g: RootedGraph, arc: Tuple[int, int], label: str):
    if arc not in g.arcs: raise ValueError("arc absent")
    if label in g.label_map.values(): raise ValueError(("duplicate inserted label", label))
    nxt = max(g.vertices) + 1; tree, leaf = nxt, nxt + 1
    arcs = set(g.arcs); arcs.remove(arc)
    arcs.update(((arc[0], tree), (tree, arc[1]), (tree, leaf)))
    labels = g.label_map; labels[leaf] = label
    out = RootedGraph.make(arcs, g.root, labels)
    check = validate_standard_strong(out)
    if not check["ok"]: raise AssertionError((arc, check))
    sd_check = standard_semidirected_audit(out)
    if not sd_check["ok"]: raise AssertionError((arc, "standard S_TC", sd_check))
    return out


def all_segment_insertions(g: RootedGraph, label: str):
    """All distinct ordinary-port positions in the active directed blob."""
    merged = {}
    for arc in cyclic_blob_arcs(g):
        h = insert_on_arc(g, arc, label); code, _ = rooted_code(h)
        merged.setdefault(code, {"graph": h, "arcs": []})["arcs"].append(arc)
    return tuple(merged[k] for k in sorted(merged))


def extend_relation(base_relation_id: str, source: RootedGraph, target: RootedGraph,
                    source_label: str, target_label: str, parent_path_id: str,
                    qt_transport, port_matching: Sequence[Tuple[str, str]],
                    max_total_ports: int = 12):
    """Enumerate one path-bound support extension on both relation sides.

    Raw arc pairs are retained even when they canonicalize to one child state.
    State deduplication is therefore algebraic only; it cannot reuse the first
    provenance's children or silently change the fixed full relation.
    """
    source_labels = set(source.label_map.values()); target_labels = set(target.label_map.values())
    matched_source = [x for x, _ in port_matching]; matched_target = [y for _, y in port_matching]
    if len(matched_source) != len(set(matched_source)) or set(matched_source) != source_labels:
        raise ValueError("base terminal does not completely and bijectively match source ports")
    if len(matched_target) != len(set(matched_target)) or set(matched_target) != target_labels:
        raise ValueError("base terminal does not completely and bijectively match target ports")
    if len(port_matching) + 1 > max_total_ports:
        raise ValueError(("safe port bound exceeded", len(port_matching) + 1, max_total_ports))
    source_insertions = all_segment_insertions(source, source_label)
    target_insertions = all_segment_insertions(target, target_label)
    matching = tuple(port_matching) + ((source_label, target_label),)
    merged = {}
    for s in source_insertions:
        for t in target_insertions:
            relation = decorated_mixed_relation(s["graph"], t["graph"], matching)
            state_payload = {
                "decorated_relation_code": relation["code"],
                "direction": relation["direction"],
                "port_matching": relation["port_matching"],
            }
            state_id = digest(state_payload)
            path_payload = {
                "full_relation_id": base_relation_id,
                "parent_path_binding_id": parent_path_id,
                "state_id": state_id,
                "source_added_label": source_label,
                "target_added_label": target_label,
                "qt_transport": qt_transport,
            }
            path_id = digest(path_payload)
            raw_pairs = tuple(sorted((sa, ta) for sa in s["arcs"] for ta in t["arcs"]))
            if state_id not in merged:
                merged[state_id] = {
                    "schema": 2,
                    "state_id": state_id,
                    "path_binding_id": path_id,
                    **path_payload,
                    "decorated_relation_sha256": relation["sha256"],
                    "decorated_relation_code": relation["code"],
                    "port_matching": [list(x) for x in relation["port_matching"]],
                    "source_vertex_transport": [list(x) for x in relation["source_vertex_transport"]],
                    "target_vertex_transport": [list(x) for x in relation["target_vertex_transport"]],
                    "source_graph": s["graph"],
                    "target_graph": t["graph"],
                    "raw_insertion_arc_pairs": list(raw_pairs),
                }
            else:
                rec = merged[state_id]
                if rec["path_binding_id"] != path_id:
                    raise AssertionError("one state acquired inconsistent fixed-relation path bindings")
                rec["raw_insertion_arc_pairs"] = sorted(set(tuple(map(tuple, x)) for x in rec["raw_insertion_arc_pairs"]) | set(raw_pairs))
    records = []
    for state_id in sorted(merged):
        rec = merged[state_id]
        rec["raw_insertion_arc_pairs"] = [
            [list(a), list(b)] for a, b in sorted(tuple(map(tuple, x)) for x in rec["raw_insertion_arc_pairs"])
        ]
        rec["record_sha256"] = digest({k: v for k, v in rec.items() if k not in ("source_graph", "target_graph", "record_sha256")})
        records.append(rec)
    return tuple(records)


def extend_p_then_q(base_relation_id: str, source: RootedGraph, target: RootedGraph,
                    parent_path_id: str, qt_transport,
                    port_matching: Sequence[Tuple[str, str]],
                    allowed_p_path_ids: Iterable[str],
                    p_labels=("L_p", "L_p"), q_labels=("L_q", "L_q"),
                    max_total_ports: int = 12):
    """Extend through ``p`` and then only through *allowed* ``p`` paths."""
    p = extend_relation(
        base_relation_id, source, target, p_labels[0], p_labels[1],
        parent_path_id, qt_transport, port_matching, max_total_ports,
    )
    allowed = set(allowed_p_path_ids)
    unknown = allowed - {x["path_binding_id"] for x in p}
    if unknown: raise ValueError(("unknown allowed p path", sorted(unknown)))
    q = []
    for rec in p:
        if rec["path_binding_id"] not in allowed: continue
        q.extend(extend_relation(
            base_relation_id, rec["source_graph"], rec["target_graph"],
            q_labels[0], q_labels[1], rec["path_binding_id"], qt_transport,
            tuple(port_matching) + (tuple(p_labels),), max_total_ports,
        ))
    # A q state may be reached through more than one allowed p path.  Preserve
    # every path record; do not collapse this list by state ID.
    return p, tuple(sorted(q, key=lambda x: (x["state_id"], x["path_binding_id"])))
