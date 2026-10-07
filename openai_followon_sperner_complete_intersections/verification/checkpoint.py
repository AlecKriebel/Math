#!/usr/bin/env python3
"""Publish only owned project artifacts on remote main using an isolated index.

The shared checkout, branch and index are not changed; a non-force push can fail
safely when another researcher updates main concurrently. No releases are made.
"""
from pathlib import Path
import datetime
import json
import os
import subprocess
import sys

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent


def run(args, env=None):
    return subprocess.check_output(args, cwd=REPO, env=env, text=True).strip()


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: checkpoint.py checkpoint_name commit_message")
    label, message = sys.argv[1:]
    before = {"head": run(["git", "rev-parse", "HEAD"]), "index_tree": run(["git", "write-tree"])}
    if run(["git", "branch", "--show-current"]) != "main":
        raise RuntimeError("main-only instruction: refusing a different branch")
    idx = PROJECT / "receipts" / (label + ".index")
    idx.unlink(missing_ok=True)
    env = dict(os.environ, GIT_INDEX_FILE=str(idx))
    try:
        run(["git", "fetch", "--no-tags", "origin", "main"])
        parent = run(["git", "rev-parse", "FETCH_HEAD"])
        run(["git", "read-tree", parent], env)
        run(["git", "add", "--", str(PROJECT.relative_to(REPO))], env)
        tree = run(["git", "write-tree"], env)
        changed = run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", parent, tree]).splitlines()
        assert all(path.startswith(PROJECT.name + "/") for path in changed)
        commit = run(["git", "commit-tree", tree, "-p", parent, "-m", message])
        result = subprocess.run(["git", "push", "origin", commit + ":refs/heads/main"], cwd=REPO, capture_output=True, text=True)
        after = {"head": run(["git", "rev-parse", "HEAD"]), "index_tree": run(["git", "write-tree"])}
        receipt = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   "base_remote_main": parent, "commit": commit, "changed_owned_files": changed,
                   "push_exit": result.returncode, "push_output": result.stdout + result.stderr,
                   "shared_before": before, "shared_after": after, "shared_state_equal": before == after}
        (PROJECT / "receipts" / (label + "_push.json")).write_text(json.dumps(receipt, indent=2) + "\n")
        print(json.dumps({k: receipt[k] for k in ["commit", "push_exit", "shared_state_equal", "push_output"]}, indent=2))
        if result.returncode:
            raise SystemExit(result.returncode)
    finally:
        idx.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
