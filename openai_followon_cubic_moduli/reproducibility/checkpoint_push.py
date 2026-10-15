"""Publish owned research notes on remote main without changing shared index/HEAD.

Usage: python3 checkpoint_push.py 'Commit message' relative-owned-path ...
Only files within this effort are accepted. Never force-pushes.
"""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
PREFIX = "openai_followon_cubic_moduli/"

def git(*args, env=None):
    return subprocess.check_output(["git", *args], cwd=ROOT, env=env, text=True).strip()

def main():
    message, *paths = sys.argv[1:]
    if not paths or any(not p.startswith(PREFIX) or ".." in Path(p).parts for p in paths):
        raise ValueError("Only explicit owned project paths are permitted")
    if git("branch", "--show-current") != "main":
        raise RuntimeError("Shared checkout must stay on main")
    before = git("rev-parse", "HEAD")
    for attempt in range(1, 6):
        git("fetch", "--no-auto-gc", "origin", "main")
        parent = git("rev-parse", "FETCH_HEAD")
        with tempfile.TemporaryDirectory(prefix="cubic-index-", dir=ROOT / PREFIX / "receipts") as d:
            env = dict(os.environ, GIT_INDEX_FILE=str(Path(d) / "index"))
            git("read-tree", parent, env=env)
            git("add", "--", *paths, env=env)
            changed = git("diff", "--cached", "--name-only", parent, env=env).splitlines()
            if any(not p.startswith(PREFIX) for p in changed):
                raise RuntimeError("Isolated index includes unrelated paths")
            tree = git("write-tree", env=env)
            commit = subprocess.check_output(
                ["git", "commit-tree", tree, "-p", parent], cwd=ROOT, env=env,
                input=message + "\n", text=True).strip()
            result = subprocess.run(["git", "push", "origin", commit + ":refs/heads/main"],
                                    cwd=ROOT, text=True, capture_output=True)
            if result.returncode:
                if "non-fast-forward" in result.stderr or "fetch first" in result.stderr or "failed to update ref" in result.stderr:
                    continue
                raise RuntimeError(result.stderr)
            remote = git("ls-remote", "origin", "refs/heads/main").split()[0]
            receipt = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                       "parent": parent, "commit": commit, "remote_main_at_check": remote,
                       "shared_head_before": before, "shared_head_after": git("rev-parse", "HEAD"),
                       "paths": changed, "attempt": attempt, "push_success": True,
                       "method": "isolated index; commit-tree; non-force push to main"}
            out = ROOT / PREFIX / "receipts" / ("push_" + commit[:12] + ".json")
            out.write_text(json.dumps(receipt, indent=2) + "\n")
            print(json.dumps(receipt, indent=2))
            return
    raise RuntimeError("Concurrent remote updates prevented push after five safe retries")

if __name__ == "__main__":
    main()
