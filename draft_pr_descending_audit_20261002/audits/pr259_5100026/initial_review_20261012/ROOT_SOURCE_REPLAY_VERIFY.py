#!/usr/bin/env python3
"""Root independently authenticates one audit family and replays all four inputs.

This driver has no provider or Git operations. It creates a new owned output
directory and never writes the frozen submission or an audit-family artifact.
"""
import argparse
import base64
import concurrent.futures
import hashlib
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--library-dir", required=True)
ap.add_argument("--output-dir", required=True)
args = ap.parse_args()
assert not sys.flags.optimize
B = Path(__file__).resolve().parent
S = B / "submitted/unsolved_math_prioritization/attempts/5100026"
F = B / "source_reproduction_adversary"
D = Path(args.output_dir).resolve()
D.mkdir(exist_ok=False)
utc = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda body: hashlib.sha256(body).hexdigest()
pin = lambda body: {"bytes": len(body), "sha256": sha(body)}
blob = lambda body: hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()
checks = []
inputs = []

def ck(condition, name):
    assert condition, name
    checks.append(name)

def read(path):
    ck(path.is_file() and not path.is_symlink(), "regular-file:" + str(path))
    body = path.read_bytes()
    inputs.append({"path": str(path), **pin(body)})
    return body

intake = json.loads(read(B / "INTAKE.json"))
for row in intake["files"]:
    body = read(Path(row["local_path"]))
    ck(pin(body) == {k: row[k] for k in ("bytes", "sha256")}, "intake-byte-pin:" + row["repository_path"])
    ck(blob(body) == row["git_blob_oid"], "native-blob:" + row["repository_path"])

for name, base in (("FROZEN_MANIFEST.json", S), ("PUBLICATION_MANIFEST.json", S), ("REVIEW_MANIFEST.json", S / "independent_review")):
    manifest = json.loads(read(base / name))
    for relative, expected in manifest["files"].items():
        assert not Path(relative).is_absolute() and ".." not in Path(relative).parts
        body = read(base / relative)
        ck(sha(body) == (expected if isinstance(expected, str) else expected["sha256"]), name + ":" + relative)
        if isinstance(expected, dict):
            ck(len(body) == expected["bytes"], name + ":size:" + relative)
    for key, target in (("reviewed_proof_sha256", S / "PROOF.md"), ("reviewed_author_manifest_sha256", S / "FROZEN_MANIFEST.json")):
        if key in manifest:
            ck(manifest[key] == sha(read(target)), name + ":" + key)

manifest_body = read(F / "MANIFEST.json")
family = json.loads(manifest_body)
for section in ("public_eligible_family_artifacts", "private_reading_evidence_excluded_from_publication"):
    for row in family[section]:
        relative = row["path"]
        assert not Path(relative).is_absolute() and ".." not in Path(relative).parts
        body = read(F / relative)
        ck(pin(body) == {k: row[k] for k in ("bytes", "sha256")}, "family-pin:" + relative)

for capture in (B / "intake_GET_captures").glob("BLOB_*.stdout.json"):
    doc = json.loads(read(capture))
    body = base64.b64decode(doc["content"])
    matching = [row for row in intake["files"] if row["git_blob_oid"] == doc["sha"]]
    ck(len(matching) == 1, "capture maps uniquely:" + capture.name)
    ck(blob(body) == doc["sha"] and len(body) == doc["size"], "capture native object:" + capture.name)
    ck(body == read(Path(matching[0]["local_path"])), "capture exact bytes:" + capture.name)

source = json.loads(read(F / "SOURCE_PINS.json"))
for row in source["source_pdf_pins"]:
    body = read(Path(row["local_reading_path"]))
    ck(sha(body) == row["sha256"] and len(body) == row["bytes"], "PDF:" + row["reading_filename"])
data_pin = source["imported_problem_pin"]
data_body = read(Path(data_pin["input_file"]))
ck(len(data_body) == data_pin["actual_bytes"] and sha(data_body) == data_pin["actual_file_sha256"], "complete dataset hash")
records = json.loads(data_body)
assert isinstance(records, list)
matching = [row for row in records if str(row.get("id")) == "5100026"]
ck(len(matching) == 1, "unique exact dataset id")
record_body = read(Path(data_pin["private_record_copy_path"]))
ck(json.loads(record_body) == matching[0], "exact imported record equals pinned dataset record")
ck(data_pin["pinned_revision"] == "37e53eabe540fb458758e198be61634bd02ee008", "dataset revision")

wrapper = D / "isolated_library_wrapper.py"
wrapper.write_text("import runpy,sys\nassert not sys.flags.optimize\nsys.path.insert(0,sys.argv[1])\nimport sympy,mpmath\nassert sympy.__version__=='1.14.0'\nassert mpmath.__version__=='1.3.0'\nscript=sys.argv[2]\nsys.argv=[script]\nrunpy.run_path(script,run_name='__main__')\n")
jobs = (("author_exact", "verify_exact.py", "exact_checks.json"),
        ("author_numeric", "verify_numeric.py", "numeric_checks.json"),
        ("review_exact", "independent_review/independent_exact.py", "independent_review/INDEPENDENT_EXACT.json"),
        ("review_numeric", "independent_review/independent_numeric.py", "independent_review/INDEPENDENT_NUMERIC.json"))

def replay(job):
    tag, script, frozen_receipt = job
    scratch = D / tag
    scratch.mkdir()
    original = (S / script).read_bytes()
    target = scratch / Path(script).name
    target.write_bytes(original)
    expected = (S / frozen_receipt).read_bytes()
    command = [sys.executable, "-I", "-B", str(wrapper), str(Path(args.library_dir).resolve()), str(target)]
    start = utc()
    tick = time.monotonic()
    result = subprocess.run(command, cwd=scratch, capture_output=True, check=False)
    (scratch / "stdout.json").write_bytes(result.stdout)
    (scratch / "stderr.txt").write_bytes(result.stderr)
    receipt = {"tag": tag, "command": command, "cwd": str(scratch), "UTC_started": start, "UTC_finished": utc(), "seconds": time.monotonic()-tick,
               "script": script, "script_pin": pin(original), "frozen_receipt": frozen_receipt, "expected_receipt_pin": pin(expected),
               "stdout": pin(result.stdout), "stderr": pin(result.stderr), "exit_code": result.returncode,
               "byte_identical": result.stdout == expected,
               "source_unchanged": (S / script).read_bytes() == original and (S / frozen_receipt).read_bytes() == expected,
               "local_wrapper_only_adds_mathematical_libraries": True}
    (scratch / "RECEIPT.json").write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
    assert result.returncode == 0 and not result.stderr and receipt["byte_identical"] and receipt["source_unchanged"], receipt
    return receipt

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    replays = list(pool.map(replay, jobs))
for row in inputs:
    ck(pin(Path(row["path"]).read_bytes()) == {k: row[k] for k in ("bytes", "sha256")}, "final input unchanged:" + row["path"])
ck((F / "MANIFEST.json").read_bytes() == manifest_body, "family manifest unchanged")
report = {"schema": "root-independent-pr259-source-replay-verification-v1", "UTC": utc(), "status": "PASS",
          "input_checks": len(checks), "checks": checks, "input_pins": inputs,
          "family_public_artifact_count": len(family["public_eligible_family_artifacts"]),
          "family_private_excluded_count": len(family["private_reading_evidence_excluded_from_publication"]),
          "family_manifest_pin": pin(manifest_body), "four_unmodified_replays": replays,
          "Root_runtime": sys.version, "library_dir": str(Path(args.library_dir).resolve()),
          "all_replay_output_bytes_identical": True, "primary_Git_writes": 0, "provider_writes": 0,
          "theorem_final_acceptance": False, "novelty_priority_clearance": False,
          "scope": "Authenticates exact source/reproduction-family artifacts and independently repeats four unmodified frozen programs under Root's explicit Python3.14.6 -I -B runtime/library path. No all-period theorem or novelty decision is implied."}
(D / "VERIFICATION.json").write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
print(json.dumps({k: report[k] for k in ("status", "input_checks", "family_public_artifact_count", "family_private_excluded_count", "all_replay_output_bytes_identical")}, sort_keys=True))
