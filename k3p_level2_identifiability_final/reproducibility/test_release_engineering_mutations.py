#!/usr/bin/env python3
"""Hostile mutation suite for deterministic K3P release engineering."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile
import time
import zipfile


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
RELEASE = PROJECT / "release"
TOOLS = PROJECT / "tools"
if str(RELEASE) not in sys.path:
    sys.path.insert(0, str(RELEASE))
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from release_common import (  # noqa: E402
    ReleaseFailure,
    atomic_write,
    canonical_json_bytes,
    head_commit,
    head_commit_epoch,
    load_head_json,
    parse_sha256sums,
    refuse_optimized_python,
    require,
    safe_relative_path,
    sha256_bytes,
    sha256_file,
    tracked_head_entries,
    tracked_worktree_fingerprint,
    verify_sha256sums,
)
from archive_tools import (  # noqa: E402
    canonical_mode,
    deterministic_tar_gz,
    deterministic_zip,
    manifest_for,
    safe_extract_tar_gz,
    safe_extract_zip,
    validate_manifest,
    verify_tar_gz,
    verify_zip,
)
from verify_release_inputs import active_paths  # noqa: E402
from run_release_suite import (  # noqa: E402
    Command,
    deterministic_environment,
    normalized_command_plan,
    quick_commands,
    regeneration_commands,
    run_one,
    suite_code_bindings,
    verify_suite_report,
)
from verify_source_reproduction import (  # noqa: E402
    DEFAULTS as SOURCE_DEFAULTS,
    committed_source_members,
    validate_source_build,
    verify_source_archive_contract,
    verify_tectonic_identity,
)
from build_release import (  # noqa: E402
    SUBMISSION_ROOTS,
    ARTICLE_PDF,
    SUPPLEMENT_PDF,
    compact_selection,
    full_selection,
    require_submission_readiness_report,
    submission_argument_map,
    validate_release_policy,
    verify_submission_package,
)
import verify_release as final_release_verifier  # noqa: E402
from build_input_inventory import preserve_or_write_bootstrap_manifest  # noqa: E402


DEFAULT_REPORT = HERE / "RELEASE_ENGINEERING_MUTATION_REPORT.json"


def canonical_diagnostic(value: str) -> str:
    """Remove TemporaryDirectory nonce components from stored diagnostics."""
    temporary_root = re.escape(tempfile.gettempdir().rstrip("/"))
    return re.sub(
        rf"{temporary_root}/k3p-[^/'\"\s]+",
        "<TEMP_DIR>",
        value,
    )


def rejected(name: str, expected: str, action) -> dict:
    try:
        action()
    except (ReleaseFailure, OSError, ValueError, json.JSONDecodeError,
            zipfile.BadZipFile) as error:
        diagnostic = str(error)
        require(expected in diagnostic,
                ("wrong mutation diagnostic", name, expected, diagnostic))
        return {"name": name, "status": "REJECTED",
                "expected_failure_class": expected,
                "diagnostic": canonical_diagnostic(diagnostic)[:500]}
    raise ReleaseFailure(("mutation survived", name))


def stale_checksum() -> None:
    with tempfile.TemporaryDirectory(prefix="k3p-release-stale-") as directory:
        root = Path(directory)
        (root / "a.txt").write_text("current\n")
        (root / "SUMS").write_text(f"{'0' * 64}  a.txt\n")
        verify_sha256sums(root, "SUMS")


def stale_manifest_hash() -> None:
    members = {"a.txt": b"content\n"}
    manifest = manifest_for("test", "root", "a" * 40, 1_700_000_000, members)
    manifest["members"][0]["sha256"] = "0" * 64
    manifest.pop("payload_sha256")
    manifest["payload_sha256"] = sha256_bytes(canonical_json_bytes(manifest))
    validate_manifest(manifest, archive_root="root",
                      observed={"a.txt": (members["a.txt"], 0o644)})


def self_referential_archive_hash() -> None:
    members = {"a.txt": b"content\n"}
    manifest = manifest_for("test", "root", "b" * 40, 1_700_000_000, members)
    manifest.pop("payload_sha256")
    manifest["archive_sha256"] = "1" * 64
    manifest["payload_sha256"] = sha256_bytes(canonical_json_bytes(manifest))
    validate_manifest(manifest, archive_root="root",
                      observed={"a.txt": (members["a.txt"], 0o644)})


def checksum_self_reference() -> None:
    parse_sha256sums(f"{'0' * 64}  RELEASE_ASSET_SHA256SUMS\n",
                     checksum_path="RELEASE_ASSET_SHA256SUMS")


def traversal_primitive() -> None:
    safe_relative_path("../escape")


def traversal_zip() -> None:
    with tempfile.TemporaryDirectory(prefix="k3p-release-traversal-") as directory:
        path = Path(directory) / "bad.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("../escape", b"bad")
        verify_zip(path)


def noncanonical_zip_timestamp() -> None:
    with tempfile.TemporaryDirectory(prefix="k3p-release-time-") as directory:
        root = Path(directory)
        canonical = root / "canonical.zip"
        bad = root / "bad.zip"
        deterministic_zip(canonical, kind="test", archive_root="root",
                          source_commit="c" * 40, source_date_epoch=1_700_000_000,
                          members={"a.txt": b"a\n"})
        with zipfile.ZipFile(canonical, "r") as source, zipfile.ZipFile(
                bad, "w", compression=zipfile.ZIP_DEFLATED) as target:
            for old in source.infolist():
                info = zipfile.ZipInfo(old.filename, date_time=(2025, 1, 2, 3, 4, 6))
                relative = "/".join(old.filename.split("/")[1:])
                info.create_system = 3
                info.external_attr = canonical_mode(relative) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                target.writestr(info, source.read(old))
        verify_zip(bad)


def noncanonical_tar_mode() -> None:
    members = {"a.txt": b"a\n"}
    manifest = manifest_for("test", "root", "c" * 40, 1_700_000_000, members)
    manifest["members"][0]["mode"] = "0600"
    manifest.pop("payload_sha256")
    manifest["payload_sha256"] = sha256_bytes(canonical_json_bytes(manifest))
    validate_manifest(manifest, archive_root="root",
                      observed={"a.txt": (members["a.txt"], 0o600)})


def optimized_input_gate() -> None:
    result = subprocess.run(
        [sys.executable, "-O", "reproducibility/verify_release_inputs.py", "--self-test"],
        cwd=PROJECT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, check=False, timeout=60,
    )
    require(result.returncode != 0 and "OPTIMIZED_PYTHON_FORBIDDEN" in result.stdout,
            ("optimized input gate survived", result.returncode, result.stdout))
    raise ReleaseFailure("OPTIMIZED_PYTHON_FORBIDDEN")


def optimized_archive_builder() -> None:
    result = subprocess.run(
        [sys.executable, "-O", "release/build_release.py", "plan", "--kind", "compact"],
        cwd=PROJECT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, check=False, timeout=60,
    )
    require(result.returncode != 0 and "OPTIMIZED_PYTHON_FORBIDDEN" in result.stdout,
            ("optimized archive builder survived", result.returncode, result.stdout))
    raise ReleaseFailure("OPTIMIZED_PYTHON_FORBIDDEN")


def forbidden_active_path() -> None:
    manifest = {
        "active_gate_reports": [{
            "path": "cut_recovery/upstream_frozen/pointwise_cut_certificate.json",
            "sha256": "0" * 64,
        }],
        "active_theorem_artifacts": [], "active_verifiers": [], "claim_locks": [],
    }
    active_paths(manifest, {"bindings": {}}, {"certification": {}})


def missing_active_path() -> None:
    manifest = {
        "active_gate_reports": [{"path": None, "sha256": "0" * 64}],
        "active_theorem_artifacts": [], "active_verifiers": [], "claim_locks": [],
    }
    active_paths(manifest, {"bindings": {}}, {"certification": {}})


def valid_source_build(commit: str = "a" * 40) -> tuple[dict, dict, int]:
    config = dict(SOURCE_DEFAULTS["article"])
    policy = json.loads((RELEASE / "RELEASE_FILESET.json").read_text(encoding="utf-8"))
    epoch = policy["pdf_source_date_epoch"]
    build = {
        "schema": "k3p-tectonic-source-build-v1",
        "kind": "article",
        "source_commit": commit,
        "source_date_epoch": epoch,
        "main": config["main"],
        "command": ["tectonic", config["main"], "--outdir", "."],
        "toolchain": {
            "name": "tectonic", "version": policy["tectonic_version"],
            "executable_sha256": policy["tectonic_sha256"],
        },
        "environment": {
            "SOURCE_DATE_EPOCH": str(epoch), "TZ": "UTC", "LC_ALL": "C",
        },
        "expected_output": config["output"],
    }
    return build, config, epoch


def wrong_source_build_engine() -> None:
    build, config, epoch = valid_source_build()
    build["command"] = ["latexmk", "-pdf", config["main"]]
    policy = json.loads((RELEASE / "RELEASE_FILESET.json").read_text())
    validate_source_build(
        build, kind="article", config=config, commit="a" * 40,
        pdf_source_date_epoch=epoch, tectonic_version=policy["tectonic_version"],
        tectonic_sha256=policy["tectonic_sha256"],
    )


def wrong_pdf_source_date_epoch() -> None:
    build, config, epoch = valid_source_build()
    build["source_date_epoch"] = epoch + 1
    build["environment"]["SOURCE_DATE_EPOCH"] = str(epoch + 1)
    policy = json.loads((RELEASE / "RELEASE_FILESET.json").read_text())
    validate_source_build(
        build, kind="article", config=config, commit="a" * 40,
        pdf_source_date_epoch=epoch, tectonic_version=policy["tectonic_version"],
        tectonic_sha256=policy["tectonic_sha256"],
    )


def inconsistent_source_build_environment() -> None:
    build, config, epoch = valid_source_build()
    build["environment"]["SOURCE_DATE_EPOCH"] = str(epoch + 1)
    policy = json.loads((RELEASE / "RELEASE_FILESET.json").read_text())
    validate_source_build(
        build, kind="article", config=config, commit="a" * 40,
        pdf_source_date_epoch=epoch, tectonic_version=policy["tectonic_version"],
        tectonic_sha256=policy["tectonic_sha256"],
    )


def fake_tectonic_executable() -> None:
    policy = json.loads((RELEASE / "RELEASE_FILESET.json").read_text())
    with tempfile.TemporaryDirectory(prefix="k3p-fake-tectonic-") as directory:
        executable = Path(directory) / "tectonic"
        executable.write_text("#!/bin/sh\necho 'Tectonic 0.16.9'\n", encoding="utf-8")
        executable.chmod(0o755)
        verify_tectonic_identity(str(executable), policy)


def pdf_equivalent_source_archive_tamper() -> None:
    with tempfile.TemporaryDirectory(prefix="k3p-release-source-tamper-") as directory:
        output = Path(directory) / "tampered.zip"
        commit = head_commit(PROJECT)
        policy = json.loads((RELEASE / "RELEASE_FILESET.json").read_text(
            encoding="utf-8"
        ))
        build, config, _epoch = valid_source_build(commit)
        members = committed_source_members(PROJECT, "article")
        members["main.tex"] = b"% PDF-equivalent source tamper\n" + members["main.tex"]
        members["SOURCE_BUILD.json"] = (
            json.dumps(build, indent=2, sort_keys=True) + "\n"
        ).encode()
        deterministic_zip(
            output, kind="article_latex_source", archive_root=config["root"],
            source_commit=commit, source_date_epoch=head_commit_epoch(PROJECT),
            members=members, extra={"source_build": "SOURCE_BUILD.json"},
        )
        verify_source_archive_contract(
            output, kind="article", project=PROJECT, policy=policy
        )


def malformed_fileset_policy() -> None:
    policy = json.loads((RELEASE / "RELEASE_FILESET.json").read_text(
        encoding="utf-8"
    ))
    policy["schema"] = "unrecognized-policy"
    validate_release_policy(policy)


def wrong_fileset_selection_lock() -> None:
    policy = load_head_json(PROJECT, "release/RELEASE_FILESET.json")
    policy["expected_full_selection_count"] += 1
    full_selection(PROJECT, validate_release_policy(policy), require_pdfs=True)


def not_ready_submission_report() -> None:
    report = {
        "schema_version": 1,
        "status": "NOT_READY",
        "structural_error_count": 0,
        "structural_errors": [],
        "release_blocker_count": 1,
        "release_blockers": ["human metadata pending"],
    }
    report["payload_sha256"] = sha256_bytes(canonical_json_bytes(report))
    require_submission_readiness_report(report, 2)


def arbitrary_submission_files() -> None:
    with tempfile.TemporaryDirectory(prefix="k3p-release-fake-submissions-") as directory:
        root = Path(directory)
        first, second = root / "first.bin", root / "second.bin"
        first.write_bytes(b"not a journal package\n")
        second.write_bytes(b"also not a journal package\n")
        packages = submission_argument_map([
            f"systematic_biology={first}",
            f"journal_of_mathematical_biology={second}",
        ])
        for kind, path in packages.items():
            verify_submission_package(
                path, kind=kind, commit="a" * 40, expected_uploads={},
                expected_members={},
            )


def mislabeled_submission_archive() -> None:
    with tempfile.TemporaryDirectory(prefix="k3p-release-mislabeled-submission-") as directory:
        path = Path(directory) / "mislabeled.zip"
        manifest = {
            "schema": "k3p-journal-submission-package-v1",
            "status": "READY",
            "kind": "journal_of_mathematical_biology",
            "source_commit": "a" * 40,
            "members": [],
        }
        manifest["payload_sha256"] = sha256_bytes(canonical_json_bytes(manifest))
        with zipfile.ZipFile(path, mode="w") as archive:
            archive.writestr(
                f"{SUBMISSION_ROOTS['systematic_biology']}/SUBMISSION_PACKAGE_MANIFEST.json",
                json.dumps(manifest, sort_keys=True).encode(),
            )
        verify_submission_package(
            path, kind="systematic_biology", commit="a" * 40,
            expected_uploads={}, expected_members={},
        )


def malicious_submission_extra() -> None:
    kind = "systematic_biology"
    uploads = {
        "K3P_level2_main_SB.pdf": {"sha256": sha256_bytes(b"main"), "bytes": 4,
                                    "path": "fixture/main.pdf"},
        "K3P_level2_supplement_SB.pdf": {
            "sha256": sha256_bytes(b"supp"), "bytes": 4, "path": "fixture/supp.pdf"
        },
        "cover_letter.pdf": {"sha256": sha256_bytes(b"cover"), "bytes": 5,
                             "path": "fixture/cover.pdf"},
    }
    expected_members = {
        "main.tex": b"source\n", "K3P_level2_main_SB.pdf": b"main",
        "K3P_level2_supplement_SB.pdf": b"supp", "cover_letter.pdf": b"cover",
    }
    observed = dict(expected_members)
    observed["MANIFEST.json"] = b'{"status":"DRAFT_NOT_READY"}\n'
    rows = [{"path": relative, "sha256": sha256_bytes(data), "bytes": len(data)}
            for relative, data in sorted(observed.items())]
    manifest = {
        "schema": "k3p-journal-submission-package-v1", "status": "READY",
        "kind": kind, "source_commit": "a" * 40, "members": rows,
    }
    manifest["payload_sha256"] = sha256_bytes(canonical_json_bytes(manifest))
    with tempfile.TemporaryDirectory(prefix="k3p-release-extra-submission-") as directory:
        path = Path(directory) / "extra.zip"
        with zipfile.ZipFile(path, mode="w") as archive:
            root = SUBMISSION_ROOTS[kind]
            for relative, data in observed.items():
                archive.writestr(f"{root}/{relative}", data)
            archive.writestr(f"{root}/SUBMISSION_PACKAGE_MANIFEST.json",
                             json.dumps(manifest, sort_keys=True).encode())
        verify_submission_package(
            path, kind=kind, commit="a" * 40, expected_uploads=uploads,
            expected_members=expected_members,
        )


def enforced_command_timeout() -> None:
    with tempfile.TemporaryDirectory(prefix="k3p-release-timeout-") as directory:
        transcript_path = Path(directory) / "timeout.log"
        with transcript_path.open("w+", encoding="utf-8") as transcript:
            run_one(
                Command(
                    "timeout_fixture",
                    [sys.executable, "-c", "import time; time.sleep(2)"],
                    timeout_seconds=1,
                ),
                deterministic_environment(PROJECT), transcript,
            )


def enforced_descendant_timeout() -> None:
    with tempfile.TemporaryDirectory(prefix="k3p-release-descendant-timeout-") as directory:
        root = Path(directory)
        marker = root / "descendant-survived"
        child = f"import time; time.sleep(2); open({str(marker)!r}, 'w').write('survived')"
        parent = (
            "import subprocess,sys,time; "
            f"subprocess.Popen([sys.executable,'-c',{child!r}]); time.sleep(10)"
        )
        transcript_path = root / "timeout.log"
        try:
            with transcript_path.open("w+", encoding="utf-8") as transcript:
                run_one(Command("descendant_timeout_fixture",
                                [sys.executable, "-c", parent], timeout_seconds=1),
                        deterministic_environment(PROJECT), transcript)
        except ReleaseFailure as error:
            require("command timeout" in str(error), "descendant timeout diagnostic")
            time.sleep(2.25)
            require(not marker.exists(), "timed-out descendant survived process-group kill")
            raise ReleaseFailure("command timeout descendant process group killed") from error


def forged_suite_command_plan() -> None:
    work = RELEASE / "work"
    work.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="suite-forgery-", dir=work) as directory:
        root = Path(directory)
        commands = quick_commands(sys.executable, False)
        plan = normalized_command_plan(commands)
        bindings = suite_code_bindings(PROJECT)
        plan_hash = sha256_bytes(canonical_json_bytes(plan))
        records = [{
            "name": command.name,
            "argv": command.argv,
            "exit_code": 0,
            "sentinel": command.sentinel,
            "sentinel_seen": True,
            "timeout_seconds": command.timeout_seconds,
            "elapsed_seconds": 0.0,
            "transcript_sha256": "0" * 64,
            "status": "PASS",
        } for command in commands]
        header = {
            "schema": "k3p-release-suite-transcript-v1",
            "mode": "quick",
            "source_commit": head_commit(PROJECT),
            "command_count": len(plan),
            "command_plan_sha256": plan_hash,
            **bindings,
            "environment": {
                "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0",
                "LC_ALL": "C", "LANG": "C", "TZ": "UTC",
                "SOURCE_DATE_EPOCH": str(head_commit_epoch(PROJECT)),
            },
        }
        transcript_path = root / "quick.log"
        transcript_path.write_text(
            json.dumps(header, sort_keys=True) + "\n" +
            "\n".join("RESULT " + json.dumps(row, sort_keys=True) for row in records) +
            "\n", encoding="utf-8",
        )
        transcript_relative = transcript_path.relative_to(PROJECT).as_posix()
        report = {
            "schema": "k3p-release-suite-report-v1", "status": "PASS",
            "mode": "quick", "source_commit": head_commit(PROJECT),
            "command_count": len(records), "command_plan": plan,
            "command_plan_sha256": plan_hash, "commands": records,
            "elapsed_seconds": 0.0,
            "peak_memory": {"ru_maxrss_raw": 0, "ru_maxrss_unit": "bytes",
                            "peak_bytes": 0},
            "tracked_fingerprint_before": tracked_worktree_fingerprint(PROJECT),
            "tracked_fingerprint_after": tracked_worktree_fingerprint(PROJECT),
            "tracked_worktree_unchanged": True, "clean_checkout_required": True,
            "initial_status": [], "final_status": [],
            "transcript": {"path": transcript_relative,
                           "sha256": sha256_file(transcript_path),
                           "bytes": transcript_path.stat().st_size},
            **bindings, "python_version": platform.python_version(),
        }
        report["command_plan"][0]["name"] = "forged_release_inputs"
        report["command_plan_sha256"] = sha256_bytes(canonical_json_bytes(
            report["command_plan"]
        ))
        report["payload_sha256"] = sha256_bytes(canonical_json_bytes(report))
        report_path = root / "quick.json"
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8")
        verify_suite_report(PROJECT, report_path, {transcript_relative})


def unknown_release_envelope_field() -> None:
    final_release_verifier.validate_envelope_field_set({
        "journal_submissions_completed": True
    })


def tampered_generated_readme() -> None:
    final_release_verifier.verify_generated_bytes(
        b"tampered instructions\n", b"canonical instructions\n", label="fixture"
    )


def tampered_archive_sidecar() -> None:
    with tempfile.TemporaryDirectory(prefix="sidecar-tamper-") as directory:
        root = Path(directory)
        archive = root / "release.zip"
        sidecar = root / "release.zip.sha256"
        archive.write_bytes(b"canonical archive bytes")
        sidecar.write_text(f"{'0' * 64}  {archive.name}\n", encoding="utf-8")
        final_release_verifier.verify_archive_sidecar(
            archive, sidecar, label="fixture"
        )


def dirty_final_verification() -> None:
    with tempfile.TemporaryDirectory(prefix="dirty-final-verifier-") as directory:
        root = Path(directory)
        project = root / "program"
        project.mkdir()
        tracked = project / "tracked.txt"
        tracked.write_text("clean\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Release Test"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "release@example.invalid"],
                       cwd=root, check=True)
        subprocess.run(["git", "add", "program/tracked.txt"], cwd=root, check=True)
        subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"],
                       cwd=root, check=True)
        tracked.write_text("dirty\n", encoding="utf-8")
        final_release_verifier.require_final_clean_state(project)


def forged_source_reproduction_builds() -> None:
    policy = load_head_json(PROJECT, "release/RELEASE_FILESET.json")
    report = {
        "schema": "k3p-pdf-source-reproduction-v1", "status": "PASS_BYTE_FOR_BYTE",
        "kind": "article", "source_commit": head_commit(PROJECT),
        "source_archive": {}, "expected_pdf": {}, "committed_source_binding": {},
        "builds": [{"run": 1, "sha256": "1" * 64, "bytes": 1,
                    "elapsed_seconds": 0.0, "transcript": "forged.log",
                    "transcript_sha256": "2" * 64}],
        "byte_identical_across_two_builds": True,
        "byte_identical_to_delivered_pdf": True,
        "tool_versions": {"tectonic": {
            "path": "/fake/tectonic", "sha256": policy["tectonic_sha256"],
            "version": policy["tectonic_version"],
        }},
        "environment": {"SOURCE_DATE_EPOCH": str(policy["pdf_source_date_epoch"]),
                        "TZ": "UTC", "LC_ALL": "C"},
        "logical_payload_sha256": "3" * 64,
    }
    final_release_verifier.validate_source_reproduction_evidence(
        report, kind="article", commit=head_commit(PROJECT),
        pdf_record={"sha256": "1" * 64, "bytes": 1}, policy=policy,
        transcript_records={},
    )


def deterministic_controls() -> list[dict]:
    with tempfile.TemporaryDirectory(prefix="k3p-release-determinism-") as directory:
        root = Path(directory)
        members = {"z.txt": b"z\n", "a/data.json": b"{}\n",
                   "bin/check.py": b"#!/usr/bin/env python3\n"}
        tar1, tar2 = root / "one.tar.gz", root / "two.tar.gz"
        zip1, zip2 = root / "one.zip", root / "two.zip"
        common = dict(kind="test", archive_root="root", source_commit="d" * 40,
                      source_date_epoch=1_700_000_000, members=members)
        deterministic_tar_gz(tar1, **common)
        deterministic_tar_gz(tar2, **common)
        deterministic_zip(zip1, **common)
        deterministic_zip(zip2, **common)
        require(tar1.read_bytes() == tar2.read_bytes(), "nondeterministic TAR.GZ builder")
        require(zip1.read_bytes() == zip2.read_bytes(), "nondeterministic ZIP builder")
        tar_report, zip_report = verify_tar_gz(tar1), verify_zip(zip1)
        tar_extract, zip_extract = root / "tar_extract", root / "zip_extract"
        safe_extract_tar_gz(tar1, tar_extract)
        safe_extract_zip(zip1, zip_extract)
        extracted_modes = {
            "tar_script": (tar_extract / "root/bin/check.py").stat().st_mode & 0o777,
            "tar_data": (tar_extract / "root/a/data.json").stat().st_mode & 0o777,
            "zip_script": (zip_extract / "root/bin/check.py").stat().st_mode & 0o777,
            "zip_data": (zip_extract / "root/a/data.json").stat().st_mode & 0o777,
        }
        require(extracted_modes == {
            "tar_script": 0o755, "tar_data": 0o644,
            "zip_script": 0o755, "zip_data": 0o644,
        }, ("safe extraction mode preservation", extracted_modes))
        return [
            {"name": "tar_gz_double_build", "status": "PASS_IDENTICAL",
             "sha256": tar_report["sha256"]},
            {"name": "zip_double_build", "status": "PASS_IDENTICAL",
             "sha256": zip_report["sha256"]},
            {"name": "safe_extraction_mode_preservation", "status": "PASS",
             "modes": {key: format(value, "04o")
                       for key, value in extracted_modes.items()}},
        ]


def duplicate_active_path_control() -> dict:
    digest = "1" * 64
    manifest = {
        "active_gate_reports": [{"path": "safe/evidence.json", "sha256": digest}],
        "active_theorem_artifacts": [],
        "active_verifiers": [{"path": "safe/evidence.json"}],
        "claim_locks": [],
    }
    certification = {
        "classification_gate": "safe/gate.py",
        "classification_gate_sha256": "2" * 64,
        "classification_mutation_gate": "safe/mutations.py",
        "classification_mutation_gate_sha256": "3" * 64,
        "classification_mutation_report": "safe/mutations.json",
        "classification_mutation_report_sha256": "4" * 64,
    }
    records = active_paths(manifest, {"bindings": {}}, {"certification": certification})
    evidence_rows = [row for row in records if row[0] == "safe/evidence.json"]
    require(evidence_rows == [("safe/evidence.json", digest)],
            ("duplicate active path normalization", records))
    return {"name": "duplicate_active_path_hash_normalization", "status": "PASS",
            "records": evidence_rows}


def untracked_exclusion_control() -> dict:
    with tempfile.TemporaryDirectory(prefix="k3p-release-git-") as directory:
        root = Path(directory)
        project = root / "program"
        project.mkdir()
        (project / "tracked.txt").write_text("tracked\n")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Release Test"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "release@example.invalid"],
                       cwd=root, check=True)
        subprocess.run(["git", "add", "program/tracked.txt"], cwd=root, check=True)
        subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"],
                       cwd=root, check=True)
        (project / "untracked.txt").write_text("must not ship\n")
        entries = tracked_head_entries(project)
        require(set(entries) == {"tracked.txt"} and "untracked.txt" not in entries,
                ("untracked file entered release selection", entries))
        return {"name": "git_head_only_selection", "status": "PASS",
                "tracked": sorted(entries), "untracked_excluded": True}


def nested_compact_dependency_control() -> dict:
    """A path bound inside a nested hash map must enter the compact archive."""
    with tempfile.TemporaryDirectory(prefix="k3p-compact-closure-") as directory:
        root = Path(directory)
        project = root / "program"
        initial = {
            "FINAL_CLAIM_LOCK.json": b"{}\n",
            "clean_room/verify_h21_transport_and_fourteen_orbits.py": b"# fixture\n",
            "reproducibility/verify_k3p_same_classification.py": b"# fixture\n",
            "reproducibility/test_k3p_same_classification_mutations.py": b"# fixture\n",
            "reproducibility/K3P_SAME_CLASSIFICATION_MUTATION_REPORT.json": b"{}\n",
            "restoration/verify_k3p_restoration.py": b"# fixture\n",
            "clean_room/adversarial/HARDENED_H21_REAUDIT.json":
                b'{"active_input_hashes": []}\n',
            "reports/primary_gate_report.json": (
                b'{"input_binding": {"observed_sha256": {'
                b'"input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py": "'
                + b"0" * 64 + b'"}}}\n'
            ),
            "input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py": b"# required fixture\n",
        }
        gate = {
            "bindings": {
                "reports/primary_gate_report.json": "1" * 64,
                "clean_room/adversarial/HARDENED_H21_REAUDIT.json": "2" * 64,
            }
        }
        initial["reproducibility/K3P_SAME_CLASSIFICATION_GATE_REPORT.json"] = (
            json.dumps(gate, sort_keys=True) + "\n"
        ).encode()
        for relative, data in initial.items():
            path = project / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Release Test"],
                       cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "release@example.invalid"],
                       cwd=root, check=True)
        subprocess.run(["git", "add", "program"], cwd=root, check=True)
        subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"],
                       cwd=root, check=True)
        expected = sorted(initial)
        policy = {
            "expected_compact_selection_count": len(expected),
            "expected_compact_selection_sha256": sha256_bytes(
                canonical_json_bytes(expected)
            ),
        }
        selected = compact_selection(project, policy)
        required = "input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py"
        require(required in selected,
                ("nested observed_sha256 dependency omitted", selected))
        return {
            "name": "nested_compact_dependency_closure",
            "status": "PASS",
            "selected_head_files": len(selected),
            "required_nested_path": required,
        }


def dirty_worktree_policy_control() -> dict:
    with tempfile.TemporaryDirectory(prefix="k3p-release-head-policy-") as directory:
        root = Path(directory)
        project = root / "program"
        policy = project / "release/RELEASE_FILESET.json"
        policy.parent.mkdir(parents=True)
        policy.write_text('{"policy": "committed"}\n')
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Release Test"],
                       cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "release@example.invalid"],
                       cwd=root, check=True)
        subprocess.run(["git", "add", "program/release/RELEASE_FILESET.json"],
                       cwd=root, check=True)
        subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"],
                       cwd=root, check=True)
        policy.write_text('{"policy": "dirty-worktree"}\n')
        observed = load_head_json(project, "release/RELEASE_FILESET.json")
        require(observed == {"policy": "committed"},
                ("dirty worktree policy affected HEAD policy", observed))
        return {"name": "dirty_worktree_policy_ignored", "status": "PASS",
                "observed": observed}


def regeneration_plan_control() -> dict:
    commands = regeneration_commands(sys.executable, False)
    names = [command.name for command in commands]
    required = {
        "cut_topology_graph_regeneration", "cut_topology_graph_compare",
        "cut_topology_graph_mutations",
        "cut_signed_pair_mutations", "cut_record39_audit", "cut_record43_audit",
        "cut_record60_audit", "cut_cyclic_verify_optimized",
        "cut_k3p_directed_inclusion_evidence_build",
        "cut_global_transfer_release_optimized", "sharpness_krawczyk_producer",
        "sharpness_topology_alln_producer", "probe_hour_scale_producer",
        "probe_full_semantic_replay", "four_port_full_universe_producer",
        "non_four_anchor_universe_producer",
        "four_port_full_universe_structure_compare",
        "four_port_full_universe_mutations", "restoration_report_portability",
        "clean_room_hardened_adversarial",
        "tree_sunlet_literal_v2_build", "tree_sunlet_literal_v2_verify",
        "tree_sunlet_literal_v2_mutations",
    }
    require(len(names) == len(set(names)) == 56 and required.issubset(names),
            ("regeneration plan coverage", sorted(required - set(names))))
    command_map = {command.name: command.argv for command in commands}
    require("--fresh" in command_map["cut_single_minor_search"],
            "single-minor regeneration is not fresh")
    require("--mutations" in command_map["cut_cyclic_verify"] and
            "--mutations" in command_map["cut_cyclic_verify_optimized"] and
            "--mutations" in command_map["cut_global_transfer_verify"] and
            "--mutations" in command_map["cut_global_transfer_verify_optimized"],
            "cut regeneration omits hostile mutations")
    require(names.index("cut_cyclic_verify_optimized") <
            names.index("cut_cyclic_manifest") and
            names.index("cut_k3p_directed_inclusion_evidence_build") <
            names.index("cut_global_transfer_build") and
            names.index("cut_global_transfer_release_optimized") <
            names.index("cut_global_transfer_manifest"),
            "regeneration manifest ordering")
    ordered_fixed_point = [
        "cut_topology_graph_regeneration",
        "cut_topology_graph_compare",
        "cut_topology_graph_mutations",
        "tree_sunlet_literal_v2_build",
        "tree_sunlet_literal_v2_verify",
        "tree_sunlet_literal_v2_mutations",
        "four_port_full_universe_producer",
        "non_four_anchor_universe_producer",
        "restoration_full_producer",
        "restoration_independent_replay",
        "restoration_mutations",
        "restoration_report_portability",
        "four_port_full_universe_structure_compare",
        "four_port_full_universe_mutations",
        "probe_hour_scale_producer",
        "probe_independent_replay",
        "probe_full_semantic_replay",
        "probe_mutations",
        "probe_manifest_seal",
        "global_infrastructure_build",
        "global_infrastructure_verify",
        "global_infrastructure_mutations",
        "clean_room_hardened_adversarial",
        "primary_rebind",
        "release_inputs",
        "integrated_fresh_independent_replay",
        "integrated_classification_mutations",
        "release_engineering_mutations",
    ]
    require(all(names.index(left) < names.index(right) for left, right in
                zip(ordered_fixed_point, ordered_fixed_point[1:])),
            ("regeneration fixed-point ordering", ordered_fixed_point))
    require("--no-write-report" in command_map["probe_mutations"] and
            "--output" in command_map["probe_independent_replay"] and
            "--output" in command_map["probe_full_semantic_replay"] and
            "--mutations-output" in command_map["probe_full_semantic_replay"] and
            "--report" in command_map["four_port_full_universe_mutations"],
            "regeneration would overwrite runtime-bearing reports")
    deterministic_environment(PROJECT)
    ephemeral_parent = PROJECT / "release/work/regeneration_ephemeral"
    require(ephemeral_parent.is_dir(),
            "regeneration ephemeral output parent was not materialized")
    return {"name": "complete_regeneration_plan", "status": "PASS",
            "command_count": len(commands), "required_commands": sorted(required),
            "ordered_fixed_point": ordered_fixed_point,
            "ephemeral_output_parent": ephemeral_parent.relative_to(PROJECT).as_posix()}


def deterministic_diagnostic_control() -> dict:
    first = canonical_diagnostic(
        f"failure at {tempfile.gettempdir()}/k3p-release-case-first/input.bin"
    )
    second = canonical_diagnostic(
        f"failure at {tempfile.gettempdir()}/k3p-release-case-second/input.bin"
    )
    require(first == second == "failure at <TEMP_DIR>/input.bin",
            "temporary diagnostic canonicalization")
    return {"name": "deterministic_diagnostics", "status": "PASS",
            "canonical_example": first}


def proof_only_exclusion_control() -> dict:
    policy = load_head_json(PROJECT, "release/RELEASE_FILESET.json")
    selected = full_selection(PROJECT, validate_release_policy(policy), require_pdfs=False)
    require(ARTICLE_PDF not in selected and SUPPLEMENT_PDF not in selected,
            "proof-only selection retained release PDFs")
    return {"name": "proof_only_pdf_exclusion", "status": "PASS",
            "selected_head_files": len(selected)}


def inventory_fixture_records() -> list[dict[str, str]]:
    return [{"record_id": f"input-{index:03d}"} for index in range(1, 37)]


def certified_manifest_input_drift() -> None:
    records = inventory_fixture_records()
    active = [row["record_id"] for row in records
              if row["record_id"] not in {"input-023", "input-032"}]
    with tempfile.TemporaryDirectory(prefix="k3p-inventory-drift-") as directory:
        manifest_path = Path(directory) / "ACTIVE_MANIFEST.json"
        manifest_path.write_text(json.dumps({
            "status": "CERTIFIED_K3P_SAME_MATHEMATICS_PUBLICATION_ENGINEERING_PENDING",
            "active_inputs": active[1:],
            "provenance_only_inputs": ["input-023", "input-032"],
        }), encoding="utf-8")
        preserve_or_write_bootstrap_manifest(records, manifest_path)


def certified_manifest_preservation_control() -> dict:
    records = inventory_fixture_records()
    active = [row["record_id"] for row in records
              if row["record_id"] not in {"input-023", "input-032"}]
    with tempfile.TemporaryDirectory(prefix="k3p-inventory-preserve-") as directory:
        manifest_path = Path(directory) / "ACTIVE_MANIFEST.json"
        manifest_path.write_text(json.dumps({
            "status": "CERTIFIED_K3P_SAME_MATHEMATICS_PUBLICATION_ENGINEERING_PENDING",
            "active_inputs": active,
            "provenance_only_inputs": ["input-023", "input-032"],
            "certification_sentinel": "must-survive-inventory-refresh",
        }, sort_keys=True), encoding="utf-8")
        before = manifest_path.read_bytes()
        preserve_or_write_bootstrap_manifest(records, manifest_path)
        require(manifest_path.read_bytes() == before,
                "certified active manifest was downgraded by inventory refresh")
    return {"name": "certified_active_manifest_preservation", "status": "PASS"}


def main(argv: list[str] | None = None) -> int:
    try:
        refuse_optimized_python()
        parser = argparse.ArgumentParser()
        parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
        parser.add_argument("--no-write-report", action="store_true")
        args = parser.parse_args(argv)
        cases = [
            rejected("stale_checksum", "stale file SHA-256", stale_checksum),
            rejected("stale_archive_member_hash", "archive member hash or size",
                     stale_manifest_hash),
            rejected("self_referential_archive_hash", "SELF_REFERENTIAL_ARCHIVE_HASH",
                     self_referential_archive_hash),
            rejected("self_referential_checksum_list", "self-referential checksum list",
                     checksum_self_reference),
            rejected("path_traversal_primitive", "path traversal forbidden",
                     traversal_primitive),
            rejected("path_traversal_zip", "path traversal forbidden", traversal_zip),
            rejected("noncanonical_zip_timestamp", "noncanonical ZIP member mtime",
                     noncanonical_zip_timestamp),
            rejected("noncanonical_tar_mode", "noncanonical manifest mode",
                     noncanonical_tar_mode),
            rejected("optimized_input_gate", "OPTIMIZED_PYTHON_FORBIDDEN",
                     optimized_input_gate),
            rejected("optimized_archive_builder", "OPTIMIZED_PYTHON_FORBIDDEN",
                     optimized_archive_builder),
            rejected("forbidden_active_evidence", "FORBIDDEN_ACTIVE_EVIDENCE",
                     forbidden_active_path),
            rejected("missing_active_evidence_path", "active evidence path required",
                     missing_active_path),
            rejected("wrong_source_build_engine", "source build command policy",
                     wrong_source_build_engine),
            rejected("fake_tectonic_executable", "Tectonic executable SHA-256 policy",
                     fake_tectonic_executable),
            rejected("wrong_pdf_source_date_epoch", "PDF source-date epoch policy",
                     wrong_pdf_source_date_epoch),
            rejected("inconsistent_source_build_environment",
                     "source build environment policy",
                     inconsistent_source_build_environment),
            rejected("pdf_equivalent_source_archive_tamper",
                     "source archive member differs from HEAD",
                     pdf_equivalent_source_archive_tamper),
            rejected("malformed_fileset_policy", "release fileset schema",
                     malformed_fileset_policy),
            rejected("wrong_fileset_selection_lock", "full release selection lock",
                     wrong_fileset_selection_lock),
            rejected("not_ready_submission_report", "submission packages are not READY",
                     not_ready_submission_report),
            rejected("arbitrary_submission_files", "not a ZIP submission package",
                     arbitrary_submission_files),
            rejected("mislabeled_submission_archive", "submission package kind",
                     mislabeled_submission_archive),
            rejected("malicious_submission_extra",
                     "journal package exact HEAD/source-map member set",
                     malicious_submission_extra),
            rejected("enforced_command_timeout", "command timeout",
                     enforced_command_timeout),
            rejected("enforced_descendant_timeout", "command timeout",
                     enforced_descendant_timeout),
            rejected("forged_suite_command_plan", "release suite exact command plan",
                     forged_suite_command_plan),
            rejected("unknown_release_envelope_field", "release envelope field set",
                     unknown_release_envelope_field),
            rejected("tampered_generated_readme", "generated README binding",
                     tampered_generated_readme),
            rejected("tampered_archive_sidecar", "archive sidecar content",
                     tampered_archive_sidecar),
            rejected("dirty_final_verification", "final verification requires a clean project",
                     dirty_final_verification),
            rejected("forged_source_reproduction_builds",
                     "source-reproduction build count",
                     forged_source_reproduction_builds),
            rejected("certified_manifest_input_drift",
                     "certified ACTIVE_MANIFEST active-input set drift",
                     certified_manifest_input_drift),
        ]
        controls = deterministic_controls()
        controls.append(untracked_exclusion_control())
        controls.append(nested_compact_dependency_control())
        controls.append(duplicate_active_path_control())
        controls.append(dirty_worktree_policy_control())
        controls.append(regeneration_plan_control())
        controls.append(deterministic_diagnostic_control())
        controls.append(proof_only_exclusion_control())
        controls.append(certified_manifest_preservation_control())
        report = {
            "schema": "k3p-release-engineering-mutations-v1",
            "status": "PASS",
            "mutation_count": len(cases),
            "rejected": sum(row["status"] == "REJECTED" for row in cases),
            "survived": 0,
            "mutations": cases,
            "controls": controls,
            "verifier_sha256": sha256_file(Path(__file__).resolve()),
            "release_common_sha256": sha256_file(HERE / "release_common.py"),
            "release_suite_sha256": sha256_file(HERE / "run_release_suite.py"),
            "release_input_verifier_sha256": sha256_file(HERE / "verify_release_inputs.py"),
            "archive_builder_sha256": sha256_file(RELEASE / "build_release.py"),
            "archive_tools_sha256": sha256_file(RELEASE / "archive_tools.py"),
            "release_verifier_sha256": sha256_file(RELEASE / "verify_release.py"),
            "source_reproduction_verifier_sha256": sha256_file(
                RELEASE / "verify_source_reproduction.py"
            ),
            "submission_validator_sha256": sha256_file(
                PROJECT / "submission/validate_submission_packages.py"
            ),
            "submission_validator_mutations_sha256": sha256_file(
                PROJECT / "submission/test_submission_validators.py"
            ),
            "probe_mutation_driver_sha256": sha256_file(
                PROJECT / "probes/test_k3p_probe_mutations.py"
            ),
            "cut_single_minor_producer_sha256": sha256_file(
                PROJECT / "cut_recovery/strong_crossbridge/search_cut_minor_signs.py"
            ),
            "fileset_policy_sha256": sha256_file(RELEASE / "RELEASE_FILESET.json"),
        }
        report["payload_sha256"] = sha256_bytes(canonical_json_bytes(report))
        if not args.no_write_report:
            atomic_write(args.output.resolve(),
                         (json.dumps(report, indent=2, sort_keys=True) + "\n").encode())
        print(json.dumps(report, indent=2, sort_keys=True))
        print("K3P_RELEASE_ENGINEERING_MUTATIONS_PASS")
        return 0
    except (ReleaseFailure, OSError, UnicodeError, ValueError, json.JSONDecodeError,
            subprocess.SubprocessError) as error:
        print(f"K3P_RELEASE_ENGINEERING_MUTATIONS_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
