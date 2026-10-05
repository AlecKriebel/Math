#!/usr/bin/env python3
"""Measure and permission-seal this completed review; never mutate named inputs."""
import datetime
import hashlib
import json
import pathlib
import stat

BASE = pathlib.Path(__file__).resolve().parent
EXPECTED_BASE = pathlib.Path("/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr311_30005303/preprint_review_02")
assert BASE == EXPECTED_BASE
ADMIN = {"FINAL_SEAL_MANIFEST.json", "FINAL_SEAL_VERIFICATION.json", "FINAL_CLOSURE_RECORD.json"}
for label in ("final_seal", "final_verify"):
    ADMIN.update("private/"+label+suffix for suffix in (".stdout", ".stderr", ".command.json"))

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def pin(path):
    data = path.read_bytes()
    return {"path":str(path.resolve()), "bytes":len(data), "sha256":hashlib.sha256(data).hexdigest(),
            "mode":format(stat.S_IMODE(path.stat().st_mode),"04o")}

started = utc()
imported = json.loads((BASE/"private/released_input_manifest.json").read_text())
assert imported["named_input_count"] == len(imported["inputs"]) == 31
originals = []
for row in imported["inputs"]:
    expected = row["original"]
    actual = pin(pathlib.Path(expected["path"]))
    assert actual == expected, (expected,actual)
    local = pin(pathlib.Path(row["local_copy"]["path"]))
    assert (local["sha256"],local["bytes"]) == (expected["sha256"],expected["bytes"])
    originals.append(actual)
initial = json.loads((BASE/"SOURCE_ONLY_FREEZE_MANIFEST.json").read_text())
gate = initial["reports"] + initial["private_evidence"]
for expected in gate:
    assert pin(pathlib.Path(expected["path"])) == expected
check = {"start_utc":started, "checked_utc":utc(), "status":"PASS_ALL_31_NAMED_INPUTS_AND_SOURCE_ONLY_GATE_UNCHANGED",
         "named_input_count":31, "named_original_inputs":originals, "source_only_entry_count":len(gate),
         "source_only_manifest":pin(BASE/"SOURCE_ONLY_FREEZE_MANIFEST.json"),
         "source_only_verification":pin(BASE/"SOURCE_ONLY_FREEZE_VERIFICATION.json"),
         "local_copy_mode_note":"Imported copies were 0644; final review sealing changes their local modes to 0444, never original named input modes."}
(BASE/"NAMED_INPUTS_FINAL_CHECK.json").write_text(json.dumps(check,indent=2)+"\n")
files = []
directories = []
for path in sorted(BASE.rglob("*")):
    assert not path.is_symlink(), path
    rel = path.relative_to(BASE).as_posix()
    if path.is_file() and rel not in ADMIN:
        path.chmod(0o444)
        measured = pin(path)
        files.append({"relative_path":rel, "bytes":measured["bytes"], "sha256":measured["sha256"], "mode":measured["mode"]})
    elif path.is_dir():
        directories.append({"relative_path":rel,"mode":format(stat.S_IMODE(path.stat().st_mode),"04o")})
manifest = {"schema":"finished-independent-review-seal-v1", "reviewer":"pr311_preprint_02", "sealed_utc":utc(),
            "substantive_full_review_complete":True, "blocking_findings":0, "completion_percent":100,
            "manifested_file_count":len(files), "files":files, "directories":directories,
            "administrative_non_self_hashing_exclusions":sorted(ADMIN),
            "exclusions_rule":"This manifest cannot hash itself or later verification and command records. All listed administrative files are separately measured and mode-sealed by FINAL_CLOSURE_RECORD.json; that final record's own pin is reported outside its bytes.",
            "named_input_check":pin(BASE/"NAMED_INPUTS_FINAL_CHECK.json"),
            "source_only_gate_manifest":pin(BASE/"SOURCE_ONLY_FREEZE_MANIFEST.json"),
            "scope":"Complete new review, not prior-verdict or selected-finding recheck. Independent final verifier rereads every listed file, all named originals and the original source-only gate.",
            "mode_limit":"0444 is reversible measured filesystem permission, not immutable storage. Directory modes are measured separately; no new entries are authorized after final closure.",
            "external_communication":False, "publication_or_merge_performed":False}
target = BASE/"FINAL_SEAL_MANIFEST.json"
assert not target.exists()
target.write_text(json.dumps(manifest,indent=2)+"\n")
target.chmod(0o444)
print(json.dumps({"status":"SEALED_REVIEW_PENDING_INDEPENDENT_MECHANICAL_VERIFICATION", "manifest":pin(target), "manifested_file_count":len(files)}))
