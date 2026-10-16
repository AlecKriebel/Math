#!/usr/bin/env python3
"""Run fail-closed custody controls only in newly owned RAM scratch copies."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

B = Path(__file__).absolute().parent
SCRATCH = B.parent / "priority_literature_scratch"
SCRATCH.mkdir(exist_ok=True)
PIN = (B / "EXTERNAL_PIN.txt").read_text().strip()
RECEIPTS = json.loads((B / "INPUT_RECEIPTS.json").read_text())["files"]
CHECKER = B / "verify_custody.py"

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def atomic(path, data):
    tmp = path.with_name("." + path.name + ".tmp")
    tmp.write_text(data)
    os.replace(tmp, path)

def make_case(root):
    packet = root / "packet"
    inputs = root / "inputs"
    shutil.copytree(B, packet)
    for row in RECEIPTS:
        dst = inputs / row["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(B.parent / row["path"], dst)
    return packet, inputs

def mutate(name, packet, inputs):
    if name == "baseline":
        return PIN
    if name == "artifact_changed":
        path = packet / "PRIORITY_REPORT.md"
        path.write_bytes(path.read_bytes() + b"\nchanged\n")
    elif name == "artifact_missing":
        (packet / "PRIORITY_REPORT.md").unlink()
    elif name == "extra_artifact":
        (packet / "EXTRA.txt").write_text("extra")
    elif name == "extra_packet_directory":
        (packet / "EXTRA").mkdir()
    elif name == "symlink_artifact":
        path = packet / "PRIORITY_REPORT.md"
        path.unlink()
        path.symlink_to(packet / "README.md")
    elif name == "manifest_changed":
        path = packet / "FROZEN_MANIFEST.json"
        path.write_bytes(path.read_bytes() + b"\n")
    elif name == "wrong_external_pin":
        return ("0" if PIN[0] != "0" else "1") + PIN[1:]
    elif name == "local_pin_changed":
        (packet / "EXTERNAL_PIN.txt").write_text("0" * 64 + "\n")
    elif name == "original_changed":
        path = inputs / next(r["path"] for r in RECEIPTS if r["path"].endswith("/author/proof.md"))
        path.write_bytes(path.read_bytes() + b"\nchanged\n")
    elif name == "original_missing":
        (inputs / next(r["path"] for r in RECEIPTS if r["path"].endswith("/author/proof.md"))).unlink()
    elif name == "extra_original":
        (inputs / "intake/original/unsolved_math_prioritization/attempts/30001223/EXTRA.md").write_text("extra")
    elif name == "extra_original_directory":
        (inputs / "intake/original/unsolved_math_prioritization/attempts/30001223/EMPTY").mkdir()
    elif name == "original_symlink":
        path = inputs / next(r["path"] for r in RECEIPTS if r["path"].endswith("/author/proof.md"))
        path.unlink()
        path.symlink_to(inputs / "intake/SELECTED_PUBLIC_RECORD.json")
    elif name == "source_identity_changed":
        path = inputs / "intake/ROOT_SOURCE_IDENTITY.json"
        path.write_bytes(path.read_bytes() + b"\n")
    elif name == "peer_snapshot_changed":
        path = packet / "PEER_READ_SNAPSHOT.json"
        path.write_bytes(path.read_bytes() + b"\n")
    else:
        raise RuntimeError("unknown control")
    return PIN

cases = ["baseline", "artifact_changed", "artifact_missing", "extra_artifact",
         "extra_packet_directory", "symlink_artifact", "manifest_changed",
         "wrong_external_pin", "local_pin_changed", "original_changed",
         "original_missing", "extra_original", "extra_original_directory",
         "original_symlink", "source_identity_changed", "peer_snapshot_changed"]
rows = []
for optimized in [False, True]:
    for name in cases:
        with tempfile.TemporaryDirectory(prefix="custody-control-", dir=SCRATCH) as tmp:
            packet, inputs = make_case(Path(tmp))
            expected = mutate(name, packet, inputs)
            cmd = [sys.executable]
            if optimized:
                cmd.append("-O")
            cmd.extend(["-B", str(CHECKER), "--root", str(packet), "--input-root", str(inputs),
                        "--expected-manifest-sha256", expected])
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            try:
                response = json.loads(result.stdout)
            except ValueError as exc:
                raise RuntimeError("non-JSON checker response: " + result.stdout + result.stderr) from exc
            wanted_pass = name == "baseline"
            passed = (result.returncode == 0 and response.get("result") == "PASS")
            require(passed == wanted_pass, "incorrect acceptance: " + name)
            require(wanted_pass or (result.returncode != 0 and response.get("result") == "FAIL"),
                    "did not fail explicitly: " + name)
            rows.append({"case": name, "optimized": optimized, "expected": "PASS" if wanted_pass else "FAIL",
                         "exit_code": result.returncode, "response": response, "control_passed": True})
out = {"recorded_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "python": sys.version, "python_executable": sys.executable,
       "tested_provisional_manifest_sha256": PIN,
       "checker_sha256": hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
       "scope": "Actual baseline plus15 physical mutation cases, each in normal/-O. Reviewed trusted checker used against owned scratch copies of packet and all46 intake files. Final manifest is regenerated after this result is included; final baselines are separately reported externally.",
       "controls": rows, "controls_passed": len(rows),
       "substantive_proof_turns": 0}
atomic(B / "CUSTODY_TEST_RESULTS.json", json.dumps(out, indent=2) + "\n")
print(json.dumps({"controls_passed":len(rows),"tested_provisional_manifest_sha256":PIN,
                  "checker_sha256":out["checker_sha256"]},sort_keys=True))
