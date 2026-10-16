#!/usr/bin/env python3
"""Post-provisional evidence binding. Never imports or runs a sibling script."""
from pathlib import Path
import concurrent.futures
import datetime
import gzip
import hashlib
import json
import re
import subprocess
import urllib.request

HERE = Path(__file__).resolve().parent
EFFORT = HERE.parents[1]
ROOT = EFFORT.parents[2]
C = EFFORT / "reviewed_candidate"
S = EFFORT / "source_snapshot"
P = EFFORT / "primary_scope_family"
R = EFFORT / "reproduction_family"

def load(p): return json.loads(p.read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
def gitblob(b): return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
def git(*args): return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout

historical = load(C / "verdict.json")
snapshot = load(EFFORT / "snapshot_manifest.json")
historical_checks = {
    "historical_audit_hash_bound_to_original": historical["audit_sha256"] == sha((S / "AUDIT.md").read_bytes()),
    "historical_audit_hash_distinct_from_current": historical["audit_sha256"] != sha((C / "AUDIT.md").read_bytes()),
    "historical_verifier_hash_still_current": historical["verifier_sha256"] == sha((S / "verify.py").read_bytes()) == sha((C / "verify.py").read_bytes()),
    "historical_review_file_hash_matches": historical["review_sha256"] == sha((C / "REVIEW.md").read_bytes()),
    "historical_review_and_verdict_immutable": all((C / n).read_bytes() == (S / n).read_bytes() for n in ["REVIEW.md", "verdict.json"]),
    "historical_review_commit_matches_status_provenance": historical["reviewed_commit"] == load(C / "status.json")["independent_review"]["reviewed_commit"],
    "current_pending_status_disambiguates_historical_pass": load(C / "status.json")["fresh_complete_acceptance_review"] == "pending" and "They do not certify the clarified current file by hash" in (C / "ACCEPTANCE_AUDIT.md").read_text(),
}
changed = [p.name for p in S.iterdir() if p.is_file() and (C / p.name).read_bytes() != p.read_bytes()]
added = sorted(p.name for p in C.iterdir() if p.is_file() and p.name != "MANIFEST.json" and not (S / p.name).exists())

family_checks = []
for record in load(P / "artifact_manifest.json")["files"]:
    b = (P / record["path"]).read_bytes()
    family_checks.append({"family": "primary_scope_family", "path": record["path"], "sha256": sha(b), "pass": sha(b) == record["sha256"] and len(b) == record["bytes"]})
for name, expected in load(R / "artifact_hashes.json")["files"].items():
    b = (R / name).read_bytes()
    family_checks.append({"family": "reproduction_family", "path": name, "sha256": sha(b), "pass": sha(b) == expected})
family_heads = {n: load(EFFORT / n / "verdict.json").get("audited_head", load(EFFORT / n / "verdict.json").get("frozen_head")) for n in ["all_index_family", "primary_scope_family", "reproduction_family"]}

source_checks = []
for name in ["source_download_manifest.json", "archive_download_manifest.json", "archive_text_manifest.json"]:
    for row in load(P / name):
        b = (P / "tmp" / row["id"]).read_bytes()
        source_checks.append({"id": row["id"], "manifest": name, "sha256": sha(b), "pass": sha(b) == row["sha256"] and len(b) == row["bytes"]})
arxiv = load(P / "arxiv_source_manifest.json")
for name, expected in [("arxiv_source.bin", arxiv["sha256"]), ("arxiv_source.tex", arxiv["tex_sha256"])]:
    b = (P / "tmp" / name).read_bytes()
    source_checks.append({"id": name, "manifest": "arxiv_source_manifest.json", "sha256": sha(b), "pass": sha(b) == expected})
crossref = load(P / "bibliographic_metadata.json")
b = (P / "tmp" / "crossref.json").read_bytes()
source_checks.append({"id": "crossref.json", "manifest": "bibliographic_metadata.json", "sha256": sha(b), "pass": sha(b) == crossref["sha256"] and len(b) == crossref["bytes"]})
probe = P / "current_corrections_probe"
for row in load(probe / "source_manifest.json")["sources"]:
    b = (probe / row["cache_path"]).read_bytes()
    source_checks.append({"id": row["source_id"], "manifest": "current_corrections_probe/source_manifest.json", "sha256": sha(b), "pass": sha(b) == row["sha256"] and len(b) == row["bytes"]})

initial_review = (P / "tmp" / "initial_review.md").read_bytes()
extension_review = (P / "tmp" / "extension_review.md").read_bytes()
initial_commit = load(P / "tmp" / "initial_commit.json")
extension_commit = load(P / "tmp" / "extension_commit.json")
archive_checks = {
    "same_review_bytes_at_both_pins": initial_review == extension_review,
    "exact_credited_git_blob": gitblob(initial_review) == "274c04c5f59fd5f56be95373191ae36d278b3618",
    "initial_commit_pin": initial_commit["sha"] == "b8f60542f758750e263016cad1d45cc0650ed64d",
    "extension_commit_pin": extension_commit["sha"] == "5abed447441b42dbe9f735e8b2960ee0a0705235",
    "initial_dates": initial_commit["commit"]["author"]["date"] == initial_commit["commit"]["committer"]["date"] == "2026-08-30T12:01:44Z",
    "extension_dates": extension_commit["commit"]["author"]["date"] == extension_commit["commit"]["committer"]["date"] == "2026-09-03T09:58:29Z",
    "metadata_unsigned": all(not row["commit"]["verification"]["verified"] and row["commit"]["verification"]["reason"] == "unsigned" for row in [initial_commit, extension_commit]),
    "arxiv_gzip_matches_tex": gzip.decompress((P / "tmp" / "arxiv_source.bin").read_bytes()) == (P / "tmp" / "arxiv_source.tex").read_bytes(),
    "cited_arxiv_pdf_digest_matches_source_manifest": "5666062b7bcf6121f6411bfd4bff4ac338eae7901a44a39bcd64260c0025b31e" in (C / "SOURCES.md").read_text(),
    "cited_published_scan_digest_matches_source_manifest": "31caf2929cfd10c44bee9b41fc85c27791d58c6769951fee7564f7abab55e909" in (C / "SOURCES.md").read_text(),
}
api_measurements = []
for row in load(P / "archive_api_ledger.json")["documents"]:
    if row["url"].endswith("/review-package.md"):
        api_measurements.append({"url": row["url"], "reported_bytes": row["bytes"], "actual_bytes": len(initial_review), "actual_unicode_characters": len(initial_review.decode()), "git_blob_matches": row["sha"] == gitblob(initial_review), "byte_count_matches": row["bytes"] == len(initial_review)})

def check_remote(family):
    rel = EFFORT.relative_to(ROOT).as_posix() + "/" + family + "/REPORT.md"
    url = "https://raw.githubusercontent.com/AlecKriebel/Math/main/" + rel
    with urllib.request.urlopen(url, timeout=30) as response:
        b = response.read()
        return {"family": family, "url": url, "http_status": response.status, "sha256": sha(b), "matches_local": b == (EFFORT / family / "REPORT.md").read_bytes()}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    remote_reports = list(pool.map(check_remote, ["all_index_family", "primary_scope_family", "reproduction_family"]))

primary_cache_ignored = git("check-ignore", "--", str(P / "tmp" / "initial_review.md")).decode().strip() != ""
result = {
    "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "phase": "post_provisional_historical_sibling_provenance_comparison",
    "historical_review_binding_checks": historical_checks,
    "original_files_changed_in_current_candidate": sorted(changed),
    "current_candidate_added_files": added,
    "sibling_manifest_entry_count": len(family_checks),
    "sibling_manifest_checks": family_checks,
    "sibling_verdict_heads": family_heads,
    "source_cache_entry_count": len(source_checks),
    "source_cache_checks": source_checks,
    "archive_and_source_binding_checks": archive_checks,
    "minor_metadata_findings": api_measurements,
    "remote_family_report_links": remote_reports,
    "third_party_fulltext_cache_ignored": primary_cache_ignored,
    "candidate_audit_unchanged_since_blind": sha((C / "AUDIT.md").read_bytes()) == load(HERE / "blind_integrity_results.json")["candidate_audit_sha256"],
    "all_decisive_checks_pass": all(historical_checks.values()) and all(r["pass"] for r in family_checks + source_checks) and all(archive_checks.values()) and all(h == snapshot["head"] for h in family_heads.values()) and all(r["matches_local"] for r in remote_reports) and primary_cache_ignored,
    "limits": "One archive connector ledger labels the Unicode character count 4891 as bytes; direct HTTP cache has 4893 bytes. Blob SHA1 and file SHA256 are correct and separate, so the construction identity is unaffected. Main links are mutable; exact local report hashes are preserved in this result and the family manifests. This script validates evidence identity, not the all-index algebra or exhaustive prior-art status.",
}
(HERE / "evidence_comparison_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ["checked_at", "sibling_manifest_entry_count", "source_cache_entry_count", "candidate_audit_unchanged_since_blind", "all_decisive_checks_pass", "minor_metadata_findings"]}, indent=2))
