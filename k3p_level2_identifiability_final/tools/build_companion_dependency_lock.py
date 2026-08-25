#!/usr/bin/env python3
"""Lock the imported model-independent JC/K2P topology dependencies."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMPORT = ROOT / "input_frozen/model_independent_topology_package"
UPSTREAM_ROOT = "k2p_level2_identifiability_closure"
UPSTREAM_COMMIT = "962c707c1cf70c8a188481a1e666e16849b0e399"
CREATED_AT = "2026-08-24T21:44:00-07:00"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def role(rel: str) -> tuple[str, str]:
    name = Path(rel).name
    if rel.startswith("atlas/"):
        return (
            "graph construction, restriction, mixed-graph, and topology reference compiler",
            "topology routines may be reused; K2P algebra is reference-only",
        )
    if rel.startswith("cycle/"):
        return (
            "cycle restoration and physical-anchor reconstruction dependency",
            "graph/topology evidence only until rechecked under the K3P active atlas",
        )
    if rel.startswith("anchor_inputs/"):
        return (
            "frozen restoration/probe anchor or parentage input",
            "model-independent graph evidence; every algebraic edge must be rebound to K3P",
        )
    if name in {
        "one_port_ledger.jsonl.gz",
        "two_port_ledger.jsonl.gz",
        "two_port_parent_inventory.jsonl.gz",
        "exact_transport_ledger.jsonl.gz",
        "parent_restriction_ledger.jsonl.gz",
    }:
        return (
            "completed K2P topology/transport ledger used as a regeneration cross-check",
            "relation, parentage, and transport rows only; K2P separators are not K3P evidence",
        )
    return (
        "completed K2P probe implementation or algebraic reference",
        "reference-only until independently regenerated and K3P-rebound",
    )


def upstream_path(rel: str) -> str:
    name = Path(rel).name
    if rel == "atlas/k2p_atlas_core.py":
        suffix = "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
    elif rel.startswith("cycle/"):
        if name in {"physical_anchors.json"}:
            suffix = f"work/cycle_three_port_closure/artifacts/{name}"
        elif name == "cycle_promotion_certificate.json":
            suffix = f"work/cycle_three_port_closure/promotion/{name}"
        else:
            suffix = f"work/cycle_three_port_closure/{name}"
    elif rel.startswith("anchor_inputs/"):
        mapping = {
            "probe_input_contract.json": "work/adversarial_proof_review/probe_input_contract.json",
            "probe_input_independent_verification.json": "work/adversarial_proof_review/probe_input_independent_verification.json",
            "probe_input_mutation_certificate.json": "work/adversarial_proof_review/probe_input_mutation_certificate.json",
            "corrected_restoration_forest.json": "work/restoration_sign_reclassification/corrected_restoration_forest.json",
            "raw_directional_ledger.jsonl.gz": "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz",
            "fixed_full_restoration_closure.json.gz": "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz",
        }
        suffix = mapping[name]
    else:
        suffix = f"work/probe_coherence_corrected/{name}"
    return f"{UPSTREAM_ROOT}/{suffix}"


def main() -> None:
    paths = sorted(path for path in IMPORT.rglob("*") if path.is_file())
    if len(paths) != 28:
        raise SystemExit(f"expected 28 imported companion files, found {len(paths)}")
    records = []
    for number, path in enumerate(paths, 1):
        rel = path.relative_to(IMPORT).as_posix()
        claimed_role, boundary = role(rel)
        records.append(
            {
                "record_id": f"companion-{number:03d}",
                "path": f"input_frozen/model_independent_topology_package/{rel}",
                "upstream_repository_path": upstream_path(rel),
                "byte_size": path.stat().st_size,
                "sha256": digest(path),
                "claimed_role": claimed_role,
                "activation_boundary": boundary,
                "status": "frozen_companion_dependency_pending_k3p_rebind",
            }
        )
    payload = {
        "schema_version": 1,
        "created_at": CREATED_AT,
        "upstream_repository_snapshot_commit": UPSTREAM_COMMIT,
        "source_files_confirmed_clean_at_import": True,
        "record_count": len(records),
        "records": records,
        "global_boundary": (
            "No K2P polynomial, rank, sign, or model-specific conclusion is active K3P "
            "evidence. Only independently replayed graph construction, restoration, "
            "parentage, exact labelled transport, and triangle-coherence facts may be promoted."
        ),
    }
    (ROOT / "COMPANION_DEPENDENCY_LOCK.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# Companion topology dependency lock",
        "",
        f"Imported from clean repository snapshot `{UPSTREAM_COMMIT}`.",
        "",
        "K2P algebra is reference-only.  Promotion is limited to independently",
        "replayed graph/restoration/parentage/transport facts and requires a K3P",
        "three-sector rebind.",
        "",
        "| ID | Project path | Bytes | SHA-256 | Role | Activation boundary | Status |",
        "|---|---|---:|---|---|---|---|",
    ]
    for record in records:
        lines.append(
            "| "
            + " | ".join(
                [
                    record["record_id"],
                    f"`{record['path']}`",
                    str(record["byte_size"]),
                    f"`{record['sha256']}`",
                    record["claimed_role"],
                    record["activation_boundary"],
                    record["status"],
                ]
            )
            + " |"
        )
    (ROOT / "COMPANION_DEPENDENCY_LOCK.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    checksum = [
        f"{record['sha256']}  {record['path']}" for record in records
    ]
    (ROOT / "COMPANION_SHA256SUMS").write_text(
        "\n".join(checksum) + "\n", encoding="utf-8"
    )
    print(f"COMPANION_DEPENDENCY_LOCK_OK records={len(records)}")


if __name__ == "__main__":
    main()

