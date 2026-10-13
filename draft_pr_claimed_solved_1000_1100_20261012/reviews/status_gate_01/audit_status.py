"""Independent, read-only audit of status and identity; no proof/body review."""
import base64
import collections
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
PROGRAM = HERE.parents[1]
REPO = "AlecKriebel/Math"

def api(endpoint, jq=None):
    args = ["gh", "api", endpoint]
    if jq:
        args += ["--jq", jq]
    return subprocess.check_output(args, text=True)

def row(text, pid):
    matches = []
    for lineno, line in enumerate(text.splitlines(), 1):
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 10 or not re.fullmatch(r"\d+", cells[1]):
            continue
        if cells[2].split(" / ")[0] != str(pid):
            continue
        # Independent fixed-schema parser. Reject shifted columns rather than
        # silently matching a status-like passage in Problem or Findings.
        if not re.fullmatch(r"[a-z][a-z0-9_]*", cells[8]):
            raise ValueError(f"Noncanonical Status column for ID {pid}")
        if not re.fullmatch(r"(?:\d+/\d+|—|-)", cells[9]):
            raise ValueError(f"Noncanonical Turns column for ID {pid}")
        matches.append({"problem_id": str(pid), "status": cells[8],
                        "turns": cells[9], "line": lineno})
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one row for ID {pid}; got {len(matches)}")
    return matches[0]

def check(pr):
    pid, n, sha = pr["problem_id"], pr["number"], pr["headRefOid"]
    endpoint = f"repos/{REPO}/contents/unsolved_math_prioritization/QUEUE.md?ref={sha}"
    obj = json.loads(api(endpoint, "{sha,content,encoding}"))
    if obj["encoding"] != "base64":
        raise ValueError(f"Unsupported encoding for PR {n}")
    content = base64.b64decode(obj["content"])
    status = row(content.decode(), pid)
    # File names identify attempt directories. No patch content is exposed.
    paths = subprocess.check_output(["gh", "api", "--paginate",
        f"repos/{REPO}/pulls/{n}/files?per_page=100", "--jq", ".[ ].filename".replace("[ ]", "[]")], text=True).splitlines()
    path_ids = sorted({m.group(1) for path in paths
        if (m := re.match(r"^unsolved_math_prioritization/attempts/(\d+)/", path))})
    return {"pr": n, "expected_problem_id": pid, "head_commit": sha,
            "head_queue_blob": obj["sha"],
            "head_queue_sha256": hashlib.sha256(content).hexdigest(),
            "head_queue_row": status, "intake_main_status": pr["queue_status"],
            "status_agrees_with_main": status["status"] == pr["queue_status"],
            "attempt_directory_ids": path_ids,
            "identity_supported_by_file_paths": pid in path_ids,
            "identity_unique_by_file_paths": path_ids == [pid]}

def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    inv = json.loads((PROGRAM / "inventory.json").read_text())
    main_queue = (PROGRAM / "queue_remote_main.md").read_bytes()
    if hashlib.sha256(main_queue).hexdigest() != inv["queue_sha256"]:
        raise ValueError("Pinned main queue digest mismatch")
    prs = inv["prs"]
    if [p["number"] for p in prs] != list(range(1000, 1101)):
        raise ValueError("Inventory has missing, duplicated, or unordered PR numbers")
    fixed_checks = [{"pr": p["number"], "row": row(main_queue.decode(), p["problem_id"]),
        "matches_intake": row(main_queue.decode(), p["problem_id"])["status"] == p["queue_status"]}
        for p in prs]
    (HERE / "independent_main_rows.json").write_text(json.dumps(fixed_checks, indent=2) + "\n")
    results, errors = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(check, p): p["number"] for p in prs}
        for i, f in enumerate(concurrent.futures.as_completed(futures), 1):
            try:
                results.append(f.result())
            except Exception as exc:
                errors.append({"pr": futures[f], "error": str(exc)})
            if i % 20 == 0:
                print(json.dumps({"checked": i, "total": len(prs), "errors": len(errors)}), flush=True)
    results.sort(key=lambda p:p["pr"])
    doc = {"started_utc": started, "completed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope": "Status and identity only; no mathematical material or PR body review",
        "queue_main_commit": inv["queue_main_commit"], "results": results, "errors": errors,
        "summary": {"head_status_counts": dict(collections.Counter(p["head_queue_row"]["status"] for p in results)),
        "distinct_head_queue_blobs": len({p["head_queue_blob"] for p in results}),
        "main_parser_mismatches": [p["pr"] for p in fixed_checks if not p["matches_intake"]],
        "head_main_status_mismatches": [p["pr"] for p in results if not p["status_agrees_with_main"]],
        "file_path_identity_unsupported": [p["pr"] for p in results if not p["identity_supported_by_file_paths"]],
        "file_path_identity_nonunique": [p["pr"] for p in results if not p["identity_unique_by_file_paths"]]}}
    (HERE / "pinned_head_status_checks.json").write_text(json.dumps(doc, indent=2) + "\n")
    print(json.dumps({"errors": errors, "summary":doc["summary"]}, indent=2))

if __name__ == "__main__":
    main()
