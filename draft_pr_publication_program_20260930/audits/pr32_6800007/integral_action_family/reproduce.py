#!/usr/bin/env python3
"""Read-only reproduction of the closed integral family; generated data in tmp/.

Run with /usr/bin/python3 from any directory. Requires the existing SymPy only
for unchanged legacy originals. This does not fetch references, run Git, import
old checkers, or mutate any recorded evidence.
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

FAMILY = pathlib.Path(__file__).resolve().parent
TMP = FAMILY / "tmp" / "reproduce"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def protected():
    original = json.loads((FAMILY / "original_inputs_receipt.json").read_text())
    snapshot = FAMILY.parent / "source_snapshot"
    for item in original["files"]:
        assert sha(snapshot / item["path"]) == item["sha256"], item["path"]
    assert sha(FAMILY / "EARLY_INTEGRAL_SEAL.md") == "d62c9962acbd293d0318518739f8d58aad91917d4cccae6bd90309033f30cf16"
    assert sha(FAMILY.parent / "pr_input" / "diff.patch") == original["exact_frozen_diff_sha256"]
    assert (FAMILY / "artifact_manifest.json").exists(), "closed first-party manifest is required"
    manifest = json.loads((FAMILY / "artifact_manifest.json").read_text())
    names = sorted(str(p.relative_to(FAMILY)) for p in FAMILY.rglob("*")
                   if p.is_file() and p.relative_to(FAMILY).parts[0] != "tmp"
                   and "__pycache__" not in p.relative_to(FAMILY).parts
                   and p.relative_to(FAMILY).as_posix() != "artifact_manifest.json")
    assert names == sorted(item["path"] for item in manifest["members"]), "manifest roster must be exact"
    assert manifest["member_count"] == len(names)
    for item in manifest["members"]:
        assert sha(FAMILY / item["path"]) == item["sha256"], item["path"]
    pr30 = FAMILY.parents[1] / "pr30_30003955" / "geometric_family"
    assert sha(pr30 / "artifact_manifest.json") == "21e46f56cf0a188560c124a92a4f4e80111a85b231d458b0d8a0bd6cfebede60"
    old = json.loads((pr30 / "artifact_manifest.json").read_text())
    assert len(old["files"]) == 26
    for item in old["files"]:
        assert sha(pr30 / item["path"]) == item["sha256"], "closed PR30: " + item["path"]

def run(command, cwd):
    return subprocess.run(command, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    protected()
    TMP.mkdir(parents=True, exist_ok=True)
    copy = TMP / "integral_controls.py"
    shutil.copyfile(FAMILY / copy.name, copy)
    process = run([sys.executable, copy.name], TMP)
    (TMP / "controls_stdout.json").write_bytes(process.stdout)
    (TMP / "controls_stderr.txt").write_bytes(process.stderr)
    assert process.returncode == 0 and not process.stderr
    assert process.stdout == (FAMILY / "integral_results.json").read_bytes()
    data = json.loads(process.stdout)
    assert data["pass"] and data["assertions"] == 3256
    negative = run([sys.executable, copy.name, "--mutant", "ordinary_c2"], TMP)
    (TMP / "ordinary_mutant_stdout.txt").write_bytes(negative.stdout)
    (TMP / "ordinary_mutant_stderr.txt").write_bytes(negative.stderr)
    assert negative.returncode == 1 and b"EXPECTED_FAILURE" in negative.stderr and not negative.stdout
    legacy = run([sys.executable, str(FAMILY / "replay_originals.py"), "--out", "tmp/reproduce/originals"], TMP)
    (TMP / "original_replay_stdout.json").write_bytes(legacy.stdout)
    (TMP / "original_replay_stderr.txt").write_bytes(legacy.stderr)
    assert legacy.returncode == 0 and not legacy.stderr
    legacy_data = json.loads(legacy.stdout)
    assert all(item["byte_identical_to_frozen_output"] for item in legacy_data["runs"])
    protected()
    print(json.dumps({"pass":True,"assertions":data["assertions"],
                      "new_output_byte_identical":True,
                      "original_outputs_byte_identical":True,
                      "negative_harness_exit":negative.returncode,
                      "negative_harness_status":"EXPECTED_FAILURE_NOT_PASS",
                      "protected_inputs_and_manifest_members_unchanged":True},indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
