#!/usr/bin/env python3
"""Adversarial mutations for the physical probe-input contract."""

from __future__ import annotations

import collections
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
CONTRACT = HERE / "probe_input_contract.json"
STRUCTURE = HERE / "verify_probe_input_structure.py"
FULL = HERE / "verify_probe_input_contract.py"
OUTPUT = HERE / "probe_input_mutation_certificate.json"


def sha(value):
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def reseal_profile(profile):
    sites = profile["sites"]
    profile["site_count"] = len(sites)
    profile["site_type_census"] = dict(sorted(collections.Counter(
        row["site_type"] for row in sites
    ).items()))
    profile["ordered_site_hash_root"] = sha([sha(row) for row in sites])
    half = profile["root_half_equivalence"]
    half["certificate_sha256"] = sha({
        key: value for key, value in half.items() if key != "certificate_sha256"
    })


def reseal_anchor(anchor):
    reseal_profile(anchor["source_candidate_profile"])
    reseal_profile(anchor["target_candidate_profile"])
    parent = anchor["parent_transport"]
    parent["transport_sha256"] = sha({
        key: value for key, value in parent.items() if key != "transport_sha256"
    })
    anchor["site_transport_sha256"] = sha(anchor["site_transport"])
    anchor["anchor_row_sha256"] = sha({
        key: value for key, value in anchor.items() if key != "anchor_row_sha256"
    })


def reseal(contract):
    for anchor in contract["anchors"]:
        reseal_anchor(anchor)
    hashes = [row["anchor_row_sha256"] for row in contract["anchors"]]
    contract["ordered_anchor_row_hashes"] = hashes
    contract["ordered_anchor_hash_root"] = sha(hashes)
    contract["payload_sha256"] = sha({
        key: value for key, value in contract.items() if key != "payload_sha256"
    })


def anchor_with_site(contract, site_type):
    return next(row for row in contract["anchors"] if any(
        site["site_type"] == site_type for site in row["source_candidate_profile"]["sites"]
    ))


def mutate_omit_anchor(contract):
    contract["anchors"].pop()


def mutate_old_172(contract):
    bad = {67161, 67167, 67401, 67407}
    contract["anchors"] = [
        row for row in contract["anchors"] if row.get("locator", {}).get("raw_id") not in bad
    ]


def mutate_duplicate_new_triangle(contract):
    index = next(i for i, row in enumerate(contract["anchors"])
                 if row.get("locator", {}).get("raw_id") == 67161)
    contract["anchors"][index] = copy.deepcopy(contract["anchors"][index + 1])


def mutate_reassign_67161(contract):
    row = next(row for row in contract["anchors"] if row.get("locator", {}).get("raw_id") == 67161)
    row["locator"]["raw_id"] = 67162


def mutate_collapse_k7_path_ids(contract):
    groups = collections.defaultdict(list)
    for row in contract["anchors"]:
        if row["origin"] == "theta2_physical_k7":
            groups[row["locator"]["upstream_anchor_id"]].append(row)
    pair = next(rows for rows in groups.values() if len(rows) == 2)
    pair[1]["anchor_id"] = pair[0]["anchor_id"]


def drop_site(contract, site_type):
    anchor = anchor_with_site(contract, site_type)
    profile = anchor["source_candidate_profile"]
    removed = next(site for site in profile["sites"] if site["site_type"] == site_type)
    profile["sites"].remove(removed)
    anchor["site_transport"] = [
        row for row in anchor["site_transport"] if row["source_site_id"] != removed["site_id"]
    ]


def mutate_drop_pendant(contract):
    drop_site(contract, "pendant_arm")


def mutate_drop_retic(contract):
    drop_site(contract, "reticulation_incoming")


def mutate_drop_root(contract):
    drop_site(contract, "root_suppressed_segment")


def mutate_split_root(contract):
    anchor = anchor_with_site(contract, "root_suppressed_segment")
    profile = anchor["source_candidate_profile"]
    site = copy.deepcopy(next(row for row in profile["sites"]
                              if row["site_type"] == "root_suppressed_segment"))
    site["mixed_endpoints"] = [site["mixed_endpoints"][0], "('artificial_split_half',)"]
    site["site_id"] = f"E:{sha(site['mixed_endpoints'])}"
    site["rooted_representatives"] = [site["rooted_representatives"][0]]
    site["site_type"] = "core_unheaded"
    profile["sites"].append(site)


def mutate_wrong_half(contract):
    anchor = contract["anchors"][0]
    anchor["source_candidate_profile"]["root_half_equivalence"][
        "semi_directed_relation_after_insertion"
    ] = "none"


def mutate_wrong_site_transport(contract):
    anchor = next(row for row in contract["anchors"] if len(row["site_transport"]) >= 2)
    anchor["site_transport"][0]["target_site_id"], anchor["site_transport"][1]["target_site_id"] = (
        anchor["site_transport"][1]["target_site_id"],
        anchor["site_transport"][0]["target_site_id"],
    )


def mutate_corrupt_parent_transport(contract):
    anchor = next(row for row in contract["anchors"]
                  if len(row["parent_transport"]["mixed_edge_map"]) >= 2)
    edge_map = anchor["parent_transport"]["mixed_edge_map"]
    edge_map[0][1], edge_map[1][1] = edge_map[1][1], edge_map[0][1]


def mutate_formula(contract):
    contract["candidate_census"]["per_graph_formula"] = "site_count = 2*k + 3*r - 4"


def mutate_topology_first(contract):
    order = contract["required_probe_classifier_order"]
    order.insert(0, "rooted_restriction_type_as_terminal_separator")


def mutate_triple_gate(contract):
    order = contract["required_probe_classifier_order"]
    order[2] = "triple_type_gate_then_selected_Ti_search"


def mutate_remove_forbidden(contract):
    contract["forbidden_probe_shortcuts"].remove("rooted_restriction_type_as_proof")


def mutate_raw4424_reintroduced(contract):
    contract["revoked_raw4424_tree_sunlet_terminal"] = True


def mutate_generic_rooted_reintroduced(contract):
    contract["rooted_restriction_classifier_enabled"] = True


def mutate_row_hash_omission(contract):
    contract["ordered_anchor_row_hashes"].pop()
    contract["ordered_anchor_hash_root"] = sha(contract["ordered_anchor_row_hashes"])


def mutate_input_binding(contract):
    contract["inputs"]["atlas_sha256"] = "0" * 64


MUTATIONS = [
    ("omitted_anchor_record", mutate_omit_anchor, "structure"),
    ("old_172_anchor_count_reintroduction", mutate_old_172, "structure"),
    ("duplicate_replacing_new_triangle_anchor", mutate_duplicate_new_triangle, "structure"),
    ("raw67161_locator_reassignment", mutate_reassign_67161, "structure"),
    ("collapse_two_k7_path_ids_sharing_topology_id", mutate_collapse_k7_path_ids, "structure"),
    ("omitted_pendant_arm", mutate_drop_pendant, "structure"),
    ("omitted_reticulation_incoming", mutate_drop_retic, "structure"),
    ("dropped_root_suppressed_segment", mutate_drop_root, "structure"),
    ("split_artificial_root_halves", mutate_split_root, "structure"),
    ("wrong_root_half_equivalence", mutate_wrong_half, "structure"),
    ("wrong_site_transport", mutate_wrong_site_transport, "structure"),
    ("corrupt_anchor_parent_transport", mutate_corrupt_parent_transport, "structure"),
    ("wrong_site_formula", mutate_formula, "structure"),
    ("topology_first_classifier_reintroduction", mutate_topology_first, "structure"),
    ("triple_type_gate_reintroduction", mutate_triple_gate, "structure"),
    ("forbidden_rooted_restriction_removed", mutate_remove_forbidden, "structure"),
    ("raw4424_false_tree_sunlet_reintroduction", mutate_raw4424_reintroduced, "structure"),
    ("generic_rooted_restriction_reintroduction", mutate_generic_rooted_reintroduced, "structure"),
    ("ordered_row_hash_omission", mutate_row_hash_omission, "structure-no-reseal"),
    ("upstream_input_binding_corruption", mutate_input_binding, "full"),
]


def run_verifier(path, kind, optimized=False):
    script = FULL if kind == "full" else STRUCTURE
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([str(script), "--contract", str(path)])
    if kind != "full":
        command.append("--quiet")
    return subprocess.run(command, capture_output=True, text=True)


def main():
    original = json.loads(CONTRACT.read_text())
    rows = []
    with tempfile.TemporaryDirectory(prefix="k2p_probe_mutations_") as temporary:
        temporary = Path(temporary)
        for index, (name, function, kind) in enumerate(MUTATIONS):
            value = copy.deepcopy(original)
            function(value)
            if kind != "structure-no-reseal":
                reseal(value)
            else:
                value["payload_sha256"] = sha({
                    key: item for key, item in value.items() if key != "payload_sha256"
                })
            path = temporary / f"mutation_{index}.json"
            path.write_text(json.dumps(value, sort_keys=True))
            result = run_verifier(path, "full" if kind == "full" else "structure")
            rows.append({
                "mutation": name, "rejected": result.returncode != 0,
                "verifier": "independent_full" if kind == "full" else "fast_fail_closed_structure",
                "returncode": result.returncode,
                "diagnostic_sha256": hashlib.sha256((result.stdout + result.stderr).encode()).hexdigest(),
            })
        optimized = run_verifier(CONTRACT, "structure", optimized=True)
        rows.append({
            "mutation": "optimized_mode_original_contract",
            "rejected": False, "passed": optimized.returncode == 0,
            "verifier": "python_-O_fast_fail_closed_structure",
            "returncode": optimized.returncode,
            "diagnostic_sha256": hashlib.sha256((optimized.stdout + optimized.stderr).encode()).hexdigest(),
        })
    rejected = sum(row.get("rejected") is True for row in rows[:-1])
    passed = rejected == len(MUTATIONS) and rows[-1]["passed"]
    report = {
        "schema": "k2p-probe-input-mutation-certificate-v1",
        "status": "PASS" if passed else "FAIL",
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "contract_payload_sha256": original["payload_sha256"],
        "adversarial_mutations": len(MUTATIONS),
        "mutations_rejected": rejected,
        "mutation_survivors": len(MUTATIONS) - rejected,
        "optimized_mode_pass": rows[-1]["passed"],
        "results": rows,
    }
    report["payload_sha256"] = sha(report)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": report["status"], "rejected": rejected,
        "survivors": report["mutation_survivors"],
        "optimized": report["optimized_mode_pass"],
        "payload_sha256": report["payload_sha256"],
    }, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
