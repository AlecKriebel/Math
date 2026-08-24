#!/usr/bin/env python3
"""Independent provenance audit for the K2P referee handoff.

This deliberately does not import any submitted verifier or producer module.
It walks the filesystem, recomputes hashes, checks both ledger payloads, audits
the five supplemental dependencies, and compares current bytes with the bound
Git commit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any


INNER_MANIFEST_REL = (
    "materials/k2p_principal_d_plus_submission_referee/"
    "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
)
INNER_MANIFEST_PROJECT_REL = (
    "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
)
PROJECT_REL = "materials/k2p_principal_d_plus_submission_referee"
REPO_PROJECT_PREFIX = "k2p_level2_identifiability_closure"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def safe_relative(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(path.parts) and not path.is_absolute() and all(
        part not in {"", ".", ".."} for part in path.parts
    )


def excluded_outer(relative: PurePosixPath) -> bool:
    if relative.as_posix() == "PACKAGE_MANIFEST.json":
        return True
    if relative.parts and relative.parts[0] in {".referee_venv", "referee_outputs"}:
        return True
    if ".venv" in relative.parts or "__pycache__" in relative.parts:
        return True
    if relative.name == ".DS_Store" or relative.suffix in {".pyc", ".pyo"}:
        return True
    return False


def excluded_inner(relative: PurePosixPath) -> bool:
    if ".venv" in relative.parts or "__pycache__" in relative.parts:
        return True
    return relative.name == ".DS_Store" or relative.suffix in {".pyc", ".pyo"}


def walk_regular(root: Path, exclusion) -> tuple[dict[str, dict[str, int | str]], list[str]]:
    rows: dict[str, dict[str, int | str]] = {}
    bad_nodes: list[str] = []
    for directory, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        base = Path(directory)
        retained_dirs: list[str] = []
        for name in sorted(dirnames):
            path = base / name
            relative = PurePosixPath(path.relative_to(root).as_posix())
            if exclusion(relative):
                continue
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
                bad_nodes.append(relative.as_posix())
                continue
            retained_dirs.append(name)
        dirnames[:] = retained_dirs
        for name in sorted(filenames):
            path = base / name
            relative = PurePosixPath(path.relative_to(root).as_posix())
            if exclusion(relative):
                continue
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
                bad_nodes.append(relative.as_posix())
                continue
            rows[relative.as_posix()] = {
                "bytes": path.stat().st_size,
                "sha256": sha_file(path),
            }
    return dict(sorted(rows.items())), sorted(bad_nodes)


def compare_rows(
    declared: dict[str, Any], actual: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[str], list[str], list[str]]:
    checks: list[dict[str, Any]] = []
    missing = sorted(set(declared) - set(actual))
    unexpected = sorted(set(actual) - set(declared))
    mismatched: list[str] = []
    for relative in sorted(set(declared) & set(actual)):
        match = declared[relative] == actual[relative]
        if not match:
            mismatched.append(relative)
        checks.append(
            {
                "path": relative,
                "declared": declared[relative],
                "actual": actual[relative],
                "match": match,
            }
        )
    return checks, missing, unexpected, mismatched


def git_bytes(repo: Path, commit: str, relative: str) -> bytes:
    run = subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if run.returncode:
        raise RuntimeError(
            f"git show failed for {commit}:{relative}: "
            f"{run.stderr.decode('utf-8', errors='replace')}"
        )
    return run.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--source-archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.handoff.resolve()
    project = root / PROJECT_REL
    outer = json.loads((root / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    inner = json.loads((root / INNER_MANIFEST_REL).read_text(encoding="utf-8"))
    binding = json.loads((root / "SUBMISSION_BINDING.json").read_text(encoding="utf-8"))

    assertions: list[dict[str, Any]] = []

    def record(name: str, observed: Any, expected: Any) -> None:
        assertions.append(
            {"name": name, "observed": observed, "expected": expected, "pass": observed == expected}
        )

    outer_unsigned = dict(outer)
    outer_payload = outer_unsigned.pop("payload_sha256", None)
    record("outer_payload_sha256", sha_bytes(canonical(outer_unsigned)), outer_payload)
    actual_outer, outer_bad_nodes = walk_regular(root, excluded_outer)
    outer_checks, outer_missing, outer_unexpected, outer_mismatched = compare_rows(
        outer["files"], actual_outer
    )
    record("outer_bad_nodes", outer_bad_nodes, [])
    record("outer_missing_paths", outer_missing, [])
    record("outer_unexpected_paths", outer_unexpected, [])
    record("outer_mismatched_rows", outer_mismatched, [])
    record("outer_file_count", len(actual_outer), outer["file_count_excluding_manifest"])
    record(
        "outer_total_bytes",
        sum(int(row["bytes"]) for row in actual_outer.values()),
        outer["total_bytes_excluding_manifest"],
    )
    record("outer_content_root", sha_bytes(canonical(actual_outer)), outer["content_root_sha256"])
    record("outer_all_paths_safe", all(safe_relative(path) for path in outer["files"]), True)

    inner_unsigned = dict(inner)
    inner_payload = inner_unsigned.pop("payload_sha256", None)
    record("inner_payload_sha256", sha_bytes(canonical(inner_unsigned)), inner_payload)
    frozen = inner["frozen_evidence"]["files"]
    submission = inner["submission_sources"]["files"]
    record("inner_frozen_count", len(frozen), inner["frozen_evidence"]["file_count"])
    record("inner_submission_count", len(submission), inner["submission_sources"]["file_count"])
    record("inner_combined_count", len(frozen) + len(submission), inner["combined_file_count_excluding_manifest"])
    record("inner_map_overlap", sorted(set(frozen) & set(submission)), [])
    record("inner_all_paths_safe", all(safe_relative(path) for path in set(frozen) | set(submission)), True)
    record(
        "frozen_content_ledger_root",
        sha_bytes(canonical(frozen)),
        inner["frozen_evidence"]["content_ledger_root_sha256"],
    )
    record(
        "submission_content_ledger_root",
        sha_bytes(canonical(submission)),
        inner["submission_sources"]["content_ledger_root_sha256"],
    )
    record(
        "inner_combined_content_root",
        sha_bytes(canonical({"frozen_evidence": frozen, "submission_sources": submission})),
        inner["combined_content_root_sha256"],
    )
    listed_inner = {**frozen, **submission}
    actual_listed = {}
    for relative in sorted(listed_inner):
        path = project / relative
        actual_listed[relative] = {
            "bytes": path.stat().st_size if path.is_file() else None,
            "sha256": sha_file(path) if path.is_file() else None,
        }
    inner_checks, inner_missing, inner_unexpected_unused, inner_mismatched = compare_rows(
        listed_inner, actual_listed
    )
    record("inner_missing_listed_paths", inner_missing, [])
    record("inner_mismatched_rows", inner_mismatched, [])

    dependencies = binding["supplemental_execution_dependencies_added_outside_the_inner_seal"]
    actual_inner, inner_bad_nodes = walk_regular(project, excluded_inner)
    expected_complete_inner = set(listed_inner) | {INNER_MANIFEST_PROJECT_REL} | set(dependencies)
    record("inner_bad_nodes", inner_bad_nodes, [])
    record("inner_complete_file_count", len(actual_inner), len(expected_complete_inner))
    record("inner_unexpected_unsealed_files", sorted(set(actual_inner) - expected_complete_inner), [])
    record("inner_missing_expected_files", sorted(expected_complete_inner - set(actual_inner)), [])

    sealed_by_hash: dict[tuple[int, str], list[str]] = {}
    for relative, row in listed_inner.items():
        sealed_by_hash.setdefault((int(row["bytes"]), str(row["sha256"])), []).append(relative)

    commit = binding["git"]["commit"]
    dependency_rows: list[dict[str, Any]] = []
    for relative, row in sorted(dependencies.items()):
        path = project / relative
        data = path.read_bytes()
        observed = {"bytes": len(data), "sha256": sha_bytes(data)}
        matches = sorted(sealed_by_hash.get((len(data), observed["sha256"]), []))
        declared_copy = row.get("matching_inner_sealed_copy")
        repo_relative = f"{REPO_PROJECT_PREFIX}/{relative}"
        committed = git_bytes(args.repo, commit, repo_relative)
        dependency_rows.append(
            {
                "path": relative,
                "observed": observed,
                "declared_sha256": row.get("sha256"),
                "source_git_commit": row.get("source_git_commit"),
                "git_path": repo_relative,
                "git_sha256": sha_bytes(committed),
                "git_bytes_identical": committed == data,
                "sealed_hash_matches": matches,
                "declared_matching_copy": declared_copy,
                "declared_copy_exact": (
                    declared_copy in matches if declared_copy is not None else not matches
                ),
            }
        )
    record(
        "dependency_hash_bindings",
        all(row["observed"]["sha256"] == row["declared_sha256"] for row in dependency_rows),
        True,
    )
    record(
        "dependency_commit_field",
        all(row["source_git_commit"] == commit for row in dependency_rows),
        True,
    )
    record(
        "dependency_git_bytes",
        all(row["git_bytes_identical"] for row in dependency_rows),
        True,
    )
    record(
        "dependency_sealed_copy_declarations",
        all(row["declared_copy_exact"] for row in dependency_rows),
        True,
    )
    record(
        "dependency_count_with_sealed_copy",
        sum(bool(row["sealed_hash_matches"]) for row in dependency_rows),
        2,
    )

    source_rows: list[dict[str, Any]] = []
    for relative, declared_sha in sorted(binding["five_source_set"].items()):
        data = (project / relative).read_bytes()
        committed = git_bytes(args.repo, commit, f"{REPO_PROJECT_PREFIX}/{relative}")
        source_rows.append(
            {
                "path": relative,
                "bytes": len(data),
                "sha256": sha_bytes(data),
                "declared_sha256": declared_sha,
                "git_sha256": sha_bytes(committed),
                "git_bytes_identical": committed == data,
            }
        )
    record("five_source_hash_bindings", all(r["sha256"] == r["declared_sha256"] for r in source_rows), True)
    record("five_source_git_bytes", all(r["git_bytes_identical"] for r in source_rows), True)

    source_archive_sha = sha_file(args.source_archive)
    record("source_archive_hash_outer", source_archive_sha, outer["source_archive_sha256"])
    record(
        "source_archive_hash_binding",
        source_archive_sha,
        binding["computational_evidence"]["source_archive_sha256"],
    )
    remote = subprocess.run(
        ["git", "remote", "get-url", "origin"], cwd=args.repo, capture_output=True, text=True, check=False
    )
    commit_type = subprocess.run(
        ["git", "cat-file", "-t", commit], cwd=args.repo, capture_output=True, text=True, check=False
    )
    record("git_commit_object_type", commit_type.stdout.strip(), "commit")

    status = "PASS" if all(row["pass"] for row in assertions) else "FAIL"
    result = {
        "schema": "independent-k2p-provenance-ledger-audit-v1",
        "status": status,
        "method": "independent os.walk/streaming-SHA256 implementation; no submitted module imported",
        "handoff": str(root),
        "repo": str(args.repo.resolve()),
        "git_remote_observed": remote.stdout.strip() if remote.returncode == 0 else None,
        "git_remote_declared": binding["git"]["repository"],
        "git_commit": commit,
        "assertions": assertions,
        "outer": {
            "actual_file_count": len(actual_outer),
            "actual_total_bytes": sum(int(row["bytes"]) for row in actual_outer.values()),
            "actual_content_root_sha256": sha_bytes(canonical(actual_outer)),
            "path_checks": outer_checks,
        },
        "inner": {
            "frozen_file_count": len(frozen),
            "submission_file_count": len(submission),
            "actual_complete_file_count": len(actual_inner),
            "path_checks": inner_checks,
        },
        "supplemental_dependencies": dependency_rows,
        "five_source_set": source_rows,
        "source_archive": {
            "path": str(args.source_archive.resolve()),
            "bytes": args.source_archive.stat().st_size,
            "sha256": source_archive_sha,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": status,
        "outer_files": len(actual_outer),
        "outer_bytes": sum(int(row["bytes"]) for row in actual_outer.values()),
        "inner_sealed_files": len(listed_inner),
        "inner_complete_files": len(actual_inner),
        "supplemental_dependencies": len(dependency_rows),
        "sealed_dependency_copies": sum(bool(row["sealed_hash_matches"]) for row in dependency_rows),
        "output": str(args.output.resolve()),
    }, sort_keys=True))
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()

