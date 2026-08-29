#!/usr/bin/env python3
"""Fail-closed verification of the final K3P release envelope and assets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile
import tempfile
import zipfile


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
REPRO = PROJECT / "reproducibility"
if str(REPRO) not in sys.path:
    sys.path.insert(0, str(REPRO))

from release_common import (  # noqa: E402
    ReleaseFailure,
    atomic_write,
    canonical_json_bytes,
    exact_head_tags,
    head_commit,
    head_commit_epoch,
    load_json,
    parse_sha256sums,
    read_head_blob,
    refuse_optimized_python,
    require,
    resolve_inside,
    safe_relative_path,
    scoped_status,
    sha256_bytes,
    sha256_file,
    tracked_head_entries,
    tracked_worktree_fingerprint,
)
from archive_tools import (  # noqa: E402
    safe_extract_tar_gz,
    safe_extract_zip,
    verify_tar_gz,
    verify_zip,
)
from build_release import (  # noqa: E402
    SUBMISSION_KINDS,
    compact_selection,
    expected_submission_members,
    expected_submission_uploads,
    full_selection,
    generated_compact_readme,
    generated_readme,
    load_release_policy,
    submission_readiness_binding,
    verify_submission_package,
)
from verify_source_reproduction import verify_source_archive_contract  # noqa: E402
from run_release_suite import verify_suite_report  # noqa: E402


def flatten_asset_records(value, output: list[dict]) -> None:
    if isinstance(value, dict) and set(("path", "sha256", "bytes")).issubset(value):
        output.append(value)
        return
    if isinstance(value, dict):
        for child in value.values():
            flatten_asset_records(child, output)
    elif isinstance(value, list):
        for child in value:
            flatten_asset_records(child, output)


def verify_record(project: Path, record: dict) -> Path:
    require(isinstance(record, dict) and set(record) == {"path", "sha256", "bytes"},
            "release asset record schema")
    relative = record.get("path")
    safe_relative_path(relative)
    path = resolve_inside(project, relative)
    require(path.is_file(), ("missing release-bound asset", relative))
    require(path.stat().st_size == record.get("bytes"), ("release asset byte count", relative))
    require(sha256_file(path) == record.get("sha256"), ("STALE_RELEASE_ASSET_HASH", relative))
    return path


def verify_archive_sidecar(archive_path: Path, sidecar_path: Path, *, label: str) -> None:
    expected = f"{sha256_file(archive_path)}  {archive_path.name}\n"
    require(sidecar_path.read_text(encoding="utf-8") == expected,
            ("archive sidecar content", label))


def verify_generated_bytes(observed: bytes, expected: bytes, *, label: str) -> None:
    require(observed == expected, ("generated README binding", label))


def validate_envelope_field_set(envelope: dict) -> None:
    require(set(envelope) == {
        "schema", "status", "source_commit", "tag", "assets",
        "submission_package_contracts", "release_asset_checksums",
        "self_reference_policy", "doi", "license", "github_release",
        "zenodo_record", "external_submission_performed", "human_only_remaining",
        "tag_scope", "payload_sha256",
    }, "release envelope field set")


def require_final_clean_state(project: Path) -> tuple[list[str], str]:
    status = scoped_status(project)
    require(status == [], ("final verification requires a clean project", status))
    return status, tracked_worktree_fingerprint(project)


def validate_source_reproduction_evidence(
        report: dict, *, kind: str, commit: str, pdf_record: dict,
        policy: dict, transcript_records: dict[str, dict]) -> None:
    require(set(report) == {
        "schema", "status", "kind", "source_commit", "source_archive",
        "expected_pdf", "committed_source_binding", "builds",
        "byte_identical_across_two_builds", "byte_identical_to_delivered_pdf",
        "tool_versions", "environment", "execution_policy", "resource_bundle",
        "logical_payload_sha256",
    }, ("source-reproduction report field set", kind))
    require(report.get("schema") == "k3p-pdf-source-reproduction-v2" and
            report.get("status") == "PASS_BYTE_FOR_BYTE" and
            report.get("kind") == kind and report.get("source_commit") == commit and
            report.get("byte_identical_across_two_builds") is True and
            report.get("byte_identical_to_delivered_pdf") is True,
            ("source-reproduction report", kind))
    pdf_relative = {
        "article": "output/pdf/K3P_Level2_Identifiability_Article.pdf",
        "supplement":
            "output/pdf/K3P_Level2_Identifiability_Reader_Supplement.pdf",
    }[kind]
    require(report.get("expected_pdf") == {
                "path": pdf_relative,
                "sha256": pdf_record["sha256"],
                "bytes": pdf_record["bytes"],
            }, ("source-reproduction expected PDF", kind))
    require(report.get("environment") == {
        "SOURCE_DATE_EPOCH": str(policy["pdf_source_date_epoch"]),
        "TZ": "UTC", "LC_ALL": "C", "LANG": "C",
        "PYTHONDONTWRITEBYTECODE": "1",
    }, ("source-reproduction environment", kind))
    require(report.get("execution_policy") == {
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
    }, ("source-reproduction execution policy", kind))
    resource = report.get("resource_bundle")
    cache_manifest_path = HERE / "TECTONIC_CACHE_MANIFEST.json"
    require(sha256_file(cache_manifest_path) ==
            policy["tectonic_cache_manifest_sha256"],
            "source-reproduction cache-manifest policy binding")
    cache_manifest = load_json(cache_manifest_path)
    require(isinstance(resource, dict) and resource == {
        "bundle_url": policy["tectonic_bundle_url"],
        "bundle_digest": policy["tectonic_bundle_digest"],
        "cache_manifest_path": "release/TECTONIC_CACHE_MANIFEST.json",
        "cache_manifest_sha256": policy["tectonic_cache_manifest_sha256"],
        "cache_manifest_payload_sha256": cache_manifest["payload_sha256"],
        "cache_file_count": cache_manifest["file_count"],
        "cache_total_bytes": cache_manifest["total_bytes"],
        "cache_verified_before_and_after": True,
        "cache_payload_vendored": False,
    }, ("source-reproduction resource bundle", kind))
    tool_versions = report.get("tool_versions")
    require(isinstance(tool_versions, dict) and set(tool_versions) == {"tectonic"} and
            isinstance(tool_versions["tectonic"], dict) and
            set(tool_versions["tectonic"]) == {"path", "sha256", "version"} and
            isinstance(tool_versions["tectonic"]["path"], str) and
            Path(tool_versions["tectonic"]["path"]).is_absolute() and
            tool_versions["tectonic"]["sha256"] == policy["tectonic_sha256"] and
            tool_versions["tectonic"]["version"] == policy["tectonic_version"],
            ("source-reproduction toolchain", kind))
    builds = report.get("builds")
    require(isinstance(builds, list) and len(builds) == 2,
            ("source-reproduction build count", kind))
    for expected_run, build in enumerate(builds, 1):
        require(isinstance(build, dict) and set(build) == {
            "run", "sha256", "bytes", "elapsed_seconds", "transcript",
            "transcript_sha256",
        }, ("source-reproduction build row", kind, expected_run))
        transcript_relative = build.get("transcript")
        expected_transcript = (
            "release/source_reproduction_evidence/"
            f"{kind}_transcripts/run{expected_run}.log"
        )
        require(build.get("run") == expected_run and
                build.get("sha256") == pdf_record["sha256"] and
                build.get("bytes") == pdf_record["bytes"] and
                isinstance(build.get("elapsed_seconds"), (int, float)) and
                build["elapsed_seconds"] >= 0 and
                transcript_relative == expected_transcript and
                transcript_relative in transcript_records and
                build.get("transcript_sha256") ==
                transcript_records[transcript_relative]["sha256"],
                ("source-reproduction build/transcript binding", kind, expected_run))
    logical = dict(report)
    claimed_logical = logical.pop("logical_payload_sha256", None)
    logical["builds"] = [
        {key: row[key] for key in ("run", "sha256", "bytes")}
        for row in builds
    ]
    logical.pop("tool_versions", None)
    require(claimed_logical == sha256_bytes(canonical_json_bytes(logical)),
            ("source-reproduction logical payload", kind))


def verify_envelope(project: Path, envelope_path: Path) -> dict:
    initial_status, initial_fingerprint = require_final_clean_state(project)
    for relative in (
        "release/verify_release.py", "release/build_release.py", "release/archive_tools.py",
        "release/verify_source_reproduction.py", "release/RELEASE_FILESET.json",
        "release/build_tectonic_cache_manifest.py",
        "release/TECTONIC_CACHE_MANIFEST.json",
        "reproducibility/run_release_suite.py", "reproducibility/release_common.py",
        "submission/validate_submission_packages.py",
    ):
        require(resolve_inside(project, relative).read_bytes() == read_head_blob(project, relative),
                ("live final-verification code differs from HEAD", relative))
    envelope = load_json(envelope_path)
    validate_envelope_field_set(envelope)
    require(envelope.get("schema") == "k3p-final-release-envelope-v1" and
            envelope.get("status") == "ASSETS_BOUND_EXTERNAL_HUMAN_ACTIONS_PENDING",
            "release envelope schema/status")
    claimed = envelope.get("payload_sha256")
    body = dict(envelope)
    body.pop("payload_sha256", None)
    require(claimed == sha256_bytes(canonical_json_bytes(body)), "release envelope payload hash")
    commit = head_commit(project)
    require(envelope.get("source_commit") == commit, "release envelope source commit")
    require(envelope.get("tag") in exact_head_tags(project), "release envelope exact tag")
    require(envelope.get("doi") == {"status": "NOT_MINTED", "value": None},
            "invented or prematurely bound DOI")
    require(envelope.get("license") ==
            {"status": "NOT_AUTHORIZED_OR_SELECTED", "value": None},
            "unauthorized license declaration")
    require(envelope.get("github_release") == {"created": False} and
            envelope.get("zenodo_record") == {"created": False} and
            envelope.get("external_submission_performed") is False,
            "premature external-release claim")
    require(envelope.get("tag_scope") ==
            "LOCAL_EXACT_HEAD_TAG_EXTERNAL_PUSH_NOT_VERIFIED",
            "release tag scope")
    require(envelope.get("human_only_remaining") == [
        "authorize explicit licenses",
        "create immutable GitHub release after final human audit",
        "mint Zenodo DOI",
        "rebuild DOI-bearing PDFs and submission packages",
        "perform journal portal submissions",
    ], "release envelope human-only boundary")
    self_policy = envelope.get("self_reference_policy", {})
    require(set(self_policy) == {
        "full_archive_contains_its_own_hash", "full_archive_contains_release_envelope",
        "checksum_list_contains_itself", "envelope_hash_is_not_embedded_in_envelope",
    } and set(self_policy.values()) == {False, True} and
            self_policy.get("full_archive_contains_its_own_hash") is False and
            self_policy.get("full_archive_contains_release_envelope") is False and
            self_policy.get("checksum_list_contains_itself") is False and
            self_policy.get("envelope_hash_is_not_embedded_in_envelope") is True,
            "release self-reference policy")

    records: list[dict] = []
    flatten_asset_records(envelope.get("assets"), records)
    require(len(records) == len({row.get("path") for row in records}),
            "duplicate envelope asset")
    paths = {row["path"]: verify_record(project, row) for row in records}
    checksum_record = envelope.get("release_asset_checksums", {})
    checksum_path = verify_record(project, checksum_record)
    checksum_relative = checksum_record["path"]
    checksums = parse_sha256sums(
        checksum_path.read_text(encoding="utf-8"), checksum_path=checksum_relative
    )
    expected = {row["path"]: row["sha256"] for row in records}
    require(checksums == expected, "release checksum list/envelope disagreement")
    require(envelope_path.relative_to(project).as_posix() not in checksums,
            "release envelope cannot checksum itself")

    assets = envelope["assets"]
    require(set(assets) == {
        "article_pdf", "supplement_pdf", "full_reproducibility_archive",
        "full_reproducibility_archive_sidecar", "compact_verifier_archive",
        "compact_verifier_archive_sidecar", "latex_source_archives",
        "clean_clone_transcripts", "source_reproduction_reports",
        "source_reproduction_transcripts", "submission_readiness_report",
        "submission_packages",
    }, "release envelope asset field set")
    readiness_record = assets.get("submission_readiness_report", {})
    readiness_path = paths.get(readiness_record.get("path"))
    require(readiness_path is not None, "submission readiness report asset")
    stored_readiness = load_json(readiness_path)
    fresh_readiness = submission_readiness_binding(project)
    require(stored_readiness == fresh_readiness,
            "stale or forged submission readiness report")
    submission_records = assets.get("submission_packages", {})
    require(set(submission_records) == SUBMISSION_KINDS,
            ("submission package kinds", sorted(submission_records)))
    observed_submission_contracts = {}
    for kind, record in submission_records.items():
        uploads = expected_submission_uploads(project, kind)
        observed_submission_contracts[kind] = verify_submission_package(
            paths[record["path"]], kind=kind, commit=commit,
            expected_uploads=uploads,
            expected_members=expected_submission_members(project, kind, uploads),
        )
    require(envelope.get("submission_package_contracts") ==
            observed_submission_contracts,
            "submission package contract binding")
    full_path = paths[assets["full_reproducibility_archive"]["path"]]
    compact_path = paths[assets["compact_verifier_archive"]["path"]]
    full_sidecar_path = paths[assets["full_reproducibility_archive_sidecar"]["path"]]
    compact_sidecar_path = paths[assets["compact_verifier_archive_sidecar"]["path"]]
    verify_archive_sidecar(full_path, full_sidecar_path, label="full")
    verify_archive_sidecar(compact_path, compact_sidecar_path, label="compact")
    full = verify_tar_gz(full_path)
    compact = verify_zip(compact_path)
    policy = load_release_policy(project)
    epoch = head_commit_epoch(project)
    require(full["kind"] == "full_reproducibility" and
            compact["kind"] == "compact_verifier" and
            full["archive_root"] == policy["archive_root"] and
            compact["archive_root"] == policy["compact_root"] and
            full["source_commit"] == compact["source_commit"] == commit and
            full["source_date_epoch"] == compact["source_date_epoch"] == epoch,
            "release archive kind/root/commit/epoch binding")
    require(full.get("metadata") == {
        "fileset_policy_sha256": sha256_bytes(read_head_blob(
            project, "release/RELEASE_FILESET.json"
        )),
        "source_archives_generated_from_committed_tex": True,
        "release_pdfs_included": True,
        "untracked_files_included": False,
    }, "full release archive metadata")
    require(compact.get("metadata") == {
        "entrypoint": "reproducibility/verify_k3p_same_classification.py",
        "entrypoint_mode": "--artifact-only --no-write-report",
        "full_archive_is_external_canonical": True,
    }, "compact release archive metadata")
    forbidden_basenames = {
        full_path.name, full_path.name + ".sha256", "RELEASE_ENVELOPE.json",
        "RELEASE_ASSET_SHA256SUMS",
    }
    expected_full = set(full_selection(project, policy, require_pdfs=True))
    expected_compact = set(compact_selection(project, policy))
    with tarfile.open(full_path, mode="r:gz") as archive:
        infos = archive.getmembers()
        names = [PurePosixPath(info.name).name for info in infos]
        require(not (forbidden_basenames & set(names)),
                ("SELF_REFERENTIAL_FULL_ARCHIVE_MEMBER", forbidden_basenames & set(names)))
        relative_infos = {
            PurePosixPath(*PurePosixPath(info.name).parts[1:]).as_posix(): info
            for info in infos
        }
        generated_full = {
            "ARCHIVE_MANIFEST.json", "REPRODUCIBILITY_README.txt",
            "source_archives/k3p_level2_article_source.zip",
            "source_archives/k3p_level2_supplement_source.zip",
        }
        require(set(relative_infos) == expected_full | generated_full,
                "full archive committed-fileset mismatch")
        for relative in expected_full:
            handle = archive.extractfile(relative_infos[relative])
            require(handle is not None and handle.read() == read_head_blob(project, relative),
                    ("full archive member differs from HEAD", relative))
        readme_handle = archive.extractfile(relative_infos["REPRODUCIBILITY_README.txt"])
        require(readme_handle is not None, "full archive generated README unreadable")
        verify_generated_bytes(readme_handle.read(), generated_readme(commit), label="full")
        embedded = {}
        for label, record in assets.get("latex_source_archives", {}).items():
            wanted = f"{full['archive_root']}/source_archives/{Path(record['path']).name}"
            info = archive.getmember(wanted)
            handle = archive.extractfile(info)
            require(handle is not None, ("embedded source archive unreadable", label))
            embedded[label] = sha256_bytes(handle.read())
            require(embedded[label] == record["sha256"],
                    ("embedded/external source archive mismatch", label))
    with zipfile.ZipFile(compact_path, mode="r") as archive:
        relative_infos = {
            PurePosixPath(*PurePosixPath(info.filename).parts[1:]).as_posix(): info
            for info in archive.infolist()
        }
        require(set(relative_infos) == expected_compact | {
            "ARCHIVE_MANIFEST.json", "README_VERIFY.txt"
        }, "compact archive committed-fileset mismatch")
        for relative in expected_compact:
            require(archive.read(relative_infos[relative]) == read_head_blob(project, relative),
                    ("compact archive member differs from HEAD", relative))
        verify_generated_bytes(
            archive.read(relative_infos["README_VERIFY.txt"]),
            generated_compact_readme(), label="compact",
        )
    require(set(assets.get("latex_source_archives", {})) == {"article", "supplement"},
            "article/supplement source archive coverage")
    committed_source_bindings = {}
    committed_source_reports = {}
    for kind, record in assets.get("latex_source_archives", {}).items():
        source = paths[record["path"]]
        source_report, _build, binding = verify_source_archive_contract(
            source, kind=kind, project=project
        )
        committed_source_reports[kind] = source_report
        committed_source_bindings[kind] = binding
        require(source_report["source_commit"] == commit, "source archive commit")

    reproduction_kinds = set()
    stored_logical_payloads = {}
    source_transcript_records = {
        record["path"]: record
        for record in assets.get("source_reproduction_transcripts", [])
    }
    require(len(source_transcript_records) == 4,
            "source-reproduction transcript asset coverage")
    used_source_transcripts: set[str] = set()
    for record in assets.get("source_reproduction_reports", []):
        report = load_json(paths[record["path"]])
        tentative_kind = report.get("kind")
        tentative_pdf_key = ("article_pdf" if tentative_kind == "article" else
                             "supplement_pdf")
        validate_source_reproduction_evidence(
            report, kind=tentative_kind, commit=commit,
            pdf_record=assets[tentative_pdf_key], policy=policy,
            transcript_records=source_transcript_records,
        )
        require(set(report) == {
            "schema", "status", "kind", "source_commit", "source_archive",
            "expected_pdf", "committed_source_binding", "builds",
            "byte_identical_across_two_builds", "byte_identical_to_delivered_pdf",
            "tool_versions", "environment", "execution_policy", "resource_bundle",
            "logical_payload_sha256",
        }, ("source-reproduction report field set", record["path"]))
        require(report.get("schema") == "k3p-pdf-source-reproduction-v2" and
                report.get("status") == "PASS_BYTE_FOR_BYTE" and
                report.get("byte_identical_across_two_builds") is True and
                report.get("byte_identical_to_delivered_pdf") is True and
                report.get("source_commit") == commit,
                ("source-reproduction report", record["path"]))
        kind = report.get("kind")
        require(kind in {"article", "supplement"} and kind not in reproduction_kinds,
                ("source-reproduction kind", kind))
        reproduction_kinds.add(kind)
        pdf_key = "article_pdf" if kind == "article" else "supplement_pdf"
        pdf_record = assets[pdf_key]
        source_record = assets["latex_source_archives"][kind]
        require(report.get("source_archive") == {
            "path": source_record["path"],
            "sha256": source_record["sha256"],
            "structural_verification": committed_source_reports[kind],
        }, ("source-reproduction source archive binding", kind))
        require(report.get("expected_pdf") == pdf_record,
                ("source-reproduction PDF binding", kind))
        require(report.get("committed_source_binding") == committed_source_bindings[kind],
                ("source-reproduction committed source binding", kind))
        tool_versions = report.get("tool_versions")
        require(isinstance(tool_versions, dict) and set(tool_versions) == {"tectonic"} and
                isinstance(tool_versions["tectonic"], dict) and
                set(tool_versions["tectonic"]) == {"path", "sha256", "version"} and
                tool_versions["tectonic"]["sha256"] == policy["tectonic_sha256"] and
                tool_versions["tectonic"]["version"] == policy["tectonic_version"],
                ("source-reproduction toolchain", kind))
        builds = report.get("builds")
        require(isinstance(builds, list) and len(builds) == 2,
                ("source-reproduction build count", kind))
        for expected_run, build in enumerate(builds, 1):
            require(isinstance(build, dict) and set(build) == {
                "run", "sha256", "bytes", "elapsed_seconds", "transcript",
                "transcript_sha256",
            }, ("source-reproduction build row", kind, expected_run))
            transcript_relative = build.get("transcript")
            require(build.get("run") == expected_run and
                    build.get("sha256") == pdf_record["sha256"] and
                    build.get("bytes") == pdf_record["bytes"] and
                    isinstance(build.get("elapsed_seconds"), (int, float)) and
                    build["elapsed_seconds"] >= 0 and
                    transcript_relative in source_transcript_records and
                    transcript_relative not in used_source_transcripts and
                    build.get("transcript_sha256") ==
                    source_transcript_records[transcript_relative]["sha256"],
                    ("source-reproduction build/transcript binding", kind, expected_run))
            used_source_transcripts.add(transcript_relative)
        logical = dict(report)
        claimed_logical = logical.pop("logical_payload_sha256", None)
        logical["builds"] = [
            {key: row[key] for key in ("run", "sha256", "bytes")}
            for row in report.get("builds", [])
        ]
        logical.pop("tool_versions", None)
        require(claimed_logical == sha256_bytes(canonical_json_bytes(logical)),
                ("source-reproduction logical payload", kind))
        stored_logical_payloads[kind] = claimed_logical
    require(reproduction_kinds == {"article", "supplement"},
            "article/supplement source-reproduction coverage")
    require(used_source_transcripts == set(source_transcript_records),
            "unused or missing source-reproduction transcript asset")

    fresh_source_payloads = {}
    fresh_source_root = project / "release/work/final_source_replay"
    fresh_source_root.mkdir(parents=True, exist_ok=True)
    for kind in ("article", "supplement"):
        pdf_key = "article_pdf" if kind == "article" else "supplement_pdf"
        report_path = fresh_source_root / f"{kind}.json"
        command = [
            sys.executable, "release/verify_source_reproduction.py", "--kind", kind,
            "--source-archive", str(paths[assets["latex_source_archives"][kind]["path"]]),
            "--expected-pdf", str(paths[assets[pdf_key]["path"]]),
            "--report", str(report_path),
        ]
        result = subprocess.run(
            command, cwd=project, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, check=False, timeout=3_600,
        )
        require(result.returncode == 0 and "K3P_SOURCE_REPRODUCTION_PASS" in result.stdout,
                ("fresh source reproduction", kind, result.stdout[-6000:]))
        fresh = load_json(report_path)
        require(fresh.get("logical_payload_sha256") == stored_logical_payloads[kind],
                ("fresh/stored source-reproduction payload", kind))
        fresh_source_payloads[kind] = fresh["logical_payload_sha256"]
    head_entries = tracked_head_entries(project)
    for key in ("article_pdf", "supplement_pdf"):
        record = assets[key]
        require(record["path"] in head_entries and
                paths[record["path"]].read_bytes() == read_head_blob(project, record["path"]),
                ("release PDF not identical to committed HEAD blob", record["path"]))

    clean_records = assets.get("clean_clone_transcripts", [])
    require(isinstance(clean_records, list) and len(clean_records) == 6,
            "exact clean-suite report/transcript asset count")
    clean_paths = {record["path"] for record in clean_records}
    require(sum(Path(relative).suffix == ".json" for relative in clean_paths) == 3 and
            sum(Path(relative).suffix == ".log" for relative in clean_paths) == 3,
            "clean-suite report/transcript extension coverage")
    suite_modes = set()
    stored_suite_payloads = {}
    for record in clean_records:
        path = paths[record["path"]]
        if path.suffix != ".json":
            continue
        binding = verify_suite_report(project, path, clean_paths)
        require(binding["mode"] not in suite_modes,
                ("duplicate clean-suite mode", binding["mode"]))
        suite_modes.add(binding["mode"])
        stored_suite_payloads[binding["mode"]] = binding["payload_sha256"]
    require(suite_modes == {"quick", "full", "regenerate"},
            ("clean-clone suite coverage", suite_modes))

    fresh_suite_payloads = {}
    replay_parent = project / "release/work"
    replay_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="final-suite-replay-", dir=replay_parent) as directory:
        replay_root = Path(directory)
        for mode in ("quick", "full"):
            result = subprocess.run(
                [sys.executable, "reproducibility/run_release_suite.py", mode,
                 "--transcript-dir", str(replay_root)],
                cwd=project, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, check=False, timeout=18_000,
            )
            require(result.returncode == 0 and
                    f"K3P_RELEASE_SUITE_{mode.upper()}_PASS" in result.stdout,
                    ("fresh clean-suite replay", mode, result.stdout[-6000:]))
        fresh_paths = {
            path.relative_to(project).as_posix()
            for path in replay_root.iterdir() if path.is_file()
        }
        require(len(fresh_paths) == 4,
                ("fresh clean-suite artifact count", sorted(fresh_paths)))
        for report_path in sorted(replay_root.glob("*.json")):
            binding = verify_suite_report(project, report_path, fresh_paths)
            fresh_suite_payloads[binding["mode"]] = binding["payload_sha256"]
        require(set(fresh_suite_payloads) == {"quick", "full"},
                "fresh clean-suite quick/full coverage")

    with tempfile.TemporaryDirectory(prefix="k3p-release-final-replay-") as directory:
        temporary = Path(directory)
        safe_extract_zip(compact_path, temporary / "compact")
        compact_root = temporary / "compact" / compact["archive_root"]
        command = [sys.executable, "reproducibility/verify_k3p_same_classification.py",
                   "--artifact-only", "--no-write-report"]
        result = subprocess.run(command, cwd=compact_root,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, check=False, timeout=1_800)
        require(result.returncode == 0 and "K3P_SAME_CLASSIFICATION_GATE_PASS" in result.stdout,
                ("compact final replay", result.stdout[-4000:]))
        compact_replay_sha = sha256_bytes(result.stdout.encode())
        safe_extract_tar_gz(full_path, temporary / "full")
        full_root = temporary / "full" / full["archive_root"]
        result = subprocess.run(command, cwd=full_root,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, check=False, timeout=1_800)
        require(result.returncode == 0 and "K3P_SAME_CLASSIFICATION_GATE_PASS" in result.stdout,
                ("full archive final replay", result.stdout[-4000:]))
        full_replay_sha = sha256_bytes(result.stdout.encode())

    require(scoped_status(project) == initial_status == [] and
            tracked_worktree_fingerprint(project) == initial_fingerprint,
            "final verification changed or dirtied the project")

    return {
        "schema": "k3p-final-release-verification-v1",
        "status": "PASS",
        "source_commit": commit,
        "tag": envelope["tag"],
        "envelope_payload_sha256": claimed,
        "asset_count": len(records),
        "full_archive": full,
        "compact_archive": compact,
        "clean_clone_modes": sorted(suite_modes),
        "stored_suite_payloads": stored_suite_payloads,
        "fresh_suite_payloads": fresh_suite_payloads,
        "source_reproduction_kinds": sorted(reproduction_kinds),
        "fresh_source_reproduction_payloads": fresh_source_payloads,
        "extracted_replays": {
            "compact_transcript_sha256": compact_replay_sha,
            "full_transcript_sha256": full_replay_sha,
        },
        "doi_minted": False,
        "license_selected": False,
        "external_release_created": False,
    }


def main(argv: list[str] | None = None) -> int:
    try:
        refuse_optimized_python()
        parser = argparse.ArgumentParser()
        parser.add_argument("--envelope", type=Path, default=HERE / "RELEASE_ENVELOPE.json")
        parser.add_argument("--report", type=Path,
                            default=HERE / "work/FINAL_RELEASE_VERIFICATION.json")
        args = parser.parse_args(argv)
        report = verify_envelope(PROJECT, args.envelope.resolve())
        report["payload_sha256"] = sha256_bytes(canonical_json_bytes(report))
        atomic_write(args.report.resolve(),
                     (json.dumps(report, indent=2, sort_keys=True) + "\n").encode())
        print(json.dumps(report, indent=2, sort_keys=True))
        print("K3P_FINAL_RELEASE_VERIFICATION_PASS")
        return 0
    except (ReleaseFailure, OSError, UnicodeError, ValueError, KeyError,
            json.JSONDecodeError, subprocess.SubprocessError, tarfile.TarError,
            zipfile.BadZipFile) as error:
        print(f"K3P_FINAL_RELEASE_VERIFICATION_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
