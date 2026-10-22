#!/usr/bin/env python3
"""Read only PR metadata and the exact target row of QUEUE.md; no PR content audit."""
import base64
import concurrent.futures
import datetime
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QUEUE = "unsolved_math_prioritization/QUEUE.md"


def api(path, ref=None):
    args = ["gh", "api", "-X", "GET", path]
    if ref:
        args.extend(["-f", "ref=" + ref])
    result = subprocess.run(args, text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def queue_at(ref):
    item = api("repos/AlecKriebel/Math/contents/" + QUEUE, ref)
    data = base64.b64decode(item["content"])
    return item["sha"], hashlib.sha256(data).hexdigest(), data.decode()


def target_rows(text, target_id):
    result = []
    for line in text.splitlines():
        cells = [v.strip() for v in line.split("|")]
        if len(cells) >= 10 and re.fullmatch(re.escape(target_id) + r"\s*/.*", cells[2]):
            result.append({"id": target_id, "rank": cells[1], "code": cells[2],
                           "status": cells[8], "turns": cells[9], "raw_row": line})
    if len(result) != 1:
        raise ValueError(f"Expected exactly one queue row for {target_id}, got {len(result)}")
    return result[0]


def main():
    metadata = json.loads((ROOT / "pr_metadata_initial.json").read_text())
    prs = list(metadata["data"]["repository"].values())
    main_commit = api("repos/AlecKriebel/Math/commits/main")["sha"]
    main_blob, main_digest, main_queue = queue_at(main_commit)
    queue_ids = set()
    for line in main_queue.splitlines():
        cells = [v.strip() for v in line.split("|")]
        if len(cells) > 9:
            match = re.fullmatch(r"(\d+)\s*/.*", cells[2])
            if match:
                queue_ids.add(match[1])
    out = ROOT / "eligibility"
    out.mkdir(exist_ok=True)

    def inspect(pr):
        # Titles and branch names are identity metadata, not proof evidence.
        candidates = set(re.findall(r"(?<!\d)\d{3,}(?!\d)", pr["title"])) & queue_ids
        if not candidates:
            candidates = set(re.findall(r"(?<!\d)\d{3,}(?!\d)", pr["headRefName"])) & queue_ids
        if not candidates:
            raise ValueError(f"Missing target identity for PR {pr['number']}")
        blob, digest, queue = queue_at(pr["headRefOid"])
        targets = sorted(candidates, key=int)
        head_rows = [target_rows(queue, target) for target in targets]
        main_rows = [target_rows(main_queue, target) for target in targets]
        decision = "eligible" if any(row["status"] == "claimed_solved" for row in head_rows) else "skip"
        receipt = {"checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   "pr": pr, "problem_ids": targets,
                   "head_queue_blob": blob, "head_queue_sha256": digest,
                   "head_queue_rows": head_rows, "remote_main_commit": main_commit,
                   "main_queue_blob": main_blob, "main_queue_sha256": main_digest,
                   "main_queue_rows": main_rows, "head_status_decision": decision,
                   "reviewed_math": False, "external_mutations": []}
        (out / f"pr{pr['number']}.json").write_text(json.dumps(receipt, indent=2) + "\n")
        print(f"PR #{pr['number']}: head={[v['status'] for v in head_rows]}, main={[v['status'] for v in main_rows]} -> {decision}", flush=True)
        return receipt

    receipts = []
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        pending = {pool.submit(inspect, pr): pr["number"] for pr in prs}
        for future in concurrent.futures.as_completed(pending):
            try:
                receipts.append(future.result())
            except Exception as error:
                errors.append({"pr": pending[future], "error": str(error)})
    receipts.sort(key=lambda v: v["pr"]["number"])
    summary = {"generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "scope": {"first": 1200, "last": 1300, "direction": "ascending",
                         "required_status": "claimed_solved", "draft_only": True},
               "remote_main_commit": main_commit, "main_queue_blob": main_blob,
               "head_target_status_counts": dict(Counter(row["status"] for r in receipts for row in r["head_queue_rows"])),
               "main_target_status_counts": dict(Counter(row["status"] for r in receipts for row in r["main_queue_rows"])),
               "head_eligible": [r["pr"]["number"] for r in receipts if any(row["status"] == "claimed_solved" for row in r["head_queue_rows"])],
               "main_eligible": [r["pr"]["number"] for r in receipts if any(row["status"] == "claimed_solved" for row in r["main_queue_rows"])],
               "checked_prs": [r["pr"]["number"] for r in receipts], "errors": errors}
    (ROOT / "ELIGIBILITY_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
