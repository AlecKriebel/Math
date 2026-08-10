#!/usr/bin/env python3
"""Independent producer for final raw hard-cover terminal seeds.

The input is self-contained and contains one record per *raw path-bound*
terminal.  This producer does not canonicalize or merge those records.  It
regenerates all p/q children, graph tensors, witnesses, transports, child
sets, and modular rank certificates.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cleanroom_probe import (
    RootedGraph, admissible_internal_blob_arcs, classify_topology, delete_port,
    digest, expected_base_relation_id, expected_relation_id,
    find_linear_separator, insert_port, invariant_pullback,
    jacobian_rank_certificate, poly_digest, quartet_tensor, standard_mixed,
    standard_strong, validate_rooted,
)


ALLOWED = {"labelled_isomorphism", "ordinary_T"}


def graph_id(g):
    return digest(g.to_json())


def transport_pairs(mapping):
    return [[u, mapping[u]] for u in sorted(mapping)]


def base_provenance(parent):
    return {
        k: parent[k]
        for k in (
            "raw_terminal_id", "fixed_full_root_case_id", "restoration_root_id",
            "parent_path_id", "Q_s", "Q_t", "port_matching",
            "base_relation_id", "base_source_rooted_graph_id",
            "base_target_rooted_graph_id",
        )
    }


def catalog_separator(source, target, catalog):
    common = sorted(set(source.label_map.values()) & set(target.label_map.values()))
    import itertools
    for quartet in itertools.combinations(common, 4):
        st, tt = quartet_tensor(source, quartet), quartet_tensor(target, quartet)
        for invariant in catalog:
            ps = invariant_pullback(st, invariant)
            pt = invariant_pullback(tt, invariant)
            if ps and not pt:
                return quartet, invariant, ps, pt
    return find_linear_separator(source, target, common)


def make_child(parent, source_arc, target_arc, label, catalog):
    sg, tg = RootedGraph.from_json(parent["source_graph"]), RootedGraph.from_json(parent["target_graph"])
    sc, si = insert_port(sg, source_arc, label)
    tc, ti = insert_port(tg, target_arc, label)
    if validate_rooted(sc) or validate_rooted(tc) or not standard_strong(sc)[0] or not standard_strong(tc)[0]:
        raise RuntimeError(f"child left locked class: {parent['relation_id']} {source_arc} {target_arc}")
    record = {
        **base_provenance(parent),
        "parent_relation_id": parent["relation_id"],
        "level": label,
        "new_label": label,
        "source_arc": list(source_arc),
        "target_arc": list(target_arc),
        "source_graph": sc.to_json(),
        "target_graph": tc.to_json(),
        "source_graph_id": graph_id(sc),
        "target_graph_id": graph_id(tc),
        "source_inclusion": si,
        "target_inclusion": ti,
        "parent_transport": parent["transport"],
    }
    candidates = classify_topology(sc, tc, parent["transport"])
    if candidates:
        record["classification"], mapping = candidates[0]
        record["transport"] = transport_pairs(mapping)
        record["witness"] = None
    else:
        sep = catalog_separator(sc, tc, catalog)
        if sep is None:
            return None, {
                "parent_relation_id": parent["relation_id"],
                "level": label,
                "source_arc": list(source_arc),
                "target_arc": list(target_arc),
                "source_graph": sc.to_json(),
                "target_graph": tc.to_json(),
                "failure": "no regenerated source-nonzero/target-zero quartet separator",
            }
        quartet, invariant, ps, pt = sep
        if not ps or pt:
            return None, {"failure": "separator has wrong source-relative orientation"}
        st, tt = quartet_tensor(sc, quartet), quartet_tensor(tc, quartet)
        record["classification"] = "generic_polynomial_separation"
        record["transport"] = None
        record["witness"] = {
            "quartet": list(quartet),
            "invariant": invariant,
            "orientation": "source_nonzero_target_zero",
            "source_pullback_sha256": poly_digest(ps),
            "target_pullback_sha256": poly_digest(pt),
            "source_quartet_tensor_sha256": digest([poly_digest(p) for p in st]),
            "target_quartet_tensor_sha256": digest([poly_digest(p) for p in tt]),
        }
    record["relation_id"] = expected_relation_id(record)
    ds, sd = delete_port(sc, label)
    dt, td = delete_port(tc, label)
    if ds != sg or dt != tg:
        raise RuntimeError("internal producer deletion regression")
    record["source_deletion"], record["target_deletion"] = sd, td
    return record, None


def normalize_base(seed):
    b = dict(seed)
    sg, tg = RootedGraph.from_json(b["source_graph"]), RootedGraph.from_json(b["target_graph"])
    b["source_graph_id"], b["target_graph_id"] = graph_id(sg), graph_id(tg)
    b["base_source_rooted_graph_id"], b["base_target_rooted_graph_id"] = b["source_graph_id"], b["target_graph_id"]
    b["relation_id"] = expected_base_relation_id(b)
    b["state_identity_sha256"] = b["relation_id"]
    if b.get("classification") not in ALLOWED:
        raise RuntimeError("seed is not an allowed hard-cover terminal")
    candidates = classify_topology(sg, tg)
    if "transport" not in b:
        candidates = [x for x in candidates if x[0] == b["classification"]]
        if not candidates:
            raise RuntimeError("seed classification has no independently regenerated map")
        b["transport"] = transport_pairs(candidates[0][1])
    if validate_rooted(sg) or validate_rooted(tg) or not standard_strong(sg)[0] or not standard_strong(tg)[0]:
        raise RuntimeError("seed fails locked class membership")
    b["base_relation_id"] = b["relation_id"]
    return b


def upper_bound_for_graph(g, base, depth):
    rule = base["extension_rank_rule"]
    if rule == "level1_cycle_2n_minus_1":
        if len(g.reticulations) != 1:
            raise RuntimeError("level-one rank rule attached to non-level-one graph")
        return 2 * len(g.label_map) - 1, rule
    if rule == "base_plus_two_per_port":
        return int(base["generic_rank_exact"]) + 2 * depth, rule
    raise RuntimeError(f"unsupported rank extension rule {rule}")


def produce(seeds):
    if seeds.get("schema") != "stc-jc-probe-extension-seeds-v1":
        raise RuntimeError("wrong seed schema")
    catalog = seeds.get("invariant_catalog", [])
    bases, p_records, q_records, gaps = [], [], [], []
    for seed in seeds["base_relations"]:
        base = normalize_base(seed)
        bases.append(base)
        for sa in admissible_internal_blob_arcs(RootedGraph.from_json(base["source_graph"])):
            for ta in admissible_internal_blob_arcs(RootedGraph.from_json(base["target_graph"])):
                rec, gap = make_child(base, sa, ta, "p", catalog)
                if gap:
                    gaps.append(gap)
                else:
                    p_records.append(rec)
    if gaps:
        return None, gaps
    by_base = {}
    for r in p_records:
        by_base.setdefault(r["base_relation_id"], []).append(r)
    for b in bases:
        b["p_child_relation_ids"] = sorted(r["relation_id"] for r in by_base.get(b["relation_id"], []))
    for p in p_records:
        p["q_child_relation_ids"] = []
        if p["classification"] not in ALLOWED:
            continue
        for sa in admissible_internal_blob_arcs(RootedGraph.from_json(p["source_graph"])):
            for ta in admissible_internal_blob_arcs(RootedGraph.from_json(p["target_graph"])):
                rec, gap = make_child(p, sa, ta, "q", catalog)
                if gap:
                    gaps.append(gap)
                else:
                    q_records.append(rec)
    if gaps:
        return None, gaps
    q_by_parent = {}
    for r in q_records:
        q_by_parent.setdefault(r["parent_relation_id"], []).append(r)
    for p in p_records:
        p["q_child_relation_ids"] = sorted(r["relation_id"] for r in q_by_parent.get(p["relation_id"], []))
    base_index = {b["relation_id"]: b for b in bases}
    unique, depth = {}, {}
    for r in p_records + q_records:
        for side in ("source", "target"):
            g = RootedGraph.from_json(r[f"{side}_graph"])
            gid = graph_id(g)
            unique[gid] = g
            depth[gid] = 1 if r["level"] == "p" else 2
    rank_records = {}
    for gid, g in sorted(unique.items()):
        # Every occurrence has one base id; equal rooted graphs must induce the
        # same exact upper bound or the run is ambiguous and rejected.
        occurrences = [r for r in p_records + q_records if gid in (r["source_graph_id"], r["target_graph_id"])]
        uppers = {upper_bound_for_graph(g, base_index[r["base_relation_id"]], depth[gid]) for r in occurrences}
        if len(uppers) != 1:
            raise RuntimeError(f"inconsistent rank upper certificate for {gid}")
        upper, rule = next(iter(uppers))
        cert = jacobian_rank_certificate(g, structural_upper_bound=upper)
        cert["upper_certificate"] = rule
        rank_records[gid] = cert
    return {
        "schema": "stc-jc-probe-extension-review-v1",
        "fixture_only": False,
        "base_relations": bases,
        "p_relations": p_records,
        "q_relations": q_records,
        "rank_records": rank_records,
    }, []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seeds", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--gaps", type=Path)
    args = ap.parse_args()
    payload, gaps = produce(json.loads(args.seeds.read_text()))
    if gaps:
        gap_path = args.gaps or args.output.with_suffix(".gaps.json")
        gap_path.write_text(json.dumps(gaps, sort_keys=True, indent=2) + "\n")
        raise SystemExit(f"UNRESOLVED probe relations; exact gaps written to {gap_path}")
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "sha256": digest(payload)}, sort_keys=True))


if __name__ == "__main__":
    main()
