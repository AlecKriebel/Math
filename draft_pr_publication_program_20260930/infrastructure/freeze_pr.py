#!/usr/bin/env python3
"""Freeze the exact Git objects for one PR without changing the checkout.

The caller must fetch the PR head first. This records evidence only; it does
not accept a result, edit QUEUE.md, or regenerate any research state.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess


def run(*args):
    return subprocess.check_output(args)


def save_new_or_identical(path, data):
    if path.exists():
        if path.read_bytes() != data:
            raise RuntimeError("Refusing to replace frozen evidence: " + str(path))
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--problem", required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--audit-dir", required=True)
    args = parser.parse_args()
    if not args.problem.isdecimal():
        raise ValueError("Numeric upstream problem ID required")
    metadata_raw = run("gh", "pr", "view", str(args.pr), "--repo", "AlecKriebel/Math",
                       "--json", "number,url,title,body,state,isDraft,headRefOid,baseRefOid,files")
    metadata = json.loads(metadata_raw)
    head, base = metadata["headRefOid"], metadata["baseRefOid"]
    if head != args.expected_head or metadata["state"] != "OPEN":
        raise RuntimeError("PR head/state differs from the selected review input")
    run("git", "cat-file", "-e", head + "^{commit}")
    if run("git", "branch", "--show-current").decode().strip() != "main":
        raise RuntimeError("Review must remain on main")
    prefix = "unsolved_math_prioritization/attempts/" + args.problem + "/"
    queue_path = "unsolved_math_prioritization/QUEUE.md"
    changed = run("git", "diff", "--name-only", base + "..." + head).decode().splitlines()
    if set(changed) != {x["path"] for x in metadata["files"]}:
        raise RuntimeError("Git and GitHub changed-file inventories differ")
    unexpected = [p for p in changed if p != queue_path and not p.startswith(prefix)]
    if unexpected:
        raise RuntimeError("Unexpected changed paths: " + repr(unexpected))
    audit = pathlib.Path(args.audit_dir)
    snapshot = audit / "source_snapshot"
    files = []
    tree = run("git", "ls-tree", "-r", "-z", head, "--", prefix)
    for entry in tree.split(b"\0"):
        if not entry:
            continue
        info, raw_path = entry.split(b"\t", 1)
        mode, kind, oid = info.decode().split()
        path = raw_path.decode()
        if mode not in ("100644", "100755") or kind != "blob":
            raise RuntimeError("Non-regular snapshot entry: " + path)
        rel = pathlib.PurePosixPath(path[len(prefix):])
        if rel.is_absolute() or ".." in rel.parts:
            raise RuntimeError("Unsafe snapshot path")
        data = run("git", "cat-file", "blob", oid)
        save_new_or_identical(snapshot / rel, data)
        files.append({"path": str(rel), "mode": mode, "git_blob": oid,
                      "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})
    if not files:
        raise RuntimeError("No attempt artifacts")
    audit.mkdir(parents=True, exist_ok=True)
    save_new_or_identical(audit / "pr_input.json", metadata_raw.rstrip(b"\n") + b"\n")
    rows = {}
    for name, ref in (("pr_base", base), ("pr_head", head), ("main_at_start", "HEAD")):
        text = run("git", "show", ref + ":" + queue_path).decode()
        matches = [line for line in text.splitlines()
                   if line.startswith("|") and len(line.split("|")) > 2
                   and line.split("|")[2].strip().split(" / ")[0] == args.problem]
        if len(matches) != 1:
            raise RuntimeError("Target QUEUE row is missing or ambiguous at " + name)
        rows[name] = matches[0]
    manifest = {"created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "pr": args.pr, "problem": args.problem, "head": head, "base": base,
                "main_at_start": run("git", "rev-parse", "HEAD").decode().strip(),
                "queue_rows": rows, "changed_paths": changed, "files": files}
    manifest_path = audit / "snapshot_manifest.json"
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text())
        if previous["head"] != head or previous["files"] != files:
            raise RuntimeError("Frozen manifest differs")
    else:
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    (audit / ".gitignore").write_text("tmp/\n__pycache__/\n")
    print(json.dumps({"pr": args.pr, "head": head, "files": len(files),
                      "snapshot_hashes_pass": True, "queue_rows": rows}, indent=2))


if __name__ == "__main__":
    main()
