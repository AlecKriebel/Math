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

    logical = dict(certificate)
    claimed = logical.pop("payload_sha256")
    require(claimed == sha(logical), "probe certificate payload")
    require(certificate["status"] == replay["status"] == mutations["status"] == "PASS", "probe gates")
    require(replay["source_certificate_sha256"] == sha_file(CERTIFICATE), "replay source binding")
    require(mutations["source_certificate_sha256"] == sha_file(CERTIFICATE), "mutation source binding")
    require(replay["source_payload_sha256"] == claimed, "replay logical binding")
    require(certificate["one_port"]["unresolved"] == certificate["two_port"]["unresolved"] == 0, "unresolved probes")
    require(certificate["assembly_theorem"]["incoherent"] == 0, "incoherent probes")

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
        "schema": "k3p-restoration-manifest-v1",
        "status": "GRAPH_CONTRACT_PASS_K3P_ALGEBRA_PENDING",
        "claim_boundary": (
            "Only the fixed-full restoration forest's graph, parentage, repair-role, "
            "and exact graph-transport data are active here. Its K2P sign/rank "
            "certificates are excluded until separately replaced by K3P evidence."
        ),
        "frozen_graph_contract": relative(RESTORATION),
        "frozen_graph_contract_sha256": sha_file(RESTORATION),
        "graph_contract_census": restoration["census"],
        "scope_contract": restoration["scope_contract"],
        "cycles": restoration["census"]["cycles"],
        "missing_children": restoration["census"]["missing_children"],
        "unresolved_graph_rows": restoration["census"]["unresolved"],
        "k3p_algebra_status": "PENDING_INDEPENDENT_RESTORATION_AUDIT",
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
        "status": "PASS_WITH_RESTORATION_K3P_ALGEBRA_PENDING",
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
