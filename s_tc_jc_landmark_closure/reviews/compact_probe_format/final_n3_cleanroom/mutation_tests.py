#!/usr/bin/env python3
"""Mutation-sensitive semantic tests for the final n=3 compact family.

Outer hashes are deliberately bypassed.  Every corruption is fed to the
clean-room graph/algebra audit, so rejection must arise from regenerated
relation semantics or completeness rather than stale file commitments.
"""

from __future__ import annotations

import base64
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import struct
import sys


HERE = Path(__file__).resolve().parent
N4 = HERE.parent / "final_n4_cleanroom"
sys.path[:0] = [str(HERE), str(N4)]

import audit_final_n3 as audit  # noqa: E402
import audit_final_n4 as common  # noqa: E402
from engine import file_sha256, load_invariants, stable_hash  # noqa: E402


PROJECT = HERE.parents[2]
SUMMARY = (PROJECT / "primary/certificates/"
           "compact_probe_schema3_n3_compact_s0_summary.json")
VERBOSE = (PROJECT / "primary/certificates/"
           "probe_extension_schema3_n3_final_summary.json")


class NullWriter:
    def __init__(self):
        self.records = 0

    def write(self, _row):
        self.records += 1


def encode(words):
    return base64.b64encode(
        struct.pack(f"<{len(words)}I", *words)).decode()


def refresh(row):
    row["path_record_id"] = stable_hash(
        {key: value for key, value in row.items()
         if key != "path_record_id"})


def words_for(row):
    return (
        list(common.decode_words(row["p_words_base64_le_u32"],
                                 int(row["p_word_count"]))),
        list(common.decode_words(row["q_words_base64_le_u32"],
                                 int(row["q_word_count"]))),
    )


def subset_path(compact, absolute_index):
    result = deepcopy(compact)
    row = next(item for item in result["paths"]
               if int(item["path_index"]) == absolute_index)
    p_words, q_words = words_for(row)
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
                           if key.endswith("_pullback_id")
                           and value not in {None, "0"})
    result["paths"] = [row]
    result["witnesses"] = {
        index: result["witnesses"][index] for index in witnesses}
    result["transports"] = {
        index: result["transports"][index] for index in transports}
    result["polynomials"] = {
        identifier: result["polynomials"][identifier]
        for identifier in polynomials}
    result["summary"]["path_range"] = [absolute_index, absolute_index + 1]
    result["summary"]["counts"] = dict(sorted(Counter(
        audit.CLASS_BY_CODE[word >> 29] for word in words).items()))
    return result


def run(candidate, inventory, verbose, invariants):
    writer = NullWriter()
    result = audit.audit_shard(
        candidate, inventory, verbose, invariants, writer)
    return result, writer.records


def main():
    compact = common.load_compact(SUMMARY, audit.EXPECTED_COMPACT["s0"])
    inventory, _commitment, _inputs = common.build_inventory([
        common.resolve(path, SUMMARY)
        for path in compact["summary"]["base_summaries"]
    ])
    verbose = audit.load_verbose(VERBOSE)
    invariants = load_invariants(
        PROJECT.parent /
        "strong_level2_phylo_identifiability/src/jc_root_spanning_atlas_data.py",
        PROJECT / "primary/seventh_invariant.json")
    generic_iso = subset_path(compact, 0)
    strict_t = subset_path(compact, 1)
    baseline_generic, generic_records = run(
        generic_iso, inventory, verbose, invariants)
    baseline_strict, strict_records = run(
        strict_t, inventory, verbose, invariants)
    cases = []

    def add(name, baseline, mutate):
        candidate = deepcopy(baseline)
        mutation_details = mutate(candidate) or {}
        try:
            run(candidate, inventory, verbose, invariants)
        except Exception as exc:
            cases.append({
                "mutation": name, "rejected": True,
                "mutation_details": mutation_details,
                "first_failure": str(exc)[:2400],
            })
        else:
            cases.append({
                "mutation": name, "rejected": False,
                "mutation_details": mutation_details,
                "first_failure": None,
            })

    def delete_relation(candidate):
        row = candidate["paths"][0]; words, _ = words_for(row)
        words.pop(); row["p_word_count"] = len(words)
        row["p_words_base64_le_u32"] = encode(words); refresh(row)
    add("delete_relation", generic_iso, delete_relation)

    def duplicate_relation(candidate):
        row = candidate["paths"][0]; words, _ = words_for(row)
        words.insert(0, words[0]); row["p_word_count"] = len(words)
        row["p_words_base64_le_u32"] = encode(words); refresh(row)
    add("duplicate_relation", generic_iso, duplicate_relation)

    def truncate_q(candidate):
        row = candidate["paths"][0]
        raw = base64.b64decode(row["q_words_base64_le_u32"])
        row["q_words_base64_le_u32"] = base64.b64encode(raw[:-1]).decode()
        refresh(row)
    add("truncate_conditional_q", strict_t, truncate_q)

    def altered_arc_order(candidate):
        row = candidate["paths"][0]
        row["source_p_arcs"][0], row["source_p_arcs"][1] = (
            row["source_p_arcs"][1], row["source_p_arcs"][0])
        refresh(row)
    add("altered_arc_order", generic_iso, altered_arc_order)

    def wrong_generic_separator(candidate):
        row = candidate["paths"][0]; words, _ = words_for(row)
        positions = [i for i, word in enumerate(words) if word >> 29 == 0]
        first = positions[0]
        old = words[first] & audit.INDEX_MASK
        replacement = next(words[pos] & audit.INDEX_MASK for pos in positions[1:]
                           if (words[pos] & audit.INDEX_MASK) != old)
        words[first] = replacement
        row["p_words_base64_le_u32"] = encode(words); refresh(row)
        return {"old_witness_index": old,
                "replacement_witness_index": replacement}
    add("valid_separator_from_wrong_generic_relation", generic_iso,
        wrong_generic_separator)

    def wrong_strict_separator(candidate):
        row = candidate["paths"][0]; words, _ = words_for(row)
        positions = [i for i, word in enumerate(words) if word >> 29 == 1]
        first = positions[0]
        old = words[first] & audit.INDEX_MASK
        replacement = next(words[pos] & audit.INDEX_MASK for pos in positions[1:]
                           if (words[pos] & audit.INDEX_MASK) != old)
        words[first] = (1 << 29) | replacement
        row["p_words_base64_le_u32"] = encode(words); refresh(row)
        return {"old_witness_index": old,
                "replacement_witness_index": replacement}
    add("valid_strict_separator_from_wrong_relation", strict_t,
        wrong_strict_separator)

    def wrong_polynomial(candidate):
        identifier = sorted(candidate["polynomials"])[0]
        candidate["polynomials"][identifier]["terms"][0][1] += 1
        return {"polynomial_id": identifier}
    add("wrong_polynomial_body", generic_iso, wrong_polynomial)

    def strict_sign(candidate):
        index, record = next((index, record)
                             for index, record in candidate["witnesses"].items()
                             if record["classification"] ==
                             "strict_open_cube_separation")
        record["probe_witness"]["target_strict_sign"] *= -1
        return {"witness_index": index}
    add("wrong_strict_sign", strict_t, strict_sign)

    def port_correspondence(candidate):
        index, record = next((index, record)
                             for index, record in candidate["transports"].items()
                             if len(record["transport"]["port_transport"]) > 1)
        ports = record["transport"]["port_transport"]
        ports[0][1], ports[1][1] = ports[1][1], ports[0][1]
        return {"transport_index": index}
    add("port_correspondence_alteration", generic_iso, port_correspondence)

    def transport_vertex(candidate):
        index, record = next((index, record)
                             for index, record in candidate["transports"].items()
                             if len(record["transport"]["vertex_transport"]) > 1)
        vertices = record["transport"]["vertex_transport"]
        vertices[0][1], vertices[1][1] = vertices[1][1], vertices[0][1]
        return {"transport_index": index}
    add("transport_vertex_corruption", generic_iso, transport_vertex)

    def t_transport(candidate):
        index, record = next((index, record)
                             for index, record in candidate["transports"].items()
                             if record["classification"] == "ordinary_T")
        edges = record["transport"]["t_quotient_edge_permutation"]
        edges[0][1], edges[1][1] = edges[1][1], edges[0][1]
        return {"transport_index": index}
    add("ordinary_T_transport_corruption", strict_t, t_transport)

    def class_flip(candidate):
        row = candidate["paths"][0]; words, _ = words_for(row)
        position = next(i for i, word in enumerate(words) if word >> 29 == 0)
        words[position] = (1 << 29) | (words[position] & audit.INDEX_MASK)
        row["p_words_base64_le_u32"] = encode(words); refresh(row)
    add("classification_code_flip", generic_iso, class_flip)

    def source_target_reversal(candidate):
        row = candidate["paths"][0]
        for left, right in (
            ("source_parent_graph_id", "target_parent_graph_id"),
            ("source_parent_normalized_graph_id",
             "target_parent_normalized_graph_id"),
            ("source_p_arcs", "target_p_arcs"),
        ):
            row[left], row[right] = row[right], row[left]
        refresh(row)
    add("source_target_reversal", generic_iso, source_target_reversal)

    def wrong_parent(candidate):
        row = candidate["paths"][0]
        row["source_parent_normalized_graph_id"] = "0" * 64; refresh(row)
    add("wrong_parent", generic_iso, wrong_parent)

    def wrong_root(candidate):
        row = candidate["paths"][0]
        row["fixed_full_root_case_id"] = "f" * 64; refresh(row)
    add("wrong_root", generic_iso, wrong_root)

    def cross_path(candidate):
        row = candidate["paths"][0]
        row["base_path_binding_id"] = inventory[1]["base_path_binding_id"]
        refresh(row)
    add("cross_path_merge", generic_iso, cross_path)

    def incomplete(candidate):
        candidate["paths"] = []
    add("incomplete_shard_coverage", generic_iso, incomplete)

    def duplicate_path(candidate):
        candidate["paths"].append(deepcopy(candidate["paths"][0]))
    add("duplicate_path_row", generic_iso, duplicate_path)

    failed = [row["mutation"] for row in cases if not row["rejected"]]
    payload = {
        "schema": "compact-probe-final-n3-cleanroom-mutations-v1",
        "status": "VERIFIED" if not failed else "FALSE",
        "scope": (
            "Semantic mutation sensitivity after bypassing outer hashes; "
            "alternate witnesses are accepted only when independently valid "
            "on the same exact relation."),
        "compact_summary": common.normalized(SUMMARY),
        "compact_summary_sha256": audit.EXPECTED_COMPACT["s0"],
        "verbose_summary": common.normalized(VERBOSE),
        "verbose_summary_sha256": audit.EXPECTED_VERBOSE,
        "baseline": {
            "path_0": baseline_generic,
            "path_0_relations": generic_records,
            "path_1": baseline_strict,
            "path_1_relations": strict_records,
        },
        "mutations": cases,
        "accepted_mutations": failed,
        "implementation": common.normalized(Path(__file__)),
        "implementation_sha256": file_sha256(Path(__file__)),
        "audit_script_sha256": file_sha256(HERE / "audit_final_n3.py"),
        "n3_engine_sha256": file_sha256(HERE / "engine_n3.py"),
        "n4_engine_sha256": file_sha256(N4 / "engine.py"),
    }
    output = HERE / "certificates/mutation_tests.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"], "mutations": len(cases),
        "accepted": failed, "output": common.normalized(output),
        "output_sha256": file_sha256(output),
    }, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
