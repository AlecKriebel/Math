#!/usr/bin/env python3
"""Publish explicit owned paths on current remote main without changing checkout/index.

No reset, branch creation, force-push, shared-index writes, or shared-ref updates.
An advancing remote causes a normal push rejection; rerun after inspecting it.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent

def git(*args, env=None):
    return subprocess.check_output(["git", *args], cwd=REPO, env=env, text=True).strip()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--message", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("paths", nargs="+")
    args = ap.parse_args()
    if git("branch", "--show-current") != "main":
        raise SystemExit("Shared checkout must remain on main.")
    shared_head = git("rev-parse", "HEAD")
    shared_index = Path(git("rev-parse", "--git-path", "index"))
    if not shared_index.is_absolute():
        shared_index = REPO / shared_index
    index_before = digest(shared_index)
    paths = []
    file_hashes = {}
    for raw in args.paths:
        path = (REPO / raw).resolve()
        if not path.is_relative_to(PROJECT) or not path.is_file() or path.is_symlink():
            raise SystemExit(f"Invalid owned regular-file path: {raw}")
        rel = str(path.relative_to(REPO))
        ignored = subprocess.run(["git", "check-ignore", "--no-index", "-q", rel], cwd=REPO).returncode
        if ignored == 0:
            raise SystemExit(f"Ignored path: {rel}")
        if ignored != 1:
            raise SystemExit("Could not determine ignore status.")
        paths.append(rel)
        file_hashes[rel] = digest(path)
    remote = git("ls-remote", "origin", "refs/heads/main").split()[0]
    subprocess.run(["git", "fetch", "--no-write-fetch-head", "origin", remote], cwd=REPO, check=True, stdout=subprocess.DEVNULL)
    with tempfile.TemporaryDirectory(prefix="checkpoint-", dir=PROJECT / "verification") as tmp:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(tmp) / "index"))
        git("read-tree", remote, env=env)
        git("add", "--", *paths, env=env)
        tree = git("write-tree", env=env)
        for rel, expected in file_hashes.items():
            if digest(REPO / rel) != expected:
                raise SystemExit(f"Owned file changed while staging: {rel}")
        commit = subprocess.check_output(["git", "commit-tree", tree, "-p", remote], input=args.message + "\n", cwd=REPO, env=env, text=True).strip()
        subprocess.run(["git", "push", "origin", f"{commit}:refs/heads/main"], cwd=REPO, check=True)
    head_after = git("rev-parse", "HEAD")
    index_after = digest(shared_index)
    receipt = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "commit": commit, "parent_remote_main": remote, "tree": tree,
        "message": args.message, "owned_paths_sha256": file_hashes,
        "remote_main_readback": git("ls-remote", "origin", "refs/heads/main").split()[0],
        "shared_head_before": shared_head, "shared_head_after": head_after,
        "shared_index_sha256_before": index_before,
        "shared_index_sha256_after": index_after,
        "checkout_and_index_untouched_by_this_script": True,
        "concurrent_shared_changes_observed": shared_head != head_after or index_before != index_after,
    }
    receipt_path = (REPO / args.receipt).resolve()
    if not receipt_path.is_relative_to(PROJECT):
        raise SystemExit("Receipt must be project-local.")
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"commit": commit, "receipt": str(receipt_path), "shared_head_unchanged": shared_head == head_after, "shared_index_unchanged": index_before == index_after}))

if __name__ == "__main__":
    main()
