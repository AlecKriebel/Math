#!/usr/bin/env python3
"""Independently test the R5 semantic-anchor and stale-table repairs."""

from __future__ import annotations

import argparse
import ast
import gzip
import hashlib
import json
import re
from pathlib import Path


HASH = re.compile(r"[0-9a-f]{64}")
REGISTRY_LABEL = "raw-four 934-class terminal certificate registry"
REGISTRY_PATH = "work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz"
OVERLAY_PATH = "work/raw4_sign_reclassification/raw4_corrected_terminal_ledger.json"


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise RuntimeError(code if detail is None else f"{code}:{detail}")


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            value = json.load(handle)
    else:
        value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "NOT_OBJECT", path)
    return value


def constant(path: Path, name: str) -> object:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == name for target in targets):
                return ast.literal_eval(node.value)
    raise RuntimeError(f"missing constant: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project.resolve()
    supplement_path = root / "proof_compression_submission/supplement/supplement.tex"
    auditor_path = root / "proof_compression_submission/adversarial_review/audit_article_sources.py"
    static_path = root / "proof_compression_submission/adversarial_review/STATIC_AUDIT_RESULT.json"
    readme_path = root / "work/corrected_composite_ledgers/README.md"
    contract_path = root / "work/final_theorem_release/CORRECTED_FINITE_UNIVERSE_CONTRACT.md"
    promotion_path = root / "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md"
    lock = load(root / "work/final_theorem_release/RELEASE_LOCK.json")["files"]
    portable = load(root / "output/referee/REFEREE_BUNDLE_CONTENTS.json")["files"]
    history_path = root / "work/final_theorem_release/HISTORICAL_ARTIFACT_REGISTRY.json"
    history = load(history_path)

    registry = load(root / REGISTRY_PATH)
    overlay = load(root / OVERLAY_PATH)
    registry_sha = sha(root / REGISTRY_PATH)
    overlay_sha = sha(root / OVERLAY_PATH)
    require(registry.get("schema") == "k2p-raw4-terminal-certificate-registry-v1", "REGISTRY_SCHEMA")
    require(registry.get("terminal_class_count") == 934, "REGISTRY_COUNT")
    require(overlay.get("schema") == "k2p-raw4-corrected-terminal-overlay-v2", "OVERLAY_SCHEMA")
    require(overlay.get("corrected_rows") == 16974, "OVERLAY_COUNT")
    require(registry_sha != overlay_sha, "REGISTRY_OVERLAY_COLLISION")

    supplement = supplement_path.read_text(encoding="utf-8")
    row_match = re.search(
        re.escape(REGISTRY_LABEL) + r"\s*&\s*\\hashvalue\{([0-9a-f]{64})\}\\\\",
        supplement,
    )
    require(row_match is not None and row_match.group(1) == registry_sha, "SUPPLEMENT_REGISTRY_ROW")
    require(
        REGISTRY_PATH in supplement
        and "k2p-raw4-terminal-certificate-registry-v1" in supplement
        and r"terminal\_class\_count}=934" in supplement
        and "16,974-row strict-sign overlay" in supplement,
        "SUPPLEMENT_TYPED_EXPLANATION",
    )

    anchors = constant(auditor_path, "PRINTED_FROZEN_ANCHORS")
    types = constant(auditor_path, "PRINTED_FROZEN_ANCHOR_TYPES")
    require(isinstance(anchors, dict) and anchors.get(REGISTRY_LABEL) == REGISTRY_PATH, "AUDITOR_REGISTRY_MAPPING")
    require(
        isinstance(types, dict)
        and types.get(REGISTRY_LABEL) == {
            "schema": "k2p-raw4-terminal-certificate-registry-v1",
            "count_field": "terminal_class_count", "count": 934,
        },
        "AUDITOR_TYPED_CONTRACT",
    )
    static = load(static_path)
    typed_rows = [
        row for row in static["printed_authority_hash_binding"]["rows"]
        if isinstance(row, dict) and row.get("label") == REGISTRY_LABEL
    ]
    require(
        len(typed_rows) == 1 and typed_rows[0].get("path") == REGISTRY_PATH
        and typed_rows[0].get("sha256") == registry_sha
        and typed_rows[0].get("declared_schema") == registry["schema"]
        and typed_rows[0].get("semantic_count") == 934,
        "STATIC_TYPED_RESULT",
    )

    artifacts = {
        "Domain, subdivision, rooting": "work/domain_rooting_closure/domain_rooting_certificate.json",
        "Two-sector bridge and marginal": "work/bridge_marginal_closure/certificate.json",
        "Independent component-scale audit": "work/global_proof_adversary/component_scale_certificate.json",
        "Raw four-port composite ledger": "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz",
        "Raw four-port independent replay": "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_independent_replay.json",
        "Raw four-port terminal registry": REGISTRY_PATH,
        "Raw four-port mutation report": "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_mutations.json",
        r"Five-port \(\theta_2\) composite ledger": "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_ledger.jsonl.gz",
        r"Five-port \(\theta_2\) independent replay": "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_independent_replay.json",
        r"Five-port \(\theta_2\) mutation report": "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_mutations.json",
        "Corrected 997-parent restoration forest": "work/restoration_sign_reclassification/corrected_restoration_forest.json",
        "Restoration independent replay": "work/restoration_sign_reclassification/corrected_restoration_replay_certificate.json",
        "Authoritative cycle promotion": "work/cycle_three_port_closure/promotion/cycle_promotion_certificate.json",
        "Ordinary-triangle common germ": "work/final_theorem_release/triangle_sunlet_certificate.json",
        "Frozen probe-input contract": "work/adversarial_proof_review/probe_input_contract.json",
        "Independent probe-input replay": "work/global_proof_adversary/probe_full_audit/primitive_anchor_replay.json",
        "Corrected full probe primary": "work/probe_coherence_corrected/probe_coherence_certificate.json",
        "Independent primitive/graph/full-map probe audit": "work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit_certificate.json",
        "Independent probe mutation report": "work/global_proof_adversary/probe_full_audit/independent_probe_mutation_report.json",
        "Independent structural/algebra probe replay": "work/probe_coherence_corrected/probe_coherence_independent_verification.json",
        "Independent site-transport partition replay": "work/probe_coherence_corrected/site_transport_partition_verification.json",
        "Weak-sharpness primary": "work/weak_sharpness_closure/weak_sharpness_certificate.json",
        "Weak-sharpness independent audit": "work/weak_sharpness_audit/audit_certificate.json",
    }
    payload_sources = dict(artifacts)
    payload_sources["Raw four-port composite ledger"] = "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_summary.json"
    payload_sources[r"Five-port \(\theta_2\) composite ledger"] = "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_summary.json"
    promotion_rows: list[dict[str, object]] = []
    parsed: dict[str, tuple[str, str, int]] = {}
    for number, line in enumerate(promotion_path.read_text(encoding="utf-8").splitlines(), 1):
        match = re.fullmatch(r"\| ([^|]+?) \| `([0-9a-f]{64})` \| `([0-9a-f]{64})`(?: \([^)]*\))? \|", line)
        if match and match.group(1) in artifacts:
            parsed[match.group(1)] = (match.group(2), match.group(3), number)
    require(set(parsed) == set(artifacts), "PROMOTION_ROW_INVENTORY", sorted(set(artifacts) - set(parsed)))
    for label, relative in artifacts.items():
        printed_file, printed_payload, line = parsed[label]
        actual_file = sha(root / relative)
        source = load(root / payload_sources[label])
        actual_payload = source.get("payload_sha256")
        require(printed_file == actual_file, "PROMOTION_FILE_STALE", label)
        require(printed_payload == actual_payload, "PROMOTION_PAYLOAD_STALE", label)
        require(relative in portable and portable[relative]["sha256"] == actual_file, "PROMOTION_NOT_FROZEN", relative)
        promotion_rows.append({"label": label, "line": line, "path": relative, "sha256": actual_file, "payload_sha256": actual_payload})

    raw_summary = load(root / payload_sources["Raw four-port composite ledger"])
    theta_summary = load(root / payload_sources[r"Five-port \(\theta_2\) composite ledger"])
    release_replay = load(root / "work/corrected_composite_ledgers/artifacts/release_contract_replay.json")
    key_values = {
        "raw_ledger_sha256": sha(root / artifacts["Raw four-port composite ledger"]),
        "raw_summary_payload": raw_summary["payload_sha256"],
        "raw_replay_payload": load(root / artifacts["Raw four-port independent replay"])["payload_sha256"],
        "raw_mutation_payload": load(root / artifacts["Raw four-port mutation report"])["payload_sha256"],
        "theta_ledger_sha256": sha(root / artifacts[r"Five-port \(\theta_2\) composite ledger"]),
        "theta_summary_payload": theta_summary["payload_sha256"],
        "theta_replay_payload": load(root / artifacts[r"Five-port \(\theta_2\) independent replay"])["payload_sha256"],
        "theta_mutation_payload": load(root / artifacts[r"Five-port \(\theta_2\) mutation report"])["payload_sha256"],
        "release_replay_payload": release_replay["payload_sha256"],
        "forest_sha256": sha(root / artifacts["Corrected 997-parent restoration forest"]),
        "registry_sha256": registry_sha,
        "raw_stream_sha256": raw_summary["uncompressed_stream_sha256"],
        "theta_stream_sha256": theta_summary["uncompressed_stream_sha256"],
    }
    readme = readme_path.read_text(encoding="utf-8")
    contract = contract_path.read_text(encoding="utf-8")
    for key, value in key_values.items():
        target = contract if key == "registry_sha256" else readme
        require(str(value) in target, "CURRENT_NARRATIVE_VALUE_MISSING", key)
    for value in (
        key_values["raw_ledger_sha256"], key_values["raw_summary_payload"],
        key_values["raw_replay_payload"], key_values["raw_mutation_payload"],
        key_values["theta_ledger_sha256"], key_values["theta_summary_payload"],
        key_values["theta_replay_payload"], key_values["theta_mutation_payload"],
        key_values["release_replay_payload"], key_values["registry_sha256"],
    ):
        require(str(value) in contract, "CONTRACT_CURRENT_VALUE_MISSING", value)

    role_paths = [
        "work/corrected_composite_ledgers/README.md",
        "work/final_theorem_release/CORRECTED_FINITE_UNIVERSE_CONTRACT.md",
        "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
    ]
    roles = []
    for relative in role_paths:
        text = (root / relative).read_text(encoding="utf-8")
        require(
            "reader snapshot only" in text
            and "work/final_theorem_release/RELEASE_LOCK.json" in text
            and "does not supersede that lock" in text,
            "ROLE_MARKER", relative,
        )
        require(relative in lock and lock[relative]["sha256"] == sha(root / relative), "ROLE_LOCK_BINDING", relative)
        roles.append({"path": relative, "sha256": sha(root / relative), "classification": "current lock-bound reader snapshot; generated lock is byte authority"})

    historical_rows = history.get("artifacts")
    require(isinstance(historical_rows, list) and len(historical_rows) == 8, "HISTORICAL_INVENTORY")
    historical_paths = set()
    historical_classifications: dict[str, int] = {}
    for item in historical_rows:
        require(isinstance(item, dict) and isinstance(item.get("path"), str), "HISTORICAL_ROW")
        relative = item["path"]
        historical_paths.add(relative)
        require(item.get("promotion_authority") is False, "HISTORICAL_PROMOTED", relative)
        require(relative in portable and portable[relative]["sha256"] == item.get("sha256"), "HISTORICAL_HASH", relative)
        classification = item.get("classification")
        require(
            isinstance(classification, str)
            and classification.startswith(("REVOKED_", "HISTORICAL_", "SUPERSEDED_")),
            "HISTORICAL_CLASSIFICATION", relative,
        )
        historical_classifications[classification] = historical_classifications.get(classification, 0) + 1
        replacements = item.get("authoritative_replacements")
        require(isinstance(replacements, list) and replacements, "HISTORICAL_REPLACEMENT", relative)
        require(all(isinstance(x, str) and x in portable for x in replacements), "HISTORICAL_REPLACEMENT_UNBOUND", relative)
    require(not (historical_paths & set(role_paths)), "CURRENT_NARRATIVE_MISCLASSIFIED_HISTORICAL")

    crosswalk = load(root / "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json")
    promotion_roles = []
    for claim in crosswalk.get("claims", []):
        for field in ("authoritative_artifacts", "producer_artifacts", "replay_artifacts", "mutation_artifacts"):
            for item in claim.get(field, []):
                if item.get("path") == role_paths[2]:
                    promotion_roles.append(item.get("role"))
    require(
        promotion_roles and all("not current submission proof authority" in str(role) for role in promotion_roles),
        "PROMOTION_MANUSCRIPT_ROLE_DRIFT",
    )

    result: dict[str, object] = {
        "schema": "k2p-r6-semantic-repair-audit-v1", "status": "PASS",
        "r5_terminal_anchor_repair": {
            "label": REGISTRY_LABEL, "path": REGISTRY_PATH, "sha256": registry_sha,
            "schema": registry["schema"], "terminal_class_count": registry["terminal_class_count"],
            "overlay_path": OVERLAY_PATH, "overlay_sha256": overlay_sha,
            "overlay_schema": overlay["schema"], "overlay_rows": overlay["corrected_rows"],
            "supplement_row_correct": True, "auditor_mapping_correct": True,
            "typed_schema_and_cardinality_gate_present": True,
        },
        "promotion_snapshot_rows": promotion_rows,
        "promotion_snapshot_row_count": len(promotion_rows),
        "current_narrative_values": key_values,
        "current_narrative_roles": roles,
        "historical_registry": {
            "path": str(history_path.relative_to(root)), "sha256": sha(history_path),
            "artifact_count": len(historical_rows),
            "classifications": dict(sorted(historical_classifications.items())),
            "current_narratives_excluded": True,
        },
        "promotion_manuscript_crosswalk_roles": promotion_roles,
        "mismatch_count": 0,
    }
    result["payload_sha256"] = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "mismatch_count": 0, "promotion_rows": len(promotion_rows), "payload_sha256": result["payload_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, sort_keys=True))
        raise SystemExit(1) from error
