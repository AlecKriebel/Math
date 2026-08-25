#!/usr/bin/env python3
"""Seal deterministic K3P restoration/probe/transport manifests.

This command deliberately distinguishes the independently regenerated K3P
probe evidence from the imported, model-independent restoration graph
contract.  It cannot promote the latter's K2P algebra certificates.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
TOPOLOGY = PROJECT / "input_frozen/model_independent_topology_package"
CERTIFICATE = HERE / "K3P_PROBE_COHERENCE_CERTIFICATE.json"
REPLAY = HERE / "K3P_PROBE_INDEPENDENT_VERIFICATION.json"
MUTATIONS = HERE / "K3P_PROBE_MUTATION_CERTIFICATE.json"
RESTORATION = TOPOLOGY / "anchor_inputs/corrected_restoration_forest.json"
K3P_RESTORATION_ROOT = PROJECT / "restoration"
K3P_RESTORATION_MANIFEST = K3P_RESTORATION_ROOT / "RESTORATION_MANIFEST.json"
K3P_RESTORATION_REPLAY = K3P_RESTORATION_ROOT / "K3P_RESTORATION_INDEPENDENT_VERIFICATION.json"
K3P_RESTORATION_MUTATIONS = K3P_RESTORATION_ROOT / "K3P_RESTORATION_MUTATION_CERTIFICATE.json"
K3P_RESTORATION_PRODUCER = K3P_RESTORATION_ROOT / "regenerate_k3p_restoration.py"


class ManifestFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ManifestFailure(message)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(PROJECT))


def sealed(value: dict) -> dict:
    result = dict(value)
    result["payload_sha256"] = sha(result)
    return result


def write_manifest(name: str, value: dict) -> None:
    (HERE / name).write_text(json.dumps(sealed(value), indent=2, sort_keys=True) + "\n")


def main() -> None:
    if not __debug__:
        raise ManifestFailure("OPTIMIZED_MODE_FORBIDDEN")
    certificate = json.loads(CERTIFICATE.read_text())
    replay = json.loads(REPLAY.read_text())
    mutations = json.loads(MUTATIONS.read_text())
    restoration = json.loads(RESTORATION.read_text())
    k3p_restoration = json.loads(K3P_RESTORATION_MANIFEST.read_text())
    k3p_restoration_replay = json.loads(K3P_RESTORATION_REPLAY.read_text())
    k3p_restoration_mutations = json.loads(K3P_RESTORATION_MUTATIONS.read_text())

    logical = dict(certificate)
    claimed = logical.pop("payload_sha256")
    require(claimed == sha(logical), "probe certificate payload")
    require(certificate["status"] == replay["status"] == mutations["status"] == "PASS", "probe gates")
    require(replay["source_certificate_sha256"] == sha_file(CERTIFICATE), "replay source binding")
    require(mutations["source_certificate_sha256"] == sha_file(CERTIFICATE), "mutation source binding")
    require(replay["source_payload_sha256"] == claimed, "replay logical binding")
    require(certificate["one_port"]["unresolved"] == certificate["two_port"]["unresolved"] == 0, "unresolved probes")
    require(certificate["assembly_theorem"]["incoherent"] == 0, "incoherent probes")
    require(k3p_restoration["status"] == "PASS", "K3P restoration manifest")
    require(k3p_restoration_replay["status"] == "PASS", "K3P restoration replay")
    require(k3p_restoration_mutations["status"] == "PASS", "K3P restoration mutations")
    require(k3p_restoration_replay["manifest_payload_sha256"] == k3p_restoration["payload_sha256"],
            "K3P restoration replay binding")
    require(k3p_restoration_mutations["manifest_payload_sha256"] == k3p_restoration["payload_sha256"],
            "K3P restoration mutation binding")
    require(k3p_restoration_mutations["mutation_count"] ==
            k3p_restoration_mutations["rejected"] == 20, "K3P restoration mutation census")
    require(k3p_restoration_mutations["accepted"] == 0, "accepted K3P restoration mutation")
    require(k3p_restoration_replay["uses_producer_code"] is False and
            k3p_restoration_replay["uses_k2p_sector_equality"] is False and
            k3p_restoration_replay["unresolved"] == 0,
            "K3P restoration replay independence boundary")
    require(k3p_restoration_mutations["verifier_sha256"] ==
            sha_file(K3P_RESTORATION_ROOT / "verify_k3p_restoration.py"),
            "K3P restoration mutation verifier binding")
    require(k3p_restoration["uses_historical_k2p_algebra"] is False and
            k3p_restoration["uses_k2p_sector_equality"] is False,
            "historical K2P restoration algebra forbidden")
    counts = k3p_restoration["census"]
    require(counts["minimal_k3p_terminal_rows"] == 36_568, "minimal K3P terminal count")
    require(counts["legacy_full_forest_leaves"] == 36_792, "legacy leaf count")
    require(counts["legacy_structural_continuations"] == 32, "legacy continuation count")
    require(counts["redundant_depth2_edges"] == 256, "redundant depth-two count")
    require(counts["active_k3p_continuations"] == 0, "active K3P continuation count")

    common = {
        "schema_version": 1,
        "model": "K3P",
        "domain": "D_{3,+}; graph coherence is also used in the strict-CT transfer",
        "producer": relative(HERE / "regenerate_k3p_probes.py"),
        "producer_sha256": sha_file(HERE / "regenerate_k3p_probes.py"),
        "certificate": relative(CERTIFICATE),
        "certificate_sha256": sha_file(CERTIFICATE),
        "certificate_payload_sha256": claimed,
        "independent_replay": relative(REPLAY),
        "independent_replay_sha256": sha_file(REPLAY),
        "mutation_certificate": relative(MUTATIONS),
        "mutation_certificate_sha256": sha_file(MUTATIONS),
    }

    write_manifest("RESTORATION_MANIFEST.json", {
        **common,
        "schema": "k3p-restoration-manifest-v2",
        "status": "PASS",
        "claim_boundary": (
            "The frozen fixed-full forest contributes only graph, parentage, repair-role, "
            "and exact graph-transport data. Complete replacement K3P algebra is "
            "independently certified by restoration/RESTORATION_MANIFEST.json. The active "
            "minimal K3P proof terminates all 36,568 first-layer rows; the 32 legacy "
            "continuations, 256 depth-two edges, and 36,792 legacy/full-forest leaves are "
            "retained only as a redundant structural replay. No historical K2P algebra is active."
        ),
        "frozen_graph_contract": relative(RESTORATION),
        "frozen_graph_contract_sha256": sha_file(RESTORATION),
        "graph_contract_census": restoration["census"],
        "scope_contract": restoration["scope_contract"],
        "cycles": restoration["census"]["cycles"],
        "missing_children": restoration["census"]["missing_children"],
        "unresolved_graph_rows": restoration["census"]["unresolved"],
        "k3p_algebra_status": "PASS_COMPLETE_INDEPENDENT_K3P_RESTORATION",
        "restoration_count_distinctions": {
            "minimal_k3p_terminal_rows": counts["minimal_k3p_terminal_rows"],
            "legacy_full_forest_leaves": counts["legacy_full_forest_leaves"],
            "legacy_structural_continuations": counts["legacy_structural_continuations"],
            "redundant_depth2_edges": counts["redundant_depth2_edges"],
            "active_k3p_continuations": counts["active_k3p_continuations"],
        },
        "standalone_k3p_restoration": {
            "manifest": {
                "path": relative(K3P_RESTORATION_MANIFEST),
                "sha256": sha_file(K3P_RESTORATION_MANIFEST),
                "payload_sha256": k3p_restoration["payload_sha256"],
                "status": k3p_restoration["status"],
            },
            "independent_replay": {
                "path": relative(K3P_RESTORATION_REPLAY),
                "sha256": sha_file(K3P_RESTORATION_REPLAY),
                "payload_sha256": k3p_restoration_replay["payload_sha256"],
                "status": k3p_restoration_replay["status"],
                "uses_producer_code": k3p_restoration_replay["uses_producer_code"],
            },
            "mutation_certificate": {
                "path": relative(K3P_RESTORATION_MUTATIONS),
                "sha256": sha_file(K3P_RESTORATION_MUTATIONS),
                "payload_sha256": k3p_restoration_mutations["payload_sha256"],
                "status": k3p_restoration_mutations["status"],
                "mutation_count": k3p_restoration_mutations["mutation_count"],
                "rejected": k3p_restoration_mutations["rejected"],
            },
            "producer": {
                "path": relative(K3P_RESTORATION_PRODUCER),
                "sha256": sha_file(K3P_RESTORATION_PRODUCER),
                "optimized_mode_forbidden": k3p_restoration["producer"]["optimized_mode_forbidden"],
            },
            "uses_historical_k2p_algebra": k3p_restoration["uses_historical_k2p_algebra"],
            "uses_k2p_sector_equality": k3p_restoration["uses_k2p_sector_equality"],
        },
    })

    one = certificate["one_port"]
    write_manifest("ONE_PORT_PROBE_MANIFEST.json", {
        **common,
        "schema": "k3p-one-port-probe-manifest-v1",
        "status": "PASS",
        "raw_pairs": one["raw_pairs"],
        "counts": one["counts"],
        "equality_survivors": one["equality_survivors"],
        "unresolved": one["unresolved"],
        "ledger": relative(HERE / "one_port_ledger.jsonl.gz"),
        "ledger_sha256": sha_file(HERE / "one_port_ledger.jsonl.gz"),
        "ordered_ledger": one["ordered_ledger"],
    })

    two = certificate["two_port"]
    write_manifest("TWO_PORT_PROBE_MANIFEST.json", {
        **common,
        "schema": "k3p-two-port-probe-manifest-v1",
        "status": "PASS",
        "parents": two["parents"],
        "raw_pairs": two["raw_pairs"],
        "counts": two["counts"],
        "equality_survivors": two["equality_survivors"],
        "reverse_order_parent_relation_counts": two["reverse_order_parent_relation_counts"],
        "unresolved": two["unresolved"],
        "parent_inventory": relative(HERE / "two_port_parent_inventory.jsonl.gz"),
        "parent_inventory_sha256": sha_file(HERE / "two_port_parent_inventory.jsonl.gz"),
        "ledger": relative(HERE / "two_port_ledger.jsonl.gz"),
        "ledger_sha256": sha_file(HERE / "two_port_ledger.jsonl.gz"),
        "ordered_parent_inventory": two["ordered_parent_inventory"],
        "ordered_ledger": two["ordered_ledger"],
    })

    transports = certificate["registries"]["exact_transports"]
    restrictions = certificate["registries"]["parent_restrictions"]
    assembly = certificate["assembly_theorem"]
    write_manifest("GLOBAL_TRANSPORT_MANIFEST.json", {
        **common,
        "schema": "k3p-global-transport-manifest-v1",
        "status": "PASS",
        "exact_transports": transports,
        "parent_restrictions": restrictions,
        "transport_ledger_sha256": sha_file(HERE / transports["path"]),
        "restriction_ledger_sha256": sha_file(HERE / restrictions["path"]),
        "triangle_anchors": assembly["one_global_triangle_gate"]["triangle_anchors"],
        "one_port_triangle_transports": assembly["one_global_triangle_gate"]["one_port_parents_inheriting_triangle"],
        "two_port_triangle_transports": assembly["one_global_triangle_gate"]["two_port_equalities_inheriting_triangle"],
        "new_triangles": assembly["one_global_triangle_gate"]["new_triangle_created_above_isomorphic_parent"],
        "incoherent": assembly["incoherent"],
        "unresolved": assembly["unresolved"],
    })

    print(json.dumps({
        "status": "PASS_WITH_COMPLETE_K3P_RESTORATION",
        "probe_payload_sha256": claimed,
        "manifests": [
            "RESTORATION_MANIFEST.json", "ONE_PORT_PROBE_MANIFEST.json",
            "TWO_PORT_PROBE_MANIFEST.json", "GLOBAL_TRANSPORT_MANIFEST.json",
        ],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ManifestFailure, KeyError, OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"K3P_PROBE_MANIFEST_FAIL:{error}") from error
