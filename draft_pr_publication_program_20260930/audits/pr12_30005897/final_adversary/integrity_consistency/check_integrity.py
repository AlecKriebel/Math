#!/usr/bin/env python3
"""Read-only byte audit; writes solely beside this script.

Run from any directory. No historical verdicts are treated as mathematics.
Paths are resolved by their declarations or the explicit source-name aliases
below, never by searching for an arbitrary file with the expected digest.
"""
import hashlib
import json
import re
import subprocess
import argparse
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
REPO = BASE.parents[2]
HEAD = "19dfaccb52a7640eec79af28a778b4f22f93479a"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--expected-proof", default="2d2e394d83ab96a6aee9b022d375fb1520499ed4aa360de51f7d1ed04f5b75ea")
PROOF = parser.parse_args().expected_proof
SNAP = BASE / "source_snapshot"
CAND = BASE / "reviewed_candidate"
PREFIX = "unsolved_math_prioritization/attempts/30005897/"
SOURCE_ALIASES = {
    "2608.19499.pdf": "pituk2026.pdf",
    "owr-2024-19.pdf": "owr2024.pdf",
    "2009.11526.pdf": "dde2021.pdf",
    "2608.17021.pdf": "messaoudi2026.pdf",
    "shift-classification.pdf": "cdv2024.pdf",
    "2607.15831.pdf": "bdm2026.pdf",
    "CDV-arxiv-2024.pdf": "cdv2024.pdf",
}
checks = []
covered_hash_locations = set()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def label(path):
    try:
        return str(path.relative_to(BASE))
    except ValueError:
        return str(path)


def check_file(manifest, pointer, target, expected, size=None):
    target = target.resolve()
    exists = target.is_file()
    blob = target.read_bytes() if exists else None
    actual = sha(blob) if exists else None
    checks.append({
        "record": label(manifest) + "#" + pointer,
        "target": str(target), "expected_sha256": expected,
        "actual_sha256": actual, "expected_bytes": size,
        "actual_bytes": len(blob) if exists else None,
        "pass": exists and actual == expected and (size is None or len(blob) == size),
    })
    covered_hash_locations.add((str(manifest), pointer))


def target_for(manifest, item):
    for k in ("absolute_path", "local_path", "path", "source", "relative_path"):
        if isinstance(item.get(k), str):
            raw = Path(item[k])
            if raw.is_absolute():
                return raw
            return (SNAP if manifest.name == "snapshot_manifest.json" else manifest.parent) / raw
    if item.get("id"):
        return BASE / "tmp/root_primary" / (item["id"] + ".pdf")
    raise ValueError((manifest, item))


def walk(manifest, value, pointer=""):
    if isinstance(value, list):
        for i, x in enumerate(value):
            walk(manifest, x, pointer + "/" + str(i))
    elif isinstance(value, dict):
        if isinstance(value.get("sha256"), str):
            check_file(manifest, pointer + "/sha256", target_for(manifest, value), value["sha256"], value.get("bytes", value.get("size")))
        for k, x in value.items():
            loc = pointer + "/" + k
            if k == "sha256" and isinstance(x, dict):
                for rel, expected in x.items():
                    check_file(manifest, loc + "/" + rel, manifest.parent / rel, expected)
            elif k == "source_pdf_sha256":
                for rel, expected in x.items():
                    check_file(manifest, loc + "/" + rel, BASE / "tmp/root_primary" / SOURCE_ALIASES[rel], expected)
            elif k == "record_sha256_canonical_json":
                record = json.loads((manifest.parent / "source_record.json").read_text())
                actual = sha(json.dumps(record, sort_keys=True, separators=(",", ":")).encode())
                checks.append({"record": label(manifest) + "#" + loc,
                               "target": str(manifest.parent / "source_record.json"),
                               "serialization": "UTF-8 json.dumps(sort_keys=True,separators=(',',':'))",
                               "expected_sha256": x, "actual_sha256": actual, "pass": x == actual})
                covered_hash_locations.add((str(manifest), loc))
            elif k in ("source_proof_sha256", "exact_candidate_sha256", "candidate_source_sha256"):
                check_file(manifest, loc, SNAP / "PROOF.md", x)
            elif k == "independently_downloaded_official_ems_sha256":
                check_file(manifest, loc, BASE / "tmp/primary_scope/ems_official_pdf.pdf", x)
            else:
                walk(manifest, x, loc)


manifests = [p for p in sorted(BASE.rglob("*.json"))
             if "final_adversary" not in p.parts
             and ("manifest" in p.name.lower() or p.name == "source_provenance.json")]
for manifest in manifests:
    walk(manifest, json.loads(manifest.read_text()))

# A second walker verifies that every literal SHA256 value in the requested
# manifest/provenance set was covered, including unusual scalar field names.
uncovered = []


def literal_hashes(manifest, value, pointer=""):
    if isinstance(value, dict):
        for k, v in value.items():
            literal_hashes(manifest, v, pointer + "/" + k)
    elif isinstance(value, list):
        for i, v in enumerate(value):
            literal_hashes(manifest, v, pointer + "/" + str(i))
    elif isinstance(value, str) and re.fullmatch("[0-9a-f]{64}", value):
        if (str(manifest), pointer) not in covered_hash_locations:
            uncovered.append({"manifest": label(manifest), "pointer": pointer, "value": value})


for manifest in manifests:
    literal_hashes(manifest, json.loads(manifest.read_text()))

# Current acceptance anchor and the root evidence-packaging hash records.
check_file(BASE / "reviewed_candidate/MANIFEST.json", "requested_current_proof", CAND / "PROOF.md", PROOF)
pack = BASE / "priority_exact/root_packaging_repair.json"
pd = json.loads(pack.read_text())
check_file(pack, "/original_raw_sha256", Path(pd["original_raw_cache"]), pd["original_raw_sha256"], pd["original_bytes"])
check_file(pack, "/compact_sha256", BASE / "priority_exact/arxiv_inventory.json", pd["compact_sha256"], pd["compact_bytes"])
for name in ("attempt.json", "attempt_status.json"):
    record = CAND / name
    doc = json.loads(record.read_text())
    check_file(record, "/proof_sha256", CAND / "PROOF.md", doc["proof_sha256"])
    check_file(record, "/original_proof_sha256", SNAP / "PROOF.md", doc["original_proof_sha256"])

# Check the frozen original against actual Git objects at the asserted PR head.
# Git is invoked read-only; no checkout, index, branch, commit, or network writes.
gd = subprocess.run(["git", "ls-tree", "-r", "--name-only", HEAD, "--", PREFIX], cwd=REPO, capture_output=True, check=True)
git_files = [line[len(PREFIX):] for line in gd.stdout.decode().splitlines()]
git_checks = []
for rel in git_files:
    blob = subprocess.run(["git", "show", HEAD + ":" + PREFIX + rel], cwd=REPO, capture_output=True, check=True).stdout
    actual = (SNAP / rel).read_bytes() if (SNAP / rel).is_file() else None
    git_checks.append({"path": rel, "git_sha256": sha(blob), "snapshot_sha256": sha(actual) if actual is not None else None,
                       "git_bytes": len(blob), "snapshot_bytes": len(actual) if actual is not None else None,
                       "pass": actual == blob})
snapshot_record = json.loads((BASE / "snapshot_manifest.json").read_text())
metadata = json.loads((BASE / "pr_metadata.json").read_text())
snapshot_inventory = sorted(str(p.relative_to(SNAP)) for p in SNAP.rglob("*") if p.is_file())
candidate_inventory = sorted(str(p.relative_to(CAND)) for p in CAND.rglob("*") if p.is_file())
snap_declared = sorted(x["path"] for x in snapshot_record["files"])
cand_declared = sorted(list(json.loads((CAND / "MANIFEST.json").read_text())["sha256"]) + ["MANIFEST.json"])
anchors = {
    "expected_pr_head": HEAD,
    "snapshot_head_matches": snapshot_record["head"] == HEAD,
    "metadata_head_matches": metadata["headRefOid"] == HEAD,
    "snapshot_files": len(snapshot_inventory), "git_original_files": len(git_files),
    "snapshot_inventory_matches_declared": snapshot_inventory == snap_declared,
    "snapshot_inventory_matches_git": snapshot_inventory == sorted(git_files),
    "snapshot_original21": len(snapshot_inventory) == 21,
    "candidate_files": len(candidate_inventory),
    "candidate_inventory_matches_declared": candidate_inventory == cand_declared,
}

# Preserve and distinguish all historical artifacts. The current review files
# retain the exact originals. Mutable current prose is tracked explicitly.
delta = []
for rel in sorted(set(snapshot_inventory) | set(candidate_inventory)):
    s, c = SNAP / rel, CAND / rel
    sb = s.read_bytes() if s.is_file() else None
    cb = c.read_bytes() if c.is_file() else None
    delta.append({"path": rel, "original_sha256": sha(sb) if sb is not None else None,
                  "current_sha256": sha(cb) if cb is not None else None,
                  "status": "identical" if sb == cb else "added" if sb is None else "removed" if cb is None else "changed"})

# Resolve current local references and repository-main document URLs against
# the workspace. This asserts intended destination existence, not that an
# unpushed document already exists on the public remote.
links = []
for document in sorted(CAND.rglob("*.md")):
    if "review" in document.relative_to(CAND).parts:
        continue  # byte-preserved historical links are not current routing.
    for number, line in enumerate(document.read_text().splitlines(), 1):
        for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", line):
            if raw.startswith("https://github.com/AlecKriebel/Math/blob/main/"):
                target = REPO / raw.split("/blob/main/", 1)[1]
            elif "://" not in raw and not raw.startswith("#"):
                target = document.parent / raw.split("#", 1)[0]
            else:
                continue
            links.append({"document": label(document), "line": number,
                          "link": raw, "workspace_target": str(target.resolve()),
                          "pass": target.exists()})
precision = BASE / "ROOT_EQ33_PRECISION.md"
precision_record = {"path":str(precision), "sha256":sha(precision.read_bytes()), "bytes":precision.stat().st_size}

result = {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "requested_proof_sha256": PROOF,
    "audit_scope": "artifact-integrity only; no historical verdict reused as a mathematical premise",
    "manifest_paths": [label(x) for x in manifests],
    "literal_hash_coverage_complete": not uncovered, "uncovered_literal_hashes": uncovered,
    "manifest_and_packaging_checks": checks,
    "git_original_snapshot_checks": git_checks, "anchors_and_inventories": anchors,
    "current_document_workspace_link_checks": links,
    "root_source_precision_addendum": precision_record,
    "all_checks_pass": all(c["pass"] for c in checks + git_checks) and not uncovered
        and all(anchors[k] for k in ("snapshot_head_matches", "metadata_head_matches", "snapshot_inventory_matches_declared", "snapshot_inventory_matches_git", "snapshot_original21", "candidate_inventory_matches_declared"))
        and all(x["pass"] for x in links),
}
(OUT / "integrity_results.json").write_text(json.dumps(result, indent=2) + "\n")
(OUT / "original_candidate_delta.json").write_text(json.dumps({"timestamp_utc":result["timestamp_utc"], "records":delta}, indent=2) + "\n")
print(json.dumps({"manifest_count":len(manifests), "hash_check_count":len(checks),
                  "git_original_check_count":len(git_checks), "all_checks_pass":result["all_checks_pass"],
                  "failures":[c for c in checks+git_checks if not c["pass"]],
                  "uncovered_literal_hashes":uncovered, "anchors_and_inventories":anchors,
                  "workspace_link_check_count":len(links), "workspace_link_failures":[x for x in links if not x["pass"]],
                  "root_source_precision_addendum":precision_record}, indent=2))
