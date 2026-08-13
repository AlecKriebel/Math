#!/usr/bin/env python3
"""Fail-closed independent verifier for path-bound p/q terminal extension."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cleanroom_probe import (
    RootedGraph, admissible_internal_blob_arcs, classify_topology, delete_port,
    digest, expected_base_relation_id, expected_relation_id, insert_port, invariant_pullback,
    jacobian_rank_certificate, poly_digest, quartet_tensor, standard_strong,
    validate_rooted, verify_strict_factor,
)


ALLOWED = {"labelled_isomorphism", "ordinary_T"}


class VerificationError(AssertionError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def pairs(x):
    return [(int(a), int(b)) for a, b in x]


def graph(record, side):
    return RootedGraph.from_json(record[f"{side}_graph"])


def verify_base(base):
    sg, tg = graph(base, "source"), graph(base, "target")
    require(base.get("source_graph_id") == digest(sg.to_json()), "base source rooted graph id mismatch")
    require(base.get("target_graph_id") == digest(tg.to_json()), "base target rooted graph id mismatch")
    require(base.get("base_source_rooted_graph_id") == base.get("source_graph_id"), "base source identity not rooted")
    require(base.get("base_target_rooted_graph_id") == base.get("target_graph_id"), "base target identity not rooted")
    require(base.get("relation_id") == expected_base_relation_id(base), "base identity omits root case/rooted graph")
    require(base.get("state_identity_sha256") == base.get("relation_id"), "state identity is weaker than raw base identity")
    require(not validate_rooted(sg), f"base {base['relation_id']} source rooted invalid")
    require(not validate_rooted(tg), f"base {base['relation_id']} target rooted invalid")
    ss, src_roots = standard_strong(sg)
    ts, tgt_roots = standard_strong(tg)
    require(ss and ts, f"base {base['relation_id']} not locked standard strong")
    if "standard_strong_rooting_count_source" in base:
        require(src_roots == base["standard_strong_rooting_count_source"], "source rooting count mismatch")
        require(tgt_roots == base["standard_strong_rooting_count_target"], "target rooting count mismatch")
    require(base["classification"] in ALLOWED, "base terminal is not allowed")
    candidates = classify_topology(sg, tg)
    stored = dict(pairs(base["transport"]))
    require(any(c == base["classification"] and m == stored for c, m in candidates),
            f"base {base['relation_id']} transport/classification not regenerated")
    require(sorted(map(tuple, base["port_matching"])) == sorted((x, x) for x in set(sg.label_map.values())),
            "base physical port matching is not complete identity in locked labels")
    base_lower = jacobian_rank_certificate(sg)["rank"]
    require(base.get("generic_rank_upper_certificate") == "frozen_base_terminal_rank",
            "base exact-rank dependency is not explicitly identified")
    require(base_lower == base.get("generic_rank_exact"),
            f"base {base['relation_id']} advertised rank lacks regenerated lower certificate")


def verify_provenance(child, base, parent):
    for k in ("raw_terminal_id", "fixed_full_root_case_id", "restoration_root_id", "parent_path_id",
              "Q_s", "Q_t", "port_matching", "base_source_rooted_graph_id",
              "base_target_rooted_graph_id"):
        require(child.get(k) == base.get(k), f"{child.get('relation_id')} changed path-bound provenance {k}")
    require(child.get("base_relation_id") == base["relation_id"], "base relation binding changed")
    require(child.get("parent_relation_id") == parent["relation_id"], "wrong immediate parent")


def verify_witness(rec, sg, tg):
    witness = rec.get("witness")
    require(isinstance(witness, dict), f"separated relation {rec['relation_id']} has no witness body")
    quartet = tuple(witness["quartet"])
    st = quartet_tensor(sg, quartet)
    tt = quartet_tensor(tg, quartet)
    require(digest([poly_digest(p) for p in st]) == witness["source_quartet_tensor_sha256"],
            f"{rec['relation_id']} source graph/tensor mismatch")
    require(digest([poly_digest(p) for p in tt]) == witness["target_quartet_tensor_sha256"],
            f"{rec['relation_id']} target graph/tensor mismatch")
    ps = invariant_pullback(st, witness["invariant"])
    pt = invariant_pullback(tt, witness["invariant"])
    require(poly_digest(ps) == witness["source_pullback_sha256"],
            f"{rec['relation_id']} source graph/polynomial mismatch")
    require(poly_digest(pt) == witness["target_pullback_sha256"],
            f"{rec['relation_id']} target graph/polynomial mismatch")
    orientation = witness["orientation"]
    if orientation == "source_nonzero_target_zero":
        require(bool(ps) and not pt, f"{rec['relation_id']} does not obstruct source containment")
        if witness.get("strict_factor_certificate") is not None:
            require(verify_strict_factor(ps, witness["strict_factor_certificate"]),
                    f"{rec['relation_id']} strict source factor certificate fails")
    elif orientation == "source_zero_target_strict":
        require(not ps and bool(pt), f"{rec['relation_id']} wrong strict orientation")
        require(witness.get("strict_factor_certificate") is not None and
                verify_strict_factor(pt, witness["strict_factor_certificate"]),
                f"{rec['relation_id']} strict target factor certificate fails")
    else:
        raise VerificationError(f"unsupported witness orientation {orientation}")


def verify_child(rec, parent, base):
    require(rec["relation_id"] == expected_relation_id(rec), f"relation id mismatch {rec.get('relation_id')}")
    verify_provenance(rec, base, parent)
    label = rec["new_label"]
    source_arc, target_arc = tuple(rec["source_arc"]), tuple(rec["target_arc"])
    psg, ptg = graph(parent, "source"), graph(parent, "target")
    expected_s, expected_si = insert_port(psg, source_arc, label)
    expected_t, expected_ti = insert_port(ptg, target_arc, label)
    sg, tg = graph(rec, "source"), graph(rec, "target")
    require(sg == expected_s and tg == expected_t, f"{rec['relation_id']} graph is not exact parent insertion")
    require(rec["source_inclusion"] == expected_si and rec["target_inclusion"] == expected_ti,
            f"{rec['relation_id']} inclusion transport mismatch")
    require(not validate_rooted(sg) and not validate_rooted(tg), f"{rec['relation_id']} rooted class failure")
    require(standard_strong(sg)[0] and standard_strong(tg)[0],
            f"{rec['relation_id']} standard-strong class failure")
    ds, sd = delete_port(sg, label)
    dt, td = delete_port(tg, label)
    require(ds == psg and dt == ptg, f"{rec['relation_id']} deletion does not recover exact parent")
    require(rec["source_deletion"] == sd and rec["target_deletion"] == td,
            f"{rec['relation_id']} deletion map mismatch")
    require(rec["parent_transport"] == parent["transport"], f"{rec['relation_id']} parent transport changed")
    if rec["classification"] in ALLOWED:
        candidates = classify_topology(sg, tg, parent["transport"])
        stored = dict(pairs(rec["transport"]))
        require(any(c == rec["classification"] and m == stored for c, m in candidates),
                f"{rec['relation_id']} allowed map is absent or incoherent with parent")
        require(rec.get("witness") is None, f"{rec['relation_id']} allowed relation carries separator")
    elif rec["classification"] == "generic_polynomial_separation":
        require(rec.get("transport") is None, f"{rec['relation_id']} separated relation carries topology map")
        verify_witness(rec, sg, tg)
    else:
        raise VerificationError(f"unresolved/unsupported child classification {rec['classification']}")


def verify_coverage(records, parents, base_by_id, level):
    parent_ids = set(parents)
    seen = set()
    grouped = {p: [] for p in parent_ids}
    for rec in records:
        require(rec.get("level") == level, f"wrong level in {rec.get('relation_id')}")
        pid = rec.get("parent_relation_id")
        require(pid in parent_ids, f"unknown/wrong parent {pid}")
        key = (pid, tuple(rec["source_arc"]), tuple(rec["target_arc"]), rec["new_label"])
        require(key not in seen, f"duplicate decorated relation {key}")
        seen.add(key)
        grouped[pid].append(rec)
    for pid, parent in parents.items():
        base = base_by_id[parent.get("base_relation_id", parent["relation_id"])]
        expected = {
            (pid, sa, ta, level)
            for sa in admissible_internal_blob_arcs(graph(parent, "source"))
            for ta in admissible_internal_blob_arcs(graph(parent, "target"))
        }
        got = {(pid, tuple(r["source_arc"]), tuple(r["target_arc"]), r["new_label"]) for r in grouped[pid]}
        require(got == expected, f"{level} arc hard cover differs: missing={sorted(expected-got)} extra={sorted(got-expected)}")
        declared_key = "p_child_relation_ids" if level == "p" else "q_child_relation_ids"
        require(sorted(parent.get(declared_key, [])) == sorted(r["relation_id"] for r in grouped[pid]),
                f"{level} per-path child set was merged, dropped, or borrowed from another rooted state")
        for rec in grouped[pid]:
            verify_child(rec, parent, base)


def verify_payload(payload, verify_ranks=True):
    require(payload.get("schema") == "stc-jc-probe-extension-review-v1", "wrong schema")
    bases = payload.get("base_relations", [])
    require(bases, "no raw allowed base terminals")
    base_by_id = {}
    raw_ids = set()
    state_identities = {}
    for b in bases:
        require(b["relation_id"] not in base_by_id, "duplicate base relation id")
        require(b["raw_terminal_id"] not in raw_ids, "deduplicated state substituted for raw terminal coverage")
        base_by_id[b["relation_id"]] = b
        raw_ids.add(b["raw_terminal_id"])
        identity = (b.get("fixed_full_root_case_id"), b.get("source_graph_id"), b.get("target_graph_id"))
        sid = b.get("state_identity_sha256")
        require(sid not in state_identities or state_identities[sid] == identity,
                "one canonical state merged distinct root cases or rooted graph ids")
        state_identities[sid] = identity
        verify_base(b)
    p = payload.get("p_relations", [])
    verify_coverage(p, base_by_id, base_by_id, "p")
    allowed_p = {r["relation_id"]: r for r in p if r["classification"] in ALLOWED}
    q = payload.get("q_relations", [])
    verify_coverage(q, allowed_p, base_by_id, "q")
    # No q record may descend from a separated p relation; unknown parents were
    # already rejected above.
    relation_ids = [r["relation_id"] for r in p + q]
    require(len(relation_ids) == len(set(relation_ids)), "duplicate relation id across levels")
    if verify_ranks:
        unique = {}
        for rec in p + q:
            for side in ("source", "target"):
                g = graph(rec, side)
                gid = digest(g.to_json())
                unique[gid] = g
        advertised = payload.get("rank_records", {})
        require(set(advertised) == set(unique), "rank-record graph hard cover mismatch")
        for gid, g in sorted(unique.items()):
            stored = advertised[gid]
            upper_kind = stored.get("upper_certificate")
            if upper_kind == "level1_cycle_2n_minus_1":
                require(len(g.reticulations) == 1, f"wrong level-one upper certificate for {gid}")
                upper = 2 * len(g.label_map) - 1
            elif upper_kind == "base_plus_two_per_port":
                occurrences = [r for r in p + q if gid in (r["source_graph_id"], r["target_graph_id"])]
                uppers = {
                    base_by_id[r["base_relation_id"]]["generic_rank_exact"] + (2 if r["level"] == "p" else 4)
                    for r in occurrences
                }
                require(len(uppers) == 1, f"inconsistent base-plus-two upper certificate for {gid}")
                upper = next(iter(uppers))
            else:
                raise VerificationError(f"unsupported exact-rank upper certificate {upper_kind} for {gid}")
            actual = jacobian_rank_certificate(g, structural_upper_bound=upper)
            actual["upper_certificate"] = upper_kind
            require(actual == advertised[gid], f"Jacobian rank/minor certificate mismatch for {gid}")
            require(actual["exact"], f"Jacobian rank not closed by structural upper bound for {gid}")
    counts = {
        "base": len(bases),
        "p": len(p),
        "p_allowed": len(allowed_p),
        "q": len(q),
        "q_allowed": sum(r["classification"] in ALLOWED for r in q),
        "rank_graphs": len(payload.get("rank_records", {})),
    }
    return {"status": "EXACT_TESTS_PASS", "counts": counts, "payload_sha256": digest(payload)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artifact", type=Path)
    ap.add_argument("--skip-ranks", action="store_true")
    args = ap.parse_args()
    payload = json.loads(args.artifact.read_text())
    result = verify_payload(payload, verify_ranks=not args.skip_ranks)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
