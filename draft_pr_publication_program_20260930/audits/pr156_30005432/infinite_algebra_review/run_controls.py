#!/usr/bin/env python3
"""Reproduce ordinary, optimized, mutant, and original-verifier controls."""
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
original = root.parent / "original_submission/files/unsolved_math_prioritization/attempts/30005432/verify.py"
records = []


def run_case(name, script, optimized, args=(), expected_code=0, expected_verdict=None):
    command = [sys.executable] + (["-O"] if optimized else []) + [str(script)] + list(args)
    process = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
    stdout = root / f"{name}.stdout.txt"
    stderr = root / f"{name}.stderr.txt"
    stdout.write_text(process.stdout)
    stderr.write_text(process.stderr)
    parsed = None
    if process.stdout.strip():
        try:
            parsed = json.loads(process.stdout)
        except json.JSONDecodeError:
            pass
    if process.returncode != expected_code:
        raise RuntimeError(f"{name}: return code {process.returncode}; expected {expected_code}")
    if expected_verdict is not None and (not isinstance(parsed, dict) or parsed.get("verdict") != expected_verdict):
        raise RuntimeError(f"{name}: unexpected output verdict")
    records.append({"name": name, "command": command, "returncode": process.returncode, "expected_returncode": expected_code, "stdout": stdout.name, "stderr": stderr.name, "parsed": parsed})
    return parsed


for optimized in (False, True):
    suffix = "optimized" if optimized else "normal"
    run_case(f"independent_{suffix}", root / "independent_verify.py", optimized, expected_verdict="PASS_INDEPENDENT_EXACT_CONTROLS")
    for mutant in ("noncharacter_epsilon", "wrong_component", "wrong_star", "two_sided_claim"):
        run_case(f"independent_{mutant}_{suffix}", root / "independent_verify.py", optimized, ("--mutant", mutant), 1, "REJECTED")
    run_case(f"original_{suffix}", original, optimized, expected_verdict="PASS_EXACT_COUNTEREXAMPLE_CONTROLS")

run_case("original_noncharacter_epsilon_normal", root / "original_mutant_replay.py", False, expected_code=1)
survival = run_case("original_noncharacter_epsilon_optimized", root / "original_mutant_replay.py", True, expected_verdict="PASS_EXACT_COUNTEREXAMPLE_CONTROLS")
normal, optimized = records[0]["parsed"], records[6]["parsed"]
if normal["checks"] != optimized["checks"] or normal["categories"] != optimized["categories"]:
    raise RuntimeError("Independent check coverage differs under -O")
receipt = {"completed_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"), "verdict": "PASS_REPRODUCTION_AND_NEGATIVE_CONTROLS", "independent_check_count_per_mode": normal["checks"], "independent_mutants_rejected_per_mode": 4, "original_optimized_mutant_survives": survival["verdict"], "records": records}
(root / "RUN_RECEIPT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
print(json.dumps({key: value for key, value in receipt.items() if key != "records"}, indent=2, sort_keys=True))
