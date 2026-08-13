#!/usr/bin/env python3
"""Focused semantic mutations for the compact-only gate.

The tests bypass outer file hashes deliberately.  Each mutation is applied to
an already parsed exact compact object and must be rejected by a regenerated
graph, algebra, relation-order, or transport-coherence check.
"""

from __future__ import annotations

import base64
from copy import deepcopy
import json
from pathlib import Path
import struct
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import semantic_gate as gate  # noqa: E402


def category(exc: BaseException) -> str:
    try:
        payload = json.loads(str(exc))
        return str(payload.get("category", "unknown"))
    except Exception:
        return type(exc).__name__


def expect_rejection(name, action, allowed_categories=None):
    try:
        action()
    except Exception as exc:
        found = category(exc)
        if allowed_categories is not None:
            gate.require(found in set(allowed_categories),
                         "unexpected_mutation_rejection_category",
                         mutation=name, found=found,
                         allowed=sorted(allowed_categories))
        return {"mutation": name, "rejected": True,
                "first_category": found}
    raise AssertionError(json.dumps({"category": "mutation_accepted",
                                     "mutation": name}, sort_keys=True))


def encoded(words):
    return base64.b64encode(struct.pack(f"<{len(words)}I", *words)).decode()


def setup():
    family = gate.FAMILIES["n3"]
    summary_path = gate.CERT / family.summary_pattern.format(shard=0)
    compact = gate.load_compact(summary_path, family.summary_sha256[0])
    base_paths = [gate.resolve(path, summary_path)
                  for path in compact["summary"]["base_summaries"]]
    inventory, commitment_rows, _inputs = gate.build_inventory(base_paths)
    gate.require(gate.inventory_commitment(commitment_rows) ==
                 compact["summary"]["path_inventory_sha256"],
                 "mutation_inventory_commitment")
    return family, compact, inventory, gate.load_invariants()


def path_union(compacts, expected):
    indices = [int(row["path_index"]) for compact in compacts
               for row in compact["paths"]]
    gate.require(indices == list(range(expected)),
                 "gapless_ordered_path_union")


def base_context(family, compact, inventory, path_index):
    row = next(row for row in compact["paths"]
               if int(row["path_index"]) == path_index)
    entry = inventory[path_index]
    source_parent = entry["source"]
    target_parent = entry["target"]
    base_record = compact["transports"][int(row["base_transport_index"])]
    base_mapping, _base_class = gate.derive_transport(
        family, source_parent, target_parent, base_record)
    source_arcs = gate.admissible_internal_arcs(source_parent)
    target_arcs = gate.admissible_internal_arcs(target_parent)
    p_keys = tuple((s, t) for s in source_arcs for t in target_arcs)
    p_words = gate.decode_words(row["p_words_base64_le_u32"], len(p_keys))
    q_words = gate.decode_words(row["q_words_base64_le_u32"],
                                int(row["q_word_count"]))
    return row, entry, source_parent, target_parent, base_mapping, p_keys, p_words, q_words


def replay_p(family, compact, inventory, invariants, path_index, p_flat,
             *, word=None, parent_mapping=None, mutated_compact=None):
    (row, entry, source_parent, target_parent, base_mapping,
     p_keys, p_words, _q_words) = base_context(
        family, compact, inventory, path_index)
    source_arc, target_arc = p_keys[p_flat]
    p0 = int(row["selected_port_count"])
    source, _ = gate.insert_port(source_parent, source_arc, f"L_{p0}")
    target, _ = gate.insert_port(target_parent, target_arc, f"L_{p0}")
    caches = {"descriptors": {}, "pullbacks": {}, "sign_proofs": {},
              "graph_audits": {}}
    used = {"witnesses": set(), "transports": set(), "polynomials": set()}
    return gate.evidence_check(
        family=family, word=p_words[p_flat] if word is None else word,
        compact=compact if mutated_compact is None else mutated_compact,
        source=source, target=target, port_count=p0 + 1,
        parent_mapping=base_mapping if parent_mapping is None else parent_mapping,
        invariants=invariants, caches=caches, used=used,
        context=[path_index, "p", p_flat])


def replay_q_under_first_T(family, compact, inventory, invariants,
                           *, force_bad_parent=False):
    path_index = 1
    p_flat = 4
    (row, _entry, source_parent, target_parent, base_mapping,
     p_keys, p_words, q_words) = base_context(
        family, compact, inventory, path_index)
    p0 = int(row["selected_port_count"])
    source_arc, target_arc = p_keys[p_flat]
    source_p, _ = gate.insert_port(source_parent, source_arc, f"L_{p0}")
    target_p, _ = gate.insert_port(target_parent, target_arc, f"L_{p0}")
    caches = {"descriptors": {}, "pullbacks": {}, "sign_proofs": {},
              "graph_audits": {}}
    used = {"witnesses": set(), "transports": set(), "polynomials": set()}
    p_evidence = gate.evidence_check(
        family=family, word=p_words[p_flat], compact=compact,
        source=source_p, target=target_p, port_count=p0 + 1,
        parent_mapping=base_mapping, invariants=invariants, caches=caches,
        used=used, context=[path_index, "p", p_flat])
    gate.require(p_evidence["classification"] == "ordinary_T",
                 "mutation_fixture_not_T")
    source_q_arcs = gate.admissible_internal_arcs(source_p)
    target_q_arcs = gate.admissible_internal_arcs(target_p)
    # p=4 is the first allowed p block and q-local=6 is its first T child.
    q_local = 6
    q_keys = tuple((s, t) for s in source_q_arcs for t in target_q_arcs)
    source_q, _ = gate.insert_port(
        source_p, q_keys[q_local][0], f"L_{p0 + 1}")
    target_q, _ = gate.insert_port(
        target_p, q_keys[q_local][1], f"L_{p0 + 1}")
    parent_mapping = p_evidence["mapping"]
    if force_bad_parent:
        first_source, first_target = parent_mapping[0]
        alternate = next(target for target in target_p.vertices
                         if target != first_target)
        parent_mapping = ((first_source, alternate), *parent_mapping[1:])
    return gate.evidence_check(
        family=family, word=q_words[q_local], compact=compact,
        source=source_q, target=target_q, port_count=p0 + 2,
        parent_mapping=parent_mapping, invariants=invariants,
        caches=caches, used=used,
        context=[path_index, "q", p_flat, q_local])


def main():
    family, compact, inventory, invariants = setup()
    results = []

    deleted = deepcopy(compact)
    deleted["paths"].pop(0)
    results.append(expect_rejection(
        "delete_path", lambda: path_union([deleted], 36),
        {"gapless_ordered_path_union"}))

    duplicated = deepcopy(compact)
    duplicated["paths"].insert(1, deepcopy(duplicated["paths"][0]))
    results.append(expect_rejection(
        "duplicate_path", lambda: path_union([duplicated], 36),
        {"gapless_ordered_path_union"}))

    altered_arc = deepcopy(compact)
    altered_arc["paths"][0]["source_p_arcs"][0] = [999, 1000]
    results.append(expect_rejection(
        "alter_arc",
        lambda: gate.require(
            tuple(tuple(x) for x in altered_arc["paths"][0]["source_p_arcs"]) ==
            gate.admissible_internal_arcs(inventory[0]["source"]),
            "source_p_arc_order"), {"source_p_arc_order"}))

    altered_order = deepcopy(compact)
    altered_order["paths"][0]["source_p_arcs"].reverse()
    results.append(expect_rejection(
        "alter_order",
        lambda: gate.require(
            tuple(tuple(x) for x in altered_order["paths"][0]["source_p_arcs"]) ==
            gate.admissible_internal_arcs(inventory[0]["source"]),
            "source_p_arc_order"), {"source_p_arc_order"}))

    witness_compact = deepcopy(compact)
    row = witness_compact["paths"][0]
    words = list(gate.decode_words(row["p_words_base64_le_u32"],
                                   int(row["p_word_count"])))
    # Preserve class 0 but move the valid relation onto a different valid
    # witness body from the same shard.
    words[0] = (0 << 29) | 1
    results.append(expect_rejection(
        "alter_witness",
        lambda: replay_p(family, witness_compact, inventory, invariants,
                         0, 0, word=words[0]),
        {"source_exact_pullback_sha256", "generic_separator_orientation"}))

    transport_compact = deepcopy(compact)
    # p=3 is a labelled isomorphism; transport index 2 is another valid
    # stored body but belongs to another decorated relation.
    wrong_transport_word = (2 << 29) | 2
    results.append(expect_rejection(
        "alter_transport",
        lambda: replay_p(family, transport_compact, inventory, invariants,
                         0, 3, word=wrong_transport_word),
        {"stored_quotient_canonicalization_not_common",
         "vertex_transport", "quotient_canonicalization_transport_not_unique",
         "transport_classification", "canonical_map_domain"}))

    # Change a separated relation to an allowed class, retaining a valid
    # library index.  Regeneration must reject the false class.
    changed_class_word = (2 << 29) | 0
    results.append(expect_rejection(
        "alter_class",
        lambda: replay_p(family, compact, inventory, invariants,
                         0, 0, word=changed_class_word),
        {"T_quotient_not_uniquely_isomorphic", "transport_classification",
         "nonrigid_direct_isomorphism"}))

    results.append(expect_rejection(
        "break_T_coherence",
        lambda: replay_q_under_first_T(
            family, compact, inventory, invariants, force_bad_parent=True),
        {"incoherent_child_transport"}))

    # A relation-local mutation of the row content address must not be hidden
    # by recomputing only the enclosing gzip hash.
    altered_record = deepcopy(compact["paths"][0])
    altered_record["fixed_full_root_case_id"] = "0" * 64
    results.append(expect_rejection(
        "alter_path_provenance",
        lambda: gate.require(
            all(altered_record[key] == inventory[0][key]
                for key in ("base_state_id", "base_path_binding_id",
                            "fixed_full_root_case_id")),
            "path_inventory_binding"), {"path_inventory_binding"}))

    gate.require(len(results) == 9 and all(row["rejected"] for row in results),
                 "mutation_suite_incomplete")
    payload = {
        "schema": "compact-probe-clean-clone-mutations-v1",
        "status": "VERIFIED",
        "outer_hashes_bypassed": True,
        "mutations": results,
    }
    output = HERE / "certificates" / "mutation_tests.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": "VERIFIED", "mutations": len(results),
                      "output": gate.normalized(output),
                      "output_sha256": gate.file_sha256(output)},
                     sort_keys=True))


if __name__ == "__main__":
    main()
