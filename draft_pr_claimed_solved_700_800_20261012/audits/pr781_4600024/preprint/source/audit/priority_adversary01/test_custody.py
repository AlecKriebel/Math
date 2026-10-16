#!/usr/bin/env python3
"""Probe copies only; return results on stdout and leave the reviewed packet unchanged."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

class TestError(Exception):
    pass

def require(condition, message):
    if not condition:
        raise TestError(message)

def run(root, source_root, manifest_pin, checker_pin, optimized):
    command = [sys.executable, "-B"]
    if optimized:
        command.append("-O")
    command += [str(root / "verify_custody.py"), "--expected-manifest-sha256", manifest_pin,
                "--expected-checker-sha256", checker_pin, "--source-root", str(source_root)]
    result = subprocess.run(command, capture_output=True, text=True, timeout=40)
    return {"returncode": result.returncode,
            "receipt": json.loads(result.stdout), "stderr": result.stderr.strip()}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-manifest-sha256", required=True)
    parser.add_argument("--expected-checker-sha256", required=True)
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    root = Path(__file__).absolute().parent
    source_root = (args.source_root or root.parent).absolute()
    results = []
    originals = [p for p in root.iterdir() if p.is_file()]
    for optimized in [False, True]:
        base = run(root, source_root, args.expected_manifest_sha256,
                   args.expected_checker_sha256, optimized)
        require(base["returncode"] == 0 and base["receipt"]["result"] == "PASS", "baseline failed")
        results.append({"case": "baseline", "optimized": optimized, **base})
    with tempfile.TemporaryDirectory(prefix="_custody_probe_", dir=root) as directory:
        temp = Path(directory)
        for optimized in [False, True]:
            for case in ["artifact_tamper", "extra_file", "extra_directory", "symlink",
                         "wrong_manifest_pin", "wrong_checker_pin",
                         "checker_tamper", "forged_manifest", "input_tamper"]:
                copy = temp / ("packet_" + case + str(optimized))
                copy.mkdir()
                for original in originals:
                    shutil.copyfile(original, copy / original.name)
                manifest_pin = args.expected_manifest_sha256
                checker_pin = args.expected_checker_sha256
                inputs = source_root
                if case == "artifact_tamper":
                    path = copy / "VERDICT.json"
                    path.write_bytes(path.read_bytes() + b" ")
                elif case == "extra_file":
                    (copy / "unexpected.json").write_text("{}")
                elif case == "extra_directory":
                    (copy / "unexpected").mkdir()
                elif case == "symlink":
                    (copy / "unexpected.json").symlink_to(copy / "VERDICT.json")
                elif case == "wrong_manifest_pin":
                    manifest_pin = "0" * 64
                elif case == "wrong_checker_pin":
                    checker_pin = "0" * 64
                elif case == "checker_tamper":
                    path = copy / "verify_custody.py"
                    path.write_bytes(path.read_bytes() + bytes([10]) + b"# harmless tamper" + bytes([10]))
                elif case == "forged_manifest":
                    value = json.loads((copy / "MANIFEST.json").read_text())
                    value["files"]["VERDICT.json"]["sha256"] = "0" * 64
                    (copy / "MANIFEST.json").write_text(json.dumps(value))
                elif case == "input_tamper":
                    inputs = temp / ("inputs_" + str(optimized))
                    pins = json.loads((copy / "INPUTS.json").read_text())["inputs"]
                    for name in pins:
                        target = inputs / name
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copyfile(source_root / name, target)
                    name = next(name for name in pins if name.endswith("PROOF.md"))
                    target = inputs / name
                    target.write_bytes(target.read_bytes() + b" ")
                result = run(copy, inputs, manifest_pin, checker_pin, optimized)
                require(result["returncode"] != 0 and result["receipt"]["result"] == "FAIL",
                        "tamper accepted: " + case)
                results.append({"case": case, "optimized": optimized, **result})
    print(json.dumps({
        "result": "PASS",
        "test_basis_manifest_sha256": args.expected_manifest_sha256,
        "checker_sha256": args.expected_checker_sha256,
        "cases": results,
        "root_packet_modified": False,
        "temporary_copy_directory_removed": True
    }, indent=2))

if __name__ == "__main__":
    main()
