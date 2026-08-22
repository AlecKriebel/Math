#!/usr/bin/env python3
"""Independent structural and cross-package audit of the coherent-probe certificate."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEFAULT_CERTIFICATE = PROJECT / "work/probe_coherence_closure/probe_certificate.json"
CYCLE = PROJECT / "work/cycle_three_port_closure/artifacts"
THETA2 = PROJECT / "work/theta2_five_port_closure/artifacts"
RAW4 = PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
ATLAS = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"


class StructuralFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise StructuralFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path):
    return json.loads(path.read_text())


def status_by_origin(rows):
    answer = collections.Counter()
    for key, value in rows.items():
        origin, status = key.rsplit(":", 1)
        answer[(origin, status)] += value
    return answer


def check_transport(row, parent, prefix):
    require(row["transport_restriction"] == "exact_on_all_parent_mixed_vertices", f"{prefix}: restriction marker")
    require(sha(row["transport"]) == row["transport_sha256"], f"{prefix}: transport hash")
    require(row["parent_transport_sha256"] == parent["transport_sha256"], f"{prefix}: parent transport")
    require(row["global_triangle"] == parent.get("global_triangle"), f"{prefix}: global triangle drift")
    if row["status"] == "triangle":
        triangle = row["global_triangle"]
        require(triangle is not None, f"{prefix}: triangle lost global witness")
        require(row["transport"]["source_triangle_edges"] == triangle["source_triangle_edges"], f"{prefix}: source triangle reassigned")
        require(row["transport"]["target_triangle_edges"] == triangle["target_triangle_edges"], f"{prefix}: target triangle reassigned")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = load(args.certificate)
    committed = certificate.pop("payload_sha256")
    require(sha(certificate) == committed, "probe payload hash")
    certificate["payload_sha256"] = committed
    require(certificate["schema"] == "k2p-complete-coherent-probe-closure-v1", "probe schema")
    require(certificate["status"] == "PASS", "probe status")
    require(certificate["unresolved"] == certificate["incoherent"] == 0, "probe unresolved/incoherent")

    inputs = certificate["inputs"]
    require(inputs["atlas_sha256"] == sha_file(ATLAS), "atlas binding")
    require(inputs["raw_four_port_ledger_sha256"] == sha_file(RAW4), "raw four-port binding")
    require(inputs["theta2_class_partition_sha256"] == sha_file(THETA2 / "class_partition.json.gz"), "theta2 class binding")
    require(inputs["theta2_summary_sha256"] == sha_file(THETA2 / "theta2_five_port_summary.json"), "theta2 summary binding")
    require(inputs["cycle_three_port_summary_sha256"] == sha_file(CYCLE / "cycle_three_port_summary.json"), "cycle summary binding")
    require(inputs["cycle_quadratic_certificates_sha256"] == sha_file(CYCLE / "quadratic_certificates.json"), "cycle quadratic binding")
    require(inputs["cycle_physical_anchors_sha256"] == sha_file(CYCLE / "physical_anchors.json"), "cycle anchor binding")
    require(inputs["cycle_full_completion_ledger_sha256"] == sha_file(CYCLE / "full_completion_ledger.jsonl.gz"), "cycle full-ledger binding")

    four = certificate["four_port_terminal_inventory"]
    require(four["terminal_class_statuses"] == {"isomorphic": 20, "triangle": 35}, "four-port terminal classes")
    require(four["terminal_member_roots"] == 80, "four-port member roots")
    require(four["omitted_member_roots"] == 54, "four-port omitted roots")
    require(four["omitted_first_child_raw"] == len(four["omitted_first_child_hashes"]) == 532, "four-port first children")
    require(four["omitted_first_child_counts"] == {"displayed_quartet_mismatch": 456, "isomorphic": 13, "strict_tree_sunlet": 63}, "four-port child partition")

    theta = certificate["theta2_terminal_inventory"]
    require(theta["selected_iso_canonical_classes"] == 32 and theta["selected_iso_raw_roots"] == 80, "theta2 selected roots")
    require(theta["selected_root_dummy_profile"] == {"0": 24, "1": 40, "2": 16}, "theta2 dummy profile")
    require(theta["first_restoration_raw"] == len(theta["first_restoration_ordered_hashes"]) == 576, "theta2 first layer")
    require(theta["first_restoration_counts"] == {"displayed_quartet_mismatch": 504, "isomorphic": 72}, "theta2 first partition")
    require(theta["second_restoration_raw"] == len(theta["second_restoration_ordered_hashes"]) == 288, "theta2 second layer")
    require(theta["second_restoration_counts"] == {"displayed_quartet_mismatch": 256, "isomorphic": 32}, "theta2 second partition")
    require(theta["physical_raw_anchors"] == 96, "theta2 physical anchors")

    cycle = certificate["cycle_terminal_inventory"]
    require(cycle["raw_initial_relations"] == len(cycle["initial_ordered_raw_hashes"]) == 13440, "cycle base raw")
    require(cycle["initial_ordered_raw_hash_root"] == sha(cycle["initial_ordered_raw_hashes"]), "cycle base hash root")
    require(cycle["initial_counts"] == {"dummy_equal_topology": 5964, "isomorphic": 8, "strict_tree_sunlet": 7452, "triangle": 16}, "cycle base partition")
    require(cycle["dummy_root_profile"] == {"1": 324, "2": 1896, "3": 2784, "4": 960}, "cycle root profile")
    expected_depths = [
        (5964, 48924, {"displayed_quartet_mismatch": 36840, "equal_topology_continuation": 4968, "isomorphic": 12, "physical_equal_topology_nonterminal": 132, "strict_tree_sunlet": 6972}),
        (4968, 38560, {"displayed_quartet_mismatch": 34968, "equal_topology_continuation": 3160, "strict_tree_sunlet": 432}),
        (3160, 24440, {"displayed_quartet_mismatch": 22520, "equal_topology_continuation": 1728, "strict_tree_sunlet": 192}),
        (1728, 10368, {"displayed_quartet_mismatch": 10368}),
    ]
    require(len(cycle["restoration_depths"]) == 4 and cycle["restoration_terminates"], "cycle restoration termination")
    for row, (parents, raw, counts) in zip(cycle["restoration_depths"], expected_depths):
        require((row["parents"], row["raw_children"], row["counts"]) == (parents, raw, counts), f"cycle depth {row['depth']} census")
        require(len(row["ordered_raw_hashes"]) == raw and sha(row["ordered_raw_hashes"]) == row["ordered_raw_hash_root"], f"cycle depth {row['depth']} hash root")
    require(cycle["restoration_edges"] == sum(row[1] for row in expected_depths), "cycle restoration edge total")
    require((cycle["physical_anchor_presentations"], cycle["direct_physical_anchors"], cycle["restored_physical_anchors"]) == (36, 24, 12), "cycle physical anchors")
    require(cycle["physical_equal_topology_quadratic_raw"] == 132, "cycle quadratic raw")
    raw_bindings = cycle["physical_equal_topology_raw_bindings"]
    require(len(raw_bindings) == len(cycle["physical_equal_topology_raw_binding_hashes"]) == 132, "cycle raw algebra bindings")
    require([sha(row) for row in raw_bindings] == cycle["physical_equal_topology_raw_binding_hashes"], "cycle raw binding hashes")
    graph_classes = {row["semi_directed_graph_pair_class_id"] for row in raw_bindings}
    descriptor_classes = {row["descriptor_pair_class_id"] for row in raw_bindings}
    require(graph_classes == set(range(30)), "cycle semi-directed class coverage")
    require(descriptor_classes == set(range(54)), "cycle descriptor class coverage")
    algebra = cycle["physical_equal_topology_descriptor_pair_classes"]
    require(len(algebra) == cycle["quadratic_classes"] == 54 and cycle["quadratic_unresolved"] == 0, "cycle quadratic class census")
    multiplicities = collections.Counter(row["raw_multiplicity"] for row in algebra)
    require(multiplicities == collections.Counter({2: 42, 4: 12}), "cycle quadratic multiplicities")
    require(collections.Counter(row["descriptor_pair_class_id"] for row in raw_bindings) == collections.Counter({row["descriptor_pair_class_id"]: row["raw_multiplicity"] for row in algebra}), "cycle raw-to-class assignment")
    released = load(CYCLE / "quadratic_certificates.json")
    released_set = {
        (row["source_descriptor_sha256"], row["target_descriptor_sha256"], row["source_pullback_sha256"], released["raw_multiplicity"][identifier])
        for identifier, row in released["certificates"].items()
    }
    independent_set = {
        (row["source_descriptor_sha256"], row["target_descriptor_sha256"], row["certificate"]["source_pullback_sha256"], row["raw_multiplicity"])
        for row in algebra
    }
    require(independent_set == released_set, "cycle released 54-class cross-binding")

    tree = certificate["three_port_terminal_inventory"]
    require(tree["tree"] == 1 and tree["internal_component_arcs"] == 0, "ordinary tree root")

    anchors = certificate["anchors"]
    records = anchors["records"]
    require(anchors["raw_total"] == len(records) == 172, "all-primitive anchor census")
    expected_origins = {
        "direct_no_dummy": 26,
        "omitted_terminal_first_child": 13,
        "theta2_physical_five_port": 24,
        "theta2_restored_six_port": 40,
        "theta2_restored_seven_port": 32,
        "cycle_physical_three_port": 24,
        "cycle_restored_four_port": 12,
        "three_port_tree": 1,
    }
    require(anchors["raw_by_origin"] == expected_origins, "anchor origins")
    by_id = {row["anchor_id"]: row for row in records}
    require(len(by_id) == len(records), "duplicate anchor id")
    expected_candidate_counts = {
        "direct_no_dummy": (7, 7),
        "omitted_terminal_first_child": (8, 8),
        "theta2_physical_five_port": (8, 8),
        "theta2_restored_six_port": (9, 9),
        "theta2_restored_seven_port": (10, 10),
        "cycle_physical_three_port": (3, 3),
        "cycle_restored_four_port": (4, 4),
        "three_port_tree": (0, 0),
    }
    for row in records:
        require(sha(row["transport"]) == row["transport_sha256"], f"anchor transport hash:{row['anchor_id']}")
        require((len(row["source_internal_candidates"]), len(row["target_internal_candidates"])) == expected_candidate_counts[row["origin"]], f"anchor candidate count:{row['anchor_id']}")
        require(row["status"] in {"isomorphic", "triangle"}, f"anchor status:{row['anchor_id']}")
        if row["status"] == "triangle":
            require(row["global_triangle"] is not None, f"anchor triangle witness:{row['anchor_id']}")
    coverage = anchors["canonical_raw_coverage"]
    require(set(map(int, coverage)) == set(range(anchors["canonical_total"])), "canonical anchor id interval")
    require(
        collections.Counter(item for values in coverage.values() for item in values)
        == collections.Counter(by_id.keys()),
        "canonical anchor raw coverage",
    )
    for row in records:
        require(row["anchor_id"] in coverage[str(row["canonical_anchor_id"])], "anchor canonical assignment")

    one = certificate["one_port"]
    theoretical_one = sum(len(row["source_internal_candidates"]) * len(row["target_internal_candidates"]) for row in records)
    require(one["raw_relations"] == len(one["ordered_raw_hashes"]) == theoretical_one, "A+p raw census")
    require(sha(one["ordered_raw_hashes"]) == one["ordered_raw_hash_root"], "A+p hash root")
    require(sum(one["status_counts"].values()) == one["raw_relations"], "A+p status partition")
    require(set(one["status_counts"]) <= {"displayed_quartet_mismatch", "strict_tree_sunlet", "isomorphic", "triangle"}, "A+p status universe")
    one_by_origin = status_by_origin(one["status_by_origin"])
    for origin in expected_origins:
        observed = sum(value for (item, _), value in one_by_origin.items() if item == origin)
        expected = sum(len(row["source_internal_candidates"]) * len(row["target_internal_candidates"]) for row in records if row["origin"] == origin)
        require(observed == expected, f"A+p origin coverage:{origin}")
    one_survivors = one["survivors"]
    require(one["terminal_survivors"] == len(one_survivors) == one["status_counts"].get("isomorphic", 0) + one["status_counts"].get("triangle", 0), "A+p terminals")
    one_by_id = {row["relation_id"]: row for row in one_survivors}
    require(len(one_by_id) == len(one_survivors), "duplicate A+p relation id")
    for row in one_survivors:
        parent = by_id[row["parent_id"]]
        require(row["stage"] == "A+p" and row["origin"] == parent["origin"], f"A+p parent/origin:{row['relation_id']}")
        require(0 <= row["source_insertion_index"] < len(parent["source_internal_candidates"]), f"A+p source index:{row['relation_id']}")
        require(0 <= row["target_insertion_index"] < len(parent["target_internal_candidates"]), f"A+p target index:{row['relation_id']}")
        require(row["relation_id"] == f"A+p:{row['parent_id']}:{row['source_insertion_index']}:{row['target_insertion_index']}", f"A+p relation id content:{row['relation_id']}")
        check_transport(row, parent, f"A+p:{row['relation_id']}")

    two = certificate["two_port"]
    require(two["parent_relations"] == len(one_survivors), "A+p+q parent census")
    theoretical_two = sum(
        (len(by_id[row["parent_id"]]["source_internal_candidates"]) + 1)
        * (len(by_id[row["parent_id"]]["target_internal_candidates"]) + 1)
        for row in one_survivors
    )
    require(two["raw_relations"] == len(two["ordered_raw_hashes"]) == theoretical_two, "A+p+q raw census")
    require(sha(two["ordered_raw_hashes"]) == two["ordered_raw_hash_root"], "A+p+q hash root")
    require(sum(two["status_counts"].values()) == two["raw_relations"], "A+p+q status partition")
    require(set(two["status_counts"]) <= {"displayed_quartet_mismatch", "strict_tree_sunlet", "isomorphic", "triangle"}, "A+p+q status universe")
    two_by_origin = status_by_origin(two["status_by_origin"])
    for origin in expected_origins:
        observed = sum(value for (item, _), value in two_by_origin.items() if item == origin)
        expected = sum(
            (len(by_id[row["parent_id"]]["source_internal_candidates"]) + 1)
            * (len(by_id[row["parent_id"]]["target_internal_candidates"]) + 1)
            for row in one_survivors if row["origin"] == origin
        )
        require(observed == expected, f"A+p+q origin coverage:{origin}")
    two_survivors = two["survivors"]
    require(two["terminal_survivors"] == len(two_survivors) == two["status_counts"].get("isomorphic", 0) + two["status_counts"].get("triangle", 0), "A+p+q terminals")
    require(len({row["relation_id"] for row in two_survivors}) == len(two_survivors), "duplicate A+p+q relation id")
    for row in two_survivors:
        parent = one_by_id[row["parent_id"]]
        grandparent = by_id[row["grandparent_id"]]
        require(row["stage"] == "A+p+q" and row["origin"] == parent["origin"] == grandparent["origin"], f"A+p+q ancestry:{row['relation_id']}")
        require(parent["parent_id"] == row["grandparent_id"], f"A+p+q grandparent:{row['relation_id']}")
        require(row["parent_source_insertion_index"] == parent["source_insertion_index"] and row["parent_target_insertion_index"] == parent["target_insertion_index"], f"A+p+q parent placement:{row['relation_id']}")
        require(0 <= row["source_insertion_index"] < len(grandparent["source_internal_candidates"]) + 1, f"A+p+q source index:{row['relation_id']}")
        require(0 <= row["target_insertion_index"] < len(grandparent["target_internal_candidates"]) + 1, f"A+p+q target index:{row['relation_id']}")
        expected_id = f"A+p+q:{row['parent_id']}:{row['source_insertion_index']}:{row['target_insertion_index']}"
        require(row["relation_id"] == expected_id, f"A+p+q relation id content:{row['relation_id']}")
        check_transport(row, parent, f"A+p+q:{row['relation_id']}")

    reviewed = certificate["reviewed_39_anchor_regression"]
    require(reviewed == {
        "one_port_raw": 2106,
        "one_port": {"displayed_quartet_mismatch": 1820, "isomorphic": 159, "strict_tree_sunlet": 115, "triangle": 12},
        "two_port_raw": 12406,
        "two_port": {"displayed_quartet_mismatch": 10952, "isomorphic": 1224, "strict_tree_sunlet": 170, "triangle": 60},
    }, "reviewed 39-anchor regression")
    coherence = certificate["coherence"]
    require(coherence["anchor_transport_multiplicity"] == coherence["survivor_transport_multiplicity"] == 1, "transport multiplicity claim")
    require(coherence["every_survivor_restricts_parent"] is True, "parent transport claim")
    require(certificate["algebra_fallback"]["invoked"] == certificate["algebra_fallback"]["exact_descriptor_pair_certificate_classes"] == 54, "algebra fallback class count")
    require(certificate["algebra_fallback"]["semi_directed_graph_pair_crosswalk_classes"] == 30, "algebra graph-pair crosswalk")
    require(certificate["algebra_fallback"]["raw_relations"] == 132, "algebra fallback raw count")
    optimization = certificate["optimization_adversarial_regression"]
    require(optimization["unsafe_reviewed_39_A_plus_p"] == {"displayed_quartet_mismatch": 1820, "isomorphic": 195, "strict_tree_sunlet": 63, "triangle": 28}, "unsafe-cache mutation census")
    require(optimization["correct_reviewed_39_A_plus_p"] == reviewed["one_port"], "correct-cache regression binding")

    report = {
        "schema": "k2p-coherent-probe-structural-adversarial-replay-v1",
        "status": "PASS",
        "probe_payload_sha256": committed,
        "raw_anchors": len(records),
        "canonical_anchors": anchors["canonical_total"],
        "one_port_raw": one["raw_relations"],
        "one_port_survivors": len(one_survivors),
        "two_port_raw": two["raw_relations"],
        "two_port_survivors": len(two_survivors),
        "cycle_descriptor_classes": len(algebra),
        "unresolved": 0,
        "incoherent": 0,
    }
    report["payload_sha256"] = sha(report)
    if args.output:
        args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (StructuralFailure, KeyError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PROBE_STRUCTURAL_REPLAY_FAIL:{exc}") from exc
