"""Verify the complete closed review and its private full-stream receipts."""
from pathlib import Path
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def binding(root, row, key="path"):
    relative = Path(row[key])
    assert not relative.is_absolute() and ".." not in relative.parts
    path = root / relative
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
    return raw


def instant(value):
    return datetime.datetime.fromisoformat(value)


manifest_raw = (HERE / "IMMUTABLE_MANIFEST.json").read_bytes()
manifest = json.loads(manifest_raw)
names = [row["path"] for row in manifest["files"]]
assert len(names) == len(set(names))
actual = sorted(path.relative_to(HERE).as_posix()
                for path in HERE.rglob("*") if path.is_file()
                and "private" not in path.relative_to(HERE).parts
                and path.name not in ["IMMUTABLE_MANIFEST.json", "FINAL_SEAL.json"])
assert actual == sorted(names)
for row in manifest["files"]:
    binding(HERE, row)
final = json.loads((HERE / "FINAL_SEAL.json").read_bytes())
assert final["manifest_sha256"] == sha(manifest_raw)
assert final["verdict"] == "PASS_ALREADY_SOLVED_CREDITED_DIRECT_PROOF"
assert final["mandatory_repairs"] == 0 and final["family_completion_percent"] == 100
assert final["live_pr_integration_certified"] is False

source = json.loads((HERE / "SOURCE_SEAL.json").read_bytes())
math = json.loads((HERE / "MATH_SEAL.json").read_bytes())
candidate = json.loads((HERE / "CANDIDATE_MATH_SEAL.json").read_bytes())
code = json.loads((HERE / "CODE_SEAL.json").read_bytes())
binding(HERE, source["source_baseline"])
binding(HERE, math["math_baseline"])
binding(HERE, math["source_seal"])
binding(HERE, candidate["candidate_mathematical_audit"])
binding(HERE, candidate["prior_source_seal"])
binding(HERE, candidate["prior_math_seal"])
for row in source["fresh_primary_receipts"]:
    binding(HERE, row)
assert source["candidate_read_before_seal"] is False
assert math["candidate_read_before_seal"] is False
assert candidate["candidate_code_read"] is False
assert candidate["candidate_code_executed"] is False
assert candidate["historical_review_read"] is False
assert all(row["sibling_conclusions_read"] is False for row in [source, math, candidate, code])
for row in code["files"]:
    raw = Path(row["absolute_path"]).read_bytes()
    assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
assert code["all_four_programs_fully_read"] is True
assert code["candidate_code_executed_before_seal"] is False
assert code["independent_code_executed_before_seal"] is False

receipt = json.loads((HERE / "REPRODUCTION.json").read_bytes())
assert receipt["status"] == "PASS" and receipt["assertions"] == 340
assert receipt["complete_manifest_binding_instances"] == 48
assert receipt["whole_snapshot_files_verified"] == 22
assert receipt["target_files_verified"] == 21
assert receipt["queue_changed_cells"] == [8, 9]
assert receipt["queue_physical_line"] == 406
assert len(receipt["commands"]) == 28
assert instant(source["utc"]) <= instant(math["utc"]) < instant(candidate["utc"]) < instant(code["utc"])
assert instant(code["utc"]) < min(instant(row["started_utc"]) for row in receipt["commands"])
prior_end = instant(code["utc"])
for row in receipt["commands"]:
    assert prior_end <= instant(row["started_utc"]) <= instant(row["finished_utc"])
    prior_end = instant(row["finished_utc"])
    assert row["returncode"] == 0
    stdout = binding(HERE, row["stdout"])
    stderr = binding(HERE, row["stderr"])
    assert stderr == b""
    if row["label"] in ["author", "historical", "independent"]:
        assert stdout == (HERE / (row["label"] + ".stdout")).read_bytes()
        assert stderr == (HERE / (row["label"] + ".stderr")).read_bytes()
        assert json.loads(stdout) == receipt[row["label"] + "_full_output"]
for row in receipt["all_bindings"]:
    root = Path(row["manifest"]).parent
    binding(root, row)
assert prior_end <= instant(receipt["completed_utc"])
assert receipt["author_full_output"]["assertions"] == 2690
assert receipt["historical_full_output"]["independent_assertions"] == 1909
assert receipt["independent_full_output"]["assertions"] == 823
assert len(receipt["independent_full_output"]["negative_controls_rejected"]) == 7
verifier = json.loads((HERE / "VERIFIER_CODE_SEAL.json").read_bytes())
binding(HERE, verifier["source"])
assert instant(verifier["utc"]) < instant(final["utc"])
print(json.dumps({"status":"PASS", "closed_public_files":len(names),
                  "complete_private_command_streams":56, "historical_binding_instances":48,
                  "independence_and_code_seals_verified":True,
                  "scope":"Closed public bytes, complete raw source and command stream bindings, all receipt fields relevant to scope/chronology, complete computation output equality; no current-live-PR acceptance."},
                 indent=2, sort_keys=True))
