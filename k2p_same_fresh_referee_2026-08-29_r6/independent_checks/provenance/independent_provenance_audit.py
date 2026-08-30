#!/usr/bin/env python3
"""Independent byte/provenance audit for the R6 referee archive.

This program deliberately imports no submitted module.  It reconstructs the
recursive evidence ledger and submission ledger, checks the deterministic ZIP,
telemetry, crosswalk references, PDF build report, and annotated Git tag from
the underlying bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


LOCK_RELATIVE = "work/final_theorem_release/RELEASE_LOCK.json"
PORTABLE_RELATIVE = "output/referee/REFEREE_BUNDLE_CONTENTS.json"
MANIFEST_RELATIVE = (
    "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
)
ARCHIVE_PREFIX = "k2p_principal_d_plus_submission_referee"
ARCHIVE_TIME = (2026, 8, 27, 0, 0, 0)
TELEMETRY_SOURCES = (
    "proof_compression_submission/article/main.tex",
    "proof_compression_submission/article/references.bib",
    "proof_compression_submission/supplement/supplement.tex",
    "proof_compression_submission/supplement/compression_tables.tex",
    "proof_compression_submission/supplement/certificate_appendix.tex",
)
OPERATIONAL = {
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json",
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json",
    "proof_compression_submission/output/FINAL_RELEASE_MUTATIONS.json",
    "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf",
    "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf",
    "proof_compression_submission/output/logs/article.log",
    "proof_compression_submission/output/logs/supplement.log",
}
SUPPLEMENTAL = {
    "output/referee/README.md",
    PORTABLE_RELATIVE,
    "output/referee/build_referee_bundle.py",
}


class Failure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise Failure(code if detail is None else f"{code}:{detail}")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_blob(path: Path) -> str:
    digest = hashlib.sha1(usedforsecurity=False)
    size = path.stat().st_size
    digest.update(f"blob {size}\0".encode())
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode()


def canonical_hash(value: object) -> str:
    return sha_bytes(canonical(value))


def strict_json_bytes(data: bytes, label: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, "DUPLICATE_JSON_NAME", f"{label}:{key}")
            result[key] = value
        return result

    def constant(token: str) -> None:
        raise Failure(f"NONFINITE_JSON:{label}:{token}")

    def floating(token: str) -> float:
        value = float(token)
        require(math.isfinite(value), "NONFINITE_FLOAT", f"{label}:{token}")
        return value

    try:
        return json.loads(
            data.decode("utf-8"), object_pairs_hook=pairs,
            parse_constant=constant, parse_float=floating,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Failure(f"JSON_DECODE:{label}:{error}") from error


def strict_object(path: Path, label: str) -> dict[str, Any]:
    value = strict_json_bytes(path.read_bytes(), label)
    require(isinstance(value, dict), "JSON_NOT_OBJECT", label)
    return value


def safe(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    require(
        not path.is_absolute() and bool(path.parts)
        and all(part not in {"", ".", ".."} for part in path.parts),
        "UNSAFE_PATH", value,
    )
    return path


def project_path(root: Path, relative: str) -> Path:
    return root.joinpath(*safe(relative).parts)


def row(path: Path) -> dict[str, int | str]:
    require(path.is_file() and not path.is_symlink(), "NOT_REGULAR", path)
    return {"bytes": path.stat().st_size, "sha256": sha_file(path)}


def verify_payload(value: dict[str, Any], label: str) -> str:
    expected = value.get("payload_sha256")
    unsigned = dict(value)
    unsigned.pop("payload_sha256", None)
    require(expected == canonical_hash(unsigned), "PAYLOAD_MISMATCH", label)
    return str(expected)


def add_sha_manifest(
    root: Path, expected: dict[str, str], manifest: str, base: str
) -> int:
    count = 0
    for number, line in enumerate(
        project_path(root, manifest).read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "MANIFEST_LINE", f"{manifest}:{number}")
        digest, child = match.groups()
        relative = (PurePosixPath(base) / safe(child)).as_posix()
        prior = expected.get(relative)
        require(prior is None or prior == digest, "NESTED_CONFLICT", relative)
        expected[relative] = digest
        count += 1
    return count


def frozen_ledger(
    root: Path, lock: dict[str, Any], lock_sha: str
) -> tuple[dict[str, dict[str, int | str]], dict[str, int]]:
    files = lock.get("files")
    require(isinstance(files, dict), "LOCK_FILES")
    expected: dict[str, str] = {}
    for relative, metadata in files.items():
        require(isinstance(relative, str) and isinstance(metadata, dict), "LOCK_ROW")
        expected[relative] = str(metadata.get("sha256"))
    counts = {
        "outer_rows": len(files),
        "rank_manifest_rows": add_sha_manifest(
            root, expected, "work/rank_upper_certificates/MANIFEST.sha256",
            "work/rank_upper_certificates",
        ),
        "cycle_manifest_rows": add_sha_manifest(
            root, expected, "work/cycle_three_port_closure/MANIFEST.sha256",
            "work/cycle_three_port_closure",
        ),
    }
    direct = PurePosixPath("package/referee/k2p_offline_sweep_portable")
    for name, key in (
        ("DIRECT_CLOSURE_LOCK.json", "direct_closure_rows"),
        ("INPUT_LOCK.json", "direct_input_rows"),
    ):
        relative = (direct / name).as_posix()
        nested = strict_object(project_path(root, relative), relative)
        nested_files = nested.get("files")
        require(isinstance(nested_files, dict), "DIRECT_FILES", name)
        counts[key] = len(nested_files)
        for child, digest in nested_files.items():
            joined = (direct / safe(str(child))).as_posix()
            prior = expected.get(joined)
            require(prior is None or prior == digest, "DIRECT_CONFLICT", joined)
            expected[joined] = str(digest)
    expected[LOCK_RELATIVE] = lock_sha

    ledger: dict[str, dict[str, int | str]] = {}
    for relative in sorted(expected):
        metadata = row(project_path(root, relative))
        require(metadata["sha256"] == expected[relative], "FROZEN_HASH", relative)
        outer = files.get(relative)
        if isinstance(outer, dict):
            require(
                metadata["sha256"] == outer.get("sha256")
                and metadata["bytes"] == outer.get("bytes"),
                "OUTER_ROW", relative,
            )
        ledger[relative] = metadata
    return ledger, counts


def include_submission(relative: PurePosixPath) -> bool:
    if not relative.parts or relative.parts[0] != "proof_compression_submission":
        return False
    if relative.as_posix() == MANIFEST_RELATIVE:
        return False
    if relative.as_posix() in OPERATIONAL:
        return True
    if (
        "output" in relative.parts or "__pycache__" in relative.parts
        or any(part.startswith(".") for part in relative.parts[1:-1])
    ):
        return False
    return relative.name != ".DS_Store" and relative.suffix not in {".pyc", ".pyo"}


def submission_ledger(root: Path) -> dict[str, dict[str, int | str]]:
    ledger: dict[str, dict[str, int | str]] = {}
    for path in sorted((root / "proof_compression_submission").rglob("*")):
        if path.is_dir():
            continue
        relative = PurePosixPath(path.relative_to(root).as_posix())
        if include_submission(relative):
            ledger[relative.as_posix()] = row(path)
    for relative in sorted(SUPPLEMENTAL):
        ledger[relative] = row(project_path(root, relative))
    return dict(sorted(ledger.items()))


def crosswalk_audit(root: Path) -> dict[str, Any]:
    relative = "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json"
    value = strict_object(project_path(root, relative), relative)
    payload = verify_payload(value, relative)
    bindings: list[tuple[str, str]] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            if isinstance(node.get("path"), str) and isinstance(node.get("sha256"), str):
                bindings.append((node["path"], node["sha256"]))
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    for path_text, digest in bindings:
        path = project_path(root, path_text)
        require(path.is_file() and sha_file(path) == digest, "CROSSWALK_BINDING", path_text)
    return {
        "status": value.get("status"), "sha256": sha_file(project_path(root, relative)),
        "payload_sha256": payload, "path_sha_bindings_checked": len(bindings),
    }


def telemetry_audit(root: Path, lock: dict[str, Any], lock_sha: str) -> dict[str, Any]:
    report_rel = "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json"
    telemetry_rel = "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json"
    report = strict_object(project_path(root, report_rel), report_rel)
    telemetry = strict_object(project_path(root, telemetry_rel), telemetry_rel)
    layers = report.get("layer_replays")
    require(
        report.get("status") == "PASS" and report.get("mode") == "full"
        and report.get("promotion_ready") is True and isinstance(layers, list)
        and len(layers) == 41 and not report.get("blockers"),
        "FULL_REPLAY_REPORT",
    )
    require(
        telemetry.get("status") == "PASS"
        and telemetry.get("clean_detached_checkout") is True,
        "TELEMETRY_STATUS",
    )
    require(telemetry.get("report", {}).get("sha256") == sha_file(project_path(root, report_rel)), "TELEMETRY_REPORT")
    expected_sources = {name: row(project_path(root, name)) for name in TELEMETRY_SOURCES}
    require(telemetry.get("submission_sources") == expected_sources, "TELEMETRY_SOURCES")
    expected_lock = {
        "bytes": project_path(root, LOCK_RELATIVE).stat().st_size,
        "path": LOCK_RELATIVE,
        "payload_sha256": lock.get("payload_sha256"),
        "sha256": lock_sha,
    }
    require(telemetry.get("release_lock") == expected_lock, "TELEMETRY_LOCK")
    require(
        telemetry.get("time_l", {}).get("real_seconds", 0) >= report.get("elapsed_seconds", 1),
        "TELEMETRY_RUNTIME",
    )
    return {
        "git_commit": telemetry.get("git_commit"), "layer_count": len(layers),
        "report_sha256": sha_file(project_path(root, report_rel)),
        "telemetry_sha256": sha_file(project_path(root, telemetry_rel)),
        "internal_elapsed_seconds": report.get("elapsed_seconds"),
        "real_seconds": telemetry.get("time_l", {}).get("real_seconds"),
        "maximum_resident_set_size_bytes": telemetry.get("time_l", {}).get("maximum_resident_set_size_bytes"),
        "peak_memory_footprint_bytes": telemetry.get("time_l", {}).get("peak_memory_footprint_bytes"),
    }


def pdf_report_audit(root: Path, submission: dict[str, dict[str, int | str]]) -> dict[str, Any]:
    relative = "proof_compression_submission/PDF_BUILD_REPORT.json"
    value = strict_object(project_path(root, relative), relative)
    payload = verify_payload(value, relative)
    require(value.get("source_set") == [
        "article/main.tex", "article/references.bib", "supplement/supplement.tex",
        "supplement/compression_tables.tex", "supplement/certificate_appendix.tex",
    ], "PDF_SOURCE_SET")
    rows: dict[str, Any] = {}
    for kind in ("article", "supplement"):
        report_row = value[kind]
        pdf_relative = report_row["pdf_path"]
        actual = row(project_path(root, pdf_relative))
        require(actual == {"bytes": report_row["bytes"], "sha256": report_row["pdf_sha256"]}, "PDF_ROW", kind)
        require(submission.get(pdf_relative) == actual, "PDF_SUBMISSION_BINDING", kind)
        require(sha_file(project_path(root, report_row["source_path"])) == report_row["source_sha256"], "PDF_SOURCE", kind)
        log_relative = f"proof_compression_submission/output/logs/{kind}.log"
        require(sha_file(project_path(root, log_relative)) == report_row["log_sha256"], "PDF_LOG", kind)
        log = project_path(root, log_relative).read_text(encoding="utf-8", errors="replace")
        require("Overfull \\hbox" not in log and "Overfull \\vbox" not in log, "PDF_OVERFULL", kind)
        require(not re.search(r"^! ", log, re.MULTILINE), "PDF_FATAL", kind)
        rows[kind] = report_row
    return {"sha256": sha_file(project_path(root, relative)), "payload_sha256": payload, "status": value.get("status"), **rows}


def archive_audit(root: Path, archive_path: Path, expected: list[str]) -> dict[str, Any]:
    expected_names = [f"{ARCHIVE_PREFIX}/{relative}" for relative in expected]
    compressed = expanded = 0
    with zipfile.ZipFile(archive_path) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        require(len(names) == len(set(names)), "ZIP_DUPLICATE")
        require(names == expected_names, "ZIP_ORDER_OR_SET")
        require(archive.comment == b"", "ZIP_COMMENT")
        for info, relative in zip(infos, expected, strict=True):
            require(info.date_time == ARCHIVE_TIME, "ZIP_TIME", relative)
            require(info.compress_type == zipfile.ZIP_DEFLATED, "ZIP_COMPRESSION", relative)
            require(info.create_system == 3 and (info.external_attr >> 16) == 0o100644, "ZIP_MODE", relative)
            require(info.extra == b"" and info.comment == b"" and not (info.flag_bits & 1), "ZIP_METADATA", relative)
            data = archive.read(info)
            require(data == project_path(root, relative).read_bytes(), "ZIP_BYTES", relative)
            compressed += info.compress_size
            expanded += info.file_size
    return {
        "sha256": sha_file(archive_path), "bytes": archive_path.stat().st_size,
        "file_count": len(expected), "compressed_member_bytes": compressed,
        "uncompressed_member_bytes": expanded, "unique_regular_members": True,
        "lexicographic_order": True, "fixed_timestamp": "2026-08-27T00:00:00",
        "mode": "100644", "encryption": False,
    }


def git_command(repo: Path, args: list[str], binary: bool = False) -> bytes | str:
    result = subprocess.run(["git", "-C", str(repo), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    require(result.returncode == 0, "GIT_COMMAND", f"{' '.join(args)}:{result.stderr.decode(errors='replace')}")
    return result.stdout if binary else result.stdout.decode().strip()


def tag_audit(
    root: Path, repo: Path, paths: list[str], telemetry: dict[str, Any],
    expected_tag: str, expected_commit: str,
) -> dict[str, Any]:
    top = Path(str(git_command(repo, ["rev-parse", "--show-toplevel"])))
    prefix = repo.resolve().relative_to(top.resolve()).as_posix()
    require(git_command(top, ["cat-file", "-t", f"refs/tags/{expected_tag}"]) == "tag", "TAG_NOT_ANNOTATED")
    tag_commit = str(git_command(top, ["rev-parse", f"{expected_tag}^{{}}"] ))
    require(tag_commit == expected_commit, "TAG_COMMIT", tag_commit)
    telemetry_commit = str(telemetry["git_commit"])
    ancestor = subprocess.run(["git", "-C", str(top), "merge-base", "--is-ancestor", telemetry_commit, tag_commit], check=False)
    require(ancestor.returncode == 0, "TELEMETRY_NOT_ANCESTOR")
    raw = git_command(top, ["ls-tree", "-r", "-z", "--long", tag_commit, "--", prefix], binary=True)
    require(isinstance(raw, bytes), "TREE_TYPE")
    tree: dict[str, tuple[str, str, int]] = {}
    for item in raw.split(b"\0"):
        if not item:
            continue
        header, name = item.split(b"\t", 1)
        mode, kind, oid, size = header.decode().split()
        require(kind == "blob", "TREE_NON_BLOB", name)
        full = name.decode()
        tree[full[len(prefix) + 1:]] = (mode, oid, int(size))
    modes = Counter()
    for relative in paths:
        tagged = tree.get(relative)
        require(tagged is not None, "TAG_MISSING", relative)
        path = project_path(root, relative)
        require(tagged[2] == path.stat().st_size and tagged[1] == git_blob(path), "TAG_BYTES", relative)
        modes[tagged[0]] += 1
    unchanged = 0
    for relative in (*TELEMETRY_SOURCES, LOCK_RELATIVE):
        before = git_command(top, ["rev-parse", f"{telemetry_commit}:{prefix}/{relative}"])
        after = git_command(top, ["rev-parse", f"{tag_commit}:{prefix}/{relative}"])
        require(before == after, "POST_TELEMETRY_CHANGE", relative)
        unchanged += 1
    return {
        "tag": expected_tag, "tag_object_type": "tag", "tag_commit": tag_commit,
        "telemetry_commit": telemetry_commit, "telemetry_commit_is_ancestor": True,
        "package_files_byte_identical_to_tag": len(paths),
        "tagged_package_file_modes": dict(sorted(modes.items())),
        "telemetry_bound_files_unchanged_through_tag": unchanged,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--git-repo", type=Path, required=True)
    parser.add_argument("--expected-tag", default="k2p-same-biorxiv-v1.0.5")
    parser.add_argument("--expected-tag-commit", default="5628a08f6bf3e5573ebbbf3e2dd8636ad00b338e")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project.resolve()

    lock_path = project_path(root, LOCK_RELATIVE)
    lock = strict_object(lock_path, LOCK_RELATIVE)
    lock_sha = sha_file(lock_path)
    lock_payload = verify_payload(lock, LOCK_RELATIVE)
    require(lock.get("promotion_ready") is True and not lock.get("blockers") and not lock.get("missing_required_files"), "LOCK_NOT_READY")
    frozen, nested_counts = frozen_ledger(root, lock, lock_sha)
    frozen_root = canonical_hash(frozen)
    frozen_bytes = sum(int(value["bytes"]) for value in frozen.values())

    portable = strict_object(project_path(root, PORTABLE_RELATIVE), PORTABLE_RELATIVE)
    require(portable.get("files") == frozen, "PORTABLE_LEDGER_FILES")
    require(portable.get("file_count") == len(frozen) and portable.get("total_bytes") == frozen_bytes and portable.get("content_ledger_root_sha256") == frozen_root, "PORTABLE_LEDGER_SUMMARY")
    require(portable.get("release_lock_sha256") == lock_sha and portable.get("release_lock_payload_sha256") == lock_payload, "PORTABLE_LOCK_BINDING")

    submission = submission_ledger(root)
    submission_root = canonical_hash(submission)
    submission_bytes = sum(int(value["bytes"]) for value in submission.values())
    manifest = strict_object(project_path(root, MANIFEST_RELATIVE), MANIFEST_RELATIVE)
    manifest_payload = verify_payload(manifest, MANIFEST_RELATIVE)
    require(manifest["frozen_evidence"]["files"] == frozen, "MANIFEST_FROZEN")
    require(manifest["submission_sources"]["files"] == submission, "MANIFEST_SUBMISSION")
    require(manifest["frozen_evidence"]["content_ledger_root_sha256"] == frozen_root, "MANIFEST_FROZEN_ROOT")
    require(manifest["submission_sources"]["content_ledger_root_sha256"] == submission_root, "MANIFEST_SUBMISSION_ROOT")
    combined_root = canonical_hash({"frozen_evidence": frozen, "submission_sources": submission})
    require(manifest.get("combined_content_root_sha256") == combined_root, "MANIFEST_COMBINED_ROOT")
    require(manifest.get("combined_file_count_excluding_manifest") == len(frozen) + len(submission), "MANIFEST_COUNT")
    require(manifest.get("submission_metadata", {}).get("versioned_annotated_source_tag") == args.expected_tag, "MANIFEST_TAG")

    expected_paths = sorted(set(frozen) | set(submission) | {MANIFEST_RELATIVE})
    archive = archive_audit(root, args.archive.resolve(), expected_paths)
    telemetry = telemetry_audit(root, lock, lock_sha)
    crosswalk = crosswalk_audit(root)
    pdf_report = pdf_report_audit(root, submission)
    tag = tag_audit(root, args.git_repo.resolve(), expected_paths, telemetry, args.expected_tag, args.expected_tag_commit)

    result: dict[str, Any] = {
        "schema": "k2p-r6-independent-provenance-audit-v1", "status": "PASS",
        "archive": archive,
        "release_lock": {"sha256": lock_sha, "bytes": lock_path.stat().st_size, "payload_sha256": lock_payload, "promotion_ready": True},
        "frozen_evidence": {"file_count": len(frozen), "total_bytes": frozen_bytes, "content_ledger_root_sha256": frozen_root, "nested_counts": nested_counts, "portable_ledger_sha256": sha_file(project_path(root, PORTABLE_RELATIVE))},
        "submission_sources": {"file_count": len(submission), "total_bytes": submission_bytes, "content_ledger_root_sha256": submission_root, "supplemental_execution_dependencies": sorted(SUPPLEMENTAL)},
        "combined": {"file_count_excluding_manifest": len(frozen) + len(submission), "content_root_sha256": combined_root, "manifest_sha256": sha_file(project_path(root, MANIFEST_RELATIVE)), "manifest_payload_sha256": manifest_payload},
        "telemetry": telemetry, "crosswalk": crosswalk, "pdf_build_report": pdf_report,
        "git_tag_binding": tag,
    }
    result["payload_sha256"] = canonical_hash(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "payload_sha256": result["payload_sha256"], "archive_sha256": archive["sha256"], "package_files": len(expected_paths)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, sort_keys=True))
        raise SystemExit(1) from error
