#!/usr/bin/env python3
"""Push explicit research files while preserving the shared checkout and index.

Only this program's subtree is indexed. All other root tree entries are copied
byte-for-byte from the observed remote parent. No local branch ref is changed.
This does not create a GitHub release or publish a Zenodo record.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

PROGRAM = Path(__file__).resolve().parent.parent
REPO = PROGRAM.parent


def run(arguments, *, env=None, data=None, check=True, cwd=REPO):
    completed = subprocess.run(["git", "-c", "gc.auto=0", *arguments],
                               cwd=cwd, env=env, input=data, capture_output=True)
    if check and completed.returncode:
        raise RuntimeError(completed.stderr.decode(errors="replace")[-4000:])
    return completed


def git_text(arguments, **kwargs):
    return run(arguments, **kwargs).stdout.decode().strip()


def digest(path):
    if not path.exists():
        return None
    result = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024*1024), b""):
            result.update(chunk)
    return result.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--message", required=True)
    args = parser.parse_args()
    assert not args.receipt.exists(), "Do not overwrite a previous push receipt"
    plan = json.loads(args.plan.read_text())
    prefix = PROGRAM.name+"/"
    paths = plan["paths"]
    assert paths and len(paths) == len(set(paths))
    relative = []
    for path in paths:
        assert path.startswith(prefix), path
        target = REPO / path
        assert target.resolve().is_relative_to(PROGRAM.resolve()), path
        assert target.is_file(), path
        assert target.name != "QUEUE.md", path
        relative.append(path[len(prefix):])
    assert git_text(["symbolic-ref", "HEAD"]) == "refs/heads/main"
    git_dir = Path(git_text(["rev-parse", "--absolute-git-dir"]))
    index = git_dir / "index"
    index_before = digest(index)
    head_before = git_text(["rev-parse", "HEAD"])
    branch_before = git_text(["symbolic-ref", "HEAD"])
    attempts = []
    receipt = None
    for attempt in range(1, 5):
        parent = git_text(["ls-remote", "origin", "refs/heads/main"]).split()[0]
        if run(["cat-file", "-e", parent+"^{commit}"], check=False).returncode:
            run(["fetch", "--no-auto-gc", "origin", "main"])
        descriptor, name = tempfile.mkstemp(prefix="kourovka-subtree-index-")
        os.close(descriptor)
        os.unlink(name)
        env = dict(os.environ, GIT_INDEX_FILE=name,
                   GIT_DIR=str(git_dir), GIT_WORK_TREE=str(PROGRAM))
        try:
            base_tree = parent+":"+PROGRAM.name
            run(["read-tree", base_tree], env=env, cwd=PROGRAM)
            run(["add", "--", *relative], env=env, cwd=PROGRAM)
            changed = run(["diff", "--cached", "--name-only", "-z", base_tree],
                          env=env, cwd=PROGRAM).stdout.split(b"\0")
            changed = [p.decode() for p in changed if p]
            assert set(changed).issubset(relative), changed
            assert changed, "No changed selected files; no duplicate checkpoint"
            subtree = git_text(["write-tree"], env=env, cwd=PROGRAM)
            entries = [p for p in run(["ls-tree", "-z", parent]).stdout.split(b"\0") if p]
            root_name = PROGRAM.name.encode()
            hits = [i for i, entry in enumerate(entries) if entry.split(b"\t", 1)[1] == root_name]
            assert len(hits) == 1
            position = hits[0]
            replacement = b"040000 tree "+subtree.encode()+b"\t"+root_name
            new_entries = entries[:]
            new_entries[position] = replacement
            assert all(a == b for i, (a, b) in enumerate(zip(entries, new_entries)) if i != position)
            tree = run(["mktree", "-z"], data=b"\0".join(new_entries)+b"\0").stdout.decode().strip()
            commit = git_text(["commit-tree", tree, "-p", parent],
                              data=(args.message+"\n").encode())
            pushed = run(["push", "origin", commit+":refs/heads/main"], check=False)
            observed = git_text(["ls-remote", "origin", "refs/heads/main"]).split()[0]
            if run(["cat-file", "-e", observed+"^{commit}"], check=False).returncode:
                run(["fetch", "--no-auto-gc", "origin", "main"])
            verified = run(["merge-base", "--is-ancestor", commit, observed], check=False).returncode == 0
            attempts.append({"attempt": attempt, "parent": parent, "commit": commit,
                             "push_exit_code": pushed.returncode, "observed_remote": observed,
                             "commit_is_remote_ancestor": verified})
            if verified:
                receipt = {"utc": datetime.now(timezone.utc).isoformat(),
                           "parent": parent, "commit": commit, "changed_files": len(changed),
                           "remote_verified": True, "observed_remote": observed,
                           "uses_alternate_subtree_index": True, "subtree": PROGRAM.name,
                           "other_root_tree_entries_byte_identical": True,
                           "original_index_unchanged": digest(index) == index_before,
                           "checkout_branch_before": branch_before,
                           "checkout_branch_after": git_text(["symbolic-ref", "HEAD"]),
                           "checkout_HEAD_before": head_before,
                           "checkout_HEAD_after": git_text(["rev-parse", "HEAD"]),
                           "publication_release_created": False, "attempts": attempts,
                           "selected_paths": paths}
                break
            if pushed.returncode == 0:
                raise RuntimeError("Push reported success but remote ancestry was not confirmed")
            if observed == parent:
                raise RuntimeError(pushed.stderr.decode(errors="replace")[-4000:])
        finally:
            for temporary in (Path(name), Path(name+".lock")):
                if temporary.exists():
                    temporary.unlink()
    assert receipt is not None, attempts
    with args.receipt.open("x") as handle:
        json.dump(receipt, handle, indent=2)
        handle.write("\n")
    print(json.dumps({k: receipt[k] for k in ("commit", "parent", "changed_files",
                                             "remote_verified", "original_index_unchanged",
                                             "publication_release_created")}))


if __name__ == "__main__":
    main()
