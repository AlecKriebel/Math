#!/usr/bin/env python3
"""Prepare only: explicit MAIN, private index/objects, no refs or network writes."""
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
CASE = ROOT.parents[1]
STORE = ROOT.parent / "objects.git"
DRIVER = ROOT / "driver.git"
AUTHOR = "c5252db6ec25ffdbfd2259bfdcf2fb6228e1846e"
AUTHOR_TREE = "a4a0630d53562387083fe4481d648e8489b4b1f7"
TARGET = "unsolved_math_prioritization/attempts/30005468"
QUEUE = "unsolved_math_prioritization/QUEUE.md"
ACCEPTANCE = CASE / "ROOT_PR278_AUTHOR_BRANCH_ACCEPTANCE_01.json"
PLAN = CASE / "ROOT_PR278_author_branch_readonly_01/PLAN.json"
READBACK = CASE / "ROOT_PR278_author_branch_readback_01/RESULT.json"
ORIGINAL = CASE / "original_submission_snapshot_01"
OVERLAY = CASE / "ROOT_native04_actual_conflict_consumption_01/ROOT_RECONSTRUCTED_62_OVERLAY.json"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def git_id(kind, data):
    return hashlib.sha1(kind.encode() + b" " + str(len(data)).encode() + b"\0" + data).hexdigest()


def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def read_pinned(record):
    path = Path(record["path"])
    need(pin(path) == record, "Accepted source pin changed: " + str(path))
    return json.loads(path.read_bytes())


def env_for(output):
    env = dict(os.environ)
    for key in list(env):
        if key.startswith("GIT_"):
            del env[key]
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null",
               GIT_NO_LAZY_FETCH="1", GIT_TERMINAL_PROMPT="0",
               GIT_INDEX_FILE=str(output / "private.index"),
               GIT_OBJECT_DIRECTORY=str(ROOT / "private_objects"),
               GIT_ALTERNATE_OBJECT_DIRECTORIES=str(STORE / "objects"))
    return env


def git(env, *args, data=None):
    return subprocess.run(["git", "--git-dir", str(DRIVER), *args], input=data,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=env, check=True, timeout=45).stdout


def entries(env, tree, recursive=False):
    args = ["ls-tree", "-z"]
    if recursive:
        args += ["-r", "-t"]
    args += [tree]
    out = {}
    for item in git(env, *args).split(b"\0"):
        if item:
            identity, path = item.split(b"\t", 1)
            mode, kind, sha = identity.decode().split()
            out[path.decode()] = {"mode": mode, "type": kind, "sha": sha}
    return out


def target_row(body):
    lines = body.splitlines(keepends=True)
    matches = []
    for i, line in enumerate(lines):
        columns = line.split(b"|")
        if len(columns) > 3 and columns[2].strip() == b"30005468 / OWR-12697710-015":
            matches.append(i)
    need(len(matches) == 1, "QUEUE must contain exactly one exact problem row")
    i = matches[0]
    return lines, i, lines[i]


def bind_author(env):
    acceptance = json.loads(ACCEPTANCE.read_bytes())
    need(acceptance["accepted"] is True and acceptance["actual_after_commit"] == AUTHOR
         and acceptance["actual_after_tree"] == AUTHOR_TREE, "Accepted author identity mismatch")
    plan = read_pinned(acceptance["plan"])
    readback = read_pinned(acceptance["actual_whole_readback_result"])
    need(readback["actual_commit"] == AUTHOR and readback["actual_tree"] == AUTHOR_TREE,
         "Accepted whole readback identity mismatch")
    need(plan["after_commit"] == AUTHOR and plan["after_tree"] == AUTHOR_TREE,
         "Accepted plan identity mismatch")
    need(git(env, "rev-parse", AUTHOR + "^{tree}").decode().strip() == AUTHOR_TREE,
         "Actual author Merkle root mismatch")
    author_all = entries(env, AUTHOR, recursive=True)
    target_all = {p: e for p, e in author_all.items() if p == TARGET or p.startswith(TARGET + "/")}
    leaves = {p: e for p, e in target_all.items() if e["type"] != "tree"}
    need(len(leaves) == 61 and all(e["mode"] == "100644" and e["type"] == "blob"
                                for e in leaves.values()), "Author61 exact census/modes differ")
    contents = {e["path"]: e["content"].encode() for e in plan["tree_payload"]["tree"]}
    need(len(contents) == 49 and len(contents.keys() & leaves.keys()) == 48,
         "Accepted selected target census differs")
    original_manifest = json.loads((ORIGINAL / "MANIFEST.json").read_bytes())
    original = {e["path"]: e for e in original_manifest}
    readback_blobs = {}
    readback_sources = []
    for file in sorted(READBACK.parent.glob("*_GET_RESPONSE.json")):
        record = json.loads(file.read_bytes())
        if record.get("encoding") == "base64" and "content" in record and "sha" in record:
            body = base64.b64decode(record["content"])
            need(git_id("blob", body) == record["sha"], "Readback body hash mismatch")
            readback_blobs[record["sha"]] = body
            readback_sources.append(pin(file))
    manifest = []
    for path, entry in sorted(leaves.items()):
        if path in contents:
            body = contents[path]
            need(readback_blobs.get(entry["sha"]) == body,
                 "Selected body missing/different in accepted readback: " + path)
            source = {"kind": "accepted_plan_and_GET_readback", "plan": str(PLAN)}
        else:
            need(path in original, "Unbound inherited author path: " + path)
            record = original[path]
            body_path = ORIGINAL / "files" / record["relative_path"]
            body = body_path.read_bytes()
            need(record["git_blob"] == entry["sha"] and record["mode"] == entry["mode"]
                 and record["bytes"] == len(body)
                 and record["sha256"] == hashlib.sha256(body).hexdigest(),
                 "Original inherited full body mismatch: " + path)
            source = {"kind": "accepted_preserved_original", "body": pin(body_path)}
        need(git_id("blob", body) == entry["sha"], "Author leaf does not bind full logical body: " + path)
        actual = git(env, "hash-object", "-w", "--stdin", data=body).decode().strip()
        need(actual == entry["sha"], "Private blob write differs")
        manifest.append(dict(path=path, **entry, bytes=len(body),
                             sha256=hashlib.sha256(body).hexdigest(), source=source))
    overlay = json.loads(OVERLAY.read_bytes())
    old_full = {e["path"]: e for e in overlay["selected"] if e["path"].startswith(TARGET + "/")}
    need(set(old_full) == set(leaves), "Historical full61 manifest census differs")
    for e in manifest:
        need((e["sha"], e["bytes"], e["sha256"]) ==
             (old_full[e["path"]]["git_blob"], old_full[e["path"]]["bytes"], old_full[e["path"]]["sha256"]),
             "Historical61 logical manifest differs: " + e["path"])
    author_queue = contents[QUEUE]
    need(git_id("blob", author_queue) == author_all[QUEUE]["sha"]
         and readback_blobs.get(author_all[QUEUE]["sha"]) == author_queue,
         "Whole accepted author QUEUE Merkle/readback binding differs")
    git(env, "hash-object", "-w", "--stdin", data=author_queue)
    _, _, accepted_row = target_row(author_queue)
    need(accepted_row == plan["queue_delta"]["after"].encode(), "Accepted row mismatch")
    baseline_row = base64.b64decode(overlay["queue_delta"]["baseline_base64"])
    return target_all, manifest, accepted_row, baseline_row, {
        "acceptance": pin(ACCEPTANCE), "accepted_plan": pin(PLAN),
        "accepted_readback_result": pin(READBACK), "original_manifest": pin(ORIGINAL / "MANIFEST.json"),
        "historical_full61_manifest": pin(OVERLAY), "selected_blob_GET_sources": readback_sources,
        "selected_target_count": 48, "inherited_original_count": 13,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--main", required=True, help="Explicit immutable fresh MAIN SHA; no default")
    parser.add_argument("--date", required=True, help="Explicit UTC commit time YYYY-MM-DDTHH:MM:SSZ")
    parser.add_argument("--output", required=True, help="New directory under this reconciliation folder")
    parser.add_argument("--queue-body", help="Optional full body for the exact MAIN QUEUE blob if missing privately")
    args = parser.parse_args()
    need(re.fullmatch(r"[0-9a-f]{40}", args.main), "MAIN must be full immutable40-hex SHA")
    timestamp = dt.datetime.strptime(args.date, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    need(timestamp <= dt.datetime.now(dt.timezone.utc), "Do not draft future-dated commit")
    output = Path(args.output).resolve()
    need(output.parent == ROOT and not output.exists(), "Output must be a new direct child of reconciliation")
    output.mkdir()
    (ROOT / "private_objects").mkdir(exist_ok=True)
    env = env_for(output)
    if not DRIVER.exists():
        subprocess.run(["git", "init", "--bare", "--initial-branch=main", str(DRIVER)],
                       env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=45)
    before_root = git(env, "rev-parse", args.main + "^{tree}").decode().strip()
    main_all = entries(env, args.main, recursive=True)
    author_all, bound61, accepted_row, baseline_row, sources = bind_author(env)
    main_target = {p: e for p, e in main_all.items() if p == TARGET or p.startswith(TARGET + "/")}
    conflicts = []
    if main_target and main_target.get(TARGET) != author_all[TARGET]:
        conflicts.append({"path": TARGET, "reason": "existing target subtree differs; partial integration or independent deletion cannot be overwritten",
                          "MAIN": main_target.get(TARGET), "accepted_author": author_all[TARGET]})
    for path, entry in main_target.items():
        if path not in author_all:
            conflicts.append({"path": path, "reason": "independent unexpected target path", "MAIN": entry})
        elif entry["type"] != "tree" and entry != author_all[path]:
            conflicts.append({"path": path, "reason": "independently changed target leaf/mode", "MAIN": entry,
                              "accepted_author": author_all[path]})
        elif entry["type"] == "tree" and author_all[path]["type"] != "tree":
            conflicts.append({"path": path, "reason": "independently changed target type", "MAIN": entry})
    for ancestor in ["unsolved_math_prioritization", "unsolved_math_prioritization/attempts"]:
        if ancestor in main_all and main_all[ancestor]["type"] != "tree":
            conflicts.append({"path": ancestor, "reason": "target ancestor is not a tree", "MAIN": main_all[ancestor]})
    need(QUEUE in main_all and main_all[QUEUE]["type"] == "blob"
         and main_all[QUEUE]["mode"] in ("100644", "100755"), "MAIN QUEUE must be a regular blob")
    queue_entry = main_all[QUEUE]
    if args.queue_body:
        queue = Path(args.queue_body).read_bytes()
        need(git_id("blob", queue) == queue_entry["sha"], "Supplied QUEUE is not explicit MAIN's full blob")
        git(env, "hash-object", "-w", "--stdin", data=queue)
    else:
        queue = git(env, "cat-file", "blob", queue_entry["sha"])
    lines, row_index, current_row = target_row(queue)
    if current_row not in (baseline_row, accepted_row):
        conflicts.append({"path": QUEUE, "reason": "independently changed exact target row",
                          "MAIN_row": current_row.decode(), "baseline_row": baseline_row.decode(),
                          "accepted_row": accepted_row.decode()})
    if conflicts:
        result = dict(schema="pr278-scoped-reconciliation-conflict-v1", main=args.main,
                      author=AUTHOR, conflicts=conflicts, prepared=False, provider_mutations=0)
        (output / "CONFLICTS.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        return 2
    lines[row_index] = accepted_row
    composed_queue = b"".join(lines)
    queue_sha = git(env, "hash-object", "-w", "--stdin", data=composed_queue).decode().strip()
    main_leaves = {p: e for p, e in main_all.items() if e["type"] != "tree"}
    nonempty_directories = set()
    for path in main_leaves:
        components = path.split("/")
        nonempty_directories.update("/".join(components[:i]) for i in range(1, len(components)))
    for path, entry in main_all.items():
        if entry["type"] == "tree":
            need(path in nonempty_directories,
                 "MAIN contains an empty tree; index route cannot preserve it: " + path)
    git(env, "read-tree", "--empty")
    inventory = b"".join((e["mode"] + " " + e["sha"] + "\t" + p).encode() + b"\0"
                         for p, e in sorted(main_leaves.items()))
    git(env, "update-index", "--info-only", "-z", "--index-info", data=inventory)
    updates = b"".join((e["mode"] + " " + e["sha"] + "\t" + e["path"]).encode() + b"\0" for e in bound61)
    updates += (queue_entry["mode"] + " " + queue_sha + "\t" + QUEUE).encode() + b"\0"
    git(env, "update-index", "-z", "--index-info", data=updates)
    tree = git(env, "write-tree", "--missing-ok").decode().strip()
    identity = "Alec Kriebel <me@aleckriebel.com> " + str(int(timestamp.timestamp())) + " +0000"
    message = "Reconcile PR278 accepted research with current MAIN\n"
    commit_raw = ("tree " + tree + "\nparent " + AUTHOR + "\nparent " + args.main +
                  "\nauthor " + identity + "\ncommitter " + identity + "\n\n" + message).encode()
    commit = git(env, "hash-object", "-t", "commit", "-w", "--stdin", data=commit_raw).decode().strip()
    tree_payload = {"base_tree": before_root, "tree": [
        {"path": TARGET, "mode": "040000", "type": "tree", "sha": author_all[TARGET]["sha"]},
        {"path": QUEUE, "mode": queue_entry["mode"], "type": "blob", "content": composed_queue.decode()}]}
    commit_payload = {"tree": tree, "parents": [AUTHOR, args.main], "message": message,
                      "author": {"name": "Alec Kriebel", "email": "me@aleckriebel.com", "date": args.date},
                      "committer": {"name": "Alec Kriebel", "email": "me@aleckriebel.com", "date": args.date}}
    repository = json.loads((READBACK.parent / "0002_GET_RESPONSE.json").read_bytes())
    need(repository["full_name"] == "AlecKriebel/Math", "Historical repository identity differs")
    cas_payload = {"query": "mutation PR278ScopedCAS($input:UpdateRefsInput!){updateRefs(input:$input){clientMutationId}}",
                   "variables": {"input": {"repositoryId": repository["node_id"],
                                             "clientMutationId": "pr278-scoped-" + commit,
                                             "refUpdates": [{"name": "refs/heads/dot/math-30005468",
                                                             "beforeOid": AUTHOR, "afterOid": commit,
                                                             "force": False}]}}}
    proposal = dict(schema="pr278-scoped-reconciliation-proposal-v1", preparation_only=True,
                    execution_authority=False, provider_mutations=0, primary_git_mutations=0,
                    main=args.main, before_tree=before_root, author=AUTHOR, accepted_author_tree=AUTHOR_TREE,
                    candidate_tree=tree, candidate_commit=commit, ordered_parents=[AUTHOR, args.main],
                    date=args.date, target_subtree=author_all[TARGET]["sha"], preserved_author_files=61,
                    queue_mode=queue_entry["mode"], queue_before_blob=queue_entry["sha"], queue_after_blob=queue_sha,
                    queue_before_row=current_row.decode(), queue_accepted_row=accepted_row.decode(),
                    queue_row_number=row_index + 1, identical_existing_target_leaves=sum(
                        e["type"] != "tree" for e in main_target.values()), conflicts=[], source_pins=sources,
                    builder_source=pin(Path(__file__).resolve()),
                    remaining_gap="Coordinated fresh MAIN window; rebuild and independently verify; provider tree/commit readback; author CAS at c525; current-MAIN recheck before later merge. GitHub has no atomic cross-ref MAIN+author CAS here.")
    for name, value in [("PROPOSAL.json", proposal), ("BOUND_AUTHOR61.json", bound61),
                        ("TREE_PAYLOAD.json", tree_payload), ("COMMIT_PAYLOAD.json", commit_payload),
                        ("CAS_PAYLOAD.json", cas_payload)]:
        (output / name).write_text(json.dumps(value, indent=2) + "\n")
    (output / "commit.raw").write_bytes(commit_raw)
    print(json.dumps({k: proposal[k] for k in ["main", "candidate_tree", "candidate_commit", "preserved_author_files", "conflicts", "remaining_gap"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
