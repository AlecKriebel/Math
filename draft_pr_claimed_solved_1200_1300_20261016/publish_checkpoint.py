#!/usr/bin/env python3
"""Publish this directory alone to remote main without touching the shared index."""
import datetime
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PRIVATE = ROOT / "_local"
PRIVATE.mkdir(exist_ok=True)


def git(*args, env=None):
    result = subprocess.run(["git", "-c", "gc.auto=0", *args], cwd=REPO,
                            env=env, text=True, capture_output=True, check=True)
    return result.stdout.strip()


def main():
    if git("branch", "--show-current") != "main":
        raise RuntimeError("Shared checkout must remain on main")
    message = PRIVATE / "commit-message.txt"
    message.write_text("Record strict QUEUE eligibility skips for draft PRs 1200–1300\n\n"
                       "All 101 drafts reference queued targets; preserve exact-status "
                       "gate and independent verification without processing their math.\n")
    for attempt in range(1, 5):
        remote = git("ls-remote", "origin", "refs/heads/main").split()[0]
        git("fetch", "--no-auto-maintenance", "--no-tags", "--no-write-fetch-head",
            "origin", remote)
        env = dict(os.environ, GIT_INDEX_FILE=str(PRIVATE / f"index-{attempt}"))
        git("read-tree", remote, env=env)
        git("add", "--", ROOT.name, env=env)
        tree = git("write-tree", env=env)
        commit = git("commit-tree", tree, "-p", remote, "-F", str(message))
        changed = git("diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines()
        if not changed or any(not p.startswith(ROOT.name + "/") for p in changed):
            raise RuntimeError("Checkpoint tree includes no change or a foreign path")
        push = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin",
                               commit + ":refs/heads/main"], cwd=REPO,
                              text=True, capture_output=True)
        receipt = {"at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   "attempt": attempt, "base": remote, "commit": commit,
                   "changed_files": changed, "push_returncode": push.returncode,
                   "push_stdout": push.stdout, "push_stderr": push.stderr,
                   "shared_branch": git("branch", "--show-current"),
                   "shared_head": git("rev-parse", "HEAD"),
                   "shared_index_modified_by_this_tool": False}
        if push.returncode == 0:
            tip = git("ls-remote", "origin", "refs/heads/main").split()[0]
            if tip != commit:
                git("fetch", "--no-auto-maintenance", "--no-tags", "--no-write-fetch-head",
                    "origin", tip)
                git("merge-base", "--is-ancestor", commit, tip)
            receipt["verified_remote_tip"] = tip
            (PRIVATE / "push_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
            print(json.dumps({"commit": commit, "base": remote,
                              "verified_remote_tip": tip, "files": len(changed)}, indent=2))
            return
        (PRIVATE / f"push_attempt_{attempt}.json").write_text(json.dumps(receipt, indent=2) + "\n")
        if "non-fast-forward" not in push.stderr and "fetch first" not in push.stderr:
            raise RuntimeError(push.stderr)
    raise RuntimeError("Remote main advanced on every bounded attempt; no force push attempted")


if __name__ == "__main__":
    main()
