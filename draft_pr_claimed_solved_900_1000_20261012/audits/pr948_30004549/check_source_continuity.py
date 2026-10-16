#!/usr/bin/env python3
"""Read-only prepublication source gate for PR948's original submitted head.

No source/cache/status/author-turn mutation; only a new own receipt is saved.
A changed head requires a new controller identity/status intake, not reuse.
"""
import argparse
from pathlib import Path
import datetime
import hashlib
import json
import sqlite3
import stat
import subprocess

A = Path(__file__).resolve().parent
P = A.parent.parent
ROOT = P.parent
HEAD = "be4313efafa1af5962394e07d8a4debff2e94d92"
ID = "30004549"
STATEMENT = "a5ce90b9c2087f20cd09cb33d9d92ca40039c19a08de3b1c098d10bf75b9179b"
REVIEW = "b667ba93b244f20bf9dd6b244af355c1b933340bb194c5a18a0d7c27d5ed9bb4"
RECORD = "5df3868e802d9da72bced3f4606c3ccd9b6610208bcc2a086bf25e082239b34f"
ROW = "14e26d488e321d3047b1aa4b2b68b56c29321b4942333804634c58a2b4d4b489"


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def run(args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, check=True).stdout


def git(*args):
    return run(["git", "-c", "gc.auto=0", *args])


def metadata():
    return json.loads(run([
        "gh", "pr", "view", "948", "--repo", "AlecKriebel/Math", "--json",
        "number,state,isDraft,headRefOid,headRefName,baseRefName,url",
    ]))


def contains(v):
    if type(v) in (str, int):
        return str(v) == ID
    if type(v) is list:
        return any(contains(x) for x in v)
    if type(v) is dict:
        return any(str(k) == ID or contains(x) for k, x in v.items())
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--receipt-name", required=True)
    args = ap.parse_args()
    require(Path(args.receipt_name).name == args.receipt_name
            and args.receipt_name.endswith(".json"), "Noncanonical receipt")
    receipt = A / args.receipt_name
    require(not receipt.exists(), "Receipt already exists; never overwrite")
    before = metadata()
    require(before["state"] == "OPEN" and before["isDraft"] is True
            and before["headRefOid"] == HEAD and before["baseRefName"] == "main",
            "Head/state changed: fresh controller status-only intake required")
    rows = [l for l in git("show", HEAD + ":unsolved_math_prioritization/QUEUE.md")
            .decode().splitlines() if "| " + ID + " /" in l]
    require(len(rows) == 1, "Ambiguous target row")
    row = rows[0]
    cells = row.split("|")
    require(cells[8].strip() == "claimed_solved",
            "OUT_OF_SCOPE: stop before reading mathematical source")
    require(hashlib.sha256(row.encode()).hexdigest() == ROW
            and cells[9].strip() == "4/5", "Original queue row drift")

    parent = git("ls-remote", "origin", "refs/heads/main").decode().split()[0]
    git("fetch", "--no-write-fetch-head", "origin", parent)
    prefix = parent + ":unsolved_math_prioritization/"
    catalog = json.loads(git("show", prefix + "catalog.json"))
    selected = [t for t in catalog if str(t["id"]) == ID]
    require(len(selected) == 1, "Ambiguous numeric source ID")
    target = selected[0]
    require(target["present"] is True and target["holds"] == [], "Absent/held source")
    policy = json.loads(git("show", prefix + "policy.json"))
    require(type(policy["turn_limit"]) is int and policy["turn_limit"] == 5,
            "Five-turn policy drift")
    dbpath = ROOT / "unsolved_math_prioritization/cache/catalog.sqlite"
    require(stat.S_ISREG(dbpath.lstat().st_mode) and not dbpath.is_symlink(),
            "Nonregular source cache")
    with sqlite3.connect(dbpath.as_uri() + "?mode=ro", uri=True) as db:
        raw = db.execute("SELECT payload,report FROM records WHERE key=?", (ID,)).fetchone()
    require(raw is not None, "Raw source absent")
    problem, prior = map(json.loads, raw)
    review = hashlib.sha256(json.dumps([problem, prior], sort_keys=True).encode()).hexdigest()
    statement = hashlib.sha256(problem["statement"].encode()).hexdigest()
    require(review == target["review_hash"] == REVIEW
            and statement == target["statement_hash"] == STATEMENT,
            "Source drift: fresh individual review required")
    private_bytes = (A / "source_record_private.txt").read_bytes()
    require(len(private_bytes) == 4190
            and hashlib.sha256(private_bytes).hexdigest() == RECORD, "Private record drift")
    private = json.loads(private_bytes)
    require(private["problem"] == problem and private["prior_research"] == prior
            and private["review_hash"] == review, "Private/raw source mismatch")
    groupsraw = git("show", prefix + "review_v2/related_target_groups.json")
    require(not contains(json.loads(groupsraw)), "New related membership requires review")

    records = json.loads((A / "ORIGINAL_FILE_RECORDS.json").read_text())["files"]
    for path, pin in records.items():
        original = A / "original" / path
        require(stat.S_ISREG(original.lstat().st_mode) and not original.is_symlink(),
                "Nonregular original: " + path)
        data = original.read_bytes()
        tree = git("ls-tree", HEAD, "--", path).decode().split()
        require(len(data) == pin["bytes"]
                and hashlib.sha256(data).hexdigest() == pin["sha256"]
                and tree[:3] == [pin["git_mode"], "blob", pin["git_blob"]]
                and data == git("show", HEAD + ":" + path), "Original drift: " + path)
    after = metadata()
    require(after == before, "PR changed during source gate")
    result = {
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "PASS_CURRENT_EXACT_CLAIMED_SOLVED_IDENTITY_SOURCE_ORIGINAL_CONTINUITY",
        "before": before, "after": after, "remote_main": parent,
        "queue_status": "claimed_solved", "queue_row_sha256": ROW,
        "declared_author_turns": "4/5", "verified_original_files": len(records),
        "statement_sha256": statement, "review_hash": review,
        "private_record_sha256": RECORD,
        "raw_sqlite_source_reconstructed_and_matched": True,
        "source_present": True, "holds": [], "related_target_groups": {},
        "related_file_sha256": hashlib.sha256(groupsraw).hexdigest(),
        "turn_limit": 5, "new_author_proof_responses": 0,
        "native_history_status": "Unknown; no synthetic queue turns recorded",
        "source_or_catalog_or_original_mutated": False,
    }
    # Preserve the actual read-only observations in the tool transcript even
    # when intermittent ENOSPC prevents the subsequent own receipt write.
    print(json.dumps(result, indent=2), flush=True)
    receipt.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
