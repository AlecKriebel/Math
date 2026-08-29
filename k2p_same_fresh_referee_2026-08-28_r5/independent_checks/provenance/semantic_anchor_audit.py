#!/usr/bin/env python3
"""Independent semantic audit of printed artifact names and current hash prose."""

from __future__ import annotations

import argparse
import ast
import gzip
import hashlib
import json
import re
from pathlib import Path


HASH_RE = re.compile(r"[0-9a-f]{64}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def read_gzip_json(path: Path) -> object:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def source_lines(path: Path, first: int, last: int) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return lines[first - 1:last]


def hashes_in_lines(path: Path, first: int, last: int) -> list[str]:
    return HASH_RE.findall("\n".join(source_lines(path, first, last)))


def constant_from_python(path: Path, name: str) -> object:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == name for target in targets):
                return ast.literal_eval(node.value)
    raise KeyError(name)


def mismatch_rows(printed: list[str], expected: list[tuple[str, str]]) -> list[dict[str, object]]:
    if len(printed) != len(expected):
        raise RuntimeError(f"hash-count mismatch: printed={len(printed)} expected={len(expected)}")
    return [
        {
            "label": label,
            "printed": observed,
            "current": current,
            "matches": observed == current,
        }
        for observed, (label, current) in zip(printed, expected, strict=True)
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project.resolve()

    paths = {
        "supplement": root / "proof_compression_submission/supplement/supplement.tex",
        "static_auditor": root / "proof_compression_submission/adversarial_review/audit_article_sources.py",
        "readme": root / "work/corrected_composite_ledgers/README.md",
        "contract": root / "work/final_theorem_release/CORRECTED_FINITE_UNIVERSE_CONTRACT.md",
        "promotion": root / "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
        "lock": root / "work/final_theorem_release/RELEASE_LOCK.json",
        "history": root / "work/final_theorem_release/HISTORICAL_ARTIFACT_REGISTRY.json",
        "overlay": root / "work/raw4_sign_reclassification/raw4_corrected_terminal_ledger.json",
        "registry": root / "work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz",
        "raw_ledger": root / "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz",
        "raw_summary": root / "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_summary.json",
        "raw_replay": root / "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_independent_replay.json",
        "raw_mutation": root / "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_mutations.json",
        "theta_ledger": root / "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_ledger.jsonl.gz",
        "theta_summary": root / "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_summary.json",
        "theta_replay": root / "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_independent_replay.json",
        "theta_mutation": root / "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_mutations.json",
        "release_replay": root / "work/corrected_composite_ledgers/artifacts/release_contract_replay.json",
        "forest": root / "work/restoration_sign_reclassification/corrected_restoration_forest.json",
        "forest_replay": root / "work/restoration_sign_reclassification/corrected_restoration_replay_certificate.json",
    }

    raw_summary = read_json(paths["raw_summary"])
    raw_replay = read_json(paths["raw_replay"])
    raw_mutation = read_json(paths["raw_mutation"])
    theta_summary = read_json(paths["theta_summary"])
    theta_replay = read_json(paths["theta_replay"])
    theta_mutation = read_json(paths["theta_mutation"])
    release_replay = read_json(paths["release_replay"])
    forest = read_json(paths["forest"])
    forest_replay = read_json(paths["forest_replay"])
    overlay = read_json(paths["overlay"])
    registry = read_gzip_json(paths["registry"])

    current = {
        "raw ledger file": sha256(paths["raw_ledger"]),
        "raw summary payload": raw_summary["payload_sha256"],
        "raw replay payload": raw_replay["payload_sha256"],
        "raw mutation payload": raw_mutation["payload_sha256"],
        "theta ledger file": sha256(paths["theta_ledger"]),
        "theta summary payload": theta_summary["payload_sha256"],
        "theta replay payload": theta_replay["payload_sha256"],
        "theta mutation payload": theta_mutation["payload_sha256"],
        "release-contract replay payload": release_replay["payload_sha256"],
        "restoration forest file": sha256(paths["forest"]),
        "terminal registry file": sha256(paths["registry"]),
        "terminal registry payload": registry["payload_sha256"],
        "raw uncompressed stream": raw_summary["uncompressed_stream_sha256"],
    }

    readme_rows = mismatch_rows(
        hashes_in_lines(paths["readme"], 16, 22),
        [(key, current[key]) for key in (
            "raw ledger file", "raw summary payload", "raw replay payload",
            "raw mutation payload", "theta ledger file", "theta summary payload",
            "theta replay payload", "theta mutation payload",
            "release-contract replay payload",
        )],
    )
    readme_forest_rows = mismatch_rows(
        hashes_in_lines(paths["readme"], 38, 39),
        [("restoration forest file", current["restoration forest file"])],
    )
    readme_stream_rows = mismatch_rows(
        hashes_in_lines(paths["readme"], 95, 100),
        [
            ("raw uncompressed stream", current["raw uncompressed stream"]),
            ("theta uncompressed stream", theta_summary["uncompressed_stream_sha256"]),
        ],
    )
    contract_rows = mismatch_rows(
        hashes_in_lines(paths["contract"], 144, 181),
        [(key, current[key]) for key in (
            "raw ledger file", "raw summary payload", "raw replay payload",
            "raw mutation payload", "theta ledger file", "theta summary payload",
            "theta replay payload", "theta mutation payload", "terminal registry file",
            "release-contract replay payload",
        )],
    )

    static_anchors = constant_from_python(paths["static_auditor"], "PRINTED_FROZEN_ANCHORS")
    supplement_anchor = hashes_in_lines(paths["supplement"], 780, 781)
    if len(supplement_anchor) != 1:
        raise RuntimeError("expected exactly one supplement terminal-registry anchor")

    lock = read_json(paths["lock"])["files"]
    history = read_json(paths["history"])
    historical_paths = {row["path"] for row in history["artifacts"]}
    role_paths = [
        "work/corrected_composite_ledgers/README.md",
        "work/final_theorem_release/CORRECTED_FINITE_UNIVERSE_CONTRACT.md",
        "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
    ]

    promotion_expected = {
        912: (sha256(paths["raw_ledger"]), raw_summary["payload_sha256"]),
        913: (sha256(paths["raw_replay"]), raw_replay["payload_sha256"]),
        914: (sha256(paths["registry"]), registry["payload_sha256"]),
        915: (sha256(paths["raw_mutation"]), raw_mutation["payload_sha256"]),
        916: (sha256(paths["theta_ledger"]), theta_summary["payload_sha256"]),
        917: (sha256(paths["theta_replay"]), theta_replay["payload_sha256"]),
        918: (sha256(paths["theta_mutation"]), theta_mutation["payload_sha256"]),
        919: (sha256(paths["forest"]), forest["payload_sha256"]),
        920: (sha256(paths["forest_replay"]), forest_replay["payload_sha256"]),
    }
    promotion_rows = []
    promotion_text = paths["promotion"].read_text(encoding="utf-8").splitlines()
    for line, expected_pair in promotion_expected.items():
        observed = HASH_RE.findall(promotion_text[line - 1])
        if len(observed) != 2:
            raise RuntimeError(f"expected two hashes on promotion-manuscript line {line}")
        promotion_rows.append({
            "line": line,
            "printed_file": observed[0],
            "current_file": expected_pair[0],
            "file_matches": observed[0] == expected_pair[0],
            "printed_payload": observed[1],
            "current_payload": expected_pair[1],
            "payload_matches": observed[1] == expected_pair[1],
        })

    result: dict[str, object] = {
        "schema": "k2p-independent-semantic-anchor-audit-v1",
        "status": "FAIL",
        "supplement_terminal_registry": {
            "source_lines": [780, 781],
            "printed_label": "raw-four terminal registry",
            "printed_sha256": supplement_anchor[0],
            "static_auditor_mapped_path": static_anchors["raw-four terminal registry"],
            "mapped_artifact_sha256": sha256(paths["overlay"]),
            "mapped_artifact_schema": overlay["schema"],
            "mapped_artifact_rows": overlay["corrected_rows"],
            "actual_registry_path": str(paths["registry"].relative_to(root)),
            "actual_registry_sha256": sha256(paths["registry"]),
            "actual_registry_schema": registry["schema"],
            "actual_registry_terminal_class_count": registry["terminal_class_count"],
            "semantic_label_matches_mapped_artifact": False,
        },
        "stale_current_language": {
            "corrected_composite_readme_lines_16_22": readme_rows,
            "corrected_composite_readme_lines_38_39": readme_forest_rows,
            "corrected_composite_readme_lines_95_100": readme_stream_rows,
            "corrected_finite_universe_contract_lines_144_181": contract_rows,
            "promotion_manifest_lines_912_920": promotion_rows,
        },
        "authority_classification": {
            path: {
                "release_lock": lock[path],
                "historical_registry_member": path in historical_paths,
            }
            for path in role_paths
        },
        "current_values": current,
    }
    result["mismatch_count"] = (
        sum(not row["matches"] for row in readme_rows + readme_forest_rows + readme_stream_rows + contract_rows)
        + sum((not row["file_matches"]) + (not row["payload_matches"]) for row in promotion_rows)
        + 1
    )
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "mismatch_count": result["mismatch_count"],
        "payload_sha256": result["payload_sha256"],
    }, sort_keys=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
