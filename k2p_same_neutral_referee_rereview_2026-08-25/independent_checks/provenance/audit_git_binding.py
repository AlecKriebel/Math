#!/usr/bin/env python3
"""Compare every extracted referee-package byte to one or more Git commits."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise SystemExit(f"{code}: {detail!r}")


def run(repo: Path, *arguments: str, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, "GIT_COMMAND_FAIL", {
        "arguments": arguments,
        "stderr": result.stderr.decode("utf-8", "replace")[-2000:],
    })
    return result.stdout


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree(repo: Path, commit: str, project_in_repo: str) -> dict[str, tuple[str, str]]:
    raw = run(repo, "ls-tree", "-r", "-z", commit, "--", project_in_repo)
    rows: dict[str, tuple[str, str]] = {}
    prefix = project_in_repo.rstrip("/") + "/"
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, kind, object_id = metadata.decode("ascii").split(" ")
        path = raw_path.decode("utf-8")
        require(path.startswith(prefix), "GIT_TREE_PREFIX", path)
        relative = path[len(prefix) :]
        require(relative not in rows, "GIT_DUPLICATE_PATH", relative)
        require(kind == "blob", "GIT_TREE_NONBLOB", (relative, kind))
        rows[relative] = (mode, object_id)
    return rows


def batch_blobs(repo: Path, rows: dict[str, tuple[str, str]]) -> dict[str, bytes]:
    process = subprocess.Popen(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(process.stdin is not None and process.stdout is not None, "GIT_BATCH_PIPE_MISSING")
    stdin = process.stdin
    stdout = process.stdout
    result: dict[str, bytes] = {}
    for relative, (_, object_id) in rows.items():
        stdin.write(object_id.encode("ascii") + b"\n")
        stdin.flush()
        header = stdout.readline().decode("ascii").rstrip("\n")
        fields = header.split(" ")
        require(len(fields) == 3 and fields[0] == object_id and fields[1] == "blob", "GIT_BATCH_HEADER", header)
        size = int(fields[2])
        data = stdout.read(size)
        delimiter = stdout.read(1)
        require(len(data) == size and delimiter == b"\n", "GIT_BATCH_TRUNCATED", relative)
        result[relative] = data
    stdin.close()
    returncode = process.wait()
    stderr = process.stderr.read() if process.stderr is not None else b""
    require(returncode == 0, "GIT_BATCH_FAIL", stderr.decode("utf-8", "replace"))
    return result


def compare_commit(
    repo: Path, project: Path, project_in_repo: str, commit: str, package_files: list[str]
) -> dict[str, Any]:
    resolved = run(repo, "rev-parse", f"{commit}^{{commit}}").decode("ascii").strip()
    rows = tree(repo, resolved, project_in_repo)
    missing = sorted(set(package_files) - set(rows))
    selected = {path: rows[path] for path in package_files if path in rows}
    blobs = batch_blobs(repo, selected)
    mismatches: list[dict[str, Any]] = []
    modes: dict[str, int] = {}
    for relative in selected:
        disk = (project / relative).read_bytes()
        committed = blobs[relative]
        if disk != committed:
            mismatches.append(
                {
                    "path": relative,
                    "package_sha256": sha(disk),
                    "commit_sha256": sha(committed),
                    "package_bytes": len(disk),
                    "commit_bytes": len(committed),
                }
            )
        mode = selected[relative][0]
        modes[mode] = modes.get(mode, 0) + 1
    return {
        "requested_revision": commit,
        "resolved_commit": resolved,
        "repository_project_file_count": len(rows),
        "package_file_count": len(package_files),
        "matching_package_file_count": len(selected) - len(mismatches),
        "missing_package_file_count": len(missing),
        "missing_package_files": missing,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "selected_git_modes": modes,
        "exact_package_match": not missing and not mismatches,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--project-in-repo", required=True)
    parser.add_argument("--revision", action="append", required=True)
    parser.add_argument("--result", required=True, type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    manifest_relative = (
        "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
    )
    manifest = json.loads((project / manifest_relative).read_text(encoding="utf-8"))
    package_files = sorted(
        set(manifest["frozen_evidence"]["files"])
        | set(manifest["submission_sources"]["files"])
        | {manifest_relative}
    )
    comparisons = [
        compare_commit(
            args.repo.resolve(), project, args.project_in_repo, revision, package_files
        )
        for revision in args.revision
    ]
    result = {
        "schema": "independent-k2p-package-git-binding-audit-v1",
        "status": "PASS" if any(row["exact_package_match"] for row in comparisons) else "NO_EXACT_COMMIT_MATCH",
        "comparisons": comparisons,
    }
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
