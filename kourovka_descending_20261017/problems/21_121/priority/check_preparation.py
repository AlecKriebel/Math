"""Read-only, offline integrity and source-scope checks for 21.121 preparation.

Default behavior: reads only the dedicated package and the specifically named
authenticated sibling Notebook cache, prints JSON, and exits. No network, writes,
Git commands, subprocesses, imports of local modules, or mathematical discovery.
This checker does not prove source theorems or certify exhaustive priority.
"""

import hashlib
import json
from pathlib import Path
import re
import sys


BASE = Path(__file__).resolve().parent
SIBLING = BASE.parent.parent / "21_122" / "priority"


def require(test, message):
    if not test:
        raise AssertionError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return json.loads((BASE / name).read_text())


def main():
    require(len(sys.argv) == 1, "No options: the default checker is read-only and offline")
    scope = load("SCOPE_CONTRACT.json")
    require(scope["problem"] == "21.121", "wrong problem")
    require(scope["stage"] == "source_preparation_only", "not source-only")
    require(scope["source_preparation_completion_percent"] == 100, "preparation not complete")
    require(scope["discovery_completion_estimate_percent"] == 0, "nonzero discovery estimate")
    require(scope["original_mathematics_started"] is False, "original research was started")
    require(scope["selection_status"] == "pending_parent_independent_audit", "premature selection")
    require(scope["parts"]["a"]["official_notice"] == "confirmed_negative", "part (a) notice lost")
    require(scope["parts"]["b"]["official_solved_marker"] is False, "part (b) marker changed")
    require(scope["parts"]["b"]["full_prior_resolution_located"] is False, "priority finding changed")
    require(scope["parts"]["b"]["requires_admissibility_at_exactly_three"] is False,
            "infimum confused with attainment")

    manifest = load("PREPARATION_MANIFEST.json")
    for rec in manifest["files"]:
        path = BASE / rec["file"]
        require(path.is_file(), f"missing package file: {rec['file']}")
        require(path.stat().st_size == rec["bytes"], f"size mismatch: {rec['file']}")
        require(digest(path) == rec["sha256"], f"hash mismatch: {rec['file']}")

    source_manifest = load("SOURCE_MANIFEST.json")
    checked_sources = 0
    failures = []
    for rec in source_manifest["sources"]:
        if rec["status"] == "retrieval_failed":
            failures.append({"url": rec["url"], "error": rec["error"]})
            continue
        path = (BASE / rec["file"]).resolve()
        require(path.is_relative_to(BASE / "cache"), "source cache escaped its dedicated folder")
        require(path.is_file(), f"missing raw cache: {rec['file']}")
        require(path.stat().st_size == rec["bytes"], f"source size mismatch: {rec['file']}")
        require(digest(path) == rec["sha256"], f"source hash mismatch: {rec['file']}")
        if "zenodo_reported_md5" in rec:
            require(hashlib.md5(path.read_bytes()).hexdigest() ==
                    rec["zenodo_reported_md5"].split(":", 1)[1], "Zenodo MD5 mismatch")
        checked_sources += 1

    provenance = load("OFFICIAL_CACHE_PROVENANCE.json")
    for rec in provenance["reused_cache"]:
        path = (BASE / rec["file"]).resolve()
        require(path.is_relative_to(SIBLING / "sources"), "unexpected sibling cache path")
        require(path.stat().st_size == rec["bytes"], "reused cache size mismatch")
        require(digest(path) == rec["sha256"], "reused cache hash mismatch")
        require(rec["sha256"] == rec["original_source_record"]["sha256"],
                "original authentication mismatch")
    require(all(r["matches_reused_cache"] for r in provenance["fresh_download_hash_checks"]),
            "fresh official PDF differs from reused cache")

    book = (SIBLING / "sources/notebook21_fresh.txt").read_text()
    pages = book.split("\f")
    matches = [(i + 1, page) for i, page in enumerate(pages)
               if "21.121. Let p be a prime number." in page]
    require(len(matches) == 1 and matches[0][0] == 197, "official problem page mismatch")
    page = matches[0][1]
    require(re.search(r"^\s*∗ a\)", page, re.M), "part (a) solved marker missing")
    require(re.search(r"^\s*b\)", page, re.M), "part (b) unstarred line missing")
    require("AI solution confirmed by C. Shramov" in page, "editorial confirmation absent")
    start = book.index("21.121. Let p be a prime number.")
    end = book.index("\n21.122.", start)
    require((BASE / "cache/official_problem_excerpt.txt").read_text() ==
            book[start:end].rstrip() + "\n", "main excerpt mismatch")
    updates = (SIBLING / "sources/notebook_updates_fresh.txt").read_text()
    start = updates.index("21.121. Let p be a prime number.")
    end = updates.index("\n∗ 21.134.", start)
    require((BASE / "cache/official_update_excerpt.txt").read_text() ==
            updates[start:end].rstrip() + "\n", "update excerpt mismatch")

    home = (BASE / "cache/official_site.html").read_text()
    require(all(s in home for s in ["October 2026 update-3", "2026-10-20",
                                   "21tkt-3.pdf", "21upd-3.pdf"]), "official current links changed")
    latest = load("cache/zenodo_latest.json")
    require(latest["id"] == 23421603, "latest Zenodo record changed")
    require(latest["metadata"]["publication_date"] == "2026-10-16", "latest date mismatch")
    require(any(r["is_last"] for r in latest["metadata"]["relations"]["version"]),
            "latest metadata does not identify last version")
    for filename in ["jayadevan.txt", "jayadevan_latest.txt"]:
        text = (BASE / "cache" / filename).read_text()
        require("Theorem 1.1." in text and "(1, ∞)" in text, "part (a) theorem scope absent")
    ku = (BASE / "cache/kinyon_urban.txt").read_text()
    require("only partial results for (b)" in ku, "Kinyon–Urban scope boundary absent")
    require("These results leave the unrestricted bound three unresolved." in ku,
            "Kinyon–Urban limitation absent")
    require("cache/" in (BASE / ".gitignore").read_text(), "raw cache not excluded")

    receipt = load("PREPARATION_RECEIPT.json")
    require(receipt["source_preparation_completion_percent"] == 100 and
            receipt["discovery_completion_estimate_percent"] == 0, "receipt percentages differ")
    require(receipt["original_mathematics_started"] is False and
            receipt["selection_status"] == "pending_parent_independent_audit", "receipt phase differs")
    print(json.dumps({
        "status": "passed",
        "problem": "21.121",
        "stage": "source_preparation_only",
        "package_files_verified": len(manifest["files"]),
        "source_records_verified": checked_sources,
        "reused_official_cache_files_verified": len(provenance["reused_cache"]),
        "source_preparation_completion_percent": 100,
        "discovery_completion_estimate_percent": 0,
        "selection_status": "pending_parent_independent_audit",
        "recorded_access_failures": failures,
        "limitations": "Integrity and scope checks only; no mathematical proof or exhaustive-priority certification",
        "network_used": False,
        "files_written": False,
    }, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(json.dumps({"status": "failed", "error": str(error)}, indent=2))
        sys.exit(1)
