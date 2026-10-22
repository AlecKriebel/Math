#!/usr/bin/env python3
"""PR397 read-only live deduplication and custody receipt. Never publishes."""
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import uuid
from urllib.parse import urlencode

AUDIT = Path(__file__).resolve().parent
EFFORT = AUDIT.parents[1]
REPO = EFFORT.parent
sys.path.insert(0, str(EFFORT))
sys.path.insert(0, str(REPO / "zenodo_deposit_tool"))
from sweep_io import atomic_json
from checkpoint import verify_destination
import zenodo


def read_command(arguments):
    result = subprocess.run(arguments, cwd=REPO, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr[:1200])
    return json.loads(result.stdout)


def account_search(client, query):
    url = client.base + "/api/user/records?" + urlencode({"q": query, "size": 25})
    found = {}
    seen_urls = set()
    total = None
    pages = 0
    while url:
        if url in seen_urls:
            raise RuntimeError("Account-search pagination loop")
        seen_urls.add(url)
        result = client.request("GET", url)
        hits = result.get("hits", {})
        count = hits.get("total")
        if isinstance(count, dict):
            if count.get("relation") != "eq":
                raise RuntimeError("Account search has an inexact total")
            count = count.get("value")
        if type(count) is not int or count < 0 or (total is not None and total != count):
            raise RuntimeError("Account total missing or changed during pagination")
        total = count
        for item in hits.get("hits", []):
            identifier = int(item["id"])
            if identifier in found:
                raise RuntimeError("Repeated account record across pages")
            found[identifier] = item
        pages += 1
        url = result.get("links", {}).get("next")
    if len(found) != total:
        raise RuntimeError("Incomplete account search")
    return {"query": query, "total": total, "pages": pages,
            "records": list(found.values())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, choices=["before_integration", "before_stage", "before_publish", "before_ledger"])
    parser.add_argument("--expected-pr-head", required=True)
    parser.add_argument("--expected-deposit-id", type=int)
    args = parser.parse_args()
    if not re.fullmatch("[0-9a-f]{40}", args.expected_pr_head):
        raise RuntimeError("Expected PR head must be an exact commit SHA")
    verify_destination()
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    operation = uuid.uuid4().hex
    raw = EFFORT / "raw" / "pr0397" / ("prepublication_" + operation)
    raw.mkdir()
    sheet = read_command(["gws", "sheets", "spreadsheets", "values", "get", "--params",
                          json.dumps({"spreadsheetId": "1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20",
                                      "range": "'Math Puzzles'!A:AQ", "valueRenderOption": "FORMATTED_VALUE"})])
    atomic_json(raw / "ledger.json", sheet)
    rows = sheet.get("values", [])
    if not rows or rows[0] != ["Original Problem", "Solution Chat URL", "DOI", "Notes"]:
        raise RuntimeError("Ledger schema changed")
    baseline = json.loads((EFFORT / "raw/pr0397/ledger_live.json").read_text())["response"].get("values", [])
    changed_rows = [index + 1 for index in range(max(len(rows), len(baseline)))
                    if (rows[index] if index < len(rows) else None)
                    != (baseline[index] if index < len(baseline) else None)]
    pattern = re.compile(r"9700002|AMR[- ]096[- ]0002|/pull/397(?!\d)|\bPR\s*#?397(?!\d)|congestion|percolation.fragmentation|spare.capacity|cross.root|Aldous", re.I)
    matches = []
    for number, row in enumerate(rows, 1):
        joined = " ".join(str(value) for value in row)
        reasons = []
        if pattern.search(joined):
            reasons.append("problem/protocol/result/PR lead")
        if args.expected_deposit_id and re.search(r"zenodo[./]" + str(args.expected_deposit_id) + r"(?!\d)", joined):
            reasons.append("expected DOI or record lead")
        if reasons:
            matches.append({"row": number, "values": row, "reasons": reasons})
    client = zenodo.ZenodoClient("production", zenodo.token_for("production"))
    positive = account_search(client, "Fibonacci")
    if 23174283 not in {int(item["id"]) for item in positive["records"]}:
        raise RuntimeError("Authenticated account query failed known-record positive control")
    search = account_search(client, '"congestion" OR "9700002" OR "AMR-096-0002" OR "Aldous" OR "spare capacity"')
    complete_account = account_search(client, "")
    atomic_json(raw / "account_positive_control.json", positive)
    atomic_json(raw / "account_target.json", search)
    atomic_json(raw / "account_complete.json", complete_account)
    target_pattern = re.compile(r"9700002|AMR.?096.?0002|congestion|percolation.fragmentation|spare.capacity|designed.tree|Aldous", re.I)
    _, local_uploads = zenodo.load_manifest(AUDIT / "preprint/publication/zenodo-deposit.json")
    upload_md5 = {entry["md5"] for entry in local_uploads}
    local_targets = []
    for item in complete_account["records"]:
        files = item.get("files", [])
        if not isinstance(files, list):
            raise RuntimeError("Unexpected account file schema; reconcile before publishing")
        file_match = any(target_pattern.search(str(entry.get("key", entry.get("filename", ""))))
                         or str(entry.get("checksum", "")).lower().removeprefix("md5:") in upload_md5
                         for entry in files)
        if target_pattern.search(json.dumps(item.get("metadata", {}))) or file_match:
            local_targets.append(item)
    # A prepared draft was observed in the complete listing while keyword
    # search omitted it. Never use keyword search alone as draft coverage.
    targets = {int(item["id"]): item for item in search["records"] + local_targets}
    unexpected = [item for identifier, item in targets.items() if identifier != args.expected_deposit_id]
    if args.expected_deposit_id is not None and args.expected_deposit_id not in {int(item["id"]) for item in local_targets}:
        raise RuntimeError("Expected deposit missing from complete account/model/file comparison")
    pr = read_command(["gh", "api", "--hostname", "github.com", "repos/AlecKriebel/Math/pulls/397"])
    main_ref = read_command(["gh", "api", "--hostname", "github.com", "repos/AlecKriebel/Math/git/ref/heads/main"])
    atomic_json(raw / "pr.json", pr)
    if pr["head"]["sha"] != args.expected_pr_head or pr["base"]["ref"] != "main" or pr["head"]["repo"]["full_name"] != "AlecKriebel/Math":
        raise RuntimeError("Live PR destination/head changed")
    if pr["state"] != "open" and not pr.get("merged"):
        raise RuntimeError("PR closed without merge; reconcile before proceeding")
    state_matches = []
    for path in (REPO / ".zenodo-state").glob("*.json"):
        value = json.loads(path.read_text())
        if re.search(r"9700002|pr0397|congestion|percolation.fragmentation|spare.capacity|designed.tree|Aldous", json.dumps(value), re.I):
            state_matches.append({"path": path.relative_to(REPO).as_posix(),
                                  "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                  "deposit_id": value.get("id", value.get("deposit_id"))})
    release = json.loads((AUDIT / "preprint/publication/RELEASE_FILES.json").read_text())
    for entry in release["files"]:
        content = (AUDIT / "preprint/publication" / entry["path"]).read_bytes()
        if len(content) != entry["bytes"] or hashlib.sha256(content).hexdigest() != entry["sha256"]:
            raise RuntimeError("Frozen publication file changed")
    receipt = {"started_utc": now, "completed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
               "operation": operation, "phase": args.phase, "read_only": True,
               "ledger_rows": len(rows), "ledger_matches": matches,
               "ledger_changed_rows_since_initial_candidate_check": changed_rows,
               "account_query": search["query"], "account_keyword_query_total": search["total"],
               "account_total": len(targets), "complete_account_records_scanned": complete_account["total"],
               "account_keyword_search_omitted_expected_deposit": args.expected_deposit_id is not None and args.expected_deposit_id not in {int(item["id"]) for item in search["records"]},
               "account_positive_control": "PASS_23174283", "unexpected_account_matches": [
                   {"id": item["id"], "title": item.get("metadata", {}).get("title"), "status": item.get("status")} for item in unexpected],
               "expected_deposit_id": args.expected_deposit_id,
               "local_deposit_state_matches": state_matches,
               "live_pr": {"state": pr["state"], "merged": pr.get("merged"), "draft": pr["draft"], "head": pr["head"]["sha"]},
               "live_main": main_ref["object"]["sha"], "release_files": release["files"],
               "raw_receipts": raw.relative_to(EFFORT).as_posix(),
               "identity_verdict": "No unexpected leads" if not matches and not unexpected and not changed_rows else "Root reconciliation required; this script does not decide mathematical identity",
               "scope": "Live read-only custody/deduplication evidence, not mathematical/priority clearance or an atomic lock across services."}
    output = AUDIT / ("PREPUBLICATION_" + args.phase.upper() + "_" + operation + ".json")
    atomic_json(output, receipt)
    print(json.dumps({"receipt": str(output), **receipt}, indent=2))


if __name__ == "__main__":
    main()
