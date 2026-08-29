#!/usr/bin/env python3
"""Independent provenance audit for the 2026-08-28 K2P referee package.

This deliberately does not import any submitted package module.  It rebuilds
the recursive frozen ledger, the submission ledger, the combined manifest,
the archive member inventory, the theorem-artifact crosswalk bindings, and
the clean-replay/tag bindings directly from bytes.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import re
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


LOCK_RELATIVE = "work/final_theorem_release/RELEASE_LOCK.json"
PORTABLE_LEDGER_RELATIVE = "output/referee/REFEREE_BUNDLE_CONTENTS.json"
MANIFEST_RELATIVE = (
    "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
)
ARCHIVE_PREFIX = "k2p_principal_d_plus_submission_referee"
EXPECTED_ARCHIVE_TIMESTAMP = (2026, 8, 27, 0, 0, 0)
EXPECTED_TAG = "k2p-same-biorxiv-v1.0.4"
TELEMETRY_SOURCES = (
    "proof_compression_submission/article/main.tex",
    "proof_compression_submission/article/references.bib",
    "proof_compression_submission/supplement/supplement.tex",
    "proof_compression_submission/supplement/compression_tables.tex",
    "proof_compression_submission/supplement/certificate_appendix.tex",
)
OPERATIONAL_EVIDENCE = {
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json",
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json",
    "proof_compression_submission/output/FINAL_RELEASE_MUTATIONS.json",
    "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf",
    "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf",
    "proof_compression_submission/output/logs/article.log",
    "proof_compression_submission/output/logs/supplement.log",
}
SUPPLEMENTAL_DEPENDENCIES = {
    "output/referee/README.md",
    PORTABLE_LEDGER_RELATIVE,
    "output/referee/build_referee_bundle.py",
}


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise AuditFailure(code if detail is None else f"{code}:{detail}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_blob_sha1_file(path: Path) -> str:
    size = path.stat().st_size
    digest = hashlib.sha1(usedforsecurity=False)
    digest.update(f"blob {size}\0".encode())
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def strict_json(data: bytes, label: str) -> Any:
    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, "DUPLICATE_JSON_NAME", f"{label}:{key}")
            result[key] = value
        return result

    def reject_constant(token: str) -> None:
        raise AuditFailure(f"NONFINITE_JSON_NUMBER:{label}:{token}")

    def finite_float(token: str) -> float:
        value = float(token)
        require(math.isfinite(value), "NONFINITE_JSON_FLOAT", f"{label}:{token}")
        return value

    try:
        text = data.decode("utf-8")
        return json.loads(
            text,
            object_pairs_hook=pairs_hook,
            parse_constant=reject_constant,
            parse_float=finite_float,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as error:
        raise AuditFailure(f"JSON_DECODE_FAIL:{label}:{error}") from error


def strict_object(path: Path, label: str) -> dict[str, Any]:
    value = strict_json(path.read_bytes(), label)
    require(isinstance(value, dict), "JSON_NOT_OBJECT", label)
    return value


def safe_relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    require(
        not path.is_absolute()
        and bool(path.parts)
        and all(part not in {"", ".", ".."} for part in path.parts),
        "UNSAFE_RELATIVE_PATH",
        value,
    )
    return path


def path_in(project: Path, relative: str) -> Path:
    return project.joinpath(*safe_relative(relative).parts)


def file_row(path: Path) -> dict[str, int | str]:
    require(path.is_file() and not path.is_symlink(), "NOT_REGULAR_FILE", path)
    return {"bytes": path.stat().st_size, "sha256": sha256_file(path)}


def verify_payload(value: dict[str, Any], label: str) -> str:
    claimed = value.get("payload_sha256")
    unsigned = dict(value)
    unsigned.pop("payload_sha256", None)
    require(
        isinstance(claimed, str) and claimed == canonical_hash(unsigned),
        "PAYLOAD_HASH_MISMATCH",
        label,
    )
    return claimed


def add_sha_manifest(
    project: Path,
    expected: dict[str, str],
    manifest_relative: str,
    base_relative: str,
) -> int:
    path = path_in(project, manifest_relative)
    count = 0
    for ordinal, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "BAD_SHA_MANIFEST_LINE", f"{manifest_relative}:{ordinal}")
        digest, child = match.groups()
        relative = (PurePosixPath(base_relative) / safe_relative(child)).as_posix()
        previous = expected.get(relative)
        require(previous is None or previous == digest, "CONFLICTING_NESTED_HASH", relative)
        expected[relative] = digest
        count += 1
    return count


def frozen_ledger(project: Path, lock: dict[str, Any], lock_sha: str) -> tuple[dict[str, dict[str, int | str]], dict[str, int]]:
    files = lock.get("files")
    require(isinstance(files, dict) and bool(files), "LOCK_FILE_MAP_MISSING")
    expected: dict[str, str] = {}
    for relative, row in files.items():
        require(isinstance(relative, str) and isinstance(row, dict), "BAD_LOCK_FILE_ROW")
        safe_relative(relative)
        digest = row.get("sha256")
        require(isinstance(digest, str), "BAD_LOCK_FILE_HASH", relative)
        expected[relative] = digest

    nested_counts = {
        "outer_lock_files": len(files),
        "rank_manifest_rows": add_sha_manifest(
            project,
            expected,
            "work/rank_upper_certificates/MANIFEST.sha256",
            "work/rank_upper_certificates",
        ),
        "cycle_manifest_rows": add_sha_manifest(
            project,
            expected,
            "work/cycle_three_port_closure/MANIFEST.sha256",
            "work/cycle_three_port_closure",
        ),
    }
    direct_root = PurePosixPath("package/referee/k2p_offline_sweep_portable")
    for name, count_key in (
        ("DIRECT_CLOSURE_LOCK.json", "direct_closure_rows"),
        ("INPUT_LOCK.json", "direct_input_rows"),
    ):
        relative = (direct_root / name).as_posix()
        nested = strict_object(path_in(project, relative), relative)
        nested_files = nested.get("files")
        require(isinstance(nested_files, dict), "DIRECT_NESTED_FILES_MISSING", name)
        nested_counts[count_key] = len(nested_files)
        for child, digest in nested_files.items():
            require(isinstance(child, str) and isinstance(digest, str), "BAD_DIRECT_BINDING", name)
            joined = (direct_root / safe_relative(child)).as_posix()
            previous = expected.get(joined)
            require(previous is None or previous == digest, "CONFLICTING_DIRECT_HASH", joined)
            expected[joined] = digest

    expected[LOCK_RELATIVE] = lock_sha
    ledger: dict[str, dict[str, int | str]] = {}
    for relative in sorted(expected):
        row = file_row(path_in(project, relative))
        require(row["sha256"] == expected[relative], "FROZEN_HASH_MISMATCH", relative)
        outer = files.get(relative)
        if isinstance(outer, dict):
            require(
                row.get("sha256") == outer.get("sha256")
                and row.get("bytes") == outer.get("bytes"),
                "OUTER_LOCK_ROW_MISMATCH",
                relative,
            )
        ledger[relative] = row
    return ledger, nested_counts


def include_submission(relative: PurePosixPath) -> bool:
    if not relative.parts or relative.parts[0] != "proof_compression_submission":
        return False
    if relative.as_posix() == MANIFEST_RELATIVE:
        return False
    if relative.as_posix() in OPERATIONAL_EVIDENCE:
        return True
    if (
        "output" in relative.parts
        or "__pycache__" in relative.parts
        or any(part.startswith(".") for part in relative.parts[1:-1])
    ):
        return False
    if relative.name == ".DS_Store" or relative.suffix in {".pyc", ".pyo"}:
        return False
    return True


def submission_ledger(project: Path) -> dict[str, dict[str, int | str]]:
    root = project / "proof_compression_submission"
    require(root.is_dir() and not root.is_symlink(), "SUBMISSION_ROOT_MISSING")
    ledger: dict[str, dict[str, int | str]] = {}
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        relative = PurePosixPath(path.relative_to(project).as_posix())
        if include_submission(relative):
            ledger[relative.as_posix()] = file_row(path)
    for relative in sorted(SUPPLEMENTAL_DEPENDENCIES):
        ledger[relative] = file_row(path_in(project, relative))
    return ledger


def check_declared_ledger(
    declared: dict[str, Any],
    actual: dict[str, dict[str, int | str]],
    label: str,
) -> None:
    require(declared.get("files") == actual, "DECLARED_FILE_LEDGER_MISMATCH", label)
    require(declared.get("file_count") == len(actual), "DECLARED_FILE_COUNT_MISMATCH", label)
    require(
        declared.get("total_bytes") == sum(int(row["bytes"]) for row in actual.values()),
        "DECLARED_TOTAL_BYTES_MISMATCH",
        label,
    )
    require(
        declared.get("content_ledger_root_sha256") == canonical_hash(actual),
        "DECLARED_CONTENT_ROOT_MISMATCH",
        label,
    )


def scan_strict_json_members(project: Path, relatives: list[str]) -> dict[str, int]:
    counters = Counter()
    for relative in relatives:
        name = PurePosixPath(relative).name
        if not (name.endswith(".json") or name.endswith(".json.gz") or name.endswith(".jsonl.gz")):
            continue
        path = path_in(project, relative)
        if name.endswith(".json"):
            strict_json(path.read_bytes(), relative)
            counters["plain_json_documents"] += 1
            continue
        if name.endswith(".json.gz"):
            plain = gzip.decompress(path.read_bytes())
            require(len(plain) <= 64 * 1024 * 1024, "GZIP_JSON_SIZE_LIMIT", relative)
            value = strict_json(plain, relative)
            require(isinstance(value, dict), "GZIP_JSON_NOT_OBJECT", relative)
            require(plain == canonical_bytes(value) + b"\n", "NONCANONICAL_GZIP_JSON", relative)
            counters["gzip_json_documents"] += 1
            counters["expanded_bytes"] += len(plain)
            continue
        total = 0
        rows = 0
        with gzip.open(path, "rb") as expanded:
            while True:
                line = expanded.readline(16 * 1024 * 1024 + 1)
                if not line:
                    break
                rows += 1
                require(len(line) <= 16 * 1024 * 1024, "JSONL_LINE_SIZE_LIMIT", f"{relative}:{rows}")
                total += len(line)
                require(total <= 4 * 1024 * 1024 * 1024, "JSONL_STREAM_SIZE_LIMIT", relative)
                require(line.endswith(b"\n") and line != b"\n", "BAD_JSONL_LINE_BOUNDARY", f"{relative}:{rows}")
                value = strict_json(line, f"{relative}:{rows}")
                require(isinstance(value, dict), "JSONL_ROW_NOT_OBJECT", f"{relative}:{rows}")
                require(line == canonical_bytes(value) + b"\n", "NONCANONICAL_JSONL", f"{relative}:{rows}")
        counters["gzip_jsonl_streams"] += 1
        counters["gzip_jsonl_rows"] += rows
        counters["expanded_bytes"] += total
    return dict(sorted(counters.items()))


def verify_crosswalk(
    project: Path,
    frozen: dict[str, dict[str, int | str]],
    submission: dict[str, dict[str, int | str]],
) -> dict[str, Any]:
    relative = "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json"
    value = strict_object(path_in(project, relative), relative)
    payload = verify_payload(value, relative)
    claims = value.get("claims")
    require(isinstance(claims, list) and len(claims) == 13, "CROSSWALK_CLAIM_COUNT")
    expected_ids = [f"C{number:02d}" for number in range(1, 14)]
    observed_prefixes: list[str] = []
    binding_count = 0
    unique_paths: set[str] = set()
    for claim in claims:
        require(isinstance(claim, dict), "BAD_CROSSWALK_CLAIM")
        claim_id = claim.get("claim_id")
        require(isinstance(claim_id, str), "BAD_CROSSWALK_CLAIM_ID")
        observed_prefixes.append(claim_id.split("-", 1)[0])
        for field in (
            "authoritative_artifacts",
            "producer_artifacts",
            "replay_artifacts",
            "mutation_artifacts",
        ):
            rows = claim.get(field)
            require(isinstance(rows, list) and bool(rows), "EMPTY_CROSSWALK_BINDINGS", f"{claim_id}:{field}")
            for row in rows:
                require(isinstance(row, dict), "BAD_CROSSWALK_BINDING", f"{claim_id}:{field}")
                path = row.get("path")
                frozen_flag = row.get("frozen")
                require(isinstance(path, str) and isinstance(frozen_flag, bool), "BAD_CROSSWALK_PATH", claim_id)
                ledger = frozen if frozen_flag else submission
                require(
                    ledger.get(path) == {"bytes": row.get("bytes"), "sha256": row.get("sha256")},
                    "UNBOUND_CROSSWALK_ARTIFACT",
                    f"{claim_id}:{path}",
                )
                binding_count += 1
                unique_paths.add(path)
    require(observed_prefixes == expected_ids, "CROSSWALK_CLAIM_ID_ORDER", observed_prefixes)
    return {
        "claim_count": len(claims),
        "binding_rows": binding_count,
        "unique_artifact_paths": len(unique_paths),
        "payload_sha256": payload,
        "sha256": sha256_file(path_in(project, relative)),
        "status": value.get("status"),
    }


def verify_telemetry(project: Path, lock: dict[str, Any], lock_sha: str) -> dict[str, Any]:
    report_relative = "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json"
    telemetry_relative = "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json"
    report = strict_object(path_in(project, report_relative), report_relative)
    telemetry = strict_object(path_in(project, telemetry_relative), telemetry_relative)
    report_sha = sha256_file(path_in(project, report_relative))
    require(telemetry.get("report", {}).get("sha256") == report_sha, "TELEMETRY_REPORT_HASH")
    require(telemetry.get("status") == "PASS", "TELEMETRY_STATUS")
    require(telemetry.get("clean_detached_checkout") is True, "TELEMETRY_NOT_CLEAN_DETACHED")
    require(report.get("status") == "PASS" and report.get("promotion_ready") is True, "REPLAY_NOT_PASS")
    layers = report.get("layer_replays")
    require(report.get("mode") == "full" and isinstance(layers, list) and len(layers) == 41, "FULL_REPLAY_LAYER_COUNT")
    lock_binding = telemetry.get("release_lock")
    require(
        isinstance(lock_binding, dict)
        and lock_binding.get("path") == LOCK_RELATIVE
        and lock_binding.get("sha256") == lock_sha
        and lock_binding.get("bytes") == path_in(project, LOCK_RELATIVE).stat().st_size
        and lock_binding.get("payload_sha256") == lock.get("payload_sha256"),
        "TELEMETRY_LOCK_BINDING",
    )
    expected_sources = {relative: file_row(path_in(project, relative)) for relative in TELEMETRY_SOURCES}
    require(telemetry.get("submission_sources") == expected_sources, "TELEMETRY_SOURCE_BINDINGS")
    report_summary = telemetry.get("report", {})
    require(
        report_summary.get("layer_count") == len(layers)
        and report_summary.get("internal_elapsed_seconds") == report.get("elapsed_seconds")
        and report_summary.get("blocker_count") == 0
        and report_summary.get("promotion_ready") is True,
        "TELEMETRY_REPORT_SUMMARY",
    )
    return {
        "git_commit": telemetry.get("git_commit"),
        "layer_count": len(layers),
        "report_sha256": report_sha,
        "telemetry_sha256": sha256_file(path_in(project, telemetry_relative)),
        "real_seconds": telemetry.get("time_l", {}).get("real_seconds"),
        "internal_elapsed_seconds": report.get("elapsed_seconds"),
        "maximum_resident_set_size_bytes": telemetry.get("time_l", {}).get("maximum_resident_set_size_bytes"),
        "peak_memory_footprint_bytes": telemetry.get("time_l", {}).get("peak_memory_footprint_bytes"),
        "runtime": telemetry.get("runtime"),
    }


def verify_pdf_report(project: Path, submission: dict[str, dict[str, int | str]]) -> dict[str, Any]:
    relative = "proof_compression_submission/PDF_BUILD_REPORT.json"
    report = strict_object(path_in(project, relative), relative)
    payload = verify_payload(report, relative)
    require(report.get("source_set") == [
        "article/main.tex",
        "article/references.bib",
        "supplement/supplement.tex",
        "supplement/compression_tables.tex",
        "supplement/certificate_appendix.tex",
    ], "PDF_SOURCE_SET")
    for kind in ("article", "supplement"):
        row = report.get(kind)
        require(isinstance(row, dict), "PDF_REPORT_ROW", kind)
        pdf_relative = row.get("pdf_path")
        source_relative = row.get("source_path")
        require(isinstance(pdf_relative, str) and isinstance(source_relative, str), "PDF_REPORT_PATH", kind)
        pdf_row = file_row(path_in(project, pdf_relative))
        require(
            pdf_row == {"bytes": row.get("bytes"), "sha256": row.get("pdf_sha256")},
            "PDF_REPORT_OUTPUT_BINDING",
            kind,
        )
        require(
            sha256_file(path_in(project, source_relative)) == row.get("source_sha256"),
            "PDF_REPORT_SOURCE_BINDING",
            kind,
        )
        require(submission.get(pdf_relative) == pdf_row, "PDF_NOT_IN_SUBMISSION_LEDGER", kind)
    for kind in ("article", "supplement"):
        log_relative = f"proof_compression_submission/output/logs/{kind}.log"
        require(
            sha256_file(path_in(project, log_relative)) == report[kind]["log_sha256"],
            "PDF_LOG_HASH",
            kind,
        )
        text = path_in(project, log_relative).read_text(encoding="utf-8", errors="replace")
        require("Overfull \\hbox" not in text and "Overfull \\vbox" not in text, "PDF_OVERFULL_BOX", kind)
        require("Token not allowed in a PDF string" not in text, "PDF_HYPERREF_WARNING", kind)
        require(not re.search(r"^! ", text, re.MULTILINE), "PDF_FATAL_LATEX", kind)
        require(not re.search(r"(?:Citation|Reference) .+ undefined", text), "PDF_UNDEFINED_REFERENCE", kind)
    return {
        "payload_sha256": payload,
        "sha256": sha256_file(path_in(project, relative)),
        "article": report["article"],
        "supplement": report["supplement"],
        "engine": report.get("engine"),
        "source_date_epoch": report.get("source_date_epoch"),
        "checks": report.get("checks"),
    }


def verify_historical_registry(project: Path, frozen: dict[str, dict[str, int | str]]) -> dict[str, Any]:
    relative = "work/final_theorem_release/HISTORICAL_ARTIFACT_REGISTRY.json"
    value = strict_object(path_in(project, relative), relative)
    payload = verify_payload(value, relative)
    artifacts = value.get("artifacts")
    require(isinstance(artifacts, list) and len(artifacts) == 8, "HISTORICAL_REGISTRY_COUNT")
    classifications = Counter()
    for row in artifacts:
        require(isinstance(row, dict), "BAD_HISTORICAL_ROW")
        artifact_path = row.get("path")
        require(isinstance(artifact_path, str), "BAD_HISTORICAL_PATH")
        require(row.get("promotion_authority") is False, "HISTORICAL_PROMOTED", artifact_path)
        require(frozen.get(artifact_path, {}).get("sha256") == row.get("sha256"), "HISTORICAL_HASH", artifact_path)
        replacements = row.get("authoritative_replacements")
        require(isinstance(replacements, list) and bool(replacements), "HISTORICAL_REPLACEMENT_MISSING", artifact_path)
        for replacement in replacements:
            require(isinstance(replacement, str) and replacement in frozen, "HISTORICAL_REPLACEMENT_UNBOUND", replacement)
        classification = row.get("classification")
        require(
            isinstance(classification, str)
            and (classification.startswith("REVOKED_")
                 or classification.startswith("HISTORICAL_")
                 or classification.startswith("SUPERSEDED_")),
            "HISTORICAL_CLASSIFICATION_MISSING",
            artifact_path,
        )
        classifications[classification] += 1
    authoritative_path = value.get("authoritative_theorem_path")
    require(
        isinstance(authoritative_path, str) and authoritative_path in frozen,
        "AUTHORITATIVE_THEOREM_PATH_UNBOUND",
    )
    partitions = value.get("release_partitions")
    require(
        isinstance(partitions, dict)
        and set(partitions)
        == {
            "authoritative_proof_inputs",
            "bound_historical_provenance",
            "bound_runtime_evidence",
        },
        "AUTHORITY_PARTITION_DRIFT",
    )
    return {
        "artifact_count": len(artifacts),
        "payload_sha256": payload,
        "sha256": sha256_file(path_in(project, relative)),
        "authoritative_theorem_path": authoritative_path,
        "classifications": dict(sorted(classifications.items())),
        "release_partitions": partitions,
    }


def archive_audit(
    project: Path,
    archive_path: Path,
    expected_paths: list[str],
) -> dict[str, Any]:
    require(archive_path.is_file() and not archive_path.is_symlink(), "ARCHIVE_NOT_REGULAR")
    expected_names = [f"{ARCHIVE_PREFIX}/{relative}" for relative in expected_paths]
    with zipfile.ZipFile(archive_path, "r") as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        require(len(names) == len(set(names)), "ARCHIVE_DUPLICATE_NAMES")
        require(names == expected_names, "ARCHIVE_MEMBER_ORDER_OR_SET")
        require(archive.comment == b"", "ARCHIVE_COMMENT")
        compressed_total = 0
        expanded_total = 0
        for info, relative in zip(infos, expected_paths, strict=True):
            require(info.date_time == EXPECTED_ARCHIVE_TIMESTAMP, "ARCHIVE_TIMESTAMP", relative)
            require(info.compress_type == zipfile.ZIP_DEFLATED, "ARCHIVE_COMPRESSION", relative)
            require(info.create_system == 3, "ARCHIVE_CREATE_SYSTEM", relative)
            require((info.external_attr >> 16) == 0o100644, "ARCHIVE_MODE", relative)
            require(info.extra == b"" and info.comment == b"", "ARCHIVE_MEMBER_METADATA", relative)
            data = archive.read(info)
            project_data = path_in(project, relative).read_bytes()
            require(data == project_data, "ARCHIVE_MEMBER_BYTES", relative)
            compressed_total += info.compress_size
            expanded_total += info.file_size
    return {
        "bytes": archive_path.stat().st_size,
        "sha256": sha256_file(archive_path),
        "file_count": len(expected_paths),
        "compressed_member_bytes": compressed_total,
        "uncompressed_member_bytes": expanded_total,
        "member_timestamp": "2026-08-27T00:00:00",
        "member_mode": "100644",
        "member_order": "project-relative lexicographic",
    }


def git_output(repo: Path, arguments: list[str], *, binary: bool = False) -> bytes | str:
    result = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, "GIT_COMMAND_FAIL", f"{' '.join(arguments)}:{result.stderr.decode(errors='replace')}")
    return result.stdout if binary else result.stdout.decode("utf-8", errors="strict").strip()


def tag_audit(
    project: Path,
    repo: Path,
    actual_paths: list[str],
    telemetry: dict[str, Any],
    archive: dict[str, Any],
) -> dict[str, Any]:
    top = Path(str(git_output(repo, ["rev-parse", "--show-toplevel"])))
    project_prefix = Path(repo.resolve().relative_to(top.resolve())).as_posix()
    tag_type = str(git_output(top, ["cat-file", "-t", EXPECTED_TAG]))
    require(tag_type == "tag", "TAG_NOT_ANNOTATED")
    tag_commit = str(git_output(top, ["rev-parse", f"{EXPECTED_TAG}^{{}}"] ))
    telemetry_commit = telemetry.get("git_commit")
    require(isinstance(telemetry_commit, str), "TELEMETRY_COMMIT_MISSING")
    require(str(git_output(top, ["cat-file", "-t", telemetry_commit])) == "commit", "TELEMETRY_COMMIT_ABSENT")
    ancestor = subprocess.run(
        ["git", "-C", str(top), "merge-base", "--is-ancestor", telemetry_commit, tag_commit],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(ancestor.returncode == 0, "TELEMETRY_COMMIT_NOT_ANCESTOR")

    tree_raw = git_output(
        top,
        ["ls-tree", "-r", "-z", "--long", tag_commit, "--", project_prefix],
        binary=True,
    )
    require(isinstance(tree_raw, bytes), "GIT_TREE_OUTPUT_TYPE")
    tree: dict[str, tuple[str, str, int]] = {}
    for entry in tree_raw.split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, oid, size = metadata.decode().split()
        require(kind == "blob", "TAG_NONBLOB_MEMBER", raw_path)
        full_path = raw_path.decode("utf-8")
        if full_path == project_prefix:
            continue
        prefix = f"{project_prefix}/"
        require(full_path.startswith(prefix), "TAG_PATH_PREFIX", full_path)
        tree[full_path[len(prefix):]] = (mode, oid, int(size))
    package_modes = Counter()
    for relative in actual_paths:
        tagged = tree.get(relative)
        require(tagged is not None, "TAG_OMITS_PACKAGE_FILE", relative)
        path = path_in(project, relative)
        require(tagged[0] in {"100644", "100755"}, "TAG_PACKAGE_FILE_MODE", relative)
        package_modes[tagged[0]] += 1
        require(tagged[2] == path.stat().st_size, "TAG_FILE_SIZE", relative)
        require(tagged[1] == git_blob_sha1_file(path), "TAG_FILE_BYTES", relative)

    for relative in (*TELEMETRY_SOURCES, LOCK_RELATIVE):
        old_oid = str(git_output(top, ["rev-parse", f"{telemetry_commit}:{project_prefix}/{relative}"]))
        tag_oid = str(git_output(top, ["rev-parse", f"{tag_commit}:{project_prefix}/{relative}"]))
        require(old_oid == tag_oid, "TELEMETRY_BOUND_FILE_CHANGED_AFTER_REPLAY", relative)

    digest_relative = (
        "proof_compression_submission/output/"
        "K2P_Principal_D_Plus_Referee_Package_20260828.zip.sha256"
    )
    digest_bytes = git_output(top, ["show", f"{tag_commit}:{project_prefix}/{digest_relative}"], binary=True)
    require(isinstance(digest_bytes, bytes), "TAG_ARCHIVE_DIGEST_TYPE")
    expected_line = (
        f"{archive['sha256']}  K2P_Principal_D_Plus_Referee_Package_20260828.zip\n"
    ).encode()
    require(digest_bytes == expected_line, "TAG_ARCHIVE_DIGEST_MISMATCH")
    return {
        "tag": EXPECTED_TAG,
        "tag_object_type": tag_type,
        "tag_commit": tag_commit,
        "telemetry_commit": telemetry_commit,
        "telemetry_commit_is_ancestor": True,
        "package_files_byte_identical_to_tag": len(actual_paths),
        "tagged_package_file_modes": dict(sorted(package_modes.items())),
        "telemetry_bound_files_unchanged_through_tag": len(TELEMETRY_SOURCES) + 1,
        "archive_digest_file_matches": True,
    }


def main() -> int:
    require(__debug__, "OPTIMIZED_PYTHON_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--git-repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-deep-json", action="store_true")
    args = parser.parse_args()

    project = args.project.resolve()
    require(project.is_dir() and not project.is_symlink(), "PROJECT_ROOT_MISSING")
    lock_path = path_in(project, LOCK_RELATIVE)
    lock = strict_object(lock_path, LOCK_RELATIVE)
    lock_payload = verify_payload(lock, LOCK_RELATIVE)
    lock_sha = sha256_file(lock_path)
    require(lock.get("promotion_ready") is True, "LOCK_NOT_PROMOTION_READY")
    require(lock.get("blockers") == [] and lock.get("missing_required_files") == [], "LOCK_HAS_BLOCKERS")

    frozen, nested_counts = frozen_ledger(project, lock, lock_sha)
    portable = strict_object(path_in(project, PORTABLE_LEDGER_RELATIVE), PORTABLE_LEDGER_RELATIVE)
    check_declared_ledger(portable, frozen, "portable_frozen")
    require(portable.get("release_lock_sha256") == lock_sha, "PORTABLE_LOCK_SHA")
    require(portable.get("release_lock_payload_sha256") == lock_payload, "PORTABLE_LOCK_PAYLOAD")

    submission = submission_ledger(project)
    manifest = strict_object(path_in(project, MANIFEST_RELATIVE), MANIFEST_RELATIVE)
    manifest_payload = verify_payload(manifest, MANIFEST_RELATIVE)
    check_declared_ledger(manifest.get("frozen_evidence", {}), frozen, "manifest_frozen")
    check_declared_ledger(manifest.get("submission_sources", {}), submission, "manifest_submission")
    require(set(frozen).isdisjoint(submission), "FROZEN_SUBMISSION_OVERLAP")
    combined = {"frozen_evidence": frozen, "submission_sources": submission}
    require(manifest.get("combined_content_root_sha256") == canonical_hash(combined), "COMBINED_ROOT")
    require(manifest.get("combined_file_count_excluding_manifest") == len(frozen) + len(submission), "COMBINED_COUNT")

    actual_paths = sorted(
        path.relative_to(project).as_posix()
        for path in project.rglob("*")
        if path.is_file() and not path.is_symlink()
    )
    expected_set = set(frozen) | set(submission) | {MANIFEST_RELATIVE}
    require(set(actual_paths) == expected_set, "PACKAGE_FILE_SET", {
        "missing": sorted(expected_set - set(actual_paths))[:5],
        "extra": sorted(set(actual_paths) - expected_set)[:5],
    })
    require(not any(path.is_symlink() for path in project.rglob("*")), "PACKAGE_HAS_SYMLINK")

    json_scan = (
        {"skipped": True}
        if args.skip_deep_json
        else scan_strict_json_members(project, sorted(set(frozen) | set(submission) | {MANIFEST_RELATIVE}))
    )
    crosswalk = verify_crosswalk(project, frozen, submission)
    telemetry = verify_telemetry(project, lock, lock_sha)
    pdf_report = verify_pdf_report(project, submission)
    historical = verify_historical_registry(project, frozen)
    archive_paths = sorted(set(frozen) | set(submission) | {MANIFEST_RELATIVE})
    archive = archive_audit(project, args.archive.resolve(), archive_paths)
    tag = tag_audit(project, args.git_repo.resolve(), actual_paths, telemetry, archive)

    outer_layer_counts = Counter()
    outer_layer_bytes = Counter()
    for row in lock["files"].values():
        layer = str(row.get("layer"))
        outer_layer_counts[layer] += 1
        outer_layer_bytes[layer] += int(row.get("bytes", 0))

    supplemental = {
        relative: {
            **file_row(path_in(project, relative)),
            "inside_frozen_ledger": relative in frozen,
            "inside_submission_ledger": relative in submission,
        }
        for relative in sorted(SUPPLEMENTAL_DEPENDENCIES)
    }

    result: dict[str, Any] = {
        "schema": "k2p-r5-independent-provenance-audit-v1",
        "status": "PASS",
        "project_root": str(project),
        "source_archive": str(args.archive.resolve()),
        "source_archive_evidence": archive,
        "release_lock": {
            "bytes": lock_path.stat().st_size,
            "sha256": lock_sha,
            "payload_sha256": lock_payload,
            "promotion_ready": lock.get("promotion_ready"),
            "candidate_outcome": lock.get("candidate_outcome"),
            "scope": lock.get("scope"),
            "outer_locked_file_count": len(lock["files"]),
            "outer_locked_total_bytes": sum(int(row["bytes"]) for row in lock["files"].values()),
            "outer_layer_file_counts": dict(sorted(outer_layer_counts.items())),
            "outer_layer_total_bytes": dict(sorted(outer_layer_bytes.items())),
            "nested_counts": nested_counts,
        },
        "frozen_recursive_ledger": {
            "file_count": len(frozen),
            "total_bytes": sum(int(row["bytes"]) for row in frozen.values()),
            "content_ledger_root_sha256": canonical_hash(frozen),
            "portable_ledger_bytes": path_in(project, PORTABLE_LEDGER_RELATIVE).stat().st_size,
            "portable_ledger_sha256": sha256_file(path_in(project, PORTABLE_LEDGER_RELATIVE)),
        },
        "submission_ledger": {
            "file_count": len(submission),
            "total_bytes": sum(int(row["bytes"]) for row in submission.values()),
            "content_ledger_root_sha256": canonical_hash(submission),
        },
        "combined_manifest": {
            "file_count_excluding_manifest": len(frozen) + len(submission),
            "package_file_count_including_manifest": len(actual_paths),
            "content_root_sha256": canonical_hash(combined),
            "manifest_bytes": path_in(project, MANIFEST_RELATIVE).stat().st_size,
            "manifest_sha256": sha256_file(path_in(project, MANIFEST_RELATIVE)),
            "manifest_payload_sha256": manifest_payload,
            "status": manifest.get("status"),
        },
        "supplemental_execution_dependencies": supplemental,
        "strict_json_scan": json_scan,
        "theorem_artifact_crosswalk": crosswalk,
        "clean_replay_telemetry": telemetry,
        "pdf_build_report": pdf_report,
        "historical_authority_registry": historical,
        "git_tag_binding": tag,
    }
    result["payload_sha256"] = canonical_hash(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "payload_sha256": result["payload_sha256"],
        "frozen_file_count": len(frozen),
        "submission_file_count": len(submission),
        "package_file_count": len(actual_paths),
        "archive_sha256": archive["sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditFailure as error:
        raise SystemExit(f"INDEPENDENT_PROVENANCE_AUDIT_FAIL:{error}") from error
