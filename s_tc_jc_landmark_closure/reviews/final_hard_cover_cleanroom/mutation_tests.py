#!/usr/bin/env python3
"""Mutation-sensitive integrity tests for normalized decorated relations."""

from copy import deepcopy
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def stable(x): return json.dumps(x, sort_keys=True, separators=(",", ":"))
def digest(x): return hashlib.sha256(stable(x).encode()).hexdigest()


def relation_payload(source, target, port_matching, direction="source_to_target"):
    return {"source": source, "target": target, "port_matching": port_matching, "direction": direction}


def make_record(source, target, port_matching, polynomial, paths, children):
    payload = relation_payload(source, target, port_matching)
    return {
        "relation_id": digest(payload), **payload,
        "polynomial": polynomial, "polynomial_sha256": digest(polynomial),
        "paths": paths, "children": sorted(children),
    }


def validate(records, expected_ids, expected_polynomials):
    ids = [r["relation_id"] for r in records]
    if len(ids) != len(set(ids)): raise ValueError("duplicate relation")
    if set(ids) != set(expected_ids): raise ValueError("missing or extra relation")
    for r in records:
        payload = relation_payload(r["source"], r["target"], r["port_matching"], r["direction"])
        if digest(payload) != r["relation_id"]: raise ValueError("decorated relation binding changed")
        if r["direction"] != "source_to_target": raise ValueError("direction reversed")
        if r["polynomial"] != expected_polynomials[r["relation_id"]]: raise ValueError("wrong regenerated polynomial")
        if digest(r["polynomial"]) != r["polynomial_sha256"]: raise ValueError("polynomial hash changed")
        declared = tuple(sorted(r["children"])); per_path = []
        for p in r["paths"]:
            if p["full_relation_id"] != r["relation_id"]: raise ValueError("inconsistent full-relation path binding")
            per_path.append(tuple(sorted(p["child_state_ids"])))
        if any(x != declared for x in per_path): raise ValueError("first-provenance child reuse")
    return True


def main():
    p1 = relation_payload("S1", "T1", [["L_0", "L_0"]]); rid1 = digest(p1)
    p2 = relation_payload("S2", "T2", [["L_0", "L_0"]]); rid2 = digest(p2)
    records = [
        make_record("S1", "T1", [["L_0", "L_0"]], [[[0], 1]], [
            {"full_relation_id": rid1, "path_id": "p1", "child_state_ids": ["c1", "c2"]},
            {"full_relation_id": rid1, "path_id": "p2", "child_state_ids": ["c1", "c2"]},
        ], ["c1", "c2"]),
        make_record("S2", "T2", [["L_0", "L_0"]], [[[1], -1]], [
            {"full_relation_id": rid2, "path_id": "q1", "child_state_ids": []},
        ], []),
    ]
    expected_ids = [r["relation_id"] for r in records]
    expected_poly = {r["relation_id"]: deepcopy(r["polynomial"]) for r in records}
    validate(records, expected_ids, expected_poly)
    mutations = {}

    cases = {}
    cases["missing_relation"] = records[:1]
    cases["duplicate_relation"] = records + [deepcopy(records[0])]
    x = deepcopy(records); x[0]["port_matching"] = [["L_0", "L_1"]]; cases["altered_port_matching"] = x
    x = deepcopy(records); x[0]["source"], x[0]["target"] = x[0]["target"], x[0]["source"]; x[0]["direction"] = "target_to_source"; cases["reversed_direction"] = x
    x = deepcopy(records); x[0]["polynomial"] = [[[0], 2]]; cases["wrong_polynomial"] = x
    x = deepcopy(records); x[0]["paths"][1]["child_state_ids"] = ["c1"]; cases["inconsistent_path_binding"] = x

    for name, case in cases.items():
        try:
            validate(case, expected_ids, expected_poly)
        except Exception as exc:
            mutations[name] = {"rejected": True, "reason": str(exc)}
        else:
            mutations[name] = {"rejected": False, "reason": "mutation passed"}
    if not all(x["rejected"] for x in mutations.values()): raise AssertionError(mutations)
    cert = {"schema": 1, "baseline": "VERIFIED", "mutations": mutations, "status": "VERIFIED"}
    cert["normalized_sha256_without_hash"] = digest(cert)
    out = HERE / "certificates"; out.mkdir(exist_ok=True)
    (out / "mutation_certificate.json").write_text(stable(cert) + "\n")
    print(stable(cert))


if __name__ == "__main__": main()

