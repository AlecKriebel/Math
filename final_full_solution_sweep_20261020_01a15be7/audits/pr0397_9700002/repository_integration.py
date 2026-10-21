#!/usr/bin/env python3
"""Narrow existing-PR tree overlay and exact integration verification; no checkout."""
import argparse
import base64
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import quote

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
sys.path.insert(0, str(ROOT))
from checkpoint import verify_destination
from remote_checkpoint import api, tree_map, overlay_entry, blob_sha
from sweep_io import atomic_json
from publication_live_gates import collect, require_release_clearance

ORIGINAL = "3705c5102b58c48e29991c61771978bf756a62e7"
PROBLEM = "problems/9700002_congestion_transition"
QUEUE = "unsolved_math_prioritization/QUEUE.md"


def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def signature(entry):
    return entry["mode"], entry["type"], entry["sha"]


def subtree(commit, path, recursive=True):
    tree = api("git/commits/" + commit)["tree"]["sha"]
    for part in path.split("/") if path else []:
        entry = tree_map(tree).get(part)
        if entry is None:
            return {}
        if entry["type"] != "tree":
            raise RuntimeError("Expected directory: " + path)
        tree = entry["sha"]
    return tree_map(tree, recursive)


def leaves(commit, path):
    return {n: signature(v) for n, v in subtree(commit, path).items() if v["type"] != "tree"}


def blob(commit, path):
    parent, name = path.rsplit("/", 1)
    item = subtree(commit, parent, False).get(name)
    if item is None or item["type"] != "blob" or item["mode"] != "100644":
        raise RuntimeError("Absent or unexpected regular file: " + path)
    value = api("git/blobs/" + item["sha"])
    if value["encoding"] != "base64":
        raise RuntimeError("Unexpected Git blob encoding")
    data = base64.b64decode(value["content"])
    if blob_sha(data) != item["sha"]:
        raise RuntimeError("Git blob identity mismatch")
    return data


def selection():
    release = json.loads((AUDIT / "preprint/publication/RELEASE_FILES.json").read_text())
    result = {}
    for entry in release["files"]:
        data = (AUDIT / "preprint/publication" / entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise RuntimeError("Release bytes changed")
        result["preprint/" + entry["path"]] = data
    if len(result) != 5:
        raise RuntimeError("Unexpected publication inventory")
    return result


def originals():
    snapshot = json.loads((AUDIT / "SOURCE_SNAPSHOT.json").read_text())
    if snapshot["head"] != ORIGINAL or len(snapshot["files"]) != 24:
        raise RuntimeError("Unexpected original binding")
    return {v["repository_path"].removeprefix(PROBLEM + "/"):
            ("100644", "blob", v["git_blob"]) for v in snapshot["files"]}


def unchanged_parent(before, after, parent, exceptions):
    a = subtree(before, parent, False)
    b = subtree(after, parent, False)
    # Recursive trees contain intermediate directories whose SHAs necessarily change.
    # Compare each immediate child, excluding only the selected subtrees/files.
    a = {k: signature(v) for k, v in a.items() if "/" not in k and k not in exceptions}
    b = {k: signature(v) for k, v in b.items() if "/" not in k and k not in exceptions}
    if a != b:
        raise RuntimeError("Unselected entries changed under " + (parent or "repository root"))


def assert_scoped_preservation(before, after, queue_changed):
    exceptions = {"problems"}
    if queue_changed:
        exceptions.add("unsolved_math_prioritization")
    unchanged_parent(before, after, "", exceptions)
    unchanged_parent(before, after, "problems", {"9700002_congestion_transition"})
    if queue_changed:
        unchanged_parent(before, after, "unsolved_math_prioritization", {"QUEUE.md"})


def own_queue_row(data):
    rows = [line for line in data.splitlines(keepends=True)
            if b"| 9700002 / AMR-096-0002 |" in line]
    if len(rows) != 1:
        raise RuntimeError("Own QUEUE row missing or duplicated")
    return rows[0]


def verify_integrated_tree(base, integrated, expected_head):
    selected = selection()
    expected = leaves(base, PROBLEM)
    added = dict(originals())
    added.update({n: ("100644", "blob", blob_sha(b)) for n, b in selected.items()})
    for name, identity in added.items():
        if name in expected and expected[name] != identity:
            raise RuntimeError("Concurrent main changed candidate file: " + name)
    expected.update(added)
    if leaves(integrated, PROBLEM) != expected:
        raise RuntimeError("Merged candidate subtree differs outside exact original/publication selection")
    old_queue = blob(base, QUEUE)
    desired = own_queue_row(blob(expected_head, QUEUE))
    if b"| claimed_solved | 2/5 |" not in desired:
        raise RuntimeError("Reviewed head status changed")
    old = own_queue_row(old_queue)
    queued = desired.replace(b"| claimed_solved | 2/5 |", b"| queued | 0/5 |")
    if old not in {queued, desired}:
        raise RuntimeError("Concurrent own QUEUE status needs reconciliation")
    if blob(integrated, QUEUE) != old_queue.replace(old, desired, 1):
        raise RuntimeError("Merged QUEUE differs beyond own exact status/turn update")
    assert_scoped_preservation(base, integrated, True)
    return {"main": base, "integrated_commit": integrated, "head": expected_head,
            "original_files": 24, "publication_files": 5,
            "unrelated_entries_preserved": True, "queue_other_bytes_preserved": True,
            "tree": api("git/commits/" + integrated)["tree"]["sha"]}


def live_pr(expected_head):
    pr = api("pulls/397")
    if (pr["head"]["sha"] != expected_head or pr["base"]["ref"] != "main"
            or pr["head"]["repo"]["full_name"] != "AlecKriebel/Math"
            or pr["state"] != "open" or pr.get("merged")):
        raise RuntimeError("Live PR changed or is no longer an unmerged open candidate")
    return pr


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["plan", "commit", "verify-test-merge"])
    parser.add_argument("--expected-pr-head", required=True)
    args = parser.parse_args()
    verify_destination()
    pr = live_pr(args.expected_pr_head)
    selected = selection()
    if args.action in {"plan", "commit"}:
        if args.expected_pr_head != ORIGINAL:
            raise RuntimeError("Publication overlay starts only from the exact reviewed original head")
        existing = leaves(ORIGINAL, PROBLEM)
        for name, identity in originals().items():
            if existing.get(name) != identity:
                raise RuntimeError("Original proof changed")
        if any(n in existing for n in selected):
            raise RuntimeError("Publication paths already exist; reconcile instead of overwriting")
        receipt = {"timestamp": stamp(), "action": args.action, "pr": 397,
                   "original_head": ORIGINAL, "head_ref": pr["head"]["ref"],
                   "selected_paths": [PROBLEM + "/" + n for n in selected],
                   "original24_files_verified": True, "shared_checkout_modified": False}
        if args.action == "plan":
            atomic_json(AUDIT / "PUBLICATION_BRANCH_PLAN.json", receipt)
            print(json.dumps(receipt, indent=2))
            return
        require_release_clearance()
        gate, acceptance = collect("before_integration", ORIGINAL)
        original_tree = api("git/commits/" + ORIGINAL)["tree"]["sha"]
        entries = [overlay_entry(PROBLEM, name, data) for name, data in selected.items()]
        tree = api("git/trees", "POST", {"base_tree": original_tree, "tree": entries})
        commit = api("git/commits", "POST", {
            "message": "Add reviewed congestion-fragmentation research note and verification package",
            "tree": tree["sha"], "parents": [ORIGINAL]})
        new = commit["sha"]
        if [p["sha"] for p in commit["parents"]] != [ORIGINAL]:
            raise RuntimeError("Unexpected publication commit ancestry")
        assert_scoped_preservation(ORIGINAL, new, False)
        expected = dict(existing)
        expected.update({n: ("100644", "blob", blob_sha(b)) for n, b in selected.items()})
        if leaves(new, PROBLEM) != expected:
            raise RuntimeError("Commit changes unselected candidate files")
        live_pr(ORIGINAL)
        branch = "git/refs/heads/" + quote(pr["head"]["ref"], safe="/")
        intent = {**receipt, "commit": new, "tree": tree["sha"],
                  "gate_receipt": gate["receipt"], "non_forced": True}
        atomic_json(AUDIT / "PUBLICATION_BRANCH_PUSH_INTENT.json", intent)
        api(branch, "PATCH", {"sha": new, "force": False})
        if api("pulls/397")["head"]["sha"] != new:
            raise RuntimeError("Publication branch outcome needs reconciliation; do not repeat overlay")
        receipt = {**intent, "status": "pushed_and_verified", "verified_at": stamp(),
                   "all_unselected_entries_preserved": True}
        atomic_json(AUDIT / "PUBLICATION_BRANCH_COMMIT.json", receipt)
        print(json.dumps(receipt, indent=2))
        return
    require_release_clearance()
    main_sha = api("git/ref/heads/main")["object"]["sha"]
    if pr.get("mergeable") is not True or not pr.get("merge_commit_sha"):
        raise RuntimeError("No clean test merge available yet")
    merged = api("git/commits/" + pr["merge_commit_sha"])
    if [p["sha"] for p in merged["parents"]] != [main_sha, args.expected_pr_head]:
        raise RuntimeError("Test merge is stale relative to live main/head")
    receipt = verify_integrated_tree(main_sha, merged["sha"], args.expected_pr_head)
    if api("git/ref/heads/main")["object"]["sha"] != main_sha:
        raise RuntimeError("Main advanced during verification; repeat read-only verification")
    receipt.update(timestamp=stamp(), status="PASS_EXACT_CURRENT_MAIN_INTEGRATION", pr=397,
                   test_merge=merged["sha"], ready_for_exact_head_merge=True,
                   live_draft=pr["draft"], local_checkout_or_index_mutations=False)
    atomic_json(AUDIT / "MERGE_INTEGRATION_ACCEPTANCE.json", receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
