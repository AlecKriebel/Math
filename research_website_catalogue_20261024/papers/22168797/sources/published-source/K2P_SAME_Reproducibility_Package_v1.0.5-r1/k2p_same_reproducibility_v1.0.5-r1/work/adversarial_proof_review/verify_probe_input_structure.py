#!/usr/bin/env python3
"""Fast fail-closed structural verifier for probe-input mutation testing."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_CONTRACT = HERE / "probe_input_contract.json"


class Failure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


def sha(value):
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def validate(contract):
    require(set(contract) == {
        "schema", "status", "claim_boundary", "inputs", "anchor_census",
        "candidate_census", "root_movement_contract", "required_probe_classifier_order",
        "forbidden_probe_shortcuts", "anchors", "ordered_anchor_row_hashes",
        "ordered_anchor_hash_root", "unresolved_anchor_inputs",
        "incoherent_site_transports", "payload_sha256",
    }, "top-level fields")
    require(contract.get("schema") == "k2p-root-invariant-probe-input-contract-v2", "schema")
    require(contract.get("status") == "PASS", "status")
    require(contract.get("payload_sha256") == sha({
        key: value for key, value in contract.items() if key != "payload_sha256"
    }), "payload")
    inputs = contract.get("inputs", {})
    require(set(inputs) == {
        "atlas_sha256", "raw4_ledger_sha256", "theta2_fixed_full_closure_sha256",
        "cycle_physical_anchors_sha256", "cycle_full_ledger_sha256",
        "cycle_promotion_certificate_sha256", "cycle_common_sha256",
        "cycle_generator_sha256",
    }, "input keys")
    require(all(isinstance(value, str) and len(value) == 64 for value in inputs.values()), "input hashes")
    anchors = contract.get("anchors", [])
    require(len(anchors) == 176, "anchor count")
    ids = [row.get("anchor_id") for row in anchors]
    require(len(set(ids)) == 176, "anchor ids")
    hashes = [row.get("anchor_row_sha256") for row in anchors]
    require(hashes == contract.get("ordered_anchor_row_hashes"), "row hash order")
    require(contract.get("ordered_anchor_hash_root") == sha(hashes), "anchor hash root")
    origins, relations, ports = collections.Counter(), collections.Counter(), collections.Counter()
    site_sums, site_types = collections.Counter(), collections.Counter()
    regression = {}
    for row in anchors:
        anchor_id = row["anchor_id"]
        require(row["anchor_row_sha256"] == sha({
            key: value for key, value in row.items() if key != "anchor_row_sha256"
        }), f"row hash:{anchor_id}")
        require(row["relation"] in {"isomorphic", "triangle"}, f"relation:{anchor_id}")
        require(row["parent_transport"].get("relation") == row["relation"], f"parent relation:{anchor_id}")
        parent = row["parent_transport"]
        require(parent.get("transport_sha256") == sha({
            key: value for key, value in parent.items() if key != "transport_sha256"
        }), f"parent hash:{anchor_id}")
        labels = row.get("labels", [])
        require(labels == list(range(len(labels))) and 3 <= len(labels) <= 7, f"labels:{anchor_id}")
        origins[row["origin"]] += 1
        relations[row["relation"]] += 1
        ports[len(labels)] += 1
        profiles = {}
        for side in ("source", "target"):
            profile = row[f"{side}_candidate_profile"]
            sites = profile.get("sites", [])
            require(profile.get("all_mixed_edge_sites_included") is True, f"all sites:{anchor_id}:{side}")
            require(profile.get("site_count") == len(sites), f"site count:{anchor_id}:{side}")
            k, r = profile.get("port_count"), profile.get("reticulation_count")
            require(k == len(labels), f"profile ports:{anchor_id}:{side}")
            require(len(sites) == 2 * k + 3 * r - 3, f"site formula:{anchor_id}:{side}")
            require(profile.get("ordered_site_hash_root") == sha([sha(site) for site in sites]),
                    f"site root:{anchor_id}:{side}")
            ids_here = [site.get("site_id") for site in sites]
            require(len(set(ids_here)) == len(ids_here), f"site ids:{anchor_id}:{side}")
            counts = collections.Counter(site.get("site_type") for site in sites)
            require(profile.get("site_type_census") == dict(sorted(counts.items())),
                    f"site type census:{anchor_id}:{side}")
            require(counts["core_unheaded"] == len(sites) - (k - 1) - 2 * r - 1,
                    f"core site formula:{anchor_id}:{side}:{counts}")
            require(counts["pendant_arm"] == k - 1,
                    f"pendant site formula:{anchor_id}:{side}:{counts}")
            require(counts["reticulation_incoming"] == 2 * r,
                    f"retic site formula:{anchor_id}:{side}:{counts}")
            require(counts["root_suppressed_segment"] == 1,
                    f"root site formula:{anchor_id}:{side}:{counts}")
            for site in sites:
                require(site["site_type"] in counts, f"site type:{anchor_id}:{side}")
                require(len(site.get("mixed_endpoints", [])) == 2, f"endpoints:{anchor_id}:{side}")
                require(site["site_id"] == f"E:{sha(site['mixed_endpoints'])}",
                        f"site id hash:{anchor_id}:{side}")
                representatives = site.get("rooted_representatives", [])
                require(len(representatives) == (
                    2 if site["site_type"] == "root_suppressed_segment" else 1
                ), f"rooted representatives:{anchor_id}:{side}")
            half = profile.get("root_half_equivalence", {})
            require(half.get("semi_directed_relation_after_insertion") == "isomorphic",
                    f"half relation:{anchor_id}:{side}")
            require(len(half.get("representative_half_arcs", [])) == 2,
                    f"half arcs:{anchor_id}:{side}")
            require(half.get("certificate_sha256") == sha({
                key: value for key, value in half.items() if key != "certificate_sha256"
            }), f"half hash:{anchor_id}:{side}")
            profiles[side] = {tuple(site["mixed_endpoints"]): site for site in sites}
            site_sums[side] += len(sites)
            site_types.update({f"{side}:{key}": value for key, value in counts.items()})
        edge_map = parent.get("mixed_edge_map", [])
        require(len(edge_map) == len(profiles["source"]) == len(profiles["target"]),
                f"parent edge coverage:{anchor_id}")
        expected_pairs = set()
        for source_edge, target_edge in edge_map:
            require(tuple(source_edge) in profiles["source"], f"source parent edge:{anchor_id}")
            require(tuple(target_edge) in profiles["target"], f"target parent edge:{anchor_id}")
            expected_pairs.add((
                profiles["source"][tuple(source_edge)]["site_id"],
                profiles["target"][tuple(target_edge)]["site_id"],
            ))
        site_transport = row.get("site_transport", [])
        require(row.get("site_transport_sha256") == sha(site_transport), f"site transport hash:{anchor_id}")
        actual_pairs = {(item["source_site_id"], item["target_site_id"]) for item in site_transport}
        require(actual_pairs == expected_pairs and len(site_transport) == len(expected_pairs),
                f"site transport mapping:{anchor_id}")
        raw_id = row.get("locator", {}).get("raw_id")
        if raw_id in {67161, 67167, 67401, 67407}:
            regression[raw_id] = (row["origin"], row["relation"])
    require(origins == {
        "four_port_direct_physical": 26, "four_port_restored_physical_k5": 17,
        "theta2_physical_k5": 24, "theta2_physical_k6": 40, "theta2_physical_k7": 32,
        "cycle_physical_k3": 24, "cycle_restored_physical_k4": 12,
        "tree_physical_k3": 1,
    }, f"origins:{origins}")
    require(relations == {"isomorphic": 143, "triangle": 33}, f"relations:{relations}")
    require(ports == {3: 25, 4: 38, 5: 41, 6: 40, 7: 32}, f"ports:{ports}")
    require(site_sums == {"source": 2206, "target": 2206}, f"site sums:{site_sums}")
    require(regression == {
        67161: ("four_port_restored_physical_k5", "triangle"),
        67167: ("four_port_restored_physical_k5", "triangle"),
        67401: ("four_port_restored_physical_k5", "triangle"),
        67407: ("four_port_restored_physical_k5", "triangle"),
    }, f"regression rows:{regression}")
    census = contract.get("anchor_census", {})
    require(census.get("physical_equality_anchor_records") == 176, "reported anchors")
    require(census.get("unique_anchor_record_ids") == 176, "reported unique anchors")
    require(census.get("four_port", {}).get("restored_physical_equalities") == 17,
            "reported four restored")
    require(census.get("four_port", {}).get("restoration_children_exact_tested") == 564,
            "reported four children")
    candidates = contract.get("candidate_census", {})
    require(candidates.get("source_sites") == 2206 and candidates.get("target_sites") == 2206,
            "reported sites")
    require(candidates.get("first_probe_source_target_pairs") == 29964,
            "reported first probe pairs")
    require(candidates.get("reticulation_incoming_edges_included") is True, "reported retic")
    require(candidates.get("pendant_arm_edges_included") is True, "reported pendants")
    require(candidates.get("artificial_root_two_halves_quotiented") is True, "reported root")
    require(candidates.get("per_graph_formula") == "site_count = 2*k + 3*r - 3", "reported formula")
    require(contract.get("required_probe_classifier_order") == [
        "exact_labelled_isomorphism_or_ordinary_triangle_relation",
        "displayed_quartet_set_strict_separator",
        "direct_full_map_Ti_search_over_every_triple_and_orientation",
        "certified_multihomogeneous_algebra_fallback_or_unresolved",
    ], "classifier order")
    forbidden = set(contract.get("forbidden_probe_shortcuts", []))
    require({
        "rooted_restriction_type_as_proof", "triple_type_gate_before_full_map_Ti_search",
        "dropping_root-tail_arcs_without_half-quotient", "dropping_pendant_arms",
        "dropping_reticulation-incoming_arcs", "accepting_transport_not_restricting_parent",
    } == forbidden, "forbidden shortcuts")
    require(contract.get("unresolved_anchor_inputs") == 0, "unresolved")
    require(contract.get("incoherent_site_transports") == 0, "incoherent")
    return {
        "anchors": len(anchors), "source_sites": site_sums["source"],
        "target_sites": site_sums["target"], "regression_rows": sorted(regression),
    }


def main():
    if not __debug__:
        raise SystemExit("PROBE_INPUT_STRUCTURE_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    result = validate(json.loads(args.contract.read_text()))
    if not args.quiet:
        print(json.dumps({"status": "PASS", **result}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (Failure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PROBE_INPUT_STRUCTURE_FAIL:{exc}") from exc
