#!/usr/bin/env python3
"""Read-only integrity checks; output stays in this auditor's own directory."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
EFFORT = HERE.parents[1]
ROOT = EFFORT.parents[2]
CANDIDATE = EFFORT / "reviewed_candidate"
SNAPSHOT = EFFORT / "source_snapshot"
EXPECTED_AUDIT = "305deec60d853ee610f8c80b0dde791ea0e3b078e99a2110d5d58e91c2655af9"
EXPECTED_HEAD = "7a845f7e025a24affe1b712cf7ada648570f9c64"
PREFIX = "unsolved_math_prioritization/attempts/11000263/"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout

def load(path):
    return json.loads(path.read_text())

manifest = load(CANDIDATE / "MANIFEST.json")
snapshot_manifest = load(EFFORT / "snapshot_manifest.json")
entries = manifest["sha256"]
actual_files = sorted(p.name for p in CANDIDATE.iterdir() if p.is_file() and p.name != "MANIFEST.json")
current_checks = [{"path": name, "expected_sha256": digest,
                   "actual_sha256": sha((CANDIDATE / name).read_bytes()),
                   "pass": digest == sha((CANDIDATE / name).read_bytes())}
                  for name, digest in sorted(entries.items())]
original_checks = []
for record in snapshot_manifest["files"]:
    name = record["path"]
    data = (SNAPSHOT / name).read_bytes()
    committed = git("show", EXPECTED_HEAD + ":" + PREFIX + name)
    blob = git("rev-parse", EXPECTED_HEAD + ":" + PREFIX + name).decode().strip()
    original_checks.append({"path": name, "sha256": sha(data), "expected_sha256": record["sha256"],
                            "git_head_sha256": sha(committed), "git_blob": blob,
                            "expected_git_blob": record["git_blob"], "size": len(data),
                            "expected_size": record["size"],
                            "pass": data == committed and sha(data) == record["sha256"]
                            and blob == record["git_blob"] and len(data) == record["size"]})

blind_text_names = ["AUDIT.md", "SCALAR_SCOPE_CHECK.md", "README.md", "SOURCES.md", "RESEARCH_LOG.md", "pr_draft.md"]
relative_links = []
for name in blind_text_names:
    body = (CANDIDATE / name).read_text()
    for target in re.findall(r"\]\(([^)]+)\)", body):
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            continue
        path = target.split("#", 1)[0]
        relative_links.append({"from": name, "target": target,
                               "exists": (CANDIDATE / path).exists()})

status = load(CANDIDATE / "status.json")
readiness = load(CANDIDATE / "readiness.json")
input_record = load(CANDIDATE / "input_record.json")
pr = load(EFFORT / "pr_input.json")
metadata = {
    "ids_consistent": status["problem_id"] == readiness["problem_id"] == input_record["problem_id"] == 11000263,
    "candidate_hash_in_status": status["current_audit_sha256"] == EXPECTED_AUDIT,
    "candidate_hash_in_readiness": readiness["current_audit_sha256"] == EXPECTED_AUDIT,
    "original_hash_in_status": status["original_audit_sha256"] == snapshot_manifest["files"][0]["sha256"],
    "queue_unsolved": status["queue_status_proposed"] == "unsolved",
    "review_pending": status["fresh_complete_acceptance_review"] == "pending",
    "no_new_discovery": status["new_discovery"] is False,
    "no_paper": status["paper_created"] is False,
    "no_deposit": status["zenodo_deposit_created"] is False,
    "no_tracker": status["tracker_row_created"] is False,
    "one_attempt": status["new_proof_attempts_used"] == 1,
    "model_effort_preserved": status["model"] == "gpt-6-astra" and status["reasoning"] == "xhigh",
    "pr_metadata_head_consistent": pr["headRefOid"] == snapshot_manifest["head"] == EXPECTED_HEAD,
    "pr_is_open_draft": pr["isDraft"] is True and pr["state"] == "OPEN" and pr["number"] == 13,
    "review_hash_is_dataset_review_join": readiness["review_hash"] == input_record["catalog_at_start"]["review_hash"],
}
result = {
    "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "phase": "blind_candidate_metadata_and_byte_integrity",
    "candidate_audit_sha256": sha((CANDIDATE / "AUDIT.md").read_bytes()),
    "expected_candidate_audit_sha256": EXPECTED_AUDIT,
    "candidate_manifest_sha256": sha((CANDIDATE / "MANIFEST.json").read_bytes()),
    "snapshot_manifest_sha256": sha((EFFORT / "snapshot_manifest.json").read_bytes()),
    "candidate_manifest_entry_count": len(entries),
    "candidate_regular_files_excluding_manifest": actual_files,
    "candidate_manifest_exact_file_coverage": sorted(entries) == actual_files,
    "candidate_manifest_checks": current_checks,
    "snapshot_file_count": len(original_checks),
    "snapshot_exact_file_coverage": sorted(r["path"] for r in snapshot_manifest["files"]) == sorted(p.name for p in SNAPSHOT.iterdir() if p.is_file()),
    "snapshot_and_git_head_checks": original_checks,
    "metadata_checks": metadata,
    "relative_links_in_blind_files": relative_links,
    "current_branch": git("rev-parse", "--abbrev-ref", "HEAD").decode().strip(),
    "audit_pass": sha((CANDIDATE / "AUDIT.md").read_bytes()) == EXPECTED_AUDIT
        and len(entries) == 18 and len(original_checks) == 16
        and sorted(entries) == actual_files
        and all(r["pass"] for r in current_checks + original_checks)
        and all(metadata.values()) and all(r["exists"] for r in relative_links),
    "bounds": "Hashes of archived REVIEW/verdict were checked as opaque bytes; their contents and all sibling reports were not read before this provisional check. Historical PR body is input provenance, not current candidate metadata. No core all-index algebra was independently decided by this script.",
}
(HERE / "blind_integrity_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ["checked_at", "candidate_audit_sha256", "candidate_manifest_entry_count", "snapshot_file_count", "candidate_manifest_exact_file_coverage", "audit_pass"]}, indent=2))
