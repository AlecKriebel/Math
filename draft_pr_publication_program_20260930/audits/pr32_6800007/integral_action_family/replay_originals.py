#!/usr/bin/env python3
"""Replay the two frozen originals in isolated ignored copies; never write inputs.

Run with /usr/bin/python3. Output directory must be below this family's tmp/.
This script checks bytes, exit status and parsed output, and reports no topology
certification. It does not import either original program into this process.
"""
import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

FAMILY = pathlib.Path(__file__).resolve().parent
SNAPSHOT = FAMILY.parent / "source_snapshot"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="tmp/replay_originals")
    args = parser.parse_args()
    out = (FAMILY / args.out).resolve()
    assert out.is_relative_to(FAMILY / "tmp"), "replays belong in ignored family tmp"
    out.mkdir(parents=True, exist_ok=True)
    receipt = {"python": sys.version, "executable": sys.executable, "runs": []}
    for source, expected, tag in (("verify.py", "verification.json", "checker"),
                                  ("review/independent_checks.py", "review/independent_results.json", "legacy_independent")):
        run = out / tag
        run.mkdir(exist_ok=True)
        copy = run / pathlib.Path(source).name
        shutil.copyfile(SNAPSHOT / source, copy)
        assert digest(copy) == digest(SNAPSHOT / source)
        process = subprocess.run([sys.executable, copy.name], cwd=str(run),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (run / "stdout.json").write_bytes(process.stdout)
        (run / "stderr.txt").write_bytes(process.stderr)
        data = json.loads(process.stdout)
        item = {"source": source, "source_sha256": digest(copy),
                "expected_output": expected, "expected_output_sha256": digest(SNAPSHOT / expected),
                "actual_output_sha256": hashlib.sha256(process.stdout).hexdigest(),
                "exit_code": process.returncode, "stderr_bytes": len(process.stderr),
                "byte_identical_to_frozen_output": process.stdout == (SNAPSHOT / expected).read_bytes(),
                "parsed_pass": data.get("pass"),
                "assertions": data.get("assertions"), "torsion_cases": data.get("torsion_cases")}
        receipt["runs"].append(item)
        assert process.returncode == 0 and not process.stderr, item
        assert item["byte_identical_to_frozen_output"] and item["parsed_pass"] is True, item
    print(json.dumps(receipt, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
