#!/usr/bin/env python3
"""Build a complete exact p/q fixture without using either research engine."""

from pathlib import Path
import json

from cleanroom_probe import (
    RootedGraph, admissible_internal_blob_arcs, classify_topology, delete_port,
    digest, expected_base_relation_id, expected_relation_id, find_linear_separator, insert_port,
    invariant_pullback, jacobian_rank_certificate, poly_digest, quartet_tensor,
    standard_mixed, standard_strong, validate_rooted,
)


HERE = Path(__file__).resolve().parent
OUT = HERE / "certificates" / "fixture.json"
SEEDS_OUT = HERE / "certificates" / "fixture_seeds.json"


def triangle_graph():
    # Root 0 has the incoming port i and the local triangle source 2.
    # Vertex 4 is the reticulation with parents 2 and 3.
    return RootedGraph.from_json({
        "root": 0,
        "arcs": [[0, 1], [0, 2], [2, 3], [2, 4], [3, 4], [3, 5], [4, 6]],
        "labels": {"1": "i", "5": "b", "6": "c"},
    })


def graph_id(g):
    return digest(g.to_json())


def transport_pairs(mapping):
    return [[u, mapping[u]] for u in sorted(mapping)]


def common_provenance(parent):
    return {
        "raw_terminal_id": "synthetic-raw-terminal-0001",
        "fixed_full_root_case_id": parent["fixed_full_root_case_id"],
        "restoration_root_id": "synthetic-restoration-root-0001",
        "parent_path_id": "synthetic-fixed-full-path-0001",
        "Q_s": ["i", "b", "c"],
        "Q_t": ["i", "b", "c"],
        "port_matching": [["i", "i"], ["b", "b"], ["c", "c"]],
        "base_relation_id": parent.get("base_relation_id", parent["relation_id"]),
        "base_source_rooted_graph_id": parent["base_source_rooted_graph_id"],
        "base_target_rooted_graph_id": parent["base_target_rooted_graph_id"],
    }


def make_child(parent, source_arc, target_arc, label, level):
    sg = RootedGraph.from_json(parent["source_graph"])
    tg = RootedGraph.from_json(parent["target_graph"])
    sc, si = insert_port(sg, tuple(source_arc), label)
    tc, ti = insert_port(tg, tuple(target_arc), label)
    if validate_rooted(sc) or validate_rooted(tc):
        raise AssertionError("fixture insertion left the rooted tree-child class")
    if not standard_strong(sc)[0] or not standard_strong(tc)[0]:
        raise AssertionError("fixture insertion left the locked standard-strong class")
    parent_transport = parent["transport"]
    candidates = classify_topology(sc, tc, parent_transport)
    record = {
        **common_provenance(parent),
        "parent_relation_id": parent["relation_id"],
        "level": level,
        "new_label": label,
        "source_arc": list(source_arc),
        "target_arc": list(target_arc),
        "source_graph": sc.to_json(),
        "target_graph": tc.to_json(),
        "source_graph_id": graph_id(sc),
        "target_graph_id": graph_id(tc),
        "source_inclusion": si,
        "target_inclusion": ti,
        "parent_transport": parent_transport,
    }
    if candidates:
        classification, mapping = candidates[0]
        record["classification"] = classification
        record["transport"] = transport_pairs(mapping)
        record["witness"] = None
    else:
        sep = find_linear_separator(sc, tc, label)
        if sep is None:
            raise AssertionError(f"no graph-derived linear separator for {level} {source_arc}->{target_arc}")
        quartet, invariant, ps, pt = sep
        if not ps or pt:
            raise AssertionError("fixture needs source-nonzero/target-zero direction")
        st, tt = quartet_tensor(sc, quartet), quartet_tensor(tc, quartet)
        record["classification"] = "generic_polynomial_separation"
        record["transport"] = None
        record["witness"] = {
            "quartet": list(quartet),
            "invariant": invariant,
            "orientation": "source_nonzero_target_zero",
            "source_pullback_sha256": poly_digest(invariant_pullback(st, invariant)),
            "target_pullback_sha256": poly_digest(invariant_pullback(tt, invariant)),
            "source_quartet_tensor_sha256": digest([poly_digest(p) for p in st]),
            "target_quartet_tensor_sha256": digest([poly_digest(p) for p in tt]),
        }
    record["relation_id"] = expected_relation_id(record)
    # Store deletion claims only after the complete child is fixed.
    sp, sd = delete_port(sc, label)
    tp, td = delete_port(tc, label)
    assert sp == sg and tp == tg
    record["source_deletion"] = sd
    record["target_deletion"] = td
    return record


def main():
    base_graph = triangle_graph()
    assert not validate_rooted(base_graph)
    strong, rooting_count = standard_strong(base_graph)
    if not strong:
        raise AssertionError("synthetic base is not standard strong")
    base_map = {v: v for v in standard_mixed(base_graph)["vertices"]}
    base_rank = jacobian_rank_certificate(base_graph)["rank"]
    base = {
        "relation_id": None,
        "raw_terminal_id": "synthetic-raw-terminal-0001",
        "fixed_full_root_case_id": "synthetic-fixed-full-root-case-0001",
        "restoration_root_id": "synthetic-restoration-root-0001",
        "parent_path_id": "synthetic-fixed-full-path-0001",
        "Q_s": ["i", "b", "c"],
        "Q_t": ["i", "b", "c"],
        "port_matching": [["i", "i"], ["b", "b"], ["c", "c"]],
        "source_graph": base_graph.to_json(),
        "target_graph": base_graph.to_json(),
        "source_graph_id": graph_id(base_graph),
        "target_graph_id": graph_id(base_graph),
        "classification": "labelled_isomorphism",
        "transport": transport_pairs(base_map),
        "standard_strong_rooting_count_source": rooting_count,
        "standard_strong_rooting_count_target": rooting_count,
        "generic_rank_exact": base_rank,
        "generic_rank_upper_certificate": "frozen_base_terminal_rank",
        "extension_rank_rule": "level1_cycle_2n_minus_1",
    }
    base["base_source_rooted_graph_id"] = base["source_graph_id"]
    base["base_target_rooted_graph_id"] = base["target_graph_id"]
    base["relation_id"] = expected_base_relation_id(base)
    base["state_identity_sha256"] = base["relation_id"]
    seed_payload = {
        "schema": "stc-jc-probe-extension-seeds-v1",
        "invariant_catalog": [],
        "base_relations": [{k: v for k, v in base.items() if k not in ("p_child_relation_ids",)}],
    }
    p_records = []
    arcs = admissible_internal_blob_arcs(base_graph)
    for sa in arcs:
        for ta in arcs:
            p_records.append(make_child(base, sa, ta, "p", "p"))
    base["p_child_relation_ids"] = sorted(r["relation_id"] for r in p_records)
    for r in p_records:
        r["q_child_relation_ids"] = []
    q_records = []
    for parent in p_records:
        if parent["classification"] not in ("labelled_isomorphism", "ordinary_T"):
            continue
        sg = RootedGraph.from_json(parent["source_graph"])
        tg = RootedGraph.from_json(parent["target_graph"])
        for sa in admissible_internal_blob_arcs(sg):
            for ta in admissible_internal_blob_arcs(tg):
                q_records.append(make_child(parent, sa, ta, "q", "q"))
    q_by_parent = {}
    for r in q_records:
        q_by_parent.setdefault(r["parent_relation_id"], []).append(r["relation_id"])
    for r in p_records:
        r["q_child_relation_ids"] = sorted(q_by_parent.get(r["relation_id"], []))
    unique_graphs = {}
    graph_depth = {}
    for rec in p_records + q_records:
        for side in ("source", "target"):
            g = RootedGraph.from_json(rec[f"{side}_graph"])
            unique_graphs[graph_id(g)] = g
            graph_depth[graph_id(g)] = 1 if rec["level"] == "p" else 2
    rank_records = {}
    for gid, g in sorted(unique_graphs.items()):
        # Exact level-one cycle dimension after the four-port threshold:
        # 2|X|-1.  This is also independently met by the modular minor.
        upper = 2 * len(g.label_map) - 1
        cert = jacobian_rank_certificate(g, structural_upper_bound=upper)
        cert["upper_certificate"] = "level1_cycle_2n_minus_1"
        rank_records[gid] = cert
    payload = {
        "schema": "stc-jc-probe-extension-review-v1",
        "fixture_only": True,
        "base_relations": [base],
        "p_relations": p_records,
        "q_relations": q_records,
        "rank_records": rank_records,
        "expected_counts": {
            "base": 1,
            "p": len(arcs) ** 2,
            "p_allowed": sum(r["classification"] in ("labelled_isomorphism", "ordinary_T") for r in p_records),
            "q": len(q_records),
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    SEEDS_OUT.write_text(json.dumps(seed_payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "output": str(OUT),
        "sha256": digest(payload),
        "counts": payload["expected_counts"],
        "rank_graphs": len(rank_records),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
