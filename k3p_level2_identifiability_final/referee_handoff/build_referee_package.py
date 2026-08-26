#!/usr/bin/env python3
"""Copy the sealed proof payload into an inspectable referee handoff folder."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
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
    ])
    paths.extend(tracked_work_logs())
    return paths


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
    require(len(paths) == 18, ("tracked WORK_LOG count", len(paths)))
    return paths


def copy_payload(candidate: Path, archive: Path, archive_record: dict) -> dict:
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
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })
    return rows


def write_outer_manifests(candidate: Path, *, commit: str, archive: Path,
                          archive_record: dict) -> dict:
    rows = payload_rows(candidate)
    manifest = {
        "schema": "k3p-independent-referee-package-v1",
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
    sum_paths = [row["path"] for row in rows] + ["PACKAGE_MANIFEST.json"]
    sums = "".join(
        f"{sha256_file(candidate / relative)}  {relative}\n"
        for relative in sorted(sum_paths)
    )
    (candidate / "SHA256SUMS").write_text(sums, encoding="utf-8")
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
            copied = copy_payload(candidate, archive, archive_record)
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
