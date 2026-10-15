#!/usr/bin/env python3
"""Copy exact frozen controls into ignored isolated directories and replay them."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE.parent / "source_snapshot"
TMP = HERE / "tmp" / "original_replay"
TMP.mkdir(parents=True, exist_ok=True)
receipts = []
history_path = HERE / "original_replay_attempts.json"
current_path = HERE / "original_replay_receipts.json"
history = json.loads(history_path.read_text()) if history_path.exists() else []
if current_path.exists():
    previous = json.loads(current_path.read_text())
    if previous not in history:
        history.append(previous)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(name, original_name, script_bytes, expected_failure=None):
    folder = TMP / name
    folder.mkdir(exist_ok=True)
    script = folder / Path(original_name).name
    script.write_bytes(script_bytes)
    command = [sys.executable, str(script)]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(command, cwd=folder, text=True, capture_output=True)
    outputs = [{"path": str(p.relative_to(HERE)), "sha256": sha(p)}
               for p in sorted(folder.iterdir()) if p.is_file() and p != script]
    receipt = {"name": name, "timestamp_utc": started, "command": command,
               "cwd": str(folder), "script_sha256": sha(script),
               "original_script_sha256": sha(SNAPSHOT/original_name),
               "return_code": result.returncode, "stdout": result.stdout,
               "stderr": result.stderr, "outputs": outputs,
               "expected_failure": expected_failure}
    if expected_failure is not None:
        receipt["expected_outcome_observed"] = result.returncode != 0 and expected_failure in result.stderr
    else:
        receipt["expected_outcome_observed"] = result.returncode == 0
        for p in folder.glob("*.json"):
            frozen = SNAPSHOT / Path(original_name).parent / p.name
            if frozen.exists():
                a, b = json.loads(p.read_text()), json.loads(frozen.read_text())
                receipt.setdefault("saved_result_comparison", {})[p.name] = {"structurally_equal": a == b,
                    "actual_sha256": sha(p), "saved_sha256": sha(frozen)}
    receipts.append(receipt)
    return receipt


original = (SNAPSHOT/"check_controls.py").read_bytes()
run("baseline", "check_controls.py", original)
historical_name = "independent_review/independent_checks.py"
run("historical_independent_baseline", historical_name,
    (SNAPSHOT/historical_name).read_bytes())
mutations = [
    ("chordal_factor_missing", b"-4*(x-y).dot(x-y)", b"-(x-y).dot(x-y)", "chordal_metric_identity"),
    ("nondecaying_tail", b"bound2=4*D*D/", b"bound2=4*D*D*R**4/", "tail_bound_derivative"),
    ("touching_regions", b"7*D>3*D+3*D", b"6*D>3*D+3*D", "two_fixed_point_regions_disjoint"),
]
for name, old, new, expected in mutations:
    if original.count(old) != 1:
        raise AssertionError("Mutation location must occur exactly once: "+name)
    run(name, "check_controls.py", original.replace(old, new), expected)

out = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "helper_sha256": sha(Path(__file__)), "python_executable": sys.executable,
       "receipts": receipts, "all_expected_outcomes": all(r["expected_outcome_observed"] for r in receipts),
       "scope": "Actual exact frozen candidate algebra-script replay and three actual code mutants. No theorem certification."}
history.append(out)
history_path.write_text(json.dumps(history, indent=2)+"\n")
current_path.write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps({"all_expected_outcomes": out["all_expected_outcomes"],
                  "cases": [{"name": r["name"], "return_code": r["return_code"],
                             "expected_outcome_observed": r["expected_outcome_observed"],
                             "saved_result_comparison": r.get("saved_result_comparison")} for r in receipts]}, indent=2))
if not out["all_expected_outcomes"]:
    raise SystemExit(1)
