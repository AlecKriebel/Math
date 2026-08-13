#!/usr/bin/env python3
"""Mutation sensitivity for the direct-anchor closure certificate."""

from __future__ import annotations

from pathlib import Path
import copy
import json

from verify_direct_anchor_probes import Failure, load_package, validate_structure


HERE = Path(__file__).resolve().parent
OUT = HERE / "certificates/mutation_results.json"


def relation_witness_binding(rows):
    witnesses = {r["witness_id"]: r for r in rows["witnesses"]}
    for record in rows["p_relations"] + rows["q_relations"]:
        wid = record.get("witness_id")
        if wid is None:
            continue
        if wid not in witnesses:
            raise Failure("missing witness")
        witness = witnesses[wid]
        if (witness["source_graph_sha256"], witness["target_graph_sha256"]) != (
            record["source_graph_sha256"], record["target_graph_sha256"]
        ):
            raise Failure("separator assigned to wrong directed relation")


def run_one(name, mutate, expected_fragment, algebra_binding=False):
    summary, original = load_package()
    rows = copy.deepcopy(original)
    mutate(rows)
    try:
        validate_structure(summary, rows, check_inputs=False)
        if algebra_binding:
            relation_witness_binding(rows)
    except (Failure, KeyError, IndexError, ValueError) as exc:
        reason = str(exc)
        if expected_fragment and expected_fragment not in reason:
            return {"name": name, "rejected": False,
                    "reason": f"wrong failure: {reason!r}; wanted {expected_fragment!r}"}
        return {"name": name, "rejected": True, "reason": reason}
    return {"name": name, "rejected": False, "reason": "mutation was accepted"}


def main():
    def delete_anchor(rows):
        rows["anchors"].pop()

    def alter_direct_id(rows):
        rows["anchors"][0]["direct_anchor_id"] = "0" * 64

    def alter_transport(rows):
        rows["anchors"][0]["transport"]["vertex_transport"][0][1] += 1

    def reverse_direction(rows):
        rows["anchors"][0]["direction"] = "target_precedes_source"

    def alter_t_choice(rows):
        row = next(r for r in rows["anchors"] if r["classification"] == "ordinary_T")
        row["classification"] = "labelled_isomorphism"
        row["transport"]["classification"] = "labelled_isomorphism"

    def delete_p(rows):
        rows["p_relations"].pop()

    def delete_q(rows):
        rows["q_relations"].pop()

    def swap_pq_order(rows):
        row = rows["q_relations"][0]
        row["stage"] = "A_plus_p"
        row["new_label"] = "L_4"

    def alter_parent(rows):
        row = rows["q_relations"][0]
        other = next(r for r in rows["p_relations"] if r["relation_id"] != row["parent_relation_id"])
        row["parent_relation_id"] = other["relation_id"]

    def alter_arc(rows):
        row = rows["p_relations"][0]
        row["source_arc"] = list(reversed(row["source_arc"]))

    def reverse_source_target(rows):
        row = rows["p_relations"][0]
        row["source_graph_sha256"], row["target_graph_sha256"] = (
            row["target_graph_sha256"], row["source_graph_sha256"]
        )
        row["source_arc"], row["target_arc"] = row["target_arc"], row["source_arc"]

    def swap_valid_witnesses(rows):
        separated = [r for r in rows["p_relations"] + rows["q_relations"] if r.get("witness_id")]
        first = separated[0]
        second = next(r for r in separated[1:]
                      if (r["source_graph_sha256"], r["target_graph_sha256"]) !=
                         (first["source_graph_sha256"], first["target_graph_sha256"]))
        first["witness_id"], second["witness_id"] = second["witness_id"], first["witness_id"]

    tests = [
        ("delete_direct_anchor", delete_anchor, "62-element", False),
        ("alter_direct_anchor_id", alter_direct_id, "unknown or altered", False),
        ("alter_canonical_transport", alter_transport, "canonical transport", False),
        ("reverse_source_target_direction", reverse_direction, "orientation changed", False),
        ("alter_ordinary_T_choice", alter_t_choice, "classification changed", False),
        ("delete_A_plus_p_relation", delete_p, "required A+p relation deleted", False),
        ("delete_A_plus_p_plus_q_relation", delete_q, "required A+p+q relation deleted", False),
        ("swap_p_q_order", swap_pq_order, "p/q order", False),
        ("alter_q_parent_transport", alter_parent, "parent binding", False),
        ("alter_insertion_arc", alter_arc, "content address", False),
        ("reverse_relation_graphs", reverse_source_target, "content address", False),
        ("assign_valid_separator_to_wrong_relation", swap_valid_witnesses,
         "separator assigned to wrong directed relation", True),
    ]
    results = [run_one(*test) for test in tests]
    payload = {
        "schema": 1,
        "status": "VERIFIED" if all(r["rejected"] for r in results) else "FALSE",
        "mutation_count": len(results),
        "mutations": results,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    if payload["status"] != "VERIFIED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
