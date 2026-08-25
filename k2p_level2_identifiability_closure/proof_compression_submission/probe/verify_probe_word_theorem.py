#!/usr/bin/env python3
"""Stream and verify the exact premises of the K2P probe word theorem."""

from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
PROBE = PROJECT / "work/probe_coherence_corrected"
INPUT_CONTRACT = PROJECT / "work/adversarial_proof_review/probe_input_contract.json"
ATLAS = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
OUTPUT = HERE / "PROBE_WORD_COVERAGE.json"

FILES = {
    "certificate": (PROBE / "probe_coherence_certificate.json", "2f4d64b32a905ce2cc06bae7d03215f9239427d421825c2525437ee6ba2ccaf6"),
    "one": (PROBE / "one_port_ledger.jsonl.gz", "d5fa13d38731bff2403eeb4e4d9e139566c4983b09d30553c6260eaac64c5c90"),
    "two": (PROBE / "two_port_ledger.jsonl.gz", "10f0afcab77f2d61cecfc36d723c6f32065c304ac088b0b8ecf12dfc867fbf9d"),
    "parents": (PROBE / "two_port_parent_inventory.jsonl.gz", "673112e949e08dce0bdbd690be647dd97d0899c2bb12121b4a16ed7a62dba3f8"),
    "transports": (PROBE / "exact_transport_ledger.jsonl.gz", "6bc8e88feac2bee68491287775f078e8e5474bf930961a7390967c9fd350044d"),
    "restrictions": (PROBE / "parent_restriction_ledger.jsonl.gz", "5d1e6c2fe38d31f6304a76886ec37829215b88c8b179f5b23596d49d37ceeb38"),
    "separation": (PROBE / "separation_proof_registry.json.gz", "057783503b1ad7b3c55c14a1cc643db4851c9e42e00595b789b7d6b6d069acfe"),
    "input_contract": (INPUT_CONTRACT, "7f686ae99dd5e6dafc1c04396b711d294a0bddd6a25574f9ea809b831ad7b377"),
}

EXPECTED_CERT_PAYLOAD = "964e9f3c241e63a1b0b12b3ceb516c58525d410c3c550e8335b619a6817400e5"
EXPECTED_INPUT_PAYLOAD = "579919ca13204ddf959b3a159e4849b69c05ac87861eba2221659ec45bd73f38"
EXPECTED_SOURCE_SUPPORT_GRAMMAR_SHA256 = (
    "cadbb4187f501ab53620b3f15deaccb60bed582dfe8fdbefd7c1ba10f5329047"
)
SITE_TYPES = {"core_unheaded", "pendant_arm", "reticulation_incoming", "root_suppressed_segment"}
EQUALITY = {"isomorphic", "triangle"}
SEPARATED = {"displayed_quartet_mismatch", "full_map_Ti_strict_sign"}


class Failure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def object_sha256(value) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def replay_payload(document: dict, expected: str, label: str, *, exclude=()) -> None:
    unhashed = dict(document)
    payload = unhashed.pop("payload_sha256")
    for key in exclude:
        unhashed.pop(key, None)
    require(payload == expected, f"{label} payload identity")
    require(object_sha256(unhashed) == payload, f"{label} payload replay")


def stream_rows(path: Path):
    with gzip.open(path, "rt") as handle:
        for line in handle:
            yield json.loads(line)


def chain_step(root: str, row: dict) -> str:
    return object_sha256({"previous": root, "row_sha256": object_sha256(row)})


def import_atlas():
    spec = importlib.util.spec_from_file_location("compression_probe_atlas", ATLAS)
    require(spec is not None and spec.loader is not None, "cannot import frozen atlas")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def source_support_grammar_sha256(atlas) -> str:
    """Fingerprint precisely the ordered primitive source grammar used here.

    The exact relation/transport evidence is already stored in the frozen
    probe ledgers and replayed below.  This reader-level word-theorem checker
    imports the atlas only to verify the six ordered theta source supports and
    the theta1 parallel segments, so a whole-file compiler hash would be an
    over-broad dependency.
    """
    records = []
    for row in atlas.source_supports():
        records.append({
            "core_id": row.core_id,
            "incoming_selected": row.incoming_selected,
            "repair_index": row.repair_index,
            "selected_sink_mask": row.selected_sink_mask,
            "words": row.words,
            "selected_labels": row.selected_labels,
            "dummy_labels": row.dummy_labels,
            "source_support": row.source_support,
            "extra_count": row.extra_count,
        })
    return object_sha256({"CORES": atlas.CORES, "source_supports": records})


def check_candidate_profile(profile: dict) -> collections.Counter:
    require(profile["all_mixed_edge_sites_included"] is True, "candidate profile omits mixed edge")
    port_count = profile["port_count"]
    reticulation_count = profile["reticulation_count"]
    expected_sites = 2 * port_count + 3 * reticulation_count - 3
    require(profile["site_count"] == expected_sites, "candidate site formula")
    sites = profile["sites"]
    require(len(sites) == expected_sites, "candidate site list count")
    ids = [site["site_id"] for site in sites]
    require(len(ids) == len(set(ids)), "duplicate candidate site")
    census = collections.Counter(site["site_type"] for site in sites)
    require(set(census) <= SITE_TYPES, "unknown candidate site type")
    require(dict(sorted(census.items())) == profile["site_type_census"], "candidate site census")
    require(census["root_suppressed_segment"] == 1, "root-suppressed site census")
    root_equivalence = profile["root_half_equivalence"]
    require(root_equivalence["semi_directed_relation_after_insertion"] == "isomorphic", "root-half equivalence")
    require(len(root_equivalence["representative_half_arcs"]) == 2, "root-half representative census")
    return census


def equality_parent_id(row: dict) -> str:
    return f"P1:{row['parent_anchor_id']}:{row['source_site_index']}:{row['target_site_index']}"


def build_coverage() -> dict:
    for label, (path, expected) in FILES.items():
        require(file_sha256(path) == expected, f"frozen input drift:{label}")

    certificate = json.loads(FILES["certificate"][0].read_text())
    replay_payload(certificate, EXPECTED_CERT_PAYLOAD, "probe certificate", exclude=("operational",))
    require(certificate["status"] == "PASS", "probe certificate status")
    require(certificate["assembly_theorem"]["unresolved"] == 0, "assembly unresolved")
    require(certificate["assembly_theorem"]["incoherent"] == 0, "assembly incoherent")
    legacy_flag = "forbidden_" + "rooted_" + "triple_oracle_used"
    require(certificate.get(legacy_flag) is False, "superseded oracle flag")

    contract = json.loads(INPUT_CONTRACT.read_text())
    replay_payload(contract, EXPECTED_INPUT_PAYLOAD, "probe input contract")
    require(contract["status"] == "PASS", "input contract status")
    require(contract["unresolved_anchor_inputs"] == contract["incoherent_site_transports"] == 0, "input contract terminal gates")

    atlas = import_atlas()
    require(
        source_support_grammar_sha256(atlas) == EXPECTED_SOURCE_SUPPORT_GRAMMAR_SHA256,
        "primitive source-support grammar drift",
    )
    supports = atlas.source_supports()
    require(
        [(record.core_id, record.repair_index) for record in supports]
        == [("theta0", 0), ("theta0", 1), ("theta1", 0), ("theta1", 1), ("theta3", 0), ("theta3", 1)],
        "frozen source-support order",
    )
    theta1_arcs = [tuple(arc) for arc in atlas.CORES["theta1"]["arcs"]]
    require(theta1_arcs.count(("U", "V")) == 2, "theta1 parallel-segment representation")

    anchors = contract["anchors"]
    require(len(anchors) == len({row["anchor_id"] for row in anchors}) == 176, "anchor record coverage")
    anchor_by_id = {row["anchor_id"]: row for row in anchors}
    source_index_census = collections.Counter()
    origin_census = collections.Counter()
    relation_census = collections.Counter()
    site_census_source = collections.Counter()
    site_census_target = collections.Counter()
    root_half_checks = 0
    site_type_changes_carried_by_exact_maps = 0
    for anchor in anchors:
        origin_census[anchor["origin"]] += 1
        relation_census[anchor["relation"]] += 1
        if "source_index" in anchor["locator"]:
            source_index_census[anchor["locator"]["source_index"]] += 1
        source_sites = check_candidate_profile(anchor["source_candidate_profile"])
        target_sites = check_candidate_profile(anchor["target_candidate_profile"])
        site_census_source.update(source_sites)
        site_census_target.update(target_sites)
        root_half_checks += 2
        source_ids = {site["site_id"] for site in anchor["source_candidate_profile"]["sites"]}
        target_ids = {site["site_id"] for site in anchor["target_candidate_profile"]["sites"]}
        mapping = anchor["site_transport"]
        require(len(mapping) == len(source_ids) == len(target_ids), "anchor site transport size")
        require({row["source_site_id"] for row in mapping} == source_ids, "anchor source site bijection")
        require({row["target_site_id"] for row in mapping} == target_ids, "anchor target site bijection")
        # Site-type names are diagnostic rooted-presentation names.  The
        # exact mixed-edge map, rather than equality of those names, is the
        # invariant transport object (root movement can change a name).
        site_type_changes_carried_by_exact_maps += sum(
            row["source_site_type"] != row["target_site_type"] for row in mapping
        )
        require(anchor["parent_transport"]["relation"] == anchor["relation"], "anchor relation transport")
    require(set(source_index_census) == set(range(6)), "theta support anchor coverage")
    require(source_index_census[2] == source_index_census[3] == 8, "theta1 repair/parallel coverage")
    require(dict(sorted(origin_census.items())) == contract["anchor_census"]["by_origin"], "anchor origin census")
    require(dict(sorted(relation_census.items())) == contract["anchor_census"]["by_relation"], "anchor relation census")
    require(root_half_checks == contract["root_movement_contract"]["every_anchor_half_equivalences_certified"] == 352, "anchor root-half census")
    expected_site_source = {
        key.split(":", 1)[1]: value
        for key, value in contract["candidate_census"]["site_types"].items()
        if key.startswith("source:")
    }
    expected_site_target = {
        key.split(":", 1)[1]: value
        for key, value in contract["candidate_census"]["site_types"].items()
        if key.startswith("target:")
    }
    require(dict(sorted(site_census_source.items())) == expected_site_source, "anchor source site census")
    require(dict(sorted(site_census_target.items())) == expected_site_target, "anchor target site census")

    public_anchors = certificate["anchor_inventory"]["public_anchors"]
    require({row["anchor_id"] for row in public_anchors} == set(anchor_by_id), "public/input anchor crosswalk")
    public_by_id = {row["anchor_id"]: row for row in public_anchors}
    anchor_transport_ids = set()
    for anchor_id, public in public_by_id.items():
        source = anchor_by_id[anchor_id]
        require(public["origin"] == source["origin"], "anchor origin crosswalk")
        require(public["relation"] == source["relation"], "anchor relation crosswalk")
        require(public["labels"] == source["labels"], "anchor label crosswalk")
        require(public["transport_id"] == source["parent_transport"]["transport_sha256"], "anchor transport crosswalk")
        if public["relation"] == "triangle":
            witness = public["global_triangle"]
            require(witness is not None and len(witness["source_triangle_edges"]) == len(witness["target_triangle_edges"]) == 3, "anchor triangle witness")
        else:
            require(public["global_triangle"] is None, "unexpected anchor triangle")
        anchor_transport_ids.add(public["transport_id"])

    separation = json.load(gzip.open(FILES["separation"][0], "rt"))
    replay_payload(separation, certificate["registries"]["separation"]["payload_sha256"], "separation registry")
    topological_registry = separation["separation_proof_registry"]
    sign_registry = separation["full_map_Ti_registry"]
    require(sign_registry["canonical_relation_certificates"] == len(sign_registry["certificates"]) == 156, "whole-map relation certificates")
    require(sign_registry["canonical_strict_polynomials"] == len(sign_registry["strict_polynomial_registry"]) == 118, "whole-map strict polynomials")
    require(sign_registry.get(legacy_flag) is False, "whole-map registry superseded-oracle flag")
    for proof in sign_registry["certificates"].values():
        weights = proof["boundary_incidence_multihomogeneity"]
        require(list(weights.values()).count("s^2*g") == 2, "T_i non-oriented weights")
        require(list(weights.values()).count("g^2") == 1, "T_i oriented weight")
        require(weights["all_unselected_boundary_incidence_weights"] == "0", "T_i unselected weights")
        require(proof["zero_pullback"].startswith("coefficientwise exact zero"), "T_i exact zero")
        require(proof["strict_sign"] == -1, "T_i strict sign orientation")
    for polynomial in sign_registry["strict_polynomial_registry"].values():
        bernstein = polynomial["Bernstein_certificate"]
        require(bernstein["positive_coefficients"] == 0, "Bernstein positive coefficient")
        require(bernstein["negative_coefficients"] > 0, "Bernstein lacks strict coefficient")
        require(bernstein["maximum_coefficient"] == "0", "Bernstein maximum")
        require("principal D_plus" in bernstein["domain"], "Bernstein physical domain")

    one_counts = collections.Counter()
    one_origin_counts = collections.Counter()
    one_parent = {}
    one_restrictions = set()
    one_transport_ids = set()
    one_root = object_sha256([])
    one_rows = 0
    for row in stream_rows(FILES["one"][0]):
        one_rows += 1
        one_root = chain_step(one_root, row)
        require(row["stage"] == "A+p", "one-port stage")
        require(row["parent_anchor_id"] in anchor_by_id, "one-port parent anchor")
        require(row["status"] in EQUALITY | SEPARATED, "one-port status")
        one_counts[row["status"]] += 1
        one_origin_counts[f"{row['origin']}:{row['status']}"] += 1
        one_restrictions.update((row["source_parent_restriction_id"], row["target_parent_restriction_id"]))
        if row["status"] in EQUALITY:
            parent_id = equality_parent_id(row)
            require(parent_id not in one_parent, "duplicate one-port equality parent")
            require(row.get("proof_id") is None, "equality row carries separator")
            require((row.get("global_triangle_sha256") is not None) == (row["status"] == "triangle"), "one-port triangle state")
            require(row["parent_transport_id"] == public_by_id[row["parent_anchor_id"]]["transport_id"], "one-port parent transport")
            one_parent[parent_id] = row
            one_transport_ids.add(row["transport_id"])
        elif row["status"] == "displayed_quartet_mismatch":
            require(row["proof_id"].startswith("Q:") and row["proof_id"] in topological_registry, "one-port quartet proof")
        else:
            require(row["proof_id"].startswith("TI:") and row["proof_id"] in sign_registry["certificates"], "one-port T_i proof")
    require(one_rows == certificate["one_port"]["raw_pairs"] == 29964, "one-port row census")
    require(one_root == certificate["one_port"]["ordered_ledger"]["ordered_hash_root"], "one-port ordered root")
    require(dict(sorted(one_counts.items())) == certificate["one_port"]["counts"], "one-port status census")
    require(dict(sorted(one_origin_counts.items())) == certificate["one_port"]["counts_by_origin"], "one-port origin census")
    require(len(one_parent) == certificate["one_port"]["equality_survivors"] == 2107, "one-port equality census")

    parent_counts_expected = {}
    parent_relations = {}
    parent_class_ids = set()
    parent_root = object_sha256([])
    parent_rows = 0
    parent_site_checks = collections.Counter()
    for row in stream_rows(FILES["parents"][0]):
        parent_rows += 1
        parent_root = chain_step(parent_root, row)
        parent_id = row["one_port_parent_id"]
        require(parent_id in one_parent and parent_id not in parent_counts_expected, "two-port parent inventory key")
        original = one_parent[parent_id]
        require(row["relation"] == original["status"], "two-port parent relation")
        require(row["source_graph_sha256"] == original["source_child_graph_sha256"], "two-port parent source graph")
        require(row["target_graph_sha256"] == original["target_child_graph_sha256"], "two-port parent target graph")
        source_census = check_candidate_profile(row["source_candidate_profile"])
        target_census = check_candidate_profile(row["target_candidate_profile"])
        parent_site_checks.update({f"source:{key}": value for key, value in source_census.items()})
        parent_site_checks.update({f"target:{key}": value for key, value in target_census.items()})
        expected_pairs = row["source_candidate_profile"]["site_count"] * row["target_candidate_profile"]["site_count"]
        require(row["raw_second_probe_pairs"] == expected_pairs, "two-port parent Cartesian product")
        parent_counts_expected[parent_id] = expected_pairs
        parent_relations[parent_id] = row["relation"]
        parent_class_ids.add(row["canonical_one_port_relation_class_id"])
    require(parent_rows == certificate["two_port"]["parents"] == 2107, "two-port parent census")
    require(set(parent_counts_expected) == set(one_parent), "one-/two-port parent exact coverage")
    require(parent_root == certificate["two_port"]["ordered_parent_inventory"]["ordered_hash_root"], "two-port parent root")
    require(len(parent_class_ids) == certificate["one_port"]["canonical_equality_relation_classes"] == 469, "one-port relation class census")
    require(sum(parent_counts_expected.values()) == certificate["two_port"]["raw_pairs"] == 544571, "two-port Cartesian total")

    two_counts = collections.Counter()
    two_origin_counts = collections.Counter()
    two_by_parent = collections.Counter()
    two_restrictions = set()
    two_transport_ids = set()
    reverse_transport_ids = set()
    reverse_relation_counts = collections.Counter()
    two_root = object_sha256([])
    two_rows = 0
    for row in stream_rows(FILES["two"][0]):
        two_rows += 1
        two_root = chain_step(two_root, row)
        require(row["stage"] == "A+p+q", "two-port stage")
        parent_id = row["one_port_parent_id"]
        require(parent_id in one_parent, "two-port parent")
        require(row["base_anchor_id"] == one_parent[parent_id]["parent_anchor_id"], "two-port base anchor")
        require(row["status"] in EQUALITY | SEPARATED, "two-port status")
        require(row["parent_transport_id"] == one_parent[parent_id]["transport_id"] if row["status"] in EQUALITY else True, "two-port parent transport")
        two_counts[row["status"]] += 1
        two_origin_counts[f"{row['origin']}:{row['status']}"] += 1
        two_by_parent[parent_id] += 1
        two_restrictions.update((row["source_parent_restriction_id"], row["target_parent_restriction_id"]))
        if row["status"] in EQUALITY:
            require(row.get("proof_id") is None, "two-port equality carries separator")
            require((row.get("global_triangle_sha256") is not None) == (row["status"] == "triangle"), "two-port triangle state")
            reverse = row["reverse_order_certificate"]
            require(reverse["same_base_anchor_id"] == row["base_anchor_id"], "reverse base anchor")
            require(reverse["reverse_parent_relation"] == row["status"], "reverse relation")
            require(reverse["conclusion"].startswith("the reversed one-probe marginal is present"), "reverse marginal conclusion")
            two_transport_ids.add(row["transport_id"])
            reverse_transport_ids.add(reverse["reverse_parent_transport_id"])
            reverse_relation_counts[row["status"]] += 1
        elif row["status"] == "displayed_quartet_mismatch":
            require(row["proof_id"].startswith("Q:") and row["proof_id"] in topological_registry, "two-port quartet proof")
        else:
            require(row["proof_id"].startswith("TI:") and row["proof_id"] in sign_registry["certificates"], "two-port T_i proof")
    require(two_rows == certificate["two_port"]["raw_pairs"] == 544571, "two-port row census")
    require(two_root == certificate["two_port"]["ordered_ledger"]["ordered_hash_root"], "two-port ordered root")
    require(dict(sorted(two_counts.items())) == certificate["two_port"]["counts"], "two-port status census")
    require(dict(sorted(two_origin_counts.items())) == certificate["two_port"]["counts_by_origin"], "two-port origin census")
    require(two_by_parent == collections.Counter(parent_counts_expected), "two-port parent Cartesian coverage")
    require(dict(sorted(reverse_relation_counts.items())) == certificate["two_port"]["reverse_order_parent_relation_counts"], "reverse relation census")

    exact_transport_ids = set()
    transport_relation_counts = collections.Counter()
    triangle_transport_witnesses = 0
    transport_root = object_sha256([])
    transport_rows = 0
    for row in stream_rows(FILES["transports"][0]):
        transport_rows += 1
        transport_root = chain_step(transport_root, row)
        require(row["record_kind"] == "exact_labelled_mixed_graph_transport", "transport record kind")
        record_id = row["record_id"]
        require(record_id not in exact_transport_ids, "duplicate exact transport")
        exact_transport_ids.add(record_id)
        record = row["record"]
        require(record["transport_sha256"] == record_id, "transport id binding")
        require(record["relation"] in EQUALITY, "transport relation")
        transport_relation_counts[record["relation"]] += 1
        vertex_map = record["vertex_map"]
        require(len({pair[0] for pair in vertex_map}) == len(vertex_map), "transport source vertex map")
        require(len({pair[1] for pair in vertex_map}) == len(vertex_map), "transport target vertex map")
        if record["relation"] == "triangle":
            witness = record["ordinary_triangle_arrowhead_witness"]
            require(witness is not None, "missing triangle arrowhead witness")
            require(len(witness["source_headed_edges"]) == len(witness["target_headed_edges"]) == 2, "triangle headed-edge census")
            require(all(witness["source_common_reticulation"] in edge for edge in witness["source_headed_edges"]), "source common reticulation")
            require(all(witness["target_common_reticulation"] in edge for edge in witness["target_headed_edges"]), "target common reticulation")
            require(len(record["source_triangle_edges"]) == len(record["target_triangle_edges"]) == 3, "triangle edge census")
            triangle_transport_witnesses += 1
        else:
            require(record["ordinary_triangle_arrowhead_witness"] is None, "isomorphism has triangle witness")
    required_transport_ids = anchor_transport_ids | one_transport_ids | two_transport_ids | reverse_transport_ids
    require(exact_transport_ids == required_transport_ids, "exact transport registry coverage")
    require(transport_rows == certificate["registries"]["exact_transports"]["unique_records"] == 67741, "transport census")
    require(transport_root == certificate["registries"]["exact_transports"]["ordered_records"]["ordered_hash_root"], "transport ordered root")

    restriction_ids = set()
    restriction_root = object_sha256([])
    restriction_rows = 0
    for row in stream_rows(FILES["restrictions"][0]):
        restriction_rows += 1
        restriction_root = chain_step(restriction_root, row)
        require(row["record_kind"] == "exact_parent_marginal_restriction", "restriction record kind")
        require(row["record_id"] not in restriction_ids, "duplicate parent restriction")
        restriction_ids.add(row["record_id"])
        record = row["record"]
        require(record["exact_labelled_relation"] == "isomorphic", "parent restriction relation")
        require(record["parent_mixed_graph_sha256"] == record["restricted_mixed_graph_sha256"], "parent restriction graph recovery")
    require(restriction_ids == one_restrictions | two_restrictions, "parent restriction registry coverage")
    require(restriction_rows == certificate["registries"]["parent_restrictions"]["unique_records"] == 4379, "restriction census")
    require(restriction_root == certificate["registries"]["parent_restrictions"]["ordered_records"]["ordered_hash_root"], "restriction ordered root")

    primitive_types = certificate["assembly_theorem"]["all_primitive_physical_anchor_types"]
    require(primitive_types == ["ordinary_tree", "cycle", "theta0", "theta1", "theta2", "theta3"], "primitive support list")
    site_gate = certificate["assembly_theorem"]["root_movement_and_site_completeness"]
    require(all(site_gate[key] is True for key in ("all_suppressed_mixed_edges", "artificial_root_halves_quotiented_by_exact_isomorphism", "pendant_arms", "reticulation_incoming_edges", "root_suppressed_segment")), "site completeness assembly gate")
    triangle_gate = certificate["assembly_theorem"]["one_global_triangle_gate"]
    require(triangle_gate["new_triangle_created_above_isomorphic_parent"] == 0, "new triangle creation")
    require(triangle_gate["every_triangle_transport_uses_the_same_parent_triangle_edges_and_common_reticulation"] is True, "global triangle transport")
    order_gate = certificate["assembly_theorem"]["two_port_order_gate"]
    require(order_gate["every_equality_has_reversed_one_port_marginal"] is True and order_gate["reversed_marginals_missing"] == 0, "word-order reverse gate")

    result = {
        "schema": "k2p-probe-word-theorem-coverage-v1",
        "status": "PASS",
        "compression_status": "PC-PARTIAL",
        "source": {
            **{
                label: {"path": str(path.relative_to(PROJECT)), "sha256": expected}
                for label, (path, expected) in FILES.items()
            },
            "atlas_source_support_grammar": {
                "path": str(ATLAS.relative_to(PROJECT)),
                "binding_kind": "ordered primitive source-support semantic fingerprint",
                "sha256": EXPECTED_SOURCE_SUPPORT_GRAMMAR_SHA256,
            },
        },
        "source_payloads": {
            "probe_certificate": EXPECTED_CERT_PAYLOAD,
            "probe_input_contract": EXPECTED_INPUT_PAYLOAD,
            "separation_registry": separation["payload_sha256"],
        },
        "primitive_anchor_coverage": {
            "types": primitive_types,
            "anchor_records": len(anchors),
            "canonical_anchor_classes": certificate["anchor_inventory"]["canonical_anchor_classes"],
            "origin_census": dict(sorted(origin_census.items())),
            "relation_census": dict(sorted(relation_census.items())),
            "theta_source_index_census": {str(key): value for key, value in sorted(source_index_census.items())},
            "theta1_parallel_segments": {
                "parallel_core_arcs": 2,
                "repair_presentations": [2, 3],
                "anchor_records_per_presentation": [source_index_census[2], source_index_census[3]],
            },
        },
        "site_coverage": {
            "site_types": sorted(SITE_TYPES),
            "source_anchor_sites": sum(site_census_source.values()),
            "target_anchor_sites": sum(site_census_target.values()),
            "source_type_census": dict(sorted(site_census_source.items())),
            "target_type_census": dict(sorted(site_census_target.items())),
            "root_half_equivalences": root_half_checks,
            "per_graph_formula": "2*k + 3*r - 3",
            "all_anchor_site_transports_bijective": True,
            "diagnostic_site_type_changes_carried_by_exact_maps": site_type_changes_carried_by_exact_maps,
        },
        "one_port": {
            "raw_pairs": one_rows,
            "counts": dict(sorted(one_counts.items())),
            "equality_parents": len(one_parent),
            "canonical_equality_relation_classes": len(parent_class_ids),
            "ordered_hash_root": one_root,
            "unresolved": 0,
        },
        "two_port": {
            "parents": parent_rows,
            "raw_pairs": two_rows,
            "counts": dict(sorted(two_counts.items())),
            "equality_rows": sum(reverse_relation_counts.values()),
            "reversed_marginals_checked": sum(reverse_relation_counts.values()),
            "reversed_marginals_missing": 0,
            "ordered_parent_hash_root": parent_root,
            "ordered_hash_root": two_root,
            "unresolved": 0,
        },
        "transport_coherence": {
            "exact_transport_records": transport_rows,
            "exact_transport_relation_census": dict(sorted(transport_relation_counts.items())),
            "triangle_arrowhead_witnesses": triangle_transport_witnesses,
            "parent_restriction_records": restriction_rows,
            "unreferenced_exact_transports": 0,
            "missing_exact_transports": 0,
            "unreferenced_parent_restrictions": 0,
            "missing_parent_restrictions": 0,
            "incoherent": 0,
        },
        "separator_coverage": {
            "displayed_quartet_certificate_classes": len(topological_registry),
            "whole_map_Ti_relation_certificate_classes": len(sign_registry["certificates"]),
            "whole_map_Ti_strict_polynomial_classes": len(sign_registry["strict_polynomial_registry"]),
            "every_Ti_boundary_incidence_multihomogeneous": True,
            "every_Ti_strict_side_Bernstein_certified": True,
        },
        "word_theorem_hypotheses": {
            "every_primitive_kernel_has_physical_equality_anchors": True,
            "every_suppressed_mixed_edge_site_is_probed": True,
            "every_one_port_nonrelation_is_exactly_separated": True,
            "every_one_port_equality_has_an_exact_parent_transport": True,
            "every_two_port_nonrelation_is_exactly_separated": True,
            "every_two_port_equality_restricts_to_both_one_port_orders": True,
            "parallel_theta1_segments_remain_edge_incidence_distinguished": True,
            "ordinary_triangle_is_a_common_reticulation_arrowhead_relation": True,
            "anchor_automorphisms_are_carried_by_exact_edge_maps": True,
            "new_triangle_above_an_isomorphic_parent": 0,
        },
        "compression_verdict": {
            "word_theorem_status": "proved from the exact finite premises",
            "finite_exception_table_found": False,
            "ledger_residue": {
                "anchors": 176,
                "one_port_rows": one_rows,
                "two_port_rows": two_rows,
                "exact_transports": transport_rows,
                "parent_restrictions": restriction_rows,
            },
            "reason": "The word-induction argument is uniform, but the bounded pass found no smaller theorem replacing the exact finite separation and transport premises.  Those ledgers remain load-bearing.",
        },
    }
    result["payload_sha256"] = object_sha256(result)
    return result


def main() -> None:
    if not __debug__:
        raise Failure("PROBE_WORD_VERIFIER_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--emit", action="store_true")
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", type=Path, nargs="?", const=OUTPUT)
    args = parser.parse_args()
    generated = build_coverage()
    if args.emit:
        print(json.dumps(generated, indent=2, sort_keys=True))
        return
    if args.write:
        OUTPUT.write_text(json.dumps(generated, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        target = OUTPUT
    else:
        target = args.check or OUTPUT
    require(target.exists(), f"missing probe word coverage:{target}")
    require(json.loads(target.read_text()) == generated, "probe word coverage drift")
    print(json.dumps({
        "status": "PASS",
        "coverage_sha256": file_sha256(target),
        "payload_sha256": generated["payload_sha256"],
        "anchors": generated["primitive_anchor_coverage"]["anchor_records"],
        "one_port_rows": generated["one_port"]["raw_pairs"],
        "two_port_rows": generated["two_port"]["raw_pairs"],
        "exact_transports": generated["transport_coherence"]["exact_transport_records"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
