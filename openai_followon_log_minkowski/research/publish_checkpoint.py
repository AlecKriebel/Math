#!/usr/bin/env python3
"""Publish ONLY this project's files using an isolated index on remote main.

Does not reset, checkout, rebase, update local main, or touch the shared index.
On concurrent remote movement, rebuild the commit on the new remote main.
"""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
PROJECT = Path(__file__).resolve().parents[1]
REL = PROJECT.relative_to(ROOT).as_posix()

def run(args, *, env=None, data=None):
    p = subprocess.run(args, cwd=ROOT, env=env, input=data, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(f"{' '.join(args)} failed: {p.stderr.strip()}")
    return p.stdout.strip()

if len(sys.argv) != 2:
    raise SystemExit("usage: publish_checkpoint.py 'commit message'")
if run(["git", "branch", "--show-current"]) != "main":
    raise SystemExit("Shared checkout must remain on main")
scratch = PROJECT / "research" / ".scratch"
scratch.mkdir(exist_ok=True)
receipt = None
for attempt in range(1, 5):
    base = run(["git", "ls-remote", "origin", "refs/heads/main"]).split()[0]
    try:
        run(["git", "cat-file", "-e", base + "^{commit}"])
    except RuntimeError:
        run(["git", "fetch", "--no-tags", "origin", base])
    with tempfile.TemporaryDirectory(dir=scratch) as temp:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(temp) / "index"))
        run(["git", "read-tree", base], env=env)
        run(["git", "add", "--", REL], env=env)
        # Reference downloads and generated review trees remain local evidence.
        tracked = run(["git", "ls-files", "--", REL], env=env).splitlines()
        for path in tracked:
            relative = Path(path.removeprefix(REL + "/"))
            reference_copy = relative.parts[0] == "agent_notes" and any(
                part.endswith("_sources") for part in relative.parts[:-1])
            review_tree = relative.parts[0] == "reviews" and any(
                "_extract" in part or "_render" in part for part in relative.parts[:-1])
            if reference_copy or review_tree:
                run(["git", "update-index", "--force-remove", "--", path], env=env)
        changed = run(["git", "diff", "--cached", "--name-only", base], env=env).splitlines()
        if any(not p.startswith(REL + "/") for p in changed):
            raise SystemExit("Refusing an unowned changed path")
        if not changed:
            print(json.dumps({"status": "no_owned_changes", "remote_main": base}))
            raise SystemExit(0)
        tree = run(["git", "write-tree"], env=env)
        commit = run(["git", "commit-tree", tree, "-p", base], data=sys.argv[1] + "\n")
        try:
            result = run(["git", "push", "origin", commit + ":refs/heads/main"])
        except RuntimeError as exc:
            if "non-fast-forward" in str(exc) or "fetch first" in str(exc) or "failed to update ref" in str(exc):
                continue
            raise
        actual = run(["git", "ls-remote", "origin", "refs/heads/main"]).split()[0]
        receipt = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   "status": "pushed", "commit": commit, "parent": base,
                   "observed_remote_main": actual, "owned_changed_paths": changed,
                   "method": "isolated index, commit-tree parented on remote main, non-force push",
                   "local_main_preserved": True, "shared_index_untouched_by_this_script": True}
        break
if receipt is None:
    raise SystemExit("Remote main moved repeatedly; no force push attempted")
receipts = PROJECT / "research" / "git_publication_receipts.jsonl"
with receipts.open("a") as stream:
    stream.write(json.dumps(receipt, sort_keys=True) + "\n")
print(json.dumps(receipt, sort_keys=True))
