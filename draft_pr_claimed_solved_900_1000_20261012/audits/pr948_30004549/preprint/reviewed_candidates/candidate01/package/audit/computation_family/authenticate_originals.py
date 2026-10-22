#!/usr/bin/env python3
"""Read-only binding of audit inputs to PR 948's immutable Git objects."""
from pathlib import Path
import datetime, hashlib, json, os, stat, subprocess

ROOT = Path(__file__).resolve().parents[5]
A = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
HEAD = "be4313efafa1af5962394e07d8a4debff2e94d92"

def git(*args):
    return subprocess.check_output(["git", "-c", "gc.auto=0", *args], cwd=ROOT)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

gate = json.loads((A / "ELIGIBILITY_GATE.json").read_bytes())
snapshot = json.loads((A / "ORIGINAL_SNAPSHOT.json").read_bytes())
records = json.loads((A / "ORIGINAL_FILE_RECORDS.json").read_bytes())
require(gate["number"] == 948 and gate["problem_id"] == "30004549", "wrong target")
require(gate["eligible"] is True and gate["status"] == "claimed_solved", "ineligible")
require(gate["headRefOid"] == snapshot["head"] == records["head"] == HEAD, "head mismatch")
require(gate["state"] == "OPEN" and gate["isDraft"] is True, "wrong PR state")
require(git("rev-parse", HEAD + "^{commit}").decode().strip() == HEAD, "no immutable commit")
require(len(snapshot["files"]) == len(records["files"]) == 24, "unexpected input count")
require(set(snapshot["files"]) == set(records["files"]), "path mismatch")
results = []
for path, expected in snapshot["files"].items():
    rec = records["files"][path]
    mode_blob_path = git("ls-tree", HEAD, "--", path).decode().strip()
    metadata, actual_path = mode_blob_path.split("\t")
    mode, kind, blob = metadata.split()
    require(actual_path == path and kind == "blob", "tree path/type mismatch: " + path)
    require(mode == rec["git_mode"] == "100644" and blob == rec["git_blob"], "Git metadata mismatch: " + path)
    content = git("cat-file", "blob", blob)
    disk = A / "original" / path
    st = disk.lstat()
    require(stat.S_ISREG(st.st_mode) and not disk.is_symlink(), "nonregular original: " + path)
    disk_bytes = disk.read_bytes()
    require(content == disk_bytes, "disk/Git bytes mismatch: " + path)
    require(len(content) == rec["bytes"] and sha(content) == expected == rec["sha256"], "size/hash mismatch: " + path)
    require(oct(stat.S_IMODE(st.st_mode)) == rec["snapshot_disk_mode"], "disk mode mismatch: " + path)
    results.append({"path": path, "git_mode": mode, "git_blob": blob, "bytes": len(content), "sha256": sha(content)})
source = A / "source_record_private.txt"
require(source.is_file() and not source.is_symlink(), "source type mismatch")
source_expected = "5df3868e802d9da72bced3f4606c3ccd9b6610208bcc2a086bf25e082239b34f"
source_actual = sha(source.read_bytes())
require(source_actual == source_expected, "corrected full private source hash mismatch")
source_record = json.loads(source.read_bytes())
statement_sha256 = sha(source_record["problem"]["statement"].encode("utf-8"))
require(statement_sha256 == "a5ce90b9c2087f20cd09cb33d9d92ca40039c19a08de3b1c098d10bf75b9179b", "nested statement mismatch")
require(source_record["review_hash"] == "b667ba93b244f20bf9dd6b244af355c1b933340bb194c5a18a0d7c27d5ed9bb4", "review hash mismatch")
require(source_record["prior_research"] == {}, "prior_research changed")
result = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "target": "PR948/problem30004549", "head": HEAD, "gate_fields_pass": True, "file_count": len(results), "all_originals_match_immutable_git": True, "private_source_pin_pass": source_actual == source_expected, "private_source_expected_sha256": source_expected, "private_source_actual_sha256": source_actual, "statement_sha256": statement_sha256, "review_hash": source_record["review_hash"], "prior_research_empty": True, "input_metadata_correction": "Initial supplied source pin was nested UTF-8 statement hash, not full-record file hash; original failed receipt retained separately.", "control_hashes": {n: sha((A/n).read_bytes()) for n in ("ELIGIBILITY_GATE.json", "ORIGINAL_SNAPSHOT.json", "ORIGINAL_FILE_RECORDS.json")}, "files": results}
(OUT / "AUTHENTICATION_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "files"}, indent=2))
require(result["private_source_pin_pass"], "private source hash mismatch; no mathematical input read")
