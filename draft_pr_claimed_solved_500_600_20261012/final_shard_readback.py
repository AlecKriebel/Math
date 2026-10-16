#!/usr/bin/env python3
"""Final read-only lifecycle/integrity check of this shard's seven eligible PRs."""
from pathlib import Path
import subprocess
import json
import hashlib
import datetime
import re
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def run(args):
    return subprocess.run(args, cwd=REPO, capture_output=True, text=True, check=True).stdout


def main():
    state = json.loads((ROOT / "STATE.json").read_text())
    completed = list(state["completed"])
    if not any(c["pr"] == 585 for c in completed):
        completed.append({"pr": 585, "problem_id": 30001232, "doi": "10.5281/zenodo.23387814",
                          "status": "published_and_merged"})
    audit = ROOT / "audits/pr585_30001232"
    receipts = audit / "receipts"
    run(["git", "-c", "gc.auto=0", "fetch", "origin", "main"])
    main_ref = run(["git", "rev-parse", "origin/main"]).strip()
    queue = run(["git", "show", f"{main_ref}:unsolved_math_prioritization/QUEUE.md"])
    header = None
    rows = {}
    for line in queue.splitlines():
        cells = [c.strip() for c in line.split("|")][1:-1]
        if cells and cells[0] == "Rank":
            header = {v: i for i, v in enumerate(cells)}
        if header and len(cells) > header["Status"]:
            for c in completed:
                if re.search(r"(?<!\d)" + str(c["problem_id"]) + r"(?!\d)", cells[header["ID / code"]]):
                    rows[c["pr"]] = {h: cells[i] for h, i in header.items()}
    checks = []
    for c in completed:
        row = rows[c["pr"]]
        expected = "already_solved" if c["pr"] == 523 else "preprint_published"
        if row["Status"] != expected or (c["pr"] != 523 and c["doi"] not in row["DOI"]):
            raise RuntimeError("Unexpected final queue row: " + str(c["pr"]))
        checks.append({"pr": c["pr"], "problem_id": c["problem_id"], "status": row["Status"],
                       "doi": row["DOI"], "turns": row["Turns"]})
    counts = {}
    for c in completed:
        if c["pr"] == 523:
            continue
        folder = ROOT / "audits" / ("pr" + str(c["pr"]) + "_" + str(c["problem_id"]))
        snapshot = json.loads((folder / "ORIGINAL_SNAPSHOT.json").read_text())
        for record in snapshot["files"]:
            data = subprocess.run(["git", "show", f"{main_ref}:{record['path']}"], cwd=REPO,
                                  capture_output=True, check=True).stdout
            # PR521's original acquisition uses bytes; later acquisitions use size.
            size = record["size"] if "size" in record else record["bytes"]
            if len(data) != size or hashlib.sha256(data).hexdigest() != record["sha256"]:
                raise RuntimeError("Changed preserved input: " + record["path"])
        counts[str(c["pr"])] = len(snapshot["files"])
    guide = run(["git", "show", f"{main_ref}:unsolved_math_prioritization/attempts/30001232/ACCEPTED_PUBLICATION.md"])
    if guide != (receipts / "ACCEPTED_PUBLICATION.md").read_text():
        raise RuntimeError("Current acceptance guide differs")

    def prcheck(c):
        metadata = json.loads(run(["gh", "pr", "view", str(c["pr"]), "--repo", "AlecKriebel/Math",
                                   "--json", "number,state,headRefOid,mergeCommit,mergedAt,url"]))
        if metadata["state"] != ("CLOSED" if c["pr"] == 523 else "MERGED"):
            raise RuntimeError("Unexpected PR lifecycle: " + str(c["pr"]))
        return metadata

    with ThreadPoolExecutor(max_workers=4) as pool:
        prs = list(pool.map(prcheck, completed))
    sheet = "1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20"
    data = json.loads(run(["gws", "sheets", "spreadsheets", "values", "get", "--params",
                           json.dumps({"spreadsheetId": sheet, "range": "'Math Puzzles'!A1:D1000"})]))
    if data["values"][0] != ["Original Problem", "Solution Chat URL", "DOI", "Notes"]:
        raise RuntimeError("Unexpected tracker headers")
    tracker = []
    for c in completed:
        if c["pr"] == 523:
            continue
        matches = [(i + 1, row) for i, row in enumerate(data["values"])
                   if len(row) > 2 and row[2] == "https://doi.org/" + c["doi"]]
        if len(matches) != 1 or str(c["problem_id"]) not in matches[0][1][0]:
            raise RuntimeError("Missing or duplicate own tracker DOI: " + str(c["pr"]))
        i, _ = matches[0]
        tracker.append({"pr": c["pr"], "range": f"'Math Puzzles'!A{i}:D{i}",
                        "doi": c["doi"], "unique_and_correct_problem": True})
    scan = "eligibility/recheck_500_600_20261015T073632Z.json"
    if json.loads((ROOT / scan).read_text())["eligible_prs"]:
        raise RuntimeError("Eligible draft remains")
    receipt = {"checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "status": "PASS", "observed_main": main_ref, "own_seven_queue_rows": checks,
               "unchanged_original_counts": counts, "all_preserved_original_inputs": sum(counts.values()),
               "all_seven_PR_lifecycles": prs, "six_unique_correct_tracker_rows": tracker,
               "current_585_guide_exact": True, "remaining_eligible_status_only_inventory": scan,
               "no_remaining_eligible_drafts": True}
    for target in [receipts / "FINAL_REMOTE_READBACK.json", ROOT / "FINAL_SHARD_AUDIT.json"]:
        target.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "seven_queue_rows": len(checks),
                      "preserved_original_inputs": sum(counts.values()),
                      "six_unique_tracker_rows": len(tracker), "guide_exact": True,
                      "remaining_eligible": 0, "observed_main": main_ref}))


if __name__ == "__main__":
    main()
