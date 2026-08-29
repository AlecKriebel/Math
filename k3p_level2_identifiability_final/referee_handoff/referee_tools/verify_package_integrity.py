#!/usr/bin/env python3
"""Verify the sealed delivered payload and canonical proof-core manifest.

Reviewer-created ``.venv`` and ``review_runs`` directories are deliberately
outside this seal, including their contents, modes, and symlink targets.  This
gate binds bytes and modes of every delivered payload file; it does not inspect
the compressed archive container itself.  After execution, use the runner's
complete before/after inventories—not this check alone—to establish drift.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile


class IntegrityFailure(RuntimeError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise IntegrityFailure(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def zip_datetime(epoch: int) -> tuple[int, int, int, int, int, int]:
    import datetime as dt
    value = dt.datetime.fromtimestamp(max(epoch, 315532800), tz=dt.timezone.utc)
    return (value.year, value.month, value.day, value.hour, value.minute,
            value.second - value.second % 2)


def mode_string(mode: int) -> str:
    return format(stat.S_IMODE(mode), "04o")


def safe_relative(value: str) -> str:
    require(isinstance(value, str) and "\\" not in value and "\x00" not in value,
            ("unsafe package path characters", value))
    path = PurePosixPath(value)
    require(value and not path.is_absolute() and ".." not in path.parts,
            ("unsafe package path", value))
    normalized = path.as_posix()
    require(normalized == value and value not in {".", ""},
            ("noncanonical package path", value))
    return value


def is_runtime_path(relative: str) -> bool:
    parts = PurePosixPath(relative).parts
    return (
        relative in {"PACKAGE_MANIFEST.json", "SHA256SUMS"}
        or (parts and parts[0] in {".venv", "review_runs"})
    )


def observed_payload(root: Path) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        safe_relative(relative)
        metadata = path.lstat()
        if is_runtime_path(relative):
            if relative in {".venv", "review_runs"}:
                require(not stat.S_ISLNK(metadata.st_mode) and
                        stat.S_ISDIR(metadata.st_mode),
                        ("runtime root must be a real directory", relative))
            continue
        require(not stat.S_ISLNK(metadata.st_mode),
                ("symlink forbidden in sealed payload", relative))
        if stat.S_ISDIR(metadata.st_mode):
            continue
        require(stat.S_ISREG(metadata.st_mode),
                ("nonregular object forbidden in sealed payload", relative))
        result[relative] = {
            "bytes": metadata.st_size,
            "mode": mode_string(metadata.st_mode),
            "sha256": sha256_file(path),
        }
    return result


def verify_outer(root: Path) -> dict[str, object]:
    manifest_path = root / "PACKAGE_MANIFEST.json"
    sums_path = root / "SHA256SUMS"
    require(manifest_path.is_file() and not manifest_path.is_symlink() and
            sums_path.is_file() and not sums_path.is_symlink(),
            "missing outer package manifest")
    require(mode_string(manifest_path.lstat().st_mode) == "0644" and
            mode_string(sums_path.lstat().st_mode) == "0644",
            "outer manifest files must have mode 0644")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    required = {
        "schema", "package_name", "package_builder_commit",
        "proof_source_commit", "canonical_archive_sha256",
        "payload_file_count", "payload_bytes", "payload",
    }
    require(set(manifest) == required and
            manifest.get("schema") == "k3p-independent-referee-package-v2",
            "outer package manifest schema")
    require(re.fullmatch(r"[0-9a-f]{40}", str(
                manifest.get("package_builder_commit"))) is not None and
            re.fullmatch(r"[0-9a-f]{40}", str(
                manifest.get("proof_source_commit"))) is not None and
            re.fullmatch(r"[0-9a-f]{64}", str(
                manifest.get("canonical_archive_sha256"))) is not None,
            "outer package identity fields")
    rows = manifest.get("payload")
    require(isinstance(rows, list), "outer package payload rows")
    expected: dict[str, dict[str, object]] = {}
    for row in rows:
        require(isinstance(row, dict) and
                set(row) == {"path", "bytes", "mode", "sha256"},
                ("outer payload row", row))
        relative = safe_relative(row["path"])
        require(relative not in expected and isinstance(row["bytes"], int) and
                row["bytes"] >= 0 and
                re.fullmatch(r"0[0-7]{3}", str(row["mode"])) is not None and
                isinstance(row["sha256"], str) and
                re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None,
                ("outer payload row fields", relative))
        expected[relative] = {
            "bytes": row["bytes"], "mode": row["mode"],
            "sha256": row["sha256"],
        }
    observed = observed_payload(root)
    require(observed == expected,
            ("outer package payload mismatch",
             sorted(set(expected) - set(observed)),
             sorted(set(observed) - set(expected)),
             sorted(path for path in set(expected) & set(observed)
                    if expected[path] != observed[path])))
    require(manifest["payload_file_count"] == len(expected) and
            manifest["payload_bytes"] == sum(row["bytes"] for row in expected.values()),
            "outer payload totals")

    sums: dict[str, str] = {}
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        digest, separator, relative = line.partition("  ")
        require(separator == "  " and
                re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
                ("malformed SHA256SUMS line", line))
        safe_relative(relative)
        require(relative not in sums, ("duplicate SHA256SUMS path", relative))
        sums[relative] = digest
    expected_sum_paths = set(expected) | {"PACKAGE_MANIFEST.json"}
    require(set(sums) == expected_sum_paths, "SHA256SUMS path set")
    for relative, digest in sums.items():
        require(sha256_file(root / relative) == digest,
                ("SHA256SUMS mismatch", relative))
    return {
        "payload_file_count": len(expected),
        "payload_bytes": manifest["payload_bytes"],
        "package_builder_commit": manifest["package_builder_commit"],
        "proof_source_commit": manifest["proof_source_commit"],
    }


def verify_inner(root: Path, proof_source_commit: str) -> dict[str, object]:
    proof = root / "proof_package"
    manifest_path = proof / "ARCHIVE_MANIFEST.json"
    require(manifest_path.is_file() and not manifest_path.is_symlink(),
            "missing proof-core archive manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest.get("source_commit") == proof_source_commit and
            manifest.get("kind") == "full_reproducibility",
            "proof-core manifest identity")
    rows = manifest.get("members")
    require(isinstance(rows, list) and
            manifest.get("member_count_excluding_manifest") == len(rows),
            "proof-core member count")
    seen: set[str] = set()
    total = 0
    for row in rows:
        require(isinstance(row, dict) and
                set(row) == {"path", "bytes", "mode", "sha256"},
                ("proof-core member row", row))
        relative = safe_relative(row["path"])
        require(relative not in seen and isinstance(row["bytes"], int) and
                row["bytes"] >= 0 and
                re.fullmatch(r"[0-9a-f]{64}", str(row["sha256"])) is not None and
                re.fullmatch(r"0[67][0-7]{2}", str(row["mode"])) is not None,
                ("invalid proof-core member", relative))
        seen.add(relative)
        path = proof / relative
        require(path.is_file() and not path.is_symlink() and
                stat.S_ISREG(path.lstat().st_mode) and
                mode_string(path.lstat().st_mode) == row["mode"] and
                path.stat().st_size == row["bytes"] and
                sha256_file(path) == row["sha256"],
                ("proof-core member mismatch", relative))
        total += row["bytes"]
    return {
        "core_member_count": len(rows),
        "core_member_bytes": total,
        "core_member_modes_checked": True,
    }


def validate_cache_manifest(cache_contract: dict, policy: dict,
                            cache_sha256: str) -> None:
    require(set(cache_contract) == {
        "schema", "bundle_url", "bundle_digest", "cache_layout",
        "bundle_hash_pointer", "file_count", "total_bytes", "files",
        "payload_sha256",
    }, "Tectonic cache manifest field set")
    require(policy.get("schema") == "k3p-release-fileset-policy-v2" and
            policy.get("tectonic_version") == "Tectonic 0.16.9" and
            re.fullmatch(r"[0-9a-f]{64}", str(
                policy.get("tectonic_sha256")
            )) is not None and
            isinstance(policy.get("pdf_source_date_epoch"), int) and
            policy["pdf_source_date_epoch"] > 0,
            "proof PDF toolchain policy")
    require(policy.get("tectonic_cache_manifest_sha256") == cache_sha256 and
            policy.get("tectonic_bundle_url") ==
            "https://relay.fullyjustified.net/default_bundle_v33.tar" and
            policy.get("tectonic_bundle_url") ==
            cache_contract.get("bundle_url") and
            policy.get("tectonic_bundle_digest") ==
            cache_contract.get("bundle_digest") and
            re.fullmatch(r"[0-9a-f]{64}", str(
                cache_contract.get("bundle_digest")
            )) is not None,
            "proof/source-reproduction Tectonic policy disagreement")
    claimed = cache_contract.get("payload_sha256")
    body = dict(cache_contract)
    body.pop("payload_sha256", None)
    require(claimed == sha256_bytes(canonical_json_bytes(body)),
            "Tectonic cache manifest payload hash")
    require(cache_contract.get("schema") ==
            "k3p-tectonic-cache-manifest-v1" and
            cache_contract.get("cache_layout") ==
            "contents of the Tectonic per-user cache root",
            "Tectonic cache manifest schema/layout")
    pointer_name = cache_contract["bundle_url"].replace(
        ":", ",58,"
    ).replace("/", ",47,")
    expected_pointer = f"bundles/hashes/{pointer_name}"
    require(cache_contract.get("bundle_hash_pointer") == expected_pointer,
            "Tectonic cache manifest bundle-pointer path")
    rows = cache_contract.get("files")
    require(isinstance(rows, list) and rows,
            "Tectonic cache manifest file inventory")
    paths = []
    total = 0
    for row in rows:
        require(isinstance(row, dict) and
                set(row) == {"path", "bytes", "sha256"},
                "Tectonic cache manifest row fields")
        relative = safe_relative(row.get("path"))
        require(isinstance(row.get("bytes"), int) and
                not isinstance(row["bytes"], bool) and row["bytes"] >= 0 and
                re.fullmatch(r"[0-9a-f]{64}", str(
                    row.get("sha256")
                )) is not None,
                ("Tectonic cache manifest row values", relative))
        paths.append(relative)
        total += row["bytes"]
    require(paths == sorted(set(paths)) and
            cache_contract.get("file_count") == len(rows) and
            cache_contract.get("total_bytes") == total,
            "Tectonic cache manifest inventory census")
    pointer_bytes = (cache_contract["bundle_digest"] + "\n").encode("ascii")
    require([row for row in rows if row["path"] == expected_pointer] == [{
        "path": expected_pointer,
        "bytes": len(pointer_bytes),
        "sha256": sha256_bytes(pointer_bytes),
    }], "Tectonic cache manifest pointer content")


def expected_source_members(proof: Path, kind: str) -> dict[str, bytes]:
    if kind == "article":
        sources = [
            proof / "manuscript/main.tex",
            proof / "manuscript/references.bib",
            *sorted((proof / "manuscript/sections").glob("*.tex")),
            *sorted((proof / "manuscript/figures").glob("*.tex")),
        ]
        require(len(sources) >= 3, "article source member set")
        return {
            path.relative_to(proof / "manuscript").as_posix(): path.read_bytes()
            for path in sources
        }
    source = proof / "supplement/reader_supplement.tex"
    require(source.is_file() and not source.is_symlink(),
            "supplement source member")
    return {source.name: source.read_bytes()}


def validate_source_build(build: dict, *, kind: str, commit: str,
                          policy: dict, cache_sha256: str) -> None:
    main = "main.tex" if kind == "article" else "reader_supplement.tex"
    output = "main.pdf" if kind == "article" else "reader_supplement.pdf"
    require(set(build) == {
        "schema", "kind", "source_commit", "source_date_epoch", "main",
        "command", "toolchain", "resource_contract", "environment",
        "execution_policy", "expected_output",
    }, ("source-build field set", kind))
    require(build.get("schema") == "k3p-tectonic-source-build-v2" and
            build.get("kind") == kind and
            build.get("source_commit") == commit and
            build.get("source_date_epoch") ==
            policy["pdf_source_date_epoch"] and
            build.get("main") == main and
            build.get("expected_output") == output and
            build.get("command") == [
                "tectonic", "--bundle", policy["tectonic_bundle_url"],
                "--only-cached", main, "--outdir", ".",
            ], ("source-build identity/command", kind))
    require(build.get("toolchain") == {
        "name": "tectonic",
        "version": policy["tectonic_version"],
        "executable_sha256": policy["tectonic_sha256"],
    } and build.get("resource_contract") == {
        "bundle_url": policy["tectonic_bundle_url"],
        "bundle_digest": policy["tectonic_bundle_digest"],
        "cache_manifest": "TECTONIC_CACHE_MANIFEST.json",
        "cache_manifest_sha256": cache_sha256,
        "cache_payload_vendored": False,
    }, ("source-build tool/resource contract", kind))
    require(build.get("environment") == {
        "SOURCE_DATE_EPOCH": str(policy["pdf_source_date_epoch"]),
        "TZ": "UTC", "LC_ALL": "C", "LANG": "C",
        "PYTHONDONTWRITEBYTECODE": "1",
    } and build.get("execution_policy") == {
        "parent_environment_inherited": False,
        "only_cached": True,
        "private_home": True,
        "private_tmp": True,
        "cache_verified_before_and_after": True,
        "fixed_path": "/usr/bin:/bin",
        "private_directory_variables": [
            "HOME", "TEXMFCONFIG", "TEXMFVAR", "TMPDIR",
            "XDG_CACHE_HOME", "XDG_CONFIG_HOME",
        ],
        "runtime_environment_keys": [
            "HOME", "LANG", "LC_ALL", "PATH", "PYTHONDONTWRITEBYTECODE",
            "SOURCE_DATE_EPOCH", "TEXMFCONFIG", "TEXMFVAR", "TMPDIR", "TZ",
            "XDG_CACHE_HOME", "XDG_CONFIG_HOME",
        ],
    }, ("source-build minimal environment", kind))


def verify_source_zip(source_archive: Path, *, proof: Path, kind: str,
                      commit: str, policy: dict, cache_bytes: bytes,
                      source_record: dict) -> dict[str, object]:
    archive_root = ("k3p_level2_article_source" if kind == "article" else
                    "k3p_level2_supplement_source")
    with zipfile.ZipFile(source_archive, mode="r") as archive:
        require(archive.testzip() is None, ("source archive CRC", kind))
        observed: dict[str, bytes] = {}
        names = []
        dates = []
        for info in archive.infolist():
            require(not info.is_dir(), ("source archive directory member", kind,
                                        info.filename))
            safe_relative(info.filename)
            parts = PurePosixPath(info.filename).parts
            require(len(parts) >= 2 and parts[0] == archive_root,
                    ("source archive root", kind, info.filename))
            relative = PurePosixPath(*parts[1:]).as_posix()
            require(relative not in observed,
                    ("duplicate source archive member", kind, relative))
            mode = (info.external_attr >> 16) & 0o7777
            require(mode == 0o644,
                    ("noncanonical source archive mode", kind, relative, mode))
            observed[relative] = archive.read(info)
            names.append(info.filename)
            dates.append(info.date_time)
    require(names == sorted(names) and len(names) == len(set(names)),
            ("source archive member ordering", kind))
    manifest_name = "ARCHIVE_MANIFEST.json"
    require(manifest_name in observed, ("source archive manifest", kind))
    manifest = json.loads(observed[manifest_name].decode("utf-8"))
    require(set(manifest) == {
        "schema", "kind", "archive_root", "source_commit",
        "source_date_epoch", "canonical_toolchain", "metadata",
        "members", "member_count_excluding_manifest",
        "outer_archive_hash_included", "self_referential_hash_forbidden",
        "payload_sha256",
    }, ("source archive manifest field set", kind))
    claimed = manifest.get("payload_sha256")
    body = dict(manifest)
    body.pop("payload_sha256", None)
    require(claimed == sha256_bytes(canonical_json_bytes(body)) and
            manifest.get("schema") == "k3p-canonical-archive-manifest-v1" and
            manifest.get("kind") == f"{kind}_latex_source" and
            manifest.get("archive_root") == archive_root and
            manifest.get("source_commit") == commit and
            isinstance(manifest.get("source_date_epoch"), int) and
            manifest["source_date_epoch"] > 0 and
            manifest.get("metadata") == {
                "source_build": "SOURCE_BUILD.json",
                "tectonic_cache_manifest": "TECTONIC_CACHE_MANIFEST.json",
            } and manifest.get("outer_archive_hash_included") is False and
            manifest.get("self_referential_hash_forbidden") is True,
            ("source archive manifest identity", kind))
    require(all(value == zip_datetime(manifest["source_date_epoch"])
                for value in dates),
            ("source archive member timestamp", kind))
    rows = manifest.get("members")
    require(isinstance(rows, list) and
            manifest.get("member_count_excluding_manifest") == len(rows),
            ("source archive manifest census", kind))
    row_paths = set()
    for row in rows:
        require(isinstance(row, dict) and
                set(row) == {"path", "bytes", "mode", "sha256"},
                ("source archive manifest row", kind))
        relative = safe_relative(row.get("path"))
        require(relative not in row_paths and relative in observed and
                row.get("mode") == "0644" and
                row.get("bytes") == len(observed[relative]) and
                row.get("sha256") == sha256_bytes(observed[relative]),
                ("source archive member binding", kind, relative))
        row_paths.add(relative)
    require(row_paths == set(observed) - {manifest_name},
            ("source archive exact member set", kind))
    require(observed.get("TECTONIC_CACHE_MANIFEST.json") == cache_bytes,
            ("source archive embedded cache manifest", kind))
    build = json.loads(observed["SOURCE_BUILD.json"].decode("utf-8"))
    validate_source_build(
        build, kind=kind, commit=commit, policy=policy,
        cache_sha256=sha256_bytes(cache_bytes),
    )
    expected = expected_source_members(proof, kind)
    source_members = {
        relative: data for relative, data in observed.items()
        if relative not in {
            manifest_name, "SOURCE_BUILD.json", "TECTONIC_CACHE_MANIFEST.json"
        }
    }
    require(set(source_members) == set(expected) and all(
        source_members[relative] == expected[relative] for relative in expected
    ), ("source archive differs from proof-package TeX", kind))
    binding = {
        "kind": kind,
        "member_count": len(expected),
        "payload_sha256": sha256_bytes(canonical_json_bytes({
            relative: sha256_bytes(expected[relative])
            for relative in sorted(expected)
        })),
    }
    structural = {
        "status": "PASS",
        "kind": manifest["kind"],
        "archive_root": archive_root,
        "source_commit": commit,
        "source_date_epoch": manifest["source_date_epoch"],
        "member_count": len(observed),
        "sha256": sha256_file(source_archive),
        "manifest_payload_sha256": claimed,
        "metadata": manifest["metadata"],
    }
    require(source_record.get("structural_verification") == structural,
            ("source archive structural report", kind))
    return binding


def verify_source_reproduction_evidence(
        root: Path, proof_source_commit: str) -> dict[str, object]:
    proof = root / "proof_package"
    evidence_root = proof / "release/source_reproduction_evidence"
    require(evidence_root.is_dir() and not evidence_root.is_symlink(),
            "missing sealed source-reproduction evidence")
    expected_paths: set[str] = set()
    cache_manifest = proof / "release/TECTONIC_CACHE_MANIFEST.json"
    require(cache_manifest.is_file() and not cache_manifest.is_symlink(),
            "missing Tectonic cache manifest")
    cache_sha256 = sha256_file(cache_manifest)
    cache_contract = json.loads(cache_manifest.read_text(encoding="utf-8"))
    policy = json.loads((proof / "release/RELEASE_FILESET.json").read_text(
        encoding="utf-8"
    ))
    validate_cache_manifest(cache_contract, policy, cache_sha256)
    used_transcripts: set[str] = set()
    for kind, pdf_name in (
        ("article", "K3P_Level2_Identifiability_Article.pdf"),
        ("supplement", "K3P_Level2_Identifiability_Reader_Supplement.pdf"),
    ):
        report_relative = f"release/source_reproduction_evidence/{kind}.json"
        expected_paths.add(report_relative)
        report_path = proof / report_relative
        require(report_path.is_file() and not report_path.is_symlink(),
                ("missing source-reproduction report", kind))
        report = json.loads(report_path.read_text(encoding="utf-8"))
        require(set(report) == {
                    "schema", "status", "kind", "source_commit",
                    "source_archive", "expected_pdf",
                    "committed_source_binding", "builds",
                    "byte_identical_across_two_builds",
                    "byte_identical_to_delivered_pdf", "tool_versions",
                    "environment", "execution_policy", "resource_bundle",
                    "logical_payload_sha256",
                } and
                report.get("schema") == "k3p-pdf-source-reproduction-v2" and
                report.get("status") == "PASS_BYTE_FOR_BYTE" and
                report.get("kind") == kind and
                report.get("source_commit") == proof_source_commit and
                report.get("byte_identical_across_two_builds") is True and
                report.get("byte_identical_to_delivered_pdf") is True,
                ("source-reproduction report identity", kind))
        resource = report.get("resource_bundle", {})
        require(resource == {
                    "bundle_url": cache_contract["bundle_url"],
                    "bundle_digest": cache_contract["bundle_digest"],
                    "cache_manifest_path": "release/TECTONIC_CACHE_MANIFEST.json",
                    "cache_manifest_sha256": cache_sha256,
                    "cache_manifest_payload_sha256":
                    cache_contract["payload_sha256"],
                    "cache_file_count": cache_contract["file_count"],
                    "cache_total_bytes": cache_contract["total_bytes"],
                    "cache_verified_before_and_after": True,
                    "cache_payload_vendored": False,
                } and
                report.get("environment") == {
                    "SOURCE_DATE_EPOCH": str(policy["pdf_source_date_epoch"]),
                    "TZ": "UTC", "LC_ALL": "C", "LANG": "C",
                    "PYTHONDONTWRITEBYTECODE": "1",
                } and
                report.get("execution_policy") == {
                    "parent_environment_inherited": False,
                    "only_cached": True,
                    "private_home": True,
                    "private_tmp": True,
                    "cache_verified_before_and_after": True,
                    "fixed_path": "/usr/bin:/bin",
                    "private_directory_variables": [
                        "HOME", "TEXMFCONFIG", "TEXMFVAR", "TMPDIR",
                        "XDG_CACHE_HOME", "XDG_CONFIG_HOME",
                    ],
                    "runtime_environment_keys": [
                        "HOME", "LANG", "LC_ALL", "PATH",
                        "PYTHONDONTWRITEBYTECODE", "SOURCE_DATE_EPOCH",
                        "TEXMFCONFIG", "TEXMFVAR", "TMPDIR", "TZ",
                        "XDG_CACHE_HOME", "XDG_CONFIG_HOME",
                    ],
                },
                ("source-reproduction closed resource contract", kind))
        tool_versions = report.get("tool_versions")
        tectonic = (tool_versions.get("tectonic", {})
                    if isinstance(tool_versions, dict) else {})
        require(isinstance(tool_versions, dict) and
                set(tool_versions) == {"tectonic"} and
                set(tectonic) == {"path", "sha256", "version"} and
                isinstance(tectonic.get("path"), str) and
                PurePosixPath(tectonic["path"]).is_absolute() and
                tectonic.get("sha256") == policy["tectonic_sha256"] and
                tectonic.get("version") == policy["tectonic_version"],
                ("source-reproduction Tectonic identity", kind))
        source_record = report.get("source_archive", {})
        source_relative = source_record.get("path")
        expected_source_relative = f"release/dist/k3p_level2_{kind}_source.zip"
        require(isinstance(source_record, dict) and
                set(source_record) == {
                    "path", "sha256", "structural_verification"
                } and source_relative == expected_source_relative and
                safe_relative(source_relative) == source_relative,
                ("source-reproduction source-archive path", kind))
        source_archive = proof / source_relative
        embedded_source = proof / "source_archives" / Path(source_relative).name
        require(source_archive.is_file() and not source_archive.is_symlink() and
                embedded_source.is_file() and not embedded_source.is_symlink() and
                source_record.get("sha256") == sha256_file(source_archive) ==
                sha256_file(embedded_source),
                ("source-reproduction source-archive binding", kind))
        committed_binding = verify_source_zip(
            source_archive, proof=proof, kind=kind,
            commit=proof_source_commit, policy=policy,
            cache_bytes=cache_manifest.read_bytes(), source_record=source_record,
        )
        require(report.get("committed_source_binding") == committed_binding,
                ("source-reproduction committed-source binding", kind))
        pdf = root / "paper" / pdf_name
        proof_pdf = proof / "output/pdf" / pdf_name
        expected_pdf_relative = f"output/pdf/{pdf_name}"
        expected_pdf = report.get("expected_pdf")
        require(pdf.is_file() and proof_pdf.is_file() and
                isinstance(expected_pdf, dict) and
                expected_pdf == {
                    "path": expected_pdf_relative,
                    "sha256": sha256_file(pdf),
                    "bytes": pdf.stat().st_size,
                } and
                expected_pdf["sha256"] == sha256_file(pdf) ==
                sha256_file(proof_pdf) and
                expected_pdf["bytes"] == proof_pdf.stat().st_size,
                ("source-reproduction PDF binding", kind))
        builds = report.get("builds")
        require(isinstance(builds, list) and len(builds) == 2,
                ("source-reproduction build count", kind))
        for run_number, build in enumerate(builds, 1):
            relative = build.get("transcript")
            expected_transcript = (
                "release/source_reproduction_evidence/"
                f"{kind}_transcripts/run{run_number}.log"
            )
            require(isinstance(build, dict) and set(build) == {
                        "run", "sha256", "bytes", "elapsed_seconds",
                        "transcript", "transcript_sha256",
                    } and relative == expected_transcript and
                    safe_relative(relative) == relative and
                    relative not in used_transcripts and
                    build.get("run") == run_number and
                    build.get("sha256") == expected_pdf["sha256"] and
                    build.get("bytes") == expected_pdf["bytes"] and
                    isinstance(build.get("elapsed_seconds"), (int, float)) and
                    not isinstance(build.get("elapsed_seconds"), bool) and
                    build["elapsed_seconds"] >= 0,
                    ("source-reproduction build row", kind, run_number))
            expected_paths.add(relative)
            used_transcripts.add(relative)
            transcript = proof / relative
            require(transcript.is_file() and not transcript.is_symlink() and
                    build.get("transcript_sha256") == sha256_file(transcript),
                    ("source-reproduction transcript binding", kind, run_number))
        logical = dict(report)
        claimed = logical.pop("logical_payload_sha256", None)
        logical["builds"] = [
            {key: row[key] for key in ("run", "sha256", "bytes")}
            for row in builds
        ]
        logical.pop("tool_versions", None)
        observed = sha256_bytes(canonical_json_bytes(logical))
        require(claimed == observed,
                ("source-reproduction logical payload", kind))
    observed_paths = {
        path.relative_to(proof).as_posix()
        for path in evidence_root.rglob("*") if path.is_file()
    }
    require(len(used_transcripts) == 4 and len(expected_paths) == 6 and
            observed_paths == expected_paths,
            ("sealed source-reproduction evidence file set",
             sorted(expected_paths - observed_paths),
             sorted(observed_paths - expected_paths)))
    return {
        "source_reproduction_reports": 2,
        "source_reproduction_transcripts": 4,
        "source_reproduction_source_archives": 2,
        "source_reproduction_closed_resource_contract": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path,
                        default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    root = args.package_root.resolve()
    try:
        outer = verify_outer(root)
        inner = verify_inner(root, outer["proof_source_commit"])
        source_reproduction = verify_source_reproduction_evidence(
            root, outer["proof_source_commit"]
        )
        print(json.dumps({
            "status": "PASS",
            "seal_scope": {
                "delivered_payload_bytes_and_modes": True,
                "excluded_runtime_roots": [".venv", "review_runs"],
                "compressed_archive_container_checked": False,
                "inner_manifest_checks_declared_members": True,
            },
            **outer, **inner, **source_reproduction,
        }, sort_keys=True))
        print("K3P_REFEREE_PACKAGE_INTEGRITY_PASS")
        return 0
    except (IntegrityFailure, OSError, UnicodeError, json.JSONDecodeError,
            zipfile.BadZipFile, KeyError, TypeError, ValueError) as error:
        print(f"K3P_REFEREE_PACKAGE_INTEGRITY_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
