#!/usr/bin/env python3
"""Fail-closed integrity and finite-universe summary verifier."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re

import evidence_bindings


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def payload_commitment(records: dict[str, tuple[int, int, str]]) -> str:
    """Recompute the clean-source payload commitment recorded at sealing."""
    commitment = hashlib.sha256()
    for relative, (size, executable_bits, digest) in sorted(records.items()):
        commitment.update(relative.encode("utf-8") + b"\0")
        commitment.update(str(size).encode("ascii") + b"\0")
        commitment.update(f"{executable_bits:o}".encode("ascii") + b"\0")
        commitment.update(digest.encode("ascii") + b"\n")
    return commitment.hexdigest()


def verify_manifest(root: Path) -> dict:
    payload = json.loads((root / "ACTIVE_MANIFEST.json").read_text())
    require(payload["schema"] == "stc-jc-proof-bundle-manifest-v1", "manifest schema")
    require(payload.get("source_tree_clean") is True,
            "bundle was not sealed from a clean source tree")
    require(re.fullmatch(r"[0-9a-f]{40}", str(payload.get("source_commit", "")))
            is not None, "bundle source commit is not an exact Git object")
    require(re.fullmatch(r"[0-9a-f]{64}",
                         str(payload.get("prepared_payload_sha256", "")))
            is not None, "clean-source prepared payload commitment is absent")
    file_rows = payload["files"]
    manifest_paths = [row["path"] for row in file_rows]
    require(len(manifest_paths) == len(set(manifest_paths)),
            "duplicate path in ACTIVE_MANIFEST.json")
    expected = {row["path"]: row for row in file_rows}
    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
        and path.name not in {"ACTIVE_MANIFEST.json", "SHA256SUMS"}
        and "__pycache__" not in path.parts
        and ".venv" not in path.parts
    }
    require(set(expected) == actual,
            f"manifest path mismatch: missing={sorted(set(expected)-actual)[:5]}, "
            f"unexpected={sorted(actual-set(expected))[:5]}")
    for relative, row in expected.items():
        path = root / relative
        require(path.stat().st_size == row["bytes"], f"size mismatch: {relative}")
        require(sha256(path) == row["sha256"], f"hash mismatch: {relative}")
        require(isinstance(row.get("executable_bits"), int),
                f"missing executable-mode binding: {relative}")
        require(path.stat().st_mode & 0o111 == row["executable_bits"],
                f"executable-mode mismatch: {relative}")
    actual_records = {
        relative: (
            expected[relative]["bytes"],
            expected[relative]["executable_bits"],
            expected[relative]["sha256"],
        )
        for relative in expected
    }
    require(payload_commitment(actual_records)
            == payload["prepared_payload_sha256"],
            "prepared payload commitment mismatch")
    checksum_rows: dict[str, str] = {}
    for line in (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        require(relative not in checksum_rows,
                f"duplicate SHA256SUMS path: {relative}")
        checksum_rows[relative] = digest
    require(checksum_rows == {relative: row["sha256"]
                              for relative, row in expected.items()},
            "SHA256SUMS is not the exact projection of ACTIVE_MANIFEST.json")
    return payload


def count_jsonl_gz(path: Path) -> int:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def verify_counts(root: Path) -> dict:
    cert = root / "primary" / "certificates"
    relations = cert / "bounded_relation_n3_schema3_n3_all_filtered_relations.jsonl.gz"
    require(count_jsonl_gz(relations) == 10466, "canonical n3 relation count")
    n3 = json.loads((cert / "bounded_relation_n3_all_filtered_summary.json").read_text())
    bounded = n3["runs"][0]["bounded_relation_certificate"]
    require(bounded["canonical_decorated_relations"] == 10466, "n3 summary count")
    require(bounded["raw_presentations_examined"] == 10826, "n3 raw count")
    require(bounded["counts"] == {
        "cycle_to_cycle_isomorphism_or_T": 12,
        "cycle_to_cycle_pending_support_completion": 18,
        "cycle_to_theta_pending_support_completion": 4914,
        "cycle_to_theta_strict_open_cube_separation": 4092,
        "isomorphism_or_T": 62,
        "pending_support_completion": 5120,
        "strict_open_cube_separation": 5284,
        "theta_to_theta_isomorphism_or_T": 50,
        "theta_to_theta_pending_support_completion": 188,
        "theta_to_theta_strict_open_cube_separation": 1192,
    }, "n3 disposition counts")
    hard3 = json.loads((cert / "hard_cover_schema3_n3_full_summary.json").read_text())
    require(hard3["runs"][0]["hard_cover"]["canonical_restored_relations"] == 68584,
            "n3 restoration state count")
    hard4 = json.loads((cert / "hard_cover_schema3_theta2_full_summary.json").read_text())
    require(hard4["runs"][0]["hard_cover"]["canonical_restored_relations"] == 2106,
            "n4 restoration state count")
    evidence = evidence_bindings.verify_frozen(root)
    require(evidence["three_outgoing"] == 10466, "evidence map n3 count")
    require(evidence["four_outgoing_survivor"] == 192, "evidence map n4 count")
    require(evidence["closure_counts"] == {
        "COMPACT_PATH_CLOSURE_BINDINGS.jsonl.gz": 276,
        "RESTORATION_CLOSURE_BINDINGS.jsonl.gz": 5476,
        "DIRECT_ANCHOR_CLOSURE_BINDINGS.jsonl.gz": 62,
    }, "closure-binding stream counts")

    index = root / "atlas" / "ATLAS_INDEX.csv.gz"
    with gzip.open(index, "rt", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    n3_rows = sum(row["universe"] == "three_outgoing" for row in rows)
    n4_rows = sum(row["universe"] == "four_outgoing_survivor" for row in rows)
    require(n3_rows == 10466, "atlas index n3 count")
    require(n4_rows == 192, "atlas index n4 count")
    frozen_evidence = evidence_bindings.read_rows(
        root / "atlas/ATLAS_EVIDENCE_BINDINGS.jsonl.gz"
    )
    expected_index = [{field: str(row.get(field, "")) for field in rows[0]}
                      for row in frozen_evidence]
    require(rows == expected_index, "human atlas index is not the projection of evidence map")
    require(len({(row["universe"], row["relation_id"], row["presentation_ordinal"])
                 for row in rows}) == len(rows),
            "atlas index presentation identifiers are not unique")
    for row in rows:
        require(row["direction"] == "source_precedes_target", "relation direction")
        require((root / row["base_verifier"]).is_file(),
                f"missing indexed base verifier: {row['base_verifier']}")
        if row["closure_verifier"]:
            require((root / row["closure_verifier"]).is_file(),
                    f"missing indexed closure verifier: {row['closure_verifier']}")
    for row in frozen_evidence:
        if row["universe"] == "three_outgoing":
            if row["disposition"] == "pending_support_completion":
                require(all(
                    binding.get("closure", {}).get("path")
                    == evidence_bindings.RESTORATION_CLOSURE_REL
                    for binding in row["evidence"]["restoration_roots"]
                ), "pending relation lacks record-level restoration closure")
            elif row["disposition"] == "isomorphism_or_T":
                require(
                    row["evidence"].get("direct_anchor_closure", {}).get("path")
                    == evidence_bindings.DIRECT_CLOSURE_REL,
                    "direct residual relation lacks probe closure",
                )
        elif row["disposition"] in {
            "fixed_full_restoration_root", "selected_incoming_rooting_duplicate"
        }:
            require(
                row["evidence"].get("restoration_closure", {}).get("path")
                == evidence_bindings.RESTORATION_CLOSURE_REL,
                "four-outgoing presentation lacks restoration closure",
            )
    four = [row["disposition"] for row in rows if row["universe"] == "four_outgoing_survivor"]
    require(four.count("direct_labelled_isomorphism") == 18, "n4 direct survivors")
    require(four.count("selected_incoming_rooting_duplicate") == 42,
            "n4 rooting-duplicate survivors")
    require(four.count("fixed_full_restoration_root") == 132, "n4 restoration roots")
    cut_reduction = json.loads(
        (root / "independent/bridge_cut/palette_reduction_certificate.json").read_text()
    )
    require(cut_reduction["status"] == "EXACTLY COMPUTED", "cut reduction status")
    require(cut_reduction["failure_count"] == 0, "cut reduction failures")
    require(cut_reduction["totals"]["balanced_total"] == 808642,
            "cut reduction balanced universe")
    require(cut_reduction["totals"]["three_run_path_obstruction"] == 229988,
            "cut reduction direct obstruction count")
    require(
        cut_reduction["totals"]["direct_palette"]
        + cut_reduction["totals"]["singleton_doubled_palette"]
        == 578654,
        "cut reduction palette count",
    )
    cut_cleanroom = json.loads(
        (root / "reviews/global_bridge/palette_cleanroom_certificate.json").read_text()
    )
    require(cut_cleanroom["status"] == "EXACTLY COMPUTED", "cut cleanroom status")
    require(cut_cleanroom["total_valid_palette_presentations"] == 379742,
            "cut cleanroom valid-presentation count")
    require(cut_cleanroom["survivor_count"] == 0, "cut cleanroom survivor")
    cut_primary = json.loads(
        (root / "independent/bridge_cut/cut_certificate.json").read_text()
    )
    primary_family_counts = {
        (row["core"], row["role"]): (
            row["balanced_compressed_checked"],
            row["valid_balanced_compressed"],
            row["valid_singleton_doubled"],
            len(row["survivors"]),
        )
        for row in cut_primary["switching_compression"]["families"]
    }
    cleanroom_family_counts = {
        (row["core"], row["role"]): (
            row["balanced_compressed_checked"],
            row["valid_balanced_compressed"],
            row["valid_singleton_doubled"],
            row["survivor_count"],
        )
        for row in cut_cleanroom["families"]
    }
    require(cleanroom_family_counts == primary_family_counts,
            "primary/clean-room cut family counts disagree")
    return {
        "three_outgoing": n3_rows,
        "four_outgoing_survivors": n4_rows,
        "cut_balanced_words": 808642,
        "cut_valid_palette_presentations": 379742,
        "record_level_evidence_sha256": evidence["logical_sha256"],
    }


def verify_scope(root: Path) -> None:
    forbidden_parts = {"history", "quarantine", "repair", "tmp", "__pycache__"}
    forbidden_names = {"AUDIT_REPORT.md", "ADVERSARIAL_REVIEW.md", "RESEARCH_LOG.md"}
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if ".venv" in relative.parts or "__pycache__" in relative.parts:
            continue
        require(not path.is_symlink(), f"symlink is not permitted: {relative}")
        require(not any(part in forbidden_parts for part in relative.parts),
                f"non-active tree leaked into bundle: {relative}")
        require(path.name not in forbidden_names, f"audit prose leaked: {relative}")
        require(("land" + "mark") not in path.name.casefold(),
                f"obsolete filename token: {relative}")
        if path.is_file() and path.suffix.casefold() in {
            ".cff", ".csv", ".json", ".md", ".py", ".sh", ".txt",
        }:
            text = path.read_text(encoding="utf-8", errors="strict")
            require(("land" + "mark") not in text.casefold(),
                    f"obsolete text token: {relative}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = verify_manifest(root)
    verify_scope(root)
    counts = verify_counts(root)
    print(json.dumps({
        "status": "VERIFIED",
        "files": len(manifest["files"]),
        "counts": counts,
        "bundle_version": manifest["version"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
