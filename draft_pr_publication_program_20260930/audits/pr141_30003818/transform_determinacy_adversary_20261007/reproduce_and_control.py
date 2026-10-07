"""Bounded child runner, preserving exact output and actual process custody."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import signal
import subprocess
import sys

root = Path(__file__).resolve().parent
python = "/opt/homebrew/opt/python@3.14/bin/python3.14"
jobs = [
    ("submitted_author_normal", root / "replay/author_replay/verify.py", []),
    ("old_independent_normal", root / "replay/independent_checks.py", []),
    ("new_clock_controls_normal", root / "joint_clock_and_moment_controls.py", []),
    ("new_clock_controls_optimized", root / "joint_clock_and_moment_controls.py", ["-O"]),
]
journal = []
for name, source, extra in jobs:
    args = [python, "-E", "-S", "-B", "-P", *extra, str(source)]
    begin = datetime.now(timezone.utc).isoformat()
    child = subprocess.Popen(args, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    timed_out = False
    try:
        out, err = child.communicate(timeout=55)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(child.pid, signal.SIGKILL)
        out, err = child.communicate()
    end = datetime.now(timezone.utc).isoformat()
    try:
        os.killpg(child.pid, 0)
        group_absent = False
    except ProcessLookupError:
        group_absent = True
    (root / (name + ".stdout")).write_bytes(out)
    (root / (name + ".stderr")).write_bytes(err)
    row = {"name": name, "source": str(source), "args": args, "pid": child.pid,
           "started_utc": begin, "ended_utc": end, "returncode": child.returncode,
           "reaped": child.poll() is not None, "process_group_absent": group_absent,
           "timed_out": timed_out,
           "stdout_size": len(out), "stdout_sha256": hashlib.sha256(out).hexdigest(),
           "stderr_size": len(err), "stderr_sha256": hashlib.sha256(err).hexdigest()}
    journal.append(row)
    (root / "CHILD_JOURNAL.json").write_text(json.dumps({"owner_actual_pid": os.getpid(), "children": journal}, indent=2) + "\n")
    if child.returncode or not group_absent or timed_out:
        print(json.dumps(row))
        raise RuntimeError("bounded reproduction failed")
    parsed = json.loads(out)
    print(json.dumps({"name": name, "assertions": parsed.get("assertions", parsed.get("independent_assertions")), "actual_child_pid": child.pid}))

original = root.parent / "original_submitted_attempt"
author = json.loads((root / "submitted_author_normal.stdout").read_text())
prior_author = json.loads((original / "verification.json").read_text())
old_independent = json.loads((root / "old_independent_normal.stdout").read_text())
prior_independent = json.loads((original / "review/independent_results.json").read_text())
new_normal = json.loads((root / "new_clock_controls_normal.stdout").read_text())
new_optimized = json.loads((root / "new_clock_controls_optimized.stdout").read_text())
if author != prior_author or old_independent != prior_independent:
    raise RuntimeError("old receipt replay differs")
for key in ("groups", "assertions", "weighted_CTMC_configurations", "negative_controls"):
    if new_normal[key] != new_optimized[key]:
        raise RuntimeError("normal/optimized control mismatch")
result = {"actual_pid": os.getpid(), "utc": datetime.now(timezone.utc).isoformat(),
          "verdict": "PASS", "author_receipt_semantic_equality": True,
          "old_independent_receipt_semantic_equality": True,
          "normal_optimized_new_control_equality": True,
          "author_assertions": author["assertions"], "old_independent_assertions": old_independent["independent_assertions"],
          "new_independent_assertions_per_mode": new_normal["assertions"],
          "all_children_reaped": all(x["reaped"] for x in journal),
          "all_process_groups_absent": all(x["process_group_absent"] for x in journal)}
(root / "REPRODUCTION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result))
