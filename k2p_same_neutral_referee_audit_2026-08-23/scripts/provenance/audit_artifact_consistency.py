#!/usr/bin/env python3
"""Cross-check papers, sources, build records, lock, crosswalk, and telemetry."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def payload_hash(value: dict[str, Any]) -> str:
    unsigned = dict(value)
    unsigned.pop("payload_sha256", None)
    return sha(canonical(unsigned))


def pdf_pages(path: Path) -> int:
    run = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=True)
    match = re.search(r"^Pages:\s+(\d+)\s*$", run.stdout, flags=re.MULTILINE)
    if not match:
        raise RuntimeError(f"pdfinfo did not report pages for {path}")
    return int(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--audit-root", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.handoff.resolve()
    audit = args.audit_root.resolve()
    project = root / "materials/k2p_principal_d_plus_submission_referee"
    submission = project / "proof_compression_submission"
    binding = json.loads((root / "SUBMISSION_BINDING.json").read_text(encoding="utf-8"))
    inner = json.loads(
        (submission / "crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json").read_text(encoding="utf-8")
    )
    report = json.loads((submission / "PDF_BUILD_REPORT.json").read_text(encoding="utf-8"))
    report_md = (submission / "PDF_BUILD_REPORT.md").read_text(encoding="utf-8")
    release_lock_path = project / "work/final_theorem_release/RELEASE_LOCK.json"
    release_lock = json.loads(release_lock_path.read_text(encoding="utf-8"))
    content_path = project / "output/referee/REFEREE_BUNDLE_CONTENTS.json"
    content = json.loads(content_path.read_text(encoding="utf-8"))
    replay_path = submission / "output/FINAL_CLEAN_FULL_REPLAY.json"
    telemetry_path = submission / "output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json"
    replay = json.loads(replay_path.read_text(encoding="utf-8"))
    telemetry = json.loads(telemetry_path.read_text(encoding="utf-8"))
    crosswalk_path = submission / "crosswalk/THEOREM_ARTIFACT_CROSSWALK.json"
    crosswalk = json.loads(crosswalk_path.read_text(encoding="utf-8"))

    checks: list[dict[str, Any]] = []

    def record(name: str, observed: Any, expected: Any, evidence: str = "provenance") -> None:
        checks.append(
            {
                "name": name,
                "observed": observed,
                "expected": expected,
                "pass": observed == expected,
                "evidence": evidence,
            }
        )

    # Papers, sources, logs, and build report.
    labels = {
        "article": (
            "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf",
            "papers/K2P_SAME_Principal_Domain_Article.pdf",
            "proof_compression_submission/article/main.tex",
            "proof_compression_submission/output/logs/article.log",
            26,
        ),
        "supplement": (
            "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf",
            "papers/K2P_SAME_Reader_Supplement.pdf",
            "proof_compression_submission/supplement/supplement.tex",
            "proof_compression_submission/output/logs/supplement.log",
            24,
        ),
    }
    paper_rows: list[dict[str, Any]] = []
    for label, (inner_rel, outer_rel, source_rel, log_rel, pages) in labels.items():
        inner_pdf = project / inner_rel
        outer_pdf = root / outer_rel
        source = project / source_rel
        log = project / log_rel
        binding_row = binding["papers"][label]
        report_row = report[label]
        observed_hash = sha_file(inner_pdf)
        observed_bytes = inner_pdf.stat().st_size
        record(f"{label}_top_inner_bytes", outer_pdf.read_bytes() == inner_pdf.read_bytes(), True)
        record(f"{label}_binding_hash", observed_hash, binding_row["sha256"])
        record(f"{label}_binding_bytes", observed_bytes, binding_row["bytes"])
        record(f"{label}_report_hash", observed_hash, report_row["pdf_sha256"])
        record(f"{label}_report_bytes", observed_bytes, report_row["bytes"])
        record(f"{label}_source_hash", sha_file(source), report_row["source_sha256"])
        record(f"{label}_log_hash", sha_file(log), report_row["log_sha256"])
        record(f"{label}_page_count", pdf_pages(inner_pdf), pages)
        record(f"{label}_report_page_count", report_row["pages"], pages)
        paper_rows.append(
            {
                "label": label,
                "pdf": str(inner_pdf),
                "bytes": observed_bytes,
                "sha256": observed_hash,
                "pages": pages,
                "source_sha256": sha_file(source),
                "log_sha256": sha_file(log),
            }
        )
    report_md_normalized = re.sub(r"\s+", " ", report_md)
    record(
        "pdf_build_report_markdown_anchors",
        all(
            str(value) in report_md_normalized
            for value in (
                report["article"]["pdf_sha256"],
                report["supplement"]["pdf_sha256"],
                report["article"]["source_sha256"],
                report["supplement"]["source_sha256"],
                "26",
                "24",
                "Tectonic 0.16.9",
            )
        ),
        True,
    )
    record("pdf_build_visual_verdict", report["visual_verdict"], "PASS")
    record("pdf_build_clean_source_flag", report["checks"]["five_source_clean_build_passed"], True)

    for relative, expected_hash in binding["five_source_set"].items():
        path = project / relative
        record(f"five_source:{relative}", sha_file(path), expected_hash)
        record(
            f"five_source_inner_manifest:{relative}",
            inner["submission_sources"]["files"][relative],
            {"bytes": path.stat().st_size, "sha256": expected_hash},
        )

    # Release lock and frozen content ledger.
    record("release_lock_payload", payload_hash(release_lock), release_lock["payload_sha256"])
    release_lock_sha = sha_file(release_lock_path)
    record("release_lock_sha_content_ledger", release_lock_sha, content["release_lock_sha256"])
    record(
        "release_lock_payload_content_ledger",
        release_lock["payload_sha256"],
        content["release_lock_payload_sha256"],
    )
    lock_bad: list[str] = []
    for relative, row in release_lock["files"].items():
        path = project / relative
        actual = {"bytes": path.stat().st_size, "sha256": sha_file(path)} if path.is_file() else None
        expected = {"bytes": row["bytes"], "sha256": row["sha256"]}
        if actual != expected:
            lock_bad.append(relative)
    record("release_lock_file_rows", lock_bad, [])
    frozen = inner["frozen_evidence"]["files"]
    record("content_ledger_equals_inner_frozen_map", content["files"], frozen)
    record("content_ledger_count", len(content["files"]), content["file_count"])
    record(
        "content_ledger_bytes",
        sum(int(row["bytes"]) for row in content["files"].values()),
        content["total_bytes"],
    )
    record("content_ledger_root", sha(canonical(content["files"])), content["content_ledger_root_sha256"])
    record(
        "content_ledger_root_inner",
        content["content_ledger_root_sha256"],
        inner["frozen_evidence"]["content_ledger_root_sha256"],
    )
    record(
        "release_lock_sha_inner",
        release_lock_sha,
        inner["frozen_evidence"]["release_lock_sha256"],
    )
    record(
        "release_lock_payload_inner",
        release_lock["payload_sha256"],
        inner["frozen_evidence"]["release_lock_payload_sha256"],
    )

    # Stored full replay and telemetry are provenance records, not re-execution.
    record("replay_report_hash", sha_file(replay_path), telemetry["report"]["sha256"])
    record("replay_telemetry_hash_inner", sha_file(telemetry_path), inner["runtime_boundary"]["telemetry_sha256"])
    record("replay_report_hash_inner", sha_file(replay_path), inner["runtime_boundary"]["report_sha256"])
    record("replay_status", replay["status"], "PASS")
    record("replay_mode", replay["mode"], "full")
    record("replay_optimized", replay["optimized_mode"], False)
    record("replay_promotion", replay["promotion_ready"], True)
    record("replay_blockers", replay["blockers"], [])
    record("replay_layer_count", len(replay["layer_replays"]), 35)
    record("replay_all_layer_statuses", all(r["status"] == "PASS" for r in replay["layer_replays"]), True)
    record(
        "replay_lock_binding",
        replay["lock_payload_sha256"],
        release_lock["payload_sha256"],
    )
    record(
        "telemetry_internal_elapsed",
        telemetry["report"]["internal_elapsed_seconds"],
        replay["elapsed_seconds"],
    )
    record("telemetry_layer_count", telemetry["report"]["layer_count"], len(replay["layer_replays"]))
    record("telemetry_lock_binding", telemetry["report"]["lock_payload_sha256"], replay["lock_payload_sha256"])
    record("telemetry_promotion", telemetry["report"]["promotion_ready"], replay["promotion_ready"])
    record("telemetry_blocker_count", telemetry["report"]["blocker_count"], len(replay["blockers"]))
    record("telemetry_runtime", telemetry["runtime"], replay["runtime"])
    commit_run = subprocess.run(
        ["git", "rev-parse", f"{telemetry['git_commit']}^{{commit}}"],
        cwd=args.repo,
        capture_output=True,
        text=True,
        check=False,
    )
    record("telemetry_git_commit_exists", commit_run.returncode, 0)

    # The theorem-artifact crosswalk is internally bound to the same frozen tree.
    record("crosswalk_payload", payload_hash(crosswalk), crosswalk["payload_sha256"])
    record("crosswalk_status", crosswalk["status"], "PASS_PC_PARTIAL")
    frozen_release = crosswalk["frozen_release"]
    record("crosswalk_release_lock_sha", frozen_release["release_lock_sha256"], release_lock_sha)
    record(
        "crosswalk_release_lock_payload",
        frozen_release["release_lock_payload_sha256"],
        release_lock["payload_sha256"],
    )
    record(
        "crosswalk_content_root",
        frozen_release["content_ledger_root_sha256"],
        content["content_ledger_root_sha256"],
    )
    record("crosswalk_frozen_count", frozen_release["file_count_including_release_lock"], len(content["files"]))
    record("crosswalk_frozen_bytes", frozen_release["total_bytes_including_release_lock"], content["total_bytes"])
    crosswalk_bad: list[str] = []
    artifact_count = 0
    for claim in crosswalk["claims"]:
        for field in (
            "authoritative_artifacts",
            "producer_artifacts",
            "replay_artifacts",
            "mutation_artifacts",
        ):
            for row in claim.get(field, []):
                artifact_count += 1
                path = project / row["path"]
                actual = {"bytes": path.stat().st_size, "sha256": sha_file(path)} if path.is_file() else None
                if actual != {"bytes": row["bytes"], "sha256": row["sha256"]}:
                    crosswalk_bad.append(f"{claim['claim_id']}:{field}:{row['path']}")
    record("crosswalk_artifact_rows", crosswalk_bad, [])
    builder_text = (submission / "crosswalk/build_theorem_artifact_crosswalk.py").read_text(encoding="utf-8")
    record(
        "crosswalk_content_ledger_dependency",
        'read_json("output/referee/REFEREE_BUNDLE_CONTENTS.json")' in builder_text,
        True,
    )

    # Current clean builds: logs are bit-identical; PDF renderings are bit-identical
    # page by page although PDF metadata timestamps and trailer IDs differ.
    build_pairs = {
        "article": (
            audit / "reports/provenance/manuscript/article/main.pdf",
            audit / "reports/provenance/manuscript/article/main.log",
            audit / "tmp/pdfs/article_sealed",
            audit / "tmp/pdfs/article_rebuilt",
            audit / "reports/provenance/manuscript/fixed_epoch_article/main.pdf",
            1787465144,
        ),
        "supplement": (
            audit / "reports/provenance/manuscript/supplement/supplement.pdf",
            audit / "reports/provenance/manuscript/supplement/supplement.log",
            audit / "tmp/pdfs/supplement_sealed",
            audit / "tmp/pdfs/supplement_rebuilt",
            audit / "reports/provenance/manuscript/fixed_epoch_supplement/supplement.pdf",
            1787465911,
        ),
    }
    rebuild_rows = []
    for label, (pdf, log, sealed_png, rebuilt_png, fixed_pdf, source_date_epoch) in build_pairs.items():
        source_pdf = project / labels[label][0]
        source_log = project / labels[label][3]
        sealed_pages = sorted(sealed_png.glob("*.png"))
        rebuilt_pages = sorted(rebuilt_png.glob("*.png"))
        raster_equal = len(sealed_pages) == len(rebuilt_pages) and all(
            a.read_bytes() == b.read_bytes() for a, b in zip(sealed_pages, rebuilt_pages)
        )
        log_text = log.read_text(encoding="utf-8", errors="replace")
        defects = [
            pattern
            for pattern in (
                "Overfull",
                "undefined references",
                "Citation.*undefined",
                "Reference.*undefined",
                "Fatal error",
                "Token not allowed in a PDF string",
            )
            if re.search(pattern, log_text, flags=re.IGNORECASE)
        ]
        record(f"current_build_{label}_log_hash", sha_file(log), sha_file(source_log), "computational")
        record(f"current_build_{label}_log_defects", defects, [], "computational")
        record(f"current_build_{label}_raster_pages", raster_equal, True, "computational")
        record(f"current_build_{label}_pages", pdf_pages(pdf), labels[label][4], "computational")
        record(
            f"fixed_epoch_build_{label}_bytes",
            fixed_pdf.read_bytes() == source_pdf.read_bytes(),
            True,
            "computational",
        )
        rebuild_rows.append(
            {
                "label": label,
                "pdf_bytes": pdf.stat().st_size,
                "pdf_sha256": sha_file(pdf),
                "sealed_pdf_sha256": sha_file(source_pdf),
                "pdf_bytes_identical": pdf.read_bytes() == source_pdf.read_bytes(),
                "build_log_sha256": sha_file(log),
                "build_log_identical": log.read_bytes() == source_log.read_bytes(),
                "raster_pages": len(sealed_pages),
                "raster_pages_byte_identical": raster_equal,
                "source_date_epoch_for_exact_rebuild": source_date_epoch,
                "fixed_epoch_pdf_sha256": sha_file(fixed_pdf),
                "fixed_epoch_pdf_bytes_identical": fixed_pdf.read_bytes() == source_pdf.read_bytes(),
            }
        )

    status = "PASS" if all(row["pass"] for row in checks) else "FAIL"
    value = {
        "schema": "independent-k2p-artifact-consistency-audit-v1",
        "status": status,
        "checks": checks,
        "papers": paper_rows,
        "release_lock": {
            "path": str(release_lock_path),
            "bytes": release_lock_path.stat().st_size,
            "sha256": release_lock_sha,
            "payload_sha256": release_lock["payload_sha256"],
            "file_rows_checked": len(release_lock["files"]),
        },
        "frozen_content_ledger": {
            "path": str(content_path),
            "bytes": content_path.stat().st_size,
            "sha256": sha_file(content_path),
            "file_rows_checked": len(content["files"]),
            "content_root_sha256": content["content_ledger_root_sha256"],
        },
        "stored_replay": {
            "report_sha256": sha_file(replay_path),
            "telemetry_sha256": sha_file(telemetry_path),
            "layer_count": len(replay["layer_replays"]),
            "historical_git_commit_full": commit_run.stdout.strip() if commit_run.returncode == 0 else None,
        },
        "crosswalk": {
            "sha256": sha_file(crosswalk_path),
            "payload_sha256": crosswalk["payload_sha256"],
            "claims": len(crosswalk["claims"]),
            "artifact_rows_checked": artifact_count,
        },
        "current_clean_builds": rebuild_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": status,
        "checks": len(checks),
        "release_lock_rows": len(release_lock["files"]),
        "frozen_rows": len(content["files"]),
        "crosswalk_artifact_rows": artifact_count,
        "output": str(args.output.resolve()),
    }, sort_keys=True))
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
