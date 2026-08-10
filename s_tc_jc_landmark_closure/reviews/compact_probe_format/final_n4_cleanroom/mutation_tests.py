#!/usr/bin/env python3
"""Mutation-sensitive tests for the final n=4 compact semantics.

The tests deliberately bypass outer file hashes and ask whether the
clean-room graph/algebra/verbose comparison itself rejects each corruption.
"""

from __future__ import annotations

import base64
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import struct
import sys

import audit_final_n4 as audit
from engine import file_sha256, load_invariants, stable_hash


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]


class NullWriter:
    def __init__(self):
        self.records = 0

    def write(self, _row):
        self.records += 1


def encode(words):
    return base64.b64encode(struct.pack(f"<{len(words)}I", *words)).decode()


def refresh(row):
    row["path_record_id"] = stable_hash(
        {key: value for key, value in row.items() if key != "path_record_id"})


def one_path(compact):
    result = deepcopy(compact)
    row = result["paths"][0]
    p_words = list(audit.decode_words(row["p_words_base64_le_u32"],
                                      int(row["p_word_count"])))
    q_words = list(audit.decode_words(row["q_words_base64_le_u32"],
                                      int(row["q_word_count"])))
    words = p_words + q_words
    witnesses = {word & audit.INDEX_MASK for word in words
                 if word >> 29 in (0, 1)}
    transports = {int(row["base_transport_index"])} | {
        word & audit.INDEX_MASK for word in words if word >> 29 in (2, 3)
    }
    polynomials = set()
    for index in witnesses:
        body = result["witnesses"][index]["probe_witness"]
        polynomials.update(str(value) for key, value in body.items()
                           if key.endswith("_pullback_id") and value not in {None, "0"})
    result["paths"] = [row]
    result["witnesses"] = {index: result["witnesses"][index]
                           for index in witnesses}
    result["transports"] = {index: result["transports"][index]
                            for index in transports}
    result["polynomials"] = {identifier: result["polynomials"][identifier]
                             for identifier in polynomials}
    result["summary"]["path_range"] = [0, 1]
    result["summary"]["counts"] = dict(sorted(Counter(
        audit.CLASS_BY_CODE[word >> 29] for word in words).items()))
    return result


def run(candidate, inventory, verbose, invariants):
    writer = NullWriter()
    return audit.audit_shard(candidate, inventory, verbose, invariants, writer)


def main():
    summary_path = (PROJECT / "primary/certificates/"
                    "compact_probe_theta2_compact_n4_s0_summary.json")
    compact = audit.load_compact(summary_path, audit.EXPECTED_COMPACT["s0"])
    inventory, _commitment, _inputs = audit.build_inventory([
        audit.resolve(path, summary_path)
        for path in compact["summary"]["base_summaries"]
    ])
    verbose_path = (PROJECT / "primary/certificates/"
                    "probe_extension_theta2_schema3_final_summary.json")
    verbose = audit.load_verbose(verbose_path)
    invariants = load_invariants(
        PROJECT.parent / "strong_level2_phylo_identifiability/src/"
        "jc_root_spanning_atlas_data.py",
        PROJECT / "primary/seventh_invariant.json")
    baseline = one_path(compact)
    baseline_result = run(baseline, inventory, verbose, invariants)
    cases = []

    def add(name, mutate):
        candidate = deepcopy(baseline)
        mutate(candidate)
        try:
            run(candidate, inventory, verbose, invariants)
        except Exception as exc:
            cases.append({
                "mutation": name, "rejected": True,
                "first_failure": str(exc)[:2000],
            })
        else:
            cases.append({"mutation": name, "rejected": False,
                          "first_failure": None})

    def pwords(candidate):
        row = candidate["paths"][0]
        return row, list(audit.decode_words(row["p_words_base64_le_u32"],
                                            int(row["p_word_count"])))

    def delete_relation(candidate):
        row, words = pwords(candidate); words.pop()
        row["p_word_count"] = len(words); row["p_words_base64_le_u32"] = encode(words)
        refresh(row)
    add("delete_relation", delete_relation)

    def duplicate_relation(candidate):
        row, words = pwords(candidate); words.insert(0, words[0])
        row["p_word_count"] = len(words); row["p_words_base64_le_u32"] = encode(words)
        refresh(row)
    add("duplicate_relation", duplicate_relation)

    def truncate_q(candidate):
        row = candidate["paths"][0]
        raw = base64.b64decode(row["q_words_base64_le_u32"])
        row["q_words_base64_le_u32"] = base64.b64encode(raw[:-1]).decode()
        refresh(row)
    add("truncate_conditional_q", truncate_q)

    def wrong_relation(candidate):
        row, words = pwords(candidate)
        positions = [i for i, word in enumerate(words) if word >> 29 == 0]
        used = [word & audit.INDEX_MASK for word in words if word >> 29 == 0]
        position = positions[0]; old = words[position] & audit.INDEX_MASK
        replacement = next(value for value in used if value != old)
        words[position] = replacement
        row["p_words_base64_le_u32"] = encode(words); refresh(row)
    add("wrong_relation_witness_index", wrong_relation)

    def wrong_polynomial(candidate):
        identifier = sorted(candidate["polynomials"])[0]
        candidate["polynomials"][identifier]["terms"][0][1] += 1
    add("wrong_polynomial_body", wrong_polynomial)

    def alter_arc_order(candidate):
        row = candidate["paths"][0]
        row["source_p_arcs"][0], row["source_p_arcs"][1] = (
            row["source_p_arcs"][1], row["source_p_arcs"][0])
        refresh(row)
    add("altered_arc_order", alter_arc_order)

    def port_correspondence(candidate):
        record = next(row for row in candidate["transports"].values()
                      if row["transport"]["port_transport"])
        ports = record["transport"]["port_transport"]
        ports[0][1], ports[1][1] = ports[1][1], ports[0][1]
    add("port_correspondence_alteration", port_correspondence)

    def transport_corruption(candidate):
        record = next(row for row in candidate["transports"].values()
                      if len(row["transport"]["vertex_transport"]) > 1)
        vertices = record["transport"]["vertex_transport"]
        vertices[0][1], vertices[1][1] = vertices[1][1], vertices[0][1]
    add("transport_vertex_corruption", transport_corruption)

    def source_target_reversal(candidate):
        row = candidate["paths"][0]
        for left, right in (
            ("source_parent_graph_id", "target_parent_graph_id"),
            ("source_parent_normalized_graph_id", "target_parent_normalized_graph_id"),
            ("source_p_arcs", "target_p_arcs"),
        ):
            row[left], row[right] = row[right], row[left]
        refresh(row)
    add("source_target_reversal", source_target_reversal)

    def wrong_parent(candidate):
        row = candidate["paths"][0]
        row["source_parent_normalized_graph_id"] = "0" * 64; refresh(row)
    add("wrong_parent", wrong_parent)

    def wrong_root(candidate):
        row = candidate["paths"][0]
        row["fixed_full_root_case_id"] = "f" * 64; refresh(row)
    add("wrong_root", wrong_root)

    def cross_path(candidate):
        row = candidate["paths"][0]
        row["base_path_binding_id"] = inventory[1]["base_path_binding_id"]
        refresh(row)
    add("cross_path_merge", cross_path)

    def incomplete(candidate):
        candidate["paths"] = []
    add("incomplete_shard_coverage", incomplete)

    def duplicate_path(candidate):
        candidate["paths"].append(deepcopy(candidate["paths"][0]))
    add("duplicate_path_row", duplicate_path)

    failed = [row["mutation"] for row in cases if not row["rejected"]]
    payload = {
        "schema": "compact-probe-final-n4-cleanroom-mutations-v1",
        "status": "VERIFIED" if not failed else "FALSE",
        "scope": "semantic mutation sensitivity after bypassing outer hashes",
        "compact_summary": audit.normalized(summary_path),
        "compact_summary_sha256": audit.EXPECTED_COMPACT["s0"],
        "verbose_summary": audit.normalized(verbose_path),
        "verbose_summary_sha256": audit.EXPECTED_VERBOSE,
        "baseline": baseline_result,
        "mutations": cases,
        "accepted_mutations": failed,
        "implementation": audit.normalized(Path(__file__)),
        "implementation_sha256": file_sha256(Path(__file__)),
        "audit_script_sha256": file_sha256(HERE / "audit_final_n4.py"),
        "engine_sha256": file_sha256(HERE / "engine.py"),
    }
    output = HERE / "certificates/mutation_tests.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": payload["status"],
                      "mutations": len(cases), "accepted": failed,
                      "output": audit.normalized(output),
                      "output_sha256": file_sha256(output)}, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
