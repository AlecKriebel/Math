#!/usr/bin/env python3
"""Fail-closed verifier for the direct-anchor extension package.

This verifier imports only the self-contained exact engine in this directory.
It reconstructs every inserted graph and fixed transport, regenerates every
displayed-tree JC pullback, and checks every strict sign certificate.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse
import copy
import gzip
import hashlib
import itertools
import json
import math

from exact_engine import (
    RootedGraph, admissible_internal_blob_arcs, classify_topology, delete_port,
    digest, invariant_pullback, pmul, poly_digest, quartet_tensor,
    root_is_lsa, standard_mixed, triangles, validate_rooted,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
CERT = HERE / "certificates"
SUMMARY = CERT / "summary.json"
RELATIONS = PROJECT / "primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_relations.jsonl.gz"
GRAPHS = PROJECT / "primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_graphs.jsonl.gz"
FAMILY = PROJECT / "reviews/final_hard_cover_cleanroom/certificates/family_n3.json.gz"
HARD_COVER = PROJECT / "primary/certificates/hard_cover_n3_schema3_n3_full.jsonl.gz"
ALLOWED = {"labelled_isomorphism", "ordinary_T"}


class Failure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


def stable(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_jsonl(path):
    with gzip.open(path, "rt") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def logical_sha(rows):
    h = hashlib.sha256()
    for row in rows:
        h.update((stable(row) + "\n").encode())
    return h.hexdigest()


def graph_sha(graph):
    return digest(graph.to_json())


def local_strong(graph):
    mixed = standard_mixed(graph)
    degree = Counter()
    for u, v, hu, hv in mixed["edges"]:
        if not hu and not hv:
            degree[u] += 1
            degree[v] += 1
    for u, v, hu, hv in mixed["edges"]:
        if hu and hv:
            return False
        if hu and degree[v] != 2:
            return False
        if hv and degree[u] != 2:
            return False
    return True


def edge_attributes(mixed):
    return {(u, v): (hu, hv) for u, v, hu, hv in mixed["edges"]}


def classify_fixed(source, target, mapping):
    sm, tm = standard_mixed(source), standard_mixed(target)
    if set(mapping) != set(sm["vertices"]) or set(mapping.values()) != set(tm["vertices"]):
        return None
    if any(sm["labels"].get(v) != tm["labels"].get(mapping[v]) for v in sm["vertices"]):
        return None
    se, te = edge_attributes(sm), edge_attributes(tm)
    if len(se) != len(te):
        return None
    bad = []
    for (u, v), attr in se.items():
        x, y = mapping[u], mapping[v]
        a, b = sorted((x, y))
        if (a, b) not in te:
            return None
        moved = attr if x <= y else (attr[1], attr[0])
        if moved != te[(a, b)]:
            bad.append(((u, v), (a, b)))
    if not bad:
        return "labelled_isomorphism"
    st, tt = triangles(sm), triangles(tm)
    if len(st) != 1 or len(tt) != 1:
        return None
    sts, tts = set(st[0]), set(tt[0])
    if {mapping[v] for v in sts} != tts:
        return None
    return "ordinary_T" if all({u, v} <= sts and {a, b} <= tts for (u, v), (a, b) in bad) else None


def transport_record(source, target, mapping, classification):
    sm, tm = standard_mixed(source), standard_mixed(target)
    target_edges = {(u, v): i for i, (u, v, _hu, _hv) in enumerate(tm["edges"])}
    st, tt = triangles(sm), triangles(tm)
    redirected = set(st[0]) if classification == "ordinary_T" else set()
    target_rets = set(target.reticulations)
    return {
        "classification": classification,
        "vertex_transport": [[u, mapping[u]] for u in sorted(mapping)],
        "edge_transport": [
            [i, target_edges[tuple(sorted((mapping[u], mapping[v])))] ]
            for i, (u, v, _hu, _hv) in enumerate(sm["edges"])
        ],
        "port_transport": [[label, label] for label in sorted(source.label_map.values())],
        "source_triangle": list(st[0]) if classification == "ordinary_T" else None,
        "target_triangle": list(tt[0]) if classification == "ordinary_T" else None,
        "reticulation_transport_outside_redirected_triangle": [
            [r, mapping[r]] for r in sorted(set(source.reticulations) - redirected)
            if mapping[r] in target_rets
        ],
    }


def extend_mapping(parent, source_parent, source_child, target_parent, target_child, label):
    _sp, sd = delete_port(source_child, label)
    _tp, td = delete_port(target_child, label)
    require(_sp == source_parent and _tp == target_parent, "child deletion does not recover its exact parent")
    out = dict(parent)
    out[int(sd["suppressed_vertex"])] = int(td["suppressed_vertex"])
    out[int(sd["deleted_leaf"])] = int(td["deleted_leaf"])
    return out


def relation_id(record):
    return digest({
        "direct_anchor_id": record["direct_anchor_id"],
        "parent_relation_id": record["parent_relation_id"],
        "stage": record["stage"],
        "new_label": record["new_label"],
        "source_arc": record["source_arc"],
        "target_arc": record["target_arc"],
        "direction": record["direction"],
    })


def family_relation_hash(relation):
    return digest([[c, list(m)] for c, m in relation])


def relation_invariant(relation):
    terms = []
    for coefficient, monomial in relation:
        powers = Counter(monomial)
        terms.append({"coefficient": coefficient,
                      "coordinate_powers": [[i, powers[i]] for i in sorted(powers)]})
    return {"terms": terms}


def parse_poly(rows):
    return {
        tuple((str(v), int(power)) for v, power in monomial): int(coefficient)
        for monomial, coefficient in rows if coefficient
    }


def bernstein_sign(poly):
    variables = sorted({v for monomial in poly for v, _power in monomial})
    if not variables:
        value = poly.get((), 0)
        return (1 if value > 0 else -1, []) if value else None
    index = {v: i for i, v in enumerate(variables)}
    degrees = [0] * len(variables)
    terms = []
    for monomial, coefficient in poly.items():
        alpha = [0] * len(variables)
        for variable, power in monomial:
            alpha[index[variable]] = power
            degrees[index[variable]] = max(degrees[index[variable]], power)
        terms.append((tuple(alpha), coefficient))
    values = []
    for beta in itertools.product(*(range(d + 1) for d in degrees)):
        total = Fraction(0)
        for alpha, coefficient in terms:
            if all(a <= b for a, b in zip(alpha, beta)):
                term = Fraction(coefficient)
                for a, b, d in zip(alpha, beta, degrees):
                    term *= Fraction(math.comb(b, a), math.comb(d, a))
                total += term
        values.append(total)
    if all(x >= 0 for x in values) and any(x > 0 for x in values):
        return 1, degrees
    if all(x <= 0 for x in values) and any(x < 0 for x in values):
        return -1, degrees
    return None


def verify_factor_certificate(poly, certificate):
    product = {(): int(certificate["content"])}
    sign = 1 if certificate["content"] > 0 else -1
    for item in certificate["factors"]:
        factor = parse_poly(item["terms"])
        require(poly_digest(factor) == item["sha256"], "factor content hash mismatch")
        actual = bernstein_sign(factor)
        require(actual is not None, "factor has no certified strict Bernstein sign")
        factor_sign, degrees = actual
        require(factor_sign == item["bernstein_sign"] and degrees == item["degrees"],
                "factor Bernstein certificate mismatch")
        for _ in range(int(item["multiplicity"])):
            product = pmul(product, factor)
        if int(item["multiplicity"]) % 2:
            sign *= factor_sign
    require(product == poly, "strict factorization does not expand to the graph-derived pullback")
    require(sign == certificate["sign"] and sign in (-1, 1), "strict product sign mismatch")


def load_package():
    summary = json.loads(SUMMARY.read_text())
    rows = {}
    for name, metadata in summary["streams"].items():
        path = PROJECT / metadata["path"]
        require(sha256_file(path) == metadata["physical_sha256"], f"{name} physical hash mismatch")
        rows[name] = read_jsonl(path)
        require(len(rows[name]) == metadata["records"], f"{name} record count mismatch")
        require(logical_sha(rows[name]) == metadata["logical_sha256"], f"{name} logical hash mismatch")
    return summary, rows


def validate_structure(summary, rows, check_inputs=True):
    if check_inputs:
        expected_inputs = {
            str(RELATIONS.relative_to(PROJECT)): sha256_file(RELATIONS),
            str(GRAPHS.relative_to(PROJECT)): sha256_file(GRAPHS),
            str(FAMILY.relative_to(PROJECT)): sha256_file(FAMILY),
            str(HARD_COVER.relative_to(PROJECT)): sha256_file(HARD_COVER),
        }
        require(summary["inputs"] == expected_inputs, "input hash lock mismatch")
    require(summary["coverage_determination"]["all_direct_anchors_represented_by_existing_terminal_families"] is False,
            "coverage result must fail closed")
    require(summary["coverage_determination"]["direct_anchor_selected_port_count"] == 4,
            "direct anchor port count changed")
    require(min(map(int, summary["coverage_determination"]["existing_terminal_anchor_port_counts"])) == 5,
            "existing path-bound terminals unexpectedly include a four-port anchor")

    graph_rows = rows["graphs"]
    graph_catalog = {}
    for row in graph_rows:
        graph = RootedGraph.from_json(row["rooted_graph"])
        require(graph_sha(graph) == row["graph_sha256"], "graph content address mismatch")
        require(row["graph_sha256"] not in graph_catalog, "duplicate graph record")
        require(not validate_rooted(graph, require_tree_child=True), "extension graph is not rooted tree-child")
        require(root_is_lsa(graph), "extension graph is not LSA-valid")
        require(local_strong(graph), "extension graph violates the locked standard-strong criterion")
        require(len(graph.reticulations) <= 2, "extension graph exceeds level two")
        graph_catalog[row["graph_sha256"]] = graph

    input_relations = {r["relation_id"]: r for r in read_jsonl(RELATIONS)
                       if r.get("classification") == "isomorphism_or_T"}
    require(len(input_relations) == 62, "frozen input does not contain exactly 62 direct anchors")
    input_graphs = {}
    needed = {r["source_graph_id"] for r in input_relations.values()} | {
        r["target_selected_graph_id"] for r in input_relations.values()
    }
    for row in read_jsonl(GRAPHS):
        if row["graph_id"] in needed:
            input_graphs[row["graph_id"]] = RootedGraph.from_json(row["rooted_graph"])
    require(set(input_graphs) == needed, "selected anchor graph missing from primary data input")

    anchors = rows["anchors"]
    require(len(anchors) == 62 and len({r["direct_anchor_id"] for r in anchors}) == 62,
            "anchor stream is not a 62-element set")
    anchor_context = {}
    for anchor in anchors:
        aid = anchor["direct_anchor_id"]
        require(aid in input_relations, "unknown or altered direct anchor id")
        original = input_relations[aid]
        require(anchor["direction"] == original["direction"] == "source_precedes_target",
                "directed source-target orientation changed")
        require(anchor["port_correspondence"] == original["port_correspondence"],
                "port correspondence changed")
        require(anchor["binding_sha256"] == original["binding_sha256"], "direct binding changed")
        require(anchor["raw_coverage_sha256"] == digest(original["raw_coverage"]), "raw coverage changed")
        source = input_graphs[original["source_graph_id"]]
        target = input_graphs[original["target_selected_graph_id"]]
        require(graph_sha(source) == anchor["source_graph_sha256"] and
                graph_sha(target) == anchor["target_graph_sha256"], "anchor graph binding changed")
        candidates = classify_topology(source, target)
        require(len(candidates) == 1, "anchor transport is not unique")
        classification, mapping = candidates[0]
        require(classification == anchor["classification"], "anchor classification changed")
        require(anchor["transport"] == transport_record(source, target, mapping, classification),
                "anchor canonical transport changed")
        probe = dict(anchor)
        claimed = probe.pop("anchor_certificate_id")
        require(digest(probe) == claimed, "anchor certificate id mismatch")
        anchor_context[aid] = (source, target, mapping)

    p_by_id = {r["relation_id"]: r for r in rows["p_relations"]}
    q_by_id = {r["relation_id"]: r for r in rows["q_relations"]}
    require(len(p_by_id) == len(rows["p_relations"]), "duplicate p relation id")
    require(len(q_by_id) == len(rows["q_relations"]), "duplicate q relation id")
    expected_p, expected_q = set(), set()
    p_context = {}

    def audit_record(record, source_parent, target_parent, parent_mapping, stage, label):
        require(record["stage"] == stage and record["new_label"] == label,
                "p/q order or stage label changed")
        require(record["direction"] == "source_precedes_target", "extension direction reversed")
        require(relation_id(record) == record["relation_id"], "relation content address mismatch")
        require(tuple(record["source_arc"]) in admissible_internal_blob_arcs(source_parent),
                "source insertion arc is not admissible")
        require(tuple(record["target_arc"]) in admissible_internal_blob_arcs(target_parent),
                "target insertion arc is not admissible")
        source_child = graph_catalog[record["source_graph_sha256"]]
        target_child = graph_catalog[record["target_graph_sha256"]]
        mapping = extend_mapping(parent_mapping, source_parent, source_child, target_parent, target_child, label)
        classification = classify_fixed(source_child, target_child, mapping)
        expected_class = classification if classification in ALLOWED else None
        if expected_class:
            require(record["classification"] == expected_class, "isomorphism/T choice changed")
            require(record["transport"] == transport_record(source_child, target_child, mapping, expected_class),
                    "extension canonical transport changed")
            require(record["witness_id"] is None, "topological survivor carries a separator")
        else:
            require(record["classification"] in {"generic_polynomial_separation", "strict_open_cube_separation"},
                    "separated relation was promoted to overlap")
            require(record["transport"] is None and record["witness_id"] is not None,
                    "separated relation transport/witness mismatch")
        return source_child, target_child, mapping

    for aid, (source, target, mapping) in anchor_context.items():
        for source_arc in admissible_internal_blob_arcs(source):
            for target_arc in admissible_internal_blob_arcs(target):
                rid = digest({"direct_anchor_id": aid, "parent_relation_id": aid,
                              "stage": "A_plus_p", "new_label": "L_4",
                              "source_arc": list(source_arc), "target_arc": list(target_arc),
                              "direction": "source_precedes_target"})
                expected_p.add(rid)
                require(rid in p_by_id, "required A+p relation deleted")
                record = p_by_id[rid]
                require(record["direct_anchor_id"] == aid and record["parent_relation_id"] == aid,
                        "A+p parent binding changed")
                p_context[rid] = audit_record(record, source, target, mapping, "A_plus_p", "L_4")
    require(set(p_by_id) == expected_p, "p relation stream has an extra or missing relation")

    for pid, (source_p, target_p, mapping_p) in p_context.items():
        parent = p_by_id[pid]
        if parent["classification"] not in ALLOWED:
            continue
        aid = parent["direct_anchor_id"]
        for source_arc in admissible_internal_blob_arcs(source_p):
            for target_arc in admissible_internal_blob_arcs(target_p):
                rid = digest({"direct_anchor_id": aid, "parent_relation_id": pid,
                              "stage": "A_plus_p_plus_q", "new_label": "L_5",
                              "source_arc": list(source_arc), "target_arc": list(target_arc),
                              "direction": "source_precedes_target"})
                expected_q.add(rid)
                require(rid in q_by_id, "required A+p+q relation deleted")
                record = q_by_id[rid]
                require(record["direct_anchor_id"] == aid and record["parent_relation_id"] == pid,
                        "A+p+q parent binding or p/q order changed")
                audit_record(record, source_p, target_p, mapping_p, "A_plus_p_plus_q", "L_5")
    require(set(q_by_id) == expected_q, "q relation stream has an extra or missing relation")

    counts = summary["counts"]
    require(counts["anchors"] == len(anchors) and counts["A_plus_p"] == len(p_by_id) and
            counts["A_plus_p_plus_q"] == len(q_by_id), "summary relation counts changed")
    require(counts["anchor_classifications"] == dict(sorted(Counter(r["classification"] for r in anchors).items())),
            "anchor classification count mismatch")
    require(counts["A_plus_p_classifications"] == dict(sorted(Counter(r["classification"] for r in p_by_id.values()).items())),
            "p classification count mismatch")
    require(counts["A_plus_p_plus_q_classifications"] == dict(sorted(Counter(r["classification"] for r in q_by_id.values()).items())),
            "q classification count mismatch")
    return graph_catalog, p_by_id, q_by_id


def verify_algebra(summary, rows, graph_catalog, p_by_id, q_by_id):
    with gzip.open(FAMILY, "rt") as stream:
        family_obj = json.load(stream)
    family = tuple(tuple((int(c), tuple(int(i) for i in monomial)) for c, monomial in relation)
                   for relation in family_obj["relations"])
    require(len(family) == summary["family"]["relations"] and
            family_obj["normalized_sha256_without_hash"] == summary["family"]["normalized_sha256_without_hash"],
            "invariant-family commitment changed")
    witnesses = {r["witness_id"]: r for r in rows["witnesses"]}
    require(len(witnesses) == len(rows["witnesses"]), "duplicate witness id")
    used = Counter()
    tensor_cache = {}

    def tensor(graph, quartet):
        key = (graph_sha(graph), tuple(quartet))
        if key not in tensor_cache:
            tensor_cache[key] = quartet_tensor(graph, tuple(quartet))
        return tensor_cache[key]

    for record in itertools.chain(p_by_id.values(), q_by_id.values()):
        wid = record["witness_id"]
        if wid is None:
            continue
        require(wid in witnesses, "relation references a missing witness")
        witness = witnesses[wid]
        require(witness["source_graph_sha256"] == record["source_graph_sha256"] and
                witness["target_graph_sha256"] == record["target_graph_sha256"],
                "valid separator assigned to the wrong graph relation")
        index = int(witness["family_relation_index"])
        require(0 <= index < len(family), "witness family index out of range")
        relation = family[index]
        require(family_relation_hash(relation) == witness["family_relation_sha256"],
                "witness invariant body changed")
        source = graph_catalog[record["source_graph_sha256"]]
        target = graph_catalog[record["target_graph_sha256"]]
        quartet = tuple(witness["quartet"])
        require(len(quartet) == 4 and set(quartet) <= set(source.label_map.values()) and
                set(quartet) <= set(target.label_map.values()), "witness quartet is not present")
        invariant = relation_invariant(relation)
        spoly = invariant_pullback(tensor(source, quartet), invariant)
        tpoly = invariant_pullback(tensor(target, quartet), invariant)
        require(poly_digest(spoly) == witness["source_pullback_sha256"] and
                len(spoly) == witness["source_pullback_term_count"], "source pullback mismatch")
        require(poly_digest(tpoly) == witness["target_pullback_sha256"] and
                len(tpoly) == witness["target_pullback_term_count"], "target pullback mismatch")
        if witness["orientation"] == "source_nonzero_target_zero":
            require(bool(spoly) and not tpoly, "generic separator has wrong source-relative direction")
            require(record["classification"] == "generic_polynomial_separation", "generic separator class mismatch")
            require(witness["target_strict_sign_certificate"] is None, "generic separator has an irrelevant sign certificate")
        elif witness["orientation"] == "source_zero_target_strict":
            require(not spoly and bool(tpoly), "strict separator has wrong zero direction")
            require(record["classification"] == "strict_open_cube_separation", "strict separator class mismatch")
            verify_factor_certificate(tpoly, witness["target_strict_sign_certificate"])
        else:
            raise Failure("unknown witness orientation")
        probe = dict(witness)
        claimed = probe.pop("witness_id")
        require(digest(probe) == claimed, "witness content address mismatch")
        used[wid] += 1
    require(set(used) == set(witnesses), "unused or missing witness record")
    require(len(witnesses) == summary["counts"]["unique_separator_witnesses"], "witness count mismatch")


def verify_package(check_algebra=True):
    summary, rows = load_package()
    graph_catalog, p_by_id, q_by_id = validate_structure(summary, rows)
    if check_algebra:
        verify_algebra(summary, rows, graph_catalog, p_by_id, q_by_id)
    return summary, rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--structure-only", action="store_true")
    args = parser.parse_args()
    summary, _rows = verify_package(check_algebra=not args.structure_only)
    print(stable({"status": "VERIFIED", "scope": summary["scope"], **summary["counts"]}))


if __name__ == "__main__":
    try:
        main()
    except Failure as exc:
        print(stable({"status": "FALSE", "reason": str(exc)}))
        raise SystemExit(1)
