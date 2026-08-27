#!/usr/bin/env python3
"""Compare packaged ledgers with repository commits without importing package code."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


MANIFEST = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
TELEMETRY = "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(repo: Path, revision: str, path: str) -> bytes | None:
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f"{revision}:{path}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def compare(repo: Path, revision: str, prefix: str, root: Path, paths: list[str]) -> dict[str, object]:
    missing: list[str] = []
    mismatched: list[str] = []
    for relative in paths:
        data = git_bytes(repo, revision, f"{prefix}/{relative}")
        if data is None:
            missing.append(relative)
        elif data != (root / relative).read_bytes():
            mismatched.append(relative)
    return {
        "revision": revision,
        "checked": len(paths),
        "missing": missing,
        "mismatched": mismatched,
        "status": "PASS" if not missing and not mismatched else "FAIL",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("repo", type=Path)
    parser.add_argument("prefix")
    parser.add_argument("tag_commit")
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    frozen = sorted(manifest["frozen_evidence"]["files"])
    sources = sorted(manifest["submission_sources"]["files"])
    all_paths = sorted(set(frozen) | set(sources) | {MANIFEST})
    telemetry = json.loads((root / TELEMETRY).read_text(encoding="utf-8"))
    replay_commit = telemetry["git_commit"]
    replay_inputs = sorted(
        set(frozen)
        | set(telemetry["submission_sources"])
    )
    result = {
        "tag_commit_all_archive_members": compare(
            args.repo, args.tag_commit, args.prefix, root, all_paths
        ),
        "replay_commit_frozen_and_five_sources": compare(
            args.repo, replay_commit, args.prefix, root, replay_inputs
        ),
        "telemetry_sha256": sha((root / TELEMETRY).read_bytes()),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
