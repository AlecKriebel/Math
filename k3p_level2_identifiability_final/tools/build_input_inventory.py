#!/usr/bin/env python3
"""Build deterministic frozen-input inventories and the bootstrap manifest."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "input_frozen"
BASE_COMMIT = "ac6b38a9f8f44dd777f671768f012dfc00e02d1b"
CREATED_AT = "2026-08-24T21:22:05-07:00"

ORIGINAL_NAMES = {
    "referenced_chat_manuscripts/jc_level2_source.tex": "main(20260824-043107)(1).tex",
    "referenced_chat_manuscripts/k2p_level2_source.tex": "main(10)(1).tex",
    "referenced_chat_manuscripts/tree_theta_collision_source.tex": "combined-paper-clarified (1).tex",
    "specification/AUTONOMOUS_FINAL_PROGRAM.txt": "pasted-text.txt",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def role_for(rel: str) -> str:
    name = Path(rel).name.lower()
    if rel.startswith("specification/"):
        return "user-supplied final certification, paper, and release specification"
    if rel.startswith("referenced_chat_manuscripts/"):
        if name.startswith("jc_"):
            return "completed JC level-2 companion manuscript"
        if name.startswith("k2p_"):
            return "completed K2P level-2 companion manuscript"
        return "exact K2P/K3P tree--theta collision manuscript"
    if "14_orbit_lock" in name:
        return "locked four-port graph-relation universe and orbit assignments"
    if "14_orbit_final_manifest" in name:
        return "cloud-stage fourteen-orbit active manifest"
    if "14_orbit_classification" in name or "14_orbit_table" in name:
        return "human-readable fourteen-orbit classification"
    if "krawczyk" in name:
        return "weak-class rigorous common-point interval certificate or verifier"
    if "sharpness" in name:
        return "weak-class base-map, all-n extension, or verifier"
    if "three_sunlet_quartic" in name:
        return "ordinary-triangle H14 quartic certificate"
    if "tree_sunlet_separator" in name:
        return "tree versus ordinary-sunlet exact separator or verifier"
    if "three_port_ranks" in name or "three_port_geometry" in name:
        return "three-port exact rank evidence or verifier"
    if "directed_rank" in name:
        return "directed-rank obstruction certificates"
    if "quartic" in name:
        return "exact polynomial separator certificate"
    if "rooting_cens" in name:
        return "rooting census certificate or verifier"
    if "model_domain_bridge" in name:
        return "K3P domain and bridge-fibre certificate or verifier"
    if "cut_transfer" in name:
        return "pointwise cut-transfer certificate or verifier"
    if "compiler_specialization" in name:
        return "K3P-to-K2P compiler-specialization replay"
    if "atlas_core" in name:
        return "primary graph-derived K3P atlas compiler"
    if "cleanroom" in name:
        return "independent fourteen-orbit clean-room verifier"
    if "fourteen_orbits" in name:
        return "primary fourteen-orbit verifier"
    if "source_ranks" in name:
        return "exact four-port source-rank certificates"
    return "supplied cloud-stage K3P proof artifact"


def source_group(rel: str) -> str:
    if rel.startswith("k3p_cloud_artifacts/"):
        return "K3P cloud-stage completion package"
    if rel.startswith("referenced_chat_manuscripts/"):
        return "referenced ChatGPT task manuscript attachment"
    return "current-task user specification attachment"


def original_path(rel: str, original_name: str) -> str:
    if rel.startswith("k3p_cloud_artifacts/"):
        return f"/Users/alec/Desktop/k3p/{original_name}"
    if rel.startswith("specification/"):
        return "/Users/alec/.codex/attachments/e797165d-2264-42ed-b132-621c3ba01ccc/pasted-text.txt"
    return "referenced ChatGPT task temporary attachment (copied before lock)"


def json_summary(path: Path) -> tuple[str, dict[str, Any]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # fail visibly in inventory, not silently
        return f"invalid JSON: {type(exc).__name__}: {exc}", {}
    if isinstance(value, dict):
        keys = sorted(value)[:30]
        summary = f"JSON object; top-level keys={keys}"
        provenance = {
            key: value[key]
            for key in sorted(value)
            if any(token in key.lower() for token in ("provenance", "created", "stage", "version", "status"))
            and isinstance(value[key], (str, int, float, bool, type(None)))
        }
        return summary, provenance
    if isinstance(value, list):
        return f"JSON array; length={len(value)}", {}
    return f"JSON scalar; type={type(value).__name__}", {}


def python_summary(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return f"Python source with syntax error at line {exc.lineno}: {exc.msg}"
    functions = [node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    classes = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
    return f"Python source; functions={functions[:30]}; classes={classes[:20]}"


def latex_summary(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    title = re.search(r"\\title\{(.{0,500}?)\}\s*\\author", text, re.DOTALL)
    title_text = " ".join(title.group(1).replace("\\\\", " ").split()) if title else "title not detected"
    return f"LaTeX manuscript; {title_text}"


def detect(path: Path) -> tuple[str, dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        summary, provenance = json_summary(path)
        return summary, provenance
    if suffix == ".py":
        return python_summary(path), {}
    if suffix == ".tex":
        return latex_summary(path), {}
    text = path.read_text(encoding="utf-8", errors="replace")
    first = next((line.strip() for line in text.splitlines() if line.strip()), "empty text file")
    return f"text document; first nonblank line={first[:240]!r}", {}


def archive_type(path: Path) -> str:
    return {
        ".json": "plain JSON file",
        ".py": "plain Python source file",
        ".md": "plain Markdown file",
        ".tex": "plain LaTeX source file",
        ".txt": "plain text file",
    }.get(path.suffix.lower(), "plain file")


def build_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    attachment_roots = (
        FROZEN / "k3p_cloud_artifacts",
        FROZEN / "referenced_chat_manuscripts",
        FROZEN / "specification",
    )
    for path in sorted(
        p for base in attachment_roots for p in base.rglob("*") if p.is_file()
    ):
        rel = path.relative_to(FROZEN).as_posix()
        original_name = ORIGINAL_NAMES.get(rel, path.name)
        detected, encoded_provenance = detect(path)
        records.append(
            {
                "record_id": f"input-{len(records)+1:03d}",
                "original_filename": original_name,
                "original_local_path": original_path(rel, original_name),
                "frozen_local_path": f"input_frozen/{rel}",
                "byte_size": path.stat().st_size,
                "sha256": sha256(path),
                "archive_type": archive_type(path),
                "claimed_role": role_for(rel),
                "detected_contents": detected,
                "source_manuscript_or_package": source_group(rel),
                "cloud_stage_provenance_if_encoded": encoded_provenance or None,
                "status": "frozen_input_unverified",
            }
        )
    return records


def write_inventory(records: list[dict[str, Any]]) -> None:
    payload = {
        "schema_version": 1,
        "generated_at": CREATED_AT,
        "project_root": ".",
        "record_count": len(records),
        "records": records,
    }
    (ROOT / "LOCAL_INPUT_INVENTORY.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# Local input inventory",
        "",
        f"Generated at `{CREATED_AT}`. Frozen input count: **{len(records)}**.",
        "",
        "All statuses are `frozen_input_unverified` until an active verifier promotes",
        "the corresponding mathematical claim.",
        "",
        "| ID | Frozen path | Bytes | SHA-256 | Type | Claimed role | Detected contents | Source | Provenance | Status |",
        "|---|---|---:|---|---|---|---|---|---|---|",
    ]
    for rec in records:
        cells = [
            rec["record_id"],
            f"`{rec['frozen_local_path']}`",
            str(rec["byte_size"]),
            f"`{rec['sha256']}`",
            rec["archive_type"],
            rec["claimed_role"],
            rec["detected_contents"],
            rec["source_manuscript_or_package"],
            json.dumps(rec["cloud_stage_provenance_if_encoded"], sort_keys=True),
            rec["status"],
        ]
        lines.append("| " + " | ".join(cell.replace("|", "\\|").replace("\n", " ") for cell in cells) + " |")
    (ROOT / "LOCAL_INPUT_INVENTORY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_locks(records: list[dict[str, Any]]) -> None:
    lock = {
        "schema_version": 1,
        "created_at": CREATED_AT,
        "base_branch": "main",
        "base_commit": BASE_COMMIT,
        "origin_main_equal_at_creation": True,
        "frozen_input_count": len(records),
        "frozen_inputs": [
            {
                "record_id": rec["record_id"],
                "path": rec["frozen_local_path"],
                "byte_size": rec["byte_size"],
                "sha256": rec["sha256"],
            }
            for rec in records
        ],
    }
    (ROOT / "INPUT_LOCK.json").write_text(
        json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    # The root checksum list covers every frozen file, including separately
    # locked companion dependencies.  The attachment inventory itself remains
    # the exact 36-file initial corpus.
    hash_paths = sorted(path for path in FROZEN.rglob("*") if path.is_file())
    hash_paths.extend([ROOT / "FINAL_CLAIM_LOCK.json", ROOT / "FINAL_CLAIM_LOCK.md"])
    checksum_lines = [
        f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in sorted(hash_paths)
    ]
    (ROOT / "SHA256SUMS").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

    manifest = {
        "schema_version": 1,
        "manifest_version": "0.1.0-bootstrap",
        "status": "bootstrap_pending_exact_replay",
        "base_commit": BASE_COMMIT,
        "active_inputs": [rec["record_id"] for rec in records],
        "input_inventory": "LOCAL_INPUT_INVENTORY.json",
        "input_lock": "INPUT_LOCK.json",
        "claim_locks": ["FINAL_CLAIM_LOCK.json", "FINAL_CLAIM_LOCK.md"],
        "active_theorem_artifacts": [],
        "active_verifiers": [],
        "excluded_evidence_root": "history/",
        "certification_gates_passed": [],
    }
    (ROOT / "ACTIVE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> None:
    records = build_records()
    if len(records) != 36:
        raise SystemExit(f"expected exactly 36 frozen inputs, found {len(records)}")
    write_inventory(records)
    write_locks(records)
    print(f"FROZEN_INPUT_INVENTORY_OK records={len(records)}")


if __name__ == "__main__":
    main()
