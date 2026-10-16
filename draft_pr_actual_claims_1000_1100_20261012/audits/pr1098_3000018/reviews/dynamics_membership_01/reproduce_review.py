#!/usr/bin/env python3
"""Run this family's own controls and authenticate its exact submitted inputs."""
import datetime
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    audit = root.parent.parent
    custody = json.loads((root / "INPUT_CUSTODY.json").read_text())
    inputs = []
    for row in custody["files"]:
        data = (audit / row["snapshot_path"]).read_bytes()
        actual = subprocess.run(["git", "show", custody["head_oid"] + ":" + row["repository_path"]],
                                capture_output=True, check=True).stdout
        require(data == actual and sha(data) == row["sha256"] and len(data) == row["bytes"],
                "submitted/Git custody mismatch: " + row["repository_path"])
        inputs.append({"path": row["repository_path"], "bytes": len(data),
                       "sha256": sha(data), "actual_git_equal": True})
    frozen = json.loads((root / "DERIVATION_FREEZE_RECEIPT.json").read_text())
    data = (root / frozen["file"]).read_bytes()
    require(sha(data) == frozen["sha256"] and len(data) == frozen["bytes"],
            "independent derivation changed")
    sources = []
    for row in json.loads((root / "SOURCE_ACQUISITION.json").read_text()):
        data = (root / row["pdf_relative_path"]).read_bytes()
        require(sha(data) == row["sha256"] and len(data) == row["bytes"], "source custody mismatch")
        sources.append({"name": row["name"], "bytes": len(data), "sha256": sha(data)})
    commands = []
    for optimized in (False, True):
        flags = ["-B"] + (["-O"] if optimized else [])
        suffix = "OPTIMIZED_RESUMED" if optimized else "NORMAL_RESUMED"
        for script, name in (("check_dynamics_membership.py", "CHECK_RESULTS_" + suffix + ".json"),
                             ("check_semantic_addendum.py", "SEMANTIC_ADDENDUM_" + suffix + ".json")):
            cmd = [sys.executable, *flags, script, name]
            start = time.monotonic()
            completed = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
            require(completed.returncode == 0, "control failed: " + completed.stderr)
            body = (root / name).read_bytes()
            require(json.loads(body) == json.loads(completed.stdout), "stdout/file result mismatch")
            commands.append({"argv": cmd, "returncode": 0, "result": name,
                             "bytes": len(body), "sha256": sha(body),
                             "duration_seconds": round(time.monotonic() - start, 3)})
            print(json.dumps({"finished": name, "sha256": sha(body)}), flush=True)
        for script, expected in (("check_dynamics_membership.py", "explicit optimized-runtime fault guard"),
                                 ("check_semantic_addendum.py", "explicit semantic-addendum optimized guard")):
            cmd = [sys.executable, *flags, script, "--self-test-invalid"]
            completed = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
            require(completed.returncode != 0 and expected in completed.stderr,
                    "explicit guard disappeared under requested runtime")
            commands.append({"argv": cmd, "returncode": completed.returncode,
                             "expected_failure": True, "expected_message": expected,
                             "stderr": completed.stderr})
    comparisons = []
    for prefix in ("CHECK_RESULTS_", "SEMANTIC_ADDENDUM_"):
        a = (root / (prefix + "NORMAL_RESUMED.json")).read_bytes()
        b = (root / (prefix + "OPTIMIZED_RESUMED.json")).read_bytes()
        require(a == b, "normal/optimized output differs")
        comparisons.append({"prefix": prefix, "normal_optimized_byte_equal": True,
                            "sha256": sha(a)})
    require((root / "CHECK_RESULTS_NORMAL.json").read_bytes() ==
            (root / "CHECK_RESULTS_NORMAL_RESUMED.json").read_bytes(),
            "previous completed normal result differs")
    receipt = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "head_oid": custody["head_oid"], "actual_git_files": inputs,
               "source_body_rehash": sources, "frozen_derivation_sha256": frozen["sha256"],
               "runtime": {"python": platform.python_version(), "platform": platform.platform()},
               "commands": commands, "comparisons": comparisons,
               "previous_normal_byte_equal": True,
               "resume_preserves_independent_chronology": True,
               "noncredited_failed_attempt": {
                   "description": "First resumed optimized execution completed checks but failed final result write ENOSPC.",
                   "counted_as_recorded_pass": False},
               "interim_optimized_stdout_only_attempt": {
                   "description": "A separate optimized rerun to /dev/null completed exit 0 and stdout matched prior normal JSON.",
                   "superseded_by_saved_reproduction_above": True}}
    (root / "REPRODUCTION_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "actual_git_files": len(inputs),
                      "sources": len(sources), "commands": len(commands),
                      "comparisons": comparisons}), flush=True)


if __name__ == "__main__":
    main()
