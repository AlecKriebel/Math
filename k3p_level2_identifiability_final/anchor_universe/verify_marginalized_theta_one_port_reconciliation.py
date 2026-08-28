#!/usr/bin/env python3
"""Reconcile every marginalized-incoming theta path with the one-port ledger.

This verifier is deliberately structural.  It regenerates the clean-room
theta root-movement mapping, uses graph hashes and mixed-edge endpoints to
crosswalk its canonical seed representatives into the frozen probe contract,
and then checks the corresponding one-port equality rows and canonical class
inventory.  It imports no atlas, probe producer, or K2P algebra.
"""

from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
VERIFIER = Path(__file__).resolve()
CORE = HERE / "independent_non_four_core.py"
ARTIFACT = HERE / "artifacts" / "NON_FOUR_ANCHOR_UNIVERSE.json"
CONTRACT = (
    PROJECT
    / "input_frozen"
    / "model_independent_topology_package"
    / "anchor_inputs"
    / "probe_input_contract.json"
)
ONE_PORT_LEDGER = PROJECT / "probes" / "one_port_ledger.jsonl.gz"
TWO_PORT_PARENT_INVENTORY = (
    PROJECT / "probes" / "two_port_parent_inventory.jsonl.gz"
)
DEFAULT_OUTPUT = HERE / "MARGINALIZED_THETA_ONE_PORT_RECONCILIATION.json"


EXPECTED_FILE_SHA256 = {
    CONTRACT: "7f686ae99dd5e6dafc1c04396b711d294a0bddd6a25574f9ea809b831ad7b377",
    ONE_PORT_LEDGER: "1091d7f1a0c78408d0c10dfab31b0d2a5ae2c5447543c5bdb99d2abcb883bf2b",
    TWO_PORT_PARENT_INVENTORY: "673112e949e08dce0bdbd690be647dd97d0899c2bb12121b4a16ed7a62dba3f8",
}
EXPECTED_MAPPING_ROWS_SHA256 = (
    "29afb6d8ab4adc9e3fb588063d19ac7f7caed40ae0364034d8fc9b9951d2bff2"
)
EXPECTED_ARTIFACT_PAYLOAD_SHA256 = (
    "deaf87176f83c50ded5868ee20aed7eef0cb8bee1b57dc34ff72cd62ae6f25db"
)
EXPECTED_CONTRACT_PAYLOAD_SHA256 = (
    "579919ca13204ddf959b3a159e4849b69c05ac87861eba2221659ec45bd73f38"
)


class ReconciliationFailure(RuntimeError):
    """Raised on any incomplete, ambiguous, or inconsistent crosswalk."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReconciliationFailure(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    require(isinstance(value, dict), f"JSON object required:{path}")
    return value


def jsonl_gzip(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rt") as handle:
        for line_number, line in enumerate(handle, 1):
            value = json.loads(line)
            require(
                isinstance(value, dict),
                f"JSONL object required:{path}:{line_number}",
            )
            yield value


def import_core() -> Any:
    name = "marginalized_theta_clean_room_core"
    specification = importlib.util.spec_from_file_location(name, CORE)
    require(
        specification is not None and specification.loader is not None,
        f"cannot import clean-room core:{CORE}",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def string_counter(counter: collections.Counter[Any]) -> dict[str, int]:
    return {
        str(key): value
        for key, value in sorted(counter.items(), key=lambda row: str(row[0]))
    }


def multiplicity_histogram(values: Iterable[int]) -> dict[str, int]:
    return string_counter(collections.Counter(values))


def verify_payload_hash(
    value: dict[str, Any], expected: str, excluded: set[str]
) -> None:
    payload = {key: item for key, item in value.items() if key not in excluded}
    require(value.get("payload_sha256") == expected, "stored payload hash binding")
    require(digest(payload) == expected, "recomputed payload hash binding")


def unique_index(rows: list[dict[str, Any]], key_name: str) -> dict[Any, dict[str, Any]]:
    result: dict[Any, dict[str, Any]] = {}
    for row in rows:
        key = row.get(key_name)
        require(key is not None, f"missing unique key:{key_name}")
        require(key not in result, f"duplicate unique key:{key_name}:{key}")
        result[key] = row
    return result


def profile_site_index(
    profile: dict[str, Any], endpoints: list[str], context: str
) -> tuple[int, dict[str, Any]]:
    sites = profile.get("sites")
    require(isinstance(sites, list), f"candidate sites missing:{context}")
    hits = [
        (index, site)
        for index, site in enumerate(sites)
        if site.get("mixed_endpoints") == endpoints
    ]
    require(len(hits) == 1, f"candidate site uniqueness:{context}:{len(hits)}")
    return hits[0]


def verify() -> dict[str, Any]:
    file_hashes = {
        path: sha256_file(path)
        for path in (
            VERIFIER,
            CORE,
            ARTIFACT,
            CONTRACT,
            ONE_PORT_LEDGER,
            TWO_PORT_PARENT_INVENTORY,
        )
    }
    for path, expected in EXPECTED_FILE_SHA256.items():
        require(file_hashes[path] == expected, f"input file hash:{path}")

    artifact = load_json(ARTIFACT)
    require(
        artifact.get("schema") == "k3p-model-independent-non-four-anchor-universe-v1",
        "non-four artifact schema",
    )
    require(artifact.get("status") == "PASS", "non-four artifact status")
    verify_payload_hash(
        artifact,
        EXPECTED_ARTIFACT_PAYLOAD_SHA256,
        {"payload_sha256", "operational"},
    )
    artifact_anchors = artifact.get("anchors")
    require(isinstance(artifact_anchors, list), "non-four artifact anchors")
    require(len(artifact_anchors) == 133, "non-four artifact anchor census")
    artifact_by_key = unique_index(artifact_anchors, "anchor_key")
    require(
        digest(sorted(artifact_by_key))
        == artifact.get("ordered_anchor_key_sha256")
        == "6c2eaccd894aaf2dc4dd8bde2f1590fc753e5e6ee53b18102b6fa8ede865df7a",
        "non-four semantic-key root",
    )

    contract = load_json(CONTRACT)
    require(
        contract.get("schema") == "k2p-root-invariant-probe-input-contract-v2",
        "frozen structural contract schema",
    )
    require(contract.get("status") == "PASS", "frozen structural contract status")
    verify_payload_hash(contract, EXPECTED_CONTRACT_PAYLOAD_SHA256, {"payload_sha256"})
    contract_anchors = contract.get("anchors")
    require(isinstance(contract_anchors, list), "frozen structural contract anchors")
    require(len(contract_anchors) == 176, "frozen structural contract census")
    unique_index(contract_anchors, "anchor_id")
    contract_by_graph_pair: dict[tuple[str, str], list[dict[str, Any]]] = (
        collections.defaultdict(list)
    )
    for anchor in contract_anchors:
        contract_by_graph_pair[
            (anchor["source_graph_sha256"], anchor["target_graph_sha256"])
        ].append(anchor)

    core = import_core()
    enumerate_theta = getattr(core, "_enumerate_theta2", None)
    require(callable(enumerate_theta), "clean-room theta enumerator")
    theta_rows, theta_stage, theta_diagnostics = enumerate_theta()
    require(len(theta_rows) == 96, "clean-room theta seed census")
    require(
        collections.Counter(row["origin"] for row in theta_rows)
        == {
            "theta2_physical_k5": 24,
            "theta2_physical_k6": 40,
            "theta2_physical_k7": 32,
        },
        "clean-room theta seed origins",
    )
    require(
        theta_stage.get("theta2_excluded_full_restoration_isomorphic_paths") == 424,
        "clean-room excluded terminal census",
    )
    root_mapping = theta_diagnostics.get("marginalized_root_movement_mapping")
    require(isinstance(root_mapping, dict), "clean-room root-movement mapping")
    require(root_mapping.get("mapped") == 424, "clean-room mapped census")
    require(root_mapping.get("unmatched") == 0, "clean-room unmatched census")
    require(
        root_mapping.get("terminal_paths_with_every_prefix_checked") == 424,
        "clean-room prefix path coverage",
    )
    require(
        root_mapping.get("prefix_exact_equality_checks") == 984,
        "clean-room prefix equality census",
    )
    require(
        root_mapping.get("canonical_seed_class_count") == 15,
        "clean-room canonical seed class census",
    )
    require(
        root_mapping.get("canonical_seed_class_member_census")
        == {"4": 4, "5": 4, "6": 2, "8": 2, "10": 2, "12": 1},
        "clean-room seed member multiplicities",
    )
    require(
        root_mapping.get("mapped_by_seed_origin")
        == {
            "theta2_physical_k5": 56,
            "theta2_physical_k6": 176,
            "theta2_physical_k7": 192,
        },
        "clean-room root-movement depth census",
    )
    mapping_rows = root_mapping.get("mapping_rows")
    require(isinstance(mapping_rows, list), "clean-room mapping rows")
    require(len(mapping_rows) == 424, "clean-room mapping row census")
    require(
        len({canonical_bytes(row) for row in mapping_rows}) == 424,
        "clean-room mapping row uniqueness",
    )
    require(
        root_mapping.get("mapping_rows_sha256")
        == digest(sorted(mapping_rows, key=canonical_bytes))
        == EXPECTED_MAPPING_ROWS_SHA256,
        "clean-room mapping row digest",
    )

    abstract_site_keys = {
        (
            row["canonical_seed_key"],
            tuple(row["source_one_port_site_on_seed"]),
            tuple(row["target_one_port_site_on_seed"]),
        )
        for row in mapping_rows
    }
    require(len(abstract_site_keys) == 66, "clean-room abstract site-pair census")
    require(
        collections.Counter(
            (
                row["source_one_port_site_type"],
                row["target_one_port_site_type"],
            )
            for row in mapping_rows
        )
        == {("mixed_edge", "root_suppressed_segment"): 424},
        "clean-room attachment-site mechanism",
    )

    preliminary: list[dict[str, Any]] = []
    requested_ledger_keys: set[tuple[str, int, int]] = set()
    seed_contract_rows: dict[str, dict[str, Any]] = {}
    for mapping in mapping_rows:
        seed_key = mapping["canonical_seed_key"]
        artifact_anchor = artifact_by_key.get(seed_key)
        require(artifact_anchor is not None, f"semantic seed key:{seed_key}")
        require(artifact_anchor.get("relation") == "isomorphic", "semantic seed relation")
        require(
            artifact_anchor.get("origin") == mapping["canonical_seed_origin"],
            "semantic seed origin",
        )
        require(
            artifact_anchor.get("port_count") == mapping["restricted_port_count"],
            "semantic seed port count",
        )
        graph_pair = (
            artifact_anchor["source_graph_sha256"],
            artifact_anchor["target_graph_sha256"],
        )
        contract_hits = contract_by_graph_pair.get(graph_pair, [])
        require(
            len(contract_hits) == 1,
            f"frozen anchor graph-pair uniqueness:{seed_key}:{len(contract_hits)}",
        )
        contract_anchor = contract_hits[0]
        previous_contract = seed_contract_rows.setdefault(seed_key, contract_anchor)
        require(previous_contract == contract_anchor, "stable semantic-to-frozen anchor map")
        require(contract_anchor.get("relation") == "isomorphic", "frozen seed relation")
        require(
            contract_anchor.get("origin") == mapping["canonical_seed_origin"],
            "frozen seed origin",
        )
        require(
            contract_anchor.get("labels")
            == list(range(mapping["restricted_port_count"])),
            "frozen seed labels",
        )

        source_index, source_site = profile_site_index(
            contract_anchor["source_candidate_profile"],
            mapping["source_one_port_site_on_seed"],
            f"source:{seed_key}",
        )
        target_index, target_site = profile_site_index(
            contract_anchor["target_candidate_profile"],
            mapping["target_one_port_site_on_seed"],
            f"target:{seed_key}",
        )
        ledger_key = (contract_anchor["anchor_id"], source_index, target_index)
        requested_ledger_keys.add(ledger_key)
        preliminary.append(
            {
                "mapping": mapping,
                "artifact_anchor": artifact_anchor,
                "contract_anchor": contract_anchor,
                "source_site_index": source_index,
                "source_site": source_site,
                "target_site_index": target_index,
                "target_site": target_site,
                "ledger_key": ledger_key,
            }
        )

    require(len(seed_contract_rows) == 15, "external canonical seed representative census")
    require(len(requested_ledger_keys) == 66, "external requested site-pair census")

    ledger_statuses: collections.Counter[str] = collections.Counter()
    ledger_keys: set[tuple[str, int, int]] = set()
    selected_ledger_rows: dict[tuple[str, int, int], dict[str, Any]] = {}
    ledger_count = 0
    for row in jsonl_gzip(ONE_PORT_LEDGER):
        ledger_count += 1
        key = (
            row.get("parent_anchor_id"),
            row.get("source_site_index"),
            row.get("target_site_index"),
        )
        require(key not in ledger_keys, f"one-port ledger key uniqueness:{key}")
        ledger_keys.add(key)
        ledger_statuses[row.get("status")] += 1
        if key in requested_ledger_keys:
            selected_ledger_rows[key] = row
    require(ledger_count == 29_964, "one-port ledger row census")
    require(
        ledger_statuses
        == {
            "displayed_quartet_mismatch": 27_758,
            "isomorphic": 1_915,
            "k3p_tree_sunlet_sos": 99,
            "triangle": 192,
        },
        "one-port ledger status census",
    )
    require(
        set(selected_ledger_rows) == requested_ledger_keys,
        "one-port ledger requested-key coverage",
    )

    requested_parent_ids = {
        f"P1:{parent_anchor_id}:{source_index}:{target_index}"
        for parent_anchor_id, source_index, target_index in requested_ledger_keys
    }
    inventory_relations: collections.Counter[str] = collections.Counter()
    inventory_ids: set[str] = set()
    selected_inventory: dict[str, dict[str, Any]] = {}
    inventory_count = 0
    for row in jsonl_gzip(TWO_PORT_PARENT_INVENTORY):
        inventory_count += 1
        parent_id = row.get("one_port_parent_id")
        require(parent_id not in inventory_ids, f"two-port parent uniqueness:{parent_id}")
        inventory_ids.add(parent_id)
        inventory_relations[row.get("relation")] += 1
        if parent_id in requested_parent_ids:
            selected_inventory[parent_id] = row
    require(inventory_count == 2_107, "two-port parent inventory census")
    require(
        inventory_relations == {"isomorphic": 1_915, "triangle": 192},
        "two-port parent inventory relation census",
    )
    require(
        set(selected_inventory) == requested_parent_ids,
        "two-port parent requested-ID coverage",
    )

    path_crosswalk: list[dict[str, Any]] = []
    grouped_site_rows: dict[str, dict[str, Any]] = {}
    abstract_to_parent: dict[tuple[Any, ...], str] = {}
    parent_to_abstract: dict[str, tuple[Any, ...]] = {}
    for item in preliminary:
        mapping = item["mapping"]
        contract_anchor = item["contract_anchor"]
        source_index = item["source_site_index"]
        target_index = item["target_site_index"]
        source_site = item["source_site"]
        target_site = item["target_site"]
        ledger = selected_ledger_rows[item["ledger_key"]]
        require(ledger.get("status") == "isomorphic", "selected one-port status")
        require(ledger.get("stage") == "A+p", "selected one-port stage")
        require(ledger.get("origin") == mapping["canonical_seed_origin"], "selected one-port origin")
        require(
            ledger.get("inserted_label") == mapping["restricted_port_count"],
            "selected one-port inserted label",
        )
        require(ledger.get("source_site_id") == source_site.get("site_id"), "source site ID")
        require(ledger.get("target_site_id") == target_site.get("site_id"), "target site ID")

        one_port_parent_id = (
            f"P1:{contract_anchor['anchor_id']}:{source_index}:{target_index}"
        )
        inventory = selected_inventory[one_port_parent_id]
        require(inventory.get("relation") == "isomorphic", "selected inventory relation")
        require(inventory.get("base_anchor_id") == contract_anchor["anchor_id"], "inventory base anchor")
        require(inventory.get("origin") == mapping["canonical_seed_origin"], "inventory origin")
        require(inventory.get("first_label") == ledger["inserted_label"], "inventory first label")
        require(inventory.get("first_source_site_index") == source_index, "inventory source site")
        require(inventory.get("first_target_site_index") == target_index, "inventory target site")
        require(
            inventory.get("source_graph_sha256") == ledger["source_child_graph_sha256"],
            "inventory source child graph",
        )
        require(
            inventory.get("target_graph_sha256") == ledger["target_child_graph_sha256"],
            "inventory target child graph",
        )

        abstract_key = (
            mapping["canonical_seed_key"],
            tuple(mapping["source_one_port_site_on_seed"]),
            tuple(mapping["target_one_port_site_on_seed"]),
        )
        previous_parent = abstract_to_parent.setdefault(abstract_key, one_port_parent_id)
        require(previous_parent == one_port_parent_id, "abstract-to-ledger site map")
        previous_abstract = parent_to_abstract.setdefault(one_port_parent_id, abstract_key)
        require(previous_abstract == abstract_key, "ledger-to-abstract site map")

        path_row = {
            "excluded_base_raw_id": mapping["excluded_base_raw_id"],
            "source_index": mapping["source_index"],
            "target_index": mapping["target_index"],
            "permutation_index": mapping["permutation_index"],
            "restored_role_order": mapping["restored_role_order"],
            "source_placement_path": mapping["source_placement_path"],
            "incoming_label_removed": mapping["incoming_label_removed"],
            "restricted_port_count": mapping["restricted_port_count"],
            "canonical_seed_key": mapping["canonical_seed_key"],
            "canonical_seed_origin": mapping["canonical_seed_origin"],
            "source_restriction_transport_sha256": mapping[
                "source_restriction_transport_sha256"
            ],
            "target_restriction_transport_sha256": mapping[
                "target_restriction_transport_sha256"
            ],
            "frozen_parent_anchor_id": contract_anchor["anchor_id"],
            "source_site_index": source_index,
            "target_site_index": target_index,
            "one_port_parent_id": one_port_parent_id,
            "canonical_one_port_relation_class_id": inventory[
                "canonical_one_port_relation_class_id"
            ],
            "one_port_transport_id": ledger["transport_id"],
        }
        path_crosswalk.append(path_row)

        site_metadata = {
            "canonical_seed_key": mapping["canonical_seed_key"],
            "canonical_seed_origin": mapping["canonical_seed_origin"],
            "seed_port_count": mapping["restricted_port_count"],
            "frozen_parent_anchor_id": contract_anchor["anchor_id"],
            "source_site_index": source_index,
            "source_site_id": source_site["site_id"],
            "source_site_type": source_site["site_type"],
            "source_site_mixed_endpoints": source_site["mixed_endpoints"],
            "target_site_index": target_index,
            "target_site_id": target_site["site_id"],
            "target_site_type": target_site["site_type"],
            "target_site_mixed_endpoints": target_site["mixed_endpoints"],
            "one_port_parent_id": one_port_parent_id,
            "canonical_one_port_relation_class_id": inventory[
                "canonical_one_port_relation_class_id"
            ],
            "one_port_relation": ledger["status"],
            "one_port_transport_id": ledger["transport_id"],
            "source_child_graph_sha256": ledger["source_child_graph_sha256"],
            "target_child_graph_sha256": ledger["target_child_graph_sha256"],
        }
        grouped = grouped_site_rows.setdefault(
            one_port_parent_id,
            {"metadata": site_metadata, "path_count": 0, "incoming_labels": collections.Counter()},
        )
        require(grouped["metadata"] == site_metadata, "stable grouped site metadata")
        grouped["path_count"] += 1
        grouped["incoming_labels"][mapping["incoming_label_removed"]] += 1

    require(len(path_crosswalk) == 424, "external path crosswalk census")
    require(len(abstract_to_parent) == len(parent_to_abstract) == 66, "site-pair bijection")
    require(len(grouped_site_rows) == 66, "grouped one-port row census")
    one_port_class_ids = {
        row["metadata"]["canonical_one_port_relation_class_id"]
        for row in grouped_site_rows.values()
    }
    require(len(one_port_class_ids) == 66, "canonical one-port class census")

    site_pair_rows = []
    for parent_id in sorted(grouped_site_rows):
        grouped = grouped_site_rows[parent_id]
        site_pair_rows.append(
            {
                **grouped["metadata"],
                "mapped_path_count": grouped["path_count"],
                "incoming_label_census": string_counter(grouped["incoming_labels"]),
            }
        )
    path_crosswalk = sorted(path_crosswalk, key=canonical_bytes)
    site_pair_rows = sorted(site_pair_rows, key=canonical_bytes)

    path_counts_by_parent = collections.Counter(
        row["one_port_parent_id"] for row in path_crosswalk
    )
    require(
        multiplicity_histogram(path_counts_by_parent.values())
        == {"1": 12, "2": 18, "4": 10, "8": 10, "12": 8, "16": 4, "24": 4},
        "one-port class path multiplicities",
    )

    seed_loads = root_mapping.get("mapped_by_seed_class")
    require(isinstance(seed_loads, dict) and len(seed_loads) == 15, "seed path loads")
    require(
        multiplicity_histogram(seed_loads.values())
        == {"14": 2, "22": 4, "24": 4, "28": 1, "44": 2, "48": 2},
        "seed class path multiplicities",
    )

    expected_depth = {
        1: (56, 3, 24, {"1": 12, "2": 6, "4": 4, "8": 2}),
        2: (176, 6, 30, {"2": 12, "4": 6, "8": 8, "16": 4}),
        3: (192, 6, 12, {"12": 8, "24": 4}),
    }
    depth_census: dict[str, Any] = {}
    for depth, (path_count, seed_count, pair_count, path_histogram) in expected_depth.items():
        seed_port_count = depth + 4
        selected_paths = [
            row for row in path_crosswalk if row["restricted_port_count"] == seed_port_count
        ]
        selected_pairs = [
            row for row in site_pair_rows if row["seed_port_count"] == seed_port_count
        ]
        selected_seed_keys = {row["canonical_seed_key"] for row in selected_paths}
        selected_parent_ids = {row["frozen_parent_anchor_id"] for row in selected_paths}
        selected_class_ids = {
            row["canonical_one_port_relation_class_id"] for row in selected_pairs
        }
        observed_histogram = multiplicity_histogram(
            row["mapped_path_count"] for row in selected_pairs
        )
        require(len(selected_paths) == path_count, f"depth path census:{depth}")
        require(len(selected_seed_keys) == seed_count, f"depth seed census:{depth}")
        require(len(selected_parent_ids) == seed_count, f"depth frozen parent census:{depth}")
        require(len(selected_pairs) == pair_count, f"depth site-pair census:{depth}")
        require(len(selected_class_ids) == pair_count, f"depth one-port class census:{depth}")
        require(observed_histogram == path_histogram, f"depth multiplicities:{depth}")
        depth_census[str(depth)] = {
            "full_path_port_count": seed_port_count + 1,
            "restricted_seed_port_count": seed_port_count,
            "mapped_paths": path_count,
            "canonical_seed_classes": seed_count,
            "one_port_site_pairs": pair_count,
            "canonical_one_port_relation_classes": pair_count,
            "path_multiplicity_per_site_pair": observed_histogram,
        }

    incoming_label_census = collections.Counter(
        (row["restricted_port_count"], row["incoming_label_removed"])
        for row in path_crosswalk
    )
    require(
        incoming_label_census
        == {
            (5, 5): 56,
            (6, 5): 88,
            (6, 6): 88,
            (7, 5): 64,
            (7, 6): 64,
            (7, 7): 64,
        },
        "incoming restored-label census",
    )

    report: dict[str, Any] = {
        "schema": "k3p-marginalized-theta-one-port-reconciliation-v1",
        "status": "PASS",
        "claim_boundary": (
            "Structural root-movement and existing-ledger reconciliation only. "
            "No K2P algebra, rank argument, or K2P separation certificate is used. "
            "The frozen contract is read only for graph-hash identity and mixed-edge "
            "candidate profiles; the stored K3P one-port relation is required to be exact "
            "labelled semi-directed isomorphism."
        ),
        "inputs": {
            "verifier": {
                "path": str(VERIFIER.relative_to(PROJECT)),
                "sha256": file_hashes[VERIFIER],
            },
            "clean_room_core": {
                "path": str(CORE.relative_to(PROJECT)),
                "sha256": file_hashes[CORE],
                "mapping_rows_sha256": EXPECTED_MAPPING_ROWS_SHA256,
            },
            "non_four_anchor_artifact": {
                "path": str(ARTIFACT.relative_to(PROJECT)),
                "sha256": file_hashes[ARTIFACT],
                "payload_sha256": artifact["payload_sha256"],
            },
            "frozen_structural_probe_contract": {
                "path": str(CONTRACT.relative_to(PROJECT)),
                "sha256": file_hashes[CONTRACT],
                "payload_sha256": contract["payload_sha256"],
            },
            "one_port_ledger": {
                "path": str(ONE_PORT_LEDGER.relative_to(PROJECT)),
                "sha256": file_hashes[ONE_PORT_LEDGER],
            },
            "two_port_parent_inventory": {
                "path": str(TWO_PORT_PARENT_INVENTORY.relative_to(PROJECT)),
                "sha256": file_hashes[TWO_PORT_PARENT_INVENTORY],
            },
        },
        "method": {
            "clean_room_root_movement": (
                "For each fully restored marginalized-incoming terminal, remove the "
                "label occupying target INCOMING, restrict and compact both sides, and "
                "exactly transport the restricted pair to its unique canonical theta seed class."
            ),
            "site_transport": (
                "Recover the removed leaf's attachment edge on each restricted side and "
                "transport both endpoints through the canonical exact mixed-graph maps."
            ),
            "external_lookup": (
                "Map the semantic seed key through its ordered graph-hash pair to one unique "
                "frozen parent, map transported endpoints to unique candidate-profile site "
                "indices, require the exact one-port ledger key to be isomorphic, and require "
                "the resulting P1 ID in the canonical parent inventory."
            ),
            "lookup_key": [
                "parent_anchor_id",
                "source_site_index",
                "target_site_index",
            ],
        },
        "global_source_census": {
            "non_four_semantic_anchors": len(artifact_anchors),
            "frozen_anchor_contract_rows": len(contract_anchors),
            "one_port_ledger_rows": ledger_count,
            "one_port_ledger_statuses": dict(sorted(ledger_statuses.items())),
            "two_port_parent_inventory_rows": inventory_count,
            "two_port_parent_inventory_relations": dict(
                sorted(inventory_relations.items())
            ),
        },
        "reconciliation_census": {
            "marginalized_incoming_abstract_parents": 176,
            "fully_restored_exact_paths": len(path_crosswalk),
            "prefix_exact_equality_checks": root_mapping[
                "prefix_exact_equality_checks"
            ],
            "theta_seed_presentations": len(theta_rows),
            "canonical_theta_seed_pair_classes": len(seed_contract_rows),
            "abstract_transported_site_pairs": len(abstract_site_keys),
            "existing_isomorphic_one_port_rows": len(grouped_site_rows),
            "canonical_one_port_relation_classes": len(one_port_class_ids),
            "mapped": len(path_crosswalk),
            "unmatched": 0,
        },
        "depth_census": depth_census,
        "multiplicity_census": {
            "seed_class_member_count": root_mapping[
                "canonical_seed_class_member_census"
            ],
            "mapped_paths_per_seed_class": multiplicity_histogram(
                seed_loads.values()
            ),
            "mapped_paths_per_one_port_site_pair": multiplicity_histogram(
                path_counts_by_parent.values()
            ),
            "incoming_label_by_restricted_port_count": {
                f"k{port}:label{label}": count
                for (port, label), count in sorted(incoming_label_census.items())
            },
        },
        "bindings": {
            "clean_room_mapping_rows_sha256": root_mapping[
                "mapping_rows_sha256"
            ],
            "path_crosswalk_sha256": digest(path_crosswalk),
            "one_port_site_pair_rows_sha256": digest(site_pair_rows),
        },
        "one_port_site_pairs": site_pair_rows,
        "path_crosswalk": path_crosswalk,
    }
    report["payload_sha256"] = digest(report)
    return report


def main() -> None:
    if not __debug__:
        raise ReconciliationFailure("optimized mode forbidden")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()
    report = verify()
    output = arguments.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(
        "MARGINALIZED_THETA_ONE_PORT_RECONCILIATION_PASS "
        f"paths={report['reconciliation_census']['mapped']} "
        f"seed_classes={report['reconciliation_census']['canonical_theta_seed_pair_classes']} "
        f"site_pairs={report['reconciliation_census']['existing_isomorphic_one_port_rows']} "
        f"payload_sha256={report['payload_sha256']}"
    )


if __name__ == "__main__":
    main()
