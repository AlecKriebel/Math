#!/usr/bin/env python3
"""Copy the sealed proof payload into an inspectable referee handoff folder."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile


PROJECT = Path(__file__).resolve().parents[1]
HANDOFF = PROJECT / "referee_handoff"
DEFAULT_ARCHIVE = PROJECT / "release/dist/k3p_level2_reproducibility.tar.gz"
DEFAULT_OUTPUT = PROJECT / "release/dist/K3P_Level2_Independent_Referee_Package"

sys.path.insert(0, str(PROJECT / "release"))
from archive_tools import safe_extract_tar_gz, verify_tar_gz  # noqa: E402
from build_release import load_release_policy  # noqa: E402
from verify_release import validate_source_reproduction_evidence  # noqa: E402
from verify_source_reproduction import verify_source_archive_contract  # noqa: E402


class PackageFailure(RuntimeError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise PackageFailure(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def head_commit() -> str:
    result = subprocess.run(
        ["git", "-C", str(PROJECT), "rev-parse", "HEAD"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        check=False, timeout=30,
    )
    require(result.returncode == 0, ("cannot resolve Git HEAD", result.stderr))
    return result.stdout.strip()


def repository_root() -> Path:
    result = subprocess.run(
        ["git", "-C", str(PROJECT), "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        check=False, timeout=30,
    )
    require(result.returncode == 0, ("cannot resolve repository root", result.stderr))
    return Path(result.stdout.strip()).resolve()


def require_head_blobs(paths: list[Path]) -> None:
    root = repository_root()
    for path in sorted(set(paths)):
        require(path.is_file() and not path.is_symlink(),
                ("builder input must be a regular file", str(path)))
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError as error:
            raise PackageFailure(("builder input outside repository", str(path))) from error
        result = subprocess.run(
            ["git", "-C", str(root), "show", f"HEAD:{relative}"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False, timeout=60,
        )
        require(result.returncode == 0 and result.stdout == path.read_bytes(),
                ("builder input is untracked or differs from HEAD", relative))


def handoff_inputs() -> list[Path]:
    paths = []
    for path in HANDOFF.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            paths.append(path)
    paths.extend([
        PROJECT / "output/pdf/K3P_Level2_Identifiability_Article.pdf",
        PROJECT / "output/pdf/K3P_Level2_Identifiability_Reader_Supplement.pdf",
        PROJECT / "release/FINAL_RELEASE_ENGINEERING_REPORT.md",
        # These live modules are imported by this builder.  Bind them to the
        # claimed package-builder commit before accepting ignored evidence.
        PROJECT / "release/archive_tools.py",
        PROJECT / "release/build_release.py",
        PROJECT / "release/TECTONIC_CACHE_MANIFEST.json",
        PROJECT / "release/verify_release.py",
        PROJECT / "release/verify_source_reproduction.py",
        PROJECT / "reproducibility/release_common.py",
        PROJECT / "reproducibility/run_release_suite.py",
        PROJECT / "submission/validate_submission_packages.py",
    ])
    paths.extend(tracked_work_logs())
    return paths


def exact_project_evidence_path(relative: object, *, expected: str,
                                label: str) -> Path:
    require(isinstance(relative, str) and relative == expected and
            "\\" not in relative and "\x00" not in relative,
            (f"noncanonical {label} path", relative, expected))
    pure = PurePosixPath(relative)
    require(not pure.is_absolute() and ".." not in pure.parts and
            pure.as_posix() == relative,
            (f"unsafe {label} path", relative))
    path = (PROJECT / Path(*pure.parts)).resolve()
    try:
        path.relative_to(PROJECT.resolve())
    except ValueError as error:
        raise PackageFailure((f"{label} path outside project", relative)) from error
    return path


def tracked_work_logs() -> list[Path]:
    prefix_result = subprocess.run(
        ["git", "-C", str(PROJECT), "rev-parse", "--show-prefix"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        check=False, timeout=30,
    )
    files_result = subprocess.run(
        ["git", "-C", str(PROJECT), "ls-files", "--", "*WORK_LOG.md"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        check=False, timeout=30,
    )
    require(prefix_result.returncode == files_result.returncode == 0,
            "cannot enumerate tracked work logs")
    prefix = prefix_result.stdout.strip()
    paths = []
    for line in files_result.stdout.splitlines():
        relative = line.removeprefix(prefix)
        path = PROJECT / relative
        require(path.is_file() and path.name.endswith("WORK_LOG.md"),
                ("invalid work-log path", relative))
        paths.append(path)
    paths = sorted(set(paths))
    require(len(paths) == 20, ("tracked WORK_LOG count", len(paths)))
    return paths


def source_reproduction_evidence(commit: str) -> list[Path]:
    evidence_root = PROJECT / "release/source_reproduction_evidence"
    policy = load_release_policy(PROJECT)
    paths = []
    for kind, pdf_name in (
        ("article", "K3P_Level2_Identifiability_Article.pdf"),
        ("supplement", "K3P_Level2_Identifiability_Reader_Supplement.pdf"),
    ):
        report_path = evidence_root / f"{kind}.json"
        require(report_path.is_file() and not report_path.is_symlink(),
                ("missing final-commit source-reproduction report", kind,
                 str(report_path)))
        report = json.loads(report_path.read_text(encoding="utf-8"))
        require(report.get("source_commit") == commit,
                ("stale source-reproduction report commit", kind,
                 report.get("source_commit"), commit))
        transcript_records = {}
        transcript_paths = []
        source_record = report.get("source_archive", {})
        source_relative = source_record.get("path")
        expected_source_relative = (
            f"release/dist/k3p_level2_{kind}_source.zip"
        )
        source_archive = exact_project_evidence_path(
            source_relative, expected=expected_source_relative,
            label=f"{kind} source archive",
        )
        require(source_archive.is_file() and not source_archive.is_symlink() and
                source_record.get("sha256") == sha256_file(source_archive),
                ("source-archive evidence binding", kind, source_relative))
        archive_report, _build, committed_binding = verify_source_archive_contract(
            source_archive, kind=kind, project=PROJECT, policy=policy
        )
        require(source_record == {
                    "path": expected_source_relative,
                    "sha256": sha256_file(source_archive),
                    "structural_verification": archive_report,
                } and
                report.get("committed_source_binding") == committed_binding,
                ("source archive/HEAD semantic binding", kind))
        builds = report.get("builds", [])
        require(isinstance(builds, list) and len(builds) == 2,
                ("source-reproduction build count", kind))
        for run_number, build in enumerate(builds, 1):
            relative = build.get("transcript")
            expected_transcript = (
                "release/source_reproduction_evidence/"
                f"{kind}_transcripts/run{run_number}.log"
            )
            transcript = exact_project_evidence_path(
                relative, expected=expected_transcript,
                label=f"{kind} run-{run_number} transcript",
            )
            require(transcript.is_file() and not transcript.is_symlink(),
                    ("missing source-reproduction transcript", relative))
            transcript_records[relative] = {"sha256": sha256_file(transcript)}
            transcript_paths.append(transcript)
        pdf = PROJECT / "output/pdf" / pdf_name
        require(pdf.is_file() and not pdf.is_symlink(),
                ("missing canonical PDF", kind, str(pdf)))
        validate_source_reproduction_evidence(
            report, kind=kind, commit=commit,
            pdf_record={"sha256": sha256_file(pdf), "bytes": pdf.stat().st_size},
            policy=policy, transcript_records=transcript_records,
        )
        require(len(transcript_paths) == len(set(transcript_paths)) == 2,
                ("source-reproduction transcript count", kind,
                 len(transcript_paths)))
        paths.extend([report_path, source_archive, *transcript_paths])
    require(len(paths) == len(set(paths)) == 8,
            ("source-reproduction evidence count/uniqueness", len(paths),
             len(set(paths))))
    return sorted(paths)


def copy_payload(candidate: Path, archive: Path, archive_record: dict,
                 source_evidence: list[Path]) -> dict:
    extraction = candidate.parent / "archive_extraction"
    extraction.mkdir(parents=True, exist_ok=False)
    safe_extract_tar_gz(archive, extraction)
    archive_root = extraction / archive_record["archive_root"]
    require(archive_root.is_dir(), "missing extracted archive root")
    proof = candidate / "proof_package"
    shutil.copytree(archive_root, proof)

    logs = tracked_work_logs()
    added_logs = 0
    for source in logs:
        relative = source.relative_to(PROJECT)
        destination = proof / relative
        if destination.exists():
            require(destination.is_file() and
                    sha256_file(destination) == sha256_file(source),
                    ("archive work-log mismatch", relative.as_posix()))
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        added_logs += 1

    release_ledger = PROJECT / "release/FINAL_RELEASE_ENGINEERING_REPORT.md"
    release_ledger_destination = proof / "release/FINAL_RELEASE_ENGINEERING_REPORT.md"
    if release_ledger_destination.exists():
        require(sha256_file(release_ledger_destination) == sha256_file(release_ledger),
                "archive release-ledger mismatch")
    else:
        release_ledger_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(release_ledger, release_ledger_destination)

    for source in source_evidence:
        relative = source.relative_to(PROJECT)
        destination = proof / relative
        require(not destination.exists(),
                ("source-reproduction evidence unexpectedly in canonical archive",
                 relative.as_posix()))
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    paper = candidate / "paper"
    paper.mkdir(parents=True)
    pdf_names = (
        "K3P_Level2_Identifiability_Article.pdf",
        "K3P_Level2_Identifiability_Reader_Supplement.pdf",
    )
    for name in pdf_names:
        source = PROJECT / "output/pdf" / name
        require(source.is_file(), ("missing PDF", name))
        proof_copy = proof / "output/pdf" / name
        require(proof_copy.is_file() and
                sha256_file(proof_copy) == sha256_file(source),
                ("paper/proof-core PDF mismatch", name))
        shutil.copy2(source, paper / name)

    for name in ("START_HERE.md", "REFEREE_PROMPT.md", "RUN_REVIEW.sh"):
        shutil.copy2(HANDOFF / name, candidate / name)
    shutil.copytree(
        HANDOFF / "referee_tools", candidate / "referee_tools",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    (candidate / "RUN_REVIEW.sh").chmod(0o755)
    for script in (candidate / "referee_tools").glob("*.py"):
        script.chmod(0o755)
    return {
        "work_logs_present": len(logs),
        "work_logs_added_to_archive_core": added_logs,
        "final_release_ledger_present": True,
        "source_reproduction_evidence_files": len(source_evidence),
        "pdfs_copied": len(pdf_names),
    }


def payload_rows(candidate: Path) -> list[dict[str, object]]:
    rows = []
    for path in sorted(candidate.rglob("*")):
        relative = path.relative_to(candidate).as_posix()
        metadata = path.lstat()
        require(not stat.S_ISLNK(metadata.st_mode),
                ("symlink forbidden in candidate", relative))
        if stat.S_ISDIR(metadata.st_mode):
            continue
        require(stat.S_ISREG(metadata.st_mode),
                ("nonregular object forbidden in candidate", relative))
        if (relative in {"PACKAGE_MANIFEST.json", "SHA256SUMS"}
                or "__pycache__" in path.parts or relative.endswith(".pyc")):
            continue
        rows.append({
            "path": relative,
            "bytes": metadata.st_size,
            "mode": format(stat.S_IMODE(metadata.st_mode), "04o"),
            "sha256": sha256_file(path),
        })
    return rows


def write_outer_manifests(candidate: Path, *, commit: str, archive: Path,
                          archive_record: dict) -> dict:
    rows = payload_rows(candidate)
    manifest = {
        "schema": "k3p-independent-referee-package-v2",
        "package_name": "K3P_Level2_Independent_Referee_Package",
        "package_builder_commit": commit,
        "proof_source_commit": archive_record["source_commit"],
        "canonical_archive_sha256": sha256_file(archive),
        "payload_file_count": len(rows),
        "payload_bytes": sum(row["bytes"] for row in rows),
        "payload": rows,
    }
    manifest_path = candidate / "PACKAGE_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                             encoding="utf-8")
    manifest_path.chmod(0o644)
    sum_paths = [row["path"] for row in rows] + ["PACKAGE_MANIFEST.json"]
    sums = "".join(
        f"{sha256_file(candidate / relative)}  {relative}\n"
        for relative in sorted(sum_paths)
    )
    sums_path = candidate / "SHA256SUMS"
    sums_path.write_text(sums, encoding="utf-8")
    sums_path.chmod(0o644)
    return manifest


def verify_candidate(candidate: Path) -> dict:
    command = [
        sys.executable,
        str(candidate / "referee_tools/verify_package_integrity.py"),
        "--package-root", str(candidate),
    ]
    result = subprocess.run(
        command, cwd=candidate, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, check=False, timeout=600,
    )
    require(result.returncode == 0 and
            "K3P_REFEREE_PACKAGE_INTEGRITY_PASS" in result.stdout,
            ("candidate integrity verification failed", result.stdout[-4000:]))
    return {"status": "PASS", "transcript": result.stdout.strip()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    archive = args.archive.resolve()
    output = args.output.resolve()
    try:
        require(archive.is_file(), ("missing canonical archive", str(archive)))
        require(not output.exists(), ("referee package output already exists", str(output)))
        require_head_blobs(handoff_inputs())
        source_evidence = source_reproduction_evidence(head_commit())
        output.parent.mkdir(parents=True, exist_ok=True)
        archive_record = verify_tar_gz(archive)
        commit = head_commit()
        require(archive_record["source_commit"] == commit,
                ("archive/HEAD commit mismatch", archive_record["source_commit"], commit))
        work_parent = PROJECT / "release/work"
        work_parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="referee-package-", dir=work_parent) as directory:
            temporary = Path(directory)
            candidate = temporary / "candidate"
            candidate.mkdir()
            copied = copy_payload(
                candidate, archive, archive_record, source_evidence
            )
            manifest = write_outer_manifests(
                candidate, commit=commit, archive=archive,
                archive_record=archive_record,
            )
            verification = verify_candidate(candidate)
            require(not (candidate / ".venv").exists() and
                    not (candidate / "review_runs").exists(),
                    "runtime state forbidden in delivered package")
            shutil.copytree(candidate, output)
        print(json.dumps({
            "status": "PASS",
            "output": str(output),
            "package_builder_commit": commit,
            "proof_source_commit": archive_record["source_commit"],
            "payload_file_count": manifest["payload_file_count"],
            "payload_bytes": manifest["payload_bytes"],
            "canonical_archive_sha256": manifest["canonical_archive_sha256"],
            **copied,
            "integrity_verification": verification["status"],
        }, indent=2, sort_keys=True))
        print("K3P_REFEREE_PACKAGE_BUILD_PASS")
        return 0
    except (PackageFailure, OSError, UnicodeError, json.JSONDecodeError,
            subprocess.SubprocessError, TypeError, ValueError) as error:
        print(f"K3P_REFEREE_PACKAGE_BUILD_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
