#!/usr/bin/env python3
"""Independently bind stored full-replay telemetry to its Git commit and package."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = child
    return value


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(), object_pairs_hook=unique_object)
    if not isinstance(value, dict):
        raise ValueError(f"not a JSON object: {path}")
    return value


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(repository: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.decode("utf-8", "replace"))
    return result.stdout


def git_bytes(repository: Path, commit: str, path: str) -> bytes:
    return run(repository, "show", f"{commit}:{path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--repository-project-path", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    submission = project / "proof_compression_submission"
    telemetry_path = submission / "output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json"
    report_path = submission / "output/FINAL_CLEAN_FULL_REPLAY.json"
    telemetry = load(telemetry_path)
    report = load(report_path)
    commit = telemetry["git_commit"]
    project_prefix = args.repository_project_path.rstrip("/")

    report_row = telemetry["report"]
    report_hash_match = report_row["sha256"] == sha_bytes(report_path.read_bytes())
    report_summary_match = (
        report["status"] == "PASS"
        and report_row["layer_count"] == len(report["layer_replays"])
        and report_row["internal_elapsed_seconds"] == report["elapsed_seconds"]
        and report_row["lock_payload_sha256"] == report["lock_payload_sha256"]
        and report_row["promotion_ready"] is report["promotion_ready"] is True
        and report_row["blocker_count"] == len(report["blockers"]) == 0
    )

    binding_mismatches: list[str] = []
    commit_mismatches: list[str] = []
    for relative, row in telemetry["submission_sources"].items():
        current = project / relative
        if current.stat().st_size != row["bytes"] or sha_bytes(current.read_bytes()) != row["sha256"]:
            binding_mismatches.append(relative)
        tagged_path = f"{project_prefix}/{relative}"
        if sha_bytes(git_bytes(args.repository, commit, tagged_path)) != row["sha256"]:
            commit_mismatches.append(relative)
    lock_row = telemetry["release_lock"]
    lock_relative = lock_row["path"]
    lock_path = project / lock_relative
    if lock_path.stat().st_size != lock_row["bytes"] or sha_bytes(lock_path.read_bytes()) != lock_row["sha256"]:
        binding_mismatches.append(lock_relative)
    if sha_bytes(git_bytes(args.repository, commit, f"{project_prefix}/{lock_relative}")) != lock_row["sha256"]:
        commit_mismatches.append(lock_relative)

    # Extend the audit beyond the telemetry's explicit six bindings: every
    # transitive frozen file in the revised manifest must be unchanged between
    # the replay commit and the distributed tag.
    revised = load(submission / "crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json")
    frozen = revised["frozen_evidence"]["files"]
    frozen_changed_since_replay: list[str] = []
    frozen_missing_at_replay: list[str] = []
    for relative, row in frozen.items():
        try:
            data = git_bytes(args.repository, commit, f"{project_prefix}/{relative}")
        except ValueError:
            frozen_missing_at_replay.append(relative)
            continue
        if len(data) != row["bytes"] or sha_bytes(data) != row["sha256"]:
            frozen_changed_since_replay.append(relative)

    tag_commit = run(args.repository, "rev-parse", f"{args.tag}^{{}}").decode().strip()
    ancestor = subprocess.run(
        ["git", "-C", str(args.repository), "merge-base", "--is-ancestor", commit, tag_commit],
        check=False,
    ).returncode == 0
    result = {
        "telemetry": {
            "bytes": telemetry_path.stat().st_size,
            "sha256": sha_bytes(telemetry_path.read_bytes()),
            "schema": telemetry.get("schema"),
            "status": telemetry.get("status"),
            "clean_detached_checkout": telemetry.get("clean_detached_checkout"),
            "git_commit": commit,
            "command": telemetry.get("command"),
            "runtime": telemetry.get("runtime"),
            "time_l": telemetry.get("time_l"),
        },
        "report": {
            "bytes": report_path.stat().st_size,
            "sha256": sha_bytes(report_path.read_bytes()),
            "hash_matches_telemetry": report_hash_match,
            "summary_matches_telemetry": report_summary_match,
            "mode": report.get("mode"),
            "layer_count": len(report.get("layer_replays", [])),
            "status": report.get("status"),
            "elapsed_seconds": report.get("elapsed_seconds"),
        },
        "explicit_binding_mismatches": sorted(set(binding_mismatches)),
        "explicit_commit_mismatches": sorted(set(commit_mismatches)),
        "frozen_file_count": len(frozen),
        "frozen_files_changed_since_replay": frozen_changed_since_replay,
        "frozen_files_missing_at_replay": frozen_missing_at_replay,
        "tag": args.tag,
        "tag_commit": tag_commit,
        "replay_commit_is_ancestor_of_tag": ancestor,
        "wall_time_not_below_internal": telemetry["time_l"]["real_seconds"] >= report["elapsed_seconds"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
