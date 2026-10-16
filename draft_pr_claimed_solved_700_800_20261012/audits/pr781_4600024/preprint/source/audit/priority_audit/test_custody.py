#!/usr/bin/env python3
"""Adversarial byte-custody tests on disposable owned copies; no source mutation."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-manifest-sha256", required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    original_input_root = root.parent
    names = [p.name for p in root.iterdir() if p.is_file()]
    output = []
    with tempfile.TemporaryDirectory(prefix="own-custody-test-", dir=root) as temp:
        scratch = Path(temp)
        for optimized in (False, True):
            for case in ("baseline", "artifact_change", "missing_artifact", "extra_file",
                         "extra_directory", "symlink_artifact", "manifest_change",
                         "wrong_external_pin", "pin_copy_change", "input_change"):
                tree = scratch / ("optimized" if optimized else "normal") / case / "priority_audit"
                tree.mkdir(parents=True)
                for name in names:
                    shutil.copyfile(root / name, tree / name)
                input_root = original_input_root
                target = tree / "REPORT.md"
                pin = args.expected_manifest_sha256
                if case == "artifact_change":
                    target.write_bytes(target.read_bytes() + b"X")
                elif case == "missing_artifact":
                    target.unlink()
                elif case == "extra_file":
                    (tree / "unexpected").write_bytes(b"")
                elif case == "extra_directory":
                    (tree / "__pycache__").mkdir()
                elif case == "symlink_artifact":
                    target.unlink()
                    target.symlink_to(root / "REPORT.md")
                elif case == "manifest_change":
                    f = tree / "FROZEN_MANIFEST.json"
                    f.write_bytes(f.read_bytes() + b" ")
                elif case == "wrong_external_pin":
                    pin = "0" * 64
                elif case == "pin_copy_change":
                    (tree / "EXTERNAL_PIN.txt").write_text("0" * 64 + "\n")
                elif case == "input_change":
                    input_root = tree.parent / "copied_inputs"
                    rows = json.loads((root / "INPUT_RECEIPTS.json").read_text())
                    for row in rows:
                        name = row["relative_input"]
                        dst = input_root / name
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copyfile(original_input_root / name, dst)
                    f = input_root / rows[0]["relative_input"]
                    f.write_bytes(f.read_bytes() + b"X")
                command = [sys.executable]
                if optimized:
                    command.append("-O")
                command += ["-B", str(root / "verify_custody.py"), "--root", str(tree),
                            "--input-root", str(input_root),
                            "--expected-manifest-sha256", pin]
                result = subprocess.run(command, capture_output=True, text=True)
                expected_success = case == "baseline"
                success = (result.returncode == 0) == expected_success
                try:
                    observed = json.loads(result.stdout)
                except ValueError:
                    observed = {"stdout": result.stdout, "stderr": result.stderr}
                output.append({"case": case, "optimized": optimized,
                               "test_pass": success, "observed": observed})
    all_pass = all(row["test_pass"] for row in output)
    print(json.dumps({"result": "PASS" if all_pass else "FAIL", "cases": output}, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
